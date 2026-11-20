"""Figures and values of the page "Ground tracks, aerobraking, and orbit lifetime"
(notes/chapter-2/ground-tracks-and-orbit-lifetime.md).

The computations follow the ground-track, aerobraking and lifetime examples of the course
slides, with the constants of orbits.py, and assert the values the slides print. Run through the runner from the book folder:

    FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_2_figures.py p25

Helpers this module adds (orbits.py lacks them): _map_frame() sets up a latitude and
longitude grid on an existing axes (map_axes() always makes its own figure), and
_log_days() puts plain day labels on a log axis.
"""
from chapter_2.orbits import *

PAGE = "p25"
E, RE = MU["Earth"], RADIUS["Earth"]
V, RV = MU["Venus"], RADIUS["Venus"]

# ---- ground tracks and coverage: the deck's Earth-observation example
H_GT = 700.0               # altitude, km
INC_GT = 98.2              # inclination, deg (retrograde, near polar)
FOV = 15.0                 # field of view of the instrument, deg

# Landsat 8, the real check (USGS, Landsat 8 Data Users Handbook): 705 km, 98.2 deg,
# 185 km swath, the track repeats after 233 orbits in 16 days.
LANDSAT = dict(h=705.0, inc=98.2, swath=185.0, days=16, orbits=233)

# ---- aerobraking: the deck's Venus orbiter
M_SC, ISP = 1200.0, 320.0          # kg, s
HP0, HA0, HC = 250.0, 25000.0, 250.0   # capture orbit periapsis and apoapsis, final circle, km altitude
HP_AB = 140.0                      # periapsis altitude during aerobraking, km
AERO_STEPS = (15000.0, 7000.0)     # apoapsis altitudes drawn between, km (illustrative); two, so the
                                   # burn at the final circle has room

# ---- orbit lifetime: US Standard Atmosphere 1976 densities (kg/m^3) at altitudes in km,
# exponential between the table points (as in the deck script)
DENS = [(150, 2.076e-9), (200, 2.541e-10), (250, 6.073e-11), (300, 1.916e-11), (350, 7.014e-12),
        (400, 2.803e-12), (450, 1.184e-12), (500, 5.215e-13), (600, 1.137e-13)]
B_LIFE = 100.0                     # ballistic coefficient m/(C_D A), kg/m^2
H_END = 150.0                      # the decay is followed down to this altitude, km
STARTS = (300.0, 400.0, 500.0)
L0_TRACK = 45.0                    # ascending node of the first orbit in the ground-track figure, deg E
X_MIN = 0.5                        # left edge of the log time axis, days

GC_ORBIT_U = 60.0                  # great-circle figure: the orbit's arrowhead, deg from the node
GC_TRACK_U = 40.0                  # great-circle figure: the track's arrowhead on the globe, deg from the node
INC_PERIOD = 40.0                  # inclination of the orbits that compare periods, deg
GEO_LON = 60.0                     # longitude of the geostationary point drawn, deg


# ===================================================================== computations
def coverage():
    """The deck's coverage example: period, westward shift, spacing, swath, days to cover."""
    a = RE + H_GT
    T = float(period(E, a))
    c = dict(a=a, T=T, T_min=T / 60.0)
    c["dL"] = 360.0 * T / T_SIDEREAL                          # westward shift per orbit, deg
    c["spacing"] = 2.0 * np.pi * RE * T / T_SIDEREAL          # at the equator, km
    c["swath"] = 2.0 * H_GT * math.tan(math.radians(FOV / 2.0))
    c["per_day"] = DAY / T                                   # orbits per (solar) day
    c["ground_day"] = c["swath"] * c["per_day"]               # km of equator imaged per day
    c["equator"] = 2.0 * np.pi * RE
    c["days"] = c["equator"] / c["ground_day"]
    c["rate"] = 360.0 / (T_SIDEREAL / 3600.0)                 # deg per hour Earth turns
    c["max_lat"] = 180.0 - INC_GT
    # reading the period back off the track: T = dL/360 x T_day, then a from the period
    c["T_back"] = c["dL"] / 360.0 * T_SIDEREAL
    c["a_back"] = float(semi_major_axis_from_period(E, c["T_back"]))
    # Landsat 8: orbits per day, spacing of neighboring paths at the equator after 16 days
    c["ls_per_day"] = LANDSAT["orbits"] / LANDSAT["days"]
    c["ls_path"] = c["equator"] / LANDSAT["orbits"]
    # the values the course slides print
    for k, deck, tol in (("T_min", 98.8, 0.05), ("dL", 24.8, 0.05), ("spacing", 2756.0, 0.5),
                         ("swath", 184.0, 0.5), ("per_day", 14.58, 0.005), ("ground_day", 2687.0, 0.5),
                         ("days", 14.9, 0.05)):
        close_to(c[k], deck, tol, f"coverage {k} against the deck")
    return c


def aerobraking():
    """Burns only against aerobraking for the Venus orbiter (rocket equation for the propellant)."""
    rp0, ra0, rc, rp_ab = RV + HP0, RV + HA0, RV + HC, RV + HP_AB
    a0 = 0.5 * (rp0 + ra0)
    s = dict(rp0=rp0, ra0=ra0, rc=rc, rp_ab=rp_ab, a0=a0)
    s["e0"] = float(eccentricity(rp0, ra0))
    # burns only: one burn at periapsis brings the apoapsis down to 250 km
    s["vp0"] = float(vis_viva(V, rp0, a0))
    s["vc"] = float(circular_speed(V, rc))
    s["dv_prop"] = s["vp0"] - s["vc"]
    # aerobraking: (1) at apoapsis lower the periapsis to 140 km; (2) drag lowers the apoapsis
    # to 250 km; (3) at that apoapsis raise the periapsis to 250 km (the orbit is then circular)
    a1 = 0.5 * (rp_ab + ra0)
    s["va0"], s["va1"] = float(vis_viva(V, ra0, a0)), float(vis_viva(V, ra0, a1))
    s["dv_walk"] = s["va0"] - s["va1"]
    a_end = 0.5 * (rp_ab + rc)
    s["va_end"] = float(vis_viva(V, rc, a_end))
    s["dv_raise"] = s["vc"] - s["va_end"]
    s["dv_ab"] = s["dv_walk"] + s["dv_raise"]

    def prop(dv):                                              # kg, dv in km/s
        return M_SC * (1.0 - math.exp(-dv * 1000.0 / (ISP * G0)))
    s["mp_prop"], s["mp_ab"] = prop(s["dv_prop"]), prop(s["dv_ab"])
    s["saved"] = s["mp_prop"] - s["mp_ab"]
    s["T0_h"] = float(period(V, a0)) / 3600.0
    for k, deck, tol in (("dv_prop", 2.078, 0.0005), ("mp_prop", 581.0, 0.5), ("dv_ab", 0.045, 0.0005),
                         ("mp_ab", 17.0, 0.5)):
        close_to(s[k], deck, tol, f"aerobraking {k} against the deck")
    assert s["dv_walk"] > 0 and s["dv_raise"] > 0
    return s


def rho_h(h):
    """Air density, kg/m^3, at altitude h (km) from DENS, exponential between the points."""
    for (h1, d1), (h2, d2) in zip(DENS, DENS[1:]):
        if h1 <= h <= h2:
            return d1 * (d2 / d1) ** ((h - h1) / (h2 - h1))
    return DENS[-1][1]


def lifetime(h0, B=B_LIFE, h_end=H_END):
    """Days for a circular Earth orbit to decay from h0 to h_end (km), da/dt = -rho sqrt(mu a)/B,
    stepped forward in time (10 min steps, 1 min below 200 km), as the deck script does.
    Returns the days and the path [(day, altitude km), ...] sampled once a day."""
    mu = E * 1e9                       # m^3/s^2
    a = (RE + h0) * 1e3                # m
    t = 0.0
    path = [(0.0, h0)]
    while a / 1e3 - RE > h_end:
        h = a / 1e3 - RE
        step = 600.0 if h > 200.0 else 60.0
        a += -rho_h(h) * math.sqrt(mu * a) / B * step
        t += step
        if int(t / DAY) != int((t - step) / DAY):
            path.append((t / DAY, a / 1e3 - RE))
    path.append((t / DAY, a / 1e3 - RE))
    return t / DAY, path


def decay_per_rev(h, B=B_LIFE):
    """Drop of the orbit radius in one revolution at altitude h (km), in m: 2 pi rho a^2 / B."""
    return 2.0 * np.pi * rho_h(h) * ((RE + h) * 1e3) ** 2 / B


def lifetimes():
    L = {h0: lifetime(h0) for h0 in STARTS}
    for h0, deck in ((300.0, 47.0), (400.0, 408.0), (500.0, 2485.0)):
        close_to(L[h0][0], deck, 0.5, f"lifetime from {h0:g} km against the deck")
    close_to(decay_per_rev(400.0), 8.1, 0.05, "decay per revolution at 400 km against the deck")
    return L


# ===================================================================== helpers
def _map_frame(ax, lon=(-180, 180), lat=(-90, 90), lon_step=60, lat_step=30, labels=True):
    """Latitude and longitude grid on an existing axes, as map_axes() draws it."""
    ax.set_xlim(*lon)
    ax.set_ylim(*lat)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(math.ceil(lon[0] / lon_step) * lon_step, lon[1] + 0.1, lon_step))
    ax.set_yticks(np.arange(math.ceil(lat[0] / lat_step) * lat_step, lat[1] + 0.1, lat_step))

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
    if labels:
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")


def _track_inertial(inc, u):
    """Latitude and longitude (deg) under a circular orbit on a planet that does not turn,
    ascending node at longitude 0, argument of latitude u (deg)."""
    u = np.radians(np.asarray(u, dtype=float))
    i = math.radians(inc)
    lat = np.degrees(np.arcsin(np.sin(i) * np.sin(u)))
    lon = np.degrees(np.arctan2(math.cos(i) * np.sin(u), np.cos(u)))
    return lat, lon


def _index_at(lat, value, north=True):
    """Index of the first point where the track crosses latitude `value` heading north (or south)."""
    d = np.gradient(lat)
    ok = (d > 0) if north else (d < 0)
    return int(np.argmin(np.abs(lat - value) + 1000.0 * ~ok))


# ===================================================================== figures
def great_circle_to_map():
    """An inclined orbit over a globe that does not turn, and its ground track on a map."""
    inc, r_orb, u_sc = 50.0, 1.32, -30.0
    fig = plt.figure(figsize=(6.5, 2.75))
    ax_g = fig.add_axes([0.0, 0.0, 0.37, 1.0])
    ax_m = fig.add_axes([0.47, 0.2, 0.52, 0.74])
    ax_g.axis("off")
    ax_g.set_aspect("equal")
    g = Globe(ax_g, view_lat=22, view_lon=-35)                        # the chapter's globe: equator and axis
    g.axis(1.42)
    g.circle(r_orb, inc, 0.0, role="initial", arrows_at=(GC_ORBIT_U,))     # clear of the axis and the limb
    g.circle(1.0, inc, 0.0, role="other", hidden="none", arrows_at=(GC_TRACK_U,))
    P_sc = g.orbit_vec(r_orb, inc, 0.0, u_sc)
    P_sub = g.orbit_vec(1.0, inc, 0.0, u_sc)
    g.curve(np.c_[P_sc, P_sub], color=INK, lw=LW_THIN)
    g.point(P_sc, "spacecraft", direction=-35, ms=6)
    g.point(P_sub, ms=6, kind="open")
    g.text(g.orbit_vec(r_orb, inc, 0.0, -125.0), "orbit", direction=200, dist=7, color=text_color("initial"))
    ax_g.set_xlim(-1.55, 1.75)
    ax_g.set_ylim(-1.3, 1.6)

    _map_frame(ax_m, lon_step=90, lat_step=45)
    u = np.linspace(0.0, 360.0, 721)
    lat, lon = _track_inertial(inc, u)
    draw_track(ax_m, lon, lat, "other", arrows_at=(_index_at(lat, 20.0),))
    k = int(np.argmin(np.abs(u - 270.0)))
    text(ax_m, (lon[k], lat[k]), "ground track", direction=-90, dist=6)
    la, lo = _track_inertial(inc, [u_sc])
    sub = (float(lo[0]), float(la[0]))
    point(ax_m, sub, ms=6, kind="open")
    callout(ax_m, sub, "point below\nthe spacecraft", at=(-10.0, -62.0), fs=FS_SMALL, ha="left")
    dimension(ax_m, (90.0, 0.0), (90.0, inc), None)
    text(ax_m, (92.0, 0.5 * inc), "$i$", direction=0, dist=4)
    close_to(float(np.max(lat)), inc, 1e-6, "highest latitude of the track equals the inclination")
    close_to(float(lon[np.argmax(lat)]), 90.0, 0.6, "the track peaks 90 deg east of the ascending node")
    save_figure(fig, "p25-great-circle-to-map")


def ground_track_fig():
    """Three successive orbits at 700 km and 98.2 deg with Earth turning under them."""
    c = coverage()
    T, dL = c["T"], c["dL"]
    L0 = L0_TRACK
    fig, ax = map_axes()
    roles = [0, 1, 2]                                    # data series: three successive revolutions
    nodes = []
    for k in range(3):
        t = np.linspace(k * T, (k + 1) * T, 2001)
        lat, lon = ground_track(INC_GT, T, t, lon_node=L0)
        i_lab = _index_at(lat, 40.0)                       # northbound, 40 deg N
        draw_track(ax, lon, lat, roles[k], label="orbit 1" if k == 0 else f"{k + 1}", label_at=i_lab,
                   direction=0, dist=6, arrows_at=(_index_at(lat, 22.0),))
        nodes.append((float(lon[0]), float(lat[0])))
        close_to(float(np.max(lat)), c["max_lat"], 0.01, "highest latitude is 180 deg minus the inclination")
    lat_end, lon_end = ground_track(INC_GT, T, [3 * T], lon_node=L0)
    nodes.append((float(lon_end[0]), float(lat_end[0])))
    for n in nodes:
        point(ax, n, ms=5)                                 # 5 pt: room for the delta-L arrow between two dots
    # the westward shift between the first two ascending nodes
    close_to(nodes[0][0] - nodes[1][0], dL, 1e-6, "successive ascending nodes are dL apart")
    close_to(nodes[1][0] - nodes[2][0], dL, 1e-6, "the shift is the same every orbit")
    # the shift, on the equator itself: any dimension above or below it between the two dots would
    # meet a track. The gap is short (25 pt), so the heads (4.5 x 2 pt) and the dots (5 pt) are smaller.
    deg_pt = 360.0 / (ax.get_position().width * fig.get_size_inches()[0] * 72.0)      # degrees per point
    edge = 3.0 * deg_pt                                    # dot radius plus a hairline gap
    equator = [l for l in ax.lines if l.get_gid() == "equator"]
    rides_on(arrow(ax, (nodes[1][0] + edge, 0.0), (nodes[0][0] - edge, 0.0), head=(4.5, 2.0), lw=LW_THIN, both=True,
                   zorder=7), *equator)                     # drawn on the equator line on purpose
    text(ax, (nodes[0][0], 0.0), f"$\\Delta L$ = {fmt(dL)}°\n({fmt(c['spacing'])} km)", direction=-60, dist=8,
         fs=FS_SMALL, multialignment="left")
    save_figure(fig, "p25-ground-track")


def track_vs_period():
    """One revolution of three orbits of different period at the same inclination, and the
    geostationary point: the longer the period, the more the planet turns under one orbit."""
    inc = INC_PERIOD
    fig, ax = map_axes()
    cases = [(3.0 * 3600.0, -170.0, 0, "3 h", (-105.0, 40.0), 90),          # data series, not orbit roles
             (8.0 * 3600.0, -120.0, 1, "8 h", (-55.0, 40.0), 90),
             (T_SIDEREAL, 160.0, 2, f"geosynchronous\n{fmt(T_SIDEREAL / 3600.0)} h", (151.0, 26.0), 180)]
    for T, L0, role, lab, at, d in cases:
        t = np.linspace(0.0, T, 3001)
        lat, lon = ground_track(inc, T, t, lon_node=L0)
        draw_track(ax, lon, lat, role, arrows_at=(_index_at(lat, 20.0),))
        text(ax, at, lab, direction=d, dist=6, color=text_color(role), multialignment="right")
        close_to(float(np.max(lat)), inc, 0.01, f"highest latitude of the {lab} track equals the inclination")
        span = float(np.degrees(np.unwrap(np.radians(lon)))[-1] - lon[0])
        close_to(span, 360.0 * (1.0 - T / T_SIDEREAL), 1e-6, f"the {lab} track advances 360 (1 - T/T_day) deg")
        point(ax, (lon[0], lat[0]), ms=5)
    point(ax, (GEO_LON, 0.0), ms=8, kind="diamond")
    text(ax, (GEO_LON, 0.0), "geostationary", direction=-90, dist=8)
    save_figure(fig, "p25-track-vs-period")


def swath_fig():
    """Side view: altitude, field of view and swath width. Top view near the equator: the
    swaths of three successive orbits and the spacing between them, to scale."""
    c = coverage()
    w, T, dL = c["swath"], c["T"], c["dL"]
    fig = plt.figure(figsize=(6.5, 3.1))
    ax_s = fig.add_axes([0.0, 0.04, 0.36, 0.94])
    ax_t = fig.add_axes([0.47, 0.2, 0.52, 0.72])
    # ---- side view, to scale, km
    ax_s.axis("off")
    ax_s.set_aspect("equal")
    sc = np.array([0.0, H_GT])
    ax_s.plot([-260.0, 420.0], [0.0, 0.0], color=INK, lw=LW_THIN)
    for sgn in (-1, 1):
        ax_s.plot([0.0, sgn * 0.5 * w], [H_GT, 0.0], color=INK, lw=LW_THIN)
    point(ax_s, sc, "spacecraft", direction=90, ms=6)
    ang0 = math.degrees(math.atan2(-H_GT, -0.5 * w))
    ang1 = math.degrees(math.atan2(-H_GT, 0.5 * w))
    r_arc = 230.0
    angle_arc(ax_s, sc, r_arc, ang0, ang1, None)
    arc_end = sc + r_arc * np.array([math.cos(math.radians(ang1)), math.sin(math.radians(ang1))])
    callout(ax_s, arc_end, f"FOV = {fmt(FOV, 2)}°", at=(70.0, 610.0), gap=2.0, fs=FS_SMALL)
    dimension(ax_s, (-0.5 * w, 0.0), (0.5 * w, 0.0), None, offset=-60.0)
    text(ax_s, (0.0, -60.0), f"$w$ = {fmt(w)} km", direction=-90, dist=8, fs=FS_SMALL)     # 184.3, as the text
    dimension(ax_s, (-200.0, 0.0), (-200.0, H_GT), None)
    text(ax_s, (-200.0, 0.5 * H_GT), f"$h$ = {fmt(H_GT, 3)} km", direction=180, dist=5, fs=FS_SMALL)
    text(ax_s, (330.0, 0.0), "ground", direction=90, dist=4, fs=FS_SMALL)
    ax_s.set_xlim(-560.0, 470.0)
    ax_s.set_ylim(-200.0, 900.0)
    close_to(2.0 * H_GT * math.tan(math.radians(0.5 * (ang1 - ang0))), w, 1e-9, "the drawn cone spans the swath")
    # ---- top view: three northbound passes near the equator, swaths to scale
    _map_frame(ax_t, lon=(-60.0, 15.0), lat=(-20.0, 20.0), lon_step=15, lat_step=10)
    half = 0.5 * w / RE                                    # swath half-width, rad of arc
    roles = [0, 1, 2]                                    # data series: three successive passes
    nodes = []
    for k in range(3):
        t = np.linspace(k * T - 0.08 * T, k * T + 0.08 * T, 801)
        lat, lon = ground_track(INC_GT, T, t, lon_node=0.0)
        lonu = np.degrees(np.unwrap(np.radians(lon)))
        # unit vectors east and north of the track direction, then the swath edges
        f, l = np.radians(lat), np.radians(lonu)
        dx, dy = np.gradient(l) * np.cos(f), np.gradient(f)
        n = np.hypot(dx, dy)
        ex, ey = -dy / n, dx / n                           # to the left of the motion
        edges = []
        for sgn in (1, -1):
            fe = f + sgn * half * ey
            le = l + sgn * half * ex / np.cos(f)
            edges.append((np.degrees(le), np.degrees(fe)))
        poly = np.c_[np.r_[edges[0][0], edges[1][0][::-1]], np.r_[edges[0][1], edges[1][1][::-1]]]
        ax_t.add_patch(Polygon(poly, closed=True, fc="#E6E6E6", ec="none", zorder=2))
        for le, fe in edges:
            ax_t.plot(le, fe, color=GRAY, lw=0.7, zorder=2.2)
        ln_k = draw_track(ax_t, lonu, lat, roles[k], label="orbit 1" if k == 0 else f"{k + 1}",
                   label_at=_index_at(lat, 15.0), direction=0, dist=9)
        if k == 0:
            callout(ax_t, (edges[0][0][_index_at(lat, -14.0)], -14.0), "swath", at=(-5.0, -16.0), gap=1.0,
                    fs=FS_SMALL)
        j = len(lat) // 2
        nodes.append(float(lonu[j]))
        track_arrow(ax_t, lonu, lat, _index_at(lat, 13.0), roles[k], line=ln_k)
    for x in nodes:
        point(ax_t, (x, 0.0), ms=5)
    close_to(nodes[0] - nodes[1], dL, 1e-3, "neighboring passes are dL apart at the equator")
    # the spacing, on the equator between the facing edges of the dots (as in the ground-track figure)
    deg_pt = 75.0 / (ax_t.get_position().width * fig.get_size_inches()[0] * 72.0)      # degrees per point
    edge = 3.0 * deg_pt
    equator = [l for l in ax_t.lines if l.get_gid() == "equator"]
    rides_on(arrow(ax_t, (nodes[1] + edge, 0.0), (nodes[0] - edge, 0.0), head="small", lw=LW_THIN, both=True, zorder=7),
             *equator)                                       # drawn on the equator line on purpose
    text(ax_t, (0.5 * (nodes[0] + nodes[1]), 0.0), f"{fmt(c['spacing'])} km", direction=-90, dist=5, fs=FS_SMALL)
    # the swath is narrower than a motion arrowhead at this scale (184 km, 6 pt): each track's
    # arrowhead covers the two edge lines of its own swath
    save_figure(fig, "p25-swath", allow=("arrowhead at data (-2.71, 12.55) lies on a line",
                                         "arrowhead at data (-27.47, 12.55) lies on a line",
                                         "arrowhead at data (-52.23, 12.55) lies on a line"))


def aerobraking_fig():
    """Aerobraking at Venus. Left, to scale: the capture orbit, the orbits after successive
    drag passes (periapsis held at 140 km), the final circle and the two burns. Right: the
    altitude of the same orbits near periapsis, against the distance along the surface."""
    s = aerobraking()
    fig = plt.figure(figsize=(6.5, 3.2))
    ax = fig.add_axes([0.0, 0.0, 0.58, 1.0])
    az = fig.add_axes([0.70, 0.2, 0.29, 0.74])
    ax.axis("off")
    ax.set_aspect("equal")
    orbits = [(s["a0"], s["e0"], "initial")]
    for h in AERO_STEPS:
        ra = RV + h
        orbits.append((0.5 * (s["rp_ab"] + ra), float(eccentricity(s["rp_ab"], ra)), "transfer"))
    orbits.append((s["rc"], 0.0, "final"))
    draw_body(ax, (0.0, 0.0), RV, name="Venus")
    for a, e, role in orbits:
        draw_orbit(ax, a, e, role, arrows_at={"initial": (100.0,), "transfer": (150.0,), "final": (150.0,)}[role])
    text(ax, orbit_point(*orbits[0][:2], 125.0), "capture orbit", direction=125, dist=5,
         color=text_color("initial"))
    text(ax, (-25800.0, -2600.0), "after drag\npasses", color=text_color("transfer"), fs=FS_SMALL)
    L1, L2 = burn_lengths([s["dv_walk"], s["dv_raise"]], longest=40.0)   # burn arrows in proportion to the delta-Vs
    burn(ax, (-s["ra0"], 0.0), 90.0, r"$\Delta V_1$", length=L1, label_dir=180.0, dist=4)   # slows: periapsis down to 140 km
    burn(ax, (-s["rc"], 0.0), -90.0, None, length=L2)                                     # speeds up: periapsis up to 250 km
    text(ax, (-s["rc"], 0.0), r"$\Delta V_2$", direction=180.0, dist=4.5 + 6.0, offset=(0.0, -0.3 * L2))
    ax.set_xlim(-33500.0, 8500.0)
    ax.set_ylim(-15000.0, 15000.0)
    # right: altitude near periapsis, against the distance along the surface
    sd = np.linspace(-2500.0, 2500.0, 401)
    th = sd / RV                                               # rad from periapsis
    for a, e, role in orbits[1:]:
        p = a * (1.0 - e * e)
        h = p / (1.0 + e * np.cos(th)) - RV
        az.plot(sd, h, **line_kw(role))
    text(az, (0.0, HC), f"final orbit, {fmt(HC, 3)} km", direction=90, dist=4, fs=FS_SMALL,
         color=text_color("final"))
    text(az, (0.0, HP_AB), f"drag passes, {fmt(HP_AB, 3)} km", direction=-90, dist=9, fs=FS_SMALL,
         color=text_color("transfer"))
    for sp in ("top", "right"):
        az.spines[sp].set_visible(False)
    az.grid(True, color=GRID, lw=0.6)
    az.set_axisbelow(True)
    az.xaxis.set_major_formatter(CommaFormatter())
    az.set_xlim(-2500.0, 2500.0)
    az.set_ylim(0.0, 500.0)
    az.set_xticks([-2000, 0, 2000])
    az.set_yticks([0, 100, 200, 300, 400, 500])
    az.set_xlabel("Distance from\nperiapsis, km")
    az.set_ylabel("Altitude, km")
    # asserts: each drawn aerobraking orbit dips to 140 km, the final orbit stays at 250 km
    for a, e, role in orbits[1:-1]:
        x, y = orbit_xy(a, e)
        close_to(float(np.min(np.hypot(x, y))) - RV, HP_AB, 1e-6, "periapsis altitude of an aerobraking orbit")
    close_to(float(np.max(np.hypot(*orbit_xy(s["rc"], 0.0)))) - RV, HC, 1e-6, "final circle altitude")
    close_to(L1 / L2, s["dv_walk"] / s["dv_raise"], 1e-12, "burn arrows in proportion to the delta-Vs")
    # the 250 km final circle is 2 pt from Venus's limb at this scale: its motion arrowhead overlaps the limb
    save_figure(fig, "p25-aerobraking", allow=("arrowhead at data (-5349, 3337) lies on an outline",))


def orbit_lifetime_fig():
    """Altitude against time for circular Earth orbits starting at 300, 400 and 500 km, with
    B = 100 kg/m^2, on a log time axis, and the five-year line."""
    L = lifetimes()
    fig, ax = data_axes(6.5, 3.6)
    ax.set_xscale("log")
    roles = {300.0: 2, 400.0: 1, 500.0: 0}               # data series (not orbit roles)
    for h0 in STARTS:
        days, path = L[h0]
        d = np.array([p[0] for p in path])
        h = np.array([p[1] for p in path])
        d[0] = X_MIN                                         # t = 0 drawn at the left edge of the log axis
        ax.plot(d, h, **line_kw(roles[h0]))
        life = f"{fmt(days, 2)} days" if days < 1000 else f"{fmt(days / 365.25, 2)} years"
        text(ax, (2.0, h0), f"starts at {fmt(h0, 3)} km: {life}", direction=90, dist=4, fs=FS_SMALL,
             color=text_color(roles[h0]), ha="left")
        assert np.all(np.diff(h) <= 0.0), "altitude only falls"
        close_to(float(h[-1]), H_END, 0.5, "each curve ends at the end altitude")
    ax.axhline(H_END, **line_kw("boundary"), zorder=2)
    text(ax, (6000.0, H_END), f"{fmt(H_END, 3)} km", direction=90, dist=3, fs=FS_SMALL, color=STEEL)
    five = 5.0 * 365.25
    ax.axvline(five, color=GRAY, lw=LW_THIN, ls=(0, (4.0, 3.0)), zorder=2)
    text(ax, (five, 560.0), "5 years", direction=0, dist=4, fs=FS_SMALL, color=STEEL)
    ax.set_xlim(X_MIN, 1.0e4)
    ax.set_ylim(100.0, 600.0)
    ax.set_xticks([1, 10, 100, 1000, 10000])
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.xaxis.set_minor_formatter(mticker.NullFormatter())
    ax.set_xlabel("Time, days (log scale)")
    ax.set_ylabel("Altitude, km")
    assert L[300.0][0] < L[400.0][0] < five < L[500.0][0], "only the 500 km orbit outlasts five years"
    save_figure(fig, "p25-orbit-lifetime")


def make_all():
    great_circle_to_map()
    ground_track_fig()
    track_vs_period()
    swath_fig()
    aerobraking_fig()
    orbit_lifetime_fig()


def values():
    """Record every number the page prints (check_values.py finds each one on the page)."""
    R = lambda k, v: record(PAGE, k, v)                    # noqa: E731
    c, s, L = coverage(), aerobraking(), lifetimes()
    # constants and givens
    R("RE", fmt(RE)); R("muE", fmt_sci(E)); R("Tsid", fmt(T_SIDEREAL)); R("Tsid_h", fmt(T_SIDEREAL / 3600.0))
    R("solar_day", fmt(DAY)); R("rate", fmt(c["rate"]))
    R("h", fmt(H_GT, 3)); R("inc", fmt(INC_GT, 3)); R("fov", fmt(FOV, 2)); R("half_fov", fmt(FOV / 2.0, 2))
    R("max_lat", fmt(c["max_lat"], 3)); R("inc_map", fmt(50.0, 2)); R("inc_period", fmt(INC_PERIOD, 2))
    # coverage example
    R("a", fmt(c["a"])); R("T_s", fmt(c["T"])); R("T_min", fmt(c["T_min"]));
    R("dL", fmt(c["dL"]))
    R("spacing", fmt(c["spacing"])); R("swath", fmt(c["swath"]))
    R("per_day", fmt(c["per_day"])); R("ground_day", fmt(c["ground_day"])); R("equator", fmt(c["equator"]))
    R("days", fmt(c["days"]))
    R("T_back", fmt(c["T_back"])); R("a_back", fmt(c["a_back"])); R("h_back", fmt(c["a_back"] - RE, 3))
    R("ls_h", fmt(LANDSAT["h"], 3)); R("ls_swath", fmt(LANDSAT["swath"], 3)); R("ls_days", str(LANDSAT["days"]))
    R("ls_orbits", str(LANDSAT["orbits"])); R("ls_per_day", fmt(c["ls_per_day"])); R("ls_path", fmt(c["ls_path"]))
    # period and geostationary
    for hours in (3.0, 8.0):
        T = hours * 3600.0
        a = float(semi_major_axis_from_period(E, T))
        R(f"turn_{hours:g}h", fmt(360.0 * T / T_SIDEREAL, 3)); R(f"alt_{hours:g}h", fmt(a - RE))
    a_geo = float(semi_major_axis_from_period(E, T_SIDEREAL))
    R("a_geo", fmt(a_geo)); R("h_geo", fmt(a_geo - RE))
    # aerobraking
    R("muV", fmt_sci(V)); R("RV", fmt(RV)); R("m_sc", fmt(M_SC)); R("isp", fmt(ISP, 3)); R("g0", fmt(G0, 6))
    R("hp0", fmt(HP0, 3)); R("ha0", fmt(HA0, 5)); R("hp_ab", fmt(HP_AB, 3))
    R("rp0", fmt(s["rp0"])); R("ra0", fmt(s["ra0"])); R("a0", fmt(s["a0"])); R("rp_ab", fmt(s["rp_ab"]))
    R("T0_h", fmt(s["T0_h"], 3))
    # five decimals for the speeds: the small burns are differences of close speeds
    R("vp0", fmt_dec(s["vp0"], 5)); R("vc", fmt_dec(s["vc"], 5)); R("dv_prop", fmt(s["dv_prop"]))
    R("va0", fmt_dec(s["va0"], 5)); R("va1", fmt_dec(s["va1"], 5)); R("dv_walk", fmt(s["dv_walk"]))
    R("va_end", fmt_dec(s["va_end"], 5)); R("dv_raise", fmt(s["dv_raise"])); R("dv_ab", fmt(s["dv_ab"]))
    R("mp_prop", fmt(s["mp_prop"], 3)); R("mp_ab", fmt(s["mp_ab"], 3)); R("saved", fmt(s["saved"], 3))
    # orbit lifetime
    R("B", fmt(B_LIFE, 3)); R("h_end", fmt(H_END, 3))
    for h0 in STARTS:
        k = f"{h0:g}"
        R(f"rho_{k}", fmt_sci(rho_h(h0)))
        R(f"dr_{k}", fmt(decay_per_rev(h0)))                 # four figures, as the text prints 8.091
        days = L[h0][0]
        R(f"life_{k}", fmt(days, 2))
    R("life_500y", fmt(L[500.0][0] / 365.25, 2))
    R("dr_400_4", fmt(decay_per_rev(400.0)))
    R("dr_150_km", fmt(decay_per_rev(H_END) / 1000.0, 2))
    R("rho_150", fmt_sci(rho_h(H_END)))
    R("muE_SI", fmt_sci(E * 1e9)); R("a_400_m", fmt_sci((RE + 400.0) * 1e3))
    R("per_day_400", fmt(DAY / float(period(E, RE + 400.0)), 3))
    # ratios of the printed lifetimes (47, 408 and 2,485 days), so they follow from the table
    life = {h0: float(fmt(L[h0][0], 2 if h0 < 450 else 4).replace(",", "")) for h0 in STARTS}
    R("ratio_34", fmt(life[400.0] / life[300.0], 2)); R("ratio_45", fmt(life[500.0] / life[400.0], 2))
    R("rho_ratio_34", fmt(rho_h(300.0) / rho_h(400.0), 2)); R("rho_ratio_45", fmt(rho_h(400.0) / rho_h(500.0), 2))
    R("day_diff", fmt(DAY - T_SIDEREAL, 3))
    R("solar_err", fmt(100.0 * (1.0 - T_SIDEREAL / DAY), 2))
    R("T_wrong_min", fmt(float(period(E, H_GT)) / 60.0, 2))
    # numbers in the alt text of the figures
    R("node2", fmt(L0_TRACK - c["dL"], 3)); R("node3", fmt(abs(L0_TRACK - 2.0 * c["dL"]), 2))
    R("dL2", fmt(2.0 * c["dL"]))                          # four figures, as the text prints the shift
    for k, h in enumerate(AERO_STEPS):
        R(f"aero_step{k}", fmt(h, 3) if h < 10000 else fmt(h, 5))
    return c, s, L
