"""Page 3.1 Wind Tunnels: figures and printed values.

Figures (notes/chapter-3/figures/):
  p31-open-circuit       side view of the open-circuit tunnel of worked example 1, parts named
  p31-closed-circuit     plan view of a closed-circuit tunnel, the parts it adds named
  p31-manometer-tunnel   the U-tube manometer between the settling chamber and the test section
  p31-pressure-along-tunnel  area, speed and static pressure along the axis (worked example 1)
  p31-boundary-layer     laminar, transition and turbulent profiles on a flat plate
  p31-viscosity          viscosity of air against temperature, Sutherland's law and table points
  p31-reynolds-ladder    Reynolds numbers from a swimming bacterium to an airliner wing
  p31-scale-speed        the speed a model needs to match the full-size Reynolds number

Sources (each opened):
  - Leishman, J. G., Introduction to Aerospace Flight Vehicles (Embry-Riddle, open textbook):
    Chapter 13 (viscosity rises with temperature for a gas, falls for a liquid; sea-level
    mu = 1.789e-5 kg/(m s)); Chapter 15, eq. (43) (Sutherland: mu = 1.458e-6 T^1.5/(T + 110.4));
    Chapter 18 (Re_x of about 5 x 10^5 for transition on a smooth flat plate, a guide that
    depends on roughness, pressure gradient and free-stream turbulence; the worked example of a
    wing of mean chord 2.75 m at Mach 0.82 and 30,000 ft; jet airplanes 10^7 to 10^8, model
    aircraft and small UAVs 10^3 to 10^5); Chapter 26 (delta = 5.0 sqrt(nu x / V) for the
    laminar Blasius layer; delta = 0.37 x / Re_x^(1/5) for a layer turbulent from the leading
    edge; the one-seventh power profile); Chapter 71 (tunnel parts, open and closed circuits,
    contraction ratio about 7, diffuser half-angle below about 3 deg, the fan makes up the
    losses, blockage below about 5 percent, the Wright brothers' 1901 tunnel, the NACA Variable
    Density Tunnel of 1922 at up to 20 atmospheres, Reynolds-Mach conflict, trips).
  - NOAA, NASA and USAF, U.S. Standard Atmosphere, 1976, Table III (dynamic viscosity, read on
    the scanned pages 98, 100, 102 and 106 of the report): 1.9421e-5 at H = -5,000 m (320.65 K),
    1.7894e-5 at 0 m (288.15 K), 1.6281e-5 at 5,000 m (255.65 K), 1.4216e-5 above 11,000 m
    (216.65 K).
  - Purcell, E. M., "Life at Low Reynolds Number", Am. J. Phys. 45, 3 (1977), pp. 3 and 4: a
    swimming person about 10^4, a goldfish about 10^2, micron-size swimmers moving 30 um/s in
    water (kinematic viscosity 10^-2 cm^2/s) about 10^-4 to 10^-5.
  - NASA Glenn Research Center, Beginner's Guide (open return, closed return, types of tunnels;
    the speed ranges subsonic, transonic 0.8 to 1.2, supersonic 1.2 to 5, hypersonic above 5).
  - NASA Langley, National Transonic Facility (NASA Common Research Model site): pressurized,
    cryogenic nitrogen down to -250 deg F.
Every worked-example value is invented: the oil manometer, the contraction ratio 7.5, the 1.2 m
test section, the 75 m airship and its 1:75 model.
"""
from chapter_3.common import *        # noqa: F401,F403
from matplotlib.patches import Polygon as _Poly
from matplotlib.transforms import Bbox

PAGE = "p31"

# ----------------------------------------------------------------- worked example 1 (the tunnel)
EX1 = dict(ratio=7.5, H2=1.2, rho_l=830.0, dh=0.200, rho=RHO_SL, p_room=P_SL, T=T_SL, g=G0,
           loss_frac=0.10,       # assumed total-pressure loss, test section to diffuser exit, as a fraction of q2
           V_set=40.0)           # the wanted test-section speed of the reverse use of the manometer (invented)
# ----------------------------------------------------------------- worked example 2 (the airship)
EX2 = dict(L_full=75.0, V_full=25.0, D_full=18.0, scale=75.0)
RE_TR = RE_TR_PLATE              # 5 x 10^5, Leishman Chapter 18 (opened)

# published data (chapter_3/published.py): the viscosity table of the U.S. Standard Atmosphere
# 1976, Leishman's airliner wing (Chapter 18) and Purcell's swimmers (1977)
USSA_MU = USSA_MU_POINTS
AIRLINER = LEISHMAN_AIRLINER
BACTERIUM = PURCELL_BACTERIUM


def _decade(v):
    """A power of ten as math: 1e4 -> "10^{4}"."""
    return f"10^{{{int(round(math.log10(v)))}}}"


def tunnel_outline():
    """The open-circuit tunnel of worked example 1: square sections, 1.2 m test section,
    contraction ratio 7.5 (tunnel.open_circuit_side)."""
    return open_circuit_side(H2=EX1["H2"], ratio=EX1["ratio"])


def ex1():
    e = dict(EX1)
    e["dp"] = manometer_dp(e["dh"], e["rho_l"], e["g"])
    e["area_term"] = 1.0 - 1.0 / e["ratio"] ** 2
    e["inv_ratio_sq"] = 1.0 / e["ratio"] ** 2
    e["V2"] = test_section_speed(e["dp"], e["rho"], e["ratio"])
    e["V1"] = settling_speed(e["V2"], e["ratio"])
    e["a"] = speed_of_sound(e["T"])
    e["M2"] = e["V2"] / e["a"]
    e["q2"] = float(dynamic_pressure(e["rho"], e["V2"]))
    e["q1"] = float(dynamic_pressure(e["rho"], e["V1"]))
    e["p1g"] = -e["q1"]                       # gauge pressure in the settling chamber (room air at rest: p0 = p_room)
    e["p2g"] = e["p1g"] - e["dp"]
    e["p1"] = e["p_room"] + e["p1g"]
    e["p2"] = e["p_room"] + e["p2g"]
    e["A2"] = e["H2"] ** 2
    e["A1"] = e["A2"] * e["ratio"]
    T = tunnel_outline()
    x3 = T.stations[3][0][0]
    e["A3"] = float(axis_area(T, [x3])[0])
    e["A3_ratio"] = e["A3"] / e["A2"]
    e["V3"] = e["V2"] * e["A2"] / e["A3"]
    e["q3"] = float(dynamic_pressure(e["rho"], e["V3"]))
    e["loss"] = e["loss_frac"] * e["q2"]
    e["p3g"] = -e["loss"] - e["q3"]
    e["p3g_noloss"] = -e["q3"]
    close_to(e["p2g"], -e["q2"], 1e-9, "Bernoulli from the room: p_room - p2 = q2")
    # the manometer used in reverse: the reading that sets the wanted speed V_set, from printed digits
    e["dp_set"] = 0.5 * e["rho"] * e["V_set"] ** 2 * round(e["area_term"], 5)
    e["dh_set"] = round(e["dp_set"], 1) / (e["rho_l"] * e["g"])
    e["dh_set_check"] = (e["V_set"] / round(e["V2"], 3)) ** 2 * e["dh"]
    close_to(manometer_dh(pressure_difference(e["V_set"], e["rho"], e["ratio"]), e["rho_l"], e["g"]), e["dh_set"], 1e-4,
             "the reverse reading", rel=True)
    return e


def ex2():
    e = dict(EX2)
    v1 = ex1()
    e["L_model"] = e["L_full"] / e["scale"]
    e["D_model"] = e["D_full"] / e["scale"]
    e["V_model"] = v1["V2"]
    e["Re_full"] = reynolds(RHO_SL, e["V_full"], e["L_full"], MU_SL)
    e["Re_model"] = reynolds(RHO_SL, e["V_model"], e["L_model"], MU_SL)
    e["Re_ratio"] = e["Re_full"] / e["Re_model"]
    e["V_match"] = speed_for_reynolds(e["Re_full"], RHO_SL, e["L_model"], MU_SL)
    e["M_match"] = e["V_match"] / v1["a"]
    e["x_tr_model"] = transition_x(RHO_SL, e["V_model"], MU_SL, RE_TR)
    e["x_tr_full"] = transition_x(RHO_SL, e["V_full"], MU_SL, RE_TR)
    e["tr_frac_model"] = e["x_tr_model"] / e["L_model"]
    e["tr_frac_full"] = e["x_tr_full"] / e["L_full"]
    e["A_front"] = math.pi * e["D_model"] ** 2 / 4.0
    e["blockage"] = e["A_front"] / v1["A2"]
    e["V_M03"] = MACH_INCOMPRESSIBLE * v1["a"]
    close_to(e["V_match"], e["V_full"] * e["scale"], 1e-9, "matching speed = full speed times the scale")
    return e


def bacterium_re():
    return BACTERIUM["V"] * BACTERIUM["L"] / BACTERIUM["nu"]


def airliner_re():
    h = AIRLINER["h_ft"] * FT
    T, p, rho = standard(h)[:3]
    a = speed_of_sound(T)
    V = AIRLINER["M"] * a
    mu = float(mu_sutherland(T))
    return dict(h=h, T=T, rho=rho, V=V, mu=mu, Re=reynolds(rho, V, AIRLINER["c"], mu))


# =================================================================== figures
def _open_circuit_axes(T, pad_x=(2.2, 2.4), pad_y=(1.9, 1.5)):
    x0, x1, y0, y1 = T.extent
    return canvas(6.5, xlim=(x0 - pad_x[0], x1 + pad_x[1]), ylim=(y0 - pad_y[0], y1 + pad_y[1]))


def open_circuit():
    """The open-circuit tunnel of worked example 1 with its parts named in flow order and the
    stations 1, 2, 3 marked outside the upper wall."""
    T = tunnel_outline()
    H1 = EX1["H2"] * math.sqrt(EX1["ratio"])
    fig, ax = _open_circuit_axes(T, pad_y=(1.9, 2.5))
    P = draw_tunnel(ax, T, highlight=("test_section",))
    D = station_marks(ax, T, patches=P)
    text(ax, D[1], "station", direction=90.0, dist=10.0, fs=FS_SMALL)
    for a, b in T.flow:
        flow_arrow(ax, a, b, width=6.0, head_width=11.0, head_len=8.0)
    x0, x1, y0, y1 = T.extent
    yb, yt = y0 - 0.45, y1 + 0.45
    sc = T["settling_chamber"].poly
    xsc0, xsc1 = sc[:, 0].min(), sc[:, 0].max()
    ct = T["contraction"].poly
    ts = T["test_section"].poly
    df = T["diffuser"].poly
    fs_ = T["fan_section"].poly
    hc = T["honeycomb"].poly
    s1 = T["screen_1"].lines[0]
    lip = T["bellmouth"].walls[1]                     # the lower lip
    lab = {
        "bellmouth": ("bellmouth", (x0 - 1.5, yb + 0.25), tuple(lip[12] + (0.0, 0.06))),
        "honeycomb": ("honeycomb", (-0.6, 2.95), (hc[:, 0].mean(), 1.5)),
        "screen_1": ("screens", (1.4, 3.85), (s1[0, 0], 0.9)),
        "settling_chamber": ("settling chamber", (xsc1 - 0.3, yb - 0.35), (xsc0 + 0.42 * (xsc1 - xsc0), -0.75 * sc[:, 1].max())),
        "contraction": ("contraction", (ct[:, 0].mean() + 2.6, yb + 0.35), None),
        "test_section": ("test section", (ts[:, 0].mean() + 0.6, yt - 0.35), (ts[:, 0].max() - 0.35, 0.35)),
        "diffuser": ("diffuser", (df[:, 0].mean() + 0.5, yb + 0.6), None),
        "fan": ("fan", (fs_[:, 0].mean() + 1.4, yt - 0.2), None),
    }
    for n, (s, at, tg) in lab.items():
        label_part(ax, P, T, n, s, at=at, ha="center", target=tg)
    assert abs(float(axis_area(T, [T.stations[1][0][0]])[0]) / float(axis_area(T, [T.stations[2][0][0]])[0])
               - EX1["ratio"]) < 1e-9, "the drawn contraction ratio is the example's"
    close_to(H1, 2 * T["settling_chamber"].poly[:, 1].max(), 1e-9, "settling-chamber height")
    assert all(D[n][1] > T.stations[n][1][1] for n in (1, 2, 3)), "every station disc sits outside the upper wall"
    trim_canvas(fig)
    save_figure(fig, "p31-open-circuit")


def closed_circuit():
    """A closed-circuit tunnel in plan view: the parts it adds to the open circuit named."""
    T = closed_circuit_plan()
    x0, x1, y0, y1 = T.extent
    fig, ax = canvas(6.5, xlim=(x0 - 40, x1 + 40), ylim=(y0 - 62, y1 + 34))
    P = draw_tunnel(ax, T, highlight=("test_section",))
    D = station_marks(ax, T, patches=P, side=-1)        # outside the loop, below the test leg
    text(ax, D[1], "station", direction=0.0, dist=10.0, fs=FS_SMALL)
    for a, b in T.flow:
        flow_arrow(ax, a, b, width=6.0, head_width=11.0, head_len=8.0)
    name_part(ax, T, "settling_chamber", "settling chamber", (2.0, -62.0), target=(49.0, -27.0))
    name_part(ax, T, "contraction", "contraction", (126.0, -60.0))
    name_part(ax, T, "test_section", "test section", (196.0, -44.0), target=(152.0, -6.0))
    name_part(ax, T, "diffuser", "diffuser", (270.0, -60.0))
    name_part(ax, T, "corner_1", "corner with\nturning vanes", (345.0, -52.0), target=(310.5, -9.5))   # clear of the vanes
    name_part(ax, T, "fan", "fan", (215.0, 116.0))
    name_part(ax, T, "return_leg", "return leg", (110.0, 116.0))
    xs = [T[n].poly[:, 0].mean() for n in ("corner_1", "corner_2", "corner_3", "corner_4")]
    assert max(xs) - min(xs) > 300.0, "four corners at the two ends of the circuit"
    assert all(D[n][1] < T.stations[n][0][1] for n in (1, 2, 3)), "every station disc sits outside the lower wall"
    hub_tail = T["hub"].poly[:, 0].min()
    assert min(T.flow[2][0][0], T.flow[2][1][0]) < max(T.flow[2][0][0], T.flow[2][1][0]) < hub_tail - 10.0, \
        "the return-leg arrow stands clear of the hub's tail cone"
    trim_canvas(fig)
    save_figure(fig, "p31-closed-circuit")


MANO_SCALE = 5.0          # the U-tube of the manometer figure is drawn this many times the tunnel's scale


def _front_part(T):
    """The parts of the open-circuit tunnel from the bellmouth to the end of the test section; the
    test section is left open at its downstream end (a break line is drawn there, not a wall)."""
    F = tunnel_subset(T, ("bellmouth", "settling_chamber", "honeycomb", "screen_1", "screen_2", "screen_3",
                          "contraction", "test_section", "support"))
    ts = F["test_section"]
    F["test_section"] = TunnelPart("test_section", ts.poly, walls=ts.walls, joints=[], inside=ts.inside,
                                   kind=ts.kind)
    return F


def _break_line(ax, x, y0, y1, amp, zorder=4.2):
    """A break line across a duct at x, from wall y0 to wall y1: straight, with one Z in the middle
    (the duct goes on; it is not closed there)."""
    ym, d = 0.5 * (y0 + y1), 0.12 * (y1 - y0)
    xs = [x, x, x + amp, x - amp, x, x]
    ys = [y0, ym - d, ym - 0.35 * d, ym + 0.35 * d, ym + d, y1]
    return ax.plot(xs, ys, color=INK, lw=LW_THIN, zorder=zorder, solid_joinstyle="miter")[0]


def manometer_tunnel():
    """The manometer of worked example 1: tapped into the settling chamber (station 1) and the test
    section (station 2); the leg under the higher pressure p1 stands lower by dh. The tunnel is to
    scale; the U-tube is drawn MANO_SCALE times larger so that dh can be read."""
    e = ex1()
    T = tunnel_outline()
    F = _front_part(T)
    x0, x1, y0, y1 = T.extent
    x_end = F["test_section"].poly[:, 0].max()
    h1 = F["settling_chamber"].poly[:, 1].max()
    h2 = F["test_section"].poly[:, 1].max()
    xs1, xs2 = T.stations[1][0][0], T.stations[2][0][0]
    fig, ax = canvas(6.5, xlim=(x0 - 1.4, x_end + 3.9), ylim=(-h1 - 3.9, y1 + 1.2))
    P = draw_tunnel(ax, F, highlight=("test_section",))
    on_part(_break_line(ax, x_end, -h2, h2, pt(ax, 3.0)), P["test_section"])
    station_marks(ax, F, which=(1, 2), side=1, patches=P)
    flow_arrow(ax, (x0 - 1.3, 0.0), (x0 - 0.35, 0.0), width=6.0, head_width=11.0, head_len=8.0)
    text(ax, (x_end, h2), f"$V_2$ = {fmt(e['V2'])} m/s", direction=45.0, dist=6.0)
    # the U-tube, enlarged: legs 1.2 m apart in the drawing, liquid levels MANO_SCALE * dh apart
    k = MANO_SCALE
    t = 0.07
    xa, xb = 0.5 * (xs1 + xs2) - 0.6, 0.5 * (xs1 + xs2) + 0.6
    top, bot = -h1 - 0.65, -h1 - 2.75
    mid = -h1 - 1.6
    lev_a, lev_b = mid - 0.5 * k * e["dh"], mid + 0.5 * k * e["dh"]
    yrun = -h1 - 0.35
    tube_kw = dict(color=INK, lw=LW_DETAIL, zorder=4, solid_joinstyle="miter")
    for xt, yt_, xl in ((xs1, -h1, xa), (xs2, -h2, xb)):      # pressure lines: down from the tap, across, down to the leg
        path = np.array([(xt, yt_), (xt, yrun), (xl, yrun), (xl, top)])
        for off in (-t, t):
            q = path.copy()
            if xl > xt:      # tube goes down, right, down: offset toward the outer side
                q[0, 0] += off; q[1] += (off, off); q[2] += (off, off); q[3, 0] += off
            else:
                q[0, 0] -= off; q[1] += (-off, off); q[2] += (-off, off); q[3, 0] -= off
            ax.plot(q[:, 0], q[:, 1], **tube_kw)
    draw_manometer(ax, xa, xb, top, bot, lev_a, lev_b, t)
    close_to(lev_b - lev_a, k * e["dh"], 1e-12, "the liquid columns are drawn MANO_SCALE times the tunnel scale")
    assert lev_a < lev_b, "the leg under the higher pressure p1 stands lower"
    assert (lev_b - lev_a) / pt(ax, 1.0) > 30.0, "the height difference is at least 30 pt in the drawing"
    xd = xb + 0.45
    ax.plot([xa + t, xd + 0.08], [lev_a, lev_a], color=GRAY, lw=0.8, ls=(0, (2, 2)), zorder=2)
    ax.plot([xb + t, xd + 0.08], [lev_b, lev_b], color=GRAY, lw=0.8, ls=(0, (2, 2)), zorder=2)
    dimension(ax, (xd, lev_a), (xd, lev_b), None, extension=False)
    text(ax, (xd, mid), "height difference,\n" + r"$\Delta h$ = " + fmt_dec(e["dh"] * 100, 1) + " cm:\n"
         + r"$p_1 - p_2$ = " + fmt_dec(e["dp"], 1) + " Pa", direction=0, dist=10, ha="left")
    text(ax, (0.5 * (xa + xb), bot - t), r"oil, $\rho_\ell$ = " + fmt(e["rho_l"], 3) + r" kg/m$^3$", direction=-90, dist=4)
    text(ax, (xs1, -h1), r"tap at $p_1$", direction=180, dist=8, offset=(0, -14))
    text(ax, (xs2, -h2), r"tap at $p_2$", direction=0, dist=8, offset=(0, -14))
    callout(ax, (xa - t, lev_a), "higher pressure\npushes this side down", at=(xa - 2.7, lev_a - 0.2), ha="center")
    trim_canvas(fig)
    save_figure(fig, "p31-manometer-tunnel")


def pressure_along_tunnel():
    """Worked example 1 along the tunnel axis: the outline with its stations, the speed, and the
    static and total pressure (relative to the room) with the assumed loss."""
    e = ex1()
    T = tunnel_outline()
    xs = {n: T.stations[n][0][0] for n in (1, 2, 3)}
    x_b1 = T["settling_chamber"].poly[:, 0].min()
    x_c1 = T["test_section"].poly[:, 0].min()
    x_t1 = T["test_section"].poly[:, 0].max()
    x_d1 = T["diffuser"].poly[:, 0].max()
    x = np.union1d(np.linspace(x_b1 + 0.02, x_d1, 900), [xs[1], xs[2], xs[3]])
    A = axis_area(T, x)
    # the assumed loss (model drag and wall friction) builds up from the model to station 3
    V, p, p0 = axis_flow(x, A, e["A2"], e["V2"], e["rho"], e["p1"], (x_t1 - 0.5 * EX1["H2"], xs[3]), e["loss"])
    pg, p0g = p - e["p_room"], p0 - e["p_room"]
    for n, Vn in ((1, e["V1"]), (2, e["V2"]), (3, e["V3"])):
        close_to(float(np.interp(xs[n], x, V)), Vn, 1e-6, f"speed at station {n}", rel=True)
    close_to(float(np.interp(xs[2], x, pg)), e["p2g"], 1e-6, "p2 on the curve", rel=True)
    close_to(float(np.interp(xs[3], x, pg)), e["p3g"], 1e-6, "p3 on the curve", rel=True)
    assert abs(V[np.argmin(p)] - V.max()) < 1e-9 * V.max(), "the static pressure dips where the speed peaks"
    FW, FH = 6.5, 6.4
    fig = plt.figure(figsize=(FW, FH))
    L, R = 0.15, 0.95
    xlo, xhi = x_b1 - 1.0, x_d1 + 1.7
    # outline panel, equal aspect, same x range as the plots below
    wpan = (R - L) * FW
    hpan_in = wpan * (2 * 2.75) / (xhi - xlo)
    ax0 = fig.add_axes([L, 1.0 - 0.03 - hpan_in / FH, R - L, hpan_in / FH])
    ax0.set_xlim(xlo, xhi); ax0.set_ylim(-2.2, 3.3); ax0.set_aspect("equal"); ax0.axis("off")
    F = tunnel_subset(T, ("settling_chamber", "honeycomb", "screen_1", "screen_2", "screen_3", "contraction",
                          "test_section", "support", "diffuser"))
    Pd = draw_tunnel(ax0, F, highlight=("test_section",))
    station_marks(ax0, F, patches=Pd, side=1)
    bot = 0.08
    gap = 0.07
    hp = (1.0 - 0.03 - hpan_in / FH - 0.05 - bot - gap) / 2
    ax1 = fig.add_axes([L, bot + hp + gap, R - L, hp])
    ax2 = fig.add_axes([L, bot, R - L, hp])
    for a in (ax1, ax2):
        for sname in ("top", "right"):
            a.spines[sname].set_visible(False)
        a.grid(True, color=GRID, lw=0.6, zorder=0)
        a.set_axisbelow(True)
        a.set_xlim(xlo, xhi)
        for n in (1, 2, 3):
            a.axvline(xs[n], **line_kw("boundary"), zorder=1)
    ax1.plot(x, V, **line_kw(0), zorder=3)
    ax1.set_ylim(0, 70)
    ax1.set_yticks([0, 20, 40, 60])
    ax1.set_ylabel("Speed, m/s", fontsize=FS_LABEL)
    ax1.tick_params(labelbottom=False, labelsize=FS_SMALL)
    M = "−"
    sp = lambda v: fmt(v, 4, minus=M)
    for n, Vn, at in ((1, e["V1"], (1.9, 30.0)), (2, e["V2"], (8.9, 63.5)), (3, e["V3"], (13.4, 12.0))):
        ax1.plot([xs[n]], [Vn], "o", color=INK, ms=5, zorder=5)
        callout(ax1, (xs[n], Vn), f"$V_{n}$ = {sp(Vn)} m/s" if n == 2 else f"$V_{n}$ =\n{sp(Vn)} m/s", at=at,
                ha="center", fs=FS_SMALL, gap=3.0)
    # pressure panel: static (solid) and total (dashed), relative to the room
    ax2.plot(x, p0g, **line_kw(1), zorder=3)
    ax2.plot(x, pg, **line_kw(0), zorder=4)
    ax2.set_ylim(-2000, 1050)
    ax2.set_yticks([-1500, -1000, -500, 0])
    ax2.set_ylabel(r"$p - p_\mathrm{room}$, Pa", fontsize=FS_LABEL)
    ax2.set_xlabel("Distance along the tunnel axis, m", fontsize=FS_LABEL)
    ax2.tick_params(labelsize=FS_SMALL)
    ax1.tick_params(labelsize=FS_SMALL)
    import matplotlib.ticker as mt
    ax2.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: (M if v < 0 else "") + f"{abs(v):,.0f}"))
    for n, pn, at in ((1, e["p1g"], (1.9, -750.0)), (2, e["p2g"], (8.55, -720.0)), (3, e["p3g"], (15.6, -1080.0))):
        ax2.plot([xs[n]], [pn], "o", color=INK, ms=5, zorder=5)
        callout(ax2, (xs[n], pn), f"$p_{n}$:\n{sp(pn)} Pa", at=at, ha="center", fs=FS_SMALL, gap=3.0)
    label_curve(ax2, x, p0g, xs[2] + 2.9, "total pressure, $p_0$", role=1, offset=(0, 16), fs=FS_SMALL)
    text(ax2, (12.6, -1620.0), "static pressure, $p$", fs=FS_SMALL)
    for a in (ax1, ax2):
        a.set_xticks(range(2, 19, 2))
    xl = xs[3] + 0.35
    ax2.plot([xs[3] - 1.2, xl + 0.1], [0.0, 0.0], color=INK, lw=0.7, zorder=2)
    ax2.plot([xs[3] + 0.08, xl + 0.1], [-e["loss"], -e["loss"]], color=INK, lw=0.7, zorder=2)
    fig.canvas.draw()
    ky = (ax2.get_ylim()[1] - ax2.get_ylim()[0]) / (ax2.get_position().height * fig.get_figheight() * 72.0)
    lead = 9.0 * ky                                 # Pa per 9 pt: the arrows point in from outside the small gap
    for y_from, y_to in ((lead, 0.0), (-e["loss"] - lead, -e["loss"])):
        arrow(ax2, (xl, y_from), (xl, y_to), color=INK, lw=LW_THIN, head="small", zorder=4, gid="grp:loss")
    ax2.plot([xl, xl], [0.0, -e["loss"]], color=INK, lw=LW_THIN, zorder=4, gid="grp:loss")
    text(ax2, (xs[3] - 0.25, 600.0), f"assumed loss,\n{fmt(100 * EX1['loss_frac'], 2)}% of $q_2$:\n{fmt(e['loss'])} Pa",
         ha="right", fs=FS_SMALL)
    save_figure(fig, "p31-pressure-along-tunnel")


def _plot_axes(width=6.5, height=3.6, rect=(0.14, 0.17, 0.82, 0.78)):
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes(list(rect))
    for sname in ("top", "right"):
        ax.spines[sname].set_visible(False)
    ax.grid(True, color=GRID, lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=FS_SMALL)
    return fig, ax


def viscosity():
    """Viscosity of air against temperature: Sutherland's law, with the table values of the
    U.S. Standard Atmosphere, 1976 marked."""
    T = np.linspace(200.0, 400.0, 300)
    mu = mu_sutherland(T)
    for _, Tk, m in USSA_MU:
        close_to(float(mu_sutherland(Tk)), m, 5e-4, f"Sutherland's law against the table at {Tk} K", rel=True)
    assert np.all(np.diff(mu) > 0), "the viscosity of air rises with temperature"
    fig, ax = _plot_axes(6.5, 3.7)
    ax.plot(T, mu * 1e5, **line_kw(0), zorder=3)
    Tt = [t for _, t, _ in USSA_MU]
    mt_ = [m * 1e5 for _, _, m in USSA_MU]
    ax.plot(Tt, mt_, "s", ms=7, mfc="white", mec=INK, mew=1.4, zorder=5, ls="none")
    ax.set_xlim(200, 400)
    ax.set_ylim(1.2, 2.4)
    ax.set_xticks([200, 250, 300, 350, 400])
    ax.set_yticks([1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
    ax.set_xlabel("Temperature, K", fontsize=FS_LABEL)
    ax.set_ylabel(r"Viscosity, $\mu$, $10^{-5}$ kg/(m s)", fontsize=FS_LABEL)
    label_curve(ax, T, mu * 1e5, 360.0, "Sutherland's law", role=0, offset=(-34, 14), fs=FS_SMALL)
    callout(ax, (Tt[0], mt_[0]), "table values,\nU.S. Standard\nAtmosphere 1976", at=(345.0, 1.55), ha="center",
            fs=FS_SMALL, gap=5.0)
    t11 = USSA_MU[-1]
    callout(ax, (t11[1], t11[2] * 1e5), f"{fmt(t11[0] / 1000, 2)} km, {fmt_dec(t11[1], 2)} K", at=(236.0, 1.31),
            ha="left", fs=FS_SMALL, gap=5.0)
    callout(ax, (T_SL, float(mu_sutherland(T_SL)) * 1e5), f"sea level, {fmt_dec(T_SL, 2)} K:\n" + r"$\mu$ = "
            + "$" + fmt_sci(MU_SL) + "$ kg/(m s)", at=(255.0, 2.17), ha="center", fs=FS_SMALL, gap=5.0)
    save_figure(fig, "p31-viscosity")


BL = dict(stations=(1.8, 2.8, 4.1, 5.0), delta_drawn=1.6, n_lam=2, wall_join=0.08,   # the boundary-layer figure
          lam_heights=(1.0 / 3.0, 2.0 / 3.0))


def boundary_layer():
    """Laminar profiles near the leading edge, transition, turbulent profiles downstream; the
    regions named by braces under the plate; the velocity is zero at the wall (no slip)."""
    fig, ax = canvas(6.5, xlim=(-1.9, 6.9), ylim=(-1.05, 2.55))
    g = boundary_layer_plate(ax, **BL)
    p0 = g["profiles"]
    text(ax, p0[0]["free_stream_tail"], r"free stream, $V_\infty$", direction=180, dist=4, color=BLUE)
    ex = g["edge"]
    callout(ax, (2.55, float(np.interp(2.55, ex.get_xdata(), ex.get_ydata()))), "boundary-layer edge",
            at=(2.75, 1.6), ha="center")
    # no slip: the leader ends on the wall dot of the first laminar profile. It enters the boundary
    # layer through its edge, so the edge is marked as the outline of that region (on_part).
    x_ns = BL["stations"][0]
    close_to(float(p0[0]["curve"][0][0]), x_ns, 1e-12, "the no-slip leader ends on a profile's wall dot")
    xe, ye = ex.get_xdata(), ex.get_ydata()
    on_part(ex, _Poly(np.r_[np.c_[xe, ye], [(xe[-1], 0.0), (xe[0], 0.0)]], closed=True, transform=ax.transData))
    callout(ax, (x_ns, pt(ax, 0.5)), "no slip: $u$ = 0\nat the wall", at=(-0.15, 0.42), ha="right")
    boundary_layer.vexag = g["vexag"]
    d = g["deltas"]
    assert d[-1] > d[1] > d[0], "the layer thickens downstream"
    assert g["drawn"][-1] / g["drawn"][1] > 2.0, "the turbulent layer is much thicker than the laminar one"
    trim_canvas(fig)
    save_figure(fig, "p31-boundary-layer")


FS_EXP = 10.0             # pt, exponents of the Reynolds-number ladder: the exponent is the data


def _sci_parts(v, sig=4):
    """A number as pieces for _pow_text: 1.284e8 -> ["1.284 × 10", ("8",)]; 1e4 -> ["10", ("4",)]."""
    e = int(math.floor(math.log10(v) + 1e-12))
    m = v / 10 ** e
    if abs(m - 1.0) < 1e-9:
        return ["10", (str(e).replace("-", "−"),)]
    return [f"{fmt(m, sig)} × 10", (str(e).replace("-", "−"),)]


def _pow_text(ax, xy, pieces, ha="left", fs=FS_SMALL, color=INK):
    """Write a label made of plain pieces and exponents (tuples), each exponent as its own text
    at FS_EXP, raised, so a power of ten reads at 10 pt on the page. Anchored at xy (data) on its
    left, right or center, vertically centered; the exponent's baseline is raised about 0.6 of
    the font size, near the cap height of the plain text. Returns the list of texts."""
    ws = [text_size(ax, p if isinstance(p, str) else p[0], fs if isinstance(p, str) else FS_EXP)[0] for p in pieces]
    gap = 0.0                                            # the exponent set against its "10"
    total = sum(ws) + gap * sum(1 for p in pieces if not isinstance(p, str))
    x = xy[0] - {"left": 0.0, "center": 0.5, "right": 1.0}[ha] * total
    out = []
    for p, w in zip(pieces, ws):
        if isinstance(p, str):
            out.append(ax.text(x, xy[1], p, fontsize=fs, color=color, ha="left", va="center", zorder=10))
            x += w
        else:
            x += gap
            out.append(ax.text(x, xy[1] + pt(ax, 0.57 * fs), p[0], fontsize=FS_EXP, color=color, ha="left",
                               va="center", zorder=10))
            x += w
    return out


def reynolds_ladder():
    """Reynolds numbers on one horizontal log scale: flows in air above the axis (filled circles),
    in water below it (open circles); the flat-plate transition guide; and the gap between the
    airship model in the tunnel and the full-size airship, bracketed."""
    e2 = ex2()
    air = airliner_re()["Re"]
    lo, hi = -6.0, 9.0
    fig, ax = canvas(6.5, xlim=(lo - 1.9, hi + 1.1), ylim=(-2.75, 3.7))
    ax.plot([lo, hi], [0, 0], color=INK, lw=LW_OUTLINE, zorder=4, solid_capstyle="butt")
    for k in range(int(lo), int(hi) + 1):
        ax.plot([k, k], [-0.09, 0.09], color=INK, lw=LW_THIN, zorder=4)
    ticks = []                                          # the texts of each tick label
    for k in range(int(lo), int(hi) + 1, 3):            # tick labels under the axis, every third decade
        if k == 0:
            ticks.append([ax.text(k, -0.6, "1", fontsize=FS_SMALL, ha="center", va="center", zorder=10)])
        else:
            ticks.append(_pow_text(ax, (k, -0.6), ["10", (str(k).replace("-", "−"),)], ha="center"))
    y2 = -1.7 - pt(ax, 8.0)                             # the second row of water labels, and "in water"
    ax.text(1.5, -2.35 - pt(ax, 8.0), "Reynolds number, $\\mathit{Re}$ (log scale)", fontsize=FS_LABEL, ha="center",
            va="center")
    yl = {"air": 0.0, "water": 0.0}

    def mark(v, filled):
        x = math.log10(v)
        ax.plot([x], [0.0], "o", ms=6.5, mfc=INK if filled else "white", mec=INK, mew=1.4, zorder=6)
        return x

    def lead(x, y, up):
        y0 = 0.17 if up else -0.17
        ax.plot([x, x], [y0, y], color=INK, lw=0.7, zorder=3)

    # in air, above the axis: the tunnel model, the airliner wing and the full-size airship
    xm, xa, xs_ = (mark(v, True) for v in (e2["Re_model"], air, e2["Re_full"]))
    for x, y, s, v in ((xm, 1.82, "airship model in the tunnel, ", e2["Re_model"]),
                       (xa, 2.52, "airliner wing in cruise, ", air),
                       (xs_, 3.22, "full-size airship, ", e2["Re_full"])):
        lead(x, y, True)
        _pow_text(ax, (x - 0.1, y), [s + _sci_parts(v)[0], _sci_parts(v)[1]], ha="right")
    # model aircraft and small drones (Leishman): a bracket just above the axis
    r0, r1 = (math.log10(v) for v in LEISHMAN_SMALL_AIRCRAFT_RE)
    yb = 0.38
    ax.plot([r0, r0, r1, r1], [yb - 0.12, yb, yb, yb - 0.12], color=INK, lw=LW_THIN, zorder=3)
    _pow_text(ax, (r0 - 0.15, yb), ["model aircraft and small drones, 10", (str(int(r0)),), "\u00a0to 10",
                                    (str(int(r1)),)], ha="right")
    # the flat-plate transition guide
    xt = math.log10(RE_TR)
    ax.plot([xt, xt], [-0.15, 1.12], color=INK, lw=1.2, ls=(0, (3, 2)), zorder=5)
    _pow_text(ax, (xt - 0.22, 1.12), ["flat-plate transition, $\\mathit{Re}_x$", "\u00a0= 5 × 10", ("5",)], ha="right")
    # in water, below the axis; the first row sits well below the tick labels, so a tick value
    # never reads as part of an example label (asserted below: 4 pt between the text boxes)
    yw = -1.0 - pt(ax, 10.5)
    examples = []
    for v, y, s, ha, dx in ((bacterium_re(), yw, "swimming bacterium, ", "center", 0.0),
                            (PURCELL_GOLDFISH_RE, yw, "goldfish, about ", "center", 0.0),
                            (PURCELL_SWIMMER_RE, y2, "person swimming, about ", "left", 0.1)):
        x = mark(v, False)
        lead(x, y + (0.3 if ha == "center" else 0.0), False)
        parts = _sci_parts(v, 1)
        examples.append(_pow_text(ax, (x + dx, y), [s + parts[0], parts[1]], ha=ha))
    # the gap between the model and the airship: below the axis, under the two marks
    yg = -0.55
    ax.plot([xm, xm, xs_, xs_], [yg + 0.12, yg, yg, yg + 0.12], color=INK, lw=LW_THIN, zorder=3)
    ratio = e2["Re_ratio"]
    text(ax, (0.5 * (xm + xs_), yg), f"{fmt(ratio, 2)} times", direction=-90.0, dist=3.0, fs=FS_SMALL,
         backing=False)
    text(ax, (lo - 0.2, 1.4), "in air", fs=FS_LABEL, ha="left", backing=False)
    text(ax, (lo - 0.2, y2), "in water", fs=FS_LABEL, ha="left", backing=False)
    close_to(10 ** (xs_ - xm), ratio, 1e-9, "the bracket spans the model-to-airship ratio")
    assert xm < xa < xs_ and math.log10(bacterium_re()) < 2.0 < 4.0 < xt < xm, "the ladder is in order"
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    box = lambda texts: Bbox.union([t.get_window_extent(rend) for t in texts])
    px4 = 4.0 * fig.dpi / 72.0
    for e in map(box, examples):                         # every water label clears every tick label
        for t in map(box, ticks):
            gap = max(t.x0 - e.x1, e.x0 - t.x1, t.y0 - e.y1, e.y0 - t.y1)
            assert gap >= px4, f"a water label is {gap * 72.0 / fig.dpi:.1f} pt from a tick label (4 pt needed)"
    trim_canvas(fig)
    save_figure(fig, "p31-reynolds-ladder")


def scale_speed():
    """The speed a model needs for the full-size airship's Reynolds number, against model length,
    with the Mach 0.3 limit of a low-speed tunnel."""
    e2 = ex2()
    e1 = ex1()
    L = np.logspace(np.log10(0.5), np.log10(EX2["L_full"]), 300)     # a model longer than the airship means nothing
    V = speed_for_reynolds(e2["Re_full"], RHO_SL, L, MU_SL)
    fig, ax = _plot_axes(6.5, 3.9)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.plot(L, V, **line_kw(0), zorder=3)
    V03, V1M = e2["V_M03"], e1["a"]
    ax.axhline(V03, **line_kw(1), zorder=2)
    ax.axhline(V1M, **line_kw(2), zorder=2)
    ax.set_xlim(0.5, 100.0); ax.set_ylim(10.0, 5000.0)
    import matplotlib.ticker as mt
    ax.xaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.xaxis.set_minor_formatter(mt.NullFormatter()); ax.yaxis.set_minor_formatter(mt.NullFormatter())
    ax.set_xlabel("Model length, m", fontsize=FS_LABEL)
    ax.set_ylabel("Speed to match the airship's $\\mathit{Re}$, m/s", fontsize=FS_LABEL)
    L03 = e2["Re_full"] * MU_SL / (RHO_SL * V03)
    close_to(float(np.interp(np.log10(L03), np.log10(L), np.log10(V))), np.log10(V03), 1e-4, "crossing on the curve")
    ax.plot([e2["L_model"]], [e2["V_match"]], "o", color=INK, ms=6, zorder=5)
    ax.plot([L03], [V03], "o", ms=6, mfc="white", mec=INK, mew=1.4, zorder=5)
    ax.plot([e2["L_full"]], [e2["V_full"]], "s", ms=6, mfc="white", mec=INK, mew=1.4, zorder=5)
    callout(ax, (e2["L_model"], e2["V_match"]), f"1:{fmt(e2['scale'], 2)} model, {fmt_dec(e2['L_model'], 1)} m:\n" + fmt(e2["V_match"]) + " m/s, Mach "
            + fmt(e2["M_match"], 3), at=(3.2, 2600.0), ha="center", fs=FS_SMALL, gap=5.0)
    callout(ax, (L03, V03), f"model {fmt(L03, 3)} m long\nreaches Mach {fmt(MACH_INCOMPRESSIBLE, 1)}", at=(4.6, 42.0), ha="center",
            fs=FS_SMALL, gap=5.0)
    callout(ax, (e2["L_full"], e2["V_full"]), f"full size: {fmt(e2['L_full'], 2)} m at {fmt(e2['V_full'], 2)} m/s", at=(18.0, 15.0), ha="center", fs=FS_SMALL,
            gap=5.0)
    text(ax, (0.6, V03), f"Mach {fmt(MACH_INCOMPRESSIBLE, 1)}, " + fmt(V03) + " m/s", direction=-90, dist=3, ha="left", fs=FS_SMALL,
         color=text_color(1))
    text(ax, (0.6, V1M), "Mach 1, " + fmt(V1M) + " m/s", direction=90, dist=3, ha="left", fs=FS_SMALL,
         color=text_color(2))
    assert e2["V_match"] > V1M > V03, "the 1:75 model would need a supersonic speed"
    save_figure(fig, "p31-scale-speed")


def make_all():
    open_circuit()
    closed_circuit()
    manometer_tunnel()
    pressure_along_tunnel()
    viscosity()
    boundary_layer()
    reynolds_ladder()
    scale_speed()


# =================================================================== values
def values():
    e = ex1()
    e2 = ex2()
    r = lambda k, t: record(PAGE, k, t)
    # worked example 1
    r("ex1_ratio", fmt_dec(e["ratio"], 1))
    r("ex1_H2", fmt_dec(e["H2"], 1))
    r("ex1_A2", fmt(e["A2"], 3))
    r("ex1_A1", fmt(e["A1"], 3))
    r("ex1_rho_l", fmt(e["rho_l"], 3))
    r("ex1_dh_cm", fmt_dec(e["dh"] * 100, 1))
    r("ex1_dh", fmt_dec(e["dh"], 3))
    r("ex1_dp", fmt_dec(e["dp"], 2))                 # rho_l g dh exactly, so p2 follows from the printed p1
    r("ex1_dp_1dec", fmt_dec(e["dp"], 1))            # as the figure labels it
    r("ex1_inv_ratio_sq", fmt(e["inv_ratio_sq"], 5))
    r("ex1_area_term", fmt(e["area_term"], 5))
    r("ex1_V2", fmt(e["V2"], 5))                     # five figures in the steps, so q2 and x_tr follow from it
    r("ex1_V2_4", fmt(e["V2"]))                      # as the figures and the running text give it
    r("ex1_V1", fmt(e["V1"]))
    r("ex1_a", fmt(e["a"]))
    r("ex1_M2", fmt(e["M2"]))
    r("ex1_q2", fmt_dec(e["q2"], 1))
    r("ex1_q1", fmt(e["q1"]))
    r("ex1_p1", fmt_dec(e["p1"], 2))                 # 101,325 minus the printed q1, exactly
    r("ex1_p2", fmt_dec(e["p2"], 1))
    r("ex1_p_room", fmt(e["p_room"], 6))
    r("ex1_A3_ratio", fmt(e["A3_ratio"]))
    r("ex1_V3", fmt(e["V3"]))
    r("ex1_q3", fmt(e["q3"]))
    r("ex1_loss", fmt(e["loss"]))
    r("ex1_p3g", fmt(-e["p3g"]))
    r("ex1_p3g_noloss", fmt(-e["p3g_noloss"]))
    r("ex1_p1g", fmt(-e["p1g"]))
    r("ex1_V_set", fmt(e["V_set"], 2)); r("ex1_dp_set", fmt_dec(e["dp_set"], 1))
    r("ex1_dh_set", fmt(e["dh_set"])); r("ex1_dh_set_cm", fmt(100 * e["dh_set"]))
    r("ex1_dh_set_check", fmt(100 * e["dh_set_check"]))
    r("ex1_loss_pct", fmt(100 * e["loss_frac"], 2))
    r("mach03_speed", fmt(e2["V_M03"]))
    # worked example 2
    r("ex2_L_model", fmt_dec(e2["L_model"], 1))
    r("ex2_D_model", fmt_dec(e2["D_model"], 2))
    r("ex2_Re_full", fmt_sci(e2["Re_full"]))
    r("ex2_Re_model", fmt_sci(e2["Re_model"]))
    r("ex2_Re_ratio", fmt(e2["Re_ratio"]))
    r("ex2_V_match", fmt(e2["V_match"]))
    r("ex2_M_match", fmt(e2["M_match"]))
    r("ex2_x_tr_model", fmt(e2["x_tr_model"]))
    r("ex2_tr_pct_model", fmt(100 * e2["tr_frac_model"]))
    r("ex2_x_tr_full", fmt(e2["x_tr_full"], 5))
    r("ex2_x_tr_model5", fmt(e2["x_tr_model"], 5))
    r("ex2_re_mu", fmt(RE_TR * MU_SL))
    r("ex2_tr_pct_full", fmt(100 * e2["tr_frac_full"]))
    r("ex2_tr_frac_full", fmt(e2["tr_frac_full"], 5))
    r("ex2_A_front", fmt(e2["A_front"]))
    r("ex2_blockage_pct", fmt(100 * e2["blockage"]))
    L03 = e2["Re_full"] * MU_SL / (RHO_SL * e2["V_M03"])
    r("ex2_L03", fmt(L03, 3))
    # boundary-layer thickness on the model (example 2)
    d_lam = float(delta_laminar(e2["x_tr_model"], RE_TR))
    d_tur = float(delta_turbulent(e2["L_model"], e2["Re_model"]))
    r("ex2_sqrt_Re_tr", fmt(math.sqrt(RE_TR), 4))
    r("ex2_d_lam_mm", fmt(1000 * d_lam))
    r("ex2_d_lam", fmt(d_lam))
    r("ex2_speed_ratio", fmt(e2["V_model"] / e2["V_full"], 3))

    # viscosity, Reynolds numbers of the ladder
    r("nu_sl", fmt_sci(kinematic_viscosity(MU_SL, RHO_SL)))
    for h, Tk, m in USSA_MU:
        r(f"ussa_T_{int(h)}", fmt_dec(Tk, 2))
        if h in (-5000.0, 11000.0):
            r(f"ussa_mu_{int(h)}", fmt(m * 1e5, 5))
    a = airliner_re()
    r("airliner_Re", fmt_sci(a["Re"]))
    r("bacterium_Re", fmt_sci(bacterium_re(), 1))
    r("bl_vexag", fmt(boundary_layer_vexag(), 2))
    print(f"   ex1: {e}")
    print(f"   ex2: {e2}")
    print(f"   airliner {a}  bacterium {bacterium_re():.3g}  L03 {L03}  d_lam {d_lam} d_tur {d_tur}")


def boundary_layer_vexag():
    """The vertical exaggeration of the boundary-layer figure (drawn on a scratch canvas)."""
    fig, ax = canvas(6.5, xlim=(-1.9, 6.9), ylim=(-1.05, 2.55))
    g = boundary_layer_plate(ax, labels=False, **BL)
    plt.close(fig)
    return g["vexag"]
