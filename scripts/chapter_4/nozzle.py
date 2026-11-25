"""The ideal rocket nozzle (page 4.1 states these results and shows them as computed figures; it never
derives them). Steady, one-dimensional, isentropic flow of a perfect gas with a constant ratio of
specific heats `g` (the pages say "ratio of specific heats" in words: gamma is the flight-path angle
in this book). SI units: Pa, K, kg/kmol, m/s; areas as ratios to the throat area.

Sources (each opened; equation numbers as printed):
  - NASA SP-125: Huzel, D. K., and Huang, D. H., Design of Liquid Propellant Rocket Engines
    (NASA, 1967), Section 1.2: Eq. (1-16) critical pressure ratio, p. 6; Eq. (1-18) exit velocity
    from the chamber temperature, the molecular mass and the pressure ratio, p. 7 (with R = 1544/M
    of Table 1-1, written here with the universal gas constant); Eq. (1-20) area ratio against the
    pressure ratio, p. 7; Eq. (1-23) area ratio against the Mach number, p. 7; Eq. (1-32)
    characteristic velocity, p. 12; Eqs. (1-33) and (1-33a) thrust coefficient, p. 12; Eq. (1-31c)
    I_s = c* C_F / g, p. 12. Sample Calculation 1-3, p. 17 (the unit check below). Section 4.3,
    Figure 4-13 and Eq. (4-7): the parabolic approximation of a bell nozzle and the length of an
    "80-percent bell", pp. 90 and 91; Figure 4-14, the parabola's wall angles against area ratio.
  - NACA Report 1135, Ames Research Staff, Equations, Tables, and Charts for Compressible Flow
    (1953): Eq. (43) temperature ratio and Eq. (44) pressure ratio against Mach number, p. 616;
    Table II (ratio of specific heats 7/5), pp. 634 and 635 (the unit checks below).
  - Flow separation: NASA SP-8120, Liquid Rocket Engine Nozzles (1976), p. 17: "an early rule
    stated that a danger of separation existed when the ratio of exit pressure to ambient pressure
    was equal to 0.4"; NASA TM X-64890, Schmucker (1974), p. 1, names this the Summerfield
    criterion (Summerfield, Foster and Swan, 1954). A curve drawn past it is stopped there.

Run this file for its unit checks:  python3 -B scripts/chapter_4/nozzle.py
"""
import math
import sys
from pathlib import Path

import numpy as np

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chapter_1.atmosphere import G0, UNIVERSAL_R  # noqa: E402

__all__ = ["SEPARATION_PE_PA", "BELL_80_ANGLES", "area_ratio_from_mach", "mach_from_area_ratio", "pressure_ratio",
           "temperature_ratio", "critical_pressure_ratio", "area_ratio_from_pressure_ratio",
           "pressure_ratio_from_area_ratio", "exit_velocity", "characteristic_velocity", "thrust_coefficient",
           "ideal_isp", "ideal_area_ratio", "separation_area_ratio", "matching_gamma", "nozzle_flow", "bell_angles", "bell_length"]

SEPARATION_PE_PA = 0.4     # SP-8120, p. 17; TM X-64890, p. 1 (the Summerfield criterion): flow separates near p_e = 0.4 p_a

# NASA SP-125, Figure 4-14, the 80-percent bell: initial and final parabola angles (deg) against area
# ratio, read from the chart (about +/- 1 deg; the chart's range is 5 to 50), and the book's own
# reading at an area ratio of 14 (27.4 and 9.8 deg, Section 4.3 design example).
BELL_80_ANGLES = [(5.0, 21.5, 14.0), (10.0, 25.5, 11.0), (14.0, 27.4, 9.8), (20.0, 29.0, 9.0), (30.0, 31.0, 8.5),
                  (40.0, 32.0, 8.0), (50.0, 33.0, 7.5)]


# ===================================================================== isentropic relations
def area_ratio_from_mach(M, g):
    """A / A_t at Mach number M (SP-125 Eq. 1-23). Example: area_ratio_from_mach(2.0, 1.4) -> 1.688"""
    M = np.asarray(M, dtype=float)
    return (1.0 / M) * ((2.0 / (g + 1.0)) * (1.0 + 0.5 * (g - 1.0) * M * M)) ** ((g + 1.0) / (2.0 * (g - 1.0)))


def mach_from_area_ratio(eps, g, supersonic=True):
    """Mach number where A / A_t = eps (>= 1), on the supersonic branch (after the throat) or the
    subsonic one (before it): the area-Mach relation solved numerically by bisection.
    Example: mach_from_area_ratio(1.688, 1.4) -> 2.000"""
    eps = float(eps)
    if eps < 1.0 - 1e-12:
        raise ValueError(f"area ratio {eps} below 1")
    if abs(eps - 1.0) < 1e-12:
        return 1.0
    lo, hi = (1.0, 2.0) if supersonic else (1e-9, 1.0)
    if supersonic:
        while area_ratio_from_mach(hi, g) < eps:
            hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = area_ratio_from_mach(mid, g) - eps
        if (f > 0) == supersonic:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def pressure_ratio(M, g):
    """p / p_c at Mach number M for a chamber at rest (NACA 1135 Eq. 44). Example: pressure_ratio(2.0, 1.4) -> 0.1278"""
    M = np.asarray(M, dtype=float)
    return (1.0 + 0.5 * (g - 1.0) * M * M) ** (-g / (g - 1.0))


def temperature_ratio(M, g):
    """T / T_c at Mach number M (NACA 1135 Eq. 43). Example: temperature_ratio(1.0, 1.2) -> 0.9091"""
    M = np.asarray(M, dtype=float)
    return 1.0 / (1.0 + 0.5 * (g - 1.0) * M * M)


def critical_pressure_ratio(g):
    """p_t / p_c at the throat, [2/(g+1)]^(g/(g-1)) (SP-125 Eq. 1-16). Example: critical_pressure_ratio(1.2) -> 0.5645"""
    return (2.0 / (g + 1.0)) ** (g / (g - 1.0))


def area_ratio_from_pressure_ratio(pe_pc, g):
    """Area ratio A_e / A_t that expands the gas to p_e / p_c (SP-125 Eq. 1-20).
    Example: area_ratio_from_pressure_ratio(0.00985, 1.2) -> 12.0"""
    r = np.asarray(pe_pc, dtype=float)
    num = (2.0 / (g + 1.0)) ** (1.0 / (g - 1.0)) * r ** (-1.0 / g)
    den = np.sqrt((g + 1.0) / (g - 1.0) * (1.0 - r ** ((g - 1.0) / g)))
    return num / den


def pressure_ratio_from_area_ratio(eps, g):
    """p_e / p_c of an ideal nozzle of area ratio eps (the supersonic exit). Example:
    pressure_ratio_from_area_ratio(12.0, 1.2) -> 0.009853"""
    return float(pressure_ratio(mach_from_area_ratio(eps, g), g))


def exit_velocity(Tc, molar_mass, pe_pc, g):
    """Exit velocity V_e (m/s) of the ideal nozzle: sqrt(2 g/(g-1) (R_u/M) T_c [1 - (p_e/p_c)^((g-1)/g)])
    (SP-125 Eq. 1-18), R_u = 8,314.5 J/(kmol K). Example: exit_velocity(3000.0, 22.0, 0.001, 1.2) -> 3,174"""
    R = UNIVERSAL_R / molar_mass
    return math.sqrt(2.0 * g / (g - 1.0) * R * Tc * (1.0 - pe_pc ** ((g - 1.0) / g)))


def characteristic_velocity(Tc, molar_mass, g):
    """Characteristic velocity c* (m/s), a property of the propellants and their combustion:
    sqrt(g R T_c) / (g sqrt[(2/(g+1))^((g+1)/(g-1))]) (SP-125 Eq. 1-32).
    Example: characteristic_velocity(3000.0, 22.0, 1.2) -> 1,688"""
    R = UNIVERSAL_R / molar_mass
    return math.sqrt(g * R * Tc) / (g * math.sqrt((2.0 / (g + 1.0)) ** ((g + 1.0) / (g - 1.0))))


def thrust_coefficient(eps, g, pc, pa):
    """Thrust coefficient C_F = F / (p_c A_t) of the ideal nozzle of area ratio eps at ambient pressure pa
    (SP-125 Eq. 1-33a). pa = 0 in vacuum. Example: thrust_coefficient(12.0, 1.2, 1000.0, 14.7) -> 1.592"""
    pe_pc = pressure_ratio_from_area_ratio(eps, g)
    mom = math.sqrt(2.0 * g * g / (g - 1.0) * (2.0 / (g + 1.0)) ** ((g + 1.0) / (g - 1.0))
                    * (1.0 - pe_pc ** ((g - 1.0) / g)))
    return mom + eps * (pe_pc - pa / pc)


def ideal_isp(eps, g, pc, pa, cstar):
    """Specific impulse (s) of the ideal nozzle: c* C_F / g0 (SP-125 Eq. 1-31c), g0 = 9.81 m/s^2.
    Example: ideal_isp(12.0, 1.2, 6.895e6, 101325.0, 1800.0) -> 292.1"""
    return cstar * thrust_coefficient(eps, g, pc, pa) / G0


def ideal_area_ratio(pc, pa, g):
    """The area ratio that expands the gas exactly to the ambient pressure (p_e = p_a): the best nozzle
    at that ambient pressure. Example: ideal_area_ratio(6.895e6, 101325.0, 1.2) -> 8.6"""
    return float(area_ratio_from_pressure_ratio(pa / pc, g))


def separation_area_ratio(pc, pa, g, limit=SEPARATION_PE_PA):
    """The area ratio at which p_e falls to `limit` x p_a (0.4: the Summerfield criterion): past it, the
    flow separates from the nozzle wall and the ideal model no longer holds.
    Example: separation_area_ratio(6.895e6, 101325.0, 1.2) -> 18"""
    return float(area_ratio_from_pressure_ratio(limit * pa / pc, g))


def matching_gamma(cf, pc, pa, lo=1.05, hi=1.40):
    """The ratio of specific heats for which the ideal nozzle, expanded to p_e = p_a, gives the thrust
    coefficient `cf` of a published table (an effective value that stands in for shifting equilibrium,
    so a computed curve passes through the table's point). Bisection. Example: matching_gamma(1.632, 1000.0, 14.7) -> 1.143"""
    def f(g):
        return thrust_coefficient(ideal_area_ratio(pc, pa, g), g, pc, pa) - cf
    if f(lo) * f(hi) > 0:
        raise ValueError(f"no ratio of specific heats between {lo} and {hi} gives C_F = {cf}")
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def nozzle_flow(area, throat_index, g, Tc, molar_mass):
    """Mach number, p/p_c, T/T_c and speed V (m/s) along a nozzle whose area ratio A/A_t is given at a
    series of stations `area` (1 at the throat): subsonic before the station throat_index, supersonic
    after it. Returns a dict of arrays: M, p, T, V. Example: nozzle_flow(A_over_At, i_throat, 1.2, 3000.0, 22.0)"""
    area = np.asarray(area, dtype=float)
    M = np.array([mach_from_area_ratio(max(a, 1.0), g, supersonic=(i > throat_index))
                  for i, a in enumerate(area)])
    M[throat_index] = 1.0
    T = temperature_ratio(M, g)
    p = pressure_ratio(M, g)
    V = M * np.sqrt(g * UNIVERSAL_R / molar_mass * Tc * T)
    return dict(M=M, p=p, T=T, V=V)


# ===================================================================== bell geometry
def bell_angles(eps):
    """Initial and final wall angles (deg) of an 80-percent parabolic bell at area ratio eps, interpolated
    in SP-125 Figure 4-14 (held at the chart's end values outside 5 to 50). Example: bell_angles(14.0) -> (27.4, 9.8)"""
    e, tn, te = np.array(BELL_80_ANGLES).T
    x = min(max(eps, e[0]), e[-1])
    return float(np.interp(x, e, tn)), float(np.interp(x, e, te))


def bell_length(r_t, eps, fraction=0.8):
    """Throat-to-exit length of a bell nozzle, `fraction` of the 15-deg cone with the same throat, throat
    radius of curvature 0.382 r_t and area ratio (SP-125 Eq. 4-7).
    Example: bell_length(1.0, 14.0) -> 8.226"""
    return fraction * (r_t * (math.sqrt(eps) - 1.0) + 0.382 * r_t * (1.0 / math.cos(math.radians(15.0)) - 1.0)) \
        / math.tan(math.radians(15.0))


# ===================================================================== unit checks
if __name__ == "__main__":
    def close(a, b, tol, what):
        assert abs(a - b) <= tol * abs(b), f"{what}: {a!r} vs {b!r} (relative {tol})"

    # NACA 1135, Table II, ratio of specific heats 7/5: M = 2 (p. 634) and M = 3 (p. 635)
    close(float(area_ratio_from_mach(2.0, 1.4)), 1.688, 3e-4, "A/A* at M = 2")
    close(float(pressure_ratio(2.0, 1.4)), 0.1278, 4e-4, "p/pt at M = 2")
    close(float(area_ratio_from_mach(3.0, 1.4)), 4.235, 2e-4, "A/A* at M = 3")
    close(float(pressure_ratio(3.0, 1.4)), 0.02722, 2e-4, "p/pt at M = 3")
    close(mach_from_area_ratio(4.235, 1.4), 3.0, 1e-3, "M from A/A* (supersonic)")
    assert mach_from_area_ratio(4.235, 1.4, supersonic=False) < 0.2, "subsonic branch"
    # SP-125 Sample Calculation 1-3, p. 17: ratio of specific heats 1.20, area ratio 12, chamber 1000 psia,
    # exit 9.85 psia; thrust coefficient 1.5918 at sea level (14.7 psia) and 1.7682 in space
    close(pressure_ratio_from_area_ratio(12.0, 1.2) * 1000.0, 9.85, 2e-3, "p_e of the area ratio 12")
    close(float(area_ratio_from_pressure_ratio(0.00985, 1.2)), 12.0, 2e-3, "area ratio of p_e/p_c")
    # (the book rounds its momentum term, 2.247 x 0.734, to 1.65: hence 0.3 percent)
    close(thrust_coefficient(12.0, 1.2, 1000.0, 14.7), 1.5918, 3e-3, "C_F at sea level")
    close(thrust_coefficient(12.0, 1.2, 1000.0, 0.0), 1.7682, 3e-3, "C_F in vacuum")
    # the two forms of the exit velocity agree: V_e = M a at the exit
    eps, g, Tc, Mw = 16.0, 1.2, 3000.0, 22.0
    fl = nozzle_flow(np.array([3.0, 1.0, eps]), 1, g, Tc, Mw)
    close(float(fl["V"][-1]), exit_velocity(Tc, Mw, float(fl["p"][-1]), g), 1e-9, "V_e two ways")
    close(float(fl["p"][1]), critical_pressure_ratio(g), 1e-12, "throat pressure")
    # thrust is highest over area ratio where p_e = p_a (fixed chamber, numerical maximum)
    pc, pa = 6.895e6, 101325.0
    eps_grid = np.linspace(2.0, 30.0, 5601)
    cf = np.array([thrust_coefficient(e, g, pc, pa) for e in eps_grid])
    close(float(eps_grid[np.argmax(cf)]), ideal_area_ratio(pc, pa, g), 2e-3, "best area ratio at p_e = p_a")
    assert separation_area_ratio(pc, pa, g) > ideal_area_ratio(pc, pa, g)
    # in vacuum a larger nozzle always helps
    cfv = np.array([thrust_coefficient(e, g, pc, 0.0) for e in eps_grid])
    assert np.all(np.diff(cfv) > 0)
    # c* C_F / g0 is the specific impulse (SP-125 Eq. 1-31c), and C_F = F/(p_c A_t) is the same number
    close(ideal_isp(eps, g, pc, pa, 1800.0), 1800.0 * thrust_coefficient(eps, g, pc, pa) / G0, 1e-12, "I_s = c* C_F / g")
    close(bell_angles(14.0)[0], 27.4, 1e-12, "SP-125 bell angles at 14")
    gm = matching_gamma(1.632, 1000.0, 14.7)              # SP-125 Table 1-9, LOX/RP-1 at 2.56: C_f 1.632
    close(thrust_coefficient(ideal_area_ratio(1000.0, 14.7, gm), gm, 1000.0, 14.7), 1.632, 1e-9, "matching gamma")
    print("nozzle.py: all unit checks passed")
