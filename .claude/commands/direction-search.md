# Explore whether the current project is taking the best direction.

Steps:

1. Read:
   - `_context/current_status.md`
   - `_context/current_issues.md`
   - `_context/next_steps.md`
   - `_context/exploration/literature_scan_log.md`
   - `paper/main.tex`
   - `paper/sections/01_introduction.tex`
   - `paper/sections/02_setup.tex`
   - `paper/sections/03_scoring_rules.tex`
   - `paper/sections/06_design_comparison.tex`
   - `paper/sections/06_risk_attitudes.tex`

2. Use the `research-strategist` agent and the direction-search skill.

3. Consider at least these candidate directions:
   - four-rule informational-efficiency horse race with quadratic, discrete metric, Manhattan, and Hamming as headline rules;
   - current methodological-note framing;
   - narrower quadratic-distance contribution;
   - partial-identification framing;
   - mechanism-design framing;
   - experimental-design framing;
   - scoring-rule theory framing;
   - computational design-comparison framing;
   - split-paper option.

4. Produce a direction memo with:
   - current implicit paper;
   - candidate directions;
   - ranking;
   - recommended direction;
   - what would change in the paper;
   - what should not change yet;
   - required literature;
   - required proofs;
   - required simulations;
   - slop risks;
   - next three tasks.

5. Append the memo to:
   `_context/exploration/direction_memos.md`

Do not edit the paper.
Do not change the project objective.
This is an exploration command.
When evaluating candidate directions, explicitly compare the current three-rule emphasis against the four-rule comparison. Assess whether Hamming deserves the same role as Manhattan given that both face difficulties in deriving clean analytical bounds.