# Theorem Development Skill

Use this skill when developing theorem candidates, propositions, lemmas, corollaries, proof sketches, or analytical derivations.

## Goal

Turn informal mathematical reasoning into structured candidate results that can later be audited.

This skill is exploratory but disciplined.

## Procedure

For a target mathematical problem:

1. Define the primitives.
2. Define the object to characterize.
3. Derive the relevant optimality condition.
4. Convert the condition into inequalities or optimization problems.
5. Search for simplifications.
6. Search for special cases.
7. Try to formulate theorem candidates.
8. Separate proven results from conjectures.
9. Identify required assumptions.
10. Identify counterexamples or edge cases.
11. Suggest proof strategies.
12. Decide what kind of result is realistic.

## For scoring-rule problems

For a scoring rule \(S\), derive:

1. expected score or expected loss;
2. optimal-report correspondence:
   \[
   R_S(p)
   \]
3. inverse belief region:
   \[
   P_S(r)=\{p:r\in R_S(p)\}
   \]
4. coordinate bounds:
   \[
   \inf_{p\in P_S(r)} p_j,\quad \sup_{p\in P_S(r)} p_j
   \]
5. linear-functional bounds:
   \[
   \inf_{p\in P_S(r)} a^\top p,\quad \sup_{p\in P_S(r)} a^\top p
   \]

## Search tactics

Try:

- pairwise report comparisons;
- one-coordinate deviations;
- exchange deviations;
- support-size reductions;
- binary case \(k=2\);
- small \(n\);
- boundary reports;
- interior reports;
- tie cases;
- convexity or linearity checks;
- finite optimization formulations;
- duality arguments where applicable;
- monotonicity arguments;
- dominance arguments;
- counterexamples.

## Result types

Classify outputs as:

- theorem;
- proposition;
- lemma;
- corollary;
- conjecture;
- example;
- counterexample;
- computational claim;
- proof strategy;
- open problem.

## Status labels

Every result must have one of:

- proven in this derivation;
- proof sketch only;
- plausible conjecture;
- supported by computation only;
- special case only;
- requires stronger assumptions;
- unresolved;
- likely false.

## Anti-slop rules

- Do not promote a conjecture to theorem.
- Do not hide gaps.
- Do not use vague phrases like "it is clear" for nontrivial steps.
- Do not claim closed form when the result is algorithmic or threshold-computed.
- Do not confuse finite computational checks with proof.
- Do not change the paper before the result is audited.

## Output format

Use:

1. Problem
2. Definitions
3. Derivation
4. Candidate theorem/proposition/lemma/corollary statements
5. Proof sketches
6. Gaps
7. Counterexample checks
8. Special cases
9. Analytical status
10. Recommended audit task