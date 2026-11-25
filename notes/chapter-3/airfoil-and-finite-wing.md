---
title: "3.2 Airfoil and Finite Wing"
short_title: 3.2 Airfoil and Finite Wing
---

:::{include} ../_parts/standards/3.2.md
:::

We design a wing in two steps. First we test its cross-section, the {term}`airfoil`, in a wind tunnel as if the wing had no ends. Then we correct those data for a real wing, whose tips change the flow over the whole span. As [page 1.5](../chapter-1/bernoulli-and-pitot-static.md) showed, lift and drag come from the pressure and the shear stress on the surface. They exist only while the body and the air move relative to each other (NASA Glenn Research Center n.d.b).

:::{note} What to take from this page
- The angle of attack $\alpha$ is measured from the free stream to the chord line. Lift is perpendicular to the free stream and drag is parallel to it.
- Forces and moment are written as $L = qSC_L$, $D = qSC_D$, $M = qScC_M$. Lowercase coefficients ($c_l$, $c_d$, $c_m$) belong to the airfoil, an infinite wing; uppercase ones to the finite wing or the whole aircraft.
- To read an airfoil chart, compute the Reynolds number first and pick the closest curve. Read $c_l$ and $c_{m,c/4}$ at the angle of attack, then $c_d$ at that $c_l$.
- Tip vortices push the air down behind the wing. As a result, the wing operates at a smaller effective angle of attack, its lift curve is less steep ($a = a_0/(1 + 57.3\,a_0/(\pi e\,\textit{AR}))$), and it generates induced drag $C_{D,i} = C_L^2/(\pi e\,\textit{AR})$.
:::

(p32-angle-of-attack)=
## Free stream, angle of attack, lift, and drag

If you hold your hand flat out the window of a moving car and tilt the front edge upward, the airflow pushes your hand upward and backward, and tilting it further increases that force. What sets the force is the tilt of your hand relative to the oncoming airstream, which is the same idea as an airfoil's angle of attack.

:::{prf:definition} Free stream, chord line, and angle of attack
:label: def-p32-angle-of-attack

The **free stream** is the undisturbed air far ahead of the body, seen from the body: its velocity is the {term}`free-stream velocity` $V_\infty$, also called the relative wind. For an aircraft in still air it points opposite to the flight path.

The **chord line** is the straight line from the leading edge to the trailing edge of the airfoil; its length is the {term}`chord` $c$ (see [airfoil geometry](#p13-airfoil)).

The **{term}`angle of attack`** $\alpha$ is the angle between the free-stream direction and the chord line (FAA 2023, Chapter 5). It is positive when the leading edge is tilted up into the free stream.
:::

{numref}`fig-p32-angle-of-attack` puts the definitions on one airfoil. The {term}`lift` $L$ is the part of the total aerodynamic force perpendicular to the free stream. The {term}`drag` $D$ is the part parallel to it, as in the [pressure and shear figure of page 1.5](#fig-p15-pressure-and-shear). Both are drawn at the quarter-chord point, $c/4$ behind the leading edge, with the pitching moment $M$ about that point, which we explain after the coefficients.

:::{figure} figures/p32-angle-of-attack.svg
:label: fig-p32-angle-of-attack
:alt: An airfoil tilted nose up in a free stream that comes from the left. A thin horizontal line runs along the free-stream direction to the leading edge, and the dashed chord line runs from the trailing edge through the leading edge and on ahead of it. The angle of attack alpha is marked by an arc between these two lines, with its label inside the angle. At the quarter-chord point a vertical arrow shows the lift and a horizontal arrow pointing downstream shows the drag. A curved arrow over the airfoil turning nose down shows the pitching moment M.
:width: 80%

Schematic of the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 section at $\alpha$ = 8°. Lift is perpendicular to the free stream and drag parallel to it, whatever the tilt of the chord, and $\alpha$ is measured from the free stream to the chord line. The moment about the quarter chord of this cambered section is nose down.
:::

The angle of attack has nothing to do with the horizon or with gravity. {numref}`fig-p32-alpha-not-horizon` shows the same airfoil at the same angle of attack in a climb, in level flight, and in a descent. What changes is the pitch angle $\theta$, between the chord line and the horizon. The flight path makes the flight-path angle $\gamma$ with the horizon (positive in a climb), and the free stream runs along the flight path, so

$$
\theta = \gamma + \alpha
$$

In level flight $\gamma = 0$ and $\theta = \alpha$. In a steep climb the nose points high while $\alpha$ stays where it was. A glider in a steady glide, nose near or below the horizon, still flies at a positive angle of attack.

:::{figure} figures/p32-alpha-not-horizon.svg
:label: fig-p32-alpha-not-horizon
:alt: Three rows, each with the same airfoil, a dashed horizon line through its leading edge, the free-stream line and arrow, and the dashed chord line. In the climb the free stream comes down from the upper left, 25 degrees below the horizon going right, and the airfoil is pitched 35 degrees nose up. In level flight the free stream is along the horizon and the airfoil is pitched 10 degrees nose up. In the descent the free stream comes up from the lower left and the airfoil is pitched 15 degrees nose down. In every row the angle alpha between the free stream and the chord line is the same 10 degrees. The pitch angle theta, between the horizon and the chord, and the flight-path angle gamma, between the horizon and the free-stream line, are marked by their own arcs in the climb and the descent.
:width: 90%

Schematic, flight paths 25° above and below the horizon and $\alpha$ = 10°, angles drawn large so they can be seen. The angle of attack is the same in all three rows. The flight-path angle $\gamma$ and the pitch angle $\theta$, both measured from the horizon, change from row to row, and in each row $\theta = \gamma + \alpha$.
:::

:::{warning} Find the free stream first
On every sketch, draw $V_\infty$ first, then the chord line, then lift perpendicular and drag parallel to $V_\infty$. Lift is not "up" and drag is not "along the chord".
:::

(p32-coefficients)=
## Lift, drag, and moment coefficients

A wind-tunnel model is smaller than the aircraft and is often tested at a different speed, so we need dimensionless quantities that carry over from model to full scale. Lift grows with the wing area $S$, airspeed, air density, and, up to stall, angle of attack; it also depends on the airfoil and wing shape, viscosity, and compressibility. Viscosity enters through the chord-based {term}`Reynolds number` ([page 3.1](#p31-reynolds-number)), $\textit{Re} = \rho V c/\mu$, and compressibility enters through the {term}`Mach number`. Dividing each force by $qS$ (the {term}`dynamic pressure` times the wing area) removes the direct scaling with size, speed, and air density, isolating the effects of geometry, $\alpha$, $\textit{Re}$, and $M$ inside one dimensionless coefficient. Once measured in a wind tunnel, that coefficient applies to any geometrically similar wing at the same angle of attack, Reynolds number, and Mach number.

::::{prf:definition} Force and moment coefficients
:label: def-p32-coefficients

With the dynamic pressure $q = \tfrac12 \rho V_\infty^2$, the wing area $S$, and a reference chord $c$, the **{term}`lift coefficient`** $C_L$, the **{term}`drag coefficient`** $C_D$, and the **moment coefficient** $C_M$ are defined by

:::{math}
:label: eq-p32-forces
\begin{aligned}
L &= q\,S\,C_L\\
D &= q\,S\,C_D\\
M &= q\,S\,c\,C_M
\end{aligned}
:::
::::

The moment needs one more length, the chord. In units, $q$ is a pressure (N/m², or lb/ft²); times an area it is a force, and times a length it is a moment. A coefficient has no units.

An airfoil is a two-dimensional shape. Its data describe a wing of constant section that never ends, an **{term}`infinite wing`**. In a wind tunnel we make one by letting the model span the test section from wall to wall, so the air finds no tip to flow around. The forces are measured per unit span, and the area per unit span is the chord, $S = c \times 1$. Lowercase letters mark the airfoil coefficients:

:::{math}
:label: eq-p32-section
\begin{aligned}
L' &= q\,c\,c_l\\
D' &= q\,c\,c_d\\
M' &= q\,c^2\,c_m
\end{aligned}
:::

with $L'$, $D'$ in N/m and $M'$ in N·m per meter of span. The moment coefficient carries the point it is taken about: $c_{m,c/4}$ about the quarter chord, $c_{m,\text{ac}}$ about the aerodynamic center of the next section. Uppercase $C_L$, $C_D$, $C_M$ belong to a **{term}`finite wing`**, which has tips, or to a whole aircraft.

:::{warning} Pounds are forces here
In English units, "lb" for lift and drag means pound-force (lbf), and mass is in slugs (sea-level air has $0.002377$ slug/ft³). One pound-force accelerates one slug at 1 ft/s², so 1 lb = 1 slug·ft/s². With $\rho$ in slug/ft³ and $V$ in ft/s, $q = \tfrac12\rho V^2$ comes out in slug/(ft·s²), which is lb/ft². Never put a weight in pound-mass into $L = qSC_L$.
:::

### Worked example 1: the lift coefficient of a fighter

Consider a fighter aircraft with a wing area $S = 280$ ft² flying at 240 knots at sea level ($\rho = 0.002377$ slug/ft³) while its wing generates $L = 22{,}000$ lb of lift. Find the lift coefficient.

1. **Speed in ft/s.** One knot is 1.6878 ft/s:
   $$
   \begin{aligned}
   V_\infty &= 240 \times 1.6878\\
            &= 405.1\ \text{ft/s}
   \end{aligned}
   $$
2. **Dynamic pressure**, in lb/ft² (see the warning above):
   $$
   \begin{aligned}
   q &= \tfrac12 \times 0.002377 \times {405.1}^{2}\\
     &= \tfrac12 \times 0.002377 \times 164{,}106\\
     &= 195.0\ \text{lb/ft}^2
   \end{aligned}
   $$
3. **Lift coefficient**, from [](#eq-p32-forces):
   $$
   \begin{aligned}
   C_L &= \frac{L}{qS}\\
       &= \frac{22{,}000}{195.0 \times 280}\\
       &= \frac{22{,}000}{54{,}600}\\
       &= 0.4029
   \end{aligned}
   $$

**Check.** The units cancel: lb divided by (lb/ft²)(ft²) leaves no units. Flying slower with the same lift would need a larger $C_L$, because $q$ falls with the square of the speed.

(p32-moment)=
## The pitching moment and the aerodynamic center

Worked example 1 needed only the lift. To know where that lift acts on the chord, we also need the moment of the surface forces. The pressure and shear forces on an airfoil add up to one force, and they also tend to rotate the airfoil. The **{term}`pitching moment`** $M$ is the moment of all the surface forces about a chosen point on the chord, per unit span for an airfoil. We take a moment that raises the leading edge (nose up) as positive. Its magnitude depends on the reference point we choose.

:::{prf:definition} Center of pressure and aerodynamic center
:label: def-p32-centers

The **{term}`center of pressure`** is the point on the chord where the resultant aerodynamic force acts. About it the moment is zero.

The **{term}`aerodynamic center`** (a.c.) is the point on the chord about which the pitching moment does not change with the angle of attack. On airfoils at low speed it lies near the quarter chord.
:::

The center of pressure looks like the natural point to use, but it moves. To see this, we put the lift $L'$ per unit span at $x_\text{cp}$ from the leading edge and take the moment about the quarter chord. A lift behind the quarter chord pitches the nose down, so

$$
M'_{c/4} = -L'\left(x_\text{cp} - \frac{c}{4}\right)
$$

Dividing by $q c^2$ turns the moment and the lift into the section coefficients, $c_{m,c/4} = -c_l\,(x_\text{cp}/c - 1/4)$. Solving for the center of pressure,

:::{math}
:label: eq-p32-cp
\frac{x_\text{cp}}{c} = \frac{1}{4} - \frac{c_{m,c/4}}{c_l}
:::

For a cambered airfoil, $c_{m,c/4}$ stays nearly constant as angle of attack changes, while $c_l$ varies widely. Equation [](#eq-p32-cp) shows that $x_\text{cp}$ moves aft as lift decreases, and approaches infinity as $c_l$ approaches zero. Physically, at zero lift a cambered airfoil still produces a nonzero pitching couple, and a pure couple with zero net force cannot be represented by a single force acting at any finite point on the chord. {numref}`tbl-p32-cp` evaluates [](#eq-p32-cp) for the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 at a Reynolds number of 6 million, using data from the chart in the next section (approximating the normal force by the lift, which is accurate at small angles). Over a 9° change in angle of attack, the center of pressure shifts from 0.55$c$ to 0.35$c$.

:::{table} Center of pressure of the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 from its section lift and moment coefficients, read from its chart at a Reynolds number of 6 million.
:label: tbl-p32-cp
:align: center

| Angle of attack $\alpha$, deg | Lift $c_l$ | Moment $c_{m,c/4}$ | Center of pressure $x_\text{cp}/c$ |
| ---: | ---: | ---: | ---: |
| −1 | 0.33 | −0.099 | 0.55 |
| 2 | 0.66 | −0.102 | 0.40 |
| 8 | 1.22 | −0.118 | 0.35 |

:::

Using the aerodynamic center avoids a moving reference point. We place the lift at the aerodynamic center and add one constant pitching moment $M_\text{ac}$ that does not vary with angle of attack ({numref}`fig-p32-moment-and-ac`). For this section at a Reynolds number of 6 million, NACA Report 824 locates the aerodynamic center at 0.275$c$, and its chart gives $c_{m,\text{ac}} \approx -0.092$ (Abbott, von Doenhoff, and Stivers 1945, page 195). The position of this point relative to the center of gravity will become important later when we study longitudinal stability.

:::{figure} figures/p32-moment-and-ac.svg
:label: fig-p32-moment-and-ac
:alt: Left panel, titled lift at the center of pressure: one airfoil drawn level over a chord scale from 0 to 1, with three upward lift arrows standing on the chord, labeled alpha equals minus 1 degree at 0.55 c, 2 degrees at 0.40 c, and 8 degrees at 0.35 c. The shortest, for minus 1 degree, stands farthest aft; the tallest, for 8 degrees, stands farthest forward. Right panel, titled lift at the aerodynamic center: the same airfoil with a single lift arrow at the point labeled aerodynamic center, 0.275 c, and a curved nose-down moment arrow labeled M ac, the same at every angle of attack.
:width: 90%

Computed from the NACA Report 824 data of the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 at a Reynolds number of 6 million, arrows in proportion to $c_l$, section drawn level. The center of pressure moves with $\alpha$ (left); the aerodynamic center stays fixed and carries one constant moment $M_\text{ac}$ (right).
:::

Camber determines the sign of $c_{m,\text{ac}}$. A positively cambered airfoil carries more lift toward the rear of the chord than a flat plate does, which creates a nose-down pitching moment, so $c_{m,\text{ac}}$ is negative. By symmetry, a symmetric airfoil produces no pitching moment at zero lift. Because $c_{m,\text{ac}}$ does not change with $\alpha$, it remains zero at every angle of attack below stall, and the center of pressure coincides with the aerodynamic center. On the chart of the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-018 in NACA Report 824, page 192, $c_{m,\text{ac}}$ stays within about 0.01 of zero.

(p32-airfoil-data)=
## Reading airfoil data

The airfoil data on this page come from NACA Report 824, "Summary of Airfoil Data" (Abbott, von Doenhoff, and Stivers 1945), measured with each model spanning the tunnel (page 3 of the report). We use two sections of its 6-series family. In the name NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618, the 6 is the series. The 4 says that the symmetric section, at zero lift, has its minimum pressure at 0.4 of the chord. The subscript 3 says the low-drag range extends 0.3 in $c_l$ above and below the design lift coefficient. After the dash, the 6 is that design lift coefficient in tenths, 0.6, and the last two digits give the thickness, 18% of the chord (report pages 5 and 6). The NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-018 has the same thickness form and no camber. The four-digit names of page 1.3 ([airfoil geometry](#p13-airfoil)) follow a different code.

{numref}`fig-p32-airfoil-chart` redraws the report's chart for the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 in the report's layout. The left panel gives $c_l$ (inner scale) and $c_{m,c/4}$ (outer scale) against $\alpha$. The right panel gives $c_d$ (upper part) and $c_{m,\text{ac}}$ (lower part) against $c_l$. Each family has three curves, one for each Reynolds number tested, 3, 6, and 9 million (the report writes $R$ for the Reynolds number).

:::{figure} figures/p32-airfoil-chart.svg
:label: fig-p32-airfoil-chart
:alt: The two-panel chart of the NACA 64-3-618 section. Left: lift coefficient against angle of attack from about minus 17 to 24 degrees, a straight line through c l equal to zero near minus 3.7 degrees, rising to a rounded peak near 1.4 to 1.6 between 15 and 20 degrees, the peak higher for higher Reynolds number; below it the quarter-chord moment coefficient, about minus 0.1, read on a separate scale outside the lift scale. Right: drag coefficient against lift coefficient, a bucket with its floor near 0.005 between c l of about 0.2 and 1.0, lower for higher Reynolds number; below it the aerodynamic-center moment coefficient, flat near minus 0.09, read on a scale on the right. Numbered dashed reading lines, each ending in an arrowhead at the scale it is read on: 1 from alpha equals 2 degrees up to the lift curve and across to c l equal to 0.66; 2 across, past the lift scale, to the outer moment scale at minus 0.10; 3 from c l equal to 0.66 up to the drag curve and across to c d equal to 0.0053; 4 across to the right-hand scale at c m ac of minus 0.092.
:width: 90%

Redrawn from published data, NACA Report 824, page 195 (Abbott, von Doenhoff, and Stivers 1945): the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 section, smooth model, at Reynolds numbers of 3, 6, and 9 million. Lift and moment are read against $\alpha$ on the left, drag and $c_{m,\text{ac}}$ against $c_l$ on the right, all on the curve of one Reynolds number. The numbered dashed lines are the readings of worked example 2 at $\alpha$ = 2° on the 6 million curves: 1 $c_l$, 2 $c_{m,c/4}$, 3 $c_d$ at that $c_l$, 4 $c_{m,\text{ac}}$.
:::

:::{tip} Reading an airfoil chart
First compute the Reynolds number based on the chord, $\textit{Re} = \rho V c/\mu$, and pick the curve closest to it. The curves differ most near stall and at the edges of the drag bucket. Then follow the numbered lines of {numref}`fig-p32-airfoil-chart`:

1. **Lift.** Go up from the angle of attack on the horizontal axis of the left panel to the lift curve, then across to the $c_l$ scale.
2. **Moment.** From the same angle, go to the $c_{m,c/4}$ curve and across to the outer moment scale. Keep the sign: $c_{m,c/4} = -0.10$ means nose down.
3. **Drag.** Find the $c_l$ of step 1 on the horizontal axis of the right panel, go up to the drag curve of the same Reynolds number, and across to the $c_d$ scale. You read $c_d$ against $c_l$, not against $\alpha$.
4. **Moment about the aerodynamic center**, if needed: from the same $c_l$ go to the $c_{m,\text{ac}}$ curve and across to its scale on the right.
:::

The chart gives five section characteristics, all used later on this page.

- **{term}`Lift-curve slope <lift-curve slope>` $a_0$.** Between about −6° and 5° the lift curve is a straight line, $c_l = a_0(\alpha - \alpha_{L=0})$. Its slope, measured between −2° and 4°, is $a_0 = 0.115$ per degree, the same at the three Reynolds numbers.
- **{term}`Zero-lift angle of attack <zero-lift angle of attack>` $\alpha_{L=0}$.** The cambered section still produces lift at $\alpha = 0$. Its lift is zero at $\alpha_{L=0} \approx -3.7$°, read from the chart.
- **Stall and maximum lift.** Above about 6° the curve bends over as the flow starts to separate from the upper surface. The section then reaches its {term}`maximum lift coefficient`, $c_{l,\max}$ = 1.37, 1.51, and 1.61 at 3, 6, and 9 million. A higher Reynolds number delays separation.
- **Drag bucket.** Inside the low-drag range the drag curve forms a bucket, because there the {term}`boundary layer` stays laminar over much of the chord ([page 3.1](#fig-p31-boundary-layer)). Its floor falls from 0.0058 at 3 million to 0.0051 at 6 million and 0.0047 at 9 million. Outside it the drag climbs quickly. Roughness such as insects, rain, or rivet heads trips the boundary layer turbulent: on the report's curve for a model with standard roughness the bucket is gone and the drag is about twice as high.
- **Moment.** $c_{m,\text{ac}}$ is nearly flat, about −0.092 at 6 million, up to stall.

{numref}`fig-p32-symmetric-cambered` compares the cambered section with its symmetric twin. The two lift curves have nearly the same slope, 0.115 and 0.110 per degree between −2° and 4°. The cambered curve is shifted to the left: its lift is zero at −3.7° instead of 0°, and at $\alpha$ = 0 it already produces $c_l \approx 0.44$.

:::{figure} figures/p32-symmetric-cambered.svg
:label: fig-p32-symmetric-cambered
:alt: Lift coefficient against angle of attack from minus 10 to 20 degrees for two sections at a Reynolds number of 6 million. The NACA 64-3-618, cambered, solid line with squares, crosses zero lift at about minus 3.7 degrees and peaks near 1.51. The NACA 64-3-018, symmetric, gray dash-dot line with circles, crosses zero lift at 0 degrees and peaks near 1.35. The two straight parts are parallel; the cambered line lies to the left of the symmetric one.
:width: 85%

Redrawn from published data, NACA Report 824, pages 192 and 195 (Abbott, von Doenhoff, and Stivers 1945), Reynolds number 6 million. Camber shifts the lift curve to a negative zero-lift angle without changing its slope.
:::

### Worked example 2: a model wing in a wind tunnel

A model wing of constant chord $c = 1.2$ m with the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 section spans the test section of a large low-speed wind tunnel. The test-section speed is 72 m/s, the air is at sea-level conditions ($\rho = 1.2250$ kg/m³, $\mu = 1.789 \times {10}^{-5}$ kg/(m·s)), and the model is set at $\alpha$ = 2°. Find the lift, drag, and moment per meter of span.

1. **Mach check.** With the [speed of sound](#p14-speed-of-sound) at sea level, 340.3 m/s, the Mach number is $72/340.3 = 0.2116$. That is below 0.3, so the low-speed data apply.
2. **Reynolds number**, based on the chord:
   $$
   \begin{aligned}
   \textit{Re} &= \frac{\rho V c}{\mu}\\
               &= \frac{1.2250 \times 72 \times 1.2}{1.789 \times {10}^{-5}}\\
               &= 5.916 \times {10}^{6}
   \end{aligned}
   $$
   The closest curve is the 6 million curve.
3. **Lift coefficient** (reading 1 in {numref}`fig-p32-airfoil-chart`): at $\alpha$ = 2°, $c_l \approx 0.66$.
4. **Moment coefficient** (reading 2): $c_{m,c/4} \approx -0.10$, nose down.
5. **Drag coefficient** (reading 3): at $c_l = 0.66$, inside the drag bucket, $c_d \approx 0.0053$. Reading 4 gives $c_{m,\text{ac}} \approx -0.092$, close to $c_{m,c/4}$ because the aerodynamic center lies close to the quarter chord.
6. **Dynamic pressure:**
   $$
   \begin{aligned}
   q &= \tfrac12 \times 1.2250 \times {72}^{2}\\
     &= 3{,}175.2\ \text{Pa}
   \end{aligned}
   $$
7. **Forces and moment per unit span**, from [](#eq-p32-section):
   $$
   \begin{aligned}
   L' &= q\,c\,c_l\\
      &= 3{,}175.2 \times 1.2\\
      &\;\;\; \times 0.66\\
      &= 2{,}515\ \text{N/m}\\
   D' &= q\,c\,c_d\\
      &= 3{,}175.2 \times 1.2\\
      &\;\;\; \times 0.0053\\
      &= 20.19\ \text{N/m}\\
   M'_{c/4} &= q\,c^2\,c_{m,c/4}\\
            &= 3{,}175.2 \times 1.44\\
            &\;\;\; \times (-0.10)\\
            &= -457.2\ \text{N}\cdot\text{m/m}
   \end{aligned}
   $$

**Check.** The section lift-to-drag ratio is $c_l/c_d = 0.66/0.0053 = 124.5$, typical of a smooth airfoil operating inside its drag bucket. A complete finite wing cannot reach this value because of three-dimensional tip effects, as we will see next.

(p32-finite-wing)=
## Why a finite wing is different

So far we have treated the wing as infinite in span, with no wingtips. On a real finite wing producing lift, the higher pressure on the lower surface drives air around each wingtip toward the lower-pressure upper surface (FAA 2023, Chapter 5). That curling flow rolls up behind the wing into two trailing **{term}`wingtip vortices <wingtip vortex>`**. Between the tips, these vortices induce a downward velocity component at and behind the wing, called the **{term}`downwash`** $w$. Outboard of the tips, they induce an upward velocity called upwash ({numref}`fig-p32-tip-vortices`).

:::{figure} figures/p32-tip-vortices.svg
:label: fig-p32-tip-vortices
:alt: A twin-engine airliner seen from behind, wings slightly raised toward the tips, with its vertical and horizontal tails. Numbered labels give the chain of cause and effect: 1, higher pressure below the wing; 2, flow around the tip, a curved line at each tip that starts under the wing, passes below and outboard of the tip, rises, and curls over the top inward into 3, the tip vortex just inboard of and above the tip. Seen from behind, the left tip vortex turns clockwise and the right one counterclockwise. 4, a row of equal downward arrows below the wing marks the downwash between the tips, and an upward arrow outside each tip marks the upwash. Lower pressure is marked above the wing.
:width: 90%

Schematic of a jet transport seen from behind, proportions of the Boeing 737-800, vortex size not to scale. The higher pressure below the wing (1) drives air around each tip (2), where it rolls up into a vortex (3), with downwash between the vortices and upwash outside (4).
:::

{numref}`fig-p32-vortex-photo` shows a real tip vortex, made visible with colored smoke.

:::{figure} figures/p32-wingtip-vortex-photo.jpg
:label: fig-p32-vortex-photo
:alt: An agricultural airplane seen from behind as it flies away low over a grass field. Red smoke rising from the ground behind it has rolled up into a large spiral, about as wide as the wingspan in the picture, above and just outboard of its right wing tip. On the side of the spiral toward the fuselage, the smoke is carried down toward the wing.
:width: 70%

Photograph. Colored smoke rising from the ground rolls up behind the wing tip into the tip vortex, and inboard of the vortex the air moves down: the downwash behind the wing. Wake vortex study, NASA Wallops Flight Facility, 1990. NASA Langley Research Center photo L90-5919 (EL-1996-00130), public domain; cropped and color-adjusted version from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Airplane_vortex_edit.jpg).
:::

A smaller airplane that flies into these vortices can be rolled harder than its ailerons can counter (FAA 2014, Sections 3 and 6). This is why air traffic controllers keep wake turbulence separations between airplanes (FAA 2014, Section 8).

Each section of the wing now experiences the free stream combined with the downward velocity $w$, tilting the incoming flow downward by a small angle. We build the vectors of {numref}`fig-p32-downwash-vectors` in the steps below; the numbers on the figure are the step numbers.

:::{tip} The downwash construction, step by step
1. Draw the airfoil at angle of attack $\alpha$ to the free stream $V_\infty$. This $\alpha$, the angle the pilot sets, is the **geometric angle of attack**.
2. Add the downwash $w$, a small velocity pointing down.
3. Add the two vectors: $V_\infty + w$ is the **local relative wind**, the flow the airfoil section experiences, tilted downward from $V_\infty$.
4. Mark the angles. The angle between the free stream and the local relative wind is the **{term}`induced angle of attack`** $\alpha_i$. The angle between the local relative wind and the chord line is the **{term}`effective angle of attack`** $\alpha_\text{eff}$, the angle the section works at. From the figure, $\alpha = \alpha_\text{eff} + \alpha_i$.
5. Draw the local section lift perpendicular to the local relative wind, which tilts it backward by $\alpha_i$.
6. Split that local lift into a part perpendicular to $V_\infty$, the lift $L$ of the wing, and a part parallel to $V_\infty$ pointing back, the **{term}`induced drag`** $D_i$. The angle between the local lift and $L$ is again $\alpha_i$.
:::

:::{figure} figures/p32-downwash-vectors.svg
:label: fig-p32-downwash-vectors
:alt: Left: a velocity triangle that closes at a point on the chord line extended ahead of the airfoil. The free-stream arrow, numbered 1, points right along the horizontal to that point; from the upstream end of the local relative wind a short downward arrow, numbered 2, the downwash w, ends at the tail of the free stream; the local relative wind, numbered 3, runs from the top of the downwash arrow to the same point, tilted down from the free stream. At that point arcs mark alpha i between the free stream and the local relative wind and alpha eff between the local relative wind and the dashed chord line, both numbered 4, and on the far side of the point, between the chord line and a thin continuation of the free-stream direction, alpha, numbered 1. Right: above the airfoil at its quarter chord, the local lift arrow, numbered 5, leans back from the vertical; with dashed lines it closes a rectangle with a vertical lift arrow L and a short horizontal induced drag arrow D i pointing downstream, both numbered 6.
:width: 95%

Schematic drawn for worked example 3 ($C_L$ = 0.55, $\textit{AR}$ = 8, $e$ = 0.90), all angles drawn 12 times their size so they can be seen, forces drawn just above the section at its quarter chord. The wing works at $\alpha_\text{eff} = \alpha - \alpha_i$, and the backward part of its tilted lift is the induced drag.
:::

(p32-induced-drag)=
## Induced drag

Computing the exact magnitude of the induced angle requires lifting-line vortex theory, which you will derive in a later aerodynamics course; here we use the standard result. For a wing whose spanwise lift distribution is elliptical, the downwash is uniform along the span, and the induced angle of attack in radians is (Anderson 2016, Chapter 5)

$$
\alpha_i = \frac{C_L}{\pi\,\textit{AR}}
$$

where $\textit{AR} = b^2/S$ is the {term}`aspect ratio` of the wing ([wing geometry](#p13-wing-geometry)). Any other spanwise lift distribution gives more induced drag. We account for it with a **{term}`span efficiency factor`** $e$: 1 for the elliptic distribution, less than 1 for any other (NASA Glenn Research Center n.d.a). Strictly, $e$ belongs to the induced drag. On a wing that is not elliptic the induced angle varies along the span, and we use the same $e$ in $\alpha_i$ and in the lift slope $a$ as a close approximation. For a whole aircraft, where the fuselage and the tail also disturb the flow, the same factor is often called the Oswald efficiency factor. In degrees, with 57.3° per radian,

:::{math}
:label: eq-p32-alpha-i
\alpha_i = \frac{57.3\,C_L}{\pi e\,\textit{AR}}
:::

The induced drag follows from step 6 of the construction. It is the backward component of the local lift, $D_i = L_\text{local}\sin\alpha_i$, while the lift is $L = L_\text{local}\cos\alpha_i$, so $D_i = L\tan\alpha_i$. The induced angle is a few degrees at most, and for a small angle in radians $\tan\alpha_i \approx \alpha_i$:

$$
D_i \approx L\,\alpha_i
$$

We divide both sides by $qS$. Here $D_i/(qS)$ is the {term}`induced drag coefficient <induced drag>` $C_{D,i}$ and $L/(qS)$ is $C_L$:

$$
C_{D,i} = C_L\,\alpha_i
$$

Then we substitute $\alpha_i = C_L/(\pi e\,\textit{AR})$ in radians:

:::{math}
:label: eq-p32-cdi
C_{D,i} = \frac{C_L^2}{\pi e\,\textit{AR}}
:::

The induced drag coefficient grows with the square of the lift coefficient (NASA Glenn Research Center n.d.a). The drag coefficient of the wing is its airfoil's drag plus the induced drag:

:::{math}
:label: eq-p32-wing-cd
C_D = c_d + \frac{C_L^2}{\pi e\,\textit{AR}}
:::

Here $c_d$, the section drag read from the chart, is the drag of skin friction and pressure that the wing has even without tips. Read it at $c_l = C_L$: every section works at $\alpha_\text{eff}$, and there its lift coefficient equals the wing's. [Page 3.3](#p33-drag-kinds) adds the fuselage, tail, and other parts to it to build the drag of a whole aircraft.

Equation [](#eq-p32-cdi) shows two ways to lower induced drag at a given lift coefficient. The first is to increase the aspect ratio, which spreads the same lift over a longer span (NASA Glenn Research Center n.d.a). This is why sailplanes, which must lose as little energy as possible, have long, slender wings. The structural trade-off is a heavier, more flexible wing for the same load (FAA 2023, Chapter 5). The second is to shape the spanwise lift distribution closer to an ellipse, which raises $e$. Adding a {term}`winglet` at an airliner's wingtip also weakens the tip vortex and lowers induced drag in cruise (FAA 2014, Section 14).

:::{warning} Degrees or radians
$\alpha_i = C_L/(\pi e\,\textit{AR})$ is in radians; $\alpha_i = 57.3\,C_L/(\pi e\,\textit{AR})$ is in degrees. $C_{D,i} = C_L^2/(\pi e\,\textit{AR})$ has no 57.3, because it came from $C_L\,\alpha_i$ with $\alpha_i$ in radians. If you put the 57.3 in the wrong equation, the answer is 57.3 times too large or too small. In the slope equation [](#eq-p32-a), $a_0$ and $a$ are per degree. With slopes per radian the same equation has no 57.3: $a = a_0/(1 + a_0/(\pi e\,\textit{AR}))$.
:::

(p32-lift-curve)=
## The lift curve of a finite wing

The airfoil chart gives $c_l$ against the angle the section works at, but on a finite wing we set the geometric $\alpha$. We need the wing's own lift curve, $C_L$ against $\alpha$, and two facts fix it.

1. **Each geometric angle produces a smaller effective angle**, $\alpha_\text{eff} = \alpha - \alpha_i$, so at any given $\alpha$ the finite wing generates less lift than its two-dimensional airfoil, giving a flatter lift-curve slope.
2. **The zero-lift angle is the same.** At zero lift there is no downwash and $\alpha_i = 0$, so the wing's lift is zero at the airfoil's $\alpha_{L=0}$. The wing's line is the airfoil's line turned about the zero-lift point, with no shift to the right.

Now we derive the slope. The wing works like its airfoil at the effective angle, so on the straight part of the curve

$$
C_L = a_0\,(\alpha_\text{eff} - \alpha_{L=0})
$$

with $a_0$ the airfoil lift-curve slope per degree. We replace the effective angle by $\alpha - \alpha_i$ and the induced angle by [](#eq-p32-alpha-i), in degrees:

$$
C_L = a_0\left(\alpha - \frac{57.3\,C_L}{\pi e\,\textit{AR}} - \alpha_{L=0}\right)
$$

We multiply out and gather the terms with $C_L$ on the left:

$$
\begin{gathered}
C_L\left(1 + \frac{57.3\,a_0}{\pi e\,\textit{AR}}\right)\\
= a_0\,(\alpha - \alpha_{L=0})
\end{gathered}
$$

Dividing by the bracket gives the wing lift curve

:::{math}
:label: eq-p32-wing-cl
C_L = a\,(\alpha - \alpha_{L=0})
:::

with the finite-wing lift-curve slope

:::{math}
:label: eq-p32-a
a = \frac{a_0}{1 + \dfrac{57.3\,a_0}{\pi e\,\textit{AR}}}
:::

The bracket is larger than 1, so $a < a_0$. As $\textit{AR}$ grows, the bracket goes to 1 and the wing behaves like its airfoil (Anderson 2016, Chapter 5). These results come from lifting-line theory. They hold for a straight (unswept) wing of aspect ratio above about 4, at low Mach number, and below stall. Swept wings and wings of very low aspect ratio need other methods.

{numref}`fig-p32-lift-curves` draws the result for the wing of worked example 3. At the same $C_L$, the horizontal gap between the airfoil line and a wing line is the induced angle.

:::{figure} figures/p32-lift-curves.svg
:label: fig-p32-lift-curves
:alt: Lift coefficient against angle of attack from minus 6 to 10 degrees. The airfoil line, solid, through the measured NACA 64-3-618 points shown as squares, and two wing lines, dashed for aspect ratio 14 and dotted for aspect ratio 8, all start from the same zero-lift angle of about minus 3.7 degrees and fan out, each ending at 6 degrees; the lower the aspect ratio, the less steep the line. A measured point at about 8 degrees lies below the straight airfoil line, where the curve starts to bend. A horizontal line at C L equal to 0.55 meets the airfoil line at alpha equal to 1.08 degrees, the aspect-ratio-14 line at about 1.9 degrees, and the aspect-ratio-8 line at alpha equal to 2.48 degrees; a dimension above it marks the gap between the airfoil and the aspect-ratio-8 wing, alpha i equal to 1.39 degrees.
:width: 85%

Computed from [](#eq-p32-a) with the airfoil data of worked example 3 ($a_0$ = 0.115 per degree, $\alpha_{L=0}$ = −3.7°, $e$ = 0.90); squares: NACA Report 824 data at 6 million. Every curve has the same zero-lift angle; the lower the aspect ratio, the less steep the wing's curve. At $C_L$ = 0.55 the gap between the airfoil and the wing of aspect ratio 8 is $\alpha_i$.
:::

The straight line holds only below stall. A finite wing reaches a maximum lift coefficient $C_{L,\max}$ lower than its airfoil's $c_{l,\max}$. The lift and the downwash vary along a real span, so when the first sections reach their own $c_{l,\max}$ and stall, the rest of the span is still working below it.

:::{warning} Lowercase or uppercase
The chart's $c_l$ at the geometric angle is not the wing's $C_L$, and its $c_d$ is not the wing's $C_D$. To go from $c_l$, $c_d$, $a_0$ to $C_L$, $C_D$, $a$, use the corrections of [](#eq-p32-a) and [](#eq-p32-wing-cd). If you use the chart values for the wing, you overstate its lift and understate its drag.
:::

## From airfoil data to a finite wing

In worked example 3 we apply the full procedure from airfoil data to finite-wing performance, and then examine how increasing the aspect ratio changes the lift-to-drag ratio.

### Worked example 3: the wing of a seaplane

Consider a twin-engine seaplane flying short routes between islands, cruising at 48 m/s at 1,500 m. Its wing has a mean chord of 2.3 m, an aspect ratio of 8, a span efficiency factor $e$ = 0.90, and the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 section, and in cruise it requires $C_L$ = 0.55. Find the wing's lift-curve slope, angle of attack, induced and effective angles, drag coefficient, and $L/D$. Then repeat the calculation with the aspect ratio increased to 14 at the same wing area.

1. **Air at 1,500 m.** From the [standard atmosphere](../chapter-1/standard-atmosphere.md), $T = 278.41$ K and $\rho = 1.0580$ kg/m³; [Sutherland's law, page 3.1](#eq-p31-sutherland), gives $\mu = 1.742 \times {10}^{-5}$ kg/(m·s).
2. **Reynolds number**, based on the mean chord:
   $$
   \begin{aligned}
   \textit{Re} &= \frac{1.0580 \times 48 \times 2.3}{1.742 \times {10}^{-5}}\\
               &= 6.705 \times {10}^{6}
   \end{aligned}
   $$
   Use the 6 million curves of {numref}`fig-p32-airfoil-chart`.
3. **Airfoil lift-curve slope**, per degree, from two readings on the straight part: $c_l \approx 0.21$ at −2° and $c_l \approx 0.90$ at 4°, so
   $$
   \begin{aligned}
   a_0 &= \frac{0.90 - 0.21}{4 - (-2)}\\
       &= \frac{0.69}{6}\\
       &= 0.115
   \end{aligned}
   $$
   The zero-lift angle read from the chart is $\alpha_{L=0} \approx -3.7$°.
4. **Wing lift-curve slope**, per degree, [](#eq-p32-a), with $\pi e\,\textit{AR} = \pi \times 0.90 \times 8 = 22.62$:
   $$
   \begin{aligned}
   \frac{57.3\,a_0}{\pi e\,\textit{AR}} &= \frac{57.3 \times 0.115}{22.62}\\
                                        &= \frac{6.5895}{22.62}\\
       &= 0.2913\\
   a &= \frac{0.115}{1 + 0.2913}\\
     &= \frac{0.115}{1.2913}\\
     &= 0.08906
   \end{aligned}
   $$
5. **Angle of attack**, from [](#eq-p32-wing-cl):
   $$
   \begin{aligned}
   \alpha &= \frac{C_L}{a} + \alpha_{L=0}\\
          &= \frac{0.55}{0.08906} + (-3.7)\\
          &= 6.176 - 3.7\\
          &= 2.476°
   \end{aligned}
   $$
6. **Induced and effective angles**, [](#eq-p32-alpha-i):
   $$
   \begin{aligned}
   \alpha_i &= \frac{57.3 \times 0.55}{22.62}\\
            &= \frac{31.515}{22.62}\\
            &= 1.393°\\
   \alpha_\text{eff} &= 2.476 - 1.393\\
                     &= 1.083°
   \end{aligned}
   $$
   Check: the airfoil at the effective angle gives $a_0(\alpha_\text{eff} - \alpha_{L=0}) = 0.115 \times 4.783 = 0.5500$, the $C_L$ asked for.
7. **Drag coefficient.** We read the section drag at $c_l = C_L = 0.55$, as the [induced drag section](#p32-induced-drag) explains: $c_d \approx 0.0054$ on the 6 million curve. With [](#eq-p32-cdi) and [](#eq-p32-wing-cd):
   $$
   \begin{aligned}
   C_{D,i} &= \frac{{0.55}^{2}}{22.62}\\
           &= \frac{0.3025}{22.62}\\
           &= 0.01337\\
   C_D &= 0.0054 + 0.01337\\
       &= 0.01877
   \end{aligned}
   $$
8. **Lift-to-drag ratio:**
   $$
   \begin{aligned}
   \frac{L}{D} &= \frac{C_L}{C_D}\\
               &= \frac{0.55}{0.01877}\\
               &= 29.30
   \end{aligned}
   $$
   The airfoil alone would give $0.55/0.0054 = 101.9$. Here the induced drag is more than twice the section drag.
9. **The longer wing**, $\textit{AR}$ = 14. We keep the wing area, the weight, and the speed, so $C_L$ stays 0.55. The span grows and the mean chord shrinks to $2.3 \times \sqrt{8/14} = 1.739$ m, so the Reynolds number falls:
   $$
   \begin{aligned}
   \textit{Re} &= \frac{6.705 \times {10}^{6} \times 1.739}{2.3}\\
               &= 5.070 \times {10}^{6}
   \end{aligned}
   $$
   That lies between the 3 and 6 million curves, closer to 6 million, so we keep $c_d \approx 0.0054$. The 3 million curve gives 0.0060 at the same $c_l$, so the true section drag is a little higher and the $L/D$ below a little optimistic. Now, with the slope per degree and angles in degrees, $\pi e\,\textit{AR} = 39.58$ and
   $$
   \begin{aligned}
   \frac{57.3\,a_0}{\pi e\,\textit{AR}} &= \frac{6.5895}{39.58}\\
       &= 0.1665\\
   a &= \frac{0.115}{1 + 0.1665}\\
     &= \frac{0.115}{1.1665}\\
     &= 0.09859\\
   \alpha &= \frac{0.55}{0.09859} + (-3.7)\\
          &= 5.579 - 3.7\\
          &= 1.879°\\
   \alpha_i &= \frac{31.515}{39.58}\\
            &= 0.796°\\
   C_{D,i} &= \frac{0.3025}{39.58}\\
           &= 0.00764\\
   C_D &= 0.0054 + 0.00764\\
       &= 0.01304\\
   \frac{L}{D} &= \frac{0.55}{0.01304}\\
               &= 42.18
   \end{aligned}
   $$
   The effective angle of attack is again $1.879 - 0.796 = 1.083$°, because generating the same $C_L$ requires the same $\alpha_\text{eff}$ regardless of aspect ratio.

**Check and trade.** Increasing the aspect ratio from $\textit{AR}$ = 8 to 14 cuts the induced drag coefficient from 0.01337 to 0.00764, in the ratio 8/14, and raises $L/D$ from 29.30 to 42.18 ({numref}`fig-p32-induced-drag-ar`), while reducing the required angle of attack. The structural trade-off is a longer, heavier, and more flexible wing.

:::{figure} figures/p32-induced-drag-ar.svg
:label: fig-p32-induced-drag-ar
:alt: Drag coefficient against lift coefficient from minus 0.2 to 1.0. The airfoil section drag, a solid line, stays near 0.005 to 0.008 across the range. Two wing curves rise above it as parabolas: dotted for aspect ratio 8, which leaves the top of the plot at 0.04 near C L of 0.9, and dashed for aspect ratio 14, reaching about 0.03 at C L of 1.0. At C L equal to 0.55, dots labeled with their values mark the airfoil drag 0.0054, the aspect-ratio-14 wing 0.0130, and the aspect-ratio-8 wing 0.0188; a double arrow between the airfoil and the aspect-ratio-8 dots is labeled C D i equal to 0.0134.
:width: 85%

Computed from [](#eq-p32-wing-cd) for worked example 3 ($e$ = 0.90), with the section drag of the NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 at 6 million from NACA Report 824. The gap above the airfoil curve is the induced drag; it grows with $C_L^2$ and shrinks as the aspect ratio grows.
:::

## Summary

:::{important} Summary
- The angle of attack is measured from the free stream to the chord line. About the aerodynamic center, near $c/4$, the pitching moment does not change with $\alpha$; it is negative (nose down) for a cambered airfoil.
- Force and moment coefficients nondimensionalize aerodynamic loads by $qS$ (and $c$ for moments): $L = qSC_L$, $D = qSC_D$, $M = qScC_M$, isolating the effects of geometry, $\alpha$, $\textit{Re}$, and $M$. Airfoil data ($c_l$, $c_d$, $c_m$) represent a two-dimensional infinite wing.
- Read a chart on the curve of the closest Reynolds number: $c_l$ and $c_{m,c/4}$ at $\alpha$, then $c_d$ at that $c_l$.
- Wingtip vortices induce downwash. The wing works at $\alpha_\text{eff} = \alpha - \alpha_i$, and the backward tilt of its lift is the induced drag, $C_{D,i} = C_L^2/(\pi e\,\textit{AR})$. Its lift curve keeps the zero-lift angle and has the smaller slope $a$.
:::

:::{table} The equations of this page.
:label: tbl-p32-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Dynamic pressure | $q = \tfrac12 \rho V_\infty^2$ |
| Lift, drag, and moment of a wing | $L = qSC_L$, $D = qSC_D$, $M = qScC_M$ |
| Per unit span of an airfoil | $L' = qc\,c_l$, $D' = qc\,c_d$, $M' = qc^2 c_m$ |
| Center of pressure | $x_\text{cp}/c = 1/4 - c_{m,c/4}/c_l$ |
| Reynolds number (chord) | $\textit{Re} = \rho V c/\mu$ |
| Airfoil lift curve | $c_l = a_0(\alpha - \alpha_{L=0})$ |
| Induced angle of attack, degrees | $\alpha_i = 57.3\,C_L/(\pi e\,\textit{AR})$ |
| Effective angle of attack | $\alpha_\text{eff} = \alpha - \alpha_i$ |
| Induced drag coefficient | $C_{D,i} = C_L^2/(\pi e\,\textit{AR})$ |
| Wing drag coefficient | $C_D = c_d + C_L^2/(\pi e\,\textit{AR})$ |
| Wing lift-curve slope, per degree | $a = a_0/(1 + 57.3\,a_0/(\pi e\,\textit{AR}))$ |
| Wing lift curve | $C_L = a(\alpha - \alpha_{L=0})$ |

:::

:::{exercise} For discussion
:label: ex-p32-discussion

1. A pilot holds the nose 5° above the horizon. Can the wing be at a negative angle of attack? Describe a flight condition where it is.
2. The NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 is designed for low drag between $c_l$ of 0.3 and 0.9 (the measured bucket at 6 million is a little wider). What would happen to the bucket if the wing were covered with insects or raindrops, and why might a designer still choose a four-digit section?
3. Why does the induced drag of an airplane matter most at takeoff and landing and at high altitude, and least in a fast dive?
4. Two wings have the same area and airfoil, one with $\textit{AR}$ = 6 and one with $\textit{AR}$ = 12. Sketch their lift curves and drag curves on one pair of axes. What does a designer gain and lose with the second?
5. Geese often fly in a V formation, each bird a little outboard of the one ahead. Using the upwash outside a wing tip, explain what a bird gains from that place.
:::

## Quiz

:::{iframe} ../quickcheck/quiz-3-2.html
:label: quiz-3-2
:enumerated: false
:width: 100%

Quiz for Standard 3.2: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Abbott, I. H., A. E. von Doenhoff, and L. S. Stivers, Jr., "[Summary of Airfoil Data](https://ntrs.nasa.gov/citations/19930090976)," NACA Report 824, National Advisory Committee for Aeronautics, 1945.
- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016.
- Federal Aviation Administration (FAA), *[Aircraft Wake Turbulence](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_90-23G.pdf)*, Advisory Circular AC 90-23G, 2014.
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023. Chapter 5, "Aerodynamics of Flight."
- NASA Glenn Research Center, "[Induced Drag Coefficient](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/induced-drag-coefficient/)," Beginner's Guide to Aeronautics, n.d.a.
- NASA Glenn Research Center, "[What is Lift?](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/what-is-lift/)," Beginner's Guide to Aeronautics, n.d.b.
