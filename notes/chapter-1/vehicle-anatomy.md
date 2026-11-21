---
title: "1.3 Vehicle Anatomy"
short_title: 1.3 Vehicle Anatomy
---

:::{include} ../_parts/standards/1.3.md
:::

Aircraft and rocket designers speak a language of their own: the {term}`flap`, the {term}`spoiler`, the {term}`interstage`, the {term}`mean aerodynamic chord`. This page names the parts of an airliner, the Boeing 737-800, and of two {term}`launch vehicles <launch vehicle>`, the Ariane 5 and the Falcon 9. It says what each part does, gives the few numbers that describe a wing and an {term}`airfoil`, and ends with the {term}`mission profile`, the sketch of what a vehicle must do. By the end you can label a drawing of an aircraft, a wing, an airfoil, or a launch vehicle and explain what each part is for. You can also compute the main wing parameters, decode a NACA four-digit airfoil, and sketch a mission profile.

:::{note} What to take from this page
- An airplane is a few large parts with one job each. The {term}`fuselage` carries the payload, the wing makes the lift, the tail keeps the aircraft steady, the engines push, and the landing gear carries it on the ground.
- Three rotations, {term}`roll`, {term}`pitch`, and {term}`yaw`, turn the aircraft about three body axes through its center of gravity. The ailerons, the elevator, and the rudder command them. Flaps, slats, and spoilers change the lift and the drag of the wing.
- A wing is described by its span $b$, area $S$, root and tip chords, taper ratio $\lambda$, sweep, aspect ratio $\textit{AR} = b^2/S$, and mean aerodynamic chord. An airfoil is described by its chord, camber, and thickness, which a NACA four-digit number gives directly.
- A launch vehicle is a stack of {term}`stages <Stage>`, each with its own tanks and engines, dropped one after the other. A mission profile cuts a flight into numbered segments.
:::

## The parts of an airplane

An airliner looks complicated, but it is built from a few large parts, and each has one main job. {numref}`fig-p13-airframe-side` names them on the Boeing 737-800, a twin-engine airliner.

:::{figure} figures/p13-airframe-side.svg
:label: fig-p13-airframe-side
:alt: Side view of a Boeing 737-800, nose to the left, the left side seen, with seven parts named: the long fuselage, the swept wing low on the fuselage, the engine nacelle under the front of the wing, the tall vertical stabilizer at the tail with the hatched rudder hinged to its trailing edge, the horizontal stabilizer at the tail, and the main landing gear under the wing. Windows and doors are drawn in thin gray lines.
:width: 90%

Schematic of the airliner from the side. Each large part has one job: the fuselage holds the payload, the wing lifts, the engines push, the tail surfaces keep the aircraft steady, and the landing gear carries it on the ground. The hatched part is a moving surface, the rudder. Proportions after the Boeing 737-800 (Boeing 2025, Sections 2.2.6 and 2.3.3).
:::

:::{table} The parts of an airplane and what each does (FAA 2023a, Chapter 3).
:label: tbl-p13-airframe
:align: center

| Part | What it does |
| --- | --- |
| {term}`Fuselage` | Holds the crew, passengers, and cargo; joins the wing and the tail |
| Wing | Makes the lift; on an airliner it also holds the fuel and carries the engines |
| {term}`Empennage` (tail group) | The two stabilizers, with the elevator and the rudder hinged to them |
| Horizontal stabilizer | Keeps the nose from pitching up and down on its own (stability in pitch); carries the elevator |
| Vertical stabilizer | Keeps the nose from swinging left and right on its own (stability in yaw); carries the rudder |
| Engine in its nacelle | Makes the thrust; the nacelle is the streamlined casing around it |
| Pylon | The strut the engine hangs from; the engine's weight and thrust pass through it into the wing |
| Landing gear | Carries the aircraft on the ground; the nose gear steers it |
| Winglet | Stands up at the wing tip; it weakens the swirl of air there and so saves fuel |
:::

The two stabilizers keep the aircraft pointed into the airflow, as the tail of a weathervane keeps it pointed into the wind. If a gust pitches the nose up, the horizontal stabilizer meets the air at a new angle, and the force it then makes swings the nose back down. The vertical stabilizer does the same when a gust swings the nose to one side. This tendency to return to steady flight with no action from the pilot is called **{term}`stability`** (FAA 2023a, Chapter 5).

Each engine sits in a streamlined casing, the **nacelle**, and hangs from a short **pylon** under the wing. The side view of {numref}`fig-p13-airframe-side` does not draw the pylon; the view from above, {numref}`fig-p13-moving-surfaces`, shows it. Near the nose, a pitot tube and small static ports feed the airspeed indicator and the altimeter, as [pitot-static instruments](#p15-pitot-static) explains.

Seen from ahead, in {numref}`fig-p13-front-view`, three more features show. The wing rises from the root to the tip: the upward angle it makes with the horizontal is the **{term}`dihedral`** angle, 6° on the 737-800 drawing. A gust that rolls the aircraft also makes it slip sideways toward the low wing. With dihedral, the low wing then meets the air at a steeper angle and makes more lift than the high wing, and the wings roll level again (FAA 2023a, Chapter 5). The engines hang low and close to the fuselage. At each wing tip a **{term}`winglet`** stands up. Air flows around the tip from the high-pressure lower surface to the low-pressure upper surface, and this swirl, the wingtip vortex, costs energy that the engines have to supply; the winglet weakens it.

:::{figure} figures/p13-front-view.svg
:label: fig-p13-front-view
:alt: Front view of the Boeing 737-800. The fuselage is a round section in the middle; the wing rises from the fuselage toward the tips at a dihedral angle of 6 degrees, marked between a horizontal line and the lower surface of the wing outboard of the engine; a winglet rises from each tip and leans slightly outward; the two engine nacelles hang just under the wing close to the fuselage. Behind the wing, the horizontal stabilizer reaches out on each side and the thin vertical stabilizer stands above the fuselage. The nose landing gear is under the fuselage and the two main landing gear legs are under the wing roots.
:width: 90%

Schematic of the airliner from ahead. The wing rises toward the tips at the dihedral angle, the engines hang under the wing, each winglet stands up at a tip, and the tail surfaces show behind the wing. Proportions as in {numref}`fig-p13-airframe-side`.
:::

:::{warning} Stabilizer or control surface
The horizontal and vertical stabilizers do not move: they keep the aircraft steady. The elevator and the rudder are the moving surfaces hinged to their trailing edges, and they turn the aircraft. On a drawing, check whether the part named is the fixed surface or the hinged one behind it.
:::

## Axes and control surfaces

The motion of an aircraft is described with three axes fixed to the aircraft. They cross at the **{term}`center of gravity`**, the point where the whole weight can be taken to act.

:::{prf:definition} Body axes, roll, pitch, and yaw
:label: def-p13-axes

The **{term}`body axes`** are three perpendicular axes through the center of gravity, fixed to the aircraft: $x$ points forward through the nose, $y$ out along the right wing, and $z$ down. A rotation about $x$ is **roll**, about $y$ is **pitch**, and about $z$ is **yaw**. A positive roll lowers the right wing, a positive pitch raises the nose, and a positive yaw swings the nose to the right.
:::

The axes form a right-handed set: curl the fingers of your right hand from $x$ toward $y$ and your thumb points along $z$. With the thumb along any axis, the fingers curl the way a positive rotation turns. {numref}`fig-p13-body-axes` shows the axes in three views. In each, one axis points out of the page or into it (a dot or a cross), and the view shows the rotation about that axis.

:::{figure} figures/p13-body-axes.svg
:label: fig-p13-body-axes
:alt: The Boeing 737-800 in three views at one scale, a thin gray outline, with the body axes through the center of gravity in heavy black. Side view, nose to the left: x forward, z down, y into the page; a curved arrow just ahead of the nose, turning upward, is labeled positive pitch, nose up, elevator. Top view from above, nose to the left: x forward, y up the page toward the wing labeled right wing, z into the page; a curved arrow ahead of the nose, turning toward the right wing, is labeled positive yaw, nose right, rudder. Front view: x toward the reader, y toward the right wing, on the reader's left, z down; a curved arrow beyond the right wing tip, turning down, is labeled positive roll, right wing down, ailerons. A key says a dot is an axis pointing toward you and a cross one pointing away.
:width: 90%

Schematic of the body axes in three views. Each rotation turns the aircraft about one body axis, and one set of surfaces commands it: the elevator pitches, the rudder yaws, and the ailerons roll. Each curved arrow shows the positive sense. The center of gravity is placed near the wing root; proportions as in {numref}`fig-p13-airframe-side`.
:::

Three moving surfaces, the **primary flight controls**, command the three rotations (FAA 2023a, Chapter 6):

- The **{term}`ailerons <Aileron>`**, near the tip of each wing, move in opposite directions. Deflecting an aileron down increases the camber of that part of the wing, and with it the lift there. (Camber, the curve of the airfoil, is defined under [airfoil geometry](#p13-airfoil).) The raised aileron on the other wing reduces its lift. One wing goes up, the other down, and the aircraft rolls.
- The **{term}`elevator`**, hinged to the horizontal stabilizer, pitches the aircraft. When the pilot pulls the control column back, the elevator's trailing edge goes up, the tail makes a downward force, the tail moves down, and the nose pitches up about the center of gravity. {numref}`fig-p13-control-deflection` draws this chain in order.
- The **{term}`rudder`**, hinged to the vertical stabilizer, yaws the aircraft. Deflected to the left, it makes a sideways force to the right on the tail, which swings the nose to the left.

:::{figure} figures/p13-control-deflection.svg
:label: fig-p13-control-deflection
:alt: Side view of the Boeing 737-800, nose to the left, in thin gray, with three numbered steps. Step 1, in an enlargement of the tail, 7 times, below: the horizontal stabilizer drawn as an airfoil section with its elevator turned trailing edge up about the hinge, a dot labeled hinge; the elevator is hatched, next to its neutral position, dashed. Step 2: a heavy arrow pointing down from the horizontal stabilizer, labeled force on the tail, down. Step 3: a curved arrow just ahead of the nose, turning upward about the center of gravity, labeled the nose pitches up.
:width: 90%

Schematic. A control surface turns the aircraft in three steps: the surface moves (1), the air pushes on it (2), and the aircraft rotates about its center of gravity (3). The downward force acts far behind the center of gravity, so it pitches the nose up. Proportions as in {numref}`fig-p13-airframe-side`.
:::

Other moving surfaces change how much lift and drag the wing makes. These are the secondary controls, placed on the wing in {numref}`fig-p13-moving-surfaces` and drawn in section in {numref}`fig-p13-high-lift`:

- **{term}`Flaps <Flap>`** on the trailing edge move down and, on an airliner, also back. They add camber and wing area, so the wing makes enough lift at the low speeds of takeoff and landing. They also add drag.
- **{term}`Slats <Slat>`** on the leading edge move forward and down and open a slot that guides air from the lower surface over the upper surface. The wing can then fly at a steeper angle to the air before the flow breaks away from its upper surface (a {term}`stall`).
- **Spoilers** are panels on top of the wing that rise to spoil the smooth flow over it, which reduces the lift and increases the drag. Raised on both wings, they let the aircraft descend without gaining speed. Raised on one wing, they help roll it. On the runway, they shorten the landing roll (FAA 2023a, Chapter 6).

:::{figure} figures/p13-moving-surfaces.svg
:label: fig-p13-moving-surfaces
:alt: Top view of the Boeing 737-800 seen from above, nose to the left, with every moving surface hatched. The wing at the top is labeled right wing and the one at the bottom left wing. Named on the right wing: the slats along the leading edge; the spoilers, a row of five panels on top of the wing ahead of the outboard flap and one panel ahead of the inboard flap; the inboard flap and the outboard flap along the trailing edge; the aileron near the tip; and the elevator on the trailing edge of the horizontal stabilizer. Named on the left wing: the pylon that joins each nacelle to the wing, a narrow strip from the middle of the nacelle to the wing's leading edge.
:width: 90%

Schematic of the moving surfaces seen from above. They line the edges of the wing and the tail: slats along the leading edge, flaps and ailerons along the trailing edge, and spoilers on top just ahead of the flaps. The hatched parts move; the pylon, named on the left wing, is fixed. The rudder, on the vertical stabilizer, does not show from above. Spans and chords of the surfaces are schematic; proportions as in {numref}`fig-p13-airframe-side`.
:::

:::{figure} figures/p13-high-lift.svg
:label: fig-p13-high-lift
:alt: One airfoil drawn twice at one scale. Above, clean, as in cruise: the slat at the leading edge, the main wing, the spoiler lying on the upper surface, and the flap at the trailing edge fit together into one airfoil. Below, after touchdown: the slat has moved forward and down, leaving a slot behind it; the flap has moved back and down, leaving a slot ahead of it; and the spoiler is raised. A thin arrow labeled air runs through each slot, from under the wing to over the piece behind the slot. The slat, flap, and spoiler are hatched.
:width: 90%

Schematic of one cambered airfoil cut into its pieces, with the positions, angles, and slot widths chosen for clarity. Extended, the slat and the flap make the airfoil longer and more curved, and the slots guide air from the lower surface over the upper one (thin arrows); a raised spoiler breaks up the flow over the top.
:::

:::{table} The moving surfaces of an airliner (FAA 2023a, Chapter 6).
:label: tbl-p13-surfaces
:align: center

| Surface | Where | What it does |
| --- | --- | --- |
| Aileron | Trailing edge, near each wing tip | Rolls the aircraft; the two move in opposite directions |
| Elevator | Trailing edge of the horizontal stabilizer | Pitches the nose up or down |
| Rudder | Trailing edge of the vertical stabilizer | Yaws the nose left or right |
| Flap | Trailing edge, between the fuselage and the aileron | More lift (and drag) at the low speeds of takeoff and landing |
| Slat | Leading edge | Lets the wing fly at a steeper angle before it stalls |
| Spoiler | Top of the wing, ahead of the flaps | Less lift and more drag; helps roll |
:::

:::{warning} Which way is right
In a top view seen from above with the nose to the left, the right wing is at the top of the page. Drawn with the nose to the right, the right wing is at the bottom. Before naming a "left aileron" or drawing a $y$ axis, place yourself in the aircraft, facing the nose, and check which wing is on your right.
:::

## Landing gear arrangements

The landing gear holds the aircraft up on the ground, lets it steer, and keeps it from tipping over. {numref}`fig-p13-gear-layouts` draws the six arrangements named by Raymer (2006), each from the side and from below.

:::{figure} figures/p13-gear-layouts.svg
:label: fig-p13-gear-layouts
:alt: Six drawings of one generic airplane, each a side view above a view from below, with the wheels in black and the center of gravity, a quartered circle, at the same station in both views. Tricycle: a nose wheel and two main wheels under the wing just behind the center of gravity; it sits level. Tail-dragger: main wheels under the wing ahead of the center of gravity and a tail wheel; it sits nose up. Multi-bogie: a nose wheel and a four-wheel bogie under each wing. Bicycle: two main wheels in line under the fuselage, one each side of the center of gravity, and outriggers at the wing tips; in its side view the outrigger stands between the main wheels and is named outrigger, at the wing tip. Single main: one main wheel just ahead of the center of gravity, a tail wheel, and tip outriggers. Quadricycle: four main wheels under the fuselage, two pairs around the center of gravity, and tip outriggers.
:width: 85%

Schematic of six landing-gear arrangements, each from the side and from below. What sets each apart is where the main wheels stand relative to the center of gravity and how many wheels share the weight. Arrangements as named by Raymer (2006).
:::

:::{table} Landing gear arrangements (FAA 2023b, Chapter 13; names after Raymer 2006).
:label: tbl-p13-gear
:align: center

| Arrangement | Where the wheels are | One reason to choose it | Example |
| --- | --- | --- | --- |
| Tricycle | Nose wheel; main wheels just behind the center of gravity | Hard braking without nosing over, a good view ahead, no ground loop | Boeing 737 |
| Tail-dragger (conventional) | Main wheels ahead of the center of gravity; a tail wheel | Light, and the nose-up stance clears a long propeller and rough ground | Douglas DC-3 |
| Multi-bogie | Nose wheel; several wheels on each main leg (a bogie) | Spreads a heavy weight over the runway | Boeing 777 |
| Bicycle (tandem) | Two main units in line under the fuselage; small outriggers under the wings | Leaves the wing free of gear, so it can be thin and flexible | Harrier, B-47 |
| Single main | One main wheel just ahead of the center of gravity, a tail wheel or skid | The lightest gear, for slow aircraft such as sailplanes | Sailplanes |
| Quadricycle | Four main units at the corners of a rectangle | Carries a large weight with the fuselage level and close to the ground | B-52 |
:::

The tricycle arrangement is the most common, on small and large aircraft alike; the table gives the three reasons the FAA lists (FAA 2023b, Chapter 13). A **{term}`ground loop`** is a sudden swerve on the ground. A tail-dragger can fall into one because its center of gravity is behind the main wheels: once the aircraft starts to turn, the weight keeps pushing it further around. In a tricycle the center of gravity is ahead of the main wheels, so the weight pulls the aircraft straight.

(p13-wing-geometry)=
## Wing geometry

Seen from above, a wing is a flat shape, its **{term}`planform`**. Most wings are close to a trapezoid on each side of the centerline, a **straight-tapered** wing, and a few numbers describe it.

:::{prf:definition} Wing span, wing area, and chord
:label: def-p13-span-area

The **wing span** $b$ is the distance from one wing tip to the other. The **wing area** $S$ is the area of the planform seen from above, including the part that runs through the fuselage to the centerline. A **{term}`chord`** is the distance from the leading edge to the trailing edge, measured parallel to the centerline. The **root chord** $c_r$ is the chord at the centerline, and the **tip chord** $c_t$ is the chord at the tip.
:::

A real wing has kinks and rounded tips. Designers replace it with a **reference wing**: the straight-tapered wing with the same span and area, extended through the fuselage to the centerline. Each half is a trapezoid with parallel sides $c_r$ and $c_t$ and height $b/2$, so the area of the whole wing is

:::{math}
:label: eq-p13-area
S = 2 \cdot \frac{b}{2}\cdot\frac{c_r + c_t}{2} = \frac{b\,(c_r + c_t)}{2}
:::

Two ratios and one angle describe the shape, whatever the size of the wing.

:::{prf:definition} Taper ratio, aspect ratio, and sweep
:label: def-p13-ratios

The **{term}`taper ratio`** is the tip chord over the root chord, $\lambda = c_t/c_r$: 1 for a rectangular wing, 0 for a wing that comes to a point. The **{term}`aspect ratio`** is the span squared over the area, $\textit{AR} = b^2/S$: a long, narrow wing has a high aspect ratio. The **{term}`sweep`** $\Lambda$ is the angle between a line along the wing, such as its leading edge, and a line perpendicular to the centerline. The sweep usually quoted is that of the quarter-chord line, which runs one quarter of the chord behind the leading edge.
:::

For a rectangular wing, $S = b\,c$ and the aspect ratio is the span over the chord. For any planform, $b^2/S$ is the span over the average chord. The jet airliners in the tables of Jenkinson et al. (1999, Data A) have aspect ratios from about 7 to 9.5. A long, narrow wing makes the same lift with less of the drag caused by the wingtip vortices; Chapter 3 covers that drag.

Writing $c_t = \lambda c_r$ in {eq}`eq-p13-area` gives the area in terms of the root chord, and solving for the root chord gives

:::{math}
:label: eq-p13-root-chord
\begin{aligned}
S &= \frac{b\,c_r\,(1 + \lambda)}{2}\\
c_r &= \frac{2S}{b\,(1 + \lambda)}
\end{aligned}
:::

One more number ties the wing to the weight of the aircraft.

:::{prf:definition} Wing loading
:label: def-p13-wing-loading

The **{term}`wing loading`** is the {term}`takeoff weight` divided by the wing area, $W_0/S$, in lb/ft² (or N/m²). It measures how big the wing is for the aircraft it must lift: the higher the wing loading, the smaller the wing and the faster the aircraft must fly to make enough lift.
:::

### Mean aerodynamic chord

A tapered wing has a different chord at every station (a position along the span, measured from the centerline), so one length is defined to stand for the whole wing: the **mean aerodynamic chord** $\bar{c}$. It is the average chord in which each strip of the wing counts in proportion to its area:

:::{math}
:label: eq-p13-mac-integral
\bar{c} = \frac{2}{S}\int_{0}^{b/2} c(y)^2\,dy
:::

For a straight-tapered wing, whose chord falls in a straight line from $c_r$ at the root to $\lambda c_r$ at the tip, the integral gives

:::{math}
:label: eq-p13-mac
\bar{c} = \frac{2}{3}\,c_r\,\frac{1 + \lambda + \lambda^2}{1 + \lambda}
:::

The mean aerodynamic chord lies at $y_{\bar{c}} = (b/6)\,(1 + 2\lambda)/(1 + \lambda)$ from the centerline. Panel (b) of {numref}`fig-p13-wing-planform` finds it without a formula:

1. Extend the root chord rearward by the tip chord.
2. Extend the tip chord forward by the root chord.
3. Join the two ends.
4. Where that line crosses the **mid-chord line** (through the middle of every chord) is the station of the mean aerodynamic chord.

The mean aerodynamic chord is the reference length for the pitching of a wing, and the center of gravity is often quoted as a percentage of it.

:::{tip} Method: wing parameters from published data
1. Put every length in one unit (feet here, as in Raymer) and the area in the square of that unit.
2. Aspect ratio: $\textit{AR} = b^2/S$.
3. Root and tip chords of the reference wing: $c_r = 2S/[b\,(1 + \lambda)]$ and $c_t = \lambda c_r$.
4. Mean aerodynamic chord: {eq}`eq-p13-mac`, and its station $y_{\bar{c}} = (b/6)(1 + 2\lambda)/(1 + \lambda)$.
5. Wing loading: $W_0/S$.
6. Check: for a jet airliner, $\textit{AR}$ between about 7 and 9.5; $\bar{c}$ always lies between $c_t$ and $c_r$.
:::

### Worked example: the wing of the Boeing 737-800

Jenkinson et al. (1999, Data A, Table 2) give the 737-800 a wing area of $S = 124.60\ \text{m}^2$, a span of $b = 34.30\ \text{m}$, and a taper ratio of $\lambda = 0.278$, with the quarter-chord line swept back 25°. Its maximum design takeoff weight, in its highest option, is 174,200 lb (Boeing 2025, Section 2.1.3). Find the aspect ratio, the root and tip chords, the mean aerodynamic chord, and the wing loading.

1. **Units.** With 1 ft = 0.3048 m, and so 1 ft² = 0.092903 m²:
   $$
   \begin{aligned}
   b &= \frac{34.30\ \text{m}}{0.3048\ \text{m/ft}}\\
     &= 112.53\ \text{ft}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   S &= \frac{124.60\ \text{m}^2}{0.092903\ \text{m}^2/\text{ft}^2}\\
     &= 1{,}341.2\ \text{ft}^2
   \end{aligned}
   $$
2. **Aspect ratio.**
   $$
   \begin{aligned}
   \textit{AR} &= \frac{b^2}{S}\\
               &= \frac{{112.53}^{2}\ \text{ft}^2}{1{,}341.2\ \text{ft}^2}\\
               &= \frac{12{,}663}{1{,}341.2}\\
               &= 9.442
   \end{aligned}
   $$
   This agrees with the published 9.44.
3. **Root and tip chords**, {eq}`eq-p13-root-chord`:
   $$
   \begin{aligned}
   c_r &= \frac{2S}{b\,(1 + \lambda)}\\
       &= \frac{2{,}682.4\ \text{ft}^2}{112.53\ \text{ft} \times 1.278}\\
       &= \frac{2{,}682.4}{143.81}\\
       &= 18.65\ \text{ft}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   c_t &= \lambda\,c_r\\
       &= 0.278 \times 18.65\\
       &= 5.185\ \text{ft}
   \end{aligned}
   $$
4. **Mean aerodynamic chord**, {eq}`eq-p13-mac`, with ${0.278}^{2} = 0.077284$:
   $$
   \begin{aligned}
   \bar{c} &= \frac{2}{3}\,c_r\,\frac{1 + \lambda + \lambda^2}{1 + \lambda}\\
           &= \frac{2}{3} \times 18.65 \times \frac{1.3553}{1.278}\\
           &= \frac{2}{3} \times 18.65 \times 1.0605\\
           &= 13.19\ \text{ft}
   \end{aligned}
   $$
   and its station, with $b/6 = 18.7555$ ft:
   $$
   \begin{aligned}
   y_{\bar{c}} &= \frac{b}{6}\cdot\frac{1 + 2\lambda}{1 + \lambda}\\
               &= 18.7555 \times \frac{1.556}{1.278}\\
               &= 18.7555 \times 1.21753\\
               &= 22.84\ \text{ft}
   \end{aligned}
   $$
5. **Wing loading.**
   $$
   \begin{aligned}
   \frac{W_0}{S} &= \frac{174{,}200\ \text{lb}}{1{,}341.2\ \text{ft}^2}\\
                 &= 129.9\ \text{lb/ft}^2
   \end{aligned}
   $$

**Check.** The aspect ratio is in the airliner range, and the mean aerodynamic chord lies between the tip chord and the root chord. Jenkinson et al. give a mean aerodynamic chord of 4.17 m, or 13.68 ft, 3.7% more than this result. The likely reason is the kink in the 737's trailing edge near the fuselage: the real planform has more area near the root than the reference trapezoid, which lengthens its mean chord. {numref}`fig-p13-wing-planform` draws the reference wing with these numbers.

:::{figure} figures/p13-wing-planform.svg
:label: fig-p13-wing-planform
:alt: Two panels at one scale. Panel a: the 737-800 reference wing seen from above, leading edge on top, with a forward arrow, shaded; its area S is 1,341.2 square feet, its span b 112.53 feet, its root chord c r 18.65 feet, and its tip chord c t 5.185 feet; a dash-dot quarter-chord line on the left half is swept back 25 degrees. Panel b: the right half-wing with the four numbered steps: 1, the root chord extended rearward by the tip chord; 2, the tip chord extended forward by the root chord; 3, a line joining the two ends; 4, its crossing with the dashed mid-chord line, where a heavy chord marks the mean aerodynamic chord, 13.19 feet long, 22.84 feet from the centerline.
:width: 90%

Computed from the published span, area, and taper ratio of the Boeing 737-800. Panel (a) gives the numbers that describe the wing: the sweep and any three of the other four fix it, because the area follows from the span and the two chords. Panel (b) finds the mean aerodynamic chord in four steps: where the line joining the two extended chords crosses the mid-chord line, 22.84 ft from the centerline. Data from Jenkinson et al. (1999, Data A, Table 2).
:::

:::{warning} Common slips with wing numbers
- The span $b$ is tip to tip. Using the length of one wing, $b/2$, in $b^2/S$ makes the aspect ratio four times too small.
- Mixing meters and feet: convert the span and the area to one system first, and remember that an area converts with the square of the length factor (1 m² is 10.764 ft², not 3.281 ft²).
- Wing loading uses the weight in pounds over the area in square feet. With a mass in kilograms, multiply by $g_0$ to get a weight in newtons, and use square meters.
:::

(p13-airfoil)=
## Airfoil geometry and NACA four-digit airfoils

Cut a wing with a plane parallel to the centerline and the cut shows the **airfoil** (also called a wing section), the cross-section shape of the wing. {numref}`fig-p13-airfoil-parts` names its parts.

:::{figure} figures/p13-airfoil-parts.svg
:label: fig-p13-airfoil-parts
:alt: A cambered airfoil, the NACA 4418, drawn from its equations, about five times longer than it is thick, rounded at the front and sharp at the back. Named: the leading edge at the front point; the trailing edge at the rear point; the straight dashed chord line joining them; the dash-dot mean camber line, which curves above the chord line; the maximum camber, a small dimension between the chord line and the mean camber line at 40 percent of the chord; the maximum thickness, a dimension between the surfaces at 30 percent of the chord; and the chord c, a dimension below the airfoil from leading edge to trailing edge.
:width: 90%

Computed from the NACA four-digit equations for the NACA 4418. Three lines fix an airfoil: the straight chord line, the curved mean camber line, and the thickness laid on either side of the camber line. Equations from Jacobs et al. (1933).
:::

:::{prf:definition} The parts of an airfoil
:label: def-p13-airfoil

The **leading edge** is the front point of the airfoil and the **trailing edge** the rear point. The **chord line** is the straight line joining them, and its length is the **chord** $c$. The **mean camber line** is the line halfway between the upper and the lower surfaces. The **{term}`camber`** is the distance between the mean camber line and the chord line, and the **thickness** is the distance between the upper and the lower surfaces. Both are usually given at their largest value, as a fraction or a percentage of the chord.
:::

An airfoil with no camber is **symmetric**: its surfaces are mirror images and its mean camber line lies on the chord line. It makes no lift when the air meets it along the chord line, while a cambered airfoil already makes some. Most wings are cambered; most tails, which must push both up and down, are symmetric.

The National Advisory Committee for Aeronautics (NACA), the forerunner of NASA, built families of airfoils from equations, so that four digits fix the whole shape (Jacobs et al. 1933; Abbott and von Doenhoff 1959).

:::{prf:definition} NACA four-digit airfoil
:label: def-p13-naca

In the NACA four-digit designation **MPXX**:
- **M**, the first digit, is the maximum camber in percent of the chord;
- **P**, the second digit, is the position of the maximum camber, in tenths of the chord from the leading edge;
- **XX**, the last two digits, are the maximum thickness in percent of the chord.

In every airfoil of the family the maximum thickness is at 30% of the chord. A designation that starts with 00 is a symmetric airfoil.
:::

{numref}`fig-p13-naca-digits` changes one digit at a time.

:::{figure} figures/p13-naca-digits.svg
:label: fig-p13-naca-digits
:alt: Three rows, each overlaying two NACA airfoils at the same chord, the first one named dashed and the second solid, with the changing digits in bold. Each mean camber line is dash-dot with a dot at its highest point; in the first row the mean camber line and its highest point are named. Row 1, first digit, maximum camber: NACA 0016, dashed, symmetric with a flat camber line, against NACA 4416, solid, whose camber line rises 4 percent of the chord. Row 2, second digit, where the camber is largest: NACA 4216, dashed, peak at 20 percent of the chord, against NACA 4616, solid, peak at 60 percent of the chord; both peaks are named. Row 3, last two digits, thickness: NACA 4408, dashed and thin, against NACA 4424, solid and thick, with the same camber line.
:width: 90%

Computed from the NACA four-digit equations, all at one chord. Each digit changes one feature: the first the height of the camber line, the second where it peaks, the last two the thickness. In each row the first airfoil named is dashed and the second solid; the changing digits are in bold. Equations from Jacobs et al. (1933).
:::

:::{tip} Method: decoding a NACA four-digit airfoil
1. Split the number into M, P, and XX.
2. Maximum camber: M% of the chord; multiply by $c$ for a length.
3. Its position: P tenths of the chord from the leading edge, that is $10\,P$% of the chord; multiply by $c$.
4. Maximum thickness: XX% of the chord, at 30% of the chord from the leading edge; multiply by $c$.
5. If M = 0, the airfoil is symmetric: there is no camber and no position of maximum camber.
:::

### Worked example: decoding two airfoils

Many wings change airfoil along the span: thick at the root, where the structure carries the largest loads, and thinner at the tip. The Douglas DC-3, for example, has a NACA 2215 at the root and a NACA 2206 at the tip (Lednicer 2026). Suppose a wing with the root and tip chords of the worked example above, $c_r = 18.65$ ft and $c_t = 5.185$ ft, used these two airfoils. Find the camber, its position, and the thickness of each, as a percentage and as a length.

1. **Root, NACA 2215** (M = 2, P = 2, XX = 15):
   - maximum camber 2% of the chord: $0.02 \times 18.65 = 0.3730$ ft;
   - at 2 tenths, 20% of the chord, from the leading edge: $0.20 \times 18.65 = 3.730$ ft;
   - maximum thickness 15% of the chord: $0.15 \times 18.65 = 2.798$ ft (33.6 in), at 30% of the chord.
2. **Tip, NACA 2206** (M = 2, P = 2, XX = 06):
   - maximum camber 2%: $0.02 \times 5.185 = 0.1037$ ft;
   - at 20% of the chord: $0.20 \times 5.185 = 1.037$ ft;
   - maximum thickness 6%: $0.06 \times 5.185 = 0.3111$ ft (3.73 in).

**Check.** The two airfoils have the same camber line shape (the same M and P). The tip airfoil is both smaller, because its chord is shorter, and relatively thinner, 6% against 15%. {numref}`fig-p13-naca-example` draws both at one scale.

:::{figure} figures/p13-naca-example.svg
:label: fig-p13-naca-example
:alt: Two airfoils drawn to one scale, then the same two drawn to one chord. Top, the NACA 2215 root airfoil, 18.65 feet long, with its maximum thickness of 2.798 feet marked at 30 percent of the chord and its maximum camber of 0.3730 feet marked 3.730 feet behind the leading edge. Middle, the NACA 2206 tip airfoil, drawn as an outline, 5.185 feet long and much smaller, with its maximum thickness of 0.3111 feet and its maximum camber of 0.1037 feet, 1.037 feet from the leading edge. Bottom, the two airfoils drawn to the same chord, the 2215 solid and the 2206 dashed inside it, their thicknesses marked as 15 percent and 6 percent of the chord.
:width: 90%

Computed from the NACA four-digit equations for the worked example. The digits give fractions of the chord, and the lengths follow from the chord: the tip airfoil is both smaller and, drawn to the same chord, relatively thinner. Equations from Jacobs et al. (1933).
:::

:::{warning} Reading the digits
- The second digit is in tenths of the chord, not percent: P = 4 means 40% of the chord.
- The digits are read in order. In NACA 4418 the camber is 4% and the thickness 18%, not the other way around.
- A percentage is not a length. Multiply by the chord, in the unit the chord is given in.
:::

## The launch vehicle

A launch vehicle carries a payload, a satellite or a spacecraft, from the ground to its orbit. How it gains the speed to stay there is the subject of [launch to orbit](../chapter-2/launch-to-orbit.md). Most of its mass is propellant: the core stage of the Ariane 5 ECA has a dry mass of 14.7 t (1 t is 1,000 kg) and carries 170 t of liquid oxygen and liquid hydrogen (Arianespace 2016, Section 1.5.1). Most of the vehicle is also thrown away on the way up. {numref}`fig-p13-launcher-parts` names the outside of a heavy launch vehicle, the Ariane 5. The launch vehicles of this page are drawn lying down with the nose to the right, so "ahead of" means toward the nose and "behind" toward the engines.

:::{figure} figures/p13-launcher-parts.svg
:label: fig-p13-launcher-parts
:alt: The Ariane 5 lying on its side, nose to the right, with an arrow marking up at liftoff. A long core stage runs from the main engine at the left end to the upper stage; two solid rocket boosters, slimmer and with pointed noses, are strapped along the core stage, one above and one below, each with a large nozzle at the left. Named: main engine, solid rocket booster, booster nozzle, and the forward attachment, a short beam between the core and a booster just behind the booster's nose. Braces under the vehicle give the extent of the core stage, the upper stage, and the payload fairing, the long rounded nose.
:width: 90%

Schematic of a heavy launch vehicle, the Ariane 5 ECA. The stack is built in the order it is used: two solid boosters and the core stage lift it off the pad, the upper stage sits ahead of the core, and the payload rides at the nose under its fairing. The upper stage includes its interstage and the equipment bay, both named in the next figure. Proportions after Arianespace (2016, Section 1.5.1); booster position, attachments, and nozzle sizes estimated.
:::

:::{prf:definition} Stage
:label: def-p13-stage

A **{term}`stage`** is a complete rocket within a launch vehicle: its own propellant tanks, its own engines, and its own structure. When its propellant is used up, the stage is dropped and the next one lights, so the rest of the climb no longer pushes the weight of empty tanks and idle engines.
:::

The parts of the Ariane 5 are:

- **Solid rocket boosters.** Each is a steel case 31.6 m long and 3.05 m across (Arianespace 2016, Section 1.5.1), filled with solid propellant in three segments. Together they give about 92% of the thrust at liftoff (ESA n.d.a).
- **Core stage** (main stage). A 5.4 m cylinder 31 m long with one engine, the Vulcain 2, burning liquid hydrogen with liquid oxygen. It runs from liftoff until the vehicle is above the atmosphere.
- **Upper stage.** A short stage with its own tanks and engine. It finishes the climb to orbit.
- **Interstage.** A short cylinder between two stages. It surrounds the engine of the upper stage and carries the separation system at its top, so it falls away with the lower stage (Arianespace 2016, Section 1.5.1).
- **Equipment bay.** The ring of avionics: the computers, the guidance sensors, and the radios that steer the vehicle.
- **Payload adapter.** The cone that holds the {term}`payload` on the upper stage and releases it in orbit.
- **{term}`Payload fairing`.** A light shell, here 17 m long, that shields the payload on the climb through the atmosphere: from the air pressing on it, from the heating, and from the noise (Arianespace 2016, Chapter 3).

A rocket engine burns a fuel with an oxidizer, and it has to keep working above the atmosphere, where there is no oxygen to take in. A liquid stage therefore carries both, each in its own tank. {numref}`fig-p13-launcher-cutaway` cuts the Ariane 5 open. In the core stage the liquid-oxygen tank sits ahead of the liquid-hydrogen tank (above it when the vehicle stands on the pad). One shared dome, the **common bulkhead**, separates the two (Arianespace 2016, Annex 4). It saves the length and the weight of a second pair of domes. ESA gives the contents of the first version of this stage: 133 t of liquid oxygen in 120 m³ and 26 t of liquid hydrogen in 390 m³ (ESA n.d.b).

:::{figure} figures/p13-launcher-cutaway.svg
:label: fig-p13-launcher-cutaway
:alt: The Ariane 5 cut open lengthwise, nose to the right, with an arrow marking up at liftoff; each propellant is tinted and hatched: liquid oxygen with diagonal hatching, liquid hydrogen with dots, the solid propellant with cross-hatching. Numbered key, from the tail to the nose: 1, the solid propellant, the grain, filling each booster; 2, the central channel along the booster's axis; 3, the long liquid-hydrogen tank of the core stage; 4, the common bulkhead, a dome that bulges into the hydrogen tank; 5, the liquid-oxygen tank, ahead of the hydrogen tank; 6, the payload under the fairing. A rectangle around the upper part is enlarged 2.7 times below the vehicle. In the enlargement, named: the upper-stage engine; the interstage around it; the upper-stage liquid-oxygen tank, a sphere behind the liquid-hydrogen tank, set into its rear dome; the liquid-hydrogen tank ahead of it, which fills the stage from wall to wall; the equipment bay; and the payload adapter seated on the bay.
:width: 90%

Schematic of the same vehicle cut open. Most of a launch vehicle is propellant: each liquid stage carries a fuel tank and an oxidizer tank, and each booster a solid grain. Proportions after Arianespace (2016, Section 1.5.1 and Annex 4) and, for the tank volumes, ESA (n.d.b); the inside of the upper stage and the boosters' channel estimated.
:::

The solid propellant of each booster is cast as a rubbery block, the **grain**, with a channel along its axis. It burns on the surface of the channel and outward toward the case, so the shape of the channel sets the burning area, and with it the thrust. A solid motor cannot be turned off; it burns until its grain is gone.

:::{table} The parts of the Ariane 5, what each does, and when it leaves the vehicle, in the order of a flight (Arianespace 2016, Figure 2.3.a and Section 3.3.3.2; times and altitudes from ESA n.d.a and n.d.b).
:label: tbl-p13-launcher
:align: center

| Part | What it does | When it leaves the vehicle |
| --- | --- | --- |
| Solid rocket boosters | About 92% of the thrust at liftoff | 1. Burned out, about 132 s after liftoff, at about 60 km |
| Payload fairing | Shields the payload in the atmosphere | 2. Once the air is so thin that the heating of the bare payload stays below 1,135 W/m² |
| Core stage with its engine and the interstage | Thrust from liftoff to above the atmosphere | 3. At engine shutdown, just under 10 min after liftoff, at about 145 km (first version) |
| Upper stage, equipment bay, and payload adapter | Finish the climb to orbit and steer the vehicle | 4. Stay together to the end; the payload is released from the adapter |
:::

The core-stage engine is started and checked on the pad; only then are the boosters lit, and the vehicle lifts off. The parts then leave in the order of {numref}`tbl-p13-launcher`.

The Falcon 9, in {numref}`fig-p13-two-stage`, is a different design: two stages, no boosters, and one pair of propellants, rocket-grade kerosene (RP-1) and liquid oxygen, in both stages. It is 70 m tall and 3.66 m across. Nine engines, eight in a ring around one, power the first stage, and one engine built for vacuum powers the second. In the first stage a common dome separates the oxygen tank from the kerosene tank behind it, and a transfer tube carries the oxygen through the kerosene tank to the engines. The interstage is fixed to the forward end of the first stage and stays with it (SpaceX 2025, Section 2). It carries four grid fins, which steer the stage through the atmosphere on its way back, and four landing legs fold against the rear of the stage.

:::{figure} figures/p13-two-stage.svg
:label: fig-p13-two-stage
:alt: The Falcon 9 cut open lengthwise, nose to the right, in two pieces at one scale, cut where the stages separate; an arrow marks up at liftoff. Lower piece, the first stage: the nine engine bells at the left, three of them seen, labeled nine engines, three seen; landing legs folded against the sides at its aft end; a kerosene tank with an oxygen transfer tube running through it; a common dome, drawn flat and labeled so; a long liquid-oxygen tank ahead of it; and at the right the empty interstage, an open cylinder with a grid fin on each side; dashed ticks at its open end mark where the stages separate. Upper piece: the vacuum engine bell behind the second stage, a short kerosene tank behind a liquid-oxygen tank, and the payload fairing with the payload. Kerosene has horizontal hatching and liquid oxygen diagonal hatching.
:width: 90%

Schematic of a two-stage launch vehicle, the Falcon 9, cut where the stages separate. The first stage keeps its interstage, with the grid fins and the landing legs it needs to return; the second stage leaves with its vacuum engine and the payload under the fairing. Each stage has its oxygen tank ahead of its kerosene tank. Proportions and tank lengths after SpaceX (2025, Section 2 and Figure 2-1); engines, legs, and grid fins estimated.
:::

:::{warning} The biggest tank is not always the fuel tank
On the Ariane 5 core stage the larger tank holds the fuel, liquid hydrogen, even though the first version of the stage carried 5.1 times more oxygen than hydrogen by mass. Hydrogen is so light that 26 t of it fill 390 m³. Name a tank by what it holds, not by its size.
:::

(p13-mission-profile)=
## Mission profiles

A design starts from what the vehicle must do, stated in the [mission statement](#p11-mission-statement). For an aircraft, what it must do in flight is drawn as a mission profile.

:::{prf:definition} Mission profile
:label: def-p13-mission-profile

A **mission profile** is a sketch of a mission as altitude against distance (or time), cut into segments, such as takeoff, climb, cruise, descent, loiter, and landing, drawn in the order they are flown. The end of each segment is numbered, starting with 0 at the start of the takeoff.
:::

The weight of the aircraft at the end of segment $i$ is written $W_i$, so $W_0$ is the takeoff weight. The sizing method of [aircraft sizing](#p16-weight-fractions) estimates the weight lost in each segment from these numbers. A **{term}`loiter`** is flying in circles at a speed that uses the least fuel per hour, while waiting for permission to land or over an area being watched; airline pilots call it a hold. A sudden fall in weight, when cargo is unloaded or weapons are released, is marked on the profile because it changes the fuel the rest of the mission needs.

:::{tip} Method: sketching a mission profile
1. Read the mission and list what the vehicle does, in order, from the start of the takeoff to the end of the landing.
2. Draw a ground line and a path above it: takeoff and landing as short level segments on the ground line, climbs and descents slanted, cruise and loiter level.
3. Name each segment beside it and number the end of each segment: 0 at the start of the takeoff, then 1, 2, 3, and so on.
4. Mark any point where the weight drops at once (payload unloaded, weapons released) with a short downward arrow on the path.
5. Add reserves the rules or the customer require, such as a loiter before landing.
:::

{numref}`fig-p13-mission-profiles` sketches three missions. An airliner climbs, cruises for most of the trip, descends, and lands. A business jet that drops passengers at one airport and flies on to another without refueling repeats the pattern, with a weight drop at the stop and, here, a loiter before the second landing. A skydiving aircraft has no cruise at all: it climbs to the jump altitude, flies a short level jump run while the skydivers leave, which drops its weight at once, then descends and lands. The profile on [aircraft sizing](#p16-weight-fractions) looks different in one respect: that method counts each descent inside another segment, so it draws the descents thinner and without a number.

:::{figure} figures/p13-mission-profiles.svg
:label: fig-p13-mission-profiles
:alt: Three mission profiles, altitude against distance, not to scale, with numbered segment ends; takeoff and landing are level segments on the ground line. Airliner, Airbus A320 class: takeoff 0 to 1, climb 1 to 2, cruise 2 to 3, descent 3 to 4, landing 4 to 5. Business jet, Phenom 100 class, two legs without refueling: takeoff, climb, cruise, descent, and landing, 0 to 5, where a downward arrow marks the weight drop as passengers get off; then takeoff, climb, cruise, descent, loiter (also called a hold) from 9 to 10, descent, and landing, 5 to 12. Skydiving aircraft, Twin Otter class: takeoff, climb, a jump run from 2 to 3 ending in a downward arrow as the skydivers jump, descent, and landing, 0 to 5.
:width: 85%

Schematic, not to scale, of three mission profiles. Each is the mission cut into segments and drawn in order, with the end of each segment numbered; a loiter, a second leg, or a drop in weight shows as its own segment or mark. In the form of the sizing profiles of Raymer (2006, Figure 3.2).
:::

:::{warning} Common slips with mission profiles
- Numbering segments instead of their ends. The numbers mark the points where one segment ends and the next begins, starting with 0 at the start of the takeoff; a profile of six segments has seven numbers, 0 to 6.
- Leaving out a segment the mission states. A loiter, a second leg, or a weapons release changes the fuel; each needs its own segment or mark.
- Drawing to scale. A cruise is far longer than the cruise altitude is high, so to scale every climb and descent would vanish; the profile is a schematic.
:::

## Summary

:::{important} Summary
- The airframe is a few large parts with one job each. Roll, pitch, and yaw turn it about the body axes through the center of gravity, commanded by the ailerons, the elevator, and the rudder.
- A straight-tapered wing is fixed by $b$, $S$, and $\lambda$ (and its sweep): $\textit{AR} = b^2/S$, $c_r = 2S/[b(1 + \lambda)]$, $\bar{c} = \tfrac{2}{3}c_r(1 + \lambda + \lambda^2)/(1 + \lambda)$. A NACA MPXX airfoil has M% camber at P tenths of the chord and XX% thickness.
- A launch vehicle is a stack of stages dropped one after the other. A mission profile is the mission cut into numbered segments.
:::

:::{table} The equations and terms of this page.
:label: tbl-p13-summary
:align: center

| Quantity | Equation or meaning |
| --- | --- |
| Wing area (straight-tapered) | $S = b\,(c_r + c_t)/2 = b\,c_r\,(1 + \lambda)/2$ |
| Taper ratio | $\lambda = c_t/c_r$ |
| Aspect ratio | $\textit{AR} = b^2/S$ |
| Root chord | $c_r = 2S/[b\,(1 + \lambda)]$ |
| Mean aerodynamic chord | $\bar{c} = \tfrac{2}{3}\,c_r\,(1 + \lambda + \lambda^2)/(1 + \lambda)$ |
| Station of the mean aerodynamic chord | $y_{\bar{c}} = (b/6)\,(1 + 2\lambda)/(1 + \lambda)$ |
| Wing loading | $W_0/S$, in lb/ft² |
| NACA MPXX | M% camber, at P tenths of the chord; XX% thickness, at 30% of the chord |
:::

:::{exercise} For discussion
:label: ex-p13-discussion

1. Why do airliners put the engines under the wing, while many business jets put them on the rear fuselage? Name one advantage of each.
2. A tail-dragger and a tricycle aircraft land with a crosswind. Which one is more likely to swerve after touchdown, and why?
3. Two wings have the same area and the same span, one rectangular and one tapered. Which of $\textit{AR}$, $\lambda$, and $\bar{c}$ differ between them?
4. Why does the payload fairing leave the vehicle long before the payload reaches orbit, instead of staying on to the end?
5. An airliner and a business jet fly the same distance on one leg. Which segments of their mission profiles are the same, and which segment would you expect to take the largest share of the fuel?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-1-3.html
:label: quiz-1-3
:enumerated: false
:width: 100%

Quiz for Standard 1.3: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Abbott, I. H., and von Doenhoff, A. E., *Theory of Wing Sections*, Dover, 1959. Chapter 6 (the NACA four-digit sections).
- Arianespace, *Ariane 5 User's Manual*, Issue 5 Revision 2, 2016. Sections 1.5.1 (the vehicle and its stages), 2.3 (Figure 2.3.a, typical sequence of events), and 3.3.3.2 (fairing jettison); Annex 4.
- Boeing Commercial Airplanes (Boeing), *[Next-Generation 737 Airplane Characteristics for Airport Planning](https://www.boeing.com/content/dam/boeing/v2/airports/acaps/737NG_REV_C.pdf)*, D6-58325-7 Rev C, 2025.
- European Space Agency (ESA), "[Ariane 5 boosters (EAP)](https://www.esa.int/Enabling_Support/Space_Transportation/Launch_vehicles/Ariane_5_boosters_EAP)," n.d.a.
- European Space Agency (ESA), "[Ariane 5 cryogenic main stage (EPC)](https://www.esa.int/articles/about-us/directorates/space-transportation/ariane/ariane-5-cryogenic-main-stage-epc)," n.d.b.
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023a.
- Federal Aviation Administration (FAA), *[Aviation Maintenance Technician Handbook, Airframe](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-31B_Aviation_Maintenance_Technician_Handbook.pdf)*, FAA-H-8083-31B, 2023b.
- Jacobs, E. N., Ward, K. E., and Pinkerton, R. M., *The Characteristics of 78 Related Airfoil Sections from Tests in the Variable-Density Wind Tunnel*, NACA Report 460, 1933.
- Jenkinson, L. R., Simpkin, P., and Rhodes, D., *Civil Jet Aircraft Design*, Arnold and Butterworth-Heinemann, 1999. Companion web site, Data A, Aircraft Data File, Boeing aircraft: [Table 2](https://booksite.elsevier.com/9780340741528/appendices/data-a/table-2/table.htm) and [Table 3](https://booksite.elsevier.com/9780340741528/appendices/data-a/table-3/table.htm).
- Lednicer, D., "[The Incomplete Guide to Airfoil Usage](https://m-selig.ae.illinois.edu/ads/aircraft.html)," UIUC Applied Aerodynamics Group, last updated 2026.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 4th ed., AIAA, 2006.
- SpaceX, *[Falcon User's Guide](https://www.spacex.com/assets/media/falcon-users-guide-2025-05-09.pdf)*, 2025. Section 2 and Figure 2-1.
