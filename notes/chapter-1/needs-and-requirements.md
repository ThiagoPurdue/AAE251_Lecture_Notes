---
title: "1.1 Needs and Requirements"
short_title: 1.1 Needs and Requirements
---

:::{include} ../_parts/standards/1.1.md
:::

Every aerospace vehicle starts as a problem someone wants solved. On this page we follow that problem from the people who care about it to a list of numbers an engineer can design to and check. We start with what a {term}`system` is and who its {term}`stakeholders <stakeholder>` are. Then we write a {term}`mission statement` and {term}`need statements <need statement>`, rank the needs, and turn them into {term}`requirements <requirement>` that are complete, dependent, and verifiable. The word "traceable" in the standard means that every requirement traces to a need (see [traceability](#p11-traceability)). One example runs through the page: an aircraft for aerial survey. It flies a camera back and forth over farmland or forest so that a mapping company can make maps from the photographs.

:::{note} What to take from this page
- A system is defined by its function, its inputs and outputs, its boundary, and its form. Its stakeholders are everyone it affects, and they are the source of its needs.
- A mission statement and a need statement say what is wanted in the stakeholders' terms and never name a design.
- A requirement is a metric and a value, with the reason kept beside it. A good set of requirements is complete, dependent (it names results, not designs), and verifiable.
- Every requirement traces to a need, every need traces to at least one requirement, and each requirement is verified by analysis, inspection, demonstration, or test, recorded in a {term}`compliance table`.
:::

We work in six steps, shown in {numref}`fig-p11-road-map`. Steps 1 to 4 describe the problem in the stakeholders' own terms. Steps 5 and 6 turn it into numbers we can hold a design to.

:::{figure} figures/p11-road-map.svg
:label: fig-p11-road-map
:alt: Flow chart of six numbered steps from top to bottom: 1 identify the stakeholders, 2 write the mission statement, 3 write the need statements, 4 rank the needs, 5 write the requirements and trace them to needs, and 6 verify each requirement and record it in a compliance table. A brace groups steps 1 to 4 as needs, what the stakeholders want in their terms, and a second brace groups steps 5 and 6 as requirements, what the system must do in numbers that can be checked.
:width: 75%

Schematic of the path from stakeholders to verified requirements. The first four steps find out what people want; the last two turn it into numbers a design can be checked against. Each step has a section on this page.
:::

## What a system is

Engineers use the word system for anything built to do a job, from a fuel pump to an airline fleet. In these notes we use the definition of the U.S. Defense Acquisition University (2001), in plain words:

:::{prf:definition} System
:label: def-p11-system

A **system** is a set of people, products, and processes that work together as one whole to provide a capability that meets a stated need or objective.
:::

A system exists because someone needs what it does. We can describe it in four ways, and a full description uses all four:

- **Function:** what the system does, said with a verb. An airliner carries passengers and their bags between airports.
- **Inputs and outputs:** what crosses into the system and what comes out of it. Fuel, passengers, and the crew's commands go in. Passengers at their destination, exhaust gas, and noise come out.
- **Boundary:** the line that separates the system from everything else. We design what lies inside. What lies outside, the environment, we accept as it is. Airports, air traffic control, and the weather are outside an airliner's boundary.
- **Form:** what the system physically is, with its shape, size, and parts.

{numref}`fig-p11-system-boundary` applies all four to one aircraft, the Boeing 737-800.

:::{figure} figures/p11-system-boundary.svg
:label: fig-p11-system-boundary
:alt: The outline of a Boeing 737-800 seen from above, nose to the left, inside a dashed rounded rectangle labeled boundary. Above it the function reads: carries passengers and their bags between airports. Below it the form reads: twin-engine jet, 39.47 meters long, 35.79 meters span with winglets, 160 seats. Three input arrows from the left reach the boundary: fuel, passengers and bags, and crew commands. Two output arrows leave it to the right: passengers and bags at the destination, and exhaust gas and noise. A line at the bottom says airports, air traffic control, and weather lie outside the boundary.
:width: 90%

Schematic of one aircraft described four ways: function, inputs and outputs, boundary, and form. Only the form says what the aircraft looks like; the other three would fit other designs too. Outline after the Boeing 737-800 (Boeing 2025).
:::

The 737-800 is 39.47 m long and seats 160 passengers in a two-class cabin. It spans 35.79 m with its winglets, the upturned wing tips, and 34.32 m without them (Boeing 2025, Sections 2.1.3 and 2.2.6). Those numbers are form. We can write the other three before the form exists, so they come first in design.

Where the boundary goes is a choice. For an airline, the aircraft is one part of a larger system that also holds its crews, its maintenance base, and its schedule. For an engine maker, the engine is the system and the aircraft is its environment. So say where the boundary is before you decide what the system must do.

:::{warning} Describing a system by its form alone
"A twin-engine jet with 160 seats" says what the aircraft is and nothing about what it is for. A description that starts with the form has already chosen the design. Start with the function, the inputs and outputs, and the boundary.
:::

## Stakeholders

Once we know where the system ends, step 1 is to find everyone it affects.

:::{prf:definition} Stakeholder
:label: def-p11-stakeholder

A **stakeholder** is a group or individual that is affected by a system or has a stake in it (NASA 2016, Section 4.1.1.2.1). One stakeholder is always the customer, who pays for the system.
:::

The stakeholders give us the needs and the {term}`constraints <constraint>`. A constraint is a limit the designers must respect but did not choose, such as a noise rule set by a regulator. Stakeholders differ in how close they stand to the product. Alexander (2005) draws them as the layers of an onion. The product is in the middle. Around it are the people who operate it, then the people who buy it or benefit from it. On the outside is everyone else it touches, such as regulators, developers, and neighbors. {numref}`fig-p11-stakeholders` places the stakeholders of the Boeing 787 this way.

:::{figure} figures/p11-stakeholders.svg
:label: fig-p11-stakeholders
:alt: Nested boxes with the Boeing 787, the product, in the middle. The first layer, operate it, holds pilots and mechanics. The second layer, buy it or ride in it, holds the airline and the passengers. The outer layer, regulate it, build it, or live near it, holds the FAA, Boeing, and airport neighbors.
:width: 90%

Schematic of the stakeholders of one airliner, from those who operate it to those who only live near its airports. Every layer has needs; the outer ones are the easiest to forget. After the onion model of Alexander (2005).
:::

{numref}`tbl-p11-roles` lists common stakeholder roles, each with its own view of the same aircraft.

:::{table} Common stakeholder roles, with an example for the Boeing 787 and what that stakeholder cares about.
:label: tbl-p11-roles
:align: center

| Role | Example for the 787 | What they care about |
| --- | --- | --- |
| Customer (owner) | The airline that buys it | Fuel burn, range, seats, price |
| Operator (user) | Pilots and cabin crew | Workload, handling like the aircraft they know |
| Maintainer | The airline's mechanics | Access to parts, time to repair |
| Beneficiary | Passengers | Safety, comfort, a reliable schedule |
| Developer | Boeing and its suppliers | A product that sells and can be built at a profit |
| Regulator | The Federal Aviation Administration (FAA) | Safety, noise, and emissions rules |
| The public | People who live near airports | Noise |
| Competitor | Other aircraft makers | Where the 787 leaves room for their products |
:::

For our survey aircraft, the stakeholders are:

- the owner, a survey and mapping company that buys the aircraft and sells maps made from its photographs (the owner pays, so the owner is the customer);
- the pilot who flies the survey lines;
- the data customer, such as a county planning office that buys the maps;
- the mechanics;
- the FAA;
- the people who live under the survey lines.

:::{warning} Forgetting the stakeholders who never touch the system
A list made only of buyers and users misses the regulator, the maintainers, and the neighbors. Their needs arrive anyway, later and at a higher cost, as a certification rule, a part nobody can reach, or a noise complaint.
:::

(p11-mission-statement)=
## The mission statement

With the stakeholders known, step 2 states their problem in one or two sentences. NASA (2016, Section 4.1.1.2.3) splits what stakeholders expect into needs, goals, and objectives. The need answers the question "What problem are we trying to solve?" and names no solution. Goals say what the system must do to meet the need. Objectives give the specific expectations under each goal. The mission statement holds the need, and often the main goal.

:::{prf:definition} Mission statement
:label: def-p11-mission-statement

A **mission statement** is a brief description of the capability a system will provide and the benefit it brings to its customer. It names no specific design, and it may state the assumptions and constraints that guide the work.
:::

An example: "An affordable, reliable attack vehicle that improves Air Force operations." You can guess that the vehicle will fly. The statement does not say whether it has a pilot, whether it is a fighter or a bomber, or how many engines it has. Those are design choices, and the mission statement leaves them open.

{numref}`fig-p11-mission-statement` shows two candidate statements for the survey aircraft. The left one describes an airplane. The right one says what the system does and why that matters to the customer.

:::{figure} figures/p11-mission-statement.svg
:label: fig-p11-mission-statement
:alt: Two panels compared row by row. The left panel, with a dashed frame, is titled names a solution, avoid. Its first row holds the statement a twin-engine, high-wing airplane with a camera hatch in the floor, braced as a design; its second and third rows read no capability stated and no benefit stated. The right panel, with a solid frame, is titled capability and benefit, use. Its three rows hold an affordable airborne survey system, braced as what it is; that photographs a whole county in one working day, braced as the capability; and so that mapping companies deliver accurate maps at low cost, braced as the benefit.
:width: 90%

Schematic of two mission statements for the survey aircraft, compared row by row. The left one has already chosen the engines, the wing position, and the camera hatch, and says nothing about what the system does or whom it serves; the right one states the capability and the benefit and leaves every design open.
:::

The first statement of a problem is often not the right one. The ARPANET, the network that grew into the Internet, was built so that researchers could share distant computers. Within a few years its largest use was electronic mail between the researchers themselves (Leiner et al. 1997). The real need was to connect people. So before you write the mission statement, ask the stakeholders what problem they are trying to solve, and check that the answer is not a solution in disguise.

:::{tip} A test for a mission statement
Name two designs that look nothing alike. If both could satisfy the statement, it names no solution. If only one could, rewrite it.
:::

## Need statements

Step 3 breaks the mission statement into what each stakeholder needs, one need per statement. The written list keeps the design focused on the people who will use the system. It also brings out needs nobody states aloud and gives the whole team one basis for the requirements.

The best source is the stakeholders themselves. We interview them in three parts:

1. **Before:** choose one person, learn their role, and prepare five or six open questions.
2. **During:** ask about real experience ("Tell me about the last time you..."). Ask what they need, not how to build it, and ask "why?" to dig deeper. Write down their own words. Do not argue, and do not sell your idea.
3. **After:** turn each statement into a need statement, and note who said it.

For the survey aircraft, we might ask a pilot: "What makes a survey day go badly?", "What do you do when the weather changes?", and "What part of the aircraft slows you down most on the ground?"

:::{prf:definition} Need statement
:label: def-p11-need-statement

A **need statement** is one sentence, written as an attribute of the system, that says what a stakeholder needs from it without saying how the system will provide it.
:::

Four guidelines turn what a stakeholder said into a need statement:

1. **What, not how.** State the problem, not a solution. A solution written as a need closes off every other design before the work begins.
2. **Be specific.** Keep the detail the stakeholder gave. If a passenger wants to keep a laptop bag under the seat, the need is that the bag fits under the seat, not that the seat area is "roomy."
3. **An attribute of the system.** Write from the point of view of the system being designed: "the aircraft fits the jet bridges at the airline's airports," not "the jet bridges can reach the aircraft."
4. **No "must," "shall," or "should."** These words suggest a level of importance, and it is too early to assign one. Importance comes from the ranking in step 4.

{numref}`tbl-p11-statements` applies the guidelines to statements an airline's people might make.

:::{table} From what a stakeholder says to a need statement. The second column breaks the guideline named in the last column; the third column follows it.
:label: tbl-p11-statements
:align: center

| What the stakeholder said | Weak need statement | Better need statement | Guideline |
| --- | --- | --- | --- |
| "Put bigger windows in the cabin." | The cabin has larger windows. | The cabin gives every seat a view outside. | What, not how |
| "My ears hurt on every descent." | The cabin is comfortable. | The cabin pressure changes slowly enough during descent to keep passengers' ears comfortable. | Be specific |
| "The gates at our airports never fit." | The jet bridges can reach the aircraft. | The aircraft fits the jet bridges at the airline's airports. | An attribute of the system |
| "You should let us change an engine overnight." | The engine should be easy to change. | An engine can be changed during one overnight stop. | No "should" |
:::

The interviews for the survey aircraft give five needs:

- N1: The aircraft stays over the survey area for a full working day.
- N2: The camera images are sharp in light turbulence.
- N3: The aircraft can use short rural airstrips.
- N4: The aircraft can be prepared and flown on a survey by one pilot without help.
- N5: The operating cost per survey hour is low.

For example, the pilot's complaint about blurred pictures became N2.

:::{warning} A solution written as a need
"The aircraft has a high wing" is a design. Ask why the stakeholder wants it. If the answer is "so the wing does not block the camera's view," the need is "The camera's view of the ground is clear of the aircraft." A low wing with the camera ahead of it meets that need too.
:::

## Ranking needs

Many needs pull the design in opposite directions. Step 4 ranks them, so that we know which one gives way when two conflict.

:::{tip} Method: ranking needs
1. Ask each stakeholder to rate every need from 1 (nice to have) to 5 (must have).
2. Average the ratings of each need with [](#eq-p11-average).
3. Rank the needs from the highest average to the lowest.
4. Break a tie by a rule stated in advance. In these notes we use the rating of the customer who pays. Asking the stakeholders again is another way.
:::

With $n$ stakeholders and $r_j$ the rating given by stakeholder $j$, the average rating of a need is

:::{math}
:label: eq-p11-average
r_\text{avg} = \frac{1}{n} \sum_{j=1}^{n} r_j
:::

### Worked example: ranking the survey aircraft's needs

Three stakeholders (the owner, the pilot, and the data customer) rated the five needs as in {numref}`tbl-p11-ratings`. The owner pays for the aircraft. Find the average rating of each need and rank the needs.

:::{table} Ratings of the survey aircraft's needs, from 1 (nice to have) to 5 (must have), with the average and the rank.
:label: tbl-p11-ratings
:align: center

<table>
<tr><th>Need</th><th class="num">Owner</th><th class="num">Pilot</th><th class="num">Data customer</th><th class="num">Average</th><th class="num">Rank</th></tr>
<tr><th scope="row">N1: The aircraft stays over the survey area for a full working day.</th><td class="num">5</td><td class="num">4</td><td class="num">5</td><td class="num">4.667</td><td class="num">1</td></tr>
<tr><th scope="row">N2: The camera images are sharp in light turbulence.</th><td class="num">4</td><td class="num">3</td><td class="num">5</td><td class="num">4.000</td><td class="num">3</td></tr>
<tr><th scope="row">N3: The aircraft can use short rural airstrips.</th><td class="num">3</td><td class="num">4</td><td class="num">2</td><td class="num">3.000</td><td class="num">5</td></tr>
<tr><th scope="row">N4: The aircraft can be prepared and flown on a survey by one pilot without help.</th><td class="num">4</td><td class="num">5</td><td class="num">2</td><td class="num">3.667</td><td class="num">4</td></tr>
<tr><th scope="row">N5: The operating cost per survey hour is low.</th><td class="num">5</td><td class="num">3</td><td class="num">4</td><td class="num">4.000</td><td class="num">2</td></tr>
</table>
:::

1. **Averages.** For N1, with $n = 3$, [](#eq-p11-average) gives
   $$
   \begin{aligned}
   r_\text{avg} &= \frac{5 + 4 + 5}{3}\\
                 &= \frac{14}{3}\\
                 &= 4.667
   \end{aligned}
   $$
   In the same way N2 gives $12/3 = 4.000$, N3 gives $9/3 = 3.000$, N4 gives $11/3 = 3.667$, and N5 gives $12/3 = 4.000$.
2. **Order.** From the highest average: N1 (4.667), then N2 and N5 (4.000 each), then N4 (3.667), then N3 (3.000).
3. **Tie.** N2 and N5 both average 4.000. The owner, who pays, rated N5 a 5 and N2 a 4, so N5 ranks 2 and N2 ranks 3.

**Check.** Each rank from 1 to 5 is used once, and N1, which every stakeholder rated 4 or 5, comes first. {numref}`fig-p11-needs-ranking` shows the result.

:::{figure} figures/p11-needs-ranking.svg
:label: fig-p11-needs-ranking
:alt: Dot plot of the five needs in rank order from the top, each named in words: 1 N1 full-day endurance, average 4.667; 2 N5 low operating cost, 4.000; 3 N2 sharp images, 4.000; 4 N4 single pilot, 3.667; 5 N3 short airstrips, 3.000. On each row a gray line runs from the lowest to the highest rating, with a circle for the owner above it, a square for the pilot on it, a triangle for the data customer below it, and a short heavy tick at the average. A bracket joins N5 and N2 with the note tie, the owner's rating decides. The line of N4 is the longest, from the data customer's 2 to the pilot's 5.
:width: 90%

Computed from the ratings of {numref}`tbl-p11-ratings`: the average and the spread of the ratings of each need. The spread is what the average hides: N4 averages 3.667, but the pilot rates it 5 and the data customer 2. The averages set the order, and the owner's higher rating of N5 breaks the tie at 4.000.
:::

A low rank does not delete a need. N3 still gets a requirement. It is only the first to give way when it conflicts with a need ranked above it.

(p11-requirements)=
## Requirements

The ranked needs say what matters, but in the stakeholders' language: "the aircraft is easy to fly," "the aircraft can land in poor visibility." They give an engineer little to design to. Step 5 turns each need into a requirement, which states in measurable terms what the system must do, still without saying how.

:::{prf:definition} Requirement
:label: def-p11-requirement

A **requirement** is a statement of what the system must do, made of a metric (the quantity that is measured) and a value (how much of it is required). Its reason is recorded beside it.
:::

"The aircraft is easy to fly" might become "the average time for a pilot to qualify on the aircraft is less than 200 hours." Even this leaves questions open: which pilots we average over, and what experience they start with. Writing the requirement brings those questions out early.

Many organizations write requirements with the word "shall." In NASA's usage, "shall" marks a requirement, "will" a statement of fact, and "should" a goal (NASA 2016, Appendix C.1).

{numref}`fig-p11-requirement-anatomy` takes apart a range requirement for an airliner. {term}`Range` is the distance the aircraft can fly on one load of fuel, given here in {term}`nautical miles <nautical mile>` (1 nmi = 1,852 m, the unit of air navigation).

:::{figure} figures/p11-requirement-anatomy.svg
:label: fig-p11-requirement-anatomy
:alt: Three boxes side by side under the headings metric, what is measured; value, how much; and reason, why that much. Metric: range with a full passenger load. Value: at least 3,000 nautical miles. Reason: Boston to Los Angeles is 2,264 nautical miles on a great circle; the rest covers winds, detours, and reserve fuel. Solid arrows lead from the metric and the value to a shaded box across the full width below: requirement, the range with a full passenger load is at least 3,000 nautical miles. A dashed line joins the reason to that box, labeled kept with the requirement, so the value can be checked later.
:width: 90%

Schematic of one requirement and its reason. A requirement is a metric plus a value, and its reason stays with it. Solid arrows: the two parts that make the requirement; dashed line: the reason kept beside it. Here the reason shows why the value is larger than the route: 2,264 nmi is the great-circle distance between the two airports' published positions, on a sphere of radius 6,371 km (FAA n.d.).
:::

The reason pays off later. Suppose someone asks whether we can cut the 3,000 nmi to save weight. The reason tells us what that would cost: the Boston to Los Angeles route. It also catches errors. The great-circle distance (the shortest path over Earth's surface) from Boston to Los Angeles is 2,264 nmi. A value of 6,000 nmi beside that reason would show that one of the two is wrong.

A good set of requirements has three qualities.

**Complete.** Together the requirements address every need. A need with no requirement will not be designed for. The traceability matrix of the next section checks this.

**Dependent.** A requirement names a result of the design, never the design itself. Think of a function $y = f(x)$. The designer chooses $x$, the inputs (materials, shapes, sizes). The system delivers $y$, the outputs (load carried, thrust, range). A requirement belongs on $y$, the dependent variable, which gives the quality its name. For example, the load an I-beam carries depends on its material, its depth, and its flange width. A requirement on the load leaves all three open. A requirement on the material fixes one of them and says nothing about the load. {numref}`fig-p11-dependent-requirement` shows the difference for a main landing gear.

:::{figure} figures/p11-dependent-requirement.svg
:label: fig-p11-dependent-requirement
:alt: Two panels. Left, titled names the design, avoid, in a dashed box: the requirement the main landing gear uses an oleo strut. A solid arrow leads to the oleo strut, allowed; dashed lines ending in a bar lead to the steel spring leg and the composite spring leg, ruled out. Right, titled names the result (dependent), use: the requirement the main landing gear absorbs a touchdown at 10 feet per second without damage. Solid arrows lead to all three designs, and all three are allowed.
:width: 90%

Schematic of two ways to state one need for the main landing gear. A requirement that names a design allows one answer; a requirement that names the result allows every design that delivers it. Solid arrows lead to the designs allowed; dashed lines ending in a bar, to those ruled out. Gear types after FAA (2023, Chapter 13).
:::

The 10 ft/s (3.05 m/s) is the descent rate that U.S. rules for transport aircraft use for landing loads (14 CFR 25.473). An oleo strut turns the energy of the touchdown into heat in a cylinder of oil and gas. A spring leg flexes (FAA 2023, Chapter 13). Either can be designed to absorb a 10 ft/s touchdown, and the requirement leaves that choice to the designer. Choosing among designs that meet the requirements is the job of a {term}`trade study`, the subject of [concept generation and trade studies](concepts-and-trade-studies.md).

**Verifiable.** We must be able to show, within the budget and the schedule, that the design meets the requirement. Words such as easy, sufficient, safe, flexible, user-friendly, maximize, and minimize cannot be verified (NASA 2016, Appendix C.4). Give the acceptable range with "at least," "at most," or "between," and do not make the range narrower than the need. A tight range looks precise and only adds cost.

:::{warning} An adjective in place of a value
"The aircraft has a long range" cannot be checked, because nothing says how long is long. "The range with a full passenger load is at least 3,000 nmi" can be checked by analysis now and by test later.
:::

Requirements also come from the environment the vehicle must survive. Each condition the design must withstand, such as icing or radiation, becomes a requirement with a metric and a value. The next page, [1.2 Hazards and Risk](hazards-and-risk.md), shows how to find these conditions and how to choose what to do about each one.

Ideally each need maps to one requirement. In practice one need often takes several. "An engine can be changed during one overnight stop" might become "time to change one engine, at most 8 h." That alone does not cover the need. The crew size, the tools, and the lifting equipment matter too, and each may need a requirement of its own.

### Worked example: requirements for the survey aircraft

Write a requirement for each of the five needs of {numref}`tbl-p11-ratings`. {numref}`fig-p11-statement-to-requirement` follows one need from the pilot's words to its requirement, and {numref}`tbl-p11-requirements` gives the whole set.

:::{figure} figures/p11-statement-to-requirement.svg
:label: fig-p11-statement-to-requirement
:alt: Three boxes from left to right joined by arrows. First, the pilot's words: on bumpy days half my pictures come out blurred. Second, need statement N2: the camera images are sharp in light turbulence. Third, requirement R2: image smear at survey speed in light turbulence is at most 0.5 pixel. Under each box a note: the customer statement is written down as said; the need statement says what, not how, as an attribute of the system; the requirement is a metric and a value that a test can check.
:width: 85%

Schematic of one line of the survey example, from what a stakeholder said to what a test can check. Each step keeps the meaning and changes the form: the words become an attribute of the system, then a number.
:::

The table uses three new terms. Endurance is the time the aircraft can stay in the air on one load of fuel. Image smear is the distance the image moves across the camera's sensor while the shutter is open, measured in pixels. Half a pixel or less keeps edges sharp to one pixel. The direct operating cost is the cost of flying one hour, counting fuel, maintenance, and crew.

:::{table} Requirements of the survey aircraft. Each traces to one need; N4 is covered by two requirements.
:label: tbl-p11-requirements
:align: center

| ID | Need | Metric | Value | Reason |
| --- | --- | --- | --- | --- |
| R1 | N1 | Endurance with the survey camera and full fuel | At least 6 h | A survey day is about 5 h over the area plus the flights to and from it |
| R2 | N2 | Image smear at survey speed in light turbulence | At most 0.5 pixel | The data customer's maps need edges sharp to one pixel |
| R3 | N3 | Takeoff distance from a dry grass strip at maximum weight | At most 600 m | The rural strips the owner uses are 600 m long or longer |
| R4 | N4 | Crew needed to fly a survey line and run the camera | At most one pilot | The owner pays for one crew seat per flight |
| R5 | N4 | Time for one person to install and secure the camera | At most 15 min | The pilot loads the camera alone before the first flight of the day |
| R6 | N5 | Direct operating cost per survey hour | At most 80% of the owner's present aircraft | Competitors set survey prices; a lower cost is the owner's margin |
:::

**Check.** Every row has a measurable metric and a value with a limit, no row names a wing, an engine, or a material, and every need appears in the second column.

(p11-traceability)=
## Traceability

The second half of step 5 ties each requirement to the need it serves. We call this link {term}`traceability`.

:::{prf:definition} Traceability
:label: def-p11-traceability

**Traceability** is the link from each requirement to the need it comes from, and from each need to the requirements that answer it. Traced both ways, it is called bidirectional (NASA 2016, Section 6.2).
:::

A traceability matrix shows the links at a glance. It has one row per need, one column per requirement, and a mark where a requirement answers a need. Two checks follow:

1. **Every row holds a mark.** A need with no requirement will be missed by the design. The set is not complete.
2. **Every column holds a mark.** A requirement that traces to no need has one of two causes. It may come from a need nobody wrote down, and we add that need. Or it is what NASA (2016, Section 6.2.1.2.3) calls gold plating, work nobody asked for, and we remove it.

{numref}`fig-p11-traceability-matrix` shows a first draft for the survey aircraft and the corrected matrix.

:::{figure} figures/p11-traceability-matrix.svg
:label: fig-p11-traceability-matrix
:alt: Two grids with needs N1 to N5 as rows. The draft grid, in a dashed frame titled draft, two errors, has requirements R1, R2, R4, R5, R6, and R7 as columns; row N3 is empty and shaded, and column R7, a high wing, is empty and shaded. The corrected grid, in a solid frame titled corrected, has R1 to R6: R1 marks N1, R2 marks N2, R3 marks N3, R4 and R5 both mark N4, and R6 marks N5, so every row and every column holds a mark.
:width: 85%

Schematic of the traceability matrix of the survey aircraft, before and after correction. The draft (dashed frame) misses the short-airstrip need (row N3 empty) and carries a design choice that answers no need (column R7 empty); the corrected matrix has a mark in every row and every column.
:::

In the draft, R7 says "the wing is mounted on top of the fuselage." No need asks for that, and it names a design, so we remove it. If a stakeholder does need the wing clear of the camera's view, we write that need down, and its requirement names the view. For the empty row N3 we add R3. Row N4 holds two marks, one need with two requirements. A requirement may also trace to two needs, and the matrix shows that too.

(p11-verification)=
## Verification

Step 6, {term}`verification`, shows that the design meets each requirement.

:::{prf:definition} Verification
:label: def-p11-verification

**Verification** is showing that a system meets its requirements: that it was built right. **Validation** is showing that it meets the stakeholders' needs: that the right system was built (NASA 2016, Section 5.0).
:::

A design can pass every verification and still fail {term}`validation` if a requirement was wrong. This is why we keep the reasons and the trace back to the needs. There are four ways to verify a requirement, listed in {numref}`tbl-p11-methods`.

:::{table} The four methods of verification (NASA 2016, Section 5.3.1.2.1), with an example of each.
:label: tbl-p11-methods
:align: center

| Method | What it means | Example |
| --- | --- | --- |
| Analysis | Predict the result with calculations or a model | Range from a fuel and performance calculation |
| Inspection | Look at the drawing or the hardware | Check that the "Remove Before Flight" flag is on the arming pin |
| Demonstration | Operate the system and observe, with few or no measurements | Show that the cargo door opens with one hand |
| Test | Operate the system under controlled conditions and measure | Measure engine thrust on a test stand |
:::

Test gives the most data and costs the most (NASA 2016, Section 5.3). Before any hardware exists, we only have analysis and the inspection of drawings. So a conceptual design verifies most of its requirements by analysis and says which test or demonstration will confirm each one later.

:::{prf:definition} Compliance table
:label: def-p11-compliance-table

A **compliance table** lists every requirement with the method that verifies it, where the evidence is, and whether the design meets it yet.
:::

{numref}`tbl-p11-compliance` is the compliance table of the survey aircraft at the end of its first design pass.

:::{table} Compliance table of the survey aircraft. The status is written in words.
:label: tbl-p11-compliance
:align: center

| ID | Requirement (short) | Method | Where it is shown | Status |
| --- | --- | --- | --- | --- |
| R1 | Endurance at least 6 h with the camera | Analysis | Endurance calculation | Meets |
| R2 | Image smear at most 0.5 pixel in light turbulence | Test | Flight over a ground target in light turbulence | Not yet shown |
| R3 | Takeoff from a 600 m grass strip | Analysis | Takeoff distance calculation | Not yet shown |
| R4 | At most one pilot, who flies the survey and runs the camera | Inspection now, demonstration later | Cockpit drawing: camera controls within the pilot's reach; then a pilot flies a survey line in a cockpit mock-up | Partly shown |
| R5 | One person installs the camera in at most 15 min | Demonstration | Trial with a full-size mock-up of the camera bay | Not yet shown |
| R6 | Operating cost at most 80% of the present aircraft | Analysis | Operating cost estimate | Not yet shown |
:::

Each "Not yet shown" or "Partly shown" is a task. The table grows with the design and tells you where the work stands.

:::{warning} "Meets" without evidence
A status of "Meets" with nothing in the "Where it is shown" column is only a claim. Every "Meets" points to a calculation, a drawing, a demonstration, or a test result.
:::

## Summary

:::{important} Summary
- Describe a system by its function, inputs and outputs, and boundary before its form; find every stakeholder, including those who never touch it.
- The mission statement and the need statements say what is wanted, in the stakeholders' terms, and name no design. Rank the needs by the average rating and break ties by a stated rule.
- A requirement is a metric and a value with its reason; the set is complete, dependent, and verifiable. The standard's "traceable" is the trace from every requirement to a need.
- Trace every requirement to a need and every need to a requirement, and verify each requirement by analysis, inspection, demonstration, or test in a compliance table.
:::

:::{table} The terms of this page.
:label: tbl-p11-terms
:align: center

| Term | What it is | Example from this page |
| --- | --- | --- |
| Stakeholder | Anyone affected by the system or with a stake in it | The survey company that owns the aircraft |
| Mission statement | Capability and benefit in a sentence, no design | An affordable airborne survey system that photographs a whole county in one working day |
| Need statement | One need, as an attribute of the system, no "should" | The camera images are sharp in light turbulence |
| Average rating | $r_\text{avg} = \frac{1}{n} \sum_{j=1}^{n} r_j$ | N1: 14/3 = 4.667 |
| Requirement | Metric and value, with a reason | Endurance with the survey camera: at least 6 h |
| Traceability | Every requirement to a need, every need to a requirement | R4 and R5 trace to N4 |
| Verification | Analysis, inspection, demonstration, or test | R2 verified by a flight test |
:::

:::{exercise} For discussion
:label: ex-p11-discussion

1. Write three need statements for a better system to clear snow and ice from the sidewalks of a large campus. Which stakeholders did you ask, or imagine asking?
2. Write three requirements for a vehicle that carries a crew of three to the International Space Station. For each one, check that it is dependent and verifiable, and give its reason.
3. List three ways to raise the thrust an engine delivers. Which of them would a dependent requirement name?
4. In {numref}`fig-p11-needs-ranking` the pilot and the data customer disagree about N4. What would you ask each of them before accepting the average?
5. Where would you draw the boundary of a satellite system: around the spacecraft alone, or around the spacecraft, the ground stations, and the launch? What changes in its inputs and outputs?
:::

## Quiz

:::{iframe} ../quickcheck/quiz-1-1.html
:label: quiz-1-1
:enumerated: false
:width: 100%

Quiz for Standard 1.1: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Alexander, I. F., "[A Taxonomy of Stakeholders: Human Roles in System Development](https://scenarioplus.org.uk/papers/stakeholder_taxonomy/stakeholder_taxonomy.htm)," *International Journal of Technology and Human Interaction*, Vol. 1, No. 1, 2005, pp. 23-59.
- Boeing Commercial Airplanes (Boeing), *[Next-Generation 737 Airplane Characteristics for Airport Planning](https://www.boeing.com/content/dam/boeing/v2/airports/acaps/737NG_REV_C.pdf)*, D6-58325-7 Rev C, 2025.
- Defense Acquisition University, *[Systems Engineering Fundamentals](https://ocw.mit.edu/courses/16-885j-aircraft-systems-engineering-fall-2005/6128a102c1a9b6dbd30f2fb18c12aa64_sefguide_01_01.pdf)*, Defense Acquisition University Press, 2001.
- Federal Aviation Administration (FAA), *[Aviation Maintenance Technician Handbook, Airframe](https://www.faa.gov/sites/faa.gov/files/FAA-H-8083-31B_Aviation_Maintenance_Technician_Handbook.pdf)*, FAA-H-8083-31B, 2023.
- Federal Aviation Administration (FAA), *Airport Master Record (FAA Form 5010-1)*, Boston Logan International (BOS) and Los Angeles International (LAX): airport reference points, n.d.
- Leiner, B. M., Cerf, V. G., Clark, D. D., Kahn, R. E., Kleinrock, L., Lynch, D. C., Postel, J., Roberts, L. G., and Wolff, S., "[Brief History of the Internet](https://www.internetsociety.org/internet/history-internet/brief-history-internet/)," Internet Society, 1997.
- NASA, *[NASA Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)*, NASA/SP-2016-6105 Rev 2, 2016.
- U.S. Code of Federal Regulations, Title 14, [Section 25.473](https://www.ecfr.gov/current/title-14/section-25.473), "Landing load conditions and assumptions."
