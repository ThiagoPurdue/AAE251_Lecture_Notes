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
python3 -B scripts/chapter_5/selftest.py                  # unit checks of perf.py, vehicles.py and looks.py
```

## Modules

| Module | What it holds |
|---|---|
| `style.py` | Chapter 5's `record`, `write_values`, `save_figure` (`figkit.Chapter` for `notes/chapter-5`), `PAGES` (`p51` thrust-and-power, `p52` range-and-endurance, `p53` climb-and-ceiling, `p54` engines, `p55` constraint-diagram-and-field-length), and multi-letter subscript sizing (`_WORD_SUB`). |
| `perf.py` | Steady level flight (`thrust_required_parts`, `power_required_parts`, `thrust_available`, `power_available`, `min_thrust_condition`, `min_power_condition`, `jet_speed_bounds`, `prop_vmax`), Breguet range and endurance (`jet_range`, `jet_endurance`, `prop_range`, `prop_endurance`, fuel-mass solvers), climb and ceiling (`climb_jet`, `climb_prop`, `jet_max_climb_angle`, `jet_max_roc`, `prop_max_roc`, analytical and numerical ceilings), constraint diagram and field length (`takeoff_ground_roll`, `landing_ground_roll`, `tw_*_line`), and jet propulsion (`jet_thrust_eq`, `propulsive_efficiency`). Shared by several pages (the end of the file): `lift_line`, `alpha_for_CL`, `level_flight_at_speed`, `level_flight_at_alpha`, `thrust_required_vs_alpha`, `trim_elevator`, `level_speed_range`, `climb_required`, `climb_hodograph`. Each section of the file has one owner (its docstring says which). Uses `G0 = 9.81 m/s^2` and `chapter_1.atmosphere.standard`. |
| `drawing5.py` | `aircraft_silhouette_right` (Boeing 737-800 side outline facing right, pitched by `pitch_deg`), and the engine sections of page 5.4 in the look of Chapter 4's engine figures: `draw_turbojet_section` (proportions after the General Electric CJ610, FAA type certificate data sheet 1E16), `draw_turbofan_section` (CFM56-7B, EASA type-certificate data sheet E.004), `draw_turboprop_section` (Rolls-Royce AE 2100D2, EASA type-certificate data sheet IM.E.040), with `engine_centerline`, `contour`, the helpers `_wall`, `_row`, `_body`, `_shaft`, `_liner`, `_lip_wall`, `_outline`, the `*_STAGES` constants, and the options `core_only=` (the enlarged half section of the core) and `sides=` (a full or a half section); the turboprop gearbox is a sketch of gears on the axis. |
| `vehicles.py` | The chapter's aircraft, one source for their data: `EXEC_JET` (twin-engine executive jet, pages 5.1 to 5.4), `GA_AIRPLANE` (single-engine general-aviation airplane, the propeller example of 5.1 and 5.2, with its lift curve and pitching-moment line), `TRANSPORT` (four-engine turboprop transport, invented for the chapter and used on page 5.3: its ceiling, and one engine out leaving three; it also carries a lift curve and a pitching-moment line that no page uses), `LIGHT_TWIN` and `LIGHT_TWIN_REQ` (light twin-jet and its requirements, the constraint-diagram page). Helpers `weight(ac)`, `available(ac, rho, n=None, delta_t=1.0)` (thrust or power available by engine kind), `power_sfc_per_m(ac)` (g/(s kW) to the weight-based c in 1/m). Each value says where it comes from; the sign convention of the pitching moment is stated at the top. |
| `looks.py` | The chapter's figure look: `required_kw(cond)` (solid, thick), `available_kw(cond)` (dashed, the same color), `COND_COLOR` (black, blue, vermilion for a first, second, third condition) and `cond_marks` (open triangles along a second condition, so it reads in grayscale), `part_kw("parasite" or "induced")`, `draw_curve(x_valid=)` (thin past the Mach limit), `stall_band`, `mach_band`, `mark_minimum` (filled circle), `tangent_from_origin` (thin dashed line from the marked origin, open square), `mark_limit` (filled diamond, drop line), `panel_title`, `on_curve`, `CONSTRAINT_STYLE` with `constraint_line` and `constraint_vertical`, and the force diagrams `level_forces`, `climb_forces` (forces to one scale, asserted in balance, drawn on their lines of action), `weight_split` (as page 4.2) and `velocity_triangle` (`rides=` names the line each arrow is drawn on, for the layout gate). The drawing constants of the two force figures, `ALPHA_DRAWN`, `GAMMA_DRAWN`, `LD_DRAWN`, `W_DRAWN`, `AC_LENGTH`, `SCALE_IN_PER_UNIT` and `INSET`, live here, so the level-flight figure of 5.1 and the climb figure of 5.3 share one scale. |
| `p51_thrust_and_power.py` to `p55_constraint_diagram_and_field_length.py` | One page each: `values()` computes every number of the worked examples, and each figure function states its lesson in its docstring and asserts what it draws. Page 5.1: 9 figures; 5.2: 5; 5.3: 9; 5.4: 6; the no-standard page: 5. |
| `selftest.py` | Unit checks of `perf.py` (on a test aircraft printed on no page), of the functions shared by several pages, of the look (balance of the force diagrams, contrast, distinct styles), and of the aircraft data against the published numbers of their examples. |
| `common.py` | The one import line for page modules; it brings `vehicles.py` and `looks.py` too (they shadow no earlier name). |

## Sources of the shared constants

- Standard atmosphere and `G0 = 9.81 m/s^2`: `chapter_1/atmosphere.py` (Anderson 1999, Appendix D, 1959 ARDC model).
- Performance and propulsion equations: Anderson, *Introduction to Flight*, 8th ed. (2016), Chapters 6 and 9 (cited by chapter); Raymer, *Aircraft Design: A Conceptual Approach*, 6th ed. (2018), Chapters 5 and 17; Leishman, *Introduction to Aerospace Flight Vehicles* (Embry-Riddle, 2022), Chapters 40 and 45 to 47; NASA Glenn Research Center, Beginner's Guide to Propulsion; FAA, *Pilot's Handbook of Aeronautical Knowledge*, FAA-H-8083-25C (2023), Chapters 5 and 11.
- Engine drawings of page 5.4: FAA type certificate data sheet 1E16, General Electric CJ610, revision 15 (2008); EASA type-certificate data sheets E.004 (CFM56-7B, issue 07, 2023) and IM.E.040 (Rolls-Royce AE 2100, issue 01, 2008).
- Regulations: 14 CFR 25.113 and 25.125 (field-length heights and the approach speed, the no-standard page) and 25.121(b) (climb gradients with one engine out, page 5.3).
