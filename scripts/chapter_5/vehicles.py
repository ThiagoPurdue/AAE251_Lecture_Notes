"""The aircraft of Chapter 5, Aircraft Performance and Propulsion: one source for their data.

Every page module takes its aircraft from here (`from chapter_5.common import *` brings them in).
Each dictionary uses the keys the functions of `perf.py` take, so a call reads

    perf.min_thrust_condition(EXEC_JET["m"], EXEC_JET["S"], EXEC_JET["CD0"], EXEC_JET["K"], rho)

or, shorter, with the helpers at the end of this file: `available(EXEC_JET, rho)`, `weight(GA_AIRPLANE)`.

Keys (SI units; angles in degrees):
  name        the words the pages use for the aircraft
  kind        "jet" (rated in thrust, T_0 per engine) or "prop" (rated in shaft power, P_0 per engine)
  m, S        mass (kg) and wing area (m^2)
  CD0, K      the drag polar C_D = C_D,0 + K C_L^2 (K = 1 / (pi e AR) where AR and e are given)
  CLmax       clean maximum lift coefficient
  n           number of engines; T0 (N) or P0 (W) per engine at sea level, full throttle
  m_ad        exponent of the density lapse, T_A or P_A proportional to (rho / rho_0)^m_ad
  eta         propeller efficiency (propeller aircraft only)
  CL0, CLa    lift curve C_L = C_L,0 + C_L,alpha alpha, alpha in degrees (where given)
  CM0, CMa, CMde  pitching-moment line C_M = C_M,0 + C_M,alpha alpha + C_M,de delta_e (where given)
  fuel        usable fuel mass, kg (where given)
  c_g         power specific fuel consumption as a mass rate, g/(s kW) (propeller aircraft, where given);
              `power_sfc_per_m()` turns it into the weight-based c (1/m) of the range equations

Sign convention of the pitching moment (stated once for every aircraft here): a nose-up moment is
positive; the elevator angle delta_e is positive with the trailing edge down, which pushes the tail
up and gives a nose-down moment, so C_M,de is negative.

Where the values come from is written beside each one. "Example aircraft" values are the given data
of a published example and are printed with that data; "assumed" values are chosen here and said
to be assumed on the page.
"""
import math

from chapter_1.atmosphere import G0, RHO_SL

# ===================================================================== the jet (pages 5.1 to 5.3)
# A twin-engine executive jet. Example aircraft: mass, wing area, polar, two engines of 27,810 N
# (55,620 N together) and the lapse exponent 0.6 are its given data. Assumed: the clean C_L,max
# of 1.6 and the upper Mach number of 0.80 to which its low-speed polar is trusted (past it, wave
# drag adds to C_D,0; page 3.3 shows the same limit as a shaded band).
EXEC_JET = dict(
    name="twin-engine executive jet", kind="jet",
    m=33100.0, S=88.2, CD0=0.015, K=0.050,          # example aircraft
    n=2, T0=27810.0, m_ad=0.6,                      # example aircraft
    CLmax=1.6,                                      # assumed
    M_limit=0.80,                                   # assumed: the polar holds up to this Mach number
)

# ===================================================================== the propeller airplane (pages 5.1 and 5.2)
# A single-engine general-aviation airplane, propeller driven by a piston engine. Example aircraft,
# every value: mass with full tanks 1,315 kg, wing area 16.3 m^2, polar 0.026 + 0.054 C_L^2,
# lift curve C_L = 0.02 + 0.12 alpha (alpha in degrees), C_L,max = 2.4 at alpha = 19.8 deg (the example
# gives no flap setting; 0.02 + 0.12 x 19.8 = 2.396), pitching moment 0.12 - 0.08 alpha and an elevator
# term of 0.075 per degree, one engine of 216 kW, eta = 0.8, m_ad = 0.6, 168 kg of fuel, power specific
# fuel consumption 0.076 g/(s kW).
# Elevator sign: the example prints +0.075 delta_e while it also takes delta_e positive with the trailing
# edge down. Under the convention stated above (nose-up moment positive) a trailing-edge-down elevator
# gives a nose-down moment, so the coefficient is stored as -0.075 per degree: the same magnitude, the
# sign of the convention. Trim then comes out trailing edge up (delta_e negative). The printed +0.075 is
# a discrepancy of the example, reported for its author.
GA_AIRPLANE = dict(
    name="single-engine general-aviation airplane", kind="prop",
    m=1315.0, S=16.3, CD0=0.026, K=0.054, CLmax=2.4, alpha_max=19.8,
    CL0=0.02, CLa=0.12,
    CM0=0.12, CMa=-0.08, CMde=-0.075,
    n=1, P0=216.0e3, eta=0.80, m_ad=0.6,
    fuel=168.0, c_g=0.076,
)

# ===================================================================== the four-engine turboprop transport
# Invented for the chapter. Its size
# and power lie between two published four-engine turboprops: the Lockheed L-188 Electra (51,256 kg,
# 120 m^2, aspect ratio 7.5, four engines of 2,800 kW) and the Lockheed C-130H (70,307 kg, 162.1 m^2,
# four engines of 3,420 kW). Every value below is assumed.
#   AR = 8.4 and e = 0.80 give K = 1 / (pi 0.80 8.4) = 0.04737.
#   Lift curve: slope 0.09 per degree, near the finite-wing value 2 pi AR / (AR + 2) = 5.07 per radian;
#   C_L,0 = 0.25 with flaps up. Cruise near C_L = 0.57 is then at about 3.5 deg.
#   Pitching moment: C_M,alpha < 0 (statically stable); trim in cruise needs about 2.6 deg of
#   trailing-edge-up elevator (delta_e negative).
#   Usable fuel 9,000 kg; power specific fuel consumption 0.082 g/(s kW) (a turboprop in cruise).
TRANSPORT = dict(
    name="four-engine turboprop transport", kind="prop",
    m=52000.0, S=128.0, CD0=0.022, AR=8.4, e=0.80, K=1.0 / (math.pi * 0.80 * 8.4),
    CLmax=1.50,
    CL0=0.25, CLa=0.09,
    CM0=0.04, CMa=-0.03, CMde=-0.025,
    n=4, P0=2900.0e3, eta=0.84, m_ad=0.75,
    fuel=9000.0, c_g=0.082,
)

# ===================================================================== the light twin-jet (constraint-diagram page)
# Example aircraft: mass 4,500 kg, wing area 18 m^2, two engines of 6,000 N, C_L,max 1.90 with takeoff
# flaps and 2.15 with landing flaps (as the example prints it; the clean 1.45 plus the example's flap
# increment 0.9 x 1.3 x 0.60 gives 2.152 unrounded, which no page prints), braking friction 0.40,
# thrust lapse exponent 0.8, polar C_D,0 = 0.022 with AR = 8 and e = 0.8, clean C_L,max 1.45.
LIGHT_TWIN = dict(
    name="light twin-jet", kind="jet",
    m=4500.0, S=18.0, CD0=0.022, AR=8.0, e=0.8, K=1.0 / (math.pi * 0.8 * 8.0),
    CLmax=1.45, CLmax_TO=1.90, CLmax_L=2.15, mu_r=0.40,
    n=2, T0=6000.0, m_ad=0.8,
)
# Its requirements (example aircraft): stall speed with landing flaps at most 46 m/s; takeoff ground
# roll at most 750 m and landing ground roll at most 700 m at sea level; rate of climb 12 m/s at
# 90 m/s at sea level; cruise at 200 m/s at 10,000 m; service ceiling (0.5 m/s) of 12,000 m.
LIGHT_TWIN_REQ = dict(V_stall=46.0, s_LO=750.0, s_L=700.0, RC=12.0, V_climb=90.0,
                      h_cruise=10000.0, V_cruise=200.0, h_ceiling=12000.0, RC_ceiling=0.5)

AIRCRAFT = {"exec_jet": EXEC_JET, "ga_airplane": GA_AIRPLANE, "transport": TRANSPORT, "light_twin": LIGHT_TWIN}


# ===================================================================== small helpers
def weight(ac, g=G0):
    """Weight m g of an aircraft dictionary, N. Example: weight(TRANSPORT) -> 510,120 N"""
    return ac["m"] * g


def available(ac, rho, n=None, delta_t=1.0, rho0=RHO_SL):
    """Thrust available (N) of a jet or power available (W, shaft power times eta) of a propeller
    aircraft at density rho, with n engines running (default: all) and throttle delta_t:
    T_A = n delta_t T_0 (rho/rho_0)^m_ad, P_A = n delta_t eta P_0 (rho/rho_0)^m_ad.
    Example: available(TRANSPORT, 1.225, n=3) -> 7,308 kW (one engine out)"""
    k = ac["n"] if n is None else n
    lapse = (rho / rho0) ** ac["m_ad"]
    if ac["kind"] == "jet":
        return k * delta_t * ac["T0"] * lapse
    return k * delta_t * ac["eta"] * ac["P0"] * lapse


def power_sfc_per_m(ac, g=G0):
    """The weight-based power specific fuel consumption c (1/m) of the propeller range and endurance
    equations, from the mass rate c_g in g/(s kW): c = c_g x 1e-3 kg/g x g / (1e3 W/kW) = c_g g 1e-6.
    Example: power_sfc_per_m(GA_AIRPLANE) -> 7.456e-7 1/m"""
    return ac["c_g"] * 1.0e-6 * g


__all__ = ["EXEC_JET", "GA_AIRPLANE", "TRANSPORT", "LIGHT_TWIN", "LIGHT_TWIN_REQ", "AIRCRAFT",
           "weight", "available", "power_sfc_per_m"]
