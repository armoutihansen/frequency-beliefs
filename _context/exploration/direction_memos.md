# Direction Memos

## Adopted direction (2026-05-21): partial-identification reframing

Decided in a `grill-with-docs` session. This is the adopted baseline, not a
candidate under consideration. The glossary is in `CONTEXT.md`; the two
hard-to-reverse decisions are recorded as `docs/adr/0001` and `docs/adr/0002`.

### 1. Candidate direction

Recast incentivized frequency-report belief elicitation as a partial-
identification problem. Each scoring rule maps an observed report to an
identified set of latent multinomial beliefs — the set of beliefs that
rationalize the report as an optimal report under that rule. The paper compares
four rules by the sharpness of the identified sets they induce.

### 2. Central research question

For frequency-report scoring rules, which rule is most informationally
efficient — i.e., yields the sharpest identified set — and how does the answer
depend on the inferential objective (coordinate vs. linear-functional inference)
and on the design regime `(n, k, belief dispersion)`?

### 3. Relation to current draft

The existing draft already contains the setup (`02_setup.tex`), a multi-rule
scoring-rule section, a design exercise, and a risk-aversion section. The
reframing keeps the mathematical content but changes the spine: the "inverse
belief region" is renamed and recast as a mechanism-induced identified set; the
quadratic rule becomes the worked centerpiece of a partial-ID contribution
rather than a standalone theorem; the design exercise becomes a comparison of
identified-set sharpness rather than a payment-probability horse race.

### 4. Required literature

Primary defense surface is the belief-elicitation literature (Schlag-Tremewan,
Schlag et al., Hossain-Okui). Secondary is the partial-identification literature
(Manski, Tamer, Molinari). A focused check against the scoring-rule literature
(Brier, Selten, Gneiting-Raftery) for the quadratic result. Binary-lottery
payment references (Roth-Malouf, Karni, Berg et al. / Selten et al.) are
required by ADR-0002.

### 5. Required theorem/proof work

Preserve and audit the quadratic closed-form coordinate and mean bounds
(verify they attain the exact inf/sup — this is what licenses "sharp").
Time-boxed analytical-bounds-search for closed-form Manhattan and Hamming
coordinate bounds; mean bounds only if coordinate bounds yield.

### 6. Required simulation/code work

Revise `design_efficiency.py` into a four-rule comparison (add Hamming) on two
headline metrics — average coordinate width and the ordered-category-mean bound
— displayed as cell-best regret. Remove payment probability as a comparison
metric.

### 7. Contribution potential

Three claims: (N1) the partial-ID framing of scoring-rule inference; (N2) the
unified four-rule informational-efficiency comparison with a contextual answer;
(N3) the closed-form quadratic identified-set characterization. Headline =
framing + contextual comparison; quadratic theorem is the centerpiece example.

### 8. Feasibility

High. The mathematical content largely exists; the work is reframing,
one bounded analytical-bounds-search, a simulation revision, and a guardrail-
mode manuscript pass. No new data collection.

### 9. Risk of slop or overclaiming

Main risks: calling computed Manhattan/Hamming bounds "sharp" (forbidden without
a tolerance qualifier); claiming distance rules are risk-aversion-robust without
the EU + binary-lottery qualifier; overclaiming N1 if the literature scan finds
a close prior. All are controlled by CONTEXT.md flagged ambiguities and the ADRs.

### 10. Recommendation

Adopted. Venue tier: general-interest economics journal with a methods section.
Scope: pure methodological paper, no empirical illustration (a stipulated worked
example in the discussion substitutes). Proceed per `_context/next_steps.md`.

## Rejected alternatives

See `_context/exploration/rejected_directions.md`.
