# Analytical Bounds Search Skill

Use this skill when trying to derive inverse-region, coordinate-bound, or mean-bound results for a scoring rule.

## Goal

Try seriously to derive analytical or semi-analytical bounds before falling back to simulation or numerical computation.

## Procedure

For a rule \(S\):

1. Write the expected score or expected loss.
2. Express the optimal-report condition:
   \[
   r \in R_S(p)
   \]
3. Convert this into inverse-region inequalities:
   \[
   P_S(r)=\{p:r\in R_S(p)\}.
   \]
4. Determine whether the inequalities are:
   - linear;
   - convex;
   - piecewise linear;
   - quadratic;
   - combinatorial;
   - nonconvex.

5. Try special cases:
   - \(k=2\);
   - small \(n\);
   - interior reports;
   - boundary reports;
   - symmetric beliefs;
   - sparse beliefs;
   - ties.

6. Try coordinate bounds:
   \[
   \inf_{p\in P_S(r)} p_j,\quad \sup_{p\in P_S(r)} p_j.
   \]

7. Try linear-functional or mean bounds:
   \[
   \inf_{p\in P_S(r)} a^\top p,\quad \sup_{p\in P_S(r)} a^\top p.
   \]

8. Classify the result as:
   - closed form;
   - semi-analytical;
   - linear program;
   - mixed-integer program;
   - threshold search;
   - brute-force finite computation;
   - unresolved.

9. If no clean bound is found, explain why.

## Output format

Use:

1. Rule
2. Expected loss
3. Optimal-report condition
4. Inverse-region representation
5. Coordinate-bound attempt
6. Mean-bound attempt
7. Special cases
8. Analytical status
9. Computational fallback
10. Safe manuscript statement