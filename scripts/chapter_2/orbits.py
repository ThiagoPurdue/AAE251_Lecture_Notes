"""Shared code for Chapter 2, Introduction to Orbits: constants, orbit equations, and the
orbit drawing helpers of the chapter figures, on top of the book's figure kit
(scripts/figkit.py: style, text and arrow helpers, number formatting, the layout gate,
save_figure and the record of printed values, all re-exported here).

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
import math
import sys
from pathlib import Path

if __name__ not in ("chapter_2.orbits", "__main__"):
    raise ImportError("import this module as chapter_2.orbits (from chapter_2.orbits import ...), "
                      "not as a bare 'orbits': the value record must be one object")

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from figkit import *  # noqa: E402,F401,F403  (the figure kit: style, helpers, gate, fmt)
from figkit import _anchor, _backing, _screen_angle, _style, _tip_shrink  # noqa: E402
from make_figures import plt, np, save, NOTES, INK, GOLD, DUST, LIGHT, AGED, STEEL, SERIES  # noqa: E402,F401
import matplotlib.ticker as mticker  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, ArrowStyle  # noqa: E402
from matplotlib.text import OffsetFrom  # noqa: E402

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
G0 = 9.81                   # m/s^2: 9.81 m/s^2, the value used throughout the course (the rocket equation uses it)
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


# ===================================================================== the record of printed values
PAGES = {
    "p21": "orbit-properties",
    "p22": "orbit-transfers",
    "p23": "launch-to-orbit",
    "p24": "patched-conics",
    "p25": "ground-tracks-and-orbit-lifetime",
}
CHAPTER = Chapter(2, PAGES, Path(__file__).resolve().parent)
VALUES, VALUES_FILE, WRITTEN = CHAPTER.VALUES, CHAPTER.VALUES_FILE, CHAPTER.WRITTEN
record, write_values, save_figure = CHAPTER.record, CHAPTER.write_values, CHAPTER.save_figure


# ===================================================================== orbit roles and body fills
# Orbit roles: one look across the chapter. color = the line, text = a label in that hue
# with at least 4.5:1 on white. Each role differs by line style as well as by color.
register_roles({
    "initial":   dict(color=BLUE, text=BLUE, ls="-", lw=LW_ORBIT),                       # initial or parking orbit
    "transfer":  dict(color=VERMILION, text="#B34E00", ls=(0, (5.0, 2.5)), lw=LW_ORBIT),  # transfer orbit
    "final":     dict(color=GREEN, text="#007A5A", ls=(0, (7.0, 2.2, 1.4, 2.2)), lw=LW_ORBIT),   # final or target
    "hyperbola": dict(color=PURPLE, text="#A0507F", ls=(0, (6.0, 1.8, 1.2, 1.8, 1.2, 1.8)), lw=LW_ORBIT),
    "other":     dict(color=INK, text=INK, ls=(0, (0.1, 2.2)), lw=LW_ORBIT, cap="round"),  # dotted black
}, ["initial", "transfer", "final", "hyperbola", "other"])     # into the kit's STYLE and SEQUENCE
BODY_FILL = {"Sun": "#F7E3A3", "Mercury": "#E4DFD8", "Venus": "#F2E4C8", "Earth": "#D7E7F5",
             "Moon": "#E6E6E6", "Mars": "#F1D6C8", "Jupiter": "#EFE1CC", "Saturn": "#F3E8CB"}
BODY_DEFAULT = "#E3EAF2"


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
