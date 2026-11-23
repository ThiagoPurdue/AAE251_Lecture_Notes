---
title: "Wing loading"
short_title: Wing loading
---

Pages 3.2 and 3.3 found the lift and drag of a wing whose size was given. Here we turn the question around and choose the size. A designer picks the wing loading, the weight each square meter of wing carries, and from it the wing area. Two kinds of requirement set it: a stall speed the aircraft must not exceed, and a cruise condition at which it should fly efficiently. No course standard is assessed on this page.

:::{note} What to take from this page
- Three numbers size an aircraft early in design: the wing loading $W/S$ sets the wing area, the thrust-to-weight (or power-to-weight) ratio sets the engines, and the aspect ratio sets the wing's shape.
- Wing loading has the units of a pressure, lb/ft² or N/m². Typical values run from under 3 lb/ft² for a solar-powered aircraft to more than 200 lb/ft² for a cruise missile.
- A stall-speed requirement caps the wing loading at $\tfrac12 \rho V_\text{stall}^2 C_{L,\max}$. Flaps raise $C_{L,\max}$ and so allow a smaller wing.
- A cruise condition asks for $W/S = q\,C_L$ at the chosen $C_L$. When the two disagree, the smaller wing loading wins, because the wing must meet both.
:::

(p34-three-numbers)=
## Three numbers that size an aircraft

Three ratios decide, more than any other numbers, what a new aircraft looks like ({numref}`fig-p34-design-parameters`):

- The {term}`wing loading` $W/S$, the takeoff weight divided by the wing area, sets the size of the wing. [Page 1.3](#p13-wing-geometry) defines it.
- The {term}`thrust-to-weight ratio` $T/W$ sets the size of the engines. A propeller aircraft uses the power-to-weight ratio $P/W$ instead, because its engine is rated in power.
- The {term}`aspect ratio` $\textit{AR} = b^2/S$ sets the shape of the wing: long and slender, or short and broad.

:::{figure} figures/p34-design-parameters.svg
:label: fig-p34-design-parameters
:alt: Plan view of a Boeing 737-800 drawn to scale, nose to the left. The wing is shaded and labeled wing area S equals 124.60 square meters, set by the wing loading W over S. The shading continues across the fuselage between dashed lines that carry the leading and trailing edges through it. The two engines are hatched and labeled: their thrust is set by the thrust-to-weight ratio T over W. A dimension on the right gives the span b, 34.30 meters, which with S sets the aspect ratio b squared over S, 9.44.
:width: 85%

Drawn to scale from the published dimensions of the Boeing 737-800. Each part is sized by one ratio: the wing area by the wing loading, the engines by the thrust-to-weight ratio, and the wing's shape by the aspect ratio. The reference area $S$ includes the part of the wing hidden inside the fuselage, shaded between dashed lines. Data from Jenkinson et al. (1999, Data A, Table 2).
:::

Here we take the first of the three. The wing loading "sizes the wing and locks in the dominant performance features of the aircraft" (Nicolai and Carichner 2010, Section 6.1). It fixes how slowly the aircraft can fly, how efficiently it cruises, and how sharply it can turn.

### The units of wing loading

The units follow from the lift equation of [page 3.2](#p32-coefficients). We divide the lift by the wing area:

:::{math}
:label: eq-p34-lift-per-area
\begin{aligned}
L &= q\,S\,C_L\\
\frac{L}{S} &= q\,C_L\\
            &= \tfrac12 \rho V^2 C_L
\end{aligned}
:::

$C_L$ has no units, so $L/S$ has the units of the dynamic pressure $q$, a force per area. In steady, level flight the lift equals the weight, $L = W$. So we measure wing loading in pounds-force per square foot (lb/ft², sometimes written psf) or newtons per square meter (N/m², the same as pascals). With 1 lb = 4.448222 N and 1 ft = 0.3048 m, 1 lb/ft² = 47.880 N/m².

### Worked example 1: the wing loading of a Boeing 777-200

Jenkinson et al. (1999, Data A, Table 4) give the 777-200 a maximum takeoff mass of 242,670 kg and a wing area of 427.80 m². Find its takeoff wing loading in N/m² and in lb/ft².

1. **Weight.** The table gives a mass, and the wing loading needs a weight, $W = m\,g_0$ with $g_0 = 9.81\ \text{m/s}^2$:
   $$
   \begin{aligned}
   W &= m\,g_0 = 242{,}670 \times 9.81\\
     &= 2{,}380{,}593\ \text{N}
   \end{aligned}
   $$
2. **Wing loading in SI units.**
   $$
   \begin{aligned}
   \frac{W}{S} &= \frac{2{,}380{,}593\ \text{N}}{427.80\ \text{m}^2}\\
               &= 5{,}565\ \text{N/m}^2
   \end{aligned}
   $$
3. **In English units.**
   $$
   \begin{aligned}
   \frac{W}{S} &= \frac{5{,}565\ \text{N/m}^2}{47.880\ \text{N/m}^2\ \text{per lb/ft}^2}\\
               &= 116.2\ \text{lb/ft}^2
   \end{aligned}
   $$

**Check.** The table itself lists a "max wing load" of 567.25 kg/m², a mass per area. Times $g_0$ it gives $567.25 \times 9.81 = 5{,}565\ \text{N/m}^2$, the same result. Each square foot of the 777's wing carries about 116 lb at takeoff.

:::{warning} Mass per area is not wing loading
Data tables often give the "wing loading" of an airliner in kg/m². That is a mass per area. Multiply by $g_0$ to get N/m² before you use it in a lift equation. In English units keep pounds as pounds-force: a weight in lb over an area in ft² gives lb/ft² directly.
:::

(p34-classes)=
## Wing loading across aircraft classes

No single wing loading suits every aircraft, because the requirements that set it conflict. Nicolai and Carichner (2010, Section 6.1) list range, endurance, landing and takeoff, maneuvering in combat, acceleration to intercept, high altitude, long endurance at high altitude, and a smooth ride at low altitude. Efficient cruise tends to push the wing loading above 100 lb/ft², while a fighter that must turn hard needs a low one. The designer favors the mission phase that matters most and checks that the others stay acceptable. {numref}`fig-p34-wing-loading-classes` shows the result for aircraft built for different missions.

:::{figure} figures/p34-wing-loading-classes.svg
:label: fig-p34-wing-loading-classes
:alt: Horizontal range bars of typical takeoff wing loading, in pounds per square foot, on one scale from 0 to 350, in two panels. Transports, sailplanes and surveillance aircraft: solar high-altitude surveillance 0.5 to 3 (Helios); competition sailplanes 7 to 12 (ASW 17); fuel-burning high-altitude surveillance 25 to 50 (RQ-4A); short-field and utility transports 40 to 90 (C-130), with an open circle for the airlifter of example 2 at 71.5; short or intermediate range jets 50 to 90 (Learjet 35); long-range transports and bombers 110 to 150 (Boeing 747), with a diamond for the Boeing 777-200 of example 1 at 116.2. Fighters and cruise missiles: high altitude 30 to 60 (F-106); air to air 50 to 80 (F-15A); close air support 65 to 90 (A-10A); strike interdiction 90 to 130 (F-4E); interceptor 120 to 150 (F-104G); low-altitude cruise missiles 200 to 240 (AGM-109), with an open circle for the missile of example 3 at 322.8, beyond the end of its bar and labeled under it.
:width: 85%

Values from Nicolai and Carichner (2010, Table 6.1), in lb/ft² (multiply by 47.880 for N/m²). Aircraft that must fly slowly or turn tightly have low wing loadings; aircraft built to cruise fast and far have high ones. The 777-200 of worked example 1 and the airlifter of worked example 2 lie inside the ranges of their classes; the missile of worked example 3 lies above its class.
:::

A competition sailplane carries 7 to 12 lb/ft², because it must circle slowly and tightly inside rising air. A long-range transport carries 110 to 150 lb/ft², because a small wing has less skin, and so less friction drag, at its high cruise speed. A low-altitude cruise missile, which never lands, carries 200 to 240 lb/ft².

(p34-stall)=
## Wing loading from a stall-speed requirement

The slowest speed at which an aircraft can hold steady, level flight is its {term}`stall speed`, $V_\text{stall}$. Below it the wing cannot make enough lift to carry the weight, even at the highest {term}`lift coefficient` it can reach before it {term}`stalls <stall>`, the {term}`maximum lift coefficient` $C_{L,\max}$. A low stall speed means a slow approach and a short landing, so many requirements set a largest allowed stall speed.

At the stall speed the wing flies at $C_{L,\max}$ and still holds up the weight. We set $L = W$, $V = V_\text{stall}$ and $C_L = C_{L,\max}$ in [](#eq-p34-lift-per-area):

$$
W = \tfrac12 \rho V_\text{stall}^2\,S\,C_{L,\max}
$$

and divide both sides by $S$:

:::{math}
:label: eq-p34-stall
\frac{W}{S} = \tfrac12 \rho V_\text{stall}^2\, C_{L,\max}
:::

This is the largest wing loading that meets the requirement. A higher wing loading puts more weight on each square meter, so the wing needs more speed to carry it and the stall speed rises. The density is that of the airport where the aircraft takes off and lands, usually sea level on a standard day.

### Flaps raise the maximum lift coefficient

A trailing-edge {term}`flap` bends the rear of the wing down for takeoff and landing. The wing section gains camber and makes more lift at every {term}`angle of attack`, and its maximum lift coefficient rises by an amount $\Delta c_{l,\max}$ measured on the section. Only the part of the span that has flaps gets this gain, and sweep reduces it. We use the estimate of Nicolai and Carichner (2010, Eq. 9.9 and Fig. 9.23) for the increase on the whole wing:

:::{math}
:label: eq-p34-flap
\Delta C_{L,\max} = \Delta c_{l,\max}\,\frac{S_\text{flapped}}{S}\,K_\Lambda
:::

where $S_\text{flapped}$ is the area of the part of the wing that carries the flaps, the whole chord over the span of each flap ({numref}`fig-p34-flap-area`; Nicolai and Carichner 2010, Fig. 9.24), and $K_\Lambda$ is a correction for the sweep $\Lambda$ of the quarter-chord line,

$$
K_\Lambda = \left(1 - 0.08\cos^2\Lambda\right)\cos^{3/4}\Lambda
$$

:::{figure} figures/p34-flap-area.svg
:label: fig-p34-flap-area
:alt: The right wing of a Boeing 737-800 in plan view, the span running to the right from the side of the fuselage and the leading edge at the top. Two flaps, shaded gray, sit along the trailing edge of the inner wing, with a short gap between them. The flapped area is hatched in two strips, one over the span of each flap: each strip covers the whole chord of the wing, from the leading edge to the trailing edge, and the hatch runs over the flaps too. The outer wing, which has no flaps, and the short gap between the two flaps are left white. A dashed quarter-chord line runs from the inner end of the outer flap to the tip; at the tip an arc marks its sweep angle, Lambda, from a short spanwise reference line.
:width: 75%

Schematic, after Nicolai and Carichner (2010, Fig. 9.24), drawn on the right wing of the Boeing 737-800 to scale. The flapped area counts the whole chord over the span of each flap, not only the flaps themselves; the small gap between the flaps, which has no flap, is left out. The sweep is measured between the quarter-chord line and the spanwise direction.
:::

An unswept wing has $K_\Lambda = 0.92$. Real aircraft show what flaps buy. With slats and flaps the 777-200 reaches a $C_{L,\max}$ of about 2.8, while the U-2S, with a simple flap on part of its span, reaches about 1.2 (Nicolai and Carichner 2010, Table 9.1).

:::{tip} Wing loading from a stall speed, in steps
1. Find the air density where the requirement applies (the airport, usually sea level).
2. Take the wing's clean $C_{L,\max}$ and add the flap increment, [](#eq-p34-flap).
3. Find the largest allowed wing loading with [](#eq-p34-stall).
4. Divide the weight by it to get the smallest wing area that meets the requirement.
:::

### Worked example 2: a four-engine airlifter

An invented four-engine turboprop airlifter, a short-field and utility transport, weighs 700,000 N at takeoff. It must stall at 50 m/s or less at sea level with its flaps down. Its unswept wing has a clean $C_{L,\max}$ of 1.40; its flaps cover 0.70 of the wing area and give the section $\Delta c_{l,\max} = 1.30$. Find the largest wing loading and the smallest wing area, with and without flaps.

1. **Flap increment**, [](#eq-p34-flap), with $K_\Lambda = 0.92$ for an unswept wing:
   $$
   \begin{aligned}
   \Delta C_{L,\max} &= 1.30 \times 0.70\\
                     &\;\;\; \times 0.92\\
                     &= 0.8372
   \end{aligned}
   $$
2. **Maximum lift coefficient, flaps down.**
   $$
   \begin{aligned}
   C_{L,\max} &= 1.40 + 0.8372\\
              &= 2.237
   \end{aligned}
   $$
3. **Dynamic pressure at the stall speed.**
   $$
   \begin{aligned}
   q &= \tfrac12 \times 1.2250\ \text{kg/m}^3\\
     &\;\;\; \times {(50\ \text{m/s})}^{2}\\
     &= 1{,}531.25\ \text{N/m}^2
   \end{aligned}
   $$
4. **Largest wing loading**, [](#eq-p34-stall), flaps down and clean:
   $$
   \begin{aligned}
   \left(\frac{W}{S}\right)_\text{flaps} &= 1{,}531.25\\
                                         &\;\;\; \times 2.237\\
                                         &= 3{,}425\ \text{N/m}^2
   \end{aligned}
   $$
   $$
   \begin{aligned}
   \left(\frac{W}{S}\right)_\text{clean} &= 1{,}531.25\\
                                         &\;\;\; \times 1.40\\
                                         &= 2{,}144\ \text{N/m}^2
   \end{aligned}
   $$
5. **Smallest wing area.**
   $$
   \begin{aligned}
   S_\text{flaps} &= \frac{700{,}000\ \text{N}}{3{,}425\ \text{N/m}^2}\\
                  &= 204.4\ \text{m}^2
   \end{aligned}
   $$
   $$
   \begin{aligned}
   S_\text{clean} &= \frac{700{,}000\ \text{N}}{2{,}144\ \text{N/m}^2}\\
                  &= 326.5\ \text{m}^2
   \end{aligned}
   $$

**Check.** In English units the flaps-down limit is $3{,}425/47.880 = 71.53\ \text{lb/ft}^2$, inside the 40 to 90 lb/ft² of short-field and utility transports in {numref}`fig-p34-wing-loading-classes`. Without flaps the wing would need 60% more area. {numref}`fig-p34-stall-speed` shows both limits at every stall speed.

:::{figure} figures/p34-stall-speed.svg
:label: fig-p34-stall-speed
:alt: Wing loading in newtons per square meter against stall speed from 36 to 64 meters per second. Two rising curves: flaps down, C L max 2.237, solid; clean, C L max 1.40, dashed and lower. A vertical dashed line at 50 meters per second marks the requirement. Where it meets the curves, dots mark the largest allowed wing loadings: 3,425 newtons per square meter with flaps down and 2,144 clean. A dimension between the two dots, what the flaps add, is labeled q delta C L max equals 1,282 newtons per square meter.
:width: 85%

Computed from [](#eq-p34-stall) at sea level for the airlifter of worked example 2. The allowed wing loading grows with the square of the stall speed, and the flaps raise it at every speed: at the required 50 m/s the flapped wing may carry 3,425 N/m². The flaps add $q\,\Delta C_{L,\max} = 1{,}282$ N/m² to the clean wing's limit.
:::

:::{warning} Which maximum lift coefficient
Use the $C_{L,\max}$ of the configuration the requirement names: flaps down for a landing stall speed, clean for a requirement in cruise. Use the wing's $C_{L,\max}$, not the airfoil's $c_{l,\max}$, because the wing's is lower (see [the lift curve of a finite wing, page 3.2](#p32-lift-curve)). And remember that $V_\text{stall}$ is squared: if you ask for a stall speed 10% slower, you allow 19% less wing loading.
:::

(p34-cruise)=
## Wing loading from a cruise condition

In steady, level cruise the lift again equals the weight. So [](#eq-p34-lift-per-area) gives the wing loading that makes the wing fly at a chosen lift coefficient:

:::{math}
:label: eq-p34-cruise
\frac{W}{S} = q\,C_L = \tfrac12 \rho V^2 C_L
:::

The cruise altitude and speed fix $q$, and the designer chooses $C_L$. For a propeller aircraft flying for best range, that $C_L$ is the one of the maximum lift-to-drag ratio (Nicolai and Carichner 2010, Section 6.2), the $C_L^* = \sqrt{C_{D,0}/K}$ found on [page 3.3](#p33-minimum-drag). For a jet cruising for best range at a constant altitude the best value is lower, $C_L = \sqrt{C_{D,0}/(3K)}$. We derive both conditions in Chapter 5; here we use them as given.

### Worked example 3: an air-launched cruise missile

Nicolai and Carichner (2010, Example 6.1) size the wing of a low-altitude cruise missile. It weighs 1,800 lb at launch and cruises at Mach 0.7 at 200 ft, close enough to sea level to use $\rho = 0.002377\ \text{slug/ft}^3$ and a speed of sound of 1,116.4 ft/s. Its drag polar has $C_{D,0} = 0.035$ and $K = 0.059$. Find the wing loading and the wing area for best jet range at constant altitude.

1. **Lift coefficient.**
   $$
   \begin{aligned}
   C_L &= \sqrt{\frac{0.035}{3 \times 0.059}}\\
       &= \sqrt{0.19774}\\
       &= 0.4447
   \end{aligned}
   $$
2. **Speed and dynamic pressure.** The speed is Mach 0.7 times the speed of sound:
   $$
   \begin{aligned}
   V &= 0.7 \times 1{,}116.4\\
     &= 781.48\ \text{ft/s}
   \end{aligned}
   $$
   $$
   \begin{aligned}
   q &= \tfrac12 \times 0.002377\\
     &\;\;\; \times {781.48}^{2}\\
     &= 725.8\ \text{lb/ft}^2
   \end{aligned}
   $$
3. **Wing loading**, [](#eq-p34-cruise):
   $$
   \begin{aligned}
   \frac{W}{S} &= 725.8 \times 0.4447\\
               &= 322.76\ \text{lb/ft}^2
   \end{aligned}
   $$
4. **Wing area.**
   $$
   \begin{aligned}
   S &= \frac{1{,}800\ \text{lb}}{322.76\ \text{lb/ft}^2}\\
     &= 5.577\ \text{ft}^2
   \end{aligned}
   $$

**Check.** Nicolai and Carichner round $C_L$ to 0.44 and find 319 lb/ft² and 5.64 ft². The result lies above the 200 to 240 lb/ft² of the class; their Table 6.1 gives typical values, not limits. The same example also shows the cost of sizing for one point of the flight only. As fuel burns at constant altitude and speed, $C_L$ falls below the best value, and the $L/D$ drops from 9.5 at launch to 6.9 at the end. The launch weight of 1,800 lb came from assuming $L/D = 9.5$ for the whole flight. Sized with the average $L/D$ of 8.2, the missile comes out near 2,860 lb at launch, the weight of the Tomahawk, a missile of this class.

(p34-two-requirements)=
## The two requirements together

A wing must meet every requirement at once. The stall requirement sets a largest wing loading; the cruise condition sets the one the designer would like. If the cruise value is larger than the stall limit, the designer takes the stall limit: the smaller wing loading, which means the larger wing.

:::{prf:definition} Design wing loading
:label: def-p34-design-wing-loading

The wing loading chosen for the design: the value the most important mission phase asks for, lowered to the smallest limit set by the other requirements (such as a stall speed) when it exceeds that limit. The takeoff weight divided by it gives the wing area.
:::

### Worked example 4: the airlifter in cruise

The airlifter of worked example 2 cruises at 7,000 m and 135 m/s for best range. Its drag polar has $C_{D,0} = 0.028$, $\textit{AR} = 10.0$ and $e = 0.80$. Find the wing loading cruise asks for and choose the design wing loading. We compare both wing loadings at the takeoff weight, which is close to the weight at the start of cruise. A full design would convert the cruise value with the weight fraction at that point of the mission ([page 1.6](../chapter-1/aircraft-sizing.md)).

1. **Drag-polar constant and best-range $C_L$.**
   $$
   \begin{aligned}
   K &= \frac{1}{\pi \times 0.80 \times 10.0}\\
     &= 0.039789
   \end{aligned}
   $$
   $$
   \begin{aligned}
   C_L^* &= \sqrt{\frac{0.028}{0.039789}}\\
         &= \sqrt{0.70371}\\
         &= 0.8389
   \end{aligned}
   $$
2. **Dynamic pressure.** The [standard atmosphere](../chapter-1/standard-atmosphere.md) gives $\rho = 0.58924\ \text{kg/m}^3$ at 7,000 m:
   $$
   \begin{aligned}
   q &= \tfrac12 \times 0.58924 \times {135}^{2}\\
     &= 5{,}369\ \text{N/m}^2
   \end{aligned}
   $$
3. **Wing loading for cruise**, [](#eq-p34-cruise):
   $$
   \begin{aligned}
   \frac{W}{S} &= 5{,}369 \times 0.8389\\
               &= 4{,}504\ \text{N/m}^2
   \end{aligned}
   $$
4. **Choice.** The stall limit, 3,425 N/m², is smaller, so the design takes $W/S = 3{,}425\ \text{N/m}^2$ and the wing area of 204.4 m².
5. **What cruise gives up.** With the larger wing the airlifter cruises at a lower lift coefficient:
   $$
   \begin{aligned}
   C_L &= \frac{3{,}425}{5{,}369}\\
       &= 0.638
   \end{aligned}
   $$
   $$
   \begin{aligned}
   C_D &= 0.028\\
       &\;\;\; + 0.039789 \times {0.638}^{2}\\
       &= 0.04420
   \end{aligned}
   $$
   $$
   \begin{aligned}
   \frac{L}{D} &= \frac{0.638}{0.04420}\\
               &= 14.43
   \end{aligned}
   $$
   The best possible is $(L/D)_{\max} = 14.98$, so the airlifter keeps 96.3% of it.

**Check.** {numref}`fig-p34-two-requirements` draws the cruise $L/D$ at every wing loading. The curve is flat near its peak, so the larger wing costs little in cruise. The designer could also cruise higher, where the lower density brings $q\,C_L^*$ down to the stall limit.

:::{figure} figures/p34-two-requirements.svg
:label: fig-p34-two-requirements
:alt: Cruise lift-to-drag ratio of the airlifter at 7,000 meters and 135 meters per second against wing loading from 1,500 to 7,000 newtons per square meter. The curve rises to a peak of 14.98 at 4,504, marked with an open square as best for cruise, then falls slowly. A dashed vertical line at 3,425 marks the stall limit; the region to its right is shaded as not allowed, where the stall speed with flaps down exceeds 50 meters per second. A filled dot at 3,425 marks the design point, L over D 14.43. A small dimension between the design point and the level of the peak is labeled minus 3.7 percent.
:width: 85%

Computed from the drag polar of worked example 4 with $C_L = (W/S)/q$. Cruise alone would choose 4,504 N/m², but the stall requirement forbids every wing loading above 3,425 N/m². The design takes the stall limit and loses less than 4% of the best lift-to-drag ratio.
:::

## Summary

:::{important} Summary
- Wing loading, thrust-to-weight ratio, and aspect ratio size the wing, the engines, and the wing's shape. Wing loading is a force per area, lb/ft² or N/m² (1 lb/ft² = 47.880 N/m²).
- A stall-speed requirement allows at most $W/S = \tfrac12 \rho V_\text{stall}^2 C_{L,\max}$. Flaps add $\Delta c_{l,\max}\,(S_\text{flapped}/S)\,K_\Lambda$ to $C_{L,\max}$ and so allow a smaller wing.
- A cruise condition asks for $W/S = q\,C_L$ at the chosen $C_L$: $C_L^*$ for a propeller aircraft at best range.
- The design takes the cruise value unless a limit such as the stall speed is lower; then it takes the limit. The wing area follows as $S = W/(W/S)$.
:::

:::{table} The equations of this page.
:label: tbl-p34-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Lift per unit wing area | $L/S = q\,C_L$ |
| Wing loading from a stall speed | $W/S = \tfrac12 \rho V_\text{stall}^2 C_{L,\max}$ |
| Flap increment for the wing | $\Delta C_{L,\max} = \Delta c_{l,\max}\,(S_\text{flapped}/S)\,K_\Lambda$ |
| Wing loading for cruise | $W/S = q\,C_L$ |
| Wing area | $S = W/(W/S)$ |

:::

:::{exercise} For discussion
:label: ex-p34-discussion

1. A sailplane and a long-range airliner both want a high lift-to-drag ratio, yet their wing loadings differ by a factor of about ten. Which requirement explains the difference?
2. An airport at high altitude has thinner air. How does that change the largest wing loading allowed by the same stall speed, and what can the designer do about it?
3. The airlifter keeps 96.3% of its best $L/D$ with a wing sized by the stall speed. Name two costs of the larger wing that the $L/D$ curve does not show.
:::

## References

- Jenkinson, L. R., Simpkin, P., and Rhodes, D., *Civil Jet Aircraft Design*, Arnold and Butterworth-Heinemann, 1999. Companion web site, Data A, Aircraft Data File, Boeing aircraft: [Table 2](https://booksite.elsevier.com/9780340741528/appendices/data-a/table-2/table.htm) and [Table 4](https://booksite.elsevier.com/9780340741528/appendices/data-a/table-4/table.htm).
- Nicolai, L. M., and Carichner, G. E., *Fundamentals of Aircraft and Airship Design*, Vol. 1, AIAA, 2010. Chapter 6 (Section 6.1, Section 6.2, Table 6.1, Example 6.1) and Chapter 9 (Eq. 9.9, Figures 9.23 and 9.24, Table 9.1).
- NOAA, NASA, and U.S. Air Force, *[U.S. Standard Atmosphere, 1976](https://ntrs.nasa.gov/citations/19770009539)*, NOAA-S/T 76-1562, NASA-TM-X-74335, 1976.
