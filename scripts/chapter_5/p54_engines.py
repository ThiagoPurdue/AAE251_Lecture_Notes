"""Figures and values of 5.4 Engines (notes/chapter-5/engines.md).

Sources:
  - Anderson, Introduction to Flight, 8th ed. (2016), Chapter 9 (control volume, turbojet
    pressure/thrust distribution, turbofan, turboprop, ramjet, Rolls-Royce single-spool
    thrust breakdown: 57,836 lb forward minus 46,678 lb rearward = 11,158 lb net).
  - Lecture 24 engine sizes (Teledyne Continental 305 turbojet vs Rolls-Royce Trent 895) and
    representative efficiency / SFC / Mach-range trends (Anderson Chapter 9; Mattingly 2006).
"""
from chapter_5.common import *
from matplotlib.patches import FancyBboxPatch

PAGE = "p54"

EX1_VINF = 220.0
EX1_TJ = dict(m_air=60.0, m_fuel=1.2, V_e=870.0)
EX1_TF = dict(m_air=280.0, m_fuel=1.2, V_e=361.5)

RR_FWD_LB = 57836.0
RR_AFT_LB = 46678.0
RR_NET_LB = 11158.0


def _num(s):
    return float(s.replace(",", "").replace("−", "-"))


# ===================================================================== figures
def fig_jet_control_volume():
    """Control volume of an air-breathing jet engine (schematic, after Anderson Fig. 9.3),
    showing incoming air at V_inf and p_inf, fuel added inside, exhaust at V_e and p_e across
    exit area A_e, and net thrust T forward."""
    fig, ax = canvas(6.5, xlim=(-1.55, 7.15), ylim=(-1.45, 1.55))
    g = draw_turbojet(ax, origin=(0.45, 0.0), scale=0.88)

    cv = FancyBboxPatch((-0.10, -0.92), 5.65, 1.84, boxstyle="square,pad=0.0",
                        fc="none", ec=STEEL, lw=1.2, ls=(0, (5, 3)), zorder=2.5)
    ax.add_patch(cv)
    text(ax, (2.72, -0.92), "control volume", direction=-90, dist=7, fs=FS_SMALL, color=STEEL)

    # Inflow velocity arrow (left)
    kind_arrow(ax, (-1.35, 0.0), (-0.22, 0.0), "velocity", None)
    text(ax, (-0.82, 0.0), "inflow,\n$V_\\infty$", direction=90, dist=8, color=BLUE, fs=FS_LABEL)
    text(ax, (-0.82, 0.0), "$p_\\infty$", direction=-90, dist=9, color=STEEL, fs=FS_LABEL)

    # Exit flow velocity arrow (right, clearly outside CV box at x=5.55)
    kind_arrow(ax, (5.68, 0.0), (6.95, 0.0), "velocity", None)
    text(ax, (6.36, 0.0), "exhaust,\n$V_e$", direction=90, dist=8, color=BLUE, fs=FS_LABEL)
    text(ax, (6.36, 0.0), "$p_e$, $A_e$", direction=-90, dist=9, color=STEEL, fs=FS_LABEL)

    # Fuel flow entering combustor from top
    kind_arrow(ax, (2.87, 1.38), (2.87, 0.54), "leads_to", None)
    text(ax, (2.87, 1.38), "fuel flow", direction=0, dist=7, fs=FS_SMALL, ha="left")

    # Thrust arrow pulling engine forward
    kind_arrow(ax, (1.55, 1.18), (0.35, 1.18), "force", "thrust, $T$", label_dir=180, dist=5)

    legend_key(ax, (4.35, 1.42), [("force", "force"), ("velocity", "velocity")], dy=17, fs=FS_SMALL)
    assert g["extent"][1] < 5.55, "engine fits inside control volume"
    trim_canvas(fig)
    save_figure(fig, "p54-jet-control-volume")


def fig_turbojet_stages():
    """Single-spool turbojet cutaway aligned above qualitative pressure and temperature profiles
    across the five stages (schematic, after Anderson Fig. 9.18)."""
    fig = plt.figure(figsize=(6.5, 5.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.15, 1.0], hspace=0.14)
    ax_top = fig.add_subplot(gs[0])
    ax_bot = fig.add_subplot(gs[1])

    ax_top.axis("off")
    ax_top.set_aspect("equal")
    g = draw_turbojet(ax_top, origin=(0.0, 0.0), scale=1.0)
    ax_top.set_xlim(-0.55, 5.95); ax_top.set_ylim(-1.15, 1.45)

    flow_arrow(ax_top, (-0.48, 0.0), (-0.06, 0.0), width=6.0, head_width=11.0, head_len=7.0)
    flow_arrow(ax_top, (5.46, 0.0), (5.88, 0.0), width=6.0, head_width=11.0, head_len=7.0)

    callouts = [
        ("inlet", "1  inlet\n(diffuser)", (0.25, 1.12)),
        ("compressor", "2  compressor", (1.54, 1.18)),
        ("combustor", "3  combustor", (2.75, 1.18)),
        ("turbine", "4  turbine", (3.72, 1.18)),
        ("nozzle", "5  nozzle", (5.05, 1.12)),
    ]
    for key, lbl, at in callouts:
        callout(ax_top, g[key], lbl, at=at, ha="center", va="center", fs=FS_SMALL, gap=2.0)
    callout(ax_top, (2.75, -0.10), "shaft (turbine drives compressor)", at=(2.75, -0.92),
            ha="center", va="center", fs=FS_SMALL, gap=2.0)

    for s in ("top", "right"):
        ax_bot.spines[s].set_visible(False)
    ax_bot.grid(True, color=GRID, lw=0.6)
    ax_bot.set_axisbelow(True)
    xs_st = [0.0, 0.9, 2.2, 3.3, 4.0, 5.4]
    for x in xs_st[1:-1]:
        ax_bot.axvline(x, **line_kw("boundary"), zorder=2)

    xp = np.array([0.0, 0.9, 2.2, 3.3, 4.0, 5.4])
    p_rel = np.array([0.12, 0.22, 0.95, 0.91, 0.42, 0.12])
    T_rel = np.array([0.12, 0.16, 0.42, 0.98, 0.72, 0.46])
    ax_bot.plot(xp, p_rel, **line_kw(0), zorder=4)
    ax_bot.plot(xp, T_rel, **line_kw(2), zorder=4)
    ax_bot.set_xlim(-0.55, 5.95); ax_bot.set_ylim(0.0, 1.24)
    ax_bot.set_xticks([0.45, 1.55, 2.75, 3.65, 4.70])
    ax_bot.set_xticklabels(["inlet", "compressor", "combustor", "turbine", "nozzle"], fontsize=FS_SMALL)
    ax_bot.set_yticks([0.12, 1.0])
    ax_bot.set_yticklabels(["ambient", "peak"], fontsize=FS_SMALL)
    ax_bot.set_ylabel("Relative level")

    text(ax_bot, (1.55, 0.98), "pressure, $p$", fs=FS_SMALL, color=INK)
    text(ax_bot, (4.80, 0.98), "temperature, $T$", fs=FS_SMALL, color=text_color(2))
    fig.subplots_adjust(left=0.14, right=0.97, bottom=0.10, top=0.96)
    assert p_rel[2] > p_rel[1] and T_rel[3] > T_rel[2] and p_rel[5] < p_rel[3]
    save_figure(fig, "p54-turbojet-stages")


def fig_engine_cutaways():
    """Three-panel comparison of the other air-breathing engine architectures:
    1 turbofan (fan + bypass duct + core), 2 turboprop (propeller + gearbox + core),
    3 ramjet (inlet spike + injectors/combustor + converging-diverging nozzle)."""
    fig, axs = new_axes(6.5, 7.6, nrows=3, equal=True)
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.97, hspace=0.18)

    # Panel 1: Turbofan
    ax = axs[0]
    g = draw_turbofan(ax, origin=(0.50, 0.0), scale=0.95)
    ax.set_xlim(-0.25, 6.25); ax.set_ylim(-1.42, 1.92)
    flow_arrow(ax, (-0.15, 0.0), (0.36, 0.0), width=5.5, head_width=10.0, head_len=6.5)
    text(ax, (-0.20, 1.78), "1  high-bypass turbofan", fs=FS_LABEL, ha="left", backing=False)
    callout(ax, g["fan"], "fan", at=(0.55, 1.32), ha="center", fs=FS_SMALL)
    callout(ax, g["bypass"], "bypass duct", at=(1.95, 1.32), ha="center", fs=FS_SMALL)
    callout(ax, g["combustor"], "core (compressor,\ncombustor, turbine)", at=(3.70, 1.32), ha="center", fs=FS_SMALL)
    callout(ax, g["nozzle"], "core\nnozzle", at=(5.60, 0.85), ha="center", fs=FS_SMALL)
    text(ax, (3.20, -1.24), "most thrust comes from the bypass air", fs=FS_SMALL, color=STEEL)

    # Panel 2: Turboprop
    ax = axs[1]
    g = draw_turboprop(ax, origin=(0.50, 0.0), scale=0.95)
    ax.set_xlim(-0.25, 6.25); ax.set_ylim(-1.42, 1.92)
    flow_arrow(ax, (-0.15, 0.0), (0.36, 0.0), width=5.5, head_width=10.0, head_len=6.5)
    text(ax, (-0.20, 1.78), "2  turboprop", fs=FS_LABEL, ha="left", backing=False)
    callout(ax, g["propeller"], "propeller", at=(0.55, 1.32), ha="center", fs=FS_SMALL)
    callout(ax, g["gearbox"], "reduction\ngearbox", at=(1.85, 1.32), ha="center", fs=FS_SMALL)
    callout(ax, g["combustor"], "gas-turbine\ncore", at=(3.28, 1.32), ha="center", fs=FS_SMALL)
    callout(ax, g["turbine"], "power\nturbine", at=(4.48, 1.32), ha="center", fs=FS_SMALL)
    callout(ax, g["nozzle"], "exhaust", at=(5.65, 0.72), ha="center", fs=FS_SMALL)
    text(ax, (3.20, -1.24), "turbine drives the propeller through the shaft and gearbox", fs=FS_SMALL, color=STEEL)

    # Panel 3: Ramjet
    ax = axs[2]
    g = draw_ramjet(ax, origin=(0.50, 0.0), scale=0.95)
    ax.set_xlim(-0.25, 6.25); ax.set_ylim(-1.28, 1.82)
    flow_arrow(ax, (-0.15, 0.0), (0.36, 0.0), width=5.5, head_width=10.0, head_len=6.5)
    text(ax, (-0.20, 1.66), "3  ramjet (no compressor or turbine)", fs=FS_LABEL, ha="left", backing=False)
    callout(ax, g["inlet"], "supersonic\ninlet spike", at=(0.75, 1.12), ha="center", fs=FS_SMALL)
    callout(ax, g["injectors"], "injectors &\nflameholder", at=(2.25, 1.12), ha="center", fs=FS_SMALL)
    callout(ax, g["combustor"], "combustor", at=(3.60, 1.12), ha="center", fs=FS_SMALL)
    callout(ax, g["nozzle"], "converging-\ndiverging nozzle", at=(5.25, 1.12), ha="center", fs=FS_SMALL)
    text(ax, (3.20, -1.06), "ram compression from high flight speed (Mach > 2)", fs=FS_SMALL, color=STEEL)

    assert g["extent"][1] < 5.8
    save_figure(fig, "p54-engine-cutaways")


def fig_propulsive_efficiency():
    """Schematic propulsive efficiency vs. flight Mach number (0 to 1.0) for propeller
    (piston/turboprop), high-bypass turbofan, and turbojet (after Lecture 24 / Anderson Ch. 9)."""
    M = np.linspace(0.02, 1.0, 200)
    eta_prop = np.where(
        M <= 0.48,
        84.0 * (1.0 - np.exp(-9.5 * M)),
        84.0 * (1.0 - np.exp(-9.5 * 0.48)) * np.exp(-4.8 * (M - 0.48) ** 2),
    )
    eta_fan = 65.0 * (M / (M + 0.30)) * (1.0 + 0.28 * M)
    eta_jet = 57.0 * (M / (M + 0.48)) * (1.0 + 0.42 * M)

    fig, ax = data_axes(6.5, 3.9)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.15, top=0.96)
    ax.plot(M, eta_prop, **line_kw(0), zorder=4)
    ax.plot(M, eta_fan, **line_kw(1), zorder=4)
    ax.plot(M, eta_jet, **line_kw(2), zorder=4)
    ax.axvline(0.55, **line_kw("boundary"), zorder=2)

    ax.set_xlim(0.0, 1.02); ax.set_ylim(0, 96)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0]); ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_xlabel("Flight Mach number, $M$")
    ax.set_ylabel("Propulsive efficiency, $\\eta_p$, %")

    text(ax, (0.34, 83.0), "piston / turboprop", direction=90, dist=4, fs=FS_SMALL, color=INK)
    text(ax, (0.86, 75.0), "high-bypass\nturbofan", fs=FS_SMALL, color=BLUE)
    text(ax, (0.86, 24.0), "turbojet", fs=FS_SMALL, color=text_color(2))
    text(ax, (0.56, 11.0), "tip compressibility\nlimits propellers", direction=0, dist=4,
         fs=FS_SMALL, color=STEEL, ha="left")

    assert np.max(eta_prop) > 78.0 and float(np.interp(0.85, M, eta_fan)) > float(np.interp(0.85, M, eta_prop))
    save_figure(fig, "p54-propulsive-efficiency")


def fig_sfc_vs_mach():
    """Schematic thrust-specific fuel consumption trends against Mach number (0 to 1.0)
    comparing piston/turboprop (equivalent TSFC), high-bypass turbofan, low-bypass turbofan,
    and turbojet (after Lecture 24 / Raymer & Anderson)."""
    M_j = np.linspace(0.0, 1.0, 200)
    sfc_tj = 0.95 + 0.30 * M_j
    sfc_lbf = 0.56 + 0.25 * M_j
    sfc_hbf = 0.38 + 0.22 * M_j
    M_p = np.linspace(0.05, 0.68, 160)
    sfc_tp = 0.14 + 0.28 * M_p + 2.6 * np.maximum(M_p - 0.42, 0.0) ** 2 * 4.5

    fig, ax = data_axes(6.5, 4.0)
    fig.subplots_adjust(left=0.14, right=0.97, bottom=0.14, top=0.96)
    ax.plot(M_j, sfc_tj, **line_kw(2), zorder=4)
    ax.plot(M_j, sfc_lbf, **line_kw(3), zorder=4)
    ax.plot(M_j, sfc_hbf, **line_kw(1), zorder=4)
    ax.plot(M_p, sfc_tp, **line_kw(0), zorder=5)

    ax.set_xlim(0.0, 1.02); ax.set_ylim(0.0, 1.42)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0]); ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])
    ax.set_xlabel("Flight Mach number, $M$")
    ax.set_ylabel("Thrust specific fuel consumption, 1/h")

    text(ax, (0.76, 1.21), "turbojet", direction=90, dist=6, fs=FS_SMALL, color=text_color(2))
    text(ax, (0.80, 0.78), "low-bypass turbofan", direction=90, dist=7, fs=FS_SMALL, color=STEEL)
    text(ax, (0.80, 0.54), "high-bypass turbofan", direction=-90, dist=8, fs=FS_SMALL, color=BLUE)
    text(ax, (0.28, 0.22), "piston / turboprop", direction=-90, dist=10, fs=FS_SMALL, color=INK)

    assert float(sfc_hbf[-1]) < float(sfc_lbf[-1]) < float(sfc_tj[-1])
    assert float(sfc_tp[20]) < float(sfc_hbf[20])
    save_figure(fig, "p54-sfc-vs-mach")


def fig_engine_map():
    """Operating envelope map matching air-breathing engine types to flight Mach number and
    mission range (schematic, after Lecture 24 Slide 29 and Anderson Chapter 9)."""
    fig, ax = data_axes(6.5, 4.2, grid=False)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.14, top=0.95)

    # Clean non-hatched tinted boxes so labels inside have clean contrast and zero pixel-test hits
    boxes = [
        (0.06, 0.4, 0.24, 3.0, None, "#FFFFFF"),
        (0.22, 3.8, 0.36, 3.0, None, "#EFEFEF"),
        (0.70, 4.6, 0.24, 4.0, None, HIGHLIGHT),
        (1.08, 2.6, 1.08, 3.2, "low-bypass\nturbofan", "#EFEFEF"),
        (1.20, 0.4, 1.55, 1.8, "turbojet /\nafterburner", "#FFFFFF"),
        (2.45, 2.6, 1.95, 3.2, "ramjet", "#EFEFEF"),
        (4.55, 2.6, 1.32, 3.2, "scramjet", "#FFFFFF"),
    ]
    for x, y, w, h, lbl, fc in boxes:
        pa = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.08",
                            fc=fc, ec=INK, lw=1.2, zorder=3)
        ax.add_patch(opaque(pa))
        if lbl:
            text(ax, (x + 0.5 * w, y + 0.5 * h), lbl, fs=FS_SMALL, backing=fc)

    # Clean callouts for the three narrow subsonic boxes (none crosses the Mach 1 line)
    callout(ax, (0.30, 1.8), "piston", at=(0.45, 1.8), ha="left", fs=FS_SMALL)
    callout(ax, (0.32, 6.8), "turboprop", at=(0.14, 9.8), ha="left", fs=FS_SMALL)
    callout(ax, (0.82, 8.6), "high-bypass\nturbofan", at=(1.45, 9.6), ha="left", fs=FS_SMALL)

    ax.set_xlim(0.0, 6.0); ax.set_ylim(0.0, 11.2)
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax.set_yticks([1.5, 5.0, 8.5])
    ax.set_yticklabels(["short", "medium", "long"], fontsize=FS_SMALL)
    ax.set_xlabel("Cruise Mach number, $M$")
    ax.set_ylabel("Mission range")
    ax.plot([1.0, 1.0], [0.0, 8.2], **line_kw("boundary"), zorder=2)
    text(ax, (1.06, 7.6), "Mach 1", direction=0, dist=3, fs=FS_SMALL, color=STEEL, ha="left")
    save_figure(fig, "p54-engine-map")


def make_all():
    fig_jet_control_volume()
    fig_turbojet_stages()
    fig_engine_cutaways()
    fig_propulsive_efficiency()
    fig_sfc_vs_mach()
    fig_engine_map()


# ===================================================================== printed values
def values():
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731
    r("rr-fwd", fmt(RR_FWD_LB, 5)); r("rr-aft", fmt(RR_AFT_LB, 5)); r("rr-net", fmt(RR_NET_LB, 5))

    Vinf = EX1_VINF
    r("ex1-Vinf", fmt(Vinf, 3))
    ma_j, mf_j, ve_j = EX1_TJ["m_air"], EX1_TJ["m_fuel"], EX1_TJ["V_e"]
    r("tj-mair", fmt_dec(ma_j, 1)); r("tj-mf", fmt_dec(mf_j, 1)); r("tj-Ve", fmt(ve_j, 3))
    T_tj = r("tj-T", fmt((ma_j + mf_j) * ve_j - ma_j * Vinf, 5))
    r("tj-T-kN", fmt(_num(T_tj) / 1000.0, 4))
    etap_tj = r("tj-etap", fmt(float(propulsive_efficiency(Vinf, ve_j)), 3))
    r("tj-etap-pct", fmt(100.0 * _num(etap_tj), 3))

    ma_f, mf_f, ve_f = EX1_TF["m_air"], EX1_TF["m_fuel"], EX1_TF["V_e"]
    r("tf-mair", fmt_dec(ma_f, 1)); r("tf-mf", fmt_dec(mf_f, 1)); r("tf-Ve", fmt_dec(ve_f, 1))
    T_tf = r("tf-T", fmt((ma_f + mf_f) * ve_f - ma_f * Vinf, 5))
    r("tf-T-kN", fmt(_num(T_tf) / 1000.0, 4))
    etap_tf = r("tf-etap", fmt(float(propulsive_efficiency(Vinf, ve_f)), 3))
    r("tf-etap-pct", fmt(100.0 * _num(etap_tf), 3))

    r("ex2-legs", "6"); r("ex2-hrs", "1.5"); r("ex2-Mach", "0.42"); r("ex2-runway", "900")
    r("ex2-tp-burn", "260"); r("ex2-tf-burn", "430")
    r("ex2-diff-hr", fmt(430 - 260, 3))
    r("ex2-diff-day", fmt(6 * 1.5 * (430 - 260), 4))
    r("ex2-tp-mass", "410"); r("ex2-tf-mass", "820")
    r("ex2-tp-noise", "82"); r("ex2-tf-noise", "86")

    r("t305-T", "90"); r("t305-W", "20"); r("t305-D", "7.0")
    r("t895-T", "95,000"); r("t895-W", "13,100"); r("t895-D", "110")
