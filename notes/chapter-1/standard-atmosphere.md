---
title: "1.4 Standard Atmosphere"
short_title: 1.4 Standard Atmosphere
---

:::{include} ../_parts/standards/1.4.md
:::

An aircraft's takeoff distance, climb rate, and cruise speed all depend on the surrounding air, so engineers need a consistent reference model of how the atmosphere changes with altitude: the {term}`standard atmosphere`. We begin by connecting gas pressure, {term}`density`, and temperature through the ideal-gas {term}`equation of state`. From a vertical force balance on still air, we then derive how pressure and density drop with altitude across both isothermal and temperature-gradient layers, and show how the same equations extend to other planets.

:::{note} What to take from this page
- Pressure, density, and temperature of a gas are linked by $p = \rho R T$, with $T$ in kelvin and $R = 287$ J/(kg K) for air.
- A force balance on still air gives the {term}`hydrostatic equation` $dp = -\rho g_0\,dh$, showing that pressure falls with height by the weight of the air left below.
- In an {term}`isothermal layer` pressure and density fall exponentially; in a {term}`gradient layer` they fall as a power of the temperature ratio. Each layer starts from the values at its own base.
- The speed of sound, $a_s = \sqrt{\gamma R T}$, depends only on temperature. The same equations work for any planet once its gas constant, gravity, and lapse rate are known.
:::

## Pressure, density, and temperature

Four quantities describe the air at any point of a flow: pressure, density, temperature, and velocity. We leave velocity for the next page, [Bernoulli and pitot static](bernoulli-and-pitot-static.md). The other three describe the state of the gas itself, and {numref}`fig-p14-gas-properties` shows what each one measures at the scale of the molecules.

:::{figure} figures/p14-gas-properties.svg
:label: fig-p14-gas-properties
:alt: Three panels, each a small sample of gas drawn as dots for molecules. Pressure: molecules with velocity arrows strike a hatched wall, and a force dF pushes on a small area dA of the wall, with p equal to dF over dA. Density: a small cube of volume dv holds five molecules of total mass dm, with rho equal to dm over dv. Temperature: molecules move in random directions at different speeds, and the mean kinetic energy of one molecule is three halves k T.
:width: 85%

Schematic, not to scale. Pressure comes from molecules striking a surface, density is their mass in a volume, and temperature measures their average kinetic energy, that is, how fast they move.
:::

:::{prf:definition} Pressure, density, and temperature
:label: def-p14-state
- **Pressure** $p$ is the normal force per unit area that a gas exerts on a surface: $p = dF/dA$ as the area $dA$ shrinks toward zero. The force comes from the momentum of the molecules that strike the surface. Unit: pascal, 1 Pa = 1 N/m². The pressure of still air on any surface, whatever its direction, is the {term}`static pressure`.
- **Density** $\rho$ is the mass per unit volume: $\rho = dm/dv$ as the volume $dv$ shrinks toward zero. Unit: kg/m³.
- **Temperature** $T$ measures the average translational kinetic energy of the molecules (their motion through space). The mean value for one molecule is $\tfrac{3}{2} k T$, where $k = 1.380649 \times {10}^{-23}$ J/K is the Boltzmann constant (NIST n.d.). Unit: kelvin, K.
:::

A bicycle pump shows all three. When you push the handle, the same mass of air fills a smaller volume. Density rises, more molecules strike the walls each second, and pressure rises, while the compression work warms the air. At sea level the mean translational kinetic energy of one air molecule is $\tfrac{3}{2}(1.380649 \times {10}^{-23})(288.16) = 5.968 \times {10}^{-21}$ J. That number is tiny, yet there are so many molecules striking every square meter each second that their combined impacts add up to 101,325 Pa on every surface.

The temperature here is absolute. It is in kelvin, counted from the zero at which the molecules would stop, and only on this scale is the energy proportional to $T$.

(p14-equation-of-state)=
## The equation of state

Pressure, density, and temperature are not independent. For air at the conditions aircraft meet, they obey the ideal gas law from chemistry, $p v = n R_u T$. Here $v$ is the volume of the gas, $n$ the number of moles, and $R_u = 8{,}314.5$ J/(kmol K) the universal gas constant, the 8.3145 J/(mol K) of chemistry written per kilomole. We divide both sides by the volume $v$ and write the number of moles as the mass $m$ divided by the molar mass $M$:

$$
p = \frac{n R_u T}{v} = \frac{m}{v}\,\frac{R_u}{M}\,T
$$

The ratio $m/v$ is the density, and $R_u/M$ is a constant for a given gas, its {term}`specific gas constant` $R$. The result is the equation of state:

:::{math}
:label: eq-p14-state
p = \rho R T
:::

For dry air, with a molar mass of 28.96 kg/kmol, $R = 8{,}314.5/28.96 = 287.1$ J/(kg K); in these notes we use $R = 287$ J/(kg K). Checking the units, kg/m³ times J/(kg K) times K gives J/m³, and a joule per cubic meter is a newton per square meter, or one pascal.

The equation of state assumes an ideal gas, whose molecules take up almost no volume and do not attract each other. Air around an aircraft fits this model well. The hot gas around a vehicle entering an atmosphere does not, and later courses treat that case.

If we put in the sea-level values of the standard atmosphere, the equation gives $\rho = 101{,}325/(287 \times 288.16) = 1.2252$ kg/m³, which agrees with the tabulated 1.2250 kg/m³ to four figures.

:::{warning} Kelvin, never Celsius
The sea-level temperature, 288.16 K, is about 15 °C. If you put 15 into the equation of state, you get $\rho = 101{,}325/(287 \times 15) = 23.5$ kg/m³, about twenty times the real density of air. Convert every temperature to kelvin, by adding 273.15 to the temperature in degrees Celsius, before it enters an equation on this page.
:::

## Why a standard atmosphere

The real atmosphere changes with place, season, time of day, and weather. An aircraft at a hot, high airport has thinner air under its wings than at a cold sea-level airport, and needs a longer runway. To compare designs or calibrate instruments, engineers need one agreed set of conditions.

:::{prf:definition} Standard atmosphere
:label: def-p14-standard-atmosphere
A **standard atmosphere** is an agreed model of the temperature, pressure, and density of the air as functions of altitude alone. The World Meteorological Organization defines it as a vertical distribution that "is roughly representative of year-round, midlatitude conditions," in which the air obeys the equation of state and the hydrostatic equation (NOAA, NASA, and U.S. Air Force 1976).
:::

The same document lists its main uses: altimeter calibration, aircraft performance calculations, and aircraft and rocket design. Although weather on any real day differs from this reference, quoting performance "at standard conditions" lets engineers compare vehicles on a common baseline.

In these notes we use the model of Anderson (2016, Chapter 3) and the NASA Glenn atmosphere model (NASA Glenn Research Center n.d.a), whose sea-level values are $T = 288.16$ K, $p = 101{,}325$ Pa, and $\rho = 1.2250$ kg/m³. The U.S. Standard Atmosphere, 1976 uses 288.15 K, a difference that does not show at four significant figures.

## The hydrostatic equation

The equation of state applies at a single point. The second equation of the model describes how pressure changes with height. Still air has weight, and the pressure at any level must support the weight of the air above it. We write that idea for a thin slab.

In {numref}`fig-p14-slab-balance` we take a column of air at rest and cut from it a thin slab of horizontal area $dA$ and thickness $dh$, with its bottom face at altitude $h$. Three vertical forces act on the slab:

1. the pressure force from below, $p\,dA$, pushing up on the bottom face;
2. the pressure force from above, $(p + dp)\,dA$, pushing down on the top face, where $dp$ is the small change of pressure across the slab;
3. the weight of the slab, its mass $\rho\,dA\,dh$ times gravity $g_0$, pulling down.

:::{figure} figures/p14-slab-balance.svg
:label: fig-p14-slab-balance
:alt: On the left, a tall column of still air standing on the ground with a thin slab highlighted partway up and an altitude arrow beside it. On the right, the slab enlarged, with area dA and thickness dh. A long force arrow pushes up on its bottom face, labeled p dA. A shorter arrow pushes down on its top face, labeled p plus dp times dA, and the weight rho g0 dA dh acts down from the center. The upward arrow is as long as the two downward arrows together.
:width: 70%

Schematic of a thin slab of still air. The pressure force from below carries the pressure force from above and the weight of the slab. The difference between the two pressure forces is exaggerated.
:::

The air does not move, so the forces add to zero. We take up as positive:

$$
\begin{aligned}
p\,dA - (p + dp)\,dA&\\
{} - \rho\,g_0\,dA\,dh &= 0
\end{aligned}
$$

When we expand the middle term, $p\,dA$ cancels:

$$
-dp\,dA - \rho\,g_0\,dA\,dh = 0
$$

Dividing by $dA$ and solving for $dp$ gives

:::{math}
:label: eq-p14-hydrostatic
dp = -\rho\,g_0\,dh
:::

This is the hydrostatic equation. The minus sign means that pressure falls as altitude rises, by the weight of each slab we pass. Near sea level $\rho g_0 = 1.2250 \times 9.81 = 12.02$ Pa per meter of climb. This equation applies to any fluid at rest. For water, whose density does not change, it gives the $\Delta p = \rho g h$ of a column of liquid, which we use for the manometer on the next page.

Integrated over the whole column, the equation shows that the pressure at the ground equals the weight of all the air above one square meter. Sea-level pressure, 101,325 Pa, is the weight of $101{,}325/9.81 = 10{,}329$ kg of air resting on each square meter.

In these notes we use $g_0 = 9.81$ m/s², the standard value 9.80665 m/s² to three figures, and we keep it the same at every altitude. Gravity weakens a little with height. The standard tables allow for this with a geopotential altitude, an altitude adjusted for the weaker gravity, which differs from the geometric altitude by about 0.3% at 20 km.

(p14-layers)=
## Layers of the standard atmosphere

We now have two equations for three unknowns: $p$, $\rho$, and $T$. The third relation is a model of temperature against altitude. The standard atmosphere gives it as a series of straight-line pieces ({numref}`fig-p14-temperature-layers`).

:::{figure} figures/p14-temperature-layers.svg
:label: fig-p14-temperature-layers
:alt: Plot of temperature in kelvin against altitude from 0 to 53 kilometers. The temperature falls in a straight line from 288.16 K at sea level to 216.66 K at 11 kilometers in the troposphere, a gradient layer with lapse rate minus 0.0065 K per meter. It stays at 216.66 K from 11 to 25 kilometers in the lower stratosphere, an isothermal layer shaded gray. In the upper stratosphere, a gradient layer, it rises at plus 0.003 K per meter to 282.66 K at 47 kilometers, then stays constant again to 53 kilometers in the stratopause, a second shaded isothermal layer.
:width: 75%

Computed from the layer model of these notes. The profile is a chain of straight segments, vertical in the isothermal layers (shaded); each layer starts at the temperature where the layer below ends.
:::

:::{prf:definition} Gradient layer, isothermal layer, lapse rate
:label: def-p14-layers
In a **gradient layer** the temperature changes linearly with altitude:

$$
T = T_1 + a\,(h - h_1)
$$

where $h_1$ is the altitude of the base of the layer, $T_1$ the temperature there, and $a = dT/dh$ the **lapse rate**, in K/m. The lapse rate is negative when temperature falls with height. In an **isothermal layer** the temperature is the same at every altitude: $a = 0$ and $T = T_1$.
:::

The lowest layer, the {term}`troposphere`, runs from sea level to 11,000 m with a {term}`lapse rate` $a = -0.0065$ K/m, meaning the air cools by 6.5 K for every kilometer of climb. Its top, the {term}`tropopause`, is at 216.66 K. Above it lies the {term}`stratosphere`. Its lower part, from 11,000 m to 25,000 m, is isothermal in this model. In its upper part the temperature rises again, at $a = +0.003$ K/m. The ozone at those heights absorbs ultraviolet light from the Sun, and that energy heats the air (Salawitch et al. 2023, Q2). A common shorthand calls the layers where temperature changes "spheres" and those where it stays constant "pauses," although that usage is imprecise. The isothermal layer from 11 to 25 km is the lower stratosphere, and the tropopause is its lower boundary at 11 km.

{numref}`tbl-p14-layers` lists the layers and the values at the base of each. The base values are not new data. We compute each one from the layer below with the equations of the next two sections, starting from sea level.

:::{table} The layers of the standard atmosphere used in these notes, with the temperature, pressure, and density at the base of each layer, carried up from sea level with $g_0 = 9.81$ m/s² and $R = 287$ J/(kg K).
:label: tbl-p14-layers
:align: center

| Base altitude $h_1$ (m) | Layer | Type | Lapse rate $a$ (K/m) | Temperature $T_1$ (K) | Pressure $p_1$ (Pa) | Density $\rho_1$ (kg/m³) |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 0 | Troposphere | Gradient | −0.0065 | 288.16 | 101,325 | 1.2250 |
| 11,000 | Lower stratosphere | Isothermal | 0 | 216.66 | 22,616 | 0.3636 |
| 25,000 | Upper stratosphere | Gradient | +0.003 | 216.66 | 2,484 | 0.03994 |
| 47,000 | Stratopause | Isothermal | 0 | 282.66 | 120.1 | 0.001480 |
| 53,000 | Mesosphere | Gradient | −0.0045 | 282.66 | 58.11 | 0.0007162 |

:::

Up to 20 km, this model and the U.S. Standard Atmosphere, 1976 agree to within 0.2%. Above 20 km they diverge. The 1976 standard begins warming at 20 km, while our model stays isothermal to 25 km and then warms faster, reaching 282.66 K at 47 km against 270.65 K. At 47 km our model's pressure is about 8.2% above the 1976 value. Use the model of these notes for the problems here, and consult the 1976 tables when a design requires upper-atmosphere data.

## Pressure and density in an isothermal layer

We combine the two equations first in the simpler kind of layer. The equation of state gives $\rho = p/(RT)$, and we put it into the hydrostatic equation:

$$
dp = -\frac{p}{R T}\,g_0\,dh
$$

Dividing both sides by $p$ separates the variables:

:::{math}
:label: eq-p14-dpp
\frac{dp}{p} = -\frac{g_0}{R T}\,dh
:::

This equation applies in every layer. In an isothermal layer $T = T_1$ is a constant, so it comes out of the integral. We integrate from the base of the layer ($h_1$, $p_1$) to any altitude $h$ in the layer (with pressure $p$):

$$
\int_{p_1}^{p} \frac{dp}{p} = -\frac{g_0}{R T_1} \int_{h_1}^{h} dh
$$

which gives

$$
\ln\frac{p}{p_1} = -\frac{g_0\,(h - h_1)}{R T_1}
$$

We take the exponential of both sides. For the density, we write the equation of state at both altitudes and divide: $\rho/\rho_1 = (p/RT)/(p_1/RT_1) = p/p_1$, because the temperature is the same. Both ratios follow one law:

:::{math}
:label: eq-p14-isothermal
\frac{p}{p_1} = \frac{\rho}{\rho_1} = \exp\left[-\frac{g_0\,(h - h_1)}{R T}\right]
:::

So in an isothermal layer, pressure and density fall exponentially. Every $R T/g_0 = 287 \times 216.66/9.81 = 6{,}339$ m of climb multiplies them by $1/e$ (dividing by $e = 2.718$, leaving about 37% remaining). On a logarithmic axis an exponential is a straight line, and that is how the isothermal layer appears in {numref}`fig-p14-pressure-density`.

## Pressure and density in a gradient layer

In a gradient layer the temperature in {eq}`eq-p14-dpp` changes with altitude, and it cannot come out of the integral as it stands. We change the variable from altitude to temperature. From $T = T_1 + a(h - h_1)$, a small change of altitude changes the temperature by $dT = a\,dh$, so

$$
dh = \frac{dT}{a}
$$

We put this into {eq}`eq-p14-dpp`:

$$
\frac{dp}{p} = -\frac{g_0}{a R}\,\frac{dT}{T}
$$

Now $g_0$, $a$, and $R$ are constants, and the right side depends only on $T$. We integrate from the base ($p_1$, $T_1$) to any point of the layer ($p$, $T$):

$$
\ln\frac{p}{p_1} = -\frac{g_0}{a R}\,\ln\frac{T}{T_1}
$$

Since $c \ln x = \ln x^{c}$, the exponentials of both sides give the pressure ratio:

:::{math}
:label: eq-p14-gradient-p
\frac{p}{p_1} = \left(\frac{T}{T_1}\right)^{-\frac{g_0}{a R}}
:::

For the density, we divide the equation of state at the two points as before. This time the temperatures differ:

$$
\frac{\rho}{\rho_1} = \frac{p}{p_1}\,\frac{T_1}{T}
= \left(\frac{T}{T_1}\right)^{-\frac{g_0}{a R}} \left(\frac{T}{T_1}\right)^{-1}
$$

and adding the exponents,

:::{math}
:label: eq-p14-gradient-rho
\frac{\rho}{\rho_1} = \left(\frac{T}{T_1}\right)^{-\left(\frac{g_0}{a R} + 1\right)}
:::

In the troposphere $a$ is negative, so the exponent of the pressure ratio is positive: $-g_0/(aR) = 9.81/(0.0065 \times 287) = 5.2586$, and the density exponent is $5.2586 - 1 = 4.2586$. A temperature ratio below 1 raised to a positive power is below 1, so pressure and density fall with altitude, as the hydrostatic equation requires.

In the upper stratosphere $a = +0.003$ K/m and the exponent is negative: $-g_0/(aR) = -9.81/(0.003 \times 287) = -11.394$. There the temperature rises with altitude and the temperature ratio is above 1. A number above 1 raised to a negative power is below 1, so the pressure still falls. For example, at 35,000 m, ten kilometers above the base of the layer at 25,000 m,

$$
\begin{aligned}
T &= 216.66 + 0.003 \times 10{,}000\\
  &= 246.66\ \text{K}\\
p &= 2{,}484 \times \left(\frac{246.66}{216.66}\right)^{-11.394}\\
  &= 2{,}484 \times 0.22819\\
  &= 566.8\ \text{Pa}
\end{aligned}
$$

:::{warning} The sign and the unit of the lapse rate
The lapse rate enters the exponent with its sign: $a = -0.0065$ K/m in the troposphere. If you drop the sign in the troposphere, the exponent turns negative and the pressure rises with altitude. The unit matters too. With $a$ in K/km and $h$ in meters, the exponent is off by a factor of 1,000. Keep $h$ in meters and $a$ in K/m.
:::

The two kinds of layer appear side by side in {numref}`fig-p14-pressure-density`. Between sea level and 25 km the pressure falls by a factor of 40.8 and the density by a factor of 30.7. Neither curve has a break at a layer boundary, because each layer starts from the values where the layer below ends.

:::{figure} figures/p14-pressure-density.svg
:label: fig-p14-pressure-density
:alt: Two plots against altitude from 0 to 30 kilometers, pressure in kilopascals and density in kilograms per cubic meter, both on logarithmic scales, with the isothermal layer from 11 to 25 kilometers shaded. Both curves fall steadily with altitude; in the isothermal layer they are straight lines, in the gradient layers below 11 and above 25 kilometers they are slightly curved. Three worked examples are marked: example 1 at 10.5 kilometers, 24.46 kilopascals, and 0.3875 kilograms per cubic meter; example 2 at 21 kilometers, 4.670 kilopascals, and 0.07509; example 3, a measured pressure of 61.5 kilopascals traced across to an altitude of 4,015 meters, with density 0.8177.
:width: 75%

Computed from the layer model of these notes. Pressure and density fall steadily with no break at a layer boundary, and in the isothermal layer (shaded) both are straight lines on the logarithmic scale. Worked examples: circle, example 1; square, example 2; triangle, example 3.
:::

## The method, in both directions

That gives us the equations for both kinds of layer. {numref}`fig-p14-method-flow` puts them into a method, and the tip below gives the same numbered steps.

:::{figure} figures/p14-method-flow.svg
:label: fig-p14-method-flow
:alt: Flow chart with five numbered steps. Step 1, write the altitude h in meters. Step 2, a decision: which layer holds h, with three branches: 0 to 11,000 meters, gradient layer, a equal to minus 0.0065 K per meter, base at sea level; 11,000 to 25,000 meters, isothermal layer at 216.66 K, base at 11,000 meters; 25,000 to 47,000 meters, gradient layer, a equal to plus 0.003 K per meter, base at 25,000 meters. All three lead to step 3, take the base values of that layer. Step 4, compute T, then p and rho. Step 5, check p equals rho R T and that p lies between the values at the base and the top of the layer.
:width: 85%

Schematic of the method that gives the properties at a given altitude. Step 2 matters most, because the layer determines both the equations and the base values to start from.
:::

:::{tip} Method: temperature, pressure, and density at a given altitude
1. Write the altitude $h$ in meters and every temperature in kelvin.
2. Find the layer that contains altitude $h$ ({numref}`tbl-p14-layers`).
3. Take the base values $h_1$, $T_1$, $p_1$, $\rho_1$ of that layer. Above 11,000 m they are not the sea-level values, so compute them from the layer below or take them from {numref}`tbl-p14-layers`.
4. Compute the temperature, pressure, and density with {eq}`eq-p14-gradient-p` and {eq}`eq-p14-gradient-rho` in a gradient layer or {eq}`eq-p14-isothermal` in an isothermal layer.
5. Check: $p = \rho R T$ agrees to about four figures, and $p$ lies between the pressures at the base and the top of the layer.
:::

The other direction starts from a measurement. An aircraft senses the pressure of the outside air, and we want its altitude.

:::{tip} Method: altitude from a measured pressure or density
1. Find the layer by comparing the measured value with the base values in {numref}`tbl-p14-layers`. Pressure and density fall steadily with altitude, so the layer is the one whose base value is just above the measurement.
2. In a gradient layer, solve {eq}`eq-p14-gradient-p` for the temperature, $T = T_1\,(p/p_1)^{-aR/g_0}$, then the altitude, $h = h_1 + (T - T_1)/a$. With a measured density, $T = T_1\,(\rho/\rho_1)^{-1/(g_0/(aR) + 1)}$; in the troposphere this exponent is $1/4.2586 = 0.23482$.
3. In an isothermal layer, solve {eq}`eq-p14-isothermal` for the altitude: $h = h_1 + (R T_1/g_0)\ln(p_1/p)$.
4. Check by computing the pressure at the altitude found.
:::

The altitude found from a measured density is the {term}`density altitude`. Pilots use it, and [a non-standard day](#p14-nonstandard) below computes one.

(p14-examples)=
## Worked examples

### Worked example 1: a cargo jet in the troposphere

A cargo jet cruises at $h = 10{,}500$ m in the standard atmosphere. Find the temperature, pressure, and density.

1. **Layer.** Because 10,500 m is below 11,000 m, we are in the troposphere, a gradient layer with $a = -0.0065$ K/m and its base at sea level ($h_1 = 0$, $T_1 = 288.16$ K, $p_1 = 101{,}325$ Pa, $\rho_1 = 1.2250$ kg/m³).
2. **Temperature.**
   $$
   \begin{aligned}
   T &= T_1 + a\,(h - h_1)\\
     &= 288.16\\
     &\;\;\; + (-0.0065)(10{,}500)\\
     &= 219.91\ \text{K}
   \end{aligned}
   $$
3. **Temperature ratio.** $T/T_1 = 219.91/288.16 = 0.763152$.
4. **Pressure**, {eq}`eq-p14-gradient-p`, with the exponent $5.2586$:
   $$
   \begin{aligned}
   p &= p_1 \left(\frac{T}{T_1}\right)^{5.2586}\\
     &= 101{,}325\\
     &\;\;\; \times {0.763152}^{5.2586}\\
     &= 101{,}325 \times 0.24138\\
     &= 24{,}458\ \text{Pa}
   \end{aligned}
   $$
5. **Density**, {eq}`eq-p14-gradient-rho`, with the exponent $4.2586$:
   $$
   \begin{aligned}
   \rho &= \rho_1 \left(\frac{T}{T_1}\right)^{4.2586}\\
        &= 1.2250 \times {0.763152}^{4.2586}\\
        &= 1.2250 \times 0.31629\\
        &= 0.3875\ \text{kg/m}^3
   \end{aligned}
   $$

**Check.** The equation of state gives $\rho = 24{,}458/(287 \times 219.91) = 0.3875$ kg/m³, the same to four figures. The jet flies in air with 32% of the sea-level density.

### Worked example 2: a weather balloon in the isothermal layer

A weather balloon carries a radiosonde, a small instrument package, up through $h = 21{,}000$ m. Find the temperature, pressure, and density there. {numref}`fig-p14-example-ladder` draws the path of the calculation.

1. **Layer.** Because 21,000 m lies between 11,000 m and 25,000 m, we are in the isothermal layer at $T = 216.66$ K. Its base is at $h_1 = 11{,}000$ m, so we need the values there first.
2. **Base values at 11,000 m**, from the troposphere. The temperature ratio is $216.66/288.16 = 0.751874$, and
   $$
   \begin{aligned}
   p_1 &= 101{,}325\\
       &\;\;\; \times {0.751874}^{5.2586}\\
       &= 101{,}325 \times 0.22320\\
       &= 22{,}616\ \text{Pa}\\
   \rho_1 &= 1.2250\\
       &\;\;\; \times {0.751874}^{4.2586}\\
       &= 1.2250 \times 0.29686\\
       &= 0.3637\ \text{kg/m}^3
   \end{aligned}
   $$

   The table lists 0.3636, computed with the unrounded exponent. Either value gives the answers below to three figures.
3. **Exponent** of {eq}`eq-p14-isothermal`:
   $$
   \begin{aligned}
   &\frac{g_0\,(h - h_1)}{R T}\\
   &\;\;\;= \frac{9.81 \times 10{,}000}{287 \times 216.66}\\
   &\;\;\;= 1.5776
   \end{aligned}
   $$
4. **Pressure and density.** The factor is $\exp(-1.5776) = 0.20647$, and
   $$
   \begin{aligned}
   p &= 22{,}616 \times 0.20647\\
     &= 4{,}670\ \text{Pa}\\
   \rho &= 0.3637 \times 0.20647\\
        &= 0.07509\ \text{kg/m}^3
   \end{aligned}
   $$

**Check.** $p/(\rho R T) = 4{,}670/(0.07509 \times 287 \times 216.66) = 1.000$. At 21 km the pressure is 4.6% of its sea-level value. Since the pressure at a level is the weight of the air above it, the balloon has risen above 95.4% of the mass of the atmosphere.

:::{figure} figures/p14-example-ladder.svg
:label: fig-p14-example-ladder
:alt: On the left, temperature against altitude from 0 to 22 kilometers, with points at sea level (288.16 K), at 11 kilometers (216.66 K), and at 21 kilometers (216.66 K). On the right, three boxes at the same heights. Sea level: T 288.16 K, p 101,325 Pa, rho 1.2250. Base of the isothermal layer at 11,000 meters: T1 216.66 K, p1 22,616 Pa, rho1 0.3637. The balloon at 21,000 meters: T 216.66 K, p 4,670 Pa, rho 0.07509. An arrow from the first box to the second is labeled step 2, gradient-layer equations from sea level; an arrow from the second to the third is labeled steps 3 and 4, isothermal-layer equations from 11,000 meters.
:width: 85%

Computed for example 2. The calculation climbs in two stages, first to 11,000 m (step 2) and then to the balloon (steps 3 and 4).
:::

:::{warning} The isothermal layer starts at 11,000 m, not at sea level
If you use sea-level pressure and the full altitude in {eq}`eq-p14-isothermal`, $101{,}325\,\exp[-9.81 \times 21{,}000/(287 \times 216.66)]$, you get 3,689 Pa instead of 4,670 Pa. The equation of a layer applies only inside that layer, measured from its own base.
:::

### Worked example 3: altitude from a measured pressure

A glider climbing in rising air measures an outside pressure of $p = 61{,}500$ Pa. Find its altitude in the standard atmosphere and the temperature and density of the air there.

1. **Layer.** Because 61,500 Pa lies between 101,325 Pa (sea level) and 22,616 Pa (11,000 m), we are in the troposphere, with its base at sea level.
2. **Temperature**, from {eq}`eq-p14-gradient-p` solved for $T$. The pressure ratio is $61{,}500/101{,}325 = 0.60696$ and the exponent $-aR/g_0 = 0.0065 \times 287/9.81 = 0.19016$:
   $$
   \begin{aligned}
   T &= T_1 \left(\frac{p}{p_1}\right)^{-aR/g_0}\\
     &= 288.16 \times {0.60696}^{0.19016}\\
     &= 262.06\ \text{K}
   \end{aligned}
   $$
3. **Altitude**, from the temperature line:
   $$
   \begin{aligned}
   h &= h_1 + \frac{T - T_1}{a}\\
     &= \frac{262.06 - 288.16}{-0.0065}\\
     &= 4{,}015\ \text{m}
   \end{aligned}
   $$
4. **Density**, from the equation of state:
   $$
   \begin{aligned}
   \rho &= \frac{p}{R T} = \frac{61{,}500}{287 \times 262.06}\\
        &= 0.8177\ \text{kg/m}^3
   \end{aligned}
   $$

**Check.** Forward from the altitude found, step 4 of the method:

$$
\begin{aligned}
T &= 288.16 - 0.0065 \times 4{,}015\\
  &= 262.06\ \text{K}\\
p &= 101{,}325 \times \left(\frac{262.06}{288.16}\right)^{5.2586}\\
  &= 61{,}502\ \text{Pa}
\end{aligned}
$$

That is the measured 61,500 Pa to four figures. The point is the triangle on {numref}`fig-p14-pressure-density`.

**The same method in the isothermal layer.** A stratospheric airship, a powered lighter-than-air craft that maintains its station high above the weather, measures an outside pressure of $p = 9{,}500$ Pa. Find its altitude and the density of the air it floats in.

1. **Layer.** Because 9,500 Pa lies between 22,616 Pa (11,000 m) and 2,484 Pa (25,000 m), we are in the isothermal layer, with $T = 216.66$ K and its base at $h_1 = 11{,}000$ m.
2. **Altitude**, from {eq}`eq-p14-isothermal` solved for $h$ (step 3 of the method), with $R T_1/g_0 = 287 \times 216.66/9.81 = 6{,}339$ m:
   $$
   \begin{aligned}
   h &= h_1 + \frac{R T_1}{g_0}\,\ln\frac{p_1}{p}\\
     &= 11{,}000\\
     &\;\;\; + 6{,}339 \times \ln\frac{22{,}616}{9{,}500}\\
     &= 11{,}000\\
     &\;\;\; + 6{,}339 \times 0.86737\\
     &= 16{,}498\ \text{m}
   \end{aligned}
   $$
3. **Density.**
   $$
   \begin{aligned}
   \rho &= \frac{p}{R T} = \frac{9{,}500}{287 \times 216.66}\\
        &= 0.1528\ \text{kg/m}^3
   \end{aligned}
   $$

**Check.** Forward from the altitude found, 5,498 m above the base of the layer:

$$
\begin{aligned}
p &= 22{,}616\\
  &\;\;\; \times \exp\left(-\frac{9.81 \times 5{,}498}{287 \times 216.66}\right)\\
  &= 9{,}500\ \text{Pa}
\end{aligned}
$$

(p14-speed-of-sound)=
## Speed of sound and Mach number

A small pressure disturbance, such as the sound of an engine, travels through air at the {term}`speed of sound`. For a given ideal gas, acoustic wave speed depends on the ratio $p/\rho$; because the equation of state gives $p/\rho = R T$, pressure and density cancel out and the speed of sound depends on temperature alone:

:::{math}
:label: eq-p14-sound
a_s = \sqrt{\gamma R T}
:::

Here $\gamma$ is the ratio of specific heats, the heat needed to warm the gas by one kelvin at constant pressure divided by the heat needed at constant volume; $\gamma = 1.4$ for air. The subscript in $a_s$ keeps the speed of sound apart from the lapse rate $a$. At sea level,

$$
\begin{aligned}
a_s &= \sqrt{1.4 \times 287 \times 288.16}\\
    &= 340.3\ \text{m/s}
\end{aligned}
$$

and in the isothermal layer, at 216.66 K, $a_s = 295.0$ m/s.

:::{prf:definition} Mach number
:label: def-p14-mach
The **{term}`Mach number`** is the speed of a vehicle divided by the speed of sound in the air around it:

$$
M = \frac{V}{a_s}
$$

A flight is subsonic for $M < 1$, transonic near $M = 1$, supersonic for $M > 1$, and hypersonic above about $M = 5$ (NASA Glenn Research Center n.d.b).
:::

For the cargo jet of example 1, at 219.91 K,

$$
\begin{aligned}
a_s &= \sqrt{1.4 \times 287 \times 219.91}\\
    &= 297.3\ \text{m/s}
\end{aligned}
$$

Cruising at $M = 0.80$, its {term}`true airspeed`, its speed relative to the air around it, is

$$
\begin{aligned}
V &= M a_s = 0.80 \times 297.3\\
  &= 237.8\ \text{m/s}
\end{aligned}
$$

:::{warning} Use the local temperature
The speed of sound in $M = V/a_s$ is the one at the aircraft's altitude. If you use the sea-level value, 340.3 m/s, the cargo jet's speed at Mach 0.80 comes out as $0.80 \times 340.3 = 272.2$ m/s, 14% too high.
:::

## Another planet: Venus

Our derivations used only the equation of state, the hydrostatic equation, and a straight-line temperature model, and none of them is special to Earth. For another planet, we change the gas constant $R$, the gravity $g$, and the lapse rate $a$, and start from the surface values of that planet.

### Worked example 4: the lower atmosphere of Venus

Venus has a thick atmosphere of carbon dioxide (96.5%) with some nitrogen. The givens (Williams n.d.; ECSS 2008, Annex G.7.2):

- average surface temperature 737 K;
- surface pressure 92 bar, $9.2 \times {10}^{6}$ Pa;
- surface gravity (at the equator) 8.87 m/s²;
- molar mass of the atmosphere 43.45 kg/kmol (the fact sheet calls it the mean molecular weight);
- lapse rate about 8 to 9 K per kilometer in the lowest 32 km, taken as $a = -0.008$ K/m.

Find the temperature, pressure, and density 10 km above the surface.

1. **Gas constant.** $R = R_u/M = 8{,}314.5/43.45 = 191.36$ J/(kg K). Here $M$ is the molar mass, not the Mach number. As a check, the surface density from the equation of state is $9.2 \times {10}^{6}/(191.36 \times 737) = 65.2$ kg/m³, close to the measured value of about 65 kg/m³.
2. **Temperature.**
   $$
   \begin{aligned}
   T &= 737\\
     &\;\;\; + (-0.008)(10{,}000)\\
     &= 657\ \text{K}
   \end{aligned}
   $$
3. **Exponent.**
   $$
   \begin{aligned}
   -\frac{g}{a R} &= \frac{8.87}{0.008 \times 191.36}\\
                  &= 5.7941
   \end{aligned}
   $$
4. **Pressure.** The temperature ratio is $657/737 = 0.891452$, and ${0.891452}^{5.7941} = 0.51388$, so
   $$
   \begin{aligned}
   p &= 9.2 \times 0.51388\\
     &= 4.728\ \text{MPa}
   \end{aligned}
   $$
5. **Density.**
   $$
   \begin{aligned}
   \rho &= \frac{p}{R T} = \frac{4.728 \times {10}^{6}}{191.36 \times 657}\\
        &= 37.61\ \text{kg/m}^3
   \end{aligned}
   $$

**Check.** Even 10 km up, the pressure on Venus is 179 times the pressure at the same altitude on Earth, and the gas there is still hotter than a kitchen oven. {numref}`fig-p14-earth-venus` compares the two atmospheres at one scale. At pressures this high carbon dioxide is not quite an ideal gas, so the model is a first estimate, good to a few percent.

:::{figure} figures/p14-earth-venus.svg
:label: fig-p14-earth-venus
:alt: Two plots against altitude above the surface from 0 to 32 kilometers. Temperature: Earth's standard atmosphere falls from 288.16 K to 216.66 K at 11 kilometers and then changes little, while the Venus model falls in a straight dashed line from 737 K to 481 K, with example 4 marked at 10 kilometers and 657 K. Pressure on a logarithmic scale: Earth's falls from 101.3 kilopascals to 0.8658 kilopascals at 32 kilometers; the Venus curve starts at 9,200 kilopascals and is still at 776 kilopascals at 32 kilometers, with example 4 marked at 4,728 kilopascals.
:width: 75%

Computed from the same layer equations for Earth's standard atmosphere and for a model of the lowest 32 km of Venus. The form of the curves is the same; only the constants differ. At 32 km the Venus pressure, 776 kPa, is still 7.7 times Earth's sea-level pressure. Venus surface values from Williams (n.d.), lapse rate from ECSS (2008).
:::

(p14-nonstandard)=
## A non-standard day

A real day can be tens of kelvin warmer or colder than standard. A simple model shifts the whole temperature profile by a constant $\Delta T$ and keeps the standard sea-level pressure. We then apply the same layer equations from $T_1 = 288.16 + \Delta T$. Designers use such days to check takeoff from hot airports.

Suppose an airport is located at 1,800 m on a day 20 K hotter than standard. The sea-level temperature of that day is 308.16 K, and at the airport

$$
\begin{aligned}
T &= 308.16\\
  &\;\;\; + (-0.0065)(1{,}800)\\
  &= 296.46\ \text{K}\\
\frac{T}{T_1} &= \frac{296.46}{308.16} = 0.962033\\
p &= 101{,}325 \times {0.962033}^{5.2586}\\
  &= 101{,}325 \times 0.81584\\
  &= 82{,}665\ \text{Pa}\\
\rho &= \frac{82{,}665}{287 \times 296.46}\\
     &= 0.9716\ \text{kg/m}^3
\end{aligned}
$$

On a standard day the airport's air would be at 276.46 K, with a density of 1.027 kg/m³. The 20 K temperature increase lowers air density by 5.4%, reducing both wing lift and engine thrust at a given airspeed.

:::{prf:definition} Density altitude
:label: def-p14-density-altitude
The **density altitude** is the altitude in the standard atmosphere at which the density equals the actual density. An aircraft performs as it would at its density altitude on a standard day (FAA 2023, Chapter 11).
:::

To find it, we use the reverse method with the density exponent: $1/4.2586 = 0.23482$, the ratio $0.9716/1.2250 = 0.79314$, and

$$
\begin{aligned}
T &= 288.16 \times {0.79314}^{0.23482}\\
  &= 272.897\ \text{K}\\
h &= \frac{272.897 - 288.16}{-0.0065}\\
  &= 2{,}348\ \text{m}
\end{aligned}
$$

So the aircraft at this airport performs as if it were 548 m higher ({numref}`fig-p14-hot-day`).

:::{figure} figures/p14-hot-day.svg
:label: fig-p14-hot-day
:alt: Two plots against altitude from 0 to 4,000 meters, with a dashed line across both at the airport elevation, 1,800 meters. Temperature: the hot-day line runs parallel to the standard line, 20 K warmer at every altitude. Density: the hot-day curve lies to the left of the standard curve. At the airport the standard density is 1.027 and the hot-day density 0.9716 kilograms per cubic meter; a vertical dotted line from the hot-day point rises at that density to the standard curve, which it meets at the density altitude, 2,348 meters.
:width: 80%

Computed for a day 20 K hotter than standard, with the standard sea-level pressure. The warmer air is less dense at every altitude. At an airport at 1,800 m its density equals the standard density at 2,348 m, which is the airport's density altitude.
:::

## Summary

:::{important} Summary
- The equation of state, $p = \rho R T$, links pressure, density, and temperature, with $T$ in kelvin and $R = 287$ J/(kg K) for air.
- The hydrostatic equation, $dp = -\rho g_0\,dh$, comes from the force balance on a slab of still air. Combined with the equation of state it gives $dp/p = -g_0\,dh/(RT)$, which integrates to an exponential in an isothermal layer and to a power of $T/T_1$ in a gradient layer.
- Every layer starts from its own base values, carried up from sea level; above 11,000 m the base is not sea level. The reverse method finds the altitude from a measured pressure or density.
- The speed of sound, $a_s = \sqrt{\gamma R T}$, depends on temperature only, and $M = V/a_s$. Another planet, or a hot day, needs only new constants or a shifted temperature profile.
:::

:::{table} The equations of this page.
:label: tbl-p14-equations
:align: center

| Quantity | Equation |
| --- | --- |
| Equation of state ($T$ in K) | $p = \rho R T$ |
| Hydrostatic equation | $dp = -\rho\,g_0\,dh$ |
| Temperature in a gradient layer ($a$ in K/m, with its sign) | $T = T_1 + a\,(h - h_1)$ |
| Pressure in a gradient layer | $p/p_1 = (T/T_1)^{-g_0/(aR)}$ |
| Density in a gradient layer | $\rho/\rho_1 = (T/T_1)^{-(g_0/(aR) + 1)}$ |
| Pressure and density in an isothermal layer | $p/p_1 = \rho/\rho_1 = \exp[-g_0 (h - h_1)/(R T)]$ |
| Speed of sound and Mach number | $a_s = \sqrt{\gamma R T}$, $M = V/a_s$ |

:::

:::{exercise} For discussion
:label: ex-p14-discussion

1. Why does the pressure fall with altitude even in a layer where the temperature does not change?
2. In the troposphere the density falls more slowly than the pressure with altitude (exponent 4.2586 against 5.2586). What does the falling temperature do to the density, through the equation of state?
3. Why does an engineer designing a high-altitude balloon rely more on the isothermal-layer equations than on the troposphere equations?
4. Two airports lie at the same elevation, one in a desert and one by a cold sea. Which has the higher density altitude in summer, and what does that mean for the runway an aircraft needs?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-1-4.html
:label: quiz-1-4
:enumerated: false
:width: 100%

Quiz for Standard 1.4: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill, 2016.
- European Cooperation for Space Standardization (ECSS), *Space Engineering: Space Environment*, ECSS-E-ST-10-04C, ESA, 2008. Annex G.7.2, Venus, as reproduced by the [SPENVIS ECSS pages](https://spenvis.oma.be/ecss/e_st_10_04c/ecss_18_07_02.htm).
- Federal Aviation Administration (FAA), *[Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-25C.pdf)*, FAA-H-8083-25C, 2023.
- NASA Glenn Research Center, "[Earth Atmosphere Model, Metric Units](https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html)," Beginner's Guide to Aeronautics, n.d.a.
- NASA Glenn Research Center, "[Mach Number](https://www.grc.nasa.gov/www/k-12/airplane/mach.html)," Beginner's Guide to Aeronautics, n.d.b.
- National Institute of Standards and Technology (NIST), "[Boltzmann constant](https://physics.nist.gov/cgi-bin/cuu/Value?k)," CODATA values of the fundamental constants, n.d.
- NOAA, NASA, and U.S. Air Force, *[U.S. Standard Atmosphere, 1976](https://ntrs.nasa.gov/citations/19770009539)*, NOAA-S/T 76-1562, NASA-TM-X-74335, 1976. Foreword (the WMO definition), Part 1 (constants and layers, Table 4).
- Salawitch, R. J., McBride, L. A., Thompson, C. R., Fleming, E. L., McKenzie, R. L., Rosenlof, K. H., Doherty, S. J., and Fahey, D. W., *[Twenty Questions and Answers About the Ozone Layer: 2022 Update](https://csl.noaa.gov/assessments/ozone/2022/twentyquestions/)*, Scientific Assessment of Ozone Depletion: 2022, World Meteorological Organization, Geneva, 2023. Question Q2.
- Williams, D. R., "[Venus Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html)," NASA Space Science Data Coordinated Archive, n.d.

