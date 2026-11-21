"""Figures and values of 1.3 Vehicle Anatomy (notes/chapter-1/vehicle-anatomy.md).

Vehicles: the Boeing 737-800 of chapter_1.aircraft (Boeing D6-58325-7 Rev C, 2025), the
Ariane 5 ECA and the Falcon 9 of chapter_1.launchers. Published numbers of the worked examples
are shared constants with their sources: the 737-800 reference wing and maximum takeoff weight
(B738_WING, B738_MTOW_LB, aircraft.py), the Ariane 5 flight facts (ARIANE5_FLIGHT,
launchers.py), the DC-3 sections (AIRFOIL_USAGE, geometry.py). NACA sections: NACA Report 460
(Jacobs, Ward and Pinkerton, 1933).
"""
import math

from chapter_1.common import *
from chapter_1 import diagrams as D
from chapter_1.aircraft import VIEWS, rotation_sense, _winglet_front
from chapter_1.launchers import HATCH_INK
from chapter_1.diagrams import key_disc
from chapter_1.style import _screen_angle
from matplotlib.patches import Rectangle
from matplotlib.path import Path as Path_

PG = "p13"
WINGLET_BOTTOM = B738["winglet_bottom_z"]
A5_FLIGHT = ARIANE5_FLIGHT
DC3_ROOT, DC3_TIP = AIRFOIL_USAGE["Douglas DC-3"]
ANATOMY_AIRFOIL = "4418"         # the airfoil drawn to name its parts (a choice)


def wing_example():
    """The 737-800 reference wing in feet and pounds, every step from the printed digits."""
    w = B738_WING
    b = round(w["b_m"] / FT, 2)                    # printed 112.53 ft
    S = round(w["S_m2"] / FT ** 2, 1)              # printed 1,341.2 ft^2
    lam = w["taper"]
    AR = b * b / S
    cr = 2.0 * S / (b * (1.0 + lam))
    cr_p = round(cr, 2)                            # printed 18.65 ft
    ct = lam * cr_p
    lam2 = lam * lam
    num = 1.0 + lam + lam2
    ratio = num / (1.0 + lam)
    mac = 2.0 / 3.0 * cr_p * round(ratio, 4)
    WS = B738_MTOW_LB / S
    pf = planform(b, cr, lam * cr, sweep_c4=w["sweep_c4"])
    b6 = (w["b_m"] / FT) / 6.0                     # printed 18.7555: b at full precision over 6
    yr = (1.0 + 2.0 * lam) / (1.0 + lam)           # printed 1.21753
    ymac = round(b6, 4) * round(yr, 5)             # printed 22.84 ft
    return dict(b=b, S=S, lam=lam, AR=AR, b2=b * b, two_S=2 * S, b_1l=b * (1 + lam), cr=cr, cr_p=cr_p, ct=ct,
                lam2=lam2, num=num, ratio=ratio, mac=mac, mac_m=round(mac, 2) * FT, WS=WS, pf=pf, ymac=ymac,
                b6=b6, yr=yr, mac_pub_ft=w["mac_m"] / FT)


def naca_values():
    """Decode the DC-3 root and tip sections for the root and tip chords of the 737-800 example."""
    e = wing_example()
    out = {}
    for tag, code, c in (("root", DC3_ROOT, e["cr_p"]), ("tip", DC3_TIP, round(e["ct"], 3))):
        d = naca4_decode(code)
        out[tag] = dict(code=code, c=c, m=d["max_camber"], p=d["camber_at"], t=d["thickness"],
                        m_len=d["max_camber"] * c, p_len=d["camber_at"] * c, t_len=d["thickness"] * c)
    return out


# ===================================================================== 1. the airframe in side view
def airframe_side():
    """Lesson: an airliner is a few large parts, each with one job."""
    parts = aircraft_side(ground=False)
    fig, ax = canvas(6.5, xlim=(-2.2, 47.6), ylim=(-3.2, 15.6))
    P = draw_parts(ax, parts, surfaces="hatch")
    name_parts(ax, P, parts, {
        "fuselage": ("fuselage", (4.0, 9.6), dict(target=(7.0, 3.3), ha="center")),
        "nacelle": ("engine nacelle", (9.0, -2.0), dict(target=(14.6, 1.0), ha="center")),
        "wing": ("wing", (18.5, 9.6), dict(target=(22.0, 3.2), ha="center")),
        "vtail": ("vertical stabilizer", (26.5, 14.6), dict(target=(34.4, 9.0), ha="center")),
        "rudder": ("rudder", (40.6, 11.2), dict(target=(37.55, 9.0), ha="left")),
        "htail": ("horizontal\nstabilizer", (40.6, 6.4), dict(target=(38.6, 5.5), ha="left")),
        "main_wheel": ("main landing gear", (27.5, -2.0), dict(ha="left")),
    })
    x0, x1, z0, z1 = extent({k: v for k, v in parts.items() if v.kind != "ground"})
    close_to(z1, B738["height"], 0.02, "height drawn")
    close_to(x1 - x0, B738["length"], 0.1, "length drawn (the stabilizer tip is drawn 0.25 m inboard of its end)")
    assert not any(k.startswith("cargo_door") for k in parts), "the left side has no cargo doors"
    save_figure(fig, "p13-airframe-side")


# ===================================================================== 2. front view
def front_view():
    """Lesson: from ahead, the engines hang under the wing on pylons, the wing rises toward the
    tips (dihedral), the winglets stand up at the tips, the tail surfaces stand behind, and the
    gear carries the weight."""
    parts = aircraft_front(ground=False)
    fig, ax = canvas(6.5, xlim=(-21.5, 21.5), ylim=(-3.3, 13.4))
    P = draw_parts(ax, parts)
    wl = _winglet_front()
    yc = B738["engine_y"]
    r_n = 0.5 * B738["nacelle_dia"]
    name_parts(ax, P, parts, {
        "winglet_L": ("winglet", (13.6, 10.6), dict(ha="center", target=wl["inside"])),
        "nacelle_L": ("engine nacelle", (10.5, -1.6), dict(ha="left", target=(5.6, 0.95))),
        "htail_R": ("horizontal stabilizer", (-12.2, 8.4), dict(ha="center", target=(-6.4, float(np.interp(6.4,
                     *np.array(sorted(map(tuple, (parts["htail_R"].xy * np.array([-1.0, 1.0]))[:12]))).T))))),
        "vtail": ("vertical stabilizer", (-6.5, 11.0), dict(ha="right", target=(0.0, 9.5))),
        "main_wheels_R": ("main landing gear", (-5.2, -2.2), dict(ha="right", target=(-3.13, 0.3))),
        "nose_wheels2": ("nose landing gear", (1.0, -2.6), dict(ha="center", target=(0.25, 0.25))),
    })
    # dihedral: a horizontal reference from a vertex on the wing's lower surface outboard of the
    # nacelle, on the right wing (left of the page), with the arc where the two lines part
    wr = parts["wing_R"].xy
    y_v = -7.2
    lower = wr[len(wr) // 2:]
    lower = lower[np.argsort(lower[:, 0])]
    z_v = float(np.interp(y_v, lower[:, 0], lower[:, 1]))
    line(ax, (y_v, z_v), (y_v - 9.5, z_v), "reference", zorder=2)
    angle_arc(ax, (y_v, z_v), 8.0, 180.0 - B738["dihedral"], 180.0, None)
    text(ax, (y_v - 8.0, z_v), f"dihedral angle, {fmt(B738['dihedral'], 1)}°", direction=-90, dist=4, fs=FS_LABEL)
    # the reference line runs under the wing, clear of the nacelle and its pylon
    assert y_v + 0.0 < -(yc + r_n + 0.5), "vertex outboard of the nacelle"
    z_w_far = float(np.interp(y_v - 9.5, lower[:, 0], lower[:, 1]))
    # the lower surface rises at the dihedral angle plus a little, as the wing thins toward the tip
    close_to(math.degrees(math.atan2(z_w_far - z_v, 9.5)), B738["dihedral"], 0.6, "the wing rises at the dihedral angle")
    # the winglet leans outward: its tip is the outermost point
    assert float(parts["winglet_L"].xy[:, 0].max()) == max(float(p.xy[:, 0].max()) for p in parts.values())
    close_to(float(parts["winglet_L"].xy[:, 1].max()), B738["winglet_top_z"], 1e-6, "winglet top")
    save_figure(fig, "p13-front-view")


# ===================================================================== 3. the moving surfaces
def moving_surfaces():
    """Lesson: the moving surfaces sit at the edges of the wing and the tail."""
    from chapter_1.aircraft import _wing_le_te
    parts = aircraft_top()
    fig, ax = canvas(6.5, xlim=(-8.5, 52.0), ylim=(-20.5, 20.5))
    P = draw_parts(ax, parts, surfaces="hatch")
    sp2, sp1 = parts["spoiler_2_R"].xy, parts["spoiler_1_R"].xy
    y2, y1 = 6.05, 3.1                                        # leaders reach the spoilers past the engine, mid-panel
    x2 = float(np.mean(_wing_le_te(B738, y2))) + 0.16 * np.diff(_wing_le_te(B738, y2))[0]
    x1 = float(np.mean(_wing_le_te(B738, y1))) + 0.16 * np.diff(_wing_le_te(B738, y1))[0]
    le9, te9 = _wing_le_te(B738, 9.0)
    name_parts(ax, P, parts, {
        "slat_3_R": ("slats", (12.5, 15.5), dict(ha="right")),
        "spoiler_2_R": ("spoilers (five panels)", (9.5, 6.9), dict(ha="right", target=(x2, y2))),
        "spoiler_1_R": ("spoiler", (9.5, y1), dict(ha="right", target=(x1, y1))),
        "flap_inboard_R": ("inboard flap", (25.5, 6.2), dict(ha="left", target=(21.0, 3.2))),
        "flap_outboard_R": ("outboard flap", (31.5, 11.0), dict(ha="left", target=(le9 + 0.88 * (te9 - le9), 9.0))),
        "aileron_R": ("aileron", (31.5, 15.4), dict(ha="left")),
        "elevator_R": ("elevator", (43.0, 9.0), dict(ha="left")),
        # the pylon joins the nacelle to the wing: named on the left wing, which carries no other label
        "pylon_L": ("pylon", (9.0, -9.0), dict(ha="right", target=(0.5 * (float(parts["pylon_L"].xy[:, 0].min())
                                                                       + _wing_le_te(B738, B738["engine_y"])[0]),
                                                                  float(parts["pylon_L"].inside[1])))),
    })
    text(ax, (B738["wing_tip_te"] + 2.5, 18.6), "right wing", ha="left", va="center", backing=False, fs=FS_LABEL)
    text(ax, (B738["wing_tip_te"] + 2.5, -18.6), "left wing", ha="left", va="center", backing=False, fs=FS_LABEL)
    assert float(parts["aileron_R"].xy[:, 1].mean()) > 0, "seen from above, the right wing is up the page"
    for tgt, part in (((x2, y2), sp2), ((x1, y1), sp1)):
        assert Path_(part).contains_point(tgt), "each spoiler leader ends in its panel"
    save_figure(fig, "p13-moving-surfaces")


# ===================================================================== 4. body axes in three views
OUTLINE_GRAY = "#555960"         # the plain aircraft under the axes: dark gray, so the axes stand out


def plain_outline(ax, parts, color=OUTLINE_GRAY, lw=1.0):
    """The aircraft as a plain outline: every outer part (no details, no hidden lines, control
    surfaces drawn like the rest), white and opaque, in one thin gray line. Returns the patches."""
    out = {}
    for name, p in sorted(parts.items(), key=lambda kv: kv[1].z):
        if p.hidden or p.kind in ("detail", "line", "ground", "surface") or (p.kind == "strut" and "pylon" in name):
            continue
        pa = opaque(ax.add_patch(Polygon(p.xy, closed=True, fc=PART_FILL, ec=color, lw=lw, joinstyle="round",
                                         zorder=p.z)))
        pa._part = name
        out[name] = pa
    return out


def body_axes_three_view():
    """Lesson: each rotation is about one body axis through the center of gravity, and one set of
    surfaces commands it; each curved arrow shows the positive sense at the part that moves."""
    from chapter_1.aircraft import place
    gap = 12.0
    v = three_view(gap=gap, detail=False, ground=False)
    x, _, z = cg_point()
    Lf, b2 = B738["length"], 0.5 * B738["span"]
    top_dy = v["top_dy"]
    front_dx = Lf + gap + 4.5 + b2
    front_dz = top_dy - z                                    # the front view beside the top view, its CG level with the top view's
    front = place(aircraft_front(detail=False, ground=False), front_dx, front_dz)
    X0, X1 = -10.0, front_dx + b2 + 2.5
    fig, ax = canvas(6.5, xlim=(X0, X1), ylim=(top_dy - 19.5, 18.0))
    for parts in (v["side"], v["top"], front):
        plain_outline(ax, parts)
    W = 1.7                                                  # axes and arcs, black and heavier than the outline
    r_n = 24.5                                               # arcs just ahead of the nose (beyond the x-axis tip)
    fs = FS_SMALL
    cs = body_axes(ax, "side", (x, z), length={"x": x + 3.2, "z": 6.0}, radius=r_n, rot_span=(193.0, 167.0),
                   rot_label="positive pitch: nose up (elevator)", rot_label_at=167.0, perp_at=(x + 2.5, z + 4.2),
                   lw=W, label_dirs={"x": 90.0}, rot_label_dir=60.0, rot_dist=12.0, fs=fs)
    ct = body_axes(ax, "top", (x, top_dy), length={"x": x + 3.2, "y": b2 + 1.0}, radius=r_n, rot_span=(193.0, 167.0),
                   rot_label="positive yaw:\nnose right\n(rudder)", rot_label_at=167.0, perp_at=(x + 6.5, top_dy),
                   lw=W, label_dirs={"x": -90.0}, rot_label_dir=45.0, rot_dist=4.0, fs=fs)
    zc = z + front_dz
    cf = body_axes(ax, "front", (front_dx, zc), length={"y": b2 + 2.5, "z": 7.0}, radius=b2 + 4.8,
                   rot_span=(166.0, 194.0), rot_label="positive roll:\nright wing down\n(ailerons)", rot_label_at=194.0,
                   perp_at=(front_dx + 3.0, zc - 6.5), lw=W, label_dirs={"y": -60.0}, rot_label_dir=-90.0, rot_dist=4.0,
                   fs=fs)
    # which wing is the right one
    text(ax, (24.5, top_dy + 13.0), "right wing", ha="left", va="center", backing=False, fs=fs)
    text(ax, (24.5, top_dy - 13.0), "left wing", ha="left", va="center", backing=False, fs=fs)
    text(ax, (front_dx - 10.0, zc + 5.2), "right wing", ha="center", va="center", backing=False, fs=fs)
    text(ax, (front_dx + 10.0, zc + 5.2), "left wing", ha="center", va="center", backing=False, fs=fs)
    # key to the two symbols, beside the side view
    kx, ky = Lf + gap + 1.5, 10.0
    perp_symbol(ax, (kx, ky), True)
    text(ax, (kx, ky), "axis pointing toward you", direction=0.0, dist=10.0, fs=fs)
    perp_symbol(ax, (kx, ky - 4.6), False)
    text(ax, (kx, ky - 4.6), "axis pointing away from you", direction=0.0, dist=10.0, fs=fs)
    for (xx, yy, s_) in ((X0 + 0.3, 17.5, "side view"), (front_dx - b2 - 1.0, zc + 13.6, "front view"),
                         (X0 + 0.3, top_dy + 21.5, "top view,\nfrom above")):     # each title above its view
        text(ax, (xx, yy), s_, va="top", ha="left", backing=False, fs=FS_LABEL, fontweight="bold")
    # the drawn y axis of the top view points to the right wing, which is up the page
    assert ct["y"][1] > 0 and float(v["top"]["wing_R"].xy[:, 1].mean()) > top_dy
    assert cs["y"][2] < 0 and cf["x"][2] > 0 and ct["z"][2] < 0
    # the front view shows all three axes: y toward the right wing, on the reader's left; z down
    assert cf["y"][0] < 0 and cf["z"][1] < 0
    assert float(front["wing_R"].xy[:, 0].mean()) < front_dx, "front view: the right wing on the reader's left"
    # each arc clears the airplane: ahead of the nose, beyond the right wing tip (with its winglet)
    assert r_n > x + 3.2 + 2.0 and b2 + 4.8 > float(np.hypot(*(np.array(front["winglet_R"].xy) - [front_dx, zc]).T).max()) + 1.0
    save_figure(fig, "p13-body-axes")


# ===================================================================== 4b. a deflected control surface: cause, force, rotation
def _tail_section(chord, z0, x0, hinge=0.70, defl=15.0):
    """The horizontal stabilizer in side view as a NACA 0010 section from x0, cut at the hinge:
    the fixed part and the elevator, the elevator turned about the hinge by defl degrees
    (counterclockwise on the page, nose to the left: trailing edge up). Returns (stabilizer,
    elevator, hinge point)."""
    sec = naca4("0010", n=121, chord=chord)
    xu, yu, xl, yl = sec["xu"], sec["yu"], sec["xl"], sec["yl"]
    xh = hinge * chord
    yh_u, yh_l = float(np.interp(xh, xu, yu)), float(np.interp(xh, xl, yl))
    fu, fl = xu <= xh, xl <= xh
    stab = np.r_[np.c_[xu[fu], yu[fu]], [(xh, yh_u), (xh, yh_l)], np.c_[xl[fl][::-1], yl[fl][::-1]]]
    ru, rl = xu > xh, xl > xh
    elev = np.r_[[(xh, yh_u)], np.c_[xu[ru], yu[ru]], np.c_[xl[rl][::-1], yl[rl][::-1]], [(xh, yh_l)]]
    hp = np.array([xh, 0.0])
    elev = rotate_xy(elev, defl, about=hp)
    off = np.array([x0, z0])
    return stab + off, elev + off, hp + off


def _lower_edge(xy, x):
    """The lowest point of a closed outline at station x (the outline's edges that span x)."""
    ys = []
    for (x0, y0), (x1, y1) in zip(xy, np.roll(xy, -1, axis=0)):
        if min(x0, x1) <= x <= max(x0, x1) and x0 != x1:
            ys.append(y0 + (y1 - y0) * (x - x0) / (x1 - x0))
    return float(min(ys))


def control_deflection():
    """Lesson (cause, force, rotation, in that order): the pilot pulls the column back and the
    elevator's trailing edge goes up (1, enlarged at the right); the air then pushes the tail down
    (2); the aircraft pitches nose up about its center of gravity (3)."""
    parts = aircraft_side(detail=False)
    fig, ax = canvas(6.5, xlim=(-9.5, 50.0), ylim=(-26.0, 15.2))
    plain_outline(ax, parts)
    x, _, z = cg_point()
    cg_symbol(ax, (x, z))
    callout(ax, (x, z), "center of gravity", at=(x - 2.0, 9.6), ha="center", gap=6.0, fs=FS_SMALL)
    # the tail, circled, and its enlargement below
    ht = parts["htail"].xy
    tc = np.array([0.5 * (ht[:, 0].min() + ht[:, 0].max()), 0.5 * (ht[:, 1].min() + ht[:, 1].max())])
    rc = 3.6
    circ = ax.add_patch(Circle(tuple(tc), rc, fc="none", ec=GRAY, lw=LW_THIN, zorder=8))
    k, chord_ = 7.0, 4.4
    ci = np.array([20.0, -16.0])                             # center of the enlarged tail section
    x_le = ci[0] - 0.5 * chord_ * k
    stab, elev, hp = _tail_section(chord_ * k, ci[1], x_le)
    neutral = _tail_section(chord_ * k, ci[1], x_le, defl=0.0)[1]
    ax.add_patch(Polygon(neutral, closed=True, fc="none", ec=INK, lw=LW_THIN, ls=(0, (3.0, 2.0)), zorder=5))
    opaque(ax.add_patch(Polygon(stab, closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, joinstyle="round", zorder=6)))
    ep = ax.add_patch(Polygon(elev, closed=True, fc=SURFACE_FILL, ec=INK, lw=LW_DETAIL + 0.3, joinstyle="round",
                              zorder=6.5))
    ep.set_hatch(HATCH_SURFACE)
    opaque(ep)
    ax.plot(*hp, "o", ms=3.0, color=INK, zorder=7)
    callout(ax, (hp[0] - 0.6, hp[1] - 0.45), "hinge", at=(hp[0] - 3.2, ci[1] - 3.0), ha="right", gap=2.0, fs=FS_SMALL)
    connects(ax.plot([tc[0] - rc * 0.2, x_le + 3.0], [tc[1] - rc * 0.98, ci[1] + 2.4], color=GRAY, lw=LW_THIN,
                     zorder=1.5)[0], circ)
    text(ax, (ci[0] + 1.0, ci[1] + 7.0), f"the tail, enlarged {fmt(k, 1)} times", ha="left", va="center", backing=False,
         fs=FS_SMALL, fontweight="bold")
    callout(ax, (x_le + 0.35 * chord_ * k, ci[1] + 0.5), "horizontal stabilizer (fixed)", at=(x_le + 1.0, ci[1] - 5.6),
            ha="left", gap=2.0, fs=FS_SMALL)
    te = elev[np.argmax(elev[:, 0])]
    callout(ax, tuple(elev.mean(axis=0)), "elevator, trailing edge up", at=(ci[0] + 4.0, ci[1] + 3.9), ha="left",
            gap=2.0, fs=FS_SMALL)
    key_disc(ax, (ci[0] + 2.1, ci[1] + 3.9), 1)
    nte = neutral[np.argmax(neutral[:, 0])]
    callout(ax, tuple(0.5 * (nte + hp) + np.array([0.0, -0.35])), "elevator in its\nneutral position (dashed)",
            at=(ci[0] + 9.0, ci[1] - 5.6), ha="left", gap=2.0, fs=FS_SMALL)
    # 2: the force on the tail, down, where it acts: from the stabilizer's lower surface, behind the tail cone
    xf = ht[:, 0].max() - 1.0
    zt = _lower_edge(ht, xf)
    kind_arrow(ax, (xf, zt), (xf, zt - 5.6), "force")
    text(ax, (xf, zt - 4.4), "force on the\ntail, down", direction=0.0, dist=9.0, fs=FS_SMALL)
    key_disc(ax, (xf + 1.2, zt - 7.6), 2)
    # 3: the rotation about the center of gravity, nose up (clockwise on the page, nose to the left)
    r = x + 3.5
    rotation_arrow(ax, (x, z), r, 196.0, 164.0, "the nose\npitches up", 164.0, dist=9.0, fs=FS_SMALL, lw=1.7,
                   label_dir=90.0)
    key_disc(ax, (x - r * math.cos(math.radians(16.0)) - 5.4, z + r * math.sin(math.radians(16.0)) + 2.6), 3)
    # asserts: the elevator's trailing edge is above the neutral one; the force points down, behind the
    # center of gravity, so its moment about it is nose up (clockwise on the page)
    assert te[1] > neutral[np.argmax(neutral[:, 0])][1] + 0.5, "trailing edge up"
    assert xf - x > 0, "a downward force behind the center of gravity pitches the nose up"
    assert rotation_sense("side") == "clockwise"
    save_figure(fig, "p13-control-deflection")


# ===================================================================== 5. landing-gear arrangements
OUTRIGGER_LABEL = (-0.06, -0.13)                        # the side-view label of the bicycle layout


def gear_layouts():
    """Lesson: the arrangements differ in where the main wheels stand relative to the center of
    gravity and in how many wheels share the weight. Each panel: side view above, view from below
    under it, one generic airplane, every wheel on structure, the center of gravity at one x."""
    kinds = ["tricycle", "tail-dragger", "multi-bogie", "bicycle", "single main", "quadricycle"]
    fig, axs = new_axes(6.5, 4.95, ncols=3, nrows=2)
    fig.subplots_adjust(left=0.005, right=0.995, bottom=0.005, top=0.995, wspace=0.04, hspace=0.03)
    ys, yp = 0.0, -0.545                                   # ground line of the side view; centerline of the plan view
    pitches = {}
    for ax, k in zip(axs.flat, kinds):
        ax.set_xlim(-0.10, 1.08)
        ax.set_ylim(-0.99, 0.405)
        side = {}
        pitches[k], contacts = gear_side(ax, k, (0.0, ys), out=side)
        plan = draw_gear_layout(ax, k, origin=(0.0, yp))
        text(ax, (0.49, -0.945), k, va="center", backing=False, fs=FS_LABEL, fontweight="bold")
        lay = GEAR_LAYOUTS[k]
        mains = [u[0] for u in lay["units"] if u[5] == "main"]
        cy = [c[1] for c in contacts]
        assert min(cy) > ys - 1e-9 and abs(min(cy) - ys) < 1e-9, k                 # every wheel on the ground
        assert side["body_low"] > ys + 0.02, f"{k}: the fuselage stands clear of the ground"
        # one center of gravity: the same station in both views (the pitch moves the side view a little)
        close_to(side["cg"][0], plan["cg"][0], 0.03, f"{k}: center of gravity at one station in both views")
        if k in ("tricycle", "multi-bogie"):
            assert lay["cg"] < min(mains), f"{k}: center of gravity ahead of the main wheels"
        if k in ("tail-dragger", "single main"):
            assert min(mains) < lay["cg"] < min(mains) + 0.06, f"{k}: center of gravity just behind the main wheels"
        if k in ("bicycle", "quadricycle"):
            assert min(mains) < lay["cg"] < max(mains), f"{k}: center of gravity between the main units"
        if k == "tricycle":
            text(ax, (-0.085, 0.385), "side view", ha="left", va="top", backing=False, fs=FS_SMALL)
            text(ax, (-0.085, -0.115), "view from below", ha="left", va="top", backing=False, fs=FS_SMALL)
            callout(ax, side["cg"], "center of\ngravity", at=(0.37, 0.335), ha="left", gap=5.0, fs=FS_SMALL)
            nose = [c for r, c in plan["units"] if r == "nose"][0]
            callout(ax, nose, "nose wheel", at=(-0.085, -0.33), ha="left", gap=4.0, fs=FS_SMALL)
            main = [c for r, c in plan["units"] if r == "main" and c[1] > yp][0]
            callout(ax, main, "main wheels", at=(0.66, -0.25), ha="left", gap=4.5, fs=FS_SMALL)
        if k == "tail-dragger":
            tw = [c for r, c in plan["units"] if r == "tail"][0]
            callout(ax, tw, "tail wheel", at=(0.80, -0.32), ha="center", gap=4.0, fs=FS_SMALL)
        if k == "multi-bogie":
            bg = [c for r, c in plan["units"] if r == "main" and c[1] > yp][0]
            callout(ax, bg, "bogie", at=(0.76, -0.25), ha="left", gap=7.0, fs=FS_SMALL)
        if k == "bicycle":
            og = [c for r, c in plan["units"] if r == "outrigger" and c[1] > yp][0]
            callout(ax, og, "outrigger", at=(0.70, -0.20), ha="left", gap=4.0, fs=FS_SMALL)
            # in the side view the wing-tip outrigger stands between the main wheels: name it there.
            # From above, a leader would pass the center-of-gravity symbol, which stands right over
            # the outrigger, and cross the fuselage and the wing; the fin leaves no room for a label
            # to the right of the symbol. So the label stands under the ground line, and its leader
            # rises at a shallow slope to the outrigger's wheel, clear of every other part
            ow = np.asarray(side["centers"]["outrigger"][0])
            an = callout(ax, tuple(ow), "outrigger, at\nthe wing tip", at=OUTRIGGER_LABEL, ha="left", gap=0.0,
                         fs=FS_SMALL)
            from matplotlib.text import Text
            fig.canvas.draw()
            bb = Text.get_window_extent(an).transformed(ax.transData.inverted())
            c0 = np.array([0.5 * (bb.x0 + bb.x1), 0.5 * (bb.y0 + bb.y1)])
            u = (ow - c0) / np.hypot(*(ow - c0))
            dcg = np.asarray(side["cg"]) - c0
            miss = abs(dcg[0] * u[1] - dcg[1] * u[0])
            assert miss > pt(ax, 4.0 + 0.5 + 3.0), "the outrigger leader passes 3 pt or more from the cg symbol"
            assert bb.y1 < ys - pt(ax, 2.0) and bb.y0 > og[1], \
                "the outrigger label stands between the ground line and the view from below"
    assert pitches["tail-dragger"] > 3.0 and pitches["single main"] > 3.0, "tail-dragger and sailplane sit nose up"
    assert abs(pitches["tricycle"]) < 1.0 and abs(pitches["quadricycle"]) < 1.0, "tricycle and quadricycle sit level"
    save_figure(fig, "p13-gear-layouts")


# ===================================================================== 6. wing planform (worked example 1)
def mac_by_construction(pf):
    """The graphical construction of the mean aerodynamic chord used on the page: extend the root
    chord aft by the tip chord (point A), extend the tip chord forward by the root chord (point B);
    the line AB crosses the mid-chord line at the station of the MAC. Half-wing coordinates
    (x aft from the root leading edge, y outboard). Returns A, B, the crossing and the MAC ends."""
    (x0, _), (x1, h), (x2, _), (x3, _) = pf["corners"]
    A = np.array([x3 + pf["c_t"], 0.0])
    B = np.array([x1 - pf["c_r"], h])
    m0, m1 = np.array([0.5 * (x0 + x3), 0.0]), np.array([0.5 * (x1 + x2), h])
    d1, d2 = B - A, m1 - m0
    cr_ = lambda u, v: u[0] * v[1] - u[1] * v[0]           # noqa: E731
    t = cr_(m0 - A, d2) / cr_(d1, d2)
    X = A + t * d1
    le = x0 + (x1 - x0) * X[1] / h
    return dict(A=A, B=B, mid_root=m0, mid_tip=m1, cross=X, mac_le=np.array([le, X[1]]),
                mac_te=np.array([le + chord_at(pf, X[1]), X[1]]))


def wing_planform():
    """Lesson, two panels at one scale: (a) span, area, the root and tip chords and the sweep fix a
    straight-tapered wing; (b) the mean aerodynamic chord is found by a construction of four
    numbered steps (737-800 reference wing)."""
    e = wing_example()
    pf = e["pf"]
    h = 0.5 * pf["b"]
    cr, ct = pf["c_r"], pf["c_t"]
    corners = pf["corners"]
    xt = corners[1][0]                                       # tip leading edge, aft of the root leading edge
    P_ = lambda x, y: (y, -x)                               # noqa: E731  span to the right, chord downward
    dy_b = -(xt + ct) - 30.0                                 # panel (b) drawn under panel (a)
    Pb = lambda x, y: (y, -x + dy_b)                        # noqa: E731
    fig, ax = canvas(6.5, xlim=(-h - 4.0, h + 21.0), ylim=(dy_b - (xt + ct) - 9.0, 13.5))
    fs = FS_SMALL
    # ---------------- (a) the reference wing
    text(ax, (-h - 3.6, 12.6), "(a) the reference wing", ha="left", va="center", backing=False, fs=FS_LABEL,
         fontweight="bold")
    outline = np.array([P_(*corners[0]), P_(*corners[1]), P_(*corners[2]), P_(*corners[3]),
                        P_(corners[2][0], -h), P_(corners[1][0], -h)])
    opaque(ax.add_patch(Polygon(outline, closed=True, fc=HIGHLIGHT, ec=INK, lw=LW_OUTLINE, joinstyle="round", zorder=3)))
    ax.plot([0, 0], [4.5, -cr - 0.8], **line_kw("boundary"), zorder=2.5)
    text(ax, (0.0, 4.5), "centerline", direction=90.0, dist=3.0, fs=fs)
    # forward arrow, leading and trailing edge
    arrow(ax, (h + 12.0, -17.0), (h + 12.0, -9.5), color=INK, lw=1.2, head="normal", zorder=4)
    text(ax, (h + 12.0, -9.5), "forward", direction=90.0, dist=3.0, fs=fs)
    le_at = P_(0.45 * xt, 0.45 * h)
    callout(ax, le_at, "leading edge", at=(0.20 * h, 8.2), ha="left", gap=2.0, fs=fs)
    te_at = P_(0.6 * xt + cr + 0.6 * (ct - cr), -0.6 * h)
    callout(ax, te_at, "trailing edge", at=(-0.92 * h, -(xt + ct) - 2.5), ha="left", gap=2.0, fs=fs)
    # span, below the wing
    yd = -(xt + ct) - 6.5
    for yy in (-h, h):
        ax.plot([yy, yy], [-(xt + ct) - 1.5, yd - 1.2], color=INK, lw=0.7, zorder=2)
    arrow(ax, (-h, yd), (h, yd), color=INK, lw=LW_THIN, head="small", both=True, zorder=2.5)
    text(ax, (0.30 * h, yd), f"span, $b$ = {fmt_dec(e['b'], 2)} ft", direction=-90.0, dist=3.0, fs=fs)
    # root chord on the centerline, named in the white wedge behind the root
    arrow(ax, (0.0, 0.0), (0.0, -cr), color=INK, lw=LW_THIN, head="small", both=True, zorder=4.5)
    text(ax, (0.0, -cr), f"root chord,\n$c_r$ = {fmt(e['cr_p'])} ft", direction=-90.0, dist=14.0, fs=fs)
    # tip chord, beside the right tip: arrows outside pointing in
    xtip = h + 1.8
    for xx in (xt, xt + ct):
        ax.plot([h + 0.6, xtip + 1.0], [-xx, -xx], color=INK, lw=0.7, zorder=2)
    dimension_outside(ax, (xtip, -(xt + ct)), (xtip, -xt), None, lead=12.0)
    text(ax, (xtip + 1.0, -(xt + 0.5 * ct)), f"tip chord,\n$c_t$ = {fmt(e['ct'])} ft", direction=0.0, dist=6.0, fs=fs)
    # quarter-chord line and its sweep, left half: a larger arc
    q0 = P_(0.25 * cr, 0.0)
    q1 = P_(xt + 0.25 * ct, -h)
    ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color=INK, lw=1.2, ls=(0, (7.0, 2.2, 1.4, 2.2)), zorder=4)
    sw = pf["sweep_c4"]
    ra = 15.0
    ax.plot([q0[0], q0[0] - ra - 2.5], [q0[1], q0[1]], color=INK, lw=LW_THIN, zorder=4)
    angle_arc(ax, q0, ra, 180.0, 180.0 + sw, None)
    am = math.radians(180.0 + 0.55 * sw)
    callout(ax, (q0[0] + ra * math.cos(am), q0[1] + ra * math.sin(am)),
            f"quarter-chord line,\nswept back $\\Lambda$ = {fmt(sw, 2)}°", at=(-h + 3.5, -0.3), ha="left", gap=2.0,
            fs=fs)
    callout(ax, (0.55 * h, -0.5 * (cr + xt + ct) + 1.0), f"wing area,\n$S$ = {fmt_dec(e['S'], 1)} ft² (shaded)",
            at=(0.74 * h, 8.2), ha="left", gap=2.0, fs=fs)
    # ---------------- (b) the construction of the mean aerodynamic chord, right half-wing
    text(ax, (-h - 3.6, dy_b + 9.0), "(b) finding the mean aerodynamic chord", ha="left", va="center",
         backing=False, fs=FS_LABEL, fontweight="bold")
    half = np.array([Pb(*corners[0]), Pb(*corners[1]), Pb(*corners[2]), Pb(*corners[3])])
    opaque(ax.add_patch(Polygon(half, closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, joinstyle="round", zorder=3)))
    ax.plot([0, 0], [dy_b + 3.0, dy_b - (cr + xt + 6.0)], **line_kw("boundary"), zorder=2.5)
    c = mac_by_construction(pf)
    A, B = Pb(*c["A"]), Pb(*c["B"])
    m0, m1 = Pb(*c["mid_root"]), Pb(*c["mid_tip"])
    R0, T1 = Pb(cr, 0.0), Pb(xt, h)
    ax.plot([R0[0], A[0]], [R0[1], A[1]], color=INK, lw=1.8, zorder=4.3, solid_capstyle="butt")      # step 1
    ax.plot([T1[0], B[0]], [T1[1], B[1]], color=INK, lw=1.8, zorder=4.3, solid_capstyle="butt")      # step 2
    ax.plot([A[0], B[0]], [A[1], B[1]], color=INK, lw=LW_THIN, zorder=4.2)                          # step 3
    ax.plot([m0[0], m1[0]], [m0[1], m1[1]], color=INK, lw=LW_THIN, ls=(0, (3.0, 2.0)), zorder=4.2)   # mid-chord line
    le, te = Pb(*c["mac_le"]), Pb(*c["mac_te"])
    ax.plot([le[0], te[0]], [le[1], te[1]], color=INK, lw=LW_MAIN + 1.0, zorder=5, solid_capstyle="butt")
    X = Pb(*c["cross"])
    ax.plot(*X, "o", ms=4.0, color=INK, zorder=6)
    disc_leader(ax, (0.0, 0.5 * (R0[1] + A[1])), 1, (-6.0, 0.5 * (R0[1] + A[1])))
    disc_leader(ax, (T1[0], 0.5 * (T1[1] + B[1])), 2, (T1[0] + 6.0, 0.5 * (T1[1] + B[1])))
    k3 = 0.25
    disc_leader(ax, (A[0] + k3 * (B[0] - A[0]), A[1] + k3 * (B[1] - A[1])), 3,
                (A[0] + k3 * (B[0] - A[0]) + 2.5, A[1] + k3 * (B[1] - A[1]) - 6.5))
    disc_leader(ax, tuple(X), 4, (X[0] - 6.0, X[1] + 5.5))
    sm = 0.80
    callout(ax, (m0[0] + sm * (m1[0] - m0[0]), m0[1] + sm * (m1[1] - m0[1])), "mid-chord line",
            at=(h - 6.0, dy_b - (xt + ct) - 5.0), ha="center", gap=2.0, fs=fs)
    callout(ax, (le[0], le[1] - 0.2 * (le[1] - te[1])),
            f"mean aerodynamic chord,\n{fmt(e['mac'])} ft long, {fmt(e['ymac'])} ft\nfrom the centerline",
            at=(0.42 * h, dy_b + 3.0), ha="left", gap=2.0, fs=fs)
    steps = ["extend the root chord rearward by $c_t$", "extend the tip chord forward by $c_r$", "join the two ends",
             "where that line crosses the\nmid-chord line is the station"]
    for n, s_ in enumerate(steps, start=1):
        yk = dy_b + 2.0 - 5.4 * (n - 1)
        key_disc(ax, (-h - 1.5, yk), n)
        if "\n" in s_:                                      # a two-line step: the disc beside its first line
            text(ax, (-h - 1.5, yk), s_, direction=0.0, dist=11.0, fs=fs, va="top", offset=(0.0, 0.6 * fs))
        else:
            text(ax, (-h - 1.5, yk), s_, direction=0.0, dist=11.0, fs=fs)
    # asserts: the construction lands where the formula puts the MAC; the drawing has the example's area
    close_to(c["cross"][1], pf["y_mac"], 1e-6, "construction finds the MAC station")
    cc = mac_construction(pf)
    close_to(cc["cross"][1], c["cross"][1], 1e-6, "both constructions agree")
    close_to(chord_at(pf, c["cross"][1]), pf["mac"], 1e-6, "MAC length")
    close_to(polygon_area(outline), e["S"], 0.05, "area of the drawn wing")
    close_to(np.hypot(*(np.array(A) - np.array(R0))), ct, 1e-9, "step 1 extends the root chord by c_t")
    close_to(np.hypot(*(np.array(B) - np.array(T1))), cr, 1e-9, "step 2 extends the tip chord by c_r")
    save_figure(fig, "p13-wing-planform")


# ===================================================================== 7. airfoil parts
def airfoil_parts():
    """Lesson: a section is fixed by its chord line, its mean camber line and its thickness."""
    sec = naca4(ANATOMY_AIRFOIL, n=201, chord=1.0)
    fig, ax = canvas(6.5, xlim=(-0.20, 1.20), ylim=(-0.36, 0.33))
    d = draw_section(ax, sec)
    m, p, t = sec["m"], sec["p"], sec["t"]
    callout(ax, (0.0, 0.0), "leading edge", at=(-0.02, 0.20), ha="right", gap=3.0)
    callout(ax, (1.0, 0.0), "trailing edge", at=(1.10, 0.13), ha="center", gap=3.0)
    ax.plot(0.0, 0.0, "o", ms=3.0, color=INK, zorder=12, gid="grp:le")
    ax.plot(1.0, 0.0, "o", ms=3.0, color=INK, zorder=12, gid="grp:te")
    callout(ax, (0.80, 0.0), "chord line", at=(0.80, -0.155), ha="center", gap=1.5)
    yc62 = float(np.interp(0.62, sec["x"], sec["yc"]))
    callout(ax, (0.62, yc62), "mean camber line", at=(0.70, 0.22), ha="left", gap=1.5)
    # maximum camber at 0.4c: a small dimension, named from above through the upper surface
    dimension_outside(ax, (p, 0.0), (p, m), None, lead=14.0)
    callout(ax, (p, m + pt(ax, 14.0)), f"maximum camber,\nat {fmt(100 * p, 2)}% of the chord", at=(0.10, 0.265),
            ha="left", gap=1.0)
    # maximum thickness at 0.3c
    xt = sec["x_tmax"]
    yu = float(np.interp(xt, sec["xu"], sec["yu"]))
    yl = float(np.interp(xt, sec["xl"], sec["yl"]))
    dimension_outside(ax, (xt, yl), (xt, yu), None, lead=11.0)
    text(ax, (xt, yl), f"maximum thickness,\nat {fmt(100 * xt, 2)}% of the chord", direction=-90.0, dist=16.0,
         fs=FS_LABEL)
    # chord c below
    dimension(ax, (0.0, -0.265), (1.0, -0.265), "chord, $c$", offset=0.0, label_side=-1, extension=False)
    for x in (0.0, 1.0):
        ax.plot([x, x], [-0.04, -0.285], color=INK, lw=0.7, zorder=2)
    close_to(float(sec["yc"].max()), m, 1e-4, "maximum camber drawn")
    close_to(xt, 0.30, 0.005, "maximum thickness at 30% of the chord")
    close_to(yu - yl, t, 0.01, "thickness drawn")
    save_figure(fig, "p13-airfoil-parts")


# ===================================================================== 8. what each digit of a NACA number does
def _naca_name(code, bold):
    """'NACA 4416' with the digits at the positions in `bold` set in bold (mathtext, Arial bold)."""
    out = "".join(f"$\\mathbf{{{c}}}$" if i in bold else c for i, c in enumerate(code))
    return "NACA " + out


def _surface_at(sec, x, upper=True):
    xs, ys = (sec["xu"], sec["yu"]) if upper else (sec["xl"], sec["yl"])
    return float(np.interp(x, xs, ys))


def naca_digits():
    """Lesson: each digit changes one feature of the shape: the first the camber, the second
    where the camber peaks, the last two the thickness. In each row the first section named is
    dashed and the second solid; the changing digits are set in bold."""
    rows = [("first digit:\nmaximum camber", "0016", "4416", (0,)),
            ("second digit:\nwhere the camber\nis largest", "4216", "4616", (1,)),
            ("last two digits:\nthickness", "4408", "4424", (2, 3))]
    fig, axs = new_axes(6.5, 5.2, nrows=3)
    fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0, hspace=0.0)
    camber_kw = dict(color=INK, lw=1.0, ls=(0, (7.0, 2.2, 1.4, 2.2)))
    for i, (ax, (title, a, b, bold)) in enumerate(zip(axs, rows)):
        ax.set_xlim(-0.62, 1.42)
        ax.set_ylim(-0.20, 0.235)
        text(ax, (-0.60, 0.02), title, ha="left", va="center", backing=False, fs=FS_LABEL, fontweight="bold")
        sa, sb = naca4(a, n=201), naca4(b, n=201)
        ax.add_patch(Polygon(sa["outline"], closed=True, fc="none", ec=INK, lw=1.3, ls=(0, (4.0, 2.5)), zorder=3))
        ax.add_patch(Polygon(sb["outline"], closed=True, fc="none", ec=INK, lw=LW_MAIN, zorder=4))
        ax.plot([0, 1], [0, 0], **line_kw("boundary"), zorder=3.2)
        for s_ in (sa, sb):
            if s_["m"] > 0:
                ax.plot(s_["x"], s_["yc"], zorder=3.5, **camber_kw)
                k = int(np.argmax(s_["yc"]))
                ax.plot(s_["x"][k], s_["yc"][k], "o", ms=4.0, color=INK, zorder=6)
        # direct labels: the solid section from above, the dashed one from below
        xb, xa = 0.86, 0.93
        callout(ax, (xb, _surface_at(sb, xb, True)), _naca_name(b, bold), at=(1.04, 0.135), ha="left", gap=1.5)
        callout(ax, (xa, _surface_at(sa, xa, False)), _naca_name(a, bold), at=(1.04, -0.12), ha="left", gap=1.5)
        if i == 0:
            xc = 0.68
            callout(ax, (xc, float(np.interp(xc, sb["x"], sb["yc"]))), "mean camber line", at=(0.55, 0.19), ha="left",
                    gap=1.5, fs=FS_SMALL)
            k = int(np.argmax(sb["yc"]))
            callout(ax, (sb["x"][k], sb["yc"][k]), "highest point of\nthe camber line", at=(0.10, 0.198),
                    ha="center", gap=3.0, fs=FS_SMALL)
        if i == 1:                                         # the two peaks of the camber line, named
            for s_, at in ((sa, (0.06, 0.20)), (sb, (0.62, 0.20))):
                k = int(np.argmax(s_["yc"]))
                callout(ax, (s_["x"][k], s_["yc"][k]), f"peak at {fmt(100 * s_['p'], 2)}%\nof the chord", at=at,
                        ha="center", gap=3.0, fs=FS_SMALL)
        da, db = naca4_decode(a), naca4_decode(b)
        changed = [j for j in range(4) if a[j] != b[j]]
        # the bold digits change; a symmetric section (00XX) also has the placeholder 0 for P
        assert all(a[j] != b[j] for j in bold) and da != db, "the bold digits are the ones that change"
        assert set(changed) - set(bold) <= ({1} if "0" in (a[0], b[0]) else set()), (a, b)
    save_figure(fig, "p13-naca-digits")


# ===================================================================== 9. worked example 2: root and tip sections
def naca_example_figure():
    """Lesson: the digits give fractions of the chord; the lengths follow from the chord, so the
    tip section is both smaller and relatively thinner. Third row: the two sections scaled to one
    chord, the thicknesses dimensioned as fractions of the chord."""
    ex = naca_values()
    r, t = ex["root"], ex["tip"]
    fig, ax = canvas(6.5, xlim=(-6.6, 23.6), ylim=(-16.6, 6.6))
    y_root, y_tip, y_cmp = 2.4, -5.9, -13.4
    fs = FS_SMALL
    sr = naca4(r["code"], n=201, chord=r["c"])
    st = naca4(t["code"], n=201, chord=t["c"])
    draw_section(ax, sr, origin=(0.0, y_root))
    draw_section(ax, st, origin=(0.0, y_tip), lw=1.0, chord_line=False, camber_line=False)   # too thin for more
    for sec, y0 in ((sr, y_root), (st, y_tip)):
        k = int(np.argmax(sec["yc"]))
        ax.plot(sec["x"][k], y0 + sec["yc"][k], "o", ms=3.5, color=INK, zorder=8)
    text(ax, (-0.5, y_root), f"root:\nNACA {r['code']}", direction=180.0, dist=4.0, fs=FS_LABEL)
    text(ax, (-0.5, y_tip - 0.3), f"tip: NACA {t['code']},\nchord {fmt(t['c'])} ft", direction=180.0, dist=4.0,
         fs=FS_LABEL)
    lead = pt(ax, 10.0)
    # root: thickness, camber and where it is, chord
    xr = 0.3 * r["c"]
    dimension_outside(ax, (xr, y_root + _surface_at(sr, xr, False)), (xr, y_root + _surface_at(sr, xr, True)), None,
                      lead=10.0)
    text(ax, (xr, y_root + _surface_at(sr, xr, True) + lead), f"maximum thickness {fmt(r['t_len'])} ft", direction=35.0,
         dist=4.0, fs=fs)
    callout(ax, (r["p_len"], y_root + r["m_len"]), f"maximum camber {fmt(r['m_len'])} ft", at=(-6.4, y_root + 3.2),
            ha="left", gap=3.0, fs=fs)
    yd = y_root - 1.85
    dimension(ax, (0.0, yd), (r["p_len"], yd), None, offset=0.0, extension=False)
    ax.plot([r["p_len"], r["p_len"]], [yd - 0.2, y_root + r["m_len"] - 0.35], color=INK, lw=0.7, zorder=2)
    text(ax, (0.5 * r["p_len"], yd), f"{fmt(r['p_len'])} ft", direction=-90.0, dist=6.0, fs=fs)
    dimension(ax, (0.0, yd - 2.3), (r["c"], yd - 2.3), f"root chord, {fmt(r['c'])} ft", label_side=-1, extension=False)
    # tip, at the same scale
    xt_ = 0.3 * t["c"]
    dimension_outside(ax, (xt_, y_tip + _surface_at(st, xt_, False)), (xt_, y_tip + _surface_at(st, xt_, True)), None,
                      lead=10.0)
    text(ax, (xt_, y_tip + _surface_at(st, xt_, False) - lead), f"maximum thickness {fmt(t['t_len'])} ft",
         direction=-35.0, dist=4.0, fs=fs)
    kt = int(np.argmax(st["yc"]))
    callout(ax, (st["x"][kt], y_tip + st["yc"][kt]), f"maximum camber {fmt(t['m_len'])} ft,\n{fmt(t['p_len'])} ft from "
            f"the leading edge", at=(-6.4, y_tip + 1.95), ha="left", gap=2.5, fs=fs)
    # the two at one chord: relatively thinner
    text(ax, (-6.4, y_cmp + 4.4), "the two airfoils drawn to the same chord", ha="left", va="center", backing=False,
         fs=FS_LABEL, fontweight="bold")
    C = r["c"]
    sa, sb = naca4(r["code"], n=201, chord=C), naca4(t["code"], n=201, chord=C)
    ax.add_patch(Polygon(sa["outline"] + np.array([0.0, y_cmp]), closed=True, fc="none", ec=INK, lw=LW_MAIN, zorder=4))
    ax.add_patch(Polygon(sb["outline"] + np.array([0.0, y_cmp]), closed=True, fc="none", ec=INK, lw=1.3,
                         ls=(0, (4.0, 2.5)), zorder=3))
    xc = 0.3 * C
    xa_, xb_ = xc - 0.9, xc + 0.9
    dimension_outside(ax, (xa_, y_cmp + _surface_at(sa, xa_, False)), (xa_, y_cmp + _surface_at(sa, xa_, True)), None,
                      lead=10.0)
    text(ax, (xa_, y_cmp + _surface_at(sa, xa_, True) + lead), f"NACA {r['code']}, solid: {fmt(100 * r['t'], 2)}% of the chord",
         direction=35.0, dist=4.0, fs=fs)
    dimension_outside(ax, (xb_, y_cmp + _surface_at(sb, xb_, False)), (xb_, y_cmp + _surface_at(sb, xb_, True)), None,
                      lead=6.0)
    callout(ax, (xb_ + 0.15, y_cmp + 0.5 * (_surface_at(sb, xb_, False) + _surface_at(sb, xb_, True))),
            f"NACA {t['code']}, dashed: {fmt(100 * t['t'], 1)}% of the chord", at=(10.5, y_cmp - 2.5), ha="left", gap=2.0,
            fs=fs)
    close_to(float(sr["yc"].max()), r["m_len"], 1e-3, "root camber drawn")
    close_to(float(st["yc"].max()), t["m_len"], 1e-3, "tip camber drawn")
    close_to(float(np.ptp(st["outline"][:, 0])), t["c"], 0.01, "tip chord drawn at the common scale")
    assert t["t"] < r["t"] and t["c"] < r["c"], "the tip is both smaller and relatively thinner"
    save_figure(fig, "p13-naca-example")


# ===================================================================== 9b. the high-lift surfaces in section
HIGH_LIFT_AIRFOIL = "2412"       # a schematic wing section (a choice; airliner sections differ in detail)


def _bezier(p0, p1, p2, n=30):
    t = np.linspace(0.0, 1.0, n)[:, None]
    return (1 - t) ** 2 * np.asarray(p0) + 2 * (1 - t) * t * np.asarray(p1) + t ** 2 * np.asarray(p2)


def high_lift_pieces(code=HIGH_LIFT_AIRFOIL, xs_u=0.15, xs_l=0.06, xsp=0.56, xf_u=0.76, xf_l=0.70, t_sp=0.013):
    """A wing section (NACA four-digit, chord 1) cut into its pieces: the slat (the leading edge,
    ahead of a curve from xs_u on the upper surface to xs_l on the lower one), the flap (behind a
    rounded nose from xf_l on the lower surface to xf_u on the upper one), the spoiler (a thin
    panel on the upper surface from xsp to xf_u, t_sp thick) and the main wing between them.
    Returns a dict of closed outlines and the spoiler hinge."""
    sec = naca4(code, n=301)
    xu, yu, xl, yl = sec["xu"], sec["yu"], sec["xl"], sec["yl"]
    U = lambda x: float(np.interp(x, xu, yu))              # noqa: E731
    Lw = lambda x: float(np.interp(x, xl, yl))             # noqa: E731
    Us, Ls = (xs_u, U(xs_u)), (xs_l, Lw(xs_l))
    slat_cut = _bezier(Us, (0.03, 0.5 * (U(0.05) + Lw(0.05))), Ls)             # from the upper to the lower surface
    up_s = xu <= xs_u
    lo_s = xl <= xs_l
    slat = np.r_[np.c_[xu[up_s][::-1], yu[up_s][::-1]], np.c_[xl[lo_s][1:], yl[lo_s][1:]], slat_cut[::-1][1:-1]]
    Uf, Lf = (xf_u, U(xf_u)), (xf_l, Lw(xf_l))
    flap_nose = _bezier(Lf, (xf_l - 0.07, 0.5 * (U(xf_l) + Lw(xf_l))), Uf)       # from the lower to the upper surface
    up_f = xu >= xf_u
    lo_f = xl >= xf_l
    flap = np.r_[flap_nose, np.c_[xu[up_f], yu[up_f]], np.c_[xl[lo_f][::-1], yl[lo_f][::-1]]]
    xsp_line = np.linspace(xsp, xf_u, 30)
    spoiler = np.r_[np.c_[xsp_line, [U(x) for x in xsp_line]], np.c_[xsp_line[::-1], [U(x) - t_sp for x in xsp_line[::-1]]]]
    up_m = (xu >= xs_u) & (xu <= xsp)
    lo_m = (xl >= xs_l) & (xl <= xf_l)
    cove = flap_nose[flap_nose[:, 1] <= U(xf_u) - t_sp]          # the main wing's cove: the flap nose below the spoiler
    main = np.r_[slat_cut, np.c_[xl[lo_m], yl[lo_m]], cove, np.c_[xsp_line[::-1], [U(x) - t_sp for x in xsp_line[::-1]]],
                 np.c_[xu[up_m][::-1], yu[up_m][::-1]]]
    return dict(slat=slat, flap=flap, spoiler=spoiler, main=main, hinge=np.array([xsp, U(xsp) - 0.5 * t_sp]),
                flap_hinge=np.array([xf_l + 0.02, Lw(xf_l) - 0.06]), slat_tip=np.array([0.0, 0.0]))


def high_lift():
    """Lesson: extended, the slat moves forward and down and the flap back and down, each opening
    a slot, so the section is longer and more curved; a raised spoiler breaks up the flow over the
    top. One section, drawn clean and extended, at one scale."""
    pc = high_lift_pieces()
    fig, ax = canvas(6.5, xlim=(-0.42, 1.52), ylim=(-0.80, 0.27))
    y_clean, y_ext = 0.02, -0.50
    fs = FS_SMALL
    st = dict(fc=PART_FILL, ec=INK, lw=LW_OUTLINE, joinstyle="round")
    sv = dict(fc=SURFACE_FILL, ec=INK, lw=LW_DETAIL, joinstyle="round", hatch=HATCH_SURFACE)
    def put(xy, dy, kw, z=3):
        pa = ax.add_patch(Polygon(np.asarray(xy) + np.array([0.0, dy]), closed=True, zorder=z, **{k: v for k, v in kw.items()
                                                                                                   if k != "hatch"}))
        if kw.get("hatch"):
            pa.set_hatch(kw["hatch"])
        return opaque(pa)
    # clean: the pieces in place
    put(pc["main"], y_clean, st)
    for k in ("slat", "flap", "spoiler"):
        put(pc[k], y_clean, sv, z=3.5)
    text(ax, (-0.40, y_clean + 0.17), "clean (cruise)", ha="left", va="center", backing=False, fs=FS_LABEL,
         fontweight="bold")
    # extended: slat forward and down, flap back and down, spoiler raised
    # slat: nose down 20 degrees about its rear upper corner, then forward and down, which opens the slot
    su = pc["slat"][np.argmax(pc["slat"][:, 0])]
    slat = rotate_xy(pc["slat"], -20.0, about=tuple(su)) + np.array([-0.085, -0.018])
    # flap: down 30 degrees about its nose, its nose moved back to just under the main wing's trailing edge
    fn = pc["flap"][np.argmin(pc["flap"][:, 0])]
    te_main = pc["main"][np.argmax(pc["main"][:, 0])]
    flap = rotate_xy(pc["flap"], -30.0, about=tuple(fn)) - fn + np.array([te_main[0] - 0.005, te_main[1] - 0.07])
    spoiler = rotate_xy(pc["spoiler"], 38.0, about=tuple(pc["hinge"]))
    put(pc["main"], y_ext, st)
    put(slat, y_ext, sv, z=3.5)
    put(flap, y_ext, sv, z=3.5)
    put(spoiler, y_ext, sv, z=3.6)
    text(ax, (-0.40, y_ext + 0.25), "after touchdown: slat and flap extended, spoiler raised", ha="left", va="center",
         backing=False, fs=FS_LABEL, fontweight="bold")
    def name(xy, s_, at, ha):                                  # a leader that ends in a dot, as on the other drawings
        callout(ax, tuple(xy), s_, at=at, ha=ha, gap=2.0, fs=fs)
        ax.plot(*xy, "o", ms=2.6, color=INK, zorder=11)
    # names, clean
    name((0.035, y_clean + 0.0), "slat", (-0.20, y_clean - 0.10), "right")
    name((0.40, y_clean + 0.02), "main wing", (0.36, y_clean - 0.14), "center")
    name((0.66, y_clean + float(pc["spoiler"][:, 1].mean())), "spoiler", (0.66, y_clean + 0.15), "center")
    name((0.88, y_clean + 0.005), "flap", (1.08, y_clean + 0.08), "left")
    # names, extended
    name(slat.mean(axis=0) + np.array([0.0, y_ext]), "slat: forward\nand down", (-0.27, y_ext - 0.14), "center")
    name(spoiler.mean(axis=0) + np.array([0.0, y_ext]), "spoiler: raised", (0.95, y_ext + 0.15), "left")
    name(flap.mean(axis=0) + np.array([0.0, y_ext]), "flap: back and down", (1.12, y_ext - 0.10), "left")
    gs = np.array([0.038, -0.052 + y_ext])                     # the slot behind the slat
    gf = np.array([0.728, -0.062 + y_ext])                       # the slot ahead of the flap
    name(gs, "slot", (0.10, y_ext - 0.20), "left")
    name(gf, "slot", (0.62, y_ext - 0.22), "center")
    # the air through each slot: from under the wing, out over the upper surface of the piece behind it
    dy = np.array([0.0, y_ext])
    air_slat = np.r_[_bezier((-0.03, -0.10), (0.005, -0.02), (0.068, 0.034)),
                     _bezier((0.068, 0.034), (0.095, 0.08), (0.24, 0.12))[1:]] + dy
    air_flap = np.r_[_bezier((0.69, -0.10), (0.715, -0.03), (0.77, -0.005)),
                     _bezier((0.77, -0.005), (0.84, -0.01), (0.93, -0.04))[1:]] + dy
    for path in (air_slat, air_flap):
        ln = ax.plot(path[:, 0], path[:, 1], color=INK, lw=1.0, zorder=4)[0]
        motion_heads(ax, path[:, 0], path[:, 1], (0.93,), line=ln, zorder=4.5)
    text(ax, tuple(air_slat[0]), "air", direction=200.0, dist=3.0, fs=fs)
    # asserts: the extended section is longer than the clean one; each piece leaves a gap to the main wing
    clean_len = 1.0
    ext_len = float(flap[:, 0].max() - slat[:, 0].min())
    assert ext_len > clean_len + 0.08, "slat and flap extended make the section longer"
    assert float(flap[:, 1].min()) < float(pc["flap"][:, 1].min()) - 0.05, "the flap goes down"
    assert float(spoiler[:, 1].max()) > float(pc["spoiler"][:, 1].max()) + 0.05, "the spoiler rises"
    from figkit import _min_dist
    assert _min_dist(slat, pc["main"]).min() > 0.004 and _min_dist(flap, pc["main"]).min() > 0.004, "open slots"
    from matplotlib.path import Path as _P
    for path in (air_slat, air_flap):                          # the air passes through the slots, not through a piece
        for piece in (slat, flap, pc["main"], spoiler):
            assert not _P(piece + dy).contains_points(path).any(), "air path clear of the pieces"
        assert path[0, 1] < y_ext + float(pc["main"][:, 1].min()) - 0.04 and path[-1, 1] > path[0, 1], "under, then over"
    save_figure(fig, "p13-high-lift")


# ===================================================================== 10. the heavy launcher, outside
def launcher_parts():
    """Lesson: the stack is built in order of use: boosters and core stage at liftoff, the upper
    stage ahead of them, the payload at the nose under its fairing. Braces under the vehicle give
    the extent of each stage."""
    parts = launch_vehicle(payload=None, orientation="horizontal")
    A = ARIANE5
    x0, x1, y0, y1 = extent(parts)
    fig, ax = canvas(6.5, xlim=(x0 - 11.5, x1 + 1.5), ylim=(y0 - 5.6, y1 + 4.6))
    P = draw_parts(ax, parts)
    z_c0 = float(parts["core_stage"].xy[:, 0].min())
    z_c1 = float(parts["core_stage"].xy[:, 0].max())
    z_f0 = float(parts["fairing"].xy[:, 0].min())
    yb = y0 - 1.2
    for (a_, b_, name) in ((z_c0, z_c1, "core stage"), (z_c1, z_f0, "upper stage"), (z_f0, x1, "payload fairing")):
        brace(ax, (b_ - 0.15, yb), (a_ + 0.15, yb), name, side=1, depth=6.0, fs=FS_LABEL)
    sf = parts["strut_fwd_left"]
    xf = float(sf.inside[0])
    name_parts(ax, P, parts, {
        "booster_left": ("solid rocket booster", (15.0, y1 + 2.6), dict(ha="center")),
        "core_engine": ("main engine", (-4.5, 0.0), dict(ha="right", target=(1.1, 0.0))),
        "booster_right_nozzle": ("booster nozzle", (-4.5, y0 + 1.0), dict(ha="right")),
    })
    # the forward attachment is small: its leader ends on the beam's forward face, with no dot to hide it,
    # and climbs under the booster's nose cone (12 degrees) to its name
    face = float(sf.xy[:, 0].max())
    callout(ax, (face - 0.05, float(sf.inside[1])), "forward attachment", at=(33.5, 4.25), ha="left", gap=1.5)
    up_at_liftoff(ax, (x0 - 11.0, y1 + 2.6), 5.0)
    x_up = parts["upper_stage"].xy[:, 0]
    assert x_up.min() > parts["core_stage"].xy[:, 0].max() - 1e-9, "upper stage ahead of the core stage"
    for tag in ("left", "right"):                             # each attachment reaches from the core to its booster
        st, bo = parts[f"strut_fwd_{tag}"].xy, parts[f"booster_{tag}"].xy
        yy = np.abs(st[:, 1])
        assert yy.min() < 0.5 * A["core_d"] and yy.max() > 0.5 * A["core_d"] + A["eap_gap"], tag
    save_figure(fig, "p13-launcher-parts")


# ===================================================================== 11. the heavy launcher, cut open
def disc_leader(ax, target, n, at, gap_pt=7.5):
    """A numbered disc (diagrams.key_disc, the chapter's one disc style) at `at` with a thin leader
    to `target`, ending in a dot. Example: disc_leader(ax, (20.0, 0.0), 4, (17.0, 1.3))"""
    at, target = np.asarray(at, float), np.asarray(target, float)
    d = target - at
    r = pt(ax, gap_pt)
    start = at + d / np.hypot(*d) * r
    ax.plot([start[0], target[0]], [start[1], target[1]], color=INK, lw=0.7, zorder=29, gid=f"grp:disc{n}")
    ax.plot(*target, "o", ms=2.6, color=INK, zorder=29.5, gid=f"grp:disc{n}")
    c = key_disc(ax, tuple(at), n)
    c.set_gid(f"grp:disc{n}")
    return c


def launcher_cutaway():
    """Lesson: most of a launch vehicle is propellant; each liquid stage carries its own fuel and
    oxidizer in separate tanks, each solid booster a solid grain, and the upper stage packs its
    tanks and engine into a few meters. Numbers run from the tail to the nose."""
    parts = launch_vehicle(cutaway=True, orientation="horizontal")
    x0, x1, y0, y1 = extent(parts)
    fig, ax = canvas(6.5, xlim=(x0 - 1.0, 64.5), ylim=(-42.2, y1 + 8.0))
    P = draw_cutaway(ax, parts)
    U = ARIANE5["upper"]
    text(ax, (x0 - 0.8, y1 + 6.4), "whole vehicle", ha="left", va="center", backing=False, fs=FS_LABEL, fontweight="bold")
    up_at_liftoff(ax, (34.0, y1 + 3.6), 5.0)
    # main view: numbered discs from the tail to the nose, one style, names in the key
    lox, lh2 = parts["lox_tank"], parts["lh2_tank"]
    bt = parts["booster_left"]                               # the upper booster in this view
    yb = float(bt.inside[1])
    zb = float(lox.xy[:, 0].min())                          # apex of the common bulkhead (it bulges into the hydrogen)
    ch = parts["booster_channel_left"].xy
    discs = [(1, (5.5, yb + 0.9), (5.5, y1 + 2.6)),        # the solid grain
             (2, (11.0, yb), (11.0, y1 + 2.6)),              # its central channel
             (3, None, (11.5, 0.0)),                         # liquid hydrogen
             (4, (zb + 0.05, 0.0), (16.8, 1.2)),             # the common bulkhead
             (5, None, (float(lox.xy[:, 0].mean()) + 0.8, 0.0)),
             (6, None, tuple(parts["payload"].inside))]
    for n, tgt, at in discs:
        if tgt is None:
            key_disc(ax, at, n)
        else:
            disc_leader(ax, tgt, n, at)
    xs_ = [d[2][0] for d in discs]
    assert all(a_ < b_ for a_, b_ in zip(xs_[:-1], xs_[1:])), "the numbers run from the tail to the nose"
    assert float(ch[:, 1].min()) < yb < float(ch[:, 1].max()), "disc 2 points into the channel"
    key = ["solid propellant (the grain)", "central channel", "liquid hydrogen (core stage)", "common bulkhead",
           "liquid oxygen (core stage)", "payload"]
    for n, s_ in enumerate(key, start=1):
        y = -11.0 - 3.1 * (n - 1)
        key_disc(ax, (1.2, y), n)
        text(ax, (1.2, y), s_, direction=0.0, dist=11.0, fs=FS_LABEL)
    # the enlarged upper part
    region = (29.9, 39.0, -3.05, 3.05)
    k = 2.7
    cx = 33.0 + 0.5 * k * (region[1] - region[0])
    fills, M, R = draw_enlarged(ax, parts, region, k, (cx, -21.3))
    text(ax, (0.5 * (R[0] + R[1]), R[2] - 10.3), f"upper part, enlarged {fmt(k, 2)} times", ha="center", va="center",
         backing=False, fs=FS_LABEL, fontweight="bold")
    frame_main = ax.add_patch(Rectangle((region[0], region[2]), region[1] - region[0], region[3] - region[2], fc="none",
                                        ec=GRAY, lw=LW_THIN, zorder=40))
    frame_in = ax.add_patch(Rectangle((R[0], R[2]), R[1] - R[0], R[3] - R[2], fc="none", ec=GRAY, lw=LW_THIN, zorder=40))
    for a_, b_ in (((region[0], region[2]), (R[0], R[3])), ((region[1], region[2]), (R[1], R[3]))):
        connects(ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=GRAY, lw=LW_THIN, zorder=1.5)[0], frame_main, frame_in)
    zu0 = ARIANE5["core_len"] + ARIANE5["iss_len"]
    eng = parts["upper_engine"].xy
    lab = [  # (text, target in the main view, label position in the figure, ha); leaders above the inset's fills
        ("liquid hydrogen tank", (zu0 + U["lh2_z1"] - 0.25, 1.9), (43.3, R[3] + 1.6), "center"),
        ("upper-stage\nengine", (float(eng[:, 0].min()) + 0.3, 0.2), (R[0] - 0.8, M((0, 0.2))[1]), "right"),
        ("interstage", (zu0 - 0.75, -2.2), (32.5, R[2] - 4.2), "center"),
        ("liquid\noxygen\ntank", (zu0 + U["lox_center"] + 0.25, -0.45), (43.0, R[2] - 5.0), "center"),
        ("equipment\nbay", (36.3, -2.0), (50.5, R[2] - 4.2), "center"),
        ("payload\nadapter", (37.4, -1.1), (59.2, R[2] - 4.2), "center"),
    ]
    for s_, tgt, at, ha in lab:
        T = M(tgt)
        callout(ax, T, s_, at=at, ha=ha, gap=2.0, zorder=44)
        ax.plot(*T, "o", ms=2.6, color=INK, zorder=45)
    # asserts: the enlarged view keeps the proportions; the upper engine sits behind (aft of) its tanks
    close_to((R[1] - R[0]) / (region[1] - region[0]), k, 1e-9, "enlargement")
    assert eng[:, 0].max() < parts["lox_tank_upper"].xy[:, 0].min(), "engine aft of the oxygen tank"
    assert parts["lox_tank"].xy[:, 0].min() < parts["lh2_tank"].xy[:, 0].max(), "common bulkhead bulges into the hydrogen"
    close_to(float(parts["adapter"].xy[:, 0].min()), float(parts["equipment_bay"].xy[:, 0].max()), 1e-9,
             "the adapter sits on the equipment bay")
    save_figure(fig, "p13-launcher-cutaway")


# ===================================================================== 12. the two-stage launcher in two pieces
FIRST_STAGE_PARTS = ("first_stage", "interstage", "stage1_joint", "rp1_tank_1", "lox_tank_1", "transfer_tube")


def _moved(parts, dx, dy):
    """place() that keeps each part's propellant and hatch."""
    from chapter_1.aircraft import place
    out = place(parts, dx, dy)
    for k in out:
        for attr in ("contents", "hatch"):
            if hasattr(parts[k], attr):
                setattr(out[k], attr, getattr(parts[k], attr))
    return out


def up_at_liftoff(ax, xy, length):
    """A small arrow along the vehicle axis, toward the nose, named "up at liftoff": the launch
    vehicles of the page lie nose to the right. Example: up_at_liftoff(ax, (40.0, 10.0), 6.0)"""
    x, y = xy
    arrow(ax, (x, y), (x + length, y), color=INK, lw=1.2, head="normal", zorder=6)
    text(ax, (x + length, y), "up at liftoff", direction=0.0, dist=4.0, fs=FS_SMALL)


def separation_mark(ax, x, y0, r, extra, label=None, side=1):
    """Two short dashed ticks across the axis at x, just outside a stage of radius r centered on
    y0, marking the plane where the stages separate; the label at the tick on the side `side`."""
    for s_ in (1, -1):
        ax.plot([x, x], [y0 + s_ * (r + 0.25), y0 + s_ * (r + extra)], color=INK, lw=1.0, ls=(0, (3.0, 2.0)), zorder=4)
    if label:
        text(ax, (x, y0 + side * (r + extra)), label, direction=90.0 * side, dist=3.0, fs=FS_SMALL)


def two_stage():
    """Lesson: a two-stage kerosene launch vehicle in section, cut where the stages separate: the
    first stage keeps its interstage, with the grid fins and the landing legs it needs to return;
    the second stage leaves with its vacuum engine and the payload under the fairing."""
    parts = two_stage_vehicle(cutaway=True, legs=True, grid_fins=True, orientation="horizontal")
    F = FALCON9
    z2 = F["stage1_len"] + F["interstage_len"]                  # the separation plane: top of the interstage
    lower = {k: v for k, v in parts.items() if k in FIRST_STAGE_PARTS or k.startswith(("engine_", "landing_leg",
                                                                                        "grid_fin"))}
    upper = {k: v for k, v in parts.items() if k not in lower}
    dx_up, dy_up = 61.0 - F["height"], 13.6                  # the upper piece drawn above, its nose at the right margin
    lo_s, up_s = lower, _moved(upper, dx_up, dy_up)
    R = 0.5 * F["d"]
    fig, ax = canvas(6.5, xlim=(-1.0, 62.0), ylim=(-8.2, 23.4))
    Pl = draw_cutaway(ax, lo_s)
    Pu = draw_cutaway(ax, up_s)
    text(ax, (-0.8, 22.4), "second stage and payload fairing, at the same scale", ha="left", va="center", backing=False, fs=FS_LABEL,
         fontweight="bold")
    text(ax, (-0.8, 7.9), "first stage with its interstage", ha="left", va="center", backing=False,
         fs=FS_LABEL, fontweight="bold")
    xs_up = z2 + dx_up
    separation_mark(ax, z2, 0.0, R + 0.35, 1.9)
    text(ax, (z2 + 0.6, 0.0), "stages\nseparate here", direction=0.0, dist=3.0, fs=FS_SMALL)
    separation_mark(ax, xs_up, dy_up, R, 2.0, "stages\nseparate here", side=1)
    up_at_liftoff(ax, (0.5, dy_up), 6.0)
    zm = float(lo_s["lox_tank_1"].xy[:, 0].min())               # the common bulkhead, drawn straight
    fs = FS_SMALL
    yt, yb = 4.6, -5.7
    name_parts(ax, Pl, lo_s, {
        "engine_1": ("nine engines\n(three seen)", (-0.8, yb), dict(ha="left", target=(0.55, float(lo_s["engine_1"].inside[1])))),
        "landing_leg_left": ("landing leg\n(folded)", (1.5, yt), dict(ha="left")),
        "rp1_tank_1": ("kerosene\n(RP-1)", (15.5, yt), dict(ha="center", target=(15.0, 1.0))),
        "transfer_tube": ("oxygen\ntransfer tube", (13.5, yb), dict(ha="center", target=(12.5, 0.0))),
        "lox_tank_1": ("liquid\noxygen", (31.0, yb), dict(ha="center", target=(31.0, -0.9))),
        "interstage": ("interstage", (38.5, yt), dict(ha="center", target=(44.0, R - 0.5 * F["wall"]))),
        "grid_fin_right": ("grid fin", (45.6, yb), dict(ha="center")),
    }, fs=fs)
    callout(ax, (zm, -1.0), "common dome\n(drawn flat)", at=(23.2, yb), ha="center", gap=1.5, fs=fs)
    ax.plot(zm, -1.0, "o", ms=2.6, color=INK, zorder=12)
    ytu, ybu = dy_up + 5.4, dy_up - 5.4
    name_parts(ax, Pu, up_s, {
        "vacuum_engine": ("vacuum\nengine", (36.3, ybu), dict(ha="right", target=(xs_up - 2.2, dy_up + 0.6))),
        "rp1_tank_2": ("kerosene\n(RP-1)", (42.0, ybu), dict(ha="center")),
        "lox_tank_2": ("liquid\noxygen", (47.5, ytu), dict(ha="center")),
        "payload": ("payload", (54.0, ytu), dict(ha="center")),
        "fairing": ("payload fairing", (54.5, ybu), dict(ha="center", target=(up_s["fairing"].xy[:, 0].max() - 2.5,
                                                                              dy_up - 0.9))),
    }, fs=fs)
    # asserts: the pieces are those that separate; the drawing keeps the published size
    gf = lo_s["grid_fin_right"].xy[:, 0]
    assert F["stage1_len"] < gf.min() and gf.max() < z2, "grid fins on the interstage, with the first stage"
    close_to(float(lo_s["interstage"].xy[:, 0].max()), z2, 1e-9, "the lower piece ends at the separation plane")
    close_to(float(up_s["second_stage"].xy[:, 0].min()) - dx_up, z2, 1e-9, "the upper piece starts there")
    close_to(float(up_s["fairing"].xy[:, 0].max()) - dx_up, F["height"], 1e-6, "height")
    close_to(float(np.ptp(lo_s["first_stage"].xy[:, 1])), F["d"], 1e-9, "diameter")
    assert float(up_s["vacuum_engine"].xy[:, 0].min()) - dx_up < z2, "the vacuum engine sat inside the interstage"
    assert lo_s["lox_tank_1"].xy[:, 0].min() > lo_s["rp1_tank_1"].xy[:, 0].min(), "oxygen ahead of the kerosene"
    save_figure(fig, "p13-two-stage")


# ===================================================================== 13. mission profiles
# Each profile: segments (name, horizontal length, altitude at its end, where along the segment
# its name sits), then the direction (deg) of each segment-end number from its point, and an
# optional weight drop (point index, what leaves, side of the words). Schematic units: neither
# distance nor altitude is to scale. Segment ends are numbered from 0 at the start of the
# takeoff, as in Raymer's sizing profiles; takeoff and landing lie on the ground line.
PROFILES = [
    ("airliner (Airbus A320 class): one flight",
     [("takeoff", 0.8, 0.0, 0.5), ("climb", 1.6, 1.0, 0.4), ("cruise", 4.6, 1.0, 0.5),
      ("descent", 1.6, 0.0, 0.45), ("landing", 0.9, 0.0, 0.5)],
     [90, 120, -45, -135, 60, 90], None),
    ("business jet (Phenom 100 class): two legs without refueling",
     [("takeoff", 0.75, 0.0, 0.5), ("climb", 0.7, 0.85, 0.4), ("cruise", 1.0, 0.85, 0.5),
      ("descent", 0.7, 0.0, 0.3), ("landing", 1.2, 0.0, 0.42), ("takeoff", 1.2, 0.0, 0.58),
      ("climb", 0.7, 0.85, 0.4), ("cruise", 1.0, 0.85, 0.5), ("descent", 0.55, 0.5, 0.45),
      ("loiter (hold)", 1.45, 0.5, 0.5, -90.0), ("descent", 1.15, 0.0, 0.35), ("landing", 0.85, 0.0, 0.5)],
     [90, 120, -45, -135, 60, 90, 120, -45, -135, -135, 75, 60, 90], (5, "passengers get off", -90.0)),
    ("skydiving aircraft (Twin Otter class): up, the jump, and down",
     [("takeoff", 0.9, 0.0, 0.5), ("climb", 2.6, 1.0, 0.4), ("jump run", 1.6, 1.0, 0.5),
      ("descent", 2.4, 0.0, 0.45), ("landing", 1.1, 0.0, 0.5)],
     [90, 120, 45, 45, 60, 90], (3, "skydivers jump", 180.0)),
]


def mission_profiles():
    """Lesson: a mission profile is the mission cut into segments, drawn in order as altitude
    against distance, with the end of each segment numbered; the segments differ by mission."""
    n = len(PROFILES)
    fig, axs = new_axes(6.5, 6.3, nrows=n, equal=False, gridspec_kw=dict(height_ratios=[2.55, 2.75, 2.25]))
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, hspace=0.06)
    counts = []
    for i, (ax, (title, segs, ndir, drop)) in enumerate(zip(axs, PROFILES)):
        L = sum(sg[1] for sg in segs)
        gr = (-0.40, 1.2 if i == 0 else 0.25)
        ax.set_xlim(-0.55, L + gr[1] + 0.05)
        ax.set_ylim((-0.62, -0.78, -0.30)[i], 1.55)
        fig.canvas.draw()
        xs, ys, ln = draw_mission_profile(ax, segs, ndir, drop, ground=gr, axes_names=(i == 0))
        text(ax, (-0.53, 1.47), title, ha="left", va="center", backing=False, fs=FS_LABEL, fontweight="bold")
        counts.append(len(segs))
        assert ys[0] == 0.0 and ys[-1] == 0.0, "the mission starts and ends on the ground"
        assert np.all(np.diff(xs) > 0) and len(ndir) == len(xs)
        for k, sg in enumerate(segs):                          # every descent ends lower than it starts
            if sg[0] == "descent":
                assert ys[k + 1] < ys[k], sg
    assert counts[1] > counts[0], "a second leg adds segments"
    assert counts[0] == 5, "the airliner flies five segments, points 0 to 5"
    save_figure(fig, "p13-mission-profiles")


# ===================================================================== drivers
def make_all():
    airframe_side()
    front_view()
    moving_surfaces()
    body_axes_three_view()
    control_deflection()
    gear_layouts()
    wing_planform()
    airfoil_parts()
    naca_digits()
    naca_example_figure()
    high_lift()
    launcher_parts()
    launcher_cutaway()
    two_stage()
    mission_profiles()


def values():
    """Every number the page prints, recorded with the text it is printed as."""
    r = lambda k, v: record(PG, k, v)                     # noqa: E731
    e = wing_example()
    w = B738_WING
    # published data of the worked example
    r("S-m2", fmt_dec(w["S_m2"], 2))
    r("b-m", fmt_dec(w["b_m"], 2))
    r("mac-m-pub", fmt_dec(w["mac_m"], 2))
    r("AR-pub", fmt_dec(w["AR"], 2))
    r("taper", fmt_dec(w["taper"], 3))
    r("sweep", fmt(w["sweep_c4"], 2))
    r("mtow", fmt(B738_MTOW_LB, 4))
    r("ft-m", fmt_dec(FT, 4))
    # step 1: units
    r("b-ft", fmt_dec(e["b"], 2))
    r("S-ft2", fmt_dec(e["S"], 1))
    r("ft2-m2", fmt_dec(FT * FT, 6))
    r("m2-ft2", fmt(1.0 / (FT * FT), 5))
    r("m-ft", fmt(1.0 / FT))
    # step 2: aspect ratio
    r("b2", fmt(e["b2"], 5))
    r("AR", fmt(e["AR"]))
    # step 3: chords
    r("two-S", fmt_dec(e["two_S"], 1))
    r("one-plus-lam", fmt_dec(1 + e["lam"], 3))
    r("b-1l", fmt(e["b_1l"], 5))
    r("cr", fmt(e["cr_p"]))
    r("ct", fmt(e["ct"]))
    # step 4: MAC and its station (station from b at full precision over 6, A1 #19)
    r("lam2", fmt(e["lam2"], 5))
    r("num", fmt(e["num"], 5))
    r("ratio", fmt(e["ratio"], 5))
    r("mac", fmt(e["mac"]))
    r("mac-pub-ft", fmt(e["mac_pub_ft"]))
    # the published chord against this result, from the printed digits (13.68 ft against 13.19 ft)
    r("mac-diff", fmt(100 * (round(e["mac_pub_ft"], 2) / round(e["mac"], 2) - 1.0), 2))
    r("ymac", fmt(e["ymac"]))
    r("b6", fmt(e["b6"], 6))
    r("ymac-ratio", fmt(e["yr"], 6))
    r("one-plus-2lam", fmt_dec(1 + 2 * e["lam"], 3))
    # step 5: wing loading
    r("WS", fmt(e["WS"]))
    # worked example 2: NACA sections at the root and tip chords
    nv = naca_values()
    for tag in ("root", "tip"):
        d = nv[tag]
        r(f"{tag}-c", fmt(d["c"]))
        r(f"{tag}-m", fmt(d["m_len"]))
        r(f"{tag}-p", fmt(d["p_len"]))
        r(f"{tag}-t", fmt(d["t_len"]))
    r("tip-t-in", fmt(nv["tip"]["t_len"] * 12.0, 3))
    r("root-t-in", fmt(nv["root"]["t_len"] * 12.0, 3))
    # vehicle facts printed in the text (published values of the shared modules)
    r("dihedral", fmt(B738["dihedral"], 1))
    A5 = ARIANE5
    r("a5-fairing-len", fmt(A5["fairing_len"], 2))
    r("a5-d", fmt(A5["core_d"], 2))
    r("a5-core-len", fmt(A5["core_len"], 2))
    r("a5-eap-len", fmt(A5["eap_len"], 3))
    r("a5-eap-d", fmt(A5["eap_d"], 3))
    r("a5-lox", fmt(A5["lox_volume"], 3))
    r("a5-lh2", fmt(A5["lh2_volume"], 3))
    r("f9-height", fmt(FALCON9["height"], 2))
    r("f9-d", fmt_dec(FALCON9["d"], 2))
    F_ = A5_FLIGHT
    r("a5-fairing-flux", fmt(F_["fairing_flux"], 4))
    r("a5-eap-share", fmt(F_["eap_thrust_share"], 2))
    r("a5-eap-sep-s", fmt(F_["eap_sep_s"], 3))
    r("a5-eap-sep-km", fmt(F_["eap_sep_km"], 2))
    r("a5-epc-min", fmt(F_["epc_burn_min"], 2))
    r("a5-epc-km", fmt(F_["epc_sep_km"], 3))
    r("a5-lox-t", fmt(F_["lox_t"], 3))
    r("a5-lh2-t", fmt(F_["lh2_t"], 2))
    r("a5-mass-ratio", fmt(F_["lox_t"] / F_["lh2_t"], 2))
    r("a5-epc-dry", fmt(F_["epc_dry_t"], 3))
    r("a5-epc-prop", fmt(F_["epc_prop_t"], 3))
