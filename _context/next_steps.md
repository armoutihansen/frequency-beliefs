# Next Steps

Date: 2026-05-21

> **ACTIVE TASK — final polish before submission.** The 2026-05-21 Hamming
> grilling session, the Hamming-first derisking plan, and the three-rule
> manuscript revision in `_context/revision_plan.md` are all COMPLETE (see that
> file's status banner and `_context/current_status.md`). Hamming was resolved
> out — refuted theorem, intractable computation — and removed from the headline
> analysis; the paper now headlines three rules, with Hamming and Chebyshev in a
> discussion subsection. What remains before submission is a final exposition
> polish and a focused external read. The "Hamming-first plan" and the numbered
> "Action sequence" below are retained as completed records.

## Hamming-first plan (RESOLVED 2026-05-21 — outcome: decouple)

**Resolution.** Both derisking tracks failed. Step 0a refuted the
interior-sufficiency theorem (interior counterexamples at `k>=5`, including the
uniform belief). Step 0b's bound-computation spike failed at `k=10`: the
optimization over the non-convex identified set `P_H(r)` was both unreliable
(computed intervals did not contain the proven modal-box inner bound) and
intractable (~340 s/report, ~340 h projected for a `--final` run). Per the
plan's floor, the outcome is **decouple**: the revision resumes as a three-rule
comparison (`_context/revision_plan.md`, now active), Hamming stays a headline
rule analytically only, and ADR-0001's Hamming-exclusion is confirmed (third
amendment). Artifacts: `outputs/verification/hamming_interior_search.md`,
`outputs/verification/hamming_spike.md`. The original plan follows for the
record.

Goal: include Hamming as a fourth rule in the design comparison, with the best
analytical treatment obtainable, then run one 4-rule manuscript revision. The
plan has a floor: it always reduces to shipping the 3-rule paper.

Key fact established in the grilling session: the Hamming optimal report and the
test `p ∈ P_H(r)` are both cheap everywhere on the closed simplex — a separable
`O(n^2 k)` dynamic program gives `V*(p) = max_s G(s;p)`, and `p ∈ P_H(r)` iff
`G(r;p) ≥ V*(p)`. The only hard part is the *optimization* `max p_h` over that
non-convex feasible set. The interior-sufficiency theorem is an *upgrade*
(it collapses `P_H` to the `O(k^2)`-constraint `H-loc` polynomial program and
certifies sharpness), not a gate.

### Step 0 — parallel derisking (do both)

0a. **Theorem probe — DONE (2026-05-21): REFUTED.** The exact
    rational-arithmetic search (`scripts/hamming_interior_search.py`, artifact
    `outputs/verification/hamming_interior_search.md`) found interior
    counterexamples for `k=5,6`. Cleanest: `n=3, k=5`, the uniform belief
    `p=(1/5,...,1/5)`, where `r=(3,0,0,0,0)` is single-unit-transfer optimal
    (`G=257/125`) but `s=(0,0,1,1,1)` is strictly better (`G=272/125`).
    Single-transfer sufficiency fails on a positive-measure set of strictly
    interior beliefs — it is not a boundary phenomenon. **The theorem route to
    certified-sharp Hamming bounds is dead**; `(H-loc)` is a strict outer set
    even on the interior. The plan now hinges entirely on Step 0b: a passing
    simulation spike lets Hamming enter the 4-rule comparison as a *computed*
    bound (never labelled "sharp"); a failing spike means decouple and ship the
    3-rule paper.

    The original 0a text follows. Extend the exact rational-arithmetic
    counterexample search of `_context/exploration/bounds_search_manhattan_hamming.md`
    §(3') from `k=3` to `k=4,5,6`: does interior single-unit-transfer optimality
    imply global Hamming optimality for strictly interior beliefs? An interior
    counterexample refutes the conjecture immediately and cheaply.

0b. **Simulation probe — DONE (2026-05-21): FAILED.** `scripts/hamming_spike.py`
    built the DP forward solver and membership oracle (both validated; the
    forward solver matched brute force on 160/160 beliefs) and a multistart
    global optimizer for the bounds. It validated at `k=3` (worst gap 0.0038 vs
    the fine grid) but failed at `k=10` on both axes: the computed intervals did
    not contain the proven modal-box inner bound (unreliable in 9-D), and the
    cost was ~340 s/report, ~340 h projected for a `--final` run (intractable).
    Artifact: `outputs/verification/hamming_spike.md`.

    The original 0b text follows. Spike Hamming bounds in the simulation: the
    separable `O(n^2 k)` DP forward solver, the exact DP membership oracle, and
    a global optimizer for the coordinate/mean bounds at the hardest cell
    (`n=50, k=10`). Validate against the modal-box / single-transfer sandwich
    (the bound must lie in `[sup over MB, sup over H-loc]`) and against the
    existing `k=3` `hamming_grid_bounds` in `verify_regions.py`.

### Step 1 — branch on Step 0

- 0a survives **and** a proof of interior sufficiency closes within a bounded
  effort budget: Hamming bounds are certified **sharp**. Promote Hamming to the
  §3 analysis and the 4-rule simulation.
- 0a refuted, or the proof does not close in budget, **but** 0b passes: Hamming
  enters the 4-rule simulation as a **computed** bound (CONTEXT.md
  "computational bound"; never labelled "sharp" without the tolerance qualifier).
- 0b fails (no validated, tractable bound computation): **decouple** — resume
  `revision_plan.md` as the 3-rule revision; Hamming stays a research thread.

### Step 2 — 4-rule simulation (only if Step 1 promotes Hamming)

Add Hamming to `scripts/design_efficiency.py` as a fourth rule; re-run
`--final --draws 5000`; regenerate the `outputs/design_exercise/` tables.
ADR-0001's second amendment (Hamming excluded from the simulation) is reversed —
record a third amendment with the Step 0 outcome. Update the CONTEXT.md
"design comparison" / "headline rule" entries to four simulation rules.

### Step 3 — single manuscript revision

Resume `revision_plan.md`, reconciled to 3-rule or 4-rule per Step 1, and
carrying decisions D1–D3 recorded in that file's status banner.

## Action sequence (historical — prior revision cycle, complete)

These steps follow the direction decided in the earlier 2026-05-21 grilling
session. See
`CONTEXT.md` for the glossary, `docs/adr/0001` and `docs/adr/0002` for the two
hard-to-reverse decisions, and `_context/exploration/direction_memos.md` for the
adopted-direction memo.

The first two steps are independent and can run in parallel. Step 3 depends on
step 1. Step 4 depends on steps 1-3. Steps 5-6 run alongside or after step 4.

### 1. Analytical-bounds-search for Manhattan and Hamming — DONE (2026-05-21)

Completed. Memo: `_context/exploration/bounds_search_manhattan_hamming.md`.
Outcome (recorded in the ADR-0001 amendment):

- **Manhattan** upgraded to semi-analytical: single-unit-transfer optimality is
  provably sufficient (identified set exact), and sharp coordinate bounds reduce
  to a one-dimensional monotone scalar equation. Not closed form (inverse
  binomial CDF), but sharp and not grid-limited.
- **Hamming** stays computational for k>2: single-transfer optimality is
  necessary but not sufficient (failure at boundary beliefs, verified by exact
  rational arithmetic). k=2 = discrete-metric closed form. A proven closed-form
  modal-box inner bound is available.
- The "two analytical + two computational" split was refined to a four-way
  spectrum; ADR-0001 amended accordingly.

The bounds-search memo was corrected after an exact-arithmetic re-audit (its
first Hamming counterexample was a numerical-tolerance artifact). The Manhattan
single-transfer-sufficiency proof and coordinate-bound theorem were
independently audited (theory-auditor, 2026-05-21) and found SOUND, with two
minor expository fixes noted in the memo for the manuscript proof.

### 2. Targeted literature scan (parallel with step 1)

Run the `literature-scan` skill, organized by the three novelty surfaces in
priority order:

- **N2 (primary)** — belief-elicitation horse races: Schlag-Tremewan, Schlag et
  al., Hossain-Okui, Trautmann-van de Kuilen. Find the closest prior comparison
  and the gap.
- **N1 (secondary)** — scoring-rule-induced identified sets in the partial-ID
  literature: Manski, Tamer, Molinari; check Lambert/Frongillo property
  elicitation and decision-theoretic identification work.
- **N3 (focused check)** — prior closed-form analytical bounds for the quadratic
  frequency rule: Brier, Selten, Gneiting-Raftery, Savage.
- **Adjacent (confirm)** — verify Roth-Malouf (1979), Karni (2009),
  Berg et al. (1986) or Selten et al. (1999) are needed for the binary-lottery
  extension and present in `paper/references.bib`.

### 3. Simulation revision (done 2026-05-21)

DONE: Manhattan coordinate bounds upgraded to a sharp threshold root-find
(validated against the fine grid, ~8e-6 agreement); cell-best regret added to
`rule_comparison.csv` alongside win shares; outputs moved to
`outputs/design_exercise/` so the committed `outputs/simulation_design/` run is
untouched; summary rewritten for the three-rule framing with headline/appendix
metric labels; payment probability confirmed as a discrete-only diagnostic.
Validated via `--smoke --validate` (100 checks) and a reduced `--pilot`.
CUT (decided 2026-05-21): the random-c appendix metric variant — worst-
coordinate width already equals the sup-over-simplex linear-functional width and
covers the appendix robustness need; a random-c metric would depend on the prior
over c and add little. The simulation code is now final.
REMAINING: run the full `--final --draws 5000` before step 4 fills in numbers.

Per the ADR-0001 second amendment, the simulation horse race is a THREE-rule
exercise — quadratic-distance, discrete-metric, Manhattan. Hamming is excluded:
its sharp bounds are computationally intractable at the headline grid's large
cells. Update `scripts/design_efficiency.py`:

- keep the three rules already present (discrete, quadratic, Manhattan); do not
  add Hamming;
- compute **average coordinate width** and the **ordered-category-mean bound**
  (canonical payoff `c = (0,1,...,k-1)/(k-1)`, already present as the linear
  mean) as headline metrics; worst-coordinate width serves as the appendix
  sup-over-simplex variant (random-c was cut, see status note above);
- **Manhattan**: replace the `c`-grid scan with a bracketed root-find at the
  threshold crossing (per the ADR-0001 amendment) so reported bounds are sharp,
  not grid-limited;
- remove payment probability as a comparison metric (keep at most a
  discrete-metric-only implementation diagnostic);
- emit full-grid data structured so curated headline subsets regenerate without
  rerunning the simulation;
- headline display: **cell-best regret** heat-maps by `(n,k,alpha)` plus a
  win-share summary; raw widths alongside for level interpretation;
- write to a NEW output location; do not overwrite the committed
  `outputs/simulation_design/` final outputs.

### 4. Manuscript revision (DONE 2026-05-21; guardrail mode)

All six sub-steps complete; the paper compiles cleanly throughout.

- 4a — terminology migration ("inverse belief region" -> "identified set")
  across main.tex and all sections. DONE.
- 4b — Setup (`02`): risk neutrality stated as the maintained assumption;
  "mechanism-induced identified set" introduced; payment-probability line fixed;
  Chebyshev demoted. DONE.
- 4c — Scoring rules (`03`): four-way analytical-to-computational spectrum;
  Manhattan semi-analytical/sharp; Hamming analytical-only (k=2 closed form,
  obstruction, modal-box sandwich); Chebyshev subsection removed. DONE.
- 4d — Design comparison (`06`): three-rule horse race; cell-best regret table
  and the low-regret-Manhattan finding; sharp-Manhattan labeling; table numbers
  from `outputs/design_exercise/`. DONE.
- citation pass (step 6): 3 wrong entries fixed, 5 entries added. DONE.
- 4e — Discussion (`07`): `06_risk_attitudes.tex` folded in as a binary-lottery
  extension subsection (ADR-0002) with proper citations and the EU-only and
  cognitive-load caveats; payment-probability tradeoff folded in; stipulated
  worked example added. The standalone risk section file was removed. DONE.
- 4f — Introduction + abstract: partial-ID framing made explicit (cites
  Manski); contribution paragraph = Q7 Option D; abstract rewritten; N2
  positioning sharpened against Schlag-Tremewan. DONE.

REMAINING from step 4:
- 4g — transcribe the audited Manhattan single-transfer-sufficiency proof into
  the appendix (`app:manhattan-proof`); `03` already references it.
- Loose ends: the `\cite[Proposition 1]{SchlagTremewanSimple}` locator must be
  checked against the published version; the 5 new bib entries are
  metadata-verified only (no local PDFs).

### 5. Proof audit (DONE 2026-05-21)

A `theory-auditor` pass audited the three appendix proofs.

- Manhattan appendix proof: SOUND in its final wording.
- Discrete-metric appendix proof: SOUND (one minor completeness line for the
  lower-endpoint attaining vector was recommended but is optional).
- Quadratic appendix proof (the centerpiece): the audit found two gaps —
  Gap A (a missing connecting inequality in the sufficiency step) and Gap B
  (a hand-waved sharpness claim). Both were fixed the same day and the fixes
  were re-audited and found to CLOSE both gaps. The quadratic proof is now
  rigorous.

The paper compiles cleanly. All numbered steps 1-6 are complete.

### 6. Citation pass (alongside / after step 4)

Run `citation-pass`: verify every entry in `paper/references.bib` against the
PDFs in `_context/related_literature/`; add the binary-lottery references
required by ADR-0002; make the novelty claim precise relative to step 2's
findings.

## Open contingencies

- Step 1 contingency RESOLVED: no closed-form Manhattan/Hamming bounds, but
  Manhattan is semi-analytical (sharp, 1-D) and Hamming has a closed-form inner
  bound. ADR-0001 amended to a four-way spectrum.
- If the step 5 proof audit finds a gap in the Manhattan sufficiency proof:
  Manhattan reverts toward "computational" and ADR-0001 must be amended again.
- If the simulation shows Manhattan and Hamming behaving near-identically across
  design cells: revisit ADR-0001 (the case for headlining both rests on
  distinguishable inferential profiles).
- If step 2 finds a close prior competitor for N2: the contribution statement
  and positioning must be sharpened before manuscript revision.

--------------------------------------------------------------------------------

## Candidate-rule screen (2026-05-22)

A systematic search for additional frequency-report scoring rules was completed;
full screen in `_context/exploration/rule_candidate_screen.md`. Outcome:

- New feasible rules found: KL divergence and RPS (closed-form / polytope);
  pinball, expectile, L_p-power, Hellinger, Huber, cumulative-L1 (semi-analytical).
- The search yielded essentially no new infeasible rules: the feasibility
  frontier is sharp — tractable iff separable AND per-coordinate cost
  discrete-convex; Hamming and Chebyshev are the two canonical failure modes.
- Verified by `scripts/candidate_rule_checks.py` (finite enumeration checks).

Candidate Stage-3 tasks, gated on a case-by-case disposition decision:

1. Prove the feasibility-frontier characterization (separable + discrete-convex
   per-coordinate ⇔ tractable / O(k²)-facet identified set). Highest-value
   result the screen surfaced — turns the rule-by-rule tractability story into
   one theorem.
2. If RPS is promoted: complete the RPS single-count-transfer sufficiency proof
   for general k (monotone cumulative lattice / L-natural-convexity), via
   `theory-auditor`; add the ordered-category setup.
3. If pinball is promoted: full derivation of the quantile rule (generalizes
   Manhattan; reuses the threshold root-find).
4. Characterize the sparse-facet Bregman sub-family (h' discrete-concave).

### Feasibility-frontier derivation (2026-05-22)

Done: `_context/exploration/feasibility_frontier.md` develops and audits the
characterization. Outcome — the result is real and useful but its optimization
core is CLASSICAL (discrete separable resource allocation: Fox 1966; Federgruen
& Groenevelt 1986; Ibaraki & Katoh 1988; Murota 2003). Per the user's decision
it is carried as an **organizing lemma + application**, not a headline theorem.
Theorem-developer + theory-auditor passes complete; all audit fixes incorporated
(notably Corollary 5's tractability "dichotomy" corrected to a three-tier
ladder). The genuinely novel parts: the optimal-report = resource-allocation
reduction, the feasibility-frontier map of scoring rules, and the identified-set
inversion (Corollary 5).

Remaining before manuscript insertion (all gated):
- Write the Theorem 3 ⟸ proof at full rigor (explicit unit-bijection +
  sender-side discrete-convexity bound).
- Verify Federgruen & Groenevelt (1986)'s exact condition phrasing for the
  separable case; add the four classical references to `references.bib`.
- Decide placement (organizing lemma in §3; §5 Hamming/Chebyshev reframed as the
  two failure modes) — a manuscript-revision decision, not taken yet.

### Master threshold theorem — theorem-development memo (2026-06-10)

New exploration memo: `_context/exploration/master_threshold_theorem.md`
(companion checks: `scripts/explore_master_threshold.py`). It develops the
generalization the user proposed (sharp bounds from Lemma 1's hypotheses):
under (S) separability + (C) discrete convexity + (M) monotone marginal
costs, the threshold/box-slice representation, interval coordinate
projections, and single-monotone-scalar-equation sharp coordinate bounds
hold for the WHOLE family — removing `feasibility_frontier.md` Corollary 5's
tier-(b) "rule-specific bonus" caveat; Propositions 1–2's closed forms drop
out of the crossing equation with explicit thresholds. Converse status:
order-preserving Hamming exclusion proven; argmin-level open; Prop 3′ of the
frontier memo found INCORRECT as stated (Hamming k=2 is the realized
exception; condition should be folded quasi-convexity). Manuscript flags:
the §3 RPS "separable count loss" sentence is imprecise (cumulative
coordinates). Gates before any manuscript edit: (1) a SECOND theory audit of
the corrected memo (the first audit mixed verified findings with fabricated
citations — see the memo's audit log); (2) a literature check on inverse
optimization for separable resource allocation (novelty gate for the
threshold inversion).

UPDATE 2026-06-10 (later the same day): gate (1) is PASSED. The second
audit ran under an evidence-rules protocol (all materials pasted inline;
findings must quote exact text) and returned "promote after fixes — no
structural rework". All fixes are applied to the memo: the Prop 3′
correction restricted to the open simplex (the audit found a real
degenerate-belief counterexample to the original quantifier), an
extended-real Lemma 1 paragraph added as Gap 8, C_0 qualifiers in A(ii)/(iv),
the unbounded-C endpoint restatement, and four wording repairs. Both
manuscript flags are now recorded in `_context/current_issues.md`.
Remaining gates: (2) the inverse-optimization literature check, then the
author's Light-vs-Full placement decision.

UPDATE 2026-06-10 (later still): gate (2) WAIVED by author decision —
novelty assumed provisionally; manuscript use must hedge "to our
knowledge"; the check should still run before submission (recorded in
`_context/current_issues.md`, Literature Issues).

DECISION 2026-06-10 (REVISED later the same day): the author initially
chose the Full restructure, then — after a value comparison — settled on
the **LIGHT integration**, with Full held in reserve for the revision
stage. Rationale: Light is consistent with the recorded venue strategy
(ADR 2026-05-21: general-interest journal, "the body stays light on
machinery"); the Light → Full upgrade path is cheap (the theorem is
developed and twice-audited in the memo) while Full → Light would waste
polished work; and Light keeps the unchecked inverse-optimization novelty
claim out of the manuscript entirely.

**DIRECTION DECISION 2026-06-10 (latest): direction (C) — TWO PAPERS
(adopted; memo in `_context/exploration/direction_memos.md`).** Remark 1
was subsequently REMOVED from `03_scoring_rules.tex` by author decision
(the extended-real sentence was rephrased to stand alone; paper recompiles
clean at 33 pp, 0 errors, 0 undefined refs). The L2/L3 repairs and the
order-preserving Hamming exclusion remain in the manuscript.

**ACTIVE TASK LIST — Paper 1 finishing pipeline (approved):**
P0. Reconcile `scripts/` display labels/keys with the manuscript's renamed
    rules (pre-existing debt, recorded 2026-05-22; prerequisite for any
    new simulation work — outputs and CSVs are coupled).
P1. Misreporting robustness exercise (approved 2026-06-10): perturb
    optimal reports (center-bias per the §5.3 predictions, plus a
    one-count uniform-error variant), measure identified-set coverage of
    the true belief by rule across the design grid. Run the
    `simulation-plan` skill first; do not overwrite committed outputs;
    write results into the design-comparison or discussion section after
    a simulation-methodologist review.
P2. Final figures for the design comparison (approved 2026-06-10):
    regret heat-maps by (n,k,alpha) + win-share summary, from existing
    outputs.
P3. The focused external human read; then submission package. Venue tier
    recalibrated to field journals (Experimental Economics / JEBO / GEB).

**Paper 2 (methods companion) — GATED, not started:** sequence on
explicit author authorization only: (i) inverse-optimization literature
check (conservative mode, per CLAUDE.md constraint 3); (ii) Chebyshev
ordinal hardening (finite coordinate-independence computation, offline);
(iii) appendix-grade write-up of the master theorem (memo Gaps 1, 8);
(iv) standalone draft. Inventory: `master_threshold_theorem.md`
(twice-audited), `feasibility_frontier.md` (audited, Prop 3' needs the
recorded amendment), `rule_candidate_screen.md`.

**STATUS UPDATE — Light integration EXECUTED 2026-06-10 (same day,
after explicit author go-ahead).** L1–L4 implemented in
`03_scoring_rules.tex` (Remark `rem:threshold`; RPS sentence fixed;
extended-real sentence added) and `07_discussion.tex` (order-preserving
Hamming exclusion). L5 done: paper compiles clean (34 pp, 0 errors, 0
undefined refs) and a targeted theory-audit (evidence-rules protocol)
returned "publishable after listed fixes" — all fixes applied and
re-compiled: the Hamming passage's orientation corrected to "strictly
increasing transformation of the expected LOSS" (the audit's one real
error catch), the remark's threshold/CDF-units reparameterization made
explicit (c vs Proposition 3's c in [0,1]), the Manhattan
CDF-monotonicity clause added for the box claim, the boundary-belief
sentence given the finite-competitor parenthetical and
restrict-to-support clause, and "plays the role of a Lagrange
multiplier". No web access of any kind was used; no citations were added.
The offline/no-Full constraints in CLAUDE.md remain in force. Remaining
before submission: the focused external human read (unchanged from the
pre-existing plan).

The original task description follows for the record.

**ACTIVE TASK — Light integration (NOT yet executed; manuscript still
untouched).** All math content must come verbatim from the twice-audited
memo `_context/exploration/master_threshold_theorem.md`; guardrail mode.
Scope — only `03_scoring_rules.tex` and `07_discussion.tex` change; no
proposition statements or proofs, no intro/abstract/setup changes.

**BINDING EXECUTION CONSTRAINTS (author-imposed, 2026-06-10):**
(a) Implement L1–L5 ONLY. Do NOT implement any part of the reserve Full
    plan below, in whole or in part, under any reading of this file.
(b) The Light execution is strictly OFFLINE: no literature search, no web
    search, no web fetching, and no downloading of any material. Do not
    dispatch `literature-reviewer` or any web-capable agent. The only
    inputs are repository files and the audited memo. (The L5 audit uses
    `theory-auditor`, which has no web tools — read/grep/glob only.)
(c) No new citations are added to `references.bib` (none are needed; the
    remark and the Hamming sentence use only already-cited sources).

L1. `03_scoring_rules.tex` §3.1: add a Remark after Lemma 1 stating the
    threshold representation ONLY (memo Theorem A(i): the single-transfer
    inequalities hold iff a common threshold c separates all sender
    marginals from all receiver marginals — a two-line max–min argument
    given discrete convexity), noting Prop 3's Manhattan threshold
    representation is its instance and that for squared-distance and
    frequency-guessing the threshold inequalities invert to additive and
    multiplicative boxes. Do NOT state parts (ii)–(v) (box-slice union,
    interval projections, scalar-equation bounds, functional sweep) —
    those stay in the memo for the reserve Full option.
L2. Same file: fix the RPS sentence (memo manuscript flag (a)) —
    asymmetric-absolute losses are governed by the lemma in the same way;
    RPS is separable in *cumulative*, not per-category, counts and falls
    outside the lemma as stated.
L3. Same file: add the extended-real convention line (memo flag (b) /
    Gap 8) — frequency-guessing's log costs are +infinity at boundary
    beliefs; marginals are defined by continuous extension from (0,1).
L4. `07_discussion.tex` (sec:other-rules): strengthen the Hamming
    paragraph with the order-preserving exclusion (memo R2): the existing
    n=3, k=5 instance certifies that no strictly increasing transform of
    the Hamming expected score is separable with discrete-convex
    coordinates. Do not state the argmin-level version (open).
L5. Compile clean (latexmk); targeted theory-audit of the new remark and
    the Hamming sentence using the evidence-rules protocol (paste all
    materials inline — the theory-auditor cannot see the working tree).

**RESERVE PLAN — Full restructure (revision-stage option, NOT
authorized).** Nothing in this file authorizes starting this plan. It may
be deployed ONLY on a new, explicit author instruction in a future session
(plausible triggers: a referee asks for the general theorem, or the venue
target shifts to a methods outlet — but the triggers themselves authorize
nothing). Its precondition — the waived inverse-optimization literature
check — likewise runs ONLY on explicit author instruction, under
author-approved access terms (conservative mode: abstracts plus
arXiv/SSRN/RePEc/official open-access full texts only; no paywall
circumvention; no browser-session tools; no files saved locally). Under
Light, that check gates nothing about submission. Original Full steps,
retained solely for that contingency:

1. `03_scoring_rules.tex` §3.1: KEEP Lemma 1 as-is (its core is classical
   — do not fold it into a claimed theorem); after it, define monotone
   marginals (M) and state a new Theorem (threshold inversion and sharp
   bounds; memo Theorem A(i)–(v)) with "to our knowledge" hedging; add the
   extended-real convention line (memo Gap 8); fix the RPS sentence
   (separable in cumulative, not per-category, counts — present as
   adjacent, not covered); cite the convex location-loss family with the
   origin condition and the pinball/quantile example (memo C4) as the
   wider-family payoff.
2. Rule subsections: one connecting sentence each — squared: additive
   boxes of width 1/n, closed forms = crossing solutions (c* = 2/m−1 etc.,
   memo C1); frequency-guessing: multiplicative boxes, n+1 and n+k−1 as
   crossing thresholds (memo C2); Manhattan: Prop 3's threshold
   representation = the theorem's part (i) instance (memo C3). Keep all
   existing proposition statements and proofs unchanged.
3. `08_appendix.tex`: new subsection after `app:lemma-proof` with the
   appendix-grade theorem proof — honest range C_0, extended-real
   paragraph, box-slice/interval-C argument, interval projections,
   crossing-or-no-crossing dichotomy with witness/compactness attainment,
   slice-LP part, location-family corollary (convexity preservation +
   Abel summation + strictness); optional short remark showing the
   two-line crossing recoveries of Props 1–2.
4. `07_discussion.tex` (sec:other-rules): add the order-preserving Hamming
   exclusion (memo R2) using the existing n=3, k=5 example — "no strictly
   increasing transform of the Hamming expected score is separable with
   discrete-convex coordinates"; argmin-level version stays unstated
   (open).
5. `02_setup.tex` closing sentence, `01_introduction.tex` contribution
   paragraph + the long footnote, and the abstract in `main.tex`: modest
   updates so the headline includes the general theorem (hedged).
6. Compile clean (latexmk); then a proof-audit pass on the NEW appendix
   subsection using the evidence-rules protocol (paste all materials
   inline — the theory-auditor cannot see the working tree; see the memo's
   audit log); before submission, run the waived inverse-optimization
   literature check.

### Feasibility-frontier lemma — inserted into the manuscript (2026-05-22)

Done. `paper/sections/03_scoring_rules.tex` now opens with a new subsection
"Optimal Reports as a Resource-Allocation Problem" — Lemma~\ref{lem:transfer}
(the single-transfer characterization), framed as an organizing lemma that the
three rule subsections instantiate. `07_discussion.tex` §5.2 reframes Hamming
and Chebyshev as the lemma's two failure modes. Four classical references added
to `references.bib` (Fox 1966; Federgruen--Groenevelt 1986; Ibaraki--Katoh 1988;
Murota 2003). The optimization result is cited as classical, not claimed new;
the stated contribution is the resource-allocation reduction + the identified-set
inversion. Paper compiles clean (26 pp). Open: a human read of the new
subsection for exposition; optionally a standalone appendix proof of the lemma
(currently it cites the classical result and points to the Manhattan appendix
proof as the worked exchange argument).
