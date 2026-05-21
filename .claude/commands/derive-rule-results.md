Develop analytical results for a specified scoring rule.

Use this command especially for Manhattan and Hamming distance rules.

If no rule is specified, ask which rule to analyze.

## Steps

1. Read:
   - `CLAUDE.md`
   - `_context/current_status.md`
   - `_context/current_issues.md`
   - `_context/next_steps.md`
   - `paper/sections/02_setup.tex`
   - `paper/sections/03_scoring_rules.tex`
   - `paper/sections/08_appendix.tex`
   - `scripts/verify_regions.py`
   - `scripts/design_efficiency.py`

2. Use:
   - `theorem-developer`
   - `theorem-development` skill
   - `analytical-bounds-search` skill
   - `rule-comparison` skill if comparing to other rules

3. For the specified rule, derive or attempt to derive:

   - expected loss;
   - optimal-report correspondence;
   - inverse belief region;
   - coordinate bounds;
   - mean or linear-functional bounds;
   - special cases;
   - computational fallback formulation.

4. Search especially for:

   - \(k=2\) results;
   - general-\(k\) finite inequality systems;
   - one-coordinate deviation characterizations;
   - exchange-deviation characterizations;
   - boundary-report cases;
   - interior-report cases;
   - monotonicity or dominance lemmas;
   - counterexamples to overly strong claims.

5. Produce candidate results using this status classification:

   - theorem-ready;
   - proposition-ready;
   - lemma-ready;
   - corollary-ready;
   - proof sketch only;
   - conjecture;
   - computationally supported;
   - special case only;
   - false as initially stated;
   - unresolved.

6. Then ask the `theory-auditor` agent to audit the most promising candidate result.

7. Output:

   - derivation memo;
   - candidate theorem/proposition/lemma/corollary statements;
   - audit summary;
   - safe claims;
   - unsafe claims;
   - next derivation tasks.

## Rules

- Do not edit the paper unless explicitly asked.
- Do not present conjectures as theorems.
- Do not claim closed-form bounds unless actually derived.
- Do not treat computational checks as proofs.
- Do not demote Hamming merely because it is analytically difficult.
- Compare Manhattan and Hamming symmetrically where relevant.