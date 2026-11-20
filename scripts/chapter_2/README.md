# Chapter 2 figure and value code

Shared code for the five pages of Chapter 2, Introduction to Orbits. One module per page,
`p2N_<slug>.py` (for example `p21_orbit_properties.py`), imports everything from
`orbits.py`. `orbits.py` is shared by all five pages: change it only at integration, keep its
unit checks passing, and never type a constant in a page module.

```bash
python3 -B scripts/make_chapter_2_figures.py            # every page module: figures, then values.json
python3 -B scripts/make_chapter_2_figures.py p23        # one page (values.json keeps the others)
FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_2_figures.py p23    # also PNG previews: look at them
FIG_LAYOUT=warn ...                                     # draft mode: list every layout problem, save anyway
python3 -B scripts/check_values.py [p23] [--strict]     # every recorded number is on its page
python3 -B scripts/chapter_2/orbits.py                  # unit checks of orbits.py
```

Always import as `from chapter_2.orbits import *` (or `from chapter_2 import orbits as O`),
never `import orbits`: a second copy of the module would lose the recorded values. Run a page
module through the runner, not directly.

## The figure standard

Every figure must be high quality and professional. Check each figure against all 23
points below before you report. The
points marked **[auto]** are also checked by `save_figure()`; the run stops when one fails.

**A. It teaches one thing**
1. One idea per figure; if the caption needs "and" twice, split it.
2. The main orbit or curve is the heaviest line (`LW_ORBIT` 2.0 pt); construction, axes and
   grid are the lightest (`LW_THIN` 0.9 pt, grid 0.6 pt).
3. Nothing the text does not use: no decoration, gradient, shadow, 3-D effect on 2-D data,
   clip art, stars or spacecraft icons (a spacecraft is a plain `point()`).

**B. The physics is drawn right**
4. Every orbit from its equation (`draw_orbit`, `orbit_xy`), body at the focus, equal aspect
   on every schematic (`new_axes` sets it).
5. To scale (draw in km with `RADIUS[...]`), unless the caption says "Not to scale" and what
   is exaggerated.
6. Velocity arrows tangent, pointing along the motion, lengths in proportion
   (`velocity_arrow` with one `scale` per figure, plus `speed_key`); a burn arrow points
   along the velocity change (forward to speed up, backward to slow down).
7. Angles from the stated reference in the stated direction: azimuth clockwise from north,
   true anomaly from periapsis in the direction of motion, inclination from the equator at
   the ascending node.
8. Direction of motion shown by an arrowhead on every orbit, counterclockwise seen from the
   north (`draw_orbit` and `Globe.circle` draw one by default).
9. At least one `assert` that measures what was drawn (`close_to()` helps).

**C. It is legible**
10. Arial, 10 pt or more at page size, dark on white, one or two sizes per figure
    (`FS_LABEL` 12, `FS_SMALL` 11). **[auto]**: no text below 10 pt, every glyph in Arial.
11. No label touches or crosses a line, arrow, marker, outline or other label; nothing
    clipped; leaders short and straight (`callout`). **[auto]**, in every panel: a label with
    its backing box keeps 0.5 pt clear of every line, arrow, marker, outline, axes frame and
    tick mark (grid lines exempt); a leader crosses no line or label on its way; an arrowhead
    lies on no other line, arrowhead or marker (only its own line, recorded with `rides_on()`, is
    exempt; a leader may cross only the outline of a filled region that contains its target,
    never an orbit line); a burn arrow
    lies beside its path, never on it. Then `pixel_problems()` renders the figure with and
    without its text and stops on any line ink a backing box
    hides and on any white box over a fill (on a fill use `backing=<fill color>`). The only
    exemption is a dimension label set on its line.
12. Symbols as in the text: `$r_p$`, `$\Delta V_1$`, `$v_\infty$`, "km/s".
13. Axis labels name quantity and unit ("Launch azimuth, degrees"); round, uncrowded ticks
    with thousands commas (`data_axes` does it); angle axes tick at 30, 45 or 90 degrees
    (`degree_ticks(ax, "x", 45)`).
14. Curves labeled directly where the label is clear (`label_curve`, `draw_orbit(label=)`);
    a legend only when direct labels cannot work, never over data.
15. Even margins, balanced white space, aspect suited to the content (wide for a time
    history, square for one orbit).

**D. It is accessible**
16. Color never the only cue: each role has its own line style; also look at the preview
    converted to grayscale.
17. Lines and marks at least 3:1 on white, text at least 4.5:1. **[auto]** for every text,
    line, marker and arrow color (grid lines exempt as decoration).
18. Alt text: what is drawn, how the parts relate, the values that matter, the point; one to
    four sentences; no "image of", no color names as the only identifier.
19. A caption that stands on its own: what, the conditions, the one thing to notice.
20. Whatever the figure shows is also in the text or a table.

**E. It is a set**
21. Same look for the same thing in every figure: use `STYLE` roles, `draw_body`, `burn`,
    `arrow`, the font constants; never set colors, line widths or arrow styles by hand. Orbit
    roles only for orbits in those roles; data curves, tracks of different orbits and the conic
    types take the data-series looks, `line_kw(0)` to `line_kw(4)` (black solid, blue dashed,
    vermilion dotted, dark gray dash-dot, green dash-dot-dot). Burns are black, beside the path
    (`burn(..., side=, offset=)`), and in proportion to their delta-V when a figure has two
    or more (`burn_lengths`), or the caption says they are not to scale.
22. Same orientation: periapsis to the right of the focus unless the figure needs otherwise;
    north up on globes and maps; the Sun at the center of heliocentric views.
23. `<tag>-<name>.svg` (`save_figure` enforces it), live text, no bitmap. **[auto]**: every
    glyph in Arial (STIX fallbacks rejected: type √ and °), every font-family written as
    `Arial, Helvetica, sans-serif`, word and ∞ subscripts set at 88% (10.6 pt for a 12 pt label;
    the check asks for 10.5 pt).

Look at every PNG at full size, two or three rounds per figure, then at the page screenshot
in light and dark mode. The final self-test PNGs of the foundation step, with grayscale
copies and their source, are in `build/foundation/selftest_final/`.

## Constants (PLAN section 5; never type a constant in a page module)

`MU`, `RADIUS` (dicts by body: Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn;
km³/s², km), `SUN_DISTANCE` (also Uranus and Neptune), `ORBIT_DAYS` (no Mars entry in either,
PLAN rule 4), `AU` (km), `OMEGA_EARTH` (rad/s), `T_SIDEREAL` (s), `G0` (m/s²) and `G_SI`
(N m²/kg², quoted only), `DAY` (86,400 s).

`RADIUS_EARTH_MEAN` = 6,371 km: the launch page uses Earth's mean radius, as launch
calculations commonly do, and says so; the other pages use `RADIUS["Earth"]` = 6,378 km. Only 2.3 uses the mean radius, and `surface_speed()` and `rotation_gain()` default
to it (0.4646 km/s at the equator). `SUN_DISTANCE_MARS_FIGURE_ONLY` places the Mars marker of
the 2.1 planet-speed figure; never print a number computed from it.

## Orbit functions (km, km/s, s; angles in degrees)

| Function | Returns |
|---|---|
| `circular_speed(mu, r)`, `escape_speed(mu, r)`, `vis_viva(mu, r, a)` | speed, km/s (a < 0 for a hyperbola) |
| `period(mu, a)`, `semi_major_axis_from_period(mu, T)` | s; km |
| `specific_energy(mu, a)`, `energy_from_state(mu, r, v)`, `semi_major_axis_from_state(mu, r, v)` | km²/s²; km |
| `eccentricity(rp, ra)`, `apsides(a, e)`, `trajectory_type(e)` | e; (rp, ra); "circle", "ellipse", "parabola", "hyperbola" |
| `conic_radius(p, e, theta)`, `true_anomaly_at_radius(a, e, r)`, `flight_path_angle(e, theta)` | km; deg; deg |
| `orbit_point(a, e, theta, rotate, center)`, `orbit_velocity(mu, a, e, theta, rotate, sense)` | (x, y) km; (vx, vy) km/s |
| `orbit_xy(a, e, n, theta0, theta1, rotate, r_max, center)`, `conic_xy(rp, e, ...)` | arrays x, y; focus at `center`, periapsis along `rotate`; hyperbola clipped at `r_max`; `conic_xy` also does the parabola |
| `time_from_periapsis(mu, a, e, theta)`, `true_anomaly_at_time(mu, a, e, t)` | Kepler's equation, ellipse and hyperbola |
| `hohmann(mu, r1, r2)` | dict: r1, r2, a_t, e_t, v_c1, v_c2, v_tp, v_ta, v_t1, v_t2, dv1, dv2, dv_total (positive), raise, T_t, tof |
| `plane_change(v, di)` | 2 v sin(di/2), km/s |
| `surface_speed(lat)`, `rotation_gain(lat, az)` | km/s (negative westward), mean Earth radius by default |
| `inclination_from_launch(lat, az)`, `launch_azimuths(lat, inc)` | deg; (northbound, southbound) deg, ValueError when out of reach |
| `periapsis_speed_hyperbola(mu, rp, vinf)`, `hyperbola(mu, rp, vinf)` | km/s; dict a, e, p, vp, theta_inf, turn, b |
| `synodic_period(T1, T2)` | in the unit of T1, T2 |
| `ground_track(inc, T, t, lon_node, day, rotating)` | lat, lon arrays, deg (circular orbit) |

## Numbers on the page

- `fmt(x, sig=4)`: significant figures, commas, half up, trailing zeros kept. Digits before
  the decimal point are never rounded away: 26,578.3 gives "26,578" (5 figures), 5,828.5
  gives "5,829". Use `fmt(x, 3)` for "105" from 105.4, and `fmt_dec(x, 1)` for "5,828.5".
- `fmt_dec(x, nd)`: exactly nd decimals. `fmt_sci(x)`: "1.327 \times 10^{11}" for math.
- `record(page, key, text)` (page: tag "p21" or file stem) records a printed number and
  returns it; record the number only ("7.669", not "7.669 km/s"). `check_values.py` then
  finds it on the page after turning `{,}` into "," and `\,`, `\ `, non-breaking spaces into
  spaces; a value must stand alone ("7.6" does not match inside "7.669").

## Drawing helpers

| Helper | Draws |
|---|---|
| `new_axes(w, h, ncols)`, `data_axes(w, h, ncols)`, `map_axes(w)` | schematic (no frame, equal aspect); data plot (light grid, comma ticks); longitude-latitude map |
| `STYLE`, `line_kw(role or i)`, `text_color(role or i)` | roles initial, transfer, final, hyperbola, other, reference, boundary; series 0 to 4 (`SERIES_STYLE`) have their own looks, none the same as a role |
| `draw_body(ax, xy, radius, name=, where=)` | light disc, black outline, label inside or beside; radius=None: a marker (not to scale) |
| `draw_orbit(ax, a, e, role, rotate, theta0, theta1, label=, label_at=, arrows_at=)` | a conic from its equation, motion arrowhead by default |
| `draw_hyperbola(ax, mu, rp, vinf, rotate, branch, r_max)` | branch from rp and v-infinity plus its asymptote; returns geometry, out_dir, end, foot_out |
| `burn(ax, xy, direction, label, length=, side=, center=)` | black dot on the path, arrow along the velocity change beside the path (6 pt outward from `center`, so the head clears the path), label at the tip |
| `burn_lengths(dvs, longest=)` | burn-arrow lengths in proportion to the delta-Vs |
| `velocity_arrow(ax, xy, v, scale, label, offset=)`, `speed_key(ax, xy, scale)` | to-scale vector (offset: beside the orbit); its scale key ("1 km/s") |
| `arrow(ax, p0, p1)`, `line(ax, p0, p1, role)`, `point(ax, xy, label, direction)` | crisp arrow; thin reference line; marked point |
| `dimension(ax, p0, p1, label, offset, label_side)` | dimension line with heads, end ticks, extension lines |
| `radius_arrow(ax, center, r, angle, label)` | a radius from a body's center |
| `angle_arc(ax, center, radius, t0, t1, label)` | angle arc, label on the bisector |
| `text(ax, xy, s, direction=, dist=)`, `callout(ax, xy, s, at)`, `label_curve(...)` | label with white backing, placed clear of xy; label with a short leader; direct curve label |
| `bars(ax, labels, values, styles, bottoms)` | white bars with colored edge and hatch, values on the bars; `bottoms` for a budget |
| `draw_track(ax, lon, lat, role, label=, arrows_at=)` | ground track, broken at the date line; motion arrowheads at the given indices |
| `track_arrow(ax, lon, lat, i, role)` | one motion arrowhead on a ground track |
| `orbit_arrows(ax, rp, e, thetas, rotate, center, role, line=)` | motion arrowheads (`MOTION_HEAD`, 10 x 3 pt) on a conic drawn by hand (`conic_xy` + `ax.plot`; pass its Line2D as `line`) |
| `rides_on(patch, *lines)` | records the line(s) an arrowhead is drawn on, the only lines the gate lets it lie on |
| `Globe(ax, view_lat, view_lon)` | orthographic globe in the chapter style (fill, outline, equator, no grid by default; add `.axis()`); `.circle(radius, inc, raan, role)`, `.plane(radius)`, `.axis()`, `.arc(origin, d0, d1, r, label)`, `.great_arc`, `.point`, `.text`, `.callout`, `.arrow`, `.vec(lat, lon)`, `.orbit_vec(r, inc, raan, u)`; hidden parts dashed |
| `save_figure(fig, name, allow=())` | the only way to save: checks layout, sizes, fonts, contrast; prints the size and a suggested `:width:` |

Style constants: `FIG_WIDTH` 6.5 in, `FS_LABEL` 12 pt, `FS_SMALL` 11 pt, `LW_ORBIT` 2.0 pt,
`LW_ARROW` 1.6 pt, `LW_THIN` 0.9 pt, `HEAD` small 7 x 2.4, normal 9 x 3.1, large 11 x 3.8 pt
(length x half-width), `GRAY` #767676, `GRID` #DDDDDD, `BODY_FILL` per body.

Contrast on white (WCAG), measured with `contrast_ratio()`:

| Role | Line | Ratio | Label text | Ratio | Line style |
|---|---|---|---|---|---|
| initial | #0072B2 | 5.19 | #0072B2 | 5.19 | solid |
| transfer | #D55E00 | 3.87 | #B34E00 | 5.24 | dashed |
| final | #009E73 | 3.42 | #007A5A | 5.34 | dash-dot |
| hyperbola | #CC79A7 | 3.06 | #A0507F | 5.32 | dash-dot-dot |
| other | #000000 | 21.0 | #000000 | 21.0 | dotted |
| reference, boundary | #767676 | 4.54 | #555960 | 7.04 | thin solid; thin dashed |

Globe grid #808B96: 3.47 on white, 3.05 on the globe fill. Black text on every body fill:
15 or more. The data grid (#DDDDDD, 1.36) is decorative and exempt. On the plane ring of a
globe (#F7F3E8) the purple hyperbola line falls to 2.76: do not draw a hyperbola over it.

## How to write a figure function

```python
"""Figures and values of 2.2 Orbit Transfers."""
from chapter_2.orbits import *

E, RE = MU["Earth"], RADIUS["Earth"]
R1, R2 = RE + 400.0, RE + 20200.0          # the worked example, km


def hohmann_figure():
    """Hohmann transfer of the worked example, to scale."""
    h = hohmann(E, R1, R2)
    fig, ax = new_axes(6.5, 5.6)
    draw_orbit(ax, R1, 0.0, "initial", label="initial orbit", label_at=300, arrows_at=(250,))
    draw_orbit(ax, R2, 0.0, "final", label="final orbit", label_at=315)
    draw_orbit(ax, h["a_t"], h["e_t"], "transfer", theta0=0, theta1=180,
               label="transfer orbit", label_at=140)
    draw_body(ax, (0, 0), RE, name="Earth")
    burn(ax, (R1, 0), 90, r"$\Delta V_1$", label_dir=0)       # along the motion: speeds up
    burn(ax, (-R2, 0), 270, r"$\Delta V_2$", label_dir=180)
    radius_arrow(ax, (0, 0), R2, 215, "$r_2$", side=-1)
    x, y = orbit_xy(h["a_t"], h["e_t"], theta0=0, theta1=180)
    close_to(float(np.max(np.hypot(x, y))), R2, 1e-6, "transfer touches the outer circle")
    save_figure(fig, "p22-hohmann")


def make_all():
    hohmann_figure()


def values():
    h = hohmann(E, R1, R2)
    record("p22", "dv1", fmt(h["dv1"]))
    record("p22", "tof-h", fmt(h["tof"] / 3600.0))
```

## Pitfalls

- **Altitude is not radius.** `r = RADIUS["Earth"] + h` everywhere; the helpers take radii.
- **To scale.** Draw schematics in km so `draw_body(ax, (0, 0), RADIUS["Earth"])` and the
  orbits share one scale. A low orbit then hugs the body (400 km is 6% of Earth's radius):
  that is the truth; say so in the text rather than exaggerate. A heliocentric figure cannot
  show planets to scale: use `draw_body(..., radius=None)` (a marker) and say "planets not to
  scale" in the caption.
- **Figure size.** `save_figure` prints the final size and a `:width:` that shows the text
  at body-text size; an equal-aspect figure is as wide as its content, so pick `new_axes`
  width and height close to the content's aspect.
- **Placing labels.** Use `direction=` (the side of the point the label goes on) rather than
  hand offsets; `draw_orbit(label_at=)` pushes labels outward from the focus. When no clear
  spot touches the point, use `callout()`. Run with `FIG_LAYOUT=warn` to list every contact
  at once, then fix each; the message gives the data point of the contact. `allow=` in
  `save_figure` exists for a justified exception: give the reason in a comment.
- **Motion.** Counterclockwise is the default everywhere; `sense=-1` only for a drawn
  retrograde orbit, and say so. Burn arrows point backward to slow down (`direction=` the
  reverse of the velocity).
- **Symbols in figures.** Write `\varepsilon` and `\phi` as on the page; never `^\circ` (it
  falls back to a non-Arial font and the run stops): type "°" outside the math. Avoid
  accents (`\dot`, `\hat`): write the character.
- **Globes.** Call `plane()` before drawing orbits so the parts below the plane are dashed.
  Keep north up (`view_lat` between 15 and 35).
- **Angles on non-equal axes.** `dimension`, `angle_arc` and `burn` directions assume equal
  aspect (schematics). On a data plot use them only for horizontal or vertical lines.
