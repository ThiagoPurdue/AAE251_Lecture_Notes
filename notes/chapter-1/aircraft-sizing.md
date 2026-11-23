---
title: "1.6 Aircraft Sizing"
short_title: 1.6 Aircraft Sizing
---

:::{include} ../_parts/standards/1.6.md
:::

Before anyone draws an aircraft, the designers need one number: how heavy the aircraft will be when it starts its takeoff run. The wing area, the engine thrust, the landing gear, and the cost all scale with that weight. Here we make the first estimate of it from the mission alone, with the method of Raymer (2006, Chapter 3). We split the {term}`takeoff weight` into four parts. The empty weight comes from the history of earlier aircraft, and the fuel comes from the mission, flown one segment at a time. Then we repeat a short calculation until the answer stops changing.

:::{note} What to take from this page
- The takeoff weight is crew plus payload plus fuel plus empty weight. With fuel and empty weight written as fractions of the takeoff weight, one equation gives $W_0$ from the crew and payload.
- The empty-weight fraction comes from a fit to earlier aircraft of the same class, $W_e/W_0 = A\,W_0^{\,C}$. It falls slowly as aircraft grow.
- The fuel fraction comes from the mission: multiply the weight fractions of the segments, then add 6% for reserve and trapped fuel. Cruise uses the Breguet range equation and {term}`loiter` the endurance equation.
- The empty-weight fraction depends on the answer, so the method iterates: guess, compute, repeat until the change is small.
:::

## The takeoff weight and its parts

The method finds one number, the takeoff weight.

:::{prf:definition} Takeoff weight
:label: def-p16-takeoff-weight

The **takeoff weight** $W_0$ is the weight of the aircraft at the start of the takeoff run, loaded with its crew, its payload, and all the fuel for the design mission. It is also called the takeoff gross weight, or the gross weight.
:::

The difficulty is that the weight depends on the design, and the design depends on the weight. A heavier aircraft needs a bigger wing and bigger engines. These add weight, and the extra weight needs more fuel. We break this circle with two facts from experience. Earlier aircraft of the same kind show how much of their weight is structure and systems. The mission shows how much fuel the aircraft burns for each pound of its weight.

### Four parts

Every pound of the takeoff weight belongs to one of four groups:

:::{math}
:label: eq-p16-buildup
\begin{aligned}
W_0 &= W_\text{crew} + W_\text{payload}\\
    &\quad + W_f + W_e
\end{aligned}
:::

- **Crew weight** $W_\text{crew}$: the people who fly and run the aircraft (pilots, flight attendants), with their bags.
- **{term}`Payload`** $W_\text{payload}$: what the mission exists to carry. For an airliner it is the passengers and their bags; for a freighter, the cargo; for a surveillance aircraft, the sensors. The worked example assumes 200 lb for each crew member and 210 lb for each passenger with bags; a real design takes these values from the customer or the operator. Some payload stays aboard (passengers, cargo) and some is dropped on the way (bombs, fire retardant). Here we treat only payload that stays aboard for the whole mission.
- **Fuel weight** $W_f$: all the fuel loaded, including the fuel kept in reserve.
- **{term}`Empty weight`** $W_e$: everything else, the part of the aircraft that stays with it: structure, engines, landing gear, systems, avionics, and furnishings.

Crew and payload are set by the mission and are known from the start. Fuel and empty weight depend on the size of the aircraft, which is not known yet.

{numref}`fig-p16-weight-buildup` shows the split for three Boeing jets loaded to their maximum takeoff weight. About half of each takeoff weight is the empty aircraft. The payload is the smallest part: 0.152 of the takeoff weight of the 757-200 and 0.113 of the 767-300ER. In the 767-300ER every pound of payload needs $400{,}000/45{,}239 = 8.842$ pounds at takeoff. This ratio is why sizing matters: an error in the empty weight or the fuel is multiplied the same way.

:::{figure} figures/p16-weight-buildup.svg
:label: fig-p16-weight-buildup
:alt: Three stacked bars, one per aircraft, each the full takeoff weight as a fraction from 0 to 1, split into operating empty weight (structure, engines, systems, crew) at the bottom, payload in the middle, and fuel on top. Boeing 757-200, 255,500 pounds: 0.501 empty, 0.152 payload, 0.347 fuel. Boeing 767-300ER, 400,000 pounds: 0.495 empty, 0.113 payload, 0.391 fuel. Boeing 747-400, 874,900 pounds: 0.457 empty, 0.0986 payload, 0.444 fuel. About half of each aircraft is empty weight, and the payload is the smallest part.
:width: 75%

Computed from published data for three Boeing jets at maximum takeoff weight, with their design payload and design fuel load. About half of each takeoff weight is the empty aircraft, and the payload is the smallest part. Takeoff weights converted from kilograms and rounded to the nearest 100 lb. Data from Jenkinson et al. (1999, Data A, Table 3).
:::

Airlines and manufacturers publish the **{term}`operating empty weight`**, which adds the crew and the items needed to operate (Boeing 2025, Section 2.1). In our method the crew is counted on its own, so $W_e$ is a little smaller than the operating empty weight of the same aircraft.

:::{warning} Weight, mass, and pounds
Here a pound is a pound of weight (a force), as in Raymer and in the US industry. Every equation divides a weight by a weight. Data in kilograms are masses: a mass of 1 kg weighs 2.205 lb at Earth's surface. Never mix a weight in pounds with a mass in kilograms in one fraction.
:::

### Solving for the takeoff weight

The fuel and empty weights grow with the aircraft, so we write each as a fraction of the takeoff weight, a pure number between 0 and 1. We multiply and divide each by $W_0$ in {eq}`eq-p16-buildup`:

$$
\begin{aligned}
W_0 = {} & W_\text{crew} + W_\text{payload}\\
& + \left(\frac{W_f}{W_0}\right) W_0 + \left(\frac{W_e}{W_0}\right) W_0
\end{aligned}
$$

We move the two terms that hold $W_0$ to the left side:

$$
\begin{gathered}
W_0 - \left(\frac{W_f}{W_0}\right) W_0 - \left(\frac{W_e}{W_0}\right) W_0\\
= W_\text{crew} + W_\text{payload}
\end{gathered}
$$

Then we factor $W_0$ out of the left side:

$$
\begin{gathered}
W_0 \left(1 - \frac{W_f}{W_0} - \frac{W_e}{W_0}\right)\\
= W_\text{crew} + W_\text{payload}
\end{gathered}
$$

and divide both sides by the bracket:

:::{math}
:label: eq-p16-w0
W_0 = \frac{W_\text{crew} + W_\text{payload}}{1 - \dfrac{W_f}{W_0} - \dfrac{W_e}{W_0}}
:::

The numerator is known from the mission. The denominator is the fraction of the takeoff weight left for crew and payload once fuel and structure have taken their share. When that fraction is small, the takeoff weight is large. When it reaches zero or below, no aircraft of this kind can fly the mission, and we say the mission does not close. The next two sections find the two fractions.

## The empty-weight fraction from history

We cannot compute the {term}`empty-weight fraction` $W_e/W_0$ before the aircraft is designed, so the first estimate comes from aircraft already built. Later in the design, estimates of the weight of each part (wing, fuselage, tails, landing gear, engines) replace it, and at the end the weights of the parts as built.

Raymer plotted $W_e/W_0$ against $W_0$ for many aircraft, sorted by class, and fitted a curve to each class:

:::{math}
:label: eq-p16-empty
\frac{W_e}{W_0} = A\,W_0^{\,C}\,K_\text{vs}
:::

The constants $A$ and $C$ of each class are in {numref}`tbl-p16-raymer`. $K_\text{vs}$ is 1.04 for a variable-sweep wing (one that swings back in flight, as on the F-14) and 1.00 for every other aircraft, so it drops out of most problems. The fit is written with $W_0$ in pounds. Raymer also gives a value of $A$ for $W_0$ in kilograms, with the same $C$.

:::{table} Empty-weight fraction fits, $W_e/W_0 = A\,W_0^{\,C}$ with $W_0$ in pounds (Raymer 2006, Table 3.1).
:label: tbl-p16-raymer
:align: center

| Class | Constant $A$ | Exponent $C$ |
| --- | ---: | ---: |
| Sailplane, unpowered | 0.86 | −0.05 |
| Sailplane, powered | 0.91 | −0.05 |
| Homebuilt, metal or wood | 1.19 | −0.09 |
| Homebuilt, composite | 1.15 | −0.09 |
| General aviation, single engine | 2.36 | −0.18 |
| General aviation, twin engine | 1.51 | −0.10 |
| Agricultural aircraft | 0.74 | −0.03 |
| Twin turboprop | 0.96 | −0.05 |
| Flying boat | 1.09 | −0.05 |
| Jet trainer | 1.59 | −0.10 |
| Jet fighter | 2.34 | −0.13 |
| Military cargo or bomber | 0.93 | −0.07 |
| Jet transport | 1.02 | −0.06 |

:::

:::{warning} Two letters that mean other things
In {eq}`eq-p16-empty`, $A$ and $C$ are fit constants. $C$ is a negative exponent with no unit. The same letter $C$ is the specific fuel consumption in the range and endurance equations below, in 1/h, and $A$ is an area elsewhere in the chapter. On the same page, $R$ is the range, not the gas constant of the standard atmosphere. Read each symbol from its equation.
:::

{numref}`fig-p16-empty-weight-trends` draws five of the fits over the weights their data cover. For the 767-300ER of {numref}`fig-p16-weight-buildup` the jet-transport fit (Raymer's name for airliners) gives

$$
\begin{aligned}
\frac{W_e}{W_0} &= 1.02\,{(400{,}000)}^{-0.06}\\
&= 0.4704
\end{aligned}
$$

against a published 0.495 for its operating empty weight. The fit is an average through scattered data, and the published value includes the crew and operating items.

:::{figure} figures/p16-empty-weight-trends.svg
:label: fig-p16-empty-weight-trends
:alt: Plot of empty-weight fraction, 0.30 to 0.75, against takeoff weight on a log scale from 100 to over 2 million pounds. Five straight sloping lines, each falling to the right and named at one end: unpowered sailplanes near 0.6 to 0.65, twin turboprops near 0.55 to 0.62, jet fighters falling steeply from 0.64 to about 0.51, jet transports from 0.56 to 0.45, and military cargo or bomber aircraft from 0.45 to 0.35. Three open squares for the Boeing 757, 767, and 747 lie just above the jet-transport line, and a dot on that line marks the worked example at 281,537 pounds and 0.480.
:width: 80%

Computed from Raymer's fits, each drawn over the range of takeoff weights of its class; squares, operating empty weight over takeoff weight of the three jets of {numref}`fig-p16-weight-buildup`. Within every class the empty-weight fraction falls as the aircraft grows, and classes differ by what their job asks of the structure. Fits from Raymer (2006, Table 3.1), ranges from Raymer (2006, Figure 3.1).
:::

Notice two things in the figure:

- **The fraction falls as the aircraft grows.** Every $C$ in {numref}`tbl-p16-raymer` is negative. Some items do not grow in proportion to the aircraft: a cockpit with its instruments and avionics, or the minimum thickness a skin can be made. In a larger aircraft they are a smaller share of the total.
- **Classes differ.** A fighter carries large engines and a structure built for hard maneuvers, so its line sits high. A long-range cargo aircraft or bomber spends most of its takeoff weight on fuel and payload, so its line sits low.

History is a good guide only for aircraft like the ones it was made from. A new structural material (composites in place of aluminum) or a new configuration (a much longer, thinner wing than any aircraft in the data) can put a design well off its class line. Use the fit for the first estimate, and know which way your design differs from its class.

(p16-weight-fractions)=
## The fuel fraction from the mission

One observation makes the fuel simple to estimate: the fuel an aircraft burns is roughly proportional to its weight. Twice the weight needs twice the lift, which costs about twice the drag, twice the thrust, and twice the fuel. So the {term}`fuel fraction` $W_f/W_0$ does not depend on the size of the aircraft. It depends on how well the aircraft turns fuel into distance or time (its engines and its aerodynamics) and on what the mission asks of it.

### Segments and weight fractions

The mission itself comes from the [requirements](#p11-requirements): the customer states the range, the payload, and the reserves. We draw the mission as a {term}`mission profile <Mission profile>` (introduced with [vehicle anatomy](#p13-mission-profile)) and divide it into segments: warm-up and takeoff, climb, cruise, loiter (flying in a holding pattern while waiting to land, which airlines call a hold), and landing. We number the end of each segment, starting with 0 for the start of the takeoff run, as in {numref}`fig-p16-mission-profile`. $W_i$ is the weight at the end of segment $i$, so $W_0$ is the takeoff weight and $W_5$ the weight after landing.

:::{figure} figures/p16-mission-profile.svg
:label: fig-p16-mission-profile
:alt: Mission profile, altitude against distance, not to scale, with the segment ends numbered 0 to 5 and arrowheads showing the direction of flight; each segment is labeled with its weight fraction. Warm-up and takeoff, a level segment on the ground line from 0 to 1, W1 over W0 equals 0.970. Climb from 1 to 2, W2 over W1 equals 0.985. Cruise, level, W3 over W2 from the range equation, then a thinner descent with no number at its top, labeled descent counted in the cruise, down to point 3. Loiter, level at a lower altitude from 3 to 4, W4 over W3 from the endurance equation. A thinner descent to the ground, labeled descent counted in the landing, then landing, a level segment on the ground line to point 5, W5 over W4 equals 0.995.
:width: 85%

Schematic, not to scale, of a simple cruise mission cut into five segments. Each segment has its own weight fraction, taken from history (warm-up and takeoff, climb, and landing) or computed (cruise, loiter). The descents carry no fraction of their own: the first is counted in the cruise and the second in the landing, so they are drawn thinner and the top of the first has no number. After Raymer (2006, Figure 3.2).
:::

:::{prf:definition} Segment weight fraction
:label: def-p16-weight-fraction

The **{term}`weight fraction`** of segment $i$ is $W_i/W_{i-1}$, the weight at the end of the segment divided by the weight at its start. It is less than 1 by the fraction of the weight burned as fuel in that segment.
:::

The weight at the end of one segment is the weight at the start of the next. So the fractions chain together, and every intermediate weight cancels:

:::{math}
:label: eq-p16-product
\frac{W_5}{W_0} = \frac{W_1}{W_0}\cdot\frac{W_2}{W_1}\cdot\frac{W_3}{W_2}\cdot\frac{W_4}{W_3}\cdot\frac{W_5}{W_4}
:::

For the short segments at the start and end, the fuel burned changes little from one aircraft to the next, so Raymer gives historical values ({numref}`tbl-p16-segments`). Cruise and loiter burn most of the fuel, and we compute them.

:::{table} Historical segment weight fractions (Raymer 2006, Chapter 3).
:label: tbl-p16-segments
:align: center

| Segment | Weight fraction $W_i/W_{i-1}$ |
| --- | ---: |
| Warm-up and takeoff | 0.970 |
| Climb | 0.985 |
| Landing | 0.995 |

:::

### Where the range and endurance equations come from

Two quantities describe how well the aircraft turns fuel into flight:

:::{prf:definition} Specific fuel consumption
:label: def-p16-sfc

The **{term}`specific fuel consumption`** $C$ of a jet engine is the weight of fuel it burns per hour for each pound of thrust it makes: pounds of fuel per hour per pound of thrust. The pounds cancel, so $C$ has the unit 1/h.
:::

The **{term}`lift-to-drag ratio`** $L/D$ is the lift of the aircraft divided by its drag, a measure of its aerodynamic efficiency ([Chapter 3 of these notes computes it](#p33-minimum-drag)).

In steady, level flight the lift balances the weight and the thrust balances the drag, $L = W$ and $T = D$ ({numref}`fig-p16-cruise-forces`).

:::{figure} figures/p16-cruise-forces.svg
:label: fig-p16-cruise-forces
:alt: Side view of a twin-jet airliner in cruise, flying to the left, with its center of gravity marked. Four force arrows act on lines through the center of gravity: lift up and weight down, drawn the same length; thrust forward and drag aft, drawn the same length. A note reads: steady level flight, L equals W, T equals D equals W divided by L over D. A thin arrow ahead of the airliner shows its velocity V.
:width: 90%

Schematic, lengths not to scale (at $L/D = 17$ the drag arrow would be one seventeenth of the lift arrow). In steady level cruise the four forces balance in pairs: lift equals weight and thrust equals drag, so the thrust needed is the weight divided by the lift-to-drag ratio. Each force is drawn on a line through the center of gravity. Outline of a Boeing 737-800, gear up.
:::

So the thrust we need is

$$
T = D = \frac{D}{L}\,L = \frac{W}{L/D}
$$

The engines burn fuel at the rate $C\,T$, and that rate is how fast the aircraft's weight falls:

$$
\frac{dW}{dt} = -C\,T = -\frac{C\,W}{L/D}
$$

We separate the variables, with the weight on the left and the time on the right:

$$
\frac{dW}{W} = -\frac{C}{L/D}\,dt
$$

**Loiter.** We integrate over a loiter of duration $E$, the {term}`endurance`, from the weight $W_{i-1}$ at its start to $W_i$ at its end, holding $C$ and $L/D$ constant:

$$
\int_{W_{i-1}}^{W_i}\frac{dW}{W} = \ln\frac{W_i}{W_{i-1}} = -\frac{C\,E}{L/D}
$$

Taking the exponential of both sides gives the endurance equation:

:::{math}
:label: eq-p16-endurance
\frac{W_i}{W_{i-1}} = \exp\left[-\frac{E\,C}{L/D}\right]
:::

**Cruise.** In cruise the aircraft covers distance $x$ at constant speed $V$, so $dt = dx/V$ and

$$
\frac{dW}{W} = -\frac{C}{V\,(L/D)}\,dx
$$

Integrating from $x = 0$ to the range $x = R$, with $V$ also constant, gives the {term}`Breguet range equation`:

:::{math}
:label: eq-p16-range
\frac{W_i}{W_{i-1}} = \exp\left[-\frac{R\,C}{V\,(L/D)}\right]
:::

Both equations assume that $C$, $L/D$, and, for cruise, $V$ stay constant through the segment, and that the flight is steady and level. We treat the range and endurance equations in full, for propeller aircraft too, in Chapter 5. A propeller engine is rated by fuel per unit of power instead of per unit of thrust, so its range equation also carries the propeller efficiency (Scholz n.d., Equation 5.54).

:::{warning} Units of the exponent
The exponent must have no unit. With $C$ in 1/h, use $E$ in hours, $R$ in {term}`nautical miles <nautical mile>`, and $V$ in knots (nautical miles per hour). Then $R\,C/V$ is nmi times 1/h divided by nmi/h, which cancels. A loiter of 30 minutes is $E = 0.5$ h, not 30. If you prefer feet and seconds, use $R$ in ft, $V$ in ft/s, and $C$ in 1/s ($C$ in 1/h divided by 3,600), with 1 nmi = 6,076.1 ft and 1 kt = 1.6878 ft/s.
:::

For a first estimate, you can take typical values from {numref}`tbl-p16-sfc` and {numref}`tbl-p16-ld`. A jet loiters near its maximum $L/D$, because {eq}`eq-p16-endurance` gives the longest loiter for the highest $L/D$. It cruises faster than that, because {eq}`eq-p16-range` depends on $V$ times $L/D$. Its cruise $L/D$ is then a little below the maximum (Scholz n.d., Section 5.7).

:::{table} Typical specific fuel consumption of jet engines, $C$ in 1/h (Scholz n.d., Table 5.7, after Raymer).
:label: tbl-p16-sfc
:align: center

| Engine | Cruise | Loiter |
| --- | ---: | ---: |
| Turbojet | 0.9 | 0.8 |
| Turbofan, low bypass ratio | 0.8 | 0.7 |
| Turbofan, high bypass ratio | 0.5 | 0.4 |

:::

A turbofan sends part of its air around the core of the engine instead of through it; the bypass ratio is the air that goes around divided by the air that goes through. A turbojet sends all its air through the core. Airliners use high-bypass turbofans, which burn the least fuel per pound of thrust; fighters use low-bypass ones.

:::{table} Typical maximum lift-to-drag ratios, rounded (Nicolai and Carichner 2010, Figure 5.3; jet airliners also Scholz n.d., Figure 5.7).
:label: tbl-p16-ld
:align: center

| Aircraft | Maximum lift-to-drag ratio |
| --- | ---: |
| Subsonic aircraft with a wing of aspect ratio 3 (a fighter) | 11 |
| Subsonic aircraft with a wing of aspect ratio 6 | 16 |
| Jet airliners (aspect ratio about 7 to 10) | 15 to 21 |
| Subsonic aircraft with a wing of aspect ratio 10 | 22 |
| Supersonic cruise aircraft at two to three times the speed of sound | 6 to 8 |

:::

The {term}`aspect ratio <Aspect ratio>` in {numref}`tbl-p16-ld` is the wing span squared over the wing area, defined under [wing geometry](#p13-wing-geometry). A long, slender wing has a high aspect ratio and a high $L/D$.

### Reserve and trapped fuel

The product {eq}`eq-p16-product` gives $W_5/W_0$, so the fuel burned on the mission is $1 - W_5/W_0$ of the takeoff weight. An aircraft also carries fuel it does not plan to burn: {term}`reserve fuel` for a diversion or a delay, and trapped fuel that stays in the tanks and lines and cannot be used. Raymer allows 6% for both together:

:::{math}
:label: eq-p16-fuel
\frac{W_f}{W_0} = 1.06\left(1 - \frac{W_x}{W_0}\right)
:::

where $W_x$ is the weight at the end of the last segment ($W_5$ in {numref}`fig-p16-mission-profile`).

:::{tip} Method: the fuel fraction
1. Draw the mission and number the end of each segment, starting with 0.
2. Take the warm-up and takeoff, climb, and landing fractions from {numref}`tbl-p16-segments`.
3. Compute each cruise fraction with {eq}`eq-p16-range` and each loiter fraction with {eq}`eq-p16-endurance`, with the $C$ and $L/D$ of that segment and units that cancel.
4. Multiply all the segment fractions to get $W_x/W_0$.
5. Compute $W_f/W_0 = 1.06\,(1 - W_x/W_0)$.
:::

:::{warning} Common slips in the fuel fraction
- Adding the segment fractions, or adding the fuel burned in each segment as a fraction of $W_0$. The fractions multiply, because each is relative to the weight at the start of its own segment.
- Using the cruise $L/D$ or the cruise $C$ in the loiter. Each segment uses its own values.
- Forgetting the 6%, or adding 0.06 instead of multiplying by 1.06.
:::

(p16-iteration)=
## The sizing iteration

Now we know the fuel fraction, but we still cannot solve {eq}`eq-p16-w0` in one step. The empty-weight fraction depends on $W_0$ through {eq}`eq-p16-empty`, so the takeoff weight appears on both sides. We get around this by guessing $W_0$, using the guess to find $W_e/W_0$, computing a new $W_0$, and repeating with the new value until it stops changing. {numref}`fig-p16-sizing-loop` shows the steps.

:::{figure} figures/p16-sizing-loop.svg
:label: fig-p16-sizing-loop
:alt: Flow chart of six numbered steps from top to bottom. Step 1, set the mission: crew, payload, and the segments. Step 2, find the fuel fraction from the segments, once. Step 3, guess the takeoff weight, or after the first pass take the new one. Step 4, find the empty-weight fraction from the historical fit. Step 5, compute a new takeoff weight from the build-up equation. Step 6, a decision: did the takeoff weight change by less than 0.1 percent? If no, an arrow returns to step 3; if yes, stop: that is the takeoff weight.
:width: 85%

Schematic of the sizing loop, with its steps numbered as in the method below and step 6 the test. The fuel fraction is found once, before the loop, because it does not depend on the size of the aircraft; only the empty-weight fraction is recomputed on each pass.
:::

:::{tip} Method: sizing an aircraft
1. Set the mission: crew and payload weights, and the segments with their speeds, distances, times, $C$, and $L/D$.
2. Find the fuel fraction $W_f/W_0$ with the method above. It is the same on every pass.
3. Guess $W_0$. A good first guess puts $W_e/W_0 = 0.5$ (about the share of the jets in {numref}`fig-p16-weight-buildup`) into {eq}`eq-p16-w0`. On later passes, use the $W_0$ from step 5.
4. Compute $W_e/W_0 = A\,W_0^{\,C}$ at that $W_0$, with $A$ and $C$ of the class from {numref}`tbl-p16-raymer`.
5. Compute a new $W_0$ from {eq}`eq-p16-w0`.
6. If the new $W_0$ differs from the guess by less than 0.1%, stop: that is the takeoff weight. Otherwise return to step 3.
:::

The tolerance of 0.1% is a choice. The inputs (the historical fits, the typical $C$ and $L/D$) are not known better than a few percent, so iterating further only refines the arithmetic. A computer can iterate to the pound in a moment.

## Worked example: a long-range airliner

A twin-jet airliner must carry 250 passengers 5,000 nmi. Find its takeoff weight. The mission is the simple cruise of {numref}`fig-p16-mission-profile`, with the data of {numref}`tbl-p16-givens`. The engines are high-bypass turbofans, so $C$ is the typical value of {numref}`tbl-p16-sfc`. The $L/D$ values are those of a jet airliner from {numref}`tbl-p16-ld`.

:::{table} Data of the worked example.
:label: tbl-p16-givens
:align: center

| Item | Value |
| --- | --- |
| Passengers | 250, at 210 lb each with bags |
| Crew | 2 pilots and 8 flight attendants, at 200 lb each |
| Cruise | $R = 5{,}000$ nmi, $V = 480$ kt, $C = 0.5$ 1/h, $L/D = 17$ |
| Loiter | $E = 0.5$ h, $C = 0.4$ 1/h, $L/D = 19$ |
| Empty-weight fit (jet transport) | $A = 1.02$, $C = -0.06$ |

:::

We follow the steps of the method above.

1. **Crew and payload.** $W_\text{payload} = 250 \times 210 = 52{,}500$ lb and $W_\text{crew} = 10 \times 200 = 2{,}000$ lb, so $W_\text{crew} + W_\text{payload} = 54{,}500$ lb.
2. **Fuel fraction.** Warm-up and takeoff, climb, and landing come from {numref}`tbl-p16-segments`: 0.970, 0.985, and 0.995. The cruise exponent, with every unit shown, is
   $$
   \begin{aligned}
   &\frac{R\,C}{V\,(L/D)}\\
   &\;\;\;= \frac{(5{,}000\ \text{nmi})(0.5\ \text{1/h})}{(480\ \text{nmi/h})(17)}\\
   &\;\;\;= \frac{5{,}000 \times 0.5}{480 \times 17}\\
   &\;\;\;= 0.30637
   \end{aligned}
   $$
   so the cruise fraction, from {eq}`eq-p16-range`, is
   $$
   \begin{aligned}
   \frac{W_3}{W_2} &= \exp(-0.30637)\\
   &= 0.73611
   \end{aligned}
   $$
   The loiter exponent is $(0.5\ \text{h})(0.4\ \text{1/h})/19$:
   $$
   \frac{0.5 \times 0.4}{19} = 0.010526
   $$
   and from {eq}`eq-p16-endurance`
   $$
   \begin{aligned}
   \frac{W_4}{W_3} &= \exp(-0.010526)\\
   &= 0.98953
   \end{aligned}
   $$
   We multiply the five fractions, {eq}`eq-p16-product`. Warm-up and takeoff with the climb give $0.970 \times 0.985 = 0.95545$, the cruise with the loiter $0.73611 \times 0.98953 = 0.72840$, and
   $$
   \begin{aligned}
   \frac{W_5}{W_0} &= 0.95545 \times 0.72840 \times 0.995\\
   &= 0.69247
   \end{aligned}
   $$
   and add the reserve, {eq}`eq-p16-fuel`:
   $$
   \begin{aligned}
   \frac{W_f}{W_0} &= 1.06\,(1 - 0.69247)\\
   &= 0.32598
   \end{aligned}
   $$
   {numref}`fig-p16-weight-staircase` follows the weight through the mission. The cruise alone burns more than a quarter of the takeoff weight.

:::{figure} figures/p16-weight-staircase.svg
:label: fig-p16-weight-staircase
:alt: Plot of the weight fraction at the end of each segment, from 0 to 5. The weight starts at 1, falls to 0.97000 after takeoff and 0.95545 after the climb, drops steeply to 0.70332 over the cruise, then to 0.69595 after the loiter and 0.69247 after landing. Segment multipliers are listed along the bottom: 0.970, 0.985, 0.73611, 0.98953, and 0.995. On the right, one double arrow spans the fuel burned, 0.30753 of the takeoff weight, and a second, slightly longer one spans the fuel loaded, 0.32598, with 6% added; the short gap between their lower ends is the reserve and trapped fuel.
:width: 85%

Computed for the worked example: the weight at the end of each segment as a fraction of the takeoff weight. Each segment multiplies the weight by its fraction, and the cruise burns most of the fuel. The fuel loaded is the fuel burned, 0.30753, plus 6% for reserve and trapped fuel.
:::

3. **First guess.** With $W_e/W_0 = 0.5$ in {eq}`eq-p16-w0`:
   $$
   \begin{aligned}
   W_0 &= \frac{54{,}500}{1 - 0.32598 - 0.5}\\
   &= 313{,}182\ \text{lb}
   \end{aligned}
   $$
   We start from the round number $W_0 = 313{,}000$ lb.
4. **Empty-weight fraction** at the guess:
   $$
   \begin{aligned}
   \frac{W_e}{W_0} &= 1.02\,{(313{,}000)}^{-0.06}\\
   &= 0.47738
   \end{aligned}
   $$
5. **New takeoff weight:**
   $$
   \begin{aligned}
   &W_0\\
   &= \frac{54{,}500}{1 - 0.32598 - 0.47738}\\
   &= 277{,}156\ \text{lb}
   \end{aligned}
   $$
6. **Test.** The new value differs from the guess by 11.5%, so it becomes the next guess, and steps 4 to 6 repeat. {numref}`tbl-p16-iterations` lists every pass. The fourth changes $W_0$ by only 0.0412%, below the 0.1% tolerance.

:::{table} The iteration of the worked example ($W_\text{crew} + W_\text{payload} = 54{,}500$ lb, $W_f/W_0 = 0.32598$).
:label: tbl-p16-iterations
:align: center

| Pass | Guessed takeoff weight $W_0$ (lb) | Empty-weight fraction $W_e/W_0$ | New takeoff weight $W_0$ (lb) | Change |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 313,000 | 0.47738 | 277,156 | −11.5% |
| 2 | 277,156 | 0.48088 | 282,179 | +1.81% |
| 3 | 282,179 | 0.48036 | 281,421 | −0.269% |
| 4 | 281,421 | 0.48044 | 281,537 | +0.0412% |

:::

**Result.** The takeoff weight is $W_0 = 281{,}537$ lb. At this weight $W_e/W_0 = 0.48043$, so the parts are

$$
\begin{aligned}
W_e &= 0.48043 \times 281{,}537\\
&= 135{,}259\ \text{lb}\\
W_f &= 0.32598 \times 281{,}537\\
&= 91{,}775\ \text{lb}
\end{aligned}
$$

**Check.** The parts add back to the takeoff weight: $54{,}500 + 91{,}775 + 135{,}259 = 281{,}534$ lb, 3 lb short of $W_0$ because we rounded the fractions to five decimals. If we carry the iteration on until the weight stops changing, it settles at 281,518 lb, 19 lb (0.007%) below the value accepted here. Stopping at 0.1% is well inside the accuracy of the inputs. The empty-weight fraction, 0.480, lies among the 0.457 to 0.501 of the three Boeing jets in {numref}`fig-p16-weight-buildup`. The fuel fraction, 0.326, is a little below their 0.347 to 0.444. The aircraft weighs 5.166 times its crew and payload.

:::{figure} figures/p16-iteration.svg
:label: fig-p16-iteration
:alt: Plot of takeoff weight in thousands of pounds against iteration. The first guess, 313,000 pounds, is an open circle. Pass 1 drops to 277,156 pounds (minus 11.5%), pass 2 rises to 282,179 (plus 1.81%), pass 3 falls to 281,421 (minus 0.269%), and pass 4 rises to 281,537 (plus 0.0412%), on a dashed line marking the accepted value, 281,537 pounds. Each value lands on the other side of that line and much closer to it.
:width: 80%

Computed for the worked example: the takeoff weight after each pass of the iteration. Each new value overshoots the accepted value on the other side, by about 15% of the previous miss, so the iteration settles in four passes.
:::

## Why the iteration converges

You do not need this section to use the method. It explains a pattern in the worked example.

{numref}`fig-p16-iteration` shows the pattern: each change has the opposite sign of the one before and is about 0.15 times as large. The changes of {numref}`tbl-p16-iterations` give $5{,}023/35{,}844 = 0.1401$, then $758/5{,}023 = 0.1509$, then $116/758 = 0.1530$.

The reason is in {eq}`eq-p16-w0`. A guess that is too high gives an empty-weight fraction that is a little too low, because the exponent $C$ is negative. The denominator is then a little too large, and the new $W_0$ comes out too low: the error changes sign. It also shrinks, because the fraction changes slowly with $W_0$.

Suppose we plot the result of one pass, the new $W_0$, against the guess. The answer $W^*$ is where this curve meets the 45° line, on which the new value equals the guess. Near $W^*$ a smooth curve is close to its tangent line. So a guess that misses the answer by a small error $e$ gives a new value that misses it by about the slope of the curve times $e$. Here the curve slopes gently downward, $\text{slope} \approx -0.15$, much flatter than the 45° line. Each pass flips the error to the other side and keeps about 0.15 of it, the factor we read from the passes above.

The numbers of the example show where the 0.15 comes from. Suppose we raise the guess by 1%. The empty-weight fraction, 0.48043, is multiplied by ${1.01}^{-0.06} = 0.99940$ and falls by 0.00029. The denominator of the sizing equation, $1 - 0.32598 - 0.48043 = 0.19359$, rises by the same 0.00029, which is 0.15% of it, so the new $W_0$ falls by 0.15%. A 1% error in the guess has become an error of 0.15% on the other side.

The iteration converges whenever the size of that slope is below 1. Here the slope is small because the exponent is small, which keeps the 0.00029 small. The exponents in {numref}`tbl-p16-raymer` are all small, 0.03 to 0.18 in size. The slope grows when the denominator of {eq}`eq-p16-w0` is small, that is, when the mission barely closes. The same change is then a larger share of the denominator, and the iteration needs many more passes.

## What the answer is sensitive to

A sizing estimate is most useful for what it shows about the design: which inputs drive the weight. {numref}`fig-p16-range-sensitivity` repeats the worked example for design ranges from 500 to 9,000 nmi and three cruise $L/D$ values. Iterated until it stops changing, the takeoff weight is 232,481 lb for 4,000 nmi, 281,518 lb for 5,000 nmi, and 349,075 lb for 6,000 nmi. Each extra 1,000 nmi costs more than the one before. The extra fuel needs structure, the structure needs more fuel, and the cruise fraction falls exponentially with range.

:::{figure} figures/p16-range-sensitivity.svg
:label: fig-p16-range-sensitivity
:alt: Plot of takeoff weight in thousands of pounds against design range from 0 to 10,000 nautical miles, for cruise lift-to-drag ratios of 15 (solid), 17 (dashed), and 19 (dotted). All three start near 135,000 pounds at 500 nautical miles and curve upward ever more steeply; the L/D 15 curve leaves the plot near 890,000 pounds at about 8,050 nautical miles, while the L/D 19 curve reaches only 600,000 pounds at 9,000. A dot marks the worked example, 5,000 nautical miles and 281,518 pounds, on the L/D 17 curve.
:width: 80%

Computed with the worked example's data, iterated until the weight stops changing, with only the design range and the cruise lift-to-drag ratio changed. The takeoff weight grows faster than the range, and a better $L/D$ pushes the steep part of the curve to longer ranges. The $L/D = 15$ curve is cut where it leaves the plot, at about 8,050 nmi.
:::

In {numref}`fig-p16-sensitivity-bars` we make each input 10% worse, one at a time.

:::{figure} figures/p16-sensitivity-bars.svg
:label: fig-p16-sensitivity-bars
:alt: Horizontal bar chart of the increase of takeoff weight, in percent, when one input of the worked example is made 10% worse. Empty-weight fraction 10% higher: plus 26.6%. Cruise lift-to-drag ratio 10% lower: plus 12.3%. Cruise fuel consumption C 10% higher: plus 11.0%. Cruise range 10% longer: plus 11.0%. Payload 10% heavier: plus 8.34%.
:width: 90%

Computed with the worked example's data, iterated until the weight stops changing, one input changed at a time. The empty-weight fraction matters most; the cruise range and the cruise fuel consumption act exactly alike, because they enter the cruise fraction only through the product $R\,C$.
:::

Three results follow:

- **The empty weight matters most.** A structure 10% heavier for its size (the constant $A$ times 1.1) raises $W_0$ by 26.6%. This is why designers track the weight of every part, and why a lighter material changes a whole design.
- **Cruise range, $C$, and $L/D$ act together.** In the cruise fraction they appear only as $R\,C/(V\,L/D)$, so 10% more range costs exactly what 10% more cruise fuel consumption costs, 11.0%. A 10% lower cruise $L/D$ costs a little more, 12.3%, because dividing by 0.9 raises the exponent by 11.1%.
- **Payload grows the aircraft by several times its own weight.** Adding 1,000 lb of payload adds 4,492 lb to $W_0$.

## Summary

:::{important} Summary
- The takeoff weight is crew plus payload plus fuel plus empty weight. Crew and payload divided by one minus the fuel fraction minus the empty-weight fraction give $W_0$, {eq}`eq-p16-w0`.
- The empty-weight fraction comes from a fit to earlier aircraft of the class, $W_e/W_0 = A\,W_0^{\,C}$, with a small negative $C$: it falls slowly as the aircraft grows.
- The fuel fraction is the product of the segment weight fractions, with the range equation for cruise and the endurance equation for loiter, plus 6%. It does not depend on the size of the aircraft.
- Because $W_e/W_0$ depends on $W_0$, the method iterates until the change is below about 0.1%. Each pass leaves about 0.15 of the error in the worked example.
:::

:::{table} The equations of this page.
:label: tbl-p16-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Weight build-up | $W_0 = W_\text{crew} + W_\text{payload} + W_f + W_e$ |
| Takeoff weight | $W_0 = (W_\text{crew} + W_\text{payload})/(1 - W_f/W_0 - W_e/W_0)$ |
| Empty-weight fraction (fit constants $A$, $C$ of the class; $W_0$ in lb) | $W_e/W_0 = A\,W_0^{\,C}$ |
| Mission weight fraction (product of the segments) | $W_x/W_0 = (W_1/W_0)(W_2/W_1)\cdots(W_x/W_{x-1})$ |
| Cruise ($R$ in nmi, $V$ in kt, $C$ in 1/h) | $W_i/W_{i-1} = \exp[-R\,C/(V\,(L/D))]$ |
| Loiter ($E$ in h, $C$ in 1/h) | $W_i/W_{i-1} = \exp[-E\,C/(L/D)]$ |
| Fuel fraction (6% reserve and trapped fuel) | $W_f/W_0 = 1.06\,(1 - W_x/W_0)$ |

:::

:::{exercise} For discussion
:label: ex-p16-discussion

1. The fuel fraction does not depend on the size of the aircraft, but the fuel weight does. Explain the difference in your own words.
2. A firefighting aircraft drops its load of water halfway through its mission. Why does the method of this page overestimate its fuel, and how would you change the segments to handle the drop?
3. A new aircraft uses a composite structure throughout, but its class line in Raymer's data comes from aluminum aircraft. Which way would you expect the true empty-weight fraction to fall, and how would you adjust the estimate?
4. Two inputs, the cruise range and the cruise specific fuel consumption, have exactly the same effect on the takeoff weight. Which of them can the designers control, and which comes from the customer?
5. A sizing iteration for another jet transport needs many more passes than the worked example. Using {eq}`eq-p16-w0`, what does that suggest about its mission?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-1-6.html
:label: quiz-1-6
:enumerated: false
:width: 100%

Quiz for Standard 1.6: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Boeing Commercial Airplanes (Boeing), *787 Airplane Characteristics for Airport Planning*, D6-58333 Rev Q, 2025.
- Jenkinson, L. R., Simpkin, P., and Rhodes, D., *Civil Jet Aircraft Design*, Arnold and Butterworth-Heinemann, 1999. Companion web site, Data A, Aircraft Data File, Boeing aircraft: [Table 2](https://booksite.elsevier.com/9780340741528/appendices/data-a/table-2/table.htm) and [Table 3](https://booksite.elsevier.com/9780340741528/appendices/data-a/table-3/table.htm).
- Nicolai, L. M., and Carichner, G. E., *Fundamentals of Aircraft and Airship Design*, Vol. 1, AIAA, 2010. Chapter 5, Figure 5.3.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 4th ed., AIAA, 2006.
- Scholz, D., "[Aircraft Design, Chapter 5: Preliminary Sizing](https://www.fzt.haw-hamburg.de/pers/Scholz/HOOU/AircraftDesign_5_PreliminarySizing.pdf)," lecture notes, Hamburg University of Applied Sciences, n.d. Sections 5.7 and 5.9, Tables 5.7 and 5.8, Figure 5.7, Equation 5.54.

