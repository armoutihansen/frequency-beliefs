# Refactor the project conceptually toward a four-rule comparison.

The four headline rules are:

1. Quadratic distance.
2. Discrete metric / exact match.
3. Manhattan distance.
4. Hamming distance.

Chebyshev remains secondary unless explicitly promoted.

Steps:

1. Read:
   - `CLAUDE.md`
   - `_context/current_status.md`
   - `_context/current_issues.md`
   - `_context/next_steps.md`
   - `paper/main.tex`
   - `paper/sections/01_introduction.tex`
   - `paper/sections/02_setup.tex`
   - `paper/sections/03_scoring_rules.tex`
   - `paper/sections/06_design_comparison.tex`
   - `paper/sections/08_appendix.tex`
   - `scripts/verify_regions.py`
   - `scripts/design_efficiency.py`

2. Use:
   - `research-strategist`
   - `theory-auditor`
   - `simulation-methodologist`
   - `code-reviewer`

3. Produce a four-rule refactor memo with:

   - current treatment of each rule;
   - what must change for Hamming to be treated symmetrically with Manhattan;
   - analytical tasks for Manhattan;
   - analytical tasks for Hamming;
   - code changes needed for `design_efficiency.py`;
   - verification changes needed for `verify_regions.py`;
   - paper-section changes needed;
   - simulation-output changes needed;
   - risks of overclaiming;
   - recommended implementation sequence.

4. Do not edit the paper unless explicitly asked.

5. Do not remove existing simulation outputs unless explicitly asked.

6. Do not rerun the final simulation unless explicitly asked.