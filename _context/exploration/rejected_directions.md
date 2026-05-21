# Rejected Directions

Alternatives considered and rejected in the 2026-05-21 `grill-with-docs`
direction session. See `_context/exploration/direction_memos.md` for the
adopted direction.

## Spine alternatives (Q1)

- **Pure quadratic-distance theorem paper.** Rejected: one rule, one theorem is
  too thin for a general-interest methods venue; the scoring-rule literature
  already has many results.
- **Pure four-rule design-comparison paper.** Rejected as the *spine*: without a
  sharp theoretical claim it reads as a benchmarking exercise. Retained as a
  component (N2) inside the partial-ID spine.

## Venue alternatives (Q3)

- **Econometrics methods journal** (J. Econometrics, Quantitative Economics).
  Rejected: raises the partial-ID machinery bar substantially (support
  functions, formal moment-inequality sharpness) and narrows the audience away
  from the elicitation researchers who actually adopt these rules.
- **Experimental / behavioral outlet.** Rejected: underuses the partial-ID
  framing, reducing it to a labeling exercise.
- **Decision-theory / OR outlet.** Rejected: smallest natural audience for the
  design exercise.

## Headline-rule alternatives (Q4)

- **Two headline rules** (quadratic + discrete-metric only). Rejected: shrinks
  the contribution to one theorem plus recovered prior art.
- **Three headline rules** (drop one of Manhattan/Hamming). Rejected: no
  mathematical justification for the asymmetry; risks the implementation-order
  bias CLAUDE.md warns against.

## Payment-frame alternatives (Q5c, ADR-0002)

- **Binary-lottery payment as the maintained body frame.** Initially adopted,
  then reversed: front-loads mechanism complexity and partly offsets the
  cognitive-load argument. Replaced by risk neutrality in the body with the
  binary-lottery extension in the discussion.
- **Direct monetary payment as maintained frame.** Rejected: under risk
  aversion it breaks robustness for the three distance rules.
- **Risk aversion in the simulation.** Rejected: doubles/triples compute,
  requires defending risk-aversion parameterizations, and shifts the simulation
  away from informational efficiency.

## Empirical-component alternatives (Q9)

- **Methods paper + empirical illustration on existing data.** Rejected for the
  initial submission: every identified set computed from a real report silently
  inherits the unverifiable optimal-reporting assumption. A stipulated worked
  example substitutes. Could be added in a revise-and-resubmit.
- **Methods paper + small original elicitation.** Rejected: out of scope,
  reopens behavioral-evidence claims the project has deliberately closed.
