# Frequency-Report Scoring Rules — Project Context

The paper studies what a researcher can infer about a subject's latent multinomial beliefs from a single incentivized count report, treating the scoring-rule mechanism as the source of the identifying restriction. The framing is partial identification: each rule induces a set-valued map from report to beliefs, and the paper compares rules by the sharpness of the resulting identified sets.

## Language

**Frequency-report scoring rule**:
A scoring rule that incentivizes reporting a count vector \(r\) summarizing predicted outcomes over \(n\) trials in \(k\) categories.
_Avoid_: "frequency elicitation rule", "count scoring rule".

**Optimal-report correspondence** (\(R_S(p)\)):
The set of count reports a subject with latent beliefs \(p\) optimally chooses under scoring rule \(S\).
_Avoid_: "best-response set", "optimal reporting region".

**Identified set** (\(\Theta_S(r)\)):
The set of latent multinomial beliefs \(p\) consistent with an observed incentivized report \(r\) under rule \(S\); equivalently, \(\{p: r \in R_S(p)\}\). When ambiguity with classical sampling-based partial identification matters, refer to it as the **mechanism-induced identified set** — the identifying restriction is the optimal-report condition imposed by the scoring rule, not a sampling distribution.
_Avoid_: "inverse belief region" (legacy term from earlier drafts; retire in new text), "feasible belief set", "preimage".

**Headline rule**:
A scoring rule given primary attention in the paper. Three rules are headline: squared-distance, frequency-guessing, and Manhattan — each characterized in the scoring-rules section and each in the design comparison. Hamming and Chebyshev distance are *not* headline rules: their identified sets are exact but resist tractable sharp bounds, and the discussion takes them up as the boundary of the approach (ADR-0001, fourth amendment).
_Avoid_: "main rule", "central rule"; describing Hamming or Chebyshev as headline rules; any "four-rule" framing of the paper.

**Coordinate bound**:
The interval projection of the identified set onto a single coordinate \(p_j\); i.e., \([\min_{p \in \Theta_S(r)} p_j, \max_{p \in \Theta_S(r)} p_j]\).
_Avoid_: "marginal bound" (collides with marginal-distribution terminology), "per-category interval".

**Mean bound** (more generally, **linear-functional bound**):
The interval \([\min_{p \in \Theta_S(r)} \langle c, p \rangle, \max_{p \in \Theta_S(r)} \langle c, p \rangle]\) for a fixed coefficient vector \(c\). A mean bound is the special case \(c_j = j\) (or some category-indexed payoff).
_Avoid_: "expected-value bound" stated as a combination of coordinate intervals — that would not be sharp.

**Sharp bound**:
A coordinate or linear-functional bound that equals the exact infimum/supremum of the functional over the full identified set \(\Theta_S(r)\). "Sharp" is a substantive claim only for *bounds* — it contrasts with non-sharp bounds obtained by composing coordinate intervals, which discard the cross-coordinate dependence imposed by the simplex and the scoring rule. Closed-form sharp bounds (squared-distance, frequency-guessing) are proven analytical results; semi-analytical sharp bounds (Manhattan) are exact up to the inverse-binomial-CDF root-find tolerance and may be called sharp with that qualifier; computed bounds (Hamming, where feasible) are sharp only up to grid/optimization tolerance and must always state the tolerance.
_Avoid_: "sharp" applied to a computed bound without the tolerance qualifier; "sharp identified set" (see Flagged ambiguities).

**Informativeness**:
A criterion for comparing rules by the sharpness of their identified sets; depends on the inferential objective (coordinate width, worst coordinate width, mean-bound width, identified-set volume, etc.).
_Avoid_: "informational efficiency" (legacy term from earlier drafts; retire in new text), "statistical efficiency" (collides with Fisher-information usage), "elicitation efficiency".

**Analytical bound** (equivalently, **closed-form bound**):
A bound on a functional of the identified set (e.g., a coordinate or mean) derived in closed form from \(R_S\), without numerical search. Squared-distance and frequency-guessing coordinate bounds are analytical.
_Avoid_: "exact bound" (collides with the precision of numerical computation), "theoretical bound".

**Semi-analytical bound**:
A bound on a functional of the identified set that is exact and one-dimensional but not closed form — typically because evaluating the relevant inverse function (e.g., the inverse binomial CDF) is not elementary. Computed by a monotone scalar equation or one-dimensional root-find, sharp up to standard numerical tolerance. Manhattan coordinate and mean bounds are semi-analytical; they are exact in a way grid-based computational bounds are not.
_Avoid_: conflating with "computational bound" (the semi-analytical class is exact-one-dimensional, not grid-limited); conflating with "analytical bound" (no closed-form expression).

**Computational bound**:
A bound on a functional of the identified set obtained by solving a finite optimization, grid procedure, or simplex-wide enumeration to specified numerical tolerance. Hamming sharp bounds are computational where they are feasible at all (§5 records that they are intractable at the design grid's scale). The paper must never describe a computational bound as closed form, and must distinguish it from a semi-analytical bound (exact-one-dimensional, not grid-limited).
_Avoid_: "numerical bound" (acceptable but ambiguous with finite-sample sampling error), "approximate bound"; calling a Manhattan-type bound "computational" (it is semi-analytical).

**Average coordinate width**:
The headline coordinate-inference metric: the arithmetic mean over \(j=1,\dots,k\) of the width of the coordinate bound on \(p_j\). Reported per design cell and averaged across Dirichlet draws of \(p\).
_Avoid_: "mean coordinate width" (collides with mean-bound), "coordinate precision".

**Ordered-category-mean bound**:
The headline linear-functional metric: the width of the bound on \(\langle c, p\rangle\) with the canonical payoff vector \(c = (0,1,\dots,k-1)/(k-1)\) — i.e., the normalized category-index mean. Sup-over-simplex and random-\(c\) variants are reported in the appendix as robustness checks.
_Avoid_: "expected-value bound", "mean width" without further qualification.

**Cell-best regret**:
For a given design cell and metric, the gap between a rule's metric value and the minimum metric value attained by any of the three headline rules in that cell. Reported as the headline comparison display (heat-map by \((n, k, \alpha)\)); raw widths and win shares accompany it.
_Avoid_: "regret" without "cell-best" qualifier (ambiguous with decision-theoretic minimax regret).

**Win share**:
For a given metric and design cell, the fraction of Dirichlet draws on which a rule attains the minimum metric value. A one-row summary in the abstract / table; not the headline display.
_Avoid_: "winning probability" (collides with payment-probability discussion of the frequency-guessing rule).

**Risk neutrality** (maintained body assumption):
The maintained assumption in the body of the paper: the subject maximizes expected score. Under this assumption, the optimal-report correspondence \(R_S(p)\) and the identified set \(\Theta_S(r)\) take their simplest forms, and all headline analytical and computational results are stated. The assumption is relaxed in the discussion via the binary-lottery extension.
_Avoid_: equating "risk neutrality" with "expected utility" — the latter is the broader EU class, with risk neutrality as the linear-utility special case.

**Binary-lottery payment** (equivalently, **probabilistic payment scheme**):
A payment scheme under which the realized score is normalized to \([0,1]\) and the subject is paid a fixed prize with probability equal to the normalized score. Under expected utility, the subject's optimal report is the same as under risk neutrality — the binary-lottery extension is what makes the body's risk-neutral analysis carry through to risk-averse subjects. Referenced in the discussion, not the body. Cite Roth–Malouf (1979), Karni (2009), and an experimental treatment (Berg et al. 1986 or Selten et al. 1999).
_Avoid_: "BDM payment" (technically related but historically tied to valuation elicitation), "lottery payment" without "binary" (ambiguous), presenting binary-lottery payment as a maintained-body assumption.

**Direct monetary payment**:
A payment scheme under which the score is paid as money. Combined with risk neutrality, it suffices for the body's analysis. Combined with risk aversion, it breaks risk-aversion-robustness for the three distance rules (the frequency-guessing rule remains robust because its score is binary). The paper does not analyze the direct-monetary + risk-averse case; the binary-lottery extension is what handles risk aversion.
_Avoid_: using "risk-aversion-robust" without specifying the payment frame.

**Payment-probability concern**:
The implementation cost specific to the frequency-guessing rule under either payment frame: the per-trial probability of receiving any positive payment shrinks exponentially in \((n, k)\) for non-degenerate beliefs, eventually making the implied lottery degenerate. This is a single-rule implementation discussion, not a cross-rule comparison metric.
_Avoid_: presenting payment probability as a horse-race metric.

**Design comparison**:
The simulation comparing the three simulation-headline rules (squared-distance, frequency-guessing, Manhattan) across design dimensions \((n, k, p)\) — number of trials, number of categories, latent-belief structure — under stated inferential objectives. Hamming is excluded from this comparison (ADR-0001, second amendment).
_Avoid_: "design comparison" (legacy term from earlier drafts; retire in new text), "horse race" in manuscript prose (acceptable in working notes only), "simulation tournament".

## Relationships

- A **frequency-report scoring rule** \(S\) induces an **optimal-report correspondence** \(R_S\).
- The **identified set** \(\Theta_S(r)\) is the preimage of \(r\) under \(R_S\): the set of beliefs that rationalize \(r\) as an optimal report.
- **Coordinate bounds** and **mean bounds** are projections / linear functionals of \(\Theta_S(r)\); they must be computed against the full set, not by composing per-coordinate intervals.
- **Informativeness** is the metric by which the **design comparison** ranks rules within design cells.

## Example dialogue

> **Reader:** "When you say the squared-distance rule has sharp closed-form bounds, you mean closed form for the **identified set** itself?"
> **Author:** "Closed form for both the **identified set** and its **coordinate bounds**. The **mean bound** also admits a closed-form expression as an optimization over the full **identified set**, not a combination of **coordinate bounds**."
> **Reader:** "And for **Manhattan** or **Hamming**?"
> **Author:** "There we currently have characterizations of \(R_S(p)\) and threshold-computed bounds. Whether closed-form **identified set** descriptions exist for those rules is an open analytical question — they remain **headline rules** in the **design comparison** even when only computational bounds are available."

## Flagged ambiguities

- "Inverse belief region" was previously used to mean what we now call the **identified set**. Retire the legacy term in new manuscript text; existing sections will be migrated.
- "Mean bound" must always be stated as an optimization over \(\Theta_S(r)\), never as a combination of **coordinate bounds**. The two coincide only in degenerate cases.
- "Sharp" applied to the **identified set** \(\Theta_S(r)\) itself is technically true but nearly vacuous — the set is by construction the exact preimage of the restriction \(r \in R_S(p)\), with no outer-set alternative to be sharp against. Reserve "sharp" for **bounds**, where it is a substantive claim. Do not write "sharp identified set"; write "identified set", and separately "sharp closed-form / computational bounds".
- The identified set \(\Theta_S(r)\) must include ties: \(p \in \Theta_S(r)\) whenever \(r\) is *one of* the optimal reports under \(p\). This weakest restriction is what makes the bounds sharp — tie-breaking is unobservable, so one cannot condition on \(r\) being the unique optimum. A future edit that switched to unique-optimum conditioning would silently change every sharpness claim.
