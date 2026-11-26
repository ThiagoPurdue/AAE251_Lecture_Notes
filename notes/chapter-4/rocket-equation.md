---
title: "4.2 Rocket Equation"
short_title: 4.2 Rocket Equation
---

:::{include} ../_parts/standards/4.2.md
:::

In Chapter 2, we expressed every maneuver as a delta-V: 3.416 km/s for the Hohmann transfer on page 2.2, and 8.833 km/s (including losses) for the launch on page 2.3. To size a real vehicle, we need to turn that delta-V into propellant mass. On this page we derive the {term}`rocket equation`, which relates delta-V to vehicle mass. Next comes the mass of a stage, split into payload, inert mass, and propellant, and the sizing of a stage for a given job. Then we find the most a single stage can ever do and add gravity and drag back in. The page ends by judging whether a real stage can reach orbit on its own.

:::{note} What to take from this page
- The rocket equation, $\Delta V = c\ln(m_i/m_f)$ with $c = I_\text{sp}\,g_0$, follows from conservation of momentum. It assumes no gravity and no drag.
- The mass ratio $m_i/m_f = e^{\Delta V/c}$ grows exponentially: each added $c$ of delta-V multiplies it by $e$.
- The inert mass fraction, $f_\text{inert} = m_\text{inert}/(m_\text{inert} + m_\text{prop})$, ties the inert mass to the propellant, so one formula gives the propellant for a payload.
- One stage can never give more than $c\ln(1/f_\text{inert})$. Gravity and drag losses are added to the requirement before any sizing.
:::

## From a delta-V to a mass

Every burn on [orbit transfers](../chapter-2/orbit-transfers.md) and every part of [the launch budget](../chapter-2/launch-to-orbit.md) requires propellant. How much depends on two things: how fast the engine throws its exhaust out, and how much of the vehicle is left when the burn ends. The relation between them was published in 1903 by Konstantin Tsiolkovsky, a Russian schoolteacher. It ties the speed of a rocket to the speed of its exhaust and to its mass with and without propellant (NASA n.d.). Every rocket design still starts from it.

We used this equation once without derivation on [ground tracks and orbit lifetime](#eq-p25-propellant), and now we derive it from conservation of momentum.

(p42-rocket-equation)=
## Deriving the rocket equation

Here is the idea. A rocket throws small pieces of mass backward at high speed. Each piece carries momentum backward, so the rocket gains the same momentum forward. This is also why a rocket works in vacuum ([thrust and specific impulse](thrust-and-specific-impulse.md)). {numref}`fig-p42-momentum-exchange` shows one small step of the burn.

:::{figure} figures/p42-momentum-exchange.svg
:label: fig-p42-momentum-exchange
:alt: Two rows, with velocities measured from the ground and positive to the right. Top row, at time t: a rocket of mass m moves right at speed V; its momentum is m V. Bottom row, at time t plus dt: the same rocket, now of mass m minus d m prop, moves right at V plus d V, and a small exhaust mass d m prop behind its nozzle moves left with velocity V minus V e, negative, as a note under the sign convention says: a velocity to the left is negative. The total momentum is (m minus d m prop)(V plus d V) plus d m prop (V minus V e).
:width: 80%

Schematic of the momentum exchange that the rocket equation comes from: the rocket gains forward momentum because the small mass it throws out carries momentum backward, and the total does not change. Velocities from the ground; drawn for an exit velocity $V_e$ larger than $V$, so the exhaust moves backward and its velocity $V - V_e$ is negative; the change $dV$ is exaggerated. Rocket outline after the Falcon 9 (SpaceX 2025).
:::

At time $t$ the rocket has mass $m$ and moves at speed $V$, measured from the ground. During a short time $dt$ it throws out a small mass $dm_\text{prop}$ of propellant. That mass leaves at the {term}`exit velocity` $V_e$ relative to the rocket, backward, so seen from the ground it moves at $V - V_e$. The rocket, now lighter, moves at $V + dV$. We assume that no outside force acts: no gravity and no drag (NASA Glenn Research Center 2023). Then the total momentum of the rocket and its exhaust is the same before and after the step.

1. **Momentum before equals momentum after.**
   $$
   \begin{aligned}
   mV &= (m - dm_\text{prop})\\
   &\;\;\; \times (V + dV)\\
   &\;\;\; + dm_\text{prop}(V - V_e)
   \end{aligned}
   $$
2. **Multiply out the right side.**
   $$
   \begin{aligned}
   mV &= mV + m\,dV\\
   &\;\;\;{} - dm_\text{prop}V\\
   &\;\;\;{} - dm_\text{prop}\,dV\\
   &\;\;\;{} + dm_\text{prop}V\\
   &\;\;\;{} - dm_\text{prop}V_e
   \end{aligned}
   $$
3. **Cancel what appears on both sides.** $mV$ cancels with $mV$, and $-dm_\text{prop}V$ cancels with $+dm_\text{prop}V$. What is left is
   $$
   \begin{aligned}
   0 &= m\,dV - dm_\text{prop}\,dV\\
   &\;\;\; - dm_\text{prop}V_e
   \end{aligned}
   $$
4. **Drop the product of two small quantities.** $dm_\text{prop}\,dV$ is a small mass times a small change of speed. When $dt$ shrinks, it shrinks much faster than the other two terms, so we drop it:
   $$
   m\,dV = dm_\text{prop}V_e
   $$
5. **Write the propellant as the mass the rocket loses.** The rocket's mass changes by $dm = -dm_\text{prop}$. Now only two variables are left, $m$ and $V$, and they separate:
   $$
   dV = -V_e\,\frac{dm}{m}
   $$
6. **Integrate over the burn**, from the initial mass $m_i$ and speed $V_i$ to the final mass $m_f$ and speed $V_f$. The integral of $1/m$ is $\ln m$:
   $$
   \begin{aligned}
   V_f - V_i &= -V_e\ln m_f\\
   &\;\;\; + V_e\ln m_i\\
   &= V_e\ln\frac{m_i}{m_f}
   \end{aligned}
   $$

Step 4 has a familiar meaning. Divide it by $dt$: $m\,dV/dt = (dm_\text{prop}/dt)\,V_e$, which is the rocket's mass times its acceleration, equal to the momentum thrust $\dot m V_e$. The exhaust also pushes with its pressure at the nozzle exit. Page 4.1 adds that pressure thrust and writes the whole thrust as $F = \dot m\,c$, with $c$ the {term}`effective exhaust velocity` ([specific impulse](#p41-specific-impulse)). With that thrust the same steps give the same result with $c$ in place of $V_e$. So from here on we write $c$, found from the specific impulse as $c = I_\text{sp}\,g_0$.

::::{prf:definition} Rocket equation
:label: def-p42-rocket-equation

The **ideal rocket equation** gives the velocity change of a rocket that burns propellant from an initial mass $m_i$ down to a final mass $m_f$:

:::{math}
:label: eq-p42-rocket
\begin{aligned}
\Delta V &= c\ln\frac{m_i}{m_f}\\
c &= I_\text{sp}\,g_0
\end{aligned}
:::

with $c$ the effective exhaust velocity, $I_\text{sp}$ the specific impulse in seconds, and $g_0$ = 9.81 m/s², the standard gravity.
::::

The word "ideal" marks what we left out. To derive this equation, we made three assumptions.

- No gravity and no drag act, so nothing outside the rocket takes speed away.
- The effective exhaust velocity $c$ stays constant for the whole burn.
- The thrust points along the motion.

The ideal $\Delta V$ is the largest velocity change the propellant can produce. Gravity and drag reduce the final velocity gain, as we see in the [section on gravity and drag](#p42-losses). Notice also that neither the thrust nor the burn time appears in the equation. A gentle engine and a strong one with the same $c$ give the same $\Delta V$ for the same masses, as long as nothing outside acts on the rocket.

:::{warning} $g_0$ is a fixed number
In $c = I_\text{sp}\,g_0$, $g_0$ is always 9.81 m/s², the standard gravity that defines the specific impulse. It is not the gravity where the rocket happens to be. If you use the Moon's gravity for a lunar lander, every mass comes out wrong. Also keep track of units for $I_\text{sp}$. Because it is given in seconds, if you substitute $I_\text{sp}$ directly in place of $c$, your result will be off by a factor of 9.81.
:::

## What the equation says

We solve [](#eq-p42-rocket) for the masses. Divide by $c$ and take the exponential of both sides:

:::{math}
:label: eq-p42-mass-ratio
\frac{m_i}{m_f} = e^{\Delta V/c}
:::

The ratio $m_i/m_f$ is the {term}`mass ratio`. The propellant burned is $m_i - m_f$, so the share of the initial mass that is propellant is

:::{math}
:label: eq-p42-share
\frac{m_\text{prop}}{m_i} = 1 - e^{-\Delta V/c}
:::

This is the form used on [the ground-tracks page](#eq-p25-propellant), solved for the propellant. Now look at the numbers in {numref}`fig-p42-mass-ratio`. A delta-V equal to $c$ needs a mass ratio of $e = 2.718$: 63% of the vehicle at ignition is propellant. Twice $c$ needs 7.389, and 86% is propellant. Three times $c$ needs 20.09, and 95% is propellant.

:::{figure} figures/p42-mass-ratio.svg
:label: fig-p42-mass-ratio
:alt: Two plots against delta-V over c, from 0 to 3.2. Top: the mass ratio m i over m f, an exponential curve from 1 through 2.718 at 1, 7.389 at 2, and 20.09 at 3, marked with dots; a note says each added c of delta-V multiplies the mass ratio by e, 2.718. Bottom: the propellant share of the initial mass in percent, rising quickly at first and then flattening, through 63 percent at 1, 86 percent at 2, and 95 percent at 3, creeping toward 100 percent.
:width: 80%

Computed from $m_i/m_f = e^{\Delta V/c}$: each added $c$ of delta-V multiplies the mass ratio by $e$, while the propellant share only creeps toward 100%. Top: mass ratio. Bottom: propellant share of the initial mass, $1 - e^{-\Delta V/c}$.
:::

Each added $c$ multiplies the mass ratio by 2.718, and that is why a delta-V much larger than $c$ is so hard to reach. The vehicle becomes almost all propellant, leaving little mass for the tanks, the engines, and the payload. Raising $c$ helps the most, because a higher specific impulse lowers the ratio $\Delta V/c$ and reduces the exponential mass ratio.

:::{warning} Which mass goes on top
$m_i$, the mass at ignition, is always the larger one, so $m_i/m_f$ is larger than 1 and its logarithm is positive. If you write $m_f/m_i$, you get a negative delta-V. The mass at the end of a burn is always the smaller one.
:::

### Worked example 1: slowing down to orbit Jupiter

A spacecraft arrives at Jupiter and must slow by $\Delta V$ = 2.1 km/s to be captured into orbit. Its initial mass is 4,000 kg and its engine has a specific impulse of 360 s in vacuum. Find the mass at the end of the burn and the propellant burned.

1. **Effective exhaust velocity.** $c = I_\text{sp}\,g_0 = 360 \times 9.81 = 3{,}532$ m/s.
2. **Delta-V over $c$**, with 2.1 km/s written as 2,100 m/s:
   $$
   \begin{aligned}
   \frac{\Delta V}{c} &= \frac{2{,}100}{3{,}532}\\
   &= 0.59456
   \end{aligned}
   $$
3. **Mass ratio**, [](#eq-p42-mass-ratio): $m_i/m_f = e^{0.59456} = 1.8122$.
4. **Final mass.**
   $$
   \begin{aligned}
   m_f &= \frac{m_i}{1.8122}\\
   &= \frac{4{,}000}{1.8122}\\
   &= 2{,}207\ \text{kg}
   \end{aligned}
   $$
5. **Propellant.** $m_\text{prop} = m_i - m_f = 4{,}000 - 2{,}207 = 1{,}793$ kg.

**Check.** The burn is a little more than half of $c$, so the propellant share should lie below the 63% of a burn of $c$. It is $1{,}793/4{,}000$, about 45%. Slowing a spacecraft down requires the same propellant as speeding it up by the same $\Delta V$. The spacecraft turns so that its engine fires against the direction of motion, and the same equation holds.

(p42-inert-mass-fraction)=
## Three kinds of mass

The rocket equation has only two masses in it, $m_i$ and $m_f$. To design a vehicle we need to know what they are made of. A vehicle splits into three parts.

- The {term}`payload` mass $m_\text{pay}$ is everything the stage carries that is not its own propulsion system, such as a satellite or the stages above it.
- The {term}`inert mass` $m_\text{inert}$ is everything in the stage that is not propellant: the empty tanks, the engines, the pipes, and the structure.
- The {term}`propellant mass` $m_\text{prop}$ is the fuel and the oxidizer that the burn uses.

At the end of the burn the propellant is gone, and the payload and the inert mass are left. At ignition all three are there:

:::{math}
:label: eq-p42-masses
\begin{aligned}
m_f &= m_\text{pay} + m_\text{inert}\\
m_i &= m_f + m_\text{prop}
\end{aligned}
:::

We now have three equations, but we face a coupling problem: we cannot know the inert mass before we know the propellant mass, because carrying more propellant requires larger, heavier tanks. What stays roughly constant across similar designs is the fraction of the stage's own mass that is inert, which we define as the inert mass fraction.

:::{prf:definition} Inert mass fraction
:label: def-p42-inert-mass-fraction

The **{term}`inert mass fraction`** of a stage is its inert mass divided by its own loaded mass, inert mass plus propellant:

$$
f_\text{inert} = \frac{m_\text{inert}}{m_\text{inert} + m_\text{prop}}
$$

The payload is not part of it.
:::

{numref}`fig-p42-three-masses` shows the three masses and what the fraction is measured against.

:::{figure} figures/p42-three-masses.svg
:label: fig-p42-three-masses
:alt: One horizontal bar split into three parts from left to right: payload m pay, a plain darker fill; inert mass m inert, hatched, named by a leader that ends on a dot inside it; propellant m prop, a plain light fill and the longest. A brace under payload and inert mass marks the final mass m f; a longer brace under the whole bar marks the initial mass m i. A brace above the inert mass and the propellant marks the stage, m inert plus m prop, with the definition f inert equals m inert over m inert plus m prop.
:width: 75%

Schematic of the three masses of a stage, in the proportions of worked example 2: the inert mass fraction is measured against the stage alone, inert mass plus propellant, never against the whole vehicle. The final mass is what is left when the propellant is gone.
:::

:::{warning} Over the stage, not over the vehicle
$f_\text{inert}$ divides the inert mass by $m_\text{inert} + m_\text{prop}$. If you divide by $m_i$, which also includes the payload, the fraction comes out too small, and every stage you size with it will be unrealistically light.
:::

The values come from stages that have flown. {numref}`tbl-p42-stages` computes the fraction of ten real stages from their published masses, and {numref}`fig-p42-inert-fractions` plots them against the propellant they carry.

:::{table} Inert mass fractions of real stages, computed from published masses: Saturn V of Apollo 11 (Orloff 2000, "Ground Ignition Weights"); Ariane 5 core and upper stage (Arianespace 2016, Section 1.5.1); Ariane 5 booster (Berkes 2005: 280 t with 240 t of propellant); Space Shuttle booster (NASA 1981, p. 2-18); Vega first three stages (Arianespace 2014, Figure 1.5.1a: gross and propellant mass). Where a source gives only the gross mass, the inert mass is the gross mass minus the propellant.
:label: tbl-p42-stages
:align: center

<table>
<tr><th>Stage</th><th>Vehicle and kind</th><th>Inert mass, t</th><th>Propellant, t</th><th>Inert mass fraction</th></tr>
<tr><th scope="row">S-IC</th><td>Saturn V, liquid first stage</td><td class="num">130.4</td><td class="num">2,146</td><td class="num">0.0573</td></tr>
<tr><th scope="row">S-II</th><td>Saturn V, liquid second stage</td><td class="num">36.16</td><td class="num">443.2</td><td class="num">0.0754</td></tr>
<tr><th scope="row">S-IVB</th><td>Saturn V, liquid third stage</td><td class="num">11.27</td><td class="num">107.1</td><td class="num">0.0952</td></tr>
<tr><th scope="row">EPC</th><td>Ariane 5, liquid core stage</td><td class="num">14.70</td><td class="num">170.0</td><td class="num">0.0796</td></tr>
<tr><th scope="row">ESC-A</th><td>Ariane 5, liquid upper stage</td><td class="num">4.540</td><td class="num">14.90</td><td class="num">0.234</td></tr>
<tr><th scope="row">EAP</th><td>Ariane 5, solid booster</td><td class="num">40.00</td><td class="num">240.0</td><td class="num">0.143</td></tr>
<tr><th scope="row">Shuttle booster</th><td>Space Shuttle, solid booster</td><td class="num">87.55</td><td class="num">502.1</td><td class="num">0.148</td></tr>
<tr><th scope="row">P80</th><td>Vega, solid first stage</td><td class="num">8.533</td><td class="num">87.71</td><td class="num">0.0887</td></tr>
<tr><th scope="row">Zefiro 23</th><td>Vega, solid second stage</td><td class="num">2.486</td><td class="num">23.81</td><td class="num">0.0945</td></tr>
<tr><th scope="row">Zefiro 9</th><td>Vega, solid third stage</td><td class="num">1.433</td><td class="num">10.57</td><td class="num">0.119</td></tr>
</table>

:::

:::{figure} figures/p42-inert-fractions.svg
:label: fig-p42-inert-fractions
:alt: Scatter plot of the inert mass fraction, 0 to 0.25, against the propellant mass of the stage, 4 to 5,000 tonnes on a logarithmic axis. Filled circles are liquid stages, open squares solid motors. A thin dashed line labeled "liquid stages: the larger, the lighter" joins the liquid stages in order of size and falls all the way: Ariane 5 upper stage at 14.90 tonnes and 0.234, S-IVB at 0.0952, Ariane 5 core at 0.0796, S-II at 0.0754, and S-IC at 2,146 tonnes and 0.0573. The solid motors sit off that line, between 0.0887 and 0.148: Vega's P80, Zefiro 23, and Zefiro 9, along with the Ariane 5 booster and the Shuttle booster.
:width: 85%

Values from the published masses of {numref}`tbl-p42-stages`: the larger a liquid stage, the smaller its inert mass fraction, from 0.23 for the small Ariane 5 upper stage down to 0.057 for the S-IC. The solid motors follow no such trend. S-IC, S-II, and S-IVB are the Saturn V stages; P80, Zefiro 23, and Zefiro 9 are Vega's.
:::

The liquid stages show a clear trend: the larger the stage, the lower the fraction, from 0.234 for the small Ariane 5 upper stage down to 0.0573 for the S-IC. The small upper stage has the highest fraction. Some of its parts, such as the engine, the attitude-control thrusters, and the interstage adapter, do not shrink in proportion to the propellant load. The solid motors follow no such trend. In a solid motor the case itself is the combustion chamber, so its whole length must hold the chamber pressure. The two large boosters, at 0.143 and 0.148, have steel cases (Arianespace 2016, Section 1.5.1; NASA 1981, p. 2-19). Vega's motors, at 0.0887 to 0.119, have cases wound from carbon fiber and epoxy (Arianespace 2014, Figure 1.5.1a). Across the table the fraction runs from 0.057 to 0.23. For a new design, we choose $f_\text{inert}$ from existing stages with comparable propellant, size, and mission.

(p42-stage-sizing)=
## Sizing a stage

That makes four equations: the rocket equation [](#eq-p42-rocket), the two mass sums [](#eq-p42-masses), and the definition of $f_\text{inert}$. Usually we know the payload, the delta-V, the specific impulse, and the inert mass fraction, and we want to find the propellant mass. We combine the four, writing $x = \Delta V/c$ to keep the lines short.

1. **Rocket equation.** From [](#eq-p42-mass-ratio), $m_i = m_f\,e^{x}$. With $m_i = m_f + m_\text{prop}$ this gives
   $$
   m_\text{prop} = m_f\left(e^{x} - 1\right)
   $$
2. **Inert mass from the propellant.** Multiply the definition of $f_\text{inert}$ by $m_\text{inert} + m_\text{prop}$, then collect $m_\text{inert}$:
   $$
   m_\text{inert} = \frac{f_\text{inert}}{1 - f_\text{inert}}\,m_\text{prop}
   $$
3. **Put both into $m_f = m_\text{pay} + m_\text{inert}$.**
   $$
   \begin{aligned}
   m_\text{prop} &= \Bigl(m_\text{pay}\\
   &\;\;\; + \frac{f_\text{inert}\,m_\text{prop}}{1 - f_\text{inert}}\Bigr)\\
   &\;\;\; \times \left(e^{x} - 1\right)
   \end{aligned}
   $$
4. **Multiply by $1 - f_\text{inert}$** and move every $m_\text{prop}$ term to the left:
   $$
   \begin{aligned}
   &m_\text{prop}\left[(1 - f_\text{inert})\right.\\
   &\;\;\;\left. - f_\text{inert}(e^{x} - 1)\right]\\
   &\;\;\;= m_\text{pay}\left(e^{x} - 1\right)\\
   &\;\;\;\;\;\; \times (1 - f_\text{inert})
   \end{aligned}
   $$
5. **Simplify the bracket.** $(1 - f_\text{inert}) - f_\text{inert}e^{x} + f_\text{inert} = 1 - f_\text{inert}e^{x}$. So

:::{math}
:label: eq-p42-mprop
\begin{aligned}
m_\text{prop} &= m_\text{pay} \times\\
&\;\;\; \frac{\left(e^{\Delta V/c} - 1\right)\left(1 - f_\text{inert}\right)}{1 - f_\text{inert}\,e^{\Delta V/c}}
\end{aligned}
:::

With the propellant known, step 2 gives the inert mass, and [](#eq-p42-masses) gives $m_f$ and $m_i$.

:::{tip} Method: sizing one stage for a payload and a delta-V
1. Convert the specific impulse to $c = I_\text{sp}\,g_0$, with $g_0 = 9.81\ \text{m/s}^2$, and write $\Delta V$ in m/s.
2. Compute $x = \Delta V/c$ and $e^{x}$. Keep five or six figures: step 4 subtracts.
3. Check that $f_\text{inert}\,e^{x} < 1$. If not, stop: no stage of this kind can do the job (see [how far one stage can go](#p42-single-stage-limit)).
4. Compute the numerator and the denominator of [](#eq-p42-mprop) separately, then divide: $m_\text{prop}$.
5. $m_\text{inert} = f_\text{inert}\,m_\text{prop}/(1 - f_\text{inert})$.
6. $m_f = m_\text{pay} + m_\text{inert}$ and $m_i = m_f + m_\text{prop}$.
7. Check: $c\ln(m_i/m_f)$ gives back $\Delta V$.
:::

### Worked example 2: one stage for a Hohmann transfer

On [orbit transfers](#p22-hohmann) we moved a spacecraft from a 400 km circular orbit to a 20,200 km circular orbit with two burns, 2.012 and 1.404 km/s, 3.416 km/s in all. Suppose one stage makes both burns. It carries a payload of 1,750 kg, its engine has $I_\text{sp}$ = 323 s, and its inert mass fraction is 0.17. Find the propellant, the inert mass, and the mass at the start of the first burn.

1. **Effective exhaust velocity and delta-V.** $c = 323 \times 9.81 = 3{,}168.63$ m/s, and 3.416 km/s is 3,416 m/s.
2. **Exponent.**
   $$
   \begin{aligned}
   x &= \frac{3{,}416}{3{,}168.63}\\
   &= 1.07807
   \end{aligned}
   $$
   and $e^{x} = e^{1.07807} = 2.93900$.
3. **Limit check.** $f_\text{inert}\,e^{x} = 0.17 \times 2.93900$, about 0.50, well below 1.
4. **Numerator and denominator** of [](#eq-p42-mprop). With $e^{x} - 1 = 1.93900$ and $1 - f_\text{inert} = 0.83$:
   $$
   \begin{aligned}
   &\text{numerator}\\
   &\;\;\;= 1{,}750 \times 1.93900 \times\\
   &\;\;\;\;\;\; 0.83\\
   &\;\;\;= 2{,}816.40\ \text{kg}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   &\text{denominator}\\
   &\;\;\;= 1 - 0.17 \times 2.93900\\
   &\;\;\;= 0.500370
   \end{aligned}
   $$
5. **Propellant.**
   $$
   \begin{aligned}
   m_\text{prop} &= \frac{2{,}816.40}{0.500370}\\
   &= 5{,}628.6\ \text{kg}
   \end{aligned}
   $$
6. **Inert mass.**
   $$
   \begin{aligned}
   m_\text{inert} &= \frac{0.17}{0.83} \times 5{,}628.6\\
   &= 1{,}152.8\ \text{kg}
   \end{aligned}
   $$
7. **Final and initial mass.**
   $$
   \begin{aligned}
   m_f &= 1{,}750 + 1{,}152.8\\
   &= 2{,}902.8\ \text{kg}\\
   m_i &= 2{,}902.8 + 5{,}628.6\\
   &= 8{,}531.4\ \text{kg}
   \end{aligned}
   $$

**Check.** The mass ratio is $8{,}531.4/2{,}902.8 = 2.9390$, and $3{,}168.63 \times \ln 2.9390$ gives back 3,416 m/s. The vehicle has a mass of about 8,531 kg at the first burn: 1,750 kg of payload, 1,153 kg of inert mass, and 5,629 kg of propellant ({numref}`fig-p42-example-stage`). The propellant is 3.2 times the payload.

:::{figure} figures/p42-example-stage.svg
:label: fig-p42-example-stage
:alt: Mass bar of worked example 2, to scale: payload 1,750 kilograms, inert mass 1,153 kilograms, hatched, and propellant 5,629 kilograms, the longest part. Braces below mark the final mass, 2,903 kilograms, and the initial mass, 8,531 kilograms. A brace above the inert mass and the propellant marks the stage, of which 17 percent is inert.
:width: 75%

Computed for worked example 2, one stage that makes both burns of the Hohmann transfer of page 2.2 (3,416 m/s, 323 s, inert mass fraction 0.17), masses to scale: to carry 1,750 kg of payload, the stage burns more than three times that mass in propellant.
:::

(p42-single-stage-limit)=
## How far one stage can go

The method above has a warning in step 3. Look at the denominator of [](#eq-p42-mprop), $1 - f_\text{inert}\,e^{\Delta V/c}$. As $\Delta V$ grows, $e^{\Delta V/c}$ grows, and the denominator shrinks toward zero. The propellant mass then grows without bound. When the denominator reaches zero, no amount of propellant is enough. So a stage can carry a payload only if

:::{math}
:label: eq-p42-limit
\Delta V < c\ln\frac{1}{f_\text{inert}}
:::

The right side has a physical meaning. A stage with no payload at all starts at $m_\text{inert} + m_\text{prop}$ and ends at $m_\text{inert}$, so its mass ratio is exactly $1/f_\text{inert}$. Even with zero payload, a stage with this $c$ and $f_\text{inert}$ cannot exceed $c\ln(1/f_\text{inert})$.

The {term}`payload fraction` $m_\text{pay}/m_i$ shows how quickly the available payload mass drops to zero as $\Delta V$ approaches this limit. To find it, we first write the initial mass with only the payload and the propellant in it. The stage itself, inert mass plus propellant, has the mass $m_\text{prop}/(1 - f_\text{inert})$, so

$$
\begin{aligned}
m_i &= m_\text{pay} + m_\text{inert}\\
&\;\;\; + m_\text{prop}\\
&= m_\text{pay} + \frac{m_\text{prop}}{1 - f_\text{inert}}
\end{aligned}
$$

We put [](#eq-p42-mprop) into it, with $x = \Delta V/c$ as before, and bring the bracket over one denominator:

$$
\begin{aligned}
m_i &= m_\text{pay} \times\\
&\;\;\; \left[1 + \frac{e^{x} - 1}{1 - f_\text{inert}\,e^{x}}\right]\\
&= m_\text{pay}\,\frac{e^{x}\left(1 - f_\text{inert}\right)}{1 - f_\text{inert}\,e^{x}}
\end{aligned}
$$

Dividing the payload by this initial mass gives the payload fraction:

:::{math}
:label: eq-p42-payload-fraction
\frac{m_\text{pay}}{m_i} = \frac{1 - f_\text{inert}\,e^{\Delta V/c}}{e^{\Delta V/c}\left(1 - f_\text{inert}\right)}
:::

{numref}`fig-p42-payload-fraction` plots it for three inert mass fractions. Every curve starts at 1, with no delta-V, and falls to zero at $\ln(1/f_\text{inert})$.

:::{figure} figures/p42-payload-fraction.svg
:label: fig-p42-payload-fraction
:alt: Plot of the payload fraction m pay over m i, 0 to 1, against delta-V over c, 0 to 2.8, for three inert mass fractions. Each curve starts at 1 and falls to zero at a marked point on the horizontal axis: Ariane 5 core stage, inert mass fraction 0.0796, solid line, zero at 2.531; worked example 2, 0.17, dashed line, zero at 1.772; Ariane 5 upper stage, 0.234, dotted line, zero at 1.454. An open circle on the dashed curve marks worked example 2, at a delta-V over c of 1.078, with a payload of 20.5 percent of the initial mass. A key at the upper right names the curves and the point.
:width: 85%

Computed from the payload fraction of one stage: each stage has a hard limit at $\Delta V/c = \ln(1/f_\text{inert})$, where no payload is left, and the higher the inert mass fraction, the sooner it comes. Inert mass fractions from {numref}`tbl-p42-stages` and worked example 2.
:::

The delta-V of a single stage can grow in only two ways. A higher $c$ raises the limit $c\ln(1/f_\text{inert})$ in proportion. A lower $f_\text{inert}$ raises $\ln(1/f_\text{inert})$, the value of $\Delta V/c$ where the payload reaches zero. Take the stage of worked example 2 and ask it to reach low Earth orbit, 8.833 km/s with the losses of [page 2.3](#p23-example) included. Its limit is $c\ln(1/0.17) = 3{,}168.63 \times 1.772 = 5{,}615$ m/s. It could not reach orbit even with no payload at all.

(p42-losses)=
## Gravity and drag

So far nothing outside the rocket acted on it. For a short burn in orbit that is close to true, but for a launch it is not: the vehicle climbs against gravity and pushes through the air for minutes. We now put both forces back and see where the losses of [ascent and losses](#p23-losses) come from.

{numref}`fig-p42-flight-path-forces` shows the forces on a vehicle climbing at a flight-path angle $\gamma$, the angle between its velocity and the local horizontal, as on page 2.3. We assume the thrust points along the velocity. Forces along the path count positive forward.

:::{figure} figures/p42-flight-path-forces.svg
:label: fig-p42-flight-path-forces
:alt: A launch vehicle climbing up and to the right at the flight-path angle gamma above the horizontal, shown beside it by a velocity arrow. Thrust F pushes forward on the engines at the tail, drag D pushes backward on the nose, and the weight m g points straight down from the center of mass. To the right, the weight is split into m g sine gamma, backward along the path, and m g cosine gamma, across it, at a right angle to each other; dashed lines close the rectangle whose diagonal is the weight, and the angle between the weight and the across-path part is gamma.
:width: 80%

Schematic of the forces on a climbing vehicle, with the thrust along the flight path: along the path, the thrust must first overcome drag and the weight component $mg\sin\gamma$; only the remaining net force accelerates the vehicle. At the right, the two parts of the weight are the sides of a rectangle whose diagonal is $mg$. Not to scale; outline after the Falcon 9 (SpaceX 2025).
:::

1. **Newton's second law along the path.** Thrust forward, drag and the along-path part of the weight backward:
   $$
   m\frac{dV}{dt} = F - D - mg\sin\gamma
   $$
2. **Thrust from the propellant flow.** $F = \dot m\,c$ ([page 4.1](#p41-specific-impulse)), and the {term}`mass flow rate` is the rate at which the vehicle loses mass, $\dot m = -dm/dt$:
   $$
   \begin{aligned}
   m\frac{dV}{dt} &= -c\frac{dm}{dt}\\
   &\;\;\; - D - mg\sin\gamma
   \end{aligned}
   $$
3. **Divide by $m$ and multiply by $dt$.**
   $$
   \begin{aligned}
   dV &= -c\,\frac{dm}{m}\\
   &\;\;\; - g\sin\gamma\,dt - \frac{D}{m}\,dt
   \end{aligned}
   $$
4. **Integrate over the burn** with $c$ held constant (an average over the burn), from $m_i$ to $m_f$ and from $t = 0$ to the burn time $t_b$:

:::{math}
:label: eq-p42-losses
\begin{aligned}
\Delta V &= c\ln\frac{m_i}{m_f}\\
&\;\;\; - \underbrace{\int_0^{t_b} g\sin\gamma\,dt}_{\Delta V_\text{gravity}}\\
&\;\;\; - \underbrace{\int_0^{t_b} \frac{D}{m}\,dt}_{\Delta V_\text{drag}}
\end{aligned}
:::

The first term is the ideal rocket equation, the second is the {term}`gravity loss`, and the third is the {term}`drag loss`. These are the integrals of page 2.3, which writes the thrust as $T$; this chapter writes $F$. When the thrust is not along the path, page 2.3's steering loss appears as a third loss.

A picture helps with the gravity loss. Think of a rocket whose thrust equals its weight and points straight up. It hovers: it burns propellant every second and gains no speed, so all of its ideal delta-V goes into the gravity loss, $g$ for every second of burn. The longer a launch vehicle takes to climb, the more it loses this way.

Now we turn the equation around. The delta-V that goes into the rocket equation to size a stage is what the mission needs plus the losses:

$$
\begin{aligned}
c\ln\frac{m_i}{m_f} &= \Delta V_\text{mission}\\
&\;\;\; + \Delta V_\text{gravity} + \Delta V_\text{drag}
\end{aligned}
$$

For a launch, this sum is the delta-V budget total of [page 2.3](#p23-budget). That total is the orbit speed plus the losses (1.6 km/s in its worked example), less the help from Earth's rotation. The losses shrink with a shorter burn: a higher {term}`thrust-to-weight ratio` reduces the gravity loss, though it requires heavier engines and stronger structure for higher loads ([how much thrust](#p44-thrust-to-weight)). A slender vehicle with a small cross section and a pointed nose cuts the drag loss. Launching east from a site near the equator lowers the requirement itself.

:::{warning} Add the losses, never subtract them
The losses are speed the vehicle must produce and does not keep, so the stage is sized for the orbit speed plus the losses. If you subtract them, the stage never reaches orbit.
:::

(p42-feasibility)=
## Judging a single-stage design

We now have everything needed to judge a single-stage design before drawing it. The question is always the same: whether this stage, with this engine and this structure, gives the delta-V the mission needs, losses included, and still carries something.

:::{tip} Method: judging whether one stage can do the job
1. Add the losses to the mission's delta-V. For a launch, use the budget total of [page 2.3](#p23-budget).
2. Convert $I_\text{sp}$ to $c = I_\text{sp}\,g_0$.
3. Compute $e^{\Delta V/c}$ and compare it with $1/f_\text{inert}$. If $e^{\Delta V/c}$ is larger, the design cannot work with any payload.
4. If it passes, size the stage with [](#eq-p42-mprop) and look at the payload fraction. A few percent is normal for a launch ([classifying launch vehicles](#p44-launch-vehicles)); a fraction near zero means the design has no margin.
5. Ask whether real stages of that kind reach the assumed $f_\text{inert}$ ({numref}`tbl-p42-stages`), and whether the thrust can lift the stage at all.
:::

### Worked example 3: the Ariane 5 core stage alone

The core stage of the Ariane 5 ([vehicle anatomy](#p13-launch-vehicle)) has an inert mass of 14,700 kg and carries 170,000 kg of liquid oxygen and liquid hydrogen. Its Vulcain 2 engine has a specific impulse of 432 s in vacuum and a thrust of 960 kN at sea level (Arianespace 2016, Section 1.5.1). We judge whether this stage, alone, could place a payload in the orbit of the worked example of [page 2.3](#p23-example), which needs 8.833 km/s with the losses included.

1. **Inert mass fraction.**
   $$
   \begin{aligned}
   f_\text{inert} &= \frac{14{,}700}{14{,}700 + 170{,}000}\\
   &= \frac{14{,}700}{184{,}700}\\
   &= 0.07959
   \end{aligned}
   $$
2. **Effective exhaust velocity.** $c = 432 \times 9.81 = 4{,}237.92$ m/s.
3. **The stage alone, with no payload.** Its mass ratio is $1/f_\text{inert} = 184{,}700/14{,}700 = 12.565$, so
   $$
   \begin{aligned}
   \Delta V &= 4{,}237.92 \times \ln 12.565\\
   &= 4{,}237.92 \times 2.5309\\
   &= 10{,}726\ \text{m/s}
   \end{aligned}
   $$
   This is the limit $c\ln(1/f_\text{inert})$ of [](#eq-p42-limit). It is 1,893 m/s more than the 8,833 m/s the orbit needs.
4. **Feasibility test.** With $\Delta V$ = 8,833 m/s,
   $$
   \begin{aligned}
   \frac{\Delta V}{c} &= \frac{8{,}833}{4{,}237.92}\\
   &= 2.08428
   \end{aligned}
   $$
   so $e^{\Delta V/c} = 8.0388$, smaller than $1/f_\text{inert}$ = 12.565. On masses alone, the stage passes.
5. **Largest payload.** Here the propellant is known and the payload is not, so we solve [](#eq-p42-mprop) for $m_\text{pay}$:
   $$
   \begin{aligned}
   m_\text{pay} &= m_\text{prop} \times\\
   &\;\;\; \frac{1 - f_\text{inert}\,e^{\Delta V/c}}{e^{\Delta V/c} - 1}\\
   &\;\;\; \times \frac{1}{1 - f_\text{inert}}
   \end{aligned}
   $$
   With $f_\text{inert}\,e^{\Delta V/c} = 0.07959 \times 8.0388 = 0.63981$, $e^{\Delta V/c} - 1 = 7.0388$, and $1 - f_\text{inert} = 0.92041$:
   $$
   \begin{aligned}
   &\text{numerator}\\
   &\;\;\;= 170{,}000 \times\\
   &\;\;\;\;\;\; (1 - 0.63981)\\
   &\;\;\;= 61{,}232\ \text{kg}\\
   &\text{denominator}\\
   &\;\;\;= 7.0388 \times 0.92041\\
   &\;\;\;= 6.4786
   \end{aligned}
   $$
   $$
   \begin{aligned}
   m_\text{pay} &= \frac{61{,}232}{6.4786}\\
   &= 9{,}451\ \text{kg}
   \end{aligned}
   $$
6. **Thrust.** At liftoff the stage alone weighs $184{,}700 \times 9.81 = 1{,}811{,}907$ N, or 1,812 kN. Its engine gives 960 kN at sea level, a thrust-to-weight ratio of $960/1{,}812 = 0.53$.

**Check.** With 9,451 kg on top, $m_i$ = 194,151 kg and $m_f$ = 24,151 kg, and $4{,}237.92 \times \ln(194{,}151/24{,}151)$ gives back 8,833 m/s. The payload is 4.9% of the initial mass, in the range of real launch vehicles.

**Judgment.** On masses alone, the core stage could put about 9.5 t in orbit. It cannot, for two reasons the rocket equation does not show. First, its thrust is about half its weight, so it cannot even leave the pad. Second, 432 s is its specific impulse in vacuum. At sea level the manual gives about 310 s, so on a climb from the ground even the ideal delta-V is smaller than computed here. This is why the Ariane 5 lights two solid boosters beside the core. They give about 92% of the thrust at liftoff ([vehicle anatomy](#p13-launch-vehicle)), and an upper stage rides above the core. When one stage cannot do the job, we stage the vehicle, which is the subject of [multistage rockets](multistage-rockets.md).

## Summary

:::{important} Summary
- The ideal rocket equation, $\Delta V = c\ln(m_i/m_f)$ with $c = I_\text{sp}\,g_0$ and $g_0 = 9.81\ \text{m/s}^2$, comes from conservation of momentum with no gravity and no drag. The mass ratio grows exponentially with $\Delta V/c$.
- A stage is payload, inert mass, and propellant. The inert mass fraction, $m_\text{inert}/(m_\text{inert} + m_\text{prop})$, is measured over the stage alone; real stages have 0.057 to 0.23.
- With $f_\text{inert}$, one formula gives the propellant for a payload and a delta-V. A stage can never give more than $c\ln(1/f_\text{inert})$.
- Gravity and drag losses are added to the mission's delta-V before sizing. A design is feasible only if $e^{\Delta V/c} < 1/f_\text{inert}$, the $f_\text{inert}$ is realistic, and the thrust can lift the vehicle.
:::

:::{table} The equations of this page.
:label: tbl-p42-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Ideal rocket equation (no gravity, no drag, constant $c$) | $\Delta V = c\ln(m_i/m_f)$ |
| Effective exhaust velocity ($g_0$ = 9.81 m/s² everywhere) | $c = I_\text{sp}\,g_0$ |
| Mass ratio | $m_i/m_f = e^{\Delta V/c}$ |
| Propellant share of the initial mass | $m_\text{prop}/m_i = 1 - e^{-\Delta V/c}$ |
| Final and initial mass | $m_f = m_\text{pay} + m_\text{inert}$, $m_i = m_f + m_\text{prop}$ |
| Inert mass fraction (over the stage, not over $m_i$) | $f_\text{inert} = m_\text{inert}/(m_\text{inert} + m_\text{prop})$ |
| Propellant for a payload (needs $f_\text{inert}e^{\Delta V/c} < 1$) | $m_\text{prop} = m_\text{pay}(e^{\Delta V/c} - 1)(1 - f_\text{inert})/(1 - f_\text{inert}e^{\Delta V/c})$ |
| Inert mass from the propellant | $m_\text{inert} = f_\text{inert}\,m_\text{prop}/(1 - f_\text{inert})$ |
| Limit of one stage (no payload) | $\Delta V < c\ln(1/f_\text{inert})$ |
| With gravity and drag (constant $c$) | $\Delta V = c\ln(m_i/m_f) - \Delta V_\text{gravity} - \Delta V_\text{drag}$ |

:::

:::{exercise} For discussion
:label: ex-p42-discussion

1. The rocket equation contains neither the thrust nor the burn time. Why does thrust still matter for a launch vehicle?
2. A designer lowers the inert mass fraction of a stage by two percentage points. Where does the point of zero payload in {numref}`fig-p42-payload-fraction` move, and why can a small change there matter so much near the limit?
3. Why does a burn that slows a spacecraft down require the same propellant as a burn that speeds it up by the same amount?
4. The Ariane 5 core stage passes the mass test for orbit and still cannot fly alone. What other checks should a feasibility study always include?
5. Large stages have lower inert mass fractions than small ones. Why might a designer still choose a small stage?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-4-2.html
:label: quiz-4-2
:enumerated: false
:width: 100%

Quiz for Standard 4.2: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Arianespace, *Ariane 5 User's Manual*, Issue 5 Revision 2, 2016. Section 1.5.1 (the stages, their masses, engines, and booster case).
- Arianespace, *Vega User's Manual*, Issue 4, 2014. Section 1.5.1, Figure 1.5.1a (the stages, gross and propellant masses, motor cases).
- Berkes, R., "The Ariane-5 ECA Heavy-Lift Launcher," *ESA Bulletin* 123, 2005, pp. 17 and 18.
- NASA, "[Konstantin E. Tsiolkovsky](https://web.archive.org/web/20250102011437/https://solarsystem.nasa.gov/genesismission/people/biographies/tsiolkovsky.pdf)," Genesis mission biographies, n.d. (archived copy).
- NASA, *Space Shuttle News Reference*, 1981. NASA Technical Reports Server 19810022734. Section 2, pp. 2-18 and 2-19 (the solid rocket boosters: "Statistics for each booster" and the motor case).
- NASA Glenn Research Center, "[Ideal Rocket Equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/)," Beginner's Guide to Aeronautics, 2023.
- Orloff, R. W., *Apollo by the Numbers: A Statistical Reference*, NASA SP-2000-4029, 2000. "Ground Ignition Weights," Apollo 11.
- SpaceX, *[Falcon User's Guide](https://www.spacex.com/assets/media/falcon-users-guide-2025-05-09.pdf)*, 2025. Section 2, Table 2-1 (height and diameter).
