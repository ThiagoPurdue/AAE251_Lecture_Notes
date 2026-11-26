"""Figures and values of 5.2 Range and Endurance (notes/chapter-5/range-and-endurance.md).

Worked examples:
  - Example 1, English units: an airplane like the CJ-1 of Anderson (2016), Chapter 6, worked with
    the method of that chapter (the page does not attribute these numbers to him): b = 53.3 ft,
    S = 318 ft^2, W_1 = 19,817 lb, 1,119 gal of fuel at 6.66 lb/gal, thrust specific fuel
    consumption 0.60 1/h, C_D,0 = 0.020, e = 0.81, rho = 0.038 lbm/ft^3 at 22,000 ft,
    g = 32.17 ft/s^2. Maximum range.
  - Example 2, SI: the twin-engine executive jet of vehicles.py at 8,500 m with an assumed thrust
    specific fuel consumption of 0.58 1/h: (a) fuel for a 3,300 km leg at best range, the speed at
    its start; (b) thrust required and throttle setting at the start and at the end of the leg;
    (c) the longest time aloft on the same fuel; (d) the fuel for a 1.5 h hold from the start mass.
  - Example 3, SI: the single-engine general-aviation airplane of vehicles.py (every value its own:
    1,315 kg, 168 kg of fuel, 0.076 g/(s kW), eta = 0.80) at 2,500 m: maximum range and maximum
    endurance on its fuel.
"""
from chapter_5.common import *

PAGE = "p52"

# ===================================================================== data of the examples
CJ1 = dict(b=53.3, S=318.0, W1=19817.0, gal=1119.0, lb_per_gal=6.66,
           CD0=0.020, e=0.81, tsfc_h=0.60, rho_lbm=0.038, g_en=32.17, h_ft=22000.0)
KM_PER_MI = 1.609344                       # km per statute mile (exact, 5,280 ft of 0.3048 m)
JET = EXEC_JET
MACH_TXT = fmt_dec(JET["M_limit"], 2)      # "0.80": every label that names the Mach limit
JET_CASE = dict(h=8500.0, tsfc_h=0.58, R_leg=3300e3, E_hold_h=1.5)   # thrust SFC assumed
GA = GA_AIRPLANE
GA_CASE = dict(h=2500.0)


def _num(s):
    return float(s.replace(",", "").replace("−", "-"))


def _sci(s):
    """The value of a fmt_sci string, "1.9162 \\times 10^{7}" -> 19162000.0."""
    m, _, e = s.partition(" \\times 10^")
    return _num(m) * (10.0 ** int(e.strip("{}")) if e else 1.0)


def _rho(h):
    return float(np.atleast_1d(standard(h)[2])[0])


def _a(h):
    return float(np.atleast_1d(speed_of_sound(standard(h)[0]))[0])


# ===================================================================== shared computations
def jet_case():
    """Example 2: the executive jet at 8,500 m, every quantity unrounded (figures use these)."""
    h = JET_CASE["h"]
    rho, a = _rho(h), _a(h)
    ct = JET_CASE["tsfc_h"] / 3600.0
    jr = jet_best_range_polar(JET["CD0"], JET["K"])
    mf, m2 = jet_fuel_for_range(JET["m"], JET_CASE["R_leg"], JET["S"], rho, ct, jr["CL"], jr["CD"])
    TA = available(JET, rho)
    return dict(h=h, rho=rho, a=a, ct=ct, jr=jr, mf=mf, m2=m2, TA=TA,
                V1=math.sqrt(2.0 * JET["m"] * G0 / (rho * JET["S"] * jr["CL"])),
                V2=math.sqrt(2.0 * m2 * G0 / (rho * JET["S"] * jr["CL"])),
                T1=jet_best_range_thrust(JET["m"], JET["CD0"], JET["K"]),
                T2=jet_best_range_thrust(m2, JET["CD0"], JET["K"]))


def mach_limit_altitude(m):
    """Altitude (m) at which the best-range speed of the executive jet at mass m reaches its Mach
    limit (bisection on the standard atmosphere)."""
    CL = jet_best_range_polar(JET["CD0"], JET["K"])["CL"]
    f = lambda h: math.sqrt(2.0 * m * G0 / (_rho(h) * JET["S"] * CL)) - JET["M_limit"] * _a(h)  # noqa: E731
    lo, hi = 0.0, 20000.0
    assert f(lo) < 0.0 < f(hi)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if f(mid) < 0.0 else (lo, mid)
    return 0.5 * (lo + hi)


def jet_limits():
    """Where the executive jet can hold its best-range condition, at the start mass of example 2."""
    th = jet_best_range_density_limit(JET["m"], JET["CD0"], JET["K"], JET["n"], JET["T0"], JET["m_ad"])
    ceil = jet_absolute_ceiling(JET["m"], JET["CD0"], JET["K"], JET["n"], JET["T0"], JET["m_ad"])
    return dict(rho_thrust=th["rho"], h_thrust=th["h"], h_mach=mach_limit_altitude(JET["m"]),
                rho_ceil=ceil["rho_ceil"], h_ceil=ceil["h_abs"])


# ===================================================================== figures
# Markers of the three ratios, the same in the ratio figure and the speed figure:
# C_L^(1/2)/C_D (jet range) a blue square, C_L/C_D (jet endurance, propeller range) a black circle,
# C_L^(3/2)/C_D (propeller endurance) a vermilion triangle (the chapter's filled diamond marks a limit).
RATIO_LOOK = {
    "half": dict(color=COND_COLOR[1], text=COND_TEXT[1], marker="s", ls=(0, (6.5, 3.0))),
    "one": dict(color=COND_COLOR[0], text=COND_TEXT[0], marker="o", ls="-"),
    "three": dict(color=COND_COLOR[2], text=COND_TEXT[2], marker="^", ls=(0, (0.1, 2.4))),
}


def fig_aero_ratios():
    """Lesson: each goal has its own best lift coefficient, a factor of sqrt(3) apart.
    Computed for the executive jet's polar (C_D,0 = 0.015, K = 0.050)."""
    CD0, K = JET["CD0"], JET["K"]
    CL = np.linspace(0.02, 1.45, 1431)
    CD = polar_CD(CL, CD0, K)
    curves = {"half": np.sqrt(CL) / CD, "one": CL / CD, "three": CL ** 1.5 / CD}
    peaks = {"half": math.sqrt(CD0 / (3.0 * K)), "one": math.sqrt(CD0 / K), "three": math.sqrt(3.0 * CD0 / K)}
    names = {"half": "$C_L^{1/2}/C_D$\njet range",
             "one": "$C_L/C_D$\njet endurance,\npropeller range",
             "three": "$C_L^{3/2}/C_D$\npropeller\nendurance"}

    fig, ax = data_axes(6.5, 4.2)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.14, top=0.97)
    ax.set_xlim(0.0, 1.5); ax.set_ylim(0.0, 1.5)
    ax.set_xticks([0.0, 0.3, 0.6, 0.9, 1.2, 1.5]); ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.spines["left"].set_bounds(0.0, 1.0)
    ax.set_xlabel("Lift coefficient, $C_L$")
    ax.set_ylabel("Ratio divided by its maximum")
    drawn = {}
    for k in ("half", "one", "three"):
        lk = RATIO_LOOK[k]
        y = curves[k] / curves[k].max()
        drawn[k] = y
        kw = dict(color=lk["color"], linestyle=lk["ls"], linewidth=LW_CURVE)
        if k == "three":
            kw["dash_capstyle"] = "round"
        ax.plot(CL, y, zorder=4, **kw)
        ax.plot([peaks[k], peaks[k]], [0.0, 1.0], color=GRAY, lw=LW_THIN, linestyle=DASH_CONSTRUCTION, zorder=2)
        ax.plot([peaks[k]], [1.0], lk["marker"], ms=MS_POINT, color=lk["color"], zorder=7)
        text(ax, (peaks[k], 0.09), fmt(peaks[k], 3), direction=0, dist=4, fs=FS_SMALL, color=lk["text"])
    text(ax, (peaks["half"], 1.0), names["half"], direction=90, dist=8, fs=FS_LABEL, color=RATIO_LOOK["half"]["text"],
         ha="right", offset=(-2, 0))
    text(ax, (peaks["one"], 1.0), names["one"], direction=90, dist=8, fs=FS_LABEL, color=INK, ha="center")
    text(ax, (peaks["three"], 1.0), names["three"], direction=90, dist=8, fs=FS_LABEL,
         color=RATIO_LOOK["three"]["text"], ha="left", offset=(2, 0))
    for k in drawn:                                           # the drawn peaks sit at the derived C_L
        close_to(float(CL[np.argmax(drawn[k])]), peaks[k], 0.002, f"drawn peak of the {k} ratio")
    close_to(peaks["one"] / peaks["half"], math.sqrt(3.0), 1e-12, "sqrt(3) between neighbors")
    close_to(float(CL[np.argmax(drawn["three"])] / CL[np.argmax(drawn["one"])]), math.sqrt(3.0), 0.01,
             "drawn peaks a factor sqrt(3) apart")
    save_figure(fig, "p52-aero-ratios")


def fig_speed_order():
    """Lesson: the three best speeds come in a fixed order, each a factor 3^(1/4) = 1.316 from the next.
    Drawn on a logarithmic scale, so equal factors are equal lengths."""
    step = 0.25 * math.log(3.0)
    X = lambda r: math.log(r) / step                       # noqa: E731  one unit = a factor 3^(1/4)
    fig, ax = canvas(6.5, xlim=(-1.75, 1.75), ylim=(-0.95, 0.65))
    lo, hi = 0.66, 1.56
    kind_arrow(ax, (X(lo), 0.0), (X(hi), 0.0), "axis", None)
    text(ax, (0.0, 0.50), "true airspeed divided by $V_{T_R,\\min}$, on a logarithmic scale", fs=FS_LABEL)
    pts = [(3.0 ** -0.25, "three", "propeller\nbest endurance", "maximum\n$C_L^{3/2}/C_D$"),
           (1.0, "one", "jet best endurance,\npropeller best range", "maximum\n$C_L/C_D$"),
           (3.0 ** 0.25, "half", "jet\nbest range", "maximum\n$C_L^{1/2}/C_D$")]
    xs = []
    for r, k, name, ratio in pts:
        lk = RATIO_LOOK[k]
        x = X(r)
        mk = ax.plot([x], [0.0], lk["marker"], ms=MS_POINT + 1, color=lk["color"], zorder=7)[0]
        xs.append(float(mk.get_xdata()[0]))
        text(ax, (x, 0.0), name, direction=90, dist=10, fs=FS_LABEL, color=lk["text"])
        text(ax, (x, 0.0), fmt(r, 3 if r < 1.0 else 4), direction=-90, dist=9, fs=FS_LABEL, color=lk["text"])
        text(ax, (x, -0.17), ratio, direction=-90, dist=9, fs=FS_LABEL, color=lk["text"])
    for x0, x1 in ((xs[0], xs[1]), (xs[1], xs[2])):
        dimension(ax, (x0, -0.72), (x1, -0.72), None, ticks=True, extension=False)
        text(ax, (0.5 * (x0 + x1), -0.72), f"$\\times$ {fmt(3.0 ** 0.25, 4)}", direction=90, dist=4, fs=FS_LABEL)
    # the drawn markers: equal steps, each the logarithm of 3^(1/4)
    close_to(xs[1] - xs[0], xs[2] - xs[1], 1e-12, "the two drawn steps are equal")
    close_to(math.exp((xs[2] - xs[1]) * step), 3.0 ** 0.25, 1e-12, "each drawn step is a factor 3^(1/4)")
    close_to(math.exp((xs[2] - xs[0]) * step), math.sqrt(3.0), 1e-12, "jet range is sqrt(3) faster than propeller endurance")
    trim_canvas(fig)
    save_figure(fig, "p52-speed-order")


def fig_jet_vs_prop_curves():
    """Lesson: on thrust required for a jet and power required for a propeller aircraft, the lowest
    point is best endurance and the tangent from the origin is best range.
    Panel 1: the executive jet at 8,500 m at the start mass of example 2 (Mach band from 0.80).
    Panel 2: the general-aviation airplane at 2,500 m with full tanks (example 3)."""
    fig, axs = data_axes(6.5, 4.0, ncols=2)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.14, top=0.90, wspace=0.32)

    # Panel 1: jet, thrust required
    ax = axs[0]
    h, rho, a = JET_CASE["h"], _rho(JET_CASE["h"]), _a(JET_CASE["h"])
    m, S, CD0, K = JET["m"], JET["S"], JET["CD0"], JET["K"]
    Vs = stall_speed_mass(m, S, JET["CLmax"], rho)
    V_lim = JET["M_limit"] * a
    ax.set_xlim(0.0, 300.0); ax.set_ylim(0.0, 40.0)
    ax.set_xticks([0, 100, 200, 300]); ax.set_yticks([0, 10, 20, 30, 40])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Thrust required, $T_R$, kN")
    panel_title(ax, f"executive jet, {fmt(h, 4)} m")
    stall_band(ax, Vs, y_label=31.0)
    mach_band(ax, V_lim, label=f"past Mach {MACH_TXT}:\nwave drag", y_label=10.0)
    V = np.linspace(Vs, 300.0, 1200)
    TR = thrust_required(m, S, CD0, K, rho, V) / 1e3
    draw_curve(ax, V, TR, required_kw(0), x_valid=V_lim)
    i_min = int(np.argmin(TR)); i_tan = int(np.argmin(TR / V))
    mark_minimum(ax, V[i_min], TR[i_min])
    callout(ax, (V[i_min], TR[i_min]), "best\nendurance,\nmax $C_L/C_D$", at=(104.0, 34.0), ha="left", fs=FS_LABEL)
    tangent_from_origin(ax, V[i_tan], TR[i_tan], 232.0, None, origin_label=None)
    callout(ax, (V[i_tan], TR[i_tan]), "best range,\nmax $C_L^{1/2}/C_D$", at=(106.0, 4.5), ha="left", fs=FS_LABEL)
    mt = min_thrust_condition(m, S, CD0, K, rho)
    jr = jet_best_range_polar(CD0, K)
    V_br = math.sqrt(2.0 * m * G0 / (rho * S * jr["CL"]))
    close_to(float(V[i_min]), mt["V"], 0.3, "drawn minimum at V_TR,min")
    close_to(float(V[i_tan]), V_br, 0.3, "drawn tangent point at the best-range speed")
    close_to(float(V[i_tan] / V[i_min]), 3.0 ** 0.25, 0.005, "drawn tangent point 3^(1/4) faster")
    assert V_br < V_lim, "the best-range point lies inside the polar's Mach limit"

    # Panel 2: propeller aircraft, power required
    ax = axs[1]
    h2, rho2 = GA_CASE["h"], _rho(GA_CASE["h"])
    m, S, CD0, K = GA["m"], GA["S"], GA["CD0"], GA["K"]
    Vs2 = stall_speed_mass(m, S, GA["CLmax"], rho2)
    ax.set_xlim(0.0, 90.0); ax.set_ylim(0.0, 150.0)
    ax.set_xticks([0, 30, 60, 90]); ax.set_yticks([0, 30, 60, 90, 120, 150])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Power required, $P_R$, kW")
    panel_title(ax, f"general-aviation airplane, {fmt(h2, 4)} m")
    stall_band(ax, Vs2, y_label=70.0)
    V = np.linspace(Vs2, 90.0, 1200)
    PR = power_required(m, S, CD0, K, rho2, V) / 1e3
    ax.plot(V, PR, zorder=4, **required_kw(0))
    j_min = int(np.argmin(PR)); j_tan = int(np.argmin(PR / V))
    mark_minimum(ax, V[j_min], PR[j_min])
    callout(ax, (V[j_min], PR[j_min]), "best endurance,\nmax $C_L^{3/2}/C_D$", at=(29.0, 128.0), ha="left",
            fs=FS_LABEL)
    tangent_from_origin(ax, V[j_tan], PR[j_tan], 78.0, None, origin_label=None)
    callout(ax, (V[j_tan], PR[j_tan]), "best range,\nmax $C_L/C_D$", at=(52.0, 14.0), ha="left", fs=FS_LABEL)
    mp = min_power_condition(m, S, CD0, K, rho2)
    mt2 = min_thrust_condition(m, S, CD0, K, rho2)
    close_to(float(V[j_min]), mp["V"], 0.1, "drawn minimum at V_PR,min")
    close_to(float(V[j_tan]), mt2["V"], 0.1, "drawn tangent point at V_TR,min")
    close_to(float(PR[j_tan] / V[j_tan]) * 1e3, mt2["T_min"], 2e-3 * mt2["T_min"], "tangent slope is T_R,min")
    assert mp["V"] > Vs2, "best endurance lies above the stall speed"
    save_figure(fig, "p52-jet-vs-prop-curves")


def fig_weight_burn():
    """Lesson: at constant altitude and lift coefficient the speed and the thrust required both fall as
    the fuel burns, so the pilot throttles back. Example 2: the executive jet, 3,300 km at 8,500 m."""
    c = jet_case()
    m1, m2 = JET["m"], c["m2"]
    ms = np.linspace(m1, m2, 400)
    x = np.array([jet_range(m1, mm, JET["S"], c["rho"], c["ct"], c["jr"]["CL"], c["jr"]["CD"]) for mm in ms]) / 1e3
    V = np.sqrt(2.0 * ms * G0 / (c["rho"] * JET["S"] * c["jr"]["CL"]))
    T = ms * G0 / c["jr"]["LD"] / 1e3
    TA = c["TA"] / 1e3
    R_km = JET_CASE["R_leg"] / 1e3

    fig, axs = data_axes(6.5, 3.9, ncols=2)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.15, top=0.90, wspace=0.34)
    ax = axs[0]
    ax.set_xlim(0, 3500); ax.set_ylim(0, 250)
    ax.set_xticks([0, 1000, 2000, 3000]); ax.set_yticks([0, 50, 100, 150, 200, 250])
    ax.set_xlabel("Distance flown, km"); ax.set_ylabel("True airspeed, $V$, m/s")
    panel_title(ax, "speed at best range")
    ax.plot(x, V, zorder=4, **required_kw(0))
    ax.plot([x[0], x[-1]], [V[0], V[-1]], "o", ms=5.5, color=INK, zorder=7, linestyle="none", clip_on=False)
    text(ax, (x[0], V[0]), f"{fmt(c['V1'], 4)} m/s", direction=-90, dist=12, fs=FS_SMALL, ha="left", offset=(5, 0))
    text(ax, (x[-1], V[-1]), f"{fmt(c['V2'], 4)} m/s", direction=-90, dist=12, fs=FS_SMALL, ha="right")

    ax = axs[1]
    ax.set_xlim(0, 3500); ax.set_ylim(0, 40)
    ax.set_xticks([0, 1000, 2000, 3000]); ax.set_yticks([0, 10, 20, 30, 40])
    ax.set_xlabel("Distance flown, km"); ax.set_ylabel("Thrust, kN")
    panel_title(ax, "thrust and throttle")
    ax.plot(x, T, zorder=4, **required_kw(0))
    ax.plot([0, R_km], [TA, TA], zorder=4, **available_kw(0))
    ax.plot([x[0], x[-1]], [T[0], T[-1]], "o", ms=5.5, color=INK, zorder=7, linestyle="none", clip_on=False)
    text(ax, (0.5 * R_km, TA), f"full throttle, $T_A$ = {fmt(TA, 4)} kN", direction=90, dist=5, fs=FS_SMALL)
    text(ax, (0.5 * R_km, float(np.interp(0.5 * R_km, x, T))), "required, $T_R$", direction=90, dist=14, fs=FS_SMALL)
    text(ax, (x[0], T[0]), f"{fmt(c['T1'] / 1e3, 4)} kN\n$\\delta_t$ = {fmt(c['T1'] / c['TA'], 4)}",
         direction=-90, dist=12, fs=FS_SMALL, ha="left", offset=(5, 0))
    text(ax, (x[-1], T[-1]), f"{fmt(c['T2'] / 1e3, 4)} kN\n$\\delta_t$ = {fmt(c['T2'] / c['TA'], 4)}",
         direction=-90, dist=12, fs=FS_SMALL, ha="right")
    # the drawn curves: the leg ends at the stated distance; speed falls as sqrt(m), thrust as m
    close_to(float(x[-1]), R_km, 1e-6, "the curve ends at the leg length")
    close_to(float(V[-1] / V[0]), math.sqrt(m2 / m1), 1e-12, "speed falls as the square root of the mass")
    close_to(float(T[-1] / T[0]), m2 / m1, 1e-12, "thrust falls in proportion to the mass")
    assert np.all(np.diff(V) < 0.0) and np.all(np.diff(T) < 0.0), "both fall all along the leg"
    assert float(T.max()) < TA, "the best-range thrust stays below full throttle"
    save_figure(fig, "p52-weight-burn")


def fig_altitude_range():
    """Lesson: jet range grows with altitude as (rho_0/rho)^(1/2), until the best-range speed reaches the
    Mach limit and, higher, until full throttle no longer gives the best-range thrust; propeller range
    and jet endurance do not change, and propeller endurance falls as (rho/rho_0)^(1/2).
    Ratios to the sea-level value at the same masses; limits of the executive jet at the start mass.
    The three lines are three quantities, not three conditions: all black, told apart by line style
    (thick solid, dash-dot, dotted) and named on the figure."""
    lim = jet_limits()
    h_top = 14.0                                             # km: both jet limits, nothing far past them
    hs = np.linspace(0.0, lim["h_thrust"], 600)
    rho = np.array([_rho(h) for h in hs])
    jet_R = np.sqrt(RHO_SL / rho)
    hk = hs / 1e3
    hk_all = np.linspace(0.0, h_top, 561)
    rho_all = np.array([_rho(1e3 * h) for h in hk_all])
    h_mach, h_thr = lim["h_mach"] / 1e3, lim["h_thrust"] / 1e3
    assert h_thr < h_top, "the thrust limit lies inside the plotted altitudes"

    fig, ax = data_axes(6.5, 4.3)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.13, top=0.97)
    ax.set_xlim(0.0, h_top); ax.set_ylim(0.0, 2.75)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14]); ax.set_yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
    ax.set_xlabel("Cruise altitude, $h$, km")
    ax.set_ylabel("Range or endurance over its sea-level value")
    mach_band(ax, h_mach, label=None)
    text(ax, (10.25, 2.68), f"jet past\nMach {MACH_TXT}:\nwave drag", fs=FS_SMALL, backing=BAND_FILL,
         ha="left", va="top", linespacing=1.15)
    draw_curve(ax, hk, jet_R, required_kw(0), x_valid=h_mach)
    y_m = float(np.interp(h_mach, hk, jet_R))
    mark_limit(ax, h_mach, y_m)
    callout(ax, (h_mach, y_m), f"jet reaches\nMach {MACH_TXT} at\n{fmt(h_mach, 3)} km", at=(8.9, 2.25), ha="right",
            fs=FS_SMALL)
    ax.plot([h_thr, h_thr], [0.0, float(jet_R[-1])], color=INK, lw=LW_THIN, linestyle=DASH_CONSTRUCTION, zorder=3)
    # at the foot of its line, below the propeller endurance curve, so it is not read across the band label
    text(ax, (h_thr, 0.06), f"thrust limit,\n{fmt(h_thr, 3)} km", fs=FS_SMALL, backing=BAND_FILL,
         ha="right", va="bottom", offset=(-3, 0), linespacing=1.15)
    callout(ax, (5.5, float(np.interp(5.5, hk, jet_R))), "jet range, √($\\rho_0/\\rho$)", at=(0.4, 1.85),
            ha="left", fs=FS_LABEL)
    flat = ax.plot([0.0, h_top], [1.0, 1.0], color=INK, linestyle=(0, (7.0, 2.5, 1.5, 2.5)), linewidth=1.6,
                   zorder=4)[0]
    text(ax, (10.35, 1.0), "jet endurance,\npropeller range:\nno change", direction=90, dist=7, fs=FS_SMALL,
         backing=BAND_FILL, ha="left")
    pe = np.sqrt(rho_all / RHO_SL)
    dots = ax.plot(hk_all, pe, color=INK, linestyle=(0, (0.1, 2.6)), linewidth=2.2, dash_capstyle="round",
                   zorder=4)[0]
    text(ax, (0.6, 0.3), "propeller endurance, √($\\rho/\\rho_0$)", fs=FS_LABEL, ha="left")
    # asserts on the drawn curves
    on_curve(hk, jet_R, 10.0, math.sqrt(RHO_SL / _rho(10000.0)), 1e-3, "jet curve is (rho_0/rho)^(1/2)")
    on_curve(hk_all, pe, 6.0, math.sqrt(_rho(6000.0) / RHO_SL), 1e-3, "propeller endurance is (rho/rho_0)^(1/2)")
    close_to(float(jet_R[0]), 1.0, 1e-12, "the jet curve starts at 1 at sea level")
    close_to(float(dots.get_ydata()[0]), 1.0, 1e-12, "the propeller endurance curve starts at 1 at sea level")
    assert np.allclose(flat.get_ydata(), 1.0), "the no-change line is flat at 1"
    close_to(float(hk[-1]), h_thr, 1e-9, "the jet curve stops at the thrust limit")
    assert h_mach < h_thr < lim["h_ceil"] / 1e3, "Mach limit, then thrust limit, both below the absolute ceiling"
    save_figure(fig, "p52-altitude-range")


def make_all():
    fig_aero_ratios()
    fig_speed_order()
    fig_jet_vs_prop_curves()
    fig_weight_burn()
    fig_altitude_range()


# ===================================================================== printed values
def values():
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731
    # General results
    r("ratio-lo", fmt(3.0 ** (-0.25), 3)); r("ratio-hi", fmt(3.0 ** 0.25, 4))
    r("pct-faster", fmt(100.0 * (3.0 ** 0.25 - 1.0), 3))
    r("sqrt3", fmt(math.sqrt(3.0), 4))
    r("thrust-factor", fmt(2.0 / math.sqrt(3.0), 4))

    # Example 1: business jet in English units
    r("cj-h-ft", fmt(CJ1["h_ft"], 5)); r("cj-rho", fmt_dec(CJ1["rho_lbm"], 3))
    r("cj-b", fmt_dec(CJ1["b"], 1)); r("cj-S", fmt(CJ1["S"], 3))
    r("cj-W1", fmt(CJ1["W1"], 5)); r("cj-gal", fmt(CJ1["gal"], 4)); r("cj-lbgal", fmt_dec(CJ1["lb_per_gal"], 2))
    r("cj-CD0", fmt_dec(CJ1["CD0"], 3)); r("cj-e", fmt_dec(CJ1["e"], 2)); r("cj-tsfc", fmt_dec(CJ1["tsfc_h"], 2))
    r("cj-g", fmt_dec(CJ1["g_en"], 2))
    Wf = r("cj-Wf", fmt(CJ1["gal"] * CJ1["lb_per_gal"], 5))
    W2 = r("cj-W2", fmt(CJ1["W1"] - _num(Wf), 6))
    AR = r("cj-AR", fmt(CJ1["b"] ** 2 / CJ1["S"], 5))
    K_cj = r("cj-K", fmt(1.0 / (math.pi * CJ1["e"] * _num(AR)), 5))
    CL_cj = r("cj-CL", fmt(math.sqrt(CJ1["CD0"] / (3.0 * _num(K_cj))), 5))
    CD_cj = r("cj-CD", fmt((4.0 / 3.0) * CJ1["CD0"], 5))
    r("cj-ct", fmt_sci(CJ1["tsfc_h"] / 3600.0, 5))
    fac1 = r("cj-fac1", fmt(2.0 / (CJ1["tsfc_h"] / 3600.0), 5))
    fac2 = r("cj-fac2", fmt(math.sqrt(2.0 * CJ1["g_en"] / (CJ1["rho_lbm"] * CJ1["S"])), 5))
    fac3 = r("cj-fac3", fmt(math.sqrt(_num(CL_cj)) / _num(CD_cj), 5))
    sm1 = r("cj-sm1", fmt(math.sqrt(CJ1["W1"]), 6))
    sm2 = r("cj-sm2", fmt(math.sqrt(_num(W2)), 6))
    dsm = r("cj-dsm", fmt(_num(sm1) - _num(sm2), 5))
    R_ft = r("cj-R-ft", fmt_sci(_num(fac1) * _num(fac2) * _num(fac3) * _num(dsm), 5))
    R_ft_p = _sci(R_ft)                                       # the printed 1.9162 x 10^7 ft
    r("cj-R-mi", fmt(R_ft_p / FT_PER_MI, 4))
    r("cj-R-km", fmt(R_ft_p * 0.3048 / 1e3, 4))               # from the printed feet (0.3048 m exact)

    # Example 2: the executive jet at 8,500 m
    c = jet_case()
    r("jet-m1", fmt(JET["m"], 5)); r("jet-S", fmt_dec(JET["S"], 1))
    r("jet-CD0", fmt_dec(JET["CD0"], 3)); r("jet-K", fmt_dec(JET["K"], 3))
    r("jet-n", str(JET["n"])); r("jet-T0", fmt(JET["T0"], 5)); r("jet-mad", fmt_dec(JET["m_ad"], 1))
    r("jet-T0-total", fmt(JET["n"] * JET["T0"], 5))
    r("jet-h", fmt(c["h"], 4)); rho_s = r("jet-rho", fmt(c["rho"], 5)); a_s = r("jet-a", fmt(c["a"], 5))
    r("jet-tsfc", fmt_dec(JET_CASE["tsfc_h"], 2)); r("jet-R-km", fmt(JET_CASE["R_leg"] / 1e3, 4))
    ct_p = _sci(r("jet-ct", fmt_sci(c["ct"], 6)))               # the printed c_t, used downstream
    r("jet-Mlim", fmt_dec(JET["M_limit"], 2))
    CLr = r("jet-CLr", fmt(math.sqrt(JET["CD0"] / (3.0 * JET["K"])), 5))
    CDr = r("jet-CDr", fmt_dec((4.0 / 3.0) * JET["CD0"], 4))
    rat = r("jet-rat", fmt(math.sqrt(_num(CLr)) / _num(CDr), 5))
    sq = r("jet-sq", fmt(math.sqrt(2.0 * G0 / (_num(rho_s) * JET["S"])), 5))
    A = r("jet-A", fmt((2.0 / ct_p) * _num(sq) * _num(rat), 6))
    sm1 = r("jet-sm1", fmt(math.sqrt(JET["m"]), 6))
    sm2 = r("jet-sm2", fmt(_num(sm1) - JET_CASE["R_leg"] / _num(A), 6))
    m2 = r("jet-m2", fmt(_num(sm2) ** 2, 5))
    r("jet-mf", fmt(JET["m"] - _num(m2), 4))
    V1 = r("jet-V1", fmt(math.sqrt(2.0 * JET["m"] * G0 / (_num(rho_s) * JET["S"] * _num(CLr))), 4))
    r("jet-M1", fmt(_num(V1) / _num(a_s), 3))
    V2 = r("jet-V2", fmt(_num(V1) * math.sqrt(_num(m2) / JET["m"]), 4))
    # (b) thrust and throttle
    sqK = r("jet-sqK", fmt(math.sqrt(JET["K"] * JET["CD0"] / 3.0), 6))
    W1 = r("jet-W1", fmt(JET["m"] * G0, 6))
    T1 = r("jet-T1", fmt(4.0 * _num(W1) * _num(sqK), 5))
    rr = r("jet-rr", fmt(_num(rho_s) / RHO_SL, 5))
    lapse = r("jet-lapse", fmt(_num(rr) ** JET["m_ad"], 5))
    TA = r("jet-TA", fmt(JET["n"] * JET["T0"] * _num(lapse), 5))
    r("jet-dt1", fmt(_num(T1) / _num(TA), 4))
    T2 = r("jet-T2", fmt(4.0 * _num(m2) * G0 * _num(sqK), 5))
    r("jet-dt2", fmt(_num(T2) / _num(TA), 4))
    # (c) longest hold on the same fuel
    sqKC = r("jet-sqKC", fmt(math.sqrt(JET["K"] * JET["CD0"]), 6))
    LDm = r("jet-LDm", fmt(1.0 / (2.0 * _num(sqKC)), 6))
    ln_j = r("jet-ln", fmt(math.log(JET["m"] / _num(m2)), 6))
    E_s = r("jet-E-s", fmt((1.0 / ct_p) * _num(LDm) * _num(ln_j), 5))
    r("jet-E-h", fmt(_num(E_s) / 3600.0, 4))
    Vavg = r("jet-Vavg", fmt(0.5 * (_num(V1) + _num(V2)), 4))
    r("jet-tleg", fmt(JET_CASE["R_leg"] / _num(Vavg) / 3600.0, 3))
    # (d) fuel for a 1.5 h hold
    r("jet-Eh", fmt(JET_CASE["E_hold_h"], 2)); Ehs = r("jet-Ehs", fmt(JET_CASE["E_hold_h"] * 3600.0, 4))
    ex = r("jet-exarg", fmt(ct_p * _num(Ehs) / _num(LDm), 5))
    ef = r("jet-exp", fmt(math.exp(-_num(ex)), 6))
    mfE = r("jet-mfE", fmt(JET["m"] * (1.0 - _num(ef)), 5))
    assert 0.29 < _num(mfE) / (JET["m"] - _num(m2)) < 0.36, "the page says: about a third of the leg's fuel"

    # Where the jet can hold its best-range condition (start mass of example 2)
    lim = jet_limits()
    Tr = r("lim-ratio", fmt(_num(T1) / (JET["n"] * JET["T0"]), 5))
    r("lim-rho", fmt(RHO_SL * _num(Tr) ** (1.0 / JET["m_ad"]), 4))
    r("lim-h-km", fmt(lim["h_thrust"] / 1e3, 3))
    r("lim-mach-km", fmt(lim["h_mach"] / 1e3, 3))
    r("lim-ceil-rho", fmt(lim["rho_ceil"], 3)); r("lim-ceil-km", fmt(lim["h_ceil"] / 1e3, 4))

    # Example 3: the general-aviation airplane at 2,500 m
    rho_g = _rho(GA_CASE["h"])
    r("ga-m1", fmt(GA["m"], 4)); r("ga-mf", fmt(GA["fuel"], 3))
    m2_g = r("ga-m2", fmt(GA["m"] - GA["fuel"], 4))
    r("ga-S", fmt_dec(GA["S"], 1)); r("ga-CD0", fmt_dec(GA["CD0"], 3)); r("ga-K", fmt_dec(GA["K"], 3))
    r("ga-eta", fmt_dec(GA["eta"], 2)); r("ga-psfc", fmt_dec(GA["c_g"], 3))
    r("ga-h", fmt(GA_CASE["h"], 4)); rho_gs = r("ga-rho", fmt(rho_g, 6))
    c_p = _sci(r("ga-c", fmt_sci(power_sfc_per_m(GA), 5)))
    etac = r("ga-etac", fmt(GA["eta"] / c_p, 7))
    CLr_g = r("ga-CLr", fmt(math.sqrt(GA["CD0"] / GA["K"]), 5))
    CDr_g = r("ga-CDr", fmt_dec(2.0 * GA["CD0"], 3))
    LDr_g = r("ga-LDr", fmt(_num(CLr_g) / _num(CDr_g), 5))
    ln_g = r("ga-ln", fmt(math.log(GA["m"] / _num(m2_g)), 6))
    R_gm = r("ga-R-m", fmt(_num(etac) * _num(LDr_g) * _num(ln_g), 6))
    r("ga-R-km", fmt(_num(R_gm) / 1000.0, 4))
    CLe_g = r("ga-CLe", fmt(math.sqrt(3.0 * GA["CD0"] / GA["K"]), 6))
    CDe_g = r("ga-CDe", fmt_dec(4.0 * GA["CD0"], 3))
    rat_eg = r("ga-rat-e", fmt(_num(CLe_g) ** 1.5 / _num(CDe_g), 5))
    sq_eg = r("ga-sq-e", fmt(math.sqrt(2.0 * _num(rho_gs) * GA["S"] / G0), 6))
    inv2 = r("ga-inv2", fmt(1.0 / math.sqrt(_num(m2_g)), 7))
    inv1 = r("ga-inv1", fmt(1.0 / math.sqrt(GA["m"]), 7))
    dinv = r("ga-dinv", fmt(_num(inv2) - _num(inv1), 6))
    E_gs = r("ga-E-s", fmt(_num(etac) * _num(sq_eg) * _num(rat_eg) * _num(dinv), 5))
    r("ga-E-h", fmt(_num(E_gs) / 3600.0, 4))
