# Candidate-Rule Screen: Additional Frequency-Report Scoring Rules

Mode: exploration. Status: screening memo, not a manuscript claim. Date: 2026-05-22.

Scope: a systematic search for frequency-report scoring rules `S(r,ω)=a−bD(r,ω)`
beyond the five already analyzed — squared-distance, frequency-guessing
(discrete metric), Manhattan (feasible, headline); Hamming, Chebyshev
(infeasible, documented). Candidates drawn from (a) the distance/divergence
family and (b) translations of prominent probability-elicitation methods. Each
is classified on the project tractability spectrum (closed-form / semi-analytical
/ computational-feasible / computationally intractable) or dismissed as
redundant / out-of-frame. Numerical statements are finite enumeration checks
(`scripts/candidate_rule_checks.py`); they corroborate the derivations but are
not proofs. Per the user's scoping decisions: ordered-category rules are in
scope; the disposition of any feasible rule is left to a case-by-case decision
after this screen.

--------------------------------------------------------------------------------

## Headline findings

1. **The search is productive but yields few genuinely infeasible rules.** The
   feasibility frontier turns out to be sharp: a count-loss rule is tractable
   **iff** (A) its expected loss separates across coordinates **and** (B) the
   per-coordinate expected cost is discrete-convex in the integer report.
   Hamming fails (B); Chebyshev fails (A). *Every other natural candidate passes
   both* and is at worst semi-analytical. The paper's "two infeasible rules" are
   therefore not an arbitrary pair — they are the two canonical failure modes.

2. **New feasible rules with closed-form / polytope identified sets:**
   **KL divergence** (the divergence translation of the logarithmic scoring
   rule) and **RPS** (the ranked probability score = squared distance on
   cumulative counts). Both are as tractable as the current closed-form headline
   rules.

3. **New feasible rules, semi-analytical (Manhattan-class):** pinball /
   asymmetric-L1 (elicits quantiles), expectile / asymmetric-squared (elicits
   expectiles), and the `L_p`-power / Hellinger / Huber / cumulative-L1 family.

4. **Correction to the Stage-1 agent screen.** The divergence-agent's analysis
   wrongly classified KL as "single-transfer not sufficient" and chi-squared as
   "intractable like Hamming." Both are wrong (see Corrections below). KL is
   fully feasible; chi-squared is computational-feasible-but-unattractive, not
   Hamming-class.

5. **Bregman result, corrected.** *Every* separable Bregman count loss has a
   polytope identified set (boundaries affine in `p`). Squared distance is **not**
   unique in this; KL is a second example. The sub-family with the *sparse*
   `O(k²)`-facet polytope is characterized by discrete-concavity of the Bregman
   generator's derivative — squared distance and KL both belong.

--------------------------------------------------------------------------------

## Screening framework — three gates

Expected loss `L(r;p)=E_p[D(r,ω)]`, `ω~Mult(n,p)`; optimal reports
`R_S(p)=argmin_r L`; identified set `P_S(r)={p : r∈R_S(p)}`.

- **Gate A — separability.** `L(r;p)=Σ_i ℓ_i(r_i;p_i)`? If not, even the optimal
  report is combinatorial (Chebyshev class) → infeasible.
- **Gate B — discrete-convexity.** Is `ℓ_i` discrete-convex in the integer
  argument? If yes, single-count-transfer optimality is *sufficient* and
  `P_S(r)` is exactly the `O(k²)`-facet transfer region. If no (Hamming class),
  the set is non-convex semialgebraic → infeasible at scale.
- **Gate C — linearity.** Are the transfer inequalities linear in `p`? Linear ⇒
  polytope ⇒ closed-form/LP. Monotone-transcendental ⇒ semi-analytical (1-D
  root-find). Non-convex ⇒ infeasible.

--------------------------------------------------------------------------------

## Candidate verdicts

### Tier 1 — feasible, closed-form / polytope

**KL divergence** — `D(r,ω)=D_KL(ω/n‖r/n)`.
Expected loss simplifies to `L(r;p)=const(p)−Σ_i n p_i log r_i` (confirmed
numerically, constant spread 3e-15). Optimal report = the KL-projection of `np`
onto the integer simplex; **elicits the mean**. Per-coordinate cost
`ℓ_i(t)=t−n p_i log t` is discrete-convex (`Δ²ℓ_i=n p_i·log[(1+1/t)/(1+1/(t+1))]>0`).
Gate A ✓, Gate B ✓ (single-transfer sufficient — 0 mismatches, all test cells),
Gate C ✓ (affine). Transfer inequality `n p_i log(1+1/r_i)+n p_j log(1+1/(r_j−1))≥2`
— linear in `p`. **P_KL(r) is a polytope with `O(k²)` linear facets ⇒
closed-form / LP coordinate and mean bounds.** Caveat: `r_i=0` gives `L=+∞`
(the `log r_i` singularity), so interior reports have all `r_i≥1`; boundary
reports are optimal only at boundary beliefs. Classification: **closed-form**,
comparable to squared-distance / frequency-guessing.

**RPS — ranked probability score** — `D(r,ω)=Σ_{j<k}(R_j−Ω_j)²`,
`R_j=Σ_{i≤j}r_i` cumulative counts. Ordered categories (structurally uses the
category order; the current rules are permutation-invariant). It is squared
distance under the linear cumulative-sum reparametrization, a PSD quadratic
form `(r−np)ᵀM(r−np)`, `M=LᵀL`. Optimal report = the `M`-projection of `np`;
**elicits the cumulative / ordinal profile** (a genuinely new functional, absent
from the current four). Gate A ✓ (separable in cumulative coordinates),
Gate B ✓ (single-transfer sufficient — 0 mismatches, corroborated at k≤4;
general-k proof is a Stage-3 audit item), Gate C ✓ (affine — each transfer
inequality `vᵀMv+2vᵀM(r−np)≤0` is linear in `p`). **P_RPS(r) is a polytope ⇒
closed-form / LP bounds.** Classification: **closed-form**, the cumulative-count
analogue of squared distance. Strongest "translation" candidate.

### Tier 2 — feasible, semi-analytical (Manhattan-class)

All separable with a convex per-coordinate loss `E[φ(t−W_i)]`, `φ` convex ⇒
`ℓ_i` discrete-convex (the convex-extension argument is legitimate here — the
per-coordinate term is the expectation of a convex function of `t−ω`,
structurally unlike Hamming's `Pr(W=t)`) ⇒ Gate B ✓ ⇒ single-transfer
sufficient. Inequalities monotone-transcendental in `p` ⇒ Gate C semi-analytical.

| Rule | `D` | Elicits | Notes |
|---|---|---|---|
| **Pinball / asymmetric-L1** | `Σ ρ_τ(r_i−ω_i)` | the **τ-quantile** | one-parameter generalization of Manhattan (τ=½); reuses the Manhattan threshold root-find. Gate B/C corroborated (0 mismatches; non-affine, gap 0.45). |
| **Expectile / asymmetric-squared** | `Σ e_τ(r_i−ω_i)` | **expectiles** | generalizes squared distance; the asymmetry breaks the variance–bias collapse, so — unlike squared — the inequalities are **not** linear in `p` (resolved). Semi-analytical. |
| `L_p`-power | `Σ|r_i−ω_i|^p`, p≥1 | `L_p`-center | bridges Manhattan (p=1) and squared (p=2); general p semi-analytical, no crisp functional. |
| Hellinger | `Σ(√r_i−√ω_i)²` | "Hellinger center" | inequalities linear in `c_i=E√W_i`, an LP-in-transformed-coordinates; Gate B/C corroborated (0 mismatches; non-affine, gap 0.44). |
| Huber | `Σ H_δ(r_i−ω_i)` | robustified mean | δ-homotopy between squared (δ→∞) and Manhattan (δ→0); no crisp functional. |
| cumulative-L1 | `Σ_{j<k}|R_j−Ω_j|` | cumulative medians | the L1 analogue of RPS; ordered categories; semi-analytical. NB: standard CRPS for discrete outcomes coincides with RPS (squared), not this L1 variant. |

### Tier 3 — infeasible / not recommended

- **Un-squared Euclidean `‖r−ω‖₂`, spherical scoring rule, energy distance.**
  Gate A fails — the norm / normalization couples coordinates. Same obstruction
  as Chebyshev → infeasible. The spherical scoring rule is the relevant
  "prominent probability rule" here; its count translation is non-separable.
- **Chi-squared divergence `Σ(r_i−ω_i)²/r_i`.** Gate A ✓, Gate B ✓ (single-
  transfer region — 0 mismatches), but **Gate C fails** — boundaries are quadric
  (non-affine, gap 2.1). So `P(r)` is a non-convex region cut by `O(k²)` quadric
  inequalities. This is **computational-feasible** (few constraints, unlike
  Hamming's combinatorial blow-up — *not* Hamming-class) but **unattractive**:
  no closed form, no clean elicited functional, and an `r_i=0` singularity. The
  Neyman variant `/ω_i` is degenerate (`+∞` for every interior `p`).
  Recommendation: **reject** — feasible but offers nothing the Tier-1/2 rules do
  not, with extra pathology.

### Redundant / out-of-frame

- **Brier / QSR** ≡ squared-distance (`‖r−ω‖²/n²`) — already the paper's
  squared-distance rule.
- **Total variation** ≡ Manhattan (`/2n`) — already analyzed.
- **Logarithmic scoring rule** — its divergence-perspective translation *is* the
  KL count loss (Tier 1). Not out-of-frame; it enters as KL.
- **Standard CRPS** — for discrete `k`-category outcomes coincides with RPS.
- **BDM, Karni (2009), matching probabilities / lottery method** — mechanisms,
  not count losses; no `D(r,ω)` form. Out of frame as candidate rules; relevant
  only as risk-robustness benchmarks in the discussion.
- **Binarized scoring rule (Hossain–Okui)** — a payment wrapper (binary
  lottery), not a distinct `D`; same identified set as the underlying rule.
  Already covered in the risk-aversion subsection.

--------------------------------------------------------------------------------

## Corrections to the Stage-1 agent screen

The divergence-screening agent made two errors, caught on review and settled by
`scripts/candidate_rule_checks.py`:

1. **KL Gate B.** The agent claimed single-transfer optimality fails for KL
   ("180/600 mismatches") and classified KL as "computational-feasible, needs a
   spike." This is wrong. KL's per-coordinate cost `ℓ_i(t)=t−n p_i log t` is
   discrete-convex, so single-transfer optimality *is* sufficient — 0 mismatches
   across n∈{4,5,6}, k∈{3,4}, 150 beliefs/cell. KL is feasible and closed-form.
2. **Bregman uniqueness.** The agent conjectured squared distance is the unique
   separable Bregman count loss with a sparse-facet polytope. False: the correct
   condition for single-transfer sufficiency is discrete-*concavity* of the
   generator's derivative `h'` (plus a side condition), not affinity of `h'`.
   `h'` affine (squared) and `h'` concave (KL: `h'=log+1`) both qualify, so a
   whole sub-family — not just squared distance — has the sparse-facet polytope.
3. **Chi-squared.** The agent called it "computationally intractable at scale,
   same league as Hamming." Overstated: chi-squared's identified set is cut by
   only `O(k²)` quadric inequalities (Gate B holds), not the combinatorial
   constraint system that makes Hamming intractable. It is feasible-but-
   unattractive, not infeasible.

The agent's Proposition B (all separable Bregman ⇒ affine cell boundaries ⇒
polytope) is **correct** and corroborated (KL Gate C affine, gap 3e-15).

--------------------------------------------------------------------------------

## Open theorem candidates (for Stage 3, if pursued)

1. **The feasibility-frontier characterization.** "A separable count-loss rule
   is tractable (single-transfer-sufficient, hence `O(k²)`-facet identified set)
   iff the per-coordinate expected cost is discrete-convex; non-separable rules
   are infeasible." This would convert the paper's "3 feasible + 2 infeasible"
   list into a theorem and is the highest-value result the search surfaced.
2. **RPS single-transfer sufficiency for general `k`.** Corroborated
   numerically at k≤4; the general proof goes through the monotone cumulative
   lattice (`L♮`-convexity). Route to `theory-auditor`.
3. **Bregman sparse-facet sub-family.** Characterize precisely which separable
   Bregman generators give the `O(k²)`-facet polytope (conjecture: `h'`
   discrete-concave plus `Δ²(t h'−h)≥0`).

--------------------------------------------------------------------------------

## Triage and recommendation (for the case-by-case disposition)

Nothing here should enter the manuscript without the Stage-3 derivation +
`theory-auditor` pass. For the disposition decision:

- **Strongest additions: RPS and pinball.** RPS adds a genuinely new functional
  (the ordinal/cumulative profile) with a closed-form polytope, and is the clean
  translation of a canonical scoring rule; cost: it needs an ordered-category
  setup. Pinball adds the quantile family, generalizes Manhattan, and reuses
  existing machinery. Both are natural full-derivation (Stage-3) candidates.
- **KL** is feasible and closed-form and is the divergence translation of the
  logarithmic scoring rule — but it elicits the *mean*, the same functional as
  squared-distance, so it adds a rule, not a new inferential target. Worth a
  mention; weaker case for headline promotion.
- **Expectile** generalizes squared-distance as pinball generalizes Manhattan;
  natural to treat the two asymmetric families together if either is pursued.
- **`L_p` / Hellinger / Huber / cumulative-L1** are feasible but have no crisp
  elicited functional — best treated as evidence for the feasibility-frontier
  characterization (finding 1) rather than as individual headline rules.
- **Recommendation:** the highest-value outcome is not any single new rule but
  the **feasibility-frontier characterization** — it generalizes the paper's
  rule-by-rule tractability story into one structural statement. Promote RPS
  and/or pinball only if the contribution is meant to widen the horse race;
  otherwise fold the screen into a single "the tractable class" result.

--------------------------------------------------------------------------------

## Verification

`scripts/candidate_rule_checks.py` (exploration-mode finite checks; run with
`uv run python scripts/candidate_rule_checks.py`):

- Gate B (single-transfer-local optimum == global optimum) over n∈{4,5,6},
  k∈{3,4}, 150 random Dirichlet beliefs/cell: **0 mismatches** for
  squared-distance (control), KL, RPS, pinball, Hellinger, and chi-squared.
- Gate C (collinear-triple linearity of optimal-report inequalities):
  **affine** for squared-distance, KL, RPS; **non-affine** for chi-squared
  (gap 2.1), pinball (0.45), Hellinger (0.44).
- KL loss-formula identity `L(r;p)=const−Σ n p_i log r_i` confirmed (constant
  spread 3e-15).

These are finite checks at small `(n,k)`, not proofs; a Stage-3 derivation with
a `theory-auditor` pass is required before any rule is described as feasible in
manuscript-bound language.
