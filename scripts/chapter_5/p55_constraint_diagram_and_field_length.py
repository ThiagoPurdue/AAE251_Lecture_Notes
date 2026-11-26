"""Figures and values of Constraint diagram and field length
(notes/chapter-5/constraint-diagram-and-field-length.md; no course standard assessed).

Every number is for the light twin-jet of `vehicles.py` (LIGHT_TWIN, LIGHT_TWIN_REQ): mass 4,500 kg,
wing area 18 m^2, two engines of 6,000 N, C_L,max 1.90 with takeoff flaps and 2.15 with landing
flaps, braking friction 0.40, polar C_D,0 = 0.022 with AR = 8 and e = 0.8, thrust lapse exponent
0.8, and its six requirements. Densities come from the book's standard atmosphere (page 1.4).

Figures, each with its lesson:
  p55-takeoff-landing-phases     each maneuver is a ground roll plus an air distance over an obstacle,
                                 and first sizing looks at the ground roll
  p55-ground-roll-forces         on takeoff the thrust speeds the aircraft up against the drag and the
                                 friction on the weight the wing does not yet carry; on landing the
                                 brakes act through that same wheel load
  p55-constraint-build           each requirement removes part of the plane; what is left is the region
                                 of designs that meet them all
  p55-constraint-diagram         the design point is the highest wing loading the limits allow and the
                                 lowest thrust-to-weight ratio above every line
  p55-field-length-sensitivity   both ground rolls grow in proportion to the wing loading, and more
                                 thrust shortens only the takeoff
"""
from matplotlib.patches import Polygon, Rectangle

from chapter_5.common import *

PAGE = "p55"

A, Q = LIGHT_TWIN, LIGHT_TWIN_REQ
REQ_NAMES = ("stall", "landing", "takeoff", "climb", "cruise", "ceiling")   # the order of the page
TEXT_VERMILION = "#B34E00"
K_LO, K_TD = 1.2, 1.3          # liftoff and touchdown speeds over the stall speed (Anderson 2016, Chapter 6)
# obstacle heights in ft (14 CFR 25.113 for takeoff, 25.125 for landing), with the significant figures
# of their meter values as the page prints them (10.7 m, 15 m)
OBSTACLE_FT = dict(takeoff=(35.0, 3), landing=(50.0, 2))
FT = 0.3048                    # m per ft
# The ceiling line carries open x marks along it, so it differs from the dash-dot landing line and from
# the climb line it lies on by a marker, not only by its dash (FIGURE_STANDARD point 16).
CEILING_MARKS = dict(marker="x", markevery=(0.035, 0.085), ms=6.0, mew=1.3)


def _num(s):
    return float(s.replace(",", "").replace("−", "-"))


def _obstacle_label(k):
    """'obstacle,\\n35 ft (10.7 m)' from OBSTACLE_FT: the regulation's height in feet and in meters."""
    ft, sig = OBSTACLE_FT[k]
    return f"obstacle,\n{fmt(ft, 2)} ft ({fmt(ft * FT, sig)} m)"


def _ceiling_kw(**over):
    """The ceiling's constraint look with its x marks (used in both constraint figures)."""
    kw = constraint_kw("ceiling", **CEILING_MARKS)
    kw.update(over)
    return kw


# ===================================================================== the constraint lines
def _lines(WS):
    """T/W (sea-level static, all engines) that each of the four thrust requirements needs at wing
    loading WS. Climb at sea level; cruise and ceiling with the lapse (rho/rho_0)^m_ad."""
    rho_cr, rho_ce = standard(Q["h_cruise"])[2], standard(Q["h_ceiling"])[2]
    return dict(
        takeoff=tw_takeoff_line(WS, Q["s_LO"], A["CLmax_TO"]),
        climb=tw_climb_line(WS, Q["RC"], Q["V_climb"], A["CD0"], A["K"], m_ad=A["m_ad"]),
        cruise=tw_cruise_line(WS, Q["V_cruise"], A["CD0"], A["K"], rho_cr, m_ad=A["m_ad"]),
        ceiling=tw_ceiling_line(WS, Q["RC_ceiling"], A["CD0"], A["K"], rho_ce, m_ad=A["m_ad"]))


def _limits():
    WS_stall = 0.5 * RHO_SL * Q["V_stall"] ** 2 * A["CLmax_L"]
    WS_land = Q["s_L"] * G0 * RHO_SL * A["CLmax_L"] * A["mu_r"] / K_TD ** 2
    return WS_stall, WS_land


def _design():
    WS_stall, WS_land = _limits()
    ws = min(WS_stall, WS_land)
    at = {k: float(v[0]) for k, v in _lines(np.array([ws])).items()}
    tw = max(at.values())
    # the design point as the page prints it: the wing loading to five figures (2,786.5 N/m²), and the
    # takeoff line there to four, so a figure label and the worked step show the same digits
    ws_label = fmt(ws, 5)
    tw_label = fmt(float(tw_takeoff_line(_num(ws_label), Q["s_LO"], A["CLmax_TO"])), 4)
    return dict(WS_stall=WS_stall, WS_land=WS_land, ws=ws, tw=tw, at=at, active=max(at, key=at.get),
                ws_label=ws_label, tw_label=tw_label)


def _own_point():
    """The light twin-jet's own wing and engines: W/S and T/W."""
    W = weight(A)
    return W / A["S"], A["n"] * A["T0"] / W


# ===================================================================== aircraft on its wheels
def _aircraft_on_gear(ax, contact, length, pitch_deg=0.0, zorder=3.0, fill=PART_FILL):
    """The Boeing 737-800 side outline with its landing gear, facing right, scaled to `length` data
    units and pitched nose-up by pitch_deg about the bottom of the main wheel, which sits at `contact`.
    Returns dict(cg, main_contact, engine, patches)."""
    parts = aircraft_side(B738, detail=False, ground=False)
    keep = ("fuselage", "wing", "winglet", "nacelle", "exhaust_nozzle", "exhaust_plug", "htail", "vtail",
            "nose_gear", "nose_wheel", "main_gear", "main_wheel")
    xs = np.concatenate([parts[k].xy[:, 0] for k in keep])
    L_raw = float(xs.max() - xs.min())
    s = length / L_raw
    ref = np.array([B738["main_gear_x"], 0.0])        # bottom of the main wheel (z up from the ground)
    c = np.asarray(contact, float)

    def place(xy):
        xy = (np.asarray(xy, float) - ref) * s
        xy[:, 0] = -xy[:, 0]                          # face right
        return rotate_xy(xy, pitch_deg) + c

    patches = {}
    for k in sorted(keep, key=lambda n: parts[n].z):
        pa = Polygon(place(parts[k].xy), closed=True, fc=fill, ec=INK, lw=LW_OUTLINE * 0.75,
                     joinstyle="round", zorder=zorder + 0.01 * parts[k].z)
        ax.add_patch(opaque(pa))
        patches[k] = pa
    fz = parts["fuselage"].xy[:, 1]
    cg_raw = np.array([xs.min() + 0.44 * L_raw, fz.min() + 0.45 * (fz.max() - fz.min())])
    eng = parts["nacelle"].xy.mean(axis=0)
    return dict(cg=place([cg_raw])[0], main_contact=c, engine=place([eng])[0], patches=patches)


def _ground(ax, x0, x1, y=0.0, depth=0.07, zorder=1.4):
    """A ground line with a light hatch below it."""
    g = ax.plot([x0, x1], [y, y], color=INK, lw=1.2, zorder=zorder + 0.1, solid_capstyle="butt")[0]
    band = Rectangle((x0, y - depth), x1 - x0, depth, fc="white", ec=GRAY, lw=0.0, zorder=zorder, hatch="////")
    ax.add_patch(band)
    return g


# ===================================================================== figures
def fig_takeoff_landing_phases():
    """Lesson: each maneuver is a ground roll plus an air distance over an obstacle, and first sizing
    looks at the ground roll."""
    xlim, ylim = (-0.35, 10.35), (-0.95, 1.55)
    fig, axs = new_axes(6.5, 2 * 6.5 * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0]) + 0.1, nrows=2, equal=True)
    fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0, hspace=0.04)
    AC = 1.30                     # outline length, data units (enlarged)
    H_TO, H_L = 0.62, 0.88        # drawn obstacle heights (35 ft and 50 ft), exaggerated
    yd = -0.45

    # ---- panel 1: takeoff
    ax = axs[0]
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    text(ax, (xlim[0] + 0.05, 1.40), "1  takeoff", fs=FS_LABEL, ha="left", backing=False)
    x_br, x_lo, x_ob = 0.75, 6.0, 8.65
    gl = _ground(ax, xlim[0] + 0.05, xlim[1] - 0.05)
    gam = math.radians(16.0)                       # drawn climb angle, exaggerated
    # circular transition from the ground, then a straight climb that reaches H_TO at the obstacle
    R = (H_TO - (x_ob - x_lo) * math.tan(gam)) / ((1 - math.cos(gam)) - math.sin(gam) * math.tan(gam))
    th = np.linspace(0.0, gam, 30)
    xa, ya = x_lo + R * np.sin(th), R * (1 - np.cos(th))
    xb = np.linspace(xa[-1], x_ob + 0.9, 20)
    yb = ya[-1] + (xb - xa[-1]) * math.tan(gam)
    # the path on the runway from brake release to liftoff, drawn thick as on the landing panel
    xg1 = np.linspace(x_br, x_lo, 10)
    xp, yp = np.r_[xg1, xa[1:], xb[1:]], np.r_[np.zeros(10), ya[1:], yb[1:]]
    ln = ax.plot(xp, yp, color=INK, lw=LW_MAIN, zorder=4)[0]
    for h in motion_heads(ax, xg1, np.zeros_like(xg1), (0.5,), line=ln):   # one head on the ground roll,
        rides_on(h, ln, gl)                                                # which runs on the ground line
    motion_heads(ax, np.r_[xa, xb[1:]], np.r_[ya, yb[1:]], (0.55,), line=ln)
    y_at_ob = float(np.interp(x_ob, xb, yb))
    close_to(y_at_ob, H_TO, 1e-9, "the drawn path clears the takeoff obstacle at its height")
    close_to(float(np.max(np.abs(yp[xp <= x_lo]))), 0.0, 1e-12, "the takeoff path runs on the runway up to liftoff")
    ax.plot([x_ob, x_ob], [0.0, H_TO], color=STEEL, lw=2.4, solid_capstyle="butt", zorder=3)
    text(ax, (x_ob, 0.5 * H_TO), _obstacle_label("takeoff"), direction=0, dist=6, fs=FS_SMALL, ha="left")
    _aircraft_on_gear(ax, (x_br, 0.0), AC, 0.0)
    _aircraft_on_gear(ax, (x_lo, 0.0), AC, 7.0)
    _aircraft_on_gear(ax, (x_ob + 0.42, y_at_ob + 0.42 * math.tan(gam) + 0.02), AC, math.degrees(gam))
    text(ax, (x_br + 0.05, 0.78), "brake release,\n$V$ = 0", fs=FS_LABEL)
    text(ax, (x_lo - 0.3, 0.86), f"liftoff, $V_{{\\mathrm{{LO}}}}$ = {fmt_dec(K_LO, 1)} $V_{{\\mathrm{{stall}}}}$",
         fs=FS_LABEL)
    dimension(ax, (x_br, yd), (x_lo, yd), None)
    text(ax, (0.5 * (x_br + x_lo), yd), "ground roll, $s_{\\mathrm{LO}}$", direction=-90, dist=4, fs=FS_LABEL)
    dimension(ax, (x_lo, yd), (x_ob, yd), None)
    text(ax, (0.5 * (x_lo + x_ob), yd), "air distance", direction=-90, dist=4, fs=FS_SMALL)
    for x in (x_br, x_lo, x_ob):
        ax.plot([x, x], [-0.09, yd - 0.06], color=INK, lw=LW_THIN, zorder=2)

    # ---- panel 2: landing
    ax = axs[1]
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    text(ax, (xlim[0] + 0.05, 1.40), "2  landing", fs=FS_LABEL, ha="left", backing=False)
    x_ob2, x_td, x_st = 1.25, 4.3, 9.35
    gl = _ground(ax, xlim[0] + 0.05, xlim[1] - 0.05)
    ga = math.radians(18.0)                        # drawn approach angle, exaggerated
    # straight approach from above the obstacle, then a circular flare that meets the ground at touchdown
    R2 = (H_L - (x_td - x_ob2) * math.tan(ga)) / ((1 - math.cos(ga)) - math.sin(ga) * math.tan(ga))
    th = np.linspace(ga, 0.0, 30)
    xf, yf = x_td - R2 * np.sin(th), R2 * (1 - np.cos(th))
    xs_ = np.linspace(x_ob2 - 0.9, xf[0], 20)
    ys_ = yf[0] + (xf[0] - xs_) * math.tan(ga)
    xg = np.linspace(x_td, x_st, 10)
    xp, yp = np.r_[xs_, xf[1:]], np.r_[ys_, yf[1:]]
    ln = ax.plot(np.r_[xp, xg[1:]], np.r_[yp, np.zeros(9)], color=INK, lw=LW_MAIN, zorder=4)[0]
    motion_heads(ax, xp, yp, (0.12, 0.62), line=ln)
    for h in motion_heads(ax, xg, np.zeros_like(xg), (0.5,), line=ln):     # one head on the ground roll,
        rides_on(h, ln, gl)                                                # as on takeoff
    close_to(float(np.interp(x_ob2, xs_, ys_)), H_L, 1e-9, "the drawn approach passes the landing obstacle at its height")
    ax.plot([x_ob2, x_ob2], [0.0, H_L], color=STEEL, lw=2.4, solid_capstyle="butt", zorder=3)
    text(ax, (x_ob2, 0.5 * H_L), _obstacle_label("landing"), direction=180, dist=6, fs=FS_SMALL, ha="right")
    _aircraft_on_gear(ax, (x_td, 0.0), AC, 5.0)
    _aircraft_on_gear(ax, (x_st - 0.02, 0.0), AC, 0.0)
    text(ax, (x_td + 0.45, 0.78), f"touchdown, $V_T$ = {fmt_dec(K_TD, 1)} $V_{{\\mathrm{{stall}}}}$", fs=FS_LABEL)
    text(ax, (x_st - 0.1, 0.78), "stop, $V$ = 0", fs=FS_LABEL)
    dimension(ax, (x_ob2, yd), (x_td, yd), None)
    text(ax, (0.5 * (x_ob2 + x_td), yd), "air distance", direction=-90, dist=4, fs=FS_SMALL)
    dimension(ax, (x_td, yd), (x_st, yd), None)
    text(ax, (0.5 * (x_td + x_st), yd), "ground roll, $s_L$", direction=-90, dist=4, fs=FS_LABEL)
    for x in (x_ob2, x_td, x_st):
        ax.plot([x, x], [-0.09, yd - 0.06], color=INK, lw=LW_THIN, zorder=2)
    save_figure(fig, "p55-takeoff-landing-phases")


def fig_ground_roll_forces():
    """Lesson: on takeoff the thrust speeds the aircraft up against the drag and the friction on the
    weight the wing does not yet carry; on landing the brakes act through that same wheel load.
    The aircraft is drawn as a free body: the runway is replaced by the wheel load and the friction
    at the main wheels. Arrow lengths show directions and the vertical balance only (not to scale)."""
    xlim, ylim = (-3.45, 3.55), (-1.95, 1.55)
    fig, axs = new_axes(6.5, 2 * 6.5 * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0]) + 0.1, nrows=2, equal=True)
    fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0, hspace=0.04)
    W_LEN, AC, Y0 = 1.35, 4.6, -0.42
    cases = (
        ("1  takeoff roll: the net force points forward", dict(T=0.44, D=0.10, L=0.50, mu=0.06)),
        ("2  landing roll, engines at idle and spoilers up: the net force points backward", dict(T=0.0, D=0.14, L=0.34, mu=0.40)),
    )
    for ax, (title, f) in zip(axs, cases):
        ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
        text(ax, (xlim[0] + 0.05, ylim[1] - 0.12), title, fs=FS_LABEL, ha="left", backing=False)
        ac = _aircraft_on_gear(ax, (0.30, Y0), AC, 0.0)
        cg, mc = ac["cg"], ac["main_contact"]
        cg_symbol(ax, cg, size=9.0)
        L = f["L"] * W_LEN
        N = W_LEN - L                                    # wheel load W - L (drawn)
        F = f["mu"] * N                                  # friction mu_r (W - L)
        close_to(L + N, W_LEN, 1e-12, "drawn lift plus wheel load equal the drawn weight")
        net = f["T"] * W_LEN - f["D"] * W_LEN - F
        assert (net > 0) == (f["T"] > 0), "net force forward on takeoff, backward on landing"
        assert mc[0] < cg[0] - 0.2, "main wheels drawn behind the center of gravity"
        kind_arrow(ax, cg + np.array([0, 0.10]), cg + np.array([0, 0.10 + L]), "force",
                   "lift, $L$" if f["T"] > 0 else "lift, $L$, small", label_dir=90 if f["T"] > 0 else 15)
        kind_arrow(ax, cg + np.array([0, -0.10]), cg + np.array([0, -0.10 - W_LEN]), "force", "weight, $W$",
                   label_dir=-90)
        nose = cg[0] + 0.44 * AC
        tail = cg[0] - 0.56 * AC
        kind_arrow(ax, (tail - 0.08, cg[1]), (tail - 0.08 - f["D"] * W_LEN - 0.15, cg[1]), "force", "drag, $D$",
                   label_dir=180)
        kind_arrow(ax, (mc[0], Y0 - N), (mc[0], Y0 - 0.05), "force")
        text(ax, (mc[0] - 0.08, Y0 - N + 0.16), "wheel load,\n$W - L$", direction=180, dist=4, fs=FS_SMALL)
        lab = "rolling friction, small" if f["T"] > 0 else "braking friction, $\\mu_r (W - L)$"
        kind_arrow(ax, (mc[0] - 0.14, Y0), (mc[0] - 0.14 - F - 0.12, Y0), "force", None)
        text(ax, (mc[0] - 0.14 - F - 0.12, Y0), lab, direction=180, dist=6, fs=FS_SMALL)
        if f["T"] > 0:
            ye = ac["engine"][1]
            kind_arrow(ax, (nose + 0.10, ye), (nose + 0.10 + f["T"] * W_LEN, ye), "force")
            text(ax, (nose + 0.10, ye), "thrust, $T$", direction=-90, dist=11, ha="left", fs=FS_LABEL)
        v0 = np.array([1.35, 0.95])
        kind_arrow(ax, v0, v0 + np.array([0.9, 0.0]), "velocity", "velocity, $V$", label_dir=0)
    legend_key(axs[1], (xlim[1] - 1.55, -1.25), [("force", "force"), ("velocity", "velocity")], dy=16, fs=FS_SMALL)
    save_figure(fig, "p55-ground-roll-forces")


def fig_constraint_build():
    """Lesson: each requirement removes part of the plane; what is left is the region of designs that
    meet them all. Six panels in the order of the page, one requirement added in each; the part it
    removes is shaded gray."""
    WS = np.linspace(1000.0, 5000.0, 401)
    lines = _lines(WS)
    WS_stall, WS_land = _limits()
    D = _design()
    fig, axs = data_axes(6.5, 4.9, nrows=2, ncols=3, sharex=True, sharey=True)
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.12, top=0.93, wspace=0.10, hspace=0.32)
    titles = dict(stall="1  stall speed", landing="2  landing roll", takeoff="3  takeoff roll",
                  climb="4  climb", cruise="5  cruise", ceiling="6  ceiling")
    hi = 0.45

    def region(done):
        ok = np.ones_like(WS, bool)
        need = np.zeros_like(WS)
        if "stall" in done:
            ok &= WS <= WS_stall
        if "landing" in done:
            ok &= WS <= WS_land
        for k in ("takeoff", "climb", "cruise", "ceiling"):
            if k in done:
                need = np.maximum(need, lines[k])
        return ok, need

    areas = []
    for i, (ax, name) in enumerate(zip(axs.flat, REQ_NAMES)):
        done = REQ_NAMES[: i + 1]
        ax.set_xlim(1000, 5000); ax.set_ylim(0.0, hi)
        ok0, need0 = region(done[:-1])
        ok, need = region(done)
        # the part this requirement removes, then what is left
        cut = ok0 & ((~ok) | (need > need0 + 1e-12))
        ax.fill_between(WS, need0, np.where(ok, need, hi), where=cut, facecolor=BAND_FILL, edgecolor=GRAY,
                        hatch="///", lw=0, zorder=0.5)
        ax.fill_between(WS[ok], need[ok], hi, color=FEASIBLE_FILL, lw=0, zorder=0.6)
        areas.append(float(np.trapezoid(np.clip(hi - need[ok], 0, None), WS[ok])))
        for k in done:
            # the new line in its own look; earlier lines thin and gray, with their dash and caps kept
            # (the cruise line's dots need their round caps to show)
            kw = constraint_kw(k) if k == name else constraint_kw(k, color=GRAY, linewidth=1.5)
            if k == "ceiling":
                kw.update(CEILING_MARKS, markevery=(0.07, 0.19))          # fewer marks in a small panel
            if k in ("stall", "landing"):
                ax.axvline(WS_stall if k == "stall" else WS_land, zorder=4 if k == name else 3, **kw)
            else:
                ax.plot(WS, lines[k], zorder=4 if k == name else 3, **kw)
        ax.set_title(titles[name], fontsize=FS_SMALL, loc="left", pad=4)
        # ticks every 1,000 from the axis start; only 2,000 and 4,000 carry a label, so the labels of
        # neighboring panels do not meet
        ax.set_xticks([1000, 2000, 3000, 4000, 5000], labels=["", "2,000", "", "4,000", ""])
        ax.set_yticks([0.0, 0.2, 0.4])
        if name in ("landing", "ceiling"):
            text(ax, (0.5 * (WS_stall + WS_land), 0.075), "removes\nnothing", fs=FS_SMALL)
        if name == "ceiling":
            ax.plot([D["ws"]], [D["tw"]], "o", ms=MS_POINT, color=INK, zorder=8)
            callout(ax, (D["ws"], D["tw"]), "design\npoint", at=(2050.0, 0.39), ha="center", fs=FS_SMALL,
                    backing=FEASIBLE_FILL)
    for ax in axs[1]:
        ax.set_xlabel("$W/S$, N/m²")
    for ax in axs[:, 0]:
        ax.set_ylabel("$T/W$")
    assert all(b <= a + 1e-9 for a, b in zip(areas, areas[1:])), "the region only shrinks"
    assert areas[-1] < 0.6 * areas[0], "the six requirements together remove much of the first region"
    close_to(areas[1], areas[0], 1e-9, "the landing limit removes nothing")
    close_to(areas[5], areas[4], 1e-9, "the ceiling removes nothing")
    gap_ce = float(np.max((lines["ceiling"] - np.maximum.reduce([lines["takeoff"], lines["climb"],
                                                                 lines["cruise"]]))[WS <= WS_stall]))
    assert gap_ce < 0.0, "the ceiling line lies below the takeoff, climb or cruise line wherever the stall allows"
    close_to(D["ws"], WS_stall, 1e-9, "the design point sits on the stall limit")
    save_figure(fig, "p55-constraint-build")


def fig_constraint_diagram():
    """Lesson: the design point is the highest wing loading the limits allow and the lowest
    thrust-to-weight ratio above every line. The lower strip enlarges T/W 0.17 to 0.25, where the
    climb and ceiling lines lie within 0.01 of each other."""
    WS = np.linspace(1000.0, 5000.0, 401)
    lines = _lines(WS)
    D = _design()
    WS_stall, WS_land = D["WS_stall"], D["WS_land"]
    need = np.max(np.vstack(list(lines.values())), axis=0)
    ws_d, tw_d = D["ws"], D["tw"]
    ws_o, tw_o = _own_point()
    fig, (ax, az) = data_axes(6.5, 5.9, nrows=2, sharex=True, gridspec_kw=dict(height_ratios=[2.3, 1.25]))
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.10, top=0.97, hspace=0.12)
    for a_, (lo, hi) in ((ax, (0.0, 0.45)), (az, (0.17, 0.25))):
        a_.set_ylim(lo, hi)
        ok = WS <= ws_d
        a_.fill_between(WS[ok], need[ok], hi, color=FEASIBLE_FILL, lw=0, zorder=0.6)
        for k, v in lines.items():
            if k == "ceiling":
                a_.plot(WS, v, zorder=4, **_ceiling_kw())
            else:
                constraint_line(a_, WS, v, k)
        constraint_vertical(a_, WS_stall, "stall")
        constraint_vertical(a_, WS_land, "landing")
        a_.plot([ws_d], [tw_d], "o", ms=MS_POINT + 1, color=INK, zorder=8)
    ax.plot([ws_o], [tw_o], "o", ms=MS_POINT, mfc="white", mec=INK, mew=1.6, zorder=8)
    ax.set_xlim(1000, 5000)
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4]); az.set_yticks([0.18, 0.20, 0.22, 0.24])
    az.set_xticks([1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000])
    az.set_xlabel("Wing loading, $W/S$, N/m²")
    ax.set_ylabel("Thrust-to-weight ratio, $T/W$")
    az.set_ylabel("$T/W$, enlarged")
    st = CONSTRAINT_STYLE
    y_at = lambda k, x: float(np.interp(x, WS, lines[k]))  # noqa: E731
    # every number in a label comes from the aircraft and its requirements (vehicles.py)
    own = f"the light twin-jet:\nwing {fmt(A['S'], 2)} m²,\nthrust {fmt(A['n'] * A['T0'], 5)} N"
    text(ax, (1800.0, 0.418), "designs that meet\nevery requirement", fs=FS_SMALL, backing=FEASIBLE_FILL)
    callout(ax, (ws_o, tw_o), own, at=(2150.0, 0.345), ha="center", fs=FS_SMALL, backing=FEASIBLE_FILL)
    callout(ax, (ws_d, tw_d), f"design point\n$W/S$ = {D['ws_label']} N/m²\n$T/W$ = {D['tw_label']}",
            at=(2990.0, 0.40), ha="left", fs=FS_SMALL)
    text(ax, (1650.0, y_at("takeoff", 1650.0)), f"takeoff roll, {fmt(Q['s_LO'], 3)} m", direction=-35, dist=8,
         fs=FS_SMALL, color=st["takeoff"]["text"])
    text(ax, (1090.0, y_at("climb", 1090.0)), "climb", direction=90, dist=5, ha="left", fs=FS_SMALL,
         color=st["climb"]["text"])
    text(ax, (1090.0, y_at("ceiling", 1090.0)), "ceiling", direction=-90, dist=6, ha="left", fs=FS_SMALL,
         color=st["ceiling"]["text"])
    text(ax, (3600.0, y_at("cruise", 3600.0)),
         f"cruise, {fmt(Q['V_cruise'], 3)} m/s\nat {fmt(Q['h_cruise'], 5)} m", direction=-90, dist=7,
         fs=FS_SMALL, color=st["cruise"]["text"])
    text(ax, (WS_stall, 0.05), f"stall speed,\n{fmt(Q['V_stall'], 2)} m/s", direction=180, dist=6, fs=FS_SMALL,
         color=st["stall"]["text"])
    text(ax, (WS_land, 0.27), f"landing roll,\n{fmt(Q['s_L'], 3)} m", direction=180, dist=6, fs=FS_SMALL,
         color=st["landing"]["text"])
    text(az, (3650.0, y_at("climb", 3650.0)), f"climb, {fmt(Q['RC'], 2)} m/s at {fmt(Q['V_climb'], 2)} m/s",
         direction=-90, dist=4, fs=FS_SMALL, color=st["climb"]["text"])
    text(az, (3600.0, y_at("ceiling", 3600.0)), f"service ceiling, {fmt(Q['h_ceiling'], 5)} m", direction=90,
         dist=9, fs=FS_SMALL, color=st["ceiling"]["text"])
    close_to(ws_d, WS_stall, 1e-9, "design point at the stall limit")
    close_to(tw_d, y_at("takeoff", ws_d), 1e-6, "the takeoff line sets the design T/W")
    assert all(y_at(k, ws_d) < tw_d for k in ("climb", "cruise", "ceiling")), "the other lines lie below it"
    assert ws_o < ws_d and tw_o > float(np.interp(ws_o, WS, need)), "the light twin-jet lies inside the region"
    gap = float(np.max(np.abs(lines["climb"] - lines["ceiling"])[WS >= 2000.0]))
    assert gap < 0.02, "climb and ceiling lines lie on each other: the enlarged strip is needed"
    save_figure(fig, "p55-constraint-diagram")


def fig_field_length_sensitivity():
    """Lesson: both ground rolls grow in proportion to the wing loading, and more thrust shortens only
    the takeoff."""
    D = _design()
    ws_o, tw_o = _own_point()
    WS = np.linspace(0.0, 4800.0, 241)
    k_to = K_LO ** 2 / (G0 * RHO_SL * A["CLmax_TO"])
    k_la = K_TD ** 2 / (G0 * RHO_SL * A["CLmax_L"] * A["mu_r"])
    to_d, to_o, la = k_to * WS / D["tw"], k_to * WS / tw_o, k_la * WS
    fig, ax = data_axes(6.5, 4.2)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.13, top=0.97)
    ax.set_xlim(0, 4800); ax.set_ylim(0, 1200)
    # each limit in the style of its roll: the takeoff limit thin dashed black, the landing limit thin
    # dotted vermilion like the landing line (they differ by style, not by color alone)
    ax.axhline(Q["s_LO"], color=INK, lw=LW_THIN, ls=DASH_CONSTRUCTION, zorder=2)
    ax.axhline(Q["s_L"], color=SERIES[1], lw=1.6, ls=(0, (0.1, 2.4)), dash_capstyle="round", zorder=2)
    ax.plot(WS, to_d, color=INK, lw=2.0, zorder=4)
    ax.plot(WS, to_o, color=INK, lw=2.0, ls=(0, (6.0, 2.5)), zorder=4)
    ax.plot(WS, la, color=SERIES[1], lw=2.4, ls=(0, (0.1, 2.6)), dash_capstyle="round", zorder=4)
    s_lo_o, s_l_o, s_l_d = k_to * ws_o / tw_o, k_la * ws_o, k_la * D["ws"]
    ax.plot([D["ws"]], [Q["s_LO"]], "o", ms=MS_POINT, color=INK, zorder=7)
    ax.plot([ws_o, ws_o], [s_lo_o, s_l_o], "o", ms=MS_POINT, mfc="white", mec=INK, mew=1.5, zorder=7, ls="none")
    ax.set_xticks([0, 1000, 2000, 3000, 4000]); ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
    ax.set_xlabel("Wing loading, $W/S$, N/m²")
    ax.set_ylabel("Ground roll, m")
    text(ax, (1700, k_to * 1700 / D["tw"]), f"takeoff, $T/W$ = {D['tw_label']}", direction=150, dist=8,
         fs=FS_SMALL)
    text(ax, (4150, k_to * 4150 / tw_o), f"takeoff,\n$T/W$ = {fmt(tw_o, 4)}", direction=-30, dist=12, fs=FS_SMALL)
    text(ax, (4100, k_la * 4100), "landing, any $T/W$", direction=-35, dist=10, fs=FS_SMALL, color=TEXT_VERMILION)
    text(ax, (250, Q["s_LO"]), f"takeoff limit, {fmt(Q['s_LO'], 3)} m", direction=90, dist=3, fs=FS_SMALL,
         ha="left")
    text(ax, (250, Q["s_L"]), f"landing limit, {fmt(Q['s_L'], 3)} m", direction=-90, dist=3, fs=FS_SMALL,
         ha="left", color=TEXT_VERMILION)
    callout(ax, (D["ws"], Q["s_LO"]), "design point", at=(1900, 900), ha="right", fs=FS_SMALL)
    callout(ax, (ws_o, s_lo_o), f"{fmt(s_lo_o, 3)} m", at=(3050, 610), ha="left", fs=FS_SMALL)
    callout(ax, (ws_o, s_l_o), f"{fmt(s_l_o, 3)} m", at=(2950, 320), ha="left", fs=FS_SMALL)
    ax.plot([ws_o, ws_o], [0.0, s_l_o], color=INK, lw=LW_THIN, ls=DASH_CONSTRUCTION, zorder=2)
    text(ax, (ws_o, 60), "the light twin-jet", direction=0, dist=5, fs=FS_SMALL, ha="left")
    on_curve(WS, to_d, D["ws"], Q["s_LO"], 1e-6, "design point on the line of the design's T/W")
    close_to(float(np.interp(0.5 * ws_o, WS, to_o)) / s_lo_o, 0.5, 1e-3, "half the wing loading, half the takeoff roll")
    assert s_lo_o < Q["s_LO"] and s_l_o < Q["s_L"] and s_l_d < Q["s_L"]
    save_figure(fig, "p55-field-length-sensitivity")


def make_all():
    fig_takeoff_landing_phases()
    fig_ground_roll_forces()
    fig_constraint_build()
    fig_constraint_diagram()
    fig_field_length_sensitivity()


# ===================================================================== printed values
def values():
    """Every printed value, rounded as printed; each later step uses the printed digits before it."""
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731
    # givens
    r("m", fmt(A["m"], 4)); r("S", fmt(A["S"], 2)); r("T-tot", fmt(A["n"] * A["T0"], 5))
    r("CD0", fmt_dec(A["CD0"], 3)); r("AR", fmt(A["AR"], 1)); r("e", fmt_dec(A["e"], 1))
    r("CL-TO", fmt_dec(A["CLmax_TO"], 2)); r("CL-L", fmt_dec(A["CLmax_L"], 2)); r("mur", fmt_dec(A["mu_r"], 2))
    r("mad", fmt_dec(A["m_ad"], 1))
    r("req-Vs", fmt(Q["V_stall"], 2)); r("req-sLO", fmt(Q["s_LO"], 3)); r("req-sL", fmt(Q["s_L"], 3))
    r("req-RC", fmt(Q["RC"], 2)); r("req-Vcl", fmt(Q["V_climb"], 2))
    r("req-Vcr", fmt(Q["V_cruise"], 3)); r("req-hcr", fmt(Q["h_cruise"], 5)); r("req-hce", fmt(Q["h_ceiling"], 5))
    # weight and polar constant
    Wp = _num(r("W", fmt(A["m"] * G0, 5)))
    Kp = _num(r("K", fmt(1.0 / (math.pi * A["e"] * A["AR"]), 4)))
    # the two wing-loading limits
    WSp = _num(r("WS-stall", fmt(0.5 * RHO_SL * Q["V_stall"] ** 2 * A["CLmax_L"], 5)))      # 2,786.5
    land_num = _num(r("land-num", fmt(RHO_SL * G0 * A["CLmax_L"] * A["mu_r"] * Q["s_L"], 4)))
    r("WS-land", fmt(land_num / 1.69, 4))
    # the four thrust lines at the stall limit
    # five figures, so that the total thrust follows from it to the newton
    tw_to = _num(r("TW-to", fmt(1.44 * WSp / (RHO_SL * G0 * A["CLmax_TO"] * Q["s_LO"]), 5)))
    r("TW-des", fmt(tw_to, 4))                     # the design point as the text and the figures give it
    q_cl = _num(r("q-cl", fmt(0.5 * RHO_SL * Q["V_climb"] ** 2, 4)))
    cl1 = _num(r("TW-cl-1", fmt(Q["RC"] / Q["V_climb"], 4)))
    cl2 = _num(r("TW-cl-2", fmt(q_cl * A["CD0"] / WSp, 4)))
    cl3 = _num(r("TW-cl-3", fmt(Kp * WSp / q_cl, 4)))
    r("TW-cl", fmt(cl1 + cl2 + cl3, 4))
    rho_cr = _num(r("rho-cr", fmt(standard(Q["h_cruise"])[2], 4)))
    q_cr = _num(r("q-cr", fmt(0.5 * rho_cr * Q["V_cruise"] ** 2, 4)))
    lap_cr = _num(r("lap-cr", fmt((rho_cr / RHO_SL) ** A["m_ad"], 4)))
    cr1 = _num(r("TW-cr-1", fmt(q_cr * A["CD0"] / WSp, 4)))
    cr2 = _num(r("TW-cr-2", fmt(Kp * WSp / q_cr, 4)))
    r("TW-cr", fmt((cr1 + cr2) / lap_cr, 4))
    rho_ce = _num(r("rho-ce", fmt(standard(Q["h_ceiling"])[2], 4)))
    lap_ce = _num(r("lap-ce", fmt((rho_ce / RHO_SL) ** A["m_ad"], 4)))
    V_ce = _num(r("V-ce", fmt(math.sqrt(2.0 * WSp / rho_ce * math.sqrt(Kp / A["CD0"])), 4)))
    tw_min = _num(r("tw-min", fmt(2.0 * math.sqrt(Kp * A["CD0"]), 4)))
    r("TW-ce", fmt((tw_min + Q["RC_ceiling"] / V_ce) / lap_ce, 4))
    # the design point, the wing and the engines
    r("S-des", fmt(Wp / WSp, 4))
    r("T-des", fmt(tw_to * Wp, 5))
    # the light twin-jet's own wing and engines, and its ground rolls
    WSo = _num(r("WS-own", fmt(Wp / A["S"], 4)))
    TWo = _num(r("TW-own", fmt(A["n"] * A["T0"] / Wp, 4)))
    r("sLO-own", fmt(1.44 * WSo / (G0 * RHO_SL * A["CLmax_TO"] * TWo), 3))
    r("sL-own", fmt(1.69 * WSo / (G0 * RHO_SL * A["CLmax_L"] * A["mu_r"]), 3))
    Vs_to = _num(r("Vs-TO-own", fmt(math.sqrt(2.0 * WSo / (RHO_SL * A["CLmax_TO"])), 4)))
    Vs_l = _num(r("Vs-L-own", fmt(math.sqrt(2.0 * WSo / (RHO_SL * A["CLmax_L"])), 4)))
    r("VLO-own", fmt(1.2 * Vs_to, 3))
    r("VT-own", fmt(1.3 * Vs_l, 3))
