"""Figures and values of 2.3 Launch to Orbit (notes/chapter-2/launch-to-orbit.md).

One function per figure, make_all() for the runner, and values() for every number the page
prints. Run through the runner from the book folder:

    FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_2_figures.py p23

Helpers that orbits.py lacks are defined here (prefixed with an underscore).
"""
from chapter_2.orbits import *

# Earth's MEAN radius, 6,371 km, as launch calculations commonly use; the other pages of the
# chapter use the equatorial 6,378 km (the page explains the convention in two sentences).
E, RE = MU["Earth"], RADIUS_EARTH_MEAN
RE_EQ = RADIUS["Earth"]                     # equatorial radius: only for the geostationary altitude
WR = OMEGA_EARTH * RE                       # eastward speed of the ground at the equator, km/s
close_to(WR, float(surface_speed(0.0)), 1e-12, "surface_speed() uses the mean radius")

# LEO band (PLAN section 7, p23)
H_LEO_LOW, H_LEO_HIGH = 160.0, 2000.0       # km altitude

# Worked example: a coastal site at 30.4 deg N to a 550 km circular orbit at 40 deg, 1.6 km/s of losses
EX_LAT, EX_H, EX_INC, EX_LOSS = 30.4, 550.0, 40.0, 1.6

# Launch sites of the table: name, latitude (deg N), source cited on the page
SITES = [
    ("Guiana Space Centre, Kourou, French Guiana", 5.0 + 3.0 / 60.0, "5°3′", "ESA"),
    ("Satish Dhawan Space Centre, Sriharikota, India", 13.733, "13.7°", "ISRO"),
    ("Kennedy Space Center, Florida, United States", 28.5, "28.5°", "Craig and Ahmad (2020)"),
    ("Baikonur Cosmodrome, Kazakhstan", 45.6, "45.6°", "ESA"),
]

# Generic coastal site of the azimuth-fan figure (not a real site; no published limits used)
FAN_LAT, FAN_AZ0, FAN_AZ1 = 35.0, 50.0, 140.0

# Latitudes of the two data plots: the deck's 40 deg plus a low and a high one
PLOT_LATS = (10.0, 40.0, 65.0)
LG_AZ, LG_I = (0.6, 7.0), (0.6, 6.0, 0.40)   # launch geometry: Az and i labels (fraction of the arc, points), i arc radius
LG_SITE, LG_NORTH, LG_PHI = (160.0, 10.0), (180.0, 4.0), (180.0, 6.0)   # launch geometry: label directions, points
LG_SITE_DIST = 10.0                         # launch-geometry figure: "launch site" label, points from the site


def geo_radius():
    """Radius (km) of the geostationary orbit: period of one sidereal day."""
    return float(semi_major_axis_from_period(E, T_SIDEREAL))


def example():
    """Every number of the worked example, full precision."""
    r = RE + EX_H
    az_n, az_s = launch_azimuths(EX_LAT, EX_INC)
    s = math.cos(math.radians(EX_INC)) / math.cos(math.radians(EX_LAT))
    v = float(circular_speed(E, r))
    rot = float(rotation_gain(EX_LAT, az_n))
    rot_s = float(rotation_gain(EX_LAT, az_s))
    cases = {}
    for key, az in (("east", 90.0), ("north", 0.0), ("west", 270.0)):
        g = float(rotation_gain(EX_LAT, az))
        cases[key] = dict(az=az, inc=float(inclination_from_launch(EX_LAT, az)), rot=g, total=v + EX_LOSS - g)
    return dict(r=r, sinaz=s, az_n=az_n, az_s=az_s, v=v, rot=rot, rot_s=rot_s,
                rot_cosi=WR * math.cos(math.radians(EX_INC)), surface=float(surface_speed(EX_LAT)),
                total=v + EX_LOSS - rot, cases=cases)


# ===================================================================== small helpers
def _ring(ax, r0, r1, fill, zorder=1.5):
    """A filled annulus between radii r0 and r1 (km) about the origin, no edge."""
    t = np.linspace(0.0, 2.0 * np.pi, 721)
    xo, yo = r1 * np.cos(t), r1 * np.sin(t)
    xi, yi = r0 * np.cos(t[::-1]), r0 * np.sin(t[::-1])
    ax.add_patch(Polygon(np.c_[np.r_[xo, xi], np.r_[yo, yi]], closed=True, fc=fill, ec="none", zorder=zorder))


def _axis_arrow_frame(ax, x0, y0, x1, y1, xlabel, ylabel):
    """Two thin axis arrows (no ticks) for a schematic plot, labeled at their ends."""
    arrow(ax, (x0, y0), (x1, y0), lw=LW_THIN, head="small")
    arrow(ax, (x0, y0), (x0, y1), lw=LW_THIN, head="small")
    text(ax, (x1, y0), xlabel, direction=-90, dist=6, ha="right")
    text(ax, (x0, y1), ylabel, direction=0, dist=6, va="top")


# ===================================================================== figures
def leo_to_scale():
    """Earth, the low-Earth-orbit band and an arc of the geostationary orbit, all to scale."""
    rg = geo_radius()
    r_lo, r_hi = RE + H_LEO_LOW, RE + H_LEO_HIGH
    fig, ax = new_axes(6.5, 2.75)
    _ring(ax, r_lo, r_hi, "#F7F3E8")
    for r in (r_lo, r_hi):
        draw_orbit(ax, r, 0.0, "boundary", arrows_at=(), gid="edge")      # the edges of the filled band
    draw_body(ax, (0, 0), RE, name="Earth", label="")
    text(ax, (0.0, 2300.0), "Earth", backing=False)
    half = 11.0
    draw_orbit(ax, rg, 0.0, "other", theta0=-half, theta1=half, arrows_at=(-6.0,))
    p_lo = (r_lo * math.cos(math.radians(128)), r_lo * math.sin(math.radians(128)))
    p_hi = (r_hi * math.cos(math.radians(112)), r_hi * math.sin(math.radians(112)))
    callout(ax, p_lo, f"{fmt(H_LEO_LOW, 3)} km altitude", at=(-12500.0, 5200.0), fs=FS_SMALL)
    callout(ax, p_hi, f"{fmt(H_LEO_HIGH, 4)} km altitude", at=(-12500.0, 9300.0), fs=FS_SMALL)
    text(ax, (r_hi * math.cos(math.radians(-40)), r_hi * math.sin(math.radians(-40))),
         "low Earth orbit", direction=-40, dist=6, color=STEEL)
    # radius of the geostationary orbit, from Earth's center (drawn over the disc)
    point(ax, (0.0, 0.0), None, ms=4.5, zorder=9)
    arrow(ax, (0.0, 0.0), (rg, 0.0), lw=LW_THIN, head="small", zorder=8)
    text(ax, (0.62 * rg, 0.0), f"radius {fmt(rg)} km", direction=90, dist=4)
    # named by its radius only: the drawing is from the mean radius, the altitude in the text from
    # the equatorial radius, and the radius is the same under either convention
    text(ax, orbit_point(rg, 0.0, half), "geostationary\norbit", direction=180, dist=8, ha="right", va="top")
    ax.set_xlim(-17500, rg + 2500)
    ax.set_ylim(-10200, 10600)
    # assert: the band is drawn at the stated altitudes and the arc at the geostationary radius
    x, y = orbit_xy(r_hi, 0.0)
    close_to(float(np.max(np.hypot(x, y))) - RE, H_LEO_HIGH, 1e-6, "outer edge of the band")
    close_to(float(period(E, rg)), T_SIDEREAL, 1e-6, "geostationary period = sidereal day")
    save_figure(fig, "p23-leo-to-scale")


def velocity_vectors():
    """Top view from above the north pole: the site's velocity plus the delta-V equals the
    orbit velocity, for a due-east launch from the equator into a 550 km equatorial orbit."""
    v_site = WR
    r_orb = RE + EX_H
    v_orb = float(circular_speed(E, r_orb))
    dv = v_orb - v_site
    S = 4000.0                                  # km of drawing per km/s, one scale for all arrows
    fig, ax = new_axes(6.5, 3.2)
    draw_body(ax, (0, 0), RE, name="Earth", label="")
    text(ax, (0.0, 3500.0), "Earth", backing=False)
    point(ax, (0.0, 0.0), None, ms=4.0)
    text(ax, (0.0, 0.0), "N", direction=0, dist=5, backing=False)
    angle_arc(ax, (0.0, 0.0), 3000.0, 205.0, 335.0, None, arrow_end=True)
    text(ax, (3000.0 * math.cos(math.radians(270)), 3000.0 * math.sin(math.radians(270))),
         r"$\omega$", direction=90, dist=4, backing=False)
    site = np.array([0.0, -RE])
    point(ax, site, None, ms=5.0, kind="open", zorder=9)
    text(ax, site, "launch site", direction=90, dist=9, fs=FS_SMALL, backing=False)
    # the vector sum, to scale: site velocity and delta-V head to tail, beside the surface (4.5 pt
    # below the site, as every vector in the chapter sits beside the path it follows); the orbit
    # velocity below. Delta-V is black, as every burn in the chapter.
    tip1 = velocity_arrow(ax, site, (v_site, 0.0), S, lw=LW_THIN, head="small", offset=4.5, zorder=7)
    text(ax, site, r"$\mathbf{v}_{\mathrm{site}}$" + f" = {fmt(v_site)} km/s", direction=-90, dist=11,
         ha="left", offset=(3.0, 0.0))
    tip2 = velocity_arrow(ax, tip1, (dv, 0.0), S, offset=4.5, zorder=7)
    text(ax, 0.5 * (tip1 + tip2) + np.array([3500.0, 0.0]), r"$\Delta\mathbf{V}$" + f" = {fmt(dv)} km/s",
         direction=90, dist=4)
    y2 = -RE - 3300.0
    p0, p1 = np.array([0.0, y2]), np.array([S * v_orb, y2])
    arrow(ax, p0, p1, color=BLUE)
    text(ax, 0.5 * (p0 + p1) + np.array([3500.0, 0.0]), r"$\mathbf{v}_{\mathrm{orbit}}$" + f" = {fmt(v_orb)} km/s",
         direction=-90, dist=5, color=text_color("initial"))
    line(ax, (0.0, -RE - 2100.0), (0.0, y2 + 700.0))
    line(ax, (S * v_orb, -RE - 700.0), (S * v_orb, y2 + 700.0))
    speed_key(ax, (-RE, y2 - 1300.0), S)
    ax.set_xlim(-RE - 800, S * v_orb + 1500)
    ax.set_ylim(y2 - 2300, RE + 700)
    close_to(float(np.hypot(*(tip2 - site))), S * v_orb, 1e-6, "site velocity + delta-V = orbit velocity")
    close_to(float(p1[0] - p0[0]) / S, v_orb, 1e-9, "orbit arrow to scale")
    save_figure(fig, "p23-velocity-vectors")


def launch_geometry():
    """Globe: launch site at latitude phi, launch azimuth Az from north, the orbit plane through
    the site with inclination i at the ascending node, and the right spherical triangle."""
    lat, inc = EX_LAT, EX_INC
    az = launch_azimuths(lat, inc)[0]
    u_s = math.degrees(math.asin(math.sin(math.radians(lat)) / math.sin(math.radians(inc))))
    dlon = math.degrees(math.atan2(math.cos(math.radians(inc)) * math.sin(math.radians(u_s)),
                                   math.cos(math.radians(u_s))))
    fig, ax = new_axes(6.5, 5.0)
    g = Globe(ax, view_lat=33.0, view_lon=dlon * 0.5 - 12.0)          # the chapter's globe: equator and axis
    g.axis(1.32)
    node = g.orbit_vec(1.0, inc, 0.0, 0.0)
    site = g.vec(lat, dlon)
    foot = g.vec(0.0, dlon)
    # motion: one arrowhead on the near arc before the node, and one just past the launch site,
    # which is the launch direction (the direction of motion along the orbit at the site)
    U_LAUNCH = u_s + 32.0
    g.circle(1.0, inc, 0.0, role="initial", arrows_at=(-14.0, U_LAUNCH))
    # the spherical triangle: the meridian side (phi) drawn heavier
    g.curve(g.vec(np.linspace(0.0, lat, 121), dlon), hidden="none", color=INK, lw=1.6)
    for P in (node, site, foot):
        g.point(P, None, ms=5.5)
    # local directions at the site: north, and the launch direction along the orbit
    north = np.array([-math.sin(math.radians(lat)) * math.cos(math.radians(dlon)),
                      -math.sin(math.radians(lat)) * math.sin(math.radians(dlon)),
                      math.cos(math.radians(lat))])
    east = np.array([-math.sin(math.radians(dlon)), math.cos(math.radians(dlon)), 0.0])
    a = math.radians(az)
    launch = math.cos(a) * north + math.sin(a) * east
    GF = Globe.FILL                                   # labels on the globe: a backing of its fill color
    g.arrow(site, site + 0.36 * north, lw=LW_THIN, head="small")
    stop = math.radians(az - 6.0)                     # the arc ends short of the orbit line
    g.arc(site, north, math.cos(stop) * north + math.sin(stop) * east, 0.20, r"$\mathit{Az}$", dist=LG_AZ[1],
          arrow_end=True, backing=GF, label_at=LG_AZ[0])
    # inclination at the ascending node, between the equator (east) and the orbit
    e_node = g.orbit_vec(1.0, 0.0, 0.0, 90.0)
    along = g.orbit_vec(1.0, inc, 0.0, 90.0)
    g.curve(np.c_[node, node + 0.52 * e_node], hidden="none", color=STEEL, lw=LW_THIN)
    g.arc(node, e_node, along, LG_I[2], "$i$", dist=LG_I[1], backing=GF, label_at=LG_I[0])
    # latitude: label beside the meridian side, inside the triangle
    g.text(g.vec(0.5 * lat, dlon), r"$\phi$", direction=LG_PHI[0], dist=LG_PHI[1], backing=GF)
    # right angle at the foot of the meridian
    sq = 0.07
    c0 = foot + sq * np.array([0.0, 0.0, 1.0])
    w = -east
    g.curve(np.c_[c0, c0 + sq * w, foot + sq * w], hidden="none", color=INK, lw=LW_THIN)
    # labels
    g.text(site, "launch site", direction=LG_SITE[0], dist=LG_SITE[1], backing=GF)
    g.callout(node, "ascending node", at=(0.05, -1.13))
    g.callout(g.vec(0.0, dlon + 38.0), "equator", at=(1.22, -0.72), color=STEEL)
    g.text(site + 0.36 * north, "north", direction=LG_NORTH[0], dist=LG_NORTH[1], fs=FS_SMALL, backing=GF)
    g.callout(g.orbit_vec(1.0, inc, 0.0, U_LAUNCH - 2.0), "launch\ndirection", at=(1.2, 0.72), fs=FS_SMALL,
              color=text_color("initial"))
    g.callout(g.orbit_vec(1.0, inc, 0.0, -40.0), "orbit plane", at=(-1.45, -0.95),
              color=text_color("initial"))
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.25, 1.5)
    # asserts: the site lies on the orbit; the angle at the node is i; at the site it is Az
    close_to(float(np.dot(site, np.cross(node, along))), 0.0, 1e-12, "site lies in the orbit plane")
    close_to(float(np.degrees(np.arccos(np.dot(e_node, along)))), inc, 1e-9, "arc at the node spans i")
    tangent = np.cross(np.cross(node, along), site)          # direction of motion at the site
    tangent /= np.linalg.norm(tangent)
    close_to(float(np.degrees(np.arctan2(np.dot(tangent, east), np.dot(tangent, north)))), az, 1e-6,
             "orbit heading at the site equals Az")
    save_figure(fig, "p23-launch-geometry")


def inclination_vs_azimuth():
    """Inclination against launch azimuth, 0 to 360 deg, for three latitudes."""
    az = np.linspace(0.0, 360.0, 1441)
    fig, ax = data_axes(6.5, 4.6)
    ax.axhline(90.0, **line_kw("reference"))
    for k, lat in enumerate(PLOT_LATS):
        i = inclination_from_launch(lat, az)
        ax.plot(az, i, **line_kw(k))
        k_min = int(np.argmin(i))
        close_to(float(i[k_min]), lat, 1e-6, f"lowest inclination at latitude {lat}")
        close_to(float(az[k_min]), 90.0, 1e-9, "lowest inclination due east")
        close_to(float(np.max(i)), 180.0 - lat, 1e-6, "highest inclination due west")
        ax.plot([90.0], [lat], MARKERS[k], color=line_kw(k)["color"], ms=6.5, mfc="white", mew=1.5, zorder=6)
    # direct labels inside each curve's hump (below its peak, due west); the lowest latitude's
    # label sits above its peak, where it has room
    for k, lat in enumerate(PLOT_LATS):
        text(ax, (270.0, 180.0 - lat), f"$\\phi$ = {fmt(lat, 2)}°", direction=90 if k == 0 else -90, dist=6 if k == 0 else 13,
             color=text_color(k))
    text(ax, (8.0, 90.0), "polar", direction=90, dist=3, fs=FS_SMALL, color=STEEL, ha="left")
    text(ax, (180.0, 22.0), "prograde", fs=FS_SMALL, color=STEEL)
    text(ax, (180.0, 160.0), "retrograde", fs=FS_SMALL, color=STEEL)
    ax.set_xlim(0, 360)
    ax.set_ylim(0, 192)
    ax.set_yticks(np.arange(0, 181, 30))
    degree_ticks(ax, "x", 45)
    degree_ticks(ax, "y", 30)
    ax.set_xlabel("Launch azimuth, degrees clockwise from north")
    ax.set_ylabel("Orbit inclination, degrees")
    save_figure(fig, "p23-inclination-vs-azimuth")


def rotation_gain_plot():
    """Delta-V from Earth's rotation against launch azimuth for the same three latitudes."""
    az = np.linspace(0.0, 360.0, 1441)
    fig, ax = data_axes(6.5, 4.6)
    ax.axhline(0.0, **line_kw("reference"))
    for k, lat in enumerate(PLOT_LATS):
        g = rotation_gain(lat, az)
        ax.plot(az, g, **line_kw(k))
        close_to(float(np.max(g)), WR * math.cos(math.radians(lat)), 1e-6, f"peak gain at latitude {lat}")
        close_to(float(az[int(np.argmax(g))]), 90.0, 1e-9, "peak due east")
        close_to(float(np.min(g)), -WR * math.cos(math.radians(lat)), 1e-6, "largest loss due west")
        ax.plot([90.0], [float(np.max(g))], MARKERS[k], color=line_kw(k)["color"], ms=6.5, mfc="white",
                mew=1.5, zorder=6)
    for k, lat in enumerate(PLOT_LATS):              # direct labels at each trough (due west)
        text(ax, (270.0, -float(surface_speed(lat))), f"$\\phi$ = {fmt(lat, 2)}°", direction=-90 if k == 0 else 90,
             dist=6 if k == 0 else 13, color=text_color(k))       # below the deepest trough, inside the other two
    ax.set_xlim(0, 360)
    ax.set_ylim(-0.6, 0.6)
    ax.set_yticks(np.arange(-0.4, 0.41, 0.2))
    degree_ticks(ax, "x", 45)
    ax.set_xlabel("Launch azimuth, degrees clockwise from north")
    ax.set_ylabel(r"$\Delta V_{\mathrm{rot}}$, km/s")
    save_figure(fig, "p23-rotation-gain")


def azimuth_fan():
    """Compass rose at a coastal site at 35 deg N: the allowed azimuth sector and the
    inclinations its edges and due east give."""
    lat = FAN_LAT
    fig, ax = new_axes(6.5, 4.6)
    R = 1.0
    th = np.linspace(0, 2 * np.pi, 361)
    ax.plot(R * np.cos(th), R * np.sin(th), color=INK, lw=LW_THIN, zorder=2, gid="edge")   # the rose's outline
    # the allowed sector, hatched; screen angle = 90 - Az
    azs = np.linspace(FAN_AZ0, FAN_AZ1, 181)
    sx = np.r_[0.0, R * np.cos(np.radians(90.0 - azs)), 0.0]
    sy = np.r_[0.0, R * np.sin(np.radians(90.0 - azs)), 0.0]
    ax.add_patch(Polygon(np.c_[sx, sy], closed=True, fc="#EAF1F8", ec=BLUE, lw=1.2, hatch="//", zorder=1.5))
    # ticks every 30 deg, compass letters
    for a in range(0, 360, 30):
        t = math.radians(90.0 - a)
        ax.plot([0.94 * math.cos(t), R * math.cos(t)], [0.94 * math.sin(t), R * math.sin(t)], color=INK,
                lw=LW_THIN, zorder=2)
    for a, lab, d in ((0, "N", 90.0), (90, "E", 62.0), (180, "S", -90.0), (270, "W", 180.0)):
        t = math.radians(90.0 - a)
        text(ax, (R * math.cos(t), R * math.sin(t)), lab, direction=d, dist=6, backing=False)
    point(ax, (0.0, 0.0), None, ms=6.0)
    text(ax, (0.0, 0.0), "launch site,\nlatitude 35° N", direction=200, dist=8, fs=FS_SMALL)
    # rays: the two edges and due east, with the inclination each gives
    for a, side in ((FAN_AZ0, 1), (90.0, 0), (FAN_AZ1, -1)):
        t = math.radians(90.0 - a)
        end = (1.32 * math.cos(t), 1.32 * math.sin(t))
        arrow(ax, (0.0, 0.0), end, lw=LW_ARROW, head="small")
        i = float(inclination_from_launch(lat, a))
        text(ax, end, f"$\\mathit{{Az}}$ = {fmt(a, 2)}°, $i$ = {fmt(i, 3)}°", direction=90.0 - a, dist=5)
    text(ax, (-0.32, -0.52), "no launches\nover land", fs=FS_SMALL, color=STEEL, backing=False)
    callout(ax, (0.62, -0.30), "allowed\nazimuths", at=(1.2, -0.62), fs=FS_SMALL, va="top")
    ax.set_xlim(-1.45, 3.0)
    ax.set_ylim(-1.45, 1.45)
    i_lo = float(inclination_from_launch(lat, 90.0))
    close_to(i_lo, lat, 1e-9, "due east gives i = latitude")
    i_edges = [float(inclination_from_launch(lat, a)) for a in (FAN_AZ0, FAN_AZ1)]
    assert all(i > lat for i in i_edges), "sector edges give higher inclinations than due east"
    save_figure(fig, "p23-azimuth-fan")


def ascent_profile():
    """Schematic ascent: vertical rise, pitch-over, gravity turn, staging, orbit insertion.
    The path comes from a flight-path angle that falls smoothly from 90 deg to 0 deg."""
    s = np.linspace(0.0, 1.0, 2001)
    s0, s1 = 0.06, 1.0                       # end of the vertical rise; insertion
    u = np.clip((s - s0) / (s1 - s0), 0.0, 1.0)
    gam = np.radians(90.0 * (1.0 - u) ** 2.2)
    ds = np.gradient(s)
    x = np.cumsum(np.cos(gam) * ds)
    y = np.cumsum(np.sin(gam) * ds)
    x, y = x - x[0], y - y[0]
    X, Y = 6.0 * x / x[-1], 3.0 * y / y[-1]
    fig, ax = new_axes(6.5, 3.6)
    _axis_arrow_frame(ax, -0.25, -0.15, 6.9, 3.75, "Downrange distance", "Altitude")
    path = ax.plot(X, Y, **line_kw(0))[0]            # a path, not an orbit: the data-series look
    rides_on(arrow(ax, (X[-30], Y[-30]), (X[-1] + 0.35, Y[-1]), color=line_kw(0)["color"], lw=LW_ORBIT, head="normal"),
           path)
    events = [(0.0, "liftoff", 0), (s0, "pitch-over", 1), (0.30, "first-stage\nseparation", 2),
              (0.55, "fairing jettison", 3), (1.0, "orbit insertion", 4)]
    for sv, lab, k in events:
        j = int(np.argmin(np.abs(s - sv)))
        point(ax, (X[j], Y[j]), None, ms=6.0)
        place = {0: dict(direction=15, dist=8), 1: dict(direction=8, dist=8), 2: dict(direction=-30, dist=8),
                 3: dict(direction=-60, dist=8), 4: dict(direction=-90, dist=9)}[k]
        text(ax, (X[j], Y[j]), lab, fs=FS_SMALL, **place)
    jg = int(np.argmin(np.abs(s - 0.14)))
    callout(ax, (X[jg], Y[jg]), "gravity turn", at=(1.05, 0.95), fs=FS_SMALL, ha="left")
    ax.axhline(0.65, xmin=0.0, xmax=1.0, **line_kw("boundary"))
    text(ax, (6.9, 0.65), "dense lower\natmosphere", direction=-90, dist=5, fs=FS_SMALL, color=STEEL, ha="right")
    ax.set_xlim(-0.5, 7.3)
    ax.set_ylim(-0.4, 3.95)
    close_to(float(np.degrees(gam[0])), 90.0, 1e-9, "vertical at liftoff")
    close_to(float(np.degrees(gam[-1])), 0.0, 1e-9, "horizontal at insertion")
    assert np.all(np.diff(gam) <= 1e-12), "flight-path angle never rises"
    save_figure(fig, "p23-ascent-profile")


def budget():
    """Delta-V budget of the worked example as floating bars."""
    ex = example()
    v, loss, rot, tot = ex["v"], EX_LOSS, ex["rot"], ex["total"]
    fig, ax = data_axes(6.5, 3.9)
    ax.grid(False, axis="x")
    labels = ["orbit speed\n$v_{\\mathrm{orbit}}$", "losses\n$\\Delta V_{\\mathrm{losses}}$",
              "rotation\n$-\\Delta V_{\\mathrm{rot}}$", "total\n$\\Delta V_{\\mathrm{total}}$"]
    vals = [v, loss, -rot, tot]
    bottoms = [0.0, v, v + loss, 0.0]
    texts = [fmt(v), "+" + fmt(loss, 2), "−" + fmt(rot), fmt(tot)]
    cont = bars(ax, labels, vals, styles=[0, 1, 2, 4], bottoms=bottoms, value_text=texts)
    ax.tick_params(axis="x", labelsize=FS_LABEL)     # 12 pt, so the word subscripts read at 10.6 pt
    for x0, x1, yv in ((0, 1, v), (1, 2, v + loss), (2, 3, tot)):
        ax.plot([x0 + 0.31, x1 - 0.31], [yv, yv], color=GRAY, lw=LW_THIN, ls=(0, (2, 2)), zorder=2)
    ax.set_ylabel("Speed or velocity change, km/s")
    ax.set_ylim(0, 10.5)
    tops = [b.get_y() + b.get_height() for b in cont.patches]
    close_to(tops[3], v + loss - rot, 1e-9, "total bar equals v + losses - rotation")
    close_to(cont.patches[2].get_y(), v + loss, 1e-9, "rotation bar hangs from the top of the losses")
    save_figure(fig, "p23-budget")


def make_all():
    leo_to_scale()
    velocity_vectors()
    launch_geometry()
    inclination_vs_azimuth()
    rotation_gain_plot()
    azimuth_fan()
    ascent_profile()
    budget()


# ===================================================================== printed values
def values():
    P = "p23"
    rg = geo_radius()
    record(P, "geo-r", fmt(rg))
    record(P, "geo-h", fmt(rg - RE_EQ))                   # above the equator
    record(P, "omega", fmt(OMEGA_EARTH * 1e5))            # printed as 7.292 x 10^-5 rad/s
    record(P, "R-mean", fmt(RE))
    record(P, "R-eq", fmt(RE_EQ))
    record(P, "R-diff-pct", fmt(100.0 * (RE_EQ - RE) / RE_EQ, 1))
    close_to(OMEGA_EARTH, 2.0 * math.pi / T_SIDEREAL, 1e-8, "omega = 2 pi / sidereal day")
    record(P, "tsid", fmt(T_SIDEREAL, 5))
    for h, key in ((H_LEO_LOW, "lo"), (H_LEO_HIGH, "hi")):
        r = RE + h
        record(P, f"leo-v-{key}", fmt(float(circular_speed(E, r))))
        record(P, f"leo-T-{key}", fmt(float(period(E, r)) / 60.0, 3))
    record(P, "band-frac", fmt(100.0 * (H_LEO_HIGH - H_LEO_LOW) / RE, 2))
    record(P, "wR", fmt(WR))
    # simplest case: equator, due east, 550 km equatorial orbit
    v550 = float(circular_speed(E, RE + EX_H))
    record(P, "eq-dv", fmt(v550 - WR))
    record(P, "eq-frac", fmt(100.0 * WR / v550, 2))
    ke = 0.5 * v550 ** 2                                   # km^2/s^2 per unit mass
    pe = E / RE - E / (RE + EX_H)
    record(P, "ke", fmt(ke, 3))
    record(P, "pe", fmt(pe, 3))
    record(P, "ke-pe", fmt(ke / pe, 2))
    # the simple subtraction against the exact vector difference, worst case (due north at the equator)
    record(P, "cross-max", fmt(1000.0 * WR ** 2 / (2.0 * v550), 2))
    exact = math.sqrt(v550 ** 2 + WR ** 2)                 # |v_orbit - v_site| for perpendicular vectors
    close_to(exact - v550, WR ** 2 / (2.0 * v550), 2e-4, "cross-track correction")
    # sites table
    record(P, "kourou-lat", fmt(SITES[0][1], 3))
    # fan figure
    record(P, "fan-i0", fmt(float(inclination_from_launch(FAN_LAT, FAN_AZ0)), 3))
    record(P, "fan-i1", fmt(float(inclination_from_launch(FAN_LAT, FAN_AZ1)), 3))
    # plots
    for lat in PLOT_LATS:
        record(P, f"peak4-{lat:g}", fmt(float(surface_speed(lat))))           # the figure's markers and alt text
    # worked example
    ex = example()
    record(P, "ex-r", fmt(ex["r"]))
    record(P, "ex-sinaz", fmt(ex["sinaz"]))
    record(P, "ex-azn", fmt(ex["az_n"], 3))
    record(P, "ex-azs", fmt(ex["az_s"], 4))
    record(P, "ex-surface", fmt(ex["surface"]))
    record(P, "ex-rot", fmt(ex["rot"]))
    close_to(ex["rot"], ex["rot_cosi"], 1e-12, "rotation gain = omega R cos i")
    close_to(ex["rot_s"], ex["rot"], 1e-12, "both azimuths give the same gain")
    record(P, "ex-v", fmt(ex["v"]))
    record(P, "ex-total", fmt(ex["total"]))
    record(P, "ex-cos40", fmt(math.cos(math.radians(EX_INC)), 4))
    record(P, "ex-rot-share", fmt(100.0 * ex["rot"] / ex["total"], 1))
    record(P, "alt-as-r", fmt(float(circular_speed(E, EX_H)), 2))
    for key, c in ex["cases"].items():
        record(P, f"ex-{key}-inc", fmt(c["inc"], 3) if c["inc"] < 100 else fmt(c["inc"], 4))
        record(P, f"ex-{key}-rot", fmt(c["rot"], minus="−") if abs(c["rot"]) > 1e-9 else "0")
        record(P, f"ex-{key}-total", fmt(c["total"]))
    # the difference of the two printed totals (9.590 - 8.788), so it follows from the table
    record(P, "ex-west-extra", fmt(float(fmt(ex["cases"]["west"]["total"])) - float(fmt(ex["cases"]["east"]["total"])), 3))
    # quiz values (checked here, printed only in the quiz)
    s = math.cos(math.radians(50.0)) / math.cos(math.radians(20.0))
    q5 = math.degrees(math.asin(s))
    assert abs(q5 - 43.16) < 0.01, q5
    q6 = WR * math.cos(math.radians(60.0))
    assert abs(q6 - 0.2323) < 1e-4, q6
    # quiz q3 (25 deg N, azimuth 300 deg) with the mean radius: the key and the two numeric distractors
    q3 = float(rotation_gain(25.0, 300.0))
    assert fmt(WR) == "0.4646" and fmt(q3, 3) == "-0.365", q3
    assert fmt(WR * math.cos(math.radians(25.0)) * math.cos(math.radians(300.0)), 3) == "0.211"
    assert fmt(WR * math.sin(math.radians(300.0)), 3) == "-0.402"
