"""Figures and values of 5.3 Climb and Ceiling (notes/chapter-5/climb-and-ceiling.md).

Worked examples (verified not in the problem bank or homework):
  - Example 1 (Twin-jet, executive jet of pages 5.1 and 5.2): m = 33,100 kg, S = 88.2 m^2,
    C_D,0 = 0.015, K = 0.050, n = 2, T_0 = 27,810 N per engine (55,620 N total), m_ad = 0.6.
    Sea-level climb at V = 125 m/s; one-engine-out obstacle check (75 m hill at 3,000 m);
    analytical absolute ceiling and graphical service ceiling from (R/C)_max vs. altitude.
  - Example 2 (Invented twin-turboprop survey aircraft): m = 11,200 kg, S = 44.0 m^2,
    C_D,0 = 0.024, K = 0.038, n = 2, P_0 = 1,150 kW per engine, eta = 0.81, m_ad = 0.85.
    Sea-level (R/C)_max, one-engine-out climb at V = 75 m/s over a 150 m mast at 2,400 m
    (does not clear!), and analytical absolute ceiling.
"""
from chapter_5.common import *

PAGE = "p53"

JET = dict(m=33100.0, S=88.2, CD0=0.015, K=0.050, n=2, T0=27810.0, m_ad=0.6,
           V_cl=125.0, d_obs=3000.0, h_obs=75.0)
PROP = dict(m=11200.0, S=44.0, CD0=0.024, K=0.038, n=2, P0=1150e3, eta=0.81, m_ad=0.85,
            V_oei=75.0, d_obs=2400.0, h_obs=150.0)
CEIL_ALTS = (0.0, 4000.0, 8000.0, 11000.0, 13000.0, 14500.0)


def _num(s):
    return float(s.replace(",", "").replace("−", "-"))


# ===================================================================== figures
def fig_climb_fbd():
    """Steady unaccelerated climb: aircraft pitched along flight path at angle gamma,
    showing L, D, T, weight mg resolved into mg cos(gamma) and mg sin(gamma), plus a small
    velocity triangle inset showing V_h = V cos(gamma) and R/C = V sin(gamma)."""
    fig, ax = canvas(6.5, xlim=(-2.30, 3.85), ylim=(-1.75, 1.85))
    gam = 20.0   # exaggerated for readability (caption states this)
    ac = aircraft_silhouette_right(ax, center=(0.0, 0.0), length=2.25, pitch_deg=gam, fill=PART_FILL)
    cg = ac["cg"]
    cg_symbol(ax, cg, size=10.0)

    # Horizontal reference and flight path
    line(ax, (-1.95, 0.0), (2.05, 0.0), role="reference", zorder=1.5)
    fp_fwd = ray(ax, cg, gam, 2.08, role="boundary", zorder=2.0)
    fp_aft = ray(ax, cg, 180.0 + gam, 1.88, role="boundary", zorder=2.0)
    ray(ax, cg, gam - 90.0, 1.55, role="reference", zorder=1.5)

    angle_mark(ax, cg, 0.0, gam, 1.25, r"$\gamma$", stated=gam, label_r=1.48, fs=FS_LABEL)
    angle_mark(ax, cg, -90.0, gam - 90.0, 0.88, r"$\gamma$", stated=gam, label_r=1.10, fs=FS_LABEL)

    u_p = unit(gam)
    u_n = unit(gam + 90.0)
    L_tip = cg + 1.48 * u_n
    T_tip = cg + 1.75 * u_p
    D_tip = cg - 1.50 * u_p
    W_len = 1.48
    W_tip = cg + np.array([0.0, -W_len])
    Wn_tip = cg - W_len * math.cos(math.radians(gam)) * u_n
    Wp_tip = cg - W_len * math.sin(math.radians(gam)) * u_p

    kind_arrow(ax, cg + 0.14 * u_n, L_tip, "force", "lift, $L$", label_dir=105, dist=5)
    rides_on(kind_arrow(ax, cg + 0.14 * u_p, T_tip, "force", None), fp_fwd)
    text(ax, T_tip, "thrust, $T$", direction=115, dist=13, fs=FS_LABEL)
    rides_on(kind_arrow(ax, cg - 0.14 * u_p, D_tip, "force", None), fp_aft)
    text(ax, D_tip, "drag, $D$", direction=115, dist=10, fs=FS_LABEL)
    kind_arrow(ax, cg + np.array([0.0, -0.14]), W_tip, "force", "weight, $mg$", label_dir=-110, dist=6)

    dash = dict(color=GRAY, lw=LW_THIN, ls=(0, (3.0, 2.0)), zorder=2.0)
    ax.plot([Wn_tip[0], W_tip[0]], [Wn_tip[1], W_tip[1]], **dash)
    ax.plot([Wp_tip[0], W_tip[0]], [Wp_tip[1], W_tip[1]], **dash)
    text(ax, Wn_tip, r"$mg\cos\gamma$", direction=-10, dist=8, fs=FS_SMALL, color=STEEL)
    callout(ax, 0.5 * (cg + Wp_tip), r"$mg\sin\gamma$", at=(-1.85, -1.20), ha="left", fs=FS_SMALL, color=STEEL)
    text(ax, (1.58, 0.0), "horizontal", direction=-90, dist=6, fs=FS_SMALL, color=STEEL)

    # Velocity triangle on the right
    vo = np.array([2.25, -0.60])
    vlen = 1.42
    vh = vo + np.array([vlen * math.cos(math.radians(gam)), 0.0])
    vt = vo + vlen * u_p
    grp = "grp:vtri"
    kind_arrow(ax, vo, vt, "velocity", None).set_gid(grp)
    kind_arrow(ax, vo, vh, "velocity", None, lw=1.2, head="small").set_gid(grp)
    kind_arrow(ax, vh, vt, "velocity", None, lw=1.2, head="small").set_gid(grp)
    angle_mark(ax, vo, 0.0, gam, 0.58, r"$\gamma$", stated=gam, label_r=0.78, fs=FS_SMALL, color=BLUE)
    text(ax, 0.5 * (vo + vt), "$V$", direction=115, dist=7, fs=FS_LABEL, color=BLUE)
    text(ax, 0.5 * (vo + vh), r"$V\cos\gamma$", direction=-90, dist=7, fs=FS_SMALL, color=BLUE)
    text(ax, 0.5 * (vh + vt), "$R/C =$\n$V\\sin\\gamma$", direction=0, dist=6, fs=FS_SMALL, color=BLUE, ha="left")
    text(ax, (2.92, 0.55), "velocity triangle", fs=FS_SMALL, color=BLUE)

    legend_key(ax, (-2.22, 1.66), [("force", "force"), ("velocity", "velocity")], dy=18, fs=FS_SMALL)
    close_to(float(np.dot(L_tip - cg, T_tip - cg)), 0.0, 1e-12, "lift perpendicular to flight path")
    trim_canvas(fig)
    save_figure(fig, "p53-climb-fbd")


def fig_excess_power():
    """Executive jet at sea level: P_A = T_A V and P_R against V, with excess power shaded and
    the speeds of maximum rate of climb (largest P_A - P_R) and maximum climb angle (V_TR,min)
    marked separately."""
    m, S, CD0, K = JET["m"], JET["S"], JET["CD0"], JET["K"]
    TA = thrust_available(JET["n"], JET["T0"], RHO_SL, JET["m_ad"])
    _, vmax = jet_speed_bounds(m, S, CD0, K, RHO_SL, TA)
    mt = min_thrust_condition(m, S, CD0, K, RHO_SL)
    rc = jet_max_roc(m, S, CD0, K, RHO_SL, TA)

    V = np.linspace(68.0, 270.0, 500)
    PR = power_required(m, S, CD0, K, RHO_SL, V) / 1e6
    PA = TA * V / 1e6

    fig, ax = data_axes(6.5, 4.1)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.14, top=0.96)
    mask = (V >= 72.0) & (V <= vmax)
    ax.fill_between(V[mask], PR[mask], PA[mask], color=HIGHLIGHT, lw=0, zorder=1)
    ax.plot(V, PR, **line_kw(0), zorder=4)
    ax.plot(V, PA, **line_kw(1), zorder=4)

    vrc = rc["V"]
    p_a_rc, p_r_rc = rc["P_A"] / 1e6, rc["P_R"] / 1e6
    dimension(ax, (vrc, p_r_rc), (vrc, p_a_rc), None, ticks=False, extension=False, zorder=5)
    ax.plot([vrc, vrc], [p_r_rc, p_a_rc], "o", ms=5.5, color=INK, zorder=6)

    vt = mt["V"]
    p_r_vt = mt["P_at_Tmin"] / 1e6
    p_a_vt = TA * vt / 1e6
    ax.plot([vt, vt], [0.0, p_a_vt], **line_kw("boundary"), zorder=3)
    ax.plot([vt], [p_r_vt], "s", ms=5.5, mfc="white", mec=INK, mew=1.3, zorder=6)

    ax.set_xlim(60, 275); ax.set_ylim(0, 16.8)
    ax.set_xticks([60, 100, 140, 180, 220, 260]); ax.set_yticks([0, 4, 8, 12, 16])
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Power, MW")

    text(ax, (212, 13.8), "$P_A = T_A V$", direction=115, dist=6, fs=FS_LABEL, color=BLUE)
    text(ax, (240, 8.6), "$P_R$", direction=-45, dist=8, fs=FS_LABEL, color=INK)
    callout(ax, (vrc, p_a_rc),
            f"largest excess power:\n$(R/C)_\\max$ = {fmt(rc['RC_max'], 4)} m/s\nat {fmt(vrc, 4)} m/s",
            at=(68.0, 13.4), ha="left", fs=FS_LABEL)
    callout(ax, (vt, 1.3),
            f"$V_{{\\gamma,\\max}} = V_{{T_R,\\min}}$ = {fmt(vt, 4)} m/s",
            at=(148.0, 1.3), ha="left", fs=FS_LABEL)
    assert vrc > vt, "jet best R/C speed is higher than best climb-angle speed"
    save_figure(fig, "p53-excess-power")


def fig_climb_angle_and_roc():
    """Executive jet at sea level: all engines (2) vs. one engine out (1).
    Panel 1: climb angle gamma vs V (peaks at V_TR,min); Panel 2: R/C vs V (peaks higher)."""
    m, S, CD0, K = JET["m"], JET["S"], JET["CD0"], JET["K"]
    TA2 = thrust_available(2, JET["T0"], RHO_SL, JET["m_ad"])
    TA1 = thrust_available(1, JET["T0"], RHO_SL, JET["m_ad"])
    V = np.linspace(68.0, 265.0, 500)
    c2 = climb_jet(m, S, CD0, K, RHO_SL, TA2, V)
    c1 = climb_jet(m, S, CD0, K, RHO_SL, TA1, V)

    g2 = jet_max_climb_angle(m, S, CD0, K, RHO_SL, TA2)
    g1 = jet_max_climb_angle(m, S, CD0, K, RHO_SL, TA1)
    r2 = jet_max_roc(m, S, CD0, K, RHO_SL, TA2)
    r1 = jet_max_roc(m, S, CD0, K, RHO_SL, TA1)

    fig, axs = data_axes(6.5, 3.8, ncols=2)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.15, top=0.90, wspace=0.34)

    ax = axs[0]
    ax.axhline(0.0, color=GRAY, lw=LW_THIN, zorder=1.5)
    ax.plot(V, c2["gamma_deg"], **line_kw(0), zorder=4)
    ax.plot(V, c1["gamma_deg"], **line_kw(1), zorder=4)
    ax.plot([g2["V"]], [g2["gamma_deg"]], "o", ms=6.0, color=INK, zorder=6)
    ax.plot([g1["V"]], [g1["gamma_deg"]], "s", ms=5.5, color=BLUE, zorder=6)
    ax.set_xlim(65, 265); ax.set_ylim(-2.5, 8.8)
    ax.set_xticks([80, 140, 200, 260]); ax.set_yticks([-2, 0, 2, 4, 6, 8])
    ax.set_title("1  climb angle", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Climb angle, $\\gamma$, deg")
    text(ax, (g2["V"], g2["gamma_deg"]), f"2 engines: {fmt(g2['gamma_deg'], 3)}°",
         direction=45, dist=7, fs=FS_SMALL, color=INK, ha="left")
    text(ax, (g1["V"], g1["gamma_deg"]), f"1 engine: {fmt(g1['gamma_deg'], 3)}°",
         direction=35, dist=8, fs=FS_SMALL, color=BLUE, ha="left")

    ax = axs[1]
    ax.axhline(0.0, color=GRAY, lw=LW_THIN, zorder=1.5)
    ax.plot(V, c2["RC"], **line_kw(0), zorder=4)
    ax.plot(V, c1["RC"], **line_kw(1), zorder=4)
    ax.plot([r2["V"]], [r2["RC_max"]], "o", ms=6.0, color=INK, zorder=6)
    ax.plot([r1["V"]], [r1["RC_max"]], "s", ms=5.5, color=BLUE, zorder=6)
    ax.set_xlim(65, 265); ax.set_ylim(-6, 20.5)
    ax.set_xticks([80, 140, 200, 260]); ax.set_yticks([-5, 0, 5, 10, 15, 20])
    ax.set_title("2  rate of climb", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Rate of climb, $R/C$, m/s")
    text(ax, (r2["V"], r2["RC_max"]), f"2 engines:\n{fmt(r2['RC_max'], 4)} m/s",
         direction=135, dist=7, fs=FS_SMALL, color=INK, ha="right")
    text(ax, (r1["V"], r1["RC_max"]), f"1 engine:\n{fmt(r1['RC_max'], 3)} m/s",
         direction=70, dist=8, fs=FS_SMALL, color=BLUE, ha="left")

    close_to(float(V[np.argmax(c2["gamma_deg"])]), g2["V"], 0.6, "gamma peak at V_TR,min")
    assert r2["V"] > g2["V"] and r1["V"] > g1["V"]
    save_figure(fig, "p53-climb-angle-and-roc")


def fig_obstacle_clearance():
    """Executive jet one-engine-out obstacle clearance over 3,000 m: steepest climb at gamma_max
    clears the 75 m hill with margin; a shallower climb at 145 m/s strikes it."""
    m, S, CD0, K = JET["m"], JET["S"], JET["CD0"], JET["K"]
    TA1 = JET["T0"]
    g_best = jet_max_climb_angle(m, S, CD0, K, RHO_SL, TA1)
    V_fast = 145.0
    c_fast = climb_jet(m, S, CD0, K, RHO_SL, TA1, V_fast)
    d_obs, h_obs = JET["d_obs"], JET["h_obs"]

    xs = np.array([0.0, d_obs + 400.0])
    y_best = xs * math.tan(math.radians(g_best["gamma_deg"]))
    y_fast = xs * math.tan(math.radians(float(c_fast["gamma_deg"])))
    h_gain_best = d_obs * math.tan(math.radians(g_best["gamma_deg"]))
    h_gain_fast = d_obs * math.tan(math.radians(float(c_fast["gamma_deg"])))

    fig, ax = data_axes(6.5, 3.6)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.16, top=0.95)
    w_obs = 180.0
    obs = Polygon([(d_obs - 0.5 * w_obs, 0.0), (d_obs - 0.15 * w_obs, h_obs),
                   (d_obs + 0.15 * w_obs, h_obs), (d_obs + 0.5 * w_obs, 0.0)],
                  closed=True, fc="#D5D5D5", ec=INK, lw=1.2, hatch="///", zorder=3)
    ax.add_patch(opaque(obs))

    ax.plot(xs, y_best, **line_kw(0), zorder=4)
    ax.plot(xs, y_fast, **line_kw(2), zorder=4)
    ax.plot([d_obs], [h_gain_best], "o", ms=6.0, color=INK, zorder=6)
    ax.plot([d_obs], [h_gain_fast], "s", ms=5.5, mfc="white", mec=text_color(2), mew=1.4, zorder=6)

    ax.set_xlim(0, 3650); ax.set_ylim(0, 128)
    ax.set_xticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500])
    ax.set_yticks([0, 25, 50, 75, 100, 125])
    ax.set_xlabel("Horizontal distance from liftoff, m")
    ax.set_ylabel("Height gained, m")

    text(ax, (1050, 66.0),
         f"steepest climb, $\\gamma_\\max$ = {fmt(g_best['gamma_deg'], 3)}°",
         fs=FS_LABEL, color=INK, ha="center")
    text(ax, (1750, 12.0),
         f"faster climb (145 m/s), $\\gamma$ = {fmt(float(c_fast['gamma_deg']), 3)}°",
         fs=FS_SMALL, color=text_color(2), ha="center")
    callout(ax, (d_obs, h_gain_best), f"clears at {fmt(h_gain_best, 3)} m",
            at=(1920, 112.0), ha="left", fs=FS_SMALL)
    callout(ax, (d_obs + 55, 36.0), f"obstacle,\n{fmt(h_obs, 2)} m",
            at=(3190, 26.0), ha="left", fs=FS_SMALL)

    assert h_gain_best > h_obs and h_gain_fast < h_obs
    save_figure(fig, "p53-obstacle-clearance")


def fig_ceiling_plot():
    """Two-panel ceiling figure:
    Panel 1: (R/C)_max vs altitude for the executive jet, marking service ceiling (0.5 m/s)
             and absolute ceiling (0 m/s).
    Panel 2: Why the ceiling exists for a propeller aircraft (Example 2): P_A,max falls while
             P_R,min rises with altitude, meeting at the absolute ceiling."""
    fig, axs = data_axes(6.5, 3.9, ncols=2)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.15, top=0.87, wspace=0.35)

    # Panel 1: Jet (R/C)_max vs altitude
    ax = axs[0]
    m, S, CD0, K = JET["m"], JET["S"], JET["CD0"], JET["K"]
    rc_of_h = lambda h: jet_max_roc(m, S, CD0, K, standard(h)[2],
                                    thrust_available(JET["n"], JET["T0"], standard(h)[2], JET["m_ad"]))["RC_max"]
    h_abs = jet_absolute_ceiling(m, CD0, K, JET["n"], JET["T0"], JET["m_ad"])["h_abs"]
    h_srv = ceiling_by_bisection(rc_of_h, SERVICE_CEILING_RC)

    hs = np.linspace(0.0, h_abs, 120)
    rcs = np.array([rc_of_h(h) for h in hs])
    ax.plot(rcs, hs / 1000.0, **line_kw(0), zorder=4)
    t_rc = [rc_of_h(h) for h in CEIL_ALTS]
    ax.plot(t_rc, np.array(CEIL_ALTS) / 1000.0, "o", ms=5.0, mfc="white", mec=INK, mew=1.3, zorder=5)
    ax.axvline(SERVICE_CEILING_RC, **line_kw("boundary"), zorder=2)
    ax.axhline(h_srv / 1000.0, color=BLUE, lw=1.0, ls=(0, (4, 2.5)), zorder=2)
    ax.axhline(h_abs / 1000.0, color=STEEL, lw=1.0, ls=(0, (1.5, 2)), zorder=2)
    ax.plot([SERVICE_CEILING_RC], [h_srv / 1000.0], "s", ms=6.0, color=BLUE, zorder=6)
    ax.plot([0.0], [h_abs / 1000.0], "D", ms=6.0, color=INK, zorder=6)

    ax.set_xlim(-0.5, 19.0); ax.set_ylim(0, 18.2)
    ax.set_xticks([0, 5, 10, 15]); ax.set_yticks([0, 4, 8, 12, 16])
    ax.set_title("1  jet ceilings from $(R/C)_\\max$", fontsize=FS_LABEL, loc="left", pad=10)
    ax.set_xlabel("Max rate of climb, $(R/C)_\\max$, m/s"); ax.set_ylabel("Altitude, $h$, km")
    text(ax, (3.2, h_abs / 1000.0), f"absolute: {fmt(h_abs / 1000.0, 4)} km",
         direction=90, dist=5, fs=FS_SMALL, color=INK, ha="left")
    text(ax, (4.8, h_srv / 1000.0), f"service: {fmt(h_srv / 1000.0, 4)} km",
         direction=-90, dist=7, fs=FS_SMALL, color=BLUE, ha="left")

    # Panel 2: Propeller aircraft P_A,max and P_R,min vs altitude
    ax = axs[1]
    mp_, Sp, CD0p, Kp = PROP["m"], PROP["S"], PROP["CD0"], PROP["K"]
    pc = prop_absolute_ceiling(mp_, Sp, CD0p, Kp, PROP["n"], PROP["P0"], PROP["eta"], PROP["m_ad"])
    hp = np.linspace(0.0, 11500.0, 120)
    rhos = standard(hp)[2]
    PA_kW = power_available(PROP["n"], PROP["P0"], PROP["eta"], rhos, PROP["m_ad"]) / 1000.0
    PRmin_kW = np.array([min_power_condition(mp_, Sp, CD0p, Kp, r_)["P_min"] / 1000.0 for r_ in rhos])
    ax.plot(hp / 1000.0, PA_kW, **line_kw(1), zorder=4)
    ax.plot(hp / 1000.0, PRmin_kW, **line_kw(0), zorder=4)
    ax.plot([pc["h_abs"] / 1000.0], [pc["P_ceil"] / 1000.0], "D", ms=6.5, color=INK, zorder=6)
    ax.plot([pc["h_abs"] / 1000.0, pc["h_abs"] / 1000.0], [0.0, pc["P_ceil"] / 1000.0],
            **line_kw("boundary"), zorder=2)

    ax.set_xlim(0, 12.0); ax.set_ylim(0, 2100)
    ax.set_xticks([0, 3, 6, 9, 12]); ax.set_yticks([0, 500, 1000, 1500, 2000])
    ax.set_title("2  propeller: $P_A$ meets $P_{R,\\min}$", fontsize=FS_LABEL, loc="left", pad=10)
    ax.set_xlabel("Altitude, $h$, km"); ax.set_ylabel("Power, kW")
    text(ax, (5.0, 1680), "$P_{A,\\max}$", fs=FS_LABEL, color=BLUE)
    text(ax, (3.4, 240), "$P_{R,\\min}$", fs=FS_LABEL, color=INK)
    callout(ax, (pc["h_abs"] / 1000.0, pc["P_ceil"] / 1000.0),
            f"ceiling,\n{fmt(pc['h_abs'] / 1000.0, 4)} km", at=(6.0, 1340), ha="left", fs=FS_SMALL)

    assert h_abs > h_srv and pc["h_abs"] > 9000.0
    save_figure(fig, "p53-ceiling-plot")


def make_all():
    fig_climb_fbd()
    fig_excess_power()
    fig_climb_angle_and_roc()
    fig_obstacle_clearance()
    fig_ceiling_plot()


# ===================================================================== printed values
def values():
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731
    m, S, CD0, K = JET["m"], JET["S"], JET["CD0"], JET["K"]
    r("jet-m", fmt(m, 5)); r("jet-S", fmt_dec(S, 1)); r("jet-CD0", fmt_dec(CD0, 3)); r("jet-K", fmt_dec(K, 3))
    r("jet-T0", fmt(JET["T0"], 5)); r("jet-T0-tot", fmt(JET["n"] * JET["T0"], 5))
    r("jet-mad", fmt_dec(JET["m_ad"], 1))
    W = r("jet-W", fmt(m * G0, 6)); Wp = _num(W)

    Vcl = JET["V_cl"]
    r("jet-Vcl", fmt(Vcl, 3))
    D0 = r("jet-D0-cl", fmt(0.5 * RHO_SL * Vcl ** 2 * S * CD0, 5))
    Di = r("jet-Di-cl", fmt(2.0 * K * Wp ** 2 / (RHO_SL * S * Vcl ** 2), 5))
    Dcl = r("jet-D-cl", fmt(_num(D0) + _num(Di), 5))
    PR_cl = r("jet-PR-cl", fmt(_num(Dcl) * Vcl / 1000.0, 4))
    PA_cl = r("jet-PA-cl", fmt(JET["n"] * JET["T0"] * Vcl / 1000.0, 4))
    RC_cl = r("jet-RC-cl", fmt((_num(PA_cl) - _num(PR_cl)) * 1000.0 / Wp, 4))
    sg_cl = r("jet-sg-cl", fmt(_num(RC_cl) / Vcl, 4))
    r("jet-gam-cl", fmt(math.degrees(math.asin(_num(sg_cl))), 3))

    TA2 = JET["n"] * JET["T0"]
    TA1 = JET["T0"]
    g2 = jet_max_climb_angle(m, S, CD0, K, RHO_SL, TA2)
    r2 = jet_max_roc(m, S, CD0, K, RHO_SL, TA2)
    g1 = jet_max_climb_angle(m, S, CD0, K, RHO_SL, TA1)
    r1 = jet_max_roc(m, S, CD0, K, RHO_SL, TA1)
    r("jet-g2max", fmt(g2["gamma_deg"], 3))
    r("jet-r2max", fmt(r2["RC_max"], 4)); r("jet-Vr2", fmt(r2["V"], 4))
    r("jet-r1max", fmt(r1["RC_max"], 3))

    r("jet-dobs", fmt(JET["d_obs"], 4)); r("jet-hobs", fmt(JET["h_obs"], 2))
    TW1 = r("jet-TW1", fmt(TA1 / Wp, 4))
    invLD = r("jet-invLD", fmt(2.0 * math.sqrt(K * CD0), 4))
    sg1 = r("jet-sg1", fmt(_num(TW1) - _num(invLD), 4))
    gam1 = r("jet-gam1", fmt(math.degrees(math.asin(_num(sg1))), 3))
    r("jet-Vgam1", fmt(g1["V"], 4))
    r("jet-hgain", fmt(JET["d_obs"] * math.tan(math.radians(_num(gam1))), 3))
    r("jet-gamreq", fmt(math.degrees(math.atan(JET["h_obs"] / JET["d_obs"])), 3))
    c_fast = climb_jet(m, S, CD0, K, RHO_SL, TA1, 145.0)
    r("jet-gam-fast", fmt(float(c_fast["gamma_deg"]), 3))
    r("jet-hgain-fast", fmt(JET["d_obs"] * math.tan(math.radians(float(c_fast["gamma_deg"]))), 3))

    Tmin_j = r("jet-Tmin", fmt(2.0 * Wp * math.sqrt(K * CD0), 5))
    ratio_c = r("jet-ceil-rat", fmt(_num(Tmin_j) / TA2, 4))
    r("jet-rhoc", fmt(RHO_SL * (_num(ratio_c) ** (1.0 / JET["m_ad"])), 4))
    jc = jet_absolute_ceiling(m, CD0, K, JET["n"], JET["T0"], JET["m_ad"])
    r("jet-habs-m", fmt(jc["h_abs"], 5)); r("jet-habs-km", fmt(jc["h_abs"] / 1000.0, 4))

    rc_of_h = lambda h: jet_max_roc(m, S, CD0, K, standard(h)[2],
                                    thrust_available(JET["n"], JET["T0"], standard(h)[2], JET["m_ad"]))["RC_max"]
    rows = []
    for h in CEIL_ALTS:
        rc_v = rc_of_h(h)
        r(f"tbl-rc-{int(h)}", fmt_dec(rc_v, 2))
        rows.append((h, float(fmt_dec(rc_v, 2))))
    h_srv = ceiling_by_bisection(rc_of_h, SERVICE_CEILING_RC)
    r("jet-hsrv-km", fmt(h_srv / 1000.0, 4))
    (h1, rc1), (h2, rc2) = rows[-2], rows[-1]
    slope = (rc2 - rc1) / (h2 - h1)
    h_srv_lin = h1 + (SERVICE_CEILING_RC - rc1) / slope
    h_abs_lin = h2 + (0.0 - rc2) / slope
    r("jet-hsrv-lin", fmt(h_srv_lin, 5))
    r("jet-habs-lin", fmt(h_abs_lin, 5))

    mp_, Sp, CD0p, Kp = PROP["m"], PROP["S"], PROP["CD0"], PROP["K"]
    r("prop-m", fmt(mp_, 5)); r("prop-S", fmt_dec(Sp, 1)); r("prop-CD0", fmt_dec(CD0p, 3)); r("prop-K", fmt_dec(Kp, 3))
    r("prop-P0-kW", fmt(PROP["P0"] / 1000.0, 4)); r("prop-eta", fmt_dec(PROP["eta"], 2)); r("prop-mad", fmt_dec(PROP["m_ad"], 2))
    Wp2 = r("prop-W", fmt(mp_ * G0, 6)); Wp2v = _num(Wp2)
    PA2_kW = r("prop-PA2", fmt(PROP["n"] * PROP["eta"] * PROP["P0"] / 1000.0, 4))
    mp_sl = min_power_condition(mp_, Sp, CD0p, Kp, RHO_SL)
    r("prop-Vp", fmt(mp_sl["V"], 4))
    Pmin_sl = r("prop-Pmin", fmt(mp_sl["P_min"] / 1000.0, 4))
    r("prop-RCmax", fmt((_num(PA2_kW) - _num(Pmin_sl)) * 1000.0 / Wp2v, 4))

    Voei = PROP["V_oei"]
    r("prop-Voei", fmt(Voei, 2)); r("prop-dobs", fmt(PROP["d_obs"], 4)); r("prop-hobs", fmt(PROP["h_obs"], 3))
    PA1_kW = r("prop-PA1", fmt(PROP["eta"] * PROP["P0"] / 1000.0, 4))
    TA1_p = r("prop-TA1", fmt(_num(PA1_kW) * 1000.0 / Voei, 5))
    D0_p = r("prop-D0-oei", fmt(0.5 * RHO_SL * Voei ** 2 * Sp * CD0p, 4))
    Di_p = r("prop-Di-oei", fmt(2.0 * Kp * Wp2v ** 2 / (RHO_SL * Sp * Voei ** 2), 4))
    D_p = r("prop-D-oei", fmt(_num(D0_p) + _num(Di_p), 4))
    sg_p = r("prop-sg-oei", fmt((_num(TA1_p) - _num(D_p)) / Wp2v, 4))
    gam_p = r("prop-gam-oei", fmt(math.degrees(math.asin(_num(sg_p))), 3))
    r("prop-hgain", fmt(PROP["d_obs"] * math.tan(math.radians(_num(gam_p))), 4))
    r("prop-gamreq", fmt(math.degrees(math.atan(PROP["h_obs"] / PROP["d_obs"])), 3))

    pc = prop_absolute_ceiling(mp_, Sp, CD0p, Kp, PROP["n"], PROP["P0"], PROP["eta"], PROP["m_ad"])
    r("prop-rhoc", fmt(pc["rho_ceil"], 4))
    r("prop-habs-m", fmt(pc["h_abs"], 5)); r("prop-habs-km", fmt(pc["h_abs"] / 1000.0, 4))
    r("prop-Pceil", fmt(pc["P_ceil"] / 1000.0, 4))
