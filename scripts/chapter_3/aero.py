"""Aerodynamics of Chapter 3: coefficients and forces, viscosity and the Reynolds number, the
boundary layer on a flat plate, the finite wing, the drag polar, drag against speed, minimum
drag, and wing loading. SI units unless a function name ends in _en (English units: ft, slug,
lbf, deg R). Angles in degrees unless a name says rad.

Sources (each opened):
  - Viscosity: U.S. Standard Atmosphere, 1976 (NOAA, NASA, USAF; NASA-TM-X-74335), Part 1,
    equation (51): mu = beta T^(3/2) / (T + S) with beta = 1.458 x 10^-6 kg/(m s K^0.5) and
    Sutherland's constant S = 110.4 K (the value of the NASA errata sheet bound with the NTRS
    copy). Table III of the same report gives mu = 1.7894 x 10^-5 N s/m^2 at 0 m (288.15 K),
    1.6937 x 10^-5 at 3,000 m geopotential (268.65 K) and 1.4216 x 10^-5 at 11,000 m
    (216.65 K): the unit checks below reproduce them. NASA Glenn Research Center,
    "Viscosity" (Beginner's Guide to Aeronautics, n.d.) states the same law with S = 198.72 deg R
    (= 110.4 K). These notes use mu = 1.789 x 10^-5 kg/(m s) at 288.16 K (sea level, page 1.4).
  - Units: 1 slug/(ft s) = 47.880 kg/(m s) (from 1 slug = 14.5939 kg and 1 ft = 0.3048 m,
    NIST SP 811, as in chapter_1/constants.py).
  - Boundary-layer thickness on a flat plate (99 percent thickness): laminar
    delta = 5.0 x / sqrt(Re_x) (the Blasius solution), turbulent delta = 0.37 x / Re_x^(1/5)
    (turbulent from the leading edge, one-seventh power profile): Leishman, J. G.,
    Introduction to Aerospace Flight Vehicles (Embry-Riddle Aeronautical University, open
    textbook, 2022), Chapter 26. The Blasius profile itself is computed in blasius() and checked
    against f''(0) = 0.332.
  - Transition Reynolds number of a flat plate: RE_TR_PLATE = 5 x 10^5, a guide value that
    depends on surface roughness, pressure gradient and free-stream turbulence (Leishman 2022,
    Chapter 18).
  - Finite wing, induced drag, drag polar, minimum drag: alpha_i = 57.3 C_L/(pi e AR),
    C_D,i = C_L^2/(pi e AR), a = a0/(1 + 57.3 a0/(pi e AR)), C_D = C_D,0 + K C_L^2 with
    K = 1/(pi e AR), in the notation of Chapter 3. The unit checks test the identities that
    follow from them.
  - Flap increment: Nicolai, L. M., and Carichner, G. E., Fundamentals of Aircraft and Airship
    Design, Vol. 1 (AIAA, 2010), Chapter 9, Eq. (9.9) and Figure 9.23: the wing increment of the
    maximum lift coefficient from a trailing-edge flap, Delta C_L,max = Delta c_l,max
    (S_flapped / S) K_Lambda, with K_Lambda = (1 - 0.08 cos^2 Lambda) cos^(3/4) Lambda and Lambda
    the quarter-chord sweep (0.92 for an unswept wing).

Run this file for its unit checks:  python3 -B scripts/chapter_3/aero.py
"""
import math

import numpy as np

# ===================================================================== constants of these notes
T_SL = 288.16                 # K, sea level (page 1.4)
RHO_SL = 1.2250               # kg/m^3
MU_SL = 1.789e-5              # kg/(m s), the value these notes use at sea level
RHO_SL_EN = 0.002377          # slug/ft^3
MU_SL_EN = 3.737e-7           # slug/(ft s)
G0 = 9.81                     # m/s^2: 9.81 m/s^2, the value used throughout the course (as chapter_1.atmosphere.G0)
G0_EN = 32.2                  # ft/s^2
DEG_PER_RAD = 57.3            # degrees per radian, as these notes write it
SUTH_BETA = 1.458e-6          # kg/(m s K^0.5), U.S. Standard Atmosphere 1976, eq. (51)
SUTH_S = 110.4                # K, Sutherland's constant (USSA 1976, errata)
SLUG_FT_S = 14.5939029 / 0.3048   # kg/(m s) per slug/(ft s) = 47.880
RE_TR_PLATE = 5.0e5           # flat-plate transition Reynolds number, a guide value (Leishman 2022, Chapter 18)
# Published table values used by the unit checks (USSA 1976, Table III): (T K, mu kg/(m s))
USSA_MU_TABLE = [(288.15, 1.7894e-5), (268.65, 1.6937e-5), (216.65, 1.4216e-5)]


# ===================================================================== forces and coefficients
def dynamic_pressure(rho, V):
    """q = rho V^2 / 2 (any consistent units). Example: dynamic_pressure(1.225, 50.0) -> 1,531"""
    return 0.5 * rho * np.asarray(V, dtype=float) ** 2


def force(coef, q, S):
    """Lift or drag from its coefficient: F = q S C. Per unit span, pass S = chord. Example: force(0.8, 1531.25, 16.0) -> 19,600"""
    return coef * q * S


def moment(coef, q, S, c):
    """Pitching moment M = q S c C_M (per unit span: S = c, so M' = q c^2 c_m). Example: moment(-0.1, 1000.0, 1.0, 1.0) -> -100.0"""
    return coef * q * S * c


def coefficient(F, q, S):
    """C = F / (q S). Example: coefficient(19600.0, 1531.25, 16.0) -> 0.8000"""
    return F / (q * S)


def mach_number(V, T, gamma=1.4, R=287.0):
    """V / sqrt(gamma R T). Example: mach_number(100.0, 288.16) -> 0.2939"""
    return V / math.sqrt(gamma * R * T)


# ===================================================================== viscosity, Reynolds number
def mu_sutherland(T, beta=SUTH_BETA, S=SUTH_S):
    """Dynamic viscosity of air, kg/(m s), at temperature T (K): mu = beta T^1.5/(T + S)
    (USSA 1976). Rises with temperature. Example: mu_sutherland(288.16) -> 1.789e-05"""
    T = np.asarray(T, dtype=float)
    return beta * T ** 1.5 / (T + S)


def mu_sutherland_en(T_R):
    """Dynamic viscosity in slug/(ft s) at T in degrees Rankine. Example: mu_sutherland_en(518.69) -> 3.737e-07"""
    return mu_sutherland(np.asarray(T_R, dtype=float) / 1.8) / SLUG_FT_S


def kinematic_viscosity(mu, rho):
    """nu = mu / rho, m^2/s (or ft^2/s). Example: kinematic_viscosity(1.789e-5, 1.225) -> 1.460e-05"""
    return mu / rho


def reynolds(rho, V, L, mu):
    """Re = rho V L / mu, with L the characteristic length (chord, body length, diameter: say which).
    Example: reynolds(1.225, 50.0, 0.25, 1.789e-5) -> 855,900"""
    return rho * V * L / mu


def speed_for_reynolds(Re, rho, L, mu):
    """Speed that gives Reynolds number Re: V = Re mu / (rho L). Example: speed_for_reynolds(1e6, 1.225, 0.25, 1.789e-5) -> 58.42"""
    return Re * mu / (rho * L)


def transition_x(rho, V, mu, Re_tr=RE_TR_PLATE):
    """Distance from the leading edge of a flat plate where Re_x reaches Re_tr: x = Re_tr mu/(rho V).
    Example: transition_x(1.225, 50.0, 1.789e-5) -> 0.1460"""
    return Re_tr * mu / (rho * V)


# ===================================================================== flat-plate boundary layer
def delta_laminar(x, Re_x):
    """99 percent thickness of a laminar boundary layer, delta = 5.0 x / sqrt(Re_x). Example: delta_laminar(0.08, 3.4e5) -> 6.860e-04"""
    return 5.0 * np.asarray(x, float) / np.sqrt(np.asarray(Re_x, float))


def delta_turbulent(x, Re_x):
    """Thickness of a turbulent boundary layer (turbulent from the leading edge), delta = 0.37 x / Re_x^0.2.
    Example: delta_turbulent(1.0, 3.4e6) -> 0.01834"""
    return 0.37 * np.asarray(x, float) / np.asarray(Re_x, float) ** 0.2


_BLASIUS = None


def blasius(eta_max=8.0, n=1601):
    """The Blasius flat-plate solution: f''' + f f''/2 = 0, f(0) = f'(0) = 0, f'(inf) = 1, by
    shooting with RK4. Returns (eta, u/U) with eta = y sqrt(U/(nu x)), and f''(0). The profile
    reaches 0.99 near eta = 4.9 (delta = 5.0 x/sqrt(Re_x) rounds it). Example: blasius()[2] -> 0.3321"""
    global _BLASIUS
    if _BLASIUS is not None and _BLASIUS[0][-1] == eta_max and len(_BLASIUS[0]) == n:
        return _BLASIUS
    eta = np.linspace(0.0, eta_max, n)
    h = eta[1] - eta[0]

    def run(s):
        y = np.array([0.0, 0.0, s])
        out = [y.copy()]
        f = lambda y: np.array([y[1], y[2], -0.5 * y[0] * y[2]])
        for _ in range(n - 1):
            k1 = f(y); k2 = f(y + 0.5 * h * k1); k3 = f(y + 0.5 * h * k2); k4 = f(y + h * k3)
            y = y + h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
            out.append(y.copy())
        return np.array(out)
    lo, hi = 0.2, 0.5
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if run(mid)[-1, 1] < 1.0:
            lo = mid
        else:
            hi = mid
    sol = run(0.5 * (lo + hi))
    _BLASIUS = (eta, sol[:, 1], 0.5 * (lo + hi))
    return _BLASIUS


def laminar_profile(y_over_delta):
    """u/U of the Blasius profile at y/delta, with delta = 5.0 x/sqrt(Re_x) (so eta = 5.0 y/delta).
    Example: laminar_profile(0.5) -> 0.7290"""
    eta, u, _ = blasius()
    return np.interp(5.0 * np.asarray(y_over_delta, float), eta, u)


def turbulent_profile(y_over_delta, n=7.0):
    """u/U = (y/delta)^(1/n), the one-seventh power law (n = 7), 1 above delta. Example: turbulent_profile(0.5) -> 0.9057"""
    r = np.clip(np.asarray(y_over_delta, float), 0.0, 1.0)
    return r ** (1.0 / n)


# ===================================================================== finite wing
def induced_angle(CL, AR, e=1.0):
    """Induced angle of attack, deg: alpha_i = 57.3 C_L / (pi e AR). Example: induced_angle(0.6, 8.0, 0.9) -> 1.520"""
    return DEG_PER_RAD * CL / (math.pi * e * AR)


def induced_drag_coef(CL, AR, e=1.0):
    """C_D,i = C_L^2 / (pi e AR). Example: induced_drag_coef(0.6, 8.0, 0.9) -> 0.01592"""
    return np.asarray(CL, float) ** 2 / (math.pi * e * AR)


def wing_lift_slope(a0, AR, e=1.0):
    """Finite-wing lift-curve slope, per deg: a = a0 / (1 + 57.3 a0 / (pi e AR)), a0 per deg.
    Example: wing_lift_slope(0.11, 8.0, 0.9) -> 0.08523"""
    return a0 / (1.0 + DEG_PER_RAD * a0 / (math.pi * e * AR))


def wing_CL(alpha, a, alpha_L0):
    """C_L = a (alpha - alpha_L=0), angles in deg, a per deg. Example: wing_CL(4.0, 0.085, -2.0) -> 0.5100"""
    return a * (np.asarray(alpha, float) - alpha_L0)


def wing_drag_coef(cd, CL, AR, e=1.0):
    """Wing drag coefficient: section drag plus induced drag, C_D = c_d + C_L^2/(pi e AR). Example: wing_drag_coef(0.006, 0.6, 8.0, 0.9) -> 0.02192"""
    return cd + induced_drag_coef(CL, AR, e)


# ===================================================================== drag polar and drag against speed
def polar_K(AR, e):
    """K = 1 / (pi e AR). Example: polar_K(8.0, 0.8) -> 0.04974"""
    return 1.0 / (math.pi * e * AR)


def polar_CD(CL, CD0, K):
    """Parabolic drag polar C_D = C_D,0 + K C_L^2. Example: polar_CD(0.5, 0.02, 0.05) -> 0.03250"""
    return CD0 + K * np.asarray(CL, float) ** 2


def min_drag_point(CD0, K):
    """The minimum-drag point of the parabolic polar: dict CL_star = sqrt(CD0/K), CD_star = 2 CD0,
    LD_max = 1/(2 sqrt(K CD0)). Example: min_drag_point(0.02, 0.05)["LD_max"] -> 15.81"""
    CLs = math.sqrt(CD0 / K)
    return dict(CL_star=CLs, CD_star=CD0 + K * CLs ** 2, LD_max=1.0 / (2.0 * math.sqrt(K * CD0)))


def level_CL(W, rho, V, S):
    """Lift coefficient in steady level flight (L = W): C_L = 2 W / (rho V^2 S). Example: level_CL(50000.0, 1.225, 60.0, 30.0) -> 0.7559"""
    return 2.0 * W / (rho * np.asarray(V, float) ** 2 * S)


def drag_parts(W, rho, V, S, CD0, K):
    """Drag in steady level flight split in its parts: parasite q S C_D0 (grows with V^2) and
    induced K W^2/(q S) (falls with 1/V^2). Returns (parasite, induced, total).
    Example: drag_parts(50000.0, 1.225, 60.0, 30.0, 0.02, 0.05)[2] -> 2,915"""
    q = dynamic_pressure(rho, V)
    Dp = q * S * CD0
    Di = K * W ** 2 / (q * S)
    return Dp, Di, Dp + Di


def min_drag_speed(W, rho, S, CD0, K):
    """Speed of minimum drag in level flight, V = sqrt(2 W/(rho S C_L*)). Example: min_drag_speed(50000.0, 1.225, 30.0, 0.02, 0.05) -> 46.49"""
    return math.sqrt(2.0 * W / (rho * S * min_drag_point(CD0, K)["CL_star"]))


# ===================================================================== wing loading
def wing_loading_stall(rho, V_stall, CL_max):
    """Largest wing loading that meets a stall speed: W/S = rho V_stall^2 C_L,max / 2. Example: wing_loading_stall(1.225, 60.0, 2.2) -> 4,851"""
    return 0.5 * rho * V_stall ** 2 * CL_max


def stall_speed(WS, rho, CL_max):
    """Stall speed from the wing loading: V = sqrt(2 (W/S)/(rho C_L,max)). Example: stall_speed(4851.0, 1.225, 2.2) -> 60.00"""
    return math.sqrt(2.0 * WS / (rho * CL_max))


def sweep_factor(sweep_deg=0.0):
    """K_Lambda = (1 - 0.08 cos^2 Lambda) cos^(3/4) Lambda, Lambda the quarter-chord sweep in deg
    (Nicolai and Carichner 2010, Figure 9.23). Example: sweep_factor(0.0) -> 0.9200"""
    c = math.cos(math.radians(sweep_deg))
    return (1.0 - 0.08 * c ** 2) * c ** 0.75


def flap_dCLmax(dcl_airfoil, S_flapped_over_S, sweep_deg=0.0):
    """Wing increment of C_L,max from a trailing-edge flap, Delta C_L,max = Delta c_l,max
    (S_flapped/S) K_Lambda (Nicolai and Carichner 2010, Eq. (9.9)). Example: flap_dCLmax(1.0, 0.65) -> 0.5980"""
    return dcl_airfoil * S_flapped_over_S * sweep_factor(sweep_deg)


# ===================================================================== unit checks
def _close(a, b, rtol, what):
    assert abs(a - b) <= rtol * abs(b), f"{what}: {a!r} vs {b!r}"


if __name__ == "__main__":
    for T, mu in USSA_MU_TABLE:                     # USSA 1976 Table III, to its 5 printed digits
        _close(float(mu_sutherland(T)), mu, 6e-5, f"Sutherland at {T} K")
    _close(float(mu_sutherland(T_SL)), MU_SL, 3e-4, "the notes' sea-level viscosity")
    _close(float(mu_sutherland_en(T_SL * 1.8)), MU_SL_EN, 5e-4, "English-unit viscosity")
    _close(MU_SL / SLUG_FT_S, MU_SL_EN, 5e-4, "unit conversion of mu")
    assert mu_sutherland(400.0) > mu_sutherland(300.0) > mu_sutherland(200.0)    # air: rises with T
    _close(reynolds(1.225, 50.0, 0.25, MU_SL), 1.225 * 12.5 / MU_SL, 1e-12, "Re")
    _close(speed_for_reynolds(reynolds(1.2, 33.0, 0.5, MU_SL), 1.2, 0.5, MU_SL), 33.0, 1e-12, "Re round trip")
    _close(reynolds(1.225, 50.0, transition_x(1.225, 50.0, MU_SL), MU_SL), RE_TR_PLATE, 1e-12, "transition x")
    eta, u, fpp = blasius()
    _close(fpp, 0.33206, 2e-4, "Blasius f''(0)")
    _close(float(np.interp(0.99, u, eta)), 4.91, 0.01, "Blasius 99 percent thickness at eta = 4.91")
    _close(float(turbulent_profile(1.0)), 1.0, 1e-12, "1/7 law at the edge")
    assert float(laminar_profile(0.0)) == 0.0 and float(turbulent_profile(0.0)) == 0.0    # no slip
    # finite wing: alpha_i in degrees is 57.3 times the radian value; C_D,i = C_L alpha_i (rad)
    CL, AR, e = 0.7, 7.5, 0.85
    _close(induced_angle(CL, AR, e) / DEG_PER_RAD * CL, float(induced_drag_coef(CL, AR, e)), 1e-12, "D_i = L alpha_i")
    a0 = 0.108
    a = wing_lift_slope(a0, AR, e)
    _close(a, a0 / (1 + DEG_PER_RAD * a0 / (math.pi * e * AR)), 1e-12, "finite slope")
    assert a < a0 and wing_lift_slope(a0, 30.0, e) > a                  # larger AR, closer to a0
    _close(float(wing_CL(-2.0, a, -2.0)), 0.0, 1e-12, "same zero-lift angle")
    # the minimum-drag point: C_D = 2 C_D0, induced = parasite, and the numerical minimum of D(V)
    CD0, K = 0.021, polar_K(8.5, 0.82)
    m = min_drag_point(CD0, K)
    _close(m["CD_star"], 2 * CD0, 1e-12, "C_D = 2 C_D0 at C_L*")
    _close(m["LD_max"], m["CL_star"] / m["CD_star"], 1e-12, "(L/D)max = C_L*/C_D*")
    CL_grid = np.linspace(0.05, 2.0, 200001)
    _close(float(np.max(CL_grid / polar_CD(CL_grid, CD0, K))), m["LD_max"], 1e-8, "L/D max numerically")
    W, S, rho = 60000.0, 28.0, 1.0
    V = np.linspace(20.0, 200.0, 400001)
    Dp, Di, D = drag_parts(W, rho, V, S, CD0, K)
    Vmd = min_drag_speed(W, rho, S, CD0, K)
    _close(float(V[np.argmin(D)]), Vmd, 1e-4, "minimum of D(V) equals the formula")
    _close(float(np.min(D)), W / m["LD_max"], 1e-8, "D_min = W/(L/D)max")
    i = int(np.argmin(abs(V - Vmd)))
    _close(float(Dp[i]), float(Di[i]), 1e-3, "parasite = induced at minimum drag")
    _close(float(level_CL(W, rho, Vmd, S)), m["CL_star"], 1e-12, "C_L at V_md")
    _close(stall_speed(wing_loading_stall(1.1, 55.0, 1.9), 1.1, 1.9), 55.0, 1e-12, "stall round trip")
    _close(flap_dCLmax(1.0, 1.0, 0.0), 0.92, 1e-12, "flap increment factor, unswept wing")
    assert sweep_factor(30.0) < sweep_factor(0.0)                        # sweep lowers the increment
    print("aero.py: all unit checks passed")
    print(f"  mu(288.16 K) = {float(mu_sutherland(T_SL)):.4e} kg/(m s); Blasius f''(0) = {fpp:.5f}")
