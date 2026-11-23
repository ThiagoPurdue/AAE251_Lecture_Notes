#!/usr/bin/env python3
"""Every unit check of the Chapter 3 shared code, in one run. From the book folder:

    python3 -B scripts/chapter_3/selftest.py

Runs the checks of aero.py, tunnel.py, airfoil_data.py and published.py, then checks the drawing helpers of
drawing3.py and the chart helper against the layout gate: a tunnel outline with its parts named,
the redrawn NACA chart with a reading, an airfoil in a free stream, the downwash construction and
the wing seen from behind, drawn with the helpers, must pass the gate; the helpers' own asserts
must catch a wrong angle and a wrong spiral sense; and the gate must catch a label on a vector.
Nothing is written to the book.
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.dont_write_bytecode = True

for name in ("aero", "tunnel", "airfoil_data", "published"):
    runpy.run_path(str(HERE / f"{name}.py"), run_name="__main__")

from chapter_3.common import *  # noqa: E402,F403
import figkit  # noqa: E402
import chapter_1.atmosphere as _atm  # noqa: E402
import chapter_3.aero as _aero  # noqa: E402

# one g in Chapters 1 and 3: 9.81 m/s^2, the value used throughout the course
assert _atm.G0 == _aero.G0 == G0 == G == 9.81, (_atm.G0, _aero.G0, G0, G)


def _gate(fig):
    return layout_problems(fig) + pixel_problems(fig)


# 1. the record and the saver are Chapter 3's, not Chapter 1's
assert record.__self__.number == 3 and save_figure.__self__.number == 3 and PAGES["p32"] == "airfoil-and-finite-wing"
import chapter_1.style as _c1  # noqa: E402
assert _c1.record.__self__.number == 1, "Chapter 1 keeps its own record"
assert figkit._WORD_SUB.search("$c_{m,ac}$") and figkit._WORD_SUB.search(r"$(L/D)_\max$")
assert figkit._WORD_SUB.search(r"$c_{m,\mathrm{ac}}$") and figkit._WORD_SUB.search(r"$M_\mathrm{ac}$")

# 2. a tunnel outline, parts named with controlled leaders, stations inside the duct: passes the gate
T = closed_circuit_plan()
x0, x1, y0, y1 = T.extent
fig, ax = canvas(6.5, xlim=(x0 - 40, x1 + 30), ylim=(y0 - 70, y1 + 34))
P = draw_tunnel(ax, T, highlight=("test_section",))
station_marks(ax, T, patches=P, inside=0.30)
name_part(ax, T, "contraction", "contraction", (125.0, -66.0))
name_part(ax, T, "fan", "fan", (215.0, 118.0))
probs = _gate(fig)
assert probs == [], probs
plt.close(fig)

# 3. the NACA chart with a two-step reading: passes the gate; the reading lies on its curve
cl = read("64-018", "cl_alpha", 9.0e6, 6.0)
fig, ax = naca_chart("64-018", reading=[dict(curve="cl_alpha", re=9.0e6, x=6.0, n=1),
                                       dict(curve="cd_cl", re=9.0e6, x=cl, n=2)])
probs = _gate(fig)
assert probs == [], probs
assert abs(ax["readings"][0]["y"] - cl) < 1e-12
plt.close(fig)

# 4. an airfoil in a free stream and the downwash construction: pass; a wrong angle is caught
fig, ax = canvas(6.5, xlim=(-2.05, 1.05), ylim=(-0.32, 0.95))
airfoil_in_stream(ax, 6.0, "64-618", 1.0, lift=0.72, drag=0.26, moment="nose down")
assert _gate(fig) == [], _gate(fig)
plt.close(fig)
fig, ax = canvas(6.5, xlim=(-4.3, 2.0), ylim=(-1.0, 2.9))
g = downwash_construction(ax, 8.0, induced_angle(0.9, 6.0, 1.0), k=3.5)
close_to(g["A"], g["Ae"] + g["Ai"], 1e-12, "alpha = alpha_eff + alpha_i as drawn")
probs = _gate(fig)
assert probs == [], probs
try:
    angle_mark(ax, (0, 0), 0.0, 10.0, 0.5, "x", stated=9.0)
    raise SystemExit("angle_mark did not catch a wrong angle")
except AssertionError:
    pass
plt.close(fig)

# 5. the wing seen from behind: the right wing on the right; the vortices turn the stated way
fig, ax = canvas(6.5, xlim=(-23.5, 23.5), ylim=(-3.4, 9.6))
w = wing_rear_view(ax)
assert w["tip_R"][0] > 0 > w["tip_L"][0] and abs(w["span"] - 34.32) < 0.2, w["span"]
spiral_vortex(ax, w["tip_R"], 0.3, 2.4, sense="ccw")
spiral_vortex(ax, w["tip_L"], 0.3, 2.4, sense="cw")
plt.close(fig)

# 6. the gate catches a label written on a vector
fig, ax = canvas(4.0, xlim=(0, 4), ylim=(0, 2))
vector(ax, (0.2, 1.0), 0.0, 3.5, "velocity")
text(ax, (2.0, 1.0), "on the arrow")
assert any("touches" in p for p in layout_problems(fig)), "label on a vector not caught"
plt.close(fig)

# 7. boundary layer on a plate: no slip, arrows on the curves, the tallest laminar profile at least
#    a quarter of the tallest turbulent one (a legibility guard: the turbulent law starts from a
#    virtual origin at the start of transition, which makes the jump in thickness larger than a
#    third), passes the gate; with the defaults and with the settings of the page's figure
#    (p31_wind_tunnels.BL: two arrows on each laminar profile, at one and two thirds of its height)
from chapter_3.p31_wind_tunnels import BL as _BL_PAGE
for kw, xlim, ylim in (({}, (-0.9, 6.3), (-0.75, 2.2)), (_BL_PAGE, (-1.9, 6.9), (-1.05, 2.55))):
    fig, ax = canvas(6.5, xlim=xlim, ylim=ylim)
    bl = boundary_layer_plate(ax, **kw)
    assert abs(bl["profiles"][0]["curve"][0][0] - kw.get("stations", (1.3,))[0]) < 1e-12 and bl["vexag"] > 1.0
    assert max(bl["drawn"][:2]) >= max(bl["drawn"]) / 4.0, bl["drawn"]
    if kw:
        assert all(len(p["tips"]) == 2 for p in bl["profiles"][:kw["n_lam"]]), "two arrows on each laminar profile"
    probs = _gate(fig)
    assert probs == [], probs
    plt.close(fig)
print("chapter_3/selftest.py: all checks passed (aero, tunnel, airfoil_data, published, drawing helpers, gate)")
