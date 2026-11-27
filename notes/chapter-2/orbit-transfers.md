---
title: "2.2 Orbit Transfers"
short_title: 2.2 Orbit Transfers
---

:::{include} ../_parts/standards/2.2.md
:::

A launch vehicle often leaves a spacecraft in a low orbit, short of the orbit where it will work. An upper stage or the spacecraft's own engine then does the rest with a few short burns. Here we compute the delta-V required for those burns, covering the Hohmann transfer between two circular orbits, the single burn that makes an elliptical orbit circular, the phasing orbit that lets one spacecraft catch another, and the change of orbit plane. Then we find the order of maneuvers that keeps the total lowest. Every method uses [the vis-viva equation](#p21-vis-viva) and [circular speed](#p21-circular-and-escape), both from [orbit properties](orbit-properties.md).

:::{note} What to take from this page
- A burn changes the velocity at one point. The new orbit passes through that point, and the vis-viva equation gives the speed it needs there.
- A Hohmann transfer is two tangential burns half an ellipse apart. Its total delta-V is $\Delta V_1 + \Delta V_2$, and it takes half the period of the transfer ellipse.
- A smaller orbit has a shorter period, so a chaser catches a target ahead in the same orbit by slowing down into a smaller phasing orbit.
- Turning the orbit plane by $\Delta i$ requires $2v\sin(\Delta i/2)$, so it belongs where the spacecraft is slowest.
:::

## Burns and delta-V

A high orbit needs two things: the right altitude and the right speed at that altitude. Suppose we launch steeply and just coast up ({numref}`fig-p22-direct-vs-parking`). To reach 20,200 km on a coast arc that leaves the ground 60° above the horizontal, the rocket needs 9.818 km/s at the ground, and that is before we count air drag and Earth's rotation. At the top it is moving at only 1.178 km/s. The circular orbit there needs 3.873 km/s, so we still need a second burn of 2.695 km/s.

The coast arc also assumes the rocket gets all 9.818 km/s in an instant. A real rocket on a path this steep burns for minutes, and during the climb it spends much of its propellant just holding itself up against gravity. We call this the {term}`gravity loss`.

:::{figure} figures/p22-direct-vs-parking.svg
:label: fig-p22-direct-vs-parking
:alt: Earth to scale with the final circular orbit 20,200 kilometers up. A dotted steep coast arc leaves the surface and reaches the final orbit at its highest point moving at 1.178 kilometers per second, a third of the 3.873 kilometers per second the circle needs there. A second route starts on a low parking orbit that hugs Earth, then follows a dashed half-ellipse, the transfer orbit, from a burn labeled delta-V 1 beside Earth to a burn labeled delta-V 2 on the far side of the final orbit, where the half-ellipse touches it; the delta-V 1 arrow is the longer of the two.
:width: 70%

Computed, to scale: two routes to a circular orbit 20,200 km above Earth, a steep coast arc from the ground, and a parking orbit at 400 km followed by a Hohmann transfer (the parking orbit is the initial orbit of {numref}`fig-p22-hohmann`). The steep coast arc arrives far slower than the final orbit requires. The burn arrows are drawn to scale with their $\Delta V$.
:::

The usual route goes through a {term}`parking orbit`, a low circular orbit where the launch vehicle stops. We compute the velocity change needed to reach it in the delta-V budget of [launch to orbit](#p23-budget). Three reasons make this the standard plan:

- The launch vehicle follows an efficient ascent profile, gaining horizontal speed early and reaching low orbit with small losses.
- The spacecraft can coast in the parking orbit until it reaches the right point to start the transfer, and the operators can check out its systems first.
- The transfer burns are tangential, so the entire velocity change alters the speed instead of turning the velocity direction.

An engine burn lasts seconds to minutes, and one lap of a low orbit takes an hour and a half. We treat the burn as instantaneous.

:::{prf:definition} Impulsive burn and delta-V
:label: def-p22-impulsive-burn

An {term}`impulsive burn` changes the velocity of a spacecraft in an instant, with no change of position. The {term}`delta-V` of the burn, $\Delta V$, is the magnitude of the change of the velocity vector, $\Delta V = |\mathbf{v}_{\text{after}} - \mathbf{v}_{\text{before}}|$. When the burn points along the velocity, $\Delta V$ equals the change of speed.
:::

Two consequences follow. First, the orbit after the burn passes through the burn point, because the spacecraft has not moved. Second, two spacecraft at the same point with different speeds are on different orbits. The vis-viva equation, $v^2 = \mu\,(2/r - 1/a)$, ties the speed $v$ at radius $r$ to the {term}`semi-major axis` $a$. At a given $r$, a higher speed means a larger $a$. When you speed up, you raise the specific orbital energy $\varepsilon = -\mu/(2a)$ and make the orbit larger; slowing down makes it smaller.

The $\Delta V$ of a burn measures how much velocity change the propulsion system must supply. Through [the rocket equation](#p42-rocket-equation) in Chapter 4, it sets how much propellant the burn requires, so we plan a mission with a $\Delta V$ budget and report every maneuver on this page in km/s.

(p22-hohmann)=
## The Hohmann transfer

The {term}`Hohmann transfer` moves a spacecraft between two circular orbits in the same plane with two tangential burns. Walter Hohmann proposed it in 1925 (Hohmann 1925). For two coplanar circles it needs less $\Delta V$ than any other transfer with two burns. A three-burn transfer requires less $\Delta V$ only when the outer radius is more than about 12 times the inner one (Curtis 2014, Chapter 6), and that almost never happens around Earth. The same transfer, between the orbits of two planets around the Sun, is the first step of [patched conics](patched-conics.md).

:::{figure} figures/p22-hohmann.svg
:label: fig-p22-hohmann
:alt: Earth to scale with the initial circular orbit of radius r 1 just above its surface and the final circular orbit of radius r 2 far outside. A dashed half-ellipse runs counterclockwise from the right side of the initial orbit, where the burn delta-V 1 points along the motion, to the left side of the final orbit, where the burn delta-V 2 also points along the motion. The two burn arrows, drawn just outside the orbits, are in proportion to the burns, so the delta-V 1 arrow is the longer. Dimension lines below show that the major axis of the transfer ellipse, 2 a t, equals r 1 plus r 2.
:width: 70%

Computed for the worked example, to scale: the Hohmann transfer from a 400 km to a 20,200 km circular orbit around Earth. The transfer orbit is half an ellipse with its periapsis on the inner circle and its apoapsis on the outer circle, so $2a_t = r_1 + r_2$. The burn arrows are drawn to scale with their $\Delta V$.
:::

The two circular radii completely determine the {term}`transfer orbit`, because its {term}`periapsis` lies on the initial circle and its {term}`apoapsis` lies on the final circle on opposite sides of Earth ({numref}`fig-p22-hohmann`). With $r_p = r_1$ and $r_a = r_2$, the semi-major axis is half the major axis:

:::{math}
:label: eq-p22-transfer-a
a_t = \frac{r_1 + r_2}{2}
:::

The {term}`eccentricity` of the transfer orbit follows from $r_p = a_t(1-e_t)$ and $r_a = a_t(1+e_t)$. Their difference is $2a_te_t$ and their sum is $2a_t$, so

:::{math}
:label: eq-p22-transfer-e
e_t = \frac{r_2 - r_1}{r_2 + r_1}
:::

**First burn.** Before the burn the spacecraft moves at the circular speed $v_{c1} = \sqrt{\mu/r_1}$. After it, the spacecraft must move at the periapsis speed of the transfer orbit, which the vis-viva equation gives with $r = r_1$ and $a = a_t$:

:::{math}
:label: eq-p22-dv1
\begin{aligned}
\Delta V_1 &= v_{t,p} - v_{c1}\\
&= \sqrt{\mu\left(\frac{2}{r_1} - \frac{1}{a_t}\right)} - \sqrt{\frac{\mu}{r_1}}
\end{aligned}
:::

**Second burn.** Half an orbit later the spacecraft reaches the apoapsis of the transfer orbit at $r_2$, moving at $v_{t,a}$. It must leave at the circular speed $v_{c2}$ of the final orbit:

:::{math}
:label: eq-p22-dv2
\Delta V_2 = v_{c2} - v_{t,a} = \sqrt{\frac{\mu}{r_2}} - \sqrt{\mu\left(\frac{2}{r_2} - \frac{1}{a_t}\right)}
:::

**Total and time of flight.** The total $\Delta V$ of the transfer is the sum of the two magnitudes. The trip covers half of the transfer ellipse, so the time of flight $t_f$ is half the transfer {term}`orbital period`:

:::{math}
:label: eq-p22-total
\Delta V_{\text{total}} = |\Delta V_1| + |\Delta V_2|, \qquad t_f = \frac{T_t}{2} = \pi\sqrt{\frac{a_t^3}{\mu}}
:::

Both burns speed the spacecraft up, and yet it ends in the larger circle moving slower than it did in the smaller one. It enters the transfer orbit at its fastest point and leaves at its slowest. Between the two burns it climbs and converts kinetic energy into potential energy, slowing all the way from periapsis to apoapsis by conservation of energy.

Both burns are tangential. At periapsis and apoapsis the velocity is perpendicular to the radius, as it is on a circle. Then the transfer ellipse touches each circle, and the old and new velocities point the same way. All of the burn goes into speed and none into turning the velocity. A burn that turns the velocity requires extra $\Delta V$, as the plane change below shows.

To go down, from a large circle to a small one, we fly the same ellipse the other way. The first burn is at the apoapsis of the transfer orbit and the second at its periapsis. Both burns point against the motion, and their magnitudes are the same as for the trip up.

:::{tip} Method: a Hohmann transfer
1. Turn altitudes into radii using $r = R + h$.
2. Compute $a_t = (r_1 + r_2)/2$.
3. Compute the four speeds, finding $v_{c1}$ and $v_{c2}$ from $\sqrt{\mu/r}$, and $v_{t,p}$ and $v_{t,a}$ from the vis-viva equation with $a = a_t$.
4. Take $\Delta V_1$ and $\Delta V_2$ at the two ends and add their magnitudes.
5. Compute the time of flight, $\pi\sqrt{a_t^3/\mu}$.
6. Sketch the orbits and check that, when going up, both burns point along the motion and the final circular speed is lower than the initial one.
:::

:::{warning} Altitude is not radius
Every equation on this page uses the distance from the center of the body. An altitude of 400 km above Earth is a radius of 6,778 km. If you put 400 km into $\sqrt{\mu/r}$, you get 31.6 km/s, a speed no Earth orbit has.
:::

## Worked example: a Hohmann transfer

A satellite is in a circular orbit 400 km above Earth. It must move to a circular orbit 20,200 km up, close to the altitude of the GPS satellites. Find each burn, the total $\Delta V$, and the time of flight. Use $\mu = 3.986 \times {10}^{5}\ \text{km}^3/\text{s}^2$ and $R = 6{,}378\ \text{km}$.

1. **Radii.** $r_1 = 6{,}378 + 400 = 6{,}778\ \text{km}$ and $r_2 = 6{,}378 + 20{,}200 = 26{,}578\ \text{km}$.
2. **Transfer orbit.** $a_t = (6{,}778 + 26{,}578)/2 = 33{,}356/2 = 16{,}678\ \text{km}$, and $e_t = (26{,}578 - 6{,}778)/33{,}356 = 0.5936$.
3. **Speeds at the first burn.**
   $$
   \begin{aligned}
   v_{c1} &= \sqrt{\frac{3.986 \times {10}^{5}}{6{,}778}}\\
          &= 7.669\ \text{km/s}
   \end{aligned}
   $$

   $$
   \begin{aligned}
   v_{t,p} &= \sqrt{3.986 \times {10}^{5}\left(\frac{2}{6{,}778} - \frac{1}{16{,}678}\right)}\\
           &= 9.681\ \text{km/s}
   \end{aligned}
   $$

   so $\Delta V_1 = 9.681 - 7.669 = 2.012\ \text{km/s}$, along the motion.
4. **Speeds at the second burn.**
   $$
   \begin{aligned}
   v_{t,a} &= \sqrt{3.986 \times {10}^{5}}\\
           &\;\;\; \times \sqrt{\frac{2}{26{,}578} - \frac{1}{16{,}678}}\\
           &= 2.469\ \text{km/s}
   \end{aligned}
   $$

   $$
   \begin{aligned}
   v_{c2} &= \sqrt{\frac{3.986 \times {10}^{5}}{26{,}578}}\\
          &= 3.873\ \text{km/s}
   \end{aligned}
   $$

   so $\Delta V_2 = 3.873 - 2.469 = 1.404\ \text{km/s}$, along the motion.
5. **Total.** $\Delta V_{\text{total}} = 2.012 + 1.404 = 3.416\ \text{km/s}$.
6. **Time of flight.** The transfer period is $T_t = 2\pi\sqrt{{16{,}678}^3/(3.986 \times {10}^{5})} = 21{,}435\ \text{s}$, so the trip takes $10{,}718\ \text{s}$, or 178.6 minutes (2.977 hours).

**Check.** The spacecraft is fastest just after the first burn and slowest just before the second, and it ends at 3.873 km/s, slower than the 7.669 km/s it started with. You can follow the whole speed history in {numref}`fig-p22-hohmann-speeds`, and {numref}`tbl-p22-hohmann` collects the results.

:::{table} Results of the worked example: Hohmann transfer around Earth from 400 km to 20,200 km altitude.
:label: tbl-p22-hohmann
:align: center

| Quantity | Symbol | Value |
| --- | :---: | ---: |
| Speed in the initial orbit | $v_{c1}$ | 7.669 km/s |
| Speed at the perigee of the transfer orbit | $v_{t,p}$ | 9.681 km/s |
| First burn, along the motion | $\Delta V_1$ | 2.012 km/s |
| Speed at the apogee of the transfer orbit | $v_{t,a}$ | 2.469 km/s |
| Speed in the final orbit | $v_{c2}$ | 3.873 km/s |
| Second burn, along the motion | $\Delta V_2$ | 1.404 km/s |
| Total | $\Delta V_{\text{total}}$ | 3.416 km/s |
| Time of flight | $T_t/2$ | 10,718 s |

:::

:::{figure} figures/p22-hohmann-speeds.svg
:label: fig-p22-hohmann-speeds
:alt: Plot of speed in kilometers per second against time in hours, from before the first burn to after the second. The speed holds at 7.669 kilometers per second in the initial orbit, jumps up by 2.012 kilometers per second at time zero to 9.681 kilometers per second, then falls steadily along the transfer orbit to 2.469 kilometers per second at 2.977 hours. There it jumps up by 1.404 kilometers per second to 3.873 kilometers per second and stays constant in the final orbit.
:width: 85%

Computed: speed against time through the Hohmann transfer of the worked example (time along the orbit from Kepler's equation, Curtis 2014, Chapter 3). Both burns raise the speed, yet the speed in the final orbit is lower than in the initial orbit, because the spacecraft slows all the way along the transfer orbit.
:::

## Circularizing an elliptical orbit

A single tangential burn at an apsis makes an elliptical orbit circular. At periapsis and at apoapsis the velocity is perpendicular to the radius, as on a circle, so only the speed has to change. A {term}`circularization burn` at apoapsis speeds the spacecraft up to the circular speed at $r_a$ and gives the large circle. A burn at periapsis slows it down to the circular speed at $r_p$ and gives the small circle ({numref}`fig-p22-circularize`). Each is half of a Hohmann transfer. Anywhere else on the ellipse the velocity is not perpendicular to the radius, so one tangential burn cannot make the orbit circular.

:::{figure} figures/p22-circularize.svg
:label: fig-p22-circularize
:alt: Earth to scale inside an elliptical orbit with its periapsis on the right and its apoapsis on the left. Two dash-dot circles, both final orbits, touch the ellipse: the circle at r a passes through the apoapsis and encloses the ellipse, and the circle at r p passes through the periapsis inside it. At the apoapsis a burn arrow labeled speed up points along the motion; at the periapsis a slightly longer burn arrow labeled slow down points against the motion.
:width: 65%

Computed to scale: the two circles a single burn can reach from an orbit of 1,000 km by 12,000 km altitude around Earth, an orbit more eccentric than the example below so that the circles stand apart. Speeding up at apoapsis gives the circle of radius $r_a$; slowing down at periapsis gives the circle of radius $r_p$. The burn arrows are drawn to scale with their $\Delta V$.
:::

**Example.** A satellite is in a 350 km by 1,100 km orbit around Earth. Find the $\Delta V$ required to circularize the orbit at apogee and at perigee. Because each burn is the difference of two close speeds, we carry the speeds to five decimals. The orbit has $r_p = 6{,}728$ km, $r_a = 7{,}478$ km, $a = 7{,}103$ km, and $e = 0.05279$.

- *Circular at 1,100 km.* At apogee the satellite moves at $v_a = \sqrt{\mu(2/r_a - 1/a)} = 7.10555$ km/s. The circle there needs $\sqrt{\mu/r_a} = 7.30089$ km/s. The burn is $\Delta V = 7.30089 - 7.10555 = 0.1953$ km/s, or 195.3 m/s, along the motion.
- *Circular at 350 km.* At perigee the satellite moves at $v_p = 7.89764$ km/s and the circle needs $7.69707$ km/s. The burn is $\Delta V = 7.69707 - 7.89764 = -0.2006$ km/s, or 200.6 m/s against the motion.

:::{warning} The sign tells the direction
A negative $\Delta V$ from "target speed minus current speed" means a burn against the motion, with the engine pointing forward. The propellant needed depends on the magnitude only, so a slowing burn of 0.2006 km/s uses the same propellant as a speeding burn of 0.2006 km/s.
:::

## Catching up: the phasing orbit

Two spacecraft in the same circular orbit move at the same speed, so the chaser behind never gains on the target ahead unless it changes its orbital period for one lap. Speeding up raises the orbit and lengthens the period, causing the chaser to fall further behind. Instead, the chaser slows down to drop into a slightly smaller ellipse, called a {term}`phasing orbit`, which has a shorter period. The chaser completes that smaller orbit in less time than the target takes around the circle and arrives back at the burn point just as the target passes through it ({numref}`fig-p22-phasing`).

**Example.** A chaser and a target share a circular Earth orbit of radius 7,000 km. The chaser crosses each point 100 s after the target. Plan the catch-up.

1. **Speed in the circle.** $v = \sqrt{3.986 \times {10}^{5}/7{,}000} = 7.54605\ \text{km/s}$, to five decimals, because the burn below is a difference of close speeds.
2. **Period of the circle.** $T = 2\pi\sqrt{{7{,}000}^3/(3.986 \times {10}^{5})} = 5{,}828.5\ \text{s}$ (97.14 minutes). The 100 s lag puts the target 6.18° ahead along the orbit.
3. **Period of the phasing orbit.** The chaser must complete one lap 100 s sooner than the target, so $T_{\text{ph}} = 5{,}828.5 - 100 = 5{,}728.5\ \text{s}$ (95.48 minutes).
4. **Its semi-major axis.** From the period equation,
   $$
   \begin{aligned}
   a_{\text{ph}} &= \left[\mu\left(\frac{T_{\text{ph}}}{2\pi}\right)^2\right]^{1/3}\\
                 &= 6{,}919.7\ \text{km}
   \end{aligned}
   $$
5. **Its perigee, and the clearance.** The burn point keeps the radius of the circle, 7,000 km, and the velocity there stays perpendicular to the radius. That makes the burn point the apogee of the phasing orbit. The perigee radius is $r_p = 2a_{\text{ph}} - r_a = 2(6{,}919.7) - 7{,}000 = 6{,}839.4$ km, and the eccentricity is $0.0116$. The perigee lies $6{,}839.4 - 6{,}378 = 461.4$ km above the surface, so the chaser stays clear of Earth.
6. **Speed needed at apogee.**

   $$
   \begin{aligned}
   v_a &= \sqrt{3.986 \times {10}^{5}}\\
       &\;\;\; \times \sqrt{\frac{2}{7{,}000} - \frac{1}{6{,}919.7}}\\
       &= 7.50214\ \text{km/s}
   \end{aligned}
   $$

7. **The burn.** $\Delta V = v_a - v = 7.50214 - 7.54605 = -0.04391\ \text{km/s} = -43.91\ \text{m/s}$. The negative sign means a burn against the motion, so the chaser slows down to catch up.
8. **The second burn.** After one lap of 5,728.5 s the chaser is back at the burn point, beside the target. A burn of 43.91 m/s along the motion restores the circle. The catch-up requires 87.82 m/s in all.

:::{figure} figures/p22-phasing.svg
:label: fig-p22-phasing
:alt: Right, Earth to scale inside the 7,000 kilometer circular orbit, with the chaser, a filled dot on the right of the orbit, 6.18 degrees behind the target, an open dot. A burn arrow at the chaser points against the motion, and the dashed phasing orbit almost coincides with the circle: it touches it at the chaser and runs slightly inside it elsewhere. Left, joined to a small box at the perigee by two thin lines, a detail to scale: one dimension shows that the phasing orbit passes 161 kilometers inside the circle, and another, drawn through the perigee, that the perigee lies 461.4 kilometers above Earth's surface.
:width: 80%

Computed for the phasing example, to scale. Right, the whole orbit: the chaser slows down at the burn point and enters a phasing orbit that is barely smaller than the circle. Left, a detail of the region near perigee marked by the box, at a larger scale: the perigee lies 461.4 km above the surface.
:::

The phasing orbit differs only slightly from the circle. Perigee drops by just 161 km, and each burn is less than 1% of the orbital speed. A larger lag requires a lower perigee, and in a single lap any lag greater than 384 s (about 6.4 minutes) would drop perigee below Earth's surface. Even a moderately lower perigee than in the example would enter the upper atmosphere, so we spread a larger lag over multiple revolutions. Over $k$ laps of the phasing orbit, its period is $T - \text{lag}/k$, keeping the orbit closer to the original circle.

:::{warning} Carry enough digits
The burn is the difference of two speeds that share their first two figures. If you round the two speeds to four significant figures, you get $-0.044$ km/s, and only two figures of the answer survive. Keep five or six figures in the period, the semi-major axis, and both speeds, and round only the final answer. Watch your units too, using periods in seconds with $\mu$ in km³/s², never minutes.
:::

(p22-plane-change)=
## Changing the orbit plane

Because velocity is a vector, an engine burn can change its direction as well as its magnitude. A pure {term}`plane change` keeps the speed constant and turns the velocity vector by the angle $\Delta i$ between the initial and final orbit planes. This burn can be performed only at a point that lies in both planes, along the {term}`line of nodes` where the two planes intersect ({numref}`fig-p22-plane-change`).

:::{figure} figures/p22-plane-change.svg
:label: fig-p22-plane-change
:alt: Left, a globe with two circular orbits of the same radius, an initial orbit in the equatorial plane and a final orbit tilted from it. The two orbits cross at two points on a line through Earth's center, the line of nodes, and a dot marks the burn at the near crossing. Right, the velocity triangle of the burn: two arrows of equal length v, labeled v 1 and v 2, start from one point with the angle delta-i between them, and a third arrow, delta-V, joins the tip of v 1 to the tip of v 2.
:width: 80%

Schematic of a plane change between two circular orbits of the same radius whose planes differ by $\Delta i$ (here 30°, with the initial orbit in the equatorial plane). Left, the burn is made where the orbits cross, on the line of nodes. Right, the velocity triangle at the burn: the speed stays the same, and $\Delta\mathbf{V}$ joins the tips of the two velocity vectors.
:::

The angular momentum per unit mass, $\mathbf{r} \times \mathbf{v}$, is perpendicular to the orbit plane, so turning the plane means turning this vector. On the line of nodes the position $\mathbf{r}$ lies in both planes. The burn turns $\mathbf{v}$ about $\mathbf{r}$ without changing its length, so the magnitude of $\mathbf{r} \times \mathbf{v}$ stays the same. The orbit keeps its size and its shape and only tilts.

We find the required $\Delta V$ from the triangle on the right of {numref}`fig-p22-plane-change`. Its two equal sides are the old and the new velocity, of length $v$, with the angle $\Delta i$ between them. The line from their common start to the midpoint of $\Delta\mathbf{V}$ bisects the angle and is perpendicular to $\Delta\mathbf{V}$. Each half of the triangle is then a right triangle with hypotenuse $v$, and the side opposite the angle $\Delta i/2$ is $\Delta V/2$. So $\Delta V/2 = v\sin(\Delta i/2)$, giving

:::{math}
:label: eq-p22-plane-change
\Delta V = 2\,v\,\sin\frac{\Delta i}{2}
:::

For a small angle, $\sin x \approx x$ gives $\Delta V \approx v\,\Delta i$, with $\Delta i$ in radians. At 8 km/s, a change of only 1° already requires 0.1396 km/s.

Because the speed $v$ in [](#eq-p22-plane-change) is the full orbital speed, plane changes require large amounts of $\Delta V$. In low Earth orbit at 8 km/s, a 30° change requires 4.141 km/s, more than the entire Hohmann transfer in the worked example. A 60° change requires 8 km/s, equal to the orbital speed itself, because the velocity triangle is then equilateral. {numref}`fig-p22-plane-change-cost` plots the required $\Delta V$ across all angles. This large $\Delta V$ requirement is why we launch a spacecraft directly into its target inclination whenever the launch site allows it; [launch to orbit](#p23-azimuth) shows which inclinations a site can reach directly.

:::{figure} figures/p22-plane-change-cost.svg
:label: fig-p22-plane-change-cost
:alt: Plot of delta-V in kilometers per second against the plane change angle from 0 to 180 degrees. The solid curve for a speed of 8.0 kilometers per second rises almost linearly at first, passes 8 kilometers per second at 60 degrees, where a dot marks delta-V equal to v, and levels off at 16 kilometers per second at 180 degrees. The dashed curve for 3.873 kilometers per second has the same shape at half the height and ends at 7.746 kilometers per second.
:width: 75%

Computed from $2v\sin(\Delta i/2)$: the $\Delta V$ required for a plane change at 8.0 km/s (low Earth orbit) and at 3.873 km/s (the final orbit of the worked example). At 60° the required $\Delta V$ equals the orbital speed; at 180° it is twice the speed.
:::

:::{warning} The speed where the burn is made
Use the speed of the spacecraft at the point of the burn, not the speed of some other part of the trip. Use $\sin(\Delta i/2)$ with the angle in degrees on your calculator, or the small-angle form with the angle in radians. If you use $v\,\Delta i$ with $\Delta i$ in degrees, your $\Delta V$ comes out 57.3 times too large.
:::

## Choosing the order of maneuvers

Now we put the pieces together. Because the $\Delta V$ for a plane change is proportional to the speed, the plane change belongs where the spacecraft is slowest. On a Hohmann transfer upward, the slowest point of the whole trip is the apogee of the transfer orbit, just before the second burn.

**Example.** The satellite of the worked example must also turn its orbit plane by 30°. Compare three plans, each with the two Hohmann burns (3.416 km/s) and a separate plane change, with $\sin 15° = 0.25882$:

- *In the low orbit, before the transfer:* $2(7.669)(0.25882) = 3.970$ km/s; total 7.386 km/s.
- *At the apogee of the transfer orbit, before the second burn:* $2(2.469)(0.25882) = 1.278$ km/s; total 4.694 km/s.
- *In the high orbit, after the transfer:* $2(3.873)(0.25882) = 2.005$ km/s; total 5.421 km/s.

:::{figure} figures/p22-maneuver-order.svg
:label: fig-p22-maneuver-order
:alt: Horizontal stacked bar chart of total delta-V for three plans. Each bar starts with the same Hohmann part of 3.416 kilometers per second, hatched one way, followed by a plane change part hatched the other way. The plane change in the low orbit gives the longest bar, 7.386 kilometers per second; at the transfer apogee the shortest, 4.694 kilometers per second; in the high orbit 5.421 kilometers per second.
:width: 85%

Computed for the worked example with a 30° plane change: the total $\Delta V$ of the three plans. The plane change requires the least $\Delta V$ at the apogee of the transfer orbit, where the spacecraft is slowest. The Hohmann burns are the same in each plan; only the speed at the plane change differs.
:::

Performing the plane change at the apogee of the transfer orbit saves 2.692 km/s compared with turning in the low orbit, because the spacecraft moves at 2.469 km/s there instead of 7.669 km/s. This sequence works only if the apogee of the transfer orbit lies on the line of nodes, which we can arrange by coasting in the parking orbit until the right moment for the first burn. For a transfer downward, the order reverses, because the slowest point occurs just after the first burn at the high apogee of the transfer orbit. Combining the plane change and the second Hohmann burn into a single angled burn requires even less $\Delta V$, because by the triangle inequality one combined vector change is shorter than the sum of two separate legs; we leave combined maneuvers to a later course.

## Summary

:::{important} Summary
- A burn changes the velocity at a point; the new orbit passes through that point, and the vis-viva equation gives the speed it needs there.
- The Hohmann transfer between circular orbits uses two tangential burns at the ends of a transfer ellipse with $a_t = (r_1 + r_2)/2$; it takes half the transfer period.
- One burn at an apsis makes an orbit circular. A slowing burn puts a chaser on a smaller, faster phasing orbit.
- A plane change requires $2v\sin(\Delta i/2)$. It is made on the line of nodes, at the slowest point of the trip that lies there.
:::

:::{table} The equations of this page.
:label: tbl-p22-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Semi-major axis of the transfer orbit | $a_t = (r_1 + r_2)/2$ |
| Eccentricity of the transfer orbit | $e_t = (r_2 - r_1)/(r_2 + r_1)$ |
| First burn | $\Delta V_1 = \sqrt{\mu(2/r_1 - 1/a_t)} - \sqrt{\mu/r_1}$ |
| Second burn | $\Delta V_2 = \sqrt{\mu/r_2} - \sqrt{\mu(2/r_2 - 1/a_t)}$ |
| Time of flight | $t_f = \pi\sqrt{a_t^3/\mu}$ |
| Circularization at an apsis | $\Delta V = \sqrt{\mu/r} - \sqrt{\mu(2/r - 1/a)}$ |
| Phasing orbit (chaser behind by lag, $k$ laps) | $T_{\text{ph}} = T - \text{lag}/k$, $a_{\text{ph}} = [\mu (T_{\text{ph}}/2\pi)^2]^{1/3}$ |
| Plane change | $\Delta V = 2v\sin(\Delta i/2)$ |

:::

:::{exercise} For discussion
:label: ex-p22-discussion

1. Both burns of a Hohmann transfer upward speed the spacecraft up, yet it ends slower than it started. Where did the speed go?
2. A chaser is 100 s ahead of its target in the same circular orbit and must let the target catch up. Which way should it burn, and what happens to its perigee or apogee?
3. Why must a plane change be made on the line of nodes? What would a burn of the same size do elsewhere on the orbit?
4. A spacecraft must lower its orbit and change its plane. In which order should it make the burns, and why?
5. A third burn can require less total $\Delta V$ than a Hohmann transfer when the outer orbit is much larger than the inner one. Where would that third burn be made?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-2-2.html
:label: quiz-2-2
:enumerated: false
:width: 100%

Quiz for Standard 2.2: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 8.
- Bate, R. R., Mueller, D. D., and White, J. E., *Fundamentals of Astrodynamics*, Dover, 1971. Chapter 3.
- Curtis, H. D., *Orbital Mechanics for Engineering Students*, 3rd ed., Butterworth-Heinemann, 2014. Chapter 3 (orbital position as a function of time, Kepler's equation) and Chapter 6 (the Hohmann transfer, phasing, and plane changes, with more worked examples).
- Hohmann, W., *Die Erreichbarkeit der Himmelskörper*, R. Oldenbourg, Munich, 1925. English translation: *The Attainability of Heavenly Bodies*, NASA Technical Translation F-44, 1960.
- Vallado, D. A., *Fundamentals of Astrodynamics and Applications*, 4th ed., Microcosm Press, 2013. Chapter 6.

