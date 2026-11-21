# Chapter 1 figure and value code

Shared code for the pages of Chapter 1, Systems Engineering and Fundamental Thoughts. One
module per page, `p1N_<slug>.py` (for example `p14_standard_atmosphere.py`), with one function
per figure, `make_all()` and `values()`. Every page module starts with the one import line

```python
from chapter_1.common import *
```

and never types a constant: every constant is in a shared module, with its source.

```bash
python3 -B scripts/make_chapter_1_figures.py              # every page module: figures, then values.json
python3 -B scripts/make_chapter_1_figures.py p14          # one page (values.json keeps the others)
FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_1_figures.py p14   # also matplotlib PNG previews
FIG_LAYOUT=warn ...                                       # draft mode: list every layout problem, save anyway
python3 -B scripts/render_svg.py notes/chapter-1/figures/p14-*.svg --out <folder> --gray   # look in Chrome
python3 -B scripts/check_values.py p14 [--strict]         # every recorded number is on its page
python3 -B scripts/chapter_1/selftest.py                  # every unit check of the shared code
```

Run a page module through the runner, never directly: a second import path would make a second
copy of the value record.

## Modules

| Module | What it holds |
|---|---|
| `style.py` | The chapter's `record`, `write_values`, `save_figure` (a `figkit.Chapter`); line weights, fills, the risk-level styles, the arrow kinds; `pt`, `kind_arrow`, `flow_arrow`, `moment_arrow`, `motion_heads`, `legend_key`. Re-exports the book's figure kit, `scripts/figkit.py` |
| `constants.py` | Units (`FT`, `NMI`, `NMI_FT`, `KT_FPS`, `MILE_KM`, `LB_KG`, `KG_LB`, `LB_N`, `SLUG_KG`, `FTLB_J`), Earth with the values of Chapter 2 (`MU_EARTH`, `RADIUS_EARTH_EQ`, `RADIUS_EARTH_MEAN`, `T_SIDEREAL`), `geo_altitude()`, airport reference points (`AIRPORTS`) and `great_circle_nmi()`, the landing-gear limit sink rate of 14 CFR 25.473 (`LIMIT_SINK_RATE_FPS`) |
| `atmosphere.py` | The standard atmosphere of these notes (constants, layers, both directions), speed of sound, a hot or cold day, another planet (`PLANETS`: Venus, with its molar mass); `UNIVERSAL_R`, `M_AIR`, `K_BOLTZMANN` |
| `environment.py` | Where the hazards of 1.2 are found, as published: bird strikes, the icing band, jet streams, the radiation belts, atomic oxygen, debris, drag decay, Hubble's orbit; the microburst of FAA AIM 7-1-24 (`MICROBURST_DOWN_FPM`, `MICROBURST_WIND_KT`, `MICROBURST_SHEAR_KT`, `MICROBURST_DOWN_MI`, `MICROBURST_OUT_MI`); the altitude above which sunlight turns a spacecraft more than drag does, NASA SP-8027 (`SRP_DOMINANT_KM`) |
| `flow.py` | Continuity, Bernoulli with and without the height term, venturi, manometer, pitot-static airspeed, draining tank |
| `sizing.py` | Raymer Table 3.1 (`EMPTY_WEIGHT_FIT`), the historical segment fractions, Breguet cruise and loiter fractions, the 6% reserve, the takeoff-weight iteration with every step; published data of real aircraft (`JET_WEIGHTS`, `SFC_TYPICAL`, `LD_TYPICAL`, `EMPTY_WEIGHT_RANGE`) |
| `geometry.py` | Curves (`superellipse`, `catmull_rom`, `fillet`, `hull`, `blunted_ogive`), NACA 4-digit sections, wing planform metrics and the MAC construction, `Part`, `rotate_parts`, `rotate_xy`, `ellipse_xy`, `extent`, `clip_poly` and `clip_line` (cut a shape to a rectangle), landing-gear layouts (`GEAR_LAYOUTS`, `GEAR_BODY`, `gear_wing_edges`; see below), sections real airplanes use (`AIRFOIL_USAGE`) |
| `aircraft.py` | The jet transport (Boeing 737-800 with winglets, `B738`) in three views: `aircraft_side(P, detail=True, ground=False)`, `aircraft_top(P, detail=True)`, `aircraft_front(P, detail=True, ground=False)`; `three_view(P, gap, detail, ground)` (side, front and top at one scale, aligned), `place(parts, dx, dy)`, `fuselage_section`, `wing_z`, `wing_box`, `cg_point`; `VIEWS` (screen directions of the body axes x, y, z in each view, right-handed by unit check) and `rotation_sense(view)`; `winglet_cant()`; published numbers the pages print (`B738_WING`, `B738_MTOW_LB`, `B738_SEATS_TWO_CLASS`) |
| `launchers.py` | `launch_vehicle(P=ARIANE5, payload="hidden", cutaway=False, orientation="vertical")` (core stage, two solid boosters), `two_stage_vehicle(P=FALCON9, payload="hidden", cutaway=False, legs=False, grid_fins=False, orientation="vertical")`; `draw_cutaway(ax, parts)` (tanks tinted and hatched by propellant, `PROPELLANT_STYLE`); `bell_contour`, `engine_side`, `capsule`; Ariane 5 flight facts (`ARIANE5_FLIGHT`) |
| `drawing.py` | Drawing hardware: `draw_parts(..., details=True)`, `label_part`, `name_parts`, `draw_section`, `planform_xy`, `draw_gear_layout`, `gear_side`, `gear_plan_shapes`, `gear_side_shapes`, `GEAR_CONTACT`, `GEAR_STANCE` (the gear arrangements; see below), `cg_symbol`, `body_axes`, `perp_symbol`, `axis_arrow`, `rotation_arrow`, `draw_enlarged` (an enlarged inset of a detail, cut at its frame), `draw_mission_profile`, `hatched_wall`, `dimension_outside`, `draw_manometer` |
| `diagrams.py` | Block diagrams and matrices: `canvas` (axes that fill the figure, so `save_figure` reports the true size), `set_frame`, `text_size`, `box` (`keep_breaks=True` keeps the given line breaks; `ls` a dashed outline), `box_height`, `lines_box` and `lines_box_height` (a box whose given lines sit on evenly spaced baselines, so a line with math keeps the spacing of a plain one), `column`, `row`, `decision` (`keep_breaks=True` for a two-line question), `route`, `step_marker`, `numbered_callout`, `key_disc`, `brace`, `matrix`; `trim_canvas(fig, margin=6.0)` crops a diagram to its drawing plus an even margin (call it last, before `save_figure`). `wrap` never breaks a line before a number ("stage 1" stays together) or between a number and its unit (`BOX_UNITS`), and balances the lines of a box when the plain fill would leave one word alone on the last line; give a box its own breaks with `keep_breaks=True` when the result still splits a name |
| `common.py` | The import line: all of the above |

Data file: `p12_f107_monthly.csv`, the monthly F10.7 solar radio flux read by the 1.2 module (its header names the source and the months).

The figure kit (`scripts/figkit.py`, shared with Chapter 2) holds `fmt`, `fmt_dec`, `fmt_sci`,
`new_axes`, `data_axes`, `text`, `callout`, `arrow`, `point`, `line`, `angle_arc`, `dimension`,
`label_curve`, `bars`, `line_kw` and `text_color` (data series 0 to 4, roles "reference" and
"boundary"), `opaque`, `rides_on`, `close_to` (absolute tolerance; `rel=True` for a relative one),
`contrast_ratio`, the gate (`layout_problems`,
`pixel_problems`, `svg_problems`) and the style constants (`FIG_WIDTH`, `FS_LABEL`, `FS_SMALL`,
`LW_THIN`, `GRAY`, `STEEL`, `INK`, `GOLD`, `LIGHT`, `SERIES`, `HEAD`, `MOTION_HEAD`).
Their use is as in `scripts/chapter_2/README.md`. `dimension(..., zorder=)` draws a dimension above
an opaque box (the default 2.5 puts it under one). When the gate reports an arrowhead lying on
another line, the position in the message is the arrowhead's tip (the wording is unchanged, so
existing `allow=` strings still match).

## Styles: one look for one thing

| Thing | Look | Name |
|---|---|---|
| Main curve or data line | 2.0 pt, black solid (`line_kw(0)`), then the series 1 to 4 | `LW_MAIN`, `line_kw(i)` |
| Outline of a vehicle, airfoil or duct wall | 1.8 pt black, white opaque fill | `LW_OUTLINE`, `PART_FILL` |
| Line inside an outline (hinge line, stage joint) | 1.0 pt black | `LW_DETAIL` |
| The part a figure is about | light gold fill (`#F5EFDC`); a control surface is also hatched | `HIGHLIGHT`, `draw_parts(highlight=)` |
| Construction, dimension, reference lines | 0.9 pt; reference gray solid, boundary gray dashed | `LW_THIN`, `line_kw("reference")`, `line_kw("boundary")` |
| Diagram box | 1.2 pt black, white; first and last box of a flow light gold | `LW_BOX`, `BOX_FILL`, `BOX_FILL_START` |
| Liquid | light blue fill | `FLUID_FILL` |
| Risk level | Low white, Medium light gray, High gray with a hatch, plus a key | `RISK_STYLE` |

Arrow kinds (FIGURE_STANDARD point 30: one arrow style means one thing; two kinds in one figure
are named, `legend_key` draws a key):

| Kind | Look | For |
|---|---|---|
| `"force"` | black, 2.2 pt, large solid head | a force, drawn where it acts |
| `"velocity"` | blue `#0072B2`, 1.6 pt, normal head; label in the same blue | a velocity; to one scale when two or more are compared |
| `"flow"` | open block arrow, black outline, white inside (`flow_arrow`) | the direction a fluid moves |
| `"leads_to"` | dark gray `#3A3A3A`, 1.4 pt, normal head, right angles only (`route`) | a step of a process, a link in a diagram |
| `"moment"` | black curved arrow (`moment_arrow`) | a rotation: roll, pitch, yaw |
| `"dimension"` | thin black, small heads both ends (`dimension`, `dimension_outside`) | a length |
| `"axis"` | black, 1.2 pt, normal head, from the origin (`body_axes`) | a body or coordinate axis |
| motion head | 10 x 3 pt head on the path (`motion_heads`) | the direction of travel along a path (a flight profile, a streamline) |

Numbered markers: one disc for the whole chapter (`DISC_FILL`, `DISC_LW`: a white disc, a thin
black ring, a regular-weight number). `step_marker` places it for the numbered steps of a method;
`numbered_callout` (with a leader) and `key_disc` (without) for a key to names beside the figure.

## Vehicles: parts, details, cutaways

Every vehicle helper returns a dict name -> `Part` (closed outline `xy`, `kind`, drawing order
`z`, `inside` point for a leader, `hidden`, and `on`: the part a detail is drawn on). Each view is
drawn as an observer sees it: the side view shows the left side with the nose to the left; the
plan view is seen from above with the nose to the left, so the right wing (`_R`) is at the top of
the page; the front view is seen from ahead, so the right wing (`_R`) is on the left of the page.
`VIEWS` in aircraft.py gives the screen directions of the body axes in each view (its unit check
tests that x, y, z are right-handed and that the drawing agrees). Part names (`_L` left wing,
`_R` right wing):

- `aircraft_side()`: fuselage, wing, winglet, nacelle, exhaust_nozzle, exhaust_plug, htail,
  vtail, rudder, nose_gear, nose_wheel, main_gear, main_wheel; details (detail=True, drawn in
  dark gray, `DETAIL_INK`): flight_deck_windows, flight_deck_post_N, cabin_window_N,
  entry_door_N, overwing_exit_N, apu_exhaust, inlet_lip, nose_hub, main_hub; ground=True adds
  the ground line. There is no pylon, wing-body fairing, cargo door, flap fairing or wing-root
  section in the side view: Boeing's drawing shows the nacelle against the wing, and a part it
  does not show is not drawn.
- `aircraft_top()`: fuselage, wing_body_fairing (a detail), vtail (a thin detail along the
  centerline, so details=False leaves it out), and per side wing, winglet, nacelle,
  exhaust_nozzle, exhaust_plug, pylon (a strip from the middle of the nacelle to the leading
  edge), htail, elevator, slat_N (20% of the chord), flap_inboard, flap_outboard, spoiler_N (root
  to tip; 1 and 6 ground spoilers), aileron. No flight-deck marks (`detail` is accepted and
  ignored for them). The rudder is named in the side view only.
- `aircraft_front()`: fuselage (the cross-section), vtail, per side wing, winglet, nacelle,
  pylon, htail, main_gear, main_wheels, main_wheels2; nose_gear, nose_wheels, nose_wheels2;
  details flight_deck_windows, inlet_L/_R, fan_L/_R (no radome outline).
- `launch_vehicle()`: fairing, equipment_bay, upper_stage, interstage, core_stage,
  core_engine, booster_left/right (also booster_top/bottom) and their _nozzle and _jointN,
  strut_fwd_left/right and strut_aft_left/right (the attachments between booster and core),
  core_jointN; payload and adapter (hidden lines; solid in a cutaway; the adapter is seated on
  the equipment bay). cutaway=True
  cuts the vehicle open: propellant volumes become parts of kind "tank" with `contents` ("lox",
  "lh2", "solid", "void"): lox_tank above lh2_tank (the `common_bulkhead` line between them),
  lh2_tank_upper (at the core-tank radius, so it fills the stage from wall to wall) above the
  nested lox_tank_upper, booster_propellant_* with
  booster_channel_* (the central channel of the grain); upper_engine (kind "engine") below the
  upper-stage tanks. Draw a cutaway with `draw_cutaway(ax, parts)`, which tints and hatches each
  propellant (`PROPELLANT_STYLE`) so it reads in grayscale; draw_parts alone draws tanks as plain
  white shapes. orientation="horizontal" keeps `contents`.
- `two_stage_vehicle()`: fairing, second_stage, interstage (an open cylinder fixed to the first
  stage), first_stage, engine_N (three separate bells seen in the side view), stage1_joint;
  legs=True landing_leg_left/right (in profile) and, outside a cutaway, landing_leg_front;
  grid_fins=True grid_fin_left/right on the interstage and, outside a cutaway, grid_fin_front;
  cutaway=True tanks lox_tank_1, rp1_tank_1, transfer_tube, lox_tank_2, rp1_tank_2 (kind "tank",
  the common bulkhead straight as in SpaceX's figure) and vacuum_engine (kind "engine") below the
  second stage. `FALCON9["lox_fraction"]` (0.53) and `["lox_fraction_2"]` (0.50) are the oxygen
  shares of the tank length, measured on Figure 2-1 of the Falcon User's Guide (2025); `["wall"]`
  is the drawn wall thickness. `ARIANE5_FLIGHT` holds the flight facts the page prints, with the
  core stage's dry and propellant masses (`epc_dry_t`, `epc_prop_t`) and a booster's propellant
  (`eap_prop_t`).

`draw_parts(ax, parts, details=False)` draws the plain outline. Details and hidden lines are
drawn thin (`LW_FINE`, dashed when hidden) and marked with `figkit.on_part` on their host part.

`body_axes(ax, view, o, length, radius, rot_span, rot_label, rot_label_at, perp_at, show=None,
lw=None, label_dirs=None, rot_label_dir=None, rot_dist=5.0)` draws the
body axes x (forward), y (right wing), z (down) through the center of gravity in one view, taken
from `aircraft.VIEWS`: the in-page axes as arrows, the axis perpendicular to the page as a circle
with a dot (toward the reader) or a cross (away) carrying its letter, and the positive rotation
about it (pitch in the side view, yaw in the top view, roll in the front view). It asserts that
the drawn set is right-handed and that the rotation turns the way `rotation_sense(view)` gives.
The optional `lw` sets the line weight, `label_dirs` (a dict by axis letter, deg) and
`rot_label_dir` move a letter or the rotation's name off a crowded spot, and `rot_dist` sets the
gap of that name; `axis_arrow` and `rotation_arrow` take the same `lw` and `label_dir`.

`draw_mission_profile(ax, segs, ndir, drop=None, ground=(-0.3, 0.3), numbers=None, thin=(),
axes_names=False, name_dist=None, distance_below=27.0)` draws a mission profile by the one rule
of the chapter, which it asserts: the takeoff and the landing are short level segments on the
ground line, and every descent before a landing runs down to it. It draws a gray ground line, a
black path, a dot and a bold number at each segment end (0 at the start of the takeoff), segment
names beside the segments and direction heads. `drop` = (point index, what leaves[, side of
the words]) draws a sudden weight drop as a short downward arrow from the path at that point,
with "weight drop: <what>" beside it; `thin` lists the segments drawn thinner (a descent counted
inside another segment; the caller leaves the point at its top unnumbered); `axes_names=True`
adds light "altitude" and "distance" arrows and the word "ground", the distance arrow
`distance_below` points under the ground line; `name_dist` moves the segment names.

**Landing-gear arrangements.** `GEAR_LAYOUTS[kind]` (kind "tricycle", "tail-dragger",
"multi-bogie", "bicycle", "single main", "quadricycle"; "multi-bogey" is kept as an alias) is a
dict: `cg`, the station of the center of gravity as a fraction of the fuselage length, and
`units`, one tuple (x, y, n, m, size, role) per wheel unit: station and side offset (fuselage
lengths), n wheels side by side and m in tandem, the drawn size, and the role ("nose", "main",
"tail" or "outrigger"). All six are drawn on one generic airplane, `GEAR_BODY` (with
`gear_wing_edges(y)`, the wing's edges at a span station). `draw_gear_layout(ax, kind, length,
origin)` draws the view from below and returns a dict (wheels, units, cg); `gear_side(ax, kind,
origin, L, out=None)` draws the side view on a ground line from `gear_side_shapes()`, at the
contact heights of `GEAR_CONTACT`, or of `GEAR_STANCE` for an arrangement that sits pitched
(tail-dragger, single main), and fills `out` with what it drew. Each wheel unit stands at the
same station in both views, under structure (wing or fuselage). `drawing._part_style` draws a
detail in the color of its `ec` attribute when it has one.

`dimension_outside` names its parts with a counter kept on the axes, so the SVG is the same on
every run.
`cg_symbol(ax, xy)` is the quartered disc; name it in the caption.

## The gate (in `figkit.py`; it stops the run)

Everything Chapter 2's gate checks (labels clear of every line, outline, arrow, marker, frame
and tick; leaders crossing nothing; arrowheads on nothing but their own line; 10 pt text; Arial
glyphs; contrast; the pixel test), plus, for the artists the Chapter 1 helpers mark:

- an `opaque()` shape hides what lies under it, so a part behind another is no obstacle where it
  is hidden (every part from `draw_parts`, every box);
- a leader may cross only the outlines of shapes that contain its end (`label_part` ends inside
  the part: the wing's outline may be crossed to reach an aileron, the slat's may not), and a
  detail drawn on a part (`on_part`: a window on the fuselage, a hidden tank in a stage) only
  when the leader ends inside that part;
- a routed arrow (`route`) crosses no box, line, arrow or other routed arrow, leaves its source
  edge and ends with its tip on the target edge (within 1 pt);
- boxes keep 2 pt clear of each other, except the cells of one `matrix`;
- the text of a `box`, `decision` or matrix cell fits inside it with 2 pt of padding.

## Sources of the shared constants

- Atmosphere: the 1959 ARDC model of Anderson's textbooks; values checked against Anderson,
  *Aircraft Performance and Design* (McGraw-Hill, 1999), Appendix D. Sea-level values, R, gamma
  and g0 as the notes use them. Venus: NASA NSSDC Venus Fact Sheet; lapse rate from
  ECSS-E-ST-10-04C, Annex G.7.2.
- Sizing: Raymer, *Aircraft Design: A Conceptual Approach*, 4th ed. (AIAA, 2006), Table 3.1 and
  the segment fractions of Chapter 3. Jet weights: Jenkinson, Simpkin and Rhodes, *Civil Jet Aircraft Design*
  (1999), companion site, Data A, Table 3. Typical C and L/D: Scholz, Aircraft Design lecture notes,
  Chapter 5 (HAW Hamburg), Table 5.7 and Figure 5.7; Nicolai and Carichner (2010), Figure 5.3.
- Units, Earth, airports and the landing-gear rule: `constants.py` (NIST SP 811; the Earth values
  of Chapter 2; FAA Form 5010-1; 14 CFR 25.473). Hazard altitudes: `environment.py` (FAA AIM,
  AC 91-74B, AC 00-30C; NASA, 2013; Banks et al., 2004; NASA ODPO; STScI).
- Jet transport: Boeing, *737 Airplane Characteristics for Airport Planning*, D6-58325-7 Rev C
  (2025), Sections 2.2.6, 2.3.3, 2.5.1 and 7.2.1 (737-800W); Boeing news release of 18 February
  2000 (winglet size); the 737 NG flight-controls summary (number and kind of moving
  surfaces). Spans and chords of the control surfaces are schematic.
- Heavy launcher: Arianespace, *Ariane 5 User's Manual*, Issue 5 Revision 2 (2016), Section
  1.5.1, Annexes 4 and 5; ESA Bulletins 85 and 123; ESA pages on the main stage and the
  boosters; CNES (2025) for the Vulcain 2 size. Estimated: booster height along the core, the
  gap and struts, exposed booster nozzle, nose-cap radius, interstage and equipment-bay
  lengths, upper-stage tanks and engine.
- Two-stage launcher: SpaceX, *Falcon User's Guide* (2025) and *Falcon 9 User's Guide* Rev 2
  (2015); stage and interstage lengths from Spaceflight101 (secondary). Estimated: engines,
  nozzles, tank lengths, legs and grid fins. Captions say "proportions after".
- NACA sections: Jacobs, Ward and Pinkerton, NACA Report 460 (1933): designation, thickness
  equation, mean line.
