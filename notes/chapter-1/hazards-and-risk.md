---
title: "1.2 Hazards and Risk"
short_title: 1.2 Hazards and Risk
---

:::{include} ../_parts/standards/1.2.md
:::

Aerospace vehicles operate in demanding environments. An airliner flies through ice, birds, and severe weather, while a satellite faces radiation, orbital debris, and vacuum. In this lecture we define what a {term}`hazard` is and survey atmospheric hazards by flight phase and space hazards by altitude. We then turn those hazards into {term}`risks <risk>`, score each risk on a {term}`risk matrix`, and apply a {term}`mitigation` to reduce it, working through an example for a small {term}`launch vehicle`. Finally, we examine how to locate critical parts whose failure alone would end a mission.

:::{note} What to take from this page
- A hazard is a condition of the operating environment that can harm the vehicle or the mission. Describe each one by its cause, its effect, and a mitigation that acts on one link of that chain.
- Atmospheric hazards depend on flight phase and altitude band; space hazards depend on altitude band, from drag and atomic oxygen in low orbit to the radiation belts above.
- A risk is a sentence, "If [event], then [consequence]," with a likelihood and a consequence from 1 to 5. In these notes the level is High when likelihood times consequence is 15 or more, Medium from 5 to 12, and Low at 4 or less.
- Most mitigations lower the likelihood; some lower the consequence. We identify a {term}`single-point failure` by stepping through the mission timeline. Adding {term}`redundancy` removes it, added margin and testing lower its likelihood without eliminating the single point, or the project accepts it with a documented reason.
:::

(p12-what-is-a-hazard)=
## What a hazard is

We start with something familiar. A slippery road is a hazard for anyone driving in winter. Water, snow, or oil on the road causes it. Its effect is that the car slides and may crash. You can salt the road, drive slower, or fit snow tires. Every hazard on this page follows the same chain of cause, hazard, and effect, with a mitigation that acts on one of its links.

:::{prf:definition} Hazard
:label: def-p12-hazard

A **hazard** is a condition of the operating environment that can harm the vehicle or its mission. NASA's safety glossary words it more generally: "a state or a set of conditions, internal or external to a system, that has the potential to cause harm" (NASA 2018).
:::

We describe a hazard as a chain of three links and an action:

1. **Cause**: what creates the condition (water on the road; supercooled water drops, still liquid below 0 °C, in a cloud).
2. **Hazard**: the condition itself (a slippery road; ice on a wing).
3. **Effect**: what the condition does to the vehicle or the mission (the car slides; the wing makes less lift and more drag).
4. **Mitigation**: an action that reduces the harm.

:::{prf:definition} Mitigation
:label: def-p12-mitigation

A **mitigation** is an action, taken or planned, that makes harm from a hazard less likely or less severe. It acts on one link of the chain by keeping the vehicle away from the cause, removing the hazard, or softening the effect.
:::

{numref}`fig-p12-hazard-anatomy` draws the chain for the icy road and for an aircraft wing in an icing cloud. The wing shows why it matters where a mitigation acts. Nobody can remove the supercooled drops from a cloud. The pilot either avoids the cloud, which acts on the cause, or heats the wing so that ice cannot form, which removes the hazard.

:::{figure} figures/p12-hazard-anatomy.svg
:label: fig-p12-hazard-anatomy
:alt: Two rows of three boxes joined by arrows, under the column heads cause, hazard, and effect. Row (a), icy road: water, snow, or oil on the road leads to a slippery road, which leads to a car that slides and may crash; dashed mitigation boxes below act on the hazard (salt or sand the road) and on the effect (drive slower, fit snow tires). Row (b), wing icing: supercooled drops in a cloud lead to ice on the wing, which leads to less lift, more drag, and an early stall; mitigations act on the cause (fly around or out of the cloud) and on the hazard (heat the wing).
:width: 65%

Schematic of the hazard chain for an icy road and for a wing in an icing cloud. Each mitigation acts on one link: the cause, the hazard, or the effect. Arrows: "leads to." Dashed lines ending in a bar: the box the mitigation acts on.
:::

### Hazard or project risk

A hazard comes from the environment the vehicle operates in. A project also faces risks that have nothing to do with that environment. An engine is delivered late, or the mass grows during design. We manage both kinds with the same tools.

:::{prf:definition} Risk
:label: def-p12-risk

A **risk** is an uncertain future event that would hurt the mission or the project, together with how likely it is (its **likelihood**) and how bad it would be (its **consequence**) (NASA 2016, Section 6.4).
:::

{numref}`tbl-p12-hazard-or-risk` sets a hazard and a {term}`project risk` side by side. A hazard becomes a risk when you score it for one particular mission, assessing how likely it is to affect this vehicle and how severely.

:::{table} Hazards and project risks.
:label: tbl-p12-hazard-or-risk
:align: center

<table>
<tr><th>Question</th><th>Hazard</th><th>Project risk</th></tr>
<tr><th scope="row">Where it comes from</th><td>The operating environment: air, weather, space</td><td>The work of building the vehicle: design, suppliers, tests, money, time</td></tr>
<tr><th scope="row">Examples</th><td>Icing, bird strike, atomic oxygen, radiation, debris</td><td>A late engine, mass growth, a battery not ready in time</td></tr>
<tr><th scope="row">What it hurts</th><td>The vehicle in operation, or the mission</td><td>Performance, cost, or schedule</td></tr>
<tr><th scope="row">How it is ranked</th><td>Turned into a risk for one mission, then scored</td><td>Scored directly</td></tr>
</table>
:::

:::{warning} A hazard must match the operating environment
List only hazards the vehicle can encounter during its mission. Icing requires liquid water in air, so it is not a hazard for a satellite in orbit. Atomic oxygen erodes surfaces only in low orbit, so it does not affect an airliner. Before scoring a hazard, state where and when the vehicle faces it.
:::

## Hazards in the atmosphere

In the atmosphere, the hazards change with the phase of flight. Most of them occur at airports and in the low airspace around them, including debris on the runway, birds, wind near the ground, and weather at the arrival airport. {numref}`fig-p12-flight-hazards` places nine hazards along the flight of a jet transport. {numref}`tbl-p12-flight-hazards` gives the cause, the effect, and one mitigation of each, under the same numbers.

:::{figure} figures/p12-flight-hazards.svg
:label: fig-p12-flight-hazards
:alt: A flight path climbs from a runway to a cruise altitude of 11 kilometers, cruises, and descends to a second runway beside a thunderstorm cloud with a flat base at 1.6 kilometers, a tower of rounded bulges, and a flat anvil top near 12 kilometers. A shaded band near the ground, edged by dashed lines, marks where most bird strikes happen, and a second band from about 2.3 to 5.4 kilometers marks the icing band of a standard day. Nine numbered circles mark the hazards, named in a key under the plot: 1 hot and high airport and 2 runway debris on the departure runway; 3 bird strike and 4 icing on the climb; 5 clear-air turbulence and 6 volcanic ash at cruise; 7 thunderstorm and lightning in the cloud; 8 wind shear and microburst on the final approach beside the storm; 9 low visibility on the arrival runway.
:width: 90%

Schematic, distance not to scale, altitude to scale. Most hazards occur at airports and during climb or descent; only two, clear-air turbulence and volcanic ash, are marked at cruise. Airports drawn at sea level; icing band computed for a standard day; bird band after FAA (n.d., AIM 7-5-1).
:::

:::{table} The hazards of {numref}`fig-p12-flight-hazards`: cause, effect, and one mitigation. Sources: FAA (n.d., Chapter 7), FAA (2023, Chapters 11 and 12), FAA (2015), FAA (2016), and FAA (2010).
:label: tbl-p12-flight-hazards
:align: center

| No. | Hazard | Cause | Effect | One mitigation |
| ---: | --- | --- | --- | --- |
| 1 | Hot and high airport | High elevation and high temperature make the air thin | Wings and engines work in thin air: longer takeoff run, weaker climb | Take off with less weight, or at a cooler time of day |
| 2 | Runway debris | Objects left on the runway: parts, tools, stones | Cut tires; damaged engines and structure | Inspect and sweep the runway |
| 3 | Bird strike | Birds near airports, mostly below 3,000 ft | Engine damage or failure, broken windshield | Wildlife control at airports; avoid low flight during migration |
| 4 | Icing | Liquid cloud drops below 0 °C that freeze when they touch the airframe | Less lift, more drag, and a wing that {term}`stalls <stall>` (suddenly loses lift) at a smaller angle to the air | Heat the wing and the engine inlets; climb or descend out of the cloud |
| 5 | Clear-air turbulence | Layers of air moving at different speeds beside a jet stream (a narrow band of strong wind high in the troposphere), with no cloud to mark them | The aircraft is thrown up and down without warning; anyone not strapped in can be hurt | Choose the route and altitude from turbulence forecasts and from reports by aircraft ahead; keep passengers belted |
| 6 | Volcanic ash | An eruption lifts fine rock and glass dust to cruise altitudes | Ash melts inside the engines and can stop them (two Boeing 747s lost all four; FAA n.d., AIM 7-6-10); it scours the windshield | Stay clear of reported ash; inside it, pull the thrust to idle and reverse course |
| 7 | Thunderstorm and lightning | Strong rising air in tall storm clouds | Severe turbulence, hail, lightning damage to electronics | Fly around storms, with weather radar |
| 8 | Wind shear and microburst | A downdraft that spreads out near the ground ({numref}`fig-p12-microburst`) | A headwind turns into a tailwind: airspeed and lift fall while the aircraft is low and slow | Warning systems at the airport and on board; wait for the storm to pass, or abandon the approach and climb away |
| 9 | Low visibility | Fog, low cloud, heavy rain, or snow | The pilot cannot see the runway | Approaches flown on instruments, down to a set minimum height; divert to another airport |

:::

Four of these hazards come with numbers we should remember:

- **Icing.** Ice builds fastest a little below 0 °C. Below about −20 °C most clouds are ice crystals, which bounce off (FAA 2015). On a standard day (the reference atmosphere of [1.4 Standard Atmosphere](standard-atmosphere.md)) the air is at 0 °C at 2,309 m and at −20 °C at 5,386 m. Cloud between those heights is the icing band. On a warmer day the band moves up.
- **Wind shear and microbursts.** {term}`Wind shear` is a sudden change of wind speed or direction over a short distance. A {term}`microburst` is a small, intense downdraft that spreads out in all directions at the ground (FAA n.d., AIM 7-1-24). Its downdraft can reach 6,000 ft/min and its outflow 45 knots (a {term}`knot` is one nautical mile per hour, 0.514 m/s). An aircraft crossing it on approach flies first into a 45-knot headwind, then through the downdraft, and then into a 45-knot tailwind ({numref}`fig-p12-microburst`). That is a change of 90 knots within a few hundred feet of the ground, where the aircraft is slow and low.
- **Clear-air turbulence.** The jet streams lie between about 6.1 and 13.7 km (20,000 to 45,000 ft) (FAA 2016).
- **Birds.** Over 90% of reported bird strikes occur at or below 3,000 ft (914 m) above the ground, in the climb and the approach (FAA n.d., AIM 7-5-1).

:::{figure} figures/p12-microburst.svg
:label: fig-p12-microburst
:alt: Side view of a microburst on the approach to a runway at the right. Under a storm cloud a downdraft, labeled up to 6,000 feet per minute, comes down and spreads along the ground into a layer of outflow, drawn as a tinted region with a dashed edge and open arrows: on the left, pointing toward the approaching aircraft, outflow labeled headwind for the aircraft, up to 45 knots; on the right, pointing away from it, outflow labeled tailwind, up to 45 knots. The path flown, a heavy line moving right, rises above the dashed planned approach at point 1 in the headwind, passes under the downdraft at point 2, and sinks below the planned approach at point 3 in the tailwind, ending low and short of the runway. A key names the points: 1 headwind, airspeed rises; 2 downdraft, the aircraft is pushed down; 3 tailwind, airspeed falls by up to 90 knots from its value at 1.
:width: 90%

Schematic, not to scale. The same outflow is a headwind on one side of the downdraft and a tailwind on the other. Open block arrows: the moving air, inside the tinted region; heavy line: the path flown; dashed line: the planned approach. Wind speeds from FAA (n.d., AIM 7-1-24).
:::

(p12-hot-and-high)=
### Hot and high airports

Thin air is a hazard too. A wing and an engine both work by moving air. The less air there is in each cubic meter, the less lift and thrust they make at a given speed. Density falls with altitude and with temperature, so the worst case is a high airport on a hot afternoon. Pilots describe this with the {term}`density altitude`, the altitude in the {term}`standard atmosphere` where the density equals the density the aircraft experiences (FAA 2023, Chapter 11).

For example, take an airport 1,600 m above sea level on an afternoon at 35 °C. The air there has a density of 0.9622 kg/m³. On a standard day it would be 1.047 kg/m³ at that airport, compared with 1.2250 kg/m³ at sea level. At this airport, air density is 21% lower than at sea level (14% lower from elevation alone). The density altitude is 2,444 m, meaning the aircraft performs as it would at 2,444 m on a standard day. Takeoff runs lengthen and climb rates drop, so on a hot enough day the aircraft must leave payload or fuel behind.

To find the density, we shift the whole standard temperature profile until it reads 35 °C at the airport, then start from the standard sea-level pressure and apply the layer equations ([a non-standard day](#p14-nonstandard) shows the calculation). If you combine the standard pressure at 1,600 m with 35 °C instead, the density comes out a little low. Because warmer air is less dense, each meter of climb leaves behind less air weight, so pressure drops more slowly with height and stays slightly higher at 1,600 m (a direct consequence of the hydrostatic balance derived on [1.4 Standard Atmosphere](standard-atmosphere.md)).

:::{warning} Sea level standard is not the design case
Performance worked out at sea level on a standard day makes the aircraft look better than it is. Check takeoff and climb at the highest airport the aircraft will use, on its hottest day, with the temperature in kelvin.
:::

(p12-space-hazards)=
## Hazards in space

Above the atmosphere, we group the hazards mostly by altitude. {numref}`fig-p12-space-altitudes` shows where each one matters. {term}`Low Earth orbits <Low Earth orbit>` still have a trace of atmosphere, which brings drag and atomic oxygen, and most of the debris is below 2,000 km. The radiation belts lie higher up. The {term}`geostationary orbit`, 35,786 km up, runs through the outer belt.

:::{figure} figures/p12-space-altitudes.svg
:label: fig-p12-space-altitudes
:alt: Bar chart on a logarithmic altitude axis from 100 to 100,000 kilometers. Drag spans 100 to 600 kilometers, atomic oxygen 180 to 650 kilometers, most debris 100 to 2,000 kilometers with a small extra bar labeled debris in the geostationary ring, the inner radiation belt about 1,600 to 12,900 kilometers with a dashed extension down to about 500 kilometers labeled South Atlantic Anomaly, and the outer belt about 19,300 to 40,200 kilometers. Dashed lines mark Hubble's orbit at 500 kilometers and the geostationary orbit at 35,786 kilometers, which lies inside the outer belt.
:width: 80%

Plotted from published values: the altitudes where each space hazard matters. Low orbits experience drag, atomic oxygen, and most of the debris; the radiation belts lie higher, except where the inner belt dips over the South Atlantic. Belt edges from NASA (2013), atomic oxygen from Banks et al. (2004), debris and drag from NASA Orbital Debris Program Office (n.d.); the belt edges move with solar activity.
:::

We take the space hazards one at a time. {numref}`tbl-p12-space-hazards`, after the solar cycle, sums them up.

- **Vacuum.** In vacuum, materials release trapped gases and vapors. This outgassing can condense on cold lenses and sensors. Without air and ordinary lubricants, clean metal surfaces in contact can also wear fast and stick together. We call this cold welding (ESA 2015).
- **Thermal extremes.** A spacecraft gains heat from the Sun, from sunlight reflected by Earth, and from Earth's infrared glow, and loses it only by radiating to space (NASA Small Spacecraft Systems Virtual Institute 2021, Chapter 7). Its surfaces heat in sunlight and cool fast in Earth's shadow.
- **Drag.** Below about 600 km enough air remains to bring a satellite down within years (NASA Orbital Debris Program Office n.d.). The section on [orbit lifetime](#p25-orbit-lifetime) works out how fast, and how the {term}`ballistic coefficient` sets the rate.
- **Atomic oxygen.** Ultraviolet sunlight splits oxygen molecules into single atoms. Between 180 and 650 km, {term}`atomic oxygen` is the most common gas. A spacecraft at orbital speed hits these atoms hard enough to oxidize and wear away polymers, such as Kapton film, and carbon composites on its forward-facing surfaces (Banks et al. 2004).
- **Debris and micrometeoroids.** Old satellites, spent stages, and fragments share the orbits with working spacecraft, mostly below 2,000 km. Pieces larger than about 10 cm are tracked; smaller ones are not. In low orbit, debris strikes at about 10 km/s on average and up to 15 km/s. At that speed a millimeter-sized fragment can puncture a wall (NASA Orbital Debris Program Office n.d.). Natural micrometeoroids add to the hazard. The International Space Station normally maneuvers out of the way when the chance of a hit by a tracked object exceeds 1 in 10,000 (NASA Orbital Debris Program Office n.d.).
- **Radiation.** Three sources of fast charged particles reach a spacecraft: the particles trapped in Earth's radiation belts, the protons the Sun throws out in solar particle events, and galactic cosmic rays from outside the solar system.
- **Solar radiation pressure.** Sunlight exerts a tiny, steady force on every illuminated surface, measured per square meter as {term}`solar radiation pressure`. Unlike atmospheric drag, this force does not fade with altitude. Above about 1,000 km, when the center of solar pressure is offset from the spacecraft's center of mass, solar radiation pressure produces a larger disturbance torque than drag does (NASA 1969, Sections 1 and 2.1).

### Radiation and its effects

Of these hazards, we need to look more closely at radiation. Earth's magnetic field traps charged particles in two rings around the planet, the Van Allen radiation belts ({numref}`fig-p12-radiation-belts`). Above the equator the inner belt extends from about 1,600 to 12,900 km and the outer belt from about 19,300 to 40,200 km (NASA 2013). The particles spiral along the field lines and bounce between the hemispheres. As a result, each belt follows the field lines and comes closer to Earth at higher latitudes.

The same magnetic field shields low orbits near the equator from most solar particles and cosmic rays (NASA 2020). Orbits that pass over the poles, high orbits, and flights away from Earth get little of this protection.

:::{figure} figures/p12-radiation-belts.svg
:label: fig-p12-radiation-belts
:alt: Cross-section of Earth and its magnetic field seen from the side, with the magnetic axis vertical. On each side of Earth, a darker crescent close to Earth is the inner belt and a larger, lighter crescent farther out is the outer belt, with a white gap between them, labeled gap on the left; both belts curve toward Earth at higher latitudes, following the field lines. On the right a thin gray line, labeled magnetic field line, runs through the gap from Earth's surface out and back. The geostationary orbit, seen edge-on, is marked by a small circle inside the outer belt on each side, at about 6.6 Earth radii from the center. A scale bar shows one Earth radius, 6,378 kilometers.
:width: 85%

Schematic, to scale, in the plane of the magnetic axis. The two belts are rings around the magnetic equator. They follow the field lines, so they come closer to Earth at high latitudes, and the geostationary orbit runs through the outer belt. The thin line in the gap is one magnetic field line. Belt edges after NASA (2013).
:::

What the radiation does to a spacecraft falls into two groups:

- **Total dose.** Every particle that passes through a material leaves a little damage. In electronics it adds up over the years until a part stops working, a cumulative effect called the {term}`total ionizing dose`. A longer mission, or an orbit inside a belt, collects more.
- **Single-event effects.** One energetic particle can disturb a chip on its own, at any moment. These {term}`single-event effects <single-event effect>` are of three kinds (O'Bryan et al. 2017):
  - an upset, a flipped memory bit (a single-event upset), which a reset or a rewrite clears;
  - a latchup, in which the part draws a large current until it is switched off and on;
  - a burnout, which destroys the part.

The structure and added material shield the electronics from the less energetic particles, which cuts the dose and the upset rate (NASA Small Spacecraft Systems Virtual Institute 2021, Chapter 6). The most energetic particles pass through anyway. So designers also use parts tested for radiation and software that checks memory and restarts a unit that stops responding.

:::{prf:definition} South Atlantic Anomaly
:label: def-p12-saa

The **{term}`South Atlantic Anomaly`** is a region over South America and the southern Atlantic Ocean where Earth's magnetic field is weaker than elsewhere. There the inner radiation belt reaches down to the altitudes of low orbits (NASA 2020).
:::

For example, the Hubble Space Telescope orbits at about 500 km and crosses the anomaly on seven to nine orbits in a row each day. For 20 to 25 minutes on each pass most observing stops, because particles hitting the detectors swamp the signal (STScI n.d.).

**Spacecraft charging** is the last effect of charged particles. They build up electric charge on the surfaces of a spacecraft and inside its insulators, until a spark discharges it and damages coatings, solar cells, or electronics. Charging is worst around the geostationary orbit and in the outer belt. The main mitigation is to connect every conducting part to a common ground, so that no part collects charge on its own (NASA 2022).

### The solar cycle

The Sun drives several of these hazards. Its activity rises and falls in the {term}`solar cycle` of about 11 years. A common measure of that activity is F10.7, the strength of the Sun's radio emission at a wavelength of 10.7 cm, in solar flux units (sfu) (NOAA n.d.a). {numref}`fig-p12-solar-cycle` plots the measured record since 1947.

:::{figure} figures/p12-solar-cycle.svg
:label: fig-p12-solar-cycle
:alt: Plot of the solar radio flux F10.7, in solar flux units, from 1947 to the present. The thin gray monthly means and the heavy 13-month running mean rise and fall in regular cycles between about 68 and 245 units. Circles mark the maxima of the running mean; a dimension line from the 1958 maximum to the most recent one reads 6 cycles in 66.6 years, 11.1 years each.
:width: 80%

Computed from measured data: monthly means and their 13-month running mean of the daily Penticton F10.7 series, adjusted to the mean distance of Earth from the Sun. Solar activity rises and falls in cycles of about 11 years, and no two maxima are alike. Data of NRC Canada, distributed by LASP (n.d.).
:::

From the data, the running mean falls to about 68 sfu at a minimum and reaches between 146 and 245 sfu at a maximum. Its maxima are 8.1 to 12.7 years apart, 11.1 years on average. The cycle changes several hazards:

- When the Sun is active, it puts extra energy into the upper atmosphere, and denser air rises to the altitudes of low orbits. Drag rises and satellites come down sooner (NOAA n.d.b). The denser air also carries more atomic oxygen.
- The energetic electrons at the geostationary orbit, which charge spacecraft, vary by up to 100 to 1 over the cycle (NASA 2022).

So a mission plan states where in the cycle the mission flies, and we design the vehicle for the worst part of the cycle it will experience.

:::{table} Hazards in space: where they matter, their effect, and mitigations.
:label: tbl-p12-space-hazards
:align: center

| Hazard | Where it matters | Effect | Mitigations |
| --- | --- | --- | --- |
| Vacuum | Everywhere | Outgassing fogs optics; cold welding of moving parts | Low-outgassing materials; vacuum lubricants |
| Thermal extremes | Everywhere; sun and shadow | Parts too hot or too cold | Coatings, insulation, radiators, heaters |
| Drag | Low orbit, below about 600 km | Orbit decays; reentry | Higher orbit; propellant to raise the orbit |
| Atomic oxygen | About 180 to 650 km | Polymers and composites worn away | Protective coatings; resistant materials |
| Debris and micrometeoroids | Mostly below 2,000 km; the geostationary ring | Puncture, loss of parts, breakup | Shielding; avoidance maneuvers; disposal at end of mission |
| Trapped radiation | The belts; the South Atlantic Anomaly | Total dose; single-event effects | Shielding; tested parts; recovery software |
| Solar particles, cosmic rays | Everywhere; least in low orbits near the equator, where Earth's magnetic field turns most of them away | Single-event effects; dose | Tested parts; recovery software; operations during solar storms |
| Charging | Geostationary orbit and the outer belt | Discharges that damage surfaces and electronics | Ground every conducting part |
| Solar radiation pressure | Everywhere in sunlight; above about 1,000 km it outweighs drag | A small, steady push that turns the spacecraft | Shapes and coatings that keep the push balanced; attitude control corrects the rest |

:::

(p12-risk-matrix)=
## The risk matrix

A list of hazards does not tell us which one to work on first. For that, we write each hazard (and each project risk) as a risk and give it two scores.

**The risk statement.** Write each risk as one sentence of the form "If [event], then [consequence]." For example: "If the second-stage engine fails its qualification test, then the first launch slips by six months." (A qualification test is the test that proves a design before it flies.) The event must be something that may or may not happen, and the consequence must say what the mission or the project loses (NASA 2011, Section 4.2.1.1).

**The two scores.** The {term}`likelihood` L rates how likely the event is. The {term}`consequence` C rates how severe the result would be. We score each from 1 to 5 with the scales of {numref}`tbl-p12-scales`, and we back each score with one sentence that explains why.

:::{table} The likelihood and consequence scales of these notes.
:label: tbl-p12-scales
:align: center

| Score | Likelihood, L | Consequence, C |
| ---: | --- | --- |
| 1 | Very unlikely | Minimal: no effect on the mission |
| 2 | Unlikely | Minor: small loss of performance or a short delay |
| 3 | Possible | Moderate: part of the mission lost, or a long delay |
| 4 | Likely | Major: most of the mission lost |
| 5 | Very likely | The mission or the program lost |

:::

**The score and the level.** Multiply the two scores:

:::{math}
:label: eq-p12-score
S = L \times C
:::

The score $S$ runs from 1 to 25. In these notes we sort it into three levels: **High** when $S$ is 15 or more, **Medium** from 5 to 12, and **Low** at 4 or less. (No product of two whole numbers from 1 to 5 falls between 12 and 15.) Individual aerospace programs set their own thresholds; for example, many human-spaceflight programs flag any catastrophic $C = 5$ risk as High even when its likelihood is low.

:::{figure} figures/p12-risk-matrix.svg
:label: fig-p12-risk-matrix
:alt: A five by five grid. Rows are likelihood 1 to 5 from bottom to top and columns are consequence 1 to 5 from left to right; each cell shows the product of the two. Cells with products 15 to 25 (the six cells at the top right) are dark gray with a light hatch, their numbers on white tabs, and are High; cells from 5 to 12 are light gray and Medium; cells from 1 to 4 (the eight cells at the bottom left) are white and Low. Heavy stair-step lines separate the three levels. A dashed frame marks the cell at likelihood 4 and consequence 3, whose product is 12, Medium. A key beside the grid names the levels with their ranges.
:width: 90%

Schematic of the risk matrix of these notes. A risk is placed in the row of its likelihood and the column of its consequence; the product of the two sets its level. Heavy lines mark the boundaries between the levels: 6 cells are High, 11 Medium, and 8 Low.
:::

The {term}`risk matrix` of {numref}`fig-p12-risk-matrix` is the picture of this rule. Each risk goes in the cell of its two scores, and we work first on the High risks, at the top right.

:::{tip} Method: ranking a hazard on the risk matrix
1. State where and when the vehicle encounters the hazard, and verify that it occurs in that environment.
2. Write the risk statement: "If [event], then [consequence]."
3. Score the likelihood L from 1 to 5, with one sentence of reason.
4. Score the consequence C from 1 to 5, with one sentence of reason.
5. Compute $S = L \times C$ and read the level: High at 15 or more, Medium from 5 to 12, Low at 4 or less.
6. Place the risk on the matrix, then work on the High risks first.
:::

:::{warning} Read the axes before you place a risk
Some documents put likelihood on the horizontal axis and consequence on the vertical one. The product, and so the level, does not change. But if you place a risk by habit, it lands in the wrong cell. Read both axis titles first, every time. On such a matrix a lower likelihood moves a risk left, not down. Say first which score the mitigation changes; the direction then follows from the axes in front of you.
:::

Keep in mind that a risk matrix is only a starting summary. Because it displays each risk separately and hides the uncertainty in each score (NASA 2011, Section 4.3.2.6), use it to prioritize your engineering effort and always support every score with a written justification.

## Mitigation moves a risk

Once a risk is on the matrix, we want to move it toward Low. A mitigation does this by lowering one of the two scores, or both.

- **Most mitigations lower the likelihood.** Testing a part early, holding a larger mass margin (weight held in reserve for growth), qualifying a second supplier, or avoiding a cloud make the event less likely. The likelihood score falls, for example from 4 to 2. On the matrix of these notes the risk moves **down**.
- **Some lower the consequence.** When the event cannot be made less likely, as with weather, the mitigation limits the impact when it occurs, such as a spare day in the {term}`launch window`, a backup unit, or a safe mode (a minimal state the spacecraft drops into after a fault). The consequence score falls, and on the matrix of these notes the risk moves **left**.

The rule limits how far a risk can move. Suppose its consequence is 5, the loss of the mission. Lowering its likelihood cannot make it Low, because $1 \times 5 = 5$ is still Medium. Such a risk stays on the list and is tracked, or we reduce its consequence by design. When a risk remains after mitigation, we accept it with its reason written down and keep watching it in case its scores change.

(p12-worked-example)=
## Worked example: risks for a small launch vehicle

An invented two-stage small launch vehicle is preparing for its first flight. Its engineers have listed five risks, consisting of three project risks and two that come from hazards of the atmosphere. Rank them, choose a mitigation for each, and rank them again. {numref}`tbl-p12-example` collects the result.

:::{table} Risks of the small launch vehicle before and after mitigation (L likelihood, C consequence, S = L × C). R5 after NASA (2023).
:label: tbl-p12-example
:align: center

| Risk | Risk statement | Before: L, C, S | Mitigation | After: L, C, S |
| --- | --- | --- | --- | --- |
| R1 | If the second-stage engine fails its qualification test, then the first launch slips by six months. | 4, 3, 12 Medium | Test the engine's components early, before the full qualification test. | 2, 3, 6 Medium |
| R2 | If the structural mass grows beyond the margin held for it, then the payload to orbit falls below the requirement. | 3, 4, 12 Medium | Raise the mass margin to 15% and review the mass report every month. | 2, 4, 8 Medium |
| R3 | If winds high above the launch site exceed their limits on launch day, then the launch is called off for the day (scrubbed). | 4, 2, 8 Medium | Plan a launch window of several days and forecast the winds with weather balloons. | 4, 1, 4 Low |
| R4 | If the supplier of the avionics (the flight electronics) delivers late, then integration and test slip. | 3, 3, 9 Medium | Qualify a second supplier for the flight computer. | 2, 2, 4 Low |
| R5 | If the vehicle climbs through an electrified cloud, then it triggers lightning that upsets its flight computer and the vehicle is lost. | 2, 5, 10 Medium | Adopt lightning launch commit criteria: do not launch through or near the cloud types they list. | 1, 5, 5 Medium |

:::

1. **Statements and scores before mitigation.** The first four rows are risks typical of a first flight, with three from the work of building the vehicle and one from the weather. Each score has its reason, read against {numref}`tbl-p12-scales`:
   - R1: the engine is new and has never run for a full burn, so a failed test is likely (L = 4); a slip of six months is a long delay (C = 3).
   - R2: mass grows on most new vehicles, so growth beyond the margin is possible (L = 3); a payload below the requirement loses most of the mission (C = 4).
   - R3: strong winds aloft are common at the launch site in this season, so a scrub is likely (L = 4); a scrub causes a one-day slip, which is a short delay (C = 2).
   - R4: the only supplier also builds for other customers, so a late delivery is possible (L = 3); a slip in integration and test is a long delay (C = 3).
   - R5 comes from a hazard of the launch environment. A launch vehicle climbing through an electrified cloud can trigger lightning. Apollo 12 triggered two strikes, at 36.5 s and 52 s after liftoff in 1969, and recovered. Atlas/Centaur-67 triggered a strike in 1987 and was destroyed (NASA 2000; NASA 2023). With launch rules in place a strike is unlikely (L = 2). The consequence is the loss of the vehicle (C = 5).
2. **Scores.** With $S = L \times C$, R1 scores $4 \times 3 = 12$, Medium. The table gives the other four. No risk is High, so we work first on the two risks scored 12.
3. **Mitigations and new scores.** Each mitigation in the table lowers one score, or both. Early component tests (R1), a larger margin (R2), and the launch rules (R5) make the event less likely, so L falls. Nobody can make the wind less likely (R3), but with a multi-day launch window a scrub has minimal mission impact, so C falls from 2 to 1. Qualifying a second supplier (R4) makes a late delivery both less likely and less disruptive to the schedule, so both scores fall. After mitigation the scores are 6, 8, 4, 4, and 5.
4. **Moves.** {numref}`fig-p12-risk-moves` draws the moves.

:::{figure} figures/p12-risk-moves.svg
:label: fig-p12-risk-moves
:alt: The five by five risk matrix with five risks shown before and after mitigation. Each cell carries its score L times C in a small number in its upper-left corner, heavy stair-step lines separate the levels, and the words Low, Medium, and High name the three regions in the cells at the bottom left, the top left, and the top right. Dashed open circles mark the scores before and solid filled circles the scores after, joined by arrows. R1 moves down from likelihood 4, consequence 3 to likelihood 2. R2 moves down from likelihood 3, consequence 4 to likelihood 2. R3 moves left from consequence 2 to consequence 1 at likelihood 4, into Low. R4 moves down and left from 3 and 3 to 2 and 2, into Low. R5 moves down from likelihood 2 to 1 at consequence 5 and stays Medium.
:width: 90%

Computed from the scores of {numref}`tbl-p12-example`. Four of the five mitigations lower the likelihood score, which on this matrix moves a risk down; two lower the consequence score, which moves it left. R5, whose consequence is the loss of the vehicle, stays Medium. Heavy lines: the boundaries between the levels; small numbers: the score of each cell.
:::

**Check.** Every mitigation lowers a score and none raises one, as a mitigation must. R5 ends Medium, as the rule predicts for a consequence of 5. The project accepts it with the launch rules in place and keeps tracking it.

## Single-point failures and the mission timeline

The risks so far came from the environment and from the project. Other risks come from the design of the vehicle itself, from parts that the whole mission depends on.

:::{prf:definition} Single-point failure
:label: def-p12-spf

A **single-point failure** is one part of a system, in hardware, software, or a person's action, whose failure alone would lose the mission (NASA 2018, "single failure point").
:::

Examples are the only engine of a single-engine airplane, a single elevator control cable, the one hinge that deploys a solar array, and the one radio of a spacecraft. To find single-point failures, we walk the mission timeline phase by phase. For each part that acts in a phase, we ask whether the mission is lost if this part fails now. {numref}`fig-p12-launch-timeline` does this for the launch of the small launch vehicle.

:::{figure} figures/p12-launch-timeline.svg
:label: fig-p12-launch-timeline
:alt: Six numbered boxes in a row, joined by arrows: 1 liftoff and stage 1 burn, 0 to 2.5 minutes; 2 stage separation, 2.5 minutes; 3 stage 2 ignition, 2.6 minutes; 4 fairing separation, 3 minutes; 5 stage 2 cutoff in orbit, 9 minutes; and 6 payload separation, 10 minutes. A brace over the first box only notes the hazards of the lower atmosphere, winds aloft and triggered lightning. Black diamonds under events 2, 3, 4, and 6 mark single-point failures.
:width: 90%

Schematic of the launch of the invented small launch vehicle, with times after liftoff. Walking the events in order shows where one failure ends the mission.
:::

Stepping through this timeline, we identify four single-point failures:

1. **Stage separation (event 2).** If the stages do not separate, the second stage cannot fly.
2. **Second-stage ignition (event 3).** The second stage has one engine; if it does not start and run, the vehicle cannot reach orbit.
3. **Fairing separation (event 4).** The fairing, the shell that protects the payload through the atmosphere, must come off. With its mass still attached, the vehicle cannot reach orbit. This happened twice to the same rocket. The Taurus XL fairing failed to separate on the launches of NASA's Orbiting Carbon Observatory in 2009 and Glory in 2011, and both satellites were lost (NASA 2019).
4. **Payload separation (event 6).** If the payload does not separate, its mission never starts.

For each single-point failure, a design team has four options: add redundancy (a second independent unit) to eliminate the single point, add design margin or extra testing to lower its failure likelihood while keeping it as a single-point failure, or accept the risk, document the rationale, and track it on the risk matrix. In our example, the project accepts the single second-stage engine because a second engine would add too much mass, and mitigates it through extra testing. Risk R1 is part of that choice.

(p12-redundancy)=
### Redundancy

Of those choices, redundancy is the one we can put a number on. {term}`Redundancy` is the use of more than one independent means to do the same job (NASA 2018). One rule of probability gives its benefit. Let $p$ be the probability that one unit fails during the mission. A single unit loses the function with probability $p$. Two units in parallel, either of which can do the job, lose it only if both fail. If the two fail independently, the probability that both fail is the product of their probabilities:

:::{math}
:label: eq-p12-pair
p_\text{pair} = p \times p = p^2
:::

For a flight computer that works through the mission with probability 0.97, $p = 1 - 0.97 = 0.030$. A redundant pair fails with probability $0.030 \times 0.030 = 0.00090$, and works with probability $1 - 0.00090 = 0.9991$. The chance of losing the function falls by a factor of $1/0.030 = 33.3$ ({numref}`fig-p12-redundancy`).

:::{figure} figures/p12-redundancy.svg
:label: fig-p12-redundancy
:alt: Two block diagrams side by side. (a) Single string: one box, flight computer, on a line from a dot marked in to a dot marked out; it fails with probability p equal to 0.030 and works with probability 0.97. (b) Redundant pair: two boxes, computer A and computer B, one above the other in parallel between the in and out dots; both fail with probability p squared, 0.030 times 0.030, which is 0.00090, so the pair works with probability 0.9991.
:width: 90%

Computed for invented values: each computer works through the mission with probability 0.97, and the two fail independently. A second unit in parallel turns a failure probability $p$ into $p^2$, because the function works as long as one path from the dot marked in to the dot marked out remains intact.
:::

This result applies only if the units fail independently. A {term}`common-cause failure` is the failure of several units from one event or one shared fault (NASA 2018), and it defeats redundancy. The first flight of Ariane 5, in 1996, shows how. Its two inertial reference systems, the units that tell the launch vehicle which way it points, failed within a fraction of a second of each other. The active unit and its backup ran the same software, and the software had a design error. The launch vehicle lost its guidance 37 seconds after the start of the main engine ignition sequence and broke up about 3 seconds later (ESA 1996). Two identical units can share a software error, a power supply, a cable run, or a radiation event. Designers guard against this by separating the units physically and electrically, and sometimes by using two different designs for the same job.

:::{warning} Redundancy has trade-offs
A second unit adds mass, power draw, expense, and new ways to fail. The switch that chooses between the two units can itself become a single-point failure. Add redundancy where a single unit's failure probability is high enough to matter, and check that the pair does fail independently.
:::

## Summary

:::{important} Summary
- A hazard is a condition of the operating environment that can harm the vehicle or the mission. Describe it by its cause, its effect, and a mitigation that acts on the cause, the hazard, or the effect.
- In the atmosphere, hazards follow the phases of flight; in space they follow altitude, and the solar cycle changes several of them.
- A risk is "If [event], then [consequence]" with likelihood L and consequence C from 1 to 5. The score $S = L \times C$ sets the level: High at 15 or more, Medium from 5 to 12, Low at 4 or less. A mitigation lowers the likelihood score or the consequence score; on the matrix of these notes that moves the risk down or left.
- Single-point failures are found by walking the mission timeline. Redundancy turns a failure probability $p$ into $p^2$, but only if the units fail independently.
:::

:::{table} The terms and equations of this page.
:label: tbl-p12-summary
:align: center

| Term | Meaning |
| --- | --- |
| Hazard | A condition of the operating environment that can harm the vehicle or the mission |
| Mitigation | An action that makes harm less likely or less severe |
| Risk statement | "If [event], then [consequence]" |
| Risk score, equation {eq}`eq-p12-score` | $S = L \times C$, with L and C from 1 to 5 |
| Level (convention of these notes) | High: $S$ of 15 or more; Medium: 5 to 12; Low: 4 or less |
| Single-point failure | One part whose failure alone loses the mission |
| Redundant pair, equation {eq}`eq-p12-pair` | Fails with probability $p^2$ if the two units fail independently |

:::

:::{exercise} For discussion
:label: ex-p12-discussion

1. An airliner and a satellite in low orbit both fly through air. Which hazards do they share, and which affect only one of them?
2. The icing band moves up on a warm day. What does that do to the time an aircraft spends in it during a climb?
3. An engineer argues that a High risk with likelihood 5 and consequence 3 matters less than a Medium risk with likelihood 2 and consequence 5. What would you need to know to evaluate that argument?
4. Why might a designer put the two computers of a redundant pair at opposite ends of a spacecraft and power them from different batteries?
5. A satellite will be launched near the next solar maximum. Which of its hazards change, and in which direction?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-1-2.html
:label: quiz-1-2
:enumerated: false
:width: 100%

Quiz for Standard 1.2: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Banks, B. A., de Groh, K. K., and Miller, S. K., *[Low Earth Orbital Atomic Oxygen Interactions with Spacecraft Materials](https://ntrs.nasa.gov/citations/20040191331)*, NASA/TM-2004-213400, NASA Glenn Research Center, 2004.
- European Space Agency (ESA), "[Ariane 501: Presentation of Inquiry Board report](https://www.esa.int/Newsroom/Press_Releases/Ariane_501_-_Presentation_of_Inquiry_Board_report)," press release, 1996.
- European Space Agency (ESA), "[Science of friction: keeping things moving in space](https://www.esa.int/Enabling_Support/Space_Engineering_Technology/Science_of_friction_keeping_things_moving_in_space)," 2015.
- Federal Aviation Administration (FAA), *[Airport Foreign Object Debris (FOD) Management](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_150_5210-24.pdf)*, Advisory Circular 150/5210-24, 2010.
- Federal Aviation Administration (FAA), *[Pilot Guide: Flight in Icing Conditions](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_91-74B.pdf)*, Advisory Circular 91-74B, 2015.
- Federal Aviation Administration (FAA), *[Clear Air Turbulence Avoidance](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_00-30C.pdf)*, Advisory Circular 00-30C, 2016.
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023.
- Federal Aviation Administration (FAA), *[Aeronautical Information Manual](https://www.faa.gov/air_traffic/publications/atpubs/aim_html/)*, n.d. Chapter 7.
- Laboratory for Atmospheric and Space Physics (LASP), "[Penticton Solar Radio Flux at 10.7 cm](https://lasp.colorado.edu/lisird/data/penticton_radio_flux)," LASP Interactive Solar Irradiance Datacenter, daily series of the Dominion Radio Astrophysical Observatory, National Research Council Canada, n.d.
- NASA, *[Spacecraft Radiation Torques](https://ntrs.nasa.gov/citations/19710014836)*, NASA SP-8027, Space Vehicle Design Criteria (Guidance and Control), 1969.
- NASA, "[Apollo 12 Ascent Phase](https://www.nasa.gov/wp-content/uploads/static/history/SP-4029/Apollo_12d_Ascent_Phase.htm)," in *Apollo by the Numbers*, NASA SP-2000-4029, 2000.
- NASA, *[NASA Risk Management Handbook](https://ntrs.nasa.gov/citations/20120000033)*, NASA/SP-2011-3422, 2011.
- NASA, "[Radiation Belts with Satellites](https://www.nasa.gov/image-article/radiation-belts-with-satellites/)," 2013.
- NASA, *[NASA Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)*, NASA/SP-2016-6105 Rev 2, 2016.
- NASA, *[Safety and Mission Assurance Acronyms, Abbreviations, and Definitions](https://ntrs.nasa.gov/citations/20180004878)*, NASA-HDBK-8709.22, 2018.
- NASA, "[NASA Investigation Uncovers Cause of Two Science Mission Launch Failures](https://www.nasa.gov/news-release/nasa-investigation-uncovers-cause-of-two-science-mission-launch-failures/)," news release 19-036, 2019.
- NASA, "[NASA Researchers Track Slowly Splitting 'Dent' in Earth's Magnetic Field](https://www.nasa.gov/missions/icon/nasa-researchers-track-slowly-splitting-dent-in-earths-magnetic-field/)," 2020.
- NASA, *[Mitigating In-Space Charging Effects: A Guideline](https://standards.nasa.gov/sites/default/files/standards/NASA/B/0/2022-06-07-NASA-HDBK-4002B-Approved.pdf)*, NASA-HDBK-4002B, 2022.
- NASA, *[Lightning Launch Commit Criteria](https://standards.nasa.gov/sites/default/files/standards/NASA/A/0/NASA-STD-4010A-Approved.pdf)*, NASA-STD-4010A, 2023.
- NASA Orbital Debris Program Office, "[Frequently Asked Questions](https://orbitaldebris.jsc.nasa.gov/faq/)," n.d.
- NASA Small Spacecraft Systems Virtual Institute, *Small Spacecraft Technology State of the Art*, NASA Ames Research Center, 2021. Chapters 6 ([Structures, Materials, and Mechanisms](https://www.nasa.gov/wp-content/uploads/2021/10/6.soa_structures_2021.pdf)) and 7 ([Thermal Control](https://www.nasa.gov/wp-content/uploads/2021/10/7.soa_thermal_2021_0.pdf)).
- National Oceanic and Atmospheric Administration (NOAA), Space Weather Prediction Center, "[F10.7 cm Radio Emissions](https://www.spaceweather.gov/phenomena/f107-cm-radio-emissions)," n.d.a.
- National Oceanic and Atmospheric Administration (NOAA), Space Weather Prediction Center, "[Satellite Drag](https://www.spaceweather.gov/impacts/satellite-drag)," n.d.b.
- O'Bryan, M. V., et al., "[Compendium of Single Event Effects Results from NASA Goddard Space Flight Center and NASA Electronic Parts and Packaging Program](https://ntrs.nasa.gov/citations/20170008448)," IEEE Nuclear and Space Radiation Effects Conference, Radiation Effects Data Workshop, 2017.
- Space Telescope Science Institute (STScI), "[HST Primer: Orbital Constraints](https://hst-docs.stsci.edu/hsp/the-hubble-space-telescope-primer-for-cycle-34/hst-primer-orbital-constraints)," *Hubble Space Telescope Primer for Cycle 34*, n.d.

