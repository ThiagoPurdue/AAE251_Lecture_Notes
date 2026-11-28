---
title: "Constraint diagram and field length"
short_title: Constraint diagram and field length
---

On pages 5.1 to 5.3, the wing and engines were already fixed, and we evaluated the resulting flight performance. In conceptual design, we work in reverse: starting from customer requirements for {term}`stall speed`, runway length, climb rate, cruise speed, and ceiling, we choose the smallest wing and engines that can satisfy every requirement together. As introduced on [page 3.4](#p34-three-numbers), we capture that sizing trade-off using two parameters, {term}`wing loading` $W/S$ and {term}`thrust-to-weight ratio` $T/W$ (writing aircraft weight as $W = mg$ throughout this page). We first estimate takeoff and landing ground rolls, and then we plot all performance constraints on a single diagram to select a feasible design point. No course standard is assessed on this page.

:::{note} What to take from this page
- On the runway the aircraft speeds up against drag and wheel friction, and it stops by braking. With the simplest assumptions, both ground rolls grow in proportion to the wing loading $W/S$.
- More thrust shortens the takeoff roll. It does not change the landing roll, so a landing requirement caps the wing loading directly.
- Each requirement becomes one line on a plot of $T/W$ against $W/S$. The designs that meet every requirement lie above every line and to the left of every vertical one.
- The design point uses the highest wing loading the limits allow and the lowest thrust-to-weight ratio above every line there, which gives the smallest wing and the smallest engines for that wing.
:::

(p55-field-length)=
## Takeoff and landing ground roll

Two of the requirements are lengths on the ground, so we start with the runway. A takeoff or a landing has two parts ({numref}`fig-p55-takeoff-landing-phases`). The {term}`ground roll` is the distance the aircraft runs on its wheels. The air distance is the flight between the runway and a set height above it. For a transport airplane, the U.S. rules measure the takeoff distance up to a height of 35 ft (10.7 m). They measure the landing distance down from a height of 50 ft (15 m) (14 CFR 25.113 and 25.125). Early sizing looks only at the ground rolls. They follow from simple physics, while the air distance needs the whole flight path through the pitch-up before liftoff and the climb.

:::{figure} figures/p55-takeoff-landing-phases.svg
:label: fig-p55-takeoff-landing-phases
:alt: Two side views over a hatched runway. Panel 1, takeoff: an aircraft outline at brake release, at speed zero; a thick path with an arrowhead along the runway to a second outline at liftoff, at 1.2 times the stall speed; then the path curves up to a third outline above a post labeled obstacle, 35 feet or 10.7 meters. Dimensions mark the ground roll, s sub L O, from brake release to liftoff, and the air distance from liftoff to the obstacle. Panel 2, landing: a path with arrowheads descends past a post labeled obstacle, 50 feet or 15 meters, to touchdown at 1.3 times the stall speed, then runs along the runway, with an arrowhead, to an outline at the stop. Dimensions mark the air distance and the ground roll, s sub L.
:width: 90%

Schematic, not to scale. The heights, the path angles, and the aircraft are drawn many times larger than the distances along the runway. Each maneuver is a ground roll plus an air distance over an obstacle, and early sizing looks at the ground roll. The obstacle heights are those of the U.S. rules for a transport airplane (14 CFR 25.113 and 25.125).
:::

### The forces during the roll

A distance follows from the acceleration, and the acceleration from the forces ({numref}`fig-p55-ground-roll-forces`). The thrust $T$ pushes the aircraft forward. The drag $D$ pulls it back. As the speed grows, the wing makes some lift $L$ and carries part of the weight. The wheels carry the rest, the **wheel load** $W - L$. The runway pushes back on the tires with a friction force $\mu_r(W - L)$, where $\mu_r$ is the friction coefficient between the tires and the runway. It is small while the wheels roll freely, and much larger when the pilot brakes. Newton's second law along the runway gives

:::{math}
:label: eq-p55-roll
m\,\frac{dV}{dt} = T - D - \mu_r\,(W - L)
:::

:::{figure} figures/p55-ground-roll-forces.svg
:label: fig-p55-ground-roll-forces
:alt: Two free-body diagrams of a Boeing 737-800 side outline on its wheels, nose to the right, each with a velocity arrow pointing forward. Panel 1, takeoff roll, where the net force points forward: lift up and weight down from the center of gravity, drag pointing back behind the tail, thrust pointing forward ahead of the nose, and at the main wheels a wheel load, W minus L, pointing up and a short arrow, rolling friction, small, pointing back. Panel 2, landing roll with the engines at idle and the spoilers up, where the net force points backward: a short lift arrow, the weight, the drag, a longer wheel load, and a long braking friction arrow, mu sub r times W minus L, pointing back. There is no thrust arrow. A key shows the force and velocity arrows.
:width: 85%

Schematic, drawn on the outline of a Boeing 737-800. On takeoff the thrust speeds the aircraft up against the drag and against the friction on the weight the wing does not yet carry. On landing the brakes act through that same wheel load. The arrow lengths are not to scale, except that the lift and the wheel load add up to the weight; the loads on all the wheels are drawn together at the main wheels.
:::

### Takeoff ground roll

The simplest model takes the thrust of a jet to be much larger than the drag and the rolling friction together. If we neglect those two, [](#eq-p55-roll) gives a constant acceleration:

$$
\begin{aligned}
a &= \frac{T}{m}\\
  &= g\,\frac{T}{W}
\end{aligned}
$$

From rest, with a constant acceleration, the speed is $V = a\,t$ and the distance is $s = \tfrac12 a\,t^2$. Taking $t = V/a$ from the first and putting it in the second gives $s = V^2/(2a)$. The aircraft lifts off at $V_\text{LO} = 1.2\,V_\text{stall}$, a margin above the stall, as Anderson (2016, Chapter 6) takes it. The stall speed with takeoff flaps comes from [page 3.4](#p34-stall), $V_\text{stall}^2 = 2(W/S)/(\rho\,C_{L,\max,\text{TO}})$. So

$$
\begin{aligned}
s_\text{LO} &= \frac{V_\text{LO}^2}{2a}\\
            &= \frac{1.44\,V_\text{stall}^2}{2g\,(T/W)}\\
            &= \frac{1.44\,(W/S)}{\rho\,g\,C_{L,\max,\text{TO}}\,(T/W)}
\end{aligned}
$$

The factor 1.44 is ${1.2}^{2}$. Multiplied out, the same result reads $s_\text{LO} = 1.44\,W^2/(g\,\rho\,S\,C_{L,\max,\text{TO}}\,T)$.

### Landing ground roll

The aircraft touches down at $V_T = 1.3\,V_\text{stall}$, with the stall speed for the landing flaps, again as Anderson (2016, Chapter 6) takes it. The rules set a similar margin on the approach. A transport airplane must fly at least 1.23 times its reference stall speed down to 50 ft (14 CFR 25.125), and it touches down a little slower. After touchdown the pilot brings the engines to idle and raises the {term}`spoiler` panels on top of the wing. The spoilers dump the lift, so almost the whole weight rests on the wheels and the brakes can use it. With $T = 0$ and $L = 0$, and with the drag neglected, [](#eq-p55-roll) becomes $m\,dV/dt = -\mu_r W$, a constant deceleration $a = g\,\mu_r$. The aircraft slows from $V_T$ to rest in

$$
\begin{aligned}
s_L &= \frac{V_T^2}{2g\,\mu_r}\\
    &= \frac{1.69\,V_\text{stall}^2}{2g\,\mu_r}\\
    &= \frac{1.69\,(W/S)}{\rho\,g\,C_{L,\max,L}\,\mu_r}
\end{aligned}
$$

where $1.69 = {1.3}^{2}$ and $C_{L,\max,L}$ is the {term}`maximum lift coefficient` with landing flaps. Here $\mu_r$ is the braking friction, much larger than the rolling friction of the takeoff.

::::{prf:definition} Takeoff and landing ground rolls
:label: def-p55-field-length
With the thrust much larger than the drag and the rolling friction on takeoff, and with no lift, no thrust, and no drag on landing:
:::{math}
:label: eq-p55-field-length
\begin{aligned}
s_\text{LO} &= \frac{1.44\,(W/S)}{\rho\,g\,C_{L,\max,\text{TO}}\,(T/W)}\\
s_L &= \frac{1.69\,(W/S)}{\rho\,g\,C_{L,\max,L}\,\mu_r}
\end{aligned}
:::
::::

Three things follow from [](#eq-p55-field-length):

- Both rolls grow in proportion to $W/S$. A small wing needs a fast liftoff and a fast touchdown, and the distance grows with the square of the speed. {term}`Flap` settings that raise $C_{L,\max}$ shorten both.
- The takeoff roll falls as $1/(T/W)$. Larger engines speed the aircraft up faster.
- The landing roll does not depend on the thrust at all. Only the wing can meet a landing requirement, so it caps $W/S$ directly.

Both rolls also grow as the density falls, so a hot day or a high airport requires a longer runway.

:::{warning} What the simple forms leave out
On takeoff, [](#eq-p55-field-length) leaves out the drag and the rolling friction, so the real roll is longer than the equation gives. On landing it leaves out the drag and any reverse thrust, which would both shorten the roll, but it assumes full braking from the moment of touchdown. The braking friction also falls on a runway covered with water or slush, and it falls further as the speed rises (Horne and Leland 1962). If you use a dry-runway $\mu_r$ for a wet runway, your landing roll comes out too short. Anderson (2016, Chapter 6) gives fuller forms that keep the drag and the friction.
:::

(p55-constraint-curves)=
## Building the constraint diagram

The two ground rolls turned two requirements into limits on $W/S$ and $T/W$. Every other requirement can be written the same way, and then all of them fit on one chart. A **{term}`constraint diagram`** plots the thrust-to-weight ratio $T/W$ against the wing loading $W/S$, with one line for each requirement (Raymer 2018, Chapter 5). Here $T$ is the sea-level static thrust of all the engines together, and $W$ is the takeoff weight.

We use the takeoff weight for every requirement. It is the simplest choice, and it errs on the safe side for the landing, the cruise, and the ceiling, which come after some fuel has burned. Two facts from [page 5.1](#p51-available-and-vmax) carry the thrust to other conditions. A jet's thrust changes little with speed, so we take the static thrust at every speed. At altitude the thrust falls with the density as $T_A = T\,(\rho/\rho_0)^{m_\text{ad}}$, and the factor $(\rho/\rho_0)^{m_\text{ad}}$ is the thrust lapse.

{numref}`fig-p55-constraint-build` builds the diagram one requirement at a time, numbered as in the list below.

1. **Stall speed** with landing flaps at sea level. [Page 3.4](#p34-stall) gave the largest wing loading for a stall speed:
   $$
   \frac{W}{S} \le \tfrac12\,\rho_0\,V_\text{stall}^2\,C_{L,\max,L}
   $$
   It does not involve the thrust, so it is a vertical line. Designs to its left meet it.
2. **Landing ground roll** at sea level. We solve the second line of [](#eq-p55-field-length) for $W/S$:
   $$
   \frac{W}{S} \le \frac{\rho_0\,g\,C_{L,\max,L}\,\mu_r\,s_L}{1.69}
   $$
   This is a second vertical line. The smaller of the two wing loadings is the real limit.
3. **Takeoff ground roll** at sea level. We solve the first line of [](#eq-p55-field-length) for $T/W$:
   $$
   \frac{T}{W} \ge \frac{1.44\,(W/S)}{\rho_0\,g\,C_{L,\max,\text{TO}}\,s_\text{LO}}
   $$
   This is a straight line through the origin. More wing loading means a faster liftoff, so it needs proportionally more thrust for the same runway.
4. **Rate of climb** $R/C$ at a speed $V$ at sea level. [Page 5.3](#p53-excess) gives the climb angle from the excess thrust, $\sin\gamma = (T - D)/W$, and the {term}`rate of climb` as $R/C = V\sin\gamma$. So $T/W = (R/C)/V + D/W$. For the drag we take $L = W$, which applies to the shallow climbs of this chart, so $C_L = W/(qS)$ with $q = \tfrac12 \rho V^2$:
   $$
   \begin{aligned}
   D &= q\,S\,C_{D,0} + q\,S\,K\,C_L^2\\
     &= q\,S\,C_{D,0} + \frac{K\,W^2}{q\,S}\\
   \frac{D}{W} &= \frac{q\,C_{D,0}}{W/S} + \frac{K\,(W/S)}{q}
   \end{aligned}
   $$
   which gives the line
   $$
   \begin{aligned}
   \frac{T}{W} &\ge \frac{R/C}{V} + \frac{q\,C_{D,0}}{W/S}\\
   &\;\;\; + \frac{K\,(W/S)}{q}
   \end{aligned}
   $$
   The parasite drag term falls as $W/S$ grows and the induced drag term rises, so the line sags in the middle.
5. **Cruise** at a speed $V$ at an altitude where the density is $\rho$. The engines at full throttle must maintain this speed, so the full thrust at that altitude equals the drag, $T\,(\rho/\rho_0)^{m_\text{ad}} = D$. We divide by $W$ and by the lapse:
   $$
   \begin{aligned}
   \frac{T}{W} &\ge \frac{1}{(\rho/\rho_0)^{m_\text{ad}}}\times\\
   &\;\;\; \left[\frac{q\,C_{D,0}}{W/S} + \frac{K\,(W/S)}{q}\right]
   \end{aligned}
   $$
   with $q = \tfrac12 \rho V^2$ at the cruise altitude.
6. **Service ceiling**. At the {term}`service ceiling` the rate of climb is still 0.5 m/s ([page 5.3](#p53-ceilings)). Near its ceiling a jet climbs best close to its minimum-thrust speed, and we take the climb line at that speed. There $D/W = 1/(L/D)_{\max} = 2\sqrt{K\,C_{D,0}}$, and the speed is $V = \sqrt{2(W/S)/\rho}\,(K/C_{D,0})^{1/4}$ ([page 3.3](#p33-minimum-drag)). With the lapse at the ceiling density:
   $$
   \begin{aligned}
   \frac{T}{W} &\ge \frac{1}{(\rho/\rho_0)^{m_\text{ad}}}\times\\
   &\;\;\; \left(2\sqrt{K\,C_{D,0}} + \frac{0.5}{V}\right)
   \end{aligned}
   $$

:::{figure} figures/p55-constraint-build.svg
:label: fig-p55-constraint-build
:alt: Six small plots of thrust-to-weight ratio from 0 to 0.45 against wing loading from 1,000 to 5,000 newtons per square meter, in two rows, titled 1 stall speed, 2 landing roll, 3 takeoff roll, 4 climb, 5 cruise, and 6 ceiling. Each adds one line in its own style, earlier lines stay thin and gray, the part the new line removes is hatched gray, and what is left is shaded light gold. The stall line removes everything right of it. The landing line, farther right, removes nothing. The takeoff line removes a wedge below it, the climb and cruise lines each remove a wedge at low wing loading, and the ceiling line, marked with crosses, removes nothing. Panel 6 marks the design point at the corner of the stall line and the takeoff line.
:width: 85%

Computed for the light twin-jet of the worked example. Each requirement removes part of the plane, and what is left is the region of designs that meet them all. Here the stall speed and the takeoff roll form the corner where the design point lies, while the landing roll and the ceiling remove nothing the others leave.
:::

The shaded area that survives all six lines is the **feasible region**. Any design inside it satisfies every requirement. A larger wing and larger engines add weight and make the aircraft more expensive to build, and a larger wing also adds friction drag in cruise. That is why we pick the {term}`design point` in two steps. First comes the highest wing loading the vertical lines allow, which gives the smallest wing. Then comes the lowest $T/W$ above every line at that wing loading, which gives the smallest engines for that wing. Left of the design point the takeoff line falls, so a lower wing loading can need less thrust, but only with a larger wing. In that case, you get smaller engines only by accepting a larger wing.

:::{tip} A constraint diagram, in steps
1. Write each requirement as a limit on $W/S$ (a vertical line) or as $T/W$ against $W/S$ (a curve or a line).
2. Carry every thrust to sea-level static thrust with the lapse $(\rho/\rho_0)^{m_\text{ad}}$.
3. Plot the lines and shade the region above all of them and left of the vertical ones.
4. Take the smallest of the wing-loading limits and read the highest line there. Then size the wing and the engines: $S = W/(W/S)$ and $T = (T/W)\,W$.
:::

A propeller aircraft is sized the same way, with its power in place of the thrust. Its engine is rated in power, and [page 5.1](#p51-available-and-vmax) gives the thrust of a propeller as $T = \eta P/V$. So each line becomes a line of the power-to-weight ratio $P/W = (T/W)\,V/\eta$, taken at the speed of that requirement. This relation applies only in flight. Near rest the propeller efficiency is low ([page 5.1](#p51-available-and-vmax)), so for the takeoff line you need the static thrust of the propeller itself.

(p55-worked-example)=
## Worked example: sizing a light twin-jet

A light twin-jet has a takeoff mass of 4,500 kg. Its {term}`drag polar` has $C_{D,0} = 0.022$, with an {term}`aspect ratio` of 8 and an Oswald efficiency factor $e = 0.8$ ([page 3.3](#p33-drag-polar)). Its maximum lift coefficient is 1.90 with takeoff flaps and 2.15 with landing flaps. The braking friction is $\mu_r = 0.40$, and its engines lose thrust with altitude as $(\rho/\rho_0)^{0.8}$. It must meet six requirements:

- A stall speed with landing flaps of at most 46 m/s at sea level.
- A takeoff ground roll of at most 750 m at sea level.
- A landing ground roll of at most 700 m at sea level.
- A rate of climb of 12 m/s at 90 m/s at sea level.
- A cruise at 200 m/s at 10,000 m.
- A service ceiling of 12,000 m.

We find the design point, and from it the wing area and the total thrust. Densities come from [the standard atmosphere of page 1.4](../chapter-1/standard-atmosphere.md), with $\rho_0 = 1.2250\ \text{kg/m}^3$.

1. **Weight and induced drag factor.**
   $$
   \begin{aligned}
   W &= 4{,}500 \times 9.81\\
     &= 44{,}145\ \text{N}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   K &= \frac{1}{\pi \times 0.8 \times 8}\\
     &= 0.04974
   \end{aligned}
   $$
2. **The two wing-loading limits.** The stall speed gives
   $$
   \begin{aligned}
   &\left(\frac{W}{S}\right)_\text{stall}\\
   &\;\;\;= 0.5 \times 1.2250 \times {46}^{2}\\
   &\;\;\;\;\;\; \times 2.15\\
   &\;\;\;= 2{,}786.5\ \text{N/m}^2
   \end{aligned}
   $$
   For the landing roll, the numerator is $1.2250 \times 9.81 \times 2.15 \times 0.40 \times 700 = 7{,}234$, so
   $$
   \begin{aligned}
   \left(\frac{W}{S}\right)_\text{landing} &= \frac{7{,}234}{1.69}\\
                                           &= 4{,}280\ \text{N/m}^2
   \end{aligned}
   $$
   The stall speed is the stricter of the two. The wing loading can be at most 2,786.5 N/m², and each thrust line is read there.
3. **Takeoff ground roll.**
   $$
   \begin{aligned}
   &\left(\frac{T}{W}\right)_\text{takeoff}\\
   &\;\;\;= \frac{1.44 \times 2{,}786.5}{1.2250 \times 9.81}\times\\
   &\;\;\;\;\;\; \frac{1}{1.90 \times 750}\\
   &\;\;\;= 0.23432
   \end{aligned}
   $$
4. **Climb at sea level.** The dynamic pressure at 90 m/s is
   $$
   \begin{aligned}
   q &= 0.5 \times 1.2250 \times {90}^{2}\\
     &= 4{,}961\ \text{N/m}^2
   \end{aligned}
   $$
   The three terms of the climb line are $12/90 = 0.1333$ for the climb itself, $4{,}961 \times 0.022/2{,}786.5 = 0.03917$ for the parasite drag, and $0.04974 \times 2{,}786.5/4{,}961 = 0.02794$ for the induced drag:
   $$
   \begin{aligned}
   &\left(\frac{T}{W}\right)_\text{climb}\\
   &\;\;\;= 0.1333 + 0.03917\\
   &\;\;\;\;\;\; + 0.02794\\
   &\;\;\;= 0.2004
   \end{aligned}
   $$
   Two thirds of the thrust goes to the climb, and one third goes to overcoming drag.
5. **Cruise at 10,000 m**, where $\rho = 0.4124\ \text{kg/m}^3$.
   $$
   \begin{aligned}
   q &= 0.5 \times 0.4124 \times {200}^{2}\\
     &= 8{,}248\ \text{N/m}^2
   \end{aligned}
   $$
   $$
   \begin{aligned}
   \left(\frac{\rho}{\rho_0}\right)^{0.8} &= {\left(\frac{0.4124}{1.2250}\right)}^{0.8}\\
                                          &= 0.4185
   \end{aligned}
   $$
   The parasite term is $8{,}248 \times 0.022/2{,}786.5 = 0.06512$ and the induced term $0.04974 \times 2{,}786.5/8{,}248 = 0.01680$:
   $$
   \begin{aligned}
   &\left(\frac{T}{W}\right)_\text{cruise}\\
   &\;\;\;= \frac{0.06512 + 0.01680}{0.4185}\\
   &\;\;\;= 0.1957
   \end{aligned}
   $$
6. **Service ceiling at 12,000 m**, where $\rho = 0.3106\ \text{kg/m}^3$.
   $$
   \begin{aligned}
   \left(\frac{\rho}{\rho_0}\right)^{0.8} &= {\left(\frac{0.3106}{1.2250}\right)}^{0.8}\\
                                          &= 0.3336
   \end{aligned}
   $$
   $$
   \begin{aligned}
   V &= \sqrt{\frac{2 \times 2{,}786.5}{0.3106}}\;\times\\
     &\;\;\; {\left(\frac{0.04974}{0.022}\right)}^{1/4}\\
     &= 164.3\ \text{m/s}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   &2\sqrt{K\,C_{D,0}}\\
   &\;\;\;= 2\sqrt{0.04974 \times 0.022}\\
   &\;\;\;= 0.06616
   \end{aligned}
   $$
   $$
   \begin{aligned}
   &\left(\frac{T}{W}\right)_\text{ceiling}\\
   &\;\;\;= \frac{0.06616 + 0.5/164.3}{0.3336}\\
   &\;\;\;= 0.2074
   \end{aligned}
   $$
7. **Design point, wing, and engines.** At 2,786.5 N/m² the takeoff line is the highest, 0.2343. The ceiling (0.2074), the climb (0.2004), and the cruise (0.1957) lie below it. So the design point is $W/S = 2{,}786.5$ N/m² and $T/W = 0.2343$ ({numref}`fig-p55-constraint-diagram`).
   $$
   \begin{aligned}
   S &= \frac{44{,}145}{2{,}786.5}\\
     &= 15.84\ \text{m}^2
   \end{aligned}
   $$
   $$
   \begin{aligned}
   T &= 0.23432 \times 44{,}145\\
     &= 10{,}344\ \text{N}
   \end{aligned}
   $$
   Each of the two engines must give half of it at sea level, standing still.

The stall speed and the takeoff roll are the two **active** requirements, and their lines intersect at the design point. The other four have margin there. The climb and the ceiling lines lie within about 0.01 of each other over most of the chart, which is why the figure enlarges that strip.

:::{figure} figures/p55-constraint-diagram.svg
:label: fig-p55-constraint-diagram
:alt: Thrust-to-weight ratio, 0 to 0.45, against wing loading, 1,000 to 5,000 newtons per square meter, with an enlarged strip. Vertical lines mark the stall speed, 46 meters per second, solid, at 2,786.5, and the landing roll, 700 meters, dash-dot, at 4,280. A rising straight line is the takeoff roll, 750 meters. A dashed curve is the climb, 12 meters per second at 90 meters per second; a dotted curve is the cruise, 200 meters per second at 10,000 meters; a dash-dot curve with crosses, on the climb near 0.2, is the service ceiling, 12,000 meters. The region above all lines and left of the stall line is shaded. A filled dot marks the design point, 2,786.5 and 0.2343; an open circle in the region marks the light twin-jet, wing 18 square meters, thrust 12,000 newtons.
:width: 85%

Computed for the light twin-jet of the worked example. The design point is the highest wing loading the limits allow, with the lowest thrust-to-weight ratio above every line at that wing loading, at the corner where the stall line intersects the takeoff line. The aircraft's own wing and engines, shown by the open circle, lie inside the region with margin. The lower strip enlarges the climb and ceiling lines, which lie on top of each other at full scale.
:::

**Check.** The light twin-jet itself has a wing of 18 m² and two engines of 6,000 N, 12,000 N in all. Its wing loading and thrust-to-weight ratio are

$$
\begin{aligned}
\frac{W}{S} &= \frac{44{,}145}{18}\\
            &= 2{,}453\ \text{N/m}^2
\end{aligned}
$$

$$
\begin{aligned}
\frac{T}{W} &= \frac{12{,}000}{44{,}145}\\
            &= 0.2718
\end{aligned}
$$

Its wing is larger than the smallest allowed, and its engines give more thrust than the design point needs. Because of that, it lies inside the feasible region, marked by the open circle in {numref}`fig-p55-constraint-diagram`. Its stall speeds with takeoff and with landing flaps are

$$
\begin{aligned}
V_\text{stall,TO} &= \sqrt{\frac{2 \times 2{,}453}{1.2250 \times 1.90}}\\
                  &= 45.91\ \text{m/s}
\end{aligned}
$$

$$
\begin{aligned}
V_\text{stall,L} &= \sqrt{\frac{2 \times 2{,}453}{1.2250 \times 2.15}}\\
                 &= 43.16\ \text{m/s}
\end{aligned}
$$

so it lifts off and touches down at

$$
\begin{aligned}
V_\text{LO} &= 1.2 \times 45.91\\
            &= 55.1\ \text{m/s}
\end{aligned}
$$

$$
\begin{aligned}
V_T &= 1.3 \times 43.16\\
    &= 56.1\ \text{m/s}
\end{aligned}
$$

The ground rolls from [](#eq-p55-field-length) are

$$
\begin{aligned}
s_\text{LO} &= \frac{1.44 \times 2{,}453}{1.2250 \times 9.81}\times\\
            &\;\;\; \frac{1}{1.90 \times 0.2718}\\
            &= 569\ \text{m}
\end{aligned}
$$

$$
\begin{aligned}
s_L &= \frac{1.69 \times 2{,}453}{1.2250 \times 9.81}\times\\
    &\;\;\; \frac{1}{2.15 \times 0.40}\\
    &= 401\ \text{m}
\end{aligned}
$$

Both are well inside the limits of 750 m and 700 m. You can see why in {numref}`fig-p55-field-length-sensitivity`. The aircraft has a lower wing loading than the design point, which shortens both rolls, and more thrust, which shortens only the takeoff.

:::{figure} figures/p55-field-length-sensitivity.svg
:label: fig-p55-field-length-sensitivity
:alt: Ground roll in meters, 0 to 1,200, against wing loading, 0 to 4,800 newtons per square meter. Three straight lines start at the origin: a solid takeoff line for a thrust-to-weight ratio of 0.2343, a dashed and lower takeoff line for 0.2718, and a dotted landing line that holds for any thrust-to-weight ratio. A thin horizontal dashed line marks the takeoff limit, 750 meters, and a thin horizontal dotted line the landing limit, 700 meters. A filled dot marks the design point, where the solid line reaches 750 meters at 2,786.5. At 2,453, marked the light twin-jet, open circles mark its takeoff roll, 569 meters, on the dashed line and its landing roll, 401 meters, on the dotted line.
:width: 90%

Computed from [](#eq-p55-field-length) for the light twin-jet. Both ground rolls grow in proportion to the wing loading, and more thrust shortens only the takeoff. The two takeoff lines differ in $T/W$, while a single landing line applies to every thrust.
:::

## Summary

:::{important} Summary
- With the simplest assumptions, both ground rolls of [](#eq-p55-field-length) grow in proportion to $W/S$. The takeoff roll also falls as $1/(T/W)$, and the landing roll does not depend on the thrust.
- A constraint diagram turns each requirement into a line of $T/W$ against $W/S$, or a vertical limit on $W/S$. The stall speed and the landing roll limit the wing loading. The takeoff, climb, cruise, and ceiling set the thrust needed.
- The design point takes the highest allowed wing loading and the lowest $T/W$ above every line there. That gives the smallest wing, $S = W/(W/S)$, and the smallest engines for that wing, $T = (T/W)\,W$.
:::

:::{table} The equations of this page.
:label: tbl-p55-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Takeoff ground roll | $s_\text{LO} = 1.44\,(W/S)/(\rho\,g\,C_{L,\max,\text{TO}}\,(T/W))$ |
| Landing ground roll | $s_L = 1.69\,(W/S)/(\rho\,g\,C_{L,\max,L}\,\mu_r)$ |
| Stall-speed limit | $W/S \le \tfrac12\,\rho_0\,V_\text{stall}^2\,C_{L,\max,L}$ |
| Landing-roll limit | $W/S \le \rho_0\,g\,C_{L,\max,L}\,\mu_r\,s_L/1.69$ |
| Takeoff line | $T/W \ge 1.44\,(W/S)/(\rho_0\,g\,C_{L,\max,\text{TO}}\,s_\text{LO})$ |
| Climb line | $T/W \ge (R/C)/V + q\,C_{D,0}/(W/S) + K\,(W/S)/q$ |
| Cruise line | $T/W \ge [q\,C_{D,0}/(W/S) + K\,(W/S)/q]/(\rho/\rho_0)^{m_\text{ad}}$ |
| Ceiling line | $T/W \ge [2\sqrt{K\,C_{D,0}} + 0.5/V]/(\rho/\rho_0)^{m_\text{ad}}$ |
| Power-to-weight ratio of a propeller aircraft (in flight) | $P/W = (T/W)\,V/\eta$ |

:::

:::{exercise} For discussion
:label: ex-p55-discussion

1. In {numref}`fig-p55-constraint-diagram`, which requirements would force a larger wing or larger engines if they became 10% stricter, and which have room to spare?
2. Why does the cruise line slope downward at low wing loading, while the takeoff line always slopes upward?
3. Suppose the light twin-jet must also land on a wet runway, where the braking friction drops from 0.40 to 0.25. How does the landing limit move, and does it become active?
4. Better flaps raise both maximum lift coefficients by 15%. How do the stall limit, the landing limit, and the takeoff line move, and what happens to the design point?
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 6.
- Horne, W. B., and Leland, T. J. W., *[Influence of Tire Tread Pattern and Runway Surface Condition on Braking Friction and Rolling Resistance of a Modern Aircraft Tire](https://ntrs.nasa.gov/citations/19620005764)*, NASA TN D-1376, 1962.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA, 2018. Chapter 5 (thrust-to-weight ratio and wing loading) and Chapter 17 (takeoff and landing).
- U.S. Code of Federal Regulations, Title 14, Part 25: [Section 25.113, Takeoff distance and takeoff run](https://www.law.cornell.edu/cfr/text/14/25.113), and [Section 25.125, Landing](https://www.law.cornell.edu/cfr/text/14/25.125).
