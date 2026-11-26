"""The figure look of Chapter 5, Aircraft Performance and Propulsion: one look for each role.

Every Chapter 5 figure draws its curves, bands, markers and force diagrams with these helpers, so
that the same thing looks the same on every page (FIGURE_STANDARD points 16, 21 and 30):

| Role | Look | Helper |
|---|---|---|
| Required (T_R, P_R) | solid, thick; black at the first condition | `required_kw(cond)` |
| Available (T_A, P_A) | dashed, thick, the color of its required curve | `available_kw(cond)` |
| A second (third) condition: an altitude, one engine out | blue (vermilion), with open triangles (inverted triangles) spaced along each curve, so it reads in grayscale | `COND_COLOR`, `cond_marks()` |
| Parasite and induced parts | thin blue dashed and thin vermilion dotted, the colors of page 3.3 | `part_kw("parasite")`, `part_kw("induced")` |
| Minimum of a curve | filled circle, labeled with value and speed | `mark_minimum()` |
| Tangent from the origin and its point | thin dashed line from a marked origin; open square | `tangent_from_origin()` |
| Crossing that sets a limit (maximum speed, ceiling) | filled diamond with a thin dashed drop line | `mark_limit()` |
| Below the stall speed | gray band "below stall" | `stall_band()` |
| Past the jet's Mach limit | gray band "wave drag: the polar no longer holds"; curves thin inside it, no computed point | `mach_band()`, `draw_curve(x_valid=)` |
| Jet and propeller aircraft | one panel each, the panel title names the aircraft | `panel_title()` |
| Constraint lines | one look per requirement, named on the line | `CONSTRAINT_STYLE`, `constraint_line()` |
| Forces on the aircraft | Chapter 1's force arrows on the 737-800 outline, to one scale, asserted in balance | `level_forces()`, `climb_forces()` |
| The weight split along and across the path | as page 4.2's flight-path figure | `weight_split()` |
| Rate of climb as the vertical part of the speed | velocity arrows of Chapter 1 | `velocity_triangle()` |

Gray bands use the fill of page 3.3's drag figure (#E6E6E6, black text 16:1). Data plots use
figkit's `data_axes`; force diagrams use equal-aspect axes (`new_axes` or `canvas`).
"""
import math

import numpy as np

from chapter_1.style import (INK, SERIES, STEEL, GRAY, HIGHLIGHT, LW_THIN, FS_LABEL, FS_SMALL,  # noqa: F401
                             text, kind_arrow, line_kw, close_to, rides_on, angle_arc)
from chapter_3.drawing3 import unit, angle_mark

# ===================================================================== colors and widths
BAND_FILL = "#E6E6E6"                         # stall and wave-drag bands (as page 3.3)
COND_COLOR = [INK, SERIES[0], SERIES[1]]      # black, blue #0072B2, vermilion #D55E00
COND_TEXT = [INK, SERIES[0], "#B34E00"]       # label colors, 4.5:1 or more on white
COND_MARK = [None, "^", "v"]                  # open markers spaced along a second or third condition
LW_CURVE = 2.2                                # required and available curves
LW_PART = 1.4                                 # parasite and induced parts
LW_BEYOND = 1.0                               # a curve inside the wave-drag band
DASH_AVAILABLE = (0, (6.5, 3.0))
DASH_PARASITE = (0, (5.0, 2.2))
DOT_INDUCED = (0, (0.1, 2.4))
DASH_CONSTRUCTION = (0, (4.0, 3.0))           # tangent and drop lines (figkit's "boundary" dash)
MS_POINT = 7.0                                # marker size of minimum, tangent and limit points


def required_kw(cond=0, **over):
    """ax.plot() keywords of a required curve (T_R or P_R) at condition `cond` (0 black, 1 blue,
    2 vermilion). Example: ax.plot(V, TR, **required_kw(1))"""
    kw = dict(color=COND_COLOR[cond], linestyle="-", linewidth=LW_CURVE, solid_capstyle="butt")
    kw.update(over)
    return kw


def available_kw(cond=0, **over):
    """ax.plot() keywords of an available curve (T_A or P_A): dashed, the color of its required curve."""
    kw = dict(color=COND_COLOR[cond], linestyle=DASH_AVAILABLE, linewidth=LW_CURVE, dash_capstyle="butt")
    kw.update(over)
    return kw


def part_kw(which, **over):
    """ax.plot() keywords of the parasite ("parasite") or induced ("induced") part of a required curve."""
    if which == "parasite":
        kw = dict(color=SERIES[0], linestyle=DASH_PARASITE, linewidth=LW_PART)
    elif which == "induced":
        kw = dict(color=SERIES[1], linestyle=DOT_INDUCED, linewidth=LW_PART + 0.4, dash_capstyle="round")
    else:
        raise ValueError("which is 'parasite' or 'induced'")
    kw.update(over)
    return kw


PART_TEXT = {"parasite": SERIES[0], "induced": "#B34E00"}


def cond_marks(ax, x, y, cond, n=5, x_range=None, at=None, zorder=5):
    """Open markers of condition `cond` (1: triangles, 2: inverted triangles) at n points spaced evenly
    in x along a curve, inside x_range (default: the whole curve). Nothing for condition 0. They let
    a second condition read without color; `at` gives the x positions instead (keep them clear of
    the marked points). Returns the Line2D or None."""
    if COND_MARK[cond] is None:
        return None
    x, y = np.asarray(x, float), np.asarray(y, float)
    lo, hi = x_range if x_range else (float(x.min()), float(x.max()))
    xs = np.asarray(at, float) if at is not None else np.linspace(lo, hi, n + 2)[1:-1]
    ys = np.interp(xs, x, y)
    return ax.plot(xs, ys, COND_MARK[cond], ms=6.0, mfc="white", mec=COND_COLOR[cond], mew=1.3,
                   zorder=zorder, linestyle="none")[0]


def draw_curve(ax, x, y, kw, x_valid=None, zorder=4):
    """Plot a curve with keywords `kw`; with x_valid, the part beyond x_valid (inside the wave-drag band)
    is drawn thin (LW_BEYOND) in the same color and style. Returns (line, line_beyond or None)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x_valid is None or x_valid >= x.max():
        return ax.plot(x, y, zorder=zorder, **kw)[0], None
    k = int(np.searchsorted(x, x_valid))
    yv = float(np.interp(x_valid, x, y))
    xa, ya = np.r_[x[:k], x_valid], np.r_[y[:k], yv]
    xb, yb = np.r_[x_valid, x[k:]], np.r_[yv, y[k:]]
    a = ax.plot(xa, ya, zorder=zorder, **kw)[0]
    kb = dict(kw)
    kb["linewidth"] = LW_BEYOND
    b = ax.plot(xb, yb, zorder=zorder, **kb)[0]
    return a, b


# ===================================================================== bands
def _band(ax, x0, x1, label, y_label, fs):
    ax.axvspan(x0, x1, color=BAND_FILL, lw=0, zorder=0.5)
    if label:
        y0, y1 = ax.get_ylim()
        yl = y_label if y_label is not None else y0 + 0.62 * (y1 - y0)
        text(ax, (0.5 * (x0 + x1), yl), label, rotation=90, fs=fs, backing=BAND_FILL, linespacing=1.15)


def stall_band(ax, V_stall, x_lo=None, label="below stall", y_label=None, fs=FS_SMALL):
    """Gray band from the left edge of the axes (or x_lo) to the stall speed, named on its side.
    Set the axis limits first. Example: stall_band(ax, 61.3)"""
    lo = ax.get_xlim()[0] if x_lo is None else x_lo
    assert V_stall > lo, "the stall speed lies inside the plotted speeds"
    _band(ax, lo, V_stall, label, y_label, fs)


def mach_band(ax, V_limit, x_hi=None, label="wave drag:\nthe polar\nno longer holds", y_label=None, fs=FS_SMALL):
    """Gray band from the speed where the jet reaches its Mach limit to the right edge of the axes
    (or x_hi), named "wave drag: the polar no longer holds". Set the axis limits first."""
    hi = ax.get_xlim()[1] if x_hi is None else x_hi
    assert V_limit < hi, "the Mach limit lies inside the plotted speeds"
    _band(ax, V_limit, hi, label, y_label, fs)


# ===================================================================== marked points
def _drop(ax, x, y, y_to, cond, zorder=2):
    return ax.plot([x, x], [y_to, y], color=COND_COLOR[cond] if cond else GRAY, lw=LW_THIN,
                   linestyle=DASH_CONSTRUCTION, zorder=zorder)[0]


def mark_minimum(ax, x, y, label=None, cond=0, direction=90.0, dist=8.0, drop=False, y_to=0.0, fs=FS_LABEL,
                 offset=(0.0, 0.0)):
    """The minimum of a curve: a filled circle (with a thin dashed drop line to y_to if drop=True) and
    its label ("minimum, 17.79 kN\\nat 104.8 m/s") toward `direction`. Returns the marker."""
    if drop:
        _drop(ax, x, y, y_to, cond)
    m = ax.plot([x], [y], "o", ms=MS_POINT, color=COND_COLOR[cond], mec=COND_COLOR[cond], zorder=7)[0]
    if label:
        text(ax, (x, y), label, direction=direction, dist=dist, fs=fs, color=COND_TEXT[cond], offset=offset)
    return m


def tangent_from_origin(ax, x_t, y_t, x_end, label=None, cond=0, direction=-30.0, dist=8.0, fs=FS_LABEL,
                        origin_label="origin", origin_dir=45.0, origin_backing=True):
    """The tangent from the origin: a thin dashed line from a marked origin (0, 0) through the point of
    tangency (x_t, y_t) to x_end, an open square at the point, and its label. The axes must start at
    zero on both axes (asserted). origin_backing: the label's backing (BAND_FILL when the origin lies in
    the stall band). Returns the line."""
    x0, y0 = ax.get_xlim()[0], ax.get_ylim()[0]
    assert x0 == 0.0 and y0 == 0.0, "a tangent from the origin needs both axes to start at zero"
    k = y_t / x_t
    ln = ax.plot([0.0, x_end], [0.0, k * x_end], color=COND_COLOR[cond], lw=1.2, linestyle=DASH_CONSTRUCTION,
                 zorder=3)[0]
    ax.plot([0.0], [0.0], "o", ms=6.5, mfc="white", mec=INK, mew=1.3, zorder=8, clip_on=False)
    if origin_label:
        text(ax, (0.0, 0.0), origin_label, direction=origin_dir, dist=12.0, fs=FS_SMALL, backing=origin_backing)
    ax.plot([x_t], [y_t], "s", ms=MS_POINT - 0.5, mfc="white", mec=COND_COLOR[cond], mew=1.5, zorder=7)
    if label:
        text(ax, (x_t, y_t), label, direction=direction, dist=dist, fs=fs, color=COND_TEXT[cond])
    return ln


def mark_limit(ax, x, y, label=None, cond=0, direction=90.0, dist=8.0, y_to=0.0, drop=True, fs=FS_LABEL,
               offset=(0.0, 0.0)):
    """A crossing that sets a limit (a maximum speed, a ceiling): a filled diamond with a thin dashed drop
    line to y_to and its label. Returns the marker."""
    if drop:
        _drop(ax, x, y, y_to, cond)
    m = ax.plot([x], [y], "D", ms=MS_POINT - 0.5, color=COND_COLOR[cond], mec=COND_COLOR[cond], zorder=7)[0]
    if label:
        text(ax, (x, y), label, direction=direction, dist=dist, fs=fs, color=COND_TEXT[cond], offset=offset)
    return m


def panel_title(ax, s, fs=FS_LABEL):
    """Title of a panel, left-aligned above it: names the aircraft (or the condition) the panel is for."""
    return ax.set_title(s, loc="left", fontsize=fs, color=INK, pad=6.0)


def on_curve(x, y, xp, yp, tol, what):
    """Assert that the point (xp, yp) lies on the drawn curve (x, y) within tol (in y units)."""
    close_to(float(np.interp(xp, np.asarray(x, float), np.asarray(y, float))), yp, tol, what)


# ===================================================================== constraint diagram
# One look per requirement. The two vertical limits (wing loading) differ from the four lines of
# thrust-to-weight ratio in color and in style; every line is named on the line.
CONSTRAINT_STYLE = {
    "takeoff": dict(color=INK, ls="-", lw=2.0, text=INK),
    "climb":   dict(color=SERIES[0], ls=(0, (6.0, 2.5)), lw=2.0, text=SERIES[0]),
    "cruise":  dict(color=SERIES[1], ls=(0, (0.1, 2.6)), lw=2.4, text="#B34E00", cap="round"),
    "ceiling": dict(color=STEEL, ls=(0, (7.0, 2.2, 1.4, 2.2)), lw=2.0, text=STEEL),
    "stall":   dict(color="#8E6F3E", ls="-", lw=2.4, text="#7A5E33"),
    "landing": dict(color="#007A5A", ls=(0, (6.0, 1.8, 1.2, 1.8, 1.2, 1.8)), lw=2.0, text="#007A5A"),
}
FEASIBLE_FILL = HIGHLIGHT                     # Purdue light gold, the region of designs that meet every requirement


def constraint_kw(name, **over):
    st = CONSTRAINT_STYLE[name]
    kw = dict(color=st["color"], linestyle=st["ls"], linewidth=st["lw"])
    if st.get("cap") == "round":
        kw.update(dash_capstyle="round")
    kw.update(over)
    return kw


def constraint_line(ax, WS, TW, name, zorder=4):
    """One requirement as a line of T/W against W/S in its look. Returns the Line2D."""
    return ax.plot(WS, TW, zorder=zorder, **constraint_kw(name))[0]


def constraint_vertical(ax, WS_limit, name, zorder=4):
    """A requirement that limits the wing loading (stall, landing): a vertical line in its look."""
    return ax.axvline(WS_limit, zorder=zorder, **constraint_kw(name))


# ===================================================================== force diagrams (equal-aspect axes)
# One scale for the force figures of pages 5.1 (level flight) and 5.3 (climb), so the aircraft and its
# forces are drawn the same size on both pages. The angles and the drag are exaggerated; the captions
# say so.
ALPHA_DRAWN = 10.0               # deg, angle of attack as drawn (cruise and climb are flown at a few degrees)
GAMMA_DRAWN = 20.0               # deg, climb angle as drawn
LD_DRAWN = 3.0                   # drawn lift-to-drag ratio (the real one is several times larger)
W_DRAWN = 1.3                    # length of the weight arrow, data units
AC_LENGTH = 2.5                  # length of the 737-800 outline, data units
SCALE_IN_PER_UNIT = 6.5 / 5.8    # inches per data unit
INSET = 1.4                      # the weight split of the climb figure is drawn 1.4 times larger


def _force(ax, tail, vec, label=None, label_dir=None, dist=4.0, fs=FS_LABEL, zorder=7, ride=None):
    tip = tail + vec
    pa = kind_arrow(ax, tail, tip, "force", label, label_dir=label_dir, dist=dist, fs=fs, zorder=zorder)
    if ride is not None:
        rides_on(pa, ride)
    return tip


def level_forces(ax, cg, W_len, alpha_deg, LD_drawn=4.0, gap=0.0, labels=True, label_dirs=None, starts=None,
                 rides=None):
    """The four forces of steady level flight drawn from the center of gravity `cg` (the aircraft as a
    point mass), to one scale in which the weight is W_len data units long. The flight path is
    horizontal (to the right); the thrust acts along the body axis, at the angle of attack alpha above
    the flight path. The drawn drag is W / LD_drawn (exaggerated: cruise L/D is several times larger)
    and the other forces close the balance exactly:
        along the path:  T cos(alpha) - D = 0          across it:  L + T sin(alpha) - m g = 0.
    `gap` (data units) starts each arrow that far from cg; `starts` (dict, keys "L", "W", "D", "T")
    overrides it per force, so a short force can be drawn on its line of action outside the outline
    (the drag behind the tail, the thrust ahead of the nose); `rides` (dict of force -> Line2D) names
    the line an arrowhead is drawn on (the flight path, the body axis) for the layout gate. Asserts
    that the four drawn vectors add up to zero. Returns dict(L, D, T, W) of the drawn vectors (numpy arrays), "tails" and "tips"."""
    cg = np.asarray(cg, float)
    a = math.radians(alpha_deg)
    D = W_len / LD_drawn
    T = D / math.cos(a)
    L = W_len - T * math.sin(a)
    vec = dict(L=np.array([0.0, L]), W=np.array([0.0, -W_len]), D=np.array([-D, 0.0]), T=T * unit(alpha_deg))
    close_to(float(np.linalg.norm(sum(vec.values()))), 0.0, 1e-12, "the four drawn forces are in balance")
    names = dict(L="lift, $L$", W="weight, $mg$", D="drag, $D$", T="thrust, $T$")
    dirs = dict(L=90.0, W=-90.0, D=180.0, T=alpha_deg)
    if label_dirs:
        dirs.update(label_dirs)
    tips, tails = {}, {}
    for k in ("L", "W", "D", "T"):
        u = vec[k] / np.linalg.norm(vec[k])
        tails[k] = cg + (starts or {}).get(k, gap) * u
        tips[k] = _force(ax, tails[k], vec[k], names[k] if labels else None, label_dir=dirs[k],
                         ride=(rides or {}).get(k))
    vec["tips"], vec["tails"] = tips, tails
    return vec


def climb_forces(ax, cg, W_len, gamma_deg, alpha_deg, LD_drawn=4.0, gap=0.0, labels=True, label_dirs=None,
                 starts=None, rides=None):
    """The four forces of a steady climb at climb angle gamma, drawn from `cg` to one scale (weight
    W_len data units). Lift is perpendicular to the flight path, drag along it backward, the thrust
    along the body axis at alpha above the path (the same convention as level_forces), the weight
    straight down. Drawn drag W / LD_drawn; thrust and lift close the balance exactly:
        along the path:  T cos(alpha) - D - m g sin(gamma) = 0
        across it:       L + T sin(alpha) - m g cos(gamma) = 0.
    `gap`, `starts` and `rides` place the arrows on their lines of action as in level_forces. Asserts the drawn
    vectors add up to zero. Returns dict(L, D, T, W, tails, tips, u, n) (u along the path, n across it)."""
    cg = np.asarray(cg, float)
    g, a = math.radians(gamma_deg), math.radians(alpha_deg)
    u, n = unit(gamma_deg), unit(gamma_deg + 90.0)
    D = W_len / LD_drawn
    T = (D + W_len * math.sin(g)) / math.cos(a)
    L = W_len * math.cos(g) - T * math.sin(a)
    vec = dict(L=L * n, W=np.array([0.0, -W_len]), D=-D * u, T=T * unit(gamma_deg + alpha_deg))
    close_to(float(np.linalg.norm(sum(vec.values()))), 0.0, 1e-12, "the four drawn forces are in balance")
    close_to(float(np.dot(vec["L"], u)), 0.0, 1e-12, "lift is drawn across the flight path")
    names = dict(L="lift, $L$", W="weight, $mg$", D="drag, $D$", T="thrust, $T$")
    dirs = dict(L=gamma_deg + 90.0, W=-90.0, D=gamma_deg + 180.0, T=gamma_deg + alpha_deg)
    if label_dirs:
        dirs.update(label_dirs)
    tips, tails = {}, {}
    for k in ("L", "W", "D", "T"):
        uu = vec[k] / np.linalg.norm(vec[k])
        tails[k] = cg + (starts or {}).get(k, gap) * uu
        tips[k] = _force(ax, tails[k], vec[k], names[k] if labels else None, label_dir=dirs[k],
                         ride=(rides or {}).get(k))
    vec.update(tails=tails, tips=tips, u=u, n=n)
    return vec


def weight_split(ax, origin, W_len, gamma_deg, title="the weight, split", arc_r=None, lw=1.4, along_dir=None,
                 across_dir=None, title_dy=0.2):
    """The weight and its two parts as force arrows, as on page 4.2: m g straight down, m g sin(gamma)
    backward along the flight path, m g cos(gamma) across it into the path, with the dashed rectangle
    whose diagonal is the weight, a right-angle mark and the angle gamma between the weight and its
    cross-path part. Asserts that the two drawn parts are perpendicular and add up to the weight.
    Returns dict(along, across, W)."""
    o = np.asarray(origin, float)
    g = math.radians(gamma_deg)
    u, n = unit(gamma_deg), unit(gamma_deg + 90.0)
    Wv = np.array([0.0, -W_len])
    along = -W_len * math.sin(g) * u
    across = -W_len * math.cos(g) * n
    for a_, b_ in ((o + along, o + along + across), (o + across, o + along + across)):
        ax.plot(*np.c_[a_, b_], color=STEEL, lw=LW_THIN, ls=(0, (4.0, 2.5)), zorder=3)
    s_ = 0.14 * W_len
    ua, uc = along / np.linalg.norm(along), across / np.linalg.norm(across)
    ax.plot(*np.c_[o + s_ * ua, o + s_ * (ua + uc), o + s_ * uc], color=INK, lw=LW_THIN, zorder=4)
    close_to(float(np.dot(ua, uc)), 0.0, 1e-12, "the two parts are drawn at a right angle")
    close_to(float(np.linalg.norm(along + across - Wv)), 0.0, 1e-12, "the two parts add up to the weight")
    close_to(float(np.dot(along, u)), -W_len * math.sin(g), 1e-12, "the along-path part is m g sin(gamma), backward")
    kind_arrow(ax, o, o + Wv, "force")
    text(ax, o + Wv, "$mg$", direction=-90.0, dist=4.0)
    kind_arrow(ax, o, o + along, "force", lw=lw)
    text(ax, o + along, "$mg\\,\\sin\\gamma$,\nbackward along\nthe path",
         direction=gamma_deg + 180.0 if along_dir is None else along_dir, dist=4.0)
    kind_arrow(ax, o, o + across, "force", lw=lw)
    text(ax, o + across, "$mg\\,\\cos\\gamma$,\nacross it", direction=gamma_deg - 70.0 if across_dir is None else across_dir,
         dist=4.0)
    r_ = arc_r or 0.45 * W_len                     # the label sits inside the wedge, beyond the arc
    angle_mark(ax, o, -90.0, gamma_deg - 90.0, r_, "$\\gamma$", stated=gamma_deg, label_r=1.45 * r_)
    if title:
        text(ax, o + np.array([0.0, title_dy * W_len]), title, fs=FS_SMALL)
    return dict(along=along, across=across, W=Wv)


def velocity_triangle(ax, origin, V_len, gamma_deg, labels=True, arc_r=None, rides=None):
    """The flight velocity V along the path at the climb angle gamma, split into its horizontal part
    V cos(gamma) and its vertical part, the rate of climb R/C = V sin(gamma), drawn with Chapter 1's
    velocity arrows to one scale. `rides` (dict with keys "V", "h", "v" -> Line2D) names the line an
    arrow is drawn on (the flight path, the horizontal) for the layout gate, as in level_forces.
    Asserts that the parts close the triangle. Returns dict(V, h, v)."""
    o = np.asarray(origin, float)
    g = math.radians(gamma_deg)
    V = V_len * unit(gamma_deg)
    h = np.array([V_len * math.cos(g), 0.0])
    v = np.array([0.0, V_len * math.sin(g)])
    close_to(float(np.linalg.norm(h + v - V)), 0.0, 1e-12, "the two parts close the velocity triangle")
    rides = rides or {}
    arrows = dict(
        V=kind_arrow(ax, o, o + V, "velocity", "velocity, $V$" if labels else None, label_dir=gamma_deg + 90.0,
                     label_at="mid"),
        h=kind_arrow(ax, o, o + h, "velocity", "$V\\cos\\gamma$" if labels else None, label_dir=-90.0,
                     label_at="mid", lw=1.3),
        v=kind_arrow(ax, o + h, o + h + v, "velocity",
                     "rate of climb,\n$R/C = V\\sin\\gamma$" if labels else None, label_dir=0.0, label_at="mid",
                     lw=1.3))
    for k, ln in rides.items():
        rides_on(arrows[k], ln)
    r_ = arc_r or 0.45 * V_len
    angle_mark(ax, o, 0.0, gamma_deg, r_, "$\\gamma$", stated=gamma_deg, label_r=1.45 * r_)
    return dict(V=V, h=h, v=v)


__all__ = ["BAND_FILL", "COND_COLOR", "COND_TEXT", "COND_MARK", "LW_CURVE", "LW_PART", "LW_BEYOND",
           "DASH_AVAILABLE", "DASH_PARASITE", "DOT_INDUCED", "DASH_CONSTRUCTION", "MS_POINT", "PART_TEXT",
           "required_kw", "available_kw", "part_kw", "cond_marks", "draw_curve", "stall_band", "mach_band",
           "mark_minimum", "tangent_from_origin", "mark_limit", "panel_title", "on_curve",
           "CONSTRAINT_STYLE", "FEASIBLE_FILL", "constraint_kw", "constraint_line", "constraint_vertical",
           "ALPHA_DRAWN", "GAMMA_DRAWN", "LD_DRAWN", "W_DRAWN", "AC_LENGTH", "SCALE_IN_PER_UNIT", "INSET",
           "level_forces", "climb_forces", "weight_split", "velocity_triangle"]
