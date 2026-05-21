# Current Issues

## Submission Readiness

The step-4 manuscript revision, the citation pass, and the step-5 proof audit
are all complete (2026-05-21). The proofs are rigorous (the two quadratic-proof
gaps were fixed and re-audited closed), the bibliography is corrected and
extended, and the paper compiles cleanly. The subsequent three-rule revision and its final
exposition pass are also complete (2026-05-21); the paper compiles with no
undefined references and no overfull boxes. What remains before submission is a
focused external read by a human reader.

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

## Three-Rule Comparison

The paper headlines three rules — quadratic, discrete-metric, Manhattan — each
in both the scoring-rules section and the design comparison. Hamming and
Chebyshev are not headline rules; they are covered in the discussion subsection
"Other Count-Loss Rules and the Limits of the Approach" (ADR-0001, fourth
amendment). Status:

- Hamming and Chebyshev were investigated thoroughly. The interior
  single-transfer-sufficiency conjecture for Hamming was refuted by exact search
  (Step 0a; `outputs/verification/hamming_interior_search.md`), and a
  bound-computation spike failed at k=10 on both reliability and runtime (Step
  0b; `outputs/verification/hamming_spike.md`). The demotion is evidence-driven,
  not arbitrary — see ADR-0001's third and fourth amendments.
- The discussion subsection states the obstructions precisely and must stay
  conservative: Hamming is not "unsolvable" (it has an exact identified set, a
  closed-form modal-box inner bound, and a k=2 closed form); the precise claim
  is that its sharp k>2 bounds are computationally intractable at the design
  grid's scale, and single-transfer optimality fails even at interior beliefs.
- Chebyshev is no longer a single passing sentence: it has a paragraph in the
  discussion subsection (no clean optimal-report characterization for k>2; its
  expected loss does not separate across coordinates).

## Simulation Metric Issues

The current winning-probability/payment-probability component is not central to the revised paper.

Reason:

- Exact-correct-report payment probability is naturally relevant to the discrete-metric / frequency-guessing rule.
- It is not a symmetric informational-efficiency metric for quadratic, Manhattan, or Hamming rules unless comparable payment implementations are specified.

Action:

- Remove payment probability from the main horse-race metrics, or move it to a short implementation discussion for the discrete-metric rule.
- Focus the simulation on inverse-region widths, mean-bound widths, ranking, and regret metrics.