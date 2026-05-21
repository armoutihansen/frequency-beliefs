# Analytical Bounds Search: Manhattan and Hamming Frequency Scoring

Mode: exploration. Status: derivation memo, not a manuscript claim.
Date: 2026-05-21. Scope: time-boxed `analytical-bounds-search` for the two
non-quadratic, non-discrete-metric headline rules. Coordinate bounds are the
primary target; mean bounds are attempted only where coordinate bounds yield.

All numerical statements below are finite computational checks (enumeration over
feasible reports, random Dirichlet beliefs, and simplex grids). They corroborate
the derivations but are not proofs. Proofs and proof gaps are stated explicitly.

Notation. Latent multinomial beliefs `p` in the simplex `Delta`; `n` trials;
realized count `omega ~ Multinomial(n,p)`; report `r` a feasible integer count
vector with `sum r_i = n`. Marginal `W_i ~ Bin(n,p_i)`. `F_i(t) = F(t;n,p_i) =
Pr(W_i <= t)`, with the conventions `F(-1;n,p)=0` and `F(n;n,p)=1`. `b(t;n,p) =
Pr(Bin(n,p)=t)`. The identified set is `P_S(r) = { p in Delta : r in R_S(p) }`
with ties included.

--------------------------------------------------------------------------------
AUDIT STATUS (theory-auditor, 2026-05-21).
The Manhattan derivation was independently audited. Claims A, B, D, E: sound.
Claim C (single-unit-transfer sufficiency — load-bearing): SOUND; the identified
set P_M(r) is exact. Claim F (coordinate-bound theorem): sound; the bound
sup p_h = max_c g_h(c) is correct and the function is unimodal. Two EXPOSITORY
fixes for the eventual manuscript proof (neither is a logical gap):
  1. Claim C proof: add one sentence noting that a below-target coordinate
     stays below target along the monotone path (so it never becomes a sender).
  2. Claim F: state the maximum of the unimodal g_h over [c_lo,c_hi] as
     "attained at the interior crossing OR at an interval endpoint", rather than
     "at the crossing, clamped".
The Hamming section below was corrected after an exact-arithmetic re-audit (see
the dated note in section (3')).
--------------------------------------------------------------------------------

================================================================================
## RULE 1 — MANHATTAN DISTANCE
================================================================================

### (1) Rule

`S_M(r,omega) = a - b * sum_i |r_i - omega_i|`, `b>0`. Risk-neutral subject
maximizes expected score, equivalently minimizes expected loss.

### (2) Expected loss

By linearity of expectation the expected loss is separable across coordinates:

  L_M(r;p) = sum_i E|r_i - W_i| = sum_i ell_i(r_i;p_i),
  ell_i(t;p_i) = E|t - W_i|, W_i ~ Bin(n,p_i).

The coordinates are coupled only through the budget constraint `sum_i r_i = n`.

Verification of claim (a). For integer `t` with `0 <= t <= n-1`,

  ell_i(t+1;p_i) - ell_i(t;p_i)
    = E|t+1-W_i| - E|t-W_i|
    = sum_w ( |t+1-w| - |t-w| ) Pr(W_i=w).

For `w <= t` the bracket is `+1`; for `w >= t+1` it is `-1`. Hence the increment
equals `Pr(W_i <= t) - Pr(W_i >= t+1) = 2 F_i(t) - 1`. CONFIRMED.

Since `F_i(t)` is nondecreasing in `t`, the increment `2 F_i(t) - 1` is
nondecreasing in `t`; therefore `ell_i(.;p_i)` is discrete-convex. CONFIRMED.
(Numerical check: increment formula matched to 1e-9 across all tested `n,p,i,t`,
consistent with the existing `verify_regions.py` check `L1 delta formula`.)

### (3) Optimal-report condition

A one-count transfer from category `j` (with `r_j > 0`) to category `i` (with
`r_i < n`) produces report `r'` with `r'_i = r_i+1`, `r'_j = r_j-1`. The change
in total expected loss is, using claim (a) twice,

  L_M(r';p) - L_M(r;p)
    = [ ell_i(r_i+1) - ell_i(r_i) ] + [ ell_j(r_j-1) - ell_j(r_j) ]
    = ( 2 F_i(r_i) - 1 ) - ( 2 F_j(r_j-1) - 1 )
    = 2 [ F_i(r_i) - F_j(r_j-1) ].

So no single-unit transfer lowers loss iff

  F_i(r_i) >= F_j(r_j-1)   for all i with r_i<n and all j with r_j>0.   (M-opt)

Claim (b) CONFIRMED, with the standard caveat that the receiver index `i` and
sender index `j` must differ; the `i=j` term is vacuous.

### (3') Sufficiency of single-unit-transfer optimality — claim (c)

This is the crucial step. The objective `sum_i ell_i(r_i)` is a separable sum of
discrete-convex (integer-convex) functions, minimized over the integer simplex
`B = { r in Z_{>=0}^k : sum_i r_i = n }`.

Theorem (discrete separable convexity). Let each `ell_i : {0,...,n} -> R` be
discrete-convex (increments nondecreasing). Then a feasible `r in B` minimizes
`sum_i ell_i(r_i)` over `B` if and only if no single-unit transfer strictly
lowers the objective.

Proof. Necessity is immediate. For sufficiency, suppose `r` is single-transfer
optimal and let `s in B` be arbitrary. The difference vector `s - r` sums to
zero, so it can be written as a sum of unit transfers: there is a sequence
`r = r^(0), r^(1), ..., r^(m) = s` where each step moves one count from some
category to another, and `m = (1/2) sum_i |s_i - r_i|`. Moreover the sequence
can be chosen monotone: at every step move a unit from a category currently
above its target `s` to a category currently below its target `s` (such a pair
always exists while `r^(l) != s`). Along a monotone path, each receiving
category's count only increases and stays `<= s_i <= n`, and each sending
category's count only decreases and stays `>= s_j >= 0`; so every intermediate
`r^(l)` is feasible. By discrete-convexity of each `ell_i`, the marginal cost of
the transfer at step `l` (moving a unit `j -> i`) is `[ell_i(c_i+1)-ell_i(c_i)]
+ [ell_j(c_j-1)-ell_j(c_j)]` with `c_i >= r_i` and `c_j <= r_j` along a monotone
path; by convexity `ell_i(c_i+1)-ell_i(c_i) >= ell_i(r_i+1)-ell_i(r_i)` and
`ell_j(c_j-1)-ell_j(c_j) >= ell_j(r_j-1)-ell_j(r_j)`. Hence each step's cost is
at least the cost of the corresponding transfer evaluated AT `r`, which is
nonnegative by single-transfer optimality of `r`. Summing, `L_M(s) >= L_M(r)`.
QED.

(This is the integer/separable specialization of the exchange/M-natural-convex
optimality theorem; see Murota, Discrete Convex Analysis. A separable sum of
discrete-convex functions restricted to a hyperplane `sum r_i = n` is
M-natural-convex, and for M-natural-convex functions local exchange optimality
implies global optimality. The self-contained monotone-path argument above
avoids invoking the general theory.)

Conclusion: for Manhattan, single-unit-transfer optimality IS sufficient for
global optimality. Therefore `P_M(r)` defined by (M-opt) is the EXACT identified
set, not merely an outer set.

Numerical corroboration: 0 mismatches in 32,700 (report, belief) pairs over
`n in {3,4,5,6}`, `k in {3,4}`, comparing (M-opt) to brute-force global
optimality. Consistent with the existing `L1 exchange region` check.

### (4) Inverse-region representation

Claim (d). The pairwise system (M-opt) is `min_i F_i(r_i) >= max_j F_j(r_j-1)`.
This holds iff there exists a scalar `c in [0,1]` with

  F_i(r_i-1) <= c <= F_i(r_i)   for all i.    (M-thresh)

The two are algebraically identical: a real `c` lies between `max_j F_j(r_j-1)`
and `min_i F_i(r_i)` iff that lower envelope does not exceed that upper envelope,
which is exactly (M-opt). With `r_i=0` the lower constraint is `0 <= c` (no
constraint); with `r_i=n` the upper constraint is `c <= 1` (no constraint).
CONFIRMED (0 mismatches in 32,700 pairs).

Claim (e). `F(t;n,u)` is continuous and strictly decreasing in `u` on `(0,1)`
for fixed `t < n` (derivative `-n*b(t;n-1,u) < 0`). So for fixed `c` the
constraint `F_i(r_i-1) <= c <= F_i(r_i)` inverts to an interval

  p_i in [ lo_i(c), hi_i(c) ],
  lo_i(c) = F^{-1}(r_i-1; c) (=0 if r_i=0),
  hi_i(c) = F^{-1}(r_i; c)   (=1 if r_i=n),

where `F^{-1}(t; c)` is the unique `u` with `F(t;n,u)=c`. Both endpoints are
nonincreasing in `c` (larger `c` => smaller `u`). The set of `p` admissible at
threshold `c` is the box `B(c) = prod_i [lo_i(c),hi_i(c)]`; the identified set is

  P_M(r) = union over c in [0,1] of ( B(c) intersect Delta ).

CONFIRMED.

### (5) Coordinate-bound attempt

Fix coordinate `h`. We want `sup p_h` over `P_M(r)`. For fixed `c`, the largest
`p_h` consistent with `B(c) intersect Delta` is

  g_h(c) = min( hi_h(c) , 1 - sum_{i != h} lo_i(c) ),

i.e. either `p_h` is capped by its own box, or it is `1` minus the minimum the
other coordinates can take while staying in their boxes. This requires `B(c)`
to actually meet the simplex, i.e. `sum_i lo_i(c) <= 1 <= sum_i hi_i(c)`.

Monotonicity in `c`: `hi_h(c)` is nonincreasing; `sum_{i!=h} lo_i(c)` is
nonincreasing, so `1 - sum_{i!=h} lo_i(c)` is nondecreasing. Therefore `g_h` is
the min of a nonincreasing and a nondecreasing function: it is unimodal
(quasi-concave) in `c`. Its maximum over the feasible `c`-interval is attained
either at the crossing `hi_h(c*) = 1 - sum_{i!=h} lo_i(c*)`, or at a feasibility
endpoint of the `c`-interval `[c_lo, c_hi]` defined by `sum lo_i(c) <= 1` and
`sum hi_i(c) >= 1`. Both defining functions are monotone in `c`, so `c_lo, c_hi`
are themselves the solutions of two monotone scalar equations. Claim (f)
CONFIRMED, with the refinement that the optimum is the crossing CLAMPED to
`[c_lo,c_hi]` (it can sit at an endpoint when the crossing is infeasible).

Symmetrically, `inf p_h = inf_c max( lo_h(c), 1 - sum_{i!=h} hi_i(c) )`, a min
over `c` of the max of a nonincreasing and a nondecreasing function, again
unimodal, optimum at a clamped crossing.

THEOREM (Manhattan sharp coordinate bound — semi-analytical).
Assume single-unit-transfer optimality (proven sufficient in (3')). For an
observed report `r` with `P_M(r)` nonempty, and any coordinate `h`,

  sup_{p in P_M(r)} p_h = max_{c in [c_lo,c_hi]} min( hi_h(c), 1 - sum_{i!=h} lo_i(c) ),
  inf_{p in P_M(r)} p_h = min_{c in [c_lo,c_hi]} max( lo_h(c), 1 - sum_{i!=h} hi_i(c) ),

each a one-dimensional optimization of a unimodal function of the scalar `c`,
solved by a single monotone scalar root-find (the clamped crossing).

Status of theorem: proof complete for the reduction to the scalar problem;
the only non-elementary ingredient is `F^{-1}`, the inverse binomial CDF in the
probability argument, which has no closed form. Hence the bound is
SEMI-ANALYTICAL, one-dimensional, and sharp — not closed form. This is the
expected best outcome and it is attained; it is a genuine upgrade over an
unstructured threshold/grid search because (i) it is sharp (a true sup/inf, not
a grid maximum) and (ii) it reduces to one scalar root, not a 2D or grid scan.

Counterexample checks. Threshold-crossing bounds matched fine-grid bounds for
`(n,k,r)` in {(5,3,(2,2,1)), (5,3,(3,2,0)), (8,3,(4,3,1)), (10,3,(5,3,2)),
(6,3,(2,2,2)), (8,4,(3,3,1,1))}; the threshold values were consistently equal
to or slightly tighter than the coarse grid, as expected for a sharp envelope.
No counterexample to unimodality of `g_h` was found.

### (6) Mean-bound attempt

The coordinate-bound result is clean, so a mean bound is in scope. For a payoff
vector `x`, `sup a^T p` over `P_M(r)`. For fixed `c`, the inner problem is a
linear objective over the box-simplex `B(c) intersect Delta`, solved by greedy
water-filling: start at `lo(c)`, fill the residual `1 - sum lo_i(c)` into
coordinates in decreasing order of `x_i` up to each `hi_i(c)`. The resulting
value `phi_x(c)` is piecewise-linear and continuous in `c`, but NOT generally
monotone or unimodal: as `c` increases, all `lo_i` and `hi_i` shift together and
the greedy ordering can change which coordinate is marginal. So the mean bound
does NOT reduce to a single scalar crossing.

Honest classification of the mean bound: `sup a^T p = max_{c in [c_lo,c_hi]}
phi_x(c)`, a one-dimensional optimization of a continuous piecewise-linear
function with finitely many breakpoints (breakpoints occur where a `hi_i(c)`
enters/leaves the active fill set, or where two coordinates tie in `x` — but `x`
is fixed, so only fill-set changes matter). It is therefore a one-dimensional
THRESHOLD SEARCH over a function whose pieces are individually maximizable, not
a single closed crossing. Semi-analytical but weaker than the coordinate case.
This should NOT be presented as closed form.

### (7) Special cases

k=2. Write `r=(t,n-t)`. The only transfer pairs are `0<->1`. (M-thresh) becomes
`F(t-1;n,p_1) <= c <= F(t;n,p_1)` for coordinate 1 and `F(n-t-1;n,1-p_1) <= c <=
F(n-t;n,1-p_1)` for coordinate 2; the second is implied by the first via
`F(t;n,p_1) = 1 - F(n-t-1;n,1-p_1)` plus the existence quantifier. Eliminating
`c` and using the budget `p_2=1-p_1`, the surviving condition is exactly

  P_{M,1}(r) = { p_1 : F(t-1;n,p_1) <= 1/2 <= F(t;n,p_1) },

the binomial-median interval. (Take `c=1/2` by the symmetry `F(t;n,p_1) +
F(n-t-1;n,1-p_1) = 1`.) CONFIRMED in `verify_regions.py` (`binary L1 median`).
This matches the existing paper text.

Boundary reports. `r_i=0`: no lower constraint, `lo_i(c)=0`; `r_i=n`: no upper
constraint, `hi_i(c)=1`. These are handled by the conventions `F(-1)=0`,
`F(n)=1` and require no special treatment in the theorem.

Ties. (M-opt) uses weak inequalities, so `p` on a face where a transfer is
exactly cost-neutral is included: `r` is then one of several optimal reports,
consistent with the ties-included definition of `P_S(r)`.

Empty c-interval. The feasible `c`-interval `[c_lo,c_hi]` is empty exactly when
no box `B(c)` meets the simplex, i.e. when `P_M(r)` itself is empty (no belief
rationalizes `r`). For any `r` that is optimal for at least one `p` the interval
is a nonempty closed subinterval of `[0,1]`. So emptiness is not a pathology of
the method; it correctly reports an unrationalizable report.

### (8) Analytical status [classification]

- Optimal-report correspondence: CLOSED FORM (pairwise CDF inequalities (M-opt)).
- Inverse region `P_M(r)`: SEMI-ANALYTICAL (exact union-of-boxes / threshold
  representation; exact, not an outer approximation).
- Coordinate bounds: SEMI-ANALYTICAL — sharp, one-dimensional, reduces to a
  single monotone scalar root-find (clamped crossing). NOT closed form (inverse
  binomial CDF is non-elementary).
- Mean / linear-functional bounds: SEMI-ANALYTICAL via a one-dimensional
  THRESHOLD SEARCH over a piecewise-linear function; weaker than the coordinate
  case. NOT closed form.

### (9) Computational fallback

If a deployment wants to avoid root-finding: evaluate `g_h(c)` and `phi_x(c)` on
a `c`-grid. Because `g_h` is unimodal the coordinate-bound grid error is
controlled and the search can be a golden-section / bisection on the crossing.
The current `verify_regions.py` `l1_threshold_bounds` already implements a
`c`-grid; it should be upgraded to bracket-and-root-find the crossing for the
coordinate bounds to make the reported numbers genuinely sharp rather than
grid-limited.

### (10) Safe manuscript statement

"For Manhattan-distance frequency scoring, single-unit-transfer optimality is
both necessary and sufficient, because the expected loss is a separable sum of
discrete-convex coordinate losses minimized over the integer simplex; hence the
identified set `P_M(r)` is characterized exactly by the pairwise inequalities
`F_i(r_i) >= F_j(r_j-1)`. Equivalently, `p` is in `P_M(r)` iff a single
threshold `c` lies in every interval `[F_i(r_i-1), F_i(r_i)]`. The sharp
coordinate bounds are obtained from a one-dimensional, monotone scalar equation
in this threshold; they are semi-analytical rather than closed form, since the
inverse binomial CDF is not elementary. We do not claim a closed-form coordinate
formula for `k>2`."

================================================================================
## RULE 2 — HAMMING DISTANCE
================================================================================

### (1) Rule

`S_H(r,omega) = a - b * sum_i 1{r_i != omega_i}`, `b>0`. Penalizes the number of
coordinates whose reported count differs from the realized count.

### (2) Expected loss

By linearity of expectation,

  L_H(r;p) = sum_i E[ 1{r_i != W_i} ] = sum_i ( 1 - Pr(W_i = r_i) )
           = sum_i ( 1 - b(r_i;n,p_i) ).

CONFIRMED. The optimal report maximizes `G(r;p) = sum_i b(r_i;n,p_i)` subject to
`sum r_i = n`.

Unimodality / non-concavity of `b(t;n,p)` in `t`. For fixed `n,p`, the binomial
pmf is unimodal in `t` with mode(s) at `floor((n+1)p)` (and `(n+1)p - 1` when
`(n+1)p` is an integer). The ratio `b(t+1)/b(t) = (n-t)/(t+1) * p/(1-p)` is
strictly decreasing in `t`, which gives strict unimodality. But `b` is NOT
discrete-concave: the second difference `b(t+1) - 2 b(t) + b(t-1)` changes sign
(positive in the tails, negative near the mode). CONFIRMED. This is the
structural obstruction.

### (3) Optimal-report condition

Single-unit transfer `j -> i` (`r_j>0`, `r_i<n`) changes `G` by

  Delta G = [ b(r_i+1;n,p_i) - b(r_i;n,p_i) ] + [ b(r_j-1;n,p_j) - b(r_j;n,p_j) ].

So `r` is single-transfer optimal iff `Delta G <= 0` for all admissible `i != j`:

  [ b(r_i+1;p_i) - b(r_i;p_i) ] + [ b(r_j-1;p_j) - b(r_j;p_j) ] <= 0.   (H-loc)

This is NECESSARY for global optimality.

### (3') Sufficiency FAILS — claim (c), decisive question

[CORRECTED 2026-05-21 after exact-arithmetic re-audit. An earlier draft of this
section gave a float-based counterexample that turned out to be a numerical-
tolerance artifact. The CONCLUSION below — single-transfer optimality is not
sufficient for Hamming — is correct and is now backed by exact rational
arithmetic. The mechanism and the location of the failure are corrected.]

Because each `b(.;n,p_i)` is unimodal but NOT discrete-concave, the separable-
discrete-convexity theorem used for Manhattan does not apply. The marginal-cost
monotonicity step in that proof ("each step's cost is at least the cost at `r`")
breaks: a multi-count transfer can traverse a valley of `-b` and end on a higher
peak of `b`, even though every single step is not strictly profitable.

Retracted earlier counterexample. An earlier draft cited `n=5, k=3,
p=(0.9998,0,0.0002), r=(0,0,5)` as "single-transfer optimal but not globally
optimal." This is WRONG. In exact arithmetic the transfer `2 -> 0` to `(1,0,4)`
strictly increases `G` (by order `1.6e-14`), so `r` is NOT single-transfer
optimal. The earlier float sweep classified it as single-transfer optimal only
because the improving transfer fell below `verify_regions.py`'s `1e-10`
tolerance. The "110 near-boundary mismatches" reported earlier are the same
artifact and must NOT be relied on. Float-based mismatch sweeps are unreliable
for this question because the obstruction lives where pmf values are near zero.

Correct, exact-arithmetic counterexample. `n=2`, `k=3`,

  p = (0, 0, 1),   r = (0, 2, 0).

This is a simplex VERTEX belief (a subject certain the outcome is category 2),
which is a legitimate point of the closed simplex `Delta`. Exact arithmetic:
`G(r;p) = b(0;2,0) + b(2;2,0) + b(0;2,1) = 1 + 0 + 0 = 1`. The two single
transfers from `r` go to `(1,1,0)` with `G = 0` and to `(0,1,1)` with `G = 1`;
neither STRICTLY increases `G`, so `r` IS single-transfer optimal. But the
global optimum is `(0,0,2)` with `G = 3` (`L_H = 0`), reached only by a
two-count transfer. So `r` is single-transfer optimal yet not globally optimal.

Where the failure lives — corrected. An exact rational-grid search (`n = 2..9`,
`k = 3`, simplex grids of denominator `12, 20, 30, 60`) found 1536 genuine
strict counterexamples and ZERO interior counterexamples: every counterexample
has at least one coordinate `p_i` EXACTLY `0`. The obstruction is therefore a
BOUNDARY phenomenon. At a belief with a zero coordinate, `b(t;n,p_i)` has exact-
zero values away from `{0,n}`, creating flat plateaus on which single transfers
are cost-neutral while a multi-count transfer still reaches a strictly better
report. This is sharper and more honest than the earlier "near the boundary,
`min(p) ~ 1e-3`" description, which conflated genuine boundary counterexamples
with sub-tolerance float noise.

Interior status — REFUTED (2026-05-21, Step 0a of the Hamming-first plan;
`scripts/hamming_interior_search.py`, artifact
`outputs/verification/hamming_interior_search.md`). An earlier version of this
memo recorded interior sufficiency as an open conjecture, the `k=3` exact
search having found no interior counterexample. An extended exact
rational-arithmetic search over `k=4,5,6` REFUTED it. Cleanest counterexample:
`n=3`, `k=5`, the UNIFORM belief `p=(1/5,1/5,1/5,1/5,1/5)`. The report
`r=(3,0,0,0,0)` is single-unit-transfer optimal — coordinate 1 is the only
sender and every transfer from it changes `G` by
`[b(1)-b(0)]+[b(2)-b(3)] = -16/125 + 11/125 = -5/125 < 0` — yet `G(r)=257/125`
while `s=(0,0,1,1,1)` has `G(s)=272/125 > G(r)`. The obstruction is therefore
NOT a boundary phenomenon: it occurs at the most interior point of the simplex,
and because every single-transfer increment is strictly negative and
`G(s)-G(r)` is strictly positive, single-transfer sufficiency fails on a
positive-measure set of strictly interior beliefs (verified for `k>=5`). The
`k=3` null result was a `k=3`-specific fact, not evidence for general interior
sufficiency. Consequence: `(H-loc)` is a strict outer set even on the interior
— there is no theorem route to certified-sharp Hamming bounds by collapsing
`P_H(r)` to `(H-loc)`.

Conclusion on claim (c). Single-unit-transfer optimality is NECESSARY but NOT
SUFFICIENT for Hamming (the failure occurring even at strictly interior
beliefs — see the REFUTED note above). The
single-transfer system `(H-loc)` defines only an OUTER set; the exact `P_H(r)`
requires the full report set:

  P_H(r) = { p in Delta : L_H(r;p) <= L_H(s;p) for ALL feasible s }.

This is an intersection of up to `C(n+k-1,k-1)` inequalities, each of the form
`sum_i b(r_i;n,p_i) >= sum_i b(s_i;n,p_i)` — a difference of products of
degree-`n` polynomials in `p`. `P_H(r)` is NOT a polytope and not generally
convex. (Verified: `global-optimal => single-transfer-optimal` held in 10,000/
10,000 pairs, confirming `(H-loc)` is a valid outer set.)

### (4) Inverse-region representation

Exact: `P_H(r)` is the semialgebraic set defined by the full system of
polynomial inequalities above. No reduction to a polytope or a one-dimensional
threshold family is available, because the obstruction is the non-concavity of
`b` in `t`, which is intrinsic and does not vanish under reparametrization.

Two-sided sandwich that IS available:

  MODAL BOX (inner)  ⊆  P_H(r)  ⊆  SINGLE-TRANSFER REGION (outer).

- Outer set: `(H-loc)`, the single-transfer inequalities. Valid outer bound
  (necessity), verified 10,000/10,000.
- Inner set: see (5).

### (5) Coordinate-bound attempt

Per-coordinate modal condition. `b(t;n,p_i)` is maximized over `t` exactly when
`t` is a mode of `Bin(n,p_i)`, which happens iff

  p_i in [ r_i/(n+1), (r_i+1)/(n+1) ]    (modal interval; ratio test on
  `b(t+1)/b(t) = (n-t)p/((t+1)(1-p))`, weak inequalities include modal ties).

THEOREM (Hamming inner bound — closed form, UNCONDITIONAL).
If `p_i in [r_i/(n+1), (r_i+1)/(n+1)]` for EVERY `i`, then `r` is a global
Hamming optimum, i.e. `p in P_H(r)`.

Proof. If `p_i` is in its modal interval then `b(r_i;n,p_i) = max_t b(t;n,p_i)`.
Hence for any feasible `s`, `G(r;p) = sum_i b(r_i;n,p_i) = sum_i max_t b(t;n,p_i)
>= sum_i b(s_i;n,p_i) = G(s;p)`. So `L_H(r;p) <= L_H(s;p)` for all `s`. QED.

Note this needs NO simplex-slackness assumption: it is unconditional. The
modal box `MB(r) = prod_i [r_i/(n+1),(r_i+1)/(n+1)]` intersected with `Delta` is
therefore a valid INNER bound for `P_H(r)`. Verified: 13,933/13,933 modal-box
beliefs were globally Hamming-optimal; and a separate test of 23,100 simplex-
projected modal-box points gave 0 failures.

[CORRECTED 2026-05-21] The modal box is the marginal-binomial-mode box: each
factor [r_i/(n+1),(r_i+1)/(n+1)] is the set of p_i for which r_i is a mode of
Bin(n,p_i). For k=2 this coincides with the discrete-metric coordinate interval
(there n+k-1 = n+1). For k>2 it does NOT coincide: the discrete-metric identified
set is the joint multinomial-mode set, whose coordinate projections are
[r_i/(n+k-1),(r_i+1)/(n+1)] — wider on the lower end. The modal box is strictly
contained, coordinate-wise, within the discrete-metric intervals. An earlier
draft of this memo wrongly equated the two for general k.

Is the modal box also an OUTER bound? NO. Tested: 2,472 of 10,000 globally-
Hamming-optimal `(r,p)` pairs had some `p_i` strictly outside its modal
interval. So `P_H(r)` is strictly larger than `MB(r)`: a coordinate `i` can sit
off its own mode if another coordinate's pmf gain compensates. Hence `MB(r)` is
a strict inner bound, and intersecting modal boxes with the simplex does NOT
give the sharp coordinate bounds.

Consequence for sharp coordinate bounds. The sharp `sup p_h` / `inf p_h` over
`P_H(r)` are optima of a linear objective over the non-convex semialgebraic set
`P_H(r)`. We could not reduce this to a closed form or to a one-dimensional
monotone equation. The structural reason: (i) `P_H(r)` is not convex, so the
extremum need not be at a vertex of any polytope; (ii) the defining inequalities
are degree-`n` polynomials, and the binding inequality at the optimum depends on
`p` in a way that does not factor coordinatewise; (iii) the non-concavity of `b`
means a "local" (single-transfer) relaxation is a strict outer set, so optimizing
over the outer set overstates the bound and is itself not closed form.

Best honest positive results for `k>2`:
- A closed-form INNER bound: the modal box `[r_i/(n+1),(r_i+1)/(n+1)]` (sound,
  unconditional; the marginal-binomial-mode box, distinct from the
  discrete-metric coordinate box for k>2 — see the correction above).
- A semi-analytical OUTER bound: optimize `p_h` over the single-transfer region
  `(H-loc)`. This region is still defined by polynomial (not linear)
  inequalities, so the outer optimization is itself a polynomial program, not a
  closed form; it is a valid over-estimate of the sharp bound.
- The sharp bound itself: BRUTE-FORCE FINITE COMPUTATION — optimize the linear
  objective over `P_H(r)` using the full enumerated polynomial system, e.g. by a
  fine simplex grid or a global polynomial-optimization solver, with a numerical
  tolerance.

Conditional sharpness. The modal box equals the sharp coordinate box exactly
when, for the report `r`, no globally-optimal belief has an off-mode coordinate.
A clean sufficient condition for this was NOT found. Heuristically the gap
between `MB(r)` and `P_H(r)` shrinks when `n` is large relative to `k` and `r`
is interior (all `r_i` away from `0` and `n`), because then each `b(.;n,p_i)` is
sharply peaked and off-mode compensation is expensive; but this is an
unverified heuristic, not a theorem, and should be labeled as such.

### (6) Mean-bound attempt

Not in scope: per the search protocol, mean bounds are attempted only if
coordinate bounds yield a clean (closed-form or semi-analytical sharp) result.
They do not for Hamming `k>2`. A mean bound over `P_H(r)` is a linear objective
over the same non-convex semialgebraic set and inherits the same classification:
brute-force finite computation. The closed-form inner bound gives a valid
(non-sharp) INNER mean interval via the discrete-metric LP over `MB(r)`.

### (7) Special cases

k=2. With `r=(t,n-t)` and `omega=(W,n-W)`, `W~Bin(n,p_1)`: since `W = t` iff
`n-W = n-t`, the two coordinate indicators are identical, so `sum_i 1{r_i !=
omega_i} = 2 * 1{r_1 != W}`. Maximizing `G` reduces to maximizing `b(t;n,p_1)`,
i.e. `t` a mode of `Bin(n,p_1)`. This is exactly the discrete-metric problem.
Hence

  P_{H,1}(r) = [ r_1/(n+1), (r_1+1)/(n+1) ],   CLOSED FORM,

identical to discrete-metric scoring. Verified within grid tolerance for
`n in {3,5,8,10}` and all `t`. (Boundaries: `t=0` gives `[0,1/(n+1)]`; `t=n`
gives `[n/(n+1),1]`.) This matches the existing paper text.

So for `k=2` Hamming inherits the discrete-metric closed form; the difficulty is
strictly a `k>2` phenomenon, created by the budget constraint coupling three or
more non-concave coordinate terms.

Degenerate / sparse beliefs. In the `k=3` exact search every counterexample to
single-transfer sufficiency had a coordinate exactly `0` — but this is
`k=3`-specific. The extended `k=4,5,6` search (see (3'), REFUTED note) found
interior counterexamples, including at the uniform belief; single-transfer
sufficiency fails on a positive-measure set of strictly interior beliefs for
`k>=5`. It is not a boundary-only phenomenon.

### (8) Analytical status [classification]

- Expected loss: CLOSED FORM (`sum_i (1 - b(r_i;n,p_i))`).
- Optimal-report correspondence (exact): requires ALL feasible `s`; the
  single-transfer system is only NECESSARY. Classification: the exact
  correspondence is a finite but non-local condition.
- Inverse region `P_H(r)`: exact form is a semialgebraic set (polynomial
  inequality system over all reports); NOT a polytope, NOT convex.
- Coordinate bounds, k=2: CLOSED FORM (= discrete-metric interval).
- Coordinate bounds, k>2:
  - closed-form INNER bound (modal box) — available;
  - semi-analytical / polynomial-program OUTER bound (single-transfer region) —
    available;
  - SHARP bound: BRUTE-FORCE FINITE COMPUTATION (grid or global polynomial
    optimization, with numerical tolerance). Not closed form, not semi-
    analytical, not a single threshold search.
- Mean bounds, k>2: BRUTE-FORCE FINITE COMPUTATION (not attempted as a primary
  target; inner bound available via the modal box).

### (9) Computational fallback

For `k>2`, sharp Hamming bounds are computed by enumerating feasible reports `s`
and the polynomial inequalities `G(r;p) >= G(s;p)`, then optimizing each
coordinate over the resulting semialgebraic set. Practical options: (i) a fine
simplex grid (the current `hamming_grid_bounds` in `verify_regions.py`), with
the bound reported as grid-limited; (ii) a global polynomial / nonconvex solver,
with a stated numerical tolerance. Either way the reported number is a
computed bound, NOT an exact sharp value, and the paper must qualify it.
The closed-form modal box should be reported ALONGSIDE as a valid inner bound,
which gives a rigorous two-sided sandwich `MB(r) ⊆ P_H(r) ⊆ {single-transfer}`.

### (10) Safe manuscript statement

"For Hamming-distance frequency scoring the expected loss is `sum_i
(1 - b(r_i;n,p_i))`, a separable sum of binomial point masses. Unlike the
Manhattan case, each coordinate term is unimodal but not discrete-concave in the
reported count, so single-unit-transfer optimality is necessary but not
sufficient for `k>2`: a multi-count transfer can move the report from one pmf
peak to a higher one. The exact identified set `P_H(r)` is therefore the
semialgebraic set defined by the expected-loss inequalities over all feasible
reports; it is not a polytope. For `k=2`, Hamming coincides with the discrete-
metric rule and inherits its closed-form coordinate interval. For `k>2` we
provide a closed-form inner bound — the modal box `prod_i [r_i/(n+1),(r_i+1)/(n+1)]`,
the marginal-binomial-mode box, unconditionally contained in `P_H(r)` — together
with the single-transfer region as an outer bound; the sharp coordinate bounds
themselves are computed numerically, and we report them as computed bounds with a
stated tolerance, not as closed-form sharp values."

================================================================================
## SUMMARY AND CLASSIFICATION TABLE
================================================================================

Rule       | Optimal report      | Inverse region      | Coordinate bounds
-----------|---------------------|---------------------|----------------------
Manhattan  | closed form         | semi-analytical     | SEMI-ANALYTICAL, sharp,
           | (pairwise CDF;      | (exact union of     | 1-D monotone scalar
           | single-transfer     | boxes / threshold)  | equation; not closed
           | proven sufficient)  |                     | form (inverse binom CDF)
-----------|---------------------|---------------------|----------------------
Hamming    | needs ALL reports   | semialgebraic,      | k=2: CLOSED FORM
           | (single-transfer    | non-convex, not a   | k>2: closed-form INNER
           | necessary only)     | polytope            | bound (modal box) +
           |                     |                     | computed sharp bound
           |                     |                     | (brute-force finite)

Manhattan mean bound: semi-analytical, 1-D piecewise-linear threshold search.
Hamming mean bound (k>2): brute-force finite computation; closed-form inner
bound available via the modal box.

================================================================================
## RECOMMENDATION ON ADR-0001 ("two analytical, two computational")
================================================================================

The framing should be REFINED, not discarded.

- Quadratic: closed-form coordinate bounds. Analytical. (Unchanged.)
- Discrete metric: closed-form coordinate bounds. Analytical. (Unchanged.)
- Manhattan: NOT closed form, but a genuine UPGRADE over the current draft's
  "threshold-computed" language. The identified set is EXACT (single-transfer
  sufficiency is now proven), and the coordinate bounds are SHARP and reduce to
  a one-dimensional monotone scalar equation. Recommended label: "semi-
  analytical: exact identified set, sharp coordinate bounds via a one-
  dimensional threshold equation." This is materially stronger than
  "computational" and the paper should say so.
- Hamming: genuinely COMPUTATIONAL for `k>2` sharp bounds — a documented
  negative result. The honest upgrade over the current draft is a proven,
  closed-form INNER bound (the modal box, the marginal-binomial-mode box; equal
  to the discrete-metric coordinate box only for k=2) plus a proven
  outer bound, giving a rigorous sandwich, and an explicit counterexample
  showing why a closed-form sharp bound is not available (non-concavity of the
  binomial pmf in the count). Recommended label: "computational, with a closed-
  form inner bound and a documented obstruction."

Net: the "two analytical / two computational" dichotomy is too coarse. A more
accurate four-way description is: two closed-form (quadratic, discrete metric),
one semi-analytical with sharp one-dimensional bounds (Manhattan), one
computational with a closed-form inner sandwich and a documented impossibility-
style obstruction (Hamming). The paper should adopt this finer language; ADR-0001
should be amended accordingly rather than left as a binary split.
