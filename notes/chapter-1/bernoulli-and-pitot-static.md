---
title: "1.5 Bernoulli and Pitot Static"
short_title: 1.5 Bernoulli and Pitot Static
---

:::{include} ../_parts/standards/1.5.md
:::

Air that moves past a vehicle pushes on it, and the push depends on how fast the air moves. This page builds the two equations that connect speed and pressure in a moving fluid. The {term}`continuity equation` says that mass is neither created nor lost as a fluid flows. {term}`Bernoulli's equation` says that where the fluid speeds up, its pressure falls. Both are derived from first-year physics, then applied to a duct, a manometer, a draining tank, and the instrument every aircraft uses to measure its airspeed: the {term}`pitot tube` and the {term}`static port`. By the end you can find speeds and pressures in a low-speed flow, turn a pressure reading into an airspeed, and reason out what each flight instrument shows when one of its openings is blocked.

:::{note} What to take from this page
- In steady flow the mass flow $\dot{m} = \rho A V$ is the same at every cross section of a duct or a stream tube. For a liquid or slow air, $A_1 V_1 = A_2 V_2$: a narrower passage means faster flow.
- Along a streamline of steady, incompressible flow without friction, $p + \tfrac12 \rho V^2$ (plus $\rho g z$ for a liquid) stays constant: where the speed rises, the pressure falls.
- A pitot-static tube measures the total pressure $p_0$ at its nose and the static pressure $p$ at its side holes; the airspeed is $V = \sqrt{2(p_0 - p)/\rho}$, with the density of the air around the aircraft.
- A blockage traps a pressure. The instrument then reads wrong in a way you can predict: find the trapped pressure, then follow how the outside pressure changes in a climb or a descent.
:::

## Velocity, streamlines, and aerodynamic forces

A flowing gas is described point by point. At each point it has a pressure $p$, a density $\rho$, and a temperature $T$, the three properties defined on the [standard atmosphere page](standard-atmosphere.md), and a fourth, the velocity $\mathbf{V}$. Together, these four quantities at every point make up the flow field.

The velocity at a point B is the velocity of a tiny piece of fluid, a fluid element, at the moment it passes through B. It can differ from one point to the next, in size and in direction. Far ahead of a vehicle the air is undisturbed; its velocity relative to the vehicle is the {term}`free-stream velocity` $V_\infty$. A vehicle moving through still air feels the same forces as a vehicle at rest in moving air, so these notes picture the vehicle at rest with the air flowing past it.

:::{prf:definition} Steady flow, streamline, stream tube
:label: def-p15-streamline

A flow is **{term}`steady <steady flow>`** when nothing at a fixed point changes with time: the pressure, density, temperature, and velocity at each point stay the same.

In steady flow every fluid element that passes a given point follows the same fixed path. That path is a **{term}`streamline`**. At each point the velocity is tangent to the streamline through that point, so fluid never crosses a streamline.

A **{term}`stream tube`** is the bundle of streamlines that pass through a small closed curve. Because no fluid crosses a streamline, no fluid crosses the wall of a stream tube: it behaves like a pipe with invisible walls.
:::

{numref}`fig-p15-stream-tube` shows the streamlines around an airfoil, the cross-section shape of a wing (its parts are named on [vehicle anatomy](#p13-airfoil)). One stream tube is shaded. Above the airfoil the streamlines crowd together and the tube narrows; the continuity equation, below, shows why that means the air there moves faster.

:::{figure} figures/p15-stream-tube.svg
:label: fig-p15-stream-tube
:alt: Six streamlines run from left to right past an airfoil tilted slightly nose up. Two of them bound a shaded stream tube that passes just above the airfoil. At station 1, ahead of the airfoil, the tube is wide and climbing, and a short velocity arrow along the flow marks the speed V1. At station 2, above the front of the airfoil, the tube is narrower and the velocity arrow V2 is longer. The streamlines far above and below are barely disturbed.
:width: 70%

Computed for ideal flow (no friction) past a cambered airfoil tilted 4° nose up. Where the stream tube narrows, from area $A_1$ to $A_2$, the flow speeds up from $V_1$ to $V_2$. The arrows lie along the local flow and are drawn to one scale: the speed ratio $V_2/V_1$ and the width ratio of the tube are both 1.26.
:::

### Where aerodynamic forces come from

Air acts on a surface in only two ways, shown in {numref}`fig-p15-pressure-and-shear`. Pressure pushes normal to the surface, into it. {term}`Shear stress`, the friction of the air sliding over the surface, drags along it. On a small element of surface of area $\Delta s$, the pressure force is $\Delta F_n = p\,\Delta s$ and the shear force is $\Delta F_t = \tau_w\,\Delta s$, where $\tau_w$ is the shear stress at the wall, in Pa. Added over the whole surface, these small forces give one resultant force $R$. Its part perpendicular to the free stream is the {term}`lift` $L$; its part along the free stream is the {term}`drag` $D$. Pressure and shear both contribute to lift and to drag.

:::{figure} figures/p15-pressure-and-shear.svg
:label: fig-p15-pressure-and-shear
:alt: Left: a small element of a body surface, with the free stream coming from the left. A pressure force arrow pushes straight into the surface and ends at the element; a shear force arrow starts at the element and points along the surface in the direction of the flow. Right: an airfoil tilted slightly nose up in the same free stream. From one point near its quarter chord, a vertical lift arrow perpendicular to the free stream, a horizontal drag arrow along it, and the resultant arrow leaning slightly back; two dashed lines close the rectangle whose diagonal is the resultant.
:width: 90%

Schematic, lengths not to scale (at cruise the drag is a small fraction of the lift). Pressure pushes normal to the surface and shear drags along it (left). Added over the whole surface they give one resultant $R$ (right); its part across the free stream is the lift $L$ and its part along the free stream is the drag $D$, the two sides of the rectangle whose diagonal is $R$.
:::

Lift needs a fluid in contact with the body and motion between the two. It comes from the body turning the flow: the wing deflects the air downward, and the air pushes the wing up (NASA Glenn Research Center n.d.h). Computing lift belongs to Chapter 3 of these notes.

(p15-continuity)=
## The continuity equation

Mass is conserved. Applied to the fluid in a stream tube or a duct, that one fact gives the first equation of this page (NASA Glenn Research Center n.d.b).

Take the stream tube of {numref}`fig-p15-continuity`, with two cross sections, station 1 of area $A_1$ and station 2 of area $A_2$. Two assumptions keep the algebra simple:

1. The flow is steady.
2. The velocity and the density are uniform across each cross section: $V_1$ and $\rho_1$ everywhere on $A_1$, $V_2$ and $\rho_2$ everywhere on $A_2$.

In a short time $dt$, the fluid that crosses station 1 moves a distance $V_1\,dt$. It fills a slab of cross-section area $A_1$ and length $V_1\,dt$, of volume $A_1 V_1\,dt$. Its mass is the density times the volume:

$$
dm_1 = \rho_1 A_1 V_1\,dt
$$

In the same way, the mass that crosses station 2 in the same time is $dm_2 = \rho_2 A_2 V_2\,dt$.

:::{figure} figures/p15-continuity.svg
:label: fig-p15-continuity
:alt: A round tube cut lengthwise, narrowing from left to right, with the flow entering at the left. In the wide part a short, fat slab of fluid of length V1 dt is shaded; in the narrow part a long, thin slab of length V2 dt is shaded. A double arrow across the tube just after each slab marks the cross section, area A1 and area A2. The masses are labeled dm1 = rho1 A1 V1 dt and dm2 = rho2 A2 V2 dt.
:width: 90%

Schematic of a round tube, with the two slabs drawn at equal volumes. In the same time $dt$, the same mass crosses both stations: where the tube is narrow, the slab must be longer, so the fluid moves faster.
:::

Fluid cannot cross the wall of a stream tube, and in steady flow no mass can pile up between the two stations or drain away. Whatever mass enters at station 1 must leave at station 2 in the same time:

$$
dm_1 = dm_2
$$

that is,

$$
\rho_1 A_1 V_1\,dt = \rho_2 A_2 V_2\,dt
$$

Dividing both sides by $dt$ gives the continuity equation:

:::{math}
:label: eq-p15-continuity
\rho_1 A_1 V_1 = \rho_2 A_2 V_2
:::

Each side is the {term}`mass flow rate`, $\dot{m} = \rho A V$, the mass that crosses a section per second. The units check: (kg/m³)(m²)(m/s) = kg/s.

### Incompressible flow

The density of a gas can change from point to point in a flow. A flow in which it does is **compressible**. A flow in which the density is the same everywhere is **{term}`incompressible <incompressible flow>`**. No real fluid is exactly incompressible, but two cases come close enough:

- liquids, such as water, fuel, or the oil in a hydraulic line, whose density barely changes even under large pressures;
- air at low speed. Below a {term}`Mach number` of 0.3, a 10% change of speed changes the density by less than 1% (NASA Glenn Research Center n.d.e). At sea level, where the speed of sound is 340.3 m/s, $M = 0.3$ is 102.1 m/s. These notes treat air as incompressible below about 100 m/s.

With $\rho_1 = \rho_2$ the density cancels from {eq}`eq-p15-continuity`:

:::{math}
:label: eq-p15-incompressible
A_1 V_1 = A_2 V_2 = Q
:::

$Q = AV$ is the {term}`volume flow rate`, in m³/s. A garden hose shows the equation at work: put a thumb over the end, the opening shrinks, and the water leaves faster.

:::{warning} Diameters are not areas
A round pipe of diameter $D$ has area $A = \pi D^2/4$. The area goes with the square of the diameter: halving the diameter quarters the area, so the speed rises four times, not two. Convert every diameter to an area, and every length to meters, before using {eq}`eq-p15-incompressible`.
:::

## The momentum equation

The continuity equation alone cannot give a pressure. That takes Newton's second law, $F = ma$, applied to a fluid element moving along a streamline.

{numref}`fig-p15-fluid-element` shows a small box of fluid, of sides $dx$, $dy$, and $dz$, with $x$ along the streamline. Three kinds of force act on it:

1. pressure, acting normal to each of its six faces;
2. shear (friction), acting along each face;
3. gravity, acting on its mass.

To keep the result simple, assume there is no friction (an {term}`inviscid flow`) and leave gravity out for now; it returns for liquids in the next section. Only pressure is left, and along $x$ only the two end faces count.

:::{figure} figures/p15-fluid-element.svg
:label: fig-p15-fluid-element
:alt: A small box of fluid with sides dx, dy, and dz. A streamline runs along x through the box, dashed where the box hides it. A heavy arrow from the left, labeled pressure force p dy dz, pushes on the left face. A heavy arrow from the right, labeled pressure force p plus dp, times dy dz, pushes on the right face, shaded. Downstream of the box a thin velocity arrow V points along the streamline.
:width: 90%

Schematic of a fluid element on a streamline, with no friction and no gravity. Along the streamline only the pressure on the two end faces pushes on it. The pressure on the right face is higher by $dp$, so the net force is $-dp\,dy\,dz$: a pressure that falls along $x$ pushes the element forward.
:::

**Force from pressure.** The pressure on the left face is $p$; on the right face, a distance $dx$ farther along, it has changed to $p + dp$, with $dp = (dp/dx)\,dx$. Each end face has area $dy\,dz$. The left face is pushed in the $+x$ direction and the right face in the $-x$ direction, so the net force along $x$ is

$$
\begin{aligned}
F &= p\,dy\,dz - \left(p + \frac{dp}{dx}\,dx\right)dy\,dz\\
  &= -\frac{dp}{dx}\,dx\,dy\,dz
\end{aligned}
$$

**Mass times acceleration.** The mass of the element is its density times its volume, $m = \rho\,dx\,dy\,dz$. Its acceleration is the rate of change of its speed as it moves. In steady flow the speed depends only on where the element is along the streamline, $V = V(x)$, so by the chain rule

$$
a = \frac{dV}{dt} = \frac{dV}{dx}\,\frac{dx}{dt} = V\,\frac{dV}{dx}
$$

The element speeds up because it moves into a region where the flow is faster, even though nothing at a fixed point changes with time.

**Newton's second law.** Setting $F = ma$:

$$
-\frac{dp}{dx}\,dx\,dy\,dz = \rho\,dx\,dy\,dz\;V\,\frac{dV}{dx}
$$

The volume $dx\,dy\,dz$ appears on both sides and cancels. Multiplying both sides by $dx$ leaves the momentum equation, also called Euler's equation:

:::{math}
:label: eq-p15-euler
dp = -\rho\,V\,dV
:::

The minus sign matters. Along a streamline, a rise in speed ($dV > 0$) comes with a fall in pressure ($dp < 0$). The pressure difference is what pushes the element faster: it moves from high pressure toward low pressure and gains speed on the way. {eq}`eq-p15-euler` holds for compressible flow too, because nothing in the derivation assumed a constant density.

(p15-bernoulli)=
## Bernoulli's equation

Integrating Euler's equation along a streamline, from a point 1 to a point 2 (two points on the airfoil streamlines of {numref}`fig-p15-stream-tube`, for example), gives Bernoulli's equation (Anderson 2016, Chapter 4).

Start from {eq}`eq-p15-euler` and integrate both sides between the two points:

$$
\int_{p_1}^{p_2} dp = -\int_{V_1}^{V_2} \rho\,V\,dV
$$

Now assume the flow is incompressible. The density is then a constant and moves outside the integral:

$$
\begin{aligned}
p_2 - p_1 &= -\rho \int_{V_1}^{V_2} V\,dV\\
          &= -\rho\left(\frac{V_2^2}{2} - \frac{V_1^2}{2}\right)
\end{aligned}
$$

Moving the terms of each point to its own side:

:::{math}
:label: eq-p15-bernoulli
p_1 + \tfrac12 \rho V_1^2 = p_2 + \tfrac12 \rho V_2^2
:::

The sum $p + \tfrac12\rho V^2$ is the same at every point of the streamline (NASA Glenn Research Center n.d.a). Each term has a name.

:::{prf:definition} Static, dynamic, and total pressure
:label: def-p15-pressures

The **{term}`static pressure`** $p$ is the pressure of the flowing fluid itself, the pressure a small surface moving with the fluid would feel. It is the $p$ of the equation of state.

The **{term}`dynamic pressure`** is $q = \tfrac12 \rho V^2$, in Pa. It measures the kinetic energy of the flow per unit volume.

The **{term}`total pressure`** is $p_0 = p + \tfrac12\rho V^2$, the pressure the fluid would reach if it were brought to rest without friction. Along a streamline of steady, incompressible, inviscid flow, the total pressure is constant.
:::

With these names, Bernoulli's equation says that static pressure and dynamic pressure trade against each other while their sum stays fixed. This is the Bernoulli effect: where the air speeds up, its static pressure falls.

:::{warning} Three wrong explanations of lift
Three popular accounts of lift are wrong (NASA Glenn Research Center n.d.c, n.d.f, n.d.g):

- **Equal transit times over the two surfaces.** Nothing forces the two flows to meet at the trailing edge.
- **A skipping-stone bounce off the lower surface.** The upper surface turns more of the flow than the lower one.
- **Half a venturi over the top.** There is no second wall.

The first and the third rest on a true fact: faster air has a lower pressure. The second rests on another: air turned downward pushes the wing up. None of them explains why the air over the top moves faster.
:::

**The height term.** For a liquid the weight of the element cannot be left out. Let $z$ now be the height of the streamline above a reference level (not the side of the box in {numref}`fig-p15-fluid-element`), and let the streamline climb at an angle $\theta$, so that $\sin\theta = dz/dx$. The weight of the element is $\rho g$ times its volume, and its part along the streamline is $\rho g \sin\theta$ times the volume, pointing backward when the streamline climbs. Add it to the pressure force in Newton's second law and divide by the volume:

$$
-\frac{dp}{dx} - \rho g \sin\theta = \rho\,V\,\frac{dV}{dx}
$$

Multiply by $dx$ and write $\sin\theta\,dx = dz$:

$$
dp = -\rho V\,dV - \rho g\,dz
$$

Integrating with $\rho$ constant, as above, gives

:::{math}
:label: eq-p15-bernoulli-z
\begin{gathered}
p_1 + \tfrac12 \rho V_1^2 + \rho g z_1\\
= p_2 + \tfrac12 \rho V_2^2 + \rho g z_2
\end{gathered}
:::

where $z$ is the height of each point above any level you choose, in m, and $g = 9.8$ m/s². With the fluid at rest ($V_1 = V_2 = 0$), it becomes $p_2 - p_1 = -\rho g (z_2 - z_1)$: the {term}`hydrostatic equation` of the [standard atmosphere page](standard-atmosphere.md) for a fluid of constant density. In air the height term is small: one meter of height changes $\rho g z$ by 12.01 Pa at sea level, while the dynamic pressure at 50 m/s is 1,531 Pa. For air these notes leave it out.

:::{note} When Bernoulli's equation holds
1. Steady flow.
2. Incompressible flow: liquids, or air below about 100 m/s.
3. No friction (inviscid flow). Close to a surface, in the thin layer where friction acts, it fails.
4. The two points lie on the same streamline.
5. No energy added or removed between the two points: no fan, pump, propeller, or turbine in between.
:::

:::{warning} Two densities, two pressure scales
Bernoulli's equation uses the density of the fluid that flows: air, about 1 kg/m³, in an airspeed problem. A manometer uses the density of its liquid, water at 1,000 kg/m³. Mixing them up is the most common error on this page. A second trap is pressure scales: absolute pressure is measured from vacuum; gauge pressure is measured from the local atmosphere. Either works in Bernoulli's equation, as long as both sides use the same one. The equation of state always needs the absolute pressure.
:::

## Using continuity and Bernoulli together

Most flow problems need both equations: continuity gives the speeds from the areas, and Bernoulli gives the pressures from the speeds.

:::{tip} Method: speed and pressure in a duct
1. Number the two stations and list what is known at each: area or diameter, speed, pressure, height.
2. Turn diameters into areas, $A = \pi D^2/4$, and put every quantity in SI units.
3. Continuity: find the unknown speed from $A_1 V_1 = A_2 V_2$.
4. Bernoulli: find the unknown pressure (or the pressure difference) from {eq}`eq-p15-bernoulli`, or {eq}`eq-p15-bernoulli-z` if the height changes in a liquid.
5. Check: the speed is higher where the area is smaller, and the pressure is lower where the speed is higher.
:::

**The venturi.** A {term}`venturi` is a duct that narrows smoothly to a throat and widens again. Measuring $p_1 - p_2$ between the inlet and the throat gives the speed. From Bernoulli, $p_1 - p_2 = \tfrac12\rho\,(V_2^2 - V_1^2)$. From continuity, $V_1 = (A_2/A_1)\,V_2$. Substituting:

$$
p_1 - p_2 = \tfrac12\rho V_2^2\left[1 - \left(\frac{A_2}{A_1}\right)^2\right]
$$

and solving for the throat speed,

:::{math}
:label: eq-p15-venturi
V_2 = \sqrt{\frac{2\,(p_1 - p_2)}{\rho\left[1 - (A_2/A_1)^2\right]}}
:::

A venturi meter measures the flow in a pipe this way. A low-speed wind tunnel sets its test speed with the same relation between its wide inlet section and its narrow test section; Chapter 3 treats wind tunnels.

**The manometer.** A {term}`manometer` measures a pressure difference with a column of liquid. In a U-tube manometer, each leg is connected to one of the two pressures, $p_a$ and $p_b$. The higher pressure pushes its side of the liquid down, and the liquid settles with a height difference $h$ between the two surfaces. Compare the two legs at the level of the lower surface. In the leg at $p_a$ the pressure is $p_a$. In the other leg it is $p_b$ plus the weight per unit area of the liquid column of height $h$ above that level. In a connected liquid at rest the pressure is the same at one level in both legs, so $p_a = p_b + \rho_\text{L}\,g\,h$, or

:::{math}
:label: eq-p15-manometer
\Delta p = p_a - p_b = \rho_\text{L}\,g\,h
:::

Here $\rho_\text{L}$ is the density of the manometer liquid. The weight of the air in the legs is small and left out. A water manometer reading of 1 cm is a pressure difference of 98.00 Pa.

**A draining tank.** Bernoulli's equation with the height term also gives the speed of liquid leaving a hole in a large open tank. Take point 1 on the free surface and point 2 in the jet, a height $z$ below it. Both are at atmospheric pressure, so the pressures cancel. The surface of a large tank falls so slowly that $V_1 \approx 0$. {eq}`eq-p15-bernoulli-z` leaves $\rho g z = \tfrac12 \rho V_2^2$, so

:::{math}
:label: eq-p15-torricelli
V_2 = \sqrt{2 g z}
:::

the speed a stone reaches when dropped from the height $z$. With 2.0 m of water above the hole, $V_2 = \sqrt{2 \times 9.8 \times 2.0} = 6.261$ m/s. If the tank is small, the surface speed is not negligible: continuity, $A_1 V_1 = A_2 V_2$, gives it, and it enters Bernoulli's equation as $\tfrac12 \rho V_1^2$.

(p15-example-duct)=
### Worked example: a cooling-air duct

A ground cart blows cooling air into the electronics bay of an airliner through a round duct that narrows from $D_1 = 12$ cm to $D_2 = 9$ cm. At station 1 the air moves at $V_1 = 20$ m/s. The air is at sea-level standard density, $\rho = 1.2250$ kg/m³. Find the speed at station 2, the volume and mass flow rates, the pressure drop $p_1 - p_2$, and the reading $h$ of a water manometer connected between the two stations ({numref}`fig-p15-duct-example`).

1. **Areas.** $A_1 = \pi (0.12)^2/4 = 0.011310$ m² and $A_2 = \pi (0.09)^2/4 = 0.0063617$ m².
2. **Speed at station 2**, {eq}`eq-p15-incompressible`:
   $$
   \begin{aligned}
   V_2 &= V_1\,\frac{A_1}{A_2} = V_1 \left(\frac{D_1}{D_2}\right)^2\\
       &= 20 \times \left(\frac{12}{9}\right)^2\\
       &= 35.556\ \text{m/s}
   \end{aligned}
   $$
   The area ratio is $(12/9)^2 = 1.778$, the square of the diameter ratio. The speed stays below 100 m/s, so the incompressible model holds.
3. **Flow rates.**
   $$
   \begin{aligned}
   Q &= A_1 V_1 = 0.011310 \times 20\\
     &= 0.2262\ \text{m}^3\text{/s}\\
   \dot{m} &= \rho\,Q = 1.2250 \times 0.2262\\
     &= 0.2771\ \text{kg/s}
   \end{aligned}
   $$
4. **Pressure drop**, {eq}`eq-p15-bernoulli`, with $V_2^2 - V_1^2 = {35.556}^{2} - {20}^{2} = 864.23$ m²/s²:
   $$
   \begin{aligned}
   p_1 - p_2 &= \tfrac12 \rho \left(V_2^2 - V_1^2\right)\\
             &= 0.5 \times 1.2250 \times 864.23\\
             &= 529.3\ \text{Pa}
   \end{aligned}
   $$
5. **Manometer reading**, {eq}`eq-p15-manometer`, with the density of water:
   $$
   \begin{aligned}
   h &= \frac{p_1 - p_2}{\rho_\text{water}\,g}\\
     &= \frac{529.3}{1{,}000 \times 9.8}\\
     &= 0.05401\ \text{m}
   \end{aligned}
   $$
   or 54.0 mm.

**Check.** The speed rose by the area ratio, 1.778, where the area fell. The pressure fell by only 0.52% of the sea-level pressure, typical of low-speed air.

:::{figure} figures/p15-duct-example.svg
:label: fig-p15-duct-example
:alt: A round duct drawn to scale narrows from 12 centimeters to 9 centimeters in diameter, with air entering at the left. On the axis at station 1 a short velocity arrow shows the given 20 meters per second; at station 2 an arrow 1.778 times as long shows 35.56 meters per second. A U-tube water manometer below the duct is tapped through the lower wall at the two stations. The water stands 54.0 millimeters higher in the leg under station 2, which shows a pressure difference p1 minus p2 of 529.3 pascals.
:width: 90%

Computed for the worked example, to scale (the duct, the speeds at one arrow scale, and the water column): a duct narrowing from 12 cm to 9 cm with sea-level air at 20 m/s. The speed rises in proportion to the area ratio and the pressure falls: the water is pushed down in the leg under the higher pressure, at station 1.
:::

(p15-pitot-static)=
## The pitot-static tube

An aircraft measures its airspeed by measuring two pressures and applying Bernoulli's equation between them.

Follow the streamline that runs straight into the nose of a probe pointed into the flow ({numref}`fig-p15-pitot-static-tube`). The air on it slows down and comes to rest at the tip, at a {term}`stagnation point`. Bernoulli's equation between a point far ahead, with static pressure $p$ and speed $V_\infty$, and the stagnation point, with speed zero, gives the pressure there:

$$
p + \tfrac12 \rho V_\infty^2 = p_\text{stagnation} + 0
$$

so that

$$
p_\text{stagnation} = p_0
$$

The stagnation point feels the total pressure of the free stream. A small hole at the tip, connected to a tube, carries that pressure to a gauge. A tube used this way is a pitot tube.

The static pressure is measured through small holes in the side of the probe, a few diameters behind the nose. The lower panel of {numref}`fig-p15-pitot-static-tube` shows why they sit there. Just behind the nose the air speeds up around the shoulder and the surface pressure dips below $p$. Farther back the flow runs parallel to the surface at the free-stream speed, and the surface pressure returns to the free-stream static pressure. Holes there feel $p$.

:::{figure} figures/p15-pitot-static-tube.svg
:label: fig-p15-pitot-static-tube
:alt: Top: a pitot-static probe in section, pointing into a flow from the left. The streamline on the axis ends at a stagnation point just ahead of the open nose hole, labeled V equals 0 and pressure p0; from the hole a central tube carries p0 to the gauge. Static holes in the side, three diameters behind the nose, open into an outer chamber that carries p to the gauge. Bottom: the computed surface pressure along the probe, minus the free-stream static pressure, divided by q. It starts at 1 at the nose, dips to minus 0.33 just behind it, and returns to almost exactly zero by the static holes.
:width: 90%

Computed for ideal flow past a round-nosed probe. The nose hole feels the total pressure $p_0$. By three diameters behind the nose the surface pressure differs from $p$ by less than 1.6% of $q$, so the side holes feel $p$, and the gauge measures the difference, $p_0 - p = q$.
:::

The gauge measures $p_0 - p$, which is the dynamic pressure, and Bernoulli's equation gives the speed (NASA Glenn Research Center n.d.d):

:::{math}
:label: eq-p15-pitot
V_\infty = \sqrt{\frac{2\,(p_0 - p)}{\rho}}
:::

The density $\rho$ is that of the air around the aircraft, at its altitude. For a standard day it comes from the [standard atmosphere](#p14-layers).

### Worked example: airspeed from a pressure reading

An uncrewed aircraft flies at $h = 6{,}000$ m in the standard atmosphere. Its pitot-static tube reads $p_0 - p = 2{,}000$ Pa. Find its airspeed.

1. **Layer.** 6,000 m is in the troposphere, a gradient layer with $a = -0.0065$ K/m that starts at sea level.
2. **Temperature.** $T = 288.16 + (-0.0065)(6{,}000) = 249.16$ K.
3. **Density**, from the gradient-layer equation with the exponent $-(g_0/(aR) + 1) = 4.2533$:
   $$
   \begin{aligned}
   \rho &= \rho_1 \left(\frac{T}{T_1}\right)^{4.2533}\\
        &= 1.2250 \left(\frac{249.16}{288.16}\right)^{4.2533}\\
        &= 0.6600\ \text{kg/m}^3
   \end{aligned}
   $$
4. **Airspeed**, {eq}`eq-p15-pitot`:
   $$
   \begin{aligned}
   V_\infty &= \sqrt{\frac{2\,(p_0 - p)}{\rho}}\\
            &= \sqrt{\frac{2 \times 2{,}000}{0.6600}}\\
            &= 77.85\ \text{m/s}
   \end{aligned}
   $$

**Check.** The speed is below 100 m/s, so the incompressible relation applies. With the sea-level density instead, the same reading gives $\sqrt{2 \times 2{,}000/1.2250} = 57.14$ m/s, about 27% too low: at altitude the thinner air needs a higher speed to produce the same dynamic pressure.

That second number has a name. An airspeed indicator cannot measure the density, so its dial turns the pressure difference into a speed as if the air had the sea-level standard density (FAA 2012, Chapter 5). The speed it shows is the **{term}`indicated airspeed`**, here 57.14 m/s. The speed of the aircraft through the air is the **{term}`true airspeed`**, here 77.85 m/s. The two are equal only where the density is the sea-level value; pilots convert one to the other with the density at their altitude (FAA 2023, Chapter 8). Real airspeed indicators also correct for compressibility, which matters at higher speeds; that correction is outside this standard.

### Worked example: a manometer reading

A pitot-static tube is held in the slipstream behind a propeller during an engine test on the ground, at sea-level standard conditions. Its two lines go to a water U-tube manometer that reads $h = 6.5$ cm. Find the speed of the slipstream.

1. **Pressure difference**, {eq}`eq-p15-manometer`, with the density of water and $h$ in meters:
   $$
   \begin{aligned}
   p_0 - p &= \rho_\text{water}\,g\,h\\
           &= 1{,}000 \times 9.8 \times 0.065\\
           &= 637.0\ \text{Pa}
   \end{aligned}
   $$
2. **Speed**, {eq}`eq-p15-pitot`, with the density of air:
   $$
   \begin{aligned}
   V &= \sqrt{\frac{2\,(p_0 - p)}{\rho}}\\
     &= \sqrt{\frac{2 \times 637.0}{1.2250}}\\
     &= 32.25\ \text{m/s}
   \end{aligned}
   $$

**Check.** Using the density of water in step 2 would give 1.129 m/s, slower than a walk, which is not a propeller slipstream.

## The pitot-static instruments

An aircraft uses the same two pressures to run three instruments, as {numref}`fig-p15-pitot-static-system` shows (FAA 2023, Chapter 8). The pitot tube on the wing or the nose collects the total pressure through its ram-air inlet; a small drain hole underneath lets water out. Static ports, flush holes in the side of the fuselage, collect the static pressure.

:::{figure} figures/p15-pitot-static-system.svg
:label: fig-p15-pitot-static-system
:alt: Diagram of an aircraft pitot-static system. Ram air enters a pitot tube that has a drain hole underneath; a solid pitot line carries the total pressure p0 to the airspeed indicator only. A static port in the skin feeds a dashed static line, which branches to all three instruments: the airspeed indicator, which reads p0 minus p, the altimeter, which reads p, and the vertical speed indicator, which reads the rate of change of p.
:width: 70%

Schematic of the pitot-static system. The pitot line feeds only the airspeed indicator; the static line feeds all three instruments, so a blocked static port upsets all three. After FAA (2023, Figure 8-1).
:::

:::{table} The three pitot-static instruments and the pressures they use.
:label: tbl-p15-instruments
:align: center

| Instrument | Connected to | What it senses | What it shows |
| --- | --- | --- | --- |
| {term}`Airspeed indicator` | Pitot line and static line | $p_0 - p$, across a diaphragm | Indicated airspeed, from $\sqrt{2(p_0 - p)/\rho_\text{SL}}$ |
| {term}`Altimeter` | Static line | $p$, with sealed metal capsules (aneroid wafers) that expand as $p$ falls | Altitude: the standard-atmosphere altitude where the pressure is $p$ |
| {term}`Vertical speed indicator` | Static line, directly and through a small calibrated leak | How fast $p$ is changing | Rate of climb or descent |

:::

The altimeter is the [standard atmosphere](#p14-layers) worked backward: it measures a pressure and shows the altitude at which the standard atmosphere has that pressure. The vertical speed indicator holds a diaphragm fed straight from the static line inside a case fed through a calibrated leak. In a climb the static pressure falls; the diaphragm feels it at once, but the case lags behind, and the difference shows as a rate of climb. In level flight the two pressures are equal and the needle reads zero.

## Blocked pitot and static ports

Ice, water, dirt, or insects can block the openings of the system. A blockage traps a pressure, and the instruments then read wrong in ways that follow from the table above (FAA 2023, Chapter 8). Aircraft that sit on the ground for a long time often wear a pitot tube cover against insects. Before each flight pilots make sure the cover is off and the openings are clear, and many aircraft heat the pitot tube to keep ice off.

:::{tip} Method: reasoning out a blockage
1. Name the blocked opening: the pitot inlet, the pitot inlet and its drain hole, or the static port.
2. Decide which pressure is now trapped in the line and at what value, or whether the line vents to the outside.
3. Follow the outside static pressure through the maneuver: it falls in a climb and rises in a descent.
4. For each instrument, compare the two pressures it now receives and read off the result.
:::

The three cases:

1. **Pitot inlet blocked, drain hole open.** The air in the pitot line leaks out through the drain hole until the line holds the outside static pressure. Both sides of the airspeed indicator feel $p$, and it falls to zero. The altimeter and the vertical speed indicator still work.
2. **Pitot inlet and drain hole both blocked.** The total pressure at the moment of the blockage is trapped. In level flight the airspeed indicator no longer responds to a change of speed. In a climb the outside static pressure falls while the trapped pressure stays, so the indicator reads higher and higher; in a descent it reads lower. It now behaves like an altimeter. The other two instruments still work.
3. **Static port blocked.** The static pressure at the moment of the blockage is trapped. The altimeter freezes and the vertical speed indicator stays at zero. As long as the altitude does not change, the trapped pressure still equals the outside pressure and the airspeed indicator reads correctly. In a climb the total pressure falls but the trapped static pressure does not, so the airspeed indicator reads low; in a descent it reads high.

:::{warning} The dangerous combination
In case 2 a climb makes the airspeed reading rise. A pilot who believes it may raise the nose to slow down, which steepens the climb and raises the reading further while the true airspeed falls. After a blockage, find the trapped pressure before trusting any reading.
:::

(p15-example-blockage)=
### Worked example: a pitot cover left on

A small cargo airplane stands at a sea-level airport with a cover over its pitot tube, and nobody removes it. Take the simplest case: the cover seals both the ram-air inlet and the drain hole, the day is standard, and the air trapped in the pitot line is still at the pressure of the runway. The pilot takes off and climbs, holding a true airspeed of 65 m/s. Find what the airspeed indicator shows on the takeoff run, at 150 m, and at 300 m.

1. **Trapped pressure.** The cover went on with the airplane at rest, so no dynamic pressure was trapped: from then on the pitot line holds the static pressure of the runway, $p_\text{pitot} = 101{,}325$ Pa.
2. **On the takeoff run.** The static line also holds 101,325 Pa, so the gap $p_\text{pitot} - p$ is zero and the indicator reads 0 m/s at any speed. At 65 m/s the dynamic pressure is 2,587.8 Pa, but none of it reaches the pitot line. A pilot who checks that the airspeed rises during the takeoff run catches the blockage here (FAA 2023, Chapter 8).
3. **At 150 m.** From the standard atmosphere,
   $$
   \begin{aligned}
   T &= 288.16 - 0.0065 \times 150\\
     &= 287.185\ \text{K}\\
   p &= 101{,}325 \times \left(\frac{287.185}{288.16}\right)^{5.2533}\\
     &= 99{,}536.9\ \text{Pa}
   \end{aligned}
   $$
   The pitot line still holds the runway pressure, so the indicator senses
   $$
   \begin{aligned}
   p_\text{pitot} - p &= 101{,}325 - 99{,}536.9\\
                      &= 1{,}788.1\ \text{Pa}\\
   V_\text{indicated} &= \sqrt{\frac{2 \times 1{,}788.1}{1.2250}}\\
                      &= 54.0\ \text{m/s}
   \end{aligned}
   $$
4. **At 300 m.** In the same way, $T = 286.210$ K and $p = 97{,}774.4$ Pa, so
   $$
   \begin{aligned}
   p_\text{pitot} - p &= 101{,}325 - 97{,}774.4\\
                      &= 3{,}550.6\ \text{Pa}\\
   V_\text{indicated} &= \sqrt{\frac{2 \times 3{,}550.6}{1.2250}}\\
                      &= 76.1\ \text{m/s}
   \end{aligned}
   $$

**Check.** The reading has nothing to do with the speed: the true airspeed stayed at 65 m/s while the dial went from 0 to 54.0 and then to 76.1 m/s, rising with height like an altimeter. With both lines open, the density at 300 m is 1.1901 kg/m³ and the dynamic pressure is $0.5 \times 1.1901 \times {65}^{2} = 2{,}514.1$ Pa. The dial would then read $\sqrt{2 \times 2{,}514.1/1.2250} = 64.1$ m/s, a little below the true airspeed because the air is thinner. The covered tube shows the right number only by chance, near 213 m. A real cover is not a perfect seal. The pressure of the trapped air also drifts with its temperature, by about 350 Pa for each kelvin, so the readings of a real covered tube wander around these values. A cover that leaks behaves like case 1, and the dial stays near zero. {numref}`fig-p15-blockage-pressures` and {numref}`tbl-p15-blockage` compare this case with the others.

:::{figure} figures/p15-blockage-pressures.svg
:label: fig-p15-blockage-pressures
:alt: Four plots of the pressure in the pitot line (solid) and the static line (dashed) against altitude from the runway to 300 meters, for an airplane at a true airspeed of 65 meters per second. Both lines open: both fall together, and the gap at 300 meters, 2.51 kilopascals, reads 64.1 meters per second. Inlet and drain blocked, the cover of the worked example: the pitot line stays at the runway pressure while the static line falls, and the gap grows to 3.55 kilopascals, read as 76.1 meters per second. Inlet blocked with the drain open: the two lines coincide and the dial reads 0. Static port blocked: the static line stays at the runway pressure, the gap closes near 213 meters, and the dial reads 0 at 300 meters.
:width: 85%

Computed for the worked example: an airplane climbing from a sea-level runway to 300 m, holding a true airspeed of 65 m/s, with each blockage in place before takeoff. The airspeed indicator reads the gap between the pitot line (solid) and the static line (dashed). A trapped pitot pressure widens the gap in a climb, and the dial reads high; a pitot line that vents through its drain closes the gap, and the dial reads zero; a trapped static pressure narrows the gap, and the dial reads low.
:::

:::{table} What the instruments show after each blockage (FAA 2023, Chapter 8).
:label: tbl-p15-blockage
:align: center

<table>
<tr><th>Case</th><th>Airspeed indicator, level flight</th><th>Airspeed indicator, climb</th><th>Airspeed indicator, descent</th><th>Altimeter</th><th>Vertical speed indicator</th></tr>
<tr><th scope="row">Pitot inlet blocked, drain open</th><td>Falls to zero</td><td>Zero</td><td>Zero</td><td>Correct</td><td>Correct</td></tr>
<tr><th scope="row">Pitot inlet and drain blocked</th><td>No change when the speed changes</td><td>Reads higher and higher</td><td>Reads lower and lower</td><td>Correct</td><td>Correct</td></tr>
<tr><th scope="row">Static port blocked</th><td>Correct while the altitude does not change</td><td>Reads low</td><td>Reads high</td><td>Frozen at the altitude of the blockage</td><td>Zero</td></tr>
</table>

:::

## Summary

:::{important} Summary
- In steady flow the mass flow $\rho A V$ is the same at every section of a stream tube or a duct; for liquids and air below about 100 m/s, $A_1 V_1 = A_2 V_2$.
- Newton's second law on a fluid element along a streamline gives $dp = -\rho V\,dV$. For incompressible flow without friction it integrates to Bernoulli's equation: the total pressure $p + \tfrac12\rho V^2$ (plus $\rho g z$ for a liquid) is constant along a streamline.
- A pitot-static tube measures $p_0$ at its stagnation point and $p$ at its side holes, and $V = \sqrt{2(p_0 - p)/\rho}$ with the local air density. The dial uses the sea-level density and shows the indicated airspeed.
- A blockage traps a pressure. A trapped pitot pressure makes the airspeed read high in a climb; a trapped static pressure freezes the altimeter, holds the vertical speed indicator at zero, and makes the airspeed read low in a climb. Both errors reverse in a descent.
:::

:::{table} The equations of this page.
:label: tbl-p15-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Mass flow rate (kg/s) | $\dot{m} = \rho A V$ |
| Continuity, steady flow | $\rho_1 A_1 V_1 = \rho_2 A_2 V_2$ |
| Continuity, incompressible; volume flow rate (m³/s) | $A_1 V_1 = A_2 V_2$, $Q = AV$ |
| Area of a round duct | $A = \pi D^2/4$ |
| Momentum (Euler's) equation, no friction | $dp = -\rho V\,dV$ |
| Bernoulli's equation, along a streamline | $p_1 + \tfrac12\rho V_1^2 + \rho g z_1 = p_2 + \tfrac12\rho V_2^2 + \rho g z_2$ |
| Manometer (density of the liquid) | $\Delta p = \rho_\text{L}\,g\,h$ |
| Draining tank, large tank | $V = \sqrt{2 g z}$ |
| Pitot-static airspeed (density of the air) | $V_\infty = \sqrt{2(p_0 - p)/\rho}$ |

:::

:::{exercise} For discussion
:label: ex-p15-discussion

1. A rocket climbs through the atmosphere, getting faster as the air gets thinner. What happens to the static pressure and to the dynamic pressure on the vehicle during the climb? Why would its designers care when the dynamic pressure is largest?
2. A duct of constant area has a model mounted inside it. Upstream and downstream of the model the areas are the same, yet the total pressure downstream is lower. Which assumption of Bernoulli's equation has failed, and where?
3. Why does a pitot-static tube work poorly at low speeds? (Estimate $p_0 - p$ at 2 m/s in air.)
4. Explain to a friend, without equations, why "the air on top has farther to go, so it goes faster" is not the reason a wing lifts.
:::

## Quiz

:::{iframe} ../quickcheck/quiz-1-5.html
:label: quiz-1-5
:enumerated: false
:width: 100%

Quiz for Standard 1.5: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016.
- Federal Aviation Administration (FAA), *[Instrument Flying Handbook](https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/FAA-H-8083-15B.pdf)*, FAA-H-8083-15B, 2012. Chapter 5, "Flight Instruments."
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023.
- NASA Glenn Research Center, "[Bernoulli's Equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/bernoullis-equation/)," Beginner's Guide to Aeronautics, n.d.a.
- NASA Glenn Research Center, "[Conservation of Mass](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/conservation-of-mass/)," Beginner's Guide to Aeronautics, n.d.b.
- NASA Glenn Research Center, "[Equal Transit Theory](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/foilw1/)," Beginner's Guide to Aeronautics, n.d.c.
- NASA Glenn Research Center, "[Pitot-Static Tube](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/pitot-static-tube-speedometer/)," Beginner's Guide to Aeronautics, n.d.d.
- NASA Glenn Research Center, "[Role of Mach Number in Compressible Flows](https://www.grc.nasa.gov/www/k-12/airplane/machrole.html)," Beginner's Guide to Aeronautics, n.d.e.
- NASA Glenn Research Center, "[Skipping Stone Theory](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/foilw2/)," Beginner's Guide to Aeronautics, n.d.f.
- NASA Glenn Research Center, "[Venturi Theory](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/venturi-theory/)," Beginner's Guide to Aeronautics, n.d.g.
- NASA Glenn Research Center, "[What is Lift?](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/what-is-lift/)," Beginner's Guide to Aeronautics, n.d.h.
