---
title: "4.4 Propellant Selection"
short_title: 4.4 Propellant Selection
---

:::{include} ../_parts/standards/4.4.md
:::

On the earlier pages of this chapter we took the specific impulse of an engine as a given number. Here we see where it comes from and how an engineer chooses the propellant and the engine. We sort rocket propulsion into its kinds and launch vehicles into their classes, compare the properties that make a propellant good, and decide how much thrust a mission needs. The worked example is a justified choice for a real kind of mission, the last burn of a communications satellite on its way to the geostationary orbit.

:::{note} What to take from this page
- High specific impulse and high thrust rarely come together. Today only chemical rockets give the thrust to leave the ground; electric thrusters give thousands of seconds of specific impulse at a tiny fraction of the thrust.
- Launch vehicles are classed by the payload they place in low Earth orbit, from small (up to 2 t) to super heavy (above 50 t). The payload is a few percent of the liftoff mass.
- A propellant is judged on four things: specific impulse, density, storability, and what it lets the engine do (thrust, throttling, restart). Liquid hydrogen gives the highest specific impulse, but it has the lowest density.
- To justify a choice, size every option with the rocket equation, compare mass and volume with numbers, and state the mass and volume trade-off of the chosen option.
:::

## Two questions

When we select a propulsion system, we answer two questions: how hard the engine must push, and how efficiently it must use its propellant. The first is the {term}`thrust`, $F$, compared with the weight it must lift or move. The second is the {term}`specific impulse`, $I_\text{sp} = F/(\dot m g_0)$, the thrust produced per unit sea-level weight flow rate of propellant ([page 4.1](#p41-specific-impulse)). A launch vehicle must push harder than its own weight, so it needs high thrust first. A spacecraft that has months to reach its target needs little thrust, and every second of specific impulse saves propellant.

:::{warning} Thrust and specific impulse are different things
If you choose an engine for its specific impulse alone, you may pick one that cannot lift its own vehicle. Thrust measures how hard the engine pushes, while specific impulse measures how little propellant it burns for each newton-second of push. The engines with the highest specific impulse produce the lowest thrust, as the next section shows.
:::

(p44-kinds)=
## Kinds of rocket propulsion

Every rocket throws mass backward, so the kinds of propulsion differ in where the energy comes from and how the mass is stored. We start with the words for what a rocket carries.

:::{prf:definition} Propellant, fuel, and oxidizer
:label: def-p44-propellant

The {term}`propellant` is all the mass a rocket carries to throw out of its nozzle. In a chemical rocket it is a {term}`fuel`, which burns, and an {term}`oxidizer`, which supplies the oxygen (or another element) the fuel burns with. A rocket carries its oxidizer because there is no air to burn with in space, and too little high in the atmosphere.
:::

Here are the kinds, from the simplest to the most efficient:

- A {term}`cold-gas thruster` lets a stored gas, often nitrogen, expand out through a nozzle with no combustion. It is simple and safe, and its small, precise pushes suit the pointing of a spacecraft (NASA 2026).
- A {term}`monopropellant` engine uses one liquid that releases energy on its own when it passes over a catalyst. Hydrazine is the usual choice, and the catalyst decomposes it into hot gas (NASA 2026).
- A {term}`bipropellant` engine keeps a fuel and an oxidizer in separate tanks and mixes them only in the combustion chamber (Huzel and Huang 1967, p. 19). This is the engine of most launch vehicles and many spacecraft.
- A {term}`solid rocket motor` carries fuel and oxidizer mixed together in one rubbery solid, the grain, cast inside the motor case. It is the booster of [the launch vehicle on page 1.3](#p13-launch-vehicle), and once lit it burns until the grain is gone.
- A {term}`hybrid rocket` keeps a solid fuel in the case and a liquid or gaseous oxidizer in a tank. It burns only while the oxidizer flows, so a valve starts and stops it (NASA 2026).
- A {term}`nuclear thermal rocket` heats hydrogen in a nuclear reactor instead of burning it. It was tested on the ground in the NERVA program and has not flown (Meyer et al. 2012, p. 4).
- {term}`Electric propulsion` uses electric power to accelerate the propellant. An ion thruster, for example, ionizes xenon and pulls the ions out with high-voltage grids (Meyer et al. 2010, p. 9).

The three fuel-and-oxidizer chemical kinds differ mostly in where the fuel and the oxidizer are stored before they burn ({numref}`fig-p44-engine-kinds`).

:::{figure} figures/p44-engine-kinds.svg
:label: fig-p44-engine-kinds
:alt: Three schematics side by side, nozzles down. Left, a liquid bipropellant engine: a fuel tank and an oxidizer tank feed a fuel pump and an oxidizer pump; the two pumps share a shaft with a turbine driven by a small gas generator; valves below the pumps lead to the thrust chamber. Under it: fuel and oxidizer in separate tanks. Center, a solid motor: a long case filled with solid propellant around a central port, an igniter at the top of the port, and a nozzle. Under it: fuel and oxidizer mixed in the grain. Right, a hybrid: a liquid oxidizer tank above a valve and a short case lined with solid fuel around a port, then a nozzle. Under it: solid fuel in the case, liquid oxidizer in a tank.
:width: 90%

Schematic, not to scale. The three fuel-and-oxidizer chemical rockets differ in where the fuel and the oxidizer are kept before they burn: in two tanks (liquid bipropellant, here with a pump feed), mixed in one solid grain (solid), or split between a solid fuel and a liquid oxidizer (hybrid). The duct that carries the turbine's exhaust overboard is not drawn.
:::

{numref}`tbl-p44-kinds` puts numbers on each kind. No single published table covers every kind, so each row gives the values of the sources named in the caption, for the devices those sources describe.

:::{table} Kinds of rocket propulsion with published values of specific impulse and thrust. Cold gas, hydrazine monopropellant, hybrid, and electric (gridded ion and Hall-effect thrusters): the ranges of the small-spacecraft devices surveyed by NASA (2026, Table 4-1), which do not cover larger hybrids or thrusters. Bipropellant: from the theoretical sea-level value of nitrogen tetroxide and MMH (Huzel and Huang 1967, Table 1-8) to the vacuum value of the RS-25 (NASA 1981, p. 2-4); thrust from the AVUM upper-stage engine of Vega (Arianespace 2014, p. 1-6) to the F-1 at sea level (NASA 1968). Solid: vacuum values of the Ariane 5 booster (Arianespace 2016, p. 1-7; ESA gives 262 s, the value {numref}`fig-p44-isp-thrust-map` plots) and of Vega's Zefiro 9 (Arianespace 2014, p. 1-6), and the Space Shuttle booster at liftoff (NASA 1981, p. 2-18). Nuclear thermal: the NERVA ground tests (Meyer et al. 2012, p. 4).
:label: tbl-p44-kinds
:align: center

<table>
<tr><th>Kind</th><th>Specific impulse, s</th><th>Thrust</th><th>Good at</th><th>Drawback</th></tr>
<tr><th scope="row">Cold gas</th><td>40 to 110</td><td>10&nbsp;µN to 3.6&nbsp;N</td><td>Simple, safe, small precise pushes</td><td>Lowest specific impulse</td></tr>
<tr><th scope="row">Monopropellant (hydrazine)</th><td>180 to 285</td><td>0.25 to 28&nbsp;N</td><td>One tank, simple, long flight record</td><td>Toxic; less specific impulse than a bipropellant</td></tr>
<tr><th scope="row">Liquid bipropellant</th><td>288 to 455.2</td><td>2.45&nbsp;kN to 6,770&nbsp;kN</td><td>High specific impulse with high thrust; throttles and restarts</td><td>Pumps, valves, two tanks; cryogenic propellants boil away</td></tr>
<tr><th scope="row">Solid</th><td>274.5 to 295.9</td><td>317&nbsp;kN to 11,790&nbsp;kN</td><td>High thrust, dense, ready without fueling</td><td>Cannot be shut down or throttled; lower specific impulse</td></tr>
<tr><th scope="row">Hybrid</th><td>215 to 300</td><td>8 to 222&nbsp;N</td><td>Starts and stops with the oxidizer valve; safer to handle than a solid</td><td>Lower combustion efficiency</td></tr>
<tr><th scope="row">Nuclear thermal</th><td>800 to 900</td><td>33.4&nbsp;kN to 1,112&nbsp;kN</td><td>About double the specific impulse of chemical rockets at high thrust</td><td>Reactor and shielding; never flown</td></tr>
<tr><th scope="row">Electric (ion and Hall)</th><td>200 to 3,000</td><td>0.1 to 55&nbsp;mN</td><td>Highest specific impulse</td><td>Needs electric power; burns last hundreds of hours</td></tr>
</table>

:::

Read the table down the thrust column and then down the specific impulse column, and notice that the order is nearly reversed, as plotted in {numref}`fig-p44-isp-thrust-map`. Today only chemical propulsion can lift a vehicle off the ground, because it alone gives more thrust than the vehicle's weight (Meyer et al. 2012, p. 3). Because electric propulsion is limited by power, it gives less than 75 mN for each kilowatt, so a spacecraft with 500 W for its thruster gets no more than 38 mN (NASA 2026). Ion thrusters in general, beyond the small devices of the table, reach 2,000 to over 10,000 s (Meyer et al. 2010, p. 9). They must fire for hundreds or thousands of hours to give the impulse a chemical engine gives in minutes (NASA 2026).

:::{figure} figures/p44-isp-thrust-map.svg
:label: fig-p44-isp-thrust-map
:alt: Log-log chart of specific impulse, 20 to 10,000 seconds, against thrust, 10 to the minus 5 to 10 to the 9 newtons. Boxes, which a note marks as small-spacecraft devices only: cold gas, lowest, at 40 to 110 seconds and 10 micronewtons to 3.6 newtons; electric propulsion, tall, at 200 to 3,000 seconds but only 0.1 to 55 millinewtons; hydrazine monopropellant and hybrids near 200 to 300 seconds at 0.25 to 222 newtons. A thin nuclear thermal box lies at 800 to 900 seconds and 33 kilonewtons to 1.1 meganewtons. Circles for the liquid engines AVUM, HM7B, J-2, Vulcain 2, and RS-25 lie at 314.6 to 455.2 seconds and 2.45 kilonewtons to 2.1 meganewtons; squares for Zefiro 9, P80, and the Ariane 5 booster at liftoff at 262 to 296 seconds and 317 kilonewtons to 5.4 meganewtons.
:width: 85%

Values from the sources of {numref}`tbl-p44-kinds`: the devices with the highest specific impulse give the lowest thrust, and only chemical engines and motors reach several meganewtons. The cold gas, monopropellant, hybrid, and electric boxes are the ranges of small-spacecraft devices (NASA 2026, Table 4-1); larger hybrids and thrusters exist. Circles are liquid engines and squares solid motors, in vacuum except the Ariane 5 booster, drawn at its thrust at liftoff, 5,400 kN, with a specific impulse of 262 s (ESA n.d.d). Specific impulse against thrust on logarithmic axes.
:::

(p44-launch-vehicles)=
## Classifying launch vehicles

We describe a launch vehicle first by what it can carry. NASA classes launch vehicles by the payload they place in low Earth orbit (McConnaughey et al. 2012, p. 2). Small vehicles carry up to 2 t and medium ones 2 to 20 t. Heavy vehicles carry 20 to 50 t, and super heavy ones more than 50 t. Three more descriptions complete the picture:

- **Stages and boosters.** How many stages burn one after the other, and whether boosters burn beside the core at liftoff ([multistage rockets](#p43-top-down)).
- **Propellant of each stage.** Solid, {term}`storable <storable propellant>` liquid, or {term}`cryogenic <cryogenic propellant>` liquid, stage by stage.
- **Expendable or reusable.** The Falcon 9 first stage is designed to be recovered and flown again (SpaceX 2025, Section 2), and the Space Shuttle's solid boosters were recovered and refurbished (NASA 1981, p. 2-18). Most other stages are used once.

:::{table} Ten launch vehicles, classed by their published payload to low Earth orbit. Each source quotes its own orbit (sun-synchronous orbits for Electron and PSLV-XL, a 500 km polar orbit for Vega C, the orbit of the International Space Station for Ariane 5 ES, whose payload there is 19,000 to 21,000 kg and whose liftoff mass is that of its Galileo flights), so the payloads compare only roughly. Sources: Rocket Lab (2022), ISRO (n.d.a, n.d.b), Arianespace (2018, 2016), ESA (n.d.a, n.d.b, n.d.c), SpaceX (2019a, 2019b), NASA (2022), Bilstein (1996), and NASA (1969).
:label: tbl-p44-launch-vehicles
:align: center

<table>
<tr><th>Vehicle</th><th>Payload to low Earth orbit, kg</th><th>Liftoff mass, t</th><th>Payload share of liftoff mass, %</th><th>Class</th><th>Propellants</th></tr>
<tr><th scope="row">Electron</th><td class="num">200</td><td class="num">13.00</td><td class="num">1.5</td><td>small</td><td>liquid oxygen and kerosene</td></tr>
<tr><th scope="row">PSLV-XL</th><td class="num">1,750</td><td class="num">320.0</td><td class="num">0.55</td><td>small</td><td>solid; storable liquids</td></tr>
<tr><th scope="row">Vega C</th><td class="num">2,250</td><td class="num">210.0</td><td class="num">1.1</td><td>medium</td><td>solid; storable upper stage</td></tr>
<tr><th scope="row">LVM3</th><td class="num">8,000</td><td class="num">640.0</td><td class="num">1.3</td><td>medium</td><td>solid; storable; oxygen and hydrogen</td></tr>
<tr><th scope="row">Ariane 5 ES</th><td class="num">19,000</td><td class="num">760.0</td><td class="num">2.5</td><td>medium</td><td>oxygen and hydrogen; solid; storable upper stage</td></tr>
<tr><th scope="row">Falcon 9</th><td class="num">22,800</td><td class="num">549.1</td><td class="num">4.2</td><td>heavy</td><td>liquid oxygen and kerosene</td></tr>
<tr><th scope="row">Space Shuttle</th><td class="num">24,310</td><td class="num">2,000</td><td class="num">1.2</td><td>heavy</td><td>oxygen and hydrogen; solid</td></tr>
<tr><th scope="row">Falcon Heavy</th><td class="num">63,800</td><td class="num">1,421</td><td class="num">4.5</td><td>super heavy</td><td>liquid oxygen and kerosene</td></tr>
<tr><th scope="row">SLS Block 1</th><td class="num">95,000</td><td class="num">2,603</td><td class="num">3.6</td><td>super heavy</td><td>oxygen and hydrogen; solid</td></tr>
<tr><th scope="row">Saturn V</th><td class="num">113,400</td><td class="num">2,906</td><td class="num">3.9</td><td>super heavy</td><td>oxygen and kerosene; oxygen and hydrogen</td></tr>
</table>

:::

The payload share column in {numref}`tbl-p44-launch-vehicles` shows the main takeaway. Every one of these vehicles puts between 0.55% and 4.5% of its liftoff mass into orbit. The rest, at least 95.5%, is propellant and inert mass. That is what [the rocket equation](#p42-rocket-equation) predicts for a launch budget such as the 8.833 km/s of [launch to orbit](#p23-budget). So the classes by payload are also classes by liftoff mass ({numref}`fig-p44-launch-vehicle-classes`). The lowest shares belong to vehicles quoted for harder orbits (PSLV-XL and Vega C to polar orbits) or carrying a heavy reusable orbiter (the Space Shuttle).

:::{figure} figures/p44-launch-vehicle-classes.svg
:label: fig-p44-launch-vehicle-classes
:alt: Log-log chart of payload to low Earth orbit, 100 to 300,000 kilograms, against liftoff mass, 5,000 to 20 million kilograms. Horizontal bands mark the classes: small lift below 2,000 kilograms, medium lift to 20,000, heavy lift to 50,000, super heavy lift above. Two parallel dotted diagonal lines mark a payload of 0.3% and of 10% of the liftoff mass. Ten named points rise from lower left to upper right between the two lines: Electron at 13 tonnes and 200 kilograms in the small band; PSLV-XL and Vega C near the small and medium boundary; LVM3 and Ariane 5 ES in the medium band; Falcon 9 and the Space Shuttle in the heavy band; Falcon Heavy, SLS Block 1, and Saturn V in the super heavy band.
:width: 85%

Values from {numref}`tbl-p44-launch-vehicles`: payload grows in proportion to liftoff mass, so the classes by payload are also classes by liftoff mass. Every vehicle lies between the dotted lines of 0.3% and 10% of liftoff mass. Payload to low Earth orbit against liftoff mass, with the four classes of McConnaughey et al. (2012); the payloads are quoted for different orbits.
:::

(p44-propellant-properties)=
## What makes a propellant good

Now we compare the propellants themselves. Huzel and Huang (1967, p. 20) list fourteen features of a good liquid propellant and warn that every propellant has disadvantages, so the choice is a compromise. Four of these properties drive most design choices: specific impulse, density, storability, and what the propellant lets the engine do. {numref}`tbl-p44-propellants` gives published values for the common pairs. The specific impulses there are theoretical, for one chamber pressure and a nozzle expanded to sea-level pressure. Real engines give 5 to 12% less (Huzel and Huang 1967, p. 21), and a vacuum nozzle gives more ([area ratio](#p41-area-ratio)). Use the table to compare propellant pairs on the same basis, because real engine data sheets use different chamber pressures and nozzle expansions.

:::{table} Theoretical performance of common propellants. Liquid pairs: Huzel and Huang (1967), Tables 1-8 to 1-10, for a chamber pressure of 1,000 psia (6.895 MPa) expanded to 14.7 psia, at the mixture ratio of best performance. Hydrazine: Table 1-6, at 300 psia. Solid: NASA (1971), Table I, at 1,000 psia.
:label: tbl-p44-propellants
:align: center

<table>
<tr><th>Propellants</th><th>Class</th><th>Mixture ratio, O/F</th><th>Specific impulse, s</th><th>Bulk density, kg/m³</th><th>Chamber temperature, K</th><th>Molecular weight of the exhaust</th></tr>
<tr><th scope="row">Liquid oxygen and liquid hydrogen</th><td>cryogenic bipropellant</td><td class="num">4.02</td><td class="num">391</td><td class="num">280</td><td class="num">2,997</td><td class="num">10.0</td></tr>
<tr><th scope="row">Liquid oxygen and kerosene (RP-1)</th><td>bipropellant, cryogenic oxidizer</td><td class="num">2.56</td><td class="num">300</td><td class="num">1,020</td><td class="num">3,672</td><td class="num">23.3</td></tr>
<tr><th scope="row">Nitrogen tetroxide and MMH</th><td>storable bipropellant, hypergolic</td><td class="num">2.16</td><td class="num">288</td><td class="num">1,200</td><td class="num">3,386</td><td>not given</td></tr>
<tr><th scope="row">Nitrogen tetroxide and UDMH</th><td>storable bipropellant, hypergolic</td><td class="num">2.61</td><td class="num">285</td><td class="num">1,180</td><td class="num">3,414</td><td class="num">23.6</td></tr>
<tr><th scope="row">Hydrazine</th><td>storable monopropellant</td><td>does not apply</td><td class="num">205</td><td class="num">1,010</td><td>not given</td><td>not given</td></tr>
<tr><th scope="row">Ammonium perchlorate, aluminum, and HTPB binder</th><td>solid</td><td>does not apply</td><td class="num">260 to 265</td><td class="num">1,772</td><td class="num">3,366 to 3,478</td><td>not given</td></tr>
</table>

:::

MMH is monomethylhydrazine and UDMH is unsymmetrical dimethylhydrazine, two fuels made from hydrazine. The {term}`mixture ratio`, O/F, is the mass of oxidizer burned for each kilogram of fuel.

### Specific impulse

A fast exhaust needs two things: a large energy release per kilogram of propellant and light exhaust molecules (Huzel and Huang 1967, p. 20). At the same temperature, lighter gas molecules move faster. Look at the first two rows of {numref}`tbl-p44-propellants`. Oxygen and kerosene burn hotter, 3,672 K against 2,997 K. Even so, oxygen and hydrogen give 1.303 times the specific impulse, because their exhaust, mostly water and hydrogen, has a molecular weight of 10.0 against 23.3. This is also why hydrogen engines run fuel-rich, with more hydrogen than complete combustion requires. The unburned hydrogen lowers the molecular weight of the exhaust (Huzel and Huang 1967, p. 20). How the chamber temperature and the molecular weight set the exhaust velocity is the subject of a later course in rocket propulsion.

### Density

A propellant must fit in tanks, and tanks are inert mass. So we need the volume that a mass of propellant fills:

```{math}
:label: eq-p44-volume
\mathcal{V} = \frac{m}{\rho}
```

where $m$ is the mass, $\rho$ the density, and $\mathcal{V}$ the volume (script V, so we do not confuse it with a velocity). A pair has two tanks, one for each liquid. Their total volume per kilogram of propellant gives the {term}`bulk density` of the pair. With the mixture ratio O/F, a kilogram of propellant contains $\text{O/F}/(1 + \text{O/F})$ kg of oxidizer and $1/(1 + \text{O/F})$ kg of fuel, so (Huzel and Huang 1967, Eq. 1-46)

```{math}
:label: eq-p44-bulk
\rho_\text{bulk} = \frac{1 + \text{O/F}}{\dfrac{\text{O/F}}{\rho_\text{ox}} + \dfrac{1}{\rho_\text{fuel}}}
```

Liquid hydrogen is the extreme case. At its boiling point it has a density of 70.83 kg/m³; liquid oxygen, at 1,141 kg/m³, is 16.1 times denser (NIST 2023). With these densities and the mixture ratio of 4.02, [](#eq-p44-bulk) gives a bulk density of 284.6 kg/m³ for oxygen and hydrogen; Huzel and Huang (1967, Table 1-10) list 280. The oxygen and kerosene pair, at 1,020 kg/m³, is 3.6 times denser.

The higher specific impulse of hydrogen means less propellant mass for the same job. To see whether that makes the stage smaller, we compare two loads with the same total impulse, the propellant mass times its effective exhaust velocity. For example, 100.0 t of oxygen and kerosene gives the same total impulse as 76.73 t of oxygen and hydrogen (100.0 t times 300/391), and {numref}`fig-p44-tank-volumes` draws their tanks to scale. The hydrogen load is 23% lighter, yet it needs 2.748 times the volume, 269.6 m³ against 98.12 m³. That is why hydrogen stages are long and wide, and why the biggest tank in a hydrogen stage carries the fuel (see [the launch vehicle on page 1.3](#p13-launch-vehicle)).

:::{figure} figures/p44-tank-volumes.svg
:label: fig-p44-tank-volumes
:alt: Two rows of tanks of one diameter, 4.0 meters, lying on their side and drawn to the same scale, with a 5 meter scale bar. Top row, oxygen and kerosene, 100.0 tonnes and 98.12 cubic meters: a liquid oxygen tank of 63.01 cubic meters and a shorter kerosene tank of 35.11 cubic meters. Bottom row, oxygen and hydrogen with the same total impulse, 76.73 tonnes and 269.6 cubic meters: a liquid oxygen tank of 53.84 cubic meters and a liquid hydrogen tank of 215.8 cubic meters. A note under the bottom row gives 2.748 times the volume of the kerosene load.
:width: 85%

Computed, to scale: for the same total impulse, the lighter hydrogen load needs 2.748 times the tank volume of the kerosene load. Specific impulses and mixture ratios of {numref}`tbl-p44-propellants`; liquid densities of NIST (2023); for kerosene, 800 kg/m³, the low end of the range of Huzel and Huang (1967, Table 1-4), as on the page on engines and tanks. Tanks drawn as cylinders 4.0 m in diameter, with no walls, domes, or gas space.
:::

{numref}`fig-p44-isp-density` plots both properties together. An ideal propellant would lie in the upper right corner, with both high specific impulse and high density, but no real propellant is there.

:::{figure} figures/p44-isp-density.svg
:label: fig-p44-isp-density
:alt: Scatter chart of specific impulse, 240 to 420 seconds, against bulk density, 0 to 2,000 kilograms per cubic meter. Oxygen and hydrogen lie alone at upper left, 391 seconds at 280 kilograms per cubic meter. Oxygen and kerosene is at 300 seconds and 1,020. Nitrogen tetroxide with MMH and with UDMH are close together near 285 to 288 seconds and 1,180 to 1,200. A filled square for the solid propellant is at lower right, 260 to 265 seconds at 1,772. Arrows at lower left point up, labeled higher specific impulse: less propellant mass, and right, labeled higher density: smaller tanks.
:width: 80%

Values from {numref}`tbl-p44-propellants`: liquid hydrogen has the highest specific impulse and the lowest density, the solid propellant has the reverse, and the storable pairs lie between them. Theoretical specific impulse at sea-level expansion against bulk density.
:::

### Storability

A propellant that boils below room temperature must be kept cold, and some of it boils away while the vehicle is on the pad or coasting in space ([boil-off](#p45-boil-off)). Huzel and Huang (1967, p. 19) sort liquid propellants by this property.

:::{prf:definition} Cryogenic, storable, and hypergolic propellants
:label: def-p44-storability

A {term}`cryogenic propellant` is a liquefied gas that boils below −146 °C at sea-level pressure, such as liquid oxygen, liquid hydrogen, or liquid methane. A {term}`storable propellant` stays liquid over a reasonable range of temperature and pressure and can be kept in closed tanks for a year or more. Two propellants are {term}`hypergolic` when they ignite on contact, with no igniter (Huzel and Huang 1967, p. 19).
:::

{numref}`fig-p44-storage-temperatures` shows what "storable" means on a thermometer. Liquid hydrogen boils at −253 °C, liquid oxygen at −183 °C, and liquid methane at −161 °C (NIST 2023). Room temperature, 20 °C, lies inside the liquid range of nitrogen tetroxide, MMH, hydrazine, and kerosene. Nitrogen tetroxide is close to its boiling point, 21 °C, which is one reason it is kept in closed tanks. Hydrazine freezes at 1.4 °C, so a spacecraft must keep it warm. Solid propellants are cast in the motor case at the factory and stay stored there.

:::{figure} figures/p44-storage-temperatures.svg
:label: fig-p44-storage-temperatures
:alt: Chart of temperature, 0 to 600 kelvin on the left axis, with the same scale in degrees Celsius on the right. Six vertical bars show the liquid range of each propellant at sea-level pressure, from freezing point to boiling point, with a heavy line at the boiling point. Liquid hydrogen and liquid oxygen have short bars near the bottom, labeled boils at minus 253 and at minus 183 degrees Celsius, below a dotted line at minus 146 degrees Celsius labeled cryogenic: boils below this line. Nitrogen tetroxide spans minus 12 to 21 degrees Celsius, MMH minus 53 to 86, hydrazine 1.4 to 113, and kerosene minus 44 to 172. A dashed line at room temperature, 20 degrees Celsius, runs behind these four bars, just under the top of the nitrogen tetroxide bar.
:width: 85%

Values from Huzel and Huang (1967, Tables 1-4 and 1-5) and NIST (2023): a storable propellant is liquid at room temperature; a cryogenic one boils far below it and must be kept cold. Liquid range of six propellants at sea-level pressure.
:::

Ignition and handling come with storability. Hypergolic pairs such as nitrogen tetroxide with MMH or UDMH need no igniter, which makes restarts simple. The hazard is that any leak that mixes them can cause a fire or explosion (Huzel and Huang 1967, p. 19). Hydrazine, its relatives, and nitrogen tetroxide are toxic (Huzel and Huang 1967, Table 1-4), so ground handling requires extra procedures and protective equipment. Oxygen and hydrogen are not toxic, but they must be loaded just before launch.

### Thrust, throttling, and restart

The last property we look at is what the propellant lets the engine do. A solid motor gives high thrust from a compact, dense package, but it cannot be shut down or throttled; its thrust history is set when the grain is cast. A liquid engine can both throttle and shut down. The RS-25 throttles from 65 to 109% of its rated power (NASA 1981, p. 2-4). The storable AVUM upper stage of Vega restarts up to 5 times in one flight (Arianespace 2014, Section 2.3). A hybrid also stops and restarts, by closing and opening its oxidizer valve.

:::{warning} Light propellant does not mean a small stage
If you compare propellants by mass alone, oxygen and hydrogen always give the lowest propellant mass. Compare the volume too, because the same job can require almost three times the tank volume, and larger tanks add inert mass and frontal area. Always compute both the mass and the volume of every option.
:::

(p44-thrust-to-weight)=
## How much thrust

Now we come back to the first question: how hard the engine must push. The {term}`thrust-to-weight ratio` $F/W$ compares the thrust with the weight of the vehicle,

```{math}
:label: eq-p44-fw
\frac{F}{W} = \frac{F}{m g_0}
```

with $m$ the mass of the vehicle at that moment and $g_0$ = 9.81 m/s². At liftoff $F/W$ must be above 1, or the vehicle cannot leave the pad, and being just above 1 is not enough. Until the vehicle builds speed, most of its thrust supports it against gravity, which creates the [gravity loss](#p42-losses). Launch vehicles lift off at 1.19 to 1.46 ({numref}`tbl-p44-fw`).

:::{table} Thrust-to-weight ratio at liftoff of four launch vehicles, from published liftoff thrusts and the liftoff masses of {numref}`tbl-p44-launch-vehicles`. Saturn V: five F-1 engines at their uprated sea-level thrust (NASA 1968). Space Shuttle: two boosters at liftoff and three main engines at rated power at sea level (NASA 1981, pp. 2-4 and 2-18). Falcon 9: SpaceX (2019a). SLS Block 1: NASA (2022).
:label: tbl-p44-fw
:align: center

<table>
<tr><th>Vehicle</th><th>Liftoff thrust, kN</th><th>Liftoff mass, t</th><th>Thrust-to-weight ratio</th></tr>
<tr><th scope="row">Saturn V</th><td class="num">33,851</td><td class="num">2,906</td><td class="num">1.19</td></tr>
<tr><th scope="row">Falcon 9</th><td class="num">7,607</td><td class="num">549.1</td><td class="num">1.41</td></tr>
<tr><th scope="row">SLS Block 1</th><td class="num">36,786</td><td class="num">2,603</td><td class="num">1.44</td></tr>
<tr><th scope="row">Space Shuttle</th><td class="num">28,584</td><td class="num">2,000</td><td class="num">1.46</td></tr>
</table>

:::

This is why Ariane 5 has boosters. On [page 4.2](#p42-feasibility) we found that its core stage alone has a thrust-to-weight ratio of 0.53 at liftoff, so it cannot lift even itself. The two solid boosters give about 92% of the thrust at liftoff (ESA n.d.d), and together with the core they lift the vehicle.

A stage that burns in orbit does not fight gravity directly, so it can push gently. The ESC-A upper stage of Ariane 5 gives 67 kN for a loaded mass of 19,440 kg, a ratio of 0.351 before it carries any payload. Electric propulsion produces even lower thrust, which is why its burns last hundreds or thousands of hours.

:::{warning} A ratio below 1 at liftoff
If you find $F/W$ below 1 at liftoff, the vehicle stays on the pad while it burns propellant. Use the mass at liftoff, propellant included, and $g_0$ = 9.81 m/s², not the local gravity of another body.
:::

(p44-justify)=
## Justifying a choice

Choosing a propellant and an engine is a small trade study ([decision matrix](#p17-decision-matrix)). A propulsion system is designed in a cycle of seven steps:

1. Define the requirements: the delta-V of each maneuver and the thrust or thrust-to-weight ratio.
2. Set the criteria for judging the options: what is feasible, and what counts most (mass, volume, simplicity, safety, cost).
3. Size the vehicle for each option with the rocket equation, from historical values of specific impulse and inert mass fraction.
4. Size the engine or motor.
5. Size the propellant tanks and the system that feeds the engine ([engines and tanks](#p45-tanks)).
6. Compare the options and choose.
7. Iterate, and write down the reasons for every choice.

This page covers steps 1 to 3 and 6 of that cycle. The method below breaks them into six steps of its own, and the worked example follows them.

:::{tip} Method: justifying a choice of propellant and engine
1. Write down what the mission needs most: the delta-V and the thrust, how long the propellant must be stored before firing, and how many burns the mission requires. Add any rule on safety or toxicity.
2. List the options that can meet those needs. A mission lasting years rules out cryogenic propellants, and a mission with several burns rules out a single solid motor.
3. Classify each option: solid, monopropellant, or bipropellant; cryogenic or storable; hypergolic or not.
4. Size each option with the rocket equation ([sizing a stage](#p42-stage-sizing)), with a cited specific impulse and inert mass fraction. Find the propellant mass, the initial mass, and the propellant volume from [](#eq-p44-volume).
5. Compare the options on specific impulse, density, storability, and thrust, with the numbers side by side.
6. Choose, and state the mass and volume trade-off in kilograms and cubic meters.
:::

### Worked example: the apogee engine of a communications satellite

A geostationary communications satellite rides a launch vehicle to a transfer orbit. The satellite must then make the last burn itself, at the apogee of that orbit, to circle Earth once a day over the equator. We compare a solid apogee motor with a storable bipropellant engine for this burn and choose one.

**Step 1. Requirement.** The launch vehicle leaves the satellite in a transfer orbit with a perigee altitude of 250 km and an apogee altitude of 35,786 km. These are the altitudes of Ariane 5's standard transfer orbit (Arianespace 2016, Section 2.4.1). That real orbit is also tilted 6° to the equator, and the real apogee burn turns the orbit plane while it raises the speed, which requires a little more delta-V. Page 2.2 does not teach that combined burn, so we take the transfer orbit in the equator plane. Without its apogee propulsion system, the satellite has a mass of $m_\text{pay}$ = 2,350 kg and must operate for many years. Here we size only the apogee burn.

**Step 2. Options.**

- *A, solid motor.* We model this option on Vega's third stage, Zefiro 9, which has a vacuum specific impulse of 295.9 s (Arianespace 2014, p. 1-6). Out of its 12,000 kg gross mass, 10,567 kg is propellant and 1,433 kg is inert mass, giving an inert mass fraction of 1,433/12,000 = 0.1194. Its propellant density is 1,772 kg/m³ ({numref}`tbl-p44-propellants`).
- *B, storable bipropellant.* We model this option on the engine of Vega's AVUM stage, a {term}`pressure-fed <Pressure-fed>` engine burning nitrogen tetroxide and UDMH at 314.6 s in vacuum. The stage is loaded with 381 kg of oxidizer and 196 kg of fuel (Arianespace 2014, p. 1-6). Their densities are 1,440 and 789 kg/m³ (Huzel and Huang 1967, Table 1-4). AVUM's own inert mass gives an inert mass fraction of 0.544, but it includes the launcher's guidance and electronics, so it does not fit a satellite. We assume $f_\text{inert}$ = 0.20 for the tanks, pressurizing gas, valves, and engine, which is higher than the value for large solid motors because pressure-fed tanks need thick walls ([engines and tanks](#p45-tanks)).

**Step 3. Classify.** Option A is a solid motor, while option B is a storable, hypergolic bipropellant that needs no igniter and can restart.

**Step 4a. Delta-V of the apogee burn.** With Earth's radius 6,378 km and $\mu = 3.986 \times {10}^{5}\ \text{km}^3/\text{s}^2$ ([orbit transfers](../chapter-2/orbit-transfers.md)), the transfer orbit has $r_p$ = 6,628 km, $r_a$ = 42,164 km, and $a$ = 24,396 km. The [vis-viva equation](#p21-vis-viva) gives the speed at apogee, and the circular speed of the geostationary orbit follows:

$$
\begin{aligned}
\frac{2}{r_a} - \frac{1}{a} &= \frac{2}{42{,}164}\\
  &\;\;\; - \frac{1}{24{,}396}\\
  &= 6.4435 \times {10}^{-6}\ \text{km}^{-1}
\end{aligned}
$$

$$
\begin{aligned}
v_a^2 &= \mu\left(\frac{2}{r_a} - \frac{1}{a}\right)\\
  &= 3.986 \times {10}^{5} \times\\
  &\;\;\; 6.4435 \times {10}^{-6}\\
  &= 2.5684\ \text{km}^2/\text{s}^2\\
v_a &= \sqrt{2.5684}\\
  &= 1.603\ \text{km/s}
\end{aligned}
$$

$$
\begin{aligned}
v_\text{GEO} &= \sqrt{\frac{\mu}{r_a}}\\
             &= \sqrt{\frac{3.986 \times {10}^{5}}{42{,}164}}\\
             &= 3.075\ \text{km/s}
\end{aligned}
$$

In the equator plane the transfer orbit and the geostationary orbit touch at apogee, and the two velocities point the same way there. So the burn adds only the difference in speed, as the second burn of a Hohmann transfer does ([orbit transfers](#p22-hohmann)):

$$
\begin{aligned}
\Delta V &= v_\text{GEO} - v_a\\
  &= 3.075 - 1.603\\
  &= 1.472\ \text{km/s}
\end{aligned}
$$

That is 1,472 m/s.

**Step 4b. Size option A** with $c = I_\text{sp} g_0$ and the stage sizing of [page 4.2](#p42-stage-sizing):

$$
\begin{aligned}
c &= 295.9 \times 9.81\\
  &= 2{,}903\ \text{m/s}\\
\frac{\Delta V}{c} &= \frac{1{,}472}{2{,}903}\\
  &= 0.50706\\
e^{\Delta V/c} &= e^{0.50706}\\
  &= 1.6604
\end{aligned}
$$

$$
\begin{aligned}
\text{numerator} &= m_\text{pay} \times\\
  &\;\;\; \left(e^{\Delta V/c} - 1\right) \times\\
  &\;\;\; \left(1 - f_\text{inert}\right)\\
  &= 2{,}350 \times\\
  &\;\;\; 0.6604 \times 0.8806\\
  &= 1{,}367\ \text{kg}\\
\text{denominator} &= 1 - f_\text{inert}\,e^{\Delta V/c}\\
  &= 1 - 0.1194 \times\\
  &\;\;\; 1.6604\\
  &= 0.80175
\end{aligned}
$$

$$
\begin{aligned}
m_\text{prop} &= \frac{1{,}367}{0.80175}\\
  &= 1{,}705\ \text{kg}\\
m_\text{inert} &= \frac{0.1194 \times 1{,}705}{1 - 0.1194}\\
  &= 231.2\ \text{kg}\\
m_i &= 2{,}350 + 231.2 + 1{,}705\\
  &= 4{,}286\ \text{kg}\\
\mathcal{V} &= \frac{1{,}705}{1{,}772}\\
  &= 0.9622\ \text{m}^3
\end{aligned}
$$

**Step 4c. Size option B** the same way:

$$
\begin{aligned}
c &= 314.6 \times 9.81\\
  &= 3{,}086\ \text{m/s}\\
\frac{\Delta V}{c} &= \frac{1{,}472}{3{,}086}\\
  &= 0.47699\\
e^{\Delta V/c} &= e^{0.47699}\\
  &= 1.6112
\end{aligned}
$$

$$
\begin{aligned}
\text{numerator} &= 2{,}350 \times\\
  &\;\;\; 0.6112 \times 0.80\\
  &= 1{,}149\ \text{kg}\\
\text{denominator} &= 1 - 0.20 \times\\
  &\;\;\; 1.6112\\
  &= 0.67776\\
m_\text{prop} &= \frac{1{,}149}{0.67776}\\
  &= 1{,}695\ \text{kg}\\
m_\text{inert} &= \frac{0.20 \times 1{,}695}{1 - 0.20}\\
  &= 423.8\ \text{kg}\\
m_i &= 2{,}350 + 423.8\\
  &\;\;\; + 1{,}695\\
  &= 4{,}469\ \text{kg}
\end{aligned}
$$

The two liquids go in two tanks. AVUM's load gives the mixture ratio, 381/196 = 1.944, so

$$
\begin{aligned}
m_\text{ox} &= \frac{1{,}695 \times 1.944}{1 + 1.944}\\
  &= 1{,}119\ \text{kg}\\
m_\text{fuel} &= \frac{1{,}695}{1 + 1.944}\\
  &= 575.7\ \text{kg}\\
\mathcal{V}_\text{ox} &= \frac{1{,}119}{1{,}440}\\
  &= 0.7771\ \text{m}^3\\
\mathcal{V}_\text{fuel} &= \frac{575.7}{789}\\
  &= 0.7297\ \text{m}^3
\end{aligned}
$$

and the propellant fills 0.7771 + 0.7297 = 1.507 m³. Checking with [](#eq-p44-bulk), the bulk density is 1,695/1.507 = 1,125 kg/m³. It lies between the densities of the two liquids, nearer the oxidizer's, as it should with almost twice as much oxidizer by mass.

**Step 5. Compare** ({numref}`fig-p44-example`). The two options burn almost the same propellant mass. The bipropellant's higher specific impulse is offset by its heavier tanks and pressurizing gas. Option B starts 183 kg heavier (4.3%) and needs 0.545 m³ more volume (57%).

:::{figure} figures/p44-example.svg
:label: fig-p44-example
:alt: Two panels of horizontal bars for the solid motor and the storable bipropellant. Upper panel, mass at the start of the burn: each bar is the payload of 2,350 kilograms, then the inert mass, then the propellant. The solid motor has 231.2 kilograms of inert mass and 1,705 of propellant, 4,286 in all; the bipropellant has 423.8 kilograms of inert mass and 1,695 of propellant, 4,469 in all, marked as 183 kilograms more. Lower panel, propellant volume: the solid propellant fills 0.9622 cubic meters; the bipropellant fills 1.507 cubic meters, split into nitrogen tetroxide, 0.7771, and UDMH, 0.7297, marked as 0.545 cubic meters more.
:width: 80%

Computed for the worked example: the storable bipropellant burns almost the same propellant mass as the solid motor but carries more inert mass. It starts 183 kg heavier and needs 0.545 m³ more volume in exchange for the ability to stop and restart. Mass at the start of the apogee burn and propellant volume of the two options.
:::

**Step 6. Choose.** We recommend the storable bipropellant, option B. The satellite needs the burn to be accurate, and a liquid engine can split the 1,472 m/s into several burns at successive apogees and correct the orbit between them. A solid motor fires once until it is empty. The satellite must also make small burns to maintain its position for years, and a liquid system can supply them from the same tanks. With a solid apogee motor it would need a second, liquid system anyway, and we have not counted that mass. The storable propellants stay stored in their tanks without boiling. The trade-off for this capability is 183 kg of extra initial mass and 0.545 m³ of extra tank volume.

**Check.** The comparison depends on the assumed inert mass fraction of option B, because a lighter bipropellant system would close the 183 kg gap while a heavier one would widen it. Put option A back into the rocket equation. Its mass after the burn is the payload plus the inert mass, 2,581 kg, and $2{,}903 \ln(4{,}286/2{,}581)$ gives 1,472 m/s, the requirement.

## What real vehicles burn, and why

With the same reasoning we can explain what the vehicles of Chapter 1 and of this page burn ({numref}`tbl-p44-real`).

:::{table} What some real vehicles burn, and the main property behind the choice. Propellants from the sources of {numref}`tbl-p44-launch-vehicles` and Arianespace (2016, p. 1-7); the reasons follow from the numbers on this page.
:label: tbl-p44-real
:align: center

<table>
<tr><th>Vehicle or stage</th><th>Propellants</th><th>Reason for the choice</th></tr>
<tr><th scope="row">Saturn V, first stage</th><td>liquid oxygen and kerosene</td><td>Density and thrust: the stage that lifts the whole vehicle needs the most thrust from the smallest tanks</td></tr>
<tr><th scope="row">Saturn V, second and third stages</th><td>liquid oxygen and liquid hydrogen</td><td>Specific impulse: every kilogram saved high up is a kilogram the stages below do not lift</td></tr>
<tr><th scope="row">Falcon 9, both stages</th><td>liquid oxygen and kerosene</td><td>Density, and one pair of propellants for both stages</td></tr>
<tr><th scope="row">Ariane 5, core stage</th><td>liquid oxygen and liquid hydrogen</td><td>Specific impulse over a long burn</td></tr>
<tr><th scope="row">Ariane 5, boosters</th><td>solid</td><td>Thrust at liftoff: the core alone has a thrust-to-weight ratio of 0.53</td></tr>
<tr><th scope="row">Geostationary satellite, apogee engine</th><td>storable, hypergolic bipropellant</td><td>Storability for years and restarts, as in the worked example</td></tr>
</table>

:::

In general, first stages prioritize high thrust and high density, upper stages prioritize high specific impulse, and spacecraft that remain in orbit for years prioritize storability, as we saw in the worked example.

## Summary

:::{important} Summary
- Rocket propulsion comes in cold gas, monopropellant, bipropellant, solid, hybrid, nuclear thermal, and electric kinds. Specific impulse and thrust run in opposite directions, with electric thrusters reaching thousands of seconds at millinewtons while only chemical rockets can lift a vehicle off the ground today.
- Launch vehicles are classed by payload to low Earth orbit: small up to 2 t, medium to 20 t, heavy to 50 t, and super heavy above. They are also described by stages and boosters, by propellants, and as expendable or reusable. Their payload is 0.55% to 4.5% of the liftoff mass.
- A propellant is judged on specific impulse, density, storability, and what it lets the engine do. Hydrogen gives the highest specific impulse and the largest tanks; storable propellants can be stored for years; solid motors give high thrust and cannot stop.
- Launch vehicles lift off at a thrust-to-weight ratio of 1.19 to 1.46; stages in orbit work at a few tenths. To justify a choice, size each option, compare mass and volume with numbers, and state the mass and volume trade-off.
:::

:::{table} The equations of this page.
:label: tbl-p44-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Volume of a propellant (script V, not velocity) | $\mathcal{V} = m/\rho$ |
| Bulk density of a pair at mixture ratio O/F | $\rho_\text{bulk} = (1 + \text{O/F})\big/\left(\text{O/F}/\rho_\text{ox} + 1/\rho_\text{fuel}\right)$ |
| Oxidizer and fuel in a mass $m_\text{prop}$ | $m_\text{ox} = m_\text{prop}\,\text{O/F}/(1 + \text{O/F})$, $m_\text{fuel} = m_\text{prop}/(1 + \text{O/F})$ |
| Thrust-to-weight ratio ($g_0$ = 9.81 m/s² everywhere) | $F/W = F/(m g_0)$ |
| Specific impulse (from page 4.1) | $I_\text{sp} = F/(\dot m g_0) = c/g_0$ |

:::

:::{exercise} For discussion
:label: ex-p44-discussion

1. Why does a launch vehicle's first stage rarely burn hydrogen, while its upper stages often do?
2. A probe will coast for seven years before its last burn. Which kinds of propulsion in {numref}`tbl-p44-kinds` can you rule out, and why?
3. The Space Shuttle and the SLS lift off with solid boosters beside a hydrogen core. What does each part bring?
4. In the worked example, how light would the bipropellant system have to be to match the solid motor's initial mass? What else, besides mass, would you weigh?
5. Electric thrusters reach thousands of seconds of specific impulse, far more than any chemical engine. Why do launch vehicles not use them?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-4-4.html
:label: quiz-4-4
:enumerated: false
:width: 100%

Quiz for Standard 4.4: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Arianespace, *Vega User's Manual*, Issue 4, 2014. Page 1-6 (stage data) and Section 2.3 (restarts of the AVUM stage).
- Arianespace, *Vega C User's Manual*, Issue 0 Revision 0, 2018. Table 2.4.2.a.
- Arianespace, *Ariane 5 User's Manual*, Issue 5 Revision 2, 2016. Page 1-7 (stage data), Sections 2.4.1 (the standard transfer orbit) and 2.4.5.
- Bilstein, R. E., *Stages to Saturn: A Technological History of the Apollo/Saturn Launch Vehicles*, NASA SP-4206, 1996. Page 5.
- European Space Agency (ESA), "[Ariane 5 ES](https://www.esa.int/Enabling_Support/Space_Transportation/Launch_vehicles/Ariane_5_ES)," n.d.a.
- European Space Agency (ESA), "[Shuttle technical facts](https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Space_Shuttle/Shuttle_technical_facts)," n.d.b.
- European Space Agency (ESA), "[Vega-C](https://www.esa.int/Enabling_Support/Space_Transportation/Vega/Vega-C)," n.d.c.
- European Space Agency (ESA), "[Ariane 5 boosters (EAP)](https://www.esa.int/Enabling_Support/Space_Transportation/Launch_vehicles/Boosters_EAP)," n.d.d.
- Huzel, D. K., and Huang, D. H., *Design of Liquid Propellant Rocket Engines*, NASA SP-125, 1967. Pages 19 to 21; Tables 1-4 and 1-5 (pp. 22 to 24), 1-6 (p. 25), and 1-8 to 1-10 (pp. 26 and 27).
- Indian Space Research Organisation (ISRO), "[PSLV](https://www.isro.gov.in/PSLV_CON.html)," n.d.a.
- Indian Space Research Organisation (ISRO), "[LVM3](https://www.isro.gov.in/GSLVmk3_CON.html)," n.d.b.
- McConnaughey, P. K., Femminineo, M. G., Koelfgen, S. J., Lepsch, R. A., Ryan, R. M., and Taylor, S. A., *NASA's Launch Propulsion Systems Technology Roadmap*, NASA Technical Reports Server 20120014957, 2012. Section 1, p. 2.
- Meyer, M., Johnson, L., Palaszewski, B., Coote, D., Goebel, D., and White, H., *In-Space Propulsion Systems Roadmap, Technology Area 02*, NASA Technical Reports Server 20110005503, 2010. Page 9.
- Meyer, M., Johnson, L., Palaszewski, B., Coote, D., Goebel, D., and White, H., *Roadmap for In-Space Propulsion Technology*, NASA/TM-2012-217641, 2012. Pages 3 and 4.
- NASA, "F-1 Engine Fact Sheet," *Saturn V News Reference*, sheet R-1, 1968.
- NASA, *Technical Information Summary, Apollo-10 (AS-505)*, Marshall Space Flight Center, 1969. Figure 18.
- NASA, *Solid Propellant Selection and Characterization*, NASA SP-8064, 1971. Table I.
- NASA, *Space Shuttle News Reference*, 1981. Pages 2-4 and 2-18.
- NASA, *Space Launch System Reference Guide*, Version 2, 2022. Page 8.
- NASA, "[State-of-the-Art of Small Spacecraft Technology, Chapter 4: In-Space Propulsion](https://www.nasa.gov/smallsat-institute/sst-soa/in-space_propulsion/)," Small Spacecraft Systems Virtual Institute, 2026. Table 4-1.
- National Institute of Standards and Technology (NIST), "[NIST Chemistry WebBook, SRD 69](https://webbook.nist.gov/chemistry/fluid/)," thermophysical properties of fluid systems: oxygen, parahydrogen, and methane at 0.101325 MPa, 2023.
- Rocket Lab, *Payload User's Guide*, Version 7.0, 2022. Page 12.
- SpaceX, "Falcon 9" and "Falcon Heavy," spacex.com, as archived in 2019 (2019a, 2019b).
- SpaceX, *[Falcon User's Guide](https://www.spacex.com/assets/media/falcon-users-guide-2025-05-09.pdf)*, 2025. Section 2.
