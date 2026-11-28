---
title: "2.3 Launch to Orbit"
short_title: 2.3 Launch to Orbit
---

:::{include} ../_parts/standards/2.3.md
:::

Reaching {term}`low Earth orbit` takes more than matching circular orbital speed at the right altitude: the rocket also has to fight gravity and atmospheric drag on the way up, while taking advantage of Earth's rotation when launching eastward. Here we assemble the launch {term}`delta-V budget` by combining target orbital speed, ascent losses, and the rotational boost from the launch site. We also connect launch azimuth, site latitude, and orbital inclination to see which orbits a given launch site can reach directly.

:::{note} What to take from this page
- A launch must deliver the circular speed of the target orbit along the orbit plane. The site already moves east with Earth, and the vehicle supplies the difference.
- The {term}`launch azimuth` $\textit{Az}$, the site latitude $\phi$, and the orbit inclination $i$ obey $\cos i = \cos\phi\,\sin\textit{Az}$. A direct launch never reaches an inclination lower than the latitude.
- Earth's rotation adds $\Delta V_{\text{rot}} = \omega R_E\cos\phi\,\sin\textit{Az}$, which is a gain for an eastward launch and a loss for a westward one.
- The budget is $\Delta V_{\text{total}} = v_{\text{orbit}} + \Delta V_{\text{losses}} - \Delta V_{\text{rot}}$, with losses of about 1.5 to 2.0 km/s for low Earth orbit (see [ascent and losses](#p23-losses)).
:::

## Low Earth orbit

Most launches end in a low Earth orbit, either as the final working orbit or as a {term}`parking orbit` for a later transfer burn. Compared with Earth's size, low Earth orbit is a thin shell close to the surface. Drawn to scale in {numref}`fig-p23-leo-to-scale`, the entire band is about 29% of Earth's radius thick.

:::{prf:definition} Low Earth orbit
:label: def-p23-leo

A **low Earth orbit** is an orbit around Earth with an altitude between about 160 km and 2,000 km.
:::

The lower limit comes from the atmosphere. Below about 160 km the air is dense enough that drag takes energy from the satellite on every revolution, and the orbit shrinks quickly. We work out how fast in [orbit lifetime](#p25-orbit-lifetime), where a satellite at 150 km reenters in less than a day. The upper limit of 2,000 km is a convention.

On this page we use Earth's mean radius, $R_E = 6{,}371$ km. The other pages of the chapter use the equatorial radius, 6,378 km. The two differ by about 0.1%, which changes results only in the fourth significant figure.

Across the band the circular speed falls from 7.812 km/s at 160 km to 6.900 km/s at 2,000 km, and the period grows from 87.5 minutes to 127 minutes. (The equations for [circular speed](#p21-circular-and-escape) and for the orbital period are on [orbit properties](orbit-properties.md).)

:::{figure} figures/p23-leo-to-scale.svg
:label: fig-p23-leo-to-scale
:alt: Earth drawn as a disc with a thin shaded ring around it between 160 kilometers and 2,000 kilometers altitude, labeled low Earth orbit. A long arrow runs from Earth's center to a short arc of the geostationary orbit far to the right, labeled by its radius, 42,164 kilometers. The whole low Earth orbit band is narrower than a third of Earth's radius.
:width: 80%

Computed to scale from Earth's mean radius (6,371 km): the edges of low Earth orbit (160 and 2,000 km altitude), and the geostationary orbit (the circular equatorial orbit whose period is one sidereal day) at its radius, 42,164 km. Low Earth orbit is a thin shell next to the surface.
:::

For contrast, a geostationary satellite circles at a radius of 42,164 km. That is 35,786 km above the equator (measured from the equatorial radius, 6,378 km), more than six Earth radii out. To get there, a spacecraft needs a transfer from a low parking orbit, which we cover on [orbit transfers](orbit-transfers.md).

:::{warning} Altitude is not radius
Every orbit equation uses the distance from Earth's center, $r = R_E + h$. A "550 km orbit" has $r = 6{,}371 + 550 = 6{,}921$ km. If you put 550 km into $\sqrt{\mu/r}$, you get about 27 km/s, more than three times the right answer.
:::

The {term}`inclination` $i$ is the angle between the orbit plane and the equator at the {term}`ascending node` (see [orbit properties](orbit-properties.md)). It sorts low orbits into the three kinds of {numref}`tbl-p23-orbit-types`.

:::{table} Kinds of orbit by inclination.
:label: tbl-p23-orbit-types
:align: center

| Kind | Inclination | How the satellite moves |
| --- | --- | --- |
| {term}`Prograde orbit` | $0^\circ \le i < {90}^\circ$ | Eastward, with Earth's rotation; $i = 0^\circ$ is an equatorial orbit |
| {term}`Polar orbit` | $i = {90}^\circ$ (in practice, close to it) | Over both poles; Earth turns beneath it, so it passes over every latitude |
| {term}`Retrograde orbit` | ${90}^\circ < i \le {180}^\circ$ | Westward, against Earth's rotation |

:::

## What a launch has to deliver

Reaching orbit requires far more energy for horizontal speed than for altitude. At 550 km the circular speed is 7.589 km/s, so each kilogram in orbit carries $v^2/2 = 28.8\ \text{km}^2/\text{s}^2$ of kinetic energy, while lifting the same kilogram from the surface to 550 km takes only $\mu/R_E - \mu/r = 4.97\ \text{km}^2/\text{s}^2$. The orbital speed requires 5.8 times as much energy as the altitude.

Velocity is a vector, so the vehicle must deliver both the speed and the direction. The direction is horizontal, along the plane of the target orbit. The vehicle also does not start from rest. The launch pad turns with Earth, so before liftoff the vehicle already moves east with the velocity of the site, $\mathbf{v}_{\text{site}}$. The vehicle supplies the rest:

:::{math}
:label: eq-p23-vector
\mathbf{v}_{\text{orbit}} = \mathbf{v}_{\text{site}} + \Delta\mathbf{V}
\qquad\Longrightarrow\qquad
\Delta\mathbf{V} = \mathbf{v}_{\text{orbit}} - \mathbf{v}_{\text{site}}
:::

The bold symbols are vectors, and $v_{\text{orbit}}$, $v_{\text{site}}$, and $\Delta V$ (delta-V) are their magnitudes. We start with the simplest case, a launch from the equator due east into an equatorial orbit. The two velocities then point the same way, and the magnitudes subtract. For a 550 km orbit ({numref}`fig-p23-velocity-vectors`):

$$
\begin{aligned}
\Delta V &= v_{\text{orbit}} - v_{\text{site}}\\
         &= 7.589 - 0.4646\\
         &= 7.124\ \text{km/s}
\end{aligned}
$$

:::{figure} figures/p23-velocity-vectors.svg
:label: fig-p23-velocity-vectors
:alt: Earth seen from above the north pole, turning counterclockwise at the rate omega, with a launch site on the equator at the bottom of the disc. Just below the site a short thin arrow pointing east is the site velocity, 0.4646 kilometers per second, and head to tail with it a long arrow of 7.124 kilometers per second is the delta-V. Below them a single arrow of 7.589 kilometers per second, the orbit velocity, starts and ends at the same places. A reference arrow shows the length of 1 kilometer per second.
:width: 70%

Computed for a due-east launch from the equator into a 550 km circular equatorial orbit: the velocity of the launch site plus the vehicle's velocity change equals the orbit velocity. Arrows to scale (reference arrow: 1 km/s); Earth not to the arrows' scale. Rotation supplies 6.1% of the orbit speed.
:::

So far we count only the velocity. The losses of the climb come on top of it, and we add them in [the delta-V budget](#p23-budget).

(p23-rotation)=
## Earth's rotation

First we need the speed of the site. Earth turns once relative to the stars in a sidereal day of 86,164 s, so its rotation rate is $\omega = 2\pi/86{,}164\ \text{s} = 7.292 \times {10}^{-5}$ rad/s. On this page $\omega$ is this rotation rate. (On [orbit properties](orbit-properties.md) the same letter names the argument of periapsis.) A point at latitude $\phi$ moves east on a circle of radius $R_E\cos\phi$ around the axis, so its speed is

:::{math}
:label: eq-p23-surface
v_{\text{site}} = \omega R_E \cos\phi
:::

At the equator this is $\omega R_E = (7.292 \times {10}^{-5})(6{,}371) = 0.4646$ km/s. It falls to zero at the poles.

Only the part of the site velocity along the launch direction helps. The site velocity points east. A launch toward azimuth $\textit{Az}$, measured clockwise from north, makes an angle of ${90}^\circ - \textit{Az}$ with east. So the useful part is $v_{\text{site}}\cos({90}^\circ - \textit{Az}) = v_{\text{site}}\sin\textit{Az}$:

:::{math}
:label: eq-p23-rot
\Delta V_{\text{rot}} = \omega R_E \cos\phi \, \sin\textit{Az}
:::

$\Delta V_{\text{rot}}$ is positive for any launch with an eastward part ($0^\circ < \textit{Az} < {180}^\circ$) and zero due north or due south. For a westward launch it is negative, because the vehicle must first cancel the eastward speed it started with. {numref}`fig-p23-rotation-gain` plots it against azimuth. Due east, the gain is 0.4575 km/s at latitude 10°, 0.3559 km/s at 40°, and 0.1963 km/s at 65°.

:::{figure} figures/p23-rotation-gain.svg
:label: fig-p23-rotation-gain
:alt: Plot of the delta-V from Earth's rotation, in kilometers per second, against launch azimuth from 0 to 360 degrees, for latitudes 10, 40, and 65 degrees. Each curve is a sine wave that starts at zero due north, peaks due east at 90 degrees (0.4575, 0.3559, and 0.1963 kilometers per second, marked), crosses zero due south at 180 degrees, and is most negative due west at 270 degrees. The lower the latitude, the larger the swing.
:width: 80%

Computed from $\Delta V_{\text{rot}} = \omega R_E\cos\phi\,\sin\textit{Az}$ for three latitudes: the velocity gained from Earth's rotation against launch azimuth. Markers: due east, the largest gain. A westward launch incurs an equal penalty, adding the same amount to the required $\Delta V$.
:::

The rest of the site velocity, $\omega R_E\cos\phi\,\cos\textit{Az}$, lies across the launch direction. In [the delta-V budget](#p23-budget) we leave it out. The error is small. Even in the worst case, a launch due north from the equator into the 550 km orbit, the exact vector difference of {eq}`eq-p23-vector` is only 14 m/s larger than the budget.

:::{warning} The sign of a westward launch
For ${180}^\circ < \textit{Az} < {360}^\circ$, $\sin\textit{Az}$ is negative and so is $\Delta V_{\text{rot}}$. The budget subtracts $\Delta V_{\text{rot}}$, and subtracting a negative number makes the total larger. Keep the sign that $\sin\textit{Az}$ gives.
:::

(p23-azimuth)=
## Launch azimuth, latitude, and inclination

The launch direction also determines which orbit we reach, because the launch site and launch direction together fix the orbit plane. Three angles describe this geometry.

:::{prf:definition} Launch azimuth
:label: def-p23-azimuth

The **launch azimuth** $\textit{Az}$ is the direction in which the vehicle flies, measured at the launch site in the local horizontal plane, clockwise from north. Here $0^\circ$ is due north, ${90}^\circ$ due east, ${180}^\circ$ due south, and ${270}^\circ$ due west.
:::

The other two are the latitude $\phi$ of the site, measured from the equator, and the inclination $i$ of the orbit. We relate the three under two assumptions:

- The vehicle climbs in one plane through Earth's center, with no turns out of that plane. The orbit plane then contains the launch site.
- $\textit{Az}$ is the direction of the vehicle's velocity in a frame that does not turn with Earth. It differs a little from the azimuth measured on the ground, and we leave that difference out.

{numref}`fig-p23-launch-geometry` shows where the orbit plane cuts the sphere. The orbit crosses the equator northbound at the ascending node and passes over the launch site. The meridian through the site crosses the equator at a right angle. The three arcs form a right spherical triangle:

- the side from the foot of the meridian to the site is the latitude $\phi$;
- the angle at the ascending node, between the equator and the orbit, is the inclination $i$;
- the angle at the site, between the meridian (looking south, toward the foot) and the orbit (looking back toward the node), is the launch azimuth $\textit{Az}$ for a northeast launch.

:::{figure} figures/p23-launch-geometry.svg
:label: fig-p23-launch-geometry
:alt: A globe with the north pole marked N and the equator drawn, cut by the orbit plane in a great circle that crosses the equator at the ascending node, where it makes the angle i with the equator, and climbs northeast through the launch site. At the site an arrow points north along the meridian; the arc from it to the orbit, measured clockwise, is the azimuth Az, and an arrowhead on the orbit just past the site marks the launch direction. The meridian from the site down to the equator is the latitude phi and meets the equator at a right angle. Node, site, and the foot of the meridian form a right spherical triangle.
:width: 70%

Schematic of the launch geometry, drawn for the worked example: latitude 30.4°, inclination 40°, azimuth 62.6°. The orbit plane, the equator, and the meridian through the site form a right spherical triangle with the right angle at the equator. The dashed part of the orbit is behind the globe.
:::

In any right spherical triangle, one of Napier's rules relates the two acute angles to the opposite side. The cosine of either acute angle equals the cosine of its opposite side times the sine of the other acute angle. Applying this identity to the angle $i$ at the node, whose opposite side is $\phi$ and whose companion acute angle is $\textit{Az}$, gives

:::{math}
:label: eq-p23-azimuth
\cos i = \cos\phi \, \sin\textit{Az}
:::

The same relation applies to a southeast launch, which crosses the equator at the descending node instead. It also applies to a site in the southern hemisphere, because $\cos\phi$ does not change when the latitude is south instead of north.

### What the equation says

We solve {eq}`eq-p23-azimuth` for the azimuth:

$$
\sin\textit{Az} = \frac{\cos i}{\cos\phi}
$$

1. **The inclination is never less than the latitude.** For a prograde orbit the azimuth lies between $0^\circ$ and ${180}^\circ$, so $0 \le \sin\textit{Az} \le 1$. Then $0 \le \cos i/\cos\phi \le 1$, which gives $\cos i \le \cos\phi$. The cosine falls as the angle grows from $0^\circ$ to ${90}^\circ$, so $i \ge \phi$.
2. **Due east gives the lowest inclination, equal to the latitude.** When $\textit{Az} = {90}^\circ$, we have $\sin\textit{Az} = 1$ and $\cos i = \cos\phi$, so $i = \phi$.
3. **Two azimuths reach the same inclination.** Because $\sin\textit{Az} = \sin({180}^\circ - \textit{Az})$, a northeast launch at $\textit{Az}$ and a southeast launch at ${180}^\circ - \textit{Az}$ put the vehicle in orbits of the same inclination. The two orbits lie in different planes, because over the site one moves northbound and the other southbound.
4. **A retrograde orbit needs a westward launch.** For $i > {90}^\circ$, $\cos i < 0$, so $\sin\textit{Az} < 0$ and ${180}^\circ < \textit{Az} < {360}^\circ$. The highest inclination, ${180}^\circ - \phi$, comes from a launch due west.
5. **A polar orbit needs a launch due north or due south**, where $\sin\textit{Az} = 0$.

{numref}`fig-p23-inclination-vs-azimuth` shows all five at once, for latitudes of 10°, 40°, and 65°.

:::{figure} figures/p23-inclination-vs-azimuth.svg
:label: fig-p23-inclination-vs-azimuth
:alt: Plot of orbit inclination against launch azimuth from 0 to 360 degrees for latitudes 10, 40, and 65 degrees. Every curve starts at 90 degrees (polar) due north, falls to its minimum due east at 90 degrees azimuth, where the inclination equals the latitude (10, 40, and 65 degrees, marked), returns to 90 degrees due south, rises to its maximum of 180 degrees minus the latitude due west (170, 140, and 115 degrees), and ends at 90 degrees. Below the 90 degree line the orbits are prograde, above it retrograde.
:width: 80%

Computed from $\cos i = \cos\phi\,\sin\textit{Az}$ for three latitudes: orbit inclination against launch azimuth. Markers: due east, where the inclination is lowest and equal to the latitude. Each inclination between $\phi$ and ${90}^\circ$ is reached by two azimuths, one each side of due east.
:::

Now combine {eq}`eq-p23-azimuth` with {eq}`eq-p23-rot`. The product $\cos\phi\,\sin\textit{Az}$ appears in both, so for a direct launch into inclination $i$

:::{math}
:label: eq-p23-rot-cosi
\Delta V_{\text{rot}} = \omega R_E \cos i
:::

for any launch site that can reach that inclination directly. Because a lower-latitude site must launch farther from due east to reach the same inclination, $\sin\textit{Az}$ decreases by the same factor that $\cos\phi$ increases, leaving their product unchanged. So a site near the equator gets no extra rotation boost into a 40° orbit compared with a site at 30°; its advantage is that it can reach low inclinations directly without a plane change.

:::{warning} Degrees and radians
The angles on this page are in degrees and $\omega$ is in radians per second. Set your calculator to degrees for $\sin\textit{Az}$ and $\cos\phi$. The product $\omega R_E$ needs no angle unit and gives km/s when $R_E$ is in km.
:::

## Launch sites and range safety

The latitude of a site fixes the lowest inclination it reaches by a direct launch. {numref}`tbl-p23-sites` lists four sites from low to high latitude.

:::{table} Latitude of four launch sites and the lowest inclination each reaches directly (a launch due east). Latitudes as published by ESA (Kourou, Baikonur), ISRO (Sriharikota, first launch pad), and Craig and Ahmad (2020) for Kennedy. These are agency reference latitudes; individual launch pads can differ by a few tenths of a degree.
:label: tbl-p23-sites
:align: center

| Launch site | Latitude | Lowest inclination, direct launch |
| --- | ---: | ---: |
| Guiana Space Centre, Kourou, French Guiana | 5.05° N | 5.05° |
| Satish Dhawan Space Centre, Sriharikota, India | 13.7° N | 13.7° |
| Kennedy Space Center, Florida, United States | 28.5° N | 28.5° |
| Baikonur Cosmodrome, Kazakhstan | 45.6° N | 45.6° |

:::

An orbit below a site's latitude is still possible, but not directly. The vehicle launches due east into an orbit inclined at the latitude. Then a separate burn turns the orbit plane, and that burn requires a large $\Delta V$ (see [the plane change](#p22-plane-change)). This is why geostationary satellites, which must end at $i = 0^\circ$, are best launched from sites near the equator.

Range safety places a second constraint on launch azimuth. Every launch range must keep spent stages, debris, and a failed vehicle away from populated areas, so each site launches only over open water or unpopulated land within a sector of permitted azimuths. The edges of that sector set the inclinations the site can reach. {numref}`fig-p23-azimuth-fan` illustrates this for a coastal site at 35° N with ocean to the east and an allowed sector from 50° to 140°. Due east gives 35.0°, the northern edge gives 51.1°, and the southern edge gives 58.2°. Inclinations from 35.0° to 51.1° can be reached with either a northeast or a southeast launch, while those from 51.1° to 58.2° can be reached only toward the southeast; polar and retrograde orbits are out of reach from this site.

:::{figure} figures/p23-azimuth-fan.svg
:label: fig-p23-azimuth-fan
:alt: A compass rose centered on a launch site at latitude 35 degrees north, with north at the top. A hatched sector, the allowed azimuths, opens toward the sea from 50 to 140 degrees; the western half, over land, is closed. Three arrows from the site mark the edges and due east: azimuth 50 degrees gives an inclination of 51.1 degrees, 90 degrees gives 35.0 degrees, and 140 degrees gives 58.2 degrees.
:width: 70%

Schematic of the allowed launch azimuths at a coastal site at latitude 35° N (a generic site, not a published range limit). The sector reaches inclinations from 35.0° to 58.2° only. Inclinations computed from $\cos i = \cos\phi\,\sin\textit{Az}$.
:::

Launch timing introduces a third constraint. Because the target orbit plane stays fixed in space while the launch site turns with Earth, launching directly into a specific plane (such as that of a space station) requires liftoff as the site rotates through that plane. For $i > \phi$ this alignment occurs twice each sidereal day, once for the northeast azimuth and once for the southeast azimuth; for $i = \phi$ it occurs once. The {term}`launch window` is the span of time around each passage during which the vehicle still has enough performance to reach the plane. Once in orbit, the inclination also sets the highest latitude the satellite passes over, as we see on [ground tracks](ground-tracks-and-orbit-lifetime.md).

(p23-losses)=
## Ascent and losses

So far we have modeled launch as an instantaneous velocity change at the surface. A real launch vehicle climbs gradually through the atmosphere, as sketched in {numref}`fig-p23-ascent-profile`:

1. **Vertical rise.** The vehicle climbs straight up, clear of the tower and into thinner air.
2. **Pitch-over.** After a few seconds, a small tilt toward the launch azimuth starts the turn.
3. **Gravity turn.** The engines then thrust along the velocity, and gravity alone bends the path toward the horizontal. Stages drop away as they empty, and the payload fairing drops once the vehicle is above most of the atmosphere.
4. **Orbit insertion.** The upper stage accelerates almost horizontally until it reaches orbit speed at the target altitude.

:::{figure} figures/p23-ascent-profile.svg
:label: fig-p23-ascent-profile
:alt: Altitude against downrange distance for a launch, without numbers. The path rises vertically from liftoff, pitches over just above the ground, and curves over in a gravity turn, passing first-stage separation and fairing jettison, until it runs horizontal at orbit insertion. A dashed line low on the plot marks the top of the dense lower atmosphere.
:width: 70%

Schematic of an ascent to low Earth orbit, not to scale. The path is vertical at liftoff and horizontal at insertion; the vehicle spends roughly its first minute in the dense lower atmosphere.
:::

Some of the velocity change the engines produce never shows up as orbit speed. We call the difference the losses, and three of them matter:

- **{term}`Gravity loss`.** While the vehicle climbs, gravity pulls back along its trajectory, reducing its speed by $g\sin\gamma$ each second at flight-path angle $\gamma$ above the horizontal. The longer and steeper the climb, the larger this integral becomes; it accounts for both the potential energy needed to reach orbit altitude and the extra loss from burning over a finite time against gravity.
- **Drag loss.** Air drag $D$ slows a vehicle of mass $m$ by $D/m$ each second. It is largest low in the atmosphere, where the air is dense and the vehicle is already fast.
- **Steering loss.** To steer the vehicle onto its path, the thrust $T$ points away from the velocity by an angle $\alpha$. Only $T\cos\alpha$ then accelerates the vehicle along the path.

:::{math}
:label: eq-p23-losses
\Delta V_{\text{losses}} = \int g\sin\gamma\,dt + \int \frac{D}{m}\,dt + \int \frac{T}{m}\,(1 - \cos\alpha)\,dt
:::

Gravity loss and drag loss work in opposite directions. A steeper climb leaves the dense lower atmosphere sooner and reduces drag loss, but it increases the vertical component of flight and adds gravity loss. Pitching over early does the reverse, so most launch vehicles fly a gravity turn as a balance between the two. Because evaluating these integrals requires a full trajectory simulation, we use a single planning value for preliminary estimates. Gravity losses are typically 1.0 to 1.5 km/s and drag losses 0.10 to 0.15 km/s (Dresia et al. 2021); adding steering losses and margin gives a typical total of 1.5 to 2.0 km/s for low Earth orbit.

(p23-budget)=
## The delta-V budget

Now we assemble the complete budget. The vehicle must reach the circular speed $v_{\text{orbit}}$ at the target radius and overcome the ascent losses, while Earth's rotation supplies part of the required velocity when launching eastward.

:::{prf:definition} Delta-V budget
:label: def-p23-budget

The **delta-V budget** of a launch is the total velocity change the vehicle must produce to reach the target orbit:

$$
\Delta V_{\text{total}} = v_{\text{orbit}} + \Delta V_{\text{losses}} - \Delta V_{\text{rot}}
$$
:::

The orbit speed is the circular speed at $r = R_E + h$ ([circular speed](#p21-circular-and-escape) and [the vis-viva equation](#p21-vis-viva) with $a = r$):

:::{math}
:label: eq-p23-vc
v_{\text{orbit}} = \sqrt{\frac{\mu}{r}} = \sqrt{\frac{\mu}{R_E + h}}
:::

The total is what the stages of the vehicle must provide. Through [the rocket equation](#p42-rocket-equation), it sets how much propellant they carry.

:::{tip} Method: delta-V from a launch site to a low circular orbit
1. Convert the altitude to a radius using $r = R_E + h$.
2. Check that the inclination can be reached directly, meaning $\phi \le i \le {180}^\circ - \phi$, with $\phi$ taken as positive in either hemisphere. If not, launch due east and add a plane change.
3. Find the launch azimuth from $\sin\textit{Az} = \cos i/\cos\phi$. Your calculator gives one angle between $-{90}^\circ$ and ${90}^\circ$. The second is ${180}^\circ$ minus it (add ${360}^\circ$ to a negative angle). Keep the one the range allows.
4. Compute $\Delta V_{\text{rot}} = \omega R_E\cos\phi\,\sin\textit{Az}$, with its sign. Check it against $\omega R_E\cos i$.
5. Compute $v_{\text{orbit}} = \sqrt{\mu/r}$.
6. Combine the terms in $\Delta V_{\text{total}} = v_{\text{orbit}} + \Delta V_{\text{losses}} - \Delta V_{\text{rot}}$.
7. Check that $|\Delta V_{\text{rot}}|$ is at most 0.4646 km/s, and that $v_{\text{orbit}}$ lies between 6.900 and 7.812 km/s for any low Earth orbit.
:::

:::{warning} Kilometers and meters
Use $\mu = 3.986 \times {10}^5\ \text{km}^3/\text{s}^2$ with $r$ in km, and $R_E$ in km in $\omega R_E$. Every term then comes out in km/s. If you mix a $\mu$ in m³/s² with a radius in km, the speed is off by a factor of 31.6, as on [orbit properties](orbit-properties.md).
:::

(p23-example)=
## Worked example: launch from a site at 30.4° N

A launch vehicle flies from a coastal launch site at latitude $\phi = {30.4}^\circ$ N to a circular orbit at $h = 550$ km with inclination $i = {40}^\circ$. Gravity, drag, and steering losses are $\Delta V_{\text{losses}} = 1.6$ km/s. Find the launch azimuth, the rotation gain, and the total delta-V. Use $\mu = 3.986 \times {10}^5\ \text{km}^3/\text{s}^2$, $R_E = 6{,}371$ km, and $\omega = 7.292 \times {10}^{-5}$ rad/s.

1. **Radius.** $r = R_E + h = 6{,}371 + 550 = 6{,}921$ km.
2. **Reach.** The orbit can be reached directly, because $i = {40}^\circ$ lies between $\phi = {30.4}^\circ$ and ${180}^\circ - {30.4}^\circ$.
3. **Launch azimuth**, {eq}`eq-p23-azimuth`:
   $$
   \begin{aligned}
   \sin\textit{Az} &= \frac{\cos i}{\cos\phi}\\
                   &= \frac{\cos {40}^\circ}{\cos {30.4}^\circ}\\
                   &= 0.8882
   \end{aligned}
   $$
   so $\textit{Az} = {62.6}^\circ$ or ${180}^\circ - {62.6}^\circ = {117.4}^\circ$.
   Both reach the 40° inclination, with ${62.6}^\circ$ to the northeast and ${117.4}^\circ$ to the southeast. Range safety restrictions determine which azimuth we fly.
4. **Rotation gain**, {eq}`eq-p23-rot`. The site moves east at $\omega R_E\cos\phi = (7.292 \times {10}^{-5})(6{,}371)\cos {30.4}^\circ = 0.4007$ km/s, and
   $$
   \begin{aligned}
   \Delta V_{\text{rot}} &= \omega R_E\cos\phi\,\sin\textit{Az}\\
                         &= 0.4007 \times 0.8882\\
                         &= 0.3559\ \text{km/s}
   \end{aligned}
   $$
   The southeast azimuth gives the same value, since $\sin {117.4}^\circ = \sin {62.6}^\circ$. Checking with {eq}`eq-p23-rot-cosi` gives $\omega R_E\cos {40}^\circ = 0.4646 \times 0.7660 = 0.3559$ km/s.
5. **Orbit speed**, {eq}`eq-p23-vc`:
   $$
   \begin{aligned}
   v_{\text{orbit}} &= \sqrt{\frac{\mu}{r}}\\
                    &= \sqrt{\frac{3.986 \times {10}^5}{6{,}921}}\\
                    &= 7.589\ \text{km/s}
   \end{aligned}
   $$
6. **Total.**
   $$
   \begin{aligned}
   &\Delta V_{\text{total}}\\
   &\;\;\;= v_{\text{orbit}} + \Delta V_{\text{losses}}\\
   &\;\;\;\phantom{=}{} - \Delta V_{\text{rot}}\\
   &\;\;\;= 7.589 + 1.6 - 0.3559\\
   &\;\;\;= 8.833\ \text{km/s}
   \end{aligned}
   $$

**Check.** The rotation gain, 0.3559 km/s, is below the equatorial maximum of 0.4646 km/s, and the orbit speed lies inside the low-orbit range. {numref}`fig-p23-budget` shows how the three terms add up.

:::{figure} figures/p23-budget.svg
:label: fig-p23-budget
:alt: Bar chart of the delta-V budget of the worked example. A first bar rises to the orbit speed, 7.589 kilometers per second, and a floating bar for the losses adds 1.6 kilometers per second on top of it, to 9.189. A short floating bar for the rotation hangs down from there by 0.3559 kilometers per second. The last bar, the total, rises from zero to 8.833 kilometers per second.
:width: 75%

Computed for the worked example: the delta-V budget of a launch from latitude 30.4° N to a 550 km circular orbit at 40° inclination with 1.6 km/s of losses. Earth's rotation accounts for about 4% of the total.
:::

**Comparison.** {numref}`tbl-p23-example` repeats the budget for the same orbit with three other launch directions.

:::{table} Delta-V budget to a 550 km circular orbit from latitude 30.4° N with 1.6 km/s of losses, for four launch directions.
:label: tbl-p23-example
:align: center

| Launch direction | Azimuth $\textit{Az}$ | Inclination $i$ | Rotation gain $\Delta V_{\text{rot}}$ (km/s) | Total $\Delta V_{\text{total}}$ (km/s) |
| --- | ---: | ---: | ---: | ---: |
| Due east | 90° | 30.4° | 0.4007 | 8.788 |
| To the 40° orbit (northeast) | 62.6° | 40° | 0.3559 | 8.833 |
| Due north (polar) | 0° | 90.0° | 0 | 9.189 |
| Due west (retrograde) | 270° | 149.6° | −0.4007 | 9.590 |

:::

Launching due east requires the least $\Delta V$, but it reaches only an inclination of 30.4°. The 40° orbit requires slightly more because a smaller component of the site velocity lies along the launch direction, and a polar orbit gains nothing from Earth's rotation. A launch due west works directly against the rotation, adding the same amount to the required $\Delta V$. It needs $9.590 - 8.788 = 0.802$ km/s more than a due-east launch, about twice the rotation gain.

## Summary

:::{important} Summary
- Low Earth orbit lies between about 160 km and 2,000 km altitude, where the circular speed is 6.900 to 7.812 km/s. Reaching orbital speed requires far more energy than climbing to orbital altitude.
- The site's eastward speed, $\omega R_E\cos\phi$, helps by its part along the launch direction, giving $\Delta V_{\text{rot}} = \omega R_E\cos\phi\,\sin\textit{Az}$, which is positive eastward and negative westward.
- From $\cos i = \cos\phi\,\sin\textit{Az}$, the lowest inclination a site reaches directly equals its latitude (due east). Two azimuths reach each higher prograde inclination, and retrograde orbits need a westward launch. Range safety narrows the azimuths further.
- The budget is $\Delta V_{\text{total}} = v_{\text{orbit}} + \Delta V_{\text{losses}} - \Delta V_{\text{rot}}$, with losses of about 1.5 to 2.0 km/s (see [ascent and losses](#p23-losses)).
:::

:::{table} The equations of this page.
:label: tbl-p23-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Velocity to add (vectors; the magnitudes subtract only when they are parallel) | $\Delta\mathbf{V} = \mathbf{v}_{\text{orbit}} - \mathbf{v}_{\text{site}}$ |
| Speed of the site (eastward; 0.4646 km/s at the equator) | $v_{\text{site}} = \omega R_E\cos\phi$ |
| Rotation gain (negative for a westward launch) | $\Delta V_{\text{rot}} = \omega R_E\cos\phi\,\sin\textit{Az}$ |
| Launch geometry (two solutions for $\textit{Az}$; $i \ge \phi$) | $\cos i = \cos\phi\,\sin\textit{Az}$ |
| Rotation gain, direct launch (the same for every site that reaches $i$) | $\Delta V_{\text{rot}} = \omega R_E\cos i$ |
| Orbit speed (radius, not altitude) | $v_{\text{orbit}} = \sqrt{\mu/(R_E + h)}$ |
| Budget (losses about 1.5 to 2.0 km/s, see [ascent and losses](#p23-losses)) | $\Delta V_{\text{total}} = v_{\text{orbit}} + \Delta V_{\text{losses}} - \Delta V_{\text{rot}}$ |

:::

:::{exercise} For discussion
:label: ex-p23-discussion

1. A geostationary satellite must end at $i = 0^\circ$. What extra burn does a launch from Kennedy need that a launch from Kourou barely needs, and where should it be made?
2. Why are most launch sites located on a coast with the sea to the east?
3. Why do launch vehicles not fly straight up to the orbit altitude and then turn horizontal? Which loss would grow, and which would shrink?
4. In the worked example two azimuths reach the 40° orbit. What could make a launch team choose one over the other?
5. A launch to rendezvous with a space station has a window of a few minutes, while a launch into any 40° orbit can be delayed for good weather. Why the difference?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-2-3.html
:label: quiz-2-3
:enumerated: false
:width: 100%

Quiz for Standard 2.3: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 8.
- Craig, A. S., and Ahmad, N., "[Space Launch System Launch Windows and Day of Launch Processes](https://ntrs.nasa.gov/citations/20205004470)," AAS 20-591, AAS/AIAA Astrodynamics Specialist Conference, 2020. NASA Technical Reports Server 20205004470.
- Curtis, H. D., *Orbital Mechanics for Engineering Students*, 3rd ed., Butterworth-Heinemann, 2014. Chapter 11.
- Dresia, K., Jentzsch, S., Waxenegger-Wilfing, G., Dos Santos Hahn, R., Deeken, J., Oschwald, M., and Mota, F., "Multidisciplinary Design Optimization of Reusable Launch Vehicles for Different Propellants and Objectives," *Journal of Spacecraft and Rockets*, Vol. 58, No. 4, 2021, pp. 1017-1029. DOI 10.2514/1.A34944.
- European Space Agency, "[Baikonur Cosmodrome](https://www.esa.int/Science_Exploration/Space_Science/Baikonur_Cosmodrome)."
- European Space Agency, "[Europe's Spaceport in French Guiana](https://www.esa.int/establishment/about-us/directorates/space-transportation/europe-s-spaceport/europe-s-spaceport)."
- Indian Space Research Organisation, "[Launch Services](https://www.isro.gov.in/launchservices.html)."
- Vallado, D. A., *Fundamentals of Astrodynamics and Applications*, 4th ed., Microcosm Press, 2013.
