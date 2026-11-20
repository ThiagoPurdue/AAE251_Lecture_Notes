"""Figures and values of 2.4 Patched Conics.

The worked example is the Mercury orbiter of the course slides (ported here with the
constants of orbits.py): a Hohmann transfer around the
Sun from Earth to Mercury, a departure burn from a 185 km circular parking orbit around
Earth, and a capture burn into a 400 km circular orbit around Mercury. No Mars numbers
anywhere (PLAN rule 4).
"""
from matplotlib.ticker import FixedLocator, NullLocator

from chapter_2.orbits import *  # noqa: F401,F403

SUN, E, ME = MU["Sun"], MU["Earth"], MU["Mercury"]
RE, RME = RADIUS["Earth"], RADIUS["Mercury"]
R_EARTH, R_MERC = SUN_DISTANCE["Earth"], SUN_DISTANCE["Mercury"]
H_PARK, H_CAP = 185.0, 400.0                      # parking and capture orbit altitudes, km (the deck's)
TARGETS = ("Mercury", "Venus", "Jupiter", "Saturn")  # synodic-period table (no Mars: PLAN rule 4)


def soi(planet):
    """Radius of a planet's sphere of influence around the Sun, km: r (mu_p/mu_Sun)^(2/5)
    (Laplace's estimate, as in Curtis, Chapter 8)."""
    return SUN_DISTANCE[planet] * (MU[planet] / SUN) ** 0.4


def mercury():
    """Every number of the Mercury example."""
    h = hohmann(SUN, R_EARTH, R_MERC)
    v_e, v_ta = h["v_c1"], h["v_t1"]              # Earth's speed; transfer speed at Earth (aphelion)
    v_m, v_tp = h["v_c2"], h["v_t2"]              # Mercury's speed; transfer speed at Mercury (perihelion)
    vinf_d, vinf_a = v_e - v_ta, v_tp - v_m
    rp_e, rp_m = RE + H_PARK, RME + H_CAP
    vc_e, vp_e = float(circular_speed(E, rp_e)), float(periapsis_speed_hyperbola(E, rp_e, vinf_d))
    vc_m, vp_m = float(circular_speed(ME, rp_m)), float(periapsis_speed_hyperbola(ME, rp_m, vinf_a))
    tof = h["tof"] / DAY
    travel = 360.0 / ORBIT_DAYS["Mercury"] * tof          # angle Mercury moves during the trip, deg
    phase = (180.0 - travel) % 360.0                       # Mercury's lead over Earth at departure, deg
    return dict(h=h, v_e=v_e, v_ta=v_ta, v_m=v_m, v_tp=v_tp, vinf_d=vinf_d, vinf_a=vinf_a, rp_e=rp_e,
                rp_m=rp_m, vc_e=vc_e, vp_e=vp_e, vc_m=vc_m, vp_m=vp_m, dv_d=vp_e - vc_e, dv_a=vp_m - vc_m,
                vesc_e=float(escape_speed(E, rp_e)), vesc_m=float(escape_speed(ME, rp_m)), tof=tof,
                travel=travel, phase=phase, dep=hyperbola(E, rp_e, vinf_d), arr=hyperbola(ME, rp_m, vinf_a))


def _check_deck(m):
    """The values printed in the course slides (Mercury example and synodic table)."""
    got = [fmt(m[k]) for k in ("v_e", "v_ta", "v_tp")] + [fmt(m[k], 3) for k in ("vinf_d", "dv_d", "vinf_a", "dv_a")]
    assert got == ["29.78", "22.25", "57.49", "7.53", "5.56", "9.61", "7.60"], got
    assert fmt(m["v_m"]) == "47.87", m["v_m"]       # the deck prints 47.88 (reported, PLAN rule 11)
    assert fmt(m["tof"], 3) == "105" and fmt(m["phase"], 3) == "108", (m["tof"], m["phase"])
    syn = [fmt(synodic_period(ORBIT_DAYS["Earth"], ORBIT_DAYS[p]), 3) for p in TARGETS]
    assert syn == ["116", "584", "399", "378"], syn


# ===================================================================== figures
def _toward(ax, xy, ang, length, label, label_dir=None, dist=6.0):
    """A thin gray direction arrow (a direction only, not a vector to scale) from xy, with its
    label to the right of the arrow, centered on it: the direction key of the patched-conics
    figures (label_dir, deg, places it elsewhere)."""
    xy = np.asarray(xy, dtype=float)
    tip = xy + length * np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
    arrow(ax, xy, tip, color=GRAY, lw=LW_THIN, head="small")
    if label_dir is None:
        right = xy if xy[0] >= tip[0] else tip
        text(ax, (right[0], 0.5 * (xy[1] + tip[1])), label, direction=0.0, dist=dist, fs=FS_SMALL, color=STEEL,
             ha="left", va="center")
    else:
        text(ax, tip, label, direction=label_dir, dist=dist, fs=FS_SMALL, color=STEEL)
    return tip


def _dashed_circle(ax, xy, r):
    return ax.add_patch(Circle(xy, r, fc="none", ec=GRAY, lw=LW_THIN, ls=(0, (4.0, 3.0)), zorder=1))


AC_SIZE, AC_XLIM, AC_YLIM = (4.6, 5.2), (-4.1, 3.8), (-5.9, 4.6)   # arrival figure: inches, Mercury radii
AC_R_IN, AC_R_FLY, AC_CAP_AT, AC_KEY = 3.6, 3.8, (-1.4, -2.3), (-3.9, 4.1)
DH_XLIM, DH_KEY, DH_LAB, DH_PARK = (-2.7, 3.3), (-2.5, 4.4), (70.0, 22.0), (-2.5, -1.4)   # departure figure, Earth radii
HT_AT = (0.30, -0.45)       # heliocentric figure: "Mercury at departure", in units of Earth's orbit radius
TC_EARTH = (0.45, 0.58)     # three-conics: Earth's radius and its parking orbit in the left inset
TC_R_IN, TC_X_IN = 1.5, 3.25    # three-conics: radius and center of each inset: the upper zoom line then meets
                                # the left inset 15 degrees below the point where the hyperbola leaves it
TC_NUM = ((-0.8, 0.6), (-0.8, 0.6))      # three-conics: the numbers 1 and 3, from the centers of the side views


def _number(ax, xy, n, color=INK):
    """A small numbered circle that names a piece of the trip (explained in the caption)."""
    return ax.annotate(str(n), xy=tuple(xy), ha="center", va="center", fontsize=FS_SMALL, color=color, zorder=12,
                       bbox=dict(boxstyle="circle,pad=0.22", fc="white", ec=color, lw=0.9), annotation_clip=False)


def three_conics():
    """Overview, not to scale: the transfer ellipse around the Sun in the middle, and magnified
    views of the two spheres of influence: departure hyperbola at Earth (left), arrival
    hyperbola and capture orbit at Mercury (right). The three conics are numbered 1, 2, 3
    (the caption names them)."""
    m = mercury()
    fig, ax = new_axes(6.5, 2.6)
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)      # the drawing uses the full width
    # middle: orbit radii to scale (1 AU = K units); planets and spheres of influence are not.
    # The orbit looks of the heliocentric-transfer figure: Earth's orbit initial, Mercury's final.
    K = 1.45
    rE, rM = K, K * R_MERC / R_EARTH
    a_t, e_t = 0.5 * (rE + rM), (rE - rM) / (rE + rM)
    draw_orbit(ax, rE, 0.0, "initial", arrows_at=(70.0,))
    draw_orbit(ax, rM, 0.0, "final", arrows_at=(115.0,))
    draw_orbit(ax, a_t, e_t, "transfer", theta0=180.0, theta1=360.0, arrows_at=(245.0,))
    draw_body(ax, (0, 0), None, name="Sun", where=90, ms=7, dist=2.5, fs=FS_SMALL)
    zoom_lines = []
    s_small, R_in, X_in = 0.11, TC_R_IN, TC_X_IN          # small sphere in the middle; magnified sphere; its center
    for p_small, sgn in (((-rE, 0.0), -1.0), ((rM, 0.0), 1.0)):
        small = _dashed_circle(ax, p_small, s_small)
        ax.plot(*p_small, "o", ms=5, color=INK, zorder=6)
        c_in = np.array([sgn * X_in, 0.0])
        big = _dashed_circle(ax, c_in, R_in)
        # zoom lines: the two outer common tangents of the small circle and the inset's circle,
        # ending at their tangent points, so they stay outside both circles
        c1 = np.asarray(p_small, dtype=float)
        dvec = c_in - c1
        dist = float(np.hypot(*dvec))
        u = dvec / dist
        alpha = math.asin((R_in - s_small) / dist)
        for sgn_t in (1.0, -1.0):
            ang = sgn_t * (0.5 * math.pi + alpha)
            n = np.array([u[0] * math.cos(ang) - u[1] * math.sin(ang), u[0] * math.sin(ang) + u[1] * math.cos(ang)])
            t1, t2 = c1 + s_small * n, c_in + R_in * n
            connects(ax.plot([t1[0], t2[0]], [t1[1], t2[1]], color=GRAY, lw=0.6, zorder=0.5)[0], small, big)
            zoom_lines.append((t1, t2, c_in))
    _number(ax, (0.0, -rE - 0.25), 2, color=text_color("transfer"))
    k_v = 0.06                                                      # arrow length per km/s: the two v-infinity arrows to scale
    L_d, L_a = burn_lengths([m["dv_d"], m["dv_a"]], longest=24.0)  # burn arrows in proportion to the delta-Vs
    gap = 0.07                                                      # v-infinity arrows start 4 pt outside the sphere

    # left: departure at Earth. The hyperbola has the real eccentricity (1.93); sizes are not to scale.
    cL = np.array([-X_in, 0.0])
    Rb, rp = TC_EARTH                                               # small enough that the hyperbola leaves the
                                                                    # sphere well above the upper zoom line
    vinf = math.sqrt((m["dep"]["e"] - 1.0) / rp)                    # mu = 1 gives the same eccentricity
    rot_d = 90.0 - m["dep"]["theta_inf"]                            # leaves upward: against Earth's motion
    draw_orbit(ax, rp, 0.0, "initial", center=cL, arrows_at=(215,))
    draw_body(ax, cL, Rb, name="Earth", fs=FS_SMALL)
    g1 = draw_hyperbola(ax, 1.0, rp, vinf, rotate=rot_d, center=cL, r_max=R_in, asymptote=False, arrows_at=())
    burn(ax, orbit_point(rp, 0.0, rot_d, center=cL), rot_d + 90.0, length=L_d, center=cL)
    v0 = g1["end"] + gap * g1["out_dir"]
    arrow(ax, v0, v0 + k_v * m["vinf_d"] * g1["out_dir"])
    text(ax, v0 + 0.5 * k_v * m["vinf_d"] * g1["out_dir"], r"$v_\infty$", direction=0, dist=8)
    text(ax, cL + np.array([0.0, -R_in]), "sphere of influence", direction=-90, dist=4, fs=FS_SMALL, color=STEEL)
    _number(ax, cL + np.array(TC_NUM[0]), 1, color=text_color("hyperbola"))

    # right: arrival at Mercury. The real arrival hyperbola is nearly straight (e = 12.9).
    cR = np.array([X_in, 0.0])
    rc = 0.70
    vinf3 = math.sqrt((m["arr"]["e"] - 1.0) / rc)
    rot_a = m["arr"]["theta_inf"] - 90.0                            # arrives moving up, as Mercury does
    draw_orbit(ax, rc, 0.0, "final", center=cR, arrows_at=(150,))
    draw_body(ax, cR, 0.52, name="Mercury", fs=FS_SMALL)          # wide enough for its name
    g3 = draw_hyperbola(ax, 1.0, rc, vinf3, rotate=rot_a, center=cR, branch="in", r_max=R_in, asymptote=False,
                        arrows_at=())
    burn(ax, orbit_point(rc, 0.0, rot_a, center=cR), rot_a - 90.0, length=L_a, center=cR)
    v1 = g3["start"] - gap * g3["in_dir"]
    arrow(ax, v1 - k_v * m["vinf_a"] * g3["in_dir"], v1)
    text(ax, v1 - 0.5 * k_v * m["vinf_a"] * g3["in_dir"], r"$v_\infty$", direction=0, dist=8)
    _number(ax, cR + np.array(TC_NUM[1]), 3, color=text_color("hyperbola"))
    ax.set_xlim(-X_in - R_in - 0.08, X_in + R_in + 0.08)
    ax.set_ylim(-R_in - 0.45, R_in + 0.26)
    # what was drawn: the transfer touches both orbits; the hyperbolas have the real eccentricities
    # and point the right way (leaving against Earth's motion, arriving with Mercury's)
    x, y = orbit_xy(a_t, e_t, theta0=180.0, theta1=360.0)
    r = np.hypot(x, y)
    close_to(float(r.max()), rE, 1e-9, "transfer touches Earth's orbit")
    close_to(float(r.min()), rM, 1e-9, "transfer touches Mercury's orbit")
    close_to(1.0 + rp * vinf ** 2, m["dep"]["e"], 1e-9, "departure hyperbola shape")
    close_to(1.0 + rc * vinf3 ** 2, m["arr"]["e"], 1e-9, "arrival hyperbola shape")
    close_to(float(g1["out_dir"][1]), 1.0, 1e-9, "v-infinity against Earth's motion (Earth moves down at the left)")
    close_to(float(g3["in_dir"][1]), 1.0, 1e-9, "arrives moving up, with Mercury (Mercury moves up at the right)")
    close_to(L_d / L_a, m["dv_d"] / m["dv_a"], 1e-12, "burn arrows in proportion to the delta-Vs")
    # each zoom line is tangent to its inset's circle: its ends and its distance from the center are on
    # the circle to within 0.5 pt at the drawn scale
    fig.canvas.draw()
    pt = float(np.hypot(*(ax.transData.transform((1.0, 0.0)) - ax.transData.transform((0.0, 0.0))))) * 72.0 / fig.dpi
    for t1, t2, c2 in zoom_lines:
        close_to(float(np.hypot(*(t2 - c2))), R_in, 0.5 / pt, "zoom line ends on the inset circle")
        w = (t2 - t1) / np.hypot(*(t2 - t1))
        close_to(abs(float(np.cross(w, c2 - t1))), R_in, 0.5 / pt, "zoom line tangent to the inset circle")
    # In the middle panel only, where the zoom lines must cross orbits: each small circle sits on the planet's
    # orbit and on the transfer orbit, which run through it, so each line crosses them just beside the circle;
    # and Mercury's orbit lies inside Earth's while the right inset lies outside it, so both lines to that
    # inset cross Earth's orbit, at a wide angle. Inside the insets the lines cross nothing.
    # (x from -1.5 to 1.4: the middle panel; the insets span |x| = 1.75 to 4.75)
    middle = ["#0072b2 at data (-1.4", "#d55e00 at data (-1.4", "#0072b2 at data (1.3", "#009e73 at data (0.5",
              "#d55e00 at data (0.5"]
    save_figure(fig, "p24-three-conics", allow=tuple("connector line crosses a line " + c for c in middle))


def heliocentric_transfer():
    """To scale: Sun, orbits of Earth and Mercury, the Hohmann half-ellipse, the planets at
    departure and at arrival, and the 108 deg lead angle."""
    m = mercury()
    h = m["h"]
    fig, ax = new_axes(6.5, 5.3)
    rE, rM = R_EARTH, R_MERC
    draw_orbit(ax, rE, 0.0, "initial", label="Earth's orbit", label_at=128, arrows_at=(100,))
    draw_orbit(ax, rM, 0.0, "final", label="Mercury's orbit", label_at=118, arrows_at=(205,), dist=6)
    # transfer: aphelion at Earth (left), perihelion at Mercury (right), traveled counterclockwise
    draw_orbit(ax, h["a_t"], h["e_t"], "transfer", theta0=180.0, theta1=360.0, arrows_at=(232.0,),
               label="transfer orbit", label_at=262, label_dir=-90, dist=8)
    draw_body(ax, (0, 0), None, name="Sun", where=90, ms=12, dist=5)
    pE0 = np.array([-rE, 0.0])
    pM0 = rM * np.array([math.cos(math.radians(180.0 + m["phase"])), math.sin(math.radians(180.0 + m["phase"]))])
    pMeet = np.array([rM, 0.0])
    line(ax, pE0, (0, 0))
    line(ax, (0, 0), pM0)
    angle_arc(ax, (0, 0), 0.31 * rE, 180.0, 180.0 + m["phase"], None, arrow_end=True)
    bis = math.radians(180.0 + 0.5 * m["phase"])
    text(ax, 0.17 * rE * np.array([math.cos(bis), math.sin(bis)]), f"{fmt(m['phase'], 3)}°", offset=(0.0, -1.5))
    point(ax, pE0, "Earth at\ndeparture", direction=180, ms=9)
    point(ax, pM0, None, kind="square", ms=8)
    callout(ax, pM0, "Mercury at\ndeparture", at=(HT_AT[0] * rE, HT_AT[1] * rE), ha="left")
    point(ax, pMeet, None, kind="open", ms=9)
    text(ax, pMeet, "Mercury at\narrival", direction=0, dist=8)
    ax.set_xlim(-1.40 * rE, 1.42 * rE)
    ax.set_ylim(-1.13 * rE, 1.08 * rE)
    # what was drawn: the half ellipse ends on both orbits; Mercury, 108 deg ahead, reaches the meeting point
    x, y = orbit_xy(h["a_t"], h["e_t"], theta0=180.0, theta1=360.0)
    close_to(float(np.hypot(x[0], y[0])), rE, 1e-3, "starts on Earth's orbit")
    close_to(float(np.hypot(x[-1], y[-1])), rM, 1e-3, "ends on Mercury's orbit")
    ang0 = math.degrees(math.atan2(pM0[1], pM0[0])) % 360.0
    close_to((ang0 + m["travel"]) % 360.0, 0.0, 1e-9, "Mercury reaches the meeting point when the spacecraft does")
    # Mercury's position at departure lies between its own orbit and the transfer orbit, which pass
    # 10 pt apart there; any leader from outside must cross the transfer orbit to reach it
    save_figure(fig, "p24-heliocentric-transfer", allow=("leader of 'Mercury at\\ndeparture' crosses a line",))


def departure_hyperbola():
    """To scale near Earth: the 185 km parking orbit, the burn at periapsis, the departure
    hyperbola of the Mercury example and its asymptote, v-infinity against Earth's motion."""
    m = mercury()
    g0 = m["dep"]
    rp = m["rp_e"]
    rot = 90.0 - g0["theta_inf"]                  # outgoing asymptote straight up
    fig, ax = new_axes(4.2, 6.0)
    draw_orbit(ax, rp, 0.0, "initial", arrows_at=(160,))
    draw_body(ax, (0, 0), RE, name="Earth")
    r_max = 5.6 * RE
    g = draw_hyperbola(ax, E, rp, m["vinf_d"], rotate=rot, r_max=r_max, arrows_at=(), asymptote=False,
                       label="departure\nhyperbola", label_at=DH_LAB[0], label_dir=0.0, dist=DH_LAB[1])
    # the asymptote, from well above the burn to the end of the branch
    x_as = float(g["foot_out"][0])
    ax.plot([x_as, x_as], [1.6 * RE, float(g["end"][1]) + 0.2 * RE], zorder=2, gid="asymptote", **line_kw("boundary"))
    pb = orbit_point(rp, 0.0, rot)
    burn(ax, pb, rot + 90.0, r"$\Delta V$", label_dir=-30.0, dist=4)
    callout(ax, orbit_point(rp, 0.0, 225.0), "parking orbit, 185 km", at=(DH_PARK[0] * RE, DH_PARK[1] * RE), ha="left",
            va="top")
    scale = 0.3 * RE                              # km per km/s
    tip = velocity_arrow(ax, g["end"], m["vinf_d"] * g["out_dir"], scale, None)
    text(ax, 0.5 * (g["end"] + tip), rf"$v_\infty$ = {fmt(m['vinf_d'])} km/s", direction=180, dist=6)
    text(ax, (x_as, 2.6 * RE), "asymptote", direction=0, dist=5, fs=FS_SMALL, color=STEEL)
    # the direction key, beside the hyperbola at mid-height; labels to the right of the arrows, as in the
    # arrival figure
    _toward(ax, (DH_KEY[0] * RE, DH_KEY[1] * RE), 0.0, 1.3 * RE, "to the Sun")
    _toward(ax, ((DH_KEY[0] + 0.65) * RE, (DH_KEY[1] - 0.9) * RE), -90.0, 1.3 * RE, "Earth's motion\naround the Sun")
    ax.set_xlim(DH_XLIM[0] * RE, DH_XLIM[1] * RE)
    ax.set_ylim(-2.2 * RE, 7.6 * RE)
    # what was drawn: burn on the parking orbit at the periapsis; v-infinity antiparallel to Earth's velocity
    close_to(float(np.hypot(*pb)), rp, 1e-9, "burn on the parking orbit")
    close_to(float(np.hypot(*g["end"])), r_max, 1e-6, "hyperbola drawn out to r_max")
    close_to(float(np.dot(g["out_dir"], [0.0, -1.0])), -1.0, 1e-12, "v-infinity opposite Earth's motion")
    close_to(float(np.hypot(*(tip - g["end"]))) / scale, m["vinf_d"], 1e-9, "v-infinity arrow to scale")
    # the 185 km parking orbit is 1.5 pt from Earth's limb at this scale: its motion arrowhead overlaps the limb
    save_figure(fig, "p24-departure-hyperbola", allow=("arrowhead at data (-6077, 2490) lies on an outline",))


def vinf_vs_dv():
    """Departure delta-V from the 185 km parking orbit against v-infinity, one burn in the parking
    orbit against two (escape first, then a burn far from Earth)."""
    m = mercury()
    rp = m["rp_e"]
    vi = np.linspace(0.0, 12.0, 241)
    one = periapsis_speed_hyperbola(E, rp, vi) - m["vc_e"]
    two = (m["vesc_e"] - m["vc_e"]) + vi
    fig, ax = data_axes(6.5, 4.0)
    ax.plot(vi, two, **line_kw(1))                      # data series, not orbit roles
    ax.plot(vi, one, **line_kw(0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.set_xticks(np.arange(0, 13, 2))
    ax.set_yticks(np.arange(0, 17, 4))
    ax.set_xlabel(r"Hyperbolic excess speed $v_\infty$, km/s")
    ax.set_ylabel(r"Departure $\Delta V$, km/s")
    text(ax, (6.0, float(np.interp(6.0, vi, two))), "escape first, then burn\nfar from Earth",
         direction=135, dist=8, color=text_color(1))
    text(ax, (10.0, float(np.interp(10.0, vi, one))), "one burn in the\nparking orbit",
         direction=-45, dist=8, color=text_color(0))
    ax.plot([m["vinf_d"]], [m["dv_d"]], "o", color=INK, ms=7, mec="white", mew=0.8, zorder=6)
    callout(ax, (m["vinf_d"], m["dv_d"]), f"Mercury example:\n{fmt(m['vinf_d'])} km/s, {fmt(m['dv_d'])} km/s",
            at=(7.9, 2.4), ha="left")
    callout(ax, (0.0, float(one[0])), f"escape only: {fmt(one[0])} km/s", at=(0.9, 1.3), ha="left")
    # what was drawn: the one-burn curve starts at the escape cost and stays below the two-burn line
    close_to(float(one[0]), m["vesc_e"] - m["vc_e"], 1e-12, "v-infinity = 0 costs the escape burn")
    assert np.all(one[1:] < two[1:]), "one burn deep in the well always beats escape-then-burn"
    assert np.all(np.diff(one) < np.diff(vi)), "each km/s of v-infinity costs less than 1 km/s"
    save_figure(fig, "p24-vinf-vs-dv")


def speed_vs_distance():
    """Speed on the departure hyperbola of the example against distance from Earth's center,
    with the escape speed and v-infinity, out to the sphere of influence."""
    m = mercury()
    r_soi = soi("Earth")
    r = np.geomspace(m["rp_e"], 1.0e6, 400)
    v = periapsis_speed_hyperbola(E, r, m["vinf_d"])
    ve = escape_speed(E, r)
    fig, ax = data_axes(6.5, 4.0)
    ax.set_xscale("log")
    ax.plot(r, v, **line_kw(0))                         # data series, not orbit roles
    ax.plot(r, ve, **line_kw(1))
    ax.axhline(m["vinf_d"], **line_kw("boundary"))
    ax.axvline(r_soi, **line_kw("reference"))
    ax.set_xlim(6.0e3, 1.0e6)
    ax.set_ylim(0, 15)
    ax.xaxis.set_major_locator(FixedLocator([1e4, 1e5, 1e6]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(CommaFormatter())
    ax.set_yticks(np.arange(0, 16, 3))
    ax.set_xlabel("Distance from Earth's center, km (log scale)")
    ax.set_ylabel("Speed, km/s")
    text(ax, (2.2e4, float(periapsis_speed_hyperbola(E, 2.2e4, m["vinf_d"]))), "on the departure hyperbola",
         direction=45, dist=6, color=text_color(0))
    text(ax, (1.2e5, float(escape_speed(E, 1.2e5))), r"escape speed √(2$\mu$/$r$)",
         direction=45, dist=5, color=text_color(1))
    text(ax, (6.0e4, m["vinf_d"]), rf"$v_\infty$ = {fmt(m['vinf_d'])} km/s", direction=-90, dist=5, color=STEEL)
    text(ax, (r_soi, 12.5), "edge of Earth's\nsphere of influence", direction=180, dist=6, color=STEEL)
    # what was drawn: the speed falls toward v-infinity and is within 1% of it at the sphere of influence
    v_soi = float(periapsis_speed_hyperbola(E, r_soi, m["vinf_d"]))
    assert np.all(np.diff(v) < 0) and np.all(v > m["vinf_d"]), "speed falls toward v-infinity"
    assert v_soi / m["vinf_d"] - 1.0 < 0.01, v_soi
    close_to(float(np.sqrt(v[0] ** 2 - ve[0] ** 2)), m["vinf_d"], 1e-9, "v^2 = v_inf^2 + v_esc^2")
    save_figure(fig, "p24-speed-vs-distance")


def arrival_capture():
    """To scale near Mercury: the arrival hyperbola of the example, the capture burn at periapsis
    against the motion, beside the path, the 400 km capture orbit, and the flyby path without
    the burn (dotted gray, at orbit weight, with its motion arrowhead)."""
    m = mercury()
    g0 = m["arr"]
    rp = m["rp_m"]
    rot = g0["theta_inf"] - 90.0                  # arrives moving up (with Mercury), passes away from the Sun
    fig, ax = new_axes(*AC_SIZE)
    r_in, r_fly = AC_R_IN * RME, AC_R_FLY * RME   # drawn length of the incoming branch and of the flyby
    draw_orbit(ax, rp, 0.0, "final", arrows_at=(150,))
    draw_body(ax, (0, 0), RME, name="Mercury", where=180.0, dist=12)
    # the flyby: a path, dotted gray at orbit weight, with one arrowhead two thirds of the way along
    lim = math.degrees(math.acos((g0["p"] / r_fly - 1.0) / g0["e"]))
    xf, yf = orbit_xy(g0["a"], g0["e"], theta0=0.0, theta1=lim, rotate=rot)
    s_f = np.r_[0.0, np.cumsum(np.hypot(np.diff(xf), np.diff(yf)))]
    th_f = float(np.interp(2.0 / 3.0 * s_f[-1], s_f, np.linspace(0.0, lim, len(xf))))
    draw_orbit(ax, g0["a"], g0["e"], "reference", rotate=rot, theta0=0.0, theta1=lim, arrows_at=(th_f,),
               color=GRAY, linewidth=LW_ORBIT, linestyle=(0, (0.1, 2.6)), dash_capstyle="round", zorder=2.5)
    g = draw_hyperbola(ax, ME, rp, m["vinf_a"], rotate=rot, branch="in", r_max=r_in, asymptote=False,
                       arrows_at=(), label="arrival hyperbola", label_at=-60.0, label_dir=0.0, dist=10)
    text(ax, orbit_point(g0["a"], g0["e"], lim, rot), "without the burn:\nflyby", direction=0.0, dist=8,
         color=STEEL, ha="left", va="top")
    pb = orbit_point(rp, 0.0, rot)
    burn(ax, pb, rot - 90.0, r"$\Delta V$", length=24.0, label_dir=0.0, dist=3)   # beside the path, away from Mercury
    callout(ax, orbit_point(rp, 0.0, 235.0), "capture orbit, 400 km", at=(AC_CAP_AT[0] * RME, AC_CAP_AT[1] * RME),
            ha="right")
    scale = 0.22 * RME
    start = g["start"]
    tail = start - m["vinf_a"] * scale * g["in_dir"]
    velocity_arrow(ax, tail, m["vinf_a"] * g["in_dir"], scale, None)
    text(ax, tail + 0.5 * m["vinf_a"] * scale * g["in_dir"], rf"$v_\infty$ = {fmt(m['vinf_a'])} km/s",
         direction=180, dist=8)
    # the direction key, as in the departure figure: labels to the right of the arrows
    _toward(ax, (AC_KEY[0] + 1.3, AC_KEY[1]) * np.array([RME, RME]), 180.0, 1.3 * RME, "to the Sun")
    _toward(ax, (AC_KEY[0] + 0.55, AC_KEY[1] - 2.4) * np.array([RME, RME]), 90.0, 1.3 * RME,
            "Mercury's motion\naround the Sun")
    ax.set_xlim(AC_XLIM[0] * RME, AC_XLIM[1] * RME)
    ax.set_ylim(AC_YLIM[0] * RME, AC_YLIM[1] * RME)
    # what was drawn: the burn is on the capture circle, against the motion; the path arrives with Mercury's motion
    close_to(float(np.hypot(*pb)), rp, 1e-9, "burn on the capture orbit")
    vb = orbit_velocity(ME, g0["a"], g0["e"], 0.0, rotate=rot)
    back = np.array([math.cos(math.radians(rot - 90.0)), math.sin(math.radians(rot - 90.0))])
    close_to(float(np.dot(vb / np.hypot(*vb), back)), -1.0, 1e-9, "burn against the motion")
    close_to(float(np.hypot(*vb)), m["vp_m"], 1e-9, "periapsis speed of the arrival hyperbola")
    close_to(float(np.dot(g["in_dir"], [0.0, 1.0])), 1.0, 1e-9, "arrives moving with Mercury")
    save_figure(fig, "p24-arrival-capture")


def synodic():
    """Phase angle of Mercury ahead of Earth against time: the required 108 deg comes back once
    every synodic period."""
    m = mercury()
    S = float(synodic_period(ORBIT_DAYS["Earth"], ORBIT_DAYS["Mercury"]))
    rate = 360.0 / ORBIT_DAYS["Mercury"] - 360.0 / ORBIT_DAYS["Earth"]       # deg/day
    t = np.linspace(-20.0, 400.0, 4201)
    ph = (m["phase"] + rate * t) % 360.0
    cuts = np.r_[0, np.where(np.diff(ph) < 0)[0] + 1, len(t)]         # one line per lap of the phase angle
    fig, ax = data_axes(6.5, 4.1)
    for i0, i1 in zip(cuts[:-1], cuts[1:]):
        ax.plot(t[i0:i1], ph[i0:i1], **line_kw(0))
    ax.axhline(m["phase"], **line_kw("boundary"))
    ax.set_xlim(-20, 400)
    ax.set_ylim(0, 432)
    ax.spines["left"].set_bounds(0, 360)
    degree_ticks(ax, "y", 90)
    ax.set_xticks(np.arange(0, 401, 50))
    ax.set_xlabel("Time, days")
    ax.set_ylabel("Phase angle, degrees")
    tw = np.array([k * S for k in range(4)])
    ax.plot(tw, np.full(4, m["phase"]), "o", color=INK, ms=7, mec="white", mew=0.8, zorder=6)
    text(ax, (254.0, m["phase"]), f"required phase\nangle, {fmt(m['phase'], 3)}°", direction=90, dist=5, ha="left",
         fs=FS_SMALL, color=STEEL)
    ym = 388.0                     # above the data: no line of the curve crosses the dimension
    for x in tw[1:3]:
        line(ax, (x, m["phase"]), (x, ym + 8.0), linewidth=0.7)
    dimension(ax, (tw[1], ym), (tw[2], ym), None)
    text(ax, (tw[1] + 0.5 * S, ym), f"$S$ = {fmt(S, 3)} days", direction=90, dist=3)
    callout(ax, (tw[0], m["phase"]), "launch\nopportunity", at=(5.0, 34.0), ha="left")
    # what was drawn: the curve returns to the required angle once every synodic period
    for k in range(4):
        close_to((m["phase"] + rate * tw[k]) % 360.0, m["phase"], 1e-9, f"window {k}")
    close_to(360.0 / rate, S, 1e-9, "one lap of the phase angle is the synodic period")
    save_figure(fig, "p24-synodic")


def make_all():
    _check_deck(mercury())
    three_conics()
    heliocentric_transfer()
    departure_hyperbola()
    vinf_vs_dv()
    speed_vs_distance()
    arrival_capture()
    synodic()


# ===================================================================== printed values
def values():
    m = mercury()
    _check_deck(m)
    P = "p24"
    h = m["h"]
    record(P, "r-earth", fmt_sci(R_EARTH))
    record(P, "r-merc", fmt_sci(R_MERC))
    record(P, "a-t", fmt_sci(h["a_t"], 5))
    record(P, "e-t", fmt(h["e_t"]))
    # the planet and transfer speeds print to five figures everywhere on the page (text and table)
    record(P, "vinf-dep", fmt(m["vinf_d"]))
    record(P, "vinf-arr", fmt(m["vinf_a"]))
    record(P, "rp-earth", fmt(m["rp_e"]))
    record(P, "rp-merc", fmt(m["rp_m"]))
    record(P, "vc-park", fmt(m["vc_e"]))
    record(P, "vp-dep", fmt(m["vp_e"]))
    record(P, "dv-dep", fmt(m["dv_d"]))
    record(P, "vc-cap", fmt(m["vc_m"]))
    record(P, "dv-cap", fmt(m["dv_a"]))
    record(P, "dv-sum", fmt(m["dv_d"] + m["dv_a"]))
    record(P, "tof-days4", fmt(m["tof"], 4))
    # five figures for the operands of the printed subtractions of steps 2, 4 and 5, so that
    # each subtraction reproduces its printed result from the digits shown
    for k in ("v_e", "v_ta", "v_m", "v_tp", "vp_m"):
        record(P, f"{k}-5", fmt(m[k], 5))
    assert fmt(float(fmt(m["v_e"], 5)) - float(fmt(m["v_ta"], 5))) == fmt(m["vinf_d"])
    assert fmt(float(fmt(m["v_tp"], 5)) - float(fmt(m["v_m"], 5))) == fmt(m["vinf_a"])
    assert fmt(float(fmt(m["vp_m"], 5)) - float(fmt(m["vc_m"]))) == fmt(m["dv_a"])
    assert fmt(float(fmt(m["vp_e"])) - float(fmt(m["vc_e"]))) == fmt(m["dv_d"])
    assert fmt(360.0 / ORBIT_DAYS["Mercury"] * float(fmt(m["tof"], 4)), 3) == fmt(m["travel"], 3)
    record(P, "vinf2-dep", fmt(m["vinf_d"] ** 2))
    record(P, "2mu-r-earth", fmt(2.0 * E / m["rp_e"]))
    record(P, "vinf2-arr", fmt(m["vinf_a"] ** 2, 5))      # five figures: their sum's root gives 10.389
    record(P, "2mu-r-merc", fmt(2.0 * ME / m["rp_m"], 5))
    # burning low against escaping first
    record(P, "vesc-park", fmt(m["vesc_e"], 5))             # five figures: 11.021 - 7.793 = 3.228
    record(P, "dv-escape", fmt(m["vesc_e"] - m["vc_e"]))
    record(P, "dv-beyond-escape", fmt(m["dv_d"] - (m["vesc_e"] - m["vc_e"])))
    record(P, "dv-two-step", fmt(m["vesc_e"] - m["vc_e"] + m["vinf_d"]))
    record(P, "vesc-cap", fmt(m["vesc_m"]))
    # hyperbola geometry
    record(P, "e-dep", fmt(m["dep"]["e"]))
    record(P, "thinf-dep", fmt(m["dep"]["theta_inf"]))
    record(P, "e-arr", fmt(m["arr"]["e"], 3))
    record(P, "turn-arr", fmt(m["arr"]["turn"], 2))
    # spheres of influence and the speed at the edge of Earth's
    r_soi = soi("Earth")
    record(P, "soi-earth", fmt(round(r_soi, -3)))
    record(P, "soi-earth-pct", fmt(100.0 * r_soi / R_EARTH, 2))
    record(P, "soi-earth-radii", fmt(r_soi / RE, 3))
    record(P, "soi-merc", fmt(round(soi("Mercury"), -3)))
    record(P, "v-at-soi", fmt(float(periapsis_speed_hyperbola(E, r_soi, m["vinf_d"]))))
    # phase angle and synodic periods
    record(P, "n-merc", fmt(360.0 / ORBIT_DAYS["Mercury"]))
    record(P, "travel", fmt(m["travel"], 3))
    record(P, "phase", fmt(m["phase"], 3))
    record(P, "phase-raw", fmt(180.0 - m["travel"], 3))
    for p in TARGETS:
        s = float(synodic_period(ORBIT_DAYS["Earth"], ORBIT_DAYS[p]))
        record(P, f"syn-{p.lower()}", fmt(s, 3))
        record(P, f"syn-{p.lower()}-yr", fmt(s / ORBIT_DAYS["Earth"], 3))
        record(P, f"T-{p.lower()}", fmt(ORBIT_DAYS[p], 4 if ORBIT_DAYS[p] < 1000 else 5))
    record(P, "T-earth", fmt(ORBIT_DAYS["Earth"], 5))
