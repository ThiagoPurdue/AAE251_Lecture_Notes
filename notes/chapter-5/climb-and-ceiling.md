---
title: "5.3 Climb and Ceiling"
short_title: 5.3 Climb and Ceiling
---

:::{include} ../_parts/standards/5.3.md
:::

On [page 5.1](#p51-level-flight), we analyzed steady, level flight, where engine thrust just balances aerodynamic drag. In real operations, an airplane also has to climb away from the runway, clear nearby obstacles, and reach its cruise altitude, all of which require more thrust and power than level flight alone. In climb performance, we track two distinct quantities: how fast the aircraft gains altitude (rate of climb) and how steeply it climbs relative to the ground (climb angle). Because those two quantities peak at different airspeeds, knowing which speed to fly is especially important when clearing terrain after an engine failure. As altitude increases, thinner air reduces engine output until no excess power remains, which defines the aircraft's ceiling.

:::{note} What to take from this page
- In a steady climb at the climb angle $\gamma$, $T = D + mg\sin\gamma$ and $L = mg\cos\gamma$. The thrust must carry the drag and the part of the weight along the path.
- The climb angle comes from the excess thrust, $\sin\gamma = (T_A - D)/(mg)$, and the {term}`rate of climb` from the {term}`excess power`, $R/C = (P_A - P_R)/(mg)$. They peak at different speeds.
- The {term}`absolute ceiling` is where the maximum rate of climb falls to zero, and the {term}`service ceiling` where it falls to 0.5 m/s.
- To clear an obstacle with one engine out, the aircraft needs a climb angle larger than the angle to the top of the obstacle, so it flies its steepest climb.
:::

(p53-climb-equations)=
## Steady climbing flight

We start, as on page 5.1, with the forces. In a **steady climb** the aircraft moves along a straight path at a constant speed, so the forces on it are in balance. The path now points up, at the {term}`flight-path angle` $\gamma$ above the horizontal. In a climb it is also called the climb angle. {numref}`fig-p53-climb-forces` shows the four forces.

:::{figure} figures/p53-climb-forces.svg
:label: fig-p53-climb-forces
:alt: A Boeing 737-800 outline climbing to the right, with its flight path at the climb angle gamma above the horizontal and its body axis at the angle of attack alpha above the path, both angles named in a key. A blue velocity arrow points along the flight path. Four black force arrows act through the center of gravity: lift perpendicular to the path, drag backward along it, thrust along the body axis, and weight straight down. The thrust arrow is much longer than the drag arrow. An inset titled the weight, split, shows the weight and its two parts, m g sine gamma backward along the path and m g cosine gamma across it, at a right angle, with the angle gamma between the weight and its across part.
:width: 100%

Schematic of the forces in a steady climb, each drawn on its line of action through the center of gravity. The thrust carries the drag and also the part of the weight along the path, so it is longer than the drag. The climb angle, the angle of attack, and the drag are exaggerated (the drag is drawn as one third of the weight), the forces are drawn to one scale, and the inset is drawn 1.4 times larger.
:::

Lift is perpendicular to the path and drag points back along it. The thrust points along the body axis, at the angle of attack $\alpha$ above the path, as on page 5.1. The weight points straight down, so it is the one force that is neither along the path nor across it. It splits into two parts, as for the rocket on [page 4.2](#p42-losses): $mg\sin\gamma$ backward along the path and $mg\cos\gamma$ across it.

Now we add the forces in each direction. Along the path, the thrust part $T\cos\alpha$ pushes forward, and the drag and $mg\sin\gamma$ push back. Across the path, the lift and $T\sin\alpha$ balance $mg\cos\gamma$:

:::{math}
:label: eq-p53-full
\begin{aligned}
T\cos\alpha - D - mg\sin\gamma &= 0\\
L + T\sin\alpha - mg\cos\gamma &= 0
\end{aligned}
:::

The angle of attack in a climb is a few degrees, so $\cos\alpha$ is close to 1, and $T\sin\alpha$ is small next to the lift. With those two steps we get the climb equations:

::::{prf:definition} Steady climb
:label: def-p53-climb
:::{math}
:label: eq-p53-climb-forces
\begin{aligned}
T &= D + mg\sin\gamma\\
L &= mg\cos\gamma
\end{aligned}
:::
::::

The first line is the one to remember. In level flight the thrust only had to match the drag. In a climb it must also lift the part of the weight that lies along the path.

The second line shows that the wing carries a little less than the weight. For a climb of a few degrees, $\cos\gamma$ is close to 1, so $L \approx mg$. This is the shallow-climb model, and every number on this page uses it. The drag at a given speed is then the drag of level flight, which you already know how to find from [page 5.1](#p51-level-flight). For small angles we can go one step further and use $\sin\gamma \approx \gamma$, with $\gamma$ in radians.

:::{figure} figures/p53-velocity-triangle.svg
:label: fig-p53-velocity-triangle
:alt: A blue velocity arrow V along a flight path inclined at the climb angle gamma above a horizontal line. A horizontal blue arrow labeled V cosine gamma runs along the horizontal from the same start, and a vertical blue arrow labeled rate of climb, R over C equals V sine gamma, rises from its end to the tip of V, closing a right triangle.
:width: 63%

Schematic of the flight velocity split into its horizontal and vertical parts. The vertical part is the rate of climb, $R/C = V\sin\gamma$. The climb angle is exaggerated.
:::

The speed along the path is $V$. Its vertical part is the speed at which the aircraft gains height, the **rate of climb**, $R/C$ ({numref}`fig-p53-velocity-triangle`):

:::{math}
:label: eq-p53-rc-def
R/C = V\sin\gamma \approx V\gamma
:::

The rate of climb is in m/s, and pilots often quote it in ft/min. If you shorten it to $R$, it reads as the range of [page 5.2](#p52-jet-breguet).

(p53-required)=
## Thrust and power required in a climb

On page 5.1 we found the thrust required for level flight at any speed. A climb only adds one term. We put the [level-flight drag of page 5.1](#eq-p51-TR) into the first climb equation, with $\sin\gamma \approx \gamma$:

:::{math}
:label: eq-p53-TR-climb
\begin{aligned}
T_R &\approx \underbrace{\tfrac12\rho V^2 S C_{D,0}}_{\text{parasite drag}}\\
&\;\;\; + \underbrace{\frac{2K(mg)^2}{\rho S V^2}}_{\text{induced drag}}\\
&\;\;\; + \underbrace{mg\,\gamma}_{\text{weight along the path}}
\end{aligned}
:::

The first two terms are the parasite and induced drag of [page 3.3](#p33-drag-speed). The third is the part of the weight carried up the path. Power is thrust times speed, so multiplying by $V$ gives the power required in a climb:

:::{math}
:label: eq-p53-PR-climb
\begin{aligned}
P_R &\approx \tfrac12\rho V^3 S C_{D,0}\\
&\;\;\; + \frac{2K(mg)^2}{\rho S V} + mg\,\gamma V
\end{aligned}
:::

The third term does not depend on the speed in [](#eq-p53-TR-climb), so climbing at a given angle raises the whole thrust-required curve by the same amount, $mg\sin\gamma \approx mg\gamma$, as {numref}`fig-p53-climb-thrust` shows for the twin-engine executive jet of [page 5.1](#p51-example-2). It has $m = 33{,}100$ kg, $mg = 324{,}711$ N, $S = 88.2$ m², $C_{D,0} = 0.015$, $K = 0.050$, and two engines of $T_0 = 27{,}810$ N, so $T_A = 55{,}620$ N together at sea level. The gray band on the left of the plot ends at its stall speed, 61.29 m/s, from a clean $C_{L,\max}$ taken as 1.6. The band on the right starts at 272.2 m/s, Mach 0.80 at sea level, past which its drag polar no longer applies.

:::{figure} figures/p53-climb-thrust.svg
:label: fig-p53-climb-thrust
:alt: Plot of thrust in kilonewtons against true airspeed from 40 to 300 meters per second for the executive jet with two engines at sea level. Three thick solid U-shaped thrust-required curves are stacked: level flight with its minimum near 18 kilonewtons, a 3 degree climb about 17 kilonewtons higher, marked with a vertical arrow labeled m g sine gamma, and the steepest climb at 6.69 degrees. A thick dashed horizontal line is the thrust available at 55.6 kilonewtons. The steepest-climb curve just touches it at a dot, labeled 104.8 meters per second. The 3 degree curve crosses it on the right at a diamond at 212.1 meters per second. Gray bands mark speeds below stall on the left and past Mach 0.80, where wave drag sets in, on the right.
:width: 85%

Computed for the executive jet at sea level. Climbing at $\gamma$ raises the thrust-required curve by $mg\sin\gamma$ at every speed, and the steepest climb is the curve that just touches the thrust available, at the minimum-thrust speed of 104.8 m/s. A 3° climb is possible from the stall up to 212.1 m/s.
:::

At $\gamma = 3$°, the curve moves up by $mg\sin\gamma = 16{,}994$ N. Where the raised curve crosses the thrust available, the engines can just maintain that climb. The crossing on the right, at 212.1 m/s here, is the fastest speed at which the jet can sustain a 3° climb. This is the climbing version of the maximum speed of page 5.1. A steeper climb raises the curve further, until it only touches the thrust available. That climb angle is the steepest the aircraft can fly, and the next sections put a number on it.

(p53-excess)=
## Excess thrust and excess power

The figure shows how steep a climb the engines can support, and now we want a formula for the climb angle and the rate of climb at a given speed. We start from the first climb equation and put the thrust available in it:

1. **Climb angle.** The engines give $T_A$. The drag takes $D$, the drag of level flight at that speed. What is left over is the **{term}`excess thrust`**, $T_A - D$, and it carries the weight along the path:
   $$
   \begin{aligned}
   T_A &= D + mg\sin\gamma\\
   \sin\gamma &= \frac{T_A - D}{mg}
   \end{aligned}
   $$
2. **Rate of climb.** We multiply the climb angle by the speed, from [](#eq-p53-rc-def):
   $$
   \begin{aligned}
   R/C &= V\sin\gamma\\
   &= \frac{T_A V - D V}{mg}
   \end{aligned}
   $$
3. **Powers.** $T_A V$ is the power available $P_A$, and $DV$ is the power required for level flight $P_R$ ([page 5.1](#p51-power-required)). Their difference is the excess power.

::::{prf:definition} Climb angle and rate of climb
:label: def-p53-excess
:::{math}
:label: eq-p53-gamma-rc
\begin{aligned}
\sin\gamma &= \frac{T_A - D}{mg}\\
R/C &= \frac{P_A - P_R}{mg}
\end{aligned}
:::
::::

Both equations are useful because they use curves you already have. The excess power is the vertical gap between the power-available and power-required curves of page 5.1 ({numref}`fig-p53-excess-power`). Dividing it by the weight gives the rate of climb. In other words, the excess power goes into raising the weight, and power divided by weight is a speed.

:::{figure} figures/p53-excess-power.svg
:label: fig-p53-excess-power
:alt: Plot of power in megawatts against true airspeed from 0 to 300 meters per second for the executive jet at sea level. A thick dashed straight line, power available P sub A equals T sub A times V, rises above a thick solid U-shaped power-required curve. The region between them, labeled excess power, is shaded light gold from the stall speed to the maximum speed. A double-headed vertical arrow at 156.6 meters per second marks the widest gap, labeled maximum rate of climb 15.32 meters per second. The two curves meet at a diamond at V max equals 258.5 meters per second. Gray bands mark speeds below stall and past Mach 0.80.
:width: 85%

Computed for the executive jet at sea level with both engines. The rate of climb is largest where the gap between power available and power required is widest, at 156.6 m/s, well above the speed of the steepest climb.
:::

These equations apply while the climb is steady and shallow. They use the drag of level flight, so they assume $L \approx mg$. They also assume the speed does not change, because an aircraft that is speeding up uses part of its excess thrust to accelerate and climbs less steeply.

:::{warning} Use watts and newtons
In $R/C = (P_A - P_R)/(mg)$, the powers must be in watts and the weight in newtons to get m/s. If you leave the powers in kW, the rate of climb comes out 1,000 times too small. In $\sin\gamma = (T_A - D)/(mg)$, divide by the weight $mg$ in newtons, not by the mass $m$, so that both sides are without units.
:::

(p53-best-climb)=
## Steepest climb and fastest climb

The next question is which speed gives the best climb. There are two answers, because there are two things to make large. The **{term}`steepest climb`** gives the most height for each meter flown over the ground. The **{term}`fastest climb`** gives the most height for each second. Pilots call the two speeds the best-angle-of-climb speed, $V_x$, and the best-rate-of-climb speed, $V_y$ (FAA 2023, Chapter 11, p. 11-7).

**The steepest climb of a jet.** We take the thrust available of a jet as the same at every speed. We write the climb angle with the [level-flight drag of page 5.1](#eq-p51-TR) and find the speed where it peaks, the same way page 3.3 found the minimum drag:

1. **The climb angle at any speed**, written as $mg\sin\gamma$:
   $$
   \begin{aligned}
   mg\sin\gamma &= T_A - \tfrac12\rho V^2 S C_{D,0}\\
   &\;\;\; - \frac{2K(mg)^2}{\rho S V^2}
   \end{aligned}
   $$
2. **Set the derivative to zero.** $T_A$ and $mg$ do not change with $V$:
   $$
   \begin{aligned}
   mg\,\frac{d(\sin\gamma)}{dV} &= -\rho V S C_{D,0}\\
   &\;\;\; + \frac{4K(mg)^2}{\rho S V^3}\\
   &= 0
   \end{aligned}
   $$
3. **Solve for the speed.** Multiply by $V^3$ and divide by $\rho S C_{D,0}$:
   $$
   \begin{aligned}
   V^4 &= \frac{4K(mg)^2}{\rho^2 S^2 C_{D,0}}\\
   V &= \sqrt{\frac{2mg}{\rho S}}\left(\frac{K}{C_{D,0}}\right)^{1/4}
   \end{aligned}
   $$
4. **Recognize it.** This is the $V_{T_R,\min}$ of [page 5.1](#eq-p51-min-thrust), the minimum-drag speed of [page 3.3](#p33-minimum-drag). There the drag is $T_{R,\min} = 2mg\sqrt{KC_{D,0}}$, so

:::{math}
:label: eq-p53-jet-gammax
\sin\gamma_{\max} = \frac{T_A}{mg} - 2\sqrt{K C_{D,0}}
:::

The result makes sense. With a flat thrust available, the excess thrust is largest where the drag is smallest. This is the point of {numref}`fig-p53-climb-thrust`, where the steepest-climb curve touched the thrust available at $V_{T_R,\min}$.

**The fastest climb of a propeller aircraft.** For a propeller aircraft we take the power available as the same at every speed. Then the excess power $P_A - P_R$ is largest where $P_R$ is smallest, at $V_{P_R,\min}$ of [page 5.1](#p51-power-required):

:::{math}
:label: eq-p53-prop-rcmax
(R/C)_{\max} = \frac{P_A - P_{R,\min}}{mg}
:::

**The other two cases.** For a jet the power available $T_A V$ grows with speed, so the widest gap in {numref}`fig-p53-excess-power` lies to the right of the minimum of $P_R$. Setting the derivative of $R/C$ to zero gives a longer formula (Anderson 2016, Chapter 6). For one aircraft it is quicker to compute $R/C$ at a few speeds and pick the largest. For a propeller aircraft the thrust available $P_A/V$ grows as the speed falls. In this model the steepest climb then comes at a low speed, for most aircraft at the stall itself. In practice the aircraft keeps a margin above the stall speed. The model is also least reliable there, because the propeller efficiency held constant here changes with speed ([thrust and power available, page 5.1](#p51-available-and-vmax)).

A picture shows why the two best speeds differ. {numref}`fig-p53-hodograph` plots the rate of climb against the horizontal speed $V\cos\gamma$, one point for each airspeed. A line from the origin to a point has a slope of $V\sin\gamma/(V\cos\gamma) = \tan\gamma$. So the steepest climb is the point where a line from the origin just touches the curve, and the fastest climb is the top of the curve.

:::{figure} figures/p53-hodograph.svg
:label: fig-p53-hodograph
:alt: Rate of climb in meters per second against horizontal speed V cosine gamma from 0 to 280 meters per second for the executive jet with two engines. A thick solid curve rises from the stall speed, peaks, and falls to zero near 258 meters per second. A thin dashed line from the origin, labeled slope equals tangent gamma, ends where it touches the curve at an open square: steepest climb, gamma max 6.69 degrees at airspeed V of 104.8 meters per second. The top of the curve is a filled circle: fastest climb, 15.32 meters per second at V of 156.6 meters per second. An open circle between them is worked example 1, V of 135 meters per second, 14.76 meters per second and 6.28 degrees. A gray band marks speeds below stall.
:width: 85%

Computed for the executive jet at sea level with both engines. The line from the origin that touches the curve gives the steepest climb, and the top of the curve gives the fastest, so the two best climbs come at different speeds. Each point is labeled with its airspeed $V$. The vertical scale is stretched, so angles on the plot are not the true climb angles.
:::

### Worked example 1: the executive jet climbs with both engines

The executive jet climbs at sea level at $V = 135$ m/s with both engines at full thrust. We find its climb angle and rate of climb, then its steepest and fastest climbs.

1. **Drag at 135 m/s**, from the [thrust required of page 5.1](#eq-p51-TR) with $\rho = 1.2250$ kg/m³:
   $$
   \begin{aligned}
   D_0 &= 0.5 \times 1.2250 \times {135}^{2} \times\\
   &\;\;\; 88.2 \times 0.015\\
   &= 14{,}768\ \text{N}\\
   D_i &= \frac{2 \times 0.050 \times {324{,}711}^{2}}{1.2250 \times 88.2 \times {135}^{2}}\\
   &= 5{,}354.5\ \text{N}\\
   D &= 14{,}768 + 5{,}354.5\\
   &= 20{,}123\ \text{N}
   \end{aligned}
   $$
2. **Climb angle** from the excess thrust, [](#eq-p53-gamma-rc). The excess thrust is $55{,}620 - 20{,}123 = 35{,}497$ N:
   $$
   \begin{aligned}
   \sin\gamma &= \frac{55{,}620 - 20{,}123}{324{,}711}\\
   &= 0.10932\\
   \gamma &= {6.28}^\circ
   \end{aligned}
   $$
3. **Rate of climb** from the excess power:
   $$
   \begin{aligned}
   P_A &= 55{,}620 \times 135 / 1{,}000\\
   &= 7{,}509\ \text{kW}\\
   P_R &= 20{,}123 \times 135 / 1{,}000\\
   &= 2{,}717\ \text{kW}\\
   R/C &= \frac{7{,}509 - 2{,}717}{324{,}711}\times\\
   &\;\;\; 1{,}000\\
   &= 14.76\ \text{m/s}
   \end{aligned}
   $$
   As a check, $V\sin\gamma = 135 \times 0.10932 = 14.76$ m/s, the same.
4. **Steepest climb**, [](#eq-p53-jet-gammax), at $V_{T_R,\min}$:
   $$
   \begin{aligned}
   V_{T_R,\min} &= 77.53 \times 1.3512\\
   &= 104.8\ \text{m/s}\\
   \frac{T_A}{mg} &= \frac{55{,}620}{324{,}711}\\
   &= 0.17129
   \end{aligned}
   $$
   $$
   \begin{aligned}
   &2\sqrt{K C_{D,0}}\\
   &\;\;\;= 2\sqrt{0.050 \times 0.015}\\
   &\;\;\;= 0.05477\\
   &\sin\gamma_{\max}\\
   &\;\;\;= 0.17129 - 0.05477\\
   &\;\;\;= 0.11652\\
   &\gamma_{\max} = {6.69}^\circ
   \end{aligned}
   $$
   Here $77.53$ m/s is $\sqrt{2mg/(\rho S)}$ and $1.3512$ is $(K/C_{D,0})^{1/4}$.
5. **Fastest climb.** Computing $R/C$ at many speeds ({numref}`fig-p53-excess-power`) gives $(R/C)_{\max} = 15.32$ m/s at 156.6 m/s, at a climb angle of 5.62°.

At 135 m/s the jet flies between its two best speeds. It climbs a little less steeply than at 104.8 m/s and a little more slowly than at 156.6 m/s ({numref}`fig-p53-hodograph`). The shallow-climb model works well here, since $\cos(6.28°) = 0.9940$, which puts the lift within 1 percent of the weight.

(p53-ceilings)=
## Ceilings

The examples so far were at sea level. As the aircraft climbs, the air gets thinner and the engines lose output as $(\rho/\rho_0)^{m_{\text{ad}}}$, where $m_{\text{ad}}$ is the lapse exponent ([page 5.1](#p51-available-and-vmax)). The excess power shrinks, and with it the maximum rate of climb. Somewhere the aircraft can no longer climb at all, and that altitude is its ceiling. Three things set it: the density falls with altitude, the thrust or power available falls with the density, and the minimum thrust or power required does not fall.

**Why a jet has a ceiling.** The minimum thrust required, $T_{R,\min} = 2mg\sqrt{KC_{D,0}}$, has no density in it. At altitude the aircraft flies the same lift coefficient at a higher speed, with the same drag. Only one curve moves, as the thrust available falls until it reaches the constant minimum ({numref}`fig-p53-why-a-ceiling`, left). [Page 5.1](#tbl-p51-thrust-altitude) lists the thrust available of the executive jet at four altitudes against its 17,785 N minimum.

**Why a propeller aircraft has a ceiling.** Two effects close the gap from both sides. The power available falls with altitude, and the minimum power required rises. From the [minimum power of page 5.1](#eq-p51-min-power), $P_{R,\min}$ is proportional to $1/\sqrt{\rho}$, because the aircraft flies faster in thin air at the same drag, and power is drag times speed. The right panel of {numref}`fig-p53-why-a-ceiling` shows it for a four-engine turboprop transport, the aircraft of worked example 3.

:::{figure} figures/p53-why-a-ceiling.svg
:label: fig-p53-why-a-ceiling
:alt: Two panels with altitude in kilometers from 0 to 18 on the vertical axis. Left panel, executive jet with two engines: a thick dashed curve, T sub A, falls from 55.6 kilonewtons at sea level toward lower thrust as altitude rises, and a thick solid vertical line, T sub R min, constant, stands at 17.8 kilonewtons. They meet at a diamond, ceiling 15.35 kilometers. Right panel, turboprop transport with four engines, power in kilowatts: a thick dashed curve, P sub A, falls from 9,744 kilowatts at sea level, and a thick solid curve, P sub R min, rising, starts at 2,825 kilowatts and grows with altitude. They meet at a diamond, ceiling 9.20 kilometers. A dotted horizontal line at 11 kilometers, labeled tropopause, marks where the curves bend.
:width: 85%

Computed for the executive jet (left) and the four-engine turboprop transport (right). A jet stops climbing when its thrust available falls to a minimum thrust required that does not change with altitude, while a propeller aircraft is limited by both a falling power available and a rising minimum power required. The corner at 11 km is the tropopause, where the temperature stops falling. The jet's ceiling of 15.35 km comes from the model, because at that altitude it would fly at Mach 0.92, past the speed to which its polar applies.
:::

**The absolute ceiling in closed form.** At the absolute ceiling the best the aircraft can do is maintain level flight, at one speed only. For a jet we set the thrust available equal to the minimum thrust required and solve for the ceiling density $\rho_c$:

1. **The condition:**
   $$
   \begin{aligned}
   &n\,T_0\left(\frac{\rho_c}{\rho_0}\right)^{m_{\text{ad}}}\\
   &\;\;\;= 2mg\sqrt{K C_{D,0}}
   \end{aligned}
   $$
2. **Divide by $n\,T_0$ and take the power $1/m_{\text{ad}}$:**

:::{math}
:label: eq-p53-ceil-jet
\rho_c = \rho_0\left[\frac{2mg\sqrt{K C_{D,0}}}{n\,T_0}\right]^{1/m_{\text{ad}}}
:::

For a propeller aircraft we set the power available equal to the minimum power required at the ceiling density. We write $P_{R,\min,0}$ for the minimum power required at sea level, so $P_{R,\min} = P_{R,\min,0}\,(\rho_0/\rho_c)^{1/2}$ at the ceiling:

1. **The condition:**
   $$
   \begin{aligned}
   &n\,\eta\,P_0\left(\frac{\rho_c}{\rho_0}\right)^{m_{\text{ad}}}\\
   &\;\;\;= P_{R,\min,0}\left(\frac{\rho_0}{\rho_c}\right)^{1/2}
   \end{aligned}
   $$
2. **Multiply by $(\rho_c/\rho_0)^{1/2}$ and divide by $n\,\eta\,P_0$.** The exponents add:

:::{math}
:label: eq-p53-ceil-prop
\left(\frac{\rho_c}{\rho_0}\right)^{m_{\text{ad}} + 1/2} = \frac{P_{R,\min,0}}{n\,\eta\,P_0}
:::

The exponent counts the two effects. For the jet only the engine loses output, so the exponent is $m_{\text{ad}}$. For the propeller aircraft the minimum power required also grows, which adds $1/2$. With the formula for $P_{R,\min,0}$ written out, [](#eq-p53-ceil-prop) becomes a closed form in the aircraft's data, as for the jet. Each ceiling density then gives an altitude through the standard atmosphere of [page 1.4](#p14-layers).

Near the ceiling the speed range of level flight also closes. On page 5.1 the maximum speed could rise or fall with altitude, depending on how fast the engine loses output ([effect of altitude](#p51-altitude)). Near the ceiling the minimum and maximum speeds always come together, and at the absolute ceiling they merge into the one speed left, $V_{T_R,\min}$ for a jet and $V_{P_R,\min}$ for a propeller aircraft.

**The service ceiling.** A climb that slows to zero never quite reaches the absolute ceiling, because the last few meters take longer and longer. The **service ceiling** is the practical limit, defined as the altitude where the maximum rate of climb has fallen to 0.5 m/s, about 100 ft/min (FAA 2023, Chapter 11, p. 11-8). It has no closed form, so you compute $(R/C)_{\max}$ at a few altitudes and find where it crosses 0.5 m/s. Near the top, the curve of $(R/C)_{\max}$ against altitude bends only a little over the last kilometer or two, making it nearly a straight line. We can draw a straight line through the two highest rows of a table to find both ceilings with little error ({numref}`fig-p53-jet-ceiling`).

### Worked example 2: the ceilings of the executive jet

We find the absolute ceiling of the executive jet from the closed form, then both ceilings from a table of maximum rate of climb.

1. **Ceiling density**, [](#eq-p53-ceil-jet), with $n\,T_0 = 55{,}620$ N and $m_{\text{ad}} = 0.6$:
   $$
   \begin{aligned}
   \frac{T_{R,\min}}{n\,T_0} &= \frac{17{,}785}{55{,}620}\\
   &= 0.3198\\
   \rho_c &= 1.2250 \times\\
   &\;\;\; {0.3198}^{1/0.6}\\
   &= 0.1832\ \text{kg/m}^3
   \end{aligned}
   $$
2. **Altitude.** This is below the density at 11,000 m, 0.3636 kg/m³, so the ceiling lies in the {term}`isothermal layer`, where the temperature stays at 216.66 K ([page 1.4](#p14-layers)). Inverting the isothermal relation $\rho = \rho_{11}\exp[-g(h - 11{,}000)/(R T_{11})]$:
   $$
   \begin{aligned}
   h_{\text{abs}} &= 11{,}000\\
   &\;\;\; - \frac{287 \times 216.66}{9.81}\times\\
   &\;\;\; \ln\frac{0.1832}{0.3636}\\
   &= 15{,}345\ \text{m}
   \end{aligned}
   $$
   That is about 15.35 km.
3. **The table.** We compute $(R/C)_{\max}$ at six altitudes, each time at the speed of the fastest climb ({numref}`tbl-p53-jet-ceil`). That speed is found as in step 5 of worked example 1, by computing $R/C$ at many speeds.

:::{table} Maximum rate of climb of the executive jet with both engines, and the Mach number of its fastest climb.
:label: tbl-p53-jet-ceil
:align: center

| Altitude, m | Maximum rate of climb, m/s | Mach number of the fastest climb |
| ---: | ---: | ---: |
| 0 | 15.32 | 0.46 |
| 2,500 | 13.28 | 0.50 |
| 5,000 | 11.19 | 0.55 |
| 9,500 | 7.17 | 0.68 |
| 13,000 | 3.16 | 0.81 |
| 14,500 | 1.17 | 0.88 |

:::

4. **A straight line through the last two rows.** Its slope is $(14{,}500 - 13{,}000)/(3.16 - 1.17) = 753.8$ m for each m/s of climb lost. From 14,500 m we go up by that slope times the climb left to lose:
   $$
   \begin{aligned}
   h_{\text{service}} &= 14{,}500 + 753.8 \times\\
   &\;\;\; (1.17 - 0.50)\\
   &= 15{,}005\ \text{m}\\
   h_{\text{abs}} &= 14{,}500 + 753.8 \times\\
   &\;\;\; 1.17\\
   &= 15{,}382\ \text{m}
   \end{aligned}
   $$
   The exact curve gives a service ceiling of 14.99 km. The straight line puts the absolute ceiling within 37 m of the closed form.

:::{figure} figures/p53-jet-ceiling.svg
:label: fig-p53-jet-ceiling
:alt: Two panels of altitude against maximum rate of climb for the executive jet. Left panel, altitude 0 to 18 kilometers: a solid curve falls from 15.32 meters per second at sea level to zero near 15.3 kilometers, through six open circles, the table rows, and bends at a dotted line, the tropopause at 11 kilometers. A gray band above about 12.7 kilometers is labeled fastest climb past Mach 0.80, wave drag; inside it the curve is thin. Right panel, the top enlarged, 12.5 to 16 kilometers, almost all in the band: the curve lies along a wide light blue straight line through the circles at 13,000 and 14,500 meters. An open square at 0.5 meters per second marks the service ceiling, 14.99 kilometers, and a diamond at zero the absolute ceiling, 15.35 kilometers.
:width: 90%

Computed for the executive jet with both engines. The service ceiling is where the maximum rate of climb has fallen to 0.5 m/s and the absolute ceiling where it reaches zero. Near the top the curve is so nearly straight that the line through the last two table rows lies on it. The corner at 11 km is the tropopause, and the gray band marks where the fastest climb passes Mach 0.80, past the speed to which the polar applies.
:::

The last column of the table is a warning. Above about 12,700 m the fastest climb of this jet is faster than Mach 0.80, past the speed to which its drag polar is trusted (the gray band). At the absolute ceiling the jet would fly its minimum-thrust speed, 270.9 m/s, which is Mach 0.92 there. At those speeds wave drag adds to the drag ([page 3.3](#p33-drag-speed)), so the real ceiling is lower. The 15.35 km is the ceiling of the model.

(p53-example-3)=
### Worked example 3: the ceiling of a propeller aircraft

The propeller aircraft of this example is a four-engine turboprop transport. It has $m = 52{,}000$ kg ($mg = 510{,}120$ N), $S = 128$ m², $C_{D,0} = 0.022$, an aspect ratio of 8.4, and $e = 0.80$, so $K = 0.04737$. Its four engines give $P_0 = 2{,}900$ kW each, with $\eta = 0.84$ and $m_{\text{ad}} = 0.75$. All of these values are assumed for this page. We find its absolute ceiling with all four engines.

1. **Minimum power required at sea level.** At $V_{P_R,\min}$ the lift coefficient is $\sqrt{3C_{D,0}/K}$ and the drag coefficient is $4C_{D,0}$ ([page 5.1](#p51-power-required)):
   $$
   \begin{aligned}
   C_L &= \sqrt{\frac{3 \times 0.022}{0.04737}}\\
   &= 1.180\\
   C_D &= 4 \times 0.022\\
   &= 0.088\\
   V &= \sqrt{\frac{2 \times 510{,}120}{1.2250 \times 128}}\times\\
   &\;\;\; \frac{1}{\sqrt{1.180}}\\
   &= 74.26\ \text{m/s}\\
   T_R &= 510{,}120 \times\\
   &\;\;\; 0.088 / 1.180\\
   &= 38{,}043\ \text{N}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   P_{R,\min,0} &= 38{,}043 \times\\
   &\;\;\; 74.26 / 1{,}000\\
   &= 2{,}825\ \text{kW}
   \end{aligned}
   $$
2. **Ceiling density**, [](#eq-p53-ceil-prop), with $n\,\eta\,P_0 = 4 \times 0.84 \times 2{,}900 = 9{,}744$ kW and the exponent $0.75 + 0.5 = 1.25$:
   $$
   \begin{aligned}
   \left(\frac{\rho_c}{\rho_0}\right)^{1.25} &= \frac{2{,}825}{9{,}744}\\
   &= 0.2899\\
   \rho_c &= 1.2250 \times\\
   &\;\;\; {0.2899}^{1/1.25}\\
   &= 0.4549\ \text{kg/m}^3
   \end{aligned}
   $$
3. **Altitude.** This is denser than at 11,000 m, so the ceiling lies in the troposphere. Inverting $\rho/\rho_0 = (1 - 0.0065\,h/288.16)^{4.2586}$ from page 1.4:
   $$
   \begin{aligned}
   &h_{\text{abs}}\\
   &\;\;\;= \frac{288.16}{0.0065}\times\\
   &\;\;\; \left[1 - \left(\frac{0.4549}{1.2250}\right)^{1/4.2586}\right]\\
   &\;\;\;= 9{,}201\ \text{m}
   \end{aligned}
   $$

The ceiling is about 9.20 km, where both curves of {numref}`fig-p53-why-a-ceiling` cross at 4,634 kW. There the transport flies at its minimum-power speed of 121.9 m/s, well below Mach 0.80, so its polar still applies. With one engine out the same formula gives 7,253 m.

(p53-one-engine-out)=
## One engine out and an obstacle

The most demanding climb comes right after an engine fails near the ground. The question is whether the aircraft still clears the terrain ahead.

**What one engine out does.** With $n$ engines, losing one cuts the thrust or power available by $1/n$. The drag does not get smaller, so the excess thrust and the excess power shrink by much more than $1/n$. {numref}`fig-p53-climb-angle-and-roc` shows this for the executive jet. With one of its two engines, its steepest climb drops from 6.69° to 1.77°, and its fastest climb from 15.32 m/s to 3.46 m/s, a loss of 77 percent. The steepest climb stays at 104.8 m/s, because $V_{T_R,\min}$ depends on the airframe and not on the engines. The fastest climb moves to a lower speed, 119.4 m/s.

:::{figure} figures/p53-climb-angle-and-roc.svg
:label: fig-p53-climb-angle-and-roc
:alt: Two panels against true airspeed from 40 to 280 meters per second for the executive jet at sea level. Left panel, climb angle in degrees: a black curve for two engines peaks at 6.69 degrees and a blue curve with open triangles for one engine peaks at 1.77 degrees, both at 104.8 meters per second, on one dashed drop line. Right panel, rate of climb in meters per second: the two-engine curve peaks at 15.32 meters per second at 156.6 meters per second, and the one-engine curve peaks at 3.46 meters per second at 119.4 meters per second, each with its own drop line. Thin gray lines mark zero, and gray bands mark speeds below stall and past Mach 0.80.
:width: 85%

Computed for the executive jet at sea level with two engines and with one. With one engine out, the steepest climb keeps its speed and loses most of its angle, while the fastest climb loses 77 percent of its rate and moves to a lower speed. Gray bands mark speeds below stall (left) and past Mach 0.80 (right).
:::

**What the model leaves out.** The failed engine adds drag, whether it is stopped or the airflow keeps its fan or propeller turning (windmilling). The pilot also keeps the aircraft straight against the uneven thrust with the rudder, which adds more drag. Early in the climb the flaps may still be out. The aircraft may also still be speeding up to its climb speed, which uses some of the excess thrust. Each of these makes the real climb angle smaller than the model's. Treat the model's answer as an upper limit. If you plan on the bare clearance, nothing is left for what the model leaves out.

**The obstacle.** An obstacle of height $h_{\text{obs}}$ stands at a horizontal distance $d_{\text{obs}}$ from the point where the climb starts. Over that distance, a steady climb at $\gamma$ gains $d_{\text{obs}}\tan\gamma$. The aircraft clears the obstacle when this is more than $h_{\text{obs}}$, which is the same as a climb angle above the angle to the top of the obstacle:

:::{math}
:label: eq-p53-obstacle
\gamma > \gamma_{\text{req}} = \arctan\frac{h_{\text{obs}}}{d_{\text{obs}}}
:::

What matters is height gained for each meter of ground, which is the climb angle. With an obstacle ahead, the aircraft flies its steepest climb instead of its fastest. Flying faster than the steepest-climb speed may raise the rate of climb, but the aircraft covers the ground even faster and arrives lower. Regulations set a limit of the same kind. The {term}`climb gradient` is the height gained over the horizontal distance, in percent. A transport certified under 14 CFR 25.121(b) must maintain a steady climb gradient of at least 2.4 percent with one of two engines out, and at least 3.0 percent with one of four out.

### Worked example 4: the transport with three of its four engines

The four-engine transport loses one engine. Its climb starts at sea level with three engines at full power, once it has reached its climb speed with the landing gear up. A ridge 360 m high has its top 4,400 m ahead. We check the climb at 105 m/s, then at 82 m/s.

1. **Required angle**, [](#eq-p53-obstacle): $360/4{,}400 = 0.08182$, so $\gamma_{\text{req}} = {4.68}^\circ$.
2. **Power available with three engines:** $3 \times 0.84 \times 2{,}900 = 7{,}308$ kW.
3. **Climb at 105 m/s.** The thrust available is $P_A/V$. The height at the ridge uses $\tan\gamma$ from $\sin\gamma$, so it does not carry the rounding of the angle:
   $$
   \begin{aligned}
   T_A &= 7{,}308 \times 1{,}000 / 105\\
   &= 69{,}600\ \text{N}\\
   D_0 &= 0.5 \times 1.2250 \times\\
   &\;\;\; {105}^{2} \times 128 \times 0.022\\
   &= 19{,}016\ \text{N}\\
   D_i &= \frac{2 \times 0.04737}{1.2250 \times 128}\times\\
   &\;\;\; \frac{{510{,}120}^{2}}{{105}^{2}}\\
   &= 14{,}261\ \text{N}\\
   D &= 19{,}016 + 14{,}261\\
   &= 33{,}277\ \text{N}\\
   \sin\gamma &= \frac{69{,}600 - 33{,}277}{510{,}120}\\
   &= 0.07120\\
   \gamma &= {4.08}^\circ\\
   \tan\gamma &= \frac{0.07120}{\sqrt{1 - {0.07120}^{2}}}\\
   &= 0.07138\\
   \Delta h &= 4{,}400 \times 0.07138\\
   &= 314\ \text{m}
   \end{aligned}
   $$
   At 105 m/s the transport reaches the ridge 46 m too low, because ${4.08}^\circ < {4.68}^\circ$.
4. **Climb at 82 m/s.** At the lower speed the same power gives more thrust, and the drag hardly changes:
   $$
   \begin{aligned}
   T_A &= 7{,}308 \times 1{,}000 / 82\\
   &= 89{,}122\ \text{N}\\
   D_0 &= 0.5 \times 1.2250 \times\\
   &\;\;\; {82}^{2} \times 128 \times 0.022\\
   &= 11{,}598\ \text{N}\\
   D_i &= \frac{2 \times 0.04737}{1.2250 \times 128}\times\\
   &\;\;\; \frac{{510{,}120}^{2}}{{82}^{2}}\\
   &= 23{,}383\ \text{N}\\
   D &= 11{,}598 + 23{,}383\\
   &= 34{,}981\ \text{N}\\
   \sin\gamma &= \frac{89{,}122 - 34{,}981}{510{,}120}\\
   &= 0.10613\\
   \gamma &= {6.09}^\circ\\
   \tan\gamma &= \frac{0.10613}{\sqrt{1 - {0.10613}^{2}}}\\
   &= 0.10673\\
   \Delta h &= 4{,}400 \times 0.10673\\
   &= 470\ \text{m}
   \end{aligned}
   $$
   At 82 m/s the transport passes over the ridge top with 110 m to spare.

**What it means.** At 105 m/s the rate of climb is $105 \times 0.07120 = 7.48$ m/s, and at 82 m/s it is $82 \times 0.10613 = 8.70$ m/s. The slower speed even climbs a little faster here, because it is closer to the minimum-power speed. What clears the ridge, though, is its larger angle ({numref}`fig-p53-obstacle-clearance`). The speed of 82 m/s is 1.25 times the clean stall speed of 65.86 m/s, with the stall speed from $C_{L,\max} = 1.50$ ([page 3.4](#p34-stall)). The model leaves out the drag of the failed engine, and the 110 m of margin is what has to cover it.

:::{figure} figures/p53-obstacle-clearance.svg
:label: fig-p53-obstacle-clearance
:alt: Plot of height in meters, 0 to 600, against horizontal distance from the start of the climb, 0 to 6,000 meters. A gray ridge, 360 meters high, has its top at 4,400 meters. A thick solid black line from the origin, labeled 82 meters per second, gamma 6.09 degrees, passes over the ridge top at a dot labeled 470 meters high at the ridge top, 110 meters to spare. A thick solid vermilion line with open inverted triangles, labeled 105 meters per second, gamma 4.08 degrees, rises less steeply and stops at a cross labeled meets the ridge face. A thin dotted vermilion line carries it on through the ridge to an open circle at 4,400 meters, labeled 314 meters, 46 meters too low.
:width: 85%

Computed for the turboprop transport with three of its four engines at sea level. Flown faster, at 105 m/s, the aircraft climbs at a smaller angle and strikes the ridge face, while at 82 m/s it passes over the top. The dotted line shows where the faster path would be at the distance of the ridge top. The vertical scale is stretched about five times.
:::

### The jet's steepest climb with one engine

{numref}`fig-p53-climb-angle-and-roc` already showed the jet's steepest climb with one engine, 1.77°. We get it directly from the closed form [](#eq-p53-jet-gammax), with $T_A = 27{,}810$ N:

$$
\begin{aligned}
\frac{T_A}{mg} &= \frac{27{,}810}{324{,}711}\\
&= 0.08565\\
\sin\gamma_{\max} &= 0.08565 - 0.05477\\
&= 0.03088\\
\gamma_{\max} &= {1.77}^\circ
\end{aligned}
$$

The climb gradient is $\tan({1.77}^\circ) = 0.0309$, or about 3.1 percent. That is above the 2.4 percent of the regulation, but only just, and before the drag of the failed engine is counted. To be 100 m above the ground, the jet needs $100/\tan\gamma_{\max}$, about 3,240 m of ground. An obstacle closer than that, or higher, calls for a lighter aircraft.

## Summary

:::{important} Summary
- In a steady climb $T = D + mg\sin\gamma$ and $L = mg\cos\gamma$. For a shallow climb $L \approx mg$, so the drag is the drag of level flight, and the climb raises the thrust-required curve by $mg\gamma$.
- The climb angle comes from the excess thrust and the rate of climb from the excess power. A jet climbs steepest at $V_{T_R,\min}$ and fastest at a higher speed; a propeller aircraft climbs fastest at $V_{P_R,\min}$ and steepest at a lower speed.
- The absolute ceiling is where $(R/C)_{\max} = 0$. For a jet, the thrust available falls to a constant $T_{R,\min}$, while for a propeller aircraft, the power available drops to a rising $P_{R,\min}$. The service ceiling is where $(R/C)_{\max} = 0.5$ m/s.
- With one engine out the excess thrust falls by much more than the thrust. To clear an obstacle, $\gamma$ must exceed $\arctan(h_{\text{obs}}/d_{\text{obs}})$, so the aircraft flies its steepest climb.
:::

:::{table} The equations of this page.
:label: tbl-p53-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Steady climb | $T = D + mg\sin\gamma$, $L = mg\cos\gamma$ |
| Rate of climb | $R/C = V\sin\gamma$ |
| Thrust required in a climb | $T_R \approx \tfrac12\rho V^2 S C_{D,0} + 2K(mg)^2/(\rho S V^2) + mg\gamma$ |
| Climb angle | $\sin\gamma = (T_A - D)/(mg)$ |
| Rate of climb from excess power | $R/C = (P_A - P_R)/(mg)$ |
| Steepest climb of a jet, at $V_{T_R,\min}$ | $\sin\gamma_{\max} = T_A/(mg) - 2\sqrt{K C_{D,0}}$ |
| Fastest climb of a propeller aircraft, at $V_{P_R,\min}$ | $(R/C)_{\max} = (P_A - P_{R,\min})/(mg)$ |
| Absolute ceiling of a jet | $\rho_c = \rho_0\left[2mg\sqrt{KC_{D,0}}/(n\,T_0)\right]^{1/m_{\text{ad}}}$ |
| Absolute ceiling of a propeller aircraft | $(\rho_c/\rho_0)^{m_{\text{ad}}+1/2} = P_{R,\min,0}/(n\,\eta\,P_0)$ |
| Obstacle clearance | $\gamma > \arctan(h_{\text{obs}}/d_{\text{obs}})$ |

:::

:::{exercise} For discussion
:label: ex-p53-discussion

1. Losing one of two engines halves the thrust. Why does it cut the rate of climb by much more than half?
2. A pilot must clear a ridge shortly after takeoff. Which speed should the pilot fly, $V_x$ or $V_y$, and why?
3. Why is the exponent of $\rho_c/\rho_0$ equal to $m_{\text{ad}}$ in the jet ceiling equation, but $m_{\text{ad}} + 1/2$ for a propeller aircraft?
4. On a hot day the air at the airport is less dense than in the standard atmosphere ([nonstandard days](#p14-nonstandard)). How does that change the rate of climb and the margin over an obstacle?
5. Why can an aircraft never quite reach its absolute ceiling, and why does that make the service ceiling the more useful number?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-5-3.html
:label: quiz-5-3
:width: 100%
:enumerated: false

Quiz for Standard 5.3: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 6.
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023. Chapter 11, "Aircraft Performance," pp. 11-7 to 11-8 (climb performance).
- Title 14 of the Code of Federal Regulations, Section 25.121, "Climb: one-engine-inoperative," paragraph (b), U.S. Government Publishing Office, 2024.
