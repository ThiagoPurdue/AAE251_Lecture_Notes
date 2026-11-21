"""Figures and values of 1.5 Bernoulli and Pitot Static (notes/chapter-1/bernoulli-and-pitot-static.md).

Every number printed on the page is computed in values() and recorded with record("p15", ...).
The figures are drawn from the same numbers.

Two ideal-flow (inviscid, incompressible) calculations of this module draw real flow patterns
instead of sketches; neither is taught on the page, which says only that the pattern was
computed:
  - _panel_solve(): a constant-strength source and vortex panel method (the Hess and Smith
    method) for a NACA 4-digit section, with the Kutta condition at the trailing edge. It gives
    the velocity anywhere around the section; the streamlines are traced from it.
  - _half_body(): the axisymmetric Rankine half-body (a uniform stream plus a point source),
    the classical ideal-flow model of a round-nosed probe. Its surface pressure shows where the
    static pressure of the free stream is felt again behind the nose.

The panel method, the half-body and the streamline tracer stay in this module: no other page
uses them. Published sources of the two methods: Hess, J. L., and Smith, A. M. O., "Calculation
of potential flow about arbitrary bodies", Progress in Aerospace Sciences 8 (1967), 1-138 (the
panel method); Anderson, J. D., Fundamentals of Aerodynamics, McGraw-Hill (a source in a uniform
stream, the Rankine half-body).
"""
from chapter_1.common import *

PAGE = "p15"

# ===================================================================== worked-example data (choices, not constants)
# Example 1: cooling-air duct of an avionics bay, fed on the ground (sea-level standard air)
EX1 = dict(D1=0.12, D2=0.09, V1=20.0)            # m, m, m/s
# Example 2: pitot-static reading of an uncrewed aircraft at 6,000 m
EX2 = dict(h=6000.0, dp=2000.0)                   # m, Pa
# Example 3: pitot-static tube in a propeller slipstream on the ground, water manometer
EX3 = dict(h_man=0.065)                           # m of water
# Example 4: a small cargo airplane takes off from a sea-level runway with the pitot cover still on
# (in the simplest case the cover seals the ram-air inlet and the drain hole); it climbs at 65 m/s true airspeed.
EX4 = dict(ha=150.0, hb=300.0, V=65.0)            # m, m, m/s
# Draining tank (short example in the text)
TANK_Z = 2.0                                       # m of water above the hole

ALPHA_SECTION = 4.0                                # deg, the airfoil of the stream-tube figure, nose up


# ===================================================================== ideal-flow helpers
def _naca_ccw(code, n):
    """NACA 4-digit outline, chord 1, closed trailing edge, ordered trailing edge -> lower surface
    -> leading edge -> upper surface -> trailing edge (counterclockwise: the left normal of each
    panel points out of the body). Uses the shared naca4() with the closed trailing edge."""
    s = naca4(code, n=n, closed_te=True)
    return np.r_[np.c_[s["xl"][::-1], s["yl"][::-1]], np.c_[s["xu"][1:], s["yu"][1:]]]


def _rotate_nose_up(xy, deg, about=(0.0, 0.0)):
    """Points turned clockwise by deg about `about` (a section pitched nose up in a flow from the left)."""
    return rotate_xy(xy, -deg, about)


def _panel_influence(P, S, E, self_mask=None):
    """Velocity at points P (M, 2) induced by unit-strength constant source and vortex panels
    from S to E (N, 2 each). Returns src, vor (M, N, 2) in global axes and the panel tangents
    and normals. Vortex positive counterclockwise."""
    d = E - S
    L = np.hypot(d[:, 0], d[:, 1])
    t = d / L[:, None]
    n = np.c_[-t[:, 1], t[:, 0]]
    r = P[:, None, :] - S[None, :, :]
    xi = (r * t[None]).sum(-1)
    eta = (r * n[None]).sum(-1)
    if self_mask is not None:
        eta = np.where(self_mask, 0.0, eta)
    r1 = np.hypot(xi, eta)
    r2 = np.hypot(xi - L[None], eta)
    beta = np.arctan2(eta, xi - L[None]) - np.arctan2(eta, xi)
    beta = np.where(beta < -math.pi, beta + 2 * math.pi, beta)
    beta = np.where(beta > math.pi, beta - 2 * math.pi, beta)
    if self_mask is not None:
        beta = np.where(self_mask, math.pi, beta)
    lg = np.log(r1 / r2) / (2 * math.pi)
    bb = beta / (2 * math.pi)
    src = lg[..., None] * t[None] + bb[..., None] * n[None]
    vor = -bb[..., None] * t[None] + lg[..., None] * n[None]
    return src, vor, t, n


def _panel_solve(xy):
    """Hess-Smith panel solution for a closed counterclockwise outline xy in a unit stream along +x.
    Returns vel(P) -> (M, 2) velocity, the surface tangential speeds at the panel midpoints, the
    midpoints, and the circulation (counterclockwise positive)."""
    S, E = xy[:-1], xy[1:]
    N = len(S)
    C = 0.5 * (S + E)
    src, vor, t, n = _panel_influence(C, S, E, np.eye(N, dtype=bool))
    Vinf = np.array([1.0, 0.0])
    A = np.zeros((N + 1, N + 1))
    b = np.zeros(N + 1)
    A[:N, :N] = (src * n[:, None, :]).sum(-1)
    A[:N, N] = (vor * n[:, None, :]).sum(-1).sum(1)
    b[:N] = -(n @ Vinf)
    At = (src * t[:, None, :]).sum(-1)
    Atv = (vor * t[:, None, :]).sum(-1).sum(1)
    A[N, :N] = At[0] + At[-1]                     # Kutta: equal speeds leaving the trailing edge
    A[N, N] = Atv[0] + Atv[-1]
    b[N] = -(t[0] @ Vinf + t[-1] @ Vinf)
    sol = np.linalg.solve(A, b)
    sig, gam = sol[:N], sol[N]

    def vel(P):
        P = np.atleast_2d(np.asarray(P, float))
        s, v, _, _ = _panel_influence(P, S, E)
        return Vinf + (s * sig[None, :, None]).sum(1) + gam * v.sum(1)

    Vt = At @ sig + Atv * gam + t @ Vinf
    return vel, Vt, C, gam * float(np.sum(np.hypot(*(E - S).T)))


def _trace(vel, p0, ds=0.004, x_end=1.7, n_max=4000):
    """A streamline from p0, traced downstream with fixed arc-length RK4 steps until x > x_end."""
    p = np.asarray(p0, float)
    pts = [p]

    def f(q):
        v = vel(q)[0]
        return v / np.hypot(*v)
    for _ in range(n_max):
        k1 = f(p)
        k2 = f(p + 0.5 * ds * k1)
        k3 = f(p + 0.5 * ds * k2)
        k4 = f(p + ds * k3)
        p = p + ds / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        pts.append(p)
        if p[0] > x_end:
            break
    return np.array(pts)


def _half_body(a=1.0, U=1.0, n=8000):
    """Axisymmetric Rankine half-body: a uniform stream U along +x plus a point source at the
    origin of strength Q = 4 pi U a^2. The nose (stagnation point) is at x = -a; far downstream the
    body radius tends to 2a. Returns the surface (x, r) from the nose aft, the surface pressure
    (p_surface - p)/q, and the Stokes stream function psi(x, r) (zero on the body)."""
    Q = 4.0 * math.pi * U * a * a
    phi = np.linspace(math.pi - 1e-6, 0.03, n)               # polar angle from +x about the source
    r = np.sqrt(2.0 * a * a * (1.0 + np.cos(phi)))
    rho = r / np.sin(phi)
    x = rho * np.cos(phi)
    u = U + Q / (4 * math.pi) * x / rho ** 3
    v = Q / (4 * math.pi) * r / rho ** 3
    cp = 1.0 - (u * u + v * v) / (U * U)

    def psi(xx, rr):
        rh = np.sqrt(xx * xx + rr * rr)
        return 0.5 * U * rr * rr - Q / (4 * math.pi) * (1.0 + xx / np.maximum(rh, 1e-12))
    return x, r, cp, psi


def _psi_line(psi, level, x, r_hi):
    """Radius r(x) > 0 where the stream function equals `level` (bisection at each x)."""
    out = np.empty_like(x)
    for i, xx in enumerate(x):
        lo, hi = 1e-9, r_hi
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if psi(xx, mid) < level:
                lo = mid
            else:
                hi = mid
        out[i] = 0.5 * (lo + hi)
    return out


# ===================================================================== the computed numbers
def _ex1():
    D1, D2, V1 = EX1["D1"], EX1["D2"], EX1["V1"]
    A1, A2 = float(area_circle(D1)), float(area_circle(D2))
    V2 = continuity_speed(V1, A1, A2)
    Q = volume_flow(A1, V1)
    mdot = mass_flow(RHO_SL, A1, V1)
    dp = bernoulli_p2(0.0, V1, V2, RHO_SL) * -1.0          # p1 - p2
    h = manometer_height(dp)
    return dict(A1=A1, A2=A2, V2=V2, Q=Q, mdot=mdot, dp=dp, h=h, ratio=A1 / A2)


def _ex2():
    h, dp = EX2["h"], EX2["dp"]
    T, p, rho = standard(h)
    a = LAYERS[0][1]                                   # K/m, the troposphere lapse rate
    n = G0 / (a * R_AIR)
    V = pitot_speed(dp, 0.0, rho)
    V_dial = pitot_speed(dp, 0.0, RHO_SL)
    return dict(T=T, rho=rho, n=n, expo=-(n + 1.0), Tr=T / T_SL, V=V, V_dial=V_dial)


def _ex3():
    dp = manometer_dp(EX3["h_man"])
    return dict(dp=dp, V=pitot_speed(dp, 0.0, RHO_SL))


def _ex4():
    """The pitot cover left on: the pitot line holds the runway's static pressure (the airplane was at
    rest when the cover went on). The four cases of the blockage figure at the same altitudes."""
    V = EX4["V"]
    trapped = P_SL                                     # Pa, static pressure of the sea-level runway
    hs = (0.0, EX4["ha"], EX4["hb"])
    st = {h: standard(h) for h in hs}
    p = {h: float(st[h][1]) for h in hs}
    rho = {h: float(st[h][2]) for h in hs}
    q = {h: float(dynamic_pressure(rho[h], V)) for h in hs}
    dial = lambda d: math.sqrt(2.0 * max(d, 0.0) / RHO_SL)      # the dial: sea-level density, stops at 0
    cases = {}
    for key in ("open", "cover", "inlet", "static"):
        c = dict(pitot={}, static={}, dp={}, dial={})
        for h in hs:
            if key == "open":
                pit, sta = p[h] + q[h], p[h]
            elif key == "cover":                        # inlet and drain closed on the ground
                pit, sta = trapped, p[h]
            elif key == "inlet":                        # inlet closed, drain open: the line vents to p
                pit, sta = p[h], p[h]
            else:                                       # static port closed on the ground
                pit, sta = p[h] + q[h], trapped
            c["pitot"][h], c["static"][h], c["dp"][h], c["dial"][h] = pit, sta, pit - sta, dial(pit - sta)
        cases[key] = c
    # where the covered tube shows the true airspeed (its gap equals the healthy one): bisection
    lo, hi = 0.0, EX4["hb"]
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        f = (trapped - float(standard(mid)[1])) - float(dynamic_pressure(float(standard(mid)[2]), V))
        lo, hi = (mid, hi) if f < 0 else (lo, mid)
    # where the static-blocked gap closes
    lo2, hi2 = 0.0, EX4["hb"]
    for _ in range(80):
        mid = 0.5 * (lo2 + hi2)
        T_, p_, r_ = standard(mid)
        f = float(p_) + float(dynamic_pressure(float(r_), V)) - trapped
        lo2, hi2 = (mid, hi2) if f > 0 else (lo2, mid)
    return dict(V=V, trapped=trapped, hs=hs, p=p, rho=rho, q=q, cases=cases, h_true=0.5 * (lo + hi),
                h_close=0.5 * (lo2 + hi2))


# ===================================================================== figures
def pressure_and_shear():
    """F0: pressure pushes normal to the surface, shear drags along it; summed over the surface
    they make one resultant R, whose parts across and along the free stream are lift and drag
    (the two sides of the rectangle whose diagonal is R). Two panels at one scale of their own."""
    FW, FH = 6.5, 2.62
    fig = plt.figure(figsize=(FW, FH))
    wl = 0.45                                            # the left panel's share of the width
    axl = fig.add_axes([0.0, 0.0, wl, 1.0])
    axr = fig.add_axes([wl, 0.0, 1.0 - wl, 1.0])
    for ax, w, (ylo, yhi), x0 in ((axl, wl, (-0.33, 0.88), None), (axr, 1.0 - wl, (-0.28, 0.73), -0.30)):
        ax.axis("off")
        ax.set_aspect("equal")
        span = (yhi - ylo) * (w * FW) / FH
        ax.set_ylim(ylo, yhi)
        ax.set_xlim((-0.5 * span, 0.5 * span) if x0 is None else (x0, x0 + span))
    fig.canvas.draw()
    vy = 0.36                                            # the height of the left free-stream arrow
    # left: a piece of a body surface, enlarged (a hatched band under the surface line)
    ax = axl
    xs = np.linspace(-0.68, 0.68, 200)
    ys = -0.05 * xs ** 2
    hatched_wall(ax, xs, ys, ys - 0.07)
    ax.plot(xs, ys, color=INK, lw=LW_OUTLINE, zorder=3.5)
    text(ax, (0.40, -0.05 * 0.40 ** 2 - 0.07), "body surface", direction=-90, dist=6)
    xe = -0.30
    P = np.array([xe, -0.05 * xe ** 2])
    tv = np.array([1.0, -0.10 * xe])
    tv /= np.hypot(*tv)
    nv = np.array([-tv[1], tv[0]])                      # out of the body
    seg = np.array([P - 0.12 * tv, P + 0.12 * tv])
    ax.plot(seg[:, 0], seg[:, 1], color=INK, lw=4.5, solid_capstyle="butt", zorder=4)
    text(ax, P - 0.07 * nv, r"element $\Delta s$", direction=-90, dist=6)
    # pressure force: normal to the surface, pushing in, ending at the element; shear force:
    # tangential, downstream, starting at the element just past the pressure arrow's head
    off = 0.035
    kind_arrow(ax, P + 0.74 * nv, P + off * nv, "force", None)
    text(ax, P + 0.70 * nv, r"pressure force $\Delta F_n$," + "\nnormal to the surface", direction=0, dist=7,
         ha="left", va="top")
    s0 = P + 0.06 * tv + off * nv
    kind_arrow(ax, s0, s0 + 0.50 * tv, "force", None)
    text(ax, s0 + 0.50 * tv, r"shear force $\Delta F_t$," + "\nalong the surface", direction=80, dist=9,
         ha="center", va="bottom")
    kind_arrow(ax, (-0.66, vy), (-0.46, vy), "velocity", None)
    text(ax, (-0.61, vy), r"$V_\infty$", direction=90, dist=4, color=BLUE)
    # right: the airfoil (NACA 2412, 4 degrees nose up) and the total force on it, with its two parts
    ax = axr
    c = 1.0
    sec = naca4("2412", n=161, chord=c)
    xy = _rotate_nose_up(sec["outline"], ALPHA_SECTION)
    opaque(ax.add_patch(Polygon(xy, closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=3)))
    i4 = int(np.argmin(abs(sec["x"] - 0.25 * c)))
    o = _rotate_nose_up(np.array([[sec["x"][i4], sec["yc"][i4]]]), ALPHA_SECTION)[0]   # quarter chord
    L, D = 0.62, 0.21
    gray = dict(color=GRAY, lw=LW_THIN, ls=(0, (3, 2)), zorder=2)
    ax.plot([o[0], o[0] + D], [o[1] + L, o[1] + L], **gray)          # the rectangle whose diagonal is R
    ax.plot([o[0] + D, o[0] + D], [o[1] + 0.06, o[1] + L], **gray)
    kind_arrow(ax, o, o + np.array([0.0, L]), "force", None)
    text(ax, o + np.array([0.0, 0.70 * L]), "lift, $L$", direction=180, dist=6)
    kind_arrow(ax, o, o + np.array([D, L]), "force", None)
    text(ax, o + np.array([D, L]), "resultant, $R$", direction=10, dist=7, ha="left")
    kind_arrow(ax, o, o + np.array([D, 0.0]), "force", None, zorder=8)
    xl = o[0] + 0.5 * D
    low = _rotate_nose_up(np.c_[sec["xl"], sec["yl"]], ALPHA_SECTION)
    y_low = float(np.interp(xl, low[:, 0], low[:, 1]))
    text(ax, (xl, y_low), "drag, $D$", direction=-90, dist=5)
    vr = 0.30
    kind_arrow(ax, (-0.27, vr), (-0.07, vr), "velocity", None)
    text(ax, (-0.22, vr), r"$V_\infty$", direction=90, dist=4, color=BLUE)
    close_to(float(np.dot(tv, nv)), 0.0, 1e-12, "the pressure force is normal to the shear force")
    assert D >= pt(ax, 3 * 11.0), "the drag arrow is at least three head lengths long"
    save_figure(fig, "p15-pressure-and-shear")


def stream_tube():
    """F1: streamlines around a NACA 2412 section (ideal flow) and one stream tube with two stations."""
    xy = _rotate_nose_up(_naca_ccw("2412", 81), ALPHA_SECTION)
    vel, _, _, _ = _panel_solve(xy)
    fig, ax = new_axes(6.5, 3.4)
    x_l, x_r = -0.72, 1.56
    set_frame(ax, x_l, x_r, -0.50, 0.66)
    seeds = [-0.44, -0.28, 0.02, 0.17, 0.40, 0.56]
    lines = {y0: _trace(vel, (x_l, y0), x_end=x_r) for y0 in seeds}
    lo, hi = lines[0.02], lines[0.17]
    xg = np.linspace(x_l, x_r - 0.01, 700)
    ylo = np.interp(xg, lo[:, 0], lo[:, 1])
    yhi = np.interp(xg, hi[:, 0], hi[:, 1])
    ax.add_patch(Polygon(np.r_[np.c_[xg, ylo], np.c_[xg[::-1], yhi[::-1]]], closed=True, fc=HIGHLIGHT, ec="none",
                         zorder=1))
    for y0, s in lines.items():
        ln = ax.plot(s[:, 0], s[:, 1], color=INK, lw=1.5 if y0 in (0.02, 0.17) else 1.0, zorder=2)[0]
        motion_heads(ax, s[:, 0], s[:, 1], (0.70,) if y0 in (0.02, 0.17) else (0.72, 0.93), line=ln)
    opaque(ax.add_patch(Polygon(xy, closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=3)))
    text(ax, (0.45, -0.075), "airfoil", direction=-90, dist=4)
    # the two stations: section lines across the tube, normal to the local flow, and the velocity
    # arrows along the local flow (one length scale for both)
    x1s, x2s = -0.40, 0.24
    out = {}
    S = 0.16                                        # arrow length per unit free-stream speed: one scale
    for xs, k in ((x1s, 1), (x2s, 2)):
        yl, yh = float(np.interp(xs, xg, ylo)), float(np.interp(xs, xg, yhi))
        cpt = np.array([xs, 0.5 * (yl + yh)])
        v = vel(cpt[None, :])[0]
        u = v / np.hypot(*v)
        nn = np.array([-u[1], u[0]])
        w = (yh - yl) * u[0]                         # the width normal to the flow (u[0] = cos of the flow angle)
        ends = np.array([cpt - 0.5 * w * nn, cpt + 0.5 * w * nn])
        out[k] = dict(w=w, V=float(np.hypot(*v)), yl=yl, yh=yh, c=cpt, u=u, ends=ends)
        ax.plot(ends[:, 0], ends[:, 1], color=INK, lw=1.4, ls=(0, (3, 1.5)), zorder=4)
        a0 = cpt + 0.015 * u
        kind_arrow(ax, a0, a0 + S * out[k]["V"] * u, "velocity", None)
    w1, w2, V1, V2 = out[1]["w"], out[2]["w"], out[1]["V"], out[2]["V"]
    # two-dimensional continuity: width times speed is the same at both stations (within 2%)
    assert abs(w1 * V1 - w2 * V2) / (w1 * V1) < 0.02, (w1, w2, V1, V2)
    assert w2 < w1 and V2 > V1
    # the arrows lie along the local flow: the arrow at station 1 climbs with the tube
    assert out[1]["u"][1] > 0.05, out[1]["u"]
    text(ax, (x1s, out[1]["yl"]), "station 1:\narea $A_1$, speed $V_1$", direction=-90, dist=6)
    text(ax, (x2s + 0.18, out[2]["yh"]), "station 2: area $A_2$, speed $V_2$", direction=90, dist=5)
    xt = 1.28
    text(ax, (xt, 0.5 * float(np.interp(xt, xg, ylo) + np.interp(xt, xg, yhi))), "stream tube", backing=HIGHLIGHT)
    s = lines[-0.44]
    xq = 0.50
    yq = float(np.interp(xq, s[:, 0], s[:, 1]))
    callout(ax, (xq, yq + 0.004), "streamline", at=(xq + 0.20, yq + 0.075), ha="left")
    stream_tube.out = out
    save_figure(fig, "p15-stream-tube")
    return out


def continuity_slabs():
    """F2: in the same time dt the same mass crosses both stations: the narrow slab is longer.
    A side section of a round tube, drawn as the duct of the worked example is."""
    fig, ax = canvas(6.5, xlim=(-1.25, 10.75), ylim=(-2.28, 2.42))
    r1, r2 = 1.40, 0.98                     # radii of the tube at the two stations
    x = np.linspace(0.0, 10.4, 500)
    s = np.clip((x - 3.2) / 3.0, 0.0, 1.0)
    r = r1 + (r2 - r1) * (0.5 - 0.5 * np.cos(math.pi * s))
    wall = 0.16
    hatched_wall(ax, x, r, r + wall)
    hatched_wall(ax, x, -r, -r - wall)
    L1 = 1.30
    L2 = L1 * (r1 / r2) ** 2                # the same volume in a round tube: r1^2 L1 = r2^2 L2
    xa, xb = 0.7, 6.9
    for x0, L, rr in ((xa, L1, r1), (xb, L2, r2)):
        ax.add_patch(Polygon([(x0, -rr), (x0 + L, -rr), (x0 + L, rr), (x0, rr)], closed=True, fc=HIGHLIGHT,
                             ec="none", zorder=1))
        for xf in (x0, x0 + L):
            ax.plot([xf, xf], [-rr, rr], color=INK, lw=LW_DETAIL, zorder=2)
    close_to(math.pi * r1 ** 2 * L1, math.pi * r2 ** 2 * L2, 1e-9, "the two slabs hold the same volume")
    for xq, L, rr, lab in ((xa, L1, r1, r"$V_1\,dt$"), (xb, L2, r2, r"$V_2\,dt$")):
        dimension(ax, (xq, rr + wall + 0.10), (xq + L, rr + wall + 0.10), None, offset=0.35)
        text(ax, (xq + 0.5 * L, rr + wall + 0.45), lab, direction=90, dist=7)
    # the area of each station, marked across the tube just downstream of the slab's face
    for xq, L, rr, k in ((xa, L1, r1, 1), (xb, L2, r2, 2)):
        xd = xq + L + 0.42
        dimension(ax, (xd, -rr), (xd, rr), None, ticks=False, extension=False)
        text(ax, (xd, 0.45 * rr), f"area $A_{k}$", direction=0, dist=6)
    text(ax, (xa + 0.5 * L1, -r1 - wall), r"mass $dm_1 = \rho_1 A_1 V_1\,dt$", direction=-90, dist=6)
    text(ax, (xb + 0.5 * L2, -r2 - wall), r"mass $dm_2 = \rho_2 A_2 V_2\,dt$", direction=-90, dist=6)
    flow_arrow(ax, (-1.15, 0.0), (-0.25, 0.0), label="flow", label_dir=-90, dist=8)
    save_figure(fig, "p15-continuity")


def fluid_element():
    """F3: the forces along x on a small fluid element on a streamline: the pressure on its two end faces."""
    fig, ax = canvas(6.5, xlim=(-3.6, 11.1), ylim=(-1.22, 4.55))
    W, H = 4.2, 2.6                        # dx and dy in the drawing
    dz = np.array([1.2, 0.85])             # the depth dz, drawn oblique
    x0, y0 = 1.6, 0.0
    F = np.array([(x0, y0), (x0 + W, y0), (x0 + W, y0 + H), (x0, y0 + H)])
    B = F + dz
    for a, b in ((B[0], B[1]), (B[0], B[3]), (F[0], B[0])):               # hidden edges
        ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=LW_THIN, ls=(0, (3, 2)), zorder=2)
    right = np.array([F[1], B[1], B[2], F[2]])
    opaque(ax.add_patch(Polygon(right, closed=True, fc=HIGHLIGHT, ec=INK, lw=LW_OUTLINE, zorder=3)))
    opaque(ax.add_patch(Polygon([F[3], F[2], B[2], B[3]], closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE,
                                zorder=3)))
    opaque(ax.add_patch(Polygon(F, closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=3)))
    dimension(ax, (F[0][0], F[0][1] - 0.2), (F[1][0], F[1][1] - 0.2), "$dx$", offset=-0.35, label_side=-1)
    dimension(ax, (F[1][0] - 0.40, F[1][1] + 0.12), (F[2][0] - 0.40, F[2][1] - 0.12), "$dy$", label_side=1,
              extension=False, ticks=False, zorder=4)
    dimension(ax, F[3] + np.array([0.0, 0.18]), B[3] + np.array([0.0, 0.18]), "$dz$", offset=0.3, label_side=1)
    callout(ax, (x0 + 0.35, H - 0.35), "fluid element,\n" + r"mass $\rho\,dx\,dy\,dz$", at=(-1.5, 4.15), ha="right")
    # the pressure forces, along x, pointing into the two end faces at the height of their centers
    yc = y0 + 0.5 * H + 0.5 * dz[1]
    xr = B[1][0]                                   # the visible right edge of the right face
    kind_arrow(ax, (x0 - 3.0, yc), (x0, yc), "force", None)
    text(ax, (x0 - 2.15, yc), "pressure force\n" + r"$p\;dy\,dz$", direction=90, dist=5)
    kind_arrow(ax, (xr + 3.6, yc), (xr, yc), "force", None)
    text(ax, (xr + 1.8, yc), "pressure force\n" + r"$(p + dp)\;dy\,dz$", direction=90, dist=5)
    # the streamline through the middle of the element (dashed where the element hides it), and
    # the velocity along it, downstream of the element
    ys_ = y0 + 0.36 * H
    xs_in = np.array([x0, x0 + W])
    ax.plot(xs_in, [ys_, ys_], color=INK, lw=1.0, ls=(0, (3, 2)), zorder=3.5)
    xl_ = np.linspace(-3.5, x0, 60)
    ln_l = ax.plot(xl_, np.full_like(xl_, ys_), color=INK, lw=1.0, zorder=2)[0]
    motion_heads(ax, xl_, np.full_like(xl_, ys_), (0.82,), line=ln_l)
    xr_ = np.linspace(xr, 11.0, 60)
    ln_r = ax.plot(xr_, np.full_like(xr_, ys_), color=INK, lw=1.0, zorder=2)[0]
    motion_heads(ax, xr_, np.full_like(xr_, ys_), (0.93,), line=ln_r)
    text(ax, (-2.55, ys_), "streamline, along $x$", direction=-90, dist=5)
    rides_on(kind_arrow(ax, (xr + 0.5, ys_), (xr + 2.6, ys_), "velocity", None), ln_r)
    text(ax, (xr + 1.05, ys_), "velocity $V$", direction=-90, dist=5, color=BLUE)
    assert xr > F[1][0] and B[1][1] < yc < B[2][1], "the right force meets the right face"
    assert y0 < ys_ < y0 + H, "the streamline passes through the element"
    save_figure(fig, "p15-fluid-element")


def duct_example():
    """F4: worked example 1 to scale: the duct, the speeds (arrows to one scale, on the axis) and the
    water column of the manometer (to the scale of the duct), tapped through the lower wall."""
    e = _ex1()
    D1, D2, V1 = EX1["D1"], EX1["D2"], EX1["V1"]
    fig, ax = canvas(6.5, xlim=(-0.13, 0.70), ylim=(-0.235, 0.165))
    x = np.linspace(0.0, 0.64, 400)
    s = np.clip((x - 0.18) / 0.18, 0.0, 1.0)
    r = 0.5 * D1 + (0.5 * D2 - 0.5 * D1) * (0.5 - 0.5 * np.cos(math.pi * s))
    wall = 0.008
    hatched_wall(ax, x, r, r + wall)
    hatched_wall(ax, x, -r, -r - wall)
    x1s, x2s = 0.07, 0.45
    r1, r2 = float(np.interp(x1s, x, r)), float(np.interp(x2s, x, r))
    close_to(2 * r1, D1, 1e-12, "D1 drawn")
    close_to(2 * r2, D2, 1e-12, "D2 drawn")
    flow_arrow(ax, (-0.12, 0.0), (-0.04, 0.0), label="air", label_dir=-90, dist=8)
    Sc = 0.0028                                     # m of drawing per m/s: both arrows to one scale
    for xs, rr, V, k, Dk in ((x1s, r1, V1, 1, D1), (x2s, r2, e["V2"], 2, D2)):
        ax.plot([xs, xs], [rr + 0.004, rr + wall + 0.030], color=GRAY, lw=LW_THIN, ls=(0, (4, 3)), zorder=2)
        ax.plot([xs, xs], [-rr, rr], color=GRAY, lw=LW_THIN, ls=(0, (4, 3)), zorder=2)
        kind_arrow(ax, (xs + 0.006, 0.0), (xs + 0.006 + Sc * V, 0.0), "velocity", None)
        Vtxt = f"{fmt(V, 2)} m/s (given)" if k == 1 else f"{fmt(V)} m/s"
        Dtxt = f"{Dk * 100:g}"
        text(ax, (xs, rr + wall + 0.030), f"$D_{k}$ = {Dtxt} cm\n$V_{k}$ = {Vtxt}", direction=90, dist=3)
    # the manometer under the duct, tapped at the two stations through a hole in the lower wall
    t = 0.005
    top1, top2 = -r1 - wall, -r2 - wall
    bot = -0.205
    lev1 = -0.170
    lev2 = lev1 + e["h"]
    ax.plot([x2s - t, x2s - t], [top2, top1], color=INK, lw=LW_DETAIL, zorder=4)
    ax.plot([x2s + t, x2s + t], [top2, top1], color=INK, lw=LW_DETAIL, zorder=4)
    for xs, rr in ((x1s, r1), (x2s, r2)):           # the pressure taps: the wall is open above each leg
        ax.add_patch(Polygon([(xs - t + 0.0006, -rr + 0.0004), (xs + t - 0.0006, -rr + 0.0004),
                              (xs + t - 0.0006, -rr - wall - 0.0004), (xs - t + 0.0006, -rr - wall - 0.0004)],
                             closed=True, fc="white", ec="none", zorder=3.6))
        ax.plot([xs - t, xs - t], [-rr, -rr - wall], color=INK, lw=LW_DETAIL, zorder=4)
        ax.plot([xs + t, xs + t], [-rr, -rr - wall], color=INK, lw=LW_DETAIL, zorder=4)
    draw_manometer(ax, x1s, x2s, top1, bot, lev1, lev2, t)
    xd = x2s + 0.045
    ax.plot([x1s + t, xd + 0.006], [lev1, lev1], color=GRAY, lw=0.8, ls=(0, (2, 2)), zorder=2)
    ax.plot([x2s + t, xd + 0.006], [lev2, lev2], color=GRAY, lw=0.8, ls=(0, (2, 2)), zorder=2)
    dimension_outside(ax, (xd, lev1), (xd, lev2), None)
    text(ax, (xd, 0.5 * (lev1 + lev2)),
         f"$h$ = {fmt_dec(e['h'] * 1000, 1)} mm\n$p_1 - p_2$ = {fmt(e['dp'])} Pa", direction=0, dist=10)
    text(ax, (0.5 * (x1s + x2s), bot - t), "water", direction=-90, dist=4)
    close_to(lev2 - lev1, e["h"], 1e-12, "the water column is drawn to the scale of the duct")
    close_to(e["V2"], V1 * (D1 / D2) ** 2, 1e-9, "the speed ratio is the area ratio")
    save_figure(fig, "p15-duct-example")


def pitot_static_tube():
    """F5: the pitot-static tube in section (total pressure at the nose hole, static pressure at the
    side holes), with the computed surface pressure along it, aligned below."""
    a = 0.25                                # half-body scale: far-downstream diameter 4a = 1 (one probe diameter)
    x, r, cp, psi = _half_body(a)
    xs = x - x[0]                           # distance from the nose, in diameters
    x_holes = 3.0                           # static holes, diameters behind the nose
    cp_holes = float(np.interp(x_holes, xs, cp))
    assert abs(cp_holes) < 0.02, cp_holes   # the surface pressure there is within 2% of q of the static pressure
    FW, FH, AH = 6.5, 4.2, 0.40
    fig = plt.figure(figsize=(FW, FH))
    ax = fig.add_axes([0.02, 0.98 - AH, 0.96, AH])
    bx = fig.add_axes([0.17, 0.13, 0.70, 0.36])
    ax.axis("off")
    x_l, x_max = -1.55, 4.6
    x_r = x_max + 1.55
    ax.set_xlim(x_l, x_r)
    half = 0.5 * (x_r - x_l) * (AH * FH) / (0.96 * FW)         # y half-range that makes the scale equal
    ax.set_ylim(-half, half)
    ax.set_aspect("equal")
    fig.canvas.draw()
    keep = xs <= x_max
    X, Rr = xs[keep], r[keep]
    # the outline drawn from about 300 points (the half-body is computed on 8,000)
    sel = np.unique(np.r_[np.searchsorted(np.cumsum(np.r_[0.0, np.hypot(np.diff(X), np.diff(Rr))]),
                                          np.linspace(0.0, float(np.sum(np.hypot(np.diff(X), np.diff(Rr)))), 300)),
                          len(X) - 1])
    sel = sel[sel < len(X)]
    X, Rr = X[sel], Rr[sel]
    wall_t = 0.08
    hole = 0.06                             # nose hole radius
    tube_t = 0.05                           # wall of the inner tube
    x_ch = 1.2                              # front of the static chamber
    for sign in (1, -1):
        rin = Rr - wall_t
        m = X >= x_ch
        inner = np.c_[X[m][::-1], sign * rin[m][::-1]]
        xh = float(np.interp(hole, Rr[:200], X[:200]))          # where the nose surface reaches the bore radius
        front = [(x_ch, sign * rin[m][0]), (x_ch, sign * hole), (xh, sign * hole)]
        poly = np.r_[np.c_[X[X >= xh], sign * Rr[X >= xh]], inner, front]
        pa = ax.add_patch(Polygon(poly, closed=True, fc="#FFFFFF", ec=INK, lw=LW_DETAIL, zorder=3))
        pa.set_hatch("////")
        opaque(pa)
        tube = np.array([(x_ch, sign * hole), (x_max, sign * hole), (x_max, sign * (hole + tube_t)),
                         (x_ch, sign * (hole + tube_t))])
        pt_ = ax.add_patch(Polygon(tube, closed=True, fc="#FFFFFF", ec=INK, lw=LW_DETAIL, zorder=3))
        pt_.set_hatch("////")
        opaque(pt_)
        rr = float(np.interp(x_holes, X, Rr))
        ax.add_patch(Polygon([(x_holes - 0.045, sign * (rr + 0.02)), (x_holes + 0.045, sign * (rr + 0.02)),
                              (x_holes + 0.045, sign * (rr - wall_t - 0.02)), (x_holes - 0.045, sign * (rr - wall_t - 0.02))],
                             closed=True, fc="white", ec="none", zorder=3.5))
    # streamlines of the ideal flow (thin black lines with small heads, as on the rest of the page);
    # the upper half only: the lower half is the mirror image, and the labels below need a clear path
    xx = np.linspace(x_l, x_max, 260)
    for lev in (0.05, 0.16):
        rr_ = _psi_line(psi, lev, xx + x[0], 3.0)
        ln = ax.plot(xx, rr_, color=INK, lw=1.0, zorder=1)[0]
        motion_heads(ax, xx, rr_, (0.08,), line=ln)
    xst = np.linspace(x_l, -0.07, 40)
    ln = ax.plot(xst, 0 * xst, color=INK, lw=1.0, zorder=1)[0]
    motion_heads(ax, xst, 0 * xst, (0.55,), line=ln)
    point(ax, (-0.035, 0.0), None, ms=3.0)          # the stagnation point, just ahead of the open bore
    callout(ax, (-0.035, -0.01), "stagnation point:\n$V$ = 0, pressure $p_0$", at=(-0.35, -0.70), ha="right")
    rr = float(np.interp(x_holes, X, Rr))
    callout(ax, (x_holes, -rr - 0.01), "static holes: pressure $p$", at=(x_holes - 0.35, -0.80), ha="right")
    text(ax, (x_l + 0.05, 0.86), r"free stream: $V_\infty$, $p$", ha="left", va="center")
    text(ax, (x_max + 0.06, -0.03), "$p_0$ to gauge", ha="left", va="top")
    text(ax, (x_max + 0.06, 0.5 * (hole + tube_t + rr - wall_t) + 0.04), "$p$ to gauge", ha="left", va="center")
    # lower panel: the computed surface pressure, same x scale and position as the drawing
    fig.canvas.draw()
    inv = fig.transFigure.inverted()
    xa0 = inv.transform(ax.transData.transform((0.0, 0.0)))[0]
    xa1 = inv.transform(ax.transData.transform((x_max, 0.0)))[0]
    pos = bx.get_position()
    bx.set_position([xa0, pos.y0, xa1 - xa0, pos.height])
    bx.plot(xs[keep], cp[keep], **line_kw(0))
    bx.axhline(0.0, **line_kw("reference"))
    for s_ in ("top", "right"):
        bx.spines[s_].set_visible(False)
    bx.set_xlim(0.0, x_max)
    bx.set_ylim(-0.5, 1.15)
    bx.set_xticks([0, 1, 2, 3, 4])
    bx.set_yticks([-0.5, 0.0, 0.5, 1.0])
    bx.set_xlabel("Distance from the nose, probe diameters")
    bx.set_ylabel(r"$(p_\mathrm{surface} - p)/q$," + "\n" + r"$q$ the dynamic pressure")
    point(bx, (0.0, 1.0), "nose: $p_\\mathrm{surface} = p_0$", direction=0, dist=4)
    point(bx, (x_holes, cp_holes), "static holes: $p_\\mathrm{surface} \\approx p$", direction=90, dist=8)
    fig.canvas.draw()
    for xv in (0.0, x_holes):                     # the two panels share one x scale
        pa_ = ax.transData.transform((xv, 0.0))[0]
        pb_ = bx.transData.transform((xv, 0.0))[0]
        assert abs(pa_ - pb_) < 0.5, (xv, pa_, pb_)
    close_to(float(cp[0]), 1.0, 1e-6, "the nose feels the whole dynamic pressure")
    pitot_static_tube.cp_holes = cp_holes
    save_figure(fig, "p15-pitot-static-tube")


def pitot_static_system():
    """F6: which pressure feeds which instrument."""
    fig, ax = new_axes(6.5, 3.6)
    set_frame(ax, -2.0, 13.0, 0.0, 7.2)
    W = 4.6
    asi = box(ax, (10.3, 6.0), "Airspeed indicator: $p_0 - p$", w=W)
    alt = box(ax, (10.3, 3.9), "Altimeter: $p$", w=W)
    vsi = box(ax, (10.3, 1.8), "Vertical speed indicator: rate of change of $p$", w=W)
    # the pitot tube: a tube open at the front (ram-air inlet), a drain hole underneath
    ty, th = 6.25, 0.22
    nose = 0.6
    tube = np.array([(nose, ty + th), (2.8, ty + th), (2.8, ty - th), (nose, ty - th)])
    ax.plot(tube[:, 0], tube[:, 1], color=INK, lw=LW_OUTLINE, zorder=3, solid_joinstyle="miter")
    ax.plot([nose, nose], [ty + th, ty + 0.09], color=INK, lw=LW_OUTLINE, zorder=3)
    ax.plot([nose, nose], [ty - th, ty - 0.09], color=INK, lw=LW_OUTLINE, zorder=3)
    ax.add_patch(Polygon([(2.30, ty - th - 0.02), (2.44, ty - th - 0.02), (2.44, ty - th + 0.02),
                          (2.30, ty - th + 0.02)], closed=True, fc="white", ec="none", zorder=3.5))
    callout(ax, (2.37, ty - th - 0.03), "drain hole", at=(1.2, 5.1), ha="right")
    text(ax, (1.7, ty + th), "pitot tube", direction=90, dist=5)
    flow_arrow(ax, (-0.55, ty), (0.48, ty), width=5.0, head_width=9.0, head_len=6.0)
    text(ax, (-0.55, ty), "ram air", direction=180, dist=4)
    # the static port: a flush hole in the fuselage skin
    sk = 1.6
    pa = ax.add_patch(Polygon([(0.3, sk), (3.2, sk), (3.2, sk + 0.22), (0.3, sk + 0.22)], closed=True, fc="#FFFFFF",
                              ec=INK, lw=LW_DETAIL, zorder=3))
    pa.set_hatch("////")
    opaque(pa)
    ax.add_patch(Polygon([(1.62, sk - 0.01), (1.78, sk - 0.01), (1.78, sk + 0.23), (1.62, sk + 0.23)], closed=True,
                         fc="white", ec="none", zorder=3.5))
    text(ax, (1.7, sk + 0.22), "static port, in the skin", direction=90, dist=5)
    # lines: the pitot line (black, solid) to the airspeed indicator only; the static line (blue, dashed) to all three
    xl = asi.cx - W / 2
    ax.plot([2.8, xl], [ty, ty], color=INK, lw=2.4, zorder=2, solid_capstyle="butt")
    trunk = 6.2
    yA = asi.cy - 0.35
    st = dict(color=BLUE, lw=2.4, ls=(0, (4, 2)), zorder=2)
    ax.plot([1.7, 1.7, trunk, trunk], [sk - 0.01, 0.55, 0.55, yA], **st)
    for b, y in ((asi, yA), (alt, alt.cy), (vsi, vsi.cy)):
        ax.plot([trunk, b.cx - W / 2], [y, y], **st)
    text(ax, (4.4, ty), "pitot line, $p_0$", direction=90, dist=4)
    text(ax, (4.0, 0.55), "static line, $p$", direction=90, dist=4, color=BLUE)
    assert yA < ty - 0.2, "the static trunk stops below the pitot line"
    save_figure(fig, "p15-pitot-static-system")


def blockage_pressures():
    """F7: the pitot-cover example and the other cases of the text, side by side at one scale: the
    pressure in the pitot line and in the static line from the runway to 300 m, the airplane at a
    true airspeed of 65 m/s. The airspeed indicator reads the gap between the two lines."""
    e = _ex4()
    hs = e["hs"]
    order = [("open", "Both lines open"), ("cover", "Inlet and drain blocked (the cover)"),
             ("inlet", "Inlet blocked, drain open"), ("static", "Static port blocked")]
    fig, axs = data_axes(6.5, 5.3, ncols=2, nrows=2, sharex=True, sharey=True)
    fig.subplots_adjust(left=0.105, right=0.995, wspace=0.08, hspace=0.12, bottom=0.095, top=0.99)
    k = 1.0 / 1000.0
    xa, xt = 330.0, 352.0                       # the gap arrow, and where the names on its right start
    for ax, (key, name) in zip(axs.flat, order):
        c = e["cases"][key]
        yp = [c["pitot"][h] * k for h in hs]
        ys = [c["static"][h] * k for h in hs]
        ax.plot(hs, yp, **line_kw(0), marker="o", ms=5.5, zorder=4)
        ax.plot(hs, ys, **line_kw(1), marker="s", ms=5.5, mfc="white", zorder=5)
        ax.set_xlim(-30.0, 545.0)
        ax.set_ylim(96.6, 106.4)
        ax.set_xticks([0, 150, 300])
        ax.set_yticks([98, 100, 102, 104, 106])
        fig.canvas.draw()
        g0, g1 = c["static"][hs[-1]] * k, c["pitot"][hs[-1]] * k
        if g1 - g0 > 0.05:
            ax.annotate("", xy=(xa, g1), xytext=(xa, g0),
                        arrowprops=dict(arrowstyle="<|-|>,head_length=0.45,head_width=0.18", color=INK, lw=LW_THIN,
                                        shrinkA=0, shrinkB=0))
            ax.plot([312.0, xa + 12.0], [g1, g1], color=GRAY, lw=0.7, zorder=2)
            ax.plot([312.0, xa + 12.0], [g0, g0], color=GRAY, lw=0.7, zorder=2)
            text(ax, (xt, 0.5 * (g0 + g1)), f"{fmt(c['dp'][hs[-1]] * k, 3)} kPa", ha="left", va="center",
                 fs=FS_SMALL)
            note = f"at 300 m:\nreads {fmt(c['dial'][hs[-1]], 3)} m/s"
        elif abs(g1 - g0) <= 0.05:
            note = "at 300 m: no gap,\nreads 0 m/s"
        else:
            note = "at 300 m: gap below\nzero, reads 0 m/s"
        text(ax, (-18.0, 97.0), note, ha="left", va="bottom", fs=FS_SMALL, backing=False)
        text(ax, (257.5, 106.25), name, fs=FS_SMALL, va="top", backing=False)
    for ax in axs[:, 0]:
        ax.set_ylabel("Pressure, kPa")
    for ax in axs[1, :]:
        ax.set_xlabel("Altitude, m")
    # the two lines named: at their ends in the first panel, where they hold a trapped pressure in the others
    a_open, a_cover, a_inlet, a_static = axs.flat
    c = e["cases"]["open"]
    text(a_open, (xt, c["pitot"][hs[-1]] * k + 0.55), "pitot line", ha="left", va="center", fs=FS_SMALL,
         color=text_color(0))
    text(a_open, (xt, c["static"][hs[-1]] * k - 0.55), "static line", ha="left", va="center", fs=FS_SMALL,
         color=text_color(1))
    text(a_cover, (150.0, e["trapped"] * k + 0.3), "pitot line, held at\nthe runway pressure", fs=FS_SMALL,
         va="bottom", color=text_color(0))
    text(a_inlet, (100.0, 103.6), "both lines at $p$", fs=FS_SMALL, color=text_color(0))
    text(a_static, (-15.0, e["trapped"] * k - 0.35), "static line held at\nrunway pressure", fs=FS_SMALL,
         ha="left", va="top", color=text_color(1))
    gaps = [e["cases"][kk]["dp"][hs[-1]] for kk in ("cover", "open", "inlet", "static")]
    assert gaps[0] > gaps[1] > gaps[2] == 0.0 > gaps[3], gaps
    save_figure(fig, "p15-blockage-pressures")


def make_all():
    pressure_and_shear()
    stream_tube()
    continuity_slabs()
    fluid_element()
    duct_example()
    pitot_static_tube()
    pitot_static_system()
    blockage_pressures()


def values():
    r = lambda k, v: record(PAGE, k, v)
    # Example 1
    e = _ex1()
    r("ex1-A1", fmt(e["A1"], 5))
    r("ex1-A2", fmt(e["A2"], 5))
    r("ex1-V2", fmt(e["V2"], 5))                    # five figures: the next step squares and subtracts
    r("ex1-V2-4", fmt(e["V2"]))
    r("ex1-ratio", fmt(e["ratio"], 4))
    r("ex1-Q", fmt(e["Q"]))
    r("ex1-mdot", fmt(e["mdot"]))
    r("ex1-dp", fmt(e["dp"]))
    r("ex1-dV2", fmt_dec(float(fmt(e["V2"], 5)) ** 2 - EX1["V1"] ** 2, 2))
    r("ex1-h", fmt(e["h"]))
    r("ex1-h-mm", fmt_dec(e["h"] * 1000, 1))
    # Example 2
    e2 = _ex2()
    r("ex2-T", fmt_dec(e2["T"], 2))
    r("ex2-expo", fmt(e2["expo"], 5))
    r("ex2-rho", fmt(e2["rho"]))
    r("ex2-V", fmt(e2["V"]))
    r("ex2-Vdial", fmt(e2["V_dial"]))
    # Example 3
    e3 = _ex3()
    r("ex3-dp", fmt(e3["dp"]))
    r("ex3-V", fmt(e3["V"]))
    # Example 4: the pitot cover left on (printed with one decimal where two pressures are subtracted)
    e4 = _ex4()
    ha, hb = EX4["ha"], EX4["hb"]
    r("ex4-trapped", fmt(e4["trapped"]))
    for h in (ha, hb):
        T_ = float(standard(h)[0])
        r(f"ex4-T-{h:.0f}", fmt_dec(T_, 3))
        r(f"ex4-p-{h:.0f}", fmt_dec(e4["p"][h], 1))
        gap = e4["trapped"] - float(fmt_dec(e4["p"][h], 1).replace(",", ""))
        r(f"ex4-gap-{h:.0f}", fmt_dec(gap, 1))
        r(f"ex4-read-{h:.0f}", fmt(math.sqrt(2.0 * float(fmt_dec(gap, 1).replace(",", "")) / RHO_SL), 3))
        close_to(gap, e4["cases"]["cover"]["dp"][h], 0.06, "printed gap")
    q0 = float(dynamic_pressure(RHO_SL, e4["V"]))
    r("ex4-q-runway", fmt_dec(q0, 1))
    r("ex4-rho-300", fmt(e4["rho"][hb], 5))
    qb = 0.5 * float(fmt(e4["rho"][hb], 5)) * e4["V"] ** 2
    r("ex4-q-300", fmt_dec(qb, 1))
    r("ex4-open-300", fmt(math.sqrt(2.0 * float(fmt_dec(qb, 1).replace(",", "")) / RHO_SL), 3))
    r("ex4-h-true", fmt(e4["h_true"], 2))
    r("ex4-h-close", fmt(e4["h_close"], 2))
    for k in ("open", "cover"):
        r(f"ex4-{k}-dpk", fmt(e4["cases"][k]["dp"][hb] / 1000, 3))
    # a sealed volume at the runway pressure: its pressure drifts by p/T for each kelvin (about 350 Pa)
    drift = e4["trapped"] / T_SL
    assert 345.0 < drift < 355.0, drift
    r("ex4-drift-per-K", f"{int(round(drift, -1))}")
    # Draining tank
    r("tank-V", fmt(draining_speed(TANK_Z)))
    # numbers in the running text
    a_sl = speed_of_sound(T_SL)
    r("a-sl", fmt(a_sl))
    r("a-sl-03", fmt(0.3 * a_sl))
    r("rho-g-1m", fmt(RHO_SL * G * 1.0))
    r("q-50", fmt(float(dynamic_pressure(RHO_SL, 50.0))))
    r("water-1cm", fmt(manometer_dp(0.01)))
    r("ex1-frac-atm", fmt(e["dp"] / P_SL * 100, 2))
    r("ex2-low-pct", fmt((e2["V"] - e2["V_dial"]) / e2["V"] * 100, 2))
    r("ex3-V-water", fmt(pitot_speed(e3["dp"], 0.0, RHO_WATER)))
    out = getattr(stream_tube, "out", None) or stream_tube()
    vr = out[2]["V"] / out[1]["V"]
    wr = out[1]["w"] / out[2]["w"]
    assert fmt(vr, 3) == fmt(wr, 3), (vr, wr)
    r("tube-ratio", fmt(vr, 3))
    x, rr, cp, psi = _half_body(0.25)
    xs = x - x[0]
    r("probe-cp-min", fmt(-cp.min(), 2))
    r("probe-cp-holes-pct", fmt(abs(np.interp(3.0, xs, cp)) * 100, 2))
