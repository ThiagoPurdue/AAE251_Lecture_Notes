"""Figures and values of 1.2 Hazards and Risk (notes/chapter-1/hazards-and-risk.md).

Nine figures, one function each, and values(), which records every number the page prints.
Run through the runner only:  python3 -B scripts/make_chapter_1_figures.py p12

Published constants (bird-strike altitudes, icing band, jet streams, radiation belts, atomic
oxygen, debris, Hubble's orbit) are in chapter_1/environment.py and Earth's in
chapter_1/constants.py, each with its source; the F10.7 data are in p12_f107_monthly.csv beside
this module (its header gives the source).
The small launch vehicle, its risks, scores and event times are invented for the example,
and so is the reliability 0.97.
"""
import csv
from pathlib import Path

from chapter_1.common import *
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.ticker as mticker

HERE = Path(__file__).resolve().parent

# ===================================================================== constants of the page
AIRPORT_H = 1600.0                  # m: elevation of the example airport (invented)
AIRPORT_T_C = 35.0                  # C: afternoon temperature of the example (invented)
INNER_MI, OUTER_MI = INNER_BELT_MI, OUTER_BELT_MI
AO_KM = ATOMIC_OXYGEN_KM
R_EARTH = RADIUS_EARTH_EQ           # km, equatorial radius

R_UNIT = 0.97                       # reliability of one flight computer over the mission (invented)

# The worked example: (id, short name, before (L, C), after (L, C)). R1 to R4 typical of
# a first flight; R5 added from the triggered-lightning hazard (NASA-STD-4010A).
RISKS = [
    ("R1", "engine test", (4, 3), (2, 3)),
    ("R2", "mass growth", (3, 4), (2, 4)),
    ("R3", "winds aloft", (4, 2), (4, 1)),
    ("R4", "late avionics", (3, 3), (2, 2)),
    ("R5", "lightning", (2, 5), (1, 5)),
]

# the launch timeline of the invented vehicle: number, phase, time after liftoff
PHASES = [
    (1, "Liftoff,\nstage 1\nburn", "0 to 2.5 min"),          # broken by hand: a stage keeps its number
    (2, "Stage\nseparation", "2.5 min"),
    (3, "Stage 2\nignition", "2.6 min"),
    (4, "Fairing\nseparation", "3 min"),
    (5, "Stage 2\ncutoff in\norbit", "9 min"),
    (6, "Payload\nseparation", "10 min"),
]
SPF_PHASES = (2, 3, 4, 6)           # events with a single-point failure in the example


def level(L, C):
    """The level of a risk under the rule of these notes: High when L x C >= 15, Medium from 5
    to 12, Low when 4 or less. Example: level(4, 3) -> 'Medium'"""
    s = L * C
    return "High" if s >= 15 else ("Medium" if s >= 5 else "Low")


def t_alt(T_K):
    """Standard-day altitude (m, troposphere) where the temperature is T_K."""
    return altitude_from_temperature(T_K, layer_of(0.0))


def f107_monthly():
    """Decimal years and monthly mean F10.7 (sfu) from p12_f107_monthly.csv."""
    t, f = [], []
    with open(HERE / "p12_f107_monthly.csv") as fh:
        rows = [r for r in fh if not r.startswith("#")]
    for r in csv.DictReader(rows):
        t.append(int(r["year"]) + (int(r["month"]) - 0.5) / 12.0)
        f.append(float(r["f107_adjusted_sfu"]))
    return np.array(t), np.array(f)


def smooth13(f):
    """13-month running mean (the half-weight ends of the usual smoothing), NaN at the ends."""
    w = np.r_[0.5, np.ones(11), 0.5] / 12.0
    out = np.full_like(f, np.nan)
    out[6:-6] = np.convolve(f, w, mode="valid")
    return out


def cycle_maxima(t, s):
    """Times and values of the maxima of the smoothed series, one per solar cycle (a maximum is
    the largest value within +-4 years)."""
    idx = []
    for i in range(len(s)):
        if np.isnan(s[i]):
            continue
        lo, hi = np.searchsorted(t, t[i] - 4.0), np.searchsorted(t, t[i] + 4.0)
        win = s[lo:hi]
        if s[i] == np.nanmax(win) and t[i] - 4.0 >= t[0] and t[i] + 1.0 <= t[-1]:
            idx.append(i)
    return t[idx], s[idx]


# ===================================================================== drawing helpers of this page
_TBARS = iter(range(1, 10000))      # numbers the drawing groups, so the SVG is the same on every run


def _tbar(ax, p0, p1, lw=1.4, bar=7.0, zorder=3):
    """The "mitigation acts here" link: a dashed line from p0 to p1 (data) ending in a short
    bar across it at p1 (a blocking mark, never an arrowhead). Returns the line."""
    ln = ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=INK, lw=lw, ls=(0, (4.0, 2.5)), zorder=zorder,
                 solid_capstyle="butt", dash_capstyle="butt")[0]
    d = np.asarray(p1, float) - np.asarray(p0, float)
    u = d / np.hypot(*d)
    n = np.array([-u[1], u[0]]) * pt(ax, bar / 2.0)
    b = ax.plot([p1[0] - n[0], p1[0] + n[0]], [p1[1] - n[1], p1[1] + n[1]], color=INK, lw=2.2, zorder=zorder,
                solid_capstyle="butt")[0]
    ln.set_gid("grp:tbar%d" % next(_TBARS))
    b.set_gid(ln.get_gid())
    return ln


def _rect(ax, x0, y0, x1, y1, fc, hatch=None, ec=INK, lw=LW_BOX, ls="-", zorder=3, name=None):
    pa = ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=ec, lw=lw, ls=ls, zorder=zorder))
    if hatch:
        pa.set_hatch(hatch)
    return pa


def _marker(ax, xy, s, after, r=10.5, fs=FS_SMALL, zorder=8):
    """A risk marker: a circle of radius r points with its name inside. Before mitigation: white
    with a dashed ring; after: Purdue gold with a solid ring. Both carry black text."""
    rr = pt(ax, r)
    c = ax.add_patch(opaque(Circle(xy, rr, fc=GOLD if after else "white", ec=INK, lw=1.6 if after else 1.3,
                                   ls="-" if after else (0, (2.5, 1.6)), zorder=zorder)))
    c._name = s
    t = ax.text(xy[0], xy[1], s, ha="center", va="center", fontsize=fs, color=INK, zorder=zorder + 1)
    t._in_box = c
    return c


# ===================================================================== 1. the anatomy of a hazard
def hazard_anatomy():
    """Lesson: a hazard sits between a cause and an effect, and each mitigation acts on one
    link of that chain: it keeps the vehicle away from the cause, removes the hazard, or softens
    the effect."""
    fig, axs = new_axes(6.5, 5.4, nrows=2)
    W = 2.35
    xs = [2.75, 5.55, 8.35]
    rows = [
        ("(a) Icy road", ["Water, snow, or oil on the road", "Slippery road", "Car slides and may crash"],
         [(1, "Salt or sand\nthe road"), (2, "Drive slower;\nfit snow tires")]),
        ("(b) Wing icing", ["Supercooled drops in a cloud", "Ice on the wing", "Less lift, more drag; early stall"],
         [(0, "Fly around\nor out of\nthe cloud"), (1, "Heat\nthe wing\n(anti-ice)")]),
    ]
    for k, (ax, (title, chain, mits)) in enumerate(zip(axs, rows)):
        set_frame(ax, -0.05, 9.6, -2.2, 1.75)
        bs = row(ax, chain, 0.2, xs[0] - W / 2, W, gap=(xs[1] - xs[0] - W) / pt(ax, 1.0),
                 fills=[None, BOX_FILL_START, None])
        for a_, b_ in zip(bs[:-1], bs[1:]):
            route(ax, a_, "right", b_, "left")
        top = bs[0].cy + bs[0].h / 2
        text(ax, (-0.05, top), title, ha="left", va="bottom", offset=(0, 6), fontweight="bold", backing=False)
        if k == 0:                                    # the column heads, once, on their own line
            for b_, h in zip(bs, ("Cause", "Hazard", "Effect")):
                text(ax, (b_.cx, top), h, direction=90, dist=26, fontweight="bold", backing=False)
        ymit = -1.5
        ax.text(-0.05, ymit, "Mitigation", ha="left", va="center", fontsize=FS_LABEL, fontstyle="italic")
        h_mit = max(box_height(ax, s_, keep_breaks=True) for _, s_ in mits)     # one height in a row
        for target, s_ in mits:
            tb = bs[target]
            mb = box(ax, (tb.cx, ymit), s_, w=W, h=h_mit, fill="white", rounded=False, keep_breaks=True)
            mb.patch.set_linestyle((0, (4.0, 2.5)))
            _tbar(ax, (tb.cx, mb.cy + mb.h / 2), (tb.cx, tb.cy - tb.h / 2 - pt(ax, 1.0)))
        if k == 1:                                    # the key: the two kinds of link
            kx, ky = xs[2] - W / 2 + 0.05, -1.05
            kind_arrow(ax, (kx, ky), (kx + 0.6, ky), "leads_to")
            text(ax, (kx + 0.6, ky), "leads to", direction=0, dist=6, fs=FS_SMALL)
            _tbar(ax, (kx, ky - 0.55), (kx + 0.6, ky - 0.55))
            text(ax, (kx + 0.6, ky - 0.55), "acts on", direction=0, dist=6, fs=FS_SMALL)
    assert len(rows) == 2 and all(len(r[1]) == 3 for r in rows)
    save_figure(fig, "p12-hazard-anatomy")


# ===================================================================== 6. the risk matrix
def _matrix_cells():
    """Fills and hatches of the 25 cells, top row (L = 5) first. The High cells get a lighter
    hatch than the shared style: thin, widely spaced lines, so a number on them stays readable."""
    fills, hatches = [], []
    for L in range(5, 0, -1):
        rf, rh = [], []
        for C in range(1, 6):
            lev = level(L, C)
            rf.append(RISK_STYLE[lev]["fill"])
            rh.append("//" if RISK_STYLE[lev]["hatch"] else None)
        fills.append(rf)
        hatches.append(rh)
    return fills, hatches


def _thin_hatch(cells):
    for b in cells.values():
        if b.patch.get_hatch():
            b.patch.set_hatch_linewidth(0.5)


def _level_edges(ax, cw, ch, lw=2.4):
    """The two stair-step boundaries between the levels, drawn as heavy lines along the cell
    edges where the level changes, so Low, Medium, and High read without the shading."""
    segs = []
    for L in range(1, 6):
        for C in range(1, 6):
            if C < 5 and level(L, C) != level(L, C + 1):          # vertical edge to the right
                segs.append(((C * cw, (L - 1) * ch), (C * cw, L * ch)))
            if L < 5 and level(L, C) != level(L + 1, C):          # horizontal edge above
                segs.append((((C - 1) * cw, L * ch), (C * cw, L * ch)))
    gid = "grp:leveledges"
    frame = Rectangle((0.0, 0.0), 5 * cw, 5 * ch, transform=ax.transData)   # no cap sticks out past the frame
    for (x0, y0), (x1, y1) in segs:
        ln = ax.plot([x0, x1], [y0, y1], color=INK, lw=lw, solid_capstyle="projecting", zorder=6, gid=gid)[0]
        ln.set_clip_path(frame)
    return segs


def _tab(ax, xy, s, fs=FS_LABEL, zorder=7):
    """A number on a small white tab with a thin ring, for a cell whose hatch would hide it."""
    w, h = text_size(ax, s, fs)
    pw, ph = w + pt(ax, 10.0), h + pt(ax, 6.0)
    pa = ax.add_patch(opaque(FancyBboxPatch((xy[0] - pw / 2, xy[1] - ph / 2), pw, ph,
                                            boxstyle=f"round,pad=0,rounding_size={pt(ax, 3.0)}", fc="white",
                                            ec=INK, lw=0.6, zorder=zorder)))
    pa._box = "matrix"                                # it sits inside a matrix cell, so the two may touch
    pa._name = "tab " + s
    t = ax.text(xy[0], xy[1], s, ha="center", va="center", fontsize=fs, color=INK, zorder=zorder + 1)
    t._in_box = pa
    return pa


def risk_matrix():
    """Lesson: a risk's place on the matrix is its likelihood (row) and consequence (column);
    their product sets its level, High from 15, Medium from 5 to 12, Low 4 or less."""
    fig, ax = new_axes(6.5, 3.6)
    fig.subplots_adjust(0, 0, 1, 1)
    set_frame(ax, -1.3, 9.9, -1.3, 4.65)
    fills, hatches = _matrix_cells()
    cells = [[("" if level(L, C) == "High" else str(L * C)) for C in range(1, 6)] for L in range(5, 0, -1)]
    cw, ch = 1.0, 0.9
    m = matrix(ax, (0.0, 0.0), cells, cw, ch, [str(i) for i in range(5, 0, -1)], [str(j) for j in range(1, 6)],
               fills=fills, hatches=hatches)
    _thin_hatch(m)
    for (i, j), b in m.items():                       # the High numbers, on white tabs
        L, C = 5 - i, j + 1
        if level(L, C) == "High":
            _tab(ax, (b.cx, b.cy), str(L * C))
    _level_edges(ax, cw, ch)
    text(ax, (-0.85, 2.25), "Likelihood, L", rotation=90, fs=FS_LABEL, backing=False)
    text(ax, (2.5, -0.85), "Consequence, C", fs=FS_LABEL, backing=False)
    # the reading of one cell: L = 4, C = 3
    cell = m[(1, 2)]
    e = pt(ax, 4.0)
    fr = ax.add_patch(Rectangle((cell.cx - cw / 2 + e, cell.cy - ch / 2 + e), cw - 2 * e, ch - 2 * e, fc="none",
                                ec=INK, lw=1.6, ls=(0, (3.0, 2.0)), zorder=5))
    fr._box = "matrix"
    fr._name = "example frame"
    ax.text(5.7, 1.0, "Framed cell (dashed): L = 4 and C = 3,\nscore 4 × 3 = 12, Medium", ha="left", va="center",
            fontsize=FS_SMALL, linespacing=1.3)
    y = 4.0
    for lev, rule in (("High", "15 to 25"), ("Medium", "5 to 12"), ("Low", "1 to 4")):
        st = RISK_STYLE[lev]
        sw = ax.add_patch(opaque(Polygon([(5.7, y - 0.27), (6.25, y - 0.27), (6.25, y + 0.27), (5.7, y + 0.27)],
                                         closed=True, fc=st["fill"], ec=INK, lw=LW_BOX, zorder=3)))
        if st["hatch"]:
            sw.set_hatch("//")
            sw.set_hatch_linewidth(0.5)
        sw._box = None
        sw._name = lev
        text(ax, (6.25, y), f"{lev}: L × C = {rule}", direction=0, dist=6)
        y -= 0.8
    ax.plot([5.7, 6.25], [y + 0.05, y + 0.05], color=INK, lw=2.4, solid_capstyle="butt")
    text(ax, (6.25, y + 0.05), "boundary between levels", direction=0, dist=6)
    n_high = sum(level(L, C) == "High" for L in range(1, 6) for C in range(1, 6))
    assert len(m) == 25 and n_high == 6, n_high
    trim_canvas(fig)
    save_figure(fig, "p12-risk-matrix")


# ===================================================================== 7. the worked example on the matrix
def risk_moves():
    """Lesson: mitigation lowers one of the two scores, and the risk moves on the matrix; in
    the matrix of these notes a lower likelihood is down and a lower consequence is left, and a
    consequence-5 risk stays Medium at best."""
    fig, ax = new_axes(6.5, 4.3)
    fig.subplots_adjust(0, 0, 1, 1)
    cw = ch = 1.25
    set_frame(ax, -1.3, 10.6, -1.35, 6.5)
    fills, hatches = _matrix_cells()
    m = matrix(ax, (0.0, 0.0), [[""] * 5 for _ in range(5)], cw, ch, [str(i) for i in range(5, 0, -1)],
               [str(j) for j in range(1, 6)], fills=fills, hatches=hatches)
    _thin_hatch(m)
    _level_edges(ax, cw, ch)
    text(ax, (-0.85, 2.5 * ch), "Likelihood, L", rotation=90, backing=False)
    text(ax, (2.5 * cw, -0.85), "Consequence, C", backing=False)
    # the product of every cell, small, in its upper-left corner (on a tab where the cell is hatched)
    for L in range(1, 6):
        for C in range(1, 6):
            xy = ((C - 1) * cw + pt(ax, 11.0), L * ch - pt(ax, 9.5))
            if level(L, C) == "High":
                _tab(ax, xy, str(L * C), fs=FS_SMALL)
            else:
                t = ax.text(*xy, str(L * C), ha="center", va="center", fontsize=FS_SMALL, color=INK, zorder=5)
                t._in_box = m[(5 - L, C - 1)].patch
    # the three levels named in free cells
    for (L, C, lev) in ((1, 1, "Low"), (5, 1, "Medium"), (5, 5, "High")):
        xy = ((C - 0.5) * cw, (L - 0.62) * ch)
        if lev == "High":
            _tab(ax, xy, lev, fs=FS_SMALL)
        else:
            t = ax.text(*xy, lev, ha="center", va="center", fontsize=FS_SMALL, color=INK, fontweight="bold", zorder=5)
            t._in_box = m[(5 - L, C - 1)].patch
    # marker positions: cell centers, nudged where an arrow passes through a cell
    nudge = {("R1", 0): (0.2, -0.1), ("R1", 1): (0.2, 0.0),                           # no two arrows cross,
             ("R4", 0): (-0.2 - pt(ax, 4.0), -0.1)}                                   # none grazes a marker

    def at(rid, k, L, C):
        dx, dy = nudge.get((rid, k), (0.0, 0.0))
        return np.array([(C - 0.5) * cw + dx, (L - 0.5) * ch + dy])

    rr = pt(ax, 10.5)
    for rid, _, b, a in RISKS:
        p0, p1 = at(rid, 0, *b), at(rid, 1, *a)
        d = p1 - p0
        u = d / np.hypot(*d)
        kind_arrow(ax, p0 + u * (rr + pt(ax, 1.5)), p1 - u * (rr + pt(ax, 2.5)), "leads_to", head="small")
        _marker(ax, p0, rid, False)
        _marker(ax, p1, rid, True)
    # the key
    x0, y = 6.75, 5.9
    _marker(ax, (x0 + rr, y), "R1", False)
    text(ax, (x0 + 2 * rr, y), "before mitigation", direction=0, dist=6, fs=FS_SMALL)
    y -= 0.75
    _marker(ax, (x0 + rr, y), "R1", True)
    text(ax, (x0 + 2 * rr, y), "after mitigation", direction=0, dist=6, fs=FS_SMALL)
    y -= 0.75
    kind_arrow(ax, (x0, y), (x0 + 2 * rr, y), "leads_to", head="small")
    text(ax, (x0 + 2 * rr, y), "move made by the mitigation", direction=0, dist=6, fs=FS_SMALL)
    y -= 0.75
    ax.plot([x0, x0 + 2 * rr], [y, y], color=INK, lw=2.4, solid_capstyle="butt")
    text(ax, (x0 + 2 * rr, y), "boundary between levels", direction=0, dist=6, fs=FS_SMALL)
    y -= 0.75
    text(ax, (x0, y), "Number in a corner:\nthe score L × C", ha="left", fs=FS_SMALL, backing=False)
    down = sum(a[0] < b[0] for _, _, b, a in RISKS)
    left = sum(a[1] < b[1] for _, _, b, a in RISKS)
    assert down == 4 and left == 2, (down, left)
    assert level(*RISKS[4][3]) == "Medium", "R5 stays Medium"
    trim_canvas(fig)
    save_figure(fig, "p12-risk-moves")


# ===================================================================== 2. hazards along a flight
FLIGHT_HAZARDS = [                 # number, name (the table on the page uses the same numbers)
    (1, "hot and high airport"), (2, "runway debris"), (3, "bird strike"), (4, "icing"),
    (5, "clear-air turbulence"), (6, "volcanic ash"), (7, "thunderstorm and lightning"),
    (8, "wind shear and microburst"), (9, "low visibility"),
]


def _profile():
    """The schematic flight path: x (arbitrary units, equal aspect with km), altitude (km)."""
    x = np.linspace(0.0, 30.0, 1201)
    h = np.zeros_like(x)
    cl = (x >= 2.6) & (x < 9.5)                     # climb: smooth rise to 11 km
    t = (x[cl] - 2.6) / 6.9
    h[cl] = 11.0 * (3 * t ** 2 - 2 * t ** 3) ** 0.75
    h[(x >= 9.5) & (x < 18.5)] = 11.0               # cruise
    de = (x >= 18.5) & (x < 27.4)                   # descent and approach
    t = (x[de] - 18.5) / 8.9
    h[de] = 11.0 * (1.0 - (3 * t ** 2 - 2 * t ** 3)) ** 1.3
    return x, h


def _band_edges(ax, y0, y1, x0=-0.6, x1=31.2):
    """Thin dashed gray lines along the top and bottom of a shaded band, so its edges read
    without the faint fill (3:1 against white)."""
    for y in (y0, y1):
        ax.plot([x0, x1], [y, y], color=GRAY, lw=0.8, ls=(0, (4.0, 3.0)), zorder=1.5)


def _tower_side(base, top, x_base, x_top, sizes, side):
    """One side of a cumulonimbus tower from (x_base, base) up to (x_top, top): rounded bulges
    of unequal height and depth (sizes, from the bottom up, as fractions), bulging outward
    (side -1: to the left, +1: to the right), joined at cusps."""
    pts = []
    sz = np.asarray(sizes, float)
    edges = base + (top - base) * np.r_[0.0, np.cumsum(sz) / sz.sum()]
    for k in range(len(sz)):
        ya, yb = edges[k], edges[k + 1]
        xa = x_base + (x_top - x_base) * (ya - base) / (top - base)
        xb = x_base + (x_top - x_base) * (yb - base) / (top - base)
        t = np.linspace(-0.5 * np.pi, 0.5 * np.pi, 18)
        depth = 0.25 + 0.5 * sz[k] / sz.max() * 0.45
        pts += list(zip(0.5 * (xa + xb) + side * depth * np.cos(t), 0.5 * (ya + yb) + 0.5 * (yb - ya) * np.sin(t)))
    return pts


def flight_hazards():
    """Lesson: each atmospheric hazard belongs to a phase of flight and a band of altitude; the
    airports and the low air around them hold more of the hazards than cruise does."""
    fig, ax = data_axes(6.5, 4.0, grid=False)
    fig.subplots_adjust(bottom=0.24, top=0.98)
    ax.set_xlim(-0.6, 31.2)
    ax.set_ylim(0.0, 13.6)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
    ax.set_ylabel("Altitude, km")
    ax.set_xlabel("Distance along the route (not to scale)")
    fig.canvas.draw()
    x, h = _profile()
    bird_km = BIRD_FT * FT / 1000.0
    ice0, ice1 = t_alt(273.15 + ICE_T_TOP_C) / 1000.0, t_alt(273.15 + ICE_T_BOT_C) / 1000.0
    ax.add_patch(Rectangle((-0.6, 0.0), 31.8, bird_km, fc="#E6E6E6", ec="none", zorder=1))
    ax.add_patch(Rectangle((-0.6, ice0), 31.8, ice1 - ice0, fc=FLUID_FILL, ec="none", zorder=1))
    _band_edges(ax, ice0, ice1)
    _band_edges(ax, bird_km, bird_km)
    text(ax, (31.2, 0.5 * (ice0 + ice1)), "icing band:\n0 to −20 °C", direction=0, dist=5, fs=FS_SMALL)
    text(ax, (31.2, 0.5 * bird_km), "most bird\nstrikes", direction=0, dist=5, fs=FS_SMALL)
    # the thunderstorm over the arrival airport, a cumulonimbus: a flat base at 1.6 km, a tower
    # of rounded bulges of unequal size (cumuliform), and a flat-topped anvil spreading out near 12 km
    left = _tower_side(1.6, 9.0, 25.1, 25.45, (1.25, 1.0, 0.8, 0.6), -1)
    right = _tower_side(1.6, 9.0, 28.6, 28.3, (1.1, 0.85, 0.65), +1)[::-1]
    anvil = catmull_rom([(25.45, 9.0), (24.4, 9.75), (23.2, 10.35), (22.5, 10.95), (23.0, 11.6), (24.6, 11.95),
                         (27.0, 12.05), (29.3, 12.0), (30.35, 11.8), (30.25, 11.3), (29.4, 10.75), (28.6, 9.75),
                         (28.3, 9.0)], n=10)
    cb = np.vstack([np.array(left), anvil, np.array(right)])
    ax.add_patch(opaque(Polygon(np.vstack([cb, cb[:1]]), closed=True, fc="#D9D9D9", ec=INK,
                                lw=LW_DETAIL, zorder=2)))
    ln = ax.plot(x, h, **line_kw(0), zorder=4)[0]
    motion_heads(ax, x, h, (0.12, 0.56, 0.74), line=ln)
    ax.plot([0.2, 2.9], [0.0, 0.0], color=INK, lw=5.0, solid_capstyle="butt", zorder=3)    # runways
    ax.plot([27.2, 29.9], [0.0, 0.0], color=INK, lw=5.0, solid_capstyle="butt", zorder=3)
    hx = lambda xx: float(np.interp(xx, x, h))                                   # noqa: E731
    x_bird = 3.05                                                                 # a point of the climb in the band
    y_gap = 0.5 * (bird_km + ice0)                                                # the white gap between the bands
    pts = {1: ((0.8, 0.0), (0.8, 3.1)), 2: ((2.3, 0.0), (2.3, 1.6)), 3: ((x_bird, hx(x_bird)), (5.0, y_gap)),
           4: ((5.05, hx(5.05)), (7.2, 3.9)), 5: ((12.0, 11.0), (12.0, 12.7)), 6: ((16.0, 11.0), (16.0, 12.7)),
           7: ((26.7, 7.2), (21.9, 8.6)), 8: ((26.4, hx(26.4)), (22.3, y_gap)), 9: ((29.4, 0.0), (30.3, y_gap))}
    R_DISC = 8.0                                                                  # pt, the chapter's callout disc
    r_disc = pt(ax, R_DISC)                                                       # the disc radius, km
    for n, (target, at) in pts.items():
        numbered_callout(ax, target, n, at, r=R_DISC)
        x0_, x1_ = ax.get_xlim()
        y0_, y1_ = ax.get_ylim()
        assert x0_ + r_disc < at[0] < x1_ - r_disc and y0_ + r_disc < at[1] < y1_ - r_disc, \
            f"disc {n} lies inside the plot frame"
    assert 2 * r_disc < ice0 - bird_km + pt(ax, 1.0), "a disc in the gap between the bands covers neither band"
    text(ax, (5.0, 8.0), "climb", fs=FS_SMALL, backing=False)
    text(ax, (14.0, 10.2), "cruise", fs=FS_SMALL, backing=False)
    text(ax, (19.0, 7.5), "descent", fs=FS_SMALL, backing=False)
    # the key to the numbers, under the plot (the table on the page repeats it with causes and effects)
    kax = fig.add_axes([0.02, 0.0, 0.96, 0.18])
    kax.axis("off")
    kw_in, kh_in = 0.96 * 6.5, 0.18 * 4.0
    kax.set_xlim(0.0, kw_in)
    kax.set_ylim(0.0, kh_in)
    kax.set_aspect("equal")
    fig.canvas.draw()
    cols = [0.15, 2.05, 3.95]
    rows = [kh_in - 0.13, kh_in - 0.37, kh_in - 0.61]
    for k, (n, name) in enumerate(FLIGHT_HAZARDS):
        xy = (cols[k // 3], rows[k % 3])
        key_disc(kax, xy, n, r=R_DISC)
        text(kax, xy, name, ha="left", direction=0.0, dist=12.0, fs=FS_SMALL, backing=False)
    assert abs(hx(14.0) - 11.0) < 1e-9 and 2.0 < ice0 < ice1 < 6.0, (ice0, ice1)
    assert 0.0 < hx(x_bird) < bird_km, "the bird strike is marked inside the band where most strikes happen"
    assert hx(5.05) > ice0 - 0.5, "the icing mark lies at the icing band"
    assert cb[:, 1].max() > 11.5 and np.ptp(cb[cb[:, 1] > 10.0][:, 0]) > np.ptp(cb[cb[:, 1] < 8.0][:, 0]), \
        "the cloud spreads into an anvil at the top"
    assert hx(25.4) < 1.6 and hx(25.0) < 1.6 + 0.2, "the approach passes under the storm's base"
    save_figure(fig, "p12-flight-hazards")


# ===================================================================== 2b. the microburst
def _approach(x, x_td, y_td, slope):
    """The planned approach path: a straight line down to the touchdown point (x_td, y_td)."""
    return y_td + slope * (x_td - np.asarray(x, float))


def microburst():
    """Lesson: a microburst's downdraft spreads out at the ground, so an aircraft on approach
    meets a headwind (airspeed rises, it floats above the path), then the downdraft, then a
    tailwind (airspeed falls, it sinks below the path), close to the ground. The outflow is
    drawn as a layer of moving air along the ground that the approach flies through."""
    H = 3.7
    fig, ax = canvas(6.5, H)                          # data units are inches; schematic, not to scale
    yg = 1.15                                         # ground; the key sits below it
    x_td, slope = 5.75, 0.22                          # touchdown point and approach slope (schematic, flat)
    ax.plot([0.05, 6.45], [yg, yg], color=INK, lw=LW_OUTLINE, zorder=3, solid_capstyle="butt")
    ax.plot([5.45, 6.4], [yg, yg], color=INK, lw=5.0, solid_capstyle="butt", zorder=3.5)   # runway
    text(ax, (5.92, yg), "runway", direction=-90, dist=6, fs=FS_SMALL, backing=False)
    # the storm cloud: a flat base, a bumpy top
    xd = 3.0                                          # the axis of the downdraft
    xc0, xc1, ybase = xd - 1.0, xd + 1.0, yg + 2.0
    top = catmull_rom([(xc1, ybase), (xc1 + 0.1, ybase + 0.2), (xc1 - 0.15, ybase + 0.37), (xd + 0.45, ybase + 0.42),
                       (xd + 0.1, ybase + 0.5), (xd - 0.3, ybase + 0.43), (xd - 0.65, ybase + 0.35),
                       (xc0 + 0.05, ybase + 0.22), (xc0, ybase)], n=10)
    ax.add_patch(opaque(Polygon(np.vstack([[(xc0, ybase), (xc1, ybase)], top]), closed=True, fc="#D9D9D9", ec=INK,
                                lw=LW_DETAIL, zorder=2)))
    text(ax, (xc0, ybase + 0.2), "storm cloud", direction=180, dist=8, fs=FS_SMALL, backing=False)
    # the moving air: a column under the cloud that spreads into a layer along the ground,
    # tinted and edged with a dashed line, with open block arrows for the direction it moves
    depth, half = 1.3, 0.42                          # layer depth and half width of the column (in)
    xl0, xl1 = 1.15, 5.25                             # outer ends of the layer
    region = np.array([(xd - half, ybase), (xd - half, yg + depth), (xl0, yg + depth), (xl0, yg),
                       (xl1, yg), (xl1, yg + depth), (xd + half, yg + depth), (xd + half, ybase)])
    ax.add_patch(Polygon(region, closed=True, fc="#E8F1F8", ec="none", zorder=1))
    ax.plot(region[:, 0], region[:, 1], color=GRAY, lw=0.8, ls=(0, (4.0, 3.0)), zorder=1.5)
    y_foot = yg + 0.72                                # the downdraft reaches down near the ground
    flow_arrow(ax, (xd, ybase - 0.06), (xd, y_foot), width=16.0, head_width=28.0, head_len=16.0)
    text(ax, (xd + half, yg + 1.55), f"downdraft, up to\n{fmt(MICROBURST_DOWN_FPM)} ft/min", direction=0, dist=8,
         fs=FS_SMALL, backing=False)
    y_lo, y_hi = 0.10, 0.58                           # heights of the outflow arrows above the ground
    left = [((xd - 0.32, yg + y_lo), (1.25, yg + y_lo)), ((xd - 0.40, yg + y_hi), (1.40, yg + y_hi))]
    # the upper tailwind arrow starts clear of the air above position 3, and the lower one ends
    # where the planned approach is high enough to pass over its head
    right = [((xd + 0.32, yg + y_lo), (4.55, yg + y_lo)), ((3.95, yg + y_hi), (4.95, yg + y_hi))]
    for a_, b_ in left + right:
        flow_arrow(ax, a_, b_, width=7.0, head_width=13.0, head_len=9.0)
    wind = fmt(MICROBURST_WIND_KT, 2)
    text(ax, (xl0, yg + 0.5), f"outflow:\nheadwind for\nthe aircraft,\nup to {wind} knots", direction=180, dist=5,
         fs=FS_SMALL, backing=False)
    text(ax, (xl1, yg + 0.6), f"outflow:\ntailwind,\nup to {wind}\nknots", direction=0, dist=5, fs=FS_SMALL,
         backing=False)
    # the planned approach (thin dashed) and the path flown through the microburst (heavy)
    xs = np.linspace(0.05, x_td, 400)
    ya = _approach(xs, x_td, yg, slope)
    ax.plot(xs, ya, color=GRAY, lw=1.0, ls=(0, (5.0, 3.0)), zorder=4)
    dev = (0.14 * np.exp(-((xs - 1.9) / 0.55) ** 2)                      # floats up in the headwind
           - 0.13 / (1.0 + np.exp(-(xs - 3.45) / 0.3)))                  # sinks in the downdraft and tailwind
    dev -= dev[0]
    xe = 4.0                                                               # where the drawn path ends
    keep = xs <= xe
    xf, yf = xs[keep], (ya + dev)[keep]
    ln = ax.plot(xf, yf, **line_kw(0), zorder=5)[0]
    rides_on(arrow(ax, (xf[-4], yf[-4]), (xf[-1], yf[-1]), color=INK, lw=LW_MAIN, head="normal", zorder=5), ln)
    # the three positions, numbered along the path, named in a key below
    pos = {1: 1.9, 2: xd, 3: 3.7}
    yp = {n: float(np.interp(v, xf, yf)) for n, v in pos.items()}
    discs = {1: (pos[1] - 0.05, yp[1] + 0.45),
             2: (pos[2], yg + 0.27),                     # under its dot, between the two lower arrows
             3: (pos[3] - 0.08, yp[3] + 0.45)}           # above its dot, clear of the downdraft arrow
    for n, at in discs.items():
        numbered_callout(ax, (pos[n], yp[n]), n, at)
    keys = [(1, "headwind: airspeed rises, the aircraft floats above the planned approach"),
            (2, "downdraft: the aircraft is pushed down"),
            (3, f"tailwind: airspeed falls, up to {fmt(MICROBURST_SHEAR_KT, 2)} knots below its value at 1; "
                "the aircraft sinks"),
            (None, "below the planned approach, short of the runway")]
    y = yg - 0.4
    for n, s_ in keys:
        if n is not None:
            key_disc(ax, (0.2, y), n, r=8.0)
        text(ax, (0.2, y), s_, ha="left", direction=0.0, dist=12.0, fs=FS_SMALL, backing=False)
        y -= 0.2 if n is None or n == 3 else 0.24
    y -= 0.06                                          # the two kinds of line, sampled
    ax.plot([0.08, 0.5], [y, y], **line_kw(0), zorder=5)
    text(ax, (0.5, y), "path flown", direction=0.0, dist=6.0, fs=FS_SMALL, backing=False)
    ax.plot([2.0, 2.42], [y, y], color=GRAY, lw=1.0, ls=(0, (5.0, 3.0)), zorder=4)
    text(ax, (2.42, y), "planned approach", direction=0.0, dist=6.0, fs=FS_SMALL, backing=False)
    # what is drawn: a headwind before the downdraft and a tailwind after it, for an aircraft flying right
    hd = lambda n: float(_approach(pos[n], x_td, yg, slope))                          # noqa: E731
    assert yp[1] > hd(1), "1: above the planned approach in the headwind"
    assert yp[3] < hd(3), "3: below the planned approach in the tailwind"
    assert pos[1] < xd < pos[3] and xf[-1] > xf[0], "headwind, downdraft, tailwind, in the order the aircraft flies"
    for n in (1, 3):
        assert yg + y_hi < yp[n] < yg + depth or yg + y_lo < yp[n] < yg + y_hi, f"{n} lies inside the outflow layer"
    assert yg + y_lo < yp[3] < yg + y_hi, "3: the path flies between the two tailwind arrows"
    assert y_foot < yp[1] and yp[2] < y_foot - 0.1, "the downdraft reaches below position 1 and over position 2"
    head_half = 13.0 / 2 / 72 + LW_MAIN / 2 / 72                   # outflow head half width + half the path width (in)
    assert float(yf[-1]) - (yg + y_lo) > head_half + 0.03, "the path's arrowhead clears the lower tailwind arrow"
    for (a_, b_) in left + right:                                  # the path crosses no outflow arrow
        xa, xb = sorted((a_[0], b_[0]))
        seg = (xf >= xa) & (xf <= xb)
        if seg.any():
            assert np.all(np.abs(yf[seg] - a_[1]) > 7.0 / 2 / 72 + 0.04), "the path crosses an outflow arrow"
    # no callout leader crosses an outflow arrow (each arrow taken as its head's full width,
    # plus a margin); every disc stays clear of the downdraft arrow
    hw_o, hl_o, rr = pt(ax, 13.0 / 2), pt(ax, 9.0), pt(ax, 8.0)
    for n, at in discs.items():
        a = np.asarray(at, float); t = np.array([pos[n], yp[n]])
        u = (t - a) / np.hypot(*(t - a))
        seg = a + u * rr + np.linspace(0.0, 1.0, 200)[:, None] * (t - a - u * rr)
        for (a_, b_) in left + right:
            xa, xb = sorted((a_[0], b_[0]))
            inside = (seg[:, 0] > xa - 0.03) & (seg[:, 0] < xb + 0.03) & (np.abs(seg[:, 1] - a_[1]) < hw_o + 0.03)
            assert not inside.any(), f"the leader of callout {n} crosses an outflow arrow"
        assert a[0] - rr > xd + pt(ax, 28.0 / 2) + 0.04 or a[0] + rr < xd - pt(ax, 28.0 / 2) - 0.04 \
            or a[1] + rr < y_foot - 0.04, f"disc {n} stays clear of the downdraft arrow"
    # the planned approach clears every arrowhead by the head's half width
    for (a_, b_) in left + right:
        x0, x1 = sorted((b_[0], b_[0] - np.sign(b_[0] - a_[0]) * hl_o))
        xh = np.linspace(x0, x1, 50)
        gap = np.abs(_approach(xh, x_td, yg, slope) - a_[1])
        assert np.all(gap > hw_o + pt(ax, 1.0 / 2) + 0.03), "the planned approach crosses an arrowhead"
    trim_canvas(fig)
    save_figure(fig, "p12-microburst")


# ===================================================================== 3. the space environment against altitude
def space_altitudes():
    """Lesson: which space hazards a spacecraft meets depends on its altitude: drag and atomic
    oxygen low down, debris mostly below 2,000 km, the radiation belts above, and the outer belt
    around the geostationary orbit."""
    fig, ax = data_axes(6.5, 4.4, grid=False)
    ax.set_yscale("log")
    ax.set_ylim(100.0, 100000.0)
    sp = 1.22                                          # spacing of the bars
    ax.set_xlim(-0.55, 4 * sp + 2.05)
    ax.set_yticks([100, 1000, 10000, 100000])
    ax.yaxis.set_major_formatter(CommaFormatter())
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    ax.set_ylabel("Altitude above the surface, km")
    fig.canvas.draw()
    inner = [v * MILE_KM for v in INNER_MI]
    outer = [v * MILE_KM for v in OUTER_MI]
    cols = [("drag", 100.0, DRAG_YEARS_KM), ("atomic\noxygen", *AO_KM), ("most\ndebris", 100.0, DEBRIS_KM),
            ("inner\nbelt", *inner), ("outer\nbelt", *outer)]
    w = 0.62
    xs = [i * sp for i in range(len(cols))]
    for x, (name, lo, hi) in zip(xs, cols):
        ax.add_patch(Rectangle((x - w / 2, lo), w, hi - lo, fc=HIGHLIGHT, ec=INK, lw=LW_BOX, zorder=3))
    ax.set_xticks(xs, [c[0] for c in cols])
    ax.tick_params(axis="x", length=0)
    # the inner belt reaches down to Hubble's altitude over the South Atlantic
    x_in = xs[3]
    ax.add_patch(Rectangle((x_in - w / 2, HUBBLE_KM * 0.92), w, inner[0] - HUBBLE_KM * 0.92, fc="white", ec=INK,
                           lw=LW_BOX, ls=(0, (3.0, 2.0)), zorder=3))
    text(ax, (x_in + w / 2, 900.0), "South Atlantic\nAnomaly", direction=0, dist=5, fs=FS_SMALL, ha="left")
    # the geostationary ring of debris, named
    geo = geo_altitude()
    x_db = xs[2]
    ax.add_patch(Rectangle((x_db - w / 2, geo / 1.04), w, geo * (1.04 - 1 / 1.04), fc=HIGHLIGHT,
                           ec=INK, lw=LW_BOX, zorder=3))
    callout(ax, (x_db - w / 2, geo * 1.04), "debris in the\ngeostationary ring", at=(x_db - 1.05, 72000.0),
            fs=FS_SMALL, ha="center")
    x_end = xs[-1] + w / 2 + 0.15
    for alt, name in ((HUBBLE_KM, f"Hubble,\n{fmt(HUBBLE_KM, 3)} km"),
                      (geo, f"geostationary\norbit, {fmt(geo)} km")):
        ax.plot([-0.55, x_end], [alt, alt], **line_kw("boundary"), zorder=2)
        if alt < 1000.0:                              # under its line, clear of the anomaly's label
            text(ax, (x_end, alt * 0.93), name, fs=FS_SMALL, color=STEEL, ha="left", va="top", offset=(4, 0))
        else:
            text(ax, (x_end, alt), name, direction=0, dist=4, fs=FS_SMALL, color=STEEL, ha="left")
    assert inner[0] > DEBRIS_KM * 0.5 and outer[0] < geo < outer[1], (inner, outer, geo)
    assert xs[-1] + w / 2 > 0.6 * (ax.get_xlim()[1] - ax.get_xlim()[0]), "the bars span most of the axis"
    save_figure(fig, "p12-space-altitudes")


# ===================================================================== 4. the radiation belts
def _belt(L1, L2, Bm, side, n=160):
    """Outline (x, y in Earth radii) of the trapped region between the dipole field lines L1 and
    L2, closed at each end where the field strength reaches Bm (the mirror points), on one side
    of the magnetic axis. In a dipole, r = L cos^2(lat) and B ~ sqrt(1 + 3 sin^2(lat)) / r^3."""
    def lam_m(L):
        f = lambda lam: math.sqrt(1 + 3 * math.sin(lam) ** 2) / (L * math.cos(lam) ** 2) ** 3 - Bm  # noqa: E731
        lo, hi = 0.0, math.acos(math.sqrt(1.0 / L)) - 1e-9
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
        return lo

    def line(L, lams):
        r = L * np.cos(lams) ** 2
        return np.c_[side * r * np.cos(lams), r * np.sin(lams)]

    Ls = np.linspace(L1, L2, 40)
    lm = np.array([lam_m(L) for L in Ls])
    outer = line(L2, np.linspace(-lm[-1], lm[-1], n))
    top = np.vstack([line(L, np.array([a])) for L, a in zip(Ls[::-1], lm[::-1])])
    inner = line(L1, np.linspace(lm[0], -lm[0], n))
    bot = np.vstack([line(L, np.array([-a])) for L, a in zip(Ls, lm)])
    return np.vstack([outer, top, inner, bot])


def radiation_belts():
    """Lesson: the particles of the radiation belts are trapped on the field lines of Earth's
    magnetic field, so the belts are two nested rings around the magnetic equator; the
    geostationary orbit runs through the outer one."""
    fig, ax = new_axes(6.5, 3.9)
    fig.subplots_adjust(0, 0, 1, 1)
    set_frame(ax, -8.0, 9.8, -4.6, 4.6)
    inner = [1.0 + v * MILE_KM / R_EARTH for v in INNER_MI]
    outer = [1.0 + v * MILE_KM / R_EARTH for v in OUTER_MI]
    # the belts close where the particles turn back (their mirror points): drawn with the field
    # strength of the inner belt's inner edge at the equator, so that edge is one smooth curve
    r_m = inner[0] * (1.0 - 1e-6)
    lam1 = math.acos(math.sqrt(r_m / inner[0]))
    Bm = math.sqrt(1 + 3 * math.sin(lam1) ** 2) / r_m ** 3
    L_gap = 3.5                                        # a field line in the gap between the belts, right side only
    lc = math.acos(math.sqrt(1.0 / L_gap))
    lam = np.linspace(-lc, lc, 300)
    r = L_gap * np.cos(lam) ** 2
    ax.plot(r * np.cos(lam), r * np.sin(lam), color=GRAY, lw=LW_THIN, zorder=1.5)
    for side in (1, -1):
        ax.add_patch(opaque(Polygon(_belt(*inner, Bm, side), closed=True, fc=GOLD, ec=INK, lw=LW_DETAIL, zorder=2)))
        ax.add_patch(opaque(Polygon(_belt(*outer, Bm, side), closed=True, fc=HIGHLIGHT, ec=INK, lw=LW_DETAIL,
                                    zorder=2)))
    ax.add_patch(opaque(Circle((0, 0), 1.0, fc="white", ec=INK, lw=LW_OUTLINE, zorder=4)))
    ax.plot([0, 0], [-3.2, 2.5], **line_kw("boundary"), zorder=1)
    text(ax, (0.0, -3.2), "magnetic axis", direction=-90, dist=3, color=STEEL)
    text(ax, (0.0, 0.0), "Earth", fs=FS_SMALL, backing=False)
    geo = 1.0 + geo_altitude() / R_EARTH
    for side in (1, -1):
        point(ax, (side * geo, 0.0), kind="open", ms=7)
    # names on the left side, inside the shapes; the gap named by a word set in it
    text(ax, (-0.5 * (inner[0] + inner[1]), 0.0), "inner\nbelt", backing=False)
    text(ax, (-0.5 * (outer[0] + outer[1]), 0.62), "outer\nbelt", backing=False)
    text(ax, (-0.5 * (inner[1] + outer[0]), 0.0), "gap", rotation=90, fs=FS_SMALL, backing=False)
    # on the right: the field line, named where it passes between Earth and the horn of the outer
    # belt (the only way in: a leader to the line farther out would cross the outer belt), with the
    # leader about 4.5 pt clear of the horn tip and of Earth
    lam_t = math.radians(55.0)
    r_t = L_gap * math.cos(lam_t) ** 2
    tgt = (r_t * math.cos(lam_t), r_t * math.sin(lam_t))
    callout(ax, tgt, "magnetic field line\n(in the gap)", at=(-0.2, 3.75), fs=FS_SMALL, ha="center", gap=0.0)
    ax.plot(*tgt, "o", ms=2.6, color=INK, zorder=5)                     # the leader ends on the line it names
    callout(ax, (geo, 0.0), "geostationary orbit\n(seen edge-on)", at=(geo + 0.3, -3.75), fs=FS_SMALL, ha="center")
    dimension(ax, (-7.8, -4.2), (-6.8, -4.2), None)
    text(ax, (-6.8, -4.2), f"Earth radius, {fmt(R_EARTH)} km", direction=0, dist=10)
    assert outer[0] < geo < outer[1] and inner[1] < outer[0] < L_gap * 1.0 + 1.0, (inner, outer, geo)
    assert inner[1] < L_gap < outer[0], "the drawn field line lies in the gap"
    trim_canvas(fig)
    save_figure(fig, "p12-radiation-belts")


# ===================================================================== 5. the solar cycle
def solar_cycle():
    """Lesson: the Sun's activity, measured by the F10.7 radio flux, rises and falls in a cycle
    of about 11 years, and every maximum differs from the last."""
    t, f = f107_monthly()
    s = smooth13(f)
    tm, sm = cycle_maxima(t, s)
    fig, ax = data_axes(6.5, 3.3)
    ax.plot(t, f, color="#8A8A8A", lw=0.8, zorder=2)
    ok = ~np.isnan(s)
    ax.plot(t[ok], s[ok], **line_kw(0), zorder=3)
    ax.plot(tm, sm, "o", ms=6, mfc="white", mec=INK, mew=1.4, zorder=4)
    ax.set_xlim(1945, 2030)
    ax.set_ylim(0, 400)
    ax.set_yticks(range(0, 401, 50))
    ax.set_xticks(range(1950, 2031, 10))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.set_xlabel("Year")
    ax.set_ylabel("Solar radio flux F10.7, sfu")
    fig.canvas.draw()
    period = float(np.mean(np.diff(tm)))
    i_sp = int(np.argmax(np.where((t > 1990.5) & (t < 1992.0), f, -1.0)))      # a monthly spike of 1991
    callout(ax, (t[i_sp], f[i_sp] + 3.0), "monthly mean", at=(2001.5, 292.0), fs=FS_SMALL, color="#555555",
            ha="center")
    callout(ax, (1964.8, 74.0), "13-month running mean", at=(1966.5, 28.0), fs=FS_SMALL, ha="left")
    yd = 345.0
    dimension(ax, (tm[0], yd), (tm[-1], yd), None)
    for tt_, ss_ in zip((tm[0], tm[-1]), (sm[0], sm[-1])):
        ax.plot([tt_, tt_], [ss_ + 12.0, yd], color=GRAY, lw=0.7, ls=(0, (2, 2)), zorder=2)
    n_cyc = len(tm) - 1
    text(ax, (0.5 * (tm[0] + tm[-1]), yd), f"{n_cyc} cycles in {fmt(tm[-1] - tm[0], 3)} years: "
         f"{fmt(period, 3)} years each", direction=90, dist=5, fs=FS_SMALL)
    assert 9.5 < period < 12.5 and len(tm) >= 6, (period, tm)
    save_figure(fig, "p12-solar-cycle")


# ===================================================================== 8. the launch timeline
def launch_timeline():
    """Lesson: walking the mission event by event shows where one failure ends the mission: the
    separations and the single second-stage engine are single-point failures."""
    fig, ax = new_axes(6.5, 2.9)
    fig.subplots_adjust(0, 0, 1, 1)
    set_frame(ax, -0.1, 14.3, -2.4, 3.3)
    W, gap = 1.95, 0.5
    names = [p_[1] for p_ in PHASES]
    bs = row(ax, names, 0.4, 0.0, W, gap=gap / pt(ax, 1.0), fs=FS_SMALL, keep_breaks=True,
             fills=[BOX_FILL_START] + [None] * 4 + [BOX_FILL_START])
    for a_, b_ in zip(bs[:-1], bs[1:]):
        route(ax, a_, "right", b_, "left")
    top = bs[0].cy + bs[0].h / 2
    bot = bs[0].cy - bs[0].h / 2
    for (n, _, tt), b_ in zip(PHASES, bs):
        key_disc(ax, (b_.cx, top + pt(ax, 14)), n, r=9.0)
        text(ax, (b_.cx, bot), tt, direction=-90, dist=5, fs=FS_SMALL, backing=False)
        if n in SPF_PHASES:
            ax.plot(b_.cx, bot - pt(ax, 34), "D", ms=9, mfc=INK, mec=INK, zorder=5)
    yb = top + pt(ax, 30)
    brace(ax, (bs[0].cx - W / 2, yb), (bs[0].cx + W / 2, yb), None, side=1)
    text(ax, (bs[0].cx - W / 2, yb + pt(ax, 9)), "hazards of the lower\natmosphere: winds aloft,\ntriggered lightning",
         ha="left", va="bottom", fs=FS_SMALL, backing=False)
    yk = bot - pt(ax, 60)
    ax.plot(0.2, yk, "D", ms=9, mfc=INK, mec=INK, zorder=5)
    text(ax, (0.2, yk), "single-point failure", direction=0, dist=9, fs=FS_SMALL)
    w_lab = text_size(ax, "atmosphere: winds aloft,", FS_SMALL)[0]
    assert w_lab < 2 * W + gap, "the hazard note is no wider than about two events"
    assert len(bs) == 6 and len(SPF_PHASES) == 4
    trim_canvas(fig)
    save_figure(fig, "p12-launch-timeline")


# ===================================================================== 9. single string and redundant pair
def redundancy():
    """Lesson: two independent units in parallel fail only if both fail, so the chance of losing
    the function falls from p to p squared."""
    fig, ax = new_axes(6.5, 2.1)
    fig.subplots_adjust(0, 0, 1, 1)
    set_frame(ax, -0.2, 13.2, -1.75, 2.4)
    pf = 1.0 - R_UNIT
    W = 2.4

    def node(xy, name):
        ax.plot(*xy, "o", ms=6, color=INK, zorder=5)
        text(ax, xy, name, direction=90, dist=6, fs=FS_SMALL, backing=False)

    # (a) single string
    ax.text(-0.2, 2.3, "(a) Single string", ha="left", va="top", fontsize=FS_LABEL, fontweight="bold")
    b = box(ax, (3.0, 0.6), "Flight computer", w=W)
    node((0.5, 0.6), "in")
    node((5.5, 0.6), "out")
    ax.plot([0.5, 3.0 - W / 2], [0.6, 0.6], color=INK, lw=LW_MAIN, zorder=3)
    ax.plot([3.0 + W / 2, 5.5], [0.6, 0.6], color=INK, lw=LW_MAIN, zorder=3)
    text(ax, (3.0, -0.95), f"fails: $p$ = {fmt(pf, 2)}\nworks: 1 − $p$ = {fmt(R_UNIT, 2)}", fs=FS_SMALL,
         backing=False, linespacing=1.4)
    # (b) redundant pair
    x0 = 7.2
    ax.text(x0 - 0.3, 2.3, "(b) Redundant pair", ha="left", va="top", fontsize=FS_LABEL, fontweight="bold")
    xc = x0 + 2.9
    ba = box(ax, (xc, 1.05), "Computer A", w=W)
    bb = box(ax, (xc, 0.15), "Computer B", w=W)
    xl, xr = x0 + 0.5, x0 + 5.3
    node((x0 - 0.05, 0.6), "in")
    node((xr + 0.55, 0.6), "out")
    ax.plot([x0 - 0.05, xl, xl], [0.6, 0.6, 1.05], color=INK, lw=LW_MAIN, zorder=3, solid_joinstyle="miter")
    ax.plot([xl, xl], [0.6, 0.15], color=INK, lw=LW_MAIN, zorder=3)
    ax.plot([xl, xc - W / 2], [1.05, 1.05], color=INK, lw=LW_MAIN, zorder=3)
    ax.plot([xl, xc - W / 2], [0.15, 0.15], color=INK, lw=LW_MAIN, zorder=3)
    ax.plot([xc + W / 2, xr], [1.05, 1.05], color=INK, lw=LW_MAIN, zorder=3)
    ax.plot([xc + W / 2, xr], [0.15, 0.15], color=INK, lw=LW_MAIN, zorder=3)
    ax.plot([xr, xr], [0.15, 1.05], color=INK, lw=LW_MAIN, zorder=3)
    ax.plot([xr, xr + 0.55], [0.6, 0.6], color=INK, lw=LW_MAIN, zorder=3)
    p2 = pf ** 2
    text(ax, (xc, -0.95), f"both fail: $p$² = {fmt(pf, 2)} × {fmt(pf, 2)} = {fmt(p2, 2)}\n"
                          f"works: 1 − $p$² = {fmt(1 - p2, 4)}", fs=FS_SMALL, backing=False, linespacing=1.4)
    assert abs((1 - p2) - 0.9991) < 1e-12
    trim_canvas(fig)
    save_figure(fig, "p12-redundancy")


def make_all():
    hazard_anatomy()
    flight_hazards()
    microburst()
    space_altitudes()
    radiation_belts()
    solar_cycle()
    risk_matrix()
    risk_moves()
    launch_timeline()
    redundancy()


def values():
    r = lambda key, txt: record("p12", key, txt)                                 # noqa: E731
    # ---- hazards in the atmosphere
    r("bird-ft", fmt(BIRD_FT))
    r("bird-m", fmt(BIRD_FT * FT, 3))
    r("ice-h0", fmt(t_alt(273.15 + ICE_T_TOP_C)))
    r("ice-h1", fmt(t_alt(273.15 + ICE_T_BOT_C)))
    r("jet-lo-km", fmt(JET_FL[0] * 100 * FT / 1000.0, 2))
    r("jet-hi-km", fmt(JET_FL[1] * 100 * FT / 1000.0, 3))
    r("jet-lo-ft", fmt(JET_FL[0] * 100))
    r("jet-hi-ft", fmt(JET_FL[1] * 100))
    r("knot-ms", fmt(NMI / 3600.0, 3))
    r("microburst-fpm", fmt(MICROBURST_DOWN_FPM))
    r("microburst-kt", f"{MICROBURST_WIND_KT:.0f}")
    r("microburst-shear-kt", f"{MICROBURST_SHEAR_KT:.0f}")
    close_to(MICROBURST_SHEAR_KT, 2.0 * MICROBURST_WIND_KT, 1e-12, "headwind to tailwind: twice the outflow")
    r("srp-km", fmt(SRP_DOMINANT_KM))
    # ---- hot and high: the example airport
    T_std, p_std, rho_std = standard(AIRPORT_H)
    T_day = 273.15 + AIRPORT_T_C
    dT = T_day - T_std
    T_h, p_h, rho_h = nonstandard(AIRPORT_H, dT)
    close_to(T_h, T_day, 1e-9, "hot-day temperature at the airport")
    r("apt-h", fmt(AIRPORT_H))
    r("apt-tc", fmt(AIRPORT_T_C, 2))
    r("apt-rho-std", fmt(rho_std))
    r("apt-rho-hot", fmt(rho_h))
    r("apt-rho-sl", fmt(RHO_SL, 5))
    r("apt-loss-pct", fmt(100.0 * (1.0 - rho_h / RHO_SL), 2))
    r("apt-loss-std-pct", fmt(100.0 * (1.0 - rho_std / RHO_SL), 2))
    r("apt-dens-alt", fmt(altitude_from_density(rho_h)))
    # ---- hazards in space
    r("inner-lo", fmt(round(INNER_MI[0] * MILE_KM, -2)))
    r("inner-hi", fmt(round(INNER_MI[1] * MILE_KM, -2)))
    r("outer-lo", fmt(round(OUTER_MI[0] * MILE_KM, -2)))
    r("outer-hi", fmt(round(OUTER_MI[1] * MILE_KM, -2)))
    r("ao-lo", fmt(AO_KM[0], 3))
    r("ao-hi", fmt(AO_KM[1], 3))
    r("debris-km", fmt(DEBRIS_KM))
    r("drag-km", fmt(DRAG_YEARS_KM, 3))
    r("hubble-km", fmt(HUBBLE_KM, 3))
    r("geo-km", fmt(geo_altitude()))
    r("re-km", fmt(R_EARTH))
    # ---- the solar cycle
    t, f = f107_monthly()
    sm_ = smooth13(f)
    tm, smax = cycle_maxima(t, sm_)
    r("f107-first", f"{int(t[0])}")
    r("f107-ncyc", f"{len(tm) - 1}")
    r("f107-span", fmt(tm[-1] - tm[0], 3))
    r("f107-period", fmt(float(np.mean(np.diff(tm))), 3))
    r("f107-min", fmt(float(np.nanmin(sm_)), 2))
    r("f107-maxlo", fmt(float(np.min(smax)), 3))
    r("f107-maxhi", fmt(float(np.max(smax)), 3))
    r("f107-spacing-lo", fmt(float(np.min(np.diff(tm))), 2))
    r("f107-spacing-hi", fmt(float(np.max(np.diff(tm))), 3))
    # ---- the risk matrix and the worked example
    counts = {lv: sum(level(L, C) == lv for L in range(1, 6) for C in range(1, 6)) for lv in ("High", "Medium", "Low")}
    for lv, n in counts.items():
        r(f"cells-{lv.lower()}", f"{n}")
    for rid, _, b, a in RISKS:
        r(f"{rid}-before", f"{b[0] * b[1]}")
        r(f"{rid}-after", f"{a[0] * a[1]}")
    # ---- redundancy
    pf = 1.0 - R_UNIT
    r("rel-unit", fmt(R_UNIT, 2))
    r("rel-pf", fmt(pf, 2))
    r("rel-pf2", fmt(pf * pf, 2))
    r("rel-pair", fmt(1.0 - pf * pf, 4))
    r("rel-ratio", fmt(1.0 / pf, 3))
    # ---- values quoted from the sources (constants of the page, each cited on it)
    quoted = {
        "src-bird-pct": ("90", "percent of reported strikes at or below 3,000 ft, AIM 7-5-1"),
        "src-debris-cm": ("10", "cm, tracking limit, NASA ODPO"),
        "src-debris-v": ("15", "km/s maximum relative speed, NASA ODPO"),
        "src-iss": ("10,000", "1 in 10,000 maneuver threshold, NASA ODPO"),
        "src-saa-min": ("25", "20 to 25 minutes per pass, STScI"),
        "src-f107-cm": ("10.7", "cm, NOAA SWPC"),
        "src-charging": ("100", "100 to 1 over the cycle, NASA-HDBK-4002B"),
        "src-apollo-1": ("36.5", "s, NASA SP-4029"),
        "src-apollo-2": ("52", "s, NASA SP-4029"),
        "src-ariane-s": ("37", "seconds, ESA Inquiry Board"),
        "src-ariane-breakup": ("3", "seconds later: broke up at about 40 s, ESA Inquiry Board"),
    }
    for key, (txt, _source) in quoted.items():
        r(key, txt)
