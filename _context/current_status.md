# Current Status

Date: 2026-05-21

## Project Thesis

As of the 2026-05-21 direction decision, the project is a methodological paper
that recasts incentivized frequency-report belief elicitation as a partial-
identification problem. A subject has latent multinomial beliefs \(p\) and
reports a count vector \(r\); each scoring rule \(S\) induces a mechanism-induced
identified set
\[
\Theta_S(r)=P_S(r)=\{p:r\in R_S(p)\},
\]
the set of beliefs that rationalize \(r\) as an optimal report. The paper
compares four rules by the sharpness of the identified sets they induce. The
practical output is a set of finite-sample bounds for latent probabilities and
linear functionals such as means.

See `CONTEXT.md` (glossary), `docs/adr/0001` and `docs/adr/0002` (hard-to-reverse
decisions), and `_context/exploration/direction_memos.md` (adopted-direction
memo). The legacy term "inverse belief region" is being retired in favor of
"identified set".

## Active Manuscript

The manuscript is in `paper/` and compiles cleanly. As of 2026-05-21 it has been
through the full step-4 revision (see `_context/next_steps.md`). Title:

> The Informational Efficiency of Frequency-Report Scoring Rules

Current structure (risk aversion is now a subsection of the discussion, not a
standalone section; `06_risk_attitudes.tex` was removed):

1. Introduction
2. Setup
3. Frequency-Report Scoring Rules
4. Informational Efficiency Exercise
5. Discussion (includes the risk-aversion / binary-lottery subsection and a
   worked example)
6. Appendix (proofs; design-exercise details)

## Active Rules

The four headline rules sit on an analytical-to-computational spectrum (ADR-0001):

- Quadratic-distance: closed-form identified set and coordinate bounds; the
  analytical centerpiece.
- Discrete-metric: closed-form coordinate bounds; the known Schlag--Tremewan
  exact-match rule.
- Manhattan-distance: exact identified set (single-transfer optimality proven
  sufficient and audited), sharp coordinate bounds via a one-dimensional
  threshold root-find — semi-analytical, not closed form.
- Hamming-distance: analytical-only — k=2 closed form, the single-transfer
  non-sufficiency obstruction, the modal-box inner / single-transfer outer
  sandwich. Excluded from the simulation (intractable at scale).

Chebyshev distance has been cut to a single acknowledging sentence.

## Current Evidence

The revised design exercise was run with:

```bash
uv run python scripts/design_efficiency.py --final --draws 5000
```

Outputs are in `outputs/design_exercise/`; the prior committed run remains in
`outputs/simulation_design/`. The grid is \(n\in\{5,10,20,50\}\),
\(k\in\{2,3,5,10\}\), \(\alpha\in\{0.1,0.3,1,3,10\}\), 5,000 Dirichlet draws per
cell; the horse race is three rules (quadratic, discrete-metric, Manhattan).

Main findings:

- Discrete-metric has the highest average-coordinate-width win share (~0.62).
- Quadratic distance has the highest worst-coordinate-width win share (~0.61)
  and leads on worst-coordinate regret.
- Manhattan rarely wins outright but has the lowest mean cell-best regret for
  average-coordinate and mean inference — the low-regret "safe" rule.
- No universal ranking; the best rule depends on the inferential objective.

## Verification Status

- `scripts/verify_regions.py` passes the implemented finite checks (discrete,
  quadratic, Manhattan exchange/threshold logic, binary cases, risk-aversion
  counterexamples).
- The 2026-05-21 analytical-bounds-search and a `theory-auditor` pass verified
  the Manhattan single-transfer-sufficiency proof and coordinate-bound theorem
  as sound; the Hamming non-sufficiency obstruction was confirmed by exact
  rational arithmetic.
- Outstanding: the step-5 proof audit of the quadratic closed-form bounds and
  the discrete-metric attribution, plus re-verification of the Manhattan proof
  in its final appendix wording. This audit is the final proof-verification gate.

## Direction Decision (2026-05-21)

A `grill-with-docs` session resolved the project direction. Summary of the
decisions; full detail in `CONTEXT.md`, the two ADRs, and
`_context/exploration/direction_memos.md`.

- **Spine.** Partial-identification reframing. Each scoring rule induces a
  mechanism-induced identified set; the quadratic rule is the worked centerpiece.
- **Venue tier.** General-interest economics journal with a methods section.
  Partial-ID framing carries the introduction and discussion; the body stays
  light on partial-ID machinery.
- **Headline rules.** Four — quadratic, discrete-metric, Manhattan, Hamming —
  framed as two with closed-form bounds and two characterized computationally
  (ADR-0001). Chebyshev stays secondary.
- **Payment frame.** Risk neutrality is the maintained body assumption; the
  binary-lottery extension is argued in the discussion to carry the analysis to
  risk-averse EU subjects (ADR-0002). No payment-probability or risk-aversion
  branch in the simulation.
- **Simulation.** Three-rule comparison (quadratic, discrete-metric, Manhattan)
  on two headline metrics — average coordinate width and the ordered-category-
  mean bound — displayed as cell-best regret. Hamming is excluded from the
  simulation horse race (ADR-0001, second amendment): its sharp bounds are
  computationally intractable at the design grid's scale. Not a
  payment-probability horse race.
- **Scope.** Pure methodological paper; no empirical illustration. A stipulated
  worked example in the discussion substitutes.
- **Contribution.** Three claims: partial-ID framing (N1), four-rule contextual
  comparison (N2), closed-form quadratic theorem (N3). Headline = framing +
  contextual comparison.

## Analytical Objective — Resolved

The time-boxed `analytical-bounds-search` (2026-05-21) is complete; memo at
`_context/exploration/bounds_search_manhattan_hamming.md`. Outcome: Manhattan is
semi-analytical with sharp coordinate bounds (single-transfer sufficiency proven
and audited); Hamming is computational for k>2, with a proven closed-form
modal-box inner bound and the non-sufficiency obstruction documented. ADR-0001
was amended to the four-way analytical-to-computational spectrum. No computed
bound is described as closed form.

## Simulation Objective

The simulation is a three-rule comparison (quadratic, discrete-metric,
Manhattan) of identified-set sharpness, not a universal-winner search. It varies
\(n\), \(k\), latent belief structure \(p\), and the inferential objective, and
reports average coordinate width and the ordered-category-mean bound, displayed
as cell-best regret with a win-share summary. Hamming is excluded because its
sharp bounds are computationally intractable at the design grid's scale
(ADR-0001, second amendment). Payment probability is at most a
discrete-metric-only implementation diagnostic, not a comparison metric.