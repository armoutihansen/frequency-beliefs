# Current Issues

## Submission Readiness

The paper is coherent enough to pause, but not ready for submission.
It still needs a dedicated citation pass, a proof audit, and a sharper final exposition.

## Mathematical Issues

- The quadratic-distance result is the main novelty candidate and needs the highest proof scrutiny.
- The discrete-metric coordinate bounds are attributed to Schlag--Tremewan and need final source verification and citation details.
- Manhattan multi-category bounds are threshold-computed; they should not be described as closed form.
- Mean bounds must continue to be stated as optimizations over the full inverse belief region, not as combinations of coordinate intervals.
- Hamming and Chebyshev distance have exact finite expected-loss representations but should not be promoted without cleaner bound results.

## Simulation Issues

- The final simulation is a design diagnostic conditional on optimal reporting; it is not evidence about actual subject behavior.
- The final tables compare only discrete metric, quadratic distance, and Manhattan distance.
- Hamming and Chebyshev are not in the headline simulation outputs.
- Manhattan results depend on threshold search with tolerance \(10^{-4}\).
- The paper currently reports tabular summaries only; final figures remain undecided.

## Interpretation Risks

- Do not claim that any rule is uniformly best.
- Do not claim the paper invents frequency guessing or the exact-match mechanism.
- Do not claim distance rules are robust to risk aversion under direct monetary payment.
- Do not oversell the cognitive advantage of frequency reports without additional empirical evidence.
- Do not describe grid or simulation evidence as mathematical proof.

## Literature Issues

The bibliography needs final verification against the local PDFs in `_context/related_literature/`.
Important sources include:

- Schlag--Tremewan for frequency guessing;
- Schlag et al. for belief-elicitation methods;
- Armantier--Treich for risk-aversion concerns;
- Hogarth for probability-assessment motivation;
- Savage, Selten, and Gneiting--Raftery for scoring-rule background.
