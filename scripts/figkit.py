"""The figure kit of the AAE251 lecture notes: one look and one layout gate for every chapter.

Chapter-neutral code shared by the chapter packages (scripts/chapter_N/): the Arial math
setup, number formatting (fmt), the style constants and line roles, the text, arrow and
dimension helpers, the axes helpers, the layout gate (layout_problems, pixel_problems,
svg_problems) and, through a Chapter object, save_figure and the record of printed values.
A chapter module makes its Chapter once and re-exports what its pages need:

    from figkit import *
    CHAPTER = Chapter(2, {"p21": "orbit-properties", ...}, Path(__file__).resolve().parent)
    record, write_values, save_figure = CHAPTER.record, CHAPTER.write_values, CHAPTER.save_figure

Import it as `figkit` only (scripts/ on the import path), never by a file path: a second
copy would split the drawing-group counter. The physics of each chapter stays in the
chapter's own modules. Run this file for its unit checks:

    python3 -B scripts/figkit.py
"""
import json
import math
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

if __name__ not in ("figkit", "__main__"):
    raise ImportError("import this module as figkit (from figkit import ...), not through a package path")

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from make_figures import plt, np, save, NOTES, INK, GOLD, DUST, LIGHT, AGED, STEEL, SERIES  # noqa: E402,F401
import matplotlib.ticker as mticker  # noqa: E402
from matplotlib.markers import MarkerStyle  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, ArrowStyle  # noqa: E402
from matplotlib.text import OffsetFrom  # noqa: E402
from matplotlib.transforms import Affine2D  # noqa: E402

# Math in labels: matplotlib mathtext set in Arial, so a label such as $\Delta V_1$ or
# $v_{\mathrm{esc}}$ matches the Arial text around it. The SVG keeps it as live text.
plt.rcParams.update({
    "mathtext.fontset": "custom",
    "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic",
    "mathtext.bf": "Arial:bold",
    "mathtext.sf": "Arial",
    "mathtext.default": "it",
    "mathtext.fallback": "stixsans",       # a glyph Arial lacks; save_figure() rejects it
    "font.size": 12,
    "axes.labelsize": 12,
    "axes.linewidth": 0.9,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "xtick.major.width": 0.9,
    "ytick.major.width": 0.9,
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "legend.fontsize": 11,
    "legend.frameon": False,
    "lines.dash_capstyle": "butt",
    "lines.solid_joinstyle": "round",
    "hatch.linewidth": 1.0,
    "axes.unicode_minus": True,
})

# Subscripts made of a word ($v_{\mathrm{orbit}}$) or the infinity sign ($v_\infty$) are set at
# SUB_WORD of the main size, not mathtext's 0.7, so they read at 10 pt or more on the page (a
# 12 pt label gives a 10.6 pt subscript). Single-letter subscripts ($r_p$, $\Delta V_1$) keep 0.7.
# Done by parsing such a label with a larger shrink factor; svg_problems() checks the result.
SUB_WORD = 0.88
_WORD_SUB = re.compile(r"_\{?\\(?:mathrm\{[A-Za-z]{2,}\}|infty)")
import functools as _functools  # noqa: E402
import matplotlib._mathtext as _mtx  # noqa: E402
from matplotlib.mathtext import MathTextParser as _MTP  # noqa: E402
if not hasattr(_mtx, "SHRINK_FACTOR") or not hasattr(_MTP._parse_cached, "__wrapped__"):
    raise ImportError("matplotlib changed: the word-subscript size in orbits.py needs updating")
_parse_plain = _MTP._parse_cached.__wrapped__


@_functools.lru_cache(200)
def _parse_cached(self, s, dpi, prop, antialiased, load_glyph_flags):
    if not _WORD_SUB.search(s):
        return _parse_plain(self, s, dpi, prop, antialiased, load_glyph_flags)
    old, _mtx.SHRINK_FACTOR = _mtx.SHRINK_FACTOR, SUB_WORD
    try:
        return _parse_plain(self, s, dpi, prop, antialiased, load_glyph_flags)
    finally:
        _mtx.SHRINK_FACTOR = old


_MTP._parse_cached = _parse_cached

# ===================================================================== number formatting
def _dec(x):
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(f"cannot format {x}")
    return Decimal(repr(x))


def _commas(d, nd, minus):
    s = f"{abs(d):,.{nd}f}"
    return (minus + s) if d < 0 and float(d) != 0.0 else s


def fmt(x, sig=4, minus="-"):
    """x with `sig` significant figures, thousands separated by commas, rounded half up.
    Digits before the decimal point are never rounded away: a number with `sig` or more
    integer digits prints as a whole number (26578.3 -> "26,578", 5828.5 -> "5,829").
    Trailing zeros are kept (2.4 with sig=3 -> "2.40"). `minus` replaces the minus sign
    (pass "−" for figure text that is not math). Example: fmt(0.264786) -> "0.2648" """
    d = _dec(x)
    if d == 0:
        return "0" if sig <= 1 else "0." + "0" * (sig - 1)
    exp = abs(d).adjusted()
    nd = max(sig - 1 - exp, 0)
    q = d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    if abs(q).adjusted() > exp and nd > 0:                 # 9.9996 -> 10.00, not 10.000
        nd -= 1
        q = d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return _commas(q, nd, minus)


def fmt_dec(x, nd, minus="-"):
    """x with exactly nd decimals, thousands separated by commas, rounded half up.
    Example: fmt_dec(5828.46, 1) -> "5,828.5" """
    q = _dec(x).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return _commas(q, nd, minus)


def fmt_sci(x, sig=4):
    """x in powers of ten as LaTeX math (no dollar signs): "1.327 \\times 10^{11}".
    Use inside $...$ on a page or in a figure label. Example: fmt_sci(MU["Sun"]) -> "1.327 \\times 10^{11}" """
    d = _dec(x)
    exp = abs(d).adjusted()
    m = fmt(float(d.scaleb(-exp)), sig)
    if m.lstrip("-").startswith("10"):                    # 9.9996e3 -> 1.000e4
        exp += 1
        m = fmt(float(d.scaleb(-exp)), sig)
    return m if exp == 0 else f"{m} \\times 10^{{{exp}}}"


# ===================================================================== style
FIG_WIDTH = 6.5           # in, the usual figure width (shown at :width: 60% to 90%)
FS_LABEL = 12             # pt, labels, symbols, axis labels
FS_SMALL = 11             # pt, secondary notes and tick labels; nothing smaller
LW_ORBIT = 2.0            # pt, orbits and data curves
LW_ARROW = 1.6            # pt, vectors and burn arrows
LW_THIN = 0.9             # pt, axes, construction, dimension and reference lines
GRAY = "#767676"          # reference lines (4.54:1 on white)
GRID = "#DDDDDD"          # data-plot grid (decorative)
BLUE, VERMILION, GREEN, PURPLE = SERIES[0], SERIES[1], SERIES[2], SERIES[3]

# Line roles: one look per role across a chapter. color = the line, text = a label in that
# hue with at least 4.5:1 on white. The kit holds the two chapter-neutral roles; a chapter
# adds its own with register_roles() (Chapter 2: the orbit roles).
STYLE = {
    "reference": dict(color=GRAY, text=STEEL, ls="-", lw=LW_THIN),                         # apse lines, axes
    "boundary":  dict(color=GRAY, text=STEEL, ls=(0, (4.0, 3.0)), lw=LW_THIN),             # SOI, atmosphere edge, asymptote
}
SEQUENCE = []          # a chapter's main roles, in order (bars() takes its hatches from it)


def register_roles(roles, sequence=()):
    """Add a chapter's line roles to STYLE (name -> dict(color, text, ls, lw[, cap])) and its
    main roles, in order, to SEQUENCE. Example: register_roles({"initial": dict(color=BLUE,
    text=BLUE, ls="-", lw=LW_ORBIT)}, ["initial"])"""
    STYLE.update(roles)
    SEQUENCE.extend(s for s in sequence if s not in SEQUENCE)


# Data series (curves of a data plot, tracks of different orbits, the conic types of a schematic):
# their own color and line-style pairs, none the same as an orbit role, so a data curve never
# looks like an initial, transfer or final orbit. line_kw(i) and text_color(i) use them.
SERIES_STYLE = [
    dict(color=INK, text=INK, ls="-", lw=LW_ORBIT),                                  # 0 black solid
    dict(color=BLUE, text=BLUE, ls=(0, (6.0, 2.5)), lw=LW_ORBIT),                    # 1 blue dashed
    dict(color=VERMILION, text="#B34E00", ls=(0, (0.1, 2.6)), lw=LW_ORBIT, cap="round"),   # 2 vermilion dotted
    dict(color=STEEL, text=STEEL, ls=(0, (7.0, 2.2, 1.4, 2.2)), lw=LW_ORBIT),         # 3 dark gray dash-dot
    dict(color=GREEN, text="#007A5A", ls=(0, (6.0, 1.8, 1.2, 1.8, 1.2, 1.8)), lw=LW_ORBIT),  # 4 green dash-dot-dot
]
MARKERS = ["o", "s", "^", "D", "v"]
HATCHES = ["//", "\\\\", "xx", "..", "++", "--"]
HEAD = {"small": (7.0, 2.4), "normal": (9.0, 3.1), "large": (11.0, 3.8)}   # arrow head length, half-width, pt
MOTION_HEAD = (10.0, 3.0)  # motion arrowhead on an orbit or track: length, half-width, pt (clearly longer than wide)


def connects(artist, *ends):
    """Tag a thin construction line (a zoom connector) and the artists it is drawn to meet at
    its ends: the layout gate checks that it crosses nothing else. Returns the artist."""
    artist.set_gid("connector")
    artist._touches = tuple(id(e) for e in ends if e is not None)
    return artist


def rides_on(patch, *lines):
    """Record the line(s) an arrowhead is drawn on: the layout gate lets a head lie on its own line only."""
    patch._rides = tuple(id(l) for l in lines if l is not None)
    return patch


def line_kw(role=0, **over):
    """Keyword arguments for ax.plot() in an orbit role of STYLE ("initial", "transfer", ...) or
    the i-th data series of SERIES_STYLE (0: black solid, 1: blue dashed, 2: vermilion dotted,
    3: dark gray dash-dot, 4: green dash-dot-dot). Use a role only for an orbit in that role.
    Example: ax.plot(x, y, **line_kw("transfer"))"""
    st = SERIES_STYLE[role] if isinstance(role, int) else STYLE[role]
    kw = dict(color=st["color"], linestyle=st["ls"], linewidth=st["lw"])
    if st.get("cap") == "round":
        kw.update(dash_capstyle="round", solid_capstyle="round")
    kw.update(over)
    return kw


def text_color(role=0):
    """Label color matching a role or series index, with at least 4.5:1 contrast on white.
    Example: text(ax, xy, "transfer orbit", color=text_color("transfer"))"""
    return SERIES_STYLE[role]["text"] if isinstance(role, int) else STYLE[role]["text"]


# ===================================================================== axes
def new_axes(width=FIG_WIDTH, height=4.0, ncols=1, nrows=1, equal=True, **kw):
    """Figure and frameless axes for a schematic (equal aspect, no ticks). With several panels
    returns an array of axes. Draw in km so bodies and orbits are to scale.
    Example: fig, ax = new_axes(6.5, 4.0)"""
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height), squeeze=False, **kw)
    for ax in axes.flat:
        ax.axis("off")
        if equal:
            ax.set_aspect("equal")
    return fig, (axes[0, 0] if axes.size == 1 else axes.squeeze())


class CommaFormatter(mticker.ScalarFormatter):
    """Tick labels with thousands separated by commas (26,000) and no offset or powers of ten.
    Example: ax.yaxis.set_major_formatter(CommaFormatter())"""

    def __init__(self):
        super().__init__(useOffset=False, useMathText=False)
        self.set_scientific(False)

    def __call__(self, x, pos=None):
        s = super().__call__(x, pos)
        m = re.match(r"^([−-]?)(\d+)(.*)$", s)
        return f"{m.group(1)}{int(m.group(2)):,}{m.group(3)}" if m else s


def degree_ticks(ax, axis="x", step=None):
    """Tick labels in degrees ("30°") on one axis, with ticks every `step` deg if given.
    Example: degree_ticks(ax, "x", 90)"""
    a = ax.xaxis if axis == "x" else ax.yaxis
    if step:
        a.set_major_locator(mticker.MultipleLocator(step))
    a.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:g}°".replace("-", "−")))


def data_axes(width=FIG_WIDTH, height=4.0, ncols=1, nrows=1, grid=True, **kw):
    """Figure and axes for a data plot: left and bottom spines, light grid behind the data,
    commas in tick labels. Label the axes with units ("Altitude, km").
    Example: fig, ax = data_axes(6.5, 4.0)"""
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height), squeeze=False, **kw)
    for ax in axes.flat:
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        if grid:
            ax.grid(True, color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.xaxis.set_major_formatter(CommaFormatter())
        ax.yaxis.set_major_formatter(CommaFormatter())
    return fig, (axes[0, 0] if axes.size == 1 else axes.squeeze())


# ===================================================================== text and marks
def _equal(ax):
    return ax.get_aspect() == 1.0


def _screen_angle(ax, vec):
    """Screen angle (deg) of a data-space direction. Exact on equal-aspect axes; on other axes
    taken from the current limits (set the limits first)."""
    vx, vy = float(vec[0]), float(vec[1])
    if _equal(ax):
        return math.degrees(math.atan2(vy, vx))
    p0 = ax.transData.transform((0.0, 0.0))
    p1 = ax.transData.transform((vx, vy))
    return math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))


def _anchor(angle):
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    ha = "left" if c > 0.38 else ("right" if c < -0.38 else "center")
    va = "bottom" if s > 0.38 else ("top" if s < -0.38 else "center")
    return ha, va


def _backing(backing):
    if backing is False or backing is None:
        return None
    fc = "white" if backing is True else backing
    return dict(boxstyle="square,pad=0.12", fc=fc, ec="none")


def text(ax, xy, s, direction=None, dist=5.0, offset=(0.0, 0.0), fs=FS_LABEL, color=INK,
         ha=None, va=None, backing=True, zorder=10, **kw):
    """Write s at the data point xy. With `direction` (deg, screen) the text sits `dist` points
    away from xy in that direction and is anchored on its near side; otherwise it is centered
    at xy shifted by `offset` (points). An opaque white backing (backing=True, or a color, or
    False for none) keeps lines from running through the text. Returns the Annotation.
    Example: text(ax, (0, 0), "Earth", direction=-90)"""
    if direction is not None:
        a = math.radians(direction)
        off = (dist * math.cos(a) + offset[0], dist * math.sin(a) + offset[1])
        h, v = _anchor(direction)
    else:
        off, h, v = offset, "center", "center"
    return ax.annotate(s, xy=tuple(np.asarray(xy, dtype=float)), xytext=off, textcoords="offset points",
                       ha=ha or h, va=va or v, fontsize=fs, color=color, bbox=_backing(backing),
                       zorder=zorder, annotation_clip=False, **kw)


def offset_text(ax, xy, s, dx, dy, **kw):
    """Text centered dx, dy points from the data point xy (shorthand for text(..., offset=)).
    Example: offset_text(ax, (7000, 0), "$r_p$", 0, -12)"""
    return text(ax, xy, s, offset=(dx, dy), **kw)


def callout(ax, xy, s, at, gap=4.0, fs=FS_LABEL, color=INK, ha=None, va="center", backing=True, zorder=10, **kw):
    """A label placed in free space at `at` (data) with a short straight leader to the point xy,
    stopping `gap` points short of it. Use it only where no clear spot touches the point; keep
    leaders short and never crossing. backing: True (white), a fill color for a label on a
    fill, or False. Returns the Annotation.
    Example: callout(ax, node_xy, "ascending node", at=(1.6, -1.2))"""
    xy, at = np.asarray(xy, dtype=float), np.asarray(at, dtype=float)
    h = ha or ("left" if at[0] >= xy[0] else "right")
    an = ax.annotate(s, xy=tuple(xy), xytext=tuple(at), ha=h, va=va, fontsize=fs, color=color, zorder=zorder,
                     bbox=_backing(backing), annotation_clip=False,
                     arrowprops=dict(arrowstyle="-", color=INK, lw=0.7, shrinkA=1.0, shrinkB=gap), **kw)
    an.arrow_patch.set_gid("leader")
    return an


def _style(head, lw):
    hl, hw = HEAD[head] if isinstance(head, str) else head
    return ArrowStyle("-|>", head_length=hl, head_width=hw), hl, hw


def _tip_shrink(hl, hw, lw):
    """No extra shrink: matplotlib already pulls a "-|>" head back by the mitred stroke, so
    the tip lands on the target point."""
    return 0.0


def arrow(ax, p0, p1, color=INK, lw=LW_ARROW, head="normal", both=False, zorder=6, **kw):
    """Straight arrow from p0 to p1 (data), crisp filled head ("small", "normal", "large" or
    (length, half-width) in points), tip exactly on p1. both=True puts a head on each end.
    Returns the patch. Example: arrow(ax, (0, 0), (1000, 0))"""
    style, hl, hw = _style(head, lw)
    if both:
        style = ArrowStyle("<|-|>", head_length=hl, head_width=hw)
    shr = _tip_shrink(hl, hw, lw)
    patch = FancyArrowPatch(tuple(p0), tuple(p1), arrowstyle=style, mutation_scale=1.0, color=color, lw=lw,
                            shrinkA=shr if both else 0.0, shrinkB=shr, joinstyle="miter", capstyle="butt",
                            zorder=zorder, **kw)
    ax.add_patch(patch)
    return patch


def velocity_arrow(ax, xy, v, scale, label=None, color=INK, lw=LW_ARROW, direction=None, dist=4.0,
                   fs=FS_LABEL, head="normal", offset=0.0, center=(0.0, 0.0), zorder=6):
    """Velocity vector v (vx, vy in km/s) drawn from xy at `scale` data units per km/s, so its
    length is to scale; state the scale in the caption or draw speed_key(). With `offset`
    (points) the arrow is moved that far sideways, away from `center` (the central body), so a
    vector tangent to an orbit sits beside the orbit instead of on it (equal-aspect axes). The
    label goes beyond the tip (or toward `direction`, deg). Returns the tip point (data, before
    the sideways offset). Example: velocity_arrow(ax, orbit_point(a, e, 0), orbit_velocity(mu, a, e, 0), 800, "$v_p$")"""
    from matplotlib.transforms import ScaledTranslation
    xy = np.asarray(xy, dtype=float)
    tip = xy + scale * np.asarray(v, dtype=float)
    shift = np.zeros(2)
    kw = {}
    if offset:
        a = math.radians(_screen_angle(ax, tip - xy))
        n = np.array([-math.sin(a), math.cos(a)])
        out = xy - np.asarray(center, dtype=float)
        if np.dot(n, out) < 0:
            n = -n
        shift = offset * n
        kw["transform"] = ax.transData + ScaledTranslation(shift[0] / 72.0, shift[1] / 72.0, ax.figure.dpi_scale_trans)
    arrow(ax, xy, tip, color=color, lw=lw, head=head, zorder=zorder, **kw)
    if label:
        ang = _screen_angle(ax, tip - xy) if direction is None else direction
        text(ax, tip, label, direction=ang, dist=dist, offset=tuple(shift), fs=fs, color=color, zorder=zorder + 4)
    return tip


def speed_key(ax, xy, scale, value=1.0, unit="km/s", color=INK, fs=FS_SMALL):
    """A horizontal reference arrow of `value` (km/s) at `scale` data units per km/s, labeled
    ("1 km/s") to the right of its tip, so arrow lengths can be read. Make it at least as long
    as the label is wide. Example: speed_key(ax, (-9000, -8000), 800)"""
    xy = np.asarray(xy, dtype=float)
    end = xy + np.array([value * scale, 0.0])
    arrow(ax, xy, end, color=color, head="small", lw=LW_ARROW)
    text(ax, end, f"{value:g} {unit}", direction=0.0, dist=5, fs=fs, color=color)
    return end


def point(ax, xy, label=None, direction=90.0, dist=5.0, color=INK, ms=6.0, kind="dot", fs=FS_LABEL, zorder=8,
          gid=None):
    """A marked point (a spacecraft, a planet position, a launch site) with an optional label
    placed toward `direction` (deg). kind: "dot", "open", "square", "diamond". gid: a drawing
    group ("grp:...", see dimension()) the point belongs to. Example: point(ax, (0, 7000), "chaser", direction=0)"""
    m = {"dot": "o", "open": "o", "square": "s", "diamond": "D"}[kind]
    ax.plot(*xy, m, color=color, mfc="white" if kind == "open" else color, mec=color, ms=ms,
            mew=1.4 if kind == "open" else 0.8, zorder=zorder, gid=gid)
    if label:
        text(ax, xy, label, direction=direction, dist=dist + ms / 2.0, fs=fs, color=color, zorder=zorder + 2)


def line(ax, p0, p1, role="reference", **kw):
    """A straight line from p0 to p1 in a STYLE role (default: thin gray reference line).
    Example: line(ax, (-12178, 0), (7078, 0))"""
    return ax.plot([p0[0], p1[0]], [p0[1], p1[1]], zorder=kw.pop("zorder", 2), **line_kw(role, **kw))[0]


def angle_arc(ax, center, radius, t0, t1, label=None, dist=4.0, arrow_end=False, color=INK, lw=LW_THIN,
              fs=FS_LABEL, backing=True, zorder=5):
    """Arc of `radius` (data units) about `center` from angle t0 to t1 (deg, counterclockwise
    when t1 > t0), with the label on the bisector just outside the arc. arrow_end=True puts
    a head at t1. Needs equal-aspect axes. Example: angle_arc(ax, (0, 0), 2500, 0, 120, r"$\\theta$")"""
    th = np.radians(np.linspace(t0, t1, max(8, int(abs(t1 - t0) * 2))))
    cx, cy = center
    xs, ys = cx + radius * np.cos(th), cy + radius * np.sin(th)
    arc = ax.plot(xs, ys, color=color, lw=lw, zorder=zorder, solid_capstyle="butt")[0]
    if arrow_end:
        rides_on(arrow(ax, (xs[-3], ys[-3]), (xs[-1], ys[-1]), color=color, lw=lw, head="small", zorder=zorder), arc)
    if label:
        b = math.radians(0.5 * (t0 + t1))
        text(ax, (cx + radius * math.cos(b), cy + radius * math.sin(b)), label, direction=math.degrees(b),
             dist=dist, fs=fs, color=color, backing=backing, zorder=zorder + 4)


_GROUPS = __import__("itertools").count(1)


def dimension(ax, p0, p1, label=None, offset=0.0, label_side=1, color=INK, lw=LW_THIN, fs=FS_LABEL,
              zorder=2.5, ticks=True, extension=True):
    """Dimension line between p0 and p1 (data), shifted `offset` data units to the left of the
    direction p0 -> p1, with arrow heads, end ticks and thin extension lines back to p0 and
    p1. The label sits beside the middle of the line (label_side=+1: to the left of
    p0 -> p1, -1: to the right) or, with label_side=0, on the line, breaking it with a white
    backing (engineering style; exempt from the label-crossing check). ticks=False leaves out the
    end ticks and extension=False the extension lines (a dimension drawn on a line between
    two marked points). Needs equal-aspect axes unless the line is horizontal or vertical.
    Example: dimension(ax, (-12178, 0), (7078, 0), "$2a$", offset=-3000)"""
    p0, p1 = np.asarray(p0, dtype=float), np.asarray(p1, dtype=float)
    d = p1 - p0
    u = d / np.hypot(*d)
    n = np.array([-u[1], u[0]])
    q0, q1 = p0 + offset * n, p1 + offset * n
    grp = f"grp:dim{next(_GROUPS)}"                   # its parts may touch each other (layout gate)
    if offset and extension:
        over = 0.12 * offset
        for p, q in ((p0, q0), (p1, q1)):
            ax.plot([p[0], q[0] + over * n[0]], [p[1], q[1] + over * n[1]], color=color, lw=0.7, zorder=zorder,
                    gid=grp)
    arrow(ax, q0, q1, color=color, lw=lw, head="small", both=True, zorder=zorder, gid=grp)
    ang = _screen_angle(ax, d)
    if ticks:
        tick = MarkerStyle("|", transform=Affine2D().rotate_deg(ang))
        ax.plot([q0[0], q1[0]], [q0[1], q1[1]], ls="none", marker=tick, ms=9, mew=lw, color=color, zorder=zorder,
                gid=grp)
    if label:
        mid = 0.5 * (q0 + q1)
        if label_side == 0:
            text(ax, mid, label, fs=fs, color=color, zorder=zorder + 4, gid="on-line")
        else:
            text(ax, mid, label, direction=ang + 90.0 * label_side, dist=4.0, fs=fs, color=color, zorder=zorder + 4)
    return grp


def radius_arrow(ax, center, r, angle, label=None, side=1, color=INK, lw=LW_THIN, fs=FS_LABEL, at=0.55,
                 zorder=2.5):
    """A radius: a thin line from `center` out to distance r (data units) toward `angle` (deg)
    with a head on the far end, labeled beside the line at fraction `at` of its length
    (side=+1: left of the outward direction, -1: right). Drawn under the bodies, so it seems
    to start at the body's surface. Returns the end point.
    Example: radius_arrow(ax, (0, 0), 26578.0, 200.0, "$r_2$")"""
    c = np.asarray(center, dtype=float)
    d = np.array([math.cos(math.radians(angle)), math.sin(math.radians(angle))])
    end = c + r * d
    arrow(ax, c, end, color=color, lw=lw, head="small", zorder=zorder)
    if label:
        text(ax, c + at * r * d, label, direction=angle + 90.0 * side, dist=4.0, fs=fs, color=color,
             zorder=zorder + 4)
    return end


def label_curve(ax, x, y, x_at, s, role=0, offset=(0.0, 8.0), color=None, fs=FS_LABEL, **kw):
    """Direct label for a data curve: s centered `offset` points from the curve point at x_at,
    in the curve's text color, on a white backing. Example: label_curve(ax, r, v, 3e8, "Earth", 0)"""
    y_at = float(np.interp(x_at, np.asarray(x, dtype=float), np.asarray(y, dtype=float)))
    return text(ax, (x_at, y_at), s, offset=offset, fs=fs, color=color or text_color(role), **kw)


def bars(ax, labels, values, styles=None, bottoms=None, value_text=None, width=0.62, horizontal=False,
         fs=FS_LABEL, zorder=3):
    """Bar chart told apart by label and hatch as well as color: white bars with a colored
    edge and hatch (styles: roles or series indices, default 0, 1, 2, ...). `bottoms` makes
    floating bars (for a budget). Each bar is labeled with its value (value_text: strings,
    default fmt(value)) at its end. Returns the bar container.
    Example: bars(ax, ["plan A", "plan B"], [5.21, 4.89])"""
    n = len(values)
    styles = list(range(n)) if styles is None else styles
    bottoms = [0.0] * n if bottoms is None else bottoms
    value_text = [fmt(v) for v in values] if value_text is None else value_text
    pos = np.arange(n)
    colors = [line_kw(s)["color"] for s in styles]
    hatch = [HATCHES[(s if isinstance(s, int) else SEQUENCE.index(s)) % len(HATCHES)] for s in styles]
    if horizontal:
        cont = ax.barh(pos, values, height=width, left=bottoms, color="white", edgecolor=colors, lw=1.5, zorder=zorder)
    else:
        cont = ax.bar(pos, values, width=width, bottom=bottoms, color="white", edgecolor=colors, lw=1.5, zorder=zorder)
    for b, h, c in zip(cont.patches, hatch, colors):
        b.set_hatch(h)
        b.set_edgecolor(c)
    for i, (v, b0, s) in enumerate(zip(values, bottoms, value_text)):
        end = b0 + v
        if horizontal:
            text(ax, (end, pos[i]), s, direction=0.0 if v >= 0 else 180.0, dist=4, fs=fs, backing=False)
        else:
            text(ax, (pos[i], end), s, direction=90.0 if v >= 0 else -90.0, dist=3, fs=fs, backing=False)
    if horizontal:
        ax.set_yticks(pos, labels)
    else:
        ax.set_xticks(pos, labels)
    return cont


# ===================================================================== the layout gate
def _contrast(c, bg=(1.0, 1.0, 1.0)):
    from matplotlib.colors import to_rgb

    def lum(rgb):
        v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    a, b = lum(to_rgb(c)), lum(bg)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def contrast_ratio(color, background="white"):
    """WCAG contrast ratio of a color against a background (default white).
    Example: contrast_ratio(BLUE) -> 5.19"""
    from matplotlib.colors import to_rgb
    return _contrast(color, to_rgb(background))


def _densify(xy, step=1.5):
    """Display-space polyline -> points no more than `step` px apart (NaN breaks kept out)."""
    xy = np.asarray(xy, dtype=float)
    xy = xy[np.all(np.isfinite(xy), axis=1)] if len(xy) else xy
    if len(xy) < 2:
        return xy
    seg = np.diff(xy, axis=0)
    n = np.maximum(1, np.ceil(np.hypot(seg[:, 0], seg[:, 1]) / step).astype(int))
    pts = [xy[:-1][i] + np.outer(np.arange(k) / k, seg[i]) for i, k in enumerate(n)]
    return np.vstack(pts + [xy[-1:]])


def _min_dist(A, B):
    """Smallest distance from each point of A (n, 2) to the point set B (m, 2), display px."""
    A, B = np.asarray(A, dtype=float), np.asarray(B, dtype=float)
    if len(A) == 0 or len(B) == 0:
        return np.full(len(A), np.inf)
    out = np.empty(len(A))
    for i in range(0, len(A), 256):
        d = A[i:i + 256, None, :] - B[None, :, :]
        out[i:i + 256] = np.sqrt(np.min(np.einsum("ijk,ijk->ij", d, d), axis=1))
    return out


def _group(artist):
    """The drawing group of an artist (gid "grp:..."): the parts of one dimension, for example."""
    g = artist.get_gid()
    return g if isinstance(g, str) and g.startswith("grp:") else None


def _head_tip(head):
    """The tip of an arrowhead triangle (display px), for messages: the corner opposite its
    shortest side (a head is longer than it is wide), whatever the order of its vertices."""
    v = np.asarray(head.vertices, dtype=float)[:3]
    sides = [np.hypot(*(v[(i + 1) % 3] - v[(i + 2) % 3])) for i in range(3)]
    return v[int(np.argmin(sides))]


def _head_samples(head, px_per_pt, apex_free=2.5):
    """Points that fill an arrowhead triangle (display px), leaving out the part within
    `apex_free` points of its tip: the tip may end on the line it points at."""
    v = np.asarray(head.vertices, dtype=float)[:3]
    apex, c1, c2 = v[1], v[0], v[2]
    pts = []
    for s in np.linspace(0.0, 1.0, 15):
        for t in np.linspace(0.0, 1.0, 9):
            pts.append(apex + s * ((1 - t) * (c1 - apex) + t * (c2 - apex)))
    pts = np.array(pts)
    return pts[np.hypot(*(pts - apex).T) > apex_free * px_per_pt], apex, 0.5 * (c1 + c2)


LABEL_CLEAR = 0.5            # pt of clear space between a label (its backing box) and any mark


def _region_contains(art, target):
    """True when `art` outlines a filled region (a patch with a face, a globe outline, or a line
    tagged gid "edge", the edge of a filled band or plane) that contains the display point
    `target`. Orbit lines never count."""
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    if art is None or target is None:
        return False
    if isinstance(art, Patch):
        path = art.get_transform().transform_path(art.get_path())
    elif isinstance(art, Line2D) and art.get_gid() == "edge":
        xy = art.get_transform().transform(np.c_[art.get_xdata(), art.get_ydata()].astype(float))
        from matplotlib.path import Path as _P
        path = _P(xy)
    else:
        return False
    return bool(path.contains_point(target))


def on_part(artist, part):
    """Mark a detail line or shape as drawn on `part` (a patch: the fuselage a window is on, the
    stage a hidden tank is in). A leader whose end lies inside `part` may cross the detail, as it
    may cross the part's own outline; for every other leader the detail is an obstacle like any
    line. Returns the artist. Example: on_part(ax.plot(x, y)[0], fuselage_patch)"""
    artist._on_part = part
    return artist


def opaque(patch):
    """Mark a filled patch as opaque for the layout gate: lines, outlines and arrows drawn under
    it (lower zorder) are hidden where it covers them and are not marks there. Hardware outlines
    and boxes use it. Returns the patch. Example: opaque(ax.add_patch(Polygon(xy, fc="white")))"""
    patch._occludes = True
    return patch


def _occlude(fig, marks, px):
    """Remove from the marks the points hidden under an opaque() patch drawn above them."""
    from matplotlib.patches import Patch
    for ax in fig.axes:
        for pa in ax.patches:
            if not (getattr(pa, "_occludes", False) and isinstance(pa, Patch) and pa.get_visible()):
                continue
            if pa.get_facecolor()[3] < 0.99:
                continue
            path = pa.get_transform().transform_path(pa.get_path())
            edge = np.vstack([_densify(p, 1.0) for p in path.to_polygons(closed_only=False) if len(p) > 1] or
                             [np.zeros((0, 2))])
            for m in marks:
                if m["z"] >= pa.get_zorder() or len(m["pts"]) == 0 or m["src"] == id(pa):
                    continue
                inside = path.contains_points(m["pts"])
                if inside.any():
                    near = _min_dist(m["pts"][inside], edge) <= 1.0 * px if len(edge) else np.zeros(inside.sum(), bool)
                    keep = ~inside
                    keep[np.flatnonzero(inside)[near]] = True          # where it meets the edge it shows
                    m["pts"] = m["pts"][keep]


def _diagram_problems(fig, marks, texts, px):
    """Gate checks for block diagrams, matrices and labeled hardware, applied only to the artists
    that the diagram helpers mark (so no figure drawn without them is affected):
      - a routed arrow (route(): a Line2D with `_route` = (source, target)) crosses no line,
        outline, arrow, marker or other routed arrow on its way; only its own head and, within
        3 pt of its ends, its source and target boxes are exempt; it starts on the source's edge
        and its tip ends on the target's edge (within 1 pt);
      - a box (a patch with `_box`) keeps 2 pt clear of every other box, except boxes of the same
        group (the cells of one matrix);
      - text set in a box (`_in_box` = the patch) lies inside it with at least 2 pt of padding.
    Returns a list of problems."""
    from matplotlib.lines import Line2D
    probs = []
    by_id = {}
    for ax in fig.axes:
        for a in list(ax.lines) + list(ax.patches):
            by_id[id(a)] = a
    # routed arrows
    for ax in fig.axes:
        for ln in ax.lines:
            ends = getattr(ln, "_route", None)
            if ends is None or not ln.get_visible():
                continue
            xy = ln.get_transform().transform(np.c_[ln.get_xdata(), ln.get_ydata()].astype(float))
            pts = _densify(xy, 1.0)
            if len(pts) < 2:
                continue
            start, tip = xy[0], xy[-1]
            head_len = getattr(ln, "_head_len", 9.0) * px
            lrad = 0.5 * ln.get_linewidth() * px
            src, dst = ends
            rides = {id(ln)}
            for pa in ax.patches:
                if id(ln) in getattr(pa, "_rides", ()):
                    rides.add(id(pa))
            d_start = np.hypot(*(pts - start).T)
            d_tip = np.hypot(*(pts - tip).T)
            body = d_tip > head_len + 1.0 * px               # the head is checked as an arrowhead
            for m in marks:
                if m["src"] in rides or len(m["pts"]) == 0:
                    continue
                sel = body.copy()
                if m["src"] == id(src):
                    sel &= d_start > 3.0 * px                   # it leaves its source box
                if m["src"] == id(dst):
                    sel &= d_tip > head_len + 3.0 * px          # it meets its target box
                q = pts[sel]
                if len(q) == 0:
                    continue
                dd = _min_dist(q, m["pts"])
                if np.any(dd < m["rad"] + lrad + 0.5):
                    p = ax.transData.inverted().transform(q[int(np.argmin(dd))])
                    probs.append(f"routed arrow crosses {m['what']} at data ({p[0]:.4g}, {p[1]:.4g})")
                    break
            for box, end, what in ((src, start, "starts"), (dst, tip, "ends")):
                if box is None:
                    continue
                path = box.get_transform().transform_path(box.get_path())
                edge = np.vstack([_densify(p, 0.5) for p in path.to_polygons(closed_only=False) if len(p) > 1])
                gap = float(_min_dist(np.asarray([end]), edge)[0]) / px
                if gap > 1.0:
                    p = ax.transData.inverted().transform(end)
                    probs.append(f"routed arrow {what} {gap:.1f} pt off its box edge at data ({p[0]:.4g}, {p[1]:.4g})")
    # boxes clear of each other
    boxes = [(pa, pa.get_window_extent()) for ax in fig.axes for pa in ax.patches
             if getattr(pa, "_box", False) is not False and pa.get_visible()]
    cl = 2.0 * px
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            (a, ba), (b, bb) = boxes[i], boxes[j]
            ga, gb = getattr(a, "_box", None), getattr(b, "_box", None)
            if ga is not None and ga is not True and ga == gb:
                continue
            if ba.x0 < bb.x1 + cl and bb.x0 < ba.x1 + cl and ba.y0 < bb.y1 + cl and bb.y0 < ba.y1 + cl:
                probs.append(f"boxes {getattr(a, '_name', '?')!r} and {getattr(b, '_name', '?')!r} are closer than 2 pt")
    # text inside its box, with padding
    pad = 2.0 * px
    for t, bb in texts:
        box = getattr(t, "_in_box", None)
        if box is None:
            continue
        e = box.get_window_extent()
        if not (bb.x0 >= e.x0 + pad and bb.x1 <= e.x1 - pad and bb.y0 >= e.y0 + pad and bb.y1 <= e.y1 - pad):
            probs.append(f"text {t.get_text()!r} does not fit inside its box with 2 pt of padding")
    return probs


def layout_problems(fig):
    """Check a drawn figure against FIGURE_STANDARD.md items 10, 11 and 17 and return a list of
    problems, in every axes (panel) of the figure:
      - a label (with its white backing box) that touches or crosses a line, an arrow, a marker,
        a body outline, an axes frame line or a tick mark, or another label;
      - a leader that crosses a line, an arrow, a marker, an outline or another label on its way
        (its last 7 pt, where it meets the point it names, are exempt; so is the outline of a
        filled region that contains that point: a body, a globe, a band or plane edge tagged
        gid "edge", a sector; never an orbit line; and the faint grid of a globe);
      - an arrowhead that lies on another line, arrow, marker or arrowhead (the tip may end on a
        line; only the arrowhead's own line, recorded with rides_on(), is exempt);
      - text below 10 pt; text with less than 4.5:1 contrast, or a line or mark with less than
        3:1, on white.
    Grid lines are exempt (decorative), and so is a dimension label placed on its line
    (label_side=0). The parts of one drawing group (gid "grp:...", for example a dimension)
    may touch each other. save_figure() runs it, then pixel_problems(), on every figure.
    Example: layout_problems(fig) -> []"""
    from matplotlib.patches import Patch, FancyArrowPatch as FAP
    from matplotlib.text import Text
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    px = fig.dpi / 72.0                                   # display px per point
    probs = []
    texts = []
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip() or t.axes is None and t.figure is None:
            continue
        bb = Text.get_window_extent(t, rend)          # the text alone, without an annotation's arrow
        if t.get_bbox_patch() is not None and t.get_bbox_patch().get_visible():
            bb = t.get_bbox_patch().get_window_extent(rend)     # with its white backing, which must not cut a line
        if bb.width < 1 or bb.height < 1:
            continue
        texts.append((t, bb))
        if t.get_fontsize() < 10:
            probs.append(f"text {t.get_text()!r} is {t.get_fontsize():g} pt (10 pt at least)")
        if _contrast(t.get_color()) < 4.5:
            probs.append(f"text {t.get_text()!r}: contrast {_contrast(t.get_color()):.2f}:1 (4.5:1 needed)")
    # what labels must stay clear of: lines, markers, arrows, outlines, frames, ticks (display px)
    marks = []                     # dict(pts, rad, z, what, src, grp)

    def add(pts, rad, z, what, src, grp=None, art=None):
        marks.append(dict(pts=np.asarray(pts, dtype=float).reshape(-1, 2), rad=rad, z=z, what=what, src=src, grp=grp,
                          art=art))
    heads, leaders, burns, connectors = [], [], [], []
    for ax in fig.axes:
        grid = set(ax.get_xgridlines()) | set(ax.get_ygridlines())
        clip = ax.bbox
        for ln in ax.lines:
            if ln in grid or not ln.get_visible():
                continue
            xy = ln.get_transform().transform(np.c_[ln.get_xdata(), ln.get_ydata()].astype(float))
            col = ln.get_color()
            if ln.get_linestyle() not in ("None", "", " ") and ln.get_linewidth() > 0:
                pts = _densify(xy)
                if ln.get_clip_on() and len(pts):
                    pts = pts[(pts[:, 0] >= clip.x0) & (pts[:, 0] <= clip.x1) & (pts[:, 1] >= clip.y0) & (pts[:, 1] <= clip.y1)]
                add(pts, 0.5 * ln.get_linewidth() * px, ln.get_zorder(),
                    "a connector line" if ln.get_gid() == "connector" else "a line", id(ln), _group(ln), art=ln)
                if ln.get_gid() == "connector":
                    connectors.append((ln, pts, ax))
                if _contrast(col) < 3.0:
                    probs.append(f"line of color {col}: contrast {_contrast(col):.2f}:1 (3:1 needed)")
            if ln.get_marker() not in ("None", None, "", " ") and ln.get_markersize() > 0:
                rad = 0.5 * ln.get_markersize() * px
                add(xy[np.all(np.isfinite(xy), axis=1)], rad, ln.get_zorder() + 0.5, "a marker", id(ln), _group(ln))
                mc = ln.get_markeredgecolor()
                if _contrast(mc) < 3.0 and _contrast(ln.get_markerfacecolor()) < 3.0:
                    probs.append(f"marker of color {mc}: contrast below 3:1")
        # the frame and the tick marks of a visible axes
        if ax.axison:
            for sp in ax.spines.values():
                if sp.get_visible() and sp.get_linewidth() > 0:
                    path = sp.get_transform().transform_path(sp.get_path())
                    for poly in path.to_polygons(closed_only=False):
                        add(_densify(poly), 0.5 * sp.get_linewidth() * px, sp.get_zorder(), "the axes frame", id(sp))
            for axis in (ax.xaxis, ax.yaxis):
                for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                    for tl in (tick.tick1line, tick.tick2line):
                        if not (tick.get_visible() and tl.get_visible()) or tl.get_markersize() <= 0:
                            continue
                        b = tl.get_window_extent(rend)
                        if b.width <= 0 and b.height <= 0:
                            continue
                        if not (clip.x0 - 1 <= 0.5 * (b.x0 + b.x1) <= clip.x1 + 1 and clip.y0 - 1 <= 0.5 * (b.y0 + b.y1) <= clip.y1 + 1):
                            continue                       # a tick outside the view is not drawn
                        add(_densify([(b.x0, b.y0), (b.x1, b.y0), (b.x1, b.y1), (b.x0, b.y1), (b.x0, b.y0)]), 0.0,
                            2.0, "a tick mark", id(tl))
        arrows = [t.arrow_patch for t in ax.texts if getattr(t, "arrow_patch", None) is not None]
        for a in arrows:
            a._gate_axes = ax
        for pa in list(ax.patches) + arrows:
            if not pa.get_visible():
                continue
            if isinstance(pa, FAP):
                path, fillable = pa._get_path_in_displaycoord()
                paths = path if isinstance(path, list) else [path]
                fills = fillable if isinstance(fillable, list) else [fillable] * len(paths)
                if pa.get_gid() in ("leader", "connector"):
                    for pth in paths:
                        pts_l = _densify(pth.vertices, 1.0)
                        (leaders if pa.get_gid() == "leader" else connectors).append((pa, pts_l, ax))
                        add(pts_l, 0.5 * pa.get_linewidth() * px, pa.get_zorder(),
                            "a leader" if pa.get_gid() == "leader" else "a connector line", id(pa))
                    continue
                if pa.get_gid() == "burn":
                    burns.append((pa, _densify(paths[0].vertices, 1.0), ax))
                for pth, fl in zip(paths, fills):
                    for poly in pth.to_polygons(closed_only=False):
                        add(_densify(poly), 0.5 * pa.get_linewidth() * px + 0.5, pa.get_zorder(),
                            "an arrowhead" if fl else "an arrow", id(pa), _group(pa))
                    if fl and len(pth.vertices) >= 3:
                        heads.append((pa, pth, ax))
                if _contrast(pa.get_edgecolor()) < 3.0:
                    probs.append(f"arrow of color {pa.get_edgecolor()}: contrast below 3:1")
            elif isinstance(pa, Patch) and pa.get_edgecolor()[3] > 0 and pa.get_linewidth() > 0:
                for poly in pa.get_transform().transform_path(pa.get_path()).to_polygons(closed_only=False):
                    add(_densify(poly), 0.5 * pa.get_linewidth() * px, pa.get_zorder(), "an outline", id(pa), _group(pa),
                        art=pa)
    # opaque discs (bodies, the globe) hide what is drawn under them. The disc comes from the
    # drawn path: get_transform() of a Circle already holds its center and radius.
    discs = []
    for ax in fig.axes:
        for pa in ax.patches:
            if isinstance(pa, Circle) and pa.get_visible() and pa.get_facecolor()[3] > 0.99:
                v = pa.get_transform().transform_path(pa.get_path()).vertices
                c = 0.5 * (v.min(axis=0) + v.max(axis=0))
                r = 0.25 * float(np.sum(v.max(axis=0) - v.min(axis=0)))
                discs.append((c, r - 0.5, pa.get_zorder()))
    for m in marks:
        for c, r, zd in discs:
            if zd > m["z"] and len(m["pts"]):
                m["pts"] = m["pts"][np.hypot(m["pts"][:, 0] - c[0], m["pts"][:, 1] - c[1]) > r]
    # opaque shapes marked with opaque() (hardware outlines, boxes) hide what lies under them, as
    # the discs do: a part drawn behind another is not a mark where it is hidden
    _occlude(fig, marks, px)
    # 1. labels against every mark
    for t, bb in texts:
        if t.get_gid() == "on-line" or t.axes is None:
            continue
        cl = LABEL_CLEAR * px                     # a label must keep this clear of every mark
        x0, y0, x1, y1 = bb.x0 - cl, bb.y0 - cl, bb.x1 + cl, bb.y1 + cl
        own = id(getattr(t, "arrow_patch", None))
        for m in marks:
            pts, rad = m["pts"], m["rad"]
            if len(pts) == 0 or m["src"] == own:
                continue
            inside = ((pts[:, 0] > x0 - rad) & (pts[:, 0] < x1 + rad) & (pts[:, 1] > y0 - rad) & (pts[:, 1] < y1 + rad))
            if inside.any():
                q = t.axes.transData.inverted().transform(pts[np.argmax(inside)])
                probs.append(f"label {t.get_text()!r} touches {m['what']} at data ({q[0]:.4g}, {q[1]:.4g})")
                break
    # 2. labels against labels
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            (ta, a), (tb, b) = texts[i], texts[j]
            if a.x0 < b.x1 - 0.5 and b.x0 < a.x1 - 0.5 and a.y0 < b.y1 - 0.5 and b.y0 < a.y1 - 0.5:
                probs.append(f"labels {ta.get_text()!r} and {tb.get_text()!r} overlap")
    # 3. leaders: clear of every mark and every other label on their way
    owner = {id(getattr(t, "arrow_patch", None)): t for t, _ in texts}
    for pa, pts, lax in leaders:
        t = owner.get(id(pa))
        name = repr(t.get_text()) if t is not None else "?"
        target = pa._posA_posB[1] if getattr(pa, "_posA_posB", None) else None
        if t is not None and hasattr(t, "xy"):
            target = t.get_transform().transform(t.xy) if t.xycoords == "data" else target
        if target is not None:
            pts = pts[np.hypot(*(pts - np.asarray(target)).T) > 7.0 * px]       # where it meets its point
        if t is not None:
            own_bb = dict(texts).get(t)
            if own_bb is not None:
                pts = pts[~((pts[:, 0] > own_bb.x0 - 1.5 * px) & (pts[:, 0] < own_bb.x1 + 1.5 * px)
                            & (pts[:, 1] > own_bb.y0 - 1.5 * px) & (pts[:, 1] < own_bb.y1 + 1.5 * px))]
        if len(pts) == 0:
            continue
        lrad = 0.5 * pa.get_linewidth() * px
        for m in marks:
            if len(m["pts"]) == 0 or m["src"] == id(pa):
                continue
            if _region_contains(m["art"], target):
                continue                     # a leader pointing into a filled region crosses its outline
            if _region_contains(getattr(m["art"], "_on_part", None), target):
                continue                     # a detail drawn on a part (a window, a hidden tank) that holds the end
            if m["art"] is not None and m["art"].get_gid() == "globe-grid":
                continue                     # the faint grid of a globe, like the grid of a plot
            d = _min_dist(pts, m["pts"])
            if np.any(d < m["rad"] + lrad + 0.5):
                q = lax.transData.inverted().transform(pts[int(np.argmin(d))])
                probs.append(f"leader of {name} crosses {m['what']} at data ({q[0]:.4g}, {q[1]:.4g})")
                break
        for tb, b in texts:
            if tb is t:
                continue
            if np.any((pts[:, 0] > b.x0) & (pts[:, 0] < b.x1) & (pts[:, 1] > b.y0) & (pts[:, 1] < b.y1)):
                probs.append(f"leader of {name} crosses the label {tb.get_text()!r}")
    # 3b. connector lines (zoom lines between panels): they cross no line, arrow, leader or label;
    # only the artists they are drawn to meet (connects()) may touch them, and only at their ends
    for ca, pts, cax in connectors:
        if len(pts) < 2:
            continue
        touch = getattr(ca, "_touches", ())
        crad = 0.5 * ca.get_linewidth() * px
        for m in marks:
            if m["src"] == id(ca) or len(m["pts"]) == 0:
                continue
            q_pts = pts
            if m["src"] in touch:                 # its own end circles or frames: only the ends may meet them
                q_pts = pts[(np.hypot(*(pts - pts[0]).T) > 15.0 * px) & (np.hypot(*(pts - pts[-1]).T) > 15.0 * px)]
                if len(q_pts) == 0:
                    continue                       # (a tangent stays near its circle for some points)
            d = _min_dist(q_pts, m["pts"])
            if np.any(d < m["rad"] + crad + 0.3):
                q = cax.transData.inverted().transform(q_pts[int(np.argmin(d))])
                col = m["art"].get_edgecolor() if hasattr(m["art"], "get_edgecolor") and not hasattr(m["art"], "get_xdata") \
                    else (m["art"].get_color() if m["art"] is not None else "")
                from matplotlib.colors import to_hex
                col = f" {to_hex(col)}" if col is not None and len(str(col)) else ""
                probs.append(f"connector line crosses {m['what']}{col} at data ({q[0]:.4g}, {q[1]:.4g})")   # every one
        for tb, b in texts:
            if np.any((pts[:, 0] > b.x0) & (pts[:, 0] < b.x1) & (pts[:, 1] > b.y0) & (pts[:, 1] < b.y1)):
                probs.append(f"connector line crosses the label {tb.get_text()!r}")
    # 4. burn arrows beside the path, never on it (their first 2 pt may touch the burn dot)
    for pa, pts, bax in burns:
        pts = pts[np.hypot(*(pts - pts[0]).T) > 2.0 * px]
        brad = 0.5 * pa.get_linewidth() * px
        for m in marks:
            if m["src"] == id(pa) or m["what"] == "a marker" or len(m["pts"]) == 0 or len(pts) == 0:
                continue
            d = _min_dist(pts, m["pts"])
            if np.any(d < m["rad"] + brad + 0.5):
                q = bax.transData.inverted().transform(pts[int(np.argmin(d))])
                probs.append(f"burn arrow lies on {m['what']} at data ({q[0]:.4g}, {q[1]:.4g}): draw it beside the path")
                break
    # 5. arrowheads: clear of other lines, arrows, markers and arrowheads (not of the line they ride on)
    for pa, head, hax in heads:
        samp, apex, base = _head_samples(head, px)
        if len(samp) == 0:
            continue
        for m in marks:
            if m["src"] == id(pa) or len(m["pts"]) == 0 or (m["grp"] is not None and m["grp"] == _group(pa)):
                continue
            if (m["grp"] or "").startswith("grp:dim") and (_group(pa) or "").startswith("grp:dim"):
                continue                                       # chained dimensions share an end tick
            if m["art"] is not None and m["art"].get_gid() == "globe-grid":
                continue                                       # the faint grid of a globe, under an orbit's arrowhead
            if m["src"] in getattr(pa, "_rides", ()):
                continue                                       # the arrowhead's own line (its orbit, track or arc)
            d = _min_dist(samp, m["pts"])
            if np.any(d < m["rad"] + 0.5):
                q = hax.transData.inverted().transform(_head_tip(head))     # the position of the tip
                probs.append(f"arrowhead at data ({q[0]:.4g}, {q[1]:.4g}) lies on {m['what']}")
                break
    # 6. diagrams: routed arrows, boxes and the text set in a box (only artists the diagram helpers mark)
    probs += _diagram_problems(fig, marks, texts, px)
    return probs


PIXEL_DPI = 216.0              # 3 px per point, as in the figure review


def _blobs(mask, min_cells):
    """Connected groups (8-neighbors) of a mask downsampled to 1 cell per point (3 x 3 px)."""
    h, w = mask.shape
    m3 = mask[:h // 3 * 3, :w // 3 * 3].reshape(h // 3, 3, w // 3, 3).any(axis=(1, 3))
    seen = np.zeros_like(m3, dtype=bool)
    out = []
    for y0, x0 in zip(*np.nonzero(m3)):
        if seen[y0, x0]:
            continue
        stack, cells = [(y0, x0)], []
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            cells.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < m3.shape[0] and 0 <= xx < m3.shape[1] and m3[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        stack.append((yy, xx))
        if len(cells) >= min_cells:
            c = np.array(cells)
            out.append((len(cells), 3.0 * c[:, 1].mean() + 1.5, 3.0 * c[:, 0].mean() + 1.5))
    return out


def pixel_problems(fig, dpi=PIXEL_DPI, min_cells=3):
    """The pixel test of the gate: render the figure at 3 px per point with
    and without its text (glyphs and backing boxes), grid lines hidden in both, and report
      - line ink (a dark or colored pixel without the text) that a label's white backing turns white;
      - a light fill (a body, globe, plane or band) that a white backing covers: on a fill use a
        backing of the fill's color (text(..., backing=<color>)) or none.
    A group of `min_cells` square points or more is a problem. A dimension label placed on its
    line (label_side=0) is exempt. Example: pixel_problems(fig) -> []"""
    from matplotlib.text import Text
    texts = [t for t in fig.findobj(Text) if t.get_visible() and t.get_text().strip() and t.get_gid() != "on-line"]
    grids = [g for ax in fig.axes for g in ax.get_xgridlines() + ax.get_ygridlines() if g.get_visible()]
    old_dpi = fig.dpi
    saved = [(t, t.get_color(), t.get_bbox_patch().get_visible() if t.get_bbox_patch() is not None else None)
             for t in texts]
    try:
        for g in grids:
            g.set_visible(False)
        fig.set_dpi(dpi)
        fig.canvas.draw()
        A = np.asarray(fig.canvas.buffer_rgba())[..., :3].astype(int).copy()
        boxes = []
        rend = fig.canvas.get_renderer()
        for t in texts:
            bp = t.get_bbox_patch()
            bb = bp.get_window_extent(rend) if bp is not None and bp.get_visible() else Text.get_window_extent(t, rend)
            boxes.append((t, bb))
            t.set_color((0, 0, 0, 0))
            if bp is not None:
                bp.set_visible(False)
        fig.canvas.draw()
        B = np.asarray(fig.canvas.buffer_rgba())[..., :3].astype(int).copy()
    finally:
        for t, c, bv in saved:
            t.set_color(c)
            if bv is not None:
                t.get_bbox_patch().set_visible(bv)
        for g in grids:
            g.set_visible(True)
        fig.set_dpi(old_dpi)
        fig.canvas.draw()
    H = A.shape[0]
    white = A.min(axis=2) > 245
    ink = (B.min(axis=2) < 170) | ((B.max(axis=2) - B.min(axis=2)) > 80)
    fill = (~ink) & (B.min(axis=2) <= 240)

    def who(x, y):
        yd = H - y                                         # display y runs up
        for t, bb in boxes:
            if bb.x0 - 3 <= x <= bb.x1 + 3 and bb.y0 - 3 <= yd <= bb.y1 + 3:
                return repr(t.get_text())
        return "a label"
    probs = []
    for n, x, y in _blobs(white & ink, min_cells):
        probs.append(f"pixel test: {who(x, y)} hides {n} pt² of line ink")
    for n, x, y in _blobs(white & fill, min_cells):
        probs.append(f"pixel test: the white backing of {who(x, y)} shows over a fill ({n} pt²)")
    return probs


FONT_FAMILY = "Arial, Helvetica, sans-serif"


def _svg_fonts(svg_text):
    """Every font-family in the SVG, plain labels and math alike, becomes FONT_FAMILY, so a device
    without Arial falls back to a sans-serif font, never to a serif."""
    return re.sub(r"font-family: ?(?:'[^']*'|\"[^\"]*\"|[A-Za-z][\w -]*)(?: ?, ?(?:'[^']*'|\"[^\"]*\"|[A-Za-z][\w -]*))*",
                  "font-family: " + FONT_FAMILY, svg_text)


def svg_problems(svg_text):
    """Problems in an SVG written by save_figure(): a glyph in a font other than Arial (STIX and
    DejaVu fallbacks included), a text element without the font-family and its fallbacks, text
    smaller than 10 pt (single-letter sub- and superscripts inside a math label are allowed), or
    a subscript made of a word, or the infinity sign, smaller than 10.5 pt (it must read at 10 pt
    on the page). Example: svg_problems(svg_path.read_text()) -> []"""
    probs = []
    for fam in sorted(set(re.findall(r"font-family: ?([^;\"]+)", svg_text))):
        if fam.strip() != FONT_FAMILY:
            probs.append(f"font-family {fam.strip()!r}: every text must read {FONT_FAMILY!r}")
    for bad in ("STIX", "DejaVu Sans Mono", "cmr10", "cmmi10"):
        if bad in svg_text:
            probs.append(f"a glyph is set in {bad}, not Arial")
    for m in re.finditer(r"<text\b(.*?)</text>", svg_text, re.S):
        body = m.group(0)
        styled = re.findall(r"<(?:text|tspan)\b[^>]*style=\"([^\"]*)\"[^>]*>([^<]*)", body)
        for style, chars in styled:
            if chars.strip() and "font-family" not in style and "font-family" not in m.group(1):
                probs.append(f"text {chars!r} has no font-family")
        sizes = [float(s) for s in re.findall(r"font(?:-size)?:[^;\"]*?([\d.]+)px", body)]
        plain = re.sub(r"<[^>]+>", "", body.split(">", 1)[1]).strip()
        if sizes and max(sizes) < 10.0:
            probs.append(f"text {plain!r} is {max(sizes):g} pt, below 10 pt")
        if sizes:
            main = max(sizes)
            runs = []                                   # runs of glyphs set smaller than the main size
            for size, chars in re.findall(r"<tspan\b[^>]*font-size: ([\d.]+)px[^>]*>([^<]*)", body):
                size = float(size)
                if size < main and runs and runs[-1][0] == size:
                    runs[-1][1] += chars
                elif size < main:
                    runs.append([size, chars])
                else:
                    runs.append([size, None])
            for size, chars in runs:
                if chars and (re.search(r"[A-Za-z]{2,}", chars) or "∞" in chars) and size < 10.5:
                    probs.append(f"subscript {chars!r} of {plain!r} is {size:g} pt (10.5 pt at least for a word or ∞)")
    return probs


def close_to(a, b, tol, what, rel=False):
    """Assert |a - b| <= tol with a message naming the check; with rel=True the tolerance is
    relative, |a - b| <= tol |b|. Example: close_to(rp, 7078.0, 1e-6, "rp");
    close_to(drawn_area, 124.6, 0.002, "wing area", rel=True)"""
    if rel:
        assert abs(a - b) <= tol * abs(b), f"{what}: {a!r} vs {b!r} (relative tolerance {tol})"
    else:
        assert abs(a - b) <= tol, f"{what}: {a!r} vs {b!r} (tolerance {tol})"


# ===================================================================== a chapter: record and save
class Chapter:
    """The record of printed values and the figure saver of one chapter.

    `number` is the chapter number, `pages` maps page tags to page file stems
    ({"p21": "orbit-properties"}), `package` is the folder of the chapter's code
    (scripts/chapter_N), which holds values.json. Figures are written to
    notes/chapter-N/figures/ and must be named "p<N><page>-<name>".
    Example: CH = Chapter(1, {"p14": "standard-atmosphere"}, Path(__file__).resolve().parent)"""

    def __init__(self, number, pages, package):
        self.number = int(number)
        self.PAGES = dict(pages)
        self.VALUES = {}                          # page stem -> {key: text}
        self.VALUES_FILE = Path(package) / "values.json"
        self.WRITTEN = set()                      # figure names written in this run
        self._name = re.compile(rf"p{self.number}\d-[a-z0-9]+(?:-[a-z0-9]+)*")
        self.FIGURES = NOTES / f"chapter-{self.number}" / "figures"

    def record(self, page, key, text):
        """Record that the string `text` is printed on `page` (a tag such as "p21" or the page file
        stem) and return it. check_values.py then requires it on the page. Record the number
        only, as printed ("7.669", not "7.669 km/s"). Example: v = record("p21", "vp", fmt(vp))"""
        if not isinstance(text, str):
            raise TypeError(f"record({page!r}, {key!r}): text must be a string; format it with fmt()")
        stem = self.PAGES.get(page, page)
        old = self.VALUES.setdefault(stem, {}).get(key)
        if old is not None and old != text:
            raise ValueError(f"record: {stem}:{key} recorded twice with different text: {old!r} and {text!r}")
        self.VALUES[stem][key] = text
        return text

    def write_values(self, only=None):
        """Write values.json of the chapter. With only=None the file holds exactly what was
        recorded in this run; with a list of page stems (or tags), those pages are replaced and
        the other pages already in the file are kept. Example: write_values()"""
        data = {}
        if only is not None:
            stems = {self.PAGES.get(p, p) for p in only}
            if self.VALUES_FILE.exists():
                data = {k: v for k, v in json.loads(self.VALUES_FILE.read_text(encoding="utf-8")).items()
                        if k not in stems}
            data.update({k: v for k, v in self.VALUES.items() if k in stems})
        else:
            data = dict(self.VALUES)
        data = {k: dict(sorted(v.items())) for k, v in sorted(data.items())}
        self.VALUES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {self.VALUES_FILE.relative_to(SCRIPTS.parent)} ({sum(len(v) for v in data.values())} values)")

    def save_figure(self, fig, name, allow=()):
        """Save notes/chapter-N/figures/<name>.svg through make_figures.save() (live text, Arial,
        deterministic; PNG copy when FIG_PREVIEW is set). Before saving, layout_problems() checks
        the drawing (labels, leaders and arrowheads clear of lines, frames, ticks, marks and other
        labels; sizes; contrast) and pixel_problems() renders it with and without its text to find
        any line a label's backing box hides and any backing box over a fill. After saving, every
        font-family is set to Arial with its fallbacks and the SVG is checked (every glyph in Arial,
        no text below 10 pt, word subscripts readable). Any problem stops the run, except those
        whose text contains one of the strings in `allow` (give the reason in a comment next to
        it). With FIG_LAYOUT=warn in the environment the problems are printed and the figure is
        saved anyway (draft mode). The name starts with the page tag: "p21-ellipse-geometry".
        Example: save_figure(fig, "p21-ellipse-geometry")"""
        n = self.number
        if not self._name.fullmatch(name):
            raise ValueError(f"figure name {name!r}: use <tag>-<name> in lower case, e.g. p{n}1-ellipse-geometry")
        w = fig.get_size_inches()[0]
        if w > 7.5:
            print(f"note: {name} is {w:.1f} in wide; the usual width is {FIG_WIDTH} in")
        found = layout_problems(fig) + pixel_problems(fig)
        lay = [p for p in found if not any(a in p for a in allow)]
        if lay and os.environ.get("FIG_LAYOUT") == "warn":       # draft mode: report and save anyway
            print(f"   LAYOUT {name}:\n     " + "\n     ".join(lay))
        elif lay:
            plt.close(fig)
            raise AssertionError(f"{name}: " + "; ".join(lay))
        save(fig, name, chapter=n)
        self.WRITTEN.add(name)
        path = NOTES / f"chapter-{n}" / "figures" / f"{name}.svg"
        raw = path.read_text(encoding="utf-8")
        probs = [f"glyph {g!r} set in {fam}, not Arial (write the character, e.g. ° not ^\\circ, √ not \\sqrt)"
                 for fam, g in re.findall(r"font-family: ?'([^']+)'[^>]*>([^<]*)<", raw) if fam != "Arial"]
        svg = _svg_fonts(raw)
        path.write_text(svg, encoding="utf-8")
        probs += svg_problems(svg)
        if probs and os.environ.get("FIG_LAYOUT") == "warn":
            print(f"   SVG {name}:\n     " + "\n     ".join(probs))
        elif probs:
            raise AssertionError(f"{name}.svg: " + "; ".join(probs))
        m = re.search(r'<svg[^>]*width="([\d.]+)pt" height="([\d.]+)pt"', svg)
        if m:
            w_in, h_in = float(m.group(1)) / 72.0, float(m.group(2)) / 72.0
            pct = int(min(100, max(40, 5 * round(w_in / FIG_WIDTH * 85 / 5))))
            print(f"   {name}.svg: {w_in:.2f} x {h_in:.2f} in; :width: {pct}% shows its text at the size of the body text")



# ===================================================================== unit checks
if __name__ == "__main__":
    from matplotlib.patches import Rectangle

    # fmt: significant figures, integer digits never rounded away, half up, commas, trailing zeros kept
    cases = [((26578.3,), "26,578"), ((7.66912,), "7.669"), ((0.264786,), "0.2648"), ((105.4, 3), "105"),
             ((105.4,), "105.4"), ((5828.5,), "5,829"), ((2.4, 3), "2.40"), ((9.99996,), "10.00"),
             ((-0.04512, 2), "-0.045"), ((1234567.0,), "1,234,567"), ((0.0,), "0.000"), ((0.5, 1), "0.5")]
    for args, want in cases:
        assert fmt(*args) == want, (args, fmt(*args), want)
    assert fmt_dec(5828.46, 1) == "5,828.5" and fmt_dec(0.125, 2) == "0.13"
    assert fmt_sci(1.327e11) == "1.327 \\times 10^{11}"
    close_to(contrast_ratio("#767676"), 4.54, 0.01, "gray on white")

    def fresh():
        fig, ax = new_axes(4.0, 3.0)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7.5)
        return fig, ax

    # the gate sees a label on a line, and passes it once moved clear
    fig, ax = fresh()
    ax.plot([0, 10], [3, 3], color=INK, lw=1.5)
    text(ax, (5, 3), "on the line")
    assert any("touches a line" in p for p in layout_problems(fig)), "label on a line not caught"
    plt.close(fig)
    fig, ax = fresh()
    ax.plot([0, 10], [3, 3], color=INK, lw=1.5)
    text(ax, (5, 3), "clear", direction=90, dist=6)
    assert layout_problems(fig) == [], layout_problems(fig)
    plt.close(fig)

    # an opaque() shape hides the line under it: a label over the hidden part is clear of it
    for hide in (False, True):
        fig, ax = fresh()
        ax.plot([0, 10], [3, 3], color=INK, lw=1.5, zorder=2)
        r = ax.add_patch(Rectangle((3, 1.5), 4, 3, fc="white", ec=INK, lw=1.2, zorder=3))
        if hide:
            opaque(r)
        text(ax, (5, 3), "inside", backing=False, zorder=5)
        got = [p for p in layout_problems(fig) if "inside" in p]
        assert bool(got) != hide, (hide, got)
        plt.close(fig)

    # routed arrows: one between two boxes passes; one through a third box is caught; one that stops
    # short of its box is caught
    def two_boxes(ax):
        a = ax.add_patch(opaque(Rectangle((0.5, 3), 2, 1.5, fc="white", ec=INK, lw=1.2, zorder=4)))
        b = ax.add_patch(opaque(Rectangle((7.5, 3), 2, 1.5, fc="white", ec=INK, lw=1.2, zorder=4)))
        a._box = b._box = None
        return a, b

    for case in ("clean", "through", "short"):
        fig, ax = fresh()
        a, b = two_boxes(ax)
        if case == "through":
            c = ax.add_patch(opaque(Rectangle((4, 3), 1.5, 1.5, fc="white", ec=INK, lw=1.2, zorder=4)))
            c._box = None
        end = 7.5 if case != "short" else 7.0
        ln = ax.plot([2.5, end], [3.75, 3.75], color=INK, lw=1.4, zorder=3)[0]
        ln._route = (a, b)
        rides_on(arrow(ax, (end - 0.5, 3.75), (end, 3.75), lw=1.4, zorder=3.1), ln)
        probs = [p for p in layout_problems(fig) if "routed" in p]
        if case == "clean":
            assert probs == [], probs
        elif case == "through":
            assert any("crosses" in p for p in probs), probs
        else:
            assert any("off its box edge" in p for p in probs), probs
        plt.close(fig)

    # text set in a box must fit with padding; boxes keep 2 pt apart unless in one group
    fig, ax = fresh()
    bx = ax.add_patch(opaque(Rectangle((4, 3), 1.0, 0.6, fc="white", ec=INK, lw=1.2, zorder=4)))
    bx._box = None
    t = ax.text(4.5, 3.3, "much too long for its box", ha="center", va="center", zorder=5)
    t._in_box = bx
    assert any("does not fit inside its box" in p for p in layout_problems(fig))
    plt.close(fig)
    fig, ax = fresh()
    p1 = ax.add_patch(Rectangle((1, 1), 2, 2, fc="white", ec=INK, zorder=4))
    p2 = ax.add_patch(Rectangle((3, 1), 2, 2, fc="white", ec=INK, zorder=4))
    p1._box = p2._box = None
    assert any("closer than 2 pt" in p for p in layout_problems(fig))
    p1._box = p2._box = "cells"
    assert not any("closer than 2 pt" in p for p in layout_problems(fig))
    plt.close(fig)
    # a detail drawn on a part (on_part): a leader that ends in the part may cross it, another may not
    for into in (True, False):
        fig, ax = fresh()
        body = opaque(ax.add_patch(Rectangle((2, 2), 6, 3, fc="white", ec=INK, lw=1.5, zorder=3)))
        door = on_part(ax.add_patch(Rectangle((4.5, 2.4), 1.0, 2.0, fc="none", ec=INK, lw=0.7, zorder=3.2)), body)
        tgt = (5.0, 3.0) if into else (5.0, 1.0)
        an = callout(ax, tgt, "a part", at=(5.0, 6.8))
        got = [p for p in layout_problems(fig) if "leader" in p and "outline" in p]
        if into:
            assert got == [], got
        else:
            assert got, "a leader that ends outside the part must not cross its detail or outline"
        plt.close(fig)
    print("figkit.py: all unit checks passed (fmt, contrast, label gate, occlusion, routed arrows, boxes, details)")
