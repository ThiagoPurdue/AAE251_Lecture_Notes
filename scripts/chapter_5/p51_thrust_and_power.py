"""Figures and values of 5.1 Thrust and Power (notes/chapter-5/thrust-and-power.md).

Running examples (from the course lectures, verified not in the problem bank or homework):
  - GA propeller aircraft (single piston + propeller): m = 1,315 kg, S = 16.3 m^2,
    C_L = 0.02 + 0.12 alpha (deg), C_L,max = 2.4, C_D = 0.026 + 0.054 C_L^2,
    C_P = 0.12 - 0.08 alpha + 0.075 delta_e (deg), P_0 = 216 kW, eta = 0.80, m_ad = 0.6.
  - Executive twin-jet: m = 33,100 kg, S = 88.2 m^2, C_D,0 = 0.015, K = 0.050,
    n = 2 engines of T_0 = 27,810 N each (total 55,620 N at sea level), m_ad = 0.6.
"""
from chapter_5.common import *

PAGE = "p51"
BAND_FILL = "#E6E6E6"

# ===================================================================== aircraft data
GA = dict(m=1315.0, S=16.3, CD0=0.026, K=0.054, CL0=0.02, CLa=0.12, CLmax=2.4,
          CP0=0.12, CPa=-0.08, CPe=0.075, n=1, P0=216e3, eta=0.80, m_ad=0.6)
JET = dict(m=33100.0, S=88.2, CD0=0.015, K=0.050, CLmax=1.6, n=2, T0=27810.0, m_ad=0.6)

GA_V1 = 70.0         # m/s, Example 1a (speed given at sea level)
GA_ALPHA2 = 5.0      # deg, Example 1b (angle of attack given at sea level)
GA_H_ALT = 6000.0    # m, altitude comparison for propeller aircraft
JET_H_MID = 10000.0  # m, altitude comparison (mid)
JET_H_HI = 14000.0   # m, altitude comparison (near ceiling)


def _num(s):
    return float(s.replace(",", "").replace("−", "-"))


# ===================================================================== figures
def fig_level_flight_fbd():
    """Side view of a jet transport in steady level flight, showing the flight path, body roll
    axis pitched at alpha, velocity V_inf, and the four forces L, mg, T, D, with an arrow key."""
    fig, ax = canvas(6.5, xlim=(-2.35, 2.55), ylim=(-1.38, 1.52))
    alpha_draw = 12.0   # exaggerated for visibility (caption states this)
    ac = aircraft_silhouette_right(ax, center=(0.0, 0.0), length=2.40, pitch_deg=alpha_draw, fill=PART_FILL)
    cg = ac["cg"]
    cg_symbol(ax, cg, size=10.0)

    # Horizontal flight path and pitched thrust/roll axis
    href = line(ax, (-2.15, 0.0), (2.25, 0.0), role="reference", zorder=1.5)
    roll_fwd = ray(ax, cg, alpha_draw, 2.00, role="boundary", zorder=2.0)
    ray(ax, cg, 180.0 + alpha_draw, 1.45, role="boundary", zorder=2.0)

    # Velocity arrow along flight path ahead of nose
    v0 = (1.35, 0.0)
    v1 = (2.15, 0.0)
    rides_on(kind_arrow(ax, v0, v1, "velocity", None), href)
    text(ax, (1.82, 0.0), r"airspeed, $V_\infty$", direction=-90, dist=8, color=BLUE, fs=FS_LABEL)
    text(ax, (-2.12, 0.0), "flight path", direction=-90, dist=7, fs=FS_SMALL, color=STEEL, ha="left")

    # Angle of attack arc between horizontal flight path and thrust line
    angle_mark(ax, cg, 0.0, alpha_draw, 1.45, r"$\alpha$", stated=alpha_draw, label_r=1.68, fs=FS_LABEL)

    # Four forces at CG (outside fuselage silhouette)
    L_tip = cg + np.array([0.0, 1.15])
    W_tip = cg + np.array([0.0, -1.10])
    D_tip = cg + np.array([-1.55, 0.0])
    T_tip = cg + 1.62 * unit(alpha_draw)
    kind_arrow(ax, cg + np.array([0.0, 0.14]), L_tip, "force", "lift, $L$", label_dir=90, dist=4)
    kind_arrow(ax, cg + np.array([0.0, -0.14]), W_tip, "force", "weight, $mg$", label_dir=-90, dist=4)
    rides_on(kind_arrow(ax, cg + np.array([-0.14, 0.0]), D_tip, "force", "drag, $D$", label_dir=135, dist=5), href)
    rides_on(kind_arrow(ax, cg + 0.14 * unit(alpha_draw), T_tip, "force", None), roll_fwd)
    text(ax, T_tip, "thrust, $T$", direction=95, dist=10, fs=FS_LABEL)

    legend_key(ax, (-2.25, 1.32), [("force", "force"), ("velocity", "velocity")], dy=18, fs=FS_SMALL)
    close_to(float(np.dot(L_tip - cg, D_tip - cg)), 0.0, 1e-12, "lift perpendicular to drag")
    close_to(math.degrees(math.atan2(T_tip[1], T_tip[0])), alpha_draw, 1e-9, "thrust along roll axis")
    trim_canvas(fig)
    save_figure(fig, "p51-level-flight-fbd")


def fig_thrust_required():
    """Executive jet at sea level: parasite, induced and total thrust required against airspeed,
    crossing at V_TR,min where parasite equals induced."""
    m, S, CD0, K = JET["m"], JET["S"], JET["CD0"], JET["K"]
    rho = RHO_SL
    mt = min_thrust_condition(m, S, CD0, K, rho)
    Vs = stall_speed_mass(m, S, JET["CLmax"], rho)
    V_hi = 260.0
    V = np.linspace(Vs, V_hi, 600)
    T0, Ti, TR = (x / 1000.0 for x in thrust_required_parts(m, S, CD0, K, rho, V))
    Tmin_kN = mt["T_min"] / 1000.0
    Vmd = mt["V"]

    fig, ax = data_axes(6.5, 4.1)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.14, top=0.96)
    ax.axvspan(40.0, Vs, color=BAND_FILL, lw=0, zorder=0.5)
    text(ax, (0.5 * (40.0 + Vs), 46.0), "stall", rotation=90, fs=FS_SMALL, backing=BAND_FILL)

    ax.plot(V, TR, **line_kw(0), zorder=4)
    ax.plot(V, T0, **line_kw(1), zorder=3)
    ax.plot(V, Ti, **line_kw(2), zorder=3)
    ax.plot([Vmd, Vmd], [0.0, Tmin_kN], **line_kw("boundary"), zorder=2)
    ax.plot([Vmd], [Tmin_kN], "o", ms=6.5, color=INK, zorder=6)
    ax.plot([Vmd], [0.5 * Tmin_kN], "o", ms=5.5, mfc="white", mec=INK, mew=1.3, zorder=6)

    ax.set_xlim(40, 260); ax.set_ylim(0, 65)
    ax.set_xticks([40, 80, 120, 160, 200, 240])
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60])
    ax.set_xlabel("True airspeed, $V$, m/s")
    ax.set_ylabel("Thrust required, $T_R$, kN")

    callout(ax, (Vmd, Tmin_kN),
            f"minimum thrust, $T_{{R,\\min}}$ = {fmt(Tmin_kN, 4)} kN\nat $V_{{T_R,\\min}}$ = {fmt(Vmd, 4)} m/s",
            at=(102, 51.0), ha="left", fs=FS_LABEL)
    callout(ax, (Vmd, 0.5 * Tmin_kN), "parasite = induced", at=(148, 7.5), ha="left", fs=FS_SMALL)
    text(ax, (256, 61.0), "total, $T_R$", fs=FS_LABEL, color=INK, ha="right")
    text(ax, (230, 23.0), "parasite,\ngrows as $V^2$", fs=FS_SMALL, color=text_color(1))
    text(ax, (82, 33.0), "induced,\nfalls as $1/V^2$", fs=FS_SMALL, color=text_color(2), ha="left")

    close_to(float(V[np.argmin(TR)]), Vmd, 0.5, "minimum of drawn T_R at V_TR,min")
    close_to(float(np.min(TR)), Tmin_kN, 0.05, "drawn T_R,min matches formula")
    save_figure(fig, "p51-thrust-required")


def fig_power_required():
    """GA propeller aircraft at sea level: parasite, induced and total power required against
    airspeed, marking V_PR,min and the tangent from the origin at V_TR,min."""
    m, S, CD0, K = GA["m"], GA["S"], GA["CD0"], GA["K"]
    rho = RHO_SL
    mp = min_power_condition(m, S, CD0, K, rho)
    mt = min_thrust_condition(m, S, CD0, K, rho)
    Vs = stall_speed_mass(m, S, GA["CLmax"], rho)
    V = np.linspace(Vs, 88.0, 600)
    P0_, Pi_, PR = (x / 1000.0 for x in power_required_parts(m, S, CD0, K, rho, V))
    Vp, Pmin = mp["V"], mp["P_min"] / 1000.0
    Vt, Pt = mt["V"], mt["P_at_Tmin"] / 1000.0

    fig, ax = data_axes(6.5, 4.2)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.14, top=0.96)
    ax.axvspan(10.0, Vs, color=BAND_FILL, lw=0, zorder=0.5)
    text(ax, (0.5 * (10.0 + Vs), 130.0), "stall", rotation=90, fs=FS_SMALL, backing=BAND_FILL)

    ax.plot(V, PR, **line_kw(0), zorder=4)
    ax.plot(V, P0_, **line_kw(1), zorder=3)
    ax.plot(V, Pi_, **line_kw(2), zorder=3)
    V_tan = np.array([0.0, 82.0])
    ax.plot(V_tan, (Pt / Vt) * V_tan, color=STEEL, lw=1.2, ls=(0, (5, 2.5)), zorder=3)

    ax.plot([Vp], [Pmin], "o", ms=6.5, color=INK, zorder=6)
    ax.plot([Vt], [Pt], "s", ms=6.0, mfc="white", mec=INK, mew=1.4, zorder=6)

    ax.set_xlim(10, 92); ax.set_ylim(0, 198)
    ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90])
    ax.set_yticks([0, 40, 80, 120, 160])
    ax.set_xlabel("True airspeed, $V$, m/s")
    ax.set_ylabel("Power required, $P_R$, kW")

    callout(ax, (Vp, Pmin),
            f"minimum power,\n{fmt(Pmin, 4)} kW at {fmt(Vp, 4)} m/s",
            at=(25.0, 152.0), ha="left", fs=FS_SMALL)
    callout(ax, (Vt, Pt),
            f"tangent from origin:\n$V_{{T_R,\\min}}$ = {fmt(Vt, 4)} m/s",
            at=(38.0, 98.0), ha="left", fs=FS_LABEL)
    text(ax, (74.0, 174.0), "total, $P_R$", fs=FS_LABEL, color=INK, ha="right")
    text(ax, (90.5, 58.0), "parasite,\ngrows as $V^3$", fs=FS_SMALL, color=text_color(1), ha="right")
    text(ax, (68.0, 29.0), "induced, falls as $1/V$", fs=FS_SMALL, color=text_color(2), ha="center")

    close_to(float(V[np.argmin(PR)]), Vp, 0.25, "minimum of P_R at V_PR,min")
    close_to(Pt / Vt, mt["T_min"] / 1000.0, 1e-6, "tangent slope equals T_R,min")
    save_figure(fig, "p51-power-required")


def fig_available_and_vmax():
    """Two panels comparing maximum speed V_max: left, executive jet (T_A meets T_R);
    right, GA propeller aircraft (P_A meets P_R), both at sea level."""
    fig, axs = data_axes(6.5, 3.8, ncols=2)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.16, top=0.90, wspace=0.34)

    # Panel 1: Executive jet at sea level
    ax = axs[0]
    m, S, CD0, K = JET["m"], JET["S"], JET["CD0"], JET["K"]
    TA = thrust_available(JET["n"], JET["T0"], RHO_SL, JET["m_ad"])
    _, v_hi = jet_speed_bounds(m, S, CD0, K, RHO_SL, TA)
    Vs_j = stall_speed_mass(m, S, JET["CLmax"], RHO_SL)
    Vj = np.linspace(Vs_j, 275.0, 400)
    TRj = thrust_required(m, S, CD0, K, RHO_SL, Vj) / 1000.0
    TA_kN = TA / 1000.0
    ax.plot(Vj, TRj, **line_kw(0), zorder=4)
    ax.plot([50.0, 275.0], [TA_kN, TA_kN], **line_kw(1), zorder=4)
    ax.plot([v_hi], [TA_kN], "o", ms=6.5, color=INK, zorder=6)
    ax.plot([v_hi, v_hi], [0.0, TA_kN], **line_kw("boundary"), zorder=2)
    ax.set_xlim(50, 280); ax.set_ylim(0, 82)
    ax.set_xticks([50, 100, 150, 200, 250])
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_title("1  jet (thrust)", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("True airspeed, $V$, m/s")
    ax.set_ylabel("Thrust, kN")
    text(ax, (118, TA_kN), f"$T_A$ = {fmt(TA_kN, 4)} kN", direction=-90, dist=6, fs=FS_SMALL, color=text_color(1))
    text(ax, (125, 11.0), "$T_R$", fs=FS_LABEL, color=INK)
    callout(ax, (v_hi, TA_kN), f"$V_\\max$ = {fmt(v_hi, 4)} m/s", at=(102, 70.0), ha="left", fs=FS_LABEL)
    close_to(float(thrust_required(m, S, CD0, K, RHO_SL, v_hi)), TA, 1e-6, "jet Vmax exact")

    # Panel 2: GA propeller aircraft at sea level
    ax = axs[1]
    mg, Sg, CD0g, Kg = GA["m"], GA["S"], GA["CD0"], GA["K"]
    PA = power_available(GA["n"], GA["P0"], GA["eta"], RHO_SL, GA["m_ad"])
    vp_max, _ = prop_vmax(mg, Sg, CD0g, Kg, RHO_SL, PA)
    Vs_g = stall_speed_mass(mg, Sg, GA["CLmax"], RHO_SL)
    Vg = np.linspace(Vs_g, 92.0, 400)
    PRg = power_required(mg, Sg, CD0g, Kg, RHO_SL, Vg) / 1000.0
    PA_kW = PA / 1000.0
    ax.plot(Vg, PRg, **line_kw(0), zorder=4)
    ax.plot([20.0, 92.0], [PA_kW, PA_kW], **line_kw(1), zorder=4)
    ax.plot([vp_max], [PA_kW], "o", ms=6.5, color=INK, zorder=6)
    ax.plot([vp_max, vp_max], [0.0, PA_kW], **line_kw("boundary"), zorder=2)
    ax.set_xlim(20, 95); ax.set_ylim(0, 232)
    ax.set_xticks([20, 40, 60, 80])
    ax.set_yticks([0, 50, 100, 150, 200])
    ax.set_title("2  propeller (power)", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("True airspeed, $V$, m/s")
    ax.set_ylabel("Power, kW")
    text(ax, (42, PA_kW), f"$P_A$ = {fmt(PA_kW, 4)} kW", direction=90, dist=5, fs=FS_SMALL, color=text_color(1))
    text(ax, (58, 36.0), "$P_R$", fs=FS_LABEL, color=INK)
    callout(ax, (vp_max, PA_kW), f"$V_\\max$ =\n{fmt(vp_max, 4)} m/s", at=(32, 118.0), ha="left", fs=FS_LABEL)
    close_to(float(power_required(mg, Sg, CD0g, Kg, RHO_SL, vp_max)), PA, 1e-4, "prop Vmax exact")
    save_figure(fig, "p51-available-and-vmax")


def fig_altitude_jet():
    """Effect of altitude on the executive jet (sea level and 14,000 m):
    left, T_R and T_A against V (T_R,min stays constant while moving right; T_A drops);
    right, P_R and P_A = T_A V against V (P_A lines get shallower; P_R moves up and right)."""
    m, S, CD0, K = JET["m"], JET["S"], JET["CD0"], JET["K"]
    rho0 = RHO_SL
    rho14 = standard(JET_H_HI)[2]
    TA0 = thrust_available(JET["n"], JET["T0"], rho0, JET["m_ad"])
    TA14 = thrust_available(JET["n"], JET["T0"], rho14, JET["m_ad"])
    mt0 = min_thrust_condition(m, S, CD0, K, rho0)
    mt14 = min_thrust_condition(m, S, CD0, K, rho14)
    _, vm0 = jet_speed_bounds(m, S, CD0, K, rho0, TA0)
    _, vm14 = jet_speed_bounds(m, S, CD0, K, rho14, TA14)

    fig, axs = data_axes(6.5, 3.9, ncols=2)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.16, top=0.90, wspace=0.35)

    V0 = np.linspace(stall_speed_mass(m, S, JET["CLmax"], rho0), 275.0, 400)
    V14 = np.linspace(stall_speed_mass(m, S, JET["CLmax"], rho14), 310.0, 400)

    # Panel 1: Thrust
    ax = axs[0]
    ax.plot(V0, thrust_required(m, S, CD0, K, rho0, V0) / 1000.0, **line_kw(0), zorder=4)
    ax.plot(V14, thrust_required(m, S, CD0, K, rho14, V14) / 1000.0, **line_kw(1), zorder=4)
    ax.plot([50.0, 275.0], [TA0 / 1000.0, TA0 / 1000.0], color=INK, lw=1.4, ls=(0, (6, 2.5)), zorder=3)
    ax.plot([130.0, 310.0], [TA14 / 1000.0, TA14 / 1000.0], color=BLUE, lw=1.4, ls=(0, (2, 2)), zorder=3)
    ax.plot([mt0["V"], mt14["V"]], [mt0["T_min"] / 1000.0, mt14["T_min"] / 1000.0], "o", ms=5.5, color=INK, zorder=6)
    ax.plot([vm0], [TA0 / 1000.0], "s", ms=5.5, mfc="white", mec=INK, mew=1.3, zorder=6)
    ax.plot([vm14], [TA14 / 1000.0], "s", ms=5.5, mfc="white", mec=BLUE, mew=1.3, zorder=6)
    ax.axhline(mt0["T_min"] / 1000.0, **line_kw("reference"), zorder=1.5)
    ax.set_xlim(50, 325); ax.set_ylim(0, 68)
    ax.set_xticks([50, 120, 190, 260]); ax.set_yticks([0, 20, 40, 60])
    ax.set_title("1  thrust vs. speed", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Thrust, kN")
    text(ax, (152, TA0 / 1000.0), "$T_A$, sea level", direction=90, dist=4, fs=FS_SMALL, color=INK)
    text(ax, (250, TA14 / 1000.0), "$T_A$, 14 km", direction=90, dist=6, fs=FS_SMALL, color=BLUE)
    text(ax, (186, 44.0), "$T_R$, sea level", fs=FS_SMALL, color=INK, ha="right")
    text(ax, (252, 8.0), "$T_R$, 14 km", fs=FS_SMALL, color=BLUE)
    text(ax, (62, mt0["T_min"] / 1000.0), "same $T_{R,\\min}$", direction=-90, dist=7, fs=FS_LABEL,
         color=STEEL, ha="left")

    # Panel 2: Power (P_A = T_A V is a straight line through the origin)
    ax = axs[1]
    ax.plot(V0, power_required(m, S, CD0, K, rho0, V0) / 1e6, **line_kw(0), zorder=4)
    ax.plot(V14, power_required(m, S, CD0, K, rho14, V14) / 1e6, **line_kw(1), zorder=4)
    Vx = np.array([0.0, 280.0])
    ax.plot(Vx, TA0 * Vx / 1e6, color=INK, lw=1.4, ls=(0, (6, 2.5)), zorder=3)
    Vx14 = np.array([0.0, 310.0])
    ax.plot(Vx14, TA14 * Vx14 / 1e6, color=BLUE, lw=1.4, ls=(0, (2, 2)), zorder=3)
    ax.plot([vm0], [TA0 * vm0 / 1e6], "s", ms=5.5, mfc="white", mec=INK, mew=1.3, zorder=6)
    ax.plot([vm14], [TA14 * vm14 / 1e6], "s", ms=5.5, mfc="white", mec=BLUE, mew=1.3, zorder=6)
    ax.set_xlim(0, 345); ax.set_ylim(0, 18.5)
    ax.set_xticks([0, 100, 200, 300]); ax.set_yticks([0, 5, 10, 15])
    ax.set_title("2  power vs. speed", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Power, MW")
    callout(ax, (175, TA0 * 175 / 1e6), "$P_A$, sea level", at=(145, 13.5), ha="right", fs=FS_SMALL, color=INK)
    callout(ax, (262, float(power_required(m, S, CD0, K, rho0, 262.0)) / 1e6), "$P_R$, sea level",
            at=(205, 17.0), ha="right", fs=FS_SMALL, color=INK)
    callout(ax, (282, TA14 * 282 / 1e6), "$P_A$\n14 km", at=(340, 12.0), ha="right", fs=FS_SMALL, color=BLUE)
    callout(ax, (268, float(power_required(m, S, CD0, K, rho14, 268.0)) / 1e6), "$P_R$, 14 km",
            at=(340, 2.2), ha="right", fs=FS_SMALL, color=BLUE)

    close_to(mt0["T_min"], mt14["T_min"], 1e-12, "minimum thrust required is independent of altitude")
    assert mt14["V"] > mt0["V"] and TA14 < TA0, "altitude shifts T_R right and drops T_A"
    save_figure(fig, "p51-altitude-jet")


def fig_altitude_prop():
    """Effect of altitude on the GA propeller aircraft (sea level and 6,000 m):
    P_R moves up and right while flat P_A falls, shrinking the excess power."""
    m, S, CD0, K = GA["m"], GA["S"], GA["CD0"], GA["K"]
    rho0 = RHO_SL
    rho6 = standard(GA_H_ALT)[2]
    PA0 = power_available(GA["n"], GA["P0"], GA["eta"], rho0, GA["m_ad"])
    PA6 = power_available(GA["n"], GA["P0"], GA["eta"], rho6, GA["m_ad"])
    mp0 = min_power_condition(m, S, CD0, K, rho0)
    mp6 = min_power_condition(m, S, CD0, K, rho6)
    vm0, _ = prop_vmax(m, S, CD0, K, rho0, PA0)
    vm6, _ = prop_vmax(m, S, CD0, K, rho6, PA6)

    V0 = np.linspace(stall_speed_mass(m, S, GA["CLmax"], rho0), 92.0, 400)
    V6 = np.linspace(stall_speed_mass(m, S, GA["CLmax"], rho6), 95.0, 400)

    fig, ax = data_axes(6.5, 4.0)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.14, top=0.96)
    ax.plot(V0, power_required(m, S, CD0, K, rho0, V0) / 1000.0, **line_kw(0), zorder=4)
    ax.plot(V6, power_required(m, S, CD0, K, rho6, V6) / 1000.0, **line_kw(1), zorder=4)
    ax.plot([20.0, 94.0], [PA0 / 1000.0, PA0 / 1000.0], color=INK, lw=1.4, ls=(0, (6, 2.5)), zorder=3)
    ax.plot([20.0, 94.0], [PA6 / 1000.0, PA6 / 1000.0], color=BLUE, lw=1.4, ls=(0, (2, 2)), zorder=3)

    ax.plot([mp0["V"]], [mp0["P_min"] / 1000.0], "o", ms=6.0, color=INK, zorder=6)
    ax.plot([mp6["V"]], [mp6["P_min"] / 1000.0], "o", ms=6.0, color=BLUE, zorder=6)
    ax.plot([vm0], [PA0 / 1000.0], "s", ms=6.0, mfc="white", mec=INK, mew=1.3, zorder=6)
    ax.plot([vm6], [PA6 / 1000.0], "s", ms=6.0, mfc="white", mec=BLUE, mew=1.3, zorder=6)

    ax.set_xlim(20, 98); ax.set_ylim(0, 210)
    ax.set_xticks([20, 35, 50, 65, 80, 95]); ax.set_yticks([0, 40, 80, 120, 160, 200])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Power, kW")

    text(ax, (38, PA0 / 1000.0), f"$P_A$, sea level ({fmt(PA0 / 1000.0, 4)} kW)",
         direction=90, dist=5, fs=FS_SMALL, color=INK, ha="left")
    text(ax, (24, PA6 / 1000.0), f"$P_A$, 6,000 m ({fmt(PA6 / 1000.0, 4)} kW)",
         direction=90, dist=5, fs=FS_SMALL, color=BLUE, ha="left")
    text(ax, (74, 146.0), "$P_R$, sea level", fs=FS_SMALL, color=INK, ha="right")
    text(ax, (82, 74.0), "$P_R$, 6,000 m", fs=FS_SMALL, color=BLUE, ha="left")
    callout(ax, (mp0["V"], mp0["P_min"] / 1000.0), f"SL min: {fmt(mp0['P_min']/1000.0, 3)} kW",
            at=(23.0, 10.0), ha="left", fs=FS_SMALL)
    callout(ax, (mp6["V"], mp6["P_min"] / 1000.0), f"6 km min: {fmt(mp6['P_min']/1000.0, 3)} kW",
            at=(36.0, 98.0), ha="left", fs=FS_SMALL, color=BLUE)

    assert mp6["P_min"] > mp0["P_min"] and mp6["V"] > mp0["V"] and PA6 < PA0
    save_figure(fig, "p51-altitude-prop")


def make_all():
    fig_level_flight_fbd()
    fig_thrust_required()
    fig_power_required()
    fig_available_and_vmax()
    fig_altitude_jet()
    fig_altitude_prop()


# ===================================================================== printed values
def values():
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731
    m, S, CD0, K = GA["m"], GA["S"], GA["CD0"], GA["K"]
    r("ga-m", fmt(m, 4)); r("ga-S", fmt_dec(S, 1)); r("ga-CD0", fmt_dec(CD0, 3)); r("ga-K", fmt_dec(K, 3))
    r("ga-CLmax", fmt_dec(GA["CLmax"], 1)); r("ga-P0-kW", fmt(GA["P0"] / 1000.0, 3))
    r("ga-eta", fmt_dec(GA["eta"], 2)); r("ga-mad", fmt_dec(GA["m_ad"], 1))
    W_ga = r("ga-W", fmt(m * G0, 5))
    Wp = _num(W_ga)

    # Example 1a: V = 70 m/s at sea level
    r("ga-V1", fmt(GA_V1, 2))
    q1 = r("ga-q1", fmt(0.5 * RHO_SL * GA_V1 ** 2, 5))
    qS1 = r("ga-qS1", fmt(_num(q1) * S, 5))
    CL1 = r("ga-CL1", fmt(Wp / _num(qS1), 4))
    a1 = r("ga-alpha1", fmt((_num(CL1) - GA["CL0"]) / GA["CLa"], 3))
    CD1 = r("ga-CD1", fmt(CD0 + K * _num(CL1) ** 2, 4))
    D1 = r("ga-D1", fmt(_num(qS1) * _num(CD1), 4))
    r("ga-P1-kW", fmt(_num(D1) * GA_V1 / 1000.0, 4))
    r("ga-de1", fmt(-(GA["CP0"] + GA["CPa"] * _num(a1)) / GA["CPe"], 3))
    PA_sl = r("ga-PA-sl", fmt(GA["eta"] * GA["P0"] / 1000.0, 4))

    # Example 1b: alpha = 5 deg at sea level
    r("ga-alpha2", fmt_dec(GA_ALPHA2, 1))
    CL2 = r("ga-CL2", fmt_dec(GA["CL0"] + GA["CLa"] * GA_ALPHA2, 2))
    CD2 = r("ga-CD2", fmt(CD0 + K * _num(CL2) ** 2, 4))
    V2 = r("ga-V2", fmt(math.sqrt(2.0 * Wp / (RHO_SL * S * _num(CL2))), 4))
    LD2 = r("ga-LD2", fmt(_num(CL2) / _num(CD2), 4))
    T2 = r("ga-T2", fmt(Wp / _num(LD2), 4))
    r("ga-P2-kW", fmt(_num(T2) * _num(V2) / 1000.0, 4))

    # GA minimum thrust, minimum power, V_max at sea level and 6,000 m
    mp0 = min_power_condition(m, S, CD0, K, RHO_SL)
    mt0 = min_thrust_condition(m, S, CD0, K, RHO_SL)
    vp0, h_vp0 = prop_vmax(m, S, CD0, K, RHO_SL, _num(PA_sl) * 1000.0)
    r("ga-Vt-sl", fmt(mt0["V"], 4)); r("ga-Tmin", fmt(mt0["T_min"], 4))
    r("ga-Vp-sl", fmt(mp0["V"], 4)); r("ga-Pmin-sl", fmt(mp0["P_min"] / 1000.0, 4))
    r("ga-Pmin-sl-3", fmt(mp0["P_min"] / 1000.0, 3))
    r("ga-Vmax-sl-0", fmt(h_vp0[0], 4))
    r("ga-Vmax-sl-1", fmt(h_vp0[1], 4))
    r("ga-Vmax-sl-2", fmt(h_vp0[2], 4))
    r("ga-Vmax-sl", fmt(vp0, 4))
    r("ga-Vs-sl", fmt(stall_speed_mass(m, S, GA["CLmax"], RHO_SL), 4))

    # GA at 6,000 m
    rho6 = standard(GA_H_ALT)[2]
    r("ga-h6", fmt(GA_H_ALT, 4)); r("ga-rho6", fmt(rho6, 4))
    PA6 = power_available(GA["n"], GA["P0"], GA["eta"], rho6, GA["m_ad"])
    mp6 = min_power_condition(m, S, CD0, K, rho6)
    vm6, _ = prop_vmax(m, S, CD0, K, rho6, PA6)
    r("ga-PA6", fmt(PA6 / 1000.0, 4))
    r("ga-Vp6", fmt(mp6["V"], 4)); r("ga-Pmin6", fmt(mp6["P_min"] / 1000.0, 3))
    r("ga-Vmax6", fmt(vm6, 4))

    # Example 2: Executive twin-jet
    mj, Sj, CD0j, Kj = JET["m"], JET["S"], JET["CD0"], JET["K"]
    r("jet-m", fmt(mj, 5)); r("jet-S", fmt_dec(Sj, 1)); r("jet-CD0", fmt_dec(CD0j, 3)); r("jet-K", fmt_dec(Kj, 3))
    r("jet-T0-one", fmt(JET["T0"], 5)); r("jet-T0-tot", fmt(JET["n"] * JET["T0"], 5))
    Wj = r("jet-W", fmt(mj * G0, 6))
    Wjp = _num(Wj)
    mtj = min_thrust_condition(mj, Sj, CD0j, Kj, RHO_SL)
    mpj = min_power_condition(mj, Sj, CD0j, Kj, RHO_SL)
    TAj0 = JET["n"] * JET["T0"]
    _, vmj0 = jet_speed_bounds(mj, Sj, CD0j, Kj, RHO_SL, TAj0)
    a_sl = float(speed_of_sound(T_SL))
    r("jet-LDmax", fmt(mtj["LD_max"], 4))
    r("jet-Tmin", fmt(mtj["T_min"], 5)); r("jet-Tmin-kN", fmt(mtj["T_min"] / 1000.0, 4))
    r("jet-Vt-sl", fmt(mtj["V"], 4))
    r("jet-Vp-sl", fmt(mpj["V"], 4)); r("jet-Pmin-sl", fmt(mpj["P_min"] / 1000.0, 4))
    r("jet-TA-sl-kN", fmt(TAj0 / 1000.0, 4))
    r("jet-Vmax-sl", fmt(vmj0, 4)); r("jet-Mmax-sl", fmt(vmj0 / a_sl, 3))
    disc_j = TAj0 ** 2 - 4.0 * CD0j * Kj * Wjp ** 2
    r("jet-root-disc", fmt(math.sqrt(disc_j), 5))
    r("jet-den-sl", fmt(RHO_SL * Sj * CD0j, 5))
    for tag, h in (("10", JET_H_MID), ("14", JET_H_HI)):
        Th, _, rhoh = standard(h)
        ah = float(speed_of_sound(Th))
        TAh = thrust_available(JET["n"], JET["T0"], rhoh, JET["m_ad"])
        mth = min_thrust_condition(mj, Sj, CD0j, Kj, rhoh)
        _, vmh = jet_speed_bounds(mj, Sj, CD0j, Kj, rhoh, TAh)
        r(f"jet-h{tag}", fmt(h, 5)); r(f"jet-rho{tag}", fmt(rhoh, 4))
        r(f"jet-TA{tag}", fmt(TAh, 5)); r(f"jet-Vt{tag}", fmt(mth["V"], 4))
        r(f"jet-Vmax{tag}", fmt(vmh, 4)); r(f"jet-Mmax{tag}", fmt(vmh / ah, 3))
    r("speed-ratio", fmt(3.0 ** (-0.25), 4))
