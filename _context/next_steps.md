# Next Steps

## 1. Citation And Literature Pass

- Verify every citation in `paper/references.bib` against the PDFs in `_context/related_literature/`.
- Replace any remaining placeholder or weak citation language.
- Make the novelty claim precise relative to Schlag--Tremewan and standard scoring-rule theory.

## 2. Mathematical Proof Audit

- Recheck the quadratic-distance projection region and closed-form coordinate bounds line by line.
- Recheck the discrete-metric transfer region and coordinate intervals against Schlag--Tremewan.
- Recheck the Manhattan threshold representation and make sure all boundary cases are stated correctly.
- Confirm the appendix proofs are sufficient and not too compressed.

## 3. Paper Tightening

- Decide whether Hamming and Chebyshev should remain in the main scoring-rule section or move to a shorter appendix note.
- Tighten the introduction around one contribution: finite-sample belief and functional bounds from frequency reports.
- Shorten any text that does not support the chain from scoring rule to inverse belief region to bounds.

## 4. Simulation Presentation

- Decide which final simulation tables belong in the paper.
- Consider adding figures from `outputs/simulation_design/`, especially:
  - win shares by \((n,k,\alpha)\);
  - mean-width comparisons under sparse beliefs;
  - exact-match payment probability as \(n\) and \(k\) grow.
- Keep the simulation framed as design evidence, not a theorem.

## 5. Final Draft Preparation

- Recompile the paper after the citation and proof pass.
- Produce a clean PDF.
- Ask for a focused external read on:
  - novelty;
  - clarity of the inverse-belief-region contribution;
  - whether the simulation evidence is useful enough for an economics/methods audience.
