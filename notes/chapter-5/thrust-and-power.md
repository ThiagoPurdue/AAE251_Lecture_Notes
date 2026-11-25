---
title: "5.1 Thrust and Power"
short_title: 5.1 Thrust and Power
---

:::{include} ../_parts/standards/5.1.md
:::

In Chapter 3, we built the {term}`drag polar` and turned it into drag as a function of airspeed. Now we put an engine on the aircraft and ask what it can do. In {term}`steady level flight`, the engines must supply enough thrust to match drag and enough power to push the aircraft forward. We compare what the airframe requires with what the engines deliver. That comparison gives us the minimum thrust, the minimum power, the top speed, and how all three shift as we climb into thinner air.

:::{note} What to take from this page
- In steady level flight with a small {term}`angle of attack`, lift equals weight ($L = mg$) and {term}`thrust required` equals drag ($T_R = D$). {term}`Power required` is $P_R = T_R V$.
- Minimum thrust required occurs at $(L/D)_{\max}$, where $C_L = \sqrt{C_{D,0}/K}$ and parasite drag equals induced drag. Minimum power required occurs slower, at $V_{P_R,\min} = {3}^{-1/4}\,V_{T_R,\min} \approx 0.760\,V_{T_R,\min}$, where induced drag is three times parasite drag.
- A jet is rated by its {term}`thrust available` $T_A = n\,\delta_t\,T_0(\rho/\rho_0)^{m_{\text{ad}}}$, which is nearly flat with speed. A propeller aircraft is rated by its {term}`power available` $P_A = n\,\delta_t\,\eta\,P_0(\rho/\rho_0)^{m_{\text{ad}}}$, which is nearly flat with speed.
- Maximum level speed $V_{\max}$ is where $T_A = T_R$ (or $P_A = P_R$). For a jet it has a closed quadratic solution; for a propeller aircraft it solves a quartic equation by iteration.
- As altitude rises, $T_{R,\min}$ stays unchanged while $V_{T_R,\min}$ grows as $\rho^{-1/2}$; both $P_{R,\min}$ and $V_{P_R,\min}$ grow as $\rho^{-1/2}$, while $T_A$ and $P_A$ fall as $(\rho/\rho_0)^{m_{\text{ad}}}$.
:::

(p51-level-flight)=
## Steady level unaccelerated flight

We start with an aircraft cruising at constant altitude and constant {term}`true airspeed` $V_\infty$ ({numref}`fig-p51-level-flight-fbd`). Four forces act on it: lift $L$ perpendicular to the flight path, drag $D$ backward along the flight path, weight $mg$ straight down, and thrust $T$ forward along the thrust line, tilted above the flight path by a small angle $\alpha$.

:::{figure} figures/p51-level-flight-fbd.svg
:label: fig-p51-level-flight-fbd
:alt: Side view of a transport aircraft flying horizontally to the right in steady level flight, with the horizontal flight path drawn as a thin gray line and the thrust line dashed at a small angle alpha above it. Four thick black force arrows act at the center of gravity: lift L straight up, weight mg straight down, drag D straight back along the flight path, and thrust T forward along the dashed thrust line. A blue velocity arrow along the flight path to the right is labeled airspeed V infinity. A key at top left distinguishes black force arrows from blue velocity arrows.
:width: 85%

Forces on an aircraft in steady level flight. When the thrust angle $\alpha$ is small, $\cos\alpha \approx 1$ and $\sin\alpha \approx 0$, so the vertical balance reduces to $L = mg$ and the horizontal balance reduces to $T = D$.
:::

With zero acceleration, the forces along and perpendicular to the flight path sum to zero:

$$
\begin{aligned}
T\cos\alpha - D &= 0\\
L + T\sin\alpha - mg &= 0
\end{aligned}
$$

In normal cruise, $\alpha$ is only a few degrees, so $\cos\alpha \approx 1$. The vertical thrust component $T\sin\alpha$ is tiny compared with weight both because $\sin\alpha$ is small and because cruise thrust $T$ is a small fraction of $mg$. Dropping those small terms leaves the two equations of **steady level unaccelerated flight** (often abbreviated SLUF):

:::{math}
:label: eq-p51-sluf
\begin{aligned}
L &= mg = \tfrac12 \rho V^2 S C_L\\
T_R &= D = \tfrac12 \rho V^2 S C_D
\end{aligned}
:::

Here $S$ is the wing reference area and $\rho$ is the air density at the flight altitude from the {term}`standard atmosphere` ([page 1.4](../chapter-1/standard-atmosphere.md)). We take $g = 9.81$ m/s² throughout these notes, and we write $T_R$ for the **thrust required** to hold steady level flight at speed $V$.

### Thrust required as a function of speed

From [](#eq-p51-sluf), the {term}`lift coefficient` needed to support the weight at speed $V$ is

$$
C_L = \frac{2mg}{\rho V^2 S}
$$

We substitute this $C_L$ into $T_R = \tfrac12\rho V^2 S(C_{D,0} + K C_L^2)$ from the parabolic {term}`drag polar` of [page 3.3](../chapter-3/drag-polar.md), with $K = 1/(\pi e\,\textit{AR})$. Cancelling one factor of $\tfrac12\rho V^2 S$ gives the thrust required at every speed:

::::{prf:definition} Thrust required in steady level flight
:label: def-p51-thrust-required
:::{math}
:label: eq-p51-TR
T_R = \tfrac12 \rho V^2 S C_{D,0} + \frac{2K(mg)^2}{\rho S V^2}
:::
::::

The first term is {term}`parasite drag`, which rises with $V^2$. The second term is {term}`induced drag`, which falls with $1/V^2$ because the wing needs a smaller $C_L$ at higher speed. Dividing the two lines of [](#eq-p51-sluf) also gives the compact form

:::{math}
:label: eq-p51-TR-LD
T_R = \frac{mg}{L/D} = \frac{mg}{C_L / C_D}
:::

{numref}`fig-p51-thrust-required` plots both terms and their sum for an executive twin-jet at sea level. Below the {term}`stall speed` $V_{\text{stall}} = \sqrt{2mg/(\rho S C_{L,\max})}$, the wing cannot generate enough lift to stay level, so that region is shaded out. Just above stall, induced drag dominates and $T_R$ is high. At high speed, parasite drag dominates and $T_R$ rises steeply again. Between the two lies a clear trough.

:::{figure} figures/p51-thrust-required.svg
:label: fig-p51-thrust-required
:alt: Plot of thrust required T sub R in kilonewtons against true airspeed V from 40 to 260 meters per second for an executive twin-jet at sea level. A shaded gray band on the left marks the stall region below 61 meters per second. A dotted orange curve labeled induced, falls as 1 over V squared drops from 26 kilonewtons near stall toward zero. A dashed blue curve labeled parasite, grows as V squared rises from 3 to 55 kilonewtons. The two cross at an open circle at 104.8 meters per second and 8.89 kilonewtons, labeled parasite equals induced. Directly above that crossing, the solid black sum curve labeled total T sub R reaches its minimum at a solid black dot labeled minimum thrust, T sub R min equals 17.79 kilonewtons at V sub T R min equals 104.8 meters per second.
:width: 80%

Thrust required against true airspeed for the executive twin-jet of worked example 2 at sea level ($m = 33{,}100$ kg, $S = 88.2$ m², $C_{D,0} = 0.015$, $K = 0.050$). Total thrust required reaches its minimum right above the speed where parasite drag and induced drag are equal.
:::

### Minimum thrust required

Because $T_R = mg/(L/D)$ from [](#eq-p51-TR-LD), minimizing thrust required is the same problem as maximizing the {term}`lift-to-drag ratio` $L/D$ from [page 3.3](#p33-minimum-drag). Differentiating [](#eq-p51-TR) with respect to $V$ and setting $dT_R/dV = 0$ gives

$$
\rho V S C_{D,0} = \frac{4K(mg)^2}{\rho S V^3}
$$

which shows that parasite drag equals induced drag ($C_{D,0} = K C_L^2$). Solving from that balance gives four results we use across all of Chapter 5:

:::{math}
:label: eq-p51-min-thrust
\begin{aligned}
C_{L,T_R,\min} &= \sqrt{\frac{C_{D,0}}{K}}, \qquad C_{D,T_R,\min} = 2 C_{D,0}\\
\left(\frac{L}{D}\right)_{\max} &= \frac{1}{2\sqrt{K C_{D,0}}}\\
T_{R,\min} &= \frac{mg}{(L/D)_{\max}} = 2mg\sqrt{K C_{D,0}}\\
V_{T_R,\min} &= \sqrt{\frac{2mg}{\rho S}}\left(\frac{K}{C_{D,0}}\right)^{1/4}
\end{aligned}
:::

Notice two physical facts in [](#eq-p51-min-thrust). First, at minimum thrust required, parasite drag equals induced drag ($C_{D,0} = K C_L^2$), so $C_D = 2 C_{D,0}$. Second, $T_{R,\min}$ does not contain air density $\rho$ at all. The least thrust needed to hold level flight is the same at sea level and at 14,000 m, though you must fly faster in thinner air to reach it.

### Worked example 1: single-point level flight and trim

A single-engine general-aviation propeller aircraft has mass $m = 1{,}315$ kg, wing area $S = 16.3$ m², lift curve $C_L = 0.02 + 0.12\,\alpha$ (with $\alpha$ in degrees), $C_{L,\max} = 2.4$, and drag polar $C_D = 0.026 + 0.054\,C_L^2$. Its pitching-moment coefficient about the {term}`center of gravity` is $C_M = 0.12 - 0.08\,\alpha + 0.075\,\delta_e$, where $\delta_e$ is the {term}`elevator` deflection in degrees. At sea level ($\rho = 1.2250$ kg/m³), find: (a) the angle of attack, thrust required, power required, and trim elevator deflection ($C_M = 0$) at $V = 70$ m/s; and (b) the airspeed, thrust required, and power required at $\alpha = {5.0}^\circ$.

We first find the aircraft weight:

$$
\begin{aligned}
mg &= 1{,}315 \times 9.81\\
   &= 12{,}900\ \text{N}
\end{aligned}
$$

**(a) Given speed $V = 70$ m/s at sea level.**

1. **Dynamic pressure and $qS$:**
   $$
   \begin{aligned}
   q &= \tfrac12 \rho V^2\\
     &= 0.5 \times 1.2250 \times {70}^{2}\\
     &= 3{,}001.3\ \text{Pa}\\
   qS &= 3{,}001.3 \times 16.3\\
      &= 48{,}921\ \text{N}
   \end{aligned}
   $$
2. **Lift coefficient and angle of attack** from $L = mg = qSC_L$:
   $$
   \begin{aligned}
   C_L &= \frac{12{,}900}{48{,}921}\\
       &= 0.2637\\
   \alpha &= \frac{C_L - 0.02}{0.12}\\
          &= \frac{0.2637 - 0.02}{0.12}\\
          &= {2.03}^\circ
   \end{aligned}
   $$
3. **Drag coefficient, thrust required, and power required:**
   $$
   \begin{aligned}
   C_D &= 0.026 + 0.054 \times {0.2637}^{2}\\
       &= 0.02976\\
   T_R &= qS C_D\\
       &= 48{,}921 \times 0.02976\\
       &= 1{,}456\ \text{N}\\
   P_R &= T_R V\\
       &= 1{,}456 \times 70\\
       &= 101{,}920\ \text{W}\\
       &= 101.9\ \text{kW}
   \end{aligned}
   $$
4. **Trim elevator deflection** from $C_M = 0$:
   $$
   \begin{aligned}
   \delta_e &= -\frac{0.12 - 0.08 \times 2.03}{0.075}\\
            &= {0.565}^\circ
   \end{aligned}
   $$

**(b) Given angle of attack $\alpha = {5.0}^\circ$ at sea level.**

1. **Coefficients from the lift curve and polar:**
   $$
   \begin{aligned}
   C_L &= 0.02 + 0.12 \times 5.0\\
       &= 0.62\\
   C_D &= 0.026 + 0.054 \times {0.62}^{2}\\
       &= 0.04676
   \end{aligned}
   $$
2. **Level-flight speed** from $mg = \tfrac12\rho V^2 S C_L$:
   $$
   \begin{aligned}
   V &= \sqrt{\frac{2mg}{\rho S C_L}}\\
     &= \sqrt{\frac{2 \times 12{,}900}{1.2250 \times 16.3 \times 0.62}}\\
     &= 45.65\ \text{m/s}
   \end{aligned}
   $$
3. **Thrust required and power required:**
   $$
   \begin{aligned}
   \frac{L}{D} &= \frac{0.62}{0.04676}\\
               &= 13.26\\
   T_R &= \frac{12{,}900}{13.26}\\
       &= 972.9\ \text{N}\\
   P_R &= 972.9 \times 45.65\\
       &= 44{,}413\ \text{W}\\
       &= 44.41\ \text{kW}
   \end{aligned}
   $$

**Check.** Flying slower at $\alpha = {5.0}^\circ$ calls for a higher lift coefficient ($0.62$ instead of $0.2637$). Because $70$ m/s lies well above the minimum-drag speed, slowing down lowers parasite drag much more than induced drag rises, reducing thrust required from $1{,}456$ N to $972.9$ N and power required from $101.9$ kW to $44.41$ kW. Both speeds remain well above the sea-level stall speed:

$$
\begin{aligned}
V_{\text{stall}} &= \sqrt{\frac{2 \times 12{,}900}{1.2250 \times 16.3 \times 2.4}}\\
                 &= 23.20\ \text{m/s}
\end{aligned}
$$

(p51-power-required)=
## Power required and minimum power

Thrust tells us what a jet engine must supply, but propeller engines are rated in power, and climbing depends on excess power. Power is force times velocity. In steady level flight, the **power required** $P_R$ is the thrust required multiplied by the true airspeed $V$. Multiplying [](#eq-p51-TR) by $V$ gives

::::{prf:definition} Power required in steady level flight
:label: def-p51-power-required
:::{math}
:label: eq-p51-PR
P_R = T_R V = \tfrac12 \rho V^3 S C_{D,0} + \frac{2K(mg)^2}{\rho S V}
:::
::::

Watch how the exponents shift when we multiply by $V$. Parasite power now rises steeply as $V^3$, while induced power falls more gently as $1/V$. Substituting $V = \sqrt{2mg/(\rho S C_L)}$ into $P_R = T_R V = (mg\,C_D/C_L)V$ gives the aerodynamic form

:::{math}
:label: eq-p51-PR-CL
P_R = \sqrt{\frac{2(mg)^3}{\rho S}}\,\frac{C_D}{C_L^{3/2}}
:::

### Minimum power required

Because $P_R$ is proportional to $C_D / C_L^{3/2}$, minimum power required occurs where $C_L^{3/2}/C_D$ is largest, not where $C_L/C_D$ is largest. Differentiating [](#eq-p51-PR) with respect to $V$ and setting $dP_R/dV = 0$ gives

$$
\frac{3}{2}\rho V^2 S C_{D,0} = \frac{2K(mg)^2}{\rho S V^2}
$$

Compare that equation with [](#eq-p51-TR): the left side is $3 D_0$ and the right side is $D_i$. At minimum power, induced drag is **three times** parasite drag ($K C_L^2 = 3 C_{D,0}$, giving $C_D = 4 C_{D,0}$). Solving for the lift coefficient, {term}`minimum-power speed`, and minimum power gives

:::{math}
:label: eq-p51-min-power
\begin{aligned}
C_{L,P_R,\min} &= \sqrt{\frac{3 C_{D,0}}{K}}, \qquad C_{D,P_R,\min} = 4 C_{D,0}\\
V_{P_R,\min} &= \sqrt{\frac{2mg}{\rho S}}\left(\frac{K}{3 C_{D,0}}\right)^{1/4} = {3}^{-1/4}\,V_{T_R,\min} \approx 0.7598\,V_{T_R,\min}\\
P_{R,\min} &= \frac{4}{{3}^{3/4}}\sqrt{\frac{2(mg)^3}{\rho S}}\,K^{3/4}\,C_{D,0}^{1/4}
\end{aligned}
:::

{numref}`fig-p51-power-required` draws the power-required curve of the general-aviation aircraft from worked example 1. Two points stand out on the same plot. The lowest point of the curve is $V_{P_R,\min} = 32.79$ m/s ($P_{R,\min} = 36.60$ kW). Because $T_R = P_R/V$, the slope of any straight line from the origin $(0,0)$ to a point on the $P_R(V)$ curve equals the thrust required at that speed. The shallowest line from the origin that touches the curve marks $V_{T_R,\min} = 43.15$ m/s. Notice that $32.79/43.15 = 0.7599$, matching ${3}^{-1/4} = 0.7598$ to four digits.

:::{figure} figures/p51-power-required.svg
:label: fig-p51-power-required
:alt: Plot of power required P sub R in kilowatts against true airspeed V from 10 to 90 meters per second for the general-aviation aircraft at sea level. A shaded gray band on the left marks the stall region below 23.2 meters per second. A dotted orange curve labeled induced, falls as 1 over V slopes downward from 39 to 10 kilowatts. A dashed blue curve labeled parasite, grows as V cubed curves sharply upward to 176 kilowatts. The solid black total P sub R curve reaches its minimum at a black dot labeled minimum power, 36.60 kilowatts at 32.79 meters per second. A dashed gray straight line from the origin lies tangent to the P sub R curve at an open square labeled tangent from origin, V sub T R min equals 43.15 meters per second.
:width: 80%

Power required against true airspeed for the general-aviation aircraft at sea level. Minimum power ($36.60$ kW at $32.79$ m/s) lies well to the left of the minimum-thrust point ($43.15$ m/s), where the line from the origin is tangent to $P_R$.
:::

:::{warning} Minimum power is slower than minimum drag
Do not assume that minimum drag and minimum power happen at the same speed. Because $P_R = T_R V$, slowing slightly below $V_{T_R,\min}$ raises $T_R$ only slightly near its flat trough while $V$ falls faster, so their product keeps decreasing until $D_i = 3 D_0$. At $V_{T_R,\min}$, $D_i = D_0$ and $C_D = 2 C_{D,0}$; at $V_{P_R,\min}$, $D_i = 3 D_0$, $C_D = 4 C_{D,0}$, and the speed is always $0.760\,V_{T_R,\min}$ for any aircraft with a parabolic polar.
:::

(p51-available-and-vmax)=
## Thrust available, power available, and maximum speed

So far we have computed what the airframe requires. Now we model what the engines can deliver. An engine's output depends on how it moves air, so we model jet and propeller engines differently (Anderson 2016, Chapter 6):

- **Jet engines** (turbojets and turbofans) are rated by their static sea-level thrust $T_0$ per engine. At subsonic speeds, thrust available changes little with airspeed, so we treat it as constant with $V$ and scale it with air density:
  :::{math}
  :label: eq-p51-TA
  T_A = n\,\delta_t\,T_0\left(\frac{\rho}{\rho_0}\right)^{m_{\text{ad}}}, \qquad P_A = T_A V
  :::
- **Propeller engines** (piston and turboprop) are rated by their sea-level shaft power $P_0$ per engine. The propeller turns shaft power into thrust power with propeller efficiency $\eta$ (typically $0.75$ to $0.85$ in cruise), so power available is nearly flat with speed:
  :::{math}
  :label: eq-p51-PA
  P_A = n\,\delta_t\,\eta\,P_0\left(\frac{\rho}{\rho_0}\right)^{m_{\text{ad}}}, \qquad T_A = \frac{P_A}{V}
  :::

In both equations, $n$ is the number of operating engines and $\delta_t$ is the throttle setting ($0 \le \delta_t \le 1$, with $\delta_t = 1$ at full output). The sea-level standard density is $\rho_0 = 1.2250$ kg/m³, and $m_{\text{ad}}$ is the air-density lapse exponent (typically $0.6$ to $1.0$, depending on the engine).

### Finding the maximum level speed

Steady level flight is possible only where available thrust (or power) is at least as large as required thrust (or power). The high-speed crossing where $T_A = T_R$ (equivalently $P_A = P_R$) sets the **maximum level speed** $V_{\max}$ ({numref}`fig-p51-available-and-vmax`).

:::{figure} figures/p51-available-and-vmax.svg
:label: fig-p51-available-and-vmax
:alt: Two panels side by side. Panel 1, titled jet (thrust), shows thrust in kilonewtons against true airspeed from 50 to 275 meters per second for the executive jet at sea level: a dashed horizontal blue line at T sub A equals 55.62 kilonewtons crosses the solid black U-shaped T sub R curve at a black dot marked V sub max equals 258.5 meters per second with a dashed drop line to the speed axis. Panel 2, titled propeller (power), shows power in kilowatts against true airspeed from 20 to 92 meters per second for the general-aviation aircraft at sea level: a dashed horizontal blue line at P sub A equals 172.8 kilowatts crosses the solid black P sub R curve at a black dot marked V sub max equals 85.51 meters per second.
:width: 85%

Computed at sea level and full throttle ($\delta_t = 1$) for the executive jet of worked example 2 (Panel 1) and the propeller aircraft of worked example 1 (Panel 2). Maximum level speed occurs at the high-speed crossing where available output matches required output ($258.5$ m/s for the jet, $85.51$ m/s for the propeller aircraft); steady level flight is possible only where the available line stays above the required curve.
:::

**For a jet**, setting $T_A = T_R$ in [](#eq-p51-TR) and multiplying by $V^2$ gives a quadratic equation in $V^2$:

$$
\left(\tfrac12 \rho S C_{D,0}\right)(V^2)^2 - T_A V^2 + \frac{2K(mg)^2}{\rho S} = 0
$$

The larger root is the maximum speed $V_{\max}$ (the smaller root is the thrust-limited minimum speed, which for most aircraft lies below stall):

:::{math}
:label: eq-p51-vmax-jet
V_{\max} = \sqrt{\frac{T_A + \sqrt{T_A^2 - 4 C_{D,0} K (mg)^2}}{\rho S C_{D,0}}}
:::

Check the expression inside the inner square root. Because $T_{R,\min} = 2mg\sqrt{K C_{D,0}}$, the discriminant is $T_A^2 - T_{R,\min}^2$. Real level flight exists only when $T_A \ge T_{R,\min}$.

**For a propeller aircraft**, setting $P_A = P_R$ in [](#eq-p51-PR) produces a quartic equation in $V$:

$$
\tfrac12 \rho S C_{D,0}\,V^3 + \frac{2K(mg)^2}{\rho S V} = P_A
$$

Because induced power is small at top speed, moving the induced-power term to the right, isolating $V^3$, and taking the cube root gives a fast fixed-point iteration:

:::{math}
:label: eq-p51-vmax-prop
V_{k+1} = \left[\frac{2}{\rho S C_{D,0}}\left(P_A - \frac{2K(mg)^2}{\rho S V_k}\right)\right]^{1/3}
:::

Starting from the zero-induced-drag estimate $V_0 = [2 P_A / (\rho S C_{D,0})]^{1/3}$, two or three passes converge to four significant figures.

:::{tip} Method: minimum speeds and $V_{\max}$
1. Find the density $\rho$ at the flight altitude from the standard atmosphere.
2. Compute $W = mg$, $T_{R,\min} = 2mg\sqrt{K C_{D,0}}$, and $V_{T_R,\min} = \sqrt{2mg/(\rho S)}\,(K/C_{D,0})^{1/4}$.
3. Compute $V_{P_R,\min} = 0.7598\,V_{T_R,\min}$ and $P_{R,\min}$ from [](#eq-p51-min-power).
4. Compute $T_A$ (jet) or $P_A$ (propeller) at full throttle ($\delta_t = 1$) using $(\rho/\rho_0)^{m_{\text{ad}}}$.
5. For a jet, use [](#eq-p51-vmax-jet) directly; for a propeller aircraft, iterate [](#eq-p51-vmax-prop) until $V$ stops changing.
6. Check the Mach number $M = V_{\max}/a_s$. If you get a Mach number above about $0.75$ to $0.80$, wave drag is missing from the subsonic polar and the real top speed is lower.
:::

### Worked example 2: minimum thrust, minimum power, and $V_{\max}$

**(a) Executive twin-jet at sea level.** An executive twin-jet has mass $m = 33{,}100$ kg, wing area $S = 88.2$ m², $C_{D,0} = 0.015$, $K = 0.050$, and two engines rated at $T_0 = 27{,}810$ N each with $m_{\text{ad}} = 0.6$. Find $(L/D)_{\max}$, $T_{R,\min}$, $V_{T_R,\min}$, $V_{P_R,\min}$, $P_{R,\min}$, and $V_{\max}$ at sea level.

1. **Weight and total sea-level thrust available:**
   $$
   \begin{aligned}
   mg &= 33{,}100 \times 9.81\\
      &= 324{,}711\ \text{N}\\
   T_A &= 2 \times 27{,}810\\
       &= 55{,}620\ \text{N}
   \end{aligned}
   $$
2. **Minimum thrust required and its speed**, [](#eq-p51-min-thrust):
   $$
   \begin{aligned}
   \left(\frac{L}{D}\right)_{\max} &= \frac{1}{2\sqrt{0.050 \times 0.015}}\\
       &= 18.26\\
   T_{R,\min} &= \frac{324{,}711}{18.26}\\
              &= 17{,}785\ \text{N}\\
   V_{T_R,\min} &= \sqrt{\frac{2 \times 324{,}711}{1.2250 \times 88.2}}\left(\frac{0.050}{0.015}\right)^{1/4}\\
                &= 104.8\ \text{m/s}
   \end{aligned}
   $$
3. **Minimum power required and its speed**, [](#eq-p51-min-power):
   $$
   \begin{aligned}
   V_{P_R,\min} &= 0.7598 \times 104.8\\
                &= 79.60\ \text{m/s}\\
   P_{R,\min} &= \frac{4}{{3}^{3/4}}\sqrt{\frac{2 \times {324{,}711}^{3}}{1.2250 \times 88.2}}\,{0.050}^{3/4}\,{0.015}^{1/4}\\
              &= 1.635 \times {10}^{6}\ \text{W}
   \end{aligned}
   $$
   which is $1{,}635$ kW.
4. **Maximum level speed**, [](#eq-p51-vmax-jet):
   $$
   \begin{aligned}
   \rho S C_{D,0} &= 1.2250 \times 88.2 \times 0.015\\
                  &= 1.6207\ \text{kg/m}\\
   \sqrt{T_A^2 - T_{R,\min}^2} &= \sqrt{{55{,}620}^{2} - {17{,}785}^{2}}\\
                               &= 52{,}700\ \text{N}\\
   V_{\max} &= \sqrt{\frac{55{,}620 + 52{,}700}{1.6207}}\\
            &= 258.5\ \text{m/s}
   \end{aligned}
   $$
   With the sea-level {term}`speed of sound` $a_s = 340.3$ m/s, this is Mach $258.5/340.3 = 0.760$, still in the subsonic regime where the parabolic polar is reasonable.

**(b) General-aviation propeller aircraft at sea level.** The aircraft of worked example 1 ($m = 1{,}315$ kg, $mg = 12{,}900$ N, $S = 16.3$ m², $C_{D,0} = 0.026$, $K = 0.054$) has a single engine rated at $P_0 = 216$ kW with propeller efficiency $\eta = 0.80$ and $m_{\text{ad}} = 0.6$. Find $V_{T_R,\min}$, $T_{R,\min}$, $V_{P_R,\min}$, $P_{R,\min}$, and $V_{\max}$ at sea level.

1. **Power available at sea level:** $P_A = 0.80 \times 216 = 172.8$ kW ($172{,}800$ W).
2. **Minimum thrust and minimum power:** [](#eq-p51-min-thrust) gives $T_{R,\min} = 966.7$ N at $V_{T_R,\min} = 43.15$ m/s; [](#eq-p51-min-power) gives $V_{P_R,\min} = 32.79$ m/s and $P_{R,\min} = 36.60$ kW.
3. **Maximum speed by fixed-point iteration**, [](#eq-p51-vmax-prop), using $\rho S C_{D,0} = 1.2250 \times 16.3 \times 0.026 = 0.51916$ kg/m and $2K(mg)^2/(\rho S) = 900{,}077$ W·m/s:
   $$
   \begin{aligned}
   V_0 &= \left(\frac{2 \times 172{,}800}{0.51916}\right)^{1/3}\\
       &= 87.32\ \text{m/s}\\
   V_1 &= \left[\frac{2}{0.51916}\left(172{,}800 - \frac{900{,}077}{87.32}\right)\right]^{1/3}\\
       &= 85.54\ \text{m/s}\\
   V_2 &= \left[\frac{2}{0.51916}\left(172{,}800 - \frac{900{,}077}{85.54}\right)\right]^{1/3}\\
       &= 85.51\ \text{m/s}
   \end{aligned}
   $$
   The next pass also gives $85.51$ m/s, so $V_{\max} = 85.51$ m/s.

**Check.** Putting $V = 85.51$ m/s back into [](#eq-p51-PR) gives parasite power $162.3$ kW plus induced power $10.5$ kW, totaling $172.8$ kW, which equals $P_A$.

(p51-altitude)=
## Effect of altitude

Climbing into thinner air changes both sides of the performance picture: the airframe curves shift, and the engines lose output. Look back at [](#eq-p51-min-thrust) and [](#eq-p51-min-power) to see how every point moves when density drops from $\rho_0$ to $\rho$:

- **Every point on the $T_R(V)$ curve shifts straight to the right** by $\sqrt{\rho_0/\rho}$ at the same thrust. In particular, $T_{R,\min}$ does not change with altitude, while $V_{T_R,\min}$ grows as $\sqrt{\rho_0/\rho}$.
- **Every point on the $P_R(V)$ curve shifts both right and up** by the same factor $\sqrt{\rho_0/\rho}$, because $P_R = T_R V$ multiplies an unchanged thrust by a higher true airspeed.
- **Both $T_A$ and $P_A$ fall** by the engine lapse factor $(\rho/\rho_0)^{m_{\text{ad}}}$.

{numref}`fig-p51-altitude-jet` shows both views for the executive twin-jet at sea level and at $14{,}000$ m. In Panel 1, the $T_R$ bucket slides horizontally right while its floor stays on the same $T_{R,\min}$ line; meanwhile the horizontal $T_A$ line drops sharply toward that floor. In Panel 2, the jet's power available $P_A = T_A V$ is a straight line through the origin with slope $T_A$. Climbing makes that $P_A$ line shallower while lifting the $P_R$ bucket up and right.

:::{figure} figures/p51-altitude-jet.svg
:label: fig-p51-altitude-jet
:alt: Two panels side by side comparing sea level in black and 14 kilometers altitude in blue for the executive twin-jet. Panel 1, titled thrust versus speed, shows solid black T sub R at sea level and dashed blue T sub R at 14 kilometers, both touching the same horizontal gray line labeled same minimum thrust required at solid dots; horizontal thrust available lines T sub A at sea level (black dashed, 55.6 kilonewtons) and T sub A at 14 kilometers (blue dotted, 20.2 kilonewtons) cross their respective T sub R curves at open squares. Panel 2, titled power versus speed, shows straight lines from the origin for P sub A at sea level (steep black dashed) and P sub A at 14 kilometers (shallow blue dotted), crossing the black and dashed blue P sub R curves at open squares; the 14 kilometer P sub R curve lies higher and farther right than the sea-level curve.
:width: 85%

Computed for the executive jet at sea level and $14{,}000$ m. Altitude shifts $T_R$ horizontally right at constant $T_{R,\min}$ (Panel 1) and lifts $P_R$ up and right while flattening $P_A = T_A V$ (Panel 2), until $T_A$ drops to $T_{R,\min}$ and leaves no excess thrust to climb higher.
:::

{numref}`fig-p51-altitude-prop` shows the same altitude shift for the general-aviation propeller aircraft between sea level and $6{,}000$ m. Here $P_R$ shifts up and right while flat $P_A$ drops from $172.8$ kW to $119.2$ kW. The vertical gap between $P_A$ and $P_R$ shrinks rapidly as altitude increases.

:::{figure} figures/p51-altitude-prop.svg
:label: fig-p51-altitude-prop
:alt: Plot of power in kilowatts against true airspeed from 20 to 95 meters per second for the general-aviation propeller aircraft at sea level in black and 6,000 meters in blue. Horizontal lines show P sub A at sea level (black dashed, 172.8 kilowatts) and P sub A at 6,000 meters (blue dotted, 119.2 kilowatts). The solid black sea-level P sub R curve has its minimum dot at 36.6 kilowatts and crosses sea-level P sub A at an open square near 85.5 meters per second. The dashed blue 6,000 meter P sub R curve lies higher and farther right, with its minimum dot at 49.9 kilowatts and its crossing with 6,000 meter P sub A at an open square near 89.6 meters per second.
:width: 80%

Altitude shifts the propeller aircraft's $P_R$ curve up and right while $P_A$ drops from $172.8$ kW at sea level to $119.2$ kW at $6{,}000$ m. The vertical gap $P_A - P_R$ shrinks sharply, even though $V_{\max}$ increases slightly at this intermediate altitude.
:::

### Worked example 3: altitude changes for jet and propeller aircraft

**(a) Executive twin-jet at 10,000 m and 14,000 m.** Using the standard atmosphere of [page 1.4](../chapter-1/standard-atmosphere.md), we find $T_A$, $V_{T_R,\min}$, and the subsonic-polar $V_{\max}$ at $10{,}000$ m ($\rho = 0.4124$ kg/m³) and $14{,}000$ m ($\rho = 0.2265$ kg/m³).

At $h = 10{,}000$ m:

$$
\begin{aligned}
T_A &= 55{,}620 \left(\frac{0.4124}{1.2250}\right)^{0.6}\\
    &= 28{,}944\ \text{N}\\
V_{T_R,\min} &= \sqrt{\frac{2 \times 324{,}711}{0.4124 \times 88.2}}\left(\frac{0.050}{0.015}\right)^{1/4}\\
             &= 180.5\ \text{m/s}
\end{aligned}
$$

Applying [](#eq-p51-vmax-jet) gives $V_{\max} = 308.1$ m/s. But at $10{,}000$ m, the temperature is $223.16$ K and the speed of sound is $299.5$ m/s, so $308.1$ m/s corresponds to Mach $1.03$. At $14{,}000$ m ($\rho = 0.2265$ kg/m³), the same steps give $T_A = 20{,}204$ N, $V_{T_R,\min} = 243.6$ m/s, and a subsonic-polar $V_{\max} = 315.3$ m/s (Mach $1.07$).

This result shows a real limit of our model. Because our parabolic drag polar leaves out {term}`wave drag`, it predicts supersonic speeds for a subsonic business jet at high altitude. On the real aircraft, shock waves form near Mach 0.78 to 0.85 and drag rises sharply. Transonic drag divergence caps the true top speed well below Mach 1.

**(b) General-aviation propeller aircraft at 6,000 m.** At $h = 6{,}000$ m ($\rho = 0.6594$ kg/m³):

$$
\begin{aligned}
P_A &= 172.8 \left(\frac{0.6594}{1.2250}\right)^{0.6}\\
    &= 119.2\ \text{kW}\\
V_{P_R,\min} &= 32.79 \sqrt{\frac{1.2250}{0.6594}}\\
             &= 44.69\ \text{m/s}\\
P_{R,\min} &= 36.60 \sqrt{\frac{1.2250}{0.6594}}\\
           &= 49.9\ \text{kW}
\end{aligned}
$$

Iterating [](#eq-p51-vmax-prop) at $\rho = 0.6594$ kg/m³ with $P_A = 119{,}200$ W gives $V_{\max} = 89.60$ m/s. That is slightly faster than the sea-level value of $85.51$ m/s because parasite power at fixed speed falls linearly with $\rho$, which drops faster than this $m_{\text{ad}} = 0.6$ engine loses power ($\rho^{0.6}$). At higher altitudes, engine power falls further and $V_{\max}$ eventually drops back down.

## Summary

:::{important} Summary
- In steady level unaccelerated flight (small $\alpha$), $L = mg = \tfrac12\rho V^2 S C_L$, $T_R = D = mg/(L/D)$, and $P_R = T_R V$.
- Minimum thrust required comes at $C_L = \sqrt{C_{D,0}/K}$, where $C_D = 2 C_{D,0}$ and $T_{R,\min} = mg/(L/D)_{\max}$ is independent of altitude.
- Minimum power required comes at $C_L = \sqrt{3 C_{D,0}/K}$, where $C_D = 4 C_{D,0}$ and $V_{P_R,\min} = {3}^{-1/4}\,V_{T_R,\min} \approx 0.760\,V_{T_R,\min}$.
- Thrust available scales as $T_A = n\,\delta_t\,T_0(\rho/\rho_0)^{m_{\text{ad}}}$ for jets, and power available scales as $P_A = n\,\delta_t\,\eta\,P_0(\rho/\rho_0)^{m_{\text{ad}}}$ for propellers. Maximum speed occurs where available equals required.
- Climbing into thinner air shifts $T_R$ straight right as $\rho^{-1/2}$, shifts $P_R$ up and right as $\rho^{-1/2}$, and reduces $T_A$ and $P_A$ as $(\rho/\rho_0)^{m_{\text{ad}}}$.
:::

:::{table} The equations of this page.
:label: tbl-p51-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Steady level flight balance | $L = mg = \tfrac12\rho V^2 S C_L$, $T_R = D = mg/(L/D)$ |
| Thrust required | $T_R = \tfrac12\rho V^2 S C_{D,0} + 2K(mg)^2/(\rho S V^2)$ |
| Power required | $P_R = T_R V = \tfrac12\rho V^3 S C_{D,0} + 2K(mg)^2/(\rho S V)$ |
| Minimum thrust condition | $C_L = \sqrt{C_{D,0}/K}$, $C_D = 2C_{D,0}$, $T_{R,\min} = 2mg\sqrt{KC_{D,0}}$ |
| Minimum-thrust speed | $V_{T_R,\min} = \sqrt{2mg/(\rho S)}\,(K/C_{D,0})^{1/4}$ |
| Minimum power condition | $C_L = \sqrt{3C_{D,0}/K}$, $C_D = 4C_{D,0}$ |
| Minimum-power speed | $V_{P_R,\min} = {3}^{-1/4}\,V_{T_R,\min} \approx 0.7598\,V_{T_R,\min}$ |
| Jet thrust available | $T_A = n\,\delta_t\,T_0(\rho/\rho_0)^{m_{\text{ad}}}$, $P_A = T_A V$ |
| Propeller power available | $P_A = n\,\delta_t\,\eta\,P_0(\rho/\rho_0)^{m_{\text{ad}}}$, $T_A = P_A/V$ |
| Jet maximum speed | $V_{\max} = \sqrt{(T_A + \sqrt{T_A^2 - 4C_{D,0}K(mg)^2})/(\rho S C_{D,0})}$ |

:::

:::{exercise} For discussion
:label: ex-p51-discussion

1. Why does minimum thrust required $T_{R,\min}$ stay constant as an aircraft climbs, while minimum power required $P_{R,\min}$ increases?
2. On a plot of $P_R$ against $V$, how can you locate both $V_{P_R,\min}$ and $V_{T_R,\min}$ with only a ruler?
3. An aircraft flies in steady level flight below $V_{T_R,\min}$. If the pilot slows down further while holding altitude, does the thrust required go up or down? Explain why pilots call this the "back side of the power curve."
4. In worked example 3(a), the subsonic parabolic polar predicts a top speed above Mach 1 at 10,000 m for a subsonic jet. What physical phenomenon did the model omit, and how would the real $T_R$ curve differ near Mach 0.85?
5. Suppose a propeller aircraft loses one of its two identical engines in cruise. What happens to $P_A$, to $P_{R,\min}$, and to the vertical gap $P_A - P_R$?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-5-1.html
:label: quiz-5-1
:width: 100%
:enumerated: false

Quiz for Standard 5.1: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 6, "Elements of Airplane Performance" (Sections 6.1 to 6.6).
- Anderson, J. D., Jr., *Aircraft Performance and Design*, McGraw-Hill, 1999. Chapter 5, "Airplane Performance: Steady Flight."
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023. Chapter 11, "Aircraft Performance."
