---
title: "3.1 Wind Tunnels"
short_title: 3.1 Wind Tunnels
---

:::{include} ../_parts/standards/3.1.md
:::

In Chapter 1 we studied the standard atmosphere and frictionless flow. Now we apply those tools to a low-speed {term}`wind tunnel`, where we measure aerodynamic forces on a stationary model in a moving stream of air. We use continuity, Bernoulli's equation, and the manometer of [page 1.5](../chapter-1/bernoulli-and-pitot-static.md) to find the test-section speed. We then introduce the {term}`viscosity` of air, which creates the {term}`boundary layer` and the {term}`Reynolds number`. That dimensionless number tells us whether the flow around a small model matches the flow around the full-size aircraft.

:::{note} What to take from this page
- A low-speed tunnel speeds the air up in a contraction, tests the model in the narrow test section, and slows the air down again in a diffuser; a fan makes up for the losses.
- Between station 1 (settling chamber) and station 2 (test section), Equation [](#eq-p31-test-section-speed) gives the test-section speed $V_2$ from $p_1 - p_2$ and the contraction ratio. The manometer gives $p_1 - p_2 = \rho_\ell\, g\, \Delta h$. Use the air's density in the speed equation and the liquid's density in the manometer equation.
- The Reynolds number $\textit{Re} = \rho V L/\mu$ compares inertial with viscous forces. On a smooth flat plate the boundary layer turns turbulent near $\textit{Re}_x = 5 \times {10}^{5}$.
- A model experiences the same flow as the full-size aircraft only at the same Reynolds number (and, at high speed, Mach number). Larger, pressurized, and cold tunnels raise a small model's Reynolds number; trip strips put transition where the aircraft has it.
:::

## What a wind tunnel is for

A wind tunnel moves air past a model that stands still. A wing flying at 50 m/s through still air and a wing held fixed in a 50 m/s stream experience the same aerodynamic forces. Only the motion of the air relative to the wing matters.

We measure three things in a tunnel (Leishman 2022, Chapter 71):

- **Forces and moments**, with a {term}`balance`, which uses load cells under the model's support to measure the lift, drag, side force, and moments.
- **Surface pressures**, through small holes in the skin, called pressure taps, piped to pressure sensors.
- **Flow pictures**, from smoke, oil films, tufts of yarn, and lasers, which show where the air goes, where it separates, and how fast it moves.

A tunnel test is less expensive and safer than a flight test, repeats the same conditions day after day, and can run before the aircraft is built. Even so, wind-tunnel testing has three main limitations:

- **Wall blockage.** The tunnel walls constrain the flow around the model. When a model's frontal area exceeds about 5% of the test-section area, the measurements require corrections for this {term}`blockage` (Leishman 2022, Chapter 71).
- **Scale mismatch.** A wind-tunnel model is usually much smaller than the full-size aircraft, which lowers the Reynolds number and can alter how the boundary layer behaves.
- **Support interference.** The strut or sting supporting the model disturbs the airflow around it.

(p31-tunnel-parts)=
## The parts of a low-speed tunnel

The simplest tunnel takes air from the room, passes it once through the test section, and blows it back out. This {term}`open-circuit tunnel <open-circuit wind tunnel>` is also called an Eiffel tunnel, after the French engineer who built an early one in 1909 (Leishman 2022, Chapter 71; NASA Glenn Research Center n.d.b). {numref}`fig-p31-open-circuit` names its parts in the order the air passes through them.

:::{figure} figures/p31-open-circuit.svg
:label: fig-p31-open-circuit
:alt: Side view of an open-circuit wind tunnel with the air entering at the left and leaving at the right. In order: a flared bellmouth inlet; a wide settling chamber holding a honeycomb and three screens; a smoothly narrowing contraction; a short, narrow test section, shaded, with a small airliner model on a support strut; a long diffuser that widens slowly; and a fan with its hub fairing near the exit. The honeycomb is drawn as a block of cell walls that run with the flow, the screens as single lines across it. Numbered circles above the tunnel mark station 1 in the settling chamber, station 2 at the start of the test section, and station 3 at the end of the diffuser.
:width: 90%

Schematic of the open-circuit tunnel of worked example 1, drawn to scale with a 1.2 m square test section and a contraction ratio of 7.5. The air is fastest in the narrow test section, where the model is mounted. The numbered circles are stations 1, 2, and 3 of the equations below.
:::

- **Bellmouth.** A rounded inlet that lets the room air turn into the tunnel without separating from the lip.
- **{term}`Settling chamber`.** The widest and slowest part. A honeycomb of small parallel cells straightens the flow, and fine wire screens break large eddies into small ones that die out quickly.
- **{term}`Contraction`**, also called the nozzle. A smoothly narrowing duct that speeds the air up and evens out the unsteadiness that is left.
- **{term}`Test section`.** The narrowest part, where the speed is highest and the model is mounted, often behind viewing windows.
- **{term}`Diffuser`.** A long duct that widens slowly to slow the air down again. Each wall diverges by less than about 3°; a wider angle makes the air separate from the walls (Leishman 2022, Chapter 71).
- **Fan.** Driven by an electric motor, it pulls the air through and makes up for the pressure lost on the way.

:::{prf:definition} Contraction ratio and tunnel stations
:label: def-p31-contraction-ratio

The **{term}`contraction ratio`** is the cross-section area of the settling chamber divided by that of the test section, $A_1/A_2$. It is typically about 7 (Leishman 2022, Chapter 71).

In these notes we number the tunnel cross sections as **station 1** in the settling chamber (the reservoir), **station 2** in the test section, and **station 3** at the exit of the diffuser.
:::

A {term}`closed-circuit tunnel <closed-circuit wind tunnel>` sends the same air around a loop ({numref}`fig-p31-closed-circuit`). It is also called a Göttingen tunnel, after the German university town where Ludwig Prandtl introduced this layout in 1907 (Leishman 2022, Chapter 71). After the diffuser the air turns four corners, each with a row of curved {term}`turning vanes` that guide it around the bend without separating. The fan is mounted in the return leg, which carries the air, still slowing down, back to the settling chamber.

:::{figure} figures/p31-closed-circuit.svg
:label: fig-p31-closed-circuit
:alt: Plan view, seen from above, of a closed-circuit wind tunnel shaped like a long rectangular loop. The air flows counterclockwise. Along the bottom leg, from left to right, are the settling chamber with honeycomb and screens, the contraction, the shaded test section holding an airliner model, and the diffuser. At the right end the air turns two corners fitted with turning vanes and enters the top leg, the return leg, which holds the fan with its long hub fairing. At the left end two larger corners with turning vanes bring the air back into the settling chamber. Numbered circles below the tunnel mark station 1 in the settling chamber, station 2 in the test section, and station 3 at the end of the diffuser.
:width: 85%

Schematic of a closed-circuit tunnel in plan view, typical proportions. From the settling chamber to the diffuser it matches {numref}`fig-p31-open-circuit`; four corners with turning vanes and a return leg bring the same air back. The fan only has to make up for the losses of one trip around the loop.
:::

{numref}`tbl-p31-open-closed` compares the two designs.

:::{table} Open-circuit and closed-circuit tunnels compared (NASA Glenn Research Center n.d.a, n.d.b; Leishman 2022, Chapter 71).
:label: tbl-p31-open-closed
:align: center

<table>
<tr><th><span class="sr-only">Feature</span></th><th>Open circuit (Eiffel)</th><th>Closed circuit (Göttingen)</th></tr>
<tr><th scope="row">Advantages</th><td>Less expensive to build; smoke and exhaust leave with the air</td><td>Better flow quality; quieter; uses less power to run, since the fan only makes up for losses</td></tr>
<tr><th scope="row">Drawbacks</th><td>Drafts in the room disturb the inlet flow; noisy; uses more power to run, since the fan keeps speeding up new air</td><td>More expensive to build; smoke and exhaust stay in the loop; the air warms up and may need cooling</td></tr>
</table>

:::

We also classify tunnels by the test-section Mach number, which sets how much the air density changes ({numref}`tbl-p31-speed-classes`). On this page we focus on low-speed tunnels, below Mach 0.3, where we can treat the air as incompressible, as on [page 1.5](../chapter-1/bernoulli-and-pitot-static.md).

:::{table} Wind tunnels by the Mach number of the test section (NASA Glenn Research Center n.d.d; Leishman 2022, Chapter 71).
:label: tbl-p31-speed-classes
:align: center

<table>
<tr><th>Kind</th><th>Mach number</th><th>What sets it apart</th></tr>
<tr><th scope="row">Subsonic</th><td class="num">below 0.8</td><td>The test section is the narrowest part; below 0.3 the density barely changes (low-speed tunnels)</td></tr>
<tr><th scope="row">Transonic</th><td class="num">0.8 to 1.2</td><td>Slotted or perforated walls keep shock waves from reflecting back onto the model</td></tr>
<tr><th scope="row">Supersonic</th><td class="num">1.2 to 5</td><td>A converging-diverging nozzle sets the Mach number; often a blowdown tunnel, run for seconds to minutes from tanks of compressed air</td></tr>
<tr><th scope="row">Hypersonic</th><td class="num">above 5</td><td>Heating of the model matters as much as the forces; runs last milliseconds to seconds</td></tr>
</table>

:::

(p31-test-section-speed)=
## Test-section speed from a manometer

A low-speed tunnel works like a large {term}`venturi`, narrowing to a throat (the test section) and widening again (Leishman 2022, Chapter 71). We find the test-section speed the same way we found the throat speed of a venturi on [page 1.5](../chapter-1/bernoulli-and-pitot-static.md), using continuity and Bernoulli's equation.

Two assumptions apply throughout this section:

1. The flow is steady and incompressible. Because the test-section Mach number is below 0.3, $\rho_1 = \rho_2 = \rho$.
2. Between stations 1 and 2 there is no friction and no fan, so Bernoulli's equation applies along the tunnel axis.

**Continuity.** The same volume of air passes stations 1 and 2 each second, $A_1 V_1 = A_2 V_2$ ([continuity, page 1.5](#p15-continuity)). So

$$
V_1 = \frac{A_2}{A_1}\,V_2
$$

The air in the settling chamber moves at $A_2/A_1$ of the test-section speed.

**Bernoulli's equation** between stations 1 and 2 ([Bernoulli's equation, page 1.5](#p15-bernoulli)):

$$
p_1 + \tfrac12 \rho V_1^2 = p_2 + \tfrac12 \rho V_2^2
$$

We collect the pressures on the left:

$$
p_1 - p_2 = \tfrac12 \rho \left(V_2^2 - V_1^2\right)
$$

**Eliminate $V_1$.** We substitute $V_1 = (A_2/A_1)V_2$ and take $V_2^2$ out of the bracket:

$$
p_1 - p_2 = \tfrac12 \rho V_2^2 \left[1 - \left(\frac{A_2}{A_1}\right)^2\right]
$$

**Solve for $V_2$:**

:::{math}
:label: eq-p31-test-section-speed
V_2 = \sqrt{\frac{2\,(p_1 - p_2)}{\rho\left[1 - (A_2/A_1)^2\right]}}
:::

This is the [venturi relation of page 1.5](#eq-p15-venturi), with $\rho$ as the density of the air in the tunnel. Equation [](#eq-p31-test-section-speed) shows three practical points about operating a tunnel:

- **The test-section pressure is lower than the settling-chamber pressure.** Because the air accelerates from station 1 to station 2, Bernoulli's equation requires $p_2 < p_1$.
- **We control the tunnel speed by setting the pressure difference.** Because the contraction ratio is fixed, [](#eq-p31-test-section-speed) links each pressure difference $p_1 - p_2$ to a unique test-section speed. The operator adjusts the fan until the manometer reaches the target difference, using flush wall taps so no probe has to stand ahead of the model and shed a wake over it.
- **The settling-chamber term is small but not zero.** For a contraction ratio of 7.5, $(A_2/A_1)^2 = 0.017778$, so omitting it would change the speed by less than 1%.

**The manometer.** A U-tube {term}`manometer` connected to a pressure tap in the settling-chamber wall and another in the test-section wall reads the pressure difference ({numref}`fig-p31-manometer-tunnel`). The higher pressure, $p_1$, pushes its leg of the liquid down until the two levels differ by $\Delta h$ ([the manometer, page 1.5](#eq-p15-manometer)):

:::{math}
:label: eq-p31-manometer
p_1 - p_2 = \rho_\ell\, g\, \Delta h
:::

Here $\rho_\ell$ is the density of the manometer liquid and $g = 9.81$ m/s², as on page 1.5.

:::{warning} Two densities in one problem
The speed formula [](#eq-p31-test-section-speed) uses the density of **air**, about 1.2 kg/m³. The manometer [](#eq-p31-manometer) uses the density of the **liquid**, hundreds or thousands of times larger. If you swap them, the speed comes out tens of times too small, or the pressure difference hundreds of times too small. Write the subscript every time, using $\rho$ for air and $\rho_\ell$ for the liquid.
:::

**The Mach check.** The incompressible equations apply only below Mach 0.3. With the speed of sound $a_s = \sqrt{\gamma R T}$ ([speed of sound, page 1.4](#p14-speed-of-sound)), that limit is 102.1 m/s at sea level.

:::{tip} Method: test-section speed from a manometer reading
1. Find $p_1 - p_2 = \rho_\ell\, g\, \Delta h$, with the liquid's density and $\Delta h$ in meters.
2. Find the area term $1 - (A_2/A_1)^2$ from the contraction ratio.
3. Find $V_2$ from [](#eq-p31-test-section-speed), with the air's density.
4. Check that the Mach number is below 0.3.

To set a test speed, run the steps backward.
:::

### Worked example 1: a university tunnel

An open-circuit tunnel stands in a laboratory at sea-level standard conditions ($p = 101{,}325$ Pa, $\rho = 1.2250$ kg/m³, and $T = 288.16$ K). Its test section is 1.2 m by 1.2 m ($A_2 = 1.44$ m²) and its contraction ratio is $A_1/A_2 = 7.5$, so $A_1 = 10.8$ m². A U-tube manometer filled with an oil of density $\rho_\ell = 830$ kg/m³, connected between the settling chamber and the test section, reads $\Delta h = 20.0$ cm. Find the test-section speed, the settling-chamber speed, the Mach number, the dynamic pressure, and the static pressures $p_1$ and $p_2$ ({numref}`fig-p31-manometer-tunnel`).

1. **Pressure difference**, [](#eq-p31-manometer), with the oil's density and $\Delta h = 0.200$ m:
   $$
   \begin{aligned}
   p_1 - p_2 &= \rho_\ell\, g\, \Delta h\\
             &= 830 \times 9.81\\
             &\;\;\; \times 0.200\\
             &= 1{,}628.46\ \text{Pa}
   \end{aligned}
   $$
2. **Area term.**
   $$
   \begin{aligned}
   \left(\frac{A_2}{A_1}\right)^2 &= \left(\frac{1}{7.5}\right)^2\\
     &= 0.017778\\
   1 - 0.017778 &= 0.98222
   \end{aligned}
   $$
3. **Test-section speed**, [](#eq-p31-test-section-speed), with the air's density:
   $$
   \begin{aligned}
   V_2 &= \sqrt{\frac{2 \times 1{,}628.46}{1.2250 \times 0.98222}}\\
       &= 52.027\ \text{m/s}
   \end{aligned}
   $$
4. **Settling-chamber speed**, from continuity:
   $$
   \begin{aligned}
   V_1 &= \frac{V_2}{A_1/A_2} = \frac{52.027}{7.5}\\
       &= 6.937\ \text{m/s}
   \end{aligned}
   $$
5. **Mach check.** At 288.16 K the speed of sound is $a_s = 340.3$ m/s, so
   $$
   \begin{aligned}
   M_2 &= \frac{52.027}{340.3}\\
       &= 0.1529
   \end{aligned}
   $$
   which is below 0.3, so the incompressible assumption is valid.
6. **Dynamic pressure in the test section:**
   $$
   \begin{aligned}
   q_2 &= \tfrac12 \rho V_2^2\\
       &= 0.5 \times 1.2250\\
       &\;\;\; \times {52.027}^{2}\\
       &= 1{,}657.9\ \text{Pa}
   \end{aligned}
   $$
7. **Static pressures.** The air starts at rest in the room, at $p_\text{room} = 101{,}325$ Pa. We neglect the small loss through the bellmouth, the honeycomb, and the screens, so the total pressure in the settling chamber is still $101{,}325$ Pa. By Bernoulli's equation,
   $$
   \begin{aligned}
   \tfrac12 \rho V_1^2 &= 0.5 \times 1.2250\\
                       &\;\;\; \times {6.937}^{2}\\
                       &= 29.47\ \text{Pa}\\
   p_1 &= p_\text{room} - \tfrac12 \rho V_1^2\\
       &= 101{,}325 - 29.47\\
       &= 101{,}295.53\ \text{Pa}
   \end{aligned}
   $$
   and in the test section
   $$
   \begin{aligned}
   p_2 &= p_1 - (p_1 - p_2)\\
       &= 101{,}295.53 - 1{,}628.46\\
       &= 99{,}667.1\ \text{Pa}
   \end{aligned}
   $$

**Check.** The room pressure minus the test-section pressure, $101{,}325 - 99{,}667.1 = 1{,}657.9$ Pa, equals $q_2$, as it must when no loss is counted ahead of the test section. The test-section pressure is only 1.6% below room pressure, which is why we read it with a manometer and not a barometer.

:::{figure} figures/p31-manometer-tunnel.svg
:label: fig-p31-manometer-tunnel
:alt: The front part of the open-circuit tunnel of worked example 1, from the bellmouth to the shaded test section. A pressure tap in the lower wall of the settling chamber, at station 1, and another in the lower wall of the test section, at station 2, are connected by tubes to the two legs of a U-tube manometer below the tunnel, drawn at five times the tunnel's scale. The oil, of density 830 kilograms per cubic meter, stands lower in the leg connected to station 1, where the pressure is higher, and higher in the leg connected to station 2. The height difference is labeled delta h equals 20.0 centimeters, p1 minus p2 equals 1,628.5 pascals, and the test section is labeled V2 equals 52.03 meters per second. The test section ends in a break line: the tunnel goes on.
:width: 80%

Computed for worked example 1. The tunnel is to scale; the manometer is enlarged 5 times so that the oil columns can be read. The higher pressure $p_1$ of the slow air in the settling chamber pushes its leg of oil down; $\Delta h$ measures $p_1 - p_2$.
:::

### Setting a test speed

Often a test calls for a speed, and we need the manometer reading that gives it. We run the same two equations backward, as in the [cooling-air duct of page 1.5](#p15-example-duct). Suppose a test in the tunnel of worked example 1 calls for $V_2 = 40$ m/s.

1. **Pressure difference**, from [](#eq-p31-test-section-speed) solved for $p_1 - p_2$, with the air's density:
   $$
   \begin{aligned}
   p_1 - p_2 &= \tfrac12 \rho V_2^2\\
             &\;\;\; \times \left[1 - \left(\frac{A_2}{A_1}\right)^2\right]\\
             &= 0.5 \times 1.2250\\
             &\;\;\; \times {40}^{2} \times 0.98222\\
             &= 962.6\ \text{Pa}
   \end{aligned}
   $$
2. **Reading**, from [](#eq-p31-manometer) solved for $\Delta h$, with the oil's density:
   $$
   \begin{aligned}
   \Delta h &= \frac{p_1 - p_2}{\rho_\ell\, g}\\
             &= \frac{962.6}{830 \times 9.81}\\
             &= 0.1182\ \text{m}
   \end{aligned}
   $$
   or 11.82 cm of oil.

**Check.** The reading grows with the square of the speed, giving $(40/52.027)^2 \times 20.0 = 11.82$ cm.

### The pressure along the tunnel

{numref}`fig-p31-pressure-along-tunnel` follows the air of worked example 1 from the settling chamber to the end of the diffuser, with the speed from continuity and the static pressure from Bernoulli's equation. The speed peaks where the static pressure dips, in the test section.

A wind tunnel needs a diffuser to slow the airflow back down after the test section, recovering most of the static pressure and reducing the power the fan must supply. In this diffuser, the area grows to 2.546 times the test-section area at station 3, so the speed falls to 20.43 m/s and the static pressure rises. With no losses, the static pressure there would be 255.8 Pa below room pressure, equal to the remaining dynamic pressure at that speed. In a real tunnel the air loses mechanical energy to the honeycomb and screens, wall friction, model drag, and, in a closed circuit, the turning vanes, so its {term}`total pressure` falls. Worked example 1 neglects the small loss ahead of the test section. Downstream of the model, the figure assumes a loss of 10% of the test-section dynamic pressure, 165.8 Pa, which leaves the static pressure at station 3 at 421.6 Pa below room pressure.

This loss is why even a closed-circuit tunnel needs a fan. The air returns to the settling chamber with less total pressure than it had when it left. In an open circuit the fan raises the air from $p_3$ back to room pressure, and in a closed circuit it replaces the losses of one trip around the loop (Leishman 2022, Chapter 71).

:::{figure} figures/p31-pressure-along-tunnel.svg
:label: fig-p31-pressure-along-tunnel
:alt: Three stacked panels sharing one horizontal axis, the distance along the tunnel from 1 to 18 meters. Top: the side outline of the tunnel of worked example 1 from the settling chamber to the end of the diffuser, stations 1, 2, and 3 marked. Middle: the speed, flat at 6.937 meters per second in the settling chamber, rising through the contraction to 52.03 meters per second in the test section, then falling through the diffuser to 20.43 meters per second at station 3. Bottom: pressures relative to the room. The total pressure stays at zero to the model and then falls slowly to minus 165.8 pascals at station 3, marked as the assumed loss, 10 percent of q2. The static pressure is minus 29.47 pascals at station 1, dips to minus 1,658 pascals in the test section, and recovers to minus 421.6 pascals at station 3.
:width: 80%

Computed for worked example 1, with an assumed total-pressure loss of 10% of $q_2$ from the model to station 3; no loss is counted ahead of the model. The diffuser turns most of the speed back into pressure; the fan restores the rest.
:::

## Viscosity, laminar and turbulent flow

So far we have treated air as if it moved past surfaces without friction. Real air is viscous, which means its layers resist sliding past one another. That internal resistance explains skin-friction drag, wing stall, and why a small wind-tunnel model can behave differently from a full-size aircraft.

### Viscosity

Honey flows slowly because its layers resist sliding over one another; that resistance is the fluid's **{term}`viscosity`**. Picture a fluid between a fixed plate and a plate that slides parallel to it. The layer touching each plate moves with it, and each layer in between slides a little over the next. Each layer pulls on its neighbors with a {term}`shear stress` $\tau$ (a force per unit area, in Pa). That stress is proportional to how fast the speed changes across the layers (NASA Glenn Research Center n.d.e):

:::{math}
:label: eq-p31-shear
\tau = \mu\, \frac{du}{dy}
:::

Here $u$ is the speed of the fluid parallel to the plates, $y$ the distance across them, and $\mu$ the **dynamic viscosity**, in kg/(m s), the same as Pa s. Air at sea level has $\mu = 1.789 \times {10}^{-5}$ kg/(m s) (Leishman 2022, Chapter 13). The viscosity divided by the density is the **{term}`kinematic viscosity`** $\nu = \mu/\rho$, in m²/s; for sea-level air $\nu = 1.460 \times {10}^{-5}$ m²/s.

The viscosity of air depends on its temperature and hardly at all on its pressure. We compute it from Sutherland's law (Leishman 2022, Chapter 15):

:::{math}
:label: eq-p31-sutherland
\mu = \frac{1.458 \times {10}^{-6}\; T^{3/2}}{T + 110.4}
:::

with $T$ in kelvin and $\mu$ in kg/(m s). Both constants are fitted to measurements; 110.4 K is Sutherland's constant. {numref}`fig-p31-viscosity` compares the law with the table of the U.S. Standard Atmosphere, which gives $1.4216$ to $1.9421 \times {10}^{-5}$ kg/(m s) from 216.65 K to 320.65 K.

:::{figure} figures/p31-viscosity.svg
:label: fig-p31-viscosity
:alt: Plot of the viscosity of air, in units of ten to the minus five kilograms per meter-second, against temperature from 200 to 400 kelvin. Sutherland's law is a gently curving line that rises from about 1.33 at 200 kelvin to about 2.29 at 400 kelvin. Four open squares from the U.S. Standard Atmosphere table, at 216.65, 255.65, 288.15, and 320.65 kelvin, lie on the line. The sea-level value, 1.789 times ten to the minus five at 288.16 kelvin, is labeled, and the square at 216.65 kelvin is labeled 11 kilometers.
:width: 80%

Computed from Sutherland's law, [](#eq-p31-sutherland), with the table values of the U.S. Standard Atmosphere, 1976 (Table III) as squares. The viscosity of air rises with temperature, the opposite of a liquid's, so air at 11 km is less viscous than air at sea level.
:::

Notice that warm air is more viscous than cold air, the opposite of liquids such as honey or oil. As a gas warms, its faster molecules transfer more momentum between neighboring layers, which increases its internal shear resistance. In a liquid, warming weakens the bonds between molecules and lowers viscosity (Leishman 2022, Chapter 13). For this reason, the cold air at a cruise altitude of 11 km is less viscous than sea-level air.

### The no-slip condition and the boundary layer

Air touching a surface sticks to it, so the air speed at the wall is zero. This is the **{term}`no-slip condition`** (NASA Glenn Research Center n.d.c). A short distance away it moves at the free-stream speed, $V_\infty$. The thin layer in between, where the speed rises from zero to $V_\infty$, is the **{term}`boundary layer`** ({numref}`fig-p31-boundary-layer`). We take its thickness $\delta$ as the height where the speed reaches 99% of $V_\infty$ (Leishman 2022, Chapter 26). Inside the layer $du/dy$ is large, and so is the shear stress, [](#eq-p31-shear). Outside it $du/dy$ is nearly zero and the air behaves as if it had no viscosity, which is why Bernoulli's equation works there.

A boundary layer comes in two kinds:

- In a **{term}`laminar <laminar flow>`** boundary layer the air moves in smooth layers that slide over one another without mixing, like the cards in a deck.
- In a **{term}`turbulent <turbulent flow>`** boundary layer the air tumbles in eddies that mix fast air from outside down toward the wall. The speed near the wall is higher, so the wall shear stress and the skin-friction drag are higher, and the layer is thicker.

The change from one to the other is **{term}`transition`**. On a smooth flat plate the layer starts laminar at the leading edge, grows thicker downstream, and turns turbulent over a short distance ({numref}`fig-p31-boundary-layer`).

:::{figure} figures/p31-boundary-layer.svg
:label: fig-p31-boundary-layer
:alt: A flat plate seen edge-on with air flowing from the left at the free-stream speed V infinity. A dashed line, the boundary-layer edge, rises from the leading edge: slowly over the laminar part, then faster from the start of a bracketed transition zone. Four velocity profiles are drawn, each starting from zero at a dot on the wall and reaching the free-stream speed at the edge, with arrows inside that grow with height: two on each laminar profile, four on each turbulent one. The two laminar profiles near the leading edge are thin and curve smoothly. The two turbulent profiles downstream are several times thicker and are full almost down to the wall, where they fall steeply to zero. Braces under the plate name the laminar layer, the transition zone, and the turbulent layer. The thickness delta is dimensioned at the last profile, and a callout points to the wall dot of the first laminar profile: no slip, u equals zero at the wall.
:width: 85%

Computed for a smooth flat plate, with laminar profiles from the Blasius solution, turbulent ones from the one-seventh power law, and transition placed where $\textit{Re}_x$ reaches $5 \times {10}^{5}$. The speed is zero at the wall in both layers; the turbulent layer is several times thicker and fuller near the wall. Heights are drawn 23 times their true size. Across the transition zone the edge is blended from the laminar to the turbulent thickness; next to the wall the turbulent profiles are drawn leaving it at a finite slope.
:::

For a smooth flat plate with constant pressure along its length, both boundary-layer thicknesses have standard relations. With $x$ the distance from the leading edge and $\textit{Re}_x = \rho V x/\mu$, a Reynolds number based on $x$ (the next section explains it), the laminar layer of the Blasius solution has

:::{math}
:label: eq-p31-delta-laminar
\delta \approx \frac{5.0\,x}{\sqrt{\textit{Re}_x}}
:::

and a layer turbulent from the leading edge, with the empirical one-seventh power law profile $u/V_\infty = (y/\delta)^{1/7}$, has (Leishman 2022, Chapter 26)

:::{math}
:label: eq-p31-delta-turbulent
\delta \approx \frac{0.37\,x}{\textit{Re}_x^{1/5}}
:::

You will derive both relations in a later aerodynamics course on boundary-layer theory; we use the laminar relation in worked example 2.

**Separation and the wake.** Where the pressure rises along a surface, as over the rear of a wing at a high {term}`angle of attack`, the slow air near the wall can slow to a stop and reverse direction. The boundary layer then leaves the surface, so the flow **{term}`separates <flow separation>`**, and a region of slow, swirling air called the **{term}`wake`** forms behind the body (NASA Glenn Research Center n.d.c; Leishman 2022, Chapter 26). Separation changes the effective shape of the body, adds pressure drag, and on a wing causes the {term}`stall`. A turbulent layer, with fast air mixed down to the wall, stays attached longer against a rising pressure than a laminar one.

(p31-reynolds-number)=
## The Reynolds number

To tell whether a boundary layer is laminar or turbulent, and where it separates, we use one number that compares the forces in the flow.

:::{prf:definition} Reynolds number
:label: def-p31-reynolds-number

The **{term}`Reynolds number`** of a flow is

$$
\textit{Re} = \frac{\rho\,V L}{\mu} = \frac{V L}{\nu}
$$

where $\rho$ is the density of the fluid, $V$ is its speed relative to the body, $\mu$ is its dynamic viscosity, $\nu$ is its kinematic viscosity, and $L$ is a **characteristic length** of the body (such as the chord of a wing, the length of a fuselage or a hull, or the diameter of a pipe). It has no units. When a Reynolds number is quoted, the length it uses must be named (Leishman 2022, Chapter 18).
:::

The Reynolds number is the ratio of inertial to viscous forces in a flow (NASA Glenn Research Center n.d.c). Inertia resists changes in a fluid element's motion, scaling with the dynamic pressure $\rho V^2$, while viscous shear stress from [](#eq-p31-shear) scales with $\mu V/L$. Taking their ratio gives $\rho V^2/(\mu V/L) = \rho V L/\mu$. When the Reynolds number is low, viscous forces dominate and internal friction damps out motion quickly. When the Reynolds number is high, inertial forces dominate, viscous effects are confined to thin boundary layers near the surface, and the flow readily turns turbulent.

The Reynolds numbers we encounter in fluid mechanics span more than twelve powers of ten ({numref}`fig-p31-reynolds-ladder`). A bacterium about 1 µm long swimming at 30 µm/s in water, whose kinematic viscosity is about ${10}^{-6}$ m²/s, has $\textit{Re} = 3 \times {10}^{-5}$. A goldfish is near ${10}^{2}$ and a person swimming near ${10}^{4}$ (Purcell 1977). Model aircraft and small drones fly at ${10}^{3}$ to ${10}^{5}$ (Leishman 2022, Chapter 18). Take a jet airliner wing with a mean chord of 2.75 m, at Mach 0.82 and 30,000 ft in the standard atmosphere of [page 1.4](../chapter-1/standard-atmosphere.md). Based on its chord, it has $\textit{Re} = 2.105 \times {10}^{7}$ (after Leishman 2022, Chapter 18).

:::{figure} figures/p31-reynolds-ladder.svg
:label: fig-p31-reynolds-ladder
:alt: A horizontal scale of Reynolds number from ten to the minus six at the left to ten to the nine at the right, one power of ten per tick. Flows in water are below the axis with open markers: a swimming bacterium at 3 times ten to the minus five, a goldfish at about one hundred, a person swimming at about ten thousand. Flows in air are above it with filled markers: a bracket for model aircraft and small drones from one thousand to one hundred thousand; the airship model of worked example 2 at 3.563 million; an airliner wing in cruise at 21.05 million; and the full-size airship at 128.4 million. A dashed line at 500,000 marks flat-plate transition. A bracket under the axis between the airship model and the full-size airship is labeled 36 times.
:width: 85%

Reynolds numbers of real flows on one logarithmic scale, each based on the body's length or chord. Values come from Purcell (1977) and Leishman (2022, Chapter 18), with the airship and its model from worked example 2. The tunnel model lies a factor of 36 below the full-size aircraft it represents.
:::

### Where a boundary layer turns turbulent

For a boundary layer the length that matters is the distance $x$ from the leading edge, so we use the local Reynolds number $\textit{Re}_x = \rho V x/\mu$. On a smooth flat plate in a quiet stream, transition begins near

:::{math}
:label: eq-p31-transition
\textit{Re}_{x,\text{tr}} \approx 5 \times {10}^{5}
:::

This value is only a guide. Surface roughness, turbulence in the oncoming air, noise, vibration, and a pressure rising along the surface all bring transition earlier. An unusually smooth surface in quiet air can delay it (Leishman 2022, Chapters 18 and 26).

We set $\textit{Re}_x$ equal to the transition value and solve for $x$ to find where transition occurs on a surface:

:::{math}
:label: eq-p31-xtr
x_\text{tr} = \frac{\textit{Re}_{x,\text{tr}}\, \mu}{\rho\, V}
:::

The faster the flow, the closer transition comes to the leading edge. A surface shorter than $x_\text{tr}$ stays laminar from end to end; one much longer is turbulent over almost all its length.

:::{warning} Which length, and which units
A wing's chord, a hull length, and the distance $x$ along a plate give different Reynolds numbers for the same flow. Use the length the problem calls for, in meters, with the viscosity in kg/(m s) and the density in kg/m³. If you put a chord in centimeters, the answer is off by a factor of 100. If you use $\nu$ where $\mu$ belongs, it is off by a factor of 1.2 at sea level. Either mistake can lead you to classify a turbulent boundary layer as laminar, or the reverse.
:::

(p31-scale-models)=
## Scale models and similarity

A model gives the right answer for the aircraft only if the flow around it is a scaled copy of the flow around the aircraft. Two conditions make that so (Leishman 2022, Chapter 71):

- **{term}`Geometric similarity <geometric similarity>`.** The model has the exact shape of the aircraft, with every length scaled by the same factor and every angle unchanged.
- **{term}`Dynamic similarity <dynamic similarity>`.** The ratios of the forces in the flow are the same. For low-speed flow this means the same Reynolds number; at high speed the Mach number must match too.

When both conditions are satisfied, the pressure distribution, boundary layers, transition, and separation are scaled copies, and the force coefficients measured on the model ([page 3.2](#p32-coefficients) defines them) apply to the aircraft.

Matching the Reynolds number is difficult because a wind-tunnel model is much smaller than the full-size aircraft. At the same airspeed and air properties, a 1/50-scale model has only 1/50 of the aircraft's Reynolds number. If you try to compensate with airspeed alone, the model needs 50 times the speed, which exceeds a low-speed tunnel's capability and pushes the Mach number into a different flow regime. In air at room conditions, a small model cannot match both Reynolds number and Mach number at once (Leishman 2022, Chapter 71).

### Worked example 2: an airship model

An airship 75 m long, with a hull diameter of 18 m, cruises at 25 m/s near sea level (invented values, typical of a large airship). A model built at 1:75 scale, 1.0 m long and 0.24 m in diameter, is tested in the tunnel of worked example 1 at $V_2 = 52.03$ m/s. Take sea-level standard air for both, $\rho = 1.2250$ kg/m³ and $\mu = 1.789 \times {10}^{-5}$ kg/(m s), and the hull length as the characteristic length. Find the Reynolds numbers of the airship and of the model, the speed the model would need to match the airship, where transition occurs on each, the boundary-layer thickness on the model, and the blockage of the test section.

1. **Full-size Reynolds number:**
   $$
   \begin{aligned}
   \textit{Re}_\text{full} &= \frac{\rho V L}{\mu}\\
     &= \frac{1.2250 \times 25 \times 75}{1.789 \times {10}^{-5}}\\
     &= 1.284 \times {10}^{8}
   \end{aligned}
   $$
2. **Model Reynolds number**, with $L = 1.0$ m:
   $$
   \begin{aligned}
   &\textit{Re}_\text{model}\\
   &\;\;\;= \frac{1.2250 \times 52.027 \times 1.0}{1.789 \times {10}^{-5}}\\
   &\;\;\;= 3.563 \times {10}^{6}
   \end{aligned}
   $$
   The model's Reynolds number is $1.284 \times {10}^{8}/(3.563 \times {10}^{6}) = 36.04$ times too small.
3. **Speed for a match.** Solving $\textit{Re} = \rho V L/\mu$ for $V$ with the model's length gives $V = \textit{Re}_\text{full}\,\mu/(\rho\, L_\text{model})$. With the same air for both, $\rho$ and $\mu$ cancel, and the speed is the airship's speed times the length ratio:
   $$
   \begin{aligned}
   V &= V_\text{full}\,\frac{L_\text{full}}{L_\text{model}}\\
     &= 25 \times \frac{75}{1.0}\\
     &= 1{,}875\ \text{m/s}
   \end{aligned}
   $$
   Its Mach number would be $1{,}875/340.3 = 5.510$, a hypersonic flow. The low-speed tunnel cannot reach it, and even if it could, compressibility would make the flow unlike the airship's.
4. **Transition on the model**, [](#eq-p31-xtr) with the flat-plate guide. The numerator is $\textit{Re}_{x,\text{tr}}\,\mu = 5 \times {10}^{5} \times 1.789 \times {10}^{-5} = 8.945$ kg/(m s), so
   $$
   \begin{aligned}
   x_\text{tr} &= \frac{8.945}{1.2250 \times 52.027}\\
               &= 0.1404\ \text{m}
   \end{aligned}
   $$
   or 14.04% of the model's length.
5. **Transition on the airship:**
   $$
   \begin{aligned}
   x_\text{tr} &= \frac{8.945}{1.2250 \times 25}\\
               &= 0.29208\ \text{m}
   \end{aligned}
   $$
   and $0.29208/75 = 0.0038944$, or 0.3894% of the hull. The airship's boundary layer is turbulent over almost all its length.
6. **Boundary-layer thickness on the model.** At the start of transition, $x = 0.14035$ m and $\textit{Re}_x = 5 \times {10}^{5}$, so [](#eq-p31-delta-laminar) gives
   $$
   \begin{aligned}
   \delta &= \frac{5.0 \times 0.14035}{\sqrt{5 \times {10}^{5}}}\\
          &= \frac{0.70175}{707.1}\\
          &= 0.0009924\ \text{m}
   \end{aligned}
   $$
   or 0.9924 mm, thin beside the 0.24 m hull.

**Check.** The Reynolds number scales with $V L$. Because the model has 1/75 of the length and 2.08 times the speed, its Reynolds number is $75/2.08 = 36$ times smaller, as we found. Steps 4 and 5 show the real problem. A laminar layer covers 14.04% of the model's length, its first seventh, but only 0.3894% of the airship's. So the model's skin-friction drag and the point where its flow separates near the tail would not match the airship's. The model's frontal area, $\pi (0.24)^2/4 = 0.04524$ m², blocks 3.142% of the 1.44 m² test section, below the 5% guide.

You can see the same scaling problem for any model size in {numref}`fig-p31-scale-speed`.

:::{figure} figures/p31-scale-speed.svg
:label: fig-p31-scale-speed
:alt: Log-log plot of the speed needed to match the full-size airship's Reynolds number against model length, from 0.5 meters up to the airship's own 75 meters. The required speed is a straight falling line: 1,875 meters per second for the one-meter 1 to 75 model, marked as Mach 5.51, down to 25 meters per second for the full-size 75-meter airship. A dashed horizontal line marks Mach 0.3 at 102.1 meters per second and a dotted line marks Mach 1 at 340.3 meters per second. The line crosses Mach 0.3 for a model 18.4 meters long.
:width: 85%

Computed for worked example 2, in sea-level air. The speed needed grows in proportion to the scale factor. The 1.0 m model would need Mach 5.51. Only a model at least 18.4 m long could match the airship's Reynolds number at Mach 0.3, the top of the low-speed range, and only the largest tunnels could fit it.
:::

### Closing the Reynolds-number gap

Engineers have four ways to raise a model's Reynolds number or make up for the gap (Leishman 2022, Chapter 71):

1. **A bigger tunnel and a bigger model.** The Reynolds number grows with the length. The largest tunnels test full-size aircraft at low speed.
2. **A pressurized tunnel.** Raising the pressure at a fixed temperature raises the density, and the Reynolds number with it, at the same speed. The NACA Variable Density Tunnel, running from 1922 at up to 20 atmospheres, produced the airfoil data used to design aircraft such as the Douglas DC-3 (Leishman 2022, Chapter 71). The airship model of worked example 2 would need a density 36.04 times that of sea-level air, more than even that tunnel could give.
3. **A cryogenic tunnel.** Cooling the gas lowers its viscosity ({numref}`fig-p31-viscosity`) and, at a fixed pressure, raises its density; both raise $\textit{Re}$. NASA's National Transonic Facility, the largest pressurized cryogenic tunnel, runs on nitrogen as cold as 250 °F below zero to reach flight Reynolds numbers at transonic speeds (NASA Langley Research Center n.d.).
4. **{term}`Trip strips <trip strip>`.** When the tunnel cannot match the flight Reynolds number, we can glue a thin strip of roughness, such as grit or small bumps, near the model's nose or leading edge. That strip forces transition at the same relative location as on the full-size aircraft, giving the model a turbulent boundary layer over the same fraction of its surface. To place the strip accurately, you still need to know beforehand where transition occurs at full scale.

## Summary

:::{important} Summary
- A low-speed tunnel has a settling chamber with honeycomb and screens, a contraction, the test section, a diffuser, and a fan. A closed circuit adds corners with turning vanes and a return leg.
- Continuity and Bernoulli's equation give the test-section speed $V_2$ from $p_1 - p_2$ and the contraction ratio, Equation [](#eq-p31-test-section-speed). The manometer gives $p_1 - p_2 = \rho_\ell\, g\, \Delta h$. The test-section pressure is the lowest in the tunnel; losses keep the diffuser from recovering all of it.
- Viscosity, which in air rises with temperature, creates a thin boundary layer that turns turbulent near $\textit{Re}_x = 5 \times {10}^{5}$ on a smooth plate. A small model in a low-speed tunnel falls short of the aircraft's Reynolds number $\rho V L/\mu$. Larger, pressurized, and cryogenic tunnels raise it, and trip strips put transition where the aircraft has it.
:::

:::{table} The equations of this page.
:label: tbl-p31-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Continuity, tunnel stations | $A_1 V_1 = A_2 V_2$ |
| Bernoulli's equation, stations 1 and 2 | $p_1 + \tfrac12 \rho V_1^2 = p_2 + \tfrac12 \rho V_2^2$ |
| Test-section speed (density of the air) | $V_2 = \sqrt{2(p_1 - p_2)/(\rho[1 - (A_2/A_1)^2])}$ |
| Manometer (density of the liquid) | $p_1 - p_2 = \rho_\ell\, g\, \Delta h$ |
| Shear stress in a fluid | $\tau = \mu\, du/dy$ |
| Kinematic viscosity | $\nu = \mu/\rho$ |
| Sutherland's law, SI units | $\mu = 1.458 \times {10}^{-6}\, T^{3/2}/(T + 110.4)$ |
| Reynolds number | $\textit{Re} = \rho V L/\mu = VL/\nu$ |
| Flat-plate transition, a guide | $\textit{Re}_{x,\text{tr}} \approx 5 \times {10}^{5}$ |
| Transition location | $x_\text{tr} = \textit{Re}_{x,\text{tr}}\,\mu/(\rho V)$ |
| Boundary-layer thickness, laminar | $\delta \approx 5.0\,x/\sqrt{\textit{Re}_x}$ |
| Boundary-layer thickness, turbulent | $\delta \approx 0.37\,x/\textit{Re}_x^{1/5}$ |

:::

:::{exercise} For discussion
:label: ex-p31-discussion

1. Why is the test section the narrowest part of a low-speed tunnel? What would go wrong if the model were placed in the settling chamber instead?
2. A student fills the manometer of worked example 1 with water instead of oil. Does the tunnel's speed change? What does change, and in which direction?
3. Air near a hot engine exhaust and air at a high cruise altitude differ in viscosity. Which is more viscous, and what does that do to the Reynolds number of a wing flying through each at the same speed and density?
4. An engineer argues that a 1:20 model tested at 20 times the full-size speed matches the Reynolds number, so the test is valid. What has the engineer forgotten?
5. Why must the engineers already know where transition occurs on the aircraft before they place trip strips on its model?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-3-1.html
:label: quiz-3-1
:enumerated: false
:width: 100%

Quiz for Standard 3.1: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Leishman, J. G., *[Introduction to Aerospace Flight Vehicles](https://eaglepubs.erau.edu/introductiontoaerospaceflightvehicles/)*, Embry-Riddle Aeronautical University, 2022 (online edition). Chapters 13, "Fundamental Properties of Fluids"; 15, "Atmospheric Properties"; 18, "Mach Number & Reynolds Number"; 26, "Boundary Layer Flows"; 71, "Wind Tunnel Testing." DOI 10.15394/eaglepub.2022.1066.
- NASA Glenn Research Center, "[Closed Return Wind Tunnel](https://www.grc.nasa.gov/www/k-12/airplane/tuncret.html)," Beginner's Guide to Aeronautics, n.d.a.
- NASA Glenn Research Center, "[Open Return Wind Tunnel](https://www.grc.nasa.gov/www/k-12/airplane/tunoret.html)," Beginner's Guide to Aeronautics, n.d.b.
- NASA Glenn Research Center, "[Reynolds Number](https://www.grc.nasa.gov/www/k-12/airplane/reynolds.html)," Beginner's Guide to Aeronautics, n.d.c.
- NASA Glenn Research Center, "[Types of Wind Tunnels](https://www.grc.nasa.gov/www/k-12/airplane/tuntype.html)," Beginner's Guide to Aeronautics, n.d.d.
- NASA Glenn Research Center, "[Viscosity](https://www.grc.nasa.gov/www/k-12/airplane/viscosity.html)," Beginner's Guide to Aeronautics, n.d.e.
- NASA Langley Research Center, "[National Transonic Facility](https://commonresearchmodel.larc.nasa.gov/home-2/high-speed-crm/experimental-approach/facilities/ntf/)," NASA Common Research Model, n.d.
- NOAA, NASA, and U.S. Air Force, *[U.S. Standard Atmosphere, 1976](https://ntrs.nasa.gov/citations/19770009539)*, NOAA-S/T 76-1562, NASA-TM-X-74335, 1976. Table III (dynamic viscosity).
- Purcell, E. M., "Life at Low Reynolds Number," *American Journal of Physics*, Vol. 45, No. 1, 1977, pp. 3 to 11. DOI 10.1119/1.10903.
