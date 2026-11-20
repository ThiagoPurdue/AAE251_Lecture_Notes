---
title: "Ground tracks, aerobraking, and orbit lifetime"
short_title: Ground tracks and orbit lifetime
---

An orbit fixed in space looks different from the ground, because the planet turns underneath it. This page follows the point directly below a spacecraft across the surface, uses that path to find the period of the orbit and the time an instrument needs to see the whole planet, and then turns to the atmosphere: how a spacecraft can use drag to shrink its orbit, and how drag ends the life of a low orbit. No course standard is assessed on this page.

:::{note} What to take from this page
- A ground track is a great circle on a planet that does not turn. With the planet turning, each pass crosses the equator $\Delta L = {360}^\circ\,T/T_{\text{day}}$ farther west, and the highest latitude reached equals the inclination.
- The swath width, the track spacing, and the number of orbits per day give the days an instrument needs to see the whole equator.
- Aerobraking lowers the apoapsis with drag at periapsis and saves most of the propellant that a burn would cost, at the price of months of passes.
- Drag lowers a low orbit a little every revolution and faster as it sinks. The lifetime grows steeply with altitude and with the ballistic coefficient $B = m/(C_D A)$.
:::

## What a ground track is

A {term}`ground track` is the path traced on the surface by the point directly below the spacecraft. Every orbit lies in a plane through the center of the planet, so on a planet that does not turn the track is where that plane cuts the surface: a great circle, centered on the center of the planet and tilted to the equator by the inclination. Ground tracks decide what a mission can do: an imaging satellite must pass over its targets, and every satellite must pass within sight of a ground station to send its data down.

A flat map changes how that circle looks. Picture the planet as a soda can with a tilted ring around it. Cut the label along one side and unroll it: the ring becomes a single wave, one crest and one trough per turn. On the can the wave is an exact sine curve. On a sphere drawn as a latitude-longitude map it is close to one, as {numref}`fig-p25-great-circle-to-map` shows for an orbit of 50° inclination.

:::{figure} figures/p25-great-circle-to-map.svg
:label: fig-p25-great-circle-to-map
:alt: Left, a globe with its north axis up, an inclined circular orbit around it, and the ground track drawn as a dotted great circle on the surface; a short line joins the spacecraft to the point directly below it. Right, the same track on a longitude and latitude map: a dotted wave that crosses the equator northbound at 0 degrees longitude, peaks at 50 degrees north at 90 degrees east, crosses the equator southbound at 180 degrees, and reaches 50 degrees south at 90 degrees west. A dimension line marks the peak latitude as the inclination, 50 degrees.
:width: 90%

Schematic, not to scale: the orbit is drawn well above the surface so that it can be told apart from its track. Left, an orbit of 50° inclination over a planet that does not turn; the open circle is the point directly below the spacecraft. Right, the same track on a latitude-longitude map, computed. The track is one wave per orbit, and its highest latitude equals the inclination $i$.
:::

The latitude $\phi$ under a circular orbit follows from the spherical triangle between the equator, the orbit, and the meridian of the spacecraft:

:::{math}
:label: eq-p25-latitude
\sin\phi = \sin i\,\sin u
:::

where $u$ is the angle the spacecraft has traveled around the orbit from the {term}`ascending node`, the point where it crosses the equator going north ($u = \omega + \theta$ in the notation of [orbit properties](orbit-properties.md)). The largest value of $\sin u$ is 1, so the highest latitude a prograde orbit reaches equals its {term}`inclination`. A retrograde orbit ($i > {90}^\circ$) reaches ${180}^\circ - i$: an orbit at 98.2° passes over every latitude up to 81.8° north and south.

## The planet turns under the orbit

The orbit plane stays fixed in space while the planet turns east beneath it. During one orbit the planet turns through ${360}^\circ\,T/T_{\text{day}}$, so the next pass crosses the equator that much farther west:

:::{math}
:label: eq-p25-shift
\Delta L = {360}^\circ\,\frac{T}{T_{\text{day}}}
:::

Here $T$ is the {term}`orbital period` and $T_{\text{day}}$ is the {term}`sidereal day`, the time the planet takes to turn once relative to the stars. For Earth it is 86,164 s, or 23.93 h, which is 236 s shorter than the 86,400 s solar day. The solar day is longer because Earth also moves around the Sun and must turn a little more than once to bring the Sun back overhead. The orbit plane is fixed relative to the stars, so the sidereal day is the one to use: Earth turns 15.04° per hour, not 15°.

{numref}`fig-p25-ground-track` shows three successive orbits of an Earth-observation satellite at 700 km altitude and 98.2° inclination. The period at 700 km is 5,926 s, or 98.77 min, so each pass crosses the equator 24.76° farther west. At the equator that is 2,756 km. The shift is westward for prograde and retrograde orbits alike, because it comes from the turning of the planet alone.

:::{figure} figures/p25-ground-track.svg
:label: fig-p25-ground-track
:alt: A longitude and latitude map with three ground tracks of a satellite at 700 kilometers and 98.2 degrees inclination, labeled orbit 1, 2, and 3 and drawn solid, dashed, and dotted. Each track starts at the equator going north and slightly west, runs along 81.8 degrees north, crosses the equator going south, runs along 81.8 degrees south, and comes back to the equator. Dots mark the equator crossings going north: orbit 1 at 45 degrees east, orbit 2 at 20.2 degrees east, orbit 3 at 4.5 degrees west. A double arrow on the equator between the first two dots reads delta L equals 24.76 degrees, 2,756 kilometers.
:width: 80%

Computed for a circular orbit at 700 km altitude and 98.2° inclination over a turning Earth (two-body motion; the slow turning of the orbit plane by Earth's equatorial bulge is left out). Dots mark the northbound equator crossings; each orbit crosses 24.76° farther west than the one before.
:::

### Reading the period off a ground track

[](#eq-p25-shift) also runs backward. Measure the westward shift between two successive northbound equator crossings on a track, and the period follows:

:::{math}
:label: eq-p25-period-from-track
T = \frac{\Delta L}{{360}^\circ}\,T_{\text{day}}
:::

With the period known, the semi-major axis comes from $T = 2\pi\sqrt{a^3/\mu}$ ([the period equation](#eq-p21-period) of orbit properties). For the track of {numref}`fig-p25-ground-track`, $\Delta L = {24.76}^\circ$ gives $T = (24.76/360)(86{,}164) = 5{,}926$ s, then $a = 7{,}078$ km and an altitude of $7{,}078 - 6{,}378 = 700$ km. The inclination comes from the same map: it is the highest latitude for a prograde orbit, or 180° minus it for a retrograde one ([inclination and launch azimuth](#p23-azimuth)).

:::{warning} Use the sidereal day
Dividing by the 86,400 s solar day, or using 15° per hour, makes $\Delta L$ 0.27% too small. The error adds up over a day of passes. Keep $T$ and $T_{\text{day}}$ in the same unit.
:::

### Period, inclination, and the geostationary orbit

A longer period gives the planet more time to turn under one orbit, so the track squeezes together in longitude ({numref}`fig-p25-track-vs-period`). In a 3 h orbit (altitude 4,182 km) Earth turns 45.1° while the spacecraft goes around once, and the track spans most of the map. In an 8 h orbit (altitude 13,929 km) Earth turns 120° and the wave is visibly compressed. When the period equals one sidereal day, the planet turns once per orbit and the track closes on itself: a circular inclined orbit traces a narrow figure eight between the latitudes $\pm i$, the same one every day. That orbit is {term}`geosynchronous <geosynchronous orbit>`. Its radius, from the period equation with $T = 86{,}164$ s, is 42,164 km, an altitude of 35,786 km.

:::{figure} figures/p25-track-vs-period.svg
:label: fig-p25-track-vs-period
:alt: A longitude and latitude map with one revolution of three circular orbits at 40 degrees inclination, all reaching 40 degrees north and south. The 3 hour orbit, solid, is a wide wave spanning most of the map, and the 8 hour orbit, dashed, is a shorter wave. The geosynchronous orbit of 23.93 hours, dotted, is a narrow figure eight centered on the equator at 160 degrees east. A diamond on the equator at 60 degrees east marks the geostationary orbit, whose track is a single point.
:width: 80%

Computed: one revolution of circular orbits at 40° inclination with periods of 3 h, 8 h, and one sidereal day, each starting at the dot on the equator, and the geostationary orbit. The longer the period, the more Earth turns during one orbit and the shorter the track. Every track reaches 40° north and south, the inclination.
:::

Set the inclination of that orbit to zero and the figure eight shrinks to a point: the spacecraft stays above one spot on the equator. This is the {term}`geostationary orbit`. A ground antenna points at a fixed spot in the sky and never has to track, which is why communications and weather satellites use it. The orbit must be equatorial: any inclination carries the spacecraft north and south.

An elliptical orbit adds one more effect. The spacecraft moves fastest near periapsis, so the track is stretched out there and bunched up near apoapsis. Russian Molniya communications satellites use this: their orbits are highly eccentric, and each satellite spends about two-thirds of its 12-hour orbit over one hemisphere (Riebeek 2009).

## Track spacing, swath, and coverage

Neighboring tracks are $\Delta L$ apart in longitude. At the equator that angle is a distance, the track spacing

:::{math}
:label: eq-p25-spacing
d = 2\pi R\,\frac{T}{T_{\text{day}}}
:::

Away from the equator the meridians close in, so the spacing shrinks roughly as $\cos\phi$ and the tracks crowd together near the highest latitude. Coverage is hardest at the equator.

An instrument looking straight down with a field of view FOV sees a strip of ground centered on the track, the swath ({numref}`fig-p25-swath`). For a narrow field of view the ground under the spacecraft is nearly flat, and the {term}`swath width` is

:::{math}
:label: eq-p25-swath
w = 2\,h\,\tan\frac{\text{FOV}}{2}
:::

with $h$ the altitude. For a wide field of view the curvature of the planet makes the real swath wider than this.

:::{figure} figures/p25-swath.svg
:label: fig-p25-swath
:alt: Left, a side view drawn to scale: a spacecraft 700 kilometers above flat ground looks down through a 15 degree field of view, which covers a strip of ground 184.3 kilometers wide. Right, a map near the equator from 60 degrees west to 15 degrees east and 20 degrees south to 20 degrees north, with three northbound passes, labeled orbit 1, 2, and 3, crossing the equator at 0, 24.76, and 49.52 degrees west, each with a narrow gray band, its swath. A double arrow on the equator between orbit 2 and orbit 1 reads 2,756 kilometers. The gaps between the bands are many times wider than the bands.
:width: 100%

Computed for the worked example: 700 km altitude, 98.2° inclination, a 15° field of view. Left, side view to scale. Right, three successive northbound passes near the equator with their swaths to scale. One day of passes leaves wide gaps between the swaths; later days fill them.
:::

At 700 km the spacing is 2,756 km and the swath only 184.3 km, so one day of passes leaves wide gaps, which the following days fill. In the ideal case, where every new swath lands exactly in a gap, the days to see the whole equator are its length divided by the ground imaged per day:

:::{math}
:label: eq-p25-days
N_{\text{days}} = \frac{2\pi R}{w\,n}, \qquad n = \frac{86{,}400\ \text{s}}{T}
:::

where $n$ is the number of orbits per (solar) day. Each orbit crosses the equator twice, once going north and once going south. A camera that needs sunlight images on only one of the two, so the estimate counts one swath per orbit. An instrument that works day and night, such as a radar, would count two.

### Worked example: an Earth-observation satellite at 700 km

A satellite in a circular orbit at $h = 700$ km and $i = {98.2}^\circ$ carries a camera with a 15° field of view. Find the shift and spacing of its tracks, its swath, and the days it needs to see the whole equator. Earth: $\mu = 3.986 \times {10}^{5}\ \text{km}^3/\text{s}^2$, $R = 6{,}378$ km, $T_{\text{day}} = 86{,}164$ s.

1. **Radius and period.** $a = R + h = 6{,}378 + 700 = 7{,}078$ km, and $T = 2\pi\sqrt{a^3/\mu} = 2\pi\sqrt{{7{,}078}^3/(3.986 \times {10}^{5})} = 5{,}926$ s, or 98.77 min.
2. **Westward shift.** $\Delta L = {360}^\circ \times 5{,}926/86{,}164 = {24.76}^\circ$.
3. **Track spacing at the equator.** $d = 2\pi(6{,}378)(5{,}926/86{,}164) = 2{,}756$ km.
4. **Swath.** $w = 2(700)\tan {7.5}^\circ = 184.3$ km.
5. **Orbits per day.** $n = 86{,}400/5{,}926 = 14.58$.
6. **Equator imaged per day.** $w\,n = 184.3 \times 14.58 = 2{,}687$ km.
7. **Days to cover the equator.** $N_{\text{days}} = 2\pi(6{,}378)/2{,}687 = 40{,}074/2{,}687 = 14.91$ days.

**Check.** The track reaches 81.8° north and south, so the orbit passes over almost all of Earth, and covering the equator, where the tracks are farthest apart, covers every latitude the track reaches.

The example is close to a real satellite. Landsat 8 flies a {term}`sun-synchronous orbit` at 705 km and 98.2°, images a 185 km swath, and repeats its track exactly after 233 orbits in 16 days (U.S. Geological Survey n.d.; NASA Science n.d.b). Its neighboring paths are $40{,}074/233 = 172.0$ km apart at the equator, less than the swath, so they overlap slightly; that overlap is why the real cycle is a little longer than the ideal 14.91 days.

:::{table} The coverage estimate of the worked example against Landsat 8. Landsat values from U.S. Geological Survey (n.d.) and NASA Science (n.d.b).
:label: tbl-p25-landsat

| Quantity | Worked example | Landsat 8 |
| --- | ---: | ---: |
| Altitude, km | 700 | 705 |
| Inclination | 98.2° | 98.2° |
| Swath width, km | 184.3 | 185 |
| Orbits per day | 14.58 | 14.56 |
| Days to cover the equator | 14.91 (ideal) | 16 (repeat cycle) |

:::

:::{warning} Altitude in the swath, radius in the period
The swath uses the altitude $h$, the distance to the ground below. The period uses the radius $a = R + h$ from the center of the planet. Using 700 km in the period equation gives a period of 3.1 minutes, an orbit deep inside the planet.
:::

## Ground tracks at other planets

Nothing in [](#eq-p25-shift) to [](#eq-p25-days) is specific to Earth; the 86,400 s in $n$ only sets the unit of the answer, Earth days. At another planet, use that planet's gravitational parameter $\mu$ and radius $R$ for the period and the swath, and its own sidereal rotation period for $T_{\text{day}}$. The highest latitude of the track still equals the inclination, which is why mapping orbits are usually near-polar: a near-polar orbit sweeps every latitude, and the turning planet brings every longitude under it in turn. A planet that turns backward, as Venus does, shifts the track east. The Magellan radar mapper, in a near-polar orbit around Venus, imaged most of the planet in the time Venus took to turn once beneath it (NASA Science n.d.a).

At Earth one more effect matters. Earth's equatorial bulge (the $J_2$ term of its gravity field) slowly turns the orbit plane, and a sun-synchronous orbit, near-polar and slightly retrograde, uses this so that the plane turns once a year and the satellite passes over each place at the same local solar time. The 98.2° inclination of the example is that choice at 700 km (Mesarch 2018).

## Aerobraking

Capturing into a large, elongated orbit costs much less {term}`delta-V` than capturing straight into a low circular one. The rest of the job, bringing the apoapsis down, can be done by the planet's atmosphere. In {term}`aerobraking`, a small burn at apoapsis lowers the periapsis into the upper atmosphere. Each pass through periapsis removes a little speed, the way a short burn against the motion would, and so lowers the apoapsis while the periapsis stays at about the same altitude. After hundreds of passes over weeks or months the orbit is nearly circular, and a second small burn at apoapsis raises the periapsis out of the atmosphere ({numref}`fig-p25-aerobraking`).

:::{figure} figures/p25-aerobraking.svg
:label: fig-p25-aerobraking
:alt: Left, to scale around Venus: a large solid capture ellipse with its periapsis just above the surface on the right, two smaller dashed ellipses after drag passes that share that periapsis, and a dash-dot final circle close to the planet. A short burn arrow, delta-V 1, at the capture apoapsis points against the motion; a longer one, delta-V 2, on the final circle points along it. Right, altitude against distance from periapsis: the drag passes dip to 140 kilometers, below the flat final orbit at 250 kilometers.
:width: 90%

Computed for the Venus orbiter of the worked example. Left, to scale: the 250 km by 25,000 km capture orbit, two orbits after drag passes (apoapsis altitudes of 15,000 and 7,000 km chosen for the drawing, periapsis at 140 km), and the final 250 km circular orbit. $\Delta V_1$ lowers the periapsis into the atmosphere; $\Delta V_2$ lifts it out. The burn arrows are drawn to scale with their $\Delta V$. Right, altitude near periapsis: the drag passes dip to 140 km, below the final orbit.
:::

The trade is propellant against time and risk. Aerobraking takes months of operations instead of minutes of burning. Every pass heats the spacecraft, which must be designed for the loads and the heating, and the team must adjust the periapsis altitude as the density of the upper atmosphere changes from day to day; too deep a pass can destroy the vehicle. In 1993 the Magellan spacecraft became the first planetary orbiter to aerobrake, at Venus (Jet Propulsion Laboratory 1993). Mars Global Surveyor, Mars Odyssey, and Mars Reconnaissance Orbiter later used aerobraking at Mars (Long et al. 2007).

### Worked example: a Venus orbiter

A 1,200 kg orbiter with an engine of $I_{\text{sp}} = 320$ s is captured into a 250 km by 25,000 km orbit around Venus and must end in a 250 km circular orbit. Compare two plans: burns only, and aerobraking with the periapsis at 140 km. Venus: $\mu = 3.249 \times {10}^{5}\ \text{km}^3/\text{s}^2$, $R = 6{,}052$ km. The propellant for each plan comes from the rocket equation, treated with propulsion in Chapter 4:

:::{math}
:label: eq-p25-propellant
m_p = m_0\left[1 - \exp\left(-\frac{\Delta V}{I_{\text{sp}}\,g_0}\right)\right], \qquad g_0 = 9.80665\ \text{m/s}^2
:::

**Plan A, burns only.**

1. **Capture orbit.** $r_p = 6{,}052 + 250 = 6{,}302$ km, $r_a = 6{,}052 + 25{,}000 = 31{,}052$ km, $a = (r_p + r_a)/2 = 18{,}677$ km. One revolution takes 7.82 hours.
2. **Speeds at periapsis.** On the capture orbit $v_p = \sqrt{\mu(2/r_p - 1/a)} = 9.25821$ km/s. On the 250 km circle $v_c = \sqrt{\mu/r_p} = 7.18019$ km/s. The speeds are given to five decimals because the burns of Plan B are differences of close speeds.
3. **Burn.** One burn against the motion at periapsis brings the apoapsis down to 250 km: $\Delta V = 9.25821 - 7.18019 = 2.078$ km/s.
4. **Propellant.** $m_p = 1{,}200\,[1 - \exp(-2{,}078/(320 \times 9.80665))] = 581$ kg.

**Plan B, aerobraking.**

1. **Lower the periapsis.** At apoapsis, lower the periapsis to 140 km ($r = 6{,}192$ km). The speed at apoapsis drops from 1.87895 to 1.86523 km/s: $\Delta V_1 = 1.86523 - 1.87895 = -0.01372$ km/s, a burn of 0.01372 km/s against the motion.
2. **Drag passes.** The atmosphere lowers the apoapsis from 25,000 km to 250 km while the periapsis stays near 140 km. This step uses no propellant, apart from small trim burns left out here.
3. **Raise the periapsis.** At the apoapsis of the final 140 km by 250 km orbit the speed is 7.14851 km/s; the 250 km circle needs 7.18019 km/s: $\Delta V_2 = 7.18019 - 7.14851 = 0.03168$ km/s, along the motion.
4. **Total.** $\Delta V = 0.01372 + 0.03168 = 0.04540$ km/s, and $m_p = 17.2$ kg.

:::{table} Burns only against aerobraking for the 1,200 kg Venus orbiter ($I_{\text{sp}} = 320$ s), from a 250 km by 25,000 km capture orbit to a 250 km circular orbit.
:label: tbl-p25-aerobraking

| Plan | $\Delta V$, km/s | Propellant, kg |
| --- | ---: | ---: |
| Burns only: one burn at periapsis | 2.078 | 581 |
| Aerobraking at 140 km, then two small burns | 0.04540 | 17.2 |

:::

Aerobraking needs 0.04540 km/s of delta-V instead of 2.078 km/s and saves 564 kg, nearly half the mass of the spacecraft.

(p25-orbit-lifetime)=
## Orbit lifetime and the end of the mission

A low Earth orbit is not permanent. The thin air at a few hundred kilometers drags on the spacecraft at every point of the orbit, and the orbit sinks. This {term}`orbit decay` is slow at first and speeds up, because the air gets denser as the orbit gets lower.

### How drag lowers an orbit

The drag force is $D = \tfrac{1}{2}\rho v^2 C_D A$, with $\rho$ the air density, $C_D$ the drag coefficient, and $A$ the reference area. Divided by the mass it is a deceleration $\rho v^2/(2B)$, where

:::{math}
:label: eq-p25-ballistic
B = \frac{m}{C_D A}
:::

is the {term}`ballistic coefficient`. A dense, compact spacecraft has a high $B$ and slows down less.

Drag takes energy out of the orbit. Per unit mass, the rate is the deceleration times the speed: $d\varepsilon/dt = -\rho v^3/(2B)$. The {term}`specific orbital energy` of the orbit is $\varepsilon = -\mu/(2a)$, so $d\varepsilon/dt = (\mu/2a^2)\,da/dt$. Setting the two equal gives $da/dt = -a^2\rho v^3/(\mu B)$. For a nearly circular orbit $v = \sqrt{\mu/a}$, and

:::{math}
:label: eq-p25-decay
\frac{da}{dt} = -\frac{\rho\sqrt{\mu a}}{B}, \qquad \Delta a_{\text{rev}} = -\frac{2\pi\rho a^2}{B}
:::

The second form is the loss in one revolution, the rate times the period $2\pi\sqrt{a^3/\mu}$. Work it in SI units: $\rho$ in kg/m³, $a$ in m, $B$ in kg/m², $\mu$ in m³/s². At 400 km, with the density of the U.S. Standard Atmosphere 1976 ($2.803 \times {10}^{-12}$ kg/m³), $a = 6.778 \times {10}^{6}$ m, and $B = 100$ kg/m², the orbit drops 8.091 m in one revolution. The orbit goes around 15.6 times a day, and the drop grows as the air thickens.

### Lifetimes at 300, 400, and 500 km

Stepping [](#eq-p25-decay) forward in time, with the density updated at each new altitude, gives the curves of {numref}`fig-p25-orbit-lifetime` and the lifetimes of {numref}`tbl-p25-lifetime`. Each 100 km of extra altitude makes the lifetime 6.1 to 8.7 times longer, mostly because the density falls by a factor of 5.4 to 6.8 over the same 100 km. The calculation stops at 150 km. There the density is $2.076 \times {10}^{-9}$ kg/m³ and the orbit loses about 5.6 km every revolution, so reentry follows in less than a day.

:::{figure} figures/p25-orbit-lifetime.svg
:label: fig-p25-orbit-lifetime
:alt: Altitude in kilometers, 100 to 600, against time in days on a log scale from under 1 to 10,000. Three curves start flat at 300, 400, and 500 kilometers and then plunge to 150 kilometers. The 300 kilometer orbit, dotted, ends at 47 days; the 400 kilometer orbit, dashed, at 408 days; the 500 kilometer orbit, solid, at 6.8 years, beyond a dashed vertical line at 5 years. A dashed horizontal line marks 150 kilometers.
:width: 80%

Computed for circular Earth orbits with $B = 100$ kg/m², U.S. Standard Atmosphere 1976 densities, and $da/dt = -\rho\sqrt{\mu a}/B$, followed down to 150 km; time zero is drawn at the left edge of the log axis. Each orbit loses little altitude for most of its life and then falls quickly.
:::

:::{table} Orbit lifetime of a circular Earth orbit with $B = 100$ kg/m², from the start altitude down to 150 km.
:label: tbl-p25-lifetime

| Start altitude, km | Density, kg/m³ | Drop in the first revolution, m | Lifetime |
| ---: | ---: | ---: | ---: |
| 300 | $1.916 \times {10}^{-11}$ | 53.69 | 47 days |
| 400 | $2.803 \times {10}^{-12}$ | 8.091 | 408 days |
| 500 | $5.215 \times {10}^{-13}$ | 1.550 | 2,485 days (6.8 years) |

:::

These are estimates for one fixed atmosphere. The density of the upper atmosphere depends on solar activity: at a given altitude it can change by about ten times between a quiet and an active Sun, and the lifetime changes with it (Wertz and Larson 1999).

:::{warning} Units in the decay equation
[](#eq-p25-decay) mixes the density in kg/m³ with the radius. Put $a$ in meters and $\mu$ in m³/s² ($3.986 \times {10}^{14}$), or the result is off by factors of a thousand. The radius is $R + h$, not the altitude.
:::

### The end of the mission

The end of a satellite's life is planned before launch. The options are:

- **Deorbit.** A burn against the motion lowers the periapsis deep into the atmosphere, and the spacecraft reenters within days. A large spacecraft whose parts could survive reentry is brought down over an empty stretch of ocean.
- **Let drag do it.** A low orbit decays on its own. A lower final orbit or a drag device that lowers $B$ makes it reenter sooner.
- **Move out of the way.** No atmosphere reaches the geostationary orbit, so a geostationary satellite is boosted into a storage orbit with its perigee above 35,986 km altitude, the upper edge of the geostationary zone, where it stays clear of working satellites (U.S. Government 2019).

The rules set the time allowed. The long-standing U.S. Government guideline allows 25 years in orbit after the end of the mission (U.S. Government 2019). In 2022 the Federal Communications Commission adopted a five-year rule for satellites in low Earth orbit that it licenses (Federal Communications Commission 2022). With $B = 100$ kg/m², the 400 km orbit of the table meets it easily; the 500 km orbit, at 6.8 years, does not, and would need a deorbit burn or a lower orbit at the end. Around another planet the rule can run the other way: planetary protection rules can require an orbiter to stay in orbit for decades, so that it does not crash onto a surface that must be kept free of Earth microbes.

## Summary

:::{important} Summary
- The ground track is where the orbit plane cuts the surface. It reaches the latitude $i$ (or ${180}^\circ - i$), and the turning planet moves each pass $\Delta L = {360}^\circ\,T/T_{\text{day}}$ west, with $T_{\text{day}}$ the sidereal day.
- A geosynchronous orbit traces the same track every day; a geostationary orbit, equatorial and circular, stays above one point.
- Swath $w = 2h\tan(\text{FOV}/2)$, spacing $2\pi R\,T/T_{\text{day}}$, and orbits per day give the ideal days to cover the equator. Use the planet's own $\mu$, $R$, and sidereal day.
- Aerobraking trades months of drag passes for most of the propellant of a capture-to-circle burn. Drag lowers low orbits by $2\pi\rho a^2/B$ per revolution, so the lifetime grows steeply with altitude and with $B$.
:::

:::{table} The equations of this page.
:label: tbl-p25-equations

| Quantity | Equation |
| --- | --- |
| Highest latitude of the track | $\phi_{\max} = i$ (prograde), ${180}^\circ - i$ (retrograde) |
| Westward shift per orbit | $\Delta L = {360}^\circ\,T/T_{\text{day}}$ |
| Period from a ground track | $T = (\Delta L/{360}^\circ)\,T_{\text{day}}$ |
| Track spacing at the equator | $d = 2\pi R\,T/T_{\text{day}}$ |
| Swath width | $w = 2h\tan(\text{FOV}/2)$ |
| Days to cover the equator (ideal) | $N_{\text{days}} = 2\pi R/(w\,n)$, $n = 86{,}400\ \text{s}/T$ |
| Propellant for a burn | $m_p = m_0\,[1 - \exp(-\Delta V/(I_{\text{sp}}\,g_0))]$ |
| Ballistic coefficient | $B = m/(C_D A)$ |
| Decay of a nearly circular orbit | $da/dt = -\rho\sqrt{\mu a}/B$, $\Delta a_{\text{rev}} = -2\pi\rho a^2/B$ |

:::

:::{exercise} For discussion
:label: ex-p25-discussion

1. A communications company wants a satellite that stays above a city at 40° N. Why can no orbit do this, and what does a geosynchronous orbit at 40° inclination do instead?
2. The example satellite and a radar satellite fly the same orbit; the radar works day and night. How does that change the days needed to cover the equator?
3. Why do the tracks of a near-polar orbit crowd together near the poles, and what does that mean for how often a place at high latitude is seen?
4. Aerobraking saved 564 kg in the Venus example. What does the mission give up in exchange, and when would you choose burns instead?
5. The lifetime curves stay nearly flat for most of the time and then drop almost vertically. Explain the shape from the densities in the lifetime table.
:::

## References

- Curtis, H. D., *Orbital Mechanics for Engineering Students*, 3rd ed., Butterworth-Heinemann, 2014. Chapter 4 (orbits in three dimensions and ground tracks).
- Federal Communications Commission, *Space Innovation; Mitigation of Orbital Debris in the New Space Age*, Second Report and Order, FCC 22-74, 2022.
- Jet Propulsion Laboratory, "[JPL Explains Successful Aerobraking Experiment](https://www.jpl.nasa.gov/news/jpl-explains-successful-aerobraking-experiment/)," news release, 1993.
- Long, S. M., You, T.-H., Halsell, C. A., Bhat, R. S., Demcak, S. W., Graat, E. J., Higa, E. S., Highsmith, D. E., Mottinger, N. A., and Jah, M. K., "[Mars Reconnaissance Orbiter Aerobraking Daily Operations and Collision Avoidance](https://ntrs.nasa.gov/citations/20080012690)," Proceedings of the 20th International Symposium on Space Flight Dynamics, 2007.
- Mesarch, M., "[GDC Orbit Primer](https://science.nasa.gov/wp-content/uploads/2023/05/GDC_OrbitPrimer.pdf)," NASA Goddard Space Flight Center, Navigation and Mission Design Branch, 2018.
- NASA Science, "[Magellan](https://science.nasa.gov/mission/magellan/)," mission overview, n.d.a.
- NASA Science, "[Worldwide Reference System (WRS)](https://science.nasa.gov/mission/landsat/worldwide-reference-system)," Landsat mission pages, n.d.b.
- Riebeek, H., "[Catalog of Earth Satellite Orbits](https://science.nasa.gov/earth/earth-observatory/catalog-of-earth-satellite-orbits)," NASA Earth Observatory, 2009.
- Sellers, J. J., Astore, W. J., Giffen, R. B., and Larson, W. J., *Understanding Space: An Introduction to Astronautics*, 3rd ed., McGraw-Hill, 2005. Section on spacecraft ground tracks.
- U.S. Geological Survey, "[Landsat 8](https://www.usgs.gov/landsat-missions/landsat-8)," Landsat Missions, n.d.
- U.S. Government, "[U.S. Government Orbital Debris Mitigation Standard Practices, 2019 Update](https://orbitaldebris.jsc.nasa.gov/library/usg_orbital_debris_mitigation_standard_practices_november_2019.pdf)," 2019.
- *U.S. Standard Atmosphere, 1976*, NOAA, NASA, and U.S. Air Force, NOAA-S/T 76-1562, 1976.
- Vallado, D. A., *Fundamentals of Astrodynamics and Applications*, 4th ed., Microcosm Press, 2013. Chapter on perturbations (atmospheric drag).
- Wertz, J. R., and Larson, W. J. (eds.), *Space Mission Analysis and Design*, 3rd ed., Microcosm Press and Kluwer, 1999. Chapter 5 (space mission geometry), Chapter 6 (orbit perturbations), Chapter 7 (orbit and constellation design), and Section 8.1 (the atmosphere and orbit decay).
