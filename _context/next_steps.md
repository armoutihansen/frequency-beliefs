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
