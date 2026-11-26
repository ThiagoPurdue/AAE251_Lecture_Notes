---
title: "4.3 Multistage Rockets"
short_title: 4.3 Multistage Rockets
---

:::{include} ../_parts/standards/4.3.md
:::

A single stage faces a hard limit, because even with no payload it cannot exceed the delta-V allowed by its effective exhaust velocity and inert mass fraction. Launch vehicles get past that limit through {term}`staging <Staging>`, stacking multiple stages and dropping each one once its propellant is empty. On this page we size such a stack. We describe a staged vehicle first, then size its stages from the payload down with the method of [sizing a stage](#p42-stage-sizing). Then we ask how many stages to use and how to split the delta-V between them. We end with a real vehicle, the Saturn V that flew Apollo 11.

:::{note} What to take from this page
- Each stage carries everything above it as its payload. The top stage is sized first, and the sizing works down to the {term}`gross liftoff mass`.
- The initial mass is the payload times one factor per stage, $e^{\Delta V_k/c_k}(1 - f_{\text{inert},k})/(1 - f_{\text{inert},k}\,e^{\Delta V_k/c_k})$, and the stage delta-Vs add up to the requirement.
- With identical stages, more stages always lower the initial mass in this model, and each added stage helps less than the one before.
- For two stages there is a best split of the delta-V. Near it the initial mass hardly changes; it grows without bound as either stage nears its own limit.
:::

## Why stage

On [page 4.2](#p42-single-stage-limit) we found the limit of one stage. With inert mass fraction $f_\text{inert}$ and effective exhaust velocity $c$, no stage can give more than $c\ln(1/f_\text{inert})$, the delta-V it reaches with no payload. Take a stage with a specific impulse of 330 s and an inert mass fraction of 0.08. Its limit is 8,177 m/s, less than the 8.833 km/s of the launch we budgeted on [page 2.3](#p23-example). That stage cannot reach orbit, whatever its payload.

The problem is the empty structure that stays attached. A single stage carries its tanks, its engines, and its airframe all the way to burnout. Near the end, much of the thrust goes into speeding up tanks that are already empty. A {term}`stage` that is dropped stops being dead weight (see [the launch vehicle](#p13-launch-vehicle) for the parts of one). The next stage then accelerates only the remaining upper stages and the payload.

{numref}`fig-p43-staging-sequence` follows the mass of a two-stage vehicle through its flight. It is the vehicle of worked example 1 below, which carries a 1,750 kg satellite through the two burns of a Hohmann transfer. Stage 1 makes the first burn, and stage 2 makes the second. After the first burn, 683.1 kg of empty stage 1 is still attached. Dropping it before the second burn means stage 2 never has to speed it up.

:::{figure} figures/p43-staging-sequence.svg
:label: fig-p43-staging-sequence
:alt: Four horizontal mass bars at one scale, one under the other, numbered 1 to 4. Bar 1, first burn starts, 7,095 kilograms: the payload, then stage 2 with its inert mass and propellant, then stage 1 with its inert mass and propellant. Bar 2, first burn ends, 3,760 kilograms: stage 1's propellant is a dashed empty outline labeled burned, 3,335 kilograms. Bar 3, stage 1 dropped, 3,077 kilograms: stage 1's inert mass is a dashed outline labeled dropped, 683.1 kilograms. Bar 4, second burn ends, 1,976 kilograms: only the payload and stage 2's inert mass remain, and stage 2's propellant is labeled burned, 1,101 kilograms. A key names payload, inert mass, and propellant.
:width: 85%

Computed for worked example 1, bars to one scale: dropping the empty first stage after the first burn means the second burn pushes 3,077 kg, not 3,760 kg. The bars show the mass of the two-stage vehicle at four moments of its flight. Dashed outlines show mass that has been burned or dropped.
:::

:::{prf:definition} Staging
:label: def-p43-staging

**Staging** is building a launch vehicle as a set of rockets, called stages, each dropped once its propellant is used. In **serial staging** the stages are stacked and fire one after the other. In **parallel staging** several stages, usually solid boosters, are strapped around a central stage and burn beside it from liftoff.
:::

## How a staged vehicle is described

Before we size a multistage vehicle, we set one numbering convention. **Stage 1 is the lowest stage, the first to burn.** Stage 2 is mounted above it, and the numbering continues upward to the payload. We always number stages in the order they fire, never from the top down.

The payload of a stage is everything above it. For the top stage, that is the real payload, the satellite or spacecraft. For stage 1, it is stage 2 with all its propellant, the {term}`payload fairing`, and the payload. {numref}`fig-p43-payload-of-a-stage` shows this on the Falcon 9 of page 1.3, a two-stage vehicle. The vehicle's initial mass on the pad is its {term}`gross liftoff mass`, the initial mass of stage 1.

:::{figure} figures/p43-payload-of-a-stage.svg
:label: fig-p43-payload-of-a-stage
:alt: Two rows of a two-stage launch vehicle lying on its side, nose to the right. Top row, while stage 1 burns: the whole vehicle, with stage 1, then the interstage, cut open to show the stage 2 engine inside it and labeled as staying with stage 1. Short marks at the joint of the interstage and stage 2 read stages separate. Stage 2 with its engine and the fairing with the payload inside are shaded, and a brace under them reads payload of stage 1: stage 2, fairing, and payload. Bottom row, while stage 2 burns: only stage 2 with its engine and the fairing, with the payload on a labeled payload adapter and a brace under the payload reading payload of stage 2.
:width: 90%

Schematic of the Falcon 9, a two-stage launch vehicle, with proportions after SpaceX (2025, Section 2): each stage carries everything above it as its payload, so stage 1 carries stage 2, the fairing, and the payload, and stage 2 carries the payload. The interstage stays with stage 1. In the top row it is drawn cut open to show the stage 2 engine inside it; that engine is part of the payload of stage 1. The fairing rides on stage 2 until it is dropped partway through the second burn.
:::

Each stage is a rocket of its own, with its own effective exhaust velocity $c_k$ and its own inert mass fraction $f_{\text{inert},k}$, where $k$ is the stage number. Stage $k$ starts its burn with the vehicle at some speed and changes it by $\Delta V_k = c_k\ln(m_{i,k}/m_{f,k})$, the [rocket equation](#p42-rocket-equation) applied to that stage alone. The next stage starts from the speed the last one left. So the stage delta-Vs add up to the delta-V of the whole vehicle:

:::{math}
:label: eq-p43-sum
\Delta V = \sum_k \Delta V_k
:::

The Falcon 9 and the Saturn V use serial staging (NASA Glenn Research Center 2024). The Ariane 5 of [page 1.3](#p13-launch-vehicle) also uses parallel staging: two solid boosters burn beside the core stage from liftoff and drop away when they are empty. This page sizes serial stages. A booster is sized the same way, but its burn overlaps the core's, so its delta-V does not just add to the core's.

(p43-top-down)=
## Sizing from the top down

Now we are ready to size a multistage vehicle, which brings up an ordering question. To size stage 1 we need its payload, and that payload is all of stage 2 together with the spacecraft on top. We do not know that mass until stage 2 is sized. The only mass we know at the start is the real payload, which rides on the top stage. So we size the top stage first and work down.

Each stage is sized with the method of [sizing a stage](#p42-stage-sizing). For a stage with payload $m_\text{pay}$, delta-V $\Delta V$, effective exhaust velocity $c$, and inert mass fraction $f_\text{inert}$, [the propellant formula of page 4.2](#eq-p42-mprop) gives

$$
\begin{aligned}
m_\text{prop} &= m_\text{pay} \times\\
&\;\;\; \frac{\left(e^{\Delta V/c} - 1\right)\left(1 - f_\text{inert}\right)}{1 - f_\text{inert}\,e^{\Delta V/c}}
\end{aligned}
$$

and $m_\text{inert} = f_\text{inert}\,m_\text{prop}/(1 - f_\text{inert})$. Adding the payload, the inert mass, and the propellant gives the stage's initial mass, which becomes the payload of the stage below.

Page 4.2 wrote that initial mass as one factor times the payload ([how far one stage can go](#p42-single-stage-limit)):

$$
\begin{aligned}
m_i &= m_\text{pay} \times\\
&\;\;\; \frac{e^{\Delta V/c}\left(1 - f_\text{inert}\right)}{1 - f_\text{inert}\,e^{\Delta V/c}}
\end{aligned}
$$

Each stage multiplies the mass above it by its own factor, so for $n$ stages

:::{math}
:label: eq-p43-product
\begin{aligned}
&m_i = m_\text{pay} \times\\
&\;\;\; \prod_{k=1}^{n} \frac{e^{\Delta V_k/c_k}\left(1 - f_{\text{inert},k}\right)}{1 - f_{\text{inert},k}\,e^{\Delta V_k/c_k}}
\end{aligned}
:::

where $m_\text{pay}$ is the real payload on top. The factor of a stage is always larger than 1. It grows without bound as $f_{\text{inert},k}\,e^{\Delta V_k/c_k}$ approaches 1, which is the single-stage limit again, now for each stage.

:::{tip} Method: sizing a multistage rocket from the top down
1. Number the stages from the bottom: stage 1 burns first. Write down the delta-V, $I_\text{sp}$, and $f_\text{inert}$ of each stage, with $\sum_k \Delta V_k$ equal to the requirement.
2. Convert each specific impulse to an effective exhaust velocity, $c_k = I_{\text{sp},k}\,g_0$, with $g_0 = 9.81$ m/s².
3. Start with the top stage. Its payload is the real payload. Compute $e^{\Delta V_k/c_k}$ and check that $f_{\text{inert},k}\,e^{\Delta V_k/c_k} < 1$.
4. Size the stage with [the propellant formula of page 4.2](#eq-p42-mprop), then $m_\text{inert}$, $m_f = m_\text{pay} + m_\text{inert}$, and $m_i = m_f + m_\text{prop}$.
5. The $m_i$ of this stage is the payload of the stage below. Repeat steps 3 and 4 down to stage 1.
6. The $m_i$ of stage 1 is the gross liftoff mass. Check it with [](#eq-p43-product), and check each stage's mass ratio $m_i/m_f$ against $e^{\Delta V_k/c_k}$.
:::

:::{warning} Size from the top, and count from the bottom
If you start with stage 1, you have no payload to put in the propellant formula: its payload is the stage above, which you have not sized yet. And if you call the top stage "stage 1", you will give each stage the other stage's delta-V or engine. Stage 1 is the bottom stage; the sizing starts at the other end.
:::

### Worked example 1: two stages for a Hohmann transfer

Sometimes the mission itself splits the delta-V. On [page 2.2](#p22-hohmann) a satellite moved from a 400 km orbit to a 20,200 km orbit with two burns of 2.012 km/s and 1.404 km/s, 3.416 km/s in all. On [page 4.2](#p42-stage-sizing) one stage did both burns for a 1,750 kg satellite. It had a specific impulse of 323 s, an inert mass fraction of 0.17, and an initial mass of 8,531 kg. Now each burn gets its own stage, with the same engine and the same inert mass fraction. Stage 1 makes the first burn, $\Delta V_1 = 2{,}012$ m/s, and is dropped. Stage 2 makes the second, $\Delta V_2 = 1{,}404$ m/s. Find the mass of each stage and the initial mass.

1. **Effective exhaust velocity**, the same for both stages:
   $$
   \begin{aligned}
   c &= I_\text{sp}\,g_0\\
     &= 323 \times 9.81\\
     &= 3{,}168.6\ \text{m/s}
   \end{aligned}
   $$
2. **Stage 2 first.** Its payload is the satellite, 1,750 kg. The exponent is $\Delta V_2/c = 1{,}404/3{,}168.6 = 0.44310$, so $e^{0.44310} = 1.5575$, and $0.17 \times 1.5575 < 1$, so stage 2 can meet its delta-V requirement. The numerator and the denominator of [the propellant formula of page 4.2](#eq-p42-mprop):
   $$
   \begin{aligned}
   &m_\text{pay}\left(e^{\Delta V_2/c} - 1\right) \times\\
   &\;\;\;\left(1 - f_\text{inert}\right)\\
   &\;\;\;= 1{,}750 \times (1.5575 - 1) \times\\
   &\;\;\;\;\;\;(1 - 0.17)\\
   &\;\;\;= 809.8\ \text{kg}
   \end{aligned}
   $$

   $$
   \begin{aligned}
   &1 - f_\text{inert}\,e^{\Delta V_2/c}\\
   &\;\;\;= 1 - 0.17 \times 1.5575\\
   &\;\;\;= 0.7352
   \end{aligned}
   $$
3. **Stage 2 masses.**
   $$
   \begin{aligned}
   m_{\text{prop},2} &= 809.8/0.7352\\
                     &= 1{,}101\ \text{kg}
   \end{aligned}
   $$

   $$
   \begin{aligned}
   m_{\text{inert},2} &= \frac{0.17}{1 - 0.17} \times 1{,}101\\
                      &= 225.5\ \text{kg}
   \end{aligned}
   $$

   Then $m_{f,2} = 1{,}750 + 225.5 = 1{,}976$ kg and $m_{i,2} = 1{,}976 + 1{,}101 = 3{,}077$ kg. That is the mass at the start of the second burn, and it is the payload of stage 1.
4. **Stage 1.** Its payload is 3,077 kg. The exponent is $\Delta V_1/c = 2{,}012/3{,}168.6 = 0.63498$, so $e^{0.63498} = 1.8870$, and $0.17 \times 1.8870 < 1$.
   $$
   \begin{aligned}
   &m_\text{pay}\left(e^{\Delta V_1/c} - 1\right) \times\\
   &\;\;\;\left(1 - f_\text{inert}\right)\\
   &\;\;\;= 3{,}077 \times (1.8870 - 1) \times\\
   &\;\;\;\;\;\;(1 - 0.17)\\
   &\;\;\;= 2{,}265\ \text{kg}
   \end{aligned}
   $$

   $$
   \begin{aligned}
   &1 - f_\text{inert}\,e^{\Delta V_1/c}\\
   &\;\;\;= 1 - 0.17 \times 1.8870\\
   &\;\;\;= 0.6792
   \end{aligned}
   $$
5. **Stage 1 masses.**
   $$
   \begin{aligned}
   m_{\text{prop},1} &= 2{,}265/0.6792\\
                     &= 3{,}335\ \text{kg}
   \end{aligned}
   $$

   $$
   \begin{aligned}
   m_{\text{inert},1} &= \frac{0.17}{1 - 0.17} \times 3{,}335\\
                      &= 683.1\ \text{kg}
   \end{aligned}
   $$

   Then $m_{f,1} = 3{,}077 + 683.1 = 3{,}760$ kg, and the initial mass is
   $$
   \begin{aligned}
   m_i &= 3{,}760 + 3{,}335\\
       &= 7{,}095\ \text{kg}
   \end{aligned}
   $$

:::{figure} figures/p43-top-down.svg
:label: fig-p43-top-down
:alt: Three horizontal mass bars at one scale, one under the other, in the order of the sizing. Step 3, start at the top: the real payload alone, 1,750 kilograms. An arrow with step 4, size stage 2 for a delta-V of 1,404 meters per second, times 1.758, leads to step 5: the payload plus stage 2's inert mass and propellant, 3,077 kilograms, the payload of stage 1. A second arrow with step 4, size stage 1 for 2,012 meters per second, times 2.306, leads to step 6: the whole vehicle, 7,095 kilograms, the gross liftoff mass. Braces under the last bar name the payload, stage 2, and stage 1, and a key names payload, inert mass, and propellant.
:width: 90%

Computed for worked example 1, bars to one scale: the sizing starts from the only mass known, the real payload, and works down, each stage multiplying the mass above it by its own factor. The steps are numbered as in the method of sizing from the top down.
:::

**Check.** Each stage must give back its own delta-V. For stage 2, $m_{i,2}/m_{f,2} = 3{,}077/1{,}976 = 1.557$, which is $e^{0.44310} = 1.5575$ to the four figures the masses carry. For stage 1, $7{,}095/3{,}760 = 1.887$ against $e^{0.63498} = 1.8870$. {numref}`fig-p43-top-down` shows the order of the sizing. Each stage multiplied the mass above it by its factor of [](#eq-p43-product): $3{,}077/1{,}750 = 1.758$ for stage 2 and $7{,}095/3{,}077 = 2.306$ for stage 1. The two stages together need $8{,}531 - 7{,}095 = 1{,}436$ kg less than the single stage, 17% less ({numref}`fig-p43-one-against-two`). They burn 4,436 kg of propellant against 5,629 kg, and carry 908.6 kg of inert mass against 1,153 kg. The mass reduction comes from not pushing the empty stage 1 through the second burn. In practice, smaller stages tend to have higher inert mass fractions, and each stage requires its own engine and separation hardware. Those added masses offset part of the 17% reduction.

:::{figure} figures/p43-one-against-two.svg
:label: fig-p43-one-against-two
:alt: Two horizontal mass bars at one scale. The top bar, one stage, 8,531 kilograms: payload, inert mass, and propellant. The bottom bar, two stages, 7,095 kilograms: payload, then a brace marks stage 2 with its small inert mass and propellant, then a brace marks stage 1 with its inert mass and propellant. A dimension arrow from the end of the bottom bar to the end of the top bar is labeled 1,436 kilograms less, 17 percent. A key names payload, inert mass, and propellant.
:width: 80%

Computed for worked example 1, bars to one scale: two stages, one for each burn of the same Hohmann transfer, need 1,436 kg (17%) less initial mass than the single stage of page 4.2, with the same payload, specific impulse (323 s), and inert mass fraction (0.17).
:::

(p43-number-of-stages)=
## How many stages

Worked example 1 used two stages because the mission had two burns. A launch is one long push, and the number of stages is ours to choose. To see what the number does, we take the simplest case: $n$ identical stages, each with the same $c$ and $f_\text{inert}$, each giving the same share $\Delta V/n$. Then every factor of [](#eq-p43-product) is the same, and

:::{math}
:label: eq-p43-identical
\begin{aligned}
&m_i = m_\text{pay} \times\\
&\;\;\; \left[\frac{e^{\Delta V/(nc)}\left(1 - f_\text{inert}\right)}{1 - f_\text{inert}\,e^{\Delta V/(nc)}}\right]^{n}
\end{aligned}
:::

Each stage now reaches its limit when its share $\Delta V/n$ reaches $c\ln(1/f_\text{inert})$. Together, $n$ identical stages can give at most $n\,c\ln(1/f_\text{inert})$: each added stage moves the limit further out.

### Worked example 2: the launch with identical stages

The launch of [page 2.3](#p23-example) needs 8.833 km/s, that is 8,833 m/s, with its gravity and drag losses already included. The payload is 750 kg. Each stage has a specific impulse of 330 s and an inert mass fraction of 0.08. Find the initial mass with one, two, and three identical stages.

1. **Effective exhaust velocity.** $c = 330 \times 9.81 = 3{,}237.3$ m/s.
2. **One stage.** $\Delta V/c = 8{,}833/3{,}237.3 = 2.7285$, so $e^{2.7285} = 15.31$. That is more than $1/f_\text{inert} = 1/0.08 = 12.50$, so $f_\text{inert}\,e^{\Delta V/c} > 1$, which means a single stage cannot reach this delta-V. Its limit is $3{,}237.3 \ln 12.50 = 8{,}177$ m/s.
3. **Two stages**, 4,416.5 m/s each. The mass ratio of each stage is $e^{8{,}833/(2 \times 3{,}237.3)} = 3.91280$. The factor of one stage:
   $$
   \begin{aligned}
   &e^{\Delta V/(2c)}\left(1 - f_\text{inert}\right)\\
   &\;\;\;= 3.91280 \times 0.92\\
   &\;\;\;= 3.59978
   \end{aligned}
   $$

   $$
   \begin{aligned}
   &1 - f_\text{inert}\,e^{\Delta V/(2c)}\\
   &\;\;\;= 1 - 0.08 \times 3.91280\\
   &\;\;\;= 0.686976
   \end{aligned}
   $$

   The factor is $3.59978/0.686976 = 5.24004$. With [](#eq-p43-identical),
   $$
   \begin{aligned}
   m_i &= 750 \times {5.24004}^{2}\\
       &= 20{,}594\ \text{kg}
   \end{aligned}
   $$
4. **Three stages**, 2,944.3 m/s each. The mass ratio is $e^{8{,}833/(3 \times 3{,}237.3)} = 2.48309$, the numerator $2.48309 \times 0.92 = 2.28444$, and the denominator $1 - 0.08 \times 2.48309 = 0.801353$. The factor is $2.28444/0.801353 = 2.85073$, and
   $$
   \begin{aligned}
   m_i &= 750 \times {2.85073}^{3}\\
       &= 17{,}375\ \text{kg}
   \end{aligned}
   $$

**Check.** Each stage of the two-stage vehicle has $f_\text{inert}\,e^{\Delta V/(2c)} = 0.08 \times 3.91280 = 0.3130$, well below 1, so both stages are far from their limit. The third stage saves $20{,}594 - 17{,}375 = 3{,}219$ kg, 16% of the two-stage mass. A fourth identical stage would bring the vehicle to 16,385 kg, a further reduction of only 990 kg.

{numref}`fig-p43-number-of-stages` shows the same calculation for every delta-V, per kilogram of payload. For a small delta-V, the three curves nearly overlap, so staging gives almost no reduction in initial mass. Each curve climbs toward its own limit: 8.177 km/s for one stage, 16.35 km/s for two. At the launch delta-V the single stage is already past its limit, two stages need 27.46 kg at liftoff for each kilogram of payload, and three need 23.17 kg.

:::{figure} figures/p43-number-of-stages.svg
:label: fig-p43-number-of-stages
:alt: Plot of initial mass per kilogram of payload, on a logarithmic scale from 1 to 1,000, against delta-V from 0 to 18 kilometers per second, for one, two, and three identical stages with a specific impulse of 330 seconds and an inert mass fraction of 0.08. All three curves start at 1. The one-stage curve shoots up to a vertical dashed line at its limit, 8.177 kilometers per second. The two-stage curve rises more slowly toward its limit at 16.35 kilometers per second, and the three-stage curve lies below it. A dotted vertical line marks the launch of page 2.3 at 8.833 kilometers per second, where an open circle on the two-stage curve is labeled 27.46 and a square on the three-stage curve, just below it, is labeled 23.17.
:width: 80%

Computed from the identical-stage equation for a specific impulse of 330 s and an inert mass fraction of 0.08: each added stage moves the limit to the right, by $c\ln(1/f_\text{inert})$ = 8.177 km/s, and helps less than the one before. Vertical axis logarithmic. Markers: the launch of worked example 2, an open circle for two stages and a square for three.
:::

{numref}`fig-p43-stage-bars` breaks the three vehicles into their stages. The bottom stage always holds most of the propellant, because it pushes everything above it.

:::{figure} figures/p43-stage-bars.svg
:label: fig-p43-stage-bars
:alt: Stacked bars of initial mass in tonnes for two, three, and four identical stages. Each bar has stage 1 at the bottom, each stage's propellant with its thin inert mass above it, and the payload on top; every stage is named, the thin stage 4 with a short leader. The two-stage bar reaches 20,594 kilograms, the three-stage bar 17,375 kilograms, 3,219 kilograms less, and the four-stage bar 16,385 kilograms, only 990 kilograms less again. Stage 1's propellant is the largest part of every bar.
:width: 85%

Computed for worked example 2, stages stacked from stage 1 at the bottom to the payload on top: a third stage saves about 3 t of 21, and a fourth less than 1 t more. In every vehicle the bottom stage carries most of the propellant.
:::

In this model more stages are always lighter. This simple model leaves out the practical penalties of adding stages. Each stage requires its own engines, an interstage, a separation system, and avionics, and each staging event adds another separation and ignition that must succeed in flight. Those penalties grow with every stage we add, while the mass reduction shrinks, as the 3,219 kg and 990 kg steps show. This is why launch vehicles use two or three stages. The Falcon 9 has two, the Ariane 5 two and a pair of boosters, and the Saturn V three.

(p43-best-split)=
## Splitting the delta-V between two stages

In worked example 1 the mission set the split: one stage per burn. In worked example 2 the stages were identical, with equal shares. Real stages are not identical. A first stage is often a large kerosene stage and the upper stage a hydrogen stage with a higher specific impulse and a heavier structure for its size. Then we must choose how much of the delta-V each stage gives, and the choice changes the initial mass.

For two stages, write the share of stage 1 as $\Delta V_1/\Delta V$, so $\Delta V_2 = \Delta V - \Delta V_1$. Picture the initial mass as the share slides from 0 to 1 ({numref}`fig-p43-split-curve`):

- **At a small share**, stage 2 does almost the whole job. If that is more than stage 2 can give alone, as in worked example 3, its factor grows without bound, and so does the initial mass.
- **At a share near 1**, stage 1 does almost everything, and the same can happen to its factor.
- **In between** the mass has a minimum, and the curve is flat near it.

**Identical stages.** Swapping the shares of two identical stages swaps their factors and leaves the product in [](#eq-p43-product) unchanged. This makes the curve symmetric about a share of one half. A curve with one minimum that is symmetric about one half has its minimum at one half. Identical stages split the delta-V equally, as in worked example 2.

**Different stages.** We look for the minimum where the slope of the curve is zero. It is easier to work with $\ln m_i$, which has its minimum at the same split. From [](#eq-p43-product),

$$
\begin{aligned}
&\ln m_i = \ln m_\text{pay}\\
&\;\;\; + \sum_{k=1}^{2}\Bigl[\frac{\Delta V_k}{c_k}\\
&\;\;\; + \ln\bigl(1 - f_{\text{inert},k}\bigr)\\
&\;\;\; - \ln\bigl(1 - f_{\text{inert},k}\,e^{\Delta V_k/c_k}\bigr)\Bigr]
\end{aligned}
$$

Taking the derivative of the bracket for stage $k$ with respect to $\Delta V_k$ gives the rate of change of $\ln m_i$:

$$
\begin{aligned}
&\frac{1}{c_k} + \frac{f_{\text{inert},k}\,e^{\Delta V_k/c_k}/c_k}{1 - f_{\text{inert},k}\,e^{\Delta V_k/c_k}}\\
&\;\;\;= \frac{1}{c_k\left(1 - f_{\text{inert},k}\,e^{\Delta V_k/c_k}\right)}
\end{aligned}
$$

Because $d(\ln m_i) = dm_i/m_i$, this derivative is the fractional increase in initial mass per extra meter per second assigned to stage $k$. If we shift a small amount of delta-V from stage 2 to stage 1, the initial mass is at a minimum when the two sensitivities are equal. Setting the two derivatives equal and taking the reciprocal of both sides gives

:::{math}
:label: eq-p43-best-split
\begin{aligned}
&c_1\left(1 - f_{\text{inert},1}\,e^{\Delta V_1/c_1}\right)\\
&\;\;\;= c_2\left(1 - f_{\text{inert},2}\,e^{\Delta V_2/c_2}\right)
\end{aligned}
:::

The condition cannot be solved for $\Delta V_1$ by hand in one step. We try splits, or plot the curve and read the minimum. The condition still tells us which way to move. A larger value of $c_k(1 - f_{\text{inert},k}\,e^{\Delta V_k/c_k})$ means a smaller fractional mass increase for each added meter per second, so we should assign more delta-V to that stage. A high effective exhaust velocity raises that value, and a heavy structure lowers it. As a result, the best split gives more of the work to the stage with the higher effective exhaust velocity and the lighter structure.

The curve is flat at the minimum because its slope there is zero. Near a flat minimum, a small shift away from the optimum increases the mass only in proportion to the square of that shift, so being slightly off the best split adds little extra mass.

### Worked example 3: the best split for two different stages

Take the launch of worked example 2 again, 8,833 m/s with a 750 kg payload, now with two different stages. Stage 1, a liquid oxygen and kerosene stage, has a specific impulse of 310 s and an inert mass fraction of 0.065. Stage 2, a liquid oxygen and liquid hydrogen stage, has 440 s and 0.13. Their effective exhaust velocities are $c_1 = 3{,}041.1$ m/s and $c_2 = 4{,}316.4$ m/s. Alone, stage 1 could give at most 8,312 m/s and stage 2 at most 8,806 m/s, so neither can do the launch by itself. We size the vehicle from the top down for the equal split and one trial split, then for the best split read from the curve. {numref}`tbl-p43-splits` collects the results.

:::{table} Worked example 3: the launch of page 2.3 (8,833 m/s, 750 kg payload) with stage 1 at 310 s and an inert mass fraction of 0.065 and stage 2 at 440 s and 0.13, for three splits of the delta-V: equal, a trial split in which stage 1 gives 3,200 m/s, and the best split. Masses in kilograms. The last two rows are the two sides of the best-split condition, in meters per second.
:label: tbl-p43-splits
:align: center

<table>
<thead>
<tr><th>Quantity</th><th>Equal split</th><th>Trial split</th><th>Best split</th></tr>
</thead>
<tbody>
<tr><th scope="row">Delta-V of stage 1, m/s</th><td class="num">4,416.5</td><td class="num">3,200</td><td class="num">3,546</td></tr>
<tr><th scope="row">Delta-V of stage 2, m/s</th><td class="num">4,416.5</td><td class="num">5,633</td><td class="num">5,287</td></tr>
<tr><th scope="row">Share of stage 1</th><td class="num">0.500</td><td class="num">0.362</td><td class="num">0.401</td></tr>
<tr><th scope="row">Stage 2: mass ratio</th><td class="num">2.782</td><td class="num">3.688</td><td class="num">3.403</td></tr>
<tr><th scope="row">Stage 2: propellant, kg</th><td class="num">1,822</td><td class="num">3,369</td><td class="num">2,813</td></tr>
<tr><th scope="row">Stage 2: inert mass, kg</th><td class="num">272.2</td><td class="num">503.4</td><td class="num">420.3</td></tr>
<tr><th scope="row">Stage 2: initial mass, kg</th><td class="num">2,844</td><td class="num">4,622</td><td class="num">3,983</td></tr>
<tr><th scope="row">Stage 1: mass ratio</th><td class="num">4.273</td><td class="num">2.864</td><td class="num">3.210</td></tr>
<tr><th scope="row">Stage 1: propellant, kg</th><td class="num">12,049</td><td class="num">9,899</td><td class="num">10,398</td></tr>
<tr><th scope="row">Stage 1: inert mass, kg</th><td class="num">837.6</td><td class="num">688.2</td><td class="num">722.9</td></tr>
<tr><th scope="row">Gross liftoff mass, kg</th><td class="num">15,730</td><td class="num">15,209</td><td class="num">15,104</td></tr>
<tr><th scope="row">Condition, stage 1 side</th><td class="num">2,196</td><td class="num">2,475</td><td class="num">2,407</td></tr>
<tr><th scope="row">Condition, stage 2 side</th><td class="num">2,755</td><td class="num">2,247</td><td class="num">2,407</td></tr>
</tbody>
</table>
:::

Read the table from left to right. The equal split, the best answer for identical stages, needs 15,730 kg. The last two rows show why the equal split is not optimal. Stage 2's value, 2,755 m/s, is larger than stage 1's, 2,196 m/s, so moving delta-V to stage 2 lowers the initial mass. Giving stage 2 more, so that stage 1 gives only 3,200 m/s, brings the mass down to 15,209 kg. Now the values have crossed, 2,475 against 2,247 m/s, which means we moved a little too far. The minimum lies between the two trials. From {numref}`fig-p43-split-curve`, the minimum occurs at a share of 0.401, where stage 1 gives 3,546 m/s and stage 2 gives 5,287 m/s. There the two sides are equal, 2,407 m/s each, and the vehicle needs 15,104 kg.

The hydrogen stage, with its much higher effective exhaust velocity, does 60% of the work, even though its structure is twice as heavy for its size. The equal split requires 4.1% more initial mass than the best split, and the trial split requires only 0.70% more. Any share within 0.05 of the best adds at most 1.2% to the initial mass, and within 0.1 adds at most 5.0%.

**Check.** At the best split the two sides of the condition are equal, 2,407 m/s each. Its gross liftoff mass, 15,104 kg, is lower than at the other two splits, as a minimum must be.

:::{figure} figures/p43-split-curve.svg
:label: fig-p43-split-curve
:alt: Two panels for worked example 3. Panel a: initial mass in tonnes, 0 to 40, against the share of the delta-V given by stage 1, 0 to 1. The U-shaped curve falls steeply from the top near a share of 0.08, has a broad flat bottom, and climbs steeply past 0.8; beyond 0.941 the region is shaded and labeled stage 1 past its limit. Three markers sit close together on the flat bottom, inside a thin rectangle labeled b, and the filled dot is labeled best split. Panel b enlarges that rectangle, shares 0.30 to 0.54 and masses from about 14.9 to 16 tonnes: the filled dot is the best split, 15.10 tonnes at a share of 0.401; a square is the trial split, 15.21 tonnes at 0.362; an open circle is the equal split, 15.73 tonnes.
:width: 80%

Computed for worked example 3: the initial mass has a best split of the delta-V, at a share of 0.401 for stage 1. Near it the mass changes little, and it grows without bound as either stage nears its limit. Stage 1 alone reaches its limit at a share of 0.941; stage 2 reaches its own only at a share of 0.003. Panel (b) enlarges the rectangle outlined in panel (a): the bottom of the curve around the three splits of the table.
:::

:::{warning} Do not split the delta-V equally by habit
The equal split is the best split only when the stages are identical. When the stages differ, check the two sides of [](#eq-p43-best-split) at your split. If they are not equal, move delta-V toward the stage with the larger side, and size again.
:::

## A real vehicle: the Saturn V

The Saturn V that launched Apollo 11 had three serial stages. The S-IC had five F-1 engines burning liquid oxygen and kerosene. The S-II had five J-2 engines and the S-IVB one J-2, both burning liquid oxygen and liquid hydrogen. NASA published the mass of every part of the vehicle at ignition (Orloff 2000) and the measured specific impulse of each stage (NASA MSFC 1969). With those numbers we can turn the sizing around: the masses give each stage's inert mass fraction and the ideal delta-V it gave. {numref}`tbl-p43-saturn` has the results.

A stage's mass at ignition is the stage plus everything above it. Two items drop away early in the S-II burn: the interstage between the first two stages and the launch escape tower on top of the spacecraft. We take them off at S-II ignition. The S-IVB burned twice, once to reach the parking orbit and once to leave it for the Moon, so its row covers both burns.

:::{table} The three stages of the Apollo 11 Saturn V. Masses from the ground ignition weights in Orloff (2000), converted from pounds; propellant is oxidizer plus fuel; the inert mass is the stage without its propellant (the source's dry mass). Specific impulse and the speed at cutoff (space-fixed, measured) from NASA MSFC (1969), Table 5-1, p. 6-4, Table 7-1, and Table 4-2; the S-IC value is the highest of the five engines' values reduced to standard sea level (263.5 to 265.0 s). The inert mass fraction, the masses at ignition and burnout, and the ideal delta-V are computed.
:label: tbl-p43-saturn
:align: center

<table>
<thead>
<tr><th>Quantity</th><th>S-IC (stage 1)</th><th>S-II (stage 2)</th><th>S-IVB (stage 3)</th></tr>
</thead>
<tbody>
<tr><th scope="row">Engines</th><td>five F-1</td><td>five J-2</td><td>one J-2</td></tr>
<tr><th scope="row">Propellants</th><td>liquid oxygen and kerosene (RP-1)</td><td>liquid oxygen and liquid hydrogen</td><td>liquid oxygen and liquid hydrogen</td></tr>
<tr><th scope="row">Propellant, t</th><td class="num">2,146</td><td class="num">443.2</td><td class="num">107.1</td></tr>
<tr><th scope="row">Inert mass, t</th><td class="num">130.4</td><td class="num">36.16</td><td class="num">11.27</td></tr>
<tr><th scope="row">Specific impulse, s</th><td class="num">265 (sea level)</td><td class="num">423.2</td><td class="num">428.7</td></tr>
<tr><th scope="row">Inert mass fraction</th><td class="num">0.0573</td><td class="num">0.0754</td><td class="num">0.0952</td></tr>
<tr><th scope="row">Mass at ignition, t</th><td class="num">2,938</td><td class="num">650.4</td><td class="num">166.8</td></tr>
<tr><th scope="row">Mass at burnout, t</th><td class="num">792.5</td><td class="num">207.1</td><td class="num">59.66</td></tr>
<tr><th scope="row">Ideal delta-V, km/s</th><td class="num">3.407</td><td class="num">4.750</td><td class="num">4.323</td></tr>
<tr><th scope="row">Speed at cutoff, km/s</th><td class="num">2.764</td><td class="num">6.916</td><td class="num">7.791 (first burn), 10.84 (second burn)</td></tr>
</tbody>
</table>
:::

The three stages give 12.48 km/s of ideal delta-V together ({numref}`fig-p43-saturn-v`), and the largest share, the S-II's, is 4.750 km/s. No single stage comes close to the total. Even the S-II, which has the best mix of high specific impulse and light structure, could give at most $c\ln(1/f_\text{inert})$ = 10.73 km/s with no payload at all.

The vehicle reached 10.84 km/s at the end of the second S-IVB burn. The 1.64 km/s difference accounts for the ascent losses and margins. It is the gravity and drag losses of [launch to orbit](#p23-losses), less the help from Earth's rotation, plus the propellant still in the tanks at each cutoff. The true difference is larger, because the S-IC's sea-level specific impulse is lower than its average over a burn that climbs out of the atmosphere.

:::{figure} figures/p43-saturn-v.svg
:label: fig-p43-saturn-v
:alt: Bar chart of ideal delta-V in kilometers per second. Three floating bars stack on each other: the first stage, S-IC, from 0 to 3.407; the second stage, S-II, adds 4.750; the third stage, S-IVB, both burns, adds 4.323. A fourth bar, the sum of the three, rises to 12.48. A dashed horizontal line at 10.84 kilometers per second is labeled speed reached at translunar injection; the sum lies above it, and a double arrow beside the sum bar marks the gap, 1.64 kilometers per second: losses, less Earth's rotation, plus unburned propellant.
:width: 80%

Computed from the masses of Orloff (2000) and the specific impulses of NASA MSFC (1969): the three stages of the Apollo 11 Saturn V share about 12.5 km/s of ideal delta-V, none more than 4.8 km/s, and the sum exceeds the 10.84 km/s the vehicle reached because the climb has losses. The gap, 1.64 km/s, is marked beside the sum.
:::

The table also explains the propellant choice for each stage. The S-IC must lift the entire 2,938 t vehicle off the pad, so it needs high thrust while keeping the tank volume manageable. That favors kerosene, about 11 times denser than liquid hydrogen (Huzel and Huang 1967, Tables 1-4 and 1-5). Higher up, every kilogram of an upper stage is multiplied by the factors of all the stages below it, as [](#eq-p43-product) shows. A high specific impulse gives the largest mass reduction in the upper stages, which is why the S-II and S-IVB burn liquid hydrogen at 423.2 and 428.7 s. Their inert mass fractions are higher than the S-IC's, as worked example 3 assumed. Propellants are compared in detail on [propellant selection](#p44-propellant-properties).

## Summary

:::{important} Summary
- Staging drops empty tanks and engines so later burns do not push them. Stage 1 is the bottom stage, and the payload of a stage is everything above it.
- Size from the top down: the real payload is the only mass known first. Each stage multiplies the mass above it by $e^{\Delta V_k/c_k}(1 - f_{\text{inert},k})/(1 - f_{\text{inert},k}\,e^{\Delta V_k/c_k})$, and $\Delta V = \sum_k \Delta V_k$.
- $n$ identical stages reach at most $n\,c\ln(1/f_\text{inert})$. More stages always lower the mass in this model, by less each time; real vehicles stop at two or three because each stage adds practical penalties that the model leaves out.
- For two stages the best split satisfies $c_1(1 - f_{\text{inert},1}\,e^{\Delta V_1/c_1}) = c_2(1 - f_{\text{inert},2}\,e^{\Delta V_2/c_2})$. Identical stages split equally; otherwise the stage with the higher effective exhaust velocity and lighter structure does more. The minimum is flat.
:::

:::{table} The equations of this page.
:label: tbl-p43-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Delta-V of the vehicle (stage 1 is the lowest) | $\Delta V = \sum_k \Delta V_k$ |
| Propellant of one stage (its payload is everything above it) | $m_\text{prop} = m_\text{pay}(e^{\Delta V/c} - 1)(1 - f_\text{inert})/(1 - f_\text{inert}\,e^{\Delta V/c})$ |
| Initial mass of $n$ stages (size from the top down) | $m_i = m_\text{pay}\prod_k e^{\Delta V_k/c_k}(1 - f_{\text{inert},k})/(1 - f_{\text{inert},k}\,e^{\Delta V_k/c_k})$ |
| $n$ identical stages, equal shares | $m_i = m_\text{pay}\left[e^{\Delta V/(nc)}(1 - f_\text{inert})/(1 - f_\text{inert}\,e^{\Delta V/(nc)})\right]^n$ |
| Limit of $n$ identical stages | $\Delta V < n\,c\ln(1/f_\text{inert})$ |
| Best split of two stages | $c_1(1 - f_{\text{inert},1}\,e^{\Delta V_1/c_1}) = c_2(1 - f_{\text{inert},2}\,e^{\Delta V_2/c_2})$ |

:::

:::{exercise} For discussion
:label: ex-p43-discussion

1. In worked example 1 the two stages carry less propellant in total than the single stage. Where exactly does the propellant saving come from?
2. Why does a solid booster strapped to a core stage not just add its delta-V to the core's, as a serial stage does?
3. If a fourth stage saves 990 kg in worked example 2, what would have to be true of its engines, interstage, and separation system for it to be worth flying?
4. In worked example 3, what happens to the best split if stage 2's inert mass fraction rises from 0.13 to 0.16? Answer from the condition before you compute.
5. The Saturn V's ideal delta-V exceeds the speed it reached by 1.64 km/s. Which of the losses would you expect to be largest, and in which stage?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-4-3.html
:label: quiz-4-3
:enumerated: false
:width: 100%

Quiz for Standard 4.3: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Huzel, D. K., and Huang, D. H., *Design of Liquid Propellant Rocket Engines*, NASA SP-125, 1967. Tables 1-4 and 1-5.
- NASA Glenn Research Center, "[Booster Staging Interactive](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/stage/)," Beginner's Guide to Aeronautics, 2024.
- NASA Marshall Space Flight Center, *Saturn V Launch Vehicle Flight Evaluation Report AS-506, Apollo 11 Mission*, MPR-SAT-FE-69-9, 1969. Table 4-2, Table 5-1, p. 6-4, and Table 7-1.
- Orloff, R. W., *Apollo by the Numbers: A Statistical Reference*, NASA SP-2000-4029, 2000. "Ground Ignition Weights."
- SpaceX, *Falcon User's Guide*, 2025. Section 2.
