"""The look of Chapter 1, Systems Engineering and Fundamental Thoughts: the chapter's record
of printed values, save_figure, and the named styles its figures share.

Built on the book's figure kit (scripts/figkit.py), which is re-exported here: the Arial math
setup, fmt, the text, arrow, dimension and axes helpers, and the layout gate. Page modules do
not import this file directly; they use the one import line

    from chapter_1.common import *

Chapter 2 names and values are reused wherever the thing is the same (FS_LABEL, LW_THIN,
GRAY, the data-series looks of SERIES_STYLE, the "reference" and "boundary" line roles).
"""
import math
import sys
from pathlib import Path

if __name__ not in ("chapter_1.style", "__main__"):
    raise ImportError("import this module as chapter_1.style (or through chapter_1.common), "
                      "not as a bare 'style': the value record must be one object")

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from figkit import *  # noqa: E402,F401,F403
from figkit import _anchor, _backing, _screen_angle, _style  # noqa: E402,F401
from make_figures import plt, np, NOTES, INK, GOLD, DUST, LIGHT, AGED, STEEL, SERIES  # noqa: E402,F401
from matplotlib.patches import Polygon, FancyArrowPatch, ArrowStyle, Circle, PathPatch  # noqa: E402,F401
from matplotlib.path import Path as MPath  # noqa: E402,F401

# ===================================================================== the record of printed values
PAGES = {
    "p11": "needs-and-requirements",
    "p12": "hazards-and-risk",
    "p13": "vehicle-anatomy",
    "p14": "standard-atmosphere",
    "p15": "bernoulli-and-pitot-static",
    "p16": "aircraft-sizing",
    "p17": "concepts-and-trade-studies",
}
CHAPTER = Chapter(1, PAGES, Path(__file__).resolve().parent)
VALUES, VALUES_FILE, WRITTEN = CHAPTER.VALUES, CHAPTER.VALUES_FILE, CHAPTER.WRITTEN
record, write_values, save_figure = CHAPTER.record, CHAPTER.write_values, CHAPTER.save_figure

# ===================================================================== line weights
LW_MAIN = 2.0             # pt, main curves and data lines (= LW_ORBIT of Chapter 2)
LW_OUTLINE = 1.8          # pt, the outer outline of a drawn vehicle, airfoil or duct wall
LW_DETAIL = 1.0           # pt, lines inside an outline: hinge lines, stage joints, panel edges
LW_BOX = 1.2              # pt, the edge of a diagram box or matrix cell
LW_FINE = 0.7             # pt, small details drawn on a part: windows, doors, hidden tanks
# LW_THIN (0.9 pt) from the kit: construction, dimension, extension and reference lines

# ===================================================================== fills (light, so black text reads on them)
PART_FILL = "#FFFFFF"     # a part drawn as line art: white, opaque (hides what lies behind it)
HIGHLIGHT = LIGHT         # the part a figure is about: Purdue light gold #F5EFDC (black text 19:1)
SURFACE_FILL = "#E8E8E8"  # control surfaces and other moving parts, with HATCH_SURFACE
HATCH_SURFACE = "////"    # hatch of a control surface (reads in grayscale)
BOX_FILL = "#FFFFFF"      # a diagram box
BOX_FILL_START = LIGHT    # the first and last box of a flow chart (start, result)
FLUID_FILL = "#DCEBF7"    # a liquid in a manometer or tank (black text 17:1)
GAS_FILL = "#F3F7FB"      # air or gas inside a duct, when it is shaded at all

# Risk levels of these notes (likelihood x consequence: High 15 or more, Medium 5 to 12, Low 4
# or less). The levels differ in lightness (white, light gray, darker gray with a hatch), never in hue
# alone, and the figure names them in a key, so the matrix reads in grayscale.
RISK_STYLE = {
    "Low":    dict(fill="#FFFFFF", hatch=None, text=INK),
    "Medium": dict(fill="#E3E3E3", hatch=None, text=INK),
    "High":   dict(fill="#B0B0B0", hatch="///", text=INK),
}

# ===================================================================== arrow kinds (FIGURE_STANDARD point 30)
# One arrow style means one thing. Every kind differs from the others in more than color:
#   force      black, heavy shaft, large solid head                 (a force where it acts)
#   velocity   blue #0072B2, medium shaft, normal solid head         (a velocity, to scale when compared)
#   flow       open block arrow, black outline, white inside         (the direction a fluid moves)
#   leads_to   dark gray #3A3A3A, medium shaft, normal head, routed  (a step in a process, a diagram link)
#   moment     black curved arrow with a small head                 (a rotation: roll, pitch, yaw)
#   dimension  thin black, small heads at both ends                 (a length; use dimension())
#   axis       black, 1.2 pt, normal head, from the origin            (a body or coordinate axis; body_axes())
ARROW_KIND = {
    "force":     dict(color=INK, lw=2.2, head="large"),
    "velocity":  dict(color=SERIES[0], lw=1.6, head="normal"),
    "leads_to":  dict(color="#3A3A3A", lw=1.4, head="normal"),
    "moment":    dict(color=INK, lw=1.4, head="normal"),
    "dimension": dict(color=INK, lw=LW_THIN, head="small"),
    "axis":      dict(color=INK, lw=1.2, head="normal"),
}
TEXT_KIND = {"force": INK, "velocity": SERIES[0], "leads_to": INK, "moment": INK, "dimension": INK, "flow": INK,
             "axis": INK}


def pt(ax, n):
    """n points in data units, on equal-aspect axes whose limits are set. Example: pt(ax, 6.0)"""
    ax.figure.canvas.draw_idle()
    a = ax.transData.inverted().transform([(0.0, 0.0), (n * ax.figure.dpi / 72.0, 0.0)])
    return float(a[1, 0] - a[0, 0])


def kind_arrow(ax, p0, p1, kind="force", label=None, label_dir=None, dist=4.0, fs=FS_LABEL, zorder=7, label_at="tip",
               **kw):
    """A straight arrow of one of the chapter's kinds ("force", "velocity", "leads_to", "moment",
    "dimension"; "flow" draws flow_arrow()) from p0 to p1 (data), tip on p1, with an optional
    label beyond the tip (or toward label_dir, deg); label_at="mid" puts it beside the middle of
    the shaft instead (toward label_dir, default: to the left of the arrow). Returns the patch.
    Example: kind_arrow(ax, (0, 0), (0, 2), "force", "lift, L")"""
    if kind == "flow":
        return flow_arrow(ax, p0, p1, label=label, zorder=zorder, **kw)
    st = dict(ARROW_KIND[kind])
    st.update(kw)
    pa = arrow(ax, p0, p1, color=st["color"], lw=st["lw"], head=st["head"], zorder=zorder)
    if label:
        a = _screen_angle(ax, np.asarray(p1, float) - np.asarray(p0, float))
        if label_at == "mid":
            ang = a + 90.0 if label_dir is None else label_dir
            at = 0.5 * (np.asarray(p0, float) + np.asarray(p1, float))
        else:
            ang = a if label_dir is None else label_dir
            at = p1
        text(ax, at, label, direction=ang, dist=dist + 2.0, fs=fs, color=TEXT_KIND[kind], zorder=zorder + 3)
    return pa


def flow_arrow(ax, p0, p1, width=7.0, head_width=13.0, head_len=9.0, label=None, label_dir=None, dist=4.0,
               fs=FS_LABEL, fill="white", lw=1.2, zorder=6):
    """The flow-direction arrow: an open block arrow (black outline, white inside) from p0 to p1
    (data), `width` points wide with a head `head_width` x `head_len` points. It shows which way
    a fluid moves, never a force or a velocity value. Equal-aspect axes. Returns the patch.
    Example: flow_arrow(ax, (-1.0, 0.0), (-0.4, 0.0), label="flow")"""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    fig = ax.figure
    fig.canvas.draw_idle()
    d0, d1 = ax.transData.transform(p0), ax.transData.transform(p1)
    k = fig.dpi / 72.0
    L = np.hypot(*(d1 - d0))
    u = (d1 - d0) / L
    n = np.array([-u[1], u[0]])
    w, hw, hl = 0.5 * width * k, 0.5 * head_width * k, head_len * k
    b = d1 - hl * u
    poly = np.array([d0 + w * n, b + w * n, b + hw * n, d1, b - hw * n, b - w * n, d0 - w * n])
    data = ax.transData.inverted().transform(poly)
    pa = ax.add_patch(Polygon(data, closed=True, fc=fill, ec=INK, lw=lw, joinstyle="miter", zorder=zorder))
    pa.set_gid("flow-arrow")
    if label:
        ang = _screen_angle(ax, p1 - p0) if label_dir is None else label_dir
        text(ax, p1, label, direction=ang, dist=dist + 2.0, fs=fs, zorder=zorder + 3)
    return pa


def moment_arrow(ax, center, radius, t0, t1, label=None, label_at=None, dist=4.0, kind="moment", fs=FS_LABEL,
                 zorder=7):
    """A curved arrow (a rotation: roll, pitch or yaw) on a circle of `radius` (data) about
    `center`, from angle t0 to t1 (deg; counterclockwise when t1 > t0), head at t1. The label sits
    outside the arc at angle label_at (default: the middle). Equal-aspect axes. Returns the Line2D.
    Example: moment_arrow(ax, (0, 0), 1.2, 200, 340, "roll")"""
    st = ARROW_KIND[kind]
    th = np.radians(np.linspace(t0, t1, 90))
    cx, cy = center
    xs, ys = cx + radius * np.cos(th), cy + radius * np.sin(th)
    ln = ax.plot(xs[:-4], ys[:-4], color=st["color"], lw=st["lw"], zorder=zorder, solid_capstyle="butt")[0]
    # (t0 > t1 draws a clockwise arrow)
    rides_on(arrow(ax, (xs[-6], ys[-6]), (xs[-1], ys[-1]), color=st["color"], lw=st["lw"], head=st["head"],
                   zorder=zorder), ln)
    if label:
        b = math.radians(0.5 * (t0 + t1) if label_at is None else label_at)
        text(ax, (cx + radius * math.cos(b), cy + radius * math.sin(b)), label, direction=math.degrees(b),
             dist=dist + 2.0, fs=fs, zorder=zorder + 3)
    return ln


def motion_heads(ax, x, y, at, line=None, color=INK, zorder=6):
    """Motion arrowheads (the kit's MOTION_HEAD, 10 x 3 pt) on a drawn path (x, y arrays), at the
    fractions `at` (0 to 1) of its length, pointing along the path: the direction of flight on a
    mission profile, of flow on a streamline. Pass the path's Line2D as `line`.
    Example: ln = ax.plot(x, y)[0]; motion_heads(ax, x, y, (0.3, 0.7), line=ln)"""
    x, y = np.asarray(x, float), np.asarray(y, float)
    s = np.r_[0.0, np.cumsum(np.hypot(np.diff(x), np.diff(y)))]
    heads = []
    for f in at:
        si = f * s[-1]
        i = int(np.clip(np.searchsorted(s, si), 1, len(s) - 1))
        tip = np.array([np.interp(si, s, x), np.interp(si, s, y)])
        back = np.array([x[i - 1], y[i - 1]])
        if np.hypot(*(tip - back)) == 0:
            back = np.array([x[max(i - 2, 0)], y[max(i - 2, 0)]])
        hl, hw = MOTION_HEAD
        heads.append(rides_on(ax.add_patch(FancyArrowPatch(tuple(back), tuple(tip), mutation_scale=1.0, lw=0.8,
                                                         arrowstyle=ArrowStyle("-|>", head_length=hl, head_width=hw),
                                                         color=color, shrinkA=0.0, shrinkB=0.0, joinstyle="miter",
                                                         zorder=zorder)), line))
    return heads


def legend_key(ax, xy, kinds, dy=None, fs=FS_SMALL, length=None):
    """A small key naming the arrow kinds used in a figure (point 30: two kinds of arrow in one
    figure are named): one short sample arrow per kind, stacked downward from xy (data), each
    with its name to the right. kinds: list of (kind, name). Returns the bottom y.
    Example: legend_key(ax, (5.0, 3.0), [("force", "force"), ("velocity", "velocity")])"""
    fig = ax.figure
    fig.canvas.draw_idle()
    inv = ax.transData.inverted()
    p = ax.transData.transform(xy)
    k = fig.dpi / 72.0
    L = (length or 28.0) * k
    step = (dy or 18.0) * k
    y = p[1]
    for kind, name in kinds:
        a, b = inv.transform((p[0], y)), inv.transform((p[0] + L, y))
        if kind == "flow":
            flow_arrow(ax, a, b, width=6.0, head_width=11.0, head_len=7.0)
        else:
            kind_arrow(ax, a, b, kind)
        text(ax, b, name, direction=0.0, dist=6.0, fs=fs)
        y -= step
    return inv.transform((p[0], y))[1]
