# Four headline rules: a four-way analytical-to-computational spectrum

The paper headlines four frequency-report scoring rules — quadratic-distance, discrete-metric, Manhattan, and Hamming. We chose four over two or three because, under the partial-identification framing aimed at a practitioner-facing methods audience, the contribution includes both the closed-form sharpness results *and* the demonstration that sharp identification is recoverable across rules of differing analytical tractability; demoting Manhattan or Hamming purely because their analytics are harder would suppress the very contrast that gives the paper its meta-contribution.

## Amendment (2026-05-21) — refined from "two analytical, two computational"

The original framing split the four rules into two "analytical" (closed-form) and two "computational." A time-boxed `analytical-bounds-search` (memo: `_context/exploration/bounds_search_manhattan_hamming.md`) found that binary split too coarse. The accurate description is a four-way spectrum:

1. **Quadratic-distance** — closed-form identified set (transfer polytope) and closed-form coordinate bounds. Analytical.
2. **Discrete-metric** — closed-form identified set and closed-form coordinate bounds (Schlag–Tremewan). Analytical.
3. **Manhattan** — *semi-analytical, and an upgrade over the original "computational" label.* Single-unit-transfer optimality is **provably sufficient** (separable discrete-convexity), so the identified set is **exact**; the sharp coordinate bounds reduce to a **one-dimensional monotone scalar equation** (a clamped threshold crossing). Not closed form only because the inverse binomial CDF is non-elementary. The bounds are genuinely sharp, not grid-limited.
4. **Hamming** — computational for `k>2`. Single-unit-transfer optimality is **necessary but not sufficient** (failure occurs at boundary beliefs); the identified set is a non-convex semialgebraic set, and sharp coordinate bounds are obtained by finite numerical computation with a stated tolerance. Positive structure: `k=2` coincides with the discrete-metric closed form, and the **modal box** `[r_i/(n+1),(r_i+1)/(n+1)]` is a proven closed-form *inner* bound.

The manuscript should adopt this four-way language rather than a binary analytical/computational dichotomy. The Manhattan single-transfer-sufficiency proof and the semi-analytical coordinate-bound theorem were independently audited (theory-auditor, 2026-05-21) and found sound, with two minor expository fixes noted in the bounds-search memo; the step-5 audit need only re-verify their final manuscript wording.

## Amendment (2026-05-21, second) — Hamming is not in the simulation horse race

The simulation revision (next_steps.md step 3) established that Hamming sharp bounds are not merely "computational" but computationally **infeasible at the headline design grid's large cells**: the only general method is brute-force search over a simplex grid in `p`, costing `C(denom+k-1,k-1)` points per report, which is ~10^14 at `k=10` — and even enumerating the `C(59,9) ≈ 1.3×10^10` feasible reports at `n=50,k=10` is impossible. The one cheap Hamming bound (the closed-form modal box) equals the discrete-metric coordinate box exactly, so using it would make Hamming a literal duplicate of discrete-metric in the horse race.

Decision: **Hamming remains a headline rule analytically but is removed from the simulation horse race.** The simulation design exercise compares the three rules with tractable sharp bounds — quadratic-distance, discrete-metric, Manhattan. Hamming keeps headline status in the scoring-rules section via its genuine analytical content: the `k=2` closed-form equivalence to discrete-metric, the proven single-transfer non-sufficiency obstruction, and the modal-box inner / single-transfer outer sandwich.

Rationale: ADR-0001 headlined Hamming on "conceptual symmetry with Manhattan." Two findings gathered after that decision dissolved the symmetry — the bounds search showed Manhattan is semi-analytical and clean while Hamming is the analytically weakest, and the simulation step showed Hamming is computationally intractable at headline scale. A rule that is both the weakest analytically and uncomputable at scale has not earned a seat in the simulation horse race. Presenting Hamming analytically and racing the three tractable rules is honest and sharpens the partial-identification spine into a clean spectrum: closed-form (quadratic, discrete-metric), semi-analytical-sharp (Manhattan), computationally intractable (Hamming).

This refines but does not fully reverse the Q4 four-rule decision: Hamming is still a headline rule in the analytical taxonomy and the scoring-rules section; only the simulation horse race is three rules.

## Amendment (2026-05-21, third) — Hamming exclusion confirmed by a dedicated derisking effort

A grilling session on 2026-05-21 reopened the question: the author asked whether Hamming could be worked harder — a stronger theorem, or a way into the simulation despite the cost. A two-track derisking effort (the "Hamming-first plan", `_context/next_steps.md`) was run. Both tracks failed, and the second amendment's exclusion stands, now on much stronger evidence.

- **Step 0a — theorem (REFUTED).** The first and second amendments both state the single-transfer non-sufficiency "failure occurs at boundary beliefs." This is now known to be false — it was a `k=3`-specific artifact. An exact rational-arithmetic search over `k=4,5,6` (`scripts/hamming_interior_search.py`) found interior counterexamples; the cleanest is the *uniform* belief `p=(1/5,...,1/5)` at `n=3,k=5`, where `r=(3,0,0,0,0)` is single-unit-transfer optimal yet `G`-suboptimal. Single-transfer optimality fails on a positive-measure set of strictly interior beliefs for `k>=5`. There is therefore no theorem route to certified-sharp Hamming bounds: the single-transfer region is a strict outer set even on the interior.

- **Step 0b — computation (FAILED).** A bound-computation spike (`scripts/hamming_spike.py`) confirmed the forward problem is cheap — the optimal Hamming report is a separable `O(n^2 k)` dynamic program, so the second amendment's "enumerate `C(59,9)` reports" framing overstated the forward cost. The genuine obstruction is the *inverse* problem: `sup`/`inf` of a linear functional over the non-convex semialgebraic identified set `P_H(r)`. The spike validated correctly at `k=3` (worst gap 0.0038 vs the fine grid) but failed at `k=10`: the computed intervals did not contain the proven closed-form modal-box inner bound, and `P_H(r)` is so small a sliver of the 9-simplex that 8000 concentrated draws yielded 0–2 feasible points. Runtime was ~340 s per report, projecting to ~340 h for a `--final` run.

Decision: **Hamming stays out of the simulation comparison; the second amendment's exclusion is confirmed.** The manuscript revision proceeds as a three-rule comparison. Hamming remains a headline rule analytically. Two manuscript consequences: (i) the §3 non-sufficiency obstruction should be illustrated with the interior uniform-belief counterexample, not a boundary case — it is the stronger and more honest illustration; (ii) statements in this ADR's earlier amendments locating the Hamming failure "at boundary beliefs" are superseded by Step 0a.

## Amendment (2026-05-21, fourth) — Hamming leaves the headline analysis

In the same session, after the third amendment confirmed Hamming out of the simulation, the author decided to remove Hamming from the headline *analysis* as well. The scoring-rules section now headlines three rules — quadratic-distance, discrete-metric, Manhattan — each characterized there and each in the design comparison. Hamming, together with Chebyshev distance, moves to a dedicated discussion subsection, "Other Count-Loss Rules and the Limits of the Approach," which states their obstructions precisely: Hamming has an exact identified set, a closed-form modal-box inner bound, and a `k=2` closed form, but its sharp bounds for `k>2` require numerical optimization over a non-convex set that is intractable at the design grid's category counts, and single-transfer optimality fails even at interior beliefs; Chebyshev's expected loss does not separate across coordinates and has no clean multi-category optimal-report characterization.

Rationale: after Steps 0a/0b, Hamming's analytical content is an obstruction plus a sandwich — a statement about where the partial-identification program stops, not a headline characterization. Placing Hamming and Chebyshev in a "limits of the approach" subsection is the honest location and yields a cleaner paper: every rule in the scoring-rules section is also in the design comparison, so the §3 and §4 scope align exactly. This reverses the original four-headline-rules decision and the third amendment's "Hamming remains a headline rule analytically." It changes no result — Hamming's characterization is preserved, only relocated and reframed as a scope boundary. The scoring-rules section's §3.2 ("Rules Without Closed-Form Bounds") is correspondingly retitled to the single Manhattan subsection.

## Considered Options

- **Two headline rules (quadratic + discrete-metric).** Cleanest theory but throws away the design-exercise breadth and removes the rules a practitioner is most likely to also consider. Rejected because it shrinks the contribution to a single theorem and recovered prior art.
- **Three headline rules (drop one of Manhattan/Hamming).** Forces an asymmetric choice between two rules with similar analytical status; would either need a substantive performance argument we don't yet have, or would reduce to "we picked the one we implemented first."
- **Four rules without the analytical/computational reframe.** Keeps the breadth but invites the referee complaint "why are threshold-computed bounds in a headline?" The four-way framing pre-empts this by making the spectrum explicit.

## Consequences

- All four rules must be evaluated on the same informational-efficiency metrics in the design exercise.
- The paper must never describe Hamming `k>2` bounds as closed form, and must not describe Manhattan bounds as closed form either — Manhattan is "semi-analytical, sharp, one-dimensional." Section text, theorem environments, and table captions must reflect the four-way spectrum.
- Manhattan's simulation code should be upgraded from a `c`-grid scan to a bracketed root-find at the threshold crossing, so reported Manhattan bounds are genuinely sharp, not grid-limited.
- Hamming requires the same simulation infrastructure as the other three; this is current work, not a future task. The closed-form modal-box inner bound should be reported alongside the computed Hamming bounds as a rigorous inner sandwich.
- If the simulation shows Manhattan and Hamming behaving near-identically across design cells, this ADR should be revisited — the case for headlining both rests on them offering distinguishable inferential profiles.

## Amendment (2026-06-10, fifth) — the limits subsection relocates into Section 3

During the Section-3 restructure (rules first, structural lemma after, on
author instruction), the author approved moving the Hamming/Chebyshev
subsection from the discussion into Section 3 as its closing subsection,
"Two Rules Outside the Structure: Hamming and Chebyshev Distance"
(label `sec:other-rules` unchanged, so all cross-references follow). This
reverses the fourth amendment's *placement* only: with the single-transfer
lemma now anchoring Section 3 and motivating the taxonomy (linear
inequalities = closed form; monotone transcendental = semi-analytical;
hypotheses fail = no tractable sharp bounds), the two failure modes
complete the structural story where it is told. The substance of the
fourth amendment stands unchanged: Hamming and Chebyshev remain demoted
from the headline analysis, excluded from the design comparison, and
characterized rather than compared. The discussion section now contains
only practical material (recommendations, risk aversion and
implementation, the open empirical question).
