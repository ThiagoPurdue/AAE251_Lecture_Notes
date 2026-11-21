"""Block diagrams, flow charts and matrices that pass the layout gate by construction.

One box style, one arrow style ("leads_to"), aligned on a grid. A box wraps its text to its
width and keeps even padding; an arrow leaves one box edge and meets another at a right angle,
with right-angle bends only; the gate then checks that text fits its box, that boxes keep clear
of each other, and that an arrow crosses no box, line or other arrow (figkit, check 6).

Work in data units on equal-aspect axes from new_axes(), with the axis limits set FIRST
(set_frame below does it): text wrapping and padding are measured in points.

    fig, ax = new_axes(6.5, 3.0)
    set_frame(ax, 0, 10, 0, 4)
    a = box(ax, (2, 2), "Guess the takeoff weight", w=2.6)
    b = box(ax, (6, 2), "Compute the empty-weight fraction", w=2.6)
    route(ax, a, "right", b, "left")
"""
import math
import re
import textwrap

import numpy as np

from chapter_1.style import *  # noqa: F401,F403
from chapter_1.style import _backing, _style  # noqa: F401
from matplotlib.patches import Polygon, FancyBboxPatch, Circle, PathPatch
from matplotlib.path import Path as MPath

PAD = 6.0          # pt, padding between a box edge and its text
DISC_FILL = "white"  # the chapter's one numbered disc (step_marker, numbered_callout, key_disc):
DISC_LW = 0.9        # a white disc, a thin black ring (pt), and a regular-weight black digit
GAP = 14.0         # pt, the usual clear space between boxes (room for an arrow and its head)


def canvas(width, height=None, xlim=None, ylim=None):
    """Frameless equal-aspect axes that fill a figure `width` inches wide, so save_figure reports
    the true size and text widths can be planned. With xlim and ylim, the figure height follows
    from them (data units of your choice); without, the data units are inches and the canvas is
    width x height (a point is 1/72). Example: fig, ax = canvas(6.5, 3.0); fig, ax = canvas(6.5,
    xlim=(-5, 45), ylim=(-20, 20))"""
    if xlim is not None and ylim is not None:
        height = width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
    else:
        xlim, ylim = (0.0, width), (0.0, height)
    fig, ax = new_axes(width, height)
    fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
    set_frame(ax, xlim[0], xlim[1], ylim[0], ylim[1])
    return fig, ax


def set_frame(ax, x0, x1, y0, y1):
    """Fix the data limits of a diagram (do it before placing boxes: wrapping and padding are
    measured in points). Example: set_frame(ax, 0, 10, 0, 4)"""
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.figure.canvas.draw()



def _text_size(ax, s, fs, weight="normal"):
    """Width and height (data units) of the text s at fs points."""
    fig = ax.figure
    t = ax.text(0, 0, s, fontsize=fs, fontweight=weight, ha="left", va="baseline", linespacing=1.15)
    fig.canvas.draw()
    bb = t.get_window_extent(fig.canvas.get_renderer())
    t.remove()
    inv = ax.transData.inverted()
    p0, p1 = inv.transform((bb.x0, bb.y0)), inv.transform((bb.x1, bb.y1))
    return float(p1[0] - p0[0]), float(p1[1] - p0[1])


def text_size(ax, s, fs=FS_LABEL, weight="normal"):
    """Width and height (data units) of the text s at fs points (set the axis limits first).
    Example: w, h = text_size(ax, "Guess W0")"""
    return _text_size(ax, s, fs, weight)


# units that never start a line of a box: they stay with the number before them
BOX_UNITS = {"m", "km", "cm", "mm", "ft", "nmi", "kt", "knots", "s", "min", "h", "K", "kg", "t", "lb", "Pa", "kPa",
         "m/s", "km/s", "ft/min", "%", "°C", "°", "minutes", "seconds", "hours", "days", "years"}


def _is_number(w):
    return bool(re.match(r"^[−+-]?\(?[0-9]", w))


def _glue(words):
    """Group the words of a box so that a line never starts with a number (it stays with the
    word before it: "stage 1", "to 2.5") and a unit never stands alone (it stays with its
    number: "2.5 min")."""
    groups = []
    for w in words:
        if groups and (_is_number(w) or (w.rstrip(",;.") in BOX_UNITS and _is_number(groups[-1].split()[-1]))):
            groups[-1] += " " + w
        else:
            groups.append(w)
    return groups


def wrap(ax, s, width, fs=FS_LABEL):
    """Break s into lines no wider than `width` (data units) at fs points, at spaces, never
    before a number and never between a number and its unit (see _glue). When the plain
    left-to-right fill would leave one word alone on the last line, the same number of lines
    is balanced instead (no line gets wider than `width`, and no box gets taller).
    Example: wrap(ax, "Compute the empty-weight fraction", 2.4)"""
    words = _glue(s.split())
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and _text_size(ax, trial, fs)[0] > width:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    lines.append(cur)
    if len(lines) >= 2 and len(lines[-1].split()) == 1:
        lines = _balanced(ax, words, len(lines), width, fs) or lines
    return "\n".join(lines)


def _balanced(ax, words, n, width, fs):
    """The split of `words` into exactly n lines, each no wider than `width`, that makes the
    line widths most even (least sum of squared slack); None if there is none."""
    memo = {}

    def wid(i, j):
        if (i, j) not in memo:
            memo[(i, j)] = _text_size(ax, " ".join(words[i:j]), fs)[0]
        return memo[(i, j)]

    best = {}

    def solve(i, k):                      # words[i:] in k lines -> (cost, [break points])
        if (i, k) in best:
            return best[(i, k)]
        m = len(words)
        if k == 1:
            w = wid(i, m)
            out = ((width - w) ** 2, [m]) if w <= width else None
        else:
            out = None
            for j in range(i + 1, m - k + 2):
                w = wid(i, j)
                if w > width:
                    break
                rest = solve(j, k - 1)
                if rest is not None:
                    c = (width - w) ** 2 + rest[0]
                    if out is None or c < out[0]:
                        out = (c, [j] + rest[1])
        best[(i, k)] = out
        return out

    if len(words) < n:
        return None
    r = solve(0, n)
    if r is None:
        return None
    cuts, i, lines = r[1], 0, []
    for j in cuts:
        lines.append(" ".join(words[i:j]))
        i = j
    return lines


class Box:
    """A diagram box: .patch (the shape), .text (its label), .cx, .cy, .w, .h, and .side(name,
    f=0.5): the point on the "left", "right", "top" or "bottom" edge at fraction f along it
    (left to right, bottom to top)."""

    def __init__(self, patch, text_, cx, cy, w, h, shape="box"):
        self.patch, self.text, self.cx, self.cy, self.w, self.h, self.shape = patch, text_, cx, cy, w, h, shape

    def side(self, name, f=0.5):
        x0, x1, y0, y1 = self.cx - self.w / 2, self.cx + self.w / 2, self.cy - self.h / 2, self.cy + self.h / 2
        if self.shape == "diamond":
            return {"left": (x0, self.cy), "right": (x1, self.cy), "top": (self.cx, y1), "bottom": (self.cx, y0)}[name]
        return {"left": (x0, y0 + f * (y1 - y0)), "right": (x1, y0 + f * (y1 - y0)),
                "top": (x0 + f * (x1 - x0), y1), "bottom": (x0 + f * (x1 - x0), y0)}[name]


def box(ax, xy, text_, w=None, h=None, fs=FS_LABEL, fill=BOX_FILL, lw=LW_BOX, pad=PAD, rounded=True, bold=False,
        group=None, name=None, zorder=4, keep_breaks=False, ls="-"):
    """A box centered at xy (data) with its text wrapped to fit and centered, `pad` points of
    padding on every side. w: the width (data; the text wraps to w minus the padding); h: the
    height (default: just enough for the text). rounded: small corner radius. keep_breaks=True
    keeps the text exactly as given, broken at its own "\n" (no re-wrap, so a phrase such as
    "a = -0.0065 K/m" stays on one line). ls: the outline style ("-", or a dash pattern such as
    (0, (5, 3)) for a boundary). The gate checks that the text stays inside with the padding and
    that the box keeps 2 pt from other boxes (boxes of one `group` may touch). Returns a Box.
    Example: b = box(ax, (2, 3), "Define the mission", w=2.4)"""
    p = pt(ax, pad)
    if w is None:
        tw, th = _text_size(ax, text_, fs)
        w = tw + 2 * p
    s = text_ if keep_breaks else wrap(ax, text_, w - 2 * p, fs)
    tw, th = _text_size(ax, s, fs)
    if h is None:
        h = th + 2 * p
    x0, y0 = xy[0] - w / 2, xy[1] - h / 2
    r = pt(ax, 4.0) if rounded else 0.0
    pa = FancyBboxPatch((x0, y0), w, h, boxstyle=f"round,pad=0,rounding_size={r}" if rounded else "square,pad=0",
                        fc=fill, ec=INK, lw=lw, ls=ls, zorder=zorder)
    ax.add_patch(opaque(pa))
    pa._box = group
    pa._name = name or text_[:24]
    t = ax.text(xy[0], xy[1], s, ha="center", va="center", fontsize=fs, color=INK, zorder=zorder + 1,
                linespacing=1.15, fontweight="bold" if bold else "normal")
    t._in_box = pa
    return Box(pa, t, xy[0], xy[1], w, h)


def box_height(ax, text_, w=None, fs=FS_LABEL, pad=PAD, keep_breaks=False):
    """The height (data) box() gives a box of width w holding text_ (with keep_breaks=True, of
    the text as broken at its own "\n"; w is then not needed). Example: box_height(ax, "Guess W0", 3.0)"""
    p = pt(ax, pad)
    s = text_ if keep_breaks else wrap(ax, text_, w - 2 * p, fs)
    return _text_size(ax, s, fs)[1] + 2 * p


LEAD = 1.3         # baseline-to-baseline spacing of lines_box(), in units of the font size


def lines_box_height(n, fs=FS_LABEL, pad=7.0, lead=LEAD, ax=None):
    """The height (points, or data units when ax is given) of a lines_box() of n lines.
    Example: h = lines_box_height(3, FS_SMALL, ax=ax)"""
    hpt = (n - 1) * lead * fs + 0.96 * fs + 2.0 * pad
    return pt(ax, hpt) if ax is not None else hpt


def lines_box(ax, xy, lines, w, h=None, fs=FS_LABEL, fill=BOX_FILL, pad=7.0, lead=LEAD, lw=LW_BOX, zorder=4,
              name=None):
    """A box holding the given lines of text, one under the other on evenly spaced baselines
    (`lead` times the font size apart), centered as a block: a line with math or subscripts
    keeps the same spacing as a plain one, which a single multi-line text does not. w: the
    width (data); h: the height (default: lines_box_height). Returns a Box (its .text is the
    first line). Example: b = lines_box(ax, (3, 2), ["0 to 11,000 m", "gradient layer"], w=3.6)"""
    n = len(lines)
    if h is None:
        h = lines_box_height(n, fs, pad, lead, ax)
    b = box(ax, xy, " ", w=w, h=h, fs=fs, fill=fill, lw=lw, zorder=zorder, name=name or lines[0][:24],
            keep_breaks=True)
    b.text.remove()
    L = pt(ax, lead * fs)
    y1 = xy[1] + ((n - 1) * L - pt(ax, 0.5 * fs)) / 2.0
    first = None
    for i, s in enumerate(lines):
        t = ax.text(xy[0], y1 - i * L, s, ha="center", va="baseline", fontsize=fs, color=INK, zorder=zorder + 1)
        t._in_box = b.patch
        first = first or t
    b.text = first
    return b


def column(ax, texts, cx, top, w, gap=20.0, fills=None, **kw):
    """Boxes stacked top to bottom in reading order, centered on x = cx, the first one's top at
    `top` (data), each `gap` points below the one above (room for a "leads_to" arrow). fills:
    one fill per box (None for the default). Returns the list of Box. Example: bs = column(ax, ["a", "b"], 3.0, 9.5, 4.0)"""
    out = []
    y = top
    for i, s in enumerate(texts):
        h = box_height(ax, s, w, kw.get("fs", FS_LABEL), kw.get("pad", PAD), kw.get("keep_breaks", False))
        fill = (fills[i] if fills is not None and fills[i] else BOX_FILL)
        out.append(box(ax, (cx, y - h / 2), s, w=w, fill=fill, **kw))
        y -= h + pt(ax, gap)
    return out


def row(ax, texts, cy, left, w, gap=24.0, fills=None, **kw):
    """Boxes side by side, left to right in reading order, centered on y = cy, the first one's left
    edge at `left` (data), each `gap` points right of the one before, all `w` wide and as tall as
    the tallest. Returns the list of Box. Example: bs = row(ax, ["a", "b", "c"], 2.0, 0.5, 2.2)"""
    h = max(box_height(ax, s, w, kw.get("fs", FS_LABEL), kw.get("pad", PAD), kw.get("keep_breaks", False))
            for s in texts)
    out = []
    x = left
    for i, s in enumerate(texts):
        fill = (fills[i] if fills is not None and fills[i] else BOX_FILL)
        out.append(box(ax, (x + w / 2, cy), s, w=w, h=h, fill=fill, **kw))
        x += w + pt(ax, gap)
    return out


def decision_size(ax, text_, w=None, h=None, fs=FS_LABEL, pad=PAD, ratio=2.0, keep_breaks=False):
    """Width, height (data) and wrapped text of the decision() diamond for text_ (see decision()).
    keep_breaks=True keeps the question as broken at its own "\n" (for example two lines,
    "Which layer\nholds $h$?"). Use it to place the diamond before drawing it.
    Example: w, h, s = decision_size(ax, "Converged?", w=3.0)"""
    p = pt(ax, pad)
    best = None
    full = _text_size(ax, text_, fs)[0]
    for k in ((1,) if keep_breaks else range(1, 6)):        # 1 to 5 lines
        if keep_breaks:
            s = text_
        else:
            s = wrap(ax, text_, full / k * 1.05 + 1e-9, fs) if k > 1 else text_
        tw, th = _text_size(ax, s, fs)
        TW, TH = tw + 2 * p, th + 2 * p
        if w is None and h is None:
            ww = TW + ratio * TH
            hh = ww / ratio
        elif h is None:
            if TW >= w:
                continue
            ww, hh = w, TH / (1.0 - TW / w)
        else:
            ww, hh = (w, h) if w is not None else (h * ratio, h)
            if TW / ww + TH / hh > 1.0:
                continue
        if best is None or ww * hh < best[1] * best[2]:
            best = (s, ww, hh)
        if w is not None and h is not None:
            break
    if best is None:
        raise ValueError(f"decision: {text_!r} does not fit a {w} x {h} diamond; make it larger or leave h out")
    s, ww, hh = best
    return ww, hh, s


def decision(ax, xy, text_, w=None, h=None, fs=FS_LABEL, fill=BOX_FILL, lw=LW_BOX, pad=PAD, ratio=2.0, name=None,
             zorder=4, keep_breaks=False):
    """A flow-chart decision node: a diamond centered at xy (data) with its question inside, fitted
    so the text block (plus `pad` points) lies inside the diamond: a text block TW x TH fits a
    diamond w x h when TW/w + TH/h <= 1. Give w (h is then the least that fits), both (the text
    wraps until it fits; ValueError if it cannot), or neither (w/h = ratio). Exits from its four
    corners (Box.side("left"), ...). Returns a Box. Example: d = decision(ax, (5, 2), "Converged?")"""
    cx, cy = xy
    w, h, s = decision_size(ax, text_, w, h, fs, pad, ratio, keep_breaks)
    poly = np.array([(cx - w / 2, cy), (cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2)])
    pa = Polygon(poly, closed=True, fc=fill, ec=INK, lw=lw, joinstyle="miter", zorder=zorder)
    ax.add_patch(opaque(pa))
    pa._box = None
    pa._name = name or text_[:24]
    t = ax.text(cx, cy, s, ha="center", va="center", fontsize=fs, color=INK, zorder=zorder + 1, linespacing=1.15)
    t._in_box = pa
    return Box(pa, t, cx, cy, w, h, shape="diamond")

def route(ax, src, src_side, dst, dst_side, via=(), src_f=0.5, dst_f=0.5, label=None, label_at=0.5, label_side=1,
          kind="leads_to", fs=FS_SMALL, zorder=3):
    """An arrow from one box edge to another with right angles only. It leaves `src` from the
    middle (or fraction src_f) of its side src_side ("left", "right", "top", "bottom") at a right
    angle, passes through the points of `via` (corners; each a point, or ("x", value) / ("y",
    value) to turn at that coordinate), and meets `dst` at a right angle on dst_side with its tip
    on the edge. A label (e.g. "yes", "no") sits beside segment number label_at (fraction of
    the path length) on side label_side (+1 left of the direction of travel, -1 right). The gate
    checks it crosses nothing. Returns the Line2D. Example: route(ax, a, "right", b, "left")"""
    st = ARROW_KIND[kind]
    p0 = np.array(src.side(src_side, src_f), dtype=float)
    p1 = np.array(dst.side(dst_side, dst_f), dtype=float)
    pts = [p0]
    out_dir = {"left": (-1, 0), "right": (1, 0), "top": (0, 1), "bottom": (0, -1)}
    cur = p0.copy()
    for v in via:
        if isinstance(v, tuple) and len(v) == 2 and isinstance(v[0], str):
            axis, val = v
            nxt = np.array([val, cur[1]]) if axis == "x" else np.array([cur[0], val])
        else:
            nxt = np.asarray(v, dtype=float)
        pts.append(nxt)
        cur = nxt
    d = np.array(out_dir[dst_side], dtype=float)
    # last corner: line up with the target point along the entry direction
    if d[0] != 0:                       # entering horizontally
        if abs(cur[1] - p1[1]) > 1e-12:
            pts.append(np.array([cur[0], p1[1]]))
    else:
        if abs(cur[0] - p1[0]) > 1e-12:
            pts.append(np.array([p1[0], cur[1]]))
    pts.append(p1)
    P = np.array(pts)
    # drop repeated points
    keep = [0] + [i for i in range(1, len(P)) if np.hypot(*(P[i] - P[i - 1])) > 1e-12]
    P = P[keep]
    for a, b in zip(P[:-1], P[1:]):
        if abs(a[0] - b[0]) > 1e-9 and abs(a[1] - b[1]) > 1e-9:
            raise ValueError(f"route: segment {a} -> {b} is not horizontal or vertical; add a via point")
    hl = _style(st["head"], st["lw"])[1]
    ln = ax.plot(P[:, 0], P[:, 1], color=st["color"], lw=st["lw"], zorder=zorder, solid_joinstyle="miter",
                 solid_capstyle="butt")[0]
    ln._route = (src.patch, dst.patch)
    ln._head_len = hl
    # the head: along the last segment, tip on the edge
    tail = P[-1] - (P[-1] - P[-2]) / np.hypot(*(P[-1] - P[-2])) * pt(ax, hl + 1.0)
    rides_on(arrow(ax, tail, P[-1], color=st["color"], lw=st["lw"], head=st["head"], zorder=zorder + 0.1), ln)
    if label:
        seg = np.hypot(*np.diff(P, axis=0).T)
        s = label_at * seg.sum()
        i = int(np.searchsorted(np.cumsum(seg), s))
        i = min(i, len(seg) - 1)
        a, b = P[i], P[i + 1]
        f = (s - (np.cumsum(seg)[i] - seg[i])) / seg[i]
        m = a + f * (b - a)
        ang = math.degrees(math.atan2(*(b - a)[::-1])) + 90.0 * label_side
        text(ax, m, label, direction=ang, dist=4.0, fs=fs, zorder=zorder + 4)
    return ln


def step_marker(ax, xy, n, r=9.0, fs=FS_SMALL, zorder=8, beside=None, gap=4.0):
    """A numbered step marker: the chapter's one numbered disc (white, a thin black ring, the
    number n in regular black type) of radius r points, centered at xy (data). The numbers match
    the numbered steps of the text. (numbered_callout() and key_disc() draw the same disc, with
    and without a leader, for a name key.) With beside=a Box the
    marker sits just outside the box's left edge, `gap` points clear of it, level with its
    middle (xy is then ignored). Returns the Circle.
    Example: step_marker(ax, b.side("top", 0.0), 1)"""
    rr = pt(ax, r)
    if beside is not None:
        xy = (beside.cx - beside.w / 2 - rr - pt(ax, gap), beside.cy)
    c = ax.add_patch(opaque(Circle(xy, rr, fc=DISC_FILL, ec=INK, lw=DISC_LW, zorder=zorder)))
    ax.text(xy[0], xy[1], str(n), ha="center", va="center", fontsize=fs, color=INK, zorder=zorder + 1)
    return c


def numbered_callout(ax, target, n, at, r=8.0, fs=FS_SMALL, zorder=9):
    """A numbered callout: a white disc with a black ring and the number n at `at` (data), with
    a short leader to `target` (use when a panel would carry more than about seven names: put the
    names in a table next to the figure). Returns the Circle.
    Example: numbered_callout(ax, parts["slat_L"].inside, 3, at=(12, 14))"""
    rr = pt(ax, r)
    at, target = np.asarray(at, dtype=float), np.asarray(target, dtype=float)
    d = target - at
    L = np.hypot(*d)
    start = at + d / L * rr
    ln = ax.plot([start[0], target[0]], [start[1], target[1]], color=INK, lw=0.7, zorder=zorder - 0.5)[0]
    ln.set_gid(f"grp:callout{n}")
    ax.plot(*target, "o", ms=2.6, color=INK, zorder=zorder, gid=f"grp:callout{n}")
    c = ax.add_patch(Circle(at, rr, fc=DISC_FILL, ec=INK, lw=DISC_LW, zorder=zorder, gid=f"grp:callout{n}"))
    ax.text(at[0], at[1], str(n), ha="center", va="center", fontsize=fs, color=INK, zorder=zorder + 1)
    return c


def key_disc(ax, xy, n, r=7.5, zorder=30):
    """A white numbered disc with no leader, opaque: the number of a part named in a key beside the
    figure (numbered_callout draws the same disc with a leader). Example: key_disc(ax, (1.2, 30.0), 3)"""
    rr = pt(ax, r)
    c = ax.add_patch(opaque(Circle(xy, rr, fc=DISC_FILL, ec=INK, lw=DISC_LW, zorder=zorder)))
    ax.text(xy[0], xy[1], str(n), ha="center", va="center", fontsize=FS_SMALL, color=INK, zorder=zorder + 1)
    return c


def brace(ax, p0, p1, label=None, side=1, depth=6.0, fs=FS_LABEL, lw=LW_THIN, zorder=4):
    """A curly brace from p0 to p1 (data), its point `depth` points toward side +1 (left of the
    direction p0 -> p1) or -1, with an optional label beyond the point. Groups items (the stages
    of a vehicle, the steps of a phase). Returns the PathPatch. Example: brace(ax, (0, 0), (0, 3), "stage 1", side=-1)"""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    L = np.hypot(*(p1 - p0))
    u = (p1 - p0) / L
    n = np.array([-u[1], u[0]]) * side
    dd = pt(ax, depth)
    q = lambda s, h: p0 + s * L * u + h * dd * n           # noqa: E731
    # two smooth halves that meet at the point
    verts = [q(0, 0), q(0, 0.5), q(0.08, 0.5), q(0.42, 0.5), q(0.5, 0.5), q(0.5, 1.0),
             q(0.5, 1.0), q(0.5, 0.5), q(0.58, 0.5), q(0.92, 0.5), q(1.0, 0.5), q(1.0, 0.0)]
    codes = [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3, MPath.LINETO, MPath.CURVE3, MPath.CURVE3,
             MPath.MOVETO, MPath.CURVE3, MPath.CURVE3, MPath.LINETO, MPath.CURVE3, MPath.CURVE3]
    pa = ax.add_patch(PathPatch(MPath(verts, codes), fc="none", ec=INK, lw=lw, zorder=zorder))
    if label:
        tip = q(0.5, 1.0)
        ang = math.degrees(math.atan2(n[1], n[0]))
        text(ax, tip, label, direction=ang, dist=3.0, fs=fs, zorder=zorder + 2)
    return pa


def matrix(ax, origin, cells, cell_w, cell_h, row_labels=None, col_labels=None, fills=None, hatches=None, fs=FS_LABEL,
           label_fs=FS_LABEL, lw=LW_BOX, group="matrix", zorder=3):
    """A grid of cells with row and column headers (a risk matrix, a traceability matrix, a
    decision matrix). origin: the lower-left corner of the cell block (data). cells: a list of
    rows, top row first, of strings (a cell's text, wrapped to fit, or ""). fills and hatches:
    the same shape, a color and a hatch per cell (None for white, no hatch). Row labels sit to
    the left of each row, column labels under each column. The cells share one group, so the
    gate lets them touch. Returns a dict (row, col) -> Box (row 0 at the top).
    Example: m = matrix(ax, (1, 0), [["", "x"], ["x", ""]], 1.0, 0.6, ["N1", "N2"], ["R1", "R2"])"""
    nr, nc = len(cells), len(cells[0])
    out = {}
    x0, y0 = origin
    for i in range(nr):
        for j in range(nc):
            cx = x0 + (j + 0.5) * cell_w
            cy = y0 + (nr - i - 0.5) * cell_h
            fc = (fills[i][j] if fills is not None and fills[i][j] else "white")
            pa = ax.add_patch(opaque(Polygon([(cx - cell_w / 2, cy - cell_h / 2), (cx + cell_w / 2, cy - cell_h / 2),
                                              (cx + cell_w / 2, cy + cell_h / 2), (cx - cell_w / 2, cy + cell_h / 2)],
                                             closed=True, fc=fc, ec=INK, lw=lw, joinstyle="miter", zorder=zorder)))
            h = hatches[i][j] if hatches is not None else None
            if h:
                pa.set_hatch(h)
            pa._box = group
            pa._name = f"cell {i},{j}"
            t = None
            s = cells[i][j]
            if s:
                ws = wrap(ax, s, cell_w - 2 * pt(ax, 3.0), fs)
                t = ax.text(cx, cy, ws, ha="center", va="center", fontsize=fs, color=INK, zorder=zorder + 2,
                            linespacing=1.1, bbox=_backing(fc) if h else None)
                t._in_box = pa
            out[(i, j)] = Box(pa, t, cx, cy, cell_w, cell_h)
    if row_labels:
        for i, s in enumerate(row_labels):
            cy = y0 + (nr - i - 0.5) * cell_h
            text(ax, (x0, cy), s, direction=180.0, dist=5.0, fs=label_fs)
    if col_labels:
        for j, s in enumerate(col_labels):
            cx = x0 + (j + 0.5) * cell_w
            text(ax, (cx, y0), s, direction=-90.0, dist=5.0, fs=label_fs)
    return out


# ===================================================================== even margins
def trim_canvas(fig, margin=6.0):
    """Crop a diagram figure to its drawn content plus `margin` points on every side, keeping
    the scale, so every canvas has the same even margin. One equal-aspect axes per figure.
    Spines, axis lines and invisible artists do not count. Call it last, before save_figure.
    Example: trim_canvas(fig)"""
    from matplotlib.spines import Spine
    from matplotlib.axis import Axis
    from matplotlib.transforms import Bbox
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    bbs = []
    for ax in fig.axes:
        for a in ax.get_children():
            if isinstance(a, (Spine, Axis)) or a is ax.patch or not a.get_visible():
                continue
            if hasattr(a, "get_text") and not a.get_text().strip():
                continue
            try:
                bb = a.get_window_extent(r)
            except Exception:
                continue
            if bb.width <= 0 and bb.height <= 0:
                continue
            if not (np.isfinite(bb.x0) and np.isfinite(bb.y1)):
                continue
            bbs.append(bb)
    u = Bbox.union(bbs)
    ax = fig.axes[0]
    inv = ax.transData.inverted()
    (dx0, dy0), (dx1, dy1) = inv.transform((u.x0, u.y0)), inv.transform((u.x1, u.y1))
    xl, yl = ax.get_xlim(), ax.get_ylim()
    pos = ax.get_position()
    s_in = pos.width * fig.get_size_inches()[0] / (xl[1] - xl[0])        # inches per data unit
    m = margin / 72.0 / s_in
    x0, x1, y0, y1 = dx0 - m, dx1 + m, dy0 - m, dy1 + m
    fig.set_size_inches((x1 - x0) * s_in, (y1 - y0) * s_in)
    ax.set_position([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    fig.canvas.draw()
    return fig.get_size_inches()
