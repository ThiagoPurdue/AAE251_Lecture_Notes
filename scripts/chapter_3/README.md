# Chapter 3 figure and value code

Shared code for the pages of Chapter 3, Aerodynamics. One module per page, `p3N_<slug>.py`
(for example `p32_airfoil_and_finite_wing.py`), with one function per figure, `make_all()` and
`values()`. Every page module starts with the one import line

```python
from chapter_3.common import *
```

and never types a constant: every constant is in a shared module, with its source.

```bash
python3 -B scripts/make_chapter_3_figures.py              # every page module: figures, then values.json
python3 -B scripts/make_chapter_3_figures.py p32          # one page (values.json keeps the others)
FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_3_figures.py p32   # also matplotlib PNG previews
FIG_LAYOUT=warn ...                                       # draft mode: list every layout problem, save anyway
python3 -B scripts/render_svg.py notes/chapter-3/figures/p32-*.svg --out <folder> --gray   # look in Chrome
python3 -B scripts/check_values.py p32 [--strict]         # every recorded number is on its page
python3 -B scripts/chapter_3/selftest.py                  # every unit check of the shared code
```

Run a page module through the runner, never directly (a second import path would make a second
copy of the value record). Matplotlib and NumPy only: nothing here needs SciPy.

## Modules

| Module | What it holds |
|---|---|
| `style.py` | Chapter 3's `record`, `write_values`, `save_figure` (a `figkit.Chapter` for `notes/chapter-3`), `PAGES` (p31 wind-tunnels, p32 airfoil-and-finite-wing, p33 drag-polar, p34 wing-loading). It also sets word subscripts such as `$c_{m,ac}$` and `$(L/D)_\max$` at the kit's word-subscript size (see "The gate") |
| `aero.py` | Coefficients and forces (`dynamic_pressure`, `force`, `moment`, `coefficient`, `mach_number`); viscosity by Sutherland's law (`mu_sutherland`, `mu_sutherland_en`, USSA 1976 constants), `kinematic_viscosity`, `reynolds`, `speed_for_reynolds`, `transition_x`; the flat-plate boundary layer (`delta_laminar`, `delta_turbulent`, `blasius`, `laminar_profile`, `turbulent_profile`); the finite wing (`induced_angle`, `induced_drag_coef`, `wing_lift_slope`, `wing_CL`, `wing_drag_coef`); the drag polar (`polar_K`, `polar_CD`, `min_drag_point`, `level_CL`, `drag_parts`, `min_drag_speed`); wing loading (`wing_loading_stall`, `stall_speed`) and the flap increment of Nicolai and Carichner (2010), Eq. (9.9) (`flap_dCLmax`, `sweep_factor`); constants `MU_SL`, `RHO_SL`, `MU_SL_EN`, `RHO_SL_EN`, `G0` (9.81 m/s², the value used throughout the course, equal to Chapter 1's; `tunnel.py` takes its `G` from it), `DEG_PER_RAD` (57.3), `RE_TR_PLATE` |
| `tunnel.py` | `test_section_speed`, `pressure_difference`, `manometer_dp`, `manometer_dh`, `settling_speed`, `mach_check`, `axis_flow` (speed, static pressure and total pressure along the axis, with a diffuser loss), `contraction_wall` (fifth-order polynomial); the outlines `closed_circuit_plan()` and `open_circuit_side()` (a `Tunnel`: dict name -> `TunnelPart`, with `stations`, `flow`, `model_parts`, `extent`); `tunnel_subset` (draw part of a tunnel); `axis_area` |
| `airfoil_data.py` | NACA Report 824 section data of the NACA 64(3)-018 and 64(3)-618 (`DATA`, `AIRFOILS`, `REYNOLDS`); `series`, `curve`, `read`, `lift_line`, `properties`; `pchip` (the shape-preserving cubic the curves are drawn with); the sections (`section_outline`, `mean_line_a1`, the report's ordinates); `naca_chart` (the chart in the report's layout) and `draw_reading` |
| `drawing3.py` | `disc` (the numbered disc on any axes), `vector`, `angle_mark` (asserts the angle drawn), `ray`, `unit`, `rotate`, `section_xy`, `airfoil_in_stream`, `downwash_construction`, `wing_rear_view`, `spiral_vortex`, `flat_plate`, `velocity_profile`, `boundary_layer_plate`, `linked_polar`, `draw_tunnel`, `station_marks`, `name_part`, `step_label` |
| `published.py` | Published numbers the pages print, each with its source: the viscosity table of the U.S. Standard Atmosphere 1976 (`USSA_MU_POINTS`), Leishman's airliner wing and Reynolds-number range of small aircraft, Purcell's swimmers, the flap and gear increments and span efficiencies of Scholz after Loftin (`SCHOLZ_FLAPS_GEAR`, `LOFTIN_E_CRUISE_JET`), the takeoff wing-loading trends of Nicolai and Carichner Table 6.1 (`WS_TRENDS_CIVIL`, `WS_TRENDS_MILITARY`), their Table 9.1 and Example 6.1 (`CLMAX_T91`, `ALCM`), and the 777-200 of Jenkinson et al. (`B772_*`) |
| `common.py` | The import line: Chapter 1's style, constants, atmosphere, flow, geometry, aircraft, drawing and diagrams, then all of the above |
| `selftest.py` | Every unit check of these modules plus gate checks of the helpers |

The full API with one-line examples is in each function's docstring; the sections below give
the import line, the data, the helpers and the usual fixes.

## A page module

```python
from chapter_3.common import *      # first line of scripts/chapter_3/p3N_<slug>.py
PAGE = "p32"
def my_figure(): ...; save_figure(fig, "p32-airfoil-chart")
def make_all(): my_figure()
def values(): record(PAGE, "cl_read", fmt(read("64-618", "cl_alpha", 6e6, 4.0), 3))
```

`common` brings everything of `chapter_1.common` and then rebinds `record`, `save_figure`,
`write_values`, `VALUES`, `WRITTEN`, `PAGES` to Chapter 3. `record(page, key, text)` takes the
printed string (`fmt(x)`, `fmt_dec`, `fmt_sci`) and returns it; recording a key twice with different
text stops the run; `values()` must record every number the page prints. Render at `--scale 1.5`
or 1.6: a 6.5 in figure then stays near 1,000 px.

## The airfoil data (NACA Report 824)

Two sections of one family and thickness, so the difference is camber alone: **NACA 64(3)-618**
(cambered, design c_l 0.6, report page 195) and **NACA 64(3)-018** (symmetric, report page 192),
each at R = 3.0, 6.0, 9.0 million, smooth model. Write them "NACA 64<sub>3</sub>-618" on a page and
`AIRFOILS[k]["name"]` in a figure. Cite the report by page (the chart pages have no figure number).

| Curve (`DATA[k][curve][Re]`) | 64-618: points at 3 / 6 / 9 million | 64-018 | Range |
|---|---|---|---|
| `cl_alpha` (alpha deg, c_l) | 31 / 34 / 28 | 21 / 31 / 22 | 618: -17 to 24 deg; 018: -21 to 22 deg |
| `cm_alpha` (alpha, c_m,c/4) | 28 / 27 / 24 | 17 / 21 / 10 | 618: -18 to 24 deg; 018: -22 to 22 deg (9 million from -2 deg) |
| `cd_cl` (c_l, c_d) | 16 / 17 / 19 | 16 / 22 / 22 | the bucket and both rising ends, c_l -1.4 to 1.5 |
| `cmac_cl` (c_l, c_m,ac) | 9 / 18 / 14 | 10 / 8 / 9 | c_l -1.1 to 1.5 |

Section characteristics from the data (`properties(k, Re)`), 6 million: 64-618 a0 = 0.1165 per deg,
alpha_L0 = -3.75 deg (the report's Figure 37 gives -4.0 deg; write "about -3.7 deg, read from the
chart"), c_l,max = 1.51, c_d,min = 0.0051, c_m,ac = -0.092, x_ac = 0.275 c; 64-018 a0 = 0.113 per deg,
alpha_L0 = 0.1 deg, c_l,max = 1.35, c_d,min = 0.0048, c_m,ac = 0.002. Maximum lift grows with R and
minimum drag falls. The 64-018 drag points at 6 million have a step near c_l = 0.42; a comparison of
the two polars reads better at 9 million.

- `read(k, curve, Re, x)` -> the value the chart draws at x (raises outside the recorded range);
  `curve(k, curve, Re, n=400, x=None)` -> (x, y); `series(...)` -> the points;
  `lift_line(k, Re, lo=-6, hi=4)` -> (a0, alpha_L0); `properties(k, Re)`; `section_outline(k, chord)`.
- `naca_chart(k, re=REYNOLDS, ranges="data"|"report", width=6.5, height=6.3, outline=True, key=True,
  markers=True, reading=[dict(curve=, re=, x=, n=[, value_label=])])` -> (fig, axes dict: left,
  right, sec_left, sec_right, outline, key, readings). The c_m,c/4 axis is outside the left panel
  (1/4 of the c_l scale), the c_m,ac axis on the right of the right panel (25 times the c_d scale):
  plot your own moment points with `y / CM_PER_CL` and `y / CMAC_PER_CD`. `CMAC_AXIS_GAP` (0.10) is how far
  (axes fraction) right of the right panel the c_m,ac axis stands, clear of the curve ends; use it to
  place anything drawn at that axis (page 3.2's chart does).

## Helpers, with an example each

| Helper | Example |
|---|---|
| `airfoil_in_stream(ax, alpha, airfoil="64-618", chord=1, c4=(0,0), V_len=0.45, lift=0.7, drag=0.18, moment=None, labels=True, arc_r=None, ext=0.90, ref=0.85, alpha_label_r=None)`; `ext` and `ref` are the lengths (chords) of the dashed chord line ahead of the leading edge and of the free-stream reference line; `alpha_label_r` (chords) puts the alpha label inside the wedge on its bisector at that radius (default: above the chord line) | `airfoil_in_stream(ax, 6.0, moment="nose down")` on `canvas(6.5, xlim=(-1.95, 1.45), ylim=(-0.35, 0.95))`, then `trim_canvas(fig)` |
| `downwash_construction(ax, alpha, alpha_i, k=2, airfoil="64-618", chord=2.0, c4=(0,0), V_len=2.2, F_len=2.2, lead=0.2, labels=True, angle_labels=True, alpha_at="upstream")` -> points P, T1, T2, F, L_local, L, Di and the drawn angles A, Ai, Ae; the velocity triangle ends at the vertex P on the chord line, `lead` chords ahead of the leading edge; `alpha_at="downstream"` marks alpha beyond P, between the chord line and a thin free-stream line from P toward the section (give `lead` about 0.9), so the alpha_i and alpha_eff wedges carry one label each | `downwash_construction(ax, 8.0, induced_angle(0.9, 6.0, 1.0), k=3.5)`; the caption states the factor k |
| `vector`, `angle_mark(ax, vertex, a_from, a_to, r, label, stated=, label_dir=, label_r=)`, `ray` | `angle_mark(ax, S, -A, 0, 1.0, r"$\alpha$", stated=A)` |
| `wing_rear_view(ax, htail=False)` -> tip_L, tip_R, span, vortex_L, vortex_R (737-800 seen from behind); `htail=True` adds the horizontal tail (on the centerline, it hides no tip); `spiral_vortex(ax, center, r0, r1, turns=1.3, sense="ccw"/"cw", inward=False)`; `inward=True` runs the spiral from r1 in to r0 with the arrowhead at the inner end (air rolling up into the core) | right tip "ccw", left tip "cw" (seen from behind) |
| `boundary_layer_plate(ax, x_end=6, transition=(3.0, 3.6), stations=(1.3, 2.8, 4.1, 5.0), n_lam=3, wall_join=0.08)` (braces for the laminar layer, transition and turbulent layer; turbulent profiles leave the wall at a finite slope) -> vexag (vertical exaggeration, for the caption), deltas, drawn, profiles, edge; `n_lam` is the number of arrows in each laminar profile (turbulent ones have four), `wall_join` is passed to the turbulent profiles; `flat_plate`, `velocity_profile(..., wall_join=None)` underneath: `wall_join=j` (turbulent only) replaces the one-seventh law below y/delta = j by a cubic that leaves the wall at the finite slope 1.5 u(j)/j and meets the law at j with its value and slope | page 3.1's boundary-layer figure |
| `linked_polar(alpha, CL, CD, marks, flip=False, labels=("$C_L$", "$C_D$"))` -> (fig, axes, points) | page 3.3's polar-from-data figure |
| `closed_circuit_plan()`, `open_circuit_side(H2=1, ratio=7.5)`, `tunnel_subset(T, names)`; `draw_tunnel(ax, T, highlight=(...))` -> patches; `station_marks(ax, T, patches=P, side=1)`; `name_part(ax, T, part, text, text_xy, start=None, target=None)` | page 3.1's tunnel figures |
| `step_label(ax, xy, n, text, color)`; `disc(ax, xy, n, above=)` | a numbered disc on a data plot |

Tunnel parts (names for `highlight`, `name_part`): closed circuit `corner_1` to `corner_4`,
`settling_chamber`, `honeycomb`, `screen_1` to `screen_4`, `contraction`, `test_section`, `support`,
`strut`, `diffuser`, `crossleg`, `return_diffuser`, `fan_section`, `fan`, `hub`, `return_leg` (ft;
flow counterclockwise, test leg below); open circuit `bellmouth`, `settling_chamber`, `honeycomb`,
`screen_1` to `screen_3`, `contraction`, `test_section`, `support`, `diffuser`, `fan_section`, `fan`,
`hub`, `exhaust` (m; flow to the right). `T.stations[n]` gives each station's two wall points,
`T.flow` good flow-arrow positions, `axis_area(T_open, x)` the area.

## Usual fixes for the gate

- A label in a narrow wedge: `angle_mark(..., label_r=)` centers it beyond the arc.
- A leader that must leave a label at a given point: `name_part(..., start=)`.
- Leaders into a tunnel part may cross that part's walls, never another part's.
- Labels are wider than they look: measure with `text_size(ax, s, fs)` before placing.
- Arrowheads on lines: end construction lines short of heads (`pt(ax, 16)`).
- Hidden tick labels (ticks outside the limits) count: keep only ticks inside the view.
- A diagram canvas: end with `trim_canvas(fig)` before `save_figure`.

## Traps

- The figure kit is imported once; `chapter_3.style` patches `figkit._WORD_SUB` at import. Never
  import chapter_3 from a Chapter 1 or 2 module.
- Elliptic lift gives the same downwash along the span: draw equal arrows behind the wing.
- The a = 1.0 mean line has an infinite slope at both ends; draw the 64-618 from the report's
  ordinates (`section_outline` does).
- Report 824 has no table of section characteristics: the unit checks use the a.c. table printed
  on each chart and the summary figures 37, 38 and 41.
- Nothing in chapter_3 imports SciPy (`pchip` is NumPy).
- `mu_sutherland` and the boundary-layer thickness formulas follow Leishman (2022), Chapters 15
  and 26; the transition guide `RE_TR_PLATE` = 5 x 10^5 his Chapter 18.

## Styles: one look for one thing

Chapter 1's styles hold (scripts/chapter_1/README.md): force arrows black and heavy, velocity
arrows blue, flow direction as open block arrows, moments as curved black arrows, construction
lines thin gray (`line_kw("reference")`) or dashed (`line_kw("boundary")`), the part a figure is
about in light gold (`HIGHLIGHT`). Chapter 3 adds:

| Thing | Look |
|---|---|
| Reynolds-number curves of the NACA data | 3.0 million: series 1 (blue dashed, circles); 6.0 million: series 0 (black solid, squares); 9.0 million: series 2 (vermilion dotted, diamonds), open markers at the test points (`RE_STYLE`) |
| A reading on a chart | thin black dashed construction lines, a black dot on the curve, the numbered disc on the axis where the reading starts |
| Tunnel walls | 1.8 pt black; joints between parts 1.0 pt; honeycomb a block of cell walls along the flow; screens (across the flow) and turning vanes (eight per corner, chord one eighth of the duct width) thin lines; fan a gray band; stations as numbered discs outside the outline, the dashed station line run out to them |
| Angles | thin arcs (`angle_mark`), label outside the arc or centered in a narrow wedge (`label_r`) |
| Tip vortex | a spiral with a normal arrowhead at its outer end |

## The gate

Unchanged: `figkit.py` is not touched. What Chapter 3 adds to it is in its helpers:

- `angle_mark(..., stated=)` asserts that the angle drawn equals the angle the text states;
- `vector` asserts the drawn direction; `downwash_construction` asserts alpha = alpha_eff + alpha_i,
  the local lift perpendicular to the local relative wind, D_i = L tan(alpha_i) and the vector scale;
- `draw_reading` asserts that the reading point lies on the drawn curve;
- `spiral_vortex` asserts its sense of rotation, `wing_rear_view` that the right wing is on the right;
- `draw_tunnel` marks every wall, joint, screen and vane as drawn on its part (`figkit.on_part`),
  and parts inside a duct (honeycomb, screens, fan, hub, support) on that duct, so the gate checks
  leaders against every other part; `station_marks(patches=)` does the same for station lines;
- `style.py` widens figkit's word-subscript pattern (`figkit._WORD_SUB`) to subscripts of two or
  more letters (`$c_{m,ac}$`, `$c_{m,c/4}$`) and `\max`, so they are set at 0.88 of the label size
  and pass the kit's own SVG check (10.5 pt for a word subscript). The change is made at import of
  chapter_3, so Chapters 1 and 2 (whose runners never import it) draw exactly as before.

## Sources of the shared constants

In each module's header: U.S. Standard Atmosphere 1976 (viscosity), Leishman (2022, boundary
layer and transition), NASA TP-3008 (Langley 14- by 22-Foot Subsonic Tunnel), NASA CR-177488 (Bell
and Mehta, contractions), NASA Glenn Beginner's Guide (tunnel parts and types, viscosity), NACA
Report 824 (section data and ordinates), Nicolai and Carichner (2010, flap increment), Boeing
D6-58325-7 (737-800 front view, through chapter_1/aircraft.py); `published.py` lists the sources of
the numbers the pages print.
