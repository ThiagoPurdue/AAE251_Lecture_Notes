"""Figures and values of 5.4 Engines (notes/chapter-5/engines.md).

Sources (opened; the page cites them by chapter, section or figure):
  - Leishman, J. G., Introduction to Aerospace Flight Vehicles, Embry-Riddle Aeronautical
    University, 2022-2027 (open textbook, CC BY-NC-ND 4.0), DOI 10.15394/eaglepub.2022.1066:
    Chapter 40 "Fundamentals of Propulsion Systems" (propulsive efficiency, fuel to air ratio of
    about 1:15 or less, turboprops below about Mach 0.5 and up to about 0.6 with advanced
    propellers, piston engines, Figure 20 specific impulse against Mach number), Chapter 46
    "Turbojet Engines" (the five stages, afterburning: thrust nearly doubles, F100-PW-229 TSFC
    0.76 and 1.94 lb/(lb h)), Chapter 47 "Turbofan & Turboprop Engines" (bypass ratio, the
    two-stream thrust, afterburning turbofans 0.3 to 0.9, F100-PW-229 about 0.36, turbofan cruise
    about Mach 0.7 to 0.85, equivalent shaft power, the Allison T56 on the C-130, open rotors);
    Chapter 40, Eq. 19 (fuel per unit thrust inversely proportional to the propulsive efficiency
    at a given thermal efficiency).
  - Anderson, Introduction to Flight, 8th ed. (2016), Chapter 9, the Rolls-Royce figure of the thrust
    distribution of a typical single-spool axial-flow jet engine (cited by chapter: the figure number,
    9.19, and the edition are not verified): the six gas loads in lb.
  - FAA type certificate data sheet 1E16, rev. 15 (2008), GE CJ610; EASA TCDS E.004 issue 07 (2023),
    CFM56-7B; EASA TCDS IM.E.040 issue 01 (2008), Rolls-Royce AE 2100: the engine drawings (stage
    counts, dimensions, gear ratio and maximum permissible rotor speeds).
  - NASA Glenn Research Center, Beginner's Guide to Propulsion (turbine engines, turbofan, turboprop,
    afterburning turbojet, ramjet pages): what each engine family is used for; the C-130 carries cargo
    a long distance with no high-speed requirement, on four turboprops; ramjets are very inefficient
    above Mach 5.
Worked example 2 uses the chapter's executive jet (vehicles.EXEC_JET); worked example 3 the chapter's
four-engine turboprop transport (vehicles.TRANSPORT), introduced on page 5.3.
"""
from chapter_5.common import *
from matplotlib.patches import Polygon
from matplotlib.ticker import FuncFormatter

PAGE = "p54"
LBF = 4.4482216152605          # N per pound-force

# ===================================================================== worked example 1
# Two engines give the same thrust at the same flight speed; fuel and the pressure term neglected,
# as in the derivation of the propulsive efficiency.
EX1 = dict(V=230.0, T=34200.0, m_small=40.0, m_large=228.0)

# ===================================================================== the turbojet of the stage figure
# An ideal single-spool turbojet standing still at sea level (assumed numbers, not the CJ610's):
# compressor pressure ratio 7, gas temperature entering the turbine 1,150 K, gamma = 1.4, the gas
# speed inside the engine neglected until the nozzle, which expands the gas to ambient pressure.
CYCLE = dict(pi_c=7.0, T4=1150.0, gamma=1.4)

# ===================================================================== thrust distribution (Anderson, Chapter 9)
# Gas loads on the parts of a typical single-spool axial-flow jet engine, lb, positive forward
# (Anderson (2016), Chapter 9, courtesy of Rolls-Royce). In flow order.
GAS_LOADS = [("compressor", 19049.0), ("compressor-exit diffuser", 2186.0), ("combustion chamber", 34182.0),
             ("turbine", -41091.0), ("exhaust unit and jet pipe", 2419.0), ("propelling nozzle", -5587.0)]
GAS_FWD, GAS_AFT, GAS_NET = 57836.0, 46678.0, 11158.0       # the figure's totals
FWD_FILL = "#D9D9D9"                                        # forward loads: plain light gray (gold is kept for bands)

# ===================================================================== published engine facts
F100 = dict(tsfc_dry=0.76, tsfc_ab=1.94, bpr=0.36)          # Leishman Ch. 46 (TSFC, lb/(lb h)) and Ch. 47 (BPR)
BPR_HIGH = (8, 12)                                          # Leishman Ch. 40: modern high-bypass turbofans
BPR_AB = (0.3, 0.9)                                         # Leishman Ch. 47: afterburning turbofans
# EASA IM.E.040, section 5 (ratings, static shaft power): from 2,787 kW (AE 2100A, maximum continuous)
# to 3,458 kW (AE 2100D2 and D2A); and the gear ratio
AE2100 = dict(P_lo=2787.0, P_hi=3458.0, gear=AE2100_GEAR)
RAMJET_LIMIT_M = 5.0                                        # NASA Glenn, ramjet page: very inefficient above Mach 5

# Mach bands: (family, solid band, lighter extension or None, source). Leishman (2022) Chapter 40,
# Figure 20 (specific impulse against flight Mach number) has no band for a turbojet without
# afterburner; its "turbofans with afterburner" ellipse holds the afterburning turbojets too (it
# marks the RR Olympus of Concorde inside it). Read off the figure to about 0.1 in Mach number.
MACH_BANDS = [
    ("propeller, piston or turbine", (0.0, 0.5), (0.5, 0.6), "Leishman Ch. 40, Turboprops"),
    ("high-bypass turbofan, cruise", (0.7, 0.85), None, "Leishman Ch. 47, Thrust Production"),
    ("turbofan or turbojet with afterburner", (0.3, 3.5), None, "Leishman Ch. 40, Figure 20"),
    ("ramjet", (2.9, 6.6), None, "Leishman Ch. 40, Figure 20"),
    ("scramjet", (4.9, 9.5), None, "Leishman Ch. 40, Figure 20"),
]
# panel limits (m) of the two engine figures: the whole engine, then the enlarged upper half of the core
TF_PANELS = (((-0.86, 4.22), (-1.06, 1.00)), ((0.56, 2.52), (-0.06, 0.58)))
TP_PANELS = (((-0.45, 3.55), (-0.94, 0.86)), ((0.72, 2.44), (-0.06, 0.40)))


def _enlargement(panels):
    """How many times larger the second panel is drawn: both panels fill the same width."""
    (t, _), (d, _) = panels
    return (t[1] - t[0]) / (d[1] - d[0])


M_SPLIT = 1.2                                               # the Mach-band axis is stretched below this

# ===================================================================== worked example 2: the executive jet
# What the fan saves at the cruise of the chapter's executive jet (vehicles.EXEC_JET): an illustration
# of propulsive efficiency, not an engine choice. The two engine air flows are the example's own
# assumptions: one engine passes 20.0 kg/s (a turbojet) and the other 100 kg/s (a turbofan), each
# exhaust taken as one stream at one speed, fuel and pressure term neglected.
EX2 = dict(h=10500.0, V=225.0, m_jet=20.0, m_fan=100.0)

# ===================================================================== worked example 3: the transport
# Engine choice for the chapter's four-engine turboprop transport (vehicles.TRANSPORT, page 5.3) on a
# mission of the page's own: heavy cargo over long legs, each flown at the speed for best range of a
# propeller aircraft (maximum L/D, page 5.2) at an assumed 6,500 m. The low-speed side uses the climb
# speed of page 5.3, worked example 4 (82 m/s, the same assumption there), at sea level, all engines.
EX3 = dict(h=6500.0, V_climb=82.0)


def _ex1():
    V, T = EX1["V"], EX1["T"]
    out = {}
    for k in ("m_small", "m_large"):
        m = EX1[k]
        Ve = V + T / m
        out[k] = dict(m=m, Ve=Ve, ratio=Ve / V, eta=float(propulsive_efficiency(V, Ve)),
                      wasted=0.5 * m * (Ve - V) ** 2, useful=T * V)
    return out


def _cycle():
    """Stations of the ideal turbojet: 0 ambient = compressor face, 3 compressor exit, 4 turbine
    entry, 5 turbine exit, 9 nozzle exit (static, at ambient pressure). Pa and K."""
    g = CYCLE["gamma"]
    k = (g - 1.0) / g
    T0, p0 = T_SL, P_SL
    p3 = CYCLE["pi_c"] * p0
    T3 = T0 * CYCLE["pi_c"] ** k
    dT = T3 - T0                                     # the compressor's temperature rise
    T4, p4 = CYCLE["T4"], p3                         # ideal combustor: constant pressure
    T5 = T4 - dT                                     # the turbine gives back only what the compressor takes
    p5 = p4 * (T5 / T4) ** (1.0 / k)
    T9 = T5 * (p0 / p5) ** k
    return dict(p0=p0, T0=T0, p3=p3, T3=T3, dT=dT, p4=p4, T4=T4, p5=p5, T5=T5, p9=p0, T9=T9)


def _cycle_along(S):
    """Pressure (Pa) and temperature (K) along the engine at the station x of the drawing (S):
    flat through the inlet, stage by stage through the compressor stages (equal pressure ratio per
    stage), a straight rise of temperature at constant pressure through the combustor, stage by
    stage through the turbine stages (equal temperature drop), and isentropic expansion to ambient
    pressure through the nozzle."""
    c = _cycle()
    k = (CYCLE["gamma"] - 1.0) / CYCLE["gamma"]
    nc, nt = CJ610_STAGES["compressor"], CJ610_STAGES["turbine"]
    xs, ps, Ts = [], [], []

    def add(x, p, T):
        xs.append(x); ps.append(p); Ts.append(T)
    (a0, a1), (b0, b1), (c0, c1), (d0, d1), (e0, e1) = (S[n] for n in
                                                       ("inlet", "compressor", "combustor", "turbine", "nozzle"))
    add(a0, c["p0"], c["T0"]); add(a1, c["p0"], c["T0"])
    for i in range(1, nc + 1):
        p = c["p0"] * CYCLE["pi_c"] ** (i / nc)
        add(b0 + (b1 - b0) * i / nc, p, c["T0"] * (p / c["p0"]) ** k)
    for i in range(1, 11):
        add(c0 + (c1 - c0) * i / 10.0, c["p3"], c["T3"] + (c["T4"] - c["T3"]) * i / 10.0)
    for i in range(1, nt + 1):
        T = c["T4"] - c["dT"] * i / nt
        add(d0 + (d1 - d0) * i / nt, c["p4"] * (T / c["T4"]) ** (1.0 / k), T)
    for i in range(1, 11):
        p = c["p5"] * (c["p0"] / c["p5"]) ** (i / 10.0)
        add(e0 + (e1 - e0) * i / 10.0, p, c["T5"] * (p / c["p5"]) ** k)
    return np.array(xs), np.array(ps), np.array(Ts), c


def _ex2():
    ac = EXEC_JET
    T, p, rho = standard(EX2["h"])
    rho = float(f"{float(rho):.5g}")                   # the density as the example prints it, 0.38745 kg/m^3
    a = speed_of_sound(T)
    V = EX2["V"]
    q = 0.5 * rho * V ** 2
    D0 = q * ac["S"] * ac["CD0"]
    Di = ac["K"] * weight(ac) ** 2 / (q * ac["S"])
    TR = float(level_flight_at_speed(ac["m"], ac["S"], ac["CD0"], ac["K"], rho, V)["T_R"])
    close_to(D0 + Di, TR, 1e-6, "the two drag parts add to the thrust required", rel=True)
    Te = TR / ac["n"]
    out = dict(rho=float(rho), a=float(a), M=float(V / a), V=V, q=float(q), D0=float(D0), Di=float(Di), TR=TR, Te=Te,
               W=weight(ac))
    for k in ("jet", "fan"):
        m = EX2["m_" + k]
        dV = Te / m
        Ve = V + dV
        A = m / (rho * V)                              # continuity: the captured stream tube far ahead
        out[k] = dict(m=m, dV=dV, Ve=Ve, eta=2.0 / (1.0 + Ve / V), A=float(A), d=math.sqrt(4.0 * A / math.pi))
    out["fuel_ratio"] = out["jet"]["eta"] / out["fan"]["eta"]   # same thermal efficiency (Leishman Ch. 40, Eq. 19)
    return out


def _ex3():
    ac = TRANSPORT
    T, p, rho = standard(EX3["h"])
    a = float(speed_of_sound(T))
    W = weight(ac)
    CL = math.sqrt(ac["CD0"] / ac["K"])                 # propeller best range: maximum C_L/C_D (page 5.2)
    LD = 1.0 / (2.0 * math.sqrt(ac["K"] * ac["CD0"]))
    V = math.sqrt(2.0 * W / (rho * ac["S"] * CL))
    D = W / LD
    TR = float(level_flight_at_speed(ac["m"], ac["S"], ac["CD0"], ac["K"], rho, V)["T_R"])
    close_to(TR, D, 1e-6, "drag at best range is the weight over (L/D)max", rel=True)
    Te = D / ac["n"]
    eta = ac["eta"]
    dV = 2.0 * V * (1.0 / eta - 1.0)                    # V_e - V for eta_p = eta: V_e/V = 2/eta - 1
    close_to(2.0 / (1.0 + (V + dV) / V), eta, 1e-12, "eta_p of that exhaust equals the propeller's eta")
    m = Te / dV
    A = m / (rho * V)
    sig = float(f"{float(rho):.4g}") / RHO_SL               # from the density as the example prints it, 0.6236
    lapse = sig ** ac["m_ad"]
    PA = ac["n"] * ac["eta"] * ac["P0"] * lapse
    close_to(PA, float(available(ac, rho)), 1e-4, "the lapse step gives the power available", rel=True)
    PA0 = float(available(ac, RHO_SL))
    TA_cl = PA0 / EX3["V_climb"]
    TA_cr = PA / V
    return dict(rho=float(rho), a=a, M=V / a, W=W, CL=CL, LD=LD, V=V, D=D, Te=Te, eta=eta, ratio=2.0 / eta - 1.0,
                dV=dV, m=m, A=A, d=math.sqrt(4.0 * A / math.pi), PA=PA, PA0=PA0, TA_cl=TA_cl, TA_cr=TA_cr,
                m_over_fan=m / EX2["m_fan"], tw_cl=TA_cl / W, ta_ratio=TA_cl / TA_cr, sig=sig, lapse=lapse)


# ===================================================================== figure helpers
def _stack(panels, width=6.5, gap=0.10, key_h=0.0, head=0.0, key_gap=None):
    """A figure of equal-aspect drawing panels stacked from the top, each `width` inches wide, the
    last one optionally followed by a key area `key_h` inches tall (data units: inches), with `head`
    inches above the first panel for its title. panels:
    list of (xlim, ylim). Returns fig, the list of axes, the key axes (or None) and the scales
    (inches per data unit)."""
    hs, ss = [], []
    for xl, yl in panels:
        s = width / (xl[1] - xl[0])
        ss.append(s)
        hs.append((yl[1] - yl[0]) * s)
    key_gap = gap if key_gap is None else key_gap
    H = head + sum(hs) + gap * (len(panels) - 1) + (key_gap + key_h if key_h else 0.0)
    fig = plt.figure(figsize=(width, H))
    axs, y = [], H - head
    for (xl, yl), h in zip(panels, hs):
        y -= h
        ax = fig.add_axes([0.0, y / H, 1.0, h / H])
        ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal"); ax.axis("off")
        ax.set_xticks([]); ax.set_yticks([])
        axs.append(ax)
        y -= gap
    kax = None
    if key_h:
        kax = fig.add_axes([0.0, 0.0, 1.0, key_h / H])
        kax.set_xlim(0.0, width); kax.set_ylim(0.0, key_h); kax.set_aspect("equal"); kax.axis("off")
        kax.set_xticks([]); kax.set_yticks([])
    fig.canvas.draw()
    return fig, axs, kax, ss


def _key(kax, names, x0=0.14, dx=3.25, dy=0.205, per_col=4):
    """The numbered key under an engine drawing: discs and names in columns of `per_col`."""
    top = kax.get_ylim()[1] - 0.14
    for i, name in enumerate(names, start=1):
        col, k = divmod(i - 1, per_col)
        xy = (x0 + dx * col, top - dy * k)
        key_disc(kax, xy, i)
        text(kax, xy, name, direction=0, dist=12, fs=FS_SMALL)


def _patch_x(p):
    v = p.get_xy()
    return float(np.min(v[:, 0])), float(np.max(v[:, 0]))


def _patch_y(p):
    v = p.get_xy()
    return float(np.min(v[:, 1])), float(np.max(v[:, 1]))


def _band_str(x):
    """A band end as the table prints it: one decimal, two where the source gives two (0.85)."""
    return fmt_dec(x, 2) if round(x * 100) % 10 else fmt_dec(x, 1)


# ===================================================================== figures
def fig_propulsive_efficiency():
    """Lesson: the same thrust costs less energy when a large flow of air is sped up a little than
    when a small flow is sped up a lot."""
    e = _ex1()
    r = np.linspace(1.0, 6.0, 401)
    eta = propulsive_efficiency(1.0, r)
    fig, ax = data_axes(6.5, 3.6)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.17, top=0.95)
    curve = ax.plot(r, eta, **required_kw(0), zorder=4)[0]
    ax.set_xlim(1.0, 6.0); ax.set_ylim(0.0, 1.1)
    ax.set_xticks([1, 2, 3, 4, 5, 6]); ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel("Exhaust speed over flight speed, $V_e/V_\\infty$")
    ax.set_ylabel("Propulsive efficiency, $\\eta_p$")
    for key, num, at in (("m_large", 2, (2.15, 0.74)), ("m_small", 1, (3.75, 0.47))):
        q = e[key]
        name = f"engine {num}, {fmt(q['m'], 3)} kg/s"
        on_curve(r, eta, q["ratio"], q["eta"], 1e-4, name + " on the curve")
        ax.plot([q["ratio"]], [q["eta"]], "o", ms=MS_POINT, color=INK, zorder=6)
        ax.plot([q["ratio"], q["ratio"]], [0.0, q["eta"]], color=INK, lw=LW_THIN, ls=DASH_CONSTRUCTION, zorder=3)
        ax.text(at[0], at[1], f"{name}:\n$V_e$ = {fmt(q['Ve'], 4)} m/s, $\\eta_p$ = {fmt(q['eta'], 4)}",
                ha="left", va="bottom", fontsize=FS_LABEL, color=INK, zorder=7)
    ax.text(1.12, 1.035, "no thrust when $V_e = V_\\infty$", ha="left", va="center", fontsize=FS_LABEL, color=INK,
            zorder=7)
    ax.text(1.75, 0.06, f"both engines: {fmt(EX1['T'] / 1e3, 3)} kN at {fmt(EX1['V'], 3)} m/s",
            ha="left", va="bottom", fontsize=FS_LABEL, color=INK, zorder=7)
    ax.plot([1.0], [1.0], "o", ms=MS_POINT, mfc="white", mec=INK, zorder=6, clip_on=False)
    xd, yd = curve.get_data()                        # the drawn points sit on the drawn curve
    for key in ("m_small", "m_large"):
        close_to(float(np.interp(e[key]["ratio"], xd, yd)), e[key]["eta"], 1e-4, key + " on the drawn curve")
    assert e["m_large"]["eta"] > 2.0 * e["m_small"]["eta"], "the large flow is more than twice as efficient"
    save_figure(fig, "p54-propulsive-efficiency")


def fig_turbojet_stages():
    """Lesson: pressure rises through the compressor, holds through the combustor and falls through
    the turbine and nozzle, and the turbine takes back only the temperature rise the compressor needs."""
    W = 6.5
    xl, yl = (-0.14, 1.16), (-0.36, 0.47)
    k_in = W / (xl[1] - xl[0])                       # inches per meter
    h_eng = (yl[1] - yl[0]) * k_in
    h_pan, gap, bot, top = 1.55, 0.18, 0.46, 0.02
    H = top + h_eng + gap + h_pan + gap + h_pan + bot
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0.0, (H - top - h_eng) / H, 1.0, h_eng / H])
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal"); ax.axis("off")
    g = draw_turbojet_section(ax)
    S = g["stations"]
    fh, fc = g["f_hub"], g["f_cas"]
    flow_arrow(ax, (-0.135, 0.12), (-0.035, 0.12), width=6.0, head_width=11.0, head_len=7.0)
    text(ax, (-0.085, 0.12), "air in", direction=90, dist=8, fs=FS_SMALL)
    flow_arrow(ax, (1.045, 0.0), (1.145, 0.0), width=6.0, head_width=11.0, head_len=7.0)
    text(ax, (1.095, 0.0), "exhaust", direction=-90, dist=9, fs=FS_SMALL)
    nc, nt = CJ610_STAGES["compressor"], CJ610_STAGES["turbine"]
    # numbered callouts in flow order, each leader ending in a dot on its part (upper half)
    xc_ = 0.5 * sum(_patch_x(g["rotors"]["compressor"][4]))
    xt_ = 0.5 * sum(_patch_x(g["rotors"]["turbine"][1]))
    liner = g["liners"][0]
    targets = {"inlet": (0.05, 0.5 * float(fc(0.05) + 0.11)),
               "compressor": (xc_, 0.5 * float(fh(xc_) + fc(xc_))),
               "combustor": (0.60, liner["r_out"]),
               "turbine": (xt_, 0.5 * float(fh(xt_) + fc(xt_))),
               "nozzle": (0.97, 0.5 * float(fc(0.97) + fh(0.97)))}
    names = [("inlet", "inlet"), ("compressor", f"compressor,\n{nc} stages"), ("combustor", "combustor"),
             ("turbine", f"turbine,\n{nt} stages"), ("nozzle", "nozzle")]
    y_d = 0.33
    for k, (key, nm) in enumerate(names, start=1):
        xm = g["mid"](key)
        numbered_callout(ax, targets[key], k, (xm, y_d))
        text(ax, (xm, y_d), nm, direction=90, dist=11, fs=FS_SMALL)
    # rotor and stator, named once on the lower half
    rr_ = g["rotors"]["compressor"][nc + 2]
    ss_ = g["stators"]["compressor"][nc + 4]
    for p_, (tx, ty), word in ((rr_, (0.12, -0.30), "rotor row (turns)"), (ss_, (0.40, -0.30), "stator row (fixed)")):
        x_ = 0.5 * sum(_patch_x(p_))
        y_ = -0.5 * float(fh(x_) + fc(x_))
        ax.plot([x_, tx], [y_, ty + 0.012], color=INK, lw=0.7, zorder=8.5)
        ax.plot([x_], [y_], "o", ms=2.6, color=INK, zorder=9)
        text(ax, (tx, ty), word, direction=-90, dist=1, fs=FS_SMALL)
    text(ax, (0.29, -0.042), "one shaft", fs=FS_SMALL, backing=False)
    # the drawing: real proportions and stage counts
    wx0, wx1 = _patch_x(g["walls"][0])
    wy0, wy1 = _patch_y(g["walls"][0])
    close_to(2.0 * wy1, CJ610_D, 1e-6, "largest diameter drawn at the published value")
    close_to(wx1 - wx0, CJ610_L, 1e-9, "length drawn at the published value")
    assert len(g["rotors"]["compressor"]) == 2 * nc and len(g["rotors"]["turbine"]) == 2 * nt, "stage counts drawn"
    for ln in g["liners"]:
        assert S["combustor"][0] < ln["x_front"] and ln["x_exit"] < _patch_x(g["stators"]["turbine"][0])[0], \
            "the liner sits in the combustor and stays open ahead of the first turbine vanes"
    # the two panels: pressure and temperature along the engine, on the drawing's x scale
    xs, ps, Ts, c = _cycle_along(S)
    y_p = (bot + h_pan + gap) / H
    axp = fig.add_axes([0.0, y_p, 1.0, h_pan / H])
    axT = fig.add_axes([0.0, bot / H, 1.0, h_pan / H])
    for a in (axp, axT):
        a.set_xlim(*xl)
        for sp in ("top", "right", "bottom"):
            a.spines[sp].set_visible(False)
        a.spines["left"].set_position(("data", -0.10))
        a.grid(True, color=GRID, lw=0.6, axis="y"); a.set_axisbelow(True)
        a.set_xticks([])
        a.plot([-0.10, CJ610_L], [0, 0], color=INK, lw=0.8, zorder=3)
        for key in ("compressor", "combustor", "turbine", "nozzle"):
            a.plot([S[key][0]] * 2, [0, 1e4], **line_kw("boundary"), zorder=2)
        a.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: fmt_dec(v, 0)))
    axp.plot(xs, ps / 1000.0, **required_kw(0), zorder=4)
    axT.plot(xs, Ts, **required_kw(0), zorder=4)
    axp.set_ylim(0, 920); axp.set_yticks([0, 200, 400, 600, 800])
    axT.set_ylim(0, 1230); axT.set_yticks([0, 400, 800, 1200])
    axp.set_ylabel("Pressure, kPa", fontsize=FS_SMALL)
    axT.set_ylabel("Temperature, K", fontsize=FS_SMALL)
    axT.text(0.5 * (xl[0] + xl[1]), -95, "Position along the engine (stations as in the drawing)", ha="center",
             va="top", fontsize=FS_SMALL, color=INK)
    for k, key in enumerate(("inlet", "compressor", "combustor", "turbine", "nozzle"), start=1):
        disc(axp, (g["mid"](key), 860), k)
    x3, x5 = S["compressor"][1], S["turbine"][1]
    point(axp, (x3, c["p3"] / 1000.0), fmt(c["p3"] / 1000.0, 4) + " kPa", direction=-45, dist=6, fs=FS_SMALL)
    point(axp, (x5, c["p5"] / 1000.0), fmt(c["p5"] / 1000.0, 4) + " kPa", direction=15, dist=9, fs=FS_SMALL)
    point(axp, (CJ610_L, c["p0"] / 1000.0))
    axp.plot([-0.10, CJ610_L], [c["p0"] / 1000.0] * 2, color=GRAY, lw=LW_THIN, ls=(0, (1.0, 2.0)), zorder=3)
    text(axp, (0.60, c["p0"] / 1000.0), "ambient pressure,\n" + fmt(c["p0"] / 1000.0, 4) + " kPa", direction=90,
         dist=3, fs=FS_SMALL)
    # the temperature rise inside the compressor and the drop inside the turbine, each measured from a
    # dotted reference line at the temperature where the stage begins
    x_rise = 0.5 * (S["compressor"][0] + S["compressor"][1]) + 0.02
    x_drop = 0.5 * (S["turbine"][0] + S["turbine"][1])
    for x0_, x1_, yy, grp in ((S["inlet"][0], x_rise, c["T0"], "rise"), (x_rise, x3, c["T3"], "rise"),
                              (S["turbine"][0], x_drop, c["T4"], "drop"), (x_drop, x5, c["T5"], "drop")):
        axT.plot([x0_, x1_], [yy, yy], color=GRAY, lw=LW_THIN, ls=(0, (1.0, 2.0)), zorder=3, gid="grp:dim" + grp)
    for xd, y0, y1, grp in ((x_rise, c["T0"], c["T3"], "rise"), (x_drop, c["T5"], c["T4"], "drop")):
        # a dimension between the two reference lines: its shaft crosses the curve, so the shaft is a plain
        # line and the two heads are short arrows at its ends, clear of the curve
        axT.plot([xd, xd], [y0, y1], color=INK, lw=LW_THIN, zorder=7, gid="grp:dim" + grp)
        k_pt = 1230.0 / (h_pan * 72.0)                            # kelvin per point on this panel
        for y_end, sgn in ((y0, 1.0), (y1, -1.0)):
            arrow(axT, (xd, y_end + sgn * 5.0 * k_pt), (xd, y_end), color=INK, lw=LW_THIN, head=(5.0, 2.2),
                  zorder=7).set_gid("grp:dim" + grp)
    axT.text(x_rise - 0.012, 0.5 * (c["T0"] + c["T3"]) + 60, "rise\n" + fmt(c["dT"], 4) + " K", ha="right",
             va="bottom", fontsize=FS_SMALL, color=INK, zorder=7)
    axT.text(S["nozzle"][0] + 0.015, c["T4"] - 40, "drop " + fmt(c["dT"], 4) + " K", ha="left", va="center",
             fontsize=FS_SMALL, color=INK, zorder=7)
    assert S["compressor"][0] < x_rise < S["compressor"][1], "the rise arrow stands inside the compressor"
    assert S["turbine"][0] < x_drop < S["turbine"][1], "the drop arrow stands inside the turbine"
    close_to(float(np.max(ps)), c["p3"], 1e-6, "pressure peaks leaving the compressor")
    close_to(float(xs[int(np.argmax(Ts))]), S["combustor"][1], 1e-9, "temperature peaks leaving the combustor")
    close_to(c["T4"] - c["T5"], c["T3"] - c["T0"], 1e-9, "turbine drop = compressor rise")
    fig.canvas.draw()
    close_to(float(axp.transData.transform((0.5, 0))[0]), float(ax.transData.transform((0.5, 0))[0]), 0.5,
             "panels aligned with the drawing")
    save_figure(fig, "p54-turbojet-stages")


def fig_thrust_distribution():
    """Lesson: the thrust is the small difference between large forward loads on the compressor and
    combustion chamber and large rearward loads on the turbine and nozzle."""
    fig, ax = data_axes(6.5, 4.2, grid=False)
    fig.subplots_adjust(left=0.14, right=0.99, bottom=0.23, top=0.97)
    ax.grid(True, axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    run = 0.0
    n = len(GAS_LOADS)
    bars = []
    for i, (name, F) in enumerate(GAS_LOADS):
        lo, hi = sorted((run, run + F))
        fwd = F > 0
        bars.append(ax.add_patch(Polygon([[i - 0.32, lo / 1e3], [i + 0.32, lo / 1e3], [i + 0.32, hi / 1e3],
                                          [i - 0.32, hi / 1e3]], closed=True, fc=(FWD_FILL if fwd else "white"),
                                         ec=INK, lw=1.0, hatch=(None if fwd else "////"), zorder=4)))
        lab = ("+" if fwd else "−") + fmt_dec(abs(F), 0)
        text(ax, (i, max(lo, hi) / 1e3), lab, direction=90, dist=4, fs=FS_SMALL)
        ax.plot([i + 0.32, i + 0.68], [(run + F) / 1e3] * 2, color=INK, lw=LW_THIN, ls=DASH_CONSTRUCTION, zorder=3)
        run += F
    net = ax.add_patch(Polygon([[n - 0.32, 0], [n + 0.32, 0], [n + 0.32, run / 1e3], [n - 0.32, run / 1e3]],
                               closed=True, fc=INK, ec=INK, lw=1.0, zorder=4))
    text(ax, (n, run / 1e3), fmt_dec(run, 0), direction=90, dist=4, fs=FS_SMALL)
    for k, (fc, hatch, word) in enumerate(((FWD_FILL, None, "forward load on the part"),
                                            ("white", "////", "rearward load on the part"))):
        yk = 58.0 - 5.0 * k
        ax.add_patch(Polygon([[3.85, yk - 1.6], [4.25, yk - 1.6], [4.25, yk + 1.6], [3.85, yk + 1.6]], closed=True,
                             fc=fc, ec=INK, lw=1.0, hatch=hatch, zorder=4))
        text(ax, (4.25, yk), word, direction=0, dist=5, fs=FS_SMALL)
    ax.set_xlim(-0.6, n + 0.6); ax.set_ylim(0, 62)
    ax.set_xticks(np.arange(n + 1))
    ax.set_xticklabels(["compressor", "diffuser", "combustion\nchamber", "turbine", "exhaust\nunit and\njet pipe",
                        "propelling\nnozzle", "thrust"], fontsize=FS_SMALL)
    ax.set_ylabel("Forward load added up from\nthe front, thousands of lb")
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60])
    # measured on the drawn bars: each bar's height is its load, and the net bar is what is left
    for (name, F), b in zip(GAS_LOADS, bars):
        y0, y1 = _patch_y(b)
        close_to((y1 - y0) * 1e3, abs(F), 1e-6, name + " bar height")
    close_to(_patch_y(net)[1] * 1e3, GAS_NET, 1e-6, "net thrust bar")
    close_to(sum(F for _, F in GAS_LOADS if F > 0), GAS_FWD, 1e-9, "forward loads add to the figure's total")
    close_to(-sum(F for _, F in GAS_LOADS if F < 0), GAS_AFT, 1e-9, "rearward loads add to the figure's total")
    assert max(_patch_y(b)[1] for b in bars) > 4.0 * _patch_y(net)[1], "the drawn peak is several times the thrust"
    save_figure(fig, "p54-thrust-distribution")


def fig_turbofan():
    """Lesson: most of the air goes around the core, and each stream has its own exhaust speed; the
    low-pressure turbine at the rear turns the fan."""
    top, det = TF_PANELS
    fig, (ax, axd), kax, ss = _stack([top, det], gap=0.34, key_h=0.92, head=0.26, key_gap=0.05)
    g = draw_turbofan_section(ax)
    gd = draw_turbofan_section(axd, core_only=True, sides=(1,))
    enl = ss[1] / ss[0]
    panel_title(ax, "whole engine, in section")
    panel_title(axd, f"core, upper half, drawn {fmt(enl, 2)} times larger")
    flow_arrow(ax, (-0.84, 0.45), (-0.56, 0.45))
    text(ax, (-0.70, 0.45), "air in", direction=90, dist=9, fs=FS_SMALL)
    flow_arrow(ax, (1.48, 0.70), (1.92, 0.70))
    text(ax, (1.92, 0.70), "bypass stream, cooler and slower:\nṁ$_\\mathrm{bypass}$ at $V_{e,\\mathrm{bypass}}$",
         direction=0, dist=5, fs=FS_LABEL, ha="left")
    flow_arrow(ax, (2.82, -0.27), (3.22, -0.27))
    text(ax, (3.22, -0.27), "core stream,\nhotter and faster:\nṁ$_\\mathrm{core}$ at $V_{e,\\mathrm{core}}$",
         direction=0, dist=5, fs=FS_LABEL, ha="left")
    fh, fcs = gd["f_hub"], gd["f_cas"]
    mid = lambda x: 0.5 * float(fh(x) + fcs(x))                                  # noqa: E731
    cx = lambda p: 0.5 * sum(_patch_x(p))                                       # noqa: E731
    # callouts 1 and 2 on the lower half, each leader from open air: 1 through the inlet to the fan,
    # 2 through the open end of the bypass duct
    numbered_callout(ax, (0.20, -0.52), 1, (-0.74, -0.64))
    numbered_callout(ax, (1.28, -0.61), 2, (1.75, -0.96))
    r_lpc, r_hpc = gd["rotors"]["lpc"][1], gd["rotors"]["hpc"][4]
    r_hpt, r_lpt = gd["rotors"]["hpt"][0], gd["rotors"]["lpt"][2]
    ln = gd["liner"]
    yd = 0.54
    for n_, tg, at in ((3, (cx(r_lpc), mid(cx(r_lpc))), (0.72, yd)), (4, (cx(r_hpc), mid(cx(r_hpc))), (1.28, yd)),
                       (5, (1.70, ln["r_out"]), (1.70, yd)), (6, (cx(r_hpt), mid(cx(r_hpt))), (1.96, yd)),
                       (7, (cx(r_lpt), mid(cx(r_lpt))), (2.26, yd)), (8, (1.945, 0.018), (1.975, 0.155))):
        numbered_callout(axd, tg, n_, at)
    _key(kax, ["fan", "bypass duct and its guide vanes", "low-pressure compressor", "high-pressure compressor",
               "combustor", "high-pressure turbine", "low-pressure turbine, turns the fan",
               "two shafts, one inside the other"])
    # measured on the drawing
    ny = [_patch_y(p) for p in g["nacelle"]]
    close_to(max(y[1] for y in ny) - min(y[0] for y in ny), CFM56_H, 1e-6, "fan case drawn at the published height")
    for k, n_st in CFM56_STAGES.items():
        assert len(g["rotors"][k]) == n_st, f"{k}: {n_st} rotor rows drawn"
    lp, hp = g["lp_shaft"], g["hp_shaft"]
    assert lp[3] < hp[2] and lp[0] <= hp[0] and lp[1] >= hp[1], "the low-pressure shaft runs inside the hollow one"
    assert lp[0] <= cx(g["rotors"]["fan"][0]) and lp[1] >= _patch_x(g["rotors"]["lpt"][0])[0], \
        "the low-pressure shaft joins the fan to the low-pressure turbine"
    assert g["a_bypass"] > 3.0 * g["a_core"], "the bypass annulus is several times the core annulus"
    assert float(np.max(g["f_cowl"](np.linspace(0.52, 2.75, 200)))) <= 0.48 + 1e-9, "a flat core cowl"
    xs_sp, rs_sp = g["spinner"]
    assert rs_sp[0] == 0.0 and np.all(np.diff(rs_sp) > 0), "a pointed spinner rising to the fan root"
    assert 1.8 <= enl <= 2.6, "the core drawn at about twice the scale"
    save_figure(fig, "p54-turbofan")


def fig_turboprop():
    """Lesson: almost all the energy of the gas goes to a shaft that turns a propeller through a gearbox."""
    top, det = TP_PANELS
    fig, (ax, axd), kax, ss = _stack([top, det], gap=0.34, key_h=0.92, head=0.26, key_gap=0.05)
    g = draw_turboprop_section(ax)
    gd = draw_turboprop_section(axd, core_only=True, sides=(1,))
    enl = ss[1] / ss[0]
    panel_title(ax, "whole engine, in section")
    panel_title(axd, f"core and power turbine, upper half, drawn {fmt(enl, 2)} times larger")
    flow_arrow(ax, (0.27, 0.68), (0.35, 0.37), width=6.0, head_width=11.0, head_len=7.0)
    text(ax, (0.27, 0.68), "air in", direction=90, dist=4, fs=FS_SMALL)
    flow_arrow(ax, (3.08, 0.24), (3.32, 0.24), width=6.0, head_width=11.0, head_len=7.0)
    text(ax, (3.20, 0.24), "slow exhaust", direction=-90, dist=9, fs=FS_SMALL)
    fh, fcs = gd["f_hub"], gd["f_cas"]
    mid = lambda x: 0.5 * float(fh(x) + fcs(x))                                  # noqa: E731
    cx = lambda p: 0.5 * sum(_patch_x(p))                                       # noqa: E731
    gb = g["gearbox"]
    numbered_callout(ax, (-0.06, -0.45), 1, (-0.32, -0.45))
    numbered_callout(ax, (0.5 * (gb[0] + gb[1]), -gb[3]), 2, (0.5 * (gb[0] + gb[1]), -0.84))
    r_c = gd["rotors"]["compressor"][6]
    r_ct, r_pt = gd["rotors"]["compressor_turbine"][0], gd["rotors"]["power_turbine"][1]
    ln = gd["liner"]
    yd = 0.355
    for n_, tg, at in ((3, (cx(r_c), mid(cx(r_c))), (1.08, yd)), (4, (1.66, ln["r_out"]), (1.62, yd)),
                       (5, (cx(r_ct), mid(cx(r_ct))), (1.90, yd)), (6, (cx(r_pt), mid(cx(r_pt))), (2.30, yd)),
                       (7, (2.07, 0.013), (2.07, 0.085))):
        numbered_callout(axd, tg, n_, at)
    _key(kax, ["propeller (blades cut short)", f"reduction gearbox, {fmt(AE2100['gear'], 4)} to 1",
               f"compressor, {AE2100_STAGES['compressor']} stages", "combustor",
               "compressor turbine, turns the compressor", "power turbine, turns the propeller",
               "power-turbine shaft, to the gearbox"])
    # measured on the drawing
    close_to(_patch_x(g["duct_wall"])[1], AE2100_L, 1e-6, "the exhaust duct ends at the published length")
    for k, n_st in AE2100_STAGES.items():
        assert len(g["rotors"][k]) == n_st, f"{k}: {n_st} rotor rows drawn"
    pt, cs = g["pt_shaft"], g["c_shaft"]
    assert gb[0] < pt[0] < gb[1], "the power-turbine shaft ends inside the gearbox"
    assert pt[3] < cs[2] and pt[0] < cs[0] and pt[1] > cs[1], "it runs inside the hollow compressor shaft"
    assert pt[1] >= _patch_x(g["rotors"]["power_turbine"][0])[0], "it reaches the power turbine"
    assert g["inlet_gap"] > 0.08, "the inlet lip leaves an open annulus above the housing"
    hb = max(_patch_y(p)[1] for p in g["blades"])
    assert hb > _patch_y(g["inlet_wall"])[1], "the propeller blade root reaches above the inlet lip"
    assert all(math.hypot(gx - 0.5 * (gb[0] + gb[1]), gy) + gr <= gb[3] + 1e-9 for gx, gy, gr in g["gears"]), \
        "the gears sit inside the ring gear"
    assert 1.8 <= enl <= 2.6, "the core drawn at about twice the scale"
    save_figure(fig, "p54-turboprop")


def fig_mach_bands():
    """Lesson: each engine family works well only in its own band of flight speed."""
    w3 = _ex3()
    fig = plt.figure(figsize=(6.5, 3.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15], wspace=0.05)
    axL, axR = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.19, top=0.98)
    n = len(MACH_BANDS)
    lims = ((axL, (0.0, M_SPLIT)), (axR, (M_SPLIT, 10.0)))
    for a, (x0, x1) in lims:
        a.set_xlim(x0, x1); a.set_ylim(-0.6, n - 0.3)
        a.set_yticks([])
        for sp in ("top", "right", "left"):
            a.spines[sp].set_visible(False)
        a.grid(True, axis="x", color=GRID, lw=0.6); a.set_axisbelow(True)
        a.tick_params(labelsize=FS_SMALL)
    axL.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0]); axR.set_xticks([2, 4, 6, 8, 10])
    axL.axvline(1.0, **line_kw("boundary"), zorder=2)
    fig.text(0.5, 0.02, f"Flight Mach number (the scale changes at Mach {fmt(M_SPLIT, 2)})", ha="center",
             fontsize=FS_LABEL)
    drawn = {}
    for i, (name, (b0, b1), ext, _src) in enumerate(MACH_BANDS):
        y = n - 1 - i
        for a, (x0, x1) in lims:
            if b1 <= x0 or b0 >= x1:
                continue
            u0, u1 = max(b0, x0), min(b1, x1)                 # the part of the band on this scale
            pa = a.add_patch(Polygon([[u0, y - 0.2], [u1, y - 0.2], [u1, y + 0.2], [u0, y + 0.2]], closed=True,
                                     fc=HIGHLIGHT, ec="none", zorder=4))
            drawn.setdefault(name, []).append(pa)
            for yy in (y - 0.2, y + 0.2):
                a.plot([u0, u1], [yy, yy], color=INK, lw=1.0, zorder=5, solid_capstyle="butt")
            for xe in (b0, b1):
                if x0 <= xe <= x1:
                    a.plot([xe, xe], [y - 0.2, y + 0.2], color=INK, lw=1.0, zorder=5)
            if ext:
                drawn[name + " ext"] = a.add_patch(Polygon([[ext[0], y - 0.2], [ext[1], y - 0.2], [ext[1], y + 0.2],
                                                            [ext[0], y + 0.2]], closed=True, fc="white", ec=INK,
                                                           lw=1.0, hatch="////", zorder=4))
    text(axL, (0.02, n - 1 + 0.2), "propeller, piston or turbine", direction=90, dist=3, fs=FS_SMALL, ha="left")
    text(axL, (0.55, n - 1 - 0.2), "advanced propellers", direction=-90, dist=3, fs=FS_SMALL)
    text(axL, (0.7, n - 2), "high-bypass turbofan, cruise", direction=180, dist=4, fs=FS_SMALL)
    text(axR, (2.4, n - 3 + 0.2), "turbofan or turbojet with afterburner", direction=90, dist=3, fs=FS_SMALL,
         ha="left")
    text(axR, (4.75, n - 4 + 0.2), "ramjet", direction=90, dist=3, fs=FS_SMALL)
    text(axR, (7.2, n - 5 + 0.2), "scramjet", direction=90, dist=3, fs=FS_SMALL)
    text(axL, (1.0, n - 0.3), "Mach 1", direction=0, dist=4, fs=FS_SMALL, ha="left")
    for a in (axL, axR):
        a.plot([M_SPLIT], [-0.6], marker=(2, 0, 60), ms=10, color=INK, clip_on=False, zorder=9)
    # measured on the drawn bars: each band's ends, across the change of scale
    for name, (b0, b1), ext, _src in MACH_BANDS:
        xs_ = [_patch_x(p) for p in drawn[name]]
        close_to(min(x[0] for x in xs_), b0, 1e-9, name + " band starts where the source puts it")
        close_to(max(x[1] for x in xs_), b1, 1e-9, name + " band ends where the source puts it")
    prop, fan = MACH_BANDS[0][0], MACH_BANDS[1][0]
    assert _patch_x(drawn[prop + " ext"])[1] < _patch_x(drawn[fan][0])[0], \
        "a gap between the propeller band and the turbofan's cruise band"
    assert _patch_x(drawn[prop][0])[0] < w3["M"] < _patch_x(drawn[prop][0])[1], \
        "the cruise of worked example 3 lies inside the drawn propeller band"
    save_figure(fig, "p54-mach-bands")


def make_all():
    fig_propulsive_efficiency()
    fig_turbojet_stages()
    fig_thrust_distribution()
    fig_turbofan()
    fig_turboprop()
    fig_mach_bands()


# ===================================================================== printed values
def values():
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731
    # worked example 1
    e = _ex1()
    r("ex1-V", fmt(EX1["V"], 3)); r("ex1-T-kN", fmt(EX1["T"] / 1e3, 3)); r("ex1-T", fmt(EX1["T"], 5))
    for tag, key in (("s", "m_small"), ("l", "m_large")):
        q = e[key]
        r(f"ex1-{tag}-m", fmt(q["m"], 3))
        r(f"ex1-{tag}-dV", fmt(q["Ve"] - EX1["V"], 4))
        r(f"ex1-{tag}-Ve", fmt(q["Ve"], 4))
        r(f"ex1-{tag}-eta", fmt(q["eta"], 4))
        r(f"ex1-{tag}-wasted-MW", fmt(q["wasted"] / 1e6, 4))
    r("ex1-useful-MW", fmt(e["m_small"]["useful"] / 1e6, 4)); r("ex1-useful-W", fmt_dec(e["m_small"]["useful"], 0))
    r("ex1-s-wasted-W", fmt_dec(e["m_small"]["wasted"], 0)); r("ex1-l-wasted-W", fmt_dec(e["m_large"]["wasted"], 0))
    r("ex1-mass-ratio", fmt(EX1["m_large"] / EX1["m_small"], 3))
    # the turbojet of the stage figure
    c = _cycle()
    r("cyc-pic", fmt(CYCLE["pi_c"], 1)); r("cyc-T4", fmt(CYCLE["T4"], 4))
    r("cyc-p0", fmt(c["p0"] / 1e3, 4))
    r("cyc-p3", fmt(c["p3"] / 1e3, 4)); r("cyc-dT", fmt(c["dT"], 4))
    r("cyc-p5", fmt(c["p5"] / 1e3, 4))
    r("cj610-stages-c", str(CJ610_STAGES["compressor"])); r("cj610-stages-t", str(CJ610_STAGES["turbine"]))
    # thrust distribution
    for name, F in GAS_LOADS:
        r("load-" + name.split()[0], fmt_dec(abs(F), 0))
    r("load-fwd", fmt(GAS_FWD, 5)); r("load-aft", fmt(GAS_AFT, 5)); r("load-net", fmt(GAS_NET, 5))
    r("load-fwd-kN", fmt(GAS_FWD * LBF / 1e3, 4))
    r("load-net-kN", fmt(GAS_NET * LBF / 1e3, 4))
    r("load-net-pct", fmt(100.0 * GAS_NET / GAS_FWD, 3))
    r("cyc-pt-ratio", fmt(c["p3"] / c["p5"], 4))
    # published facts
    r("bpr-high-lo", str(BPR_HIGH[0])); r("bpr-high-hi", str(BPR_HIGH[1]))
    r("bpr-ab-lo", fmt(BPR_AB[0], 1)); r("bpr-ab-hi", fmt(BPR_AB[1], 1)); r("f100-bpr", fmt(F100["bpr"], 2))
    r("f100-tsfc-dry", fmt(F100["tsfc_dry"], 2)); r("f100-tsfc-ab", fmt(F100["tsfc_ab"], 3))
    r("f100-tsfc-ratio", fmt(F100["tsfc_ab"] / F100["tsfc_dry"], 3))
    r("ae2100-gear", fmt(AE2100["gear"], 4)); r("ae2100-P-lo", fmt(AE2100["P_lo"], 4))
    r("ae2100-P-hi", fmt(AE2100["P_hi"], 4))
    r("ramjet-limit", fmt(RAMJET_LIMIT_M, 1))
    r("tf-enl", fmt(_enlargement(TF_PANELS), 2)); r("tp-enl", fmt(_enlargement(TP_PANELS), 2))
    for name, (b0, b1), ext, _src in MACH_BANDS:
        tag = name.split()[0].replace(",", "") + ("-fan" if "cruise" in name else "")
        if b0 > 0.0:
            r(f"band-{tag}-lo", _band_str(b0))
        r(f"band-{tag}-hi", _band_str(b1))
        if ext:
            r(f"band-{tag}-ext", _band_str(ext[1]))
    # worked example 2: the executive jet
    w = _ex2()
    ac = EXEC_JET
    r("ej-m", fmt(ac["m"], 5)); r("ej-S", fmt(ac["S"], 3)); r("ej-CD0", fmt(ac["CD0"], 2)); r("ej-K", fmt_dec(ac["K"], 3))
    r("ej-Mlim", fmt_dec(ac["M_limit"], 2)); r("ej-W", fmt(w["W"], 6))
    r("ex2-h", fmt(EX2["h"], 5)); r("ex2-V", fmt(EX2["V"], 3))
    r("ex2-a", fmt(w["a"], 4)); r("ex2-M", fmt(w["M"], 3))
    r("ex2-rho5", fmt(w["rho"], 5)); r("ex2-q", fmt_dec(w["q"], 1))
    r("ex2-D0", fmt_dec(w["D0"], 1)); r("ex2-Di", fmt_dec(w["Di"], 1)); r("ex2-TR", fmt_dec(w["TR"], 1))
    r("ex2-Te", fmt(w["Te"], 5))
    for k in ("jet", "fan"):
        q = w[k]
        r(f"ex2-{k}-m", fmt(q["m"], 3)); r(f"ex2-{k}-dV", fmt(q["dV"], 4))
        r(f"ex2-{k}-Ve", fmt(q["Ve"], 4 if k == "jet" else 5))
        r(f"ex2-{k}-eta", fmt(q["eta"], 4)); r(f"ex2-{k}-A", fmt(q["A"], 4)); r(f"ex2-{k}-d", fmt(q["d"], 3))
    r("ex2-fuel-ratio", fmt(w["fuel_ratio"], 3)); r("ex2-fuel-saving", fmt(100.0 * (1.0 - w["fuel_ratio"]), 2))
    # worked example 3: the transport
    t = _ex3()
    tr = TRANSPORT
    r("tr-m", fmt(tr["m"], 5)); r("tr-S", fmt(tr["S"], 3)); r("tr-CD0", fmt(tr["CD0"], 2))
    r("tr-K", fmt(tr["K"], 4)); r("tr-n", str(tr["n"])); r("tr-P0", fmt(tr["P0"] / 1e3, 4))
    r("tr-eta", fmt(tr["eta"], 2)); r("tr-mg", fmt(t["W"], 6))
    r("ex3-h", fmt(EX3["h"], 4)); r("ex3-rho", fmt(t["rho"], 4)); r("ex3-a", fmt(t["a"], 4))
    r("ex3-CL", fmt(t["CL"], 4)); r("ex3-V", fmt(t["V"], 5)); r("ex3-M", fmt(t["M"], 3))
    r("ex3-D", fmt(t["D"], 5)); r("ex3-Te", fmt(t["Te"], 4)); r("ex3-ratio", fmt(t["ratio"], 4))
    r("ex3-dV", fmt(t["dV"], 4)); r("ex3-m", fmt(t["m"], 4))
    r("ex3-m-over-fan", fmt(100.0 * (t["m_over_fan"] - 1.0), 2))
    r("ex3-Vcl", fmt(EX3["V_climb"], 2)); r("ex3-PA0", fmt(t["PA0"] / 1e3, 4)); r("ex3-PA", fmt(t["PA"] / 1e3, 4))
    r("ex3-TAcl", fmt(t["TA_cl"] / 1e3, 4)); r("ex3-TAcr", fmt(t["TA_cr"] / 1e3, 4))
    r("ex3-D-kN", fmt(t["D"] / 1e3, 4)); r("ex3-ta-ratio", fmt(t["ta_ratio"], 3))
    r("ex3-sig", fmt(t["sig"], 5)); r("ex3-lapse", fmt(t["lapse"], 5)); r("tr-mad", fmt(tr["m_ad"], 2))
