"""Shared code for Chapter 2, Introduction to Orbits: constants, orbit equations, number
formatting, the record of printed values, and the drawing helpers of the chapter figures.

Every page module (scripts/chapter_2/p2N_<slug>.py) imports from here, always as

    from chapter_2.orbits import *          # or: from chapter_2 import orbits as O

and never as a bare `import orbits` (that would make a second copy of the value record).
The runner scripts/make_chapter_2_figures.py puts scripts/ on the import path. The API is
summarized in scripts/chapter_2/README.md.

Units at the API: km, km/s, km^3/s^2, km^2/s^2, seconds, and angles in DEGREES unless a
name says radians. G0 is the only SI constant in m/s^2.

Run this file to run its unit checks:

    python3 -B scripts/chapter_2/orbits.py
"""
import json
import math
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

if __name__ not in ("chapter_2.orbits", "__main__"):
    raise ImportError("import this module as chapter_2.orbits (from chapter_2.orbits import ...), "
                      "not as a bare 'orbits': the value record must be one object")

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from make_figures import plt, np, save, NOTES, INK, GOLD, DUST, LIGHT, AGED, STEEL, SERIES  # noqa: E402,F401
import matplotlib.ticker as mticker  # noqa: E402
from matplotlib.markers import MarkerStyle  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, ArrowStyle  # noqa: E402
from matplotlib.text import OffsetFrom  # noqa: E402
from matplotlib.transforms import Affine2D  # noqa: E402

# Math in labels: matplotlib mathtext set in Arial, so a label such as $\Delta V_1$ or
# $v_{\mathrm{esc}}$ matches the Arial text around it. The SVG keeps it as live text.
plt.rcParams.update({
    "mathtext.fontset": "custom",
    "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic",
    "mathtext.bf": "Arial:bold",
    "mathtext.sf": "Arial",
    "mathtext.default": "it",
    "mathtext.fallback": "stixsans",       # a glyph Arial lacks; save_figure() rejects it
    "font.size": 12,
    "axes.labelsize": 12,
    "axes.linewidth": 0.9,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "xtick.major.width": 0.9,
    "ytick.major.width": 0.9,
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "legend.fontsize": 11,
    "legend.frameon": False,
    "lines.dash_capstyle": "butt",
    "lines.solid_joinstyle": "round",
    "hatch.linewidth": 1.0,
    "axes.unicode_minus": True,
})

# Subscripts made of a word ($v_{\mathrm{orbit}}$) or the infinity sign ($v_\infty$) are set at
# SUB_WORD of the main size, not mathtext's 0.7, so they read at 10 pt or more on the page (a
# 12 pt label gives a 10.6 pt subscript). Single-letter subscripts ($r_p$, $\Delta V_1$) keep 0.7.
# Done by parsing such a label with a larger shrink factor; svg_problems() checks the result.
SUB_WORD = 0.88
_WORD_SUB = re.compile(r"_\{?\\(?:mathrm\{[A-Za-z]{2,}\}|infty)")
import functools as _functools  # noqa: E402
import matplotlib._mathtext as _mtx  # noqa: E402
from matplotlib.mathtext import MathTextParser as _MTP  # noqa: E402
if not hasattr(_mtx, "SHRINK_FACTOR") or not hasattr(_MTP._parse_cached, "__wrapped__"):
    raise ImportError("matplotlib changed: the word-subscript size in orbits.py needs updating")
_parse_plain = _MTP._parse_cached.__wrapped__


@_functools.lru_cache(200)
def _parse_cached(self, s, dpi, prop, antialiased, load_glyph_flags):
    if not _WORD_SUB.search(s):
        return _parse_plain(self, s, dpi, prop, antialiased, load_glyph_flags)
    old, _mtx.SHRINK_FACTOR = _mtx.SHRINK_FACTOR, SUB_WORD
    try:
        return _parse_plain(self, s, dpi, prop, antialiased, load_glyph_flags)
    finally:
        _mtx.SHRINK_FACTOR = old


_MTP._parse_cached = _parse_cached

# ===================================================================== constants (PLAN 5)
MU = {                      # gravitational parameter GM, km^3/s^2
    "Sun": 1.327e11, "Mercury": 2.203e4, "Venus": 3.249e5, "Earth": 3.986e5,
    "Moon": 4.903e3, "Mars": 4.283e4, "Jupiter": 1.267e8, "Saturn": 3.793e7,
}
RADIUS = {                  # radius, km: equatorial for Earth, Jupiter and Saturn, mean for the others
    "Sun": 696000.0, "Mercury": 2440.0, "Venus": 6052.0, "Earth": 6378.0,
    "Moon": 1737.0, "Mars": 3390.0, "Jupiter": 71492.0, "Saturn": 60268.0,
}
# Earth's mean radius, km, as launch calculations commonly use. The other pages of the
# chapter use the equatorial 6,378 km; the launch page (p23) explains the convention. Only
# p23 uses this one; surface_speed() and rotation_gain() default to it.
RADIUS_EARTH_MEAN = 6371.0
AU = 1.496e8                # astronomical unit, km
SUN_DISTANCE = {            # mean distance from the Sun, km (no Mars entry: PLAN rule 4)
    "Mercury": 5.790e7, "Venus": 1.082e8, "Earth": 1.496e8,
    "Jupiter": 5.203 * AU, "Saturn": 9.537 * AU,
    "Uranus": 19.19 * AU, "Neptune": 30.07 * AU,     # JPL approximate planetary elements
}
# Mars's mean distance from the Sun, km, kept out of SUN_DISTANCE on purpose (PLAN rule 4):
# it only places the unlabeled-value Mars marker on the planet-speed figure of 2.1. Never
# print a number computed from it.
SUN_DISTANCE_MARS_FIGURE_ONLY = 1.524 * AU
ORBIT_DAYS = {              # orbital period around the Sun, days (no Mars entry: PLAN rule 4)
    "Mercury": 87.97, "Venus": 224.7, "Earth": 365.26, "Jupiter": 4332.6, "Saturn": 10759.0,
}
OMEGA_EARTH = 7.292e-5      # Earth's rotation rate, rad/s
T_SIDEREAL = 86164.0        # sidereal day, s
G0 = 9.80665                # standard gravity, m/s^2 (SI: the rocket equation uses it)
G_SI = 6.674e-11            # universal gravitational constant, N m^2/kg^2 (SI; CODATA 2018), quoted only
DAY = 86400.0               # solar day, s (unit conversion only)


# ===================================================================== orbit functions
def circular_speed(mu, r):
    """Speed on a circular orbit of radius r, km/s: sqrt(mu/r).
    Example: circular_speed(MU["Earth"], RADIUS["Earth"] + 400) -> 7.669"""
    return np.sqrt(mu / r)


def escape_speed(mu, r):
    """Escape speed at radius r, km/s: sqrt(2 mu/r).
    Example: escape_speed(MU["Earth"], RADIUS["Earth"]) -> 11.18"""
    return np.sqrt(2.0 * mu / r)


def vis_viva(mu, r, a):
    """Speed at radius r on an orbit of semi-major axis a (negative for a hyperbola), km/s.
    Example: vis_viva(MU["Earth"], 7000.0, 8000.0) -> 8.004"""
    return np.sqrt(mu * (2.0 / r - 1.0 / a))


def period(mu, a):
    """Orbital period, s: 2 pi sqrt(a^3/mu). Example: period(MU["Earth"], 6778.0) / 60 -> 92.56"""
    return 2.0 * np.pi * np.sqrt(a ** 3 / mu)


def semi_major_axis_from_period(mu, T):
    """Semi-major axis, km, of an orbit of period T (s): (mu (T/2 pi)^2)^(1/3).
    Example: semi_major_axis_from_period(MU["Earth"], T_SIDEREAL) -> 42,164"""
    return (mu * (T / (2.0 * np.pi)) ** 2) ** (1.0 / 3.0)


def specific_energy(mu, a):
    """Specific orbital energy, km^2/s^2: -mu/(2a). Example: specific_energy(MU["Earth"], 7000.0) -> -28.47"""
    return -mu / (2.0 * a)


def energy_from_state(mu, r, v):
    """Specific orbital energy, km^2/s^2, from radius r (km) and speed v (km/s): v^2/2 - mu/r.
    Negative: ellipse or circle; zero: parabola; positive: hyperbola.
    Example: energy_from_state(MU["Earth"], 7000.0, 8.0) -> -24.94"""
    return 0.5 * np.asarray(v) ** 2 - mu / np.asarray(r)


def semi_major_axis_from_state(mu, r, v):
    """Semi-major axis, km, from radius r and speed v (vis-viva solved for a); negative for a
    hyperbola, infinite for a parabola. Example: semi_major_axis_from_state(MU["Earth"], 7000.0, 8.0) -> 7,990"""
    eps = energy_from_state(mu, r, v)
    return np.inf if eps == 0 else -mu / (2.0 * eps)


def eccentricity(rp, ra):
    """Eccentricity from the periapsis and apoapsis radii (km): (ra - rp)/(ra + rp).
    Example: eccentricity(7078.0, 12178.0) -> 0.2648"""
    return (ra - rp) / (ra + rp)


def apsides(a, e):
    """Periapsis and apoapsis radius, km: (a(1 - e), a(1 + e)). Example: apsides(9628.0, 0.2648) -> (7078.5, 12177.5)"""
    return a * (1.0 - e), a * (1.0 + e)


def conic_radius(p, e, theta):
    """Radius, km, on a conic of semi-latus rectum p (km) and eccentricity e at true anomaly
    theta (deg): p / (1 + e cos theta). Example: conic_radius(7000.0, 0.2, 90.0) -> 7000"""
    return p / (1.0 + e * np.cos(np.radians(theta)))


def trajectory_type(e, tol=1e-9):
    """'circle', 'ellipse', 'parabola' or 'hyperbola' from the eccentricity.
    Example: trajectory_type(0.2648) -> 'ellipse'"""
    if e < tol:
        return "circle"
    if abs(e - 1.0) < tol:
        return "parabola"
    return "ellipse" if e < 1.0 else "hyperbola"


def true_anomaly_at_radius(a, e, r):
    """True anomaly (deg, 0 to 180, outbound) where the conic (a, e) reaches radius r (km).
    Example: true_anomaly_at_radius(9628.0, 0.2648, 9628.0) -> 105.4"""
    p = a * (1.0 - e * e)
    c = (p / r - 1.0) / e
    if abs(c) > 1.0 + 1e-12:
        raise ValueError(f"the orbit never reaches r = {r} km")
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def orbit_point(a, e, theta, rotate=0.0, center=(0.0, 0.0)):
    """Position (x, y), km, at true anomaly theta (deg) on the conic (a, e) with the focus at
    `center` and periapsis along `rotate` (deg from +x). Example: orbit_point(7000.0, 0.0, 90.0) -> [0, 7000]"""
    p = a * (1.0 - e * e)
    r = conic_radius(p, e, theta)
    t = np.radians(theta + rotate)
    return np.array([center[0] + r * np.cos(t), center[1] + r * np.sin(t)])


def orbit_velocity(mu, a, e, theta, rotate=0.0, sense=1):
    """Velocity vector (vx, vy), km/s, at true anomaly theta (deg) on the conic (a, e), in the
    same frame as orbit_point(); sense=+1 counterclockwise motion, -1 clockwise.
    Example: orbit_velocity(MU["Earth"], 7000.0, 0.0, 0.0) -> [0, 7.546]"""
    p = a * (1.0 - e * e)
    h = math.sqrt(mu / p)
    th = math.radians(theta)
    vr, vt = h * e * math.sin(th), h * (1.0 + e * math.cos(th))
    t = math.radians(theta + rotate)
    v = np.array([vr * math.cos(t) - vt * math.sin(t), vr * math.sin(t) + vt * math.cos(t)])
    return v if sense > 0 else -v


def flight_path_angle(e, theta):
    """Flight-path angle (deg), the angle of the velocity above the local horizontal, at true
    anomaly theta (deg). Example: flight_path_angle(0.2648, 90.0) -> 14.83"""
    th = math.radians(theta)
    return math.degrees(math.atan2(e * math.sin(th), 1.0 + e * math.cos(th)))


def conic_xy(rp, e, theta0=None, theta1=None, n=721, rotate=0.0, r_max=None, center=(0.0, 0.0)):
    """Points (x, y), km, of the conic with periapsis radius rp (km) and eccentricity e, with
    the focus at `center` and periapsis along `rotate` (deg). Works for every e >= 0. Default
    range: the whole ellipse; for e >= 1 the branch out to r_max (default 6 rp) on both sides.
    Angles theta0, theta1 in deg; a range past the asymptote is clipped.
    Example: x, y = conic_xy(7000.0, 1.0, r_max=30000.0)   # a parabola"""
    p = rp * (1.0 + e)
    if e < 1.0:
        lo = 0.0 if theta0 is None else theta0
        hi = 360.0 if theta1 is None else theta1
        if r_max is not None and r_max < rp * (1 + e) / (1 - e):
            lim = math.degrees(math.acos((p / r_max - 1.0) / e))
            lo, hi = max(lo, -lim), min(hi, lim)
    else:
        rm = 6.0 * rp if r_max is None else r_max
        lim = math.degrees(math.acos(max(-1.0, (p / rm - 1.0) / e)))
        lo = -lim if theta0 is None else max(theta0, -lim)
        hi = lim if theta1 is None else min(theta1, lim)
    th = np.linspace(lo, hi, n)
    r = conic_radius(p, e, th)
    t = np.radians(th + rotate)
    return center[0] + r * np.cos(t), center[1] + r * np.sin(t)


def orbit_xy(a, e, n=721, theta0=None, theta1=None, rotate=0.0, r_max=None, center=(0.0, 0.0)):
    """Points (x, y), km, of the orbit of semi-major axis a (km; negative for a hyperbola) and
    eccentricity e, focus at `center`, periapsis along `rotate` (deg). True-anomaly range in
    deg (default: the whole ellipse, or the hyperbola branch out to r_max, default 6 rp).
    For a parabola use conic_xy(). Example: x, y = orbit_xy(9628.0, 0.2648)"""
    if abs(e - 1.0) < 1e-12:
        raise ValueError("a parabola has no finite a: use conic_xy(rp, 1.0, ...)")
    return conic_xy(a * (1.0 - e), e, theta0, theta1, n, rotate, r_max, center)


def time_from_periapsis(mu, a, e, theta):
    """Time (s) to fly from periapsis to true anomaly theta (deg) on an ellipse or a hyperbola
    (a < 0), from Kepler's equation. Negative before periapsis; for an ellipse each extra turn
    past +-180 deg adds one period. Example: time_from_periapsis(MU["Earth"], 9628.0, 0.2648, 180.0) -> T/2"""
    th = np.asarray(theta, dtype=float)
    if e < 1.0:
        n = math.sqrt(mu / a ** 3)
        k = np.round(th / 360.0)
        w = np.radians(th - 360.0 * k)                       # wrapped to [-180, 180]
        E = 2.0 * np.arctan2(math.sqrt(1.0 - e) * np.sin(w / 2.0), math.sqrt(1.0 + e) * np.cos(w / 2.0))
        M = E - e * np.sin(E)
        return M / n + k * 2.0 * math.pi / n
    if e > 1.0:
        n = math.sqrt(mu / (-a) ** 3)
        F = 2.0 * np.arctanh(math.sqrt((e - 1.0) / (e + 1.0)) * np.tan(np.radians(th) / 2.0))
        return (e * np.sinh(F) - F) / n
    raise ValueError("time_from_periapsis: parabola not supported")


def true_anomaly_at_time(mu, a, e, t):
    """True anomaly (deg) reached a time t (s) after periapsis, on an ellipse (unwrapped: one turn
    adds 360) or a hyperbola (a < 0); Kepler's equation by Newton's method.
    Example: true_anomaly_at_time(MU["Earth"], 9628.0, 0.2648, 600.0) -> 39.64"""
    t = np.asarray(t, dtype=float)
    if e < 1.0:
        n = math.sqrt(mu / a ** 3)
        M = n * t
        E = M + e * np.sin(M)
        for _ in range(50):
            E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
        k = np.floor((E + np.pi) / (2 * np.pi))
        Ew = E - 2 * np.pi * k
        th = 2.0 * np.arctan2(math.sqrt(1.0 + e) * np.sin(Ew / 2.0), math.sqrt(1.0 - e) * np.cos(Ew / 2.0))
        return np.degrees(th) + 360.0 * k
    n = math.sqrt(mu / (-a) ** 3)
    M = n * t
    F = np.arcsinh(M / e)
    for _ in range(80):
        F = F - (e * np.sinh(F) - F - M) / (e * np.cosh(F) - 1.0)
    return np.degrees(2.0 * np.arctan(math.sqrt((e + 1.0) / (e - 1.0)) * np.tanh(F / 2.0)))


def hohmann(mu, r1, r2):
    """Hohmann transfer between circular orbits of radius r1 and r2 (km), up or down.
    Returns a dict: r1, r2, a_t, e_t (transfer ellipse), v_c1, v_c2 (circular speeds),
    v_tp, v_ta (transfer speed at its periapsis and apoapsis), v_t1, v_t2 (transfer speed at
    r1 and at r2), dv1, dv2, dv_total (magnitudes, km/s, always positive), raise (True when
    r2 > r1: both burns along the motion; False: both against it), T_t (transfer period, s),
    tof (time of flight, s, half of T_t).
    Example: hohmann(MU["Earth"], 6778.0, 26578.0)["dv_total"] -> 3.416"""
    a_t = 0.5 * (r1 + r2)
    lo, hi = min(r1, r2), max(r1, r2)
    v_c1, v_c2 = circular_speed(mu, r1), circular_speed(mu, r2)
    v_t1, v_t2 = vis_viva(mu, r1, a_t), vis_viva(mu, r2, a_t)
    T_t = period(mu, a_t)
    return dict(r1=r1, r2=r2, a_t=a_t, e_t=(hi - lo) / (hi + lo), v_c1=v_c1, v_c2=v_c2,
                v_tp=vis_viva(mu, lo, a_t), v_ta=vis_viva(mu, hi, a_t), v_t1=v_t1, v_t2=v_t2,
                dv1=abs(v_t1 - v_c1), dv2=abs(v_c2 - v_t2), dv_total=abs(v_t1 - v_c1) + abs(v_c2 - v_t2),
                T_t=T_t, tof=0.5 * T_t) | {"raise": r2 > r1}


def plane_change(v, di):
    """Delta-V (km/s) to turn a velocity of magnitude v (km/s) by di (deg) at constant speed:
    2 v sin(di/2). Example: plane_change(7.669, 30.0) -> 3.970"""
    return 2.0 * np.asarray(v) * np.sin(np.radians(di) / 2.0)


def surface_speed(lat, R=RADIUS_EARTH_MEAN, omega=OMEGA_EARTH):
    """Eastward speed (km/s) of the ground at latitude lat (deg): omega R cos(lat), with
    Earth's mean radius (the launch convention of the course; pass R for another radius).
    Example: surface_speed(0.0) -> 0.4646; surface_speed(0.0, RADIUS["Earth"]) -> 0.4651"""
    return omega * R * np.cos(np.radians(lat))


def rotation_gain(lat, az, R=RADIUS_EARTH_MEAN, omega=OMEGA_EARTH):
    """Delta-V (km/s) the rotating Earth gives a launch at latitude lat toward azimuth az
    (deg, clockwise from north): omega R cos(lat) sin(az), with Earth's mean radius;
    negative for a westward launch. Example: rotation_gain(28.5, 90.0) -> 0.4083"""
    return surface_speed(lat, R, omega) * np.sin(np.radians(az))


def inclination_from_launch(lat, az):
    """Orbit inclination (deg, 0 to 180) from launch latitude lat and azimuth az (deg):
    cos i = cos(lat) sin(az). Example: inclination_from_launch(40.0, 90.0) -> 40.0"""
    c = np.cos(np.radians(lat)) * np.sin(np.radians(az))
    return np.degrees(np.arccos(np.clip(c, -1.0, 1.0)))


def launch_azimuths(lat, inc):
    """The two launch azimuths (deg, 0 to 360, clockwise from north) that put a launch from
    latitude lat (deg) into an orbit of inclination inc (deg): sin(az) = cos(inc)/cos(lat).
    Returns (northbound, southbound). Raises ValueError when inc < lat or inc > 180 - lat
    (out of reach of a direct launch). Example: launch_azimuths(28.5, 51.6) -> (44.98, 135.02)"""
    s = math.cos(math.radians(inc)) / math.cos(math.radians(lat))
    if abs(s) > 1.0 + 1e-12:
        raise ValueError(f"inclination {inc} deg is out of reach from latitude {lat} deg")
    az1 = math.degrees(math.asin(max(-1.0, min(1.0, s))))
    return az1 % 360.0, (180.0 - az1) % 360.0


def periapsis_speed_hyperbola(mu, rp, vinf):
    """Speed (km/s) at periapsis radius rp (km) of a hyperbola with excess speed vinf (km/s):
    sqrt(vinf^2 + 2 mu/rp). Example: periapsis_speed_hyperbola(MU["Earth"], 6563.0, 3.0) -> 11.42"""
    return np.sqrt(np.asarray(vinf) ** 2 + 2.0 * mu / rp)


def hyperbola(mu, rp, vinf):
    """Geometry of the hyperbola with periapsis radius rp (km) and excess speed vinf (km/s).
    Returns a dict: a (km, negative), e, p (semi-latus rectum, km), vp (periapsis speed, km/s),
    theta_inf (deg, true anomaly of the asymptote), turn (deg, turn angle 2 asin(1/e)),
    b (km, aiming radius). Example: hyperbola(MU["Earth"], 6563.0, 3.0)["e"] -> 1.148"""
    a = -mu / vinf ** 2
    e = 1.0 + rp * vinf ** 2 / mu
    return dict(a=a, e=e, p=a * (1.0 - e * e), vp=float(periapsis_speed_hyperbola(mu, rp, vinf)),
                theta_inf=math.degrees(math.acos(-1.0 / e)), turn=math.degrees(2.0 * math.asin(1.0 / e)),
                b=-a * math.sqrt(e * e - 1.0))


def synodic_period(T1, T2):
    """Synodic period 1/|1/T1 - 1/T2|, in the unit of T1 and T2.
    Example: synodic_period(ORBIT_DAYS["Venus"], ORBIT_DAYS["Earth"]) -> 583.9"""
    return 1.0 / abs(1.0 / T1 - 1.0 / T2)


def ground_track(inc, T, t, lon_node=0.0, day=T_SIDEREAL, rotating=True):
    """Latitude and longitude (deg; longitude wrapped to -180..180) under a circular orbit of
    inclination inc (deg) and period T (s) at times t (s), starting at the ascending node over
    longitude lon_node (deg). The planet turns once per `day` seconds (sidereal), so each pass
    crosses the equator 360 T/day deg farther west. Example: lat, lon = ground_track(98.2, 5928.0, t)"""
    t = np.asarray(t, dtype=float)
    u = 2.0 * np.pi * t / T
    i = math.radians(inc)
    lat = np.degrees(np.arcsin(np.sin(i) * np.sin(u)))
    lon = lon_node + np.degrees(np.arctan2(np.cos(i) * np.sin(u), np.cos(u)))
    lon = np.degrees(np.unwrap(np.radians(lon)))
    if rotating:
        lon = lon - 360.0 * t / day
    return lat, (lon + 180.0) % 360.0 - 180.0


# ===================================================================== number formatting
def _dec(x):
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(f"cannot format {x}")
    return Decimal(repr(x))


def _commas(d, nd, minus):
    s = f"{abs(d):,.{nd}f}"
    return (minus + s) if d < 0 and float(d) != 0.0 else s


def fmt(x, sig=4, minus="-"):
    """x with `sig` significant figures, thousands separated by commas, rounded half up.
    Digits before the decimal point are never rounded away: a number with `sig` or more
    integer digits prints as a whole number (26578.3 -> "26,578", 5828.5 -> "5,829").
    Trailing zeros are kept (2.4 with sig=3 -> "2.40"). `minus` replaces the minus sign
    (pass "−" for figure text that is not math). Example: fmt(0.264786) -> "0.2648" """
    d = _dec(x)
    if d == 0:
        return "0" if sig <= 1 else "0." + "0" * (sig - 1)
    exp = abs(d).adjusted()
    nd = max(sig - 1 - exp, 0)
    q = d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    if abs(q).adjusted() > exp and nd > 0:                 # 9.9996 -> 10.00, not 10.000
        nd -= 1
        q = d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return _commas(q, nd, minus)


def fmt_dec(x, nd, minus="-"):
    """x with exactly nd decimals, thousands separated by commas, rounded half up.
    Example: fmt_dec(5828.46, 1) -> "5,828.5" """
    q = _dec(x).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return _commas(q, nd, minus)


def fmt_sci(x, sig=4):
    """x in powers of ten as LaTeX math (no dollar signs): "1.327 \\times 10^{11}".
    Use inside $...$ on a page or in a figure label. Example: fmt_sci(MU["Sun"]) -> "1.327 \\times 10^{11}" """
    d = _dec(x)
    exp = abs(d).adjusted()
    m = fmt(float(d.scaleb(-exp)), sig)
    if m.lstrip("-").startswith("10"):                    # 9.9996e3 -> 1.000e4
        exp += 1
        m = fmt(float(d.scaleb(-exp)), sig)
    return m if exp == 0 else f"{m} \\times 10^{{{exp}}}"


# ===================================================================== the record of printed values
PAGES = {
    "p21": "orbit-properties",
    "p22": "orbit-transfers",
    "p23": "launch-to-orbit",
    "p24": "patched-conics",
    "p25": "ground-tracks-and-orbit-lifetime",
}
VALUES = {}                               # page stem -> {key: text}
VALUES_FILE = Path(__file__).resolve().parent / "values.json"


def record(page, key, text):
    """Record that the string `text` is printed on `page` (a tag such as "p21" or the page file
    stem) and return it. check_values.py then requires it on the page. Record the number
    only, as printed ("7.669", not "7.669 km/s"). Example: v = record("p21", "vp", fmt(vp))"""
    if not isinstance(text, str):
        raise TypeError(f"record({page!r}, {key!r}): text must be a string; format it with fmt()")
    stem = PAGES.get(page, page)
    old = VALUES.setdefault(stem, {}).get(key)
    if old is not None and old != text:
        raise ValueError(f"record: {stem}:{key} recorded twice with different text: {old!r} and {text!r}")
    VALUES[stem][key] = text
    return text


def write_values(only=None):
    """Write scripts/chapter_2/values.json. With only=None the file holds exactly what was
    recorded in this run; with a list of page stems (or tags), those pages are replaced and
    the other pages already in the file are kept. Example: write_values()"""
    data = {}
    if only is not None:
        stems = {PAGES.get(p, p) for p in only}
        if VALUES_FILE.exists():
            data = {k: v for k, v in json.loads(VALUES_FILE.read_text(encoding="utf-8")).items() if k not in stems}
        data.update({k: v for k, v in VALUES.items() if k in stems})
    else:
        data = dict(VALUES)
    data = {k: dict(sorted(v.items())) for k, v in sorted(data.items())}
    VALUES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {VALUES_FILE.relative_to(SCRIPTS.parent)} ({sum(len(v) for v in data.values())} values)")


# ===================================================================== style
FIG_WIDTH = 6.5           # in, the usual figure width (shown at :width: 60% to 90%)
FS_LABEL = 12             # pt, labels, symbols, axis labels
FS_SMALL = 11             # pt, secondary notes and tick labels; nothing smaller
LW_ORBIT = 2.0            # pt, orbits and data curves
LW_ARROW = 1.6            # pt, vectors and burn arrows
LW_THIN = 0.9             # pt, axes, construction, dimension and reference lines
GRAY = "#767676"          # reference lines (4.54:1 on white)
GRID = "#DDDDDD"          # data-plot grid (decorative)
BLUE, VERMILION, GREEN, PURPLE = SERIES[0], SERIES[1], SERIES[2], SERIES[3]

# Orbit roles: one look across the chapter. color = the line, text = a label in that hue
# with at least 4.5:1 on white. Each role differs by line style as well as by color.
STYLE = {
    "initial":   dict(color=BLUE, text=BLUE, ls="-", lw=LW_ORBIT),                       # initial or parking orbit
    "transfer":  dict(color=VERMILION, text="#B34E00", ls=(0, (5.0, 2.5)), lw=LW_ORBIT),  # transfer orbit
    "final":     dict(color=GREEN, text="#007A5A", ls=(0, (7.0, 2.2, 1.4, 2.2)), lw=LW_ORBIT),   # final or target
    "hyperbola": dict(color=PURPLE, text="#A0507F", ls=(0, (6.0, 1.8, 1.2, 1.8, 1.2, 1.8)), lw=LW_ORBIT),
    "other":     dict(color=INK, text=INK, ls=(0, (0.1, 2.2)), lw=LW_ORBIT, cap="round"),  # dotted black
    "reference": dict(color=GRAY, text=STEEL, ls="-", lw=LW_THIN),                         # apse lines, axes
    "boundary":  dict(color=GRAY, text=STEEL, ls=(0, (4.0, 3.0)), lw=LW_THIN),             # SOI, atmosphere edge, asymptote
}
SEQUENCE = ["initial", "transfer", "final", "hyperbola", "other"]   # the orbit roles, in order
# Data series (curves of a data plot, tracks of different orbits, the conic types of a schematic):
# their own color and line-style pairs, none the same as an orbit role, so a data curve never
# looks like an initial, transfer or final orbit. line_kw(i) and text_color(i) use them.
SERIES_STYLE = [
    dict(color=INK, text=INK, ls="-", lw=LW_ORBIT),                                  # 0 black solid
    dict(color=BLUE, text=BLUE, ls=(0, (6.0, 2.5)), lw=LW_ORBIT),                    # 1 blue dashed
    dict(color=VERMILION, text="#B34E00", ls=(0, (0.1, 2.6)), lw=LW_ORBIT, cap="round"),   # 2 vermilion dotted
    dict(color=STEEL, text=STEEL, ls=(0, (7.0, 2.2, 1.4, 2.2)), lw=LW_ORBIT),         # 3 dark gray dash-dot
    dict(color=GREEN, text="#007A5A", ls=(0, (6.0, 1.8, 1.2, 1.8, 1.2, 1.8)), lw=LW_ORBIT),  # 4 green dash-dot-dot
]
MARKERS = ["o", "s", "^", "D", "v"]
HATCHES = ["//", "\\\\", "xx", "..", "++", "--"]
BODY_FILL = {"Sun": "#F7E3A3", "Mercury": "#E4DFD8", "Venus": "#F2E4C8", "Earth": "#D7E7F5",
             "Moon": "#E6E6E6", "Mars": "#F1D6C8", "Jupiter": "#EFE1CC", "Saturn": "#F3E8CB"}
BODY_DEFAULT = "#E3EAF2"
HEAD = {"small": (7.0, 2.4), "normal": (9.0, 3.1), "large": (11.0, 3.8)}   # arrow head length, half-width, pt
MOTION_HEAD = (10.0, 3.0)  # motion arrowhead on an orbit or track: length, half-width, pt (clearly longer than wide)


def connects(artist, *ends):
    """Tag a thin construction line (a zoom connector) and the artists it is drawn to meet at
    its ends: the layout gate checks that it crosses nothing else. Returns the artist."""
    artist.set_gid("connector")
    artist._touches = tuple(id(e) for e in ends if e is not None)
    return artist


def rides_on(patch, *lines):
    """Record the line(s) an arrowhead is drawn on: the layout gate lets a head lie on its own line only."""
    patch._rides = tuple(id(l) for l in lines if l is not None)
    return patch


def line_kw(role=0, **over):
    """Keyword arguments for ax.plot() in an orbit role of STYLE ("initial", "transfer", ...) or
    the i-th data series of SERIES_STYLE (0: black solid, 1: blue dashed, 2: vermilion dotted,
    3: dark gray dash-dot, 4: green dash-dot-dot). Use a role only for an orbit in that role.
    Example: ax.plot(x, y, **line_kw("transfer"))"""
    st = SERIES_STYLE[role] if isinstance(role, int) else STYLE[role]
    kw = dict(color=st["color"], linestyle=st["ls"], linewidth=st["lw"])
    if st.get("cap") == "round":
        kw.update(dash_capstyle="round", solid_capstyle="round")
    kw.update(over)
    return kw


def text_color(role=0):
    """Label color matching a role or series index, with at least 4.5:1 contrast on white.
    Example: text(ax, xy, "transfer orbit", color=text_color("transfer"))"""
    return SERIES_STYLE[role]["text"] if isinstance(role, int) else STYLE[role]["text"]


# ===================================================================== axes
def new_axes(width=FIG_WIDTH, height=4.0, ncols=1, nrows=1, equal=True, **kw):
    """Figure and frameless axes for a schematic (equal aspect, no ticks). With several panels
    returns an array of axes. Draw in km so bodies and orbits are to scale.
    Example: fig, ax = new_axes(6.5, 4.0)"""
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height), squeeze=False, **kw)
    for ax in axes.flat:
        ax.axis("off")
        if equal:
            ax.set_aspect("equal")
    return fig, (axes[0, 0] if axes.size == 1 else axes.squeeze())


class CommaFormatter(mticker.ScalarFormatter):
    """Tick labels with thousands separated by commas (26,000) and no offset or powers of ten.
    Example: ax.yaxis.set_major_formatter(CommaFormatter())"""

    def __init__(self):
        super().__init__(useOffset=False, useMathText=False)
        self.set_scientific(False)

    def __call__(self, x, pos=None):
        s = super().__call__(x, pos)
        m = re.match(r"^([−-]?)(\d+)(.*)$", s)
        return f"{m.group(1)}{int(m.group(2)):,}{m.group(3)}" if m else s


def degree_ticks(ax, axis="x", step=None):
    """Tick labels in degrees ("30°") on one axis, with ticks every `step` deg if given.
    Example: degree_ticks(ax, "x", 90)"""
    a = ax.xaxis if axis == "x" else ax.yaxis
    if step:
        a.set_major_locator(mticker.MultipleLocator(step))
    a.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:g}°".replace("-", "−")))


def data_axes(width=FIG_WIDTH, height=4.0, ncols=1, nrows=1, grid=True, **kw):
    """Figure and axes for a data plot: left and bottom spines, light grid behind the data,
    commas in tick labels. Label the axes with units ("Altitude, km").
    Example: fig, ax = data_axes(6.5, 4.0)"""
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height), squeeze=False, **kw)
    for ax in axes.flat:
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        if grid:
            ax.grid(True, color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.xaxis.set_major_formatter(CommaFormatter())
        ax.yaxis.set_major_formatter(CommaFormatter())
    return fig, (axes[0, 0] if axes.size == 1 else axes.squeeze())


def map_axes(width=FIG_WIDTH, lon_step=60, lat_step=30, axis_labels=True):
    """Figure and axes for a ground track: longitude -180 to 180 deg, latitude -90 to 90 deg,
    1 deg = 1 deg, labels such as "120°W" and "30°N", light grid, the equator marked.
    Draw tracks with draw_track(). Example: fig, ax = map_axes()"""
    fig, ax = plt.subplots(figsize=(width, width * 0.5 + 0.55))
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(-180, 181, lon_step))
    ax.set_yticks(np.arange(-90, 91, lat_step))

    def lon_label(v, _):
        v = int(round(v))
        return "0°" if v == 0 else ("180°" if abs(v) == 180 else f"{abs(v)}°{'E' if v > 0 else 'W'}")

    def lat_label(v, _):
        v = int(round(v))
        return "0°" if v == 0 else f"{abs(v)}°{'N' if v > 0 else 'S'}"

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lon_label))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lat_label))
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.axhline(0.0, color=GRAY, lw=LW_THIN, zorder=1, gid="equator")
    for s in ax.spines.values():
        s.set_linewidth(LW_THIN)
    if axis_labels:
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
    return fig, ax


# ===================================================================== text and marks
def _equal(ax):
    return ax.get_aspect() == 1.0


def _screen_angle(ax, vec):
    """Screen angle (deg) of a data-space direction. Exact on equal-aspect axes; on other axes
    taken from the current limits (set the limits first)."""
    vx, vy = float(vec[0]), float(vec[1])
    if _equal(ax):
        return math.degrees(math.atan2(vy, vx))
    p0 = ax.transData.transform((0.0, 0.0))
    p1 = ax.transData.transform((vx, vy))
    return math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))


def _anchor(angle):
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    ha = "left" if c > 0.38 else ("right" if c < -0.38 else "center")
    va = "bottom" if s > 0.38 else ("top" if s < -0.38 else "center")
    return ha, va


def _backing(backing):
    if backing is False or backing is None:
        return None
    fc = "white" if backing is True else backing
    return dict(boxstyle="square,pad=0.12", fc=fc, ec="none")


def text(ax, xy, s, direction=None, dist=5.0, offset=(0.0, 0.0), fs=FS_LABEL, color=INK,
         ha=None, va=None, backing=True, zorder=10, **kw):
    """Write s at the data point xy. With `direction` (deg, screen) the text sits `dist` points
    away from xy in that direction and is anchored on its near side; otherwise it is centered
    at xy shifted by `offset` (points). An opaque white backing (backing=True, or a color, or
    False for none) keeps lines from running through the text. Returns the Annotation.
    Example: text(ax, (0, 0), "Earth", direction=-90)"""
    if direction is not None:
        a = math.radians(direction)
        off = (dist * math.cos(a) + offset[0], dist * math.sin(a) + offset[1])
        h, v = _anchor(direction)
    else:
        off, h, v = offset, "center", "center"
    return ax.annotate(s, xy=tuple(np.asarray(xy, dtype=float)), xytext=off, textcoords="offset points",
                       ha=ha or h, va=va or v, fontsize=fs, color=color, bbox=_backing(backing),
                       zorder=zorder, annotation_clip=False, **kw)


def offset_text(ax, xy, s, dx, dy, **kw):
    """Text centered dx, dy points from the data point xy (shorthand for text(..., offset=)).
    Example: offset_text(ax, (7000, 0), "$r_p$", 0, -12)"""
    return text(ax, xy, s, offset=(dx, dy), **kw)


def callout(ax, xy, s, at, gap=4.0, fs=FS_LABEL, color=INK, ha=None, va="center", backing=True, zorder=10, **kw):
    """A label placed in free space at `at` (data) with a short straight leader to the point xy,
    stopping `gap` points short of it. Use it only where no clear spot touches the point; keep
    leaders short and never crossing. backing: True (white), a fill color for a label on a
    fill, or False. Returns the Annotation.
    Example: callout(ax, node_xy, "ascending node", at=(1.6, -1.2))"""
    xy, at = np.asarray(xy, dtype=float), np.asarray(at, dtype=float)
    h = ha or ("left" if at[0] >= xy[0] else "right")
    an = ax.annotate(s, xy=tuple(xy), xytext=tuple(at), ha=h, va=va, fontsize=fs, color=color, zorder=zorder,
                     bbox=_backing(backing), annotation_clip=False,
                     arrowprops=dict(arrowstyle="-", color=INK, lw=0.7, shrinkA=1.0, shrinkB=gap), **kw)
    an.arrow_patch.set_gid("leader")
    return an


def _style(head, lw):
    hl, hw = HEAD[head] if isinstance(head, str) else head
    return ArrowStyle("-|>", head_length=hl, head_width=hw), hl, hw


def _tip_shrink(hl, hw, lw):
    """No extra shrink: matplotlib already pulls a "-|>" head back by the mitred stroke, so
    the tip lands on the target point."""
    return 0.0


def arrow(ax, p0, p1, color=INK, lw=LW_ARROW, head="normal", both=False, zorder=6, **kw):
    """Straight arrow from p0 to p1 (data), crisp filled head ("small", "normal", "large" or
    (length, half-width) in points), tip exactly on p1. both=True puts a head on each end.
    Returns the patch. Example: arrow(ax, (0, 0), (1000, 0))"""
    style, hl, hw = _style(head, lw)
    if both:
        style = ArrowStyle("<|-|>", head_length=hl, head_width=hw)
    shr = _tip_shrink(hl, hw, lw)
    patch = FancyArrowPatch(tuple(p0), tuple(p1), arrowstyle=style, mutation_scale=1.0, color=color, lw=lw,
                            shrinkA=shr if both else 0.0, shrinkB=shr, joinstyle="miter", capstyle="butt",
                            zorder=zorder, **kw)
    ax.add_patch(patch)
    return patch


def velocity_arrow(ax, xy, v, scale, label=None, color=INK, lw=LW_ARROW, direction=None, dist=4.0,
                   fs=FS_LABEL, head="normal", offset=0.0, center=(0.0, 0.0), zorder=6):
    """Velocity vector v (vx, vy in km/s) drawn from xy at `scale` data units per km/s, so its
    length is to scale; state the scale in the caption or draw speed_key(). With `offset`
    (points) the arrow is moved that far sideways, away from `center` (the central body), so a
    vector tangent to an orbit sits beside the orbit instead of on it (equal-aspect axes). The
    label goes beyond the tip (or toward `direction`, deg). Returns the tip point (data, before
    the sideways offset). Example: velocity_arrow(ax, orbit_point(a, e, 0), orbit_velocity(mu, a, e, 0), 800, "$v_p$")"""
    from matplotlib.transforms import ScaledTranslation
    xy = np.asarray(xy, dtype=float)
    tip = xy + scale * np.asarray(v, dtype=float)
    shift = np.zeros(2)
    kw = {}
    if offset:
        a = math.radians(_screen_angle(ax, tip - xy))
        n = np.array([-math.sin(a), math.cos(a)])
        out = xy - np.asarray(center, dtype=float)
        if np.dot(n, out) < 0:
            n = -n
        shift = offset * n
        kw["transform"] = ax.transData + ScaledTranslation(shift[0] / 72.0, shift[1] / 72.0, ax.figure.dpi_scale_trans)
    arrow(ax, xy, tip, color=color, lw=lw, head=head, zorder=zorder, **kw)
    if label:
        ang = _screen_angle(ax, tip - xy) if direction is None else direction
        text(ax, tip, label, direction=ang, dist=dist, offset=tuple(shift), fs=fs, color=color, zorder=zorder + 4)
    return tip


def speed_key(ax, xy, scale, value=1.0, unit="km/s", color=INK, fs=FS_SMALL):
    """A horizontal reference arrow of `value` (km/s) at `scale` data units per km/s, labeled
    ("1 km/s") to the right of its tip, so arrow lengths can be read. Make it at least as long
    as the label is wide. Example: speed_key(ax, (-9000, -8000), 800)"""
    xy = np.asarray(xy, dtype=float)
    end = xy + np.array([value * scale, 0.0])
    arrow(ax, xy, end, color=color, head="small", lw=LW_ARROW)
    text(ax, end, f"{value:g} {unit}", direction=0.0, dist=5, fs=fs, color=color)
    return end


def burn(ax, xy, direction, label=None, length=24.0, color=INK, label_dir=None, dist=3.0, fs=FS_LABEL,
         ms=6.5, side=1, center=(0.0, 0.0), offset=6.0, zorder=8):
    """An impulsive burn: a black dot at xy, on the path, and beside it an arrow `length` points
    long along the velocity change (deg, or a vector such as the velocity: forward to speed up,
    backward to slow down). The arrow is parallel to the path, starts level with the dot and
    sits `offset` points to its side (6 pt: its head clears the path by 2 pt), so it never hides the path it follows: side=+1 on the
    outer side (away from `center`, the central body), -1 on the inner side. When a figure has
    two or more burns, give lengths in proportion to the delta-Vs (burn_lengths()), or say in
    the caption that the burn arrows are not to scale. The label sits at the tip (toward
    label_dir, deg). Returns the tip, in points from xy.
    Example: burn(ax, (6778, 0), 90, r"$\\Delta V_1$", length=30)"""
    xy = tuple(np.asarray(xy, dtype=float))
    ang = float(direction) if np.ndim(direction) == 0 else _screen_angle(ax, direction)
    a = math.radians(ang)
    u = np.array([math.cos(a), math.sin(a)])
    n = np.array([-u[1], u[0]])
    out = np.asarray(xy) - np.asarray(center, dtype=float)
    out_s = _screen_angle(ax, out) if np.hypot(*out) > 0 else ang + 90.0
    if np.dot(n, [math.cos(math.radians(out_s)), math.sin(math.radians(out_s))]) < 0:
        n = -n
    start = side * offset * n
    tip = start + length * u
    off = OffsetFrom(ax.transData, xy, unit="points")
    style, hl, hw = _style("normal", LW_ARROW)
    an = ax.annotate("", xy=tuple(tip), xycoords=off, xytext=tuple(start), textcoords=off, annotation_clip=False,
                     arrowprops=dict(arrowstyle=style, mutation_scale=1.0, color=color, lw=LW_ARROW, shrinkA=0.0,
                                     shrinkB=_tip_shrink(hl, hw, LW_ARROW), joinstyle="miter", capstyle="butt"),
                     zorder=zorder)
    an.arrow_patch.set_gid("burn")
    ax.plot(*xy, "o", color=INK, ms=ms, mec="white", mew=0.8, zorder=zorder + 1)
    if label:
        la = ang if label_dir is None else label_dir
        h, v = _anchor(la)
        # beside the tip, a label also clears the half-width of the head
        dd = dist + (HEAD["normal"][1] + 1.3) * abs(math.sin(math.radians(la - ang)))
        lx, ly = dd * math.cos(math.radians(la)), dd * math.sin(math.radians(la))
        ax.annotate(label, xy=tuple(tip), xycoords=off, xytext=(lx, ly), textcoords="offset points", ha=h, va=v,
                    fontsize=fs, color=color, bbox=_backing(True), zorder=zorder + 2, annotation_clip=False)
    return tip


def burn_lengths(dvs, longest=30.0, shortest=10.0):
    """Burn-arrow lengths (points) in proportion to the delta-Vs `dvs`, the largest `longest`
    points. Raises ValueError when the smallest would be shorter than `shortest` points: then
    draw them at one length and say in the caption that the burn arrows are not to scale.
    Example: burn_lengths([2.012, 1.404]) -> [30.0, 20.93]"""
    dvs = [abs(float(d)) for d in dvs]
    out = [longest * d / max(dvs) for d in dvs]
    if min(out) < shortest:
        raise ValueError(f"burn arrows in proportion would be {min(out):.1f} pt: say 'not to scale' instead")
    return out


def point(ax, xy, label=None, direction=90.0, dist=5.0, color=INK, ms=6.0, kind="dot", fs=FS_LABEL, zorder=8,
          gid=None):
    """A marked point (a spacecraft, a planet position, a launch site) with an optional label
    placed toward `direction` (deg). kind: "dot", "open", "square", "diamond". gid: a drawing
    group ("grp:...", see dimension()) the point belongs to. Example: point(ax, (0, 7000), "chaser", direction=0)"""
    m = {"dot": "o", "open": "o", "square": "s", "diamond": "D"}[kind]
    ax.plot(*xy, m, color=color, mfc="white" if kind == "open" else color, mec=color, ms=ms,
            mew=1.4 if kind == "open" else 0.8, zorder=zorder, gid=gid)
    if label:
        text(ax, xy, label, direction=direction, dist=dist + ms / 2.0, fs=fs, color=color, zorder=zorder + 2)


def line(ax, p0, p1, role="reference", **kw):
    """A straight line from p0 to p1 in a STYLE role (default: thin gray reference line).
    Example: line(ax, (-12178, 0), (7078, 0))"""
    return ax.plot([p0[0], p1[0]], [p0[1], p1[1]], zorder=kw.pop("zorder", 2), **line_kw(role, **kw))[0]


def angle_arc(ax, center, radius, t0, t1, label=None, dist=4.0, arrow_end=False, color=INK, lw=LW_THIN,
              fs=FS_LABEL, backing=True, zorder=5):
    """Arc of `radius` (data units) about `center` from angle t0 to t1 (deg, counterclockwise
    when t1 > t0), with the label on the bisector just outside the arc. arrow_end=True puts
    a head at t1. Needs equal-aspect axes. Example: angle_arc(ax, (0, 0), 2500, 0, 120, r"$\\theta$")"""
    th = np.radians(np.linspace(t0, t1, max(8, int(abs(t1 - t0) * 2))))
    cx, cy = center
    xs, ys = cx + radius * np.cos(th), cy + radius * np.sin(th)
    arc = ax.plot(xs, ys, color=color, lw=lw, zorder=zorder, solid_capstyle="butt")[0]
    if arrow_end:
        rides_on(arrow(ax, (xs[-3], ys[-3]), (xs[-1], ys[-1]), color=color, lw=lw, head="small", zorder=zorder), arc)
    if label:
        b = math.radians(0.5 * (t0 + t1))
        text(ax, (cx + radius * math.cos(b), cy + radius * math.sin(b)), label, direction=math.degrees(b),
             dist=dist, fs=fs, color=color, backing=backing, zorder=zorder + 4)


_GROUPS = __import__("itertools").count(1)


def dimension(ax, p0, p1, label=None, offset=0.0, label_side=1, color=INK, lw=LW_THIN, fs=FS_LABEL,
              zorder=2.5, ticks=True, extension=True):
    """Dimension line between p0 and p1 (data), shifted `offset` data units to the left of the
    direction p0 -> p1, with arrow heads, end ticks and thin extension lines back to p0 and
    p1. The label sits beside the middle of the line (label_side=+1: to the left of
    p0 -> p1, -1: to the right) or, with label_side=0, on the line, breaking it with a white
    backing (engineering style; exempt from the label-crossing check). ticks=False leaves out the
    end ticks and extension=False the extension lines (a dimension drawn on a line between
    two marked points). Needs equal-aspect axes unless the line is horizontal or vertical.
    Example: dimension(ax, (-12178, 0), (7078, 0), "$2a$", offset=-3000)"""
    p0, p1 = np.asarray(p0, dtype=float), np.asarray(p1, dtype=float)
    d = p1 - p0
    u = d / np.hypot(*d)
    n = np.array([-u[1], u[0]])
    q0, q1 = p0 + offset * n, p1 + offset * n
    grp = f"grp:dim{next(_GROUPS)}"                   # its parts may touch each other (layout gate)
    if offset and extension:
        over = 0.12 * offset
        for p, q in ((p0, q0), (p1, q1)):
            ax.plot([p[0], q[0] + over * n[0]], [p[1], q[1] + over * n[1]], color=color, lw=0.7, zorder=zorder,
                    gid=grp)
    arrow(ax, q0, q1, color=color, lw=lw, head="small", both=True, zorder=zorder, gid=grp)
    ang = _screen_angle(ax, d)
    if ticks:
        tick = MarkerStyle("|", transform=Affine2D().rotate_deg(ang))
        ax.plot([q0[0], q1[0]], [q0[1], q1[1]], ls="none", marker=tick, ms=9, mew=lw, color=color, zorder=zorder,
                gid=grp)
    if label:
        mid = 0.5 * (q0 + q1)
        if label_side == 0:
            text(ax, mid, label, fs=fs, color=color, zorder=zorder + 4, gid="on-line")
        else:
            text(ax, mid, label, direction=ang + 90.0 * label_side, dist=4.0, fs=fs, color=color, zorder=zorder + 4)
    return grp


def radius_arrow(ax, center, r, angle, label=None, side=1, color=INK, lw=LW_THIN, fs=FS_LABEL, at=0.55,
                 zorder=2.5):
    """A radius: a thin line from `center` out to distance r (data units) toward `angle` (deg)
    with a head on the far end, labeled beside the line at fraction `at` of its length
    (side=+1: left of the outward direction, -1: right). Drawn under the bodies, so it seems
    to start at the body's surface. Returns the end point.
    Example: radius_arrow(ax, (0, 0), 26578.0, 200.0, "$r_2$")"""
    c = np.asarray(center, dtype=float)
    d = np.array([math.cos(math.radians(angle)), math.sin(math.radians(angle))])
    end = c + r * d
    arrow(ax, c, end, color=color, lw=lw, head="small", zorder=zorder)
    if label:
        text(ax, c + at * r * d, label, direction=angle + 90.0 * side, dist=4.0, fs=fs, color=color,
             zorder=zorder + 4)
    return end

# ===================================================================== bodies and orbits
def draw_body(ax, xy, radius=None, label=None, name=None, where="center", fill=None, dist=4.0, ms=11.0,
              fs=FS_LABEL, lw=1.0, zorder=5):
    """A body: a light-filled disc with a black outline, of `radius` data units (to scale), or,
    with radius=None, a marker of ms points (not to scale; say so in the caption). `name` picks
    the fill from BODY_FILL ("Earth", "Sun", ...); the label defaults to the name. where:
    "center" (inside the disc) or a direction ("below", "above", "left", "right" or deg).
    Example: draw_body(ax, (0, 0), RADIUS["Earth"], name="Earth")"""
    fc = fill or BODY_FILL.get(name, BODY_DEFAULT)
    label = name if label is None else label
    if radius is None:
        ax.plot(*xy, "o", ms=ms, mfc=fc, mec=INK, mew=lw, zorder=zorder)
        half_pts = ms / 2.0
    else:
        ax.add_patch(Circle(xy, radius, fc=fc, ec=INK, lw=lw, zorder=zorder))
        half_pts = 0.0
    if label:
        if where == "center":
            text(ax, xy, label, fs=fs, backing=False, zorder=zorder + 4)
        else:
            ang = {"below": -90.0, "above": 90.0, "left": 180.0, "right": 0.0}.get(where, where)
            edge = np.asarray(xy, dtype=float)
            if radius is not None:
                edge = edge + radius * np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
            text(ax, edge, label, direction=ang, dist=dist + half_pts, fs=fs, zorder=zorder + 4)


def orbit_arrows(ax, rp, e, thetas, rotate=0.0, center=(0.0, 0.0), role="initial", sense=1, zorder=3, line=None):
    """Motion arrowheads in the role color on the conic with periapsis radius rp (km) and
    eccentricity e, focus at `center`, periapsis along `rotate` (deg), at the true anomalies
    `thetas` (deg), pointing along the motion (sense=-1 reverses it). draw_orbit() calls it;
    use it directly for a conic drawn with conic_xy() and ax.plot(), and pass that Line2D as
    `line` (the gate lets a head lie on its own line only).
    Example: orbit_arrows(ax, 1.0, 0.5, (200.0,), role="transfer")"""
    st = {"color": line_kw(role)["color"]}
    p = rp * (1.0 + e)

    def at(th):
        r = conic_radius(p, e, th)
        t = math.radians(th + rotate)
        return np.array([center[0] + r * math.cos(t), center[1] + r * math.sin(t)])
    for th in thetas:
        tip, back = at(th), at(th - 0.4 * sense)          # the head points along the motion
        hl, hw = MOTION_HEAD
        rides_on(ax.add_patch(FancyArrowPatch(tuple(back), tuple(tip), mutation_scale=1.0, lw=0.8,
                                            arrowstyle=ArrowStyle("-|>", head_length=hl, head_width=hw),
                                            color=st["color"], shrinkA=0.0, shrinkB=0.0, joinstyle="miter",
                                            zorder=max(zorder + 0.5, 6.0))), line)     # above the bodies


def draw_orbit(ax, a, e, role="initial", rotate=0.0, theta0=None, theta1=None, center=(0.0, 0.0), r_max=None,
               arrows_at="auto", sense=1, label=None, label_at=None, label_dir=None, dist=5.0, fs=FS_LABEL,
               zorder=3, **kw):
    """Draw the conic (a km, e; a < 0 for a hyperbola) in a STYLE role, focus at `center`,
    periapsis along `rotate` (deg), over the true-anomaly range theta0..theta1 (deg). Arrow
    heads in the role color show the motion (counterclockwise, as seen from the north; the
    chapter's convention) at the true anomalies `arrows_at`: "auto" puts one at 100 deg on a
    closed orbit and halfway along an arc; () draws none; sense=-1 reverses the motion
    (only for a retrograde orbit, and say so in the caption). The label sits at true anomaly label_at, pushed out from the focus (or toward
    label_dir, deg). Extra keywords go to ax.plot. Returns the Line2D.
    Example: draw_orbit(ax, 6778.0, 0.0, "initial", label="parking orbit", label_at=135)"""
    x, y = orbit_xy(a, e, theta0=theta0, theta1=theta1, rotate=rotate, r_max=r_max, center=center)
    ln = ax.plot(x, y, zorder=zorder, **line_kw(role, **kw))[0]
    if isinstance(arrows_at, str):
        if e < 1.0 and theta0 is None and theta1 is None:
            arrows_at = (100.0,)
        else:
            p_ = a * (1.0 - e * e)
            th = np.degrees(np.arctan2(y - center[1], x - center[0])) - rotate
            th = np.degrees(np.unwrap(np.radians(th)))
            r_ = np.hypot(x - center[0], y - center[1])
            assert np.allclose(r_, conic_radius(p_, e, th), rtol=1e-6)
            s_ = np.r_[0.0, np.cumsum(np.hypot(np.diff(x), np.diff(y)))]
            arrows_at = (float(np.interp(0.5 * s_[-1], s_, th)),)       # halfway along the arc
    if arrows_at:
        orbit_arrows(ax, a * (1.0 - e), e, arrows_at, rotate, center, role, sense, zorder, line=ln)
    if label is not None:
        th = 90.0 if label_at is None else label_at
        pt = orbit_point(a, e, th, rotate, center)
        ang = (th + rotate) if label_dir is None else label_dir
        text(ax, pt, label, direction=ang, dist=dist, fs=fs, color=text_color(role), zorder=zorder + 7)
    return ln


def draw_hyperbola(ax, mu, rp, vinf, role="hyperbola", rotate=0.0, branch="out", r_max=None, center=(0.0, 0.0),
                   asymptote=True, arrows_at="auto", label=None, label_at=None, label_dir=None, dist=5.0,
                   zorder=3, **kw):
    """Draw the hyperbola with periapsis radius rp (km) and excess speed vinf (km/s), focus at
    `center`, periapsis along `rotate` (deg). branch: "out" (periapsis outward: departure),
    "in" (inward: arrival) or "both"; it ends at r_max (default 6 rp). asymptote=True draws
    the asymptote of each branch drawn (thin dashed gray) from the point nearest the focus
    (the foot, at the aiming radius b) to the end of the branch; asymptote="full" starts it
    at the center of the hyperbola, which lies far away when vinf is low. Returns
    hyperbola() plus: line, out_dir and in_dir (unit vectors of the velocity far away,
    leaving and arriving), end (outgoing end point), start (incoming start point),
    center_xy (center of the hyperbola), foot_out and foot_in (feet of the asymptotes).
    Example: h = draw_hyperbola(ax, MU["Earth"], 6563.0, 3.0, r_max=40000.0)"""
    g = hyperbola(mu, rp, vinf)
    a, e, ti = g["a"], g["e"], g["theta_inf"]
    rm = 6.0 * rp if r_max is None else r_max
    lim = math.degrees(math.acos((g["p"] / rm - 1.0) / e))
    lo, hi = {"out": (0.0, lim), "in": (-lim, 0.0), "both": (-lim, lim)}[branch]
    ln = draw_orbit(ax, a, e, role, rotate, lo, hi, center, r_max=rm, arrows_at=arrows_at, label=label,
                    label_at=label_at, label_dir=label_dir, dist=dist, zorder=zorder, **kw)
    rot = math.radians(rotate)
    c_xy = np.array(center) + (-a * e) * np.array([math.cos(rot), math.sin(rot)])
    out_dir = np.array([math.cos(math.radians(ti + rotate)), math.sin(math.radians(ti + rotate))])
    # arriving: the asymptote at -theta_inf, traveled toward the planet
    in_dir = -np.array([math.cos(math.radians(-ti + rotate)), math.sin(math.radians(-ti + rotate))])
    end, start = orbit_point(a, e, lim, rotate, center), orbit_point(a, e, -lim, rotate, center)
    F = np.asarray(center, dtype=float)
    feet = {}
    for want, d, pt in (("out", out_dir, end), ("in", -in_dir, start)):
        s_foot = float(np.dot(F - c_xy, d))
        feet[want] = c_xy + s_foot * d
        if asymptote and branch in (want, "both"):
            L = float(np.dot(pt - c_xy, d))
            s0 = -0.12 * L if asymptote == "full" else s_foot - 0.08 * (L - s_foot)
            p0, p1 = c_xy + s0 * d, c_xy + (L + 0.04 * (L - s_foot)) * d
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], zorder=zorder - 1, gid="asymptote", **line_kw("boundary"))
    return g | dict(line=ln, out_dir=out_dir, in_dir=in_dir, end=end, start=start, center_xy=c_xy,
                    foot_out=feet["out"], foot_in=feet["in"])


def track_arrow(ax, lon, lat, i, role="initial", zorder=6, line=None):
    """Motion arrowhead on a ground track (deg) at index i, pointing the way the spacecraft
    moves (from point i - 2 to point i), in the look of the arrowheads draw_orbit() puts on an
    orbit. Example: track_arrow(ax, lon, lat, 120, "transfer")"""
    st = {"color": line_kw(role)["color"]}
    tip, back = (float(lon[i]), float(lat[i])), (float(lon[i - 2]), float(lat[i - 2]))
    rides_on(ax.add_patch(FancyArrowPatch(back, tip, mutation_scale=1.0, lw=0.8,
                                        arrowstyle=ArrowStyle("-|>", head_length=MOTION_HEAD[0],
                                                              head_width=MOTION_HEAD[1]),
                                        color=st["color"], shrinkA=0.0, shrinkB=0.0, joinstyle="miter",
                                        zorder=zorder)), line)


def draw_track(ax, lon, lat, role="initial", label=None, label_at=None, direction=90.0, dist=4.0, zorder=3,
               arrows_at=(), **kw):
    """Draw a ground track (deg) on map_axes(), broken where it wraps at +-180 deg. The label
    sits at index label_at of the arrays, toward `direction` (deg). arrows_at: indices of the
    arrays where a motion arrowhead is drawn (track_arrow). Returns the Line2D.
    Example: draw_track(ax, lon, lat, "initial", label="orbit 1", label_at=40, arrows_at=(120,))"""
    lon, lat = np.asarray(lon, dtype=float), np.asarray(lat, dtype=float)
    jump = np.where(np.abs(np.diff(lon)) > 180.0)[0]
    x, y = np.insert(lon, jump + 1, np.nan), np.insert(lat, jump + 1, np.nan)
    ln = ax.plot(x, y, zorder=zorder, **line_kw(role, **kw))[0]
    for i in arrows_at:
        track_arrow(ax, lon, lat, int(i), role, line=ln)
    if label is not None:
        i = len(lon) // 2 if label_at is None else label_at
        text(ax, (lon[i], lat[i]), label, direction=direction, dist=dist, color=text_color(role), zorder=zorder + 7)
    return ln


def label_curve(ax, x, y, x_at, s, role=0, offset=(0.0, 8.0), color=None, fs=FS_LABEL, **kw):
    """Direct label for a data curve: s centered `offset` points from the curve point at x_at,
    in the curve's text color, on a white backing. Example: label_curve(ax, r, v, 3e8, "Earth", 0)"""
    y_at = float(np.interp(x_at, np.asarray(x, dtype=float), np.asarray(y, dtype=float)))
    return text(ax, (x_at, y_at), s, offset=offset, fs=fs, color=color or text_color(role), **kw)


def bars(ax, labels, values, styles=None, bottoms=None, value_text=None, width=0.62, horizontal=False,
         fs=FS_LABEL, zorder=3):
    """Bar chart told apart by label and hatch as well as color: white bars with a colored
    edge and hatch (styles: roles or series indices, default 0, 1, 2, ...). `bottoms` makes
    floating bars (for a budget). Each bar is labeled with its value (value_text: strings,
    default fmt(value)) at its end. Returns the bar container.
    Example: bars(ax, ["plan A", "plan B"], [5.21, 4.89])"""
    n = len(values)
    styles = list(range(n)) if styles is None else styles
    bottoms = [0.0] * n if bottoms is None else bottoms
    value_text = [fmt(v) for v in values] if value_text is None else value_text
    pos = np.arange(n)
    colors = [line_kw(s)["color"] for s in styles]
    hatch = [HATCHES[(s if isinstance(s, int) else SEQUENCE.index(s)) % len(HATCHES)] for s in styles]
    if horizontal:
        cont = ax.barh(pos, values, height=width, left=bottoms, color="white", edgecolor=colors, lw=1.5, zorder=zorder)
    else:
        cont = ax.bar(pos, values, width=width, bottom=bottoms, color="white", edgecolor=colors, lw=1.5, zorder=zorder)
    for b, h, c in zip(cont.patches, hatch, colors):
        b.set_hatch(h)
        b.set_edgecolor(c)
    for i, (v, b0, s) in enumerate(zip(values, bottoms, value_text)):
        end = b0 + v
        if horizontal:
            text(ax, (end, pos[i]), s, direction=0.0 if v >= 0 else 180.0, dist=4, fs=fs, backing=False)
        else:
            text(ax, (pos[i], end), s, direction=90.0 if v >= 0 else -90.0, dist=3, fs=fs, backing=False)
    if horizontal:
        ax.set_yticks(pos, labels)
    else:
        ax.set_xticks(pos, labels)
    return cont


# ===================================================================== globe (orthographic projection)
class Globe:
    """A sphere drawn by orthographic projection, seen from above the point (view_lat,
    view_lon) in deg, centered at `center` with `radius` data units, with a light fill, the
    equator, and (grid > 0) a meridian and parallel grid every `grid` deg. The chapter's
    globes share one style: no grid (labels sit on the globe), the equator, and axis(). Positions are 3-D vectors
    in units of the sphere radius: z toward the north pole, x toward longitude 0 (a
    non-rotating frame). Lines behind the sphere are dashed (orbits) or left out (lines on
    the surface). Example: g = Globe(ax, view_lat=20, view_lon=-30); g.circle(1.6, inc=40, role="initial")"""

    FILL = "#EAF1F8"
    GRIDC = "#808B96"          # 3.0:1 on the globe fill, drawn thin (0.5 pt)

    def __init__(self, ax, center=(0.0, 0.0), radius=1.0, view_lat=20.0, view_lon=0.0, fill=None, grid=0,
                 equator=True, grid_lon0=0.0, zorder=1):
        self.ax, self.c, self.R, self.z = ax, np.asarray(center, dtype=float), radius, zorder
        f, l = math.radians(view_lat), math.radians(view_lon)
        self.e_view = np.array([math.cos(f) * math.cos(l), math.cos(f) * math.sin(l), math.sin(f)])
        self.e_east = np.array([-math.sin(l), math.cos(l), 0.0])
        self.e_north = np.cross(self.e_view, self.e_east)
        self.planes = []                     # (unit normal, radius) of the planes drawn with plane()
        ax.add_patch(Circle(tuple(self.c), radius, fc=fill or self.FILL, ec="none", zorder=zorder))
        ax.add_patch(Circle(tuple(self.c), radius, fc="none", ec=INK, lw=1.1, zorder=zorder + 0.6))
        if grid:
            for lon in np.arange(grid_lon0, grid_lon0 + 360.0, grid):
                self.meridian(lon, color=self.GRIDC, lw=0.5, zorder=zorder + 0.1, gid="globe-grid")
            for lat in np.arange(grid, 90.0, grid):
                self.parallel(lat, color=self.GRIDC, lw=0.5, zorder=zorder + 0.1, gid="globe-grid")
                self.parallel(-lat, color=self.GRIDC, lw=0.5, zorder=zorder + 0.1, gid="globe-grid")
        if equator:
            self.parallel(0.0, color=STEEL, lw=1.1, zorder=zorder + 0.2)

    # --- geometry
    @staticmethod
    def vec(lat, lon, r=1.0):
        """3-D position of latitude lat, longitude lon (deg) at radius r (sphere radii).
        Example: g.vec(28.5, -80.6)   # a launch site on the surface"""
        f, l = np.radians(lat), np.radians(lon)
        return r * np.array([np.cos(f) * np.cos(l), np.cos(f) * np.sin(l), np.sin(f) * np.ones_like(l)])

    @staticmethod
    def orbit_vec(radius, inc, raan, u):
        """3-D position on the circle of `radius` in the plane of inclination inc and ascending
        node raan (deg), at argument of latitude u (deg, from the ascending node).
        Example: node = g.orbit_vec(1.35, 40.0, 0.0, 0.0)   # the ascending node"""
        i, O, u = math.radians(inc), math.radians(raan), np.radians(u)
        return radius * np.array([math.cos(O) * np.cos(u) - math.sin(O) * np.sin(u) * math.cos(i),
                                  math.sin(O) * np.cos(u) + math.cos(O) * np.sin(u) * math.cos(i),
                                  np.sin(u) * math.sin(i)])

    def xy(self, P):
        """Projected 2-D data coordinates of 3-D point(s) P (shape (3,) or (3, n)).
        Example: x, y = g.xy(g.vec(0.0, 0.0))"""
        P = np.asarray(P, dtype=float)
        x, y = np.tensordot(self.e_east, P, 1), np.tensordot(self.e_north, P, 1)
        return np.array([self.c[0] + self.R * x, self.c[1] + self.R * y])

    def visible(self, P):
        """True where 3-D point(s) P are hidden neither by the (opaque) sphere nor by a plane
        drawn with plane() (a point below the equatorial plane, seen from above, is hidden
        where the plane's ring covers it).
        Example: g.visible(g.vec(0.0, 180.0))   # the far side: False"""
        P = np.asarray(P, dtype=float)
        depth = np.tensordot(self.e_view, P, 1)
        rho2 = np.sum(P * P, axis=0) - depth ** 2
        vis = (rho2 >= 1.0 - 1e-9) | (depth >= np.sqrt(np.clip(1.0 - rho2, 0.0, None)) - 1e-9)
        for n, rp in self.planes:
            nd = float(np.dot(n, self.e_view))
            if abs(nd) < 1e-9:
                continue
            t = -np.tensordot(n, P, 1) / nd                       # distance along the line of sight
            Q = P + np.multiply.outer(self.e_view, t) if P.ndim > 1 else P + t * self.e_view
            vis = vis & ~((t > 1e-9) & (np.sqrt(np.sum(Q * Q, axis=0)) <= rp))
        return vis

    # --- drawing
    def curve(self, P, hidden="dashed", role=None, zorder=None, **kw):
        """Draw the 3-D polyline P (3, n): visible runs in the role style (or **kw); hidden runs
        thin and dashed (hidden="dashed"), left out ("none") or as visible ("same").
        Example: g.curve(np.c_[node, node + 0.6 * east], color=STEEL, lw=LW_THIN)"""
        P = np.asarray(P, dtype=float)
        vis = self.visible(P)
        x, y = self.xy(P)
        for short, full in (("lw", "linewidth"), ("ls", "linestyle"), ("c", "color")):
            if short in kw:
                kw[full] = kw.pop(short)
        st = line_kw(role, **kw) if role else dict(kw)
        z = self.z + 2.0 if zorder is None else zorder
        hid = dict(st, linestyle=(0, (2.2, 2.2)), linewidth=min(1.1, st.get("linewidth", 1.0)))
        hid.pop("dash_capstyle", None)
        edges = np.flatnonzero(np.diff(vis.astype(int))) + 1
        self.last_lines = []
        for seg in np.split(np.arange(len(vis)), edges):
            if len(seg) == 0:
                continue
            ext = np.r_[seg, seg[-1] + 1] if seg[-1] + 1 < len(vis) else seg   # close the gap
            if vis[seg[0]]:
                self.last_lines += self.ax.plot(x[ext], y[ext], zorder=z, **st)
            elif hidden == "dashed":
                self.last_lines += self.ax.plot(x[ext], y[ext], zorder=z - 0.3, **hid)
            elif hidden == "same":
                self.last_lines += self.ax.plot(x[ext], y[ext], zorder=z, **st)
        return P

    def circle(self, radius=1.0, inc=0.0, raan=0.0, role="initial", hidden="dashed", u0=0.0, u1=360.0, n=721,
               arrows_at="auto", zorder=None, **kw):
        """Circle (an orbit, or a great circle when radius=1) of `radius` sphere radii in the
        plane (inc, raan) deg, from argument of latitude u0 to u1 deg, with arrow heads showing
        the motion (prograde, u increasing) at the arguments of latitude `arrows_at` (deg;
        "auto": one at the visible point nearest the viewer; (): none). Returns the 3-D points.
        Example: g.circle(1.25, inc=51.6, raan=40, role="initial")"""
        u = np.linspace(u0, u1, n)
        P = self.orbit_vec(radius, inc, raan, u)
        self.curve(P, hidden=hidden, role=role, zorder=zorder, **kw)
        lines = list(self.last_lines)
        if isinstance(arrows_at, str):
            vis = self.visible(P)
            depth = np.where(vis, np.tensordot(self.e_view, P, 1), -np.inf)
            arrows_at = (float(u[int(np.argmax(depth))]),) if vis.any() else ()
        col = kw.get("color", line_kw(role)["color"] if role else INK)
        for ua in arrows_at:
            tip = self.xy(self.orbit_vec(radius, inc, raan, ua))
            back = self.xy(self.orbit_vec(radius, inc, raan, ua - 0.5))
            rides_on(self.ax.add_patch(FancyArrowPatch(tuple(back), tuple(tip), mutation_scale=1.0, lw=0.8,
                                                     arrowstyle=ArrowStyle("-|>", head_length=MOTION_HEAD[0],
                                                                           head_width=MOTION_HEAD[1]),
                                                     color=col, shrinkA=0.0, shrinkB=0.0, joinstyle="miter",
                                                     zorder=(self.z + 2.0 if zorder is None else zorder) + 0.5)),
                   *lines)
        return P

    def parallel(self, lat, **kw):
        """A circle of latitude on the surface; the far side is left out.
        Example: g.parallel(30.0, color=STEEL, lw=0.8)"""
        return self.curve(self.vec(lat, np.linspace(0.0, 360.0, 361)), hidden="none", **kw)

    def meridian(self, lon, **kw):
        """A meridian on the surface; the far side is left out.
        Example: g.meridian(-80.6, color=STEEL, lw=0.8)"""
        return self.curve(self.vec(np.linspace(-90.0, 90.0, 181), lon), hidden="none", **kw)

    def great_arc(self, P0, P1, r=None, n=120, hidden="dashed", **kw):
        """Arc of the great circle from 3-D point P0 to P1 (shorter way), at radius r (default:
        the radius of P0). Returns the 3-D points.
        Example: g.great_arc(g.vec(28.5, -80.6), g.vec(0.0, -30.0), color=INK, lw=LW_THIN)"""
        P0, P1 = np.asarray(P0, dtype=float), np.asarray(P1, dtype=float)
        r = np.linalg.norm(P0) if r is None else r
        a, b = P0 / np.linalg.norm(P0), P1 / np.linalg.norm(P1)
        w = math.acos(max(-1.0, min(1.0, float(np.dot(a, b)))))
        s = np.linspace(0.0, 1.0, n)
        P = (np.outer(a, np.sin((1 - s) * w)) + np.outer(b, np.sin(s * w))) / math.sin(w) * r
        return self.curve(P, hidden=hidden, **kw)

    def arrow(self, P0, P1, **kw):
        """Projected arrow between 3-D points (see arrow() for the keywords).
        Example: g.arrow(node, node + 0.4 * along, color=BLUE)"""
        return arrow(self.ax, self.xy(P0), self.xy(P1), **kw)

    def point(self, P, label=None, direction=90.0, **kw):
        """Projected point marker with an optional label (see point()).
        Example: g.point(g.vec(28.5, -80.6), "launch site", direction=180)"""
        point(self.ax, self.xy(P), label, direction=direction, **kw)

    def text(self, P, s, **kw):
        """Text at the projection of 3-D point P (see text()).
        Example: g.text(g.vec(0.0, -10.0), "equator", direction=-90)"""
        return text(self.ax, self.xy(P), s, **kw)

    def callout(self, P, s, at, **kw):
        """Label at the 2-D data point `at` with a short leader to the projection of P (see callout()).
        Example: g.callout(node, "ascending node", at=(1.1, -1.1))"""
        return callout(self.ax, self.xy(P), s, at, **kw)

    def arc(self, origin, d0, d1, radius, label=None, dist=4.0, arrow_end=False, color=INK, lw=LW_THIN,
            fs=FS_LABEL, backing=True, label_at=0.5, zorder=None):
        """Angle arc in 3-D: about the point `origin`, from direction d0 to direction d1 (3-D
        vectors), of `radius` sphere radii, projected; label on the bisector (or at the fraction
        `label_at` of the arc, from d0), pushed out from the origin. Use it for the
        inclination at a node, an azimuth at a launch site, Omega or omega.
        Example: g.arc(node, east, along, 0.5, "$i$")   # inclination at the node"""
        o = np.asarray(origin, dtype=float)
        a = np.asarray(d0, dtype=float) / np.linalg.norm(d0)
        b = np.asarray(d1, dtype=float) / np.linalg.norm(d1)
        w = math.acos(max(-1.0, min(1.0, float(np.dot(a, b)))))
        s = np.linspace(0.0, 1.0, 60)
        D = (np.outer(a, np.sin((1 - s) * w)) + np.outer(b, np.sin(s * w))) / math.sin(w)
        x, y = self.xy(o[:, None] + radius * D)
        z = self.z + 3.0 if zorder is None else zorder
        arc = self.ax.plot(x, y, color=color, lw=lw, zorder=z)[0]
        if arrow_end:
            rides_on(arrow(self.ax, (x[-4], y[-4]), (x[-1], y[-1]), color=color, lw=lw, head="small", zorder=z), arc)
        if label:
            mid = self.xy(o + radius * D[:, int(round(59 * label_at))])
            ang = _screen_angle(self.ax, mid - self.xy(o))
            text(self.ax, mid, label, direction=ang, dist=dist, fs=fs, color=color, backing=backing, zorder=z + 4)

    def axis(self, length=1.4, label="N", south=True, color=INK, lw=LW_THIN):
        """The rotation axis: from the north pole out to `length` sphere radii (and from the
        south pole when south=True); the part inside the sphere is not drawn.
        Example: g.axis(1.5)"""
        z = np.linspace(1.0, length, 50)
        zero = np.zeros_like(z)
        self.curve(np.array([zero, zero, z]), hidden="none", color=color, lw=lw)
        if label:
            text(self.ax, self.xy([0.0, 0.0, length]), label, direction=90.0, dist=3.0, color=color)
        if south:
            self.curve(np.array([zero, zero, -z]), hidden="none", color=color, lw=lw)

    def plane(self, radius, inc=0.0, raan=0.0, fill="#F7F3E8", edge=GRAY, alpha=1.0):
        """The ring of a plane (inc, raan) between the sphere and `radius` sphere radii: the far
        half is drawn under the sphere, the near half over it, both with a thin edge. Call it
        before drawing orbits: from then on, curves hidden by the ring are dashed.
        Example: g.plane(2.0)   # the equatorial plane"""
        i, O = math.radians(inc), math.radians(raan)
        self.planes.append((np.array([math.sin(O) * math.sin(i), -math.cos(O) * math.sin(i), math.cos(i)]), radius))
        u = np.linspace(0.0, 360.0, 721)
        outer = self.orbit_vec(radius, inc, raan, u)
        depth = np.tensordot(self.e_view, outer, 1)
        u_front = u[np.argmax(depth)]
        for k, (lo, hi) in enumerate(((u_front + 90.0, u_front + 270.0), (u_front - 90.0, u_front + 90.0))):
            uu = np.linspace(lo, hi, 361)
            o = self.xy(self.orbit_vec(radius, inc, raan, uu))
            i = self.xy(self.orbit_vec(1.0, inc, raan, uu[::-1]))
            poly = np.c_[np.r_[o[0], i[0]], np.r_[o[1], i[1]]]
            z = self.z - 0.5 if k == 0 else self.z + 1.0
            self.ax.add_patch(Polygon(poly, closed=True, fc=fill, ec="none", alpha=alpha, zorder=z))
            self.ax.plot(o[0], o[1], color=edge, lw=0.8, zorder=z + 0.05, gid="edge")
            if k == 1:                                   # where the plane meets the sphere
                self.ax.plot(i[0], i[1], color=STEEL if inc == 0 else edge, lw=1.1 if inc == 0 else 0.8,
                             zorder=z + 0.05)


# ===================================================================== saving
WRITTEN = set()          # figure names written in this run (the runner reports stale files)
_NAME = re.compile(r"p2\d-[a-z0-9]+(?:-[a-z0-9]+)*")


def _contrast(c, bg=(1.0, 1.0, 1.0)):
    from matplotlib.colors import to_rgb

    def lum(rgb):
        v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    a, b = lum(to_rgb(c)), lum(bg)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def contrast_ratio(color, background="white"):
    """WCAG contrast ratio of a color against a background (default white).
    Example: contrast_ratio(BLUE) -> 5.19"""
    from matplotlib.colors import to_rgb
    return _contrast(color, to_rgb(background))


def _densify(xy, step=1.5):
    """Display-space polyline -> points no more than `step` px apart (NaN breaks kept out)."""
    xy = np.asarray(xy, dtype=float)
    xy = xy[np.all(np.isfinite(xy), axis=1)] if len(xy) else xy
    if len(xy) < 2:
        return xy
    seg = np.diff(xy, axis=0)
    n = np.maximum(1, np.ceil(np.hypot(seg[:, 0], seg[:, 1]) / step).astype(int))
    pts = [xy[:-1][i] + np.outer(np.arange(k) / k, seg[i]) for i, k in enumerate(n)]
    return np.vstack(pts + [xy[-1:]])


def _min_dist(A, B):
    """Smallest distance from each point of A (n, 2) to the point set B (m, 2), display px."""
    A, B = np.asarray(A, dtype=float), np.asarray(B, dtype=float)
    if len(A) == 0 or len(B) == 0:
        return np.full(len(A), np.inf)
    out = np.empty(len(A))
    for i in range(0, len(A), 256):
        d = A[i:i + 256, None, :] - B[None, :, :]
        out[i:i + 256] = np.sqrt(np.min(np.einsum("ijk,ijk->ij", d, d), axis=1))
    return out


def _group(artist):
    """The drawing group of an artist (gid "grp:..."): the parts of one dimension, for example."""
    g = artist.get_gid()
    return g if isinstance(g, str) and g.startswith("grp:") else None


def _head_samples(head, px_per_pt, apex_free=2.5):
    """Points that fill an arrowhead triangle (display px), leaving out the part within
    `apex_free` points of its tip: the tip may end on the line it points at."""
    v = np.asarray(head.vertices, dtype=float)[:3]
    apex, c1, c2 = v[1], v[0], v[2]
    pts = []
    for s in np.linspace(0.0, 1.0, 15):
        for t in np.linspace(0.0, 1.0, 9):
            pts.append(apex + s * ((1 - t) * (c1 - apex) + t * (c2 - apex)))
    pts = np.array(pts)
    return pts[np.hypot(*(pts - apex).T) > apex_free * px_per_pt], apex, 0.5 * (c1 + c2)


LABEL_CLEAR = 0.5            # pt of clear space between a label (its backing box) and any mark


def _region_contains(art, target):
    """True when `art` outlines a filled region (a patch with a face, a globe outline, or a line
    tagged gid "edge", the edge of a filled band or plane) that contains the display point
    `target`. Orbit lines never count."""
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    if art is None or target is None:
        return False
    if isinstance(art, Patch):
        path = art.get_transform().transform_path(art.get_path())
    elif isinstance(art, Line2D) and art.get_gid() == "edge":
        xy = art.get_transform().transform(np.c_[art.get_xdata(), art.get_ydata()].astype(float))
        from matplotlib.path import Path as _P
        path = _P(xy)
    else:
        return False
    return bool(path.contains_point(target))


def layout_problems(fig):
    """Check a drawn figure against FIGURE_STANDARD.md items 10, 11 and 17 and return a list of
    problems, in every axes (panel) of the figure:
      - a label (with its white backing box) that touches or crosses a line, an arrow, a marker,
        a body outline, an axes frame line or a tick mark, or another label;
      - a leader that crosses a line, an arrow, a marker, an outline or another label on its way
        (its last 7 pt, where it meets the point it names, are exempt; so is the outline of a
        filled region that contains that point: a body, a globe, a band or plane edge tagged
        gid "edge", a sector; never an orbit line; and the faint grid of a globe);
      - an arrowhead that lies on another line, arrow, marker or arrowhead (the tip may end on a
        line; only the arrowhead's own line, recorded with rides_on(), is exempt);
      - text below 10 pt; text with less than 4.5:1 contrast, or a line or mark with less than
        3:1, on white.
    Grid lines are exempt (decorative), and so is a dimension label placed on its line
    (label_side=0). The parts of one drawing group (gid "grp:...", for example a dimension)
    may touch each other. save_figure() runs it, then pixel_problems(), on every figure.
    Example: layout_problems(fig) -> []"""
    from matplotlib.patches import Patch, FancyArrowPatch as FAP
    from matplotlib.text import Text
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    px = fig.dpi / 72.0                                   # display px per point
    probs = []
    texts = []
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip() or t.axes is None and t.figure is None:
            continue
        bb = Text.get_window_extent(t, rend)          # the text alone, without an annotation's arrow
        if t.get_bbox_patch() is not None and t.get_bbox_patch().get_visible():
            bb = t.get_bbox_patch().get_window_extent(rend)     # with its white backing, which must not cut a line
        if bb.width < 1 or bb.height < 1:
            continue
        texts.append((t, bb))
        if t.get_fontsize() < 10:
            probs.append(f"text {t.get_text()!r} is {t.get_fontsize():g} pt (10 pt at least)")
        if _contrast(t.get_color()) < 4.5:
            probs.append(f"text {t.get_text()!r}: contrast {_contrast(t.get_color()):.2f}:1 (4.5:1 needed)")
    # what labels must stay clear of: lines, markers, arrows, outlines, frames, ticks (display px)
    marks = []                     # dict(pts, rad, z, what, src, grp)

    def add(pts, rad, z, what, src, grp=None, art=None):
        marks.append(dict(pts=np.asarray(pts, dtype=float).reshape(-1, 2), rad=rad, z=z, what=what, src=src, grp=grp,
                          art=art))
    heads, leaders, burns, connectors = [], [], [], []
    for ax in fig.axes:
        grid = set(ax.get_xgridlines()) | set(ax.get_ygridlines())
        clip = ax.bbox
        for ln in ax.lines:
            if ln in grid or not ln.get_visible():
                continue
            xy = ln.get_transform().transform(np.c_[ln.get_xdata(), ln.get_ydata()].astype(float))
            col = ln.get_color()
            if ln.get_linestyle() not in ("None", "", " ") and ln.get_linewidth() > 0:
                pts = _densify(xy)
                if ln.get_clip_on() and len(pts):
                    pts = pts[(pts[:, 0] >= clip.x0) & (pts[:, 0] <= clip.x1) & (pts[:, 1] >= clip.y0) & (pts[:, 1] <= clip.y1)]
                add(pts, 0.5 * ln.get_linewidth() * px, ln.get_zorder(),
                    "a connector line" if ln.get_gid() == "connector" else "a line", id(ln), _group(ln), art=ln)
                if ln.get_gid() == "connector":
                    connectors.append((ln, pts, ax))
                if _contrast(col) < 3.0:
                    probs.append(f"line of color {col}: contrast {_contrast(col):.2f}:1 (3:1 needed)")
            if ln.get_marker() not in ("None", None, "", " ") and ln.get_markersize() > 0:
                rad = 0.5 * ln.get_markersize() * px
                add(xy[np.all(np.isfinite(xy), axis=1)], rad, ln.get_zorder() + 0.5, "a marker", id(ln), _group(ln))
                mc = ln.get_markeredgecolor()
                if _contrast(mc) < 3.0 and _contrast(ln.get_markerfacecolor()) < 3.0:
                    probs.append(f"marker of color {mc}: contrast below 3:1")
        # the frame and the tick marks of a visible axes
        if ax.axison:
            for sp in ax.spines.values():
                if sp.get_visible() and sp.get_linewidth() > 0:
                    path = sp.get_transform().transform_path(sp.get_path())
                    for poly in path.to_polygons(closed_only=False):
                        add(_densify(poly), 0.5 * sp.get_linewidth() * px, sp.get_zorder(), "the axes frame", id(sp))
            for axis in (ax.xaxis, ax.yaxis):
                for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                    for tl in (tick.tick1line, tick.tick2line):
                        if not (tick.get_visible() and tl.get_visible()) or tl.get_markersize() <= 0:
                            continue
                        b = tl.get_window_extent(rend)
                        if b.width <= 0 and b.height <= 0:
                            continue
                        if not (clip.x0 - 1 <= 0.5 * (b.x0 + b.x1) <= clip.x1 + 1 and clip.y0 - 1 <= 0.5 * (b.y0 + b.y1) <= clip.y1 + 1):
                            continue                       # a tick outside the view is not drawn
                        add(_densify([(b.x0, b.y0), (b.x1, b.y0), (b.x1, b.y1), (b.x0, b.y1), (b.x0, b.y0)]), 0.0,
                            2.0, "a tick mark", id(tl))
        arrows = [t.arrow_patch for t in ax.texts if getattr(t, "arrow_patch", None) is not None]
        for a in arrows:
            a._gate_axes = ax
        for pa in list(ax.patches) + arrows:
            if not pa.get_visible():
                continue
            if isinstance(pa, FAP):
                path, fillable = pa._get_path_in_displaycoord()
                paths = path if isinstance(path, list) else [path]
                fills = fillable if isinstance(fillable, list) else [fillable] * len(paths)
                if pa.get_gid() in ("leader", "connector"):
                    for pth in paths:
                        pts_l = _densify(pth.vertices, 1.0)
                        (leaders if pa.get_gid() == "leader" else connectors).append((pa, pts_l, ax))
                        add(pts_l, 0.5 * pa.get_linewidth() * px, pa.get_zorder(),
                            "a leader" if pa.get_gid() == "leader" else "a connector line", id(pa))
                    continue
                if pa.get_gid() == "burn":
                    burns.append((pa, _densify(paths[0].vertices, 1.0), ax))
                for pth, fl in zip(paths, fills):
                    for poly in pth.to_polygons(closed_only=False):
                        add(_densify(poly), 0.5 * pa.get_linewidth() * px + 0.5, pa.get_zorder(),
                            "an arrowhead" if fl else "an arrow", id(pa), _group(pa))
                    if fl and len(pth.vertices) >= 3:
                        heads.append((pa, pth, ax))
                if _contrast(pa.get_edgecolor()) < 3.0:
                    probs.append(f"arrow of color {pa.get_edgecolor()}: contrast below 3:1")
            elif isinstance(pa, Patch) and pa.get_edgecolor()[3] > 0 and pa.get_linewidth() > 0:
                for poly in pa.get_transform().transform_path(pa.get_path()).to_polygons(closed_only=False):
                    add(_densify(poly), 0.5 * pa.get_linewidth() * px, pa.get_zorder(), "an outline", id(pa), _group(pa),
                        art=pa)
    # opaque discs (bodies, the globe) hide what is drawn under them. The disc comes from the
    # drawn path: get_transform() of a Circle already holds its center and radius.
    discs = []
    for ax in fig.axes:
        for pa in ax.patches:
            if isinstance(pa, Circle) and pa.get_visible() and pa.get_facecolor()[3] > 0.99:
                v = pa.get_transform().transform_path(pa.get_path()).vertices
                c = 0.5 * (v.min(axis=0) + v.max(axis=0))
                r = 0.25 * float(np.sum(v.max(axis=0) - v.min(axis=0)))
                discs.append((c, r - 0.5, pa.get_zorder()))
    for m in marks:
        for c, r, zd in discs:
            if zd > m["z"] and len(m["pts"]):
                m["pts"] = m["pts"][np.hypot(m["pts"][:, 0] - c[0], m["pts"][:, 1] - c[1]) > r]
    # 1. labels against every mark
    for t, bb in texts:
        if t.get_gid() == "on-line" or t.axes is None:
            continue
        cl = LABEL_CLEAR * px                     # a label must keep this clear of every mark
        x0, y0, x1, y1 = bb.x0 - cl, bb.y0 - cl, bb.x1 + cl, bb.y1 + cl
        own = id(getattr(t, "arrow_patch", None))
        for m in marks:
            pts, rad = m["pts"], m["rad"]
            if len(pts) == 0 or m["src"] == own:
                continue
            inside = ((pts[:, 0] > x0 - rad) & (pts[:, 0] < x1 + rad) & (pts[:, 1] > y0 - rad) & (pts[:, 1] < y1 + rad))
            if inside.any():
                q = t.axes.transData.inverted().transform(pts[np.argmax(inside)])
                probs.append(f"label {t.get_text()!r} touches {m['what']} at data ({q[0]:.4g}, {q[1]:.4g})")
                break
    # 2. labels against labels
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            (ta, a), (tb, b) = texts[i], texts[j]
            if a.x0 < b.x1 - 0.5 and b.x0 < a.x1 - 0.5 and a.y0 < b.y1 - 0.5 and b.y0 < a.y1 - 0.5:
                probs.append(f"labels {ta.get_text()!r} and {tb.get_text()!r} overlap")
    # 3. leaders: clear of every mark and every other label on their way
    owner = {id(getattr(t, "arrow_patch", None)): t for t, _ in texts}
    for pa, pts, lax in leaders:
        t = owner.get(id(pa))
        name = repr(t.get_text()) if t is not None else "?"
        target = pa._posA_posB[1] if getattr(pa, "_posA_posB", None) else None
        if t is not None and hasattr(t, "xy"):
            target = t.get_transform().transform(t.xy) if t.xycoords == "data" else target
        if target is not None:
            pts = pts[np.hypot(*(pts - np.asarray(target)).T) > 7.0 * px]       # where it meets its point
        if t is not None:
            own_bb = dict(texts).get(t)
            if own_bb is not None:
                pts = pts[~((pts[:, 0] > own_bb.x0 - 1.5 * px) & (pts[:, 0] < own_bb.x1 + 1.5 * px)
                            & (pts[:, 1] > own_bb.y0 - 1.5 * px) & (pts[:, 1] < own_bb.y1 + 1.5 * px))]
        if len(pts) == 0:
            continue
        lrad = 0.5 * pa.get_linewidth() * px
        for m in marks:
            if len(m["pts"]) == 0 or m["src"] == id(pa):
                continue
            if _region_contains(m["art"], target):
                continue                     # a leader pointing into a filled region crosses its outline
            if m["art"] is not None and m["art"].get_gid() == "globe-grid":
                continue                     # the faint grid of a globe, like the grid of a plot
            d = _min_dist(pts, m["pts"])
            if np.any(d < m["rad"] + lrad + 0.5):
                q = lax.transData.inverted().transform(pts[int(np.argmin(d))])
                probs.append(f"leader of {name} crosses {m['what']} at data ({q[0]:.4g}, {q[1]:.4g})")
                break
        for tb, b in texts:
            if tb is t:
                continue
            if np.any((pts[:, 0] > b.x0) & (pts[:, 0] < b.x1) & (pts[:, 1] > b.y0) & (pts[:, 1] < b.y1)):
                probs.append(f"leader of {name} crosses the label {tb.get_text()!r}")
    # 3b. connector lines (zoom lines between panels): they cross no line, arrow, leader or label;
    # only the artists they are drawn to meet (connects()) may touch them, and only at their ends
    for ca, pts, cax in connectors:
        if len(pts) < 2:
            continue
        touch = getattr(ca, "_touches", ())
        crad = 0.5 * ca.get_linewidth() * px
        for m in marks:
            if m["src"] == id(ca) or len(m["pts"]) == 0:
                continue
            q_pts = pts
            if m["src"] in touch:                 # its own end circles or frames: only the ends may meet them
                q_pts = pts[(np.hypot(*(pts - pts[0]).T) > 15.0 * px) & (np.hypot(*(pts - pts[-1]).T) > 15.0 * px)]
                if len(q_pts) == 0:
                    continue                       # (a tangent stays near its circle for some points)
            d = _min_dist(q_pts, m["pts"])
            if np.any(d < m["rad"] + crad + 0.3):
                q = cax.transData.inverted().transform(q_pts[int(np.argmin(d))])
                col = m["art"].get_edgecolor() if hasattr(m["art"], "get_edgecolor") and not hasattr(m["art"], "get_xdata") \
                    else (m["art"].get_color() if m["art"] is not None else "")
                from matplotlib.colors import to_hex
                col = f" {to_hex(col)}" if col is not None and len(str(col)) else ""
                probs.append(f"connector line crosses {m['what']}{col} at data ({q[0]:.4g}, {q[1]:.4g})")   # every one
        for tb, b in texts:
            if np.any((pts[:, 0] > b.x0) & (pts[:, 0] < b.x1) & (pts[:, 1] > b.y0) & (pts[:, 1] < b.y1)):
                probs.append(f"connector line crosses the label {tb.get_text()!r}")
    # 4. burn arrows beside the path, never on it (their first 2 pt may touch the burn dot)
    for pa, pts, bax in burns:
        pts = pts[np.hypot(*(pts - pts[0]).T) > 2.0 * px]
        brad = 0.5 * pa.get_linewidth() * px
        for m in marks:
            if m["src"] == id(pa) or m["what"] == "a marker" or len(m["pts"]) == 0 or len(pts) == 0:
                continue
            d = _min_dist(pts, m["pts"])
            if np.any(d < m["rad"] + brad + 0.5):
                q = bax.transData.inverted().transform(pts[int(np.argmin(d))])
                probs.append(f"burn arrow lies on {m['what']} at data ({q[0]:.4g}, {q[1]:.4g}): draw it beside the path")
                break
    # 5. arrowheads: clear of other lines, arrows, markers and arrowheads (not of the line they ride on)
    for pa, head, hax in heads:
        samp, apex, base = _head_samples(head, px)
        if len(samp) == 0:
            continue
        for m in marks:
            if m["src"] == id(pa) or len(m["pts"]) == 0 or (m["grp"] is not None and m["grp"] == _group(pa)):
                continue
            if (m["grp"] or "").startswith("grp:dim") and (_group(pa) or "").startswith("grp:dim"):
                continue                                       # chained dimensions share an end tick
            if m["art"] is not None and m["art"].get_gid() == "globe-grid":
                continue                                       # the faint grid of a globe, under an orbit's arrowhead
            if m["src"] in getattr(pa, "_rides", ()):
                continue                                       # the arrowhead's own line (its orbit, track or arc)
            d = _min_dist(samp, m["pts"])
            if np.any(d < m["rad"] + 0.5):
                q = hax.transData.inverted().transform(apex)
                probs.append(f"arrowhead at data ({q[0]:.4g}, {q[1]:.4g}) lies on {m['what']}")
                break
    return probs


PIXEL_DPI = 216.0              # 3 px per point, as in the figure review


def _blobs(mask, min_cells):
    """Connected groups (8-neighbors) of a mask downsampled to 1 cell per point (3 x 3 px)."""
    h, w = mask.shape
    m3 = mask[:h // 3 * 3, :w // 3 * 3].reshape(h // 3, 3, w // 3, 3).any(axis=(1, 3))
    seen = np.zeros_like(m3, dtype=bool)
    out = []
    for y0, x0 in zip(*np.nonzero(m3)):
        if seen[y0, x0]:
            continue
        stack, cells = [(y0, x0)], []
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            cells.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < m3.shape[0] and 0 <= xx < m3.shape[1] and m3[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        stack.append((yy, xx))
        if len(cells) >= min_cells:
            c = np.array(cells)
            out.append((len(cells), 3.0 * c[:, 1].mean() + 1.5, 3.0 * c[:, 0].mean() + 1.5))
    return out


def pixel_problems(fig, dpi=PIXEL_DPI, min_cells=3):
    """The pixel test of the gate: render the figure at 3 px per point with
    and without its text (glyphs and backing boxes), grid lines hidden in both, and report
      - line ink (a dark or colored pixel without the text) that a label's white backing turns white;
      - a light fill (a body, globe, plane or band) that a white backing covers: on a fill use a
        backing of the fill's color (text(..., backing=<color>)) or none.
    A group of `min_cells` square points or more is a problem. A dimension label placed on its
    line (label_side=0) is exempt. Example: pixel_problems(fig) -> []"""
    from matplotlib.text import Text
    texts = [t for t in fig.findobj(Text) if t.get_visible() and t.get_text().strip() and t.get_gid() != "on-line"]
    grids = [g for ax in fig.axes for g in ax.get_xgridlines() + ax.get_ygridlines() if g.get_visible()]
    old_dpi = fig.dpi
    saved = [(t, t.get_color(), t.get_bbox_patch().get_visible() if t.get_bbox_patch() is not None else None)
             for t in texts]
    try:
        for g in grids:
            g.set_visible(False)
        fig.set_dpi(dpi)
        fig.canvas.draw()
        A = np.asarray(fig.canvas.buffer_rgba())[..., :3].astype(int).copy()
        boxes = []
        rend = fig.canvas.get_renderer()
        for t in texts:
            bp = t.get_bbox_patch()
            bb = bp.get_window_extent(rend) if bp is not None and bp.get_visible() else Text.get_window_extent(t, rend)
            boxes.append((t, bb))
            t.set_color((0, 0, 0, 0))
            if bp is not None:
                bp.set_visible(False)
        fig.canvas.draw()
        B = np.asarray(fig.canvas.buffer_rgba())[..., :3].astype(int).copy()
    finally:
        for t, c, bv in saved:
            t.set_color(c)
            if bv is not None:
                t.get_bbox_patch().set_visible(bv)
        for g in grids:
            g.set_visible(True)
        fig.set_dpi(old_dpi)
        fig.canvas.draw()
    H = A.shape[0]
    white = A.min(axis=2) > 245
    ink = (B.min(axis=2) < 170) | ((B.max(axis=2) - B.min(axis=2)) > 80)
    fill = (~ink) & (B.min(axis=2) <= 240)

    def who(x, y):
        yd = H - y                                         # display y runs up
        for t, bb in boxes:
            if bb.x0 - 3 <= x <= bb.x1 + 3 and bb.y0 - 3 <= yd <= bb.y1 + 3:
                return repr(t.get_text())
        return "a label"
    probs = []
    for n, x, y in _blobs(white & ink, min_cells):
        probs.append(f"pixel test: {who(x, y)} hides {n} pt² of line ink")
    for n, x, y in _blobs(white & fill, min_cells):
        probs.append(f"pixel test: the white backing of {who(x, y)} shows over a fill ({n} pt²)")
    return probs


FONT_FAMILY = "Arial, Helvetica, sans-serif"


def _svg_fonts(svg_text):
    """Every font-family in the SVG, plain labels and math alike, becomes FONT_FAMILY, so a device
    without Arial falls back to a sans-serif font, never to a serif."""
    return re.sub(r"font-family: ?(?:'[^']*'|\"[^\"]*\"|[A-Za-z][\w -]*)(?: ?, ?(?:'[^']*'|\"[^\"]*\"|[A-Za-z][\w -]*))*",
                  "font-family: " + FONT_FAMILY, svg_text)


def svg_problems(svg_text):
    """Problems in an SVG written by save_figure(): a glyph in a font other than Arial (STIX and
    DejaVu fallbacks included), a text element without the font-family and its fallbacks, text
    smaller than 10 pt (single-letter sub- and superscripts inside a math label are allowed), or
    a subscript made of a word, or the infinity sign, smaller than 10.5 pt (it must read at 10 pt
    on the page). Example: svg_problems(svg_path.read_text()) -> []"""
    probs = []
    for fam in sorted(set(re.findall(r"font-family: ?([^;\"]+)", svg_text))):
        if fam.strip() != FONT_FAMILY:
            probs.append(f"font-family {fam.strip()!r}: every text must read {FONT_FAMILY!r}")
    for bad in ("STIX", "DejaVu Sans Mono", "cmr10", "cmmi10"):
        if bad in svg_text:
            probs.append(f"a glyph is set in {bad}, not Arial")
    for m in re.finditer(r"<text\b(.*?)</text>", svg_text, re.S):
        body = m.group(0)
        styled = re.findall(r"<(?:text|tspan)\b[^>]*style=\"([^\"]*)\"[^>]*>([^<]*)", body)
        for style, chars in styled:
            if chars.strip() and "font-family" not in style and "font-family" not in m.group(1):
                probs.append(f"text {chars!r} has no font-family")
        sizes = [float(s) for s in re.findall(r"font(?:-size)?:[^;\"]*?([\d.]+)px", body)]
        plain = re.sub(r"<[^>]+>", "", body.split(">", 1)[1]).strip()
        if sizes and max(sizes) < 10.0:
            probs.append(f"text {plain!r} is {max(sizes):g} pt, below 10 pt")
        if sizes:
            main = max(sizes)
            runs = []                                   # runs of glyphs set smaller than the main size
            for size, chars in re.findall(r"<tspan\b[^>]*font-size: ([\d.]+)px[^>]*>([^<]*)", body):
                size = float(size)
                if size < main and runs and runs[-1][0] == size:
                    runs[-1][1] += chars
                elif size < main:
                    runs.append([size, chars])
                else:
                    runs.append([size, None])
            for size, chars in runs:
                if chars and (re.search(r"[A-Za-z]{2,}", chars) or "∞" in chars) and size < 10.5:
                    probs.append(f"subscript {chars!r} of {plain!r} is {size:g} pt (10.5 pt at least for a word or ∞)")
    return probs


def save_figure(fig, name, allow=()):
    """Save notes/chapter-2/figures/<name>.svg through make_figures.save() (live text, Arial,
    deterministic; PNG copy when FIG_PREVIEW is set). Before saving, layout_problems() checks
    the drawing (labels, leaders and arrowheads clear of lines, frames, ticks, marks and other
    labels; sizes; contrast) and pixel_problems() renders it with and without its text to find
    any line a label's backing box hides and any backing box over a fill. After saving, every
    font-family is set to Arial with its fallbacks and the SVG is checked (every glyph in Arial,
    no text below 10 pt, word subscripts readable). Any problem stops the run, except those
    whose text contains one of the strings in `allow` (give the reason in a comment next to
    it). With FIG_LAYOUT=warn in the environment the problems are printed and the figure is
    saved anyway (draft mode). The name starts with the page tag: "p21-ellipse-geometry".
    Example: save_figure(fig, "p21-ellipse-geometry")"""
    if not _NAME.fullmatch(name):
        raise ValueError(f"figure name {name!r}: use <tag>-<name> in lower case, e.g. p21-ellipse-geometry")
    w = fig.get_size_inches()[0]
    if w > 7.5:
        print(f"note: {name} is {w:.1f} in wide; the usual width is {FIG_WIDTH} in")
    found = layout_problems(fig) + pixel_problems(fig)
    lay = [p for p in found if not any(a in p for a in allow)]
    if lay and os.environ.get("FIG_LAYOUT") == "warn":       # draft mode: report and save anyway
        print(f"   LAYOUT {name}:\n     " + "\n     ".join(lay))
    elif lay:
        plt.close(fig)
        raise AssertionError(f"{name}: " + "; ".join(lay))
    save(fig, name, chapter=2)
    WRITTEN.add(name)
    path = NOTES / "chapter-2" / "figures" / f"{name}.svg"
    raw = path.read_text(encoding="utf-8")
    probs = [f"glyph {g!r} set in {fam}, not Arial (write the character, e.g. ° not ^\\circ, √ not \\sqrt)"
             for fam, g in re.findall(r"font-family: ?'([^']+)'[^>]*>([^<]*)<", raw) if fam != "Arial"]
    svg = _svg_fonts(raw)
    path.write_text(svg, encoding="utf-8")
    probs += svg_problems(svg)
    if probs and os.environ.get("FIG_LAYOUT") == "warn":
        print(f"   SVG {name}:\n     " + "\n     ".join(probs))
    elif probs:
        raise AssertionError(f"{name}.svg: " + "; ".join(probs))
    m = re.search(r'<svg[^>]*width="([\d.]+)pt" height="([\d.]+)pt"', svg)
    if m:
        w_in, h_in = float(m.group(1)) / 72.0, float(m.group(2)) / 72.0
        pct = int(min(100, max(40, 5 * round(w_in / FIG_WIDTH * 85 / 5))))
        print(f"   {name}.svg: {w_in:.2f} x {h_in:.2f} in; :width: {pct}% shows its text at the size of the body text")


def close_to(a, b, tol, what):
    """Assert |a - b| <= tol with a message naming the check. Example: close_to(rp, 7078.0, 1e-6, "rp")"""
    assert abs(a - b) <= tol, f"{what}: {a!r} vs {b!r} (tolerance {tol})"


# ===================================================================== unit checks
if __name__ == "__main__":
    E, RE = MU["Earth"], RADIUS["Earth"]

    vc, ve = float(circular_speed(E, RE)), float(escape_speed(E, RE))
    close_to(vc, 7.9054, 5e-4, "circular speed at Earth's surface")
    close_to(ve, 11.1798, 5e-4, "escape speed at Earth's surface")
    assert fmt(vc, 2) == "7.9" and fmt(ve, 3) == "11.2", (fmt(vc, 2), fmt(ve, 3))
    close_to(float(escape_speed(E, 7000.0) / circular_speed(E, 7000.0)), math.sqrt(2.0), 1e-12, "v_esc = sqrt(2) v_c")

    T400 = float(period(E, RE + 400.0)) / 60.0
    assert fmt(T400) == "92.56", T400          # 92.4 min needs R = 6,371 km; the book uses 6,378 km
    close_to(float(semi_major_axis_from_period(E, period(E, 12345.0))), 12345.0, 1e-6, "a from T round trip")

    h = hohmann(E, RE + 400.0, RE + 20200.0)
    close_to(h["a_t"] * (1 - h["e_t"]), h["r1"], 1e-6, "transfer periapsis touches the inner circle")
    close_to(h["a_t"] * (1 + h["e_t"]), h["r2"], 1e-6, "transfer apoapsis touches the outer circle")
    assert h["dv1"] > 0 and h["dv2"] > 0 and h["raise"]
    close_to(h["tof"], 0.5 * float(period(E, h["a_t"])), 1e-6, "tof is half the transfer period")
    close_to(h["dv_total"], h["dv1"] + h["dv2"], 1e-12, "total")
    close_to(float(vis_viva(E, h["r1"], h["a_t"])) * h["r1"], float(vis_viva(E, h["r2"], h["a_t"])) * h["r2"],
             1e-9, "angular momentum r v the same at both apsides")
    hd = hohmann(E, RE + 20200.0, RE + 400.0)
    close_to(hd["dv_total"], h["dv_total"], 1e-12, "going down costs the same")
    assert not hd["raise"]

    close_to(float(surface_speed(0.0, RADIUS["Earth"])), 0.4651, 5e-5, "rotation speed at the equator, R = 6,378 km")
    close_to(float(surface_speed(0.0)), 0.4646, 5e-5, "rotation speed at the equator, mean radius 6,371 km")
    assert fmt(float(surface_speed(0.0))) == "0.4646", surface_speed(0.0)
    close_to(float(rotation_gain(30.4, launch_azimuths(30.4, 40.0)[0])),
             OMEGA_EARTH * RADIUS_EARTH_MEAN * math.cos(math.radians(40.0)), 1e-12, "rotation gain = omega R cos i")
    close_to(G_SI * 5.972e24 / 1e9, MU["Earth"], 0.002 * MU["Earth"], "G M of Earth agrees with mu")
    assert "Mars" not in SUN_DISTANCE and "Mars" not in ORBIT_DAYS, "PLAN rule 4"
    close_to(SUN_DISTANCE["Neptune"] / AU, 30.07, 1e-12, "Neptune distance")
    close_to(float(inclination_from_launch(40.0, 90.0)), 40.0, 1e-9, "due east: i = latitude")
    for lat, inc in ((28.5, 51.6), (30.4, 40.0), (40.0, 90.0), (5.2, 98.2), (34.7, 145.0), (0.0, 0.0)):
        for az in launch_azimuths(lat, inc):
            close_to(float(inclination_from_launch(lat, az)), inc, 1e-7, f"azimuth round trip {lat}, {inc}")
    try:
        launch_azimuths(40.0, 30.0)
        raise AssertionError("an inclination below the latitude must raise")
    except ValueError:
        pass
    close_to(float(rotation_gain(40.0, 270.0)), -float(rotation_gain(40.0, 90.0)), 1e-12, "westward loses")

    assert energy_from_state(E, 7000.0, 7.0) < 0
    close_to(float(energy_from_state(E, 7000.0, float(escape_speed(E, 7000.0)))), 0.0, 1e-9, "parabola: zero energy")
    assert energy_from_state(E, 7000.0, 12.0) > 0
    close_to(float(energy_from_state(E, 7000.0, vis_viva(E, 7000.0, 9000.0))), float(specific_energy(E, 9000.0)),
             1e-9, "energy from state = -mu/2a")

    S = synodic_period(ORBIT_DAYS["Venus"], ORBIT_DAYS["Earth"])
    close_to(S, 583.9, 0.1, "synodic period of Venus, days")

    a_e, e_e = 9628.0, 0.2648
    T = float(period(E, a_e))
    close_to(float(time_from_periapsis(E, a_e, e_e, 180.0)), T / 2.0, 1e-6, "periapsis to apoapsis: T/2")
    close_to(float(time_from_periapsis(E, a_e, e_e, 540.0)), 1.5 * T, 1e-6, "one more turn adds T")
    close_to(float(time_from_periapsis(E, a_e, e_e, -90.0)), -float(time_from_periapsis(E, a_e, e_e, 90.0)), 1e-9, "odd")
    for th in (10.0, 135.0, 179.0, 300.0, 700.0):
        close_to(float(true_anomaly_at_time(E, a_e, e_e, time_from_periapsis(E, a_e, e_e, th))), th, 1e-7, "Kepler")
    g = hyperbola(E, 6563.0, 3.0)
    for th in (20.0, 80.0, 110.0):
        close_to(float(true_anomaly_at_time(E, g["a"], g["e"], time_from_periapsis(E, g["a"], g["e"], th))), th, 1e-7,
                 "hyperbolic Kepler")
    close_to(float(vis_viva(E, 6563.0, g["a"])), g["vp"], 1e-9, "hyperbola periapsis speed by vis-viva")
    close_to(float(conic_radius(g["p"], g["e"], g["theta_inf"] - 1e-9)) > 1e9, True, 0, "asymptote at theta_inf")

    x, y = orbit_xy(a_e, e_e)
    close_to(float(np.max(x)), a_e * (1 - e_e), 1e-6, "periapsis on +x")
    close_to(float(np.min(x)), -a_e * (1 + e_e), 1e-6, "apoapsis on -x")
    x, y = orbit_xy(g["a"], g["e"], r_max=50000.0)
    close_to(float(np.max(np.hypot(x, y))), 50000.0, 1e-6, "hyperbola clipped at r_max")
    v = orbit_velocity(E, a_e, e_e, 0.0)
    close_to(float(np.hypot(*v)), float(vis_viva(E, a_e * (1 - e_e), a_e)), 1e-9, "velocity vector magnitude")
    lat, lon = ground_track(98.2, 5928.0, np.linspace(0, 5928.0, 2001))
    close_to(float(np.max(lat)), 180.0 - 98.2, 1e-3, "track reaches 180 - i for a retrograde orbit")

    # Mercury example of 2.4 (the deck's values): planet speeds, v-infinity, burns, trip time
    Ms, rE, rM = MU["Sun"], SUN_DISTANCE["Earth"], SUN_DISTANCE["Mercury"]
    hm = hohmann(Ms, rE, rM)
    vinf_d, vinf_a = hm["v_c1"] - hm["v_t1"], hm["v_t2"] - hm["v_c2"]
    dv_dep = float(periapsis_speed_hyperbola(E, RE + 185.0, vinf_d) - circular_speed(E, RE + 185.0))
    dv_cap = float(periapsis_speed_hyperbola(MU["Mercury"], RADIUS["Mercury"] + 400.0, vinf_a)
                   - circular_speed(MU["Mercury"], RADIUS["Mercury"] + 400.0))
    got = [fmt(v) for v in (hm["v_c1"], hm["v_t1"], vinf_d, dv_dep, hm["v_t2"], hm["v_c2"], vinf_a, dv_cap)]
    assert got == ["29.78", "22.25", "7.534", "5.557", "57.49", "47.87", "9.613", "7.604"], got  # deck: 47.88
    assert fmt(hm["tof"] / DAY, 3) == "105", hm["tof"] / DAY

    # fmt: sig figs; integer digits are never rounded away; half up; commas; trailing zeros kept
    cases = [((26578.3,), "26,578"), ((7.66912,), "7.669"), ((0.264786,), "0.2648"), ((105.4, 3), "105"),
             ((105.4,), "105.4"), ((5828.5,), "5,829"), ((2.4, 3), "2.40"), ((9.99996,), "10.00"),
             ((-0.04512, 2), "-0.045"), ((1234567.0,), "1,234,567"), ((0.0,), "0.000"), ((0.5, 1), "0.5")]
    for args, want in cases:
        assert fmt(*args) == want, (args, fmt(*args), want)
    assert fmt_dec(5828.46, 1) == "5,828.5" and fmt_dec(5828.5, 1) == "5,828.5" and fmt_dec(468.35, 1) == "468.4"
    assert fmt_dec(0.125, 2) == "0.13" and fmt_dec(-1234.5, 0) == "-1,235"
    assert fmt(-3.21, minus="−") == "−3.210"
    assert fmt_sci(MU["Sun"]) == "1.327 \\times 10^{11}" and fmt_sci(OMEGA_EARTH) == "7.292 \\times 10^{-5}"
    assert fmt_sci(MU["Earth"]) == "3.986 \\times 10^{5}" and fmt_sci(5.0) == "5.000"
    print("orbits.py: all unit checks passed")
    print(f"  v_c(R_E) = {vc:.4f} km/s, v_esc(R_E) = {ve:.4f} km/s, T(400 km) = {T400:.2f} min, "
          f"S(Venus) = {S:.1f} d, surface speed = {float(surface_speed(0.0)):.4f} km/s (mean radius)")
