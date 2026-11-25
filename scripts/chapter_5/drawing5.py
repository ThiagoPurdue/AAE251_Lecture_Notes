"""Drawing helpers for Chapter 5, Aircraft Performance and Propulsion.

Provides reusable line-art schematics on equal-aspect axes:
  - `aircraft_profile_fbd`: the Boeing 737-800 side outline from chapter_1.aircraft (scaled,
    cleaned of landing gear, rotated nose-right and pitched by theta) for level and climbing
    flight free-body diagrams.
  - `draw_turbojet`, `draw_turbofan`, `draw_turboprop`, `draw_ramjet`: crisp engineering
    cutaway schematics of the four main air-breathing engine types, built with opaque() and
    on_part() so the layout gate checks every label and leader cleanly.
"""
import math

import numpy as np
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch

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


# ===================================================================== engine cutaway helpers
def _blade_row(ax, x, r_in, r_out, w, host, zorder=4.2, fc="#D8D8D8"):
    """One upper and one lower axial compressor/turbine blade row drawn on `host`."""
    for sgn in (1.0, -1.0):
        y0 = sgn * r_in
        h = sgn * (r_out - r_in)
        p = Rectangle((x - 0.5 * w, min(y0, y0 + h)), w, abs(h), fc=fc, ec=INK, lw=LW_FINE, zorder=zorder)
        ax.add_patch(p)
        on_part(p, host)


def _flame_chamber(ax, x0, x1, r_in, r_out, host, zorder=4.2):
    """Upper and lower annular combustor cans with clean schematic flame tongues."""
    for sgn in (1.0, -1.0):
        y_lo = min(sgn * r_in, sgn * r_out)
        h = abs(r_out - r_in)
        can = FancyBboxPatch((x0, y_lo), x1 - x0, h, boxstyle="round,pad=0.0,rounding_size=0.06",
                             fc=HIGHLIGHT, ec=INK, lw=LW_DETAIL, zorder=zorder)
        ax.add_patch(can)
        on_part(can, host)
        # two clean flame waves inside the combustor (reads in grayscale)
        ym = 0.5 * (y_lo + y_lo + h)
        amp = 0.22 * h
        xf = np.linspace(x0 + 0.14 * (x1 - x0), x1 - 0.12 * (x1 - x0), 17)
        yf = ym + amp * np.sin(np.linspace(0, 3 * math.pi, 17))
        ln = ax.plot(xf, yf, color=INK, lw=LW_FINE, zorder=zorder + 0.1)[0]
        on_part(ln, host)


def draw_turbojet(ax, origin=(0.0, 0.0), scale=1.0, zorder=3.0):
    """Engineering cutaway of a single-spool axial turbojet, flow left to right.
    Total length 5.4 * scale, max radius 0.72 * scale. Returns dict of part anchor points and casing patch."""
    ox, oy = origin
    s = scale
    # Outer casing (upper + lower symmetric duct): inlet (0..0.9), compressor (0.9..2.2),
    # combustor (2.2..3.3), turbine (3.3..4.0), nozzle (4.0..5.4)
    xs = np.array([0.0, 0.9, 2.2, 3.3, 4.0, 5.4]) * s + ox
    rs = np.array([0.52, 0.68, 0.56, 0.62, 0.58, 0.34]) * s
    top = np.c_[xs, oy + rs]
    bot = np.c_[xs[::-1], oy - rs[::-1]]
    casing = Polygon(np.r_[top, bot], closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE,
                     joinstyle="round", zorder=zorder)
    ax.add_patch(opaque(casing))

    # Center shaft + nose cone + exhaust plug
    shaft_x = np.array([0.35, 0.85, 2.2, 3.3, 4.0, 4.75]) * s + ox
    shaft_r = np.array([0.0, 0.18, 0.25, 0.16, 0.22, 0.0]) * s
    shaft_poly = np.r_[np.c_[shaft_x, oy + shaft_r], np.c_[shaft_x[::-1], oy - shaft_r[::-1]]]
    shaft = Polygon(shaft_poly, closed=True, fc="#EFEFEF", ec=INK, lw=LW_DETAIL, zorder=zorder + 0.5)
    ax.add_patch(shaft)
    on_part(shaft, casing)

    # Centerline dashed
    cl = ax.plot([ox - 0.15 * s, ox + 5.55 * s], [oy, oy], **line_kw("reference"), zorder=zorder + 0.1)[0]
    on_part(cl, casing)

    # Compressor rows (5 converging stages)
    for k, frac in enumerate(np.linspace(0.0, 1.0, 5)):
        xc = (1.02 + frac * 1.04) * s + ox
        rin = (0.19 + 0.06 * frac) * s
        rout = (0.65 - 0.08 * frac) * s
        _blade_row(ax, xc, rin, rout, 0.10 * s, casing, zorder=zorder + 0.6, fc="#DCDCDC")

    # Combustor (annular upper & lower)
    _flame_chamber(ax, ox + 2.30 * s, ox + 3.20 * s, 0.22 * s, 0.54 * s, casing, zorder=zorder + 0.6)

    # Turbine rows (2 stages)
    for frac in (0.0, 1.0):
        xt = (3.44 + frac * 0.34) * s + ox
        rin = (0.18 + 0.03 * frac) * s
        rout = (0.58 - 0.02 * frac) * s
        _blade_row(ax, xt, rin, rout, 0.11 * s, casing, zorder=zorder + 0.6, fc="#B8B8B8")

    return dict(
        casing=casing,
        inlet=(ox + 0.45 * s, oy + 0.50 * s),
        compressor=(ox + 1.54 * s, oy + 0.48 * s),
        combustor=(ox + 2.75 * s, oy + 0.44 * s),
        turbine=(ox + 3.62 * s, oy + 0.45 * s),
        nozzle=(ox + 4.85 * s, oy + 0.32 * s),
        shaft=(ox + 2.75 * s, oy),
        x_stations=xs,
        top_r=rs,
        extent=(ox, ox + 5.4 * s, oy - 0.72 * s, oy + 0.72 * s),
    )


def draw_turbofan(ax, origin=(0.0, 0.0), scale=1.0, zorder=3.0):
    """Engineering cutaway of a high-bypass turbofan: large front fan, outer bypass duct, and inner core."""
    ox, oy = origin
    s = scale
    # Outer bypass nacelle (0.0 to 3.1)
    bx = np.array([0.0, 0.45, 2.2, 3.1]) * s + ox
    br = np.array([0.82, 0.94, 0.90, 0.76]) * s
    nac = Polygon(np.r_[np.c_[bx, oy + br], np.c_[bx[::-1], oy - br[::-1]]],
                  closed=True, fc=GAS_FILL, ec=INK, lw=LW_OUTLINE, joinstyle="round", zorder=zorder)
    ax.add_patch(opaque(nac))

    # Inner core cowl (0.85 to 4.9)
    cx = np.array([0.85, 1.30, 2.30, 3.30, 4.00, 4.90]) * s + ox
    cr = np.array([0.46, 0.46, 0.44, 0.48, 0.44, 0.24]) * s
    core = Polygon(np.r_[np.c_[cx, oy + cr], np.c_[cx[::-1], oy - cr[::-1]]],
                   closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE * 0.9, joinstyle="round", zorder=zorder + 0.3)
    ax.add_patch(opaque(core))
    on_part(core, nac)

    # Center spinner + shaft + exhaust plug
    sx = np.array([0.12, 0.55, 2.30, 3.30, 4.00, 4.65]) * s + ox
    sr = np.array([0.0, 0.18, 0.20, 0.14, 0.17, 0.0]) * s
    shaft = Polygon(np.r_[np.c_[sx, oy + sr], np.c_[sx[::-1], oy - sr[::-1]]],
                    closed=True, fc="#EFEFEF", ec=INK, lw=LW_DETAIL, zorder=zorder + 0.5)
    ax.add_patch(shaft)
    on_part(shaft, nac)

    # Large front fan blades
    _blade_row(ax, ox + 0.55 * s, 0.18 * s, 0.89 * s, 0.18 * s, nac, zorder=zorder + 0.65, fc="#CCCCCC")

    # Core compressor (4 stages)
    for frac in np.linspace(0.0, 1.0, 4):
        xc = (1.22 + frac * 0.88) * s + ox
        _blade_row(ax, xc, 0.19 * s, 0.42 * s, 0.09 * s, core, zorder=zorder + 0.6, fc="#DCDCDC")
    # Combustor
    _flame_chamber(ax, ox + 2.38 * s, ox + 3.18 * s, 0.18 * s, 0.42 * s, core, zorder=zorder + 0.6)
    # Turbine (2 stages)
    for frac in (0.0, 1.0):
        xt = (3.42 + frac * 0.30) * s + ox
        _blade_row(ax, xt, 0.16 * s, 0.42 * s, 0.10 * s, core, zorder=zorder + 0.6, fc="#B8B8B8")

    return dict(
        casing=nac, core=core,
        fan=(ox + 0.55 * s, oy + 0.72 * s),
        bypass=(ox + 1.85 * s, oy + 0.68 * s),
        compressor=(ox + 1.65 * s, oy + 0.32 * s),
        combustor=(ox + 2.78 * s, oy + 0.31 * s),
        turbine=(ox + 3.57 * s, oy + 0.31 * s),
        nozzle=(ox + 4.45 * s, oy + 0.22 * s),
        extent=(ox, ox + 4.9 * s, oy - 0.94 * s, oy + 0.94 * s),
    )


def draw_turboprop(ax, origin=(0.0, 0.0), scale=1.0, zorder=3.0):
    """Engineering cutaway of a turboprop: front propeller, spinner, reduction gearbox, core, exhaust."""
    ox, oy = origin
    s = scale
    # Core nacelle (0.95 to 4.9)
    cx = np.array([0.95, 1.40, 2.35, 3.30, 4.10, 4.90]) * s + ox
    cr = np.array([0.44, 0.50, 0.48, 0.52, 0.46, 0.28]) * s
    core = Polygon(np.r_[np.c_[cx, oy + cr], np.c_[cx[::-1], oy - cr[::-1]]],
                   closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, joinstyle="round", zorder=zorder)
    ax.add_patch(opaque(core))

    # Spinner (nose ahead of propeller)
    sp_x = np.array([0.05, 0.35, 0.65, 0.95]) * s + ox
    sp_r = np.array([0.0, 0.18, 0.26, 0.30]) * s
    spinner = Polygon(np.r_[np.c_[sp_x, oy + sp_r], np.c_[sp_x[::-1], oy - sp_r[::-1]]],
                      closed=True, fc="#EFEFEF", ec=INK, lw=LW_OUTLINE * 0.9, zorder=zorder + 0.4)
    ax.add_patch(opaque(spinner))

    # Propeller blades (tall, slim airfoil-like paddles above & below spinner)
    for sgn in (1.0, -1.0):
        px = np.array([0.36, 0.46, 0.55, 0.49, 0.39]) * s + ox
        py = oy + sgn * np.array([0.22, 0.95, 0.95, 0.55, 0.22]) * s
        bl = Polygon(np.c_[px, py], closed=True, fc="#D0D0D0", ec=INK, lw=LW_DETAIL, zorder=zorder + 0.6)
        ax.add_patch(opaque(bl))

    # Reduction gearbox box inside front of nacelle
    gb = Rectangle((ox + 0.95 * s, oy - 0.22 * s), 0.45 * s, 0.44 * s,
                   fc=SURFACE_FILL, ec=INK, lw=LW_DETAIL, hatch="///", zorder=zorder + 0.6)
    ax.add_patch(gb)
    on_part(gb, core)

    # Shaft from gearbox to turbine
    sh = Rectangle((ox + 1.40 * s, oy - 0.08 * s), 2.65 * s, 0.16 * s,
                   fc="#EFEFEF", ec=INK, lw=LW_DETAIL, zorder=zorder + 0.5)
    ax.add_patch(sh)
    on_part(sh, core)

    # Compressor (3 stages)
    for frac in np.linspace(0.0, 1.0, 3):
        xc = (1.62 + frac * 0.56) * s + ox
        _blade_row(ax, xc, 0.11 * s, 0.44 * s, 0.09 * s, core, zorder=zorder + 0.6, fc="#DCDCDC")
    # Combustor
    _flame_chamber(ax, ox + 2.40 * s, ox + 3.18 * s, 0.13 * s, 0.44 * s, core, zorder=zorder + 0.6)
    # Multi-stage power turbine (3 stages — extracts almost all energy for propeller!)
    for frac in np.linspace(0.0, 1.0, 3):
        xt = (3.40 + frac * 0.48) * s + ox
        _blade_row(ax, xt, 0.11 * s, 0.44 * s, 0.10 * s, core, zorder=zorder + 0.6, fc="#B8B8B8")

    return dict(
        casing=core,
        propeller=(ox + 0.46 * s, oy + 0.78 * s),
        gearbox=(ox + 1.18 * s, oy + 0.12 * s),
        compressor=(ox + 1.90 * s, oy + 0.32 * s),
        combustor=(ox + 2.79 * s, oy + 0.30 * s),
        turbine=(ox + 3.64 * s, oy + 0.32 * s),
        nozzle=(ox + 4.50 * s, oy + 0.22 * s),
        extent=(ox, ox + 4.9 * s, oy - 0.96 * s, oy + 0.96 * s),
    )


def draw_ramjet(ax, origin=(0.0, 0.0), scale=1.0, zorder=3.0):
    """Engineering cutaway of a ramjet: supersonic inlet spike/diffuser, fuel injectors/flameholder,
    open combustor, converging-diverging nozzle (no rotating compressor or turbine)."""
    ox, oy = origin
    s = scale
    # Outer cowl (0.55 to 4.9): converging-diverging nozzle at exit
    rx = np.array([0.55, 1.40, 2.30, 3.55, 4.10, 4.90]) * s + ox
    rr = np.array([0.46, 0.54, 0.62, 0.62, 0.36, 0.56]) * s
    cowl = Polygon(np.r_[np.c_[rx, oy + rr], np.c_[rx[::-1], oy - rr[::-1]]],
                   closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, joinstyle="round", zorder=zorder)
    ax.add_patch(opaque(cowl))

    # Supersonic inlet centerbody (spike)
    sp_x = np.array([0.0, 1.15, 1.95, 1.15]) * s + ox
    sp_y = np.array([0.0, 0.28, 0.0, -0.28]) * s + oy
    spike = Polygon(np.c_[sp_x, sp_y], closed=True, fc="#E5E5E5", ec=INK, lw=LW_OUTLINE * 0.9, zorder=zorder + 0.5)
    ax.add_patch(opaque(spike))
    on_part(spike, cowl)

    # Fuel injectors and V-gutter flameholders
    for y_off in (-0.30, 0.0, 0.30):
        # V-gutter pointing upstream
        vx = np.array([2.35, 2.15, 2.35]) * s + ox
        vy = oy + (y_off + np.array([0.09, 0.0, -0.09])) * s
        ln = ax.plot(vx, vy, color=INK, lw=LW_DETAIL + 0.3, zorder=zorder + 0.6)[0]
        on_part(ln, cowl)
        # injector dot just ahead
        pt_m = ax.plot([ox + 2.02 * s], [oy + y_off * s], "o", ms=3.5, color=INK, zorder=zorder + 0.7)[0]
        on_part(pt_m, cowl)

    # Open combustion zone (light gold fill + clean flame waves)
    comb = FancyBboxPatch((ox + 2.40 * s, oy - 0.52 * s), 1.12 * s, 1.04 * s,
                          boxstyle="round,pad=0.0,rounding_size=0.08",
                          fc=HIGHLIGHT, ec="none", zorder=zorder + 0.2)
    ax.add_patch(comb)
    on_part(comb, cowl)
    for y_off in (-0.28, 0.0, 0.28):
        xf = np.linspace(ox + 2.46 * s, ox + 3.45 * s, 21)
        yf = oy + y_off * s + 0.06 * s * np.sin(np.linspace(0, 4 * math.pi, 21))
        ln = ax.plot(xf, yf, color=INK, lw=LW_FINE, zorder=zorder + 0.4)[0]
        on_part(ln, cowl)

    return dict(
        casing=cowl,
        inlet=(ox + 0.65 * s, oy + 0.22 * s),
        injectors=(ox + 2.15 * s, oy + 0.34 * s),
        combustor=(ox + 2.95 * s, oy + 0.36 * s),
        nozzle=(ox + 4.42 * s, oy + 0.34 * s),
        extent=(ox, ox + 4.9 * s, oy - 0.64 * s, oy + 0.64 * s),
    )
