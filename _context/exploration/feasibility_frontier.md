# The Feasibility Frontier of Frequency-Report Scoring Rules

Mode: exploration. Status: derivation memo, not a manuscript claim. Date: 2026-05-22.

Scope: the Stage-3 derivation called for by `rule_candidate_screen.md`
("Open theorem candidates", item 1). It develops the result that organizes the
candidate screen — *which* separable frequency-report scoring rules admit a
tractable identified set, and *why* — and positions it correctly relative to the
prior literature.

Audit status: a `theory-auditor` pass is complete and its fixes are incorporated
below (Prop 1 finiteness; Theorem 3 ⟸ proof-tightening; Prop 3′ wording
downgrade; Prop 4 Hamming argument corrected; Corollary 5 dichotomy replaced by
a three-tier ladder). The optimization core has additionally been cross-checked
against the classical resource-allocation literature (see §6).

--------------------------------------------------------------------------------

## 0. The honest positioning (read this first)

The characterization below is **true and useful, but its optimization core is
classical, not new.** The statement "for an integer separable minimization on
the simplex, single-unit-exchange local optimality is global iff the separable
objective is discrete-convex" is the **discrete separable resource-allocation
problem** — Fox (1966), Federgruen & Groenevelt (1986, *necessary and
sufficient* conditions), Ibaraki & Katoh (1988); discrete convexity per Murota
(2003). It must therefore be presented as an **organizing lemma that applies a
classical result**, never as a new theorem.

What is genuinely the paper's own, and survives a novelty check:

1. **The reduction itself** — recognizing that the optimal-report problem under
   a separable frequency-report scoring rule *is* a discrete separable
   resource-allocation problem on the integer simplex. Once seen, it is
   immediate; it does not appear to have been used before to study scoring-rule
   tractability.
2. **The feasibility-frontier map** — using the reduction to classify which
   frequency-report scoring rules induce a tractable optimal-report
   correspondence, with Hamming and Chebyshev as the two canonical failure modes.
3. **The identified-set inversion** — Corollary 5: inverting the optimal-report
   correspondence into an `O(k²)`-facet identified set of beliefs, and the
   polytope / semi-analytical / threshold tractability ladder. The literature
   check found no prior work inverting scoring-rule reports into belief
   identified sets.

The write-up's weight must rest on (1)–(3); the optimization characterization is
cited, not claimed.

--------------------------------------------------------------------------------

## 1. Setup

`k` outcomes, `n` trials; latent multinomial beliefs `p` in the simplex `Δ`;
realized count vector `ω ~ Multinomial(n,p)`; marginal `W_i ~ Bin(n,p_i)`. A
report `r` is a feasible integer count vector (`r_i≥0`, `Σr_i=n`); feasible set
`Ω_n`. A rule is `S(r,ω)=a−bD(r,ω)`, `b>0`; a risk-neutral subject minimizes
`L(r;p)=E_p[D(r,ω)]` over `Ω_n`; `R_S(p)=argmin_r L`; identified set
`P_S(r)={p∈Δ : r∈R_S(p)}`. A *single-count transfer* is `r ↦ r+e_i−e_j`
(requires `r_j≥1`); these moves generate `Ω_n`.

The organizing lemma concerns the **coordinate-separable count-loss family**:
`D(r,ω)=Σ_i d(r_i,ω_i)` for a primitive per-coordinate loss `d`. Per-coordinate
expected cost `ℓ(t;q)=E_{W~Bin(n,q)}[d(t,W)]`; forward difference
`Δℓ(t;q)=ℓ(t+1;q)−ℓ(t;q)`; `ℓ(·;q)` is *discrete-convex* iff `Δℓ(·;q)` is
nondecreasing (second forward differences `≥0`).

--------------------------------------------------------------------------------

## 2. The organizing lemma

**Lemma 1 (separable reduction).** If `D` is coordinate-separable then
`L(r;p)=Σ_i ℓ(r_i;p_i)`, because `E_p[d(r_i,ω_i)]` depends on `ω` only through
the marginal law of `ω_i`, which is `Bin(n,p_i)` regardless of the multinomial
coupling. Hence `R_S(p)` solves the **integer separable resource-allocation
problem**
> minimize `Σ_i ℓ(r_i;p_i)` subject to `Σ_i r_i = n`, `r_i ∈ ℤ_{≥0}`.
*(Elementary; proof complete. `d` is finite on the finite grid
`{0,…,n}²`, so every `ℓ(t;q)` is finite — state this once.)*

**Lemma 2 (the classical characterization — cited, not claimed).** For the
integer separable resource-allocation problem, single-unit-transfer local
optimality is sufficient for global optimality, *for every right-hand side and
every report*, **iff** each per-coordinate cost `ℓ(·;q)` is discrete-convex.
This is the classical discrete separable resource-allocation result: the greedy
/ marginal-allocation algorithm is exact under discrete convexity (Fox 1966;
Ibaraki & Katoh 1988), and the convexity condition is *necessary* as well as
sufficient (Federgruen & Groenevelt 1986). Necessity of single-transfer
optimality (Prop 2 below) is unconditional and free.

- The **⟸ direction** (discrete-convexity ⟹ sufficiency) also has a fully
  self-contained proof in this paper's own setting: it is the audited Manhattan
  "Claim C" of `bounds_search_manhattan_hamming.md`, whose monotone-path /
  exchange argument uses *only* discrete-convexity of `ℓ` — nothing
  Manhattan-specific (no median, no `2F−1`, no absolute value); this was
  verified against the actual Claim C proof by the theorem-developer pass. The
  paper can therefore give the ⟸ proof self-contained and cite the classical
  literature for the full iff. **Manuscript-proof requirement (auditor):** the
  write-up must state explicitly (a) the bijection between the
  `Σ(s_i−r_i)^+` up-units and the equally-many down-units, and (b) the
  *sender-side* discrete-convexity bound `−Δℓ(m';p_j) ≥ −Δℓ(r_j−1;p_j)` for
  `m'≤r_j−1`, not only the receiver-side bound — the sketch is otherwise
  underspecified.
- The **⟹ direction** (non-convex ⟹ single-transfer fails) is the classical
  necessity half; it is not an open problem. A self-contained witness for the
  paper's setting is the "fold-against-itself" construction — choosing the
  budget `m = 2t₀+2` so the folded cost `g(t)=ℓ(t;q₀)+ℓ(m−t;q₀)` inherits the
  non-convexity at `t₀` and acquires a non-global local minimum — together with
  the exact Hamming witness (`n=3,k=5`, uniform `p`, report `(3,0,0,0,0)`
  single-transfer-optimal but `(0,0,1,1,1)` strictly better).

**Necessity (Prop 2).** For any `D` and any `p`: `r∈R_S(p)` ⟹ no single-count
transfer strictly lowers `L`. (Unconditional; the transfer change is
`Δℓ(r_i;p_i) − Δℓ(r_j−1;p_j)`.)

**Proposition 4 (the checkable primitive-level test).** If the primitive loss
`d(·,w)` is discrete-convex in `t` for *every* fixed realization `w∈{0,…,n}`
(boundary `w` included), then `ℓ(·;q)` is discrete-convex for every `q` —
because `Δ²ℓ(t;q)=E_W[Δ²_t d(t,W)]` is an expectation of nonnegative quantities
(expectation preserves discrete convexity; Murota 2003, or a one-line proof
from the definition). This is the *operational* form of the frontier: one
checks convexity of a finite primitive table `d`, never a binomial expectation.

- Passes (tractable): squared distance, Manhattan, `L_p`-power (`p≥1`), Huber,
  pinball/asymmetric-`L1`, expectile/asymmetric-squared, Hellinger. Hellinger's
  primitive `d(t,w)=(√t−√w)²=t−2√w·√t+w` is discrete-convex in `t` because
  `−√t` is discrete-convex (verified in the convex-family screen).
- Hamming. Prop 4 is *sufficient, not necessary*; for Hamming it simply does
  not apply — `d(t,w)=1{t≠w}` is a 0/1 notch, not discrete-convex
  (`Δ²_t d(w−2,w)=0−2·1+1=−1<0`). But the failure of Prop 4's *sufficient*
  condition is **not itself** the proof that Hamming is intractable. The actual
  disqualifier is at the `ℓ` level: `ℓ(t;q)=1−\binom{n}{t}q^t(1−q)^{n−t}` is one
  minus a unimodal binomial pmf, hence strictly *concave* across the pmf's mode,
  so `ℓ(·;q)` is itself non-discrete-convex — the exact Lemma-2 condition fails.
  State this `ℓ`-level argument, not the `Δ²d` computation, as the reason
  Hamming is out.
- Prop 4 is sufficient, not necessary, for the Lemma-2 condition; the exact
  condition is discrete-convexity of `ℓ` itself (e.g. KL's per-coordinate cost
  `ℓ(t;q)=t−nq·log t` is discrete-convex without `d` having the primitive form).

**The `k=2` caveat (Prop 3′).** For `k=2` (`r=(t,n−t)`), single-transfer
sufficiency is equivalent to discrete-convexity of the *folded* cost
`g(t)=ℓ(t;p_1)+ℓ(n−t;p_2)` for all `(p_1,p_2)`. This is **formally weaker** than
discrete-convexity of `ℓ` itself (a sum of two discrete-convex functions is
discrete-convex, but `g` can be discrete-convex without each `ℓ` being — a
constructed example confirms the formal gap is non-empty). The clean iff of
Lemma 2 is therefore stated for `k≥3`. We do **not** claim `k=2` as a
substantive exception: that would require exhibiting an actual count loss whose
`ℓ` is non-discrete-convex yet whose folded `g` is discrete-convex for all
`(p_1,p_2)`, which has not been done. State `k=2` only as "the condition is
formally weaker," not as a worked exception.

--------------------------------------------------------------------------------

## 3. The two failure modes

Within the natural count-loss families, tractability fails in exactly two ways,
and the paper's two infeasible rules are one canonical instance of each:

1. **Separable but `ℓ` not discrete-convex — Hamming.** Lemma 1 applies, Lemma 2
   does not: single-transfer optimality is only necessary, and `P_S(r)` is the
   full polynomial system over all `binom(n+k−1,k−1)` reports — a non-convex
   semialgebraic set, intractable at the design grid's scale.
2. **Not coordinate-separable — Chebyshev** (`D=max_i|r_i−ω_i|`). Lemma 1 itself
   fails: the `max` couples coordinates, the expected loss does not separate,
   and there is no resource-allocation structure — even computing `R_S(p)` is
   combinatorial.

This is what makes the paper's "three feasible, two infeasible" list not a list
but a structure: feasibility needs separability (Lemma 1) *and* discrete-convex
per-coordinate cost (Lemma 2); the two infeasible rules negate one conjunct each.

--------------------------------------------------------------------------------

## 4. What the lemma delivers — the contribution

**The feasibility-frontier map.** Every rule in `rule_candidate_screen.md` is
classified by Lemmas 1–2 + Prop 4: squared / frequency-guessing / KL / RPS are
separable with discrete-convex (indeed affine-`Δ`) cost ⟹ polytope; Manhattan /
pinball / expectile / `L_p` / Huber / Hellinger / cumulative-`L1` are separable
discrete-convex with monotone-transcendental `Δ` ⟹ semi-analytical; Hamming and
the non-separable rules are the two failure modes. The rule-by-rule tractability
story becomes one structural statement.

**Corollary 5 (identified-set inversion — the novel object).** Under
discrete-convexity, `P_S(r)` is *exactly*
> `{ p∈Δ : Δℓ(r_i;p_i) ≥ Δℓ(r_j−1;p_j)  ∀ i≠j with r_j≥1 }`,

an intersection of at most `k(k−1)` facets. Convention: extend `ℓ(t;·)=+∞` for
`t∉{0,…,n}`, so `Δℓ(n;·)=+∞` (a coordinate already at `n` cannot receive — the
constraint is vacuous); pairs with sender `r_j=0` are excluded by the `r_j≥1`
restriction. Edge case: if `r_i=n` for some `i` then no transfer is feasible and
`P_S(r)=Δ`.

Writing `δ_t(q):=Δℓ(t;q)`, the tractability of the bounds is a **three-tier
ladder**, not a dichotomy (auditor correction):

- **(a) `δ_t` affine in `q`** for every `t` ⟹ `P_S(r)` is a **polytope** —
  coordinate and linear-functional bounds are LPs (closed form for the
  coordinate bounds). Squared distance, frequency-guessing, KL, RPS.
- **(b) `δ_t` monotone but transcendental in `q`** ⟹ `P_S(r)` is a finite
  intersection of monotone-transcendental inequalities — **semi-analytical**.
  Caveat: each facet couples *two* coordinates, so the sharp coordinate and
  mean bounds are a finite optimization over the *joint* region; they do **not**
  decompose into per-coordinate root-finds. A genuine reduction to a
  one-dimensional monotone root-find is a *rule-specific bonus* — Manhattan
  enjoys it via its threshold-`c` representation (all facets share the form
  `F_i(r_i)≥F_j(r_j−1)`), but it is not automatic for every rule in the convex
  family.
- **(c) `δ_t` non-monotone in `q`** ⟹ a facet's `q`-inverse-image is a union of
  intervals; `P_S(r)` need not be convex or connected. Bounds are at best
  threshold-computed / simulation. Nothing forces `δ_t` monotone in the belief
  for a general discrete-convex `d`, so this tier is real, though the screened
  rules all fall in (a) or (b).

This inversion — from a classical resource-allocation optimum to a
sharply-characterized identified set of beliefs, with the bound-tractability
ladder — is the genuinely new object. The literature check found no prior work
performing it. (Consistent with the project guardrail: mean bounds are
optimizations over the full identified set `P_S(r)`, never combinations of
coordinate intervals.)

--------------------------------------------------------------------------------

## 5. Novelty delineation (explicit, for the manuscript)

| Component | Status | Citation |
|---|---|---|
| Single-transfer sufficiency ⟺ discrete-convexity (the iff) | **classical** | Fox 1966; Federgruen & Groenevelt 1986; Ibaraki & Katoh 1988 |
| Expectation preserves discrete convexity (Prop 4 step) | **classical / elementary** | Murota 2003, or one-line proof |
| Optimal-report problem = discrete separable resource allocation (Lemma 1) | **the paper's reduction** — immediate once seen, but the connecting move | — |
| Feasibility-frontier map of frequency-report scoring rules (§4) | **the paper's contribution** | — |
| Identified-set inversion + the three-tier tractability ladder (Cor 5) | **the paper's contribution** | — |

Manuscript language must say the optimization characterization is classical and
cite it; the contribution claims should be hedged "to our knowledge" for the
application and the inversion. Keep distinct from the classical *properness*
characterization (a scoring rule is proper iff the expected score is convex *in
the probability vector* — Savage; Gneiting & Raftery): that is a different
convexity, of a different object, and a referee could conflate them.

--------------------------------------------------------------------------------

## 6. Verification

- `scripts/candidate_rule_checks.py` (finite enumeration, `n∈{4,5,6}`,
  `k∈{3,4}`): single-transfer-local optimum `==` global optimum for every
  discrete-convex rule tested (squared, KL, RPS, pinball, Hellinger — 0
  mismatches); the Gate-C affine/non-affine split matches tiers (a) and (b) of
  Corollary 5's ladder.
- The Hamming failure (Lemma 2 ⟹ direction) is exact-verified in
  `bounds_search_manhattan_hamming.md` and `outputs/verification/`.
- The `⟸` direction is the audited Manhattan Claim C; the theorem-developer
  verified its proof uses only discrete-convexity, and the `theory-auditor`
  pass confirmed the generalization is mathematically sound.

Finite checks corroborate; they are not proofs. Lemma 2 itself rests on the
cited classical results.

--------------------------------------------------------------------------------

## 7. Status and next steps

- **Audit (complete).** The `theory-auditor` pass returned: Props 1–2 SOUND;
  Theorem 3 ⟸, Props 3′/4 and Corollary 5 SOUND-WITH-FIX. All fixes are
  incorporated above. The remaining manuscript obligation is to write the
  Theorem 3 ⟸ proof at full rigor (the explicit unit-bijection and sender-side
  bound). One audit recommendation — the converse / non-convexity direction —
  is moot here: it is the classical necessity half (Federgruen & Groenevelt),
  cited not proven. (The audit ran in a background environment that did not see
  the working tree, so it could not read Claim C directly; the theorem-developer
  pass, which did read it, supplies that check.)
- **Literature verification.** Confirm against the full text of Federgruen &
  Groenevelt (1986) that, restricted to separable objectives, their
  necessary-and-sufficient condition is exactly coordinatewise discrete
  convexity (for the *separable* simple resource-allocation problem this is
  textbook Ibaraki & Katoh — solid — but the citation phrasing should be exact).
- **References.** When this reaches the manuscript, add to `references.bib`:
  Fox (1966, *Management Science* 13(3)); Federgruen & Groenevelt (1986,
  *Operations Research* 34(6):909–918); Ibaraki & Katoh (1988, *Resource
  Allocation Problems*, MIT Press); Murota (2003, *Discrete Convex Analysis*,
  SIAM).
- **Manuscript home (gated).** If adopted: an organizing lemma in §3 (it
  precedes and unifies the three rule subsections), with §5's Hamming/Chebyshev
  discussion reframed as the two failure modes. No manuscript edit until the
  audit closes and a placement decision is taken.
- **Disposition.** Per the user's decision, this is carried as an organizing
  lemma + application, not a headline theorem.
