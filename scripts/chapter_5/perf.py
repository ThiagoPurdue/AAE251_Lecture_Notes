"""Aircraft performance and propulsion physics for Chapter 5.

SI units throughout (m, s, kg, N, W, Pa, kg/m^3, rad/deg as noted) unless a function explicitly
handles English units (noted in its docstring). Gravity g0 = 9.81 m/s^2 and sea-level standard
density rho0 = 1.2250 kg/m^3 come from chapter_1.atmosphere so every chapter shares one atmosphere.

Sources:
  - Anderson, J. D., Introduction to Flight, 8th ed. (McGraw-Hill, 2016), Chapters 6 and 9.
  - Raymer, D. P., Aircraft Design: A Conceptual Approach, 4th ed. (AIAA, 2006), Chapters 5 and 17.
  - NASA Glenn Research Center, Beginner's Guide to Propulsion (jet thrust equation, bypass ratio,
    propulsive efficiency).

Run this file for its unit checks:  python3 -B scripts/chapter_5/perf.py
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
G_EN = 32.174            # ft/s^2 (exact standard gravity in ft/s^2; Anderson Example 6.19 uses 32.17)
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
    from d[(T_A - D)V]/dV = 0, Anderson Eq. 6.77). Returns dict(V, RC_max, gamma_deg, D, P_A, P_R)."""
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
    """Approximate takeoff ground roll (Anderson Section 6.15), m: s_LO = 1.44 W^2 / (g rho S C_L,max,TO T)."""
    return 1.44 * W ** 2 / (g * rho * S * CL_max_TO * T)


def landing_ground_roll(W, S, CL_max_L, mu_r, rho=RHO_SL, g=G0):
    """Approximate landing ground roll with braking friction mu_r (Anderson Section 6.16, drag & lift neglected), m:
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


# ===================================================================== unit checks
def _close(a, b, rtol, what):
    assert abs(a - b) <= rtol * max(abs(b), 1e-12), f"{what}: {a!r} vs {b!r}"


if __name__ == "__main__":
    # 1. Minimum thrust and power match dense numerical grid
    m, S, CD0, K, rho = 15000.0, 48.0, 0.020, 0.045, 0.90
    V = np.linspace(40.0, 300.0, 200001)
    T0, Ti, TR = thrust_required_parts(m, S, CD0, K, rho, V)
    P0_, Pi_, PR = power_required_parts(m, S, CD0, K, rho, V)
    mt = min_thrust_condition(m, S, CD0, K, rho)
    mp = min_power_condition(m, S, CD0, K, rho)
    _close(float(V[np.argmin(TR)]), mt["V"], 1e-4, "V_TR,min matches grid")
    _close(float(np.min(TR)), mt["T_min"], 1e-7, "T_R,min matches grid")
    _close(float(V[np.argmin(PR)]), mp["V"], 1e-4, "V_PR,min matches grid")
    _close(float(np.min(PR)), mp["P_min"], 1e-7, "P_R,min matches grid")
    _close(mp["V"] / mt["V"], 3.0 ** (-0.25), 1e-12, "V_PR,min / V_TR,min = 3^(-1/4)")
    # At V_PR,min: induced drag is 3x parasite drag
    T0p, Tip, _ = thrust_required_parts(m, S, CD0, K, rho, mp["V"])
    _close(float(Tip), 3.0 * float(T0p), 1e-10, "at V_PR,min, D_i = 3 D_0")
    # At jet best range: parasite drag is 3x induced drag
    jr = jet_best_range_polar(CD0, K)
    _close(K * jr["CL"] ** 2, CD0 / 3.0, 1e-12, "at jet best range, D_0 = 3 D_i")
    # 2. Jet and prop Vmax satisfy T_R = T_A and P_R = P_A
    vlo, vhi = jet_speed_bounds(m, S, CD0, K, rho, 2.2 * mt["T_min"])
    _close(float(thrust_required(m, S, CD0, K, rho, vhi)), 2.2 * mt["T_min"], 1e-10, "jet Vmax exact")
    _close(float(thrust_required(m, S, CD0, K, rho, vlo)), 2.2 * mt["T_min"], 1e-10, "jet Vlow exact")
    vpmax, _ = prop_vmax(m, S, CD0, K, rho, 3.0 * mp["P_min"])
    _close(float(power_required(m, S, CD0, K, rho, vpmax)), 3.0 * mp["P_min"], 1e-9, "prop Vmax exact")
    # 3. Range and endurance round-trips with fuel solvers
    R_test = jet_range(m, 0.8 * m, S, rho, 1.7e-4, jr["CL"], jr["CD"])
    mf_back, _ = jet_fuel_for_range(m, R_test, S, rho, 1.7e-4, jr["CL"], jr["CD"])
    _close(mf_back, 0.2 * m, 1e-10, "jet range fuel round-trip")
    Rp_test = prop_range(m, 0.85 * m, 0.82, 7.0e-7, mt["CL"], mt["CD"])
    mfp_back, _ = prop_fuel_for_range(m, Rp_test, 0.82, 7.0e-7, mt["CL"], mt["CD"])
    _close(mfp_back, 0.15 * m, 1e-10, "prop range fuel round-trip")
    Ep_test = prop_endurance(m, 0.85 * m, S, rho, 0.82, 7.0e-7, mp["CL"], mp["CD"])
    mfe_back, _ = prop_fuel_for_endurance(m, Ep_test, S, rho, 0.82, 7.0e-7, mp["CL"], mp["CD"])
    _close(mfe_back, 0.15 * m, 1e-10, "prop endurance fuel round-trip")
    # 4. Jet max R/C matches dense numerical search, and analytical ceiling matches bisection
    TA_c = 2.0 * mt["T_min"]
    rc_an = jet_max_roc(m, S, CD0, K, rho, TA_c)
    rc_grid = float(np.max(climb_jet(m, S, CD0, K, rho, TA_c, V)["RC"]))
    _close(rc_an["RC_max"], rc_grid, 1e-6, "jet max R/C analytical vs grid")
    jc = jet_absolute_ceiling(m, CD0, K, 2, 1.1 * mt["T_min"], 0.7)
    h_bis = ceiling_by_bisection(
        lambda h: jet_max_roc(m, S, CD0, K, standard(h)[2],
                              thrust_available(2, 1.1 * mt["T_min"], standard(h)[2], 0.7))["RC_max"],
        target=0.0,
    )
    _close(jc["h_abs"], h_bis, 1e-4, "jet analytical ceiling matches bisection")
    pc = prop_absolute_ceiling(m, S, CD0, K, 2, 1.8 * mp["P_min"], 0.80, 0.85)
    hp_bis = ceiling_by_bisection(
        lambda h: prop_max_roc(m, S, CD0, K, standard(h)[2],
                               power_available(2, 1.8 * mp["P_min"], 0.80, standard(h)[2], 0.85))["RC_max"],
        target=0.0,
    )
    _close(pc["h_abs"], hp_bis, 1e-4, "prop analytical ceiling matches bisection")
    # 5. Propulsive efficiency bounds
    _close(float(propulsive_efficiency(200.0, 200.0)), 1.0, 1e-12, "eta_p = 1 when V_e = V_inf")
    _close(float(propulsive_efficiency(200.0, 600.0)), 0.5, 1e-12, "eta_p = 0.5 when V_e = 3 V_inf")
    print("perf.py: all unit checks passed")
