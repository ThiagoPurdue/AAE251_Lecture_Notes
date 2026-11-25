---
title: "5.2 Range and Endurance"
short_title: 5.2 Range and Endurance
---

:::{include} ../_parts/standards/5.2.md
:::

Every kilogram of fuel burned makes the aircraft lighter, which lowers the lift and thrust needed for level flight. On page 1.6, we used a cruise weight-fraction shortcut for preliminary sizing; here we derive the full **Breguet range and endurance equations** from scratch for both jet and propeller aircraft. A jet burns fuel in proportion to thrust, while a propeller engine burns fuel in proportion to shaft power. Because of that difference, the two propulsion types have different formulas, different optimal lift coefficients, and different responses to cruise altitude.

:::{note} What to take from this page
- {term}`Range` $R$ is total ground distance flown in still air on a load of fuel; {term}`endurance` $E$ is total time stayed aloft on that fuel.
- Fuel burn rate is proportional to thrust for a jet ($d(mg)/dt = -c_t T_A$, using {term}`thrust specific fuel consumption` $c_t$) and to shaft power for a propeller aircraft ($d(mg)/dt = -c P_A/\eta$, using {term}`power specific fuel consumption` $c$).
- Three aerodynamic ratios set the optimal cruise points: $C_L^{1/2}/C_D$ for jet range ($C_L = \sqrt{C_{D,0}/(3K)}$), $C_L/C_D$ for jet endurance and propeller range ($C_L = \sqrt{C_{D,0}/K}$), and $C_L^{3/2}/C_D$ for propeller endurance ($C_L = \sqrt{3 C_{D,0}/K}$).
- The three optimal speeds form a fixed geometric sequence spaced by ${3}^{1/4} \approx 1.316$: $V_{\text{prop,end}} = 0.760\,V_{T_R,\min}$, $V_{\text{prop,rng}} = V_{\text{jet,end}} = V_{T_R,\min}$, and $V_{\text{jet,rng}} = 1.316\,V_{T_R,\min}$.
- Jet range grows as $\rho^{-1/2}$ with altitude, which is why airliners climb to the top of the troposphere. Propeller range does not depend on air density, while propeller endurance is largest at sea level.
:::

(p52-fuel-consumption)=
## Fuel consumption: jets versus propellers

Range is the integral of airspeed over flight time, $R = \int V\,dt$, and endurance is the integral of time, $E = \int dt$. To evaluate either integral, we connect elapsed time $dt$ to the loss of aircraft weight $d(mg)$ as fuel burns. That link depends on how the engine uses fuel (Anderson 2016, Section 6.13):

- **Jet engines** burn fuel weight per second in proportion to thrust:
  :::{math}
  :label: eq-p52-fuel-jet
  \frac{d(mg)}{dt} = -c_t\,T_A
  :::
  The proportionality constant $c_t$ is the **{term}`thrust specific fuel consumption`** (TSFC), weight of fuel burned per unit thrust per unit time. Its units are $\text{N}/(\text{N}\cdot\text{s}) = 1/\text{s}$ (often quoted in $1/\text{h}$, which we divide by $3{,}600$ to get $1/\text{s}$).
- **Propeller engines** burn fuel weight per second in proportion to shaft power $P_{\text{shaft}} = P_A/\eta$:
  :::{math}
  :label: eq-p52-fuel-prop
  \frac{d(mg)}{dt} = -c\,\frac{P_A}{\eta}
  :::
  The proportionality constant $c$ is the **{term}`power specific fuel consumption`** (PSFC), weight of fuel burned per unit shaft power per unit time. In SI units its base unit is $\text{N}/(\text{W}\cdot\text{s}) = \text{N}/(\text{N}\cdot\text{m}) = 1/\text{m}$. Manufacturers often quote mass of fuel per second per kilowatt, such as $\text{g}/(\text{s}\cdot\text{kW})$; multiplying by ${10}^{-6}\,g$ converts that to $1/\text{m}$.

:::{warning} Check the units of $c_t$ and $c$ before substituting
The two specific fuel consumptions do not have the same dimensions. Jet $c_t$ has units of $1/\text{s}$ (weight per force per time), while propeller $c$ has units of $1/\text{m}$ (weight per power per time). Before you plug values into the Breguet equations, convert $c_t$ to $1/\text{s}$ (divide $1/\text{h}$ by $3{,}600$) and $c$ to $1/\text{m}$ (multiply $\text{kg}/(\text{s}\cdot\text{W})$ by $g = 9.81$ m/s²).
:::

(p52-jet-breguet)=
## Jet range and endurance

We start with a jet, where fuel burn is proportional to thrust, so steady level flight links fuel use directly to $L/D$. In steady level flight, $T_A = T_R = D = mg/(C_L/C_D)$. Solving [](#eq-p52-fuel-jet) for $dt$ gives

$$
dt = -\frac{d(mg)}{c_t\,T_R} = -\frac{1}{c_t}\frac{C_L}{C_D}\frac{dm}{m}
$$

Holding altitude, $c_t$, and $C_L$ (and so $C_D$) constant from initial mass $m_1$ to final mass $m_2 = m_1 - m_{\text{fuel}}$ lets us pull the constants outside the integral. Integrating $E = \int dt$ gives **jet endurance**:

::::{prf:definition} Breguet endurance equation for a jet
:label: def-p52-jet-endurance
:::{math}
:label: eq-p52-jet-E
E = \frac{1}{c_t}\frac{C_L}{C_D}\ln\frac{m_1}{m_2}
:::
::::

To find **jet range**, we multiply $dt$ by the level-flight airspeed $V = \sqrt{2mg/(\rho S C_L)}$ before integrating, simplifying $\sqrt{m}/m = 1/\sqrt{m}$ and $C_L/\sqrt{C_L} = \sqrt{C_L}$:

$$
dR = V\,dt = -\frac{1}{c_t}\sqrt{\frac{2g}{\rho S}}\frac{\sqrt{C_L}}{C_D}\,\frac{dm}{\sqrt{m}}
$$

Integrating $\int_{m_1}^{m_2} (-dm/\sqrt{m}) = 2(\sqrt{m_1} - \sqrt{m_2})$ gives **jet range**:

::::{prf:definition} Breguet range equation for a jet
:label: def-p52-jet-range
:::{math}
:label: eq-p52-jet-R
R = \frac{2}{c_t}\sqrt{\frac{2g}{\rho S}}\frac{\sqrt{C_L}}{C_D}\left(\sqrt{m_1} - \sqrt{m_2}\right)
:::
::::

Look at the assumptions built into [](#eq-p52-jet-E) and [](#eq-p52-jet-R): constant altitude ($\rho$ constant), constant $c_t$, and constant angle of attack ($C_L$ and $C_D$ constant). Because $V = \sqrt{2mg/(\rho S C_L)}$, holding $C_L$ and $\rho$ fixed means the jet gradually slows down and throttles back as fuel burns away ({numref}`fig-p52-weight-burn`). In airline operations, air traffic control instead assigns a constant Mach number, so the jet climbs in steps as it lightens to keep $C_L$ close to the optimum.

:::{figure} figures/p52-weight-burn.svg
:label: fig-p52-weight-burn
:alt: Two panels side by side for the executive jet flying 4,000 kilometers at 9,500 meters at constant best-range lift coefficient. Panel 1, titled airspeed slows as mass drops, shows a solid black line falling from 230.4 meters per second at 0 kilometers to 210.0 meters per second at 4,000 kilometers. Panel 2, titled thrust required drops with weight, shows a dashed blue line falling from 20.54 kilonewtons at 0 kilometers to 17.07 kilonewtons at 4,000 kilometers.
:width: 85%

Cruise at constant altitude ($9{,}500$ m) and constant $C_L$ for the executive jet of worked example 2. As $5{,}597$ kg of fuel burns over $4{,}000$ km, both the required true airspeed and the thrust required fall steadily.
:::

### Optimal flight conditions for a jet

- **Maximum jet endurance** maximizes $C_L/C_D$ in [](#eq-p52-jet-E). That is the minimum-thrust point from [page 5.1](#eq-p51-min-thrust):
  $$
  C_L = \sqrt{\frac{C_{D,0}}{K}}, \qquad C_D = 2 C_{D,0}, \qquad V = V_{T_R,\min}
  $$
- **Maximum jet range** maximizes $C_L^{1/2}/C_D$ in [](#eq-p52-jet-R). Differentiating $C_L^{1/2}/(C_{D,0} + K C_L^2)$ with respect to $C_L$ and setting the numerator to zero gives
  $$
  \tfrac12 C_L^{-1/2}(C_{D,0} + K C_L^2) - C_L^{1/2}(2 K C_L) = 0
  $$
  which simplifies to $K C_L^2 = \tfrac{1}{3} C_{D,0}$:
  :::{math}
  :label: eq-p52-jet-opt-R
  C_L = \sqrt{\frac{C_{D,0}}{3K}}, \qquad C_D = \frac{4}{3}\,C_{D,0}, \qquad V = {3}^{1/4}\,V_{T_R,\min} \approx 1.316\,V_{T_R,\min}
  :::

At maximum jet range, induced drag is only one third of parasite drag, so the jet cruises $31.6\%$ faster than its minimum-drag speed.

(p52-prop-breguet)=
## Propeller range and endurance

Now we repeat the same steps for a propeller aircraft, where fuel burn is proportional to shaft power instead of thrust. In steady level flight, $P_A = P_R = D V$. Solving [](#eq-p52-fuel-prop) for $dt$ and substituting $D = mg/(C_L/C_D)$ gives

$$
dt = -\frac{\eta}{c}\frac{d(mg)}{D V} = -\frac{\eta}{c}\frac{C_L}{C_D}\frac{dm}{m V}
$$

Notice what happens when we compute **propeller range** $dR = V\,dt$: the airspeed $V$ cancels out. Integrating from $m_1$ to $m_2$ at constant $\eta$, $c$, and $C_L$ gives

::::{prf:definition} Breguet range equation for a propeller aircraft
:label: def-p52-prop-range
:::{math}
:label: eq-p52-prop-R
R = \frac{\eta}{c}\frac{C_L}{C_D}\ln\frac{m_1}{m_2}
:::
::::

For **propeller endurance**, $V$ does not cancel. Substituting $V = \sqrt{2mg/(\rho S C_L)}$ into $dt$ and combining $C_L\sqrt{C_L} = C_L^{3/2}$ and $m\sqrt{m} = m^{3/2}$ gives

$$
dt = -\frac{\eta}{c}\sqrt{\frac{\rho S}{2g}}\frac{C_L^{3/2}}{C_D}\,\frac{dm}{m^{3/2}}
$$

Integrating $\int_{m_1}^{m_2} (-dm/m^{3/2}) = 2(1/\sqrt{m_2} - 1/\sqrt{m_1})$ gives **propeller endurance**:

::::{prf:definition} Breguet endurance equation for a propeller aircraft
:label: def-p52-prop-endurance
:::{math}
:label: eq-p52-prop-E
E = \frac{\eta}{c}\sqrt{\frac{2\rho S}{g}}\frac{C_L^{3/2}}{C_D}\left(\frac{1}{\sqrt{m_2}} - \frac{1}{\sqrt{m_1}}\right)
:::
::::

### Optimal flight conditions for a propeller aircraft

- **Maximum propeller range** maximizes $C_L/C_D$ in [](#eq-p52-prop-R):
  $$
  C_L = \sqrt{\frac{C_{D,0}}{K}}, \qquad C_D = 2 C_{D,0}, \qquad V = V_{T_R,\min}
  $$
- **Maximum propeller endurance** maximizes $C_L^{3/2}/C_D$ in [](#eq-p52-prop-E). That is the minimum-power point from [page 5.1](#eq-p51-min-power):
  $$
  C_L = \sqrt{\frac{3 C_{D,0}}{K}}, \qquad C_D = 4 C_{D,0}, \qquad V = V_{P_R,\min} = {3}^{-1/4}\,V_{T_R,\min} \approx 0.760\,V_{T_R,\min}
  $$

(p52-comparison)=
## Comparing jet and propeller flight conditions

When we put all four optimal conditions side by side, a clean pattern appears ({numref}`fig-p52-aero-ratios`). Each peak lies a factor of $\sqrt{3}$ in $C_L$ from its neighbor. Because $V \propto C_L^{-1/2}$, the three optimal speeds are spaced by a factor of ${3}^{1/4} \approx 1.316$ ({numref}`fig-p52-speed-order`).

:::{figure} figures/p52-aero-ratios.svg
:label: fig-p52-aero-ratios
:alt: Plot of three normalized aerodynamic ratios against lift coefficient C sub L from 0 to 1.45 for the executive jet polar (C sub D 0 equals 0.015, K equals 0.050). The dashed blue curve for C sub L to the one-half over C sub D (jet range) peaks at a blue square at C sub L equals 0.316. The solid black curve for C sub L over C sub D (jet endurance and propeller range) peaks at a black circle at C sub L equals 0.548. The dotted orange curve for C sub L to the three-halves over C sub D (propeller endurance) peaks at an orange diamond at C sub L equals 0.949. Vertical dashed lines drop from each peak to its C sub L value.
:width: 80%

Normalized aerodynamic ratios against $C_L$ for $C_{D,0} = 0.015$, $K = 0.050$. Moving from jet range to propeller endurance raises the optimal $C_L$ by $\sqrt{3}$ at each step ($0.316 \to 0.548 \to 0.949$).
:::

:::{figure} figures/p52-speed-order.svg
:label: fig-p52-speed-order
:alt: Horizontal axis labeled V divided by V sub T R min with three marked points. On the left, an orange square at 0.760 is labeled propeller max endurance (minimum power required). In the center, a black circle at 1.000 is labeled propeller max range and jet max endurance (minimum thrust required and maximum lift-to-drag ratio). On the right, a blue diamond at 1.316 is labeled jet max range (maximum C sub L to the one-half over C sub D). Two dimension arrows below the axis show that each step multiplies the speed by 3 to the one-fourth power.
:width: 80%

Exact ordering of optimal speeds for any aircraft with a parabolic polar. Both range speeds are $31.6\%$ faster than their corresponding endurance speeds, and each jet optimum lies one factor of ${3}^{1/4}$ faster than the matching propeller optimum.
:::

You can also read all four points straight off the thrust-required and power-required curves ({numref}`fig-p52-jet-vs-prop-curves`):

- For a **jet**, look at $T_R(V)$. The bottom of the bucket minimizes $T_R$ (fuel flow per second), giving maximum endurance. Because fuel burned per meter is $(c_t T_R)/V$, the tangent line from the origin minimizes the slope $T_R/V$ and gives maximum range.
- For a **propeller aircraft**, look at $P_R(V)$. The bottom of the bucket minimizes $P_R$ (fuel flow per second), giving maximum endurance. Because fuel burned per meter is $(c P_R/\eta)/V = (c/\eta)T_R$, the tangent line from the origin minimizes the slope $P_R/V$ and gives maximum range.

:::{figure} figures/p52-jet-vs-prop-curves.svg
:label: fig-p52-jet-vs-prop-curves
:alt: Two panels side by side. Panel 1, titled jet: thrust required, shows a solid black U-shaped T sub R curve against airspeed V from 0 to 320 meters per second. Its lowest point is marked with a black dot labeled max endurance (minimum T sub R); a dashed blue straight line from the origin touches the curve tangentially farther right at an open blue square labeled max range (tangent). Panel 2, titled propeller: power required, shows the same geometric pattern on a solid black P sub R curve against V from 0 to 85 meters per second: lowest point marked max endurance (minimum P sub R) and tangent from the origin marked max range (tangent).
:width: 85%

Geometric reading of optimal speeds on $T_R(V)$ for a jet (Panel 1) and $P_R(V)$ for a propeller aircraft (Panel 2). In both panels, the trough gives maximum endurance and the tangent from the origin gives maximum range.
:::

### Why jets cruise high and propellers do not need to

Check where air density $\rho$ appears in the four Breguet equations:

- **Jet range** [](#eq-p52-jet-R) has $1/\sqrt{\rho}$ in front. At higher altitude, lower density forces a higher true airspeed at the same optimal $C_L$ and $T_R$. The jet covers more kilometers for the same thrust and fuel flow per second ({numref}`fig-p52-altitude-range`).
- **Jet endurance** [](#eq-p52-jet-E) has no $\rho$ at all (assuming constant $c_t$), because minimum thrust does not depend on altitude.
- **Propeller range** [](#eq-p52-prop-R) has no $\rho$ at all. Flying higher speeds the aircraft up, which raises $P_R$ by the same factor and leaves kilometers per kilogram of fuel unchanged ({numref}`fig-p52-altitude-range`).
- **Propeller endurance** [](#eq-p52-prop-E) has $\sqrt{\rho}$ in front. Because $P_{R,\min}$ is smallest at sea level, a propeller aircraft stays aloft longest in dense, low-altitude air.

:::{figure} figures/p52-altitude-range.svg
:label: fig-p52-altitude-range
:alt: Plot of maximum range R in kilometers against cruise altitude h from 0 to 12 kilometers. A solid black curve for the executive jet rises from 2,390 kilometers at sea level through a black dot at 9.5 kilometers and 4,000 kilometers to 4,760 kilometers at 12 kilometers, labeled jet: grows as 1 over rho to the one-half. A dashed blue horizontal line from 0 to 7 kilometers at 1,956 kilometers, with an open square at 2.5 kilometers, is labeled Example 3 propeller: 1,956 kilometers (flat with h).
:width: 85%

Effect of cruise altitude on maximum range for the aircraft of worked examples 2 and 3. Jet range climbs steadily as $\rho^{-1/2}$ (capped in practice by engine ceiling and transonic Mach limits), while propeller range is flat with altitude.
:::

:::{table} Summary of Breguet optima for jet and propeller aircraft.
:label: tbl-p52-optima
:align: center

| Case | Maximized ratio | Optimal $C_L$ | Optimal $C_D$ | Speed relative to $V_{T_R,\min}$ | Best altitude (constant SFC) |
| --- | --- | --- | --- | --- | --- |
| Jet range | $C_L^{1/2}/C_D$ | $\sqrt{C_{D,0}/(3K)}$ | $\tfrac{4}{3} C_{D,0}$ | $1.316\,V_{T_R,\min}$ | High altitude ($R \propto \rho^{-1/2}$) |
| Jet endurance | $C_L/C_D$ | $\sqrt{C_{D,0}/K}$ | $2 C_{D,0}$ | $1.000\,V_{T_R,\min}$ | Independent of $\rho$ |
| Propeller range | $C_L/C_D$ | $\sqrt{C_{D,0}/K}$ | $2 C_{D,0}$ | $1.000\,V_{T_R,\min}$ | Independent of $\rho$ |
| Propeller endurance | $C_L^{3/2}/C_D$ | $\sqrt{3 C_{D,0}/K}$ | $4 C_{D,0}$ | $0.760\,V_{T_R,\min}$ | Sea level ($E \propto \rho^{1/2}$) |

:::

(p52-worked-examples)=
## Worked examples

We now work three examples: a business jet in English units, a reverse jet-fuel calculation in SI, and a propeller aircraft in SI.

### Worked example 1: maximum range of a business jet (English units)

A light twin-engine business jet (based on the CJ-1 data in Anderson 2016, Example 6.19) cruises at $h = 22{,}000$ ft ($\rho = 0.038$ lbm/ft³). It has wingspan $b = 53.3$ ft, wing area $S = 318$ ft², gross weight $W_1 = 19{,}817$ lb, fuel capacity $1{,}119$ gal at $6.66$ lb/gal, $C_{D,0} = 0.020$, $e = 0.81$, and $\text{TSFC} = 0.60$ 1/h. Find its maximum range in statute miles.

1. **Fuel weight and final weight:**
   $$
   \begin{aligned}
   W_f &= 1{,}119 \times 6.66\\
       &= 7{,}452.5\ \text{lb}\\
   W_2 &= 19{,}817 - 7{,}452.5\\
       &= 12{,}365\ \text{lb}
   \end{aligned}
   $$
2. **Drag polar and best-range aerodynamic ratio:**
   $$
   \begin{aligned}
   \textit{AR} &= \frac{{53.3}^{2}}{318}\\
               &= 8.934\\
   K &= \frac{1}{\pi \times 0.81 \times 8.934}\\
     &= 0.043986\\
   C_L &= \sqrt{\frac{0.020}{3 \times 0.043986}}\\
       &= 0.3893\\
   C_D &= \frac{4}{3} \times 0.020\\
       &= 0.026667\\
   \frac{\sqrt{C_L}}{C_D} &= \frac{\sqrt{0.3893}}{0.026667}\\
                          &= 23.40
   \end{aligned}
   $$
3. **Convert TSFC to $1/\text{s}$ and evaluate [](#eq-p52-jet-R).** Because $\rho$ is given in lbm/ft³ and an object's mass in lbm is numerically equal to its weight in lb at standard gravity, we use the numerical values of $W_1$ and $W_2$ in lbm with $g = 32.17$ ft/s², so the mass units cancel cleanly inside $\sqrt{2g/(\rho S)}\,(\sqrt{W_1} - \sqrt{W_2})$:
   $$
   \begin{aligned}
   c_t &= \frac{0.60}{3{,}600}\\
       &= 1.667 \times {10}^{-4}\ \text{1/s}\\
   \frac{2}{c_t} &= \frac{2 \times 3{,}600}{0.60}\\
                 &= 12{,}000\ \text{s}\\
   \sqrt{\frac{2g}{\rho S}} &= \sqrt{\frac{2 \times 32.17}{0.038 \times 318}}\\
                            &= 2.307\ \text{ft}/(\text{s}\cdot\text{lbm}^{1/2})\\
   \sqrt{W_1} - \sqrt{W_2} &= 140.77 - 111.20\\
                           &= 29.57\ \text{lbm}^{1/2}\\
   R &= 12{,}000 \times 2.307 \times 23.40 \times 29.57\\
     &= 19{,}155{,}612\ \text{ft}
   \end{aligned}
   $$
4. **Convert feet to statute miles** ($5{,}280$ ft/mi):
   $$
   \begin{aligned}
   R &= \frac{19{,}155{,}612}{5{,}280}\\
     &= 3{,}628\ \text{mi}
   \end{aligned}
   $$
   That is $5{,}839$ km of still-air cruise range (real operational range is shorter once takeoff, climb, descent, and reserves are subtracted).

### Worked example 2: fuel for a jet mission and endurance on that fuel (SI)

The executive twin-jet of [page 5.1](thrust-and-power.md) ($m_1 = 33{,}100$ kg, $S = 88.2$ m², $C_{D,0} = 0.015$, $K = 0.050$) cruises at $h = 9{,}500$ m ($\rho = 0.43863$ kg/m³) with $\text{TSFC} = 0.58$ 1/h. Find: (a) the fuel mass required to fly $R = 4{,}000$ km at maximum-range conditions, and (b) the maximum endurance on that same fuel load.

**(a) Reverse calculation: fuel mass for 4,000 km.**

1. **Best-range aerodynamic factor and $c_t$:**
   $$
   \begin{aligned}
   c_t &= \frac{0.58}{3{,}600}\\
       &= 1.611 \times {10}^{-4}\ \text{1/s}\\
   C_L &= \sqrt{\frac{0.015}{3 \times 0.050}}\\
       &= 0.3162\\
   C_D &= \frac{4}{3} \times 0.015\\
       &= 0.0200\\
   \frac{\sqrt{C_L}}{C_D} &= \frac{\sqrt{0.3162}}{0.0200}\\
                          &= 28.12
   \end{aligned}
   $$
2. **Collect the prefactor $A$ in $R = A(\sqrt{m_1} - \sqrt{m_2})$:**
   $$
   \begin{aligned}
   \sqrt{\frac{2g}{\rho S}} &= \sqrt{\frac{2 \times 9.81}{0.43863 \times 88.2}}\\
                            &= 0.7121\ \text{m}/(\text{s}\cdot\text{kg}^{1/2})\\
   A &= \frac{2}{1.611 \times {10}^{-4}} \times 0.7121 \times 28.12\\
     &= 248{,}594\ \text{m}/\text{kg}^{1/2}
   \end{aligned}
   $$
3. **Solve for $m_2$ and $m_f$:**
   $$
   \begin{aligned}
   \sqrt{m_2} &= \sqrt{m_1} - \frac{R}{A}\\
              &= 181.93 - \frac{4{,}000{,}000}{248{,}594}\\
              &= 165.84\ \text{kg}^{1/2}\\
   m_2 &= {165.84}^{2}\\
       &= 27{,}503\ \text{kg}\\
   m_f &= 33{,}100 - 27{,}503\\
       &= 5{,}597\ \text{kg}
   \end{aligned}
   $$
   At the start of cruise, the best-range airspeed is
   $$
   \begin{aligned}
   V_1 &= \sqrt{\frac{2 \times 33{,}100 \times 9.81}{0.43863 \times 88.2 \times 0.3162}}\\
       &= 230.4\ \text{m/s}
   \end{aligned}
   $$
   which is Mach $0.764$, comfortably subsonic. By the end of the $4{,}000$ km leg, $V_2$ has dropped to $210.0$ m/s and thrust required has fallen from $20.54$ kN to $17.07$ kN ({numref}`fig-p52-weight-burn`).

**(b) Maximum endurance on the same 5,597 kg of fuel.**

At maximum endurance, $C_L = \sqrt{0.015/0.050} = 0.5477$, $C_D = 2 \times 0.015 = 0.030$, and $(L/D)_{\max} = 0.5477/0.030 = 18.26$. Using [](#eq-p52-jet-E):

$$
\begin{aligned}
\ln\frac{m_1}{m_2} &= \ln\frac{33{,}100}{27{,}503}\\
                   &= 0.18524\\
E &= \frac{1}{1.611 \times {10}^{-4}} \times 18.26 \times 0.18524\\
  &= 20{,}996\ \text{s}\\
  &= 5.83\ \text{h}
\end{aligned}
$$

**Check.** Flying 4,000 km at an average speed near 220 m/s takes about $4{,}000{,}000/220/3{,}600 = 5.05$ h. Slowing to the minimum-drag speed extends time aloft from $5.05$ h to $5.83$ h on the same fuel, because the engines burn fuel at the lowest possible rate per second even though the jet covers less distance.

### Worked example 3: range, endurance, and fuel for a propeller aircraft (SI)

The general-aviation propeller aircraft of [page 5.1](thrust-and-power.md) ($m_1 = 1{,}315$ kg, $S = 16.3$ m², $C_{D,0} = 0.026$, $K = 0.054$, $\eta = 0.80$) carries $m_f = 168$ kg of usable fuel and cruises at $h = 2{,}500$ m ($\rho = 0.9567$ kg/m³). Its engine has $\text{PSFC} = 0.076$ g/(s·kW). Find: (a) maximum range, (b) maximum endurance, and (c) the fuel required for a $1{,}000$ km leg.

We first convert PSFC to $1/\text{m}$ and find $m_2$:

$$
\begin{aligned}
c &= 0.076 \times {10}^{-6} \times 9.81\\
  &= 7.456 \times {10}^{-7}\ \text{1/m}\\
\frac{\eta}{c} &= \frac{0.80}{7.456 \times {10}^{-7}}\\
               &= 1{,}072{,}961\ \text{m}\\
m_2 &= 1{,}315 - 168\\
    &= 1{,}147\ \text{kg}
\end{aligned}
$$

**(a) Maximum range**, [](#eq-p52-prop-R), at $C_L = \sqrt{C_{D,0}/K}$:

$$
\begin{aligned}
C_L &= \sqrt{\frac{0.026}{0.054}}\\
    &= 0.6939\\
C_D &= 2 \times 0.026\\
    &= 0.052\\
\frac{C_L}{C_D} &= \frac{0.6939}{0.052}\\
                &= 13.34\\
\ln\frac{m_1}{m_2} &= \ln\frac{1{,}315}{1{,}147}\\
                   &= 0.13669\\
R &= 1{,}072{,}961 \times 13.34 \times 0.13669\\
  &= 1{,}956{,}485\ \text{m}\\
  &= 1{,}956\ \text{km}
\end{aligned}
$$

**(b) Maximum endurance**, [](#eq-p52-prop-E), at $C_L = \sqrt{3 C_{D,0}/K}$:

$$
\begin{aligned}
C_L &= \sqrt{\frac{3 \times 0.026}{0.054}}\\
    &= 1.202\\
C_D &= 4 \times 0.026\\
    &= 0.104\\
\frac{C_L^{3/2}}{C_D} &= \frac{{1.202}^{3/2}}{0.104}\\
                      &= 12.67\\
\sqrt{\frac{2\rho S}{g}} &= \sqrt{\frac{2 \times 0.9567 \times 16.3}{9.81}}\\
                         &= 1.783\ \text{s}\cdot\text{kg}^{1/2}/\text{m}\\
\frac{1}{\sqrt{m_2}} - \frac{1}{\sqrt{m_1}} &= 0.029527 - 0.027576\\
                                            &= 0.001951\ \text{kg}^{-1/2}\\
E &= 1{,}072{,}961 \times 1.783 \times 12.67 \times 0.001951\\
  &= 47{,}290\ \text{s}\\
  &= 13.14\ \text{h}
\end{aligned}
$$

**(c) Fuel required for a 1,000 km leg.** Inverting [](#eq-p52-prop-R) gives $m_2 = m_1\exp[-R c/(\eta\,L/D)]$:

$$
\begin{aligned}
\frac{R c}{\eta (L/D)} &= \frac{1{,}000{,}000 \times 7.456 \times {10}^{-7}}{0.80 \times 13.34}\\
                       &= 0.069865\\
m_2 &= 1{,}315 \times e^{-0.069865}\\
    &= 1{,}226.3\ \text{kg}\\
m_f &= 1{,}315 - 1{,}226.3\\
    &= 88.70\ \text{kg}
\end{aligned}
$$

**Check.** The 1,000 km leg is just over half the full 1,956 km range ($51.1\%$), and it requires $88.70$ kg out of $168$ kg ($52.8\%$) of the fuel. Slightly more than half the fuel is needed for the first half of the trip because the aircraft is heavier during the first half.

## Summary

:::{important} Summary
- Jet fuel flow is proportional to thrust ($c_t$, units $1/\text{s}$), giving $R \propto (\sqrt{C_L}/C_D)\rho^{-1/2}(\sqrt{m_1}-\sqrt{m_2})$ and $E \propto (C_L/C_D)\ln(m_1/m_2)$.
- Propeller fuel flow is proportional to shaft power ($c$, units $1/\text{m}$), giving $R \propto (C_L/C_D)\ln(m_1/m_2)$ and $E \propto (C_L^{3/2}/C_D)\rho^{1/2}(m_2^{-1/2}-m_1^{-1/2})$.
- On $T_R(V)$ for a jet or $P_R(V)$ for a propeller aircraft, the trough gives maximum endurance and the tangent from the origin gives maximum range.
- The optimal speeds form a geometric ladder spaced by ${3}^{1/4} \approx 1.316$: propeller endurance ($0.760\,V_{T_R,\min}$), propeller range and jet endurance ($V_{T_R,\min}$), and jet range ($1.316\,V_{T_R,\min}$).
- Climbing raises jet range as $\rho^{-1/2}$, leaves propeller range and jet endurance unchanged, and lowers propeller endurance as $\rho^{1/2}$.
:::

:::{table} The equations of this page.
:label: tbl-p52-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Jet range | $R = (2/c_t)\sqrt{2g/(\rho S)}(\sqrt{C_L}/C_D)(\sqrt{m_1}-\sqrt{m_2})$ |
| Jet endurance | $E = (1/c_t)(C_L/C_D)\ln(m_1/m_2)$ |
| Jet best-range polar | $C_L = \sqrt{C_{D,0}/(3K)}$, $C_D = \tfrac{4}{3} C_{D,0}$ |
| Jet best-endurance polar | $C_L = \sqrt{C_{D,0}/K}$, $C_D = 2 C_{D,0}$ |
| Propeller range | $R = (\eta/c)(C_L/C_D)\ln(m_1/m_2)$ |
| Propeller endurance | $E = (\eta/c)\sqrt{2\rho S/g}(C_L^{3/2}/C_D)(1/\sqrt{m_2}-1/\sqrt{m_1})$ |
| Propeller best-range polar | $C_L = \sqrt{C_{D,0}/K}$, $C_D = 2 C_{D,0}$ |
| Propeller best-endurance polar | $C_L = \sqrt{3 C_{D,0}/K}$, $C_D = 4 C_{D,0}$ |

:::

:::{exercise} For discussion
:label: ex-p52-discussion

1. Why does a jet fly $31.6\%$ faster for maximum range than for maximum endurance, and why does a propeller aircraft show the same $31.6\%$ ratio between its own best-range and best-endurance speeds?
2. An airliner flies a $4{,}000$ km trip in steady level cruise at constant $C_L$ and constant altitude. Does the first $2{,}000$ km burn more fuel, less fuel, or the same fuel as the second $2{,}000$ km? Explain physically.
3. Why does altitude appear inside the jet range equation but not inside the propeller range equation?
4. Suppose you need an unmanned aircraft to orbit over a wildfire for 24 hours on a fixed fuel budget. Would you pick a jet or a propeller, and should it loiter at low altitude or high altitude?
5. In the Breguet equations, why does increasing wing area $S$ help propeller endurance while hurting jet range (at fixed mass and polar)?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-5-2.html
:label: quiz-5-2
:width: 100%
:enumerated: false

Quiz for Standard 5.2: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 6, Sections 6.13 to 6.15 and Example 6.19 (CJ-1 business jet).
- Anderson, J. D., Jr., *Aircraft Performance and Design*, McGraw-Hill, 1999. Chapter 5, Sections 5.10 and 5.11.
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023. Chapter 11, "Aircraft Performance."
