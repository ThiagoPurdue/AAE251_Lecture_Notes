"""Published numbers that the pages of Chapter 3 print or draw, each with its source (every
source opened). The invented values of the worked examples stay in the page modules; what a
book, a report or a data set states is here.

Sources:
  - NOAA, NASA and USAF, U.S. Standard Atmosphere, 1976, Table III (dynamic viscosity, report
    pages 98, 100, 102 and 106).
  - Leishman, J. G., Introduction to Aerospace Flight Vehicles (Embry-Riddle Aeronautical
    University, open textbook, 2022), Chapter 18: the worked example of an airliner wing of mean
    chord 2.75 m at Mach 0.82 and 30,000 ft; model aircraft and small uncrewed aircraft fly at
    Reynolds numbers of 10^3 to 10^5.
  - Purcell, E. M., "Life at Low Reynolds Number", American Journal of Physics 45 (1977), pp. 3
    and 4: a person swimming, about 10^4; a goldfish, about 10^2; a micron-size swimmer moving
    30 micrometers per second in water (kinematic viscosity 10^-2 cm^2/s).
  - Scholz, D., Aircraft Design, Chapter 5 (Hamburg University of Applied Sciences, lecture
    notes, n.d.): Section 5.4, Eq. (5.21), after Loftin (1980), drag increments of passenger
    jets with flaps (0.01 at 15 deg, 0.03 at 35 deg) and with the landing gear extended
    (0.015), and a span efficiency of 0.7 with flaps and slats extended; Section 5.7, the span
    efficiency 0.85 that Loftin chooses for jets in cruise.
  - Nicolai, L. M., and Carichner, G. E., Fundamentals of Aircraft and Airship Design, Vol. 1
    (AIAA, 2010): Table 6.1 (takeoff wing-loading trends, lb/ft^2, by dominant mission
    requirement, with an example aircraft of each class), Section 6.1 (cruise efficiency
    drives the takeoff wing loading above about 100 lb/ft^2), Example 6.1 (the air-launched
    cruise missile and its published answers), Table 9.1 (C_L,max of aircraft with their
    high-lift systems).
  - Jenkinson, L. R., Simpkin, P., and Rhodes, D., Civil Jet Aircraft Design (1999), companion
    web site, Data A, Table 4 (Boeing 777-200).

Run this file for its unit checks:  python3 -B scripts/chapter_3/published.py
"""
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chapter_3.aero import RHO_SL_EN, mu_sutherland  # noqa: E402


# ===================================================================== viscosity, Reynolds numbers (page 3.1)
# U.S. Standard Atmosphere 1976, Table III: (geopotential altitude m, temperature K, mu kg/(m s))
USSA_MU_POINTS = [(-5000.0, 320.65, 1.9421e-5), (0.0, 288.15, 1.7894e-5), (5000.0, 255.65, 1.6281e-5),
                  (11000.0, 216.65, 1.4216e-5)]
# Leishman (2022), Chapter 18: an airliner wing of mean chord 2.75 m at Mach 0.82 and 30,000 ft
LEISHMAN_AIRLINER = dict(c=2.75, M=0.82, h_ft=30000.0)
# Leishman (2022), Chapter 18: the Reynolds-number range of model aircraft and small uncrewed aircraft
LEISHMAN_SMALL_AIRCRAFT_RE = (1.0e3, 1.0e5)
# Purcell (1977): a micron-size swimmer, 30 micrometers per second in water (nu = 1e-6 m^2/s)
PURCELL_BACTERIUM = dict(L=1.0e-6, V=30.0e-6, nu=1.0e-6)
PURCELL_GOLDFISH_RE = 1.0e2
PURCELL_SWIMMER_RE = 1.0e4

# ===================================================================== drag polar configurations (page 3.3)
# Scholz (n.d.), Section 5.7, after Loftin (1980): span efficiency of jets in cruise
LOFTIN_E_CRUISE_JET = 0.85
# Scholz (n.d.), Section 5.4, Eq. (5.21), after Loftin (1980): passenger jets, flap and gear
# drag increments, span efficiency with flaps and slats extended, and the lift coefficient of
# each flap setting
SCHOLZ_FLAPS_GEAR = {"takeoff": dict(dCD_flap=0.01, dCD_gear=0.015, e=0.7, CL_op=1.3, flap_deg=15),
                     "landing": dict(dCD_flap=0.03, dCD_gear=0.015, e=0.7, CL_op=1.7, flap_deg=35)}

# ===================================================================== wing loading (wing-loading page)
# Nicolai and Carichner (2010), Table 6.1: dominant mission requirement, (W/S)_TO range in
# lb/ft^2, example aircraft. The table's light-aircraft row is left out on purpose (the
# instructor's decision: the notes give no wing loading for light aircraft). Split into two
# groups for the figure (six rows each).
WS_TRENDS_CIVIL = [
    ("High-altitude surveillance, solar", 0.5, 3.0, "Helios"),
    ("Competition sailplanes", 7.0, 12.0, "ASW 17"),
    ("High-altitude surveillance, fuel-burning", 25.0, 50.0, "RQ-4A"),
    ("Short-field and utility transports", 40.0, 90.0, "C-130"),
    ("Short or intermediate range jets", 50.0, 90.0, "Learjet 35"),
    ("Long-range transports and bombers", 110.0, 150.0, "Boeing 747"),
]
WS_TRENDS_MILITARY = [
    ("Fighter, high altitude", 30.0, 60.0, "F-106"),
    ("Fighter, air to air", 50.0, 80.0, "F-15A"),
    ("Fighter, close air support", 65.0, 90.0, "A-10A"),
    ("Fighter, strike interdiction", 90.0, 130.0, "F-4E"),
    ("Fighter, interceptor", 120.0, 150.0, "F-104G"),
    ("Low-altitude cruise missiles", 200.0, 240.0, "AGM-109"),
]
# Nicolai and Carichner (2010), Section 6.1: cruise efficiency drives (W/S)_TO above this, lb/ft^2
WS_CRUISE_HIGH = 100.0
# Nicolai and Carichner (2010), Table 9.1: C_L,max of two aircraft with their high-lift systems
CLMAX_T91 = {"777-200": 2.8, "U-2S": 1.21}
# Nicolai and Carichner (2010), Example 6.1: air-launched cruise missile (and its published answers)
ALCM = dict(CD0=0.035, K=0.059, W_lb=1800.0, M=0.7, h_ft=200.0, rho=RHO_SL_EN, a=1116.4,
            book_CL=0.44, book_WS=319.0, book_S=5.64, book_LD_start=9.5, book_LD_end=6.9,
            book_LD_avg=8.2,       # the average L/D over the flight: sized with it, the missile comes out near
            tomahawk_lb=2860.0)    # the launch weight of the Tomahawk (AGM-109), 2,860 lb (Example 6.1, closing)
# Jenkinson et al. (1999), Data A, Table 4: Boeing 777-200
B772_MTOW_KG = 242670.0
B772_S_M2 = 427.80
B772_WING_LOAD_KGM2 = 567.25


# ===================================================================== unit checks
if __name__ == "__main__":
    for _, T, mu in USSA_MU_POINTS:                       # the table agrees with Sutherland's law
        assert abs(float(mu_sutherland(T)) - mu) <= 5e-4 * mu, (T, mu)
    assert abs(B772_MTOW_KG / B772_S_M2 - B772_WING_LOAD_KGM2) < 0.01        # Jenkinson's wing load
    assert all(lo < hi for _, lo, hi, _ in WS_TRENDS_CIVIL + WS_TRENDS_MILITARY)
    assert not any("172" in ex or "ight" in nm for nm, *_, ex in WS_TRENDS_CIVIL)   # no light-aircraft row
    for c in SCHOLZ_FLAPS_GEAR.values():
        assert c["e"] < LOFTIN_E_CRUISE_JET
    print("published.py: all unit checks passed")
