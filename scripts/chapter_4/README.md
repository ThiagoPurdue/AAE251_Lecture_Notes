# Chapter 4 figure and value code

Shared code for the pages of Chapter 4, Rocket Design. One module per page, `p4N_<slug>.py` (for
example `p42_rocket_equation.py`), with one function per figure, `make_all()` and `values()`. Every
page module starts with the one import line

```python
from chapter_4.common import *
```

and never types a constant: every constant is in a shared module, with its source.

```bash
python3 -B scripts/make_chapter_4_figures.py              # every page module: figures, then values.json
python3 -B scripts/make_chapter_4_figures.py p42          # one page (values.json keeps the others)
FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_4_figures.py p42   # also matplotlib PNG previews
FIG_LAYOUT=warn ...                                       # draft mode: list every layout problem, save anyway
python3 -B scripts/render_svg.py notes/chapter-4/figures/p42-*.svg --out <folder> --scale 1.5 --gray   # look in Chrome
python3 -B scripts/check_values.py p42 [--strict]         # every recorded number is on its page
python3 -B scripts/chapter_4/selftest.py                  # every unit check of the shared code
```

Run a page module through the runner, never directly (a second import path makes a second copy of
the value record). A run of one page renumbers the SVG group ids of that page's figures; a run of
the whole chapter gives the files that are kept.

## Modules

| Module | What it holds |
|---|---|
| `style.py` | Chapter 4's `record`, `write_values`, `save_figure` (a `figkit.Chapter` for `notes/chapter-4`), `PAGES` (p41 thrust-and-specific-impulse, p42 rocket-equation, p43 multistage-rockets, p44 propellant-selection, p45 engines-and-tanks). It also sets word subscripts and labels with two subscripts at the kit's word-subscript size (see "The gate"), and holds `printed(x, sig)`, the printed string of a number with the value a reader takes from it, so a worked step uses the digits shown |
| `rocket.py` | Thrust and the rocket equation (SI units): `thrust`, `thrust_parts`, `air_breathing_thrust`, `effective_exhaust_velocity`, `isp_from_c`, `c_from_isp`, `isp_from_thrust`, `mass_flow`, `expansion_state` (and `EXPANSION_STATES`, the order of every figure), `exit_area_from_thrusts`, `diameter_from_area`, `area_from_diameter`, `ambient_pressure` (page 1.4's atmosphere, 0 to 59.5 km), `fixed_nozzle_thrust`, `fixed_nozzle_isp`; `delta_v`, `mass_ratio`, `propellant_share`, `final_mass`, `inert_mass_fraction`, `inert_from_prop`, `size_stage`, `stage_factor`, `single_stage_limit`, `stage_delta_v`, `gravity_loss_constant_angle`, `StageLimitError`; `G0` (9.81 m/s², from page 1.4's code) |
| `staging.py` | `size_stages` (top down, any number of stages, lists in stage order, stage 1 first), `identical_stages`, `identical_limit`, `split_mass`, `split_sweep` (nan past a limit), `best_split` (asserts the best-split condition), `split_condition` |
| `nozzle.py` | The ideal nozzle for a ratio of specific heats `g`: `area_ratio_from_mach`, `mach_from_area_ratio` (either branch), `pressure_ratio`, `temperature_ratio`, `critical_pressure_ratio`, `area_ratio_from_pressure_ratio`, `pressure_ratio_from_area_ratio`, `exit_velocity`, `characteristic_velocity`, `thrust_coefficient`, `ideal_isp`, `ideal_area_ratio`, `separation_area_ratio` (`SEPARATION_PE_PA` = 0.4), `matching_gamma`, `nozzle_flow`; the 80-percent bell (`bell_angles`, `bell_length`, `BELL_80_ANGLES`) |
| `published.py` | Every published number the pages may print, each with its source (below) |
| `links.py` | The bridge to numbers the book has already printed: `HOHMANN_22`, `LAUNCH_23`, `ARIANE5_FLIGHT`, `ARIANE5_CORE`, and Chapter 2's `circular_speed`, `hohmann`, `MU`, `RADIUS`; `km_as_printed` (a delta-V printed in km/s, in m/s from its printed digits); `TRANSFER_STAGE`, the stage of worked example 2 of page 4.2 that page 4.3 splits into two |
| `drawing4.py` | The drawing helpers (below) |
| `common.py` | The import line: Chapter 1's style, constants, atmosphere, flow, geometry, launchers, drawing and diagrams, Chapter 3's `disc`, `vector`, `step_label`, `unit`, `data_per_pt`, then all of the above |
| `selftest.py` | Every unit check of these modules plus gate checks of the helpers |

## A page module

```python
from chapter_4.common import *      # first line of scripts/chapter_4/p4N_<slug>.py
PAGE = "p42"
def example_stage(): ...; save_figure(fig, "p42-example-stage")
def make_all(): example_stage()
def values():
    s = size_stage(1750.0, 3416.0, isp=323.0, f_inert=0.17)
    record(PAGE, "ex2-mprop", fmt(s["m_prop"]))
```

`record(page, key, text)` takes the printed string (`fmt(x)`, `fmt_dec`, `fmt_sci`) and returns it;
recording a key twice with different text stops the run; `values()` must record every number the
page prints, and `scripts/check_values.py --strict` then requires each on the page while
`scripts/check_chains.py` recomputes every printed step from the digits printed before it. An
exponential magnifies rounding: print `x = dV/c` and `e^x` to five figures where the next step
divides by `1 - f e^x`, and compute the following steps from the printed values, so the chain closes.
When a delta-V comes from Chapter 2 in km/s, convert the printed value (3.416 km/s is 3,416 m/s) and
size with that: the full-precision 3,415.9 m/s gives 5,628 kg of propellant where the page's own
numbers give 5,629 kg.

## The bridge to Chapters 1 and 2

`links.py` imports `chapter_2.orbits` under a private name and reads the inputs of the worked
examples of pages 2.2 and 2.3 from their page modules; it records nothing in Chapter 2's record and
exports only numbers and pure functions. Each number is asserted equal to the string the earlier page
prints (its `values.json`), so a change there stops the run.

| Name | Holds |
|---|---|
| `HOHMANN_22` | the transfer of page 2.2: `h1`, `h2` (400 and 20,200 km), `r1`, `r2`, `dv1` 2.012, `dv2` 1.404, `dv_total` 3.416 km/s |
| `LAUNCH_23` | the launch of page 2.3: `v_orbit` 7.589, `losses` 1.6, `rotation` 0.3559, `total` 8.833 km/s (`lat`, `h`, `inc`) |
| `ARIANE5_CORE` | the core stage of page 1.3: `dry_kg` 14,700, `prop_kg` 170,000 |

## The published data (`published.py`)

Each dict stores the values as the source prints them (with its unit) and `engine_si`,
`propellant_si`, `saturn_stage_kg` give SI values.

- **Engines.** `RS25`: the Space Shuttle Main Engine at rated (100 percent) power, from the Space
  Shuttle News Reference (NASA, 1981), p. 2-4: 375,000 lbf at sea level, 470,000 lbf in vacuum, 363.2
  and 455.2 s, area ratio 77.5, chamber 2,970 psia, about 3,000 kg; exit and throat diameters 90.7 and
  10.3 in from HAER TX-116, p. 274. The two thrusts give an exit diameter of 2.304 m against 2.304 m
  published, and one mass flow, 468.2 kg/s, at both points: use this engine where a page works from a
  real engine's sea-level and vacuum data. `F1`: the F-1 fact sheet (sea-level thrust 1,522,000 lbf as
  uprated, area ratio 16, exit diameter 11 ft 7 in, chamber 965 psia) and 265 s at sea level (Biggs,
  2009); no NASA source opened gives its vacuum thrust, so the F-1 is not checked and serves only for
  its proportions. `J2`: the J-2 fact sheet (225,000 lbf and 424 s in vacuum, area ratio 27.5, exit
  6 ft 5 in). `VULCAIN2`: Ariane 5 User's Manual, p. 1-7 (960 and 1,390 kN, about 310 and 432 s); its
  rounded sea-level values do not agree with its vacuum values (the two mass flows differ by 4
  percent), so use only the vacuum ones. `engine_check(E)` gives the exit-diameter check.
- **Stages.** `SATURN_V_AS506` (Apollo 11, Orloff, Apollo by the Numbers: dry, oxidizer, fuel and
  other masses in lb; specific impulse, burn time and cutoff velocity from the AS-506 flight
  evaluation report; the S-IC's 265 s is per engine at sea level). `STAGES`: eleven real stages with
  dry and propellant masses (the three Saturn V stages, the Ariane 5 core stage, upper stage and
  booster, the Shuttle solid booster, the four Vega stages), each with its source; `STAGE_ISP_VAC`.
- **Launch vehicles.** `LAUNCH_VEHICLES`: Electron, PSLV-XL, Vega C, LVM3, Ariane 5 ES, Falcon 9,
  Space Shuttle, Falcon Heavy, SLS Block 1, Saturn V, each with payload to low Earth orbit and the
  orbit it is quoted for, liftoff mass, liftoff thrust as printed, stages, boosters, propellants and
  source. `LV_CLASSES` and `lv_class()`: small up to 2 t, medium 2 to 20 t, heavy 20 to 50 t, super
  heavy above 50 t (McConnaughey et al., NASA's Launch Propulsion Systems Technology Roadmap, p. 2).
- **Propellants.** `PROPELLANTS`: theoretical performance from NASA SP-125, Tables 1-8 to 1-10
  (chamber 1,000 psia, expanded to 14.7 psia, shifting equilibrium): oxygen and hydrogen, oxygen and
  kerosene, nitrogen tetroxide with MMH and with Aerozine 50; oxygen and methane from NACA RM E58B20
  (frozen composition, 600 psia: say so wherever it stands beside the others; its bulk density is
  computed with `bulk_density` from the NIST densities). `HYDRAZINE_MONO` (SP-125 Table 1-6, 300
  psia, frozen), `SOLID_AP_AL` (SP-8064 Table I). `NIST`: boiling point, saturated liquid density and
  heat of vaporization of oxygen, hydrogen (the values of parahydrogen, the form of stored liquid hydrogen) and methane at one atmosphere. `SP125_PROPERTIES`:
  freezing and boiling points and densities of the storables, kerosene and the cryogens (deg F, g/cc).
- **Kinds of propulsion.** `PROPULSION_KINDS`: specific-impulse and thrust ranges of cold gas,
  monopropellant, bipropellant, solid, hybrid, nuclear thermal and electric propulsion. No open source
  gives one table for all of them, so each range names its own source (NASA's State of the Art of Small
  Spacecraft Technology, Table 4-1, for small devices; the engines and motors above for large ones;
  Johnson et al., 2012, for nuclear thermal). Large hybrids are not covered.
- **Data first printed on one page.** The end of `published.py` holds the published numbers that one
  page prints and no other page uses (the Saturn V's escape tower and translunar speed for page 4.3;
  Vega, Ariane 5, Space Shuttle, NERVA and small-spacecraft data for page 4.4; External Tank, tank
  pressure, aluminum and ullage data from SP-125 for "Engines and tanks"), each with its source.

## Helpers, with an example each

| Helper | Example |
|---|---|
| `thrust_chamber(r_t, area_ratio, contraction_ratio=1.6, L_star=1.143, wall=0.12 r_t, injector=0.30 r_t, origin=(0, 0), conv_angle=30)` -> parts (wall_upper, wall_lower, injector, chamber, converging, diverging), stations, r_c, r_t, r_e, x, r, envelope; asserts the area ratio | `tc = thrust_chamber(0.4413, 16.0)` (F-1 proportions) |
| `draw_thrust_chamber(ax, tc, highlight=(), axis=True, exit_plane=True)` -> patches; `name_station(ax, tc, P, name, text, at, target=None)` (name: a part, "throat" or "exit plane") | `name_station(ax, tc, P, "chamber", "combustion\nchamber", (-0.45, 2.15))` |
| `chamber_contour(...)` the inner contour alone (x, r, stations) | `nozzle_flow((c["r"] / c["r_t"])**2, c["i_throat"], 1.2, Tc, M)` |
| `plume(ax, exit_xy, r_exit, state, length, shocks=True)` -> upper, lower, s, r, shocks; asserts inside, on or outside one radius downstream | `plume(ax, (xe, 0), Re, "overexpanded", 3.0)` |
| `pressure_arrows(ax, xy, n=6, length=14, side=1, inward=True)` -> [(base, tip)] | `pressure_arrows(ax, [(x0, h), (x1, h)], n=6)` |
| `arrow_key(ax, xy, [(kind, name)])` (kinds of Chapter 1 and "pressure") | `arrow_key(ax, xy, [("pressure", "pressure"), ("force", "force"), ("flow", "flow")])` |
| `mass_bar(ax, origin, segments, scale, height, orientation="horizontal", labels=True, label_at=None, two_lines=True, total=None)` -> patches, spans, end, total | `mass_bar(ax, (0, 0), [("payload", 1750), ("inert", 1153), ("propellant", 5629)], 9.6/8531, 0.95)` |
| `mass_braces(ax, bar, [(i0, i1, label)], side=-1, step=16)`; `mass_key(ax, xy)` | `mass_braces(ax, b, [(0, 1, "$m_f$"), (0, 2, "$m_i$")], step=30)` |
| `stage_stack(ax, stages, payload=None, origin, width=1.0)` -> patches, joints, spans, top, bottom | `stage_stack(ax, [dict(length=4), dict(length=2.2)], dict(length=1.2, name="payload"))` |
| `aligned_axes(width, xlim, ylim_draw, plot_height)` -> fig, ax_plot, ax_draw (one horizontal scale, asserted) | `fig, ap, ad = aligned_axes(6.5, xlim, (-0.06, 1.9), 2.6)` |
| `liquid_engine(feed="pump" or "pressure", origin, size=1)`, `solid_motor(origin)`, `hybrid_motor(origin)` -> schematic dicts; `draw_schematic(ax, S)` -> patches; name parts with `label_part(ax, P, S["parts"], name, text, at)` | page-4.4 engine kinds |
| `log_axis(ax, "x", lo, hi, "comma" or "power", label)`; `range_boxes(ax, items)` (items: name, x0, x1, y0, y1, optional `label_at` or `callout` and `target`); `class_bands(ax, classes, label_x=, ha=)`; `named_scatter(ax, points)` (points: name, x, y, optional `label_at`); `place_labels(ax, requests)` | the specific impulse against thrust map; the launch-vehicle chart |
| `fill_region(ax, xy, style, z=3.0, edge_lw)`: a tinted and hatched region with a black outline, in the look of the chapter's tanks and mass bars, for a shape a page draws itself | `fill_region(ax, [(0, 0), (2, 0), (2, 1), (0, 1)], LIQUID_STYLE["oxidizer"])` |
| `tanks_in_stage(ax, stage_d, tanks, origin)` (tanks: name, volume, ullage, style; ullage is the gas space added to the liquid volume as a fraction of it) -> tanks (center, D, level, V_tank), top, region; `sphere_diameter(V)` | `tanks_in_stage(ax, 3.0, [dict(name="kerosene", volume=4.11, ullage=0.05, style="fuel"), ...])` |
| `temperature_axis(ax, lo, hi, step)` -> the Celsius axis on the right | `temperature_axis(ax, 0, 400, 50)` |
| `math_row(ax, xy, ["$p_e$", "<", "$p_a$"])` a short relation as separate pieces | under each plume |

## Styles: one look for one thing

Chapter 1's styles hold (scripts/chapter_1/README.md): thrust is a `"force"` arrow (black, heavy), a
velocity a `"velocity"` arrow (blue), the exhaust and the propellant inflow `flow_arrow` (open block
arrow), construction lines thin gray, the part a figure is about light gold (`HIGHLIGHT`). Chapter 4 adds:

| Thing | Look | Name |
|---|---|---|
| Payload, inert mass, propellant | gold plain; white with a gray hatch; light blue plain (read in grayscale); key with `mass_key` | `MASS_STYLE`, `MASS_ORDER` |
| A wall cut in section (thrust chamber, injector) | white, `////` hatch, 1.2 pt black outline | `WALL_HATCH`, `WALL_LW` |
| Pressure on a wall | short thin steel-gray arrows, small heads, normal to the wall, tips on it; named in `arrow_key` | `PRESSURE_ARROW` |
| Jet boundary; oblique shock | black dashed 1.5 pt; thin black solid | `PLUME_STYLE`, `SHOCK_STYLE` |
| The three states of expansion | always in the order overexpanded, ideally expanded, underexpanded | `EXPANSION_STATES` |
| Oxidizer, fuel, solid propellant, solid fuel | Chapter 1's cutaway tints and hatches | `LIQUID_STYLE` (from `PROPELLANT_STYLE`) |
| Range boxes on a log chart | an outline color and line style each, with a light fill of the same color | `RANGE_STYLES`, `RANGE_TEXT` |

## The gate

Unchanged: `figkit.py` is not touched. What Chapter 4 adds is in its helpers:

- `thrust_chamber` and `chamber_contour` assert the drawn area ratio and throat; every wall, gas region,
  the axis and the exit plane are drawn on the engine's envelope (`figkit.on_part`), so a leader that
  ends inside the engine may cross them and any other leader is stopped (`selftest.py` tests both);
- `plume` asserts the boundary one exit radius downstream; `mass_bar` asserts that the segments add up
  to the bar (and to `total`); `tanks_in_stage` asserts that each tank fits the stage and holds its
  liquid volume; `best_split` asserts the best-split condition; `aligned_axes` asserts the shared scale;
- in `draw_schematic` the pipes and valves are drawn on the feed system's envelope, and in
  `tanks_in_stage` the walls on the stage, so a leader may cross a pipe or a wall to reach a component
  inside; in `range_boxes` the boxes overlap, so a callout's leader may cross another box's edge;
- `style.py` widens the kit's word-subscript pattern (as Chapter 3's does) to braced subscripts of two
  or more letters, `\text{...}`, `\max`, and any label with two or more subscripts. Matplotlib writes
  the small glyphs of one label next to each other in the SVG, so the kit's SVG check would read
  "$p_e < p_a$" or "$A_e/A_t$" as the word subscript "ea" or "et"; set at 0.88 of a 12 pt label they
  are 10.6 pt and pass. Such a label must be 12 pt (`FS_LABEL`): at 11 pt it is stopped.

Usual fixes: a label inside a narrow box (`range_boxes`) or near a cluster of points
(`named_scatter`) takes `label_at`; a crowded box takes a `callout`; `place_labels` prints a note when
no candidate is clear, and the gate then says where it touches. Labels on a fill take the fill as
their backing (the pixel test stops a white box on a fill). Hidden tick labels count: `log_axis` with
limits keeps only the decades inside the view.

## Traps

- Mass flow in a figure is the character "ṁ" (U+1E41, in Arial), never `\dot{m}`. Volume is the word
  "volume" in a figure (script V is not in Arial). No `^\circ`: write °.
- `nozzle_flow` uses the chamber's own state: with a finite contraction ratio the gas already moves in
  the chamber, so normalize by the first station to plot ratios to the chamber value.
- The ideal nozzle with a ratio of specific heats of 1.2 gives a thrust coefficient 2 percent below
  SP-125's shifting-equilibrium tables; `matching_gamma(Cf, 1000, 14.7)` gives the value (1.143 for
  oxygen and kerosene, 1.236 for oxygen and hydrogen) that puts a computed curve through the table's
  point. Say in the caption which was used.
- `fixed_nozzle_thrust` holds the flow at its vacuum rating; the altitude of ideal expansion needs an
  exit pressure, which the sources do not give: compute it from the area ratio and chamber pressure
  (`pressure_ratio_from_area_ratio`) and state the ratio of specific heats.
- The atmosphere of page 1.4 ends at 59.5 km: a plot against altitude stops there, with the vacuum
  value drawn as a dashed line.
- The bell angles come from SP-125 Figure 4-14, read to about a degree, and are held at the chart's
  end values beyond an area ratio of 50.
- The chamber of a large engine is only a little wider than its throat (SP-125's design example uses a
  contraction ratio of 1.6); the drawn wall is thicker than a real one (say so in the caption).
