#!/usr/bin/env python3
"""Unit checks of Chapter 5's shared code: perf.py (the physics), vehicles.py (the aircraft) and
looks.py (the figure look). Run from the book folder:

    python3 -B scripts/chapter_5/selftest.py

The test aircraft of section 1 is invented for these checks (14,200 kg, 41.5 m^2, polar
0.019 + 0.052 C_L^2) and is printed on no page. Section 4 checks that the aircraft data of
vehicles.py reproduce the published numbers of their examples.
"""
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import numpy as np  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from chapter_1.atmosphere import standard, speed_of_sound, G0, RHO_SL  # noqa: E402
from chapter_5.perf import *  # noqa: F401,F403,E402
from chapter_5 import vehicles as VH  # noqa: E402
from chapter_5 import looks as LK  # noqa: E402
from figkit import contrast_ratio  # noqa: E402

N_CHECKS = 0


def close(a, b, rtol, what):
    """Relative closeness; absolute (tolerance rtol) when b is zero."""
    global N_CHECKS
    N_CHECKS += 1
    assert abs(a - b) <= (rtol * abs(b) if b != 0 else rtol), f"{what}: {a!r} vs {b!r}"


def check(cond, what):
    global N_CHECKS
    N_CHECKS += 1
    assert cond, what


# ===================================================================== 1. level flight, range, climb, ceilings
m, S, CD0, K, rho = 14200.0, 41.5, 0.019, 0.052, 0.95
V = np.linspace(40.0, 320.0, 200001)
T0, Ti, TR = thrust_required_parts(m, S, CD0, K, rho, V)
P0_, Pi_, PR = power_required_parts(m, S, CD0, K, rho, V)
mt = min_thrust_condition(m, S, CD0, K, rho)
mp = min_power_condition(m, S, CD0, K, rho)
close(float(V[np.argmin(TR)]), mt["V"], 1e-4, "V_TR,min matches grid")
close(float(np.min(TR)), mt["T_min"], 1e-7, "T_R,min matches grid")
close(float(V[np.argmin(PR)]), mp["V"], 1e-4, "V_PR,min matches grid")
close(float(np.min(PR)), mp["P_min"], 1e-7, "P_R,min matches grid")
close(mp["V"] / mt["V"], 3.0 ** (-0.25), 1e-12, "V_PR,min / V_TR,min = 3^(-1/4)")
T0p, Tip, _ = thrust_required_parts(m, S, CD0, K, rho, mp["V"])
close(float(Tip), 3.0 * float(T0p), 1e-10, "at V_PR,min, induced drag is three times parasite drag")
jr = jet_best_range_polar(CD0, K)
close(K * jr["CL"] ** 2, CD0 / 3.0, 1e-12, "at jet best range, parasite drag is three times induced drag")
vlo, vhi = jet_speed_bounds(m, S, CD0, K, rho, 2.3 * mt["T_min"])
close(float(thrust_required(m, S, CD0, K, rho, vhi)), 2.3 * mt["T_min"], 1e-10, "jet V_max exact")
close(float(thrust_required(m, S, CD0, K, rho, vlo)), 2.3 * mt["T_min"], 1e-10, "jet low crossing exact")
vpmax, _ = prop_vmax(m, S, CD0, K, rho, 2.7 * mp["P_min"])
close(float(power_required(m, S, CD0, K, rho, vpmax)), 2.7 * mp["P_min"], 1e-9, "prop V_max exact")
ct, eta, c = 1.9e-4, 0.78, 6.5e-7
R_test = jet_range(m, 0.81 * m, S, rho, ct, jr["CL"], jr["CD"])
close(jet_fuel_for_range(m, R_test, S, rho, ct, jr["CL"], jr["CD"])[0], 0.19 * m, 1e-10, "jet range fuel round trip")
Rp = prop_range(m, 0.86 * m, eta, c, mt["CL"], mt["CD"])
close(prop_fuel_for_range(m, Rp, eta, c, mt["CL"], mt["CD"])[0], 0.14 * m, 1e-10, "prop range fuel round trip")
Ep = prop_endurance(m, 0.86 * m, S, rho, eta, c, mp["CL"], mp["CD"])
close(prop_fuel_for_endurance(m, Ep, S, rho, eta, c, mp["CL"], mp["CD"])[0], 0.14 * m, 1e-10,
      "prop endurance fuel round trip")
TA_c = 2.1 * mt["T_min"]
rc_an = jet_max_roc(m, S, CD0, K, rho, TA_c)
close(rc_an["RC_max"], float(np.max(climb_jet(m, S, CD0, K, rho, TA_c, V)["RC"])), 1e-6, "jet max R/C against grid")
jc = jet_absolute_ceiling(m, CD0, K, 2, 1.15 * mt["T_min"], 0.7)
h_bis = ceiling_by_bisection(lambda h: jet_max_roc(m, S, CD0, K, standard(h)[2],
                             thrust_available(2, 1.15 * mt["T_min"], standard(h)[2], 0.7))["RC_max"], target=0.0)
close(jc["h_abs"], h_bis, 1e-4, "jet closed-form ceiling matches bisection")
pc = prop_absolute_ceiling(m, S, CD0, K, 2, 1.7 * mp["P_min"], eta, 0.85)
hp_bis = ceiling_by_bisection(lambda h: prop_max_roc(m, S, CD0, K, standard(h)[2],
                              power_available(2, 1.7 * mp["P_min"], eta, standard(h)[2], 0.85))["RC_max"], target=0.0)
close(pc["h_abs"], hp_bis, 1e-4, "prop closed-form ceiling matches bisection")
close(float(propulsive_efficiency(230.0, 230.0)), 1.0, 1e-12, "eta_p = 1 when V_e = V_inf")
close(float(propulsive_efficiency(230.0, 690.0)), 0.5, 1e-12, "eta_p = 0.5 when V_e = 3 V_inf")

# ===================================================================== 2. the shared functions added for several pages
CL0, CLa = 0.21, 0.085                      # lift curve of the test aircraft (per degree)
sp = level_flight_at_speed(m, S, CD0, K, rho, 150.0, CL0, CLa)
close(float(sp["T_R"]), float(thrust_required(m, S, CD0, K, rho, 150.0)), 1e-12, "speed given: T_R = drag")
close(float(sp["L"]), m * G0, 1e-12, "speed given: L = m g")
back = level_flight_at_alpha(m, S, CD0, K, rho, float(sp["alpha"]), CL0, CLa)
close(float(back["V"]), 150.0, 1e-12, "angle given: the speed comes back")
close(float(back["T_R"]), float(sp["T_R"]), 1e-12, "angle given: the thrust comes back")
a = np.linspace(-1.0, 16.0, 170001)
ta = thrust_required_vs_alpha(m, CD0, K, CL0, CLa, a)
close(float(np.min(ta["T_R"])), mt["T_min"], 1e-9, "least T_R against alpha is T_R,min")
close(float(ta["CL"][np.argmin(ta["T_R"])]), math.sqrt(CD0 / K), 1e-4, "least T_R at C_L of (L/D)max")
check(float(ta["alpha"][0]) > -CL0 / CLa, "only angles with positive lift are returned")
CM0, CMa, CMde = 0.05, -0.028, -0.022
de = float(trim_elevator(3.0, CM0, CMa, CMde))
close(CM0 + CMa * 3.0 + CMde * de, 0.0, 1e-12, "trim: the pitching moment is zero")
CLmax = 1.55
rj = level_speed_range(m, S, CD0, K, rho, CLmax, 2.3 * mt["T_min"], "jet")
close(rj["V_max"], vhi, 1e-12, "jet speed range: top end")
check(rj["V_min"] == max(rj["V_stall"], rj["V_low"]), "jet speed range: low end is the higher of the two")
rp = level_speed_range(m, S, CD0, K, rho, CLmax, 2.7 * mp["P_min"], "prop")
close(float(power_required(m, S, CD0, K, rho, rp["V_low"])), 2.7 * mp["P_min"], 1e-9, "prop speed range: low crossing")
close(rp["V_max"], vpmax, 1e-12, "prop speed range: top end")
rn = level_speed_range(m, S, CD0, K, rho, CLmax, 0.9 * mt["T_min"], "jet")
check(rn["V_max"] is None and rn["V_min"] is None, "no level flight when T_A < T_R,min")
c0 = climb_required(m, S, CD0, K, rho, V, 0.0)
close(float(np.max(np.abs(c0["T_R"] - TR))), 0.0, 1e-9, "climb at zero angle is level flight")
c6 = climb_required(m, S, CD0, K, rho, 140.0, 6.0)
W = m * G0
close(float(c6["weight_part"]), W * math.sin(math.radians(6.0)), 1e-12, "the weight part is m g sin(gamma)")
close(float(c6["induced"]), 2.0 * K * (W * math.cos(math.radians(6.0))) ** 2 / (rho * S * 140.0 ** 2), 1e-12,
      "induced drag in a climb uses L = m g cos(gamma)")
close(float(c6["P_R"]), float(c6["T_R"]) * 140.0, 1e-12, "P_R = T_R V in a climb")
cs = climb_required(m, S, CD0, K, rho, 140.0, 6.0, small_angle=True)
close(float(cs["T_R"] - thrust_required(m, S, CD0, K, rho, 140.0)), W * math.radians(6.0), 1e-12,
      "small angles: the level curve raised by m g gamma")
Vd = np.linspace(55.0, 320.0, 106001)
hj = climb_hodograph(m, S, CD0, K, rho, Vd, TA_c, "jet")
close(hj["steepest"]["gamma_deg"], jet_max_climb_angle(m, S, CD0, K, rho, TA_c)["gamma_deg"], 1e-6,
      "hodograph: steepest climb is the jet's maximum climb angle")
close(hj["steepest"]["V"], mt["V"], 1e-3, "hodograph: jet steepest climb at V_TR,min")
close(hj["fastest"]["Vv"], rc_an["RC_max"], 1e-6, "hodograph: fastest climb is the maximum R/C")
i_t = int(np.argmax(hj["Vv"] / hj["Vh"]))
close(float(hj["Vh"][i_t]), hj["steepest"]["Vh"], 1e-9, "hodograph: the tangent from the origin touches at the steepest climb")
PA_c = 2.4 * mp["P_min"]
hp = climb_hodograph(m, S, CD0, K, rho, Vd, PA_c, "prop")
close(hp["fastest"]["Vv"], prop_max_roc(m, S, CD0, K, rho, PA_c)["RC_max"], 1e-8, "hodograph: prop fastest is max R/C")
check(hp["steepest"]["V"] < hp["fastest"]["V"], "hodograph: steepest climb is slower than fastest climb")

# ===================================================================== 3. the look
fig, ax = plt.subplots(figsize=(4, 4))
ax.set_aspect("equal"); ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
lf = LK.level_forces(ax, (0.0, 0.0), 2.0, 8.0, LD_drawn=4.0)
close(float(np.linalg.norm(lf["L"] + lf["W"] + lf["D"] + lf["T"])), 0.0, 1e-12, "level forces balance")
cf = LK.climb_forces(ax, (0.0, 0.0), 2.0, 12.0, 5.0, LD_drawn=4.0)
close(float(np.linalg.norm(cf["L"] + cf["W"] + cf["D"] + cf["T"])), 0.0, 1e-12, "climb forces balance")
ws = LK.weight_split(ax, (1.5, 1.5), 1.0, 12.0)
close(float(np.linalg.norm(ws["along"] + ws["across"] - ws["W"])), 0.0, 1e-12, "weight split closes")
plt.close(fig)
for i in (1, 2):
    check(contrast_ratio(LK.COND_COLOR[i]) >= 3.0, f"condition {i} line contrast 3:1")
for i in range(3):
    check(contrast_ratio(LK.COND_TEXT[i]) >= 4.5, f"condition {i} text contrast 4.5:1")
for k, st in LK.CONSTRAINT_STYLE.items():
    check(contrast_ratio(st["color"]) >= 3.0, f"constraint line {k}: contrast 3:1")
    check(contrast_ratio(st["text"]) >= 4.5, f"constraint label {k}: contrast 4.5:1")
looks_ = [(str(st["color"]), str(st["ls"])) for st in LK.CONSTRAINT_STYLE.values()]
check(len(set(looks_)) == len(looks_), "every constraint line has its own look")
check(len({str(s["ls"]) for s in LK.CONSTRAINT_STYLE.values()}) >= 5, "constraint lines differ in style, not color alone")

# ===================================================================== 4. the aircraft reproduce their examples
J, GA, TR_, LT = VH.EXEC_JET, VH.GA_AIRPLANE, VH.TRANSPORT, VH.LIGHT_TWIN
TRANSPORT_CMDE_NEG = TR_["CMde"] < 0.0
close(2.0 * VH.weight(J) * math.sqrt(J["K"] * J["CD0"]), 17785.0, 2e-5, "jet: T_R,min = 17,785 N")
for rho_, T_ in ((1.112, 52482.0), (0.736, 40970.0), (0.413, 28968.0)):        # the example's densities
    close(VH.available(J, rho_), T_, 5e-5, f"jet: thrust available at {rho_} kg/m^3")
close(jet_absolute_ceiling(J["m"], J["CD0"], J["K"], J["n"], J["T0"], J["m_ad"])["rho_ceil"], 0.183, 2e-3,
      "jet: ceiling density 0.183 kg/m^3")
close(J["M_limit"], 0.80, 0, "jet: polar trusted to Mach 0.80")
g70 = level_flight_at_speed(GA["m"], GA["S"], GA["CD0"], GA["K"], RHO_SL, 70.0, GA["CL0"], GA["CLa"])
close(float(g70["CL"]), 0.2637, 2e-4, "GA airplane: C_L at 70 m/s")
close(float(g70["alpha"]), 2.031, 2e-4, "GA airplane: alpha at 70 m/s")
close(float(trim_elevator(g70["alpha"], GA["CM0"], GA["CMa"], GA["CMde"])), -0.566, 1e-3,
      "GA airplane: trim at 70 m/s is 0.566 deg trailing edge up")
check(GA["CMde"] < 0.0 and TRANSPORT_CMDE_NEG, "both moment lines follow the stated sign convention")
close(VH.available(GA, RHO_SL), 172.8e3, 1e-12, "GA airplane: power available at sea level")
gp = min_power_condition(GA["m"], GA["S"], GA["CD0"], GA["K"], RHO_SL)
close(gp["P_min"], 36.60e3, 2e-4, "GA airplane: minimum power 36.60 kW")
close(gp["V"], 32.79, 2e-4, "GA airplane: at 32.79 m/s")
Vs_ga = stall_speed_mass(GA["m"], GA["S"], GA["CLmax"], RHO_SL)
close(Vs_ga, 23.2, 2e-3, "GA airplane: stall speed 23.2 m/s with C_L,max 2.4")
check(gp["V"] > Vs_ga, "GA airplane: minimum-power speed above the stall speed")
close(GA["CL0"] + GA["CLa"] * GA["alpha_max"], GA["CLmax"], 2e-3, "GA airplane: C_L,max at alpha_max (2.396, printed 2.4)")
close(VH.power_sfc_per_m(GA), 7.456e-7, 1e-4, "GA airplane: c in 1/m")
close(TR_["K"], 0.04737, 1e-4, "transport: K from AR and e")
for h in (0.0, 6500.0):
    _, _, r_ = standard(h)[:3]
    vm, _ = prop_vmax(TR_["m"], TR_["S"], TR_["CD0"], TR_["K"], r_, VH.available(TR_, r_))
    check(vm / speed_of_sound(standard(h)[0]) < 0.6, f"transport: V_max below Mach 0.6 at {h:.0f} m")
check(math.sqrt(3.0 * TR_["CD0"] / TR_["K"]) < TR_["CLmax"], "transport: minimum-power C_L below C_L,max")
cr = level_flight_at_speed(TR_["m"], TR_["S"], TR_["CD0"], TR_["K"], standard(6500.0)[2], 150.0, TR_["CL0"], TR_["CLa"])
check(2.0 < float(cr["alpha"]) < 5.0, "transport: cruise angle of attack a few degrees")
de_c = float(trim_elevator(cr["alpha"], TR_["CM0"], TR_["CMa"], TR_["CMde"]))
check(-5.0 < de_c < 0.0, "transport: trim elevator a few degrees, trailing edge up")
close(VH.available(TR_, RHO_SL, n=3), 0.75 * VH.available(TR_, RHO_SL), 1e-12, "transport: one engine out leaves 3/4")
WSs = 0.5 * RHO_SL * VH.LIGHT_TWIN_REQ["V_stall"] ** 2 * LT["CLmax_L"]
close(WSs, 2787.0, 2e-4,"light twin: stall limit 2,787 N/m^2")
close(VH.LIGHT_TWIN_REQ["s_L"] * G0 * RHO_SL * LT["CLmax_L"] * LT["mu_r"] / 1.69, 4280.0, 2e-4,
      "light twin: landing limit 4,280 N/m^2")
close(float(tw_takeoff_line(WSs, VH.LIGHT_TWIN_REQ["s_LO"], LT["CLmax_TO"])), 0.2344, 1e-3, "light twin: T/W 0.2344")
close(takeoff_ground_roll(VH.weight(LT), LT["S"], LT["CLmax_TO"], LT["n"] * LT["T0"]), 569.0, 1e-3,
      "light twin: takeoff ground roll 569 m")
close(landing_ground_roll(VH.weight(LT), LT["S"], LT["CLmax_L"], LT["mu_r"]), 401.0, 1e-3,
      "light twin: landing ground roll 401 m")

print(f"chapter_5 selftest: {N_CHECKS} checks passed")
