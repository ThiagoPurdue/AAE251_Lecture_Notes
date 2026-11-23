---
title: "Concept generation and trade studies"
short_title: Concepts and trade studies
---

Requirements say what a vehicle must do. They do not say what it looks like. Between the two lies a choice among designs that differ in kind: a conventional airplane or one that takes off vertically, a piston engine or electric motors. Here we make that choice in a way others can check. We generate several concepts without judging them, compare them in a weighted decision matrix, check whether the answer depends on the weights, and write the decision down. One example runs through the page: an uncrewed cargo aircraft that carries supplies between small islands. No course standard is assessed on this page.

:::{note} What to take from this page
- Generate concepts before judging them: list the functions, list several ways to do each, and combine one way per function into a concept.
- In a weighted decision matrix the criteria come from the requirements, the weights add up to 1 and are set before any scoring, and each concept's total is the sum of weight times score.
- A winner is trustworthy only if it survives a change of the weights. Find the weight at which the winner changes and report it.
- Record each decision in a trade-study log, with the options, the data, the result, and what would change it.
:::

## What a trade study is

A design starts as a {term}`concept`: a short description of how the vehicle will do its job, specific enough to estimate its weight, cost, and performance. (We make the first weight estimate of a concept with [aircraft sizing](#p16-iteration).) A turboprop airplane that lands on a runway is one concept for the island cargo aircraft. An electric aircraft that takes off vertically is another.

:::{prf:definition} Trade study
:label: def-p17-trade-study

A {term}`trade study` compares alternative ways to meet the same requirements, ranks them against criteria taken from those requirements, and drops the less promising ones (NASA 2016, Appendix B). The word "trade" is short for trade-off: no concept is best on every criterion, so the study shows what each choice gives up.
:::

The order of the steps ({numref}`fig-p17-trade-study-steps`) matters more than any formula on this page. We generate concepts first, so that the comparison has real alternatives. We set the weights before the scores, so that nobody can tune them toward a favorite. The check and the record come last, so that the decision can be defended and revisited.

:::{figure} figures/p17-trade-study-steps.svg
:label: fig-p17-trade-study-steps
:alt: A flow chart of seven numbered boxes from top to bottom joined by arrows. 1, generate concepts, one option per function. 2, pick the criteria from the requirements. 3, set the weights before scoring; they add up to 1. 4, score each concept from 1 to 5. 5, add up weight times score for each concept. 6, change the weights and watch the winner. 7, record the decision in the log. A brace on the right groups steps 2 to 6 as the decision matrix.
:width: 75%

Schematic of a trade study in seven steps. The weights are fixed in step 3, before any scoring, and the result is tested before it is recorded.
:::

## Generate concepts before judging them

The first concept that comes to mind is rarely the best one, and if we judge it at once, the search stops. So product designers keep the two activities apart: generate many concepts first, judge them later (Ulrich and Eppinger 2016, Chapter 7; Roemer 2006). One orderly way to generate them is the {term}`combination table`:

:::{tip} Method: generating concepts with a combination table
1. List the functions the vehicle must perform. Take them from the requirements: a requirement on the cargo load becomes the function "carry cargo."
2. For each function, list several ways to do it, without judging them yet.
3. Pick one option for each function. Each pick is a concept.
4. Keep at least three concepts that differ in their main options, not only in a detail.
:::

{numref}`fig-p17-combination-table` is the combination table of the island cargo aircraft. It has four functions with three options each, so it holds $3 \times 3 \times 3 \times 3 = 81$ combinations. Some make no sense, such as a sling load under a fixed wing that takes off from a runway. A few are worth a closer look, and some that look odd are real: a rotor with a runway takeoff is an autogyro. The traced path is one concept: a wing plus lift rotors, electric motors, vertical takeoff, and cargo inside the fuselage. This is a "lift-plus-cruise" aircraft: separate rotors lift it for a vertical takeoff and landing (VTOL), and a propeller and the wing carry it in cruise.

:::{figure} figures/p17-combination-table.svg
:label: fig-p17-combination-table
:alt: A table with four functions as rows (make lift, make thrust, take off, carry cargo) and three options per function as columns. Make lift: fixed wing, rotor, wing plus lift rotors. Make thrust: piston engine, turboprop, electric motors. Take off: runway, short strip, vertical. Carry cargo: inside fuselage, pod under wing, sling load. Arrows trace concept C through the shaded, bold cells: wing plus lift rotors, electric motors, vertical, and inside fuselage.
:width: 90%

Schematic of the combination table of the island cargo aircraft. A concept is one option for each function: concept C, an electric lift-plus-cruise VTOL, is traced through the table, and the other 80 paths are other concepts.
:::

We carry three concepts forward, chosen to differ in how they make thrust and how they take off ({numref}`tbl-p17-concepts`).

:::{table} The three concepts of the island cargo aircraft, one option per function.
:label: tbl-p17-concepts

| Concept | Make lift | Make thrust | Take off | Carry cargo |
| --- | --- | --- | --- | --- |
| A, twin piston, conventional | Fixed wing | Piston engine (two) | Runway | Inside fuselage |
| B, single turboprop, conventional | Fixed wing | Turboprop | Runway | Inside fuselage |
| C, electric lift-plus-cruise VTOL | Wing plus lift rotors | Electric motors | Vertical | Inside fuselage |
:::

If a concept cannot meet a must-have requirement at all, we drop it here, before any scoring, and the log says why. Scoring it would only add noise to the matrix (NASA 2016, Section 6.8.1.2.1; Goldberg et al. 1994, Section 2.1.3).

:::{warning} Three versions of one idea are not three concepts
Three conventional airplanes that differ only in wing span give the matrix nothing to decide. Make the concepts differ in their main options: how the vehicle makes lift, makes thrust, or takes off.
:::

(p17-decision-matrix)=
## The weighted decision matrix

We compare the concepts in a {term}`decision matrix`, which lists the criteria in rows and the concepts in columns (NASA 2016, Appendix B). A {term}`criterion` is a property on which we compare the concepts, taken from the [requirements](needs-and-requirements.md): payload and range, operating cost, runway length, and so on. Each criterion carries a {term}`weight <Weight of a criterion>`, a fraction that says how much it counts. Each concept gets a score from 1 (poor) to 5 (excellent) on each criterion, and its weighted total is

:::{math}
:label: eq-p17-weighted-total
\text{total}_j = \sum_{i=1}^{n} w_i\, s_{ij}, \qquad \sum_{i=1}^{n} w_i = 1
:::

where $n$ is the number of criteria, $w_i$ the weight of criterion $i$, and $s_{ij}$ the score of concept $j$ on criterion $i$. Because the weights add up to 1, the total is a weighted average of the scores and also lies between 1 and 5. The weight $w_i$ is a pure number. It has nothing to do with the weight of the aircraft.

:::{tip} Method: building the decision matrix (steps 2 to 6)
2. Pick four to six criteria from the requirements. Each must tell the concepts apart and must not measure the same thing as another criterion.
3. Give each criterion a weight. The weights add up to 1. Write down why, before scoring anything.
4. Score each concept from 1 to 5 on each criterion, with a reason or a number for every score.
5. Multiply each score by its weight and add the products for each concept ([](#eq-p17-weighted-total)).
6. Change the weights a little and see whether the winner changes.
:::

### Worked example: the island cargo aircraft

The five criteria and their weights come from the requirements of the cargo service. Payload and range count most, because the aircraft exists to move supplies between islands. {numref}`tbl-p17-decision-matrix` gives the scores. A score of 5 always means "best for the mission," so on a cost criterion 5 means the lowest cost, and on runway length 5 means the shortest runway.

:::{table} Weighted decision matrix of the island cargo aircraft. Each cell gives the score from 1 to 5 and, in parentheses, the weight times the score.
:label: tbl-p17-decision-matrix

<table>
<tr><th>Criterion</th><th class="num">Weight</th><th class="num">A, twin piston</th><th class="num">B, single turboprop</th><th class="num">C, electric VTOL</th></tr>
<tr><th scope="row">Payload and range</th><td class="num">0.30</td><td class="num">3 (0.90)</td><td class="num">5 (1.50)</td><td class="num">2 (0.60)</td></tr>
<tr><th scope="row">Operating cost</th><td class="num">0.25</td><td class="num">4 (1.00)</td><td class="num">3 (0.75)</td><td class="num">3 (0.75)</td></tr>
<tr><th scope="row">Runway length needed</th><td class="num">0.20</td><td class="num">2 (0.40)</td><td class="num">2 (0.40)</td><td class="num">5 (1.00)</td></tr>
<tr><th scope="row">Technical risk</th><td class="num">0.15</td><td class="num">5 (0.75)</td><td class="num">4 (0.60)</td><td class="num">2 (0.30)</td></tr>
<tr><th scope="row">Noise near villages</th><td class="num">0.10</td><td class="num">2 (0.20)</td><td class="num">2 (0.20)</td><td class="num">4 (0.40)</td></tr>
<tr><th scope="row">Weighted total</th><td class="num">1.00</td><td class="num">3.25</td><td class="num">3.45</td><td class="num">3.05</td></tr>
</table>
:::

The reasons behind the scores, in short:

- **Payload and range.** A battery stores much less energy per kilogram than fuel, so C carries the least over the same distance. A turbine is light for its power, so B carries the most.
- **Operating cost.** Piston engines cost less to buy and to overhaul than a turbine. C saves on energy but must replace its batteries.
- **Runway length.** A and B need a runway; C needs only a landing pad.
- **Technical risk.** Piston twins and turboprops have flown for decades. Electric lift rotors are new, with few in service.
- **Noise.** Electric motors are quieter than engines, although the lift rotors still make noise at takeoff.

For concept B, [](#eq-p17-weighted-total) gives

$$
\begin{aligned}
\text{total}_\text{B} &= 0.30 \times 5 + 0.25 \times 3\\
&\;\; + 0.20 \times 2 + 0.15 \times 4\\
&\;\; + 0.10 \times 2\\
&= 1.50 + 0.75 + 0.40\\
&\;\; + 0.60 + 0.20\\
&= 3.45
\end{aligned}
$$

The same sum gives 3.25 for A and 3.05 for C, so B wins. As a check, every total lies between the lowest and highest score of its column, as a weighted average must. {numref}`fig-p17-weighted-totals` shows where each total comes from.

:::{figure} figures/p17-weighted-totals.svg
:label: fig-p17-weighted-totals
:alt: Three stacked bars, one per concept, each built from five segments in the same order from the bottom: payload and range (weight 0.30), shaded gold, then operating cost (0.25), runway length needed (0.20), technical risk (0.15), and noise near villages (0.10) in white and grays. Each segment shows the weight times the score. A, twin piston: 0.90, 1.00, 0.40, 0.75, 0.20, total 3.25. B, single turboprop: 1.50, 0.75, 0.40, 0.60, 0.20, total 3.45, the highest. C, electric VTOL: 0.60, 0.75, 1.00, 0.30, 0.40, total 3.05. B's payload and range segment, 1.50, drawn with a heavy outline, is the largest of the chart.
:width: 85%

Computed from {numref}`tbl-p17-decision-matrix`, with payload and range the bottom segment of every bar. B wins because it scores 5 on payload and range, the criterion with the largest weight, worth 1.50 (heavy outline). C's top score on runway length adds 1.00, but its low scores on payload and on technical risk cost it more.
:::

:::{warning} Weights set after scoring steer the answer
Once the scores are on the table, it is tempting to raise the weight of the criterion where your favorite concept does well. Fix the weights first and write down the reason for each. NASA's decision report records the rationale for the weights in its own section, ahead of the rationale for the scores (NASA 2016, Table 6.8-1).
:::

:::{warning} One property counted twice
Two criteria that measure the same thing, such as "range" and "fuel needed for the trip," count one property twice and tilt the result. Each criterion should be independent of the others (Goldberg et al. 1994, Section 2.1.3).
:::

## Checking the result: sensitivity to the weights

The weights are judgments, so the winner should not depend on a small change in one of them. A {term}`sensitivity check` changes one weight, scales the others so that all of them still add up to 1, and recomputes the totals.

Suppose criterion $k$ has the weight $w_k$, and we change it to $w_k'$. To keep the sum at 1, we multiply every other weight by the same factor:

:::{math}
:label: eq-p17-rescale
f = \frac{1 - w_k'}{1 - w_k}
:::

The other weights add up to $1 - w_k$ before the change, so after it they add up to $f\,(1 - w_k) = 1 - w_k'$, and the total is 1 again. We call $r_j = \text{total}_j - w_k s_{kj}$ the part of concept $j$'s total that does not come from criterion $k$. It is scaled by the same factor, so the new total is

:::{math}
:label: eq-p17-new-total
\text{total}_j' = w_k' s_{kj} + f\, r_j
:::

### Worked example: a larger weight on runway length

We raise the runway weight from 0.20 to 0.35 (criterion $k$ is runway length).

1. **Rest of each total.** Without the runway part: $r_\text{A} = 3.25 - 0.40 = 2.85$, $r_\text{B} = 3.45 - 0.40 = 3.05$, and $r_\text{C} = 3.05 - 1.00 = 2.05$.
2. **Scaling factor**, [](#eq-p17-rescale): $f = 0.65/0.80 = 0.8125$.
3. **New totals**, [](#eq-p17-new-total):
   $$
   \begin{aligned}
   \text{total}_\text{A}' &= 0.35 \times 2\\
                            &\;\; + 0.8125 \times 2.85\\
                            &= 0.70 + 2.316\\
                            &= 3.016
   \end{aligned}
   $$
   $$
   \begin{aligned}
   \text{total}_\text{B}' &= 0.35 \times 2\\
                            &\;\; + 0.8125 \times 3.05\\
                            &= 0.70 + 2.478\\
                            &= 3.178
   \end{aligned}
   $$
   $$
   \begin{aligned}
   \text{total}_\text{C}' &= 0.35 \times 5\\
                            &\;\; + 0.8125 \times 2.05\\
                            &= 1.75 + 1.666\\
                            &= 3.416
   \end{aligned}
   $$
4. **Tie weight.** We write $w$ for the new runway weight $w_k'$. Each new total is a straight line in $w$, and B and C tie at the weight $w_k^{*}$ where their two lines cross:
   $$
   \begin{aligned}
   \text{B:}\quad &2w + (1 - w)\,\frac{3.05}{0.80}\\
   \text{C:}\quad &5w + (1 - w)\,\frac{2.05}{0.80}
   \end{aligned}
   $$
   We set the two equal, move the $(1 - w)$ terms to the left and the $w$ terms to the right, then multiply by 0.80 and solve for $w$:
   $$
   \begin{aligned}
   (1 - w)\,\frac{1.00}{0.80} &= 3w\\
   1.00 - 1.00\,w &= 2.40\,w\\
   w_k^{*} &= \frac{1.00}{3.40}\\
           &= 0.2941
   \end{aligned}
   $$

**Check.** The new weights still add up to 1: $0.35 + 0.8125 \times 0.80 = 1.000$. At $w_k^{*}$ both totals equal 3.279.

At 0.35, C wins. {numref}`fig-p17-weight-sensitivity` draws all three lines. Any runway weight below 0.2941 keeps B ahead, and any weight above it puts C ahead. The margin is only $0.2941 - 0.20 = 0.094$, less than half the weight already given to runway length. Concept A never wins: it has the same runway score as B and a smaller $r$, so its line stays below B's.

:::{figure} figures/p17-weight-sensitivity.svg
:label: fig-p17-weight-sensitivity
:alt: A plot of weighted total against the new weight of the runway criterion, w k prime, from 0 to 0.6, with the other weights scaled so that all add up to 1. Three straight lines. B, single turboprop, dashed, falls as the runway weight grows. A, twin piston, solid, falls too and stays below B. C, electric VTOL, dotted, rises steeply. At the weight set first, 0.20, B leads with 3.45. B and C cross at the tie weight w k star, 0.2941, where the winner changes. At the check weight 0.35, C leads with 3.416.
:width: 75%

Computed from {numref}`tbl-p17-decision-matrix` with [](#eq-p17-new-total), the other four weights scaled to keep the sum at 1. The winner changes from B to C when the runway weight passes the tie weight, 0.2941, not far above the 0.20 set first.
:::

We test the scores the same way. The gap between B and A is $3.45 - 3.25 = 0.20$, smaller than the 0.25 that one step on the operating-cost score is worth. If B's operating cost were scored 2 instead of 3, B's total would fall to 3.20 and A would win. NASA's handbook asks that a recommendation say whether such changes could reverse the ranking, and that closely ranked alternatives be reported together (NASA 2016, Section 6.8.1.2.5). For the island aircraft, the fair result is B, by a small margin over A, and C if a short runway matters more than the weights say. Scores from 1 to 5 are judgments, so totals this close call for better data before the choice is final (Goldberg et al. 1994, Section 2.1.3). Here that means the operating cost and the runways of the islands.

## The trade-study log

A decision that is not written down gets argued again later, often by people who do not know why it was made. A {term}`trade-study log` keeps one entry per decision. {numref}`tbl-p17-log` shows the entry for the island cargo aircraft, with the fields that NASA's decision report asks for in short form (NASA 2016, Section 6.8.1.3 and Table 6.8-1).

:::{table} One entry of a trade-study log: the concept decision of the island cargo aircraft.
:label: tbl-p17-log

| Field | Entry |
| --- | --- |
| Decision | Choose the vehicle concept |
| Options considered | Twin piston, single turboprop, electric lift-plus-cruise VTOL |
| Criteria and data | The weighted decision matrix; weights set from the requirements before scoring |
| Result | Single turboprop (3.45); electric VTOL wins if the runway weight exceeds 0.2941 |
| What would change it | A customer requirement for vertical takeoff and landing |
| Who decided | The design group; the configuration engineer wrote the entry |
:::

The entry also carries the date of the decision. The line "what would change it" is the most useful one. When a requirement changes, a look through the log shows which decisions you must reopen.

## Summary

:::{important} Summary
- Generate concepts with a combination table, one option per function, and keep at least three that differ in their main options.
- Take the criteria from the requirements, set weights that add up to 1 before scoring, score from 1 to 5 with a reason, and add weight times score.
- Change one weight, scale the others, and find the weight at which the winner changes. A small margin is reported as a close result.
- Write each decision in the trade-study log, including what would change it.
:::

:::{table} The equations of this page.
:label: tbl-p17-equations

| Quantity | Equation |
| --- | --- |
| Weighted total of concept $j$ | $\text{total}_j = \sum_i w_i s_{ij}$, with $\sum_i w_i = 1$ |
| Scaling factor when weight $k$ changes | $f = (1 - w_k')/(1 - w_k)$ |
| New total | $\text{total}_j' = w_k' s_{kj} + f\, r_j$, with $r_j = \text{total}_j - w_k s_{kj}$ |

:::

:::{seealso} Further reading
Goldberg et al. (1994, Section 2.1) work a weighted trade study end to end, with the sensitivity step. Raymer (2006) has a chapter on sizing and trade studies for aircraft.
:::

:::{exercise} For discussion
:label: ex-p17-discussion

1. The island cargo aircraft must also be able to fly in strong crosswinds. Which criterion would you add, which weights would you lower to make room for it, and how might the ranking change?
2. Concept C wins at a runway weight of 0.35. What would you want to know about the islands before you accept a weight that high?
3. Why is it a mistake to score concepts first and choose the weights afterward, even when the people doing it are honest?
4. Name a combination in {numref}`fig-p17-combination-table` that makes no physical sense, and one that nobody would think of at first but might be worth a look.
5. Two concepts finish within 0.05 of each other. What would you do next, and what would you write in the log?
:::

## References

- Goldberg, B. E., Everhart, K., Stevens, R., Babbitt, N., Clemens, P., and Stout, L., *[System Engineering "Toolbox" for Design-Oriented Engineers](https://ntrs.nasa.gov/citations/19950012517)*, NASA Reference Publication 1358, NASA Marshall Space Flight Center, 1994. Section 2.1 (trade studies).
- NASA, *[NASA Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)*, NASA/SP-2016-6105 Rev 2, 2016.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 4th ed., AIAA, 2006.
- Roemer, T. A., "[Product Specifications and Concept Generation](https://ocw.mit.edu/courses/15-783j-product-design-and-development-spring-2006/resources/clas7_cncpt_genr/)," lecture notes, 15.783J Product Design and Development, MIT OpenCourseWare, 2006.
- Ulrich, K. T., and Eppinger, S. D., *Product Design and Development*, 6th ed., McGraw-Hill, 2016. Chapter 7 (concept generation) and Chapter 8 (concept selection).

