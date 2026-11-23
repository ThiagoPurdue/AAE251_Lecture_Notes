"""Low-speed wind tunnels (3.1 Wind Tunnels): the test-section speed from a pressure difference,
the manometer, the speed and pressure along the tunnel axis, the Mach check, and the outlines of
a closed-circuit (Gottingen) tunnel in plan view and an open-circuit (Eiffel) tunnel in side view.

Stations (as on page 3.1): 1 settling chamber (reservoir), 2 test section, 3 diffuser exit;
contraction ratio A1/A2.

Sources (each opened):
  - Gentry, G. L., Jr., Quinto, P. F., Gatlin, G. M., and Applin, Z. T., "The Langley 14- by
    22-Foot Subsonic Tunnel: Description, Flow Characteristics, and Guide for Users", NASA
    TP-3008, 1990: Figure 2 (plan of the circuit: 320 ft between the corner centers, 65 ft
    between the leg centerlines; four corners with turning vanes; honeycomb and four screens in
    the settling chamber; fan and its fairing in the return leg) and Table 1 (contraction 60 ft
    long, area ratio 8.99; test section 50 ft; first diffuser 142.5 ft, area ratio 2.67; third
    diffuser 54.33 ft; fan section 45.5 ft; fourth diffuser 170 ft). Its first diffuser opens
    from 14.5 x 21.75 ft to 27 x 31.5 ft over 142.5 ft: about 2.5 deg per wall. The closed-circuit
    outline follows these numbers; the plan widths of the corners and the return leg were read
    off Figure 2. Page 3.1 captions the outline "typical proportions".
  - Bell, J. H., and Mehta, R. D., "Contraction Design for Small Low-Speed Wind Tunnels", NASA
    CR-177488, 1988: contraction ratios of 6 to 10 suit small low-speed tunnels; the fifth-order
    polynomial wall Y = H_i - (H_i - H_e)(6 X'^5 - 15 X'^4 + 10 X'^3), X' = x/L, which they
    selected; a length of 0.89 inlet heights for their ratio-7.7 contraction.
  - NASA Glenn Research Center, "Open Return Wind Tunnel", "Closed Return Wind Tunnel" and "Wind
    Tunnel Parts" (Beginner's Guide to Aeronautics, n.d.): the parts and their names (bellmouth,
    flow straighteners, test section, diffuser, fan and drive motor, turning vanes), the
    Eiffel and Gottingen names, and the advantages and drawbacks of each.
  The open-circuit outline is not one particular tunnel: contraction ratio 7.5 by default (page
  3.1's tunnel) and length 0.89
  inlet heights (Bell and Mehta), diffuser walls at 2.5 deg (TP-3008), a test section two
  heights long; its caption says "typical proportions".

Run this file for its unit checks:  python3 -B scripts/chapter_3/tunnel.py
"""
import math
import sys as _sys
from pathlib import Path as _Path

import numpy as np

if __name__ == "__main__":
    _sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from chapter_3.aero import G0 as G  # noqa: E402  (9.81 m/s^2, the value used throughout the course)
RHO_WATER = 1000.0         # kg/m^3
RHO_MERCURY = 13600.0      # kg/m^3
MACH_INCOMPRESSIBLE = 0.3  # the limit for treating the flow as incompressible (page 1.5)


# ===================================================================== speed and pressure
def test_section_speed(dp, rho, ratio):
    """Test-section speed from p1 - p2 and the contraction ratio A1/A2:
    V2 = sqrt(2 (p1 - p2) / (rho [1 - (A2/A1)^2])), rho of the air. Example: test_section_speed(1500.0, 1.225, 7.5) -> 49.93"""
    return math.sqrt(2.0 * dp / (rho * (1.0 - 1.0 / ratio ** 2)))


def pressure_difference(V2, rho, ratio):
    """p1 - p2 that gives the test-section speed V2. Example: pressure_difference(50.0, 1.225, 7.5) -> 1,504"""
    return 0.5 * rho * V2 ** 2 * (1.0 - 1.0 / ratio ** 2)


def manometer_dp(dh, rho_liquid=RHO_WATER, g=G):
    """p1 - p2 = rho_l g dh (rho of the manometer liquid). Example: manometer_dp(0.164) -> 1,609"""
    return rho_liquid * g * dh


def manometer_dh(dp, rho_liquid=RHO_WATER, g=G):
    """Height difference of the manometer liquid for p1 - p2. Example: manometer_dh(1608.8) -> 0.1640"""
    return dp / (rho_liquid * g)


def settling_speed(V2, ratio):
    """V1 = V2 A2/A1. Example: settling_speed(50.0, 7.5) -> 6.667"""
    return V2 / ratio


def mach_check(V, T, gamma=1.4, R=287.0):
    """(Mach number, True when below 0.3). Example: mach_check(50.0, 288.16) -> (0.1469, True)"""
    M = V / math.sqrt(gamma * R * T)
    return M, M < MACH_INCOMPRESSIBLE


def axis_flow(x, A, A2, V2, rho, p1, x_loss=None, loss=0.0):
    """Speed and static pressure along the tunnel axis for the area A(x) (arrays), one-dimensional
    incompressible flow: V = V2 A2/A; p = p0 - rho V^2/2, with p0 the reservoir total pressure.
    Downstream of x_loss[0] the total pressure falls linearly to p0 - loss (Pa) at x_loss[1]
    (friction on the walls and the drag of the model: the diffuser does not recover all of it).
    Returns (V, p, p0). Example: axis_flow(x, A, 1.0, 50.0, 1.225, 101325.0, (5.0, 12.0), 120.0)"""
    x, A = np.asarray(x, float), np.asarray(A, float)
    V = V2 * A2 / A
    V1 = V2 * A2 / A[0]
    p00 = p1 + 0.5 * rho * V1 ** 2
    p0 = np.full_like(x, p00)
    if x_loss is not None and loss:
        f = np.clip((x - x_loss[0]) / (x_loss[1] - x_loss[0]), 0.0, 1.0)
        p0 = p00 - loss * f
    return V, p0 - 0.5 * rho * V ** 2, p0


# ===================================================================== outline helpers
def contraction_wall(Hi, He, L, n=60):
    """Half-height (or half-width) along a contraction of length L from Hi to He, the fifth-order
    polynomial of Bell and Mehta (1988): zero slope and zero curvature at both ends. Returns (x, h).
    Example: contraction_wall(3.0, 1.0, 2.67)[1][30] -> 2.000"""
    x = np.linspace(0.0, L, n)
    s = x / L
    return x, Hi - (Hi - He) * (6 * s ** 5 - 15 * s ** 4 + 10 * s ** 3)


class TunnelPart:
    """One part of a tunnel outline: `name`, `poly` (closed outline of the air space of the part,
    data units), `walls` (open polylines, the solid walls, drawn heavy), `joints` (the faces where
    it meets its neighbors, drawn thin), `inside` (a point for a leader), `kind` ("duct", "corner",
    "honeycomb", "screen", "vanes", "model", "support", "fan", "hub", "lip"), `lines` (open
    polylines drawn on the part: screens, vanes, fan blades), `host` (the duct part it sits in:
    a leader that ends inside the host may cross it)."""

    def __init__(self, name, poly, walls=(), joints=(), inside=None, kind="duct", lines=(), host=None):
        self.name, self.kind, self.host = name, kind, host
        self.poly = np.asarray(poly, float)
        self.walls = [np.asarray(w, float) for w in walls]
        self.joints = [np.asarray(j, float) for j in joints]
        self.lines = [np.asarray(l, float) for l in lines]
        self.inside = np.asarray(inside if inside is not None else self.poly.mean(axis=0), float)

    def __repr__(self):
        return f"TunnelPart({self.name!r}, {self.kind})"


class Tunnel(dict):
    """A dict name -> TunnelPart with attributes: `stations` {1: (p, q), 2: ..., 3: ...} (the two
    wall points of each station's cross-section line), `flow` (list of (p0, p1) where a flow
    arrow reads well, inside the ducts), `view` ("plan" or "side"), `unit` ("ft" or "m"),
    `ratio` (contraction ratio of the outline), `extent` (x0, x1, y0, y1)."""


def tunnel_subset(T, names):
    """A Tunnel holding only the named parts of T (in that order), with T's stations, flow
    places, model, view, unit, ratio and extent: draw part of a tunnel, for example the front
    from the bellmouth to the test section. Example: F = tunnel_subset(T, ("contraction", "test_section"))"""
    F = Tunnel()
    for n in names:
        F[n] = T[n]
    for a in ("model_parts", "stations", "flow", "view", "unit", "ratio", "extent"):
        if hasattr(T, a):
            setattr(F, a, getattr(T, a))
    return F


def _rect(x0, x1, y0, y1):
    return np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def _corner(name, c, w, turn, nv=8, min_chord=0.0):
    """A square mitred corner of side w centered at c, turning the flow by 90 deg. turn = (d_in,
    d_out): unit vectors of the flow entering and leaving. Vanes: a cascade of nv quarter arcs
    centered on the diagonal from the outer to the inner corner, each tangent to d_in at its start
    and d_out at its end, chord one eighth of the duct width (the same look in every corner; the
    spacing grows with the corner), but at least min_chord: a small corner then gets fewer,
    larger vanes (nv scaled by the ratio of the two chords), so each still reads as an arc."""
    c = np.asarray(c, float)
    din, dout = np.asarray(turn[0], float), np.asarray(turn[1], float)
    h = 0.5 * w
    inner = c - din * h + dout * h          # where the inner walls meet
    outer = c + din * h - dout * h
    poly = _rect(c[0] - h, c[0] + h, c[1] - h, c[1] + h)
    # the two solid walls are the outer ones: the side facing the oncoming flow (+din) and the
    # side behind the leaving flow (-dout)
    walls = [np.array([outer + dout * w, outer]), np.array([outer, outer - din * w])]
    vanes = []
    chord = max(w / 8.0, min_chord)
    if chord > w / 8.0:
        nv = max(4, int(round(nv * (w / 8.0) / chord)))
    t_end = 0.10 * chord / (w / 8.0)       # larger vanes stand further from the corners of the duct
    ts = np.linspace(t_end, 1.0 - t_end, nv)
    r = chord / math.sqrt(2.0)              # a quarter arc of radius r has a chord of r sqrt(2)
    u0, u1 = -dout, din                 # from a vane's center to its start and to its end
    th0, th1 = math.atan2(u0[1], u0[0]), math.atan2(u1[1], u1[0])
    sweep = (th1 - th0 + math.pi) % (2 * math.pi) - math.pi
    m = (u0 + u1) / np.hypot(*(u0 + u1))
    for t in ts:
        P = outer + t * (inner - outer)     # the middle of the vane lies on the diagonal
        cen = P - r * m
        th = np.linspace(th0, th0 + sweep, 16)
        vanes.append(np.c_[cen[0] + r * np.cos(th), cen[1] + r * np.sin(th)])
    inside = c + 0.28 * (outer - c)
    return TunnelPart(name, poly, walls=walls, inside=inside, kind="corner", lines=vanes), inner, outer


def closed_circuit_plan():
    """Closed-circuit (Gottingen) tunnel in plan view, seen from above, flow counterclockwise:
    the test leg along y = 0 (flow to the right), the return leg along y = 65 ft (flow to the
    left). Units: ft. Parts: corner_1 .. corner_4 (turning vanes as lines), settling_chamber
    (with honeycomb and screen_1 .. screen_4 as separate parts), contraction, test_section,
    model (plan outline of a jet transport, span 0.55 of the test-section width), support (a
    sting from the tail to a strut fairing), diffuser (the first diffuser), crossleg (the
    second diffuser, between corners 1 and 2), return_diffuser (third), fan_section with fan
    and hub, return_leg (the fourth diffuser, widening to corner 3). Proportions after the
    Langley 14- by 22-Foot Subsonic Tunnel (see the header). Example: T = closed_circuit_plan()"""
    from chapter_1.aircraft import aircraft_top, B738
    T = Tunnel()
    Wb, Ws, Wt = 65.0, 32.0, 21.75          # big corners and settling chamber; small corners; test section
    yr = 65.0                              # return-leg centerline
    xL, xR = 0.0, 320.0                    # corner centers
    x_sc0, x_c0, x_c1 = 0.5 * Wb, 0.5 * Wb + 25.0, 0.5 * Wb + 85.0
    x_t1 = x_c1 + 50.0
    x_d1 = xR - 0.5 * Ws
    # corners (flow: down -> right at corner 4, right -> up at 1, up -> left at 2, left -> down at 3)
    c4, _, _ = _corner("corner_4", (xL, 0.0), Wb, ((0, -1), (1, 0)))
    vmin = 6.0                             # ft: the smallest vane chord (about 6 pt in the plan figure)
    c1, _, _ = _corner("corner_1", (xR, 0.0), Ws, ((1, 0), (0, 1)), min_chord=vmin)
    c2, _, _ = _corner("corner_2", (xR, yr), Ws, ((0, 1), (-1, 0)), min_chord=vmin)
    c3, _, _ = _corner("corner_3", (xL, yr), Wb, ((-1, 0), (0, -1)))
    for c in (c1, c2, c3, c4):
        T[c.name] = c
    h = 0.5 * Wb
    T["settling_chamber"] = TunnelPart("settling_chamber", _rect(x_sc0, x_c0, -h, h),
                                       walls=[[(x_sc0, h), (x_c0, h)], [(x_sc0, -h), (x_c0, -h)]],
                                       joints=[[(x_sc0, -h), (x_sc0, h)], [(x_c0, -h), (x_c0, h)]],
                                       inside=(x_sc0 + 8.5, -0.75 * h))
    T["honeycomb"] = TunnelPart("honeycomb", _rect(x_sc0 + 3.0, x_sc0 + 7.0, -h, h), kind="honeycomb", host="settling_chamber",
                                inside=(x_sc0 + 5.0, -0.75 * h))
    for i, xs in enumerate((x_sc0 + 11.0, x_sc0 + 14.0, x_sc0 + 17.0, x_sc0 + 20.0)):
        T[f"screen_{i + 1}"] = TunnelPart(f"screen_{i + 1}", _rect(xs - 0.3, xs + 0.3, -h, h), kind="screen", host="settling_chamber",
                                          lines=[[(xs, -h), (xs, h)]], inside=(xs, -0.75 * h))
    xc, hc = contraction_wall(h, 0.5 * Wt, x_c1 - x_c0)
    xc = xc + x_c0
    up, lo = np.c_[xc, hc], np.c_[xc, -hc]
    T["contraction"] = TunnelPart("contraction", np.r_[lo, up[::-1]], walls=[up, lo],
                                  joints=[[(x_c0, -h), (x_c0, h)], [(x_c1, -0.5 * Wt), (x_c1, 0.5 * Wt)]],
                                  inside=(x_c0 + 40.0, -0.5 * Wt))
    ht = 0.5 * Wt
    T["test_section"] = TunnelPart("test_section", _rect(x_c1, x_t1, -ht, ht),
                                   walls=[[(x_c1, ht), (x_t1, ht)], [(x_c1, -ht), (x_t1, -ht)]],
                                   joints=[[(x_c1, -ht), (x_c1, ht)], [(x_t1, -ht), (x_t1, ht)]],
                                   inside=(x_t1 - 4.0, -0.6 * ht))
    hd = 0.5 * Ws
    T["diffuser"] = TunnelPart("diffuser", [(x_t1, -ht), (x_d1, -hd), (x_d1, hd), (x_t1, ht)],
                               walls=[[(x_t1, ht), (x_d1, hd)], [(x_t1, -ht), (x_d1, -hd)]],
                               joints=[[(x_d1, -hd), (x_d1, hd)]], inside=(0.5 * (x_t1 + x_d1), -0.5 * ht))
    # right crossleg between corners 1 and 2
    T["crossleg"] = TunnelPart("crossleg", _rect(xR - hd, xR + hd, hd, yr - hd),
                               walls=[[(xR - hd, hd), (xR - hd, yr - hd)], [(xR + hd, hd), (xR + hd, yr - hd)]],
                               joints=[[(xR - hd, hd), (xR + hd, hd)], [(xR - hd, yr - hd), (xR + hd, yr - hd)]],
                               inside=(xR + 0.3 * hd, 0.5 * yr))
    # return leg: third diffuser, fan section, fourth diffuser
    x3a, x3b, x4 = x_d1, x_d1 - 54.0, x_d1 - 54.0 - 45.5
    hf = 20.0
    T["return_diffuser"] = TunnelPart("return_diffuser", [(x3a, yr - hd), (x3a, yr + hd), (x3b, yr + hf), (x3b, yr - hf)],
                                      walls=[[(x3a, yr + hd), (x3b, yr + hf)], [(x3a, yr - hd), (x3b, yr - hf)]],
                                      joints=[[(x3a, yr - hd), (x3a, yr + hd)], [(x3b, yr - hf), (x3b, yr + hf)]],
                                      inside=(0.5 * (x3a + x3b), yr + 0.5 * hd))
    T["fan_section"] = TunnelPart("fan_section", _rect(x4, x3b, yr - hf, yr + hf),
                                  walls=[[(x4, yr + hf), (x3b, yr + hf)], [(x4, yr - hf), (x3b, yr - hf)]],
                                  joints=[[(x4, yr - hf), (x4, yr + hf)]], inside=(x4 + 8.0, yr + 0.75 * hf))
    xfan = x3b - 12.0
    T["fan"] = TunnelPart("fan", _rect(xfan - 1.2, xfan + 1.2, yr - hf + 0.8, yr + hf - 0.8), kind="fan", host="fan_section",
                          inside=(xfan, yr + 0.6 * hf))
    # the hub fairing: a round nose upstream of the fan (the flow comes from the right) and a long tail cone
    hr = 7.0
    s = np.linspace(0.0, 1.0, 40)
    nose = np.c_[xfan + 2.0 + 6.0 * (1 - np.sqrt(1 - (1 - s) ** 2)) * 0 + 6.0 * np.cos(0.5 * math.pi * s),
                 hr * np.sin(0.5 * math.pi * s)]
    tail_x = np.linspace(xfan + 2.0, xfan - 75.0, 40)
    tail = np.c_[tail_x, hr * (1 - ((xfan + 2.0 - tail_x) / 77.0) ** 1.6)]
    top = np.r_[nose, tail[1:]]
    hub = np.r_[top, top[::-1] * [1, -1]] + [0.0, yr]
    T["hub"] = TunnelPart("hub", hub, kind="hub", host="fan_section", inside=(xfan - 15.0, yr))
    T["return_leg"] = TunnelPart("return_leg", [(x4, yr - hf), (x4, yr + hf), (0.5 * Wb, yr + h), (0.5 * Wb, yr - h)],
                                 walls=[[(x4, yr + hf), (0.5 * Wb, yr + h)], [(x4, yr - hf), (0.5 * Wb, yr - h)]],
                                 joints=[[(0.5 * Wb, yr - h), (0.5 * Wb, yr + h)]],
                                 inside=(0.5 * (x4 + 0.5 * Wb), yr + 0.6 * h))
    # model: plan outline of the jet transport, span 0.55 of the test-section width, nose upstream
    k = 0.55 * Wt / B738["span"]
    xm = 0.5 * (x_c1 + x_t1) - 0.5 * k * B738["length"]
    model = {}
    for n, p in aircraft_top(B738).items():
        if p.kind in ("surface",) or n.startswith(("slat", "spoiler", "flap", "aileron", "elevator")):
            continue
        model[n] = p.xy * k + [xm, 0.0]
    T.model_parts = model
    tail_x = xm + k * B738["length"]
    x_strut = x_t1 - 6.0
    T["support"] = TunnelPart("support", [(tail_x - 0.5, -0.35), (x_strut, -0.35), (x_strut, 0.35), (tail_x - 0.5, 0.35)],
                              kind="support", host="test_section", inside=(0.5 * (tail_x + x_strut), 0.0))
    th_ = np.linspace(0, 2 * math.pi, 60)
    T["strut"] = TunnelPart("strut", np.c_[x_strut + 2.5 * np.cos(th_), 0.8 * np.sin(th_)], kind="support", host="test_section",
                            inside=(x_strut, 0.0))
    T.model_box = (xm, tail_x, -0.5 * k * B738["span"], 0.5 * k * B738["span"])
    T.stations = {1: ((x_sc0 + 22.5, -h), (x_sc0 + 22.5, h)),
                  2: ((x_c1 + 6.0, -ht), (x_c1 + 6.0, ht)),
                  3: ((x_d1 - 2.0, -hd), (x_d1 - 2.0, hd))}
    T.flow = [((x_c1 + 60.0, 0.0), (x_c1 + 90.0, 0.0)), ((xR, 0.25 * yr), (xR, 0.6 * yr)),
              ((x4 - 58.0, yr), (x4 - 93.0, yr)), ((xL, yr - 8.0), (xL, 12.0))]     # return-leg arrow clear of the hub's tail
    T.view, T.unit, T.ratio = "plan", "ft", (Wb / Wt)
    T.extent = (xL - 0.5 * Wb, xR + 0.5 * Ws, -0.5 * Wb, yr + 0.5 * Wb)
    T.areas = dict(settling=Wb, test=Wt)       # plan widths (ft)
    return T


def open_circuit_side(H2=1.0, ratio=7.5, L_test=2.0, diffuser_deg=2.5, diffuser_ratio=1.6):
    """Open-circuit (Eiffel) tunnel in side view, flow left to right, square cross-sections, test
    section height H2 (m). Parts: bellmouth (inlet with a rounded lip), settling_chamber with
    honeycomb and screen_1 .. screen_3, contraction (fifth-order wall, length 0.89 inlet heights,
    area ratio `ratio`, so the height ratio is sqrt(ratio)), test_section (L_test heights long)
    with a model (side view of the jet transport, length 0.45 H2) on a support strut from the
    floor, diffuser (walls at diffuser_deg, height ratio diffuser_ratio), fan_section with fan
    and hub, exhaust. Example: T = open_circuit_side()"""
    from chapter_1.aircraft import aircraft_side, B738
    T = Tunnel()
    H1 = H2 * math.sqrt(ratio)
    h1, h2 = 0.5 * H1, 0.5 * H2
    x_b0, x_b1 = 0.0, 0.35 * H1
    x_s1 = x_b1 + 0.75 * H1
    Lc = 0.89 * H1
    x_c1 = x_s1 + Lc
    x_t1 = x_c1 + L_test * H2
    h3 = h2 * diffuser_ratio
    Ld = (h3 - h2) / math.tan(math.radians(diffuser_deg))
    x_d1 = x_t1 + Ld
    x_f1 = x_d1 + 0.9 * H2
    x_e1 = x_f1 + 0.5 * H2
    # bellmouth: a quarter-ellipse lip flaring out at the inlet
    s = np.linspace(0.0, 1.0, 30)
    lip_y = h1 + 0.18 * H1 * (1 - s) ** 2
    lip = np.c_[x_b0 + (x_b1 - x_b0) * s, lip_y]
    T["bellmouth"] = TunnelPart("bellmouth", np.r_[lip * [1, -1], lip[::-1]], walls=[lip, lip * [1, -1]],
                                joints=[[(x_b1, -h1), (x_b1, h1)]], inside=(0.5 * x_b1, -0.6 * h1), kind="duct")
    T["settling_chamber"] = TunnelPart("settling_chamber", _rect(x_b1, x_s1, -h1, h1),
                                       walls=[[(x_b1, h1), (x_s1, h1)], [(x_b1, -h1), (x_s1, -h1)]],
                                       joints=[[(x_s1, -h1), (x_s1, h1)]], inside=(x_s1 - 0.12 * H1, -0.75 * h1))
    T["honeycomb"] = TunnelPart("honeycomb", _rect(x_b1 + 0.06 * H1, x_b1 + 0.2 * H1, -h1, h1), kind="honeycomb", host="settling_chamber",
                                inside=(x_b1 + 0.13 * H1, 0.5 * h1))
    for i, f in enumerate((0.36, 0.48, 0.60)):
        xs = x_b1 + f * H1
        T[f"screen_{i + 1}"] = TunnelPart(f"screen_{i + 1}", _rect(xs - 0.008, xs + 0.008, -h1, h1), kind="screen", host="settling_chamber",
                                          lines=[[(xs, -h1), (xs, h1)]], inside=(xs, 0.5 * h1))
    xc, hc = contraction_wall(h1, h2, Lc)
    xc = xc + x_s1
    up, lo = np.c_[xc, hc], np.c_[xc, -hc]
    T["contraction"] = TunnelPart("contraction", np.r_[lo, up[::-1]], walls=[up, lo],
                                  joints=[[(x_c1, -h2), (x_c1, h2)]], inside=(x_s1 + 0.6 * Lc, -0.4 * h1))
    T["test_section"] = TunnelPart("test_section", _rect(x_c1, x_t1, -h2, h2),
                                   walls=[[(x_c1, h2), (x_t1, h2)], [(x_c1, -h2), (x_t1, -h2)]],
                                   joints=[[(x_t1, -h2), (x_t1, h2)]], inside=(x_t1 - 0.45 * H2, 0.5 * h2))
    T["diffuser"] = TunnelPart("diffuser", [(x_t1, -h2), (x_d1, -h3), (x_d1, h3), (x_t1, h2)],
                               walls=[[(x_t1, h2), (x_d1, h3)], [(x_t1, -h2), (x_d1, -h3)]],
                               joints=[[(x_d1, -h3), (x_d1, h3)]], inside=(0.5 * (x_t1 + x_d1), -0.5 * h2))
    T["fan_section"] = TunnelPart("fan_section", _rect(x_d1, x_f1, -h3, h3),
                                  walls=[[(x_d1, h3), (x_f1, h3)], [(x_d1, -h3), (x_f1, -h3)]],
                                  joints=[[(x_f1, -h3), (x_f1, h3)]], inside=(x_d1 + 0.15 * H2, 0.8 * h3))
    xfan = x_d1 + 0.55 * H2
    T["fan"] = TunnelPart("fan", _rect(xfan - 0.03, xfan + 0.03, -h3 + 0.03, h3 - 0.03), kind="fan", host="fan_section",
                          inside=(xfan, 0.6 * h3))
    hr = 0.22 * h3
    sx = np.linspace(0.0, 1.0, 30)
    hub_top = np.c_[x_d1 + 0.05 * H2 + (xfan + 0.15 * H2 - x_d1 - 0.05 * H2) * sx,
                    hr * np.sqrt(np.clip(1 - (1 - sx) ** 2.0, 0, 1))]
    hub_top = np.r_[hub_top, [(xfan + 0.3 * H2, 0.6 * hr)]]
    T["hub"] = TunnelPart("hub", np.r_[hub_top, hub_top[::-1] * [1, -1]], kind="hub", host="fan_section", inside=(xfan - 0.1 * H2, 0.0))
    T["exhaust"] = TunnelPart("exhaust", _rect(x_f1, x_e1, -h3, h3),
                              walls=[[(x_f1, h3), (x_e1, h3)], [(x_f1, -h3), (x_e1, -h3)]],
                              joints=[[(x_e1, -h3), (x_e1, h3)]], inside=(0.5 * (x_f1 + x_e1), 0.6 * h3))
    k = 0.6 * H2 / B738["length"]
    side = aircraft_side(B738, detail=False)
    zc = 0.5 * (B738["fus_bottom"] + B738["fus_top"])
    xm = 0.5 * (x_c1 + x_t1) - 0.5 * k * B738["length"]
    T.model_parts = {n: (p.xy - [0.0, zc]) * k + [xm, 0.05 * H2] for n, p in side.items()
                     if p.kind != "ground" and not n.endswith(("gear", "wheel"))}
    x_strut = xm + k * 17.5
    T["support"] = TunnelPart("support", _rect(x_strut - 0.02 * H2, x_strut + 0.02 * H2, -h2, 0.05 * H2 - k * 1.5),
                              kind="support", host="test_section", inside=(x_strut, -0.5 * h2))
    T.model_box = (xm, xm + k * B738["length"], 0.05 * H2 - k * 2.5, 0.05 * H2 + k * 9.0)
    T.stations = {1: ((x_b1 + 0.68 * H1, -h1), (x_b1 + 0.68 * H1, h1)),
                  2: ((x_c1 + 0.3 * H2, -h2), (x_c1 + 0.3 * H2, h2)),
                  3: ((x_d1 - 0.05 * H2, -h3), (x_d1 - 0.05 * H2, h3))}
    T.flow = [((x_b0 - 0.55 * H1, 0.0), (x_b0 - 0.1 * H1, 0.0)), ((x_e1 + 0.1 * H1, 0.0), (x_e1 + 0.55 * H1, 0.0))]
    T.view, T.unit, T.ratio = "side", "m", ratio
    T.extent = (x_b0, x_e1, -h1 - 0.18 * H1, h1 + 0.18 * H1)
    T.lengths = dict(contraction=Lc, diffuser=Ld, test=L_test * H2, total=x_e1 - x_b0)
    return T


def axis_area(T, x):
    """Cross-section area along the axis of an open_circuit_side() tunnel (square sections, m^2),
    from its outline: 4 h(x)^2 with h the wall half-height. Example: axis_area(T, [5.0])"""
    walls = [T[n].walls[0] for n in ("settling_chamber", "contraction", "test_section", "diffuser", "fan_section")]
    pts = np.vstack(walls)
    order = np.argsort(pts[:, 0], kind="stable")
    hx = np.interp(np.asarray(x, float), pts[order, 0], np.abs(pts[order, 1]))
    return 4.0 * hx ** 2


# ===================================================================== unit checks
def _close(a, b, rtol, what):
    assert abs(a - b) <= rtol * abs(b), f"{what}: {a!r} vs {b!r}"


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from chapter_1.flow import venturi_speed
    dp, rho, r = 1200.0, 1.2, 8.5
    V2 = test_section_speed(dp, rho, r)
    _close(pressure_difference(V2, rho, r), dp, 1e-12, "speed and pressure difference round trip")
    # the same result as page 1.5's venturi relation (V1 at the inlet), times the area ratio
    _close(V2, venturi_speed(dp, rho, r, 1.0) * r, 1e-12, "venturi relation of 1.5")
    _close(manometer_dh(manometer_dp(0.0731, RHO_MERCURY), RHO_MERCURY), 0.0731, 1e-12, "manometer round trip")
    M, ok = mach_check(102.0, 288.16)
    assert ok and abs(M - 0.2998) < 1e-3
    # one-dimensional flow along the axis: with no loss the pressure returns to p1 where A = A1
    x = np.linspace(0, 1, 5); A = np.array([7.5, 3.0, 1.0, 3.0, 7.5])
    V, p, p0 = axis_flow(x, A, 1.0, 40.0, 1.2, 1.0e5)
    _close(float(p[-1]), 1.0e5, 1e-12, "no loss: full recovery")
    _close(float(p[0] - p[2]), pressure_difference(40.0, 1.2, 7.5), 1e-12, "p1 - p2 from the axis")
    V, p, p0 = axis_flow(x, A, 1.0, 40.0, 1.2, 1.0e5, (0.5, 1.0), 150.0)
    _close(float(1.0e5 - p[-1]), 150.0, 1e-9, "the diffuser loss shows at the exit")
    xw, hw = contraction_wall(3.0, 1.0, 2.0, n=2001)
    assert hw[0] == 3.0 and abs(hw[-1] - 1.0) < 1e-12 and np.all(np.diff(hw) <= 1e-12)
    slope = np.gradient(hw, xw)
    assert abs(slope[0]) < 1e-5 and abs(slope[-1]) < 1e-5          # zero slope at both ends
    T = closed_circuit_plan()
    _close(T["corner_2"].poly[:, 0].mean() - T["corner_3"].poly[:, 0].mean(), 320.0, 1e-12, "320 ft between corners")
    _close(T["contraction"].walls[0][0, 1] / T["contraction"].walls[0][-1, 1], 65.0 / 21.75, 1e-9, "plan width ratio")
    d = T["diffuser"].walls[0]
    ang = math.degrees(math.atan2(d[1, 1] - d[0, 1], d[1, 0] - d[0, 0]))
    assert 1.0 < ang < 3.5, ang                                    # a small diffuser wall angle (TP-3008: about 2 to 2.5 deg)
    for n in ("corner_1", "corner_2", "corner_3", "corner_4"):
        c = T[n]
        x0, x1 = c.poly[:, 0].min(), c.poly[:, 0].max()
        y0, y1 = c.poly[:, 1].min(), c.poly[:, 1].max()
        for v in c.lines:
            assert np.all((v[:, 0] > x0) & (v[:, 0] < x1) & (v[:, 1] > y0) & (v[:, 1] < y1)), f"vane outside {n}"
    O = open_circuit_side()
    a1 = float(axis_area(O, [O.stations[1][0][0]])[0]); a2 = float(axis_area(O, [O.stations[2][0][0]])[0])
    _close(a1 / a2, 7.5, 1e-9, "contraction ratio of the open-circuit outline")
    _close(O.lengths["contraction"], 0.89 * math.sqrt(7.5), 1e-12, "contraction 0.89 inlet heights")
    print("tunnel.py: all unit checks passed")
    print(f"  closed circuit: contraction plan-width ratio {65 / 21.75:.2f}; diffuser wall {ang:.2f} deg; "
          f"open circuit total length {O.lengths['total']:.2f} m")
