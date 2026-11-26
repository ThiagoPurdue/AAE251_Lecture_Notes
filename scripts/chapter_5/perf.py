"""Aircraft performance and propulsion physics for Chapter 5.

SI units throughout (m, s, kg, N, W, Pa, kg/m^3, rad/deg as noted) unless a function explicitly
handles English units (noted in its docstring). Gravity g0 = 9.81 m/s^2 and sea-level standard
density rho0 = 1.2250 kg/m^3 come from chapter_1.atmosphere so every chapter shares one atmosphere.

Sources:
  - Anderson, J. D., Introduction to Flight, 8th ed. (McGraw-Hill, 2016), Chapters 6 and 9.
  - Raymer, D. P., Aircraft Design: A Conceptual Approach, 6th ed. (AIAA, 2018), Chapters 5 and 17.
  - NASA Glenn Research Center, Beginner's Guide to Propulsion (jet thrust equation, bypass ratio,
    propulsive efficiency).

The unit checks of this module are in scripts/chapter_5/selftest.py:  python3 -B scripts/chapter_5/selftest.py

Sections and their owners while the pages are improved in parallel: steady level flight (5.1),
range and endurance (5.2), climb and ceiling (5.3), constraint diagram and field length (no-standard
page), jet propulsion (5.4); "shared by several pages" (at the end) belongs to the chapter's shared
code and changes only through the coordinator.
"""
import math
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from chapter_1.atmosphere import G0, RHO_SL, standard, altitude_from_density, speed_of_sound  # noqa: E402
from chapter_3.aero import polar_K, polar_CD, min_drag_point, level_CL, dynamic_pressure  # noqa: E402

# English-unit constants (NIST SP 811 / Anderson)
G_EN = 32.174            # ft/s^2 (exact standard gravity in ft/s^2; the CJ-1 example of Anderson (2016), Chapter 6, uses 32.17)
FT_PER_MI = 5280.0       # ft per statute mile
FT_PER_M = 1.0 / 0.3048
HP_TO_W = 745.7          # W per mechanical horsepower
SERVICE_CEILING_RC = 0.5  # m/s (about 100 ft/min), standard jet/prop service-ceiling definition


# ===================================================================== steady level flight: thrust and power
def thrust_required_parts(m, S, CD0, K, rho, V, g=G0):
    """Parasite, induced and total thrust required in steady level flight, N:
    T_R = 1/2 rho V^2 S C_D,0 + 2 K (m g)^2 / (rho S V^2). Returns (T_R0, T_Ri, T_R)."""
    W = m * g
    V = np.asarray(V, dtype=float)
    qS = 0.5 * rho * V ** 2 * S
    T0 = qS * CD0
    Ti = K * W ** 2 / qS
    return T0, Ti, T0 + Ti


def thrust_required(m, S, CD0, K, rho, V, g=G0):
    """Total thrust required T_R(V) in steady level flight, N."""
    return thrust_required_parts(m, S, CD0, K, rho, V, g=g)[2]


def power_required_parts(m, S, CD0, K, rho, V, g=G0):
    """Parasite, induced and total power required in steady level flight, W:
    P_R = T_R V = 1/2 rho S C_D,0 V^3 + 2 K (m g)^2 / (rho S V). Returns (P_R0, P_Ri, P_R)."""
    T0, Ti, T = thrust_required_parts(m, S, CD0, K, rho, V, g=g)
    V = np.asarray(V, dtype=float)
    return T0 * V, Ti * V, T * V


def power_required(m, S, CD0, K, rho, V, g=G0):
    """Total power required P_R(V) = T_R(V) V in steady level flight, W."""
    return power_required_parts(m, S, CD0, K, rho, V, g=g)[2]


def thrust_available(n, T0, rho, m_ad, delta_t=1.0, rho0=RHO_SL):
    """Jet thrust available, N: T_A = n delta_t T_0 (rho / rho_0)^m_ad."""
    return n * delta_t * T0 * (np.asarray(rho, dtype=float) / rho0) ** m_ad


def power_available(n, P0, eta, rho, m_ad, delta_t=1.0, rho0=RHO_SL):
    """Propeller shaft power delivered to the air, W: P_A = n delta_t eta P_0 (rho / rho_0)^m_ad."""
    return n * delta_t * eta * P0 * (np.asarray(rho, dtype=float) / rho0) ** m_ad


def min_thrust_condition(m, S, CD0, K, rho, g=G0):
    """Minimum thrust required in steady level flight (also (L/D)max):
    C_L = sqrt(C_D,0 / K), C_D = 2 C_D,0, V = sqrt(2 m g / (rho S)) (K / C_D,0)^(1/4),
    T_R,min = 2 m g sqrt(K C_D,0). Returns a dict."""
    W = m * g
    CL = math.sqrt(CD0 / K)
    CD = 2.0 * CD0
    LD_max = CL / CD
    V = math.sqrt(2.0 * W / (rho * S)) * (K / CD0) ** 0.25
    T_min = 2.0 * W * math.sqrt(K * CD0)
    return dict(CL=CL, CD=CD, LD_max=LD_max, V=V, T_min=T_min, P_at_Tmin=T_min * V)


def min_power_condition(m, S, CD0, K, rho, g=G0):
    """Minimum power required in steady level flight (max C_L^(3/2)/C_D):
    C_L = sqrt(3 C_D,0 / K), C_D = 4 C_D,0, V = sqrt(2 m g / (rho S)) (K / (3 C_D,0))^(1/4),
    P_R,min = (4/3) sqrt((2 (m g)^3 / (rho S)) sqrt(3 K^3 C_D,0)). Returns a dict."""
    W = m * g
    CL = math.sqrt(3.0 * CD0 / K)
    CD = 4.0 * CD0
    V = math.sqrt(2.0 * W / (rho * S)) * (K / (3.0 * CD0)) ** 0.25
    P_min = (4.0 / 3.0) * math.sqrt((2.0 * W ** 3 / (rho * S)) * math.sqrt(3.0 * K ** 3 * CD0))
    return dict(CL=CL, CD=CD, ratio=CL ** 1.5 / CD, V=V, P_min=P_min, T_at_Pmin=P_min / V)


def jet_speed_bounds(m, S, CD0, K, rho, TA, g=G0):
    """Level-flight speeds where T_R(V) = T_A for a jet (constant T_A with V), solved from the
    quadratic in V^2: 1/2 rho S C_D,0 V^4 - T_A V^2 + 2 K W^2 / (rho S) = 0.
    Returns (V_low, V_max) in m/s, or (None, None) if T_A < T_R,min."""
    W = m * g
    disc = TA ** 2 - 4.0 * CD0 * K * W ** 2
    if disc < 0.0:
        return None, None
    r = math.sqrt(disc)
    v_lo = math.sqrt(max((TA - r) / (rho * S * CD0), 0.0))
    v_hi = math.sqrt((TA + r) / (rho * S * CD0))
    return v_lo, v_hi


def prop_vmax(m, S, CD0, K, rho, PA, g=G0, n_iter=60):
    """Maximum level-flight speed V_max (m/s) of a propeller aircraft where P_R(V) = P_A, by
    fixed-point iteration starting from the zero-induced-drag estimate V0 = (2 P_A / (rho S C_D,0))^(1/3).
    Returns (V_max, history) or (None, []) if P_A < P_R,min."""
    mp = min_power_condition(m, S, CD0, K, rho, g=g)
    if PA < mp["P_min"]:
        return None, []
    W = m * g
    V = (2.0 * PA / (rho * S * CD0)) ** (1.0 / 3.0)
    hist = [V]
    for _ in range(n_iter):
        rhs = PA - 2.0 * K * W ** 2 / (rho * S * V)
        if rhs <= 0.0:
            break
        V_new = ((2.0 / (rho * S * CD0)) * rhs) ** (1.0 / 3.0)
        hist.append(V_new)
        if abs(V_new - V) < 1e-12:
            V = V_new
            break
        V = V_new
    return V, hist


def stall_speed_mass(m, S, CL_max, rho, g=G0):
    """Level-flight stall speed, m/s: V_stall = sqrt(2 m g / (rho S C_L,max))."""
    return math.sqrt(2.0 * m * g / (rho * S * CL_max))


# ===================================================================== range and endurance (Breguet)
def jet_best_range_polar(CD0, K):
    """Best jet range polar point (max C_L^(1/2)/C_D): C_L = sqrt(C_D,0 / (3 K)), C_D = (4/3) C_D,0."""
    CL = math.sqrt(CD0 / (3.0 * K))
    CD = CD0 + K * CL ** 2
    return dict(CL=CL, CD=CD, ratio=math.sqrt(CL) / CD, LD=CL / CD)


def jet_range(m1, m2, S, rho, ct, CL, CD, g=G0):
    """Breguet jet range, m (or ft in consistent English units):
    R = (2 / c_t) sqrt(2 g / (rho S)) (sqrt(C_L) / C_D) (sqrt(m1) - sqrt(m2))."""
    return (2.0 / ct) * math.sqrt(2.0 * g / (rho * S)) * (math.sqrt(CL) / CD) * (math.sqrt(m1) - math.sqrt(m2))


def jet_endurance(m1, m2, ct, CL, CD):
    """Breguet jet endurance, s: E = (1 / c_t) (C_L / C_D) ln(m1 / m2)."""
    return (1.0 / ct) * (CL / CD) * math.log(m1 / m2)


def jet_fuel_for_range(m1, R, S, rho, ct, CL, CD, g=G0):
    """Fuel mass m_f = m1 - m2 needed for a jet to fly range R, kg."""
    A = (2.0 / ct) * math.sqrt(2.0 * g / (rho * S)) * (math.sqrt(CL) / CD)
    sm2 = math.sqrt(m1) - R / A
    if sm2 <= 0.0:
        raise ValueError("required range exceeds physically possible mass ratio")
    m2 = sm2 ** 2
    return m1 - m2, m2


def prop_range(m1, m2, eta, c, CL, CD):
    """Breguet propeller range, m: R = (eta / c) (C_L / C_D) ln(m1 / m2), with c in 1/m (weight flow / shaft power)."""
    return (eta / c) * (CL / CD) * math.log(m1 / m2)


def prop_endurance(m1, m2, S, rho, eta, c, CL, CD, g=G0):
    """Breguet propeller endurance, s:
    E = (eta / c) sqrt(2 rho S / g) (C_L^(3/2) / C_D) (1/sqrt(m2) - 1/sqrt(m1))."""
    return (eta / c) * math.sqrt(2.0 * rho * S / g) * (CL ** 1.5 / CD) * (1.0 / math.sqrt(m2) - 1.0 / math.sqrt(m1))


def prop_fuel_for_range(m1, R, eta, c, CL, CD):
    """Fuel mass m_f = m1 - m2 needed for a propeller aircraft to fly range R, kg."""
    m2 = m1 * math.exp(-R * c / (eta * (CL / CD)))
    return m1 - m2, m2


def prop_fuel_for_endurance(m1, E, S, rho, eta, c, CL, CD, g=G0):
    """Fuel mass m_f = m1 - m2 needed for a propeller aircraft to loiter for time E (s), kg."""
    B = (eta / c) * math.sqrt(2.0 * rho * S / g) * (CL ** 1.5 / CD)
    inv_sm2 = 1.0 / math.sqrt(m1) + E / B
    m2 = 1.0 / (inv_sm2 ** 2)
    return m1 - m2, m2


def jet_fuel_for_endurance(m1, E, ct, CL, CD):
    """Fuel mass m_f = m1 - m2 needed for a jet to stay aloft for time E (s) at constant C_L, kg:
    the jet endurance equation solved for m2, m_f = m1 [1 - exp(-c_t E C_D / C_L)]. Returns (m_f, m2)."""
    m2 = m1 * math.exp(-ct * E * CD / CL)
    return m1 - m2, m2


def jet_best_range_thrust(m, CD0, K, g=G0):
    """Thrust required at the best-range lift coefficient of a jet, N: with C_L = sqrt(C_D,0 / (3K))
    and C_D = (4/3) C_D,0, T_R = m g C_D / C_L = 4 m g sqrt(K C_D,0 / 3). It does not depend on the
    density; it is 2/sqrt(3) = 1.155 times the minimum thrust required."""
    return 4.0 * m * g * math.sqrt(K * CD0 / 3.0)


def jet_best_range_throttle(m, CD0, K, n, T0, rho, m_ad, g=G0, rho0=RHO_SL):
    """Throttle setting delta_t that makes the thrust available equal the best-range thrust required:
    n delta_t T_0 (rho/rho_0)^m_ad = 4 m g sqrt(K C_D,0 / 3). A value above 1 means the engines cannot
    hold the best-range condition at that density."""
    return jet_best_range_thrust(m, CD0, K, g=g) / (n * T0 * (rho / rho0) ** m_ad)


def jet_best_range_density_limit(m, CD0, K, n, T0, m_ad, g=G0, rho0=RHO_SL):
    """Lowest density (kg/m^3) at which full throttle still gives the best-range thrust:
    rho = rho_0 [4 m g sqrt(K C_D,0 / 3) / (n T_0)]^(1/m_ad). Returns dict(rho, h)."""
    rho = rho0 * (jet_best_range_thrust(m, CD0, K, g=g) / (n * T0)) ** (1.0 / m_ad)
    return dict(rho=rho, h=altitude_from_density(rho))


# ===================================================================== climb and ceiling
def climb_jet(m, S, CD0, K, rho, TA, V, g=G0):
    """Steady shallow-climb performance of a jet at speed V and available thrust T_A:
    sin(gamma) = (T_A - D) / (m g), R/C = (T_A - D) V / (m g). Returns dict(D, P_R, P_A, sin_gamma, gamma_deg, RC)."""
    W = m * g
    D = thrust_required(m, S, CD0, K, rho, V, g=g)
    sin_g = (TA - D) / W
    gam = np.degrees(np.arcsin(np.clip(sin_g, -1.0, 1.0)))
    RC = (TA - D) * V / W
    return dict(D=D, P_R=D * V, P_A=TA * V, sin_gamma=sin_g, gamma_deg=gam, RC=RC)


def climb_prop(m, S, CD0, K, rho, PA, V, g=G0):
    """Steady shallow-climb performance of a propeller aircraft at speed V and available power P_A:
    R/C = (P_A - P_R) / (m g), sin(gamma) = R/C / V. Returns dict(D, P_R, P_A, sin_gamma, gamma_deg, RC)."""
    W = m * g
    D = thrust_required(m, S, CD0, K, rho, V, g=g)
    PR = D * V
    RC = (PA - PR) / W
    sin_g = RC / V
    gam = np.degrees(np.arcsin(np.clip(sin_g, -1.0, 1.0)))
    return dict(D=D, P_R=PR, P_A=PA, sin_gamma=sin_g, gamma_deg=gam, RC=RC)


def jet_max_climb_angle(m, S, CD0, K, rho, TA, g=G0):
    """Maximum climb angle of a jet (constant T_A with V), reached at V_TR,min:
    sin(gamma_max) = T_A / (m g) - 2 sqrt(K C_D,0). Returns dict(V, T_min, sin_gamma, gamma_rad, gamma_deg)."""
    W = m * g
    mt = min_thrust_condition(m, S, CD0, K, rho, g=g)
    sg = TA / W - 2.0 * math.sqrt(K * CD0)
    return dict(V=mt["V"], T_min=mt["T_min"], sin_gamma=sg, gamma_rad=math.asin(max(min(sg, 1.0), -1.0)),
                gamma_deg=math.degrees(math.asin(max(min(sg, 1.0), -1.0))))


def jet_max_roc(m, S, CD0, K, rho, TA, g=G0):
    """Maximum rate of climb of a jet at density rho and thrust available T_A (exact analytical speed
    from d[(T_A - D)V]/dV = 0, Anderson (2016), Chapter 6). Returns dict(V, RC_max, gamma_deg, D, P_A, P_R)."""
    W = m * g
    Z = 1.0 + math.sqrt(1.0 + 3.0 / (((1.0 / (2.0 * math.sqrt(K * CD0))) ** 2) * (TA / W) ** 2))
    V = math.sqrt((TA / (3.0 * rho * S * CD0)) * Z)
    c = climb_jet(m, S, CD0, K, rho, TA, V, g=g)
    return dict(V=V, RC_max=float(c["RC"]), gamma_deg=float(c["gamma_deg"]), D=float(c["D"]),
                P_A=float(c["P_A"]), P_R=float(c["P_R"]))


def prop_max_roc(m, S, CD0, K, rho, PA, g=G0):
    """Maximum rate of climb of a propeller aircraft (constant P_A with V), reached at V_PR,min:
    (R/C)_max = (P_A - P_R,min) / (m g). Returns dict(V, P_min, RC_max, gamma_deg)."""
    W = m * g
    mp = min_power_condition(m, S, CD0, K, rho, g=g)
    rc = (PA - mp["P_min"]) / W
    sg = max(min(rc / mp["V"], 1.0), -1.0)
    return dict(V=mp["V"], P_min=mp["P_min"], RC_max=rc, gamma_deg=math.degrees(math.asin(sg)))


def jet_absolute_ceiling(m, CD0, K, n, T0, m_ad, g=G0, rho0=RHO_SL):
    """Analytical absolute ceiling of a jet: T_A,max(rho) = T_R,min = 2 m g sqrt(K C_D,0).
    Returns dict(T_min, rho_ceil, h_abs)."""
    W = m * g
    T_min = 2.0 * W * math.sqrt(K * CD0)
    rho_c = rho0 * (T_min / (n * T0)) ** (1.0 / m_ad)
    return dict(T_min=T_min, rho_ceil=rho_c, h_abs=altitude_from_density(rho_c))


def prop_absolute_ceiling(m, S, CD0, K, n, P0, eta, m_ad, g=G0, rho0=RHO_SL):
    """Analytical absolute ceiling of a propeller aircraft: P_A,max(rho) = P_R,min(rho).
    Returns dict(rho_ceil, h_abs, P_ceil)."""
    W = m * g
    c_pmin = (4.0 / 3.0) * math.sqrt((2.0 * W ** 3 / S) * math.sqrt(3.0 * K ** 3 * CD0))
    PA0 = n * eta * P0
    rho_c = (c_pmin * (rho0 ** m_ad) / PA0) ** (2.0 / (2.0 * m_ad + 1.0))
    return dict(rho_ceil=rho_c, h_abs=altitude_from_density(rho_c), P_ceil=PA0 * (rho_c / rho0) ** m_ad)


def ceiling_by_bisection(rc_of_h, target=SERVICE_CEILING_RC, h_lo=0.0, h_hi=24000.0):
    """Altitude (m) where maximum rate of climb rc_of_h(h) equals `target` (m/s)."""
    lo, hi = float(h_lo), float(h_hi)
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if rc_of_h(mid) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ===================================================================== constraint diagram & field length
def takeoff_ground_roll(W, S, CL_max_TO, T, rho=RHO_SL, g=G0):
    """Approximate takeoff ground roll (Anderson (2016), Chapter 6), m: s_LO = 1.44 W^2 / (g rho S C_L,max,TO T)."""
    return 1.44 * W ** 2 / (g * rho * S * CL_max_TO * T)


def landing_ground_roll(W, S, CL_max_L, mu_r, rho=RHO_SL, g=G0):
    """Approximate landing ground roll with braking friction mu_r (Anderson (2016), Chapter 6; drag and lift neglected), m:
    s_L = 1.69 W / (g rho S C_L,max,L mu_r)."""
    return 1.69 * W / (g * rho * S * CL_max_L * mu_r)


def tw_takeoff_line(WS, s_LO, CL_max_TO, rho=RHO_SL, g=G0):
    """Sea-level T/W required to meet takeoff ground roll s_LO as a function of W/S."""
    return 1.44 * np.asarray(WS, dtype=float) / (g * rho * CL_max_TO * s_LO)


def tw_climb_line(WS, RC, V, CD0, K, rho=RHO_SL, m_ad=0.8, rho0=RHO_SL):
    """Sea-level T/W required for rate of climb RC at speed V and density rho as a function of W/S."""
    WS = np.asarray(WS, dtype=float)
    q = 0.5 * rho * V ** 2
    tw_alt = RC / V + q * CD0 / WS + K * WS / q
    return tw_alt / ((rho / rho0) ** m_ad)


def tw_cruise_line(WS, V, CD0, K, rho, m_ad=0.8, rho0=RHO_SL):
    """Sea-level T/W required for steady level cruise at speed V and density rho as a function of W/S."""
    return tw_climb_line(WS, 0.0, V, CD0, K, rho=rho, m_ad=m_ad, rho0=rho0)


def tw_ceiling_line(WS, RC_ceil, CD0, K, rho, m_ad=0.8, rho0=RHO_SL):
    """Sea-level T/W required for rate of climb RC_ceil at ceiling density rho (evaluated at V_TR,min)."""
    WS = np.asarray(WS, dtype=float)
    V = np.sqrt(2.0 * WS / rho * math.sqrt(K / CD0))
    return (RC_ceil / V + 2.0 * math.sqrt(K * CD0)) / ((rho / rho0) ** m_ad)


# ===================================================================== jet propulsion
def jet_thrust_eq(m_air, m_fuel, V_e, V_inf, p_e=0.0, p_inf=0.0, A_e=0.0):
    """Air-breathing jet engine thrust, N: T = (m_air + m_fuel) V_e - m_air V_inf + (p_e - p_inf) A_e."""
    return (m_air + m_fuel) * V_e - m_air * V_inf + (p_e - p_inf) * A_e


def propulsive_efficiency(V_inf, V_e):
    """Ideal propulsive efficiency of a jet (neglecting fuel mass flow): eta_p = 2 / (1 + V_e / V_inf)."""
    return 2.0 / (1.0 + np.asarray(V_e, dtype=float) / np.asarray(V_inf, dtype=float))


# ===================================================================== shared by several pages
# Owner: the chapter's shared code (pages 5.1, 5.3 and the no-standard page use these). Source of
# every relation here: Anderson (2016), Chapter 6 (steady level flight, climb), with the lift curve
# and the pitching-moment line of the example aircraft of `vehicles.py`.
def lift_line(alpha_deg, CL0, CLa):
    """Lift coefficient on the straight part of the lift curve, C_L = C_L,0 + C_L,alpha alpha
    (alpha in degrees). Valid below the stall only: compare the result with C_L,max."""
    return CL0 + CLa * np.asarray(alpha_deg, dtype=float)


def alpha_for_CL(CL, CL0, CLa):
    """Angle of attack (deg) on the straight lift curve for a lift coefficient: (C_L - C_L,0) / C_L,alpha."""
    return (np.asarray(CL, dtype=float) - CL0) / CLa


def level_flight_at_speed(m, S, CD0, K, rho, V, CL0=None, CLa=None, g=G0):
    """Steady level flight at a given true airspeed V (the "speed given" problem). Assumes the thrust
    acts along the flight path or at a small angle to it, so L = m g and T_R = D. Returns
    dict(CL, CD, LD, L, D, T_R, P_R) and, when the lift curve is given, alpha (deg). The caller checks
    the result against C_L,max and against the thrust or power available."""
    W = m * g
    V = np.asarray(V, dtype=float)
    q = 0.5 * rho * V ** 2
    CL = W / (q * S)
    CD = CD0 + K * CL ** 2
    D = q * S * CD
    out = dict(CL=CL, CD=CD, LD=CL / CD, L=W + 0.0 * V, D=D, T_R=D, P_R=D * V)
    if CL0 is not None and CLa is not None:
        out["alpha"] = alpha_for_CL(CL, CL0, CLa)
    return out


def level_flight_at_alpha(m, S, CD0, K, rho, alpha_deg, CL0, CLa, g=G0):
    """Steady level flight at a given angle of attack (the "angle of attack given" problem): the lift
    curve gives C_L, the polar gives C_D, then V = sqrt(2 m g / (rho S C_L)), T_R = m g / (L/D),
    P_R = T_R V. Needs C_L > 0 (a positive angle above zero lift). Returns
    dict(alpha, CL, CD, LD, V, L, D, T_R, P_R)."""
    W = m * g
    CL = lift_line(alpha_deg, CL0, CLa)
    if np.any(CL <= 0.0):
        raise ValueError("level flight needs a positive lift coefficient")
    CD = CD0 + K * CL ** 2
    V = np.sqrt(2.0 * W / (rho * S * CL))
    TR = W * CD / CL
    return dict(alpha=np.asarray(alpha_deg, dtype=float), CL=CL, CD=CD, LD=CL / CD, V=V,
                L=W + 0.0 * CL, D=TR, T_R=TR, P_R=TR * V)


def thrust_required_vs_alpha(m, CD0, K, CL0, CLa, alpha_deg, g=G0):
    """Thrust required in steady level flight against angle of attack: T_R = m g / (L/D), with C_L from
    the lift curve and C_D from the polar. The density and the wing area do not enter: at one angle of
    attack the aircraft needs the same thrust at every altitude (only the speed changes). Returns
    dict(alpha, CL, CD, LD, T_R) for the angles where C_L > 0."""
    a = np.asarray(alpha_deg, dtype=float)
    CL = lift_line(a, CL0, CLa)
    keep = CL > 0.0
    a, CL = a[keep], CL[keep]
    CD = CD0 + K * CL ** 2
    return dict(alpha=a, CL=CL, CD=CD, LD=CL / CD, T_R=m * g * CD / CL)


def trim_elevator(alpha_deg, CM0, CMa, CMde):
    """Elevator angle (deg) that makes the pitching moment zero (trim) at angle of attack alpha:
    C_M = C_M,0 + C_M,alpha alpha + C_M,de delta_e = 0, so delta_e = -(C_M,0 + C_M,alpha alpha) / C_M,de.
    The sign of the answer follows the convention of the coefficients (vehicles.py states it)."""
    return -(CM0 + CMa * np.asarray(alpha_deg, dtype=float)) / CMde


def level_speed_range(m, S, CD0, K, rho, CLmax, available_, kind, g=G0):
    """The speeds at which steady level flight is possible at density rho, for a jet (kind="jet",
    available_ = thrust available T_A, N, taken constant with speed) or a propeller aircraft
    (kind="prop", available_ = power available P_A, W, taken constant with speed).
    The low end is the higher of the stall speed and the low-speed crossing of available and
    required; the high end is the high-speed crossing. Returns dict(V_stall, V_low, V_min, V_max,
    low_limit) with low_limit "stall" or "thrust" or "power"; V_min and V_max are None when the
    aircraft cannot hold level flight there (available below the minimum required)."""
    Vs = stall_speed_mass(m, S, CLmax, rho, g=g)
    if kind == "jet":
        v_lo, v_hi = jet_speed_bounds(m, S, CD0, K, rho, available_, g=g)
    elif kind == "prop":
        v_hi, _ = prop_vmax(m, S, CD0, K, rho, available_, g=g)
        v_lo = None
        if v_hi is not None:                      # low crossing: bisection between a slow speed and V_PR,min
            lo, hi = 1.0e-3, min_power_condition(m, S, CD0, K, rho, g=g)["V"]
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if float(power_required(m, S, CD0, K, rho, mid, g=g)) > available_:
                    lo = mid
                else:
                    hi = mid
            v_lo = 0.5 * (lo + hi)
    else:
        raise ValueError("kind is 'jet' or 'prop'")
    if v_hi is None:
        return dict(V_stall=Vs, V_low=None, V_min=None, V_max=None, low_limit=None)
    if v_hi <= Vs:
        return dict(V_stall=Vs, V_low=v_lo, V_min=None, V_max=None, low_limit="stall")
    low_limit = "stall" if Vs >= v_lo else ("thrust" if kind == "jet" else "power")
    return dict(V_stall=Vs, V_low=v_lo, V_min=max(Vs, v_lo), V_max=v_hi, low_limit=low_limit)


def climb_required(m, S, CD0, K, rho, V, gamma_deg, g=G0, small_angle=False):
    """Thrust and power required in a steady climb at speed V and climb angle gamma (thrust along
    the flight path): L = m g cos(gamma), T_R = D + m g sin(gamma), with
    D = 1/2 rho V^2 S C_D,0 + 2 K (m g cos(gamma))^2 / (rho S V^2), and P_R = T_R V.
    small_angle=True uses cos(gamma) = 1 and sin(gamma) = gamma (radians), the form in which the
    level-flight curves are simply raised by m g gamma (thrust) and m g gamma V (power). Returns
    dict(parasite, induced, weight_part, T_R, P_R), each in N except P_R in W."""
    W = m * g
    V = np.asarray(V, dtype=float)
    gr = math.radians(gamma_deg)
    c, s = (1.0, gr) if small_angle else (math.cos(gr), math.sin(gr))
    qS = 0.5 * rho * V ** 2 * S
    par = qS * CD0
    ind = K * (W * c) ** 2 / qS
    wp = W * s + 0.0 * V
    TR = par + ind + wp
    return dict(parasite=par, induced=ind, weight_part=wp, T_R=TR, P_R=TR * V)


def climb_hodograph(m, S, CD0, K, rho, V, available_, kind, g=G0):
    """The climb hodograph: vertical speed (rate of climb, R/C) against horizontal speed V cos(gamma)
    for every airspeed V, in the shallow-climb model of climb_jet and climb_prop (drag at L = m g;
    kind "jet" with thrust available T_A in N, "prop" with power available P_A in W). The tangent
    from the origin to the curve touches it at the steepest climb (largest gamma); the top of the
    curve is the fastest climb (largest R/C). Returns dict(V, Vh, Vv, gamma_deg, steepest, fastest),
    steepest and fastest each dict(V, Vh, Vv, gamma_deg) at the best grid point of V (pass a dense V)."""
    V = np.asarray(V, dtype=float)
    c = (climb_jet if kind == "jet" else climb_prop)(m, S, CD0, K, rho, available_, V, g=g)
    gam = np.asarray(c["gamma_deg"], dtype=float)
    Vv = np.asarray(c["RC"], dtype=float)
    Vh = V * np.cos(np.radians(gam))
    i_s, i_f = int(np.argmax(gam)), int(np.argmax(Vv))
    pick = lambda i: dict(V=float(V[i]), Vh=float(Vh[i]), Vv=float(Vv[i]), gamma_deg=float(gam[i]))  # noqa: E731
    return dict(V=V, Vh=Vh, Vv=Vv, gamma_deg=gam, steepest=pick(i_s), fastest=pick(i_f))
