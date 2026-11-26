---
title: "Engines and tanks"
short_title: Engines and tanks
---

Pages 4.2 to 4.4 gave us a propellant mass for each stage ([sizing a stage](#p42-stage-sizing)). Knowing the propellant mass alone does not give us the hardware dimensions. On this page, we size the engine that burns the propellant and the tanks that hold it, and we estimate how much cryogenic propellant boils away while the stage is on the pad or coasting in space. No course standard is assessed on this page.

:::{note} What to take from this page
- The thrust and the specific impulse set the mass flow, $\dot m = F/(I_\text{sp}\,g_0)$, and the propellant load then sets the burn time, $t_b = m_\text{prop}/\dot m$.
- The same flow passes through the throat, $\dot m = p_c A_t/c^*$. A higher chamber pressure gives a smaller engine but needs a stronger chamber and feed system.
- Each tank holds its share of the propellant, split with the mixture ratio, plus a gas space called ullage. The mass of its wall grows with its pressure times its volume.
- Heat that leaks into a cryogenic tank boils propellant away at the rate $\dot Q/h_\text{vap}$. That loss is small over a few days, but it becomes a large share of the propellant over several months.
:::

(p45-engine)=
## The engine

### Mass flow and burn time

We start with the thrust $F$ that the engine must produce. From [specific impulse, page 4.1](#p41-specific-impulse), thrust equals the mass flow rate times $I_\text{sp}\,g_0$, so the required propellant mass flow rate is

:::{math}
:label: eq-p45-mass-flow
\dot m = \frac{F}{I_\text{sp}\,g_0}
:::

with $g_0 = 9.81\ \text{m/s}^2$. If the mass flow rate is steady, the {term}`burn time` is the propellant mass divided by that mass flow rate:

:::{math}
:label: eq-p45-burn-time
t_b = \frac{m_\text{prop}}{\dot m}
:::

If we substitute [](#eq-p45-mass-flow) into [](#eq-p45-burn-time) and rearrange, the mass flow rate cancels and we obtain $F\,t_b = m_\text{prop}\,I_\text{sp}\,g_0$. The propellant mass and specific impulse set this total impulse, while a higher-thrust engine delivers the same impulse in less time.

### Worked example 1: the main engines of the Space Shuttle

The Space Shuttle had three RS-25 main engines, fed by the External Tank. At rated power, 100% of its design thrust, each engine gives 470,000 lbf (2,090,664 N) in vacuum with a specific impulse of 455.2 s. The tank holds 616,493 kg of liquid oxygen and 102,618 kg of liquid hydrogen, 719,112 kg in all (the source's total; NASA 1981, pp. 2-4 and 2-34). Find the mass flow of one engine and the time the three engines take to empty the tank.

1. **Mass flow of one engine**, [](#eq-p45-mass-flow):
   $$
   \begin{aligned}
   \dot m &= \frac{2{,}090{,}664}{455.2 \times 9.81}\\
          &= 468.2\ \text{kg/s}
   \end{aligned}
   $$
2. **Three engines.**
   $$
   \begin{aligned}
   \dot m_\text{total} &= 3 \times 468.2\\
                       &= 1{,}404.6\ \text{kg/s}
   \end{aligned}
   $$
3. **Burn time**, [](#eq-p45-burn-time):
   $$
   \begin{aligned}
   t_b &= \frac{719{,}112\ \text{kg}}{1{,}404.6\ \text{kg/s}}\\
       &= 512.0\ \text{s}
   \end{aligned}
   $$
   That is 8.53 minutes.

**Check.** NASA (1981, p. 2-4) gives the main engines "approximately the first 8.5 minutes of flight". The engines are throttled between 65 and 109% of rated power during the climb, so our flow at rated power is an average.

### The throat and the chamber pressure

The size of the engine comes from its throat, the narrowest section of the nozzle. The hot gas in the {term}`combustion chamber` is at the {term}`chamber pressure` $p_c$, and it flows through the throat at the speed of sound. A higher chamber pressure packs more gas into each cubic meter, so the same throat passes more mass each second (Huzel and Huang 1967, Eq. 1-32):

:::{math}
:label: eq-p45-throat
\dot m = \frac{p_c\,A_t}{c^*}
:::

where $A_t$ is the throat area and $c^*$ is the characteristic velocity of the propellants.

:::{prf:definition} Characteristic velocity
:label: def-p45-characteristic-velocity

The {term}`characteristic velocity` $c^* = p_c A_t/\dot m$, in m/s, is the chamber pressure times the throat area per unit mass flow. With a higher $c^*$, the engine maintains the same chamber pressure through the same throat area using a smaller propellant mass flow rate. It depends on the propellants, their mixture ratio, and how well they burn, and not on the nozzle downstream of the throat. A more energetic combustion gives a higher $c^*$ (Huzel and Huang 1967, Section 1.3).
:::

Checking the units of [](#eq-p45-throat), Pa times m² divided by m/s equals N·s/m, or kg/s. Huzel and Huang (1967, Tables 1-9 and 1-10) list theoretical values. Liquid oxygen and liquid hydrogen at a mixture ratio of 4.02 give 2,432 m/s (7,980 ft/s), and liquid oxygen and kerosene give 1,804 m/s (5,920 ft/s).

We can find the RS-25's $c^*$ from its own data. Its throat is 10.3 in (0.2616 m) across (NASA 2015, p. 274), so $A_t = \pi \times {0.2616}^{2}/4 = 0.05375$ m². Its chamber pressure is 2,970 psia, or 20.48 MPa (NASA 1981, p. 2-4). Then

$$
\begin{aligned}
c^* &= \frac{20.48 \times {10}^{6} \times 0.05375}{468.2}\\
    &= 2{,}351\ \text{m/s}
\end{aligned}
$$

That is close to the theoretical value but not equal, because the RS-25 burns 6 parts of oxygen to 1 of hydrogen, and $c^*$ changes with the mixture ratio.

Now we solve [](#eq-p45-throat) for the throat area, $A_t = \dot m\,c^*/p_c$. For a given flow and propellant, the throat area is inversely proportional to the chamber pressure ({numref}`fig-p45-throat-and-pressure`). At half the RS-25's pressure, 10.24 MPa, the same flow needs 0.1075 m², twice the area. So a lower chamber pressure means a bigger, heavier engine. A higher chamber pressure requires a stronger chamber and a feed system that delivers the propellants at an even higher pressure (Huzel and Huang 1967, Section 1.3).

:::{figure} figures/p45-throat-and-pressure.svg
:label: fig-p45-throat-and-pressure
:alt: Throat area in square meters against chamber pressure in megapascals, from 4 to 29 megapascals, for one mass flow. The curve falls steeply at low pressure and flattens at high pressure. A filled dot marks the RS-25 at 20.48 megapascals and 0.05375 square meters. An open dot at half that pressure, 10.24 megapascals, sits at 0.1075 square meters, twice the area. Dashed lines run from both dots to both axes. On the area axis a double arrow marked times 2 spans the two areas; on the pressure axis a double arrow marked times one half spans the two pressures.
:width: 80%

Computed: halving the chamber pressure doubles the throat area the same flow needs, and doubling it halves the throat. From [](#eq-p45-throat) with the RS-25's mass flow, 468.2 kg/s, and the characteristic velocity found from its data, 2,351 m/s, both held fixed. Engine data from NASA (1981, p. 2-4) and NASA (2015, p. 274).
:::

### How heavy the engine is

Up to now, we have grouped the engine mass inside the stage's inert mass. To estimate the engine mass separately, we use the engine's own {term}`thrust-to-weight ratio`, defined as engine thrust divided by engine weight on Earth, $W = m\,g_0$. (Unlike the vehicle ratio near 1.2 to 1.5 on page 4.4, an individual engine's ratio is much larger.) {numref}`tbl-p45-engine-mass` gives it for three engines.

:::{table} The thrust-to-weight ratio of three large engines, from published thrust and mass: the F-1 at its uprated sea-level thrust (NASA 1968a), the RS-25 and the J-2 in vacuum (NASA 1981, p. 2-4; NASA 1968b).
:label: tbl-p45-engine-mass
:align: center

<table>
<thead>
<tr><th>Engine</th><th>Propellants</th><th>Thrust, kN</th><th>Mass, kg</th><th>Thrust-to-weight ratio</th></tr>
</thead>
<tbody>
<tr><th scope="row">F-1 (Saturn V first stage)</th><td>liquid oxygen and kerosene</td><td class="num">6,770 (sea level)</td><td class="num">8,391</td><td class="num">82.2</td></tr>
<tr><th scope="row">RS-25 (Space Shuttle)</th><td>liquid oxygen and liquid hydrogen</td><td class="num">2,091 (vacuum)</td><td class="num">3,000</td><td class="num">71.0</td></tr>
<tr><th scope="row">J-2 (Saturn V upper stages)</th><td>liquid oxygen and liquid hydrogen</td><td class="num">1,001 (vacuum)</td><td class="num">1,579</td><td class="num">64.6</td></tr>
</tbody>
</table>

:::

Each engine lifts 65 to 82 times its own weight, and Huzel and Huang (1967, Section 2.1) put large engines of their time at 75 to 125. Because the total thrust $F$ produced by the engines equals both $(F/W)_\text{engine}\,m_\text{engine}\,g_0$ and $(F/W)_\text{vehicle}\,m_\text{vehicle}\,g_0$, where $m_\text{engine}$ is the combined mass of all engines on the vehicle, setting them equal gives

$$
\frac{m_\text{engine}}{m_\text{vehicle}} = \frac{(F/W)_\text{vehicle}}{(F/W)_\text{engine}}
$$

A launch vehicle needs a thrust-to-weight ratio a little above 1 to leave the pad ([page 4.4](#p44-thrust-to-weight)). With engine ratios near 70, the engines are a small part of the vehicle's mass.

### Feeding the engine: pressure or pumps

The propellants must enter the chamber above $p_c$. We have two ways to get them there ({numref}`fig-p45-feed-systems`; Huzel and Huang 1967, Section 1.5, Figures 1-12 and 1-13):

- A {term}`pressure-fed` engine pushes the propellants out of the tanks with a gas, usually helium, stored in a bottle at high pressure. A regulator keeps the tank pressure steady. Because there is no rotating turbomachinery, the system is simple, but the tanks must withstand a pressure higher than the chamber pressure.
- A pump-fed engine raises the pressure with a {term}`turbopump`: a pump for each propellant, driven by a turbine on the same shaft. On the F-1 and the J-2 a small gas generator burns a little of both propellants to drive the turbine (NASA 1968a, 1968b). The tanks need only enough pressure to feed the pumps.

Pump-fed booster stages run their tanks at 30 to 100 psia (0.2 to 0.7 MPa). Pressure-fed upper stages run theirs at 100 to 400 psia, up to 2.8 MPa (Huzel and Huang 1967, Section 8.1). The heavier tanks show in the propellant fraction, the share of the stage's own loaded mass that is propellant, or one minus the {term}`inert mass fraction`. Typical values are 0.94 for pump-fed stages and 0.89 for pressure-fed stages (Huzel and Huang 1967, Section 2.1).

:::{figure} figures/p45-feed-systems.svg
:label: fig-p45-feed-systems
:alt: Two schematics side by side, nozzles down. Left, pressure-fed: a helium sphere at the top feeds, through a valve labeled regulator, two capsule-shaped tanks below it, fuel and oxidizer, with thick, hatched walls; pipes with valves lead down from each tank to the thrust chamber. Under it: tanks at 0.7 to 2.8 megapascals, thick, heavy walls. Right, pump-fed: two thin-walled tanks, fuel and oxidizer, each piped down to its own pump, the fuel pump and the oxidizer pump, on one shaft with a turbine between them; a gas generator below the turbine burns a little of each propellant to drive it; pipes with valves lead from the pumps to the thrust chamber. Under it: tanks at 0.2 to 0.7 megapascals, thin, light walls.
:width: 80%

Schematic, not to scale; wall thickness exaggerated. In a pressure-fed engine the tank pressure must push the propellants into the chamber, so the tanks are thick and heavy. In a pump-fed engine the turbopump raises the pressure after the tanks, so the tanks stay at low pressure and can be thin and light. Tank pressures from Huzel and Huang (1967, Section 8.1); the gas that keeps a little pressure in the pump-fed tanks and the duct that carries the turbine's exhaust overboard are not drawn.
:::

(p45-tanks)=
## The tanks

The tanks must hold the propellant and fit inside the stage. First we split the propellant mass with the {term}`mixture ratio`, O/F, the mass of oxidizer per kilogram of fuel ([page 4.4](#p44-propellant-properties)):

:::{math}
:label: eq-p45-split
\begin{aligned}
m_\text{ox} &= m_\text{prop}\,\frac{\text{O/F}}{1 + \text{O/F}}\\
m_\text{fuel} &= \frac{m_\text{prop}}{1 + \text{O/F}}
\end{aligned}
:::

Each liquid takes the volume $\mathcal{V} = m/\rho$. We never fill a tank to the top: we leave a gas space, the {term}`ullage`, for the pressurizing gas and for the liquid to expand as it warms. Huzel and Huang (1967, Eq. 8-1, Sample Calculation 8-1) allow 2.5%. With an ullage fraction $u$ of the liquid volume, the tank volume is

:::{math}
:label: eq-p45-tank-volume
\mathcal{V}_\text{tank} = (1 + u)\,\frac{m}{\rho}
:::

For a given volume, a sphere is the lightest pressure vessel: it has the least surface and the lowest wall stress (Huzel and Huang 1967, Section 8.2). A sphere of volume $\mathcal{V}_\text{tank}$ has the diameter

:::{math}
:label: eq-p45-sphere
d = {\left(\frac{6\,\mathcal{V}_\text{tank}}{\pi}\right)}^{1/3}
:::

and it must be smaller than the stage diameter. Stacked spheres waste length, so large stages use cylindrical tanks with domed ends, often sharing one dome, the common bulkhead of [page 1.3](#p13-launch-vehicle).

:::{tip} Method: sizing the tanks of a stage
1. Split the propellant mass into oxidizer and fuel with the mixture ratio, [](#eq-p45-split).
2. Find each liquid volume, $\mathcal{V} = m/\rho$, with the density of that liquid at its storage temperature.
3. Add the ullage, [](#eq-p45-tank-volume).
4. Find each tank's size, [](#eq-p45-sphere) for a sphere, and check that it fits the stage.
:::

### Worked example 2: the tanks of a kerosene upper stage

An upper stage carries 12,000 kg of liquid oxygen and kerosene at a mixture ratio of 2.56 (Huzel and Huang 1967, Table 1-9). Each tank is a sphere with 5% ullage, and the stage is 3.0 m in diameter. Liquid oxygen has a density of 1,141 kg/m³ at its boiling point (NIST 2023). For kerosene (RP-1) Huzel and Huang (1967, Table 1-4) give 800 to 820 kg/m³ at 20 °C. We take 800 kg/m³, which gives the larger tank. Find the size of each tank.

1. **Split the propellant**, [](#eq-p45-split):
   $$
   \begin{aligned}
   m_\text{ox} &= 12{,}000 \times \frac{2.56}{3.56}\\
               &= 8{,}629\ \text{kg}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   m_\text{fuel} &= \frac{12{,}000}{3.56}\\
                 &= 3{,}371\ \text{kg}
   \end{aligned}
   $$
2. **Liquid volumes, in m³.**
   $$
   \begin{aligned}
   \mathcal{V}_\text{ox} &= \frac{8{,}629}{1{,}141}\\
                         &= 7.563
   \end{aligned}
   $$
   $$
   \begin{aligned}
   \mathcal{V}_\text{fuel} &= \frac{3{,}371}{800}\\
                           &= 4.214
   \end{aligned}
   $$
3. **Tank volumes with 5% ullage, in m³**, [](#eq-p45-tank-volume):
   $$
   \begin{aligned}
   \mathcal{V}_\text{tank,ox} &= 1.05 \times 7.563\\
                              &= 7.941
   \end{aligned}
   $$
   $$
   \begin{aligned}
   \mathcal{V}_\text{tank,fuel} &= 1.05 \times 4.214\\
                                &= 4.425
   \end{aligned}
   $$
4. **Sphere diameters**, [](#eq-p45-sphere):
   $$
   \begin{aligned}
   d_\text{ox} &= {\left(\frac{6 \times 7.941}{\pi}\right)}^{1/3}\\
               &= 2.475\ \text{m}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   d_\text{fuel} &= {\left(\frac{6 \times 4.425}{\pi}\right)}^{1/3}\\
                 &= 2.037\ \text{m}
   \end{aligned}
   $$

**Check.** Both spheres are smaller than the 3.0 m stage, so they fit, one above the other, in 4.51 m of its length ({numref}`fig-p45-tanks-in-stage`). The oxygen is 71.9% of the propellant mass but only 64.2% of the tank volume. Its tank holds 2.56 times the kerosene's mass in 1.79 times the volume, because liquid oxygen is denser.

:::{figure} figures/p45-tanks-in-stage.svg
:label: fig-p45-tanks-in-stage
:alt: Left: a stage 3.0 meters wide, drawn as two vertical walls, holding two spherical tanks one above the other, touching, to scale. The upper tank, liquid oxygen, has a diameter of 2.475 meters; the lower tank, kerosene, 2.037 meters, each marked by a dimension line across it. A dimension beside the stage gives the length of the two tanks together, 4.51 meters. Each tank is filled with its liquid to a level below the top, and the empty cap above the liquid in each is labeled ullage, 5 percent. Right: two horizontal bars of equal length, split into oxygen and kerosene. Mass: oxygen 71.9 percent, kerosene 28.1 percent. Volume: oxygen 64.2 percent, kerosene 35.8 percent.
:width: 85%

Computed for worked example 2, tanks to scale in the 3.0 m stage. Oxygen is almost three quarters of the mass, but its tank has less than twice the volume of the kerosene tank because liquid oxygen is denser. The bars compare each liquid's share of the mass with its share of the tank volume. Densities from NIST (2023) and Huzel and Huang (1967, Table 1-4).
:::

:::{warning} Include ullage when sizing a tank
If you size a tank to $m/\rho$ alone, it has no gas space. Add the ullage, and use each liquid's own density at its storage temperature. For a low-density propellant such as liquid hydrogen, the tank volume drives the overall dimensions of the stage ([page 1.3](#p13-launch-vehicle)).
:::

### The tank wall

Next we find how thick a tank wall must be to hold its pressure, and what mass that adds. The internal pressure $p$ pushes outward on the wall, placing the wall in tension. We call this tensile force per unit wall area the {term}`hoop stress`, $\sigma$, and we find it from a force balance ({numref}`fig-p45-tank-wall`). Cut a thin-walled cylinder of radius $r$, length $L$, and wall thickness $t_\text{w}$ in half along its length. The pressure pushes the two halves apart with the force $p \times 2rL$, and the two cut walls hold them together with $\sigma \times 2t_\text{w}L$. Setting the two equal gives $\sigma = p\,r/t_\text{w}$. If we cut a sphere through its center instead, the pressure acts over the circular area $\pi r^2$ while the wall stress acts over the ring area $2\pi r\,t_\text{w}$, so the stress is half as large:

:::{math}
:label: eq-p45-hoop
\begin{aligned}
\sigma_\text{cylinder} &= \frac{p\,r}{t_\text{w}}\\
\sigma_\text{sphere} &= \frac{p\,r}{2\,t_\text{w}}
\end{aligned}
:::

:::{figure} figures/p45-tank-wall.svg
:label: fig-p45-tank-wall
:alt: Two free bodies side by side: left, half of a cylinder cut along its length; right, half of a sphere cut through its center. Each is a hatched half ring labeled wall, t w, with pressure arrows, named in a key, pushing outward on its inside, normal to it, and a heavy arrow labeled sigma, the wall stress, pointing down from each cut end. Below each, the cut seen from below: for the cylinder a light rectangle 2r wide and L long, marked 2rL, between two hatched wall strips; for the sphere a light disk of radius r, marked pi r squared, inside a hatched ring. Under them, the force balances give sigma equals p r over t w for the cylinder and p r over 2 t w for the sphere.
:width: 90%

Schematic, not to scale; wall thickness exaggerated. A sphere holds the same pressure at half the wall stress of a cylinder of the same radius and wall: for the same area inside the cut, it has twice as much wall. The pressure on the inside of each half adds up to the pressure times the area inside the cut, and the cut wall carries that force.
:::

Huzel and Huang (1967, Eqs. 8-11 and 8-30) solve these for the wall thickness at an allowable stress $\sigma_\text{allow}$, with the welds taken as strong as the plate (a weld efficiency of 1). The allowable stress is the highest stress the design lets the material carry, below its yield strength. For a sphere, $t_\text{w} = p\,r/(2\sigma_\text{allow})$. Its wall mass is area times thickness times the density $\rho_\text{w}$ of the wall material. With $\mathcal{V} = \tfrac{4}{3}\pi r^3$,

:::{math}
:label: eq-p45-tank-mass
\begin{aligned}
m_\text{tank} &= 4\pi r^2\,t_\text{w}\,\rho_\text{w}\\
&= \frac{3}{2}\,\frac{\rho_\text{w}}{\sigma_\text{allow}}\,p\,\mathcal{V}
\end{aligned}
:::

The wall mass grows with the pressure times the volume. A strong, light material, with a small $\rho_\text{w}/\sigma_\text{allow}$, makes a light tank.

### Worked example 3: the wall of the oxygen tank

Take the oxygen sphere of worked example 2, of radius $2.475/2 = 1.238$ m, made of the aluminum alloy 6061-T6. Huzel and Huang (1967, Section 8.2 and Sample Calculation 8-2) give it an allowable working stress of 31,800 psi (219.3 MPa) and a density of 0.1 lb/in³ (2,768 kg/m³). Find the wall thickness and mass at 0.3 MPa, a pump-fed tank pressure, and at 2.0 MPa, a pressure-fed one.

1. **Thickness, pump-fed**, [](#eq-p45-hoop):
   $$
   \begin{aligned}
   t_\text{w} &= \frac{0.3 \times {10}^{6} \times 1.238}{2 \times 219.3 \times {10}^{6}}\\
              &= 0.000847\ \text{m}
   \end{aligned}
   $$
   That is 0.847 mm.
2. **Wall mass, pump-fed**, [](#eq-p45-tank-mass):
   $$
   \begin{aligned}
   m_\text{tank} &= 4 \times \pi \times {1.238}^{2} \times\\
                 &\;\;\; 0.000847 \times 2{,}768\\
                 &= 45.2\ \text{kg}
   \end{aligned}
   $$
3. **Thickness and mass, pressure-fed.** The thickness grows in proportion to the pressure:
   $$
   \begin{aligned}
   t_\text{w} &= \frac{2.0 \times {10}^{6} \times 1.238}{2 \times 219.3 \times {10}^{6}}\\
              &= 0.00565\ \text{m}
   \end{aligned}
   $$
   That is 5.65 mm of wall.
   $$
   \begin{aligned}
   m_\text{tank} &= 4 \times \pi \times {1.238}^{2} \times\\
                 &\;\;\; 0.00565 \times 2{,}768\\
                 &= 301\ \text{kg}
   \end{aligned}
   $$

**Check.** The pump-fed wall, 0.847 mm, is above the thinnest aluminum stock Huzel and Huang recommend for tanks, 0.020 in (0.508 mm). A real tank is heavier, because its walls also carry thrust, bending, and handling loads, and its welds need extra thickness (Huzel and Huang 1967, Section 8.2). The comparison holds all the same: the pressure-fed tank is almost seven times heavier.

(p45-boil-off)=
## Boil-off

Liquid oxygen and liquid hydrogen are {term}`cryogenic propellants <cryogenic propellant>` that remain liquid only at temperatures far below room temperature. At atmospheric pressure, liquid hydrogen boils at 20.27 K (NIST 2023). Because the propellant is stored at its boiling point, heat that leaks into the tank does not raise the liquid temperature. Instead, it vaporizes some of the liquid, and the vapor must be vented to keep the tank pressure steady. This loss is {term}`boil-off`.

The energy that boils one kilogram of a liquid at its boiling point is its {term}`heat of vaporization`, $h_\text{vap}$. At atmospheric pressure it is 446.1 kJ/kg for hydrogen and 213.1 kJ/kg for oxygen (NIST 2023). The hydrogen values are NIST's for parahydrogen, the form that stored liquid hydrogen settles into (Leachman et al. 2009, Section 3). The values for normal hydrogen, the room-temperature mixture, differ by less than 1%. If heat leaks in at the steady rate $\dot Q$, in watts, and all of it boils liquid, we get the boil-off rate

:::{math}
:label: eq-p45-boil-off
\dot m_\text{boil} = \frac{\dot Q}{h_\text{vap}}
:::

The units check: W over J/kg is (J/s)(kg/J) = kg/s.

### Worked example 4: a hydrogen stage on a four-day coast

A hydrogen stage carries 3,500 kg of liquid hydrogen and coasts for four days before its burn. Heat leaks into its hydrogen tank at 40 W. Find the hydrogen lost to boil-off.

1. **Boil-off rate**, [](#eq-p45-boil-off), with $h_\text{vap}$ in J/kg:
   $$
   \begin{aligned}
   \dot m_\text{boil} &= \frac{40}{446{,}100}\\
                      &= 8.967 \times {10}^{-5}\ \text{kg/s}
   \end{aligned}
   $$
2. **Per day**, with 86,400 s in a day:
   $$
   \begin{aligned}
   \dot m_\text{boil} &= 8.967 \times {10}^{-5} \times\\
                      &\;\;\; 86{,}400\\
                      &= 7.747\ \text{kg/day}
   \end{aligned}
   $$
3. **Over four days.**
   $$
   \begin{aligned}
   m_\text{boil} &= 7.747 \times 4\\
                 &= 30.99\ \text{kg}
   \end{aligned}
   $$
4. **Share of the load.**
   $$
   \begin{aligned}
   \frac{m_\text{boil}}{m} &= \frac{30.99}{3{,}500} \times 100\\
                            &= 0.89\%
   \end{aligned}
   $$

**Check.** Under 1% over four days is small; we add it to the propellant load. Over months, at 7.747 kg a day, it grows large ({numref}`fig-p45-boil-off`). At 160 W the tank would be empty after 113 days.

:::{figure} figures/p45-boil-off.svg
:label: fig-p45-boil-off
:alt: Two panels of hydrogen boiled off in kilograms against coast time in days, for heat leaks of 10, 40, and 160 watts, each a straight line from zero. Left panel, the first 10 days, up to 100 kilograms: a dot on the 40 watt line at 4 days marks 30.99 kilograms. Right panel, six months, up to 4,000 kilograms, with a dashed line at the whole load of 3,500 kilograms: the 160 watt line reaches it at an open dot, empty after 113 days; the 40 watt line reaches about 1,400 kilograms at 180 days and the 10 watt line about 350.
:width: 80%

Computed: the loss grows in proportion to time and to the heat leak, tens of kilograms over a few days and a large part of the load over months. From [](#eq-p45-boil-off) for the 3,500 kg of hydrogen of worked example 4, with a steady heat leak, all of it boiling liquid. The two panels show the same lines at two time scales.
:::

There are four ways to keep the loss small (Plachta, Johnson, and Feller 2014; Huzel and Huang 1967, Section 8.1):

- **Insulation.** Multilayer insulation, many thin reflective sheets around the tank, cuts the heat leak.
- **A shorter wait.** The loss is proportional to the coast time, so a mission that burns sooner loses less.
- **Active cooling.** A cryocooler, a small refrigerator, removes incoming heat, though it requires electric power and adds hardware mass. In a NASA test it stopped the boil-off of liquid oxygen and cut that of liquid hydrogen by 60% (Plachta, Johnson, and Feller 2014).
- **Storable propellants.** A propellant that is liquid at room temperature does not boil away; kerosene, for example, boils only above 172 °C (Huzel and Huang 1967, Table 1-4), and hypergolic pairs are storable in both tanks. The trade-off is a lower specific impulse.

:::{warning} Watch the units of the heat of vaporization
Tables give $h_\text{vap}$ in kJ/kg. If you divide watts by kJ/kg, your boil-off rate comes out 1,000 times too large. Convert to J/kg first. The rate is then in kg/s: multiply by 86,400 for a loss per day.
:::

## Summary

:::{important} Summary
- An engine burns $\dot m = F/(I_\text{sp}\,g_0)$ each second and empties its tanks in $t_b = m_\text{prop}/\dot m$.
- The flow through the throat is $\dot m = p_c A_t/c^*$, where $c^*$ depends on the propellants and their mixture ratio. Halving the chamber pressure doubles the throat. Large engines weigh about one seventieth of their thrust.
- A pump-fed engine keeps its tanks at low pressure; a pressure-fed engine is simpler but needs heavier tanks. Each tank holds its share of the propellant, split with the mixture ratio, plus ullage, and its wall mass grows with pressure times volume.
- A cryogenic propellant boils away at the rate $\dot Q/h_\text{vap}$. That loss is small over a few days, but it becomes a large share of the propellant over several months.
:::

:::{table} The equations of this page.
:label: tbl-p45-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Mass flow from thrust | $\dot m = F/(I_\text{sp}\,g_0)$ |
| Burn time | $t_b = m_\text{prop}/\dot m$ |
| Mass flow through the throat | $\dot m = p_c A_t/c^*$ |
| Oxidizer and fuel mass | $m_\text{ox} = m_\text{prop}\,\text{O/F}/(1 + \text{O/F})$, $m_\text{fuel} = m_\text{prop}/(1 + \text{O/F})$ |
| Tank volume with ullage | $\mathcal{V}_\text{tank} = (1 + u)\,m/\rho$ |
| Diameter of a spherical tank | $d = {(6\,\mathcal{V}_\text{tank}/\pi)}^{1/3}$ |
| Hoop stress | $\sigma = p\,r/t_\text{w}$ (cylinder), $p\,r/(2\,t_\text{w})$ (sphere) |
| Wall mass of a spherical tank | $m_\text{tank} = \tfrac{3}{2}(\rho_\text{w}/\sigma_\text{allow})\,p\,\mathcal{V}$ |
| Boil-off rate | $\dot m_\text{boil} = \dot Q/h_\text{vap}$ |

:::

:::{exercise} For discussion
:label: ex-p45-discussion

1. Two engines give the same thrust with the same propellants. One has twice the chamber pressure of the other. Which one has the smaller throat, and what does its feed system need that the other's does not?
2. Why might a small spacecraft engine be pressure-fed while a first-stage engine is pump-fed?
3. Boil-off grows with the heat leak and with the coast time. Which of the four ways to reduce it acts on the heat leak, which on the time, and what trade-off does each involve?
:::

## References

- Huzel, D. K., and Huang, D. H., *Design of Liquid Propellant Rocket Engines*, NASA SP-125, 1967. Section 1.3 (Eq. 1-32), Section 1.5 (Figures 1-12 and 1-13), Section 2.1, Tables 1-4, 1-9, and 1-10, and Chapter VIII (Sections 8.1 to 8.3, Eqs. 8-1, 8-11, and 8-30, Sample Calculations 8-1 and 8-2).
- NASA, *[Space Shuttle News Reference](https://ntrs.nasa.gov/citations/19810022734)*, 1981. NASA Technical Reports Server 19810022734. Pages 2-4, 2-5, and 2-34.
- NASA, *[Space Transportation System](https://www.nasa.gov/wp-content/uploads/2015/12/3.pdf)*, Historic American Engineering Record HAER No. TX-116, Part III, Space Shuttle Main Engine, 2015. Page 274.
- NASA, "F-1 Engine Fact Sheet," *Saturn V News Reference*, sheet R-1, 1968a.
- NASA, "J-2 Engine Fact Sheet," *Saturn V News Reference*, sheet R-16, 1968b.
- Leachman, J. W., Jacobsen, R. T, Penoncello, S. G., and Lemmon, E. W., "[Fundamental Equations of State for Parahydrogen, Normal Hydrogen, and Orthohydrogen](https://srd.nist.gov/jpcrdreprint/1.3160306.pdf)," *Journal of Physical and Chemical Reference Data*, Vol. 38, No. 3, 2009, pp. 721 to 748. Section 3.
- National Institute of Standards and Technology (NIST), "[NIST Chemistry WebBook, SRD 69](https://webbook.nist.gov/chemistry/fluid/)," thermophysical properties of fluid systems: oxygen and parahydrogen at 0.101325 MPa, 2023.
- Plachta, D. W., Johnson, W. L., and Feller, J. R., "[Cryogenic Boil-Off Reduction System Testing](https://ntrs.nasa.gov/citations/20150000134)," AIAA/ASME/SAE/ASEE Joint Propulsion Conference, 2014. NASA Technical Reports Server 20150000134.
