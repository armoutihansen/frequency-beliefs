# Current Issues

## Submission Readiness

The step-4 manuscript revision, the citation pass, and the step-5 proof audit
are all complete (2026-05-21). The proofs are rigorous (the two quadratic-proof
gaps were fixed and re-audited closed), the bibliography is corrected and
extended, and the paper compiles cleanly. What remains before submission is a
sharper final exposition pass and a focused external read.

## Mathematical Issues

- Quadratic-distance proof: the step-5 audit (2026-05-21) found two gaps in the
  appendix proof (Gap A: the sufficiency step omitted the connecting inequality
  `2M <= sum_i d_i^2`; Gap B: the sharpness claim was hand-waved). Both were
  FIXED the same day — Gap A by stating `2M <= sum_i d_i^2` explicitly (with the
  remark that negative-d coordinates necessarily have `r_j>0`), Gap B by
  supplying and verifying explicit endpoint-attaining belief vectors for all
  three coordinate-bound cases — and the fixes were re-audited (theory-auditor)
  and found to CLOSE both gaps. The quadratic centerpiece proof is now rigorous.
- The discrete-metric attribution to Schlag--Tremewan is verified: their
  Proposition 1 (local PDF read 2026-05-21) states exactly the coordinate bounds
  `[r_i/(n+k-1),(r_i+1)/(n+1)]`. The appendix discrete-metric proof was audited
  SOUND, with one minor completeness line recommended (verify the lower-endpoint
  attaining vector satisfies all constraints).
- Manhattan: the 2026-05-21 bounds search upgraded this rule, and the derivation
  was independently audited (theory-auditor, 2026-05-21) and found SOUND.
  Single-unit-transfer optimality is provably sufficient, so the identified set
  is exact; sharp coordinate bounds reduce to a one-dimensional monotone scalar
  equation (semi-analytical, not closed form, not grid-limited). Two minor
  expository fixes are needed in the eventual manuscript proof (see the audit
  note in the bounds-search memo) but there is no logical gap. Do not describe
  Manhattan bounds as closed form; they may be described as sharp and
  semi-analytical.
- Mean bounds must continue to be stated as optimizations over the full identified
  set, not as combinations of coordinate intervals.
- Hamming: bounds are computational for k>2. Single-unit-transfer optimality is
  necessary but NOT sufficient (failure at boundary beliefs); the identified set
  is a non-convex semialgebraic set. k=2 coincides with discrete-metric (closed
  form). A proven closed-form inner bound exists (the modal box). Sharp k>2
  bounds must be reported as computed, with a stated tolerance.
- Chebyshev distance remains secondary; not part of the headline four-rule set.

## Simulation Issues

- The simulation is a design diagnostic conditional on optimal reporting; it is not evidence about actual subject behavior.
- The simulation horse race compares three rules — discrete metric, quadratic
  distance, Manhattan distance. Hamming is excluded by design (ADR-0001, second
  amendment): its sharp bounds are computationally intractable at the design
  grid's large cells. Chebyshev remains secondary.
- Manhattan bounds are being upgraded from a c-grid scan to a sharp root-find;
  once done, the threshold-tolerance caveat no longer applies.
- The paper currently reports tabular summaries only; final figures remain undecided.

## Interpretation Risks

- Do not claim that any rule is uniformly best.
- Do not claim the paper invents frequency guessing or the exact-match mechanism.
- Do not claim distance rules are robust to risk aversion under direct monetary payment.
- Do not oversell the cognitive advantage of frequency reports without additional empirical evidence.
- Do not describe grid or simulation evidence as mathematical proof.

## Literature Issues

The bibliography needs final verification against the local PDFs in `_context/related_literature/`.
Important sources include:

- Schlag--Tremewan for frequency guessing;
- Schlag et al. for belief-elicitation methods;
- Armantier--Treich for risk-aversion concerns;
- Hogarth for probability-assessment motivation;
- Savage, Selten, and Gneiting--Raftery for scoring-rule background.

## Four-Rule Comparison Issues

The project compares quadratic, discrete-metric, Manhattan, and Hamming rules as
headline rules in the ANALYTICAL taxonomy; the SIMULATION horse race covers only
the first three (ADR-0001, second amendment). The 2026-05-21
analytical-bounds-search (memo:
`_context/exploration/bounds_search_manhattan_hamming.md`; outcome recorded in
ADR-0001) resolved the analytical investigation. Remaining open issues:

- The Manhattan single-transfer-sufficiency proof and the semi-analytical
  coordinate-bound theorem are new results awaiting the proof audit
  (next_steps.md step 5) before manuscript entry.
- Hamming is presented analytically only: k=2 closed form (= discrete-metric),
  the single-transfer non-sufficiency obstruction, and the modal-box inner /
  single-transfer outer sandwich. It is not in the simulation horse race.
- The simulation code is being revised to upgrade Manhattan from a c-grid scan
  to a sharp root-find at the threshold crossing.
- The scoring-rules section must present Hamming honestly as the analytically
  weakest and computationally intractable rule, without implying it was demoted
  arbitrarily — the demotion is evidence-driven (see ADR-0001).
- Chebyshev is cut from the main text (decided 2026-05-21): it is neither
  headline, analyzed, nor simulated, so it is demoted to a single acknowledging
  sentence noting the inverse-region machinery extends to other count-loss
  criteria. The standalone Chebyshev subsection is removed.

## Simulation Metric Issues

The current winning-probability/payment-probability component is not central to the revised paper.

Reason:

- Exact-correct-report payment probability is naturally relevant to the discrete-metric / frequency-guessing rule.
- It is not a symmetric informational-efficiency metric for quadratic, Manhattan, or Hamming rules unless comparable payment implementations are specified.

Action:

- Remove payment probability from the main horse-race metrics, or move it to a short implementation discussion for the discrete-metric rule.
- Focus the simulation on inverse-region widths, mean-bound widths, ranking, and regret metrics.