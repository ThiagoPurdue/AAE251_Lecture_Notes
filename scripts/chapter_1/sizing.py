"""First takeoff-weight estimate (1.6 Aircraft Sizing), in the units Raymer and the values of
these notes use: pounds (weight), nautical miles, feet, knots, hours; specific fuel consumption
C in 1/h (pounds of fuel per hour per pound of thrust).

The equations are those of the page:
  W0 = (W_crew + W_payload) / (1 - Wf/W0 - We/W0)
  We/W0 = A W0^C                         (historical fit, Raymer Table 3.1)
  cruise: Wi/W(i-1) = exp[-R C / (V L/D)]  (Breguet range equation)
  loiter: Wi/W(i-1) = exp[-E C / (L/D)]    (endurance equation)
  Wf/W0 = 1.06 (1 - Wx/W0)               (6% reserve and trapped fuel)

Sources:
  - Raymer, D. P., Aircraft Design: A Conceptual Approach, 4th ed., AIAA, 2006: Table 3.1
    (empty-weight fraction fits, A and C for W0 in lb, and A for W0 in kg) and the historical
    mission-segment weight fractions of Chapter 3 (warm-up and takeoff 0.970, climb 0.985,
    landing 0.995).
  - Unit conversions: chapter_1/constants.py.
  - Real aircraft (JET_WEIGHTS, SFC_TYPICAL, LD_TYPICAL, EMPTY_WEIGHT_RANGE): the sources are
    given beside each table below.

Run this file for its unit checks:  python3 -B scripts/chapter_1/sizing.py
"""
import math

import numpy as np

# ===================================================================== Raymer Table 3.1
# Empty-weight fraction We/W0 = A W0^C Kvs (Kvs = 1.04 for variable sweep, 1.00 for fixed
# sweep). A for W0 in pounds; A_METRIC for W0 in kilograms; C the same for both.
EMPTY_WEIGHT_FIT = {          # class: (A, A_metric, C)
    "Sailplane, unpowered": (0.86, 0.83, -0.05),
    "Sailplane, powered": (0.91, 0.88, -0.05),
    "Homebuilt, metal or wood": (1.19, 1.11, -0.09),
    "Homebuilt, composite": (1.15, 1.07, -0.09),
    "General aviation, single engine": (2.36, 2.05, -0.18),
    "General aviation, twin engine": (1.51, 1.4, -0.10),
    "Agricultural aircraft": (0.74, 0.72, -0.03),
    "Twin turboprop": (0.96, 0.92, -0.05),
    "Flying boat": (1.09, 1.05, -0.05),
    "Jet trainer": (1.59, 1.47, -0.10),
    "Jet fighter": (2.34, 2.11, -0.13),
    "Military cargo or bomber": (0.93, 0.88, -0.07),
    "Jet transport": (1.02, 0.97, -0.06),
}
K_VS_VARIABLE = 1.04          # variable-sweep wing (Raymer Table 3.1)

# Historical segment weight fractions W_end/W_start (Raymer, Chapter 3)
SEGMENT_FRACTION = {"warm-up and takeoff": 0.970, "climb": 0.985, "landing": 0.995}
RESERVE_FACTOR = 1.06         # 6% reserve and trapped fuel: Wf/W0 = 1.06 (1 - Wx/W0)

# Empty-weight lines of Raymer Figure 3.1: the range of takeoff weights (lb) each class's line
# covers in the figure (read from the figure)
EMPTY_WEIGHT_RANGE = {
    "Sailplane, unpowered": (300.0, 1500.0),
    "Twin turboprop": (7000.0, 60000.0),
    "Jet fighter": (22000.0, 140000.0),
    "Jet transport": (25000.0, 1.0e6),
    "Military cargo or bomber": (30000.0, 1.0e6),
}

# ===================================================================== published data of real aircraft
# Jenkinson, Simpkin and Rhodes, Civil Jet Aircraft Design (Arnold/Butterworth-Heinemann, 1999),
# companion web site, "Data A: Aircraft Data File", Table 3 (Boeing aircraft): maximum takeoff,
# operational empty, design payload and design fuel load, kg (the last three add up to the
# maximum takeoff mass), and the wing aspect ratio.
JET_WEIGHTS = {
    "757-200": dict(mto=115900.0, oe=58040.0, payload=17670.0, fuel=40190.0, ar=7.82),
    "767-300ER": dict(mto=181437.0, oe=89902.0, payload=20520.0, fuel=71015.0, ar=7.99),
    "747-400": dict(mto=396830.0, oe=181484.0, payload=39140.0, fuel=176206.0, ar=7.39),
}
# Typical thrust-specific fuel consumption C of jet engines, 1/h, (cruise, loiter): Scholz,
# Aircraft Design lecture notes, Chapter 5 (HAW Hamburg), Table 5.7, based on Raymer (1989)
SFC_TYPICAL = [("Turbojet", 0.9, 0.8), ("Turbofan, low bypass ratio", 0.8, 0.7),
               ("Turbofan, high bypass ratio", 0.5, 0.4)]
# Typical maximum lift-to-drag ratios, rounded readings: Nicolai and Carichner, Fundamentals of
# Aircraft and Airship Design, Vol. 1 (AIAA, 2010), Figure 5.3; jet airliners from Scholz,
# Figure 5.7
LD_TYPICAL = [("Subsonic aircraft with a wing of aspect ratio 3 (a fighter)", "11"),
              ("Subsonic aircraft with a wing of aspect ratio 6", "16"),
              ("Jet airliners (aspect ratio about 7 to 10)", "15 to 21"),
              ("Subsonic aircraft with a wing of aspect ratio 10", "22"),
              ("Supersonic cruise aircraft at two to three times the speed of sound", "6 to 8")]

# ===================================================================== units (constants.py)
import sys as _sys                                       # noqa: E402
from pathlib import Path as _Path                        # noqa: E402
if str(_Path(__file__).resolve().parents[1]) not in _sys.path:   # run on its own: find the package
    _sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from chapter_1.constants import FT, NMI, NMI_FT, KT_FPS, LB_N, LB_KG, KG_LB  # noqa: E402,F401


def empty_weight_fraction(W0, cls="Jet transport", kvs=1.0, metric=False):
    """We/W0 = A W0^C Kvs from Raymer Table 3.1 for the class `cls` (a key of EMPTY_WEIGHT_FIT),
    W0 in lb (or in kg with metric=True). Example: empty_weight_fraction(100000.0) -> 0.5112"""
    A, Am, C = EMPTY_WEIGHT_FIT[cls]
    return (Am if metric else A) * np.asarray(W0, dtype=float) ** C * kvs


def cruise_fraction(R_nmi, C_per_h, V_kt, LD):
    """Breguet range equation solved for the cruise weight fraction:
    Wi/W(i-1) = exp[-R C / (V L/D)] with R in nmi, V in knots (nmi/h), C in 1/h.
    Example: cruise_fraction(1700.0, 0.55, 410.0, 13.0) -> 0.8391"""
    return math.exp(-R_nmi * C_per_h / (V_kt * LD))


def loiter_fraction(E_h, C_per_h, LD):
    """Endurance equation solved for the loiter weight fraction: Wi/W(i-1) = exp[-E C / (L/D)]
    with E in hours and C in 1/h. Example: loiter_fraction(1.25, 0.45, 13.0) -> 0.9577"""
    return math.exp(-E_h * C_per_h / LD)


def mission_fraction(fractions):
    """Wx/W0: the product of the segment fractions, in order (a list of numbers, or of
    (name, fraction) pairs). Example: mission_fraction([0.970, 0.985, 0.8391, 0.995]) -> 0.7977"""
    out = 1.0
    for f in fractions:
        out *= f[1] if isinstance(f, (tuple, list)) else f
    return out


def fuel_fraction(Wx_W0, reserve=RESERVE_FACTOR):
    """Wf/W0 = 1.06 (1 - Wx/W0). Example: fuel_fraction(0.7977) -> 0.2144"""
    return reserve * (1.0 - Wx_W0)


def size_takeoff_weight(W_crew, W_payload, Wf_W0, cls="Jet transport", guess=None, tol=1.0, kvs=1.0,
                        max_steps=200):
    """The sizing iteration: guess W0, compute We/W0 from the fit, compute a new
    W0 = (W_crew + W_payload) / (1 - Wf/W0 - We/W0), and repeat with the new value until two
    successive values differ by less than `tol` lb. The fuel fraction does not depend on W0 here
    (fixed segment fractions). The default first guess assumes We/W0 = 0.5. Returns a dict: W0 (converged), steps (list of dicts guess,
    We_W0, W0_new, change), We, Wf. Raises ValueError when 1 - Wf/W0 - We/W0 <= 0 (the mission
    cannot close). Example: size_takeoff_weight(500.0, 6200.0, 0.2144)["W0"] -> 28,570"""
    if guess is None:                      # default first guess: an empty-weight fraction of 0.5
        guess = (W_crew + W_payload) / max(0.05, 1.0 - Wf_W0 - 0.5)
    W = float(guess)
    steps = []
    for _ in range(max_steps):
        we = float(empty_weight_fraction(W, cls, kvs))
        den = 1.0 - Wf_W0 - we
        if den <= 0.0:
            raise ValueError(f"the mission does not close: 1 - Wf/W0 - We/W0 = {den:.4f} at W0 = {W:.0f} lb")
        new = (W_crew + W_payload) / den
        steps.append(dict(guess=W, We_W0=we, W0_new=new, change=new - W))
        if abs(new - W) < tol:
            return dict(W0=new, steps=steps, We=float(empty_weight_fraction(new, cls, kvs)) * new, Wf=Wf_W0 * new)
        W = new
    raise ValueError("the iteration did not converge")


# ===================================================================== unit checks
def _close(a, b, rtol, what):
    assert abs(a - b) <= rtol * abs(b), f"{what}: {a!r} vs {b!r}"


if __name__ == "__main__":
    # Table 3.1 fits: values computed from the published constants
    _close(float(empty_weight_fraction(100000.0)), 1.02 * 100000.0 ** -0.06, 1e-12, "jet transport fit")
    _close(float(empty_weight_fraction(100000.0)), 0.51124, 1e-4, "jet transport at 100,000 lb")
    _close(float(empty_weight_fraction(3000.0, "General aviation, single engine")), 0.55851, 1e-4, "GA single, 3,000 lb")
    # the metric A gives the same fraction for the same aircraft (to the rounding of the table)
    for cls in EMPTY_WEIGHT_FIT:
        lb = float(empty_weight_fraction(50000.0, cls))
        kg = float(empty_weight_fraction(50000.0 * 0.45359237, cls, metric=True))
        assert abs(lb - kg) < 0.012, (cls, lb, kg)
    assert len(EMPTY_WEIGHT_FIT) == 13
    # the fraction falls as aircraft grow (C < 0 for every class)
    assert all(c < 0 for _, _, c in EMPTY_WEIGHT_FIT.values())
    # units
    _close(NMI_FT, 6076.115, 1e-6, "ft per nmi")
    _close(KT_FPS, 1.687810, 1e-6, "ft/s per knot")
    # Breguet: units cancel when R in nmi, V in kt, C in 1/h; the same in ft, ft/s, 1/s
    f1 = cruise_fraction(1700.0, 0.55, 410.0, 13.0)
    f2 = math.exp(-(1700.0 * NMI_FT) * (0.55 / 3600.0) / (410.0 * KT_FPS * 13.0))
    _close(f1, f2, 1e-12, "Breguet in two unit systems")
    _close(loiter_fraction(1.25, 0.45, 13.0), math.exp(-1.25 * 0.45 / 13.0), 1e-12, "endurance")
    wx = mission_fraction([("takeoff", 0.970), ("climb", 0.985), ("cruise", f1), ("landing", 0.995)])
    wf = fuel_fraction(wx)
    _close(wf, 1.06 * (1.0 - 0.970 * 0.985 * f1 * 0.995), 1e-12, "fuel fraction")
    r = size_takeoff_weight(500.0, 6200.0, wf)
    W0 = r["W0"]
    _close(W0, 6700.0 / (1.0 - wf - float(empty_weight_fraction(W0))), 1e-4, "converged W0 is a fixed point")
    _close(r["We"] + r["Wf"] + 6700.0, W0, 1e-4, "the weights add up")
    assert len(r["steps"]) > 2 and abs(r["steps"][-1]["change"]) < 1.0
    try:
        size_takeoff_weight(500.0, 6200.0, 0.6)
        raise AssertionError("a fuel fraction of 0.6 cannot close")
    except ValueError:
        pass
    print("sizing.py: all unit checks passed")
    print(f"  example: Wf/W0 = {wf:.4f}, W0 = {W0:,.0f} lb in {len(r['steps'])} steps")
