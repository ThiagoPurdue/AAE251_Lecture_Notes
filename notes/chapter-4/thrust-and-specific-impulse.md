---
title: "4.1 Thrust and Specific Impulse"
short_title: 4.1 Thrust and Specific Impulse
---

:::{include} ../_parts/standards/4.1.md
:::

A rocket engine has one job: to push. To turn the delta-V of Chapter 2 into propellant, we need to know how it makes that push and how well it uses what it burns. On this page we start from momentum and derive the thrust of a rocket engine. We follow the gas through the engine, from the combustion chamber to the exit of the nozzle. Then we define the two numbers that describe an engine's performance, the effective exhaust velocity and the specific impulse. Last, we see how the exit pressure, the size of the nozzle, and the altitude change the thrust. The same equation then works for an engine that breathes air.

:::{note} What to take from this page
- Thrust has two parts: the momentum the exhaust carries away, $\dot m V_e$, and the pressure term, $(p_e - p_a)A_e$, which can be positive, zero, or negative.
- The effective exhaust velocity is $c = F/\dot m$, and the specific impulse is $I_\text{sp} = c/g_0$, in seconds, with $g_0 = 9.81\ \text{m/s}^2$ everywhere.
- Comparing the exit pressure with the ambient pressure tells whether a nozzle is overexpanded ($p_e < p_a$), ideally expanded, or underexpanded ($p_e > p_a$).
- A larger area ratio lowers the exit pressure. In vacuum a larger nozzle always helps; at sea level there is a best area ratio. A fixed nozzle gains thrust all the way to vacuum.
:::

## A rocket pushes on its own exhaust

Picture a person standing on a skateboard with a heavy ball. The person throws the ball forward and rolls backward. Nothing outside pushed the person. Person and ball started at rest, so their total momentum was zero, and it is still zero after the throw. The ball carries momentum one way, and the person carries the same amount the other way.

A rocket does the same thing many times a second. It throws mass, its exhaust gas, backward at high speed, and it gains the momentum the exhaust carries the other way. It does not need air, the ground, or anything else to push against. That is why a rocket works in the vacuum of space, and even works a little better there, as we see later on this page.

This was not obvious to everyone. In 1920 an editorial in *The New York Times* mocked Robert Goddard for claiming that a rocket could work in a vacuum. The editorial assumed that a rocket needs air to push against. In 1969, the day after Apollo 11 left for the Moon, the newspaper printed a short correction. It said that a rocket can work in a vacuum as well as in an atmosphere (Uri 2021).

(p41-thrust-from-momentum)=
## Thrust from the momentum of the exhaust

We now put the skateboard idea into an equation. Newton's second law, written for momentum, says that a force equals the rate of change of momentum. A rocket engine throws out gas continuously. Suppose the engine throws out a small mass $\Delta m$ in a short time $\Delta t$, and each bit of it leaves at speed $c$ relative to the rocket. That mass carries away the momentum $\Delta m\,c$. Dividing by the time gives the rate at which the exhaust carries momentum away, and this rate is the force the engine and its exhaust push on each other:

:::{math}
:label: eq-p41-thrust-momentum
F = \frac{\Delta m}{\Delta t}\,c = \dot m\,c
:::

Here $\dot m$ is the {term}`mass flow rate` of propellant through the engine, in kg/s (we met it with the continuity equation on [page 1.5](#p15-continuity)). The force on the rocket is the {term}`thrust` $F$, in newtons, and it points opposite to the exhaust.

[](#eq-p41-thrust-momentum) says there are two ways to get more thrust: throw more mass each second, or throw it faster. The speed $c$ is called the effective exhaust velocity. The word "effective" makes sense once we add the pressure at the nozzle exit, in [the thrust equation](#p41-thrust-equation).

## Inside a rocket engine

To throw gas out fast, a rocket engine turns the chemical energy of its propellants into heat, and the heat into speed. In {numref}`fig-p41-engine-anatomy` we follow the parts in the order the gas meets them:

1. The **injector** sprays the fuel and the oxidizer into the chamber and mixes them.
2. In the **{term}`combustion chamber`** they burn. The products are a gas at a high temperature and a high pressure, moving slowly.
3. The **converging section** narrows, and the gas speeds up as the area shrinks.
4. The **{term}`throat`** is the narrowest point.
5. The **diverging section** widens again, and the gas keeps speeding up while its pressure and temperature fall.
6. At the **exit plane** the gas leaves the engine with the {term}`exit velocity` $V_e$, the exit pressure $p_e$, through the exit area $A_e$.

The converging and diverging sections together are the **{term}`nozzle`**.

:::{figure} figures/p41-engine-anatomy.svg
:label: fig-p41-engine-anatomy
:alt: A rocket thrust chamber cut in half lengthwise, flow from left to right. Fuel and oxidizer arrows enter at the left through a flat injector plate. Numbered callouts mark, in flow order, 1 the injector, 2 the combustion chamber, a short cylinder, 3 the converging section, 4 the throat, the narrowest point, marked by a short dashed line across it, 5 the long, widening diverging section, and 6 the exit plane, a dashed line at the open end, where an arrow labeled exhaust leaves. Below, three boxes joined by arrows: chemical energy of the propellants, which burns in part 2 to give heat, a hot gas at high pressure, which expands in parts 3 to 5 to give speed, a fast, cooler exhaust.
:width: 95%

Schematic of a liquid rocket thrust chamber in section. The engine turns chemical energy into heat in the chamber, and heat into speed in the nozzle; the numbers follow the gas. Proportions of the F-1 engine (area ratio 16; NASA 1968a), contour after Huzel and Huang (1967, Section 4.3), wall thickness exaggerated.
:::

{numref}`fig-p41-nozzle-flow` follows the gas along the nozzle. The pressure falls from the chamber to the exit, the temperature falls too, and the speed rises. The gas trades its pressure and its heat for speed. The narrowing and widening shape is what lets the gas pass the speed of sound. Before the throat the gas moves slower than the {term}`speed of sound`, which we met on [page 1.4](#p14-speed-of-sound). At the throat it reaches the speed of sound. After the throat it moves faster than sound and speeds up further as the nozzle widens (Huzel and Huang 1967, p. 6). Why a faster-than-sound flow speeds up in a widening duct is a question for a later course in compressible flow. Here we take the result and use it.

:::{figure} figures/p41-nozzle-flow.svg
:label: fig-p41-nozzle-flow
:alt: Two panels at the same horizontal scale. The upper panel is a plot of three ratios along the nozzle. Pressure, a solid line, starts at 1 in the chamber, falls steeply through the throat, and ends near zero at the exit. Temperature, a dashed line, starts at 1 and falls to about 0.44. Speed, a dotted line, starts low in the chamber, rises steeply through the throat and reaches 1 at the exit. A vertical dashed line at the throat is labeled throat, speed of sound, with slower than sound to its left and faster than sound to its right. The lower panel is the upper half of the thrust chamber, narrowest at the same vertical line, with the chamber, the throat, the exit, and the nozzle wall named.
:width: 80%

Computed: the gas trades pressure and temperature for speed, and it passes the speed of sound at the throat. Ideal-nozzle relations of Huzel and Huang (1967, Section 1.2) for the F-1 contour of {numref}`fig-p41-engine-anatomy`, with a ratio of specific heats of 1.2, the value of their Sample Calculation 1-2. Pressure and temperature are ratios to their values at the start of the chamber, speed is a ratio to the exit speed.
:::

(p41-thrust-equation)=
## The thrust equation

[](#eq-p41-thrust-momentum) leaves out one effect: the pressure of the exhaust at the exit plane. To see it, we draw a box around the whole engine, a **control volume**, and write Newton's second law for what is inside it ({numref}`fig-p41-control-volume`). We make three assumptions:

1. The engine runs steadily, so nothing inside the box changes with time.
2. The exhaust leaves straight back, with one speed $V_e$ and one pressure $p_e$ over the whole exit plane.
3. The propellants enter the engine with negligible momentum along the axis.

:::{figure} figures/p41-control-volume.svg
:label: fig-p41-control-volume
:alt: A rocket engine inside a dashed rectangle labeled control volume. A hatched engine mount runs left from the injector, through the left side of the rectangle, to a hatched block labeled vehicle. Short gray arrows labeled ambient pressure p a press inward on the top, bottom, and left sides and on the right side above and below the nozzle exit. On the exit plane, of area A e, longer and heavier black arrows labeled exit pressure p e press inward. An open block arrow leaves the exit to the right, labeled exhaust, m dot, V e. Inside the box, just above the mount, a heavy arrow points right, toward the exhaust, labeled force on the engine from the vehicle, F. Outside, a heavy arrow points left from the vehicle, labeled thrust on the vehicle, F.
:width: 90%

Schematic, not to scale. Thrust has two parts: the momentum that leaves through the exit plane, and the pressure on the exit plane that is not balanced by the outside air. The arrows on the box are forces on what is inside it; the thrust on the vehicle is the equal and opposite force at the mount. After Huzel and Huang (1967, Section 1.2) and NASA Glenn Research Center (n.d.a).
:::

We take the direction of the exhaust as positive and go in steps.

1. **Momentum.** Each second, mass $\dot m$ leaves the box at speed $V_e$ and the propellants bring in no momentum along the axis. So the net force on what is inside the box, in the direction of the exhaust, must be $\dot m V_e$.
2. **The force from the vehicle.** The engine pushes the vehicle forward with the thrust $F$. By Newton's third law the vehicle pushes back on the engine with the same force, toward the exhaust: $+F$. {numref}`fig-p41-control-volume` draws both: the force on the engine where the mount crosses the box, and the thrust on the vehicle outside it.
3. **The pressure.** The outside air presses on every face of the box with the ambient pressure $p_a$, except on the exit plane, where the exhaust presses with $p_e$. A uniform pressure all around a closed box adds up to no force. So we split the pressure on the exit plane into $p_a$, which cancels with the rest, and the difference $p_e - p_a$. The difference acts on the area $A_e$, pushing into the box, against the exhaust: $-(p_e - p_a)A_e$.
4. **Newton's second law.** The forces add up to the momentum that leaves each second:

$$
F - (p_e - p_a)A_e = \dot m V_e
$$

Solving for $F$ gives the rocket thrust equation:

:::{math}
:label: eq-p41-thrust
F = \dot m V_e + (p_e - p_a)A_e
:::

The first term is the **{term}`momentum thrust`** and the second is the **{term}`pressure thrust`** (NASA Glenn Research Center n.d.a). Both have units of newtons: (kg/s)(m/s) = kg·m/s² = N, and (Pa)(m²) = (N/m²)(m²) = N.

The pressure thrust has a plain meaning. Suppose the gas leaves at a pressure above that of the air around it. Then the gas inside the nozzle has pushed on the walls harder than the outside air pushes back, and the engine gets extra thrust. If the gas leaves below the outside pressure, the outside air wins and the term is negative.

:::{warning} Pascals, not kilopascals
The pressure term needs pressures in pascals, so that pressure times area gives newtons. If you put 85 and 101.325 (kPa) into $(p_e - p_a)A_e$ with $A_e$ = 0.95 m², you get −15.51 N instead of −15,509 N. That is a thousand times too small, and the pressure term seems to vanish.
:::

(p41-specific-impulse)=
## Effective exhaust velocity and specific impulse

Now we can say what "effective" means. We compare [](#eq-p41-thrust) with $F = \dot m c$ and ask which single speed $c$ would give the whole thrust:

:::{prf:definition} Effective exhaust velocity
:label: def-p41-c

The **{term}`effective exhaust velocity`** $c$ is the thrust per unit mass flow rate of propellant:

$$
c = \frac{F}{\dot m} = V_e + \frac{(p_e - p_a)A_e}{\dot m}
$$
:::

It is not a speed anyone could measure in the jet. It is the exit velocity corrected for the pressure term, so that $F = \dot m c$ holds exactly. When $p_e = p_a$, the two are equal.

Engineers usually quote the same information as a time. Over a time $\Delta t$ the engine delivers the impulse $F\,\Delta t$, the change of momentum it gives the vehicle, and burns the mass $\Delta m = \dot m\,\Delta t$. On Earth that propellant would weigh $\Delta m\,g_0$.

:::{prf:definition} Specific impulse
:label: def-p41-isp

The **{term}`specific impulse`** is the impulse delivered per unit weight of propellant burned, with the weight taken at the {term}`standard gravity` $g_0 = 9.81\ \text{m/s}^2$:

$$
I_\text{sp} = \frac{F\,\Delta t}{\Delta m\,g_0} = \frac{F}{\dot m\,g_0} = \frac{c}{g_0}
$$
:::

Thrust divided by a weight flow, N divided by N/s, leaves seconds. Pounds of thrust divided by pounds per second of weight flow also leave seconds. The number is the same in SI and in English units, and engine makers quote it that way (NASA Glenn Research Center n.d.b). The seconds are not a time of anything (Huzel and Huang 1967, p. 11). To go back to a speed, multiply: $c = I_\text{sp}\,g_0$. The RS-25, the main engine of the Space Shuttle, has $I_\text{sp}$ = 455.2 s in vacuum (NASA 1981, p. 2-4), so its effective exhaust velocity there is $455.2 \times 9.81 = 4{,}466$ m/s.

:::{warning} $g_0$ is not the local gravity
$g_0$ is a fixed conversion number, 9.81 m/s², on the launch pad, in orbit, or on the Moon. If you divide $c$ by the gravity of the place where the engine fires, you get a different specific impulse for the same engine, and the numbers no longer compare. Specific impulse is also not a velocity: if you put 455.2 s into a formula that wants m/s, you are off by a factor of 9.81.
:::

Specific impulse and thrust answer different questions. Thrust says how hard the engine pushes. Specific impulse says how much thrust each kilogram per second of propellant buys, so it measures how well the engine uses its propellant. One engine can have a lot of one and little of the other. At sea level the F-1, the first-stage engine of the Saturn V, gave 6,770 kN (1,522,000 lbf) at 265 s (NASA 1968a; Biggs 2009, p. 19). The RS-25 gave 1,668 kN at 363.2 s (NASA 1981, p. 2-4). The F-1 pushed 4.1 times as hard, while the RS-25 got 37% more thrust out of each kilogram per second of propellant. [Page 4.4](#p44-kinds) compares the kinds of rocket propulsion in a table and shows that high specific impulse and high thrust rarely come together. Its [table of propellants](#tbl-p44-propellants) gives the specific impulse of the common propellant pairs.

### Worked example 1: a first-stage engine at sea level

An engine burns 340 kg/s of propellant. The exhaust leaves the exit plane at $V_e$ = 2,750 m/s and $p_e$ = 85.0 kPa, through an exit area of 0.95 m². Find the thrust and its two parts, the effective exhaust velocity, the specific impulse, and the state of the nozzle at sea level, where $p_a$ = 101,325 Pa.

1. **Momentum thrust.**
   $$
   \begin{aligned}
   \dot m V_e &= 340 \times 2{,}750\\
              &= 935{,}000\ \text{N}
   \end{aligned}
   $$
2. **Pressure thrust**, with both pressures in pascals: $p_e - p_a = 85{,}000 - 101{,}325 = -16{,}325$ Pa, so
   $$
   \begin{aligned}
   &(p_e - p_a)A_e\\
   &\;\;\;= (-16{,}325) \times 0.95\\
   &\;\;\;= -15{,}509\ \text{N}
   \end{aligned}
   $$
3. **Thrust**, [](#eq-p41-thrust).
   $$
   \begin{aligned}
   F &= 935{,}000 - 15{,}509\\
     &= 919{,}491\ \text{N}
   \end{aligned}
   $$
   That is 919.5 kN.
4. **Effective exhaust velocity.**
   $$
   \begin{aligned}
   c &= \frac{F}{\dot m}\\
     &= \frac{919{,}491}{340}\\
     &= 2{,}704.4\ \text{m/s}
   \end{aligned}
   $$
5. **Specific impulse.**
   $$
   \begin{aligned}
   I_\text{sp} &= \frac{c}{g_0}\\
               &= \frac{2{,}704.4}{9.81}\\
               &= 275.7\ \text{s}
   \end{aligned}
   $$
6. **State of the nozzle.** $p_e$ = 85.0 kPa is below $p_a$ = 101.3 kPa, so the nozzle is overexpanded at sea level and the pressure term is negative.

**Check.** The second form of $c$ gives the same answer: the pressure term per unit mass flow is $-15{,}509/340 = -45.61$ m/s, and $2{,}750 - 45.61 = 2{,}704.4$ m/s. The pressure term is small, 1.7% of the thrust, as it usually is near ideal expansion. In vacuum the same engine at the same flow would get the full $p_e A_e = 85{,}000 \times 0.95 = 80{,}750$ N, so $F = 935{,}000 + 80{,}750 = 1{,}015{,}750$ N, about 10% more than at sea level.

(p41-expansion)=
## Overexpanded, underexpanded, ideally expanded

The sign of the pressure term depends only on how the exit pressure compares with the ambient pressure. Engineers give the three cases names ({numref}`fig-p41-expansion-states`):

- **{term}`Overexpanded`**, $p_e < p_a$. The nozzle expanded the gas too far, below the pressure of the air around it. The pressure term is negative. Outside the exit the higher ambient pressure squeezes the jet inward, and the plume narrows, often with a pattern of bright {term}`shock` diamonds. A shock is a thin zone where the gas slows down and its pressure jumps.
- **{term}`Ideally expanded`**, $p_e = p_a$. The pressure term is zero, the jet leaves straight, and $c = V_e$.
- **{term}`Underexpanded`**, $p_e > p_a$. The nozzle did not expand the gas far enough. The pressure term is positive. Outside the exit the gas keeps expanding into the lower pressure around it, and the plume spreads wide.

:::{figure} figures/p41-expansion-states.svg
:label: fig-p41-expansion-states
:alt: Three identical nozzles stacked from top to bottom, each with a dashed jet boundary leaving its exit. Top, overexpanded: the boundary, labeled jet boundary, turns inward, gray arrows labeled p a press it in from outside, and two thin lines labeled shocks cross on the axis behind the exit; p e is less than p a, pressure term negative. Middle, ideally expanded: the boundary runs straight back at the exit radius; p e equals p a, pressure term zero. Bottom, underexpanded: the boundary turns outward, gray arrows labeled p e push it out from inside; p e is greater than p a, pressure term positive.
:width: 80%

Schematic, not to scale; plume angles exaggerated. One nozzle at three outside pressures: the plume shows which way the pressure term pushes. It is squeezed in when the exit pressure is below the ambient pressure, straight when they are equal, and spread out when the exit pressure is above it. After Huzel and Huang (1967, Section 1.2).
:::

Real plumes show the same thing. {numref}`fig-p41-plume-sea-level` shows engines firing near sea level, and {numref}`fig-p41-plume-altitude` shows a vehicle high in its climb.

:::{figure} figures/p41-plume-sea-level-photo.jpg
:label: fig-p41-plume-sea-level
:alt: The tail of the Space Shuttle Endeavour just after liftoff, seen from below: two main-engine bells at the top, partly hidden by the body flap, and the edge of a wing at the right. Below the engine area, three narrow, pale blue exhaust plumes; each starts to glow a short way below the vehicle with a bright, flat upper edge. The ground and the water lie far below.
:width: 60%

Photograph. Near sea level the plumes of the main engines stay narrow: the outside air, at a higher pressure than the exhaust, squeezes each jet, and the bright, flat edge where each plume starts to glow is a shock in the jet. Space Shuttle Endeavour just after liftoff, 2007. NASA/Kennedy Space Center photo KSC-07pp2287, public domain; cropped from the original in the [NASA Image and Video Library](https://images.nasa.gov/details/KSC-07pp2287).
:::

:::{figure} figures/p41-plume-altitude-photo.jpg
:label: fig-p41-plume-altitude
:alt: A Saturn V high in its climb against a dark blue sky, seen from the side. Its orange exhaust plume spreads far wider than the rocket and trails down and away behind it.
:width: 60%

Photograph. High in the climb the outside pressure is low, and the plume spreads far wider than the rocket. This photograph and {numref}`fig-p41-plume-sea-level` show different vehicles, a Saturn V high up and a Space Shuttle near sea level; only the outside pressure matters here. The Saturn V of Apollo 11 photographed from an aircraft during its climb, 1969. NASA/U.S. Air Force image 69PC-413, public domain; cropped from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:ALOTS_image_of_Apollo_11_launch_%2869PC-413%29.jpg).
:::

Now suppose we can choose the nozzle for a given engine and flow, and we want the most thrust at one ambient pressure. If we make the nozzle a little longer and wider, the gas expands further: $V_e$ rises and $p_e$ falls. As long as $p_e > p_a$, the extra expansion gains more momentum thrust than it loses pressure thrust. Once $p_e < p_a$, the gas is expanded below the outside pressure and the trade turns against us. The best nozzle at one ambient pressure is therefore the one that makes $p_e = p_a$ (Huzel and Huang 1967, p. 15). For a nozzle that already exists, this does not mean that thrust is highest where $p_e = p_a$. We come back to this point in the section on altitude.

:::{warning} Overexpanded is $p_e < p_a$
If you mix up the two names, think of what the nozzle did to the gas. "Over" means it expanded the gas too much, so the exit pressure fell below $p_a$. "Under" means it did not expand the gas enough, so $p_e$ is still above $p_a$. Then the sign of $(p_e - p_a)$ follows: negative when overexpanded, positive when underexpanded.
:::

(p41-area-ratio)=
## Area ratio

The nozzle controls the expansion through its shape. The **{term}`area ratio`** (also called the expansion ratio) is the exit area divided by the throat area, $A_e/A_t$. The larger the area ratio, the further the gas expands: the exit pressure is lower and the exit velocity is higher. The relation between the area ratio and the pressure ratio comes from the equations of compressible flow. We do not solve it by hand. {numref}`fig-p41-isp-area-ratio` shows its result for one propellant pair.

:::{figure} figures/p41-isp-area-ratio.svg
:label: fig-p41-isp-area-ratio
:alt: Plot of specific impulse in seconds against area ratio from 0 to 60. A dashed curve, in vacuum, rises steeply and keeps rising, to about 366 seconds at an area ratio of 60. A solid curve, at sea level, rises to a peak of 300 seconds at an area ratio of 10, marked with a dot and the note best at sea level, p e equals p a, then falls slowly and stops at an area ratio of 21 with an open circle labeled flow may separate from the wall.
:width: 80%

Computed: at sea level there is a best area ratio, where $p_e = p_a$; in vacuum a larger nozzle always helps. Liquid oxygen and kerosene at a chamber pressure of 1,000 psia (6.895 MPa), ideal-nozzle relations of Huzel and Huang (1967, Section 1.2) with the ratio of specific heats (1.14) that matches their theoretical thrust coefficient (Table 1-9). The sea-level curve stops where $p_e$ falls to 0.4 $p_a$, an early rule of thumb for flow separation (NASA 1976, p. 17).
:::

Two lessons come out of the figure.

- **At sea level there is a best area ratio.** For these propellants and this {term}`chamber pressure` (the pressure of the gas in the combustion chamber), the best area ratio is 10. There $p_e = p_a$ and the specific impulse peaks at 300 s. A larger nozzle overexpands the gas and loses thrust. Far past the best ratio the flow can stop following the wall and separate from it, which causes large sideways loads on the nozzle. An early rule of thumb put the danger at about $p_e = 0.4\,p_a$, and the exact point cannot be predicted well (NASA 1976, p. 17).
- **In vacuum a larger nozzle always helps.** With $p_a = 0$ there is nothing to overexpand against, and the curve keeps rising: 327 s at the sea-level best ratio of 10, 359 s at 40. What stops the designer is the size and the mass of the nozzle, not the gas.

This is why an engine that fires near sea level carries a short nozzle with a small area ratio. An engine that fires only in vacuum carries a long one with a large area ratio. {numref}`fig-p41-nozzle-sizes` draws two engines of the Saturn V to the same throat size. The F-1 of the first stage has an area ratio of 16 (NASA 1968a); the J-2 of the upper stages, 27.5 (NASA 1968b). The F-1's 16 is past the sea-level best because the engine keeps firing high into the thin air, where a larger nozzle pays off. The RS-25 lights on the launch pad but works mostly at altitude, and its area ratio is 77.5 (NASA 1981, p. 2-4). It can afford that because its chamber pressure is high. It runs at 2,970 psia (pounds per square inch, absolute; 20.5 MPa), three to four times the F-1's 965 psia and the J-2's 763 psia. The higher the chamber pressure, the larger the area ratio a nozzle can have before its exit pressure falls to a given value (Huzel and Huang 1967, Eq. 1-20).

:::{figure} figures/p41-nozzle-sizes.svg
:label: fig-p41-nozzle-sizes
:alt: Two thrust chambers in section side by side, drawn with throats of the same size, each with its throat diameter marked. Left, the F-1, a sea-level engine with area ratio 16.0: its exit diameter is 4.00 times the throat diameter. Right, the J-2, a vacuum engine with area ratio 27.5: its nozzle is longer and its exit diameter is 5.24 times the throat diameter.
:width: 85%

Computed contours drawn with the same throat: a vacuum engine carries a much larger nozzle for the same throat. Published area ratios of the F-1 (16) and the J-2 (27.5) (NASA 1968a, 1968b), bell shapes after Huzel and Huang (1967, Section 4.3), wall thickness exaggerated. The real J-2 is a smaller engine than the F-1: here only the shapes are compared.
:::

## Thrust changes with altitude

A launch vehicle climbs from sea level to vacuum with one fixed nozzle on each engine. Along the way the ambient pressure falls, and only that changes in [](#eq-p41-thrust). At the same power setting, $\dot m$, $V_e$, and $p_e$ stay the same, as long as the flow stays attached to the nozzle wall. The sum $\dot m V_e + p_e A_e$ is then a constant. In vacuum, where $p_a = 0$, that constant is the vacuum thrust $F_\text{vac}$. At any altitude:

:::{math}
:label: eq-p41-altitude
F = F_\text{vac} - p_a A_e
:::

As the vehicle climbs, $p_a$ falls and the thrust rises, all the way to vacuum. The nozzle is ideally expanded at one altitude only, where $p_a = p_e$. That altitude is not where the thrust is highest: above it the nozzle is underexpanded, the pressure term is positive, and the thrust keeps growing.

### Worked example 2: the RS-25 from sea level to vacuum

The Space Shuttle News Reference gives the RS-25 at rated power, 100% of its design thrust (NASA 1981, p. 2-4). At sea level it gives 375,000 lbf (1,668.1 kN) with $I_\text{sp}$ = 363.2 s; in vacuum, 470,000 lbf (2,090.7 kN) with $I_\text{sp}$ = 455.2 s. Find the mass flow, the exit area, and the thrust and specific impulse at 8 km and at 30 km.

1. **Mass flow**, from $F = \dot m I_\text{sp} g_0$ at sea level:
   $$
   \begin{aligned}
   \dot m &= \frac{F_\text{sl}}{I_\text{sp,sl}\,g_0}\\
          &= \frac{1.6681 \times {10}^{6}}{363.2 \times 9.81}\\
          &= 468.2\ \text{kg/s}
   \end{aligned}
   $$
   The vacuum values give the same flow: $2.0907 \times {10}^{6}/(455.2 \times 9.81) = 468.2$ kg/s. The source is consistent, and one engine at one power setting has one flow.
2. **Exit area.** At sea level $p_a$ = 101,325 Pa, and [](#eq-p41-altitude) gives $F_\text{vac} - F_\text{sl} = p_a A_e$:
   $$
   \begin{aligned}
   &F_\text{vac} - F_\text{sl}\\
   &\;\;\;= 2{,}090.7 - 1{,}668.1\\
   &\;\;\;= 422.6\ \text{kN}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   A_e &= \frac{F_\text{vac} - F_\text{sl}}{p_a}\\
       &= \frac{422{,}600}{101{,}325}\\
       &= 4.171\ \text{m}^2
   \end{aligned}
   $$
   A circle of 4.171 m² has a diameter of 2.304 m, against the 2.3 m the same reference shows for the nozzle exit. The published thrusts and the published nozzle agree.
3. **At 8 km**, the ambient pressure is 35,582 Pa (from the standard atmosphere of [page 1.4](#p14-layers)). The lost pressure thrust is $p_a A_e = 35{,}582 \times 4.171 = 148{,}413$ N, or 148.4 kN, so
   $$
   \begin{aligned}
   F &= 2{,}090.7 - 148.4\\
     &= 1{,}942.3\ \text{kN}
   \end{aligned}
   $$
   and $I_\text{sp} = 1.9423 \times {10}^{6}/(468.2 \times 9.81) = 422.9$ s.
4. **At 30 km**, the ambient pressure is 1,159 Pa, so $p_a A_e = 1{,}159 \times 4.171 = 4{,}834$ N, or 4.834 kN, and
   $$
   \begin{aligned}
   F &= 2{,}090.7 - 4.834\\
     &= 2{,}086\ \text{kN}
   \end{aligned}
   $$
   with $I_\text{sp} = 2.086 \times {10}^{6}/(468.2 \times 9.81) = 454.2$ s.
5. **State of the nozzle.** The source does not give the exit pressure. The ideal-nozzle relations of Huzel and Huang (1967) give about 15.8 kPa for this area ratio and chamber pressure (the caption of {numref}`fig-p41-thrust-altitude` gives the details). At 8 km, $p_a$ = 35.58 kPa is higher, so the nozzle is overexpanded and the pressure term $(p_e - p_a)A_e$ is about −82.5 kN. At 30 km, $p_a$ = 1.159 kPa is lower, so the nozzle is underexpanded and the pressure term is about 61.0 kN.

**Check.** The thrust lies between the sea-level and the vacuum values at both altitudes, and it is larger higher up. {numref}`fig-p41-thrust-altitude` shows the whole climb. From sea level to vacuum the RS-25 gains 25% in thrust and in specific impulse, with nothing changed but the air outside. The nozzle is ideally expanded at about 13.3 km, where the thrust is 2,025 kN, and the thrust keeps rising above that altitude.

:::{figure} figures/p41-thrust-altitude.svg
:label: fig-p41-thrust-altitude
:alt: Two stacked plots against altitude from 0 to 60 kilometers for the RS-25 engine. Top, thrust in kilonewtons: a curve rises from 1,668.1 at sea level, marked with a square, through 1,942.3 at 8 kilometers, marked with an open circle, and a filled dot at 13.3 kilometers labeled ideally expanded, to 2,086 at 30 kilometers, another open circle, and then flattens against a dashed line at the vacuum thrust, 2,090.7. Bottom, specific impulse in seconds, the same shape: 363.2 at sea level, 422.9 at 8 kilometers, 454.2 at 30 kilometers, approaching the dashed vacuum value, 455.2.
:width: 80%

Computed for the RS-25 at rated power: a fixed nozzle gains thrust all the way up; ideal expansion, near 13.3 km, is one point on the way and not the maximum. From $F = F_\text{vac} - p_a A_e$ with the published thrusts (NASA 1981, p. 2-4), the exit area from worked example 2, and the standard atmosphere of page 1.4. Open circles: the two altitudes of worked example 2. The ideal-expansion altitude uses an exit pressure of 15.8 kPa, computed, not published. It comes from the ideal-nozzle relations of Huzel and Huang (1967, Section 1.2) for the area ratio of 77.5 and the chamber pressure of 20.5 MPa. The ratio of specific heats is 1.236, the value that matches their theoretical thrust coefficient for oxygen and hydrogen (Table 1-10).
:::

(p41-air-breathing)=
## The same equation for an engine that breathes air

A jet engine or a ramjet also makes thrust by throwing gas backward. The difference is where the gas comes from. A rocket carries everything it throws out, so its propellant enters with no momentum along the axis. An engine that breathes air takes its gas from the air it flies through. Seen from the engine, that air arrives already moving at the flight speed $V_\infty$. So the engine gets credit only for the speed it adds to the air. We apply the same control volume, with the air entering at $V_\infty$ and the ambient pressure now written $p_\infty$, and get:

:::{math}
:label: eq-p41-air
\begin{aligned}
F &= \dot m (V_e - V_\infty)\\
&\;\;\; + (p_e - p_\infty)A_e\\
\dot m &= \rho V A
\end{aligned}
:::

Here $\dot m$ is the mass flow of air, which continuity gives from the free-stream density, the flight speed, and the area of the {term}`stream tube` the inlet captures. The mass of the fuel is small compared with the air, and we leave it out (NASA Glenn Research Center n.d.d).

A **{term}`ramjet`** is the simplest such engine ({numref}`fig-p41-air-breathing`). It has no compressor: its forward speed rams the air into the inlet, which slows the air and raises its pressure. Fuel burns in the compressed air, and the hot gas leaves through a nozzle faster than the air came in. Because the compression comes from the flight speed, a ramjet makes thrust only when it is already moving fast. Another engine must bring it up to speed first (NASA Glenn Research Center n.d.c). [Chapter 5 covers engines that breathe air](#p54-how-engines-make-thrust) and measures how much fuel they use.

:::{figure} figures/p41-air-breathing.svg
:label: fig-p41-air-breathing
:alt: A ramjet cut in half lengthwise: an open inlet at the left, labeled A = 0.2649 square meters, that widens smoothly into a long combustor, where a fuel arrow enters through the wall, then a nozzle that narrows and widens to the exit at the right, labeled A e = 0.40 square meters. A velocity arrow before the inlet is labeled air in, V infinity, 750 meters per second. A longer velocity arrow behind the exit is labeled out, V e, 1,250 meters per second. Under it, a dashed arrow repeats the incoming speed, and a dimension from its tip to the tip of the outgoing arrow is labeled change, V e minus V infinity. A key names the velocity arrows, drawn to one scale, and the flow arrow.
:width: 80%

Schematic of a ramjet. Only the change of speed of the air counts: the air arrives at $V_\infty$ and leaves at $V_e$, and the dashed arrow repeats the incoming speed under the outgoing one. The length is not to scale; the inlet and exit areas and the speeds are those of worked example 3, and the velocity arrows are drawn to one scale. A real inlet at this speed first slows the air through shocks; the sketch shows only the duct.
:::

### Worked example 3: a ramjet at 14 km

A ramjet flies at 750 m/s at 14 km, where the standard atmosphere of page 1.4 gives $p_\infty$ = 14,088 Pa and $\rho_\infty$ = 0.2265 kg/m³ (Mach 2.54). It takes in 45 kg/s of air, and the exhaust leaves at 1,250 m/s and 16.0 kPa through an exit area of 0.40 m². Find the thrust and the inlet area.

1. **Momentum term.**
   $$
   \begin{aligned}
   &\dot m (V_e - V_\infty)\\
   &\;\;\;= 45 \times (1{,}250 - 750)\\
   &\;\;\;= 22{,}500\ \text{N}
   \end{aligned}
   $$
2. **Pressure term.** $p_e - p_\infty = 16{,}000 - 14{,}088 = 1{,}912$ Pa, so
   $$
   \begin{aligned}
   &(p_e - p_\infty)A_e\\
   &\;\;\;= 1{,}912 \times 0.40\\
   &\;\;\;= 764.8\ \text{N}
   \end{aligned}
   $$
3. **Thrust.**
   $$
   \begin{aligned}
   F &= 22{,}500 + 764.8\\
     &= 23{,}265\ \text{N}
   \end{aligned}
   $$
   That is 23.26 kN.
4. **Inlet area**, from $\dot m = \rho V A$:
   $$
   \begin{aligned}
   A &= \frac{\dot m}{\rho_\infty V_\infty}\\
     &= \frac{45}{0.2265 \times 750}\\
     &= 0.2649\ \text{m}^2
   \end{aligned}
   $$

**Check.** The exhaust leaves faster than the air arrives, so the thrust is positive. The nozzle is slightly underexpanded ($p_e > p_\infty$), and the pressure term adds a little.

Specific impulse keeps its definition, $F/(\dot m g_0)$. On the air flow, the ramjet of worked example 3 gives $23{,}265/(45 \times 9.81) = 52.70$ s. Engine makers quote it on the fuel flow alone, which gives a much larger number. [Chapter 5](#p51-available-and-vmax) works with the fuel flow.

:::{warning} Do not leave out $V_\infty$
If you use the rocket form, $\dot m V_e$, for an engine that breathes air, you give the engine credit for the momentum the air already had when it arrived. In worked example 3 that gives $45 \times 1{,}250 + 764.8 = 57{,}015$ N, more than twice the right answer. The air brings in $45 \times 750 = 33{,}750$ N of momentum each second, and the engine must pay it back before it gains anything.
:::

## Summary

:::{important} Summary
- A rocket pushes on its own exhaust, so it works in vacuum. Its thrust is $F = \dot m V_e + (p_e - p_a)A_e$: the momentum thrust plus the pressure thrust, with pressures in pascals.
- The effective exhaust velocity $c = F/\dot m$ and the specific impulse $I_\text{sp} = c/g_0$ (seconds, $g_0$ = 9.81 m/s² everywhere) measure how well an engine uses its propellant; thrust measures how hard it pushes.
- $p_e < p_a$: overexpanded, pressure term negative, plume squeezed in. $p_e > p_a$: underexpanded, pressure term positive, plume spread out. The best nozzle at one ambient pressure gives $p_e = p_a$.
- A larger area ratio $A_e/A_t$ expands the gas further. At sea level there is a best area ratio; in vacuum a larger nozzle always helps. A fixed nozzle gains thrust all the way to vacuum, $F = F_\text{vac} - p_a A_e$. An engine that breathes air counts only the speed it adds, $V_e - V_\infty$.
:::

:::{table} The equations of this page.
:label: tbl-p41-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Thrust from momentum (no pressure term) | $F = \dot m V_e$ |
| Rocket thrust equation | $F = \dot m V_e + (p_e - p_a)A_e$ |
| Effective exhaust velocity | $c = F/\dot m = V_e + (p_e - p_a)A_e/\dot m$ |
| Specific impulse (s; $g_0$ = 9.81 m/s²) | $I_\text{sp} = F/(\dot m g_0) = c/g_0$ |
| Thrust of a fixed nozzle at altitude | $F = F_\text{vac} - p_a A_e$ |
| Engine that breathes air (fuel flow neglected) | $F = \dot m (V_e - V_\infty) + (p_e - p_\infty)A_e$, with $\dot m = \rho V A$ |

:::

:::{exercise} For discussion
:label: ex-p41-discussion

1. A rocket and a ramjet both fly at 750 m/s and throw gas back at 1,250 m/s relative to themselves. Why does the rocket get more thrust per kilogram per second of gas?
2. Why do vacuum engines not use an even larger area ratio than they do, if a larger nozzle always helps in vacuum?
3. A first-stage engine fires from sea level to about 60 km. Would you choose its area ratio for ideal expansion at sea level, at 60 km, or somewhere between? What does each choice cost?
4. The plume of a launch vehicle grows wider and wider as it climbs. What does that tell you about the pressure term of its engines?
5. Two engines have the same thrust; one has twice the specific impulse of the other. What is different about how much propellant each burns in one minute?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-4-1.html
:label: quiz-4-1
:enumerated: false
:width: 100%

Quiz for Standard 4.1: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Biggs, R. E., "Rocketdyne F-1 Saturn V First Stage Engine," in *Remembering the Giants: Apollo Rocket Propulsion Development*, NASA SP-2009-4545, 2009, pp. 17-27. NASA Technical Reports Server 20100027316.
- Huzel, D. K., and Huang, D. H., *Design of Liquid Propellant Rocket Engines*, NASA SP-125, 1967. Section 1.2 (pp. 6, 7, 11, and 15; Eq. 1-20), Tables 1-9 and 1-10, and Section 4.3.
- NASA, "F-1 Engine Fact Sheet," *Saturn V News Reference*, sheet R-1, 1968a.
- NASA, "J-2 Engine Fact Sheet," *Saturn V News Reference*, sheet R-16, 1968b.
- NASA, *Liquid Rocket Engine Nozzles*, NASA SP-8120, 1976. p. 17.
- NASA, *Space Shuttle News Reference*, 1981. p. 2-4. NASA Technical Reports Server 19810022734.
- NASA Glenn Research Center, "[Rocket Thrust](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/rocket-thrust/)," Beginner's Guide to Aeronautics, n.d.a.
- NASA Glenn Research Center, "[Specific Impulse](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/specific-impulse/)," Beginner's Guide to Aeronautics, n.d.b.
- NASA Glenn Research Center, "[Ramjet Propulsion](https://www.grc.nasa.gov/www/K-12/airplane/ramjet.html)," Beginner's Guide to Aeronautics, n.d.c.
- NASA Glenn Research Center, "[Ramjet / Scramjet Thrust](https://www.grc.nasa.gov/WWW/K-12/airplane/ramth.html)," Beginner's Guide to Aeronautics, n.d.d.
- Uri, J., "[95 Years Ago: Goddard's First Liquid-Fueled Rocket](https://www.nasa.gov/history/95-years-ago-goddards-first-liquid-fueled-rocket/)," NASA, 2021.
