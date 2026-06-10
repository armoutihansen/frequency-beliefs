"""Exploration checks for the master-threshold-theorem memo.

Companion to _context/exploration/master_threshold_theorem.md. NOT part of the
paper's verification suite; finite checks here are evidence, not proof.

Checks:
  1. For the three headline rules plus an asymmetric-absolute (pinball) rule,
     the generalized threshold/crossing-equation coordinate bounds agree with
     (a) the paper's closed forms where they exist (squared, freq-guessing) and
     (b) brute-force grid bounds over the simplex (k=3).
  2. Membership: brute-force optimality == single-transfer == threshold form
     (Lemma 1 / Stage 1), including for the pinball rule.
  3. Ranked probability score (RPS): is single-transfer optimality (over all
     coordinate pairs) sufficient for global optimality? (Tests the Section 3
     remark that RPS belongs to the tractable family.)

Run: uv run python scripts/explore_master_threshold.py
"""

import itertools
import math
import random
from math import inf, lgamma, log

from scipy.stats import binom

N, K = 5, 3
REPORTS = [r for r in itertools.product(range(N + 1), repeat=K) if sum(r) == N]
TAU = 0.3  # pinball asymmetry

# ---------------------------------------------------------------- rules ----
# Each rule: ell(t, q) = expected per-coordinate cost (up to a constant in q),
#            dl(t, q)  = forward difference ell(t+1, q) - ell(t, q).


def _pmf(q):
    return [binom.pmf(w, N, q) for w in range(N + 1)]


def _cdf(t, q):
    if t < 0:
        return 0.0
    if t >= N:
        return 1.0
    return float(binom.cdf(t, N, q))


def ell_sq(t, q):
    return (t - N * q) ** 2


def dl_sq(t, q):
    return 2 * t + 1 - 2 * N * q


def ell_fg(t, q):
    if q <= 0:
        return 0.0 if t == 0 else inf
    return lgamma(t + 1) - t * log(q)


def dl_fg(t, q):
    if q <= 0:
        return inf
    return log(t + 1) - log(q)


def ell_man(t, q):
    return sum(pw * abs(t - w) for w, pw in enumerate(_pmf(q)))


def dl_man(t, q):
    return 2 * _cdf(t, q) - 1


def _psi_pin(x):
    return TAU * x if x >= 0 else (TAU - 1) * x


def ell_pin(t, q):
    return sum(pw * _psi_pin(t - w) for w, pw in enumerate(_pmf(q)))


def dl_pin(t, q):
    # E[psi(t+1-W) - psi(t-W)] = tau*F(t) + (tau-1)*(1-F(t)) = F(t) - (1-tau)
    return _cdf(t, q) - (1 - TAU)


RULES = {
    "squared": (ell_sq, dl_sq),
    "freq-guess": (ell_fg, dl_fg),
    "manhattan": (ell_man, dl_man),
    "pinball": (ell_pin, dl_pin),
}

QEPS = 1e-12  # stand-in for q = 0 where dl blows up (freq-guessing)


# ------------------------------------------- threshold-endpoint inverses ----
def p_lower(dl, rv, c):
    """Smallest q in [0,1] with B(q) = dl(rv-1, q) <= c; None if infeasible."""
    if rv == 0:
        return 0.0
    B = lambda q: dl(rv - 1, q)
    if B(1.0) > c:
        return None
    if B(QEPS) <= c:
        return 0.0
    lo, hi = QEPS, 1.0  # B decreasing: B(lo) > c >= B(hi)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if B(mid) > c:
            lo = mid
        else:
            hi = mid
    return hi


def p_upper(dl, rv, c):
    """Largest q in [0,1] with A(q) = dl(rv, q) >= c; None if infeasible."""
    if rv == N:
        return 1.0
    A = lambda q: dl(rv, q)
    if A(QEPS) < c:
        return None
    if A(1.0) >= c:
        return 1.0
    lo, hi = QEPS, 1.0  # A decreasing: A(lo) >= c > A(hi)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if A(mid) >= c:
            lo = mid
        else:
            hi = mid
    return lo


def crossing_bound(dl, r, i, which):
    """Sharp coordinate bound via the generalized crossing equation.

    which='upper': solve p_i^U(c) + sum_{v!=i} p_v^L(c) = 1, return p_i^U(c*).
    which='lower': solve p_i^L(c) + sum_{v!=i} p_v^U(c) = 1, return p_i^L(c*).
    Infeasible endpoints are encoded to keep the LHS monotone in c.
    """

    def lhs(c):
        if which == "upper":
            own = p_upper(dl, r[i], c)
            tot = own if own is not None else 0.0
            for v in range(K):
                if v == i:
                    continue
                pl = p_lower(dl, r[v], c)
                tot += pl if pl is not None else 1.0
        else:
            own = p_lower(dl, r[i], c)
            tot = own if own is not None else 1.0
            for v in range(K):
                if v == i:
                    continue
                pu = p_upper(dl, r[v], c)
                tot += pu if pu is not None else 0.0
        return tot

    # bracket: marginal costs at q=1 (low end) and q~0 (high end), all coords
    cands = []
    for v in range(K):
        for t in (r[v] - 1, r[v]):
            if 0 <= t <= N - 1:
                cands += [dl(t, 1.0), min(dl(t, QEPS), 1e6)]
    c_lo, c_hi = min(cands) - 1.0, max(cands) + 1.0
    # LHS is nonincreasing in c; find LHS(c) = 1
    if lhs(c_lo) < 1.0 - 1e-9:  # no crossing: bound at low-threshold end
        c_star = c_lo
    elif lhs(c_hi) > 1.0 + 1e-9:  # no crossing: bound at high-threshold end
        c_star = c_hi
    else:
        lo, hi = c_lo, c_hi
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if lhs(mid) >= 1.0:
                lo = mid
            else:
                hi = mid
        c_star = lo
    p = p_upper(dl, r[i], c_star) if which == "upper" else p_lower(dl, r[i], c_star)
    return p if p is not None else (1.0 if which == "upper" else 0.0)


# ------------------------------------------------------------ closed forms --
def closed_sq(r, i):
    m = sum(1 for x in r if x > 0)
    if r[i] == 0:
        return 0.0, m / (N * (m + 1))
    return (r[i] - 1) / N + 1 / (N * K), (r[i] + 1) / N - 1 / (N * m)


def closed_fg(r, i):
    return r[i] / (N + K - 1), (r[i] + 1) / (N + 1)


# ------------------------------------------------------ brute-force tools ---
def brute_region_bounds(ell, dl, h=0.005, subsample=7):
    """Grid the simplex (k=3); per report, min/max of each coordinate over the
    brute-force identified set. Also cross-checks membership: brute == single-
    transfer == threshold(max-min) on a subsample."""
    qgrid = [j * h for j in range(int(round(1 / h)) + 1)]
    tables = {q: [ell(t, q) for t in range(N + 1)] for q in qgrid}
    dtab = {q: [dl(t, q) for t in range(N)] for q in qgrid}
    lo = {r: [1.0] * K for r in REPORTS}
    hi = {r: [0.0] * K for r in REPORTS}
    mismatches, idx = 0, 0
    for a in qgrid:
        for b in qgrid:
            c3 = 1 - a - b
            if c3 < -1e-12:
                continue
            c3 = max(c3, 0.0)
            c3 = min((round(c3 / h)) * h, 1.0)  # snap to table key
            p = (a, b, c3)
            vals = {r: sum(tables[p[v]][r[v]] for v in range(K)) for r in REPORTS}
            best = min(vals.values())
            idx += 1
            for r in REPORTS:
                if vals[r] <= best + 1e-9:
                    for v in range(K):
                        lo[r][v] = min(lo[r][v], p[v])
                        hi[r][v] = max(hi[r][v], p[v])
                    member = True
                else:
                    member = False
                if idx % subsample == 0:
                    # single-transfer test via max-min threshold form
                    A = [dtab[p[v]][r[v]] for v in range(K) if r[v] < N]
                    B = [dtab[p[v]][r[v] - 1] for v in range(K) if r[v] > 0]
                    st = (min(A) if A else inf) >= (max(B) if B else -inf) - 1e-9
                    if st != member:
                        mismatches += 1
    return lo, hi, mismatches


# ------------------------------------------------------------- RPS check ----
def rps_check(trials=500, seed=11):
    rng = random.Random(seed)
    worst = 0.0
    fails = 0
    for n, k in [(3, 3), (4, 3), (5, 3), (4, 4), (6, 4)]:
        reps = [r for r in itertools.product(range(n + 1), repeat=k) if sum(r) == n]
        for _ in range(trials):
            cuts = sorted(rng.random() for _ in range(k - 1))
            p = [b - a for a, b in zip([0.0] + cuts, cuts + [1.0])]
            P = [sum(p[: j + 1]) for j in range(k - 1)]

            def f(r):
                R = list(itertools.accumulate(r))[:-1]
                return sum((R[j] - n * P[j]) ** 2 for j in range(k - 1))

            vals = {r: f(r) for r in reps}
            best = min(vals.values())
            for r in reps:
                ok = all(
                    vals[r] <= f(tuple(r[v] + (v == i) - (v == j) for v in range(k))) + 1e-9
                    for i in range(k)
                    for j in range(k)
                    if i != j and r[j] > 0
                )
                if ok and vals[r] > best + 1e-9:
                    fails += 1
                    worst = max(worst, vals[r] - best)
    return fails, worst


# ------------------------------------------------------------------- main ---
if __name__ == "__main__":
    print(f"n={N}, k={K}, reports={len(REPORTS)}\n")

    print("== Check 1a: crossing-equation bounds vs closed forms ==")
    for name, closed in [("squared", closed_sq), ("freq-guess", closed_fg)]:
        ell, dl = RULES[name]
        err = 0.0
        for r in REPORTS:
            for i in range(K):
                clo, chi = closed(r, i)
                blo = crossing_bound(dl, r, i, "lower")
                bhi = crossing_bound(dl, r, i, "upper")
                err = max(err, abs(blo - clo), abs(bhi - chi))
        print(f"  {name:11s} max |crossing - closed| = {err:.2e}")

    print("\n== Check 1b/2: crossing bounds vs grid brute force; membership ==")
    for name in RULES:
        ell, dl = RULES[name]
        lo, hi, mism = brute_region_bounds(ell, dl)
        gap = 0.0
        bad_sharp = 0
        for r in REPORTS:
            if hi[r][0] < lo[r][0]:
                continue  # report never optimal on grid (none expected)
            for i in range(K):
                blo = crossing_bound(dl, r, i, "lower")
                bhi = crossing_bound(dl, r, i, "upper")
                # validity: crossing interval must cover all grid members
                if lo[r][i] < blo - 1e-6 or hi[r][i] > bhi + 1e-6:
                    bad_sharp += 1
                # sharpness: grid members should approach the crossing bounds
                gap = max(gap, lo[r][i] - blo, bhi - hi[r][i])
        print(
            f"  {name:11s} membership mismatches={mism}, "
            f"validity violations={bad_sharp}, max grid gap={gap:.4f}"
        )

    print("\n== Check 3: RPS single-transfer sufficiency (all pairs) ==")
    fails, worst = rps_check()
    print(f"  single-transfer-optimal but not global: {fails} cases (worst gap {worst:.3g})")
