---
title: "3.3 Drag Polar"
short_title: 3.3 Drag Polar
---

:::{include} ../_parts/standards/3.3.md
:::

In steady level flight, an aircraft's engines must generate enough thrust to balance aerodynamic drag. On this page we separate subsonic drag into two physical parts: the drag caused by moving a vehicle through the air, and the induced drag caused by generating lift. We then combine both into one relation, the {term}`drag polar`, which gives the {term}`drag coefficient` at every {term}`lift coefficient`. Applying the polar to steady level flight produces the curve of total drag versus airspeed, which reaches a clear minimum.

:::{note} What to take from this page
- Subsonic drag has two parts. {term}`Parasite drag` (skin friction, pressure drag, interference) comes from moving through the air; induced drag comes from making lift.
- The drag polar $C_D = C_{D,0} + K C_L^2$, with $K = 1/(\pi e\,\textit{AR})$, holds for one configuration. Each point on it is one angle of attack.
- In steady level flight $D = qSC_{D,0} + KW^2/(qS)$: the parasite part grows with $V^2$, the induced part falls with $1/V^2$, and the total has a minimum.
- Minimum drag and the maximum lift-to-drag ratio come at $C_L^* = \sqrt{C_{D,0}/K}$, where the induced drag equals the parasite drag, $C_D = 2C_{D,0}$, and $(L/D)_{\max} = 1/(2\sqrt{K C_{D,0}})$.
:::

(p33-drag-kinds)=
## Two kinds of drag

Drag is the part of the aerodynamic force that acts along the free stream, against the motion ([page 1.5](../chapter-1/bernoulli-and-pitot-static.md) splits the total force into lift and drag). At subsonic speeds it comes from two sources (FAA 2023, Chapter 5):

1. **Moving through the air.** Any component moving through the air experiences drag even when it produces no lift, such as a strut, a landing-gear leg, or a fuselage. This is {term}`parasite drag`, defined as the drag not directly associated with lift generation.
2. **Generating lift.** A finite wing producing lift sheds wingtip vortices that induce downwash and tilt the local lift vector backward. That rearward component is the {term}`induced drag` of [page 3.2](#p32-induced-drag), which vanishes at zero lift.

Parasite drag has three parts, drawn in {numref}`fig-p33-parasite-drag-kinds` (FAA 2023, Chapter 5):

- **{term}`Skin friction drag`.** Air directly in contact with a surface moves with the surface under the {term}`no-slip condition`, forming a thin {term}`boundary layer` ([page 3.1](wind-tunnels.md)) that shears between the surface and the free stream. The resulting {term}`shear stress` pulls every square meter of exposed surface downstream. Skin friction grows with wetted area (the total surface area in contact with the air) and surface roughness, which is why aircraft use flush rivets and smooth finishes.
- **{term}`Pressure drag`**, also called form drag. Behind a blunt body, the boundary layer separates from the surface and leaves a wide, swirling wake of low pressure. Combined with the high stagnation pressure on the nose, this pressure imbalance pushes the body rearward. Streamlining keeps the flow attached nearly to the trailing edge and narrows the wake, cutting drag sharply: based on frontal area, NASA Glenn Research Center (n.d.a) lists a drag coefficient of 1.28 for a flat plate perpendicular to the flow compared with 0.045 for a streamlined airfoil shape, nearly a factor of 30 lower. Because an airfoil chart references $c_d$ to the chord (several times larger than the thickness), the section drag coefficient of the same airfoil is smaller still.
- **{term}`Interference drag`.** Where two parts meet, at a wing root or a pylon, the flows around them collide and the drag of the pair is more than the sum of the two alone. A rounded fairing in the corner, called a fillet, reduces it.

:::{figure} figures/p33-parasite-drag-kinds.svg
:label: fig-p33-parasite-drag-kinds
:alt: Three panels. Panel 1, skin friction: velocity arrows over a flat plate shrink toward zero at the wall; the curve through their tips is the velocity profile, and a bracket from the wall to the top of the profile marks the boundary layer. Short force arrows along the wall point downstream, labeled shear stress pulls the wall downstream. Panel 2, pressure drag: a round strut and a streamlined strut of the same thickness in the same free stream; the round strut leaves a wide hatched wake, the streamlined strut a thin one. Panel 3, interference: a fuselage seen from ahead with a low wing; the corner on the left is bare, the one on the right is filled with a fairing.
:width: 90%

Schematic, not to scale (the boundary layer is drawn far thicker than it is). Parasite drag has three causes: shear stress on the skin (1), low pressure in the wake behind a blunt body (2), and the extra drag where two parts meet (3). For the same thickness, the streamlined strut leaves a much thinner wake than the round one, and a fairing fills the corner where the wing meets the fuselage. Sources: FAA (2023), Chapter 5; the streamlined strut is a NACA 0033 section, 3 times as long as it is thick.
:::

A fourth kind, {term}`wave drag`, appears only as the aircraft nears the speed of sound, when shock waves form on its surface (NASA Glenn Research Center n.d.b). The critical Mach number is the flight Mach number at which the air somewhere on the aircraft first reaches the speed of sound. Wave drag rises sharply once the flight Mach number passes it by about 10% (FAA 2023, Chapter 5). We leave wave drag out of the polars on this page, so they hold only well below that speed.

### The zero-lift drag coefficient of an aircraft

The drag coefficient of the whole aircraft at zero lift is its **{term}`zero-lift drag coefficient`** $C_{D,0}$. Like every coefficient of the aircraft, it uses the wing area $S$ as its reference area, even though most of it comes from the fuselage, the tails, the engine nacelles, and the gaps around them:

$$
D_0 = q\,S\,C_{D,0}, \qquad q = \tfrac12 \rho V^2
$$

:::{warning} The airfoil's $c_d$ is not the aircraft's $C_{D,0}$
The section drag coefficient $c_d$ read from an airfoil chart ([page 3.2](#p32-airfoil-data)) is the drag of a slice of wing, per unit span, with no tips, no fuselage, and no tails. The NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 section of {numref}`fig-p33-polar-from-data` has $c_d = 0.0053$ at point B. A whole passenger jet has $C_{D,0}$ near 0.02 (Scholz n.d., Section 5.4), several times more. Use $C_{D,0}$ in the drag polar of an aircraft; use $c_d$ only for the wing section.
:::

(p33-drag-polar)=
## The drag polar

On page 3.2 we found the drag coefficient of a finite wing as its section drag plus the induced drag, $C_D = c_d + C_L^2/(\pi e\,\textit{AR})$ ([induced drag](#p32-induced-drag)). The whole aircraft follows the same pattern, with its zero-lift drag coefficient in place of $c_d$. The result is the **drag polar**:

::::{prf:definition} Drag polar
:label: def-p33-drag-polar

The **drag polar** of an aircraft is the relation between its drag coefficient and its lift coefficient. In its simplest form, the parabolic drag polar,

:::{math}
:label: eq-p33-polar
C_D = C_{D,0} + K C_L^2
:::

:::{math}
:label: eq-p33-K
K = \frac{1}{\pi e\,\textit{AR}}
:::

$C_{D,0}$ is the zero-lift drag coefficient, $K C_L^2$ the induced drag coefficient, $\textit{AR}$ the aspect ratio of the wing, and $e$ the span efficiency factor.
::::

For a whole aircraft, $e$ is the Oswald efficiency factor named on [page 3.2](#p32-induced-drag). It is lower than the $e$ of the wing alone. The drag of the fuselage and the tails also grows a little with lift, and the simple polar puts that growth into $K$. Scholz (n.d., Section 5.7), after Loftin, takes $e = 0.85$ for jet aircraft in cruise.

We can write the polar in three ways, all with the same information:

1. **An equation**, [](#eq-p33-polar), with two numbers that describe the aircraft: $C_{D,0}$ and $K$.
2. **A table** of $C_L$ against $C_D$, as in worked example 1 below.
3. **A graph** of one against the other, {numref}`fig-p33-polar-anatomy`.

You will usually see the graph plotted with $C_L$ on the vertical axis and $C_D$ on the horizontal axis. The curve is a horizontal parabola with its vertex at $C_D = C_{D,0}$ along $C_L = 0$. The horizontal distance between the vertical line $C_D = C_{D,0}$ and the curve is the induced drag coefficient, which starts at zero at zero lift and grows with $C_L^2$.

:::{figure} figures/p33-polar-anatomy.svg
:label: fig-p33-polar-anatomy
:alt: Graph of lift coefficient from minus 0.6 to 1.4 against drag coefficient from 0 to 0.09. A sideways parabola has its vertex at C sub D equals 0.017, C sub L equals 0. A gray band from C sub D equals 0 to 0.017 is labeled zero-lift drag; the light gold region between that band and the curve is labeled induced drag, K C sub L squared. Seven open circles on the curve mark the points of worked example 1, from C sub L of 0 to 1.2.
:width: 90%

Computed for the airliner of worked example 1, $C_{D,0} = 0.017$, $K = 0.038527$ (invented values typical of a twin-jet wide-body airliner). The drag coefficient at any lift coefficient is the zero-lift part, the same at every $C_L$, plus the induced part, which grows with $C_L^2$. The circles are the rows of {numref}`tbl-p33-example-polar`.
:::

### Worked example 1: the drag polar of an airliner

Consider a twin-jet wide-body airliner weighing $W = 1{,}500{,}000$ N in cruise, with a wing area $S = 300$ m², a span $b = 54.0$ m, a span efficiency factor $e = 0.85$, and a zero-lift drag coefficient $C_{D,0} = 0.017$. Build its drag polar.

1. **Aspect ratio.**
   $$
   \begin{aligned}
   \textit{AR} &= \frac{b^2}{S}\\
               &= \frac{{54.0}^{2}}{300}\\
               &= \frac{2{,}916}{300}\\
               &= 9.720
   \end{aligned}
   $$
2. **Induced drag factor**, [](#eq-p33-K), with five figures because it is used again:
   $$
   \begin{aligned}
   K &= \frac{1}{\pi e\,\textit{AR}}\\
     &= \frac{1}{\pi (0.85)(9.720)}\\
     &= \frac{1}{25.956}\\
     &= 0.038527
   \end{aligned}
   $$
3. **The polar**: $C_D = 0.017 + 0.038527\,C_L^2$.
4. **A table.** For each $C_L$, add the induced part to $C_{D,0}$ and divide $C_L$ by $C_D$. At $C_L = 0.6$:
   $$
   \begin{aligned}
   K C_L^2 &= 0.038527 \times {0.6}^{2}\\
           &= 0.013870\\
   C_D &= 0.017 + 0.013870\\
       &= 0.03087\\
   \frac{L}{D} &= \frac{C_L}{C_D} = \frac{0.6}{0.03087}\\
       &= 19.44
   \end{aligned}
   $$
   {numref}`tbl-p33-example-polar` gives the other rows.

:::{table} The drag polar of the airliner of worked example 1, $C_D = 0.017 + 0.038527\,C_L^2$: the lift, induced drag, and drag coefficients and the lift-to-drag ratio.
:label: tbl-p33-example-polar
:align: center

| Lift $C_L$ | Induced drag $K C_L^2$ | Drag $C_D$ | Lift-to-drag ratio $L/D$ |
| ---: | ---: | ---: | ---: |
| 0 | 0.00000 | 0.01700 | 0 |
| 0.2 | 0.00154 | 0.01854 | 10.79 |
| 0.4 | 0.00616 | 0.02316 | 17.27 |
| 0.6 | 0.01387 | 0.03087 | 19.44 |
| 0.8 | 0.02466 | 0.04166 | 19.20 |
| 1.0 | 0.03853 | 0.05553 | 18.01 |
| 1.2 | 0.05548 | 0.07248 | 16.56 |

:::

**Check.** At low $C_L$ the zero-lift part dominates and $L/D$ is poor; at high $C_L$ the induced part dominates and $L/D$ falls again. The best value in the table, 19.44 at $C_L = 0.6$, is inside the range page 1.6 gives for the [maximum $L/D$ of jet airliners](#tbl-p16-ld). The true maximum lies between $C_L = 0.6$ and 0.8, and the section on minimum drag finds it.

### Building a polar from wind-tunnel data

We can also measure a polar. In a wind tunnel we set a model at a series of {term}`angles of attack <angle of attack>`, and at each one the {term}`balance` measures the lift and the drag. That gives two curves against the angle of attack, $C_L(\alpha)$ and $C_D(\alpha)$. Each angle then gives one pair $(C_D, C_L)$, and plotting the pairs gives the polar ({numref}`fig-p33-polar-from-data`). Notice that the angle of attack no longer shows on the polar: each point stands for one angle, but the graph does not say which. The same steps work for a wing section, whose coefficients are written in lowercase.

:::{figure} figures/p33-polar-from-data.svg
:label: fig-p33-polar-from-data
:alt: Three small graphs side by side for the NACA 64-3-618 section at a Reynolds number of 6 million. Graph 1: lift coefficient against angle of attack, a nearly straight rising line. Graph 2: drag coefficient at each angle of attack, low and flat from about minus 2 to plus 4 degrees, rising on both sides. Graph 3: lift coefficient against drag coefficient. Three points are marked with the same letter and marker on every graph: A at minus 4 degrees, B at 2 degrees, C at 8 degrees. Point B has the least drag; C has the most.
:width: 85%

Redrawn from published data, NACA Report 824, page 195: the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 section at a {term}`Reynolds number` of 6 million. Follow one letter through the three panels: each point of the polar is one angle of attack ({numref}`tbl-p33-link`). Panel 1 is the report's lift curve. Panel 2 gives the drag at each angle, read from the report's curve of $c_d$ against $c_l$ at the lift of that angle. Panel 3 takes $c_l$ from panel 1 and $c_d$ from panel 2.
:::

:::{table} The angle of attack and the section lift and drag coefficients of the three marked points of {numref}`fig-p33-polar-from-data`, read from the curves (NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618, Reynolds number 6 million; Abbott, von Doenhoff, and Stivers 1945).
:label: tbl-p33-link
:align: center

| Point | Angle of attack $\alpha$, deg | Lift $c_l$ | Drag $c_d$ |
| --- | ---: | ---: | ---: |
| A | −4 | −0.04 | 0.0072 |
| B | 2 | 0.66 | 0.0053 |
| C | 8 | 1.22 | 0.0117 |

:::

Notice that this airfoil's polar departs from a simple parabola: its drag stays nearly flat inside a low-drag bucket and climbs steeply outside that band, because this 6-series family was shaped for laminar flow around a design lift coefficient ([page 3.2](#p32-airfoil-data)). Adding the fuselage, tails, and other components smooths out the bucket, so the parabolic model of [](#eq-p33-polar) fits a complete aircraft well for preliminary design.

### Symmetric and cambered sections

The polar of a symmetric section is symmetric about $c_l = 0$: the section has its least drag at zero lift, and the same drag at $c_l$ and at $-c_l$. A cambered section is shaped to make lift efficiently, and its lowest drag comes at a positive lift coefficient. {numref}`fig-p33-symmetric-cambered-polar` shows both for two sections of the same family and thickness, which differ only in camber. Here we take the low-drag range as the range of $c_l$ where $c_d$ stays within 10% of its minimum:

- NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-018 (symmetric): $c_l$ from −0.33 to 0.36, centered on zero to within the accuracy of the chart, with a least $c_d$ of 0.0046.
- NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 (cambered): $c_l$ from 0.26 to 0.88, with a least $c_d$ of 0.0047.

:::{figure} figures/p33-symmetric-cambered-polar.svg
:label: fig-p33-symmetric-cambered-polar
:alt: Graph of section lift coefficient, up, against section drag coefficient from 0 to 0.020, across, for two sections at a Reynolds number of 9 million. The symmetric NACA 64-3-018, dash-dot gray, has a low-drag stretch of nearly constant drag from about minus 0.33 to 0.36, centered on zero lift. The cambered NACA 64-3-618, solid black, has its low-drag stretch from about 0.26 to 0.88, shifted to positive lift. Vertical bars to the left of the curves mark the two low-drag ranges.
:width: 90%

Redrawn from published data, NACA Report 824, pages 192 and 195, at a Reynolds number of 9 million, with $c_l$ up as in the other polars of this page. Camber moves the low-drag range of the polar from zero lift to positive lift; the least drag is about the same. The bars mark where $c_d$ stays within 10% of its minimum.
:::

A complete aircraft with a cambered wing behaves the same way, reaching minimum drag at a small positive lift coefficient. For simplicity, the parabolic polar [](#eq-p33-polar) neglects that small shift and places minimum drag at $C_L = 0$, which is accurate enough for the analysis that follows.

### One polar for each configuration

A polar belongs to one aircraft in one configuration, at one [Reynolds number](#p31-reynolds-number) and one {term}`Mach number`. Lowering the flaps or the landing gear gives a different polar ({numref}`fig-p33-polar-configurations`). The extra drag of flaps and gear adds to $C_{D,0}$, and extended flaps also lower $e$, which makes $K$ larger. For passenger jets, Scholz (n.d., Section 5.4), after Loftin, takes these values: $\Delta C_{D,0} = 0.01$ for flaps at 15°, 0.03 for flaps at 35°, 0.015 for the gear down, and $e = 0.70$ with the flaps out. Scholz gives the flap increments for $C_L = 1.3$ at takeoff and 1.7 at landing, so the flapped polars hold near those lift coefficients. Added to the clean airliner of worked example 1, they give {numref}`tbl-p33-configurations`.

:::{table} Polars of the airliner of worked example 1 in three configurations: the zero-lift drag coefficient, the span efficiency factor, and the induced drag factor. The clean values are invented; the increments and $e$ with flaps are those of Scholz (n.d., Section 5.4).
:label: tbl-p33-configurations
:align: center

| Configuration | Zero-lift drag $C_{D,0}$ | Span efficiency $e$ | Induced drag factor $K$ |
| --- | ---: | ---: | ---: |
| Clean (cruise) | 0.017 | 0.85 | 0.03853 |
| Takeoff: flaps 15°, gear down | 0.042 | 0.70 | 0.04678 |
| Landing: flaps 35°, gear down | 0.062 | 0.70 | 0.04678 |

:::

:::{figure} figures/p33-polar-configurations.svg
:label: fig-p33-polar-configurations
:alt: Graph of lift coefficient from 0 to 2.0 against drag coefficient from 0 to 0.25 with three polars: clean, solid black, starting at 0.017; takeoff, dashed blue, starting at 0.042; landing, dotted vermilion, starting at 0.062. Each flapped polar lies to the right of the one before it and bends over more. A filled square on the takeoff polar marks C sub L equals 1.3, where L over D is 10.74; a filled diamond on the landing polar marks C sub L equals 1.7, where L over D is 8.621.
:width: 85%

Computed from {numref}`tbl-p33-configurations`. Flaps and landing gear shift the polar to the right and flatten it, so every lift coefficient produces more drag. The flap increments hold near $C_L = 1.3$ for takeoff and 1.7 for landing (Scholz n.d., Section 5.4); the two marked points give $L/D$ there, 10.74 and 8.621.
:::

Higher drag is often useful during landing. On final approach, the extra drag from flaps and landing gear lets the pilot fly slowly along a steeper descent path without picking up excess airspeed.

(p33-drag-speed)=
## Drag against speed in steady level flight

The polar gives drag coefficients, but a pilot or a designer wants the drag in newtons at a given speed. In **{term}`steady level flight`**, flight at constant speed and altitude, the forces balance: lift equals weight and thrust equals drag. That one condition, $L = W$, ties the lift coefficient to the speed, and the polar then gives the drag at any speed.

1. **Lift coefficient from the weight.** With $L = qSC_L = W$:
   :::{math}
   :label: eq-p33-level-CL
   C_L = \frac{W}{qS} = \frac{2W}{\rho V^2 S}
   :::
2. **Drag from the polar.** We multiply [](#eq-p33-polar) by $qS$:
   $$
   \begin{aligned}
   D &= qSC_D\\
     &= qSC_{D,0} + qS\,K C_L^2
   \end{aligned}
   $$
3. **Substitute the lift coefficient.** With $C_L = W/(qS)$, the second term is $qS\,K\,W^2/(qS)^2$, and one $qS$ cancels:
   :::{math}
   :label: eq-p33-drag-speed
   D = qSC_{D,0} + \frac{K W^2}{qS}
   :::

The first term is the parasite drag, the second the induced drag. With $q = \tfrac12\rho V^2$ they behave in opposite ways:

- the parasite drag $\tfrac12\rho V^2 S C_{D,0}$ grows with the square of the speed;
- the induced drag $2KW^2/(\rho V^2 S)$ falls with the square of the speed.

Their sum is a U-shaped curve with a minimum ({numref}`fig-p33-drag-speed`). Near the stall the induced drag dominates, and at high speed the parasite drag does (FAA 2023, Chapter 5).

:::{figure} figures/p33-drag-speed.svg
:label: fig-p33-drag-speed
:alt: Two graphs sharing a horizontal axis of true airspeed from 100 to 250 meters per second. The curves run from 109.5 to 232.6 meters per second; the shaded strips outside are labeled stall and wave drag. Top: drag in kilonewtons. A dashed parasite curve rises with speed, a dotted induced curve falls, and they cross at 164.5 meters per second, where each is about 38.4 kilonewtons. The solid total is U-shaped with its minimum of 76.78 kilonewtons at that speed. Squares mark 85.44 kilonewtons at 130 meters per second and 82.72 kilonewtons at 200. Bottom: lift-to-drag ratio, peaking at 19.54 at 164.5 meters per second.
:width: 85%

Computed for the airliner of worked example 2 at 7,500 m. Drag is least, and $L/D$ is largest, at one speed: where the falling induced drag meets the rising parasite drag. The two squares are the speeds of worked example 2, one on each side of the minimum, with drags within a few percent of each other. The curves stop where the polar stops holding (shaded). Below 109.5 m/s, level flight needs more than the clean $C_{L,\max}$, taken as 1.5. Above Mach 0.75 (232.6 m/s), also an invented limit, wave drag adds to the drag.
:::

**How angle of attack relates to speed.** Even though angle of attack does not appear on the horizontal axis of {numref}`fig-p33-drag-speed`, every steady level airspeed corresponds to a specific angle of attack. Equation [](#eq-p33-level-CL) sets $C_L = W/(qS)$ at each speed: flying faster requires a smaller $C_L$ and a lower angle of attack, while flying slower requires a larger $C_L$ and a higher angle of attack. Each speed on {numref}`fig-p33-drag-speed` maps to one point on the drag polar ({numref}`fig-p33-polar-anatomy`), which in turn corresponds to one angle of attack via the lift curve ([page 3.2](#p32-lift-curve)).

:::{warning} Weight in newtons, density of the air
$W$ in [](#eq-p33-drag-speed) is a force: the mass times $g_0$, in newtons, or pounds-force in English units (with $\rho$ in slug/ft³). An airliner of 152,905 kg weighs 1,500,000 N. If you put the mass in kilograms in place of $W$, the induced drag comes out ${9.81}^{2} = 96.24$ times too small. The density is that of the air at the flight altitude, from the standard atmosphere ([page 1.4](../chapter-1/standard-atmosphere.md)).
:::

(p33-minimum-drag)=
## Minimum drag and the maximum lift-to-drag ratio

In level flight the lift equals the weight, so we can write the drag with the weight:

$$
D = \frac{D}{L}\,L = \frac{C_D}{C_L}\,W
$$

Because weight is fixed, drag is minimized where $C_D/C_L$ is smallest, which is the same condition where $L/D$ reaches its maximum. In steady level flight, minimum drag and maximum lift-to-drag ratio occur at the same airspeed.

### The lift coefficient for minimum drag

1. **Write the quantity to minimize** with the polar [](#eq-p33-polar):
   $$
   \begin{aligned}
   \frac{C_D}{C_L} &= \frac{C_{D,0} + K C_L^2}{C_L}\\
                   &= \frac{C_{D,0}}{C_L} + K C_L
   \end{aligned}
   $$
   The first term falls as $C_L$ grows and the second rises, so there is a minimum between.
2. **Differentiate with respect to $C_L$** and set the derivative to zero:
   $$
   \begin{aligned}
   \frac{d}{dC_L}\left(\frac{C_D}{C_L}\right) &= -\frac{C_{D,0}}{C_L^2} + K\\
     &= 0
   \end{aligned}
   $$
3. **Solve for $C_L$.** The solution is the lift coefficient for minimum drag, $C_L^*$:
   :::{math}
   :label: eq-p33-CLstar
   \begin{aligned}
   C_L^{*} &= \sqrt{\frac{C_{D,0}}{K}}\\
     &= \sqrt{\pi e\,\textit{AR}\,C_{D,0}}
   \end{aligned}
   :::
   The second derivative, $2C_{D,0}/C_L^3$, is positive for $C_L > 0$, so this is a minimum of $C_D/C_L$ and a maximum of $L/D$.
4. **The drag coefficient there.** Squaring [](#eq-p33-CLstar) gives $K C_L^{*2} = C_{D,0}$: at minimum drag **the induced drag equals the parasite drag**, and
   $$
   \begin{aligned}
   C_D &= C_{D,0} + K C_L^{*2}\\
       &= 2C_{D,0}
   \end{aligned}
   $$
5. **The maximum lift-to-drag ratio** is $C_L^*$ divided by that drag coefficient:
   :::{math}
   :label: eq-p33-LDmax
   \begin{aligned}
   \left(\frac{L}{D}\right)_{\max} &= \frac{C_L^*}{2C_{D,0}}\\
       &= \frac{\sqrt{C_{D,0}/K}}{2C_{D,0}}\\
       &= \frac{1}{2\sqrt{K C_{D,0}}}
   \end{aligned}
   :::

Notice that the drag coefficient at minimum drag is twice $C_{D,0}$. An aircraft cannot hold level flight at $C_L = 0$ because it would generate no lift to support its weight. Supporting the weight produces induced drag, and at the optimal lift coefficient $C_L^*$, that induced drag equals the parasite drag.

{numref}`fig-p33-polar-tangent` shows the same result on the polar. The ratio $C_L/C_D$ at any point of the polar is the slope of the straight line from the origin to that point. The steepest such line just touches the polar: it is the tangent from the origin, and it touches at $C_L^*$.

:::{figure} figures/p33-polar-tangent.svg
:label: fig-p33-polar-tangent
:alt: Graph of lift coefficient from 0 to 1.5 against drag coefficient from 0 to 0.11 with the airliner's polar. Thin lines from the origin reach the polar at C sub L of 0.3, where L over D is 14.7, and at 1.35, where L over D is 15.5. A dashed line from the origin is tangent to the polar at a filled dot at C sub L star equals 0.6643, labeled tangent, slope L over D max equals 19.54. At the height of the tangent point, two equal dimension arrows split its drag coefficient: C sub D 0 equals 0.017 from the axis, then K C sub L star squared equals 0.017 up to the dot.
:width: 80%

Computed for the airliner of worked example 1. The lift-to-drag ratio at a point of the polar is the slope of the line from the origin to it; the tangent from the origin is the steepest line that still reaches the polar, so it marks $(L/D)_{\max}$ at $C_L^*$. There the induced part equals $C_{D,0}$, so $C_D = 0.034$, twice $C_{D,0}$.
:::

The tangent construction on the three polars of {numref}`fig-p33-polar-configurations` gives $(L/D)_{\max} = 19.54$ clean, 11.28 for takeoff, and 9.284 for landing. The flapped values come at $C_L^* = 0.948$ and 1.15, below the lift coefficients where the flap increments hold, so take them as values of the simple model only.

### The speed and the drag at the minimum

The speed that gives $C_L^*$ in level flight follows from [](#eq-p33-level-CL), solved for $V$:

:::{math}
:label: eq-p33-Vmd
V = \sqrt{\frac{2W}{\rho\,S\,C_L^*}}
:::

This is the **{term}`minimum-drag speed`**. The drag there is the weight divided by the best lift-to-drag ratio:

:::{math}
:label: eq-p33-Dmin
D_{\min} = \frac{W}{(L/D)_{\max}}
:::

The minimum drag depends only on the weight and on the polar. The speed where it occurs depends on the wing loading $W/S$ and on the density. Higher up, in thinner air, the same minimum drag comes at a higher true airspeed.

:::{warning} The lowest point of the polar is not the minimum drag
The smallest drag coefficient on the polar, $C_{D,0}$ at $C_L = 0$, describes an aircraft that carries no weight. In level flight the minimum drag is at $C_L^*$, where $C_D = 2C_{D,0}$. If you need $C_D$ at any other speed, do not use $2C_{D,0}$: compute $C_L$ from [](#eq-p33-level-CL) and $C_D$ from the polar.
:::

:::{tip} Method: minimum drag of an aircraft in level flight
1. Find $\textit{AR} = b^2/S$ and $K = 1/(\pi e\,\textit{AR})$.
2. Find the density at the flight altitude from the standard atmosphere.
3. Compute $C_L^* = \sqrt{C_{D,0}/K}$ and $(L/D)_{\max} = 1/(2\sqrt{K C_{D,0}})$.
4. Compute the minimum-drag speed $V = \sqrt{2W/(\rho S C_L^*)}$ and check its Mach number.
5. Compute $D_{\min} = W/(L/D)_{\max}$.
6. For any other speed, use $D = qSC_{D,0} + KW^2/(qS)$.
:::

### Why designers care

In steady level flight thrust equals drag, so minimum drag corresponds to the least thrust needed to stay aloft. Because a jet engine burns fuel roughly in proportion to thrust, flying near $(L/D)_{\max}$ minimizes fuel burn per unit time (maximum endurance). That is why a jet loiters near its maximum $L/D$ ([page 1.6](../chapter-1/aircraft-sizing.md)), and the [Breguet range equation](#eq-p16-range) shows that range also improves with higher $L/D$. Equation [](#eq-p33-LDmax) shows two ways we can increase $(L/D)_{\max}$: reduce $C_{D,0}$ through a cleaner, smoother airframe, or reduce $K$ by using a higher aspect ratio or higher span efficiency $e$. In [Chapter 5](#p51-thrust-required) we will use the drag curve to calculate thrust and power required, best range and endurance speeds, and climb performance.

### Worked example 2: minimum drag of the airliner

The airliner of worked example 1 ($W = 1{,}500{,}000$ N, $S = 300$ m², $C_{D,0} = 0.017$, $K = 0.038527$) flies level at 7,500 m. Find $C_L^*$, $(L/D)_{\max}$, the minimum-drag speed and the minimum drag, then the drag at 130 m/s and at 200 m/s.

1. **Density.** $h = 7{,}500$ m is in the troposphere. The standard atmosphere of [page 1.4](../chapter-1/standard-atmosphere.md) gives
   $$
   \begin{aligned}
   T &= 288.16 - 0.0065\,h\\
     &= 239.41\ \text{K}\\
   \rho &= 1.2250 \times {0.83082}^{4.2586}\\
        &= 0.55635\ \text{kg/m}^3
   \end{aligned}
   $$
   with $T/T_1 = 239.41/288.16 = 0.83082$.
2. **Lift coefficient for minimum drag**, [](#eq-p33-CLstar):
   $$
   \begin{aligned}
   C_L^* &= \sqrt{\frac{C_{D,0}}{K}}\\
         &= \sqrt{\frac{0.017}{0.038527}}\\
         &= \sqrt{0.44125}\\
         &= 0.6643
   \end{aligned}
   $$
3. **Maximum lift-to-drag ratio**, [](#eq-p33-LDmax):
   $$
   \begin{aligned}
   K C_{D,0} &= 0.038527\\
             &\;\;\; \times 0.017\\
             &= 0.00065496\\
   \left(\frac{L}{D}\right)_{\max} &= \frac{1}{2\sqrt{K C_{D,0}}}\\
       &= \frac{1}{2\sqrt{0.00065496}}\\
       &= \frac{1}{2 \times 0.025592}\\
       &= 19.537
   \end{aligned}
   $$
   Check with $C_L^*/(2C_{D,0}) = 0.6643/(2 \times 0.017) = 19.54$, the same. The induced drag coefficient there is $0.038527 \times 0.44129 = 0.01700$, equal to $C_{D,0}$, so $C_D = 0.034$.
4. **Minimum-drag speed**, [](#eq-p33-Vmd). The wing loading is $W/S = 1{,}500{,}000/300 = 5{,}000$ N/m², and
   $$
   \begin{aligned}
   \rho\,S\,C_L^* &= 0.55635 \times 300\\
                  &\quad \times 0.6643\\
                  &= 110.87\ \text{kg/m}\\
   V &= \sqrt{\frac{2W}{\rho\,S\,C_L^*}}\\
     &= \sqrt{\frac{3{,}000{,}000}{110.87}}\\
     &= \sqrt{27{,}059}\\
     &= 164.50\ \text{m/s}
   \end{aligned}
   $$
   The [speed of sound](#p14-speed-of-sound) at 239.41 K is $\sqrt{1.4 \times 287 \times 239.41} = 310.2$ m/s, so the Mach number is $164.5/310.2 = 0.530$: well below the speeds where wave drag appears.
5. **Minimum drag**, [](#eq-p33-Dmin):
   $$
   \begin{aligned}
   D_{\min} &= \frac{W}{(L/D)_{\max}}\\
          &= \frac{1{,}500{,}000}{19.537}\\
          &= 76{,}777\ \text{N}
   \end{aligned}
   $$
6. **Drag at 130 m/s** (Mach 0.419), [](#eq-p33-drag-speed). First the two pieces that every speed needs, $q$ and $K W^2$:
   $$
   \begin{aligned}
   q &= 0.5(0.55635)({130}^{2})\\
     &= 4{,}701\ \text{Pa}\\
   qS &= 4{,}701 \times 300\\
      &= 1{,}410{,}300\ \text{N}\\
   K W^2 &= 0.038527\\
         &\quad \times (1{,}500{,}000)^2\\
         &= 8.6686 \times {10}^{10}\ \text{N}^2
   \end{aligned}
   $$
   Then the two parts of the drag, the zero-lift (parasite) drag $D_0$ and the induced drag $D_i$:
   $$
   \begin{aligned}
   D_0 &= 1{,}410{,}300 \times 0.017\\
       &= 23{,}975\ \text{N}\\
   D_i &= \frac{8.6686 \times {10}^{10}}{1{,}410{,}300}\\
       &= 61{,}466\ \text{N}\\
   D &= 23{,}975 + 61{,}466\\
     &= 85{,}441\ \text{N}
   \end{aligned}
   $$
7. **Drag at 200 m/s**, the same way:
   $$
   \begin{aligned}
   q &= 0.5(0.55635)({200}^{2})\\
     &= 11{,}127\ \text{Pa}\\
   qS &= 11{,}127 \times 300\\
      &= 3{,}338{,}100\ \text{N}\\
   D_0 &= 3{,}338{,}100 \times 0.017\\
       &= 56{,}748\ \text{N}\\
   D_i &= \frac{8.6686 \times {10}^{10}}{3{,}338{,}100}\\
       &= 25{,}969\ \text{N}\\
   D &= 56{,}748 + 25{,}969\\
     &= 82{,}717\ \text{N}
   \end{aligned}
   $$
   The Mach number is $200/310.2 = 0.645$.

**Check.** Both speeds have more drag than the minimum, 76,777 N, as they must. At 130 m/s the lift coefficient is $1{,}500{,}000/1{,}410{,}300 = 1.064$, above $C_L^*$, so the induced drag is the larger part. At 200 m/s it is $1{,}500{,}000/3{,}338{,}100 = 0.4494$, below $C_L^*$, so the parasite drag is the larger part. The two drags are close, and so are their lift-to-drag ratios: $1{,}500{,}000/85{,}441 = 17.56$ and $1{,}500{,}000/82{,}717 = 18.13$, both below 19.54. {numref}`fig-p33-drag-speed` draws all three speeds.

### Worked example 3: the polar from measurements

In worked examples 1 and 2 we started from $C_{D,0}$ and $K$ and computed drag. In flight testing we work in reverse: we measure the thrust needed for steady level flight (which equals drag) at known speeds, and from those drag measurements we solve for $C_{D,0}$ and $K$. Each level-flight measurement gives one point $(C_L, C_D)$ on the polar, so two measurements determine the two constants.

**(a) Two drag measurements.** Consider a single-aisle airliner weighing $W = 650{,}000$ N with a wing area $S = 122$ m². In steady level flight at 4,500 m ($\rho = 0.7766$ kg/m³, [page 1.4](../chapter-1/standard-atmosphere.md)), its measured drag is 41,600 N at 115 m/s and 40,400 N at 175 m/s. Find $C_{D,0}$ and $K$.

1. **One point of the polar for each speed**: $q = \tfrac12\rho V^2$, then $C_L = W/(qS)$ from [](#eq-p33-level-CL) and $C_D = D/(qS)$ ({numref}`tbl-p33-flight-test`).

:::{table} Worked example 3: the two measured points, $W = 650{,}000$ N, $S = 122$ m², $\rho = 0.7766$ kg/m³.
:label: tbl-p33-flight-test
:align: center

| Speed $V$, m/s | Drag $D$, N | Dynamic pressure $q$, Pa | Pressure times area $qS$, N | Lift coefficient $C_L$ | Lift coefficient squared $C_L^2$ | Drag coefficient $C_D$ |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 115 | 41,600 | 5,135.3 | 626,507 | 1.0375 | 1.0764 | 0.066400 |
| 175 | 40,400 | 11,892 | 1,450,824 | 0.44802 | 0.20072 | 0.027846 |

:::

2. **Subtract the two polar equations** $C_{D1} = C_{D,0} + K C_{L1}^2$ and $C_{D2} = C_{D,0} + K C_{L2}^2$, so that $C_{D,0}$ drops out:
   $$
   \begin{aligned}
   K &= \frac{C_{D1} - C_{D2}}{C_{L1}^2 - C_{L2}^2}\\
     &= \frac{0.066400 - 0.027846}{1.0764 - 0.20072}\\
     &= \frac{0.038554}{0.87568}\\
     &= 0.044027
   \end{aligned}
   $$
3. **Zero-lift drag coefficient** from the first point:
   $$
   \begin{aligned}
   C_{D,0} &= C_{D1} - K C_{L1}^2\\
           &= 0.066400\\
           &{} - 0.044027 \times 1.0764\\
           &= 0.066400\\
           &{} - 0.047391\\
           &= 0.019009
   \end{aligned}
   $$

**Check.** The second point lies on the polar too: $0.019009 + 0.044027 \times 0.20072 = 0.027846$, its measured $C_D$. The polar of this airliner is $C_D = 0.0190 + 0.0440\,C_L^2$.

**(b) A stated maximum lift-to-drag ratio.** Sometimes we know $C_{D,0}$ and $(L/D)_{\max}$ instead, for example from a glide test. Squaring [](#eq-p33-LDmax) and solving for $K$ gives

:::{math}
:label: eq-p33-K-from-LD
K = \frac{1}{4\,C_{D,0}\,(L/D)_{\max}^2}
:::

Consider a fighter aircraft in clean configuration well below the speed of sound, with $C_{D,0} = 0.020$ and $(L/D)_{\max} = 11.0$:

$$
\begin{aligned}
K &= \frac{1}{4 \times 0.020 \times {11.0}^{2}}\\
  &= \frac{1}{9.680}\\
  &= 0.10331
\end{aligned}
$$

**Check.** Put this $K$ back into [](#eq-p33-LDmax): $1/(2\sqrt{0.10331 \times 0.020}) = 11.00$, the stated $(L/D)_{\max}$.

## Summary

:::{important} Summary
- Subsonic drag consists of parasite drag (skin friction, pressure drag, and interference drag, present even at zero lift) plus induced drag (the drag caused by generating lift). Wave drag adds to both as flight speed nears Mach 1.
- The drag polar $C_D = C_{D,0} + K C_L^2$, $K = 1/(\pi e\,\textit{AR})$, can be written as an equation, a table, or a graph. Each point is one angle of attack, and each configuration has its own polar. Two measured drags give two points of the polar and fix $C_{D,0}$ and $K$.
- In steady level flight $L = W$ gives $C_L = W/(qS)$ and $D = qSC_{D,0} + KW^2/(qS)$: parasite drag grows with $V^2$, induced drag falls with $1/V^2$.
- Minimum drag and $(L/D)_{\max}$ come at $C_L^* = \sqrt{C_{D,0}/K}$, where the two parts are equal and $C_D = 2C_{D,0}$; then $(L/D)_{\max} = 1/(2\sqrt{KC_{D,0}})$, $V = \sqrt{2W/(\rho S C_L^*)}$, and $D_{\min} = W/(L/D)_{\max}$.
:::

:::{table} The equations of this page.
:label: tbl-p33-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Drag polar | $C_D = C_{D,0} + K C_L^2$ |
| Induced drag factor | $K = 1/(\pi e\,\textit{AR})$ |
| Lift coefficient in level flight | $C_L = W/(qS) = 2W/(\rho V^2 S)$ |
| Drag in level flight | $D = qSC_{D,0} + KW^2/(qS)$ |
| Lift coefficient for minimum drag | $C_L^* = \sqrt{C_{D,0}/K}$ |
| Drag coefficient at minimum drag | $C_D = 2C_{D,0}$ |
| Maximum lift-to-drag ratio | $(L/D)_{\max} = 1/(2\sqrt{KC_{D,0}})$ |
| $K$ from two points of the polar | $K = (C_{D1} - C_{D2})/(C_{L1}^2 - C_{L2}^2)$ |
| $K$ from $(L/D)_{\max}$ | $K = 1/(4\,C_{D,0}\,(L/D)_{\max}^2)$ |
| Minimum-drag speed | $V = \sqrt{2W/(\rho S C_L^*)}$ |
| Minimum drag | $D_{\min} = W/(L/D)_{\max}$ |

:::

:::{exercise} For discussion
:label: ex-p33-discussion

1. A sailplane has a wing of high aspect ratio and a smooth skin. Which term of the drag polar does each feature lower, and why does a sailplane need both?
2. Wheel fairings on a small aircraft, wingtip extensions, and a cleaner wing-root fairing all lower drag. Which part of the polar does each one change?
3. An airliner flies at the same weight at 3,000 m and at 9,000 m. Do its minimum drag, its $(L/D)_{\max}$, and its minimum-drag speed change? Explain from the equations.
4. As fuel burns, an airliner's weight falls. What happens to its minimum drag and to its minimum-drag speed at a fixed altitude?
5. Why might a pilot on approach to landing want more drag, not less?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-3-3.html
:label: quiz-3-3
:width: 100%
:enumerated: false

Quiz for Standard 3.3: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Abbott, I. H., A. E. von Doenhoff, and L. S. Stivers, Jr., "[Summary of Airfoil Data](https://ntrs.nasa.gov/citations/19930090976)," NACA Report 824, National Advisory Committee for Aeronautics, 1945. Pages 192 (NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-018) and 195 (NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618).
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023. Chapter 5, "Aerodynamics of Flight."
- NASA Glenn Research Center, "[Shape Effects on Drag](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/shape-effects-on-drag/)," Beginner's Guide to Aeronautics, n.d.a.
- NASA Glenn Research Center, "[What is Drag?](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/what-is-drag/)," Beginner's Guide to Aeronautics, n.d.b.
- Scholz, D., "[Aircraft Design, Chapter 5: Preliminary Sizing](https://www.fzt.haw-hamburg.de/pers/Scholz/HOOU/AircraftDesign_5_PreliminarySizing.pdf)," lecture notes, Hamburg University of Applied Sciences, n.d. Section 5.4 (flap and landing-gear increments after Loftin 1980) and Section 5.7 (span efficiency of jets in cruise).

