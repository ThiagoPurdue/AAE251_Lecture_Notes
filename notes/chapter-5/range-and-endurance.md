---
title: "5.2 Range and Endurance"
short_title: 5.2 Range and Endurance
---

:::{include} ../_parts/standards/5.2.md
:::

Two questions come up for every aircraft that carries a load of fuel. The first is how far it can fly on that fuel, which is its {term}`range`. The second is how long it can stay in the air on that fuel, which is its {term}`endurance`. For an airliner on a long route, range is the main concern. For an aircraft that must circle over one place, endurance matters most. Both depend on three things: the amount of fuel the aircraft carries, how fast its engines burn that fuel, and its aerodynamics, which here means its drag polar.

On [page 1.6](../chapter-1/aircraft-sizing.md) we used the jet range and endurance equations to size an aircraft, with typical values of the fuel consumption and of $L/D$. On this page we derive them from the fuel flow of the engine and the balance of forces of [steady level flight](#p51-level-flight), for a jet and for a propeller aircraft. Then we find the flight condition that gives the most range and the most endurance for each. Last, we see why a jet cruises high and a propeller aircraft does not need to.

:::{note} What to take from this page
- A jet burns fuel in proportion to its thrust, a propeller aircraft in proportion to its shaft power. So the two have different range and endurance equations, the Breguet equations.
- Jet range peaks at the largest $C_L^{1/2}/C_D$, jet endurance and propeller range at the largest $C_L/C_D$, and propeller endurance at the largest $C_L^{3/2}/C_D$. Each lift coefficient is $\sqrt{3}$ times the one before it.
- The three best speeds are $0.760$, $1$, and $1.316$ times the minimum-thrust speed, for propeller endurance, jet endurance and propeller range, and jet range.
- Jet range grows with altitude, until the jet reaches its Mach limit or its engines can no longer give the best-range thrust. Propeller range does not change with altitude, and propeller endurance is best low.
:::

(p52-fuel-consumption)=
## Fuel consumption: jets and propellers

To find how far or how long the aircraft flies, the first thing to know is how fast it loses weight. Every second, the engines burn some fuel, and the aircraft gets lighter by the weight of that fuel. How much they burn depends on the kind of engine.

A **jet engine** burns fuel in proportion to the thrust it makes. This is the same idea as for a rocket on [page 4.1](../chapter-4/thrust-and-specific-impulse.md), where the thrust and the propellant flow go together. The weight of fuel burned per second is

:::{math}
:label: eq-p52-fuel-jet
\frac{d(mg)}{dt} = -c_t\,T
:::

with $T$ the thrust the engines make. The constant $c_t$ is the **{term}`thrust specific fuel consumption`**, defined as the weight of fuel burned per unit of thrust per unit of time. Its unit is N of fuel per N of thrust per second, so $\text{N}/(\text{N}\cdot\text{s}) = 1/\text{s}$. The minus sign indicates that the weight goes down. Page 1.6 wrote the same quantity as $C$, in 1/h ([its definition](#def-p16-sfc)). Engine data are usually quoted in 1/h, so we divide by $3{,}600$ s/h to get $c_t$ in 1/s.

A **propeller aircraft** has a piston engine or a turbine that turns a shaft, and the propeller turns the shaft power into thrust power. The engine burns fuel in proportion to the shaft power. The propeller delivers the power $P$ to the air with an efficiency $\eta$, so the shaft power is $P/\eta$, and

:::{math}
:label: eq-p52-fuel-prop
\frac{d(mg)}{dt} = -c\,\frac{P}{\eta}
:::

The constant $c$ is the **{term}`power specific fuel consumption`**, defined as the weight of fuel burned per unit of shaft power per unit of time. Its unit is $\text{N}/(\text{W}\cdot\text{s})$. A watt is a newton meter per second, so this is $\text{N}/(\text{N}\cdot\text{m}) = 1/\text{m}$.

Engine data give this constant as a mass of fuel per unit of energy, for example in grams per kilowatt-hour. Divided by $3{,}600$ s/h, it is in grams per second for each kilowatt, and we call it $c_\text{m}$. Multiplying by $g$ and converting the units turns $c_\text{m}$ into the weight-based $c$:

$$
\begin{aligned}
c &= c_\text{m}\,\frac{\text{g}}{\text{s}\cdot\text{kW}}\times\frac{1\ \text{kg}}{1{,}000\ \text{g}}\\
&\;\;\;\times 9.81\ \frac{\text{N}}{\text{kg}}\times\frac{1\ \text{kW}}{1{,}000\ \text{W}}\\
&= c_\text{m}\times 9.81\times{10}^{-6}\ \text{1/m}
\end{aligned}
$$

For an engine that burns $0.076$ g/(s·kW), $c = 7.4556 \times {10}^{-7}$ 1/m.

:::{warning} $c_t$ and $c$ are weight rates, not mass rates
Both constants count the weight of fuel burned, not its mass. If you are given a mass flow of fuel, in kg/s per newton or g/s per kilowatt, multiply by $g$ before you use it in the equations of this page. Also keep the two units apart: $c_t$ is in 1/s and $c$ in 1/m. If you put a jet's $c_t$ in 1/h into a range equation, your answer is off by a factor of $3{,}600$.
:::

(p52-assumptions)=
## The assumptions behind the equations

The results apply only as far as their assumptions do, so before we integrate, we state what stays fixed. We make five assumptions.

1. **The specific fuel consumption is constant**, whatever the speed, altitude, and throttle setting. A real engine's value changes with all three.
2. **The angle of attack is small**, so the thrust acts nearly along the flight path.
3. **The thrust is much smaller than the lift**, so the part of the thrust that supports the aircraft, $T\sin\alpha$, is negligible against $L$.
4. **The weight falls slowly**, so at every moment the aircraft is in [steady level flight](#p51-level-flight): $L = mg$ and $T = D$.
5. **The air is still and the atmosphere does not change**, so the distance through the air is the distance over the ground.

With assumptions 2 to 4, the aircraft is in steady level flight at each moment. The thrust $T$ equals the thrust required $T_R$, and the lift balance gives the speed:

$$
\begin{aligned}
T_R &= \frac{mg}{C_L/C_D}\\
V &= \sqrt{\frac{2mg}{\rho S C_L}}
\end{aligned}
$$

The first line is the thrust required of [page 5.1](#eq-p51-TR-LD).

(p52-jet-breguet)=
## Jet range and endurance

Now we combine the fuel law of the jet with these two results, keeping the altitude and the lift coefficient constant. A constant altitude fixes the density $\rho$. A constant $C_L$ fixes $C_D$ through the polar, so the pilot maintains one angle of attack.

### Jet endurance

We solve [](#eq-p52-fuel-jet) for the time $dt$ in which a small weight of fuel $d(mg)$ is burned, and put in the thrust required:

$$
\begin{aligned}
dt &= -\frac{d(mg)}{c_t\,T_R}\\
&= -\frac{1}{c_t}\,\frac{C_L}{C_D}\,\frac{g\,dm}{mg}\\
&= -\frac{1}{c_t}\,\frac{C_L}{C_D}\,\frac{dm}{m}
\end{aligned}
$$

Here $g$ is constant, so $d(mg) = g\,dm$, and $g$ cancels. The endurance $E$ is the time it takes for the mass to fall from $m_1$ at the start to $m_2$ at the end, where $m_1 - m_2$ is the fuel burned. With $c_t$, $C_L$, and $C_D$ constant they come out of the integral, and the integral of $1/m$ is $\ln m$:

$$
\begin{aligned}
E &= -\frac{1}{c_t}\,\frac{C_L}{C_D}\int_{m_1}^{m_2}\frac{dm}{m}\\
&= \frac{1}{c_t}\,\frac{C_L}{C_D}\,(\ln m_1 - \ln m_2)
\end{aligned}
$$

::::{prf:definition} Breguet endurance equation for a jet
:label: def-p52-jet-endurance
:::{math}
:label: eq-p52-jet-E
E = \frac{1}{c_t}\,\frac{C_L}{C_D}\,\ln\frac{m_1}{m_2}
:::
with $c_t$ in 1/s, $E$ in seconds, and $m_1$ and $m_2$ the masses at the start and at the end.
::::

There is no density in this equation. The time a jet can stay up depends on its $L/D$, its engines, and its fuel, not on its altitude. Keep the start mass on top of the logarithm, because writing $\ln(m_2/m_1)$ gives you a negative time.

### Jet range

For the range we follow the distance $x$ instead of the time. In a time $dt$ the aircraft covers $dx = V\,dt$. Putting in $dt$ from above and the speed from the lift balance gives:

$$
\begin{aligned}
dx &= V\,dt\\
&= -\sqrt{\frac{2mg}{\rho S C_L}}\;\frac{1}{c_t}\,\frac{C_L}{C_D}\,\frac{dm}{m}
\end{aligned}
$$

Next we collect what depends on the mass and what depends on the lift coefficient. The mass appears as $\sqrt{m}/m = 1/\sqrt{m}$, and the lift coefficient as $C_L/\sqrt{C_L} = \sqrt{C_L}$:

$$
dx = -\frac{1}{c_t}\sqrt{\frac{2g}{\rho S}}\;\frac{\sqrt{C_L}}{C_D}\;\frac{dm}{\sqrt{m}}
$$

The range is $R = x_2 - x_1$, the distance from where the mass is $m_1$ to where it is $m_2$. The limits of the integral change from distances to masses. The integral of $m^{-1/2}$ is $2\sqrt{m}$:

$$
\begin{aligned}
R &= -\frac{1}{c_t}\sqrt{\frac{2g}{\rho S}}\,\frac{\sqrt{C_L}}{C_D}\\
&\;\;\;\times\int_{m_1}^{m_2}\frac{dm}{\sqrt{m}}\\
&= \frac{2}{c_t}\sqrt{\frac{2g}{\rho S}}\,\frac{\sqrt{C_L}}{C_D}\\
&\;\;\;\times\left(\sqrt{m_1} - \sqrt{m_2}\right)
\end{aligned}
$$

::::{prf:definition} Breguet range equation for a jet
:label: def-p52-jet-range
:::{math}
:label: eq-p52-jet-R
\begin{aligned}
R &= \frac{2}{c_t}\sqrt{\frac{2g}{\rho S}}\,\frac{\sqrt{C_L}}{C_D}\\
&\;\;\;\times\left(\sqrt{m_1} - \sqrt{m_2}\right)
\end{aligned}
:::
with $c_t$ in 1/s, for flight at constant altitude and constant lift coefficient.
::::

Some books write $\sqrt{C_L}/C_D$ as $\sqrt{C_L/C_D^2}$ under the root. It is the same quantity. This time the density stays in the equation, so thinner air gives a longer range. The [side-by-side comparison](#p52-altitude) comes back to this.

Page 1.6 wrote the jet range with the speed kept constant ([its range equation](#eq-p16-range)). Since $mg = \tfrac12\rho V^2 S C_L$, a constant speed and a constant $C_L$ need the density to fall with the mass, so that aircraft drifts up as it gets lighter. Here we keep the altitude constant instead.

### What the pilot does as the fuel burns

At constant altitude and constant $C_L$, the speed $V = \sqrt{2mg/(\rho S C_L)}$ falls as the square root of the mass. The thrust required, $mg/(C_L/C_D)$, falls in proportion to the mass. So the pilot slows down and throttles back as the fuel burns ({numref}`fig-p52-weight-burn`). The Federal Aviation Administration describes the same cruise control, noting that as the weight decreases, the best speed and power setting decrease, or the best altitude increases (FAA 2023, Chapter 11, p. 11-10).

:::{figure} figures/p52-weight-burn.svg
:label: fig-p52-weight-burn
:alt: Two panels against distance flown from 0 to 3,500 kilometers, for the executive jet flying 3,300 kilometers at 8,500 meters at the best-range lift coefficient. Left panel: a solid black line for the true airspeed falls from 216.9 meters per second at the start to 200.1 meters per second at the end. Right panel: a dashed black horizontal line for full throttle, T sub A, at 32.29 kilonewtons; below it a solid black line for the thrust required falls from 20.54 kilonewtons, throttle setting 0.6361, to 17.48 kilonewtons, throttle setting 0.5413.
:width: 85%

Computed for worked example 2, showing the executive jet at 8,500 m and the best-range lift coefficient. As the fuel burns, the speed falls with the square root of the mass and the thrust required falls in proportion to the mass, so the pilot eases the throttle back from 0.6361 to 0.5413. The axes start at zero, showing that the changes are real but modest on one leg.
:::

(p52-jet-best)=
## Best conditions for a jet

What the pilot should fly follows from the two equations. In each, the only thing the pilot chooses in flight is the lift coefficient, set by the angle of attack. The task is to find the $C_L$ that makes the aerodynamic part largest.

### Best endurance

[](#eq-p52-jet-E) is largest where $C_L/C_D$ is largest. That is the maximum lift-to-drag ratio found [on page 3.3](#p33-minimum-drag):

$$
\begin{aligned}
C_L &= \sqrt{\frac{C_{D,0}}{K}}\\
C_D &= 2C_{D,0}\\
\left(\frac{L}{D}\right)_{\max} &= \frac{1}{2\sqrt{K C_{D,0}}}
\end{aligned}
$$

This is the point of minimum thrust required on [page 5.1](#eq-p51-min-thrust), flown at the speed $V_{T_R,\min}$. That makes physical sense, because a jet burns fuel in proportion to thrust, so the minimum thrust means the least fuel per second.

### Best range

[](#eq-p52-jet-R) is largest where $C_L^{1/2}/C_D$ is largest. We write it with the polar and set its derivative to zero.

1. **The ratio with the polar:**
   $$
   \frac{C_L^{1/2}}{C_D} = \frac{C_L^{1/2}}{C_{D,0} + K C_L^2}
   $$
2. **The quotient rule.** The derivative is the derivative of the top times the bottom, minus the top times the derivative of the bottom, all over the bottom squared, $C_D^2$. Its top is
   $$
   \begin{aligned}
   N &= \tfrac12 C_L^{-1/2}\left(C_{D,0} + K C_L^2\right)\\
   &\;\;\; - C_L^{1/2}\,(2KC_L)
   \end{aligned}
   $$
3. **Set the top to zero**, $N = 0$, and multiply it by $2C_L^{1/2}$:
   $$
   \begin{aligned}
   &C_{D,0} + K C_L^2 - 4KC_L^2 = 0\\
   &C_{D,0} = 3KC_L^2
   \end{aligned}
   $$
4. **Solve for the lift coefficient and find the drag coefficient:**
   :::{math}
   :label: eq-p52-jet-opt-R
   \begin{aligned}
   C_L &= \sqrt{\frac{C_{D,0}}{3K}}\\
   C_D &= C_{D,0} + \tfrac13 C_{D,0}\\
   &= \tfrac43\,C_{D,0}
   \end{aligned}
   :::

The ratio is zero at $C_L = 0$ and falls toward zero at large $C_L$, so this single point is the maximum. Some books maximize $C_L/C_D^2$ instead. That is the square of the ratio above, and a positive quantity and its square peak at the same $C_L$, so the answer is the same.

Notice what step 3 shows. At best range, the induced drag $KC_L^2$ is one third of the parasite drag $C_{D,0}$. The jet flies faster than at minimum thrust. Since $V$ is proportional to $1/\sqrt{C_L}$ at a given weight and altitude, and this $C_L$ is the one of minimum thrust divided by $\sqrt{3}$,

$$
\begin{aligned}
\frac{V_\text{best range}}{V_{T_R,\min}} &= \left(\sqrt{3}\right)^{1/2}\\
&= {3}^{1/4}\\
&= 1.316
\end{aligned}
$$

A jet cruises for range $31.6$% faster than it flies for endurance. Flying faster helps because the engines burn fuel per second in proportion to the thrust, while the distance gained per second grows with the speed. Just above the minimum-thrust speed the thrust curve is nearly flat, so the thrust rises much more slowly than the speed. The best balance comes where $T_R/V$ is smallest, and the [comparison](#p52-comparison) shows that point on a graph.

### Thrust and throttle at best range

Next we need to know whether the engines can maintain this condition. The thrust required at best range is the weight divided by $L/D$ at that point:

$$
\begin{aligned}
T_R &= mg\,\frac{C_D}{C_L}\\
&= mg\,\frac{\tfrac43 C_{D,0}}{\sqrt{C_{D,0}/(3K)}}\\
&= 4mg\sqrt{\frac{K C_{D,0}}{3}}
\end{aligned}
$$

This is $2/\sqrt{3} = 1.155$ times the minimum thrust required, $2mg\sqrt{KC_{D,0}}$. Like the minimum, it depends on the weight and the polar, not on the altitude.

The pilot sets this thrust with the {term}`throttle setting` $\delta_t$, a number from 0, no thrust, to 1, full thrust. With the thrust available of [page 5.1](#eq-p51-TA), $T_A = n\,\delta_t\,T_0(\rho/\rho_0)^{m_\text{ad}}$ for $n$ engines of sea-level thrust $T_0$, the two thrusts match when

:::{math}
:label: eq-p52-throttle
\delta_t = \frac{4mg}{n\,T_0}\left(\frac{\rho_0}{\rho}\right)^{m_\text{ad}}\sqrt{\frac{KC_{D,0}}{3}}
:::

At a constant altitude the throttle setting falls as the mass falls. A value above 1 means the engines cannot give the best-range thrust at that altitude.

### Fuel for a given range or endurance of a jet

Often we know the trip and want the fuel. It comes from solving the two jet equations for $m_2$ and subtracting $m_2$ from $m_1$. From [](#eq-p52-jet-R):

:::{math}
:label: eq-p52-jet-fuel-R
\begin{aligned}
\sqrt{m_2} &= \sqrt{m_1}\\
&\;\;\; - \frac{c_t R}{2}\sqrt{\frac{\rho S}{2g}}\,\frac{C_D}{\sqrt{C_L}}\\
m_\text{fuel} &= m_1 - m_2
\end{aligned}
:::

From [](#eq-p52-jet-E), dividing by the factor in front of the logarithm and taking the exponential of both sides gives:

:::{math}
:label: eq-p52-jet-fuel-E
\begin{aligned}
m_2 &= m_1\exp\left(-c_t E\,\frac{C_D}{C_L}\right)\\
m_\text{fuel} &= m_1\Bigl[1\\
&\;\;\; - \exp\left(-c_t E\,\frac{C_D}{C_L}\right)\Bigr]
\end{aligned}
:::

(p52-prop-breguet)=
## Propeller range and endurance

Now we repeat the steps for a propeller aircraft, which burns fuel in proportion to its power. In steady level flight the power delivered to the air is the power required, $P = P_R = T_R V$. Solving [](#eq-p52-fuel-prop) for $dt$ gives:

$$
\begin{aligned}
dt &= -\frac{\eta}{c}\,\frac{d(mg)}{T_R V}\\
&= -\frac{\eta}{c}\,\frac{C_L}{C_D}\,\frac{dm}{m\,V}
\end{aligned}
$$

### Propeller range

The distance in the time $dt$ is $dx = V\,dt$, and the speed cancels:

$$
dx = -\frac{\eta}{c}\,\frac{C_L}{C_D}\,\frac{dm}{m}
$$

We integrate from $m_1$ to $m_2$ at constant $\eta$, $c$, and $C_L$, as for the jet endurance:

::::{prf:definition} Breguet range equation for a propeller aircraft
:label: def-p52-prop-range
:::{math}
:label: eq-p52-prop-R
R = \frac{\eta}{c}\,\frac{C_L}{C_D}\,\ln\frac{m_1}{m_2}
:::
with $c$ in 1/m and $R$ in meters.
::::

The propeller range has the same form as the jet endurance. It is largest at the maximum $C_L/C_D$, the minimum-thrust point, and it has no density in it. The reason is the same in both cases. Fuel per meter is $(c/\eta)P_R/V = (c/\eta)T_R$, so the least fuel per meter comes at the minimum thrust. The FAA gives the same rule, stating that a propeller aircraft gets its maximum range at the maximum $L/D$. That comes at one angle of attack and one lift coefficient, whatever the weight or altitude (FAA 2023, Chapter 11, p. 11-10).

### Propeller endurance

For the time, the speed does not cancel. Putting in $1/V = \sqrt{\rho S C_L/(2mg)}$:

$$
\begin{aligned}
dt &= -\frac{\eta}{c}\,\frac{C_L}{C_D}\,\sqrt{\frac{\rho S C_L}{2mg}}\,\frac{dm}{m}\\
&= -\frac{\eta}{c}\sqrt{\frac{\rho S}{2g}}\;\frac{C_L^{3/2}}{C_D}\;\frac{dm}{m^{3/2}}
\end{aligned}
$$

The integral of $m^{-3/2}$ is $-2m^{-1/2}$. From $m_1$ to $m_2$:

$$
\begin{aligned}
E &= \frac{\eta}{c}\sqrt{\frac{\rho S}{2g}}\,\frac{C_L^{3/2}}{C_D}\left[\frac{2}{\sqrt{m}}\right]_{m_1}^{m_2}\\
&= \frac{\eta}{c}\,2\sqrt{\frac{\rho S}{2g}}\,\frac{C_L^{3/2}}{C_D}\\
&\;\;\;\times\left(\frac{1}{\sqrt{m_2}} - \frac{1}{\sqrt{m_1}}\right)
\end{aligned}
$$

and $2\sqrt{\rho S/(2g)} = \sqrt{2\rho S/g}$:

::::{prf:definition} Breguet endurance equation for a propeller aircraft
:label: def-p52-prop-endurance
:::{math}
:label: eq-p52-prop-E
\begin{aligned}
E &= \frac{\eta}{c}\sqrt{\frac{2\rho S}{g}}\,\frac{C_L^{3/2}}{C_D}\\
&\;\;\;\times\left(\frac{1}{\sqrt{m_2}} - \frac{1}{\sqrt{m_1}}\right)
\end{aligned}
:::
with $c$ in 1/m and $E$ in seconds.
::::

### Best conditions for a propeller aircraft

Best range comes at the largest $C_L/C_D$, where $C_L = \sqrt{C_{D,0}/K}$ and $C_D = 2C_{D,0}$, at the speed $V_{T_R,\min}$.

Best endurance comes at the largest $C_L^{3/2}/C_D$. The quotient rule again gives, after setting the top to zero and dividing it by $C_L^{1/2}$,

$$
\begin{aligned}
&\tfrac32\left(C_{D,0} + KC_L^2\right) - 2KC_L^2 = 0\\
&C_L = \sqrt{\frac{3C_{D,0}}{K}}
\end{aligned}
$$

There $C_D = C_{D,0} + 3C_{D,0} = 4C_{D,0}$, which means the induced drag is three times the parasite drag. This is the point of [minimum power required](#eq-p51-min-power), as it should be, since a propeller engine burns fuel in proportion to power. Its speed is $V_{P_R,\min} = {3}^{-1/4}\,V_{T_R,\min} = 0.760\,V_{T_R,\min}$.

The density appears in front of [](#eq-p52-prop-E) as $\sqrt{\rho}$, so a propeller aircraft stays up longest flying slowly in dense air, close to the ground.

### Fuel for a given range or endurance of a propeller aircraft

Solving [](#eq-p52-prop-R) and [](#eq-p52-prop-E) for $m_2$ in the same way gives:

:::{math}
:label: eq-p52-prop-fuel
\begin{aligned}
m_\text{fuel} &= m_1\Bigl[1\\
&\;\;\; - \exp\left(-\frac{c}{\eta}\,\frac{C_D}{C_L}\,R\right)\Bigr]\\
\frac{1}{\sqrt{m_2}} &= \frac{1}{\sqrt{m_1}}\\
&\;\;\; + E\,\frac{c}{\eta}\,\frac{C_D}{C_L^{3/2}}\sqrt{\frac{g}{2\rho S}}
\end{aligned}
:::

and then $m_\text{fuel} = m_1 - m_2$ for the endurance.

(p52-comparison)=
## Jets and propeller aircraft side by side

That makes four best conditions. Side by side, they show a pattern that applies to every aircraft with a parabolic polar, and they explain why jets and propeller aircraft cruise so differently.

### Three ratios, three lift coefficients

{numref}`fig-p52-aero-ratios` plots the three aerodynamic ratios for one polar. Each peaks at its own lift coefficient, and each of these lift coefficients is $\sqrt{3} = 1.732$ times the one before it.

:::{figure} figures/p52-aero-ratios.svg
:label: fig-p52-aero-ratios
:alt: Graph of three ratios, each divided by its own maximum, against lift coefficient from 0 to 1.5, for the polar C sub D equals 0.015 plus 0.050 C sub L squared. A dashed blue curve, C sub L to the one-half over C sub D, for jet range, peaks with a blue square at C sub L equals 0.316. A solid black curve, C sub L over C sub D, for jet endurance and propeller range, peaks with a black circle at 0.548. A dotted vermilion curve, C sub L to the three-halves over C sub D, for propeller endurance, peaks with a vermilion triangle at 0.949. Thin dashed lines drop from each peak to the axis.
:width: 85%

Computed for the polar of the executive jet, $C_D = 0.015 + 0.050\,C_L^2$. Each goal has its own best lift coefficient, and each is $\sqrt{3}$ times the one to its left: 0.316, 0.548, and 0.949.
:::

### Three speeds in a fixed order

At a given weight and altitude the speed goes as $1/\sqrt{C_L}$. A factor of $\sqrt{3}$ in $C_L$ is then a factor of ${3}^{1/4} = 1.316$ in speed. For any aircraft with a parabolic polar the three best speeds come in the order of {numref}`fig-p52-speed-order`.

:::{figure} figures/p52-speed-order.svg
:label: fig-p52-speed-order
:alt: A horizontal speed axis, true airspeed divided by V sub T R min, on a logarithmic scale. A vermilion triangle at 0.760 is labeled propeller best endurance, maximum C sub L to the three-halves over C sub D. A black circle at 1.000 is labeled jet best endurance and propeller best range, maximum C sub L over C sub D. A blue square at 1.316 is labeled jet best range, maximum C sub L to the one-half over C sub D. Below, two dimension arrows of equal length between neighboring points, each labeled times 1.316.
:width: 80%

Schematic, valid for any aircraft with a parabolic drag polar. The best speeds are always in this order, each 1.316 times the one before; on a logarithmic scale the two steps are equal lengths.
:::

### Reading the best points off the curves

You can also find all four points on the curves of [page 5.1](#p51-power-required), with no algebra ({numref}`fig-p52-jet-vs-prop-curves`).

- For a **jet**, look at the thrust required, $T_R(V)$. The fuel flow is $c_t T_R$, so the lowest point of the curve gives the best endurance. The fuel per meter is $c_t T_R/V$. That is smallest where the line from the origin to the curve has the least slope, which is the line tangent to the curve. Its point of contact is the best range.
- For a **propeller aircraft**, look at the power required, $P_R(V)$. The fuel flow is $(c/\eta)P_R$, so the lowest point gives the best endurance. The fuel per meter is $(c/\eta)P_R/V$, smallest at the tangent from the origin, which gives the best range.

:::{figure} figures/p52-jet-vs-prop-curves.svg
:label: fig-p52-jet-vs-prop-curves
:alt: Two panels. Left, the executive jet at 8,500 m: thrust required against true airspeed, a solid black U-shaped curve between gray bands, below stall and past Mach 0.80 with wave drag, thin in the second band. Its lowest point, a filled circle, is labeled best endurance, max C sub L over C sub D. A dashed line from an open circle at the origin touches it at an open square, best range, max C sub L to the one-half over C sub D. Right, the general-aviation airplane at 2,500 m: power required, drawn the same way, with best endurance, max C sub L to the three-halves over C sub D, at the lowest point and best range, max C sub L over C sub D, at the tangent point.
:width: 85%

Computed for the executive jet at 8,500 m at the start of worked example 2, and for the general-aviation airplane at 2,500 m with full tanks (worked example 3). On either curve the lowest point is the best endurance and the tangent from the origin is the best range, because fuel per second follows the curve and fuel per meter follows its slope from the origin.
:::

(p52-altitude)=
### Where the density appears

Now look again at the four equations and ask where the density $\rho$ appears ({numref}`fig-p52-altitude-range`).

- **Jet range** carries $1/\sqrt{\rho}$. At the same $C_L$ and weight, thinner air means a higher true airspeed for the same thrust and so the same fuel per second. The jet covers more distance on the same fuel.
- **Jet endurance** has no $\rho$. The minimum thrust does not change with altitude.
- **Propeller range** has no $\rho$. Higher up, the speed and the power required rise by the same factor, so the fuel per meter does not change.
- **Propeller endurance** carries $\sqrt{\rho}$. The minimum power required grows with altitude, so a propeller aircraft stays up longest in dense air.

These results rest on the assumption of a constant $c_t$ or $c$. In a real propeller aircraft, the FAA notes, any change of range with altitude comes from the engine and the propeller (FAA 2023, Chapter 11, p. 11-11).

### How high a jet should cruise

The jet range keeps growing as the air thins, so it seems a jet should fly as high as it can. But the best-range condition stops being possible at two limits, and both come below the {term}`absolute ceiling` of [page 5.3](#p53-ceilings). We work them for the executive jet at the start mass of worked example 2.

The first limit is the speed. The best-range speed rises as $1/\sqrt{\rho}$, while the speed of sound falls up to 11 km. The polar of this jet applies only up to Mach 0.80 ([page 5.1](#p51-available-and-vmax)); past it, {term}`wave drag` adds to $C_{D,0}$. On the standard atmosphere of [page 1.4](../chapter-1/standard-atmosphere.md), the best-range speed reaches Mach 0.80 at about $10.1$ km.

The second limit is the thrust. It comes where [](#eq-p52-throttle) gives $\delta_t = 1$, where full throttle only just provides the best-range thrust. With the numbers of worked example 2, $T_R = 20{,}537$ N against $n\,T_0 = 55{,}620$ N at sea level:

$$
\begin{aligned}
\frac{\rho}{\rho_0} &= \left(\frac{20{,}537}{55{,}620}\right)^{1/0.6}\\
\rho &= 1.225\times {0.36924}^{1/0.6}\\
&= 0.2328\ \text{kg/m}^3
\end{aligned}
$$

That is about $13.8$ km. Higher than this, the engines cannot give the best-range thrust. The absolute ceiling, where full thrust only matches the minimum thrust required, is higher still, at $0.183$ kg/m³ or about $15.35$ km. There the jet can fly at one speed only, the minimum-thrust speed, and not at the best-range speed.

:::{figure} figures/p52-altitude-range.svg
:label: fig-p52-altitude-range
:alt: Graph of range or endurance over its sea-level value, 0 to 2.75, against cruise altitude, 0 to 14 kilometers. A thick solid black curve for jet range, the square root of rho 0 over rho, rises from 1 at sea level to about 1.7 at a filled diamond labeled jet reaches Mach 0.80 at 10.1 km. From there a gray band, jet past Mach 0.80, wave drag, covers the rest of the graph; the curve goes on thin to a vertical dashed line at 13.8 kilometers labeled thrust limit. A black dash-dot horizontal line at 1 is labeled jet endurance, propeller range: no change. A black dotted curve falls from 1 to about 0.43 at 14 kilometers, labeled propeller endurance, the square root of rho over rho 0.
:width: 85%

Computed from the standard atmosphere for range and endurance at fixed masses, with the limits of the executive jet at the start mass of worked example 2. Only the jet range gains from altitude, and it gains only up to the Mach limit at 10.1 km; the thrust limit comes at 13.8 km. The jet curve bends upward at 11 km, where the density starts to fall faster. The propeller lines show the density factor only.
:::

In practice, long-range cruise is flown a little faster than the best-range speed. The FAA describes it at 99% of the best specific range, the distance flown per unit of fuel. That gives up 1% of range in return for a cruise speed 3% to 5% higher (FAA 2023, Chapter 11, p. 11-10).

### The two kinds of aircraft in one table

{numref}`tbl-p52-optima` collects the results, with the levers that raise range and endurance.

:::{table} Range and endurance of a jet and of a propeller aircraft, with a parabolic polar and a constant specific fuel consumption.
:label: tbl-p52-optima
:align: center

<table>
<thead><tr><th>Quantity</th><th>Jet</th><th>Propeller aircraft</th></tr></thead>
<tbody>
<tr><th scope="row">Fuel flow follows</th><td>the thrust</td><td>the shaft power</td></tr>
<tr><th scope="row">Best range</th><td>1.316 × the minimum-thrust speed; induced drag one third of parasite drag</td><td>the minimum-thrust speed, maximum lift-to-drag ratio</td></tr>
<tr><th scope="row">Best endurance</th><td>the minimum-thrust speed, maximum lift-to-drag ratio</td><td>the minimum-power speed, 0.760 × the minimum-thrust speed; induced drag three times parasite drag</td></tr>
<tr><th scope="row">Range as the aircraft climbs</th><td>grows as one over the square root of the density, up to the Mach and thrust limits</td><td>does not change</td></tr>
<tr><th scope="row">Endurance as the aircraft climbs</th><td>does not change</td><td>falls as the square root of the density</td></tr>
<tr><th scope="row">Other ways to get more range and endurance</th><td>a lower thrust specific fuel consumption; more fuel</td><td>a higher propeller efficiency; a lower power specific fuel consumption; more fuel on a lighter aircraft</td></tr>
</tbody>
</table>
:::

(p52-worked-examples)=
## Worked examples

### Worked example 1: maximum range of a jet like the CJ-1 (English units)

Anderson (2016, Chapter 6) works the maximum range of a light twin-turbofan business jet that he calls the CJ-1. We use the same method for an airplane like it, with the numbers below. The jet cruises at $22{,}000$ ft, where $\rho = 0.038$ lbm/ft³. Its wingspan is $b = 53.3$ ft and its wing area $S = 318$ ft². It weighs $19{,}817$ lb with full tanks and carries $1{,}119$ gal of fuel at $6.66$ lb/gal. Its polar has $C_{D,0} = 0.020$ and $e = 0.81$, and its thrust specific fuel consumption is $0.60$ 1/h. Find the maximum range.

The jet range equation applies in any consistent units. Here the masses are in lbm, the density in lbm/ft³, and $g = 32.17$ ft/s². At standard gravity a mass of 1 lbm weighs 1 lb, so the weights become masses with the same numbers.

1. **Fuel and final mass:**
   $$
   \begin{aligned}
   m_\text{fuel} &= 1{,}119\times 6.66\\
   &= 7{,}452.5\ \text{lbm}\\
   m_2 &= 19{,}817 - 7{,}452.5\\
   &= 12{,}364.5\ \text{lbm}
   \end{aligned}
   $$
2. **Polar and best-range ratio:**
   $$
   \begin{aligned}
   \textit{AR} &= \frac{{53.3}^{2}}{318}\\
   &= 8.9336\\
   K &= \frac{1}{\pi\times 0.81\times 8.9336}\\
   &= 0.043988\\
   C_L &= \sqrt{\frac{0.020}{3\times 0.043988}}\\
   &= 0.38930\\
   C_D &= \tfrac43\times 0.020\\
   &= 0.026667\\
   \frac{\sqrt{C_L}}{C_D} &= \frac{\sqrt{0.38930}}{0.026667}\\
   &= 23.397
   \end{aligned}
   $$
3. **The factors of [](#eq-p52-jet-R).** The fuel consumption is $c_t = 0.60/3{,}600 = 1.6667 \times {10}^{-4}$ 1/s, so $2/c_t$ is a round number:
   $$
   \begin{aligned}
   \frac{2}{c_t} &= \frac{2\times 3{,}600}{0.60}\\
   &= 12{,}000\ \text{s}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   &\sqrt{\frac{2g}{\rho S}}\\
   &\;\;\;= \sqrt{\frac{2\times 32.17}{0.038\times 318}}\\
   &\;\;\;= 2.3075\ \text{ft}/(\text{s}\cdot\text{lbm}^{1/2})
   \end{aligned}
   $$
   $$
   \begin{aligned}
   &\sqrt{m_1} - \sqrt{m_2}\\
   &\;\;\;= 140.773 - 111.196\\
   &\;\;\;= 29.577\ \text{lbm}^{1/2}
   \end{aligned}
   $$
4. **Range:**
   $$
   \begin{aligned}
   R &= 12{,}000\times 2.3075\\
   &\;\;\;\times 23.397\times 29.577\\
   &= 1.9162 \times {10}^{7}\ \text{ft}
   \end{aligned}
   $$
   With $5{,}280$ ft in a statute mile, that is $3{,}629$ mi, and with $0.3048$ m in a foot, $5{,}841$ km. It is a still-air cruise range, so the fuel for takeoff, climb, descent, and reserves would come out of it.

### Worked example 2: fuel for a leg, throttle, and hold of the executive jet (SI)

The twin-engine executive jet of [page 5.1](#p51-example-2) has $m_1 = 33{,}100$ kg, $S = 88.2$ m², $C_{D,0} = 0.015$, $K = 0.050$, and two engines of $T_0 = 27{,}810$ N with $m_\text{ad} = 0.6$. It cruises at $8{,}500$ m, where the [standard atmosphere](../chapter-1/standard-atmosphere.md) gives $\rho = 0.49482$ kg/m³ and a speed of sound of $305.91$ m/s. We assume a thrust specific fuel consumption of $0.58$ 1/h, between the typical cruise values of a low-bypass and a high-bypass turbofan in [the table of page 1.6](#tbl-p16-sfc). Find:

- (a) The fuel for a $3{,}300$ km leg flown at best range.
- (b) The thrust and throttle setting at the start and at the end of the leg.
- (c) The longest time it could stay up on the same fuel.
- (d) The fuel for a hold of $1.5$ h (circling over one place before landing), flown from the start mass $m_1$.

**(a) Fuel for the leg.** We convert the fuel consumption and find the best-range condition:

$$
\begin{aligned}
c_t &= \frac{0.58}{3{,}600}\\
&= 1.61111 \times {10}^{-4}\ \text{1/s}\\
C_L &= \sqrt{\frac{0.015}{3\times 0.050}}\\
&= 0.31623\\
C_D &= \tfrac43\times 0.015\\
&= 0.0200\\
\frac{\sqrt{C_L}}{C_D} &= \frac{\sqrt{0.31623}}{0.0200}\\
&= 28.117
\end{aligned}
$$

The constant factors of [](#eq-p52-jet-R) make one number $A$, so that $R = A\,(\sqrt{m_1} - \sqrt{m_2})$:

$$
\begin{aligned}
&\sqrt{\frac{2g}{\rho S}}\\
&\;\;\;= \sqrt{\frac{2\times 9.81}{0.49482\times 88.2}}\\
&\;\;\;= 0.67049\ \text{m}/(\text{s}\cdot\text{kg}^{1/2})
\end{aligned}
$$

$$
\begin{aligned}
A &= \frac{2}{1.61111\times{10}^{-4}}\times\\
&\;\;\; 0.67049\times 28.117\\
&= 234{,}027\ \text{m}/\text{kg}^{1/2}
\end{aligned}
$$

The final mass follows, as in [](#eq-p52-jet-fuel-R):

$$
\begin{aligned}
\sqrt{m_2} &= \sqrt{m_1} - \frac{R}{A}\\
&= 181.934 - \frac{3{,}300{,}000}{234{,}027}\\
&= 167.833\ \text{kg}^{1/2}\\
m_2 &= {167.833}^{2}\\
&= 28{,}168\ \text{kg}\\
m_\text{fuel} &= 33{,}100 - 28{,}168\\
&= 4{,}932\ \text{kg}
\end{aligned}
$$

We find the speed at the start of the leg, with the weight $m_1 g = 324{,}711$ N, and its Mach number:

$$
\begin{aligned}
V_1 &= \sqrt{\frac{2\times 324{,}711}{0.49482\times 88.2}}\times\\
&\;\;\;\frac{1}{\sqrt{0.31623}}\\
&= 216.9\ \text{m/s}\\
M &= \frac{216.9}{305.91}\\
&= 0.709
\end{aligned}
$$

That is below Mach 0.80, so the polar applies. At the end of the leg the speed has fallen to $200.1$ m/s ({numref}`fig-p52-weight-burn`).

**(b) Thrust and throttle.** At the start, the best-range thrust is

$$
\begin{aligned}
\sqrt{\frac{K C_{D,0}}{3}} &= \sqrt{\frac{0.050\times 0.015}{3}}\\
&= 0.0158114\\
T_R &= 4mg\sqrt{\frac{K C_{D,0}}{3}}\\
&= 4\times 324{,}711\times\\
&\;\;\; 0.0158114\\
&= 20{,}537\ \text{N}
\end{aligned}
$$

The thrust available at full throttle at $8{,}500$ m is

$$
\begin{aligned}
\frac{\rho}{\rho_0} &= \frac{0.49482}{1.225}\\
&= 0.40393\\
T_A &= 55{,}620\times {0.40393}^{0.6}\\
&= 55{,}620\times 0.58048\\
&= 32{,}286\ \text{N}
\end{aligned}
$$

So the throttle setting at the start is $\delta_t = 20{,}537/32{,}286 = 0.6361$. This best-range thrust equals the jet's thrust at its minimum-power speed on [page 5.1](#p51-example-2), because at both points $C_D/C_L = 4\sqrt{KC_{D,0}/3}$. At the end of the leg, the same formula with $m_2 = 28{,}168$ kg gives

$$
\begin{aligned}
T_R &= 4\times 28{,}168\times 9.81\times\\
&\;\;\; 0.0158114\\
&= 17{,}477\ \text{N}\\
\delta_t &= \frac{17{,}477}{32{,}286}\\
&= 0.5413
\end{aligned}
$$

The engines have plenty of margin at this altitude, and the pilot eases the throttle back as the jet gets lighter.

**(c) Longest time on the same fuel.** Best endurance is at $(L/D)_{\max}$, and [](#eq-p52-jet-E) needs no altitude:

$$
\begin{aligned}
\sqrt{K C_{D,0}} &= \sqrt{0.050\times 0.015}\\
&= 0.0273861\\
\left(\frac{L}{D}\right)_{\max} &= \frac{1}{2\times 0.0273861}\\
&= 18.2574\\
\ln\frac{m_1}{m_2} &= \ln\frac{33{,}100}{28{,}168}\\
&= 0.161347\\
E &= \frac{18.2574}{1.61111\times{10}^{-4}}\times\\
&\;\;\; 0.161347\\
&= 18{,}284\ \text{s}\\
&= 5.079\ \text{h}
\end{aligned}
$$

Compare this with the leg itself. At an average speed of about $208.5$ m/s, the $3{,}300$ km take about $4.40$ h. Slowing down to the minimum-thrust speed keeps the jet up longer on the same fuel, but it covers less distance.

**(d) Fuel for a 1.5 h hold.** With [](#eq-p52-jet-fuel-E) at $(L/D)_{\max}$, from the start mass and with $E = 5{,}400$ s:

$$
\begin{aligned}
c_t E\,\frac{C_D}{C_L} &= \frac{1.61111\times{10}^{-4}}{18.2574}\times\\
&\;\;\; 5{,}400\\
&= 0.047652
\end{aligned}
$$

$$
\exp(-0.047652) = 0.953466
$$

$$
\begin{aligned}
m_\text{fuel} &= 33{,}100\times\\
&\;\;\; (1 - 0.953466)\\
&= 1{,}540.3\ \text{kg}
\end{aligned}
$$

That is about a third of the fuel of the $3{,}300$ km leg.

### Worked example 3: range and endurance of a propeller aircraft (SI)

The single-engine general-aviation airplane of [page 5.1](#p51-example-1) has $m_1 = 1{,}315$ kg with full tanks, $S = 16.3$ m², $C_{D,0} = 0.026$, $K = 0.054$, and a propeller efficiency $\eta = 0.80$. It carries $168$ kg of usable fuel, and its engine burns $0.076$ g/(s·kW). Find its maximum range and its maximum endurance at $2{,}500$ m, where $\rho = 0.956714$ kg/m³.

**Fuel constant and final mass.** From the [conversion above](#p52-fuel-consumption):

$$
\begin{aligned}
c &= 7.4556 \times {10}^{-7}\ \text{1/m}\\
\frac{\eta}{c} &= \frac{0.80}{7.4556\times{10}^{-7}}\\
&= 1{,}073{,}019\ \text{m}\\
m_2 &= 1{,}315 - 168\\
&= 1{,}147\ \text{kg}
\end{aligned}
$$

**Maximum range**, with [](#eq-p52-prop-R) at the largest $C_L/C_D$:

$$
\begin{aligned}
C_L &= \sqrt{\frac{0.026}{0.054}}\\
&= 0.69389\\
C_D &= 2\times 0.026\\
&= 0.052\\
\frac{C_L}{C_D} &= \frac{0.69389}{0.052}\\
&= 13.344\\
\ln\frac{m_1}{m_2} &= \ln\frac{1{,}315}{1{,}147}\\
&= 0.136687\\
R &= 1{,}073{,}019\times 13.344\times\\
&\;\;\; 0.136687\\
&= 1{,}957{,}134\ \text{m}\\
&= 1{,}957\ \text{km}
\end{aligned}
$$

The altitude did not enter. The same fuel gives the same range at sea level.

**Maximum endurance**, with [](#eq-p52-prop-E) at the largest $C_L^{3/2}/C_D$:

$$
\begin{aligned}
C_L &= \sqrt{\frac{3\times 0.026}{0.054}}\\
&= 1.20185\\
C_D &= 4\times 0.026\\
&= 0.104\\
\frac{C_L^{3/2}}{C_D} &= \frac{{1.20185}^{3/2}}{0.104}\\
&= 12.669
\end{aligned}
$$

$$
\begin{aligned}
&\sqrt{\frac{2\rho S}{g}}\\
&\;\;\;= \sqrt{\frac{2\times 0.956714\times 16.3}{9.81}}\\
&\;\;\;= 1.78306\ \text{s}\cdot\text{kg}^{1/2}/\text{m}
\end{aligned}
$$

$$
\begin{aligned}
&\frac{1}{\sqrt{m_2}} - \frac{1}{\sqrt{m_1}}\\
&\;\;\;= 0.02952693 - 0.02757637\\
&\;\;\;= 0.00195056\ \text{kg}^{-1/2}
\end{aligned}
$$

$$
\begin{aligned}
E &= 1{,}073{,}019\times 1.78306\\
&\;\;\;\times 12.669\times 0.00195056\\
&= 47{,}280\ \text{s}\\
&= 13.13\ \text{h}
\end{aligned}
$$

Unlike the range, this result depends on the altitude through $\sqrt{\rho}$, so if we fly lower, the airplane stays up longer.

## Summary

:::{important} Summary
- A jet burns fuel in proportion to its thrust ($c_t$ in 1/s), a propeller aircraft in proportion to its shaft power ($c$ in 1/m). Integrating the fuel flow in steady level flight at constant altitude and $C_L$ gives the four Breguet equations.
- Jet range is best at the largest $C_L^{1/2}/C_D$, jet endurance and propeller range at the largest $C_L/C_D$, and propeller endurance at the largest $C_L^{3/2}/C_D$. The best speeds are $0.760$, $1$, and $1.316$ times $V_{T_R,\min}$.
- At best range a jet needs $4mg\sqrt{KC_{D,0}/3}$ of thrust, and the pilot throttles back as the fuel burns. Jet range grows with altitude until the Mach limit or until full throttle no longer gives that thrust, below the absolute ceiling.
:::

:::{table} The equations of this page.
:label: tbl-p52-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Fuel flow, jet | $d(mg)/dt = -c_t\,T$ |
| Fuel flow, propeller aircraft | $d(mg)/dt = -c\,P/\eta$ |
| Jet range | $R = (2/c_t)\sqrt{2g/(\rho S)}\,(\sqrt{C_L}/C_D)(\sqrt{m_1}-\sqrt{m_2})$ |
| Jet endurance | $E = (1/c_t)(C_L/C_D)\ln(m_1/m_2)$ |
| Jet best range | $C_L = \sqrt{C_{D,0}/(3K)}$, $C_D = \tfrac43 C_{D,0}$ |
| Thrust at jet best range | $T_R = 4mg\sqrt{KC_{D,0}/3}$ |
| Throttle at jet best range | $\delta_t = (4mg/(nT_0))(\rho_0/\rho)^{m_\text{ad}}\sqrt{KC_{D,0}/3}$ |
| Jet best endurance, propeller best range | $C_L = \sqrt{C_{D,0}/K}$, $C_D = 2C_{D,0}$ |
| Propeller range | $R = (\eta/c)(C_L/C_D)\ln(m_1/m_2)$ |
| Propeller endurance | $E = (\eta/c)\sqrt{2\rho S/g}\,(C_L^{3/2}/C_D)(1/\sqrt{m_2}-1/\sqrt{m_1})$ |
| Propeller best endurance | $C_L = \sqrt{3C_{D,0}/K}$, $C_D = 4C_{D,0}$ |
| Fuel for a jet range | $\sqrt{m_2} = \sqrt{m_1} - (c_t R/2)\sqrt{\rho S/(2g)}\,C_D/\sqrt{C_L}$ |
| Fuel for a jet endurance | $m_\text{fuel} = m_1[1 - \exp(-c_t E\,C_D/C_L)]$ |
| Fuel for a propeller range | $m_\text{fuel} = m_1[1 - \exp(-(c/\eta)(C_D/C_L)R)]$ |
| Fuel for a propeller endurance | $1/\sqrt{m_2} = 1/\sqrt{m_1} + E\,(c/\eta)(C_D/C_L^{3/2})\sqrt{g/(2\rho S)}$ |

:::

:::{exercise} For discussion
:label: ex-p52-discussion

1. Why does a jet fly faster for its best range than for its best endurance? Why is the factor between a propeller aircraft's two best speeds the same 1.316?
2. A jet flies a long leg at constant altitude and constant $C_L$. Does the first half of the distance burn more fuel, less fuel, or the same fuel as the second half? Explain with the forces.
3. Why does the density appear in the jet range equation but not in the propeller range equation?
4. A jet and a propeller aircraft with the same polar and the same fuel fraction must each stay over one point as long as possible. At what altitude and at what speed, relative to its own minimum-thrust speed, should each one fly?
5. At a fixed mass and polar, a larger wing area $S$ helps the endurance of a propeller aircraft. Why does it lower the range of a jet at a given altitude?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-5-2.html
:label: quiz-5-2
:width: 100%
:enumerated: false

Quiz for Standard 5.2: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 6.
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023. Chapter 11, "Aircraft Performance," pp. 11-9 to 11-11 (range performance).
