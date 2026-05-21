Run a proof audit on the specified claim, theorem, proposition, or section.

If no specific claim is provided, prioritize the quadratic-distance result in `paper/sections/03_scoring_rules.tex`.

Steps:

1. Read:
   - `_context/current_status.md`
   - `_context/current_issues.md`
   - `_context/next_steps.md`
   - `paper/sections/02_setup.tex`
   - relevant part of `paper/sections/03_scoring_rules.tex`

2. Use the `theory-auditor` agent.

3. Classify the claim as one of:
   - valid;
   - valid but incomplete;
   - unclear notation;
   - true under stronger assumptions;
   - unsupported by current proof;
   - false as stated;
   - computationally checked but not analytically proven.

4. Report:
   - exact claim;
   - assumptions;
   - proof logic;
   - gap or risk;
   - minimal correction;
   - whether `_context/current_issues.md` should be updated.

Do not edit LaTeX unless explicitly asked.