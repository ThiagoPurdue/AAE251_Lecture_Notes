"""Figures and values of 2.2 Orbit Transfers (notes/chapter-2/orbit-transfers.md).

Worked examples (all around Earth, constants from orbits.py):
  - Hohmann transfer from a 400 km to a 20,200 km circular orbit.
  - A steep coast arc from the surface (60 deg above the horizontal) to the same high orbit,
    to show why a high orbit is reached through a parking orbit.
  - Circularizing a 350 km by 1,100 km orbit at apoapsis or at periapsis.
  - Phasing: chaser and target in a 7,000 km circular orbit, the chaser 100 s behind.
  - A 30 deg plane change made in the low orbit, at the transfer apogee, or in the high orbit.
Run through the runner: python3 -B scripts/make_chapter_2_figures.py p22
"""
from chapter_2.orbits import *  # noqa: F401,F403

PAGE = "p22"
E, RE = MU["Earth"], RADIUS["Earth"]

# --- the worked examples (inputs)
H1, H2 = 400.0, 20200.0               # Hohmann example, altitudes, km
R1, R2 = RE + H1, RE + H2
GAMMA = 60.0                          # steep coast arc: angle above the horizontal at the ground, deg
CP, CA = 350.0, 1100.0                # circularization example, periapsis and apoapsis altitudes, km
R_PH, LAG = 7000.0, 100.0             # phasing example: circle radius, km; the chaser's lag, s
DI = 30.0                             # plane change of the maneuver-order example, deg
V_LEO = 8.0                           # speed of the cost curve, km/s (the value used in the course slides)
PC_FINAL = (75.0, 45.0, 5.0)          # plane-change figure: "final orbit" label (argument of latitude, direction, pt)
FIG_CIRC = (1000.0, 12000.0)          # orbit drawn in the circularization figure, altitudes, km
CIRC_EL_AT, CIRC_RP_AT, CIRC_RP_TEXT = (0.0, -14500.0), (-5750.0, 9000.0), "circle at $r_p$"   # label places, km


# ===================================================================== computations
def steep_arc(r_top=R2, gamma=GAMMA):
    """Coast arc that leaves the surface at `gamma` deg above the horizontal and reaches r_top at
    its apoapsis. Returns the speed at the ground, the speed at the top, a, e and the true
    anomaly at the ground (deg)."""
    c = math.cos(math.radians(gamma))
    v0 = math.sqrt(2.0 * E * (1.0 / RE - 1.0 / r_top) / (1.0 - (RE * c / r_top) ** 2))
    h = RE * v0 * c
    v_top = h / r_top
    eps = 0.5 * v0 ** 2 - E / RE
    a = -E / (2.0 * eps)
    e = math.sqrt(1.0 + 2.0 * eps * h ** 2 / E ** 2)
    p = h ** 2 / E
    th0 = math.degrees(math.acos((p / RE - 1.0) / e))
    return dict(v0=v0, v_top=v_top, a=a, e=e, p=p, th0=th0)


def circularize(hp=CP, ha=CA):
    rp, ra = RE + hp, RE + ha
    a, e = 0.5 * (rp + ra), eccentricity(rp, ra)
    va, vp = float(vis_viva(E, ra, a)), float(vis_viva(E, rp, a))
    vca, vcp = float(circular_speed(E, ra)), float(circular_speed(E, rp))
    return dict(rp=rp, ra=ra, a=a, e=e, va=va, vp=vp, vca=vca, vcp=vcp, dva=vca - va, dvp=vcp - vp)


def phasing(r=R_PH, lag=LAG):
    T = float(period(E, r))
    v = float(circular_speed(E, r))
    T_ph = T - lag
    a_ph = float(semi_major_axis_from_period(E, T_ph))
    rp = 2.0 * a_ph - r
    v_a = float(vis_viva(E, r, a_ph))
    a_min = 0.5 * (r + RE)                       # perigee on the surface: the largest lag one lap can remove
    return dict(T=T, v=v, T_ph=T_ph, a_ph=a_ph, rp=rp, e=(r - rp) / (r + rp), clear=rp - RE, v_a=v_a,
                dv=v_a - v, lead=360.0 * lag / T, max_lag=T - float(period(E, a_min)))


def printed_total(pc, dv_total):
    """Total of a plan as a student gets it from the printed parts (each to four figures), so
    that the page, the table and the figure agree to the last digit."""
    tot = float(fmt(pc)) + float(fmt(dv_total))
    assert abs(tot - (pc + dv_total)) < 1.5e-3, "rounded total within rounding of the exact total"
    return tot


def maneuver_order():
    h = hohmann(E, R1, R2)
    plans = [("in the low orbit", h["v_c1"]), ("at the transfer apogee", h["v_ta"]), ("in the high orbit", h["v_c2"])]
    out = []
    for name, v in plans:
        pc = float(plane_change(v, DI))
        out.append(dict(name=name, v=v, pc=pc, total=printed_total(pc, h["dv_total"])))
    return h, out


# ===================================================================== figures
def fig_direct_vs_parking():
    """A steep coast arc from the ground against a parking orbit and a Hohmann transfer, to scale."""
    s = steep_arc()
    h = hohmann(E, R1, R2)
    fig, ax = new_axes(6.5, 6.0)
    rot_h = 0.0                                    # transfer periapsis direction, deg
    lam = 242.0                                       # screen angle of the launch site of the steep arc, deg
    rot_s = lam - s["th0"]                           # steep arc: periapsis direction, deg
    draw_orbit(ax, R2, 0.0, "final", label="final orbit", label_at=35, arrows_at=(220,))
    draw_orbit(ax, h["a_t"], h["e_t"], "transfer", rotate=rot_h, theta0=0, theta1=180,
               label="transfer orbit", label_at=120, label_dir=105, arrows_at=(95,))
    draw_orbit(ax, s["a"], s["e"], "other", rotate=rot_s, theta0=s["th0"], theta1=180.0,
               arrows_at=(s["th0"] + 0.6 * (180.0 - s["th0"]),))
    draw_orbit(ax, R1, 0.0, "initial", arrows_at=(130,))
    draw_body(ax, (0, 0), RE, name="Earth")
    site = orbit_point(s["a"], s["e"], s["th0"], rot_s)
    top = orbit_point(s["a"], s["e"], 180.0, rot_s)
    point(ax, site, ms=5)
    point(ax, top, ms=6)
    text(ax, orbit_point(s["a"], s["e"], s["th0"] + 0.35 * (180.0 - s["th0"]), rot_s), "steep coast arc",
         direction=180, dist=8)
    text(ax, top, f"arrives at {fmt(s['v_top'])} km/s", direction=-50, dist=8)
    callout(ax, orbit_point(R1, 0.0, 200.0), "parking orbit", at=(-RE - 0.20 * R2, -0.07 * R2), ha="right", gap=3)
    p1 = orbit_point(h["a_t"], h["e_t"], 0.0, rot_h)
    p2 = orbit_point(h["a_t"], h["e_t"], 180.0, rot_h)
    L1, L2 = burn_lengths([h["dv1"], h["dv2"]])          # burn arrows in proportion to the delta-Vs
    burn(ax, p1, orbit_velocity(E, h["a_t"], h["e_t"], 0.0, rot_h), r"$\Delta V_1$", length=L1, label_dir=0, dist=5)
    burn(ax, p2, orbit_velocity(E, h["a_t"], h["e_t"], 180.0, rot_h), r"$\Delta V_2$", length=L2, label_dir=180,
         dist=5)
    ax.set_xlim(-1.12 * R2, 1.12 * R2)
    ax.set_ylim(-1.16 * R2, 1.06 * R2)
    # checks on what was drawn
    close_to(float(np.hypot(*top)), R2, 1e-6, "steep coast arc tops out on the final orbit")
    close_to(float(np.hypot(*site)), RE, 1e-6, "steep arc starts on the surface")
    close_to(float(flight_path_angle(s["e"], s["th0"])), GAMMA, 1e-6, "steep arc leaves at GAMMA")
    close_to(float(np.hypot(*p2)), R2, 1e-6, "transfer apoapsis on the final orbit")
    close_to(L1 / L2, h["dv1"] / h["dv2"], 1e-12, "burn arrows in proportion to the delta-Vs")
    save_figure(fig, "p22-direct-vs-parking")


def fig_hohmann():
    """Hohmann transfer of the worked example, to scale, with r1, r2 and 2 a_t dimensioned."""
    h = hohmann(E, R1, R2)
    fig, ax = new_axes(6.5, 6.3)
    draw_orbit(ax, R2, 0.0, "final", label="final orbit", label_at=40, arrows_at=(70,))
    draw_orbit(ax, h["a_t"], h["e_t"], "transfer", theta0=0, theta1=180, label="transfer orbit",
               label_at=125, label_dir=110, arrows_at=(90,))
    draw_orbit(ax, R1, 0.0, "initial", arrows_at=(230,))
    draw_body(ax, (0, 0), RE, name="Earth")
    line(ax, (-R2, 0), (R1, 0))                         # apse line of the transfer
    callout(ax, orbit_point(R1, 0.0, 340.0), "initial orbit", at=(1.35 * R1, -0.3 * R1), ha="left", gap=3)
    L1, L2 = burn_lengths([h["dv1"], h["dv2"]])          # burn arrows in proportion to the delta-Vs
    burn(ax, (R1, 0), 90, r"$\Delta V_1$", length=L1, label_dir=0, dist=5)
    burn(ax, (-R2, 0), 270, r"$\Delta V_2$", length=L2, label_dir=180, dist=5)
    g = -0.24 * R2                                     # extension lines start below the burn arrows
    y1, y2 = -0.42 * R2, -0.62 * R2
    dimension(ax, (-R2, g), (0, g), "$r_2$", offset=y1 - g, label_side=-1)
    dimension(ax, (0, g), (R1, g), "$r_1$", offset=y1 - g, label_side=-1)
    dimension(ax, (-R2, g), (R1, g), "$2a_t = r_1 + r_2$", offset=y2 - g, label_side=-1)
    ax.set_xlim(-1.18 * R2, 1.06 * R2)
    ax.set_ylim(-1.06 * R2, 1.06 * R2)
    x, y = orbit_xy(h["a_t"], h["e_t"], theta0=0, theta1=180)
    r = np.hypot(x, y)
    close_to(float(r.min()), R1, 1e-6, "transfer touches the initial circle")
    close_to(float(r.max()), R2, 1e-6, "transfer touches the final circle")
    close_to(float(x.max() - x.min()), 2 * h["a_t"], 1e-6, "major axis drawn is 2 a_t")
    close_to(L1 / L2, h["dv1"] / h["dv2"], 1e-12, "burn arrows in proportion to the delta-Vs")
    save_figure(fig, "p22-hohmann")


def fig_hohmann_speeds():
    """Speed against time through the Hohmann transfer of the worked example."""
    h = hohmann(E, R1, R2)
    tof_h = h["tof"] / 3600.0
    fig, ax = data_axes(6.5, 3.9)
    t_tr = np.linspace(0.0, h["tof"], 400)
    th = true_anomaly_at_time(E, h["a_t"], h["e_t"], t_tr)
    th[-1] = 180.0
    r = conic_radius(h["a_t"] * (1 - h["e_t"] ** 2), h["e_t"], th)
    v_tr = vis_viva(E, r, h["a_t"])
    t0, t1 = -1.0, tof_h + 1.3                         # room for the delta-V 2 label inside the plot
    ax.plot([t0, 0.0], [h["v_c1"]] * 2, **line_kw("initial"))
    ax.plot(t_tr / 3600.0, v_tr, **line_kw("transfer"))
    ax.plot([tof_h, t1], [h["v_c2"]] * 2, **line_kw("final"))
    arrow(ax, (0.0, h["v_c1"]), (0.0, h["v_tp"]))
    arrow(ax, (tof_h, h["v_ta"]), (tof_h, h["v_c2"]))
    ax.plot([0.0, tof_h], [h["v_c1"], h["v_ta"]], "o", color=INK, ms=5, zorder=8)
    text(ax, (0.0, h["v_tp"]), rf"$\Delta V_1$ = {fmt(h['dv1'])} km/s", direction=40, dist=12)
    text(ax, (tof_h, 0.5 * (h["v_ta"] + h["v_c2"])), rf"$\Delta V_2$ = {fmt(h['dv2'])} km/s", direction=0,
         dist=9, va="top", offset=(0.0, 5.0))           # below the final-orbit line, clear of the arrowhead
    text(ax, (-0.5, h["v_c1"]), "initial orbit", direction=-90, dist=5, color=text_color("initial"))
    text(ax, (tof_h + 0.3, h["v_c2"]), "final orbit", direction=90, dist=5, color=text_color("final"))
    k = int(0.42 * len(t_tr))
    text(ax, (t_tr[k] / 3600.0, v_tr[k]), "transfer orbit", direction=45, dist=6, color=text_color("transfer"))
    ax.set_xlim(t0, t1)
    ax.set_ylim(0, 12)
    ax.set_xlabel("Time after the first burn, hours")
    ax.set_ylabel("Speed, km/s")
    close_to(float(v_tr[0]), h["v_tp"], 1e-9, "transfer starts at its periapsis speed")
    close_to(float(v_tr[-1]), h["v_ta"], 1e-6, "transfer ends at its apoapsis speed")
    assert np.all(np.diff(v_tr) < 0), "the spacecraft slows all the way out"
    close_to(float(v_tr[0] - h["v_c1"]), h["dv1"], 1e-9, "first jump is dv1")
    save_figure(fig, "p22-hohmann-speeds")


def fig_circularize():
    """An elliptical orbit with the two circles a single burn can give, to scale."""
    hp, ha = FIG_CIRC
    rp, ra = RE + hp, RE + ha
    a, e = 0.5 * (rp + ra), eccentricity(rp, ra)
    fig, ax = new_axes(6.5, 5.0)
    line(ax, (-ra, 0), (rp, 0))
    # both circles a single burn can reach are final orbits: same style, told apart by their labels
    draw_orbit(ax, ra, 0.0, "final", label=r"circle at $r_a$", label_at=50, arrows_at=(120,))
    draw_orbit(ax, rp, 0.0, "final", arrows_at=(250,))
    draw_orbit(ax, a, e, "initial", arrows_at=(235,))
    draw_body(ax, (0, 0), RE, name="Earth")
    text(ax, CIRC_EL_AT, "elliptical orbit", color=text_color("initial"))      # between the ellipse and the r_a circle
    text(ax, CIRC_RP_AT, CIRC_RP_TEXT, color=text_color("final"))              # between the r_p circle and the ellipse
    va, vca = float(vis_viva(E, ra, a)), float(circular_speed(E, ra))
    vp, vcp = float(vis_viva(E, rp, a)), float(circular_speed(E, rp))
    La, Lp = burn_lengths([vca - va, vp - vcp])              # burn arrows in proportion to the delta-Vs
    tip_a = burn(ax, (-ra, 0), 270, "speed\nup", length=La, label_dir=180, dist=4)
    tip_p = burn(ax, (rp, 0), 270, "slow\ndown", length=Lp, label_dir=0, dist=4)
    text(ax, (-ra, 0), "apoapsis", direction=135, dist=8, fs=FS_SMALL)
    text(ax, (rp, 0), "periapsis", direction=45, dist=8, fs=FS_SMALL)
    ax.set_xlim(-1.32 * ra, 1.25 * ra)
    ax.set_ylim(-1.08 * ra, 1.1 * ra)
    x, y = orbit_xy(a, e)
    r = np.hypot(x, y)
    close_to(float(r.min()), rp, 1e-6, "ellipse touches the inner circle at periapsis")
    close_to(float(r.max()), ra, 1e-6, "ellipse touches the outer circle at apoapsis")
    assert vca > va and vcp < vp, "speed up at apoapsis, slow down at periapsis"
    close_to(La / Lp, (vca - va) / (vp - vcp), 1e-12, "burn arrows in proportion to the delta-Vs")
    save_figure(fig, "p22-circularize")


def fig_phasing():
    """Phasing orbit of the chaser: the full view to scale and a detail near perigee, to scale."""
    p = phasing()
    # the detail on the left, next to the box it magnifies, so the two connector lines stay short
    fig, (az, ax) = new_axes(7.0, 4.1, ncols=2, gridspec_kw=dict(width_ratios=[1.0, 1.25], wspace=0.14))
    # full view
    draw_orbit(ax, R_PH, 0.0, "initial", label="circular orbit", label_at=58, arrows_at=(110,))
    draw_orbit(ax, p["a_ph"], p["e"], "transfer", rotate=180.0, arrows_at=(250,))
    draw_body(ax, (0, 0), RE, name="Earth")
    callout(ax, orbit_point(p["a_ph"], p["e"], 40.0, 180.0), "phasing orbit", at=(-0.95 * R_PH, -1.22 * R_PH),
            ha="center")
    tgt = orbit_point(R_PH, 0.0, p["lead"])
    point(ax, (R_PH, 0.0), ms=6)
    point(ax, tgt, kind="open", ms=7)
    text(ax, tgt, "target", direction=60, dist=7)
    text(ax, (R_PH, 0.0), "chaser", direction=0, dist=10)
    burn(ax, (R_PH, 0.0), 270, r"$\Delta V$", label_dir=0, dist=4, length=26)
    # the zoom box
    zx0, zx1, zy0, zy1 = -7150.0, -6050.0, -550.0, 550.0
    box = ax.plot([zx0, zx1, zx1, zx0, zx0], [zy0, zy0, zy1, zy1, zy0], color=INK, lw=LW_THIN, zorder=9)[0]
    text(ax, (zx0, 0.0), "detail", direction=180, dist=5, fs=FS_SMALL)
    ax.set_xlim(-1.3 * R_PH, 1.5 * R_PH)
    ax.set_ylim(-1.32 * R_PH, 1.25 * R_PH)
    # detail near perigee, same orientation, to scale
    th = np.radians(np.linspace(170, 190, 200))
    az.add_patch(Circle((0, 0), RE, fc=BODY_FILL["Earth"], ec=INK, lw=1.0, zorder=5))
    draw_orbit(az, R_PH, 0.0, "initial", arrows_at=(185.5,))
    draw_orbit(az, p["a_ph"], p["e"], "transfer", rotate=180.0, arrows_at=(4.5,))
    peri = np.array([-p["rp"], 0.0])
    # the perigee altitude, measured at the perigee: from the dot to Earth's surface
    grp = dimension(az, (-RE, 0.0), peri, None, ticks=False)
    point(az, peri, ms=5, gid=grp, zorder=9)
    text(az, 0.5 * (peri + np.array([-RE, 0.0])), f"{fmt(p['clear'])} km", direction=90, dist=4, fs=FS_SMALL)
    text(az, peri, "perigee", direction=-60, dist=7, fs=FS_SMALL)
    # how far the perigee drops below the circle (the text's 161 km)
    yd = -330.0
    xc = -math.sqrt(R_PH ** 2 - yd ** 2)
    th_d = 180.0 - math.degrees(math.atan2(-yd, p["rp"]))       # true anomaly (rotate 180) near the same height
    xo = float(orbit_point(p["a_ph"], p["e"], 180.0 - th_d, 180.0)[0])
    dimension(az, (xc, yd), (xo, yd), None, ticks=False)
    text(az, (xo, yd), f"{fmt(R_PH - p['rp'], 3)} km", direction=0, dist=6, fs=FS_SMALL)
    text(az, (-6200.0, 400.0), "Earth", backing=False)
    az.set_xlim(zx0, zx1)
    az.set_ylim(zy0, zy1)
    frame = az.plot([zx0, zx1, zx1, zx0, zx0], [zy0, zy0, zy1, zy1, zy0], color=INK, lw=LW_THIN, zorder=9,
                    clip_on=False)[0]
    from matplotlib.patches import ConnectionPatch
    for yy in (zy0, zy1):                       # connector lines from the box to the detail, as in p24-three-conics
        connects(ax.add_patch(ConnectionPatch(xyA=(zx0, yy), coordsA=ax.transData, xyB=(zx1, yy), coordsB=az.transData,
                                              color=GRAY, lw=0.6, zorder=0.5, clip_on=False)), box, frame)
    # checks
    close_to(float(period(E, p["a_ph"])), p["T"] - LAG, 1e-6, "phasing period is T minus the lag")
    x, y = orbit_xy(p["a_ph"], p["e"], rotate=180.0)
    r = np.hypot(x, y)
    close_to(float(r.max()), R_PH, 1e-6, "phasing apogee on the circle at the burn point")
    close_to(float(r.min()), p["rp"], 1e-6, "perigee radius drawn")
    assert p["rp"] > RE, "the phasing orbit clears the surface"
    close_to(float(np.degrees(np.arctan2(tgt[1], tgt[0]))), p["lead"], 1e-9, "target lead angle")
    save_figure(fig, "p22-phasing")


def fig_plane_change():
    """Two circular orbits of the same radius whose planes differ by DI, crossing at the line of
    nodes, and the velocity triangle of the burn there."""
    fig, (ax, at) = new_axes(7.0, 3.9, ncols=2, gridspec_kw=dict(width_ratios=[1.35, 1.0], wspace=0.05))
    g = Globe(ax, view_lat=22, view_lon=-40)                          # the chapter's globe: equator and axis
    g.axis(1.32)
    r = 1.45
    g.circle(r, 0.0, 0.0, role="initial", arrows_at=(330,))
    g.circle(r, DI, 0.0, role="final", arrows_at=(235,))
    node = g.orbit_vec(r, 0.0, 0.0, 0.0)
    anti = g.orbit_vec(r, 0.0, 0.0, 180.0)
    sl = np.linspace(0.0, 1.0, 400)
    g.curve(1.12 * (np.outer(anti, 1 - sl) + np.outer(node, sl)), hidden="dashed", color=GRAY, lw=LW_THIN)
    v1 = g.orbit_vec(1.0, 0.0, 0.0, 90.0)
    v2 = g.orbit_vec(1.0, DI, 0.0, 90.0)
    g.point(node, ms=6)
    g.callout(node * 1.12, "line of nodes", at=(1.05, -1.32))
    g.text(g.orbit_vec(r, 0.0, 0.0, 180.0 - 40.0 + 90.0), "initial orbit", direction=180, dist=8, color=text_color("initial"))
    g.text(g.orbit_vec(r, DI, 0.0, PC_FINAL[0]), "final orbit", direction=PC_FINAL[1], dist=PC_FINAL[2],
           color=text_color("final"))
    ax.set_xlim(-2.45, 1.75)
    ax.set_ylim(-1.55, 1.45)
    # velocity triangle, true shape: v1 and v2 of equal length, angle DI between them
    L = 2.6
    o = np.array([0.0, 0.0])
    b = math.radians(-DI / 2.0)
    d1 = np.array([math.cos(b), math.sin(b)])
    d2 = np.array([math.cos(b + math.radians(DI)), math.sin(b + math.radians(DI))])
    t1, t2 = o + L * d1, o + L * d2
    arrow(at, o, t1, color=BLUE)
    arrow(at, o, t2, color=text_color("final"))
    arrow(at, t1, t2)
    mid = 0.5 * (t1 + t2)
    angle_arc(at, o, 0.9, math.degrees(b), math.degrees(b) + DI, r"$\Delta i$", dist=3)
    text(at, t1, r"$\mathbf{v}_1$", direction=-30, dist=4, color=BLUE)
    text(at, t2, r"$\mathbf{v}_2$", direction=30, dist=4, color=text_color("final"))
    text(at, mid, r"$\Delta \mathbf{V}$", direction=0, dist=6)
    text(at, 0.55 * t1, r"$v$", direction=-90, dist=6)
    text(at, 0.55 * t2, r"$v$", direction=90, dist=6)
    at.set_xlim(-0.35, 3.4)
    at.set_ylim(-1.55, 1.45)
    close_to(float(np.degrees(np.arccos(np.dot(v1, v2)))), DI, 1e-9, "orbit planes differ by DI at the node")
    close_to(float(np.hypot(*(t2 - t1))), float(plane_change(L, DI)), 1e-9, "triangle side is 2 v sin(di/2)")
    save_figure(fig, "p22-plane-change")


def fig_plane_change_cost():
    """Delta-V of a plane change against the angle, at 8 km/s and at the high-orbit speed."""
    h = hohmann(E, R1, R2)
    di = np.linspace(0.0, 180.0, 361)
    fig, ax = data_axes(6.5, 4.0)
    c8 = plane_change(V_LEO, di)
    ch = plane_change(h["v_c2"], di)
    ax.plot(di, c8, **line_kw(0))
    ax.plot(di, ch, **line_kw(1))
    label_curve(ax, di, c8, 100.0, f"$v$ = {fmt(V_LEO, 2)} km/s", 0, offset=(-6, 10), ha="right", va="bottom")
    label_curve(ax, di, ch, 150.0, f"$v$ = {fmt(h['v_c2'])} km/s", 1, offset=(0, 13))
    x60 = 60.0
    ax.plot([x60], [float(plane_change(V_LEO, x60))], "o", color=INK, ms=6, zorder=8)
    text(ax, (x60, float(plane_change(V_LEO, x60))), r"60°: $\Delta V = v$", direction=-30, dist=8)
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 17)
    degree_ticks(ax, "x", 30)
    ax.set_xlabel(r"Plane change angle $\Delta i$, degrees")
    ax.set_ylabel(r"$\Delta V$, km/s")
    close_to(float(plane_change(V_LEO, 60.0)), V_LEO, 1e-9, "60 deg costs the orbital speed")
    close_to(float(c8[-1]), 2 * V_LEO, 1e-9, "180 deg costs twice the speed")
    assert np.all(np.diff(c8) > 0), "cost grows with the angle"
    save_figure(fig, "p22-plane-change-cost")


def fig_maneuver_order():
    """Total delta-V of the three plans: Hohmann burns plus the plane change, stacked."""
    h, plans = maneuver_order()
    fig, ax = data_axes(6.5, 3.4)
    ax.grid(False, axis="y")
    names = ["plane change\nin the low orbit", "plane change at\nthe transfer apogee", "plane change\nin the high orbit"]
    n = len(plans)
    hoh = [h["dv_total"]] * n
    pcs = [p["pc"] for p in plans]
    bars(ax, names, hoh, styles=[0] * n, value_text=[""] * n, horizontal=True)      # data series
    bars(ax, names, pcs, styles=[1] * n, bottoms=hoh, horizontal=True,
         value_text=[f"{fmt(p['total'])} km/s" for p in plans])
    ax.invert_yaxis()
    text(ax, (0.5 * h["dv_total"], -0.5), "Hohmann burns", direction=90, dist=2, color=text_color(0))
    text(ax, (h["dv_total"] + 0.5 * pcs[0], -0.5), "plane change", direction=90, dist=2,
         color=text_color(1))
    ax.set_xlim(0, 9)
    ax.set_ylim(2.5, -1.05)
    ax.set_xlabel(r"Total $\Delta V$, km/s")
    ax.tick_params(axis="y", length=0)
    best = min(plans, key=lambda q: q["total"])
    assert best["name"] == "at the transfer apogee", "the slowest point is cheapest"
    for p in plans:
        close_to(p["pc"], float(plane_change(p["v"], DI)), 1e-12, "segment length is 2 v sin(di/2)")
    save_figure(fig, "p22-maneuver-order")


def make_all():
    fig_direct_vs_parking()
    fig_hohmann()
    fig_hohmann_speeds()
    fig_circularize()
    fig_phasing()
    fig_plane_change()
    fig_plane_change_cost()
    fig_maneuver_order()


# ===================================================================== printed values
def values():
    R = lambda k, t: record(PAGE, k, t)  # noqa: E731
    h = hohmann(E, R1, R2)
    R("h-r1", fmt(R1, 4)); R("h-r2", fmt(R2, 5)); R("h-at", fmt(h["a_t"], 5)); R("h-et", fmt(h["e_t"]))
    R("h-vc1", fmt(h["v_c1"])); R("h-vtp", fmt(h["v_tp"])); R("h-dv1", fmt(h["dv1"]))
    R("h-vta", fmt(h["v_ta"])); R("h-vc2", fmt(h["v_c2"])); R("h-dv2", fmt(h["dv2"]))
    R("h-dvt", fmt(h["dv_total"])); R("h-Tt", fmt(h["T_t"])); R("h-tof-s", fmt(h["tof"]))
    R("h-tof-h", fmt(h["tof"] / 3600.0)); R("h-tof-min", fmt(h["tof"] / 60.0))
    R("h-sum", fmt(R1 + R2, 5))
    s = steep_arc()
    R("s-v0", fmt(s["v0"])); R("s-vtop", fmt(s["v_top"])); R("s-burn", fmt(h["v_c2"] - s["v_top"]))
    c = circularize()
    R("c-rp", fmt(c["rp"])); R("c-ra", fmt(c["ra"])); R("c-a", fmt(c["a"])); R("c-e", fmt(c["e"]))
    # five decimals for the speeds: each burn is a difference of close speeds
    R("c-va", fmt_dec(c["va"], 5)); R("c-vca", fmt_dec(c["vca"], 5)); R("c-dva", fmt(c["dva"]))
    R("c-vp", fmt_dec(c["vp"], 5)); R("c-vcp", fmt_dec(c["vcp"], 5)); R("c-dvp", fmt(abs(c["dvp"])))
    p = phasing()
    R("p-v", fmt_dec(p["v"], 5)); R("p-T", fmt_dec(p["T"], 1)); R("p-Tmin", fmt(p["T"] / 60.0))
    R("p-lead", fmt(p["lead"], 3)); R("p-Tph", fmt_dec(p["T_ph"], 1)); R("p-Tphmin", fmt(p["T_ph"] / 60.0))
    R("p-aph", fmt_dec(p["a_ph"], 1)); R("p-rp", fmt_dec(p["rp"], 1)); R("p-clear", fmt(p["clear"]))
    R("p-e", fmt(p["e"], 3)); R("p-va", fmt_dec(p["v_a"], 5)); R("p-dv-kms", fmt(abs(p["dv"])))
    R("p-dv-ms", fmt(abs(p["dv"]) * 1000.0)); R("p-dv2-ms", fmt(2 * abs(p["dv"]) * 1000.0))
    R("p-maxlag", fmt(p["max_lag"], 3)); R("p-maxlag-min", fmt(p["max_lag"] / 60.0, 2))
    R("p-gap", fmt(R_PH - p["rp"], 3))
    _, plans = maneuver_order()
    for key, q in zip(("low", "apo", "high"), plans):
        R(f"m-pc-{key}", fmt(q["pc"])); R(f"m-tot-{key}", fmt(q["total"]))
    R("m-save", fmt(plans[0]["total"] - plans[1]["total"]))
    R("m-sin15", fmt(math.sin(math.radians(DI / 2.0)), 5))  # five figures: 2(7.669)(0.25882) = 3.970
    R("pc-180-hi", fmt(2 * float(fmt(h["v_c2"]))))             # twice the printed 3.873
    R("pc-8-30", fmt(plane_change(V_LEO, 30.0))); R("pc-8-1", fmt(plane_change(V_LEO, 1.0)))
    R("mu", fmt_sci(E)); R("RE", fmt(RE))
    R("warn-v", fmt(math.sqrt(E / H1), 3)); R("deg-rad", fmt(180.0 / math.pi, 3))
    R("c-dva-ms", fmt(c["dva"] * 1000.0)); R("c-dvp-ms", fmt(abs(c["dvp"]) * 1000.0))
    R("fig-circ-hp", fmt(FIG_CIRC[0])); R("fig-circ-ha", fmt(FIG_CIRC[1], 5))      # the orbit of the figure
