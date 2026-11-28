---
title: "5.1 Thrust and Power"
short_title: 5.1 Thrust and Power
---

:::{include} ../_parts/standards/5.1.md
:::

In Chapter 3, we used the {term}`drag polar` to find the aerodynamic drag an aircraft must overcome at any airspeed. To predict aircraft performance, we now match that airframe drag against what the propulsion system can deliver. Comparing thrust and power required with thrust and power available gives us the minimum and maximum level-flight speeds and shows how the flight envelope narrows with altitude. We work through the full analysis for two representative airplanes: a single-engine propeller aircraft and a twin-engine business jet.

:::{note} What to take from this page
- In {term}`steady level flight` with a small {term}`angle of attack`, lift balances the weight, $L = mg$, and the {term}`thrust required` equals the drag, $T_R = D = mg/(L/D)$. The {term}`power required` is $P_R = T_R V$.
- Minimum thrust comes at $(L/D)_{\max}$, where the parasite and induced drag are equal. Minimum power comes at a lower speed, $V_{P_R,\min} = {3}^{-1/4}\,V_{T_R,\min}$, where the induced drag is three times the parasite drag.
- A jet is rated in thrust and a propeller aircraft in power. The jet's thrust and the propeller aircraft's power are each nearly flat with speed, and both fall with altitude as $(\rho/\rho_0)^{m_{\text{ad}}}$.
- Level flight is possible from the stall speed up to the {term}`maximum speed <Maximum level speed>`, where available equals required. With altitude the required curves move right, the available curves come down, and the band of possible speeds closes.
:::

(p51-level-flight)=
## Steady level flight

Most of a flight is cruise, so cruise is where we start, by saying exactly what kind of flight this is and which forces act on the aircraft.

::::{prf:definition} Level flight and steady flight
:label: def-p51-steady-level

**{term}`Level flight`** is flight at constant altitude, meaning the flight path is horizontal. **{term}`Steady flight`** is flight with no acceleration, so the speed and its direction do not change, and the forces and moments on the aircraft add up to zero. **Steady level flight** is both at once.
::::

Three angles describe how the aircraft points and where it goes ({numref}`fig-p51-flight-angles`). The {term}`flight-path angle` $\gamma$ is measured from the horizontal to the flight path, the direction of the velocity. The angle of attack $\alpha$ is measured from the flight path to the body axis. The {term}`pitch angle` $\theta$ is measured from the horizontal to the body axis, so $\theta = \gamma + \alpha$. In level flight $\gamma = 0$, and the pitch angle and the angle of attack are the same.

:::{figure} figures/p51-flight-angles.svg
:label: fig-p51-flight-angles
:alt: Two side views of a Boeing 737-800 outline. Top, climbing: a horizontal line, a solid flight path line with a blue velocity arrow, and a dashed body axis line, all from the center of gravity. Arcs mark gamma from the horizontal to the flight path, alpha from the flight path to the body axis, and a larger arc theta from the horizontal to the body axis. Bottom, level: the flight path lies on the horizontal, and the arcs for alpha and theta span the same angle. A note below says theta equals gamma plus alpha, and in level flight gamma is zero.
:width: 80%

Schematic, angles exaggerated (drawn as 15° and 10°). The pitch angle is the flight-path angle plus the angle of attack. In level flight the flight-path angle is zero, so the pitch angle equals the angle of attack.
:::

To write the forces, we make four assumptions:

1. **The thrust acts along the body axis**, so it points at the angle of attack $\alpha$ above the flight path.
2. **The air is still**, with no wind and no gusts.
3. **The flight is coordinated**, so the aircraft does not slip sideways through the air.
4. **The ground is an inertial frame**, so we neglect the rotation of the Earth.

With these, four forces act on the aircraft ({numref}`fig-p51-level-flight-fbd`). Lift $L$ is perpendicular to the flight path and drag $D$ is along it, backward. The weight $mg$ points straight down, and the thrust $T$ points along the body axis.

:::{figure} figures/p51-level-flight-fbd.svg
:label: fig-p51-level-flight-fbd
:alt: Side view of a Boeing 737-800 outline pitched nose up, flying to the right along a horizontal flight path. A dashed body axis passes through the center of gravity at the angle alpha above the flight path. Four thick black force arrows act on lines through the center of gravity: lift L straight up, weight mg straight down of about the same length, a short drag D backward along the flight path behind the tail, and a short thrust T forward along the body axis ahead of the nose. A thinner blue arrow below the nose is the velocity V. A key at top left names the force and velocity arrows.
:width: 95%

Schematic. With a small angle of attack, lift balances the weight and thrust balances the drag. The angle of attack is drawn as 10° and the drag as one third of the weight; in cruise both are several times smaller. The four forces are drawn to one scale, in balance, each on its line of action through the center of gravity.
:::

With no acceleration, the forces along the flight path and across it each add up to zero:

$$
\begin{aligned}
T\cos\alpha - D &= 0\\
L + T\sin\alpha - mg &= 0
\end{aligned}
$$

Two small quantities now drop out. In cruise $\alpha$ is a few degrees, so $\cos\alpha$ is close to 1. The vertical part of the thrust, $T\sin\alpha$, is small for two reasons. First, $\sin\alpha$ is small, and second, the thrust is a small fraction of the weight. For the airplane of worked example 1 at 70 m/s, $\alpha = {2.03}^\circ$ and $\cos\alpha = 0.99937$. Its thrust is 1,456 N, so $T\sin\alpha$ is 51.6 N, only 0.40 percent of the weight. Dropping these terms leaves the two equations of steady level flight:

:::{math}
:label: eq-p51-sluf
\begin{aligned}
L &= mg = \tfrac12 \rho V^2 S C_L\\
T_R &= D = \tfrac12 \rho V^2 S C_D
\end{aligned}
:::

Here $V$ is the {term}`true airspeed` ([page 1.5](../chapter-1/bernoulli-and-pitot-static.md)), $S$ the wing area, and $\rho$ the density at the flight altitude from the {term}`standard atmosphere` ([page 1.4](../chapter-1/standard-atmosphere.md)). $T_R$, the thrust required, is the thrust needed to maintain this flight. The moments must also be zero. A pitching moment would rotate the nose up or down, so the pilot sets the elevator until that moment vanishes. An aircraft with zero pitching moment is **{term}`trimmed <Trim>`**.

## What the pilot sets and what the design sets

Before we solve these equations, we sort their quantities into three groups. Some are fixed before the flight starts, others come out of the analysis, and a few are in the pilot's hands.

- **Parameters** are fixed by the design and by the day. They are the weight $mg$, the wing area $S$, the polar constants $C_{D,0}$ and $K$, the engine data, and the air density $\rho$.
- **Variables** are what the analysis finds: $L$, $D$, $T$, $V$, the power, $\gamma$, $\alpha$, $C_L$, and $C_D$.
- **Pilot inputs** are the four controls ([page 1.3](../chapter-1/vehicle-anatomy.md) shows the surfaces). They are the aileron angle $\delta_a$, the elevator angle $\delta_e$, the rudder angle $\delta_r$, and the {term}`throttle setting` $\delta_t$. Two of them matter on this page. The elevator angle is positive with the trailing edge down, and the throttle setting runs from 0, no thrust, to 1, full thrust. The ailerons and the rudder matter in turns, which this chapter does not treat.

The pitching moment also needs a sign, and nose up is positive. A trailing-edge-down elevator pushes the tail up and the nose down, so it makes a negative moment. As a result, the pitching-moment coefficient falls as $\delta_e$ grows.

(p51-thrust-required)=
## Thrust required

From the second line of [](#eq-p51-sluf), the thrust required equals the drag. [Page 3.3](#p33-drag-speed) found the drag at any speed by putting the lift coefficient of level flight into the polar. In the symbols of this chapter, with the weight written $mg$:

::::{prf:definition} Thrust required in steady level flight
:label: def-p51-thrust-required
:::{math}
:label: eq-p51-TR
\begin{aligned}
T_R &= \tfrac12 \rho V^2 S C_{D,0}\\
&\;\;\; + \frac{2K(mg)^2}{\rho S V^2}
\end{aligned}
:::
::::

The first term is the {term}`parasite drag`, which grows as $V^2$, and the second is the {term}`induced drag`, which falls as $1/V^2$.

Dividing the second line of [](#eq-p51-sluf) by the first gives a second form. The factor $\tfrac12\rho V^2 S$ cancels, and $T_R/(mg) = C_D/C_L$:

:::{math}
:label: eq-p51-TR-LD
T_R = \frac{mg}{L/D} = \frac{mg}{C_L / C_D}
:::

The thrust required is the weight divided by the {term}`lift-to-drag ratio`, which is why $L/D$ is also called the aerodynamic efficiency. A cleaner aircraft needs less thrust to carry the same weight.

### Two kinds of problem

Problems come in two kinds. When the speed is given, the lift equation gives $C_L = 2mg/(\rho V^2 S)$, the lift curve gives $\alpha$, and the polar gives $C_D$. When the angle of attack is given, the lift curve of [page 3.2](#p32-lift-curve) gives $C_L = C_{L,0} + C_{L,\alpha}\,\alpha$, with the {term}`lift-curve slope` $C_{L,\alpha}$, and the polar gives $C_D$. Then the lift equation, solved for the speed, gives

$$
V = \sqrt{\frac{2mg}{\rho S C_L}}
$$

So $\alpha$, $C_L$, and $C_D$ go together. If you know one of them, the lift curve and the polar give you the other two.

### Thrust required against angle of attack

Since $C_L$ and $C_D$ both follow from $\alpha$, so does their ratio:

$$
\begin{aligned}
\frac{C_L}{C_D} &= \frac{C_L}{C_{D,0} + K C_L^2}\\
C_L &= C_{L,0} + C_{L,\alpha}\,\alpha
\end{aligned}
$$

At small $\alpha$ the lift coefficient is small and $L/D$ is low. At large $\alpha$ the induced drag, which grows as $C_L^2$, takes over and $L/D$ falls again. In between it has a maximum, and by [](#eq-p51-TR-LD) the thrust required has its minimum at the same angle ({numref}`fig-p51-ld-and-thrust-vs-alpha`). For the general-aviation airplane of worked example 1, that angle is 5.62°, where $C_L = 0.6939$. Notice that neither $\rho$ nor $S$ appears in $T_R = mg/(L/D)$. At a given angle of attack the aircraft needs the same thrust at every altitude; only the speed changes.

:::{figure} figures/p51-ld-and-thrust-vs-alpha.svg
:label: fig-p51-ld-and-thrust-vs-alpha
:alt: Two graphs sharing a horizontal axis of angle of attack from 0 to 22 degrees, with a gray band past stall above 19.8 degrees. Top: lift-to-drag ratio rises from about 5 at 1 degree to a maximum, marked with a filled dot, of 13.34 at 5.62 degrees, then falls to about 7 at stall. Bottom: thrust required in newtons falls steeply from 1 degree, labeled fast flight, to a filled dot labeled minimum thrust, at the same 5.62 degrees, then rises slowly, labeled slow flight, to about 1,800 N at stall. Open circles on both curves mark the cases of worked example 1, labeled 2.03 degrees, 70 m/s and 5.0 degrees, 45.65 m/s.
:width: 85%

Computed for the general-aviation airplane of worked example 1, from its lift curve and polar. The thrust required is the weight over $L/D$, so the minimum thrust comes at the angle of attack of the highest $L/D$, here 5.62°. A low angle of attack means fast flight, a high one slow flight. The open circles are the two cases of worked example 1.
:::

### Thrust required against speed

Each speed in level flight requires its own angle of attack. Flying slowly needs a large $C_L$ and a high angle of attack, so induced drag dominates. Flying fast needs a small $C_L$ and a low angle of attack, and the parasite drag dominates ({numref}`fig-p51-thrust-required`). For the executive jet of worked example 2, at sea level, $C_L$ is 0.94 at 80 m/s and only 0.11 at 230 m/s.

:::{figure} figures/p51-thrust-required.svg
:label: fig-p51-thrust-required
:alt: Graph of thrust required in kilonewtons against true airspeed from 0 to 300 meters per second for the executive jet at sea level, with gray bands below stall, under 61 meters per second, and past Mach 0.80, above 272 meters per second, labeled wave drag. A dashed blue parasite curve rises and a dotted vermilion induced curve falls; they meet at an open circle labeled parts equal at 104.8 meters per second. The solid black total curve has its minimum, a filled dot labeled minimum thrust 17.79 kilonewtons, directly above. Open squares mark a slow point at 80 meters per second, C sub L 0.94, high angle of attack, and a fast point at 230 meters per second, C sub L 0.11, low angle of attack.
:width: 85%

Computed for the executive jet at sea level. Induced drag dominates in slow flight at a high angle of attack, parasite drag dominates in fast flight at a low angle of attack, and minimum thrust occurs where the two parts are equal. The curves turn thin where the polar no longer applies.
:::

The minimum thrust is the minimum drag of [page 3.3](#p33-minimum-drag). The speed where it occurs, the {term}`minimum-thrust speed` $V_{T_R,\min}$, is the {term}`minimum-drag speed` of that page under another name. There the induced drag equals the parasite drag, and the [minimum-drag equations of page 3.3](#eq-p33-CLstar) give:

:::{math}
:label: eq-p51-min-thrust
\begin{aligned}
C_{L} &= \sqrt{\frac{C_{D,0}}{K}}\\
\left(\frac{L}{D}\right)_{\max} &= \frac{1}{2\sqrt{K C_{D,0}}}\\
T_{R,\min} &= 2mg\sqrt{K C_{D,0}}\\
V_{T_R,\min} &= \sqrt{\frac{2mg}{\rho S}}\left(\frac{K}{C_{D,0}}\right)^{1/4}
\end{aligned}
:::

The third line has no $\rho$ in it. The minimum thrust needed to maintain level flight is the same at every altitude, though in thin air you reach it at a higher true airspeed.

(p51-power-required)=
## Power required and minimum power

Thrust is not the whole picture, because a propeller engine is rated in power and the climb of [page 5.3](#p53-excess) depends on spare power. We need the power the airframe requires as well.

Power is the rate of doing work. A force $\vec F$ that moves its point of action by $d\vec x$ does the work $\vec F \cdot d\vec x$, and dividing by the time $dt$ gives the power, $P = \vec F \cdot \vec V$. In steady level flight the thrust is, to our approximation, along the velocity, so the **power required** is

::::{prf:definition} Power required in steady level flight
:label: def-p51-power-required
:::{math}
:label: eq-p51-PR
\begin{aligned}
P_R &= T_R V\\
&= \tfrac12 \rho V^3 S C_{D,0}\\
&\;\;\; + \frac{2K(mg)^2}{\rho S V}
\end{aligned}
:::
::::

This is [](#eq-p51-TR) with each term multiplied by $V$, so the parasite power now grows as $V^3$, and the induced power falls only as $1/V$. A third form uses the coefficients. We start from $P_R = (mg\,C_D/C_L)\,V$ and put in $V = \sqrt{2mg/(\rho S C_L)}$:

:::{math}
:label: eq-p51-PR-CL
\begin{aligned}
P_R &= \frac{mg\,C_D}{C_L}\sqrt{\frac{2mg}{\rho S C_L}}\\
&= \sqrt{\frac{2(mg)^3}{\rho S}}\,\frac{C_D}{C_L^{3/2}}
\end{aligned}
:::

Because of that factor, the minimum power occurs where $C_L^{3/2}/C_D$ is largest, instead of where $C_L/C_D$ is largest.

### Minimum power required

We find the minimum from [](#eq-p51-PR), step by step.

1. **Differentiate** with respect to $V$ and set the result to zero:
   $$
   \begin{aligned}
   \frac{dP_R}{dV} &= \tfrac32 \rho V^2 S C_{D,0}\\
   &\;\;\; - \frac{2K(mg)^2}{\rho S V^2}\\
   &= 0
   \end{aligned}
   $$
2. **Compare the two terms.** The first is three times the parasite drag $\tfrac12\rho V^2 S C_{D,0}$, and the second is the induced drag itself. At minimum power, the induced drag is three times the parasite drag.
3. **Write it in coefficients.** The ratio of induced to parasite drag is $K C_L^2/C_{D,0}$, so $K C_L^2 = 3C_{D,0}$. Then $C_L = \sqrt{3C_{D,0}/K}$ and $C_D = 4C_{D,0}$.
4. **Find the speed** from the lift equation with this $C_L$, and the power from [](#eq-p51-PR-CL).

:::{math}
:label: eq-p51-min-power
\begin{aligned}
C_{L} &= \sqrt{\frac{3 C_{D,0}}{K}}\\
V_{P_R,\min} &= \sqrt{\frac{2mg}{\rho S}}\left(\frac{K}{3 C_{D,0}}\right)^{1/4}\\
P_{R,\min} &= \frac{4}{{3}^{3/4}}\sqrt{\frac{2(mg)^3}{\rho S}}\\
&\;\;\;\times K^{3/4}\,C_{D,0}^{1/4}
\end{aligned}
:::

Dividing the two speeds gives

$$
\begin{aligned}
V_{P_R,\min} &= {3}^{-1/4}\,V_{T_R,\min}\\
&= 0.7598\,V_{T_R,\min}
\end{aligned}
$$

For any aircraft with a parabolic polar, the {term}`minimum-power speed` is about 24 percent below the minimum-thrust speed.

{numref}`fig-p51-power-required` shows both points on one curve. Because $T_R = P_R/V$, the slope of a straight line from the origin to any point of the curve is the thrust required there. The shallowest such line just touches the curve, and it touches at the minimum-thrust speed. For the general-aviation airplane of worked example 1, at sea level, the minimum power is 36.60 kW at 32.79 m/s. There the induced power is 27.45 kW, three times the parasite power of 9.15 kW.

:::{figure} figures/p51-power-required.svg
:label: fig-p51-power-required
:alt: Graph of power required in kilowatts against true airspeed from 0 to 100 meters per second for the general-aviation airplane at sea level, with a gray band below stall up to 23.2 meters per second. A dashed blue parasite curve rises steeply and a dotted vermilion induced curve falls. The solid black total curve has its lowest point, a filled dot, at 36.60 kilowatts and 32.79 meters per second; below it two open circles show the induced part three times the parasite part. A thin dashed line starts at an open circle at the origin and touches the curve at an open square, labeled tangent from the origin, minimum thrust, to the right of the minimum.
:width: 85%

Computed for the general-aviation airplane at sea level. Minimum power comes at a lower speed than minimum thrust. Minimum thrust is where a line from the origin touches the curve, and the slope of that line is the minimum thrust required. At the minimum power the induced part is three times the parasite part.
:::

:::{warning} The minimum-power speed is below the minimum-thrust speed
Do not assume that the minimum thrust and the minimum power come at the same speed. Just below $V_{T_R,\min}$ the drag curve is nearly flat, so the drag rises a little while the speed falls more. Their product keeps falling until the induced drag is three times the parasite drag.
:::

(p51-available-and-vmax)=
## Thrust and power available

So far we have looked only at what the airframe needs. The engines are the other side, and the two kinds are rated in different ways, so we model them differently (Anderson 2016, Chapter 6).

A **jet engine** is rated by its sea-level static thrust $T_0$ per engine. We take its {term}`thrust available` as constant with speed and let it fall with density:

:::{math}
:label: eq-p51-TA
\begin{aligned}
T_A &= n\,\delta_t\,T_0\left(\frac{\rho}{\rho_0}\right)^{m_{\text{ad}}}\\
P_A &= T_A V
\end{aligned}
:::

A **propeller engine** is rated by the shaft power $P_0$ it gives at sea level. The propeller turns shaft power into thrust power with the {term}`propeller efficiency` $\eta$, and the result is the {term}`power available`:

:::{math}
:label: eq-p51-PA
\begin{aligned}
P_A &= n\,\delta_t\,\eta\,P_0\left(\frac{\rho}{\rho_0}\right)^{m_{\text{ad}}}\\
T_A &= \frac{P_A}{V}
\end{aligned}
:::

Here $n$ is the number of engines that run, $\delta_t$ the throttle setting, and $\rho_0 = 1.2250$ kg/m³ the sea-level density. The exponent $m_{\text{ad}}$, called the lapse exponent, describes how fast the engine loses output as the air thins. It comes with the engine data, and for our two aircraft it is $m_{\text{ad}} = 0.6$.

{numref}`fig-p51-available-against-speed` shows what these models mean. The jet's thrust is flat, so its power available grows in proportion to the speed. The propeller's power is flat, so its thrust falls as speed rises. If you double the speed, the thrust drops in half. Real engines are only nearly flat. A fixed-pitch propeller is efficient at one combination of airspeed and engine speed, and its efficiency is low at the start of the takeoff roll (FAA 2023, Chapter 5). Our constant $\eta$ is a cruise value.

:::{figure} figures/p51-available-against-speed.svg
:label: fig-p51-available-against-speed
:alt: Four graphs against true airspeed. Left column, the executive jet: thrust available is a flat dashed line at 55.62 kilonewtons; power available is a dashed straight line from the origin, with open circles at 5.562 megawatts at 100 meters per second and 11.12 megawatts at 200. Right column, the general-aviation airplane: thrust available is a dashed curve falling from about 8.6 kilonewtons at 20 meters per second, with open circles at 4.32 kilonewtons at 40 and 2.16 kilonewtons at 80; power available is a flat dashed line at 172.8 kilowatts.
:width: 85%

Computed for the two aircraft at sea level and full throttle. In this model a jet's thrust and a propeller aircraft's power do not change with speed, so the propeller's thrust falls as speed rises. Doubling the speed doubles the jet's power and halves the propeller's thrust.
:::

:::{warning} Watts, and all the engines
$P_0$ is often given in kilowatts and $T_0$ per engine. Before you use [](#eq-p51-PA) with [](#eq-p51-PR), convert the power to watts and multiply by the number of running engines $n$.
:::

(p51-example-1)=
### Worked example 1: the general-aviation airplane in level flight

The airplane has $m = 1{,}315$ kg, $S = 16.3$ m², the lift curve $C_L = 0.02 + 0.12\,\alpha$ ($\alpha$ in degrees), and the polar $C_D = 0.026 + 0.054\,C_L^2$. Its {term}`maximum lift coefficient` is 2.4, reached near $\alpha = {19.8}^\circ$. Its pitching-moment coefficient about the {term}`center of gravity` is $C_M = 0.12 - 0.08\,\alpha - 0.075\,\delta_e$, with both angles in degrees and the signs of the convention above. One piston engine gives $P_0 = 216$ kW, with $\eta = 0.80$. At sea level ($\rho = 1.2250$ kg/m³), find the flight condition at 70 m/s, then at $\alpha = {5.0}^\circ$, and check that both can be flown.

The weight is

$$
\begin{aligned}
mg &= 1{,}315 \times 9.81\\
   &= 12{,}900\ \text{N}
\end{aligned}
$$

**(a) Speed given, 70 m/s.**

1. **Dynamic pressure** and $qS$:
   $$
   \begin{aligned}
   q &= 0.5 \times 1.2250 \times {70}^{2}\\
     &= 3{,}001.3\ \text{Pa}\\
   qS &= 3{,}001.3 \times 16.3\\
      &= 48{,}921\ \text{N}
   \end{aligned}
   $$
2. **Lift coefficient and angle of attack**, from $L = mg = qSC_L$ and the lift curve:
   $$
   \begin{aligned}
   C_L &= \frac{12{,}900}{48{,}921}\\
       &= 0.2637\\
   \alpha &= \frac{0.2637 - 0.02}{0.12}\\
          &= {2.03}^\circ
   \end{aligned}
   $$
3. **Drag coefficient, drag, and thrust required.** The lift is the weight, 12,900 N.
   $$
   \begin{aligned}
   C_D &= 0.026 + 0.054 \times\\
       &\;\;\; {0.2637}^{2}\\
       &= 0.02976\\
   T_R &= 48{,}921 \times 0.02976\\
       &= 1{,}456\ \text{N}
   \end{aligned}
   $$
4. **Power required:**
   $$
   \begin{aligned}
   P_R &= 1{,}456 \times 70\\
       &= 101{,}920\ \text{W}
   \end{aligned}
   $$
   That is 101.9 kW.
5. **Trim.** We set $C_M = 0$ and solve for $\delta_e$:
   $$
   \begin{aligned}
   \delta_e &= \frac{0.12 - 0.08\,\alpha}{0.075}\\
            &= \frac{0.12 - 0.08 \times 2.03}{0.075}\\
            &= \frac{-0.0424}{0.075}\\
            &= {-0.565}^\circ
   \end{aligned}
   $$
   The minus sign means trailing edge up, so at this speed the airplane needs a little nose-up elevator.

**(b) Angle of attack given, 5.0°.**

1. **Coefficients** from the lift curve and the polar:
   $$
   \begin{aligned}
   C_L &= 0.02 + 0.12 \times 5.0\\
       &= 0.62\\
   C_D &= 0.026 + 0.054 \times\\
       &\;\;\; {0.62}^{2}\\
       &= 0.04676
   \end{aligned}
   $$
2. **Speed** from the lift equation:
   $$
   \begin{aligned}
   V &= \sqrt{\frac{2 \times 12{,}900}{1.2250 \times 16.3}}\times\\
     &\;\;\; \frac{1}{\sqrt{0.62}}\\
     &= 45.65\ \text{m/s}
   \end{aligned}
   $$
3. **Thrust and power required**, with [](#eq-p51-TR-LD):
   $$
   \begin{aligned}
   \frac{L}{D} &= \frac{0.62}{0.04676}\\
               &= 13.26\\
   T_R &= \frac{12{,}900}{13.26}\\
       &= 972.9\ \text{N}\\
   P_R &= 972.9 \times 45.65\\
       &= 44{,}413\ \text{W}
   \end{aligned}
   $$
   That is 44.41 kW.

**(c) Checking that the airplane can fly both.** Every answer must pass two checks. The lift coefficient must stay below $C_{L,\max}$, and 0.2637 and 0.62 are both below 2.4. The power required must also stay below the power available, $0.80 \times 216 = 172.8$ kW, and both 101.9 kW and 44.41 kW pass.

Suppose you find that some other speed needs $C_L = 2.8$. That is more than the wing can give, so the speed lies below the stall speed, $V_\text{stall} = \sqrt{2mg/(\rho S C_{L,\max})} = 23.20$ m/s ([page 3.4](#p34-stall)), and the airplane cannot fly at that speed in level flight. Suppose instead a high speed needed more than 172.8 kW. The engine cannot supply it, so the airplane either slows down or descends.

**Check.** Slowing from 70 m/s to 45.65 m/s cut the thrust required from 1,456 N to 972.9 N. At 70 m/s the airplane is far above its minimum-thrust speed, so slowing down sheds more parasite drag than it adds induced drag. Both cases appear on the curves of {numref}`fig-p51-ld-and-thrust-vs-alpha`.

(p51-vmax)=
## Maximum speed and the speed range

Now we bring the two sides together. Level flight is possible wherever the engines can provide at least what the airframe needs. The fastest such speed, where available equals required, is the **maximum speed** $V_{\max}$, also called the maximum level speed. The slowest is usually set by the stall, not by the engine (FAA 2023, Chapter 11).

**For a jet**, we set $T_A = T_R$ in [](#eq-p51-TR) and multiply by $V^2$. This gives a quadratic equation in $V^2$:

$$
\begin{aligned}
&\left(\tfrac12 \rho S C_{D,0}\right)(V^2)^2 - T_A\,V^2\\
&\;\;\; + \frac{2K(mg)^2}{\rho S} = 0
\end{aligned}
$$

The quadratic formula gives two roots, and the larger one is the maximum speed:

:::{math}
:label: eq-p51-vmax-jet
V_{\max} = \sqrt{\frac{T_A + \sqrt{T_A^2 - 4 C_{D,0} K (mg)^2}}{\rho S C_{D,0}}}
:::

The smaller root, with a minus sign in front of the inner root, is the low-speed crossing, which usually lies below the stall speed. Since $T_{R,\min} = 2mg\sqrt{KC_{D,0}}$, the expression under the inner root equals $T_A^2 - T_{R,\min}^2$. If the thrust available is less than the minimum thrust required, there is no level flight at all.

**For a propeller aircraft**, we set $P_A = P_R$ in [](#eq-p51-PR):

$$
\tfrac12 \rho S C_{D,0}\,V^3 + \frac{2K(mg)^2}{\rho S V} = P_A
$$

Multiplied by $V$, this is a quartic equation in $V$, with no handy closed form. At the maximum speed the induced power is small, so we solve for the $V^3$ term and put the previous guess of $V$ in the small induced term. Taking the cube root gives an iteration:

:::{math}
:label: eq-p51-vmax-prop
V_{k+1} = \left[\frac{2}{\rho S C_{D,0}}\left(P_A - \frac{2K(mg)^2}{\rho S V_k}\right)\right]^{1/3}
:::

We start the iteration from $V_0 = [2P_A/(\rho S C_{D,0})]^{1/3}$, the speed with no induced drag, and two to four passes give four figures.

:::{figure} figures/p51-available-and-vmax.svg
:label: fig-p51-available-and-vmax
:alt: Two graphs at sea level. Left, the executive jet: thrust in kilonewtons against true airspeed from 0 to 320 meters per second, with gray bands below stall and past Mach 0.80, labeled wave drag. A dashed horizontal line T sub A at 55.6 kilonewtons meets the solid U-shaped T sub R curve at a filled diamond, V max equal to 258.5 meters per second, with a drop line. Right, the general-aviation airplane: power in kilowatts against speed from 0 to 100 meters per second. A dashed line P sub A at 172.8 kilowatts meets the solid P sub R curve at a diamond, V max equal to 85.51 meters per second. In each graph a dimension line labeled level flight possible runs from the stall speed to V max.
:width: 85%

Computed for the two aircraft at sea level and full throttle. Level flight is possible from the stall speed to the speed where available equals required. The jet's maximum speed lies just inside the range where its polar applies.
:::

:::{tip} Method: minimum thrust, minimum power, and maximum speed
1. Find the density at the altitude from the standard atmosphere, and the weight $mg$ in newtons.
2. Compute $T_{R,\min}$ and $V_{T_R,\min}$ from [](#eq-p51-min-thrust), then $V_{P_R,\min}$ and $P_{R,\min}$ from [](#eq-p51-min-power).
3. Compute $T_A$ or $P_A$ at that density, with all running engines.
4. For a jet use [](#eq-p51-vmax-jet); for a propeller aircraft iterate [](#eq-p51-vmax-prop) until $V$ stops changing.
5. Check the low end against the stall speed, and the Mach number at the maximum speed against the range where the polar applies.
:::

(p51-example-2)=
### Worked example 2: minimum thrust, minimum power, and maximum speed at sea level

**(a) The executive jet.** It has $m = 33{,}100$ kg, $S = 88.2$ m², $C_{D,0} = 0.015$, $K = 0.050$, and two engines of $T_0 = 27{,}810$ N, so $T_A = 55{,}620$ N at sea level. Its clean $C_{L,\max}$ of 1.6 is assumed, and so is the Mach number up to which its polar applies, 0.80.

1. **Weight and minimum thrust**, [](#eq-p51-min-thrust):
   $$
   \begin{aligned}
   mg &= 33{,}100 \times 9.81\\
      &= 324{,}711\ \text{N}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   &\sqrt{K C_{D,0}}\\
   &\;\;\;= \sqrt{0.050 \times 0.015}\\
   &\;\;\;= 0.027386
   \end{aligned}
   $$
   $$
   \begin{aligned}
   T_{R,\min} &= 2 \times 324{,}711 \times\\
              &\;\;\; 0.027386\\
              &= 17{,}785\ \text{N}
   \end{aligned}
   $$
   So $(L/D)_{\max} = 1/(2 \times 0.027386) = 18.26$.
2. **The two speeds.** Both share the factor $\sqrt{2mg/(\rho S)}$:
   $$
   \begin{aligned}
   &\sqrt{\frac{2 \times 324{,}711}{1.2250 \times 88.2}}\\
   &\;\;\;= 77.528\ \text{m/s}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   V_{T_R,\min} &= 77.528 \times 1.3512\\
                &= 104.8\ \text{m/s}\\
   V_{P_R,\min} &= 77.528 \times 1.0267\\
                &= 79.60\ \text{m/s}
   \end{aligned}
   $$
   Here $1.3512 = (0.050/0.015)^{1/4}$ and $1.0267 = (0.050/0.045)^{1/4}$.
3. **Minimum power.** At $V_{P_R,\min}$ the lift coefficient is $\sqrt{3C_{D,0}/K}$ and $C_D = 4C_{D,0} = 0.060$, so
   $$
   \begin{aligned}
   C_L &= \sqrt{0.045/0.050}\\
       &= 0.94868\\
   T_R &= \frac{324{,}711 \times 0.060}{0.94868}\\
       &= 20{,}537\ \text{N}\\
   P_{R,\min} &= 20{,}537 \times 79.60\\
              &= 1{,}634{,}745\ \text{W}
   \end{aligned}
   $$
   That is 1,635 kW, the same as [](#eq-p51-min-power) gives.
4. **Maximum speed**, [](#eq-p51-vmax-jet):
   $$
   \begin{aligned}
   \rho S C_{D,0} &= 1.2250 \times 88.2 \times\\
                  &\;\;\; 0.015\\
                  &= 1.6207\ \text{kg/m}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   &\sqrt{T_A^2 - T_{R,\min}^2}\\
   &\;\;\;= \sqrt{{55{,}620}^{2} - {17{,}785}^{2}}\\
   &\;\;\;= 52{,}700\ \text{N}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   V_{\max} &= \sqrt{\frac{55{,}620 + 52{,}700}{1.6207}}\\
            &= 258.5\ \text{m/s}
   \end{aligned}
   $$
5. **Checks.** With the speed of sound at sea level, 340.3 m/s, the Mach number is $258.5/340.3 = 0.760$, just below 0.80, which is reached at 272.2 m/s. The low-speed crossing is 42.45 m/s, below the stall speed of 61.29 m/s. So at sea level, the jet can fly level from 61.29 m/s to 258.5 m/s.

**(b) The general-aviation airplane.** Its minimum power follows the same steps as the jet's, from the shared factor $\sqrt{2mg/(\rho S)}$:

$$
\begin{aligned}
&\sqrt{\frac{2 \times 12{,}900}{1.2250 \times 16.3}}\\
&\;\;\;= 35.95\ \text{m/s}
\end{aligned}
$$

$$
\begin{aligned}
V_{P_R,\min} &= 35.95 \times 0.9122\\
             &= 32.79\ \text{m/s}\\
C_L &= \sqrt{0.078/0.054}\\
    &= 1.2019\\
T_R &= \frac{12{,}900 \times 0.104}{1.2019}\\
    &= 1{,}116.2\ \text{N}\\
P_{R,\min} &= 1{,}116.2 \times 32.79\\
           &= 36{,}600\ \text{W}
\end{aligned}
$$

Here $0.9122 = (0.054/0.078)^{1/4}$ and $C_D = 4 \times 0.026 = 0.104$. The minimum power is 36.60 kW, and the power available is 172.8 kW, or 172,800 W. The iteration needs two numbers:

$$
\begin{aligned}
\rho S C_{D,0} &= 1.2250 \times 16.3 \times\\
               &\;\;\; 0.026\\
               &= 0.51916\ \text{kg/m}\\
\frac{2K(mg)^2}{\rho S} &= \frac{2 \times 0.054}{1.2250 \times 16.3}\times\\
                        &\;\;\; {12{,}900}^{2}\\
                        &= 900{,}077\ \text{W\,m/s}
\end{aligned}
$$

Then the passes of [](#eq-p51-vmax-prop) give:

$$
\begin{aligned}
V_0 &= \left(\frac{2 \times 172{,}800}{0.51916}\right)^{1/3}\\
    &= 87.32\ \text{m/s}\\
V_1 &= \Big[\frac{2}{0.51916}\times\\
    &\;\;\; \Big(172{,}800 - \frac{900{,}077}{87.32}\Big)\Big]^{1/3}\\
    &= 85.54\ \text{m/s}\\
V_2 &= \Big[\frac{2}{0.51916}\times\\
    &\;\;\; \Big(172{,}800 - \frac{900{,}077}{85.54}\Big)\Big]^{1/3}\\
    &= 85.51\ \text{m/s}
\end{aligned}
$$

The next pass gives 85.51 m/s again, so $V_{\max} = 85.51$ m/s. The airplane can fly level from its stall speed, 23.20 m/s, to 85.51 m/s.

**Check.** At this speed the parasite power is 162.3 kW and the induced power 10.5 kW, which add up to 172.8 kW.

(p51-altitude)=
## Effect of altitude

Aircraft spend much of their flight high above sea level, so the next question is what thin air does to each curve. We take one point of the thrust-required curve, at one lift coefficient, and follow it up.

1. **The speed.** The lift equation gives $V = \sqrt{2mg/(\rho S C_L)}$. At the same $C_L$ the speed grows as $\sqrt{\rho_0/\rho}$.
2. **The thrust.** By [](#eq-p51-TR-LD), $T_R = mg\,C_D/C_L$ has no density in it, so it does not change.
3. **The power.** $P_R = T_R V$ is the same thrust times a higher speed, so it grows as $\sqrt{\rho_0/\rho}$ too.

Every point of the $T_R$ curve slides to the right by the factor $\sqrt{\rho_0/\rho}$, at the same height. Every point of the $P_R$ curve moves right and up by that factor. As a result, the minimum thrust stays the same while its speed grows, and both the minimum power and its speed grow. The stall speed, $\sqrt{2mg/(\rho S C_{L,\max})}$, grows by the same factor, so the low end of the speed range moves right as well. Meanwhile the engines lose output as $(\rho/\rho_0)^{m_{\text{ad}}}$.

In {numref}`tbl-p51-thrust-altitude`, we follow the jet's thrust available up through the atmosphere of page 1.4, against its minimum thrust required of 17,785 N.

:::{table} Thrust available of the executive jet at full throttle against its minimum thrust required, 17,785 N at every altitude. Densities from the standard atmosphere of page 1.4.
:label: tbl-p51-thrust-altitude
:align: center

| Altitude, m | Density, kg/m³ | Thrust available, N | Thrust available minus minimum required, N |
| ---: | ---: | ---: | ---: |
| 0 | 1.22500 | 55,620 | 37,835 |
| 1,000 | 1.11158 | 52,470 | 34,685 |
| 5,000 | 0.73589 | 40,967 | 23,182 |
| 10,000 | 0.41243 | 28,944 | 11,159 |

:::

The margin shrinks as the jet climbs, but at 10,000 m it can still fly level. Higher up, the thrust available falls to the minimum thrust required, and above that altitude no level flight is possible. That altitude is the ceiling of [page 5.3](#p53-ceilings).

{numref}`fig-p51-altitude-jet` shows the same changes on the curves of the jet.

:::{figure} figures/p51-altitude-jet.svg
:label: fig-p51-altitude-jet
:alt: Two graphs of thrust in kilonewtons against true airspeed for the executive jet: sea level on the left in black, 9,500 m on the right in blue with open triangles. Each has gray bands below stall and past Mach 0.80, labeled wave drag. A thin gray line at 17.79 kilonewtons, labeled minimum thrust, runs across both. At sea level the solid T sub R curve touches it at 104.8 meters per second and meets the dashed T sub A line at 55.6 kilonewtons at a diamond, V max 258.5 meters per second. At 9,500 m the T sub R curve touches the same line at 175.1 meters per second, and the dashed T sub A line at about 30 kilonewtons crosses the curve only inside the Mach band, where both are drawn thin.
:width: 85%

Computed for the executive jet at sea level and 9,500 m. Altitude slides the thrust-required curve to the right at the same minimum while the thrust available drops toward it. At 9,500 m the crossing lies past Mach 0.80, where the polar no longer applies, so no maximum speed is marked.
:::

{numref}`fig-p51-altitude-prop` shows them for the general-aviation airplane, whose excess power shrinks from both sides.

:::{figure} figures/p51-altitude-prop.svg
:label: fig-p51-altitude-prop
:alt: Graph of power in kilowatts against true airspeed from 0 to 120 meters per second for the general-aviation airplane, at sea level in black and at 6,500 m in blue with open triangles on both of its lines. Solid curves are power required and dashed horizontal lines power available, 172.8 kilowatts at sea level and 115.2 at 6,500 m. The 6,500 m curve starts at a higher speed and lies above and to the right of the sea-level curve. Vertical arrows at each minimum, labeled excess power, are shorter at 6,500 m. Filled diamonds mark the maximum speeds, 85.51 meters per second at sea level and 89.75 at 6,500 m. A gray band marks the speeds below stall at sea level.
:width: 85%

Computed for the general-aviation airplane at sea level and 6,500 m. At altitude the power required moves up and right and the power available comes down, so the excess power shrinks. Each power-required curve starts at its own stall speed.
:::

### When the maximum speed rises and when it falls

To see whether the maximum speed rises with altitude, we look at the engine, because near $V_{\max}$ the parasite drag dominates. For a jet, $T_A \approx \tfrac12\rho V_{\max}^2 S C_{D,0}$, so $V_{\max}^2 \approx 2T_A/(\rho S C_{D,0})$. The thrust available goes as $\rho^{m_{\text{ad}}}$, so $V_{\max}^2$ goes as $\rho^{m_{\text{ad}}-1}$. A propeller aircraft gives the same exponent for $V_{\max}^3$.

- If $m_{\text{ad}} < 1$, the engine loses output more slowly than the parasite drag falls. The maximum speed then rises with altitude, as long as the induced drag at the maximum speed stays small, as for our two aircraft.
- If $m_{\text{ad}} \ge 1$, the maximum speed does not rise.

In both cases the induced drag grows with altitude and pulls the maximum speed down. Near the ceiling the maximum speed falls and closes onto the low end, and a jet at its ceiling can fly only at $V_{T_R,\min}$. Many textbook sketches show the maximum speed lower at altitude (Anderson 2016, Chapter 6). That trend is real above some altitude, or for an engine that loses output fast.

### Worked example 3: the two aircraft at altitude

**(a) The executive jet at 9,500 m**, where $\rho = 0.4386$ kg/m³ and $\rho/\rho_0 = 0.3580$.

1. **Thrust available and minimum-thrust speed:**
   $$
   \begin{aligned}
   T_A &= 55{,}620 \times\\
       &\;\;\; {0.3580}^{0.6}\\
       &= 30{,}030\ \text{N}\\
   V_{T_R,\min} &= 104.8 \times 1.671\\
                &= 175.1\ \text{m/s}
   \end{aligned}
   $$
   Here $1.671 = \sqrt{1.2250/0.4386}$. The minimum thrust is still 17,785 N, and the stall speed has moved up to 102.4 m/s.
2. **Where the polar stops.** The speed of sound at 9,500 m is 301.6 m/s, so Mach 0.80 is 241.3 m/s. At that speed the thrust required is
   $$
   \begin{aligned}
   q &= 0.5 \times 0.4386 \times\\
     &\;\;\; {241.3}^{2}\\
     &= 12{,}769\ \text{Pa}\\
   qS &= 12{,}769 \times 88.2\\
      &= 1{,}126{,}226\ \text{N}\\
   D_0 &= 1{,}126{,}226 \times 0.015\\
       &= 16{,}893\ \text{N}\\
   D_i &= \frac{K (mg)^2}{qS}\\
       &= \frac{0.050 \times {324{,}711}^{2}}{1{,}126{,}226}\\
       &= 4{,}681\ \text{N}\\
   T_R &= 16{,}893 + 4{,}681\\
       &= 21{,}574\ \text{N}
   \end{aligned}
   $$
   The jet has 30,030 N, more than it needs at Mach 0.80. Its thrust-limited maximum speed lies past Mach 0.80, where [](#eq-p51-vmax-jet) no longer applies. In reality {term}`wave drag`, which our polar leaves out, sets the maximum speed there ([page 3.3](#p33-drag-speed) shows the same limit).

**(b) The general-aviation airplane at 6,500 m**, where $\rho = 0.6236$ kg/m³ and $\rho/\rho_0 = 0.50906$.

$$
\begin{aligned}
P_A &= 172.8 \times {0.50906}^{0.6}\\
    &= 115.24\ \text{kW}\\
V_{P_R,\min} &= 32.79 \times 1.4016\\
             &= 45.96\ \text{m/s}\\
P_{R,\min} &= 36.60 \times 1.4016\\
           &= 51.30\ \text{kW}
\end{aligned}
$$

Here $1.4016 = \sqrt{1.2250/0.6236}$. The power available fell by about a third, and the minimum power required rose by more than a third. The maximum speed comes from [](#eq-p51-vmax-prop) with $P_A = 115{,}240$ W and the density at 6,500 m:

$$
\begin{aligned}
\rho S C_{D,0} &= 0.6236 \times 16.3 \times\\
               &\;\;\; 0.026\\
               &= 0.26428\ \text{kg/m}\\
\frac{2K(mg)^2}{\rho S} &= \frac{2 \times 0.054}{0.6236 \times 16.3}\times\\
                        &\;\;\; {12{,}900}^{2}\\
                        &= 1{,}768{,}111\ \text{W\,m/s}
\end{aligned}
$$

$$
\begin{aligned}
V_0 &= \left(\frac{2 \times 115{,}240}{0.26428}\right)^{1/3}\\
    &= 95.54\ \text{m/s}\\
V_1 &= \Big[\frac{2}{0.26428}\times\\
    &\;\;\; \Big(115{,}240 -\\
    &\;\;\;\;\;\; \frac{1{,}768{,}111}{95.54}\Big)\Big]^{1/3}\\
    &= 90.13\ \text{m/s}
\end{aligned}
$$

The induced power is larger up here, so the iteration needs more passes. The next ones give 89.78, 89.76, and 89.75 m/s, and then 89.75 m/s again, so $V_{\max} = 89.75$ m/s. That is faster than the 85.51 m/s at sea level. This engine has $m_{\text{ad}} = 0.6$, below 1, so the maximum speed still rises at this altitude, as the section above predicts.

## Summary

:::{important} Summary
- Steady level flight with a small angle of attack gives $L = mg = \tfrac12\rho V^2 S C_L$ and $T_R = D = mg/(L/D)$; $P_R = T_R V$. Check every answer against $C_{L,\max}$ and against the thrust or power available.
- Minimum thrust comes at $C_L = \sqrt{C_{D,0}/K}$, the same at every altitude. Minimum power comes at $C_L = \sqrt{3C_{D,0}/K}$ and $V_{P_R,\min} = 0.7598\,V_{T_R,\min}$; a line from the origin touches the power curve at $V_{T_R,\min}$.
- A jet's thrust and a propeller's power are nearly flat with speed and fall as $(\rho/\rho_0)^{m_{\text{ad}}}$. Level flight runs from the stall speed to $V_{\max}$, where available equals required.
- With altitude the required curves move right by $\sqrt{\rho_0/\rho}$, the available curves fall, and the speed range closes toward the ceiling.
:::

:::{table} The equations of this page.
:label: tbl-p51-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Steady level flight | $L = mg = \tfrac12\rho V^2 S C_L$, $T_R = D = mg/(L/D)$ |
| Thrust required | $T_R = \tfrac12\rho V^2 S C_{D,0} + 2K(mg)^2/(\rho S V^2)$ |
| Power required | $P_R = T_R V = \tfrac12\rho V^3 S C_{D,0} + 2K(mg)^2/(\rho S V)$ |
| Minimum thrust | $C_L = \sqrt{C_{D,0}/K}$, $T_{R,\min} = 2mg\sqrt{KC_{D,0}}$ |
| Minimum-thrust speed | $V_{T_R,\min} = \sqrt{2mg/(\rho S)}\,(K/C_{D,0})^{1/4}$ |
| Power required from the coefficients | $P_R = \sqrt{2(mg)^3/(\rho S)}\,C_D/C_L^{3/2}$ |
| Minimum power | $C_L = \sqrt{3C_{D,0}/K}$, $P_{R,\min} = (4/{3}^{3/4})\sqrt{2(mg)^3/(\rho S)}\,K^{3/4}C_{D,0}^{1/4}$ |
| Minimum-power speed | $V_{P_R,\min} = \sqrt{2mg/(\rho S)}\,(K/(3C_{D,0}))^{1/4}$ |
| Jet thrust available | $T_A = n\,\delta_t\,T_0(\rho/\rho_0)^{m_{\text{ad}}}$, $P_A = T_A V$ |
| Propeller power available | $P_A = n\,\delta_t\,\eta\,P_0(\rho/\rho_0)^{m_{\text{ad}}}$, $T_A = P_A/V$ |
| Jet maximum speed | $V_{\max} = \sqrt{(T_A + \sqrt{T_A^2 - 4C_{D,0}K(mg)^2})/(\rho S C_{D,0})}$ |
| Propeller maximum speed (iterate) | $V_{k+1} = [2(P_A - 2K(mg)^2/(\rho S V_k))/(\rho S C_{D,0})]^{1/3}$ |

:::

:::{exercise} For discussion
:label: ex-p51-discussion

1. Why does the minimum thrust required stay the same as an aircraft climbs, while the minimum power required grows?
2. On a plot of $P_R$ against $V$, how can you find both $V_{P_R,\min}$ and $V_{T_R,\min}$ with only a ruler?
3. An airplane flies level, slower than its minimum-power speed. If the pilot slows down further and holds altitude, must the power go up or down? Why does that matter on a slow approach to land?
4. At 9,500 m the executive jet still has spare thrust at Mach 0.80. What limits its real maximum speed there, and how would its thrust-required curve look past Mach 0.80?
5. Two airplanes have the same polar and wing loading. One engine has $m_{\text{ad}} = 0.6$ and the other $m_{\text{ad}} = 1.0$. Which airplane's maximum speed rises as it climbs, and why?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-5-1.html
:label: quiz-5-1
:width: 100%
:enumerated: false

Quiz for Standard 5.1: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 6, "Elements of Airplane Performance."
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023. Chapter 5, "Aerodynamics of Flight" (p. 5-29, propellers), and Chapter 11, "Aircraft Performance" (pp. 11-5 to 11-6 and 11-11 to 11-12).
