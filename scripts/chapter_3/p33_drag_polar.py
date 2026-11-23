"""Figures and values of 3.3 Drag Polar (notes/chapter-3/drag-polar.md).

Every number printed on the page is computed in values() and recorded with record("p33", ...).
The figures are drawn from the same numbers.

The running example is an invented twin-jet wide-body airliner (EX below). Its clean values are
invented; the configuration figure adds the flap and landing-gear increments and the span
efficiency with flaps down that Scholz (n.d., Section 5.4, after Loftin 1980) gives for
passenger jets, and the clean span efficiency that Loftin chooses for jet aircraft in cruise
(Scholz n.d., Section 5.7); both are in chapter_3/published.py. The section data are NACA Report 824 (the shared
airfoil_data module).

Helpers written here (not in the shared code): _wake(), a schematic wake band behind a body for
the pressure-drag panel; _fuselage_front(), a circle-and-wing front view for the interference panel.
"""
from chapter_3.common import *
from chapter_3.airfoil_data import pchip as _pchip
from matplotlib.patches import Circle, Polygon as _Poly

PAGE = "p33"

# ===================================================================== worked-example data (choices, not constants)
# An invented twin-jet wide-body airliner in steady level flight at 7,500 m (standard atmosphere of page 1.4).
EX = dict(W=1.5e6, S=300.0, b=54.0, e=LOFTIN_E_CRUISE_JET, CD0=0.017, h=7500.0)   # N, m^2, m, -, -, m (e: Loftin, via Scholz)
EX_SPEEDS = (130.0, 200.0)                                               # m/s, the two other speeds of example 2
TABLE_CL = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2)                           # the polar table of example 1
TANGENT_CL = (0.3, 1.35)                                                  # the two non-optimal lines of the tangent figure
# Where the clean polar of the example holds in the drag-speed figure (invented values of the example):
# below the speed where level flight needs more than the clean wing's C_L,max, and above the Mach
# number where wave drag, which the polar leaves out, starts to add to the drag.
EX_CLMAX_CLEAN = 1.5
EX_M_LIMIT = 0.75

# Worked example 3, the reverse use of the polar (invented values).
# (a) an invented single-aisle airliner, two drags measured in level flight at 4,500 m;
# (b) an invented fighter, clean and subsonic, K from a stated (L/D)max and C_D,0.
EX3 = dict(W=650000.0, S=122.0, h=4500.0, V=(115.0, 175.0), D=(41600.0, 40400.0))   # N, m^2, m, m/s, N
EX3B = dict(CD0=0.020, LDmax=11.0)

# Configurations: the flap and gear increments and span efficiency of SCHOLZ_FLAPS_GEAR
# (chapter_3/published.py; Scholz n.d., Section 5.4, Eq. 5.21, after Loftin 1980: passenger jets).
FLAPS_GEAR = SCHOLZ_FLAPS_GEAR

# The section of the polar-from-data figure: NACA 64(3)-618 at R = 6 million (Report 824, page 195)
SECTION, SECTION_RE = "64-618", 6.0e6
LINK_ALPHA = (-4.0, 2.0, 8.0)          # deg, the three points A, B, C carried through the panels
LINK_RANGE = (-6.0, 11.0)              # deg, the part of the lift curve drawn
SYMCAM_RE = 9.0e6                      # the symmetric-cambered comparison (both curves smooth at 9 million)


# ===================================================================== computations
def example():
    """Every number of the running example."""
    W, S, b, e, CD0, h = (EX[k] for k in ("W", "S", "b", "e", "CD0", "h"))
    AR = b ** 2 / S
    K = polar_K(AR, e)
    m = min_drag_point(CD0, K)
    T, p, rho = (float(v) for v in standard(h))
    a_s = float(speed_of_sound(T))
    WS = W / S
    Vmd = min_drag_speed(W, rho, S, CD0, K)
    Dmin = W / m["LD_max"]
    table = []
    for cl in TABLE_CL:
        cd = float(polar_CD(cl, CD0, K))
        table.append(dict(CL=cl, CDi=K * cl ** 2, CD=cd, LD=(cl / cd if cl > 0 else 0.0)))
    speeds = []
    for V in EX_SPEEDS:
        q = float(dynamic_pressure(rho, V))
        Dp, Di, D = (float(x) for x in drag_parts(W, rho, V, S, CD0, K))
        speeds.append(dict(V=V, q=q, Dp=Dp, Di=Di, D=D, CL=W / (q * S), M=V / a_s, LD=W / D))
    q_md = float(dynamic_pressure(rho, Vmd))
    Dp_md, Di_md, D_md = (float(x) for x in drag_parts(W, rho, Vmd, S, CD0, K))
    V_lo = math.sqrt(2.0 * W / (rho * S * EX_CLMAX_CLEAN))     # level flight at the clean C_L,max
    V_hi = EX_M_LIMIT * a_s
    return dict(W=W, S=S, b=b, e=e, CD0=CD0, h=h, AR=AR, K=K, CLs=m["CL_star"], CDs=m["CD_star"],
                LDmax=m["LD_max"], T=T, rho=rho, a=a_s, WS=WS, Vmd=Vmd, Dmin=Dmin, q_md=q_md,
                Dp_md=Dp_md, Di_md=Di_md, D_md=D_md, M_md=Vmd / a_s, table=table, speeds=speeds,
                V_lo=V_lo, V_hi=V_hi)


def polar_from_two_points(CL1, CD1, CL2, CD2):
    """C_D,0 and K of the parabolic polar through two points (C_L, C_D):
    K = (C_D1 - C_D2)/(C_L1^2 - C_L2^2), C_D,0 = C_D1 - K C_L1^2.
    Example: polar_from_two_points(1.0, 0.06, 0.5, 0.03) -> (0.02, 0.04)"""
    K = (CD1 - CD2) / (CL1 ** 2 - CL2 ** 2)
    return CD1 - K * CL1 ** 2, K


def K_from_LDmax(CD0, LDmax):
    """K from (L/D)max = 1/(2 sqrt(K C_D,0)): K = 1/(4 C_D,0 (L/D)max^2). Example: K_from_LDmax(0.02, 15.0) -> 0.05556"""
    return 1.0 / (4.0 * CD0 * LDmax ** 2)


def example3():
    """Worked example 3: (a) C_D,0 and K from two drags measured in level flight; (b) K from (L/D)max."""
    W, S, h = EX3["W"], EX3["S"], EX3["h"]
    rho = float(standard(h)[2])
    pts = []
    for V, D in zip(EX3["V"], EX3["D"]):
        q = float(dynamic_pressure(rho, V))
        pts.append(dict(V=V, D=D, q=q, qS=q * S, CL=W / (q * S), CD=D / (q * S)))
    CD0, K = polar_from_two_points(pts[0]["CL"], pts[0]["CD"], pts[1]["CL"], pts[1]["CD"])
    for p in pts:                          # both measured drags lie on the polar found
        close_to(float(drag_parts(W, rho, p["V"], S, CD0, K)[2]), p["D"], 1e-6 * p["D"], "measured drag on the polar")
    Kb = K_from_LDmax(EX3B["CD0"], EX3B["LDmax"])
    close_to(min_drag_point(EX3B["CD0"], Kb)["LD_max"], EX3B["LDmax"], 1e-12, "K from (L/D)max round trip")
    return dict(W=W, S=S, h=h, rho=rho, pts=pts, CD0=CD0, K=K, LDmax=min_drag_point(CD0, K)["LD_max"],
                Kb=Kb)


def configurations():
    """Clean, takeoff and landing polars of the example airliner: (name, CD0, e, K, CL_op)."""
    E = example()
    m = min_drag_point(E["CD0"], E["K"])
    out = [dict(name="clean", CD0=E["CD0"], e=E["e"], K=E["K"], CL_op=None, LDmax=m["LD_max"], CLs=m["CL_star"])]
    for name, c in FLAPS_GEAR.items():
        CD0 = E["CD0"] + c["dCD_flap"] + c["dCD_gear"]
        K = polar_K(E["AR"], c["e"])
        m = min_drag_point(CD0, K)
        out.append(dict(name=name, CD0=CD0, e=c["e"], K=K, CL_op=c["CL_op"], flap_deg=c["flap_deg"],
                        CD_op=float(polar_CD(c["CL_op"], CD0, K)),
                        LD_op=c["CL_op"] / float(polar_CD(c["CL_op"], CD0, K)),
                        LDmax=m["LD_max"], CLs=m["CL_star"]))
    return out


def section_link():
    """Dense lift and drag of the section against alpha, and the points A, B, C."""
    a, cl = series(SECTION, "cl_alpha", SECTION_RE)
    alpha = np.linspace(*LINK_RANGE, 241)
    CL = _pchip(a, cl, alpha)
    CD = curve(SECTION, "cd_cl", SECTION_RE, x=CL)[1]
    pts = []
    for al in LINK_ALPHA:
        c_l = float(_pchip(a, cl, al))
        pts.append(dict(alpha=al, cl=c_l, cd=float(read(SECTION, "cd_cl", SECTION_RE, c_l))))
    return alpha, CL, CD, pts


def bucket(k, Re=6.0e6, frac=1.10):
    """The low-drag range of a section: the c_l range where c_d stays within `frac` of its minimum,
    from the drawn curve, and the minimum itself."""
    x, y = curve(k, "cd_cl", Re, n=2001)
    i = int(np.argmin(y))
    ok = y <= frac * y[i]
    # the connected run around the minimum
    lo = i
    while lo > 0 and ok[lo - 1]:
        lo -= 1
    hi = i
    while hi < len(x) - 1 and ok[hi + 1]:
        hi += 1
    return dict(cd_min=float(y[i]), cl_at_min=float(x[i]), lo=float(x[lo]), hi=float(x[hi]),
                mid=0.5 * float(x[lo] + x[hi]))


# ===================================================================== drawing helpers of this page
def _wake(ax, x0, y_top, y_bot, x1, spread, hatch="////", label=None):
    """A wake band behind a body: from the separation points (x0, y_top) and (x0, y_bot), widening
    by `spread` on each side by x1; light gray with a hatch (reads in grayscale), dashed edges."""
    xs = np.linspace(x0, x1, 40)
    s = spread * ((xs - x0) / (x1 - x0)) ** 0.6
    top, bot = y_top + s, y_bot - s
    poly = np.r_[np.c_[xs, top], np.c_[xs[::-1], bot[::-1]]]
    pa = ax.add_patch(_Poly(poly, closed=True, fc="#EFEFEF", ec="none", hatch=hatch, zorder=1))
    pa.set_edgecolor(GRAY)
    pa.set_linewidth(0.0)
    ax.plot(xs, top, **line_kw("boundary"), zorder=2)
    ax.plot(xs, bot, **line_kw("boundary"), zorder=2)
    return pa, (xs, top, bot)


# ===================================================================== figures
def fig_parasite_kinds():
    """Three kinds of parasite drag in three panels: skin friction (shear along a plate), pressure
    drag (a round strut and a streamlined strut of the same thickness, with their wakes), and
    interference (a low wing meeting a fuselage, seen from ahead, bare corner on one side and a
    fairing on the other)."""
    fig, ax = canvas(6.5, xlim=(-0.25, 6.5), ylim=(0.0, 2.55))
    fs = FS_SMALL
    # ---------------- panel 1: skin friction
    text(ax, (1.0, 2.40), "1  skin friction", fs=FS_LABEL, backing=False)
    y0, delta = 0.80, 0.62
    flat_plate(ax, 0.15, 1.95, 0.10, y0=y0)
    prof = velocity_profile(ax, 0.45, delta, "turbulent", u_len=0.55, y0=y0, n_arrows=3, no_slip=False)
    tail = prof["free_stream_tail"]
    text(ax, (tail[0] + 0.24, tail[1]), r"$V_\infty$", direction=90, dist=4, color=BLUE, fs=FS_LABEL)
    callout(ax, (0.45 + 0.55 * 0.95, y0 + 0.50), "velocity\nprofile", at=(1.30, y0 + 0.92), ha="left", fs=fs)
    # the layer itself: from the wall up to where the speed reaches the free stream
    xb = 0.27
    dimension(ax, (xb, y0), (xb, y0 + delta), None)
    text(ax, (xb, y0 + 0.5 * delta), "boundary\nlayer", direction=180, dist=7, fs=fs)
    close_to(float(prof["curve"][1].max() - y0), delta, 1e-9, "bracket spans the profile")
    for x in (1.20, 1.50, 1.80):              # wall shear stress: the force of the air on the wall
        kind_arrow(ax, (x - 0.22, y0 + 0.055), (x, y0 + 0.055), "force", lw=1.4, head="small")
    text(ax, (1.05, y0 - 0.10), "shear stress pulls\nthe wall downstream", direction=-90, dist=4, fs=fs)
    # ---------------- panel 2: pressure drag, same thickness, round against streamlined
    xc = 2.95
    text(ax, (3.30, 2.40), "2  pressure drag", fs=FS_LABEL, backing=False)
    t = 0.40                                  # thickness of both struts, drawn units
    r = 0.5 * t
    yc1, yc2 = 1.70, 0.68
    sep = math.radians(82.0)                  # schematic separation near the top and bottom of the round strut
    _wake(ax, xc - r * math.cos(sep), yc1 + r * math.sin(sep), yc1 - r * math.sin(sep), 4.25, 0.16)
    ax.add_patch(opaque(Circle((xc, yc1), r, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=4)))
    text(ax, (3.70, yc1 + 0.50), "wide wake", fs=fs)
    chord = t / 0.33                          # NACA 0033: a symmetric section of 3:1 fineness
    sec = naca4("0033", n=121, chord=chord)["outline"]
    sx, sy = sec[:, 0] + (xc - r), sec[:, 1] + yc2
    th = float(sy.max() - sy.min())
    close_to(th, t, 0.01 * t, "streamlined strut has the thickness of the round strut")
    close_to(chord / th, 3.0, 0.05, "3:1 fineness")
    _wake(ax, xc - r + chord, yc2 + 0.012, yc2 - 0.012, 4.25, 0.05)
    ax.add_patch(opaque(_Poly(np.c_[sx, sy], closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=4)))
    text(ax, (3.98, yc2 + 0.26), "thin wake", fs=fs)
    xd = xc - r - 0.13
    dimension(ax, (xd, yc1 - r), (xd, yc1 + r), None)
    dimension(ax, (xd, yc2 - r), (xd, yc2 + r), None)
    text(ax, (xd + 0.25, 0.5 * (yc1 + yc2)), "same thickness", fs=fs)
    kind_arrow(ax, (2.30, 2.10), (2.75, 2.10), "velocity", None, lw=1.2, head="small")
    text(ax, (2.30, 2.10), r"$V_\infty$", direction=180, dist=3, color=BLUE, fs=FS_LABEL)
    # ---------------- panel 3: interference at the wing-body junction, seen from ahead
    text(ax, (5.55, 2.40), "3  interference", fs=FS_LABEL, backing=False)
    fc_ = (5.62, 1.30)
    R = 0.40
    wing_t = 0.07
    yw = fc_[1] - 0.62 * R                    # a low wing: its upper surface below the fuselage center
    xl, xr = 4.55, 6.50
    wpoly = np.array([(xl, yw - wing_t), (xr, yw - wing_t), (xr, yw), (xl, yw)])
    ax.add_patch(opaque(_Poly(wpoly, closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=3)))
    ax.add_patch(opaque(Circle(fc_, R, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=4)))
    dx = math.sqrt(R ** 2 - (yw - fc_[1]) ** 2)
    jl, jr = (fc_[0] - dx, yw), (fc_[0] + dx, yw)
    # fairing on the right junction: a concave fillet joining the fuselage side to the wing's upper surface
    th0 = math.atan2(yw - fc_[1], dx)
    a0 = th0 + math.radians(48.0)
    p_f = (fc_[0] + R * math.cos(a0), fc_[1] + R * math.sin(a0))
    q_f = (jr[0] + 0.26, yw)
    tt = np.linspace(0.0, 1.0, 50)
    ctrl = np.array([p_f, (jr[0] + 0.03, yw + 0.03), q_f])
    fil = ((1 - tt) ** 2)[:, None] * ctrl[0] + (2 * (1 - tt) * tt)[:, None] * ctrl[1] + (tt ** 2)[:, None] * ctrl[2]
    arc_t = np.linspace(a0, th0, 30)
    arc = np.c_[fc_[0] + R * np.cos(arc_t), fc_[1] + R * np.sin(arc_t)]
    fpoly = np.r_[fil, [jr], arc[::-1]]
    fp = ax.add_patch(opaque(_Poly(fpoly, closed=True, fc=HIGHLIGHT, ec="none", zorder=5)))
    ax.plot(fil[:, 0], fil[:, 1], color=INK, lw=LW_OUTLINE, zorder=6, solid_capstyle="round")
    ax.plot([jl[0]], [jl[1]], "o", ms=5, mfc="white", mec=INK, mew=1.2, zorder=7)
    callout(ax, (jl[0] - 0.03, jl[1] + 0.04), "bare\ncorner", at=(4.58, yw + 0.36), ha="left", fs=fs)
    callout(ax, (q_f[0] - 0.10, yw + 0.03), "fairing", at=(6.08, yw + 0.50), ha="left", fs=fs)
    text(ax, fc_, "fuselage", fs=fs, backing=False)
    text(ax, (6.20, yw - wing_t), "wing", direction=-90, dist=5, fs=fs)
    text(ax, (5.55, 0.42), "seen from ahead", fs=fs)
    trim_canvas(fig)
    save_figure(fig, "p33-parasite-drag-kinds")


def fig_polar_from_data():
    """Three linked panels: c_l and c_d against alpha (measured), then c_l against c_d."""
    alpha, CL, CD, pts = section_link()
    fig, axs, P = linked_polar(alpha, CL, CD, list(LINK_ALPHA), width=6.5, height=3.3, flip=True,
                               labels=("Section lift\ncoefficient, $c_l$", "Section drag\ncoefficient, $c_d$"),
                               label_dir=[[-20, 160, 160], [45, 90, 160], [0, 0, 110]])
    titles = ("1  lift, measured", "2  drag at each angle", "3  drag polar")
    for ax, t in zip(axs, titles):
        ax.set_title(t, fontsize=FS_SMALL, loc="left")
    for ax in axs[:2]:
        ax.set_xticks([-4, 0, 4, 8])
        ax.set_xlabel("Angle of attack,\n$\\alpha$, deg")
    axs[2].set_xlim(0.004, 0.018)
    axs[2].set_xticks([0.005, 0.015])
    axs[1].set_ylim(0.004, 0.018)
    axs[1].set_yticks([0.005, 0.010, 0.015])
    for ax in (axs[0], axs[2]):
        ax.set_ylim(-0.4, 1.6); ax.set_yticks([0.0, 0.5, 1.0, 1.5])
    fig.subplots_adjust(top=0.90, bottom=0.25, left=0.12, right=0.97, wspace=0.95)
    for p, q in zip(P, pts):
        close_to(p["CL"], q["cl"], 2e-3, "panel 1 and 3 share c_l")
        close_to(p["CD"], q["cd"], 2e-5, "panel 2 and 3 share c_d")
    save_figure(fig, "p33-polar-from-data")


def _example_polar_axes(height=3.6):
    fig, ax = data_axes(6.5, height)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.15, top=0.97)
    return fig, ax


BAND_FILL = "#E6E6E6"     # the zero-lift drag band (black text on it: 16:1)


def fig_polar_anatomy():
    """The example polar with its two parts: the zero-lift drag coefficient C_D,0 (a band) and the
    induced drag coefficient K C_L^2 (between the band and the curve); the points of worked
    example 1 marked."""
    E = example()
    CD0, K = E["CD0"], E["K"]
    fig, ax = _example_polar_axes(3.6)
    CL = np.linspace(-0.6, 1.4, 400)
    CD = polar_CD(CL, CD0, K)
    ax.fill_betweenx(CL, 0.0, CD0, color=BAND_FILL, lw=0, zorder=1)
    ax.fill_betweenx(CL, CD0, CD, color=HIGHLIGHT, lw=0, zorder=1)
    ax.plot(CD, CL, **line_kw(0), zorder=4)
    ax.axvline(CD0, **line_kw("boundary"), zorder=3)
    for row in E["table"]:
        ax.plot([row["CD"]], [row["CL"]], "o", ms=6, mfc="white", mec=INK, mew=1.3, zorder=6)
        close_to(float(polar_CD(row["CL"], CD0, K)), row["CD"], 1e-12, "table point on the polar")
    ax.set_xlim(0.0, 0.09); ax.set_ylim(-0.6, 1.4)
    ax.set_xticks([0.0, 0.02, 0.04, 0.06, 0.08]); ax.set_yticks([-0.4, 0.0, 0.4, 0.8, 1.2])
    ax.set_xlabel("Drag coefficient, $C_D$"); ax.set_ylabel("Lift coefficient, $C_L$")
    text(ax, (0.5 * CD0, 0.78), "zero-lift\ndrag,\n$C_{D,0}$ = " + fmt_dec(CD0, 3), fs=FS_SMALL, backing=BAND_FILL)
    text(ax, (0.033, 1.18), "induced drag,\n$K\\,C_L^2$", fs=FS_SMALL, backing=HIGHLIGHT)
    text(ax, (float(polar_CD(-0.42, CD0, K)), -0.42), "drag polar", direction=20, dist=10, fs=FS_SMALL)
    text(ax, (float(E["table"][-1]["CD"]), 1.2), "worked example 1:\n$C_L$ = 0 to 1.2", direction=-25, dist=10,
         fs=FS_SMALL)
    i = int(np.argmin(CD))
    close_to(float(CL[i]), 0.0, 0.006, "vertex of the polar at C_L = 0")
    save_figure(fig, "p33-polar-anatomy")


def fig_symmetric_cambered():
    """Measured section drag polars, drawn as the other polars of the page (c_l up, c_d across):
    the symmetric 64(3)-018 has its low-drag range centered on c_l = 0, the cambered 64(3)-618 at
    a positive c_l. R = 9 million, where both sets of test points lie on smooth curves."""
    fig, ax = data_axes(6.5, 3.9)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.14, top=0.97)
    rows = []
    for k, s in (("64-018", 3), ("64-618", 0)):
        x, y = curve(k, "cd_cl", SYMCAM_RE, n=500)
        ax.plot(y, x, **line_kw(s), zorder=4)
        b = bucket(k, SYMCAM_RE)
        rows.append((k, s, b, x, y))
    ax.set_ylim(-1.75, 1.8); ax.set_xlim(0.0, 0.020)
    ax.set_xticks([0.0, 0.005, 0.010, 0.015, 0.020]); ax.set_yticks([-1.2, -0.6, 0.0, 0.6, 1.2, 1.8])
    ax.set_xlabel("Section drag coefficient, $c_d$"); ax.set_ylabel("Section lift\ncoefficient, $c_l$")
    (k18, s18, b18, x18, y18), (k618, s618, b618, x618, y618) = rows
    text(ax, (float(y18[0]), float(x18[0])), AIRFOILS[k18]["name"], direction=-90, dist=5, fs=FS_SMALL,
         color=text_color(s18))
    text(ax, (float(y618[-1]), float(x618[-1])), AIRFOILS[k618]["name"], direction=90, dist=6, fs=FS_SMALL,
         color=text_color(s618))
    for (k, s, b), xb in (((k18, s18, b18), 0.0032), ((k618, s618, b618), 0.0015)):
        ax.plot([xb, xb], [b["lo"], b["hi"]], color=text_color(s), lw=2.4, solid_capstyle="butt", zorder=3)
        for ye in (b["lo"], b["hi"]):
            ax.plot([xb - 0.0003, xb + 0.0003], [ye, ye], color=text_color(s), lw=1.2, zorder=3)
    text(ax, (0.0032, b18["lo"]), "low-drag range,\nsymmetric", direction=-90, dist=6, fs=FS_SMALL,
         color=text_color(s18))
    text(ax, (0.0015, b618["hi"]), "low-drag range,\ncambered", direction=90, dist=6, fs=FS_SMALL,
         color=text_color(s618), ha="left", offset=(-8, 0))
    assert b618["mid"] - b18["mid"] > 0.3, "camber moves the low-drag range to positive lift"
    assert abs(b18["mid"]) < 0.1, "the symmetric section's low-drag range is centered on zero lift"
    save_figure(fig, "p33-symmetric-cambered-polar")


def fig_polar_tangent():
    """L/D is the slope of a line from the origin to a point of the polar; the tangent line has the
    largest slope and touches at C_L*, where the induced part equals C_D,0."""
    E = example()
    CD0, K, CLs, LDm = E["CD0"], E["K"], E["CLs"], E["LDmax"]
    fig, ax = _example_polar_axes(3.8)
    CL = np.linspace(0.0, 1.45, 400)
    CD = polar_CD(CL, CD0, K)
    ax.plot(CD, CL, **line_kw(0), zorder=4)
    lines = []
    for cl in (TANGENT_CL[0], CLs, TANGENT_CL[1]):
        cd = float(polar_CD(cl, CD0, K))
        ld = cl / cd
        tangent = abs(cl - CLs) < 1e-12
        x_end = 1.2 / ld if tangent else cd
        kw = line_kw("reference") if not tangent else dict(color=INK, lw=1.2, ls=(0, (5, 2.5)))
        ax.plot([0.0, x_end], [0.0, x_end * ld], zorder=3, **kw)
        ax.plot([cd], [cl], "o", ms=6.5, mfc=("white" if not tangent else INK), mec=INK, mew=1.3, zorder=6)
        lines.append((cl, cd, ld))
    slopes = CL[1:] / CD[1:]
    close_to(float(np.max(slopes)), LDm, 1e-4 * LDm, "largest slope is (L/D)max")
    close_to(float(CL[1:][np.argmax(slopes)]), CLs, 0.01, "tangent point at C_L*")
    ax.set_xlim(0.0, 0.11); ax.set_ylim(0.0, 1.5)
    ax.set_xticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.10]); ax.set_yticks([0.0, 0.3, 0.6, 0.9, 1.2, 1.5])
    ax.set_xlabel("Drag coefficient, $C_D$"); ax.set_ylabel("Lift coefficient, $C_L$")
    (c1, d1, l1), (c2, d2, l2), (c3, d3, l3) = lines
    text(ax, (d1, c1), "$L/D$ = " + fmt(l1, 3), direction=-30, dist=12, fs=FS_LABEL)
    text(ax, (d3, c3), "$L/D$ = " + fmt(l3, 3), direction=-30, dist=12, fs=FS_LABEL)
    text(ax, (1.2 / l2, 1.2), "tangent, slope\n$(L/D)_\\max$ = " + fmt(l2, 4), direction=125, dist=12, fs=FS_LABEL)
    # the split of C_D at the tangent point, on the line C_L = C_L*: C_D,0 from 0, then K C_L*^2, equal
    dimension(ax, (0.0, c2), (CD0, c2), None, extension=False)
    dimension(ax, (CD0, c2), (d2, c2), None, extension=False)
    text(ax, (0.5 * CD0, c2), "$C_{D,0}$\n" + fmt_dec(CD0, 3), direction=90, dist=5, fs=FS_LABEL)
    text(ax, (0.5 * (CD0 + d2), c2), "$K\\,{C_L^*}^2$\n" + fmt_dec(K * CLs ** 2, 3), direction=90, dist=5,
         fs=FS_LABEL)
    text(ax, (0.0015, c2), "$C_L^*$ = " + fmt(c2, 4), direction=-90, dist=7, fs=FS_LABEL, ha="left")
    close_to(K * CLs ** 2, CD0, 1e-12, "induced part equals C_D,0 at C_L*")
    close_to(d2 - CD0, CD0, 1e-12, "the two dimensions are equal")
    save_figure(fig, "p33-polar-tangent")


def fig_drag_speed():
    """Top: parasite, induced and total drag against speed for the example; bottom: L/D = W/D. The
    minimum drag and the maximum L/D fall at one speed."""
    E = example()
    W, rho, S, CD0, K = E["W"], E["rho"], E["S"], E["CD0"], E["K"]
    fig, axs = data_axes(6.5, 6.2, nrows=2, sharex=True, gridspec_kw=dict(height_ratios=[1.45, 1.0]))
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.10, top=0.98, hspace=0.10)
    V_lo, V_hi = E["V_lo"], E["V_hi"]
    V = np.linspace(V_lo, V_hi, 600)      # only where the clean polar holds
    close_to(float(level_CL(W, rho, V[0], S)), EX_CLMAX_CLEAN, 1e-9, "left end at the clean C_L,max")
    close_to(V[-1] / E["a"], EX_M_LIMIT, 1e-9, "right end at the Mach limit")
    for a_ in axs:                        # the two speed ranges outside the polar, shaded and named
        for lo, hi in ((100.0, V_lo), (V_hi, 250.0)):
            a_.axvspan(lo, hi, color=BAND_FILL, lw=0, zorder=0.5)
    for xm, s in ((0.5 * (100.0 + V_lo), "stall"), (0.5 * (V_hi + 250.0), "wave drag")):
        text(axs[0], (xm, 118.0), s, rotation=90, fs=FS_SMALL, backing=BAND_FILL)
    Dp, Di, D = (np.asarray(x) / 1000.0 for x in drag_parts(W, rho, V, S, CD0, K))
    ax = axs[0]
    ax.plot(V, D, **line_kw(0), zorder=4)
    ax.plot(V, Dp, **line_kw(1), zorder=3)
    ax.plot(V, Di, **line_kw(2), zorder=3)
    Vmd, Dmin = E["Vmd"], E["Dmin"] / 1000.0
    axs[0].plot([Vmd, Vmd], [E["Dp_md"] / 1000.0, Dmin], **line_kw("boundary"), zorder=2)
    axs[1].plot([Vmd, Vmd], [12.0, E["LDmax"]], **line_kw("boundary"), zorder=2)
    ax.plot([Vmd], [Dmin], "o", ms=6.5, color=INK, zorder=6)
    ax.plot([Vmd], [E["Dp_md"] / 1000.0], "o", ms=5.5, mfc="white", mec=INK, mew=1.2, zorder=6)
    close_to(E["Dp_md"], E["Di_md"], 1e-6 * E["Dp_md"], "parasite = induced at V_md")
    close_to(float(V[np.argmin(D)]), Vmd, 0.3, "drawn minimum at V_md")
    ax.set_ylim(0, 140); ax.set_yticks([0, 20, 40, 60, 80, 100, 120, 140])
    ax.set_ylabel("Drag, kN")
    text(ax, (Vmd, Dmin), "minimum drag,\n" + fmt(E["Dmin"] / 1000.0, 4) + " kN", direction=90, dist=30,
         fs=FS_LABEL)
    text(ax, (Vmd, E["Dp_md"] / 1000.0), "parts equal", direction=-90, dist=12, fs=FS_LABEL)
    for s in E["speeds"]:
        ax.plot([s["V"]], [s["D"] / 1000.0], "s", ms=6, mfc="white", mec=INK, mew=1.3, zorder=6)
    s1, s2 = E["speeds"]
    for s_, d_ in ((s1, 80), (s2, 90)):
        text(ax, (s_["V"], s_["D"] / 1000.0), f"{s_['V']:.0f} m/s,\n" + fmt(s_["D"] / 1000.0, 4) + " kN",
             direction=d_, dist=16, fs=FS_LABEL)
    label_curve(ax, V, D, 224.0, "total", 0, offset=(0, 13), fs=FS_LABEL)
    text(ax, (125.0, 40.0), "parasite,\ngrows as $V^2$", fs=FS_LABEL, color=text_color(1))
    text(ax, (216.0, 43.0), "induced,\nfalls as $1/V^2$", fs=FS_LABEL, color=text_color(2))
    ax = axs[1]
    LD = W / (D * 1000.0)
    ax.plot(V, LD, **line_kw(0), zorder=4)
    ax.plot([Vmd], [E["LDmax"]], "o", ms=6.5, color=INK, zorder=6)
    close_to(float(np.max(LD)), E["LDmax"], 1e-3, "drawn maximum L/D")
    close_to(float(V[np.argmax(LD)]), Vmd, 0.3, "maximum L/D at V_md")
    ax.set_ylim(12, 22); ax.set_yticks([12, 14, 16, 18, 20, 22])
    ax.set_ylabel("Lift-to-drag ratio, $L/D$")
    ax.set_xlabel("True airspeed, $V$, m/s")
    ax.set_xlim(100, 250); ax.set_xticks([100, 125, 150, 175, 200, 225, 250])
    text(ax, (Vmd, E["LDmax"]), "$(L/D)_\\max$ = " + fmt(E["LDmax"], 4) + " at " + fmt(Vmd, 4) + " m/s",
         direction=60, dist=8, fs=FS_LABEL)
    for s in E["speeds"]:
        ax.plot([s["V"]], [s["LD"]], "s", ms=6, mfc="white", mec=INK, mew=1.3, zorder=6)
    save_figure(fig, "p33-drag-speed")


def fig_configurations():
    """Clean, takeoff and landing polars of the example airliner: flaps and gear move the polar to
    the right and make it flatter. The flapped polars carry a point at the lift coefficient their
    increments belong to (Scholz n.d., Section 5.4: C_L = 1.3 takeoff, 1.7 landing), with its L/D.
    No tangent lines here: the page teaches the tangent construction later."""
    cfg = configurations()
    fig, ax = data_axes(6.5, 3.8)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.15, top=0.97)
    CL_top = 1.75
    CL = np.linspace(0.0, CL_top, 300)
    styles = {"clean": 0, "takeoff": 1, "landing": 2}
    for c in cfg:
        CD = polar_CD(CL, c["CD0"], c["K"])
        ax.plot(CD, CL, **line_kw(styles[c["name"]]), zorder=4)
        c["end"] = (float(CD[-1]), CL_top)
        close_to(float(CD[0]), c["CD0"], 1e-12, "nose of the polar at C_D,0")
    for c, mk in ((cfg[1], "s"), (cfg[2], "D")):
        ax.plot([c["CD_op"]], [c["CL_op"]], mk, ms=6.5, color=INK, zorder=6)
        close_to(c["CL_op"] / c["CD_op"], c["LD_op"], 1e-12, "marked L/D")
    ax.set_xlim(0.0, 0.25); ax.set_ylim(0.0, 2.0)
    ax.set_xticks([0.0, 0.05, 0.10, 0.15, 0.20, 0.25]); ax.set_yticks([0.0, 0.4, 0.8, 1.2, 1.6, 2.0])
    ax.set_xlabel("Drag coefficient, $C_D$"); ax.set_ylabel("Lift coefficient, $C_L$")
    c0, c1, c2 = cfg
    text(ax, c0["end"], "clean", direction=90, dist=5, fs=FS_LABEL, color=text_color(0))
    text(ax, c1["end"], "takeoff", direction=95, dist=5, fs=FS_LABEL, color=text_color(1), ha="right")
    text(ax, c2["end"], "landing", direction=85, dist=5, fs=FS_LABEL, color=text_color(2), ha="left")
    # a key for the two marked points, in the free corner (direct labels would sit between the curves)
    for i, (c, mk, nm) in enumerate(((c1, "s", "takeoff"), (c2, "D", "landing"))):
        yk = 0.48 - 0.20 * i
        ax.plot([0.142], [yk], mk, ms=6.5, color=INK, zorder=6)
        text(ax, (0.142, yk), nm + ": $C_L$ = " + fmt_dec(c["CL_op"], 1) + ", $L/D$ = " + fmt(c["LD_op"], 4),
             direction=0, dist=7, fs=FS_LABEL)
    assert c0["CD0"] < c1["CD0"] < c2["CD0"], "flaps and gear add zero-lift drag"
    assert c1["K"] > c0["K"], "flaps lower e, so K grows"
    for cl in (0.5, 1.0, 1.5):                 # every lift coefficient costs more drag
        assert polar_CD(cl, c0["CD0"], c0["K"]) < polar_CD(cl, c1["CD0"], c1["K"]) < polar_CD(cl, c2["CD0"], c2["K"])
    save_figure(fig, "p33-polar-configurations")


def make_all():
    fig_parasite_kinds()
    fig_polar_from_data()
    fig_polar_anatomy()
    fig_symmetric_cambered()
    fig_polar_tangent()
    fig_drag_speed()
    fig_configurations()


def _num(s):
    """The float of a printed string ("1,500,000" -> 1500000.0)."""
    return float(s.replace(",", "").replace("−", "-"))


def values():
    """Every number the page prints, recorded as printed. Where a printed number feeds a later
    printed step, the later step is computed from the printed digits (check_chains)."""
    r = lambda k, v: record(PAGE, k, v)          # noqa: E731
    E = example()
    # givens
    r("W", fmt(E["W"], 7)); r("S", fmt(E["S"], 3)); r("b", fmt_dec(E["b"], 1)); r("e", fmt_dec(E["e"], 2))
    r("CD0", fmt_dec(E["CD0"], 3)); r("h", fmt(E["h"], 4))
    # example 1: AR, K, the table
    r("b2", fmt(E["b"] ** 2, 4))
    AR = r("AR", fmt(E["AR"], 4))
    pieAR = math.pi * E["e"] * _num(AR)
    r("pieAR", fmt(pieAR, 5))
    K = r("K", fmt(1.0 / pieAR, 5))
    Kp = _num(K)
    close_to(Kp, E["K"], 1e-6, "printed K")
    for row in E["table"]:
        c = row["CL"]
        tag = f"{c:.1f}"
        r(f"tbl-CDi-{tag}", fmt_dec(row["CDi"], 5))
        r(f"tbl-CD-{tag}", fmt_dec(row["CD"], 5))
        if c > 0:
            r(f"tbl-LD-{tag}", fmt(row["LD"], 4))
    # the worked line at C_L = 0.6
    cdi = r("ex1-CDi", fmt_dec(Kp * 0.36, 6))
    cd = r("ex1-CD", fmt_dec(E["CD0"] + _num(cdi), 5))
    r("ex1-LD", fmt(0.6 / _num(cd), 4))
    r("ex1-LD-best", fmt(max(rw["LD"] for rw in E["table"]), 4))
    # example 2: atmosphere, C_L*, (L/D)max, V_md, D_min, the check, two other speeds
    r("T", fmt_dec(E["T"], 2))
    r("Tratio", fmt(_num(fmt_dec(E["T"], 2)) / T_SL, 5))
    r("rho-exp", fmt(-G0 / (LAYERS[0][1] * R_AIR) - 1.0, 5))       # the density exponent of page 1.4
    rho = r("rho", fmt(E["rho"], 5))       # five figures, so the drag at the two speeds follows from it
    rhop = _num(rho)
    ratio = r("ratio", fmt(E["CD0"] / Kp, 5))
    CLs = r("CLs", fmt(math.sqrt(_num(ratio)), 4))
    close_to(_num(CLs), E["CLs"], 1e-4, "printed C_L*")
    prod = r("KCD0", fmt_dec(Kp * E["CD0"], 8))
    root = r("root", fmt(math.sqrt(Kp * E["CD0"]), 5))
    LD = r("LDmax", fmt(1.0 / (2.0 * _num(root)), 5))
    close_to(_num(LD), E["LDmax"], 1e-3, "printed (L/D)max")
    r("LDmax4", fmt(E["LDmax"], 4))
    r("LDcheck", fmt(_num(CLs) / (2 * E["CD0"]), 4))
    r("CDs", fmt_dec(2 * E["CD0"], 3))
    den = rhop * E["S"] * _num(CLs)
    r("Vden", fmt(den, 5))
    Vsq = r("Vsq", fmt(2 * E["W"] / _num(fmt(den, 5)), 5))
    Vmd = r("Vmd", fmt(math.sqrt(_num(Vsq)), 5))
    close_to(_num(Vmd), E["Vmd"], 0.02, "printed V_md")
    r("Vmd4", fmt(E["Vmd"], 4))
    r("WS", fmt(E["WS"], 4))
    r("a", fmt(E["a"], 4))
    r("Mmd", fmt(_num(fmt(E["Vmd"], 4)) / _num(fmt(E["a"], 4)), 3))
    Dmin = r("Dmin", fmt(E["W"] / _num(LD), 5))
    close_to(_num(Dmin), E["Dmin"], 2.0, "printed D_min")
    r("Dmin-kN", fmt(E["Dmin"] / 1000.0, 4))
    # the check at V_md: q, the two parts
    r("CLs2", fmt(_num(CLs) ** 2, 5))
    r("CDi-star", fmt_dec(Kp * _num(fmt(_num(CLs) ** 2, 5)), 5))
    r("KW2", fmt_sci(Kp * E["W"] ** 2, 5))
    # two other speeds
    for s in E["speeds"]:
        v = f"{s['V']:.0f}"
        qv = r(f"q-{v}", fmt(0.5 * rhop * s["V"] ** 2, 4))
        qS = r(f"qS-{v}", fmt(_num(qv) * E["S"], 7))
        dp = r(f"Dp-{v}", fmt(_num(qv) * E["S"] * E["CD0"], 5))
        di = r(f"Di-{v}", fmt(Kp * E["W"] ** 2 / _num(qS), 5))
        D = r(f"D-{v}", fmt(_num(dp) + _num(di), 5))
        close_to(_num(D), s["D"], 3.0, "printed drag")
        r(f"D-{v}-kN", fmt(s["D"] / 1000.0, 4))
        r(f"CL-{v}", fmt(E["W"] / (_num(qv) * E["S"]), 4))
        r(f"LD-{v}", fmt(E["W"] / _num(D), 4))
        r(f"M-{v}", fmt(s["V"] / _num(fmt(E["a"], 4)), 3))
        r(f"V-{v}", v)
    # the polar from tunnel data: the section and the three points
    for nm, p in zip("ABC", section_link()[3]):
        r(f"link-{nm}-alpha", fmt(p["alpha"], 1, minus="−"))
        r(f"link-{nm}-cl", fmt_dec(p["cl"], 2, minus="−"))
        r(f"link-{nm}-cd", fmt_dec(p["cd"], 4))
    # symmetric and cambered: the low-drag ranges at 9 million
    for k, tag in (("64-018", "018"), ("64-618", "618")):
        b = bucket(k, SYMCAM_RE)
        r(f"bucket-{tag}-lo", fmt_dec(b["lo"], 2, minus="−"))
        r(f"bucket-{tag}-hi", fmt_dec(b["hi"], 2))
        r(f"bucket-{tag}-cdmin", fmt_dec(b["cd_min"], 4))
    r("bucket-frac", "10")
    # numbers quoted from sources, and the warnings
    r("glenn-plate", "1.28"); r("glenn-airfoil", "0.045"); r("glenn-factor", "30")
    r("scholz-CD0", "0.02"); r("wave-pct", "10")
    r("mass", fmt(E["W"] / G0, 3))
    r("g2", fmt(G0 ** 2, 4))
    # the tangent figure and the drag figure (alt texts)
    for cl in TANGENT_CL:
        r(f"tan-CL-{cl}", fmt(cl, 2) if cl >= 1 else fmt(cl, 1))
        r(f"tan-LD-{cl}", fmt(cl / float(polar_CD(cl, E["CD0"], E["K"])), 3))
    r("Dp-md-kN", fmt(E["Dp_md"] / 1000.0, 3))
    # configurations
    for c in configurations():
        n = c["name"]
        r(f"cfg-{n}-CD0", fmt_dec(c["CD0"], 3))
        r(f"cfg-{n}-e", fmt_dec(c["e"], 2))
        r(f"cfg-{n}-LDmax", fmt(min_drag_point(c["CD0"], c["K"])["LD_max"], 4))
        r(f"cfg-{n}-K", fmt(c["K"], 4))
        if n != "clean":
            r(f"cfg-{n}-flap", fmt_dec(FLAPS_GEAR[n]["dCD_flap"], 2))
            r(f"cfg-{n}-gear", fmt_dec(FLAPS_GEAR[n]["dCD_gear"], 3))
            r(f"cfg-{n}-deg", str(FLAPS_GEAR[n]["flap_deg"]))
            r(f"cfg-{n}-CLop", fmt_dec(c["CL_op"], 1))
            r(f"cfg-{n}-LDop", fmt(c["LD_op"], 4))
            r(f"cfg-{n}-CLs", fmt(c["CLs"], 3))
    # the range of the drag-speed figure
    r("clmax-clean", fmt_dec(EX_CLMAX_CLEAN, 1)); r("M-limit", fmt_dec(EX_M_LIMIT, 2))
    r("V-lo", fmt(E["V_lo"], 4)); r("V-hi", fmt(E["V_hi"], 4))
    # worked example 3: (a) C_D,0 and K from two measured drags, printed step by step
    X = example3()
    r("ex3-W", fmt(X["W"], 6)); r("ex3-S", fmt(X["S"], 3)); r("ex3-h", fmt(X["h"], 4))
    rho3 = r("ex3-rho", fmt(X["rho"], 4))
    cls, cds = [], []
    for i, p in enumerate(X["pts"], start=1):
        r(f"ex3-V{i}", f"{p['V']:.0f}"); r(f"ex3-D{i}", fmt(p["D"], 5))
        q = r(f"ex3-q{i}", fmt(0.5 * _num(rho3) * p["V"] ** 2, 5))
        qS = r(f"ex3-qS{i}", fmt(_num(q) * X["S"], 6))
        cl = r(f"ex3-CL{i}", fmt(X["W"] / _num(qS), 5))
        r(f"ex3-CL2{i}", fmt(_num(cl) ** 2, 5))
        cd = r(f"ex3-CD{i}", fmt(p["D"] / _num(qS), 5))
        cls.append(_num(fmt(_num(cl) ** 2, 5))); cds.append(_num(cd))
    dcd = r("ex3-dCD", fmt(cds[0] - cds[1], 5))
    dcl = r("ex3-dCL2", fmt(cls[0] - cls[1], 5))
    K3 = r("ex3-K", fmt(_num(dcd) / _num(dcl), 5))
    kcl = r("ex3-KCL2", fmt(_num(K3) * cls[0], 5))
    CD03 = r("ex3-CD0", fmt(cds[0] - _num(kcl), 5))
    close_to(_num(K3), X["K"], 2e-3 * X["K"], "printed K of example 3")
    close_to(_num(CD03), X["CD0"], 2e-3 * X["CD0"], "printed C_D,0 of example 3")
    r("ex3-check", fmt(_num(CD03) + _num(K3) * cls[1], 5))
    r("ex3-CD0-3", fmt(X["CD0"], 3)); r("ex3-K-3", fmt(X["K"], 3))
    # (b) K from (L/D)max
    r("ex3b-CD0", fmt_dec(EX3B["CD0"], 3)); r("ex3b-LD", fmt_dec(EX3B["LDmax"], 1))
    den = r("ex3b-den", fmt(4.0 * EX3B["CD0"] * EX3B["LDmax"] ** 2, 4))
    Kb3 = r("ex3b-K", fmt(1.0 / _num(den), 5))
    # the check: (L/D)max back from the printed K, 1/(2 sqrt(K C_D,0))
    r("ex3b-check", fmt(1.0 / (2.0 * math.sqrt(_num(Kb3) * EX3B["CD0"])), 4))
    close_to(_num(fmt(1.0 / _num(den), 5)), X["Kb"], 1e-4 * X["Kb"], "printed K of example 3b")
