# Chapter 5 figure and value code

Shared code for the pages of Chapter 5, Aircraft Performance and Propulsion. One module per page,
`p5N_<slug>.py`, with one function per figure, `make_all()` and `values()`. Every page module starts
with the one import line

```python
from chapter_5.common import *
```

Run from the book folder (in a scratch copy outside OneDrive):

```bash
python3 -B scripts/make_chapter_5_figures.py              # all pages: figures, then values.json
python3 -B scripts/make_chapter_5_figures.py p51          # one page
python3 -B scripts/render_svg.py notes/chapter-5/figures/p51-*.svg --out <folder> --scale 1.6 --gray
python3 -B scripts/check_values.py p51 [--strict]
python3 -B scripts/chapter_5/perf.py                      # unit checks of the physics module
```

## Modules

| Module | What it holds |
|---|---|
| `style.py` | Chapter 5's `record`, `write_values`, `save_figure` (`figkit.Chapter` for `notes/chapter-5`), `PAGES` (`p51` thrust-and-power, `p52` range-and-endurance, `p53` climb-and-ceiling, `p54` engines, `p55` constraint-diagram-and-field-length), and multi-letter subscript sizing (`_WORD_SUB`). |
| `perf.py` | Steady level flight (`thrust_required_parts`, `power_required_parts`, `thrust_available`, `power_available`, `min_thrust_condition`, `min_power_condition`, `jet_speed_bounds`, `prop_vmax`), Breguet range and endurance (`jet_range`, `jet_endurance`, `prop_range`, `prop_endurance`, fuel-mass solvers), climb and ceiling (`climb_jet`, `climb_prop`, `jet_max_climb_angle`, `jet_max_roc`, `prop_max_roc`, analytical and numerical ceilings), constraint diagram and field length (`takeoff_ground_roll`, `landing_ground_roll`, `tw_*_line`), and jet propulsion (`jet_thrust_eq`, `propulsive_efficiency`). Uses `G0 = 9.81 m/s^2` and `chapter_1.atmosphere.standard`. |
| `drawing5.py` | `aircraft_silhouette_right` (Boeing 737-800 side outline facing right, pitched by `pitch_deg`), and engineering cutaways `draw_turbojet`, `draw_turbofan`, `draw_turboprop`, `draw_ramjet`. |
| `common.py` | The one import line for page modules. |

## Sources of the shared constants

- Standard atmosphere and `G0 = 9.81 m/s^2`: `chapter_1/atmosphere.py` (Anderson 1999, Appendix D, 1959 ARDC model).
- Performance and propulsion equations: Anderson, *Introduction to Flight*, 8th ed. (2016), Chapters 6 and 9; Raymer, *Aircraft Design: A Conceptual Approach*, 4th ed. (2006), Chapters 5 and 17; NASA Glenn Research Center, Beginner's Guide to Propulsion.
