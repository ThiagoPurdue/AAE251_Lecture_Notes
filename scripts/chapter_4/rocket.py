"""Thrust, specific impulse and the rocket equation (pages 4.1 to 4.3). SI units at the API: N, kg,
kg/s, m/s, Pa, m^2, s. Symbols as the pages write them: F, mdot, V_e, p_e, p_a, A_e, c, I_sp, g0,
m_i, m_f, m_pay, m_inert, m_prop, f_inert = m_inert / (m_inert + m_prop).

  thrust F = mdot V_e + (p_e - p_a) A_e; its two parts; the same for an engine that breathes air,
  F = mdot (V_e - V_inf) + (p_e - p_inf) A_e (the fuel flow neglected); c = F / mdot; I_sp = c / g0.
  The rocket equation dV = c ln(m_i / m_f), both ways; the stage sizing
  m_prop = m_pay (e^x - 1)(1 - f) / (1 - f e^x), x = dV / c; the single-stage limit c ln(1/f).

g0 is 9.81 m/s^2, the value used throughout the course, taken from page 1.4's shared code
(chapter_1.atmosphere.G0) and never typed again. The ambient pressure against altitude is page
1.4's standard atmosphere (chapter_1.atmosphere.standard, valid to 59.5 km).

Sources: Sutton, G. P., and Biblarz, O., Rocket Propulsion Elements, Chapters 2 and 4 (thrust,
specific impulse, the rocket equation, stage relations); NASA SP-125 (Huzel and Huang, 1967),
Section 1.2, Eqs. (1-31) to (1-34) (thrust, specific impulse); NASA Glenn Research Center,
"Beginner's Guide to Rockets" (rocket thrust equation, specific impulse, ideal rocket equation).

Run this file for its unit checks:  python3 -B scripts/chapter_4/rocket.py
"""
import math
import sys
from pathlib import Path

import numpy as np

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chapter_1.atmosphere import G0, P_SL, standard, H_TOP  # noqa: E402

__all__ = ["G0", "thrust", "thrust_parts", "air_breathing_thrust", "effective_exhaust_velocity", "isp_from_c",
           "c_from_isp", "isp_from_thrust", "mass_flow", "expansion_state", "EXPANSION_STATES", "exit_area_from_thrusts",
           "diameter_from_area", "area_from_diameter", "ambient_pressure", "fixed_nozzle_thrust", "fixed_nozzle_isp",
           "delta_v", "mass_ratio", "propellant_share", "final_mass", "inert_mass_fraction", "inert_from_prop",
           "size_stage", "stage_factor", "single_stage_limit", "stage_delta_v", "gravity_loss_constant_angle",
           "StageLimitError"]

EXPANSION_STATES = ("overexpanded", "ideally expanded", "underexpanded")   # the order of every figure


# ===================================================================== thrust and specific impulse
def thrust_parts(mdot, Ve, pe, pa, Ae):
    """The two parts of rocket thrust (N): momentum thrust mdot V_e and pressure thrust (p_e - p_a) A_e.
    Example: thrust_parts(470.0, 4400.0, 15000.0, 101325.0, 4.17) -> (2,068,000, -360,000)"""
    return mdot * Ve, (pe - pa) * Ae


def thrust(mdot, Ve, pe, pa, Ae):
    """Rocket thrust F = mdot V_e + (p_e - p_a) A_e (N). Pressures in Pa, never kPa.
    Example: thrust(470.0, 4400.0, 15000.0, 101325.0, 4.17) -> 1,708,000"""
    m, p = thrust_parts(mdot, Ve, pe, pa, Ae)
    return m + p


def air_breathing_thrust(mdot, Ve, V_inf, pe, p_inf, Ae):
    """Thrust of an engine that breathes air (N): F = mdot (V_e - V_inf) + (p_e - p_inf) A_e, with
    mdot the air flow and the fuel flow neglected. Example: air_breathing_thrust(40.0, 1300.0, 700.0, 11000.0, 11000.0, 0.5) -> 24,000"""
    return mdot * (Ve - V_inf) + (pe - p_inf) * Ae


def effective_exhaust_velocity(mdot, Ve, pe, pa, Ae):
    """Effective exhaust velocity c = V_e + (p_e - p_a) A_e / mdot (m/s), so that F = mdot c.
    Example: effective_exhaust_velocity(470.0, 4400.0, 15000.0, 101325.0, 4.17) -> 3,634"""
    return Ve + (pe - pa) * Ae / mdot


def isp_from_c(c):
    """Specific impulse I_sp = c / g0 (s), with g0 = 9.81 m/s^2. Example: isp_from_c(3168.6) -> 323.0"""
    return c / G0


def c_from_isp(isp):
    """Effective exhaust velocity c = I_sp g0 (m/s). Example: c_from_isp(323.0) -> 3,169"""
    return isp * G0


def isp_from_thrust(F, mdot):
    """I_sp = F / (mdot g0) (s). Example: isp_from_thrust(1.668e6, 468.2) -> 363.2"""
    return F / (mdot * G0)


def mass_flow(F, isp):
    """Propellant mass flow mdot = F / (I_sp g0) (kg/s). Example: mass_flow(1.668e6, 363.2) -> 468.2"""
    return F / (isp * G0)


def expansion_state(pe, pa, rtol=1e-3):
    """The state of expansion from the exit and ambient pressures: "overexpanded" (p_e < p_a: the
    nozzle expanded the gas below the outside pressure), "ideally expanded" (p_e = p_a within
    rtol) or "underexpanded" (p_e > p_a). Example: expansion_state(15000.0, 101325.0) -> "overexpanded" """
    if abs(pe - pa) <= rtol * max(abs(pa), abs(pe)):
        return "ideally expanded"
    return "overexpanded" if pe < pa else "underexpanded"


def exit_area_from_thrusts(F_sl, F_vac, p_sl=P_SL):
    """Exit area (m^2) of a fixed nozzle from its published sea-level and vacuum thrust at one flow:
    F_vac - F_sl = p_sl A_e. Example: exit_area_from_thrusts(1.668e6, 2.0907e6) -> 4.171"""
    return (F_vac - F_sl) / p_sl


def diameter_from_area(A):
    """Diameter (m) of a circle of area A (m^2). Example: diameter_from_area(4.171) -> 2.304"""
    return math.sqrt(4.0 * A / math.pi)


def area_from_diameter(D):
    """Area (m^2) of a circle of diameter D (m). Example: area_from_diameter(2.304) -> 4.169"""
    return 0.25 * math.pi * D * D


def ambient_pressure(h):
    """Ambient pressure (Pa) at altitude h (m) in page 1.4's standard atmosphere (scalar or array;
    0 to 59.5 km). Example: ambient_pressure(15000.0) -> 12,032"""
    return standard(h)[1]


def fixed_nozzle_thrust(F_vac, Ae, h):
    """Thrust (N) of an engine with a fixed nozzle at altitude h (m), at the flow of its vacuum
    rating: F = F_vac - p_a(h) A_e (the momentum part and p_e do not change with altitude).
    Example: fixed_nozzle_thrust(2.0907e6, 4.171, 15000.0) -> 2,041,000"""
    return F_vac - ambient_pressure(h) * Ae


def fixed_nozzle_isp(F_vac, Ae, mdot, h):
    """Specific impulse (s) of that engine at altitude h (m): F(h) / (mdot g0).
    Example: fixed_nozzle_isp(2.0907e6, 4.171, 468.2, 0.0) -> 363.2"""
    return fixed_nozzle_thrust(F_vac, Ae, h) / (mdot * G0)


# ===================================================================== the rocket equation
class StageLimitError(ValueError):
    """Raised when a stage cannot give the delta-V asked of it: f_inert e^(dV/c) >= 1."""


def delta_v(c, mi, mf):
    """Ideal delta-V (m/s): dV = c ln(m_i / m_f). Example: delta_v(3168.63, 8531.0, 2902.0) -> 3,416"""
    return c * math.log(mi / mf)


def mass_ratio(dv, c):
    """Mass ratio m_i / m_f = e^(dV / c). Example: mass_ratio(3416.0, 3168.63) -> 2.939"""
    return math.exp(dv / c)


def propellant_share(dv, c):
    """Share of the initial mass burned as propellant: 1 - e^(-dV / c) (m_prop / m_i).
    Example: propellant_share(3168.63, 3168.63) -> 0.6321"""
    return 1.0 - math.exp(-dv / c)


def final_mass(mi, dv, c):
    """Final mass m_f = m_i e^(-dV / c) (kg). Example: final_mass(8531.0, 3416.0, 3168.63) -> 2,902"""
    return mi * math.exp(-dv / c)


def inert_mass_fraction(m_inert, m_prop):
    """f_inert = m_inert / (m_inert + m_prop): over the stage's own loaded mass, never over m_i.
    Example: inert_mass_fraction(14700.0, 170000.0) -> 0.07959"""
    return m_inert / (m_inert + m_prop)


def inert_from_prop(m_prop, f_inert):
    """Inert mass m_inert = f_inert m_prop / (1 - f_inert) (kg). Example: inert_from_prop(5629.0, 0.17) -> 1,153"""
    return f_inert * m_prop / (1.0 - f_inert)


def stage_factor(dv, c, f_inert):
    """The factor m_i / m_pay of one stage: e^x (1 - f) / (1 - f e^x), x = dV / c. Raises
    StageLimitError past the stage's limit. Example: stage_factor(3416.0, 3168.63, 0.17) -> 4.875"""
    e = math.exp(dv / c)
    den = 1.0 - f_inert * e
    if den <= 0.0:
        raise StageLimitError(f"a stage with f_inert = {f_inert:g} and c = {c:g} m/s cannot give {dv:g} m/s: "
                              f"f_inert e^(dV/c) = {f_inert * e:.4f} >= 1 (limit {single_stage_limit(c, f_inert):.1f} m/s)")
    return e * (1.0 - f_inert) / den


def size_stage(m_pay, dv, c=None, f_inert=None, isp=None):
    """Size one stage for a payload, a delta-V and an inert mass fraction (give c in m/s or isp in s).
    Returns a dict: x = dV/c, exp = e^x (the mass ratio), m_prop = m_pay (e^x - 1)(1 - f)/(1 - f e^x),
    m_inert = f m_prop / (1 - f), m_f = m_pay + m_inert, m_i = m_f + m_prop, numerator, denominator
    (of m_prop), payload_fraction = m_pay / m_i, c, f_inert, m_pay, dv. Raises StageLimitError when
    f e^x >= 1 (no payload can be carried). Example: size_stage(1750.0, 3416.0, isp=323.0, f_inert=0.17)["m_i"] -> 8,531"""
    if c is None:
        c = c_from_isp(isp)
    if f_inert is None or not 0.0 < f_inert < 1.0:
        raise ValueError(f"f_inert must be between 0 and 1, got {f_inert!r}")
    x = dv / c
    e = math.exp(x)
    num = m_pay * (e - 1.0) * (1.0 - f_inert)
    den = 1.0 - f_inert * e
    if den <= 0.0:
        stage_factor(dv, c, f_inert)                      # raises with the message
    m_prop = num / den
    m_inert = inert_from_prop(m_prop, f_inert)
    m_f = m_pay + m_inert
    m_i = m_f + m_prop
    return dict(x=x, exp=e, numerator=num, denominator=den, m_prop=m_prop, m_inert=m_inert, m_f=m_f, m_i=m_i,
                payload_fraction=m_pay / m_i, c=c, f_inert=f_inert, m_pay=m_pay, dv=dv)


def single_stage_limit(c, f_inert):
    """The largest delta-V of one stage, reached with no payload at all: c ln(1 / f_inert) (m/s).
    Example: single_stage_limit(3168.63, 0.17) -> 5,615"""
    return c * math.log(1.0 / f_inert)


def stage_delta_v(c, m_inert, m_prop, m_pay=0.0):
    """Ideal delta-V (m/s) of a real stage from its masses: c ln((m_pay + m_inert + m_prop) / (m_pay + m_inert)).
    Example: stage_delta_v(c_from_isp(432.0), 14700.0, 170000.0) -> 10,726"""
    return delta_v(c, m_pay + m_inert + m_prop, m_pay + m_inert)


def gravity_loss_constant_angle(t_b, gamma_deg, g=G0):
    """Gravity loss (m/s) of a burn of t_b seconds flown at a constant flight-path angle gamma (deg):
    g t_b sin(gamma), the integral of g sin(gamma) dt when gamma does not change.
    Example: gravity_loss_constant_angle(150.0, 40.0) -> 945.9"""
    return g * t_b * math.sin(math.radians(gamma_deg))


# ===================================================================== unit checks
if __name__ == "__main__":
    def close(a, b, tol, what):
        assert abs(a - b) <= tol * max(1.0, abs(b)), f"{what}: {a!r} vs {b!r}"

    assert G0 == 9.81
    # thrust: parts add up; c and I_sp both ways; units Pa x m^2 = N
    m, p = thrust_parts(470.0, 4400.0, 15000.0, P_SL, 4.17)
    close(m + p, thrust(470.0, 4400.0, 15000.0, P_SL, 4.17), 1e-12, "thrust = momentum + pressure")
    c = effective_exhaust_velocity(470.0, 4400.0, 15000.0, P_SL, 4.17)
    close(470.0 * c, m + p, 1e-12, "F = mdot c")
    close(c_from_isp(isp_from_c(c)), c, 1e-12, "c -> I_sp -> c")
    close(isp_from_thrust(m + p, 470.0), c / G0, 1e-12, "I_sp = F / (mdot g0)")
    close(mass_flow(m + p, c / G0), 470.0, 1e-12, "mdot from F and I_sp")
    # the air-breathing form is the rocket form with the incoming momentum taken away
    close(air_breathing_thrust(40.0, 1300.0, 700.0, 11000.0, 11000.0, 0.5), 40.0 * 600.0, 1e-12, "air-breathing")
    close(air_breathing_thrust(40.0, 1300.0, 0.0, 9000.0, 11000.0, 0.5), thrust(40.0, 1300.0, 9000.0, 11000.0, 0.5),
          1e-12, "air-breathing with V_inf = 0 is the rocket form")
    # expansion states, in the chapter's order and from the sign of p_e - p_a
    assert expansion_state(15000.0, P_SL) == EXPANSION_STATES[0]
    assert expansion_state(P_SL, P_SL) == EXPANSION_STATES[1]
    assert expansion_state(2 * P_SL, P_SL) == EXPANSION_STATES[2]
    # a fixed nozzle: sea-level and vacuum thrust come back from the exit area; thrust rises with altitude
    A = exit_area_from_thrusts(1.668e6, 2.0907e6)
    close(fixed_nozzle_thrust(2.0907e6, A, 0.0), 1.668e6, 1e-9, "fixed nozzle at sea level")
    hs = np.linspace(0.0, H_TOP, 60)
    assert np.all(np.diff(fixed_nozzle_thrust(2.0907e6, A, hs)) > 0), "thrust rises with altitude"
    close(diameter_from_area(area_from_diameter(2.3)), 2.3, 1e-12, "area <-> diameter")
    # rocket equation: dV = c gives 63% propellant; 2c gives 86%
    close(propellant_share(1.0, 1.0), 1.0 - math.exp(-1.0), 1e-12, "dV = c")
    assert f"{propellant_share(2.0, 1.0):.2f}" == "0.86" and f"{propellant_share(1.0, 1.0):.2f}" == "0.63"
    # stage sizing round trip: the sized stage's m_i / m_f gives back the delta-V
    s = size_stage(1750.0, 3416.0, isp=323.0, f_inert=0.17)
    close(delta_v(s["c"], s["m_i"], s["m_f"]), 3416.0, 1e-12, "sized stage gives back its delta-V")
    close(s["m_inert"] / (s["m_inert"] + s["m_prop"]), 0.17, 1e-12, "f_inert of the sized stage")
    close(s["m_i"], 1750.0 * stage_factor(3416.0, s["c"], 0.17), 1e-12, "m_i = m_pay x stage factor")
    close(stage_delta_v(s["c"], s["m_inert"], s["m_prop"], 1750.0), 3416.0, 1e-12, "stage_delta_v")
    # the stage formula against the long way: masses added one by one until m_i/m_f = e^x
    m_prop = 0.0
    for _ in range(200):                                   # fixed point: m_prop = m_f (e^x - 1)
        m_f = 1750.0 + inert_from_prop(m_prop, 0.17)
        m_prop = m_f * (math.exp(3416.0 / s["c"]) - 1.0)
    close(m_prop, s["m_prop"], 1e-9, "stage formula = iteration")
    # the limit: at c ln(1/f) the payload fraction is zero; past it, a clear error
    lim = single_stage_limit(s["c"], 0.17)
    close(stage_factor(lim * (1 - 1e-9), s["c"], 0.17) > 1e6, True, 0, "factor blows up at the limit")
    try:
        size_stage(1750.0, lim * 1.01, c=s["c"], f_inert=0.17)
        raise SystemExit("size_stage did not stop past the limit")
    except StageLimitError:
        pass
    close(gravity_loss_constant_angle(100.0, 90.0), 981.0, 1e-12, "vertical burn loses g t_b")
    print("rocket.py: all unit checks passed")
