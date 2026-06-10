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

## Direction memo (2026-06-10): venue/identity fork after the master threshold theorem

Status: **ADOPTED same day — direction (C), two papers.** Author also
selected for paper 1: Remark 1 removal (executed; paper recompiles clean at
33 pp), the misreporting robustness exercise, and final figures; the
small-cell Hamming/Chebyshev option was declined. Paper 2 remains gated on
explicit authorization of the inverse-optimization literature check.
Original analysis follows. Offline (no literature access,
per the 2026-06-10 binding constraints). Theory inventory: the twice-audited
`master_threshold_theorem.md` and the audited `feasibility_frontier.md`.

### 1. Current implicit paper

A partial-identification methods paper for experimentalists: three rules
characterized (two closed-form, one semi-analytical), organized by a
classical-cored lemma, compared in a design exercise, with contextual
recommendations and an implementation/risk-aversion discussion. 34 pp,
compiles clean, submission-ready modulo an external read. Honest tier
assessment: a good FIELD-journal paper (Experimental Economics, JEBO, GEB);
the ADR's "general-interest journal" tier was optimistic.

### 2. Candidate directions

(A) Field paper as-is, optional strengtheners: final figures; a
misreporting-coverage robustness exercise (perturb optimal reports, e.g.
center-bias, measure identified-set coverage of true p — quantifies the
paper's own biggest conditional, reuses existing bound code); small-cell
Hamming/Chebyshev simulation REJECTED for this paper (documented
intractability at grid scale per ADR-0001 spike; near-zero decision value
for the field audience since neither rule offers the researcher tractable
bounds).

(B) Single methods paper: general count-loss family (already in §2),
master theorem, three-tier closed-form/semi-analytical/intractable
classification, rule-level boundary theorems, quantile family. Most theory
exists at memo grade. Genuinely missing: appendix-grade write-up (memo
Gaps 1, 8); Chebyshev ordinal hardening (non-separability currently proven
only for the raw expected loss — a finite coordinate-independence
computation, offline-doable); the MANDATORY inverse-optimization novelty
check (author authorization required); venue re-aim (GEB/ET/QE/JoE).
Risks: "core is classical" referee attack; novelty gate unresolved; months
of delay; the polished applied half shrinks to an illustration.

(C) Two related papers: paper 1 = (A) now; paper 2 = the methods paper
from the memo inventory, literature-gate first, own pace. Synergies:
simulation framework reuses for quantile rules; paper 1 self-contained
(no general claims — Remark 1 removal advised to avoid both the loose end
and overlap); paper 2 cites paper 1 as the worked application.
Salami risk mitigated: paper 2's content strictly exceeds paper 1's needs
(inversion machinery, interval projections, new rule family, boundary
theorems). Fallback if the novelty gate kills paper 2: fold back as a
revision-stage Full for paper 1; paper 1 unharmed either way.

### 3. Ranking

C > A > B. C contains A and adds a decoupled option; B couples a
submission-ready paper's fate to an unchecked novelty claim and a venue
shift.

### 4. Recommendation

(C). Paper-1 decisions: remove Remark 1; keep the L2/L3 repairs and the
Hamming order-preserving exclusion (corrections/sharpenings, not theory
claims); strengtheners ranked: figures (low effort) > misreporting
robustness exercise (moderate effort, highest audience value) >> NOT
Hamming/Chebyshev. Paper-2 sequence: literature gate (explicit author
authorization, conservative mode) -> Chebyshev ordinal hardening ->
appendix-grade write-up -> standalone draft.

### 5. What must be true / what would change it

Holds if: author accepts field-journal tier for paper 1; has appetite for
a second project; machinery novelty plausibly intact. Changes if: author
wants one flagship and accepts the delay (-> B); the literature gate kills
the machinery's novelty (-> A only; reserve Full dead); the external read
finds paper 1 too thin even for field venues (-> reconsider B as a merge).

### 6. Next three tasks (under C)

1. Author decisions: direction; Remark 1 removal; which strengtheners.
2. Execute paper-1 decisions; external-read submission package.
3. On explicit authorization: paper-2 literature gate, then Chebyshev
   ordinal check.

## Rejected alternatives

See `_context/exploration/rejected_directions.md`.
