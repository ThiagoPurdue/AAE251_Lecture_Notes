"""The standard atmosphere of these notes (1.4 Standard Atmosphere), and the same equations
for another planet or moon. SI units throughout: m, K, Pa, kg/m^3, m/s.

The model is the one of Anderson's textbooks, the 1959 ARDC model atmosphere: temperature
falls linearly from sea level to 11 km (lapse rate -6.5 K/km), stays at 216.66 K from 11 km to
25 km, rises at +3 K/km to 47 km (282.66 K), stays constant to 53 km, then falls at -4.5 K/km.
Gravity is the constant g0 = 9.8 m/s^2 and the altitude is taken as geopotential (the tables
list both; the difference is under 0.3% below 20 km).

Sources:
  - Anderson, J. D., Aircraft Performance and Design, McGraw-Hill, 1999, Appendix D,
    "Standard Atmosphere, SI Units" (the table states its values are from the 1959 ARDC
    model atmosphere; it lists geometric and geopotential altitude, T, p and rho). The layer
    breaks and lapse rates above were checked against its rows up to 59.5 km, and the unit
    checks below compare with its rows.
  - The sea-level values and the constants of the values these notes use: T = 288.16 K,
    p = 101,325 Pa, rho = 1.2250 kg/m^3, R = 287 J/(kg K), gamma = 1.4, g0 = 9.8 m/s^2.

Run this file for its unit checks:  python3 -B scripts/chapter_1/atmosphere.py
"""
import math

import numpy as np

# ===================================================================== constants
T_SL = 288.16              # K, sea-level standard temperature
P_SL = 101325.0            # Pa, sea-level standard pressure
RHO_SL = 1.2250            # kg/m^3, sea-level standard density
R_AIR = 287.0              # J/(kg K), specific gas constant of air
GAMMA_AIR = 1.4            # ratio of specific heats of air
G0 = 9.8                   # m/s^2, gravity (constant with altitude in these notes)

# Layers: (base altitude m, lapse rate K/m). Each layer runs to the next base. Gradient
# layers have a != 0, isothermal layers a = 0. Names as the text uses them.
LAYERS = [
    (0.0, -0.0065),        # troposphere: gradient
    (11000.0, 0.0),        # lower stratosphere: isothermal, 216.66 K
    (25000.0, 0.003),      # upper stratosphere: gradient
    (47000.0, 0.0),        # stratopause: isothermal, 282.66 K
    (53000.0, -0.0045),    # mesosphere: gradient
]
LAYER_NAMES = ["troposphere", "lower stratosphere", "upper stratosphere", "stratopause", "mesosphere"]
H_TOP = 59500.0            # m, the highest altitude of the source table; the model stops here
H_TROPOPAUSE = 11000.0     # m, top of the gradient layer the aircraft examples use
H_ISO_TOP = 25000.0        # m, top of the isothermal layer


def gradient_layer(h, h1, T1, p1, rho1, a, g0=G0, R=R_AIR):
    """T (K), p (Pa), rho (kg/m^3) at altitude h (m) in a gradient layer of lapse rate a (K/m)
    whose base h1 has T1, p1, rho1: T = T1 + a (h - h1), p/p1 = (T/T1)^(-g0/(aR)),
    rho/rho1 = (T/T1)^(-(g0/(aR) + 1)). Example: gradient_layer(5000, 0, 288.16, 101325, 1.225, -0.0065)[1] -> 54,038"""
    T = T1 + a * (np.asarray(h, dtype=float) - h1)
    n = g0 / (a * R)
    r = T / T1
    return T, p1 * r ** (-n), rho1 * r ** (-(n + 1.0))


def isothermal_layer(h, h1, T1, p1, rho1, g0=G0, R=R_AIR):
    """T (K), p (Pa), rho (kg/m^3) at altitude h (m) in an isothermal layer at temperature T1
    whose base h1 has p1, rho1: p/p1 = rho/rho1 = exp[-g0 (h - h1)/(R T1)].
    Example: isothermal_layer(16000, 11000, 216.66, 22650, 0.3642)[1] -> 10,300"""
    h = np.asarray(h, dtype=float)
    f = np.exp(-g0 * (h - h1) / (R * T1))
    return T1 + 0.0 * h, p1 * f, rho1 * f


def layer_bases(T0=T_SL, p0=P_SL, rho0=RHO_SL, layers=LAYERS, g0=G0, R=R_AIR):
    """The base of every layer carried up from sea level: list of dicts h1, a, T1, p1, rho1,
    h2 (the top of the layer) and name. Example: layer_bases()[1]["p1"] -> 22,650 (Pa at 11 km)"""
    out = []
    T1, p1, rho1 = T0, p0, rho0
    for i, (h1, a) in enumerate(layers):
        h2 = layers[i + 1][0] if i + 1 < len(layers) else H_TOP
        out.append(dict(h1=h1, h2=h2, a=a, T1=T1, p1=p1, rho1=rho1,
                        name=LAYER_NAMES[i] if i < len(LAYER_NAMES) else f"layer {i + 1}"))
        if a == 0.0:
            T1, p1, rho1 = (float(v) for v in isothermal_layer(h2, h1, T1, p1, rho1, g0, R))
        else:
            T1, p1, rho1 = (float(v) for v in gradient_layer(h2, h1, T1, p1, rho1, a, g0, R))
    return out


_BASES = layer_bases()


def layer_of(h):
    """The layer dict (see layer_bases) that holds altitude h (m). Example: layer_of(15000)["name"] -> 'lower stratosphere'"""
    if h < 0.0 or h > H_TOP:
        raise ValueError(f"altitude {h} m is outside the model (0 to {H_TOP:.0f} m)")
    for L in _BASES:
        if L["h1"] <= h <= L["h2"]:
            return L
    raise ValueError(h)


def standard(h):
    """Standard-atmosphere T (K), p (Pa), rho (kg/m^3) at altitude h (m, scalar or array),
    found by carrying the base values up through each layer.
    Example: standard(11000.0) -> (216.66, 22,650, 0.3642)"""
    h_arr = np.atleast_1d(np.asarray(h, dtype=float))
    T, p, rho = np.empty_like(h_arr), np.empty_like(h_arr), np.empty_like(h_arr)
    for i, hh in enumerate(h_arr):
        L = layer_of(float(hh))
        if L["a"] == 0.0:
            t_, p_, r_ = isothermal_layer(hh, L["h1"], L["T1"], L["p1"], L["rho1"])
        else:
            t_, p_, r_ = gradient_layer(hh, L["h1"], L["T1"], L["p1"], L["rho1"], L["a"])
        T[i], p[i], rho[i] = t_, p_, r_
    if np.ndim(h) == 0:
        return float(T[0]), float(p[0]), float(rho[0])
    return T, p, rho


def altitude_from_pressure(p):
    """Altitude (m) where the standard pressure is p (Pa): find the layer whose base and top
    pressures bracket p, then invert its equation. Example: altitude_from_pressure(54038.0) -> 5,000"""
    for L in _BASES:
        p_top = standard(L["h2"])[1]
        if p_top <= p <= L["p1"] * (1 + 1e-12):
            if L["a"] == 0.0:
                return L["h1"] - R_AIR * L["T1"] / G0 * math.log(p / L["p1"])
            T = L["T1"] * (p / L["p1"]) ** (-L["a"] * R_AIR / G0)
            return L["h1"] + (T - L["T1"]) / L["a"]
    raise ValueError(f"pressure {p} Pa is outside the model")


def altitude_from_density(rho):
    """Altitude (m) where the standard density is rho (kg/m^3). The density altitude of a
    measured density. Example: altitude_from_density(0.7364) -> 5,000"""
    for L in _BASES:
        r_top = standard(L["h2"])[2]
        if r_top <= rho <= L["rho1"] * (1 + 1e-12):
            if L["a"] == 0.0:
                return L["h1"] - R_AIR * L["T1"] / G0 * math.log(rho / L["rho1"])
            n = G0 / (L["a"] * R_AIR)
            T = L["T1"] * (rho / L["rho1"]) ** (-1.0 / (n + 1.0))
            return L["h1"] + (T - L["T1"]) / L["a"]
    raise ValueError(f"density {rho} kg/m^3 is outside the model")


def altitude_from_temperature(T, layer):
    """Altitude (m) in a gradient layer (a layer dict) where the temperature is T (K).
    Example: altitude_from_temperature(255.66, layer_of(1000)) -> 5,000"""
    if layer["a"] == 0.0:
        raise ValueError("an isothermal layer has one temperature at every altitude")
    return layer["h1"] + (T - layer["T1"]) / layer["a"]


def speed_of_sound(T, gamma=GAMMA_AIR, R=R_AIR):
    """Speed of sound a_s = sqrt(gamma R T), m/s. Example: speed_of_sound(288.16) -> 340.3"""
    return np.sqrt(gamma * R * np.asarray(T, dtype=float))


def mach(V, T, gamma=GAMMA_AIR, R=R_AIR):
    """Mach number V / a_s. Example: mach(250.0, 216.66) -> 0.8473"""
    return np.asarray(V, dtype=float) / speed_of_sound(T, gamma, R)


def density_from_state(p, T, R=R_AIR):
    """Equation of state solved for density: rho = p / (R T), kg/m^3. Example: density_from_state(101325, 288.16) -> 1.225"""
    return np.asarray(p, dtype=float) / (R * np.asarray(T, dtype=float))


def pressure_from_state(rho, T, R=R_AIR):
    """Equation of state: p = rho R T, Pa. Example: pressure_from_state(1.225, 288.16) -> 101,300"""
    return np.asarray(rho, dtype=float) * R * np.asarray(T, dtype=float)


def nonstandard(h, dT):
    """A hot or cold day: the standard temperature profile shifted by dT (K) at every altitude
    of the troposphere, with the standard sea-level pressure. Returns T, p, rho at h (m, below
    11 km). Example: nonstandard(0.0, 20.0)[2] -> 1.146"""
    T0 = T_SL + dT
    rho0 = P_SL / (R_AIR * T0)
    if np.any(np.asarray(h) > H_TROPOPAUSE):
        raise ValueError("nonstandard() covers the troposphere only")
    return gradient_layer(h, 0.0, T0, P_SL, rho0, LAYERS[0][1])


# ===================================================================== another planet or moon
def planet(h, T0, p0, g, R, a, rho0=None):
    """T, p, rho at altitude h (m) above the surface of a planet whose lowest layer has surface
    temperature T0 (K), pressure p0 (Pa), gravity g (m/s^2), gas constant R (J/(kg K)) and lapse
    rate a (K/m; 0 for isothermal). rho0 defaults to the equation of state p0/(R T0).
    Example: planet(1000.0, **PLANETS["Venus"]["model"])"""
    rho0 = p0 / (R * T0) if rho0 is None else rho0
    if a == 0.0:
        return isothermal_layer(h, 0.0, T0, p0, rho0, g, R)
    return gradient_layer(h, 0.0, T0, p0, rho0, a, g, R)


def planet_altitude_from_pressure(p, T0, p0, g, R, a, rho0=None):
    """Altitude (m) where the pressure of planet() is p (Pa). Example: planet_altitude_from_pressure(5e6, **PLANETS["Venus"]["model"])"""
    if a == 0.0:
        return -R * T0 / g * math.log(p / p0)
    T = T0 * (p / p0) ** (-a * R / g)
    return (T - T0) / a


UNIVERSAL_R = 8314.5       # J/(kmol K), universal gas constant (NIST CODATA 2018: 8,314.46, rounded):
                           # R = UNIVERSAL_R / molar mass (kg/kmol)
M_AIR = 28.96              # kg/kmol, molar mass of sea-level dry air (U.S. Standard Atmosphere, 1976,
                           # Table 3: 28.9644, rounded)
K_BOLTZMANN = 1.380649e-23  # J/K, Boltzmann constant (NIST CODATA, exact since 2019)

# Lowest-atmosphere values of another planet for a worked example on another world (no Mars:
# the notes compute nothing for Mars). Each value with its source; "computed" marks arithmetic
# on the source values. A page that uses one cites the same sources.
PLANETS = {
    "Venus": dict(
        model=dict(T0=737.0,          # K, average surface temperature: NASA NSSDC, Venus Fact Sheet (D. R. Williams)
                   p0=9.2e6,          # Pa, surface pressure 92 bar: same fact sheet
                   g=8.87,            # m/s^2, surface gravity (mean): same fact sheet
                   R=UNIVERSAL_R / 43.45,  # J/(kg K) (molar_mass below), from the mean molecular weight 43.45 of the fact sheet (computed: 191.4)
                   a=-0.008,          # K/m: "a lapse rate increasing from 8 to 9 K km-1" from 0 to 32 km,
                                      # ECSS-E-ST-10-04C (ESA), Annex G.7.2 Venus
                   rho0=65.0),        # kg/m^3, surface density ~65: NASA NSSDC, Venus Fact Sheet
        valid_to=32000.0,             # m, the deep layer of ECSS-E-ST-10-04C Annex G.7.2
        molar_mass=43.45,             # kg/kmol, mean molecular weight: NASA NSSDC, Venus Fact Sheet
    ),
}


# ===================================================================== unit checks
def _close(a, b, rtol, what):
    assert abs(a - b) <= rtol * abs(b), f"{what}: {a!r} vs {b!r} (rtol {rtol})"


if __name__ == "__main__":
    # The source table (Anderson 1999, Appendix D, 1959 ARDC): geopotential altitude h, T, p, rho.
    # The table uses g0 = 9.80665 m/s^2 and R = 287.05; these notes use 9.8 and 287, so pressure
    # and density agree within 0.3% to 25 km and 0.8% at 47 km; temperatures agree to 0.01 K.
    TABLE = [  # h (geopotential, m), T, p, rho
        (4996.0, 255.69, 5.4048e4, 7.3643e-1),
        (9984.0, 223.26, 2.6500e4, 4.1351e-1),
        (14965.0, 216.66, 1.2112e4, 1.9475e-1),
        (19937.0, 216.66, 5.5293e3, 8.8909e-2),
        (24902.0, 216.66, 2.5273e3, 4.0639e-2),
        (29859.0, 231.24, 1.1855e3, 1.7861e-2),
        (46655.0, 281.63, 1.2558e2, 1.5535e-3),
        (58948.0, 255.89, 2.7403e1, 3.7307e-4),
    ]
    for h, T, p, rho in TABLE:
        t_, p_, r_ = standard(h)
        assert abs(t_ - T) < 0.02, (h, t_, T)
        tol = 0.003 if h < 25500 else 0.009
        _close(p_, p, tol, f"p at {h} m")
        _close(r_, rho, tol, f"rho at {h} m")
    b = layer_bases()
    _close(b[1]["T1"], 216.66, 1e-12, "tropopause temperature 288.16 - 71.5")
    _close(b[3]["T1"], 282.66, 1e-12, "47 km temperature 216.66 + 66")
    T, p, rho = standard(0.0)
    _close(rho, RHO_SL, 1e-12, "sea level density")
    _close(float(density_from_state(P_SL, T_SL)), 1.2251, 1e-3, "state equation at sea level")
    # round trips
    for h in (0.0, 1234.0, 11000.0, 18000.0, 25000.0, 31000.0, 50000.0, 58000.0):
        T, p, rho = standard(h)
        _close(altitude_from_pressure(p) + 1.0, h + 1.0, 1e-9, f"h from p at {h}")
        _close(altitude_from_density(rho) + 1.0, h + 1.0, 1e-9, f"h from rho at {h}")
    _close(float(speed_of_sound(288.16)), 340.28, 1e-4, "speed of sound at sea level")
    _close(float(speed_of_sound(216.66)), 295.06, 1e-4, "speed of sound at 11 km")
    # isothermal layer: pressure falls by e over R T / g0
    H = R_AIR * 216.66 / G0
    T, p1, _ = standard(12000.0)
    T, p2, _ = standard(12000.0 + H)
    _close(p2 / p1, math.exp(-1.0), 1e-12, "scale height")
    # gradient equation reduces to the isothermal one as a -> 0
    g = gradient_layer(3000.0, 0.0, 250.0, 1e5, 1.0, -1e-9)
    i = isothermal_layer(3000.0, 0.0, 250.0, 1e5, 1.0)
    _close(float(g[1]), float(i[1]), 1e-6, "gradient -> isothermal")
    # Venus: the given surface values agree with the equation of state
    for name, P in PLANETS.items():
        m = P["model"]
        _close(m["p0"] / (m["R"] * m["T0"]), m["rho0"], 0.02, f"{name}: p0 = rho0 R T0")
        T, p, rho = planet(1000.0, **m)
        _close(planet_altitude_from_pressure(float(p), **m), 1000.0, 1e-9, f"{name} round trip")
    assert "Mars" not in PLANETS, "nothing is computed for Mars in these notes"
    _close(float(nonstandard(0.0, 0.0)[2]), 1.2251, 1e-3, "nonstandard with dT = 0")
    print("atmosphere.py: all unit checks passed")
    for h in (0.0, 5000.0, 11000.0, 16000.0, 25000.0):
        T, p, rho = standard(h)
        print(f"  h = {h:7.0f} m: T = {T:7.2f} K, p = {p:10.1f} Pa, rho = {rho:.5f} kg/m^3")
