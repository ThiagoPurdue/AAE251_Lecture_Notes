"""A jet transport in side, plan and front view, as separate closed parts (chapter_1.geometry.Part)
that drawing.draw_parts() draws as line art: the Boeing 737-800 with winglets.

Coordinates in meters: x aft from the nose tip, z up from the ground, the airplane level. Each
view is drawn as an observer sees it, with the nose to the left in the side and plan views:
  - side view (x, z): the left side seen, nose to the left;
  - plan view (x, y_page): seen from ABOVE, nose to the left, so the RIGHT wing ("_R" parts) is
    toward the top of the page and the left wing ("_L") toward the bottom;
  - front view (y_page, z): seen from ahead, so the LEFT wing ("_L") is on the right of the page
    and the right wing ("_R") on the left.
VIEWS gives, for each view, the screen directions (right, up, toward the reader) of the body
axes x (forward), y (out the right wing) and z (down); the unit checks below test that they form
a right-handed set and that the drawn geometry agrees with them.

Sources (the published numbers are the keys of B738 marked "published"; each has a unit check):
  - Boeing, "737 Airplane Characteristics for Airport Planning", D6-58325-7 Rev C, 2025:
    2.2.6 General Dimensions, 737-800W (length 39.47 m, span with winglets 35.79 m, height
    12.55 m, fuselage width 3.76 m, nose to inlet 13.36 m, engine 4.83 m from the centerline,
    nose gear 4.09 m from the nose, wheelbase 15.60 m, main-gear track 5.72 m, tail span
    14.35 m, nose to tail-cone end 38.02 m, nose to wing-tip leading and trailing edge
    23.47 m and 24.99 m); 2.3.3 Ground Clearances, 737-800W at OEW (engine 0.64 m,
    entry doors 2.74 m and 3.12 m, wing tip with winglet 6.76 m, bottom of winglet 4.32 m,
    stabilizer 5.64 m); 2.5.1 Cabin Cross-Section (fuselage 3.76 m wide; its outer contour,
    measured on the scaled section, is 4.03 m tall); 7.2.1 tires (27 in nose, 44.5 in main).
    Shapes between those points (nose and tail-cone profile, sweep breaks, fin, nacelle,
    doors, flight-deck windows) are read off the scaled general-dimensions drawings.
  - Boeing news release, 18 February 2000, "New Winglets Boost Boeing Next-Generation 737
    Performance": the winglet is 8 ft long and tapers from a 4 ft base to 2 ft at the tip.
  - Control surfaces: Boeing 737 NG systems summary, Flight Controls (from the operations
    manual): four slats outboard and two leading-edge flaps inboard of each engine, double-
    slotted flaps inboard and outboard of each engine, six spoiler panels per wing (four
    flight, two ground), one aileron, two elevators, one rudder. Spans and chords of the
    surfaces are schematic: no public source gives them.

Height: the general-dimensions drawing draws the fuselage 3.95 m tall from 1.00 m to 4.95 m;
the clearance table gives a measured top of fuselage of 5.56 m at OEW, the entry-door sills at
2.74 m (front) and 3.12 m (aft), so the airplane sits about 0.8 deg nose down at OEW. The floor
of the section drawing is 1.52 m above the fuselage bottom, which puts the bottom at 1.22 m at
the front door and 1.60 m at the aft door. Drawn level, the fuselage bottom here is 1.40 m (the
middle) and the top 5.43 m; the tail height is the dimensioned 12.55 m.
"""
import math

import numpy as np

from chapter_1.geometry import Part, catmull_rom, circle_xy, fillet, hull, naca4, superellipse, _mirror

__all__ = ["B738", "B738_WING", "B738_MTOW_LB", "B738_SEATS_TWO_CLASS", "aircraft_side", "aircraft_top", "aircraft_front", "fuselage_section", "wing_box", "wing_z",
           "place", "three_view", "cg_point", "VIEWS", "rotation_sense", "winglet_cant"]

# ===================================================================== parameters
B738 = dict(
    length=39.47,            # m, published: overall length (to the tip of the horizontal tail)
    span=35.79,              # m, published: span with winglets (737-800W)
    span_wing=34.32,         # m, published: span without winglets (737-800); the wing tip here
    height=12.55,            # m, published: top of the fin above the ground
    fus_width=3.76,          # m, published
    fus_height=4.03,         # m, measured on the scaled cabin cross-section (2.5.1)
    fus_bottom=1.40,         # m, from the entry-door sills and the section floor (see the module text)
    tail_end=38.02,          # m, published: nose to the end of the tail cone
    nose_gear_x=4.09,        # m, published
    wheelbase=15.60,         # m, published
    track=5.72,              # m, published: main-gear track
    nose_tire=27 * 0.0254,   # m, published: 27 in tires
    main_tire=44.5 * 0.0254,  # m, published: 44.5 in tires
    engine_y=4.83,           # m, published: engine centerline from the fuselage centerline
    inlet_x=13.36,           # m, published: nose to the engine inlet
    engine_ground=0.64,      # m, published: engine above the ground (OEW)
    nacelle_dia=2.10,        # m, read off the drawings (front view about 2.2 wide, side about 2.0 tall)
    fan_cowl_end=16.55,      # m, read off the side view
    wing_root_le=14.90, wing_root_te=21.35,          # m, read off the plan view (at the fuselage side)
    wing_kink_y=5.65, wing_kink_le=17.40,            # m, read off the plan view
    wing_tip_le=23.47, wing_tip_te=24.99,            # m, published: nose to wing tip leading/trailing edge
    wing_root_z=2.62,        # m, chord line at the root: 1.22 m above the fuselage bottom (front view)
    dihedral=6.0,            # deg, from the bottom of the winglet, 4.32 m (published), and the root height
    winglet_height=8 * 0.3048, winglet_root_chord=4 * 0.3048, winglet_tip_chord=2 * 0.3048,   # published
    winglet_top_z=6.76,      # m, published: wing tip (top of the winglet) above the ground
    winglet_sweep_x=1.9,     # m, read off the side view: the winglet tip leading edge aft of its root
    ht_span=14.35,           # m, published
    ht_root_le=32.68, ht_root_te=37.10, ht_tip_le=37.90,   # m, read off the plan view
    ht_tip_z=5.64,           # m, published: stabilizer tip above the ground (OEW)
    ht_dihedral=7.0,         # deg, read off the front view
    vt_root_le=31.60, vt_dorsal_le=28.90, vt_tip_le=37.55, vt_tip_te=38.55, vt_root_te=36.95,  # m, side view
    cg_x=17.5,               # m, a center of gravity near the quarter chord of the mean chord (schematic)
)
B738["ht_tip_te"] = B738["length"]
B738["main_gear_x"] = B738["nose_gear_x"] + B738["wheelbase"]
B738["fus_top"] = B738["fus_bottom"] + B738["fus_height"]
B738["ht_semispan"] = 0.5 * B738["ht_span"]
B738["winglet_bottom_z"] = 4.32   # m, published: bottom of the winglet above the ground (2.3.3, OEW)

# Published numbers the pages print that the outlines do not use:
#   - the trapezoidal reference wing of the 737-800: Jenkinson, Simpkin and Rhodes, Civil Jet
#     Aircraft Design (1999), companion web site, Data A, Table 2 (area m^2, span m, mean
#     aerodynamic chord m, aspect ratio, taper ratio, quarter-chord sweep deg);
#   - maximum design takeoff weight (highest option) and two-class seating: Boeing
#     D6-58325-7 Rev C, Sections 2.1 and 2.1.3.
B738_WING = dict(S_m2=124.60, b_m=34.30, mac_m=4.17, AR=9.44, taper=0.278, sweep_c4=25.0)
B738_MTOW_LB = 174200.0
B738_SEATS_TWO_CLASS = 160
# compatibility with the first version of these outlines
B738.update(fus_bottom_drawn=1.00, nose_z=None, nacelle_y=B738["engine_y"], nacelle_front=B738["inlet_x"],
            nacelle_rear=B738["fan_cowl_end"])

_ZD0, _ZD1 = 1.00, 4.95          # fuselage bottom and top on the general-dimensions side view


def _zmap(P, zd):
    """Height on the drawing (fuselage drawn from 1.00 to 4.95 m) -> height here."""
    return P["fus_bottom"] + (np.asarray(zd, dtype=float) - _ZD0) * P["fus_height"] / (_ZD1 - _ZD0)


# ===================================================================== fuselage
# Side profile read off the general-dimensions drawing (x m, z on the drawing): the nose droops
# (the radome tip is low), the crown runs nearly flat, the aft body sweeps up to the tail cone.
_TOP = [(0.0, 2.45), (0.06, 2.70), (0.25, 2.96), (0.65, 3.24), (1.15, 3.56), (1.65, 3.86), (2.2, 4.12),
        (2.85, 4.36), (3.6, 4.53), (4.6, 4.66), (6.0, 4.79), (7.5, 4.88), (9.0, 4.93), (11.0, 4.95)]
_TOP_TAIL = [(34.0, 4.95), (35.6, 4.93), (36.6, 4.86), (37.35, 4.68), (37.85, 4.44)]
_BOT = [(0.0, 2.45), (0.06, 2.20), (0.25, 1.96), (0.6, 1.76), (1.2, 1.52), (1.9, 1.30), (2.6, 1.14),
        (3.3, 1.04), (4.2, 1.00), (5.5, 1.00)]
_BOT_TAIL = [(25.0, 1.00), (26.5, 1.03), (28.5, 1.18), (30.5, 1.43), (32.5, 1.78), (34.5, 2.22), (36.3, 2.75),
             (37.5, 3.22), (37.95, 3.45)]


def _fuselage_side(P):
    tail_x = P["tail_end"]
    top = np.r_[catmull_rom(_TOP, 10), catmull_rom(_TOP_TAIL, 10)]
    bot = np.r_[catmull_rom(_BOT, 10), catmull_rom(_BOT_TAIL, 10)]
    # the tail cone ends in the exhaust of the auxiliary power unit: a short rounded cap
    z_hi, z_lo = 4.25, 3.52
    zm, rc = 0.5 * (z_hi + z_lo), 0.5 * (z_hi - z_lo)
    a = np.linspace(0.5 * math.pi, -0.5 * math.pi, 17)
    cap = np.c_[tail_x - 0.12 + 0.12 * np.cos(a), zm + rc * np.sin(a)]
    out = np.r_[top, cap[1:-1], bot[::-1][:-1]]
    return np.c_[out[:, 0], _zmap(P, out[:, 1])]


def _fuselage_plan(P, n=120):
    W = 0.5 * P["fus_width"]
    Ln, xs, xe, we = 6.5, 29.0, P["tail_end"], 0.22
    x1 = np.linspace(0.0, Ln, n)
    y1 = W * superellipse(x1 / Ln, 1.9)
    x2 = np.linspace(xs, xe - 0.1, 60)
    y2 = we + (W - we) * (1.0 - ((x2 - xs) / (xe - 0.1 - xs)) ** 2.2)
    a = np.linspace(0.5 * math.pi, 0.0, 8)
    cap = np.c_[xe - 0.1 + 0.1 * np.cos(a), we * np.sin(a)]
    half = np.r_[np.c_[x1, y1], np.c_[x2, y2], cap[1:]]
    return np.r_[half, _mirror(half[::-1])[1:]]


def fuselage_section(P=B738, n=180):
    """Outer contour of the fuselage cross-section (y, z), closed: an upper half-circle of the
    fuselage width and a deeper lower lobe (a half-ellipse), as on the cabin cross-section of
    the source. Example: xy = fuselage_section()"""
    R = 0.5 * P["fus_width"]
    zc = P["fus_bottom"] + P["fus_height"] - R
    b = zc - P["fus_bottom"]
    t = np.linspace(0.0, math.pi, n // 2)
    upper = np.c_[R * np.cos(t), zc + R * np.sin(t)]
    t2 = np.linspace(math.pi, 2.0 * math.pi, n // 2)
    lower = np.c_[R * np.cos(t2), zc + b * np.sin(t2)]
    return np.r_[upper, lower[1:-1]]


# ===================================================================== wing
def _wing_le_te(P, y):
    """Leading and trailing edge x of the wing at |y| (fuselage side to the tip)."""
    y = abs(y)
    W = 0.5 * P["fus_width"]
    yk, yt = P["wing_kink_y"], 0.5 * P["span_wing"]
    if y <= yk:
        le = P["wing_root_le"] + (P["wing_kink_le"] - P["wing_root_le"]) * (y - W) / (yk - W)
        te = P["wing_root_te"]
    else:
        f = (y - yk) / (yt - yk)
        le = P["wing_kink_le"] + (P["wing_tip_le"] - P["wing_kink_le"]) * f
        te = P["wing_root_te"] + (P["wing_tip_te"] - P["wing_root_te"]) * f
    return le, te


def wing_z(P, y):
    """Height of the wing chord line at |y| (dihedral from the root). Example: wing_z(B738, 17.16)"""
    W = 0.5 * P["fus_width"]
    return P["wing_root_z"] + (abs(y) - W) * math.tan(math.radians(P["dihedral"]))


def _thickness(P, y):
    """Wing thickness ratio at |y|: 13% at the root, 10% at the tip (typical; schematic)."""
    W, yt = 0.5 * P["fus_width"], 0.5 * P["span_wing"]
    f = min(max((abs(y) - W) / (yt - W), 0.0), 1.0)
    return 0.13 - 0.03 * f


def wing_box(P, y0, y1, f0, f1, side=1, n=24):
    """Closed shape on the wing (plan view) between spanwise stations y0..y1 and chord fractions
    f0..f1 (0 at the leading edge, 1 at the trailing edge): a control surface or a panel.
    Example: wing_box(B738, 12.4, 16.3, 0.78, 1.0)   # an aileron"""
    ys = np.linspace(y0, y1, n)
    front = np.array([[le + f0 * (te - le), y] for y in ys for le, te in [_wing_le_te(P, y)]])
    back = np.array([[le + f1 * (te - le), y] for y in ys[::-1] for le, te in [_wing_le_te(P, y)]])
    return np.r_[front, back] * np.array([1.0, side])


def _wing_plan(P, side=1):
    yt = 0.5 * P["span_wing"]
    W = 0.5 * P["fus_width"]
    le_in = (P["wing_kink_le"] - P["wing_root_le"]) / (P["wing_kink_y"] - W)
    root_le = P["wing_root_le"] - le_in * W
    poly = np.array([[root_le, 0.0], [P["wing_kink_le"], P["wing_kink_y"]], [P["wing_tip_le"], yt],
                     [P["wing_tip_te"], yt], [P["wing_root_te"], P["wing_kink_y"]], [P["wing_root_te"], 0.0]])
    return poly * np.array([1.0, side])


def _winglet_plan(P, side=1):
    """The blended winglet seen from above: a narrow swept strip from the wing tip out to the
    span with winglets (the winglet stands nearly upright, so its plan is thin)."""
    yt, yw = 0.5 * P["span_wing"], 0.5 * P["span"]
    le0, te0 = P["wing_tip_le"], P["wing_tip_te"]
    le1 = le0 + P["winglet_sweep_x"]
    te1 = le1 + P["winglet_tip_chord"]
    lr = le0 - 0.30 * (le0 - P["wing_kink_le"]) / (yt - P["wing_kink_y"])        # 0.3 m inboard of the tip
    tr = te0 - 0.30 * (te0 - P["wing_root_te"]) / (yt - P["wing_kink_y"])
    front = catmull_rom([(lr, yt - 0.30), (le0 + 0.35, yt + 0.20), (le1 - 0.35, yw - 0.06), (le1, yw)], 8)
    back = catmull_rom([(te1, yw), (te1 - 0.25, yw - 0.12), (te0 + 0.25, yt + 0.25), (tr, yt - 0.30)], 8)
    return np.r_[front, back] * np.array([1.0, side])


def _winglet_side(P):
    """The winglet seen from the side: it rises from the tip with a blend, swept aft, tapering
    from the 4 ft base to the 2 ft tip (published), up to the published wing-tip height."""
    le0 = P["wing_tip_le"]
    z0 = wing_z(P, 0.5 * P["span_wing"])
    zt = P["winglet_top_z"]
    c0, c1 = P["winglet_root_chord"], P["winglet_tip_chord"]
    le1 = le0 + P["winglet_sweep_x"]
    te0 = le0 + P["wing_tip_te"] - P["wing_tip_le"]
    lead = catmull_rom([(le0 - 0.05, z0 + 0.05), (le0 + 0.35, z0 + 0.55), (le0 + 0.95, z0 + 1.25),
                        (le1 - 0.12, zt - 0.10), (le1, zt)], 8)
    trail = catmull_rom([(le1 + c1, zt), (le1 + c1 - 0.15, zt - 0.6), (le0 + c0 + 0.55, z0 + 0.9),
                         (te0 + 0.05, z0 + 0.22), (te0, z0 + 0.08)], 8)
    return np.r_[lead, trail]


def _section_xz(P, y, chord_scale=1.0):
    """Wing section at station |y| in side view: (x, z) outline of a NACA 24xx-like section at
    a small nose-up incidence."""
    le, te = _wing_le_te(P, y)
    c = (te - le) * chord_scale
    t = _thickness(P, y)
    s = naca4(f"24{int(round(100 * t)):02d}", 40, chord=c)["outline"]
    a = math.radians(-1.5)
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return s @ R.T + np.array([le, wing_z(P, y)])


# ===================================================================== nacelle
def _nacelle_side(P):
    """Fan cowl, exhaust nozzle (core cowl) and plug in side view, as three closed shapes."""
    r = 0.5 * P["nacelle_dia"]
    zb = P["engine_ground"]
    zc = zb + r
    x0, x1 = P["inlet_x"], P["fan_cowl_end"]
    # fan cowl: a rounded inlet lip, the crest a little behind the lip, a cowl that tapers aft,
    # and a flattened lower side (the 737 inlet)
    top = catmull_rom([(x0 + 0.02, zc + 0.80 * r), (x0 + 0.15, zc + 0.93 * r), (x0 + 0.55, zc + 0.995 * r),
                       (x0 + 1.25, zc + 1.0 * r), (x0 + 2.3, zc + 0.93 * r), (x1, zc + 0.78 * r)], 10)
    bot = catmull_rom([(x1, zc - 0.74 * r), (x0 + 2.3, zc - 0.90 * r), (x0 + 1.1, zb + 0.005),
                       (x0 + 0.45, zb + 0.03), (x0 + 0.17, zb + 0.12), (x0 + 0.05, zc - 0.70 * r)], 10)
    lip = catmull_rom([(x0 + 0.05, zc - 0.70 * r), (x0 - 0.03, zc - 0.2 * r), (x0 - 0.04, zc + 0.3 * r),
                       (x0 + 0.02, zc + 0.80 * r)], 8)
    cowl = np.r_[top, bot[1:], lip[1:-1]]
    # exhaust nozzle (core cowl): from inside the fan cowl, tapering to the core exit
    core = np.array([(x1 - 0.3, zc + 0.56 * r), (x1 + 0.95, zc + 0.40 * r), (x1 + 0.95, zc - 0.40 * r),
                     (x1 - 0.3, zc - 0.56 * r)])
    core = np.r_[catmull_rom([core[0], (x1 + 0.4, zc + 0.50 * r), core[1]], 8),
                 catmull_rom([core[2], (x1 + 0.4, zc - 0.50 * r), core[3]], 8)]
    plug = np.r_[catmull_rom([(x1 + 0.7, zc + 0.30 * r), (x1 + 1.3, zc + 0.18 * r), (x1 + 1.85, zc)], 8),
                 catmull_rom([(x1 + 1.85, zc), (x1 + 1.3, zc - 0.18 * r), (x1 + 0.7, zc - 0.30 * r)], 8)[1:]]
    return cowl, core, plug, zc


def _nacelle_plan(P, side=1):
    """Fan cowl, exhaust nozzle and plug in plan view (the nacelle is round: same widths as the side)."""
    r = 0.5 * P["nacelle_dia"]
    yc = side * P["engine_y"]
    x0, x1 = P["inlet_x"], P["fan_cowl_end"]
    half = catmull_rom([(x0 + 0.02, 0.78 * r), (x0 + 0.25, 0.92 * r), (x0 + 0.75, 0.99 * r), (x0 + 1.4, r),
                        (x0 + 2.4, 0.93 * r), (x1, 0.78 * r)], 10)
    lip = catmull_rom([(x0 + 0.02, -0.78 * r), (x0 - 0.06, -0.55 * r), (x0 - 0.08, 0.0), (x0 - 0.06, 0.55 * r),
                       (x0 + 0.02, 0.78 * r)], 8)
    cowl = np.r_[half, (half * np.array([1, -1]))[::-1], lip[1:-1]]
    core = np.r_[catmull_rom([(x1 - 0.3, 0.56 * r), (x1 + 0.4, 0.50 * r), (x1 + 0.95, 0.40 * r)], 8),
                 catmull_rom([(x1 + 0.95, -0.40 * r), (x1 + 0.4, -0.50 * r), (x1 - 0.3, -0.56 * r)], 8)]
    plug = np.r_[catmull_rom([(x1 + 0.7, 0.30 * r), (x1 + 1.3, 0.18 * r), (x1 + 1.85, 0.0)], 8),
                 catmull_rom([(x1 + 1.85, 0.0), (x1 + 1.3, -0.18 * r), (x1 + 0.7, -0.30 * r)], 8)[1:]]
    sh = np.array([0.0, yc])
    return cowl + sh, core + sh, plug + sh


# ===================================================================== tails
def _ht_edges(P, y):
    s = P["ht_semispan"]
    f = min(abs(y) / s, 1.0)
    return (P["ht_root_le"] + (P["ht_tip_le"] - P["ht_root_le"]) * f,
            P["ht_root_te"] + (P["ht_tip_te"] - P["ht_root_te"]) * f)


def _ht_z(P, y):
    return P["ht_tip_z"] - (P["ht_semispan"] - abs(y)) * math.tan(math.radians(P["ht_dihedral"]))


def _ht_plan(P, side=1):
    s = P["ht_semispan"]
    poly = np.array([[P["ht_root_le"], 0.0], [P["ht_tip_le"], s], [P["ht_tip_te"], s], [P["ht_root_te"], 0.0]])
    poly = fillet(poly, 1, 0.5, 12)
    return poly * np.array([1.0, side])


def _ht_box(P, y0, y1, f0, f1, side=1, n=16):
    ys = np.linspace(y0, y1, n)
    front = np.array([[le + f0 * (te - le), y] for y in ys for le, te in [_ht_edges(P, y)]])
    back = np.array([[le + f1 * (te - le), y] for y in ys[::-1] for le, te in [_ht_edges(P, y)]])
    return np.r_[front, back] * np.array([1.0, side])


def _vt_side(P):
    zt = P["fus_top"]
    zr = zt - 0.35
    k = (P["height"] - zt) / (12.55 - 4.95)          # the drawing's fin, scaled to the published height
    Z = lambda zd: zt + (zd - 4.95) * k                  # noqa: E731
    dorsal = catmull_rom([(P["vt_dorsal_le"], zt), (P["vt_dorsal_le"] + 1.6, Z(5.55)),
                          (32.85, Z(6.55)), (33.25, Z(7.05))], 10)
    lead = [(P["vt_tip_le"] - 0.25, P["height"] - 0.30), (P["vt_tip_le"], P["height"] - 0.05)]
    vt = np.r_[[(P["vt_dorsal_le"] - 0.2, zr)], dorsal, lead,
               [(P["vt_tip_le"] + 0.25, P["height"]), (P["vt_tip_te"], P["height"]), (P["vt_root_te"], zt),
                (P["vt_root_te"], zr)]]
    vt = fillet(vt, len(dorsal) + 2, 0.25, 8)
    te0, te1 = np.array([P["vt_root_te"], zt]), np.array([P["vt_tip_te"], P["height"]])
    on_te = lambda z: te0 + (te1 - te0) * (z - te0[1]) / (te1[1] - te0[1])     # noqa: E731
    z_lo, z_hi = zt + 0.25, P["height"] - 0.30
    te_lo, te_hi = on_te(z_lo), on_te(z_hi)
    rudder = np.array([te_lo - np.array([1.55, 0.0]), te_hi - np.array([0.62, 0.0]), te_hi, te_lo])
    return vt, rudder


def _vt_root_chord(P):
    return P["vt_root_te"] - P["vt_root_le"]


# ===================================================================== gear
def _wheel(center, r, n=72):
    return circle_xy(center, r, n)


def _strut(x, z_top, z_bot, w):
    return np.array([(x - w / 2, z_top), (x + w / 2, z_top), (x + w / 2, z_bot), (x - w / 2, z_bot)])


# ===================================================================== the three views
def aircraft_side(P=B738, detail=True, ground=False):
    """Parts of the jet transport in side view (x aft, z up; the left side seen), as a dict
    name -> Part. Outer parts: fuselage, wing (one closed sliver), winglet, nacelle (fan cowl),
    exhaust_nozzle, exhaust_plug, htail, vtail, rudder, nose_gear, nose_wheel, main_gear,
    main_wheel (no pylon and no wing-body fairing: from the side they hide between the nacelle,
    the wing and the belly). With detail=True also thin dark-gray detail shapes drawn on their
    part (each with `on` naming it): flight_deck_windows, cabin_windows_N, entry_door_1,
    entry_door_2, overwing_exit_1/2, apu_exhaust, inlet_lip, nose_hub, main_hub. The view shows
    the left side, so the cargo doors, which are on the right side (Boeing D6-58325-7, Section
    5.1.4: the cargo loaders serve the side opposite the passenger bridge), are not drawn.
    ground=True adds the ground line (kind "ground").
    Example: parts = aircraft_side(); P = draw_parts(ax, parts)"""
    parts = {}
    zb, zt = P["fus_bottom"], P["fus_top"]
    parts["fuselage"] = Part("fuselage", _fuselage_side(P), "body", z=3.0, inside=(9.0, _zmap(P, 3.2)))
    # wing: the envelope of the root section (at the fuselage side) and the tip section
    W, yt = 0.5 * P["fus_width"], 0.5 * P["span_wing"]
    root, tip = _section_xz(P, W), _section_xz(P, yt)
    parts["wing"] = Part("wing", hull(np.r_[root, tip]), "body", z=4.0, inside=(22.0, wing_z(P, 9.0) + 0.1))
    parts["winglet"] = Part("winglet", _winglet_side(P), "body", z=4.1,
                            inside=(P["wing_tip_le"] + 1.3, wing_z(P, yt) + 1.4))
    # nacelle, nozzle, plug, pylon (all in front of the wing root)
    cowl, core, plug, zc = _nacelle_side(P)
    x0, x1, r = P["inlet_x"], P["fan_cowl_end"], 0.5 * P["nacelle_dia"]
    parts["nacelle"] = Part("nacelle", cowl, "engine", z=6.0, inside=(x0 + 1.4, zc))
    parts["exhaust_nozzle"] = Part("exhaust_nozzle", core, "engine", z=5.9, inside=(x1 + 0.45, zc + 0.25 * r))
    parts["exhaust_plug"] = Part("exhaust_plug", plug, "engine", z=5.95, inside=(x1 + 1.25, zc))
    # no pylon in the side view: on the 737 the nacelle sits just ahead of and under the wing, and
    # from the side the pylon hides between them (Boeing's side view shows no separate strut);
    # the front view draws it
    # horizontal tail (near side): envelope of its root and tip sections; vertical tail and rudder
    yr = 1.0
    le_r, te_r = _ht_edges(P, yr)
    hr = naca4("0010", 30, chord=te_r - le_r)["outline"] + np.array([le_r, _ht_z(P, yr)])
    le_t, te_t = _ht_edges(P, P["ht_semispan"] - 0.25)
    ht = naca4("0010", 30, chord=te_t - le_t)["outline"] + np.array([le_t, _ht_z(P, P["ht_semispan"])])
    parts["htail"] = Part("htail", hull(np.r_[hr, ht]), "body", z=5.0, inside=(37.4, _ht_z(P, 4.0)))
    vt, rud = _vt_side(P)
    parts["vtail"] = Part("vtail", vt, "body", z=2.0, inside=(35.0, 8.6))
    parts["rudder"] = Part("rudder", rud, "surface", z=2.3, inside=(rud[:, 0].mean(), 8.6))
    # landing gear, wheels on the ground (tires to scale); a two-wheel unit seen from the side reads as one wheel
    rn, rm = 0.5 * P["nose_tire"], 0.5 * P["main_tire"]
    xn, xm = P["nose_gear_x"], P["main_gear_x"]
    parts["nose_gear"] = Part("nose_gear", np.r_[_strut(xn, zb + 0.15, 0.62, 0.20)[:2], _strut(xn, 0.62, rn, 0.12)[2:]],
                              "gear", z=2.5, inside=(xn, 0.9))
    parts["nose_wheel"] = Part("nose_wheel", _wheel((xn, rn), rn), "gear", z=2.6, inside=(xn, rn + 0.5 * rn))
    main = np.array([(xm - 0.15, zb + 0.6), (xm + 0.15, zb + 0.6), (xm + 0.15, 1.05), (xm + 0.09, 1.0),
                     (xm + 0.09, rm), (xm - 0.09, rm), (xm - 0.09, 1.0), (xm - 0.15, 1.05)])
    parts["main_gear"] = Part("main_gear", main, "gear", z=6.5, inside=(xm, 1.15))
    parts["main_wheel"] = Part("main_wheel", _wheel((xm, rm), rm), "gear", z=6.6, inside=(xm, rm + 0.6 * rm))
    if detail:
        _side_details(P, parts)
    if ground:
        parts["ground"] = Part("ground", [(-1.0, 0.0), (P["length"] + 1.0, 0.0)], "ground", z=1.0)
    return parts


def _rrect(x0, x1, z0, z1, r, n=6):
    """A rounded rectangle, closed."""
    pts = np.array([(x0, z0), (x1, z0), (x1, z1), (x0, z1)])
    for i in (3, 2, 1, 0):
        pts = fillet(pts, i, r, n)
    return pts


DETAIL_INK = "#555960"           # windows, doors and exits: dark gray, so the outline dominates


def _side_details(P, parts):
    Z = lambda zd: float(_zmap(P, zd))                     # noqa: E731
    # flight-deck windows: windshield and two side windows under the curve of the nose
    xs = np.linspace(1.50, 3.25, 24)
    crown = _zmap(P, np.interp(xs, *np.array(_TOP).T))
    sill = np.interp(xs, [1.50, 3.25], [Z(3.48), Z(3.66)])
    head = crown - 0.24
    win = np.r_[np.c_[xs, head], np.c_[xs[::-1], sill[::-1]]]
    parts["flight_deck_windows"] = Part("flight_deck_windows", win, "detail", z=3.2, on="fuselage",
                                        inside=(2.4, Z(3.75)))
    for k, xd in enumerate((2.02, 2.62)):              # window posts
        i = int(np.argmin(np.abs(xs - xd)))
        parts[f"flight_deck_post_{k}"] = Part(f"flight_deck_post_{k}", [(xd, sill[i]), (xd + 0.06, head[i])], "line",
                                              z=3.25, on="fuselage")
    # doors and exits (outlines read off the side view)
    doors = {"entry_door_1": (4.45, 5.30, 2.52, 4.20), "entry_door_2": (31.55, 32.40, 2.52, 4.20),
             "overwing_exit_1": (16.55, 17.05, 2.95, 3.70), "overwing_exit_2": (17.65, 18.15, 2.95, 3.70)}
    for name, (a, b, c, d) in doors.items():
        parts[name] = Part(name, _rrect(a, b, Z(c), Z(d), 0.12), "detail", z=3.2, on="fuselage",
                           inside=(0.5 * (a + b), Z(0.5 * (c + d))))
    # cabin window line: 20 in pitch, skipping the doors and exits
    k = 0
    x = 5.95
    while x < 31.0:
        if not (16.25 < x < 18.45 or 27.3 < x < 29.0):
            parts[f"cabin_window_{k}"] = Part(f"cabin_window_{k}", _rrect(x - 0.12, x + 0.12, Z(3.47), Z(3.80), 0.09, 4),
                                              "detail", z=3.2, on="fuselage", inside=(x, Z(3.63)))
            k += 1
        x += 0.508
    # tail cone: the APU exhaust
    ze = Z(0.5 * (4.25 + 3.52))
    parts["apu_exhaust"] = Part("apu_exhaust", _rrect(P["tail_end"] - 0.55, P["tail_end"] - 0.05, ze - 0.17, ze + 0.17,
                                                      0.12, 5), "detail", z=3.2, on="fuselage",
                                inside=(P["tail_end"] - 0.3, ze))
    # engine inlet lip and wheel hubs
    cowl, core, plug, zc = _nacelle_side(P)
    r = 0.5 * P["nacelle_dia"]
    x0 = P["inlet_x"]
    parts["inlet_lip"] = Part("inlet_lip", [(x0 + 0.28, zc + 0.86 * r), (x0 + 0.30, zc - 0.66 * r)], "line", z=6.05,
                              on="nacelle")
    rn, rm = 0.5 * P["nose_tire"], 0.5 * P["main_tire"]
    parts["nose_hub"] = Part("nose_hub", circle_xy((P["nose_gear_x"], rn), 0.42 * rn, 36), "detail", z=2.65,
                             on="nose_wheel")
    parts["main_hub"] = Part("main_hub", circle_xy((P["main_gear_x"], rm), 0.40 * rm, 48), "detail", z=6.65,
                             on="main_wheel")
    for k, p in parts.items():
        if k.startswith(("cabin_window", "entry_door", "overwing_exit", "flight_deck", "apu_exhaust")):
            p.ec = DETAIL_INK


def aircraft_top(P=B738, detail=True):
    """Parts of the jet transport in plan view, seen from above with the nose to the left (x aft,
    page y toward the right wing), as a dict name -> Part: fuselage, wing_body_fairing, vtail and,
    per side ("_R" right wing, toward the top of the page; "_L" left wing, toward the bottom),
    wing, winglet, nacelle, exhaust_nozzle, exhaust_plug, pylon, htail, and the moving
    surfaces as separate shapes: slat_1.._4 (outboard of the engine), flap_inboard,
    flap_outboard, spoiler_1.._6 (root to tip), aileron, elevator. Also slat, spoiler (the
    middle panel) and rudder-free compatibility names: "slat_L" is slat_2_L, "spoiler_L" is
    spoiler_4_L. The fin (vtail) is a thin 7% section drawn with the detail weight; the pylon
    is a strip from the middle of the nacelle to the wing. `detail` is kept for compatibility
    (the plan view has no details). The rudder is left out of the plan view: name it in the
    side view.
    Example: parts = aircraft_top(); P = draw_parts(ax, parts, highlight=("aileron_L",))"""
    parts = {}
    yt = 0.5 * P["span_wing"]
    W = 0.5 * P["fus_width"]
    for s, tag in ((-1, "_L"), (1, "_R")):          # seen from above, nose left: the right wing is up the page
        cowl, core, plug = _nacelle_plan(P, s)
        yc = s * P["engine_y"]
        parts["nacelle" + tag] = Part("nacelle" + tag, cowl, "engine", z=2.0, inside=(P["inlet_x"] + 0.8, yc))
        parts["exhaust_nozzle" + tag] = Part("exhaust_nozzle" + tag, core, "engine", z=1.9,
                                             inside=(P["fan_cowl_end"] + 0.5, yc))
        parts["exhaust_plug" + tag] = Part("exhaust_plug" + tag, plug, "engine", z=1.95,
                                           inside=(P["fan_cowl_end"] + 1.3, yc))
        le = _wing_le_te(P, P["engine_y"])[0]
        pw = 0.22                                         # the pylon seen from above: a narrow strip, two
        xa = P["inlet_x"] + 1.5                           # straight lines from mid-nacelle to the wing
        pyl = np.array([(xa, yc - pw), (le + 0.6, yc - pw), (le + 0.6, yc + pw), (xa, yc + pw)])
        parts["pylon" + tag] = Part("pylon" + tag, pyl, "strut", z=2.5, inside=(0.5 * (xa + le), yc))
        parts["wing" + tag] = Part("wing" + tag, _wing_plan(P, s), "body", z=3.0, inside=(20.5, s * 9.5))
        parts["winglet" + tag] = Part("winglet" + tag, _winglet_plan(P, s), "body", z=3.05,
                                      inside=(P["wing_tip_le"] + 1.3, s * (yt + 0.36)))
        # leading edge: four slats outboard of the engine
        y0s = 6.35
        edges = np.linspace(y0s, yt - 0.45, 5)
        for i in range(4):
            a, b = edges[i] + 0.06, edges[i + 1] - 0.06
            parts[f"slat_{i + 1}{tag}"] = Part(f"slat_{i + 1}{tag}", wing_box(P, a, b, 0.0, 0.20, s), "surface",
                                               z=3.3, inside=(_wing_le_te(P, 0.5 * (a + b))[0] + 0.25, s * 0.5 * (a + b)))
        # trailing edge: inboard flap, a gap behind the engine (schematic), outboard flap, aileron
        parts["flap_inboard" + tag] = Part("flap_inboard" + tag, wing_box(P, W + 0.1, 4.25, 0.76, 1.0, s), "surface",
                                           z=3.3, inside=(P["wing_root_te"] - 0.55, s * 3.2))
        parts["flap_outboard" + tag] = Part("flap_outboard" + tag, wing_box(P, 5.45, 12.35, 0.76, 1.0, s), "surface",
                                            z=3.3, inside=(_wing_le_te(P, 9.0)[1] - 0.5, s * 9.0))
        parts["aileron" + tag] = Part("aileron" + tag, wing_box(P, 12.55, yt - 0.70, 0.76, 1.0, s), "surface", z=3.3,
                                      inside=(_wing_le_te(P, 14.4)[1] - 0.35, s * 14.4))
        # spoilers: six panels ahead of the flaps (one ground spoiler inboard, four flight
        # spoilers and one ground spoiler outboard); positions schematic
        spans = [(W + 0.25, 4.10)] + list(zip(np.linspace(5.60, 12.20, 6)[:-1] + 0.07, np.linspace(5.60, 12.20, 6)[1:] - 0.07))
        for i, (a, b) in enumerate(spans):
            parts[f"spoiler_{i + 1}{tag}"] = Part(f"spoiler_{i + 1}{tag}", wing_box(P, a, b, 0.58, 0.745, s), "surface",
                                                  z=3.3, inside=(np.mean(_wing_le_te(P, 0.5 * (a + b))) +
                                                                 0.16 * np.diff(_wing_le_te(P, 0.5 * (a + b)))[0],
                                                                 s * 0.5 * (a + b)))
        parts["htail" + tag] = Part("htail" + tag, _ht_plan(P, s), "body", z=3.0, inside=(36.4, s * 4.0))
        parts["elevator" + tag] = Part("elevator" + tag, _ht_box(P, 1.05, P["ht_semispan"] - 0.55, 0.70, 1.0, s),
                                       "surface", z=3.3, inside=(_ht_edges(P, 4.0)[1] - 0.35, s * 4.0))
    # compatibility names of the first version
    parts["slat_L"], parts["slat_R"] = parts["slat_2_L"], parts["slat_2_R"]
    parts["spoiler_L"], parts["spoiler_R"] = parts["spoiler_4_L"], parts["spoiler_4_R"]
    parts["fuselage"] = Part("fuselage", _fuselage_plan(P), "body", z=4.0, inside=(10.0, 0.0))
    wbf = catmull_rom([(12.0, W - 0.05), (13.8, W + 0.22), (18.0, W + 0.42), (22.5, W + 0.32), (25.6, W - 0.05)], 10)
    parts["wing_body_fairing"] = Part("wing_body_fairing", np.r_[wbf, _mirror(wbf[::-1])], "detail", z=3.9,
                                      inside=(18.5, W + 0.08))
    # the fin seen from above: a thin section (7% thick) from the true fin root leading edge to the
    # tip's trailing edge (the span of the swept fin seen from above), drawn with the detail weight
    c = P["vt_tip_te"] - P["vt_root_le"]
    fin = naca4("0007", 60, chord=c, closed_te=True)["outline"] + np.array([P["vt_root_le"], 0.0])
    parts["vtail"] = Part("vtail", fin, "detail", z=5.0, inside=(P["vt_root_le"] + 0.3 * c, 0.0))
    return parts


def _winglet_front_raw(P, tip, blend_r, n):
    """The blended winglet seen from ahead (left wing, +y): it leaves the wing tip along the
    dihedral, turns up through a blend of radius blend_r (estimated) and runs straight, canted
    outward, to its tip. Only published numbers fix it: the tip of the wing without winglets
    (half of span_wing, at the dihedral height, which the clearance table gives as 4.32 m) and the
    winglet tip (half of `span`, at winglet_top_z = 6.76 m). The cant follows from them: the
    winglet rises 2.4 m and moves out 0.74 m. The section thickness tapers from 0.13 m to 0.06 m
    (estimated, about 10% of the chord). Returns dict outline (closed), center (the center line),
    cant (deg from the vertical of the straight part), inside."""
    yt = 0.5 * P["span_wing"]
    yw, zt = tip
    z0 = wing_z(P, yt)
    th0 = math.radians(P["dihedral"])
    c = np.array([yt - blend_r * math.sin(th0), z0 + blend_r * math.cos(th0)])   # center of the blend arc

    def end_of_arc(th1):
        return c + blend_r * np.array([math.sin(th1), -math.cos(th1)])
    # the straight part must pass through the winglet tip: solve for its angle th1 by bisection
    lo, hi = th0 + 0.01, math.radians(89.9)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        p1 = end_of_arc(mid)
        d = np.array([yw, zt]) - p1
        if math.atan2(d[1], d[0]) > mid:     # the tip lies above the tangent: turn further
            lo = mid
        else:
            hi = mid
    th1 = 0.5 * (lo + hi)
    p1 = end_of_arc(th1)
    arc_t = np.linspace(th0, th1, n // 2)
    arc = np.array([c + blend_r * np.array([math.sin(t), -math.cos(t)]) for t in arc_t])
    straight = np.linspace(p1, (yw, zt), n // 2)[1:]
    center = np.r_[[(yt - 0.15, z0 - 0.15 * math.tan(th0))], arc, straight]
    seg = np.diff(center, axis=0)
    tang = np.r_[seg[:1], 0.5 * (seg[:-1] + seg[1:]), seg[-1:]]
    tang /= np.hypot(tang[:, 0], tang[:, 1])[:, None]
    nrm = np.c_[-tang[:, 1], tang[:, 0]]
    s_len = np.r_[0.0, np.cumsum(np.hypot(seg[:, 0], seg[:, 1]))]
    half = 0.5 * (0.13 + (0.06 - 0.13) * s_len / s_len[-1])
    upper, lower = center + half[:, None] * nrm, center - half[:, None] * nrm
    a = np.linspace(0.0, math.pi, 9)[1:-1]                 # rounded tip cap
    tipc = center[-1] + half[-1] * (np.outer(np.cos(a), nrm[-1]) + np.outer(np.sin(a), tang[-1]))
    outline = np.r_[upper, tipc, lower[::-1]]
    k = int(0.75 * len(center))
    return dict(outline=outline, center=center, cant=90.0 - math.degrees(th1), inside=tuple(center[k]))


def _winglet_front(P=B738, blend_r=0.40, n=40):
    """The blended winglet seen from ahead (left wing, +y; see _winglet_front_raw): the center
    line is aimed so that the outline reaches the published span with winglets and the published
    winglet-tip height exactly."""
    want = np.array([0.5 * P["span"], P["winglet_top_z"]])
    tip = want.copy()
    for _ in range(6):
        w = _winglet_front_raw(P, tip, blend_r, n)
        got = np.array([w["outline"][:, 0].max(), w["outline"][:, 1].max()])
        tip = tip + (want - got)
    w["top"] = tuple(want)
    return w


def aircraft_front(P=B738, detail=True, ground=False):
    """Parts of the jet transport seen from ahead (y across, the left wing on the right of the
    page; z up), as a dict name -> Part: fuselage (the cross-section), vtail, and per side
    ("_L" left, +y; "_R" right) wing, winglet, nacelle, pylon, htail, main_gear, main_wheels;
    nose_gear and nose_wheels on the centerline. With detail=True: flight_deck_windows (the
    windshield band), inlet_L/_R and fan_L/_R (the inlet and the fan face). ground=True adds the ground
    line. Example: parts = aircraft_front(ground=True); P = draw_parts(ax, parts)"""
    parts = {}
    W, yt, yw = 0.5 * P["fus_width"], 0.5 * P["span_wing"], 0.5 * P["span"]
    zb, zt = P["fus_bottom"], P["fus_top"]
    parts["fuselage"] = Part("fuselage", fuselage_section(P), "body", z=5.0, inside=(0.0, zb + 2.6))
    # vertical tail (seen edge on: thin, tapering)
    tr, tt = 0.12 * _vt_root_chord(P) / 2, 0.09 * 1.5 / 2
    parts["vtail"] = Part("vtail", np.array([(-tr, zt - 0.4), (tr, zt - 0.4), (tt, P["height"] - 0.05),
                                             (0.0, P["height"]), (-tt, P["height"] - 0.05)]), "body", z=1.0,
                          inside=(0.0, 9.0))
    for s, tag in ((1, "_L"), (-1, "_R")):
        # wing: upper and lower surface lines from the root to the tip, with dihedral
        ys = np.linspace(W - 0.4, yt, 30)
        zc_ = np.array([wing_z(P, y) for y in ys])
        th = np.array([0.5 * _thickness(P, y) * (_wing_le_te(P, y)[1] - _wing_le_te(P, y)[0]) for y in ys])
        upper, lower = zc_ + th * 0.75, zc_ - th * 0.6
        wing = np.r_[np.c_[ys, upper], np.c_[ys[::-1], lower[::-1]]]
        parts["wing" + tag] = Part("wing" + tag, wing * np.array([s, 1]), "body", z=3.0,
                                   inside=(s * 10.0, wing_z(P, 10.0)))
        wl = _winglet_front(P)
        parts["winglet" + tag] = Part("winglet" + tag, wl["outline"] * np.array([s, 1]), "body", z=3.1,
                                      inside=(s * wl["inside"][0], wl["inside"][1]))
        # nacelle: round with a flattened lower side, centered on the engine line
        r = 0.5 * P["nacelle_dia"]
        zc = P["engine_ground"] + r
        t = np.linspace(0.0, 2.0 * math.pi, 120, endpoint=False)
        ny = 1.03 * r * np.cos(t)
        nz = np.where(np.sin(t) < 0, 0.94 * r * np.sin(t) * (1.0 - 0.18 * np.abs(np.cos(t)) ** 2), r * np.sin(t))
        yc = s * P["engine_y"]
        parts["nacelle" + tag] = Part("nacelle" + tag, np.c_[yc + ny, zc + nz], "engine", z=6.0, inside=(yc, zc - 0.55 * r))
        zw = wing_z(P, P["engine_y"])
        parts["pylon" + tag] = Part("pylon" + tag, np.array([(yc - 0.20, zc + 0.8 * r), (yc + 0.20, zc + 0.8 * r),
                                                            (yc + 0.20, zw + 0.05), (yc - 0.20, zw + 0.05)]),
                                    "body", z=5.5, inside=(yc, 0.5 * (zc + r + zw)))
        # horizontal tail: thin, with dihedral, behind the fuselage
        ys = np.linspace(0.8, P["ht_semispan"], 12)
        hz = np.array([_ht_z(P, y) for y in ys])
        hth = np.linspace(0.30, 0.10, 12)
        ht = np.r_[np.c_[ys, hz + hth * 0.5], np.c_[ys[::-1], (hz - hth * 0.5)[::-1]]]
        parts["htail" + tag] = Part("htail" + tag, ht * np.array([s, 1]), "body", z=2.0,
                                    inside=(s * 5.0, _ht_z(P, 5.0)))
        # main gear: strut from the wing down to a pair of wheels (16.5 in wide tires, side by side)
        rm, wt = 0.5 * P["main_tire"], 16.5 * 0.0254
        yg = s * 0.5 * P["track"]
        parts["main_gear" + tag] = Part("main_gear" + tag, _strut(yg, wing_z(P, abs(yg)) - 0.2, rm + 0.25, 0.22), "gear",
                                        z=6.5, inside=(yg, 1.4))
        wheels = []
        for dy in (-0.5 * wt - 0.06, 0.5 * wt + 0.06):
            wheels.append(_rrect(yg + dy - 0.5 * wt, yg + dy + 0.5 * wt, 0.0, 2 * rm, 0.12, 6))
        parts["main_wheels" + tag] = Part("main_wheels" + tag, wheels[0], "gear", z=6.6, inside=(yg + (-0.5 * wt - 0.06), rm))
        parts["main_wheels2" + tag] = Part("main_wheels2" + tag, wheels[1], "gear", z=6.6,
                                           inside=(yg + (0.5 * wt + 0.06), rm))
    rn, wn = 0.5 * P["nose_tire"], 7.75 * 0.0254
    parts["nose_gear"] = Part("nose_gear", _strut(0.0, zb + 0.2, rn + 0.15, 0.16), "gear", z=6.5, inside=(0.0, 0.95))
    parts["nose_wheels"] = Part("nose_wheels", _rrect(-0.06 - wn, -0.06, 0.0, 2 * rn, 0.08, 5), "gear", z=6.6,
                                inside=(-0.06 - 0.5 * wn, rn))
    parts["nose_wheels2"] = Part("nose_wheels2", _rrect(0.06, 0.06 + wn, 0.0, 2 * rn, 0.08, 5), "gear", z=6.6,
                                 inside=(0.06 + 0.5 * wn, rn))
    if detail:
        zw0, zw1 = float(_zmap(P, 3.55)), float(_zmap(P, 3.85))
        parts["flight_deck_windows"] = Part("flight_deck_windows", np.array([(-1.15, zw0), (1.15, zw0), (1.30, zw1 + 0.05),
                                                                            (-1.30, zw1 + 0.05)]), "detail", z=5.2,
                                            on="fuselage", inside=(0.0, 0.5 * (zw0 + zw1)))
        parts["flight_deck_windows"].ec = DETAIL_INK
        for s, tag in ((1, "_L"), (-1, "_R")):
            r = 0.5 * P["nacelle_dia"]
            zc = P["engine_ground"] + r
            yc = s * P["engine_y"]
            parts["inlet" + tag] = Part("inlet" + tag, circle_xy((yc, zc + 0.05), 0.80 * r, 72), "detail", z=6.1,
                                        on="nacelle" + tag)
            parts["fan" + tag] = Part("fan" + tag, circle_xy((yc, zc + 0.05), 0.20 * r, 36), "detail", z=6.15,
                                      on="nacelle" + tag)
    if ground:
        parts["ground"] = Part("ground", [(-yw - 1.0, 0.0), (yw + 1.0, 0.0)], "ground", z=1.0)
    return parts


# ===================================================================== three views, body axes
def place(parts, dx=0.0, dy=0.0):
    """The parts moved by (dx, dy) (data units). Example: front = place(aircraft_front(), 45.0, 0.0)"""
    out = {}
    for k, p in parts.items():
        out[k] = Part(p.name, p.xy + np.array([dx, dy]), p.kind, p.z, p.hidden, p.inside + np.array([dx, dy]),
                      on=getattr(p, "on", None))
    return out


def three_view(P=B738, gap=5.0, detail=True, ground=True):
    """The three views arranged as an engineering three-view at one scale: the side view at the
    top left (nose to the left, ground at z = 0), the front view to its right on the same ground
    line, and the plan view under the side view, aligned in x (nose to the left, left wing up).
    Returns dict side=, front=, top= (dicts of parts in one coordinate frame) and offsets
    (front_dx, top_dy). Draw each with draw_parts on one equal-aspect axes.
    Example: v = three_view(); [draw_parts(ax, v[k]) for k in ("side", "front", "top")]"""
    side = aircraft_side(P, detail=detail, ground=ground)
    front_dx = P["length"] + gap + 0.5 * P["span"]
    front = place(aircraft_front(P, detail=detail, ground=ground), front_dx, 0.0)
    top_dy = -(gap + 0.5 * P["span"])
    top = place(aircraft_top(P, detail=detail), 0.0, top_dy)
    return dict(side=side, front=front, top=top, front_dx=front_dx, top_dy=top_dy)


def cg_point(P=B738):
    """A center of gravity for the axes figures: x near the quarter of the mean chord, z near the
    middle of the fuselage, above the wing root (schematic). Returns (x, y, z). Example: x, y, z = cg_point()"""
    return P["cg_x"], 0.0, P["fus_bottom"] + 0.55 * P["fus_height"]


# ===================================================================== body axes in each view
# Screen directions (right, up, toward the reader) of the body axes in each view of this module:
# x forward (toward the nose), y out the right wing, z down. Positive rotations follow the
# right-hand rule: roll (about x) puts the right wing down, pitch (about y) the nose up, yaw
# (about z) the nose to the right.
VIEWS = {
    "side":  dict(x=(-1.0, 0.0, 0.0), y=(0.0, 0.0, -1.0), z=(0.0, -1.0, 0.0), normal="y", rotation="pitch"),
    "top":   dict(x=(-1.0, 0.0, 0.0), y=(0.0, 1.0, 0.0), z=(0.0, 0.0, -1.0), normal="z", rotation="yaw"),
    "front": dict(x=(0.0, 0.0, 1.0), y=(-1.0, 0.0, 0.0), z=(0.0, -1.0, 0.0), normal="x", rotation="roll"),
}


def rotation_sense(view):
    """How the positive rotation about the axis normal to the page turns on the page:
    "counterclockwise" when that axis points toward the reader, "clockwise" when it points away.
    Example: rotation_sense("top") -> "clockwise" (yaw, nose right, seen from above)"""
    v = VIEWS[view]
    return "counterclockwise" if v[v["normal"]][2] > 0 else "clockwise"


def winglet_cant(P=B738):
    """Cant of the straight part of the blended winglet from the vertical, deg (front view)."""
    return _winglet_front(P)["cant"]


# ===================================================================== unit checks
def _close(a, b, tol, what):
    assert abs(a - b) <= tol, f"{what}: {a!r} vs {b!r} (tol {tol})"


if __name__ == "__main__":
    from chapter_1.geometry import polygon_area  # noqa: F401
    P = B738

    def ext(parts, kinds=None):
        pts = np.vstack([p.xy for p in parts.values() if p.kind not in ("ground",) and (kinds is None or p.kind in kinds)])
        return pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].min(), pts[:, 1].max()
    top = aircraft_top()
    x0, x1, y0, y1 = ext(top)
    _close(x1 - x0, 39.47, 0.02, "overall length (to the tip of the tail)")
    _close(y1 - y0, 35.79, 0.01, "span with winglets")
    _close(float(np.ptp(top["fuselage"].xy[:, 1])), 3.76, 0.005, "fuselage width")
    _close(float(np.ptp(top["htail_L"].xy[:, 1]) + np.ptp(top["htail_R"].xy[:, 1])), 14.35, 0.01, "tail span")
    _close(float(top["fuselage"].xy[:, 0].max()), 38.02, 0.01, "nose to the tail-cone end")
    _close(float(top["nacelle_R"].inside[1]), 4.83, 1e-9, "engine centerline")
    _close(float(top["nacelle_L"].xy[:, 0].min()), 13.36, 0.10, "nose to the inlet (the rounded lip reaches 8 cm ahead)")
    wl = top["wing_R"].xy
    _close(float(wl[np.argmax(wl[:, 1]), 0]), 23.47, 0.6, "wing tip leading edge (rounded corner)")
    side = aircraft_side(ground=True)
    x0, x1, z0, z1 = ext(side)
    _close(z1, 12.55, 0.01, "height")
    _close(z0, 0.0, 1e-9, "wheels on the ground")
    _close(float(side["main_wheel"].xy[:, 0].mean() - side["nose_wheel"].xy[:, 0].mean()), 15.60, 1e-6, "wheelbase")
    _close(float(np.ptp(side["main_wheel"].xy[:, 1])), 44.5 * 0.0254, 1e-3, "main tire")
    _close(float(np.ptp(side["nose_wheel"].xy[:, 1])), 27 * 0.0254, 1e-3, "nose tire")
    _close(float(side["nacelle"].xy[:, 1].min()), 0.64, 0.01, "engine above the ground")
    _close(float(side["winglet"].xy[:, 1].max()), 6.76, 0.01, "top of the winglet")
    _close(wing_z(P, 0.5 * P["span_wing"]), 4.32, 0.12, "bottom of the winglet (dihedral)")
    f = side["fuselage"].xy
    _close(float(f[:, 1].max() - f[:, 1].min()), 4.03, 0.02, "fuselage height")
    _close(float(side["fuselage"].xy[:, 0].max()), 38.02, 0.01, "tail-cone end (side)")
    front = aircraft_front(ground=True)
    x0, x1, z0, z1 = ext(front)
    _close(x1 - x0, 35.79, 0.01, "span with winglets (front)")
    _close(z1, 12.55, 0.01, "height (front)")
    sec = front["fuselage"].xy
    _close(float(np.ptp(sec[:, 0])), 3.76, 0.005, "section width")
    _close(float(np.ptp(sec[:, 1])), 4.03, 0.005, "section height")
    gl = front["main_gear_L"].inside[0] - front["main_gear_R"].inside[0]
    _close(gl, 5.72, 1e-9, "track")
    _close(float(front["htail_L"].xy[:, 1].max()), 5.64, 0.2, "stabilizer tip height")
    _close(P["winglet_height"], 2.4384, 1e-9, "winglet 8 ft")
    v = three_view()
    assert set(v) >= {"side", "front", "top"}
    # handedness: in every view x, y, z form a right-handed set (x cross y = z), and the drawing agrees
    for name, vw in VIEWS.items():
        assert np.allclose(np.cross(vw["x"], vw["y"]), vw["z"]), f"{name} view: body axes not right-handed"
        assert sum(abs(c) for c in vw[vw["normal"]][:2]) == 0.0, f"{name} view: the normal axis lies in the page"
    assert float(top["wing_R"].xy[:, 1].mean()) > 0 > float(top["wing_L"].xy[:, 1].mean()), \
        "plan view seen from above, nose left: the right wing must be toward the top of the page"
    assert float(top["fuselage"].xy[:, 0].min()) < float(top["htail_R"].xy[:, 0].min()), "plan view: nose to the left"
    assert float(front["wing_R"].xy[:, 0].mean()) < 0 < float(front["wing_L"].xy[:, 0].mean()), \
        "front view seen from ahead: the right wing must be on the left of the page"
    assert float(side["fuselage"].xy[:, 0].min()) < float(side["vtail"].xy[:, 0].min()), "side view: nose to the left"
    assert rotation_sense("side") == "clockwise" and rotation_sense("top") == "clockwise" \
        and rotation_sense("front") == "counterclockwise"
    # positive yaw seen from above turns the nose (left end) toward the right wing (up the page):
    # a clockwise turn moves a point left of the center upward
    assert np.cross([0, 0, -1.0], [-1.0, 0, 0])[1] > 0
    # winglet seen from ahead: rises from the tip and leans outward (no inward hook)
    wl = front["winglet_L"].xy
    _close(float(wl[:, 0].max()), 0.5 * P["span"], 1e-6, "winglet tip at the span with winglets (front)")
    _close(float(wl[:, 1].max()), P["winglet_top_z"], 1e-6, "winglet top height (front)")
    cen = _winglet_front(P)["center"]
    assert np.all(np.diff(cen[:, 0]) > 0), "the winglet moves outward all the way up"
    assert 5.0 < winglet_cant(P) < 20.0, winglet_cant(P)
    print("aircraft.py: all unit checks passed")
