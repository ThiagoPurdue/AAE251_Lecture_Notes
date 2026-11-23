---
title: "2.4 Patched Conics"
short_title: 2.4 Patched Conics
---

:::{include} ../_parts/standards/2.4.md
:::

A trip to another planet passes through three gravity fields: the departure planet's, the Sun's, and the target planet's. The method of {term}`patched conics` treats one field at a time, so each piece of the trip is a conic section you already know how to handle. We build the method in three steps (the transfer around the Sun, the departure burn, and the capture burn) and work a complete example for an orbiter sent to Mercury. Then we apply the same steps to a trip to the Moon and see how the planets' periods set the timing of a launch.

:::{note} What to take from this page
- Inside a planet's {term}`sphere of influence` only the planet's gravity counts; outside it only the Sun's. The trip becomes a departure hyperbola, a transfer ellipse around the Sun, and an arrival hyperbola.
- The {term}`hyperbolic excess speed` $v_\infty$ links the pieces: for a Hohmann transfer, it is the difference between the spacecraft's speed and the planet's speed around the Sun.
- Each burn is the speed on the hyperbola at the burn radius, $\sqrt{v_\infty^2 + 2\mu/r_p}$, minus the speed of the circular orbit there, with the $\mu$ of the planet where the burn happens.
- The target must be at the meeting point when the spacecraft arrives, so launch opportunities come back once every {term}`synodic period`.
:::

## The idea: one body at a time

A spacecraft between Earth and Mercury feels the Sun, Earth, Mercury, and every other planet at once. The two-body problem of [orbit properties](orbit-properties.md) has a closed-form answer only for one central body. So we split the trip into pieces and keep, in each piece, only the body that dominates.

We make the split at the sphere of influence of each planet. Close to a planet, the planet's pull bends the path far more than the Sun's pull changes it, and the motion is a conic around the planet. Far from the planet, the Sun dominates, and the motion is a conic around the Sun. Laplace's estimate of the boundary is

:::{math}
:label: eq-p24-soi
r_{\text{SOI}} = r\left(\frac{\mu_{\text{planet}}}{\mu_{\text{Sun}}}\right)^{2/5}
:::

where $r$ is the planet's distance from the Sun (Curtis 2014, Chapter 8). For Earth, $r_{\text{SOI}}$ is about 925,000 km, or 145 Earth radii. That is large next to Earth, but only 0.62% of Earth's distance from the Sun. For Mercury it is about 112,000 km.

:::{prf:definition} Patched conics
:label: def-p24-patched-conics

**Patched conics** is an approximate method for interplanetary trajectories. Inside the sphere of influence of a planet, the spacecraft moves on a conic around that planet; outside it, on a conic around the Sun. The conics are joined ("patched") at the edge of the sphere of influence, where the spacecraft's velocity relative to the planet sets the hyperbolic excess speed $v_\infty$.
:::

A trip from one planet to another has three pieces ({numref}`fig-p24-three-conics`):

1. **Departure.** A hyperbola around the departure planet, from the burn in the {term}`parking orbit` out to the edge of the sphere of influence.
2. **Transfer.** An ellipse around the Sun from the departure planet's orbit to the target planet's orbit. On this page it is a Hohmann transfer.
3. **Arrival.** A hyperbola around the target planet, ending in a {term}`capture burn` into an orbit around it.

:::{figure} figures/p24-three-conics.svg
:label: fig-p24-three-conics
:alt: Three pieces of a trip from Earth to Mercury, numbered 1 to 3. In the middle, piece 2: the Sun with Earth's orbit, solid, Mercury's orbit, dash-dot, and a dashed half ellipse, the transfer orbit, running from Earth on the left, through the bottom, to Mercury on the right; small dashed circles around Earth and Mercury are magnified at the sides, each joined to its magnified view by two thin lines that touch both circles. At the left, piece 1: the departure hyperbola leaves Earth's parking orbit after a burn and crosses Earth's sphere of influence moving upward at v infinity. At the right, piece 3: the arrival hyperbola enters Mercury's sphere of influence moving upward at a larger v infinity and ends with a burn, longer than the departure burn, into a circular orbit.
:width: 95%

Schematic of a trip by patched conics, not to scale. The radii of the two orbits in the middle are to scale; the planets and the spheres of influence (dashed) are enlarged, and the two side views are magnified. Motion is counterclockwise; the two $v_\infty$ arrows are drawn to the same scale, and so are the two burn arrows. Each piece is a conic around one body: 1, the departure hyperbola around Earth; 2, the transfer orbit around the Sun; 3, the arrival hyperbola around Mercury.
:::

The method rests on these assumptions:

- The planets move on circular orbits in one plane.
- Burns are impulsive: the velocity changes at once and the position does not.
- The sphere of influence is small against the distance between the planets. For the leg around the Sun, the spacecraft starts at the departure planet's position and ends at the target planet's position. The days spent inside each sphere of influence are short next to the months of the transfer, so we ignore them.

With these assumptions the method gives a first estimate of the burns and the trip time, good enough to size a propulsion system and to compare destinations (Bate, Mueller, and White 1971, Chapter 8).

## Step 1: the transfer around the Sun

In the first step we ignore both planets and find the transfer orbit around the Sun. With circular, coplanar planet orbits, the cheapest two-burn transfer is [the Hohmann transfer](#p22-hohmann): half an ellipse that touches the departure planet's orbit (radius $r_1$) and the target's orbit (radius $r_2$), with semi-major axis $a_t = (r_1 + r_2)/2$.

Each planet moves at the circular speed of its orbit around the Sun. The spacecraft's speed at each end of the transfer orbit follows from [the vis-viva equation](#p21-vis-viva). Both use the Sun's $\mu$:

:::{math}
:label: eq-p24-planet-speeds
v_{\text{planet}} = \sqrt{\frac{\mu_{\text{Sun}}}{r}}, \qquad v_t = \sqrt{\mu_{\text{Sun}}\left(\frac{2}{r} - \frac{1}{a_t}\right)}
:::

Comparing the two speeds tells us which way the spacecraft must leave:

- **Going outward** (to Jupiter, say), the departure planet sits at the periapsis of the transfer orbit. The transfer speed there is higher than the planet's, so the spacecraft must leave faster than the planet, along the planet's direction of motion.
- **Going inward** (to Venus or Mercury), the departure planet sits at the apoapsis. The transfer speed there is lower than the planet's, so the spacecraft must leave slower than the planet, against the planet's direction of motion.

{numref}`fig-p24-heliocentric-transfer` shows the inward case to scale. The time of flight is half the period of the transfer orbit, $t_f = \pi\sqrt{a_t^3/\mu_{\text{Sun}}}$.

:::{figure} figures/p24-heliocentric-transfer.svg
:label: fig-p24-heliocentric-transfer
:alt: Top view of the Sun with the circular orbits of Earth and Mercury drawn to scale, and the Hohmann transfer as a dashed half ellipse from Earth at departure on the left, around the bottom, to the meeting point on Mercury's orbit at the right. Mercury at departure is marked 108 degrees ahead of Earth, measured counterclockwise at the Sun. All motion is counterclockwise.
:width: 75%

Computed with the constants of this chapter: the Hohmann transfer from Earth to Mercury, orbits to scale, planets not to scale. Motion is counterclockwise. At departure Mercury must already be 108° ahead of Earth so that it reaches the meeting point together with the spacecraft (see the section on the phase angle).
:::

(p24-vinf)=
## Hyperbolic excess speed

The transfer speed $v_t$ is measured around the Sun. The spacecraft starts with the planet's speed, so the speed it must have relative to the planet, once it is far from the planet, is the difference:

:::{math}
:label: eq-p24-vinf
v_\infty = \left|\,v_t - v_{\text{planet}}\,\right|
:::

The speeds subtract directly because, on a Hohmann transfer, the two velocities are parallel at both ends. For any other transfer, $v_\infty$ is the size of the vector difference.

:::{prf:definition} Hyperbolic excess speed
:label: def-p24-vinf

The **hyperbolic excess speed** $v_\infty$ is the speed of a spacecraft relative to a planet when it is far from the planet. Leaving, it is what is left after the spacecraft has climbed out of the planet's gravity well; arriving, it is the speed at which the spacecraft approaches from far away. The gravity well is the dip in potential energy, $-\mu/r$, around the planet.
:::

A spacecraft that leaves a planet at exactly [escape speed](#p21-circular-and-escape) follows a parabola and arrives far away with zero speed relative to the planet. To go anywhere, it needs more than escape speed, and that puts it on a hyperbola. The hyperbola has the same parts as an ellipse (a periapsis, a semi-major axis $a$, an eccentricity $e$), but $e > 1$, $a$ is negative, and there is no apoapsis. The path straightens out along an asymptote, the direction in which the spacecraft leaves.

We find the speed anywhere on the hyperbola from energy. The {term}`specific orbital energy` is constant along the path:

:::{math}
:label: eq-p24-energy
\varepsilon = \frac{v^2}{2} - \frac{\mu}{r}
:::

Far from the planet, $r$ is large, $\mu/r$ goes to zero, and $v$ goes to $v_\infty$. So $\varepsilon = v_\infty^2/2$, which is positive, as it must be for a hyperbola. Setting the two expressions for $\varepsilon$ equal at any radius $r$ gives

:::{math}
:label: eq-p24-hyperbola-speed
v^2 = v_\infty^2 + \frac{2\mu}{r}
:::

Since $2\mu/r$ is the square of the escape speed at $r$, the speed on the hyperbola is $v = \sqrt{v_\infty^2 + v_{\text{esc}}^2}$. Comparing $\varepsilon = v_\infty^2/2$ with $\varepsilon = -\mu/(2a)$ also gives the semi-major axis, $a = -\mu/v_\infty^2$.

{numref}`fig-p24-speed-vs-distance` follows the speed along a departure hyperbola. The spacecraft leaves the parking orbit at 13.35 km/s and slows as it climbs. At the edge of Earth's sphere of influence its speed is 7.591 km/s, within 1% of $v_\infty$ = 7.534 km/s. This is why we can treat the edge of the sphere of influence as "far away" and start the leg around the Sun with $v_\infty$.

:::{figure} figures/p24-speed-vs-distance.svg
:label: fig-p24-speed-vs-distance
:alt: Line plot of speed in kilometers per second against distance from Earth's center, from 6,563 to 1,000,000 kilometers on a log scale. The speed on the departure hyperbola falls from 13.35 kilometers per second at the parking orbit and levels off at the horizontal line v infinity equals 7.534 kilometers per second. The escape speed curve falls from 11.021 kilometers per second to below 1 kilometer per second. A vertical line marks the edge of Earth's sphere of influence near 925,000 kilometers, where the hyperbola speed is almost equal to v infinity.
:width: 80%

Computed from {eq}`eq-p24-hyperbola-speed`: speed on the departure hyperbola of the Mercury example ($v_\infty$ = 7.534 km/s, burn at 185 km altitude) and the escape speed, against distance from Earth's center. The speed falls toward $v_\infty$ and is within 1% of it at the edge of the sphere of influence.
:::

:::{warning} Two speeds, two frames
$v_t$ and $v_{\text{planet}}$ are speeds around the Sun and use $\mu_{\text{Sun}}$. $v_\infty$ and every speed on the hyperbola are speeds relative to the planet and use the planet's $\mu$. If you mix the two, for example by computing the hyperbola speed with $\mu_{\text{Sun}}$, your numbers are wrong by orders of magnitude.
:::

## Step 2: the departure burn

The spacecraft waits in a circular parking orbit of radius $r_p$ around the departure planet. One burn along the direction of motion raises its speed from the circular speed to the speed of the hyperbola at that radius. The burn point becomes the periapsis of the hyperbola ({numref}`fig-p24-departure-hyperbola`). With {eq}`eq-p24-hyperbola-speed` at $r = r_p$, the velocity change $\Delta V$ (delta-V) of the {term}`departure burn` is

:::{math}
:label: eq-p24-dv-departure
\Delta V_{\text{dep}} = \sqrt{v_\infty^2 + \frac{2\mu}{r_p}} - \sqrt{\frac{\mu}{r_p}}
:::

with $\mu$ of the departure planet and $r_p = R + h$, the radius of the parking orbit (not its altitude).

:::{figure} figures/p24-departure-hyperbola.svg
:label: fig-p24-departure-hyperbola
:alt: Earth drawn to scale with its 185 kilometer circular parking orbit hugging the surface. A burn on the side facing the Sun pushes the spacecraft along its direction of motion onto the departure hyperbola, which curves away from Earth and straightens out along a dashed vertical asymptote to the right of Earth. An arrow at the far end shows v infinity, 7.534 kilometers per second, pointing up. Direction arrows show the Sun to the right and Earth's motion around the Sun pointing down, so the spacecraft leaves against Earth's motion.
:width: 45%

Computed for the Mercury example, to scale near Earth: the departure hyperbola ($e$ = 1.935) from the 185 km parking orbit, with the burn at its periapsis. The $v_\infty$ arrow is drawn to scale with the distances (1 km/s to 0.3 Earth radii); the gray arrows show directions only. Going inward to Mercury, the spacecraft must leave against Earth's motion around the Sun, so the burn is made on the side of Earth facing the Sun.
:::

Where we make the burn depends on the direction $v_\infty$ must have. For the inward trip $v_\infty$ must point against Earth's motion. The burn point lies 121.1° back from that direction, counted against the spacecraft's motion around Earth, which puts it on the side of Earth facing the Sun ({numref}`fig-p24-departure-hyperbola`). Going outward, we make the burn on the night side.

### Why burn deep in the gravity well

Burning in the low parking orbit is much cheaper than escaping first and then burning far from Earth. {numref}`fig-p24-vinf-vs-dv` compares the two plans from a 185 km orbit, where the circular speed is 7.793 km/s and the escape speed 11.021 km/s.

- **Escape first, then burn.** Reaching escape speed costs 3.228 km/s. The spacecraft then arrives far from Earth with no speed left, and a second burn must supply all of $v_\infty$. For $v_\infty$ = 7.534 km/s the total is 10.76 km/s.
- **One burn in the parking orbit.** {eq}`eq-p24-dv-departure` gives 5.557 km/s for the same $v_\infty$.

The reason is energy. A burn $\Delta V$ made at speed $v$ adds about $v\,\Delta V$ to the specific orbital energy, so the same burn adds more energy where the spacecraft is fast, deep in the gravity well. The extra energy appears far away as $v_\infty$. On the curve of {numref}`fig-p24-vinf-vs-dv`, each extra km/s of $v_\infty$ costs less than 1 km/s of $\Delta V$.

:::{figure} figures/p24-vinf-vs-dv.svg
:label: fig-p24-vinf-vs-dv
:alt: Line plot of departure delta-V against hyperbolic excess speed from 0 to 12 kilometers per second, for a 185 kilometer parking orbit around Earth; both plans start at 3.228 kilometers per second, the cost of just escaping. The dashed straight line, escaping first and then burning far from Earth, rises with slope one. The solid curve, one burn in the parking orbit, rises slowly at first and stays well below the line. The Mercury example is marked on the curve at 7.534 and 5.557 kilometers per second.
:width: 80%

Computed with $\mu$ and $R$ of Earth: the departure $\Delta V$ from a 185 km circular orbit against the $v_\infty$ it buys. For any $v_\infty$ above zero the single low burn costs less. Solid curve: one burn in the parking orbit, {eq}`eq-p24-dv-departure`. Dashed line: escape first (3.228 km/s, the escape speed minus the circular speed), then burn far from Earth, where every km/s of $\Delta V$ adds one km/s of $v_\infty$, so $\Delta V = 3.228\ \text{km/s} + v_\infty$.
:::

## Step 3: arrival and capture

At the target, the same reasoning runs backward. The spacecraft arrives at the target's orbit with the transfer speed $v_t$, and the target moves at $v_{\text{planet}}$. So the spacecraft enters the target's sphere of influence with $v_\infty = |v_t - v_{\text{planet}}|$ relative to the target. Inside the sphere of influence it falls toward the target on a hyperbola and speeds up. At periapsis, at radius $r_p$, its speed is $\sqrt{v_\infty^2 + 2\mu/r_p}$, now with the target's $\mu$.

A hyperbola does not close. Without a burn, the spacecraft swings past the target and leaves again at $v_\infty$, as on the flyby path of {numref}`fig-p24-arrival-capture`. To stay, it must slow down at periapsis, with a burn against its motion, to the speed of the orbit it wants. For a circular capture orbit of radius $r_p$,

:::{math}
:label: eq-p24-dv-capture
\Delta V_{\text{cap}} = \sqrt{v_\infty^2 + \frac{2\mu}{r_p}} - \sqrt{\frac{\mu}{r_p}}
:::

which has the same form as the departure burn, with the target's $\mu$ and the target's $v_\infty$. If the capture orbit is an ellipse with periapsis $r_p$ and semi-major axis $a$, subtract its periapsis speed $\sqrt{\mu(2/r_p - 1/a)}$ instead of the circular speed. That speed is higher, so capture into a long ellipse costs less than capture into a low circle.

:::{warning} The burn is not $v_\infty$
The departure and capture burns are differences of speeds at the burn radius. If you take $\Delta V = v_\infty$, or subtract $v_\infty$ from the periapsis speed, you skip the gravity well and get the wrong answer. In the Mercury example, $v_\infty$ at departure is 7.534 km/s, but the burn is 5.557 km/s.
:::

:::{figure} figures/p24-arrival-capture.svg
:label: fig-p24-arrival-capture
:alt: Mercury drawn to scale with a 400 kilometer circular capture orbit and the arrival hyperbola, which comes up from below, nearly straight, entering at v infinity equal to 9.613 kilometers per second. At its periapsis, on the side of Mercury away from the Sun, a burn arrow drawn just beside the path points backward against the motion. A dotted path with a motion arrowhead continues upward past Mercury, bent only slightly, labeled as the flyby without the burn. Direction arrows show the Sun to the left and Mercury's motion around the Sun pointing up.
:width: 55%

Computed for the Mercury example, to scale near Mercury: the capture burn at the periapsis of the arrival hyperbola, against the motion, into a 400 km circular orbit. The $v_\infty$ arrow is to scale with the distances (1 km/s to 0.22 Mercury radii); the gray arrows show directions only. The arrival hyperbola is fast ($e$ = 12.9) and bends by only 8.9°, so without the burn the spacecraft flies past and leaves.
:::

:::{tip} Method: patched conics
1. Write $r_1$, $r_2$ of the two planets around the Sun and $a_t = (r_1 + r_2)/2$.
2. Find each planet's speed $\sqrt{\mu_{\text{Sun}}/r}$ and the transfer speed at each end from vis-viva with $\mu_{\text{Sun}}$.
3. Take the differences: $v_\infty$ at departure and at arrival.
4. Convert altitudes to radii: $r_p = R + h$ for the parking and capture orbits.
5. At each planet, with that planet's $\mu$: $\Delta V = \sqrt{v_\infty^2 + 2\mu/r_p} - \sqrt{\mu/r_p}$.
6. Trip time: half the transfer period, converted from seconds to days.
:::

## Worked example: a Mercury orbiter

A spacecraft flies a direct Hohmann transfer from Earth to Mercury, with no flybys. It leaves a 185 km circular parking orbit around Earth and is captured into a 400 km circular orbit around Mercury. Find $v_\infty$ at each end, both burns, and the trip time. Earth and Mercury move on circular, coplanar orbits.

Use the values of [the table of constants](#tbl-p21-constants): $\mu_{\text{Sun}} = 1.327 \times {10}^{11}$ km³/s². Earth: $\mu = 3.986 \times {10}^{5}$ km³/s², $R$ = 6,378 km, distance from the Sun $r_1 = 1.496 \times {10}^{8}$ km. Mercury: $\mu = 2.203 \times {10}^{4}$ km³/s², $R$ = 2,440 km, distance from the Sun $r_2 = 5.790 \times {10}^{7}$ km.

1. **Transfer orbit.** $a_t = (1.496 \times {10}^{8} + 5.790 \times {10}^{7})/2 = 1.0375 \times {10}^{8}$ km, with eccentricity $(r_1 - r_2)/(r_1 + r_2)$ = 0.4419. Earth is at the aphelion and Mercury at the perihelion.
2. **Excess speed at Earth.** Earth's speed is $\sqrt{\mu_{\text{Sun}}/r_1}$ = 29.783 km/s. The transfer speed at Earth is

   $$
   \begin{aligned}
   v_t &= \sqrt{\mu_{\text{Sun}}\,(2/r_1 - 1/a_t)}\\
       &= 22.249\ \text{km/s}
   \end{aligned}
   $$

   So $v_\infty = 29.783 - 22.249 = 7.534$ km/s, against Earth's motion.
3. **Departure burn.** $r_p = 6{,}378 + 185 = 6{,}563$ km. The hyperbola speed is $\sqrt{v_\infty^2 + 2\mu/r_p} = \sqrt{56.76 + 121.5}$ = 13.35 km/s, and the circular speed is $\sqrt{\mu/r_p}$ = 7.793 km/s. $\Delta V_{\text{dep}} = 13.35 - 7.793 = 5.557$ km/s.
4. **Excess speed at Mercury.** Mercury's speed is $\sqrt{\mu_{\text{Sun}}/r_2}$ = 47.874 km/s. The transfer speed at Mercury is

   $$
   \begin{aligned}
   v_t &= \sqrt{\mu_{\text{Sun}}\,(2/r_2 - 1/a_t)}\\
       &= 57.487\ \text{km/s}
   \end{aligned}
   $$

   So $v_\infty = 57.487 - 47.874 = 9.613$ km/s: the spacecraft overtakes Mercury from behind.
5. **Capture burn.** $r_p = 2{,}440 + 400 = 2{,}840$ km. The hyperbola speed is $\sqrt{92.413 + 15.514}$ = 10.389 km/s, and the circular speed is 2.785 km/s. $\Delta V_{\text{cap}} = 10.389 - 2.785 = 7.604$ km/s, against the motion.
6. **Trip time.** $t_f = \pi\sqrt{a_t^3/\mu_{\text{Sun}}}$ = 105.5 days.

:::{table} Results of the Mercury example. Speeds around the Sun use $\mu_{\text{Sun}}$; speeds near a planet use that planet's $\mu$.
:label: tbl-p24-mercury

| Step | Quantity | Value |
| --- | --- | ---: |
| Around the Sun | Earth's speed | 29.783 km/s |
| | Transfer speed at Earth (aphelion) | 22.249 km/s |
| | Transfer speed at Mercury (perihelion) | 57.487 km/s |
| | Mercury's speed | 47.874 km/s |
| Departure | $v_\infty$ at Earth | 7.534 km/s |
| | Departure burn from 185 km | 5.557 km/s |
| Arrival | $v_\infty$ at Mercury | 9.613 km/s |
| | Capture burn into 400 km circular orbit | 7.604 km/s |
| Total | Both burns | 13.16 km/s |
| Trip | Time of flight | 105.5 days |

:::

**Check.** Of the 5.557 km/s departure burn, 3.228 km/s is the cost of escaping from the parking orbit. The remaining 2.329 km/s buys 7.534 km/s of $v_\infty$, the advantage of the low burn shown in {numref}`fig-p24-vinf-vs-dv`. At Mercury the capture burn costs most of $v_\infty$, because Mercury's well is shallow. The escape speed at a radius of 2,840 km is only 3.939 km/s, so burning low at Mercury saves little.

The capture burn is the expensive part. The spacecraft falls toward the Sun and gains speed all the way. It arrives 9.613 km/s faster than Mercury, and Mercury's weak gravity cannot help remove that speed. A propulsion system able to deliver 7.604 km/s after the cruise would be far heavier than the orbiter it carries. Real Mercury orbiters avoid this: MESSENGER flew past Earth once, Venus twice, and Mercury three times, each flyby trading speed with a planet, before it entered orbit around Mercury (Solomon et al. 2007). This chapter does not cover such flybys (gravity assists).

## Going to the Moon

A trip to the Moon uses the same three steps with Earth as the central body in place of the Sun. The spacecraft never leaves Earth's sphere of influence, so the departure needs no hyperbola.

1. **Transfer around Earth.** A Hohmann transfer from the parking orbit (radius $r_1$) out to the radius of the Moon's orbit, $r_{\text{Moon}}$, with $a_t = (r_1 + r_{\text{Moon}})/2$ and Earth's $\mu$. The departure burn is the first Hohmann burn, $\Delta V_{\text{dep}} = \sqrt{\mu_{\text{Earth}}(2/r_1 - 1/a_t)} - \sqrt{\mu_{\text{Earth}}/r_1}$.
2. **Excess speed at the Moon.** At apogee the spacecraft moves at $v_{t} = \sqrt{\mu_{\text{Earth}}(2/r_{\text{Moon}} - 1/a_t)}$, slower than the Moon's own speed $\sqrt{\mu_{\text{Earth}}/r_{\text{Moon}}}$. The Moon overtakes the spacecraft, and the spacecraft enters the Moon's sphere of influence with $v_\infty = \sqrt{\mu_{\text{Earth}}/r_{\text{Moon}}} - v_t$ relative to the Moon.
3. **Capture.** With the Moon's $\mu$ and the radius $r_p$ of the lunar orbit, $\Delta V_{\text{cap}} = \sqrt{v_\infty^2 + 2\mu_{\text{Moon}}/r_p} - \sqrt{\mu_{\text{Moon}}/r_p}$, a burn against the motion.

The estimate is rougher for the Moon than for a planet. The Moon's sphere of influence is not small next to its distance from Earth. The spacecraft spends a large part of the trip where Earth and the Moon pull with comparable strength, and the Sun's pull also changes the path. Engineers design real lunar trajectories by integrating the motion under all of these bodies, starting from a patched-conic estimate.

## When to leave: phase angle and synodic period

The transfer orbit works only if the target is at the meeting point when the spacecraft gets there. The target moves during the trip, so at departure it must already be ahead of (or behind) the departure planet by the right angle, the {term}`phase angle`.

The meeting point is 180° from the departure point around the Sun. During the trip time $t_f$ the target moves through the angle $n_2 t_f$, where $n_2 = 360°/T_2$ is its angular rate and $T_2$ its orbital period. At departure it must therefore lead the departure planet by

:::{math}
:label: eq-p24-phase
\text{phase angle} = {180}^\circ - n_2\, t_f
:::

adding or subtracting 360° as needed to bring the result between 0° and 360°. For Mercury, $n_2$ = 360°/87.97 days = 4.092° per day, so in 105.5 days Mercury moves 432°, more than one full turn. The formula gives ${180}^\circ - {432}^\circ = -{252}^\circ$, which is the same direction as 108° ahead of Earth ({numref}`fig-p24-heliocentric-transfer`).

The required alignment does not last. The two planets move at different angular rates, so the angle between them changes at the rate $360°/T_1 - 360°/T_2$ and returns to the same value after one {term}`synodic period`:

:::{math}
:label: eq-p24-synodic
S = \frac{1}{\left|\,1/T_1 - 1/T_2\,\right|}
:::

A launch opportunity comes once every synodic period ({numref}`fig-p24-synodic`). A mission that misses one opportunity waits one synodic period for the next.

:::{figure} figures/p24-synodic.svg
:label: fig-p24-synodic
:alt: Line plot of the phase angle of Mercury ahead of Earth, from 0 to 360 degrees, against time from 0 to 400 days. The angle rises steadily, wraps from 360 back to 0 degrees, and rises again, forming a sawtooth. A dashed horizontal line marks the required phase angle of 108 degrees. Dots mark where the sawtooth crosses it, at 0, 116, 232, and 348 days; a dimension between two dots reads S equals 116 days.
:width: 80%

Computed from the orbital periods of [the table of constants](#tbl-p21-constants): phase angle of Mercury ahead of Earth against time, starting at a launch opportunity. The required 108° comes back once every synodic period, $S$ = 116 days.
:::

{numref}`tbl-p24-synodic` gives the synodic periods with Earth for Mercury, Venus, Jupiter, and Saturn. Planets far from the Sun move slowly, so for Jupiter and Saturn the synodic period is close to one year. In one year Earth comes back to the same place, while the outer planet has moved only a little. Of these four, Venus has the longest synodic period, because its period is the closest to Earth's.

:::{table} Synodic periods with Earth, from {eq}`eq-p24-synodic` with $T_1$ = 365.26 days and the orbital periods of the table of constants on [orbit properties](orbit-properties.md).
:label: tbl-p24-synodic

| Target | Orbital period, days | Synodic period, days | Synodic period, years |
| --- | ---: | ---: | ---: |
| Mercury | 87.97 | 116 | 0.317 |
| Venus | 224.7 | 584 | 1.60 |
| Jupiter | 4,332.6 | 399 | 1.09 |
| Saturn | 10,759 | 378 | 1.04 |

:::

:::{warning} Units in the time of flight
$\pi\sqrt{a_t^3/\mu}$ with $a_t$ in km and $\mu$ in km³/s² gives seconds. Divide by 86,400 to get days before comparing with orbital periods in days. If you use $\mu$ in m³/s² with $a_t$ in km, the time is wrong by a factor of more than 30,000.
:::

## Limits of the method

Patched conics gives an estimate for early design. To plan the trajectory a spacecraft actually flies, engineers add what the method leaves out:

- The real orbits of the planets, which are eccentric and tilted to each other. Mercury's orbit is the most eccentric of the eight planets, so the numbers of the worked example change with the date of the trip.
- Transfers other than the Hohmann transfer: faster trips at a higher cost, chosen from charts of launch date against arrival date.
- The pull of the Sun inside each sphere of influence and of the planets outside it, through numerical integration of the motion.
- Small correction burns during the cruise, and gravity assists from other planets.

## Summary

:::{important} Summary
- Patched conics splits a trip into conics around one body at a time, joined at the edge of each sphere of influence: departure hyperbola, Hohmann ellipse around the Sun, arrival hyperbola.
- For a Hohmann transfer, the hyperbolic excess speed is the difference between the transfer speed and the planet's speed around the Sun. On the hyperbola, $v^2 = v_\infty^2 + 2\mu/r$.
- Each burn is the hyperbola speed at the burn radius minus the speed of the orbit there, with that planet's $\mu$. A burn low in a gravity well buys more $v_\infty$ per km/s than a burn far from the planet; a capture at a small planet costs most of $v_\infty$.
- The target must lead by the phase angle at departure; the same alignment returns once every synodic period.
:::

:::{table} The equations of this page.
:label: tbl-p24-equations

| Quantity | Equation |
| --- | --- |
| Sphere of influence | $r_{\text{SOI}} = r\,(\mu_{\text{planet}}/\mu_{\text{Sun}})^{2/5}$ |
| Planet and transfer speeds around the Sun | $v_{\text{planet}} = \sqrt{\mu_{\text{Sun}}/r}$, $\quad v_t = \sqrt{\mu_{\text{Sun}}(2/r - 1/a_t)}$ |
| Hyperbolic excess speed | $v_\infty = \lvert v_t - v_{\text{planet}}\rvert$ |
| Speed on a hyperbola | $v^2 = v_\infty^2 + 2\mu/r$ |
| Departure or capture burn (circular orbit) | $\Delta V = \sqrt{v_\infty^2 + 2\mu/r_p} - \sqrt{\mu/r_p}$ |
| Time of flight | $t_f = \pi\sqrt{a_t^3/\mu_{\text{Sun}}}$ |
| Phase angle at departure | ${180}^\circ - n_2\,t_f$ |
| Synodic period | $S = 1/\lvert 1/T_1 - 1/T_2\rvert$ |

:::

:::{exercise} For discussion
:label: ex-p24-discussion

1. A spacecraft bound for Venus leaves Earth's sphere of influence moving against Earth's motion around the Sun. Explain why, using the speeds at the ends of the transfer orbit.
2. For the same $v_\infty$, would a departure from a parking orbit at 1,000 km altitude cost more or less than one from 185 km? Reason from the energy argument for burning deep in the gravity well before computing.
3. Capture into a long ellipse costs less than capture into a low circular orbit with the same periapsis. What does a mission give up by choosing the ellipse?
4. The synodic period with Jupiter is just over one year. Describe the motion of the two planets that makes this so.
5. The Moon's sphere of influence is not small next to its distance from Earth. Which assumption of the method does this break, and how would you check the estimate?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-2-4.html
:label: quiz-2-4
:enumerated: false
:width: 100%

Quiz for Standard 2.4: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Bate, R. R., Mueller, D. D., and White, J. E., *Fundamentals of Astrodynamics*, Dover, 1971. Chapter 8.
- Curtis, H. D., *Orbital Mechanics for Engineering Students*, 3rd ed., Butterworth-Heinemann, 2014. Chapter 8.
- Solomon, S. C., McNutt, R. L., Gold, R. E., and Domingue, D. L., "MESSENGER Mission Overview," *Space Science Reviews*, Vol. 131, 2007, pp. 3-39. DOI 10.1007/s11214-007-9247-6.

