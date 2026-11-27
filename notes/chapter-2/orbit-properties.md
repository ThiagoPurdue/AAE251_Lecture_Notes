---
title: "2.1 Orbit Properties"
short_title: 2.1 Orbit Properties
---

:::{include} ../_parts/standards/2.1.md
:::

Every orbit in this chapter starts from Newton's law of gravitation, which leads to the two-body model, the orbit equation, Kepler's laws, and the vis-viva equation. Together, these relations let us find a spacecraft's speed at any point and classify any trajectory from a single position and speed. We will apply them to an Earth satellite, a Venus orbiter, and a small body crossing Earth's orbit.

:::{note} What to take from this page
- In the two-body problem every path is a conic section with the central body at a focus. Two numbers fix its size and shape: the semi-major axis $a$ and the eccentricity $e$.
- The period depends only on $a$, with $T = 2\pi\sqrt{a^3/\mu}$.
- The specific orbital energy $\varepsilon = v^2/2 - \mu/r = -\mu/(2a)$ is the same at every point of an orbit. The vis-viva equation follows from it and gives the speed anywhere.
- The sign of $\varepsilon$, or the speed against the escape speed $\sqrt{2\mu/r}$, tells whether a spacecraft stays bound or leaves.
:::

## Gravity between two bodies

Two masses attract each other along the line between their centers. Newton's law of universal gravitation gives the magnitude of the force:

:::{math}
:label: eq-p21-gravity
F = \frac{G\,m_1 m_2}{r^2}
:::

Here $m_1$ and $m_2$ are the two masses, $r$ is the distance between their centers, and $G = 6.674 \times {10}^{-11}$ N·m²/kg² is the universal gravitational constant. The force on each body points toward the other, and the two forces are equal and opposite ({numref}`fig-p21-two-body`).

:::{figure} figures/p21-two-body.svg
:label: fig-p21-two-body
:alt: A large sphere of mass m 1 on the left and a small sphere of mass m 2 on the right. An arrow labeled F starts at the large sphere and points right, toward the small one; an equal arrow labeled F starts at the small sphere and points left, toward the large one. A dimension line below gives the distance r between the two centers.
:width: 60%

Schematic, not to scale. Each body pulls on the other with a force of the same magnitude $F$, along the line between the centers; $r$ is measured from center to center.
:::

In orbit work we do not use $G$ and the mass of the central body separately. We use their product, the {term}`gravitational parameter`

:::{math}
:label: eq-p21-mu
\mu = G M
:::

where $M$ is the mass of the central body. We know the product far better than either factor, because we measure it directly from the motion of moons and spacecraft. If you keep distances in kilometers and $\mu$ in km³/s², every speed on this page comes out in km/s.

:::{table} Constants of the bodies used in this chapter: gravitational parameter, radius (equatorial for Earth, Jupiter, and Saturn; mean for the others), mean distance from the Sun, and orbital period around the Sun.
:label: tbl-p21-constants

| Body | Gravitational parameter $\mu$ (km³/s²) | Radius $R$ (km) | Distance from the Sun (km) | Orbital period (days) |
| --- | ---: | ---: | ---: | ---: |
| Sun | $1.327 \times {10}^{11}$ | 696,000 | | |
| Mercury | $2.203 \times {10}^{4}$ | 2,440 | $5.790 \times {10}^{7}$ | 87.97 |
| Venus | $3.249 \times {10}^{5}$ | 6,052 | $1.082 \times {10}^{8}$ | 224.7 |
| Earth | $3.986 \times {10}^{5}$ | 6,378 | $1.496 \times {10}^{8}$ | 365.26 |
| Moon | $4.903 \times {10}^{3}$ | 1,737 | | |
| Mars | $4.283 \times {10}^{4}$ | 3,390 | | |
| Jupiter | $1.267 \times {10}^{8}$ | 71,492 | $7.784 \times {10}^{8}$ | 4,332.6 |
| Saturn | $3.793 \times {10}^{7}$ | 60,268 | $1.427 \times {10}^{9}$ | 10,759 |

:::

Earth's distance from the Sun, $1.496 \times {10}^{8}$ km, is one astronomical unit (AU). For Earth the table gives the equatorial radius; [launch to orbit](launch-to-orbit.md) uses the mean radius, 6,371 km.

:::{warning} Kilometers and meters
Tables in SI units give $\mu$ in m³/s² (Earth: $3.986 \times {10}^{14}$ m³/s²). If you mix that value with a radius in kilometers, your speeds are off by a factor of 31.6, the square root of 1,000. Keep every length in kilometers, or every length in meters, from start to finish.
:::

## The two-body problem

To find the path that gravity produces, we start with a simplified case. When three or more bodies attract one another, the equations of motion have no general closed-form solution. Heinrich Bruns proved this in 1887, and Henri Poincaré extended the result a few years later (O'Connor and Robertson 2006). Two isolated bodies do have an exact solution, and it gives a reliable baseline for most spacecraft orbits. This {term}`two-body problem` rests on four assumptions:

1. Each body is a point mass, or a sphere whose mass is spread evenly in layers, so that it attracts as if all its mass were concentrated at its center.
2. Only two bodies are present.
3. Gravity is the only force. There is no drag, no thrust, and no pressure from sunlight.
4. The spacecraft is so light that the central body does not move in response to it.

Under these assumptions the spacecraft moves in a fixed plane through the center of the central body, along a curve we can write in closed form. Real orbits slowly depart from this ideal path. Atmospheric drag lowers low orbits on every revolution, the Moon and the Sun pull on high Earth orbits, and Earth's equatorial bulge slowly rotates the plane of an inclined orbit (Mesarch 2018). We begin with the two-body orbit and include these perturbations when they matter.

## The orbit equation

Solving the two-body equations of motion in polar coordinates $(r, \theta)$ centered on the attracting body gives the orbit equation:

:::{math}
:label: eq-p21-orbit
r = \frac{a\,(1 - e^2)}{1 + e\cos\theta}
:::

This relation gives the radial distance $r$ from the center of the central body as a function of the {term}`true anomaly` $\theta$. We measure $\theta$ at the central body from the point of closest approach in the direction of motion. Two constants fix the curve. The {term}`semi-major axis` $a$ sets its size, and the {term}`eccentricity` $e$ sets its shape. The numerator $p = a(1 - e^2)$ is the semi-latus rectum; because $\cos 90° = 0$, the denominator becomes 1 at $\theta = 90°$, leaving $r = p$.

For a closed orbit the curve is an ellipse ({numref}`fig-p21-ellipse-geometry`). The central body lies at one focus, and the other focus is empty. The longest diameter of the ellipse is $2a$ and the shortest is $2b$, where $b$ is the semi-minor axis. The center lies a distance $c$ from each focus, and

:::{math}
:label: eq-p21-ellipse
e = \frac{c}{a}, \qquad b = a\sqrt{1 - e^2}
:::

:::{figure} figures/p21-ellipse-geometry.svg
:label: fig-p21-ellipse-geometry
:alt: An ellipse of eccentricity 0.5 with its major axis horizontal, the central body at the right focus, and the empty focus and the center on the axis to its left. Dimension lines mark a from the apoapsis on the left to the center, c from the center to the focus, and b from the center down to the ellipse. Below, r a runs from the apoapsis to the focus and r p from the focus to the periapsis on the right. A spacecraft on the upper right is joined to the focus by a line r, at angle theta from the direction of periapsis.
:width: 65%

Schematic of an ellipse with $e = 0.5$. The central body is at a focus, not at the center. The radius $r$ and the true anomaly $\theta$ locate the spacecraft; $\theta$ is measured from periapsis in the direction of motion.
:::

The closest point to the central body is the {term}`periapsis` and the farthest is the {term}`apoapsis`; together they are the apsides, and the line through them is the major axis. With $\theta = 0$ and $\theta = 180°$ in [](#eq-p21-orbit), we get their radii:

:::{math}
:label: eq-p21-apsides
r_p = a\,(1 - e), \qquad r_a = a\,(1 + e)
:::

Adding and subtracting the two radii gives the two results you will use most often:

:::{math}
:label: eq-p21-a-e
a = \frac{r_p + r_a}{2}, \qquad e = \frac{r_a - r_p}{r_a + r_p}
:::

Each central body has its own names for the apsides ({numref}`tbl-p21-apsides`). In this book we write "periapsis" and "apoapsis" in general, and "perigee" and "apogee" for orbits around Earth.

:::{table} Names of the closest and farthest points of an orbit.
:label: tbl-p21-apsides

| Central body | Closest point | Farthest point |
| --- | --- | --- |
| Any body | periapsis | apoapsis |
| Earth | perigee | apogee |
| Sun | perihelion | aphelion |
| Moon | perilune | apolune |

:::

:::{warning} Altitude is not radius
Mission data gives altitudes $h$ above the surface. Every equation on this page needs radii from the center, $r = R + h$. A 400 km orbit around Earth has $r = 6{,}778$ km, not 400 km. Add the radius of the body before you compute anything, and subtract it again when you need an altitude at the end.
:::

## Conic sections

The eccentricity determines which of four curves the orbit follows. All four are {term}`conic sections <conic section>`, the shapes formed when a plane cuts a cone, and in every orbit the central body lies at a focus ({numref}`fig-p21-conic-sections`).

- **Circle**, $e = 0$: the radius is constant and equal to $a$.
- **Ellipse**, $0 < e < 1$: a closed orbit between $r_p$ and $r_a$.
- **Parabola**, $e = 1$: an open path. The spacecraft passes periapsis once and moves away forever, its speed falling toward zero. Its $a$ is infinite.
- **Hyperbola**, $e > 1$: an open path that retains positive speed far from the body. Because $1 - e^2$ is negative when $e > 1$, the semi-major axis $a$ is taken as negative so that $p = a(1 - e^2)$ and the radius $r$ remain positive.

:::{figure} figures/p21-conic-sections.svg
:label: fig-p21-conic-sections
:alt: Four curves through one periapsis point on the right, all with the same focus, each with arrowheads showing counterclockwise motion. A circle with e equal to 0 is the smallest, and an ellipse with e equal to 0.5 extends three times as far on the left. A parabola with e equal to 1 opens toward the left, and a hyperbola with e equal to 2 opens wider still.
:width: 60%

Schematic of the four conic sections with one focus and one periapsis radius. A larger eccentricity gives a more elongated or more open path. Only the circle and the ellipse close.
:::

A spacecraft on a circle or an ellipse comes back to the same point every revolution, and we call it a satellite. A spacecraft on a parabola or a hyperbola passes the central body once and does not return. A spacecraft leaving one planet for another departs on a hyperbola, the first piece of [patched conics](patched-conics.md).

## Where the orbit sits in space

The orbit equation places the spacecraft in its own plane, with angles counted from periapsis. To place the orbit itself in space, we need three more angles. Each is measured from a reference plane and a reference direction in that plane. For Earth orbits the plane is Earth's equator, and for Sun orbits it is the plane of Earth's orbit; for both, the direction is that of the vernal equinox. The orbit plane crosses the reference plane along the {term}`line of nodes`. The {term}`ascending node` is where the spacecraft crosses the reference plane going north.

:::{figure} figures/p21-orbital-elements.svg
:label: fig-p21-orbital-elements
:alt: A three-dimensional drawing of an elliptical orbit tilted against a flat reference plane drawn as a shaded disc; the part of the orbit below the plane is dashed. The orbit crosses the plane at the ascending node, on the front right, along a dashed line of nodes through the central body. Angle Omega, 60 degrees, lies in the reference plane from the reference direction to the ascending node, and angle i, 40 degrees, at the node is the tilt of the orbit plane. Angle omega, 70 degrees, lies in the orbit plane from the node to periapsis, and angle theta, 80 degrees, from periapsis to the spacecraft; the arcs of Omega, omega, and theta end in arrowheads that show the direction in which each angle is measured.
:width: 85%

Schematic of the orbital elements, not to scale (the central body is drawn small), for $i = 40°$, $\Omega = 60°$, $\omega = 70°$, and $\theta = 80°$. Angles $i$ and $\Omega$ orient the orbit plane, $\omega$ turns the ellipse within its plane, and $\theta$ locates the spacecraft. The arrowheads on the arcs of $\Omega$, $\omega$, and $\theta$ show the direction in which each angle is measured: $\Omega$ eastward in the reference plane, from the reference direction to the ascending node; $\omega$ and $\theta$ in the orbit plane, in the direction of motion.
:::

Six numbers, the classical orbital elements, fix the orbit and the position on it ({numref}`tbl-p21-elements`). In the plane of the orbit, the angle from the ascending node to the spacecraft is $\omega + \theta$.

:::{table} The six classical orbital elements.
:label: tbl-p21-elements

| Element | Symbol | What it fixes |
| --- | --- | --- |
| Semi-major axis | $a$ | size of the orbit |
| Eccentricity | $e$ | shape of the orbit |
| Inclination | $i$ | tilt of the orbit plane from the reference plane, measured at the ascending node (0° to 180°) |
| Right ascension of the ascending node (longitude of the ascending node, around the Sun) | $\Omega$ | direction of the ascending node, from the reference direction |
| Argument of periapsis | $\omega$ | direction of periapsis in the orbit plane, from the ascending node |
| True anomaly | $\theta$ | position of the spacecraft, from periapsis |

:::

In the rest of this chapter we use only the {term}`inclination`. An orbit with $i$ below 90° moves eastward with Earth's rotation; above 90°, it moves westward. The launch site and the launch direction set the inclination, as [launch to orbit](#p23-azimuth) shows, and the inclination sets the highest latitude a satellite passes over, as [ground tracks](ground-tracks-and-orbit-lifetime.md) shows.

## Kepler's laws

The orbit equation describes the geometry of the path, and Kepler's laws connect that geometry to motion in time, telling us how the satellite's speed varies around the orbit and how long each revolution takes. Johannes Kepler discovered three laws of planetary motion from the observations of Tycho Brahe, publishing the first two in 1609 and the third in 1619 (Field 1999). Newton later derived all three from his law of gravitation, showing that they apply to any satellite around any central body.

**First law.** A satellite moves on an ellipse with the central body at one focus. This is the closed case of the orbit equation.

**Second law.** The line from the central body to the satellite sweeps out equal areas in equal times ({numref}`fig-p21-equal-areas`). Near periapsis the line is short, so it must turn through a large angle to cover a given area; near apoapsis it is long and turns slowly. So the satellite moves fastest at periapsis and slowest at apoapsis.

:::{figure} figures/p21-equal-areas.svg
:label: fig-p21-equal-areas
:alt: An ellipse of eccentricity 0.6 with the central body at the right focus and two shaded sectors that start at the body. The sector A 1 reaches the orbit around periapsis and is short and wide, spanning 127 degrees. The sector A 2 reaches the orbit around apoapsis and is long and narrow, spanning 9.4 degrees. Both are swept in the same time Delta t, and their areas are equal.
:width: 65%

Computed for $e = 0.6$; the central body is a point, not to scale. Each sector is swept in one twelfth of the period, one centered on periapsis ($A_1$) and one on apoapsis ($A_2$). The two areas are equal.
:::

The rate at which area is swept is half the product of the radius and the part of the velocity perpendicular to it. At the apsides the velocity is perpendicular to the radius, so the second law gives

:::{math}
:label: eq-p21-apsides-speed
r_p\, v_p = r_a\, v_a
:::

**Third law.** The square of the {term}`orbital period` is proportional to the cube of the semi-major axis. Newton's law supplies the constant:

:::{math}
:label: eq-p21-period
T = 2\pi\sqrt{\frac{a^3}{\mu}}
:::

The period depends on $a$ alone. A circle and a long ellipse with the same $a$ around the same body take the same time. For two orbits around the same body the constant cancels:

:::{math}
:label: eq-p21-period-ratio
\frac{T_1^2}{T_2^2} = \frac{a_1^3}{a_2^3}
:::

Doubling the semi-major axis multiplies the period by $2^{3/2} = 2.828$. For a circular orbit 400 km above Earth, $a = 6{,}778$ km and $T = 5{,}553$ s, or about 92.6 minutes. This is why astronauts in {term}`low Earth orbit` see a sunrise about every hour and a half. We see how a launch vehicle reaches such an orbit in [launch to orbit](launch-to-orbit.md).

:::{warning} Seconds, minutes, and hours
With $\mu$ in km³/s², [](#eq-p21-period) gives $T$ in seconds. Convert a period given in hours or minutes to seconds before solving for $a$, and convert the answer back only at the end.
:::

(p21-vis-viva)=
## Energy and speed

Because the speed changes around the orbit, we use energy to find it at any point. Gravity is a conservative force and the only force acting, so the sum of kinetic and potential energy stays constant. The kinetic energy of a mass $m$ moving at speed $v$ is $\tfrac{1}{2}mv^2$. The potential energy at distance $r$ from the central body is $-GMm/r$, taken as zero infinitely far away and negative everywhere closer. The total is

:::{math}
:label: eq-p21-energy-total
E_{\text{tot}} = \frac{1}{2}\, m v^2 - \frac{G M m}{r}
:::

Dividing by $m$ removes the mass of the spacecraft and leaves the {term}`specific orbital energy`, the energy per unit mass, in km²/s²:

:::{math}
:label: eq-p21-energy
\varepsilon = \frac{v^2}{2} - \frac{\mu}{r}
:::

As the spacecraft climbs toward apoapsis, its specific potential energy $-\mu/r$ rises (becomes less negative) and its specific kinetic energy $v^2/2$ falls by the same amount, keeping $\varepsilon$ constant.

The energy also depends on the size of the orbit, and the second law gives us the link. We write [](#eq-p21-energy) at periapsis and at apoapsis and set the two equal:

$$
\frac{v_p^2}{2} - \frac{\mu}{r_p} = \frac{v_a^2}{2} - \frac{\mu}{r_a}
\quad\Longrightarrow\quad
v_p^2 - v_a^2 = 2\mu\left(\frac{1}{r_p} - \frac{1}{r_a}\right) = 2\mu\,\frac{r_a - r_p}{r_p\, r_a}
$$

Now we replace $v_a$ with $v_p r_p/r_a$ from [](#eq-p21-apsides-speed). The left side becomes $v_p^2 (r_a^2 - r_p^2)/r_a^2$, and dividing both sides by $(r_a - r_p)$ leaves

$$
v_p^2 = \frac{2\mu\, r_a}{r_p\,(r_a + r_p)}
$$

We put this back into the energy at periapsis and use $r_a + r_p = 2a$:

$$
\varepsilon = \frac{\mu\, r_a}{r_p\,(r_a + r_p)} - \frac{\mu}{r_p}
= \frac{\mu\,(r_a - r_a - r_p)}{r_p\,(r_a + r_p)}
= -\frac{\mu}{r_a + r_p}
$$

:::{math}
:label: eq-p21-energy-a
\varepsilon = -\frac{\mu}{2a}
:::

The energy depends on $a$ alone, as the period does. Two orbits with the same semi-major axis have the same energy, whatever their eccentricities.

If we set the two expressions for $\varepsilon$ equal, $v^2/2 - \mu/r = -\mu/(2a)$, and solve for $v^2$, we get the {term}`vis-viva equation`:

:::{math}
:label: eq-p21-vis-viva
v^2 = \mu\left(\frac{2}{r} - \frac{1}{a}\right)
:::

With it you can find the speed at any radius on any conic section, using $1/a = 0$ for a parabola and the negative $a$ for a hyperbola. We compute every burn on [orbit transfers](orbit-transfers.md) from this equation. Notice that it gives the speed (the magnitude of the velocity), not its direction. The velocity is perpendicular to the radius at the apsides and on a circle; elsewhere on an ellipse it is tilted from the local horizontal.

(p21-circular-and-escape)=
## Circular speed and escape speed

Two speeds at a given radius mark the boundaries between the types of path. On a circle the radius never changes and equals $a$. With $r = a$, the vis-viva equation gives the {term}`circular speed`:

:::{math}
:label: eq-p21-vc
v_c = \sqrt{\frac{\mu}{r}}
:::

At Earth's surface, $\mu/R = 62.496$ km²/s² and $v_c = 7.905$ km/s. That is the speed a satellite would need to circle Earth at zero altitude, if there were no air. At 400 km altitude it is 7.669 km/s. The circular speed falls as the radius grows. {numref}`fig-p21-planet-speeds` shows it for the planets, from Mercury at 47.87 km/s to Neptune at 5.431 km/s.

:::{figure} figures/p21-planet-speeds.svg
:label: fig-p21-planet-speeds
:alt: Orbital speed in kilometers per second against distance from the Sun in astronomical units, on a logarithmic axis from 0.3 to 40. A single curve, v c equal to the square root of mu Sun over r, falls from 54.38 kilometers per second at 0.3 AU to 4.709 at 40 AU. All eight planets sit on the curve, from Mercury to Neptune; Mars, between Earth and Jupiter, is marked by name only. Mercury moves at 47.87, Venus at 35.02, Earth at 29.78, Jupiter at 13.06, Saturn at 9.643, Uranus (19.19 AU) at 6.799, and Neptune (30.07 AU) at 5.431 kilometers per second.
:width: 80%

Computed: circular speed around the Sun with $\mu_{\text{Sun}}$ from {numref}`tbl-p21-constants`, at the mean distance of each of the eight planets (Standish and Williams). The farther a planet is from the Sun, the slower it moves.
:::

To escape the central body permanently, a spacecraft must enter an open path, since any elliptical orbit eventually returns to periapsis. The boundary between bound and open paths is the parabola, which has $e = 1$ and an infinite semi-major axis $a$. Setting $1/a = 0$ in the vis-viva equation gives the {term}`escape speed`:

:::{math}
:label: eq-p21-vesc
v_{\text{esc}} = \sqrt{\frac{2\mu}{r}} = \sqrt{2}\; v_c
:::

At Earth's surface $v_{\text{esc}} = 11.18$ km/s. At any radius the escape speed is $\sqrt{2} = 1.414$ times the circular speed. A spacecraft moving at the escape speed has zero energy and reaches infinite distance with no speed left. The direction does not matter, as long as the path does not cross the surface of the body.

(p21-classify)=
## Classifying a trajectory

One radius and one speed are enough to tell whether a spacecraft stays bound to the central body. The energy [](#eq-p21-energy) has no angle in it, and its sign sets the type of conic ({numref}`tbl-p21-classify`).

:::{table} The four types of trajectory in the two-body problem.
:label: tbl-p21-classify

| Type | Eccentricity $e$ | Energy $\varepsilon$ | Speed $v$ at radius $r$ | Semi-major axis $a$ |
| --- | --- | --- | --- | --- |
| Circle | $e = 0$ | negative | $v = v_c$, with the velocity perpendicular to the radius | $a = r$ |
| Ellipse | $0 < e < 1$ | negative | $v < v_{\text{esc}}$ | finite and positive |
| Parabola | $e = 1$ | zero | $v = v_{\text{esc}}$ | infinite |
| Hyperbola | $e > 1$ | positive | $v > v_{\text{esc}}$ | negative |

:::

{numref}`fig-p21-trajectories-by-speed` shows the five cases from one starting point, with the velocity perpendicular to the radius. Below the circular speed, the start becomes the apoapsis of an ellipse that dips closer to the body. Above it, the start becomes the periapsis of a larger ellipse. At the escape speed the path opens into a parabola, and above it into a hyperbola.

:::{figure} figures/p21-trajectories-by-speed.svg
:label: fig-p21-trajectories-by-speed
:alt: Earth to scale with five paths, each with its own line style and label, that all leave one point on the right, at radius 13,000 kilometers, moving straight up. At 0.85 times the circular speed the path is an ellipse inside the circle, at the circular speed, 5.537 kilometers per second, it is a circle. At 1.15 times the circular speed it is a larger ellipse reaching far to the left. At the escape speed, 7.831 kilometers per second, it is a parabola, and at 1.2 times the escape speed a hyperbola, both open toward the upper left.
:width: 90%

Computed for Earth, to scale, from a start at radius 13,000 km with the velocity perpendicular to the radius. The speed at the start alone sets the type of path: below the escape speed the path closes, and at or above it the path is open. At that radius, $v_c = 5.537$ km/s and $v_{\text{esc}} = 7.831$ km/s. The open paths are drawn only after the start.
:::

:::{tip} Method: classifying a trajectory
1. Find the radius from the center of the body, $r = R + h$.
2. Compute the energy $\varepsilon = v^2/2 - \mu/r$, or compare $v$ with $v_{\text{esc}} = \sqrt{2\mu/r}$.
3. Read the type from the sign. A negative energy means a bound ellipse (or a circle); then $a = -\mu/(2\varepsilon)$, and the period follows from [](#eq-p21-period). Zero means a parabola, and a positive energy means a hyperbola, so the spacecraft leaves.
:::

The speed determines the specific energy $\varepsilon$ and the semi-major axis $a$, but not the eccentricity $e$, which also depends on the direction of the velocity. Suppose two spacecraft pass the same point at the same speed below escape speed, one moving horizontally and one climbing. Both follow ellipses with the same semi-major axis $a$ and orbital period $T$, but with different eccentricities $e$ and different apsis radii.

## Worked examples

### Example 1: an Earth satellite from its altitudes

A satellite orbits Earth with a perigee altitude of 700 km and an apogee altitude of 5,800 km. Find the semi-major axis, the eccentricity, the period, the speeds at perigee and apogee, and the specific orbital energy. Use $\mu = 3.986 \times {10}^{5}$ km³/s² and $R = 6{,}378$ km.

1. **Radii.** Measured from the center, $r_p = 6{,}378 + 700 = 7{,}078$ km and $r_a = 6{,}378 + 5{,}800 = 12{,}178$ km.
2. **Semi-major axis**, [](#eq-p21-a-e): $a = (7{,}078 + 12{,}178)/2 = 9{,}628$ km.
3. **Eccentricity**, [](#eq-p21-a-e): $e = (12{,}178 - 7{,}078)/(12{,}178 + 7{,}078) = 5{,}100/19{,}256 = 0.2649$.
4. **Period**, [](#eq-p21-period): $T = 2\pi\sqrt{{9{,}628}^3/(3.986 \times {10}^{5})} = 9{,}402$ s, which is 156.7 minutes or 2.612 hours.
5. **Perigee speed**, [](#eq-p21-vis-viva): $v_p^2 = 3.986 \times {10}^{5}\,(2/7{,}078 - 1/9{,}628) = 71.23$ km²/s², so $v_p = 8.440$ km/s.
6. **Apogee speed.** $v_a^2 = 3.986 \times {10}^{5}\,(2/12{,}178 - 1/9{,}628) = 24.06$ km²/s², so $v_a = 4.905$ km/s.
7. **Specific orbital energy**, [](#eq-p21-energy-a): $\varepsilon = -3.986 \times {10}^{5}/(2 \times 9{,}628) = -20.70$ km²/s².

**Check.** The energy at perigee from [](#eq-p21-energy) is $35.62 - 56.32 = -20.70$ km²/s², matching our value above. The second law checks out as well, since $r_p v_p = 7{,}078 \times 8.440 = 59{,}738$ km²/s and $r_a v_a = 12{,}178 \times 4.905 = 59{,}733$ km²/s, the same to the four figures of the speeds. The satellite moves faster at perigee than at apogee, as {numref}`fig-p21-speed-around-orbit` shows. At $\theta = 90°$ and $\theta = 270°$ the radius is $p = r_p(1 + e) = 7{,}078 \times 1.2649 = 8{,}953$ km and the speed is 6.903 km/s.

:::{figure} figures/p21-speed-around-orbit.svg
:label: fig-p21-speed-around-orbit
:alt: The orbit of example 1 around Earth, drawn to scale, with velocity arrows at four points, drawn just outside the orbit, and a reference arrow of 2 kilometers per second. At perigee, on the right, the arrow points straight up and reads 8.440 kilometers per second. At apogee, on the left, it points straight down and reads 4.905. At the two points directly above and below Earth the arrows read 6.903 kilometers per second; the upper one tilts outward from the local horizontal (climbing) and the lower one inward (descending).
:width: 60%

Computed for the orbit of Example 1 (perigee altitude 700 km, apogee altitude 5,800 km), to scale, with velocity arrows to scale at four points. The arrows are tangent to the orbit, drawn just outside it, and longest at perigee.
:::

### Example 2: a Venus orbiter from its period

A spacecraft orbits Venus with a period of 8.0 hours and a periapsis altitude of 400 km. Find the semi-major axis, the apoapsis radius and altitude, and the eccentricity. Use $\mu = 3.249 \times {10}^{5}$ km³/s² and $R = 6{,}052$ km.

1. **Period in seconds.** $T = 8.0 \times 3{,}600 = 28{,}800$ s.
2. **Semi-major axis.** Solving [](#eq-p21-period) for $a$ gives $a = \left[\mu\,(T/2\pi)^2\right]^{1/3}$. With $T/2\pi = 4{,}583.66$ s, $a = \left[3.249 \times {10}^{5} \times {4{,}583.66}^2\right]^{1/3} = 18{,}969.6$ km.
3. **Periapsis radius.** $r_p = 6{,}052 + 400 = 6{,}452$ km.
4. **Apoapsis radius and altitude.** From $a = (r_p + r_a)/2$, $r_a = 2a - r_p = 31{,}487$ km. The apoapsis altitude is $31{,}487 - 6{,}052 = 25{,}435$ km.
5. **Eccentricity.** $e = (31{,}487 - 6{,}452)/(31{,}487 + 6{,}452) = 25{,}035/37{,}939 = 0.6599$.

**Check.** $r_p = a(1 - e) = 18{,}969.6 \times 0.3401 = 6{,}452$ km. Keep the semi-major axis to one decimal here, because $r_a$ is the difference of two large numbers and rounding $a$ to 18,970 km changes its last digit.

### Example 3: a small body crossing Earth's orbit

A small body crosses the distance of Earth's orbit from the Sun, $r = 1.496 \times {10}^{8}$ km, moving at 40.0 km/s relative to the Sun. Determine whether it is bound to the Sun. Use $\mu_{\text{Sun}} = 1.327 \times {10}^{11}$ km³/s².

1. **Energy terms.** $v^2/2 = {40.0}^2/2 = 800.0$ km²/s² and $\mu/r = 1.327 \times {10}^{11}/(1.496 \times {10}^{8}) = 887.03$ km²/s².
2. **Energy.** $\varepsilon = 800.0 - 887.03 = -87.03$ km²/s², which is negative.
3. **Type and size.** The body is on an ellipse around the Sun and will return. Its semi-major axis is $a = -\mu/(2\varepsilon) = 7.624 \times {10}^{8}$ km, or 5.096 AU. By [](#eq-p21-period-ratio), with Earth's orbit of 1 AU and one year as the reference, its period is ${5.096}^{3/2} = 11.50$ years.

**Check.** The escape speed at 1 AU is $\sqrt{2\mu/r} = 42.12$ km/s, and 40.0 km/s is below it. Earth's own circular speed there is 29.78 km/s.

Suppose instead the body crossed the same point at 45.0 km/s. Then $v^2/2$ would be 1,012.5 km²/s², and $\varepsilon = 125.5$ km²/s² would be positive. The path would be a hyperbola, and the body would leave the solar system. Position and speed alone do not give the eccentricity or the closest distance to the Sun. For those we also need the direction of the velocity.

## Summary

:::{important} Summary
- Under the two-body assumptions, an orbit is a conic section with the central body at a focus. The semi-major axis sets its size and the eccentricity its shape. Always work with radii from the center.
- The period and the energy depend only on $a$. The second law makes the spacecraft fastest at periapsis.
- The vis-viva equation gives the speed anywhere. The circular speed is $\sqrt{\mu/r}$ and the escape speed is $\sqrt{2}$ times larger.
- The sign of the energy classifies a trajectory as bound when negative, parabolic when zero, and hyperbolic when positive.
:::

:::{table} The equations of this page.
:label: tbl-p21-equations

| Quantity | Equation |
| --- | --- |
| Orbit equation | $r = a(1 - e^2)/(1 + e\cos\theta)$ |
| Apsides | $r_p = a(1 - e)$, $r_a = a(1 + e)$ |
| Semi-major axis and eccentricity from the apsides | $a = (r_p + r_a)/2$, $e = (r_a - r_p)/(r_a + r_p)$ |
| Period | $T = 2\pi\sqrt{a^3/\mu}$ |
| Specific orbital energy | $\varepsilon = v^2/2 - \mu/r = -\mu/(2a)$ |
| Vis-viva equation | $v^2 = \mu\,(2/r - 1/a)$ |
| Circular speed | $v_c = \sqrt{\mu/r}$ |
| Escape speed | $v_{\text{esc}} = \sqrt{2\mu/r}$ |

:::

:::{exercise} For discussion
:label: ex-p21-discussion

1. Two satellites around Earth have the same semi-major axis. One is on a circle and one on a long ellipse. Compare their periods and their energies. Which one reaches the higher speed, and where?
2. A satellite in a circular orbit fires its engine forward for a moment and speeds up. Where on its new orbit is the point where it fired?
3. The escape speed does not depend on the direction of the velocity. Which directions still fail to escape, and why?
4. Why does the two-body model work well for a satellite 20,000 km above Earth but poorly for one 250 km above it?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-2-1.html
:label: quiz-2-1
:enumerated: false
:width: 100%

Quiz for Standard 2.1: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 8.
- Bate, R. R., Mueller, D. D., and White, J. E., *Fundamentals of Astrodynamics*, Dover, 1971. Chapters 1 and 2.
- Curtis, H. D., *Orbital Mechanics for Engineering Students*, 3rd ed., Butterworth-Heinemann, 2014. Chapters 2 and 4.
- Field, J. V., "[Johannes Kepler](https://mathshistory.st-andrews.ac.uk/Biographies/Kepler/)," MacTutor History of Mathematics, University of St Andrews, 1999.
- Mesarch, M., "[GDC Orbit Primer](https://science.nasa.gov/wp-content/uploads/2023/05/GDC_OrbitPrimer.pdf)," NASA Goddard Space Flight Center, Navigation and Mission Design Branch, 2018.
- O'Connor, J. J., and Robertson, E. F., "[Ernst Heinrich Bruns](https://mathshistory.st-andrews.ac.uk/Biographies/Bruns/)," MacTutor History of Mathematics, University of St Andrews, 2006.
- Standish, E. M., and Williams, J. G., "[Keplerian Elements for Approximate Positions of the Major Planets](https://ssd.jpl.nasa.gov/planets/approx_pos.html)," Jet Propulsion Laboratory, Solar System Dynamics.

