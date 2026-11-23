"""Continuity, Bernoulli and the pitot-static tube (1.5 Bernoulli and Pitot Static). SI units:
m, m^2, m/s, Pa, kg/m^3, kg/s, m^3/s.

The equations are those of the page:
mdot = rho A V, A1 V1 = A2 V2, Q = A V, p1 + rho V1^2/2 + rho g z1 = p2 + rho V2^2/2 + rho g z2,
delta p = rho g h, A = pi D^2/4; and the pitot-static airspeed V = sqrt(2 (p0 - p)/rho), which
is Bernoulli's equation between the free stream and the stagnation point (incompressible flow).

Run this file for its unit checks:  python3 -B scripts/chapter_1/flow.py
"""
import math
import sys as _sys
from pathlib import Path as _Path

import numpy as np

if __name__ == "__main__":
    _sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from chapter_1.atmosphere import G0 as G  # noqa: E402  (9.81 m/s^2, the value used throughout the course)
RHO_WATER = 1000.0         # kg/m^3, water
RHO_AIR_SL = 1.2250        # kg/m^3, sea-level standard air (atmosphere.RHO_SL)
V_INCOMPRESSIBLE = 100.0   # m/s, below about this airspeed air may be treated as incompressible


def area_circle(D):
    """Area of a circle of diameter D: pi D^2 / 4. Example: area_circle(0.1) -> 0.007854"""
    return math.pi * np.asarray(D, dtype=float) ** 2 / 4.0


def mass_flow(rho, A, V):
    """Mass flow rate rho A V, kg/s. Example: mass_flow(1.225, 0.5, 40.0) -> 24.50"""
    return rho * A * V


def volume_flow(A, V):
    """Volume flow rate Q = A V, m^3/s. Example: volume_flow(0.002, 3.0) -> 0.006000"""
    return A * V


def continuity_speed(V1, A1, A2, rho1=1.0, rho2=1.0):
    """Speed at station 2 from rho1 A1 V1 = rho2 A2 V2 (incompressible when rho1 = rho2).
    Example: continuity_speed(10.0, 0.04, 0.01) -> 40.00"""
    return rho1 * A1 * V1 / (rho2 * A2)


def bernoulli_p2(p1, V1, V2, rho, z1=0.0, z2=0.0, g=G):
    """Pressure at station 2 on the same streamline: p2 = p1 + rho (V1^2 - V2^2)/2 + rho g (z1 - z2).
    Example: bernoulli_p2(101325.0, 10.0, 40.0, 1.225) -> 100,406"""
    return p1 + 0.5 * rho * (V1 ** 2 - V2 ** 2) + rho * g * (z1 - z2)


def bernoulli_V2(p1, p2, V1, rho, z1=0.0, z2=0.0, g=G):
    """Speed at station 2 from Bernoulli: V2 = sqrt(V1^2 + 2 (p1 - p2)/rho + 2 g (z1 - z2)).
    Example: bernoulli_V2(101325.0, 100406.25, 10.0, 1.225) -> 40.00"""
    return math.sqrt(V1 ** 2 + 2.0 * (p1 - p2) / rho + 2.0 * g * (z1 - z2))


def dynamic_pressure(rho, V):
    """Dynamic pressure q = rho V^2 / 2, Pa. Example: dynamic_pressure(1.225, 100.0) -> 6,125"""
    return 0.5 * rho * np.asarray(V, dtype=float) ** 2


def venturi_speed(dp, rho, A1, A2):
    """Speed V1 at the inlet of a venturi (or a contraction) from the pressure drop dp = p1 - p2
    between inlet area A1 and throat area A2 (continuity plus Bernoulli, no height change):
    V1 = sqrt(2 dp / (rho ((A1/A2)^2 - 1))). Example: venturi_speed(918.75, 1.225, 0.04, 0.01) -> 10.00"""
    return math.sqrt(2.0 * dp / (rho * ((A1 / A2) ** 2 - 1.0)))


def manometer_dp(h, rho_fluid=RHO_WATER, g=G):
    """Pressure difference shown by a manometer column h (m) of a fluid of density rho_fluid:
    delta p = rho g h, Pa. Example: manometer_dp(0.05) -> 490.5"""
    return rho_fluid * g * h


def manometer_height(dp, rho_fluid=RHO_WATER, g=G):
    """Column height (m) for a pressure difference dp (Pa): h = dp / (rho g). Example: manometer_height(490.5) -> 0.05000"""
    return dp / (rho_fluid * g)


def pitot_speed(p0, p, rho):
    """Airspeed from a pitot-static tube, incompressible: V = sqrt(2 (p0 - p) / rho), m/s, with
    p0 the total (pitot) pressure and p the static pressure. Example: pitot_speed(107450.0, 101325.0, 1.225) -> 100.0"""
    return math.sqrt(2.0 * (p0 - p) / rho)


def draining_speed(z, g=G):
    """Speed of a jet leaving a large open tank through a hole z (m) below the free surface
    (Bernoulli from the surface to the jet, both at atmospheric pressure): V = sqrt(2 g z).
    Example: draining_speed(1.0) -> 4.429"""
    return math.sqrt(2.0 * g * z)


# ===================================================================== unit checks
def _close(a, b, rtol, what):
    assert abs(a - b) <= rtol * max(abs(b), 1e-300), f"{what}: {a!r} vs {b!r}"


if __name__ == "__main__":
    # Closed forms the equations must reproduce
    _close(float(area_circle(0.1)), 0.00785398, 1e-6, "area of a 10 cm circle")
    V2 = continuity_speed(10.0, 0.04, 0.01)
    _close(V2, 40.0, 1e-12, "area ratio 4 gives four times the speed")
    p2 = bernoulli_p2(101325.0, 10.0, V2, 1.225)
    _close(p2, 101325.0 - 0.5 * 1.225 * (1600.0 - 100.0), 1e-12, "Bernoulli pressure drop")
    _close(bernoulli_V2(101325.0, p2, 10.0, 1.225), V2, 1e-12, "Bernoulli round trip")
    _close(venturi_speed(101325.0 - p2, 1.225, 0.04, 0.01), 10.0, 1e-12, "venturi round trip")
    # total pressure is constant along the streamline
    _close(p2 + float(dynamic_pressure(1.225, V2)), 101325.0 + float(dynamic_pressure(1.225, 10.0)), 1e-12, "p0 const")
    # height term: still water, 10 m deeper is 98.1 kPa more
    _close(bernoulli_p2(101325.0, 0.0, 0.0, RHO_WATER, z1=0.0, z2=-10.0) - 101325.0, 98100.0, 1e-12, "hydrostatic")
    _close(manometer_height(manometer_dp(0.123)), 0.123, 1e-12, "manometer round trip")
    _close(pitot_speed(101325.0 + float(dynamic_pressure(1.225, 100.0)), 101325.0, 1.225), 100.0, 1e-12, "pitot")
    _close(draining_speed(1.0), 4.42945, 1e-5, "Torricelli, 1 m head")
    _close(mass_flow(1.225, 0.5, 40.0), 24.5, 1e-12, "mass flow")
    # a water manometer reading of 1 inch (25.4 mm) is about 249 Pa (with g = 9.81: 249.2 Pa)
    _close(manometer_dp(0.0254), 249.17, 1e-4, "inch of water")
    print("flow.py: all unit checks passed")
