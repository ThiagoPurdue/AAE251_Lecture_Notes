"""Units, Earth and the few places of Chapter 1 that are not tied to one topic, each with its
source. Every page module reaches them through `from chapter_1.common import *`; no page module
types a constant of its own.

Sources:
  - Units: 1 ft = 0.3048 m, 1 nautical mile = 1,852 m, 1 statute mile = 1,609.344 m and
    1 lb (mass) = 0.45359237 kg are exact by definition (NIST Special Publication 811,
    Appendix B); 1 lb (force) = 4.448222 N follows from the last with standard gravity;
    1 slug = 14.5939029 kg and 1 ft lb = 1.3558179483 J (same appendix).
  - Earth: the values of Chapter 2 (scripts/chapter_2/orbits.py), so a number for Earth is the
    same in every chapter of the book: gravitational parameter 3.986 x 10^5 km^3/s^2,
    equatorial radius 6,378 km, mean radius 6,371 km, sidereal day 86,164 s.
  - Landing gear: 14 CFR 25.473(a)(2): a transport airplane's landing gear is designed for a
    limit descent velocity of 10 ft/s at the design landing weight.
  - Airports: FAA Form 5010-1, Airport Master Record, airport reference points of Boston
    Logan (BOS) and Los Angeles (LAX), degrees, minutes and seconds.

Run this file for its unit checks:  python3 -B scripts/chapter_1/constants.py
"""
import math

# ===================================================================== units (exact)
FT = 0.3048                   # m per ft
NMI = 1852.0                  # m per nautical mile
NMI_FT = NMI / FT             # ft per nautical mile (6,076.1)
KT_FPS = NMI_FT / 3600.0      # ft/s per knot (1.6878)
MILE_KM = 1.609344            # km per statute mile
LB_KG = 0.45359237            # kg per lb (mass)
KG_LB = 1.0 / LB_KG           # lb per kg (2.2046)
LB_N = 4.448222               # N per lb (weight)
SLUG_KG = 14.5939029          # kg per slug
FTLB_J = 1.3558179483         # J per ft lb

# ===================================================================== Earth (as in Chapter 2)
MU_EARTH = 3.986e5            # km^3/s^2, gravitational parameter GM
RADIUS_EARTH_EQ = 6378.0      # km, equatorial radius
RADIUS_EARTH_MEAN = 6371.0    # km, mean radius (great-circle distances)
T_SIDEREAL = 86164.0          # s, sidereal day


# ===================================================================== a regulation the pages quote
LIMIT_SINK_RATE_FPS = 10.0    # ft/s, limit descent velocity of a transport airplane's landing gear


def _dms(d, m, s, sign=1.0):
    return sign * (d + m / 60.0 + s / 3600.0)


# Airport reference points, (latitude north, longitude east) in degrees (FAA Form 5010-1)
AIRPORTS = {
    "BOS": (_dms(42, 21, 46.6), _dms(71, 0, 23.0, -1.0)),
    "LAX": (_dms(33, 56, 32.987), _dms(118, 24, 28.975, -1.0)),
}


def great_circle_nmi(a, b, R_km=RADIUS_EARTH_MEAN):
    """Great-circle distance (nmi) between two (lat, lon) points in degrees on a sphere of radius
    R_km (haversine formula). Example: great_circle_nmi(AIRPORTS["BOS"], AIRPORTS["LAX"]) -> 2,264"""
    p1, l1 = map(math.radians, a)
    p2, l2 = map(math.radians, b)
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin((l2 - l1) / 2) ** 2
    return 2.0 * R_km * 1000.0 * math.asin(math.sqrt(h)) / NMI


def geo_altitude():
    """Altitude (km) of the geostationary orbit: the circular orbit whose period is one sidereal
    day, a = (mu (T/2 pi)^2)^(1/3), minus the equatorial radius. Example: geo_altitude() -> 35,786"""
    a = (MU_EARTH * (T_SIDEREAL / (2.0 * math.pi)) ** 2) ** (1.0 / 3.0)
    return a - RADIUS_EARTH_EQ


if __name__ == "__main__":
    assert abs(NMI_FT - 6076.115) < 1e-3 and abs(KT_FPS - 1.687810) < 1e-6
    assert abs(KG_LB - 2.204623) < 1e-6
    d = great_circle_nmi(AIRPORTS["BOS"], AIRPORTS["LAX"])
    assert 2200.0 < d < 2300.0, d                  # Boston to Los Angeles is about 2,260 nmi
    assert abs(great_circle_nmi((0.0, 0.0), (0.0, 1.0)) - 2 * math.pi * 6371.0e3 / 360.0 / NMI) < 1e-9
    g = geo_altitude()
    assert abs(g - 35786.0) < 5.0, g               # the geostationary altitude, about 35,786 km
    print("constants.py: all unit checks passed")
    print(f"  BOS-LAX {d:,.1f} nmi, GEO altitude {g:,.1f} km")
