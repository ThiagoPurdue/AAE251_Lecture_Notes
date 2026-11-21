"""Figures and values of 1.4 Standard Atmosphere (notes/chapter-1/standard-atmosphere.md).

One function per figure, make_all() for the runner, and values() for every number the page
prints. Run through the runner from the book folder:

    FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_1_figures.py p14

Every constant comes from chapter_1/atmosphere.py (the model of these notes). Helpers that the
shared code lacks are defined here, prefixed with an underscore.

Worked examples (invented; no
scenario or number set repeats):
  1. a cargo jet cruising at 10,500 m (gradient layer, forward);
  2. a weather balloon at 21,000 m (isothermal layer, base values carried up from sea level);
  3. a glider whose outside pressure reads 61,500 Pa (altitude from a measured pressure),
     with the forward check, and a stratospheric airship that reads 9,500 Pa (the same
     reverse method in the isothermal layer);
  4. Venus at 10 km (the same equations with Venus's surface values, gas constant, gravity
     and lapse rate; sources in atmosphere.PLANETS);
  and a short hot-day case: an airport at 1,800 m on a day 20 K hotter than standard, and the
  pressure at 35,000 m (a gradient layer with a positive lapse rate).
The comparison with the U.S. Standard Atmosphere, 1976 uses a short implementation of that
standard below 47 km (us1976()), from its Table 4 constants.
"""
from chapter_1.common import *
from chapter_1.diagrams import PAD

P = "p14"

# ===================================================================== worked-example choices
EX1_H = 10500.0          # m, cargo jet (gradient layer)
EX2_H = 21000.0          # m, weather balloon (isothermal layer)
EX3_P = 61500.0          # Pa, glider's outside-air pressure (reverse)
EX3B_P = 9500.0          # Pa, stratospheric airship's outside-air pressure (reverse, isothermal layer)
UP_H = 35000.0           # m, the positive-lapse-rate case (upper stratosphere)
EX4_H = 10000.0          # m, Venus
HOT_H, HOT_DT = 1800.0, 20.0     # m and K: airport elevation and temperature shift of the hot day
VENUS = PLANETS["Venus"]["model"]

K_BOLTZ = K_BOLTZMANN    # J/K (atmosphere.py)
R_UNIV = UNIVERSAL_R     # J/(kmol K) (atmosphere.py)
GAMMA = GAMMA_AIR

# the line looks of this page: the standard atmosphere and the comparison case
STD = dict(line_kw(0))
ALT = dict(line_kw(1))
HOT = dict(line_kw(2))
BAND = "#EFEFEF"         # the isothermal layer's band on the plots
MK = dict(ms=7.0, mec=INK, mew=1.0, zorder=9, ls="none")


def exponent():
    """-g0/(aR) of the troposphere (the pressure exponent) and the density exponent."""
    a = LAYERS[0][1]
    n = -G0 / (a * R_AIR)
    return n, n - 1.0


def example1():
    T, p, rho = standard(EX1_H)
    r = T / T_SL
    n, nd = exponent()
    return dict(T=T, r=r, p=P_SL * r ** n, rho=RHO_SL * r ** nd, a=float(speed_of_sound(T)),
                rho_state=p / (R_AIR * T), p_std=p, rho_std=rho)


def base11():
    L = layer_of(15000.0)
    return L["T1"], L["p1"], L["rho1"]


def example2():
    T1, p1, rho1 = base11()
    x = G0 * (EX2_H - H_TROPOPAUSE) / (R_AIR * T1)
    f = math.exp(-x)
    T, p, rho = standard(EX2_H)
    close_to(p, p1 * f, 1e-12, "isothermal equation = standard()")
    return dict(T1=T1, p1=p1, rho1=rho1, r11=T1 / T_SL, x=x, f=f, p=p, rho=rho, a=float(speed_of_sound(T1)))


def example3():
    """Altitude from a measured pressure (gradient layer): T = T0 (p/p0)^(-aR/g0), h = (T - T0)/a."""
    a = LAYERS[0][1]
    k = -a * R_AIR / G0                     # 1/5.2533 = 0.19036
    ratio = EX3_P / P_SL
    T = T_SL * ratio ** k
    h = (T - T_SL) / a
    close_to(h, altitude_from_pressure(EX3_P), 1e-9, "inverse of the gradient equation")
    return dict(ratio=ratio, k=k, T=T, h=h, rho=EX3_P / (R_AIR * T))


def example4():
    m = VENUS
    rho0 = m["p0"] / (m["R"] * m["T0"])
    T = m["T0"] + m["a"] * EX4_H
    n = -m["g"] / (m["a"] * m["R"])
    r = T / m["T0"]
    p = m["p0"] * r ** n
    rho = p / (m["R"] * T)
    Tp, pp, _ = planet(EX4_H, **m)
    close_to(p, float(pp), 1e-12, "Venus pressure")
    pe = standard(EX4_H)[1]
    return dict(rho0=rho0, T=T, n=n, r=r, p=p, rho=rho, earth_p=pe, earth_rho=standard(EX4_H)[2])


def hot_day():
    Ts, ps, rhos = standard(HOT_H)
    Th, ph, rhoh = (float(v) for v in nonstandard(HOT_H, HOT_DT))
    hd = altitude_from_density(rhoh)
    return dict(Ts=Ts, ps=ps, rhos=rhos, Th=Th, ph=ph, rhoh=rhoh, hd=hd,
                T0h=T_SL + HOT_DT, rho0h=P_SL / (R_AIR * (T_SL + HOT_DT)))


def us1976(h):
    """T (K) and p (Pa) of the U.S. Standard Atmosphere, 1976 at geopotential altitude h (m), up
    to 47 km: T0 = 288.15 K, p0 = 101,325 Pa, g0 = 9.80665 m/s^2, R = 287.053 J/(kg K), layer
    bases 0, 11, 20, 32 and 47 km with lapse rates -6.5, 0, +1.0 and +2.8 K/km (NOAA, NASA and
    USAF 1976, Part 1, Table 4)."""
    g, R = 9.80665, 287.053
    T1, p1 = 288.15, 101325.0
    for h1, h2, a in ((0.0, 11000.0, -0.0065), (11000.0, 20000.0, 0.0), (20000.0, 32000.0, 0.001),
                      (32000.0, 47000.0, 0.0028)):
        top = min(h, h2)
        if a == 0.0:
            T, p = T1, p1 * math.exp(-g * (top - h1) / (R * T1))
        else:
            T = T1 + a * (top - h1)
            p = p1 * (T / T1) ** (-g / (a * R))
        if h <= h2:
            return T, p
        T1, p1 = T, p
    return T1, p1


def compare1976():
    """The model of these notes against the 1976 standard: the largest pressure difference up to
    20 km, and the temperatures and pressures at 47 km."""
    hs = np.linspace(0.0, 20000.0, 401)
    dmax = max(abs(float(standard(h)[1]) / us1976(h)[1] - 1.0) for h in hs)
    T47, p47 = us1976(47000.0)
    return dict(dmax=dmax, T47=T47, p47=p47, T47n=float(standard(47000.0)[0]), p47n=float(standard(47000.0)[1]))


def _pv(x, sig=4):
    """(printed string, its value): a number as the page prints it, and the value a student reads."""
    t = fmt(x, sig)
    return t, float(t.replace(",", ""))


def chains():
    """Every printed step of the worked examples, each computed from the digits printed before it
    (as a student redoes it), and checked against the full-precision model within 2e-4."""
    C = {}

    def put(key, x, sig=4, exact=None, tol=2e-4):
        t, v = _pv(x, sig)
        C[key] = t
        C[key + "#"] = v
        if exact is not None:
            close_to(v, exact, tol * abs(exact), f"printed chain {key}")
        return v

    put("L2-p1", layer_bases()[2]["p1"], 4)
    n = put("n", exponent()[0], 5)
    nd = put("nd", n - 1.0, 5)
    # example 1: gradient layer, forward
    e1 = example1()
    T = put("ex1-T", T_SL + LAYERS[0][1] * EX1_H, 5, e1["T"])
    r = put("ex1-r", T / T_SL, 6, e1["r"])
    fp = put("ex1-fp", r ** n, 5)
    fr = put("ex1-fr", r ** nd, 5)
    put("ex1-p", P_SL * fp, 5, e1["p"])
    put("ex1-rho", RHO_SL * fr, 4, e1["rho"])
    put("ex1-rho-state", C["ex1-p#"] / (R_AIR * T), 4, e1["rho"], 4e-4)
    put("ex1-a", math.sqrt(GAMMA * R_AIR * T), 4, e1["a"])
    put("ex1-V", 0.80 * C["ex1-a#"], 4)
    put("ex1-p-kPa", C["ex1-p#"] / 1000.0, 4)
    # example 2: isothermal layer, base values carried up from sea level
    e2 = example2()
    r11 = put("ex2-r11", 216.66 / T_SL, 6, e2["r11"])
    f11 = put("ex2-f11p", r11 ** n, 5)
    g11 = put("ex2-f11r", r11 ** nd, 5)
    p1 = put("ex2-p1", P_SL * f11, 4, e2["p1"])
    rho1 = put("ex2-rho1", RHO_SL * g11, 4, e2["rho1"])
    x = put("ex2-x", G0 * (EX2_H - H_TROPOPAUSE) / (R_AIR * 216.66), 5, e2["x"])
    fx = put("ex2-f", math.exp(-x), 5, e2["f"])
    put("ex2-p", p1 * fx, 4, e2["p"])
    put("ex2-rho", rho1 * fx, 4, e2["rho"])
    put("ex2-p-kPa", C["ex2-p#"] / 1000.0, 4)
    # example 3: altitude from a measured pressure
    e3 = example3()
    q = put("ex3-ratio", EX3_P / P_SL, 5, e3["ratio"])
    k = put("ex3-k", -LAYERS[0][1] * R_AIR / G0, 5, e3["k"])
    T3 = put("ex3-T", T_SL * q ** k, 5, e3["T"])
    put("ex3-h", (T3 - T_SL) / LAYERS[0][1], 4, e3["h"], 1e-3)
    put("ex3-rho", EX3_P / (R_AIR * T3), 4, e3["rho"])
    # example 3, the forward check from the altitude found
    h3 = C["ex3-h#"]
    T3c = put("ex3-Tc", T_SL + LAYERS[0][1] * h3, 5)
    put("ex3-pc", P_SL * (T3c / T_SL) ** n, 5, EX3_P, 1e-4)
    # the same measurement method in the isothermal layer (an airship reads 9,500 Pa)
    Hs = put("H-iso5", R_AIR * 216.66 / G0, 4)
    lnr = put("ex3b-ln", math.log(p1 / EX3B_P), 5)
    h3b = put("ex3b-h", H_TROPOPAUSE + Hs * lnr, 5, altitude_from_pressure(EX3B_P), 1e-4)
    put("ex3b-dh", h3b - H_TROPOPAUSE, 4)
    put("ex3b-rho", EX3B_P / (R_AIR * 216.66), 4, float(standard(altitude_from_pressure(EX3B_P))[2]), 1e-3)
    put("ex3b-pc", p1 * math.exp(-G0 * (h3b - H_TROPOPAUSE) / (R_AIR * 216.66)), 4, EX3B_P, 2e-4)
    # a positive lapse rate: the pressure at 35,000 m
    b2 = layer_bases()[2]
    nup = put("up-n", -G0 / (b2["a"] * R_AIR), 5)
    Tup = put("up-T", 216.66 + b2["a"] * (UP_H - b2["h1"]), 5, float(standard(UP_H)[0]))
    fup = put("up-f", (Tup / 216.66) ** nup, 5)
    put("up-p", C["L2-p1#"] * fup, 4, float(standard(UP_H)[1]), 2e-3)
    # example 4: Venus
    e4 = example4()
    m = VENUS
    Rv = put("v-R", UNIVERSAL_R / PLANETS["Venus"]["molar_mass"], 5, m["R"])
    put("v-rho0", m["p0"] / (Rv * m["T0"]), 3, e4["rho0"], 2e-3)
    Tv = put("v-T", m["T0"] + m["a"] * EX4_H, 3, e4["T"], 1e-3)
    nv = put("v-n", -m["g"] / (m["a"] * Rv), 5, e4["n"])
    rv = put("v-r", Tv / m["T0"], 6, e4["r"])
    fv = put("v-f", rv ** nv, 5)
    pv = put("v-p-MPa", m["p0"] / 1e6 * fv, 4, e4["p"] / 1e6)
    put("v-rho", pv * 1e6 / (Rv * Tv), 4, e4["rho"])
    put("v-p-kPa", pv * 1000.0, 4)
    # hot day
    hd = hot_day()
    T0h = put("hot-T0h", T_SL + HOT_DT, 5)
    Th = put("hot-Th", T0h + LAYERS[0][1] * HOT_H, 5, hd["Th"])
    rh = put("hot-r", Th / T0h, 6)
    fh = put("hot-f", rh ** n, 5)
    ph = put("hot-ph", P_SL * fh, 4, hd["ph"])
    rhoh = put("hot-rhoh", ph / (R_AIR * Th), 4, hd["rhoh"])
    qh = put("hot-q", rhoh / RHO_SL, 5)
    kd = put("hot-kd", 1.0 / nd, 5)
    Td = put("hot-Td", T_SL * qh ** kd, 6)
    put("hot-hd", (Td - T_SL) / LAYERS[0][1], 4, hd["hd"], 1e-3)
    put("hot-Ts", T_SL + LAYERS[0][1] * HOT_H, 5, hd["Ts"])
    put("hot-rhos", hd["rhos"], 4)
    return C


# ===================================================================== small helpers
def _km(h):
    return np.asarray(h, dtype=float) / 1000.0


def _log_ticks(ax, axis, ticks, labels=None):
    a = ax.xaxis if axis == "x" else ax.yaxis
    (ax.set_xticks if axis == "x" else ax.set_yticks)(ticks)
    a.set_major_formatter(mticker.FixedFormatter(labels or [f"{t:,g}" for t in ticks]))
    a.set_minor_formatter(mticker.NullFormatter())
    a.set_minor_locator(mticker.NullLocator())


def _lines_height(ax, lines, fs=FS_LABEL, pad=PAD):
    """Height (data) of a box holding these lines of text, broken as given."""
    return box_height(ax, "\n".join(lines), fs=fs, pad=pad, keep_breaks=True)


def _box_lines(ax, xy, lines, w, h=None, fill=BOX_FILL, fs=FS_LABEL):
    """A diagram box whose text keeps the given line breaks (diagrams.box with keep_breaks)."""
    return box(ax, xy, "\n".join(lines), w=w, h=h, fill=fill, fs=fs, keep_breaks=True)


def _molecule(ax, xy, zorder=6):
    ax.plot(*xy, "o", ms=6.0, color=INK, zorder=zorder)


# ===================================================================== figures
def gas_properties():
    """What pressure, density and temperature measure, molecule by molecule (schematic)."""
    fig, axs = new_axes(6.5, 2.95, ncols=3)
    W, H, Y0 = 10.0, 12.6, -0.9
    for ax in axs:
        ax.set_xlim(0.0, W)
        ax.set_ylim(Y0, H)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005, wspace=0.06)
    vk = ARROW_KIND["velocity"]
    for ax, name in zip(axs, ("pressure", "density", "temperature")):
        ax.add_patch(Polygon([(0.15, 2.0), (9.85, 2.0), (9.85, 10.9), (0.15, 10.9)], closed=True, fc="none",
                             ec=GRAY, lw=LW_THIN, zorder=1))
        text(ax, (5.0, 11.8), name, backing=False)

    def molecules(ax, pts):
        for (x, y), (vx, vy) in pts:
            _molecule(ax, (x, y))
            arrow(ax, (x, y), (x + vx, y + vy), color=vk["color"], lw=1.3, head="small", zorder=6)

    # (a) pressure: molecules strike a surface; the normal force dF on a small area dA
    ax = axs[0]
    wall = ax.add_patch(opaque(Polygon([(7.6, 2.0), (8.6, 2.0), (8.6, 10.9), (7.6, 10.9)], closed=True,
                                       fc="#FFFFFF", ec=INK, lw=LW_OUTLINE, zorder=3)))
    wall.set_hatch("////")
    ax.plot([7.6, 7.6], [5.3, 7.5], color=AGED, lw=5.0, solid_capstyle="butt", zorder=4)
    callout(ax, (7.5, 7.3), "area $dA$", at=(5.0, 8.5), ha="right", fs=FS_SMALL)
    kind_arrow(ax, (4.6, 6.4), (7.45, 6.4), "force")
    text(ax, (4.6, 6.4), "force $dF$", direction=180, dist=4, fs=FS_SMALL)
    molecules(ax, [((1.3, 9.9), (1.3, -0.5)), ((1.5, 3.3), (1.4, 0.6)), ((5.0, 2.9), (1.3, 0.5)),
                   ((6.3, 9.7), (-1.2, 0.5))])
    text(ax, (5.0, 0.9), "$p = dF/dA$", backing=False)

    # (b) density: the mass of the molecules inside a small volume dv
    ax = axs[1]
    x0, y0, s, d = 2.6, 4.4, 3.8, 1.3
    front = ax.add_patch(Polygon([(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s)], closed=True,
                                 fc=LIGHT, ec=INK, lw=LW_DETAIL, zorder=3))
    ax.plot([x0, x0 + d, x0 + s + d, x0 + s + d, x0 + s], [y0 + s, y0 + s + d, y0 + s + d, y0 + d, y0],
            color=INK, lw=LW_DETAIL, zorder=3)
    ax.plot([x0 + s, x0 + s + d], [y0 + s, y0 + s + d], color=INK, lw=LW_DETAIL, zorder=3)
    for xy in ((3.4, 5.2), (5.6, 5.5), (4.3, 6.6), (3.3, 7.5), (5.6, 7.5)):
        _molecule(ax, xy, zorder=5)
    for xy in ((1.0, 2.9), (8.9, 3.1), (1.0, 10.0), (8.9, 6.4)):
        _molecule(ax, xy)
    text(ax, (x0 + 0.5 * (s + d), y0 + s + d), "volume $dv$", direction=90, dist=5, fs=FS_SMALL)
    text(ax, (x0 + s / 2, y0), "mass $dm$ inside", direction=-90, dist=6, fs=FS_SMALL)
    text(ax, (5.0, 0.9), "$\\rho = dm/dv$", backing=False)

    # (c) temperature: random motion; the average kinetic energy of one molecule
    ax = axs[2]
    pts = [((1.5, 9.4), (1.5, 0.5)), ((5.4, 9.8), (-0.8, 0.8)), ((8.0, 8.6), (1.0, -1.0)), ((4.2, 6.8), (-1.7, -0.6)),
           ((6.3, 5.2), (0.5, 1.4)), ((1.6, 4.4), (1.1, -1.0)), ((8.2, 3.6), (-0.6, -0.9))]
    molecules(ax, pts)
    text(ax, (5.0, 3.0), "random\nvelocities", backing=False, color=TEXT_KIND["velocity"], fs=FS_SMALL)
    text(ax, (5.0, 0.45), "mean kinetic energy of a\nmolecule, $(3/2)\\,kT$", backing=False, fs=FS_SMALL)
    assert len(pts) == 7 and front is not None
    save_figure(fig, "p14-gas-properties")


def slab_balance():
    """Force balance on a thin slab of still air: the hydrostatic equation (schematic)."""
    fig, ax = new_axes(6.5, 4.3)
    set_frame(ax, -2.2, 13.0, -1.8, 10.2)
    # the column of still air, with the slab highlighted
    cx0, cx1 = 0.4, 2.4
    ax.add_patch(opaque(Polygon([(cx0, 0.0), (cx1, 0.0), (cx1, 9.0), (cx0, 9.0)], closed=True, fc=GAS_FILL,
                                ec=INK, lw=LW_DETAIL, zorder=2)))
    ys0, ys1 = 5.0, 5.45
    ax.add_patch(opaque(Polygon([(cx0, ys0), (cx1, ys0), (cx1, ys1), (cx0, ys1)], closed=True, fc=GOLD,
                                ec=INK, lw=LW_DETAIL, zorder=3)))
    ground = ax.add_patch(Polygon([(-0.4, -0.55), (3.2, -0.55), (3.2, 0.0), (-0.4, 0.0)], closed=True, fc="white",
                                  ec=INK, lw=LW_DETAIL, zorder=2))
    ground.set_hatch("////")
    kind_arrow(ax, (-0.9, 0.0), (-0.9, 9.4), "dimension")
    text(ax, (-0.9, 9.4), "altitude, $h$", direction=90, dist=4)
    text(ax, (1.4, 7.4), "still\nair", backing=False, fs=FS_SMALL)
    text(ax, (1.4, -0.55), "ground", direction=-90, dist=4)
    # zoom lines to the enlarged slab
    X0, X1, Y0, Y1 = 5.6, 10.8, 3.6, 5.8
    for (a, b) in (((cx1, ys1), (X0, Y1)), ((cx1, ys0), (X0, Y0))):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=GRAY, lw=LW_THIN, ls=(0, (3, 2)), zorder=1)
    ax.add_patch(opaque(Polygon([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)], closed=True, fc=LIGHT, ec=INK,
                                lw=LW_OUTLINE, zorder=3)))
    text(ax, (7.9, 0.5 * (Y0 + Y1) + 0.1), "slab: area $dA$,\nmass $\\rho\\,dA\\,dh$", backing=False, fs=FS_SMALL)
    dimension(ax, (X1, Y0), (X1, Y1), "$dh$", offset=-0.7, label_side=-1)
    # forces, drawn so that their lengths balance: up = down + weight (the difference exaggerated)
    up, top, wt = 3.5, 1.3, 2.2
    xa, xw = 6.2, 10.15
    yc = 0.5 * (Y0 + Y1)
    kind_arrow(ax, (xa, Y0 - up), (xa, Y0), "force")
    text(ax, (xa, Y0 - up), "pressure force from\nbelow, $p\\,dA$", direction=-90, dist=4)
    kind_arrow(ax, (xa, Y1 + top), (xa, Y1), "force")
    text(ax, (xa, Y1 + top), "pressure force from above, $(p + dp)\\,dA$", direction=90, dist=4, ha="left",
         offset=(-12, 0))
    point(ax, (xw, yc), None, ms=5.0, zorder=8)
    kind_arrow(ax, (xw, yc), (xw, yc - wt), "force")
    text(ax, (xw, yc - wt), "weight,\n$\\rho\\,g_0\\,dA\\,dh$", direction=-90, dist=4)
    close_to(up, top + wt, 1e-12, "the drawn forces balance")
    save_figure(fig, "p14-slab-balance")


def temperature_layers():
    """The temperature of the standard atmosphere against altitude, layer by layer (computed)."""
    h = np.linspace(0.0, 53000.0, 1061)
    T = standard(h)[0]
    fig, ax = data_axes(6.5, 4.6)
    ax.set_xlim(195.0, 314.0)
    ax.set_ylim(0.0, 53.0)
    bases = layer_bases()
    for L in bases[:4]:
        if L["a"] == 0.0:
            ax.axhspan(_km(L["h1"]), _km(L["h2"]), color=BAND, lw=0, zorder=0)
    for hb in (11.0, 25.0, 47.0):
        ax.axhline(hb, **line_kw("boundary"), zorder=1)
    ln = ax.plot(T, _km(h), **STD, zorder=4)[0]
    ax.set_xlabel("Temperature $T$, K")
    ax.set_ylabel("Altitude $h$, km")
    ax.set_yticks([0, 11, 25, 47, 53])
    ax.set_xticks([200, 220, 240, 260, 280, 300])
    text(ax, (199.0, 2.4), "troposphere, gradient layer", ha="left", va="center")
    text(ax, (250.0, 8.5), "lapse rate $a$ = −0.0065 K/m", ha="left", va="center")
    text(ax, (311.0, 18.0), "lower stratosphere\nisothermal layer, $T$ = 216.66 K", ha="right", va="center",
         backing=BAND)
    text(ax, (199.0, 36.0), "upper stratosphere\ngradient layer\n$a$ = +0.003 K/m", ha="left", va="center")
    text(ax, (199.0, 50.0), "stratopause: isothermal layer, $T$ = 282.66 K", ha="left", va="center", backing=BAND)
    ax.plot([T_SL], [0.0], "o", color=INK, ms=6, zorder=6, clip_on=False)
    text(ax, (T_SL, 0.0), "288.16 K\nat sea level", direction=50, dist=7, ha="left", va="bottom")
    close_to(float(np.interp(11.0, _km(h), T)), 216.66, 1e-6, "tropopause temperature drawn")
    close_to(float(np.interp(47.0, _km(h), T)), 282.66, 1e-6, "47 km temperature drawn")
    assert ln is not None
    save_figure(fig, "p14-temperature-layers")


def pressure_density():
    """Pressure and density against altitude on log scales, with the worked examples (computed)."""
    h = np.linspace(0.0, 30000.0, 1201)
    T, p, rho = standard(h)
    e1, e2, e3 = example1(), example2(), example3()
    fig, (a1, a2) = data_axes(6.5, 5.4, ncols=2, sharey=True)
    fig.subplots_adjust(wspace=0.12)
    mk = dict(MK, ms=6.0)
    for ax in (a1, a2):
        ax.set_xscale("log")
        ax.set_ylim(0.0, 30.0)
        ax.set_yticks([0, 5, 10, 15, 20, 25, 30])
        for hb in (11.0, 25.0):
            ax.axhline(hb, **line_kw("boundary"), zorder=1)
        ax.axhspan(11.0, 25.0, color=BAND, lw=0, zorder=0)
    a1.plot(p / 1000.0, _km(h), **STD, zorder=4)
    a2.plot(rho, _km(h), **STD, zorder=4)
    a1.set_xlim(1.0, 200.0)
    _log_ticks(a1, "x", [1, 3, 10, 30, 100])
    a2.set_xlim(0.01, 2.0)
    _log_ticks(a2, "x", [0.01, 0.03, 0.1, 0.3, 1])
    for ax in (a1, a2):
        ax.grid(True, which="major", color=GRID, lw=0.6, zorder=0.5)
    a1.set_xlabel("Pressure $p$, kPa (log scale)")
    a2.set_xlabel("Density $\\rho$, kg/m³ (log scale)")
    a1.set_ylabel("Altitude $h$, km")
    # the layers, named once, in the left panel
    text(a1, (195.0, 11.0), "11 km", direction=90, dist=3, ha="right", fs=FS_SMALL, backing=BAND)
    text(a1, (195.0, 25.0), "25 km", direction=90, dist=3, ha="right", fs=FS_SMALL, backing=False)
    text(a1, (20.0, 15.0), "isothermal layer:\nstraight line", ha="left", va="center", fs=FS_SMALL, backing=False)
    text(a1, (1.25, 1.8), "gradient layer:\ncurved", ha="left", va="center", fs=FS_SMALL, backing=False)   # in the troposphere, where the bend shows
    # the examples: circle 1, square 2, triangle 3
    a1.plot([e1["p"] / 1000.0], [_km(EX1_H)], "o", mfc="white", **mk)
    a1.plot([e2["p"] / 1000.0], [_km(EX2_H)], "s", mfc="white", **mk)
    a2.plot([e1["rho"]], [_km(EX1_H)], "o", mfc="white", **mk)
    a2.plot([e2["rho"]], [_km(EX2_H)], "s", mfc="white", **mk)
    a2.plot([e3["rho"]], [_km(e3["h"])], "^", mfc="white", **mk)
    # example 3: read the altitude from the measured pressure
    pk, hk = EX3_P / 1000.0, _km(e3["h"])
    a1.plot([pk, pk], [0.0, hk], color=INK, lw=LW_THIN, ls=(0, (2, 2)), zorder=3)
    a1.plot([1.0, pk], [hk, hk], color=INK, lw=LW_THIN, ls=(0, (2, 2)), zorder=3)
    a1.plot([pk], [hk], "^", mfc="white", **mk)
    text(a1, (1.12, hk + 0.5), f"Ex. 3: {fmt(EX3_P / 1000.0, 3)} kPa\ngives {fmt(e3['h'])} m", ha="left",
         va="bottom", fs=FS_SMALL, backing=False)
    text(a1, (e1["p"] / 1000.0, _km(EX1_H)), f"Ex. 1, {fmt(EX1_H / 1000.0, 3)} km:\n{fmt(e1['p'] / 1000.0)} kPa",
         direction=-165, dist=7, ha="right", va="top", fs=FS_SMALL, backing=False)
    text(a1, (e2["p"] / 1000.0, _km(EX2_H)), f"Ex. 2, {fmt(EX2_H / 1000.0, 2)} km:\n{fmt(e2['p'] / 1000.0)} kPa",
         direction=30, dist=6, ha="left", va="bottom", fs=FS_SMALL, backing=BAND)
    text(a2, (e1["rho"], _km(EX1_H)), f"Ex. 1: {fmt(e1['rho'])} kg/m³", direction=-165, dist=7, ha="right",
         va="top", fs=FS_SMALL, backing=False)
    text(a2, (e2["rho"], _km(EX2_H)), f"Ex. 2:\n{fmt(e2['rho'])} kg/m³", direction=30, dist=6, fs=FS_SMALL,
         ha="left", va="bottom", backing=BAND)
    text(a2, (e3["rho"], _km(e3["h"])), f"Ex. 3: {fmt(e3['rho'])} kg/m³", direction=180, dist=7, fs=FS_SMALL,
         backing=False, ha="right")
    # assert: in the isothermal layer log p is linear in h (constant slope), in the gradient layer it is not
    lp = np.log(p)
    s_iso = np.diff(lp[(h >= 11000) & (h <= 25000)])
    s_grad = np.diff(lp[h <= 11000])
    assert np.ptp(s_iso) < 1e-9 * abs(s_iso.mean()) + 1e-12 and np.ptp(s_grad) > 0.1 * abs(s_grad.mean())
    assert float(rho[-1]) > 0.01, "the density curve reaches 30 km inside the axis"
    save_figure(fig, "p14-pressure-density")


def method_flow():
    """The method: find the layer, start from its base, carry the base values up (schematic)."""
    bw, gapb = 3.8, 0.30                       # layer boxes: width and the gap between them (data)
    W = 3 * bw + 2 * gapb                       # width of the full-width boxes
    cx = 6.62
    x0, x1 = -0.12, cx + W / 2 + 0.14
    fig, ax = canvas((x1 - x0) / 2.0, xlim=(x0, x1), ylim=(1.16, 12.92))
    b1 = lines_box(ax, (cx, 12.45), ["Write the altitude $h$ in meters"], w=7.0, fill=BOX_FILL_START)
    q = "Which layer holds $h$?"
    dw, dh, _ = decision_size(ax, q, w=7.0, h=2.6)
    d = decision(ax, (cx, b1.cy - b1.h / 2 - pt(ax, 18) - dh / 2), q, w=dw, h=dh)
    lines = [["0 to 11,000 m", "gradient layer", "$a$ = −0.0065 K/m", "base: sea level"],
             ["11,000 to 25,000 m", "isothermal layer", "$T$ = 216.66 K", "base: 11,000 m"],
             ["25,000 to 47,000 m", "gradient layer", "$a$ = +0.003 K/m", "base: 25,000 m"]]
    hb = lines_box_height(4, FS_SMALL, ax=ax)
    yb = d.cy - dh / 2 - pt(ax, 24) - hb / 2
    xs = [cx - bw - gapb, cx, cx + bw + gapb]
    bl = [lines_box(ax, (x, yb), L, w=bw, h=hb, fs=FS_SMALL) for x, L in zip(xs, lines)]
    t3 = ["Take the base values $T_1$, $p_1$, $\\rho_1$ of that layer,",
          "carried up from sea level through every layer below"]
    h3 = lines_box_height(2, ax=ax)
    b3 = lines_box(ax, (cx, yb - hb / 2 - pt(ax, 22) - h3 / 2), t3, w=W)
    t4 = ["Compute $T$ first, then $p$ and $\\rho$,", "with the equations of that layer"]
    b4 = lines_box(ax, (cx, b3.cy - b3.h / 2 - pt(ax, 20) - h3 / 2), t4, w=W)
    t5 = ["Check: $p = \\rho R T$, and $p$ lies between", "the values at the base and the top of the layer"]
    b5 = lines_box(ax, (cx, b4.cy - b4.h / 2 - pt(ax, 20) - h3 / 2), t5, w=W, fill=BOX_FILL_START)
    route(ax, b1, "bottom", d, "top")
    route(ax, d, "bottom", bl[1], "top")
    route(ax, d, "left", bl[0], "top")
    route(ax, d, "right", bl[2], "top")
    for bx_ in bl:
        route(ax, bx_, "bottom", b3, "top", dst_f=(bx_.cx - (b3.cx - b3.w / 2)) / b3.w)
    route(ax, b3, "bottom", b4, "top")
    route(ax, b4, "bottom", b5, "top")
    # the five step numbers in one column, left of the full-width boxes
    xd = cx - W / 2 - pt(ax, 9.0) - pt(ax, 4.0)
    for n, y in ((1, b1.cy), (2, d.cy), (3, b3.cy), (4, b4.cy), (5, b5.cy)):
        step_marker(ax, (xd, y), n)
    gaps = [bl[1].cx - bl[1].w / 2 - (bl[0].cx + bl[0].w / 2), bl[2].cx - bl[2].w / 2 - (bl[1].cx + bl[1].w / 2)]
    assert min(gaps) >= pt(ax, 10.0) - 1e-9, "the layer boxes keep 10 pt apart"
    assert 1.16 < b5.cy - b5.h / 2 < 1.45, f"the chart fills its frame ({b5.cy - b5.h / 2:.2f})"
    save_figure(fig, "p14-method-flow")


def example_ladder():
    """Worked example 2 drawn: the base values carried from sea level to 11 km, then to 21 km (computed)."""
    e2 = example2()
    fig = plt.figure(figsize=(6.5, 4.9))
    ylo, yhi = -6.0, 24.0
    bot, top = 0.012, 0.985                      # the right panel (boxes) in figure fractions
    a1 = fig.add_axes([0.415, bot, 0.58, top - bot])
    # the left plot starts at h = 0, level with the sea-level connector of the right panel
    f0 = bot + (top - bot) * (0.0 - ylo) / (yhi - ylo)
    a0 = fig.add_axes([0.115, f0, 0.30, top - f0])
    for s_ in ("top", "right"):
        a0.spines[s_].set_visible(False)
    h = np.linspace(0.0, 23000.0, 461)
    T = standard(h)[0]
    a0.plot(T, _km(h), **STD, zorder=4)
    a0.set_xlim(205.0, 300.0)
    a0.set_ylim(0.0, yhi)
    a0.set_xticks([220, 260, 300])
    a0.set_yticks([0, 5, 11, 15, 21])
    a0.set_xlabel("Temperature $T$, K")
    a0.set_ylabel("Altitude $h$, km")
    for hh, mk in ((0.0, "o"), (11.0, "o"), (21.0, "s")):
        Tp = float(standard(hh * 1000.0)[0])
        a0.plot([Tp], [hh], mk, mfc="white" if mk == "s" else INK, clip_on=False, **MK)
        a0.plot([Tp + 4.0, 300.0], [hh, hh], color=GRAY, lw=LW_THIN, ls=(0, (1.5, 2.5)), zorder=2, clip_on=False)
    a1.axis("off")
    fig.canvas.draw()
    bb = a1.get_window_extent()
    xr = (yhi - ylo) * bb.width / bb.height
    a1.set_xlim(0.0, xr)
    a1.set_ylim(ylo, yhi)
    a1.set_aspect("equal")
    fig.canvas.draw()
    bw = 0.80 * xr
    bx = 0.19 * xr
    rows = [
        (0.0, ["Sea level, $h$ = 0 m", "$T$ = 288.16 K,  $p$ = 101,325 Pa", "$\\rho$ = 1.2250 kg/m³"], BOX_FILL),
        (11.0, ["Isothermal-layer base, $h_1$ = 11,000 m",
                f"$T_1$ = {fmt(e2['T1'], 5)} K,  $p_1$ = {fmt(e2['p1'])} Pa", f"$\\rho_1$ = {fmt(e2['rho1'])} kg/m³"],
         BOX_FILL),
        (21.0, ["The balloon, $h$ = 21,000 m", f"$T$ = {fmt(e2['T1'], 5)} K,  $p$ = {fmt(e2['p'])} Pa",
                f"$\\rho$ = {fmt(e2['rho'])} kg/m³"], BOX_FILL_START),
    ]
    hb = lines_box_height(3, FS_SMALL, ax=a1)
    # the sea-level box hangs below its connector; the other two are centered on their altitude
    ys = [0.0 - hb / 2, 11.0, 21.0]
    boxes = [lines_box(a1, (bx + bw / 2, y), L, w=bw, h=hb, fill=f, fs=FS_SMALL) for y, (_, L, f) in zip(ys, rows)]
    for y in (0.0, 11.0, 21.0):
        a1.plot([0.0, bx - pt(a1, 3)], [y, y], color=GRAY, lw=LW_THIN, ls=(0, (1.5, 2.5)), zorder=2)
    a1.plot([bx - pt(a1, 3), bx], [0.0, 0.0], color=GRAY, lw=LW_THIN, ls=(0, (1.5, 2.5)), zorder=2)
    labels = ("step 2: gradient-layer equations,\nfrom sea level", "steps 3 and 4: isothermal-layer\nequations, from 11,000 m")
    for i, lab in enumerate(labels):
        route(a1, boxes[i], "top", boxes[i + 1], "bottom", src_f=0.12, dst_f=0.12)
        ym = 0.5 * (boxes[i].cy + boxes[i].h / 2 + boxes[i + 1].cy - boxes[i + 1].h / 2)
        text(a1, (bx + 0.12 * bw, ym), lab, direction=0, dist=8, fs=FS_SMALL, ha="left")
    close_to(boxes[0].cy + boxes[0].h / 2, 0.0, 1e-9, "the sea-level box hangs from h = 0")
    close_to(e2["p"], float(standard(EX2_H)[1]), 1e-12, "the box shows the computed pressure")
    save_figure(fig, "p14-example-ladder")


def earth_venus():
    """Earth's standard atmosphere and the Venus model at one scale (computed)."""
    hv = np.linspace(0.0, PLANETS["Venus"]["valid_to"], 321)
    Tv, pv, _ = planet(hv, **VENUS)
    he = np.linspace(0.0, 32000.0, 321)
    Te, pe, _ = standard(he)
    e4 = example4()
    fig, (a1, a2) = data_axes(6.5, 4.0, ncols=2, sharey=True)
    fig.subplots_adjust(wspace=0.16)
    a1.plot(Te, _km(he), **STD, zorder=4)
    a1.plot(Tv, _km(hv), **ALT, zorder=4)
    a2.plot(pe / 1000.0, _km(he), **STD, zorder=4)
    a2.plot(pv / 1000.0, _km(hv), **ALT, zorder=4)
    for ax in (a1, a2):
        ax.set_ylim(0.0, 32.0)
        ax.set_yticks([0, 10, 20, 30])
    a1.set_xlim(150.0, 800.0)
    a1.set_xticks([200, 400, 600])
    a2.set_xscale("log")
    a2.set_xlim(0.5, 30000.0)
    _log_ticks(a2, "x", [1, 10, 100, 1000, 10000], ["1", "10", "$10^2$", "$10^3$", "$10^4$"])
    a2.grid(True, color=GRID, lw=0.6)
    a1.set_xlabel("Temperature $T$, K")
    a2.set_xlabel("Pressure $p$, kPa (log scale)")
    a1.set_ylabel("Altitude above the surface, km")
    a1.plot([e4["T"]], [_km(EX4_H)], "o", mfc="white", **MK)
    a2.plot([e4["p"] / 1000.0], [_km(EX4_H)], "o", mfc="white", **MK)
    text(a1, (e4["T"], _km(EX4_H)), f"Ex. 4: {fmt(e4['T'], 3)} K", direction=180, dist=8, fs=FS_SMALL, ha="right")
    text(a2, (e4["p"] / 1000.0, _km(EX4_H)), f"Ex. 4:\n{fmt(e4['p'] / 1000.0)} kPa", direction=180, dist=8,
         fs=FS_SMALL, ha="right")
    text(a1, (250.0, 18.0), "Earth", color=text_color(0), backing=False, ha="left")
    text(a1, (640.0, 24.0), "Venus", color=text_color(1), backing=False, ha="left")
    text(a2, (1.3, 5.0), "Earth", color=text_color(0), backing=False, ha="left")
    text(a2, (3000.0, 26.0), "Venus", color=text_color(1), backing=False, ha="left")
    assert float(pv[-1]) > 5.0 * P_SL, "Venus at 32 km is still above Earth's sea-level pressure"
    save_figure(fig, "p14-earth-venus")


def hot_day_figure():
    """A day 20 K hotter than standard: temperature and density, and the density altitude (computed)."""
    hd = hot_day()
    h = np.linspace(0.0, 4000.0, 401)
    Ts, _, rs = standard(h)
    Th, _, rh = nonstandard(h, HOT_DT)
    fig, (a1, a2) = data_axes(6.5, 4.2, ncols=2, sharey=True)
    fig.subplots_adjust(wspace=0.14)
    a1.plot(Ts, h, **STD, zorder=4)
    a1.plot(Th, h, **HOT, zorder=4)
    a2.plot(rs, h, **STD, zorder=4)
    a2.plot(rh, h, **HOT, zorder=4)
    for ax in (a1, a2):
        ax.set_ylim(0.0, 4000.0)
        ax.set_yticks([0, 1000, 2000, 3000, 4000])
        ax.axhline(HOT_H, color=GRAY, lw=LW_THIN, ls=(0, (4, 3)), zorder=2)
    a1.set_ylabel("Altitude $h$, m")
    a1.set_xlim(240.0, 315.0)
    a1.set_xticks([240, 260, 280, 300])
    a1.set_xlabel("Temperature $T$, K")
    a2.set_xlim(0.70, 1.30)
    a2.set_xticks([0.8, 1.0, 1.2])
    a2.set_xlabel("Density $\\rho$, kg/m³")
    y = 3000.0
    Tsy = float(standard(y)[0])
    dimension(a1, (Tsy, y), (Tsy + HOT_DT, y), None, extension=False, ticks=False)
    text(a1, (Tsy, y), "$\\Delta T$ = 20 K", direction=180, dist=6, fs=FS_SMALL)
    text(a1, (242.0, HOT_H), "airport\n1,800 m", direction=-90, dist=4, ha="left", fs=FS_SMALL, backing=False)
    text(a1, (250.0, 900.0), "standard", ha="left", backing=False, color=text_color(0))
    text(a1, (292.0, 3700.0), "hot day", ha="left", backing=False, color=text_color(2))
    text(a2, (1.0, 3650.0), "standard", ha="left", backing=False, color=text_color(0))
    text(a2, (0.84, 600.0), "hot day", backing=False, color=text_color(2))
    # the airport and the density altitude
    a2.plot([hd["rhoh"], hd["rhoh"]], [HOT_H, hd["hd"]], color=INK, lw=LW_THIN, ls=(0, (2, 2)), zorder=3)
    a2.plot([hd["rhoh"]], [HOT_H], "o", mfc="white", **MK)
    a2.plot([hd["rhoh"]], [hd["hd"]], "D", mfc="white", **MK)
    a2.plot([hd["rhos"]], [HOT_H], "o", mfc=INK, **MK)
    text(a2, (hd["rhoh"], HOT_H), f"hot day:\n{fmt(hd['rhoh'])} kg/m³", direction=-140, dist=8,
         fs=FS_SMALL, ha="right", va="top")
    text(a2, (hd["rhoh"], hd["hd"]), f"density altitude\n{fmt(hd['hd'])} m, where\nstandard air has\nthe hot-day density",
         direction=20, dist=9, fs=FS_SMALL, ha="left", va="bottom")
    text(a2, (hd["rhos"], HOT_H), f"standard:\n{fmt(hd['rhos'])} kg/m³", direction=35, dist=8, fs=FS_SMALL,
         ha="left", va="bottom")
    close_to(float(np.interp(hd["rhoh"], rs[::-1], h[::-1])), hd["hd"], 2e-3, "density altitude read from the curve")
    save_figure(fig, "p14-hot-day")


def make_all():
    gas_properties()
    slab_balance()
    temperature_layers()
    pressure_density()
    method_flow()
    example_ladder()
    earth_venus()
    hot_day_figure()


# ===================================================================== values
def values():
    r = lambda k, v: record(P, k, v)          # noqa: E731
    C = chains()
    for k, v in C.items():
        if not k.endswith("#"):
            r(k, v)
    # constants and definitions
    r("ke-sl", fmt(1.5 * K_BOLTZ * T_SL * 1e21))          # printed as 5.968 x 10^-21 J
    r("R-from-M", fmt(R_UNIV / M_AIR))
    r("R-univ", fmt(R_UNIV, 5))
    r("M-air", fmt(M_AIR))
    r("M-venus", fmt(PLANETS["Venus"]["molar_mass"]))
    r("rho-state-sl", fmt(P_SL / (R_AIR * T_SL), 5))
    r("rho-celsius", fmt(P_SL / (R_AIR * (T_SL - 273.15)), 3))
    r("dpdh-sl", fmt(RHO_SL * G0))
    r("H-iso", fmt(R_AIR * 216.66 / G0))
    r("column-mass", fmt(P_SL / G0))
    # geopotential and geometric altitude at 20 km (r0 = 6,356.766 km, U.S. Standard Atmosphere 1976)
    r("geopot-pct", fmt(100.0 * 20.0 / (6356.766 - 20.0), 1))
    # against the U.S. Standard Atmosphere, 1976
    cmp_ = compare1976()
    assert cmp_["dmax"] < 0.002, "the two models agree to within 0.2% up to 20 km"
    r("us76-T47", fmt(cmp_["T47"], 5))
    r("us76-p47-pct", fmt(100.0 * (cmp_["p47n"] / cmp_["p47"] - 1.0), 1))
    r("R-univ-mol", fmt(R_UNIV / 1000.0, 5))
    r("us76-dmax", fmt(100.0 * cmp_["dmax"], 1))
    b = layer_bases()
    r("p-drop-25", fmt(P_SL / b[2]["p1"], 3))
    r("rho-drop-25", fmt(RHO_SL / b[2]["rho1"], 3))
    # layer table
    for i, L in enumerate(layer_bases()[:5]):
        r(f"L{i}-T1", fmt(L["T1"], 5))
        r(f"L{i}-p1", fmt(L["p1"]))
        r(f"L{i}-rho1", fmt(L["rho1"]) if i else fmt_dec(RHO_SL, 4))
    # percentages and comparisons in the text
    r("ex1-rho-pct", fmt(100.0 * C["ex1-rho#"] / RHO_SL, 2))
    r("ex2-pct", fmt(100.0 * C["ex2-p#"] / P_SL, 2))
    r("ex2-wrong-p", fmt(P_SL * math.exp(-G0 * EX2_H / (R_AIR * 216.66))))
    r("ex2-a", fmt(float(speed_of_sound(216.66))))
    e4 = example4()
    r("v-earth-ratio", fmt(e4["p"] / e4["earth_p"], 3))
    r("v-p32-kPa", fmt(float(planet(32000.0, **VENUS)[1]) / 1000.0, 3))
    r("a-sl", fmt(float(speed_of_sound(T_SL))))
    r("a-11", fmt(float(speed_of_sound(216.66))))
    hd = hot_day()
    r("hot-pct", fmt(100.0 * (1.0 - hd["rhoh"] / hd["rhos"]), 2))
    r("ex2-above", fmt(100.0 * (1.0 - C["ex2-p#"] / P_SL), 3))
    r("ex2-check", fmt_dec(C["ex2-p#"] / (C["ex2-rho#"] * R_AIR * 216.66), 3))
    r("ex1-V-wrong", fmt(0.80 * float(fmt(float(speed_of_sound(T_SL))))))
    r("ex1-V-err", fmt(100.0 * (0.80 * 340.3 / C["ex1-V#"] - 1.0), 2))
    r("v-p32-ratio", fmt(float(planet(32000.0, **VENUS)[1]) / P_SL, 2))
    r("v-T32", fmt(float(planet(32000.0, **VENUS)[0]), 3))
    r("earth-p32-kPa", fmt(float(standard(32000.0)[1]) / 1000.0))
    r("p-sl-kPa", fmt(P_SL / 1000.0))
    r("hot-dh", fmt(C["hot-hd#"] - HOT_H, 3))
    # quiz values (checked here, printed only in quickcheck/quiz-1-4.html, from scripts/quizzes/1.4.json)
    close_to(float(fmt(70000.0 / (R_AIR * 253.15))), 0.9635, 1e-12, "quiz q2 key")
    close_to(float(fmt(70000.0 / (R_AIR * 273.15))), 0.8929, 1e-12, "quiz q2 distractor, 273.15 K")
    close_to(float(fmt(70000.0 / (8.314 * 253.15))), 33.26, 1e-12, "quiz q2 distractor, universal R")
    close_to(float(fmt(70000.0 / (R_AIR * -20.0))), -12.20, 1e-12, "quiz q2 distractor, Celsius")
    close_to(float(standard(19000.0)[0]), 216.66, 1e-9, "quiz q4 key")
    close_to(T_SL - 0.0065 * 19000.0, 164.66, 1e-9, "quiz q4 distractor")
    close_to(216.66 + 0.003 * 8000.0, 240.66, 1e-9, "quiz q4 distractor")
    assert layer_of(altitude_from_pressure(16000.0))["name"] == "lower stratosphere", "quiz q6 key"
    close_to(float(fmt(0.70 * 295.0)), 206.5, 1e-12, "quiz q7 key")
    close_to(float(fmt(0.70 * 340.3)), 238.2, 1e-12, "quiz q7 distractor")
    close_to(float(fmt(295.0 / 0.70)), 421.4, 1e-12, "quiz q7 distractor")
    close_to(float(fmt(0.70 * math.sqrt(R_AIR * 216.66))), 174.6, 1e-12, "quiz q7 distractor")
