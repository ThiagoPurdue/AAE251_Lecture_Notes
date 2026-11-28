---
title: "5.4 Engines"
short_title: 5.4 Engines
---

:::{include} ../_parts/standards/5.4.md
:::

On pages 5.1 to 5.3, we treated the propulsion system as a black box defined by its available thrust or power, its altitude lapse, and its specific fuel consumption ($c_t$ or $c$). Here we open up the engine to see how those characteristics arise. Every air-breathing engine produces thrust by accelerating incoming air to a higher exhaust velocity. The trade-off between moving a large mass flow slowly or a small mass flow quickly drives propulsive efficiency and guides the choice of engine type for a given mission.

:::{note} What to take from this page
- An engine that breathes air makes thrust by speeding up the air it takes in, [](#eq-p54-thrust). With no air coming in, the same equation is the rocket thrust of Chapter 4.
- The propulsive efficiency $\eta_p = 2/(1 + V_e/V_\infty)$ is high when the engine speeds up a large flow of air a little, and low when it speeds up a small flow a lot.
- A turbojet has five stages in flow order: inlet, compressor, combustor, turbine, nozzle. The turbine takes from the hot gas only the work the compressor needs; what is left becomes exhaust speed.
- Turbofans, turboprops, turboshafts, and afterburners use the same core in different ways. To choose among them, start from the speed that dominates the mission, then check size, fuel, cost, and acceptance.
:::

(p54-how-engines-make-thrust)=
## Thrust from an engine that breathes air

Before we compare engines, we need one equation that applies to all of them. Page 4.1 derived it, the [air-breathing thrust equation](#eq-p41-air), by applying the control volume of a rocket to [an engine that breathes air](#p41-air-breathing). Chapter 4 wrote thrust as $F$; we write $T$, as on [page 5.1](#eq-p51-TA). The inflow speed $V_\infty$ is the flight speed $V$ of pages 5.1 to 5.3.

Page 4.1 left out the fuel. We now keep it. Air enters at the {term}`mass flow rate` $\dot m_\text{air}$ and the flight speed $V_\infty$. Fuel comes from the tanks at $\dot m_f$, already moving with the aircraft, so it brings no momentum along the axis relative to the engine. Both leave through the nozzle at the exit velocity $V_e$, at a pressure $p_e$ over the exit area $A_e$. The momentum balance gives:

::::{prf:definition} Thrust of an engine that breathes air
:label: def-p54-thrust
:::{math}
:label: eq-p54-thrust
\begin{aligned}
T &= (\dot m_\text{air} + \dot m_f)V_e\\
&\;\;\; - \dot m_\text{air}V_\infty\\
&\;\;\; + (p_e - p_\infty)A_e
\end{aligned}
:::
::::

The first term is the momentum that leaves each second. The second is the momentum the air already had when it came in, often called the ram drag. The third is the pressure thrust of page 4.1.

We often simplify it twice. First, the fuel is a small part of the flow. At most about 1 kg of fuel can burn in every 15 kg of air, and engines run leaner than that (Leishman 2022, Chapter 40). Second, a nozzle that expands the gas to the outside pressure, $p_e = p_\infty$, has no pressure term. Then

:::{math}
:label: eq-p54-thrust-simple
T \approx \dot m_\text{air}(V_e - V_\infty)
:::

Thrust depends only on how much air the engine moves and how much speed it adds.

Now we set $\dot m_\text{air} = 0$ in [](#eq-p54-thrust). Nothing comes in from outside, everything that leaves was carried on board, and the equation becomes $T = \dot m V_e + (p_e - p_\infty)A_e$, the [rocket thrust equation of page 4.1](#eq-p41-thrust). One momentum balance covers both kinds of engine. The difference is where the mass comes from.

The fuel flow $\dot m_f$ is what the fuel laws of [page 5.2](#p52-fuel-consumption) measure. There, the thrust specific fuel consumption is $c_t = \dot m_f g/T$, and a lower $c_t$ means a longer range.

(p54-propulsive-efficiency)=
## Large air flow or fast exhaust

[](#eq-p54-thrust-simple) shows that two different engines can give the same thrust. One moves a small flow of air and throws it out fast. The other moves a large flow and adds only a little speed. To see which one wastes less fuel, we follow the energy.

Watch the air from the ground. Before the aircraft arrives, the air is still. After the engine has passed, that air moves backward at $V_e - V_\infty$, and nothing gives its energy back. The engine also does useful work by pushing the aircraft with the force $T$ at the speed $V_\infty$, which is the power $TV_\infty$ of [page 5.1](#eq-p51-TA). The **{term}`propulsive efficiency`** is the useful power over all the power the engine gives to the air. We neglect the fuel flow and take $p_e = p_\infty$, so $T = \dot m(V_e - V_\infty)$, writing $\dot m$ for $\dot m_\text{air}$.

1. **Useful power.** We multiply the thrust by the flight speed:

   $$
   T V_\infty = \dot m (V_e - V_\infty)V_\infty
   $$
2. **Power left in the wake.** Each second, the mass $\dot m$ is left moving at $V_e - V_\infty$, so it carries away the kinetic energy

   $$
   \frac{1}{2}\dot m (V_e - V_\infty)^2
   $$
3. **The ratio** of the useful power to the sum of the two:

   $$
   \eta_p = \frac{T V_\infty}{T V_\infty + \frac{1}{2}\dot m (V_e - V_\infty)^2}
   $$
4. **Put in** $T = \dot m (V_e - V_\infty)$ from step 1. Every term then contains the factor $\dot m (V_e - V_\infty)$, and we cancel it from the top and from both terms of the bottom:

   $$
   \eta_p = \frac{V_\infty}{V_\infty + \frac{1}{2}(V_e - V_\infty)}
   $$
5. **Multiply** top and bottom by 2 and collect the terms:

   $$
   \eta_p = \frac{2V_\infty}{V_\infty + V_e}
   $$
6. **Divide** top and bottom by $V_\infty$:

::::{prf:definition} Propulsive efficiency
:label: def-p54-etap
:::{math}
:label: eq-p54-etap
\eta_p = \frac{2}{1 + V_e/V_\infty}
:::
::::

{numref}`fig-p54-propulsive-efficiency` plots [](#eq-p54-etap). The equation assumes one exhaust speed and gives an ideal value. It counts only the energy left in the wake, not how well the engine turns fuel into gas energy. The two together set the fuel burned per unit thrust (Leishman 2022, Chapter 40).

:::{figure} figures/p54-propulsive-efficiency.svg
:label: fig-p54-propulsive-efficiency
:alt: A solid curve of propulsive efficiency, from 0 to 1, against the exhaust speed over the flight speed, from 1 to 6. It starts at 1 at a ratio of 1, marked by an open circle labeled no thrust when V e equals V infinity, and falls steadily to about 0.29 at 6. Two filled points sit on the curve with dashed drop lines: engine 2, 228 kilograms per second, V e 380.0 meters per second and efficiency 0.7541, at a ratio of about 1.65; engine 1, 40 kilograms per second, V e 1,085 meters per second and efficiency 0.3498, at about 4.72. A note says both engines make 34.2 kilonewtons at 230 meters per second.
:width: 85%

Computed from [](#eq-p54-etap) for worked example 1. Producing the same thrust at the same speed takes less energy when the engine speeds up a large air flow a little. Engine 2 moves 5.70 times as much air as engine 1 and is more than twice as efficient. An exhaust no faster than the flight would be perfectly efficient and give no thrust.
:::

:::{warning} High efficiency is not high thrust
If you push $V_e$ down toward $V_\infty$ to raise $\eta_p$, you also push the thrust $\dot m(V_e - V_\infty)$ toward zero. The only way to keep the thrust is a larger $\dot m$, which needs a larger fan or propeller.
:::

### Worked example 1: one thrust, two air flows

Two engines each give 34.2 kN at a flight speed of 230 m/s. Engine 1 moves 40.0 kg/s of air and engine 2 moves 228 kg/s. We neglect the fuel and take $p_e = p_\infty$. Find each exhaust speed, each propulsive efficiency, and the power each leaves in the wake.

1. **Exhaust speed**, from $T = \dot m(V_e - V_\infty)$, so $V_e = V_\infty + T/\dot m$. For engine 1:

   $$
   \begin{aligned}
   V_e &= 230 + \frac{34{,}200}{40.0}\\
   &= 230 + 855.0\\
   &= 1{,}085\ \text{m/s}
   \end{aligned}
   $$

   For engine 2:

   $$
   \begin{aligned}
   V_e &= 230 + \frac{34{,}200}{228}\\
   &= 230 + 150.0\\
   &= 380.0\ \text{m/s}
   \end{aligned}
   $$
2. **Propulsive efficiency**, [](#eq-p54-etap):

   $$
   \begin{aligned}
   \eta_{p,1} &= \frac{2}{1 + 1{,}085/230}\\
   &= 0.3498\\
   \eta_{p,2} &= \frac{2}{1 + 380.0/230}\\
   &= 0.7541
   \end{aligned}
   $$
3. **Power.** Both engines do the same useful work:

   $$
   \begin{aligned}
   T V_\infty &= 34{,}200 \times 230\\
   &= 7{,}866{,}000\ \text{W}
   \end{aligned}
   $$

   That is 7.866 MW. The power left in the wake, $\frac{1}{2}\dot m (V_e - V_\infty)^2$, is not the same at all. For engine 1:

   $$
   \begin{aligned}
   &\frac{1}{2} \times 40.0 \times {855.0}^{2}\\
   &\;\;\;= 14{,}620{,}500\ \text{W}
   \end{aligned}
   $$

   For engine 2:

   $$
   \begin{aligned}
   &\frac{1}{2} \times 228 \times {150.0}^{2}\\
   &\;\;\;= 2{,}565{,}000\ \text{W}
   \end{aligned}
   $$

   That is 14.62 MW for engine 1 and 2.565 MW for engine 2.

**Check.** The efficiency is the useful power over the total: $7.866/(7.866 + 14.62) = 0.3498$ for engine 1 and $7.866/(7.866 + 2.565) = 0.7541$ for engine 2, as in step 2.

Engine 2 moves 5.70 times as much air, speeds it up by 150.0 m/s instead of 855.0 m/s, and wastes only 2.565 MW. This is why airliners carry large fans and slower aircraft carry propellers.

(p54-engine-stages)=
## Inside a turbojet

To choose an engine we need to see inside the box, because every family on this page is built from the same parts. The simplest is the **{term}`turbojet`**. {numref}`fig-p54-turbojet-stages` shows one in section. The air passes five stages in order (Leishman 2022, Chapter 46):

1. **Inlet.** It slows the incoming air and delivers a smooth flow to the compressor. The air must reach the compressor below the speed of sound, even when the aircraft flies faster, so a supersonic inlet slows the air through shocks first. The inlet is also called the intake.
2. **{term}`Compressor`.** Rows of rotating blades, the rotors, alternate with rows of fixed vanes, the stators. Each pair is one compressor stage, and each raises the pressure a little. The compressor in the figure has 8 of them (FAA 2008). Squeezing the air also heats it.
3. **{term}`Combustor`.** Fuel is sprayed into the compressed air and burns continuously, at nearly constant pressure. The temperature reaches its highest value here. The combustor is also called the burner or the combustion chamber.
4. **{term}`Turbine`.** The hot gas expands through rows of turbine blades, which turn the shaft that drives the compressor. The turbine takes only the work the compressor and the engine accessories need.
5. **Nozzle.** The nozzle turns what the turbine left in the gas, its pressure and temperature above those of the outside air, into exhaust speed $V_e$.

:::{figure} figures/p54-turbojet-stages.svg
:label: fig-p54-turbojet-stages
:alt: Top, a single-spool turbojet in section along a dash-dot centerline, air entering at the left: open inlet, an 8-stage compressor, an annular combustor liner, a 2-stage turbine, a tail cone, and a converging nozzle, with one shaft from the turbine to the compressor. Numbers 1 to 5 name the five stages; one rotor row and one stator row are named below. Under the drawing, two plots against position along the engine, numbered the same. Pressure is flat at the ambient 101.3 kilopascals through the inlet, rises to 709.3 through the compressor, holds through the combustor, and falls to 344.6 through the turbine and to ambient through the nozzle. Temperature rises 214.3 kelvin inside the compressor, climbs to 1,150 through the combustor, and drops 214.3 kelvin inside the turbine.
:width: 95%

Schematic of a single-spool turbojet in section, with the pressure and temperature along it. Pressure rises through the compressor, stays constant through the combustor, and falls through the turbine and nozzle. The turbine takes back the same 214.3 K the compressor added and still leaves pressure for the nozzle. Proportions after the General Electric CJ610 (FAA 2008: 8 compressor stages, 2 turbine stages, length, and largest diameter); the plots are computed for an ideal turbojet standing still at sea level, with an assumed compressor pressure ratio of 7 and 1,150 K at the turbine entry.
:::

We computed the curves of {numref}`fig-p54-turbojet-stages` with the relations of a thermodynamics course. The compressor raises the pressure from 101.3 to 709.3 kPa, and the temperature by 214.3 K. The combustor heats the gas to 1,150 K at constant pressure. The turbine must give the compressor back the same work. For a gas, the work per kilogram goes with the change of temperature, so the turbine lowers the temperature by the same 214.3 K.

This is the idea that makes the engine work. The turbine works on gas that is much hotter than the air the compressor squeezed, and hot gas gives up the same work with a much smaller pressure drop. The compressor needed a pressure ratio of 7. The turbine needs only $709.3/344.6 = 2.058$. The gas leaves the turbine at 344.6 kPa, more than three times the outside pressure, and the nozzle turns that excess into speed. Burning fuel between the compressor and the turbine is what leaves this excess.

Larger engines split the compressor into a low-pressure and a high-pressure part, each turned by its own turbine on its own shaft, one shaft inside the other. Each shaft with its compressor and turbine is a **{term}`spool`**, and two spools let each compressor turn at the speed that suits it (Leishman 2022, Chapter 47).

The turbine blades limit how hot the gas can be. They spin in the hottest gas of the engine, so they are made of high-temperature alloys and cooled with air bled from the compressor (Leishman 2022, Chapter 46).

(p54-thrust-buildup)=
### Where the thrust acts on the engine

[](#eq-p54-thrust) gives the net thrust from what enters and leaves, without looking inside. The parts inside experience something else. The gas pushes on every blade, vane, wall, and cone, and the loads on the parts are much larger than the thrust. Anderson (2016, Chapter 9) reproduces them from Rolls-Royce for a typical single-spool turbojet. {numref}`fig-p54-thrust-distribution` adds them up from the front.

- **Forward loads.** The compressor carries 19,049 lb, because the pressure rises toward its rear. The compressor-exit diffuser, which slows the air before the combustor, carries 2,186 lb. The combustion chamber carries 34,182 lb, and the exhaust unit and jet pipe 2,419 lb. In all, $19{,}049 + 2{,}186 + 34{,}182 + 2{,}419 = 57{,}836$ lb.
- **Rearward loads.** The turbine carries 41,091 lb, because the pressure falls through it, and the propelling nozzle 5,587 lb. In all, $41{,}091 + 5{,}587 = 46{,}678$ lb.
- **Net thrust.** The difference, $57{,}836 - 46{,}678 = 11{,}158$ lb, is what the mounts pass to the aircraft. That is 49.63 kN, only 19.3% of the 257.3 kN of forward load.

:::{figure} figures/p54-thrust-distribution.svg
:label: fig-p54-thrust-distribution
:alt: A waterfall chart of the forward load added up from the front of a jet engine, in thousands of pounds, with one bar per part in flow order. Plain gray bars for forward loads: compressor plus 19,049, diffuser plus 2,186, combustion chamber plus 34,182, bringing the total to about 55,400 pounds. A hatched bar for the turbine, minus 41,091, brings it down to about 14,300. A gray bar for the exhaust unit and jet pipe, plus 2,419, and a hatched bar for the propelling nozzle, minus 5,587, end at the black thrust bar of 11,158 pounds. A key names plain gray bars as forward loads and hatched bars as rearward loads.
:width: 85%

Values from the Rolls-Royce figure reproduced in Anderson (2016), Chapter 9, for a typical single-spool turbojet. The thrust is the small difference between large forward loads on the compressor and combustion chamber and a large rearward load on the turbine, with the running total climbing to five times the thrust before the turbine takes most of it back.
:::

So the parts are built for loads several times the thrust, while the mounts carry only the difference.

(p54-engine-families)=
## The engine families

At subsonic speed the turbojet is inefficient, because all its thrust comes from one fast, hot jet ({numref}`fig-p54-propulsive-efficiency`). The other families keep the same core and change what is done with its energy.

(p54-turbofan)=
### Turbofan

A **{term}`turbofan`** puts a large fan in front of the core and drives it with an extra turbine at the rear, on its own shaft ({numref}`fig-p54-turbofan`). The fan splits the incoming air into two streams. The core stream goes through the compressor, combustor, and turbines, as in a turbojet. The bypass stream goes only through the fan, then around the core through the bypass duct, and leaves through its own nozzle (Leishman 2022, Chapter 47). The **{term}`bypass ratio`** compares the two:

:::{math}
:label: eq-p54-bypass
\beta = \frac{\dot m_\text{bypass}}{\dot m_\text{core}}
:::

:::{figure} figures/p54-turbofan.svg
:label: fig-p54-turbofan
:alt: Two drawings of a two-spool high-bypass turbofan. Top, the whole engine in section along a dash-dot centerline: a wide fan inside the nacelle, guide vanes across the bypass duct, and the core. An arrow behind the nacelle is labeled bypass stream, cooler and slower, m dot bypass at V e bypass; one behind the core is labeled core stream, hotter and faster, m dot core at V e core. Below, the upper half of the core drawn 2.6 times larger: a 3-stage low-pressure compressor, a 9-stage high-pressure compressor, an annular combustor liner, a 1-stage high-pressure turbine, and a 4-stage low-pressure turbine. An inner shaft joins the fan to the low-pressure turbine, inside a hollow shaft from the high-pressure compressor to the high-pressure turbine. A key names the parts.
:width: 90%

Schematic of a two-spool high-bypass turbofan in section, with the upper half of its core enlarged below. Most of the air goes around the core, and each stream leaves at its own speed, with the bypass stream cooler and slower and the core stream hotter and faster. The low-pressure turbine at the rear turns the fan through the inner shaft. Proportions after the CFM56-7B (EASA 2023: stages, length, and fan-case height); the two streams are not drawn to a measured bypass ratio.
:::

The engine of {numref}`fig-p54-turbofan` powers the Boeing 737-800 of [page 1.3](../chapter-1/vehicle-anatomy.md) (Boeing 2025, Section 3.3). Because each stream has its own exit speed, we write one term per stream in [](#eq-p54-thrust). With both nozzles expanded to the outside pressure and the fuel in the core stream:

:::{math}
:label: eq-p54-turbofan
\begin{aligned}
T &= \dot m_\text{bypass}(V_{e,\text{bypass}} - V_\infty)\\
&\;\;\; + (\dot m_\text{core} + \dot m_f)V_{e,\text{core}}\\
&\;\;\; - \dot m_\text{core}V_\infty
\end{aligned}
:::

The bypass stream works like engine 2 in worked example 1, accelerating a large mass of air by a small amount. A **high-bypass turbofan** gets most of its thrust from the fan, and modern ones have bypass ratios of about 8 to 12 (Leishman 2022, Chapter 40). Its slower jet is also quieter. Airliners use it.

A **low-bypass turbofan** is slimmer and gets more thrust from each kilogram of air, though its exhaust is faster. Fighters use it, often with an afterburner, at bypass ratios of about 0.3 to 0.9. The Pratt & Whitney F100-PW-229 of the F-15E and F-16C has about 0.36 (Leishman 2022, Chapter 47). A turbojet is the limit $\beta = 0$.

### Worked example 2: what the fan saves on the executive jet

The twin-engine executive jet of [page 5.1](#p51-example-2) has a mass of 33,100 kg ($mg$ = 324,711 N), a wing area of 88.2 m², and the polar $C_D = 0.015 + 0.050\,C_L^2$. It cruises at 225 m/s at 10,500 m. We compare two engines that produce the same thrust there. One passes 20.0 kg/s of air, like a turbojet, and the other passes 100 kg/s, like a turbofan. We treat each exhaust as one stream at one speed and neglect the fuel, as in worked example 1.

1. **Thrust in cruise.** At 10,500 m the standard atmosphere of [page 1.4](#p14-speed-of-sound) gives $\rho$ = 0.38745 kg/m³ and a speed of sound of 297.3 m/s, so $M = 225/297.3 = 0.757$. That is below Mach 0.80, up to which we trust this jet's polar. The thrust required is the [drag of page 5.1](#eq-p51-TR):

   $$
   \begin{aligned}
   q &= 0.5 \times 0.38745 \times {225}^{2}\\
   &= 9{,}807.3\ \text{Pa}\\
   D_0 &= 9{,}807.3 \times 88.2 \times\\
   &\;\;\; 0.015\\
   &= 12{,}975.1\ \text{N}\\
   D_i &= \frac{0.050 \times {324{,}711}^{2}}{9{,}807.3 \times 88.2}\\
   &= 6{,}094.6\ \text{N}\\
   D &= 12{,}975.1 + 6{,}094.6\\
   &= 19{,}069.7\ \text{N}
   \end{aligned}
   $$

   Each engine gives half, 9,534.8 N.
2. **Exhaust speed and propulsive efficiency**, from $V_e = V_\infty + T/\dot m$ and [](#eq-p54-etap). For the engine of 20.0 kg/s:

   $$
   \begin{aligned}
   V_e &= 225 + \frac{9{,}534.8}{20.0}\\
   &= 225 + 476.7\\
   &= 701.7\ \text{m/s}\\
   \eta_p &= \frac{2}{1 + 701.7/225}\\
   &= 0.4856
   \end{aligned}
   $$

   For the engine of 100 kg/s:

   $$
   \begin{aligned}
   V_e &= 225 + \frac{9{,}534.8}{100}\\
   &= 225 + 95.35\\
   &= 320.35\ \text{m/s}\\
   \eta_p &= \frac{2}{1 + 320.35/225}\\
   &= 0.8252
   \end{aligned}
   $$
3. **Fuel.** Suppose the two engines turn fuel into gas energy equally well. Then, at the same flight speed, the fuel burned per unit thrust goes as $1/\eta_p$ (Leishman 2022, Chapter 40, Eq. 19). The turbofan burns

   $$
   \begin{aligned}
   &\frac{0.4856}{0.8252}\\
   &\;\;\;= 0.588
   \end{aligned}
   $$

   of the turbojet's fuel, 41% less, on every hour of cruise.
4. **Size.** Continuity, $\dot m = \rho V A$, gives the area of the stream tube each engine must capture far ahead. For 20.0 kg/s, $A = 20.0/(0.38745 \times 225) = 0.2294$ m², a circle 0.540 m across. For 100 kg/s, $A = 100/(0.38745 \times 225) = 1.147$ m², a circle 1.21 m across.

To get that fuel saving, the engine needs a larger fan and nacelle, which add weight and drag of their own.

(p54-turboprop)=
### Turboprop and turboshaft

A **{term}`turboprop`** pushes the same idea further. Its turbine takes almost all the energy of the gas as shaft power and turns a propeller, which moves a huge flow of air a little faster ({numref}`fig-p54-turboprop`). The exhaust leaves slowly and adds only a small jet thrust (Leishman 2022, Chapter 47). In many turboprops the turbine that turns the propeller, the **{term}`power turbine`**, is mounted on its own shaft, free of the compressor and its turbine. The AE 2100D2 of the figure is built this way (EASA 2008).

:::{figure} figures/p54-turboprop.svg
:label: fig-p54-turboprop
:alt: Two drawings of a free-turbine turboprop. Top, the whole engine in section along a dash-dot centerline: at the left a pointed spinner and the propeller blade roots, cut short; behind them the reduction gearbox, sketched as a set of gears in the housing, with an annular inlet around it where an arrow labeled air in enters; the exhaust duct widens to the right, where an arrow is labeled slow exhaust. Below, the upper half of the core and power turbine drawn 2.3 times larger, in flow order: a 14-stage compressor, an annular combustor liner, a 2-stage compressor turbine on a hollow shaft, and a 2-stage power turbine whose shaft runs forward through the hollow shaft to the gearbox. A key names parts 1 to 7.
:width: 90%

Schematic of a free-turbine turboprop in section, with the upper half of its core and power turbine enlarged below. Almost all the energy of the gas goes to a shaft that turns the propeller through a gearbox, and the exhaust leaves slowly. Proportions after the Rolls-Royce AE 2100D2 (EASA 2008: stages, gearbox ratio, and length); the gearbox, sketched as a set of gears, and the air inlet around it are drawn on the engine axis, while on this engine the gearbox lies a little above the axis and the air enters below it.
:::

At turbine speed the propeller tips would go faster than sound (Leishman 2022, Chapter 47), so a reduction gearbox slows the propeller down. On the AE 2100D2 the gearbox ratio is 13.98 (EASA 2008).

A turboprop is rated in shaft power, so its thrust comes from [the relation of page 5.1](#eq-p51-PA), $T = \eta P/V$, with the propeller efficiency $\eta$. The small jet thrust $T_j$ of the exhaust adds the power $T_jV_\infty$. Engine makers combine it into one number, the **{term}`equivalent shaft power`** $P_\text{es}$, defined as the shaft power that would give the same total with the propeller alone (Leishman 2022, Chapter 47).

:::{math}
:label: eq-p54-esp
\begin{aligned}
P_\text{es} &= P_s + \frac{T_jV_\infty}{\eta}\\
T &= \frac{\eta P_\text{es}}{V_\infty}
\end{aligned}
:::

Here $P_s$ is the shaft power. If you work in English units, with power in horsepower and speed in ft/s, the thrust in pounds is $T = 550\,\eta P/V$, because 1 hp is 550 ft·lb/s.

A **{term}`turboshaft`** is the same engine with the propeller replaced by an output shaft. Most helicopters, apart from small ones with piston engines, use one to turn the rotor through a gearbox and transmission (Leishman 2022, Chapter 47). Turboshafts also drive boats and tanks (NASA Glenn Research Center n.d.d).

(p54-afterburner)=
### Afterburner

An **{term}`afterburner`** is a second combustion zone behind the turbine. Fuel is sprayed into the exhaust, flame holders keep the flame in place, and an adjustable nozzle passes the hotter, faster flow. The exhaust still has plenty of oxygen, because the main combustor burns only part of it (Leishman 2022, Chapter 46).

We burn the extra fuel there, and not in the combustor, because the turbine blades limit how hot the gas reaching them can be. Behind the turbine there are no spinning blades, so we can heat the gas much further and get a faster jet. The penalty is heavy fuel burn. The thrust can nearly double, while the fuel flow grows much more. For the F100-PW-229 the thrust specific fuel consumption goes from 0.76 to 1.94 lb of fuel per lb of thrust per hour, $1.94/0.76 = 2.55$ times more (Leishman 2022, Chapter 46). Fighters light it for takeoff, climb, and combat. Concorde used afterburning turbojets for takeoff and to accelerate through the speed of sound, and turned the afterburners off in cruise (Leishman 2022, Chapter 46; NASA Glenn Research Center n.d.a).

### Ramjet and scramjet

At high supersonic speed the inlet alone can compress the air. A **{term}`ramjet`** has no compressor and no turbine. Its inlet slows the air below the speed of sound, and the fuel burns in that slow air. Page 4.1 draws one and [works an example](#p41-air-breathing). It makes no thrust standing still, so a rocket or another engine must bring it up to speed first. Above about Mach 5, slowing the air to subsonic speed wastes too much energy, and the ramjet loses most of its efficiency (NASA Glenn Research Center n.d.b). Published charts still carry its band to about Mach 6.6 (Leishman 2022, Chapter 40, Figure 20). A **{term}`scramjet`** keeps the flow supersonic through the combustor (NASA Glenn Research Center n.d.b).

### Piston engine and propeller

The oldest arrangement is a piston engine turning a propeller. It is simple, it costs little, and the propeller is efficient at low speed. Three things limit it (Leishman 2022, Chapter 40). The power for each kilogram of engine falls as engines get bigger. The propeller loses efficiency as its tips approach the speed of sound. And the thin air at altitude cuts the power, unless a supercharger or turbocharger feeds the engine. Piston engines stay with small aircraft that fly low and slow.

### Two more arrangements

With **vectored thrust** the engine turns its exhaust downward, as on the F-35B, which also uses a shaft-driven lift fan to land vertically. An **open rotor**, or unducted fan, drops the fan case for an even higher effective bypass ratio (Leishman 2022, Chapter 47).

(p54-matching-mission)=
## Choosing an engine type

Now we choose among the families for a mission. Two things come first:

- the range of flight speeds the mission needs;
- the speed that dominates the flight.

That speed is usually the cruise, or the {term}`loiter` for an aircraft that circles over one place, and sometimes the maximum speed or the climb.

We look at the dominating speed first, because each family works well only in a band of speed ({numref}`fig-p54-mach-bands`). Propellers work well up to about Mach 0.5, and advanced designs to about 0.6, before their tips approach the speed of sound (Leishman 2022, Chapter 40). High-bypass turbofans cruise at about Mach 0.7 to 0.85 (Leishman 2022, Chapter 47). Faster still come engines with afterburners, then ramjets and scramjets.

Propeller engines also deliver their thrust differently. With the power fixed, $T = \eta P/V$ is largest at low speed and falls as the aircraft speeds up ([page 5.1](#eq-p51-PA)), while a jet's thrust changes much less with speed. So a turboprop gives strong thrust at takeoff and in the climb, and less as the cruise speed rises. Turboprops suit missions at the slow end of {numref}`fig-p54-mach-bands`.

:::{figure} figures/p54-mach-bands.svg
:label: fig-p54-mach-bands
:alt: Horizontal bars against flight Mach number, with the scale stretched from 0 to 1.2 and compressed from 1.2 to 10, a break mark between, and a dashed line at Mach 1. From the top: propeller, piston or turbine, from 0 to 0.5, with a hatched extension to 0.6 labeled advanced propellers; high-bypass turbofan, cruise, from 0.7 to 0.85; turbofan or turbojet with afterburner, from 0.3 to 3.5; ramjet, from 2.9 to 6.6; scramjet, from 4.9 to 9.5.
:width: 90%

Values from Leishman (2022). Each engine family works well only in its own band of flight speed, and a faster mission needs an engine that makes a faster jet. The propeller band is from Chapter 40 and the turbofan cruise band from Chapter 47; the other three bands are read from Chapter 40, Figure 20, to about 0.1 in Mach number, and that figure has no band for a turbojet without afterburner. That figure's afterburner band is named "turbofans with afterburner" and marks Concorde's afterburning turbojet inside it, so the bar here names both. Below Mach 1.2 the scale is stretched.
:::

:::{table} Engine families, the speeds where they work well, and real aircraft that carry them (sources in the text).
:label: tbl-p54-families
:align: center

<table>
<tr><th>Engine type</th><th>Works well</th><th>Why</th><th>Real aircraft</th></tr>
<tr><th scope="row">Piston engine and propeller</th><td>Low speed and low altitude</td><td>Simple and cheap; the power for each kilogram falls as engines grow</td><td>Small aircraft</td></tr>
<tr><th scope="row">Turboprop</th><td>Up to about Mach 0.5, or 0.6 with advanced propellers</td><td>Moves a huge air flow a little; strong thrust at low speed</td><td>Lockheed C-130 Hercules, four Allison T56</td></tr>
<tr><th scope="row">High-bypass turbofan</th><td>Cruise at about Mach 0.7 to 0.85</td><td>A large, efficient bypass stream; a ducted fan works at a higher speed than a propeller</td><td>Boeing 737-800, two CFM56-7B</td></tr>
<tr><th scope="row">Low-bypass turbofan or turbojet, with afterburner</th><td>From about Mach 0.3 to 3.5; built for transonic and supersonic flight</td><td>Slim, with much thrust per kilogram of air; the afterburner adds thrust for short times</td><td>F-15E and F-16C, F100-PW-229; Concorde, afterburning turbojets</td></tr>
<tr><th scope="row">Ramjet, scramjet</th><td>About Mach 2.9 to 6.6, and 4.9 to 9.5</td><td>No rotating parts; no thrust standing still</td><td>Supersonic missiles, boosted to speed (ramjet)</td></tr>
</table>

:::

Speed is only the first filter. We then check four areas.

:::{tip} Method: choosing an engine type
1. **Engine size.** Find how much thrust or power the aircraft needs, and check whether an engine of that family is built in that size.
2. **Flight envelope and fuel consumption.** Pick the family that works well at the dominating speed and burns the least fuel there, based on its propulsive efficiency. Then verify that it can also handle the other flight phases, such as takeoff and climb.
3. **Costs.** An engine already in production is the cheapest to buy, a growth version of one costs more, and a new engine costs the most. Fuel and maintenance are part of the operating cost, and frequent maintenance keeps the aircraft on the ground.
4. **Acceptance.** Check noise outside and inside, vibration, and passenger comfort. Propeller aircraft are noisy and usually fly lower than jets, in rougher air.

Back every choice with numbers from the first two steps.
:::

:::{warning} The maximum speed is not the cruise speed
If you choose the engine for the highest speed the aircraft must reach, you may give it the wrong engine for the speed it flies most of the time. Find the speed that dominates the mission first. The maximum speed is a check the engine must also pass.
:::

### Worked example 3: an engine type for the four-engine transport

The [four-engine turboprop transport of page 5.3](#p53-example-3) has a mass of 52,000 kg ($mg$ = 510,120 N), a wing area of 128 m², $C_{D,0} = 0.022$, and $K = 0.04737$. Page 5.3 gave it four engines of 2,900 kW of shaft power each, with a propeller efficiency of 0.84. Suppose its job is to carry heavy cargo over long legs, and it flies each leg at the speed for best range, at 6,500 m. We check its engine type with the method, speed first, as if the choice were still open.

1. **Flight envelope and dominating speed.** Here the cruise dominates. A propeller aircraft gets its best range at the maximum $C_L/C_D$ of [page 5.2](#p52-prop-breguet), where $C_L = \sqrt{C_{D,0}/K}$. With $\rho$ = 0.6236 kg/m³ at 6,500 m ([page 1.4](#p14-speed-of-sound)):

   $$
   \begin{aligned}
   C_L &= \sqrt{0.022/0.04737}\\
   &= 0.6815\\
   V &= \sqrt{\frac{2 \times 510{,}120}{0.6236 \times 128}} \times\\
   &\;\;\; \frac{1}{\sqrt{0.6815}}\\
   &= 136.95\ \text{m/s}
   \end{aligned}
   $$

   The speed of sound there is 314.3 m/s, so $M = 136.95/314.3 = 0.436$. That is inside the propeller band of {numref}`fig-p54-mach-bands` and well below the cruise band of the high-bypass turbofan, which starts at Mach 0.7.
2. **Engine size and cruise thrust.** At this point $C_D = 2C_{D,0} = 0.044$ (page 5.2), so the drag is

   $$
   \begin{aligned}
   D &= 510{,}120 \times \frac{0.044}{0.6815}\\
   &= 32{,}935\ \text{N}
   \end{aligned}
   $$

   or 8,234 N for each engine. Turboprops of 2,900 kW are in production, and the AE 2100 of {numref}`fig-p54-turboprop` is rated from 2,787 to 3,458 kW (EASA 2008).
3. **Fuel and propulsive efficiency.** By [](#eq-p54-etap), even an ideal jet stream matches the propeller's 0.84 only if its exhaust leaves at $V_e/V_\infty = 2/0.84 - 1 = 1.381$ times the flight speed. Each engine must then add only a little speed to a large air flow:

   $$
   \begin{aligned}
   V_e - V_\infty &= 2 \times 136.95 \times\\
   &\;\;\; (1/0.84 - 1)\\
   &= 52.17\ \text{m/s}\\
   \dot m &= \frac{8{,}234}{52.17}\\
   &= 157.8\ \text{kg/s}
   \end{aligned}
   $$

   That is 58% more air than the turbofan of worked example 2 moved, for less thrust. The slower an aircraft flies, the more air an efficient engine must move. A propeller moves it with no duct around it, and it is the most efficient choice at low and moderate speeds (Leishman 2022, Chapter 47).
4. **Low-speed thrust.** With the power fixed, $T = \eta P/V$ grows as the speed falls. At sea level the four engines give $P_A = 4 \times 0.84 \times 2{,}900 = 9{,}744$ kW. At 82 m/s, the slower climb speed of [page 5.3](#p53-one-engine-out), that is $T_A = 9{,}744/82 = 118.8$ kN. This aircraft has $m_\text{ad} = 0.75$. In the cruise air the lapse of page 5.1 is $(\rho/\rho_0)^{m_\text{ad}} = {0.50906}^{0.75} = 0.60267$. The engines then give $9{,}744 \times 0.60267 = 5{,}872$ kW and $T_A = 5{,}872/136.95 = 42.88$ kN, enough for the 32.93 kN of drag. At the climb speed they give 2.77 times as much, and a heavy aircraft needs that margin to climb.
5. **Costs and acceptance.** An engine in production, as step 2 found, is the cheapest choice. Propeller noise and vibration reach the cabin, which matters less for cargo than for passengers.

The turboprop fits this mission on speed, fuel, and thrust.

**Check.** A real aircraft with the same job has the same engine type. The Lockheed C-130 carries cargo over long distances with no need for high speed, on four Allison T56 turboprops (NASA Glenn Research Center n.d.c; Leishman 2022, Chapter 47).

## Summary

:::{important} Summary
- An air-breathing engine makes the thrust of [](#eq-p54-thrust), equal to the momentum it adds to the air and the fuel plus a pressure term.
- With $\eta_p = 2/(1 + V_e/V_\infty)$, the same thrust burns less fuel when a large air flow is sped up a little. Turbofans and propellers exist for that reason.
- A turbojet passes air through inlet, compressor, combustor, turbine, and nozzle. The turbine gives back only what the compressor took, and the rest becomes exhaust speed. The thrust is the small difference of large loads inside the engine.
- Start by choosing the engine family for the speed that dominates the mission, then confirm the choice with size, fuel, cost, and acceptance.
:::

:::{table} The equations of this page.
:label: tbl-p54-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Thrust of an engine that breathes air | $T = (\dot m_\text{air} + \dot m_f)V_e - \dot m_\text{air}V_\infty + (p_e - p_\infty)A_e$ |
| The same, fuel neglected, nozzle expanded to ambient | $T \approx \dot m_\text{air}(V_e - V_\infty)$ |
| Propulsive efficiency | $\eta_p = 2/(1 + V_e/V_\infty)$ |
| Bypass ratio | $\beta = \dot m_\text{bypass}/\dot m_\text{core}$ |
| Thrust of a turbofan | $T = \dot m_\text{bypass}(V_{e,\text{bypass}} - V_\infty) + (\dot m_\text{core} + \dot m_f)V_{e,\text{core}} - \dot m_\text{core}V_\infty$ |
| Equivalent shaft power and thrust of a turboprop | $P_\text{es} = P_s + T_jV_\infty/\eta$; $T = \eta P_\text{es}/V_\infty$ |

:::

:::{exercise} For discussion
:label: ex-p54-discussion

1. Why does the pressure reach its highest value leaving the compressor, while the temperature reaches its highest value leaving the combustor?
2. To raise $\eta_p$ at a fixed flight speed and a fixed thrust, should the exhaust speed go up or down? What must happen to the air flow?
3. Why does a fighter use a low-bypass turbofan, and not the high-bypass turbofan of an airliner?
4. Why can a ramjet not take off from a runway on its own?
5. An afterburner burns fuel less efficiently than the main combustor. Why not burn all the fuel in the main combustor instead?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-5-4.html
:label: quiz-5-4
:width: 100%
:enumerated: false

Quiz for Standard 5.4: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016. Chapter 9 (thrust distribution of a typical single-spool axial-flow jet engine, courtesy of Rolls-Royce).
- Boeing Commercial Airplanes (Boeing), *[Next-Generation 737 Airplane Characteristics for Airport Planning](https://www.boeing.com/content/dam/boeing/v2/airports/acaps/737NG_REV_C.pdf)*, D6-58325-7 Rev C, 2025. Section 3.3 (737-800 with CFM56-7B engines).
- European Union Aviation Safety Agency (EASA), *Type-Certificate Data Sheet IM.E.040, Rolls-Royce Corporation AE 2100 Series Engines*, issue 01, 2008. Description, dimensions, ratings, and gear ratio.
- European Union Aviation Safety Agency (EASA), *Type-Certificate Data Sheet E.004, CFM International CFM56-7B Series Engines*, issue 07, 2023. Sections 2 and 4.
- Federal Aviation Administration (FAA), *Type Certificate Data Sheet 1E16, General Electric CJ610 Series*, revision 15, 2008. Type, stages, and principal dimensions.
- Leishman, J. G., *[Introduction to Aerospace Flight Vehicles](https://eaglepubs.erau.edu/introductiontoaerospaceflightvehicles/)*, Embry-Riddle Aeronautical University, 2022 (online edition, updated). Chapter 40 (Fundamentals of Propulsion Systems, with Figure 20), Chapter 45 (Aircraft Propellers), Chapter 46 (Turbojet Engines), Chapter 47 (Turbofan and Turboprop Engines). DOI 10.15394/eaglepub.2022.1066.
- NASA Glenn Research Center, "[Afterburning Turbojet](https://www.grc.nasa.gov/WWW/K-12/BGP/aturba.html)," Beginner's Guide to Propulsion, n.d.a.
- NASA Glenn Research Center, "[Ramjet Propulsion](https://www.grc.nasa.gov/WWW/K-12/BGP/ramjet.html)," Beginner's Guide to Propulsion, n.d.b.
- NASA Glenn Research Center, "[Turbine Engines](https://www.grc.nasa.gov/WWW/K-12/BGP/turbine.html)," Beginner's Guide to Propulsion, n.d.c.
- NASA Glenn Research Center, "[Turboprop Engine](https://www.grc.nasa.gov/WWW/K-12/BGP/aturbp.html)," Beginner's Guide to Propulsion, n.d.d.
