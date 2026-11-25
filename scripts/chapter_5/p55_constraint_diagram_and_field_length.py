"""Figures and values of Constraint diagram and field length
(notes/chapter-5/constraint-diagram-and-field-length.md; no course standard assessed).

Worked example: invented twin-jet utility and medical transport (distinct from all bank,
homework, and lecture-insert numbers):
  m = 6,200 kg, C_D,0 = 0.023, AR = 8.4, e = 0.82, C_L,max,TO = 1.95, C_L,max,L = 2.25,
  mu_r = 0.40, m_ad = 0.80.
  Requirements: V_stall <= 48 m/s (flaps down, sea level), s_LO <= 780 m, s_L <= 680 m,
  R/C >= 13 m/s at 92 m/s (sea level), cruise 210 m/s at 10,000 m, service ceiling 12,000 m.
"""
from chapter_5.common import *

PAGE = "p55"

EX = dict(m=6200.0, CD0=0.023, AR=8.4, e=0.82, CL_TO=1.95, CL_L=2.25, mu_r=0.40, m_ad=0.80)
REQ = dict(Vs=48.0, s_LO=780.0, s_L=680.0, RC=13.0, V_cl=92.0, h_cr=10000.0, V_cr=210.0,
           h_ceil=12000.0, RC_ceil=0.5)


def _num(s):
    return float(s.replace(",", "").replace("−", "-"))


def _design_point():
    K = polar_K(EX["AR"], EX["e"])
    W = EX["m"] * G0
    WS_st = 0.5 * RHO_SL * REQ["Vs"] ** 2 * EX["CL_L"]
    WS_la = REQ["s_L"] * G0 * RHO_SL * EX["CL_L"] * EX["mu_r"] / 1.69
    WS_des = min(WS_st, WS_la)
    rho_cr = standard(REQ["h_cr"])[2]
    rho_ce = standard(REQ["h_ceil"])[2]
    lines = dict(
        takeoff=float(tw_takeoff_line(WS_des, REQ["s_LO"], EX["CL_TO"])),
        climb=float(tw_climb_line(WS_des, REQ["RC"], REQ["V_cl"], EX["CD0"], K)),
        cruise=float(tw_cruise_line(WS_des, REQ["V_cr"], EX["CD0"], K, rho_cr, m_ad=EX["m_ad"])),
        ceiling=float(tw_ceiling_line(WS_des, REQ["RC_ceil"], EX["CD0"], K, rho_ce, m_ad=EX["m_ad"])),
    )
    TW_des = max(lines.values())
    S_des = W / WS_des
    T_des = TW_des * W
    return dict(K=K, W=W, WS_st=WS_st, WS_la=WS_la, WS_des=WS_des, TW_des=TW_des,
                S_des=S_des, T_des=T_des, lines=lines, rho_cr=rho_cr, rho_ce=rho_ce)


# ===================================================================== figures
def fig_takeoff_landing_phases():
    """Two-panel side-view schematic of takeoff (ground roll s_LO to V_LO = 1.2 V_stall,
    then air distance over a 15 m obstacle) and landing (approach over a 15 m obstacle,
    touchdown at V_T = 1.3 V_stall, braking ground roll s_L)."""
    fig, axs = new_axes(6.5, 4.4, nrows=2, equal=True)
    fig.subplots_adjust(left=0.03, right=0.97, bottom=0.04, top=0.95, hspace=0.22)

    # Panel 1: Takeoff
    ax = axs[0]
    ax.set_xlim(-0.2, 6.3); ax.set_ylim(-0.68, 1.48)
    text(ax, (-0.15, 1.30), "1  takeoff", fs=FS_LABEL, ha="left", backing=False)
    g1 = ax.plot([0.0, 5.95], [0.0, 0.0], color=GRAY, lw=1.0, zorder=1.5)[0]
    xs_to = np.r_[np.linspace(0.3, 3.6, 20), np.linspace(3.6, 5.65, 40)]
    ys_to = np.r_[np.zeros(20), 0.78 * ((np.linspace(0.0, 1.0, 40)) ** 1.35)]
    ln = ax.plot(xs_to, ys_to, **line_kw(0), zorder=4)[0]
    for h in motion_heads(ax, xs_to, ys_to, (0.28, 0.85), line=ln):
        rides_on(h, ln, g1)
    ax.plot([5.65, 5.65], [0.0, 0.78], color=INK, lw=1.4, zorder=3)
    text(ax, (5.65, 0.39), "15 m\nobstacle", direction=0, dist=5, fs=FS_SMALL, ha="left")
    ax.plot([0.3, 3.6], [0.0, 0.0], "o", ms=5.5, color=INK, zorder=6)
    text(ax, (0.3, 0.0), "brake\nrelease", direction=90, dist=8, fs=FS_SMALL)
    callout(ax, (3.6, 0.03), "liftoff, $V_{\\mathrm{LO}} = 1.2\\,V_{\\mathrm{stall}}$",
            at=(3.15, 0.65), ha="right", fs=FS_LABEL)
    dimension(ax, (0.3, -0.34), (3.6, -0.34), None, ticks=True, extension=False)
    text(ax, (1.95, -0.34), "ground roll, $s_{\\mathrm{LO}}$", direction=-90, dist=5, fs=FS_LABEL)
    dimension(ax, (3.6, -0.34), (5.65, -0.34), None, ticks=True, extension=False)
    text(ax, (4.62, -0.34), "air distance", direction=-90, dist=5, fs=FS_SMALL)

    # Panel 2: Landing
    ax = axs[1]
    ax.set_xlim(-0.2, 6.3); ax.set_ylim(-0.68, 1.48)
    text(ax, (-0.15, 1.30), "2  landing", fs=FS_LABEL, ha="left", backing=False)
    g2 = ax.plot([0.0, 5.95], [0.0, 0.0], color=GRAY, lw=1.0, zorder=1.5)[0]
    xs_la = np.r_[np.linspace(0.35, 2.35, 40), np.linspace(2.35, 5.65, 20)]
    ys_la = np.r_[0.78 * ((1.0 - np.linspace(0.0, 1.0, 40)) ** 1.35), np.zeros(20)]
    ln2 = ax.plot(xs_la, ys_la, **line_kw(0), zorder=4)[0]
    for h in motion_heads(ax, xs_la, ys_la, (0.16, 0.72), line=ln2):
        rides_on(h, ln2, g2)
    ax.plot([0.35, 0.35], [0.0, 0.78], color=INK, lw=1.4, zorder=3)
    text(ax, (0.35, 0.39), "15 m", direction=180, dist=5, fs=FS_SMALL, ha="right")
    ax.plot([2.35, 5.65], [0.0, 0.0], "o", ms=5.5, color=INK, zorder=6)
    callout(ax, (2.35, 0.03), "touchdown, $V_T = 1.3\\,V_{\\mathrm{stall}}$",
            at=(2.80, 0.65), ha="left", fs=FS_LABEL)
    text(ax, (5.65, 0.0), "stop", direction=90, dist=8, fs=FS_SMALL)
    dimension(ax, (0.35, -0.34), (2.35, -0.34), None, ticks=True, extension=False)
    text(ax, (1.35, -0.34), "air distance", direction=-90, dist=5, fs=FS_SMALL)
    dimension(ax, (2.35, -0.34), (5.65, -0.34), None, ticks=True, extension=False)
    text(ax, (4.00, -0.34), "braking ground roll, $s_L$", direction=-90, dist=5, fs=FS_LABEL)

    assert xs_to[-1] == 5.65 and xs_la[-1] == 5.65
    save_figure(fig, "p55-takeoff-landing-phases")


def fig_constraint_diagram():
    """Constraint diagram (sea-level T/W vs W/S) for the invented twin-jet medical transport,
    with feasible region shaded in light gold and design point marked at the corner."""
    D = _design_point()
    K = D["K"]
    WS = np.linspace(1400.0, 4800.0, 400)
    to = tw_takeoff_line(WS, REQ["s_LO"], EX["CL_TO"])
    cl = tw_climb_line(WS, REQ["RC"], REQ["V_cl"], EX["CD0"], K)
    cr = tw_cruise_line(WS, REQ["V_cr"], EX["CD0"], K, D["rho_cr"], m_ad=EX["m_ad"])
    ce = tw_ceiling_line(WS, REQ["RC_ceil"], EX["CD0"], K, D["rho_ce"], m_ad=EX["m_ad"])

    mask = WS <= D["WS_des"]
    lower = np.maximum.reduce([to, cl, cr, ce])

    fig, ax = data_axes(6.5, 4.4)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.14, top=0.96)
    ax.fill_between(WS[mask], lower[mask], 0.50, color=HIGHLIGHT, lw=0, zorder=1)
    ax.plot(WS, to, **line_kw(0), zorder=4)
    ax.plot(WS, cl, **line_kw(1), zorder=4)
    ax.plot(WS, cr, **line_kw(2), zorder=4)
    ax.plot(WS, ce, **line_kw(3), zorder=4)
    ax.axvline(D["WS_st"], color=AGED, lw=2.0, ls="-", zorder=4)
    ax.axvline(D["WS_la"], color=STEEL, lw=1.6, ls=(0, (6, 2, 1.5, 2)), zorder=3)

    ax.plot([D["WS_des"]], [D["TW_des"]], "o", ms=7.5, color=INK, zorder=7)
    ax.set_xlim(1400, 4800); ax.set_ylim(0.0, 0.48)
    ax.set_xticks([1500, 2000, 2500, 3000, 3500, 4000, 4500])
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4])
    ax.set_xlabel("Wing loading, $W/S$, N/m$^2$")
    ax.set_ylabel("Sea-level thrust-to-weight ratio, $T/W$")

    text(ax, (2120, 0.44), "feasible region", fs=FS_LABEL, backing=HIGHLIGHT)
    text(ax, (3750, 0.355), "takeoff", fs=FS_SMALL, color=INK, ha="center")
    text(ax, (3820, float(tw_climb_line(3820.0, REQ["RC"], REQ["V_cl"], EX["CD0"], K))), "climb",
         direction=90, dist=7, fs=FS_SMALL, color=BLUE)
    text(ax, (4050, float(tw_cruise_line(4050.0, REQ["V_cr"], EX["CD0"], K, D["rho_cr"], m_ad=EX["m_ad"]))),
         "cruise", direction=-90, dist=9, fs=FS_SMALL, color=text_color(2))
    text(ax, (1750, 0.172), "ceiling", fs=FS_SMALL, color=STEEL)
    text(ax, (D["WS_st"], 0.43), "stall\nlimit", direction=0, dist=6, fs=FS_SMALL, color=AGED, ha="left")
    text(ax, (D["WS_la"], 0.43), "landing\nlimit", direction=180, dist=6, fs=FS_SMALL, color=STEEL, ha="right")

    callout(ax, (D["WS_des"], D["TW_des"]),
            f"design point:\n$W/S$ = {fmt(D['WS_des'], 4)} N/m$^2$\n$T/W$ = {fmt_dec(D['TW_des'], 3)}",
            at=(2080, 0.34), ha="left", fs=FS_SMALL, backing=HIGHLIGHT)

    close_to(D["TW_des"], D["lines"]["takeoff"], 1e-12, "takeoff sets T/W at stall limit")
    assert D["WS_st"] < D["WS_la"], "stall limit is tighter than landing limit"
    save_figure(fig, "p55-constraint-diagram")


def fig_field_length_sensitivity():
    """Takeoff ground roll s_LO and landing ground roll s_L against wing loading W/S at the
    chosen T/W = 0.250, showing the linear growth of both distances with W/S and the design point."""
    D = _design_point()
    WS = np.linspace(1500.0, 4500.0, 300)
    s_to = 1.44 * WS / (G0 * RHO_SL * EX["CL_TO"] * D["TW_des"])
    s_la = 1.69 * WS / (G0 * RHO_SL * EX["CL_L"] * EX["mu_r"])
    s_to_hi = 1.44 * WS / (G0 * RHO_SL * EX["CL_TO"] * 0.30)

    fig, ax = data_axes(6.5, 3.8)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.15, top=0.96)
    ax.plot(WS, s_to, **line_kw(0), zorder=4)
    ax.plot(WS, s_to_hi, **line_kw(1), zorder=4)
    ax.plot(WS, s_la, **line_kw(2), zorder=4)
    ax.plot([D["WS_des"]], [REQ["s_LO"]], "o", ms=6.5, color=INK, zorder=6)
    s_la_des = float(1.69 * D["WS_des"] / (G0 * RHO_SL * EX["CL_L"] * EX["mu_r"]))
    ax.plot([D["WS_des"]], [s_la_des], "s", ms=6.0, mfc="white", mec=text_color(2), mew=1.4, zorder=6)

    ax.set_xlim(1500, 4600); ax.set_ylim(0, 1200)
    ax.set_xticks([1500, 2000, 2500, 3000, 3500, 4000, 4500])
    ax.set_yticks([0, 300, 600, 900, 1200])
    ax.set_xlabel("Wing loading, $W/S$, N/m$^2$")
    ax.set_ylabel("Ground roll distance, m")

    text(ax, (3820, 1005), "takeoff, $T/W = 0.250$", direction=120, dist=8, fs=FS_SMALL, color=INK)
    text(ax, (4520, 775), "$T/W = 0.300$", fs=FS_SMALL, color=BLUE, ha="right")
    text(ax, (3980, 560), "landing ($\\mu_r = 0.40$)", direction=-55, dist=10, fs=FS_SMALL, color=text_color(2))
    callout(ax, (D["WS_des"], REQ["s_LO"]), f"design: $s_{{\\mathrm{{LO}}}}$ = {fmt(REQ['s_LO'], 3)} m",
            at=(1650, 940), ha="left", fs=FS_LABEL)
    callout(ax, (D["WS_des"], s_la_des), f"$s_L$ = {fmt(s_la_des, 3)} m",
            at=(2200, 180), ha="left", fs=FS_SMALL, color=text_color(2))

    close_to(float(1.44 * D["WS_des"] / (G0 * RHO_SL * EX["CL_TO"] * D["TW_des"])), REQ["s_LO"], 1e-6, "s_LO at design")
    save_figure(fig, "p55-field-length-sensitivity")


def make_all():
    fig_takeoff_landing_phases()
    fig_constraint_diagram()
    fig_field_length_sensitivity()


# ===================================================================== printed values
def values():
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731
    D = _design_point()
    r("m", fmt(EX["m"], 4)); r("CD0", fmt_dec(EX["CD0"], 3))
    r("AR", fmt_dec(EX["AR"], 1)); r("e", fmt_dec(EX["e"], 2))
    r("CL-TO", fmt_dec(EX["CL_TO"], 2)); r("CL-L", fmt_dec(EX["CL_L"], 2))
    r("mur", fmt_dec(EX["mu_r"], 2)); r("mad", fmt_dec(EX["m_ad"], 2))
    W = r("W", fmt(EX["m"] * G0, 5)); Wp = _num(W)
    K = r("K", fmt(1.0 / (math.pi * EX["e"] * EX["AR"]), 5)); Kp = _num(K)

    r("req-Vs", fmt(REQ["Vs"], 2)); r("req-sLO", fmt(REQ["s_LO"], 3)); r("req-sL", fmt(REQ["s_L"], 3))
    r("req-RC", fmt(REQ["RC"], 2)); r("req-Vcl", fmt(REQ["V_cl"], 2))
    r("req-Vcr", fmt(REQ["V_cr"], 3)); r("req-hcr", fmt(REQ["h_cr"], 5))
    r("req-hceil", fmt(REQ["h_ceil"], 5))

    WS_st = r("WS-stall", fmt(0.5 * RHO_SL * REQ["Vs"] ** 2 * EX["CL_L"], 4))
    r("WS-land", fmt(REQ["s_L"] * G0 * RHO_SL * EX["CL_L"] * EX["mu_r"] / 1.69, 4))
    WS_p = _num(WS_st)

    tw_to = r("TW-to", fmt_dec(1.44 * WS_p / (G0 * RHO_SL * EX["CL_TO"] * REQ["s_LO"]), 3))
    q_cl = r("q-cl", fmt(0.5 * RHO_SL * REQ["V_cl"] ** 2, 4))
    r("TW-cl", fmt_dec(REQ["RC"] / REQ["V_cl"] + _num(q_cl) * EX["CD0"] / WS_p + Kp * WS_p / _num(q_cl), 3))

    rho_cr = r("rho-cr", fmt(D["rho_cr"], 4))
    q_cr = r("q-cr", fmt(0.5 * _num(rho_cr) * REQ["V_cr"] ** 2, 4))
    lap_cr = r("lap-cr", fmt((_num(rho_cr) / RHO_SL) ** EX["m_ad"], 4))
    r("TW-cr", fmt_dec((_num(q_cr) * EX["CD0"] / WS_p + Kp * WS_p / _num(q_cr)) / _num(lap_cr), 3))

    rho_ce = r("rho-ce", fmt(D["rho_ce"], 4))
    lap_ce = r("lap-ce", fmt((_num(rho_ce) / RHO_SL) ** EX["m_ad"], 4))
    V_ce = r("V-ce", fmt(math.sqrt(2.0 * WS_p / _num(rho_ce) * math.sqrt(Kp / EX["CD0"])), 4))
    r("TW-ce", fmt_dec((REQ["RC_ceil"] / _num(V_ce) + 2.0 * math.sqrt(Kp * EX["CD0"])) / _num(lap_ce), 3))

    r("S-des", fmt(Wp / WS_p, 4))
    T_tot = r("T-tot", fmt(_num(tw_to) * Wp, 5))
    r("T-one", fmt(_num(T_tot) / 2.0, 4))

    V_s_to = math.sqrt(2.0 * WS_p / (RHO_SL * EX["CL_TO"]))
    r("V-LO", fmt(1.2 * V_s_to, 3))
    r("V-TD", fmt(1.3 * REQ["Vs"], 3))
    r("s-L-des", fmt(1.69 * WS_p / (G0 * RHO_SL * EX["CL_L"] * EX["mu_r"]), 3))
