---
title: "Constraint diagram and field length"
short_title: Constraint diagram and field length
---

In pages 5.1 through 5.3, we analyzed an aircraft whose wing area and engine thrust were already given. Early in conceptual design, we work in reverse. We start with the customer's performance requirements (stall speed, runway length, climb rate, cruise speed, and ceiling). Then we ask how small the wing and engines can be while still meeting all of them. Putting all of those requirements on one plot of {term}`thrust-to-weight ratio` $T/W$ against {term}`wing loading` $W/S$ builds the **{term}`constraint diagram`**, tying Chapter 3's wing sizing ([page 3.4](../chapter-3/wing-loading.md)) directly to Chapter 5's performance equations. No course standard is assessed on this page.

:::{note} What to take from this page
- Takeoff and landing ground rolls scale linearly with wing loading $W/S$ and inversely with $C_{L,\max}$, so smaller wings and lower-lift flaps require longer runways.
- Every performance requirement turns into one boundary curve on a plot of sea-level $T/W$ against $W/S$. Stall speed and landing distance set vertical upper limits on $W/S$, while takeoff, climb, cruise, and ceiling set lower limits on $T/W$.
- The feasible design space lies above every thrust boundary and to the left of every wing-loading limit.
- Picking the corner with the lowest $T/W$ and largest feasible $W/S$ gives the smallest engines and smallest wing that meet every requirement at once.
:::

(p55-field-length)=
## Takeoff and landing ground roll

A takeoff or landing splits into two parts ({numref}`fig-p55-takeoff-landing-phases`): an **air distance** over a standard $15$ m ($50$ ft) obstacle, and a **ground roll** along the runway. In preliminary sizing, we use closed-form ground-roll formulas that link runway length straight to wing loading $W/S$ and thrust-to-weight ratio $T/W$ (Anderson 2016, Sections 6.17 and 6.18).

:::{figure} figures/p55-takeoff-landing-phases.svg
:label: fig-p55-takeoff-landing-phases
:alt: Two stacked schematic diagrams. Panel 1, titled takeoff, shows an aircraft rolling horizontally from brake release to liftoff at V sub L O equals 1.2 V sub stall over a dimension labeled ground roll s sub L O, then curving upward over a dimension labeled air distance to clear a 15 meter obstacle. Panel 2, titled landing, shows an aircraft descending from a 15 meter obstacle over an air distance to touchdown at V sub T equals 1.3 V sub stall, then rolling horizontally over a dimension labeled braking ground roll s sub L to a stop.
:width: 75%

Schematic of takeoff (Panel 1) and landing (Panel 2). Each maneuver splits into a runway ground roll (accelerating to $1.2\,V_{\text{stall}}$ on takeoff, braking from $1.3\,V_{\text{stall}}$ to rest on landing) and an air distance over a $15$ m obstacle; preliminary sizing focuses on the ground rolls $s_{\text{LO}}$ and $s_L$.
:::

We start with takeoff, where the aircraft accelerates from rest to liftoff speed $V_{\text{LO}} = 1.2\,V_{\text{stall}}$, with $V_{\text{stall}} = \sqrt{2(W/S)/(\rho\,C_{L,\max,\text{TO}})}$. Neglecting aerodynamic drag and rolling resistance compared with full takeoff thrust gives an average acceleration of $a \approx T/m = g(T/W)$. Substituting $V_{\text{LO}}^2 = 1.44\,V_{\text{stall}}^2$ into $s_{\text{LO}} = V_{\text{LO}}^2/(2a)$ cancels the factor of $2$ and gives the **liftoff ground-roll distance**:

::::{prf:definition} Liftoff ground roll and landing braking roll
:label: def-p55-field-length
:::{math}
:label: eq-p55-field-length
\begin{aligned}
s_{\text{LO}} &= \frac{1.44\,(W/S)}{\rho\,g\,C_{L,\max,\text{TO}}\,(T/W)}\\
s_L &= \frac{1.69\,(W/S)}{\rho\,g\,C_{L,\max,L}\,\mu_r}
\end{aligned}
:::
::::

On landing, the aircraft touches down at $V_T = 1.3\,V_{\text{stall}}$ with landing flaps giving $C_{L,\max,L}$. The pilot then deploys {term}`spoiler` panels to dump lift onto the wheels and brakes with effective rolling-friction coefficient $\mu_r$ (typically $0.3$ to $0.5$ on dry concrete). The braking force $\mu_r W$ gives an average deceleration of $a \approx \mu_r W/m = g\mu_r$, which gives the second line of [](#eq-p55-field-length), with ${1.3}^{2} = 1.69$.

Look at what [](#eq-p55-field-length) tells us physically:

- Both $s_{\text{LO}}$ and $s_L$ grow **linearly with $W/S$** and shrink when high-lift devices ({term}`flap` and {term}`slat` systems) raise $C_{L,\max}$.
- Takeoff roll also drops as $1/(T/W)$, because larger engines accelerate the aircraft to liftoff speed in a shorter distance.
- Landing roll does **not** depend on engine thrust (without thrust reversers), so a maximum landing distance caps $W/S$ outright.

(p55-constraint-curves)=
## Building the constraint diagram

The ground-roll equations give us runway limits on $W/S$ and $T/W$. Now we combine those limits with stall, climb, cruise, and ceiling on one chart. On a **constraint diagram**, we plot every performance requirement on a single chart of sea-level static thrust-to-weight ratio $T/W$ (vertical axis) against wing loading $W/S$ (horizontal axis). Rearranging the formulas of [page 3.4](../chapter-3/wing-loading.md) and pages 5.1 through 5.3 gives six boundaries:

1. **Stall speed** ($V_{\text{stall}}$ at sea level with landing flaps $C_{L,\max,L}$):
   $$
   \frac{W}{S} \le \tfrac12 \rho_0 V_{\text{stall}}^2 C_{L,\max,L}
   $$
   This condition gives a **vertical line**, with feasible designs to the left.
2. **Landing braking roll** ($s_L$ at sea level), from [](#eq-p55-field-length):
   $$
   \frac{W}{S} \le \frac{\rho_0\,g\,C_{L,\max,L}\,\mu_r\,s_L}{1.69}
   $$
   This condition also gives a **vertical line**, so the stricter of stall and landing sets the upper limit on $W/S$.
3. **Takeoff ground roll** ($s_{\text{LO}}$ at sea level), solving [](#eq-p55-field-length) for $T/W$:
   $$
   \frac{T}{W} \ge \frac{1.44}{\rho_0\,g\,C_{L,\max,\text{TO}}\,s_{\text{LO}}}\left(\frac{W}{S}\right)
   $$
   This gives a **straight line rising from the origin**, because higher wing loading requires proportionally more thrust to lift off in the same runway distance.
4. **Rate of climb** ($R/C$ at speed $V_{\text{cl}}$ and dynamic pressure $q_{\text{cl}}$ at sea level), using $D/W = q_{\text{cl}} C_{D,0}/(W/S) + (K/q_{\text{cl}})(W/S)$ and dividing $T_A = D + W(R/C)/V_{\text{cl}}$ by $W$:
   $$
   \frac{T}{W} \ge \frac{q_{\text{cl}}\,C_{D,0}}{W/S} + \frac{K}{q_{\text{cl}}}\left(\frac{W}{S}\right) + \frac{R/C}{V_{\text{cl}}}
   $$
5. **Cruise speed** ($V_{\text{cr}}$ at altitude $h_{\text{cr}}$, dynamic pressure $q_{\text{cr}}$, and thrust lapse $\alpha_T = (\rho_{\text{cr}}/\rho_0)^{m_{\text{ad}}}$), dividing $T_A = T_R$ by $\alpha_T W$:
   $$
   \frac{T}{W} \ge \frac{1}{\alpha_T}\left[\frac{q_{\text{cr}}\,C_{D,0}}{W/S} + \frac{K}{q_{\text{cr}}}\left(\frac{W}{S}\right)\right]
   $$
6. **Service ceiling** ($R/C = 0.5$ m/s at ceiling altitude $h_{\text{ce}}$, flying at $V_{T_R,\min}$ from [](#eq-p51-min-thrust) with lapse $\alpha_{T,\text{ce}} = (\rho_{\text{ce}}/\rho_0)^{m_{\text{ad}}}$):
   $$
   \frac{T}{W} \ge \frac{1}{\alpha_{T,\text{ce}}}\left(2\sqrt{K C_{D,0}} + \frac{0.5}{V_{T_R,\min}}\right)
   $$

Each boundary separates feasible designs from infeasible ones. To read the **feasible region**, you stay above every thrust boundary and to the left of every vertical wing-loading limit. Because bigger wings (low $W/S$) and bigger engines (high $T/W$) both add structural weight and cost, we usually pick the **lower-right corner** of the feasible region, which gives the smallest engine thrust and smallest wing area that meet every constraint.

(p55-worked-example)=
## Worked example: sizing a twin-jet utility transport

Consider a twin-jet medical and utility transport with design mass $m = 6{,}200$ kg ($W = 60{,}822$ N), $C_{D,0} = 0.023$, $\textit{AR} = 8.4$, $e = 0.82$, $C_{L,\max,\text{TO}} = 1.95$, $C_{L,\max,L} = 2.25$, braking friction $\mu_r = 0.40$, and engine lapse $m_{\text{ad}} = 0.80$. It must meet six requirements:

- Sea-level landing stall speed $V_{\text{stall}} \le 48$ m/s;
- Sea-level takeoff ground roll $s_{\text{LO}} \le 780$ m;
- Sea-level landing braking roll $s_L \le 680$ m;
- Sea-level climb rate $R/C \ge 13$ m/s at $V_{\text{cl}} = 92$ m/s;
- Cruise at $V_{\text{cr}} = 210$ m/s at $h_{\text{cr}} = 10{,}000$ m ($\rho = 0.4124$ kg/m³);
- Service ceiling $h_{\text{ce}} = 12{,}000$ m ($\rho = 0.3106$ kg/m³).

We find the feasible design point $(W/S, T/W)$, the wing area $S$, and the required sea-level static thrust per engine.

1. **Induced drag factor:**
   $$
   \begin{aligned}
   K &= \frac{1}{\pi \times 0.82 \times 8.4}\\
     &= 0.046212
   \end{aligned}
   $$
2. **Vertical wing-loading limits** (sea level, $\rho_0 = 1.2250$ kg/m³):
   $$
   \begin{aligned}
   \left(\frac{W}{S}\right)_{\text{stall}} &= 0.5 \times 1.2250 \times {48}^{2} \times 2.25\\
                                           &= 3{,}175\ \text{N/m}^2\\
   \left(\frac{W}{S}\right)_{\text{land}} &= \frac{1.2250 \times 9.81 \times 2.25 \times 0.40 \times 680}{1.69}\\
                                          &= 4{,}352\ \text{N/m}^2
   \end{aligned}
   $$
   Stall speed ($3{,}175$ N/m²) is stricter than the landing roll ($4{,}352$ N/m²), so stall sets the right-hand boundary of the feasible region.
3. **Evaluate the four thrust boundaries at $W/S = 3{,}175$ N/m²:**
   - **Takeoff roll** ($s_{\text{LO}} = 780$ m):
     $$
     \begin{aligned}
     \left(\frac{T}{W}\right)_{\text{TO}} &= \frac{1.44 \times 3{,}175}{1.2250 \times 9.81 \times 1.95 \times 780}\\
                                          &= 0.250
     \end{aligned}
     $$
   - **Sea-level climb** ($q_{\text{cl}} = 0.5 \times 1.2250 \times {92}^{2} = 5{,}184$ Pa):
     $$
     \begin{aligned}
     \left(\frac{T}{W}\right)_{\text{cl}} &= \frac{5{,}184 \times 0.023}{3{,}175} + \frac{0.046212 \times 3{,}175}{5{,}184} + \frac{13}{92}\\
                                          &= 0.207
     \end{aligned}
     $$
   - **Cruise at 10,000 m** ($q_{\text{cr}} = 0.5 \times 0.4124 \times {210}^{2} = 9{,}093$ Pa, lapse $\alpha_T = (0.4124/1.2250)^{0.80} = 0.4185$):
     $$
     \begin{aligned}
     \left(\frac{T}{W}\right)_{\text{cr}} &= \frac{1}{0.4185}\left(\frac{9{,}093 \times 0.023}{3{,}175} + \frac{0.046212 \times 3{,}175}{9{,}093}\right)\\
                                          &= 0.196
     \end{aligned}
     $$
   - **Service ceiling at 12,000 m** (lapse $\alpha_{T,\text{ce}} = (0.3106/1.2250)^{0.80} = 0.3336$, and from [](#eq-p51-min-thrust) at $W/S = 3{,}175$ N/m², $V_{T_R,\min} = 170.2$ m/s):
     $$
     \begin{aligned}
     V_{T_R,\min} &= \sqrt{\frac{2 \times 3{,}175}{0.3106}}\left(\frac{0.046212}{0.023}\right)^{1/4}\\
                  &= 170.2\ \text{m/s}\\
     \left(\frac{T}{W}\right)_{\text{ce}} &= \frac{1}{0.3336}\left(2\sqrt{0.046212 \times 0.023} + \frac{0.5}{170.2}\right)\\
                                          &= 0.204
     \end{aligned}
     $$
4. **Pick the design point and size the aircraft.** {numref}`fig-p55-constraint-diagram` plots all six boundaries. At $W/S = 3{,}175$ N/m², takeoff ($T/W = 0.250$) is the highest requirement, above climb ($0.207$), ceiling ($0.204$), and cruise ($0.196$). Choosing $(W/S, T/W) = (3{,}175\ \text{N/m}^2, 0.250)$ gives:
   $$
   \begin{aligned}
   S &= \frac{60{,}822}{3{,}175}\\
     &= 19.16\ \text{m}^2\\
   T_0 &= 0.250 \times 60{,}822\\
       &= 15{,}206\ \text{N}
   \end{aligned}
   $$
   With two engines, each needs $7{,}603$ N of sea-level static thrust.

:::{figure} figures/p55-constraint-diagram.svg
:label: fig-p55-constraint-diagram
:alt: Constraint diagram plotting sea-level thrust-to-weight ratio T over W from 0 to 0.48 against wing loading W over S from 1,400 to 4,800 newtons per square meter. A vertical brown line at 3,175 newtons per square meter marks the stall limit, and a vertical dash-dot gray line at 4,352 marks the landing limit. A solid black straight line rising from bottom left to top right marks the takeoff constraint, a dashed blue curve marks climb, a dotted orange curve marks cruise, and a dash-dot gray line near 0.204 marks ceiling. The feasible region above all thrust curves and left of the stall limit is shaded light beige. A black dot at the lower-right corner of the feasible region marks the design point: W over S equals 3,175 newtons per square meter and T over W equals 0.250.
:width: 80%

Constraint diagram for the twin-jet utility transport. The stall limit and the takeoff line are the two active constraints that fix the design point ($W/S = 3{,}175$ N/m², $T/W = 0.250$); climb, ceiling, cruise, and landing are all satisfied with margin to spare.
:::

**Check.** {numref}`fig-p55-field-length-sensitivity` shows how both ground rolls vary with wing loading. At $W/S = 3{,}175$ N/m² and $T/W = 0.250$, liftoff speed is $V_{\text{LO}} = 61.9$ m/s and $s_{\text{LO}} = 780$ m (right on the requirement). Touchdown speed is $V_T = 62.4$ m/s and the braking roll is $s_L = 496$ m, well under the $680$ m limit. Raising $T/W$ to $0.300$ would shorten the takeoff roll to $650$ m, though it would require heavier engines.

:::{figure} figures/p55-field-length-sensitivity.svg
:label: fig-p55-field-length-sensitivity
:alt: Plot of ground roll distance from 0 to 1,200 meters against wing loading W over S from 1,500 to 4,500 newtons per square meter. Three straight lines rise from left to right: a solid black line for takeoff at T over W equals 0.250 passing through a black dot at 3,175 newtons per square meter and 780 meters, a lower dashed blue line for takeoff at T over W equals 0.300, and a dotted orange line for landing braking roll (mu sub r equals 0.40) passing through an open orange square at 3,175 newtons per square meter and 496 meters.
:width: 85%

Ground-roll sensitivity to wing loading and thrust-to-weight ratio. Both takeoff and landing rolls grow linearly with $W/S$; increasing $T/W$ from $0.250$ to $0.300$ shortens the takeoff roll by one sixth without changing the landing roll.
:::

## Summary

:::{important} Summary
- Liftoff ground roll scales as $s_{\text{LO}} = 1.44(W/S)/(\rho g C_{L,\max,\text{TO}}(T/W))$; landing braking roll scales as $s_L = 1.69(W/S)/(\rho g C_{L,\max,L}\mu_r)$.
- A constraint diagram plots every performance requirement as a boundary in $(W/S, T/W)$ space. Stall and landing limit $W/S$ from the right, while takeoff, climb, cruise, and ceiling bound $T/W$ from below.
- Only the active constraints touch the corner of the feasible region; choosing that corner gives the smallest wing area $S = W/(W/S)$ and smallest total thrust $T_0 = (T/W)W$ that meet all requirements.
:::

:::{table} The equations of this page.
:label: tbl-p55-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Liftoff ground roll | $s_{\text{LO}} = 1.44(W/S)/(\rho\,g\,C_{L,\max,\text{TO}}\,(T/W))$ |
| Landing braking roll | $s_L = 1.69(W/S)/(\rho\,g\,C_{L,\max,L}\,\mu_r)$ |
| Stall wing-loading limit | $W/S \le \tfrac12\rho_0 V_{\text{stall}}^2 C_{L,\max,L}$ |
| Takeoff constraint | $T/W \ge 1.44(W/S)/(\rho_0\,g\,C_{L,\max,\text{TO}}\,s_{\text{LO}})$ |
| Climb constraint | $T/W \ge q_{\text{cl}} C_{D,0}/(W/S) + (K/q_{\text{cl}})(W/S) + (R/C)/V_{\text{cl}}$ |
| Cruise constraint | $T/W \ge (1/\alpha_T)[q_{\text{cr}} C_{D,0}/(W/S) + (K/q_{\text{cr}})(W/S)]$ |

:::

:::{exercise} For discussion
:label: ex-p55-discussion

1. On {numref}`fig-p55-constraint-diagram`, which two requirements would force you to pick larger engines or a larger wing if they became $10\%$ stricter, and which requirements have slack?
2. Why does the cruise curve slope downward with $W/S$ at low wing loading in {numref}`fig-p55-constraint-diagram`, while the takeoff line always slopes upward?
3. If the medical transport must operate from a wet runway where braking friction $\mu_r$ drops from $0.40$ to $0.25$, how does the landing boundary move on the constraint diagram, and does it become active?
4. How would adding slotted flaps that raise $C_{L,\max,\text{TO}}$ and $C_{L,\max,L}$ by $15\%$ shift the stall, landing, and takeoff boundaries?
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 6, Sections 6.17 and 6.18.
- Gudmundsson, S., *General Aviation Aircraft Design: Applied Methods and Procedures*, 2nd ed., Butterworth-Heinemann, 2022. Chapter 3, "Constraint Analysis."
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA, 2018. Chapter 5, "Thrust-to-Weight Ratio and Wing Loading."
