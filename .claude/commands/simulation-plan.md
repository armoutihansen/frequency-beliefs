# Review or update the simulation/design-efficiency plan.

Steps:

1. Read `_context/current_status.md`.
2. Read `_context/current_issues.md`.
3. Read `_context/next_steps.md`.
4. Read `paper/sections/06_design_comparison.tex`.
5. Inspect `scripts/design_efficiency.py`.
6. Inspect available files under `outputs/simulation_design/`.
7. Use the `simulation-methodologist` agent.

The simulation plan should now evaluate a four-rule horse race among:

1. quadratic distance;
2. discrete metric / exact match;
3. Manhattan distance;
4. Hamming distance.

The simulation should determine which rule performs best under which contexts, varying:

- \(n\);
- \(k\);
- belief distribution \(p\);
- Dirichlet concentration parameter;
- inferential objective.

Report:

1. simulation question;
2. target quantities;
3. parameter grid;
4. rules compared;
5. whether Hamming is included symmetrically with Manhattan;
6. informational-efficiency metrics;
7. metrics that should be removed or demoted;
8. supported claims;
9. unsupported or overstated claims;
10. table/figure recommendations;
11. robustness recommendations;
12. code-paper consistency issues;
13. whether the simulation design supports the current four-rule paper direction.

The exact-correct-report payment probability should not be treated as a main horse-race metric because it is directly relevant only to the discrete-metric / frequency-guessing implementation. If retained, it should be isolated as an implementation issue for the discrete-metric rule.

Do not rerun the final simulation unless explicitly asked.
Do not overwrite outputs unless explicitly asked.