# CLAUDE.md

This repository contains an academic microeconomics research project on belief elicitation with frequency reports.

The active paper is:

> The Informational Efficiency of Frequency-Report Scoring Rules

The project studies what a researcher can infer about latent multinomial beliefs \(p\) from an observed incentivized count report \(r\), given that each scoring rule induces an optimal-report correspondence and therefore an inverse belief region
\[
P_S(r)=\{p:r\in R_S(p)\}.
\]

The repository combines academic paper writing, mathematical proof checking, literature review, research strategy, and reproducible simulation code.

## ACTIVE AUTHOR-IMPOSED CONSTRAINTS (2026-06-10, amended same day after the direction-C decision)

These override anything else in this file or in `_context/` until the author explicitly lifts them:

1. The adopted direction is **(C): two papers** (decision memo in `_context/exploration/direction_memos.md`). The approved scope for **paper 1** (the current manuscript) is: the executed Light integration, the executed Remark-1 removal, the misreporting robustness exercise, and final figures — nothing else. The master-threshold machinery must NOT enter paper 1; it is reserved for the future **paper 2** (methods companion), which must not be drafted without a new, explicit author instruction.
2. All approved work is **strictly offline**: no literature search, no web search, no web fetching, no downloading of any material, and no dispatching of `literature-reviewer` or any web-capable agent, except on explicit author instruction. Inputs are repository files and the `_context/` memos.
3. The deferred inverse-optimization literature check (precondition for paper 2) runs ONLY on explicit author instruction, under author-approved access terms (conservative mode; no paywall circumvention; no local PDF saving).

## Core distinction: exploration vs manuscript claims

Claude is allowed and encouraged to explore alternative directions for the project.

However, exploratory ideas must not be silently converted into manuscript claims.

Use two modes:

### Exploration mode

Use this mode for:

- online literature discovery;
- identifying related literatures;
- proposing alternative framings;
- suggesting new theorem directions;
- suggesting new simulation exercises;
- assessing whether the paper should pivot, narrow, or expand.

Exploration output belongs in:

- `_context/exploration/direction_memos.md`
- `_context/exploration/literature_scan_log.md`
- `_context/exploration/rejected_directions.md`
- `_context/next_steps.md`

Exploration may be creative, speculative, and comparative, but it must clearly label uncertainty.

### Guardrail mode

Use this mode for:

- manuscript edits;
- theorem statements;
- proof revisions;
- citation claims;
- final contribution statements;
- simulation interpretation;
- abstract/introduction claims.

Guardrail mode must be conservative, academically precise, and evidence-based.

No exploratory claim may enter the paper unless it has passed the relevant checks:

1. literature check;
2. theory/proof check, if formal;
3. simulation/code feasibility check, if computational;
4. contribution-positioning check.

## Repository structure

Important files and folders:

- `paper/main.tex`: main LaTeX entry point.
- `paper/references.bib`: bibliography.
- `paper/sections/01_introduction.tex`: introduction.
- `paper/sections/02_setup.tex`: formal setup.
- `paper/sections/03_scoring_rules.tex`: main scoring-rule analysis.
- `paper/sections/06_design_comparison.tex`: informational-efficiency design exercise.
- `paper/sections/06_risk_attitudes.tex`: risk-aversion section.
- `paper/sections/07_discussion.tex`: discussion.
- `paper/sections/08_appendix.tex`: appendix.
- `scripts/verify_regions.py`: computational checks for rule characterizations and examples.
- `scripts/design_efficiency.py`: simulation/design-efficiency exercise.
- `outputs/design_exercise/`: final simulation outputs (the run the paper tables and `scripts/consistency_check.py` read); `outputs/simulation_design/` holds the older committed run.
- `_context/current_status.md`: current project status.
- `_context/current_issues.md`: known issues and risks.
- `_context/next_steps.md`: next planned tasks.
- `_context/related_literature/`: local literature PDFs and literature notes.
- `_context/exploration/`: exploratory direction memos and literature scans.

Generated LaTeX files such as `.aux`, `.bbl`, `.blg`, `.fdb_latexmk`, `.fls`, `.log`, `.out`, `.synctex.gz`, and generated PDFs should generally not be edited.

## Current research framing

The current paper is a methodological research paper on the informativeness of frequency-report scoring rules, framed as a partial-identification problem. The "note" label that appeared in earlier project docs is retired: at 31 pages with three propositions, two lemmas, a corollary, a full design comparison, and an asymmetric-Dirichlet robustness check, the manuscript is a research paper, not a note.

The current conceptual pipeline is:

1. Elicitation mechanism.
2. Optimal-report correspondence.
3. Inverse belief region.
4. Belief and mean bounds.
5. Informational-efficiency comparison.
6. Risk-aversion and implementation discussion.

This pipeline is the current baseline, not a permanent constraint. Claude may propose alternatives in exploration mode.

Possible alternative directions may include, but are not limited to:

- a stronger mechanism-design framing;
- a belief-identification framing;
- an econometric partial-identification framing;
- a behavioral-experimental framing;
- a decision-theoretic scoring-rule framing;
- a design-comparison paper focused on implementation tradeoffs;
- a shorter methodological note with narrower claims.

Alternative directions must be evaluated before paper edits are made.

## Active rules

The paper headlines three rules (ADR-0001 fourth amendment; current state recorded in `_context/current_status.md`):

1. Squared-distance frequency scoring (the analytical centrepiece; previously called "quadratic-distance").
2. Frequency-guessing scoring (the known exact-match / discrete-metric rule of Schlag–Tremewan; previously called "discrete-metric").
3. Manhattan-distance frequency scoring.

Hamming and Chebyshev distance are NOT headline rules. They appear only in the discussion subsection "Other Frequency-Report Scoring Rules and the Limits of the Approach":

- Hamming has an exact identified set, a closed-form modal-box inner bound, and a `k=2` closed form, but its sharp `k>2` bounds need numerical optimization over a non-convex set that is intractable at the design grid's scale, and single-transfer optimality fails even at interior beliefs.
- Chebyshev's expected loss does not separate across coordinates and has no clean optimal-report characterization for `k>2`.

Older text below this section that still references "four rules" or "Hamming as headline" reflects the pre-2026-05-21 plan and is superseded.

## Three-rule research objective

The current objective is to compare the informativeness of three frequency-report scoring rules: squared-distance, frequency-guessing, and Manhattan.

For each rule, the project characterizes:

1. the induced optimal-report correspondence;
2. the identified set \(P_S(r)\);
3. coordinate bounds, if analytically tractable;
4. mean or linear-functional bounds, if analytically tractable;
5. computational bounds where closed-form analytical bounds are unavailable;
6. performance in a three-rule comparison over \(n\), \(k\), and latent belief distributions \(p\).

The analytical status:

1. Squared-distance: closed-form identified set, closed-form coordinate bounds, LP mean bounds.
2. Frequency-guessing: closed-form coordinate bounds and mean bounds (Schlag–Tremewan); the present paper restates them for self-containment.
3. Manhattan: exact identified set; sharp one-dimensional coordinate bounds (Lemma `lem:manhattan-unimodal`); sharp mean bounds via threshold-grid optimisation.

If closed-form analytical bounds are unavailable, the paper says so explicitly and uses computational bounds or simulation evidence carefully.

## Main contribution candidates

The current main contribution candidates are:

1. A transparent identified-set and bound characterization for squared-distance frequency scoring (the analytical centrepiece).
2. A unified three-rule comparison of squared-distance, frequency-guessing, and Manhattan frequency-report scoring rules, organised by a single structural condition (separability plus discrete convexity) that Hamming and Chebyshev each violate.
3. A design exercise showing which rule performs best in which contexts, varying \(n\), \(k\), and latent belief structure \(p\).

The project should not assume ex ante that one rule is uniformly best.

The target conclusion should be contextual:

- which rule performs better for which inferential objective;
- under which \(n\), \(k\), and belief-distribution regimes;
- for which metric, such as average coordinate width, worst-coordinate width, mean-bound width, or other relevant informational-efficiency criteria.

## Known mathematical constraints

Preserve the following distinctions:

- The discrete-metric rule is the known exact-match/fixed-prize rule and should be attributed carefully.
- The quadratic-distance rule currently has the strongest analytical characterization.
- Manhattan multi-category bounds are currently threshold-computed and should not be described as closed form unless a valid derivation is added.
- Hamming-distance bounds should be actively investigated. Do not assume they are analytically impossible without a documented attempt.
- Mean bounds must be stated as optimizations over the full inverse belief region, not as combinations of coordinate intervals.
- Chebyshev distance is currently secondary and should not be part of the headline horse race unless explicitly promoted.
- Finite computational checks are not mathematical proofs.
- Simulation evidence is not proof of uniform dominance.

For Manhattan and Hamming, Claude should distinguish:

1. closed-form analytical bounds;
2. semi-analytical characterizations;
3. finite optimization formulations;
4. threshold-computed bounds;
5. simulation-only evidence.

## Simulation and design-comparison objective

The simulation is a three-rule comparison among:

1. squared-distance;
2. frequency-guessing (discrete-metric / exact match);
3. Manhattan distance.

Hamming is excluded because its sharp `k>2` bounds are computationally intractable at the design grid's scale (ADR-0001 second amendment); Chebyshev because its expected loss does not separate across coordinates. The purpose is to identify which rule is more informative in which contexts.

The relevant design dimensions are:

- number of trials \(n\);
- number of categories \(k\);
- latent belief structure \(p\);
- belief concentration/dispersion, for example through Dirichlet parameters;
- inferential objective, such as coordinate bounds, worst-coordinate bounds, and mean or linear-functional bounds.

The simulation should allow contextual conclusions of the form:

- Rule A performs better for sparse beliefs and larger \(k\).
- Rule B performs better for balanced beliefs.
- Rule C performs better for average coordinate width.
- Rule D performs better for worst-coordinate or mean-oriented inference.

Do not seek a uniform winner unless the evidence strongly supports one.

## Simulation metrics

The simulation should focus on informational-efficiency metrics, not payment probabilities.

Relevant metrics include:

- average coordinate-bound width;
- worst coordinate-bound width;
- average linear-functional or mean-bound width;
- worst linear-functional or mean-bound width;
- volume or proxy-volume of inverse belief regions, if computationally feasible;
- frequency of winning by metric and design cell;
- rank distribution across rules by design cell;
- regret relative to the best rule in each cell.

The existing winning-probability/payment-probability component is not central to the paper because only the discrete-metric / frequency-guessing rule pays based on exact correctness in that sense.

Payment probability may be discussed only as an implementation issue for the frequency-guessing / discrete-metric rule, not as a symmetric horse-race metric across rules.

## Interpretation risks

Avoid the following claims in manuscript text:

- Do not claim that any rule is uniformly best.
- Do not claim that the paper invents frequency guessing.
- Do not claim that the exact-match mechanism is new.
- Do not claim distance rules are robust to risk aversion under direct monetary payments.
- Do not oversell the cognitive advantage of frequency reports without additional empirical evidence.
- Do not describe grid or simulation evidence as proof.

Exploration documents may discuss such ideas as hypotheses or risks, but must label them as unverified.

Additional interpretation risks for the rule comparison:

- Do not compare payment probabilities across rules as if they were common informativeness metrics.
- Do not treat exact-match winning probability as relevant for Manhattan or squared-distance rules unless the payment implementation is explicitly defined.
- Do not describe the comparison as behavioural evidence; it is conditional on optimal reporting.
- Do not claim Hamming is inferior; the project's position is that Hamming has an exact identified set but no tractable sharp bounds at the design grid's scale.
- Do not imply that computational bounds are analytically closed form.

## Literature review policy

The literature reviewer should actively search online when asked to perform a literature scan.

The literature reviewer should:

- identify related papers;
- summarize each paper’s relevant contribution;
- explain how it relates to the current paper;
- distinguish direct competitors from background literature;
- identify novelty risks;
- suggest how the paper should position itself;
- recommend citations or citation checks.

The literature reviewer must not:

- invent citations;
- invent page numbers;
- claim to have read a paper that was only found via abstract or metadata;
- treat online search snippets as sufficient evidence for detailed claims;
- move citations into the manuscript without verification.

Important existing sources include:

- Schlag–Tremewan for simple/frequency belief elicitation.
- Schlag et al. for belief-elicitation methods.
- Armantier–Treich for incentives, stakes, hedging, and risk-aversion concerns.
- Hogarth for probability-assessment motivation.
- Savage, Selten, and Gneiting–Raftery for scoring-rule background.

## Direction-search policy

Claude may investigate whether the current project direction is the best one.

Direction-search output must be organized as a memo with:

1. candidate direction;
2. central research question;
3. relation to current draft;
4. required literature;
5. required theorem/proof work;
6. required simulation/code work;
7. contribution potential;
8. feasibility;
9. risk of slop or overclaiming;
10. recommendation.

Direction-search memos belong in:

- `_context/exploration/direction_memos.md`

Rejected directions should be summarized in:

- `_context/exploration/rejected_directions.md`

A direction may be proposed aggressively, but adoption into the paper must be conservative.

## Workflow rules

Before substantial research work, read:

1. _context/current_status.md
2. _context/current_issues.md
3. _context/next_steps.md
4. relevant paper section(s)
5. relevant script(s), if the task involves simulations or verification
6. relevant exploration files, if the task concerns project direction

For substantial tasks:

1. Identify whether the task is exploration mode or guardrail mode.
2. Restate the immediate objective.
3. Identify affected files.
4. Inspect relevant context.
5. Make minimal coherent edits, unless explicitly asked for a broad exploration memo.
6. Update or recommend updates to context files if the project state changes.
7. Distinguish completed changes from remaining open issues.

## LaTeX rules

- Preserve notation unless there is a documented reason to change it.
- If notation changes, update the relevant explanatory text and flag the change.
- Keep theorem/proposition statements conservative.
- Do not introduce unsupported claims.
- Do not rewrite entire sections unless explicitly requested.
- Prefer targeted edits over broad stylistic rewrites.
- Keep academic prose precise and non-generic.

## Code rules

Use uv commands from the README.

Relevant checks:

```bash
uv run python scripts/verify_regions.py
uv run python -m py_compile scripts/design_efficiency.py scripts/verify_regions.py
```

The final design exercise command is:

```bash
uv run python scripts/design_efficiency.py --final --draws 5000
```

Before editing simulation code, inspect how outputs are written and how paper tables depend on them.

Do not overwrite final outputs unless explicitly asked.

## Preferred use of subagents

Use:

- `literature-reviewer` for online literature discovery, citation checking, and related-work positioning.
- `research-strategist` for identifying alternative project directions and deciding whether the current framing is optimal.
- `theory-auditor` for mathematical claims and proof checking.
- `simulation-methodologist` for the design exercise and simulation interpretation.
- `paper-editor` for LaTeX exposition and section rewriting.
- `code-reviewer` for Python scripts and reproducibility checks.
- Use the `rule-comparison` skill whenever comparing the three headline rules or revising the design-comparison section.
- Use the `analytical-bounds-search` skill before concluding that a rule lacks analytical bounds.

For exploratory work, combine `literature-reviewer` and `research-strategist`.

For manuscript work, combine `paper-editor` with `theory-auditor` or `literature-reviewer` as needed.

## Agent skills

### Issue tracker

Issues live on GitHub (`armoutihansen/frequency-beliefs`); use the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repo: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.