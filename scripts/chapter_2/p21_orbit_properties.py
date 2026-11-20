"""Figures and values of 2.1 Orbit Properties (notes/chapter-2/orbit-properties.md).

One function per figure, make_all() to draw them, values() to record every number the page
prints. Run through the runner from the book folder:

    FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_2_figures.py p21

Helpers written here (not in orbits.py): _poly_area() for the swept areas, _orbit3d() for
an ellipse in three dimensions on the orbital-elements globe.
"""
from chapter_2.orbits import *  # noqa: F401,F403

TAG = "p21"
E, RE = MU["Earth"], RADIUS["Earth"]

# Worked example 1: an Earth satellite, perigee altitude 700 km, apogee altitude 5,800 km.
EX1_HP, EX1_HA = 700.0, 5800.0
# Worked example 2: a spacecraft around Venus, period 8.0 h, periapsis altitude 400 km.
EX2_T_H, EX2_HP = 8.0, 400.0
# Worked example 3: a small body crossing 1 AU from the Sun at 40.0 km/s (and at 45.0 km/s).
EX3_V, EX3_V2 = 40.0, 45.0
# Low Earth orbit used for the "about 90 minutes" statement.
LEO_H = 400.0
# Figure parameters (quoted in captions and alt text, so recorded in values()).
EG_CENTER = (-40.0, 9.0)                    # ellipse-geometry figure: "center" label, direction and points
ELL_E = 0.5                                  # ellipse-geometry figure
CONIC_E = (0.0, 0.5, 1.0, 2.0)               # conic-sections figure
KEPLER_E, KEPLER_N = 0.6, 12                 # equal-areas figure: e, and dt = T / KEPLER_N
OE = dict(inc=40.0, raan=60.0, argp=70.0, th=80.0)   # orbital-elements figure, deg
PLANE_FILL = "#F7F3E8"                       # the reference plane (Globe.plane's default fill)
OE_W_AT = 0.35                                # omega label at 35% of its arc (clear of both arrowheads)
OE_R = (3.8, 2.0, 2.5)                       # radii of the Omega, omega and theta arcs (plane units)
OE_NODE_AT, OE_W_DIST = (1.9, 0.0), 5.0         # "ascending node" label offset from the node (data), omega label distance (pt)
TRAJ_R0 = 13000.0                            # trajectories-by-speed figure: start radius, km
TRAJ_FC = (0.85, 1.15)                       # speeds below and above v_c, as fractions of v_c
TRAJ_FE = 1.2                                # hyperbola speed, as a fraction of v_esc
TRAJ_Y, TRAJ_TOP = 19800.0, 21500.0           # height of the open-path labels; top of the drawing, km
TRAJ_FIGSIZE = (8.5, 7.432)                # large enough that the 0.85 label fits between its ellipse and the circle
TRAJ_LAB_AT, TRAJ_LAB_FS = (-9900.0, 0.0), FS_LABEL

# Planets of the speed figure, in order from the Sun. Mars is drawn as a named marker on the
# curve like the others; no speed is printed for it, so values() records none.
PLANETS = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


def planet_distance(n):
    """Mean distance from the Sun, km (Mars from its figure-only constant)."""
    return SUN_DISTANCE_MARS_FIGURE_ONLY if n == "Mars" else SUN_DISTANCE[n]


def ex1():
    rp, ra = RE + EX1_HP, RE + EX1_HA
    a = 0.5 * (rp + ra)
    e = float(eccentricity(rp, ra))
    T = float(period(E, a))
    vp, va = float(vis_viva(E, rp, a)), float(vis_viva(E, ra, a))
    return dict(rp=rp, ra=ra, a=a, e=e, T=T, vp=vp, va=va, eps=float(specific_energy(E, a)))


def ex2():
    mu, R = MU["Venus"], RADIUS["Venus"]
    T = EX2_T_H * 3600.0
    a = float(semi_major_axis_from_period(mu, T))
    rp = R + EX2_HP
    ra = 2.0 * a - rp
    return dict(mu=mu, R=R, T=T, a=a, rp=rp, ra=ra, ha=ra - R, e=float(eccentricity(rp, ra)))


def ex3(v):
    mu, r = MU["Sun"], AU
    eps = float(energy_from_state(mu, r, v))
    return dict(mu=mu, r=r, v=v, ke=0.5 * v * v, pe=mu / r, eps=eps,
                a=float(semi_major_axis_from_state(mu, r, v)), vesc=float(escape_speed(mu, r)),
                vc=float(circular_speed(mu, r)))


def _poly_area(x, y):
    """Area of a closed polygon (shoelace formula)."""
    return 0.5 * abs(float(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))))


# ===================================================================== figures
def two_body():
    """Two point masses pulling on each other along the line between their centers."""
    fig, ax = new_axes(6.5, 2.3)
    R1, R2, d = 1.0, 0.42, 6.0
    c1, c2 = np.array([0.0, 0.0]), np.array([d, 0.0])
    draw_body(ax, c1, R1, label="$m_1$", where="above", fill=BODY_DEFAULT)
    draw_body(ax, c2, R2, label="$m_2$", where="above", fill=BODY_DEFAULT)
    L = 1.6                                          # equal and opposite: Newton's third law
    f1 = (c1 + np.array([R1, 0.0]), c1 + np.array([R1 + L, 0.0]))
    f2 = (c2 - np.array([R2, 0.0]), c2 - np.array([R2 + L, 0.0]))
    arrow(ax, *f1, head="large")
    arrow(ax, *f2, head="large")
    text(ax, 0.5 * (f1[0] + f1[1]), "$F$", direction=90, dist=7)
    text(ax, 0.5 * (f2[0] + f2[1]), "$F$", direction=90, dist=7)
    dimension(ax, c1, c2, "$r$", offset=-1.55, label_side=-1)
    ax.plot(*c1, "o", color=INK, ms=3.5, zorder=8)
    ax.plot(*c2, "o", color=INK, ms=3.5, zorder=8)
    ax.set_xlim(-1.3, d + 0.8)
    ax.set_ylim(-2.0, 1.6)
    close_to(np.hypot(*(f1[1] - f1[0])), np.hypot(*(f2[1] - f2[0])), 1e-12, "forces equal in size")
    close_to(float(np.dot(f1[1] - f1[0], f2[1] - f2[0])), -L * L, 1e-12, "forces opposite, along the line")
    save_figure(fig, "p21-two-body")


def ellipse_geometry():
    """Ellipse with the central body at a focus: a, b, c, r_p, r_a, and r, theta to a point."""
    a, e = 1.0, ELL_E
    c, b, p = a * e, a * math.sqrt(1 - e * e), a * (1 - e * e)
    rp, ra = apsides(a, e)
    fig, ax = new_axes(6.5, 4.6)
    line(ax, (-ra, 0), (rp, 0))                                  # major axis
    draw_orbit(ax, a, e, 1, arrows_at=(215,))            # the e = 0.5 ellipse in its look of p21-conic-sections
    text(ax, (-c, -0.6 * b), "$b$", direction=180, dist=5)
    # points on the axis
    draw_body(ax, (0, 0), 0.065, label="", fill=BODY_DEFAULT)
    point(ax, (-c, 0), None, ms=5)
    point(ax, (-2 * c, 0), None, kind="open", ms=6)
    point(ax, (rp, 0), "periapsis", direction=0, ms=5)
    point(ax, (-ra, 0), "apoapsis", direction=180, ms=5)
    text(ax, (0.0, 0.0), "focus", direction=-55, dist=12)
    text(ax, (-2 * c, 0.0), "empty focus", direction=-90, dist=7)
    text(ax, (-c, 0.0), "center", direction=EG_CENTER[0], dist=EG_CENTER[1])
    # a (center to apoapsis) and c (center to focus), just above the axis
    dimension(ax, (-ra, 0), (-c, 0), "$a$", offset=0.13, label_side=1)
    dimension(ax, (-c, 0), (0, 0), "$c$", offset=0.13, label_side=1)
    # r_a and r_p below the ellipse
    yd = -(b + 0.2)
    dimension(ax, (-ra, 0), (0, 0), "$r_a$", offset=yd, label_side=-1)
    dimension(ax, (0, 0), (rp, 0), "$r_p$", offset=yd, label_side=-1)
    # a point on the orbit: r and theta
    th = 62.0
    P = orbit_point(a, e, th)
    line(ax, (0, 0), P, role="reference", color=INK)
    point(ax, P, "spacecraft", direction=th, ms=6)
    text(ax, 0.55 * P, "$r$", direction=th + 90, dist=4)
    angle_arc(ax, (0, 0), 0.22, 0, th, r"$\theta$", arrow_end=True, dist=5)
    ax.set_xlim(-ra - 0.45, rp + 0.55)
    ax.set_ylim(yd - 0.42, b + 0.3)
    # b: a dimension from just below the center dot (2 pt clear of it) down to the bottom of the
    # ellipse, with heads like a and c
    fig.canvas.draw()
    unit_pt = float(np.diff(ax.transData.transform([(0.0, 0.0), (0.0, 1.0)])[:, 1])[0]) * 72.0 / fig.dpi
    dimension(ax, (-c, -(2.5 + 2.0) / unit_pt), (-c, -b), None, ticks=False)
    x, y = orbit_xy(a, e)
    close_to(float(np.max(x) - np.min(x)), 2 * a, 1e-9, "major axis drawn is 2a")
    close_to(float(np.max(y)), b, 1e-5, "semi-minor axis drawn is b")
    close_to(0.5 * (float(np.max(x)) + float(np.min(x))), -c, 1e-9, "center a distance c from the focus")
    close_to(float(np.hypot(*P)), float(conic_radius(p, e, th)), 1e-12, "the point lies on the orbit")
    save_figure(fig, "p21-ellipse-geometry")


def conic_sections():
    """Circle, ellipse, parabola and hyperbola with one focus and one periapsis."""
    rp = 1.0
    fig, ax = new_axes(5.6, 5.0)
    e0, e1, e2, e3 = CONIC_E
    curves = ((0, e0, ""), (1, e1, ""), (2, e2, ""), ("hyperbola", e3, ""))      # data-series looks, not orbit roles
    arrows = {e0: 135.0, e1: 200.0, e2: 80.0, e3: 62.0}
    for role, e, lab in curves:
        x, y = conic_xy(rp, e, r_max=None if e < 1 else 30.0, n=2001)
        ln = ax.plot(x, y, zorder=3, **line_kw(role))[0]
        orbit_arrows(ax, rp, e, (arrows[e],), role=role, line=ln)
    draw_body(ax, (0, 0), None, label="", ms=9)
    text(ax, (0, 0), "focus", direction=-90, dist=9)
    point(ax, (rp, 0), "periapsis", direction=0, ms=5)
    X0, X1, Y0, Y1 = -3.45, 1.95, -2.75, 2.75
    text(ax, orbit_point(1.0, 0.0, 225.0), f"circle, $e$ = {e0:g}", direction=225, dist=5,
         color=text_color(0))
    text(ax, (-rp * (1 + e1) / (1 - e1), 0.0), f"ellipse,\n$e$ = {e1:g}", direction=0, dist=10,
         color=text_color(1), ha="left", va="center")
    for e, yl, role, lab in ((e2, 2.2, 2, f"parabola,\n$e$ = {e2:g}"),
                             (e3, 2.2, "hyperbola", f"hyperbola,\n$e$ = {e3:g}")):
        x, y = conic_xy(rp, e, theta0=0.0, theta1=179.0, r_max=30.0, n=4001)
        k = int(np.argmin(np.abs(y - yl)))
        side = 180.0 if e == e2 else 0.0
        text(ax, (x[k], y[k]), lab, direction=side, dist=22 if e == e2 else 16, color=text_color(role), va="center")
    ax.set_xlim(X0, X1)
    ax.set_ylim(Y0, Y1)
    for e in CONIC_E:                                     # one periapsis, one focus
        x, y = conic_xy(rp, e, theta0=-1.0, theta1=1.0, r_max=30.0, n=201)
        close_to(float(np.max(np.hypot(x, y))), rp * (1 + e) / (1 + e * math.cos(math.radians(1.0))), 1e-9,
                 "conic passes through the common periapsis")
        close_to(float(np.max(x)), rp, 1e-9, f"periapsis of e = {e} on +x at r_p")
    x, y = conic_xy(rp, e1)
    close_to(float(np.min(x)), -rp * (1 + e1) / (1 - e1), 1e-9, "ellipse apoapsis at r_a = r_p (1 + e)/(1 - e)")
    save_figure(fig, "p21-conic-sections")


def equal_areas():
    """Two sectors swept in equal times, near periapsis and near apoapsis (Kepler's equation)."""
    a, e, mu = 1.0, KEPLER_E, 1.0
    T = 2 * math.pi * math.sqrt(a ** 3 / mu)
    dt = T / KEPLER_N
    fig, ax = new_axes(6.0, 3.9)
    areas = []
    for k, (t0, t1) in enumerate(((-dt / 2, dt / 2), (T / 2 - dt / 2, T / 2 + dt / 2))):
        th = true_anomaly_at_time(mu, a, e, np.linspace(t0, t1, 200))
        r = conic_radius(a * (1 - e * e), e, th)
        x, y = r * np.cos(np.radians(th)), r * np.sin(np.radians(th))
        px, py = np.r_[0.0, x], np.r_[0.0, y]
        ax.add_patch(Polygon(np.c_[px, py], closed=True, fc=DUST if k == 0 else DUST, ec=INK, lw=LW_THIN,
                             zorder=2))
        areas.append(_poly_area(px, py))
    draw_orbit(ax, a, e, "initial", arrows_at=(130.0,))
    draw_body(ax, (0, 0), None, label="", ms=9, zorder=6)
    rp, ra = apsides(a, e)
    text(ax, (0.24, 0.0), "$A_1$", backing=False)
    callout(ax, (-1.40, 0.03), "$A_2$", at=(-1.12, 0.36), ha="center", va="bottom", gap=2)
    text(ax, (rp, 0.0), r"$\Delta t$", direction=0, dist=6)
    text(ax, (-ra, 0.0), r"$\Delta t$", direction=180, dist=6)
    text(ax, (rp, 0.0), "periapsis", direction=-50, dist=17)
    text(ax, (-ra, 0.0), "apoapsis", direction=-130, dist=17)
    b = a * math.sqrt(1 - e * e)
    ax.set_xlim(-ra - 0.45, rp + 0.45)
    ax.set_ylim(-b - 0.12, b + 0.12)
    assert abs(areas[0] - areas[1]) / areas[1] < 0.005, f"swept areas differ: {areas}"
    close_to(areas[0], math.pi * a * b * dt / T, 0.005 * areas[0], "each sector is (dt/T) of the ellipse area")
    save_figure(fig, "p21-equal-areas")


def speed_around_orbit():
    """The orbit of worked example 1, to scale, with velocity vectors to scale at four points."""
    x1 = ex1()
    a, e = x1["a"], x1["e"]
    scale = 850.0                                       # km of drawing per km/s
    fig, ax = new_axes(6.5, 4.6)
    line(ax, (-x1["ra"], 0), (x1["rp"], 0))
    draw_orbit(ax, a, e, "initial", arrows_at=(225.0,))
    draw_body(ax, (0, 0), RE, name="Earth")
    p = a * (1 - e * e)
    tips = {}
    # each vector starts level with its point and sits 4.5 pt outside the orbit, so it never hides it
    for th, lab, ldir, vdir in ((0.0, "perigee", -45.0, None), (90.0, None, None, None),
                                (180.0, "apogee", 135.0, 180.0), (270.0, None, None, None)):
        P = orbit_point(a, e, th)
        v = orbit_velocity(E, a, e, th)
        point(ax, P, None, ms=6)
        sp = float(np.hypot(*v))
        tips[th] = velocity_arrow(ax, P, v, scale, f"{fmt(sp)} km/s", offset=4.5, direction=vdir,
                                  dist=5 if vdir is None else 8)
        close_to(sp, float(vis_viva(E, float(np.hypot(*P)), a)), 1e-9, "arrow length from vis-viva")
        if lab:
            text(ax, P, lab, direction=ldir, dist=8)
    speed_key(ax, (-x1["ra"] - 2400.0, -p - 3000.0), scale, value=2.0)
    ax.set_xlim(-x1["ra"] - 5200.0, x1["rp"] + 5200.0)
    ax.set_ylim(-p - 6200.0, p + 6200.0)
    # the arrows are tangent: velocity perpendicular to r at the apsides, and r v_perp is constant
    vp, va = orbit_velocity(E, a, e, 0.0), orbit_velocity(E, a, e, 180.0)
    close_to(float(vp[0]), 0.0, 1e-12, "velocity at perigee perpendicular to r")
    close_to(float(np.hypot(*vp)) * x1["rp"], float(np.hypot(*va)) * x1["ra"], 1e-6, "r_p v_p = r_a v_a")
    save_figure(fig, "p21-speed-around-orbit")


def planet_speeds():
    """Circular speed around the Sun against distance, with the planets marked."""
    mu = MU["Sun"]
    names = PLANETS
    dist = {n: planet_distance(n) for n in names}
    fig, ax = data_axes(6.5, 3.8)
    ax.set_xscale("log")
    r = np.geomspace(0.3, 40.0, 400) * AU
    v = circular_speed(mu, r)
    ax.plot(r / AU, v, **line_kw(0))
    for n in names:
        rn = dist[n]
        vn = float(circular_speed(mu, rn))
        ax.plot(rn / AU, vn, "o", color=INK, ms=6, zorder=5)
        side = {"Mercury": 25.0, "Uranus": 235.0, "Neptune": 90.0}.get(n, 45.0)
        text(ax, (rn / AU, vn), n, direction=side, dist=8, fs=FS_SMALL)
    ax.set_xlim(0.3, 40.0)
    ax.set_ylim(0, 55)
    ax.set_xticks([0.3, 0.5, 1, 2, 5, 10, 20, 40])
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:g}"))
    ax.xaxis.set_minor_formatter(mticker.NullFormatter())
    ax.set_xlabel("Distance from the Sun, AU (log scale)")
    ax.set_ylabel("Orbital speed, km/s")
    text(ax, (2.6, float(circular_speed(mu, 2.6 * AU))), r"$v_c$ = √($\mu_{\mathrm{Sun}}$/$r$)",      # the Arial square-root sign, not a STIX glyph
         direction=45, dist=10, color=text_color(0))
    vs = [float(circular_speed(mu, dist[n])) for n in names]
    assert all(v1 > v2 for v1, v2 in zip(vs, vs[1:])), "speed falls with distance"
    close_to(vs[0] / vs[-1], math.sqrt(dist["Neptune"] / dist["Mercury"]), 1e-9, "v ~ 1/sqrt(r)")
    save_figure(fig, "p21-planet-speeds")


def trajectories_by_speed():
    """Paths from one point for five speeds, all starting perpendicular to the radius."""
    r0 = TRAJ_R0
    vc, ve = float(circular_speed(E, r0)), float(escape_speed(E, r0))
    f1, f2 = TRAJ_FC
    # data-series looks, as in the conic-sections figure (circle black solid, ellipse blue dashed,
    # parabola vermilion dotted, hyperbola in the hyperbola style); the second ellipse dark gray dash-dot
    cases = ((1, f1 * vc, "", 0.0), (0, vc, "", 0.0), (3, f2 * vc, "", 0.0),
             (2, ve, "", 0.0), ("hyperbola", TRAJ_FE * ve, "", 0.0))
    fig, ax = new_axes(*TRAJ_FIGSIZE)
    for role, v, lab, _ in cases:
        eps = 0.5 * v * v - E / r0
        if v < vc:                                          # the start is apoapsis
            e = 1.0 - r0 * v * v / E
            rp_ = r0 * (1 - e) / (1 + e)
            x, y = conic_xy(rp_, e, n=2001, rotate=180.0)
            arr = 60.0
        else:                                               # the start is periapsis
            e = r0 * v * v / E - 1.0
            if e < 1e-9:
                x, y = conic_xy(r0, 0.0, n=2001)
                arr = 160.0
            elif e < 1.0:
                x, y = conic_xy(r0, e, n=2001)
                arr = 215.0
            else:
                x, y = conic_xy(r0, e, theta0=0.0, theta1=179.9, n=4001, r_max=150000.0)
                arr = 75.0 if e < 1.05 else 60.0
        ln = ax.plot(x, y, zorder=3, **line_kw(role))[0]
        orbit_arrows(ax, r0 * (1 - e) / (1 + e) if v < vc else r0, e, (arr,),
                     rotate=180.0 if v < vc else 0.0, role=role, line=ln)
        if abs(eps) > 1e-9:
            close_to(float(vis_viva(E, r0, -E / (2 * eps))), v, 1e-9, "speed at the start point")
        close_to(float(np.hypot(x[0], y[0])) if v >= vc else float(np.max(np.hypot(x, y))), r0, 1e-6,
                 "every path passes through the start point")
    draw_body(ax, (0, 0), RE, name="Earth")
    point(ax, (r0, 0), None, ms=6, zorder=9)
    # the starting velocity, beside the paths (every path leaves along it)
    velocity_arrow(ax, (r0, 0), (0.0, 1.0), 4000.0, "$v$", offset=5.0, direction=0, dist=7, zorder=9)
    # direct labels, in the color of each path
    col = {c[0]: text_color(c[0]) for c in cases}
    text(ax, TRAJ_LAB_AT, f"{f1:g} $v_c$:\nellipse", color=col[1], fs=TRAJ_LAB_FS)   # between the ellipse and the circle
    text(ax, orbit_point(r0, 0.0, 135.0), "$v_c$: circle", direction=135.0, dist=6, color=col[0])
    e_t = f2 ** 2 - 1.0
    a_t = r0 / (1.0 - e_t)
    text(ax, (r0 - a_t, -a_t * math.sqrt(1 - e_t ** 2)), f"{f2:g} $v_c$: ellipse", direction=-90, dist=6,
         color=col[3])
    Y = TRAJ_Y
    text(ax, (r0 - Y * Y / (4 * r0), Y), r"$v_{\mathrm{esc}}$: parabola", direction=180, dist=14, color=col[2])
    e_h = 2.0 * TRAJ_FE ** 2 - 1.0
    xh, yh = conic_xy(r0, e_h, theta0=0.0, theta1=150.0, n=6001, r_max=150000.0)
    k = int(np.argmin(np.abs(yh - Y)))
    text(ax, (xh[k], yh[k]), f"{TRAJ_FE:g} $v_{{\\mathrm{{esc}}}}$:\nhyperbola", direction=0, dist=10,
         color=col["hyperbola"])
    ax.set_xlim(-29000.0, 21500.0)
    ax.set_ylim(-23000.0, TRAJ_TOP)
    close_to(ve / vc, math.sqrt(2.0), 1e-12, "v_esc = sqrt(2) v_c")
    save_figure(fig, "p21-trajectories-by-speed")



def _orbit3d(a, e, inc, raan, argp, th):
    """3-D points (in sphere radii) of the ellipse (a, e) in the plane (inc, raan) with argument
    of periapsis argp, at true anomalies th (deg)."""
    th = np.asarray(th, dtype=float)
    r = conic_radius(a * (1 - e * e), e, th)
    return Globe.orbit_vec(1.0, inc, raan, argp + th) * r


def orbital_elements():
    """The orbit plane against the reference plane: i, Omega, omega, theta, line of nodes."""
    inc, raan, argp, th_sc = OE["inc"], OE["raan"], OE["argp"], OE["th"]
    a, e = 5.5, 0.25
    fig, ax = new_axes(6.5, 5.2)
    g = Globe(ax, radius=1.0, view_lat=30.0, view_lon=30.0, grid=0, equator=False)
    g.plane(10.5, fill=PLANE_FILL)
    th = np.linspace(0.0, 360.0, 1441)
    P = _orbit3d(a, e, inc, raan, argp, th)
    g.curve(P, role="initial")
    orbit_lines = list(g.last_lines)
    t0, t1 = g.xy(_orbit3d(a, e, inc, raan, argp, [-36.0])[:, 0]), g.xy(_orbit3d(a, e, inc, raan, argp, [-35.0])[:, 0])
    rides_on(ax.add_patch(FancyArrowPatch(tuple(t0), tuple(t1), mutation_scale=1.0, lw=0.8,
                                        color=line_kw("initial")["color"],
                                        arrowstyle=ArrowStyle("-|>", head_length=MOTION_HEAD[0],
                                                              head_width=MOTION_HEAD[1]),
                                        shrinkA=0.0, shrinkB=0.0, joinstyle="miter", zorder=6)), *orbit_lines)   # motion
    O = np.zeros(3)
    xref = np.array([1.0, 0.0, 0.0])
    node_dir = g.orbit_vec(1.0, 0.0, 0.0, raan)
    peri_dir = g.orbit_vec(1.0, inc, raan, argp)
    sc_dir = g.orbit_vec(1.0, inc, raan, argp + th_sc)
    r_node = float(conic_radius(a * (1 - e * e), e, -argp))
    r_sc = float(conic_radius(a * (1 - e * e), e, th_sc))
    rp = a * (1 - e)
    node = r_node * node_dir
    PL = PLANE_FILL                                 # labels on the plane: a backing of its own color
    g.arrow(O, 14.1 * xref, color=INK, lw=LW_THIN)
    g.text(14.1 * xref, "reference\ndirection", direction=200, dist=5)
    g.curve(np.c_[-10.5 * node_dir, 10.5 * node_dir], color=GRAY, lw=LW_THIN, ls=(0, (4.0, 3.0)), hidden="same")
    g.curve(np.c_[O, rp * peri_dir], color=INK, lw=LW_THIN, hidden="same")
    g.curve(np.c_[O, r_sc * sc_dir], color=INK, lw=LW_THIN, hidden="same")
    # each angle measured from its reference in the direction of motion: the head marks its end
    g.arc(O, xref, node_dir, OE_R[0], r"$\Omega$", dist=3, arrow_end=True, backing=PL)
    g.arc(O, node_dir, peri_dir, OE_R[1], r"$\omega$", dist=OE_W_DIST, arrow_end=True, backing=PL, label_at=OE_W_AT)
    g.arc(O, peri_dir, sc_dir, OE_R[2], r"$\theta$", dist=4, arrow_end=True, backing=PL)
    east = g.orbit_vec(1.0, 0.0, 0.0, raan + 90.0)
    along = g.orbit_vec(1.0, inc, raan, 90.0)
    g.curve(np.c_[node, node + 1.7 * east], color=GRAY, lw=LW_THIN, hidden="same")
    g.arc(node, east, along, 1.35, "$i$", dist=4, backing=PL)
    g.point(node, None, ms=6)
    g.point(rp * peri_dir, None, ms=6)
    g.point(r_sc * sc_dir, None, ms=7)
    nx, ny = g.xy(node)
    # right of the node, between the line of nodes and the reference line of i, with a short leader
    callout(ax, (nx, ny), "ascending\nnode", at=(nx + OE_NODE_AT[0], ny + OE_NODE_AT[1]), ha="left", gap=3, backing=PL)
    g.text(rp * peri_dir, "periapsis", direction=30, dist=7, backing=PL)
    sx, sy = g.xy(r_sc * sc_dir)
    text(ax, (sx, sy), "spacecraft", direction=75, dist=6, backing=PL)      # on the plane, under its back edge
    g.text(-10.5 * node_dir, "line of nodes", direction=150, dist=6, color=STEEL)
    text(ax, (-8.0, -0.6), "reference\nplane", color=STEEL, backing=False)
    ax.set_xlim(-13.5, 13.0)
    ax.set_ylim(-9.6, 7.6)
    close_to(float(np.degrees(np.arccos(np.dot(east, along)))), inc, 1e-9, "arc at the node spans i")
    close_to(float(np.degrees(np.arccos(np.dot(xref, node_dir)))), raan, 1e-9, "arc spans Omega")
    close_to(float(np.degrees(np.arccos(np.dot(node_dir, peri_dir)))), argp, 1e-9, "arc spans omega")
    close_to(float(node[2]), 0.0, 1e-12, "the ascending node lies in the reference plane")
    save_figure(fig, "p21-orbital-elements")


def make_all():
    two_body()
    ellipse_geometry()
    conic_sections()
    orbital_elements()
    equal_areas()
    speed_around_orbit()
    planet_speeds()
    trajectories_by_speed()


# ===================================================================== values
def values():
    r = lambda key, text: record(TAG, key, text)          # noqa: E731
    # constants table and G
    r("G", fmt_sci(G_SI))
    for body in ("Sun", "Mercury", "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn"):
        r(f"mu-{body}", fmt_sci(MU[body]))
        r(f"R-{body}", fmt(RADIUS[body], 4))
    for body in ("Mercury", "Venus", "Earth", "Jupiter", "Saturn"):     # no Mars (PLAN rule 4)
        r(f"d-{body}", fmt_sci(SUN_DISTANCE[body]))
        r(f"T-{body}", fmt(ORBIT_DAYS[body], 4 if body in ("Mercury", "Venus") else 5))   # as given
    r("R-Earth-mean", fmt(RADIUS_EARTH_MEAN))
    # circular and escape speed at Earth's surface; a low orbit
    vc0, ve0 = float(circular_speed(E, RE)), float(escape_speed(E, RE))
    r("vc-surface", fmt(vc0))
    r("vesc-surface", fmt(ve0))
    r("mu-over-R", fmt(E / RE, 5))                          # five figures: sqrt of it gives v_c to four
    r("leo-h", fmt(LEO_H, 3))
    r("leo-r", fmt(RE + LEO_H))
    r("leo-T-s", fmt(float(period(E, RE + LEO_H))))
    # minutes from the printed seconds, to three figures, so the conversion follows from the page
    r("leo-T-min", fmt(float(fmt(float(period(E, RE + LEO_H))).replace(",", "")) / 60.0, 3))
    r("leo-vc", fmt(float(circular_speed(E, RE + LEO_H))))
    r("sqrt2", fmt(math.sqrt(2.0)))
    r("mu-Earth-SI", fmt_sci(MU["Earth"] * 1e9))
    r("km-m-factor", fmt(math.sqrt(1000.0), 3))
    r("kepler-ratio", fmt(2.0 ** 1.5))
    # worked example 1
    x = ex1()
    r("ex1-hp", fmt(EX1_HP, 3))
    r("ex1-ha", fmt(EX1_HA))
    r("ex1-rp", fmt(x["rp"]))
    r("ex1-ra", fmt(x["ra"]))
    r("ex1-a", fmt(x["a"]))
    r("ex1-diff", fmt(x["ra"] - x["rp"]))
    r("ex1-sum", fmt(x["ra"] + x["rp"]))
    r("ex1-e", fmt(x["e"]))
    r("ex1-T-s", fmt(x["T"]))
    r("ex1-T-min", fmt(x["T"] / 60.0))
    r("ex1-T-h", fmt(x["T"] / 3600.0))
    r("ex1-vp2", fmt(x["vp"] ** 2))
    r("ex1-va2", fmt(x["va"] ** 2))
    r("ex1-vp", fmt(x["vp"]))
    r("ex1-va", fmt(x["va"]))
    r("ex1-eps", fmt(x["eps"]))
    r("ex1-ke-p", fmt(0.5 * x["vp"] ** 2))
    r("ex1-pe-p", fmt(E / x["rp"]))
    # the second-law check from the printed radii and speeds: both products, to four figures
    num = lambda s: float(s.replace(",", ""))              # noqa: E731
    r("ex1-rpvp", fmt(num(fmt(x["rp"])) * num(fmt(x["vp"])), 5))
    r("ex1-ravp", fmt(num(fmt(x["ra"])) * num(fmt(x["va"])), 5))
    # the radius at theta = 90 deg, p = r_p (1 + e), from the printed r_p and e
    p = x["a"] * (1 - x["e"] ** 2)
    r("ex1-1pe", fmt(1.0 + num(fmt(x["e"])), 5))
    r("ex1-p", fmt(num(fmt(x["rp"])) * num(fmt(1.0 + num(fmt(x["e"])), 5))))
    assert fmt(p) == fmt(num(fmt(x["rp"])) * (1.0 + num(fmt(x["e"])))), "p from the printed digits"
    r("ex1-v90", fmt(float(vis_viva(E, p, x["a"]))))
    # worked example 2 (Venus)
    y = ex2()
    r("ex2-T-h", fmt(EX2_T_H, 2))
    r("ex2-T-s", fmt(y["T"]))
    r("ex2-hp", fmt(EX2_HP, 3))
    r("ex2-mu", fmt_sci(y["mu"]))
    r("ex2-R", fmt(y["R"]))
    r("ex2-Tover2pi", fmt_dec(y["T"] / (2 * math.pi), 2))
    r("ex2-a", fmt(y["a"]))
    r("ex2-rp", fmt(y["rp"]))
    r("ex2-ra", fmt(y["ra"]))
    r("ex2-ha", fmt(y["ha"]))
    r("ex2-e", fmt(y["e"]))
    r("ex2-a-1dp", fmt_dec(y["a"], 1))
    r("ex2-1me", fmt(1.0 - y["e"]))
    close_to(float(fmt_dec(y["a"], 1).replace(",", "")) * float(fmt(1.0 - y["e"])), y["rp"], 0.5, "check line of ex2")
    r("ex2-diff", fmt(y["ra"] - y["rp"]))
    r("ex2-sum", fmt(y["ra"] + y["rp"]))
    # worked example 3 (a small body at 1 AU from the Sun)
    z, z2 = ex3(EX3_V), ex3(EX3_V2)
    r("ex3-v", fmt(EX3_V, 3))
    r("ex3-v2", fmt(EX3_V2, 3))
    r("ex3-AU", fmt_sci(AU))
    r("ex3-mu", fmt_sci(z["mu"]))
    r("ex3-ke", fmt_dec(z["ke"], 1))
    r("ex3-pe", fmt(z["pe"], 5))
    r("ex3-eps", fmt(z["eps"]))
    r("ex3-a", fmt_sci(z["a"]))
    r("ex3-a-AU", fmt(z["a"] / AU))
    r("ex3-T-yr", fmt((z["a"] / AU) ** 1.5))
    r("ex3-vesc", fmt(z["vesc"]))
    r("ex3-vc", fmt(z["vc"]))
    r("ex3-ke2", fmt_dec(z2["ke"], 1))
    r("ex3-eps2", fmt(z2["eps"]))
    # figures: values quoted in captions and alt text
    vc13, ve13 = float(circular_speed(E, TRAJ_R0)), float(escape_speed(E, TRAJ_R0))
    r("traj-r0", fmt(TRAJ_R0))
    r("traj-vc", fmt(vc13))
    r("traj-vesc", fmt(ve13))
    # alt text and text: the speeds of the planets of the constants table follow from the table's
    # printed distance (Saturn: 1.427 x 10^9 km gives 9.643; 9.537 AU would give 9.644)
    table_d = lambda n: float(fmt_sci(SUN_DISTANCE[n]).replace(" \\times 10^{", "e").rstrip("}"))   # noqa: E731
    for n in ("Mercury", "Earth"):
        r(f"planet-v-{n}", fmt(float(circular_speed(MU["Sun"], table_d(n)))))
    r("planet-v-Neptune", fmt(float(circular_speed(MU["Sun"], SUN_DISTANCE["Neptune"]))))
    r("planet-d-Neptune", fmt(SUN_DISTANCE["Neptune"] / AU))
    r("planet-d-Uranus", fmt(SUN_DISTANCE["Uranus"] / AU))
    for n in ("Venus", "Jupiter", "Saturn"):                    # four significant figures, as the others
        r(f"planet-v-{n}", fmt(float(circular_speed(MU["Sun"], table_d(n)))))
    r("planet-v-Uranus", fmt(float(circular_speed(MU["Sun"], SUN_DISTANCE["Uranus"]))))
    r("planet-v-0.3", fmt(float(circular_speed(MU["Sun"], 0.3 * AU))))
    r("planet-v-40", fmt(float(circular_speed(MU["Sun"], 40.0 * AU))))
    r("fig-ell-e", f"{ELL_E:g}")
    for k, e in enumerate(CONIC_E[1:]):
        r(f"fig-conic-e{k + 1}", f"{e:g}")
    r("fig-kepler-e", f"{KEPLER_E:g}")
    mu, T = 1.0, 2 * math.pi
    th_p = 2 * float(true_anomaly_at_time(mu, 1.0, KEPLER_E, T / KEPLER_N / 2))
    th_a = 2 * (180.0 - float(true_anomaly_at_time(mu, 1.0, KEPLER_E, T / 2 - T / KEPLER_N / 2)))
    r("fig-kepler-thp", fmt(th_p, 3))
    r("fig-kepler-tha", fmt(th_a, 2))
    for k, v in OE.items():
        r(f"fig-oe-{k}", f"{v:g}")
    r("fig-traj-f1", f"{TRAJ_FC[0]:g}")
    r("fig-traj-f2", f"{TRAJ_FC[1]:g}")
    r("fig-traj-fe", f"{TRAJ_FE:g}")
