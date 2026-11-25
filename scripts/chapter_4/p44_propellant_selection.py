"""Figures and values of 4.4 Propellant Selection (notes/chapter-4/propellant-selection.md).

One function per figure, make_all() for the runner, and values() for every number the page prints.
Run through the runner from the book folder:

    FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_4_figures.py p44

Published numbers come from chapter_4/published.py. The few this page needs and the shared module does
not hold are defined below, each with its source (opened 2026-11-24). The worked example (the apogee
burn of a geostationary communications satellite) uses invented values only for the satellite mass and
the inert mass fraction of the bipropellant system; everything else is published.
"""
from chapter_4.common import *  # noqa: F401,F403
import matplotlib  # noqa: E402
import matplotlib.ticker  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

PAGE = "p44"


# ------------------------------------------------------------------ invented values of the worked example
EX_M_PAY = 2350.0          # kg: the satellite without its apogee propulsion system (invented)
EX_F_BIPROP = 0.20         # assumed inert mass fraction of the pressure-fed bipropellant system (reason on the page)
LV_GUIDE = (0.003, 0.10)   # payload shares of the two guide lines of the launch-vehicle chart (they bracket every vehicle)


def _c(K):
    return K - 273.15


def _K(deg_f):
    return f_to_k(deg_f)


def _num(x, nd=None, sig=4):
    return fmt_dec(x, nd) if nd is not None else fmt(x, sig)


# ================================================================== the computations
def apogee_burn():
    """The apogee burn from a transfer orbit with the perigee and apogee altitudes of Ariane 5's standard
    transfer orbit, taken in the equator plane, to the geostationary orbit: a coplanar circularization with
    page 2.2's vis-viva equation and circular speed (the 6 deg plane change of the real orbit is left out,
    since page 2.2 does not teach the combined burn). Printed digits feed the next step."""
    mu, R = MU["Earth"], RADIUS["Earth"]
    rp, ra = R + GTO_HP, R + GTO_HA
    a = 0.5 * (rp + ra)
    va = math.sqrt(mu * (2.0 / ra - 1.0 / a))
    vc = math.sqrt(mu / ra)
    va_p, vc_p = float(fmt(va).replace(",", "")), float(fmt(vc).replace(",", ""))
    dv = vc_p - va_p                                       # coplanar: the speeds add along one line
    return dict(rp=rp, ra=ra, a=a, va=va, vc=vc, va_p=va_p, vc_p=vc_p, dv=dv,
                dv_ms=round(float(fmt(dv)) * 1000.0))


def _p(s):
    return float(s.replace(",", ""))


def size_option(m_pay, dv, isp, f):
    """Stage sizing of page 4.2 with every step computed from the printed digits of the step before."""
    c = isp * G0
    c_s = fmt(c)
    x = dv / _p(c_s)
    x_s = fmt(x, 5)
    e = math.exp(_p(x_s))
    e_s = fmt(e, 5)
    num = m_pay * (_p(e_s) - 1.0) * (1.0 - f)
    num_s = fmt(num)
    den = 1.0 - f * _p(e_s)
    den_s = fmt(den, 5)
    mp = _p(num_s) / _p(den_s)
    mp_s = fmt(mp)
    mi_inert = f * _p(mp_s) / (1.0 - f)
    mi_inert_s = fmt(mi_inert)
    m_i = m_pay + _p(mi_inert_s) + _p(mp_s)
    m_i_s = fmt(m_i)
    full = size_stage(m_pay, dv, isp=isp, f_inert=f)          # the shared code, full precision
    close_to(mp, full["m_prop"], 2e-3, "printed chain against size_stage", rel=True)
    return dict(c=c, c_s=c_s, x_s=x_s, e_s=e_s, num_s=num_s, den_s=den_s, mp=_p(mp_s), mp_s=mp_s,
                mi_inert=_p(mi_inert_s), mi_inert_s=mi_inert_s, m_i=_p(m_i_s), m_i_s=m_i_s, full=full)


def example():
    """Every number of the worked example."""
    burn = apogee_burn()
    dv = burn["dv_ms"]
    # option A: a solid motor modeled on Vega's third stage, Zefiro 9
    z9 = [s for s in STAGES if s[0] == "Zefiro 9"][0]
    f_solid = inert_mass_fraction(z9[3], z9[4])
    f_solid_s = fmt(f_solid)
    isp_solid = STAGE_ISP_VAC["Zefiro 9"]
    rho_solid = SOLID_AP_AL["density_lb_in3"] * LB_KG / IN3_M3
    A = size_option(EX_M_PAY, dv, isp_solid, _p(f_solid_s))
    A["V"] = A["mp"] / float(fmt(rho_solid).replace(",", ""))
    # option B: a storable bipropellant engine as on Vega's AVUM (nitrogen tetroxide and UDMH, pressure-fed)
    isp_b = STAGE_ISP_VAC["AVUM"]
    r_b = AVUM_NTO_KG / AVUM_UDMH_KG
    r_b_s = fmt(r_b)
    B = size_option(EX_M_PAY, dv, isp_b, EX_F_BIPROP)
    rho_ox = SP125_PROPERTIES["nitrogen tetroxide"][2] * 1000.0
    rho_fu = SP125_PROPERTIES["UDMH"][2] * 1000.0
    m_ox = B["mp"] * _p(r_b_s) / (1.0 + _p(r_b_s))
    m_fu = B["mp"] / (1.0 + _p(r_b_s))
    m_ox_s, m_fu_s = fmt(m_ox), fmt(m_fu)
    V_ox = _p(m_ox_s) / rho_ox
    V_fu = _p(m_fu_s) / rho_fu
    V_ox_s, V_fu_s = fmt(V_ox), fmt(V_fu)
    B.update(r=r_b, r_s=r_b_s, m_ox=_p(m_ox_s), m_fu=_p(m_fu_s), m_ox_s=m_ox_s, m_fu_s=m_fu_s, rho_ox=rho_ox,
             rho_fu=rho_fu, V_ox=_p(V_ox_s), V_fu=_p(V_fu_s), V_ox_s=V_ox_s, V_fu_s=V_fu_s,
             V=_p(V_ox_s) + _p(V_fu_s), rho_bulk=bulk_density(_p(r_b_s), rho_ox, rho_fu))
    # the inert mass fraction at which option B would weigh as much as option A at the start
    lo, hi = 0.05, 0.30
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if size_stage(EX_M_PAY, dv, isp=isp_b, f_inert=mid)["m_i"] < A["m_i"]:
            lo = mid
        else:
            hi = mid
    return dict(burn=burn, dv=dv, f_solid=f_solid, f_solid_s=f_solid_s, isp_solid=isp_solid, rho_solid=rho_solid,
                A=A, B=B, isp_b=isp_b, f_even=0.5 * (lo + hi), z9=z9)


def same_impulse():
    """Two propellant loads that give the same total impulse (m_prop c): 100 t of oxygen and kerosene against
    oxygen and hydrogen, with SP-125's specific impulses and mixture ratios; component densities from NIST
    (oxygen, hydrogen) and the chapter's kerosene density (published.RP1_RHO, SP-125 Table 1-4)."""
    k, h = propellant_si("LOX/RP-1"), propellant_si("LOX/LH2")
    rho_lox, rho_lh2 = NIST["oxygen"]["rho"], NIST["hydrogen"]["rho"]
    rho_rp1 = RP1_RHO
    out = {}
    for key, P, m, rho_f in (("kero", k, 100000.0, rho_rp1), ("hydro", h, 100000.0 * k["isp"] / h["isp"], rho_lh2)):
        r = P["r"]
        mo, mf = m * r / (1 + r), m / (1 + r)
        out[key] = dict(m=m, r=r, m_ox=mo, m_fu=mf, V_ox=mo / rho_lox, V_fu=mf / rho_f, rho_f=rho_f,
                        V=mo / rho_lox + mf / rho_f, isp=P["isp"])
        # the total as printed is the sum of the two printed parts, so a reader who adds them gets it
        # (oxygen and kerosene: 63.01 + 35.11 = 98.12, against 98.13 from the unrounded parts)
        out[key]["V_s"] = fmt(float(fmt(mo / rho_lox).replace(",", "")) + float(fmt(mf / rho_f).replace(",", "")))
    close_to(out["kero"]["m"] * out["kero"]["isp"], out["hydro"]["m"] * out["hydro"]["isp"], 1e-9, "same impulse", rel=True)
    out["rho_lox"], out["rho_lh2"], out["rho_rp1"] = rho_lox, rho_lh2, rho_rp1
    return out


def propellant_rows():
    """Rows of the propellant table: name, class, mixture ratio, I_s (s), bulk density (kg/m^3), chamber
    temperature (K), molecular weight of the exhaust; None where the source gives nothing."""
    rows = []
    for key, cls in (("LOX/LH2", "cryogenic bipropellant"), ("LOX/RP-1", "bipropellant, cryogenic oxidizer"),
                     ("NTO/MMH", "storable bipropellant, hypergolic")):
        P = propellant_si(key)
        rows.append(dict(key=key, name=P["name"], cls=cls, r=P["r"], isp=P["isp"], rho=P["rho_bulk"], Tc=P["Tc"],
                         M=P["M"]))
    rows.append(dict(key="NTO/UDMH", name="nitrogen tetroxide and UDMH", cls="storable bipropellant, hypergolic",
                     r=NTO_UDMH["r"], isp=NTO_UDMH["Is"], rho=NTO_UDMH["d"] * 1000.0, Tc=_K(NTO_UDMH["Tc_F"]),
                     M=NTO_UDMH["M"]))
    rows.append(dict(key="N2H4", name="hydrazine", cls="storable monopropellant", r=None, isp=HYDRAZINE_MONO["Is"],
                     rho=SP125_PROPERTIES["hydrazine"][2] * 1000.0, Tc=None, M=None))
    lo, hi = SOLID_AP_AL["Tc_F"]
    rows.append(dict(key="solid", name="ammonium perchlorate, aluminum and HTPB binder", cls="solid",
                     r=None, isp=SOLID_AP_AL["Is"], rho=SOLID_AP_AL["density_lb_in3"] * LB_KG / IN3_M3,
                     Tc=(_K(lo), _K(hi)), M=None))
    return rows


def liquid_ranges():
    """Freezing and boiling points (K) at one atmosphere: SP-125 Tables 1-4 and 1-5 (deg F), with NIST's
    boiling points for oxygen and hydrogen (they agree with SP-125 within 0.1 K)."""
    S = SP125_PROPERTIES
    out = [("liquid hydrogen", _K(S["liquid hydrogen"][0]), NIST["hydrogen"]["Tb"], "cryo"),
           ("liquid oxygen", _K(S["liquid oxygen"][0]), NIST["oxygen"]["Tb"], "cryo"),
           ("nitrogen tetroxide", _K(S["nitrogen tetroxide"][0]), _K(S["nitrogen tetroxide"][1]), "store"),
           ("MMH", _K(S["MMH"][0]), _K(S["MMH"][1]), "store"),
           ("hydrazine", _K(S["hydrazine"][0]), _K(S["hydrazine"][1]), "store"),
           ("kerosene (RP-1)", _K(S["RP-1"][0][1]), _K(S["RP-1"][1][0]), "store")]
    return out


def lh2_bulk_nist():
    """Bulk density of liquid oxygen and liquid hydrogen at SP-125's mixture ratio (4.02) from the NIST
    liquid densities, with the page's bulk-density equation (SP-125 Table 1-10 lists 0.28 g/cc)."""
    return bulk_density(propellant_si("LOX/LH2")["r"], NIST["oxygen"]["rho"], NIST["hydrogen"]["rho"])


def liftoff_rows():
    out = []
    for v in LAUNCH_VEHICLES:
        if v["name"] in LIFTOFF_THRUST:
            F = LIFTOFF_THRUST[v["name"]]
            out.append(dict(name=v["name"], F=F, m=v["liftoff"], FW=F / (v["liftoff"] * G0)))
    return sorted(out, key=lambda d: d["FW"])


def big_engines():
    """Large engines and motors for the specific impulse against thrust chart: (name, thrust N, I_sp s, kind)."""
    rs, f1, j2, vu = engine_si(RS25), engine_si(F1), engine_si(J2), engine_si(VULCAIN2)
    return [("RS-25, vacuum", rs["F_vac"], rs["isp_vac"], "liquid"),
            ("F-1, sea level", f1["F_sl"], f1["isp_sl"], "liquid"),
            ("J-2, vacuum", j2["F_vac"], j2["isp_vac"], "liquid"),
            ("Vulcain 2, vacuum", vu["F_vac"], vu["isp_vac"], "liquid"),
            ("HM7B (ESC-A), vacuum", ESCA_F, STAGE_ISP_VAC["ESC-A"], "liquid"),
            ("AVUM engine, vacuum", AVUM_F_VAC, STAGE_ISP_VAC["AVUM"], "liquid"),
            ("P80, vacuum", P80_F_VAC, STAGE_ISP_VAC["P80"], "solid"),
            ("Zefiro 9, vacuum", Z9_F_VAC, STAGE_ISP_VAC["Zefiro 9"], "solid"),
            ("Ariane 5 booster, at liftoff", EAP_LIFTOFF_F, EAP_LIFTOFF_ISP, "solid")]


# ================================================================== figures
def engine_kinds():
    fig, ax = canvas(6.5, xlim=(-2.6, 13.3), ylim=(-1.9, 9.6))
    L = liquid_engine("pump", origin=(0.0, 0.0))
    # the turbine exhaust duct is left out here: between the tanks it cannot carry a name whose leader does not
    # read as the duct itself, and the lesson of this figure is where the propellants are kept
    tx, tz = L["points"]["turbine_exhaust"]
    n0 = len(L["pipes"])
    L["pipes"] = [pl for pl in L["pipes"] if not (len(pl) == 2 and abs(pl[1][0] - tx) < 1e-9 and abs(pl[1][1] - tz) < 1e-9)]
    assert len(L["pipes"]) == n0 - 1
    S = solid_motor(origin=(5.6, 0.0))
    H = hybrid_motor(origin=(10.4, 0.0))
    PL, PS, PH = draw_schematic(ax, L), draw_schematic(ax, S), draw_schematic(ax, H)

    def lab(P, Sx, name, s_, at, **kw):
        return label_part(ax, P, Sx["parts"], name, s_, at, **kw)
    lab(PL, L, "fuel_tank", "fuel", (-1.85, 7.75), ha="center")
    lab(PL, L, "oxidizer_tank", "oxidizer", (1.95, 7.75), ha="center")
    lab(PL, L, "fuel_pump", "fuel\npump", (-2.0, 4.85), ha="center")
    lab(PL, L, "oxidizer_pump", "oxidizer\npump", (2.15, 3.85), ha="center")
    # the turbine named centered between the two tank lines (x = -0.8 and 0.8), above it, with a short
    # slanted leader (no pipe crossed); the pumps are named as on the page on engines and tanks
    lab(PL, L, "turbine", "turbine", (0.0, 4.88), ha="center", target=(0.14, 4.2), fs=FS_SMALL)

    lab(PL, L, "gas_generator", "gas\ngenerator", (-2.15, 3.2), ha="center")
    lab(PL, L, "thrust_chamber", "thrust\nchamber", (1.85, 1.2), ha="center")
    lab(PS, S, "case", "case", (4.0, 7.0), ha="center", target=(5.6 - 0.72, 5.6))
    lab(PS, S, "grain", "solid\npropellant", (3.75, 2.55), ha="center", target=(5.6 - 0.45, 3.3))
    lab(PS, S, "igniter", "igniter", (7.1, 7.4), ha="center")
    lab(PS, S, "port", "port", (7.2, 3.8), ha="center", target=(5.6, 3.8))
    lab(PS, S, "nozzle", "nozzle", (7.1, 0.6), ha="center")
    lab(PH, H, "oxidizer_tank", "liquid\noxidizer", (12.2, 7.4), ha="center")
    lab(PH, H, "grain", "solid fuel", (12.3, 3.1), ha="center", target=(10.4 + 0.4, 3.0))
    lab(PH, H, "nozzle", "nozzle", (11.95, 0.6), ha="center")
    for x, title, note in ((0.0, "liquid bipropellant", "fuel and oxidizer\nin separate tanks"),
                           (5.6, "solid", "fuel and oxidizer\nmixed in the grain"),
                           (10.4, "hybrid", "solid fuel in the case,\nliquid oxidizer in a tank")):
        text(ax, (x, 9.05), title, va="bottom", fontweight="bold")
        text(ax, (x, -0.55), note, va="top", fs=FS_SMALL)
    # what the drawing asserts: the liquid engine keeps its two propellants in two tanks, the solid in one grain
    assert {"fuel_tank", "oxidizer_tank"} <= set(L["parts"]) and "grain" in S["parts"] and "oxidizer_tank" in H["parts"]
    assert "grain" in H["parts"] and "oxidizer_tank" not in S["parts"]
    trim_canvas(fig)
    save_figure(fig, "p44-engine-kinds")


def isp_thrust_map():
    fig, ax = data_axes(6.5, 5.0)
    log_axis(ax, "x", 1e-5, 1e9, "power", "Thrust, $F$, N")
    log_axis(ax, "y", 20.0, 10000.0, "comma", "Specific impulse, $I_\\text{sp}$, s")
    ion, hall = SOA["gridded ion"], SOA["Hall-effect"]
    items = [
        dict(name="cold gas", x0=SOA["cold gas"][2], x1=SOA["cold gas"][3], y0=SOA["cold gas"][0], y1=SOA["cold gas"][1]),
        dict(name="electric (ion and Hall)", x0=min(ion[2], hall[2]), x1=max(ion[3], hall[3]),
             y0=min(ion[0], hall[0]), y1=max(ion[1], hall[1]), callout=(3e-2, 6000.0), target=(2e-3, 2000.0), ha="left"),
        dict(name="hydrazine monopropellant", x0=SOA["hydrazine monopropellant"][2],
             x1=SOA["hydrazine monopropellant"][3], y0=SOA["hydrazine monopropellant"][0],
             y1=SOA["hydrazine monopropellant"][1], callout=(0.1, 148.0), target=(1.0, 200.0), ha="left"),
        # the hybrid box overlaps the monopropellant box: outline only, so both outlines show through the overlap
        dict(name="hybrid", x0=SOA["hybrid"][2], x1=SOA["hybrid"][3], y0=SOA["hybrid"][0], y1=SOA["hybrid"][1],
             callout=(4.0e1, 480.0), target=(60.0, 285.0), ha="center", fill=False),
        dict(name="nuclear thermal", x0=NERVA[2], x1=NERVA[3], y0=NERVA[0], y1=NERVA[1],
             callout=(6.0e4, 2600.0), target=(1.5e5, 870.0), ha="center"),
    ]
    patches, labels = range_boxes(ax, items)
    for it, pa in zip(items, patches):
        close_to(pa.get_x(), it["x0"], 1e-12 * it["x0"], "box drawn from its range")
    # the condition of the four small boxes, written on the chart under them
    text(ax, (1.4e-5, 29.0), "cold gas, monopropellant, hybrid, and electric boxes: small-spacecraft devices only",
         direction=0.0, dist=0.0, fs=FS_SMALL, color=STEEL, va="center")
    eng = [e for e in big_engines() if not e[0].startswith("F-1")]
    pos = {}
    for name, F, isp, kind in eng:
        ax.plot([F], [isp], "o" if kind == "liquid" else "s", ms=6.5, mfc="white" if kind == "liquid" else STEEL,
                mec=INK, mew=1.3, zorder=7)
        pos[name.split(",")[0]] = (F, isp)
    # each engine and motor named on the chart (the caption names them too)
    text(ax, pos["AVUM engine"], "AVUM", direction=90.0, dist=6.0, fs=FS_SMALL)
    text(ax, pos["HM7B (ESC-A)"], "HM7B", direction=90.0, dist=6.0, fs=FS_SMALL)
    text(ax, pos["Zefiro 9"], "Zefiro 9", direction=180.0, dist=6.0, fs=FS_SMALL)
    text(ax, pos["P80"], "P80", direction=-115.0, dist=6.0, fs=FS_SMALL, backing=False)
    # the three large liquid engines sit close together: a column of names to their right, leaders fanning out
    for nm, y in (("RS-25", 560.0), ("Vulcain 2", 1000.0), ("J-2", 1500.0)):
        an = ax.annotate(nm, xy=pos[nm], xytext=(8.0e6, y), ha="left", va="center", fontsize=FS_SMALL, color=INK,
                         zorder=10, annotation_clip=False, bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"),
                         arrowprops=dict(arrowstyle="-", color=INK, lw=0.7, shrinkA=1.0, shrinkB=4.0, relpos=(0.0, 0.5)))
        an.arrow_patch.set_gid("leader")                       # the leader leaves the label's left end
    text(ax, pos["Ariane 5 booster"], "Ariane 5 booster,\nat liftoff", direction=0.0, dist=6.0, fs=FS_SMALL, ha="left")
    # key for the two kinds of engine points, in the empty lower right
    kx, ky = 1.0e3, 70.0
    ax.plot([kx], [ky], "o", ms=6.5, mfc="white", mec=INK, mew=1.3, zorder=7)
    text(ax, (kx, ky), "liquid engines of launch vehicles", direction=0.0, dist=7.0, fs=FS_SMALL)
    ax.plot([kx], [ky / 1.45], "s", ms=6.5, mfc=STEEL, mec=INK, mew=1.3, zorder=7)
    text(ax, (kx, ky / 1.45), "solid motors of launch vehicles", direction=0.0, dist=7.0, fs=FS_SMALL)
    # the lesson, measured: the devices above 1,000 s give less than 0.1 N; every device above 1 MN is chemical,
    # apart from the nuclear thermal engine, which stops near 1.1 MN
    assert max(ion[3], hall[3]) < 0.1 and max(isp for _, F, isp, _ in eng if F > 1e6) < 460.0
    assert NERVA[3] < 2e6 < max(F for _, F, _, _ in eng)
    save_figure(fig, "p44-isp-thrust-map")


def launch_vehicle_classes():
    fig, ax = data_axes(6.5, 4.6)
    x0, x1, y0, y1 = 5e3, 2e7, 100.0, 3e5
    log_axis(ax, "x", x0, x1, "comma", "Liftoff mass, kg")
    log_axis(ax, "y", y0, y1, "comma", "Payload to low Earth orbit, kg")
    class_bands(ax, [(n + " lift", lo, hi) for n, lo, hi in LV_CLASSES], label_x=6.0e3, ha="left")
    # two lines of constant payload share bracket every vehicle: payload grows in proportion to liftoff mass
    shares = [v["payload"] / v["liftoff"] for v in LAUNCH_VEHICLES]
    lo_s, hi_s = LV_GUIDE
    assert lo_s < min(shares) and max(shares) < hi_s, shares
    xe = {lo_s: (x0 * 8.0, x1), hi_s: (x0 * 2.0, x1)}                # ends kept clear of the class names
    for s_ in (lo_s, hi_s):
        xa, xb = max(xe[s_][0], y0 / s_), min(xe[s_][1], y1 / s_)
        ax.plot([xa, xb], [s_ * xa, s_ * xb], color=STEEL, lw=1.1, ls=(0, (2.0, 2.0)), zorder=2)
    # each guide line named in the clear space beside its lower end
    text(ax, (3.0e5, 330.0), f"payload = {fmt_dec(100.0 * lo_s, 1)}%\nof liftoff mass", direction=0.0, dist=0.0, fs=FS_SMALL, color=STEEL,
         ha="left", va="center", backing=False)
    text(ax, (1.4e6, 2.3e5), f"payload = {fmt(100.0 * hi_s, 2)}% of liftoff mass", direction=0.0, dist=0.0, fs=FS_SMALL, color=STEEL,
         ha="right", va="center", backing=False)
    side = {"Falcon Heavy": (1.2, 1.0, "left", "center"), "Falcon 9": (1.06, 1.22, "left", "bottom"),
            "Space Shuttle": (0.9, 1.3, "left", "bottom"), "Ariane 5 ES": (1.0, 1 / 1.22, "center", "top"),
            "Electron": (1.2, 1.0, "left", "center"), "LVM3": (1.2, 1.0, "left", "center"),
            "Vega C": (1 / 1.2, 1.15, "right", "bottom"), "PSLV-XL": (1 / 1.2, 0.85, "right", "center")}
    band_fill = ("#F2F2F2", "#FFFFFF")                       # class_bands' two fills, small lift first

    def fill_at(y):
        i = [k for k, (_, lo, hi) in enumerate(LV_CLASSES) if lo <= y < hi][0]
        return band_fill[i % 2]
    near = {}
    for v in LAUNCH_VEHICLES:
        if v["name"] in side:
            fx, fy, ha, va = side[v["name"]]
            # no white box on the gray bands: each name is backed by the fill of the band it sits in
            named_scatter(ax, [dict(name=v["name"], x=v["liftoff"], y=v["payload"],
                                    label_at=[(v["liftoff"] * fx, v["payload"] * fy, ha, va)])],
                          backing=fill_at(v["payload"] * fy))
        else:
            near[v["name"]] = v
            ax.plot([v["liftoff"]], [v["payload"]], "o", ms=6.5, mfc="white", mec=INK, mew=1.4, zorder=6)
    # Saturn V and SLS Block 1 almost touch: each name to the right, one above the other, with a short leader
    for nm, at in (("Saturn V", (6.0e6, 2.2e5)), ("SLS Block 1", (6.0e6, 1.35e5))):
        v = near[nm]
        an = ax.annotate(nm, xy=(v["liftoff"], v["payload"]), xytext=at, ha="left", va="center", fontsize=FS_SMALL,
                         color=INK, zorder=10, annotation_clip=False, bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"),
                         arrowprops=dict(arrowstyle="-", color=INK, lw=0.7, shrinkA=1.0, shrinkB=4.0, relpos=(0.0, 0.5)))
        an.arrow_patch.set_gid("leader")                     # the leader leaves the name's left end
    assert set(near) == {"Saturn V", "SLS Block 1"}
    # payload grows with liftoff mass: the order by liftoff mass and by payload agree for most vehicles
    lm = np.log10([v["liftoff"] for v in LAUNCH_VEHICLES])
    lp = np.log10([v["payload"] for v in LAUNCH_VEHICLES])
    assert np.corrcoef(lm, lp)[0, 1] > 0.9
    save_figure(fig, "p44-launch-vehicle-classes")


def isp_density():
    fig, ax = data_axes(6.5, 4.2)
    ax.set_xlim(0, 2000)
    ax.set_ylim(240, 420)
    rows = {r["key"]: r for r in propellant_rows()}
    h, k, m, u = rows["LOX/LH2"], rows["LOX/RP-1"], rows["NTO/MMH"], rows["NTO/UDMH"]
    pts = [dict(name="oxygen and hydrogen", x=h["rho"], y=h["isp"], label_at=[(h["rho"] + 45.0, h["isp"], "left", "center")]),
           dict(name="oxygen and kerosene", x=k["rho"], y=k["isp"], label_at=[(k["rho"] + 40.0, k["isp"] + 4.0, "left", "bottom")]),
           dict(name="nitrogen tetroxide and MMH", x=m["rho"], y=m["isp"],
                label_at=[(m["rho"] + 40.0, m["isp"] + 1.0, "left", "center")])]
    named_scatter(ax, pts, fs=FS_SMALL)
    ax.plot([u["rho"]], [u["isp"]], "o", ms=6.5, mfc="white", mec=INK, mew=1.4, zorder=6)
    # the UDMH pair sits almost on the MMH pair: its name below, with a short leader
    callout(ax, (u["rho"], u["isp"]), "nitrogen tetroxide and UDMH", (u["rho"] - 60.0, 272.0), fs=FS_SMALL, ha="right")
    # the solid: the solid-motor square of the specific impulse and thrust chart at the middle of its range,
    # with a bar over the range the source gives
    s = rows["solid"]
    lo, hi = s["isp"]
    ax.plot([s["rho"], s["rho"]], [lo, hi], color=INK, lw=1.4, solid_capstyle="butt", zorder=6)
    for yy in (lo, hi):
        ax.plot([s["rho"] - 14.0, s["rho"] + 14.0], [yy, yy], color=INK, lw=1.4, zorder=6)
    ax.plot([s["rho"]], [0.5 * (lo + hi)], "s", ms=6.5, mfc=STEEL, mec=INK, mew=1.3, zorder=7)
    text(ax, (s["rho"] - 14.0, hi), "solid propellant,\n260 to 265 s", direction=180.0, dist=5.0, fs=FS_SMALL,
         va="bottom")
    # the two directions of "better", as arrows from the lower left
    arrow(ax, (120.0, 262.0), (120.0, 318.0), color=STEEL, lw=1.3)
    text(ax, (120.0, 318.0), "higher specific impulse:\nless propellant mass", direction=0.0, dist=6.0, fs=FS_SMALL,
         va="top", color=STEEL)
    arrow(ax, (120.0, 250.0), (560.0, 250.0), color=STEEL, lw=1.3)
    text(ax, (560.0, 250.0), "higher density: smaller tanks", direction=0.0, dist=6.0, fs=FS_SMALL, color=STEEL)
    ax.set_xlabel("Bulk density, kg/m³")
    ax.set_ylabel("Specific impulse, $I_\\text{sp}$, s")
    # the lesson, measured: hydrogen has the highest specific impulse and the lowest density; the solid the reverse
    liq = [h, k, m, u]
    assert max(liq, key=lambda r: r["isp"])["key"] == "LOX/LH2" == min(liq, key=lambda r: r["rho"])["key"]
    assert s["rho"] > max(r["rho"] for r in liq) and hi < min(r["isp"] for r in liq)
    save_figure(fig, "p44-isp-density")


TANK_STYLE = {"oxidizer": LIQUID_STYLE["oxidizer"], "fuel": LIQUID_STYLE["fuel"], "lh2": PROPELLANT_STYLE["lh2"],
              "solid": LIQUID_STYLE["solid"]}


def _fill_poly_public(ax, xy, style, z=3.0):
    return fill_region(ax, xy, style, z, LW_DETAIL + 0.4)


def tank_volumes():
    """Two propellant loads with the same total impulse, as tanks of one diameter lying on their side, to scale."""
    s = same_impulse()
    D = 4.0
    A = math.pi * D * D / 4.0
    fig, ax = canvas(6.5, xlim=(-0.5, 23.5), ylim=(-15.0, 2.6))
    rows = (("kero", "oxygen and kerosene", "kerosene", "fuel", 0.0),
            ("hydro", "oxygen and hydrogen, same total impulse", "liquid hydrogen", "lh2", -7.4))
    lengths = {}
    for key, title, fuel_name, fuel_sty, y in rows:
        d = s[key]
        x = 0.0
        segs = (("oxidizer", d["V_ox"], "liquid oxygen"), (fuel_sty, d["V_fu"], fuel_name))
        for sty, V, label in segs:
            L = V / A
            _fill_poly_public(ax, [(x, y - D / 2), (x + L, y - D / 2), (x + L, y + D / 2), (x, y + D / 2)], TANK_STYLE[sty])
            text(ax, (x + 0.5 * L, y - D / 2), f"{label}\n{fmt(V)} m³", va="top", dist=4.0, direction=-90.0, fs=FS_SMALL)
            x += L
        lengths[key] = x
        close_to(x, d["V"] / A, 1e-9, "row length from the volume")
        text(ax, (0.0, y + D / 2), f"{title}: {fmt(d['m'] / 1000.0)} t, {d['V_s']} m³", direction=90.0, dist=5.0,
             ha="left", fs=FS_LABEL)
    for xx in (18.0, 23.0):
        ax.plot([xx, xx], [0.55, 1.05], color=INK, lw=LW_THIN)
    ax.plot([18.0, 23.0], [0.8, 0.8], color=INK, lw=LW_THIN + 0.4)
    text(ax, (20.5, 1.05), "5 m", direction=90.0, dist=3.0, fs=FS_SMALL)
    # the lesson on the figure: the ratio of the two volumes, under the right end of the longer row
    ratio = s["hydro"]["V"] / s["kero"]["V"]
    text(ax, (lengths["hydro"], -7.4 - D / 2), f"{fmt(ratio, 4)} × the volume\nof the kerosene load", direction=-90.0,
         dist=4.0, ha="right", fs=FS_SMALL)
    # the lesson, measured: the lighter load (hydrogen) needs the longer tanks
    assert s["hydro"]["m"] < s["kero"]["m"] and lengths["hydro"] > 2.5 * lengths["kero"]
    trim_canvas(fig)
    save_figure(fig, "p44-tank-volumes")


def storage_temperatures():
    fig, ax = data_axes(6.5, 4.6)
    rng = liquid_ranges()
    sec = temperature_axis(ax, 0.0, 600.0, 100.0)
    xs = np.arange(len(rng))
    # the propellant fills of the rest of the book: hydrogen green dots, oxygen and the oxidizer nitrogen
    # tetroxide blue diagonal hatch, the fuels tan with horizontal lines
    fills = {"liquid hydrogen": PROPELLANT_STYLE["lh2"], "liquid oxygen": LIQUID_STYLE["oxidizer"],
             "nitrogen tetroxide": LIQUID_STYLE["oxidizer"], "MMH": LIQUID_STYLE["fuel"],
             "hydrazine": LIQUID_STYLE["fuel"], "kerosene (RP-1)": LIQUID_STYLE["fuel"]}
    T_room = _K(ROOM_F)
    for i, (name, Tf, Tb, kind) in enumerate(rng):
        fill_region(ax, [(i - 0.28, Tf), (i + 0.28, Tf), (i + 0.28, Tb), (i - 0.28, Tb)], fills[name], z=4.0,
                    edge_lw=1.2)
        ax.plot([i - 0.28, i + 0.28], [Tb, Tb], color=INK, lw=2.2, zorder=5)
    # boiling points of the two cryogens and of nitrogen tetroxide, at their heavy lines
    lr = {n: (Tf, Tb) for n, Tf, Tb, _ in rng}
    for name, i in (("liquid hydrogen", 0), ("liquid oxygen", 1)):
        text(ax, (i + 0.28, lr[name][1]), f"boils at {fmt_dec(_c(lr[name][1]), 0, minus='−')} °C", direction=0.0,
             dist=4.0, fs=FS_SMALL, va="bottom")
    # nitrogen tetroxide: the label sits right on its bar, just above the heavy line, narrow (two lines) so it
    # stays well clear of the MMH bar beside it; the room-temperature label is moved under its line to make room
    nto = text(ax, (2, lr["nitrogen tetroxide"][1]), f"boils at\n{fmt_dec(_c(lr['nitrogen tetroxide'][1]), 0)} °C",
               direction=90.0, dist=4.0, fs=FS_SMALL)
    ax.set_xlim(-0.6, len(rng) - 0.4)
    ax.set_xticks(xs)
    ax.set_xticklabels(["liquid\nhydrogen", "liquid\noxygen", "nitrogen\ntetroxide", "MMH", "hydrazine",
                        "kerosene\n(RP-1)"], fontsize=FS_SMALL)
    ax.grid(axis="x", visible=False)
    # room temperature, drawn behind the bars so the boiling point of nitrogen tetroxide stays visible
    ax.axhline(T_room, color=INK, lw=1.4, ls=(0, (6.0, 3.0)), zorder=3)
    ax.text(-0.5, T_room - 8.0, f"room temperature, {fmt(_c(T_room), 2)} °C", ha="left", va="top", fontsize=FS_SMALL,
            bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"), zorder=6)
    T_cryo = _K(CRYO_LIMIT_F)
    ax.axhline(T_cryo, color=STEEL, lw=1.1, ls=(0, (2.0, 2.0)), zorder=3)
    ax.text(-0.5, T_cryo + 8.0, "cryogenic: boils below this line", ha="left", va="bottom", fontsize=FS_SMALL,
            color=STEEL, bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"), zorder=6)
    ax.text(len(rng) - 0.45, 560.0, "bar: liquid range at sea-level pressure\nheavy line: boiling point", ha="right",
            va="top", fontsize=FS_SMALL, bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"), zorder=6)
    # the lesson, measured: room temperature lies inside every storable's liquid range and above every cryogen's
    for name, Tf, Tb, kind in rng:
        if kind == "cryo":
            assert Tb < T_cryo < T_room, name
        else:
            assert Tf < T_room <= Tb + 1.5, name
    # the nitrogen tetroxide label is centered on its own bar and ends well short of the MMH bar
    fig.canvas.draw()
    bb = nto.get_window_extent().transformed(ax.transData.inverted())
    close_to(0.5 * (bb.x0 + bb.x1), 2.0, 0.02, "the boiling-point label is centered on the nitrogen tetroxide bar")
    assert bb.x1 < 3 - 0.28 - 0.25 and bb.y0 > lr["nitrogen tetroxide"][1], "label above its bar, clear of MMH"
    save_figure(fig, "p44-storage-temperatures")


def example_figure():
    ex = example()
    A, B = ex["A"], ex["B"]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 5.0), gridspec_kw=dict(height_ratios=[1.35, 1.0], hspace=0.55))
    names = ["storable\nbipropellant", "solid motor"]
    for ax in (ax1, ax2):
        ax.set_yticks([0, 1])
        ax.set_yticklabels(names, fontsize=FS_SMALL)
        ax.tick_params(axis="y", length=0)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.grid(axis="x", color="#E0E0E0", lw=0.6, zorder=0)
        ax.set_axisbelow(True)
    # panel 1: mass at the start of the burn, kg, every segment named with the example's numbers
    ax1.set_ylim(-0.9, 1.85)
    ax1.set_xlim(0, 5500)
    ax1.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax1.set_xlabel("Mass at the start of the burn, kg")
    for y, O, side in ((1.0, A, 1), (0.0, B, -1)):
        x = 0.0
        for kind, m in (("payload", EX_M_PAY), ("inert", O["mi_inert"]), ("propellant", O["mp"])):
            _fill_poly_public(ax1, [(x, y - 0.3), (x + m, y - 0.3), (x + m, y + 0.3), (x, y + 0.3)], MASS_STYLE[kind])
            if kind == "payload":
                text(ax1, (x + 0.5 * m, y), f"payload, {fmt(EX_M_PAY)} kg", fs=FS_SMALL, backing=MASS_STYLE[kind]["fill"])
            elif kind == "propellant":
                text(ax1, (x + 0.5 * m, y), f"propellant, {O['mp_s']} kg", fs=FS_SMALL,
                     backing=MASS_STYLE[kind]["fill"])
            else:                                   # the hatched inert segment is named outside, above or below
                text(ax1, (x + 0.5 * m, y + side * 0.3), f"inert mass, {O['mi_inert_s']} kg", direction=90.0 * side,
                     dist=3.0, fs=FS_SMALL)
            x += m
        close_to(x, O["m_i"], 1e-4, "bar length against the printed initial mass", rel=True)
        text(ax1, (x, y), f"{O['m_i_s']} kg", direction=0.0, dist=5.0, fs=FS_SMALL)
    # the difference, marked between the two bar ends
    xa, xb = A["m_i"], B["m_i"]
    ax1.plot([xa, xa], [0.7, 0.3], color=STEEL, lw=LW_THIN, ls=(0, (2.0, 2.0)), zorder=2)
    ax1.plot([xa, xb], [0.5, 0.5], color=INK, lw=LW_THIN + 0.4, solid_capstyle="butt", zorder=3)   # too short for heads
    ax1.plot([xb, xb], [0.42, 0.58], color=INK, lw=LW_THIN, zorder=3)
    text(ax1, (xb, 0.5), f"{fmt(xb - xa, 3)} kg more", direction=0.0, dist=4.0, fs=FS_SMALL)
    # panel 2: propellant volume, m^3
    ax2.set_xlim(0, 1.9)
    ax2.set_ylim(-1.35, 1.5)
    ax2.set_xlabel("Propellant volume, m³")
    _fill_poly_public(ax2, [(0, 0.7), (A["V"], 0.7), (A["V"], 1.3), (0, 1.3)], TANK_STYLE["solid"])
    text(ax2, (A["V"], 1.0), f"solid propellant, {fmt(A['V'])} m³", direction=0.0, dist=5.0, fs=FS_SMALL)
    _fill_poly_public(ax2, [(0, -0.3), (B["V_ox"], -0.3), (B["V_ox"], 0.3), (0, 0.3)], TANK_STYLE["oxidizer"])
    _fill_poly_public(ax2, [(B["V_ox"], -0.3), (B["V"], -0.3), (B["V"], 0.3), (B["V_ox"], 0.3)], TANK_STYLE["fuel"])
    text(ax2, (B["V"], 0.0), f"{fmt(B['V'])} m³", direction=0.0, dist=5.0, fs=FS_SMALL)
    text(ax2, (0.5 * B["V_ox"], -0.3), f"nitrogen tetroxide,\n{fmt(B['V_ox'])} m³", direction=-90.0, dist=3.0,
         fs=FS_SMALL)
    text(ax2, (B["V_ox"] + 0.5 * B["V_fu"], -0.3), f"UDMH,\n{fmt(B['V_fu'])} m³", direction=-90.0, dist=3.0,
         fs=FS_SMALL)
    VA_p, VB_p = float(fmt(A["V"])), float(fmt(B["V"]))
    va_, vb_ = A["V"], B["V"]
    ax2.plot([va_, va_], [0.7, 0.3], color=STEEL, lw=LW_THIN, ls=(0, (2.0, 2.0)), zorder=2)
    arrow(ax2, (va_, 0.5), (vb_, 0.5), color=INK, lw=LW_THIN, head="small", both=True)
    text(ax2, (vb_, 0.5), f"{fmt(VB_p - VA_p, 3)} m³ more", direction=0.0, dist=4.0, fs=FS_SMALL)
    # the lesson, measured: the bipropellant option is heavier and larger, the solid lighter and smaller, and the
    # extra mass is inert mass (the two propellant masses differ by less than 1%)
    assert B["m_i"] > A["m_i"] and B["V"] > A["V"]
    assert abs(B["mp"] - A["mp"]) < 0.01 * A["mp"] and B["mi_inert"] - A["mi_inert"] > B["m_i"] - A["m_i"]
    save_figure(fig, "p44-example")


def make_all():
    engine_kinds()
    isp_thrust_map()
    launch_vehicle_classes()
    isp_density()
    tank_volumes()
    storage_temperatures()
    example_figure()


# ================================================================== values printed on the page
def values():
    P = PAGE
    # kinds of propulsion (table)
    for k in ("cold gas", "hydrazine monopropellant", "hybrid"):
        key = k.split()[0]
        record(P, f"soa-{key}-isp0", f"{SOA[k][0]:,.0f}")
        record(P, f"soa-{key}-isp1", f"{SOA[k][1]:,.0f}")
    record(P, "cold-F0", "10")                       # 10 microN
    record(P, "cold-F1", fmt(SOA["cold gas"][3], 2))
    record(P, "mono-F0", fmt(SOA["hydrazine monopropellant"][2], 2))
    record(P, "mono-F1", fmt(SOA["hydrazine monopropellant"][3], 2))
    record(P, "hyb-F0", fmt(SOA["hybrid"][2], 1))
    record(P, "hyb-F1", fmt(SOA["hybrid"][3], 3))
    record(P, "el-F0", fmt(SOA["gridded ion"][2] * 1e3, 1))
    record(P, "el-F1", fmt(SOA["Hall-effect"][3] * 1e3, 2))
    record(P, "el-isp0", fmt(SOA["Hall-effect"][0], 3))
    record(P, "el-isp1", fmt(SOA["gridded ion"][1]))
    record(P, "ion-max", fmt(ION_MAX))
    record(P, "ion-min", fmt(2000.0))
    record(P, "soa-500w-P", fmt(500.0, 3))
    record(P, "soa-mn-kw", fmt(SOA_MN_PER_KW, 2))
    record(P, "soa-500w", fmt(SOA_500W_MN, 2))
    record(P, "nerva-isp0", fmt(NERVA[0], 3))
    record(P, "nerva-isp1", fmt(NERVA[1], 3))
    record(P, "nerva-F0", fmt(NERVA[2] / 1e3, 3))
    record(P, "nerva-F1", fmt(NERVA[3] / 1e3))
    ntomm = propellant_si("NTO/MMH")
    rs = engine_si(RS25)
    f1 = engine_si(F1)
    record(P, "bi-isp0", fmt(ntomm["isp"], 3))
    record(P, "bi-isp1", fmt(rs["isp_vac"], 4))
    record(P, "avum-F", fmt(AVUM_F_VAC / 1e3, 3))
    record(P, "f1-F", fmt(f1["F_sl"] / 1e3))
    record(P, "eap-isp", fmt(STAGE_ISP_VAC["EAP"], 4))
    record(P, "z9-isp", fmt(STAGE_ISP_VAC["Zefiro 9"], 4))
    record(P, "z9-F", fmt(Z9_F_VAC / 1e3, 3))
    record(P, "srb-F", fmt(SRB_F / 1e3))
    # launch vehicles (table and figure)
    for v in LAUNCH_VEHICLES:
        k = v["name"].lower().replace(" ", "-")
        record(P, f"lv-{k}-pay", f"{v['payload']:,.0f}")
        record(P, f"lv-{k}-m", fmt(v["liftoff"] / 1000.0))
        record(P, f"lv-{k}-share", fmt(100.0 * v["payload"] / v["liftoff"], 2))
        record(P, f"lv-{k}-class", lv_class(v["payload"]))
    record(P, "lv-a5es-hi", f"{[v for v in LAUNCH_VEHICLES if v['name'] == 'Ariane 5 ES'][0]['payload_hi']:,.0f}")
    shares = [100.0 * v["payload"] / v["liftoff"] for v in LAUNCH_VEHICLES]
    record(P, "lv-share-min", fmt(min(shares), 2))
    record(P, "lv-share-max", fmt(max(shares), 2))
    record(P, "lv-rest-min", fmt(100.0 - float(fmt(max(shares), 2)), 3))
    record(P, "launch-23", fmt(LAUNCH_23["total"]))
    record(P, "lv-guide-lo", fmt_dec(100.0 * LV_GUIDE[0], 1))
    record(P, "lv-guide-hi", fmt(100.0 * LV_GUIDE[1], 2))
    for name, lo, hi in LV_CLASSES:
        if hi < float("inf"):
            record(P, f"class-{name.replace(' ', '-')}-hi", f"{hi / 1000.0:.0f}")
    # propellant table
    for r in propellant_rows():
        k = r["key"].lower().replace("/", "-")
        if r["r"]:
            record(P, f"prop-{k}-r", fmt_dec(r["r"], 2))
        if isinstance(r["isp"], tuple):
            record(P, f"prop-{k}-isp0", fmt(r["isp"][0], 3))
            record(P, f"prop-{k}-isp1", fmt(r["isp"][1], 3))
        else:
            record(P, f"prop-{k}-isp", fmt(r["isp"], 3))
        # SP-125 prints bulk densities to two or three figures (0.28, 1.02 g/cc): print them as the source does
        record(P, f"prop-{k}-rho", fmt(r["rho"], 4 if r["key"] == "solid" else 3))
        if isinstance(r["Tc"], tuple):
            record(P, f"prop-{k}-Tc0", fmt(r["Tc"][0]))
            record(P, f"prop-{k}-Tc1", fmt(r["Tc"][1]))
        elif r["Tc"]:
            record(P, f"prop-{k}-Tc", fmt(r["Tc"]))
        if r["M"]:
            record(P, f"prop-{k}-M", fmt_dec(r["M"], 1))
    record(P, "test-lo", fmt(TEST_LOW_PCT[0], 1))
    record(P, "test-hi", fmt(TEST_LOW_PCT[1], 2))
    rows = {r["key"]: r for r in propellant_rows()}
    record(P, "lh2-rp1-isp-ratio", fmt(rows["LOX/LH2"]["isp"] / rows["LOX/RP-1"]["isp"]))
    # the bulk density of oxygen and hydrogen from the page's own equation and the NIST densities (SP-125 lists 280)
    bulk_h = lh2_bulk_nist()
    record(P, "lh2-bulk-nist", fmt(bulk_h))
    record(P, "lh2-r", fmt_dec(rows["LOX/LH2"]["r"], 2))
    record(P, "rp1-lh2-bulk-ratio", fmt(rows["LOX/RP-1"]["rho"] / float(fmt(bulk_h)), 2))
    record(P, "sp125-pc-psia", fmt(1000.0))
    record(P, "sp125-pc-mpa", fmt(1000.0 * PSI / 1e6))
    record(P, "sp125-pe-psia", fmt(14.7, 3))
    record(P, "hyd-pc-psia", fmt(300.0, 3))
    # same total impulse (tank volumes)
    s = same_impulse()
    for key in ("kero", "hydro"):
        d = s[key]
        record(P, f"si-{key}-m", fmt(d["m"] / 1000.0))
        record(P, f"si-{key}-Vox", fmt(d["V_ox"]))
        record(P, f"si-{key}-Vfu", fmt(d["V_fu"]))
        record(P, f"si-{key}-V", d["V_s"])
    record(P, "si-mass-less-pct", fmt(100.0 * (1.0 - s["hydro"]["m"] / s["kero"]["m"]), 2))
    record(P, "si-vol-ratio", fmt(s["hydro"]["V"] / s["kero"]["V"], 4))
    assert fmt(s["hydro"]["V"] / s["kero"]["V"], 4) == fmt(float(s["hydro"]["V_s"]) / float(s["kero"]["V_s"]), 4), \
        "the ratio is also that of the two printed totals"
    record(P, "rho-lox", fmt(s["rho_lox"]))
    record(P, "rho-lh2", fmt(s["rho_lh2"]))
    record(P, "rho-rp1", fmt(s["rho_rp1"], 3))
    record(P, "lox-lh2-ratio", fmt(s["rho_lox"] / s["rho_lh2"], 3))
    # storage temperatures
    lr = {n: (Tf, Tb) for n, Tf, Tb, _ in liquid_ranges()}
    record(P, "tb-lh2-c", fmt_dec(_c(lr["liquid hydrogen"][1]), 0, minus="−"))
    record(P, "tb-lox-c", fmt_dec(_c(lr["liquid oxygen"][1]), 0, minus="−"))
    record(P, "tb-nto-c", fmt_dec(_c(lr["nitrogen tetroxide"][1]), 0, minus="−"))
    record(P, "tf-hydrazine-c", fmt(_c(lr["hydrazine"][0]), 2, minus="−"))
    record(P, "tb-ch4-c", fmt_dec(_c(NIST["methane"]["Tb"]), 0, minus="−"))
    record(P, "cryo-c", fmt_dec(_c(_K(CRYO_LIMIT_F)), 0, minus="−"))
    record(P, "room-c", fmt(_c(_K(ROOM_F)), 2))
    record(P, "avum-restarts", "5")
    record(P, "rs25-thr-lo", "65")
    record(P, "rs25-thr-hi", "109")
    # thrust-to-weight
    for d in liftoff_rows():
        k = d["name"].lower().replace(" ", "-")
        record(P, f"fw-{k}-F", fmt(d["F"] / 1e3))
        record(P, f"fw-{k}-m", fmt(d["m"] / 1000.0))
        record(P, f"fw-{k}", fmt(d["FW"], 3))
    esca = [s_ for s_ in STAGES if s_[0] == "ESC-A"][0]
    m_esca = esca[3] + esca[4]
    record(P, "esca-F", fmt(ESCA_F / 1e3, 2))
    record(P, "esca-m", fmt(m_esca))
    record(P, "esca-fw", fmt(ESCA_F / (m_esca * G0), 3))
    fws = [d["FW"] for d in liftoff_rows()]
    record(P, "fw-min", fmt(min(fws), 3))
    record(P, "fw-max", fmt(max(fws), 3))
    epc = ARIANE5_CORE
    v2 = engine_si(VULCAIN2)
    m_core = epc["dry_kg"] + epc["prop_kg"]
    record(P, "core-fw", fmt(v2["F_sl"] / (m_core * G0), 2))     # as page 4.2 prints it
    record(P, "eap-share", fmt(EAP_LIFTOFF_SHARE_PCT, 2))
    record(P, "eap-liftoff-F", fmt(EAP_LIFTOFF_F / 1e3))
    record(P, "eap-liftoff-isp", fmt(EAP_LIFTOFF_ISP, 3))
    # worked example
    ex = example()
    b = ex["burn"]
    record(P, "ex-hp", fmt(GTO_HP, 3))
    record(P, "ex-ha", fmt(GTO_HA, 5))
    record(P, "ex-inc", fmt(GTO_INC, 1))
    record(P, "ex-R", fmt(RADIUS["Earth"]))
    record(P, "ex-mu", fmt(MU["Earth"] / 1e5))
    record(P, "ex-rp", fmt(b["rp"]))
    record(P, "ex-ra", fmt(b["ra"], 5))
    record(P, "ex-a", fmt(b["a"], 5))
    br = 2.0 / b["ra"] - 1.0 / b["a"]
    record(P, "ex-bracket", fmt(br * 1e6, 5))
    record(P, "ex-va2", fmt(MU["Earth"] * br, 5))
    record(P, "ex-va", fmt(b["va"]))
    record(P, "ex-vc", fmt(b["vc"]))
    record(P, "ex-dv", fmt(b["dv"]))
    record(P, "ex-dv-ms", fmt(ex["dv"]))
    record(P, "ex-mpay", fmt(EX_M_PAY))
    record(P, "ex-z9-dry", fmt(ex["z9"][3]))
    record(P, "ex-z9-gross", fmt(ex["z9"][3] + ex["z9"][4]))
    record(P, "ex-z9-prop", fmt(ex["z9"][4]))
    record(P, "ex-fA", ex["f_solid_s"])
    record(P, "ex-ispA", fmt(ex["isp_solid"], 4))
    record(P, "ex-rhoA", fmt(ex["rho_solid"]))
    record(P, "ex-ispB", fmt(ex["isp_b"], 4))
    record(P, "ex-fB", fmt_dec(EX_F_BIPROP, 2))
    record(P, "ex-avum-ox", fmt(AVUM_NTO_KG, 3))
    record(P, "ex-avum-fu", fmt(AVUM_UDMH_KG, 3))
    record(P, "ex-avum-f", fmt(inert_mass_fraction(688.0, AVUM_NTO_KG + AVUM_UDMH_KG), 3))
    for tag, O in (("A", ex["A"]), ("B", ex["B"])):
        record(P, f"ex-c{tag}", O["c_s"])
        record(P, f"ex-x{tag}", O["x_s"])
        record(P, f"ex-e{tag}", O["e_s"])
        record(P, f"ex-num{tag}", O["num_s"])
        record(P, f"ex-den{tag}", O["den_s"])
        record(P, f"ex-mp{tag}", O["mp_s"])
        record(P, f"ex-mi{tag}", O["mi_inert_s"])
        record(P, f"ex-m0{tag}", O["m_i_s"])
        record(P, f"ex-V{tag}", fmt(O["V"]))
    B = ex["B"]
    record(P, "ex-rB", B["r_s"])
    record(P, "ex-mox", B["m_ox_s"])
    record(P, "ex-mfu", B["m_fu_s"])
    record(P, "ex-rho-nto", fmt(B["rho_ox"]))
    record(P, "ex-rho-udmh", fmt(B["rho_fu"], 3))
    record(P, "ex-Vox", B["V_ox_s"])
    record(P, "ex-Vfu", B["V_fu_s"])
    record(P, "ex-rho-bulkB", fmt(B["rho_bulk"]))
    A = ex["A"]
    record(P, "ex-dm", fmt(B["m_i"] - A["m_i"], 3))
    record(P, "ex-dm-pct", fmt(100.0 * (B["m_i"] - A["m_i"]) / A["m_i"], 2))
    VA_p, VB_p = float(fmt(A["V"])), float(fmt(B["V"]))
    record(P, "ex-dV", fmt(VB_p - VA_p, 3))
    record(P, "ex-dV-pct", fmt(100.0 * (VB_p - VA_p) / VA_p, 2))
    mfA = EX_M_PAY + A["mi_inert"]
    record(P, "ex-mfA", fmt(mfA))
    close_to(A["c"] * math.log(A["m_i"] / mfA), ex["dv"], 2.0, "option A back in the rocket equation")
