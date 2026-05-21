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
