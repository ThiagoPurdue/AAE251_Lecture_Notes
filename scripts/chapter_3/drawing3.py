"""Drawing helpers of Chapter 3 that Chapter 1 lacks: numbered discs for data plots, vectors and
checked angle marks, the downwash construction, a wing seen from behind with its tip vortices,
boundary-layer profiles over a flat plate, three linked panels for building a
drag polar, an airfoil in a free stream with its forces and moment, and the wind-tunnel outlines
of tunnel.py drawn as line art. Every helper asserts what it draws (angles, lengths, tangency).

Line art follows Chapter 1 (chapter_1/README.md, "Styles"): velocity arrows blue, force arrows
black and heavy, flow direction as open block arrows, construction lines thin, angles thin arcs.
"""
import math

import numpy as np

from chapter_1.style import *  # noqa: F401,F403
from chapter_1.style import _screen_angle  # noqa: F401
from chapter_1.diagrams import DISC_FILL, DISC_LW
from matplotlib.patches import Polygon, Ellipse

from chapter_3 import aero as _aero


# ===================================================================== small marks
def data_per_pt(ax):
    """Data units per point along x and y of axes whose limits and size are set (any aspect).
    Example: kx, ky = data_per_pt(ax)"""
    fig = ax.figure
    bb = ax.get_position()
    w_pt = bb.width * fig.get_figwidth() * 72.0
    h_pt = bb.height * fig.get_figheight() * 72.0
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    return (x1 - x0) / w_pt, (y1 - y0) / h_pt


def disc(ax, xy, n, r=8.0, above=False, below=False, fs=FS_SMALL, zorder=12):
    """The chapter's numbered disc (white, thin black ring, regular digit) on any axes, including a
    data plot whose units differ in x and y: an ellipse in data units that shows as a circle of
    radius r points. above/below=True puts it r + 2 points above or below xy (the start of a
    reading on an axis). Opaque. Returns the patch. Example: disc(ax, (4.0, -1.6), 1, above=True)"""
    kx, ky = data_per_pt(ax)
    x, y = float(xy[0]), float(xy[1])
    if above:
        y += (r + 2.0) * ky
    if below:
        y -= (r + 2.0) * ky
    e = ax.add_patch(opaque(Ellipse((x, y), 2 * r * kx, 2 * r * ky, fc=DISC_FILL, ec=INK, lw=DISC_LW,
                                    zorder=zorder)))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=fs, color=INK, zorder=zorder + 1)
    return e


def unit(deg):
    """Unit vector at angle deg (counterclockwise from +x). Example: unit(90.0) -> (0, 1)"""
    a = math.radians(deg)
    return np.array([math.cos(a), math.sin(a)])


def vector(ax, origin, angle_deg, length, kind="velocity", label=None, label_dir=None, dist=4.0, label_at="tip",
           fs=FS_LABEL, zorder=7):
    """A vector drawn to scale from `origin` at angle_deg (equal-aspect axes), of `length` data
    units, in one of Chapter 1's arrow kinds ("velocity", "force", ...). Returns the tip point.
    Asserts the drawn direction. Example: tip = vector(ax, (0, 0), -3.0, 2.0, "velocity", "$V$")"""
    o = np.asarray(origin, float)
    tip = o + length * unit(angle_deg)
    kind_arrow(ax, o, tip, kind, label, label_dir=label_dir, dist=dist, fs=fs, zorder=zorder, label_at=label_at)
    d = tip - o
    assert abs(math.degrees(math.atan2(d[1], d[0])) - angle_deg + 360.0) % 360.0 < 1e-9 or \
        abs((math.degrees(math.atan2(d[1], d[0])) - angle_deg + 180.0) % 360.0 - 180.0) < 1e-9
    return tip


def angle_mark(ax, vertex, a_from, a_to, radius, label=None, stated=None, tol=1e-6, dist=4.0, fs=FS_LABEL,
               color=INK, zorder=5, label_dir=None, label_r=None, label_angle=None):
    """An angle drawn between two lines that meet at `vertex`, the lines at screen angles a_from and
    a_to (deg; equal-aspect axes): a thin arc of `radius` data units from a_from to a_to, its label
    on the bisector just outside the arc (or toward label_dir). With `stated` (deg), asserts that the
    angle drawn equals the angle the text states (times any drawing factor the caller applied).
    label_r (data units) centers the label on the bisector at that radius instead (for a label that
    must sit inside a narrow wedge, beyond the arc); label_angle (deg) puts it on that ray instead
    of the bisector (just outside one of the two lines). Returns the arc's Line2D.
    Example: angle_mark(ax, (0, 0), -8.0, 0.0, 1.2, r"$\\alpha$", stated=8.0)"""
    sweep = a_to - a_from
    if stated is not None:
        assert abs(abs(sweep) - stated) <= tol, f"angle drawn {abs(sweep):.6f} deg, stated {stated:.6f} deg"
    th = np.radians(np.linspace(a_from, a_to, max(12, int(abs(sweep) * 3))))
    cx, cy = vertex
    ln = ax.plot(cx + radius * np.cos(th), cy + radius * np.sin(th), color=color, lw=LW_THIN, zorder=zorder,
                 solid_capstyle="butt")[0]
    if label:
        b = math.radians(0.5 * (a_from + a_to) if label_angle is None else label_angle)
        if label_r is not None:
            text(ax, (cx + label_r * math.cos(b), cy + label_r * math.sin(b)), label, fs=fs, color=color,
                 zorder=zorder + 4)
        else:
            p = (cx + radius * math.cos(b), cy + radius * math.sin(b))
            text(ax, p, label, direction=math.degrees(b) if label_dir is None else label_dir, dist=dist, fs=fs,
                 color=color, zorder=zorder + 4)
    return ln


def ray(ax, vertex, angle_deg, length, role="reference", **kw):
    """A straight construction line from vertex at angle_deg (deg), `length` data units. Returns the Line2D."""
    v = np.asarray(vertex, float)
    e = v + length * unit(angle_deg)
    return ax.plot([v[0], e[0]], [v[1], e[1]], zorder=kw.pop("zorder", 2), **line_kw(role, **kw))[0]


# ===================================================================== an airfoil in a free stream
def rotate(xy, deg, about=(0.0, 0.0)):
    """Points turned counterclockwise by deg about `about`."""
    a = math.radians(deg)
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return (np.asarray(xy, float) - about) @ R.T + about


def section_xy(airfoil="64-618", chord=1.0, alpha=0.0, c4=(0.0, 0.0)):
    """Closed outline of a section (a NACA Report 824 section of airfoil_data, or a NACA 4-digit
    code such as "2415" through chapter_1's naca4) with chord `chord`, pitched nose up by alpha
    (deg; the flow comes from the left) about its quarter-chord point, which is placed at c4.
    Returns (outline, le, te) as points. Example: xy, le, te = section_xy("64-618", 1.0, 6.0)"""
    from chapter_3.airfoil_data import section_outline, AIRFOILS
    if airfoil in AIRFOILS:
        xy = section_outline(airfoil, chord)
    else:
        from chapter_1.geometry import naca4
        xy = naca4(airfoil, chord=chord)["outline"]
    q = np.array([0.25 * chord, 0.0])
    xy = rotate(xy - q, -alpha) + c4
    le = rotate(np.array([[-0.25 * chord, 0.0]]), -alpha)[0] + c4
    te = rotate(np.array([[0.75 * chord, 0.0]]), -alpha)[0] + c4
    return xy, le, te


def airfoil_in_stream(ax, alpha, airfoil="64-618", chord=1.0, c4=(0.0, 0.0), V_len=0.45, lift=0.7, drag=0.18,
                      moment=None, fill=PART_FILL, labels=True, arc_r=None, zorder=3, ext=0.90, ref=0.85,
                      alpha_label_r=None):
    """An airfoil at angle of attack alpha (deg) in a free stream from the left (equal-aspect axes):
    the section (opaque, outline weight), its chord line extended ahead of the leading edge
    (dashed), a horizontal reference line through the quarter chord along the free stream, the
    free-stream velocity arrow ahead of the section, the alpha arc between the free-stream line
    and the chord line (vertex at the quarter chord, on the upstream side), and at the quarter
    chord the lift (perpendicular to the free stream, up), the drag (parallel to it, downstream)
    and, if `moment` is "nose up" or "nose down", the pitching-moment arrow (nose up is clockwise
    in this view: the leading edge, on the left, rises). Lengths in data units; lift=0 or drag=0
    leaves an arrow out. ext and ref: lengths (chords) of the chord line ahead of the leading edge
    and of the free-stream line; alpha_label_r (chords): put the alpha label inside the wedge on
    the bisector at that radius (default: above the chord line). Returns a dict of points and
    artists. Asserts that lift is perpendicular and drag parallel to the free stream and that the
    alpha drawn is the alpha given.
    Example: g = airfoil_in_stream(ax, 6.0, moment="nose down")"""
    c4 = np.asarray(c4, float)
    xy, le, te = section_xy(airfoil, chord, alpha, c4)
    out = dict(le=le, te=te, c4=c4, outline=xy)
    out["section"] = opaque(ax.add_patch(Polygon(xy, closed=True, fc=fill, ec=INK, lw=LW_OUTLINE, zorder=zorder)))
    ext_p = le + (le - te) / np.hypot(*(le - te)) * ext * chord
    out["chord_line"] = ax.plot([ext_p[0], te[0]], [ext_p[1], te[1]], **line_kw("boundary"), zorder=zorder + 0.5)[0]
    href = le + np.array([-ref * chord, 0.0])
    out["reference"] = ax.plot([href[0], le[0]], [href[1], le[1]], **line_kw("reference"), zorder=1.5)[0]
    r = arc_r or 0.55 * chord                           # alpha at the leading edge: free stream line to chord line
    if alpha_label_r is None:
        out["alpha_arc"] = angle_mark(ax, le, 180.0 - alpha, 180.0, r, r"$\alpha$" if labels else None,
                                      stated=alpha, label_dir=90.0, dist=9.0)
    else:
        out["alpha_arc"] = angle_mark(ax, le, 180.0 - alpha, 180.0, r, r"$\alpha$" if labels else None,
                                      stated=alpha, label_r=alpha_label_r * chord)
    va = href + np.array([-0.12 * chord - V_len, 0.0])
    kind_arrow(ax, va, va + np.array([V_len, 0.0]), "velocity", None)
    if labels:
        text(ax, va + np.array([0.40 * V_len, 0.0]), r"free stream, $V_\infty$", direction=90, dist=9, color=BLUE)
    if lift:
        Lt = c4 + np.array([0.0, lift])
        kind_arrow(ax, c4, Lt, "force", "lift, $L$" if labels else None, label_dir=90)
        assert abs(Lt[0] - c4[0]) < 1e-12, "lift perpendicular to the free stream"
        out["lift_tip"] = Lt
    if drag:
        # from the quarter chord, long enough that its head clears the trailing edge
        Dt = c4 + np.array([max(drag, 0.75 * chord * math.cos(math.radians(alpha)) + 0.22 * chord), 0.0])
        kind_arrow(ax, c4, Dt, "force", None)
        assert Dt[0] - pt(ax, 13.0) > te[0], "the drag arrowhead clears the trailing edge"
        if labels:
            text(ax, Dt, "drag, $D$", direction=0, dist=6)
        assert abs(Dt[1] - c4[1]) < 1e-12, "drag parallel to the free stream"
        out["drag_tip"] = Dt
    if moment:
        rr = 0.27 * chord                 # above the section: the arc clears the upper surface
        if moment == "nose up":
            moment_arrow(ax, c4, rr, 155.0, 35.0, "moment, $M$" if labels else None, label_at=130.0)
        else:
            moment_arrow(ax, c4, rr, 35.0, 155.0, "moment, $M$" if labels else None, label_at=130.0)
    return out


# ===================================================================== the downwash construction
def downwash_construction(ax, alpha, alpha_i, k=2.0, airfoil="64-618", chord=2.0, c4=(0.0, 0.0), V_len=2.2,
                          F_len=2.2, lead=0.2, labels=True, angle_labels=True, fs=FS_LABEL, alpha_at="upstream"):
    """The finite-wing construction of the textbooks (Anderson's "downwash and induced drag"
    figure) on equal-aspect axes, flow from the left. The section sits at angle of attack alpha
    with its chord line extended forward to a vertex P, `lead` chords ahead of the leading edge.
    The velocity triangle ends at P, so it feeds the section: the free stream V_inf (horizontal)
    and the local relative wind both arrive at P; the downwash w closes the triangle at its
    upstream end (local relative wind = V_inf + w). At P: alpha between V_inf and the chord line,
    alpha_eff between the local relative wind and the chord line, alpha_i between V_inf and the
    local relative wind, three arcs at three radii. At the quarter-chord station (on the upper
    surface above it, so the arrows clear the outline) the local lift, perpendicular to the local
    relative wind, and its components: lift L perpendicular to V_inf and induced drag D_i parallel
    to it, with the rectangle completed by dashed lines. Every arrow is labeled directly.
    Angles are drawn k times their size (say so in the caption): w = V tan(k alpha_i) and
    D_i = L tan(k alpha_i) in the drawing. Asserts alpha = alpha_eff + alpha_i as drawn, the local
    lift perpendicular to the local wind, the triangle closing at P, and the scales.
    alpha_at="downstream" marks alpha on the far side of P instead, between the chord line and a
    thin free-stream reference line from P toward the section (give `lead` room for it, about
    0.9), so the alpha_i and alpha_eff wedges upstream carry one label each. Returns a dict
    of points (P, T1, T2, c4, F (force origin), L_local, L, Di, le, te) and the drawn angles.
    Example: g = downwash_construction(ax, 8.0, 2.74, k=3.5)"""
    A, Ai = k * alpha, k * alpha_i
    Ae = A - Ai
    c4 = np.asarray(c4, float)
    xy, le, te = section_xy(airfoil, chord, A, c4)
    opaque(ax.add_patch(Polygon(xy, closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=3)))
    u_ch = (le - te) / np.hypot(*(le - te))                 # along the chord, toward upstream
    P = le + u_ch * lead * chord                            # the vertex, on the chord line extended
    gp = pt(ax, 14.0)                                        # the chord line, broken round the vertex so the
    ext_ch = 0.95
    for a_, b_ in ((P + u_ch * ext_ch * V_len, P + u_ch * gp), (P - u_ch * gp, te)):   # arrowheads there stay clear
        ax.plot([a_[0], b_[0]], [a_[1], b_[1]], **line_kw("boundary"), zorder=1.6)
    # the velocity triangle, arrows ending at P: T1 -> P free stream, T2 -> T1 downwash, T2 -> P local wind
    T1 = P - np.array([V_len, 0.0])
    w = V_len * math.tan(math.radians(Ai))
    T2 = T1 + np.array([0.0, w])
    # both arrive at P with their heads there, so the triangle visibly closes; the two heads meet
    # at P and are one drawing group with the triangle (the layout gate lets them touch)
    grp = "grp:velocity-triangle"
    kind_arrow(ax, T1, P, "velocity", None).set_gid(grp)
    kind_arrow(ax, T2, T1, "velocity", None, lw=1.4).set_gid(grp)
    kind_arrow(ax, T2, P, "velocity", None).set_gid(grp)
    stop = 0.0
    close_to(float(np.hypot(*(P - T1))), V_len, 1e-12, "V_inf to scale")
    close_to(float(np.hypot(*(P - T2))), V_len / math.cos(math.radians(Ai)), 1e-12, "local wind = V_inf + w")
    close_to(math.degrees(math.atan2(-(P - T2)[1], (P - T2)[0])), Ai, 1e-9, "local wind alpha_i below V_inf")
    # the three angles at P, on the upstream side (V_inf at 180 deg, local wind at 180 - Ai, chord at
    # 180 - A): alpha_i innermost, alpha_eff next, alpha outermost spanning both, each label in its
    # own wedge just beyond its arc (alpha's in the alpha_eff wedge, beyond every arc)
    if alpha_at == "upstream":
        # (a compact layout for a small drawing: alpha's label sits just above the chord line)
        ri, re_, ra = 0.58 * V_len, 0.72 * V_len, max(0.34 * V_len, pt(ax, 52.0))
        angle_mark(ax, P, 180.0 - A, 180.0, ra, r"$\alpha$" if angle_labels else None, stated=A,
                   label_r=ra + pt(ax, 6.0), label_angle=180.0 - A - 14.0)
        li, le_ = 0.90 * V_len, 0.84 * V_len
    else:
        ri, re_ = 0.50 * V_len, 0.72 * V_len
        d_ = 0.85 * lead * chord                       # the free-stream direction continued past P
        ax.plot([P[0], P[0] + d_], [P[1], P[1]], **line_kw("reference"), zorder=1.6)
        rd = 0.55 * lead * chord
        assert rd > gp, "the alpha arc lies beyond the break of the chord line at P"
        angle_mark(ax, P, -A, 0.0, rd, r"$\alpha$" if angle_labels else None, stated=A, label_r=rd + pt(ax, 10.0))
        li, le_ = ri + pt(ax, 14.0), re_ + pt(ax, 19.0)
    angle_mark(ax, P, 180.0 - Ai, 180.0, ri, r"$\alpha_i$" if angle_labels else None, stated=Ai, label_r=li)
    angle_mark(ax, P, 180.0 - A, 180.0 - Ai, re_, r"$\alpha_\mathrm{eff}$" if angle_labels else None,
               stated=Ae, label_r=le_)
    close_to(Ae + Ai, A, 1e-12, "alpha = alpha_eff + alpha_i")
    # forces at the quarter-chord station, from 6 points above the upper surface over the
    # quarter-chord point (the caption says so), so every arrow clears the outline
    up = xy[np.abs(xy[:, 0] - c4[0]) < 0.02 * chord]
    F = np.array([c4[0], up[:, 1].max() + pt(ax, 6.0)])
    Lloc = F + F_len * unit(90.0 - Ai)
    Lv = F + np.array([0.0, F_len * math.cos(math.radians(Ai))])
    Dv = F + np.array([F_len * math.sin(math.radians(Ai)), 0.0])
    wind = (P - T2) / np.hypot(*(P - T2))
    close_to(float(np.dot(Lloc - F, wind)), 0.0, 1e-12, "local lift perpendicular to the local wind")
    close_to((Dv - F)[0] / (Lv - F)[1], math.tan(math.radians(Ai)), 1e-12, "D_i = L tan(alpha_i)")
    # the rectangle that splits the local lift: dashed sides from the tips of L and D_i to the tip
    # of the local lift, 6 points clear of each end (clear of the arrowheads)
    dash = dict(color=GRAY, lw=LW_THIN, ls=(0, (3.0, 2.0)), zorder=2)
    gap = pt(ax, 6.0)
    for a_, b_, g_end in ((Lv, Lloc, gap), (Dv, Lloc, pt(ax, 22.0))):   # the vertical side stops below the
        u_ = (b_ - a_) / np.hypot(*(b_ - a_))                          # local lift's head, which leans over it
        e0, e1 = a_ + u_ * gap, b_ - u_ * g_end
        assert np.dot(e1 - e0, u_) > 0, "both sides of the force rectangle are drawn"
        ax.plot([e0[0], e1[0]], [e0[1], e1[1]], **dash)
    kind_arrow(ax, F, Lloc, "force", None)
    kind_arrow(ax, F, Lv, "force", None)
    kind_arrow(ax, F, Dv, "force", None, head="small")        # short arrow: a small head, not all head
    out = dict(P=P, T1=T1, T2=T2, le=le, te=te, c4=c4, F=F, L_local=Lloc, L=Lv, Di=Dv, A=A, Ai=Ai, Ae=Ae)
    if labels:
        text(ax, 0.5 * (T1 + P - np.array([stop, 0.0])), r"free stream, $V_\infty$", direction=-90, dist=7, fs=fs,
             color=BLUE)
        text(ax, 0.5 * (T1 + T2), "downwash, $w$", direction=180, dist=10, fs=fs, color=BLUE)
        text(ax, T2, "local relative wind", direction=135, dist=6, fs=fs, color=BLUE)
        text(ax, Lloc, "local lift", direction=20, dist=6, fs=fs)
        text(ax, Lv, "lift, $L$", direction=160, dist=6, fs=fs)
        text(ax, Dv, r"induced drag, $D_i$", direction=-10, dist=8, fs=fs)
    return out


# ===================================================================== wing seen from behind
def wing_rear_view(ax, P=None, scale=1.0, origin=(0.0, 0.0), z=3.0, fill=SURFACE_FILL, htail=False):
    """A jet transport seen from behind (front elevation mirrored: the left wing on the left of the
    page), from chapter_1.aircraft.aircraft_front (Boeing 737-800: span 34.32 m without winglets,
    dihedral 6 deg, fuselage 3.76 m wide): fuselage section, wings, vertical tail, engines and
    pylons, filled light gray with the outline kept, so they read as solid; with htail=True the
    horizontal tail too (on the centerline, it hides no tip); winglets and gear left out so the
    plain wing tip shows. Units m times `scale`. Returns
    dict(parts=patches, tip_L, tip_R (the tip points), span, vortex_L, vortex_R (where the tip
    vortex cores sit: just inboard of and above the tips, as observed; a spiral of outer radius up
    to 1.6 m about them stays clear of the wing)).
    Example: g = wing_rear_view(ax)"""
    from chapter_1.aircraft import aircraft_front, B738
    P = P or B738
    parts = aircraft_front(P, detail=False, ground=False)
    o = np.asarray(origin, float)
    keep = [n for n in parts if n in ("fuselage", "wing_L", "wing_R", "vtail") or n.startswith(("nacelle", "pylon"))
            or (htail and n.startswith("htail"))]
    out, tips = {}, {}
    for n in sorted(keep, key=lambda n: parts[n].z):
        xy = parts[n].xy * np.array([-1.0, 1.0]) * scale + o          # seen from behind: mirror
        out[n] = opaque(ax.add_patch(Polygon(xy, closed=True, fc=fill, ec=INK, lw=LW_OUTLINE, joinstyle="round",
                                             zorder=z + 0.01 * parts[n].z)))
        if n.startswith("wing"):
            i = np.argmax(np.abs(xy[:, 0] - o[0]))
            side = xy[np.abs(np.abs(xy[:, 0] - o[0]) - abs(xy[i, 0] - o[0])) < 1e-6]
            tips[n[-1]] = np.array([xy[i, 0], side[:, 1].mean()])
    assert tips["R"][0] > o[0] and tips["L"][0] < o[0], "rear view: the right wing on the right"
    inb = 0.035 * (tips["R"][0] - tips["L"][0])
    vR = tips["R"] + np.array([-inb, 2.0 * scale])
    vL = tips["L"] + np.array([inb, 2.0 * scale])
    return dict(parts=out, tip_L=tips["L"], tip_R=tips["R"], span=float(tips["R"][0] - tips["L"][0]),
                vortex_L=vL, vortex_R=vR)


def spiral_vortex(ax, center, r0, r1, turns=1.3, sense="ccw", start_deg=-90.0, lw=1.4, color=INK, zorder=6,
                  inward=False):
    """A tip vortex seen along its axis: an Archimedean spiral from radius r0 to r1 (data units,
    equal-aspect axes) with an arrowhead at the outer end, turning counterclockwise (sense="ccw")
    or clockwise. inward=True runs it the other way, from r1 at start_deg in to r0, arrowhead at
    the inner end: the air that comes round a wing tip and rolls up into the core. Seen from behind,
    the right-wing tip vortex turns counterclockwise and the left one clockwise (air rolls up from
    the higher pressure below the wing round the tip to the lower pressure above). Returns the
    Line2D. Example: spiral_vortex(ax, tip, 0.2, 1.6, sense="ccw")"""
    s = 1.0 if sense == "ccw" else -1.0
    t = np.linspace(0.0, 1.0, 240)
    th = np.radians(start_deg) + s * 2 * math.pi * turns * t
    r = r0 + (r1 - r0) * t if not inward else r1 - (r1 - r0) * t
    x, y = center[0] + r * np.cos(th), center[1] + r * np.sin(th)
    ln = ax.plot(x[:-6], y[:-6], color=color, lw=lw, zorder=zorder, solid_capstyle="butt")[0]
    rides_on(arrow(ax, (x[-12], y[-12]), (x[-1], y[-1]), color=color, lw=lw, head="normal", zorder=zorder), ln)
    # the sense drawn is the sense asked: cross product of successive radius vectors
    v0 = np.array([x[10] - center[0], y[10] - center[1]]); v1 = np.array([x[20] - center[0], y[20] - center[1]])
    assert np.sign(v0[0] * v1[1] - v0[1] * v1[0]) == s, "spiral turns the stated way"
    return ln


# ===================================================================== boundary layer on a flat plate
def flat_plate(ax, x0, x1, thickness, y0=0.0):
    """A flat plate seen edge-on with its top at y0, from x0 to x1: a hatched wall (chapter_1
    hatched_wall), sharp leading edge. Returns the patch. Example: flat_plate(ax, 0.0, 10.0, 0.3)"""
    from chapter_1.drawing import hatched_wall
    x = np.array([x0, x1])
    return hatched_wall(ax, x, np.full(2, y0), np.full(2, y0 - thickness))


def velocity_profile(ax, x, delta, kind="laminar", u_len=1.0, y0=0.0, n_arrows=4, label=None, color=None,
                     lw=LW_MAIN, zorder=5, no_slip=True, free_stream=True, fs_gap=None, edge_top=None,
                     wall_join=None, heights=None, min_arrow=12.0):
    """A velocity profile at station x over a wall at y0, delta and u_len in data units (the
    vertical scale is usually exaggerated: state it): the station line (thin gray, wall to the
    edge), arrows of length u(y)/U times u_len at n_arrows heights inside delta, each ending
    exactly on the profile curve (laminar: Blasius, aero.laminar_profile; turbulent: the
    one-seventh power law), the curve itself, the no-slip point (a dot on the wall, u = 0), and,
    with free_stream=True, the free-stream arrow V_inf (length u_len) just above the edge (or above
    edge_top, the highest edge over the arrow's length, when the edge rises). wall_join=j (a
    turbulent profile only) replaces the power law below y/delta = j by a cubic that starts at
    the wall with the finite slope 1.5 u(j)/j and meets the power law at j with its value and
    slope: the thin layer next to the wall where the speed rises steeply but not infinitely, so
    the drawn profile leaves the wall at a visible angle (the power law alone runs along the wall)
    and stays as full as the power law above j. heights (fractions of delta) replaces the
    n_arrows evenly spaced heights; an arrow shorter than min_arrow points is left out.
    Returns dict(curve=(x, y), tips, line, free_stream_tail). Asserts u = 0 at the wall, the
    arrow tips on the curve and the free-stream arrow longer than every arrow inside.
    Example: velocity_profile(ax, 2.0, 0.4, "laminar", u_len=0.8)"""
    eta = np.linspace(0.0, 1.0, 300)
    f = _aero.laminar_profile if kind == "laminar" else _aero.turbulent_profile
    u = f(eta)
    if wall_join and kind != "laminar":              # a cubic near the wall: u(0) = 0, finite slope s0 there,
        j = float(wall_join)                            # value and slope of the 1/7 law at y/delta = j
        F, Fp = j ** (1.0 / 7.0), (1.0 / 7.0) * j ** (-6.0 / 7.0)
        s0 = 1.5 * F / j
        c3 = (Fp + s0 - 2.0 * F / j) / j ** 2
        c2 = (F - s0 * j - c3 * j ** 3) / j ** 2
        t = np.minimum(eta, j)
        u = np.where(eta < j, s0 * t + c2 * t ** 2 + c3 * t ** 3, u)
        assert np.all(np.diff(u) >= 0.0), "the joined profile rises monotonically"
    assert float(u[0]) == 0.0, "no slip at the wall"
    col = color or INK
    ax.plot([x, x], [y0, y0 + delta], color=GRAY, lw=LW_THIN, zorder=zorder - 1)
    cx, cy = x + u * u_len, y0 + eta * delta
    ln = ax.plot(cx, cy, color=col, lw=lw, zorder=zorder, solid_capstyle="butt")[0]
    tips = []
    fr = np.linspace(0.25, 0.85, n_arrows) if heights is None else np.asarray(heights, float)
    for h in fr * delta:
        L = float(np.interp(h, cy - y0, cx - x))
        if L > pt(ax, min_arrow):
            pa = kind_arrow(ax, (x, y0 + h), (x + L, y0 + h), "velocity", None, lw=1.0, head="small")
            rides_on(pa, ln)                              # the arrow ends on the profile by design
            tips.append((x + L, y0 + h))
            close_to(float(np.interp(h, cy - y0, cx - x)), L, 1e-12, "arrow tip on the profile")
    if no_slip:
        ax.plot([x], [y0], "o", ms=4.0, color=INK, zorder=zorder + 1)
    tail = None
    if free_stream:
        g = fs_gap if fs_gap is not None else pt(ax, 9.0)
        top = y0 + (delta if edge_top is None else edge_top)
        tail = (x, top + g)
        kind_arrow(ax, tail, (x + u_len, top + g), "velocity", None, lw=1.2, head="small")
        assert all(t[0] - x <= u_len + 1e-12 for t in tips)
    if label:
        text(ax, (x + 0.5 * u_len, y0 + delta), label, direction=90, dist=4)
    return dict(curve=(cx, cy), tips=tips, line=ln, free_stream_tail=tail)


def boundary_layer_plate(ax, x_end=6.0, transition=(3.0, 3.6), Re_tr=None, stations=(1.3, 2.8, 4.1, 5.0),
                         delta_drawn=1.35, u_len=0.5, plate=0.12, dim_station=-1, labels=True, fs=FS_LABEL,
                         n_lam=3, wall_join=0.08, lam_heights=None):
    """A flat plate with its boundary layer, to one exaggerated vertical scale: the plate (hatched),
    the boundary-layer edge (dashed, labeled), laminar profiles (Blasius) ahead of the transition
    zone and turbulent ones (one-seventh power) behind it, a free-stream arrow V_inf above the
    edge at every station, the thickness delta dimensioned at one station, and under the plate
    three braces: the laminar layer, the transition zone, the turbulent layer. The flow's Reynolds
    number per unit length is set so that Re_x reaches aero.RE_TR_PLATE at the start of the
    transition zone; the turbulent thickness is 0.37 (x - x_v)/Re^(1/5) from a virtual origin x_v
    chosen so it equals the laminar 5.0 x/sqrt(Re_x) at the start of the zone, and across the zone
    the edge blends from the laminar to the turbulent law (a smooth step), so the edge starts to
    steepen where the transition brace starts. Turbulent profiles leave the wall at an angle
    (velocity_profile wall_join). lam_heights (fractions of delta, for example (1/3, 2/3)) puts
    the arrows of the laminar profiles at those heights and asserts each is drawn, so a thin
    laminar profile still shows the speed growing from the wall. delta_drawn sets the drawn thickness at the last station; the
    vertical exaggeration is returned as `vexag` (drawn height over true height, horizontal and
    vertical in the same length unit) for the caption. Returns dict(vexag, Re_per_length, x_v,
    deltas (true), drawn (drawn thicknesses), profiles).
    Example: g = boundary_layer_plate(ax); g["vexag"]"""
    from chapter_1.diagrams import brace
    x0t, x1t = transition
    Re_u = (Re_tr or _aero.RE_TR_PLATE) / x0t
    dl0 = float(_aero.delta_laminar(x0t, Re_u * x0t))
    x_v = x0t - (dl0 / 0.37 * Re_u ** 0.2) ** (1 / 0.8)

    def delta(x):
        x = np.asarray(x, float)
        lam = _aero.delta_laminar(np.maximum(x, 1e-9), Re_u * np.maximum(x, 1e-9))
        tur = _aero.delta_turbulent(np.maximum(x - x_v, 1e-9), Re_u * np.maximum(x - x_v, 1e-9))
        s = np.clip((x - x0t) / (x1t - x0t), 0.0, 1.0)
        w = s * s * (3.0 - 2.0 * s)                  # smooth step across the transition zone
        return (1.0 - w) * lam + w * tur
    k = delta_drawn / float(delta(stations[dim_station]))
    flat_plate(ax, 0.0, x_end, plate)
    xs = np.linspace(0.005, x_end, 600)
    edge = ax.plot(xs, delta(xs) * k, **line_kw("boundary"), zorder=2)[0]
    profiles = []
    for xs_ in stations:
        kind = "laminar" if xs_ < x0t else "turbulent"
        top = float(np.max(delta(np.linspace(xs_, xs_ + u_len, 50)))) * k
        lam = kind == "laminar"
        profiles.append(velocity_profile(ax, xs_, float(delta(xs_)) * k, kind, u_len=u_len,
                                         n_arrows=n_lam if lam else 4, edge_top=top, wall_join=wall_join,
                                         heights=lam_heights if lam else None,
                                         min_arrow=8.0 if (lam and lam_heights is not None) else 12.0))
        if lam and lam_heights is not None:
            assert len(profiles[-1]["tips"]) == len(lam_heights), "every laminar arrow is drawn"
    for xt in (x0t, x1t):
        close_to(float(delta(xt + 1e-7)) / float(delta(xt - 1e-7)), 1.0, 1e-5, "thickness continuous across transition")
    sl = lambda x: float(delta(x + 1e-4) - delta(x - 1e-4)) / 2e-4
    assert sl(x1t + 0.05) > 2.0 * sl(x0t - 0.05), "the edge steepens across the transition zone"
    ds = stations[dim_station]
    dd = float(delta(ds)) * k
    xd = ds + u_len + pt(ax, 12.0)
    dimension(ax, (xd, 0.0), (xd, dd), None, ticks=False, extension=False, zorder=4)
    ax.plot([ds + u_len, xd + pt(ax, 4.0)], [dd, dd], color=GRAY, lw=0.7, zorder=2)
    out = dict(vexag=k, Re_per_length=Re_u, x_v=x_v, deltas=[float(delta(s_)) for s_ in stations],
               drawn=[float(delta(s_)) * k for s_ in stations], profiles=profiles, edge=edge)
    if labels:
        text(ax, (xd, 0.5 * dd), "thickness,\n" + r"$\delta$", direction=0, dist=5, fs=fs)
        yb, gap = -plate - pt(ax, 3.0), pt(ax, 3.0)
        for a, b, s in ((pt(ax, 6.0), x0t - gap, "laminar layer"), (x0t + gap, x1t - gap, "transition"),
                        (x1t + gap, x_end, "turbulent layer")):
            brace(ax, (b, yb), (a, yb), s, fs=fs)
    return out


# ===================================================================== drag polar from data: three linked panels
def linked_polar(alpha, CL, CD, marks, width=6.5, height=2.6, flip=False, labels=("$C_L$", "$C_D$"),
                 mark_names=None, label_dir=135.0):
    """Three panels in reading order: C_L against alpha, C_D against alpha, and the polar (C_D
    against C_L; with flip=True C_L against C_D). `marks` are angles of
    attack carried through every panel: the same marker and the same letter (A, B, C, ...) on each
    panel. label_dir: the direction (deg) of each letter from its point: one value, one per mark,
    or one list per panel (put the letter on the side of the curve that is clear). Returns (fig, axes, points).
    Asserts that each marked point lies on its curve in every panel.
    Example: fig, axs, pts = linked_polar(a, CL, CD, [-2.0, 4.0, 10.0])"""
    from chapter_3.airfoil_data import pchip
    fig, axs = data_axes(width, height, ncols=3)
    fig.subplots_adjust(wspace=0.85, left=0.11, right=0.98, bottom=0.2, top=0.95)
    alpha, CL, CD = (np.asarray(v, float) for v in (alpha, CL, CD))
    names = mark_names or [chr(65 + i) for i in range(len(marks))]
    fCL, fCD = (lambda a: pchip(alpha, CL, a)), (lambda a: pchip(alpha, CD, a))
    axs[0].plot(alpha, CL, **line_kw(0)); axs[1].plot(alpha, CD, **line_kw(0))
    if flip:
        axs[2].plot(CD, CL, **line_kw(0))
    else:
        axs[2].plot(CL, CD, **line_kw(0))
    import matplotlib.ticker as _mt
    for a_ in axs:
        a_.xaxis.set_major_locator(_mt.MaxNLocator(3)); a_.yaxis.set_major_locator(_mt.MaxNLocator(4))
    axs[0].set_xlabel(r"$\alpha$, deg"); axs[0].set_ylabel(labels[0])
    axs[1].set_xlabel(r"$\alpha$, deg"); axs[1].set_ylabel(labels[1])
    axs[2].set_xlabel(labels[1] if flip else labels[0]); axs[2].set_ylabel(labels[0] if flip else labels[1])
    for a_ in axs:                      # only ticks inside the view (no hidden tick labels)
        a_.set_xlim(a_.get_xlim()); a_.set_ylim(a_.get_ylim())
        for get, put, lim in ((a_.get_xticks, a_.set_xticks, a_.get_xlim()), (a_.get_yticks, a_.set_yticks, a_.get_ylim())):
            put([t for t in get() if lim[0] - 1e-12 <= t <= lim[1] + 1e-12])
    pts = []
    for i, (a, nm) in enumerate(zip(marks, names)):
        cl, cd = float(fCL(a)), float(fCD(a))
        m = MARKERS[i % len(MARKERS)]
        for j, (ax, (px, py)) in enumerate(zip(axs, ((a, cl), (a, cd), ((cd, cl) if flip else (cl, cd))))):
            ax.plot([px], [py], m, ms=6.5, mfc="white", mec=INK, mew=1.2, zorder=6)
            d = label_dir
            if isinstance(d, (list, tuple)):
                d = d[j][i] if isinstance(d[0], (list, tuple)) else d[i]
            text(ax, (px, py), nm, direction=d, dist=10, fs=FS_SMALL)
        pts.append(dict(alpha=a, CL=cl, CD=cd, name=nm))
        close_to(float(np.interp(a, alpha, CL)), cl, 2e-3 * max(1.0, abs(cl)), "mark on the lift curve")
    return fig, axs, pts


# ===================================================================== wind-tunnel outlines as line art
def draw_tunnel(ax, T, highlight=(), fill=PART_FILL, vane_lw=1.0, model=True, zbase=2.0):
    """Draw a tunnel from tunnel.py (closed_circuit_plan() or open_circuit_side()) as line art on
    equal-aspect axes: each part a white opaque shape (light gold for the parts in `highlight`),
    walls 1.8 pt, joints between parts 1.0 pt, the honeycomb as a block of cell walls that run
    with the flow (lines along the axis), screens (lines across the flow) and turning vanes
    as thin lines, the fan as a gray band with its hub fairing, the model as the plan or side
    outline of the jet transport on its support. Walls, vanes and screens are drawn on their part
    (figkit.on_part), so a leader that ends inside a part may cross them. Returns dict name ->
    patch. Example: P = draw_tunnel(ax, closed_circuit_plan(), highlight=("test_section",))"""
    from matplotlib.patches import Polygon as Poly
    out = {}
    order = {"duct": 0.0, "corner": 0.0, "honeycomb": 0.4, "screen": 0.5, "fan": 0.6, "hub": 0.7, "support": 0.8,
             "model": 0.9}
    for name, p in T.items():
        z = zbase + order.get(p.kind, 0.0)
        if p.kind == "honeycomb":
            pa = Poly(p.poly, closed=True, fc="white", ec=INK, lw=LW_DETAIL, hatch=None, zorder=z)
            # cell walls run with the flow: lines parallel to the axis, about 7 across the duct
            # (screens are single lines across the flow, so the two straighteners look different)
            (hx0, hy0), (hx1, hy1) = p.poly.min(axis=0), p.poly.max(axis=0)
            cells = [np.array([(hx0, yy), (hx1, yy)]) for yy in np.linspace(hy0, hy1, 9)[1:-1]]
        elif p.kind == "screen":
            pa = Poly(p.poly, closed=True, fc="none", ec="none", lw=0.0, zorder=z)
        elif p.kind == "fan":
            pa = Poly(p.poly, closed=True, fc="#D9D9D9", ec=INK, lw=LW_DETAIL, zorder=z)
        elif p.kind in ("hub", "support"):
            pa = Poly(p.poly, closed=True, fc="white", ec=INK, lw=LW_DETAIL, zorder=z)
        else:
            pa = Poly(p.poly, closed=True, fc=HIGHLIGHT if name in highlight else fill, ec="none", lw=0.0,
                      zorder=z)
        ax.add_patch(pa)
        if p.kind not in ("screen",):
            opaque(pa)
        pa._part = name
        out[name] = pa
        for w in p.walls:
            on_part(ax.plot(w[:, 0], w[:, 1], color=INK, lw=LW_OUTLINE, zorder=z + 0.05, solid_capstyle="round")[0], pa)
        for j in p.joints:
            on_part(ax.plot(j[:, 0], j[:, 1], color=INK, lw=LW_DETAIL, zorder=z + 0.04)[0], pa)
        for ln in p.lines + (cells if p.kind == "honeycomb" else []):
            on_part(ax.plot(ln[:, 0], ln[:, 1], color=INK, lw=vane_lw if p.kind == "corner" else LW_FINE,
                            zorder=z + 0.06, solid_capstyle="butt")[0], pa)
    for name, p in T.items():                       # parts inside a duct part: drawn on it
        if p.host and p.host in out:
            on_part(out[name], out[p.host])
    for ln in ax.lines:
        host = getattr(ln, "_on_part", None)
        nm = getattr(host, "_part", None)
        if nm in T and T[nm].host and T[nm].host in out:
            on_part(ln, out[T[nm].host])
    if model and getattr(T, "model_parts", None):
        host = out.get("test_section")
        for n, xy in sorted(T.model_parts.items()):
            pa = ax.add_patch(Poly(xy, closed=True, fc="white", ec=INK, lw=LW_FINE, zorder=zbase + 1.0 +
                                   (0.02 if "fuselage" in n else 0.0), joinstyle="round"))
            opaque(pa)
            on_part(pa, host)
            out["model:" + n] = pa
    return out


def station_marks(ax, T, which=(1, 2, 3), fs=FS_SMALL, side=1, patches=None, inside=None):
    """The stations 1, 2, 3 of a tunnel: a dashed line across the duct at each station (thin) and a
    numbered disc just outside the wall, the dashed line run on to it (side=1: beyond the upper
    wall; -1: the lower). With
    patches (the dict draw_tunnel returns) each station line is drawn on the duct part that holds
    it, so a leader into that part may cross it. inside=f puts each disc on its station line inside
    the duct, at fraction f of the way from the lower wall (labels then have the outside to
    themselves). Returns the disc centers. Example: station_marks(ax, T, patches=P, inside=0.2)"""
    from matplotlib.path import Path as _MP
    from chapter_1.diagrams import key_disc
    out = {}
    for n in which:
        p, q = (np.asarray(v, float) for v in T.stations[n])
        on = ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=LW_THIN, ls=(0, (3.0, 2.0)), zorder=4.5)[0]
        if patches:
            mid = 0.5 * (p + q)
            for nm, tp in T.items():
                if tp.kind in ("duct", "corner") and _MP(tp.poly).contains_point(mid):
                    on_part(on, patches[nm])
                    break
        end = q if side > 0 else p
        d = (q - p) / np.hypot(*(q - p)) * side
        c = end + d * pt(ax, 15.0) if inside is None else p + inside * (q - p)
        if inside is None:                           # the station line runs on, outside the wall, to the disc
            ax.plot([end[0], c[0] - d[0] * pt(ax, 7.5)], [end[1], c[1] - d[1] * pt(ax, 7.5)], color=INK, lw=LW_THIN,
                    ls=(0, (3.0, 2.0)), zorder=4.5, gid=f"grp:station{n}")
        key_disc(ax, c, n)
        out[n] = c
    return out


def step_label(ax, xy, n, s, color=INK, fs=FS_LABEL, r=7.5):
    """A label that opens with the chapter's numbered disc: the disc centered at xy (data, equal
    aspect) and the text starting just right of it, so a figure's numbered steps read like the
    numbered steps of the text. Returns the text. Example: step_label(ax, (0.2, 0.5), 2, "downwash, $w$", BLUE)"""
    from chapter_1.diagrams import key_disc
    key_disc(ax, xy, n, r=r)
    return text(ax, xy, s, direction=0.0, dist=r + 3.0, fs=fs, color=color)


def name_part(ax, T, name, s, text_xy, start=None, target=None, fs=FS_LABEL, ha="center", va="center"):
    """Name a part of a tunnel (or any part with an `inside` point) with a label at text_xy and a
    straight leader that starts at `start` (a point just outside the label's edge, so the leader
    can leave the label where it is clear) and ends inside the part with a small dot (as
    chapter_1 label_part). Without `start` the leader leaves the label's middle (label_part).
    Returns the text. Example: name_part(ax, T, "honeycomb", "honeycomb", (21, -48), start=(36, -40.5))"""
    tgt = np.asarray(target if target is not None else T[name].inside, float)
    if start is None:
        an = callout(ax, tgt, s, text_xy, gap=1.5, fs=fs, ha=ha, va=va)
        an.arrow_patch.set_gid("leader")
        t = an
    else:
        t = text(ax, text_xy, s, fs=fs, ha=ha, va=va)
        an = callout(ax, tgt, " ", start, gap=1.5, fs=fs, backing=False)
        an.arrow_patch.set_gid("leader")
    ax.plot(*tgt, "o", ms=2.6, color=INK, zorder=12, gid=f"grp:lead-{name}")
    return t
