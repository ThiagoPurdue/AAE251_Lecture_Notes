"""Figures and values of 1.1 Needs and Requirements (notes/chapter-1/needs-and-requirements.md).

The running example of the page is an aerial survey aircraft: three stakeholders rate five
needs; the
requirements, their values and the compliance table are written for these notes. The other
examples are a Boeing 737-800 (system boundary; Boeing D6-58325-7 Rev C), a Boeing 787
(stakeholders), an airliner range requirement (Boston to Los Angeles, FAA airport reference
points) and a main landing gear (14 CFR 25.473; FAA-H-8083-31B, Chapter 13).
"""
import math

from chapter_1.common import *
from matplotlib.patches import FancyBboxPatch, Polygon
from chapter_1 import diagrams as D

TAG = "p11"

# ===================================================================== data of the page (not constants)
# The survey aircraft: three stakeholders rate five needs from 1 (nice to have) to 5 (must have).
# The owner is the customer who buys the aircraft,
# so a tie in the average goes to the need the owner rates higher (the page states this rule).
NEEDS = [
    ("N1", "The aircraft stays over the survey area for a full working day."),
    ("N2", "The camera images are sharp in light turbulence."),
    ("N3", "The aircraft can use short rural airstrips."),
    ("N4", "The aircraft can be prepared and flown on a survey by one pilot without help."),
    ("N5", "The operating cost per survey hour is low."),
]
RATERS = ["Owner", "Pilot", "Data customer"]
RATINGS = {"N1": (5, 4, 5), "N2": (4, 3, 5), "N3": (3, 4, 2), "N4": (4, 5, 2), "N5": (5, 3, 4)}
PAYER = 0                                   # index of the owner in RATERS: breaks ties

# The survey aircraft's requirements: (id, need it traces to, metric, value, reason, method, where, status)
REQS = [
    ("R1", "N1", "Endurance with the survey camera and full fuel", "at least 6 h",
     "A survey day is about 5 h over the area plus the flights to and from it", "Analysis",
     "Endurance calculation", "Meets"),
    ("R2", "N2", "Image smear at survey speed in light turbulence", "at most 0.5 pixel",
     "The data customer's maps need edges sharp to one pixel", "Test",
     "Flight over a ground target in light turbulence", "Not yet shown"),
    ("R3", "N3", "Takeoff distance from a dry grass strip at maximum weight", "at most 600 m",
     "The rural strips the owner uses are 600 m long or longer", "Analysis",
     "Takeoff distance calculation", "Not yet shown"),
    ("R4", "N4", "Crew needed to fly a survey line and run the camera", "at most one pilot",
     "The owner pays for one crew seat per flight", "Inspection now, demonstration later",
     "Cockpit drawing: camera controls within the pilot's reach; then a pilot flies a survey line in a "
     "cockpit mock-up", "Partly shown"),
    ("R5", "N4", "Time for one person to install and secure the camera", "at most 15 min",
     "The pilot loads the camera alone before the first flight of the day", "Demonstration",
     "Trial with a full-size mock-up of the camera bay", "Not yet shown"),
    ("R6", "N5", "Direct operating cost per survey hour", "at most 80% of the owner's present aircraft",
     "Survey prices are set by competitors; the owner needs a lower cost to earn more", "Analysis",
     "Operating cost estimate", "Not yet shown"),
]

# Range requirement of an airliner: the airport reference points of Boston and Los Angeles
# (AIRPORTS, constants.py)
BOS, LAX = AIRPORTS["BOS"], AIRPORTS["LAX"]
RANGE_REQ_NMI = 3000.0                      # the value the example requirement states (a choice)
RANGE_WRONG_NMI = 6000.0                    # a value that the Boston to Los Angeles reason cannot support
QUALIFY_H = 200.0                           # "average time for a pilot to qualify", a requirement example
ENGINE_CHANGE_H = 8.0                       # "time to change one engine", a requirement example
SURVEY_DAY_H = 5.0                          # hours over the area in a survey day (R1's reason)

# Main landing gear: limit descent velocity at the design landing weight (constants.py)
SINK_RATE_FPS = LIMIT_SINK_RATE_FPS


def ranking():
    """Average rating of each need and its rank; ties broken by the payer's rating.
    Returns a list of dicts in N1..N5 order with avg and rank."""
    rows = []
    for nid, _ in NEEDS:
        r = RATINGS[nid]
        rows.append(dict(id=nid, ratings=r, avg=sum(r) / len(r)))
    order = sorted(rows, key=lambda d: (-round(d["avg"], 9), -d["ratings"][PAYER]))
    for k, d in enumerate(order, start=1):
        d["rank"] = k
    return rows


def trace_problems(needs, reqs, links):
    """Needs with no requirement and requirements with no need (the two checks of a
    traceability matrix). links: set of (need, req)."""
    lone_needs = [n for n in needs if not any((n, r) in links for r in reqs)]
    lone_reqs = [r for r in reqs if not any((n, r) in links for n in needs)]
    return lone_needs, lone_reqs


# ===================================================================== figures
PT = 1.0 / 72.0                             # one point, in the inch units of the diagram canvases


def _canvas(w, h):
    """A diagram canvas w x h inches whose data units are inches (diagrams.canvas)."""
    return D.canvas(w, h)


def _tw(ax, s, fs=FS_LABEL, weight="normal"):
    """Width and height (inches) of the text s at fs points."""
    return D.text_size(ax, s, fs, weight)


def road_map():
    """The six steps from stakeholders to verified requirements, numbered as the page's
    sections; a brace groups the stakeholders' side and the engineer's side."""
    fig, ax = _canvas(6.5, 3.3)
    steps = ["Identify the stakeholders", "Write the mission statement", "Write the need statements",
             "Rank the needs", "Write the requirements\nand trace them to needs",
             "Verify each requirement and\nrecord it in a compliance table"]
    fills = [BOX_FILL_START] + [None] * 4 + [BOX_FILL_START]
    bs = D.column(ax, steps, 2.3, 3.27, 3.4, gap=14.0, fills=fills, keep_breaks=True)
    for i, b in enumerate(bs, start=1):
        D.step_marker(ax, None, i, beside=b)
    for a, b in zip(bs[:-1], bs[1:]):
        D.route(ax, a, "bottom", b, "top")
    x = 4.1
    D.brace(ax, (x, bs[0].cy + bs[0].h / 2), (x, bs[3].cy - bs[3].h / 2), side=-1, depth=8.0)
    D.brace(ax, (x, bs[4].cy + bs[4].h / 2), (x, bs[5].cy - bs[5].h / 2), side=-1, depth=8.0)
    ym1 = 0.5 * (bs[0].cy + bs[3].cy)
    ym2 = 0.5 * (bs[4].cy + bs[5].cy)
    text(ax, (x + 14 * PT, ym1), "Needs: what the\nstakeholders want,\nin their terms", ha="left", va="center",
         fs=FS_LABEL, backing=False)
    text(ax, (x + 14 * PT, ym2), "Requirements: what\nthe system must do,\nin numbers that\ncan be checked",
         ha="left", va="center", fs=FS_LABEL, backing=False)
    assert all(len(ln.split()) > 1 for b in bs for ln in b.text.get_text().split("\n")), "no line of one word"
    assert len(bs) == 6 and all(a.cy > b.cy for a, b in zip(bs[:-1], bs[1:])), "steps in reading order"
    trim_canvas(fig)
    save_figure(fig, "p11-road-map")


# the parts of the 737-800 top view drawn as a plain outline at the size of the boundary figure
_OUTLINE_PARTS = ("wing_L", "wing_R", "winglet_L", "winglet_R", "htail_L", "htail_R", "nacelle_L", "nacelle_R",
                  "fuselage")


def _aircraft_outline(ax, parts, lw=1.0):
    """The Boeing 737-800 seen from above as clean line art for a small figure: the outlines of
    the fuselage, the wings with their winglets, the horizontal tail and the two nacelles, white
    filled and drawn at the detail weight; the fin, seen edge-on from above, as a slender shape on
    the centerline (6% thick). No control-surface lines: at this size they would merge."""
    z = {"wing_L": 2, "wing_R": 2, "winglet_L": 2, "winglet_R": 2, "htail_L": 2, "htail_R": 2,
         "nacelle_L": 3.5, "nacelle_R": 3.5, "fuselage": 3}
    for name in _OUTLINE_PARTS:
        xy = parts[name].xy
        ax.add_patch(opaque(Polygon(xy, closed=True, fc="white", ec=INK, lw=lw, joinstyle="round", zorder=z[name])))
    v = parts["vtail"].xy
    x0, x1 = float(v[:, 0].min()), float(v[:, 0].max())
    xs = np.linspace(x0, x1, 60)
    t = (xs - x0) / (x1 - x0)
    half = 0.5 * 0.06 * (x1 - x0) * (2.969 * np.sqrt(t) - 1.26 * t - 3.516 * t ** 2 + 2.843 * t ** 3 - 1.015 * t ** 4)
    fin = np.r_[np.c_[xs, half], np.c_[xs[::-1], -half[::-1]]]
    ax.add_patch(opaque(Polygon(fin, closed=True, fc="white", ec=INK, lw=0.8, zorder=4)))
    return 2.0 * float(half.max())


def system_boundary():
    """A Boeing 737-800 described four ways: function, inputs and outputs, boundary, form.
    Drawn in meters (the aircraft to scale) as a plain outline sized for the figure."""
    L = B738["length"]
    parts = aircraft_top()                          # seen from above, nose to the left
    X0, X1, Y0, Y1 = -54.0, 100.0, -40.0, 36.0
    w_in = 6.5
    fig, ax = new_axes(w_in, w_in * (Y1 - Y0) / (X1 - X0))
    fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
    D.set_frame(ax, X0, X1, Y0, Y1)
    fin_t = _aircraft_outline(ax, parts)
    bx0, bx1, by0, by1 = -5.0, 45.0, -21.0, 21.0
    bnd = FancyBboxPatch((bx0, by0), bx1 - bx0, by1 - by0, boxstyle="round,pad=0,rounding_size=3",
                         fc="none", ec=INK, lw=1.4, ls=(0, (5.0, 3.0)), zorder=1)
    ax.add_patch(bnd)
    xc = 0.5 * (bx0 + bx1)
    text(ax, (xc, by1), "Function: carries passengers and\ntheir bags between airports",
         direction=90.0, dist=5.0, fs=FS_LABEL, backing=False)
    text(ax, (xc, by0), f"Form: twin-engine jet, {fmt(L)} m long,\n{fmt(B738['span'])} m span with winglets, "
         f"{B738_SEATS_TWO_CLASS} seats", direction=-90.0, dist=5.0, fs=FS_LABEL, backing=False)
    text(ax, (bx0, by1 - 3.0), "boundary", direction=180.0, dist=5.0, fs=FS_LABEL, backing=False)
    xin0, xin1 = -52.0, bx0 - 1.0
    xout0, xout1 = bx1 + 1.0, 98.0
    for y, s in [(10.0, "fuel"), (-1.0, "passengers and bags"), (-12.0, "crew commands")]:
        kind_arrow(ax, (xin0, y), (xin1, y), "leads_to")
        text(ax, (xin0, y), s, direction=90.0, dist=3.0, fs=FS_LABEL, ha="left", backing=False)
    for y, s in [(5.0, "passengers and bags\nat the destination"), (-11.0, "exhaust gas and noise")]:
        kind_arrow(ax, (xout0, y), (xout1, y), "leads_to")
        text(ax, (xout0 + 2.0, y), s, direction=90.0, dist=3.0, fs=FS_LABEL, ha="left", backing=False)
    text(ax, (xin0, 25.0), "Inputs", fs=FS_LABEL, ha="left", backing=False, fontweight="bold")
    text(ax, (xout1, 25.0), "Outputs", fs=FS_LABEL, ha="right", backing=False, fontweight="bold")
    text(ax, (0.5 * (X0 + X1), -36.0), "Outside the boundary (the environment): airports, air traffic control, "
         "and weather", fs=FS_LABEL, backing=False, fontstyle="italic")
    x0, x1, y0, y1 = extent({k: parts[k] for k in _OUTLINE_PARTS})
    close_to(x1 - x0, L, 0.05, "length drawn")
    close_to(y1 - y0, B738["span"], 0.05, "span drawn, winglets included")
    assert 0.3 < fin_t < 0.7, fin_t
    assert bx0 < x0 and x1 < bx1 and by0 < y0 and y1 < by1, "the aircraft lies inside the boundary"
    trim_canvas(fig)
    save_figure(fig, "p11-system-boundary")


def stakeholder_onion():
    """Stakeholders of the Boeing 787 in nested layers, nearest the product first (after
    Alexander's onion model, drawn as nested boxes so every name sits on a straight line)."""
    W, H = 6.5, 3.55
    fig, ax = _canvas(W, H)
    strip = 24.0 * PT                                  # height of one text strip
    pad = 3.0 * PT
    cx, cy = W / 2, H / 2
    c_w, c_h = 1.55, 2 * strip
    widths = [3.05, 4.65, 6.4]
    titles = ["operate it", "buy it or ride in it", "regulate it, build it, or live near it"]
    names = [[("pilots", -0.75), ("mechanics", 0.75)], [("airline", -1.55), ("passengers", 1.55)],
             [("FAA", -2.35), ("Boeing", 0.0), ("airport neighbors", 2.25)]]
    hs = [c_h + 2 * (strip + pad) * (k + 1) for k in range(3)]
    for k in (2, 1, 0):
        w, h = widths[k], hs[k]
        ax.add_patch(opaque(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                           boxstyle=f"round,pad=0,rounding_size={6 * PT}",
                                           fc="white", ec=INK, lw=LW_BOX, zorder=2 + (2 - k))))
    ax.add_patch(opaque(FancyBboxPatch((cx - c_w / 2, cy - c_h / 2), c_w, c_h,
                                       boxstyle=f"round,pad=0,rounding_size={6 * PT}",
                                       fc=HIGHLIGHT, ec=INK, lw=LW_BOX, zorder=6)))
    text(ax, (cx, cy + 0.25 * c_h), "Boeing 787", fs=FS_LABEL, backing=False, fontweight="bold", zorder=12)
    text(ax, (cx, cy - 0.25 * c_h), "the product", fs=FS_LABEL, backing=False, zorder=12)
    for k in range(3):
        h_in = c_h if k == 0 else hs[k - 1]
        y_top = cy + h_in / 2 + 0.5 * (hs[k] - h_in) / 2
        y_bot = cy - h_in / 2 - 0.5 * (hs[k] - h_in) / 2
        text(ax, (cx, y_top), titles[k], fs=FS_LABEL, backing=False, fontstyle="italic", zorder=12)
        for s, dx in names[k]:
            text(ax, (cx + dx, y_bot), s, fs=FS_LABEL, backing=False, zorder=12)
    assert hs[2] < H and widths[2] < W, "the outer layer fits the canvas"
    assert widths[0] > c_w and all(a < b for a, b in zip(widths[:-1], widths[1:])), "layers grow outward"
    trim_canvas(fig)
    save_figure(fig, "p11-stakeholders")


def mission_statement():
    """A statement that names a solution, beside one that states capability and benefit, for
    the survey aircraft of the page, compared row by row: what it is, the capability, the benefit."""
    W, H = 7.2, 2.6
    fig, ax = _canvas(W, H)
    fs = FS_LABEL
    line_h = 1.22 * fs * PT
    # rows: (left lines, left role, right lines, right role); a role of None leaves the row unbraced
    rows = [(["A twin-engine, high-wing", "airplane with a camera", "hatch in the floor"], "a design",
             ["An affordable airborne", "survey system"], "what it is"),
            (["no capability stated"], None, ["that photographs a whole", "county in one working day,"],
             "capability"),
            (["no benefit stated"], None, ["so that mapping companies", "deliver accurate maps", "at low cost"],
             "benefit")]
    gap = 7.0 * PT
    top = H - 0.42
    panels = [[0.02, "Names a solution: avoid", (0, (5.0, 3.0)), 0], [None, "Capability and benefit: use", "-", 2]]
    rights, bottoms = [], []
    for pnl in panels:
        if pnl[0] is None:
            pnl[0] = rights[-1] + 0.12 + 0.22               # the second panel starts 0.22 in after the first
        x0, title, ls, col = pnl
        xt = x0 + 0.12
        lines_all = [ln for r in rows for ln in r[col]]
        w_text = max(_tw(ax, ln, fs)[0] for ln in lines_all)
        xb = xt + w_text + 8 * PT                   # braces 8 pt right of the longest line
        y = top - 0.08
        right = xb
        for r in rows:
            n = max(len(r[0]), len(r[2]))
            lines, role = r[col], r[col + 1]
            italic = role is None
            for k, ln in enumerate(lines):
                text(ax, (xt, y - (k + 0.5) * line_h), ln, fs=fs, ha="left", backing=False,
                     fontstyle="italic" if italic else "normal", color=STEEL if italic else INK)
            if role:
                y1 = y - len(lines) * line_h
                D.brace(ax, (xb, y - 1 * PT), (xb, y1 + 1 * PT), side=1, depth=6.0)
                text(ax, (xb + 12 * PT, 0.5 * (y + y1)), role, fs=fs, ha="left", backing=False, fontstyle="italic")
                right = max(right, xb + 12 * PT + _tw(ax, role, fs)[0])
            y -= n * line_h + gap
        rights.append(right)
        bottoms.append(y + gap)
    yb = min(bottoms) - 0.1
    for (x0, title, ls, col), right in zip(panels, rights):
        ax.add_patch(FancyBboxPatch((x0, yb), right + 0.12 - x0, top - yb, boxstyle=f"round,pad=0,rounding_size={6 * PT}",
                                    fc="none", ec=INK, lw=LW_BOX, ls=ls, zorder=1))
        text(ax, (x0 + 0.1, top), title, direction=90.0, dist=5.0, fs=FS_LABEL, ha="left", backing=False,
             fontweight="bold")
    assert yb > 0.02 and rights[0] + 0.12 < panels[1][0] and rights[1] + 0.12 < W, "both statements fit"
    trim_canvas(fig)
    save_figure(fig, "p11-mission-statement")


# short names of the needs, for the ranking figure
NEED_SHORT = {"N1": "full-day endurance", "N2": "sharp images", "N3": "short airstrips", "N4": "single pilot",
              "N5": "low operating cost"}


def needs_ranking():
    """Each need in rank order: the three stakeholders' ratings on a range line, the average as a
    heavy tick. The spread behind each average is what the figure shows."""
    rows = ranking()
    order = sorted(rows, key=lambda d: d["rank"])
    fig, ax = data_axes(6.5, 3.6, grid=False)
    ys = np.arange(len(order))[::-1].astype(float)
    marks = [("o", SERIES[0], 0.25), ("s", SERIES[1], 0.0), ("^", SERIES[2], -0.25)]
    for y, d in zip(ys, order):
        r = d["ratings"]
        ax.plot([min(r), max(r)], [y, y], color="#767676", lw=1.4, solid_capstyle="butt", zorder=2)
        ax.plot([d["avg"], d["avg"]], [y - 0.11, y + 0.11], color=INK, lw=3.0, solid_capstyle="butt", zorder=3)
    for j, (who, (m, c, off)) in enumerate(zip(RATERS, marks)):
        ax.plot([d["ratings"][j] for d in order], ys + off, m, ms=7.5, mfc=c, mec=INK, mew=0.8, ls="none",
                zorder=5, label=who)
    ax.plot([], [], color=INK, lw=3.0, marker="|", ms=0, label="average")
    xa = 5.45
    for y, d in zip(ys, order):
        text(ax, (xa, y), fmt(d["avg"]), fs=FS_LABEL, ha="left", backing=False)
    text(ax, (xa, ys[0] + 0.62), "Average", fs=FS_LABEL, ha="left", backing=False, fontweight="bold")
    ax.set_yticks(ys, [f"{d['rank']}. {d['id']}, {NEED_SHORT[d['id']]}" for d in order])
    ax.tick_params(axis="y", length=0)
    # the tie: a bracket joining the two rows at 4.000, named in words
    yt = [y for y, d in zip(ys, order) if abs(d["avg"] - 4.0) < 1e-9]
    xt = 6.25
    ax.plot([xt - 0.08, xt, xt, xt - 0.08], [yt[0], yt[0], yt[1], yt[1]], color=INK, lw=LW_THIN, zorder=3)
    text(ax, (xt, 0.5 * (yt[0] + yt[1])), "tie: the owner's\nrating decides", direction=0.0, dist=5.0,
         fs=FS_LABEL, backing=False)
    xmin, xmax = 0.6, 8.0
    ax.set_xlim(xmin, xmax)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_ylim(-0.6, len(order) - 0.15)
    ax.set_xlabel("Rating, 1 (nice to have) to 5 (must have)")
    ax.xaxis.set_label_coords((3.0 - xmin) / (xmax - xmin), -0.13)
    ax.spines["bottom"].set_bounds(1.0, 5.0)
    ax.spines["left"].set_visible(False)
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=4, frameon=False, fontsize=FS_LABEL,
              handletextpad=0.4, columnspacing=1.3, handlelength=1.2)
    tie = [d for d in order if abs(d["avg"] - 4.0) < 1e-9]
    assert [d["id"] for d in tie] == ["N5", "N2"], "the tie at 4.000 is broken by the owner's rating"
    for d in order:
        close_to(d["avg"], sum(d["ratings"]) / 3.0, 1e-12, d["id"])
        assert min(d["ratings"]) <= d["avg"] <= max(d["ratings"]), "the average lies on its range line"
    save_figure(fig, "p11-needs-ranking")


def requirement_anatomy():
    """A requirement = metric + value, with its reason kept beside it."""
    W, H = 6.5, 3.0
    fig, ax = _canvas(W, H)
    d = great_circle_nmi(BOS, LAX)
    top = H - 0.03
    hdr = [("Metric", "what is measured"), ("Value", "how much"), ("Reason", "why that much")]
    ex = ["Range with a full\npassenger load", f"At least {fmt(RANGE_REQ_NMI)} nmi",
          f"Boston to Los Angeles is\n{fmt(d)} nmi on a great circle;\nthe rest covers winds,\n"
          "detours, and reserve fuel"]
    xs, ws = [0.03, 2.03, 3.78], [1.8, 1.55, 2.69]
    Hb = max(D.box_height(ax, e, keep_breaks=True) for e in ex)
    lh = 1.22 * FS_LABEL * PT
    y_box = top - 2 * lh - 0.08 - Hb / 2
    boxes = []
    for x, w, (h1, h2), e in zip(xs, ws, hdr, ex):
        text(ax, (x, top), h1, fs=FS_LABEL, ha="left", va="top", backing=False, fontweight="bold")
        text(ax, (x, top - lh), h2, fs=FS_LABEL, ha="left", va="top", backing=False)
        boxes.append(D.box(ax, (x + w / 2, y_box), e, w=w, h=Hb, keep_breaks=True))
    rx0, rx1 = xs[0], xs[2] + ws[2]
    gap_v = 2 * lh + 0.22
    y_res_top = y_box - Hb / 2 - gap_v
    res_text = f"Requirement: the range with a full passenger load is at least {fmt(RANGE_REQ_NMI)} nmi."
    hr = D.box_height(ax, res_text, rx1 - rx0)
    res = D.box(ax, (0.5 * (rx0 + rx1), y_res_top - hr / 2), res_text, w=rx1 - rx0, h=hr, fill=BOX_FILL_START)
    for b in boxes[:2]:
        f = (b.cx - (res.cx - res.w / 2)) / res.w
        D.route(ax, b, "bottom", res, "top", dst_f=f)
    # the reason is kept with the requirement: a dashed link, no arrowhead
    xk = boxes[2].cx - boxes[2].w / 2 + 0.25
    ln = ax.plot([xk, xk], [boxes[2].cy - Hb / 2, res.cy + res.h / 2], color=INK, lw=1.4, ls=(0, (4.0, 2.5)),
                 zorder=3, solid_capstyle="butt", dash_capstyle="butt")[0]
    text(ax, (xk, 0.5 * (boxes[2].cy - Hb / 2 + res.cy + res.h / 2)),
         "kept with the requirement, so\nthe value can be checked later", direction=0.0, dist=7.0, fs=FS_LABEL,
         backing=False, fontstyle="italic")
    assert d < RANGE_REQ_NMI, "the value covers the route the reason names"
    assert res.cy < boxes[2].cy and abs(res.w - (rx1 - rx0)) < 1e-9, "the requirement spans the three parts"
    trim_canvas(fig)
    save_figure(fig, "p11-requirement-anatomy")


def _blocked(ax, p0, p1, bar=8.0):
    """A "ruled out" link: a dashed line from p0 down to p1 ending in a short bar across it (no
    arrowhead), so it cannot be read as the solid "leads to" arrow of an allowed design."""
    ln = ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="#3A3A3A", lw=1.4, ls=(0, (4.0, 2.5)), zorder=3,
                 solid_capstyle="butt", dash_capstyle="butt")[0]
    h = 0.5 * bar * PT
    b = ax.plot([p1[0] - h, p1[0] + h], [p1[1], p1[1]], color=INK, lw=2.2, zorder=3, solid_capstyle="butt")[0]
    gid = "grp:blocked%d" % next(_BLOCKED)
    ln.set_gid(gid)
    b.set_gid(gid)
    return ln


_BLOCKED = iter(range(1, 10000))


def dependent_requirement():
    """One requirement that names a design beside one that names a result (dependent): the
    first allows one main landing gear design, the second all three."""
    W, H = 6.5, 2.7
    fig, ax = _canvas(W, H)
    sink = fmt(SINK_RATE_FPS, 2)
    panels = [(0.02, 3.13, "Names the design: avoid",
               "The main landing gear\nuses an oleo strut.", (True, False, False), (0, (5.0, 3.0))),
              (3.37, 6.48, "Names the result (dependent): use",
               f"The main landing gear absorbs a\ntouchdown at {sink} ft/s without damage.", (True, True, True), "-")]
    designs = ["Oleo strut", "Steel spring leg", "Composite spring leg"]
    top = H - 0.02
    Hr = max(D.box_height(ax, p[3], keep_breaks=True) for p in panels)
    counts = []
    for x0, x1, title, req, ok, ls in panels:
        text(ax, (0.5 * (x0 + x1), top), title, fs=FS_LABEL, va="top", backing=False, fontweight="bold")
        r = D.box(ax, (0.5 * (x0 + x1), top - 0.32 - Hr / 2), req, w=x1 - x0, h=Hr, keep_breaks=True, ls=ls)
        gap = 0.08
        w = (x1 - x0 - 2 * gap) / 3.0
        hd = max(D.box_height(ax, dn, w, FS_LABEL) for dn in designs)
        yd = 0.62
        for k, (dn, good) in enumerate(zip(designs, ok)):
            cx = x0 + w / 2 + k * (w + gap)
            b = D.box(ax, (cx, yd), dn, w=w, h=hd, fill=BOX_FILL)
            f = (cx - (r.cx - r.w / 2)) / r.w
            if good:
                D.route(ax, r, "bottom", b, "top", src_f=f)
            else:
                _blocked(ax, (cx, r.cy - r.h / 2), (cx, yd + hd / 2 + 4 * PT))
            text(ax, (cx, yd - hd / 2), "allowed" if good else "ruled out", direction=-90.0, dist=4.0,
                 fs=FS_LABEL, backing=False, fontweight="bold" if good else "normal",
                 fontstyle="normal" if good else "italic")
        counts.append(sum(ok))
    assert counts == [1, 3], "naming the design allows one gear; naming the result allows all three"
    trim_canvas(fig)
    save_figure(fig, "p11-dependent-requirement")


def statement_to_requirement():
    """One line of the survey example: the pilot's words, the need statement, the requirement."""
    W, H = 6.5, 1.9
    fig, ax = _canvas(W, H)
    texts = ["“On bumpy days\nhalf my pictures\ncome out blurred.”",               # broken by hand: "at most"
             "N2: The camera\nimages are sharp in\nlight turbulence.",             # stays with its number
             "R2: Image smear\nat survey speed in\nlight turbulence is\nat most 0.5 pixel."]
    w = 1.9
    gap_pt = 22.0
    left = (W - 3 * w - 2 * gap_pt * PT) / 2
    yb = H - 0.05 - 0.5 * max(D.box_height(ax, t, w, keep_breaks=True) for t in texts)
    bs = D.row(ax, texts, yb, left, w, gap=gap_pt, fills=[None, None, BOX_FILL_START], keep_breaks=True)
    for a, b in zip(bs[:-1], bs[1:]):
        D.route(ax, a, "right", b, "left")
    notes = ["Customer statement: the pilot's words, written down as said",
             "Need statement: what, not how; an attribute of the system",
             "Requirement: a metric and a value that a test can check"]
    for b, s in zip(bs, notes):
        t = D.wrap(ax, s, b.w, FS_LABEL)
        text(ax, (b.cx, b.cy - b.h / 2), t, direction=-90.0, dist=6.0, fs=FS_LABEL, backing=False,
             fontstyle="italic")
    assert all(a.cx < b.cx for a, b in zip(bs[:-1], bs[1:])), "left to right"
    assert all(abs(a.cy - b.cy) < 1e-12 for a, b in zip(bs[:-1], bs[1:])), "one row"
    trim_canvas(fig)
    save_figure(fig, "p11-statement-to-requirement")


def traceability_matrix():
    """A draft traceability matrix with a gap and an orphan, beside the corrected one. The draft,
    the version to avoid, has a dashed frame, as the wrong side of every comparison on the page."""
    W, H = 6.5, 3.3
    fig, ax = _canvas(W, H)
    needs = [n for n, _ in NEEDS]
    good = {(r[1], r[0]) for r in REQS}
    draft_reqs = ["R1", "R2", "R4", "R5", "R6", "R7"]
    draft = {(n, r) for (n, r) in good if r in draft_reqs}
    lone_n, lone_r = trace_problems(needs, draft_reqs, draft)
    fixed_reqs = [r[0] for r in REQS]
    ln2, lr2 = trace_problems(needs, fixed_reqs, good)
    assert lone_n == ["N3"] and lone_r == ["R7"] and not ln2 and not lr2, "the draft has one gap and one orphan"
    c = 0.3
    y0 = 1.13
    for (ox, reqs, links, title, note, ls) in [
            (0.75, draft_reqs, draft, "Draft: two errors", "N3 has no requirement;\nR7 (a high wing) traces to no need",
             (0, (5.0, 3.0))),
            (4.45, fixed_reqs, good, "Corrected", "every row and every\ncolumn holds an X", "-")]:
        cells, fills = [], []
        for n in needs:
            cells.append(["X" if (n, r) in links else "" for r in reqs])
            fills.append(["#E3E3E3" if (title.startswith("Draft") and (n in lone_n or r in lone_r)) else None
                          for r in reqs])
        D.matrix(ax, (ox, y0), cells, c, c, row_labels=needs, col_labels=reqs, fills=fills, fs=FS_LABEL,
                 label_fs=FS_LABEL)
        xm = ox + c * len(reqs) / 2
        nw = max(_tw(ax, ln, FS_LABEL)[0] for ln in note.split("\n"))
        fx0 = min(ox - 0.72, xm - nw / 2 - 0.1)
        fx1 = max(ox + c * len(reqs) + 0.17, xm + nw / 2 + 0.1)
        fy0, fy1 = -0.12, y0 + c * len(needs) + 0.47
        ax.add_patch(FancyBboxPatch((fx0, fy0), fx1 - fx0, fy1 - fy0, boxstyle=f"round,pad=0,rounding_size={6 * PT}",
                                    fc="none", ec=INK, lw=LW_BOX, ls=ls, zorder=1))
        text(ax, (fx0 + 0.08, fy1), title, direction=90.0, dist=5.0, fs=FS_LABEL, ha="left", backing=False,
             fontweight="bold")
        text(ax, (xm, 0.02), note, fs=FS_LABEL, va="bottom", backing=False, fontstyle="italic")
        text(ax, (ox - 0.36, y0 + c * len(needs)), "needs", direction=90.0, dist=5.0, fs=FS_LABEL, backing=False)
        text(ax, (xm, y0 - 0.43), "requirements", fs=FS_LABEL, backing=False)
    trim_canvas(fig)
    save_figure(fig, "p11-traceability-matrix")


def make_all():
    road_map()
    system_boundary()
    stakeholder_onion()
    mission_statement()
    needs_ranking()
    requirement_anatomy()
    dependent_requirement()
    statement_to_requirement()
    traceability_matrix()


def values():
    P = TAG
    rows = ranking()
    for d in rows:
        record(P, f"avg-{d['id']}", fmt(d["avg"]))
        record(P, f"rank-{d['id']}", str(d["rank"]))
    d_bl = great_circle_nmi(BOS, LAX)
    record(P, "bos-lax-nmi", fmt(d_bl))
    record(P, "earth-r-mean", fmt(RADIUS_EARTH_MEAN))
    record(P, "range-req-nmi", fmt(RANGE_REQ_NMI))
    record(P, "b738-seats", str(B738_SEATS_TWO_CLASS))
    record(P, "b738-length", fmt(B738["length"]))
    record(P, "b738-span", fmt(B738["span"]))
    record(P, "b738-span-wing", fmt(B738["span_wing"]))
    record(P, "sink-fps", fmt(SINK_RATE_FPS, 2))
    record(P, "sink-ms", fmt(SINK_RATE_FPS * FT, 3))
    record(P, "sum-N1", str(sum(RATINGS["N1"])))
    record(P, "sum-N2", str(sum(RATINGS["N2"])))
    record(P, "sum-N3", str(sum(RATINGS["N3"])))
    record(P, "sum-N4", str(sum(RATINGS["N4"])))
    record(P, "sum-N5", str(sum(RATINGS["N5"])))
    record(P, "range-wrong-nmi", fmt(RANGE_WRONG_NMI))
    record(P, "nmi-m", fmt(NMI))
    assert great_circle_nmi(BOS, LAX) < RANGE_REQ_NMI < RANGE_WRONG_NMI
    record(P, "qualify-h", fmt(QUALIFY_H, 3))
    record(P, "engine-change-h", fmt(ENGINE_CHANGE_H, 1))
    record(P, "survey-day-h", fmt(SURVEY_DAY_H, 1))
    vals = {r[0]: r[3] for r in REQS}
    for rid, key, num in [("R1", "R1-endurance-h", "6"), ("R2", "R2-smear-px", "0.5"), ("R3", "R3-takeoff-m", "600"),
                          ("R5", "R5-install-min", "15"), ("R6", "R6-cost-pct", "80")]:
        assert num in vals[rid], (rid, vals[rid])
        record(P, key, num)
    assert float("6") > SURVEY_DAY_H, "R1 covers the survey day plus the transit"
