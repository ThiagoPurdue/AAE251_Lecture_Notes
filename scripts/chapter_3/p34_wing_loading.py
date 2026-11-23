"""Page "Wing loading" (Chapter 3, no standard): figures and printed values.

Sources (each opened):
  - Nicolai, L. M., and Carichner, G. E., Fundamentals of Aircraft and Airship Design, Vol. 1,
    AIAA, 2010: Chapter 6, Section 6.1 (the requirements that set the takeoff wing loading),
    Table 6.1 (takeoff wing loading trends, lb/ft^2, page 153), Section 6.2 (a propeller
    aircraft cruises for range at (L/D)max), Example 6.1 (the air-launched cruise missile:
    C_D,0 = 0.035, K = 0.059, Mach 0.7 at 200 ft, launch weight 1,800 lb, C_L = (C_D,0/3K)^1/2);
    Chapter 9, Eq. (9.9) and Figure 9.23 (wing increment of the maximum lift coefficient from a
    trailing-edge flap, K_Lambda = (1 - 0.08 cos^2 Lambda) cos^(3/4) Lambda), Table 9.1 (C_L,max of
    aircraft with their high-lift systems).
  - Jenkinson, L. R., Simpkin, P., and Rhodes, D., Civil Jet Aircraft Design, 1999, companion web
    site, Data A, Table 4 (Boeing 777-200: maximum takeoff mass 242,670 kg, wing area 427.80 m^2,
    "max wing load" 567.25 kg/m^2).
The four-engine turboprop airlifter of the worked examples is invented (values typical of the
STOL and utility transport class of Table 6.1).
"""
from chapter_3.common import *
from matplotlib.patches import Rectangle, Polygon

PAGE = "p34"

# ===================================================================== data
LB_FT2 = LB_N / FT ** 2            # N/m^2 per lb/ft^2 (47.880)

# Published data (Nicolai and Carichner 2010, Tables 6.1 and 9.1, Example 6.1; Jenkinson et al.
# 1999, Data A): chapter_3/published.py. The flap relation (Nicolai and Carichner 2010, Eq. (9.9),
# Figure 9.23) is aero.flap_dCLmax with aero.sweep_factor.

# Invented four-engine turboprop airlifter (short-field and utility transport class)
LIFTER = dict(W=700000.0, V_stall=50.0, CLmax_clean=1.40, dcl_flap=1.30, flapped=0.70, sweep=0.0,
              CD0=0.028, AR=10.0, e=0.80, h_cruise=7000.0, V_cruise=135.0)


def _row(name):
    """A row of the wing-loading trends (Nicolai and Carichner 2010, Table 6.1) by its name."""
    rows = [r for r in WS_TRENDS_CIVIL + WS_TRENDS_MILITARY if r[0] == name]
    assert len(rows) == 1, name
    return rows[0]


STOL = "Short-field and utility transports"
LONG = "Long-range transports and bombers"
SAIL = "Competition sailplanes"
SOLAR = "High-altitude surveillance, solar"
MISSILE = "Low-altitude cruise missiles"


# ===================================================================== the numbers of the page
def _numbers():
    n = {}
    # Worked example 1: Boeing 777-200
    W = B772_MTOW_KG * G0
    n["W772"] = W
    n["WS772"] = W / B772_S_M2
    n["WS772_en"] = round(n["WS772"]) / round(LB_FT2, 3)
    # Worked example 2: airlifter, stall requirement
    L = LIFTER
    n["K_sweep"] = sweep_factor(L["sweep"])
    n["dCL"] = flap_dCLmax(L["dcl_flap"], L["flapped"], L["sweep"])
    n["CLmax_flaps"] = L["CLmax_clean"] + round(n["dCL"], 4)
    n["q_stall"] = 0.5 * RHO_SL * L["V_stall"] ** 2
    n["WS_stall"] = wing_loading_stall(RHO_SL, L["V_stall"], round(n["CLmax_flaps"], 3))
    n["WS_clean"] = wing_loading_stall(RHO_SL, L["V_stall"], L["CLmax_clean"])
    n["S_stall"] = L["W"] / round(n["WS_stall"])
    n["S_clean"] = L["W"] / round(n["WS_clean"])
    n["WS_stall_en"] = round(n["WS_stall"]) / round(LB_FT2, 3)
    n["WS_gain"] = n["q_stall"] * round(n["dCL"], 4)                 # what the flaps add at 50 m/s: q dCL,max
    # Worked example 3: cruise missile
    A = ALCM
    n["m_ratio"] = A["CD0"] / (3.0 * A["K"])
    n["m_CL"] = math.sqrt(round(n["m_ratio"], 5))
    n["m_V"] = A["M"] * A["a"]
    n["m_q"] = 0.5 * A["rho"] * n["m_V"] ** 2
    n["m_WS"] = round(n["m_q"], 1) * round(n["m_CL"], 4)
    n["m_S"] = A["W_lb"] / round(n["m_WS"], 2)
    # Worked example 4: airlifter, cruise condition, then both together
    T, p, rho = standard(L["h_cruise"])
    n["rho_c"] = rho
    n["K"] = polar_K(L["AR"], L["e"])
    n["CL_star_ratio"] = L["CD0"] / round(n["K"], 6)
    n["CL_star"] = math.sqrt(round(n["CL_star_ratio"], 5))
    n["q_c"] = 0.5 * round(rho, 5) * L["V_cruise"] ** 2
    n["WS_cruise"] = round(n["q_c"]) * round(n["CL_star"], 4)
    n["CL_design"] = round(n["WS_stall"]) / round(n["q_c"])
    CLd = round(n["CL_design"], 3)
    n["CD_design"] = L["CD0"] + round(n["K"], 6) * CLd ** 2
    n["LD_design"] = CLd / round(n["CD_design"], 5)
    n["LD_max"] = min_drag_point(L["CD0"], n["K"])["LD_max"]
    n["LD_frac"] = round(n["LD_design"], 2) / round(n["LD_max"], 2)
    return n


N = _numbers()


# ===================================================================== figures
def design_parameters():
    """One airliner (the Boeing 737-800, plan view to scale) with the three numbers that size it:
    the wing area (wing loading), the engines (thrust-to-weight ratio) and the span with the area
    (aspect ratio). The reference area runs through the fuselage: its edges are dashed there."""
    parts = aircraft_top()
    only = [k for k in parts if k.split("_")[0] in ("fuselage", "wing", "winglet", "nacelle", "pylon",
                                                     "htail", "vtail", "exhaust")]
    X0, X1, Y0, Y1 = -3.0, 64.0, -19.5, 19.5
    w_in = 6.5
    fig, ax = new_axes(w_in, w_in * (Y1 - Y0) / (X1 - X0))
    fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
    set_frame(ax, X0, X1, Y0, Y1)
    P = draw_parts(ax, parts, highlight=("wing_L", "wing_R"), only=only, details=False)
    for k in ("nacelle_L", "nacelle_R"):
        P[k].set_hatch("////")
        P[k].set_facecolor("#D9D9D9")
    # the part of the reference area inside the fuselage: shaded, its edges dashed
    wr = parts["wing_R"].xy
    root_le, root_te = wr[0, 0], wr[-1, 0]           # the wing's root chord on the centerline
    fus = parts["fuselage"].xy
    up = fus[fus[:, 1] > 0]
    order = np.argsort(up[:, 0])
    yf = float(np.interp(0.5 * (root_le + root_te), up[order, 0], up[order, 1]))
    le_y = lambda y: float(np.interp(abs(y), wr[:2, 1], wr[:2, 0]))
    inner = np.array([(le_y(-yf), -yf), (le_y(yf), yf), (root_te, yf), (root_te, -yf)])
    zf = P["fuselage"].get_zorder()
    sh = ax.add_patch(Polygon(inner, closed=True, fc=HIGHLIGHT, ec="none", zorder=zf + 0.01))
    on_part(sh, P["fuselage"])
    for a, b in ((inner[0], inner[1]), (inner[2], inner[3])):
        on_part(ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=LW_DETAIL, ls=(0, (3, 2)), zorder=zf + 0.02)[0],
                P["fuselage"])
    # span of the wing (Jenkinson et al. 1999: 34.30 m, without the winglets)
    b = B738_WING["b_m"]
    xw0, xw1, yw0, yw1 = extent({k: parts[k] for k in ("wing_L", "wing_R")})
    close_to(yw1 - yw0, b, 0.05, "wing span drawn")
    xd = 43.0
    for yy in (yw0, yw1):
        ax.plot([xw1 + 0.8, xd + 1.0], [yy, yy], **line_kw("reference"), zorder=1)
    dimension(ax, (xd, yw0), (xd, yw1), None, extension=False)
    text(ax, (xd, 5.5), f"span, $b$ = {fmt(b)} m", direction=0.0, dist=6.0)
    text(ax, (xd, -1.5), "with $S$, it sets the\naspect ratio, the shape:", direction=0.0, dist=6.0)
    text(ax, (xd, -8.0), r"$\mathit{AR} = b^2/S$ = " + fmt(B738_WING["AR"], 3), direction=0.0, dist=6.0)
    # wing area and engines, named at the left with short leaders
    label_part(ax, P, parts, "wing_R", f"wing area, $S$ = {fmt(B738_WING['S_m2'], 5)} m$^2$,\n"
               "set by the wing loading $W/S$", at=(-2.5, 15.0), ha="left", target=(19.5, 8.0))
    label_part(ax, P, parts, "nacelle_L", "engines: thrust set by the\nthrust-to-weight ratio $T/W$",
               at=(-2.5, -15.5), ha="left", target=(14.0, -4.8))
    assert (B738["length"] / (X1 - X0)) > 0.55, "the aircraft fills more than half the width"
    trim_canvas(fig)
    save_figure(fig, "p34-design-parameters")


def flap_area():
    """The right wing of the 737-800 in plan view, span across: the flaps, the flapped area (the
    whole chord, leading edge to trailing edge, over the span of each flap; Nicolai and Carichner
    2010, Figure 9.24), hatched over the flaps too, the gap between the flaps left out; and the sweep
    of the quarter-chord line, constructed at the tip on the white outer panel."""
    from matplotlib import patheffects as pe
    parts = aircraft_top()
    wr = parts["wing_R"].xy
    yfus = B738["fus_width"] / 2.0                   # the fuselage side
    # plan coordinates turned so the span runs to the right and the leading edge is at the top
    T = lambda xy: np.c_[np.asarray(xy)[:, 1], -np.asarray(xy)[:, 0]]
    fi, fo = parts["flap_inboard_R"].xy, parts["flap_outboard_R"].xy
    le = lambda y: float(np.interp(y, wr[:3, 1], wr[:3, 0]))
    te = lambda y: float(np.interp(y, wr[[5, 4, 3], 1], wr[[5, 4, 3], 0]))

    def strip(y0, y1):
        ys = np.linspace(y0, y1, 40)
        return np.r_[np.c_[[le(y) for y in ys], ys], np.c_[[te(y) for y in ys[::-1]], ys[::-1]]]
    spans = [(float(f[:, 1].min()), float(f[:, 1].max())) for f in (fi, fo)]
    spans[0] = (yfus, spans[0][1])                    # the inboard flap starts at the fuselage side (drawn 0.1 m out)
    strips = [strip(*sp) for sp in spans]
    # the exposed wing: from the fuselage side to the tip
    yk, yt = wr[1, 1], wr[2, 1]
    exposed = np.array([(le(yfus), yfus), (le(yk), yk), (le(yt), yt), (te(yt), yt), (te(yk), yk), (te(yfus), yfus)])
    X0, X1, Y0, Y1 = -1.0, 19.0, -27.4, -11.0
    fig, ax = canvas(6.5, xlim=(X0, X1), ylim=(Y0, Y1))
    wing = ax.add_patch(opaque(Polygon(T(exposed), closed=True, fc="white", ec=INK, lw=LW_OUTLINE,
                                       joinstyle="round", zorder=2)))
    for st in strips:                                 # the flapped area: light fill under the flaps
        on_part(ax.add_patch(Polygon(T(st), closed=True, fc=HIGHLIGHT, ec="none", lw=0.0, zorder=2.1)), wing)
    for f in (fi, fo):                                # the flaps, gray
        on_part(ax.add_patch(Polygon(T(f), closed=True, fc=SURFACE_FILL, ec="none", lw=0.0, zorder=2.2)), wing)
    for st in strips:                                 # the hatch lies over the flaps: they are part of the area
        on_part(ax.add_patch(Polygon(T(st), closed=True, fc="none", ec=GRAY, lw=0.0, hatch="\\\\",
                                     hatch_linewidth=0.5, zorder=2.3)), wing)
    for f in (fi, fo):                                # flap outlines on top of the hatch
        on_part(ax.add_patch(Polygon(T(f), closed=True, fc="none", ec=INK, lw=LW_DETAIL, zorder=2.4)), wing)
    ax.add_patch(Polygon(T(exposed), closed=True, fc="none", ec=INK, lw=LW_OUTLINE, joinstyle="round",
                         zorder=2.6))                 # the wing's outline, over the fills
    for y0, y1 in spans:                              # the ends of each strip: chordwise lines
        for y in (y0, y1):
            on_part(ax.plot([y, y], [-le(y), -te(y)], color=INK, lw=LW_DETAIL, zorder=2.5)[0], wing)
    for (y0, y1), f in zip(spans, (fi, fo)):         # the hatch covers each flap from end to end
        assert y0 <= f[:, 1].min() + 1e-9 and f[:, 1].max() <= y1 + 1e-9
    # the fuselage side, a short stretch of it
    xa, xb = le(yfus) - 1.0, te(yfus) + 1.2
    ax.plot([yfus, yfus], [-xa, -xb], color=INK, lw=LW_OUTLINE, zorder=3)
    text(ax, (yfus, -xb), "fuselage side", direction=-90.0, dist=3.0, fs=FS_SMALL)
    # quarter-chord line of the outer panel (black, dashed, a white halo where it crosses the hatch)
    q = lambda y: le(y) + 0.25 * (te(y) - le(y))
    qa, qb = np.array([yk, -q(yk)]), np.array([yt, -q(yt)])
    on_part(ax.plot(*np.c_[qa, qb], color=INK, lw=1.2, ls=(0, (6, 3)), zorder=3,
                    path_effects=[pe.Stroke(linewidth=3.2, foreground="white"), pe.Normal()])[0], wing)
    sweep = math.degrees(math.atan2(-(qb[1] - qa[1]), qb[0] - qa[0]))
    close_to(sweep, B738_WING["sweep_c4"], 0.03, "quarter-chord sweep of the drawn wing", rel=True)
    # the sweep, at the tip: from the spanwise direction (a reference line running inboard) to the
    # quarter-chord line, on the outer panel, which has no flaps
    r_arc, r_lab = 2.0, 2.75
    ref_end = qb + np.array([-(r_arc + 0.2), 0.0])  # just past the arc: the leader below passes its end
    assert ref_end[0] > spans[1][1] and -ref_end[1] < te(ref_end[0]), "the construction stays on the outer panel"
    on_part(ax.plot([qb[0], ref_end[0]], [qb[1], ref_end[1]], **line_kw("reference"), zorder=3)[0], wing)
    arc = angle_mark(ax, qb, 180.0 - sweep, 180.0, r_arc, r"$\Lambda$", stated=sweep, label_r=r_lab)
    on_part(arc, wing)
    am = qb + r_arc * unit(180.0 - 0.6 * sweep)
    lab = qb + r_lab * unit(180.0 - 0.5 * sweep)
    assert -lab[1] < te(lab[0]) - 0.5 and -lab[1] > q(lab[0]) + 0.3, "the label sits between the two lines"
    callout(ax, am, "sweep of the\nquarter-chord line", at=(13.5, -25.5), ha="center")
    # the flapped area and the flaps
    callout(ax, (3.1, -le(3.1) - 0.7), "flapped area, $S_\\mathrm{flapped}$:\nthe whole chord where\nthe wing has flaps",
            at=(6.6, -12.6), ha="center")
    callout(ax, (9.0, -float(np.interp(9.0, fo[:24, 1], fo[:24, 0])) - 0.4), "flaps", at=(7.6, -25.6), ha="center")
    callout(ax, (3.1, -float(np.interp(3.1, fi[:24, 1], fi[:24, 0])) - 0.4), " ", at=(6.9, -25.2), backing=False)
    Sf = sum(float(np.trapezoid([te(y) - le(y) for y in np.linspace(*sp, 200)], np.linspace(*sp, 200)))
             for sp in spans)
    yy = np.linspace(0.0, yt, 400)
    S_half = float(np.trapezoid([te(y) - le(y) for y in yy], yy))
    close_to(2 * S_half, B738_WING["S_m2"], 0.04, "the drawn wing has the published area", rel=True)
    assert 0.4 < Sf / S_half < 0.9, Sf / S_half
    flap_area.ratio = Sf / S_half
    trim_canvas(fig)
    save_figure(fig, "p34-flap-area")


def wing_loading_classes():
    """Typical takeoff wing loadings by mission (Nicolai and Carichner 2010, Table 6.1), two panels at
    one scale, with the 777-200 of worked example 1 and the airlifter and the missile of worked
    examples 2 and 3 marked."""
    groups = [("Transports, sailplanes, and surveillance aircraft", WS_TRENDS_CIVIL),
              ("Fighters and cruise missiles", WS_TRENDS_MILITARY)]
    hr = [len(WS_TRENDS_CIVIL) + 0.9, len(WS_TRENDS_MILITARY) + 0.9]
    fig, axs = data_axes(6.5, 6.8, nrows=2, sharex=True, gridspec_kw=dict(height_ratios=hr))
    fig.subplots_adjust(left=0.43, right=0.97, top=0.955, bottom=0.09, hspace=0.30)
    ys_of = {}
    for ax, (title, rows) in zip(axs, groups):
        n = len(rows)
        ys = np.arange(n)[::-1]
        for y, (name, lo, hi, ex) in zip(ys, rows):
            ax.add_patch(Rectangle((lo, y - 0.22), hi - lo, 0.44, fc=HIGHLIGHT, ec=INK, lw=1.2, zorder=3))
            if ex:
                text(ax, (hi, y), ex, direction=0.0, dist=4.0, fs=FS_SMALL, backing=False)
            ys_of[name] = (ax, y)
        ax.set_yticks(ys, [r[0] for r in rows])
        ax.set_ylim(-1.2, n - 0.3)                       # room under the last row for an example label
        ax.grid(False, axis="y")
        ax.tick_params(axis="y", length=0)
        ax.tick_params(axis="x", labelbottom=True)
        ax.set_title(title, fontsize=FS_LABEL, loc="left", x=-0.72, fontweight="bold")
        ax.set_xlim(0, 350)
        ax.set_xticks([0, 50, 100, 150, 200, 250, 300, 350])
    # the 777-200 of worked example 1, in the long-range transport row
    ax, y = ys_of[LONG]
    ws = float(N["WS772_en"])
    ax.plot([ws], [y], marker="D", ms=7, mfc=INK, mec=INK, ls="none", zorder=6)
    text(ax, (ws - 6.0, y - 0.52), f"Boeing 777-200, example 1: {fmt(ws)}", ha="left", fs=FS_SMALL)
    lo, hi = _row(LONG)[1:3]
    assert lo <= ws <= hi, "the 777-200 lies inside the long-range transport range"
    # the airlifter of worked example 2 (flaps-down stall limit), in the short-field row
    ax, y = ys_of[STOL]
    wa = float(N["WS_stall_en"])
    ax.plot([wa], [y], "o", ms=7, mfc="white", mec=INK, mew=1.5, ls="none", zorder=6)
    text(ax, (wa - 6.0, y - 0.5), f"airlifter, example 2: {fmt(wa, 3)}", ha="left", fs=FS_SMALL, backing=False)
    assert _row(STOL)[1] <= wa <= _row(STOL)[2], "the airlifter lies inside its class"
    # the missile of worked example 3, above its class
    ax, y = ys_of[MISSILE]
    wm = float(N["m_WS"])
    ax.plot([wm], [y], "o", ms=7, mfc="white", mec=INK, mew=1.5, ls="none", zorder=6)
    text(ax, (wm + 10.0, y - 0.52), f"missile, example 3: {fmt(wm, 4)}", ha="right", fs=FS_SMALL)   # under its row, as the others
    assert wm > _row(MISSILE)[2], "the missile of example 3 lies above its class range"
    axs[1].set_xlabel("Takeoff wing loading, lb/ft²")
    save_figure(fig, "p34-wing-loading-classes")


def stall_speed():
    """Largest wing loading that meets a stall speed, clean and flaps down, for the airlifter of
    worked example 2, with what the flaps add at the required speed (a dimension on the
    requirement line, between the two allowed wing loadings)."""
    L = LIFTER
    fig, ax = data_axes(6.5, 4.6)
    fig.subplots_adjust(left=0.13, right=0.97, top=0.96, bottom=0.14)
    V = np.linspace(36.0, 64.0, 200)
    clf = round(N["CLmax_flaps"], 3)
    ws_f = wing_loading_stall(RHO_SL, V, clf)
    ws_c = wing_loading_stall(RHO_SL, V, L["CLmax_clean"])
    ax.plot(V, ws_f, **line_kw(0))
    ax.plot(V, ws_c, **line_kw(1))
    Vs = L["V_stall"]
    ax.set_xlim(35, 65); ax.set_ylim(0, 6000)
    ax.set_xticks([35, 40, 45, 50, 55, 60, 65]); ax.set_yticks([0, 1000, 2000, 3000, 4000, 5000, 6000])
    ax.set_xlabel("Stall speed, m/s")
    ax.set_ylabel("Wing loading, $W/S$, N/m²")
    wf, wc = round(N["WS_stall"]), round(N["WS_clean"])
    # the requirement line, broken where the dimension between the two points sits on it
    ax.plot([Vs, Vs], [0.0, wc], **line_kw("boundary"), zorder=1)
    ax.plot([Vs, Vs], [wf, 6000.0], **line_kw("boundary"), zorder=1)
    for w in (wf, wc):
        ax.plot([Vs], [w], "o", ms=6.5, color=INK, zorder=6)
    close_to(float(wing_loading_stall(RHO_SL, Vs, clf)), N["WS_stall"], 1e-9, "point on the flaps-down curve")
    assert ws_f.max() < 6000, "the flaps-down curve stays inside the frame"
    text(ax, (Vs, wf), f"{fmt(wf)} N/m²", direction=155.0, dist=9.0)
    text(ax, (Vs, wc), f"{fmt(wc)} N/m²", direction=140.0, dist=10.0)
    # what the flaps add at the required stall speed
    fig.canvas.draw()
    ky = 6000.0 / (ax.get_position().height * fig.get_figheight() * 72.0)       # W/S units per point
    r = 5.0 * ky                                                                    # clear of the dots
    dimension(ax, (Vs, wc + r), (Vs, wf - r), None, extension=False, ticks=False)
    # its label, q dCL,max = what the flaps add, in two lines, each set into the band between
    # the two curves (the band rises to the right)
    text(ax, (Vs, 3250.0), r"$q\,\Delta C_{L,\max}$", direction=0.0, dist=12.0)
    text(ax, (Vs, 2890.0), f"= {fmt(N['WS_gain'])} N/m²", direction=0.0, dist=12.0, fs=FS_SMALL)
    close_to(wf - wc, N["WS_gain"], 1.0, "the dimension spans the two points (rounded limits)")
    vf = 41.0
    callout(ax, (vf, float(wing_loading_stall(RHO_SL, vf, clf))), f"flaps down, $C_{{L,\\max}}$ = {fmt(clf)}",
            at=(37.5, 4600.0), ha="left")
    label_curve(ax, V, ws_c, 42.0, f"clean, $C_{{L,\\max}}$ = {fmt(L['CLmax_clean'], 3)}", 1, offset=(14.0, -26.0))
    text(ax, (Vs, 600), "requirement: stall\nat 50 m/s or less", direction=0.0, dist=6.0)
    # the lesson: at one stall speed the flapped wing can carry more weight per area
    assert wf > 1.5 * wc and np.all(np.diff(ws_f) > 0), "flaps raise the allowed wing loading; it grows with speed"
    save_figure(fig, "p34-stall-speed")


def two_requirements():
    """Cruise lift-to-drag ratio of the airlifter against wing loading, with the stall limit: the
    design takes the smaller wing loading, at a small cost in L/D (marked)."""
    L = LIFTER
    K = round(N["K"], 6)
    q = round(N["q_c"])
    WS = np.linspace(1500.0, 7000.0, 400)
    CL = WS / q
    LD = CL / (L["CD0"] + K * CL ** 2)
    fig, ax = data_axes(6.5, 3.9)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.96, bottom=0.14)
    lim = round(N["WS_stall"])
    ax.axvspan(lim, 7000, fc="#EDEDED", lw=0.0, zorder=0)
    ax.plot(WS, LD, **line_kw(0), zorder=3)
    ax.axvline(lim, **line_kw("boundary"), zorder=2)
    ax.set_xlim(1500, 7000); ax.set_ylim(6, 17)
    ax.set_xticks([2000, 3000, 4000, 5000, 6000, 7000]); ax.set_yticks([6, 8, 10, 12, 14, 16])
    ax.set_xlabel("Wing loading, $W/S$, N/m²")
    ax.set_ylabel("Cruise $L/D$ at 7,000 m, 135 m/s")
    wc = round(N["WS_cruise"])
    ldm = N["LD_max"]
    ldd = round(N["LD_design"], 2)
    ax.plot([wc], [ldm], "s", ms=6.5, mfc="white", mec=INK, mew=1.5, zorder=6)
    ax.plot([lim], [ldd], "o", ms=7, color=INK, zorder=6)
    LDw = float(np.interp(wc, WS, LD))
    close_to(LDw, ldm, 0.01, "the L/D curve peaks at the cruise wing loading")
    assert LD.argmax() == np.abs(WS - wc).argmin() or abs(WS[LD.argmax()] - wc) < 20.0, "peak at W/S = q C_L*"
    text(ax, (wc, ldm), f"best for cruise:\n{fmt(wc)} N/m², $L/D$ = {fmt(ldm)}", direction=90.0, dist=8.0,
         fs=FS_SMALL, backing=False)
    text(ax, (lim, ldd), f"design point: {fmt(lim)} N/m²\n$L/D$ = {fmt(ldd)}", direction=-35.0, dist=9.0,
         fs=FS_SMALL, backing=False)
    # the cost of the stall limit: from the design point up to the best L/D
    xg = lim - 520.0
    ax.plot([xg - 20.0, wc - 90.0], [ldm, ldm], color=GRAY, lw=0.7, zorder=2)
    ax.plot([xg - 20.0, lim - 70.0], [ldd, ldd], color=GRAY, lw=0.7, zorder=2)
    fig.canvas.draw()
    ky = (ax.get_ylim()[1] - ax.get_ylim()[0]) / (ax.get_position().height * fig.get_figheight() * 72.0)
    lead = 9.0 * ky                                   # arrows point in from outside: the gap is small
    for y_from, y_to in ((ldd - lead, ldd), (ldm + lead, ldm)):
        arrow(ax, (xg, y_from), (xg, y_to), color=INK, lw=LW_THIN, head="small", zorder=4, gid="grp:ld-cost")
    ax.plot([xg, xg], [ldd, ldm], color=INK, lw=LW_THIN, zorder=4, gid="grp:ld-cost")
    assert float(np.interp(xg, WS, LD)) < ldd - lead, "the lower arrow stays above the curve"
    close_to(ldm - ldd, ldm * (1.0 - N["LD_frac"]), 0.01, "the dimension spans the L/D given up")
    loss = fmt(100.0 - 100.0 * N["LD_frac"], 2)
    text(ax, (xg, 0.5 * (ldd + ldm)), f"−{loss}%", direction=180.0, dist=7.0, fs=FS_SMALL)
    text(ax, (5600, 9.0), "not allowed: the stall speed\nwith flaps down exceeds 50 m/s", fs=FS_SMALL, backing=False)
    text(ax, (lim, 7.0), "stall limit", direction=180.0, dist=5.0, fs=FS_SMALL)
    assert lim < wc, "the stall requirement allows less wing loading than cruise wants"
    save_figure(fig, "p34-two-requirements")


def make_all():
    design_parameters()
    flap_area()
    wing_loading_classes()
    stall_speed()
    two_requirements()


# ===================================================================== printed values
def values():
    r = lambda k, s: record(PAGE, k, s)
    r("lbft2", fmt(LB_FT2, 5))
    # example 1
    r("m772", fmt(B772_MTOW_KG)); r("S772", fmt(B772_S_M2, 5)); r("g0", fmt(G0, 3))
    r("W772", fmt(N["W772"])); r("WS772", fmt(N["WS772"])); r("WS772_en", fmt(N["WS772_en"]))
    r("wl772", fmt(B772_WING_LOAD_KGM2, 5))
    r("wl772_N", fmt(B772_WING_LOAD_KGM2 * G0))
    close_to(B772_MTOW_KG / B772_S_M2, B772_WING_LOAD_KGM2, 0.01, "Jenkinson's wing load")
    # trends quoted in the text
    r("lr_lo", fmt(_row(LONG)[1], 3)); r("lr_hi", fmt(_row(LONG)[2], 3))
    r("sp_lo", fmt(_row(SAIL)[1], 1)); r("sp_hi", fmt(_row(SAIL)[2], 2))
    r("cm_lo", fmt(_row(MISSILE)[1], 3)); r("cm_hi", fmt(_row(MISSILE)[2], 3))
    r("solar_hi", fmt(_row(SOLAR)[2], 1))
    # example 2
    L = LIFTER
    r("L_W", fmt(L["W"])); r("L_Vs", fmt(L["V_stall"], 2)); r("L_clc", fmt(L["CLmax_clean"], 3))
    r("L_dcl", fmt(L["dcl_flap"], 3)); r("L_fl", fmt(L["flapped"], 2)); r("Ksw", fmt(N["K_sweep"], 2))
    r("dCL", fmt(N["dCL"])); r("CLf", fmt(N["CLmax_flaps"])); r("q_st", fmt(N["q_stall"], 6))
    r("WS_st", fmt(N["WS_stall"])); r("WS_cl", fmt(N["WS_clean"])); r("S_st", fmt(N["S_stall"]))
    r("S_cl", fmt(N["S_clean"])); r("WS_st_en", fmt(N["WS_stall_en"]))
    # example 3
    A = ALCM
    r("m_CD0", fmt(A["CD0"], 2)); r("m_K", fmt(A["K"], 2)); r("m_W", fmt(A["W_lb"]))
    r("m_a", fmt(A["a"], 5)); r("m_M", fmt(A["M"], 1));
    r("m_ratio", fmt(N["m_ratio"], 5)); r("m_CL", fmt(N["m_CL"])); r("m_V", fmt(N["m_V"], 5))
    r("m_q", fmt(N["m_q"])); r("m_WS", fmt(N["m_WS"], 5)); r("m_S", fmt(N["m_S"]))
    # example 4
    r("CD0", fmt(L["CD0"], 2)); r("AR", fmt(L["AR"], 3)); r("e", fmt(L["e"], 2))
    r("h_c", fmt(L["h_cruise"])); r("V_c", fmt(L["V_cruise"], 3))
    r("K", fmt(N["K"], 5)); r("CLs_ratio", fmt(N["CL_star_ratio"], 5)); r("CLs", fmt(N["CL_star"]))
    r("rho_c", fmt(N["rho_c"], 5)); r("q_c", fmt(N["q_c"])); r("WS_c", fmt(N["WS_cruise"]))
    r("CL_d", fmt(N["CL_design"], 3)); r("CD_d", fmt(N["CD_design"])); r("LD_d", fmt(N["LD_design"]))
    r("LD_max", fmt(N["LD_max"])); r("LD_pct", fmt(100.0 * N["LD_frac"], 3))
    # other numbers in the text
    r("lb_N", fmt(LB_N, 7)); r("ft_m", fmt(FT, 4)); r("rho_sl", fmt(RHO_SL, 5))
    r("ws772_round", fmt(N["WS772_en"], 3))
    r("cruise_high", fmt(WS_CRUISE_HIGH, 3))
    r("stol_lo", fmt(_row(STOL)[1], 2)); r("stol_hi", fmt(_row(STOL)[2], 2))
    r("clmax_777", fmt(CLMAX_T91["777-200"], 2)); r("clmax_u2", fmt(CLMAX_T91["U-2S"], 2))
    r("area_more", fmt(100.0 * (N["S_clean"] / N["S_stall"] - 1.0), 2))
    v10 = 0.9
    r("v10", fmt(100.0 * (1.0 - v10), 2)); r("ws19", fmt(100.0 * (1.0 - v10 ** 2), 2))
    r("ld_loss", fmt(100.0 - 100.0 * N["LD_frac"], 1))
    r("m_h", fmt(A["h_ft"], 3)); r("m_rho", fmt(A["rho"], 4))
    r("m_LD0", fmt(A["book_LD_start"], 2)); r("m_LD1", fmt(A["book_LD_end"], 2))
    r("m_bCL", fmt(A["book_CL"], 2)); r("m_bWS", fmt(A["book_WS"], 3)); r("m_bS", fmt(A["book_S"], 3))
    close_to(N["m_WS"] * A["book_CL"] / round(N["m_CL"], 4), A["book_WS"], 1.0, "the book's rounding explains its 319")
    r("m_tomahawk", fmt(A["tomahawk_lb"])); r("m_LDavg", fmt(A["book_LD_avg"], 2))
    assert A["book_LD_end"] < A["book_LD_avg"] < A["book_LD_start"], "the average lies between launch and end"
    # what the figures print
    r("WS_gain", fmt(N["WS_gain"]))
    r("WS_st_en3", fmt(N["WS_stall_en"], 3)); r("m_WS4", fmt(N["m_WS"], 4))
    r("ld_loss2", fmt(100.0 - 100.0 * N["LD_frac"], 2))
