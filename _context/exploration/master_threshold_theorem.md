# Theorem-Development Memo: The Master Threshold Theorem

Date: 2026-06-10
Mode: exploration (theorem development). Nothing in this memo is a manuscript
claim. Adoption requires the audit task in Section 10 plus a novelty check
(Section 9) before any paper edit.

Companion verification script: `scripts/explore_master_threshold.py`
(finite computational checks; evidence, not proof).

---

## 1. Problem

The paper's Lemma 1 (`lem:transfer`) shows: if an optimal report minimizes a
separable objective with discrete-convex per-coordinate costs, the identified
set \(P_S(r)\) is exactly the set cut out by the \(O(k^2)\) single-transfer
inequalities. Downstream of the lemma, each headline rule currently gets its
sharp coordinate bounds by per-rule work: linearity for squared-distance and
frequency-guessing, the threshold/unimodality lemmas
(`lem:manhattan-unimodal`, `lem:l1-linear`) for Manhattan.

Target: a **master theorem** showing that the threshold representation, the
interval-valued coordinate projections, the single-monotone-scalar-equation
coordinate bounds, and the one-parameter LP family for linear functionals are
all *general consequences* of three conditions — separability (S), discrete
convexity (C), and a previously implicit third condition, monotone marginal
costs (M). Secondary, time-boxed target: what survives of the converse
("sharp bounds only if (S)+(C)"), at the level of the exact local
characterization of \(P_S(r)\).

**Relation to prior project work** (`feasibility_frontier.md` and
`rule_candidate_screen.md`, both 2026-05-22). The frontier memo already
develops the *optimality-level* characterization (its Lemma 2, cited as
classical: Fox; Federgruen–Groenevelt; Ibaraki–Katoh; Murota) and the
identified-set inversion (its Corollary 5), with a three-tier tractability
ladder. The delta here is concentrated in one place: **Corollary 5's tier
(b) caveat is removed.** That memo states that the reduction of sharp
coordinate bounds to a one-dimensional monotone root-find is "a
rule-specific bonus — Manhattan enjoys it via its threshold-\(c\)
representation ... but it is not automatic for every rule in the convex
family." Theorem A below shows it *is* automatic: tier (b)'s defining
property — \(\delta_t\) monotone in \(q\) — is exactly condition (M), and
(S)+(C) alone already yield the threshold representation by a max–min
argument the frontier memo did not take. Every tier-(b) rule (pinball,
expectile, Huber, Hellinger, \(L_p\), cumulative-\(L_1\)) therefore gets
Manhattan-grade machinery — exact threshold-box identified set, interval
projections, scalar-equation sharp coordinate bounds — and the tier-(a)
closed forms drop out of the same crossing equation with explicit
thresholds (C1–C2). The pinball rule itself was already identified as a
feasible candidate by the screen; what is new here is the proof that the
full bound machinery applies to it.

## 2. Definitions

Feasible reports \(\OmegaN=\{r\in\N_0^k:\sum_i r_i=n\}\). For a scoring rule
\(S\) define, as in the paper, \(R_S(p)\) and
\(P_S(r)=\{p\in\Delta^k: r\in R_S(p)\}\).

**(S) Separability (ordinal).** There exist per-coordinate costs
\(\ell_i:\{0,\dots,n\}\times[0,1]\to\R\cup\{+\infty\}\) such that for every
\(p\in\Delta^k\),
\[
R_S(p)=\argmin_{r\in\OmegaN}\sum_{i=1}^k \ell_i(r_i;p_i).
\]
Because the argmin is invariant to strictly increasing transforms of the
expected score, (S) is an *ordinal* condition: frequency-guessing satisfies it
via the log transform although its expected score is a product. The headline
rules have \(\ell_i=\ell\) for all \(i\); coordinate-dependent \(\ell_i\) is
allowed (asymmetric losses).

**(C) Discrete convexity.** For each \(i,q\), the forward difference
\(\Delta\ell_i(t;q)=\ell_i(t+1;q)-\ell_i(t;q)\) is nondecreasing in \(t\) on
\(\{0,\dots,n-1\}\).

**(M) Monotone marginals.** For each \(i\) and \(t\in\{0,\dots,n-1\}\), the map
\(q\mapsto\Delta\ell_i(t;q)\) is continuous (extended-real values permitted at
\(q\in\{0,1\}\), finite on \((0,1)\)) and strictly decreasing on \([0,1]\).

For an observed report \(r\), write the **receiver marginal**
\(A_v(q)=\Delta\ell_v(r_v;q)\) (defined when \(r_v<n\)) and the **sender
marginal** \(B_v(q)=\Delta\ell_v(r_v-1;q)\) (defined when \(r_v>0\)). Note
only the two difference levels \(t\in\{r_v-1,r_v\}\) enter for a given report.

Generalized inverse endpoints, for a threshold \(c\):
\[
p_v^{(L)}(c)=\begin{cases}\inf\{q\in[0,1]:B_v(q)\le c\}, & r_v>0\ (\inf\emptyset:=+\infty),\\ 0,& r_v=0,\end{cases}
\qquad
p_v^{(U)}(c)=\begin{cases}\sup\{q\in[0,1]:A_v(q)\ge c\}, & r_v<n\ (\sup\emptyset:=-\infty),\\ 1,& r_v=n.\end{cases}
\]
Slice: \(\Sigma(c)=\{p\in\Delta^k: p_v^{(L)}(c)\le p_v\le p_v^{(U)}(c)\ \forall v\}\).
Effective threshold set: \(C=\{c:\Sigma(c)\ne\emptyset\}\).

The \(\pm\infty\) conventions matter: an empty constraint set makes the box
empty, so spurious slices cannot arise. A cleaner device for proofs is the
**honest range** \(C_0=[\max_{v:r_v>0}B_v(1),\ \min_{v:r_v<n}A_v(0)]\): any
threshold witnessing \(p\in P_S(r)\) can be taken in \(C_0\) (a witness
\(c\) satisfies \(c\ge B_v(p_v)\ge B_v(1)\) and \(c\le A_v(p_v)\le A_v(0)\)
by (M)), and on \(C_0\) every constraint set is nonempty, so the inverse
endpoints are finite and the conventions never fire. Standing assumptions:
\(n\ge1\), \(k\ge2\); marginals are extended-real-valued, finite on
\((0,1)\), continuous in the extended sense.

## 3. Derivation (key steps)

1. **Max–min.** Lemma 1 gives \(p\in P_S(r)\) iff \(A_i(p_i)\ge B_j(p_j)\) for
   all \(i\ne j\) with \(r_j>0\) (receiver feasibility \(r_i+1\le n\) is
   automatic when some \(r_j>0\), \(j \neq i\)). Under (C), the diagonal
   comparisons \(A_v\ge B_v\) hold identically, so the system is equivalent to
   \(\min_{i:r_i<n}A_i(p_i)\ \ge\ \max_{j:r_j>0}B_j(p_j)\), i.e. to the
   existence of a threshold \(c\) with \(B_v(p_v)\le c\le A_v(p_v)\) for every
   coordinate (each constraint imposed only where defined). *This is exactly
   the Manhattan threshold representation of Proposition 3, and it is fully
   general given (S)+(C).* Economically, \(c\) is the Lagrange multiplier on
   the resource constraint \(\sum_i r_i = n\): the report is optimal iff some
   common marginal-cost level rationalizes every coordinate simultaneously.
2. **Inversion.** Under (M), \(\{q:B_v(q)\le c\}=[p_v^{(L)}(c),1]\) and
   \(\{q:A_v(q)\ge c\}=[0,p_v^{(U)}(c)]\) (closed, attained; empty cases
   encoded by \(\pm\infty\)). Hence \(P_S(r)=\bigcup_{c}\Sigma(c)\) with
   box–simplex slices whose endpoints are continuous and nonincreasing in
   \(c\) where finite.
3. **Crossing.** Maximizing \(p_i\) over a nonempty slice gives
   \(\min\bigl(p_i^{(U)}(c),\,1-\sum_{v\ne i}p_v^{(L)}(c)\bigr)\) — the min of
   a nonincreasing and a nondecreasing continuous function of \(c\) — so the
   sharp bound is located where the two cross, generalizing
   `lem:manhattan-unimodal` after one substitution: the binomial proof gets
   crossing *existence* from the full range of the CDF (LHS runs from
   \(\ge1\) at \(c=0\) to \(0\) at \(c=1\)), which abstract (M) does not
   supply, so Theorem A(iv) replaces it with the crossing-or-endpoint
   dichotomy plus the witness/compactness attainment argument. That step is
   new content, not inherited. The closed forms of Propositions 1–2
   drop out by solving the crossing equation explicitly (Section 4,
   Corollaries C1–C2): the squared-distance and Schlag–Tremewan constants are
   crossing thresholds.

## 4. Candidate statements

### Theorem A (master threshold theorem)

Let \(S\) satisfy (S) and (C), fix \(r\in\OmegaN\) with \(P_S(r)\ne\emptyset\).

**(i) Threshold representation.** [(S)+(C) only]
\[
P_S(r)=\bigl\{p\in\Delta^k:\ \exists c\in\overline\R,\ B_v(p_v)\le c\le A_v(p_v)\ \forall v\bigr\}.
\]

**(ii) Box slices.** [add (M)] \(P_S(r)=\bigcup_{c\in C}\Sigma(c)
=\bigcup_{c\in C_0}\Sigma(c)\); each \(\Sigma(c)\) is a box–simplex slice;
\(p_v^{(L)},p_v^{(U)}\) are continuous and nonincreasing in \(c\) on
\(C\subseteq C_0\); \(C\) is a nonempty interval (closed where the marginals
are finite, possibly unbounded when a marginal diverges at \(q\in\{0,1\}\),
e.g. frequency-guessing). On \(C_0\), per-coordinate box nonemptiness
\(p_v^{(L)}(c)\le p_v^{(U)}(c)\) is automatic — from (C) at coordinates with
\(0<r_v<n\), and from the \(C_0\) endpoint conditions at boundary
coordinates (\(r_v=0\) needs \(p_v^{(U)}(c)\ge0\), i.e.\ \(c\le A_v(0)\);
\(r_v=n\) needs \(p_v^{(L)}(c)\le1\), i.e.\ \(c\ge B_v(1)\)) — so
\(\Sigma(c)\ne\emptyset\) iff
\(\sum_v p_v^{(L)}(c)\le1\le\sum_v p_v^{(U)}(c)\).

**(iii) Interval projections.** Every coordinate projection of \(P_S(r)\) is a
closed interval \([\underline p_i(r),\overline p_i(r)]\) — even when
\(P_S(r)\) is non-convex.

**(iv) Scalar-equation bounds.**
\(\overline p_i(r)=\max_{c\in C}\min\bigl(p_i^{(U)}(c),\,1-\sum_{v\ne i}p_v^{(L)}(c)\bigr)\),
attained at any solution of
\[
p_i^{(U)}(c)+\sum_{v\ne i}p_v^{(L)}(c)=1
\]
when one exists in \(C\); when no crossing exists in \(C\), the bound is the
optimum of the binding monotone branch over \(C\), which is attained at a
finite threshold by the witness argument (the maximizer \(p^*\) of the
compact \(P_S(r)\) has a witness \(c^*\in C\cap C_0\) at which the slice
maximum already equals \(\overline p_i\)) — "endpoint of \(C\)" is not
literally meaningful when \(C\) is unbounded. The left side is continuous
and nonincreasing in \(c\), so the bound is the solution of a single
monotone scalar problem locatable by bisection. The solution set is an
interval on which the bound value is constant; under strict interior
monotonicity it is a single point. Symmetrically, \(\underline p_i(r)\)
solves \(p_i^{(L)}(c)+\sum_{v\ne i}p_v^{(U)}(c)=1\). Useful auxiliary fact:
any solution \(c\in C_0\) of the crossing equation automatically yields a
nonempty slice, since \(\sum_v p_v^{(L)}(c)\le p_i^{(U)}(c)+\sum_{v\ne
i}p_v^{(L)}(c)=1\le\sum_v p_v^{(U)}(c)\), using \(p_v^{(L)}(c)\le
p_v^{(U)}(c)\) for *all* \(v\) — valid on \(C_0\) per (ii), including
boundary coordinates; only the no-crossing branch needs an explicit
membership check.

**(v) Linear functionals.** For any \(a\in\R^k\),
\(\sup_{p\in P_S(r)}a^\top p=\sup_{c\in C}V_a(c)\), where \(V_a(c)\) is the
linear program over \(\Sigma(c)\) (solvable in closed greedy form per slice),
and \(V_a\) is continuous on \(C\). [Unimodality of \(V_a\) in \(c\) is NOT
claimed; open problem, Section 9.]

Status: (i) **proven in this derivation** (one-paragraph max–min argument on
top of Lemma 1). (ii)–(v) **proven in this derivation modulo write-up care**
at the boundary (empty-slice encoding, unbounded \(C\), attainment via
compactness of \(P_S(r)\)); the arguments are those of the existing audited
Manhattan lemmas with binomial-specific facts replaced by (M). Computational
corroboration: zero discrepancies vs brute force in 25,200 membership checks
(three rules) plus the four-rule grid run in the companion script.

### Corollary C1 (squared-distance: Prop 1 recovered, with explicit thresholds)

Marginals \(A_v(q)=2r_v+1-2nq\), \(B_v(q)=2r_v-1-2nq\); slices are sliding
boxes of width \(1/n\). The crossing equations are linear in \(c\) and give,
for \(m=m(r)\):
- upper bound, \(r_i>0\): \(c^*=2/m-1\), \(\overline p_i=(r_i+1)/n-1/(nm)\);
- upper bound, \(r_i=0\): \(c^*=(1-m)/(1+m)\), \(\overline p_i=m/(n(m+1))\);
- lower bound, \(r_i>0\): \(c^*=(k-2)/k\), \(\underline p_i=(r_i-1)/n+1/(nk)\).

Clamp validity at \(c^*\) checked (senders need \(c^*\le 2r_v-1\), true since
\(c^*\le1\le 2r_v-1\) for \(r_v\ge1\); receivers stay in \([0,1]\) for
non-vertex \(r\)). Status: **proven in this derivation** (elementary algebra;
verified to machine precision in the companion script).

### Corollary C2 (frequency-guessing: Schlag–Tremewan bounds recovered)

After the log transform, \(\Delta\ell(t;q)=\log(t+1)-\log q\). With
\(\lambda=e^c\), slices are multiplicative boxes
\(p_v\in[r_v/\lambda,(r_v+1)/\lambda]\). Crossing equations:
\((n+1)/\lambda=1\) (upper) and \((n+k-1)/\lambda=1\) (lower), i.e.
\[
\overline p_i=\frac{r_i+1}{n+1},\qquad \underline p_i=\frac{r_i}{n+k-1}.
\]
The constants \(n+1\) and \(n+k-1\) are crossing thresholds. One convention
note (second audit): the box description \(p_v\in[r_v/\lambda,(r_v+1)/\lambda]\)
omits the \(r_v=n\) convention \(p_v^{(U)}=1\); at a vertex report
\(r=n e_j\) with \(k>2\), the lower-bound equation for a coordinate
\(i\ne j\) has no finite crossing (the bound is the constant \(0\), the
no-crossing branch), while the generic algebra would silently write
\((n+1)/\lambda\) for the vertex coordinate. The stated formulas are
unaffected. Status: **proven in this derivation**; matches Proposition 2
exactly.

### Corollary C3 (Manhattan)

\(A_v(q)=2F(r_v;n,q)-1\), \(B_v(q)=2F(r_v-1;n,q)-1\); reparameterizing
\(c\mapsto(1+c)/2\in[0,1]\) recovers Proposition 3's threshold representation
and `lem:manhattan-unimodal`/`lem:l1-linear` as the special case of Theorem A.
Status: **proven** (specialization).

### Corollary C4 (convex location-loss family — new rules for free)

Let \(D(r,\omega)=\sum_i\psi_i(r_i-\omega_i)\) with each
\(\psi_i:\Z\to\R\) convex and **strictly discretely convex at the origin**,
\(\psi_i(-1)+\psi_i(1)>2\psi_i(0)\). ("Strictly kinked" is the wrong word:
\(\psi=x^2\) satisfies the condition with no kink.) Then (S), (C), (M) all
hold:
- (C): \(\ell_i(t;q)=\E_{W\sim\mathrm{Bin}(n,q)}\psi_i(t-W)\) is discrete-convex in
  \(t\) (expectation preserves convexity).
- (M), made rigorous by Abel summation: with
  \(g_t(w)=\psi_i(t+1-w)-\psi_i(t-w)\) nonincreasing in \(w\) (convexity),
  \[
  \Delta\ell_i(t;q)=\E[g_t(W)]
  =g_t(n)+\sum_{w=0}^{n-1}\bigl[g_t(w)-g_t(w+1)\bigr]F(w;n,q).
  \]
  Every bracket is \(\ge0\); each \(F(w;n,q)\) with \(w\le n-1\) is strictly
  decreasing in \(q\) (\(\partial F(t;n,q)/\partial q=-n\,b(t;n-1,q)\)); and
  for \(t\in\{0,\dots,n-1\}\) the bracket at \(w=t\) equals
  \(g_t(t)-g_t(t+1)=\psi_i(1)+\psi_i(-1)-2\psi_i(0)>0\), with both \(w=t\)
  and \(w=t+1\) in the support since \(t\le n-1\). Hence
  \(\Delta\ell_i(t;\cdot)\) is strictly decreasing. Continuity is polynomial.

So Theorem A applies wholesale: squared (\(\psi=x^2\)), Manhattan
(\(\psi=|x|\)), Huber, and the **asymmetric absolute (pinball) family**
\(\psi_\tau(x)=\tau x^+ +(1-\tau)x^-\) — already identified as a feasible
candidate in `rule_candidate_screen.md`; C4 supplies the proof that the full
sharp-bound machinery applies to it. Its forward problem elicits
coordinate-wise generalized \((1-\tau)\)-quantiles of the binomial marginals
up to the resource-constraint shift — the optimality condition is
\(F(r_v-1;n,p_v)\le(1-\tau)+c\le F(r_v;n,p_v)\) with \(c\) the common
multiplier, so the unconstrained-quantile reading holds exactly only when
\(c=0\) is feasible (\(\Delta\ell(t;q)=F(t;n,q)-(1-\tau)\)) — and its sharp
bounds are semi-analytical exactly like Manhattan's. Status: **proven in this
derivation** (strictness step now via the Abel identity above); pinball case
computationally verified (\(\tau=0.3\); zero membership mismatches, bounds
valid and sharp vs grid).

**Nonemptiness caveat.** "New rules for free" includes rules for which some
reports are never optimal, where the bound machinery is vacuous. Explicit
example (heterogeneous coordinate losses, \(k=2\), \(n=2\), \(r=(1,1)\)):
\(\psi_1(d)=2d+|d|\), \(\psi_2(d)=\varepsilon|d|\), both convex and strictly
discretely convex at the origin. Then
\(B_1(q)=\Delta\ell_1(0;q)=1+2F(0;2,q)\ge1\) while
\(A_2(q)=\Delta\ell_2(1;q)=\varepsilon\,(2F(1;2,q)-1)\le\varepsilon\), so for
\(\varepsilon<1\) the transfer \(1\to2\) improves at every \(p\):
\(P_S((1,1))=\emptyset\). The \(\pm\infty\) encoding in Section 2 handles
this correctly (every slice is empty), but Theorem A's hypothesis
\(P_S(r)\ne\emptyset\) is substantive, not cosmetic. For the three headline
rules \(p=r/n\in P_S(r)\) always (squared: \(r\) is the integer projection of
\(n\cdot r/n\); frequency-guessing: \(r\) is a mode at \(p=r/n\); Manhattan:
\(F(r_v-1;n,r_v/n)\le1/2\le F(r_v;n,r_v/n)\) — the binomial integer-mean
median fact), so nonemptiness holds there.

### Converse results (secondary target; level (a): exact local characterization)

**R1 (representation-level necessity — classical).** Single-transfer
optimality implies global optimality *for all separable instances* iff each
coordinate cost is discrete-convex; this is the classical greedy-optimality
characterization (Fox 1966; Federgruen–Groenevelt 1986; Ibaraki–Katoh 1988;
Murota 2003) that the paper already cites. Within a *fixed* rule's induced
family \(\{\ell_i(\cdot;q):q\in[0,1]\}\), necessity additionally requires the
non-convexity to be embeddable in a realizable instance (a richness condition
on how marginals vary with \(q\)). Status: **classical (cited), with the
embedding caveat stated here**.

**R2 (rule-level necessity for order-preserving representations).**
Distinguish two notions of "representation":
- *order-preserving*: a strictly increasing \(\varphi\) with
  \(\varphi(\E_p S(r,\omega))=-\sum_i\ell_i(r_i;p_i)\) — preserves the full
  preference order over reports at every \(p\) (this is what the
  frequency-guessing log transform does);
- *argmin-preserving*: only \(R_S(p)=\argmin_r\sum_i\ell_i(r_i;p_i)\) is
  required (the (S) used by Theorem A).

A local-global failure at one instance — a \(p\) and reports \(r,s\) with
\(r\) single-transfer optimal at \(p\) but \(\E_p S(s,\cdot)>\E_p S(r,\cdot)\)
— certifies that **no order-preserving separable discrete-convex
representation exists**: the transform preserves both "\(r\) weakly beats
every transfer neighbor" and "\(s\) strictly beats \(r\)", contradicting
Lemma 1's sufficiency for the transformed objective. Applied to the paper's
verified Hamming instance (\(n=3\), \(k=5\), uniform \(p\),
\(r=(3,0,0,0,0)\): expected-loss check with \(b(t;3,0.2)\) gives
\(L(r)=2.944\), all transfer neighbors \(2.984\), \(L(0,0,1,1,1)=2.824\);
`outputs/verification/hamming_interior_search.md`): **no strictly increasing
transform of the Hamming expected score at \((n,k)=(3,5)\) is separable with
discrete-convex coordinates.** Status: **proven (order-preserving case)**.

The argmin-level exclusion is **open**: an argmin-preserving representation
need not preserve the ranking of \(r\) against its transfer neighbors at a
\(p\) where neither is optimal (at the instance above the argmin is the
permutation orbit of \((1,1,1,0,0)\), so the comparison \(r\) vs.\ its
neighbors is unconstrained). Ruling that out would require violating a
correspondence-level implication of (S)+(C) — e.g.\ exhibiting an \(r'\) with
a disconnected coordinate projection of \(P_H(r')\), which under (S)+(C)+(M)
is impossible by A(iii). Candidate route, not attempted: compute Hamming
coordinate projections exactly at small \((n,k)\) and look for
non-interval projections.

**Essential caveat (the \(k=2\) subtlety).** Non-convexity of *a*
representation does not put a rule outside the class: Hamming at \(k=2\) has
the non-convex representation \(\sum_i\{1-\Pr(\mathrm{Bin}(n,p_i)=r_i)\}\) yet
*equals* frequency-guessing, which has a convex representation. The class
boundary is a property of the rule, and the existential quantifier over
\((n,k)\) in R2 is essential.

**Correction to `feasibility_frontier.md` Prop 3′** (quantifier fixed by the
second audit). That memo claims "for \(k=2\), single-transfer sufficiency is
*equivalent* to discrete-convexity of the folded cost
\(g(t)=\ell(t;p_1)+\ell(n-t;p_2)\) for all \((p_1,p_2)\)" and adds that no
actual count loss realizing a \(k=2\) exception "has been done." Both halves
need revision. Hamming at \(k=2\) is the realized exception **on the open
simplex**: on the simplex slice \(p_2=1-p_1\) its folded cost is
\(2\{1-b(t;n,p_1)\}\) (using \(b(n-t;n,1-p_1)=b(t;n,p_1)\)), which is *not*
discrete-convex (the pmf is not discrete-concave), yet for every
\(p_1\in(0,1)\) single-transfer sufficiency holds: the binomial pmf is
strictly log-concave there (likelihood ratio \(b(t+1)/b(t)\) strictly
decreasing), so weak local maxima form a single point or one adjacent tied
pair, all global. **At degenerate beliefs the claim fails**: at \(p_1=0\),
\(n=2\), the folded cost is \(g=(0,2,2)\), so \(r=(2,0)\) admits no
strictly improving transfer (\(g(1)=g(2)\)) yet is not globally optimal
(\(g(0)=0\)) — the zero plateau defeats weak single-transfer optimality, and
"strictly log-concave" is false at \(p_1\in\{0,1\}\). So the correct
statement is: the right \(k=2\) condition is "every local minimizer of the
folded cost is global" (discrete quasi-convexity), strictly weaker than
folded discrete convexity, with Hamming the realized exception on the open
simplex and the boundary handled separately (the product-form inequalities
of Proposition 2 cover it for the equivalent frequency-guessing
representation, with extended-real marginals). Domain note: the frontier
memo writes "for all \((p_1,p_2)\)" without fixing the domain; the natural
reading for this project is the simplex slice \(p_2=1-p_1\), and the
amendment should pin that down. Prop 3′ should be amended before any of its
content is promoted.

**R3 (necessity for location losses — conjecture).** For every non-convex
\(\psi\) there exist \(n,k,p\) at which single-transfer optimality fails to
imply global optimality for \(D=\sum_i\psi(r_i-\omega_i)\). Proof strategy:
near-vertex beliefs make \(\ell(\cdot;q)\to\psi(\cdot)\) as \(q\to0\),
exposing the raw non-convexity; embed a flat-local-minimum configuration
across several coordinates as in the Hamming uniform-belief instance. The
\(k=2\) caveat shows the \(\exists k\) quantifier cannot be dropped. Status:
**plausible conjecture; unresolved (time-boxed out)**.

**R4 (separability is not necessary — the M\(^\natural\) direction).** At
level (a), (S) itself is not necessary. The ranked probability score
\(\sum_{j<k}(R_j-\Omega_j)^2\) (cumulative counts \(R_j\), \(\Omega_j\sim\)
\(\mathrm{Bin}(n,P_j)\)) is *not* separable in the report coordinates, yet the
all-pairs single-transfer characterization held in 2,500/2,500 random
instances over \((n,k)\in\{(3,3),(4,3),(5,3),(4,4),(6,4)\}\) (companion
script, Check 3). The natural unifying hypothesis is M\(^\natural\)-convexity
of the expected loss in \(r\) (Murota), for which local-exchange optimality
characterizes global optimality and of which separable-convex-on-the-simplex
is the canonical special case. RPS transfer inequalities are linear in \(p\),
so its identified set would be a polytope. Status: **supported by computation
only; M\(^\natural\) claim is a proof strategy, not a result**.

## 5. Proof sketches

- **A(i).** Necessity/sufficiency from Lemma 1; the max–min step uses only
  (C) for the diagonal. One paragraph; no gaps identified.
- **A(ii).** Monotone inversion of \(A_v,B_v\); \(C\) is an interval because
  individual feasibility gives half-lines and
  \(\sum_v p_v^{(L)}(c)\le1\le\sum_v p_v^{(U)}(c)\) are an up- and a down-set
  in \(c\) by endpoint monotonicity; closedness from continuity.
- **A(iii).** \(\pi_i(\Sigma(c))\) is an interval with endpoints continuous in
  \(c\); the region between two continuous graphs over the interval \(C\) is
  connected; its projection is an interval; closed by compactness of
  \(P_S(r)\) (finitely many weak inequalities, each continuous in \(p\)).
- **A(iv).** On \(C\), slice maxima are \(\min(\text{noninc},\text{nondec})\);
  restricting to \(C\) removes the empty-slice overstatement issue that the
  existing Manhattan proof absorbs by a monotone-bound argument. Crossing or
  endpoint; bisection on a monotone reparameterization when \(C\) is
  unbounded (e.g. frequency-guessing at vertex reports, where
  \(\lambda\in[n,\infty)\)).
- **A(v).** Sup over a union is the sup of slice sups; greedy LP on a
  box–simplex slice; continuity of the greedy value in the endpoints.
- **C1, C2.** Explicit algebra recorded in Section 4; clamp checks included.
- **C4.** Two short lemmas: expectation preserves discrete convexity; strict
  stochastic monotonicity of \(\mathrm{Bin}(n,q)\) plus a non-constant
  monotone integrand gives strict monotonicity of the expectation.
- **R2.** Invariance: local-global failure is a statement about \(R_S\)
  itself, hence inherited by every representation satisfying (S).

## 6. Gaps

1. A(ii)/(iv) boundary write-up: unbounded \(C\) (reparameterize; attainment
   secured by compactness of \(P_S(r)\) and the witness argument — the
   maximizer \(p^*\) has a witness \(c^*\in C\cap C_0\) at which the slice
   maximum already equals \(\overline p_i\)). The appendix-grade write-up
   does not exist yet.
2. Uniqueness in A(iv) requires strict monotonicity of the relevant endpoint
   functions on the interior; the general statement guarantees only a
   constant-value solution interval (on a flat root interval both branches of
   the min are constant, so the bound value is unique).
3. \(P_S(r)\ne\emptyset\) is a substantive hypothesis: it genuinely fails for
   some C4-class rules (see the explicit \(\psi_1=2d+|d|\),
   \(\psi_2=\varepsilon|d|\) example in C4). For the three headline rules
   \(r/n\in P_S(r)\) always.
4. R2 is proven only for order-preserving representations; the argmin-level
   exclusion is open (see R2).
5. R3 and R4 are not results (conjecture / computational support only).
6. Novelty risk: the threshold \(c\) is the Lagrange multiplier of the
   resource constraint, and inverting allocations at a common multiplier may
   exist in the **inverse optimization** literature for separable resource
   allocation (e.g. Ahuja–Orlin-style inverse problems). A literature check is
   REQUIRED before claiming Theorem A as novel (Section 9/10).
7. A(v): the outer one-dimensional problem in \(c\) is continuous but not
   shown unimodal; it must be treated as a global 1-d search (grid with
   stated tolerance), exactly as the paper already does for Manhattan mean
   bounds. Only the *coordinate* bounds get the bisection guarantee, via the
   monotone crossing equation.
8. Extended-real Lemma 1 (second audit): the shipped appendix proof of
   `lem:transfer` implicitly assumes finite coordinate costs. For
   frequency-guessing at boundary beliefs, \(\ell(t;0)=+\infty\) for
   \(t>0\) and \(\Delta\ell\) as a difference is \(\infty-\infty\); the
   repair is to define the marginals by continuous extension from \((0,1)\)
   (for FG, \(\Delta\ell(t;q)=\log(t+1)-\log q\to+\infty\) as \(q\to0\), no
   ambiguity) and to note that optimal reports are supported on
   \(\mathrm{supp}(p)\), so all comparisons the proof needs are
   well-defined. One paragraph; needed for the master write-up and, as a
   minor flag, for the manuscript's framing sentence that each headline
   rule "is an instance of Lemma 1" (Proposition 2's own appendix proof is
   product-form and unaffected).

## 7. Counterexample checks

- **\(n=1\) degeneracy.** Any two feasible reports differ by one transfer, so
  the single-transfer characterization holds for *any* separable loss; (C) is
  not necessary at fixed small \(n\). All converse statements must quantify
  over \(n\) (or "for some \(n,k\)").
- **Hamming \(k=2\) vs \(k\ge3\).** Inside the class at \(k=2\) (equals
  frequency-guessing), outside at \((n,k)=(3,5)\) by R2. Shows rule-level
  class membership is not decidable from one representation.
- **Empty-slice overstatement.** The existing Manhattan proof's \(\phi(c)\)
  can overstate the sliced maximum at infeasible \(c\); the overstatement is
  absorbed by monotonicity there, and removed here by restricting to \(C\).
  Not a counterexample, but a trap the master write-up must avoid.
- **Empty identified set.** \(P_S(r)=\emptyset\) occurs for genuine members
  of the C4 class (heterogeneous losses; see C4). Theorem A's nonemptiness
  hypothesis cannot be dropped.

## 8. Special cases

- \(k=2\): the threshold collapses; the bound interval is the set of \(p_1\)
  where \(r_1\) is a generalized median/quantile of \(\mathrm{Bin}(n,p_1)\)
  (Manhattan/pinball) or the linear interval (squared, frequency-guessing).
- Vertex reports \(r=n e_j\): only sender constraints for \(j\), only
  receiver constraints for the rest; \(C\) may be unbounded
  (frequency-guessing); bounds remain valid with the stated conventions
  (squared: \(\overline p_j=1\), matching \(m=1\) closed form).
- Coordinates with \(r_i=0\): lower bound \(0\); upper bound from the
  crossing equation (C1 reproduces \(m/(n(m+1))\)).

## 9. Analytical status summary

| Result | Status |
|---|---|
| A(i) threshold representation | proven in this derivation |
| A(ii) box slices, interval \(C\) | proven modulo boundary write-up |
| A(iii) interval projections | proven modulo boundary write-up |
| A(iv) scalar-equation bounds | proven modulo boundary write-up |
| A(v) linear-functional sweep | proven modulo continuity write-up |
| A(v) unimodality of \(V_a\) in \(c\) | open problem |
| C1 squared closed forms via \(c^*\) | proven (algebra + machine-precision check + independent audit re-derivation) |
| C2 frequency-guessing via \(\lambda^*\) | proven (algebra + machine-precision check + independent audit re-derivation) |
| C3 Manhattan specialization | proven |
| C4 convex location family (incl. pinball) | proven (Abel-summation strictness); computation-corroborated |
| C4 nonemptiness of \(P_S(r)\) | can fail in the class (explicit example); holds for headline rules |
| R1 representation-level converse | classical (cited), caveat added |
| R2 order-preserving Hamming exclusion | proven (instance re-verified numerically) |
| R2 argmin-level Hamming exclusion | open |
| R3 location-loss converse | plausible conjecture, unresolved |
| R4 M\(^\natural\)/RPS direction | supported by computation only |
| Prop 3′ correction (open simplex) | proven on interior; boundary failure exhibited (second audit) |
| Novelty vs inverse-optimization literature | UNCHECKED — required before adoption |

**Manuscript flag (independent of adoption).** Section 3's sentence calling
the ranked probability score one of the "other separable count losses ...
governed by [the lemma] in the same way" is imprecise: RPS is separable in
*cumulative* counts, not in the per-category counts Lemma 1 quantifies over,
so the lemma does not literally apply. (`rule_candidate_screen.md` states
this correctly — "Gate A ✓ (separable in cumulative coordinates)" — and
`feasibility_frontier.md` §4 lists RPS without the cumulative caveat; the
imprecision entered between the screen and the manuscript.) Check 3 supports
the sentence's *conclusion* computationally, but the mechanism wording
should be revised (or the claim derived properly via R4) regardless of
whether Theorem A is adopted. A second prior-memo flag: `feasibility_frontier.md`
Prop 3′ is incorrect as stated (see the correction under R2).

## 10. Audit log and remaining audit task

**First audit (2026-06-10, theory-auditor).** Outcome, after independent
verification of every finding in the main session:
- *Accepted (verified independently):* the R2 order-vs-argmin gap (real;
  R2 weakened accordingly above); the \(P_S(r)=\emptyset\) example in the C4
  class (marginal computations re-derived; added to C4); the Abel-summation
  strictness identity (verified; adopted in C4); the honest-range \(C_0\)
  device (adopted in Section 2); the "crossings automatically yield nonempty
  slices" fact (verified; added to A(iv)); independent confirmation of the
  C1/C2 algebra and the Hamming instance numerics; standing caveats
  (\(n\ge1\), \(k\ge2\), extended-real marginals; adopted).
- *Rejected (checked against the repository):* the audit cited a filename
  that does not exist, quoted memo passages that are not in this memo,
  attributed empty-set conventions (\(\inf\emptyset=1\)) this memo does not
  use (it uses \(\pm\infty\), under which the auditor's "spurious slice"
  counterexample does not arise), and criticized a "residual redistribution"
  construction that appears nowhere in the shipped appendix proof of
  `lem:manhattan-unimodal` (grep-verified). Those findings were discarded.
  Likely source of the unplaceable material: conflation with the prior
  memos `feasibility_frontier.md` / `bounds_search_manhattan_hamming.md`,
  whose "Theorem 3 ⟸" write-up obligations (explicit unit-bijection,
  sender-side bound) resemble the criticized construction. Because of this
  mix, a SECOND independent audit of the corrected memo is required before
  any promotion.

**Second audit (2026-06-10, theory-auditor, evidence-rules protocol: all
materials pasted inline; every finding required to quote exact text).**
Overall verdict: **promote after fixes — no structural rework**. All
findings were re-verified in the main session before incorporation:
- *T7 (error, accepted and fixed):* the Prop 3′ correction's "for every
  \((p_1,p_2)\)" failed at degenerate beliefs (verified: \(n=2\), \(p_1=0\),
  \(g=(0,2,2)\), \(r=(2,0)\) weakly single-transfer optimal but not global);
  restricted to the open simplex above.
- *T1 (gap, accepted):* extended-real Lemma 1 paragraph needed for
  frequency-guessing at boundary beliefs — added as Gap 8.
- *T2/T3 (refinements, accepted):* \(C_0\) qualifiers for box nonemptiness
  at boundary coordinates and in the auxiliary fact; endpoint-branch
  restatement for unbounded \(C\) (witness/compactness attainment).
- *T4/T5/T6/T8 (wording, accepted):* C2 vertex-coordinate convention note;
  pinball quantile gloss qualified by the multiplier shift; "monotone"
  → "strictly increasing" in R2; "generalizes verbatim" corrected — the
  binomial crossing-existence step is replaced, not inherited.
- *Confirmed sound:* A(i)–(v) structure, C1/C2 algebra (independently
  re-derived, all values matching Propositions 1–2), C4 Abel argument and
  emptiness example, headline nonemptiness, R2 logic and numerics, the
  argmin-orbit openness argument.
- *Discarded as environment artifacts:* "memo file absent from repository"
  and "possible appendix corruption" — the files exist and are intact
  (read directly in the main session); the auditor evidently cannot see
  the working tree, which also explains the first audit's confabulations.

**Remaining gates before promotion** (audit gate now PASSED):
1. ~~`literature-reviewer` task: inverse optimization for separable resource
   allocation~~ — **WAIVED by author decision (2026-06-10)**: novelty of the
   threshold-inversion characterization is ASSUMED, not checked.
   Consequences: (a) any manuscript statement of Theorem A must carry
   "to our knowledge" hedging; (b) the check must still run before
   submission (CLAUDE.md guardrail: literature check precedes manuscript
   claims); (c) mitigating fact: the paper-specific novelty surface —
   inverting scoring-rule reports into *belief* identified sets — was
   already checked 2026-05-22 (`feasibility_frontier.md` §0: "The
   literature check found no prior work inverting scoring-rule reports
   into belief identified sets"); only the abstract inverse-optimization
   analogue remains unchecked.
2. Author placement decision: **TAKEN 2026-06-10 — LIGHT integration**,
   with Full held in reserve for the revision stage (rationale and the
   Light execution plan L1–L5 in `_context/next_steps.md`). Under Light,
   only Theorem A(i) (the threshold representation, elementary given
   Lemma 1) enters the manuscript, as a remark; parts (ii)–(v), the
   corollaries, and R2's full statement stay in this memo as the reserve
   Full option.
3. At write-up time (reserve Full option only): the appendix-grade
   boundary write-up (Gaps 1, 8), preceded by the waived
   inverse-optimization literature check — which, under Light, no longer
   gates submission, only the Full upgrade. BOTH the Full upgrade and the
   literature check require new, explicit author instruction; no agent
   session may initiate either. The approved Light execution is strictly
   offline — no literature search, web access, or downloading (binding
   constraints in `_context/next_steps.md`).

Manuscript options (decision taken 2026-06-10, recorded above and in
`_context/next_steps.md`):
- **Light — CHOSEN**: add the threshold representation as a remark to
  Lemma 1, reword the RPS sentence, add the extended-real convention line,
  and sharpen the Hamming demotion with the order-preserving exclusion.
  Execution plan L1–L5 in `_context/next_steps.md`; not yet executed.
- **Full — RESERVE (revision stage)**: restate Lemma 1 → master theorem in
  §3 with Propositions 1–3 as corollaries (C1–C3), and mention the
  pinball/quantile family (C4) as the wider-family example. Precondition:
  the inverse-optimization literature check. Deploy if referees ask for
  the general theorem or the venue target shifts to a methods outlet.
