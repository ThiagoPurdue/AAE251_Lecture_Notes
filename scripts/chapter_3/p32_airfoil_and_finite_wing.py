"""Page 3.2 Airfoil and Finite Wing: figures and printed values.

Run through the runner only:  python3 -B scripts/make_chapter_3_figures.py p32

Airfoil data: NACA 64(3)-618 and 64(3)-018 of NACA Report 824 (chapter_3/airfoil_data.py).
Worked examples (invented values):
  1. lift coefficient of a fighter, in English units;
  2. a model wing spanning a tunnel test section (NACA 64(3)-618 at 2 deg, R near 6 million);
  3. the wing of a twin-engine seaplane built with the same airfoil, aspect ratio 8, then 14 at the
     same wing area (so the chord and the Reynolds number fall).
Helpers written here (the shared modules lack them): _flight_panel (an airfoil on a climbing,
level or descending path), _extra_reading (a second reading on a line another reading drew),
_disc_beside (a numbered disc placed beside a drawn label).
"""
from chapter_3.common import *  # noqa: F401,F403
from chapter_3.airfoil_data import (read, curve, series, properties, naca_chart, draw_reading,
                                    CM_PER_CL, CMAC_PER_CD, CMAC_AXIS_GAP, RE_STYLE, AIRFOILS)
from chapter_3.drawing3 import (angle_mark, section_xy, airfoil_in_stream, downwash_construction,
                                wing_rear_view, spiral_vortex, disc, unit)
from chapter_1.diagrams import key_disc
from chapter_3 import aero
from matplotlib.patches import Polygon
import matplotlib.text

PAGE = "p32"
AF, SYM = "64-618", "64-018"
RE6 = 6.0e6
MINUS = "−"

# ---------------------------------------------------------------- worked example 1 (fighter, English units)
EX1 = dict(S=280.0, L=22000.0, V_kt=240.0, rho=aero.RHO_SL_EN)
# ---------------------------------------------------------------- worked example 2 (model wing in a tunnel)
EX2 = dict(c=1.2, V=72.0, alpha=2.0, rho=aero.RHO_SL, mu=aero.MU_SL)
# ---------------------------------------------------------------- worked example 3 (seaplane wing)
EX3 = dict(h=1500.0, V=48.0, c=2.3, AR=8.0, AR2=14.0, e=0.90, CL=0.55, a_lo=-2.0, a_hi=4.0)
# ---------------------------------------------------------------- figures
AOA_FIG = 8.0                         # deg, the angle of attack of the first figure (large enough to see)
FLIGHT_ALPHA = 10.0                   # deg, the angle of attack of the three flight paths
FLIGHT_GAMMA = 25.0                   # deg, climb and descent angles drawn
CP_ALPHAS = (-1.0, 2.0, 8.0)          # deg, the three angles of the moment figure
K_ANGLE = 12.0                        # the downwash construction draws its angles 12 times their size
TH_CLIMB_R, TH_CLIMB_LR, TH_CLIMB_OUT = 0.80, 0.92, 12.0  # climb theta: arc radius, label radius (data units), label angle beyond the chord line (deg)


def _r(x, nd):
    """x rounded to nd decimals, as printed (readings and printed intermediate values)."""
    return float(f"{x:.{nd}f}")


def _m(s):
    """A string with a typographic minus for figure text that is not math."""
    return s.replace("-", MINUS)


def _split_label(ax, which, first, second):
    """An axis label with two single-letter subscripts ("Drag coefficient, $c_d$ or $C_D$") written
    as two text pieces on one baseline, the first ending with "or". The kit's SVG check reads every
    small glyph of one text element as one run, so two subscripts in one label would read as a
    two-letter word subscript; in two elements each is a letter, as it is. Same place, size and
    reading direction as the axis label it replaces."""
    fig = ax.figure
    lab = ax.xaxis.label if which == "x" else ax.yaxis.label
    lab.set_text(first + " " + second)
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bb = lab.get_window_extent(rend)
    fs = lab.get_fontsize()
    rot = 0 if which == "x" else 90
    probe = fig.text(0, 0, first + " " + second, fontsize=fs, va="baseline", ha="left", rotation=rot,
                     rotation_mode="anchor")
    pb = probe.get_window_extent(rend)
    ax0 = fig.transFigure.transform((0, 0))
    if which == "x":                                     # baseline = top of the label - height above it
        base = bb.y1 - (pb.y1 - ax0[1])
        start = 0.5 * (bb.x0 + bb.x1) - 0.5 * pb.width
    else:                                                # rotated: the baseline is a vertical line
        base = bb.x1 - (ax0[0] - pb.x0)
        start = 0.5 * (bb.y0 + bb.y1) - 0.5 * pb.height
    probe.remove()
    lab.set_text("")
    inv = fig.transFigure.inverted()
    p1 = fig.text(0, 0, first + " ", fontsize=fs, va="baseline", ha="left", rotation=rot, rotation_mode="anchor")
    w1 = p1.get_window_extent(rend)
    if which == "x":
        p1.set_position(inv.transform((start, base)))
        fig.text(*inv.transform((start + w1.width, base)), second, fontsize=fs, va="baseline", ha="left")
    else:
        p1.set_position(inv.transform((base, start)))
        fig.text(*inv.transform((base, start + w1.height)), second, fontsize=fs, va="baseline", ha="left",
                 rotation=90, rotation_mode="anchor")


# ===================================================================== numbers of the examples
def ex1():
    d = dict(EX1)
    d["V"] = d["V_kt"] * KT_FPS
    d["q"] = float(aero.dynamic_pressure(d["rho"], _r(d["V"], 1)))
    d["CL"] = d["L"] / (_r(d["q"], 1) * d["S"])
    return d


def ex2():
    d = dict(EX2)
    d["Re"] = aero.reynolds(d["rho"], d["V"], d["c"], d["mu"])
    d["a_s"] = speed_of_sound(T_SL)
    d["M"] = d["V"] / _r(d["a_s"], 1)
    d["cl"] = _r(read(AF, "cl_alpha", RE6, d["alpha"]), 2)
    d["cm"] = _r(read(AF, "cm_alpha", RE6, d["alpha"]), 2)
    d["cd"] = _r(read(AF, "cd_cl", RE6, d["cl"]), 4)
    d["cmac"] = _r(read(AF, "cmac_cl", RE6, d["cl"]), 3)
    d["q"] = float(aero.dynamic_pressure(d["rho"], d["V"]))
    q = _r(d["q"], 1)
    d["Lp"] = q * d["c"] * d["cl"]
    d["Dp"] = q * d["c"] * d["cd"]
    d["c2"] = d["c"] ** 2
    d["Mp"] = q * d["c2"] * d["cm"]
    d["LD"] = d["cl"] / d["cd"]
    return d


def _zero_lift(airfoil=AF, Re=RE6):
    a = np.linspace(-6.0, 2.0, 80001)
    return float(a[np.argmin(np.abs(curve(airfoil, "cl_alpha", Re, x=a)[1]))])


def ex3():
    d = dict(EX3)
    T, p, rho = standard(d["h"])
    d["T"], d["rho"], d["mu"] = T, rho, float(aero.mu_sutherland(T))
    d["Re"] = aero.reynolds(_r(rho, 4), d["V"], d["c"], _r(d["mu"] * 1e5, 3) * 1e-5)
    # the longer wing keeps the wing area: chord c sqrt(AR/AR2), Reynolds number in proportion
    d["c2"] = d["c"] * math.sqrt(d["AR"] / d["AR2"])
    d["Re2"] = _r(d["Re"] / 1e6, 3) * 1e6 * _r(d["c2"], 3) / d["c"]
    d["cd_3"] = _r(read(AF, "cd_cl", 3.0e6, d["CL"]), 4)       # the 3 million curve, for the bound
    d["cl_lo"] = _r(read(AF, "cl_alpha", RE6, d["a_lo"]), 2)
    d["cl_hi"] = _r(read(AF, "cl_alpha", RE6, d["a_hi"]), 2)
    d["a0"] = _r((d["cl_hi"] - d["cl_lo"]) / (d["a_hi"] - d["a_lo"]), 3)
    d["aL0"] = _r(_zero_lift(), 1)
    d["cd"] = _r(read(AF, "cd_cl", RE6, d["CL"]), 4)
    for tag, AR in (("", d["AR"]), ("2", d["AR2"])):
        pea = math.pi * d["e"] * AR
        d["pea" + tag] = pea
        d["ratio" + tag] = aero.DEG_PER_RAD * d["a0"] / _r(pea, 2)
        d["den" + tag] = 1.0 + _r(d["ratio" + tag], 4)
        d["a" + tag] = d["a0"] / d["den" + tag]
        d["CLa" + tag] = d["CL"] / _r(d["a" + tag], 5)
        d["alpha" + tag] = _r(d["CLa" + tag], 3) + d["aL0"]
        d["ai" + tag] = aero.DEG_PER_RAD * d["CL"] / _r(pea, 2)
        d["aeff" + tag] = _r(d["alpha" + tag], 3) - _r(d["ai" + tag], 3)
        d["CDi" + tag] = d["CL"] ** 2 / _r(pea, 2)
        d["CD" + tag] = d["cd"] + _r(d["CDi" + tag], 5)
        d["LD" + tag] = d["CL"] / _r(d["CD" + tag], 5)
    d["cl_check"] = d["a0"] * (_r(d["aeff"], 3) - d["aL0"])
    d["LD_section"] = d["CL"] / d["cd"]
    d["CL2"] = d["CL"] ** 2
    return d


def cp_positions():
    """x_cp/c = 1/4 - c_m,c/4 / c_l at the three angles of the moment figure (small angles: the
    normal force taken equal to the lift)."""
    out = []
    for a in CP_ALPHAS:
        cl = read(AF, "cl_alpha", RE6, a)
        cm = read(AF, "cm_alpha", RE6, a)
        out.append(dict(alpha=a, cl=cl, cm=cm, xcp=0.25 - cm / cl))
    return out


# ===================================================================== figure 1: alpha, lift, drag, moment
def angle_of_attack():
    """Lesson: lift is perpendicular and drag parallel to the free stream, and alpha is measured
    from the free stream to the chord line."""
    fig, ax = canvas(6.5, xlim=(-2.45, 1.55), ylim=(-0.40, 0.98))
    g = airfoil_in_stream(ax, AOA_FIG, AF, 1.0, (0.0, 0.0), lift=0.72, drag=0.26, moment=None,
                          arc_r=1.10, ext=1.42, ref=1.42, alpha_label_r=1.27)
    moment_arrow(ax, g["c4"], 0.27, 35.0, 155.0, "moment, $M$", label_at=35.0)   # nose down: counterclockwise
    u = (g["le"] - g["te"]) / np.hypot(*(g["le"] - g["te"]))
    p = g["le"] + u * 0.55
    callout(ax, p, "chord line", at=(p[0], p[1] + 0.30), ha="center", gap=0.5)
    point(ax, g["c4"], None, ms=4.5)
    callout(ax, g["c4"], "quarter chord, $c$/4", at=(0.22, -0.30), ha="left")
    ang = math.degrees(math.atan2(*(g["le"] - g["te"])[::-1]))
    close_to(ang, 180.0 - AOA_FIG, 1e-9, "chord line drawn at alpha to the free stream")
    trim_canvas(fig)
    save_figure(fig, "p32-angle-of-attack")


# ===================================================================== figure 2: alpha is not the pitch
def _flight_panel(ax, gamma, name):
    """An airfoil flying a path at gamma (deg, + climb) at angle of attack FLIGHT_ALPHA. The free
    stream comes from ahead along the path, so the air moves along -gamma (left to right). The
    chord sits FLIGHT_ALPHA nose up from the free stream and theta = gamma + alpha nose up from the
    horizon. Lines through the leading edge: horizon (gray dashed), free stream (gray solid, with
    the velocity arrow on it), chord line (black dashed). Arcs: alpha (free stream to chord) and
    theta (horizon to chord). Returns theta."""
    al = FLIGHT_ALPHA
    theta = gamma + al
    xy, le, te = section_xy(AF, 1.0, theta, (0.0, 0.0))
    ax.add_patch(opaque(Polygon(xy, closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=3)))
    uc = (le - te) / np.hypot(*(le - te))               # along the chord, toward the nose
    ax.plot([le[0] + uc[0] * 1.55, le[0]], [le[1] + uc[1] * 1.55, le[1]], **line_kw("boundary"), zorder=3.5)
    uf = unit(-gamma)                                   # the direction the air moves
    f0 = le - uf * 2.10
    ax.plot([f0[0], le[0]], [f0[1], le[1]], **line_kw("reference"), zorder=1.5)
    t0 = f0 - uf * 0.78
    kind_arrow(ax, t0, t0 + uf * 0.62, "velocity", None)
    if gamma:
        text(ax, t0, r"free stream, $V_\infty$", direction=180.0 - gamma, dist=5, color=BLUE)
    else:
        text(ax, t0 + uf * 0.31, r"free stream, $V_\infty$", direction=-90.0, dist=9, color=BLUE)
    ax.plot([le[0] - 1.95, le[0] + 1.25], [le[1], le[1]], color=GRAY, lw=LW_THIN, ls=(0, (6.0, 3.0)), zorder=1)
    text(ax, (le[0] + 1.30, le[1]), "horizon", direction=0, dist=4, color=GRAY)
    # in the descent the alpha wedge lies inside the gamma wedge: alpha's arc and label move in
    ra, rl = (1.60, 1.80) if gamma >= 0 else (1.42, 1.62)
    angle_mark(ax, le, 180.0 - theta, 180.0 - gamma, ra, r"$\alpha$", stated=al, label_r=rl)
    if abs(gamma) > 1e-9:                               # level flight: theta = alpha and gamma = 0, one arc
        # theta: horizon to chord. In the climb the gamma wedge lies inside the theta wedge and the
        # alpha wedge is too narrow for a second label, so the theta label sits at the chord end of
        # its arc, just beyond the chord line (never in the gamma wedge); in the descent it sits
        # below the horizon, in its own wedge.
        if gamma > 0:
            angle_mark(ax, le, 180.0 - theta, 180.0, TH_CLIMB_R, r"$\theta$", stated=abs(theta),
                       label_r=TH_CLIMB_LR, label_angle=180.0 - theta - TH_CLIMB_OUT)
            assert 180.0 - theta - TH_CLIMB_OUT < 180.0 - gamma, "climb: theta label outside the gamma wedge"
        else:
            angle_mark(ax, le, 180.0 - theta, 180.0, 0.72, r"$\theta$", stated=abs(theta),
                       label_r=1.25, label_angle=180.0 - 0.5 * theta)
        # gamma: horizon to the flight path (the free-stream line), outside the other arcs
        angle_mark(ax, le, 180.0 - gamma, 180.0, 1.90, r"$\gamma$", stated=abs(gamma), label_r=2.07)
    text(ax, (le[0] + 1.25, le[1] + 0.27), name, ha="left", va="center", fontweight="bold")
    nose = (math.degrees(math.atan2(uc[1], uc[0])) + 360.0) % 360.0
    close_to(nose, 180.0 - theta, 1e-9, "chord pitched theta above the horizon")
    close_to(theta - gamma, al, 1e-12, "alpha = pitch - flight-path angle")
    return theta


def alpha_not_horizon():
    """Lesson: the same angle of attack on a climb, in level flight and in a descent; the angle of
    attack is measured from the free stream, not from the horizon (the pitch angle differs)."""
    rows = ((FLIGHT_GAMMA, "climb"), (0.0, "level flight"), (-FLIGHT_GAMMA, "descent"))
    lims = ((-0.74, 1.30), (-0.30, 0.40), (-1.30, 0.40))
    fig, axs = new_axes(6.5, 4.51, nrows=3, gridspec_kw=dict(height_ratios=[b - a for a, b in lims]))
    fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0, hspace=0.0)
    for ax, (g, name), lim in zip(axs, rows, lims):
        ax.set_xlim(-4.35, 2.05); ax.set_ylim(*lim)
        ax.set_xticks([]); ax.set_yticks([])
        _flight_panel(ax, g, name)
        # the whole section lies inside its panel, 8 points clear of the edges
        xy = section_xy(AF, 1.0, g + FLIGHT_ALPHA, (0.0, 0.0))[0]
        m8 = pt(ax, 8.0)
        assert xy[:, 1].min() - m8 > lim[0] and xy[:, 1].max() + m8 < lim[1], f"{name}: section inside its panel"
    save_figure(fig, "p32-alpha-not-horizon")


# ===================================================================== figure 3: center of pressure and a.c.
def moment_and_ac():
    """Lesson: the center of pressure moves as alpha changes; about the aerodynamic center the
    moment stays the same, so the lift there plus one constant moment describes the airfoil."""
    cps = cp_positions()
    p = properties(AF, RE6)
    xac = p["x_ac"]
    fig, axs = new_axes(6.5, 3.62, ncols=2)
    fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=0.91, wspace=0.08)
    sc = 0.66                                           # drawn length of the lift arrow per unit c_l
    xy, le, te = section_xy(AF, 1.0, 0.0, (0.25, 0.0))
    for ax in axs:
        ax.set_xlim(-0.08, 1.08); ax.set_ylim(-0.40, 1.04)
        ax.set_xticks([]); ax.set_yticks([])
        ax.add_patch(opaque(Polygon(xy, closed=True, fc=PART_FILL, ec=INK, lw=LW_OUTLINE, zorder=3)))
        ax.plot([0.0, 1.0], [0.0, 0.0], **line_kw("boundary"), zorder=3.5)
    ax = axs[0]
    for c in cps:
        P = np.array([c["xcp"], 0.0])
        tip = P + np.array([0.0, sc * c["cl"]])
        kind_arrow(ax, P, tip, "force", None)
        point(ax, P, None, ms=4.0)
        text(ax, tip, r"$\alpha$ = " + _m(fmt_dec(c["alpha"], 0)) + "°, at " + fmt(c["xcp"], 2) + "$c$",
             direction=90 if c["alpha"] > 5 else 0, dist=3 if c["alpha"] > 5 else 6)
        close_to(float(np.hypot(*(tip - P))) / sc, c["cl"], 1e-12, "arrow length in proportion to c_l")
    # a chord scale under the section, so the positions can be read
    ys = -0.15
    ax.plot([0.0, 1.0], [ys, ys], color=INK, lw=0.8, zorder=2)
    for xt in (0.0, 0.25, 0.5, 0.75, 1.0):
        ax.plot([xt, xt], [ys, ys + 0.025], color=INK, lw=0.8, zorder=2)
        text(ax, (xt, ys), f"{xt:g}", direction=-90, dist=3, fs=FS_SMALL)
    text(ax, (1.0, ys), "$x/c$", direction=0, dist=12, fs=FS_SMALL)
    ax.set_title("lift at the center of pressure", fontsize=FS_LABEL, pad=2)
    text(ax, (0.5, -0.30), "it moves as " + r"$\alpha$" + " changes", direction=-90, dist=2)
    ax = axs[1]
    P = np.array([xac, 0.0])
    tip = P + np.array([0.0, sc * cps[1]["cl"]])
    kind_arrow(ax, P, tip, "force", None)
    point(ax, P, None, ms=4.0)
    text(ax, tip, "lift", direction=90, dist=3)
    moment_arrow(ax, P, 0.22, 50.0, 140.0, None)
    text(ax, P + 0.22 * unit(50.0), r"$M_\mathrm{ac}$", direction=35, dist=7)
    callout(ax, P, "aerodynamic center, " + fmt(xac, 3) + "$c$", at=(0.42, -0.17), ha="left")
    text(ax, (0.5, -0.30), r"$M_\mathrm{ac}$ the same at every $\alpha$", direction=-90, dist=2)
    ax.set_title("lift at the aerodynamic center", fontsize=FS_LABEL, pad=2)
    assert cps[0]["xcp"] > cps[1]["xcp"] > cps[2]["xcp"] > xac, "the center of pressure moves forward as c_l grows"
    save_figure(fig, "p32-moment-and-ac")


# ===================================================================== figure 4: the redrawn NACA chart
def _extra_reading(fig, out, curve_name, x, n, sy, side):
    """A reading on a curve whose vertical line another reading has drawn: a dot on the curve and a
    dashed line across to the moment scale it is read on, with a small arrowhead at that scale and
    the numbered disc just above the line near its end. side="left": the scale is the outer axis
    out["sec_left"] outside the panel; the line runs on through the inner c_l scale and is broken
    only behind the c_l tick label at its height (2 pt clear each side), so the eye follows one line
    from the curve to the moment scale. side="right": the axis on the panel's right edge."""
    from figkit import arrow, rides_on
    ax = out["left"] if curve_name in ("cl_alpha", "cm_alpha") else out["right"]
    y = read(AF, curve_name, RE6, x)
    yp = y * sy
    x0, x1 = ax.get_xlim()
    kx, ky = data_per_pt(ax)
    fx = lambda f: x0 + f * (x1 - x0)                   # axes fraction -> data x
    kw = dict(color=INK, lw=LW_THIN, ls=(0, (3.0, 2.0)), zorder=5, clip_on=False)
    if side == "left":
        xe = fx(-0.42) + 1.5 * kx                        # the outer c_m,c/4 axis line
        fig.canvas.draw()
        rend = fig.canvas.get_renderer()
        inv = ax.transData.inverted()
        hit = []
        for t in ax.get_yticklabels():
            if t.get_text() and t.get_visible():
                bb = t.get_window_extent(rend)
                (bx0, by0), (bx1, by1) = inv.transform((bb.x0, bb.y0)), inv.transform((bb.x1, bb.y1))
                if by0 < yp < by1:
                    hit.append((bx0, bx1))
        assert len(hit) == 1, "one c_l tick label at the height of the reading"
        bx0, bx1 = hit[0]
        ax.plot([bx1 + 2.0 * kx, x], [yp, yp], **kw)
        ln = ax.plot([xe + 6.0 * kx, bx0 - 2.0 * kx], [yp, yp], **kw)[0]
        assert xe + 6.0 * kx < bx0 - 2.0 * kx, "the line reaches the moment scale left of the tick label"
        hd = arrow(ax, (xe + 7.0 * kx, yp), (xe, yp), color=INK, lw=LW_THIN, head="small", zorder=5)
        dx = xe + 12.0 * kx
    else:
        xe = fx(1.0 + CMAC_AXIS_GAP) - 1.5 * kx            # the c_m,ac axis line, set off the panel
        ln = ax.plot([x, xe - 6.0 * kx], [yp, yp], **kw)[0]
        hd = arrow(ax, (xe - 7.0 * kx, yp), (xe, yp), color=INK, lw=LW_THIN, head="small", zorder=5)
        dx = xe - 12.0 * kx
    hd.set_clip_on(False)
    rides_on(hd, ln)
    ax.plot([x], [yp], "o", color=INK, ms=3.6, zorder=6)
    disc(ax, (dx, yp + (11.0 if side == "left" else -11.0) * ky), n).set_clip_on(False)   # outside the panel
    xc, yc = curve(AF, curve_name, RE6, x=[x])
    close_to(float(yc[0]) * sy, yp, 1e-12, "the reading lies on the drawn curve")
    return y


def airfoil_chart():
    """Lesson: how to read the NACA chart: alpha -> c_l, alpha -> c_m,c/4, c_l -> c_d, c_l -> c_m,ac,
    on the curve of the right Reynolds number (worked example 2)."""
    d = ex2()
    fig, out = naca_chart(AF, reading=[dict(curve="cl_alpha", re=RE6, x=d["alpha"], n=1),
                                       dict(curve="cd_cl", re=RE6, x=d["cl"], n=3)])
    _extra_reading(fig, out, "cm_alpha", d["alpha"], 2, 1.0 / CM_PER_CL, "left")
    _extra_reading(fig, out, "cmac_cl", d["cl"], 4, 1.0 / CMAC_PER_CD, "right")
    close_to(out["readings"][0]["y"], read(AF, "cl_alpha", RE6, d["alpha"]), 1e-12, "reading 1")
    save_figure(fig, "p32-airfoil-chart")


# ===================================================================== figure 5: symmetric and cambered
def symmetric_cambered():
    """Lesson: camber shifts the lift curve to the left (zero lift at a negative angle) without
    changing its slope; the symmetric section has zero lift at zero angle."""
    fig, ax = data_axes(6.5, 3.4)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.15, top=0.97)
    ax.set_xlim(-10, 20); ax.set_ylim(-1.0, 1.8)
    ax.set_xticks(range(-8, 21, 4)); ax.set_yticks([-0.8, -0.4, 0, 0.4, 0.8, 1.2, 1.6])
    ax.axhline(0.0, color=INK, lw=0.8, zorder=1)
    out = {}
    for k, role, mk in ((AF, 0, "s"), (SYM, 3, "o")):     # symmetric: series 3, as on page 3.3
        a, cl = curve(k, "cl_alpha", RE6)
        m = (a >= -10) & (a <= 20)
        ax.plot(a[m], cl[m], **line_kw(role), zorder=3)
        xs, ys = series(k, "cl_alpha", RE6)
        mm = (xs >= -10) & (xs <= 20)
        ax.plot(xs[mm], ys[mm], ls="none", marker=mk, ms=4.4, mfc="white", mec=line_kw(role)["color"], mew=1.0, zorder=3.5)
        out[k] = _zero_lift(k)
    ax.plot([out[AF]], [0.0], "o", color=INK, ms=6, zorder=6)
    ax.plot([out[SYM]], [0.0], "o", color=INK, ms=6, zorder=6)
    callout(ax, (out[AF], 0.0), r"$\alpha_{L=0}$ ≈ " + _m(fmt_dec(out[AF], 1)) + "°", at=(-9.4, 0.30), ha="left")
    callout(ax, (out[SYM], 0.0), r"$\alpha_{L=0}$ = 0°", at=(3.0, -0.55), ha="left")
    text(ax, (-3.0, 1.05), AIRFOILS[AF]["name"] + ", cambered")
    text(ax, (15.2, 0.60), AIRFOILS[SYM]["name"] + ", symmetric", color=text_color(3))
    ax.set_xlabel(r"Section angle of attack, $\alpha$, deg")
    ax.set_ylabel(r"Section lift coefficient, $c_l$")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}".replace("-", MINUS)))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}".replace("-", MINUS)))
    # same slope: the two lines differ by a shift along alpha
    s1 = (read(AF, "cl_alpha", RE6, 4.0) - read(AF, "cl_alpha", RE6, -2.0)) / 6.0
    s2 = (read(SYM, "cl_alpha", RE6, 4.0) - read(SYM, "cl_alpha", RE6, -2.0)) / 6.0
    assert abs(s1 - s2) / s1 < 0.06 and out[AF] < -3.0 and abs(out[SYM]) < 0.2
    save_figure(fig, "p32-symmetric-cambered")
    return out


# ===================================================================== figure 6: tip vortices
def tip_vortices():
    """Lesson, in numbered order: (1) higher pressure below the wing pushes air (2) round each tip
    toward the lower pressure above, (3) the air rolls up into a tip vortex just inboard of the
    tip, and (4) the two vortices push the air down between them (downwash) and up outside them
    (upwash)."""
    fig, ax = canvas(6.5, xlim=(-23.5, 23.5), ylim=(-4.6, 14.0))
    g = wing_rear_view(ax, htail=True)
    tz = g["tip_R"][1]
    # each tip: one streamline that starts under the wing inboard of the tip, passes under the tip,
    # rises outboard of it and curls over the top into the vortex core (vortex size not to scale)
    lines = {}
    for side, sense in (("R", "ccw"), ("L", "cw")):
        tip = g["tip_" + side]
        k = 1.0 if side == "R" else -1.0
        core = tip + np.array([-0.6 * k, 2.0])
        start = -115.0 if side == "R" else -65.0
        lines[side] = spiral_vortex(ax, core, 0.5, 3.4, turns=1.0, sense=sense, start_deg=start, lw=1.3,
                                    color=BLUE, inward=True)
        xs, ys = lines[side].get_data()
        assert ys[0] < tip[1] - 0.5 and k * (xs[0] - tip[0]) < 0, "the streamline starts under the wing, inboard"
        assert max(k * (xs - tip[0])) > 1.0, "it passes outboard of the tip"
        # a head on the way round the tip, pointing along the streamline (outboard and up)
        sl = np.r_[0.0, np.cumsum(np.hypot(np.diff(xs), np.diff(ys)))]
        i1 = int(np.searchsorted(sl, 0.24 * sl[-1])); i0 = int(np.searchsorted(sl, sl[i1] - 0.9))
        rides_on(arrow(ax, (xs[i0], ys[i0]), (xs[i1], ys[i1]), color=BLUE, lw=1.3, head="normal", zorder=6),
                 lines[side])
        assert k * (xs[i1] - xs[i0]) > 0, "the head points outboard under the tip"
    for y in (-13.0, -8.0, -2.7, 2.7, 8.0, 13.0):           # elliptic lift: the same downwash along the span
        kind_arrow(ax, (y, 0.2), (y, -1.7), "velocity", None)
    for y in (-21.3, 21.3):
        kind_arrow(ax, (y, tz - 1.6), (y, tz + 0.4), "velocity", None)
    text(ax, (10.5, -1.9), "downwash", direction=-90, dist=4, color=BLUE)
    # one "upwash" label; the arrow outside the right tip is the same flow (seven labels in all)
    text(ax, (-21.3, tz - 1.6), "upwash", direction=-90, dist=4, color=BLUE)
    callout(ax, (9.0, 3.62), "lower pressure\nabove the wing", at=(8.6, 8.1), ha="center")
    callout(ax, (-10.5, 2.9), "higher pressure below the wing", at=(-10.5, -3.4), ha="center")
    callout(ax, g["tip_R"] + np.array([-0.6, -1.45]), "flow around\nthe tip", at=(18.2, -0.55), ha="center")
    text(ax, g["tip_R"] + np.array([-0.6, 5.5]), "right tip vortex", direction=90, dist=4)
    text(ax, g["tip_L"] + np.array([0.6, 5.5]), "left tip vortex", direction=90, dist=4)
    fig.canvas.draw()
    _disc_beside(ax, "higher pressure below the wing", 1, "left")
    _disc_beside(ax, "flow around\nthe tip", 2, "left")
    _disc_beside(ax, "right tip vortex", 3, "left")
    _disc_beside(ax, "downwash", 4, "right")
    trim_canvas(fig)
    save_figure(fig, "p32-tip-vortices")


# ===================================================================== figure 7: the downwash construction
def _disc_beside(ax, label, n, side, gap=3.0, r=7.5):
    """The numbered disc just left or right of the drawn label whose text is `label` (the steps of
    the construction are numbered as in the text). Equal-aspect axes."""
    fig = ax.figure
    rend = fig.canvas.get_renderer()
    hits = [t for t in ax.texts if t.get_text() == label]
    assert len(hits) == 1, f"one label {label!r} on the figure"
    # the box of the text alone: an Annotation's own window extent also takes in its leader line
    bb = matplotlib.text.Text.get_window_extent(hits[0], rend)
    inv = ax.transData.inverted()
    (x0, y0), (x1, y1) = inv.transform((bb.x0, bb.y0)), inv.transform((bb.x1, bb.y1))
    k = pt(ax, gap + r)
    x = x0 - k if side == "left" else x1 + k
    nl = label.count("\n") + 1                          # on the first line of a label of several lines
    yc = y1 - 0.5 * (y1 - y0) / nl
    key_disc(ax, (x, yc), n, r=r)
    # the disc sits on its label's (first) line, beside the text and clear of it
    assert y1 - (y1 - y0) / nl - 1e-9 <= yc <= y1 + 1e-9, f"disc {n} on the line of {label!r}"
    edge = x + pt(ax, r) if side == "left" else x - pt(ax, r)
    assert abs(abs(edge - (x0 if side == "left" else x1)) - pt(ax, gap)) < pt(ax, 0.5), f"disc {n} beside {label!r}"
def downwash_vectors():
    """Lesson: downwash tilts the local relative wind down by alpha_i, so the wing works at the smaller
    alpha_eff and its lift, perpendicular to the local wind, tilts back; the backward part is D_i."""
    d = ex3()
    alpha, ai = d["alpha"], d["ai"]
    fig, ax = canvas(6.5, xlim=(-9.2, 2.6), ylim=(-1.9, 3.2))
    VL = 3.9
    g = downwash_construction(ax, alpha, ai, k=K_ANGLE, V_len=VL, F_len=2.7, lead=0.9, alpha_at="downstream")
    close_to(g["A"], K_ANGLE * alpha, 1e-12, "alpha drawn k times its size")
    close_to(g["Ai"], K_ANGLE * ai, 1e-12, "alpha_i drawn k times its size")
    fig.canvas.draw()
    # the numbers of the steps of the text, one beside each thing the step draws
    _disc_beside(ax, r"free stream, $V_\infty$", 1, "left")
    _disc_beside(ax, r"$\alpha$", 1, "left")
    _disc_beside(ax, "downwash, $w$", 2, "left")
    _disc_beside(ax, "local relative wind", 3, "left")
    _disc_beside(ax, r"$\alpha_\mathrm{eff}$", 4, "left")
    _disc_beside(ax, r"$\alpha_i$", 4, "left")
    _disc_beside(ax, "local lift", 5, "right")
    _disc_beside(ax, "lift, $L$", 6, "left")
    _disc_beside(ax, r"induced drag, $D_i$", 6, "right")
    trim_canvas(fig)
    save_figure(fig, "p32-downwash-vectors")
    return g


# ===================================================================== figure 8: lift curves
def lift_curves():
    """Lesson: the finite wing's lift curve has the same zero-lift angle and a smaller slope than the
    airfoil's; at one C_L the wing needs alpha_i more angle of attack."""
    d = ex3()
    fig, ax = data_axes(6.5, 3.6)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.14, top=0.97)
    ax.set_xlim(-6, 10); ax.set_ylim(-0.2, 1.3)
    ax.set_xticks(range(-6, 11, 2)); ax.set_yticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2])
    fm = plt.FuncFormatter(lambda v, _: f"{v:g}".replace("-", MINUS))
    ax.xaxis.set_major_formatter(fm); ax.yaxis.set_major_formatter(fm)
    xs, ys = series(AF, "cl_alpha", RE6)
    m = (xs >= -6) & (xs <= 10)
    ax.plot(xs[m], ys[m], ls="none", marker="s", ms=4.4, mfc="white", mec=INK, mew=1.0, zorder=3.5)
    aL0, a0 = d["aL0"], d["a0"]
    A_END = 6.0                          # the straight lines stop where the measured curve starts to bend
    a = np.linspace(aL0 - 1.5, A_END, 50)
    ax.plot(a, a0 * (a - aL0), **line_kw(0), zorder=3)
    ax.plot(a, d["a"] * (a - aL0), **line_kw(2), zorder=3)
    ax.plot(a, d["a2"] * (a - aL0), **line_kw(1), zorder=3)
    for slope, role, lab in ((d["a2"], 1, "wing, $AR$ = 14"), (d["a"], 2, "wing, $AR$ = 8")):
        text(ax, (A_END, slope * (A_END - aL0)), lab, direction=22 if role == 1 else -22, dist=6,
             color=text_color(role))
    ax.axhline(0.0, color=INK, lw=0.8, zorder=1)
    CL = d["CL"]
    ax.plot([-6, d["alpha"]], [CL, CL], **line_kw("reference"), zorder=2)
    ax.plot([d["aeff"]], [CL], "o", color=INK, ms=5, zorder=6)
    ax.plot([d["alpha"]], [CL], "o", color=INK, ms=5, zorder=6)
    ax.plot([d["alpha2"]], [CL], "o", color=INK, ms=5, zorder=6)
    # the example's angles beside their dots, where no line passes: airfoil up-left, AR 8 down-right
    text(ax, (d["aeff"], CL), r"$\alpha$ = " + fmt(d["aeff"], 3) + "°", direction=150, dist=6, fs=FS_SMALL)
    text(ax, (d["alpha"], CL), r"$\alpha$ = " + fmt(d["alpha"], 3) + "°", direction=-30, dist=6, fs=FS_SMALL)
    dimension(ax, (d["aeff"], CL), (d["alpha"], CL), None, offset=0.25, extension=True)
    text(ax, (0.5 * (d["aeff"] + d["alpha"]), CL + 0.25), r"$\alpha_i$ = " + fmt(d["ai"], 3) + "°", direction=90, dist=10)
    ax.plot([aL0], [0.0], "o", color=INK, ms=5, zorder=6)
    callout(ax, (aL0, 0.0), r"same $\alpha_{L=0}$", at=(-2.4, -0.12), ha="left")
    text(ax, (A_END, a0 * (A_END - aL0)), "airfoil, $a_0$", direction=125, dist=8)
    text(ax, (-5.7, CL), "$C_L$ = " + fmt_dec(CL, 2), direction=90, dist=3, ha="left")
    ax.set_xlabel(r"Angle of attack, $\alpha$, deg")
    _split_label(ax, "y", "Lift coefficient, $c_l$ or", "$C_L$")
    assert d["a2"] < a0 and d["a"] < d["a2"], "slope falls with aspect ratio"
    close_to(d["alpha"] - d["aeff"], d["ai"], 2e-3, "the horizontal gap at C_L is alpha_i")
    save_figure(fig, "p32-lift-curves")


# ===================================================================== figure 9: drag of the wing
def induced_drag_ar():
    """Lesson: the wing's drag coefficient is the section drag plus C_L^2/(pi e AR); the gap above the
    airfoil curve is the induced drag, smaller at the larger aspect ratio."""
    d = ex3()
    fig, ax = data_axes(6.5, 4.0)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.14, top=0.97)
    c = np.linspace(-0.2, 1.0, 300)
    cd = curve(AF, "cd_cl", RE6, x=c)[1]
    ax.plot(c, cd, **line_kw(0), zorder=3)
    for AR, role in ((d["AR"], 2), (d["AR2"], 1)):
        ax.plot(c, cd + aero.induced_drag_coef(c, AR, d["e"]), **line_kw(role), zorder=3)
    ax.set_xlim(-0.2, 1.0); ax.set_ylim(0, 0.04)
    ax.set_xticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0]); ax.set_yticks([0, 0.01, 0.02, 0.03, 0.04])
    fm = plt.FuncFormatter(lambda v, _: f"{v:g}".replace("-", MINUS))
    ax.xaxis.set_major_formatter(fm)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.2f}" if v else "0"))
    CL = d["CL"]
    for y in (d["cd"], d["CD2"], d["CD"]):
        ax.plot([CL], [y], "o", color=INK, ms=5, zorder=6)
    dimension(ax, (CL, d["cd"]), (CL, d["CD"]), None, offset=0.0, extension=False)
    text(ax, (CL, 0.0083), r"$C_{D,i}$ = " + fmt(d["CDi"], 3), direction=0, dist=10)
    text(ax, (CL, d["cd"]), fmt_dec(d["cd"], 4), direction=-90, dist=7, fs=FS_SMALL)
    text(ax, (CL, d["CD"]), fmt_dec(d["CD"], 4), direction=135, dist=10, fs=FS_SMALL)
    text(ax, (CL, d["CD2"]), fmt_dec(d["CD2"], 4), direction=-20, dist=11, fs=FS_SMALL)
    label_curve(ax, c, cd, 0.30, "airfoil, $c_d$", 0, offset=(0, -11))
    text(ax, (0.995, 0.016), "wing, $AR$ = 14", ha="right", color=text_color(1))
    label_curve(ax, c, cd + aero.induced_drag_coef(c, d["AR"], d["e"]), 0.80, "wing, $AR$ = 8", 2, offset=(-44, 8))
    _split_label(ax, "x", "Lift coefficient, $c_l$ or", "$C_L$")
    _split_label(ax, "y", "Drag coefficient, $c_d$ or", "$C_D$")
    close_to(float(np.interp(CL, c, cd + aero.induced_drag_coef(c, d["AR"], d["e"]))) - float(np.interp(CL, c, cd)),
             float(aero.induced_drag_coef(CL, d["AR"], d["e"])), 1e-6, "the gap is C_D,i")
    save_figure(fig, "p32-induced-drag-ar")


# ===================================================================== registry
def make_all():
    angle_of_attack()
    alpha_not_horizon()
    moment_and_ac()
    airfoil_chart()
    symmetric_cambered()
    tip_vortices()
    downwash_vectors()
    lift_curves()
    induced_drag_ar()


def values():
    R = lambda k, t: record(PAGE, k, t)
    # ---- the two sections, from the chart data
    p6 = properties(AF, RE6)
    R("x_ac_618", fmt(p6["x_ac"], 3))
    R("cmac_618", fmt(p6["cm_ac"], 2))
    R("aL0_618", fmt_dec(_zero_lift(), 1))
    for Re, k in ((3.0e6, "3"), (6.0e6, "6"), (9.0e6, "9")):
        R("clmax_618_" + k, fmt_dec(properties(AF, Re)["cl_max"], 2))
        R("cdmin_618_" + k, fmt(properties(AF, Re)["cd_min"], 2))
    # slopes as the page measures them: two readings, at -2 and 4 deg, each to two decimals
    s1 = (_r(read(AF, "cl_alpha", RE6, 4.0), 2) - _r(read(AF, "cl_alpha", RE6, -2.0), 2)) / 6.0
    s2 = (_r(read(SYM, "cl_alpha", RE6, 4.0), 2) - _r(read(SYM, "cl_alpha", RE6, -2.0), 2)) / 6.0
    R("slope_618", fmt_dec(s1, 3)); R("slope_018", fmt_dec(s2, 3))
    R("cl0_618", fmt_dec(read(AF, "cl_alpha", RE6, 0.0), 2))
    R("clmax_018_6", fmt_dec(properties(SYM, RE6)["cl_max"], 2))
    # ---- center of pressure
    for c in cp_positions():
        t = fmt_dec(c["alpha"], 0)
        R("cp_cl_" + t, fmt_dec(c["cl"], 2)); R("cp_cm_" + t, fmt_dec(c["cm"], 3, minus=MINUS)); R("cp_x_" + t, fmt(c["xcp"], 2))
    # ---- example 1
    d = ex1()
    R("e1_S", fmt(d["S"], 3)); R("e1_L", fmt(d["L"], 5)); R("e1_Vkt", fmt(d["V_kt"], 3))
    R("e1_kt", fmt(KT_FPS, 5)); R("e1_V", fmt_dec(d["V"], 1)); R("e1_rho", fmt(d["rho"], 4))
    R("e1_q", fmt_dec(d["q"], 1)); R("e1_CL", fmt(d["CL"], 4))
    R("e1_V2", fmt(_r(d["V"], 1) ** 2, 6)); R("e1_qS", fmt(_r(d["q"], 1) * d["S"], 5))
    # ---- example 2
    d = ex2()
    R("e2_c", fmt_dec(d["c"], 1)); R("e2_V", fmt(d["V"], 2)); R("e2_alpha", fmt(d["alpha"], 1))
    R("e2_rho", fmt_dec(d["rho"], 4)); R("e2_mu", fmt(d["mu"] * 1e5, 4))
    R("e2_Re", fmt(d["Re"] / 1e6, 4)); R("e2_as", fmt_dec(d["a_s"], 1)); R("e2_M", fmt(d["M"], 4))
    R("e2_cl", fmt_dec(d["cl"], 2)); R("e2_cm", fmt_dec(d["cm"], 2)); R("e2_cd", fmt_dec(d["cd"], 4))
    R("e2_cmac", fmt_dec(d["cmac"], 3))
    R("e2_q", fmt_dec(d["q"], 1)); R("e2_Lp", fmt(d["Lp"], 4)); R("e2_Dp", fmt(d["Dp"], 4))
    R("e2_c2", fmt_dec(d["c2"], 2)); R("e2_Mp", fmt(d["Mp"], 4)); R("e2_LD", fmt(d["LD"], 4))
    # ---- example 3
    d = ex3()
    R("e3_h", fmt(d["h"], 4)); R("e3_V", fmt(d["V"], 2)); R("e3_c", fmt_dec(d["c"], 1))
    R("e3_AR", fmt(d["AR"], 1)); R("e3_AR2", fmt(d["AR2"], 2)); R("e3_e", fmt_dec(d["e"], 2))
    R("e3_CL", fmt_dec(d["CL"], 2)); R("e3_T", fmt_dec(d["T"], 2))
    R("e3_rho", fmt_dec(d["rho"], 4)); R("e3_mu", fmt(d["mu"] * 1e5, 4)); R("e3_Re", fmt(d["Re"] / 1e6, 4))
    R("e3_clhi", fmt_dec(d["cl_hi"], 2)); R("e3_cllo", fmt_dec(d["cl_lo"], 2))
    R("e3_ahi", fmt(d["a_hi"], 1)); R("e3_alo", fmt(d["a_lo"], 1))
    R("e3_a0", fmt_dec(d["a0"], 3)); R("e3_aL0", fmt_dec(d["aL0"], 1)); R("e3_cd", fmt_dec(d["cd"], 4))
    for tag in ("", "2"):
        R("e3_pea" + tag, fmt_dec(d["pea" + tag], 2)); R("e3_ratio" + tag, fmt_dec(d["ratio" + tag], 4))
        R("e3_den" + tag, fmt_dec(d["den" + tag], 4)); R("e3_a" + tag, fmt_dec(d["a" + tag], 5))
        R("e3_CLa" + tag, fmt_dec(d["CLa" + tag], 3)); R("e3_alpha" + tag, fmt_dec(d["alpha" + tag], 3))
        R("e3_ai" + tag, fmt_dec(d["ai" + tag], 3)); R("e3_aeff" + tag, fmt_dec(d["aeff" + tag], 3))
        R("e3_CDi" + tag, fmt_dec(d["CDi" + tag], 5)); R("e3_CD" + tag, fmt_dec(d["CD" + tag], 5))
        R("e3_LD" + tag, fmt(d["LD" + tag], 4))
    R("e3_clcheck", fmt_dec(d["cl_check"], 4)); R("e3_LDsec", fmt(d["LD_section"], 4))
    R("e3_c2", fmt_dec(d["c2"], 3)); R("e3_Re2", fmt(d["Re2"] / 1e6, 4)); R("e3_cd3", fmt_dec(d["cd_3"], 4))
    R("e3_CL2", fmt_dec(d["CL2"], 4))
    R("e3_dcl", fmt_dec(d["cl_hi"] - d["cl_lo"], 2)); R("e3_da", fmt(d["a_hi"] - d["a_lo"], 1))
    R("e3_57a0", fmt_dec(aero.DEG_PER_RAD * d["a0"], 4)); R("e3_57CL", fmt_dec(aero.DEG_PER_RAD * d["CL"], 3))
    R("e3_aeff_m_aL0", fmt_dec(_r(d["aeff"], 3) - d["aL0"], 3))
    R("e3_ai_fig", fmt(d["ai"], 3)); R("e3_CDi_fig", fmt(d["CDi"], 3))
    R("k_angle", fmt(K_ANGLE, 1))
    R("fig_alpha", fmt(AOA_FIG, 1)); R("flight_alpha", fmt(FLIGHT_ALPHA, 2)); R("flight_gamma", fmt(FLIGHT_GAMMA, 2))
