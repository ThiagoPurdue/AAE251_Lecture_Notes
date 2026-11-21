"""Launch vehicles standing on the pad, as separate closed parts (chapter_1.geometry.Part) for
drawing.draw_parts(): a heavy launcher with a cryogenic core stage and two solid boosters
(proportions after Ariane 5 ECA) and a two-stage kerosene and liquid-oxygen launcher
(proportions after Falcon 9). Coordinates in meters: x across, z up from the lowest nozzle
exit. Each vehicle has an outline version and a cutaway version (cutaway=True adds the tanks,
engines, adapter and payload inside as thin dashed hidden lines, each drawn on its stage).

Sources:
  - Ariane 5 ECA. Arianespace, "Ariane 5 User's Manual", Issue 5 Revision 2, 2016: Section
    1.5.1 (fairing 5.4 m x 17 m; upper stage ESC-A 5.4 m x 4.711 m with its interstage; solid
    booster EAP 3.05 m x 31.6 m), Annex 4 (main core stage EPC "31 m long", two tanks with a
    common bulkhead) and Annex 5, Figure A5.1 (fairing: about 10.8 m of cylinder, then the
    ogive). ESA Bulletin 123, Berkes, "The Ariane-5 ECA Heavy-Lift Launcher", 2005 (core stage
    31 m long; 50.5 m tall in a dual launch with the long fairing). ESA, "Main cryogenic stage
    EPC" (liquid oxygen above, 120 m^3; liquid hydrogen below, 390 m^3). ESA, "Boosters (EAP)"
    (nozzle 3.8 m long, 3.1 m outer diameter at the exit). ESA Bulletin 85, Gigou et al., 1996
    (booster nose: a conical front skirt at 12 degrees ending in a hemispherical cap). CNES,
    "Ariane 5, le lanceur en chiffres", 2025 (Vulcain 2: 3 m high, 2 m in diameter). AIAA
    vehicle guide, Ariane (the boosters' upper attachment at the core's forward skirt; Vulcain 2
    area ratio 58.2). The upper stage (ESC-A) has "two fully separated tanks" (Ariane 5 User's
    Manual, Annex 4); their layout inside the stage (hydrogen above, the oxygen tank tucked under
    the hydrogen tank's lower dome) is a schematic choice, not a published drawing.
    Estimated (no source gives them): the height of the boosters along the core (their nose
    1 m below the top of the core stage, above the forward attachment at the core's forward
    skirt), the gap between booster and core (0.4 m), the
    attachment struts, the exposed length of the booster nozzle, the booster nose-cap radius,
    the interstage and equipment-bay lengths, the upper-stage tank and engine sizes. The
    stack is 53.9 m tall; published heights run from 50.5 m (ESA, 2005) to 53 m (ESA media
    kit, 2023) for the long fairing.
  - Falcon 9. SpaceX, "Falcon User's Guide", May 2025: height 70 m with the standard fairing,
    diameter 3.66 m, fairing 5.2 m x 13.2 m; liquid oxygen above the RP-1 in both stages, a
    common dome, a transfer tube carrying oxygen through the fuel tank; nine engines, eight
    around one; four landing legs and four grid fins; the vacuum engine inside the interstage.
    Falcon 9 User's Guide Rev 2 (2015), Figure 5-2 (the fairing's conical base skirt).
    The interstage "is fixed to the forward end of the first stage tank" and carries the
    separation system at its forward end, so it stays with the first stage; the four grid fins
    sit "near the top of the first stage", on the interstage (Section 2). The guide says "a common
    dome" separates the tanks but not which way it bulges; its Figure 2-1 draws the joint as a
    flat band, and so do these drawings (a straight bulkhead). Tank lengths: measured on that
    figure (oxygen 53% of the first-stage tank length, 50% of the second stage's).
    Stage and interstage lengths from Spaceflight101, "Falcon 9 FT" (first stage 42.6 m,
    interstage about 4.5 m, second stage 12.6 m), a secondary source. Estimated: engine and
    nozzle sizes, legs and grid fins.
"""
import math

import numpy as np

from chapter_1.geometry import Part, blunted_ogive, catmull_rom, circle_xy, _mirror

__all__ = ["ARIANE5", "ARIANE5_FLIGHT", "FALCON9", "launch_vehicle", "two_stage_vehicle", "bell_contour", "engine_side", "capsule",
           "PROPELLANT_STYLE", "draw_cutaway"]


# ===================================================================== shapes
def bell_contour(r_t, r_e, length, theta_n=30.0, theta_e=8.0, n=40):
    """Radius along a bell nozzle from the throat (s = 0, radius r_t) to the exit (s = length,
    radius r_e): a parabolic contour (quadratic Bezier) leaving the throat at theta_n deg and
    reaching the exit at theta_e deg, the usual approximation of a thrust-optimized bell.
    Returns (s, r). Example: s, r = bell_contour(0.13, 1.0, 2.4)"""
    tn, te = math.tan(math.radians(theta_n)), math.tan(math.radians(theta_e))
    # control point: where the throat and exit tangents meet
    sx = (r_e - r_t - te * length) / (tn - te)
    P0, P1, P2 = np.array([0.0, r_t]), np.array([sx, r_t + tn * sx]), np.array([length, r_e])
    t = np.linspace(0.0, 1.0, n)[:, None]
    B = (1 - t) ** 2 * P0 + 2 * (1 - t) * t * P1 + t ** 2 * P2
    return B[:, 0], B[:, 1]


def engine_side(x, z_top, height, r_exit, r_throat=None, r_chamber=None, area_ratio=None, mount=True):
    """A liquid rocket engine seen from the side, nozzle down: an optional mount cone, the
    combustion chamber, the throat and a bell nozzle, as one closed outline. The exit is at
    z_top - height. r_throat from the area ratio when given. Example: engine_side(0.0, 3.0, 3.0, 1.0, area_ratio=58.2)"""
    if r_throat is None:
        r_throat = r_exit / math.sqrt(area_ratio) if area_ratio else 0.25 * r_exit
    r_chamber = r_chamber or max(1.8 * r_throat, 0.32 * r_exit)
    z_th = z_top - 0.24 * height                         # throat
    z_ch = z_top - 0.08 * height                         # chamber top shoulder
    s, r = bell_contour(r_throat, r_exit, z_th - (z_top - height), theta_n=32.0, theta_e=9.0)
    bell = np.c_[x + r, z_th - s]
    conv = catmull_rom([(x + r_chamber, z_ch), (x + r_chamber, z_ch - 0.06 * height),
                        (x + 0.5 * (r_chamber + r_throat), z_th + 0.05 * height), (x + r_throat, z_th)], 6)
    top = [(x + 0.55 * r_chamber, z_top), (x + r_chamber, z_ch + 0.02 * height)] if mount else [(x + r_chamber, z_top)]
    half = np.r_[top, conv[1:], bell[1:]]
    other = np.c_[2 * x - half[::-1, 0], half[::-1, 1]]
    return np.r_[half, other]


def capsule(x, z0, z1, R, h_top, h_bot, n=24, bot_inverted=False):
    """A tank: a cylinder of radius R from z0 to z1 with elliptical domes h_top above and h_bot
    below (bot_inverted=True turns the lower dome up, as a common bulkhead seen from below).
    Returns a closed outline. Example: capsule(0.0, 5.0, 20.0, 2.65, 1.87, 1.87)"""
    t = np.linspace(0.0, math.pi, n)
    top = np.c_[x + R * np.cos(t), z1 + h_top * np.sin(t)]
    s = -1.0 if not bot_inverted else 1.0
    bot = np.c_[x + R * np.cos(t + math.pi), z0 + s * h_bot * np.abs(np.sin(t))]
    return np.r_[top, bot[1:-1]]


def _tank(parts, name, xy, contents, on, inside, z=3.2):
    """A propellant volume of a cutaway: a closed part of kind "tank" drawn on its stage."""
    p = Part(name, xy, "tank", z=z, on=on, inside=inside)
    p.contents = contents
    parts[name] = p
    return p


def _lay_down(parts):
    """The parts rotated to lie nose to the right (x along the vehicle, the old +x side at the
    bottom of the page), keeping each part's contents and hatch."""
    from chapter_1.geometry import rotate_parts
    out = rotate_parts(parts, -90.0)
    for k, p in parts.items():
        for attr in ("contents", "hatch"):
            if hasattr(p, attr):
                setattr(out[k], attr, getattr(p, attr))
    return out


def _box(x0, x1, z0, z1):
    return np.array([(x0, z0), (x1, z0), (x1, z1), (x0, z1)])


def _shift(xy, dx=0.0, dz=0.0):
    return np.asarray(xy, dtype=float) + np.array([dx, dz])


# ===================================================================== heavy launcher with boosters
ARIANE5 = dict(
    core_d=5.4,               # m, published (User's Manual 1.5.1)
    core_len=31.0,            # m, published: core stage EPC with its engine (Annex 4; ESA Bulletin 123)
    engine_height=3.0,        # m, published (CNES 2025, rounded): Vulcain 2
    engine_exit=2.0,          # m, published (CNES 2025, rounded): Vulcain 2 diameter
    engine_area_ratio=58.2,   # published (AIAA vehicle guide)
    engine_in_skirt=0.7,      # m, estimated: how far the engine top sits inside the aft skirt
    esc_len=4.711,            # m, published: upper stage between its interface rings, with the interstage
    iss_len=1.9,              # m, estimated: the interstage part of it
    veb_len=1.14,             # m, estimated: the vehicle equipment bay
    fairing_len=17.0, fairing_cyl=10.8, fairing_nose_r=0.55,   # m, published (1.5.1; Figure A5.1)
    eap_d=3.05, eap_len=31.6,  # m, published
    eap_nozzle_len=3.8, eap_nozzle_exit=3.1,   # m, published (ESA): nozzle length and exit outer diameter
    eap_nozzle_out=2.6,       # m, estimated: the part of the nozzle below the aft skirt
    eap_nose_cone_deg=12.0,   # deg, published (ESA Bulletin 85): the conical front skirt
    eap_nose_cap=0.55,        # m, estimated: radius of the hemispherical cap
    eap_top_below_core=1.0,   # m, estimated: booster nose 1 m below the top of the core stage
    eap_gap=0.4,              # m, estimated: booster to core
    lox_volume=120.0, lh2_volume=390.0,   # m^3, published (ESA, main stage EPC; generic version)
    tank_wall=0.05,           # m, the tanks drawn 5 cm inside the skin
    payload_d=3.6, payload_len=5.2, adapter_len=1.2,        # a generic satellite under the fairing
    eap_channel_r=0.45,       # m, estimated: radius of the central channel of the solid grain (drawn)
    # upper stage, estimated (no source gives the sizes): heights from the top of the interstage
    upper=dict(lh2_z0=0.60, lh2_z1=2.15, lh2_dome_top=0.50, lh2_dome_bot=0.60,
               lox_center=0.20, lox_r=0.85, engine_len=2.0, engine_exit=1.0),
)


def _eap_nose(R, cone_deg, r_cap, n=40):
    """Upper half-outline (r, z from the start of the nose) of a cone at cone_deg ending in a
    tangent hemispherical cap of radius r_cap. Returns (r, z) points and the nose length."""
    a = math.radians(cone_deg)
    r_t = r_cap * math.cos(a)                      # radius where the cone meets the cap
    L_cone = (R - r_t) / math.tan(a)
    z_c = L_cone - r_cap * math.sin(a)             # cap center on the axis
    cone = np.c_[np.linspace(R, r_t, 12), np.linspace(0.0, L_cone, 12)]
    t = np.linspace(a, 0.5 * math.pi, n)
    cap = np.c_[r_cap * np.cos(t), z_c + r_cap * np.sin(t)]
    pts = np.r_[cone, cap[1:]]
    return pts, z_c + r_cap


def launch_vehicle(P=ARIANE5, payload="hidden", cutaway=False, orientation="vertical"):
    """Parts of a heavy launcher with two strap-on solid boosters (proportions after Ariane 5
    ECA), standing on its nozzles (x across, z up). Outer parts: fairing, equipment_bay,
    upper_stage, interstage, core_stage, core_engine, booster_left and booster_right (also as
    booster_top / booster_bottom), their _nozzle, the attachment struts (strut_fwd_*,
    strut_aft_*), stage-joint lines. payload="hidden" draws the payload and its adapter as
    hidden lines (None leaves them out). cutaway=True draws the vehicle cut open along its
    axis: the payload and adapter become solid line art, and the propellant volumes become
    closed parts of kind "tank" (each with `contents` "lox", "lh2" or "solid", drawn on its
    stage; draw them with draw_cutaway(), which tints and hatches each propellant): lox_tank
    above lh2_tank in the core stage, sharing the common bulkhead (`common_bulkhead`, an open
    line on the core stage); in the upper stage lh2_tank_upper above the nested lox_tank_upper,
    with its engine (upper_engine, kind "engine") below them; booster_propellant_* with the
    central channel of the grain (booster_channel_*, contents "void"). orientation="horizontal" lays it nose to the right, as
    the first version did. Example: parts = launch_vehicle(cutaway=True)"""
    R = 0.5 * P["core_d"]
    parts = {}
    he = P["engine_height"]
    z_core0 = he - P["engine_in_skirt"]               # bottom of the core stage's skin
    z_core1 = P["core_len"]                           # top of the core stage (forward skirt)
    parts["core_stage"] = Part("core_stage", _box(-R, R, z_core0, z_core1), "stage", z=3.0,
                               inside=(0.0, 0.5 * (z_core0 + z_core1)))
    parts["core_engine"] = Part("core_engine", engine_side(0.0, he, he, 0.5 * P["engine_exit"],
                                                           area_ratio=P["engine_area_ratio"]),
                                "engine", z=2.5, inside=(0.0, 0.35 * he))
    z = z_core1
    parts["interstage"] = Part("interstage", _box(-R, R, z, z + P["iss_len"]), "stage", z=3.0,
                               inside=(0.0, z + 0.5 * P["iss_len"]))
    z += P["iss_len"]
    up = P["esc_len"] - P["iss_len"]
    parts["upper_stage"] = Part("upper_stage", _box(-R, R, z, z + up), "stage", z=3.0, inside=(0.0, z + 0.5 * up))
    z += up
    parts["equipment_bay"] = Part("equipment_bay", _box(-R, R, z, z + P["veb_len"]), "stage", z=3.0,
                                  inside=(0.0, z + 0.5 * P["veb_len"]))
    z += P["veb_len"]
    z_fair0 = z
    nose = blunted_ogive(R, P["fairing_len"] - P["fairing_cyl"], P["fairing_nose_r"])
    right = np.r_[[(R, z_fair0)], np.c_[nose[:, 1], z_fair0 + P["fairing_cyl"] + nose[:, 0]]]
    fairing = np.r_[right, np.c_[-right[::-1, 0], right[::-1, 1]][1:]]
    parts["fairing"] = Part("fairing", fairing, "fairing", z=3.0, inside=(0.5 * R, z_fair0 + 0.4 * P["fairing_cyl"]))
    parts["core_joint0"] = Part("core_joint0", [(-R, z_core0 + 1.3), (R, z_core0 + 1.3)], "line", z=3.1,
                                on="core_stage")                 # the aft skirt joint (schematic)
    if payload:
        a0 = z_fair0                                      # the adapter sits on the equipment bay
        rp = 0.5 * P["payload_d"]
        hid = not cutaway                                 # cut open, the payload is in plain view
        parts["adapter"] = Part("adapter", np.array([(-1.3, a0), (1.3, a0), (0.75, a0 + P["adapter_len"]),
                                                    (-0.75, a0 + P["adapter_len"])]), "detail", z=3.5, hidden=hid,
                                inside=(0.0, a0 + 0.5 * P["adapter_len"]), on="fairing")
        p0 = a0 + P["adapter_len"]
        parts["payload"] = Part("payload", _box(-rp, rp, p0, p0 + P["payload_len"]), "detail", z=3.5, hidden=hid,
                                inside=(0.0, p0 + 0.5 * P["payload_len"]), on="fairing")
    # boosters: nose cone and cap, cylinder, flared aft skirt, nozzle
    rB = 0.5 * P["eap_d"]
    top = z_core1 - P["eap_top_below_core"]
    bot = top - P["eap_len"]
    case0 = bot + P["eap_nozzle_out"]
    nose, L_nose = _eap_nose(rB, P["eap_nose_cone_deg"], P["eap_nose_cap"])
    half = np.r_[[(1.08 * rB, case0), (rB, case0 + 2.2)], np.c_[nose[:, 0], top - L_nose + nose[:, 1]]]
    body = np.r_[half, np.c_[-half[::-1, 0], half[::-1, 1]][1:]]
    for side, tag in ((1, "right"), (-1, "left")):
        xc = side * (R + P["eap_gap"] + rB)
        nm = f"booster_{tag}"
        parts[nm] = Part(nm, _shift(body, xc), "stage", z=4.0, inside=(xc, 0.5 * (case0 + top)))
        noz = engine_side(xc, case0 + 0.6, P["eap_nozzle_out"] + 0.6, 0.5 * P["eap_nozzle_exit"],
                          r_throat=0.5 * P["eap_nozzle_exit"] / math.sqrt(10.36), r_chamber=0.62 * rB, mount=False)
        parts[nm + "_nozzle"] = Part(nm + "_nozzle", noz, "engine", z=3.8, inside=(xc, bot + 0.45 * P["eap_nozzle_out"]))
        L_cyl = (top - L_nose) - (case0 + 2.2)
        for k, zj in enumerate((case0 + 2.2, case0 + 2.2 + L_cyl / 3, case0 + 2.2 + 2 * L_cyl / 3, top - L_nose)):
            parts[f"{nm}_joint{k}"] = Part(f"{nm}_joint{k}", [(xc - rB, zj), (xc + rB, zj)], "line", z=4.1, on=nm)
        # attachments (estimated): a forward beam where the booster is still cylindrical, just below
        # its nose cone, and an aft beam near the core's aft skirt; each spans the gap and overlaps
        # both walls, so it joins the booster to the core
        x_in, x_out = side * R, side * (R + P["eap_gap"])
        lo, hi = min(x_in, x_out), max(x_in, x_out)
        for nm_, zf in ((f"strut_fwd_{tag}", top - L_nose - 0.6), (f"strut_aft_{tag}", z_core0 + 1.3)):
            parts[nm_] = Part(nm_, _box(lo - 0.12, hi + 0.12, zf - 0.45, zf + 0.45), "strut", z=3.9,
                              inside=(0.5 * (lo + hi), zf))
        if cutaway:
            # the solid grain fills the motor case; it burns from a central channel outward
            g0, g1 = case0 + 2.6, top - L_nose - 0.3
            grain = Part(f"booster_propellant_{tag}", _shift(capsule(0.0, g0, g1, rB - 0.12, 1.0, 0.9), xc), "tank", z=4.2,
                         on=nm, inside=(xc + side * 0.75, 0.5 * (case0 + top)))
            grain.contents = "solid"
            parts[grain.name] = grain
            rc = P["eap_channel_r"]
            ch = Part(f"booster_channel_{tag}", _shift(capsule(0.0, g0 - 0.6, g1 - 0.2, rc, 0.5 * rc, 0.0001), xc), "tank",
                      z=4.25, on=nm, inside=(xc, 0.5 * (g0 + g1)))
            ch.contents = "void"
            parts[ch.name] = ch
    parts["booster_top"], parts["booster_bottom"] = parts["booster_left"], parts["booster_right"]
    parts["booster_top_nozzle"], parts["booster_bottom_nozzle"] = parts["booster_left_nozzle"], parts["booster_right_nozzle"]
    if cutaway:
        Rt = R - P["tank_wall"] - 0.0
        h = Rt / math.sqrt(2.0)
        A = math.pi * Rt * Rt
        v_dome = 2.0 / 3.0 * A * h
        L_lox = (P["lox_volume"] - 2.0 * v_dome) / A
        L_lh2 = P["lh2_volume"] / A
        zA = z_core0 + 1.3                                 # the bottom of the hydrogen tank's lower dome
        z1 = zA + h
        z2 = z1 + L_lh2                                    # rim of the common bulkhead
        z3 = z2 + L_lox
        _tank(parts, "lh2_tank", capsule(0.0, z1, z2, Rt, -h, h), "lh2", "core_stage", (0.9, 0.5 * (z1 + z2)))
        _tank(parts, "lox_tank", capsule(0.0, z2, z3, Rt, h, h), "lox", "core_stage", (0.9, 0.5 * (z2 + z3)))
        t = np.linspace(math.pi, 2.0 * math.pi, 40)
        parts["common_bulkhead"] = Part("common_bulkhead", np.c_[Rt * np.cos(t), z2 + h * np.sin(t)], "line", z=3.3,
                                        on="core_stage", inside=(0.0, z2 - h))
        # upper stage (estimated sizes): hydrogen tank above, as wide as the stage (the core
        # tanks' radius), the oxygen tank nested in its concave lower dome, the engine below the
        # oxygen tank, inside the interstage and the core's forward skirt
        U = P["upper"]
        zu0 = z_core1 + P["iss_len"]
        _tank(parts, "lh2_tank_upper", capsule(0.0, zu0 + U["lh2_z0"], zu0 + U["lh2_z1"], Rt, U["lh2_dome_top"],
                                               U["lh2_dome_bot"], bot_inverted=True),
              "lh2", "upper_stage", (1.7, zu0 + U["lh2_z1"] - 0.3))
        zl = zu0 + U["lox_center"]
        _tank(parts, "lox_tank_upper", capsule(0.0, zl - 0.25, zl + 0.25, U["lox_r"], U["lox_r"] - 0.25,
                                               U["lox_r"] - 0.25), "lox", "interstage", (0.0, zl))
        ze = zl - U["lox_r"] - 0.05                       # the engine hangs from the bottom of the oxygen tank
        parts["upper_engine"] = Part("upper_engine", engine_side(0.0, ze, U["engine_len"], 0.5 * U["engine_exit"],
                                                                 r_throat=0.09, r_chamber=0.21),
                                     "engine", z=3.4, on="interstage", inside=(0.0, ze - 0.62 * U["engine_len"]))
    if orientation == "horizontal":
        parts = _lay_down(parts)
    return parts


# Ariane 5 flight and stage facts the pages print (not used by the outline). ESA web pages
# "Ariane 5 boosters (EAP)" (share of liftoff thrust %, separation time s and altitude km),
# "Ariane 5 cryogenic main stage (EPC)" (oxygen and hydrogen loads t of the first version of
# the stage, burn time min, separation altitude km) and "Ariane 5 Vulcain engine" (stage empty
# and full mass t, first version). For the version drawn, the ECA, the Ariane 5 User's Manual,
# Issue 5 Rev 2 (2016), Section 1.5.1 gives the core stage EPC a dry mass of 14,700 kg and 170 t
# of LOX + LH2 (epc_dry_t, epc_prop_t) and each booster 240 t of solid propellant; fairing
# jettison at a heat flux of 1,135 W/m^2: Section 3.3.3.2.
ARIANE5_FLIGHT = dict(eap_thrust_share=92.0, eap_sep_s=132.0, eap_sep_km=60.0, epc_burn_min=10.0, epc_sep_km=145.0,
                      lox_t=133.0, lh2_t=26.0, fairing_flux=1135.0, epc_empty_t=12.5, epc_full_t=170.0,
                      epc_dry_t=14.7, epc_prop_t=170.0, eap_prop_t=240.0)


# ===================================================================== two-stage kerosene launcher
FALCON9 = dict(
    d=3.66,                  # m, published (Falcon User's Guide 2025, Table 2-1)
    height=70.0,             # m, published: with both stages, interstage and the standard fairing
    fairing_d=5.2, fairing_len=13.2,   # m, published
    fairing_skirt=0.9,       # m, published (User's Guide Rev 2, Figure 5-2): the conical base skirt
    fairing_cyl=6.9, fairing_nose_r=0.5,   # m, estimated from the same figure
    stage1_len=42.6,         # m, secondary (Spaceflight101): first stage
    interstage_len=4.5,      # m, secondary (Spaceflight101, estimated there)
    engine_out=1.3,          # m, estimated: the part of the first-stage nozzles below the base
    engine_exit=0.92,        # m, estimated: first-stage nozzle exit diameter
    ring_radius=1.30,        # m, estimated: radius of the ring of eight engines
    mvac_exit=3.0, mvac_len=4.0,   # m, estimated: second-stage engine inside the interstage
    lox_fraction=0.53,       # the share of the first-stage tank length taken by liquid oxygen, and
    lox_fraction_2=0.50,     # of the second stage's: both measured on Figure 2-1 of the Falcon User's Guide (2025)
    wall=0.12,               # m, drawn: the interstage wall in section (wide enough to see)
    payload_d=3.0, payload_len=4.6, adapter_len=0.9,
    leg_len=9.5, leg_depth=0.30, fin_w=1.2, fin_h=1.5,   # m, estimated
)


def two_stage_vehicle(P=FALCON9, payload="hidden", cutaway=False, legs=False, grid_fins=False,
                      orientation="vertical"):
    """Parts of a two-stage kerosene and liquid-oxygen launcher (proportions after Falcon 9),
    standing on its engines (x across, z up): fairing, second_stage, interstage, first_stage,
    engine_1..engine_9 (the nine first-stage engines seen from the side: the five front ones
    in front of the four behind), stage-joint lines; legs=True adds landing_leg_* folded along
    the first stage, grid_fins=True adds grid_fin_* stowed on the interstage, which belongs to the
    first stage (separation at its top, z = stage1_len + interstage_len).
    payload="hidden" draws the payload and its adapter as hidden lines. cutaway=True adds, as
    tanks on their stage: lox_tank_1 above rp1_tank_1 (a straight common bulkhead) and the oxygen
    transfer tube of the first stage, lox_tank_2 above rp1_tank_2 of the second stage, and its
    vacuum engine (vacuum_engine) inside the interstage; the interstage becomes an open cylinder
    (its walls in section) and only the three engines in the section plane are drawn.
    Example: parts = two_stage_vehicle(cutaway=True)"""
    R = 0.5 * P["d"]
    parts = {}
    z0 = P["engine_out"]
    z1 = P["stage1_len"]
    z2 = z1 + P["interstage_len"]
    z_f0 = P["height"] - P["fairing_len"]
    parts["first_stage"] = Part("first_stage", _box(-R, R, z0, z1), "stage", z=3.0, inside=(0.0, 0.5 * (z0 + z1)))
    if cutaway:                                           # cut open: an open cylinder, its walls in section
        t = P["wall"]
        parts["interstage"] = Part("interstage", np.array([(-R, z1), (-R, z2), (-R + t, z2), (-R + t, z1 + t),
                                                           (R - t, z1 + t), (R - t, z2), (R, z2), (R, z1)]), "stage",
                                   z=3.0, inside=(0.0, 0.5 * (z1 + z2)))
    else:
        parts["interstage"] = Part("interstage", _box(-R, R, z1, z2), "stage", z=3.0, inside=(0.0, 0.5 * (z1 + z2)))
    parts["second_stage"] = Part("second_stage", _box(-R, R, z2, z_f0), "stage", z=3.0, inside=(0.0, 0.5 * (z2 + z_f0)))
    Rf = 0.5 * P["fairing_d"]
    nose = blunted_ogive(Rf, P["fairing_len"] - P["fairing_skirt"] - P["fairing_cyl"], P["fairing_nose_r"])
    zc0 = z_f0 + P["fairing_skirt"]
    right = np.r_[[(R, z_f0), (Rf, zc0)], np.c_[nose[:, 1], zc0 + P["fairing_cyl"] + nose[:, 0]]]
    parts["fairing"] = Part("fairing", np.r_[right, np.c_[-right[::-1, 0], right[::-1, 1]][1:]], "fairing", z=3.0,
                            inside=(0.5 * Rf, zc0 + 0.45 * P["fairing_cyl"]))
    parts["stage1_joint"] = Part("stage1_joint", [(-R, z0 + 1.2), (R, z0 + 1.2)], "line", z=3.1, on="first_stage")
    # nine engines: center, and eight on a ring, seen from the side; the near ones over the far ones.
    # Cut open along the axis, only the three in the section plane show: the center engine and the
    # two ring engines at the sides, three separate bells
    re_ = 0.5 * P["engine_exit"]
    angles = (90.0, 45.0, 135.0, 0.0, 180.0, None, 270.0, 315.0, 225.0) if not cutaway else (0.0, None, 180.0)
    k = 0
    for ang in angles:
        if ang is None:
            x, near = 0.0, 0.0
        else:
            x, near = P["ring_radius"] * math.cos(math.radians(ang)), -math.sin(math.radians(ang))
        k += 1
        parts[f"engine_{k}"] = Part(f"engine_{k}", engine_side(x, z0 + 0.25, z0 + 0.25, re_, r_throat=0.12, r_chamber=0.2,
                                                               mount=False),
                                    "engine", z=2.0 + 0.2 * near, inside=(x, 0.4 * z0))
    if legs:
        # four legs folded flat against the first stage during ascent (Falcon User's Guide); seen
        # from the side, two show in profile (a thin wedge, hinged at the base) and one face on
        lw_, L = P["leg_depth"], P["leg_len"]
        for s, tag in ((1, "right"), (-1, "left")):
            parts[f"landing_leg_{tag}"] = Part(f"landing_leg_{tag}", np.array([(s * R, z0 + 0.15), (s * (R + lw_), z0 + 0.15),
                                                                              (s * (R + lw_), z0 + 0.9),
                                                                              (s * (R + 0.6 * lw_), z0 + L),
                                                                              (s * R, z0 + L + 0.2)]),
                                               "gear", z=3.4, inside=(s * (R + 0.45 * lw_), z0 + 0.5 * L))
        if not cutaway:                                   # cut open, the leg facing the reader is cut away
          parts["landing_leg_front"] = Part("landing_leg_front", np.array([(-0.75, z0 + 0.15), (0.75, z0 + 0.15),
                                                                        (0.22, z0 + L), (-0.22, z0 + L)]),
                                            "detail", z=3.4, on="first_stage", inside=(0.0, z0 + 0.3 * L))
    if grid_fins:                                         # on the interstage, near the top of the first stage
        zf = z2 - 0.5 - P["fin_h"]
        for s, tag in ((1, "right"), (-1, "left")):
            x_a, x_b = sorted((s * R, s * (R + 0.35)))
            parts[f"grid_fin_{tag}"] = Part(f"grid_fin_{tag}", _box(x_a, x_b, zf, zf + P["fin_h"]), "surface", z=3.4,
                                            inside=(s * (R + 0.12), zf + 0.5 * P["fin_h"]))
        if not cutaway:                                   # cut open, the fin facing the reader is cut away
            parts["grid_fin_front"] = Part("grid_fin_front", _box(-0.5 * P["fin_w"], 0.5 * P["fin_w"], zf, zf + P["fin_h"]),
                                           "surface", z=3.4, inside=(0.0, zf + 0.5 * P["fin_h"]))
            parts["grid_fin_front"].hatch = "+++"             # the lattice of a grid fin seen face on
    if payload:
        a0 = z_f0 + 0.2
        rp = 0.5 * P["payload_d"]
        hid = not cutaway
        parts["adapter"] = Part("adapter", np.array([(-1.1, a0), (1.1, a0), (0.8, a0 + P["adapter_len"]),
                                                    (-0.8, a0 + P["adapter_len"])]), "detail", z=3.5, hidden=hid,
                                inside=(0.0, a0 + 0.5 * P["adapter_len"]), on="fairing")
        p0 = a0 + P["adapter_len"]
        parts["payload"] = Part("payload", _box(-rp, rp, p0, p0 + P["payload_len"]), "detail", z=3.5, hidden=hid,
                                inside=(0.0, p0 + 0.5 * P["payload_len"]), on="fairing")
    if cutaway:
        Rt = R - 0.05
        h = 0.7 * Rt
        # first stage: oxygen above, RP-1 below, the common dome between them drawn straight (the
        # guide does not say which way it bulges); the transfer tube carries the oxygen down through
        # the middle of the RP-1 tank to the engines (Falcon User's Guide)
        flat = 1e-4
        t0, t1 = z0 + 1.6, z1 - 1.4
        zm = t1 - P["lox_fraction"] * (t1 - t0)
        _tank(parts, "rp1_tank_1", capsule(0.0, t0 + h, zm, Rt, flat, h), "rp1", "first_stage", (0.95, 0.5 * (t0 + zm)))
        _tank(parts, "lox_tank_1", capsule(0.0, zm, t1 - h, Rt, h, flat), "lox", "first_stage", (0.95, 0.5 * (zm + t1)))
        _tank(parts, "transfer_tube", _box(-0.2, 0.2, z0 + 0.35, zm), "lox", "first_stage", (0.0, 0.5 * (t0 + zm)), z=3.25)
        # second stage: the same layout, shorter (its tank is "a shorter version of the first-stage tank")
        s0, s1 = z2 + 0.6, z_f0 - 0.5
        sm = s1 - P["lox_fraction_2"] * (s1 - s0)
        _tank(parts, "rp1_tank_2", capsule(0.0, s0 + h, sm, Rt, flat, h), "rp1", "second_stage", (0.95, 0.5 * (s0 + sm)))
        _tank(parts, "lox_tank_2", capsule(0.0, sm, s1 - h, Rt, h, flat), "lox", "second_stage", (0.95, 0.5 * (sm + s1)))
        parts["vacuum_engine"] = Part("vacuum_engine", engine_side(0.0, s0 - 0.1, P["mvac_len"], 0.5 * P["mvac_exit"],
                                                                   r_throat=0.16, r_chamber=0.30),
                                      "engine", z=3.4, on="interstage", inside=(0.0, s0 - 0.1 - 0.6 * P["mvac_len"]))
    if orientation == "horizontal":
        parts = _lay_down(parts)
    return parts


# ===================================================================== drawing a cutaway
# One look per propellant, so a cutaway reads in grayscale: a light tint and its own hatch.
# The tints are light enough for black text (contrast above 12:1); the hatch is mid gray.
PROPELLANT_STYLE = {
    "lox":   dict(fill="#D3E6F5", hatch="////", name="liquid oxygen"),
    "lh2":   dict(fill="#DCEFD7", hatch="...", name="liquid hydrogen"),
    "rp1":   dict(fill="#F7E3C8", hatch="---", name="kerosene (RP-1)"),
    "solid": dict(fill="#E6E2DA", hatch="xx", name="solid propellant"),
    "void":  dict(fill="#FFFFFF", hatch=None, name="central channel"),
}
HATCH_INK = "#7A7A7A"          # hatch lines inside the tanks (4.3:1 on white)


def draw_cutaway(ax, parts, highlight=(), lw_tank=None, skip=("common_bulkhead",)):
    """Draw a cutaway from launch_vehicle(cutaway=True) or two_stage_vehicle(cutaway=True): every
    part except the tanks with drawing.draw_parts (white line art), then each tank as a closed
    shape with its propellant's tint and hatch (PROPELLANT_STYLE) and a black outline, drawn on
    its stage (a leader that ends inside the stage may cross it). Returns the dict of patches
    (tanks included). Example: P = draw_cutaway(ax, launch_vehicle(cutaway=True))"""
    from chapter_1.drawing import draw_parts
    from chapter_1.style import Polygon, INK, LW_DETAIL, opaque, on_part
    plain = {k: v for k, v in parts.items() if v.kind != "tank" and k not in skip}
    P = draw_parts(ax, plain, highlight=highlight)
    lw = LW_DETAIL if lw_tank is None else lw_tank
    for name, p in sorted(parts.items(), key=lambda kv: kv[1].z):
        if p.kind != "tank":
            continue
        st = PROPELLANT_STYLE[p.contents]
        fillp = Polygon(p.xy, closed=True, fc=st["fill"], ec=HATCH_INK, lw=0.0, zorder=p.z)
        if st["hatch"]:
            fillp.set_hatch(st["hatch"])
        ax.add_patch(fillp)
        opaque(fillp)
        edge = Polygon(p.xy, closed=True, fc="none", ec=INK, lw=lw, joinstyle="round", zorder=p.z + 0.01)
        ax.add_patch(edge)
        fillp._part = edge._part = name
        host = P.get(p.on)
        if host is not None:
            on_part(fillp, host)
            on_part(edge, host)
        P[name] = edge
        P[name + "#fill"] = fillp
    return P


# ===================================================================== unit checks
def _close(a, b, tol, what):
    assert abs(a - b) <= tol, f"{what}: {a!r} vs {b!r} (tol {tol})"


def _span(parts, name, axis):
    return float(np.ptp(parts[name].xy[:, axis]))


if __name__ == "__main__":
    s, r = bell_contour(0.13, 1.0, 2.4)
    _close(float(r[0]), 0.13, 1e-12, "bell starts at the throat")
    _close(float(r[-1]), 1.0, 1e-12, "bell ends at the exit")
    assert np.all(np.diff(r) > 0), "bell radius grows"
    a5 = launch_vehicle(cutaway=True)
    P = ARIANE5
    _close(_span(a5, "fairing", 1), 17.0, 1e-6, "fairing length")
    _close(_span(a5, "fairing", 0), 5.4, 1e-6, "fairing diameter")
    _close(_span(a5, "core_stage", 0), 5.4, 1e-9, "core diameter")
    _close(float(a5["core_stage"].xy[:, 1].max() - a5["core_engine"].xy[:, 1].min()), 31.0, 1e-9,
           "core stage with its engine, 31 m")
    _close(_span(a5, "core_engine", 1), 3.0, 1e-9, "engine height")
    _close(_span(a5, "core_engine", 0), 2.0, 1e-9, "engine exit diameter")
    _close(_span(a5, "interstage", 1) + _span(a5, "upper_stage", 1), 4.711, 1e-9, "upper stage with interstage")
    b = a5["booster_right"].xy
    _close(float(b[:, 1].max() - a5["booster_right_nozzle"].xy[:, 1].min()), 31.6, 1e-9, "booster length")
    xc = a5["booster_right"].inside[0]
    _close(float(2 * np.max(np.abs(b[np.abs(b[:, 1] - (b[:, 1].min() + 2.2)) < 1e-9, 0] - xc))), 3.05, 1e-9,
           "booster diameter")
    _close(_span(a5, "booster_right_nozzle", 0), 3.1, 1e-9, "booster nozzle exit")
    Rt = 2.7 - P["tank_wall"]
    A = math.pi * Rt * Rt
    lox = a5["lox_tank"].xy
    # the tanks hold the published volumes (cylinder plus two elliptical domes)
    h = Rt / math.sqrt(2.0)
    L = float(lox[:, 1].max() - lox[:, 1].min()) - 2 * h
    _close(A * L + 4.0 / 3.0 * A * h, P["lox_volume"], 0.5, "LOX tank volume (sampled domes)")
    total = float(max(p.xy[:, 1].max() for p in a5.values()))
    assert 50.5 <= total <= 54.7, total
    f9 = two_stage_vehicle(cutaway=True, legs=True, grid_fins=True)
    _close(float(max(p.xy[:, 1].max() for p in f9.values())), 70.0, 1e-6, "Falcon 9 height")
    _close(float(min(p.xy[:, 1].min() for p in f9.values())), 0.0, 1e-9, "on its engines")
    _close(_span(f9, "first_stage", 0), 3.66, 1e-9, "Falcon 9 diameter")
    _close(_span(f9, "fairing", 0), 5.2, 1e-9, "fairing diameter")
    _close(_span(f9, "fairing", 1), 13.2, 1e-6, "fairing height")
    assert len([k for k in f9 if k.startswith("engine_")]) == 3, "cut open: the three engines in the section plane"
    assert len([k for k in two_stage_vehicle() if k.startswith("engine_")]) == 9, "nine engines in the outline"
    F = FALCON9
    z1, z2 = F["stage1_len"], F["stage1_len"] + F["interstage_len"]
    for k in ("grid_fin_left", "grid_fin_right"):
        g = f9[k].xy[:, 1]
        assert z1 < g.min() and g.max() < z2, "the grid fins sit on the interstage, which stays with the first stage"
    e = sorted((float(f9[k].xy[:, 0].min()), float(f9[k].xy[:, 0].max())) for k in ("engine_1", "engine_2", "engine_3"))
    assert e[0][1] < e[1][0] and e[1][1] < e[2][0], "three separate bells"
    assert f9["vacuum_engine"].xy[:, 1].min() < z2 < f9["second_stage"].xy[:, 1].min() + 1e-9, \
        "the vacuum engine hangs below the second stage, inside the interstage before separation"
    a5h = launch_vehicle(cutaway=True)
    _close(float(a5h["adapter"].xy[:, 1].min()), float(a5h["equipment_bay"].xy[:, 1].max()), 1e-9,
           "the payload adapter sits on the equipment bay")
    for tag in ("left", "right"):
        st, bo = a5h[f"strut_fwd_{tag}"].xy[:, 0], a5h[f"booster_{tag}"].xy
        zc = a5h[f"strut_fwd_{tag}"].inside[1]
        cyl = bo[np.abs(np.abs(bo[:, 0] - a5h[f"booster_{tag}"].inside[0]) - 0.5 * P["eap_d"]) < 1e-9, 1]
        assert cyl.min() < zc < cyl.max(), "the forward attachment meets the booster where it is cylindrical"
        assert st.min() < -2.7 + 1e-9 or st.max() > 2.7 - 1e-9, tag
    # cutaway: every tank lies inside its stage, the propellants are named, nothing is nested wrongly
    for veh in (a5, f9):
        for k, p in veh.items():
            if p.kind == "tank":
                assert p.contents in PROPELLANT_STYLE, k
    up = a5["lox_tank_upper"].xy
    assert up[:, 1].max() < a5["lh2_tank_upper"].xy[:, 1].min() + P["upper"]["lh2_dome_bot"], "oxygen tank nested under the hydrogen dome"
    assert a5["upper_engine"].xy[:, 1].max() < up[:, 1].min(), "upper-stage engine below its oxygen tank"
    assert a5["upper_engine"].xy[:, 1].min() > a5["lox_tank"].xy[:, 1].max(), "upper-stage engine clear of the core tank"
    lox, lh2 = a5["lox_tank"].xy, a5["lh2_tank"].xy
    assert lox[:, 1].min() < lh2[:, 1].max(), "the oxygen tank's lower dome bulges into the hydrogen tank (common bulkhead)"
    assert a5["upper_engine"].xy[:, 1].min() > a5["booster_right"].xy[:, 1].max(), "upper engine above the booster noses"
    h1 = launch_vehicle(orientation="horizontal")
    assert np.ptp(h1["core_stage"].xy[:, 0]) > np.ptp(h1["core_stage"].xy[:, 1])
    print("launchers.py: all unit checks passed")
    print(f"  heavy launcher: {total:.2f} m tall")
