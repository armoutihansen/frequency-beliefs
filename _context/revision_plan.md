# Paper Revision Plan — Handoff (2026-05-21)

> **STATUS — COMPLETE (2026-05-21).** The three-rule revision was executed.
> Steps 1–6 below were carried out with decisions D1–D3 applied, and the author
> additionally removed Hamming from the headline analysis (ADR-0001 fourth
> amendment): the paper now headlines three rules, and Hamming and Chebyshev are
> covered in a new discussion subsection, "Other Count-Loss Rules and the Limits
> of the Approach," which states their obstructions precisely (Hamming's §3
> non-sufficiency point uses the interior uniform-belief counterexample). The
> paper compiles cleanly — 0 undefined references; one pre-existing overfull box
> remains in the untouched risk-aversion paragraph. The steps below are retained
> as the executed record. A final end-to-end exposition read was also done
> (2026-05-21): the closed-form comparison was promoted to its own subsubsection,
> minor repetition trimmed, the one large pre-existing overfull box fixed, and
> the design-comparison robustness checks (alternative outcome vector; tie rate)
> surfaced from the existing simulation output into the appendix rather than
> left as deferred "open questions". The paper compiles cleanly: 0 undefined
> references, no errors, one negligible sub-2pt overfull box. Remaining before
> submission: a focused external read by a human reader.
>
> Three grilling-session decisions carry into the eventual revision and amend
> the steps below:
> - **D1 (amends Step 1 and §1).** The moved §3 crossover paragraph and the §4
>   back-reference must say the ranking turns on *report* concentration — the
>   count `m` of positive-report categories — because the §3 bounds are a
>   statement about `m(r)`, not about beliefs. §4 ties report concentration to
>   belief concentration. §1's "it does not need the simulation" overclaims: §3
>   owns the report-level crossover, §4 owns the belief-level one.
> - **D2 (amends Step 5).** Canonical term is "design comparison"; "design
>   exercise" is retired (CONTEXT.md glossary updated). Section title unchanged.
> - **D3 (amends Step 3).** The contribution paragraph leads with the three
>   concrete new characterizations (quadratic closed-form; Manhattan sharp
>   semi-analytical; Hamming obstruction + sandwich) and the contingent decision
>   rule. Partial identification is named as the organizing lens, not asserted
>   as the headline novelty.

## How to use this document

Self-contained handoff for a fresh Claude Code session; the prior session ran low
on context. Read §0 to orient, then execute the §2 steps in order, compiling and
checking after each. The paper is in good shape — this is a focused structural and
exposition revision, not a rewrite. Work in guardrail mode: conservative, targeted
edits; preserve theorem/proof content; do not introduce unsupported claims.

## 0. Orientation

### The paper
`paper/main.tex` — an economics methods paper, "The Informational Efficiency of
Frequency-Report Scoring Rules." A subject has latent multinomial beliefs `p`; an
incentivized frequency-report scoring rule elicits a count report `r`; each rule
`S` induces an identified set `P_S(r) = {p : r ∈ R_S(p)}` and finite-sample bounds
on the latent probabilities and on linear functionals. The paper recasts belief
elicitation as partial identification, characterizes four rules, and compares
which is most informative.

### Current section structure
1. Introduction — `sections/01_introduction.tex`
2. Setup — `02_setup.tex`
3. Frequency-Report Scoring Rules — `03_scoring_rules.tex`
   (§3.1 Rules with Closed-Form Bounds: quadratic-distance, discrete-metric;
   §3.2 Rules Without Closed-Form Bounds: Manhattan, Hamming)
4. Informational Efficiency: A Design Comparison — `06_design_comparison.tex`
   (the simulation / design exercise)
5. Discussion — `07_discussion.tex`
6. Appendix — `08_appendix.tex` (proofs; design-exercise details)

### Decision record — READ THESE FIRST
- `CLAUDE.md` — project instructions and guardrails.
- `CONTEXT.md` — glossary. The object is the "identified set" `P_S(r)`; the legacy
  term "inverse belief region" is retired.
- `docs/adr/0001-...md` — the four rules sit on an analytical-to-computational
  spectrum (quadratic and discrete-metric: closed form; Manhattan: semi-analytical
  / sharp; Hamming: computational). Hamming is a headline rule analytically but
  is NOT in the simulation horse race.
- `docs/adr/0002-...md` — risk neutrality is the maintained body assumption; the
  binary-lottery extension to risk-averse EU subjects is argued in the discussion.
- `_context/current_status.md`, `current_issues.md`, `next_steps.md`.
- `_context/exploration/bounds_search_manhattan_hamming.md` — the audited
  Manhattan/Hamming derivations.

### Build
From the repo root: `cd paper && latexmk -pdf -interaction=nonstopmode main.tex`
— run it TWICE so cross-references settle. Verify with
`grep -ci undefined main.log` → should be `0`. NOTE: the shell working directory
tends to drift to the repo root between commands — always `cd` into `paper/`
before compiling.

### Working style
Guardrail mode. Compile after every step. The user wants genuine pushback on
design decisions, not deference (see auto-memory). When done, update
`_context/current_status.md`, `current_issues.md`, and `next_steps.md`.

## 1. Purpose of this revision

The paper's **organizing question** — confirmed with the author — is *when is each
scoring rule optimal*, where "optimal" means *most informationally efficient* (the
rule whose identified set gives the tightest bounds). The answer is **contingent**
on the inferential target (coordinate vs. linear-functional/mean) and the belief
regime (how concentrated the subject's beliefs are). The paper delivers a
contingent decision rule, not a single winner.

The paper's **claimed novelty** is NOT "comparing scoring rules" — generic
multi-rule elicitation comparisons already exist (see the literature scan in
`_context/exploration/literature_scan_log.md`; Schlag–Tremewan already derive
belief bounds from frequency reports). The claimed novelty is the
**partial-identification framework** (each rule → identified set → finite-sample
bounds) and the **closed-form characterizations** that make the "when is each rule
optimal" answer rigorous. The introduction and abstract must locate the novelty
there, not in the act of comparing.

**Trigger for the revision.** The discrete-vs-quadratic crossover — which of the
two rules gives tighter average-coordinate bounds — is **analytically derivable**
from the §3 closed-form bounds; it does not need the simulation. The paper is
currently structured as if the simulation (§4) carries that comparison. The
revision re-balances:

- §3 should **own** the analytic comparison of the two closed-form rules.
- §4 (the simulation) should be framed honestly as what it uniquely adds: it
  **confirms** the analytic crossover, **quantifies** it (win shares, the α≈1
  crossover location, regret magnitudes), and **extends** the comparison to
  Manhattan distance, which has no closed-form bound and cannot be compared
  analytically.
- The introduction and abstract should reflect this analytical/computational
  split.

Plus an exposition/consistency pass to clear artifacts left by many local edits.

### Verified facts the revision relies on (do not re-derive incorrectly)
- Discrete-metric coordinate-bound width for category `i`:
  `[r_i(k-2)+(n+k-1)] / [(n+1)(n+k-1)]` — linear in `r_i`.
- Because `Σ r_i = n`, the **average** discrete-metric coordinate width over the
  `k` coordinates is a **constant** (independent of the report):
  `(k-1)(2n+k) / [k(n+1)(n+k-1)]`. (Checked: `n=20,k=5` → `0.0714`.)
- Quadratic-distance coordinate width, positive-report category:
  `2/n - 1/(nm) - 1/(nk)` where `m = m(r)` = number of categories with positive
  reported counts — independent of `r_i`, shrinks as the report concentrates
  (smaller `m`). Zero-report category: width `m/(n(m+1))`.
- At `m=k` (balanced report) the average quadratic width exceeds the discrete
  constant, for all `n≥1, k≥2` (proven). Hence the crossover.
- These are elementary algebra on the §3 closed-form bounds, which were audited
  sound on 2026-05-21.

## 2. Revision steps

### Step 1 — Move the analytic comparison of the closed-form rules from §4 to §3

`06_design_comparison.tex` currently opens its regime result (under the paragraph
header `\paragraph{The ranking is governed by belief concentration.}`) with a
paragraph deriving the closed-form crossover. That derivation belongs in §3.

1a. In `03_scoring_rules.tex`, insert a new `\paragraph` at the **end of §3.1** —
after the discrete-metric subsection's "Practical interpretation" paragraph and
immediately before `\subsection{Rules Without Closed-Form Bounds}`. Suggested text
(refine wording as needed; keep the math exact):

```
\paragraph{Comparing the two closed-form rules.}
The two closed-form rules can be compared directly through their coordinate-bound widths.
The discrete-metric coordinate width, \([r_i(k-2)+(n+k-1)]/[(n+1)(n+k-1)]\), is linear in the reported count \(r_i\); because \(\sum_i r_i=n\) fixes the average reported count at \(n/k\), the average of this width over the \(k\) coordinates is a constant,
\[
\frac{(k-1)(2n+k)}{k(n+1)(n+k-1)},
\]
the same for every report.
The quadratic-distance coordinate width for a positive-report category, \(2/n-1/(nm)-1/(nk)\) with \(m=m(r)\) the number of categories with positive reported counts, does not depend on \(r_i\) and shrinks as the report concentrates on fewer categories.
A report concentrated on few categories therefore has a small average quadratic width; a balanced report, with \(m=k\), has an average quadratic width that exceeds the discrete-metric constant.
Which of the two closed-form rules gives the narrower average coordinate bound thus turns on belief concentration, before any simulation---a contrast the design comparison of the next section quantifies and extends to Manhattan distance.
```

1b. In `06_design_comparison.tex`, replace the analytic opening paragraph with a
short back-reference. The regime result should now open:

```
\paragraph{The ranking is governed by belief concentration.}
Section~3 showed, from the closed-form bounds alone, that which of the two closed-form rules gives the narrower average coordinate bound turns on belief concentration.
The design comparison confirms and quantifies that crossover, and extends it to Manhattan distance, which has no closed-form bound.
Averaged over the whole grid the three rules barely differ---mean coordinate width \(0.103\), \(0.104\), and \(0.102\) for discrete-metric, quadratic-distance, and Manhattan scoring---because each rule's favourable and unfavourable regimes cancel.
Table~\ref{tab:regime-wins} reports the win shares---the share of belief draws on which a rule gives the narrowest interval---broken out by \(\alpha\).
```

Compile; check 0 undefined refs.

### Step 2 — Reframe §4 as confirm / quantify / extend

In `06_design_comparison.tex`, make the section's framing explicit: the design
comparison's role is to confirm the §3 analytic crossover, quantify it, and extend
the comparison to Manhattan (no closed form). The intro/framing paragraph already
calls the exercise "a diagnostic"; adjust it so the confirm/quantify/extend role
is stated. Do not overclaim — it remains conditional on optimal reporting and is
not behavioural evidence.

Consider (optional) whether the section title "Informational Efficiency: A Design
Comparison" should sharpen now that §3 owns the analytic comparison; "A Design
Comparison" still fits. Author's call — flag, do not force.

### Step 3 — Reframe the contribution: introduction and abstract

The introduction's contribution paragraph and the abstract must reflect §1 of this
plan: organizing question = "when is each rule optimal"; claimed novelty = the
partial-identification framework + the closed-form characterizations.

In `01_introduction.tex`, revise the contribution paragraph so it:
- states the **organizing question** explicitly — what can be inferred from a
  report, and which rule does it most informatively, in which regime;
- credits the **partial-identification framework** and the **characterizations**
  as the contribution (not "comparing rules");
- makes clear the closed-form rules' comparison is **analytic** (a consequence of
  the bounds), and the design exercise **quantifies and extends** it to Manhattan;
- keeps the existing honest positioning ("not a new exact-match mechanism;
  Schlag–Tremewan already derive belief bounds for the frequency-guessing rule").

In `main.tex`, revise the abstract for the same framing: lead with the question
and the partial-identification recast; note the closed-form characterizations; say
the design comparison quantifies the ranking and covers Manhattan.

Keep both conservative and precise. Do not call computed bounds "closed form";
do not call distance rules risk-aversion-robust without the EU + binary-lottery
qualifier.

### Step 4 — §5 discussion consistency

In `07_discussion.tex`, check the chain recap and the three regime-keyed
recommendations are consistent with the re-balanced framing (organizing question =
"when is each rule optimal"). The recommendations are already regime-keyed in
plain language; likely only light edits. Ensure nothing implies the comparison is
purely a simulation result.

### Step 5 — Exposition and consistency pass

End-to-end read of the paper; fix accumulated local-edit artifacts:
- `03_scoring_rules.tex` §3.1.2 opens "The second **primary** rule…" — orphaned
  wording, since the §3.1 heading was renamed "Rules with Closed-Form Bounds".
  Reword.
- `07_discussion.tex` has a single `\subsection` ("Risk Aversion and
  Implementation"). Decide: keep it, or de-subsection it (a lone subsection is
  mildly awkward).
- `06_design_comparison.tex` ends on the "Payment probability" paragraph (a
  discrete-metric implementation aside) — a slightly soft section closer.
  Consider a one-sentence closer or a light reorder.
- Terminology: "design exercise" vs. "design comparison" appear interchangeably.
  Pick one (recommend "design comparison") and use it consistently.
- Check every `\ref`/`\cite` resolves (0 undefined after compile).
- Confirm the introduction, §3, §4, §5, and the abstract tell one coherent story.

### Step 6 — Verification and wrap-up
- Compile clean: `cd paper && latexmk -pdf -interaction=nonstopmode main.tex`
  twice; `grep -ci undefined main.log` → `0`; check for overfull boxes.
- Sanity-check the analytic claims in the moved §3 paragraph (the constant
  `(k-1)(2n+k)/[k(n+1)(n+k-1)]` and the `m=k` inequality) — elementary algebra
  on the audited §3 bounds; a careful read suffices.
- Update `_context/current_status.md`, `current_issues.md`, `next_steps.md` to
  record the revision.

## 3. Do not break
- The audited proofs: the Manhattan single-unit-transfer **sufficiency** proof in
  Appendix `app:manhattan-proof`, and the quadratic-distance proof in
  `app:squared-proof` (its sufficiency step and the explicit endpoint-attaining
  vectors). Both were independently audited sound on 2026-05-21. Do not alter the
  mathematics; wording edits only, if any.
- ADR-0001 and ADR-0002 decisions: four-rule analytical taxonomy; Hamming not in
  the simulation; risk neutrality maintained in the body; binary-lottery
  extension in the discussion.
- The simulation outputs in `outputs/design_exercise/` are from the final run
  (`uv run python scripts/design_efficiency.py --final --draws 5000`); the §4 and
  appendix table numbers come from there. Do not re-run unless a table must
  change. The committed prior run in `outputs/simulation_design/` is untouched
  legacy — leave it.
- Retired term: never reintroduce "inverse belief region" — the term is
  "identified set".
- Never describe a computed bound (Manhattan mean bounds; Hamming `k>2` bounds)
  as closed form; never call distance rules robust to risk aversion without the
  "under expected utility, binary-lottery implementation" qualifier.

## 4. Open / deferred items (context, not blocking)
- The `\cite[Proposition 1]{SchlagTremewanSimple}` locator in §3 was verified
  correct against the local PDF.
- The 5 bibliography entries added in the citation pass (Roth–Malouf, Berg et al.,
  Karni, Hossain–Okui, Manski) are metadata-verified; no local PDFs.
- A final exposition polish and a focused external read remain after this
  revision, per `_context/current_issues.md`.
