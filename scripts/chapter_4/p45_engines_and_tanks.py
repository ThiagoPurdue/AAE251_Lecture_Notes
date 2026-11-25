from chapter_4.common import *  # noqa: F401,F403
"""Page "Engines and tanks" (Chapter 4, no standard): figures and printed values.

Sources (each opened):
  - NASA, Space Shuttle News Reference (1981), NTRS 19810022734: p. 2-4 (main engine: thrust, specific
    impulse, chamber pressure 2970 psia, mixture ratio 6, "approximately 8.5 minutes", throttling 65 to
    109 percent), p. 2-34 (External Tank: 616,493 kg of liquid oxygen and 102,618 kg of liquid hydrogen,
    719,112 kg in all). The engine's own numbers are chapter_4.published.RS25.
  - NASA HAER TX-116, p. 274: throat diameter 10.3 in (chapter_4.published.RS25).
  - Huzel and Huang, NASA SP-125 (1967): Eq. (1-32), p. 12 (c* = p_c A_t g / w); Tables 1-9 and 1-10
    (theoretical c*, chapter_4.published.PROPELLANTS); Table 1-4 (RP-1 density 0.80 to 0.82 g/cc at 68 F,
    boiling 342 to 507 F); Section 2.1, p. 35 (thrust per pound of engine 75 to 125 for larger modern
    engines; propellant fraction 0.94 pump-fed, 0.89 pressure-fed); Section 1.5, pp. 28 and 29, Figures 1-12
    and 1-13 (pressurized-gas and turbopump feed); Chapter VIII: Section 8.1 (tank pressures: pump-fed
    booster tanks 30 to 100 psia, pressure-fed upper-stage tanks 100 to 400 psia), Eq. (8-1) and Sample
    Calculation (8-1) (ullage, 2.5 percent), Section 8.2 (sphere the lightest pressure vessel; materials:
    aluminum alloys, average density 0.1 lb/in^3; Sample Calculation 8-2: 6061-T6 allowable working
    stress 31,800 psi in mainstage; minimum wall stock 0.020 in for aluminum), Section 8.3, Eqs. (8-10),
    (8-11), (8-13), (8-30) (sphere and cylinder wall thickness from the hoop-membrane stress).
  - NIST Chemistry WebBook: liquid oxygen and parahydrogen at 0.101325 MPa (chapter_4.published.NIST).
  - Plachta, Johnson and Feller, "Cryogenic Boil-Off Reduction System Testing", AIAA Joint Propulsion
    Conference (2014), NTRS 20150000134, p. 1 (boil-off losses for missions longer than several days;
    insulation and cryocoolers reduce them; LH2 is the hardest); abstract: liquid oxygen zero boil-off, liquid
    hydrogen boil-off reduced 60 percent by a 90 K cryocooler (chapter_4.published.PLACHTA_LH2_CUT).
  - NIST Chemistry WebBook, normal hydrogen at 0.101325 MPa (chapter_4.published.NIST_NORMAL_H2): the largest
    difference from parahydrogen's boiling point, density and heat of vaporization.
The two tank examples are the lectures' own (12,000 kg of oxygen and kerosene at a mixture ratio of
2.56 with 5 percent ullage in a 3.0 m stage; 3,500 kg of hydrogen, a 40 W heat leak, a four-day coast).
The tank pressures of worked example 3 (0.3 and 2.0 MPa) are chosen inside SP-125's two ranges.
"""
from matplotlib.patches import Rectangle, PathPatch  # noqa: E402,F401
from matplotlib.path import Path as MPath  # noqa: E402
from chapter_4.drawing4 import _capsule, _below, _fill_poly, _pt, _poly, WALL_LW  # noqa: E402  (private shape helpers, read only)

PAGE = "p45"


# Worked example 2 (the lectures'): oxygen and kerosene upper stage
TANK = dict(m_prop=12000.0, r=2.56, ullage=0.05, stage_d=3.0)
# Worked example 3: tank pressures inside SP-125's ranges (Pa)
P_PUMP, P_PRESS = 0.3e6, 2.0e6
# Worked example 4 (the lectures'): hydrogen stage on a four-day coast
BOIL = dict(m=3500.0, Q=40.0, days=4.0)
HEAT_LEAK_W = (10.0, 40.0, 160.0)         # W, the three curves of the boil-off figure (illustrative)
DAY = 86400.0


def _r(x, sig=4):
    """The number as printed (fmt), back as a float, so each step is computed from printed digits."""
    return float(fmt(x, sig).replace(",", ""))


def _rd(x, nd):
    return float(fmt_dec(x, nd).replace(",", ""))


# ===================================================================== the numbers of the page
def _numbers():
    n = {}
    s = engine_si(RS25)
    # --- worked example 1: the Shuttle's main engines
    n["F_vac"] = s["F_vac"]
    n["mdot"] = s["F_vac"] / (s["isp_vac"] * G0)
    mdot = _r(n["mdot"])                                   # 468.2
    n["mdot3"] = SHUTTLE_MAIN_ENGINES * mdot               # 1,404.6
    n["t_b"] = SHUTTLE_ET_PROP_KG / n["mdot3"]
    n["t_b_min"] = _rd(n["t_b"], 1) / 60.0
    n["pc"] = s["pc"]
    pc = _rd(s["pc"] / 1e6, 2) * 1e6                       # 20.48 MPa
    n["d_t"] = s["throat_d"]
    n["A_t"] = math.pi / 4.0 * _r(s["throat_d"]) ** 2
    A_t = _r(n["A_t"])
    n["cstar"] = pc * A_t / mdot
    n["cstar_h2"] = propellant_si("LOX/LH2")["cstar"]
    n["cstar_rp"] = propellant_si("LOX/RP-1")["cstar"]
    n["A_t_half"] = mdot * _r(n["cstar"]) / (pc / 2.0)
    # engine thrust-to-weight ratios (W = m g0)
    f1, j2 = engine_si(F1), engine_si(J2)
    n["fw"] = dict(F1=f1["F_sl"] / (f1["mass"] * G0), J2=j2["F_vac"] / (j2["mass"] * G0),
                   RS25=s["F_vac"] / (s["mass"] * G0), RS25_sl=s["F_sl"] / (s["mass"] * G0))
    n["eng"] = dict(F1=f1, J2=j2, RS25=s)
    # --- worked example 2: the tanks
    T = TANK
    m_ox = T["m_prop"] * T["r"] / (1.0 + T["r"])
    m_f = T["m_prop"] / (1.0 + T["r"])
    n["m_ox"], n["m_f"] = m_ox, m_f
    rho_ox = _r(NIST["oxygen"]["rho"])                     # 1,141
    rho_f = RP1_RHO                                        # 800 (published.py: the larger tank)
    n["rho_ox"], n["rho_f"] = rho_ox, rho_f
    n["V_ox"] = _r(m_ox) / rho_ox
    n["V_f"] = _r(m_f) / rho_f
    n["Vt_ox"] = _r(n["V_ox"]) * (1.0 + T["ullage"])
    n["Vt_f"] = _r(n["V_f"]) * (1.0 + T["ullage"])
    n["d_ox"] = sphere_diameter(_r(n["Vt_ox"]))
    n["d_f"] = sphere_diameter(_r(n["Vt_f"]))
    n["mass_share_ox"] = m_ox / T["m_prop"]
    n["vol_share_ox"] = n["Vt_ox"] / (n["Vt_ox"] + n["Vt_f"])
    n["vol_ratio"] = n["Vt_ox"] / n["Vt_f"]
    n["stack"] = n["d_ox"] + n["d_f"]
    # --- worked example 3: the wall of the oxygen tank
    Sw = AL_SW_PSI * PSI
    n["Sw"] = Sw
    n["rho_al"] = AL_RHO
    r_ox = _r(_r(n["d_ox"]) / 2.0)                         # 1.238 m, as printed
    n["r_ox"] = r_ox
    Sw_p = _r(Sw / 1e6) * 1e6                              # 219.3 MPa
    rho_al = _r(AL_RHO)                                    # 2,768
    for key, p in (("pump", P_PUMP), ("press", P_PRESS)):
        t = p * r_ox / (2.0 * Sw_p)
        n[f"t_{key}"] = t
        tp = _r(t * 1000.0, 3) / 1000.0
        n[f"m_{key}"] = 4.0 * math.pi * r_ox ** 2 * tp * rho_al
        n[f"m_{key}_exact"] = 4.0 * math.pi * r_ox ** 2 * t * rho_al
    n["t_min"] = AL_MIN_WALL_IN * IN
    # --- worked example 4: boil-off
    h = _r(NIST["hydrogen"]["h_vap"]) * 1000.0             # 446.1 kJ/kg in J/kg
    n["h_vap"] = h
    rate = BOIL["Q"] / h
    n["rate"] = rate
    n["rate_day"] = _r(rate) * DAY
    n["lost"] = _r(n["rate_day"]) * BOIL["days"]
    n["lost_pct"] = _r(n["lost"]) / BOIL["m"] * 100.0
    n["empty_days"] = BOIL["m"] / (HEAT_LEAK_W[2] / h * DAY)
    # parahydrogen against normal hydrogen (NIST): the largest relative difference of the three values printed
    para = NIST["hydrogen"]
    n["h2_diff"] = max(abs(NIST_NORMAL_H2[k] / para[k] - 1.0) for k in ("Tb", "rho", "h_vap"))
    assert n["h2_diff"] < 0.01, n["h2_diff"]
    return n


N = _numbers()


# ===================================================================== figures
def fig_feed_systems():
    """Pressure-fed and pump-fed engines side by side, the tank pressures of SP-125 under each.
    Lesson: a pump lets the tanks stay at low pressure, so they can be thin and light."""
    fig, ax = canvas(6.5, xlim=(-2.5, 8.6), ylim=(-1.75, 8.6))
    A = liquid_engine("pressure", origin=(0.0, 0.0))
    B = liquid_engine("pump", origin=(5.4, 0.0))
    # the turbine exhaust duct is left out, as on page 4.4's engine-kinds figure, so the two pump-fed schematics
    # match; the lesson here is the tank walls, not where the turbine gas goes
    tx, tz = B["points"]["turbine_exhaust"]
    n0 = len(B["pipes"])
    B["pipes"] = [pl for pl in B["pipes"] if not (len(pl) == 2 and abs(pl[1][0] - tx) < 1e-9 and abs(pl[1][1] - tz) < 1e-9)]
    assert len(B["pipes"]) == n0 - 1
    liquids_a = dict(A["liquids"])
    A["liquids"] = {}                       # the pressure-fed liquids are drawn below, inside the thick wall
    PA, PB = draw_schematic(ax, A), draw_schematic(ax, B)
    # thick walls on the pressure-fed tanks (exaggerated): a section-hatched band of one thickness all round,
    # as the thrust-chamber walls of page 4.1, between the outer outline and an inner capsule; the liquid fills
    # the inner capsule only. The pump-fed tanks keep a single outline (a thin wall).
    lw_tank = LW_DETAIL + 0.4               # the outline weight draw_schematic gives every tank
    t_wall = _pt(ax, 3.5 * lw_tank)         # band at 3.5 times the thin wall's line
    for nm in ("fuel_tank", "oxidizer_tank"):
        xy = A["parts"][nm].xy
        x_lo, x_hi, z_lo, z_hi = xy[:, 0].min(), xy[:, 0].max(), xy[:, 1].min(), xy[:, 1].max()
        R = 0.5 * (x_hi - x_lo)
        cx, z0, z1 = 0.5 * (x_lo + x_hi), z_lo + R, z_hi - R
        inner = _capsule(cx, z0, z1, R - t_wall)
        band = PathPatch(MPath.make_compound_path(MPath(np.r_[xy, xy[:1]], closed=True),
                                                  MPath(np.r_[inner[::-1], inner[-1:]], closed=True)),
                         fc="white", ec=INK, lw=lw_tank, hatch=WALL_HATCH, joinstyle="round", zorder=3.5)
        ax.add_patch(band)
        on_part(band, PA[nm])
        sty, level = liquids_a[nm]
        liq = _below(inner, level)
        fp, ed = _fill_poly(ax, liq, LIQUID_STYLE[sty], 3.2, edge_lw=0.0)
        ed.set_visible(False)
        on_part(fp, PA[nm])
        at_ = liq[np.abs(liq[:, 1] - level) < 1e-9]
        on_part(ax.plot([at_[:, 0].min(), at_[:, 0].max()], [level, level], color=INK, lw=LW_FINE, zorder=3.3)[0], PA[nm])
        # what the drawing asserts: the liquid lies inside the inner outline, and the wall is one thickness
        assert liq[:, 0].min() >= cx - (R - t_wall) - 1e-9 and liq[:, 0].max() <= cx + (R - t_wall) + 1e-9
        assert liq[:, 1].min() >= z0 - (R - t_wall) - 1e-9
        assert t_wall >= 3.0 * _pt(ax, lw_tank), "the thick wall is at least three times the thin one"
    lab = lambda P, S, name, s_, at, **kw: label_part(ax, P, S["parts"], name, s_, at, **kw)  # noqa: E731
    lab(PA, A, "pressurant", "helium", (-1.45, 7.75), ha="center")
    lab(PA, A, "fuel_tank", "fuel", (-2.0, 3.55), ha="center")
    lab(PA, A, "oxidizer_tank", "oxidizer", (2.05, 3.55), ha="center")
    lab(PA, A, "thrust_chamber", "thrust\nchamber", (1.65, 0.75), ha="center")
    text(ax, (0.0, 8.35), "pressure-fed", va="bottom")
    (_, (xv, zv)), = [v for v in A["valves"] if v[0] == "regulator"]
    callout(ax, (xv + 0.12, zv), "regulator", at=(1.55, 6.75), fs=FS_LABEL)
    lab(PB, B, "fuel_tank", "fuel", (3.55, 6.55), ha="center")
    lab(PB, B, "oxidizer_tank", "oxidizer", (7.5, 6.55), ha="center")
    lab(PB, B, "fuel_pump", "fuel pump", (3.45, 5.05), ha="center")
    lab(PB, B, "oxidizer_pump", "oxidizer\npump", (7.45, 4.15), ha="center")
    # the turbine named between the two tank lines, above it, with a short slanted leader (no pipe crossed),
    # as on page 4.4's engine-kinds figure
    lab(PB, B, "turbine", "turbine", (5.25, 4.9), ha="center", target=(5.4 + 0.08, 4.2))
    lab(PB, B, "gas_generator", "gas\ngenerator", (3.4, 3.65), ha="center", target=(5.4 - 0.12, 3.40))
    lab(PB, B, "thrust_chamber", "thrust\nchamber", (7.05, 0.75), ha="center")
    text(ax, (5.4, 8.35), "pump-fed", va="bottom")
    lo_a, hi_a = (p * PSI / 1e6 for p in TANK_PSIA["pressure"])
    lo_b, hi_b = (p * PSI / 1e6 for p in TANK_PSIA["pump"])
    text(ax, (0.0, -0.75), f"tanks at {fmt(lo_a, 1)} to {fmt(hi_a, 2)} MPa:\nthick, heavy walls", va="center")
    text(ax, (5.4, -0.75), f"tanks at {fmt(lo_b, 1)} to {fmt(hi_b, 1)} MPa:\nthin, light walls", va="center")
    # the pressure-fed tanks hold more than the pump-fed ones
    assert lo_a >= hi_b - 1e-9 and hi_a > 3.0 * hi_b, (lo_a, hi_a, lo_b, hi_b)
    assert "pressurant" in A["parts"] and "turbine" in B["parts"] and "turbine" not in A["parts"]
    trim_canvas(fig)
    save_figure(fig, "p45-feed-systems")


def fig_throat_and_pressure():
    """Throat area against chamber pressure for the RS-25's mass flow and c*.
    Lesson: halving the chamber pressure doubles the throat for the same flow."""
    mdot, cs = _r(N["mdot"]), _r(N["cstar"])
    pc_rs = _rd(N["pc"] / 1e6, 2)
    p = np.linspace(4.0, 29.0, 400)
    A = mdot * cs / (p * 1e6)
    fig, ax = data_axes(6.5, 3.6)
    ax.plot(p, A, **line_kw(0))
    a_rs, a_half = _r(N["A_t"]), _r(N["A_t_half"])
    close_to(mdot * cs / (pc_rs * 1e6), a_rs, 2e-3, "the curve passes through the RS-25's published throat", rel=True)
    close_to(mdot * cs / (pc_rs * 1e6 / 2.0), a_half, 2e-3, "half the pressure on the curve", rel=True)
    close_to(a_half / a_rs, 2.0, 2e-3, "half the pressure, twice the throat")
    # construction: each point read on both axes; the pressures halve (x 1/2) while the areas double (x 2)
    for pp, aa in ((pc_rs, a_rs), (pc_rs / 2.0, a_half)):
        ax.plot([0.0, pp], [aa, aa], **line_kw("boundary"))
        ax.plot([pp, pp], [0.0, aa], **line_kw("boundary"))
    x_dim, y_dim = 1.6, 0.022
    dimension(ax, (x_dim, a_rs), (x_dim, a_half), "×2", label_side=-1, ticks=False, extension=False)
    dimension(ax, (pc_rs, y_dim), (pc_rs / 2.0, y_dim), "×½", label_side=-1, ticks=False, extension=False)
    point(ax, (pc_rs, a_rs), None, ms=7)
    point(ax, (pc_rs / 2.0, a_half), None, ms=7, kind="open")
    text(ax, (pc_rs, a_rs), f"RS-25: {fmt(pc_rs)} MPa,\n{fmt(a_rs)} m²", direction=45.0, dist=9.0, ha="left")
    text(ax, (pc_rs / 2.0, a_half), f"half the pressure, {fmt(pc_rs / 2.0)} MPa:\ntwice the area, {fmt(a_half)} m²",
         direction=40.0, dist=9.0, ha="left")
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 0.30)
    ax.set_xlabel("Chamber pressure, $p_c$, MPa")
    ax.set_ylabel("Throat area, $A_t$, m²")
    save_figure(fig, "p45-throat-and-pressure")


def fig_tanks_in_stage():
    """The two spheres of worked example 2 in the 3.0 m stage, to scale, with mass and volume shares.
    Lesson: oxygen is 72 percent of the mass, yet its tank is not even twice the fuel tank."""
    fig, ax = canvas(6.5, xlim=(-2.9, 9.4), ylim=(-0.8, 5.4))
    # the spheres touch, and the stage is cut at their outer tangents, so its drawn length is the stack
    T = tanks_in_stage(ax, TANK["stage_d"], [
        dict(name="kerosene", volume=_r(N["V_f"]), ullage=TANK["ullage"], style="fuel"),
        dict(name="liquid oxygen", volume=_r(N["V_ox"]), ullage=TANK["ullage"], style="oxidizer")],
        gap=0.0, margin=0.0)
    hs = TANK["stage_d"] / 2.0
    for name, key in (("kerosene", "f"), ("liquid oxygen", "ox")):
        t = T["tanks"][name]
        close_to(t["D"], N["d_" + key], 1e-3, "drawn diameter", rel=True)
        cx, cz = t["center"]
        dimension(ax, (cx - t["R"], cz), (cx + t["R"], cz), None, ticks=False, extension=False, zorder=4.2)
        text(ax, (cx + hs, cz), f"{name},\nd = {fmt(N['d_' + key])} m", direction=0.0, dist=8.0, ha="left")
        top_ = cz + t["R"]
        callout(ax, (cx + 0.1, t["level"] + 0.55 * (top_ - t["level"])), f"ullage, {fmt(100 * TANK['ullage'], 1)}%",
                at=(cx + hs + 0.22, top_ - 0.18), fs=FS_SMALL, ha="left")
    dimension(ax, (-hs, 0.0), (hs, 0.0), "stage, 3.0 m", label_side=-1, offset=-0.3)
    close_to(T["top"] - T["bottom"], N["d_ox"] + N["d_f"], 1e-3, "drawn stack length", rel=True)
    dimension(ax, (-hs, T["bottom"]), (-hs, T["top"]), f"{fmt(N['stack'], 3)} m", offset=0.35, label_side=1)
    # oxygen's share of the mass and of the tank volume, two bars of one length
    x0, L, hb = 5.0, 4.0, 0.42
    rows = [("mass", N["mass_share_ox"], 3.55), ("volume", N["vol_share_ox"], 1.75)]
    st_o, st_f = LIQUID_STYLE["oxidizer"], LIQUID_STYLE["fuel"]
    for nm, f, y in rows:
        fill_region(ax, [(x0, y), (x0 + L * f, y), (x0 + L * f, y + hb), (x0, y + hb)], st_o, 3.0)
        fill_region(ax, [(x0 + L * f, y), (x0 + L, y), (x0 + L, y + hb), (x0 + L * f, y + hb)], st_f, 3.0)
        text(ax, (x0, y + hb / 2), nm, direction=180.0, dist=5.0)
        text(ax, (x0 + L * f / 2, y + hb), f"oxygen, {fmt(100 * f, 3)}%", direction=90.0, dist=4.0, fs=FS_SMALL)
        text(ax, (x0 + L * (1 + f) / 2, y), f"kerosene,\n{fmt(100 * (1 - f), 3)}%", direction=-90.0, dist=4.0,
             fs=FS_SMALL)
    close_to(rows[0][1], N["m_ox"] / TANK["m_prop"], 1e-12, "mass share drawn")
    close_to(rows[1][1], N["Vt_ox"] / (N["Vt_ox"] + N["Vt_f"]), 1e-12, "volume share drawn")
    assert N["mass_share_ox"] > 0.7 and N["vol_share_ox"] < 0.65
    trim_canvas(fig)
    save_figure(fig, "p45-tanks-in-stage")


def fig_tank_wall():
    """Free bodies of the hoop-stress derivation: half a cylinder cut along its length (end view) and half a
    sphere cut through its center, each with the pressure normal to the inside wall and the wall stress on the
    two cut edges; below each, the cut face seen from below, with the projected area the pressure acts on
    (2rL, pi r^2) and the wall area that carries the stress (2 t_w L, 2 pi r t_w).
    Lesson: the pressure acts on the projected area, the wall carries it on its thin cut, and a sphere has
    twice the wall per unit of projected area, so half the stress."""
    r, t = 1.0, 0.14                         # inner radius and wall thickness (exaggerated), drawing units
    ro = r + t
    Lc = 1.4                                 # length of the cylinder seen in the cut face
    cols = ((0.0, "cylinder, cut along its length\n(end view)"), (4.0, "sphere, cut through\nits center"))   # two lines each
    y2 = -2.35                               # center of the cut-face row
    fig, ax = canvas(6.5, xlim=(-1.9, 7.9), ylim=(-4.9, 2.1))
    th = np.linspace(0.0, math.pi, 181)
    for xc, title in cols:
        # the half wall, cut in section, and the pressure on its inside, normal to it
        ring = np.r_[np.c_[xc + ro * np.cos(th), ro * np.sin(th)], np.c_[xc + r * np.cos(th[::-1]), r * np.sin(th[::-1])]]
        wall = _poly(ax, ring, fc="white", ec=INK, lw=WALL_LW, hatch=WALL_HATCH, z=3.0)
        inner = np.c_[xc + r * np.cos(th), r * np.sin(th)]
        pressure_arrows(ax, inner, n=9, length=16.0, side=1, inward=True, margin=0.07)
        # the wall stress on the two cut edges, pulling this half toward the other half
        for sx in (-1, 1):
            xs = xc + sx * (r + 0.5 * t)
            kind_arrow(ax, (xs, 0.0), (xs, -0.6), "force", "$\\sigma$", label_dir=90.0 - 90.0 * sx, label_at="tip", dist=5.0)
        callout(ax, (xc - (r + 0.5 * t) * math.cos(math.radians(40)), (r + 0.5 * t) * math.sin(math.radians(40))),
                "wall, $t_\\text{w}$", at=(xc - 1.45, 1.45), ha="center", fs=FS_LABEL)
        text(ax, (xc, 1.75), title, va="bottom", fs=FS_LABEL)
        text(ax, (xc, -1.0), "the cut, seen from below", fs=FS_SMALL)
    # cut faces: the projected area (light) and the cut wall (section hatch)
    xc = cols[0][0]
    for sx in (-1, 1):
        x_in, x_out = xc + sx * r, xc + sx * ro
        _poly(ax, [(x_in, y2 - Lc / 2), (x_out, y2 - Lc / 2), (x_out, y2 + Lc / 2), (x_in, y2 + Lc / 2)], fc="white",
              ec=INK, lw=WALL_LW, hatch=WALL_HATCH, z=3.0)
    gas_c = _poly(ax, [(xc - r, y2 - Lc / 2), (xc + r, y2 - Lc / 2), (xc + r, y2 + Lc / 2), (xc - r, y2 + Lc / 2)],
                  fc=HIGHLIGHT, ec=INK, lw=WALL_LW, z=3.0)
    text(ax, (xc, y2), "$2rL$", fs=FS_LABEL, backing=HIGHLIGHT)
    dimension(ax, (xc - r, y2 - Lc / 2), (xc + r, y2 - Lc / 2), "$2r$", offset=-0.25, label_side=-1)
    dimension(ax, (xc + ro, y2 - Lc / 2), (xc + ro, y2 + Lc / 2), "$L$", offset=-0.25, label_side=-1)
    xc2 = cols[1][0]
    o_xy = np.c_[xc2 + ro * np.cos(2 * th), y2 + ro * np.sin(2 * th)]
    i_xy = np.c_[xc2 + r * np.cos(2 * th[::-1]), y2 + r * np.sin(2 * th[::-1])]
    ann = PathPatch(MPath.make_compound_path(MPath(o_xy, closed=True), MPath(i_xy, closed=True)), fc="white", ec=INK,
                    lw=WALL_LW, hatch=WALL_HATCH, joinstyle="round", zorder=3.0)
    ax.add_patch(ann)
    disk = _poly(ax, np.c_[xc2 + r * np.cos(2 * th), y2 + r * np.sin(2 * th)], fc=HIGHLIGHT, ec=INK, lw=WALL_LW, z=3.1)
    text(ax, (xc2, y2 + 0.3), "$\\pi r^2$", fs=FS_LABEL, backing=HIGHLIGHT)
    a_r = math.radians(-30.0)
    on_part(ax.plot([xc2, xc2 + r * math.cos(a_r)], [y2, y2 + r * math.sin(a_r)], color=INK, lw=LW_THIN, zorder=3.5)[0], disk)
    text(ax, (xc2 + 0.5 * r * math.cos(a_r), y2 + 0.5 * r * math.sin(a_r)), "$r$", direction=60.0, dist=7.0,
         backing=HIGHLIGHT)
    # the two balances, under their columns
    text(ax, (cols[0][0], -3.85), "$p\\,(2rL) = \\sigma\\,(2t_\\text{w}L)$", va="top")
    text(ax, (cols[1][0], -3.85), "$p\\,(\\pi r^2) = \\sigma\\,(2\\pi r\\,t_\\text{w})$", va="top")
    text(ax, (cols[0][0], -4.35), "$\\sigma = p\\,r/t_\\text{w}$", va="top")
    text(ax, (cols[1][0], -4.35), "$\\sigma = p\\,r/(2\\,t_\\text{w})$", va="top")
    arrow_key(ax, (5.75, 0.75), [("pressure", "pressure, $p$"), ("force", "wall stress, $\\sigma$")])
    # what the drawing asserts: the vertical part of the pressure on the half wall adds up to p times the
    # projected width 2r (per unit length), and the drawn cut faces have the inner radius of the walls above
    up = np.trapezoid(np.sin(th) * r, th)
    close_to(up, 2.0 * r, 1e-4, "pressure on the half wall = p x 2r per unit length")
    close_to(np.ptp(gas_c.get_xy()[:, 0]), 2.0 * r, 1e-12, "projected width drawn")
    close_to(np.ptp(disk.get_xy()[:, 0]), 2.0 * r, 1e-3, "projected disk drawn", rel=True)
    trim_canvas(fig)
    save_figure(fig, "p45-tank-wall")


def fig_boil_off():
    """Hydrogen boiled off against coast time for three heat leaks, over ten days and over six months, the
    example marked. Lesson: boil-off is small over days and decisive over months."""
    h, m0 = N["h_vap"], BOIL["m"]
    fig, (a1, a2) = data_axes(6.5, 3.7, ncols=2, gridspec_kw=dict(width_ratios=[1.0, 1.35], wspace=0.55))
    spans = ((a1, 10.0, 100.0, "the first 10 days"), (a2, 180.0, 4000.0, "six months"))
    label_at = {a1: {10.0: (8.0, (8.0, -14.0)), 40.0: (9.0, (-18.0, 12.0)), 160.0: (2.0, (24.0, -2.0))},
                a2: {10.0: (150.0, (0.0, 16.0)), 40.0: (120.0, (-16.0, 16.0)), 160.0: (60.0, (-30.0, 0.0))}}
    for ax, dmax, ymax, title in spans:
        for i, Q in enumerate(HEAT_LEAK_W):
            rate = Q / h * DAY                                         # kg per day
            d_end = min(dmax, m0 / rate, ymax / rate)
            dd = np.linspace(0.0, d_end, 200)
            ax.plot(dd, rate * dd, **line_kw(i))
            x_at, off = label_at[ax][Q]
            label_curve(ax, dd, rate * dd, x_at, f"{Q:g} W", i, offset=off, fs=FS_SMALL)
        ax.set_xlim(0, dmax)
        ax.set_ylim(0, ymax)
        ax.set_title(title, fontsize=FS_LABEL, pad=8.0)
        ax.set_xlabel("Coast time, days")
    a1.set_xticks([0, 2, 4, 6, 8, 10])
    a2.set_xticks([0, 30, 60, 90, 120, 150, 180])
    a1.set_ylabel("Hydrogen boiled off, kg")
    a2.set_ylabel("Hydrogen boiled off, kg")
    # six months: the whole load, and the day the largest heat leak empties the tank
    a2.axhline(m0, **line_kw("boundary"))
    text(a2, (8.0, m0), "whole load", direction=90.0, dist=3.0, ha="left", fs=FS_SMALL)
    te = N["empty_days"]
    point(a2, (te, m0), None, ms=6, kind="open")
    text(a2, (te, m0), f"empty after\n{fmt(te, 3)} days", direction=-55.0, dist=9.0, ha="left", fs=FS_SMALL)
    # ten days: the example
    ex = (BOIL["days"], _r(N["lost"]))
    point(a1, ex, None, ms=7)
    text(a1, ex, f"{fmt(N['lost'])} kg", direction=-35.0, dist=7.0, ha="left", fs=FS_SMALL)
    close_to(BOIL["Q"] / h * DAY * BOIL["days"], ex[1], 1e-3, "example on the 40 W line", rel=True)
    close_to(m0 / (HEAT_LEAK_W[2] / h * DAY), te, 1e-9, "the 160 W line reaches the whole load")
    assert ex[1] / m0 < 0.01 and HEAT_LEAK_W[1] / h * DAY * 180.0 / m0 > 0.35, "small over days, large over months"
    save_figure(fig, "p45-boil-off")


def make_all():
    fig_feed_systems()
    fig_throat_and_pressure()
    fig_tanks_in_stage()
    fig_tank_wall()
    fig_boil_off()


# ===================================================================== values printed on the page
def values():
    n = N
    R = lambda k, t: record(PAGE, k, t)  # noqa: E731
    s = n["eng"]["RS25"]
    # worked example 1
    R("ex1-F", fmt(RS25["F_vac_lbf"]))
    R("ex1-FN", fmt(n["F_vac"]))
    R("ex1-isp", fmt(RS25["isp_vac"]))
    R("ex1-mdot", fmt(n["mdot"]))
    R("ex1-mdot3", fmt_dec(n["mdot3"], 1))
    R("ex1-prop", fmt(SHUTTLE_ET_PROP_KG))
    R("ex1-lox", fmt(SHUTTLE_ET_LOX_KG))
    R("ex1-lh2", fmt(SHUTTLE_ET_LH2_KG))
    R("ex1-tb", fmt_dec(n["t_b"], 1))
    R("ex1-tbmin", fmt(n["t_b_min"], 3))
    R("ex1-pc", fmt_dec(n["pc"] / 1e6, 2))
    R("ex1-pc-psia", fmt(RS25["pc_psia"]))
    R("ex1-dt-in", fmt(RS25["throat_d_in"], 3))
    R("ex1-dt", fmt(n["d_t"]))
    R("ex1-At", fmt(n["A_t"]))
    R("ex1-cstar", fmt(n["cstar"]))
    R("ex1-mix", fmt(RS25_MIXTURE, 1))
    R("cstar-h2", fmt(n["cstar_h2"]))
    R("cstar-rp", fmt(n["cstar_rp"]))
    R("cstar-h2-fps", fmt(PROPELLANTS["LOX/LH2"]["cstar_fps"]))
    R("cstar-rp-fps", fmt(PROPELLANTS["LOX/RP-1"]["cstar_fps"]))
    R("mix-h2", fmt(PROPELLANTS["LOX/LH2"]["r"], 3))
    R("At-half", fmt(n["A_t_half"]))
    R("pc-half", fmt_dec(n["pc"] / 2e6, 2))
    # engine thrust-to-weight table
    e = n["eng"]
    R("fw-f1-FkN", fmt(e["F1"]["F_sl"] / 1e3))
    R("fw-f1-m", fmt(e["F1"]["mass"]))
    R("fw-f1", fmt(n["fw"]["F1"], 3))
    R("fw-j2-FkN", fmt(e["J2"]["F_vac"] / 1e3))
    R("fw-j2-m", fmt(e["J2"]["mass"]))
    R("fw-j2", fmt(n["fw"]["J2"], 3))
    R("fw-rs-FkN", fmt(s["F_vac"] / 1e3))
    R("fw-rs-m", fmt(s["mass"]))
    R("fw-rs", fmt(n["fw"]["RS25"], 3))
    R("fw-sp125-lo", fmt(SP125_ENGINE_FW[0], 2))
    R("fw-sp125-hi", fmt(SP125_ENGINE_FW[1], 3))
    R("pf-pump", fmt(SP125_PROP_FRACTION["pump"], 2))
    R("pf-press", fmt(SP125_PROP_FRACTION["pressure"], 2))
    R("tank-pump-lo", fmt(TANK_PSIA["pump"][0], 2))
    R("tank-pump-hi", fmt(TANK_PSIA["pump"][1], 3))
    R("tank-press-hi", fmt(TANK_PSIA["pressure"][1], 3))
    R("tank-pump-lo-MPa", fmt(TANK_PSIA["pump"][0] * PSI / 1e6, 1))
    R("tank-pump-hi-MPa", fmt(TANK_PSIA["pump"][1] * PSI / 1e6, 1))
    R("tank-press-hi-MPa", fmt(TANK_PSIA["pressure"][1] * PSI / 1e6, 2))
    # worked example 2
    R("ex2-mprop", fmt(TANK["m_prop"]))
    R("ex2-r", fmt(TANK["r"], 3))
    R("ex2-r1", fmt(1.0 + TANK["r"], 3))
    R("ex2-mox", fmt(n["m_ox"]))
    R("ex2-mf", fmt(n["m_f"]))
    R("ex2-rhoox", fmt(n["rho_ox"]))
    R("ex2-rhof", fmt(n["rho_f"], 3))
    R("ex2-rhof-hi", fmt(RP1_RHO_RANGE[1], 3))
    R("ex2-Vox", fmt(n["V_ox"]))
    R("ex2-Vf", fmt(n["V_f"]))
    R("ex2-ull", fmt(100 * TANK["ullage"], 1))
    R("ex2-ull-sp125", fmt(100 * SP125_ULLAGE, 2))
    R("ex2-Vtox", fmt(n["Vt_ox"]))
    R("ex2-Vtf", fmt(n["Vt_f"]))
    R("ex2-dox", fmt(n["d_ox"]))
    R("ex2-df", fmt(n["d_f"]))
    R("ex2-stage", fmt(TANK["stage_d"], 2))
    R("ex2-share-m", fmt(100 * n["mass_share_ox"], 3))
    R("ex2-share-v", fmt(100 * n["vol_share_ox"], 3))
    R("ex2-vratio", fmt(n["vol_ratio"], 3))
    R("ex2-stack", fmt(n["stack"], 3))
    # worked example 3
    R("ex3-Sw-psi", fmt(AL_SW_PSI))
    R("ex3-Sw", fmt(n["Sw"] / 1e6))
    R("ex3-rho", fmt(n["rho_al"]))
    R("ex3-r", fmt(n["r_ox"]))
    R("ex3-p1", fmt(P_PUMP / 1e6, 1))
    R("ex3-p2", fmt(P_PRESS / 1e6, 2))
    R("ex3-t1", fmt(n["t_pump"] * 1000.0, 3))
    R("ex3-t2", fmt(n["t_press"] * 1000.0, 3))
    R("ex3-m1", fmt(n["m_pump"], 3))
    R("ex3-m2", fmt(n["m_press"], 3))
    R("ex3-tmin", fmt(n["t_min"] * 1000.0, 3))
    R("ex3-tmin-in", fmt(AL_MIN_WALL_IN, 2))
    # worked example 4
    R("ex4-m", fmt(BOIL["m"]))
    R("ex4-Q", fmt(BOIL["Q"], 2))
    R("ex4-h", fmt(n["h_vap"] / 1000.0))
    R("ex4-rate", fmt_sci(n["rate"]).replace("10^", "{10}^"))
    R("ex4-rate-day", fmt(n["rate_day"]))
    R("ex4-days", fmt(BOIL["days"], 1))
    R("ex4-lost", fmt(n["lost"]))
    R("ex4-pct", fmt(n["lost_pct"], 2))
    R("ex4-h-ox", fmt(NIST["oxygen"]["h_vap"]))
    R("ex4-Tb-h2", fmt(NIST["hydrogen"]["Tb"]))
    R("ex4-rp1-boil", fmt((RP1_BOIL_F - 32.0) * 5.0 / 9.0, 3))
    R("ex4-empty", fmt(n["empty_days"], 3))
    R("h2-normal-diff", f"less than {math.ceil(100.0 * n['h2_diff'])}%")
    R("cool-lh2-cut", f"{fmt(100.0 * PLACHTA_LH2_CUT, 2)}%")
