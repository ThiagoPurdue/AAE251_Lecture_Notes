"""Figures and values of 5.1 Thrust and Power (notes/chapter-5/thrust-and-power.md).

The two aircraft come from vehicles.py:
  - EXEC_JET, the twin-engine executive jet (pages 5.1 to 5.3);
  - GA_AIRPLANE, the single-engine general-aviation airplane with its lift curve and pitching-moment
    line (sign convention of vehicles.py: nose-up moment positive, elevator positive trailing edge
    down, so C_M,de < 0 and trim in cruise is trailing edge up).
Scenario values chosen here: the airplane at 70 m/s and at 5 deg at sea level (the examples' own
cases); the jet at 9,500 m and the airplane at 6,500 m for the effect of altitude; the jet's thrust
available at 0, 1,000, 5,000 and 10,000 m against its minimum thrust required.

Every figure states its lesson in a comment before it is drawn; every number printed on the page
is recorded by values(). The force figure takes the look of looks.level_forces (thrust along the
body axis at the angle of attack, as on page 5.3).
"""
import math

from matplotlib import patheffects

from chapter_5.common import *

PAGE = "p51"

J, A = EXEC_JET, GA_AIRPLANE
V_SPEED_CASE = 70.0          # m/s, the airplane at a given speed, sea level
ALPHA_CASE = 5.0             # deg, the airplane at a given angle of attack, sea level
CL_TOO_HIGH = 2.8            # a lift coefficient asked for at some slow speed (the feasibility question)
H_JET = 9500.0               # m, the jet's second altitude
H_PROP = 6500.0              # m, the airplane's second altitude
H_TABLE = (0.0, 1000.0, 5000.0, 10000.0)   # m, thrust available against the minimum thrust required
V_SLOW, V_FAST = 80.0, 230.0  # m/s, two points on the jet's thrust-required curve
V_PAIR_PROP = (40.0, 80.0)   # m/s, speed doubled: the propeller's thrust halves
V_PAIR_JET = (100.0, 200.0)  # m/s, speed doubled: the jet's power doubles
GAMMA_SHOWN, ALPHA_SHOWN = 15.0, 10.0   # deg, the angles as drawn in p51-flight-angles (exaggerated)

# force figure: ALPHA_DRAWN, LD_DRAWN, W_DRAWN, AC_LENGTH and SCALE_IN_PER_UNIT come from looks.py,
# the one scale shared with the climb figure of page 5.3


def _mach_label():
    """The wave-drag band's label, its Mach number formatted from the jet's M_limit field."""
    return f"past Mach {fmt_dec(J['M_limit'], 2)}:\nwave drag"


def _num(s):
    return float(s.replace(",", "").replace("−", "-"))


def _jet():
    return J["m"], J["S"], J["CD0"], J["K"]


def _ga():
    return A["m"], A["S"], A["CD0"], A["K"]


# ===================================================================== 1. the three angles
def fig_flight_angles():
    """Lesson: the pitch angle is the flight-path angle plus the angle of attack, and level flight
    means the flight-path angle is zero (then pitch angle and angle of attack are the same)."""
    xl, yl = (-1.75, 7.6), (-3.85, 2.65)
    fig, ax = canvas(6.5, xlim=xl, ylim=yl)
    R_RAY = 3.35
    cases = [(0.0, GAMMA_SHOWN, ALPHA_SHOWN, "climbing"), (-2.3, 0.0, ALPHA_SHOWN, "level")]
    drawn = []
    for y0, g, a, name in cases:
        th = g + a
        cg = np.array([0.0, y0])
        ac = aircraft_silhouette_right(ax, center=cg, length=AC_LENGTH, pitch_deg=th, fill=PART_FILL)
        cg_symbol(ax, ac["cg"], size=9.0)
        hor = ray(ax, cg, 0.0, R_RAY, role="reference", zorder=1.5)
        ray(ax, cg, 180.0, 1.5, role="reference", zorder=1.5)
        ray(ax, cg, th, R_RAY, role="boundary", zorder=2.0)
        ray(ax, cg, 180.0 + th, 1.5, role="boundary", zorder=2.0)
        text(ax, cg + R_RAY * unit(th), "body axis", direction=th, dist=4, fs=FS_SMALL, color=STEEL)
        text(ax, cg + np.array([-1.5, 0.9]), name, fs=FS_LABEL, ha="left")
        if g > 0.0:
            text(ax, cg + np.array([R_RAY, 0.0]), "horizontal", direction=0, dist=4, fs=FS_SMALL, color=STEEL)
            path = ray(ax, cg, g, R_RAY, role="reference", zorder=1.6)
            v0 = cg + R_RAY * unit(g)
            rides_on(kind_arrow(ax, v0, v0 + 0.8 * unit(g), "velocity"), path)
            text(ax, v0 + 0.8 * unit(g), "flight path,\nvelocity $V$", direction=g, dist=5, fs=FS_SMALL,
                 color=SERIES[0])
            angle_mark(ax, cg, 0.0, g, 1.9, r"$\gamma$", stated=g, label_r=2.25)
            angle_mark(ax, cg, g, th, 2.4, r"$\alpha$", stated=a, label_r=2.78)
            close_to(th, g + a, 1e-12, "pitch angle drawn as flight-path angle plus angle of attack")
        else:
            v0 = cg + np.array([R_RAY, 0.0])
            rides_on(kind_arrow(ax, v0, v0 + np.array([0.8, 0.0]), "velocity"), hor)
            text(ax, v0 + np.array([0.8, 0.0]), "velocity $V$", direction=0, dist=5, fs=FS_SMALL, color=SERIES[0])
            text(ax, cg + np.array([4.85, 0.0]), "horizontal = flight path", direction=-90, dist=13, fs=FS_SMALL,
                 color=STEEL)
            angle_mark(ax, cg, 0.0, th, 2.4, r"$\alpha$", stated=a, label_r=2.75)
            close_to(th, a, 1e-12, "level flight: pitch angle drawn equal to the angle of attack")
        # theta just outside its own arc, inside its sector: on the bisector when level, and between the
        # horizontal and the flight path when climbing (the flight path crosses the bisector there)
        angle_mark(ax, cg, 0.0, th, 3.05, r"$\theta$", stated=th, label_r=3.35,
                   label_angle=0.5 * g if g > 0.0 else None)
        drawn.append(th)
    text(ax, (2.9, -3.45), "flight-path angle $\\gamma$: horizontal to flight path; angle of attack $\\alpha$: "
         "flight path to body axis;\npitch angle $\\theta$: horizontal to body axis, so $\\theta = \\gamma + \\alpha$. "
         "In level flight $\\gamma = 0$ and $\\theta = \\alpha$.", fs=FS_SMALL, linespacing=1.4)
    assert drawn[0] > drawn[1], "the climbing aircraft is drawn with the larger pitch angle"
    trim_canvas(fig)
    save_figure(fig, "p51-flight-angles")


# ===================================================================== 2. level-flight forces
def fig_level_flight_fbd():
    """Lesson: with a small angle of attack, lift balances the weight and thrust balances the drag.
    The four forces are drawn to one scale and in balance; the angle and the drag are exaggerated."""
    fig, ax = canvas(SCALE_IN_PER_UNIT * 5.8, xlim=(-3.05, 2.75), ylim=(-1.62, 1.62))
    a = ALPHA_DRAWN
    ac = aircraft_silhouette_right(ax, center=(0.0, 0.0), length=AC_LENGTH, pitch_deg=a, fill=PART_FILL)
    cg = ac["cg"]
    cg_symbol(ax, cg, size=10.0)
    line(ax, (-1.62, 0.0), (2.55, 0.0), role="reference", zorder=1.5)
    text(ax, (2.55, 0.0), "flight path", direction=-90, dist=6, fs=FS_SMALL, color=STEEL, ha="right")
    body = ray(ax, cg, a, 2.45, role="boundary", zorder=2.0)
    ray(ax, cg, 180.0 + a, 1.5, role="boundary", zorder=2.0)
    text(ax, cg + 2.45 * unit(a), "body axis", direction=a, dist=4, fs=FS_SMALL, color=STEEL)
    f = level_forces(ax, cg, W_DRAWN, a, LD_drawn=LD_DRAWN, starts=dict(L=0.10, W=0.10, D=1.62, T=1.28),
                     label_dirs=dict(T=a + 105.0, D=180.0), rides=dict(T=body))
    angle_mark(ax, cg, 0.0, a, 2.12, r"$\alpha$", stated=a, label_r=2.3, fs=FS_LABEL)
    v0 = np.array([0.95, -0.62])
    kind_arrow(ax, v0, v0 + np.array([0.95, 0.0]), "velocity")
    text(ax, v0 + np.array([0.95, 0.0]), "velocity, $V$", direction=0, dist=6, color=SERIES[0], fs=FS_LABEL)
    legend_key(ax, (-2.95, 1.45), [("force", "force"), ("velocity", "velocity")], dy=18, fs=FS_SMALL)
    close_to(float(np.linalg.norm(f["L"] + f["W"] + f["D"] + f["T"])), 0.0, 1e-12, "drawn forces in balance")
    assert abs(f["L"][1] / -f["W"][1] - 1.0) < 0.08 and abs(np.linalg.norm(f["T"]) / -f["D"][0] - 1.0) < 0.02
    close_to(f["tails"]["D"][1], 0.0, 1e-12, "drag drawn on the flight path through the center of gravity")
    close_to(math.degrees(math.atan2(*(f["tails"]["T"] - cg)[::-1])), a, 1e-9, "thrust drawn on the body axis")
    trim_canvas(fig)
    save_figure(fig, "p51-level-flight-fbd")


# ===================================================================== 3. L/D and thrust required against alpha
def fig_ld_and_thrust_vs_alpha():
    """Lesson: thrust required is the weight over L/D, so the minimum thrust comes at the angle of
    attack of the highest L/D."""
    m, S, CD0, K = _ga()
    a_max = A["alpha_max"]
    al = np.linspace(1.0, a_max, 800)
    r = thrust_required_vs_alpha(m, CD0, K, A["CL0"], A["CLa"], al)
    mt = min_thrust_condition(m, S, CD0, K, RHO_SL)
    a_best = float(alpha_for_CL(mt["CL"], A["CL0"], A["CLa"]))
    c1 = level_flight_at_speed(m, S, CD0, K, RHO_SL, V_SPEED_CASE, A["CL0"], A["CLa"])
    c2 = level_flight_at_alpha(m, S, CD0, K, RHO_SL, ALPHA_CASE, A["CL0"], A["CLa"])
    fig, (ax1, ax2) = data_axes(6.5, 5.2, nrows=2, sharex=True, gridspec_kw=dict(height_ratios=[1, 1.15]))
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.10, top=0.97, hspace=0.12)
    for ax in (ax1, ax2):
        ax.set_xlim(0.0, 22.0)
        ax.set_xticks([0, 4, 8, 12, 16, 20])
    ax1.set_ylim(0.0, 20.0); ax1.set_yticks([0, 5, 10, 15, 20])
    ax2.set_ylim(0.0, 3000.0); ax2.set_yticks([0, 1000, 2000, 3000])
    ax1.set_ylabel("Lift-to-drag ratio, $L/D$")
    ax2.set_ylabel("Thrust required, $T_R$, N")
    ax2.set_xlabel("Angle of attack, $\\alpha$, degrees")
    for ax in (ax1, ax2):
        ax.axvspan(a_max, 22.0, color=BAND_FILL, lw=0, zorder=0.5)
    text(ax1, (0.5 * (a_max + 22.0), 10.0), "past\nstall", fs=FS_SMALL, backing=BAND_FILL, rotation=90)
    ax1.plot(r["alpha"], r["LD"], zorder=4, **required_kw(0, linewidth=LW_PART + 0.4))
    ax2.plot(r["alpha"], r["T_R"], zorder=4, **required_kw(0))
    LDmax = float(mt["LD_max"])
    for ax, y in ((ax1, LDmax), (ax2, mt["T_min"])):
        ax.plot([a_best, a_best], [0.0, y], color=GRAY, lw=LW_THIN, linestyle=DASH_CONSTRUCTION, zorder=2)
    ax1.plot([a_best], [LDmax], "o", ms=MS_POINT, color=INK, zorder=7)
    text(ax1, (a_best, LDmax), f"$(L/D)_{{\\max}}$ = {fmt(LDmax, 4)} at $\\alpha$ = {fmt(a_best, 3)}°",
         direction=80, dist=8, fs=FS_LABEL)
    mark_minimum(ax2, a_best, mt["T_min"], f"minimum thrust,\n$\\alpha$ = {fmt(a_best, 3)}°", direction=-50,
                 dist=10, fs=FS_SMALL)
    # each open circle is labeled with its own angle and speed, on the side away from the minimum
    cases = ((c1, f"{fmt(float(c1['alpha']), 3)}°, {fmt(V_SPEED_CASE, 2)} m/s", 25.0),
             (c2, f"{fmt_dec(ALPHA_CASE, 1)}°, {fmt(float(c2['V']), 4)} m/s", 205.0))
    for c, lab, d in cases:
        aa, TT, LD = float(c["alpha"]), float(c["T_R"]), float(c["LD"])
        ax1.plot([aa], [LD], "o", ms=5.0, mfc="white", mec=INK, mew=1.2, zorder=7)
        ax2.plot([aa], [TT], "o", ms=5.0, mfc="white", mec=INK, mew=1.2, zorder=7)
        text(ax2, (aa, TT), lab, direction=d, dist=7, fs=FS_SMALL)
    text(ax2, (15.0, float(np.interp(15.0, r["alpha"], r["T_R"]))), "$T_R = mg\\,/\\,(L/D)$", direction=115,
         dist=22, fs=FS_LABEL)
    # the two ends of the speed curve of p51-thrust-required: low angle of attack is fast flight
    text(ax2, (1.35, float(np.interp(1.35, r["alpha"], r["T_R"]))), "fast flight", direction=0, dist=8,
         fs=FS_SMALL)
    text(ax2, (16.0, float(np.interp(16.0, r["alpha"], r["T_R"]))), "slow flight", direction=-90, dist=16,
         fs=FS_SMALL)
    text(ax1, (17.0, float(np.interp(17.0, r["alpha"], r["LD"]))), "$L/D$", direction=60, dist=6, fs=FS_LABEL)
    close_to(float(r["alpha"][np.argmax(r["LD"])]), a_best, 0.05, "drawn L/D peaks at the alpha of C_L*")
    close_to(float(r["alpha"][np.argmin(r["T_R"])]), a_best, 0.05, "drawn T_R is least at the same alpha")
    close_to(float(np.min(r["T_R"])), mt["T_min"], 1e-3 * mt["T_min"], "drawn minimum is T_R,min")
    on_curve(r["alpha"], r["T_R"], float(c1["alpha"]), float(c1["T_R"]), 1.0, "70 m/s case on the curve")
    on_curve(r["alpha"], r["T_R"], ALPHA_CASE, float(c2["T_R"]), 1.0, "5 deg case on the curve")
    save_figure(fig, "p51-ld-and-thrust-vs-alpha")


# ===================================================================== 4. thrust required against speed
def fig_thrust_required():
    """Lesson: slow flight pays induced drag at a high angle of attack, fast flight pays parasite drag at
    a low one, and the minimum thrust is where the two parts are equal."""
    m, S, CD0, K = _jet()
    rho = RHO_SL
    mt = min_thrust_condition(m, S, CD0, K, rho)
    Vs = stall_speed_mass(m, S, J["CLmax"], rho)
    VM = J["M_limit"] * float(speed_of_sound(standard(0.0)[0]))
    X1 = 300.0
    V = np.linspace(Vs, X1, 900)
    T0, Ti, TR = (x / 1e3 for x in thrust_required_parts(m, S, CD0, K, rho, V))
    fig, ax = data_axes(6.5, 4.2)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.13, top=0.97)
    ax.set_xlim(0.0, X1); ax.set_ylim(0.0, 70.0)
    ax.set_xticks([0, 50, 100, 150, 200, 250, 300]); ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Thrust required, $T_R$, kN")
    stall_band(ax, Vs, y_label=48.0)
    mach_band(ax, VM, label=_mach_label(), y_label=20.0)
    draw_curve(ax, V, TR, required_kw(0), x_valid=VM)
    draw_curve(ax, V, T0, part_kw("parasite"), x_valid=VM, zorder=3)
    draw_curve(ax, V, Ti, part_kw("induced"), x_valid=VM, zorder=3)
    Tmin = mt["T_min"] / 1e3
    mark_minimum(ax, mt["V"], Tmin, drop=True, y_to=0.5 * Tmin)
    callout(ax, (mt["V"], Tmin), f"minimum thrust,\n{fmt(Tmin, 4)} kN\nat {fmt(mt['V'], 4)} m/s", at=(112.0, 35.0),
            ha="left")
    ax.plot([mt["V"]], [0.5 * Tmin], "o", ms=6.0, mfc="white", mec=INK, mew=1.3, zorder=7)
    callout(ax, (mt["V"], 0.5 * Tmin), "parts equal", at=(mt["V"] + 9.0, 3.1), ha="center", fs=FS_SMALL, gap=5.0)
    pts = []
    for Vp, txt in ((V_SLOW, "slow: $C_L$ = {}\nhigh angle of attack"), (V_FAST, "fast: $C_L$ = {}\nlow angle of attack")):
        CL = 2.0 * m * G0 / (rho * Vp ** 2 * S)
        Tp = float(thrust_required(m, S, CD0, K, rho, Vp)) / 1e3
        ax.plot([Vp], [Tp], "s", ms=MS_POINT - 1.0, mfc="white", mec=INK, mew=1.3, zorder=7)
        if Vp < mt["V"]:   # slow point: a short leader up to the free space left of the minimum's label
            callout(ax, (Vp, Tp), txt.format(fmt(CL, 2)), at=(64.0, 45.0), ha="left", fs=FS_SMALL)
        else:              # fast point: the label sits just above and left of its square, no leader
            text(ax, (Vp, Tp), txt.format(fmt(CL, 2)), direction=135, dist=8, fs=FS_SMALL)
        pts.append((Vp, Tp))
    text(ax, (262.0, float(np.interp(262.0, V, TR))), "total, $T_R$", direction=135, dist=12, fs=FS_LABEL)
    text(ax, (205.0, float(np.interp(205.0, V, T0))), "parasite,\ngrows as $V^2$", direction=-40, dist=8,
         fs=FS_LABEL, color=PART_TEXT["parasite"])
    text(ax, (222.0, float(np.interp(222.0, V, Ti))), "induced,\nfalls as $1/V^2$", direction=90, dist=6,
         fs=FS_LABEL, color=PART_TEXT["induced"])
    close_to(float(V[np.argmin(TR)]), mt["V"], 0.4, "drawn minimum at V_TR,min")
    close_to(float(np.interp(mt["V"], V, T0)), float(np.interp(mt["V"], V, Ti)), 0.05, "parts drawn equal there")
    assert pts[0][0] < mt["V"] < pts[1][0] and mt["V"] < VM, "slow point left of the minimum, fast point right"
    save_figure(fig, "p51-thrust-required")


# ===================================================================== 5. power required against speed
def fig_power_required():
    """Lesson: minimum power comes at a lower speed than minimum thrust, which is where a line from the
    origin touches the power-required curve."""
    m, S, CD0, K = _ga()
    rho = RHO_SL
    Vs = stall_speed_mass(m, S, A["CLmax"], rho)
    X1 = 100.0
    V = np.linspace(Vs, 90.0, 800)
    P0_, Pi_, PR = (x / 1e3 for x in power_required_parts(m, S, CD0, K, rho, V))
    mp = min_power_condition(m, S, CD0, K, rho)
    mt = min_thrust_condition(m, S, CD0, K, rho)
    fig, ax = data_axes(6.5, 4.4)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.13, top=0.97)
    ax.set_xlim(0.0, X1); ax.set_ylim(0.0, 200.0)
    ax.set_xticks([0, 20, 40, 60, 80, 100]); ax.set_yticks([0, 40, 80, 120, 160, 200])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Power required, $P_R$, kW")
    stall_band(ax, Vs, y_label=120.0, label=f"below stall,\n$C_{{L,\\max}}$ = {fmt(A['CLmax'], 2)}", fs=FS_LABEL)
    ax.plot(V, PR, zorder=4, **required_kw(0))
    ax.plot(V, P0_, zorder=3, **part_kw("parasite"))
    ax.plot(V, Pi_, zorder=3, **part_kw("induced"))
    Pmin = mp["P_min"] / 1e3
    mark_minimum(ax, mp["V"], Pmin, drop=True)
    callout(ax, (mp["V"], Pmin), f"minimum power,\n{fmt(Pmin, 4)} kW\nat {fmt(mp['V'], 4)} m/s",
            at=(25.5, 112.0), ha="left", fs=FS_SMALL)
    tangent_from_origin(ax, mt["V"], mt["P_at_Tmin"] / 1e3, 78.0, None, origin_label=None)
    callout(ax, (mt["V"], mt["P_at_Tmin"] / 1e3),
            "tangent from the origin:\nminimum thrust",
            at=(72.0, 168.0), ha="right", fs=FS_SMALL)
    p_par = float(np.interp(mp["V"], V, P0_)); p_ind = float(np.interp(mp["V"], V, Pi_))
    ax.plot([mp["V"], mp["V"]], [p_par, p_ind], "o", ms=5.0, mfc="white", mec=INK, mew=1.1, zorder=7,
            linestyle="none")
    text(ax, (mp["V"] + 6.0, 6.8), f"induced = {fmt(p_ind / p_par, 1)} × parasite", ha="left", fs=FS_SMALL)
    text(ax, (72.0, float(np.interp(72.0, V, PR))), "total, $P_R$", direction=150, dist=14, fs=FS_LABEL)
    text(ax, (80.0, float(np.interp(80.0, V, P0_))), "parasite,\ngrows as $V^3$", direction=-35, dist=12,
         fs=FS_SMALL, color=PART_TEXT["parasite"])
    text(ax, (70.0, float(np.interp(70.0, V, Pi_))), "induced, falls as $1/V$", direction=90, dist=9,
         fs=FS_SMALL, color=PART_TEXT["induced"])
    close_to(float(V[np.argmin(PR)]), mp["V"], 0.15, "drawn minimum at V_PR,min")
    slopes = PR / V
    close_to(float(V[np.argmin(slopes)]), mt["V"], 0.15, "the line from the origin touches at V_TR,min")
    close_to(float(np.min(slopes)) * 1e3, mt["T_min"], 1e-3 * mt["T_min"], "its slope is T_R,min")
    close_to(p_ind / p_par, 3.0, 0.01, "drawn induced part is three times the parasite part at V_PR,min")
    assert Vs < mp["V"] < mt["V"], "stall, then minimum power, then minimum thrust"
    save_figure(fig, "p51-power-required")


# ===================================================================== 6. available against speed
def fig_available_against_speed():
    """Lesson: a jet's thrust and a propeller aircraft's power are nearly flat with speed, so the
    propeller's thrust falls as speed rises (and the jet's power rises with it)."""
    TA = available(J, RHO_SL)
    PA = available(A, RHO_SL)
    fig, axs = data_axes(6.5, 5.0, nrows=2, ncols=2, sharex="col")
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.10, top=0.93, wspace=0.42, hspace=0.22)
    (aT_j, aT_p), (aP_j, aP_p) = axs
    Vj = np.linspace(0.0, 300.0, 300)
    Vp = np.linspace(20.0, 100.0, 400)
    panel_title(aT_j, "executive jet")
    panel_title(aT_p, "general-aviation airplane")
    aT_j.plot(Vj, np.full_like(Vj, TA / 1e3), **available_kw(0))
    aP_j.plot(Vj, TA * Vj / 1e6, **available_kw(0))
    aP_p.plot(Vp, np.full_like(Vp, PA / 1e3), **available_kw(0))
    aT_p.plot(Vp, PA / Vp / 1e3, **available_kw(0))
    aT_j.set_xlim(0, 300); aT_j.set_ylim(0, 80); aT_j.set_yticks([0, 20, 40, 60, 80])
    aP_j.set_ylim(0, 20); aP_j.set_yticks([0, 5, 10, 15, 20]); aP_j.set_xticks([0, 100, 200, 300])
    aT_p.set_xlim(0, 100); aT_p.set_ylim(0, 10); aT_p.set_yticks([0, 2, 4, 6, 8, 10])
    aP_p.set_ylim(0, 250); aP_p.set_yticks([0, 50, 100, 150, 200, 250]); aP_p.set_xticks([0, 20, 40, 60, 80, 100])
    aT_j.set_ylabel("Thrust available, kN"); aT_p.set_ylabel("Thrust available, kN")
    aP_j.set_ylabel("Power available, MW"); aP_p.set_ylabel("Power available, kW")
    for ax in (aP_j, aP_p):
        ax.set_xlabel("True airspeed, $V$, m/s")
    text(aT_j, (150.0, TA / 1e3), f"$T_A$ = {fmt(TA / 1e3, 4)} kN, flat", direction=-90, dist=6, fs=FS_SMALL)
    text(aP_p, (60.0, PA / 1e3), f"$P_A$ = {fmt(PA / 1e3, 4)} kW, flat", direction=-90, dist=6, fs=FS_SMALL)
    text(aP_j, (215.0, TA * 215.0 / 1e6), "$P_A = T_A V$", direction=-50, dist=12, fs=FS_LABEL)
    text(aT_p, (60.0, PA / 60.0 / 1e3), "$T_A = P_A / V$", direction=50, dist=14, fs=FS_LABEL)
    pj = [TA * v / 1e6 for v in V_PAIR_JET]
    tp = [PA / v / 1e3 for v in V_PAIR_PROP]
    aP_j.plot(V_PAIR_JET, pj, "o", ms=6.0, mfc="white", mec=INK, mew=1.3, zorder=7, linestyle="none")
    aT_p.plot(V_PAIR_PROP, tp, "o", ms=6.0, mfc="white", mec=INK, mew=1.3, zorder=7, linestyle="none")
    for v, y in zip(V_PAIR_JET, pj):
        text(aP_j, (v, y), f"{fmt(y, 4)} MW", direction=140 if v > 150.0 else -35, dist=7, fs=FS_SMALL)
    for v, y in zip(V_PAIR_PROP, tp):
        text(aT_p, (v, y), f"{fmt(y, 3)} kN", direction=-130, dist=7, fs=FS_SMALL)
    close_to(pj[1] / pj[0], 2.0, 1e-12, "jet: doubling the speed doubles the power")
    close_to(tp[1] / tp[0], 0.5, 1e-12, "propeller: doubling the speed halves the thrust")
    on_curve(Vp, PA / Vp / 1e3, V_PAIR_PROP[1], tp[1], 1e-3, "the marked point lies on the drawn curve")
    save_figure(fig, "p51-available-against-speed")


# ===================================================================== 7. the speed range at sea level
def fig_available_and_vmax():
    """Lesson: level flight is possible from the stall speed to the speed where available meets
    required."""
    fig, axs = data_axes(6.5, 3.9, ncols=2)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.15, top=0.91, wspace=0.30)
    ax = axs[0]
    m, S, CD0, K = _jet()
    TA = available(J, RHO_SL)
    rj = level_speed_range(m, S, CD0, K, RHO_SL, J["CLmax"], TA, "jet")
    VM = J["M_limit"] * float(speed_of_sound(standard(0.0)[0]))
    X1 = 320.0                                  # as p51-altitude-jet, so the band holds its two-line label
    V = np.linspace(rj["V_stall"], X1, 700)
    TR = thrust_required(m, S, CD0, K, RHO_SL, V) / 1e3
    ax.set_xlim(0.0, X1); ax.set_ylim(0.0, 80.0)
    ax.set_xticks([0, 100, 200, 300]); ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Thrust, kN")
    panel_title(ax, "executive jet, sea level")
    stall_band(ax, rj["V_stall"], label="below stall", y_label=40.0)
    mach_band(ax, VM, label=_mach_label(), y_label=32.0)
    draw_curve(ax, V, TR, required_kw(0), x_valid=VM)
    draw_curve(ax, np.array([rj["V_stall"], X1]), np.array([TA, TA]) / 1e3, available_kw(0), x_valid=VM)
    mark_limit(ax, rj["V_max"], TA / 1e3, drop=True)
    text(ax, (rj["V_max"], TA / 1e3), f"$V_\\max$ = {fmt(rj['V_max'], 4)} m/s", direction=135, dist=12, ha="right")
    text(ax, (150.0, TA / 1e3), "$T_A$", direction=-90, dist=4)
    text(ax, (150.0, float(np.interp(150.0, V, TR))), "$T_R$", direction=-35, dist=6)
    dimension(ax, (rj["V_stall"], 8.0), (rj["V_max"], 8.0), "level flight possible", label_side=0, fs=FS_SMALL,
              ticks=True, extension=False)
    on_curve(V, TR, rj["V_max"], TA / 1e3, 0.01, "jet V_max on the drawn curve")
    assert rj["V_max"] < VM and rj["low_limit"] == "stall"
    ax = axs[1]
    m, S, CD0, K = _ga()
    PA = available(A, RHO_SL)
    rp = level_speed_range(m, S, CD0, K, RHO_SL, A["CLmax"], PA, "prop")
    X1 = 100.0
    V = np.linspace(rp["V_stall"], X1, 700)
    PR = power_required(m, S, CD0, K, RHO_SL, V) / 1e3
    ax.set_xlim(0.0, X1); ax.set_ylim(0.0, 250.0)
    ax.set_xticks([0, 20, 40, 60, 80, 100]); ax.set_yticks([0, 50, 100, 150, 200, 250])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Power, kW")
    panel_title(ax, "general-aviation airplane, sea level")
    stall_band(ax, rp["V_stall"], label="below stall", y_label=150.0)
    ax.plot(V, PR, zorder=4, **required_kw(0))
    ax.plot([rp["V_stall"], X1], [PA / 1e3, PA / 1e3], zorder=4, **available_kw(0))
    mark_limit(ax, rp["V_max"], PA / 1e3, drop=True)
    text(ax, (rp["V_max"], PA / 1e3), f"$V_\\max$ = {fmt(rp['V_max'], 4)} m/s", direction=135, dist=12, ha="right")
    text(ax, (50.0, PA / 1e3), "$P_A$", direction=-90, dist=4)
    text(ax, (60.0, float(np.interp(60.0, V, PR))), "$P_R$", direction=-35, dist=6)
    dimension(ax, (rp["V_stall"], 25.0), (rp["V_max"], 25.0), "level flight possible", label_side=0, fs=FS_SMALL,
              ticks=True, extension=False)
    on_curve(V, PR, rp["V_max"], PA / 1e3, 0.05, "propeller V_max on the drawn curve")
    assert rp["low_limit"] == "stall"
    save_figure(fig, "p51-available-and-vmax")


# ===================================================================== 8. the jet at two altitudes
def fig_altitude_jet():
    """Lesson: altitude slides the thrust-required curve to the right at the same minimum while the
    thrust available drops toward it. One panel per altitude, each with its own stall speed and its own
    Mach-limit speed; the same scales, so the shift reads across the two."""
    m, S, CD0, K = _jet()
    X0, X1 = 0.0, 320.0
    fig, axs = data_axes(6.5, 3.9, ncols=2, sharey=True)
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.15, top=0.91, wspace=0.14)
    Tmin = min_thrust_condition(m, S, CD0, K, RHO_SL)["T_min"] / 1e3
    out = []
    for cond, (ax, h, name) in enumerate(zip(axs, (0.0, H_JET), ("sea level", f"{fmt(H_JET, 4)} m"))):
        T_, _, rho = standard(h)[:3]
        Vs = stall_speed_mass(m, S, J["CLmax"], rho)
        VM = J["M_limit"] * float(speed_of_sound(T_))
        ax.set_xlim(X0, X1); ax.set_ylim(0.0, 70.0)
        ax.set_xticks([0, 100, 200, 300]); ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70])
        ax.set_xlabel("True airspeed, $V$, m/s")
        panel_title(ax, f"executive jet, {name}")
        stall_band(ax, Vs, label="below stall", y_label=42.0)
        mach_band(ax, VM, label=_mach_label(), y_label=37.0 if cond == 0 else 50.0)
        V = np.linspace(Vs, X1, 700)
        TR = thrust_required(m, S, CD0, K, rho, V) / 1e3
        TA = available(J, rho) / 1e3
        ax.plot([X0, X1], [Tmin, Tmin], color=GRAY, lw=LW_THIN, zorder=2)
        draw_curve(ax, V, TR, required_kw(cond), x_valid=VM)
        draw_curve(ax, np.array([Vs, X1]), np.array([TA, TA]), available_kw(cond), x_valid=VM)
        mt = min_thrust_condition(m, S, CD0, K, rho)
        mark_minimum(ax, mt["V"], mt["T_min"] / 1e3, cond=cond)
        text(ax, (mt["V"], mt["T_min"] / 1e3), f"{fmt(mt['V'], 4)} m/s", direction=-90, dist=7, fs=FS_SMALL,
             color=COND_TEXT[cond])
        _, vhi = jet_speed_bounds(m, S, CD0, K, rho, TA * 1e3)
        text(ax, (Vs + 0.3 * (VM - Vs), TA), "$T_A$", direction=-90, dist=5, color=COND_TEXT[cond])
        out.append(dict(ax=ax, V=V, TR=TR, TA=TA, Vs=Vs, VM=VM, mt=mt, vhi=vhi, rho=rho))
    s0, s1 = out
    a0 = s0["ax"]
    mark_limit(a0, s0["vhi"], s0["TA"])
    text(a0, (178.0, 64.5), f"$V_\\max$ = {fmt(s0['vhi'], 4)} m/s")
    text(a0, (150.0, float(np.interp(150.0, s0["V"], s0["TR"]))), "$T_R$", direction=135, dist=6)
    # the gray line's own label, set below it with a short leader, apart from the minimum's speed label
    callout(a0, (185.0, Tmin), f"minimum thrust,\n{fmt(Tmin, 4)} kN", at=(182.0, 5.5), ha="center", fs=FS_SMALL,
            color=STEEL, gap=2.0)
    a1 = s1["ax"]
    cond_marks(a1, s1["V"], s1["TR"], 1, at=(120.0, 140.0, 215.0, 232.0))
    text(a1, (225.0, float(np.interp(225.0, s1["V"], s1["TR"]))), "$T_R$", direction=90, dist=9, color=COND_TEXT[1])
    text(a1, (0.5 * (s1["VM"] + X1), Tmin), "same\nminimum", direction=-90, dist=4, fs=FS_SMALL, color=STEEL,
         backing=BAND_FILL)
    axs[0].set_ylabel("Thrust, kN")
    for r in out:
        close_to(float(np.min(r["TR"])), Tmin, 1e-3, "drawn minimum is the same T_R,min")
    close_to(s1["mt"]["V"] / s0["mt"]["V"], math.sqrt(s0["rho"] / s1["rho"]), 1e-12,
             "the minimum moves right by sqrt(rho0/rho)")
    assert s0["vhi"] < s0["VM"], "sea-level V_max inside the polar"
    assert s1["vhi"] > s1["VM"], "the crossing at altitude lies past the Mach limit: not marked"
    assert s1["Vs"] > s0["Vs"] and s1["VM"] < s0["VM"], "both ends of the usable speeds move with altitude"
    save_figure(fig, "p51-altitude-jet")


# ===================================================================== 9. the propeller airplane at two altitudes
def fig_altitude_prop():
    """Lesson: at altitude the power required moves up and right and the power available comes down,
    so the excess power shrinks from both sides."""
    m, S, CD0, K = _ga()
    X1, XAX = 100.0, 120.0         # curves to 100 m/s; the axis to 120 leaves room for the V_max labels
    fig, ax = data_axes(6.5, 4.4)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.13, top=0.97)
    ax.set_xlim(0.0, XAX); ax.set_ylim(0.0, 200.0)
    ax.set_xticks([0, 20, 40, 60, 80, 100, 120]); ax.set_yticks([0, 40, 80, 120, 160, 200])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Power, kW")
    res = []
    for cond, h in enumerate((0.0, H_PROP)):
        rho = standard(h)[2]
        Vs = stall_speed_mass(m, S, A["CLmax"], rho)
        V = np.linspace(Vs, X1, 700)
        PR = power_required(m, S, CD0, K, rho, V) / 1e3
        PA = available(A, rho) / 1e3
        mp = min_power_condition(m, S, CD0, K, rho)
        vmax, _ = prop_vmax(m, S, CD0, K, rho, PA * 1e3)
        ax.plot(V, PR, zorder=4, **required_kw(cond))
        ax.plot([Vs, X1], [PA, PA], zorder=4, **available_kw(cond))
        mark_minimum(ax, mp["V"], mp["P_min"] / 1e3, cond=cond)
        mark_limit(ax, vmax, PA, cond=cond, drop=False)
        xg = mp["V"]
        grp = dimension(ax, (xg, mp["P_min"] / 1e3 + 2.0), (xg, PA - 2.0), None, color=COND_COLOR[cond],
                        ticks=False, extension=False)
        if cond == 0:
            # the 6,500 m curves start at their stall speed, just left of this arrow: a white halo and a
            # place above them keep the arrow from reading as their boundary
            for art in list(ax.patches) + list(ax.lines):
                if art.get_gid() == grp:
                    art.set_path_effects([patheffects.withStroke(linewidth=4.0, foreground="white"),
                                          patheffects.Normal()])
                    art.set_zorder(4.6)
        res.append(dict(V=V, PR=PR, PA=PA, mp=mp, vmax=vmax, Vs=Vs))
    s0, s1 = res
    cond_marks(ax, s1["V"], s1["PR"], 1, at=(40.0, 60.0, 72.0))
    # the 6,500 m power available carries the same open triangles, so the two P_A lines differ by more
    # than color
    pa_marks = cond_marks(ax, [s1["Vs"], X1], [s1["PA"], s1["PA"]], 1, at=(78.0, 96.0))
    ax.axvspan(0.0, s0["Vs"], color=BAND_FILL, lw=0, zorder=0.5)
    text(ax, (0.5 * s0["Vs"], 60.0), "below stall,\nsea level", rotation=90, fs=FS_SMALL, backing=BAND_FILL)
    text(ax, (s0["mp"]["V"], 0.5 * (s1["PA"] + s0["PA"])), "excess\npower", direction=0, dist=6,
         fs=FS_SMALL)
    text(ax, (s1["mp"]["V"], 0.5 * (s1["mp"]["P_min"] / 1e3 + s1["PA"])), "excess\npower", direction=0, dist=6,
         fs=FS_SMALL, color=COND_TEXT[1])
    text(ax, (24.5, s0["PA"]), f"$P_A$, sea level, {fmt(s0['PA'], 4)} kW", direction=90, dist=4, fs=FS_SMALL,
         ha="left")
    text(ax, (35.5, s1["PA"]), f"$P_A$, {fmt(H_PROP, 4)} m, {fmt(s1['PA'], 4)} kW", direction=90, dist=4, fs=FS_SMALL,
         color=COND_TEXT[1], ha="left")
    text(ax, (s0["vmax"], s0["PA"]), f"{fmt(s0['vmax'], 4)} m/s", direction=-40, dist=10, fs=FS_SMALL)
    text(ax, (s1["vmax"], s1["PA"]), f"{fmt(s1['vmax'], 4)} m/s", direction=-40, dist=10, fs=FS_SMALL,
         color=COND_TEXT[1])
    text(ax, (80.0, float(np.interp(80.0, s0["V"], s0["PR"]))), "$P_R$, sea level", direction=180, dist=10,
         fs=FS_SMALL)
    text(ax, (84.0, float(np.interp(84.0, s1["V"], s1["PR"]))), f"$P_R$, {fmt(H_PROP, 4)} m", direction=-30, dist=8,
         fs=FS_SMALL, color=COND_TEXT[1])
    assert pa_marks is not None and len(pa_marks.get_xdata()) == 2, "6,500 m P_A drawn with its markers"
    g0 = s0["PA"] - s0["mp"]["P_min"] / 1e3
    g1 = s1["PA"] - s1["mp"]["P_min"] / 1e3
    assert g1 < g0, "the largest excess power shrinks with altitude"
    close_to(s1["mp"]["V"] / s0["mp"]["V"], math.sqrt(RHO_SL / standard(H_PROP)[2]), 1e-12,
             "minimum-power point moves right by sqrt(rho0/rho)")
    on_curve(s1["V"], s1["PR"], s1["vmax"], s1["PA"], 0.05, "6,500 m V_max on the drawn curve")
    save_figure(fig, "p51-altitude-prop")


def make_all():
    fig_flight_angles()
    fig_level_flight_fbd()
    fig_ld_and_thrust_vs_alpha()
    fig_thrust_required()
    fig_power_required()
    fig_available_against_speed()
    fig_available_and_vmax()
    fig_altitude_jet()
    fig_altitude_prop()


# ===================================================================== printed values
def values():
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731

    # ---------------- angles as drawn in the two schematics (stated in their captions)
    r("angles-gamma-drawn", fmt(GAMMA_SHOWN, 2)); r("angles-alpha-drawn", fmt(ALPHA_SHOWN, 2))
    r("fbd-alpha-drawn", fmt(ALPHA_DRAWN, 2))
    assert LD_DRAWN == 3.0, "the caption of p51-level-flight-fbd says the drag is drawn as one third of the weight"

    # ---------------- the general-aviation airplane: data
    m, S, CD0, K = _ga()
    r("ga-m", fmt(m, 4)); r("ga-S", fmt_dec(S, 1)); r("ga-CD0", fmt_dec(CD0, 3)); r("ga-K", fmt_dec(K, 3))
    r("ga-CL0", fmt_dec(A["CL0"], 2)); r("ga-CLa", fmt_dec(A["CLa"], 2))
    r("ga-CLmax", fmt_dec(A["CLmax"], 1)); r("ga-alpha-max", fmt_dec(A["alpha_max"], 1))
    r("ga-CM0", fmt_dec(A["CM0"], 2)); r("ga-CMa", fmt_dec(-A["CMa"], 2)); r("ga-CMde", fmt_dec(-A["CMde"], 3))
    r("ga-P0-kW", fmt(A["P0"] / 1e3, 3)); r("ga-eta", fmt_dec(A["eta"], 2)); r("ga-mad", fmt_dec(A["m_ad"], 1))
    Wp = _num(r("ga-W", fmt(m * G0, 5)))

    # ---------------- worked example 1 (a): speed given, 70 m/s at sea level
    V1 = V_SPEED_CASE
    r("ga-V1", fmt(V1, 2))
    q1 = _num(r("ga-q1", fmt(0.5 * RHO_SL * V1 ** 2, 5)))
    qS1 = _num(r("ga-qS1", fmt(q1 * S, 5)))
    CL1 = _num(r("ga-CL1", fmt(Wp / qS1, 4)))
    a1 = _num(r("ga-alpha1", fmt((CL1 - A["CL0"]) / A["CLa"], 3)))
    CD1 = _num(r("ga-CD1", fmt(CD0 + K * CL1 ** 2, 4)))
    D1 = _num(r("ga-D1", fmt(qS1 * CD1, 4)))
    P1 = _num(r("ga-P1", fmt(D1 * V1, 5)))
    r("ga-P1-kW", fmt(P1 / 1e3, 4))
    num = _num(r("ga-trim-num", fmt(A["CM0"] + A["CMa"] * a1, 3)))
    r("ga-de1", fmt(-num / A["CMde"], 3))
    r("ga-de1-abs", fmt(abs(num / A["CMde"]), 3))
    PA_sl = _num(r("ga-PA-sl", fmt(A["eta"] * A["P0"] / 1e3, 4)))
    r("ga-cos1", fmt(math.cos(math.radians(a1)), 5))
    Ts = _num(r("ga-Tsin1", fmt(D1 * math.sin(math.radians(a1)), 3)))
    r("ga-Tsin1-pct", fmt(100.0 * Ts / Wp, 2))

    # ---------------- worked example 1 (b): angle of attack given, 5 deg at sea level
    r("ga-alpha2", fmt_dec(ALPHA_CASE, 1))
    CL2 = _num(r("ga-CL2", fmt_dec(A["CL0"] + A["CLa"] * ALPHA_CASE, 2)))
    CD2 = _num(r("ga-CD2", fmt(CD0 + K * CL2 ** 2, 4)))
    V2 = _num(r("ga-V2", fmt(math.sqrt(2.0 * Wp / (RHO_SL * S * CL2)), 4)))
    LD2 = _num(r("ga-LD2", fmt(CL2 / CD2, 4)))
    T2 = _num(r("ga-T2", fmt(Wp / LD2, 4)))
    P2 = _num(r("ga-P2", fmt(T2 * V2, 5)))
    r("ga-P2-kW", fmt(P2 / 1e3, 4))

    # ---------------- worked example 1 (c): feasibility
    r("ga-CL-high", fmt_dec(CL_TOO_HIGH, 1))
    r("ga-Vs-sl", fmt(stall_speed_mass(m, S, A["CLmax"], RHO_SL), 4))

    # ---------------- the airplane: minimum thrust and power, alpha view, V_max
    mt = min_thrust_condition(m, S, CD0, K, RHO_SL)
    mp = min_power_condition(m, S, CD0, K, RHO_SL)
    r("ga-LDmax", fmt(mt["LD_max"], 4)); r("ga-CLstar", fmt(mt["CL"], 4))
    r("ga-alpha-star", fmt(float(alpha_for_CL(mt["CL"], A["CL0"], A["CLa"])), 3))
    r("ga-Vp-sl", fmt(mp["V"], 4)); r("ga-Pmin-sl", fmt(mp["P_min"] / 1e3, 4))
    # worked example 2 (b): the minimum power in steps, as for the jet
    wsg = _num(r("ga-root-ws", fmt(math.sqrt(2.0 * Wp / (RHO_SL * S)), 4)))
    k3g = _num(r("ga-k314", fmt((K / (3.0 * CD0)) ** 0.25, 4)))
    Vpg = _num(fmt(wsg * k3g, 4))
    close_to(Vpg, _num(fmt(mp["V"], 4)), 1e-9, "printed V_PR,min of the airplane from the printed factors")
    CLpg = _num(r("ga-CLp", fmt(math.sqrt(3.0 * CD0 / K), 5)))
    CDpg = _num(r("ga-CDp", fmt_dec(4.0 * CD0, 3)))
    TRpg = _num(r("ga-TRp", fmt(Wp * CDpg / CLpg, 5)))
    Ppg = _num(r("ga-Pmin-W", fmt(TRpg * Vpg, 5)))
    close_to(Ppg / 1e3, _num(fmt(mp["P_min"] / 1e3, 4)), 0.005, "printed P_R,min of the airplane from the steps")
    vp0, _ = prop_vmax(m, S, CD0, K, RHO_SL, PA_sl * 1e3)
    den = _num(r("ga-den-sl", fmt(RHO_SL * S * CD0, 5)))
    ind = _num(r("ga-ind-num", fmt(2.0 * K * Wp ** 2 / (RHO_SL * S), 6)))
    PAW = PA_sl * 1e3
    r("ga-PA-sl-W", fmt(PAW, 6))
    v = (2.0 * PAW / den) ** (1.0 / 3.0)
    vs = [_num(r("ga-Vmax-it0", fmt(v, 4)))]
    for k in (1, 2):
        v = ((2.0 / den) * (PAW - ind / vs[-1])) ** (1.0 / 3.0)
        vs.append(_num(r(f"ga-Vmax-it{k}", fmt(v, 4))))
    r("ga-Vmax-sl", fmt(vp0, 4))
    close_to(vs[-1], vp0, 0.006, "two hand passes reach the converged V_max to four figures")
    pp = power_required_parts(m, S, CD0, K, RHO_SL, vp0)
    r("ga-Vmax-par-kW", fmt(float(pp[0]) / 1e3, 4)); r("ga-Vmax-ind-kW", fmt(float(pp[1]) / 1e3, 3))
    pm = power_required_parts(m, S, CD0, K, RHO_SL, mp["V"])
    r("ga-Pmin-par-kW", fmt(float(pm[0]) / 1e3, 3)); r("ga-Pmin-ind-kW", fmt(float(pm[1]) / 1e3, 4))
    for v_ in V_PAIR_PROP:
        r(f"ga-TA-{int(v_)}", fmt(PAW / v_ / 1e3, 3))

    # ---------------- the airplane at 6,500 m
    rho6 = standard(H_PROP)[2]
    r("ga-h6", fmt(H_PROP, 4)); r("ga-rho6", fmt(rho6, 4))
    rho6p = _num(fmt(rho6, 4))
    # five figures in the ratio and the root, so the printed steps land on the exact results
    ratio6 = _num(r("ga-ratio6", fmt(rho6p / RHO_SL, 5)))
    PA6 = _num(r("ga-PA6", fmt(PA_sl * ratio6 ** A["m_ad"], 5)))
    r("ga-PA6-kW4", fmt(PA6, 4))
    PA6W = _num(r("ga-PA6-W", fmt(PA6 * 1e3, 5)))
    root6 = _num(r("ga-root6", fmt(math.sqrt(RHO_SL / rho6p), 5)))
    r("ga-Vp6", fmt(_num(fmt(mp["V"], 4)) * root6, 4))
    r("ga-Pmin6", fmt(_num(fmt(mp["P_min"] / 1e3, 4)) * root6, 4))
    close_to(_num(fmt(_num(fmt(mp["V"], 4)) * root6, 4)), mp["V"] * math.sqrt(RHO_SL / rho6), 0.006,
             "printed minimum-power speed at 6,500 m")
    vm6, _ = prop_vmax(m, S, CD0, K, rho6, available(A, rho6))
    r("ga-Vmax6", fmt(vm6, 4))
    # the hand passes at 6,500 m, from the printed density, weight and power available
    den6 = _num(r("ga-den6", fmt(rho6p * S * CD0, 5)))
    ind6 = _num(r("ga-ind6", fmt(2.0 * K * Wp ** 2 / (rho6p * S), 7)))
    v = (2.0 * PA6W / den6) ** (1.0 / 3.0)
    vs6 = [_num(r("ga-Vmax6-it0", fmt(v, 4)))]
    for k in range(1, 8):
        v = ((2.0 / den6) * (PA6W - ind6 / vs6[-1])) ** (1.0 / 3.0)
        vs6.append(_num(fmt(v, 4)))
        if vs6[-1] == vs6[-2]:
            break
        r(f"ga-Vmax6-it{k}", fmt(v, 4))
    assert vs6[-1] == vs6[-2] and fmt(vs6[-1], 4) == fmt(vm6, 4), "the printed passes converge on V_max"

    # ---------------- the jet: data and worked example 2
    mj, Sj, CD0j, Kj = _jet()
    r("jet-m", fmt(mj, 5)); r("jet-S", fmt_dec(Sj, 1)); r("jet-CD0", fmt_dec(CD0j, 3)); r("jet-K", fmt_dec(Kj, 3))
    r("jet-T0-one", fmt(J["T0"], 5)); r("jet-mad", fmt_dec(J["m_ad"], 1)); r("jet-CLmax", fmt_dec(J["CLmax"], 1))
    TA0 = _num(r("jet-T0-tot", fmt(J["n"] * J["T0"], 5)))
    Wj = _num(r("jet-W", fmt(mj * G0, 6)))
    mtj = min_thrust_condition(mj, Sj, CD0j, Kj, RHO_SL)
    mpj = min_power_condition(mj, Sj, CD0j, Kj, RHO_SL)
    LDj = _num(r("jet-LDmax", fmt(mtj["LD_max"], 4)))
    sq = _num(r("jet-sqrtKC", fmt(math.sqrt(Kj * CD0j), 5)))
    Tminj = _num(r("jet-Tmin", fmt(2.0 * Wj * sq, 5)))
    close_to(Tminj, mtj["T_min"], 1.0, "printed T_R,min from the printed root")
    close_to(1.0 / (2.0 * sq), LDj, 0.01, "(L/D)max from the printed root")
    r("jet-Tmin-kN", fmt(mtj["T_min"] / 1e3, 4))
    ws = _num(r("jet-root-ws", fmt(math.sqrt(2.0 * Wj / (RHO_SL * Sj)), 5)))
    k1 = _num(r("jet-k14", fmt((Kj / CD0j) ** 0.25, 5)))
    k3 = _num(r("jet-k314", fmt((Kj / (3.0 * CD0j)) ** 0.25, 5)))
    Vtj = _num(r("jet-Vt-sl", fmt(ws * k1, 4)))
    close_to(Vtj, mtj["V"], 0.06, "V_TR,min from the printed factors")
    r("speed-ratio", fmt(3.0 ** (-0.25), 4))
    r("speed-ratio-3", fmt(3.0 ** (-0.25), 3))
    Vpj = _num(r("jet-Vp-sl", fmt(ws * k3, 4)))
    CLp = _num(r("jet-CLp", fmt(math.sqrt(3.0 * CD0j / Kj), 5)))
    r("jet-CDp", fmt_dec(4.0 * CD0j, 3))
    TRp = _num(r("jet-TRp", fmt(Wj * 4.0 * CD0j / CLp, 5)))
    Pp = _num(r("jet-Pmin-W", fmt(TRp * Vpj, 5)))
    r("jet-Pmin-sl", fmt(Pp / 1e3, 4))
    close_to(Pp, mpj["P_min"], 0.001 * mpj["P_min"], "printed P_R,min from the printed steps")
    close_to(ws * k3, mpj["V"], 0.01, "V_PR,min from the printed factors")
    rootj = _num(r("jet-root-disc", fmt(math.sqrt(TA0 ** 2 - Tminj ** 2), 5)))
    denj = _num(r("jet-den-sl", fmt(RHO_SL * Sj * CD0j, 5)))
    vmj = _num(r("jet-Vmax-sl", fmt(math.sqrt((TA0 + rootj) / denj), 4)))
    _, vmj_exact = jet_speed_bounds(mj, Sj, CD0j, Kj, RHO_SL, TA0)
    close_to(vmj, vmj_exact, 0.06, "printed V_max")
    a_sl = _num(r("a-sl", fmt(float(speed_of_sound(T_SL)), 4)))
    r("jet-Mmax-sl", fmt(vmj / a_sl, 3))
    r("jet-VM-sl", fmt(J["M_limit"] * a_sl, 4))
    r("jet-Mlimit", fmt_dec(J["M_limit"], 2))
    r("jet-Vs-sl", fmt(stall_speed_mass(mj, Sj, J["CLmax"], RHO_SL), 4))
    vlo, _ = jet_speed_bounds(mj, Sj, CD0j, Kj, RHO_SL, TA0)
    r("jet-Vlow-sl", fmt(vlo, 4))
    for v_, key in ((V_SLOW, "slow"), (V_FAST, "fast")):
        r(f"jet-V-{key}", fmt(v_, 2))
        r(f"jet-CL-{key}", fmt(2.0 * Wj / (RHO_SL * v_ ** 2 * Sj), 2))
    for v_ in V_PAIR_JET:
        r(f"jet-PA-{int(v_)}", fmt(TA0 * v_ / 1e6, 4))

    # ---------------- the jet: thrust available against altitude (table)
    for h in H_TABLE:
        rho = standard(h)[2]
        tag = f"{int(h)}"
        if h:
            r(f"jet-tab-h{tag}", fmt(h, 4))
        rp_ = _num(r(f"jet-tab-rho{tag}", fmt_dec(rho, 5)))
        TAt = r(f"jet-tab-TA{tag}", fmt(available(J, rho), 5))
        assert fmt(J["n"] * J["T0"] * (rp_ / RHO_SL) ** J["m_ad"], 5) == TAt, "printed density gives the thrust"
        r(f"jet-tab-excess{tag}", fmt(available(J, rho) - mtj["T_min"], 5))

    # ---------------- the jet at 9,500 m (worked example 3)
    T95, _, rho95 = standard(H_JET)[:3]
    r("jet-h95", fmt(H_JET, 4))
    rho95p = _num(r("jet-rho95", fmt(rho95, 4)))
    ratio95 = _num(r("jet-ratio95", fmt(rho95p / RHO_SL, 4)))
    TA95 = _num(r("jet-TA95", fmt(TA0 * ratio95 ** J["m_ad"], 5)))
    root95 = _num(r("jet-root95", fmt(math.sqrt(RHO_SL / rho95p), 4)))
    Vt95 = _num(r("jet-Vt95", fmt(Vtj * root95, 4)))
    r("jet-Vs95", fmt(stall_speed_mass(mj, Sj, J["CLmax"], rho95), 4))
    a95 = _num(r("a-95", fmt(float(speed_of_sound(T95)), 4)))
    VM95 = _num(r("jet-VM95", fmt(J["M_limit"] * a95, 4)))
    q95 = _num(r("jet-q95", fmt(0.5 * rho95p * VM95 ** 2, 5)))
    qS95 = _num(r("jet-qS95", fmt(q95 * Sj, 6)))
    par95 = _num(r("jet-par95", fmt(qS95 * CD0j, 5)))
    ind95 = _num(r("jet-ind95", fmt(Kj * Wj ** 2 / qS95, 4)))
    TRVM = _num(r("jet-TR-VM95", fmt(par95 + ind95, 5)))
    assert TRVM < TA95 and Vt95 < VM95
