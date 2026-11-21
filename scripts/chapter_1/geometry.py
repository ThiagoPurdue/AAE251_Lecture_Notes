"""Geometry of 1.3 Vehicle Anatomy: NACA 4-digit sections, wing planform metrics, and the
parametric outlines of a jet transport and a launch vehicle, plus the helpers that draw them
as line art in the chapter style.

Units: meters for the vehicles and wings (the helpers do not care), chord fractions for
airfoils. Angles in degrees.

Outlines are built from smooth parametric curves (superellipse noses, power-law tail cones,
the NACA thickness form for fins) through stations read from published dimensioned drawings:

  - Jet transport: Boeing 737-800 (no winglets). Boeing, "737 Airplane Characteristics for
    Airport Planning", D6-58325-7 Rev C, 2025: Section 2.2.5, General Dimensions, Model
    737-800 (length 39.47 m, span 34.32 m, height 12.55 m, fuselage width 3.76 m, nose to
    wing-tip leading edge 23.47 m and trailing edge 24.99 m, nose gear 4.09 m from the nose,
    wheelbase 15.60 m, horizontal-tail span 14.35 m, engine centerline 4.83 m from the
    fuselage centerline, nose to engine inlet 13.36 m) and Section 7.2.1 (tires 27 in nose,
    44.5 in main). Stations between the dimensioned points (nose and tail-cone shape,
    sweep breaks, fin and nacelle outline) were read off the same scaled drawing. The
    positions and chords of the control surfaces are schematic (typical of a jet transport;
    the document does not give them).
  - Launch vehicle: Ariane 5 ECA. Arianespace, "Ariane 5 User's Manual", Issue 5 Revision 2,
    2016: Section 1.5.1 (fairing 5.4 m x 17 m; cryogenic upper stage ESC-A 5.4 m x 4.711 m
    including its interstage structure; main core stage EPC 5.4 m x 23.8 m without engine;
    solid boosters EAP 3.05 m x 31.6 m) and Annex 5, Figure A5.1 (fairing: cylinder about
    10.8 m, then the ogive). Estimated, not given in the manual: the lengths of the
    interstage part and of the equipment bay, the engine and nozzle sizes, the booster nose
    cone, and the height of the boosters along the core (from the manual's vehicle
    illustration). A caption says "proportions after Ariane 5 ECA".
  - NACA 4-digit sections: Jacobs, E. N., Ward, K. E., and Pinkerton, R. M., "The
    Characteristics of 78 Related Airfoil Sections from Tests in the Variable-Density Wind
    Tunnel", NACA Report 460, 1933 (the four-digit designation, the thickness equation
    +-y = 0.29690 sqrt(x) - 0.12600 x - 0.35160 x^2 + 0.28430 x^3 - 0.10150 x^4 for the 20%
    basic section, scaled to the thickness, and the mean line of two parabolic arcs).

Run this file for its unit checks:  python3 -B scripts/chapter_1/geometry.py
"""
import math

import numpy as np


# ===================================================================== curves
def superellipse(t, n):
    """The quarter superellipse (1 - (1 - t)^n)^(1/n) for t in [0, 1]: 0 at t = 0 with a
    vertical tangent, 1 at t = 1 with a horizontal one. n = 2 is a quarter ellipse; a smaller n
    is blunter. Example: superellipse(0.5, 2.0) -> 0.8660"""
    t = np.clip(np.asarray(t, dtype=float), 0.0, 1.0)
    return (1.0 - (1.0 - t) ** n) ** (1.0 / n)


def catmull_rom(points, n=24, closed=False):
    """A smooth curve (centripetal Catmull-Rom spline) through the points (k, 2), `n` samples
    per span; passes through every point. Example: xy = catmull_rom([(0, 0), (1, 1), (2, 0)])"""
    P = np.asarray(points, dtype=float)
    if closed:
        P = np.vstack([P[-1], P, P[0], P[1]])
    else:
        P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        t0 = 0.0
        t1 = t0 + max(np.hypot(*(p1 - p0)), 1e-9) ** 0.5
        t2 = t1 + max(np.hypot(*(p2 - p1)), 1e-9) ** 0.5
        t3 = t2 + max(np.hypot(*(p3 - p2)), 1e-9) ** 0.5
        t = np.linspace(t1, t2, n, endpoint=False)[:, None]
        a1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
        a2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
        a3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
        b1 = (t2 - t) / (t2 - t0) * a1 + (t - t0) / (t2 - t0) * a2
        b2 = (t3 - t) / (t3 - t1) * a2 + (t - t1) / (t3 - t1) * a3
        out.append((t2 - t) / (t2 - t1) * b1 + (t - t1) / (t2 - t1) * b2)
    out.append(P[-2][None, :] if not closed else P[1][None, :])
    return np.vstack(out)


def fillet(poly, i, r, n=16):
    """Round the corner i of the closed polygon `poly` (k, 2) with an arc of radius r (same
    units), tangent to both sides. Returns the new polygon. Example: fillet(square, 2, 0.1)"""
    P = np.asarray(poly, dtype=float)
    a, b, c = P[i - 1], P[i], P[(i + 1) % len(P)]
    u, v = (a - b) / np.hypot(*(a - b)), (c - b) / np.hypot(*(c - b))
    half = 0.5 * math.acos(float(np.clip(np.dot(u, v), -1.0, 1.0)))
    d = r / math.tan(half)
    p, q = b + d * u, b + d * v
    m = (u + v) / np.hypot(*(u + v))
    ctr = b + (r / math.sin(half)) * m
    a0, a1 = math.atan2(*(p - ctr)[::-1]), math.atan2(*(q - ctr)[::-1])
    da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    arc = ctr + r * np.c_[np.cos(a0 + da * np.linspace(0, 1, n)), np.sin(a0 + da * np.linspace(0, 1, n))]
    return np.vstack([P[:i], arc, P[i + 1:]])


def circle_xy(center, r, n=96):
    """Closed polygon of a circle. Example: circle_xy((0, 0), 1.0)"""
    t = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    return np.c_[center[0] + r * np.cos(t), center[1] + r * np.sin(t)]


def hull(points):
    """Convex hull (counterclockwise) of a set of points (k, 2), by the monotone chain.
    Example: hull(np.r_[root_xy, tip_xy])"""
    P = sorted(map(tuple, np.asarray(points, dtype=float)))
    if len(P) < 3:
        return np.asarray(P)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return np.asarray(lo[:-1] + up[:-1])


def polygon_area(xy):
    """Area of a closed polygon (shoelace), positive. Example: polygon_area([(0,0),(1,0),(1,1),(0,1)]) -> 1"""
    x, y = np.asarray(xy, dtype=float).T
    return 0.5 * abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


# ===================================================================== NACA 4-digit sections
def naca4(code, n=161, chord=1.0, closed_te=False):
    """A NACA 4-digit section "MPTT" (e.g. "4418"): maximum camber M% of the chord at P/10 of the
    chord, maximum thickness TT% of the chord. Thickness laid off perpendicular to the mean
    camber line (NACA Report 460), cosine spacing, n points per surface.
    closed_te=True uses -0.1036 for the last coefficient (zero trailing-edge thickness).
    Returns a dict: m, p, t (fractions), x (stations), yc (mean line), yt (half thickness),
    xu, yu, xl, yl (upper and lower surfaces), outline (closed, from the trailing edge over the
    top and back under), all scaled by `chord`, and x_tmax (station of maximum thickness).
    Example: naca4("4418")["yc"].max() -> 0.04"""
    code = str(code)
    if len(code) != 4 or not code.isdigit():
        raise ValueError(f"NACA 4-digit code expected, got {code!r}")
    m, p, t = int(code[0]) / 100.0, int(code[1]) / 10.0, int(code[2:]) / 100.0
    beta = np.linspace(0.0, math.pi, n)
    x = 0.5 * (1.0 - np.cos(beta))
    k4 = -0.1036 if closed_te else -0.1015
    yt = 5.0 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 + k4 * x ** 4)
    if m == 0.0 or p == 0.0:
        yc, dyc = np.zeros_like(x), np.zeros_like(x)
    else:
        fwd = x < p
        yc = np.where(fwd, m / p ** 2 * (2 * p * x - x ** 2), m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x ** 2))
        dyc = np.where(fwd, 2 * m / p ** 2 * (p - x), 2 * m / (1 - p) ** 2 * (p - x))
    th = np.arctan(dyc)
    xu, yu = x - yt * np.sin(th), yc + yt * np.cos(th)
    xl, yl = x + yt * np.sin(th), yc - yt * np.cos(th)
    outline = np.r_[np.c_[xu[::-1], yu[::-1]], np.c_[xl[1:], yl[1:]]] * chord
    xt = np.linspace(0.0, 1.0, 20001)
    ytt = 5.0 * t * (0.2969 * np.sqrt(xt) - 0.1260 * xt - 0.3516 * xt ** 2 + 0.2843 * xt ** 3 + k4 * xt ** 4)
    return dict(code=code, m=m, p=p, t=t, x=x * chord, yc=yc * chord, yt=yt * chord, xu=xu * chord,
                yu=yu * chord, xl=xl * chord, yl=yl * chord, outline=outline,
                x_tmax=float(xt[np.argmax(ytt)]) * chord, chord=chord)


# Sections a real airplane uses: Lednicer, "The Incomplete Guide to Airfoil Usage" (UIUC
# Applied Aerodynamics Group): the Douglas DC-3 has a NACA 2215 at the root and a NACA 2206 at
# the tip.
AIRFOIL_USAGE = {"Douglas DC-3": ("2215", "2206")}


def naca4_decode(code):
    """The meaning of a NACA 4-digit number: dict max_camber (fraction of chord), camber_at
    (fraction of chord from the leading edge), thickness (fraction of chord).
    Example: naca4_decode("4418") -> {'max_camber': 0.04, 'camber_at': 0.4, 'thickness': 0.18}"""
    s = naca4(code, n=3)
    return dict(max_camber=s["m"], camber_at=s["p"], thickness=s["t"])


# ===================================================================== wing planform
def planform(b, c_r, c_t, sweep_le=None, sweep_c4=None):
    """A straight-tapered wing of span b, root chord c_r and tip chord c_t, with the leading-edge
    sweep sweep_le or the quarter-chord sweep sweep_c4 (deg; give one). Returns a dict:
    b, c_r, c_t, S (area), AR (b^2/S), taper (c_t/c_r), mac (mean aerodynamic chord,
    2/3 c_r (1 + l + l^2)/(1 + l)), y_mac (its distance from the centerline, b/6 (1 + 2l)/(1 + l)),
    x_mac (its leading edge, aft of the root leading edge), sweep_le, sweep_c4, sweep_te,
    sweep_at(f) (sweep of the line at chord fraction f), and corners: the half-wing for y >= 0,
    as root LE, tip LE, tip TE, root TE, with x aft from the root leading edge.
    Example: planform(10.0, 2.0, 1.0, sweep_le=20.0)["AR"] -> 6.667"""
    if (sweep_le is None) == (sweep_c4 is None):
        raise ValueError("give one of sweep_le and sweep_c4")
    lam = c_t / c_r
    half = 0.5 * b
    if sweep_le is None:
        sweep_le = math.degrees(math.atan(math.tan(math.radians(sweep_c4)) + 0.25 * (c_r - c_t) / half))
    tle = math.tan(math.radians(sweep_le))

    def sweep_at(f):
        return math.degrees(math.atan(tle - f * (c_r - c_t) / half))
    S = 0.5 * (c_r + c_t) * b
    mac = 2.0 / 3.0 * c_r * (1 + lam + lam ** 2) / (1 + lam)
    y_mac = b / 6.0 * (1 + 2 * lam) / (1 + lam)
    x_tip = half * tle
    corners = np.array([[0.0, 0.0], [x_tip, half], [x_tip + c_t, half], [c_r, 0.0]])
    return dict(b=b, c_r=c_r, c_t=c_t, S=S, AR=b * b / S, taper=lam, mac=mac, y_mac=y_mac, x_mac=y_mac * tle,
                sweep_le=sweep_le, sweep_c4=sweep_at(0.25), sweep_te=sweep_at(1.0), sweep_at=sweep_at,
                corners=corners)


def chord_at(pf, y):
    """Local chord at distance y from the centerline of a planform() wing. Example: chord_at(pf, 0.0) -> c_r"""
    return pf["c_r"] + (pf["c_t"] - pf["c_r"]) * abs(y) / (0.5 * pf["b"])


def mac_construction(pf):
    """Points of the classic drawing that finds the mean aerodynamic chord (half-wing, y >= 0,
    x aft from the root leading edge): the root chord extended forward by the tip chord
    (point A, ahead of the root LE) and the tip chord extended aft by the root chord (point B,
    behind the tip TE); the line A-B crosses the mid-chord line at the spanwise station of the
    MAC. Returns a dict: A, B, mid_root, mid_tip, cross (the crossing), mac_le, mac_te.
    Example: c = mac_construction(pf); c["cross"][1] -> pf["y_mac"]"""
    (x0, _), (x1, h), (x2, _), (x3, _) = pf["corners"]
    A = np.array([x0 - pf["c_t"], 0.0])
    B = np.array([x2 + pf["c_r"], h])
    m0, m1 = np.array([0.5 * (x0 + x3), 0.0]), np.array([0.5 * (x1 + x2), h])
    # intersection of A-B with m0-m1
    d1, d2 = B - A, m1 - m0
    def cross(u, v):
        return u[0] * v[1] - u[1] * v[0]
    s = cross(m0 - A, d2) / cross(d1, d2)
    X = A + s * d1
    y = X[1]
    le = x0 + (x1 - x0) * y / h
    return dict(A=A, B=B, mid_root=m0, mid_tip=m1, cross=X, mac_le=np.array([le, y]),
                mac_te=np.array([le + chord_at(pf, y), y]))


# ===================================================================== parts
class Part:
    """One closed shape of a drawn vehicle: name, xy (k, 2) closed outline, kind ("body",
    "surface" for a control surface or other moving part, "engine", "gear", "fairing",
    "stage", "strut", "detail" (a thin shape drawn on a part: a window, a door, a hidden tank),
    "line" (an open line drawn on a part, such as a stage joint) or "ground"), z (drawing
    order), hidden (drawn dashed, as a hidden line), `inside`, a point well inside the shape
    where a leader may end, and `on`, the name of the part a detail is drawn on (a leader that
    ends inside that part may cross the detail)."""

    def __init__(self, name, xy, kind="body", z=3.0, hidden=False, inside=None, on=None):
        self.name, self.xy, self.kind, self.z, self.hidden = name, np.asarray(xy, dtype=float), kind, z, hidden
        self.inside = np.asarray(inside, dtype=float) if inside is not None else self.xy.mean(axis=0)
        self.on = on

    def __repr__(self):
        return f"Part({self.name!r}, {len(self.xy)} points, kind={self.kind!r})"


def _mirror(xy):
    return np.asarray(xy, dtype=float) * np.array([1.0, -1.0])


# ===================================================================== shared vehicle helpers
def blunted_ogive(R, length, rn, n=120):
    """Upper half-outline (x from 0 at the base, y) of a tangent ogive of base radius R whose
    sharp tip is replaced by a sphere of radius rn tangent to it, scaled so the whole nose is
    `length` long. Ends on the axis at x = length. Example: blunted_ogive(2.7, 6.2, 0.55)"""
    def build(Lo):
        rho = (R ** 2 + Lo ** 2) / (2.0 * R)
        xs = math.sqrt((rho - rn) ** 2 - (rho - R) ** 2)               # sphere center on the axis
        Co, Cs = np.array([0.0, R - rho]), np.array([xs, 0.0])
        T = Co + rho * (Cs - Co) / np.hypot(*(Cs - Co))                 # tangency point
        x = np.linspace(0.0, T[0], n)
        y = np.sqrt(rho ** 2 - x ** 2) + R - rho
        a0 = math.atan2(T[1], T[0] - xs)
        a = np.linspace(a0, 0.0, 30)[1:]
        return np.r_[np.c_[x, y], np.c_[xs + rn * np.cos(a), rn * np.sin(a)]], xs + rn
    lo, hi = 0.5 * length, 3.0 * length
    for _ in range(80):                                                 # nose length grows with Lo
        mid = 0.5 * (lo + hi)
        if build(mid)[1] < length:
            lo = mid
        else:
            hi = mid
    return build(0.5 * (lo + hi))[0]


def rotate_xy(xy, deg, about=(0.0, 0.0)):
    """Points xy (N, 2) rotated counterclockwise by deg degrees about the point `about` (a negative
    angle turns them clockwise: rotate_xy(section, -4.0) pitches a section nose up in a flow from
    the left). Example: rotate_xy([(1.0, 0.0)], 90.0) -> [[0, 1]]"""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    o = np.asarray(about, float)
    return (np.asarray(xy, float) - o) @ np.array([[c, s], [-s, c]]) + o


def ellipse_xy(cx, cy, rx, ry, t0=0.0, t1=2 * math.pi, n=90):
    """x and y arrays of an ellipse (or an arc of it from t0 to t1, radians) centered at (cx, cy)
    with semi-axes rx and ry. Example: x, y = ellipse_xy(0.0, 0.0, 0.2, 1.0)"""
    t = np.linspace(t0, t1, n)
    return cx + rx * np.cos(t), cy + ry * np.sin(t)


# ===================================================================== clipping (enlarged insets)
def clip_poly(xy, r):
    """Sutherland-Hodgman: the closed polygon xy clipped to the rectangle r = (x0, x1, y0, y1).
    Example: clip_poly(circle_xy((0, 0), 1.0), (0, 2, -2, 2))"""
    out = [tuple(q) for q in np.asarray(xy, float)]
    x0, x1, y0, y1 = r
    for inside, cut in ((lambda q: q[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
                        (lambda q: q[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
                        (lambda q: q[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
                        (lambda q: q[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1))):
        src, out = out, []
        if not src:
            break
        prev = src[-1]
        for cur in src:
            if inside(cur):
                if not inside(prev):
                    out.append(cut(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cut(prev, cur))
            prev = cur
    return np.array(out)


def clip_line(xy, r, step=0.02):
    """The open polyline xy cut to the rectangle r = (x0, x1, y0, y1): a list of the pieces
    inside it, sampled every `step` data units. Example: clip_line([(0, 0), (3, 0)], (1, 2, -1, 1))"""
    x0, x1, y0, y1 = r
    pts = []
    xy = np.asarray(xy, float)
    for a, b in zip(xy[:-1], xy[1:]):
        n = max(2, int(np.hypot(*(b - a)) / step) + 1)
        seg = np.linspace(a, b, n)
        pts.append(seg if not pts else seg[1:])
    q = np.vstack(pts)
    ins = (q[:, 0] >= x0 - 1e-9) & (q[:, 0] <= x1 + 1e-9) & (q[:, 1] >= y0 - 1e-9) & (q[:, 1] <= y1 + 1e-9)
    pieces, cur = [], []
    for k, ok in enumerate(ins):
        if ok:
            cur.append(q[k])
        elif cur:
            pieces.append(np.array(cur))
            cur = []
    if cur:
        pieces.append(np.array(cur))
    return [pc for pc in pieces if len(pc) > 1]


def rotate_parts(parts, angle_deg, about=(0.0, 0.0)):
    """The parts rotated by angle_deg (counterclockwise) about a point: rotate_parts(p, 90)
    stands a launch_vehicle() on its tail. Example: parts = rotate_parts(launch_vehicle(), -90)"""
    a = math.radians(angle_deg)
    Rm = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    c = np.asarray(about, dtype=float)
    out = {}
    for k, p in parts.items():
        out[k] = Part(p.name, (p.xy - c) @ Rm.T + c, p.kind, p.z, p.hidden, (p.inside - c) @ Rm.T + c,
                      on=getattr(p, "on", None))
    return out


def extent(parts):
    """(xmin, xmax, ymin, ymax) of all parts. Example: x0, x1, y0, y1 = extent(aircraft_side())"""
    allp = np.vstack([p.xy for p in parts.values()])
    return float(allp[:, 0].min()), float(allp[:, 0].max()), float(allp[:, 1].min()), float(allp[:, 1].max())


# ===================================================================== landing-gear arrangements
# One generic airplane for the six arrangements (fuselage lengths: x aft from the nose, y across,
# z up from the fuselage centerline). Plan view: a fuselage of half-width GEAR_BODY["w"] with
# an elliptical nose and a tapered tail cone, a straight-tapered wing (root chord from
# wing_le0 to wing_te0 at the centerline, tip chord from wing_le1 to wing_te1 at semispan
# wing_b2) and a horizontal tail; side view: the same fuselage, half-height h, its tail cone
# swept up, a fin, and the wing seen edge on, low on the fuselage (wing_z).
GEAR_BODY = dict(w=0.050, h=0.056, nose=0.16, cone0=0.62,
                 wing_le0=0.36, wing_te0=0.60, wing_le1=0.45, wing_te1=0.54, wing_b2=0.32, wing_z=-0.042,
                 tail_le0=0.84, tail_te0=0.975, tail_le1=0.91, tail_te1=0.975, tail_b2=0.13)


def gear_wing_edges(y, B=GEAR_BODY):
    """Leading and trailing edge x of the generic wing at |y| (fuselage lengths)."""
    f = min(abs(y) / B["wing_b2"], 1.0)
    return (B["wing_le0"] + (B["wing_le1"] - B["wing_le0"]) * f, B["wing_te0"] + (B["wing_te1"] - B["wing_te0"]) * f)


GEAR_LAYOUTS = {
    # name: cg, the x of the center of gravity, and the wheel units (x, y, n side by side, m in
    # tandem, size, role) in fuselage lengths; size 1 is a main wheel, a nose wheel, a tail wheel
    # or an outrigger is smaller. Each unit stands on structure: under the fuselage (|y| below its
    # half-width) or under the wing (inside the planform). Schematic positions after the
    # arrangements Raymer (2006) names; the bicycle, single-main and quadricycle layouts add the
    # wing-tip outriggers that keep such aircraft level. One x per unit and one x of the center of
    # gravity serve both views.
    "tricycle":     dict(cg=0.47, units=[(0.12, 0.0, 1, 1, 0.8, "nose"), (0.54, 0.12, 1, 1, 1.0, "main"),
                                         (0.54, -0.12, 1, 1, 1.0, "main")]),
    "tail-dragger": dict(cg=0.47, units=[(0.415, 0.10, 1, 1, 1.0, "main"), (0.415, -0.10, 1, 1, 1.0, "main"),
                                         (0.95, 0.0, 1, 1, 0.55, "tail")]),
    "multi-bogie":  dict(cg=0.45, units=[(0.11, 0.0, 1, 1, 0.8, "nose"), (0.545, 0.115, 2, 2, 0.85, "main"),
                                         (0.545, -0.115, 2, 2, 0.85, "main")]),
    "bicycle":      dict(cg=0.48, units=[(0.28, 0.0, 1, 1, 1.0, "main"), (0.68, 0.0, 1, 1, 1.0, "main"),
                                         (0.495, 0.305, 1, 1, 0.55, "outrigger"), (0.495, -0.305, 1, 1, 0.55, "outrigger")]),
    "single main":  dict(cg=0.47, units=[(0.43, 0.0, 1, 1, 1.0, "main"), (0.95, 0.0, 1, 1, 0.55, "tail"),
                                         (0.495, 0.305, 1, 1, 0.55, "outrigger"), (0.495, -0.305, 1, 1, 0.55, "outrigger")]),
    "quadricycle":  dict(cg=0.48, units=[(0.33, 0.028, 1, 1, 0.9, "main"), (0.33, -0.028, 1, 1, 0.9, "main"),
                                         (0.63, 0.028, 1, 1, 0.9, "main"), (0.63, -0.028, 1, 1, 0.9, "main"),
                                         (0.495, 0.305, 1, 1, 0.55, "outrigger"), (0.495, -0.305, 1, 1, 0.55, "outrigger")]),
}
GEAR_LAYOUTS["multi-bogey"] = GEAR_LAYOUTS["multi-bogie"]      # the first spelling, still accepted


_MOVED = {"aircraft": ("B738", "aircraft_side", "aircraft_top", "aircraft_front", "wing_box"),
          "launchers": ("ARIANE5", "launch_vehicle")}


def __getattr__(name):
    """The vehicle outlines moved to aircraft.py and launchers.py; the old names still work here."""
    for mod, names in _MOVED.items():
        if name in names:
            import importlib
            return getattr(importlib.import_module(f"chapter_1.{mod}"), name)
    raise AttributeError(name)


# ===================================================================== unit checks
def _close(a, b, tol, what):
    assert abs(a - b) <= tol, f"{what}: {a!r} vs {b!r} (tol {tol})"


if __name__ == "__main__":
    # NACA Report 460: the 20% basic section has its maximum ordinate 0.1 at 0.3 chord and the
    # ordinate 0.002 at the trailing edge (conditions 1 and 2 of the report); the 0012 is it scaled
    # to 12%: 0.06 at 0.3 chord
    s = naca4("0020", 4001)
    _close(float(np.interp(0.30, s["x"], s["yt"])), 0.100, 5e-4, "Report 460, basic section, 0.1 at 0.3 chord")
    _close(float(s["yt"][-1]), 0.002, 5e-4, "Report 460, basic section, 0.002 at the trailing edge")
    s = naca4("0012", 4001)
    _close(float(np.interp(0.30, s["x"], s["yt"])), 0.06002, 2e-5, "NACA 0012 ordinate at 30%")
    _close(s["x_tmax"], 0.30, 0.005, "NACA 0012 maximum thickness at 30% chord")
    _close(float(np.interp(1.0, s["x"], s["yt"])), 0.00126, 1e-5, "open trailing edge half-thickness")
    _close(float(naca4("0012", 401, closed_te=True)["yt"][-1]), 0.0, 1e-6, "closed trailing edge")
    s = naca4("4418", 2001)
    _close(float(s["yc"].max()), 0.04, 1e-6, "NACA 4418 maximum camber 4%")
    _close(float(s["x"][np.argmax(s["yc"])]), 0.40, 0.002, "NACA 4418 maximum camber at 40%")
    _close(float(2 * s["yt"].max()), 0.18, 1e-4, "NACA 4418 thickness 18%")
    assert naca4_decode("4418") == dict(max_camber=0.04, camber_at=0.4, thickness=0.18)
    # the camber line is the mean of the two surfaces at the same station (thickness perpendicular to it)
    up = np.interp(0.5, s["xu"], s["yu"])
    lo = np.interp(0.5, s["xl"], s["yl"])
    _close(0.5 * float(up + lo), float(np.interp(0.5, s["x"], s["yc"])), 2e-4, "mean line between the surfaces")
    # planform: closed forms against a strip integration
    pf = planform(30.0, 5.0, 1.5, sweep_le=30.0)
    y = np.linspace(0.0, 15.0, 200001)
    c = chord_at(pf, y)
    _close(2 * np.trapezoid(c, y), pf["S"], 1e-6, "area")
    mac_num = 2 * np.trapezoid(c * c, y) / pf["S"]
    _close(mac_num, pf["mac"], 1e-6, "mean aerodynamic chord by integration")
    _close(2 * np.trapezoid(c * y, y) / pf["S"], pf["y_mac"], 1e-6, "MAC station by integration")
    _close(pf["AR"], 30.0 ** 2 / pf["S"], 1e-12, "aspect ratio")
    _close(planform(30.0, 5.0, 1.5, sweep_c4=pf["sweep_c4"])["sweep_le"], 30.0, 1e-9, "sweep conversion")
    con = mac_construction(pf)
    _close(float(con["cross"][1]), pf["y_mac"], 1e-9, "the graphical construction finds the MAC station")
    _close(float(con["mac_te"][0] - con["mac_le"][0]), pf["mac"], 1e-9, "the chord there is the MAC")
    # rectangular wing: MAC = chord, at the quarter span
    rw = planform(10.0, 2.0, 2.0, sweep_le=0.0)
    _close(rw["mac"], 2.0, 1e-12, "rectangular MAC")
    _close(rw["y_mac"], 2.5, 1e-12, "rectangular MAC station")
    assert polygon_area([(0, 0), (1, 0), (1, 1), (0, 1)]) == 1.0
    print("geometry.py: all unit checks passed")
    print(f"  planform(30, 5, 1.5, 30 deg): S = {pf['S']:.2f}, AR = {pf['AR']:.3f}, MAC = {pf['mac']:.4f} at "
          f"y = {pf['y_mac']:.4f}, sweep c/4 = {pf['sweep_c4']:.2f} deg")
