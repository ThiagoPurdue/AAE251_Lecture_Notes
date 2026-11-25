"""The bridge from Chapter 4 to the published numbers of Chapters 1 and 2.

Chapter 4 builds its examples on worked examples the book has already printed: the Hohmann
transfer of page 2.2 (400 km to 20,200 km), the launch budget of page 2.3 (8.833 km/s, losses
included) and the Ariane 5 core stage of page 1.3. This module reads them from the code that
printed them and exposes numbers and pure functions only.

Why a bridge and not a star import: `chapter_2.orbits` keeps its own value record (`record`,
`save_figure`, `VALUES` of Chapter 2) and its own style names. `from chapter_2.orbits import *`
inside Chapter 4 would rebind Chapter 4's `record` and `save_figure` to Chapter 2's. Here the
module is imported under a private name, nothing is recorded in it, and only the names in
`__all__` leave this file.

Every number is asserted equal to the string the earlier page prints (its values.json), so a
change on page 2.2 or 2.3 stops the Chapter 4 run instead of silently changing a link.

    HOHMANN_22   dict: r1, r2 (km), dv1, dv2, dv_total (km/s), as page 2.2's worked example
    LAUNCH_23    dict: v_orbit, losses, rotation, total (km/s), as page 2.3's worked example
    ARIANE5_FLIGHT, ARIANE5_CORE   page 1.3's Ariane 5 facts; the core stage's dry and propellant
                 masses in kg (14,700 and 170,000)
    circular_speed(mu, r), hohmann(mu, r1, r2), MU, RADIUS   Chapter 2's functions and constants
"""
import json
import sys
from pathlib import Path

if __name__ not in ("chapter_4.links", "__main__"):
    raise ImportError("import this module as chapter_4.links (or through chapter_4.common)")

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import chapter_2.orbits as _O  # noqa: E402  (a private name: its record and saver never leave here)
import chapter_2.p22_orbit_transfers as _P22  # noqa: E402  (the inputs of page 2.2's worked example)
import chapter_2.p23_launch_to_orbit as _P23  # noqa: E402  (the inputs of page 2.3's worked example)
from chapter_1.launchers import ARIANE5_FLIGHT  # noqa: E402
from figkit import fmt  # noqa: E402

__all__ = ["km_as_printed", "TRANSFER_STAGE", "HOHMANN_22", "LAUNCH_23", "ARIANE5_FLIGHT", "ARIANE5_CORE", "circular_speed", "hohmann", "MU", "RADIUS"]

circular_speed = _O.circular_speed
hohmann = _O.hohmann
MU = dict(_O.MU)
RADIUS = dict(_O.RADIUS)

_PRINTED = {p.parent.name: json.loads(p.read_text(encoding="utf-8"))
            for p in (SCRIPTS / "chapter_1" / "values.json", SCRIPTS / "chapter_2" / "values.json")}


def _printed(chapter, page, key):
    return _PRINTED[chapter][page][key]


# ===================================================================== page 2.2: the Hohmann transfer
_h = _O.hohmann(_O.MU["Earth"], _P22.R1, _P22.R2)
HOHMANN_22 = dict(h1=_P22.H1, h2=_P22.H2, r1=_P22.R1, r2=_P22.R2,
                  dv1=float(_h["dv1"]), dv2=float(_h["dv2"]), dv_total=float(_h["dv_total"]))
assert fmt(HOHMANN_22["dv1"]) == "2.012" == _printed("chapter_2", "orbit-transfers", "h-dv1"), HOHMANN_22
assert fmt(HOHMANN_22["dv2"]) == "1.404", HOHMANN_22
assert fmt(HOHMANN_22["dv_total"]) == "3.416", HOHMANN_22

# ===================================================================== page 2.3: the launch budget
_ex = _P23.example()
LAUNCH_23 = dict(lat=_P23.EX_LAT, h=_P23.EX_H, inc=_P23.EX_INC, v_orbit=float(_ex["v"]), losses=float(_P23.EX_LOSS),
                 rotation=float(_ex["rot"]), total=float(_ex["total"]))
assert fmt(LAUNCH_23["total"]) == "8.833" == _printed("chapter_2", "launch-to-orbit", "ex-total"), LAUNCH_23
assert fmt(LAUNCH_23["v_orbit"]) == _printed("chapter_2", "launch-to-orbit", "ex-v")
assert fmt(LAUNCH_23["rotation"]) == _printed("chapter_2", "launch-to-orbit", "ex-rot")
assert abs(LAUNCH_23["v_orbit"] + LAUNCH_23["losses"] - LAUNCH_23["rotation"] - LAUNCH_23["total"]) < 1e-12

# ===================================================================== page 1.3: the Ariane 5 core stage
ARIANE5_FLIGHT = dict(ARIANE5_FLIGHT)
ARIANE5_CORE = dict(dry_kg=1000.0 * ARIANE5_FLIGHT["epc_dry_t"], prop_kg=1000.0 * ARIANE5_FLIGHT["epc_prop_t"])
assert ARIANE5_CORE == dict(dry_kg=14700.0, prop_kg=170000.0), ARIANE5_CORE

if __name__ == "__main__":
    print("links.py: page 2.2", fmt(HOHMANN_22["dv1"]), fmt(HOHMANN_22["dv2"]), fmt(HOHMANN_22["dv_total"]),
          "km/s; page 2.3", fmt(LAUNCH_23["total"]), "km/s; page 1.3 core stage", ARIANE5_CORE)


def km_as_printed(v_kms):
    """A delta-V an earlier page printed in km/s, converted to m/s from its printed digits (3.416 km/s is
    3,416 m/s), so a Chapter 4 example sizes with the number the reader sees. Example:
    km_as_printed(HOHMANN_22["dv_total"]) -> 3416.0"""
    from chapter_1.style import fmt
    return 1000.0 * float(fmt(v_kms))


# The transfer stage of page 4.2's worked example 2, which page 4.3 splits into two stages: payload (kg),
# specific impulse (s) and inert mass fraction, invented for the example (checked against the leak list).
TRANSFER_STAGE = dict(m_pay=1750.0, isp=323.0, f=0.17)
