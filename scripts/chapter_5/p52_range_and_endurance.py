"""Figures and values of 5.2 Range and Endurance (notes/chapter-5/range-and-endurance.md).

Worked examples (verified not in the problem bank or homework):
  - Example 1 (published, Anderson Example 6.19 / Lecture 22): CJ-1 business jet at 22,000 ft,
    English units: b = 53.3 ft, S = 318 ft^2, W_1 = 19,817 lb, fuel 7,452.5 lb (1,119 gal at
    6.66 lb/gal), TSFC = 0.60 lbf/(lbf h), C_D,0 = 0.020, e = 0.81, rho = 0.038 lbm/ft^3.
  - Example 2 (SI jet, reverse fuel for range): Executive jet (from page 5.1) at 9,500 m,
    m_1 = 33,100 kg, S = 88.2 m^2, C_D,0 = 0.015, K = 0.050, TSFC = 0.58 1/h, R_req = 4,000 km.
  - Example 3 (SI propeller aircraft): GA aircraft (from page 5.1) at 2,500 m,
    m_1 = 1,315 kg, m_fuel = 168 kg, S = 16.3 m^2, C_D,0 = 0.026, K = 0.054, eta = 0.80,
    PSFC = 0.076 g/(s kW).
"""
from chapter_5.common import *

PAGE = "p52"

# ===================================================================== aircraft data
CJ1 = dict(b=53.3, S=318.0, W1=19817.0, gal=1119.0, lb_per_gal=6.66,
           CD0=0.020, e=0.81, tsfc_h=0.60, rho_lbm=0.038, g_en=32.17, h_ft=22000.0)
JET = dict(m1=33100.0, S=88.2, CD0=0.015, K=0.050, tsfc_h=0.58, h=9500.0, R_req=4000e3)
GA = dict(m1=1315.0, mf=168.0, S=16.3, CD0=0.026, K=0.054, eta=0.80, psfc_g_skW=0.076,
          h=2500.0, R_leg=1000e3)


def _num(s):
    return float(s.replace(",", "").replace("−", "-"))


# ===================================================================== figures
def fig_aero_ratios():
    """The three aerodynamic ratios normalized by their peaks against C_L for the executive jet
    polar (C_D,0 = 0.015, K = 0.050), showing the exact peak order: sqrt(C_D0/3K) < sqrt(C_D0/K)
    < sqrt(3 C_D0/K), a factor of sqrt(3) between neighbors."""
    CD0, K = JET["CD0"], JET["K"]
    CL = np.linspace(0.05, 1.45, 500)
    CD = polar_CD(CL, CD0, K)
    r_half = np.sqrt(CL) / CD
    r_one = CL / CD
    r_three = (CL ** 1.5) / CD

    cl_r = math.sqrt(CD0 / (3.0 * K))
    cl_m = math.sqrt(CD0 / K)
    cl_p = math.sqrt(3.0 * CD0 / K)

    fig, ax = data_axes(6.5, 4.0)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.14, top=0.95)
    ax.plot(CL, r_half / np.max(r_half), **line_kw(1), zorder=4)
    ax.plot(CL, r_one / np.max(r_one), **line_kw(0), zorder=5)
    ax.plot(CL, r_three / np.max(r_three), **line_kw(2), zorder=4)

    for cl_pk, st, mk in ((cl_r, 1, "s"), (cl_m, 0, "o"), (cl_p, 2, "D")):
        ax.plot([cl_pk, cl_pk], [0.0, 1.0], **line_kw("boundary"), zorder=2)
        ax.plot([cl_pk], [1.0], mk, ms=6.5, color=text_color(st), zorder=6)

    ax.set_xlim(0.0, 1.48); ax.set_ylim(0.0, 1.42)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel("Lift coefficient, $C_L$")
    ax.set_ylabel("Ratio divided by its maximum")

    text(ax, (cl_r - 0.06, 1.03), "$C_L^{1/2}/C_D$\njet range", direction=90, dist=8, fs=FS_LABEL,
         color=text_color(1), ha="center")
    text(ax, (cl_m + 0.03, 1.03), "$C_L/C_D$\njet end. &\nprop range", direction=90, dist=8, fs=FS_LABEL,
         color=INK, ha="center")
    text(ax, (cl_p + 0.06, 1.03), "$C_L^{3/2}/C_D$\nprop endurance", direction=90, dist=8, fs=FS_LABEL,
         color=text_color(2), ha="center")

    text(ax, (cl_r, 0.10), fmt(cl_r, 3), direction=0, dist=4, fs=FS_SMALL, color=text_color(1))
    text(ax, (cl_m, 0.10), fmt(cl_m, 3), direction=0, dist=4, fs=FS_SMALL, color=INK)
    text(ax, (cl_p, 0.10), fmt(cl_p, 3), direction=0, dist=4, fs=FS_SMALL, color=text_color(2))

    close_to(float(CL[np.argmax(r_half)]), cl_r, 0.01, "C_L^(1/2)/C_D peak")
    close_to(float(CL[np.argmax(r_one)]), cl_m, 0.01, "C_L/C_D peak")
    close_to(float(CL[np.argmax(r_three)]), cl_p, 0.01, "C_L^(3/2)/C_D peak")
    save_figure(fig, "p52-aero-ratios")


def fig_jet_vs_prop_curves():
    """Side-by-side geometric reading of maximum endurance and maximum range (after Anderson
    Figures 6.42 and 6.45): left, jet T_R vs V (minimum = max endurance, tangent from origin =
    max range); right, propeller P_R vs V (minimum = max endurance, tangent from origin = max range)."""
    fig, axs = data_axes(6.5, 3.8, ncols=2)
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.15, top=0.90, wspace=0.35)

    # Panel 1: Executive jet at 9,500 m
    ax = axs[0]
    rho_j = standard(JET["h"])[2]
    mt_j = min_thrust_condition(JET["m1"], JET["S"], JET["CD0"], JET["K"], rho_j)
    jr = jet_best_range_polar(JET["CD0"], JET["K"])
    V_re = math.sqrt(2.0 * JET["m1"] * G0 / (rho_j * JET["S"] * jr["CL"]))
    T_re = float(thrust_required(JET["m1"], JET["S"], JET["CD0"], JET["K"], rho_j, V_re)) / 1000.0
    V_ee = mt_j["V"]
    T_ee = mt_j["T_min"] / 1000.0

    Vj = np.linspace(115.0, 310.0, 400)
    TRj = thrust_required(JET["m1"], JET["S"], JET["CD0"], JET["K"], rho_j, Vj) / 1000.0
    ax.plot(Vj, TRj, **line_kw(0), zorder=4)
    # Tangent from origin to T_R(V) touches at V_re (minimizes T_R / V ~ C_D / sqrt(C_L))
    V_tan = np.array([0.0, 305.0])
    ax.plot(V_tan, (T_re / V_re) * V_tan, color=BLUE, lw=1.2, ls=(0, (5, 2.5)), zorder=3)
    ax.plot([V_ee], [T_ee], "o", ms=6.5, color=INK, zorder=6)
    ax.plot([V_re], [T_re], "s", ms=6.0, mfc="white", mec=BLUE, mew=1.5, zorder=6)
    ax.set_xlim(0, 320); ax.set_ylim(0, 38)
    ax.set_xticks([0, 100, 200, 300]); ax.set_yticks([0, 10, 20, 30])
    ax.set_title("1  jet: thrust required", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Thrust required, $T_R$, kN")
    callout(ax, (V_ee, T_ee), "max endurance\n(min $T_R$)", at=(12, 29.0), ha="left", fs=FS_SMALL)
    callout(ax, (V_re, T_re), "max range\n(tangent)", at=(132, 6.5), ha="left", fs=FS_SMALL, color=BLUE)
    # Check tangency numerically: slope of T_R at V_re equals T_re / V_re
    dT = float(thrust_required(JET["m1"], JET["S"], JET["CD0"], JET["K"], rho_j, V_re + 0.01) -
               thrust_required(JET["m1"], JET["S"], JET["CD0"], JET["K"], rho_j, V_re - 0.01)) / 20.0
    close_to(dT, T_re / V_re, 1e-3, "origin line tangent to jet T_R at best range")

    # Panel 2: GA propeller at 2,500 m
    ax = axs[1]
    rho_g = standard(GA["h"])[2]
    mp_g = min_power_condition(GA["m1"], GA["S"], GA["CD0"], GA["K"], rho_g)
    mt_g = min_thrust_condition(GA["m1"], GA["S"], GA["CD0"], GA["K"], rho_g)
    V_ep, P_ep = mp_g["V"], mp_g["P_min"] / 1000.0
    V_rp, P_rp = mt_g["V"], mt_g["P_at_Tmin"] / 1000.0
    Vg = np.linspace(27.0, 82.0, 400)
    PRg = power_required(GA["m1"], GA["S"], GA["CD0"], GA["K"], rho_g, Vg) / 1000.0
    ax.plot(Vg, PRg, **line_kw(0), zorder=4)
    V_tan2 = np.array([0.0, 78.0])
    ax.plot(V_tan2, (P_rp / V_rp) * V_tan2, color=BLUE, lw=1.2, ls=(0, (5, 2.5)), zorder=3)
    ax.plot([V_ep], [P_ep], "o", ms=6.5, color=INK, zorder=6)
    ax.plot([V_rp], [P_rp], "s", ms=6.0, mfc="white", mec=BLUE, mew=1.5, zorder=6)
    ax.set_xlim(0, 85); ax.set_ylim(0, 120)
    ax.set_xticks([0, 20, 40, 60, 80]); ax.set_yticks([0, 30, 60, 90, 120])
    ax.set_title("2  propeller: power required", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("True airspeed, $V$, m/s"); ax.set_ylabel("Power required, $P_R$, kW")
    callout(ax, (V_ep, P_ep), "max endurance\n(min $P_R$)", at=(6, 92.0), ha="left", fs=FS_SMALL)
    callout(ax, (V_rp, P_rp), "max range\n(tangent)", at=(40, 18.0), ha="left", fs=FS_SMALL, color=BLUE)
    close_to(P_rp / V_rp, mt_g["T_min"] / 1000.0, 1e-6, "origin line tangent to prop P_R at best range")
    save_figure(fig, "p52-jet-vs-prop-curves")


def fig_speed_order():
    """The three key flight speeds on a single scale (divided by V_TR,min): 3^(-1/4) = 0.760,
    1.000, and 3^(1/4) = 1.316, showing which condition each maximizes for prop vs. jet."""
    fig, ax = canvas(6.5, xlim=(0.48, 1.56), ylim=(-0.22, 0.30))
    r_lo = 3.0 ** (-0.25)
    r_mid = 1.0
    r_hi = 3.0 ** 0.25

    # Horizontal speed axis
    kind_arrow(ax, (0.54, 0.0), (1.52, 0.0), "axis", None)
    text(ax, (1.52, 0.0), "$V / V_{T_R,\\min}$", direction=-90, dist=7, fs=FS_LABEL, ha="right")

    pts = [
        (r_lo, "0.760", "s", 2),
        (r_mid, "1.000", "o", 0),
        (r_hi, "1.316", "D", 1),
    ]
    for x, num_s, mk, st in pts:
        ax.plot([x], [0.0], mk, ms=7.5, color=text_color(st), zorder=6)
        text(ax, (x, 0.0), num_s, direction=-90, dist=10, fs=FS_LABEL, color=text_color(st))
    callout(ax, (r_lo, 0.015), "prop max endurance\n($P_{R,\\min}$)", at=(0.54, 0.17), ha="left", fs=FS_LABEL,
            color=text_color(2))
    callout(ax, (r_mid, 0.015), "prop max range\n& jet max endurance\n($T_{R,\\min}$, $(L/D)_\\max$)",
            at=(1.00, 0.17), ha="center", fs=FS_LABEL, color=INK)
    callout(ax, (r_hi, 0.015), "jet max range\n($C_L^{1/2}/C_D$ max)", at=(1.52, 0.17), ha="right", fs=FS_LABEL,
            color=text_color(1))

    # Ratio dimensions underneath
    dimension(ax, (r_lo, -0.14), (r_mid, -0.14), None, ticks=True, extension=False)
    text(ax, (0.5 * (r_lo + r_mid), -0.14), "$\\times 3^{1/4}$", direction=-90, dist=6, fs=FS_SMALL)
    dimension(ax, (r_mid, -0.14), (r_hi, -0.14), None, ticks=True, extension=False)
    text(ax, (0.5 * (r_mid + r_hi), -0.14), "$\\times 3^{1/4}$", direction=-90, dist=6, fs=FS_SMALL)

    close_to(r_hi / r_mid, 3.0 ** 0.25, 1e-12, "upper ratio is 3^(1/4)")
    close_to(r_mid / r_lo, 3.0 ** 0.25, 1e-12, "lower ratio is 3^(1/4)")
    trim_canvas(fig)
    save_figure(fig, "p52-speed-order")


def fig_weight_burn():
    """Executive jet cruising 4,000 km at 9,500 m at constant C_L for best range:
    true airspeed V and thrust required T_R both fall as fuel burns."""
    rho = standard(JET["h"])[2]
    ct = 1.611e-4
    jr = jet_best_range_polar(JET["CD0"], JET["K"])
    mf, m2 = jet_fuel_for_range(JET["m1"], JET["R_req"], JET["S"], rho, ct, jr["CL"], jr["CD"])
    ms = np.linspace(JET["m1"], m2, 300)
    xs_km = np.array([jet_range(JET["m1"], mm, JET["S"], rho, ct, jr["CL"], jr["CD"]) / 1000.0 for mm in ms])
    Vs = np.sqrt(2.0 * ms * G0 / (rho * JET["S"] * jr["CL"]))
    Ts = ms * G0 / jr["LD"] / 1000.0

    fig, axs = data_axes(6.5, 3.6, ncols=2)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.16, top=0.90, wspace=0.35)

    ax = axs[0]
    ax.plot(xs_km, Vs, **line_kw(0), zorder=4)
    ax.plot([0.0, xs_km[-1]], [Vs[0], Vs[-1]], "o", ms=5.5, color=INK, zorder=6)
    ax.set_xlim(0, 4200); ax.set_ylim(200, 260)
    ax.set_xticks([0, 1000, 2000, 3000, 4000]); ax.set_yticks([200, 220, 240, 260])
    ax.set_title("1  airspeed slows as mass drops", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("Distance flown, km"); ax.set_ylabel("True airspeed, $V$, m/s")
    text(ax, (120, Vs[0]), f"{fmt(Vs[0], 4)} m/s", direction=90, dist=6, fs=FS_SMALL, ha="left")
    text(ax, (xs_km[-1] - 120, Vs[-1]), f"{fmt(Vs[-1], 4)} m/s", direction=-90, dist=7, fs=FS_SMALL, ha="right")

    ax = axs[1]
    ax.plot(xs_km, Ts, **line_kw(1), zorder=4)
    ax.plot([0.0, xs_km[-1]], [Ts[0], Ts[-1]], "s", ms=5.5, color=BLUE, zorder=6)
    ax.set_xlim(0, 4200); ax.set_ylim(14, 24)
    ax.set_xticks([0, 1000, 2000, 3000, 4000]); ax.set_yticks([14, 16, 18, 20, 22, 24])
    ax.set_title("2  thrust required drops with weight", fontsize=FS_SMALL, loc="left")
    ax.set_xlabel("Distance flown, km"); ax.set_ylabel("Thrust required, $T_R$, kN")
    text(ax, (120, Ts[0]), f"{fmt(Ts[0], 4)} kN", direction=90, dist=6, fs=FS_SMALL, color=BLUE, ha="left")
    text(ax, (xs_km[-1] - 120, Ts[-1]), "17.07 kN", direction=-90, dist=7, fs=FS_SMALL,
         color=BLUE, ha="right")

    assert Vs[-1] < Vs[0] and Ts[-1] < Ts[0]
    close_to(float(xs_km[-1]), JET["R_req"] / 1000.0, 1e-6, "curve reaches 4,000 km")
    save_figure(fig, "p52-weight-burn")


def fig_altitude_range():
    """Jet range vs. cruise altitude for the executive jet carrying the fuel of Example 2
    (5,597 kg), showing R proportional to 1/sqrt(rho), compared with the GA propeller aircraft
    whose Breguet range stays flat with altitude."""
    rho95 = standard(JET["h"])[2]
    ct = 1.611e-4
    jr = jet_best_range_polar(JET["CD0"], JET["K"])
    mf, m2 = jet_fuel_for_range(JET["m1"], JET["R_req"], JET["S"], rho95, ct, jr["CL"], jr["CD"])

    hs = np.linspace(0.0, 12000.0, 121)
    R_jet = np.array([jet_range(JET["m1"], m2, JET["S"], standard(h)[2], ct, jr["CL"], jr["CD"]) / 1000.0
                      for h in hs])
    c_ga = 7.456e-7
    mt_ga = min_thrust_condition(GA["m1"], GA["S"], GA["CD0"], GA["K"], RHO_SL)
    R_ga_km = prop_range(GA["m1"], GA["m1"] - GA["mf"], GA["eta"], c_ga, mt_ga["CL"], mt_ga["CD"]) / 1000.0

    fig, ax = data_axes(6.5, 3.8)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.15, top=0.96)
    ax.plot(hs / 1000.0, R_jet, **line_kw(0), zorder=4)
    ax.plot([0.0, 7.0], [R_ga_km, R_ga_km], **line_kw(1), zorder=4)
    ax.plot([JET["h"] / 1000.0], [4000.0], "o", ms=6.5, color=INK, zorder=6)
    ax.plot([GA["h"] / 1000.0], [R_ga_km], "s", ms=6.0, mfc="white", mec=BLUE, mew=1.4, zorder=6)

    ax.set_xlim(0, 12.5); ax.set_ylim(0, 5200)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12]); ax.set_yticks([0, 1000, 2000, 3000, 4000, 5000])
    ax.set_xlabel("Cruise altitude, $h$, km")
    ax.set_ylabel("Maximum range, $R$, km")

    callout(ax, (JET["h"] / 1000.0, 4000.0), "Example 2 jet:\n4,000 km at 9.5 km",
            at=(4.8, 4350.0), ha="left", fs=FS_SMALL)
    text(ax, (7.0, R_ga_km), "Example 3 propeller:\n1,956 km (flat with $h$)",
         direction=0, dist=8, fs=FS_SMALL, color=BLUE)
    text(ax, (0.8, 3300.0), "jet: grows as $1/\\rho^{1/2}$", fs=FS_LABEL, color=INK, ha="left")

    assert R_jet[-1] > 1.7 * R_jet[0], "jet range grows strongly with altitude"
    save_figure(fig, "p52-altitude-range")


def make_all():
    fig_aero_ratios()
    fig_jet_vs_prop_curves()
    fig_speed_order()
    fig_weight_burn()
    fig_altitude_range()


# ===================================================================== printed values
def values():
    r = lambda k, v: record(PAGE, k, v)  # noqa: E731
    # Example 1: CJ-1 business jet (Anderson Example 6.19, English units)
    r("cj-h-ft", fmt(CJ1["h_ft"], 5)); r("cj-rho", fmt_dec(CJ1["rho_lbm"], 3))
    r("cj-b", fmt_dec(CJ1["b"], 1)); r("cj-S", fmt(CJ1["S"], 3))
    r("cj-W1", fmt(CJ1["W1"], 5)); r("cj-gal", fmt(CJ1["gal"], 4)); r("cj-lbgal", fmt_dec(CJ1["lb_per_gal"], 2))
    r("cj-CD0", fmt_dec(CJ1["CD0"], 3)); r("cj-e", fmt_dec(CJ1["e"], 2)); r("cj-tsfc", fmt_dec(CJ1["tsfc_h"], 2))
    Wf = r("cj-Wf", fmt(CJ1["gal"] * CJ1["lb_per_gal"], 5))
    W2 = r("cj-W2", fmt(CJ1["W1"] - _num(Wf), 5))
    AR = r("cj-AR", fmt(CJ1["b"] ** 2 / CJ1["S"], 4))
    K_cj = r("cj-K", fmt(1.0 / (math.pi * CJ1["e"] * _num(AR)), 5))
    CL_cj = r("cj-CL", fmt(math.sqrt(CJ1["CD0"] / (3.0 * _num(K_cj))), 4))
    CD_cj = r("cj-CD", fmt((4.0 / 3.0) * CJ1["CD0"], 5))
    ct_cj = r("cj-ct", fmt_sci(CJ1["tsfc_h"] / 3600.0, 4))
    # Exact 2 / (0.60 / 3600) = 12,000 s (avoids rounding drift from 1.667e-4)
    fac1 = r("cj-fac1", fmt(2.0 / (CJ1["tsfc_h"] / 3600.0), 5))
    fac2 = r("cj-fac2", fmt(math.sqrt(2.0 * CJ1["g_en"] / (CJ1["rho_lbm"] * CJ1["S"])), 4))
    fac3 = r("cj-fac3", fmt(math.sqrt(_num(CL_cj)) / _num(CD_cj), 4))
    sm1 = r("cj-sm1", fmt(math.sqrt(CJ1["W1"]), 5))
    sm2 = r("cj-sm2", fmt(math.sqrt(_num(W2)), 5))
    dsm = r("cj-dsm", fmt(_num(sm1) - _num(sm2), 4))
    R_ft = r("cj-R-ft", fmt(_num(fac1) * _num(fac2) * _num(fac3) * _num(dsm), 5))
    R_mi = r("cj-R-mi", fmt(_num(R_ft) / FT_PER_MI, 4))
    r("cj-R-km", fmt(_num(R_mi) * 1.60934, 4))

    # Example 2: Executive jet SI at 9,500 m (reverse fuel for 4,000 km + endurance on same fuel)
    rho_j = standard(JET["h"])[2]
    a_j = float(speed_of_sound(standard(JET["h"])[0]))
    r("jet-m1", fmt(JET["m1"], 5)); r("jet-S", fmt_dec(JET["S"], 1))
    r("jet-CD0", fmt_dec(JET["CD0"], 3)); r("jet-K", fmt_dec(JET["K"], 3))
    r("jet-h", fmt(JET["h"], 4)); rho_js = r("jet-rho", fmt(rho_j, 5))
    r("jet-tsfc", fmt_dec(JET["tsfc_h"], 2)); r("jet-Rreq-km", fmt(JET["R_req"] / 1000.0, 4))
    ct_j = JET["tsfc_h"] / 3600.0
    r("jet-ct", fmt_sci(ct_j, 4))
    ct_jp = 1.611e-4
    CLr = r("jet-CLr", fmt(math.sqrt(JET["CD0"] / (3.0 * JET["K"])), 4))
    CDr = r("jet-CDr", fmt_dec((4.0 / 3.0) * JET["CD0"], 4))
    rat_j = r("jet-rat", fmt(math.sqrt(_num(CLr)) / _num(CDr), 4))
    Aj_sq = r("jet-sq", fmt(math.sqrt(2.0 * G0 / (_num(rho_js) * JET["S"])), 4))
    Aj = r("jet-A", fmt((2.0 / ct_jp) * _num(Aj_sq) * _num(rat_j), 5))
    sm1_j = r("jet-sm1", fmt(math.sqrt(JET["m1"]), 5))
    sm2_j = r("jet-sm2", fmt(_num(sm1_j) - JET["R_req"] / _num(Aj), 5))
    m2_j = r("jet-m2", fmt(_num(sm2_j) ** 2, 5))
    mf_j = r("jet-mf", fmt(JET["m1"] - _num(m2_j), 4))
    Vr1 = r("jet-Vr1", fmt(math.sqrt(2.0 * JET["m1"] * G0 / (_num(rho_js) * JET["S"] * _num(CLr))), 4))
    Vr2 = r("jet-Vr2", fmt(math.sqrt(2.0 * _num(m2_j) * G0 / (_num(rho_js) * JET["S"] * _num(CLr))), 4))
    r("jet-Mr1", fmt(_num(Vr1) / a_j, 3))
    # Thrust at start and end of cruise
    LD_r = _num(CLr) / _num(CDr)
    r("jet-Tr1-kN", fmt(JET["m1"] * G0 / LD_r / 1000.0, 4))
    r("jet-Tr2-kN", fmt(_num(m2_j) * G0 / LD_r / 1000.0, 4))
    # Max endurance on same fuel
    CLe = r("jet-CLe", fmt(math.sqrt(JET["CD0"] / JET["K"]), 4))
    CDe = r("jet-CDe", fmt_dec(2.0 * JET["CD0"], 3))
    LDe = r("jet-LDe", fmt(_num(CLe) / _num(CDe), 4))
    ln_j = r("jet-ln", fmt(math.log(JET["m1"] / _num(m2_j)), 5))
    E_js = r("jet-E-s", fmt((1.0 / ct_jp) * _num(LDe) * _num(ln_j), 5))
    r("jet-E-h", fmt(_num(E_js) / 3600.0, 3))

    # Example 3: GA propeller aircraft at 2,500 m
    rho_g = standard(GA["h"])[2]
    r("ga-m1", fmt(GA["m1"], 4)); r("ga-mf", fmt(GA["mf"], 3))
    m2_g = r("ga-m2", fmt(GA["m1"] - GA["mf"], 4))
    r("ga-S", fmt_dec(GA["S"], 1)); r("ga-CD0", fmt_dec(GA["CD0"], 3)); r("ga-K", fmt_dec(GA["K"], 3))
    r("ga-eta", fmt_dec(GA["eta"], 2)); r("ga-psfc", fmt_dec(GA["psfc_g_skW"], 3))
    r("ga-h", fmt(GA["h"], 4)); rho_gs = r("ga-rho", fmt(rho_g, 4))
    c_ga = GA["psfc_g_skW"] * 1e-6 * G0
    r("ga-c", fmt_sci(c_ga, 4))
    c_gap = 7.456e-7
    etac = r("ga-etac", fmt(GA["eta"] / c_gap, 5))
    CLr_g = r("ga-CLr", fmt(math.sqrt(GA["CD0"] / GA["K"]), 4))
    CDr_g = r("ga-CDr", fmt_dec(2.0 * GA["CD0"], 3))
    LDr_g = r("ga-LDr", fmt(_num(CLr_g) / _num(CDr_g), 4))
    ln_g = r("ga-ln", fmt(math.log(GA["m1"] / _num(m2_g)), 5))
    R_gm = r("ga-R-m", fmt(_num(etac) * _num(LDr_g) * _num(ln_g), 5))
    r("ga-R-km", fmt(_num(R_gm) / 1000.0, 4))
    # Max endurance
    CLe_g = r("ga-CLe", fmt(math.sqrt(3.0 * GA["CD0"] / GA["K"]), 4))
    CDe_g = r("ga-CDe", fmt_dec(4.0 * GA["CD0"], 3))
    rat_eg = r("ga-rat-e", fmt(_num(CLe_g) ** 1.5 / _num(CDe_g), 4))
    sq_eg = r("ga-sq-e", fmt(math.sqrt(2.0 * _num(rho_gs) * GA["S"] / G0), 4))
    inv2 = r("ga-inv2", fmt(1.0 / math.sqrt(_num(m2_g)), 5))
    inv1 = r("ga-inv1", fmt(1.0 / math.sqrt(GA["m1"]), 5))
    dinv = r("ga-dinv", fmt(_num(inv2) - _num(inv1), 4))
    E_gs = r("ga-E-s", fmt(_num(etac) * _num(sq_eg) * _num(rat_eg) * _num(dinv), 5))
    r("ga-E-h", fmt(_num(E_gs) / 3600.0, 4))
    # Reverse: fuel for 1,000 km leg
    r("ga-Rleg-km", fmt(GA["R_leg"] / 1000.0, 4))
    ex_arg = r("ga-exarg", fmt(GA["R_leg"] * c_gap / (GA["eta"] * _num(LDr_g)), 5))
    m2_leg = r("ga-m2-leg", fmt(GA["m1"] * math.exp(-_num(ex_arg)), 5))
    r("ga-mf-leg", fmt(GA["m1"] - _num(m2_leg), 4))
    # Ratios in speed-order figure
    r("ratio-lo", fmt(3.0 ** (-0.25), 3)); r("ratio-hi", fmt(3.0 ** 0.25, 4))
