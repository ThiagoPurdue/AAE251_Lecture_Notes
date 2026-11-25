from chapter_4.common import *  # noqa: F401,F403
# Figures and values of 4.1 Thrust and Specific Impulse (notes/chapter-4/thrust-and-specific-impulse.md).
#
# One function per figure, make_all() for the runner, and values() for every number the page prints.
# Run through the runner from the book folder:
#
#     FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_4_figures.py p41
#
# Worked examples:
#   1. an invented first-stage engine at sea level (forward: thrust, its two parts, c, I_sp, state);
#   2. a real engine, the RS-25 at rated power (published.RS25: Space Shuttle News Reference, 1981,
#      p. 2-4): mass flow, exit area from the two published thrusts, thrust at 8 and 30 km;
#   3. an invented ramjet at 14 km (thrust and inlet area).
# Every printed step is computed from the digits printed before it (rounded with fmt), so the
# page's chains close.
#
import math

from chapter_4.drawing4 import WALL_LW  # the outline of a wall cut in section (the engine mount)
from scipy.interpolate import PchipInterpolator  # the smooth ramjet duct (shape preserving: no overshoot)

PAGE = "p41"

# ---------------------------------------------------------------- worked example 1 (invented)
EX1 = dict(mdot=340.0, Ve=2750.0, pe=85000.0, Ae=0.95)          # kg/s, m/s, Pa, m^2; at sea level
# ---------------------------------------------------------------- worked example 2 (RS-25, rated power)
EX2_H = (8000.0, 30000.0)                                         # m: two altitudes not used elsewhere
# gas of the computed nozzle figures: the ratio of specific heats that puts the ideal nozzle through
# SP-125's oxygen-hydrogen thrust coefficient (Table 1-10) and its oxygen-kerosene one (Table 1-9)
G_H2 = matching_gamma(PROPELLANTS["LOX/LH2"]["Cf"], 1000.0, 14.7)
G_RP1 = matching_gamma(PROPELLANTS["LOX/RP-1"]["Cf"], 1000.0, 14.7)
# ---------------------------------------------------------------- worked example 3 (invented ramjet)
EX3 = dict(h=14000.0, V_inf=750.0, mdot=45.0, Ve=1250.0, pe=16000.0, Ae=0.40)

F1S = engine_si(F1)
RT_F1 = 0.5 * F1S["throat_d"]          # F-1 throat radius from its exit diameter and area ratio 16


P = printed                            # (text, value as printed): chapter_4.style


# ================================================================== numbers
def example1():
    e = EX1
    pa = P_SL
    mom = e["mdot"] * e["Ve"]
    prs = (e["pe"] - pa) * e["Ae"]
    mom_s, mom_p = P(mom)
    prs_s, prs_p = P(prs, minus="−")
    F_s, F_p = P(mom_p + prs_p)
    c_s, c_p = P(F_p / e["mdot"], 5)                       # one more digit, so I_sp = c/g0 has the last digit
    isp_s, isp_p = P(c_p / G0)                             # of F/(m-dot g0) (275.68 -> 275.7)
    assert isp_s == fmt(F_p / (e["mdot"] * G0)), "I_sp from the printed c agrees with F/(m-dot g0)"
    c2 = e["Ve"] + (e["pe"] - pa) * e["Ae"] / e["mdot"]
    dvc_s, dvc_p = P((e["pe"] - pa) * e["Ae"] / e["mdot"])
    c2_s, _ = P(e["Ve"] + dvc_p, 5)                        # the check: V_e plus the printed pressure term
    assert c2_s == c_s, (c2_s, c_s)
    vac_prs_s, vac_prs_p = P(e["pe"] * e["Ae"])
    Fv_s, Fv_p = P(mom_p + vac_prs_p)
    close_to(F_p, thrust(e["mdot"], e["Ve"], e["pe"], pa, e["Ae"]), 60.0, "printed thrust")
    close_to(c2, c_p, 0.5, "the two forms of c")
    assert expansion_state(e["pe"], pa) == "overexpanded"
    return dict(mom=mom_s, prs=prs_s, F=F_s, F_kN=fmt(F_p / 1e3), c=c_s, isp=isp_s, dvc=dvc_s,
                vac_prs=vac_prs_s, Fv=Fv_s, Fv_kN=fmt(Fv_p / 1e3), F_p=F_p, Fv_p=Fv_p,
                rise=fmt(100.0 * (Fv_p / F_p - 1.0), 2))


def rs25():
    """Worked example 2 and the thrust-altitude figure: the RS-25 at rated power."""
    s = engine_si(RS25)
    Fsl_s, Fsl = P(s["F_sl"] / 1e3, 5)                 # kN, five figures so the flows agree when printed
    Fv_s, Fv = P(s["F_vac"] / 1e3, 5)
    md_s, md = P(Fsl * 1e3 / (s["isp_sl"] * G0))
    mdv_s, mdv = P(Fv * 1e3 / (s["isp_vac"] * G0))
    assert md_s == mdv_s, (md_s, mdv_s)
    dF_s, dF = P(Fv - Fsl, 4)
    A_s, A = P(dF * 1e3 / P_SL)
    D_s, D = P(diameter_from_area(A))
    pe = pressure_ratio_from_area_ratio(s["area_ratio"], G_H2) * s["pc"]
    h_id = altitude_from_pressure(pe)
    rows = []
    for h in EX2_H:
        pa_s, pa = P(ambient_pressure(h))
        pkN_s, pkN = P(pa * A)                            # N, from the printed p_a and A_e
        pk_s, pk = P(pkN / 1e3)                           # kN
        # the thrust with as many figures as the next step needs: I_sp from the printed F and m-dot must have
        # the last digit of the direct computation (8 km: 1,942 would give 422.8 against 422.90)
        A_full = (s["F_vac"] - s["F_sl"]) / P_SL
        md_full = s["F_sl"] / (s["isp_sl"] * G0)
        I_direct = fmt((s["F_vac"] - ambient_pressure(h) * A_full) / (md_full * G0))
        for sig in (4, 5):
            F_s, Fh = P(Fv - pk, sig)
            I_s, I = P(Fh * 1e3 / (md * G0))
            if I_s == I_direct:
                break
        assert I_s == I_direct, (h, I_s, I_direct)
        prs_s, _ = P((pe - pa) * A / 1e3, 3, minus="−")
        rows.append(dict(h=f"{h / 1e3:g}", pa=pa_s, pa_kPa=fmt(pa / 1e3), pkN=pkN_s, pk=pk_s, F=F_s, isp=I_s,
                         state=expansion_state(pe, pa), F_p=Fh, prs=prs_s))
    assert rows[0]["state"] == "overexpanded" and rows[1]["state"] == "underexpanded"
    F_id = Fv - ambient_pressure(h_id) * A / 1e3
    return dict(s=s, Fsl=Fsl_s, Fv=Fv_s, Fsl_p=Fsl, Fv_p=Fv, md=md_s, md_p=md, dF=dF_s, A=A_s, A_p=A, D=D_s,
                D_pub=fmt(s["exit_d"], 2), pe=pe, pe_kPa=fmt(pe / 1e3, 3), h_id=h_id, h_id_km=fmt(h_id / 1e3, 3),
                F_id=fmt(F_id), rows=rows, gain=fmt(100.0 * (Fv / Fsl - 1.0), 2),
                lbf_sl=fmt(RS25["F_sl_lbf"], 3), lbf_v=fmt(RS25["F_vac_lbf"], 3), D_rel=100.0 * (D - s["exit_d"]) / s["exit_d"])


def example3():
    e = EX3
    T_inf, p_inf, rho = standard(e["h"])
    rho_s, rho_p = P(rho)
    pinf_s, pinf_p = P(p_inf)
    dV = e["Ve"] - e["V_inf"]
    mom_s, mom_p = P(e["mdot"] * dV)
    prs_s, prs_p = P((e["pe"] - pinf_p) * e["Ae"])
    F_s, F_p = P(mom_p + prs_p)
    Ain_s, Ain_p = P(e["mdot"] / (rho_p * e["V_inf"]))
    close_to(F_p, air_breathing_thrust(e["mdot"], e["Ve"], e["V_inf"], e["pe"], p_inf, e["Ae"]), 10.0, "ramjet thrust")
    wrong_s, _ = P(e["mdot"] * e["Ve"] + prs_p)            # the rocket form, V_inf left out (quiz distractor)
    # specific impulse on the air flow (the fuel flow is neglected), from the printed thrust
    isp_s, _ = P(F_p / (e["mdot"] * G0))
    assert isp_s == fmt((mom_p + prs_p) / (e["mdot"] * G0)), "I_sp from the printed thrust has the direct last digit"
    return dict(rho=rho_s, pinf=pinf_s, pinf_kPa=fmt(pinf_p / 1e3), dV=fmt(dV, 3), mom=mom_s, prs=prs_s, F=F_s,
                F_kN=fmt((mom_p + prs_p) / 1e3), Ain=Ain_s, wrong=wrong_s, ram=fmt(e["mdot"] * e["V_inf"]),
                M=fmt(e["V_inf"] / float(speed_of_sound(T_inf)), 3), isp=isp_s)




# ================================================================== figures
def _canvas(xlim, ylim, width=6.5):
    return canvas(width, xlim=xlim, ylim=ylim)


ANATOMY_PARTS = ["injector", "combustion chamber", "converging section", "throat", "diverging section", "exit plane"]


def fig_engine_anatomy():
    """Lesson: the engine turns chemical energy into heat and heat into speed, part by part."""
    tc = thrust_chamber(RT_F1, F1["area_ratio"])
    st, Re, Rc = tc["stations"], tc["r_e"], tc["r_c"]
    fig, ax = _canvas((-2.3, 7.4), (-4.15, 2.55), width=6.5)
    P = draw_thrust_chamber(ax, tc)
    xi, xc, xe = st["injector"], st["chamber_end"], st["exit"]
    rt = tc["r_t"]
    # the throat as a station: a thin dashed line across the narrowest section, like the exit plane
    th = ax.plot([0.0, 0.0], [-rt, rt], color=INK, lw=LW_THIN, ls=(0, (3.0, 2.0)), zorder=2.6)[0]
    on_part(th, P["envelope"])
    # numbered callouts in flow order (the names are in the key at the right and in the text): 3 ends on the
    # converging wall, 4 comes from below to the lower end of the throat line
    x3 = 0.5 * xc
    r3 = float(np.interp(x3, tc["x"], tc["r"]))
    targets = [(xi - 0.10, 0.45), (0.5 * (xi + xc), 0.30), (x3, r3 + 0.5 * tc["wall"]), (0.0, -rt),
               (0.55 * xe, 0.55), (xe, 0.80 * Re)]
    ats = [(xi - 0.45, 1.35), (0.5 * (xi + xc) - 0.05, 1.7), (0.15, 1.5), (0.35, -1.3), (2.6, 1.25), (xe, 2.25)]
    for k, (tg, at) in enumerate(zip(targets, ats), start=1):
        numbered_callout(ax, tg, k, at)
    assert xc < x3 < 0.0, "callout 3 ends on the converging section"
    close_to(float(np.min(tc["r"])), rt, 1e-12, "the throat line is drawn at the narrowest section")
    kx, ky = 5.0, -0.6
    for k, name in enumerate(ANATOMY_PARTS, start=1):
        y = ky - 0.42 * (k - 1)
        key_disc(ax, (kx, y), k)
        text(ax, (kx, y), name, direction=0.0, dist=12.0, fs=FS_LABEL)
    for yy, nm in ((0.30 * Rc, "fuel"), (-0.30 * Rc, "oxidizer")):
        x1 = xi - 0.30 * RT_F1 - 0.04
        flow_arrow(ax, (x1 - 0.75, yy), (x1, yy), width=6.0, head_width=11.0, head_len=7.0)
        text(ax, (x1 - 0.75, yy), nm, direction=180.0, dist=4.0)
    flow_arrow(ax, (xe + 0.15, 0.0), (xe + 1.15, 0.0), label="exhaust", label_dir=0.0)
    # the three forms of energy, in flow order
    yb = -3.5
    b1 = box(ax, (-0.9, yb), "chemical energy\nof the propellants", w=2.15, keep_breaks=True)
    b2 = box(ax, (2.2, yb), "heat: hot gas\nat high pressure", w=2.15, keep_breaks=True)
    b3 = box(ax, (5.3, yb), "speed: a fast,\ncooler exhaust", w=2.15, keep_breaks=True)
    route(ax, b1, "right", b2, "left")
    route(ax, b2, "right", b3, "left")
    for a_, b_, s_ in ((b1, b2, "burns in 2"), (b2, b3, "expands in 3 to 5")):
        text(ax, (0.5 * (a_.cx + b_.cx), yb + 0.5 * b1.h), s_, direction=90.0, dist=3.0, fs=FS_SMALL)
    close_to(tc["r_e"] ** 2 / tc["r_t"] ** 2, 16.0, 1e-9, "F-1 area ratio as drawn")
    trim_canvas(fig)
    save_figure(fig, "p41-engine-anatomy")


def fig_nozzle_flow():
    """Lesson: through the nozzle the gas trades pressure and temperature for speed, and it passes the
    speed of sound at the throat."""
    tc = thrust_chamber(RT_F1, F1["area_ratio"], n=400, n_arc=60)     # fine sampling: smooth curves at the throat
    st = tc["stations"]
    ps = propellant_si("LOX/RP-1")
    g = 1.2
    # the flow on a fine, even grid along the axis. The one-dimensional relations break the slope of the Mach
    # number, and so of every curve, at the throat, where the wall's radius of curvature jumps from 1.5 r_t
    # to 0.382 r_t (the real, two-dimensional flow has no such break). The break is removed: M - 1 has the
    # slope s_u before the throat and s_d after it; the term (s_d - s_u) x for x > 0 is replaced by the smooth
    # ramp (s_d - s_u) (x/2)(1 + tanh(x/w)), w = 0.15 r_t. M stays 1 at the throat, below 1 before it and
    # above 1 after it, and is unchanged a few w away.
    x = np.linspace(tc["x"][0], tc["x"][-1], 1501)
    x = x - x[np.argmin(np.abs(x))]                                    # a grid point on the throat
    area = np.maximum(np.interp(x, tc["x"], tc["r"]) ** 2 / tc["r_t"] ** 2, 1.0)
    it = int(np.argmin(np.abs(x)))
    fl0 = nozzle_flow(area, it, g, ps["Tc"], ps["M"])
    u = fl0["M"] - 1.0
    s_u = float(np.polyfit(x[it - 3:it + 1], u[it - 3:it + 1], 1)[0])
    s_d = float(np.polyfit(x[it:it + 4], u[it:it + 4], 1)[0])
    w = 0.15 * tc["r_t"]
    corr = (s_d - s_u) * (0.5 * x * (1.0 + np.tanh(x / w)) - np.where(x > 0, x, 0.0))
    M = 1.0 + u + np.where(np.abs(x) < 8.0 * w, corr, 0.0)              # (the ramp is below 1e-6 beyond 8 w)
    assert np.all(M[:it] < 1.0) and np.all(M[it + 1:] > 1.0) and M[it] == 1.0, "sonic at the throat only"
    close_to(float(M[-1]), float(fl0["M"][-1]), 1e-9, "the exit Mach number is unchanged")
    T = temperature_ratio(M, g)
    fl = dict(M=M, p=pressure_ratio(M, g), T=T, V=M * np.sqrt(T))      # V in units of the chamber's speed of
    # sound at rest: only V/V_e is plotted
    xlim = (st["injector"] - 0.45, st["exit"] + 0.35)
    fig, ap, ad = aligned_axes(6.5, xlim, (-0.06, tc["r_e"] + 0.12), 2.7, left=0.95, right=0.2, gap=0.10)
    Ve = fl["V"][-1]
    curves = [(fl["p"] / fl["p"][0], 0, "pressure, $p/p_c$"), (fl["T"] / fl["T"][0], 1, "temperature, $T/T_c$"),
              (fl["V"] / Ve, 2, "speed, $V/V_e$")]
    for y, i, _ in curves:
        ap.plot(x, y, **line_kw(i))
    ap.set_ylim(0, 1.08)
    ap.set_ylabel("Ratio to the chamber\nor the exit value")
    ap.set_xticks([])
    ap.tick_params(axis="x", length=0)
    text(ap, (1.25, 0.16), curves[0][2], ha="left", color=text_color(0))
    text(ap, (2.35, 0.67), curves[1][2], ha="left", color=text_color(1))
    label_curve(ap, x, curves[2][0], 3.3, curves[2][2], 2, offset=(0.0, -17.0))
    ap.axvline(0.0, color=GRAY, lw=LW_THIN, ls=(0, (4.0, 3.0)), zorder=1)
    text(ap, (0.0, 1.08), "throat: speed of sound", direction=90.0, dist=3.0, fs=FS_SMALL)
    text(ap, (0.5 * (xlim[0] + 0.0), 0.5), "slower than\nsound", fs=FS_SMALL)
    text(ap, (3.25, 0.33), "faster than sound", fs=FS_SMALL)
    P = draw_thrust_chamber(ad, tc, half=True)
    ad.plot([0.0, 0.0], [tc["r_t"] + tc["wall"], tc["r_e"] + 0.12], color=GRAY, lw=LW_THIN, ls=(0, (4.0, 3.0)), zorder=1)
    th = ad.plot([0.0, 0.0], [0.0, tc["r_t"]], color=GRAY, lw=LW_THIN, ls=(0, (4.0, 3.0)), zorder=2.6)[0]
    on_part(th, P["envelope"])
    # the parts, named in the lower panel
    xch = 0.5 * (st["injector"] + st["chamber_end"])
    name_station(ad, tc, P, "chamber", "chamber", (xch, 1.3), target=(xch, 0.45 * tc["r_c"]), fs=FS_SMALL, ha="center")
    text(ad, (0.0, 0.5 * tc["r_t"]), "throat", direction=0.0, dist=4.0, fs=FS_SMALL)
    text(ad, (st["exit"], 0.45 * tc["r_e"]), "exit", direction=180.0, dist=4.0, fs=FS_SMALL)
    xw = 0.62 * st["exit"]
    rw = float(np.interp(xw, tc["x"], tc["r"])) + tc["wall"]
    text(ad, (xw, rw), "nozzle wall", direction=120.0, dist=5.0, fs=FS_SMALL)
    close_to(float(fl["M"][it]), 1.0, 1e-12, "M = 1 at the throat")
    # (the smoothing ramp dips by under 1e-6 in the flat chamber: no visible rise)
    assert np.all(np.diff(fl["p"]) < 1e-6) and np.all(np.diff(fl["V"]) > -1e-6), "p falls and V rises along the nozzle"
    save_figure(fig, "p41-nozzle-flow")


def nozzle_flow_calc(tc, g, ps):
    return nozzle_flow((tc["r"] / tc["r_t"]) ** 2, int(tc["r"].argmin()), g, ps["Tc"], ps["M"])


def fig_control_volume():
    """Lesson: thrust has two parts, the momentum that leaves and the pressure that does not cancel at the exit."""
    tc = thrust_chamber(RT_F1, F1["area_ratio"])
    st, Re = tc["stations"], tc["r_e"]
    fig, ax = _canvas((-5.6, 8.1), (-3.9, 3.0), width=6.5)
    P = draw_thrust_chamber(ax, tc, axis=False, exit_plane=False)
    xi = st["injector"] - 0.30 * RT_F1                     # the back of the injector plate
    x0, x1, h = xi - 1.25, st["exit"], Re + 0.55
    cv = [(x1, h), (x0, h), (x0, -h), (x1, -h), (x1, h)]
    ax.plot(*np.array(cv).T, color=INK, lw=LW_THIN + 0.3, ls=(0, (5.0, 3.0)), zorder=2.4)
    # the engine mount: a strut from the injector, through the left face of the box, to the vehicle's thrust
    # structure (cut in section, as the walls); the box cuts the strut, so the vehicle's force acts there
    sw = 0.09
    xv1 = x0 - 0.55                                        # right face of the vehicle's thrust structure
    xv0 = xv1 - 0.42
    hv = 0.95
    strut = [(xv1, -sw), (xi, -sw), (xi, sw), (xv1, sw)]
    ax.add_patch(Polygon(strut, closed=True, fc="white", ec=INK, lw=WALL_LW, hatch=WALL_HATCH, zorder=4))
    ax.add_patch(Polygon([(xv0, -hv), (xv1, -hv), (xv1, hv), (xv0, hv)], closed=True, fc="white", ec=INK, lw=WALL_LW,
                         hatch=WALL_HATCH, zorder=4))
    text(ax, (0.5 * (xv0 + xv1), -hv), "vehicle", direction=-90.0, dist=4.0)
    # the forces: on the box, the vehicle pushes the engine toward the exhaust (+F); on the vehicle, the
    # engine pushes forward (the thrust): equal and opposite, at the mount. The force on the engine runs just
    # above the mount and is named in the empty space above the chamber, well inside the box; the thrust on
    # the vehicle is named above its arrow, ending short of the vehicle block
    ya = sw + 0.30
    kind_arrow(ax, (x0 + 0.05, ya), (xi - 0.08, ya), "force")
    text(ax, (x0 + 0.40, 0.95), "force on the\nengine from the\nvehicle, $F$", ha="left", va="bottom")
    kind_arrow(ax, (xv0, 0.0), (xv0 - 1.05, 0.0), "force")
    text(ax, (xv0 - 0.12, 0.22), "thrust on the\nvehicle, $F$", ha="right", va="bottom")
    # pressures: the outside air (p_a, gray) on every face; on the exit plane the exhaust's p_e (black, longer)
    pressure_arrows(ax, [(x0, h), (x1, h)], n=6, side=1, margin=0.06)
    pressure_arrows(ax, [(x1, -h), (x0, -h)], n=6, side=1, margin=0.06)
    pressure_arrows(ax, [(x0, -h), (x0, -1.85)], n=1, side=1, margin=0.5)
    pressure_arrows(ax, [(x0, sw + 0.2), (x0, h)], n=3, side=1, margin=0.2)
    pressure_arrows(ax, [(x1, h), (x1, Re)], n=1, side=1, margin=0.5)
    pressure_arrows(ax, [(x1, -Re), (x1, -h)], n=1, side=1, margin=0.5)
    # p_e: black, heavier and longer than p_a, so the key tells the two apart without color
    PE = dict(color=INK, lw=1.7, head="small")
    pe = pressure_arrows(ax, [(x1, Re), (x1, -Re)], n=4, side=1, margin=0.12, length=22.0, color=PE["color"], lw=PE["lw"])
    text(ax, (0.5 * (x0 + x1), h), "ambient pressure, $p_a$", direction=90.0, dist=20.0, color=PRESSURE_ARROW["color"])
    text(ax, pe[0][0], "exit pressure, $p_e$", direction=0.0, dist=5.0)
    text(ax, (x0, -h), "control volume", direction=-90.0, dist=21.0, ha="left")
    flow_arrow(ax, (x1 + 0.12, 0.0), (x1 + 1.1, 0.0), label="exhaust, ṁ, $V_e$", label_dir=0.0, dist=5.0)
    # the exit plane, bracketed: area A_e, where p_e acts
    xd = x1 - 0.22
    dimension(ax, (xd, -Re), (xd, Re), None, extension=False)
    text(ax, (xd, 0.0), "exit plane,\narea $A_e$", direction=180.0, dist=5.0, backing=False)
    # the key: two columns under the box
    yk = -h - 0.75
    arrow_key(ax, (x0 + 3.1, yk), [("pressure", "ambient pressure, $p_a$"), ("pressure", "exit pressure, $p_e$", PE)])
    arrow_key(ax, (x0 + 7.9, yk), [("force", "force"), ("flow", "flow")])
    assert pe[0][0][0] > x1 and pe[0][1][0] == x1, "p_e arrows push into the box on the exit plane"
    assert xi - 0.08 > x0 + 0.05, "the force on the engine points toward the exhaust (+x)"
    assert PE["lw"] > PRESSURE_ARROW["lw"] + 0.5, "the exit-pressure arrows are clearly heavier than the ambient ones"
    assert xv0 - 1.05 < xv0, "the thrust on the vehicle points forward (-x), opposite"
    trim_canvas(fig)
    save_figure(fig, "p41-control-volume")


def fig_expansion_states():
    """Lesson: the plume shows which way the pressure term pushes."""
    rt, eps = 0.18, 9.0
    tc0 = thrust_chamber(rt, eps)
    Re = tc0["r_e"]
    fig, ax = _canvas((-1.0, 6.2), (-5.3, 0.95), width=6.5)
    rows = [("overexpanded", "$p_e$ < $p_a$", "pressure term negative"),
            ("ideally expanded", "$p_e$ = $p_a$", "pressure term zero"),
            ("underexpanded", "$p_e$ > $p_a$", "pressure term positive")]
    for k, (state, rel, term) in enumerate(rows):
        y = -k * 1.95
        tc = thrust_chamber(rt, eps, origin=(0.0, y))
        draw_thrust_chamber(ax, tc, axis=False)
        xe = tc["stations"]["exit"]
        pl = plume(ax, (xe, y), Re, state, 2.9)
        if state != "ideally expanded":
            m = (pl["s"] > 0.9 * Re) & (pl["s"] < 2.6)
            edge = np.c_[xe + pl["s"][m], y + pl["r"][m]]
            pa_ = pressure_arrows(ax, edge, n=3, side=1 if state == "overexpanded" else -1, length=12.0, margin=0.15)
            base = pa_[-1][0]
            text(ax, base, "$p_a$" if state == "overexpanded" else "$p_e$", direction=0.0, dist=6.0,
                 color=PRESSURE_ARROW["color"])
        if state == "overexpanded":
            # name the two kinds of line once, in the top panel
            xb = xe + 1.9
            text(ax, (xb, y - float(np.interp(1.9, pl["s"], pl["r"]))), "jet boundary", direction=-90.0, dist=4.0,
                 fs=FS_SMALL)
            sx, sy = pl["shocks"][3].get_data()                   # the lower reflected shock
            tg = (sx[0] + 0.6 * (sx[1] - sx[0]), sy[0] + 0.6 * (sy[1] - sy[0]))
            callout(ax, tg, "shocks", (xe + 2.05, y + 0.02), gap=1.5, fs=FS_SMALL)
        text(ax, (tc["stations"]["injector"] - 0.1, y + 0.62), state, ha="left", va="bottom", fontweight="bold")
        math_row(ax, (xe + 3.0, y + 0.18), rel.split(" "))
        text(ax, (xe + 3.0, y - 0.18), term, ha="left", fs=FS_SMALL)
        assert EXPANSION_STATES[k] == state
    trim_canvas(fig)
    save_figure(fig, "p41-expansion-states")


def isp_area_ratio_data():
    ps = propellant_si("LOX/RP-1")
    pc, pa = 1000.0, 14.7                                   # psia, the table's conditions (ratios only)
    g = G_RP1
    eps = np.linspace(1.5, 60.0, 600)
    vac = np.array([ps["cstar"] * thrust_coefficient(e, g, pc, 0.0) / G0 for e in eps])
    e_sep = separation_area_ratio(pc, pa, g)
    e_opt = ideal_area_ratio(pc, pa, g)
    es = eps[eps <= e_sep]
    sl = np.array([ps["cstar"] * thrust_coefficient(e, g, pc, pa) / G0 for e in es])
    isp_opt = ps["cstar"] * thrust_coefficient(e_opt, g, pc, pa) / G0
    isp_vac_opt = ps["cstar"] * thrust_coefficient(e_opt, g, pc, 0.0) / G0
    isp_vac_40 = ps["cstar"] * thrust_coefficient(40.0, g, pc, 0.0) / G0
    return dict(ps=ps, g=g, eps=eps, vac=vac, e_sep=e_sep, e_opt=e_opt, es=es, sl=sl, isp_opt=isp_opt,
                isp_vac_opt=isp_vac_opt, isp_vac_40=isp_vac_40)


def fig_isp_area_ratio():
    """Lesson: at sea level there is a best area ratio; in vacuum a larger nozzle always helps."""
    d = isp_area_ratio_data()
    eps, vac, es, sl = d["eps"], d["vac"], d["es"], d["sl"]
    fig, ax = data_axes(6.5, 3.9)
    ax.plot(eps, vac, **line_kw(1))
    ax.plot(es, sl, **line_kw(0))
    i = int(np.argmax(sl))
    close_to(d["isp_opt"], d["ps"]["isp"], 2e-3, "the curve passes through SP-125's 300 s", rel=True)
    close_to(float(es[i]), d["e_opt"], 0.2, "the best sea-level area ratio is where p_e = p_a")
    assert np.all(np.diff(vac) > 0), "in vacuum a larger nozzle always helps"
    point(ax, (d["e_opt"], d["isp_opt"]), None, ms=7)
    text(ax, (d["e_opt"], d["isp_opt"]), f"best at sea level: $p_e = p_a$,\narea ratio {fmt(d['e_opt'], 2)}",
         direction=50.0, dist=10.0, ha="left")
    point(ax, (es[-1], sl[-1]), None, kind="open", ms=7)
    text(ax, (es[-1], sl[-1]), "flow may separate\nfrom the wall", direction=-40.0, dist=10.0, ha="left", fs=FS_SMALL)
    label_curve(ax, eps, vac, 45.0, "in vacuum", 1, offset=(0.0, -16.0))
    label_curve(ax, es, sl, 12.0, "at sea level", 0, offset=(0.0, -19.0))
    ax.set_xlim(0, 60)
    ax.set_ylim(240, 380)
    ax.set_xlabel("Area ratio, $A_e/A_t$")
    ax.set_ylabel("Specific impulse, $I_\\text{sp}$, s")
    save_figure(fig, "p41-isp-area-ratio")


def fig_nozzle_sizes():
    """Lesson: a vacuum engine carries a much larger nozzle for the same throat."""
    fig, ax = _canvas((-1.5, 11.6), (-3.8, 2.9), width=6.2)
    rt = 0.40
    y_lab = -2.75                                          # the exit labels, one under each nozzle, at one height
    for name, E, x in (("F-1", F1, 0.0), ("J-2", J2, 5.8)):
        tc = thrust_chamber(rt, E["area_ratio"], origin=(x, 0.0), wall=0.05)
        P = draw_thrust_chamber(ax, tc, axis=True)
        xe = tc["stations"]["exit"]
        k = tc["r_e"] / tc["r_t"]
        dimension(ax, (xe + 0.22, -tc["r_e"]), (xe + 0.22, tc["r_e"]), None)
        xm = 0.5 * (x + xe)
        text(ax, (xm, y_lab), f"exit diameter\n= {fmt(k, 3)} × throat diameter", va="top")
        # the throat diameter: a dimension across the throat, named above the engine with a leader off the axis
        dimension(ax, (x, -rt), (x, rt), None, ticks=False, extension=False, zorder=5)
        callout(ax, (x, 0.0), "throat diameter", (x + 2.0, 0.46), gap=1.5, ha="center")
        role = "sea-level engine" if name == "F-1" else "vacuum engine"
        text(ax, (tc["stations"]["injector"], 2.35), f"{name}, {role}\narea ratio {fmt(E['area_ratio'], 3)}",
             ha="left", va="bottom")
        close_to(tc["r_e"] ** 2 / tc["r_t"] ** 2, E["area_ratio"], 1e-9, f"{name} area ratio as drawn")
    trim_canvas(fig)
    save_figure(fig, "p41-nozzle-sizes")


def fig_thrust_altitude():
    """Lesson: a fixed nozzle gains thrust all the way up; ideal expansion is one point on the way."""
    R = rs25()
    s, A, md = R["s"], R["A_p"], R["md_p"]
    h = np.linspace(0.0, H_TOP, 400)
    F = (s["F_vac"] - ambient_pressure(h) * A) / 1e3
    I = F * 1e3 / (md * G0)
    fig, (a1, a2) = data_axes(6.5, 5.0, nrows=2, sharex=True)
    fig.subplots_adjust(hspace=0.12)
    h_id = R["h_id"]
    for ax, y, vac, sl, lab in ((a1, F, s["F_vac"] / 1e3, s["F_sl"] / 1e3, "Thrust, $F$, kN"),
                               (a2, I, s["isp_vac"], s["isp_sl"], "Specific impulse, $I_\\text{sp}$, s")):
        ax.plot(h / 1e3, y, **line_kw(0))
        ax.axhline(vac, **line_kw("boundary"))
        ax.set_ylabel(lab)
        point(ax, (0.0, sl), None, ms=7, kind="square")
        yi = float(np.interp(h_id, h, y))
        point(ax, (h_id / 1e3, yi), None, ms=7)
    close_to(float(F[0]), s["F_sl"] / 1e3, 0.2, "sea-level point on the curve")
    close_to(float(I[0]), s["isp_sl"], 2e-3, "published sea-level I_sp on the curve", rel=True)
    assert np.all(np.diff(F) > 0), "thrust rises all the way up"
    a1.set_ylim(1560, 2170)
    a1.set_yticks([1700, 1800, 1900, 2000, 2100])
    a2.set_ylim(340, 472)
    a2.set_yticks([350, 375, 400, 425, 450])
    text(a1, (0.0, s["F_sl"] / 1e3), f"sea level: {R['Fsl']} kN", direction=-20.0, dist=9.0, ha="left", fs=FS_SMALL)
    text(a1, (50.0, s["F_vac"] / 1e3), f"vacuum: {R['Fv']} kN", direction=90.0, dist=4.0, fs=FS_SMALL)
    text(a1, (h_id / 1e3, float(np.interp(h_id, h, F))), f"ideally expanded at {R['h_id_km']} km",
         direction=-60.0, dist=12.0, ha="left", fs=FS_SMALL)
    text(a2, (0.0, s["isp_sl"]), f"sea level: {fmt(s['isp_sl'])} s", direction=-20.0, dist=9.0, ha="left", fs=FS_SMALL)
    text(a2, (50.0, s["isp_vac"]), f"vacuum: {fmt(s['isp_vac'])} s", direction=90.0, dist=4.0, fs=FS_SMALL)
    # the two altitudes of worked example 2, with their printed values
    for row, hh, d1, d2 in ((R["rows"][0], EX2_H[0], -35.0, -35.0), (R["rows"][1], EX2_H[1], -35.0, -35.0)):
        point(a1, (hh / 1e3, row["F_p"]), None, ms=7, kind="open")
        text(a1, (hh / 1e3, row["F_p"]), f"{row['h']} km: {row['F']} kN", direction=d1, dist=9.0, ha="left", fs=FS_SMALL)
        point(a2, (hh / 1e3, float(row["isp"])), None, ms=7, kind="open")
        text(a2, (hh / 1e3, float(row["isp"])), f"{row['h']} km: {row['isp']} s", direction=d2, dist=9.0, ha="left",
             fs=FS_SMALL)
        close_to(float(np.interp(hh, h, F)), row["F_p"], 0.5, "example point on the thrust curve")
    a2.set_xlim(-1.2, 60)
    a2.set_xticks([0, 10, 20, 30, 40, 50, 60])
    a2.set_xlabel("Altitude, km")
    save_figure(fig, "p41-thrust-altitude")


def _ramjet_contour():
    """Inner radius of a ramjet duct against x (m), drawn from the worked example's areas: inlet
    capture area A (from rho V A), a diffuser that widens to the combustor, a combustor, then a
    converging-diverging nozzle to the exit area A_e. Schematic proportions (not a real engine)."""
    E = example3_areas()
    r_in, r_e = math.sqrt(E["A_in"] / math.pi), math.sqrt(EX3["Ae"] / math.pi)
    r_c, r_t = 1.45 * r_e, 0.80 * r_e
    # stations: inlet lip, diffuser, combustor (flat), nozzle throat, exit; a shape-preserving (PCHIP) spline
    # through them: it passes through every station, so the inlet and exit keep their areas, and it does not
    # overshoot, so the combustor stays straight and the wall has no wave
    st = np.array([(0.0, r_in), (0.5, r_in + 0.52 * (0.98 * r_c - r_in)), (1.05, 0.98 * r_c), (1.45, r_c), (2.3, r_c),
                   (3.15, r_c), (3.75, r_t), (4.3, r_e)])
    x = np.unique(np.r_[np.linspace(st[0, 0], st[-1, 0], 300), st[:, 0]])
    r = PchipInterpolator(st[:, 0], st[:, 1])(x)
    assert np.all(np.diff(x) > 0), "the spline runs forward along the duct"
    comb = (x >= 1.45) & (x <= 3.15)
    close_to(float(np.ptp(r[comb])), 0.0, 1e-12, "the combustor wall is straight")
    assert np.max(r) <= r_c + 1e-12, "no bulge past the combustor radius"
    r[0], r[-1] = r_in, r_e
    return x, r, r_in, r_e


def example3_areas():
    e = EX3
    T, p, rho = standard(e["h"])
    return dict(A_in=e["mdot"] / (rho * e["V_inf"]))


def fig_air_breathing():
    """Lesson: only the change of speed of the air counts."""
    x, r, r_in, r_e = _ramjet_contour()
    fig, ax = _canvas((-2.7, 7.3), (-1.75, 1.75), width=6.5)
    t = 0.07
    for sg in (1, -1):
        wall = np.r_[np.c_[x, sg * r], np.c_[x[::-1], sg * (r[::-1] + t)]]
        ax.add_patch(Polygon(wall, closed=True, fc="white", ec=INK, lw=1.2, hatch=WALL_HATCH, zorder=4))
    ax.plot([x[0], x[-1]], [0, 0], color=GRAY, lw=LW_THIN, ls=(0, (8.0, 2.5, 1.5, 2.5)), zorder=2)
    X = example3()
    text(ax, (0.35, -0.74), f"inlet\n$A$ = {X['Ain']} m²", va="top")
    text(ax, (2.3, -0.74), "combustor", va="top")
    text(ax, (4.1, -0.74), f"nozzle exit\n$A_e$ = {fmt(EX3['Ae'], 2)} m²", va="top")
    arrow_key(ax, (4.9, 1.55), [("velocity", "velocity, to one scale"), ("flow", "flow")])
    xf = 1.5
    rc = float(np.interp(xf, x, r))
    flow_arrow(ax, (xf, rc + 0.55), (xf, rc + t + 0.03), width=5.0, head_width=10.0, head_len=6.0)
    text(ax, (xf, rc + 0.55), "fuel", direction=90.0, dist=3.0)
    # velocities to one scale (blue velocity arrows): the air arrives at V_inf and leaves at V_e
    sc = 1.9 / EX3["Ve"]
    xa = -0.25
    kind_arrow(ax, (xa - sc * EX3["V_inf"], 0.0), (xa, 0.0), "velocity")
    text(ax, (xa - 0.5 * sc * EX3["V_inf"], 0.0), f"air in, $V_\\infty$\n{fmt(EX3['V_inf'], 3)} m/s", direction=90.0,
         dist=9.0, color=TEXT_KIND["velocity"])
    xo = x[-1] + 0.25
    kind_arrow(ax, (xo, 0.0), (xo + sc * EX3["Ve"], 0.0), "velocity")
    text(ax, (xo + 0.5 * sc * EX3["Ve"], 0.0), f"out, $V_e$\n{fmt(EX3['Ve'])} m/s", direction=90.0, dist=9.0,
         color=TEXT_KIND["velocity"])
    # the incoming speed again, dashed, under the outgoing one: the difference is what the engine adds
    yd = -0.42
    ax.annotate("", xy=(xo + sc * EX3["V_inf"], yd), xytext=(xo, yd),
                arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.25", color=SERIES[0], lw=1.4,
                                ls=(0, (4.0, 2.0)), shrinkA=0, shrinkB=0), zorder=6)
    dimension(ax, (xo + sc * EX3["V_inf"], yd - 0.32), (xo + sc * EX3["Ve"], yd - 0.32), None, extension=False, ticks=False)
    text(ax, (xo + sc * 0.5 * (EX3["V_inf"] + EX3["Ve"]), yd - 0.32), "change, $V_e - V_\\infty$",
         direction=-90.0, dist=8.0)
    close_to(float(r[0]) ** 2 * math.pi, example3_areas()["A_in"], 1e-9, "inlet drawn with the example's area")
    close_to(float(r[-1]) ** 2 * math.pi, EX3["Ae"], 1e-9, "exit drawn with the example's area")
    close_to(sc * EX3["Ve"] / (sc * EX3["V_inf"]), EX3["Ve"] / EX3["V_inf"], 1e-12, "arrows to one scale")
    trim_canvas(fig)
    save_figure(fig, "p41-air-breathing")


def make_all():
    fig_engine_anatomy()
    fig_nozzle_flow()
    fig_control_volume()
    fig_expansion_states()
    fig_isp_area_ratio()
    fig_nozzle_sizes()
    fig_thrust_altitude()
    fig_air_breathing()


def values():
    r = lambda k, v: record(PAGE, k, v)                                    # noqa: E731
    # section: effective exhaust velocity and specific impulse (anchor engines)
    s = engine_si(RS25)
    r("rs25-vac-isp", fmt(RS25["isp_vac"]))
    r("rs25-sl-isp", fmt(RS25["isp_sl"]))
    r("rs25-vac-c", fmt(c_from_isp(RS25["isp_vac"])))
    r("f1-sl-kN", fmt(F1S["F_sl"] / 1e3))
    r("f1-sl-lbf", fmt(F1["F_sl_lbf"]))
    r("f1-isp", fmt(F1["isp_sl"], 3))
    r("f1-ratio-thrust", fmt(F1S["F_sl"] / s["F_sl"], 2))
    r("rs25-sl-kN", fmt(s["F_sl"] / 1e3))
    r("rs25-isp-gain", fmt(100.0 * (RS25["isp_sl"] / F1["isp_sl"] - 1.0), 2))
    # worked example 1
    e = example1()
    for k in ("mom", "prs", "F", "F_kN", "c", "isp", "dvc", "vac_prs", "Fv"):
        r(f"ex1-{k}", e[k])
    r("ex1-mdot", fmt(EX1["mdot"], 3))
    r("ex1-Ve", fmt(EX1["Ve"]))
    r("ex1-pe", fmt(EX1["pe"]))
    r("ex1-pe-kPa", fmt(EX1["pe"] / 1e3, 3))
    r("ex1-Ae", fmt(EX1["Ae"], 2))
    r("ex1-kPa-wrong", fmt((EX1["pe"] / 1e3 - P_SL / 1e3) * EX1["Ae"], 4, minus="−"))
    r("ex1-share", fmt(100.0 * abs(float(e["prs"].replace(",", "").replace("−", "-"))) / e["F_p"], 2))
    r("ex1-rise", e["rise"])
    r("p-sl", fmt(P_SL))
    r("ex1-dp", fmt(EX1["pe"] - P_SL))
    r("ex3-dp", fmt(EX3["pe"] - float(example3()["pinf"].replace(",", ""))))
    r("p-sl-kPa", fmt(P_SL / 1e3))
    r("p-sl-kPa-full", fmt(P_SL / 1e3, 6))
    r("ex1-pe-kPa-int", fmt(EX1["pe"] / 1e3, 2))
    # area ratio (computed figure)
    d = isp_area_ratio_data()
    r("ar-best", fmt(d["e_opt"], 2))
    r("ar-best-isp", fmt(d["isp_opt"], 3))
    r("ar-vac-at-best", fmt(d["isp_vac_opt"], 3))
    r("ar-vac-40", fmt(d["isp_vac_40"], 3))
    r("ar-sep", fmt(d["e_sep"], 2))
    r("ar-vac-60", fmt(float(d["vac"][-1]), 3))
    tc = thrust_chamber(RT_F1, F1["area_ratio"])
    fl = nozzle_flow_calc(tc, 1.2, propellant_si("LOX/RP-1"))
    r("flow-T-exit", fmt(float(fl["T"][-1] / fl["T"][0]), 2))
    r("g-rp1", fmt(G_RP1, 3))
    r("g-h2", fmt(G_H2, 4))                       # 1.236: the value that reproduces 15.8 kPa and 13.3 km
    r("ar-pc-MPa", fmt(1000.0 * PSI / 1e6, 4))     # the figure's chamber pressure, 1,000 psia, in MPa
    r("sep-rule", fmt(SEPARATION_PE_PA, 1))
    # nozzle sizes
    r("f1-ar", fmt(F1["area_ratio"], 2))
    r("j2-ar", fmt(J2["area_ratio"], 3))
    r("rs25-ar", fmt(RS25["area_ratio"], 3))
    r("f1-exit-k", fmt(math.sqrt(F1["area_ratio"]), 3))
    r("j2-exit-k", fmt(math.sqrt(J2["area_ratio"]), 3))
    r("f1-pc", fmt(F1["pc_psia"], 3))
    r("j2-pc", fmt(J2["pc_psia"], 3))
    r("rs25-pc", fmt(RS25["pc_psia"]))
    r("rs25-pc-MPa", fmt(s["pc"] / 1e6, 3))
    # worked example 2: the RS-25
    R = rs25()
    for k in ("Fsl", "Fv", "md", "A", "D", "D_pub", "pe_kPa", "h_id_km", "F_id", "gain", "lbf_sl", "lbf_v"):
        r(f"ex2-{k}", R[k])
    r("ex2-Fsl-sci", fmt(R["Fsl_p"] / 1e3, 5))
    r("ex2-Fv-sci", fmt(R["Fv_p"] / 1e3, 5))
    r("ex2-dF", R["dF"])
    r("ex2-dF-N", fmt(float(R["dF"].replace(",", "")) * 1e3))
    for i, row in enumerate(R["rows"]):
        for k in ("h", "pa", "pa_kPa", "pkN", "pk", "F", "isp", "prs"):
            r(f"ex2-{i}-{k}", row[k])
    assert abs(R["D_rel"]) < 0.5
    # worked example 3: the ramjet
    x = example3()
    for k in ("rho", "pinf", "mom", "prs", "F", "F_kN", "Ain", "wrong", "ram", "M", "isp"):
        r(f"ex3-{k}", x[k])
    for k, v in (("h", fmt(EX3["h"] / 1e3, 2)), ("Vinf", fmt(EX3["V_inf"], 3)), ("mdot", fmt(EX3["mdot"], 2)),
                 ("Ve", fmt(EX3["Ve"])), ("pe", fmt(EX3["pe"])), ("pe-kPa", fmt(EX3["pe"] / 1e3, 3)),
                 ("Ae", fmt(EX3["Ae"], 2))):
        r(f"ex3-{k}", v)
    # quiz values (checked here, printed only in the quiz)
    close_to(c_from_isp(1.0) * 0 + 3200.0 / G0, 326.2, 0.05, "quiz: I_sp from c = 3,200 m/s")
    close_to((60000.0 - 100000.0) * 0.5, -20000.0, 1e-9, "quiz: pressure thrust")
    close_to(air_breathing_thrust(40.0, 1100.0, 500.0, 1.0, 1.0, 1.0), 24000.0, 1e-9, "quiz: ramjet thrust")
