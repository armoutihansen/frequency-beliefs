"""Computational checks for frequency-report belief regions.

This script is intentionally small-scale. It verifies finite-sample
characterizations by enumeration for small n,k and produces worked examples.

Run from the repository root:

    uv run python scripts/verify_regions.py --write-notes
"""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
from scipy.optimize import brentq, linprog
from scipy.stats import binom


TOL = 1e-9


def feasible_reports(n: int, k: int) -> list[tuple[int, ...]]:
    if k == 1:
        return [(n,)]
    reports: list[tuple[int, ...]] = []
    for x in range(n + 1):
        for tail in feasible_reports(n - x, k - 1):
            reports.append((x,) + tail)
    return reports


def simplex_grid(k: int, denom: int) -> list[np.ndarray]:
    return [np.array(r, dtype=float) / denom for r in feasible_reports(denom, k)]


def multinomial_pmf(w: tuple[int, ...], p: np.ndarray) -> float:
    n = sum(w)
    coeff = math.factorial(n)
    out = float(coeff)
    for wi, pi in zip(w, p):
        out /= math.factorial(wi)
        if wi > 0:
            out *= float(pi) ** wi
    return out


def score_exact(r: tuple[int, ...], w: tuple[int, ...], a: float = 0.0, b: float = 1.0) -> float:
    return a + b * float(r == w)


def score_squared(r: tuple[int, ...], w: tuple[int, ...], a: float = 0.0) -> float:
    return a - sum((ri - wi) ** 2 for ri, wi in zip(r, w))


def score_l1(r: tuple[int, ...], w: tuple[int, ...], a: float = 0.0) -> float:
    return a - sum(abs(ri - wi) for ri, wi in zip(r, w))


def score_linf(r: tuple[int, ...], w: tuple[int, ...], a: float = 0.0) -> float:
    return a - max(abs(ri - wi) for ri, wi in zip(r, w))


def score_hamming(r: tuple[int, ...], w: tuple[int, ...], a: float = 0.0) -> float:
    return a - sum(ri != wi for ri, wi in zip(r, w))


def expected_score(
    rule: str, r: tuple[int, ...], p: np.ndarray, omega: list[tuple[int, ...]], a: float = 0.0
) -> float:
    if rule == "exact":
        fn = lambda rr, ww: score_exact(rr, ww, a=a, b=1.0)
    elif rule == "squared":
        fn = lambda rr, ww: score_squared(rr, ww, a=a)
    elif rule == "l1":
        fn = lambda rr, ww: score_l1(rr, ww, a=a)
    elif rule == "linf":
        fn = lambda rr, ww: score_linf(rr, ww, a=a)
    elif rule == "hamming":
        fn = lambda rr, ww: score_hamming(rr, ww, a=a)
    else:
        raise ValueError(rule)
    return sum(multinomial_pmf(w, p) * fn(r, w) for w in omega)


def argmax_reports(scores: dict[tuple[int, ...], float], tol: float = TOL) -> set[tuple[int, ...]]:
    m = max(scores.values())
    return {r for r, v in scores.items() if abs(v - m) <= tol}


def argmin_reports(vals: dict[tuple[int, ...], float], tol: float = TOL) -> set[tuple[int, ...]]:
    m = min(vals.values())
    return {r for r, v in vals.items() if abs(v - m) <= tol}


def direct_optima(rule: str, p: np.ndarray, n: int, k: int, a: float = 0.0) -> set[tuple[int, ...]]:
    reports = feasible_reports(n, k)
    scores = {r: expected_score(rule, r, p, reports, a=a) for r in reports}
    return argmax_reports(scores)


def exact_modes(p: np.ndarray, n: int, k: int) -> set[tuple[int, ...]]:
    reports = feasible_reports(n, k)
    pmfs = {r: multinomial_pmf(r, p) for r in reports}
    return argmax_reports(pmfs)


def exact_transfer_region(r: tuple[int, ...], p: np.ndarray, tol: float = 1e-10) -> bool:
    # Boundary support condition.
    for ri, pi in zip(r, p):
        if pi <= tol and ri > 0:
            return False
    for j, rj in enumerate(r):
        if rj == 0:
            continue
        for i, ri in enumerate(r):
            if p[i] * rj > p[j] * (ri + 1) + tol:
                return False
    return True


def exact_coordinate_intervals(r: tuple[int, ...], n: int, k: int) -> list[tuple[float, float]]:
    return [(ri / (n + k - 1), (ri + 1) / (n + 1)) for ri in r]


def endpoint_vectors_exact(r: tuple[int, ...], n: int, k: int, i: int) -> tuple[np.ndarray, np.ndarray]:
    upper = np.array([rj / (n + 1) for rj in r], dtype=float)
    upper[i] = (r[i] + 1) / (n + 1)
    if r[i] == 0:
        lower = np.array(r, dtype=float)
        denom = sum(lower)
        if denom > 0:
            lower /= denom
        lower[i] = 0.0
    else:
        lower = np.array([(rj + 1) / (n + k - 1) for rj in r], dtype=float)
        lower[i] = r[i] / (n + k - 1)
    return lower, upper


def squared_projection_optima(p: np.ndarray, n: int, k: int) -> set[tuple[int, ...]]:
    x = n * p
    vals = {r: float(np.sum((np.array(r) - x) ** 2)) for r in feasible_reports(n, k)}
    return argmin_reports(vals)


def squared_halfspace_region(r: tuple[int, ...], p: np.ndarray, n: int, k: int, tol: float = 1e-10) -> bool:
    rr = np.array(r, dtype=float)
    for s in feasible_reports(n, k):
        ss = np.array(s, dtype=float)
        lhs = 2 * n * float(np.dot(p, ss - rr))
        rhs = float(np.dot(ss, ss) - np.dot(rr, rr))
        if lhs > rhs + tol:
            return False
    return True


def squared_transfer_region(r: tuple[int, ...], p: np.ndarray, n: int, tol: float = 1e-10) -> bool:
    for j, rj in enumerate(r):
        if rj == 0:
            continue
        for i, ri in enumerate(r):
            if n * (p[i] - p[j]) > ri - rj + 1 + tol:
                return False
    return True


def squared_lp_bounds(
    r: tuple[int, ...], n: int, k: int, objective: np.ndarray | None = None
) -> tuple[list[tuple[float, float]], tuple[float, float] | None]:
    reports = feasible_reports(n, k)
    rr = np.array(r, dtype=float)
    a_ub = []
    b_ub = []
    for s in reports:
        ss = np.array(s, dtype=float)
        a_ub.append(2 * n * (ss - rr))
        b_ub.append(float(np.dot(ss, ss) - np.dot(rr, rr)))
    a_eq = [np.ones(k)]
    b_eq = [1.0]
    bounds = [(0.0, 1.0)] * k

    def solve(c: np.ndarray) -> float:
        res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
        if not res.success:
            raise RuntimeError(res.message)
        return float(res.fun)

    coord_bounds = []
    for i in range(k):
        c = np.zeros(k)
        c[i] = 1.0
        lo = solve(c)
        hi = -solve(-c)
        coord_bounds.append((clean(lo), clean(hi)))

    obj_bounds = None
    if objective is not None:
        lo = solve(objective)
        hi = -solve(-objective)
        obj_bounds = (clean(lo), clean(hi))
    return coord_bounds, obj_bounds


def squared_closed_form_bounds(r: tuple[int, ...], n: int, k: int) -> list[tuple[float, float]]:
    """Closed-form coordinate bounds for the squared-distance region.

    Let m be the number of positive reported coordinates. These formulas are
    derived from the one-count transfer inequalities and are checked against
    the LP implementation below.
    """
    m = sum(1 for ri in r if ri > 0)
    out = []
    for ri in r:
        if ri == 0:
            out.append((0.0, clean(m / (n * (m + 1)))))
        else:
            lo = (ri - 1) / n + 1 / (n * k)
            hi = (ri + 1) / n - 1 / (n * m)
            out.append((clean(lo), clean(hi)))
    return out


def exact_lp_mean_bounds(r: tuple[int, ...], n: int, k: int, x: np.ndarray) -> tuple[float, float]:
    a_ub = []
    b_ub = []
    for j, rj in enumerate(r):
        if rj == 0:
            continue
        for i, ri in enumerate(r):
            row = np.zeros(k)
            row[i] = rj
            row[j] -= ri + 1
            a_ub.append(row)
            b_ub.append(0.0)
    a_eq = [np.ones(k)]
    b_eq = [1.0]
    bounds = [(0.0, 1.0)] * k

    def solve(c: np.ndarray) -> float:
        res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
        if not res.success:
            raise RuntimeError(res.message)
        return float(res.fun)

    return clean(solve(x)), clean(-solve(-x))


def binom_abs_loss(t: int, n: int, p: float) -> float:
    return sum(abs(t - w) * binom.pmf(w, n, p) for w in range(n + 1))


def l1_separable_objective(r: tuple[int, ...], p: np.ndarray, n: int) -> float:
    return sum(binom_abs_loss(ri, n, float(pi)) for ri, pi in zip(r, p))


def l1_separable_optima(p: np.ndarray, n: int, k: int) -> set[tuple[int, ...]]:
    vals = {r: l1_separable_objective(r, p, n) for r in feasible_reports(n, k)}
    return argmin_reports(vals)


def l1_delta(i: int, t: int, p: np.ndarray, n: int) -> float:
    return binom_abs_loss(t + 1, n, float(p[i])) - binom_abs_loss(t, n, float(p[i]))


def l1_exchange_region(r: tuple[int, ...], p: np.ndarray, n: int, tol: float = 1e-10) -> bool:
    for i, ri in enumerate(r):
        if ri >= n:
            continue
        fi = binom.cdf(ri, n, float(p[i]))
        for j, rj in enumerate(r):
            if rj <= 0:
                continue
            fj = binom.cdf(rj - 1, n, float(p[j]))
            if fi + tol < fj:
                return False
    return True


def l1_exchange_optima(p: np.ndarray, n: int, k: int) -> set[tuple[int, ...]]:
    return {r for r in feasible_reports(n, k) if l1_exchange_region(r, p, n)}


def binom_cdf_safe(t: int, n: int, p: float) -> float:
    if t < 0:
        return 0.0
    if t >= n:
        return 1.0
    return float(binom.cdf(t, n, p))


def binom_cdf_inverse_decreasing(t: int, n: int, c: float) -> float:
    """Return u with Pr(Bin(n,u)<=t)=c for t<n.

    The CDF is continuous and weakly decreasing from 1 at u=0 to 0 at u=1.
    """
    if c <= 0.0:
        return 1.0
    if c >= 1.0:
        return 0.0
    return float(brentq(lambda u: binom_cdf_safe(t, n, u) - c, 0.0, 1.0))


def l1_threshold_box(r: tuple[int, ...], n: int, c: float) -> tuple[np.ndarray, np.ndarray]:
    lo = []
    hi = []
    for ri in r:
        if ri == 0:
            lo.append(0.0)
        else:
            lo.append(binom_cdf_inverse_decreasing(ri - 1, n, c))
        if ri == n:
            hi.append(1.0)
        else:
            hi.append(binom_cdf_inverse_decreasing(ri, n, c))
    return np.array(lo), np.array(hi)


def l1_threshold_bounds(
    r: tuple[int, ...], n: int, k: int, c_denom: int = 2000, x: np.ndarray | None = None
) -> tuple[list[tuple[float, float]] | None, tuple[float, float] | None, int]:
    coord_los = np.full(k, np.inf)
    coord_his = np.full(k, -np.inf)
    mean_lo = np.inf
    mean_hi = -np.inf
    feasible_count = 0
    for c in np.linspace(0.0, 1.0, c_denom + 1):
        lo, hi = l1_threshold_box(r, n, float(c))
        if lo.sum() > 1.0 + 1e-10 or hi.sum() + 1e-10 < 1.0:
            continue
        feasible_count += 1
        for h in range(k):
            fixed_lo = max(float(lo[h]), 1.0 - float(np.sum(np.delete(hi, h))))
            fixed_hi = min(float(hi[h]), 1.0 - float(np.sum(np.delete(lo, h))))
            coord_los[h] = min(coord_los[h], fixed_lo)
            coord_his[h] = max(coord_his[h], fixed_hi)
        if x is not None:
            # Linear objective over a box-simplex. Greedy allocation is exact
            # for fixed c; this is only over a c-grid.
            residual = 1.0 - float(lo.sum())
            p_min = lo.copy()
            for idx in np.argsort(x):
                add = min(float(hi[idx] - lo[idx]), residual)
                p_min[idx] += add
                residual -= add
                if residual <= 1e-12:
                    break
            residual = 1.0 - float(lo.sum())
            p_max = lo.copy()
            for idx in np.argsort(-x):
                add = min(float(hi[idx] - lo[idx]), residual)
                p_max[idx] += add
                residual -= add
                if residual <= 1e-12:
                    break
            mean_lo = min(mean_lo, float(p_min @ x))
            mean_hi = max(mean_hi, float(p_max @ x))
    if feasible_count == 0:
        return None, None, 0
    coord = [(clean(float(coord_los[i])), clean(float(coord_his[i]))) for i in range(k)]
    mean = None
    if x is not None:
        mean = (clean(mean_lo), clean(mean_hi))
    return coord, mean, feasible_count


def l1_grid_bounds(
    r: tuple[int, ...], n: int, k: int, denom: int, x: np.ndarray | None = None
) -> tuple[list[tuple[float, float]] | None, tuple[float, float] | None, int]:
    pts = [p for p in simplex_grid(k, denom) if l1_exchange_region(r, p, n, tol=1e-12)]
    if not pts:
        return None, None, 0
    arr = np.vstack(pts)
    coord = [(clean(float(arr[:, i].min())), clean(float(arr[:, i].max()))) for i in range(k)]
    mean = None
    if x is not None:
        vals = arr @ x
        mean = (clean(float(vals.min())), clean(float(vals.max())))
    return coord, mean, len(pts)


def linf_loss(r: tuple[int, ...], w: tuple[int, ...]) -> int:
    return max(abs(ri - wi) for ri, wi in zip(r, w))


def linf_expected_loss(r: tuple[int, ...], p: np.ndarray, n: int, k: int) -> float:
    return sum(multinomial_pmf(w, p) * linf_loss(r, w) for w in feasible_reports(n, k))


def linf_expected_loss_tail_sum(r: tuple[int, ...], p: np.ndarray, n: int, k: int) -> float:
    total = 0.0
    for m in range(1, n + 1):
        total += sum(
            multinomial_pmf(w, p)
            for w in feasible_reports(n, k)
            if linf_loss(r, w) >= m
        )
    return total


def linf_optima(p: np.ndarray, n: int, k: int) -> set[tuple[int, ...]]:
    vals = {r: linf_expected_loss(r, p, n, k) for r in feasible_reports(n, k)}
    return argmin_reports(vals)


def linf_grid_bounds(
    r: tuple[int, ...], n: int, k: int, denom: int, x: np.ndarray | None = None
) -> tuple[list[tuple[float, float]] | None, tuple[float, float] | None, int]:
    pts = [p for p in simplex_grid(k, denom) if r in linf_optima(p, n, k)]
    if not pts:
        return None, None, 0
    arr = np.vstack(pts)
    coord = [(clean(float(arr[:, i].min())), clean(float(arr[:, i].max()))) for i in range(k)]
    mean = None
    if x is not None:
        vals = arr @ x
        mean = (clean(float(vals.min())), clean(float(vals.max())))
    return coord, mean, len(pts)


def linf_losses_for_report(n: int, k: int, r: tuple[int, ...], p: np.ndarray) -> dict[tuple[int, ...], float]:
    return {s: clean(linf_expected_loss(s, p, n, k)) for s in feasible_reports(n, k)}


def hamming_loss(r: tuple[int, ...], w: tuple[int, ...]) -> int:
    return sum(ri != wi for ri, wi in zip(r, w))


def hamming_expected_loss(r: tuple[int, ...], p: np.ndarray, n: int) -> float:
    # Linearity of expectation reduces the expected coordinate-mismatch loss
    # to binomial marginal exact-coordinate probabilities.
    return clean(sum(1.0 - float(binom.pmf(ri, n, float(pi))) for ri, pi in zip(r, p)))


def hamming_optima(p: np.ndarray, n: int, k: int) -> set[tuple[int, ...]]:
    vals = {r: hamming_expected_loss(r, p, n) for r in feasible_reports(n, k)}
    return argmin_reports(vals)


def hamming_grid_bounds(
    r: tuple[int, ...], n: int, k: int, denom: int, x: np.ndarray | None = None
) -> tuple[list[tuple[float, float]] | None, tuple[float, float] | None, int]:
    pts = [p for p in simplex_grid(k, denom) if r in hamming_optima(p, n, k)]
    if not pts:
        return None, None, 0
    arr = np.vstack(pts)
    coord = [(clean(float(arr[:, i].min())), clean(float(arr[:, i].max()))) for i in range(k)]
    mean = None
    if x is not None:
        vals = arr @ x
        mean = (clean(float(vals.min())), clean(float(vals.max())))
    return coord, mean, len(pts)


def squared_grid_bounds(
    r: tuple[int, ...], n: int, k: int, denom: int, x: np.ndarray | None = None
) -> tuple[list[tuple[float, float]] | None, tuple[float, float] | None, int]:
    pts = [p for p in simplex_grid(k, denom) if squared_transfer_region(r, p, n)]
    if not pts:
        return None, None, 0
    arr = np.vstack(pts)
    coord = [(clean(float(arr[:, i].min())), clean(float(arr[:, i].max()))) for i in range(k)]
    mean = None
    if x is not None:
        vals = arr @ x
        mean = (clean(float(vals.min())), clean(float(vals.max())))
    return coord, mean, len(pts)


def exact_grid_bounds(
    r: tuple[int, ...], k: int, denom: int, x: np.ndarray | None = None
) -> tuple[list[tuple[float, float]] | None, tuple[float, float] | None, int]:
    pts = [p for p in simplex_grid(k, denom) if exact_transfer_region(r, p)]
    if not pts:
        return None, None, 0
    arr = np.vstack(pts)
    coord = [(clean(float(arr[:, i].min())), clean(float(arr[:, i].max()))) for i in range(k)]
    mean = None
    if x is not None:
        vals = arr @ x
        mean = (clean(float(vals.min())), clean(float(vals.max())))
    return coord, mean, len(pts)


def polytope_linear_extremum(
    r: tuple[int, ...], n: int, k: int, rule: str, c: np.ndarray, maximize: bool = False
) -> float:
    """Solve max/min c.p over the identified set P_S(r) for the polytope rules.

    rule = "exact" uses frequency-guessing constraints r_j p_i <= (r_i+1) p_j for r_j>0;
    rule = "squared" uses 2n(s-r).p <= |s|^2-|r|^2 for all feasible s.
    """
    if rule == "exact":
        a_ub, b_ub = [], []
        for j, rj in enumerate(r):
            if rj == 0:
                continue
            for i, ri in enumerate(r):
                row = np.zeros(k)
                row[i] = rj
                row[j] -= ri + 1
                a_ub.append(row)
                b_ub.append(0.0)
    elif rule == "squared":
        reports = feasible_reports(n, k)
        rr = np.array(r, dtype=float)
        a_ub, b_ub = [], []
        for s in reports:
            ss = np.array(s, dtype=float)
            a_ub.append(2 * n * (ss - rr))
            b_ub.append(float(np.dot(ss, ss) - np.dot(rr, rr)))
    else:
        raise ValueError(f"unsupported rule: {rule}")
    a_eq = [np.ones(k)]
    b_eq = [1.0]
    bnds = [(0.0, 1.0)] * k
    obj = -c if maximize else c
    res = linprog(obj, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bnds, method="highs")
    if not res.success:
        raise RuntimeError(res.message)
    return -float(res.fun) if maximize else float(res.fun)


def polytope_cumsum_bounds(
    r: tuple[int, ...], n: int, k: int, rule: str
) -> list[tuple[float, float]]:
    """For each j=1..k, return (inf S_j, sup S_j) over the rule's identified set."""
    out = []
    for j in range(1, k + 1):
        c = np.zeros(k)
        c[:j] = 1.0
        lo = polytope_linear_extremum(r, n, k, rule, c, maximize=False)
        hi = polytope_linear_extremum(r, n, k, rule, c, maximize=True)
        out.append((clean(lo), clean(hi)))
    return out


def l1_cumsum_bounds(
    r: tuple[int, ...], n: int, k: int, c_denom: int = 2000
) -> list[tuple[float, float]]:
    """For each j=1..k, return (inf S_j, sup S_j) over the Manhattan identified set,
    computed via the threshold-indexed slice family (sharp up to grid tolerance in c).
    """
    inf_S = [np.inf] * k
    sup_S = [-np.inf] * k
    for c in np.linspace(0.0, 1.0, c_denom + 1):
        lo, hi = l1_threshold_box(r, n, float(c))
        if lo.sum() > 1.0 + 1e-10 or hi.sum() + 1e-10 < 1.0:
            continue
        # On the slice, cumulative sum S_j(p)=sum_{i<=j} p_i has
        #   inf = max(sum_{i<=j} lo_i,   1 - sum_{i>j} hi_i)
        #   sup = min(sum_{i<=j} hi_i,   1 - sum_{i>j} lo_i)
        # (greedy LP solutions for a linear objective over a box with one equality.)
        for j in range(1, k + 1):
            head_lo = float(lo[:j].sum())
            head_hi = float(hi[:j].sum())
            tail_lo = float(lo[j:].sum())
            tail_hi = float(hi[j:].sum())
            slice_inf = max(head_lo, 1.0 - tail_hi)
            slice_sup = min(head_hi, 1.0 - tail_lo)
            inf_S[j - 1] = min(inf_S[j - 1], slice_inf)
            sup_S[j - 1] = max(sup_S[j - 1], slice_sup)
    return [(clean(inf_S[j]), clean(sup_S[j])) for j in range(k)]


def quantile_index_range(
    s_bounds: list[tuple[float, float]], tau: float = 0.5, eps: float = 1e-10
) -> tuple[int, int]:
    """From (inf S_j, sup S_j) for j=1..k, return the (min, max) achievable tau-quantile index.

    j*(p) = min{j : S_j(p) >= tau}; bounds use the equivalences
      min_p j*(p) = min{j : sup S_j >= tau},
      max_p j*(p) = max{j : inf S_{j-1} < tau}   (with S_0 = 0).
    """
    k = len(s_bounds)
    min_j = next((j for j in range(1, k + 1) if s_bounds[j - 1][1] >= tau - eps), k)
    max_j = 1
    for j in range(1, k + 1):
        inf_Sjm1 = 0.0 if j == 1 else s_bounds[j - 2][0]
        if inf_Sjm1 < tau - eps:
            max_j = j
    return min_j, max_j


def polytope_median_bound(
    r: tuple[int, ...], n: int, k: int, x: np.ndarray, rule: str, tau: float = 0.5
) -> tuple[tuple[float, float], tuple[int, int]]:
    """Median (or tau-quantile) bound on Y = x_J, J~p, p in P_rule(r). x assumed nondecreasing."""
    s = polytope_cumsum_bounds(r, n, k, rule)
    lo_j, hi_j = quantile_index_range(s, tau)
    return (float(x[lo_j - 1]), float(x[hi_j - 1])), (lo_j, hi_j)


def l1_median_bound(
    r: tuple[int, ...], n: int, k: int, x: np.ndarray, tau: float = 0.5, c_denom: int = 2000
) -> tuple[tuple[float, float], tuple[int, int]]:
    """Median (or tau-quantile) bound for Manhattan, via threshold-indexed slice family."""
    s = l1_cumsum_bounds(r, n, k, c_denom)
    lo_j, hi_j = quantile_index_range(s, tau)
    return (float(x[lo_j - 1]), float(x[hi_j - 1])), (lo_j, hi_j)


def brute_median_index_set(
    r: tuple[int, ...], n: int, k: int, denom: int, rule: str, tau: float = 0.5
) -> set[int]:
    """Enumerate the simplex grid; for each p in the rule's identified region, compute the
    tau-quantile index of the cumulative distribution and collect achievable indices.
    """
    region_test = {
        "exact":   lambda p: exact_transfer_region(r, p),
        "squared": lambda p: squared_transfer_region(r, p, n),
        "l1":      lambda p: l1_exchange_region(r, p, n),
    }[rule]
    indices: set[int] = set()
    for p in simplex_grid(k, denom):
        if not region_test(p):
            continue
        cum = 0.0
        for j in range(1, k + 1):
            cum += float(p[j - 1])
            if cum >= tau - 1e-12:
                indices.add(j)
                break
    return indices


def clean(v: float, tol: float = 1e-10) -> float:
    if abs(v) < tol:
        return 0.0
    if abs(v - 1.0) < tol:
        return 1.0
    return v


def fmt_interval(iv: tuple[float, float] | None, digits: int = 4) -> str:
    if iv is None:
        return "NA"
    return f"[{iv[0]:.{digits}f}, {iv[1]:.{digits}f}]"


def direct_expected_values_binary(rule: str, p1: float, a: float = 9.0) -> dict[tuple[int, int], tuple[float, float]]:
    p = np.array([p1, 1 - p1])
    reports = feasible_reports(2, 2)
    out = {}
    for r in reports:
        es = expected_score(rule, r, p, reports, a=a)
        eu = sum(multinomial_pmf(w, p) * math.sqrt({"squared": score_squared, "l1": score_l1}[rule](r, w, a=a)) for w in reports)
        out[r] = (es, eu)
    return out


@dataclass
class CheckResult:
    name: str
    passed: int = 0
    failed: int = 0
    details: list[str] | None = None

    def __post_init__(self) -> None:
        if self.details is None:
            self.details = []

    def check(self, condition: bool, detail: str) -> None:
        if condition:
            self.passed += 1
        else:
            self.failed += 1
            self.details.append(detail)

    @property
    def ok(self) -> bool:
        return self.failed == 0


def run_checks() -> list[CheckResult]:
    results = [
        CheckResult("exact direct optima = multinomial modes"),
        CheckResult("exact transfer region = mode region on grid"),
        CheckResult("exact interval formula contains grid region and endpoints satisfy region"),
        CheckResult("squared direct optima = projection"),
        CheckResult("squared halfspace/transfer regions = projection on grid"),
        CheckResult("squared closed-form intervals = LP intervals"),
        CheckResult("L1 direct optima = separable binomial objective"),
        CheckResult("L1 delta formula"),
        CheckResult("L1 exchange region = direct optima on grid"),
        CheckResult("binary L1 median intervals"),
        CheckResult("direct-monetary risk reversals"),
        CheckResult("Hamming direct optima = marginal exact-coordinate objective"),
        CheckResult("binary Hamming = exact match"),
        CheckResult("median-index sets (analytic LP/threshold) contain brute-force grid"),
    ]
    r0, r1, r2, r3, r4, r4b, r5, r6, r7, r8, r9, r10, r11, r12 = results

    for n, k, denom in [(2, 2, 8), (2, 3, 8), (3, 3, 8), (4, 3, 8)]:
        reports = feasible_reports(n, k)
        for p in simplex_grid(k, denom):
            exact_direct = direct_optima("exact", p, n, k)
            modes = exact_modes(p, n, k)
            r0.check(exact_direct == modes, f"n={n}, k={k}, p={p}: {exact_direct} != {modes}")
            for rep in reports:
                r1.check((rep in modes) == exact_transfer_region(rep, p), f"exact transfer mismatch n={n}, k={k}, r={rep}, p={p}")

            sq_direct = direct_optima("squared", p, n, k)
            sq_proj = squared_projection_optima(p, n, k)
            r3.check(sq_direct == sq_proj, f"squared direct mismatch n={n}, k={k}, p={p}")
            for rep in reports:
                h = squared_halfspace_region(rep, p, n, k)
                t = squared_transfer_region(rep, p, n)
                r4.check((rep in sq_proj) == h == t, f"squared region mismatch n={n}, k={k}, r={rep}, p={p}, proj={rep in sq_proj}, h={h}, t={t}")

            l1_direct = direct_optima("l1", p, n, k)
            l1_sep = l1_separable_optima(p, n, k)
            l1_ex = l1_exchange_optima(p, n, k)
            r5.check(l1_direct == l1_sep, f"L1 direct/separable mismatch n={n}, k={k}, p={p}")
            r7.check(l1_direct == l1_ex, f"L1 exchange mismatch n={n}, k={k}, p={p}, direct={l1_direct}, ex={l1_ex}")
            h_direct = direct_optima("hamming", p, n, k)
            h_formula = hamming_optima(p, n, k)
            r10.check(h_direct == h_formula, f"Hamming direct/formula mismatch n={n}, k={k}, p={p}, direct={h_direct}, formula={h_formula}")
            for i in range(k):
                for t in range(n):
                    lhs = l1_delta(i, t, p, n)
                    rhs = 2 * binom.cdf(t, n, float(p[i])) - 1
                    r6.check(abs(lhs - rhs) < 1e-9, f"delta mismatch n={n}, p={p}, i={i}, t={t}, {lhs} vs {rhs}")

        for rep in reports:
            exact_iv = exact_coordinate_intervals(rep, n, k)
            grid_iv, _, count = exact_grid_bounds(rep, k, denom)
            if count:
                for i, (lo, hi) in enumerate(exact_iv):
                    glo, ghi = grid_iv[i]
                    r2.check(lo <= glo + 1e-10 and ghi <= hi + 1e-10, f"exact grid interval outside formula n={n}, k={k}, r={rep}, i={i}, grid={grid_iv[i]}, formula={(lo, hi)}")
                    lower, upper = endpoint_vectors_exact(rep, n, k, i)
                    r2.check(exact_transfer_region(rep, lower) and exact_transfer_region(rep, upper), f"endpoint not feasible n={n}, k={k}, r={rep}, i={i}")
            lp_iv, _ = squared_lp_bounds(rep, n, k)
            cf_iv = squared_closed_form_bounds(rep, n, k)
            for i, (lp, cf) in enumerate(zip(lp_iv, cf_iv)):
                ok = abs(lp[0] - cf[0]) < 1e-8 and abs(lp[1] - cf[1]) < 1e-8
                r4b.check(ok, f"squared closed-form mismatch n={n}, k={k}, r={rep}, i={i}, lp={lp}, cf={cf}")

    for n in [2, 3, 5, 10]:
        denom = 100
        for t in range(n + 1):
            for p1 in np.linspace(0, 1, denom + 1):
                p = np.array([p1, 1 - p1])
                is_l1 = (t, n - t) in l1_exchange_optima(p, n, 2)
                f_left = 0.0 if t == 0 else binom.cdf(t - 1, n, p1)
                f_right = binom.cdf(t, n, p1)
                is_med = f_left <= 0.5 + 1e-10 and f_right + 1e-10 >= 0.5
                r8.check(is_l1 == is_med, f"binary median mismatch n={n}, t={t}, p={p1}, l1={is_l1}, med={is_med}")
                is_hamming = (t, n - t) in hamming_optima(p, n, 2)
                is_exact = (t, n - t) in exact_modes(p, n, 2)
                r11.check(is_hamming == is_exact, f"binary Hamming/exact mismatch n={n}, t={t}, p={p1}, hamming={is_hamming}, exact={is_exact}")

    sq_vals = direct_expected_values_binary("squared", 0.229)
    l1_vals = direct_expected_values_binary("l1", 0.289)
    sq_es = max(sq_vals, key=lambda rr: sq_vals[rr][0])
    sq_eu = max(sq_vals, key=lambda rr: sq_vals[rr][1])
    l1_es = max(l1_vals, key=lambda rr: l1_vals[rr][0])
    l1_eu = max(l1_vals, key=lambda rr: l1_vals[rr][1])
    r9.check(sq_es == (0, 2) and sq_eu == (1, 1), f"squared risk reversal failed: {sq_vals}")
    r9.check(l1_es == (0, 2) and l1_eu == (1, 1), f"L1 risk reversal failed: {l1_vals}")

    # Median-index check: the analytic median-index set (from polytope LP for exact/squared,
    # threshold-grid for L1) must contain every index produced by brute-force enumeration
    # over the simplex grid. The other direction is grid-tolerance-bound.
    for n, k, denom in [(2, 3, 120), (3, 3, 120), (4, 3, 80), (3, 4, 80)]:
        for rep in feasible_reports(n, k):
            brute = brute_median_index_set(rep, n, k, denom, "exact")
            _, jr_exact = polytope_median_bound(rep, n, k, np.arange(k, dtype=float), "exact")
            r12.check(brute.issubset(set(range(jr_exact[0], jr_exact[1] + 1))),
                      f"exact median miss n={n} k={k} r={rep} brute={brute} analytic={jr_exact}")
            brute = brute_median_index_set(rep, n, k, denom, "squared")
            _, jr_sq = polytope_median_bound(rep, n, k, np.arange(k, dtype=float), "squared")
            r12.check(brute.issubset(set(range(jr_sq[0], jr_sq[1] + 1))),
                      f"squared median miss n={n} k={k} r={rep} brute={brute} analytic={jr_sq}")
            brute = brute_median_index_set(rep, n, k, denom, "l1")
            _, jr_l1 = l1_median_bound(rep, n, k, np.arange(k, dtype=float), c_denom=400)
            r12.check(brute.issubset(set(range(jr_l1[0], jr_l1[1] + 1))),
                      f"L1 median miss n={n} k={k} r={rep} brute={brute} analytic={jr_l1}")

    return results


def exact_payment_probability(r: tuple[int, ...]) -> float:
    n = sum(r)
    p = np.array(r, dtype=float) / n
    return multinomial_pmf(r, p)


def worked_example(n: int, k: int, r: tuple[int, ...], grid_denom: int = 160, threshold_denom: int = 10000) -> dict:
    x = np.arange(k, dtype=float)
    exact_coord = exact_coordinate_intervals(r, n, k)
    exact_mean = exact_lp_mean_bounds(r, n, k, x)
    sq_coord = squared_closed_form_bounds(r, n, k)
    _, sq_mean = squared_lp_bounds(r, n, k, x)
    l1_coord, l1_mean, l1_count = l1_threshold_bounds(r, n, k, threshold_denom, x)
    l1_grid_coord, l1_grid_mean, l1_grid_count = l1_grid_bounds(r, n, k, grid_denom, x)
    exact_grid, exact_grid_mean, exact_grid_count = exact_grid_bounds(r, k, grid_denom, x)
    return {
        "n": n,
        "k": k,
        "r": r,
        "x": tuple(int(v) for v in x),
        "exact_coord": exact_coord,
        "exact_mean": exact_mean,
        "exact_grid": exact_grid,
        "exact_grid_mean": exact_grid_mean,
        "exact_grid_count": exact_grid_count,
        "squared_coord": sq_coord,
        "squared_mean": sq_mean,
        "l1_coord_threshold": l1_coord,
        "l1_mean_threshold": l1_mean,
        "l1_threshold_count": l1_count,
        "l1_coord_grid": l1_grid_coord,
        "l1_mean_grid": l1_grid_mean,
        "l1_grid_count": l1_grid_count,
        "grid_denom": grid_denom,
        "threshold_denom": threshold_denom,
        "exact_payment_at_report_share": exact_payment_probability(r),
    }


def make_worked_examples_md(examples: list[dict]) -> str:
    lines = [
        "# Worked Examples",
        "",
        "Intervals labeled exact are analytic or LP-computed over an exact finite-dimensional region. L1 multi-category intervals use the threshold-search characterization over the exact CDF-exchange region; the reported numerical values are approximations over a fine threshold grid.",
        "",
    ]
    for label, ex in zip(["Example A", "Example B"], examples):
        lines += [
            f"## {label}: n = {ex['n']}, k = {ex['k']}, r = {ex['r']}",
            "",
            f"Numerical outcomes for mean intervals: \\(x={ex['x']}\\).",
            "",
            f"Exact-match payment probability at representative belief \\(p=r/n\\): `{ex['exact_payment_at_report_share']:.6f}`.",
            "",
            "| Rule | p1 interval | p2 interval | p3 interval | mean interval | Method |",
            "|---|---:|---:|---:|---:|---|",
        ]

        def row(rule: str, coord, mean, method: str) -> str:
            vals = [fmt_interval(coord[i]) if coord and i < len(coord) else "NA" for i in range(3)]
            return f"| {rule} | {vals[0]} | {vals[1]} | {vals[2]} | {fmt_interval(mean)} | {method} |"

        lines.append(row("Exact match", ex["exact_coord"], ex["exact_mean"], "closed form for coordinates; LP for mean"))
        lines.append(row("Squared distance", ex["squared_coord"], ex["squared_mean"], "closed form for coordinates; LP for mean"))
        lines.append(row("L1 distance", ex["l1_coord_threshold"], ex["l1_mean_threshold"], f"threshold-search approximation, denominator {ex['threshold_denom']}; {ex['l1_threshold_count']} feasible thresholds"))
        lines += [
            "",
            "Width comparison:",
            "",
            "| Rule | p1 width | p2 width | p3 width | mean width |",
            "|---|---:|---:|---:|---:|",
        ]
        for rule, coord, mean in [
            ("Exact match", ex["exact_coord"], ex["exact_mean"]),
            ("Squared distance", ex["squared_coord"], ex["squared_mean"]),
            ("L1 distance (threshold)", ex["l1_coord_threshold"], ex["l1_mean_threshold"]),
        ]:
            widths = [(iv[1] - iv[0]) if iv else float("nan") for iv in (coord or [None, None, None])]
            while len(widths) < 3:
                widths.append(float("nan"))
            mw = mean[1] - mean[0] if mean else float("nan")
            lines.append(f"| {rule} | {widths[0]:.4f} | {widths[1]:.4f} | {widths[2]:.4f} | {mw:.4f} |")
        lines += [
            "",
            f"Grid diagnostic for L1: simplex grid denominator `{ex['grid_denom']}` gave coordinate intervals "
            f"{[fmt_interval(iv) for iv in (ex['l1_coord_grid'] or [])]} and mean interval {fmt_interval(ex['l1_mean_grid'])}.",
            "",
            "Interpretation: exact-match and squared-distance coordinate intervals are analytically transparent; squared-distance mean intervals use LPs over the same linear region; L1 intervals are explicit through CDF inequalities and numerically sharper through threshold search than through a coarse simplex grid.",
            "",
        ]
    return "\n".join(lines)


def make_verification_md(results: list[CheckResult], examples: list[dict]) -> str:
    lines = [
        "# Computational Verification",
        "",
        "This note summarizes finite-sample computational checks run by `scripts/verify_regions.py`. These checks are not mathematical proofs; grid checks are finite approximations.",
        "",
        "## Checks Run",
        "",
        "| Check | Passed | Failed | Status |",
        "|---|---:|---:|---|",
    ]
    for res in results:
        lines.append(f"| {res.name} | {res.passed} | {res.failed} | {'passed' if res.ok else 'FAILED'} |")
    lines += ["", "## Claims Checked", ""]
    if all(r.ok for r in results):
        lines.append("- All implemented finite-grid and enumeration checks passed.")
    else:
        lines.append("- Some checks failed; see failure details below.")
    lines += [
        "- Exact-match direct expected-score maximizers matched multinomial modes.",
        "- Exact-match transfer inequalities matched mode membership on tested grids.",
        "- Exact-match coordinate interval formula contained all tested grid points and endpoint constructions satisfied the transfer region.",
        "- Squared-distance direct expected-score maximizers matched Euclidean projections of \\(np\\).",
        "- Squared-distance halfspace and one-count transfer characterizations agreed with projection membership on tested grids.",
        "- Squared-distance coordinate intervals matched closed-form formulas checked against exact LPs.",
        "- Squared-distance mean intervals are implemented as exact LPs over the same polytope.",
        "- L1 direct expected-score maximizers matched the separable binomial-marginal objective.",
        "- L1 marginal increments matched \\(\\Delta_i(t)=2F_i(t)-1\\).",
        "- L1 exchange/CDF inequalities matched direct optima on tested grids.",
        "- L1 worked-example intervals are reported using the one-dimensional threshold-search characterization, with simplex-grid intervals retained only as diagnostics.",
        "- Binary L1 median intervals matched exchange-optimal reports on tested grids.",
        "- Direct-monetary risk-aversion counterexamples in the paper were verified by enumeration.",
        "",
        "## Worked Examples Generated",
        "",
    ]
    for ex in examples:
        lines.append(f"- \\(n={ex['n']}, k={ex['k']}, r={ex['r']}\\), with \\(x={ex['x']}\\).")
    lines += [
        "",
        "## Limitations",
        "",
        "- Grid verification is not proof and depends on the selected grid denominator.",
        "- L1 multi-category intervals in `worked_examples.md` are numerical threshold-search approximations; the exact object is the one-dimensional threshold optimization over CDF-inverse box-simplex constraints.",
        "- Exact-match bounds still require final bibliography metadata for the Schlag--Tremewan citation.",
        "- No broad Monte Carlo simulation was run; checks are finite enumeration and grid consistency tests for small cases.",
    ]
    failures = [d for r in results for d in (r.details or [])]
    if failures:
        lines += ["", "## Failure Details", ""]
        lines += [f"- {d}" for d in failures[:50]]
    return "\n".join(lines)


def linf_example(n: int, k: int, r: tuple[int, ...], denom: int) -> dict:
    x = np.arange(k, dtype=float)
    coord, mean, count = linf_grid_bounds(r, n, k, denom, x)
    beliefs = {
        "uniform": np.ones(k) / k,
        "report share": np.array(r, dtype=float) / n,
    }
    if k == 3:
        beliefs["asymmetric"] = np.array([0.6, 0.3, 0.1])
    else:
        raw = np.arange(k, 0, -1, dtype=float)
        beliefs["asymmetric"] = raw / raw.sum()

    reps = []
    for label, p in beliefs.items():
        opt = sorted(linf_optima(p, n, k))
        loss = linf_expected_loss(r, p, n, k)
        tail = linf_expected_loss_tail_sum(r, p, n, k)
        reps.append((label, tuple(clean(float(v)) for v in p), opt, clean(loss), clean(tail)))
    return {
        "n": n,
        "k": k,
        "r": r,
        "coord": coord,
        "mean": mean,
        "count": count,
        "denom": denom,
        "x": tuple(int(v) for v in x),
        "representative": reps,
    }


def interval_width(iv: tuple[float, float] | None) -> float:
    if iv is None:
        return float("nan")
    return clean(iv[1] - iv[0])


def average_coordinate_width(coord: list[tuple[float, float]] | None) -> float:
    if not coord:
        return float("nan")
    return clean(float(np.mean([interval_width(iv) for iv in coord])))


def max_coordinate_width(coord: list[tuple[float, float]] | None) -> float:
    if not coord:
        return float("nan")
    return clean(max(interval_width(iv) for iv in coord))


def region_share(count: int, denom: int, k: int) -> float:
    total = len(feasible_reports(denom, k))
    return clean(count / total)


def redirection_example(
    n: int,
    k: int,
    r: tuple[int, ...],
    grid_denom: int,
    threshold_denom: int,
) -> dict:
    x = np.arange(k, dtype=float)
    exact_coord = exact_coordinate_intervals(r, n, k)
    exact_mean = exact_lp_mean_bounds(r, n, k, x)
    exact_grid, _, exact_count = exact_grid_bounds(r, k, grid_denom, x)

    squared_coord = squared_closed_form_bounds(r, n, k)
    _, squared_mean = squared_lp_bounds(r, n, k, x)
    _, _, squared_count = squared_grid_bounds(r, n, k, grid_denom, x)

    l1_coord, l1_mean, l1_threshold_count = l1_threshold_bounds(r, n, k, threshold_denom, x)
    _, _, l1_count = l1_grid_bounds(r, n, k, grid_denom, x)

    linf_coord, linf_mean, linf_count = linf_grid_bounds(r, n, k, grid_denom, x)
    hamming_coord, hamming_mean, hamming_count = hamming_grid_bounds(r, n, k, grid_denom, x)

    rules = [
        ("Exact", exact_coord, exact_mean, exact_count, "closed-form coordinates; LP mean"),
        ("Squared", squared_coord, squared_mean, squared_count, "closed-form coordinates; LP mean"),
        ("L1", l1_coord, l1_mean, l1_count, f"threshold approximation; {l1_threshold_count} feasible thresholds"),
        ("L-infinity", linf_coord, linf_mean, linf_count, "simplex-grid approximation"),
        ("Hamming", hamming_coord, hamming_mean, hamming_count, "simplex-grid approximation"),
    ]
    rows = []
    for name, coord, mean, count, method in rules:
        rows.append(
            {
                "rule": name,
                "coord": coord,
                "mean": mean,
                "count": count,
                "share": region_share(count, grid_denom, k),
                "avg_width": average_coordinate_width(coord),
                "max_width": max_coordinate_width(coord),
                "mean_width": interval_width(mean),
                "method": method,
            }
        )
    return {
        "n": n,
        "k": k,
        "r": r,
        "x": tuple(int(v) for v in x),
        "grid_denom": grid_denom,
        "threshold_denom": threshold_denom,
        "payment": exact_payment_probability(r),
        "rows": rows,
    }


def make_redirection_diagnostics_md(grid_denom: int = 50, threshold_denom: int = 2000) -> str:
    cases = [
        (2, 3, (1, 1, 0)),
        (2, 3, (2, 0, 0)),
        (5, 3, (2, 2, 1)),
        (5, 3, (3, 2, 0)),
        (5, 3, (5, 0, 0)),
        (10, 3, (5, 3, 2)),
        (10, 3, (9, 1, 0)),
        (10, 3, (10, 0, 0)),
    ]
    examples = [redirection_example(n, k, r, grid_denom, threshold_denom) for n, k, r in cases]

    win_counts = {
        "avg": {name: 0 for name in ["Exact", "Squared", "L1", "L-infinity", "Hamming"]},
        "mean": {name: 0 for name in ["Exact", "Squared", "L1", "L-infinity", "Hamming"]},
    }
    for ex in examples:
        avg_winner = min(ex["rows"], key=lambda row: row["avg_width"] if not math.isnan(row["avg_width"]) else float("inf"))
        mean_winner = min(ex["rows"], key=lambda row: row["mean_width"] if not math.isnan(row["mean_width"]) else float("inf"))
        win_counts["avg"][avg_winner["rule"]] += 1
        win_counts["mean"][mean_winner["rule"]] += 1

    lines = [
        "# Redirection Diagnostics",
        "",
        "This note implements the concrete diagnostic step from `redirection_assessment.md`. It is exploratory and should not be read as a proof or as manuscript-ready evidence.",
        "",
        "## Setup",
        "",
        "- Rules compared: exact match, squared distance, L1, L-infinity, and Hamming coordinate mismatch.",
        "- Fixed diagnostic dimension: `k=3`.",
        f"- Simplex grid denominator for approximate regions: `{grid_denom}`.",
        f"- L1 threshold denominator: `{threshold_denom}`.",
        "- Mean intervals use numerical outcomes `x=(0,1,2)`.",
        "- Exact and squared coordinate/mean bounds use analytic/LP formulas; L1, L-infinity, and Hamming entries with grid shares are diagnostic approximations unless otherwise stated.",
        "",
        "## Hamming Rule Implemented",
        "",
        "The Hamming coordinate-mismatch rule uses",
        "",
        "\\[",
        "d_H(r,\\omega)=\\sum_i \\mathbf 1\\{r_i\\ne\\omega_i\\}.",
        "\\]",
        "",
        "Its expected loss is",
        "",
        "\\[",
        "\\mathbb E_p[d_H(r,\\omega)]",
        "=\\sum_i \\{1-\\Pr(\\mathrm{Bin}(n,p_i)=r_i)\\}.",
        "\\]",
        "",
        "Thus Hamming is computationally simpler than L-infinity because it separates in expected loss, but its inverse region is still nonlinear in \\(p\\) and the count-sum constraint couples the report coordinates.",
        "",
        "## Winner Counts Across Diagnostic Cases",
        "",
        "| Metric | Exact | Squared | L1 | L-infinity | Hamming |",
        "|---|---:|---:|---:|---:|---:|",
        f"| Lowest average coordinate width | {win_counts['avg']['Exact']} | {win_counts['avg']['Squared']} | {win_counts['avg']['L1']} | {win_counts['avg']['L-infinity']} | {win_counts['avg']['Hamming']} |",
        f"| Lowest mean width | {win_counts['mean']['Exact']} | {win_counts['mean']['Squared']} | {win_counts['mean']['L1']} | {win_counts['mean']['L-infinity']} | {win_counts['mean']['Hamming']} |",
        "",
        "Winner counts involving L-infinity or Hamming should be interpreted cautiously because those bounds are grid approximations.",
        "",
        "## Case Tables",
        "",
    ]

    for ex in examples:
        lines += [
            f"### n = {ex['n']}, k = {ex['k']}, r = {ex['r']}",
            "",
            f"Exact-match payment probability at `p=r/n`: `{ex['payment']:.6f}`.",
            "",
            "| Rule | avg coord width | max coord width | mean width | grid region share | method |",
            "|---|---:|---:|---:|---:|---|",
        ]
        for row in ex["rows"]:
            lines.append(
                f"| {row['rule']} | {row['avg_width']:.4f} | {row['max_width']:.4f} | "
                f"{row['mean_width']:.4f} | {row['share']:.4f} | {row['method']} |"
            )
        lines.append("")

    lines += [
        "## Diagnostic Interpretation",
        "",
        "- Squared distance remains the strongest analytical candidate because its bounds are exact, transparent, and cheap to compute.",
        "- Exact match remains a serious benchmark, not a dominated baseline: it wins some finite cases and has fixed-prize risk robustness.",
        "- L1 remains the only nonlinear comparison rule with a structured threshold representation.",
        "- L-infinity sometimes looks competitive in the coarse grid tables, but it does not gain main-text status from these diagnostics because the intervals come from grid checks over a nonseparable nonlinear region.",
        "- Hamming is easier to compute than L-infinity and is worth one targeted derivation attempt if the project moves toward a broader taxonomy. The current diagnostic is not enough to promote it to the main theorem structure because its bounds are still grid-based and nonlinear.",
        "",
        "## Recommendation For The Redirection",
        "",
        "Do not broaden the paper into a five-rule taxonomy yet. Keep the main paper centered on squared distance, exact match, and L1. If a broader taxonomy remains attractive, the next mathematical target should be Hamming, not L-infinity, because Hamming separates in expected loss and may be more tractable. Use L-infinity as diagnostic/future-work material unless a later derivation finds clean closed-form or low-dimensional bounds.",
    ]
    return "\n".join(lines)


def make_linf_exploration_md(denom: int = 120) -> str:
    examples = [
        linf_example(2, 3, (1, 1, 0), denom),
        linf_example(3, 3, (2, 1, 0), denom),
        linf_example(5, 3, (2, 2, 1), denom),
    ]

    lines = [
        "# L-infinity Exploration",
        "",
        "This is a side exploration only. It does not propose adding the rule to the paper.",
        "",
        "## Mechanism",
        "",
        "The candidate rule is",
        "",
        "\\[",
        "S_\\infty(r,\\omega)=a-\\|r-\\omega\\|_\\infty",
        "=a-\\max_i |r_i-\\omega_i|.",
        "\\]",
        "",
        "The rule rewards minimizing the largest category-level count error. It is a worst-coordinate-error rule, unlike L1, which penalizes total absolute error, and squared L2, which penalizes squared aggregate error.",
        "",
        "## Optimal Report Correspondence",
        "",
        "For latent beliefs \\(p\\), the forward correspondence is",
        "",
        "\\[",
        "R_\\infty(p)=\\arg\\min_{r\\in\\Omega}\\mathbb E_p[\\|r-\\omega\\|_\\infty].",
        "\\]",
        "",
        "The objective does not decompose across coordinates because the maximum couples the category errors inside every realization. A useful exact identity is the tail-sum formula",
        "",
        "\\[",
        "\\mathbb E_p\\|r-\\omega\\|_\\infty=\\sum_{m=1}^n\\Pr_p(\\|r-\\omega\\|_\\infty\\ge m),",
        "\\]",
        "",
        "but the probabilities are joint multinomial probabilities over boxes around \\(r\\), not sums of marginal binomial losses. This makes the rule computationally checkable by enumeration for small \\(n,k\\), but it does not give a componentwise median, mean-projection, or mode characterization.",
        "",
        "Status: no clean multi-category optimal-report characterization was found. One-count transfer conditions can be checked numerically, but they are not obviously sufficient in the way they are for separable convex L1 or squared-distance objectives.",
        "",
        "## Binary Case",
        "",
        "Let \\(k=2\\), \\(r=(t,n-t)\\), and \\(\\omega=(W,n-W)\\), where \\(W\\sim\\mathrm{Bin}(n,p_1)\\). Then",
        "",
        "\\[",
        "\\|r-\\omega\\|_\\infty",
        "=\\max\\{|t-W|, |(n-t)-(n-W)|\\}",
        "=|t-W|.",
        "\\]",
        "",
        "By contrast, the L1 loss is \\(2|t-W|\\). Multiplying the loss by a positive constant does not change the argmin, so binary L-infinity and binary L1 induce the same optimal reports.",
        "",
        "The inverse interval is therefore the binomial-median interval:",
        "",
        "\\[",
        "P_{\\infty,1}(t,n-t)",
        "=\\{p_1\\in[0,1]:F(t-1;n,p_1)\\le 1/2\\le F(t;n,p_1)\\}.",
        "\\]",
        "",
        "With \\(F(-1;n,p_1)=0\\) and \\(F(n;n,p_1)=1\\), the boundary cases are the same as binary L1: for \\(t=0\\), \\(0\\le p_1\\le 1-2^{-1/n}\\); for \\(t=n\\), \\(2^{-1/n}\\le p_1\\le1\\).",
        "",
        "## Multi-Category Inverse Region",
        "",
        "For an observed report \\(r\\), the exact inverse region is",
        "",
        "\\[",
        "P_\\infty(r)=\\{p\\in\\Delta^k:",
        "\\mathbb E_p\\|r-\\omega\\|_\\infty\\le",
        "\\mathbb E_p\\|s-\\omega\\|_\\infty\\ \\forall s\\in\\Omega\\}.",
        "\\]",
        "",
        "This is finite and computationally usable for small \\(n,k\\), because all alternatives \\(s\\in\\Omega\\) and all realizations \\(\\omega\\in\\Omega\\) can be enumerated. However, each inequality is a polynomial probability inequality in \\(p\\), not a linear halfspace. The region is not generally polyhedral, and no convexity is asserted.",
        "",
        "## Identification Bounds",
        "",
        "The exact coordinate bounds are",
        "",
        "\\[",
        "\\underline p_{\\infty,i}(r)=\\min_{p\\in\\Delta^k}p_i,\\qquad",
        "\\overline p_{\\infty,i}(r)=\\max_{p\\in\\Delta^k}p_i",
        "\\]",
        "",
        "subject to the expected-loss inequalities defining \\(P_\\infty(r)\\). These are nonlinear programs. Closed-form multi-category bounds were not found. The grid intervals below are approximate diagnostics only, not proofs of sharpness.",
        "",
        "## Small Multi-Category Examples",
        "",
        f"Grid denominator: `{denom}`. All L-infinity intervals in this section are grid approximations.",
        "",
    ]

    for ex in examples:
        lines += [
            f"### n = {ex['n']}, k = {ex['k']}, r = {ex['r']}",
            "",
            f"Numerical outcomes for mean interval: \\(x={ex['x']}\\).",
            "",
            "| Quantity | Approximate interval |",
            "|---|---:|",
        ]
        coord = ex["coord"]
        for i in range(ex["k"]):
            lines.append(f"| p{i + 1} | {fmt_interval(coord[i]) if coord else 'NA'} |")
        lines.append(f"| mean | {fmt_interval(ex['mean'])} |")
        lines += [
            "",
            f"Grid points in approximate inverse region: `{ex['count']}`.",
            "",
            "| Representative belief | p | L-infinity optimal reports | expected loss at observed r | tail-sum check |",
            "|---|---|---|---:|---:|",
        ]
        for label, p, opt, loss, tail in ex["representative"]:
            lines.append(f"| {label} | `{p}` | `{opt}` | {loss:.6f} | {tail:.6f} |")
        lines.append("")

    lines += [
        "## Comparison With Current Rules",
        "",
        "| Rule | Objective | Forward object | Inverse region | Coordinate bounds | Main advantage | Main drawback |",
        "|---|---|---|---|---|---|---|",
        "| Exact match | zero-one exact equality | multinomial mode | transfer/mode region | closed form | robust/simple | exact payment probability can be low |",
        "| Squared L2 | squared aggregate error | integer projection of \\(np\\) | linear region | closed form for coordinates; LP for moments | mean-oriented and transparent | direct monetary version assumes risk neutrality |",
        "| L1 | total absolute error | constrained median-type report | CDF exchange region | binary closed form; multi-category nonlinear | median-oriented | less transparent for \\(k>2\\) |",
        "| L-infinity | worst coordinate error | no clean multi-category characterization found | expected-loss inequalities over all reports | binary same as L1; multi-category nonlinear/grid | controls largest count error | nonseparable and inferentially opaque |",
        "",
        "## Should \\(L^\\infty\\) Be Included In The Paper?",
        "",
        "Recommendation: mention briefly in discussion/future work at most, and exclude from the main theorem structure.",
        "",
        "Reason: the binary case is clean but adds no new result because it coincides with binary L1. In multi-category settings, the objective is natural but nonseparable; the inverse region appears to require expected-loss inequalities over all alternative reports, and coordinate intervals are nonlinear programs or grid approximations. This does not strengthen the paper's simplicity-first chain unless a later derivation finds closed-form bounds or a practically compelling special case.",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-notes", action="store_true", help="write verification notes under outputs/verification/")
    parser.add_argument("--grid-denom", type=int, default=160, help="grid denominator for worked L1 approximations")
    parser.add_argument("--threshold-denom", type=int, default=10000, help="threshold grid denominator for worked L1 threshold-search approximations")
    parser.add_argument("--linfty-exploration", action="store_true", help="print the side exploration note for L-infinity scoring")
    parser.add_argument("--redirection-diagnostics", action="store_true", help="print diagnostics for the informational-efficiency redirection")
    parser.add_argument("--write-redirection-diagnostics", action="store_true", help="write redirection diagnostics under outputs/verification/")
    parser.add_argument("--diagnostic-grid-denom", type=int, default=50, help="simplex grid denominator for redirection diagnostics")
    parser.add_argument("--diagnostic-threshold-denom", type=int, default=2000, help="L1 threshold grid denominator for redirection diagnostics")
    args = parser.parse_args()

    if args.linfty_exploration:
        print(make_linf_exploration_md(args.grid_denom))
        return

    if args.redirection_diagnostics or args.write_redirection_diagnostics:
        diagnostics = make_redirection_diagnostics_md(args.diagnostic_grid_denom, args.diagnostic_threshold_denom)
        print(diagnostics)
        if args.write_redirection_diagnostics:
            root = Path(__file__).resolve().parents[1]
            out = root / "outputs" / "verification"
            out.mkdir(parents=True, exist_ok=True)
            (out / "redirection_diagnostics.md").write_text(diagnostics + "\n", encoding="utf-8")
        return

    results = run_checks()
    examples = [
        worked_example(10, 3, (5, 3, 2), args.grid_denom, args.threshold_denom),
        worked_example(2, 3, (1, 1, 0), args.grid_denom, args.threshold_denom),
    ]

    verification = make_verification_md(results, examples)
    worked = make_worked_examples_md(examples)

    print(verification)
    print()
    print("---")
    print()
    print(worked)

    if args.write_notes:
        root = Path(__file__).resolve().parents[1]
        out = root / "outputs" / "verification"
        out.mkdir(parents=True, exist_ok=True)
        (out / "computational_verification.md").write_text(verification + "\n", encoding="utf-8")
        (out / "worked_examples.md").write_text(worked + "\n", encoding="utf-8")

    if any(not res.ok for res in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
