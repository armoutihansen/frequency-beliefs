# Current Status

Date: 2026-06-10

## Update — 2026-06-10 (latest) Direction (C) adopted: two papers; Remark 1 removed

A direction-search session resolved the venue/identity question (memo:
`_context/exploration/direction_memos.md`, adopted): **(C) two papers** —
paper 1 is the current manuscript, finished for a field venue
(Experimental Economics / JEBO / GEB tier; the earlier "general-interest"
tier is retired as optimistic), and paper 2 is a future methods companion
built from the audited master-threshold/frontier memos, gated on explicit
author authorization of the inverse-optimization literature check.
For paper 1 the author selected: Remark 1 REMOVED (executed; the
extended-real sentence now stands alone; 33 pp, clean compile), plus two
approved strengtheners not yet executed — the misreporting robustness
exercise and final figures (task list P0–P3 in `_context/next_steps.md`;
P0 is the pre-existing scripts-renaming debt, a prerequisite). The
small-cell Hamming/Chebyshev simulation was considered and declined.
CLAUDE.md's binding constraints were amended to the new scope: paper-1
tasks only, strictly offline, paper 2 and any literature work only on
explicit author instruction.

## Update — 2026-06-10 (later) LIGHT integration EXECUTED

On explicit author instruction the Light plan L1–L5 was executed the same
day: Remark `rem:threshold` (threshold form of the single-transfer
inequalities, with the three rules' band inversions) added after Lemma 1 in
`03_scoring_rules.tex`; the RPS sentence corrected (cumulative vs
per-category counts); the extended-real boundary-belief sentence added; the
order-preserving Hamming exclusion added to `07_discussion.tex`. A targeted
theory-audit (evidence-rules protocol, all materials pasted) returned
"publishable after listed fixes"; all fixes were applied — notably the
expected-LOSS orientation in the Hamming passage and the explicit
CDF-units reparameterization in the remark — and the paper compiles clean
(34 pp, 0 errors, 0 undefined references). Execution was fully offline; no
citations added. The CLAUDE.md author-imposed constraints (Light only;
no literature search without explicit instruction) remain in force.

## Update — 2026-06-10 Master threshold theorem developed; LIGHT integration approved (not yet executed)

A theorem-development session generalized Lemma 1's bound machinery: under
separability, discrete convexity, and monotone marginal costs, the
identified set is a one-parameter union of box–simplex slices, coordinate
projections are intervals, sharp coordinate bounds solve single monotone
scalar equations, and Propositions 1–2's closed forms drop out of the
crossing equation with explicit thresholds (the Schlag–Tremewan constants
n+1 and n+k−1 are crossing thresholds). Full development, status labels,
converse analysis (order-preserving Hamming exclusion proven; argmin-level
open), and two audits in
`_context/exploration/master_threshold_theorem.md`; companion checks in
`scripts/explore_master_threshold.py`. Two corrections to prior exploration
docs are recorded there (frontier memo's Prop 3′ is wrong as stated; its
Corollary 5 tier-(b) "rule-specific bonus" caveat is removed).

Decisions (2026-06-10): the inverse-optimization novelty check was WAIVED
(novelty assumed provisionally); placement decision settled on the **LIGHT
integration** — threshold-representation remark after Lemma 1, RPS-sentence
fix, extended-real convention line, order-preserving Hamming exclusion in
the discussion — with the Full restructure held in reserve for the revision
stage (gated on the waived literature check). Execution plan L1–L5 in
`_context/next_steps.md`; the MANUSCRIPT IS STILL UNTOUCHED.

BINDING CONSTRAINTS (author-imposed, 2026-06-10): implement the LIGHT
option only — the Full restructure and the inverse-optimization literature
check each require new, explicit author instruction and must not be
initiated by any agent session. The Light execution is strictly offline:
no literature search, no web search/fetching, no downloading, no
web-capable subagents (full statement in `_context/next_steps.md`).
Audit-protocol note: theory-auditor subagents cannot see the working
tree — paste all materials into the audit prompt (see the memo's audit
log).

## Update — 2026-05-22 Related-work expansion and scoring-rule renaming

Two manuscript passes were completed (logged in
`_context/exploration/literature_scan_log.md`):

1. A thorough related-literature review: the cited papers were read in full
   (PDFs in `_context/related_literature/`), and the introduction's "Related
   literature" block and the discussion were rewritten to contrast the paper
   against the elicitability, frequency-guessing, partial-identification, and
   elicitation-method literatures. 13 verified citations added.

2. A notation/naming-consistency review against that literature, which led to
   three author-approved renames applied manuscript-wide:
   - "quadratic-distance" scoring -> **"squared-distance"** scoring (the
     centerpiece rule), to avoid collision with the *quadratic scoring rule*
     (QSR), a different, proper, probability-report rule.
   - "discrete-metric" scoring -> **"frequency-guessing"** scoring, matching
     Schlag--Tremewan. The metric object \(D_0=\mathbf 1\{r\neq\omega\}\) is
     still called "the discrete metric".
   - "informational efficiency" -> **"informativeness"** (title, body), closer
     to partial-identification usage. New title: *The Informativeness of
     Frequency-Report Scoring Rules*.
   Also: §2 now states explicitly that these are not *proper* scoring rules and
   that a frequency report is a vector of counts; a stray \(S_2\) in the
   appendix proof was unified to \(S_Q\). The paper compiles cleanly (25 pages).

NOT yet synced to the new names: `scripts/` (display labels/keys are coupled
across `design_efficiency.py`, `consistency_check.py`, `verify_regions.py` and
to the committed CSV outputs — a separate refactor + rerun), and `CLAUDE.md`
(which also still lists four headline rules and is independently stale on the
three-rule decision). Both should be reconciled before the next simulation run.

## Update — 2026-05-21 Hamming grilling session and three-rule revision

A `grill-with-docs` session reopened the Hamming rule, ran a two-track
derisking effort (the Hamming-first plan), and resolved it: both tracks failed
— the interior single-transfer-sufficiency theorem was refuted, and the
Hamming bound computation was intractable and unreliable at `k=10` (ADR-0001
third amendment; artifacts in `outputs/verification/`). The author then removed
Hamming from the headline analysis entirely (ADR-0001 fourth amendment), and the
manuscript revision in `_context/revision_plan.md` was executed:

- The paper now headlines THREE rules — quadratic-distance, discrete-metric,
  Manhattan — each in both the scoring-rules section and the design comparison.
- Hamming and Chebyshev are covered in a new discussion subsection, "Other
  Count-Loss Rules and the Limits of the Approach," stating their obstructions
  precisely.
- §3 owns the analytic comparison of the two closed-form rules at the level of
  report concentration; §4 ties it to belief concentration, quantifies it, and
  extends to Manhattan. The introduction and abstract were reframed to lead with
  the concrete characterizations, partial identification as the lens.
- The paper compiles cleanly (0 undefined references).

Text below that still says "four headline rules" reflects the earlier
2026-05-21 direction decision and is superseded by this update.

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
compares three rules by the sharpness of the identified sets they induce. The
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

The paper headlines three rules, all in both the scoring-rules section and the
design comparison (ADR-0001, fourth amendment):

- Quadratic-distance: closed-form identified set and coordinate bounds; the
  analytical centerpiece.
- Discrete-metric: closed-form coordinate bounds; the known Schlag--Tremewan
  exact-match rule.
- Manhattan-distance: exact identified set (single-transfer optimality proven
  sufficient and audited), sharp coordinate bounds via a one-dimensional
  threshold root-find — semi-analytical, not closed form.

Hamming and Chebyshev distance are not headline rules. They appear only in the
discussion subsection "Other Count-Loss Rules and the Limits of the Approach":
Hamming has an exact identified set, a closed-form modal-box inner bound, and a
k=2 closed form, but its sharp k>2 bounds need numerical optimization over a
non-convex set that is intractable at the design grid's scale, and
single-transfer optimality fails even at interior beliefs; Chebyshev's expected
loss does not separate across coordinates and has no clean optimal-report
characterization for k>2.

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