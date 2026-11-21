"""Figures and values of 1.6 Aircraft Sizing (notes/chapter-1/aircraft-sizing.md).

The worked example sizes a long-range twin-jet airliner (an invented mission). Its numbers are computed the way a student
computes them by hand: every intermediate value is rounded to the digits the page prints, and the
next step uses the rounded value, so each printed step reproduces from the digits before it
(scripts/check_chains.py). The shared helpers of sizing.py (full precision) check the hand chain.

Published data (each with its source in the shared module that holds it): Raymer Table 3.1
fits, the historical segment fractions, the class ranges of Raymer Figure 3.1
(EMPTY_WEIGHT_RANGE), three Boeing jets at maximum takeoff weight (JET_WEIGHTS), typical
specific fuel consumption (SFC_TYPICAL) and lift-to-drag ratios (LD_TYPICAL): chapter_1/sizing.py.
"""
import math

from chapter_1.common import *

TAG = "p16"
BOEING = JET_WEIGHTS
# The classes drawn on the empty-weight figure, with the name each line carries
TREND_CLASSES = [(cls, *EMPTY_WEIGHT_RANGE[cls], name) for cls, name in
                 (("Sailplane, unpowered", "sailplane"), ("Twin turboprop", "twin turboprop"),
                  ("Jet fighter", "jet fighter"), ("Jet transport", "jet transport"),
                  ("Military cargo or bomber", "military cargo or bomber"))]

# ===================================================================== the worked example
N_PAX, W_PAX = 250, 210.0          # passengers, lb each with bags
N_CREW, W_PERSON = 10, 200.0       # 2 pilots and 8 flight attendants, lb each
R_NMI, V_KT, C_CR, LD_CR = 5000.0, 480.0, 0.5, 17.0       # cruise: nmi, kt, 1/h, -
E_H, C_LT, LD_LT = 0.5, 0.4, 19.0                          # loiter: h, 1/h, -
CLASS = "Jet transport"
GUESS_FRAC = 0.5                   # first guess: We/W0 = 0.5 (about half, Figure 1)
TOL = 0.001                        # stop when the change is below 0.1%


def r5(x):
    """Round to 5 decimal places, as the page prints a fraction."""
    return round(x, 5)


def r5s(x):
    """Round to 5 significant figures (an exponent like 0.010526)."""
    return float(f"{x:.5g}")


def hand_example():
    """The worked example as a student does it, each step from the rounded values printed
    before it. Returns a dict of every number the page prints."""
    A, _, Cexp = EMPTY_WEIGHT_FIT[CLASS]
    d = dict(A=A, Cexp=Cexp)
    d["W_pay"] = N_PAX * W_PAX
    d["W_crew"] = N_CREW * W_PERSON
    d["W_fixed"] = d["W_pay"] + d["W_crew"]
    d["x_cr"] = r5(R_NMI * C_CR / (V_KT * LD_CR))
    d["f_cr"] = r5(math.exp(-d["x_cr"]))
    d["x_lt"] = r5s(E_H * C_LT / LD_LT)
    d["f_lt"] = r5(math.exp(-d["x_lt"]))
    f = [SEGMENT_FRACTION["warm-up and takeoff"], SEGMENT_FRACTION["climb"], d["f_cr"], d["f_lt"],
         SEGMENT_FRACTION["landing"]]
    d["seg"] = f
    w, prod = [1.0], 1.0
    for fi in f:                                   # the weight at each segment end, W_i/W0:
        prod *= fi                                 # the product of the printed fractions, rounded
        w.append(r5(prod))
    d["Wi"] = w
    d["Wx"] = r5(f[0] * f[1] * f[2] * f[3] * f[4])
    d["burn"] = r5(1.0 - d["Wx"])
    d["Wf"] = r5(RESERVE_FACTOR * d["burn"])
    d["den0"] = r5(1.0 - d["Wf"] - GUESS_FRAC)
    d["guess_exact"] = d["W_fixed"] / d["den0"]
    d["guess"] = round(d["guess_exact"], -3)       # a round first guess
    rows = []
    W = d["guess"]
    for _ in range(30):
        we = r5(A * W ** Cexp)
        den = r5(1.0 - d["Wf"] - we)
        new = round(d["W_fixed"] / den)
        ch = (new - W) / W
        rows.append(dict(guess=W, We=we, den=den, new=new, change=new - W, pct=100.0 * ch))
        W = new
        if abs(ch) < TOL:
            break
    d["rows"] = rows
    d["W0"] = rows[-1]["new"]
    d["We_W0"] = r5(A * d["W0"] ** Cexp)
    d["We"] = round(d["We_W0"] * d["W0"])
    d["Wf_lb"] = round(d["Wf"] * d["W0"])
    d["sum"] = d["W_fixed"] + d["Wf_lb"] + d["We"]
    d["den"] = r5(1.0 - d["Wf"] - d["We_W0"])
    d["k"] = r5s(Cexp * d["We_W0"] / d["den"])
    return d


def full_example(R=R_NMI, LD=LD_CR, C=C_CR, V=V_KT, pay=None, A_scale=1.0, E=E_H):
    """The same mission at full precision with the shared helpers (sizing.py). Returns W0 (lb),
    or None when the mission does not close."""
    pay = N_PAX * W_PAX if pay is None else pay
    f = [SEGMENT_FRACTION["warm-up and takeoff"], SEGMENT_FRACTION["climb"], cruise_fraction(R, C, V, LD),
         loiter_fraction(E, C_LT, LD_LT), SEGMENT_FRACTION["landing"]]
    wf = fuel_fraction(mission_fraction(f))
    A, _, Cexp = EMPTY_WEIGHT_FIT[CLASS]
    # solve W = K / (1 - wf - s A W^C) by bisection on the fixed point (robust near the wall)
    K = N_CREW * W_PERSON + pay

    def gap(W):
        den = 1.0 - wf - A_scale * A * W ** Cexp
        return W * den - K if den > 0 else -1.0
    lo, hi = K, 5.0e7
    if gap(hi) <= 0:
        return None
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if gap(mid) > 0:
            hi = mid
        else:
            lo = mid
    return hi


def sensitivities():
    """Percent change of W0 when one input is made 10% worse, the others as in the example."""
    base = full_example()
    cases = [("Empty-weight fraction 10% higher", dict(A_scale=1.1)),
             ("Cruise lift-to-drag ratio 10% lower", dict(LD=LD_CR * 0.9)),
             ("Cruise range 10% longer", dict(R=R_NMI * 1.1)),
             ("Cruise fuel consumption $C$ 10% higher", dict(C=C_CR * 1.1)),
             ("Payload 10% heavier", dict(pay=N_PAX * W_PAX * 1.1))]
    return base, [(name, 100.0 * (full_example(**kw) / base - 1.0)) for name, kw in cases]


# ===================================================================== figures
FILL_EMPTY, FILL_PAY, FILL_FUEL = "#8F8F8F", GOLD, "#FFFFFF"


def weight_buildup():
    """Three real jets: each takeoff weight split into operating empty weight, payload and fuel."""
    names = list(BOEING)
    fig, ax = data_axes(6.5, 3.9, grid=False)
    xs = np.arange(3) * 1.55
    wbar = 0.78
    ax.set_xlim(-0.6, xs[-1] + 2.35)
    ax.set_ylim(0.0, 1.19)
    tops = []
    for x, n in zip(xs, names):
        b = BOEING[n]
        parts = [b["oe"] / b["mto"], b["payload"] / b["mto"], b["fuel"] / b["mto"]]
        close_to(sum(parts), 1.0, 1e-9, f"{n}: the parts add up to the takeoff mass")
        y0 = 0.0
        for frac, fill in zip(parts, (FILL_EMPTY, FILL_PAY, FILL_FUEL)):
            ax.add_patch(opaque(plt.Rectangle((x - wbar / 2, y0), wbar, frac, fc=fill, ec=INK, lw=LW_BOX, zorder=3)))
            text(ax, (x, y0 + frac / 2), fmt(frac, 3), fs=FS_SMALL, backing=False, zorder=6)
            y0 += frac
        tops.append(parts)
        lab = f"{fmt(round(b['mto'] * KG_LB, -2))} lb"
        text(ax, (x, 1.0), ("takeoff weight\n" if x == xs[0] else "") + lab, direction=90, dist=4, fs=FS_SMALL,
             backing=False)
    xl = xs[-1] + wbar / 2
    last = tops[-1]
    mids = [last[0] / 2, last[0] + last[1] / 2, last[0] + last[1] + last[2] / 2]
    labels = ["operating empty weight\n(structure, engines,\nsystems, crew)", "payload", "fuel"]
    for m, s in zip(mids, labels):
        text(ax, (xl, m), s, direction=0, dist=8, fs=FS_SMALL, backing=False)
    ax.set_xticks(xs, list(names))
    ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0], ["0", "0.25", "0.50", "0.75", "1.00"])
    ax.set_ylabel("Fraction of the takeoff weight")
    ax.tick_params(axis="x", length=0)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_bounds(0.0, 1.0)
    oe = [BOEING[n]["oe"] / BOEING[n]["mto"] for n in names]
    pay = [BOEING[n]["payload"] / BOEING[n]["mto"] for n in names]
    assert all(0.45 < v < 0.51 for v in oe) and oe[2] < oe[0], oe              # about half, less when larger
    assert all(p < min(o, 1.0 - o - p) for p, o in zip(pay, oe)), pay           # payload is the smallest part
    save_figure(fig, "p16-weight-buildup")


def sizing_loop():
    """The sizing method as a flow chart, steps numbered as in the text: step 6 is the test."""
    x0, x1, y0, y1 = -1.0, 11.2, -0.08, 12.04
    unit = 6.3 * 0.98 / (x1 - x0)                         # in per data unit (axes fill the figure)
    fig, ax = new_axes(6.3, (y1 - y0) * unit / 0.98)
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    set_frame(ax, x0, x1, y0, y1)
    steps = [["Set the mission:", "crew, payload, and the segments"],
             ["Find the fuel fraction $W_f\\,/\\,W_0$", "from the segments (once)"],
             ["Guess the takeoff weight $W_0$", "(after the first pass: the new $W_0$)"],
             ["Find $W_e\\,/\\,W_0$ from the historical fit", "at that $W_0$"],
             ["Compute a new $W_0$", "from the build-up equation"]]
    W, cx = 6.8, 4.1
    h2 = lines_box_height(2, ax=ax)
    bx, y = [], y1 - 0.1
    for i, L in enumerate(steps):
        bx.append(lines_box(ax, (cx, y - h2 / 2), L, w=W, fill=BOX_FILL_START if i == 0 else BOX_FILL))
        y -= h2 + pt(ax, 16.0)
    y_last = bx[-1].cy - bx[-1].h / 2
    q = "Did $W_0$\nchange by less\nthan 0.1%?"                       # broken by hand: balanced lines
    dh = decision_size(ax, q, w=6.4, keep_breaks=True)[1]
    d = decision(ax, (cx, y_last - pt(ax, 16.0) - dh / 2), q, w=6.4, keep_breaks=True)
    h1 = lines_box_height(1, ax=ax)
    done = lines_box(ax, (cx, d.cy - dh / 2 - pt(ax, 36.0) - h1 / 2), ["Stop: $W_0$ is the takeoff weight"], w=W,
                     fill=BOX_FILL_START)
    xd = cx - W / 2 - pt(ax, 9.0) - pt(ax, 4.0)
    for i, b in enumerate(bx):
        step_marker(ax, (xd, b.cy), i + 1)
    step_marker(ax, (xd, d.cy), 6)
    for a, b in zip(bx[:-1], bx[1:]):
        route(ax, a, "bottom", b, "top")
    route(ax, bx[-1], "bottom", d, "top")
    route(ax, d, "bottom", done, "top", label="yes", label_at=0.33, label_side=1)
    route(ax, d, "right", bx[2], "right", via=[("x", 10.5)], label="no", label_at=0.08, label_side=1)
    assert done.cy - done.h / 2 > y0, f"the chart fits its frame ({done.cy - done.h / 2:.2f})"
    assert bx[1].cy > bx[2].cy, "the fuel fraction is found before the loop starts"
    save_figure(fig, "p16-sizing-loop")


def _end_on_dash(ax, ln):
    """Shift the dash pattern of a dashed line so that it ends on the end of a full dash (no
    stray short stroke at the end)."""
    fig = ax.figure
    fig.canvas.draw()
    xy = ax.transData.transform(np.c_[ln.get_xdata(), ln.get_ydata()])
    L = float(np.sum(np.hypot(*np.diff(xy, axis=0).T))) * 72.0 / fig.dpi       # points
    off, seq = ln._dash_pattern
    if not seq:
        return
    P = float(sum(seq))
    n = max(1, round((L - seq[0]) / P))             # whole periods, then one last dash
    k = L / (n * P + seq[0])                         # stretch the pattern a little so both ends are dashes
    lw = ln.get_linewidth()
    ln.set_linestyle((0.0, [k * v / lw for v in seq]))


def empty_weight_trends(ex):
    """Raymer's fits for five classes, three real jets, and the worked example. Each name sits
    against its own line, clear of the others, so the figure reads in grayscale."""
    fig, ax = data_axes(6.5, 5.0)
    ax.set_xscale("log")
    ax.set_xlim(100.0, 2.6e6)
    ax.set_ylim(0.30, 0.75)
    ax.set_xticks([100, 1000, 10000, 100000, 1000000], ["100", "1,000", "10,000", "100,000", "1,000,000"])
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.set_yticks([0.3, 0.4, 0.5, 0.6, 0.7], ["0.30", "0.40", "0.50", "0.60", "0.70"])
    ax.set_xlabel("Takeoff weight $W_0$, lb (log scale)")
    ax.set_ylabel("Empty-weight fraction $W_e/W_0$")
    style = {"Jet transport": 0, "Twin turboprop": 1, "Jet fighter": 2, "Sailplane, unpowered": 3,
             "Military cargo or bomber": 4}
    place = {  # where each direct label sits: (W0 on the line, direction, distance in points, ha)
        "Sailplane, unpowered": (1150.0, -70, 11, "left"),
        "Twin turboprop": (4500.0, 90, 6, None),
        "Jet fighter": (22000.0, 35, 6, "left"),
        "Jet transport": (1.0e6, 35, 6, "left"),
        "Military cargo or bomber": (150000.0, -135, 6, None),
    }
    names = {"Sailplane, unpowered": "sailplane,\nunpowered", "Jet transport": "jet\ntransport"}
    for cls, lo, hi, name in TREND_CLASSES:
        if cls == "Jet fighter":                       # stop short of the jet-transport line it runs into
            Wt = np.geomspace(lo, hi, 400)
            gap = empty_weight_fraction(Wt, cls) - empty_weight_fraction(Wt, CLASS)
            hi = float(Wt[np.nonzero(gap >= 0.0065)[0][-1]])
        W = np.geomspace(lo, hi, 80)
        y = empty_weight_fraction(W, cls)
        ln = ax.plot(W, y, **line_kw(style[cls]))[0]
        if style[cls] == 1:
            _end_on_dash(ax, ln)
        at, dirn, dist, ha = place[cls]
        text(ax, (at, float(empty_weight_fraction(at, cls))), names.get(cls, name), direction=dirn, dist=dist,
             fs=FS_SMALL, color=text_color(style[cls]), **({"ha": ha} if ha else {}))
    for n, b in BOEING.items():
        ax.plot(b["mto"] * KG_LB, b["oe"] / b["mto"], "s", ms=6.5, mfc="white", mec=INK, mew=1.3, zorder=8)
    text(ax, (5.5e5, 0.53), "Boeing 757, 767, 747\n(published)", fs=FS_SMALL, va="bottom")
    ax.plot(ex["W0"], ex["We_W0"], "o", ms=7, color=INK, zorder=9)
    text(ax, (6.6e5, 0.423), f"worked example\n{fmt(ex['W0'])} lb, {fmt_dec(ex['We_W0'], 3)}", fs=FS_SMALL)
    for cls, lo, hi, _ in TREND_CLASSES:
        assert float(empty_weight_fraction(hi, cls)) < float(empty_weight_fraction(lo, cls)), cls
    close_to(float(empty_weight_fraction(ex["W0"], CLASS)), ex["We_W0"], 1e-5, "example on the jet-transport fit")
    save_figure(fig, "p16-empty-weight-trends")


def mission_profile():
    """The mission cut into five segments, each labeled with its weight fraction (symbol and value,
    or the equation that gives it), drawn by the chapter's mission-profile rule (drawing.py): the
    takeoff and the landing on the ground line, the descents that carry no fraction of their own
    drawn thin, with no number at their top."""
    fig, ax = new_axes(6.5, 2.85, equal=False)
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    f = lambda k: fmt_dec(SEGMENT_FRACTION[k], 3)          # noqa: E731
    segs = [(f"warm-up\nand takeoff,\n$W_1/W_0$ = {f('warm-up and takeoff')}", 1.6, 0.0, 0.5),
            (f"climb,\n$W_2/W_1$ = {f('climb')}", 1.3, 1.0, 0.45, -40.0),
            ("cruise, $W_3/W_2$ from the range equation", 4.6, 1.0, 0.5),
            ("descent (counted\nin the cruise)", 1.0, 0.6, 0.75, 225.0),
            ("loiter, $W_4/W_3$ from\nthe endurance equation", 4.3, 0.6, 0.58, 90.0),
            ("descent (counted\nin the landing)", 1.1, 0.0, 0.5, 20.0),
            (f"landing,\n$W_5/W_4$ = {f('landing')}", 1.6, 0.0, 0.5)]
    numbers = ["0", "1", "2", None, "3", "4", None, "5"]
    L = sum(sg[1] for sg in segs)
    ax.set_xlim(-1.0, L + 1.9)
    ax.set_ylim(-0.70, 1.42)
    fig.canvas.draw()
    xs, ys, ln = draw_mission_profile(ax, segs, [90, 120, -45, None, -90, -135, None, 90], numbers=numbers,
                                      thin=(3, 5), ground=(-0.6, 1.8), axes_names=True, distance_below=52.0)
    nseg = sum(1 for n in numbers if n is not None) - 1
    cruise = xs[3] - xs[2]
    assert nseg == 5 and ys[0] == ys[-1] == 0.0, "five segments, from the ground to the ground"
    assert cruise == max(np.diff(xs)), "the cruise is the longest segment"
    assert ys[4] == ys[5] > 0.0, "the loiter is flown level, at its own altitude"
    assert ys[1] == ys[0] == 0.0 and ys[-1] == ys[-2] == 0.0, "takeoff and landing on the ground line"
    save_figure(fig, "p16-mission-profile")


def cruise_forces():
    """The four forces on an airliner in steady level cruise (schematic): lift balances weight and
    thrust balances drag. Drawn on the Boeing 737-800 side view of the vehicle anatomy page (gear up),
    with each force on a line through the center of gravity; lengths not to scale."""
    parts = aircraft_side(detail=False)
    keep = {k: v for k, v in parts.items() if "gear" not in k and "wheel" not in k}
    xg, _, zg = cg_point()
    x0f, x1f, z0f, z1f = -15.6, 55.0, -8.6, 15.4
    fig, ax = canvas(6.5, xlim=(x0f, x1f), ylim=(z0f, z1f))
    draw_parts(ax, keep, details=False)
    cg_symbol(ax, (xg, zg))
    top = max(float(np.max(v.xy[:, 1])) for k, v in keep.items() if k in ("fuselage",))
    bot = min(float(np.min(v.xy[:, 1])) for v in keep.values())
    nose = min(float(np.min(v.xy[:, 0])) for v in keep.values())
    tail = max(float(np.max(v.xy[:, 0])) for v in keep.values())
    LW_len, TD_len = 8.5, 11.0                         # drawn lengths: L = W, T = D (not to scale)
    l0, w0 = (xg, top + 0.5), (xg, bot - 0.5)
    kind_arrow(ax, l0, (xg, l0[1] + LW_len), "force")
    kind_arrow(ax, w0, (xg, w0[1] - LW_len), "force")
    t0, d0 = (nose - 0.6, zg), (tail + 0.6, zg)
    kind_arrow(ax, t0, (t0[0] - TD_len, zg), "force")
    kind_arrow(ax, d0, (d0[0] + TD_len, zg), "force")
    text(ax, (xg, l0[1] + LW_len), "lift, $L$", direction=0, dist=8, ha="left", va="top")
    text(ax, (xg, w0[1] - LW_len), "weight, $W$", direction=0, dist=8, ha="left", va="bottom")
    text(ax, t0, "thrust, $T$", direction=90, dist=7, ha="right")
    text(ax, d0, "drag, $D$", direction=90, dist=7, ha="left")
    callout(ax, (xg - 0.15, zg + 0.15), "center of gravity", at=(9.0, 8.4), ha="right", fs=FS_SMALL)
    text(ax, (x1f - 0.6, z0f + 0.6), "steady level flight:\n$L = W$\n$T = D = W/(L/D)$", ha="right", va="bottom")
    v0, v1 = (x0f + 13.5, z1f - 2.6), (x0f + 1.0, z1f - 2.6)
    kind_arrow(ax, v0, v1, "velocity")
    text(ax, v0, "velocity, $V$", direction=-90, dist=6, ha="right", color=TEXT_KIND["velocity"])
    close_to(abs(l0[1] + LW_len - l0[1]), abs(w0[1] - LW_len - w0[1]), 1e-12, "lift and weight drawn equal")
    assert t0[1] == d0[1] == zg, "thrust and drag act along one line through the center of gravity"
    save_figure(fig, "p16-cruise-forces")


def weight_staircase(ex):
    """The worked example: the weight at each segment end, W_i/W0, and the fuel it gives."""
    fig, ax = data_axes(7.2, 4.1)
    x = np.arange(6)
    w = np.array(ex["Wi"])
    ax.set_xlim(-0.4, 7.45)
    ax.set_ylim(0.555, 1.05)
    ax.plot(x, w, **line_kw(0))
    ax.plot(x, w, "o", ms=6, color=INK, zorder=6)
    for i, (xi, wi) in enumerate(zip(x, w)):
        s = "1" if i == 0 else fmt_dec(wi, 5)
        text(ax, (xi, wi), s, direction=(90, -90, 45, -90, -90, -90)[i], dist=7, fs=FS_SMALL)
    names = ["takeoff", "climb", "cruise", "loiter", "landing"]
    for i in range(5):
        f = ex["seg"][i]
        s = fmt_dec(f, 3) if i in (0, 1, 4) else fmt_dec(f, 5)
        text(ax, (i + 0.5, 0.60), f"{names[i]}\n× {s}", fs=FS_SMALL, backing=False)
    xd, xe = 5.55, 6.15                         # the two double arrows: fuel burned, fuel loaded
    wf_low = 1.0 - ex["Wf"]                     # 1 - Wf/W0: where the fuel loaded reaches
    line(ax, (5.15, w[-1]), (xd + 0.2, w[-1]), "boundary")
    line(ax, (0.2, 1.0), (xe + 0.2, 1.0), "boundary")
    line(ax, (xd - 0.08, wf_low), (xe + 0.2, wf_low), "boundary")
    dimension(ax, (xd, w[-1]), (xd, 1.0), None, extension=False, ticks=False)
    dimension(ax, (xe, wf_low), (xe, 1.0), None, extension=False, ticks=False)
    text(ax, (xd, 0.915), f"fuel burned\n1 − $W_5/W_0$ = {fmt_dec(ex['burn'], 5)}", direction=180, dist=6,
         fs=FS_SMALL)
    text(ax, (xe, 0.85), "fuel loaded,\n6% added:\n" + r"$W_f\,/\,W_0$" + f" =\n{fmt_dec(ex['Wf'], 5)}",
         direction=0, dist=6, fs=FS_SMALL, ha="left")
    text(ax, (xe + 0.2, wf_low), "reserve and\ntrapped fuel", direction=0, dist=5, fs=FS_SMALL, ha="left")
    ax.set_xticks(x, [str(i) for i in x])
    ax.set_xlabel("End of segment $i$ (numbered as on the mission profile)")
    ax.set_ylabel("Weight fraction $W_i/W_0$")
    ax.set_yticks([0.6, 0.7, 0.8, 0.9, 1.0], ["0.60", "0.70", "0.80", "0.90", "1.00"])
    drops = -np.diff(w)
    assert np.all(drops > 0) and int(np.argmax(drops)) == 2, drops                # every segment burns; cruise most
    close_to(w[-1], ex["Wx"], 1e-12, "the staircase ends at W5/W0")
    close_to(1.0 - wf_low, RESERVE_FACTOR * (1.0 - w[-1]), 1e-4, "the fuel loaded is the fuel burned plus 6%")
    save_figure(fig, "p16-weight-staircase")


def iteration(ex):
    """The worked example's iteration: W0 after each pass, closing in on the answer from both sides."""
    rows = ex["rows"]
    n = np.arange(len(rows) + 1)
    W = np.array([rows[0]["guess"]] + [r["new"] for r in rows]) / 1000.0
    fig, ax = data_axes(6.5, 3.8)
    ax.set_xlim(-0.4, len(rows) + 1.6)
    ax.set_ylim(268.0, 320.0)
    line(ax, (-0.4, ex["W0"] / 1000.0), (len(rows) + 0.55, ex["W0"] / 1000.0), "boundary")
    text(ax, (len(rows) + 0.55, ex["W0"] / 1000.0), f"accepted value,\n{fmt(ex['W0'])} lb", direction=0, dist=5,
         fs=FS_SMALL, color=STEEL)
    ax.plot(n, W, **line_kw(0, zorder=4))
    ax.plot(n[:1], W[:1], "o", ms=7, mfc="white", mec=INK, mew=1.4, zorder=6)
    ax.plot(n[1:], W[1:], "o", ms=6, color=INK, zorder=6)
    text(ax, (0, W[0]), f"first guess {fmt(rows[0]['guess'])} lb", direction=0, dist=8, fs=FS_SMALL)
    dirs = [-90, 90, -90, 90]
    for i, r in enumerate(rows):
        s = f"{fmt(r['new'])} lb\n({'+' if r['pct'] > 0 else '−'}{fmt(abs(r['pct']), 3)}%)"
        text(ax, (i + 1, r["new"] / 1000.0), s, direction=dirs[i], dist=7, fs=FS_SMALL)
    ax.set_xticks(n, ["guess"] + [str(i) for i in n[1:]])
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Takeoff weight $W_0$, 1,000 lb")
    ax.set_yticks([270, 280, 290, 300, 310, 320])
    ch = [r["change"] for r in rows]
    assert all(a * b < 0 and abs(b) < abs(a) for a, b in zip(ch[:-1], ch[1:])), ch   # alternates and shrinks
    assert abs(rows[-1]["pct"]) < 100 * TOL
    save_figure(fig, "p16-iteration")


def range_sensitivity(ex):
    """W0 against the design range for three cruise lift-to-drag ratios."""
    fig, ax = data_axes(6.5, 4.2)
    ax.set_xlim(0.0, 10500.0)
    ax.set_ylim(0.0, 1000.0)
    curves = {}
    for i, LD in enumerate((15.0, 17.0, 19.0)):
        Rs = np.linspace(500.0, 9000.0, 341)
        W = np.array([full_example(R=R, LD=LD) / 1000.0 for R in Rs])
        ok = W < 890.0
        ax.plot(Rs[ok], W[ok], **line_kw(i))
        curves[LD] = (Rs[ok], W[ok])
    for i, LD in enumerate((15.0, 17.0, 19.0)):
        Rs, W = curves[LD]
        text(ax, (Rs[-1], W[-1]), f"$L/D$ = {LD:.0f}", direction=90 if LD == 15.0 else 0, dist=6, fs=FS_SMALL,
             color=text_color(i))
    W_full = full_example()                       # the curve is iterated until it stops changing
    ax.plot(R_NMI, W_full / 1000.0, "o", ms=7, color=INK, zorder=9)
    ax.plot(700.0, 830.0, "o", ms=7, color=INK, zorder=9)                     # a key for the marker
    text(ax, (700.0, 830.0), f"worked example: {fmt(R_NMI)} nmi, {fmt(round(W_full))} lb", direction=0, dist=8,
         fs=FS_SMALL)
    ax.set_xlabel("Design range $R$, nmi")
    ax.set_ylabel("Takeoff weight $W_0$, 1,000 lb")
    ax.set_xticks([0, 2000, 4000, 6000, 8000, 10000])
    w2, w4, w6 = (full_example(R=r) for r in (2000.0, 4000.0, 6000.0))
    assert (w6 - w4) > (w4 - w2) > 0, (w2, w4, w6)                                # grows faster than the range
    assert full_example(LD=19.0) < full_example() < full_example(LD=15.0)        # better L/D, lighter aircraft
    save_figure(fig, "p16-range-sensitivity")


def sensitivity_bars(sens):
    """How much W0 grows when each input is made 10% worse."""
    base, cases = sens
    cases = sorted(cases, key=lambda c: c[1])
    fig, ax = data_axes(5.0, 3.0, grid=False)
    y = np.arange(len(cases))
    vals = [c[1] for c in cases]
    for yi, v in zip(y, vals):
        ax.add_patch(opaque(plt.Rectangle((0.0, yi - 0.3), v, 0.6, fc=GOLD, ec=INK, lw=LW_BOX, zorder=3)))
        text(ax, (v, yi), f"+{fmt(v, 3)}%", direction=0, dist=4, fs=FS_SMALL, backing=False)
    ax.set_xlim(0.0, 32.0)
    ax.set_ylim(-0.6, len(cases) - 0.4)
    ax.set_yticks(y, [c[0] for c in cases])
    ax.set_xticks([0, 10, 20, 30])
    ax.set_xlabel("Increase of $W_0$, %")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.grid(True, axis="x", color=GRID, lw=0.6)
    d = dict(cases)
    close_to(d["Cruise range 10% longer"], d["Cruise fuel consumption $C$ 10% higher"], 1e-9,
             "cruise range and cruise C act alike")
    assert max(vals) == d["Empty-weight fraction 10% higher"]
    save_figure(fig, "p16-sensitivity-bars")


# ===================================================================== runner hooks
def make_all():
    ex = hand_example()
    weight_buildup()
    sizing_loop()
    empty_weight_trends(ex)
    mission_profile()
    cruise_forces()
    weight_staircase(ex)
    iteration(ex)
    range_sensitivity(ex)
    sensitivity_bars(sensitivities())


def values():
    """Record every number the page prints (check_values.py finds each one on the page)."""
    ex = hand_example()
    full = full_example()
    assert abs(full - ex["W0"]) < 0.002 * full, (full, ex["W0"])     # the hand chain agrees with sizing.py
    rec = lambda k, v: record(TAG, k, v)

    # Figure 1 and the text beside it: three Boeing jets (kg converted to lb)
    for n, b in BOEING.items():
        rec(f"{n}-W0", fmt(round(b["mto"] * KG_LB, -2)))
        for part in ("oe", "payload", "fuel"):
            rec(f"{n}-{part}-frac", fmt(b[part] / b["mto"], 3))
    b767 = BOEING["767-300ER"]
    pay767 = round(b767["payload"] * KG_LB)
    rec("767-payload-lb", fmt(pay767))
    rec("767-W0-per-payload", fmt(400000.0 / pay767))
    rec("767-fit", fmt(float(empty_weight_fraction(400000.0)), 4))
    rec("767-oe-frac", fmt_dec(b767["oe"] / b767["mto"], 3))
    oe = sorted(b["oe"] / b["mto"] for b in BOEING.values())
    fu = sorted(b["fuel"] / b["mto"] for b in BOEING.values())
    rec("oe-min", fmt_dec(oe[0], 3))
    rec("oe-max", fmt_dec(oe[-1], 3))
    rec("fuel-min", fmt_dec(fu[0], 3))
    rec("fuel-max", fmt_dec(fu[-1], 3))
    rec("kg-lb", fmt(KG_LB))

    # Tables of published values
    for cls, (A, _, C) in EMPTY_WEIGHT_FIT.items():
        rec(f"fit-{cls}-A", f"{A:.2f}")
        rec(f"fit-{cls}-C", f"{abs(C):.2f}")
    rec("Kvs", f"{K_VS_VARIABLE:.2f}")
    for k, v in SEGMENT_FRACTION.items():
        rec(f"seg-{k}", f"{v:.3f}")
    rec("reserve", f"{RESERVE_FACTOR:.2f}")
    for name, cr, lt in SFC_TYPICAL:
        rec(f"sfc-{name}-cruise", f"{cr:.1f}")
        rec(f"sfc-{name}-loiter", f"{lt:.1f}")
    for name, v in LD_TYPICAL:
        rec(f"ld-{name}", v)
    rec("exp-min", f"{min(abs(c) for *_, c in EMPTY_WEIGHT_FIT.values()):.2f}")
    rec("exp-max", f"{max(abs(c) for *_, c in EMPTY_WEIGHT_FIT.values()):.2f}")

    # Units
    rec("nmi-ft", fmt_dec(NMI_FT, 1))
    rec("kt-fps", fmt(KT_FPS, 5))

    # The worked example (hand chain)
    rec("pax", str(N_PAX))
    rec("W-pax", fmt(W_PAX, 3))
    rec("W-person", fmt(W_PERSON, 3))
    rec("W-pay", fmt(ex["W_pay"]))
    rec("W-crew", fmt(ex["W_crew"]))
    rec("W-fixed", fmt(ex["W_fixed"]))
    rec("R", fmt(R_NMI))
    rec("V", fmt(V_KT, 3))
    rec("LD-cr", fmt(LD_CR, 2))
    rec("LD-lt", fmt(LD_LT, 2))
    rec("x-cr", fmt_dec(ex["x_cr"], 5))
    rec("f-cr", fmt_dec(ex["f_cr"], 5))
    rec("x-lt", fmt(ex["x_lt"], 5))
    rec("f-lt", fmt_dec(ex["f_lt"], 5))
    rec("f-cr-lt", fmt_dec(r5(ex["f_cr"] * ex["f_lt"]), 5))       # cruise times loiter, as the page groups it
    close_to(r5(r5(SEGMENT_FRACTION["warm-up and takeoff"] * SEGMENT_FRACTION["climb"]) * r5(ex["f_cr"] * ex["f_lt"])
                * SEGMENT_FRACTION["landing"]), ex["Wx"], 1e-12, "the grouped product gives the same W5/W0")
    for i, wi in enumerate(ex["Wi"][2:], start=2):
        rec(f"W{i}", fmt_dec(wi, 5))
    rec("Wx", fmt_dec(ex["Wx"], 5))
    rec("burn", fmt_dec(ex["burn"], 5))
    rec("Wf", fmt_dec(ex["Wf"], 5))
    rec("guess-exact", fmt(round(ex["guess_exact"])))
    rec("guess", fmt(ex["guess"]))
    for i, r in enumerate(ex["rows"], start=1):
        rec(f"it{i}-guess", fmt(r["guess"]))
        rec(f"it{i}-We", fmt_dec(r["We"], 5))
        rec(f"it{i}-new", fmt(r["new"]))
        rec(f"it{i}-pct", fmt(abs(r["pct"]), 3))
    rec("n-passes", str(len(ex["rows"])))
    rec("W0", fmt(ex["W0"]))
    rec("We-W0", fmt_dec(ex["We_W0"], 5))
    rec("We", fmt(ex["We"]))
    rec("Wf-lb", fmt(ex["Wf_lb"]))
    rec("sum", fmt(ex["sum"]))
    rec("sum-short", str(int(ex["W0"] - ex["sum"])))
    rec("W0-full", fmt(round(full)))
    rec("W0-full-diff", str(int(ex["W0"] - round(full))))
    rec("W0-full-diff-pct", fmt_dec(100.0 * (ex["W0"] - full) / full, 3))
    rec("We-W0-3", fmt_dec(ex["We_W0"], 3))
    rec("Wf-3", fmt_dec(ex["Wf"], 3))
    rec("W0-per-fixed", fmt(ex["W0"] / ex["W_fixed"]))
    cr_burn = ex["Wi"][2] - ex["Wi"][3]
    assert cr_burn > 0.25                                            # "more than a quarter"

    # Why it converges
    rows = ex["rows"]
    for i in range(1, len(rows)):
        a, b = rows[i - 1]["change"], rows[i]["change"]
        rec(f"ch{i}", f"{int(abs(a)):,}")
        rec(f"ratio{i}", fmt(abs(b / a), 4))
    last = int(abs(rows[-1]["change"]))
    rec(f"ch{len(rows)}", f"{last:,}")
    # the arithmetic argument: a 1% higher guess, with the converged fractions
    f101 = 1.01 ** ex["Cexp"]
    d_we = ex["We_W0"] * (1.0 - f101)                               # the fall of We/W0
    assert fmt_dec(ex["Cexp"], 2) == "−0.06" or abs(ex["Cexp"] + 0.06) < 1e-12
    rec("conv-1pct-factor", fmt_dec(f101, 5))
    rec("conv-dwe", fmt_dec(d_we, 5))
    rec("conv-den", fmt_dec(ex["den"], 5))
    rec("conv-den-pct", fmt_dec(100.0 * d_we / ex["den"], 2))
    close_to(d_we / ex["den"], abs(ex["k"]) * 0.01, 2e-5, "a 1% change gives the slope of the pass, 0.15")

    # Sensitivity
    for R in (4000.0, 6000.0):
        rec(f"W0-R{int(R)}", fmt(round(full_example(R=R))))
    base, cases = sensitivities()
    for name, v in cases:
        rec(f"sens-{name}", fmt(v, 3))
    rec("ld-exp-rise", fmt(100.0 * (1.0 / 0.9 - 1.0), 3))
    rec("pay-1000", fmt(round(full_example(pay=N_PAX * W_PAX + 1000.0) - base)))
    Rs = np.linspace(500.0, 9000.0, 341)
    r_cut = max(R for R in Rs if full_example(R=R, LD=15.0) / 1000.0 < 890.0)
    rec("R-cut-15", fmt(r_cut))
    return ex
