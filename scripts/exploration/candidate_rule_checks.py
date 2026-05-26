"""Finite enumeration checks for candidate-rule screening (exploration mode).

Corroborates the Stage-1 analytical screen for additional frequency-report
scoring rules. NOT a proof — finite checks over small (n,k) and random
Dirichlet beliefs. See _context/exploration/rule_candidate_screen.md.

For each rule D(r,omega) we check, on small grids:
  * GATE B  -- is single-count-transfer optimality SUFFICIENT?  i.e. does the
    set of single-transfer-local optima equal the set of global optima?
  * GATE C  -- are the pairwise optimal-report inequalities affine in p?
    checked by sampling L(r;p)-L(s;p) and testing linearity in p.

Run:  uv run python scripts/candidate_rule_checks.py
"""

from __future__ import annotations

import itertools
import math
import random
import sys
from pathlib import Path

# Allow `from config import ...` when run as `python scripts/exploration/<name>.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import SEED_CANDIDATE_RULES

random.seed(SEED_CANDIDATE_RULES)


# ---------------------------------------------------------------- combinatorics
def compositions(n: int, k: int):
    """All nonnegative integer k-vectors summing to n."""
    if k == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in compositions(n - first, k - 1):
            yield (first,) + rest


def multinomial_pmf(omega, p):
    n = sum(omega)
    logc = math.lgamma(n + 1) - sum(math.lgamma(o + 1) for o in omega)
    s = logc
    for o, pi in zip(omega, p):
        if o > 0:
            if pi <= 0.0:
                return 0.0
            s += o * math.log(pi)
    return math.exp(s)


def dirichlet(k):
    g = [random.gammavariate(1.0, 1.0) for _ in range(k)]
    t = sum(g)
    return tuple(x / t for x in g)


# ----------------------------------------------------------------------- losses
def d_squared(r, omega):
    return sum((ri - oi) ** 2 for ri, oi in zip(r, omega))


def d_kl(r, omega):
    """KL count loss in the (realization || report) order: sum omega_i log(omega_i/r_i)."""
    tot = 0.0
    for ri, oi in zip(r, omega):
        if oi == 0:
            continue
        if ri == 0:
            return math.inf
        tot += oi * math.log(oi / ri)
    return tot


def d_chisq(r, omega):
    """Chi-squared count loss, /r_i variant. Undefined at r_i=0."""
    tot = 0.0
    for ri, oi in zip(r, omega):
        if ri == 0:
            return math.inf
        tot += (ri - oi) ** 2 / ri
    return tot


def d_rps(r, omega):
    """Ranked probability score: squared distance on cumulative counts."""
    cr = list(itertools.accumulate(r))
    co = list(itertools.accumulate(omega))
    return sum((a - b) ** 2 for a, b in zip(cr[:-1], co[:-1]))


def _pinball(u, tau):
    return u * tau if u >= 0 else u * (tau - 1.0)


def d_pinball(r, omega, tau=0.3):
    """Asymmetric-L1 (pinball) count loss; elicits the tau-quantile."""
    return sum(_pinball(ri - oi, tau) for ri, oi in zip(r, omega))


def d_hellinger(r, omega):
    """Hellinger count loss: sum (sqrt(r_i) - sqrt(omega_i))^2."""
    return sum((math.sqrt(ri) - math.sqrt(oi)) ** 2 for ri, oi in zip(r, omega))


# ----------------------------------------------------------------- expected loss
def expected_loss(r, p, dfunc, omegas):
    tot = 0.0
    for omega in omegas:
        w = multinomial_pmf(omega, p)
        if w == 0.0:
            continue
        d = dfunc(r, omega)
        if d == math.inf:
            return math.inf
        tot += w * d
    return tot


# -------------------------------------------------------------------- gate B
def gate_b_check(n, k, dfunc, n_beliefs=200, tol=1e-9, positive_reports_only=False):
    """Does single-transfer-local optimality == global optimality?"""
    reports = list(compositions(n, k))
    omegas = reports
    if positive_reports_only:
        reports = [r for r in reports if all(ri > 0 for ri in r)]
    mismatches = 0
    for _ in range(n_beliefs):
        p = dirichlet(k)
        loss = {r: expected_loss(r, p, dfunc, omegas) for r in reports}
        best = min(loss.values())
        global_opt = {r for r, v in loss.items() if v <= best + tol}
        for r in reports:
            if loss[r] == math.inf:
                continue
            improving_transfer = False
            for i in range(k):
                for j in range(k):
                    if i == j or r[j] == 0:
                        continue
                    s = list(r)
                    s[i] += 1
                    s[j] -= 1
                    s = tuple(s)
                    if positive_reports_only and any(si == 0 for si in s):
                        continue
                    if loss.get(s, math.inf) < loss[r] - tol:
                        improving_transfer = True
            is_local = not improving_transfer
            is_global = r in global_opt
            if is_local and not is_global:
                mismatches += 1
    return mismatches


# -------------------------------------------------------------------- gate C
def gate_c_linear(n, k, dfunc, n_triples=300, tol=1e-6):
    """Is r |-> [L(r;p) - L(s;p)] affine in p?  Tested via collinear triples:
    for p2 = (p1+p3)/2, an affine function satisfies f(p2) = (f(p1)+f(p3))/2."""
    reports = [r for r in compositions(n, k) if all(ri > 0 for ri in r)] or list(
        compositions(n, k)
    )
    omegas = list(compositions(n, k))
    worst = 0.0
    for _ in range(n_triples):
        p1, p3 = dirichlet(k), dirichlet(k)
        p2 = tuple((a + b) / 2 for a, b in zip(p1, p3))
        r, s = random.sample(reports, 2)

        def diff(p):
            lr = expected_loss(r, p, dfunc, omegas)
            ls = expected_loss(s, p, dfunc, omegas)
            return lr - ls

        f1, f2, f3 = diff(p1), diff(p2), diff(p3)
        if any(math.isinf(x) for x in (f1, f2, f3)):
            continue
        gap = abs(f2 - 0.5 * (f1 + f3))
        worst = max(worst, gap)
    return worst


# ----------------------------------------------------------------------- driver
def main():
    print("=" * 72)
    print("Candidate-rule screening checks (exploration mode; finite checks)")
    print("=" * 72)

    rules = [
        ("squared-distance (control: feasible)", d_squared, False),
        ("KL divergence (omega||r order)", d_kl, True),
        ("chi-squared (/r_i)", d_chisq, True),
        ("RPS (squared on cumulative counts)", d_rps, False),
        ("pinball / asymmetric-L1 (tau=0.3)", d_pinball, False),
        ("Hellinger", d_hellinger, False),
    ]

    print("\n-- GATE B: single-transfer-local optimum == global optimum? --")
    print("   (mismatches > 0  =>  single-transfer NOT sufficient => Hamming-class)")
    for name, dfunc, pos in rules:
        for (n, k) in [(4, 3), (5, 3), (6, 3), (5, 4), (6, 4)]:
            m = gate_b_check(n, k, dfunc, n_beliefs=150, positive_reports_only=pos)
            flag = "OK" if m == 0 else f"FAIL ({m} mismatches)"
            print(f"   {name:42s} n={n} k={k}: {flag}")

    print("\n-- GATE C: are optimal-report inequalities affine in p? --")
    print("   (worst collinear-triple gap; ~0 => affine => polytope identified set)")
    for name, dfunc, _pos in rules:
        worst = gate_c_linear(5, 3, dfunc)
        verdict = "AFFINE (polytope)" if worst < 1e-6 else f"NON-AFFINE (gap {worst:.2e})"
        print(f"   {name:42s}: {verdict}")

    print("\n-- KL loss formula check: L(r;p) == const - sum_i n p_i log r_i ? --")
    omegas = list(compositions(6, 3))
    reports = [r for r in omegas if all(ri > 0 for ri in r)]
    p = dirichlet(3)
    n = 6
    direct = {r: expected_loss(r, p, d_kl, omegas) for r in reports}
    predicted = {r: -sum(n * pi * math.log(ri) for ri, pi in zip(r, p)) for r in reports}
    # both should rank reports identically and differ by an r-independent constant
    consts = [direct[r] - predicted[r] for r in reports]
    spread = max(consts) - min(consts)
    print(f"   const spread across reports: {spread:.2e}  (->0 confirms the formula)")


if __name__ == "__main__":
    main()
