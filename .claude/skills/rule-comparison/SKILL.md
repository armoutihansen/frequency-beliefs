# Rule Comparison Skill

Use this skill when comparing scoring rules in the frequency-report paper.

## Current headline rules

The four headline rules are:

1. Quadratic distance.
2. Discrete metric / exact match.
3. Manhattan distance.
4. Hamming distance.

Chebyshev is secondary unless explicitly promoted.

## Goal

Compare the four rules in a way that is analytically disciplined and simulation-relevant.

## Analytical comparison

For each rule, identify:

1. scoring rule definition;
2. optimal-report correspondence;
3. inverse belief region;
4. coordinate-bound method;
5. mean-bound or linear-functional-bound method;
6. implementation concerns;
7. current analytical status.

Classify analytical status as:

- closed form;
- semi-analytical;
- finite optimization;
- threshold-computed;
- computational only;
- unresolved.

## Simulation comparison

For each rule, compare:

- average coordinate-bound width;
- worst-coordinate-bound width;
- mean-bound or linear-functional-bound width;
- rank by design cell;
- regret relative to best rule;
- frequency of winning by metric.

Do not use exact-correct-report payment probability as a main horse-race metric unless comparable payment implementations are defined for all rules.

## Contextual conclusions

The desired conclusion is contextual, not universal.

Use language such as:

- "For sparse beliefs and larger \(k\), rule X performs better under metric Y."
- "For balanced beliefs, rule Y tends to produce narrower average coordinate bounds."
- "For mean-oriented inference, rule Z performs best in these cells."
- "No rule uniformly dominates across all design cells and metrics."

## Output format

Use:

1. Rule definitions
2. Analytical status table
3. Simulation metric table
4. Contextual performance summary
5. Unsupported claims
6. Required derivations
7. Required code changes
8. Safe manuscript wording