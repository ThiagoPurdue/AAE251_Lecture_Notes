"""Figures and values of 5.3 Climb and Ceiling (notes/chapter-5/climb-and-ceiling.md).

Aircraft (from vehicles.py):
  - EXEC_JET, the twin-engine executive jet: the climb with both engines at 135 m/s, the steepest
    and fastest climbs, the ceilings (closed form and a table of maximum rate of climb), and one
    engine out by the closed form of the steepest climb.
  - TRANSPORT, the four-engine turboprop transport: the absolute ceiling of a propeller aircraft,
    and one engine out of four (three left) against a ridge, at 105 m/s and then at 82 m/s.
Scenario values chosen for this page and screened against the course's problems: 135 m/s; the
table altitudes 0, 2,500, 5,000, 9,500, 13,000 and 14,500 m; a ridge 360 m high, 4,400 m
from the start of the climb; 105 and 82 m/s for the transport.

Every relation is the shallow-climb model of perf.py (climb_jet, climb_prop): drag computed with
L = m g, T = D + m g sin(gamma), R/C = V sin(gamma) = (P_A - P_R) / (m g).
"""
from chapter_5.common import *
from matplotlib.patches import Polygon

PAGE = "p53"

JET, TR = EXEC_JET, TRANSPORT
V_WE1 = 135.0                                   # m/s, the jet's climb speed of worked example 1
CEIL_ALTS = (0.0, 2500.0, 5000.0, 9500.0, 13000.0, 14500.0)
N_LEFT = 3                                      # engines left on the transport with one out
V_TR_FAST, V_TR_SLOW = 105.0, 82.0              # m/s, the transport's two climb speeds
RIDGE_D, RIDGE_H = 4400.0, 360.0                # m, distance to the ridge top and its height
GAMMA_FAMILY = 3.0                              # deg, the middle curve of the climb-thrust figure
JET_GAIN_H = 100.0                              # m, height the one-engine jet must gain
GRADIENT_TWIN, GRADIENT_FOUR = 2.4, 3.0         # percent: 14 CFR 25.121(b), one engine out, gear up

# Drawing constants of the climb-forces figure (ALPHA_DRAWN, GAMMA_DRAWN, LD_DRAWN, W_DRAWN, AC_LENGTH,
# SCALE_IN_PER_UNIT, INSET) come from looks.py: the one scale shared with page 5.1's level-flight figure.


def _mach_text():
    """The jet's Mach limit as printed on the page and in the figures ("Mach 0.80"), from vehicles.py."""
    return f"Mach {fmt_dec(JET['M_limit'], 2)}"


def _band_label():
    """Name of the wave-drag band, as on page 5.1: where it starts and why the polar fails there."""
    return f"past {_mach_text()}:\nwave drag"


STRAIGHT_LINE = "#4C95D0"    # the wide stroke of the straight line in p53-jet-ceiling: 3.2:1 on white, lighter than ink


def _tropopause(ax, label_xy=None, fs=FS_SMALL):
    """Thin dotted line at the tropopause, where the standard atmosphere's temperature stops falling
    (the corner of every curve against altitude); named once per figure at label_xy (data)."""
    hk = H_TROPOPAUSE / 1e3
    ln = ax.axhline(hk, color=GRAY, lw=LW_THIN, ls=(0, (1.0, 2.5)), zorder=1.5)
    if label_xy is not None:
        text(ax, label_xy, f"tropopause,\n{fmt(hk, 2)} km", fs=fs, color=STEEL)
    return ln


def _num(s):
    return float(s.replace(",", "").replace("−", "-"))


def _jet():
    return JET["m"], JET["S"], JET["CD0"], JET["K"]


def _tr():
    return TR["m"], TR["S"], TR["CD0"], TR["K"]


def _rc_max_jet(h):
    rho = standard(h)[2]
    m, S, CD0, K = _jet()
    return jet_max_roc(m, S, CD0, K, rho, available(JET, rho))


def _mach_band_altitude():
    """Altitude (m) above which the jet's fastest-climb speed passes its Mach limit (bisection)."""
    def over(h):
        T_ = standard(h)[0]
        return _rc_max_jet(h)["V"] - JET["M_limit"] * float(speed_of_sound(T_))
    lo, hi = 0.0, 15000.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if over(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _tr_climb(V):
    m, S, CD0, K = _tr()
    return climb_prop(m, S, CD0, K, RHO_SL, available(TR, RHO_SL, n=N_LEFT), V)


# ===================================================================== figures
def fig_climb_forces():
    """Lesson: in a climb the thrust balances the drag plus the part of the weight along the path.
    The aircraft and its forces are drawn at the scale of page 5.1's level-flight figure (same
    outline length, same weight arrow, same drawn L/D); the inset splits the weight as page 4.2 does."""
    g, a = GAMMA_DRAWN, ALPHA_DRAWN
    W = W_DRAWN
    xl, yl = (-2.75, 4.65), (-2.05, 2.05)
    fig, ax = canvas(SCALE_IN_PER_UNIT * (xl[1] - xl[0]), xlim=xl, ylim=yl)
    ac = aircraft_silhouette_right(ax, center=(0.0, 0.0), length=AC_LENGTH, pitch_deg=g + a, fill=PART_FILL)
    cg = ac["cg"]
    cg_symbol(ax, cg, size=10.0)
    path_f = ray(ax, cg, g, 2.45, role="reference", zorder=1.5)
    ray(ax, cg, 180.0 + g, 1.65, role="reference", zorder=1.5)
    ray(ax, cg, 0.0, 2.15, role="reference", zorder=1.5)
    text(ax, cg + np.array([2.15, 0.0]), "horizontal", direction=0, dist=4, fs=FS_LABEL, color=STEEL)
    body = ray(ax, cg, g + a, 2.85, role="boundary", zorder=2.0)
    ray(ax, cg, 180.0 + g + a, 1.4, role="boundary", zorder=2.0)
    text(ax, cg + 2.85 * unit(g + a), "body axis", direction=g + a, dist=4, fs=FS_LABEL, color=STEEL)
    f = climb_forces(ax, cg, W, g, a, LD_drawn=LD_DRAWN, starts=dict(L=0.10, W=0.10, D=1.72, T=1.32),
                     label_dirs=dict(T=g + a + 90.0, D=g + 180.0), rides=dict(T=body))
    angle_mark(ax, cg, g, g + a, 2.25, r"$\alpha$", stated=a, label_r=2.55, fs=FS_LABEL)
    angle_mark(ax, cg, 0.0, g, 1.6, r"$\gamma$", stated=g, label_r=1.9, fs=FS_LABEL)
    v0 = cg + 2.55 * unit(g)
    rides_on(kind_arrow(ax, v0, v0 + 0.9 * unit(g), "velocity"), path_f)
    text(ax, v0 + 0.9 * unit(g), "velocity, $V$", direction=g - 60.0, dist=6, color=SERIES[0], fs=FS_LABEL)
    text(ax, v0 + 0.3 * unit(g), "flight path", direction=g - 90.0, dist=17, color=STEEL, fs=FS_LABEL)
    ws = weight_split(ax, (3.55, -0.15), INSET * W, g, arc_r=0.75, along_dir=g + 180.0, title=None)
    text(ax, (3.55, -0.15 + 0.22 * INSET * W), "the weight, split", fs=FS_LABEL)
    yk = legend_key(ax, (-2.65, 1.9), [("force", "force"), ("velocity", "velocity")], dy=19, fs=FS_LABEL)
    # the two angles named once, under the key (the arcs carry the symbols)
    text(ax, (-2.65, yk), "$\\gamma$: climb angle", ha="left", va="center", fs=FS_LABEL)
    text(ax, (-2.65, yk - 0.27), "$\\alpha$: angle of attack", ha="left", va="center", fs=FS_LABEL)
    # what the figure must show: the drawn forces balance, and the thrust along the path carries the
    # drag plus m g sin(gamma), so it is drawn longer than the drag
    close_to(float(np.linalg.norm(f["L"] + f["W"] + f["D"] + f["T"])), 0.0, 1e-12, "drawn forces in balance")
    along_T = float(np.dot(f["T"], f["u"]))
    close_to(along_T, -float(np.dot(f["D"], f["u"])) + W * math.sin(math.radians(g)), 1e-12,
             "thrust along the path = drag + m g sin(gamma)")
    assert np.linalg.norm(f["T"]) > 1.5 * np.linalg.norm(f["D"]), "thrust visibly longer than drag"
    close_to(float(np.linalg.norm(ws["along"])), INSET * W * math.sin(math.radians(g)), 1e-12,
             "inset to its stated scale")
    trim_canvas(fig)
    save_figure(fig, "p53-climb-forces")


def fig_velocity_triangle():
    """Lesson: the rate of climb is the vertical part of the flight velocity, V sin(gamma)."""
    g = GAMMA_DRAWN
    fig, ax = canvas(4.2, xlim=(-0.35, 3.45), ylim=(-0.75, 1.55))
    o = np.array([0.0, 0.0])
    Vlen = 2.6
    path = ray(ax, o, g, 3.25, role="reference", zorder=1.5)
    text(ax, o + 3.25 * unit(g), "flight path", direction=g, dist=4, fs=FS_SMALL, color=STEEL)
    hor = line(ax, (-0.25, 0.0), (3.3, 0.0), role="reference", zorder=1.5)
    text(ax, (3.3, 0.0), "horizontal", direction=-90, dist=5, fs=FS_SMALL, color=STEEL, ha="right")
    Vv = Vlen * unit(g)
    h = np.array([Vv[0], 0.0])
    v = np.array([0.0, Vv[1]])
    close_to(float(np.linalg.norm(h + v - Vv)), 0.0, 1e-12, "the two parts close the velocity triangle")
    aV = rides_on(kind_arrow(ax, o, o + Vv, "velocity"), path)
    rides_on(kind_arrow(ax, o, o + h, "velocity", lw=1.3), hor)
    av = kind_arrow(ax, o + h, o + h + v, "velocity", lw=1.3)
    angle_mark(ax, o, 0.0, g, 0.75, r"$\gamma$", stated=g, label_r=1.05)
    blue = SERIES[0]
    text(ax, o + 0.5 * Vv, "velocity, $V$", direction=g + 90.0, dist=14, color=blue)
    text(ax, o + 0.5 * h, "$V\\cos\\gamma$", direction=-90.0, dist=6, color=blue)
    text(ax, o + h + 0.5 * v, "rate of climb,\n$R/C = V\\sin\\gamma$", direction=0.0, dist=7, color=blue)
    # measured on the drawn arrows and lines: the vertical arrow starts on the drawn horizontal and ends
    # on the drawn flight path, at the tip of V, and its length is the drawn V times sin(gamma)
    (pa0, pa1), (pv0, pv1) = (np.asarray(x_, float) for x_ in aV._posA_posB), (np.asarray(x_, float) for x_ in av._posA_posB)
    px, py = (np.asarray(d_, float) for d_ in path.get_data())
    d_path = np.array([px[-1] - px[0], py[-1] - py[0]])
    close_to(float(np.cross(d_path, pv1 - np.array([px[0], py[0]]))), 0.0, 1e-9, "R/C arrow ends on the drawn path")
    close_to(float(pv0[1] - hor.get_data()[1][0]), 0.0, 1e-12, "R/C arrow starts on the drawn horizontal")
    close_to(float(np.linalg.norm(pv1 - pa1)), 0.0, 1e-12, "R/C arrow ends at the tip of V")
    close_to(float(pv1[1] - pv0[1]), float(np.linalg.norm(pa1 - pa0)) * math.sin(math.radians(g)), 1e-12,
             "vertical side drawn as V sin(gamma)")
    trim_canvas(fig)
    save_figure(fig, "p53-velocity-triangle")


def fig_climb_thrust():
    """Lesson: climbing at the angle gamma raises the whole thrust-required curve by m g sin(gamma);
    the steepest climb is the curve that just touches the thrust available, at the minimum-thrust speed."""
    m, S, CD0, K = _jet()
    W = m * G0
    TA = available(JET, RHO_SL) / 1e3
    Vs = stall_speed_mass(m, S, JET["CLmax"], RHO_SL)
    VM = JET["M_limit"] * float(speed_of_sound(T_SL))
    g_max = jet_max_climb_angle(m, S, CD0, K, RHO_SL, available(JET, RHO_SL))
    mt = min_thrust_condition(m, S, CD0, K, RHO_SL)
    X0, X1 = 40.0, 300.0
    V = np.linspace(Vs, X1, 800)
    TR0 = thrust_required(m, S, CD0, K, RHO_SL, V) / 1e3
    fig, ax = data_axes(6.5, 4.3)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.13, top=0.91)
    ax.set_xlim(X0, X1); ax.set_ylim(0.0, 80.0)
    ax.set_xticks([50, 100, 150, 200, 250, 300]); ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Thrust, kN")
    stall_band(ax, Vs, y_label=62.0)
    mach_band(ax, VM, label=_band_label(), y_label=27.0)
    panel_title(ax, "executive jet, two engines, sea level")
    gammas = (0.0, GAMMA_FAMILY, g_max["gamma_deg"])
    curves = []
    for i, gd in enumerate(gammas):
        lift = W * math.sin(math.radians(gd)) / 1e3
        y = TR0 + lift
        draw_curve(ax, V, y, required_kw(0), x_valid=VM)
        curves.append((gd, y, lift))
    draw_curve(ax, np.array([Vs, X1]), np.array([TA, TA]), available_kw(0), x_valid=VM)
    # labels centered in the gaps between the curves (each gap is m g sin(gamma) tall)
    text(ax, (125.0, 11.0), "level flight, $\\gamma$ = 0", fs=FS_SMALL)
    text(ax, (100.0, 30.5), f"$\\gamma$ = {fmt(GAMMA_FAMILY, 1)}°", fs=FS_SMALL)
    text(ax, (135.0, 50.5), "thrust available, $T_A$", fs=FS_LABEL)
    text(ax, (112.0, 71.0), f"steepest climb,\n$\\gamma_\\max$ = {fmt(gammas[-1], 3)}°\nat {fmt(mt['V'], 4)} m/s",
         fs=FS_LABEL)
    y_top = curves[-1][1]
    mark_minimum(ax, mt["V"], float(np.interp(mt["V"], V, y_top)))
    xd = 150.0
    y0d, y3d = float(np.interp(xd, V, curves[0][1])), float(np.interp(xd, V, curves[1][1]))
    dimension(ax, (xd, y0d), (xd, y3d), None, ticks=False, extension=False)
    text(ax, (xd, 0.5 * (y0d + y3d)), "$mg\\,\\sin\\gamma$", direction=180, dist=4, fs=FS_SMALL)
    y3 = curves[1][1]
    k = int(np.argmax((V > mt["V"]) & (y3 >= TA)))
    v3 = float(np.interp(TA, [y3[k - 1], y3[k]], [V[k - 1], V[k]]))
    mark_limit(ax, v3, TA, f"{fmt(v3, 4)} m/s", direction=140, dist=8, fs=FS_SMALL, drop=True)
    close_to(float(np.max(np.abs(curves[1][1] - curves[0][1] - curves[1][2]))), 0.0, 1e-9, "curve raised by m g sin gamma")
    close_to(float(np.min(y_top)), TA, 0.01, "the steepest curve just touches T_A")
    close_to(float(V[np.argmin(y_top)]), mt["V"], 0.4, "and touches it at V_TR,min")
    assert v3 < VM, "the crossing at GAMMA_FAMILY lies inside the polar's range"
    save_figure(fig, "p53-climb-thrust")


def fig_excess_power():
    """Lesson: the rate of climb is largest where the gap between power available and power required
    is widest; for a jet that is well above the speed of the steepest climb."""
    m, S, CD0, K = _jet()
    TA = available(JET, RHO_SL)
    Vs = stall_speed_mass(m, S, JET["CLmax"], RHO_SL)
    VM = JET["M_limit"] * float(speed_of_sound(T_SL))
    _, vmax = jet_speed_bounds(m, S, CD0, K, RHO_SL, TA)
    rc = jet_max_roc(m, S, CD0, K, RHO_SL, TA)
    X1 = 300.0
    V = np.linspace(Vs, X1, 800)
    PR = power_required(m, S, CD0, K, RHO_SL, V) / 1e6
    PA = TA * V / 1e6
    fig, ax = data_axes(6.5, 4.2)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.13, top=0.91)
    ax.set_xlim(0.0, X1); ax.set_ylim(0.0, 18.0)
    ax.set_xticks([0, 50, 100, 150, 200, 250, 300]); ax.set_yticks([0, 3, 6, 9, 12, 15, 18])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Power, MW")
    stall_band(ax, Vs, y_label=11.0)
    mach_band(ax, VM, label=_band_label(), y_label=5.0)
    panel_title(ax, "executive jet, two engines, sea level")
    mask = V <= vmax
    ax.fill_between(V[mask], PR[mask], PA[mask], color=HIGHLIGHT, lw=0, zorder=1)
    draw_curve(ax, V, PR, required_kw(0), x_valid=VM)
    draw_curve(ax, V, PA, available_kw(0), x_valid=VM)
    vrc, pa_rc, pr_rc = rc["V"], rc["P_A"] / 1e6, rc["P_R"] / 1e6
    dimension(ax, (vrc, pr_rc), (vrc, pa_rc), None, ticks=False, extension=False, zorder=5)
    callout(ax, (vrc, pa_rc),
            f"widest gap, at {fmt(vrc, 4)} m/s:\n$(R/C)_\\max$ = {fmt(rc['RC_max'], 4)} m/s",
            at=(75.0, 14.6), ha="left", fs=FS_LABEL)
    text(ax, (115.0, float(np.interp(115.0, V, PR))), "power required, $P_R$", direction=-35, dist=10, fs=FS_LABEL)
    text(ax, (138.0, float(np.interp(138.0, V, PA))), "power available,\n$P_A = T_A V$", direction=120, dist=8,
         fs=FS_LABEL)
    text(ax, (128.0, 4.8), "excess\npower", fs=FS_SMALL, backing=HIGHLIGHT)
    mark_limit(ax, vmax, TA * vmax / 1e6, f"$V_\\max$ = {fmt(vmax, 4)} m/s", direction=150, dist=10, fs=FS_LABEL)
    gap = PA - PR
    close_to(float(V[np.argmax(np.where(mask, gap, -1e9))]), vrc, 0.4, "drawn gap widest at the max R/C speed")
    assert vrc > min_thrust_condition(m, S, CD0, K, RHO_SL)["V"] and vmax < VM
    save_figure(fig, "p53-excess-power")


def fig_hodograph():
    """Lesson: the tangent from the origin to the curve of vertical against horizontal speed gives the
    steepest climb and its top gives the fastest, which is why the two speeds differ."""
    m, S, CD0, K = _jet()
    TA = available(JET, RHO_SL)
    Vs = stall_speed_mass(m, S, JET["CLmax"], RHO_SL)
    _, vmax = jet_speed_bounds(m, S, CD0, K, RHO_SL, TA)
    V = np.linspace(Vs, vmax, 4000)
    hd = climb_hodograph(m, S, CD0, K, RHO_SL, V, TA, "jet")
    g = jet_max_climb_angle(m, S, CD0, K, RHO_SL, TA)
    r = jet_max_roc(m, S, CD0, K, RHO_SL, TA)
    st = dict(V=g["V"], Vh=g["V"] * math.cos(g["gamma_rad"]), Vv=g["V"] * g["sin_gamma"])
    fa = dict(V=r["V"], Vh=r["V"] * math.cos(math.radians(r["gamma_deg"])), Vv=r["RC_max"])
    c1 = climb_jet(m, S, CD0, K, RHO_SL, TA, V_WE1)
    w1 = dict(Vh=V_WE1 * math.cos(math.radians(float(c1["gamma_deg"]))), Vv=float(c1["RC"]))
    fig, ax = data_axes(6.5, 4.2)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.13, top=0.91)
    ax.set_xlim(0.0, 280.0); ax.set_ylim(0.0, 20.0)
    ax.set_xticks([0, 40, 80, 120, 160, 200, 240, 280]); ax.set_yticks([0, 4, 8, 12, 16, 20])
    ax.set_xlabel("Horizontal speed, $V\\cos\\gamma$, m/s"); ax.set_ylabel("Rate of climb, $R/C$, m/s")
    stall_band(ax, float(hd["Vh"][0]), y_label=14.0)
    ax.plot(hd["Vh"], hd["Vv"], zorder=4, **required_kw(0))
    panel_title(ax, "executive jet, two engines, sea level")
    tangent_from_origin(ax, st["Vh"], st["Vv"], st["Vh"], None, origin_label=None)
    text(ax, (40.0, 40.0 * st["Vv"] / st["Vh"]), "slope\n= tan $\\gamma$", direction=125, dist=6, fs=FS_SMALL,
         backing=BAND_FILL)
    callout(ax, (st["Vh"], st["Vv"]), f"steepest climb:\n$\\gamma_\\max$ = {fmt(g['gamma_deg'], 3)}°\nat $V$ = {fmt(st['V'], 4)} m/s",
            at=(122.0, 6.6), ha="left", fs=FS_LABEL)
    mark_minimum(ax, fa["Vh"], fa["Vv"], f"fastest climb: {fmt(fa['Vv'], 4)} m/s\nat $V$ = {fmt(fa['V'], 4)} m/s",
                 direction=60, dist=8, fs=FS_SMALL)
    ax.plot([w1["Vh"]], [w1["Vv"]], "o", ms=6.0, mfc="white", mec=INK, mew=1.3, zorder=6)
    text(ax, (w1["Vh"], w1["Vv"]),
         f"worked example 1,\n$V$ = {fmt(V_WE1, 3)} m/s:\n{fmt(float(c1['RC']), 4)} m/s, {fmt(float(c1['gamma_deg']), 3)}°",
         direction=115, dist=8, fs=FS_SMALL)
    ratio = hd["Vv"] / hd["Vh"]
    i = int(np.argmax(ratio))
    close_to(float(hd["V"][i]), g["V"], 0.3, "the line from the origin touches at V_TR,min")
    close_to(float(hd["V"][int(np.argmax(hd["Vv"]))]), r["V"], 0.3, "the top of the drawn curve is the fastest climb")
    assert r["V"] > g["V"]
    save_figure(fig, "p53-hodograph")


def fig_why_a_ceiling():
    """Lesson: a jet stops climbing when its thrust available has fallen to a value that does not change
    with altitude; a propeller aircraft is caught between a falling and a rising curve."""
    mj, Sj, CD0j, Kj = _jet()
    mt_, St, CD0t, Kt = _tr()
    jc = jet_absolute_ceiling(mj, CD0j, Kj, JET["n"], JET["T0"], JET["m_ad"])
    pc = prop_absolute_ceiling(mt_, St, CD0t, Kt, TR["n"], TR["P0"], TR["eta"], TR["m_ad"])
    fig, axs = data_axes(6.5, 4.2, ncols=2)
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.14, top=0.91, wspace=0.30)
    ax = axs[0]
    h = np.linspace(0.0, 18000.0, 400)
    rho = standard(h)[2]
    TA = available(JET, rho) / 1e3
    Tmin = jc["T_min"] / 1e3
    ax.set_xlim(0.0, 60.0); ax.set_ylim(0.0, 18.0)
    ax.set_xticks([0, 20, 40, 60]); ax.set_yticks([0, 3, 6, 9, 12, 15, 18])
    ax.set_xlabel("Thrust, kN"); ax.set_ylabel("Altitude, $h$, km")
    panel_title(ax, "executive jet, two engines")
    _tropopause(ax, label_xy=(49.0, H_TROPOPAUSE / 1e3 + 1.3))
    ax.plot(TA, h / 1e3, zorder=4, **available_kw(0))
    ax.plot([Tmin, Tmin], [0.0, 18.0], zorder=4, **required_kw(0))
    ax.plot([0.0, Tmin], [jc["h_abs"] / 1e3] * 2, color=GRAY, lw=LW_THIN, ls=DASH_CONSTRUCTION, zorder=2)
    ax.plot([Tmin], [jc["h_abs"] / 1e3], "D", ms=MS_POINT - 0.5, color=INK, zorder=7)
    text(ax, (40.0, float(np.interp(-40.0, -TA, h / 1e3))), "$T_A$", direction=20, dist=11, fs=FS_LABEL)
    text(ax, (Tmin, 3.0), "$T_{R,\\min}$,\nconstant", direction=0, dist=6, fs=FS_LABEL)
    text(ax, (Tmin, jc["h_abs"] / 1e3), f"ceiling,\n{fmt(jc['h_abs'] / 1e3, 4)} km", direction=40, dist=10,
         fs=FS_SMALL)
    ax = axs[1]
    PA = available(TR, rho) / 1e3
    PRmin = np.array([min_power_condition(mt_, St, CD0t, Kt, r_)["P_min"] for r_ in rho]) / 1e3
    ax.set_xlim(0.0, 12000.0); ax.set_ylim(0.0, 18.0)
    ax.set_xticks([0, 4000, 8000, 12000]); ax.set_yticks([0, 3, 6, 9, 12, 15, 18])
    ax.set_xticklabels(["0", "4,000", "8,000", "12,000"])
    ax.set_xlabel("Power, kW")
    panel_title(ax, "turboprop transport, four engines")
    _tropopause(ax)
    ax.plot(PA, h / 1e3, zorder=4, **available_kw(0))
    ax.plot(PRmin, h / 1e3, zorder=4, **required_kw(0))
    ax.plot([0.0, pc["P_ceil"] / 1e3], [pc["h_abs"] / 1e3] * 2, color=GRAY, lw=LW_THIN, ls=DASH_CONSTRUCTION, zorder=2)
    ax.plot([pc["P_ceil"] / 1e3], [pc["h_abs"] / 1e3], "D", ms=MS_POINT - 0.5, color=INK, zorder=7)
    text(ax, (8000.0, float(np.interp(-8000.0, -PA, h / 1e3))), "$P_A$", direction=20, dist=11, fs=FS_LABEL)
    text(ax, (float(np.interp(15.5, h / 1e3, PRmin)), 15.5), "$P_{R,\\min}$,\nrising",
         direction=-30, dist=14, fs=FS_LABEL)
    text(ax, (pc["P_ceil"] / 1e3, pc["h_abs"] / 1e3), f"ceiling,\n{fmt(pc['h_abs'] / 1e3, 3)} km",
         direction=-10, dist=12, fs=FS_SMALL)
    close_to(float(np.interp(Tmin, TA[::-1], h[::-1])), jc["h_abs"], 30.0, "T_A meets T_R,min at the jet ceiling")
    d = PA - PRmin
    close_to(float(np.interp(0.0, d[::-1], h[::-1])), pc["h_abs"], 30.0, "P_A meets P_R,min at the transport ceiling")
    assert PRmin[-1] > PRmin[0], "the minimum power required rises with altitude"
    save_figure(fig, "p53-why-a-ceiling")


def fig_jet_ceiling():
    """Lesson: the service ceiling is where the maximum rate of climb has fallen to 0.5 m/s and the
    absolute ceiling where it reaches zero; near the top the curve is nearly straight, so a line
    through the last two table rows finds both."""
    m, S, CD0, K = _jet()
    jc = jet_absolute_ceiling(m, CD0, K, JET["n"], JET["T0"], JET["m_ad"])
    h_srv = ceiling_by_bisection(lambda h: _rc_max_jet(h)["RC_max"], SERVICE_CEILING_RC)
    h_band = _mach_band_altitude()
    hs = np.linspace(0.0, jc["h_abs"], 300)
    rcs = np.array([_rc_max_jet(h)["RC_max"] for h in hs])
    rows = [(h, float(fmt_dec(_rc_max_jet(h)["RC_max"], 2))) for h in CEIL_ALTS]
    (h1, r1), (h2, r2) = rows[-2], rows[-1]
    slope = (h2 - h1) / (r2 - r1)
    fig, axs = data_axes(6.5, 4.4, ncols=2, gridspec_kw=dict(width_ratios=[1.15, 1.0]))
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.13, top=0.91, wspace=0.32)
    ax = axs[0]
    ax.set_xlim(0.0, 18.0); ax.set_ylim(0.0, 18.0)
    ax.set_xticks([0, 3, 6, 9, 12, 15, 18]); ax.set_yticks([0, 3, 6, 9, 12, 15, 18])
    ax.set_xlabel("Maximum rate of climb, m/s"); ax.set_ylabel("Altitude, $h$, km")
    panel_title(ax, "sea level to the ceiling")
    ax.axhspan(h_band / 1e3, 18.0, color=BAND_FILL, lw=0, zorder=0.5)
    text(ax, (12.0, 16.2), f"fastest climb past\n{_mach_text()}: wave drag", fs=FS_SMALL, backing=BAND_FILL)
    _tropopause(ax, label_xy=(14.5, H_TROPOPAUSE / 1e3 - 1.25))
    ok = hs <= h_band                               # thick below the band, thin inside it (the chapter's look)
    kb = required_kw(0, linewidth=LW_BEYOND)
    ax.plot(rcs[ok], hs[ok] / 1e3, zorder=4, **required_kw(0))
    ax.plot(rcs[~ok], hs[~ok] / 1e3, zorder=4, **kb)
    ax.plot([r for _, r in rows], [h / 1e3 for h, _ in rows], "o", ms=6.0, mfc="white", mec=INK, mew=1.3,
            zorder=6, linestyle="none", clip_on=False)
    text(ax, (rows[1][1], rows[1][0] / 1e3), "table rows", direction=35, dist=8, fs=FS_SMALL)
    ax = axs[1]
    lo, hi = 12.5, 16.0
    ax.set_xlim(0.0, 4.0); ax.set_ylim(lo, hi)
    ax.set_xticks([0, 1, 2, 3, 4]); ax.set_yticks([13, 14, 15, 16])
    ax.set_xlabel("Maximum rate of climb, m/s")
    panel_title(ax, "the top, enlarged")
    ax.axhspan(h_band / 1e3, hi, color=BAND_FILL, lw=0, zorder=0.5)
    text(ax, (3.05, 15.8), f"past {_mach_text()}", fs=FS_SMALL, backing=BAND_FILL)
    ax.plot(rcs[ok], hs[ok] / 1e3, zorder=4, **required_kw(0))
    ax.plot(rcs[~ok], hs[~ok] / 1e3, zorder=4, **kb)
    # the straight line: a wide light stroke under the curve, so both show where they lie together
    rr = np.array([0.0, 3.6])
    ax.plot(rr, (h2 + slope * (rr - r2)) / 1e3, color=STRAIGHT_LINE, lw=6.0, solid_capstyle="butt", zorder=3)
    ax.plot([r1, r2], [h1 / 1e3, h2 / 1e3], "o", ms=6.0, mfc="white", mec=INK, mew=1.3, zorder=6, linestyle="none")
    text(ax, (r1, h1 / 1e3), f"{fmt(h1, 5)} m", direction=215, dist=12, fs=FS_SMALL, backing=BAND_FILL)
    text(ax, (r2, h2 / 1e3), f"{fmt(h2, 5)} m", direction=40, dist=7, fs=FS_SMALL, backing=BAND_FILL)
    ax.plot([SERVICE_CEILING_RC] * 2, [lo, h_srv / 1e3], color=GRAY, lw=LW_THIN, zorder=2)
    text(ax, (SERVICE_CEILING_RC, 13.6), f"{fmt_dec(SERVICE_CEILING_RC, 1)} m/s", direction=0, dist=4, fs=FS_SMALL,
         backing=BAND_FILL)
    ax.plot([SERVICE_CEILING_RC], [h_srv / 1e3], "s", ms=MS_POINT - 0.5, mfc="white", mec=INK, mew=1.5, zorder=7)
    ax.plot([0.0], [jc["h_abs"] / 1e3], "D", ms=MS_POINT - 0.5, color=INK, zorder=7, clip_on=False)
    text(ax, (SERVICE_CEILING_RC, h_srv / 1e3), f"service ceiling, {fmt(h_srv / 1e3, 4)} km", direction=20,
         dist=12, fs=FS_SMALL, backing=BAND_FILL)
    text(ax, (0.0, jc["h_abs"] / 1e3), f"absolute ceiling, {fmt(jc['h_abs'] / 1e3, 4)} km", direction=40,
         dist=9, fs=FS_SMALL, backing=BAND_FILL)
    callout(ax, (2.75, (h2 + slope * (2.75 - r2)) / 1e3 + 0.07), "straight line\nthrough two rows",
            at=(2.2, 14.05), ha="left", fs=FS_SMALL, color=SERIES[0], backing=BAND_FILL)
    close_to(float(np.interp(SERVICE_CEILING_RC, rcs[::-1], hs[::-1])), h_srv, 10.0, "service ceiling on the curve")
    close_to(float(rcs[-1]), 0.0, 1e-6, "the curve reaches zero at the absolute ceiling")
    assert abs((h2 + slope * (0.0 - r2)) - jc["h_abs"]) < 60.0, "the straight line lands within 60 m of the ceiling"
    assert h_band < h1, "both top rows lie past the Mach limit (stated on the page)"
    save_figure(fig, "p53-jet-ceiling")


def fig_climb_angle_and_roc():
    """Lesson: with one engine out the steepest climb keeps its speed and loses most of its angle,
    while the fastest climb moves to a lower speed."""
    m, S, CD0, K = _jet()
    TA2, TA1 = available(JET, RHO_SL), available(JET, RHO_SL, n=1)
    Vs = stall_speed_mass(m, S, JET["CLmax"], RHO_SL)
    VM = JET["M_limit"] * float(speed_of_sound(T_SL))
    V = np.linspace(Vs, 280.0, 900)
    c2 = climb_jet(m, S, CD0, K, RHO_SL, TA2, V)
    c1 = climb_jet(m, S, CD0, K, RHO_SL, TA1, V)
    g2 = jet_max_climb_angle(m, S, CD0, K, RHO_SL, TA2)
    g1 = jet_max_climb_angle(m, S, CD0, K, RHO_SL, TA1)
    r2 = jet_max_roc(m, S, CD0, K, RHO_SL, TA2)
    r1 = jet_max_roc(m, S, CD0, K, RHO_SL, TA1)
    fig, axs = data_axes(6.5, 4.0, ncols=2)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.14, top=0.90, wspace=0.32)
    for ax in axs:
        ax.set_xlim(40.0, 280.0)
        ax.set_xticks([50, 100, 150, 200, 250])
        ax.set_xlabel("True airspeed, $V$, m/s")
        ax.axhline(0.0, color=GRAY, lw=LW_THIN, zorder=1.5)
    ax = axs[0]
    ax.set_ylim(-4.0, 8.0); ax.set_yticks([-4, -2, 0, 2, 4, 6, 8])
    ax.set_ylabel("Climb angle, $\\gamma$, deg")
    panel_title(ax, "climb angle")
    stall_band(ax, Vs, label=None)
    mach_band(ax, VM, label=None)
    draw_curve(ax, V, c2["gamma_deg"], required_kw(0), x_valid=VM)
    draw_curve(ax, V, c1["gamma_deg"], required_kw(1), x_valid=VM)
    cond_marks(ax, V, c1["gamma_deg"], 1, at=(80.0, 150.0, 190.0))
    mark_minimum(ax, g2["V"], g2["gamma_deg"], f"two engines: {fmt(g2['gamma_deg'], 3)}°", direction=45, dist=10,
                 fs=FS_SMALL, drop=True, y_to=-4.0)
    mark_minimum(ax, g1["V"], g1["gamma_deg"], f"one engine:\n{fmt(g1['gamma_deg'], 3)}°", cond=1, direction=30,
                 dist=12, fs=FS_SMALL)
    text(ax, (g2["V"], -3.0), f"{fmt(g2['V'], 4)} m/s", direction=0, dist=5, fs=FS_SMALL)
    ax = axs[1]
    ax.set_ylim(-8.0, 20.0); ax.set_yticks([-8, -4, 0, 4, 8, 12, 16, 20])
    ax.set_ylabel("Rate of climb, $R/C$, m/s")
    panel_title(ax, "rate of climb")
    stall_band(ax, Vs, label=None)
    mach_band(ax, VM, label=None)
    draw_curve(ax, V, c2["RC"], required_kw(0), x_valid=VM)
    draw_curve(ax, V, c1["RC"], required_kw(1), x_valid=VM)
    cond_marks(ax, V, c1["RC"], 1, at=(75.0, 170.0, 200.0))
    mark_minimum(ax, r2["V"], r2["RC_max"], f"two engines: {fmt(r2['RC_max'], 4)} m/s\nat {fmt(r2['V'], 4)} m/s",
                 direction=90, dist=6, fs=FS_SMALL, drop=True, y_to=0.0)
    mark_minimum(ax, r1["V"], r1["RC_max"], None, cond=1, drop=True, y_to=0.0)
    text(ax, (140.0, -4.0), f"one engine:\n{fmt(r1['RC_max'], 3)} m/s at\n{fmt(r1['V'], 4)} m/s", fs=FS_SMALL,
         color=COND_TEXT[1])
    close_to(float(V[np.argmax(c2["gamma_deg"])]), g2["V"], 0.4, "two-engine angle peaks at V_TR,min")
    close_to(float(V[np.argmax(c1["gamma_deg"])]), g1["V"], 0.4, "one-engine angle peaks at the same speed")
    close_to(float(np.max(c2["RC"])), r2["RC_max"], 1e-3, "drawn top of the two-engine R/C")
    close_to(float(V[np.argmax(c1["RC"])]), r1["V"], 0.4, "one-engine R/C peaks at a lower speed")
    assert r1["V"] < r2["V"] and g1["gamma_deg"] < 0.3 * g2["gamma_deg"]
    save_figure(fig, "p53-climb-angle-and-roc")


def fig_obstacle_clearance():
    """Lesson: flown faster, at a smaller climb angle, the aircraft arrives lower and meets the ridge face,
    while the slower, steeper climb passes over the top. Paths and heights from the unrounded angles;
    the labels print three figures, as the worked example does."""
    gs, gf = (float(_tr_climb(v)["gamma_deg"]) for v in (V_TR_SLOW, V_TR_FAST))
    hs_ = RIDGE_D * math.tan(math.radians(gs))
    hf_ = RIDGE_D * math.tan(math.radians(gf))
    X1 = 6000.0
    fig, ax = data_axes(6.5, 3.7)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.15, top=0.97)
    ax.set_xlim(0.0, X1); ax.set_ylim(0.0, 600.0)
    ax.set_xticks([0, 1000, 2000, 3000, 4000, 5000, 6000]); ax.set_yticks([0, 100, 200, 300, 400, 500, 600])
    ax.set_xticklabels(["0", "1,000", "2,000", "3,000", "4,000", "5,000", "6,000"])
    ax.set_xlabel("Horizontal distance from the start of the climb, m")
    ax.set_ylabel("Height, m")
    xr = np.linspace(RIDGE_D - 1300.0, X1, 300)
    yr = np.where(xr <= RIDGE_D, RIDGE_H * np.exp(-((xr - RIDGE_D) / 620.0) ** 2),
                  RIDGE_H * np.exp(-((xr - RIDGE_D) / 900.0) ** 2))
    ax.add_patch(opaque(Polygon(np.r_[np.c_[xr, yr], [[X1, 0.0], [xr[0], 0.0]]], closed=True, fc="#D5D5D5",
                                ec=INK, lw=1.2, zorder=3)))
    text(ax, (RIDGE_D + 160.0, 70.0), f"ridge, {fmt(RIDGE_H, 3)} m high", fs=FS_SMALL, backing="#D5D5D5")
    xa = np.array([0.0, X1])
    ax.plot(xa, xa * math.tan(math.radians(gs)), zorder=4, **required_kw(0))
    k = np.linspace(0.0, RIDGE_D, 2000)
    yf = k * math.tan(math.radians(gf))
    ground = np.interp(k, xr, yr, left=0.0)
    hit = float(k[np.argmax((k > RIDGE_D - 1300.0) & (yf <= ground))])
    kk = k[k <= hit]
    ax.plot(kk, kk * math.tan(math.radians(gf)), zorder=4, **required_kw(2))
    cond_marks(ax, kk, kk * math.tan(math.radians(gf)), 2, at=(800.0, 1800.0, 2800.0))
    # where the fast path would be at the ridge top: a thin dotted "would be" line through the ridge
    kw_ = required_kw(2, linewidth=LW_THIN, linestyle=(0, (1.0, 2.2)))
    ax.plot([hit, RIDGE_D], [hit * math.tan(math.radians(gf)), hf_], zorder=4, **kw_)
    ax.plot([RIDGE_D], [hf_], "o", ms=5.5, mfc="white", mec=COND_COLOR[2], mew=1.3, zorder=7)
    callout(ax, (RIDGE_D, hf_), f"{fmt(hf_, 3)} m,\n{fmt(RIDGE_H - hf_, 2)} m too low", at=(RIDGE_D + 500.0, 425.0),
            ha="left", fs=FS_SMALL, color=COND_TEXT[2])   # on white above the ridge: 5.2:1 (on the ridge fill only 3.6:1)
    ax.plot([RIDGE_D], [hs_], "o", ms=MS_POINT, color=INK, zorder=7)
    ax.plot([hit], [hit * math.tan(math.radians(gf))], "X", ms=8.0, color=COND_COLOR[2], mec="white", mew=0.6, zorder=7)
    text(ax, (1500.0, 1500.0 * math.tan(math.radians(gs))),
         f"{fmt(V_TR_SLOW, 2)} m/s: $\\gamma$ = {fmt(gs, 3)}°", direction=125, dist=6, fs=FS_SMALL)
    text(ax, (1000.0, 1000.0 * math.tan(math.radians(gf))),
         f"{fmt(V_TR_FAST, 3)} m/s: $\\gamma$ = {fmt(gf, 3)}°", direction=-40, dist=8, fs=FS_SMALL,
         color=COND_TEXT[2])
    text(ax, (RIDGE_D, hs_), f"{fmt(hs_, 3)} m high at the ridge top,\n{fmt(hs_ - RIDGE_H, 3)} m to spare",
         direction=150, dist=12, fs=FS_SMALL)
    callout(ax, (hit, hit * math.tan(math.radians(gf))), "meets the\nridge face", at=(3150.0, 120.0), ha="center",
            fs=FS_SMALL, color=COND_TEXT[2])
    # the vertical scale is stretched: the caption says "about five times"
    fig.canvas.draw()
    bb = ax.get_window_extent()
    exag = (bb.height / 600.0) / (bb.width / X1)
    assert 4.5 < exag < 5.5, f"vertical exaggeration {exag:.2f} (the caption says about five times)"
    assert hs_ > RIDGE_H > hf_, "the slow climb clears the ridge and the fast one does not"
    assert hit < RIDGE_D, "the failing path stops on the ridge face"
    save_figure(fig, "p53-obstacle-clearance")


def make_all():
    fig_climb_forces()
    fig_velocity_triangle()
    fig_climb_thrust()
    fig_excess_power()
    fig_hodograph()
    fig_why_a_ceiling()
    fig_jet_ceiling()
    fig_climb_angle_and_roc()
    fig_obstacle_clearance()


# ===================================================================== printed values
def values():
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731
    m, S, CD0, K = _jet()
    r("jet-m", fmt(m, 5)); r("jet-S", fmt_dec(S, 1)); r("jet-CD0", fmt_dec(CD0, 3)); r("jet-K", fmt_dec(K, 3))
    r("jet-T0", fmt(JET["T0"], 5)); TA2 = _num(r("jet-TA2", fmt(JET["n"] * JET["T0"], 5)))
    r("jet-mad", fmt_dec(JET["m_ad"], 1))
    W = _num(r("jet-W", fmt(m * G0, 6)))
    r("jet-CLmax", fmt_dec(JET["CLmax"], 1))
    r("jet-Vs", fmt(stall_speed_mass(m, S, JET["CLmax"], RHO_SL), 4))
    # worked example 1: both engines at 135 m/s
    V = V_WE1
    r("we1-V", fmt(V, 3))
    D0 = _num(r("we1-D0", fmt(0.5 * RHO_SL * V ** 2 * S * CD0, 5)))
    Di = _num(r("we1-Di", fmt(2.0 * K * W ** 2 / (RHO_SL * S * V ** 2), 5)))
    D = _num(r("we1-D", fmt(D0 + Di, 5)))
    r("we1-excess-T", fmt(TA2 - D, 5))
    sg = _num(r("we1-sg", fmt_dec((TA2 - D) / W, 5)))
    r("we1-gam", fmt(math.degrees(math.asin(sg)), 3))
    PA = _num(r("we1-PA", fmt(TA2 * V / 1000.0, 4)))
    PR = _num(r("we1-PR", fmt(D * V / 1000.0, 4)))
    r("we1-RC", fmt((PA - PR) * 1000.0 / W, 4))
    r("we1-RC-check", fmt(V * sg, 4))
    r("we1-cos", fmt_dec(math.cos(math.asin(sg)), 4))
    # steepest and fastest climb with both engines
    a1 = _num(r("jet-Vfac", fmt(math.sqrt(2.0 * W / (RHO_SL * S)), 4)))
    b1 = _num(r("jet-Kfac", fmt_dec((K / CD0) ** 0.25, 4)))
    r("jet-Vgam", fmt(a1 * b1, 4))
    TW2 = _num(r("jet-TW2", fmt_dec(TA2 / W, 5)))
    inv = _num(r("jet-invLD", fmt_dec(2.0 * math.sqrt(K * CD0), 5)))
    sg2 = _num(r("jet-sg2", fmt_dec(TW2 - inv, 5)))
    r("jet-gam2", fmt(math.degrees(math.asin(sg2)), 3))
    rc2 = jet_max_roc(m, S, CD0, K, RHO_SL, available(JET, RHO_SL))
    r("jet-RC2", fmt(rc2["RC_max"], 4)); r("jet-Vrc2", fmt(rc2["V"], 4)); r("jet-gam-rc2", fmt(rc2["gamma_deg"], 3))
    _, vmax = jet_speed_bounds(m, S, CD0, K, RHO_SL, available(JET, RHO_SL))
    r("jet-Vmax", fmt(vmax, 4))
    r("jet-VM-sl", fmt(JET["M_limit"] * float(speed_of_sound(T_SL)), 4))
    gam4 = GAMMA_FAMILY
    r("fam-gam", fmt(gam4, 1)); r("fam-lift", fmt(W * math.sin(math.radians(gam4)), 5))
    lo, hi = min_thrust_condition(m, S, CD0, K, RHO_SL)["V"], 400.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if float(thrust_required(m, S, CD0, K, RHO_SL, mid)) + W * math.sin(math.radians(gam4)) < TA2:
            lo = mid
        else:
            hi = mid
    r("fam-v4", fmt(0.5 * (lo + hi), 4))
    # the transport's data
    mt_, St, CD0t, Kt = _tr()
    r("tr-m", fmt(mt_, 5)); r("tr-S", fmt(St, 3)); r("tr-CD0", fmt_dec(CD0t, 3)); r("tr-K", fmt_dec(Kt, 5))
    r("tr-AR", fmt_dec(TR["AR"], 1)); r("tr-e", fmt_dec(TR["e"], 2))
    r("tr-P0", fmt(TR["P0"] / 1e3, 4)); r("tr-eta", fmt_dec(TR["eta"], 2)); r("tr-mad", fmt_dec(TR["m_ad"], 2))
    r("tr-CLmax", fmt_dec(TR["CLmax"], 2))
    Wt = _num(r("tr-W", fmt(mt_ * G0, 6)))
    Kp = _num(fmt_dec(Kt, 5))
    Vst = r("tr-Vs", fmt(stall_speed_mass(mt_, St, TR["CLmax"], RHO_SL), 4))
    # worked example 3: the transport's absolute ceiling, four engines
    CLp = _num(r("tr-CLp", fmt_dec(math.sqrt(3.0 * CD0t / Kp), 3)))
    CDp = _num(r("tr-CDp", fmt_dec(4.0 * CD0t, 3)))
    Vp = _num(r("tr-Vp", fmt(math.sqrt(2.0 * Wt / (RHO_SL * St * CLp)), 4)))
    Tp = _num(r("tr-Tp", fmt(Wt * CDp / CLp, 5)))
    Pmin = _num(r("tr-Pmin", fmt(Tp * Vp / 1000.0, 4)))
    PA4 = _num(r("tr-PA4", fmt(TR["n"] * TR["eta"] * TR["P0"] / 1e3, 4)))
    r("tr-exp", fmt_dec(TR["m_ad"] + 0.5, 2))
    rat = _num(r("tr-ceil-rat", fmt_dec(Pmin / PA4, 4)))
    rhoc = _num(r("tr-rhoc", fmt_dec(RHO_SL * rat ** (1.0 / (TR["m_ad"] + 0.5)), 4)))
    r("tr-habs", fmt(T_SL / 0.0065 * (1.0 - (rhoc / RHO_SL) ** (1.0 / 4.2586)), 4))
    pc4 = prop_absolute_ceiling(mt_, St, CD0t, Kt, TR["n"], TR["P0"], TR["eta"], TR["m_ad"])
    pc3 = prop_absolute_ceiling(mt_, St, CD0t, Kt, N_LEFT, TR["P0"], TR["eta"], TR["m_ad"])
    r("tr-habs-km", fmt(pc4["h_abs"] / 1e3, 3)); r("tr-Pceil", fmt(pc4["P_ceil"] / 1e3, 4))
    r("tr-habs3", fmt(pc3["h_abs"], 4))
    r("tr-Vceil", fmt(min_power_condition(mt_, St, CD0t, Kt, pc4["rho_ceil"])["V"], 4))
    # worked example 2: the jet's ceilings
    Tmin = _num(r("jet-Tmin", fmt(2.0 * W * math.sqrt(K * CD0), 5)))
    ratc = _num(r("jet-ceil-rat", fmt_dec(Tmin / TA2, 4)))
    rhoj = _num(r("jet-rhoc", fmt_dec(RHO_SL * ratc ** (1.0 / JET["m_ad"]), 4)))
    T11, _, rho11 = standard(11000.0)
    T11p = _num(r("atm-T11", fmt_dec(T11, 2))); rho11p = _num(r("atm-rho11", fmt_dec(rho11, 4)))
    jc = jet_absolute_ceiling(m, CD0, K, JET["n"], JET["T0"], JET["m_ad"])
    habs_m = _num(r("jet-habs-m", fmt(11000.0 - R_AIR * T11p / G0 * math.log(rhoj / rho11p), 5)))
    r("jet-habs-km", fmt(jc["h_abs"] / 1e3, 4))
    Vc = min_thrust_condition(m, S, CD0, K, jc["rho_ceil"])["V"]
    ac = float(speed_of_sound(standard(jc["h_abs"])[0]))
    r("jet-Vceil", fmt(Vc, 4)); r("jet-Mceil", fmt_dec(Vc / ac, 2))
    r("jet-hband", fmt(round(_mach_band_altitude(), -2), 5))
    rows = []
    for h in CEIL_ALTS:
        rr = _rc_max_jet(h)
        T_ = standard(h)[0]
        rcv = r(f"tbl-rc-{int(h)}", fmt_dec(rr["RC_max"], 2))
        r(f"tbl-M-{int(h)}", fmt_dec(rr["V"] / float(speed_of_sound(T_)), 2))
        rows.append((h, _num(rcv)))
    h_srv = ceiling_by_bisection(lambda h: _rc_max_jet(h)["RC_max"], SERVICE_CEILING_RC)
    r("jet-hsrv-km", fmt(h_srv / 1e3, 4))
    (h1, rc1), (h2, rc2_) = rows[-2], rows[-1]
    sl = _num(r("jet-slope", fmt((h2 - h1) / (rc1 - rc2_), 4)))
    r("jet-hsrv-lin", fmt(h2 + sl * (rc2_ - SERVICE_CEILING_RC), 5))
    habs_lin = h2 + sl * rc2_
    r("jet-habs-lin", fmt(habs_lin, 5))
    r("jet-habs-diff", fmt(abs(habs_lin - habs_m), 2))
    # one engine out: the jet
    TA1 = JET["T0"]
    TW1 = _num(r("jet-TW1", fmt_dec(TA1 / W, 5)))
    sg1 = _num(r("jet-sg1", fmt_dec(TW1 - inv, 5)))
    gam1 = _num(r("jet-gam1", fmt(math.degrees(math.asin(sg1)), 3)))
    rc1j = jet_max_roc(m, S, CD0, K, RHO_SL, TA1)
    r("jet-RC1", fmt(rc1j["RC_max"], 3)); r("jet-Vrc1", fmt(rc1j["V"], 4))
    r("jet-rc-loss", fmt(100.0 * (1.0 - rc1j["RC_max"] / rc2["RC_max"]), 2))
    tg1 = _num(r("jet-tan1", fmt_dec(math.tan(math.radians(gam1)), 4)))
    r("jet-grad1", fmt_dec(100.0 * tg1, 1))
    r("reg-twin", fmt_dec(GRADIENT_TWIN, 1)); r("reg-four", fmt_dec(GRADIENT_FOUR, 1))
    r("jet-gainH", fmt(JET_GAIN_H, 3))
    r("jet-gainD", fmt(round(JET_GAIN_H / math.tan(math.asin(TA1 / W - 2.0 * math.sqrt(K * CD0))), -1), 4))
    # worked example 4: the transport with three engines against the ridge
    PA3 = _num(r("tr-PA3", fmt(N_LEFT * TR["eta"] * TR["P0"] / 1e3, 4)))
    r("ridge-d", fmt(RIDGE_D, 4)); r("ridge-h", fmt(RIDGE_H, 3))
    r("ridge-tan", fmt_dec(RIDGE_H / RIDGE_D, 5))
    r("ridge-greq", fmt(math.degrees(math.atan(RIDGE_H / RIDGE_D)), 3))
    for tag, Vx in (("fast", V_TR_FAST), ("slow", V_TR_SLOW)):
        r(f"tr-V-{tag}", fmt(Vx, 3 if Vx >= 100 else 2))
        TAx = _num(r(f"tr-TA-{tag}", fmt(PA3 * 1000.0 / Vx, 5)))
        D0x = _num(r(f"tr-D0-{tag}", fmt(0.5 * RHO_SL * Vx ** 2 * St * CD0t, 5)))
        Dix = _num(r(f"tr-Di-{tag}", fmt(2.0 * Kp * Wt ** 2 / (RHO_SL * St * Vx ** 2), 5)))
        Dx = _num(r(f"tr-D-{tag}", fmt(D0x + Dix, 5)))
        sgx = _num(r(f"tr-sg-{tag}", fmt_dec((TAx - Dx) / Wt, 5)))
        r(f"tr-gam-{tag}", fmt(math.degrees(math.asin(sgx)), 3))
        # the height at the ridge from the printed sin(gamma), not from the rounded angle: tan = sin / cos
        tgx = _num(r(f"tr-tan-{tag}", fmt_dec(sgx / math.sqrt(1.0 - sgx ** 2), 5)))
        hx = _num(r(f"tr-h-{tag}", fmt(RIDGE_D * tgx, 3)))
        r(f"tr-margin-{tag}", fmt(abs(hx - RIDGE_H), 2 if abs(hx - RIDGE_H) < 100.0 else 3))
        r(f"tr-RC-{tag}", fmt(Vx * sgx, 3))
    r("tr-slow-ratio", fmt_dec(V_TR_SLOW / _num(Vst), 2))
