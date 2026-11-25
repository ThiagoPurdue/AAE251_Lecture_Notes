---
title: "5.4 Engines"
short_title: 5.4 Engines
---

:::{include} ../_parts/standards/5.4.md
:::

In pages 5.1 through 5.3, we treated the propulsion system as a black box that delivered either thrust $T_A$ or power $P_A$ and burned fuel at rate $c_t$ or $c$. Here we open the cowling and look inside. Every air-breathing aircraft engine makes thrust the same way, by accelerating a stream of air backward. Yet different flight speeds and mission lengths call for different internal machinery. Understanding how each stage works and how propulsive efficiency trades exhaust speed against mass flow lets us match the right engine to any mission.

:::{note} What to take from this page
- Every air-breathing engine obeys Newton's second and third laws: $T = (\dot{m}_{\text{air}} + \dot{m}_f)V_e - \dot{m}_{\text{air}} V_\infty + (p_e - p_\infty)A_e$, driven physically by net pressure forces inside the engine.
- A **turbojet** has five main stages in order: inlet (diffuser), compressor, combustor, turbine, and nozzle. The turbine extracts just enough energy to spin the compressor on a shared shaft; the nozzle turns the remaining hot gas into high-speed exhaust.
- Ideal {term}`propulsive efficiency` $\eta_p = 2/(1 + V_e/V_\infty)$ is highest when an engine accelerates a **large** mass of air by a **small** speed increase.
- Engine families span the flight envelope in order: piston and {term}`turboprop` at low subsonic speeds, and high-bypass {term}`turbofan` engines for subsonic airliners (Mach $0.7$ to $0.9$). Supersonic fighters use low-bypass turbofans or {term}`turbojet` engines (often with an {term}`afterburner`), while {term}`ramjet` and {term}`scramjet` engines are used above Mach 2 to 5.
- Selecting an engine means balancing cruise Mach number, fuel burn (SFC), runway length, mission range, noise, weight, and maintenance cost together.
:::

(p54-how-engines-make-thrust)=
## How an air-breathing engine makes thrust

We draw a control volume around an air-breathing engine flying through still air at true airspeed $V_\infty$ ({numref}`fig-p54-jet-control-volume`). Air enters the front at mass flow rate $\dot{m}_{\text{air}}$ and speed $V_\infty$, and fuel enters at rate $\dot{m}_f$ (typically $1\%$ to $2\%$ of $\dot{m}_{\text{air}}$). Hot exhaust then leaves the nozzle exit of area $A_e$ at speed $V_e$ and static pressure $p_e$.

:::{figure} figures/p54-jet-control-volume.svg
:label: fig-p54-jet-control-volume
:alt: Schematic cross section of a turbojet engine enclosed inside a dashed gray rectangle labeled control volume. A blue velocity arrow enters on the left labeled inflow V infinity with static pressure p infinity beneath it. A gray arrow points downward into the combustor labeled fuel flow. A blue velocity arrow leaves on the right labeled exhaust V sub e with p sub e and A sub e beneath it. Above the control volume, a thick black force arrow points left labeled thrust T. A key at top right distinguishes black force arrows from blue velocity arrows.
:width: 85%

Control volume around an air-breathing jet engine. Thrust equals the rate of momentum increase across the engine plus any unbalanced pressure force across the nozzle exit.
:::

Applying conservation of linear momentum to this control volume gives the general **jet thrust equation** (Anderson 2016, Section 9.5):

::::{prf:definition} Air-breathing jet thrust equation
:label: def-p54-thrust
:::{math}
:label: eq-p54-thrust
T = (\dot{m}_{\text{air}} + \dot{m}_f)V_e - \dot{m}_{\text{air}} V_\infty + (p_e - p_\infty)A_e
:::
::::

When the nozzle expands the exhaust all the way down to ambient pressure ($p_e = p_\infty$), the pressure term vanishes and thrust is pure momentum change:

$$
T = (\dot{m}_{\text{air}} + \dot{m}_f)V_e - \dot{m}_{\text{air}} V_\infty \approx \dot{m}_{\text{air}}(V_e - V_\infty)
$$

Look at how the engine physically pushes the aircraft forward. Internal air pressure pushes **forward** on the compressor blades, diffuser walls, and front of the combustion chamber. At the same time, pressure pushes **backward** on the turbine blades and exhaust cone. In a classic Rolls-Royce single-spool turbojet analyzed by Anderson (2016, Figure 9.19), internal pressure forces total $57{,}836$ lb forward and $46{,}678$ lb aft. The difference leaves $11{,}158$ lb of net thrust pushing straight through the engine mounts.

Air-breathing engines also span three orders of magnitude in size. A small Teledyne 305 turbojet used in target drones measures $7.0$ in in diameter, weighs $20$ lb, and makes $90$ lb of thrust. By contrast, a widebody Rolls-Royce Trent 895 high-bypass turbofan measures $110$ in across the fan, weighs $13{,}100$ lb, and delivers $95{,}000$ lb of thrust (Anderson 2016, Section 9.1).

### Propulsive efficiency: large mass flow versus high exhaust speed

The same thrust $T \approx \dot{m}_{\text{air}}(V_e - V_\infty)$ can be made in two ways: accelerate a **small** air flow to high speed, or accelerate a **large** air flow slightly past $V_\infty$. We compare the two by checking how much energy each leaves behind in the exhaust wake.

The useful propulsive power delivered to the airframe is $T V_\infty \approx \dot{m}_{\text{air}}(V_e - V_\infty)V_\infty$, while the kinetic-energy rate added to the airstream is $\tfrac12 \dot{m}_{\text{air}}(V_e^2 - V_\infty^2)$. Taking their ratio, factoring $V_e^2 - V_\infty^2 = (V_e - V_\infty)(V_e + V_\infty)$, and cancelling $\dot{m}_{\text{air}}(V_e - V_\infty)$ gives the ideal **{term}`propulsive efficiency`** (ignoring $\dot{m}_f \ll \dot{m}_{\text{air}}$ and taking $p_e = p_\infty$):

::::{prf:definition} Ideal propulsive efficiency
:label: def-p54-etap
:::{math}
:label: eq-p54-etap
\eta_p = \frac{T V_\infty}{\tfrac12 \dot{m}_{\text{air}}(V_e^2 - V_\infty^2)} = \frac{2}{1 + V_e/V_\infty}
:::
::::

From [](#eq-p54-etap), we can see why subsonic aircraft look the way they do. As $V_e$ approaches $V_\infty$, $\eta_p$ approaches $100\%$ because almost no kinetic energy is wasted in the wake (though $V_e$ must stay slightly above $V_\infty$ to produce thrust). Producing large thrust with a small velocity increase $(V_e - V_\infty)$ requires a large mass flow rate $\dot{m}_{\text{air}}$, which is why subsonic aircraft use wide propellers or wide turbofan fans.

(p54-engine-stages)=
## Stages of a turbojet and the engine families

Now we look at the parts inside the engine that create that pressure and exhaust speed. Every gas-turbine engine shares the same five-station core ({numref}`fig-p54-turbojet-stages`, NASA Glenn Research Center n.d.a). Follow the air from front to back:

1. **Inlet (diffuser).** Slows the incoming air smoothly before it meets the spinning blades, converting part of its kinetic energy into a slight rise in static pressure and temperature.
2. **Compressor.** Alternating rows of rotating rotor blades and fixed stator vanes squeeze the air to pressure ratios of $20$ to $50$. That compression raises static pressure to its peak and heats the air.
3. **Combustor (burner).** Fuel sprays continuously into the compressed air and burns at nearly constant pressure, driving gas temperature to its peak.
4. **Turbine.** Hot, high-pressure gas expands through turbine blades and spins the central shaft that drives the compressor (and, on a turbofan or turboprop, the fan or propeller). Both pressure and temperature drop across the turbine.
5. **Nozzle.** Accelerates the remaining pressurized gas out the back to exhaust speed $V_e$, dropping pressure back toward ambient while converting thermal energy into thrust.

:::{figure} figures/p54-turbojet-stages.svg
:label: fig-p54-turbojet-stages
:alt: Two stacked panels. Top panel shows a cutaway diagram of a five-stage turbojet labeled from left to right: 1 inlet (diffuser), 2 compressor with five vertical blade stages, 3 combustor with flame curves, 4 turbine with two blade stages, and 5 converging nozzle; a central gray shaft runs from the turbine to the compressor, labeled shaft (turbine drives compressor). Bottom panel aligns vertical dashed station boundaries beneath the engine and plots relative pressure p (solid black) and temperature T (dotted orange) from ambient to peak: pressure rises sharply through the compressor, stays nearly flat in the combustor, drops through the turbine, and falls to ambient in the nozzle; temperature rises modestly in the compressor, spikes to its peak at the combustor exit, and drops through the turbine and nozzle while staying well above ambient at the exit.
:width: 85%

Schematic, after NASA Glenn Research Center (n.d.a). The five stages of a turbojet (top) and qualitative paths of static pressure and temperature (bottom): pressure peaks leaving the compressor, temperature peaks leaving the combustor, and the turbine drops both to power the shaft.
:::

Changing how we handle airflow around that core gives the main air-breathing engine families ({numref}`fig-p54-engine-cutaways`):

- **Piston (reciprocating) + propeller.** An internal-combustion engine turns a shaft and propeller. In SI units, thrust is $T = \eta P/V$ (in English units with brake horsepower $\text{bhp}$ and speed in ft/s, $T = 550\,\eta\,\text{bhp}/V$). Piston engines are inexpensive and fuel-efficient at low speed, but limited in power and altitude.
- **{term}`Turboprop` and {term}`turboshaft`.** A gas-turbine core drives extra power-turbine stages connected through a reduction gearbox to a propeller (turboprop) or helicopter rotor (turboshaft). Almost all core energy goes into shaft power. That gives far higher power-to-weight than a piston engine while keeping propeller efficiency up to about Mach $0.55$.
- **{term}`Turbofan`.** A wide ducted fan at the front, driven by the turbine, accelerates cool bypass air around the hot gas-turbine core. We measure that split with the **{term}`bypass ratio`**:
  :::{math}
  :label: eq-p54-bypass
  \beta = \frac{\dot{m}_{\text{bypass}}}{\dot{m}_{\text{core}}}
  :::
  Because bypass air and core air leave at different speeds ($V_{e,\text{bypass}}$ and $V_{e,\text{core}}$), total thrust at matched exit pressure adds both streams:
  $$
  T = \dot{m}_{\text{bypass}}(V_{e,\text{bypass}} - V_\infty) + (\dot{m}_{\text{core}} + \dot{m}_f)V_{e,\text{core}} - \dot{m}_{\text{core}}V_\infty
  $$
  - **High-bypass turbofans** ($\beta \approx 5$ to $12$) get $75\%$ to $90\%$ of their thrust from the cool fan stream. Lower exhaust speed raises $\eta_p$, lowers fuel burn, and reduces jet noise. That is why high-bypass turbofans power airliners and business jets.
  - **Low-bypass turbofans** ($\beta \approx 0.3$ to $1.5$) keep a slender frontal area for low supersonic wave drag. They also burn less fuel in subsonic cruise than a pure turbojet, making them standard on modern supersonic fighters.
- **Turbojet and {term}`afterburner`.** Pure core flow has zero bypass ($\beta = 0$). High exhaust speed makes a turbojet loud and inefficient at low speed, yet compact and effective at high supersonic Mach numbers. Adding an **afterburner** injects extra fuel into the oxygen-rich exhaust downstream of the turbine. That roughly doubles thrust for brief takeoff or supersonic combat bursts, while roughly doubling specific fuel consumption.
- **{term}`Ramjet` and {term}`scramjet`.** Above roughly Mach $2$, slowing the oncoming supersonic flow through shock waves in a contoured inlet compresses the air on its own. That removes the heavy rotating compressor and turbine. A **ramjet** slows flow to subsonic speed in the combustor and works well from Mach $2$ to Mach $5$, though it makes zero static thrust and needs a rocket or jet booster to accelerate. Above Mach $5$, slowing air to subsonic speed creates extreme temperatures that break down gas molecules and melt walls. A **scramjet** (supersonic combustion ramjet) instead burns fuel directly in supersonic flow.

:::{figure} figures/p54-engine-cutaways.svg
:label: fig-p54-engine-cutaways
:alt: Three stacked cutaway schematics. Panel 1, high-bypass turbofan: a wide outer fan and shaded bypass duct surround a slender gas-turbine core (compressor, combustor, turbine, core nozzle), captioned most thrust comes from the bypass air. Panel 2, turboprop: a front propeller connects through a hatched reduction gearbox and long shaft to the gas-turbine core and three-stage power turbine, captioned turbine drives the propeller through the shaft and gearbox. Panel 3, ramjet (no compressor or turbine): a sharp supersonic inlet spike compresses flow into fuel injectors, flameholders, a combustor, and a converging-diverging nozzle, captioned ram compression from high flight speed (Mach greater than 2).
:width: 60%

Cutaways of three air-breathing engine architectures beyond the pure turbojet: high-bypass turbofan (1), turboprop (2), and ramjet (3). Each adapts how air is compressed and accelerated to match a different speed regime.
:::

(p54-matching-mission)=
## Matching an engine to a mission

Now we connect propulsive efficiency and fuel burn directly to choosing an engine. Two charts show where each engine family performs best: propulsive efficiency against Mach number ({numref}`fig-p54-propulsive-efficiency`) and thrust specific fuel consumption against Mach number ({numref}`fig-p54-sfc-vs-mach`).

:::{figure} figures/p54-propulsive-efficiency.svg
:label: fig-p54-propulsive-efficiency
:alt: Plot of propulsive efficiency eta sub p in percent against flight Mach number from 0 to 1.0. A solid black curve for piston and turboprop rises quickly to a peak near 83 percent around Mach 0.48, then drops steeply past a vertical dashed gray line at Mach 0.55 labeled tip compressibility limits propellers. A dashed blue curve for high-bypass turbofan climbs steadily across the plot to about 64 percent at Mach 1.0, crossing above the propeller curve near Mach 0.75. A dotted orange curve for turbojet rises below the turbofan curve, reaching about 55 percent at Mach 1.0.
:width: 80%

Representative curves, after Anderson (2016), Chapter 9. Propellers have the highest propulsive efficiency below Mach $0.55$, before sonic shocks on the blade tips cause their efficiency to drop steeply; high-bypass turbofans are the most efficient choice in high-subsonic cruise.
:::

:::{figure} figures/p54-sfc-vs-mach.svg
:label: fig-p54-sfc-vs-mach
:alt: Plot of thrust specific fuel consumption in 1 per hour against flight Mach number from 0 to 1.0. A solid black curve for piston and turboprop lies lowest (0.16 to 0.26) up to Mach 0.45, then climbs steeply above Mach 0.55 as propeller efficiency collapses. A dashed blue line for high-bypass turbofan slopes gently from 0.38 to 0.60 across the plot. A dash-dot gray line for low-bypass turbofan lies higher from 0.56 to 0.81. A dotted orange line for turbojet lies highest from 0.95 to 1.25.
:width: 80%

Representative curves, after Anderson (2016), Chapter 9 (lower TSFC is better). Turboprops burn the least fuel per unit thrust below Mach $0.5$, while high-bypass turbofans have the lowest fuel burn in high-subsonic airliner cruise.
:::

Look at the crossover around Mach $0.55$ in both plots. Below Mach $0.5$, a propeller accelerates a wide disk of air by a small amount, giving $\eta_p$ above $80\%$ and the lowest equivalent TSFC of any air-breathing engine. Above Mach $0.55$, forward speed plus blade rotation pushes the propeller tips close to Mach 1. Shock waves form on the tips, drag surges, and propeller efficiency drops sharply. High-bypass turbofans enclose their fan inside a cowling (inlet diffuser) that slows the oncoming air slightly before it reaches the blades. That lets airliners cruise cleanly at Mach $0.75$ to $0.88$ with TSFC near $0.5$ to $0.6$ 1/h.

Extending the view to supersonic and hypersonic speeds gives the mission map in {numref}`fig-p54-engine-map`, and {numref}`tbl-p54-engine-comparison` compares the six main families side by side.

:::{figure} figures/p54-engine-map.svg
:label: fig-p54-engine-map
:alt: Chart mapping mission range (short, medium, long on the vertical axis) against cruise Mach number from 0 to 6 on the horizontal axis, with a vertical dashed line at Mach 1. Below Mach 1, tall boxes appear left to right for piston (Mach 0.05 to 0.3, short range), turboprop (Mach 0.2 to 0.58, medium range), and high-bypass turbofan (Mach 0.7 to 0.95, medium to long range, shaded light beige). Above Mach 1 appear boxes for low-bypass turbofan (Mach 1.1 to 2.2, medium range), turbojet with afterburner (Mach 1.2 to 2.8, short range), ramjet (Mach 2.5 to 4.4, medium range), and scramjet (Mach 4.6 to 5.9, medium range).
:width: 85%

Representative operating envelopes, after Mattingly (2006), Chapter 1. Each engine family occupies a distinct cruise Mach band where its compression method and exhaust velocity keep efficiency high.
:::

:::{table} Comparison of the six main air-breathing propulsion families (Anderson 2016, Chapter 9; Mattingly 2006, Chapter 1).
:label: tbl-p54-engine-comparison
:align: center

<table>
<tr><th>Engine type</th><th>Typical Mach range</th><th>Relative TSFC</th><th>Strengths</th><th>Main limits</th></tr>
<tr><th scope="row">Piston + propeller</th><td class="num">0 to 0.3</td><td>Lowest at low speed</td><td>Low purchase cost, simple maintenance, strong low-speed efficiency</td><td>Low power-to-weight, drops off with altitude, speed-limited</td></tr>
<tr><th scope="row">Turboprop</th><td class="num">0.2 to 0.55</td><td>Lowest below Mach 0.5</td><td>High takeoff thrust for short runways, lighter than piston at high power</td><td>Propeller tip compressibility caps cruise near Mach 0.55; cabin noise</td></tr>
<tr><th scope="row">High-bypass turbofan</th><td class="num">0.65 to 0.9</td><td>Low (0.45 to 0.65 1/h)</td><td>Best long-range subsonic fuel economy, quietest jet, high cruise altitude</td><td>Large frontal area creates heavy drag near and above Mach 1</td></tr>
<tr><th scope="row">Low-bypass turbofan</th><td class="num">0.8 to 2.2</td><td>Moderate (0.65 to 0.85 1/h)</td><td>Slender profile for supersonic flight, good subsonic cruise, accepts afterburner</td><td>Higher fuel burn and noise than high-bypass turbofan</td></tr>
<tr><th scope="row">Turbojet (with afterburner)</th><td class="num">1.0 to 3.0</td><td>High (0.95 to 2.0 1/h)</td><td>Small cross section, high specific thrust at supersonic speeds</td><td>Poor subsonic propulsive efficiency, high fuel burn, loud exhaust</td></tr>
<tr><th scope="row">Ramjet / scramjet</th><td class="num">2.5 to 6+</td><td>High, viable at high Mach</td><td>No rotating compressor or turbine; handles extreme stagnation temperatures</td><td>Zero static thrust (requires booster to reach operating Mach number)</td></tr>
</table>

:::

(p54-worked-examples)=
## Worked examples

We now apply these ideas twice: first to compare two engines at the same thrust, then to pick an engine for a regional airline.

### Worked example 1: turbojet versus high-bypass turbofan at the same thrust

Two engines fly at $V_\infty = 220$ m/s with matched exit pressure ($p_e = p_\infty$) and burn fuel at $\dot{m}_f = 1.2$ kg/s:

- **Engine A (turbojet):** $\dot{m}_{\text{air}} = 60.0$ kg/s, exhaust speed $V_e = 870$ m/s.
- **Engine B (high-bypass turbofan):** total $\dot{m}_{\text{air}} = 280.0$ kg/s, effective average exhaust speed $V_e = 361.5$ m/s.

We find the thrust and ideal propulsive efficiency of each engine and compare them.

1. **Engine A (turbojet)**, [](#eq-p54-thrust) and [](#eq-p54-etap):
   $$
   \begin{aligned}
   T_A &= (60.0 + 1.2) \times 870 - 60.0 \times 220\\
       &= 40{,}044\ \text{N}\\
       &= 40.04\ \text{kN}\\
   \eta_{p,A} &= \frac{2}{1 + 870/220}\\
              &= 0.404
   \end{aligned}
   $$
2. **Engine B (high-bypass turbofan):**
   $$
   \begin{aligned}
   T_B &= (280.0 + 1.2) \times 361.5 - 280.0 \times 220\\
       &= 40{,}054\ \text{N}\\
       &= 40.05\ \text{kN}\\
   \eta_{p,B} &= \frac{2}{1 + 361.5/220}\\
              &= 0.757
   \end{aligned}
   $$

**Comparison.** Both engines produce almost the same thrust ($40.04$ kN versus $40.05$ kN), yet the turbofan reaches $75.7\%$ propulsive efficiency while the turbojet reaches only $40.4\%$. The turbofan moves $4.7$ times as much air mass through a gentle speed jump ($+141.5$ m/s instead of $+650$ m/s). That leaves far less wasted kinetic energy in the wake and keeps exhaust noise much lower.

### Worked example 2: choosing an engine for an inter-island commuter aircraft

A regional airline needs a $30$-seat commuter and mail aircraft to fly $6$ legs per day. Each leg lasts $1.5$ h at cruise Mach $0.42$, out of coastal island airfields with $900$ m runways. We evaluate three candidates: twin piston engines, twin turboprops, and twin high-bypass turbofans.

1. **Eliminate piston engines.** A $30$-seat commuter at Mach $0.42$ needs roughly $1{,}000$ to $1{,}500$ kW per engine. That lies well above the practical power-to-weight range of modern aircraft piston engines, and pistons bring heavier vibration and maintenance loads on airline schedules.
2. **Compare twin turboprop versus twin high-bypass turbofan** using representative numbers for this class at Mach $0.42$:
   - **Cruise speed match:** Mach $0.42$ lies right in the peak propulsive-efficiency range of a propeller ({numref}`fig-p54-propulsive-efficiency`), well below the Mach $0.55$ tip-compressibility limit.
   - **Fuel burn:** The twin turboprop burns $260$ kg/h versus $430$ kg/h for the twin turbofan, a saving of $170$ kg/h. Across $6 \times 1.5 = 9$ flight hours per day, that saves $170 \times 9 = 1{,}530$ kg of fuel every day.
   - **Runway performance and engine weight:** Propeller thrust $T_A = P_A/V$ is highest at low speed, so the turboprop accelerates briskly off $900$ m runways and can use reverse blade pitch on landing. Each turboprop also weighs half as much as the turbofan ($410$ kg versus $820$ kg per engine).
   - **Noise:** Community takeoff noise is lower for the turboprop ($82$ dBA versus $86$ dBA), though cabin propeller tone needs acoustic insulation.

**Recommendation.** We choose the **twin turboprop**. At Mach $0.42$ on short $900$ m runways, it reduces daily fuel burn by $1{,}530$ kg, saves $820$ kg of engine weight across both engines, and provides stronger low-speed takeoff thrust. When you choose an engine for a real mission, you check speed, fuel burn, runway length, and weight together. A high-bypass turbofan would become the better choice only if the airline raised its cruise speed past Mach $0.65$ on longer routes with longer runways.

## Summary

:::{important} Summary
- Air-breathing thrust follows $T = (\dot{m}_{\text{air}} + \dot{m}_f)V_e - \dot{m}_{\text{air}} V_\infty + (p_e - p_\infty)A_e$, transmitted physically through internal pressure forces on the engine parts.
- A turbojet passes air through five stages: inlet, compressor (pressure peaks), combustor (temperature peaks), turbine (drives the compressor shaft), and nozzle (accelerates exhaust).
- Ideal propulsive efficiency $\eta_p = 2/(1 + V_e/V_\infty)$ shows why giving a large air mass a small speed increase is more efficient than accelerating a small air mass to high exhaust speed.
- Piston and turboprop engines are most efficient below Mach $0.55$, and high-bypass turbofans are best suited from Mach $0.65$ to $0.9$. Low-bypass turbofans and afterburning turbojets cover Mach $1$ to $3$, while ramjets and scramjets operate from Mach $2.5$ upward without rotating compressors or turbines.
:::

:::{table} The equations of this page.
:label: tbl-p54-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Air-breathing jet thrust | $T = (\dot{m}_{\text{air}} + \dot{m}_f)V_e - \dot{m}_{\text{air}} V_\infty + (p_e - p_\infty)A_e$ |
| Ideal propulsive efficiency | $\eta_p = 2/(1 + V_e/V_\infty)$ |
| Bypass ratio | $\beta = \dot{m}_{\text{bypass}}/\dot{m}_{\text{core}}$ |
| Propeller thrust from shaft power | $T = \eta P / V$ (SI); $T = 550\,\eta\,\text{bhp}/V$ (English, $V$ in ft/s) |

:::

:::{exercise} For discussion
:label: ex-p54-discussion

1. Why does static pressure peak at the exit of the compressor while static temperature peaks at the exit of the combustor?
2. If you want higher propulsive efficiency $\eta_p$ at a given cruise speed $V_\infty$, should you raise or lower the exhaust velocity $V_e$, and what must happen to the air mass flow rate $\dot{m}_{\text{air}}$ to keep thrust constant?
3. Why does a supersonic fighter use a low-bypass turbofan instead of the high-bypass turbofan found on a commercial airliner?
4. Why can a ramjet not take off from a runway under its own power?
5. Suppose the commuter airline of worked example 2 replaces its short island hops with $1{,}800$ km mainland routes out of $2{,}500$ m runways and wants to cruise at Mach $0.78$. Which engine family is the better choice now, and why?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-5-4.html
:label: quiz-5-4
:width: 100%
:enumerated: false

Quiz for Standard 5.4: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 9, "Propulsion" (Sections 9.1 to 9.10 and Figure 9.19).
- Mattingly, J. D., *Elements of Propulsion: Gas Turbines and Rockets*, AIAA Education Series, 2006. Chapter 1, "Introduction to Propulsion."
- NASA Glenn Research Center, "[Turbojet Engine](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/turbojet-engine/)," Beginner's Guide to Aeronautics, n.d.a.
- NASA Glenn Research Center, "[General Thrust Equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/general-thrust-equation/)," Beginner's Guide to Aeronautics, n.d.b.
