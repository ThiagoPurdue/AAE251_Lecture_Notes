"""Drawing helpers of Chapter 4, Rocket Design, in the book's line-art style (Chapter 1's fills, line
weights and arrow kinds; white opaque parts with black outlines; hatching where a wall is cut).

  (a) thrust_chamber / draw_thrust_chamber   a thrust chamber in section, from a real contour
  (b) plume                                   the jet boundary for the three states of expansion
  (c) pressure_arrows                         short arrows normal to a wall (one arrow kind, PRESSURE_ARROW)
  (d) MASS_STYLE, mass_bar, mass_braces       mass bars to one scale, one look for payload, inert, propellant
  (e) stage_stack                             a simple stack of stages and payload, for the idea
  (f) aligned_axes                            a data plot above a schematic, sharing the horizontal scale
  (g) liquid_engine, solid_motor, hybrid_motor   engine and feed schematics in one style
  (h) range_boxes, named_scatter, class_bands, log_axis   log-log charts with direct labels
  (i) tanks_in_stage                          spherical or cylindrical tanks inside a stage, to scale, with ullage
  (j) temperature_axis                        a temperature scale in kelvin and degrees Celsius

Every helper works on equal-aspect axes in meters (hardware) unless it says otherwise, returns what it
drew, and asserts what it exists to show (an area ratio, a mass sum, a boundary inside or outside the
exit radius, a tank volume). Leaders into hardware may cross only the outlines of the part they name:
every wall, detail and hatch drawn on an engine is marked with figkit.on_part on the part it belongs to.

Sources of the shapes: NASA SP-125 (Huzel and Huang, 1967), Section 4.3, Figure 4-13 and Eq. (4-7)
(the parabolic approximation of a bell nozzle: a circular arc of 1.5 r_t before the throat, one of
0.382 r_t after it, then a parabola to the exit, 80 percent of the length of a 15-deg cone), Figure 4-14
(the parabola's angles), and its design example of Section 4.3 (contraction ratio 1.6, characteristic
chamber length 45 in, for a liquid oxygen and kerosene engine); Chapter 3 of the same book for the
feed systems; Sutton and Biblarz, Rocket Propulsion Elements, Chapters 1, 12 and 16 (solid motor and
hybrid layouts, schematic only).
"""
import math

import numpy as np

from chapter_1.style import *  # noqa: F401,F403
from chapter_1.style import _screen_angle  # noqa: F401
from chapter_1.diagrams import brace, text_size, key_disc  # noqa: F401
from chapter_1.launchers import PROPELLANT_STYLE, HATCH_INK
from chapter_1.geometry import Part, catmull_rom
from chapter_4.nozzle import bell_angles, bell_length
from matplotlib.patches import Polygon, Rectangle, Circle, PathPatch
from matplotlib.path import Path as MPath

__all__ = ["fill_region", "MASS_STYLE", "MASS_ORDER", "PRESSURE_ARROW", "PLUME_STYLE", "SHOCK_STYLE", "LIQUID_STYLE", "WALL_HATCH",
           "chamber_contour", "thrust_chamber", "draw_thrust_chamber", "name_station", "plume", "pressure_arrows",
           "mass_bar", "mass_braces", "stage_stack", "aligned_axes", "liquid_engine", "solid_motor",
           "hybrid_motor", "draw_schematic", "range_boxes", "named_scatter", "class_bands", "log_axis",
           "tanks_in_stage", "sphere_diameter", "temperature_axis", "place_labels", "arrow_key", "math_row", "mass_key", "RANGE_STYLES", "RANGE_TEXT"]

WALL_HATCH = "////"                       # a wall cut in section (as chapter_1.drawing.hatched_wall)
WALL_LW = 1.2                             # pt, outline of a wall in section
PRESSURE_ARROW = dict(color="#555960", lw=1.0, head="small")     # pressure on a wall (steel gray, thin)
PLUME_STYLE = dict(color=INK, lw=1.5, ls=(0, (5.0, 3.0)))        # the jet boundary (dashed)
SHOCK_STYLE = dict(color=INK, lw=0.9, ls="-")                     # an oblique shock (thin solid)

# One look for each kind of mass on every page (point 21): they differ in lightness and hatch, so they
# read in grayscale. Payload: Purdue gold, plain; inert mass: white with a dense gray hatch (structure);
# propellant: light blue, plain. Labels on a plain segment use the segment's fill as their backing; a
# hatched segment is labeled outside.
MASS_STYLE = {
    "payload":    dict(fill=GOLD, hatch=None, name="payload"),
    "inert":      dict(fill="#FFFFFF", hatch="////", name="inert mass"),
    "propellant": dict(fill="#DCEBF7", hatch=None, name="propellant"),
}
MASS_ORDER = ("payload", "inert", "propellant")
# Liquids in an engine schematic: the oxidizer and the fuel tints of Chapter 1's cutaways
LIQUID_STYLE = {"oxidizer": PROPELLANT_STYLE["lox"], "fuel": PROPELLANT_STYLE["rp1"],
                "solid": PROPELLANT_STYLE["solid"],
                "solid fuel": dict(fill="#F7E3C8", hatch="xx", name="solid fuel"),
                "pressurant": dict(fill="#FFFFFF", hatch=None, name="pressurant gas")}


def _pt(ax, n):
    """n points in data units (equal-aspect axes with limits set)."""
    a = ax.transData.inverted().transform([(0.0, 0.0), (n * ax.figure.dpi / 72.0, 0.0)])
    return float(a[1, 0] - a[0, 0])


def _poly(ax, xy, fc="white", ec=INK, lw=LW_OUTLINE, hatch=None, z=3.0, opaque_=True, **kw):
    pa = Polygon(np.asarray(xy, float), closed=True, fc=fc, ec=ec, lw=lw, joinstyle="round", zorder=z, **kw)
    if hatch:
        pa.set_hatch(hatch)
    ax.add_patch(pa)
    if opaque_ and fc not in ("none", None):
        opaque(pa)
    return pa


def fill_region(ax, xy, style, z=3.0, edge_lw=LW_DETAIL):
    """A tinted and hatched region (a propellant, a mass) with a black outline: the fill of the chapter's
    tanks and mass bars, for a page that draws its own shape. Example:
    fill_region(ax, [(0, 0), (2, 0), (2, 1), (0, 1)], LIQUID_STYLE["oxidizer"])"""
    return _fill_poly(ax, xy, style, z, edge_lw)


def _fill_poly(ax, xy, style, z, edge_lw=LW_DETAIL):
    """A region with a tint and a hatch (a propellant, a mass), drawn as a hatched fill with no edge (the
    hatch in HATCH_INK) and a black outline above it, as chapter_1.launchers.draw_cutaway does."""
    fp = Polygon(np.asarray(xy, float), closed=True, fc=style["fill"], ec=HATCH_INK, lw=0.0, zorder=z)
    if style.get("hatch"):
        fp.set_hatch(style["hatch"])
    ax.add_patch(fp)
    opaque(fp)
    ed = Polygon(np.asarray(xy, float), closed=True, fc="none", ec=INK, lw=edge_lw, joinstyle="round", zorder=z + 0.01)
    ax.add_patch(ed)
    return fp, ed


# ===================================================================== (a) the thrust chamber
def _arc(c, R, a0, a1, n=24):
    t = np.radians(np.linspace(a0, a1, n))
    return np.c_[c[0] + R * np.cos(t), c[1] + R * np.sin(t)]


def chamber_contour(r_t, area_ratio, contraction_ratio=1.6, L_star=45 * 0.0254, conv_angle=30.0,
                    bell_fraction=0.8, n=60, n_arc=None):
    """The inner contour (x, r) of a thrust chamber, flow in +x, throat at x = 0: the injector face, a
    cylindrical chamber of radius r_t sqrt(contraction_ratio), a converging cone at conv_angle deg ending
    in the throat arc of radius 1.5 r_t, the throat, then the 80-percent parabolic bell of SP-125 Section
    4.3 (arc of 0.382 r_t, parabola at the angles of Figure 4-14, length of Eq. 4-7) to the exit radius
    r_t sqrt(area_ratio). The chamber length makes the volume up to the throat L_star x A_t (SP-125's
    characteristic length; default 45 in, its design example). Returns a dict: x, r (arrays from the
    injector to the exit), stations (injector, chamber_end, throat, exit: x), r_c, r_t, r_e, i_throat.
    n is the number of points on the bell; n_arc, if given, the number on each of the three arcs (default
    16, 12 and 12): a plot of the flow along the contour takes a fine sampling (n=400, n_arc=60), so its
    curves have no straight segments at the throat. Example: c = chamber_contour(0.4413, 16.0)"""
    Rt, Rc, Re = r_t, r_t * math.sqrt(contraction_ratio), r_t * math.sqrt(area_ratio)
    b = math.radians(conv_angle)
    n_up, n_fil, n_dn = (16, 12, 12) if n_arc is None else (n_arc, n_arc, n_arc)
    # converging: throat arc (1.5 r_t) from the throat back to the cone angle
    phi = np.linspace(0.0, b, n_up)
    up = np.c_[-1.5 * Rt * np.sin(phi), Rt + 1.5 * Rt * (1.0 - np.cos(phi))]
    xA, rA = up[-1]
    # a fillet between the cone and the cylinder: radius Rc, or smaller when the chamber is only a little wider
    # than the throat (a low contraction ratio, as in large engines), leaving a short straight cone
    if Rc - rA <= 0.0:
        raise ValueError(f"contraction ratio {contraction_ratio} too small for a {conv_angle} deg converging section")
    R2 = min(1.0 * Rc, 0.8 * (Rc - rA) / (1.0 - math.cos(b)))
    rP = Rc - R2 * (1.0 - math.cos(b))
    xP = xA - (rP - rA) / math.tan(b)
    xc = xP - R2 * math.sin(b)
    fil = _arc((xc, Rc - R2), R2, 90.0, 90.0 - math.degrees(b), n_fil)       # from the cylinder's end to P
    # chamber volume up to the throat: cylinder + the converging part (by the area along x)
    xs_conv = np.r_[fil[:, 0], up[::-1, 0]]
    rs_conv = np.r_[fil[:, 1], up[::-1, 1]]
    order = np.argsort(xs_conv)
    xs_conv, rs_conv = xs_conv[order], rs_conv[order]
    v_conv = float(np.trapezoid(math.pi * rs_conv ** 2, xs_conv))
    At, Ac = math.pi * Rt * Rt, math.pi * Rc * Rc
    L_cyl = max((L_star * At - v_conv) / Ac, 0.35 * Rc)
    x_inj = xc - L_cyl
    # diverging: arc of 0.382 r_t to N, parabola (quadratic Bezier) to the exit
    tn, te = bell_angles(area_ratio)
    Ln = bell_length(Rt, area_ratio, bell_fraction)
    ph = np.radians(np.linspace(0.0, tn, n_dn))
    down = np.c_[0.382 * Rt * np.sin(ph), Rt + 0.382 * Rt * (1.0 - np.cos(ph))]
    N = down[-1]
    E = np.array([Ln, Re])
    m1, m2 = math.tan(math.radians(tn)), math.tan(math.radians(te))
    qx = (E[1] - N[1] + m1 * N[0] - m2 * E[0]) / (m1 - m2)
    Q = np.array([qx, N[1] + m1 * (qx - N[0])])
    assert N[0] < Q[0] < E[0], "bell control point between N and E"
    t = np.linspace(0.0, 1.0, n)[:, None]
    bell = (1 - t) ** 2 * N + 2 * (1 - t) * t * Q + t ** 2 * E
    pts = np.r_[[(x_inj, Rc)], fil, up[::-1], down[1:], bell[1:]]
    x, r = pts[:, 0], pts[:, 1]
    i_t = int(np.argmin(r))
    close_to(float(r[i_t]), Rt, 1e-9, "throat radius")
    close_to(float(r[-1] ** 2 / Rt ** 2), area_ratio, 1e-9, "drawn area ratio")
    return dict(x=x, r=r, r_t=Rt, r_c=Rc, r_e=Re, i_throat=i_t, L_cyl=L_cyl, theta_n=tn, theta_e=te,
                stations=dict(injector=float(x_inj), chamber_end=float(xc), throat=0.0, exit=float(Ln)))


def _offset(x, r, t):
    """The polyline (x, r) moved a distance t along its outward normal (the wall's outer surface)."""
    p = np.c_[x, r]
    d = np.gradient(p, axis=0)
    d /= np.hypot(d[:, 0], d[:, 1])[:, None]
    nrm = np.c_[-d[:, 1], d[:, 0]]
    return p + t * nrm


def thrust_chamber(r_t, area_ratio, contraction_ratio=1.6, L_star=45 * 0.0254, wall=None, injector=None,
                   origin=(0.0, 0.0), conv_angle=30.0, n=60, n_arc=None):
    """The parts of a thrust chamber in section (flow in +x, axis on y = origin[1], throat at x =
    origin[0]), as closed outlines (chapter_1.geometry.Part): wall_upper, wall_lower (the wall cut in
    section, drawn `wall` thick, default 0.12 r_t: wider than a real wall so it reads), injector (the
    injector plate across the chamber, cut in section), and the gas regions chamber, converging, diverging
    (named regions a leader may end in). Also returns stations (x of injector, chamber_end, throat, exit),
    radii r_c, r_t, r_e, the inner contour (x, r) and `envelope` (the outer outline: everything drawn on the
    engine is on it). Asserts the drawn area ratio. Example: tc = thrust_chamber(0.4413, 16.0)"""
    c = chamber_contour(r_t, area_ratio, contraction_ratio, L_star, conv_angle, n=n, n_arc=n_arc)
    ox, oy = origin
    t = wall if wall is not None else 0.12 * r_t
    tj = injector if injector is not None else 0.30 * r_t
    x, r = c["x"] + ox, c["r"]
    outer = _offset(x, r, t)
    outer[0, 0] = x[0]                                   # the wall starts square at the injector face
    outer[-1] = (x[-1], r[-1] + t)                       # and ends square at the exit plane
    up = np.r_[np.c_[x, oy + r], outer[::-1] * [1, 1] + [0, oy]]
    lo = np.c_[up[:, 0], 2 * oy - up[:, 1]]
    st = {k: v + ox for k, v in c["stations"].items()}
    xi = st["injector"]
    Rc = c["r_c"]
    parts = {}
    parts["wall_upper"] = Part("wall_upper", up, "wall", z=4.0, inside=(float(x[len(x) // 2]), oy + float(r[len(x) // 2]) + 0.5 * t))
    parts["wall_lower"] = Part("wall_lower", lo, "wall", z=4.0, inside=(float(x[len(x) // 2]), oy - float(r[len(x) // 2]) - 0.5 * t))
    parts["injector"] = Part("injector", np.array([(xi - tj, oy - Rc - t), (xi, oy - Rc - t), (xi, oy + Rc + t),
                                                   (xi - tj, oy + Rc + t)]), "wall", z=4.0,
                             inside=(xi - 0.5 * tj, oy + 0.45 * Rc))
    # gas regions (between the walls): chamber (to the start of the converging section), converging, diverging
    def region(a, b):
        m = (x >= a - 1e-12) & (x <= b + 1e-12)
        xx, rr = x[m], r[m]
        return np.r_[np.c_[xx, oy + rr], np.c_[xx[::-1], oy - rr[::-1]]]
    xt = st["throat"]
    parts["chamber"] = Part("chamber", region(xi, st["chamber_end"]), "gas", z=2.0,
                            inside=(0.5 * (xi + st["chamber_end"]), oy + 0.55 * Rc))
    parts["converging"] = Part("converging", region(st["chamber_end"], xt), "gas", z=2.0,
                               inside=(0.5 * (st["chamber_end"] + xt), oy + 0.45 * Rc))
    parts["diverging"] = Part("diverging", region(xt, st["exit"]), "gas", z=2.0,
                              inside=(xt + 0.55 * (st["exit"] - xt), oy + 0.45 * c["r_e"]))
    env = np.r_[[(xi - tj, oy + Rc + t)], outer + [0, oy], (outer * [1, -1] + [0, oy])[::-1], [(xi - tj, oy - Rc - t)]]
    close_to(float((up[len(x) - 1, 1] - oy) ** 2 / c["r_t"] ** 2), area_ratio, 1e-9, "exit radius gives the area ratio")
    return dict(parts=parts, stations=st, r_c=Rc, r_t=c["r_t"], r_e=c["r_e"], x=x, r=r, axis_y=oy, wall=t,
                envelope=env, theta_n=c["theta_n"], theta_e=c["theta_e"], L_cyl=c["L_cyl"])


def draw_thrust_chamber(ax, tc, highlight=(), axis=True, exit_plane=True, z=0.0, half=False):
    """Draw a thrust_chamber(): the gas regions white (a highlighted one in light gold), the walls and the
    injector cut in section (white, WALL_HATCH, black outline), the axis as a thin dash-dot line and the
    exit plane as a thin dashed line. Every wall and region is drawn on the engine's envelope (on_part), so
    a leader that ends inside the engine may cross them and no other leader may. half=True draws only the
    half above the axis (the injector plate stops at the axis), for a panel under a plot along the nozzle.
    Returns a dict of patches (and "envelope", "axis", "exit_plane").
    Example: P = draw_thrust_chamber(ax, tc, highlight=("throat",))"""
    P = {}
    oy0 = tc["axis_y"]

    def _cut(xy):                                        # the upper half of a part symmetric about the axis
        xy = np.array(xy, float)
        if half:
            xy[:, 1] = np.maximum(xy[:, 1], oy0)
        return xy
    env = Polygon(_cut(tc["envelope"]), closed=True, fc="white", ec="none", lw=0.0, zorder=z + 1.5)
    ax.add_patch(env)
    P["envelope"] = env
    for name, p in tc["parts"].items():
        if half and name == "wall_lower":
            continue
        if p.kind == "gas":
            fc = HIGHLIGHT if name in highlight else "white"
            pa = Polygon(_cut(p.xy), closed=True, fc=fc, ec="none", lw=0.0, zorder=z + p.z)
            ax.add_patch(pa)
        else:
            pa = _poly(ax, _cut(p.xy), fc="white", ec=INK, lw=WALL_LW, hatch=WALL_HATCH, z=z + p.z)
        on_part(pa, env)
        pa._part = name
        P[name] = pa
    st, oy = tc["stations"], tc["axis_y"]
    if axis:
        x0, x1 = st["injector"] - 0.6 * tc["r_t"], st["exit"] + 0.25 * tc["r_t"]
        ln = ax.plot([x0, x1], [oy, oy], color=GRAY, lw=LW_THIN, ls=(0, (8.0, 2.5, 1.5, 2.5)), zorder=z + 2.5)[0]
        on_part(ln, env)
        P["axis"] = ln
    if exit_plane:
        xe, re = st["exit"], tc["r_e"]
        ln = ax.plot([xe, xe], [oy if half else oy - re, oy + re], color=INK, lw=LW_THIN, ls=(0, (3.0, 2.0)),
                     zorder=z + 2.6)[0]
        on_part(ln, env)
        P["exit_plane"] = ln
    return P


def name_station(ax, tc, P, name, s, at, target=None, fs=FS_LABEL, ha=None):
    """Name a part of a drawn thrust chamber (a gas region, a wall, the injector, or "throat" and "exit
    plane") with a label at `at` and a short leader that ends inside it with a small dot.
    Example: name_station(ax, tc, P, "chamber", "combustion chamber", (x, y))"""
    st, oy = tc["stations"], tc["axis_y"]
    if target is None:
        if name == "throat":
            target = (st["throat"], oy + 0.55 * tc["r_t"])
        elif name == "exit plane":
            target = (st["exit"], oy + 0.62 * tc["r_e"])
        else:
            target = tc["parts"][name].inside
    an = callout(ax, target, s, at, gap=1.5, fs=fs, ha=ha)
    an.arrow_patch.set_gid("leader")
    ax.plot(*target, "o", ms=2.6, color=INK, zorder=12, gid=f"grp:lead-{name}")
    return an


# ===================================================================== (b) the plume
def plume(ax, exit_xy, r_exit, state, length, shocks=True, n=120, zorder=3.0):
    """The jet boundary behind a nozzle exit at exit_xy (the exit's center, flow in +x) of radius r_exit,
    drawn `length` long for one state of expansion: "overexpanded" (the boundary turns in, squeezed by the
    higher outside pressure; with shocks=True the two oblique shocks from the lip, thin lines meeting on
    the axis and reflecting back out), "ideally expanded" (straight), "underexpanded" (it turns out and
    widens). Clean dashed boundaries (PLUME_STYLE); the caption says the angles are exaggerated. Asserts
    that one exit radius downstream the boundary is inside, on or outside the exit radius. Returns a dict:
    upper, lower (Line2D), r (the boundary radius against distance), shocks (Line2D list).
    Example: plume(ax, (3.0, 0.0), 1.0, "underexpanded", 4.0)"""
    x0, y0 = exit_xy
    s = np.linspace(0.0, length, n)
    R = r_exit
    if state == "overexpanded":
        r = R * (1.0 - 0.30 * (1.0 - np.exp(-s / (0.55 * R))) + 0.06 * (1.0 - np.cos(np.clip(s - 1.6 * R, 0, None) / R * 1.6)))
    elif state == "ideally expanded":
        r = np.full_like(s, R)
    elif state == "underexpanded":
        r = R * (1.0 + 0.42 * (1.0 - np.exp(-s / (0.9 * R))))
    else:
        raise ValueError(f"state must be one of overexpanded, ideally expanded, underexpanded: {state!r}")
    r1 = float(np.interp(R, s, r))
    if state == "overexpanded":
        assert r1 < 0.97 * R, "overexpanded: the boundary is inside the exit radius one radius downstream"
    elif state == "ideally expanded":
        assert abs(r1 - R) < 1e-12, "ideally expanded: the boundary stays at the exit radius"
    else:
        assert r1 > 1.03 * R, "underexpanded: the boundary is outside the exit radius one radius downstream"
    kw = dict(color=PLUME_STYLE["color"], lw=PLUME_STYLE["lw"], ls=PLUME_STYLE["ls"], zorder=zorder)
    up = ax.plot(x0 + s, y0 + r, **kw)[0]
    lo = ax.plot(x0 + s, y0 - r, **kw)[0]
    sh = []
    if shocks and state == "overexpanded":
        xm = x0 + 1.15 * R                                  # where the two lip shocks meet on the axis
        xr = x0 + 2.0 * R                                   # where the reflected shocks reach the boundary
        rr = float(np.interp(xr - x0, s, r))
        for sg in (1, -1):
            sh.append(ax.plot([x0, xm], [y0 + sg * R * 0.985, y0], color=SHOCK_STYLE["color"], lw=SHOCK_STYLE["lw"],
                              zorder=zorder)[0])
            sh.append(ax.plot([xm, xr], [y0, y0 + sg * rr * 0.97], color=SHOCK_STYLE["color"], lw=SHOCK_STYLE["lw"],
                              zorder=zorder)[0])
    return dict(upper=up, lower=lo, s=s, r=r, shocks=sh, r_at_one_radius=r1)


# ===================================================================== (c) pressure arrows
def pressure_arrows(ax, xy, n=6, length=14.0, side=1, inward=True, margin=0.08, color=None, lw=None, zorder=6):
    """Short arrows normal to the polyline xy (data), evenly spaced along it (leaving `margin` of its length
    free at each end), each `length` points long on the side `side` (+1: left of the polyline's direction,
    -1: right). inward=True: the arrows point at the wall, tips on it (a pressure pushing on the wall);
    inward=False: they start on the wall and point away. One arrow kind (PRESSURE_ARROW: thin steel gray,
    small head); name it in a key. Returns the list of (base, tip) points.
    Example: pressure_arrows(ax, [(0, 1), (4, 1)], n=5, side=1)"""
    xy = np.asarray(xy, float)
    seg = np.hypot(*np.diff(xy, axis=0).T)
    s = np.r_[0.0, np.cumsum(seg)]
    L = _pt(ax, length)
    out = []
    for f in np.linspace(margin, 1.0 - margin, n):
        si = f * s[-1]
        i = int(np.clip(np.searchsorted(s, si), 1, len(s) - 1))
        p = xy[i - 1] + (si - s[i - 1]) / seg[i - 1] * (xy[i] - xy[i - 1])
        d = (xy[i] - xy[i - 1]) / seg[i - 1]
        nrm = side * np.array([-d[1], d[0]])
        a, b = (p + L * nrm, p) if inward else (p, p + L * nrm)
        arrow(ax, a, b, color=color or PRESSURE_ARROW["color"], lw=lw or PRESSURE_ARROW["lw"], head=PRESSURE_ARROW["head"],
              zorder=zorder)
        out.append((a, b))
    return out


# ===================================================================== (d) mass bars
def _seg_list(segments):
    out = []
    for sgm in segments:
        if isinstance(sgm, dict):
            out.append(dict(kind=sgm["kind"], mass=float(sgm["mass"]), name=sgm.get("name"), value=sgm.get("value"),
                            style=sgm.get("style")))
        else:
            kind, mass = sgm[0], float(sgm[1])
            out.append(dict(kind=kind, mass=mass, name=sgm[2] if len(sgm) > 2 else None,
                            value=sgm[3] if len(sgm) > 3 else None, style=None))
    return out


def mass_bar(ax, origin, segments, scale, height, orientation="horizontal", unit="kg", fs=FS_LABEL, labels=True,
             label_at=None, two_lines=True, total=None, zorder=3.0, edge_lw=LW_DETAIL):
    """A bar whose segments are masses drawn to one scale: `scale` data units per kilogram (give several
    bars in one figure the same scale). origin: the start (left end of a horizontal bar, bottom of a
    vertical one) at the bar's lower or left edge. segments: in drawing order, each (kind, mass[, name[,
    value text]]) or a dict with those keys; kind is "payload", "inert" or "propellant" (MASS_STYLE: one look
    for each), or any kind with its own `style` dict (fill, hatch). Each segment is named with its name
    (default: the kind's name) and its value (default fmt(mass) + " kg"): inside the segment when the text
    fits and the segment is plain, otherwise outside (above a horizontal bar, to the right of a vertical
    one) with a short leader; label_at maps a segment index to a label position (data) to move one.
    Asserts that the drawn lengths add up to the total (or to `total` when given). Returns a dict: patches,
    spans [(start, end) along the bar], labels, end, total.
    Example: mass_bar(ax, (0, 0), [("payload", 1750), ("inert", 1153), ("propellant", 5629)], 1e-3, 0.6)"""
    segs = _seg_list(segments)
    x0, y0 = origin
    horiz = orientation == "horizontal"
    pos = 0.0
    spans, patches, labs = [], [], []
    for i, sg in enumerate(segs):
        st = sg["style"] or MASS_STYLE[sg["kind"]]
        Lg = sg["mass"] * scale
        if horiz:
            rect = [(x0 + pos, y0), (x0 + pos + Lg, y0), (x0 + pos + Lg, y0 + height), (x0 + pos, y0 + height)]
        else:
            rect = [(x0, y0 + pos), (x0 + height, y0 + pos), (x0 + height, y0 + pos + Lg), (x0, y0 + pos + Lg)]
        fp, ed = _fill_poly(ax, rect, st, zorder, edge_lw)
        patches.append((fp, ed))
        spans.append((pos, pos + Lg))
        pos += Lg
    tot = sum(sg["mass"] for sg in segs)
    close_to(pos, tot * scale, 1e-9 * max(1.0, tot * scale), "mass bar: the segments add up to the bar")
    if total is not None:
        close_to(tot, float(total), 1e-6 * max(1.0, float(total)), "mass bar: the segments add up to the total")
    if labels:
        for i, sg in enumerate(segs):
            st = sg["style"] or MASS_STYLE[sg["kind"]]
            name = sg["name"] if sg["name"] is not None else st["name"]
            val = sg["value"] if sg["value"] is not None else f"{fmt(sg['mass'])} {unit}"
            if not val:
                s = name
            elif not name:
                s = val
            else:
                s = f"{name}\n{val}" if two_lines else f"{name}, {val}"
            if not s:
                continue
            a, b = spans[i]
            mid = 0.5 * (a + b)
            c = (x0 + mid, y0 + 0.5 * height) if horiz else (x0 + 0.5 * height, y0 + mid)
            w, h = text_size(ax, s, fs)
            room = (b - a) if horiz else height
            room_h = height if horiz else (b - a)
            plain = not st.get("hatch")
            if label_at is not None and i in label_at:
                t = callout(ax, c, s, label_at[i], fs=fs, ha="center", va="center")
                t.arrow_patch.set_gid("leader")
                ax.plot(*c, "o", ms=2.6, color=INK, zorder=zorder + 5, gid=f"grp:mass-{x0:.6g}-{y0:.6g}-{i}")
                labs.append(t)
            elif plain and w + 2 * _pt(ax, 3.0) <= room and h + 2 * _pt(ax, 2.0) <= room_h:
                t = ax.text(*c, s, ha="center", va="center", fontsize=fs, color=INK, zorder=zorder + 2,
                            linespacing=1.15, bbox=dict(boxstyle="square,pad=0.12", fc=st["fill"], ec="none"))
                labs.append(t)
            else:
                if horiz:
                    at = (x0 + mid, y0 + height + _pt(ax, 8.0) + 0.5 * h)
                else:
                    at = (x0 + height + _pt(ax, 10.0) + 0.5 * w, y0 + mid)
                t = callout(ax, c, s, at, fs=fs, ha="center", va="center")
                t.arrow_patch.set_gid("leader")
                ax.plot(*c, "o", ms=2.6, color=INK, zorder=zorder + 5, gid=f"grp:mass-{x0:.6g}-{y0:.6g}-{i}")
                labs.append(t)
    end = (x0 + pos, y0) if horiz else (x0, y0 + pos)
    return dict(patches=patches, spans=spans, labels=labs, end=end, total=tot, origin=(x0, y0), height=height,
                horizontal=horiz, scale=scale, segments=segs)


def mass_braces(ax, bar, groups, side=-1, depth=6.0, gap=4.0, step=16.0, fs=FS_LABEL):
    """Braces along a mass_bar(): groups is a list of (first segment, last segment, label); each brace spans
    those segments, `gap` points from the bar on `side` (-1: below a horizontal bar, left of a vertical one;
    +1: above or right), the n-th brace `step` points further out than the one before, so m_f and m_i can
    be shown together. Returns the braces. Example: mass_braces(ax, bar, [(0, 1, "$m_f$"), (0, 2, "$m_i$")])"""
    x0, y0 = bar["origin"]
    h = bar["height"]
    out = []
    for k, (i0, i1, lab) in enumerate(groups):
        a, b = bar["spans"][i0][0], bar["spans"][i1][1]
        off = _pt(ax, gap + k * step)
        if bar["horizontal"]:
            y = y0 - off if side < 0 else y0 + h + off
            p0, p1 = (x0 + b, y), (x0 + a, y)
            if side > 0:
                p0, p1 = p1, p0
        else:
            x = x0 - off if side < 0 else x0 + h + off
            p0, p1 = (x, y0 + a), (x, y0 + b)
            if side > 0:
                p0, p1 = p1, p0
        out.append(brace(ax, p0, p1, lab, side=1, depth=depth, fs=fs))
    return out


# ===================================================================== (e) a stack of stages
def stage_stack(ax, stages, payload=None, origin=(0.0, 0.0), width=1.0, nozzle=True, separation=True,
                fs=FS_LABEL, names=True, zorder=3.0):
    """A clean stack of stages for a figure about the idea (not a real vehicle: real vehicles use Chapter
    1's launch_vehicle and two_stage_vehicle). stages: list in stage order (stage 1, the lowest, first) of
    dicts with `length` (data units) and optional `name` ("stage 1"); payload: dict(length, name) drawn on
    top under a nose (MASS_STYLE payload fill). Vertical, nose up; stage 1 has a bell nozzle below it; the
    joints between stages are separation planes (thin dashed lines that run past the outline). Returns a
    dict: patches, joints (y of each separation plane, from the lowest), top, bottom, stage spans
    [(y0, y1)], x (center).
    Example: S = stage_stack(ax, [dict(length=4.0), dict(length=2.0)], dict(length=1.2, name="payload"))"""
    x, y = origin
    w = width
    out = dict(patches={}, joints=[], spans=[], x=x)
    if nozzle:
        hn = 0.55 * w
        noz = [(x - 0.12 * w, y + hn), (x + 0.12 * w, y + hn), (x + 0.30 * w, y), (x - 0.30 * w, y)]
        out["patches"]["nozzle"] = _poly(ax, noz, lw=LW_DETAIL + 0.2, z=zorder)
        y += hn
    out["bottom"] = y
    for k, sgm in enumerate(stages):
        L = float(sgm["length"])
        rect = [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + L), (x - w / 2, y + L)]
        pa = _poly(ax, rect, lw=LW_OUTLINE, z=zorder)
        out["patches"][f"stage{k + 1}"] = pa
        out["spans"].append((y, y + L))
        if names:
            t = ax.text(x, y + L / 2, sgm.get("name", f"stage {k + 1}"), ha="center", va="center", fontsize=fs,
                        color=INK, zorder=zorder + 2)
            t._in_box = None
        y += L
        if k < len(stages) - 1:
            out["joints"].append(y)
    if payload is not None:
        L = float(payload["length"])
        rect = [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + L), (x - w / 2, y + L)]
        fp, ed = _fill_poly(ax, rect, MASS_STYLE["payload"], zorder, LW_OUTLINE)
        out["patches"]["payload"] = ed
        out["spans"].append((y, y + L))
        if names:
            ax.text(x, y + L / 2, payload.get("name", "payload"), ha="center", va="center", fontsize=fs, color=INK,
                    zorder=zorder + 2, bbox=dict(boxstyle="square,pad=0.12", fc=MASS_STYLE["payload"]["fill"], ec="none"))
        out["joints"].append(y)
        y += L
        nose = [(x - w / 2, y), (x + w / 2, y), (x, y + 0.9 * w)]
        out["patches"]["nose"] = _poly(ax, nose, lw=LW_OUTLINE, z=zorder)
        y += 0.9 * w
    out["top"] = y
    if separation:
        ext = 0.28 * w
        for yj in out["joints"]:
            ax.plot([x - w / 2 - ext, x + w / 2 + ext], [yj, yj], color=INK, lw=LW_THIN, ls=(0, (3.0, 2.0)),
                    zorder=zorder + 1)
    return out


# ===================================================================== (f) a plot aligned with a drawing
def aligned_axes(width, xlim, ylim_draw, plot_height, left=0.85, right=0.25, top=0.15, gap=0.12, bottom=0.08):
    """A data axes above a schematic axes that share the horizontal scale exactly (the nozzle-flow figure):
    the schematic is equal-aspect in data units with x in xlim and y in ylim_draw; the plot above has the
    same x limits and is plot_height inches tall. Margins in inches. Returns fig, ax_plot, ax_draw.
    Example: fig, top, bot = aligned_axes(6.5, (-1.5, 4.5), (-2.0, 2.0), 2.4)"""
    aw = width - left - right
    s = aw / (xlim[1] - xlim[0])                       # inches per data unit
    dh = s * (ylim_draw[1] - ylim_draw[0])
    H = bottom + dh + gap + plot_height + top
    fig = plt.figure(figsize=(width, H))
    axd = fig.add_axes([left / width, bottom / H, aw / width, dh / H])
    axp = fig.add_axes([left / width, (bottom + dh + gap) / H, aw / width, plot_height / H])
    axd.set_xlim(*xlim)
    axd.set_ylim(*ylim_draw)
    axd.set_aspect("equal", adjustable="box")
    axd.axis("off")
    axp.set_xlim(*xlim)
    for sname in ("top", "right"):
        axp.spines[sname].set_visible(False)
    axp.grid(True, color=GRID, lw=0.6)
    axp.set_axisbelow(True)
    axp.yaxis.set_major_formatter(CommaFormatter())
    fig.canvas.draw()
    pa, pd = axp.get_window_extent(), axd.get_window_extent()
    assert abs(pa.x0 - pd.x0) < 0.5 and abs(pa.x1 - pd.x1) < 0.5, "the two axes share the horizontal scale"
    return fig, axp, axd


# ===================================================================== (g) engine and feed schematics
def _capsule(x, z0, z1, R, n=30):
    """A tank outline: a cylinder of radius R from z0 to z1 with hemispherical domes (vertical)."""
    t = np.linspace(0.0, math.pi, n)
    top = np.c_[x + R * np.cos(t), z1 + R * np.sin(t)]
    bot = np.c_[x - R * np.cos(t), z0 - R * np.sin(t)]
    return np.r_[top, bot]


def _below(xy, level):
    """The part of a closed convex outline below the height `level` (a liquid in a tank)."""
    from chapter_1.geometry import clip_poly
    xy = np.asarray(xy, float)
    lo = xy[:, 1].min() - 1.0
    return clip_poly(xy, (xy[:, 0].min() - 1.0, xy[:, 0].max() + 1.0, lo, level))


def _nozzle_outline(x, z_top, height, r_c, r_t, r_e, chamber=0.32):
    """A small thrust chamber, nozzle down: chamber of radius r_c (`chamber` of the height; a nozzle fixed to
    a motor case has almost none), converging to the throat r_t, bell to r_e
    (chapter_1.launchers.bell_contour). Closed outline."""
    from chapter_1.launchers import bell_contour
    hc = chamber * height
    z_th = z_top - hc - 0.10 * height
    s, r = bell_contour(r_t, r_e, z_th - (z_top - height), theta_n=30.0, theta_e=9.0, n=30)
    conv = catmull_rom([(x + r_c, z_top - hc), (x + r_c, z_top - hc - 0.02 * height),
                        (x + 0.5 * (r_c + r_t), z_th + 0.04 * height), (x + r_t, z_th)], 6)
    half = np.r_[[(x + r_c, z_top)], conv, np.c_[x + r[1:], z_th - s[1:]]]
    other = np.c_[2 * x - half[::-1, 0], half[::-1, 1]]
    return np.r_[half, other]


def _valve(x, z, s):
    """A valve symbol (two triangles tip to tip across a vertical pipe) as one closed outline."""
    return np.array([(x - s, z + 0.6 * s), (x + s, z + 0.6 * s), (x - s, z - 0.6 * s), (x + s, z - 0.6 * s)])


def liquid_engine(feed="pump", origin=(0.0, 0.0), size=1.0):
    """A liquid bipropellant engine with its two tanks, nozzle down, as a schematic (not to scale):
    feed="pressure": a pressurant sphere above the tanks pushes the propellants through valves to the
    thrust chamber; feed="pump": a turbopump (a pump for each propellant on one shaft with a turbine,
    driven by a small gas generator that burns a little of both) feeds the chamber. Returns a schematic dict
    (draw it with draw_schematic): parts (name -> Part: fuel_tank, oxidizer_tank, thrust_chamber, and
    pressurant or fuel_pump, oxidizer_pump, turbine, gas_generator), points (the end of the turbine exhaust
    duct), liquids (part name -> (style, level)), pipes (open polylines), valves (name, center). Every part has
    an `inside` point for a leader.
    Example: S = liquid_engine("pressure", origin=(0, 0))"""
    ox, oz = origin
    k = size
    P, pipes, valves, liquids = {}, [], [], {}
    R = 0.55 * k
    xf, xo = ox - 0.80 * k, ox + 0.80 * k
    z_ch = oz + 2.30 * k                                       # top of the thrust chamber (the injector)
    P["thrust_chamber"] = Part("thrust_chamber", _nozzle_outline(ox, z_ch, 2.2 * k, 0.34 * k, 0.15 * k, 0.62 * k), "engine",
                               z=3.0, inside=(ox, z_ch - 0.35 * k))
    if feed == "pressure":
        t0, t1 = oz + 4.30 * k, oz + 5.30 * k
        P["fuel_tank"] = Part("fuel_tank", _capsule(xf, t0, t1, R), "tank", z=3.0, inside=(xf, t0 + 0.2 * k))
        P["oxidizer_tank"] = Part("oxidizer_tank", _capsule(xo, t0, t1, R), "tank", z=3.0, inside=(xo, t0 + 0.2 * k))
        zs = t1 + R + 0.95 * k
        P["pressurant"] = Part("pressurant", _circle(ox, zs, 0.42 * k), "tank", z=3.0, inside=(ox, zs))
        # pressurant lines: down from the sphere, split to the two tank tops
        zj = t1 + R + 0.30 * k
        pipes += [[(ox, zs - 0.42 * k), (ox, zj)], [(xf, t1 + R), (xf, zj), (xo, zj), (xo, t1 + R)]]
        valves.append(("regulator", (ox, 0.5 * (zs - 0.42 * k + zj))))
        zv = oz + 3.30 * k
        for xt, nm in ((xf, "fuel"), (xo, "oxidizer")):
            pipes.append([(xt, t0 - R), (xt, zv), (xt, z_ch + 0.30 * k), (ox + 0.5 * (xt - ox) * 0.25, z_ch + 0.30 * k),
                          (ox + 0.5 * (xt - ox) * 0.25, z_ch)])
            valves.append((f"{nm}_valve", (xt, zv)))
        liquids["fuel_tank"] = ("fuel", t1 - 0.05 * k)
        liquids["oxidizer_tank"] = ("oxidizer", t1 - 0.05 * k)
    elif feed == "pump":
        t0, t1 = oz + 5.75 * k, oz + 6.65 * k
        P["fuel_tank"] = Part("fuel_tank", _capsule(xf, t0, t1, R), "tank", z=3.0, inside=(xf, t0 + 0.2 * k))
        P["oxidizer_tank"] = Part("oxidizer_tank", _capsule(xo, t0, t1, R), "tank", z=3.0, inside=(xo, t0 + 0.2 * k))
        zp = oz + 4.15 * k                                     # the shaft of the pumps and the turbine
        rp = 0.25 * k
        P["fuel_pump"] = Part("fuel_pump", _circle(xf, zp, rp), "pump", z=3.2, inside=(xf, zp))
        P["oxidizer_pump"] = Part("oxidizer_pump", _circle(xo, zp, rp), "pump", z=3.2, inside=(xo, zp))
        tw, th = 0.26 * k, 0.30 * k                            # the turbine: a trapezoid on the shaft
        P["turbine"] = Part("turbine", np.array([(ox - tw, zp - th), (ox + tw, zp - 0.6 * th), (ox + tw, zp + 0.6 * th),
                                                 (ox - tw, zp + th)]), "pump", z=3.2, inside=(ox, zp))
        zg = zp - 0.85 * k                                     # the gas generator, below the turbine
        P["gas_generator"] = Part("gas_generator", np.array([(ox - 0.22 * k, zg - 0.17 * k), (ox + 0.22 * k, zg - 0.17 * k),
                                                             (ox + 0.22 * k, zg + 0.17 * k), (ox - 0.22 * k, zg + 0.17 * k)]),
                                  "pump", z=3.2, inside=(ox, zg))
        pipes.append([(xf + rp, zp), (ox - tw, zp)])           # the shaft
        pipes.append([(ox + tw, zp), (xo - rp, zp)])
        pipes += [[(xf, t0 - R), (xf, zp + rp)], [(xo, t0 - R), (xo, zp + rp)]]    # tanks to pumps
        pipes.append([(ox, zg + 0.17 * k), (ox, zp - th)])     # hot gas up to the turbine
        pipes.append([(ox, zp + th), (ox, zp + 0.95 * k)])     # turbine exhaust, up between the tanks
        zv = z_ch + 0.55 * k
        for xp_, nm in ((xf, "fuel"), (xo, "oxidizer")):
            xi = ox + 0.5 * (xp_ - ox) * 0.25
            pipes.append([(xp_, zp - rp), (xp_, zv), (xp_, z_ch + 0.22 * k), (xi, z_ch + 0.22 * k), (xi, z_ch)])
            valves.append((f"{nm}_valve", (xp_, zv)))
            pipes.append([(xp_, zg), (ox + np.sign(xp_ - ox) * 0.22 * k, zg)])   # a little of each to the gas generator
        liquids["fuel_tank"] = ("fuel", t1 - 0.05 * k)
        liquids["oxidizer_tank"] = ("oxidizer", t1 - 0.05 * k)
    else:
        raise ValueError("feed must be 'pressure' or 'pump'")
    points = {"turbine_exhaust": (ox, zp + 0.95 * k)} if feed == "pump" else {}
    return dict(parts=P, points=points, pipes=pipes, valves=valves, liquids=liquids, origin=(ox, oz), size=k,
                kind=f"liquid, {feed}-fed")


def _circle(x, z, r, n=60):
    t = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    return np.c_[x + r * np.cos(t), z + r * np.sin(t)]


def solid_motor(origin=(0.0, 0.0), size=1.0):
    """A solid rocket motor in section, nozzle down (schematic): the case (a cylinder with domes), the
    propellant grain cast against it (Chapter 1's solid hatch) with its central port, the igniter at the
    top of the port, and the nozzle. Returns a schematic dict (see liquid_engine): parts case, grain, port,
    igniter, nozzle. Example: S = solid_motor(origin=(4, 0))"""
    ox, oz = origin
    k = size
    R = 0.75 * k
    z0, z1 = oz + 2.4 * k, oz + 5.6 * k
    case = _capsule(ox, z0, z1, R)
    P = {}
    P["case"] = Part("case", case, "case", z=3.0, inside=(ox - 0.93 * R, 0.5 * (z0 + z1)))
    rin = R - 0.07 * k
    grain = _capsule(ox, z0, z1, rin)
    rp = 0.20 * k
    port = np.array([(ox - rp, z0 - 0.55 * k), (ox + rp, z0 - 0.55 * k), (ox + rp, z1 + 0.30 * k), (ox - rp, z1 + 0.30 * k)])
    P["grain"] = Part("grain", grain, "grain", z=3.1, inside=(ox - 0.55 * R, 0.5 * (z0 + z1) + 0.4 * k))
    P["port"] = Part("port", port, "port", z=3.2, inside=(ox, 0.5 * (z0 + z1) - 0.3 * k))
    P["igniter"] = Part("igniter", np.array([(ox - 0.12 * k, z1 + 0.05 * k), (ox + 0.12 * k, z1 + 0.05 * k),
                                             (ox + 0.12 * k, z1 + 0.30 * k), (ox - 0.12 * k, z1 + 0.30 * k)]),
                        "detail", z=3.3, inside=(ox, z1 + 0.18 * k))
    zt = z0 - R + 0.10 * k
    P["nozzle"] = Part("nozzle", _nozzle_outline(ox, zt, 1.6 * k, 0.30 * k, 0.16 * k, 0.55 * k, chamber=0.04), "engine",
                       z=2.9, inside=(ox, zt - 1.1 * k))
    return dict(parts=P, points={}, pipes=[], valves=[], liquids={}, origin=(ox, oz), size=k, kind="solid",
                solids={"grain": "solid"}, voids=["port"])


def hybrid_motor(origin=(0.0, 0.0), size=1.0):
    """A hybrid rocket motor, nozzle down (schematic): a liquid oxidizer tank above, a valve, and a case
    holding a solid fuel grain with its port, then the nozzle. Returns a schematic dict (see liquid_engine):
    parts oxidizer_tank, case, grain, port, nozzle; the oxidizer feed line and its valve.
    Example: S = hybrid_motor(origin=(8, 0))"""
    ox, oz = origin
    k = size
    P = {}
    R = 0.55 * k
    t0, t1 = oz + 5.30 * k, oz + 6.10 * k
    P["oxidizer_tank"] = Part("oxidizer_tank", _capsule(ox, t0, t1, R), "tank", z=3.0, inside=(ox, t0 + 0.1 * k))
    Rc = 0.62 * k
    z0, z1 = oz + 2.4 * k, oz + 4.4 * k
    case = np.array([(ox - Rc, z0), (ox + Rc, z0), (ox + Rc, z1), (ox - Rc, z1)])
    P["case"] = Part("case", case, "case", z=3.0, inside=(ox + 0.93 * Rc, 0.5 * (z0 + z1)))
    rin = Rc - 0.07 * k
    P["grain"] = Part("grain", np.array([(ox - rin, z0 + 0.12 * k), (ox + rin, z0 + 0.12 * k), (ox + rin, z1 - 0.12 * k),
                                         (ox - rin, z1 - 0.12 * k)]), "grain", z=3.1,
                      inside=(ox + 0.55 * Rc, 0.5 * (z0 + z1) + 0.3 * k))
    rp = 0.20 * k
    P["port"] = Part("port", np.array([(ox - rp, z0), (ox + rp, z0), (ox + rp, z1), (ox - rp, z1)]), "port", z=3.2,
                     inside=(ox, 0.5 * (z0 + z1)))
    P["nozzle"] = Part("nozzle", _nozzle_outline(ox, z0, 1.6 * k, 0.30 * k, 0.16 * k, 0.55 * k, chamber=0.04), "engine",
                       z=2.9, inside=(ox, z0 - 1.1 * k))
    zv = 0.5 * (z1 + t0 - R)
    pipes = [[(ox, t0 - R), (ox, z1)]]
    return dict(parts=P, points={}, pipes=pipes, valves=[("oxidizer_valve", (ox, zv))],
                liquids={"oxidizer_tank": ("oxidizer", t1 - 0.05 * k)}, origin=(ox, oz), size=k, kind="hybrid",
                solids={"grain": "solid fuel"}, voids=["port"])


def draw_schematic(ax, S, highlight=(), lw_pipe=1.4):
    """Draw a schematic from liquid_engine, solid_motor or hybrid_motor in the chapter's one style: tanks,
    pumps, cases and the thrust chamber white with black outlines (LW_DETAIL + 0.4); liquids filled to their
    level with the oxidizer and fuel tints of Chapter 1's cutaways (LIQUID_STYLE); a solid grain with the
    solid hatch, its port white; pipes as 1.4 pt black lines; valves as two small triangles. Every detail
    is drawn on its part (on_part), so a leader may end inside a liquid or a grain. Returns a dict of
    patches by part name. Example: P = draw_schematic(ax, liquid_engine("pump"))"""
    P = {}
    lw = LW_DETAIL + 0.4
    for name, p in sorted(S["parts"].items(), key=lambda kv: kv[1].z):
        if p.kind in ("grain", "port"):
            continue
        fc = HIGHLIGHT if name in highlight else "white"
        P[name] = _poly(ax, p.xy, fc=fc, lw=lw, z=p.z)
        P[name]._part = name
    for name, (sty, level) in S["liquids"].items():
        st = LIQUID_STYLE[sty]
        xy = _below(S["parts"][name].xy, level)
        fp, ed = _fill_poly(ax, xy, st, S["parts"][name].z + 0.1, edge_lw=0.0)
        ed.set_visible(False)
        on_part(fp, P[name])
        at = xy[np.abs(xy[:, 1] - level) < 1e-9]
        sl = ax.plot([at[:, 0].min(), at[:, 0].max()], [level, level], color=INK, lw=LW_FINE,
                     zorder=S["parts"][name].z + 0.2)[0]
        on_part(sl, P[name])
        P[name + "#liquid"] = fp
    for name, sty in S.get("solids", {}).items():
        p = S["parts"][name]
        fp, ed = _fill_poly(ax, p.xy, LIQUID_STYLE[sty], p.z, edge_lw=LW_DETAIL)
        host = P.get("case")
        if host is not None:
            on_part(fp, host)
            on_part(ed, host)
        P[name] = ed
        P[name + "#fill"] = fp
    for name in S.get("voids", []):
        p = S["parts"][name]
        pa = _poly(ax, p.xy, fc="white", lw=LW_DETAIL, z=p.z)
        if "case" in P:
            on_part(pa, P["case"])
        P[name] = pa
    # the feed system's envelope (the hull of every part and pipe, invisible): pipes and valves are drawn on it,
    # so a leader that ends on a component inside it may cross a pipe on its way (as in any feed schematic)
    from chapter_1.geometry import hull
    pts = np.vstack([p.xy for p in S["parts"].values()] + [np.asarray(pl, float) for pl in S["pipes"]])
    env = Polygon(np.asarray(hull([tuple(q) for q in pts]), float), closed=True, fc="none", ec="none", lw=0.0, zorder=0.1)
    ax.add_patch(env)
    P["#envelope"] = env
    for pl in S["pipes"]:
        q = np.asarray(pl, float)
        ln = ax.plot(q[:, 0], q[:, 1], color=INK, lw=lw_pipe, zorder=2.5, solid_joinstyle="miter", solid_capstyle="butt")[0]
        on_part(ln, env)
        P.setdefault("#pipes", []).append(ln)
    s = 0.13 * S["size"]
    for name, (x, z) in S["valves"]:
        pa = _poly(ax, _valve(x, z, s), fc="white", lw=LW_DETAIL, z=3.4)
        on_part(pa, env)
        P[name] = pa
    return P


# ===================================================================== (h) log-log charts with direct labels
def log_axis(ax, axis="x", lo=None, hi=None, style="comma", label=None):
    """A logarithmic axis with a label at every decade: style "comma" ("0.1", "1", "1,000", "100,000") or
    "power" ($10^{-3}$; single-digit superscripts are allowed by the SVG check). Minor ticks unlabeled.
    Example: log_axis(ax, "y", 100, 1e6, "comma", "Payload to low Earth orbit, kg")"""
    import matplotlib.ticker as mt
    a = ax.xaxis if axis == "x" else ax.yaxis
    (ax.set_xscale if axis == "x" else ax.set_yscale)("log")
    if lo is not None:
        (ax.set_xlim if axis == "x" else ax.set_ylim)(lo, hi)

    def f(v, _):
        e = int(round(math.log10(v)))
        if abs(v - 10.0 ** e) > 1e-9 * v:
            return ""
        if style == "power":
            return f"$10^{{{e}}}$".replace("-", "−")         # every decade as a power of ten, 10^0 and 10^1 too
        return f"{v:,.0f}" if e >= 0 else f"{v:.{-e}f}"
    if lo is not None:                                   # only the decades inside the view (a hidden tick label counts)
        a.set_major_locator(mt.FixedLocator([10.0 ** e for e in range(math.ceil(math.log10(lo) - 1e-9),
                                                                       math.floor(math.log10(hi) + 1e-9) + 1)]))
    else:
        a.set_major_locator(mt.LogLocator(base=10.0, numticks=30))
    a.set_major_formatter(mt.FuncFormatter(f))
    a.set_minor_locator(mt.LogLocator(base=10.0, subs=tuple(range(2, 10)), numticks=30))
    a.set_minor_formatter(mt.NullFormatter())
    if label:
        (ax.set_xlabel if axis == "x" else ax.set_ylabel)(label)


def _obstacles(ax, skip=()):
    """Display points of every visible line, patch edge and marker of ax (grid excluded), for placing labels."""
    from figkit import _densify
    pts = []
    grid = set(ax.get_xgridlines()) | set(ax.get_ygridlines())
    for ln in ax.lines:
        if ln in grid or not ln.get_visible() or ln in skip:
            continue
        xy = ln.get_transform().transform(np.c_[ln.get_xdata(), ln.get_ydata()].astype(float))
        if ln.get_linestyle() not in ("None", "", " "):
            pts.append(_densify(xy, 1.5))
        if ln.get_marker() not in ("None", None, "", " "):
            ms = ln.get_markersize() * ax.figure.dpi / 72.0
            for p in xy[np.all(np.isfinite(xy), axis=1)]:
                t = np.linspace(0, 2 * math.pi, 12)
                pts.append(p + 0.5 * ms * np.c_[np.cos(t), np.sin(t)])
    for pa in ax.patches:
        if not pa.get_visible() or pa in skip or pa.get_edgecolor()[3] == 0 or pa.get_linewidth() == 0:
            continue
        for poly in pa.get_transform().transform_path(pa.get_path()).to_polygons(closed_only=False):
            pts.append(_densify(poly, 1.5))
    return np.vstack(pts) if pts else np.zeros((0, 2))


def place_labels(ax, requests, pad=1.8, fs=FS_LABEL):
    """Place direct labels where they touch no line, edge, marker or label already drawn: each request is a
    dict(text, candidates=[(x, y, ha, va), ...] in data units, color, backing) and the first clear candidate
    wins (the last one is used, with a printed note, when none is clear). Returns the Text objects.
    Example: place_labels(ax, [dict(text="bipropellant", candidates=[(1e3, 400, "left", "bottom")])])"""
    fig = ax.figure
    out = []
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    obs = _obstacles(ax)
    k = fig.dpi / 72.0
    from matplotlib.text import Text as _T
    placed = []                                            # labels already on the axes count as placed
    for t0 in ax.texts:
        if t0.get_visible() and t0.get_text().strip():
            b0 = _T.get_window_extent(t0, rend)
            placed.append((b0.x0 - 1.6 * k, b0.y0 - 1.6 * k, b0.x1 + 1.6 * k, b0.y1 + 1.6 * k))
    for rq in requests:
        chosen = None
        for (x, y, ha, va) in rq["candidates"]:
            t = ax.text(x, y, rq["text"], ha=ha, va=va, fontsize=rq.get("fs", fs), color=rq.get("color", INK),
                        zorder=rq.get("zorder", 10), linespacing=1.15,
                        bbox=dict(boxstyle="square,pad=0.12", fc=rq.get("backing", "white"), ec="none")
                        if rq.get("backing", "white") else None)
            from matplotlib.text import Text as _T
            bb = _T.get_window_extent(t, rend)              # the glyphs; the backing adds about 1.5 pt
            e = (pad + 1.6) * k
            x0, y0, x1, y1 = bb.x0 - e, bb.y0 - e, bb.x1 + e, bb.y1 + e
            axb = ax.get_window_extent(rend)
            inside_ax = bb.x0 >= axb.x0 and bb.x1 <= axb.x1 and bb.y0 >= axb.y0 and bb.y1 <= axb.y1
            hit = len(obs) and np.any((obs[:, 0] > x0) & (obs[:, 0] < x1) & (obs[:, 1] > y0) & (obs[:, 1] < y1))
            hit = hit or any(not (x1 < b[0] or b[2] < x0 or y1 < b[1] or b[3] < y0) for b in placed)
            if not hit and inside_ax:
                chosen = t
                placed.append((x0, y0, x1, y1))
                break
            t.remove()
        if chosen is None:
            x, y, ha, va = rq["candidates"][-1]
            print(f"   place_labels: no clear spot for {rq['text']!r}; the gate will say where it touches")
            chosen = ax.text(x, y, rq["text"], ha=ha, va=va, fontsize=rq.get("fs", fs), color=rq.get("color", INK),
                             zorder=10, bbox=dict(boxstyle="square,pad=0.12", fc=rq.get("backing", "white"), ec="none"))
        out.append(chosen)
    return out


RANGE_STYLES = [dict(color=INK, ls="-"), dict(color=SERIES[0], ls=(0, (6.0, 2.5))), dict(color=SERIES[1], ls=(0, (1.2, 2.0))),
                dict(color=STEEL, ls=(0, (7.0, 2.2, 1.4, 2.2))), dict(color=SERIES[2], ls=(0, (6.0, 1.8, 1.2, 1.8, 1.2, 1.8))),
                dict(color=SERIES[3], ls="-"), dict(color="#8E6F3E", ls=(0, (3.0, 1.5)))]
RANGE_TEXT = [INK, SERIES[0], "#B34E00", STEEL, "#007A5A", "#A0507F", "#7A5C2E"]


def range_boxes(ax, items, lw=1.6, fs=FS_LABEL, fill_alpha=0.10):
    """One box per item on logarithmic axes (the specific impulse against thrust map): items are dicts
    (name, x0, x1, y0, y1[, label_at=(x, y, ha, va) list]) and each box is outlined in its own color and
    line style (RANGE_STYLES), so overlapping boxes stay apart in grayscale. The name is placed inside its
    box where it touches no other box (place_labels; candidates: the box's corners and center, or
    label_at), or, with callout=(x, y) and target=(x, y), outside it with a short leader to a point inside it
    (where the boxes overlap, such a leader may cross another box's edge: the boxes are regions of one plot
    and all of them are drawn on the plot's area). Each box has a light fill of its color (fill_alpha), so
    overlaps read. Returns (patches, labels). Example: range_boxes(ax, [dict(name="solid", x0=37, x1=1.2e7, y0=187, y1=296)])"""
    patches, reqs = [], []
    for i, it in enumerate(items):
        st = RANGE_STYLES[i % len(RANGE_STYLES)]
        from matplotlib.colors import to_rgba
        fc = to_rgba(st["color"], fill_alpha) if it.get("fill", True) else "none"    # fill=False: outline only
        r = Rectangle((it["x0"], it["y0"]), it["x1"] - it["x0"], it["y1"] - it["y0"], fc=fc,
                      ec=st["color"], lw=lw, ls=st["ls"], zorder=3 + 0.01 * i)
        ax.add_patch(r)
        patches.append(r)
    area = Rectangle((0, 0), 1, 1, transform=ax.transAxes, fc="none", ec="none", lw=0.0, zorder=0.1)
    ax.add_patch(area)
    for r in patches:
        on_part(r, area)
    ax.figure.canvas.draw()
    labels = [None] * len(items)
    for i, it in enumerate(items):
        if "callout" in it:
            t = callout(ax, it["target"], it["name"], it["callout"], fs=fs, color=RANGE_TEXT[i % len(RANGE_TEXT)],
                        ha=it.get("ha"))
            t.arrow_patch.set_gid("leader")
            labels[i] = t
    for i, it in enumerate(items):
        if "callout" in it:
            continue
        gx, gy = math.sqrt(it["x0"] * it["x1"]), math.sqrt(it["y0"] * it["y1"])
        fx, fy = (it["x1"] / it["x0"]) ** 0.06, (it["y1"] / it["y0"]) ** 0.10
        cands = it.get("label_at") or [(gx, gy, "center", "center"), (it["x0"] * fx, it["y1"] / fy, "left", "top"),
                                       (it["x1"] / fx, it["y1"] / fy, "right", "top"),
                                       (it["x0"] * fx, it["y0"] * fy, "left", "bottom"),
                                       (it["x1"] / fx, it["y0"] * fy, "right", "bottom")]
        from matplotlib.colors import to_rgb
        c = np.array(to_rgb(RANGE_STYLES[i % len(RANGE_STYLES)]["color"]))
        back = tuple(1.0 - fill_alpha * (1.0 - c))          # the box's own fill as seen over white
        reqs.append((i, dict(text=it["name"], candidates=cands, color=RANGE_TEXT[i % len(RANGE_TEXT)], fs=fs,
                             backing=back)))
    for (i, _), t in zip(reqs, place_labels(ax, [r for _, r in reqs], fs=fs)):
        labels[i] = t
    return patches, labels


def class_bands(ax, classes, axis="y", fills=("#F2F2F2", "#FFFFFF"), fs=FS_SMALL, label_x=None, ha="right"):
    """Shaded bands across a plot for classes along one axis (launch-vehicle classes by payload): classes is
    a list of (name, lo, hi); bands alternate the two fills, their edges thin gray dashed lines, each named
    inside the band at label_x (data units; default the right end, right-aligned; ha="left" with a label_x
    near the left end) on the band's own fill. Returns the band patches.
    Example: class_bands(ax, LV_CLASSES)"""
    out = []
    lim = ax.get_ylim() if axis == "y" else ax.get_xlim()
    for i, (name, lo, hi) in enumerate(classes):
        lo_, hi_ = max(lo, lim[0]), min(hi, lim[1])
        if hi_ <= lo_:
            continue
        fc = fills[i % len(fills)]
        if axis == "y":
            band = ax.axhspan(lo_, hi_, fc=fc, ec="none", zorder=0.5)
            for v in (lo, hi):
                if lim[0] < v < lim[1]:
                    ax.axhline(v, color=GRAY, lw=LW_THIN, ls=(0, (4.0, 3.0)), zorder=0.6)
            xl = label_x if label_x is not None else ax.get_xlim()[1]
            ym = math.sqrt(lo_ * hi_) if ax.get_yscale() == "log" else 0.5 * (lo_ + hi_)
            ax.text(xl, ym, name, ha=ha, va="center", fontsize=fs, color=STEEL, zorder=1,
                    bbox=dict(boxstyle="square,pad=0.12", fc=fc, ec="none"))
        else:
            band = ax.axvspan(lo_, hi_, fc=fc, ec="none", zorder=0.5)
        out.append(band)
    return out


def named_scatter(ax, points, ms=6.5, fs=FS_SMALL, marker="o", color=INK, mfc="white", dist=5.0, backing="white"):
    """Points with names placed beside them where they touch nothing (place_labels; the eight directions
    around the point are tried in order, or the point's own `label_at` list). points: dicts (name, x, y[,
    marker][, label_at]). Returns the labels. Example: named_scatter(ax, [dict(name="Falcon 9", x=5.49e5, y=22800)])"""
    for p in points:
        ax.plot([p["x"]], [p["y"]], p.get("marker", marker), ms=ms, mfc=p.get("mfc", mfc), mec=color, mew=1.4, zorder=6)
    ax.figure.canvas.draw()
    inv = ax.transData.inverted()
    reqs = []
    k = ax.figure.dpi / 72.0
    for p in points:
        c = ax.transData.transform((p["x"], p["y"]))
        d = (dist + ms / 2) * k
        dirs = [(1, 0, "left", "center"), (-1, 0, "right", "center"), (0, 1, "center", "bottom"),
                (0, -1, "center", "top"), (0.75, 0.75, "left", "bottom"), (-0.75, 0.75, "right", "bottom"),
                (0.75, -0.75, "left", "top"), (-0.75, -0.75, "right", "top")]
        cands = p.get("label_at") or [(*inv.transform(c + d * np.array([dx, dy])), ha, va) for dx, dy, ha, va in dirs]
        reqs.append(dict(text=p["name"], candidates=cands, fs=fs, backing=backing))   # backing None: no box
    return place_labels(ax, reqs, fs=fs)


# ===================================================================== (i) tanks inside a stage
def sphere_diameter(volume):
    """Diameter (m) of a sphere of the given volume (m^3): (6 V / pi)^(1/3). Example: sphere_diameter(7.94) -> 2.475"""
    return (6.0 * volume / math.pi) ** (1.0 / 3.0)


def _cap_height(R, V):
    """Height h of liquid in a sphere of radius R holding the volume V: pi h^2 (3R - h) / 3 = V (bisection)."""
    lo, hi = 0.0, 2.0 * R
    for _ in range(100):
        h = 0.5 * (lo + hi)
        if math.pi * h * h * (3.0 * R - h) / 3.0 < V:
            lo = h
        else:
            hi = h
    return 0.5 * (lo + hi)


def tanks_in_stage(ax, stage_d, tanks, origin=(0.0, 0.0), gap=0.25, wall_lw=LW_OUTLINE, fs=FS_LABEL, margin=0.3,
                   zorder=3.0):
    """Spherical tanks stacked inside a stage of diameter stage_d (m), to scale, nozzle side down: tanks is a
    list, lowest first, of dicts (name, liquid volume m^3, ullage: the gas space added on top of the liquid
    volume, as a fraction of it, style: a LIQUID_STYLE key). Each tank's volume is the liquid volume x
    (1 + ullage) and its diameter follows; the liquid fills it from the bottom to the height that holds the liquid volume, the ullage gas
    above it is white. The stage is drawn as its two side walls (cut lines at the ends). Asserts that every
    tank fits the stage and that the drawn liquid holds the stated volume. Returns a dict: tanks (name ->
    dict(center, D, level, patch, liquid)), top, bottom, walls.
    Example: tanks_in_stage(ax, 3.0, [dict(name="kerosene", volume=4.11, ullage=0.05, style="fuel"), ...])"""
    x, y = origin
    out = dict(tanks={}, bottom=y)
    zc = y + margin
    for t in tanks:
        Vt = t["volume"] * (1.0 + t["ullage"])
        D = sphere_diameter(Vt)
        R = 0.5 * D
        assert D <= stage_d + 1e-9, f"tank {t['name']}: {D:.3f} m does not fit a {stage_d} m stage"
        cz = zc + R
        circ = _circle(x, cz, R, 120)
        pa = _poly(ax, circ, fc="white", lw=LW_DETAIL + 0.4, z=zorder + 0.5)
        h = _cap_height(R, t["volume"])
        close_to(math.pi * h * h * (3 * R - h) / 3.0, t["volume"], 1e-9 * t["volume"], "liquid volume in the tank")
        level = cz - R + h
        liq = _below(circ, level)
        fp, ed = _fill_poly(ax, liq, LIQUID_STYLE[t["style"]], zorder + 0.6, edge_lw=0.0)
        ed.set_visible(False)
        on_part(fp, pa)
        hw = math.sqrt(max(R * R - (level - cz) ** 2, 0.0))
        sl = ax.plot([x - hw, x + hw], [level, level], color=INK, lw=LW_FINE, zorder=zorder + 0.7)[0]
        on_part(sl, pa)
        out["tanks"][t["name"]] = dict(center=(x, cz), D=D, R=R, level=level, patch=pa, liquid=fp, V_tank=Vt)
        zc = cz + R + gap
    top = zc - gap + margin
    out["top"] = top
    # the stage: an invisible region the walls and tanks are drawn on (a leader that ends inside it may cross a wall)
    region = Polygon([(x - stage_d / 2, y), (x + stage_d / 2, y), (x + stage_d / 2, top), (x - stage_d / 2, top)],
                     closed=True, fc="none", ec="none", lw=0.0, zorder=0.1)
    ax.add_patch(region)
    walls = []
    for sx in (-1, 1):
        walls.append(on_part(ax.plot([x + sx * stage_d / 2] * 2, [y, top], color=INK, lw=wall_lw, zorder=zorder)[0], region))
    for yy in (y, top):
        walls.append(on_part(ax.plot([x - stage_d / 2, x + stage_d / 2], [yy, yy], color=GRAY, lw=LW_THIN,
                                     ls=(0, (6.0, 3.0)), zorder=zorder - 0.5)[0], region))
    for t in out["tanks"].values():
        on_part(t["patch"], region)
    out["walls"] = walls
    out["region"] = region
    return out


# ===================================================================== (j) a temperature scale
def temperature_axis(ax, lo, hi, step=50.0, step_c=None, label_k="Temperature, K", label_c="Temperature, °C"):
    """A vertical temperature scale on a data axes: kelvin on the left (lo to hi, a tick every `step`) and
    degrees Celsius on the right (a secondary axis, T - 273.15, a tick every step_c, default `step`).
    Returns the secondary axis. Example: sec = temperature_axis(ax, 0, 400, 50)"""
    import matplotlib.ticker as mt
    ax.set_ylim(lo, hi)
    ax.yaxis.set_major_locator(mt.MultipleLocator(step))
    ax.set_ylabel(label_k)
    sec = ax.secondary_yaxis("right", functions=(lambda T: T - 273.15, lambda c: c + 273.15))
    sec.yaxis.set_major_locator(mt.MultipleLocator(step_c or step))
    sec.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:,.0f}".replace("-", "−")))
    sec.set_ylabel(label_c)
    ax.spines["right"].set_visible(False)
    return sec


def arrow_key(ax, xy, entries, dy=18.0, length=26.0, fs=FS_SMALL):
    """A key naming the arrow kinds of a figure (point 30), one sample arrow per kind stacked downward from
    xy (data), with its name to the right: kinds are Chapter 1's ("force", "velocity", "flow", ...) and
    "pressure" (PRESSURE_ARROW). entries: list of (kind, name), or (kind, name, style) where style changes
    the color and line weight of a pressure arrow (two pressures told apart, as p_a and p_e). Returns the
    bottom y. Example: arrow_key(ax, (0, 0), [("pressure", "pressure"), ("force", "force"), ("flow", "flow of gas")])"""
    from chapter_1.style import legend_key
    fig = ax.figure
    fig.canvas.draw()
    inv = ax.transData.inverted()
    p = ax.transData.transform(xy)
    k = fig.dpi / 72.0
    y = p[1]
    for entry in entries:
        kind, name = entry[0], entry[1]
        sty = dict(PRESSURE_ARROW, **(entry[2] if len(entry) > 2 else {}))
        a, b = inv.transform((p[0], y)), inv.transform((p[0] + length * k, y))
        if kind == "pressure":
            arrow(ax, a, b, color=sty["color"], lw=sty["lw"], head=sty["head"])
            text(ax, b, name, direction=0.0, dist=6.0, fs=fs)
        else:
            legend_key(ax, a, [(kind, name)], fs=fs, length=length)
        y -= dy * k
    return inv.transform((p[0], y))[1]


def math_row(ax, xy, pieces, fs=FS_LABEL, color=INK, gap=3.0, va="center", zorder=10):
    """Write a short relation such as "p_e < p_a" as separate text pieces side by side, starting at xy (data,
    left end). Needed when one label would hold two single-letter subscripts: matplotlib groups the small
    glyphs of one label together in the SVG, and the kit's SVG check then reads "ea" as a word subscript.
    pieces: strings ("$p_e$", "<", "$p_a$"). Returns the Text objects.
    Example: math_row(ax, (5.0, 1.0), ["$p_e$", "<", "$p_a$"])"""
    out = []
    x, y = xy
    g = _pt(ax, gap)
    for s in pieces:
        t = text(ax, (x, y), s, ha="left", va=va, fs=fs, color=color, zorder=zorder)
        w, _ = text_size(ax, s, fs)
        x += w + g
        out.append(t)
    return out


def mass_key(ax, xy, kinds=MASS_ORDER, w=18.0, h=10.0, dy=16.0, fs=FS_SMALL, horizontal=True, gap=14.0):
    """A key to the mass looks (MASS_STYLE): one small swatch per kind with its name, in a row from xy (data,
    the left end of the first swatch's middle) or a column (horizontal=False). Returns the patches.
    Example: mass_key(ax, (0.0, -3.0))"""
    out = []
    x, y = xy
    for kind in kinds:
        st = MASS_STYLE[kind]
        ww, hh = _pt(ax, w), _pt(ax, h)
        rect = [(x, y - hh / 2), (x + ww, y - hh / 2), (x + ww, y + hh / 2), (x, y + hh / 2)]
        out.append(_fill_poly(ax, rect, st, 3.0, LW_DETAIL))
        t = text(ax, (x + ww, y), st["name"], direction=0.0, dist=4.0, fs=fs)
        if horizontal:
            tw, _ = text_size(ax, st["name"], fs)
            x += ww + _pt(ax, 4.0) + tw + _pt(ax, gap)
        else:
            y -= _pt(ax, dy)
    return out
