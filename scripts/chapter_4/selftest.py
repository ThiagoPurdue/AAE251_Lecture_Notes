#!/usr/bin/env python3
"""Every unit check of the Chapter 4 shared code, in one run. From the book folder:

    python3 -B scripts/chapter_4/selftest.py

Runs the checks of rocket.py, staging.py, nozzle.py, published.py and links.py, then checks the
drawing helpers of drawing4.py against the layout gate: a thrust chamber in section with its parts
named, the three plumes, pressure arrows on a wall, mass bars with braces, a stack of stages, the engine
schematics, tanks inside a stage and a temperature scale must pass the gate; the helpers' own asserts
must catch a wrong area ratio, a mass bar that does not add up and a tank that does not fit; and the
gate must catch a leader into one engine part that crosses another part's wall. Nothing is written to
the book.
"""
import math
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.dont_write_bytecode = True

for name in ("rocket", "staging", "nozzle", "published", "links"):
    runpy.run_path(str(HERE / f"{name}.py"), run_name="__main__")

from chapter_4.common import *  # noqa: E402,F403
import figkit  # noqa: E402
import chapter_1.atmosphere as _atm  # noqa: E402
import chapter_4.rocket as _rk  # noqa: E402


def _gate(fig):
    return layout_problems(fig) + pixel_problems(fig)


# 1. one g, the chapter's own record, the word-subscript size, Chapter 2 keeps its own record
assert _atm.G0 == _rk.G0 == G0 == 9.81, (_atm.G0, _rk.G0, G0)
assert record.__self__.number == 4 and save_figure.__self__.number == 4 and PAGES["p45"] == "engines-and-tanks"
import chapter_1.style as _c1  # noqa: E402
assert _c1.record.__self__.number == 1, "Chapter 1 keeps its own record"
import chapter_2.orbits as _o2  # noqa: E402
assert _o2.record.__self__.number == 2 and not _o2.VALUES, "the bridge records nothing in Chapter 2's record"
for s in (r"$I_\mathrm{sp}$", r"$m_{pay}$", r"$f_\text{inert}$", r"$p_e < p_a$", r"Area ratio, $A_e/A_t$"):
    assert figkit._WORD_SUB.search(s), s
assert not figkit._WORD_SUB.search(r"$V_e$"), "a single one-letter subscript keeps mathtext's size"

# 2. the bridge: page 2.2's transfer and page 2.3's budget as printed
assert fmt(HOHMANN_22["dv1"]) == "2.012" and fmt(HOHMANN_22["dv2"]) == "1.404" and fmt(HOHMANN_22["dv_total"]) == "3.416"
assert fmt(LAUNCH_23["total"]) == "8.833"
close_to(float(hohmann(MU["Earth"], HOHMANN_22["r1"], HOHMANN_22["r2"])["dv_total"]), HOHMANN_22["dv_total"], 1e-12,
         "bridge function = bridge number")

# 3. a thrust chamber in section (F-1 proportions), every part named: passes the gate
F1S = engine_si(F1)
tc = thrust_chamber(0.5 * F1S["throat_d"], F1["area_ratio"])
close_to(tc["r_e"] ** 2 / tc["r_t"] ** 2, 16.0, 1e-9, "F-1 area ratio as drawn")
st = tc["stations"]
assert st["injector"] < st["chamber_end"] < st["throat"] < st["exit"]
fig, ax = canvas(6.5, xlim=(-2.4, 5.4), ylim=(-2.6, 2.9))
P = draw_thrust_chamber(ax, tc)
name_station(ax, tc, P, "injector", "injector", (-1.6, 1.6), target=(st["injector"] - 0.06, 0.42))
name_station(ax, tc, P, "chamber", "combustion\nchamber", (-0.45, 2.3), target=(0.5 * (st["injector"] + st["chamber_end"]), 0.3))
name_station(ax, tc, P, "throat", "throat", (0.7, -1.6), target=(0.0, -0.15))
probs = _gate(fig)
assert probs == [], probs
# the gate catches a leader that ends outside the engine and crosses its wall
callout(ax, (2.0, 2.6), "outside", at=(2.0, -0.5)).arrow_patch.set_gid("leader")
assert any("leader" in p for p in layout_problems(fig)), "a leader across the wall to a point outside was not caught"
plt.close(fig)
try:
    chamber_contour(0.44, 16.0, contraction_ratio=1.01)
    raise SystemExit("chamber_contour accepted a chamber narrower than its throat arc")
except ValueError:
    pass

# 4. the three plumes, in the chapter's order, with pressure arrows on the boundary: pass the gate
fig, ax = canvas(6.5, xlim=(-1.0, 6.4), ylim=(-5.4, 1.0))
for k, state in enumerate(EXPANSION_STATES):
    y = -2.0 * k
    t = thrust_chamber(0.18, 9.0, origin=(0.0, y))
    draw_thrust_chamber(ax, t, axis=False)
    pl = plume(ax, (t["stations"]["exit"], y), t["r_e"], state, 2.8)
    assert (pl["r_at_one_radius"] > t["r_e"]) == (state == "underexpanded")
probs = _gate(fig)
assert probs == [], probs
plt.close(fig)
try:
    plume(plt.gca(), (0, 0), 1.0, "perfectly expanded", 3.0)
    raise SystemExit("plume accepted an unknown state")
except ValueError:
    plt.close("all")

# 5. pressure arrows normal to a wall, tips on it
fig, ax = canvas(4.0, xlim=(0, 4), ylim=(0, 2))
ax.plot([0.5, 3.5], [0.8, 0.8], color=INK, lw=1.4)
arrs = pressure_arrows(ax, [(0.5, 0.8), (3.5, 0.8)], n=5, side=1)
for a, b in arrs:
    assert abs(b[1] - 0.8) < 1e-12 and a[1] > b[1] and abs(a[0] - b[0]) < 1e-12, (a, b)
assert _gate(fig) == [], _gate(fig)
plt.close(fig)

# 6. mass bars: a bar adds up; two bars share a scale; braces; a key; a wrong total is caught
s = size_stage(1750.0, 3416.0, isp=323.0, f_inert=0.17)
fig, ax = canvas(6.5, xlim=(-0.4, 10.2), ylim=(-2.6, 2.0))
sc = 9.6 / s["m_i"]
b = mass_bar(ax, (0.0, 0.4), [("payload", 1750.0), ("inert", s["m_inert"]), ("propellant", s["m_prop"])], sc, 0.95,
             total=s["m_i"])
close_to(b["end"][0], s["m_i"] * sc, 1e-9, "bar length")
mass_braces(ax, b, [(0, 1, "$m_f$"), (0, 2, "$m_i$")], side=-1, step=24.0)
mass_key(ax, (0.0, -2.2))
probs = _gate(fig)
assert probs == [], probs
try:
    mass_bar(ax, (0.0, -1.5), [("payload", 1.0), ("propellant", 2.0)], sc, 0.3, labels=False, total=4.0)
    raise SystemExit("mass_bar did not catch a total that does not add up")
except AssertionError:
    pass
plt.close(fig)

# 7. a stack of stages with braces "payload of stage k": passes the gate
fig, ax = canvas(4.0, xlim=(-2.5, 3.5), ylim=(-0.5, 9.5))
S = stage_stack(ax, [dict(length=4.0), dict(length=2.2)], dict(length=1.2, name="payload"), origin=(0.0, 0.0), width=1.2)
y1 = S["joints"][0]
brace(ax, (0.95, S["top"]), (0.95, y1), "payload of stage 1", side=1)
assert S["spans"][0][1] == y1 and len(S["joints"]) == 2
probs = _gate(fig)
assert probs == [], probs
plt.close(fig)

# 8. the engine schematics, parts named with leaders: pass the gate
fig, ax = canvas(6.0, xlim=(-2.4, 12.9), ylim=(-0.3, 9.4))
L, Sm, H = liquid_engine("pressure", origin=(0.0, 0.0)), solid_motor(origin=(5.6, 0.0)), hybrid_motor(origin=(10.2, 0.0))
PL, PS, PH = draw_schematic(ax, L), draw_schematic(ax, Sm), draw_schematic(ax, H)
label_part(ax, PL, L["parts"], "pressurant", "pressurant", (-1.8, 7.9), ha="center")
label_part(ax, PL, L["parts"], "thrust_chamber", "thrust\nchamber", (1.8, 1.2), ha="center")
label_part(ax, PS, Sm["parts"], "grain", "propellant", (3.7, 2.55), ha="center", target=(5.6 - 0.45, 3.3))
label_part(ax, PH, H["parts"], "grain", "solid fuel", (12.05, 3.1), ha="center", target=(10.6, 3.0))
probs = _gate(fig)
assert probs == [], probs
plt.close(fig)

# 9. tanks inside a stage, to scale: volumes held; a tank too large for the stage is caught
fig, ax = canvas(4.0, xlim=(-3.2, 3.4), ylim=(-0.5, 5.6))
T = tanks_in_stage(ax, 3.0, [dict(name="fuel", volume=4.0, ullage=0.05, style="fuel"),
                             dict(name="oxidizer", volume=7.5, ullage=0.05, style="oxidizer")])
for t in T["tanks"].values():
    close_to(math.pi / 6.0 * t["D"] ** 3, t["V_tank"], 1e-9 * t["V_tank"], "sphere volume")
assert _gate(fig) == [], _gate(fig)
try:
    tanks_in_stage(ax, 1.0, [dict(name="big", volume=4.0, ullage=0.05, style="fuel")])
    raise SystemExit("tanks_in_stage did not catch a tank wider than the stage")
except AssertionError:
    pass
plt.close(fig)

# 10. a temperature scale in kelvin and degrees Celsius, and the log axes of the range charts
fig, ax = data_axes(4.0, 4.0)
sec = temperature_axis(ax, 0.0, 400.0, 50.0)
ax.set_xlim(0, 1)
ax.set_xticks([])
for name, Tb in (("hydrogen", NIST["hydrogen"]["Tb"]), ("oxygen", NIST["oxygen"]["Tb"])):
    ax.axhline(Tb, color=INK, lw=1.4)
    text(ax, (0.5, Tb), name, direction=90.0, dist=3.0, fs=FS_SMALL)
fig.canvas.draw()
assert abs(sec.get_ylim()[0] + 273.15) < 1e-6, sec.get_ylim()
assert _gate(fig) == [], _gate(fig)
plt.close(fig)
fig, ax = data_axes(6.5, 4.4)
log_axis(ax, "x", 1e-5, 1e8, "power", "Thrust, $F$, N")
log_axis(ax, "y", 20.0, 20000.0, "comma", "Specific impulse, s")
items = [dict(name=k[0], x0=k[3], x1=k[4], y0=k[1], y1=k[2]) for k in PROPULSION_KINDS[:2]]
items[1].update(callout=(4e-3, 140.0), target=(1.0, 240.0), ha="left")      # a label outside, with a leader
patches, labels = range_boxes(ax, items)
assert len(patches) == 2 and all(lb is not None for lb in labels)
assert _gate(fig) == [], _gate(fig)
plt.close(fig)
print("chapter_4/selftest.py: all checks passed (rocket, staging, nozzle, published, links, drawing helpers, gate)")
