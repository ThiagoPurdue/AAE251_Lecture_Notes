---
title: Glossary
---

The notes use these terms in a fixed sense. In the text, a term with a dotted underline opens its definition.

:::{glossary}
Aerobraking
: Lowering the apoapsis of an orbit with atmospheric drag instead of a burn: the periapsis is placed in the upper atmosphere, and each pass removes a little speed. A small burn at the end lifts the periapsis out of the atmosphere.

Apoapsis
: The point of an orbit farthest from the central body, at radius $r_a = a(1 + e)$. Around Earth it is called the apogee, around the Sun the aphelion.

Ascending node
: The point where an orbit crosses the reference plane (the equator, for an Earth orbit) going north. The inclination is measured there.

Ballistic coefficient
: $B = m/(C_D A)$, the mass of a vehicle divided by its drag coefficient times its reference area, in kg/m². The higher it is, the less drag slows the vehicle.

Capture burn
: The burn at the periapsis of an arrival hyperbola, against the direction of motion, that slows a spacecraft enough to stay in orbit around the target. Without it the spacecraft flies past and leaves.

Circular speed
: The speed of a circular orbit of radius $r$: $v_c = \sqrt{\mu/r}$. It falls as the radius grows.

Circularization burn
: A single burn at periapsis or apoapsis that changes the speed to the circular speed at that radius, so the orbit becomes a circle through that point.

Conic section
: A curve cut from a cone by a plane: a circle, an ellipse, a parabola, or a hyperbola. Every trajectory of the two-body problem is one, with the central body at a focus.

Delta-V
: The magnitude of the change of a spacecraft's velocity vector made by a burn, written $\Delta V$ and given in km/s. Through the rocket equation it sets the propellant the burn uses.

Delta-V budget
: The total velocity change a launch vehicle must produce to reach its target orbit: the orbit speed plus the gravity, drag, and steering losses, minus the speed gained from Earth's rotation.

Departure burn
: The burn in a parking orbit that raises a spacecraft's speed to the speed of a departure hyperbola, so it leaves the planet with the hyperbolic excess speed it needs.

Eccentricity
: The number $e$ that sets the shape of a conic section: 0 for a circle, between 0 and 1 for an ellipse, 1 for a parabola, and more than 1 for a hyperbola. For an ellipse, $e = (r_a - r_p)/(r_a + r_p)$.

Escape speed
: The lowest speed at radius $r$ that carries a spacecraft away from the central body for good: $v_{\text{esc}} = \sqrt{2\mu/r}$, which puts it on a parabola.

Geostationary orbit
: A circular orbit in the equatorial plane with a period of one sidereal day. The spacecraft stays above one point on the equator, so a ground antenna can point at it without tracking.

Geosynchronous orbit
: An orbit whose period is one sidereal day. Its ground track repeats every day; a circular, equatorial one is a geostationary orbit.

Gravitational parameter
: The product $\mu = GM$ of the universal gravitational constant and the mass of the central body, in km³/s². Earth's is $3.986 \times {10}^{5}$ km³/s².

Gravity loss
: The part of a launch vehicle's velocity change spent holding the vehicle up against gravity while it climbs, $g\sin\gamma$ for each second at flight-path angle $\gamma$.

Ground track
: The path on a planet's surface directly below an orbiting spacecraft. On a planet that turns eastward, as Earth does, each pass crosses the equator farther west than the one before.

Hohmann transfer
: A transfer between two circular orbits in the same plane along half of an ellipse that touches both, with one tangential burn at each end. Of all two-burn transfers between such orbits, it needs the least delta-V.

Hyperbolic excess speed
: The speed $v_\infty$ a spacecraft has relative to a planet when it is far from the planet, after climbing out of the planet's gravity well. On the hyperbola, $v^2 = v_\infty^2 + 2\mu/r$.

Impulsive burn
: A burn treated as instantaneous: the velocity changes at once and the position does not, so the new orbit passes through the burn point.

Inclination
: The angle $i$ between the orbit plane and the reference plane (the equator, for an Earth orbit), measured at the ascending node, from 0° to 180°.

Launch azimuth
: The direction in which a launch vehicle flies, measured at the launch site in the horizontal plane, clockwise from north: ${90}^\circ$ is due east.

Launch window
: The span of time in which a launch can reach its target orbit. For a launch into a given orbit plane it opens when the rotating launch site passes through that plane.

Line of nodes
: The line along which the orbit plane crosses the reference plane (the equator, for Earth orbits), or along which two orbit planes cross. It passes through the center of the central body; a plane change can only be made at a point on it.

Low Earth orbit
: An orbit around Earth with an altitude between about 160 km and 2,000 km. Below it, drag brings a satellite down within days.

Orbit decay
: The slow loss of altitude of a low orbit caused by atmospheric drag. It speeds up as the orbit sinks into denser air and ends in reentry.

Orbital period
: The time $T$ for one revolution of a closed orbit: $T = 2\pi\sqrt{a^3/\mu}$. It depends only on the semi-major axis.

Parking orbit
: A low circular orbit where the launch vehicle leaves a spacecraft, which waits there until it starts a transfer to its working orbit.

Patched conics
: An approximate method for interplanetary trajectories: inside a planet's sphere of influence the spacecraft moves on a conic around the planet, outside it on a conic around the Sun, and the conics are joined at the edge of the sphere of influence.

Periapsis
: The point of an orbit closest to the central body, at radius $r_p = a(1 - e)$. Around Earth it is called the perigee, around the Sun the perihelion.

Phase angle
: The angle by which the target planet must lead the departure planet, seen from the Sun, at the moment of departure, so that the target reaches the meeting point together with the spacecraft.

Phasing orbit
: An orbit with a slightly different period from that of the original orbit, flown for one or more laps so that a spacecraft arrives back at the starting point earlier or later and meets a target there.

Plane change
: A burn that turns the orbit plane by an angle $\Delta i$ while keeping the speed, costing $2v\sin(\Delta i/2)$.

Polar orbit
: An orbit with an inclination of ${90}^\circ$, or close to it, which passes over both poles.

Prograde orbit
: An orbit with an inclination below ${90}^\circ$, in which the satellite moves eastward, the same way as Earth turns.

Retrograde orbit
: An orbit with an inclination between ${90}^\circ$ and ${180}^\circ$, in which the satellite moves westward, against Earth's rotation.

Semi-major axis
: Half the longest diameter of an ellipse, $a = (r_p + r_a)/2$. It sets the size, the period, and the energy of an orbit. It is infinite for a parabola and negative for a hyperbola.

Sidereal day
: The time a planet takes to turn once relative to the stars. For Earth it is 86,164 s, a little shorter than the 86,400 s solar day.

Specific orbital energy
: The kinetic plus potential energy per unit mass, $\varepsilon = v^2/2 - \mu/r = -\mu/(2a)$, in km²/s². It is the same at every point of an orbit; its sign tells whether the orbit is closed.

Sphere of influence
: The region around a planet inside which only the planet's gravity is counted in the motion of a spacecraft. Its radius is about $r(\mu_{\text{planet}}/\mu_{\text{Sun}})^{2/5}$, with $r$ the planet's distance from the Sun.

Standard
: A statement of one thing you can do by the end of the course, written as "I can ...". Each standard has its own page in these notes.

Sun-synchronous orbit
: A near-polar, slightly retrograde low Earth orbit whose plane is turned by Earth's equatorial bulge once a year, so the spacecraft passes over each place at the same local solar time.

Swath width
: The width of the strip of ground an instrument sees as the spacecraft passes over; $w = 2h\tan(\text{FOV}/2)$ for an instrument looking straight down with a narrow field of view.

Synodic period
: The time between two successive returns of the same alignment of two planets as seen from the Sun, $S = 1/|1/T_1 - 1/T_2|$. A launch opportunity between them comes once every synodic period.

Transfer orbit
: The orbit a spacecraft follows between two burns that take it from one orbit to another; for a Hohmann transfer, half of an ellipse.

True anomaly
: The angle $\theta$ at the central body from periapsis to the spacecraft, measured in the direction of motion.

Two-body problem
: The motion of two point masses under their mutual gravity alone. Its solution is a conic section with the central body at a focus.

Vis-viva equation
: $v^2 = \mu(2/r - 1/a)$: the speed at radius $r$ on an orbit of semi-major axis $a$, for every conic section.
:::
