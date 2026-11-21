"""Drawing helpers for hardware: vehicles, airfoils, wings and landing gear, in the chapter
style (line art: white opaque parts, black outlines, light gold for the part a figure is
about, hatched control surfaces). The shapes come from chapter_1.geometry.

    parts = aircraft_side()
    patches = draw_parts(ax, parts, highlight=("wing",))
    label_part(ax, patches, parts, "vtail", "vertical stabilizer", at=(30.0, 11.0))
"""
import math

import numpy as np

from chapter_1.style import *  # noqa: F401,F403
from chapter_1.style import _screen_angle  # noqa: F401
from chapter_1.geometry import (Part, naca4, planform, chord_at, mac_construction, GEAR_LAYOUTS, GEAR_BODY,
                                gear_wing_edges, superellipse,
                                clip_poly, clip_line, polygon_area,  # noqa: F401
                                circle_xy, superellipse)
from matplotlib.patches import Polygon


def _part_style(p, highlight, surfaces):
    hidden = p.hidden
    if hidden:
        return dict(fc="none", ec=INK, lw=LW_DETAIL, ls=(0, (3.0, 2.0)), hatch=None)
    if p.kind == "surface":
        # the two wings of a plan view are mirror images, and so are their hatches: the left
        # wing ("_L") gets the hatch reflected, so a slat looks the same on both sides
        hatch = HATCH_SURFACE.replace("/", "\\") if str(p.name).endswith("_L") else HATCH_SURFACE
        if p.name in highlight:
            return dict(fc=HIGHLIGHT, ec=INK, lw=LW_DETAIL, ls="-", hatch=hatch)
        fc = SURFACE_FILL if surfaces == "hatch" else PART_FILL
        return dict(fc=fc, ec=INK, lw=LW_DETAIL, ls="-", hatch=hatch if surfaces == "hatch" else None)
    if p.kind == "detail":
        if getattr(p, "on", None):                           # drawn on a part: outline only, thin
            return dict(fc="none", ec=getattr(p, "ec", INK), lw=getattr(p, "lw", None) or LW_FINE, ls="-", hatch=None)
        return dict(fc=PART_FILL, ec=getattr(p, "ec", INK), lw=LW_DETAIL, ls="-", hatch=None)
    if p.kind == "strut":
        return dict(fc=HIGHLIGHT if p.name in highlight else PART_FILL, ec=INK, lw=LW_DETAIL + 0.2, ls="-", hatch=None)
    fc = HIGHLIGHT if p.name in highlight else PART_FILL
    return dict(fc=fc, ec=INK, lw=LW_OUTLINE, ls="-", hatch=None)


def draw_parts(ax, parts, highlight=(), only=None, surfaces="plain", zbase=0.0, details=True):
    """Draw the parts (a dict from aircraft_side(), aircraft_top(), launch_vehicle(), ...) as
    line art: each part an opaque closed shape (so a part behind another is hidden where it is
    covered), black outline, LW_OUTLINE for the outer parts and LW_DETAIL for control surfaces
    and details; `highlight` names parts filled with HIGHLIGHT (the part a figure is about; a
    highlighted control surface is also hatched, so it reads in grayscale); surfaces="plain"
    (default) draws control surfaces as white outlined shapes, "hatch" fills them all light gray
    with HATCH_SURFACE; hidden parts (inside a fairing or a stage) are thin dashed lines. `only`
    limits the parts drawn; details=False leaves out every detail and hidden part (the plain
    outline). A detail drawn on a part (Part.on: a window on the fuselage, a hidden tank in a
    stage) is a thin outline the gate lets a leader cross when the leader ends inside that part
    (figkit.on_part). A "ground" part is a thin gray line.
    Returns a dict name -> patch. Set equal aspect (new_axes does). Example: P = draw_parts(ax, aircraft_top())"""
    out = {}
    for name, p in sorted(parts.items(), key=lambda kv: kv[1].z):
        if only is not None and name not in only:
            continue
        if not details and (p.hidden or p.kind in ("detail", "line")):
            continue
        if p.kind == "ground":
            out[name] = ax.plot(p.xy[:, 0], p.xy[:, 1], color=GRAY, lw=LW_THIN, zorder=zbase + p.z,
                                solid_capstyle="butt")[0]
            continue
        if p.kind == "line":                                  # an open line on a part (a joint)
            out[name] = ax.plot(p.xy[:, 0], p.xy[:, 1], color=INK, lw=LW_DETAIL if not getattr(p, "on", None) else LW_FINE,
                                zorder=zbase + p.z, solid_capstyle="butt")[0]
            continue
        st = _part_style(p, highlight, surfaces)
        pa = Polygon(p.xy, closed=True, fc=st["fc"], ec=st["ec"], lw=st["lw"], ls=st["ls"], joinstyle="round",
                     zorder=zbase + p.z)
        if st["hatch"] or getattr(p, "hatch", None):
            pa.set_hatch(getattr(p, "hatch", None) or st["hatch"])
        ax.add_patch(pa)
        if not p.hidden and st["fc"] != "none":
            opaque(pa)
        pa._part = name
        out[name] = pa
    for name, a in out.items():                             # details: drawn on their part
        host = getattr(parts[name], "on", None)
        if host is not None and host in out:
            on_part(a, out[host])
    return out


def name_parts(ax, patches, parts, names, fs=FS_LABEL):
    """label_part for several parts: names maps a part name to (text, at) or (text, at, kwargs).
    Example: name_parts(ax, P, parts, {"wing": ("wing", (20, 8)), "vtail": ("fin", (30, 12), dict(ha="right"))})"""
    out = {}
    for name, spec in names.items():
        kw = dict(spec[2]) if len(spec) > 2 else {}
        kw.setdefault("fs", fs)
        out[name] = label_part(ax, patches, parts, name, spec[0], spec[1], **kw)
    return out


def label_part(ax, patches, parts, name, text_, at, fs=FS_LABEL, ha=None, va="center", gap=1.5, target=None,
               backing=True):
    """Name a drawn part: the label at `at` (data) with a short straight leader that ends inside
    the part (at its `inside` point, or `target`), with a small dot there. The gate lets the
    leader cross only the outlines of shapes that contain its end (the part, and a larger part
    it lies on). Returns the annotation. Example: label_part(ax, P, parts, "aileron_L", "aileron", at=(28, 15))"""
    tgt = np.asarray(target if target is not None else parts[name].inside, dtype=float)
    an = callout(ax, tgt, text_, at, gap=gap, fs=fs, ha=ha, va=va, backing=backing)
    ax.plot(*tgt, "o", ms=2.6, color=INK, zorder=12, gid=f"grp:lead-{name}")
    an.arrow_patch.set_gid("leader")
    return an


# ===================================================================== airfoils
def draw_section(ax, sec, origin=(0.0, 0.0), chord_line=True, camber_line=True, fill=PART_FILL, lw=LW_OUTLINE,
                 zorder=3):
    """Draw a naca4() section at `origin` (data, the leading edge): the outline (opaque,
    LW_OUTLINE), and on top of it the chord line (thin dashed gray, from the leading to the
    trailing edge) and the mean camber line (black dash-dot). Returns a dict outline,
    chord, camber (artists). Example: draw_section(ax, naca4("4418", chord=1.0))"""
    o = np.asarray(origin, dtype=float)
    out = {}
    pa = Polygon(sec["outline"] + o, closed=True, fc=fill, ec=INK, lw=lw, joinstyle="round", zorder=zorder)
    ax.add_patch(pa)
    out["outline"] = pa
    if chord_line:
        out["chord"] = ax.plot([o[0], o[0] + sec["chord"]], [o[1], o[1]], **line_kw("boundary"),
                               zorder=zorder + 1)[0]
    if camber_line and sec["m"] > 0:
        out["camber"] = ax.plot(o[0] + sec["x"], o[1] + sec["yc"], color=INK, lw=1.3,
                                ls=(0, (7.0, 2.2, 1.4, 2.2)), zorder=zorder + 1.2)[0]
    return out


# ===================================================================== wing planform
def planform_xy(pf, both=False, origin=(0.0, 0.0)):
    """Closed outline (x aft, y to the left) of a planform() wing: the right half (y >= 0, root on
    the centerline at `origin`), or both halves. Example: xy = planform_xy(pf, both=True)"""
    c = pf["corners"] + np.asarray(origin, dtype=float)
    if not both:
        return c
    m = c * np.array([1.0, -1.0]) + np.array([0.0, 2.0 * origin[1]])
    return np.r_[c[[0, 1, 2, 3]], m[[2, 1]]]        # root LE, right tip, root TE, left tip


# ===================================================================== landing gear
def _gear_body_halfwidth(x, B=GEAR_BODY):
    """Half-width (plan) of the generic fuselage at x (fuselage lengths): an elliptical nose, a
    straight middle, a tail cone that narrows to a fifth of the width."""
    x = np.asarray(x, dtype=float)
    nose = B["w"] * np.sqrt(np.clip(1.0 - (1.0 - x / B["nose"]) ** 2, 0.0, 1.0))
    s = np.clip((x - B["cone0"]) / (1.0 - B["cone0"]), 0.0, 1.0)
    cone = B["w"] * (1.0 - 0.80 * s ** 1.6)
    return np.where(x < B["nose"], nose, np.where(x > B["cone0"], cone, B["w"]))


def _gear_stations(n_nose=40, n_body=60):
    """x stations along the generic fuselage: dense at the nose (cosine spacing), so the round nose
    shows no corners."""
    B = GEAR_BODY
    t = np.linspace(0.0, 0.5 * math.pi, n_nose)
    xn = B["nose"] * (1.0 - np.cos(t))
    return np.r_[xn, np.linspace(B["nose"], 1.0, n_body)[1:]]


def gear_plan_shapes(L=1.0, origin=(0.0, 0.0)):
    """Closed outlines (plan view, nose to the left) of the generic airplane of the gear figure:
    fuselage, wing (one shape across the fuselage), horizontal tail. Example: f, w, t = gear_plan_shapes()"""
    B = GEAR_BODY
    o = np.asarray(origin, dtype=float)
    x = _gear_stations()
    w = _gear_body_halfwidth(x)
    a = np.linspace(0.5 * math.pi, -0.5 * math.pi, 9)[1:-1]          # rounded end of the tail cone
    cap = np.c_[1.0 - w[-1] * 0.6 + w[-1] * 0.6 * np.cos(a), w[-1] * np.sin(a)]
    xs = np.r_[x[:-1], 1.0 - w[-1] * 0.6]
    body = np.r_[np.c_[xs, np.r_[w[:-1], w[-1]]], cap, np.c_[xs[::-1], -np.r_[w[:-1], w[-1]][::-1]]]
    wing = np.array([(B["wing_le0"], 0.0), (B["wing_le1"], B["wing_b2"]), (B["wing_te1"], B["wing_b2"]),
                     (B["wing_te0"], 0.0), (B["wing_te1"], -B["wing_b2"]), (B["wing_le1"], -B["wing_b2"])])
    tail = np.array([(B["tail_le0"], 0.0), (B["tail_le1"], B["tail_b2"]), (B["tail_te1"], B["tail_b2"]),
                     (B["tail_te0"], 0.0), (B["tail_te1"], -B["tail_b2"]), (B["tail_le1"], -B["tail_b2"])])
    return body * L + o, wing * L + o, tail * L + o


def draw_gear_layout(ax, kind, length=1.0, origin=(0.0, 0.0), fs=FS_SMALL, cg=True):
    """Plan-view schematic of a landing-gear arrangement, seen from below, nose to the left (a key
    of GEAR_LAYOUTS: "tricycle", "tail-dragger", "multi-bogie", "bicycle", "single main",
    "quadricycle"): the generic airplane of gear_plan_shapes(), each wheel as a small black rounded
    rectangle on its structure (under the fuselage or inside the wing), and the center of gravity
    as the quartered disc (cg_symbol) at the same x as in gear_side(). The names are those of
    Raymer's arrangements. Returns dict wheels (patches), units (list of (role, center xy)), cg
    (xy). Example: d = draw_gear_layout(ax, "tricycle", origin=(0, 0))"""
    from matplotlib.patches import FancyBboxPatch
    ox, oy = origin
    L = length
    body, wing, tail = gear_plan_shapes(L, origin)
    opaque(ax.add_patch(Polygon(wing, closed=True, fc=PART_FILL, ec=INK, lw=LW_DETAIL, joinstyle="round", zorder=2)))
    opaque(ax.add_patch(Polygon(tail, closed=True, fc=PART_FILL, ec=INK, lw=LW_DETAIL, joinstyle="round", zorder=2)))
    opaque(ax.add_patch(Polygon(body, closed=True, fc=PART_FILL, ec=INK, lw=LW_DETAIL + 0.2, joinstyle="round",
                                zorder=3)))
    lay = GEAR_LAYOUTS[kind]
    wheels, units = [], []
    for (x, y, n, m, sz, role) in lay["units"]:
        wl, ww = 0.050 * L * sz, 0.022 * L * sz
        for i in range(n):
            for j in range(m):
                cx = ox + (x + (j - 0.5 * (m - 1)) * 0.060 * sz) * L
                cy = oy + (y + (i - 0.5 * (n - 1)) * 0.032 * sz) * L
                wh = FancyBboxPatch((cx - 0.5 * wl, cy - 0.5 * ww), wl, ww,
                                    boxstyle=f"round,pad=0,rounding_size={0.009 * L * sz}", fc=INK, ec=INK, lw=0.6,
                                    zorder=6)
                ax.add_patch(wh)
                wheels.append(wh)
        units.append((role, (ox + x * L, oy + y * L)))
    out = dict(wheels=wheels, units=units, cg=(ox + lay["cg"] * L, oy))
    if cg:
        cg_symbol(ax, out["cg"], size=9.0)
    return out


def cg_symbol(ax, xy, size=12.0, zorder=9):
    """The center-of-gravity symbol: a circle `size` points across, quartered, two opposite
    quarters black, at xy (data). It keeps its size whatever the scale. Name it in the caption
    or with a label. Returns the two Line2D. Example: cg_symbol(ax, (17.5, 3.2))"""
    from matplotlib.path import Path as _P
    t = np.linspace(0.0, 0.5 * math.pi, 16)
    q1 = np.r_[[(0.0, 0.0)], np.c_[np.cos(t), np.sin(t)], [(0.0, 0.0)]]
    q3 = -q1
    verts = np.r_[q1, q3]
    codes = ([_P.MOVETO] + [_P.LINETO] * (len(q1) - 2) + [_P.CLOSEPOLY]) * 2
    quarters = MarkerStyle(_P(verts, codes))
    a = ax.plot(*xy, marker="o", ms=size, mfc="white", mec=INK, mew=1.0, ls="none", zorder=zorder)[0]
    b = ax.plot(*xy, marker=quarters, ms=size - 1.0, mfc=INK, mec=INK, mew=0.0, ls="none",
                zorder=zorder + 0.1, gid="grp:cg")[0]
    a.set_gid("grp:cg")
    return a, b


def perp_symbol(ax, o, toward_reader, r_pt=5.5):
    """An axis normal to the page: a circle with a dot (pointing toward the reader) or a cross
    (pointing away). Example: perp_symbol(ax, (17.5, 3.2), True)"""
    r = pt(ax, r_pt)
    c = ax.add_patch(Circle(o, r, fc="white", ec=INK, lw=1.0, zorder=9))
    c.set_gid("grp:axis-dot")
    if toward_reader:
        ax.plot(*o, "o", ms=2.8, color=INK, zorder=9.1, gid="grp:axis-dot")
    else:
        k = r / math.sqrt(2.0)
        for s in (1, -1):
            ax.plot([o[0] - k, o[0] + k], [o[1] - s * k, o[1] + s * k], color=INK, lw=1.0, zorder=9.1,
                    gid="grp:axis-dot")
    return c


def axis_arrow(ax, o, d, L, name, label_dist=4.0, fs=FS_LABEL, lw=None, label_dir=None):
    """An "axis" arrow from o along the unit screen direction d, L data units long, its letter
    `name` beyond the tip (or toward label_dir, deg); lw overrides the kind's weight. Returns the
    tip. Example: axis_arrow(ax, (0, 0), (-1, 0), 20.0, "x")"""
    st = ARROW_KIND["axis"]
    tip = np.asarray(o, float) + L * np.asarray(d, float)
    arrow(ax, o, tip, color=st["color"], lw=lw or st["lw"], head=st["head"], zorder=8)
    ang = math.degrees(math.atan2(d[1], d[0])) if label_dir is None else label_dir
    text(ax, tip, f"${name}$", direction=ang, dist=label_dist if label_dir is None else label_dist + 4.0, fs=fs,
         zorder=11)
    return tip


def rotation_arrow(ax, c, r, t0, t1, label, label_at, dist=5.0, fs=FS_LABEL, lw=None, label_dir=None):
    """A "moment" arrow on a circle of radius r about c from t0 to t1 deg (t1 < t0: clockwise),
    its head ending exactly at t1 whatever the radius, labeled at angle label_at.
    Example: rotation_arrow(ax, (17.5, 3.2), 7.5, 150.0, 30.0, "pitch", 90.0)"""
    st = ARROW_KIND["moment"]
    w = lw or st["lw"]
    hl = HEAD[st["head"]][0]
    sgn = 1.0 if t1 > t0 else -1.0
    dth = math.degrees(pt(ax, hl) / r) * sgn
    th = np.radians(np.linspace(t0, t1 - dth, 90))
    ln = ax.plot(c[0] + r * np.cos(th), c[1] + r * np.sin(th), color=st["color"], lw=w, zorder=7,
                 solid_capstyle="butt")[0]
    a, b = math.radians(t1 - dth), math.radians(t1)
    rides_on(arrow(ax, (c[0] + r * math.cos(a), c[1] + r * math.sin(a)), (c[0] + r * math.cos(b), c[1] + r * math.sin(b)),
                   color=st["color"], lw=w, head=st["head"], zorder=7), ln)
    m = math.radians(label_at)
    text(ax, (c[0] + r * math.cos(m), c[1] + r * math.sin(m)), label, direction=label_at if label_dir is None else label_dir,
         dist=dist, fs=fs, zorder=11)
    return ln


def body_axes(ax, view, o, length, radius, rot_span, rot_label, rot_label_at, perp_at, show=None, fs=FS_LABEL,
              perp_gap=6.5, lw=None, label_dirs=None, rot_label_dir=None, rot_dist=5.0):
    """Body axes x (forward), y (out the right wing) and z (down) through o (the center of
    gravity) in one view of an airplane drawn by aircraft_side/top/front, taken from
    chapter_1.aircraft.VIEWS (right-handed by its unit check): the in-page axes as "axis" arrows
    (`length`, one number or a dict per axis, so an arrow reaches past the outline), the axis
    normal to the page as a dot (toward the reader) or a cross (away) carrying its letter at
    `perp_at` (data) with a short leader, and the positive rotation about that axis over
    rot_span (deg, t0 to t1; t1 < t0 for clockwise), named rot_label at angle rot_label_at. It
    asserts that rot_span turns the way rotation_sense(view) gives and that the drawn x, y, z
    are right-handed. show: the in-page axes to draw (default both). lw: the weight of the axes
    and the arc (default: the kinds' weights); label_dirs: {axis: deg} puts an axis letter
    beside its tip instead of beyond it; rot_label_dir and rot_dist place the rotation's name.
    Returns the screen vectors of x, y, z. Equal-aspect axes, limits set first.
    Example: body_axes(ax, "side", (17.5, 3.2), {"x": 21.5, "z": 7.0}, 7.5, (150.0, 30.0),
    "pitch (elevator)", 90.0, (14.0, 7.0))"""
    from chapter_1.aircraft import VIEWS, rotation_sense
    vw = VIEWS[view]
    drawn = {}
    for name in ("x", "y", "z"):
        v = vw[name]
        if name == vw["normal"]:
            perp_symbol(ax, o, v[2] > 0)
            callout(ax, o, f"${name}$", at=perp_at, gap=perp_gap, fs=fs, ha="center")
            drawn[name] = v
            continue
        if show is not None and name not in show:
            drawn[name] = v
            continue
        L = length[name] if isinstance(length, dict) else length
        axis_arrow(ax, o, v[:2], L, name, fs=fs, lw=lw, label_dir=(label_dirs or {}).get(name))
        drawn[name] = v
    sense = "clockwise" if rot_span[1] < rot_span[0] else "counterclockwise"
    assert sense == rotation_sense(view), f"{view}: the positive {vw['rotation']} turns {rotation_sense(view)}"
    rotation_arrow(ax, o, radius, rot_span[0], rot_span[1], rot_label, rot_label_at, fs=fs, lw=lw,
                   label_dir=rot_label_dir, dist=rot_dist)
    assert np.allclose(np.cross(drawn["x"], drawn["y"]), drawn["z"]), f"{view}: axes drawn are not right-handed"
    return drawn


# ===================================================================== landing gear in side view
GEAR_CONTACT = {"main": -0.135, "nose": -0.135, "tail": -0.135, "outrigger": None}     # body frame, fuselage lengths
GEAR_STANCE = {                       # contact heights that differ from GEAR_CONTACT (the aircraft then sits pitched)
    "tail-dragger": {"main": -0.150, "tail": -0.072},
    "single main": {"main": -0.105, "tail": -0.040},
}


def gear_side_shapes():
    """Closed outlines (side view, nose to the left, body frame: z up from the centerline, in
    fuselage lengths) of the generic airplane: fuselage, fin and the wing seen edge on.
    Example: body, fin, wing = gear_side_shapes()"""
    B = GEAR_BODY
    h = B["h"]
    x = _gear_stations()
    e = np.sqrt(np.clip(1.0 - (1.0 - x / B["nose"]) ** 2, 0.0, 1.0))
    s = np.clip((x - B["cone0"]) / (1.0 - B["cone0"]), 0.0, 1.0)
    top = np.where(x < B["nose"], h * e, h * (1.0 - 0.25 * s ** 1.5))
    bot = np.where(x < B["nose"], -h * e, -h + 1.0 * h * s ** 1.3)
    body = np.r_[np.c_[x, top], np.c_[x[::-1][1:], bot[::-1][1:]]]
    zt = lambda xx: float(np.interp(xx, x, top))           # noqa: E731
    fin = np.array([(0.785, zt(0.785) - 0.01), (0.885, 3.4 * h), (0.962, 3.4 * h), (0.990, zt(0.99) - 0.01)])
    c = B["wing_te0"] - B["wing_le0"]
    sec = naca4("0010", 40, chord=c)["outline"] + np.array([B["wing_le0"], B["wing_z"]])
    return body, fin, sec


def gear_side(ax, kind, origin, L=1.0, out=None):
    """Side view of an arrangement, nose to the left, on a ground line: the generic airplane of
    gear_side_shapes(), each wheel unit of GEAR_LAYOUTS at the same x as in draw_gear_layout() (a
    pair side by side reads as one wheel, a bogie as two wheels in tandem on a beam), and the
    center of gravity at its x. The aircraft sits on its wheels: when the front and rear units
    stand at different heights (GEAR_STANCE) it is pitched until both touch the ground (the
    tail-dragger sits nose up); wing-tip outriggers reach the ground. One per key of
    GEAR_LAYOUTS; draw it above draw_gear_layout() of the same kind. Returns the pitch angle
    (deg) and the wheel contact points; `out` (a dict) receives tf (body frame to data), the
    wheel centers by role, the center of gravity and the lowest point of the fuselage.
    Example: pitch, contacts = gear_side(ax, "tail-dragger", (0.0, 0.08))"""
    ox, oy = origin
    B = GEAR_BODY
    body, fin, wing = gear_side_shapes()
    lay = GEAR_LAYOUTS[kind]
    stance = dict(GEAR_CONTACT, **GEAR_STANCE.get(kind, {}))
    lo = body[body[:, 1] <= 0.0]
    lo = lo[np.argsort(lo[:, 0])]
    wl = wing[wing[:, 1] <= B["wing_z"] + 1e-9]
    wl = wl[np.argsort(wl[:, 0])]
    bottom = lambda xx: float(np.interp(xx, lo[:, 0], lo[:, 1]))             # noqa: E731
    wing_lo = lambda xx: float(np.interp(xx, wl[:, 0], wl[:, 1]))            # noqa: E731
    units = {}
    for (x, y, n, m, sz, role) in lay["units"]:
        units.setdefault((round(x, 4), role), (x, y, n, m, sz, role))   # a pair side by side: one wheel seen
    legs = []
    for (x, y, n, m, sz, role) in units.values():
        r = 0.026 * sz
        top = bottom(x) if abs(y) <= B["w"] else wing_lo(x)
        zc = stance[role]
        legs.append(dict(x=x, top=top, contact=zc, r=r, m=m, sz=sz, role=role))
    ground_units = [g for g in legs if g["role"] != "outrigger"]
    g0 = min(ground_units, key=lambda g: g["x"])
    g1 = max(ground_units, key=lambda g: g["x"])
    b0, b1 = np.array([g0["x"], g0["contact"]]), np.array([g1["x"], g1["contact"]])
    ang = math.atan2(b1[1] - b0[1], b1[0] - b0[0])
    R = np.array([[math.cos(-ang), -math.sin(-ang)], [math.sin(-ang), math.cos(-ang)]])

    def tf(xy):
        q = (np.asarray(xy, float) - b0) @ R.T
        return (q + np.array([b0[0], 0.0])) * L + np.array([ox, oy])
    ax.plot([ox - 0.03 * L, ox + 1.03 * L], [oy, oy], color=GRAY, lw=LW_THIN, zorder=1)
    for shape, zz, lw in ((fin, 2.0, LW_DETAIL + 0.2), (body, 3.0, LW_DETAIL + 0.2), (wing, 3.5, LW_DETAIL)):
        opaque(ax.add_patch(Polygon(tf(shape), closed=True, fc=PART_FILL, ec=INK, lw=lw, joinstyle="round", zorder=zz)))
    contacts, centers = [], {}
    for g in legs:
        r = g["r"] * L
        a = tf([(g["x"], g["top"])])[0]
        if g["role"] == "outrigger":                         # hangs from the wing to the ground
            ctrs = [np.array([a[0], oy + r])]
            beam = None
        else:
            c = tf([(g["x"], g["contact"])])[0] + np.array([0.0, r])      # the wheel touches the ground
            if g["m"] > 1:                                   # a bogie: two wheels in tandem on a beam
                d = 0.030 * g["sz"] * L
                ctrs = [c - np.array([d, 0.0]), c + np.array([d, 0.0])]
                beam = (ctrs[0], ctrs[1])
            else:
                ctrs, beam = [c], None
        foot = 0.5 * (ctrs[0] + ctrs[-1])
        ax.plot([a[0], foot[0]], [a[1], foot[1]], color=INK, lw=1.4, zorder=2.5, solid_capstyle="butt")
        if beam is not None:
            ax.plot([beam[0][0], beam[1][0]], [beam[0][1], beam[1][1]], color=INK, lw=1.6, zorder=5.5,
                    solid_capstyle="butt")
        for cc in ctrs:
            ax.add_patch(Circle(cc, r, fc=INK, ec=INK, lw=0.6, zorder=6))
            contacts.append((float(cc[0]), float(cc[1] - r)))
        centers.setdefault(g["role"], []).append(tuple(ctrs[0]))
    cgp = tf([(lay["cg"], 0.014)])[0]
    cg_symbol(ax, cgp, size=8.0)
    if out is not None:
        out.update(tf=tf, centers=centers, cg=tuple(cgp), body_low=float(tf(body)[:, 1].min()),
                   wing=tf(wing), body=tf(body))
    return math.degrees(ang), contacts


# ===================================================================== enlarged inset
def draw_enlarged(ax, parts, region, k, center):
    """Draw the parts that lie in `region` (x0, x1, y0, y1, data), enlarged k times about the
    region's center and moved to `center`, cut at the region's edges (an enlarged inset of a
    detail, joined to the main view by two thin lines the page draws). Fills and outlines are
    drawn apart so no outline runs along the cut; tanks keep their propellant tint and hatch.
    Returns dict name -> fill patch, the function mapping a point of the main view to the
    inset, and the inset rectangle. Example: fills, M, R = draw_enlarged(ax, parts, (-3, 3, 40, 52), 2.7, (30, -20))"""
    from chapter_1.launchers import PROPELLANT_STYLE, HATCH_INK
    x0, x1, y0, y1 = region
    c0 = np.array([0.5 * (x0 + x1), 0.5 * (y0 + y1)])
    c1 = np.asarray(center, float)
    M = lambda q: (np.asarray(q, float) - c0) * k + c1          # noqa: E731
    R = (M((x0, y0))[0], M((x1, y1))[0], M((x0, y0))[1], M((x1, y1))[1])
    fills = {}
    lw_of = {"stage": LW_OUTLINE, "fairing": LW_OUTLINE, "engine": LW_OUTLINE, "body": LW_OUTLINE, "strut": LW_DETAIL,
             "gear": LW_OUTLINE, "detail": LW_DETAIL, "tank": LW_DETAIL}
    for name, p in sorted(parts.items(), key=lambda kv: kv[1].z):
        if p.hidden or name in ("common_bulkhead",):
            continue
        xy = M(p.xy)
        if p.kind == "line":
            for pc in clip_line(xy, R):
                ln = ax.plot(pc[:, 0], pc[:, 1], color=INK, lw=LW_DETAIL, zorder=20 + p.z, solid_capstyle="butt")[0]
                if p.on in fills:
                    on_part(ln, fills[p.on])
            continue
        poly = clip_poly(xy, R)
        if len(poly) < 3 or polygon_area(poly) < 1e-6:
            continue
        if p.kind == "tank":
            st = PROPELLANT_STYLE[p.contents]
            fp = Polygon(poly, closed=True, fc=st["fill"], ec=HATCH_INK, lw=0.0, zorder=20 + p.z)
            if st["hatch"]:
                fp.set_hatch(st["hatch"])
        else:
            fp = Polygon(poly, closed=True, fc=PART_FILL, ec="none", lw=0.0, zorder=20 + p.z)
        ax.add_patch(fp)
        opaque(fp)
        fills[name] = fp
        host = fills.get(p.on) if p.on else None
        for pc in clip_line(np.r_[xy, xy[:1]], R):
            ln = ax.plot(pc[:, 0], pc[:, 1], color=INK, lw=lw_of.get(p.kind, LW_DETAIL), zorder=20 + p.z + 0.01,
                         solid_capstyle="round", solid_joinstyle="round")[0]
            on_part(ln, fp)
            if host is not None:
                ln._on_part = fp
        if host is not None:
            on_part(fp, host)
    return fills, M, R


# ===================================================================== mission profile
def draw_mission_profile(ax, segs, ndir, drop=None, ground=(-0.3, 0.3), name_fs=FS_SMALL, heads=True, numbers=None,
                         thin=(), axes_names=False, name_dist=None, distance_below=27.0):
    """A mission profile (schematic, not to scale) on axes whose limits are set, drawn by the one
    rule of the chapter: takeoff and landing are short level segments on the ground line, climbs
    and descents are slanted, cruise and loiter are level. The path runs as straight segments
    from the start of the takeoff; a dot with its bold number marks the end of every segment (0 at
    the start of the takeoff); each segment is named beside it (below the ground line for a
    segment on the ground); direction-of-flight heads sit on the longer airborne segments.
    segs: list of (name, horizontal length, altitude at its end, fraction along the segment where
    its name sits[, direction of the name from the segment in degrees, when the default side is
    crowded]). ndir: the direction (deg) of each number from its point, one per point.
    numbers: the label of each point (default 0, 1, 2, ...; None leaves a point unmarked).
    thin: indices of segments that carry no weight fraction of their own in the sizing method
    (a descent counted in the cruise): drawn as a thinner line, and the point at their top is
    left unnumbered by the caller. drop: (point index, what leaves) draws a weight drop as a
    short downward arrow that starts on the path at that point, with "weight drop: <what>" beside
    it. axes_names=True adds a light "altitude" arrow at the left, a light "distance" arrow under
    the start (distance_below points under the ground line), and the word "ground" on the ground
    line (once per figure). ground: how far the
    ground line runs past the first and last points. Returns the x and y of the points and the
    path line (the thick part).
    Example: xs, ys, ln = draw_mission_profile(ax, [("takeoff", 0.7, 0.0, 0.5), ("climb", 1.4, 1.0, 0.4)], [90, 120, -45])"""
    L = sum(sg[1] for sg in segs)
    gl = ax.plot([ground[0], L + ground[1]], [0.0, 0.0], color=GRAY, lw=LW_THIN, zorder=1)[0]
    xs, ys = [0.0], [0.0]
    for (_, dx, yend, *_r) in segs:
        xs.append(xs[-1] + dx)
        ys.append(yend)
    xs, ys = np.array(xs), np.array(ys)
    thin = set(thin)
    # the thick path, in runs of segments that are not thin; the thin segments on their own
    runs, cur = [], [0]
    for k in range(len(segs)):
        if k in thin:
            if len(cur) > 1:
                runs.append(cur)
            cur = [k + 1]
            ax.plot(xs[k:k + 2], ys[k:k + 2], color=INK, lw=1.0, zorder=4, solid_capstyle="butt")
        else:
            cur.append(k + 1)
    if len(cur) > 1:
        runs.append(cur)
    lines = [ax.plot(xs[r], ys[r], color=INK, lw=LW_MAIN, zorder=4, solid_joinstyle="round", solid_capstyle="round")[0]
             for r in runs]
    ln = lines[0]
    fr = []
    for k, (name, dx, yend, f, *opt) in enumerate(segs):
        p0, p1 = np.array([xs[k], ys[k]]), np.array([xs[k + 1], ys[k + 1]])
        at = p0 + f * (p1 - p0)
        if opt:
            d = float(opt[0])
        elif ys[k] == 0.0 and yend == 0.0:
            d = -90.0                                     # on the ground: named below the ground line
        else:
            d = _screen_angle(ax, p1 - p0) + 90.0         # beside the segment, on the outer side
        if name:
            dist = name_dist if name_dist is not None else (9.0 if opt else (6.0 if d != -90.0 else 5.0))
            text(ax, at, name, direction=d, dist=dist, fs=name_fs)
        if heads and name and k not in thin and dx >= 0.8 and ys[k] + yend > 0.0:
            fr.append((k, 0.78 if ys[k] != yend else 0.68))
    for k, f in fr:
        r = next(r for r in runs if k + 1 in r and k in r)
        xr, yr = xs[r], ys[r]
        s_len = np.r_[0.0, np.cumsum(np.hypot(np.diff(xr), np.diff(yr)))]
        xa = xs[k] + f * (xs[k + 1] - xs[k])
        motion_heads(ax, xr, yr, [float(np.interp(xa, xr, s_len) / s_len[-1])], line=lines[runs.index(r)])
    labels = [str(k) for k in range(len(xs))] if numbers is None else numbers
    for k, (x, y) in enumerate(zip(xs, ys)):
        if labels[k] is None:
            continue
        ax.plot(x, y, "o", ms=4.5, color=INK, zorder=6)
        text(ax, (x, y), labels[k], direction=ndir[k], dist=6.5, fs=FS_SMALL, fontweight="bold")
    def dy(n):                                            # n points as a height in data units
        ax.figure.canvas.draw_idle()
        q = ax.transData.inverted().transform([(0.0, 0.0), (0.0, n * ax.figure.dpi / 72.0)])
        return float(q[1, 1] - q[0, 1])

    def dx_(n):                                           # n points as a width in data units
        q = ax.transData.inverted().transform([(0.0, 0.0), (n * ax.figure.dpi / 72.0, 0.0)])
        return float(q[1, 0] - q[0, 0])
    if drop:
        kd, what, *side = drop
        side = side[0] if side else 0.0
        tip = (xs[kd], ys[kd] - dy(26.0))
        arrow(ax, (xs[kd], ys[kd]), tip, color=INK, lw=1.4, head="normal", zorder=5.5, gid="grp:weight-drop")
        text(ax, tip, f"weight drop:\n{what}", direction=side, dist=6.0 if side != -90.0 else 3.0, fs=FS_SMALL)
    if axes_names:
        y1 = ax.get_ylim()[1]
        xa_ = ground[0]
        h0 = dy(8.0)
        arrow(ax, (xa_, h0), (xa_, h0 + 0.80 * (y1 - h0)), color=GRAY, lw=LW_THIN, head="small", zorder=2)
        text(ax, (xa_, h0 + 0.36 * (y1 - h0)), "altitude", direction=180.0, dist=3.0, fs=FS_SMALL, rotation=90.0,
             ha="right", va="center")
        yd = -dy(distance_below)
        arrow(ax, (xa_, yd), (xa_ + dx_(70.0), yd), color=GRAY, lw=LW_THIN, head="small", zorder=2)
        text(ax, (xa_ + dx_(70.0), yd), "distance", direction=0.0, dist=3.0, fs=FS_SMALL)
        text(ax, (L + ground[1], 0.0), "ground", direction=90.0, dist=3.0, fs=FS_SMALL, ha="right")
        assert ground[1] > 0.6, "room for the word ground beyond the last point"
    assert ys[0] == 0.0 and ys[-1] == 0.0 and np.all(np.diff(xs) > 0) and len(ndir) == len(xs), \
        "a mission starts and ends on the ground, flies forward, and numbers every segment end"
    for k, (name, dx, yend, *_r) in enumerate(segs):            # the rule of the chapter
        if name and name.startswith(("takeoff", "landing", "warm-up")):
            assert ys[k] == 0.0 and yend == 0.0, f"{name}: takeoff and landing lie on the ground line"
    return xs, ys, ln


# ===================================================================== a wall in section
def hatched_wall(ax, x, y_in, y_out, zorder=3):
    """A duct or tube wall cut in section: a hatched band between the inner surface y_in(x) and
    the outer surface y_out(x), opaque. Example: hatched_wall(ax, x, r, r + 0.07)"""
    band = np.r_[np.c_[x, y_in], np.c_[x[::-1], y_out[::-1]]]
    pa = ax.add_patch(Polygon(band, closed=True, fc="#FFFFFF", ec=INK, lw=LW_DETAIL, zorder=zorder))
    pa.set_hatch("////")
    opaque(pa)
    return pa


# ===================================================================== small dimensions
def dimension_outside(ax, p0, p1, label=None, label_dir=None, dist=4.0, lead=12.0, color=INK, lw=LW_THIN, fs=FS_LABEL,
                      zorder=4):
    """A dimension too small for arrows inside it (a camber or a thickness of a few points):
    two arrows `lead` points long point in from outside, their tips on p0 and p1 (data), with
    a thin line joining the tips. The label sits beyond the p1 arrow (or toward label_dir,
    deg). Equal-aspect axes. Returns the group name the parts share (the gate lets them touch).
    Example: dimension_outside(ax, (0.4, 0.0), (0.4, 0.02), "2% of c")"""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    u = (p1 - p0) / np.hypot(*(p1 - p0))
    L = pt(ax, lead)
    ax._dimout_count = getattr(ax, "_dimout_count", 0) + 1          # a name that is the same on every run
    grp = f"grp:dimout{ax._dimout_count}-{p0[0]:.6g}-{p0[1]:.6g}"
    arrow(ax, p0 - L * u, p0, color=color, lw=lw, head="small", zorder=zorder, gid=grp)
    arrow(ax, p1 + L * u, p1, color=color, lw=lw, head="small", zorder=zorder, gid=grp)
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, zorder=zorder, gid=grp)
    if label:
        ang = math.degrees(math.atan2(u[1], u[0])) if label_dir is None else label_dir
        text(ax, p1 + L * u if label_dir is None else 0.5 * (p0 + p1), label, direction=ang, dist=dist, fs=fs,
             color=color, zorder=zorder + 3)
    return grp



# ===================================================================== manometer
def draw_manometer(ax, x_left, x_right, top, bottom, level_left, level_right, tube, fluid=FLUID_FILL, lw=LW_DETAIL,
                   zorder=4):
    """A U-tube manometer in section: legs at x_left and x_right (centerlines, data) from `top`
    down to the bend at `bottom`, inner half-width `tube`, filled with fluid from the bend up to
    level_left and level_right. The leg under the higher pressure has the lower level. Returns
    the fluid patch. Equal-aspect axes. Example: draw_manometer(ax, 0.2, 0.8, -0.1, -0.35, -0.25, -0.23, 0.008)"""
    t = tube
    fl = np.array([(x_left - t, level_left), (x_left - t, bottom - t), (x_right + t, bottom - t), (x_right + t, level_right),
                   (x_right - t, level_right), (x_right - t, bottom + t), (x_left + t, bottom + t), (x_left + t, level_left)])
    fp = ax.add_patch(Polygon(fl, closed=True, fc=fluid, ec="none", zorder=zorder - 0.5))
    outer = [(x_left - t, top), (x_left - t, bottom - t), (x_right + t, bottom - t), (x_right + t, top)]
    inner = [(x_left + t, top), (x_left + t, bottom + t), (x_right - t, bottom + t), (x_right - t, top)]
    for pts in (outer, inner):
        p = np.array(pts)
        ax.plot(p[:, 0], p[:, 1], color=INK, lw=lw, zorder=zorder, solid_joinstyle="miter")
    for x, lv in ((x_left, level_left), (x_right, level_right)):         # the free surfaces
        ax.plot([x - t, x + t], [lv, lv], color=INK, lw=lw, zorder=zorder)
    return fp
