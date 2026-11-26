"""Drawing helpers for Chapter 5, Aircraft Performance and Propulsion.

Provides reusable line-art schematics on equal-aspect axes:
  - `aircraft_profile_fbd`: the Boeing 737-800 side outline from chapter_1.aircraft (scaled,
    cleaned of landing gear, rotated nose-right and pitched by theta) for level and climbing
    flight free-body diagrams.
  - `draw_turbojet_section`, `draw_turbofan_section`, `draw_turboprop_section` (full sections;
    sides=(1,) with core_only=True gives the half section of the core alone) (page 5.4): engine sections in the
    look of Chapter 4's engine figures (walls cut in section hatched, open inlets and exits, rotor
    rows filled and stator rows open, the annular combustor liner as two thin walls with a rounded
    dome, a fuel nozzle and an open rear, smooth contours from `contour`, shafts drawn to the parts
    they turn, a dash-dot centerline), with proportions after a published
    engine: the General Electric CJ610 (FAA type certificate data sheet 1E16), the CFM56-7B (EASA
    type-certificate data sheet E.004) and the Rolls-Royce AE 2100D2 (EASA type-certificate data
    sheet IM.E.040). `engine_centerline` draws the centerline.
"""
import math

import numpy as np
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch  # noqa: F401 (page modules take them from here)

from chapter_1.style import *  # noqa: F401,F403
from chapter_1.aircraft import aircraft_side, B738
from chapter_1.geometry import rotate_xy


def aircraft_silhouette_right(ax, center=(0.0, 0.0), length=2.4, pitch_deg=0.0, fill=PART_FILL, zorder=3.0):
    """Draw the Boeing 737-800 side outline (without landing gear) facing RIGHT, scaled to
    `length` data units, centered at `center` (CG), and pitched nose-up by `pitch_deg`.
    Returns dict(cg, nose, tail, patches)."""
    parts = aircraft_side(B738, detail=False, ground=False)
    keep = ("fuselage", "wing", "winglet", "nacelle", "exhaust_nozzle", "exhaust_plug", "htail", "vtail")
    # In aircraft_side, nose is at x=0 and tail at x=L (~39.5 m), facing LEFT.
    # Mirror x -> -x so nose points RIGHT, shift CG (at ~0.44 L) to origin, scale to `length`.
    all_x = np.concatenate([parts[k].xy[:, 0] for k in keep if k in parts])
    all_y = np.concatenate([parts[k].xy[:, 1] for k in keep if k in parts])
    L_raw = float(all_x.max() - all_x.min())
    cg_raw = np.array([all_x.min() + 0.44 * L_raw, all_y.min() + 0.25 * (all_y.max() - all_y.min())])
    scale = length / L_raw
    c = np.asarray(center, dtype=float)
    patches = {}
    for k in sorted((n for n in keep if n in parts), key=lambda n: parts[n].z):
        xy = parts[k].xy.copy()
        xy = (xy - cg_raw) * scale
        xy[:, 0] = -xy[:, 0]                          # face right
        xy = rotate_xy(xy, pitch_deg) + c
        pa = Polygon(xy, closed=True, fc=fill, ec=INK, lw=LW_OUTLINE * 0.85, joinstyle="round",
                     zorder=zorder + 0.01 * parts[k].z)
        ax.add_patch(opaque(pa))
        patches[k] = pa
    nose = rotate_xy(np.array([[0.44 * length, 0.0]]), pitch_deg)[0] + c
    tail = rotate_xy(np.array([[-0.56 * length, 0.0]]), pitch_deg)[0] + c
    return dict(cg=c, nose=nose, tail=tail, patches=patches)


# ===================================================================== engine sections (page 5.4)
# The look of Chapter 4's engine figures: walls cut in section hatched, open inlets and exits,
# rotor blade rows filled dark and stator rows open, the annular combustor liner drawn as two thin
# walls with a rounded dome and the fuel nozzle at the front and an open rear, shafts drawn to the
# parts they turn, a dash-dot centerline. Every contour is a smooth curve: a shape-preserving cubic
# (no overshoot) through a few control points, sampled finely, so no polyline corner shows. Each
# engine is drawn in full section; the turbofan and the turboprop can also draw the upper half of
# their core alone, for an enlarged view (sides=(1,), core_only=True). Units are meters, x from the front
# flange of the engine. Only the dimensions a published source gives are asserted (the overall
# length, the largest diameter or height, and the number of stages); the flow-path radii are drawn
# by eye to them, so every caption says "proportions after ...". The page module adds labels, flow
# arrows and keys. Each draw function returns the drawn patches it asserts on.
from scipy.interpolate import PchipInterpolator  # noqa: E402  (shape preserving: no overshoot)
from matplotlib.patches import Circle  # noqa: E402  (the gear sketch of the turboprop)

WALL_HATCH = "////"         # a wall cut in section (as chapter_1.drawing.hatched_wall)
ROTOR_FILL = "#555960"      # rotor blade rows (filled, steel); stator rows are open (white)
SHAFT_LW = 0.9              # discs that join a blade row to its shaft
LINER_LW = 1.2              # the two walls and the dome of a combustor liner


def contour(xp, rp):
    """A smooth contour r(x) through the control points (xp, rp): a shape-preserving cubic, so it
    never overshoots the points. Returns the callable. Example: contour([0, 1, 2], [0.2, 0.3, 0.2])(1.5)"""
    f = PchipInterpolator(np.asarray(xp, dtype=float), np.asarray(rp, dtype=float))
    return lambda x: f(np.asarray(x, dtype=float))


def _xs(x0, x1, n=240):
    return np.linspace(float(x0), float(x1), n)


def _wall(ax, x, r_in, r_out, sg, z=4.0, hatch=WALL_HATCH):
    """A wall cut in section: hatched between the arrays r_in and r_out over x, on the upper (sg=1)
    or lower (sg=-1) half. Returns the patch."""
    x = np.asarray(x, dtype=float)
    xy = np.r_[np.c_[x, sg * np.asarray(r_in, dtype=float)], np.c_[x[::-1], sg * np.asarray(r_out, dtype=float)[::-1]]]
    return ax.add_patch(opaque(Polygon(xy, closed=True, fc="white", ec=INK, lw=1.0, hatch=hatch, zorder=z,
                                       joinstyle="round")))


def _row(ax, x, w, f_hub, f_tip, rotor, sg, z=5.0):
    """One blade row in section, centered at x, w wide, between the contours f_hub and f_tip (its
    edges follow the annulus): a rotor filled dark, a stator open. Returns the patch."""
    x0, x1 = x - w / 2.0, x + w / 2.0
    xy = np.array([[x0, float(f_hub(x0))], [x1, float(f_hub(x1))], [x1, float(f_tip(x1))], [x0, float(f_tip(x0))]])
    return ax.add_patch(Polygon(xy * [1, sg], closed=True, fc=(ROTOR_FILL if rotor else "white"), ec=INK, lw=0.7,
                                zorder=z))


def _body(ax, x, r, sg, z=3.5):
    """The inner body (nose, hub, drum, tail cone) of a section, closed to the centerline. Returns
    the patch."""
    x, r = np.asarray(x, dtype=float), np.asarray(r, dtype=float)
    xy = np.r_[np.c_[x, sg * r], [[x[-1], 0.0], [x[0], 0.0]]]
    return ax.add_patch(Polygon(xy, closed=True, fc="white", ec=INK, lw=1.0, zorder=z, joinstyle="round"))


def _shaft(ax, x0, x1, r0, r1, sg, hatch=None, z=4.0):
    """A shaft in section between radii r0 and r1 (filled dark, or white with a hatch)."""
    xy = np.array([[x0, r0], [x1, r0], [x1, r1], [x0, r1]]) * [1, sg]
    fc = "white" if hatch else ROTOR_FILL
    return ax.add_patch(Polygon(xy, closed=True, fc=fc, ec=INK, lw=0.7, hatch=hatch, zorder=z))


def _liner(ax, x0, x1, x_exit, r_in, r_out, exit_in, exit_out, sg, r_case=None, z=5.5):
    """The annular combustor liner in section: two thin walls (inner at r_in, outer at r_out) joined
    at the front by a rounded dome, running to x1 and then turning smoothly to the turbine's inlet
    radii (exit_in, exit_out) at x_exit, where the liner is open. With r_case (the casing radius at
    the dome), a fuel nozzle runs in from the casing to the front of the dome. Returns a dict:
    the line, the dome front x, the exit x and radii."""
    a = 0.5 * (r_out - r_in)
    rc = 0.5 * (r_out + r_in)
    t = np.linspace(0.5 * math.pi, 1.5 * math.pi, 40)
    xd, rd = x0 + a + a * np.cos(t), rc + a * np.sin(t)                    # front half circle, top to bottom
    s = np.linspace(0.0, 1.0, 40)
    blend = 0.5 * (1.0 - np.cos(math.pi * s))                             # smooth turn to the exit radii
    xo = np.r_[x_exit - (x_exit - x1) * s, x1, x0 + a]
    ro = np.r_[exit_out + (r_out - exit_out) * blend, r_out, r_out]
    xi = np.r_[x0 + a, x1, x1 + (x_exit - x1) * s]
    ri = np.r_[r_in, r_in, r_in + (exit_in - r_in) * blend]
    xx, rr = np.r_[xo, xd, xi], np.r_[ro, rd, ri]
    ln = ax.plot(xx, sg * rr, color=INK, lw=LINER_LW, zorder=z, solid_joinstyle="round", solid_capstyle="butt")[0]
    if r_case is not None:                                                # fuel nozzle: stem from the casing, tip at the dome
        xs_ = x0 - 0.6 * a
        ax.plot([xs_, xs_, x0 - 0.15 * a], [sg * r_case, sg * rc, sg * rc], color=INK, lw=1.0, zorder=z,
                solid_joinstyle="round")
        ax.plot([x0 - 0.15 * a], [sg * rc], "o", ms=2.6, color=INK, zorder=z + 0.1)
    return dict(line=ln, x_front=x0, x_exit=x_exit, exit_in=exit_in, exit_out=exit_out, r_in=r_in, r_out=r_out)


def engine_centerline(ax, x0, x1):
    """The dash-dot centerline of an engine section, from x0 to x1."""
    return ax.plot([x0, x1], [0.0, 0.0], color=GRAY, lw=LW_FINE + 0.2, ls=(0, (8.0, 2.5, 1.5, 2.5)), zorder=2)[0]


# --- the single-spool turbojet: proportions after the General Electric CJ610 (FAA type certificate
# data sheet 1E16, revision 15, 2008: turbojet, 8-stage axial-flow compressor, annular combustion
# chamber, 2-stage turbine; length 40.50 in flange to flange, largest diameter 17.56 in at the
# largest flange). Station x (m) of the five stages, in flow order.
CJ610_L = 40.50 * 0.0254          # 1.0287 m
CJ610_D = 17.56 * 0.0254          # 0.4460 m
CJ610_STAGES = dict(compressor=8, turbine=2)
TURBOJET_STATIONS = dict(inlet=(0.0, 0.10), compressor=(0.10, 0.46), combustor=(0.46, 0.74),
                         turbine=(0.74, 0.86), nozzle=(0.86, CJ610_L))


def draw_turbojet_section(ax):
    """A single-spool turbojet in full section, flow left to right, x from the front flange (m):
    inlet with its nose fairing, 8-stage compressor whose hub rises and tip falls as the air is
    squeezed, annular combustor liner with its fuel nozzle, 2-stage turbine, tail cone and converging
    nozzle, one shaft from the turbine to the compressor. Proportions after the CJ610 (CJ610_L,
    CJ610_D, CJ610_STAGES). Returns a dict: stations, the contours (f_hub, f_cas), the outer wall
    patches, the rotor and stator patches of each stage group, the liners, the shaft, x_exit."""
    S = TURBOJET_STATIONS
    R = CJ610_D / 2.0
    L = CJ610_L
    f_cas = contour([0.0, 0.10, 0.44, 0.47, 0.52, 0.60, 0.68, 0.73, 0.76, 0.86, 0.90, L],
                    [0.180, 0.178, 0.145, 0.152, 0.188, 0.190, 0.188, 0.170, 0.168, 0.186, 0.180, 0.135])
    f_out = contour([0.0, 0.10, 0.44, 0.47, 0.52, 0.60, 0.68, 0.73, 0.76, 0.86, 0.90, L],
                    [0.194, 0.192, 0.159, 0.168, 0.210, R, 0.210, 0.186, 0.182, 0.200, 0.194, 0.146])
    # inner body in one smooth contour: nose fairing at the inlet plane, hub, drum and tail cone
    f_hub = contour([0.0, 0.012, 0.035, 0.065, 0.10, 0.44, 0.47, 0.52, 0.68, 0.73, 0.76, 0.86, 0.90, 0.95, 0.995, L],
                    [0.0, 0.030, 0.050, 0.062, 0.070, 0.118, 0.112, 0.100, 0.100, 0.118, 0.122, 0.128, 0.118, 0.080,
                     0.036, 0.0])
    xb = _xs(0.0, L, 320)
    rb = f_hub(xb)
    xx = np.union1d(_xs(0.0, L, 300), [0.60])                             # the largest flange is sampled exactly
    out = dict(stations=S, f_hub=f_hub, f_cas=f_cas, walls=[], rotors={"compressor": [], "turbine": []},
               stators={"compressor": [], "turbine": []}, liners=[], x_exit=L, r_exit=float(f_cas(L)))
    for sg in (1, -1):
        out["walls"].append(_wall(ax, xx, f_cas(xx), f_out(xx), sg))
        _body(ax, xb, rb, sg)
        for i in range(CJ610_STAGES["compressor"]):                       # each compressor stage: rotor, then stator
            x = 0.125 + 0.042 * i
            out["rotors"]["compressor"].append(_row(ax, x, 0.016, f_hub, f_cas, True, sg))
            out["stators"]["compressor"].append(_row(ax, x + 0.020, 0.011, f_hub, f_cas, False, sg))
        out["liners"].append(_liner(ax, 0.505, 0.68, 0.738, 0.116, 0.172, 0.124, 0.165, sg, r_case=float(f_cas(0.49))))
        for i in range(CJ610_STAGES["turbine"]):                          # each turbine stage: nozzle vanes, then rotor
            x = 0.770 + 0.048 * i
            out["stators"]["turbine"].append(_row(ax, x, 0.014, f_hub, f_cas, False, sg))
            out["rotors"]["turbine"].append(_row(ax, x + 0.022, 0.016, f_hub, f_cas, True, sg))
        out["shaft"] = _shaft(ax, 0.10, 0.84, 0.0, 0.013, sg)
        for x0, x1 in ((0.125, 0.14), (0.419, 0.43), (0.792, 0.80), (0.840, 0.84)):
            ax.plot([x0, x1], [sg * float(f_hub(x0)), sg * 0.013], color=INK, lw=SHAFT_LW, zorder=4.5)
    engine_centerline(ax, -0.12, L + 0.10)
    out["mid"] = lambda k: 0.5 * (S[k][0] + S[k][1])                       # noqa: E731
    return out


def _lip_wall(ax, x_lip, r_lip, rho, xs_out, rs_out, xs_in, rs_in, sg, z=4.0, hatch=WALL_HATCH, n=240):
    """A cowl or nacelle wall cut in section with a rounded inlet lip: the outer contour through
    (xs_out, rs_out) and the inner contour through (xs_in, rs_in), both starting at x = x_lip + rho
    at r_lip + rho and r_lip - rho, joined at the front by a half circle of radius rho (the lip), and
    by a straight trailing edge at the rear. Returns the patch."""
    f_o, f_i = contour(xs_out, rs_out), contour(xs_in, rs_in)
    xo, xi = _xs(xs_out[0], xs_out[-1], n), _xs(xs_in[0], xs_in[-1], n)
    t = np.linspace(0.5 * math.pi, 1.5 * math.pi, 40)
    xa, ra = x_lip + rho + rho * np.cos(t), r_lip + rho * np.sin(t)          # the lip, outer to inner through the front
    xy = np.r_[np.c_[xo[::-1], f_o(xo[::-1])], np.c_[xa[1:-1], ra[1:-1]], np.c_[xi, f_i(xi)]]
    return ax.add_patch(opaque(Polygon(xy * [1, sg], closed=True, fc="white", ec=INK, lw=1.0, hatch=hatch, zorder=z,
                                       joinstyle="round")))


def _outline(ax, xy, sg, z=4.6, lw=0.7):
    """A thin closed outline (a rotor disk or drum seen in section), white inside. Returns the patch."""
    return ax.add_patch(Polygon(np.asarray(xy, dtype=float) * [1, sg], closed=True, fc="white", ec=INK, lw=lw,
                                zorder=z))


# --- the two-spool high-bypass turbofan: proportions after the CFM56-7B (EASA type-certificate
# data sheet E.004, issue 07, 2023, sections 2 and 4: dual rotor; single-stage fan, 3-stage
# low-pressure compressor, 9-stage high-pressure compressor, annular combustor, single-stage
# high-pressure turbine, 4-stage low-pressure turbine; overall length 2,508 mm, height 1,829 mm).
# Only the length and the fan-case height are sourced; the bypass ratio is not drawn to a value.
CFM56_L, CFM56_H = 2.508, 1.829
CFM56_STAGES = dict(fan=1, lpc=3, hpc=9, hpt=1, lpt=4)


def draw_turbofan_section(ax, core_only=False, sides=(1, -1)):
    """A two-spool high-bypass turbofan in section, flow left to right (x in m from the fan-case
    front flange): pointed spinner, wide-chord fan, nacelle with a rounded inlet lip, outlet guide
    vanes in the bypass duct, core cowl, 3 + 9 compressor stages, annular combustor liner, 1 + 4
    turbine stages, the low-pressure shaft inside the hollow high-pressure shaft, and the rotor
    disks and drums that join each rotor to its shaft. sides=(1, -1) draws the full section, (1,)
    the half above the centerline; core_only=True leaves out the nacelle, the fan and the guide vanes
    (for an enlarged view of the core). Returns a dict: the contours, the nacelle patches, the rotor
    patches of the upper half by group, the liner, the shafts, the two annulus areas at the core
    inlet (bypass, core)."""
    R = CFM56_H / 2.0
    f_hub = contour([0.52, 0.62, 0.85, 1.00, 1.55, 1.60, 1.84, 1.88, 1.96, 2.46, 2.75],
                    [0.28, 0.28, 0.27, 0.205, 0.215, 0.215, 0.215, 0.218, 0.22, 0.24, 0.20])
    f_cas = contour([0.52, 0.62, 0.85, 1.00, 1.55, 1.60, 1.84, 1.88, 1.96, 2.46, 2.75],
                    [0.42, 0.41, 0.38, 0.30, 0.258, 0.30, 0.30, 0.292, 0.29, 0.38, 0.34])
    lip = dict(x_lip=-0.60, r_lip=0.83, rho=0.04)                         # nacelle: rounded lip, highlight at x = -0.60
    n_out = ([-0.56, -0.40, -0.20, 0.30, 0.80, 1.38], [0.87, 0.897, R, R, 0.875, 0.742])
    n_in = ([-0.56, -0.40, -0.20, 0.30, 0.80, 1.38], [0.79, 0.778, 0.775, 0.778, 0.765, 0.728])
    f_nin = contour(*n_in)
    f_cowl = contour([0.52, 0.70, 1.20, 1.60, 2.20, 2.75], [0.42, 0.46, 0.48, 0.47, 0.43, 0.36])
    # inner body in one smooth contour: pointed spinner to the fan root, flat hub to the splitter, the
    # hub under the booster, the goose neck, the hub under the core and the core exhaust plug
    s = np.linspace(0.0, 1.0, 40)
    xs_sp = -0.08 + 0.24 * s
    rs_sp = 0.27 * (0.8 * s + 0.2 * (2.0 * s - s ** 2))                   # a slightly convex cone
    f_tail = contour([0.16, 0.52, 0.62, 0.85, 1.00, 1.55, 1.60, 1.84, 1.88, 1.96, 2.46, 2.75, 2.95, 3.10, 3.15],
                     [0.27, 0.28, 0.28, 0.27, 0.205, 0.215, 0.215, 0.215, 0.218, 0.22, 0.24, 0.20, 0.12, 0.035, 0.0])
    xt = _xs(0.16, 3.15, 400)
    xb, rb = np.r_[xs_sp, xt[1:]], np.r_[rs_sp, f_tail(xt)[1:]]
    xk = _xs(0.52, 2.75)
    out = dict(f_hub=f_hub, f_cas=f_cas, f_nin=f_nin, f_cowl=f_cowl, nacelle=[], rotors={k: [] for k in CFM56_STAGES},
               spinner=(xs_sp, rs_sp))
    for sg in sides:
        up = sg == 1
        if not core_only:
            out["nacelle"].append(_lip_wall(ax, lip["x_lip"], lip["r_lip"], lip["rho"], *n_out, *n_in, sg))
        _wall(ax, xk, f_cowl(xk) - 0.025, f_cowl(xk), sg)                # core cowl
        _wall(ax, xk, f_cas(xk), np.minimum(f_cas(xk) + 0.025, f_cowl(xk) - 0.025), sg)   # core casing
        _body(ax, xb, rb, sg)
        if not core_only:
            fan = ax.add_patch(Polygon(np.array([[0.13, 0.27], [0.31, 0.27], [0.34, float(f_nin(0.34))],
                                                 [0.10, float(f_nin(0.10))]]) * [1, sg], closed=True, fc=ROTOR_FILL,
                                       ec=INK, lw=0.7, zorder=5.0))        # wide-chord fan blade
            if up:
                out["rotors"]["fan"].append(fan)
                out["ogv"] = _row(ax, 0.78, 0.05, f_cowl, f_nin, False, sg)
            else:
                _row(ax, 0.78, 0.05, f_cowl, f_nin, False, sg)            # outlet guide vanes
            _outline(ax, [[0.15, 0.27], [0.29, 0.27], [0.25, 0.035], [0.19, 0.035]], sg)   # fan disk
        for i in range(CFM56_STAGES["lpc"]):
            x = 0.625 + 0.085 * i
            p = _row(ax, x, 0.030, f_hub, f_cas, True, sg)
            if up:
                out["rotors"]["lpc"].append(p)
            _row(ax, x + 0.042, 0.022, f_hub, f_cas, False, sg)
            _outline(ax, [[x - 0.012, float(f_hub(x - 0.012))], [x + 0.012, float(f_hub(x + 0.012))],
                          [x + 0.006, 0.255], [x - 0.006, 0.255]], sg)   # its disk, down to the drum
        _outline(ax, [[0.25, 0.235], [0.84, 0.235], [0.84, 0.255], [0.25, 0.255]], sg)   # booster drum, from the fan disk
        for i in range(CFM56_STAGES["hpc"]):
            x = 1.025 + 0.058 * i
            p = _row(ax, x, 0.022, f_hub, f_cas, True, sg)
            if up:
                out["rotors"]["hpc"].append(p)
            _row(ax, x + 0.029, 0.015, f_hub, f_cas, False, sg)
        ln = _liner(ax, 1.615, 1.80, 1.865, 0.228, 0.284, 0.222, 0.288, sg, r_case=float(f_cas(1.59)))
        _row(ax, 1.885, 0.020, f_hub, f_cas, False, sg)                   # high-pressure turbine: vanes, rotor
        p = _row(ax, 1.915, 0.024, f_hub, f_cas, True, sg)
        xd = _xs(1.03, 1.91, 60)                                          # high-pressure drum, HPC to HPT
        _outline(ax, np.r_[np.c_[xd, f_hub(xd) - 0.012], [[1.88, 0.095], [1.07, 0.095]]], sg)
        if up:
            out["rotors"]["hpt"].append(p)
            out["liner"] = ln
        for i in range(CFM56_STAGES["lpt"]):
            x = 2.00 + 0.11 * i
            _row(ax, x, 0.022, f_hub, f_cas, False, sg)
            p = _row(ax, x + 0.04, 0.026, f_hub, f_cas, True, sg)
            if up:
                out["rotors"]["lpt"].append(p)
            xr = x + 0.04                                                 # its disk, down to the drum
            _outline(ax, [[xr - 0.013, float(f_hub(xr - 0.013))], [xr + 0.013, float(f_hub(xr + 0.013))],
                          [xr + 0.006, 0.12], [xr - 0.006, 0.12]], sg)
        _outline(ax, [[2.03, 0.10], [2.38, 0.10], [2.38, 0.12], [2.03, 0.12]], sg)   # low-pressure turbine drum
        _outline(ax, [[2.34, 0.10], [2.38, 0.10], [2.38, 0.035], [2.34, 0.035]], sg)  # and its cone to the shaft
        out["lp_shaft"] = (0.22, 2.38, 0.0, 0.035)
        out["hp_shaft"] = (1.02, 1.92, 0.055, 0.095)
        _shaft(ax, *out["lp_shaft"], sg)                                  # low-pressure shaft
        _shaft(ax, *out["hp_shaft"], sg, hatch="xxxx")                    # high-pressure shaft (hollow)
    engine_centerline(ax, -0.70, 3.30)
    out["a_core"] = math.pi * float(f_cas(0.55) ** 2 - f_hub(0.55) ** 2)
    out["a_bypass"] = math.pi * float(f_nin(0.55) ** 2 - f_cowl(0.55) ** 2)
    out["bypass_exit"] = (1.38, 0.5 * (0.728 + float(f_cowl(1.38))))
    out["core_exit"] = (2.75, 0.5 * (0.20 + 0.34))
    return out


# --- the free-turbine turboprop: proportions after the Rolls-Royce AE 2100D2 (EASA type-certificate
# data sheet IM.E.040, issue 01, 2008: free turbine turboprop, 14-stage axial compressor, annular
# combustor, 2-stage gas generator turbine, 2-stage power turbine, front-mounted propeller
# reduction gearbox of 13.98:1; overall length 2.97 m). Only the length, the stage counts and the
# gear ratio are drawn to the data sheet; the radii are by eye. The gearbox and the propeller are
# drawn on the engine axis with the air inlet around them (on this engine family the gearbox sits
# above the axis and the air enters below it); the gearbox is sketched as a set of gears, and the
# propeller blades are cut short (the real propeller is several meters across).
AE2100_L = 2.97
AE2100_GEAR = 13.98
AE2100_STAGES = dict(compressor=14, compressor_turbine=2, power_turbine=2)


def draw_turboprop_section(ax, core_only=False, sides=(1, -1)):
    """A free-turbine turboprop in section, flow left to right (x in m from the propeller flange):
    pointed spinner and propeller blade roots, reduction gearbox (sketched as gears) in its housing,
    annular air inlet with a rounded lip, 14-stage compressor, annular combustor liner, 2-stage
    compressor turbine (the data sheet's gas generator turbine) on the compressor's hollow shaft,
    2-stage power turbine whose shaft runs forward inside it to the gearbox, exhaust duct. sides and
    core_only as for the turbofan (core_only leaves out the propeller, the gearbox and the inlet).
    Returns a dict: the contours, the exhaust wall patch, the rotor patches of the upper half by
    group, the liner, the shafts, the gearbox extent, the inlet gap, the propeller blade patches."""
    f_hub = contour([0.75, 1.00, 1.43, 1.48, 1.83, 1.88, 2.06, 2.10, 2.36, 2.62, AE2100_L],
                    [0.155, 0.146, 0.135, 0.120, 0.120, 0.130, 0.140, 0.150, 0.160, 0.130, 0.120])
    f_cas = contour([0.75, 1.00, 1.43, 1.48, 1.83, 1.88, 2.06, 2.10, 2.36, 2.62, AE2100_L],
                    [0.255, 0.215, 0.170, 0.205, 0.210, 0.182, 0.205, 0.222, 0.260, 0.290, 0.300])
    lip = dict(x_lip=0.375, r_lip=0.415, rho=0.025)                       # inlet: rounded lip, highlight at x = 0.375
    i_out = ([0.40, 0.50, 0.62, 0.75], [0.44, 0.435, 0.38, 0.285])
    i_in = ([0.40, 0.50, 0.62, 0.75], [0.39, 0.355, 0.30, 0.255])
    # inner body: pointed spinner to the propeller root, the gearbox housing, the hub and tail cone
    s = np.linspace(0.0, 1.0, 40)
    xs_sp = -0.22 + 0.22 * s
    rs_sp = 0.20 * (0.8 * s + 0.2 * (2.0 * s - s ** 2))
    f_house = contour([0.0, 0.10, 0.25, 0.40, 0.55, 0.75, 1.00, 1.43, 1.48, 1.83, 1.88, 2.06, 2.10, 2.36, 2.62, 2.78,
                       2.88],
                      [0.20, 0.265, 0.30, 0.285, 0.215, 0.155, 0.146, 0.135, 0.120, 0.120, 0.130, 0.140, 0.150, 0.160,
                       0.130, 0.060, 0.0])
    xt = _xs(0.0, 2.88, 400)
    xb, rb = np.r_[xs_sp, xt[1:]], np.r_[rs_sp, f_house(xt)[1:]]
    xx = _xs(0.75, AE2100_L, 240)
    out = dict(f_hub=f_hub, f_cas=f_cas, rotors={k: [] for k in AE2100_STAGES}, blades=[], body=[])
    gb = (0.13, 0.37)                                                     # the gearbox: x extent of its gear set
    for sg in sides:
        up = sg == 1
        if not core_only:
            p = _lip_wall(ax, lip["x_lip"], lip["r_lip"], lip["rho"], *i_out, *i_in, sg)
            if up:
                out["inlet_wall"] = p
        p = _wall(ax, xx, f_cas(xx), f_cas(xx) + 0.03, sg)
        if up:
            out["duct_wall"] = p
        out["body"].append(_body(ax, xb, rb, sg, z=3.6))
        for i in range(AE2100_STAGES["compressor"]):
            x = 0.775 + 0.0465 * i
            p = _row(ax, x, 0.018, f_hub, f_cas, True, sg)
            if up:
                out["rotors"]["compressor"].append(p)
            _row(ax, x + 0.022, 0.012, f_hub, f_cas, False, sg)
        ln = _liner(ax, 1.515, 1.78, 1.865, 0.140, 0.190, 0.133, 0.176, sg, r_case=float(f_cas(1.49)))
        if up:
            out["liner"] = ln
        for i in range(AE2100_STAGES["compressor_turbine"]):
            x = 1.895 + 0.075 * i
            _row(ax, x, 0.022, f_hub, f_cas, False, sg)
            p = _row(ax, x + 0.032, 0.026, f_hub, f_cas, True, sg)
            if up:
                out["rotors"]["compressor_turbine"].append(p)
        for i in range(AE2100_STAGES["power_turbine"]):
            x = 2.13 + 0.10 * i
            _row(ax, x, 0.026, f_hub, f_cas, False, sg)
            p = _row(ax, x + 0.040, 0.032, f_hub, f_cas, True, sg)
            if up:
                out["rotors"]["power_turbine"].append(p)
        out["pt_shaft"] = (gb[1] - 0.01, 2.30, 0.0, 0.026)
        out["c_shaft"] = (0.78, 1.97, 0.042, 0.070)
        _shaft(ax, *out["pt_shaft"], sg)                                  # power-turbine shaft, to the gearbox
        _shaft(ax, *out["c_shaft"], sg, hatch="xxxx")                     # compressor shaft (hollow)
        for x0, r0, x1, r1 in ((0.78, float(f_hub(0.78)), 0.80, 0.070), (1.97, 0.070, 1.95, float(f_hub(1.95))),
                               (2.21, 0.026, 2.18, float(f_hub(2.18))), (2.30, 0.026, 2.27, float(f_hub(2.27)))):
            ax.plot([x0, x1], [sg * r0, sg * r1], color=INK, lw=SHAFT_LW, zorder=4.5)
        if not core_only:
            # propeller blade root, cut short with a break line at r = 0.70
            bx = np.array([-0.09, 0.09, 0.075, -0.075])
            by = np.array([0.20, 0.20, 0.70, 0.70])
            p = ax.add_patch(Polygon(np.c_[bx, sg * by], closed=True, fc=ROTOR_FILL, ec=INK, lw=0.8, zorder=3.4))
            out["blades"].append(p)
            zz = np.linspace(-0.11, 0.11, 7)
            ax.plot(zz, sg * (0.70 + 0.02 * np.array([0, 1, -1, 1, -1, 1, 0])), color=INK, lw=0.9, zorder=3.5)
            _shaft(ax, -0.12, gb[0] + 0.01, 0.0, 0.045, sg, z=4.4)        # propeller shaft
    if not core_only:
        # reduction gearbox, sketched as a gear set on the axis: an outer ring gear, a small sun gear on
        # the power-turbine shaft, and three planet gears between them (pitch circles)
        cx, rr = 0.5 * (gb[0] + gb[1]), 0.5 * (gb[1] - gb[0])
        gears = [(cx, 0.0, rr), (cx, 0.0, 0.034)]
        for a in (90.0, 210.0, 330.0):
            gears.append((cx + 0.077 * math.cos(math.radians(a)), 0.077 * math.sin(math.radians(a)), 0.040))
        for gx, gy, gr in gears:
            ax.add_patch(Circle((gx, gy), gr, fc="white" if gr == rr else SURFACE_FILL, ec=INK, lw=0.9, zorder=4.6 if gr == rr else 4.7))
        out["gears"] = gears
    engine_centerline(ax, -0.36, AE2100_L + 0.08)
    out["gearbox"] = (gb[0], gb[1], 0.0, 0.5 * (gb[1] - gb[0]))
    out["length"] = float(xx[-1])
    out["inlet_gap"] = float(contour(*i_in)(0.45) - f_house(0.45))       # open annulus between lip and housing
    return out
