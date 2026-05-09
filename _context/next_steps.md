# Next Steps

## Immediate Priority: Four-Rule Refactor

1. Audit the current treatment of Hamming in the paper and code.
2. Promote Hamming to the same conceptual status as Manhattan in the research plan.
3. Revisit analytical derivations for Manhattan and Hamming.
4. Redesign the simulation as a four-rule horse race:
   - quadratic;
   - discrete metric;
   - Manhattan;
   - Hamming.

## Analytical Tasks

1. Derive or characterize Hamming-distance optimal-report correspondences.
2. Derive or characterize Hamming inverse belief regions.
3. Attempt coordinate-bound derivations for Hamming.
4. Revisit Manhattan analytical bounds and determine whether sharper results are possible.
5. If closed-form bounds are unavailable, formulate computational bound problems clearly.

## Simulation Tasks

1. Update `scripts/design_efficiency.py` to include Hamming in the headline comparison.
2. Remove or deprioritize payment/winning probability as a main metric.
3. Add design-cell comparisons by:
   - \(n\);
   - \(k\);
   - Dirichlet concentration parameter;
   - belief sparsity or balance;
   - inferential objective.

4. Add metrics:
   - average coordinate width;
   - worst-coordinate width;
   - mean-bound width;
   - rank by design cell;
   - regret relative to cell-best rule;
   - frequency of rule winning by metric.

5. Decide which outputs belong in:
   - main paper tables;
   - main paper figures;
   - appendix;
   - repository-only robustness outputs.

## Paper Tasks

1. Revise the introduction so the paper promises a four-rule comparison.
2. Revise the scoring-rules section so Hamming is presented alongside Manhattan.
3. Revise the design-comparison section around contextual rule performance.
4. Remove or demote payment-probability discussion from the simulation section.
5. Keep payment probability only as an implementation concern for exact-match/frequency guessing, if useful.
 
## Citation And Literature Pass

- Verify every citation in `paper/references.bib` against the PDFs in `_context/related_literature/`.
- Replace any remaining placeholder or weak citation language.
- Make the novelty claim precise relative to Schlag--Tremewan and standard scoring-rule theory.

## Mathematical Proof Audit

- Recheck the quadratic-distance projection region and closed-form coordinate bounds line by line.
- Recheck the discrete-metric transfer region and coordinate intervals against Schlag--Tremewan.
- Recheck the Manhattan threshold representation and make sure all boundary cases are stated correctly.
- Confirm the appendix proofs are sufficient and not too compressed.

## Paper Tightening

- Tighten the introduction around one contribution: finite-sample belief and functional bounds from frequency reports.
- Shorten any text that does not support the chain from scoring rule to inverse belief region to bounds.

## Simulation Presentation

- Decide which final simulation tables belong in the paper.
- Consider adding figures from `outputs/simulation_design/`, especially:
  - win shares by \((n,k,\alpha)\);
  - mean-width comparisons under sparse beliefs;

## Final Draft Preparation

- Recompile the paper after the citation and proof pass.
- Produce a clean PDF.
- Ask for a focused external read on:
  - novelty;
  - clarity of the inverse-belief-region contribution;
  - whether the simulation evidence is useful enough for an economics/methods audience.
