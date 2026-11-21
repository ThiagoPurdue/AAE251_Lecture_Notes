"""Figures and values of the page "Concept generation and trade studies"
(notes/chapter-1/concepts-and-trade-studies.md). No standard is assessed on this page.

One function per figure, make_all() for the runner, and values() for every number the page
prints. Run through the runner from the book folder:

    FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_1_figures.py p17

The worked example is an uncrewed island cargo aircraft: the combination table, the weights,
the scores and the three concepts are given; every total, the rescaled totals and the weight at which the winner changes are
computed here. Helpers that the shared code lacks are defined here, prefixed with "_".
"""
from chapter_1.common import *

P = "p17"

# ---------------------------------------------------------------- the example
# Concept combination table: function -> three options, in a fixed order
FUNCTIONS = [
    ("Make lift", ["Fixed wing", "Rotor", "Wing plus lift rotors"]),
    ("Make thrust", ["Piston engine", "Turboprop", "Electric motors"]),
    ("Take off", ["Runway", "Short strip", "Vertical"]),
    ("Carry cargo", ["Inside fuselage", "Pod under wing", "Sling load"]),
]
# The three concepts: one option (column index) per function, and their names
CONCEPTS = {
    "A": dict(name="twin piston, conventional", short="twin piston", path=(0, 0, 0, 0)),
    "B": dict(name="single turboprop, conventional", short="single turboprop", path=(0, 1, 0, 0)),
    "C": dict(name="electric lift-plus-cruise VTOL", short="electric VTOL", path=(2, 2, 2, 0)),
}
# Criteria: name, short name for figures, weight (set before scoring), scores of A, B, C (1 to 5, 5 best)
CRITERIA = [
    ("Payload and range", "payload and range", 0.30, (3, 5, 2)),
    ("Operating cost", "operating cost", 0.25, (4, 3, 3)),
    ("Runway length needed", "runway length needed", 0.20, (2, 2, 5)),
    ("Technical risk", "technical risk", 0.15, (5, 4, 2)),
    ("Noise near villages", "noise near villages", 0.10, (2, 2, 4)),
]
NAMES = ("A", "B", "C")
K_RUNWAY = 2                    # index of the criterion whose weight the sensitivity check changes
W_CHECK = 0.35                  # the check of the page: the runway weight raised to 0.35
SEG_FILLS = [GOLD, "#FFFFFF", "#D9D9D9", "#9E9E9E", "#EDEDED"]   # stacked segments: payload and range in gold
                                                                # (the criterion that decides), the rest in grays
CONCEPT_ROLE = {"A": 0, "B": 1, "C": 2}   # data series of the sensitivity plot: black solid, blue dashed, vermilion dotted


# ---------------------------------------------------------------- the arithmetic
def weights():
    return np.array([c[2] for c in CRITERIA])


def scores():
    """Array [criterion, concept] of the scores."""
    return np.array([c[3] for c in CRITERIA], dtype=float)


def totals(w=None):
    """Weighted total of each concept: sum over criteria of weight times score."""
    w = weights() if w is None else np.asarray(w, float)
    close_to(float(w.sum()), 1.0, 1e-12, "weights add up to 1")
    return w @ scores()


def rescaled_weights(w_k, k=K_RUNWAY):
    """Set the weight of criterion k to w_k and scale every other weight by the same factor
    (1 - w_k)/(1 - w_k0), so that the weights still add up to 1."""
    w0 = weights()
    f = (1.0 - w_k) / (1.0 - w0[k])
    w = w0 * f
    w[k] = w_k
    return w


def total_vs_weight(w_k, j, k=K_RUNWAY):
    """Total of concept j when criterion k has weight w_k (others rescaled): a straight line in w_k."""
    w0, s = weights(), scores()
    rest = float(totals()[j] - w0[k] * s[k, j])
    return w_k * s[k, j] + (1.0 - w_k) / (1.0 - w0[k]) * rest


def crossover(j1, j2, k=K_RUNWAY):
    """The weight of criterion k at which concepts j1 and j2 have equal totals (others rescaled)."""
    w0, s, T = weights(), scores(), totals()
    r1, r2 = T[j1] - w0[k] * s[k, j1], T[j2] - w0[k] * s[k, j2]
    return float((r1 - r2) / ((1.0 - w0[k]) * (s[k, j2] - s[k, j1]) + (r1 - r2)))


# ---------------------------------------------------------------- figures
def trade_study_steps():
    """The order of a trade study: concepts first, weights before scores, a check, a record."""
    steps = ["Generate concepts: one option per function",
             "Pick the criteria from the requirements",
             "Set the weights before scoring; they add up to 1",
             "Score each concept from 1 to 5",
             "Add up weight × score for each concept",
             "Change the weights and watch the winner",
             "Record the decision in the log"]
    fig, ax = canvas(6.5, 4.15)                   # data units are inches
    W, cx = 3.75, 2.55
    fills = [BOX_FILL_START] + [None] * 5 + [BOX_FILL_START]
    bx = column(ax, steps, cx, 4.05, W, gap=16.0, fills=fills)
    for i, b in enumerate(bx):
        step_marker(ax, None, i + 1, beside=b)
    for a, b in zip(bx[:-1], bx[1:]):
        route(ax, a, "bottom", b, "top")
    xr = cx + W / 2 + pt(ax, 7.0)
    groups = [(1, 5, "decision matrix")]                  # one brace: the steps of the matrix
    for i0, i1, name in groups:
        top = bx[i0].cy + bx[i0].h / 2
        bot = bx[i1].cy - bx[i1].h / 2
        brace(ax, (xr, top), (xr, bot), name, side=1)
    ys = [b.cy for b in bx]
    assert len(bx) == 7 and all(y0 > y1 for y0, y1 in zip(ys[:-1], ys[1:])), "seven steps, top to bottom"
    assert bx[-1].cy - bx[-1].h / 2 > 0.0, "the column fits its frame"
    assert all("\n" not in b.text.get_text() for b in bx), "each step on one line"
    trim_canvas(fig)                                       # one even margin round the drawing
    save_figure(fig, "p17-trade-study-steps")


def combination_table():
    """A concept is one option per function: concept C traced through the combination table."""
    H = 3.75
    fig, ax = canvas(6.5, H)                        # data units are inches
    xs_fun, w_fun = 0.72, 1.34
    xs_opt, w_opt = [2.27, 3.92, 5.57], 1.55
    texts = [f for f, _ in FUNCTIONS] + [o for _, opts in FUNCTIONS for o in opts]
    h = max(box_height(ax, t, w_opt) for t in texts)
    gap = pt(ax, 24.0)
    top = H - 0.3
    path = CONCEPTS["C"]["path"]
    cells = {}
    for r, (fun, opts) in enumerate(FUNCTIONS):
        cy = top - h / 2 - r * (h + gap)
        box(ax, (xs_fun, cy), fun, w=w_fun, h=h, bold=True, rounded=False)
        for c, opt in enumerate(opts):
            on = path[r] == c
            cells[(r, c)] = box(ax, (xs_opt[c], cy), opt, w=w_opt, h=h, rounded=False,
                                fill=HIGHLIGHT if on else BOX_FILL, bold=on, lw=2.0 if on else LW_BOX)
    for x, s in [(xs_fun, "Function")] + [(x, f"Option {i + 1}") for i, x in enumerate(xs_opt)]:
        text(ax, (x, top), s, direction=90, dist=5, fs=FS_LABEL, fontweight="bold")
    # the trace of concept C, from the first function to the last
    for r in range(len(FUNCTIONS) - 1):
        a, b = cells[(r, path[r])], cells[(r + 1, path[r + 1])]
        if path[r] == path[r + 1]:
            route(ax, a, "bottom", b, "top")
        else:
            y_mid = a.cy - h / 2 - gap / 2
            route(ax, a, "bottom", b, "top", via=[("y", y_mid)])
    # key under the table
    y_key = top - 4 * h - 3 * gap - pt(ax, 22.0)
    sw = box(ax, (xs_opt[0] - w_opt / 2 + 0.25, y_key), "", w=0.5, h=pt(ax, 14.0), fill=HIGHLIGHT, rounded=False,
             lw=2.0)
    text(ax, (sw.cx + sw.w / 2, y_key), "concept C, electric lift-plus-cruise VTOL: one option for each function",
         direction=0, dist=6, fs=FS_SMALL, backing=False)
    n_comb = int(np.prod([len(o) for _, o in FUNCTIONS]))
    traced = [cells[(r, path[r])].text.get_text().replace("\n", " ") for r in range(len(FUNCTIONS))]
    assert traced == [FUNCTIONS[r][1][path[r]] for r in range(4)], traced
    assert n_comb == 81 and len(set(r for r, _ in cells)) == 4, "four functions, 81 combinations"
    assert y_key - pt(ax, 7.0) > 0.0, "the key fits the frame"
    save_figure(fig, "p17-combination-table")


def weighted_totals():
    """Stacked weighted scores: B wins on payload and range, the heaviest criterion."""
    w, s = weights(), scores()
    contrib = w[:, None] * s                       # [criterion, concept]
    T = totals()
    fig, ax = data_axes(6.5, 5.0, grid=False)
    ax.yaxis.grid(True, color=GRID, lw=0.6)
    x = np.arange(3)
    bw = 0.56
    bottoms = np.zeros(3)
    tops = []
    for i, (name, short, wi, _) in enumerate(CRITERIA):
        bars_ = ax.bar(x, contrib[i], bw, bottom=bottoms, color=SEG_FILLS[i], edgecolor=INK, lw=1.0, zorder=3)
        for j in range(3):                         # each segment carries its weight x score
            text(ax, (x[j], bottoms[j] + contrib[i, j] / 2), fmt_dec(contrib[i, j], 2), fs=FS_SMALL,
                 backing=False, zorder=6)
        bottoms = bottoms + contrib[i]
        tops.append(bars_)
    tops[0].patches[1].set_linewidth(2.4)              # B's payload-and-range segment, the one that decides
    tops[0].patches[1].set_zorder(4)
    ax.set_xlim(-0.5, 3.6)
    ax.set_ylim(0, 3.8)
    ax.set_yticks([0, 1, 2, 3])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xticks(x, [f"{n}\n{CONCEPTS[n]['short']}" for n in NAMES])
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Weighted total, sum of weight × score")
    jb = int(np.argmax(T))
    for j in range(3):
        lab = "total " + fmt_dec(T[j], 2) + (", highest" if j == jb else "")
        text(ax, (x[j], T[j]), lab, direction=90, dist=4, fs=FS_SMALL, backing=False,
             fontweight="bold" if j == jb else "normal")
    # criterion names beside the segments of bar C (every bar stacks them in the same order)
    cum = np.r_[0.0, np.cumsum(contrib[:, 2])]
    for i, (_, short, wi, _) in enumerate(CRITERIA):
        ymid = 0.5 * (cum[i] + cum[i + 1])
        text(ax, (x[2] + bw / 2, ymid), f"{short}, weight {fmt_dec(wi, 2)}", direction=0, dist=7, fs=FS_SMALL)
    for j in range(3):
        drawn = sum(b.patches[j].get_height() for b in tops)
        close_to(drawn, float(T[j]), 1e-12, f"bar {NAMES[j]} height is its weighted total")
    assert jb == 1, "B has the highest total"
    assert tops[0].patches[1].get_facecolor()[:3] != tops[1].patches[1].get_facecolor()[:3], "payload stands out"
    assert tops[0].patches[1].get_height() == max(b.patches[j].get_height() for b in tops for j in range(3)), \
        "B's payload-and-range segment is the largest of the chart"
    save_figure(fig, "p17-weighted-totals")


def weight_sensitivity():
    """The totals against the runway weight: C overtakes B at 0.294."""
    wk = np.linspace(0.0, 0.6, 241)
    w0 = weights()[K_RUNWAY]
    ws = crossover(1, 2)
    fig, ax = data_axes(6.5, 4.4)
    lines = {}
    for j, n in enumerate(NAMES):
        y = np.array([total_vs_weight(v, j) for v in wk])
        lines[n] = ax.plot(wk, y, **line_kw(CONCEPT_ROLE[n]), zorder=4)[0]
    ax.set_xlim(0.0, 0.6)
    ax.set_ylim(2.4, 4.2)
    ax.set_xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}"))
    ax.set_yticks([2.5, 3.0, 3.5, 4.0])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}"))
    ax.set_xlabel("New weight of the runway criterion, $w_k$′")
    ax.set_ylabel("Weighted total")
    # the weight set before scoring and the check: a dashed line from a label at the bottom
    # up to the highest of the three marked points
    for v, lab in ((w0, f"weight set\nfirst, {fmt_dec(w0, 2)}"), (W_CHECK, f"check,\n{fmt_dec(W_CHECK, 2)}")):
        top = max(total_vs_weight(v, j) for j in range(3))
        ax.plot([v, v], [2.72, top], **line_kw("boundary"), zorder=2)
        text(ax, (v, 2.72), lab, direction=-90, dist=3, fs=FS_SMALL, backing=False)
        for j, n in enumerate(NAMES):
            point(ax, (v, total_vs_weight(v, j)), None, ms=6.5, color=line_kw(CONCEPT_ROLE[n])["color"], zorder=6)
    # the crossover, labeled in the free wedge above it
    yc = total_vs_weight(ws, 1)
    point(ax, (ws, yc), None, kind="open", ms=9.0, zorder=7)
    callout(ax, (ws, yc), f"tie: $w_k$* = {fmt(ws)};\nthe winner changes", at=(ws, 3.86), gap=6, fs=FS_SMALL,
            ha="center")
    # values of the leader at each marked weight
    text(ax, (w0, float(totals()[1])), fmt_dec(float(totals()[1]), 2), direction=62, dist=7, fs=FS_SMALL,
         color=text_color(1))
    text(ax, (W_CHECK, total_vs_weight(W_CHECK, 2)), fmt(total_vs_weight(W_CHECK, 2)), direction=-30, dist=7,
         fs=FS_SMALL, color=text_color(2))
    # direct curve labels, each beside its own line where the space is free
    text(ax, (0.02, 3.93), "B, single turboprop", ha="left", va="center", fs=FS_SMALL, color=text_color(1))
    text(ax, (0.02, 3.27), "A, twin piston", ha="left", va="center", fs=FS_SMALL, color=text_color(0))
    text(ax, (0.455, 3.50), "C, electric VTOL", ha="left", va="center", fs=FS_SMALL, color=text_color(2))
    # assert on the drawn lines: B above C left of the crossover, C above B right of it
    yb, ycl = lines["B"].get_ydata(), lines["C"].get_ydata()
    i = int(np.searchsorted(wk, ws))
    assert yb[i - 1] > ycl[i - 1] and yb[i + 1] < ycl[i + 1], "the B and C lines cross at the computed weight"
    close_to(float(np.interp(W_CHECK, wk, ycl)), total_vs_weight(W_CHECK, 2), 1e-9, "C at the check weight")
    close_to(float(np.interp(w0, wk, yb)), float(totals()[1]), 1e-9, "B at the weight set first")
    save_figure(fig, "p17-weight-sensitivity")


def make_all():
    trade_study_steps()
    combination_table()
    weighted_totals()
    weight_sensitivity()


# ---------------------------------------------------------------- printed values
def values():
    w, s, T = weights(), scores(), totals()
    close_to(float(T[0]), 3.25, 1e-12, "total A")
    close_to(float(T[1]), 3.45, 1e-12, "total B")
    close_to(float(T[2]), 3.05, 1e-12, "total C")
    record(P, "n-comb", str(int(np.prod([len(o) for _, o in FUNCTIONS]))))
    for i, (name, short, wi, sc) in enumerate(CRITERIA):
        record(P, f"w{i}", fmt_dec(wi, 2))
        for j, n in enumerate(NAMES):
            record(P, f"ws-{i}-{n}", fmt_dec(wi * sc[j], 2))
    for j, n in enumerate(NAMES):
        record(P, f"T-{n}", fmt_dec(float(T[j]), 2))
    record(P, "gap-BA", fmt_dec(float(T[1] - T[0]), 2))
    record(P, "gap-BC", fmt_dec(float(T[1] - T[2]), 2))
    # one score step on operating cost (weight 0.25): B's score 3 -> 2
    k_cost = 1
    record(P, "B-cost-down", fmt_dec(float(T[1] - w[k_cost]), 2))
    assert T[1] - w[k_cost] < T[0], "one step on B's cost score puts A ahead"
    # sensitivity: runway weight 0.20 -> 0.35, the others scaled by f
    k, w0 = K_RUNWAY, w[K_RUNWAY]
    f = (1.0 - W_CHECK) / (1.0 - w0)
    record(P, "w-check", fmt_dec(W_CHECK, 2))
    record(P, "f", fmt(f))
    record(P, "one-minus-wcheck", fmt_dec(1.0 - W_CHECK, 2))
    record(P, "one-minus-w0", fmt_dec(1.0 - w0, 2))
    record(P, "sum-check", fmt(W_CHECK + float(fmt(f)) * (1.0 - w0)))
    close_to(float(rescaled_weights(W_CHECK).sum()), 1.0, 1e-12, "rescaled weights add up to 1")
    for j, n in enumerate(NAMES):
        rest = float(T[j] - w0 * s[k, j])
        record(P, f"rest-{n}", fmt_dec(rest, 2))
        record(P, f"runway-part-{n}", fmt_dec(w0 * s[k, j], 2))
        frest = float(fmt(f)) * float(fmt_dec(rest, 2))
        record(P, f"frest-{n}", fmt(frest))
        record(P, f"wcheck-s-{n}", fmt_dec(W_CHECK * s[k, j], 2))
        tnew = total_vs_weight(W_CHECK, j)
        close_to(tnew, float(rescaled_weights(W_CHECK) @ s[:, j]), 1e-12, "line form = rescaled weights")
        record(P, f"Tcheck-{n}", fmt(tnew))
    # the weight at which C overtakes B
    ws = crossover(1, 2)
    rB, rC = float(T[1] - w0 * s[k, 1]), float(T[2] - w0 * s[k, 2])
    record(P, "dR", fmt_dec(rB - rC, 2))
    record(P, "den-part", fmt_dec((1.0 - w0) * (s[k, 2] - s[k, 1]), 2))     # 0.80 x 3 = 2.40, the w term
    record(P, "den", fmt_dec((1.0 - w0) * (s[k, 2] - s[k, 1]) + (rB - rC), 2))
    record(P, "ws", fmt(ws))
    record(P, "T-at-ws", fmt(total_vs_weight(ws, 1)))
    close_to(total_vs_weight(ws, 1), total_vs_weight(ws, 2), 1e-12, "B and C equal at the crossover")
    record(P, "dw", fmt(ws - w0, 2))
    # A never overtakes B: same runway score, smaller rest
    assert all(total_vs_weight(v, 0) < total_vs_weight(v, 1) for v in np.linspace(0.0, 0.95, 96))   # equal only at w = 1, where the runway is all that counts
