---
title: "5.3 Climb and Ceiling"
short_title: 5.3 Climb and Ceiling
---

:::{include} ../_parts/standards/5.3.md
:::

Level flight uses only enough thrust to match drag. To climb, the engines must supply **more** thrust and more power than level flight requires, using the surplus to lift the aircraft against gravity. We ask two climb questions in design and operations: how **fast** an aircraft gains altitude ({term}`rate of climb`), and how **steeply** it rises over the ground ({term}`flight-path angle`). Steepness matters most right after takeoff when an engine fails near terrain. As altitude increases and engine output drops, that surplus vanishes and sets the aircraft's ceiling.

:::{note} What to take from this page
- In a steady climb at flight-path angle $\gamma$, $T = D + mg\sin\gamma$ and $L = mg\cos\gamma$. For shallow climbs ($\cos\gamma \approx 1$), $L \approx mg$ and $D \approx T_R$.
- {term}`Rate of climb` is $R/C = V\sin\gamma = (P_A - P_R)/(mg)$, so it depends on {term}`excess power` $P_A - P_R$.
- Climb angle follows $\sin\gamma = (T_A - D)/(mg)$, so it depends on **excess thrust** $T_A - T_R$. For a jet, steepest climb occurs at $V_{T_R,\min}$, while fastest climb occurs faster.
- To clear an obstacle of height $h_{\text{obs}}$ at horizontal distance $d_{\text{obs}}$, an aircraft needs $\gamma > \arctan(h_{\text{obs}}/d_{\text{obs}})$, which maximizes climb **angle**, not climb rate.
- The {term}`absolute ceiling` is the altitude where $(R/C)_{\max} = 0$ ($T_A = T_{R,\min}$ for a jet, $P_A = P_{R,\min}$ for a propeller). The {term}`service ceiling` is where $(R/C)_{\max} = 0.5$ m/s ($100$ ft/min).
:::

(p53-climb-equations)=
## Steady climbing flight

We picture an aircraft climbing along a straight path inclined at the **flight-path angle** $\gamma$ above the horizontal ({numref}`fig-p53-climb-fbd`). Lift $L$ remains perpendicular to the flight path and drag $D$ acts backward along it, while weight $mg$ still points straight down toward Earth's center. Resolving weight along and perpendicular to the flight path puts a backward component $mg\sin\gamma$ along the drag line and a downward component $mg\cos\gamma$ opposing lift.

:::{figure} figures/p53-climb-fbd.svg
:label: fig-p53-climb-fbd
:alt: Side view of an aircraft climbing to the right at flight-path angle gamma above a thin horizontal line, with a blue velocity triangle on the right. Four thick black force arrows act at the center of gravity: thrust T forward along the flight path, drag D backward along it, lift L perpendicular to the flight path, and weight mg straight down. Gray dashed construction lines resolve weight into mg sin gamma backward along the flight path and mg cos gamma perpendicular to it. The blue velocity triangle shows airspeed V along the hypotenuse at angle gamma, horizontal component V cos gamma, and vertical component R over C equals V sin gamma.
:width: 90%

Force balance and velocity triangle in a steady climb at flight-path angle $\gamma$. Weight contributes a backward component $mg\sin\gamma$ that thrust must overcome in addition to drag.
:::

If the thrust vector lies nearly along the flight path and the climb is steady (zero acceleration), we get two force balances:

:::{math}
:label: eq-p53-climb-forces
\begin{aligned}
T_A &= D + mg\sin\gamma\\
L &= mg\cos\gamma
\end{aligned}
:::

Solving the first equation for $\sin\gamma$ gives the **climb angle**. From the velocity triangle in {numref}`fig-p53-climb-fbd`, the vertical climb speed is $R/C = V\sin\gamma$, which turns excess thrust $(T_A - D)$ into **excess power** $(P_A - P_R)$:

::::{prf:definition} Climb angle and rate of climb
:label: def-p53-climb
:::{math}
:label: eq-p53-gamma-rc
\begin{aligned}
\sin\gamma &= \frac{T_A - D}{mg}\\
R/C &= V\sin\gamma = \frac{T_A V - D V}{mg} = \frac{P_A - P_R}{mg}
\end{aligned}
:::
::::

For civil transport and general-aviation aircraft, climb angles are typically shallow (under about ${15}^\circ$, where $\cos\gamma > 0.966$). In that shallow-climb approximation we take $\cos\gamma \approx 1$, which makes $L \approx mg$ and lets us read $D$ and $P_R$ straight from the level-flight curves $T_R(V)$ and $P_R(V)$ of [page 5.1](thrust-and-power.md).

(p53-excess-power)=
## Excess power, steepest climb, and fastest climb

Look at [](#eq-p53-gamma-rc) on the power curve ({numref}`fig-p53-excess-power`). At any airspeed $V$, the vertical distance between the $P_A$ curve and the $P_R$ curve is the excess power $P_A - P_R$. When you divide that gap by $mg$, you get the rate of climb at that speed.

:::{figure} figures/p53-excess-power.svg
:label: fig-p53-excess-power
:alt: Plot of power in megawatts against true airspeed from 60 to 270 meters per second for the executive twin-jet at sea level. A dashed blue straight line P sub A equals T sub A times V rises from 3.7 to 14.9 megawatts above the solid black U-shaped P sub R curve, with the excess-power region between them shaded beige. A double-headed vertical black arrow at 156.6 meters per second marks the widest vertical gap, labeled largest excess power: maximum rate of climb equals 15.32 meters per second at 156.6 meters per second. Farther left, an open square on P sub R with a vertical dashed line marks V sub gamma max equals V sub T R min equals 104.8 meters per second.
:width: 80%

Excess power $P_A - P_R$ (shaded) for the executive twin-jet at sea level. Maximum rate of climb occurs where the vertical gap between $P_A$ and $P_R$ is widest ($156.6$ m/s), well above the steepest-climb speed ($104.8$ m/s).
:::

Two distinct optimal climb speeds follow from these relations, and pilots give each its own name (FAA 2023, Chapter 11):

- **Best-angle-of-climb speed ($V_x$, or $V_{\gamma,\max}$)** maximizes $\sin\gamma = (T_A - T_R)/(mg)$, giving the most altitude gained per unit of **horizontal distance**.
  - For a **jet**, $T_A$ is flat with speed, so $T_A - T_R$ is largest where $T_R$ is smallest, at $V_{T_R,\min}$:
    :::{math}
    :label: eq-p53-jet-gammax
    \sin\gamma_{\max} = \frac{T_A}{mg} - \frac{1}{(L/D)_{\max}} = \frac{T_A}{mg} - 2\sqrt{K C_{D,0}}
    :::
  - For a **propeller aircraft**, $T_A = P_A/V$ rises steeply as speed decreases, boosting excess thrust $T_A - T_R$ until induced drag catches up near stall, so $\gamma_{\max}$ occurs even slower than $V_{P_R,\min}$.
- **Best-rate-of-climb speed ($V_y$, or $V_{R/C,\max}$)** maximizes $R/C = (P_A - P_R)/(mg)$, giving the most altitude gained per unit of **time**.
  - For a **propeller aircraft**, $P_A$ is flat with speed, so $P_A - P_R$ is widest right where $P_R$ is smallest, at $V_{P_R,\min}$:
    :::{math}
    :label: eq-p53-prop-rcmax
    (R/C)_{\max} = \frac{P_A - P_{R,\min}}{mg}
    :::
  - For a **jet**, $P_A = T_A V$ slopes upward with speed, so the widest vertical gap $(P_A - P_R)$ occurs where the slope of $P_R(V)$ matches $T_A$, well to the right of $V_{T_R,\min}$ ({numref}`fig-p53-excess-power`).

{numref}`fig-p53-climb-angle-and-roc` plots $\gamma(V)$ and $R/C(V)$ side by side for the executive twin-jet at sea level with both engines running and with one engine inoperative (OEI). Losing half the thrust reduces climb performance by much more than half, because drag stays the same while available thrust drops by $50\%$. Here the steepest climb angle drops from ${6.69}^\circ$ to ${1.77}^\circ$ and maximum climb rate drops from $15.32$ m/s to $3.46$ m/s.

:::{figure} figures/p53-climb-angle-and-roc.svg
:label: fig-p53-climb-angle-and-roc
:alt: Two panels side by side for the executive twin-jet at sea level, comparing two engines (solid black) and one engine inoperative (dashed blue) across airspeed from 70 to 265 meters per second. Panel 1, titled climb angle, shows two-engine gamma peaking at 6.69 degrees at 104.8 meters per second and one-engine gamma peaking at 1.77 degrees at the same speed. Panel 2, titled rate of climb, shows two-engine R over C peaking at 15.32 meters per second at 156.6 meters per second and one-engine R over C peaking at 3.46 meters per second near 119 meters per second. A thin gray line marks zero climb in both panels.
:width: 85%

Climb angle (Panel 1) and rate of climb (Panel 2) for the executive twin-jet at sea level with two engines and with one engine out. Losing one of two engines eliminates $77\%$ of the peak climb rate, because excess thrust drops far faster than total thrust.
:::

:::{warning} Check the units of $\gamma_{\max}$
In [](#eq-p53-jet-gammax), every term is dimensionless: $T_A/(mg)$ is thrust divided by weight, and $2\sqrt{K C_{D,0}} = 1/(L/D)_{\max}$ is drag divided by lift. If you forget to divide $T_A$ by $mg$, you get a force in newtons instead of $\sin\gamma$.
:::

### Worked example 1: sea-level climb of a twin-jet

We find the rate of climb and flight-path angle of the executive twin-jet of [page 5.1](thrust-and-power.md) ($m = 33{,}100$ kg, $mg = 324{,}711$ N, $S = 88.2$ m², $C_{D,0} = 0.015$, $K = 0.050$, $T_A = 55{,}620$ N with both engines at sea level) climbing at $V = 125$ m/s.

1. **Parasite drag, induced drag, and total drag** from [](#eq-p51-TR) at $\rho = 1.2250$ kg/m³:
   $$
   \begin{aligned}
   D_0 &= 0.5 \times 1.2250 \times {125}^{2} \times 88.2 \times 0.015\\
       &= 12{,}662\ \text{N}\\
   D_i &= \frac{2 \times 0.050 \times {324{,}711}^{2}}{1.2250 \times 88.2 \times {125}^{2}}\\
       &= 6{,}245.5\ \text{N}\\
   D &= 12{,}662 + 6{,}245.5\\
     &= 18{,}908\ \text{N}
   \end{aligned}
   $$
2. **Power available, power required, and rate of climb**, [](#eq-p53-gamma-rc):
   $$
   \begin{aligned}
   P_A &= 55{,}620 \times 125\\
       &= 6{,}952{,}500\ \text{W}\\
       &= 6{,}953\ \text{kW}\\
   P_R &= 18{,}908 \times 125\\
       &= 2{,}363{,}500\ \text{W}\\
       &= 2{,}364\ \text{kW}\\
   R/C &= \frac{(6{,}953 - 2{,}364) \times 1{,}000}{324{,}711}\\
       &= 14.13\ \text{m/s}
   \end{aligned}
   $$
3. **Flight-path angle:**
   $$
   \begin{aligned}
   \sin\gamma &= \frac{14.13}{125}\\
              &= 0.1130\\
   \gamma &= {6.49}^\circ
   \end{aligned}
   $$

**Check.** Because $\cos({6.49}^\circ) = 0.9936$, the shallow-climb approximation $L \approx mg$ is accurate to better than $1\%$. Because $125$ m/s lies between $V_{\gamma,\max} = 104.8$ m/s and $V_{R/C,\max} = 156.6$ m/s, both $14.13$ m/s and ${6.49}^\circ$ fall slightly below their respective peaks of $15.32$ m/s and ${6.69}^\circ$ ({numref}`fig-p53-climb-angle-and-roc`).

(p53-obstacle-clearance)=
## Obstacle clearance with one engine out

Now we look at a safety-critical climb test. Suppose an aircraft lifts off at sea level and loses one engine, with a hill, mast, or building of height $h_{\text{obs}}$ standing at horizontal distance $d_{\text{obs}}$ ahead. Clearing the obstacle requires a climb angle larger than the line-of-sight angle to the top of the obstacle:

:::{math}
:label: eq-p53-obstacle
\gamma > \gamma_{\text{req}} = \arctan\!\left(\frac{h_{\text{obs}}}{d_{\text{obs}}}\right), \qquad \Delta h = d_{\text{obs}}\tan\gamma > h_{\text{obs}}
:::

Because obstacle clearance depends on altitude gained per horizontal meter, the pilot must fly at the **best-angle** speed $V_{\gamma,\max}$, not the faster best-rate speed. {numref}`fig-p53-obstacle-clearance` shows why: climbing faster raises the vertical speed in m/s, yet the aircraft covers ground so much more quickly that it arrives at the obstacle lower down.

:::{figure} figures/p53-obstacle-clearance.svg
:label: fig-p53-obstacle-clearance
:alt: Side-view climb trajectory showing height gained in meters against horizontal distance from liftoff up to 3,500 meters, with a hatched obstacle 75 meters tall at 3,000 meters. The solid black line labeled steepest climb, gamma max equals 1.77 degrees rises above the obstacle and passes through a black dot labeled clears at 92.7 meters. A dotted orange line labeled faster climb (145 meters per second), gamma equals 1.08 degrees runs lower and strikes the obstacle at an open orange square at 56.7 meters.
:width: 80%

One-engine-inoperative obstacle clearance for the executive twin-jet of worked example 2. Flying at steepest-climb speed ($104.8$ m/s, $\gamma_{\max} = {1.77}^\circ$) clears the $75$ m obstacle at $92.7$ m; flying faster at $145$ m/s lowers the path to $56.7$ m and strikes it.
:::

### Worked example 2: one-engine-out obstacle clearance for the twin-jet

Right after sea-level liftoff, the executive twin-jet loses one engine ($n = 1$, $T_A = 27{,}810$ N). A $75$ m hill stands $3{,}000$ m beyond liftoff. We check whether the jet clears the hill.

1. **Required climb angle**, [](#eq-p53-obstacle):
   $$
   \begin{aligned}
   \gamma_{\text{req}} &= \arctan\!\left(\frac{75}{3{,}000}\right)\\
                       &= {1.43}^\circ
   \end{aligned}
   $$
2. **Maximum one-engine climb angle**, [](#eq-p53-jet-gammax), at $V_{\gamma,\max} = V_{T_R,\min} = 104.8$ m/s:
   $$
   \begin{aligned}
   \frac{T_A}{mg} &= \frac{27{,}810}{324{,}711}\\
                  &= 0.08565\\
   2\sqrt{K C_{D,0}} &= 2\sqrt{0.050 \times 0.015}\\
                     &= 0.05477\\
   \sin\gamma_{\max} &= 0.08565 - 0.05477\\
                     &= 0.03088\\
   \gamma_{\max} &= {1.77}^\circ
   \end{aligned}
   $$
3. **Height at $3{,}000$ m:**
   $$
   \begin{aligned}
   \Delta h &= 3{,}000 \tan({1.77}^\circ)\\
            &= 92.7\ \text{m}
   \end{aligned}
   $$

**Verdict.** The jet clears the hill because ${1.77}^\circ > {1.43}^\circ$; it crosses $3{,}000$ m at $92.7$ m, clearing the $75$ m hill by $17.7$ m. Notice what happens if the pilot instead speeds up to $145$ m/s (closer to the OEI best-rate speed). Climb angle drops to ${1.08}^\circ$, height at $3{,}000$ m falls to $56.7$ m, and the aircraft strikes the hill ({numref}`fig-p53-obstacle-clearance`).

(p53-ceilings)=
## Service ceiling and absolute ceiling

As an aircraft climbs, available thrust and power fall as $(\rho/\rho_0)^{m_{\text{ad}}}$, so $(R/C)_{\max}$ steadily declines toward zero (Anderson 2016, Section 6.9):

- The **{term}`absolute ceiling`** is the altitude where $(R/C)_{\max} = 0$. At that altitude, $T_A = T_{R,\min}$ (equivalently $P_A = P_{R,\min}$), leaving zero excess power and only one possible level-flight speed. An aircraft would take infinite time to reach it.
- The **{term}`service ceiling`** is the practical operational limit, defined as the altitude where $(R/C)_{\max} = 0.5$ m/s (about $100$ ft/min). For jet transports, aviation regulations also use a cruise-climb criterion of $1.5$ m/s ($300$ ft/min).

We can find ceilings in two ways ({numref}`fig-p53-ceiling-plot`):

1. **Analytical absolute ceiling.** Set available output equal to minimum required output and solve for the ceiling air density $\rho_c$, then invert the standard atmosphere of [page 1.4](../chapter-1/standard-atmosphere.md) for altitude $h$:
   - **Jet** ($T_A = T_{R,\min}$, constant with altitude):
     :::{math}
     :label: eq-p53-ceil-jet
     n\,T_0\left(\frac{\rho_c}{\rho_0}\right)^{m_{\text{ad}}} = T_{R,\min} = 2mg\sqrt{K C_{D,0}}
     :::
   - **Propeller** ($P_A = P_{R,\min}$, where $P_{R,\min} = P_{R,\min,\text{SL}}\sqrt{\rho_0/\rho_c}$ rises with altitude; multiplying both sides by $(\rho_c/\rho_0)^{1/2}$ combines the density ratios):
     :::{math}
     :label: eq-p53-ceil-prop
     n\,\eta\,P_0\left(\frac{\rho_c}{\rho_0}\right)^{m_{\text{ad}}} = P_{R,\min,\text{SL}}\left(\frac{\rho_0}{\rho_c}\right)^{1/2} \quad \Longrightarrow \quad \left(\frac{\rho_c}{\rho_0}\right)^{m_{\text{ad}} + 1/2} = \frac{P_{R,\min,\text{SL}}}{n\,\eta\,P_0}
     :::
2. **Graphical ceiling (both service and absolute).** Compute $(R/C)_{\max}$ at several altitudes and plot altitude $h$ against $(R/C)_{\max}$. You read off the service ceiling at $R/C = 0.5$ m/s and the absolute ceiling where the curve reaches $R/C = 0$.

:::{figure} figures/p53-ceiling-plot.svg
:label: fig-p53-ceiling-plot
:alt: Two panels side by side. Panel 1, titled jet ceilings from maximum rate of climb, plots altitude h from 0 to 17 kilometers against maximum rate of climb from 0 to 18 meters per second for the executive twin-jet: a solid black curve through six open circles drops from 15.32 meters per second at sea level to a blue square at 0.5 meters per second (service ceiling 14.99 kilometers) and a black diamond at 0 meters per second (absolute ceiling 15.35 kilometers). Panel 2, titled propeller: P sub A meets minimum P sub R, plots power in kilowatts against altitude from 0 to 12 kilometers for the twin-turboprop of worked example 4: a dashed blue maximum P sub A curve falls from 1,863 kilowatts while a solid black minimum P sub R curve rises from 417 kilowatts; they cross at a black diamond labeled ceiling, 10.16 kilometers.
:width: 85%

Computed for the executive jet of worked example 3 (Panel 1) and the twin-turboprop of worked example 4 (Panel 2). Both views locate the ceiling where excess power shrinks to $0.5$ m/s (service ceiling, $14.99$ km for the jet) or zero (absolute ceiling, $15.35$ km for the jet and $10.16$ km for the turboprop where falling $P_{A,\max}$ meets rising $P_{R,\min}$).
:::

### Worked example 3: absolute and service ceilings of the twin-jet

We find the absolute ceiling of the executive twin-jet analytically, then use the $(R/C)_{\max}$ table below to find its service ceiling and check the absolute ceiling graphically.

1. **Analytical absolute ceiling**, [](#eq-p53-ceil-jet):
   $$
   \begin{aligned}
   \left(\frac{\rho_c}{\rho_0}\right)^{0.6} &= \frac{T_{R,\min}}{n\,T_0}\\
                                            &= \frac{17{,}785}{55{,}620}\\
                                            &= 0.3198\\
   \rho_c &= 1.2250 \times {0.3198}^{1/0.6}\\
          &= 0.1832\ \text{kg/m}^3
   \end{aligned}
   $$
   Because $\rho_c = 0.1832$ kg/m³ is smaller than the tropopause density ($0.3636$ kg/m³ at $11{,}000$ m), the ceiling lies in the isothermal lower {term}`stratosphere` ($T_1 = 216.66$ K, [page 1.4](../chapter-1/standard-atmosphere.md)). Inverting $\rho_c = \rho_{11}\exp[-g(h - 11{,}000)/(R T_1)]$ gives
   $$
   \begin{aligned}
   h_{\text{abs}} &= 11{,}000 - \frac{287 \times 216.66}{9.81}\ln\frac{0.1832}{0.3636}\\
                  &= 15{,}347\ \text{m}\\
                  &= 15.35\ \text{km}
   \end{aligned}
   $$
2. **Graphical service and absolute ceilings** from $(R/C)_{\max}$ evaluated at six altitudes ({numref}`tbl-p53-jet-ceil` and Panel 1 of {numref}`fig-p53-ceiling-plot`):

:::{table} Maximum rate of climb of the executive twin-jet at six altitudes.
:label: tbl-p53-jet-ceil
:align: center

| Altitude $h$, m | 0 | 4,000 | 8,000 | 11,000 | 13,000 | 14,500 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Maximum rate of climb $(R/C)_{\max}$, m/s | 15.32 | 12.04 | 8.56 | 5.70 | 3.16 | 1.17 |

:::

Linearly extrapolating through the top two points ($13{,}000$ m at $3.16$ m/s and $14{,}500$ m at $1.17$ m/s) has slope $(14{,}500 - 13{,}000)/(1.17 - 3.16) = -753.8$ m/(m/s), which gives:

- **Service ceiling** ($R/C = 0.50$ m/s): $14{,}500 + 753.8 \times (1.17 - 0.50) = 15{,}005$ m (exact curve: $14.99$ km).
- **Absolute ceiling** ($R/C = 0$): $14{,}500 + 753.8 \times 1.17 = 15{,}382$ m (within $35$ m of the exact analytical value $15{,}347$ m).

### Worked example 4: climb, one-engine-out check, and ceiling of a twin-turboprop

Consider a twin-turboprop survey aircraft with mass $m = 11{,}200$ kg ($mg = 109{,}872$ N), wing area $S = 44.0$ m², $C_{D,0} = 0.024$, $K = 0.038$, and two engines rated at $P_0 = 1{,}150$ kW each with $\eta = 0.81$ and $m_{\text{ad}} = 0.85$. Find: (a) its sea-level $(R/C)_{\max}$ with both engines, (b) whether it clears a $150$ m radio mast at $2{,}400$ m horizontal distance when climbing at $V = 75$ m/s with one engine out, and (c) its two-engine analytical absolute ceiling.

1. **Sea-level power available:**
   - Both engines: $P_{A,2} = 2 \times 0.81 \times 1{,}150 = 1{,}863$ kW.
   - One engine: $P_{A,1} = 0.81 \times 1{,}150 = 931.5$ kW.
2. **Sea-level $(R/C)_{\max}$**, [](#eq-p53-prop-rcmax). From [](#eq-p51-min-power), $V_{P_R,\min} = 54.42$ m/s and $P_{R,\min} = 417.0$ kW:
   $$
   \begin{aligned}
   (R/C)_{\max} &= \frac{(1{,}863 - 417.0) \times 1{,}000}{109{,}872}\\
                &= 13.16\ \text{m/s}
   \end{aligned}
   $$
3. **One-engine-out climb at $V = 75$ m/s** against the $150$ m mast at $2{,}400$ m ($\gamma_{\text{req}} = \arctan(150/2{,}400) = {3.58}^\circ$):
   $$
   \begin{aligned}
   T_{A,1} &= \frac{931{,}500}{75}\\
           &= 12{,}420\ \text{N}\\
   D_0 &= 0.5 \times 1.2250 \times {75}^{2} \times 44.0 \times 0.024\\
       &= 3{,}638\ \text{N}\\
   D_i &= \frac{2 \times 0.038 \times {109{,}872}^{2}}{1.2250 \times 44.0 \times {75}^{2}}\\
       &= 3{,}026\ \text{N}\\
   D &= 3{,}638 + 3{,}026\\
     &= 6{,}664\ \text{N}\\
   \sin\gamma &= \frac{12{,}420 - 6{,}664}{109{,}872}\\
              &= 0.05239\\
   \gamma &= {3.00}^\circ\\
   \Delta h &= 2{,}400 \tan({3.00}^\circ)\\
            &= 125.8\ \text{m}
   \end{aligned}
   $$
   **Verdict.** At $75$ m/s the aircraft reaches only $125.8$ m at the mast and does **not** clear $150$ m (${3.00}^\circ < {3.58}^\circ$). To clear it, the pilot must slow toward the best-angle speed (closer to $V_{P_R,\min}$, where $T_{A,1} = P_{A,1}/V$ is much larger) or reduce takeoff weight.
4. **Two-engine analytical absolute ceiling**, [](#eq-p53-ceil-prop), with exponent $m_{\text{ad}} + 0.5 = 0.85 + 0.5 = 1.35$:
   $$
   \begin{aligned}
   \left(\frac{\rho_c}{\rho_0}\right)^{1.35} &= \frac{417.0}{1{,}863}\\
                                             &= 0.2238\\
   \rho_c &= 1.2250 \times {0.2238}^{1/1.35}\\
          &= 0.4042\ \text{kg/m}^3
   \end{aligned}
   $$
   Because $0.4042 > 0.3636$ kg/m³, this density lies inside the {term}`troposphere`. Inverting the tropospheric density formula from [page 1.4](../chapter-1/standard-atmosphere.md), $\rho/\rho_0 = (1 - 0.0065\,h/288.16)^{4.2586}$, gives $h_{\text{abs}} = 10{,}162$ m $= 10.16$ km, where $P_{A,2}$ and $P_{R,\min}$ meet at $726.0$ kW (Panel 2 of {numref}`fig-p53-ceiling-plot`).

## Summary

:::{important} Summary
- Steady climbing flight balances $T_A = D + mg\sin\gamma$ and $L = mg\cos\gamma$; for shallow climbs, $L \approx mg$ and $D \approx T_R$.
- Excess thrust governs climb angle, $\sin\gamma = (T_A - D)/(mg)$, while excess power governs rate of climb, $R/C = (P_A - P_R)/(mg)$.
- For a jet, $\sin\gamma_{\max} = T_A/(mg) - 2\sqrt{K C_{D,0}}$ occurs at $V_{T_R,\min}$, while $(R/C)_{\max}$ occurs faster. For a propeller aircraft, $(R/C)_{\max} = (P_A - P_{R,\min})/(mg)$ occurs at $V_{P_R,\min}$, while $\gamma_{\max}$ occurs slower.
- Obstacle clearance checks $\gamma > \arctan(h_{\text{obs}}/d_{\text{obs}})$, so best-angle speed (not best-rate speed) maximizes clearance.
- Absolute ceiling is where $(R/C)_{\max} = 0$ ($T_A = T_{R,\min}$ for a jet, $P_A = P_{R,\min}$ for a propeller); service ceiling is where $(R/C)_{\max} = 0.5$ m/s.
:::

:::{table} The equations of this page.
:label: tbl-p53-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Climb force balance | $T_A = D + mg\sin\gamma$, $L = mg\cos\gamma$ |
| Climb angle | $\sin\gamma = (T_A - D)/(mg)$ |
| Rate of climb | $R/C = V\sin\gamma = (P_A - P_R)/(mg)$ |
| Jet steepest climb angle | $\sin\gamma_{\max} = T_A/(mg) - 2\sqrt{K C_{D,0}}$ (at $V_{T_R,\min}$) |
| Propeller max rate of climb | $(R/C)_{\max} = (P_A - P_{R,\min})/(mg)$ (at $V_{P_R,\min}$) |
| Obstacle clearance condition | $\gamma > \arctan(h_{\text{obs}}/d_{\text{obs}})$, $\Delta h = d_{\text{obs}}\tan\gamma$ |
| Jet absolute ceiling | $n\,T_0(\rho_c/\rho_0)^{m_{\text{ad}}} = 2mg\sqrt{K C_{D,0}}$ |
| Propeller absolute ceiling | $(\rho_c/\rho_0)^{m_{\text{ad}}+1/2} = P_{R,\min,\text{SL}}/(n\,\eta\,P_0)$ |

:::

:::{exercise} For discussion
:label: ex-p53-discussion

1. Why does losing one engine on a twin-engine aircraft reduce the rate of climb by much more than $50\%$?
2. After takeoff from an airport surrounded by hills, a pilot wants the greatest height margin over a ridge $2$ km ahead. Should the pilot climb at best-angle speed $V_x$ or best-rate speed $V_y$, and why?
3. Why does the exponent on $\rho_c/\rho_0$ equal $m_{\text{ad}}$ in the jet ceiling equation, but $m_{\text{ad}} + 1/2$ in the propeller ceiling equation?
4. How does a hot summer day (higher density altitude) affect an aircraft's rate of climb and obstacle-clearance margin on takeoff?
5. Why can an aircraft never reach its absolute ceiling in a finite flight?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-5-3.html
:label: quiz-5-3
:width: 100%
:enumerated: false

Quiz for Standard 5.3: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 6, Sections 6.7 to 6.10.
- Anderson, J. D., Jr., *Aircraft Performance and Design*, McGraw-Hill, 1999. Chapter 5, Sections 5.6 to 5.8.
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023. Chapter 11, "Aircraft Performance."
