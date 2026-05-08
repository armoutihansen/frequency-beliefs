# Current Status

Date: 2026-05-08

## Project Thesis

The project is currently framed as a methodological note on the informational efficiency of frequency-report scoring rules.
A subject has latent multinomial beliefs \(p\), reports a count vector \(r\), and the researcher uses the scoring rule to infer the inverse belief region
\[
P_S(r)=\{p:r\in R_S(p)\}.
\]
The practical output is a set of finite-sample bounds for latent probabilities and linear functionals such as means.

## Active Manuscript

The manuscript is in `paper/`.
It is stabilized for now, but it is not submission ready.
The current title is:

> The Informational Efficiency of Frequency-Report Scoring Rules

Current structure:

1. Introduction
2. Setup
3. Frequency-report scoring rules
4. Informational efficiency exercise
5. Risk aversion
6. Discussion
7. Appendix

## Active Rules

The main rules in the paper are:

- Quadratic-distance frequency scoring: main analytical contribution.
- Discrete-metric frequency scoring: known Schlag--Tremewan exact-match rule with analytic bounds.
- Manhattan-distance frequency scoring: structured comparison rule with threshold-computed bounds.

Hamming and Chebyshev distance are discussed as secondary computable rules, but they are not part of the headline simulation results.

## Current Evidence

The final design exercise has been run with:

```bash
uv run python scripts/design_efficiency.py --final --draws 5000
```

The outputs are in `outputs/simulation_design/`.
The final grid uses:

- \(n\in\{5,10,20,50\}\);
- \(k\in\{2,3,5,10\}\);
- \(\alpha\in\{0.1,0.3,1,3,10\}\);
- 5,000 Dirichlet belief draws per cell.

Main summary:

- Discrete metric has the highest average coordinate-width win share, about `0.620`.
- Quadratic distance has the highest worst-coordinate-width win share, about `0.607`.
- Quadratic distance is strongest for mean-oriented inference in sparse-belief cells, especially low \(\alpha\), larger \(n\), and larger \(k\).
- Manhattan distance is useful as a structured comparison rule, but the final simulation does not support presenting it as dominant.
- Exact-match payment probabilities can become very small as \(n\), \(k\), and belief balance increase.

## Verification Status

`scripts/verify_regions.py` passed the implemented finite checks for:

- discrete-metric mode and interval formulas;
- quadratic-distance projection, inverse region, and coordinate bounds;
- Manhattan-distance exchange and threshold logic;
- binary special cases;
- direct-monetary risk-aversion counterexamples.

These checks are finite computational checks, not substitutes for final mathematical proof verification.
