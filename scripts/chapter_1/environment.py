"""The operating environment of aircraft and spacecraft (1.2 Hazards and Risk): where each hazard
is found, as published. Numbers only, each with its source; the pages cite the same sources.

Sources:
  - FAA, Aeronautical Information Manual, 7-5-1: over 90% of reported bird strikes happen at or
    below 3,000 ft above ground level.
  - FAA, Aeronautical Information Manual, 7-1-24 (microbursts): the downdraft is typically less
    than 1 mile across and can be as strong as 6,000 ft/min; the horizontal outflow near the
    surface can extend to about 2 1/2 miles across, with winds as strong as 45 knots, a 90-knot
    change from headwind to tailwind for an aircraft crossing it, within a few hundred feet of the
    ground.
  - FAA AC 91-74B, Pilot Guide: Flight in Icing Conditions (2015): ice accretes most at
    temperatures a little below 0 C; the liquid water content is negligible below about -20 C.
  - FAA AC 00-30C, Clear Air Turbulence Avoidance (2016): jet streams from FL200 to FL450.
  - NASA, "Radiation Belts with Satellites" (2013): the inner belt about 1,000 to 8,000 miles
    above the equator, the outer belt about 12,000 to 25,000 miles.
  - Banks, de Groh and Miller, NASA/TM-2004-213400 (2004): atomic oxygen is the most abundant
    species between 180 and 650 km.
  - NASA Orbital Debris Program Office, Frequently Asked Questions: most debris lies within
    2,000 km of the surface; below 600 km it falls back within several years.
  - NASA SP-8027, Spacecraft Radiation Torques (1969), Sections 1 and 2.1: the force of sunlight
    is nearly the same at every altitude of an Earth orbit, while drag falls with altitude, so
    radiation torques are generally the larger above about 1,000 km.
  - STScI, Hubble Space Telescope Primer: Hubble orbits at about 500 km.
  - The solar radio flux F10.7: monthly means of the adjusted Penticton series, file
    p12_f107_monthly.csv beside this module (its header gives the source and the months).
"""
BIRD_FT = 3000.0                    # ft above ground: over 90% of reported bird strikes at or below
ICE_T_TOP_C = 0.0                   # deg C: icing band, warm edge
ICE_T_BOT_C = -20.0                 # deg C: icing band, cold edge
JET_FL = (200.0, 450.0)             # flight levels (hundreds of ft): jet streams
INNER_BELT_MI = (1000.0, 8000.0)    # statute miles above the equator: inner radiation belt
OUTER_BELT_MI = (12000.0, 25000.0)  # statute miles above the equator: outer radiation belt
ATOMIC_OXYGEN_KM = (180.0, 650.0)   # km: atomic oxygen the most abundant species
DEBRIS_KM = 2000.0                  # km: most debris lies below this altitude
DRAG_YEARS_KM = 600.0               # km: below it, debris falls back within several years
HUBBLE_KM = 500.0                   # km: Hubble's orbit
MICROBURST_DOWN_FPM = 6000.0        # ft/min: strongest downdraft of a microburst (AIM 7-1-24)
MICROBURST_WIND_KT = 45.0           # knots: strongest outflow wind near the surface (AIM 7-1-24)
MICROBURST_SHEAR_KT = 90.0          # knots: headwind-to-tailwind change across it (AIM 7-1-24)
MICROBURST_DOWN_MI = 1.0            # statute miles: the downdraft is typically less than this across
MICROBURST_OUT_MI = 2.5             # statute miles: the outflow extends to about this across
SRP_DOMINANT_KM = 1000.0            # km: above it, radiation torques are generally larger than drag torques (SP-8027)
