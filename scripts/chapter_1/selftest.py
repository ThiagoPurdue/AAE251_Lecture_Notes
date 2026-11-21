#!/usr/bin/env python3
"""Every unit check of the Chapter 1 shared code, in one run. From the book folder:

    python3 -B scripts/chapter_1/selftest.py

Runs the checks of constants.py, atmosphere.py, flow.py, sizing.py, geometry.py, aircraft.py and
launchers.py, then checks the drawing and diagram helpers against the layout gate: a flow chart, a
matrix and a labeled vehicle drawn with the helpers must pass it, and the gate must catch an
arrow routed through a box. Nothing is written to the book.
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.dont_write_bytecode = True

for name in ("constants", "atmosphere", "flow", "sizing", "geometry", "aircraft", "launchers"):
    runpy.run_path(str(HERE / f"{name}.py"), run_name="__main__")

from chapter_1.common import *  # noqa: E402,F403


def _gate(fig):
    return layout_problems(fig) + pixel_problems(fig)


# a small flow chart: a column, a decision, a loop
fig, ax = new_axes(5.0, 5.0)
set_frame(ax, 0.0, 10.0, 0.0, 10.0)
bs = column(ax, ["Define the mission", "Guess the takeoff weight", "Compute a new takeoff weight"], 4.0, 9.6, 5.0)
w, h, _ = decision_size(ax, "Close to the guess?", w=4.4)
d = decision(ax, (4.0, bs[-1].cy - bs[-1].h / 2 - pt(ax, 18) - h / 2), "Close to the guess?", w=4.4)
for a, b in zip(bs[:-1], bs[1:]):
    route(ax, a, "bottom", b, "top")
route(ax, bs[-1], "bottom", d, "top")
route(ax, d, "right", bs[1], "right", via=[("x", 8.6)], label="no", label_at=0.08)
for i, b in enumerate(bs):
    step_marker(ax, None, i + 1, beside=b)
probs = _gate(fig)
assert probs == [], probs
plt.close(fig)

# the gate catches an arrow routed through a box
fig, ax = new_axes(5.0, 2.0)
set_frame(ax, 0.0, 10.0, 0.0, 4.0)
a = box(ax, (1.5, 2.0), "A", w=2.0)
m = box(ax, (5.0, 2.0), "B", w=2.0)
c = box(ax, (8.5, 2.0), "C", w=2.0)
route(ax, a, "right", c, "left")
assert any("routed arrow crosses" in p for p in layout_problems(fig)), "an arrow through a box must fail"
plt.close(fig)

# a matrix with headers
fig, ax = new_axes(4.0, 3.0)
set_frame(ax, -1.5, 5.5, -1.0, 4.25)
mt = matrix(ax, (0.0, 0.0), [["1", "2"], ["3", "4"]], 1.2, 0.9, ["row 1", "row 2"], ["A", "B"],
            fills=[["white", RISK_STYLE["High"]["fill"]], [None, None]],
            hatches=[[None, RISK_STYLE["High"]["hatch"]], [None, None]])
assert len(mt) == 4
probs = _gate(fig)
assert probs == [], probs
plt.close(fig)

# a labeled vehicle: leaders may cross only the outlines that contain their end
parts = aircraft_top()
fig, ax = new_axes(5.0, 4.0)
P = draw_parts(ax, parts)
ax.set_xlim(-2, 48)
ax.set_ylim(-19, 19)
label_part(ax, P, parts, "aileron_R", "aileron", at=(31.0, 15.5), ha="left")
probs = _gate(fig)
assert probs == [], probs
label_part(ax, P, parts, "spoiler_R", "spoiler", at=(10.0, 13.0), ha="right")   # its leader crosses the slat
assert any("leader of 'spoiler' crosses" in p for p in layout_problems(fig)), "a leader across another part must fail"
plt.close(fig)

# details drawn on a part: a leader to the fuselage may cross its windows and doors, a leader
# to the wing may not cross a door it does not end in... unless the door is on a part holding the end
parts = aircraft_side(ground=False)
fig, ax = new_axes(6.0, 2.6)
ax.set_xlim(-1, 41)
ax.set_ylim(-1, 14)
P = draw_parts(ax, parts)
label_part(ax, P, parts, "fuselage", "fuselage", at=(3.0, 9.6), target=(7.0, 3.3))
probs = _gate(fig)
assert probs == [], probs
plt.close(fig)
# the cutaway: a leader to a hidden tank crosses the stage outline and other hidden lines of that stage
parts = launch_vehicle(cutaway=True)
fig, ax = new_axes(4.0, 6.0)
ax.set_xlim(-21, 21)
ax.set_ylim(-2, 55)
P = draw_parts(ax, parts)
label_part(ax, P, parts, "payload", "payload", at=(6.0, 46.0), ha="left")
probs = _gate(fig)
assert probs == [], probs
plt.close(fig)
# every view keeps the published dimensions together (one scale)
v = three_view()
assert abs(max(p.xy[:, 0].max() for p in v["front"].values()) - min(p.xy[:, 0].min() for p in v["front"].values())
           - 35.79 - 2.0) < 0.05

print("chapter_1 selftest: all unit checks passed")
