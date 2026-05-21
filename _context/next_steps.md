# Next Steps

Date: 2026-05-21

> **ACTIVE TASK — paper revision.** Steps 1–6 below are complete. The current
> work is the structural and exposition revision specified in
> **`_context/revision_plan.md`** — a fresh session should start there.

These steps follow the direction decided in the 2026-05-21 grilling session. See
`CONTEXT.md` for the glossary, `docs/adr/0001` and `docs/adr/0002` for the two
hard-to-reverse decisions, and `_context/exploration/direction_memos.md` for the
adopted-direction memo.

## Action sequence

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
