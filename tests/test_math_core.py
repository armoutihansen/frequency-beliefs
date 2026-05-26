"""Unit tests for the pure-math public surface.

These pin the numeric behaviour of the math functions so the Phase 2 dedupe
refactor cannot silently drift the simulation outputs.
"""

import math
from itertools import product

import numpy as np
from scipy.stats import multinomial

from verify_regions import (
    exact_coordinate_intervals,
    feasible_reports,
    l1_threshold_bounds,
    multinomial_pmf,
    simplex_grid,
    squared_closed_form_bounds,
)


def test_feasible_reports_count_k2():
    # For n trials, k=2 categories: there are n+1 feasible reports.
    for n in (1, 5, 10):
        assert len(feasible_reports(n, 2)) == n + 1


def test_feasible_reports_count_general():
    # Multiset coefficient C(n+k-1, k-1) = (n+k-1)! / (n! (k-1)!)
    for n, k in [(3, 3), (5, 4), (4, 5)]:
        expected = math.comb(n + k - 1, k - 1)
        assert len(feasible_reports(n, k)) == expected


def test_feasible_reports_sum_to_n():
    for n, k in [(5, 3), (3, 4)]:
        for r in feasible_reports(n, k):
            assert sum(r) == n
            assert len(r) == k
            assert all(ri >= 0 for ri in r)


def test_multinomial_pmf_agrees_with_scipy():
    # Cross-check our hand-rolled pmf against scipy's reference implementation.
    rng = np.random.default_rng(42)
    for n, k in [(3, 3), (5, 4), (2, 2)]:
        p = rng.dirichlet(np.ones(k))
        for w in feasible_reports(n, k):
            ours = multinomial_pmf(w, p)
            theirs = float(multinomial.pmf(w, n=n, p=p))
            assert math.isclose(ours, theirs, rel_tol=1e-9, abs_tol=1e-12)


def test_multinomial_pmf_sums_to_one():
    rng = np.random.default_rng(7)
    for n, k in [(3, 3), (4, 4)]:
        p = rng.dirichlet(np.ones(k))
        total = sum(multinomial_pmf(w, p) for w in feasible_reports(n, k))
        assert math.isclose(total, 1.0, abs_tol=1e-9)


def test_exact_coordinate_intervals_published_formula():
    # The closed-form for the exact-match rule: [r_i/(n+k-1), (r_i+1)/(n+1)].
    r, n, k = (2, 1, 0), 3, 3
    expected = [(2 / 5, 3 / 4), (1 / 5, 2 / 4), (0 / 5, 1 / 4)]
    got = exact_coordinate_intervals(r, n, k)
    assert all(
        math.isclose(g[0], e[0]) and math.isclose(g[1], e[1])
        for g, e in zip(got, expected)
    )


def test_exact_coordinate_intervals_endpoints_in_simplex():
    # Lower and upper bounds must be in [0, 1].
    for n, k in [(5, 3), (3, 4)]:
        for r in feasible_reports(n, k):
            for lo, hi in exact_coordinate_intervals(r, n, k):
                assert 0.0 <= lo <= hi <= 1.0


def test_squared_closed_form_bounds_published_formula():
    # For r=(2,1,0), n=3, k=3, m=2:
    #   r_i=2: [(2-1)/3+1/(3*3), (2+1)/3-1/(3*2)] = [4/9, 5/6]
    #   r_i=1: [(1-1)/3+1/(3*3), (1+1)/3-1/(3*2)] = [1/9, 1/2]
    #   r_i=0: [0, m/(n*(m+1))] = [0, 2/9]
    r, n, k = (2, 1, 0), 3, 3
    expected = [(4 / 9, 5 / 6), (1 / 9, 1 / 2), (0.0, 2 / 9)]
    got = squared_closed_form_bounds(r, n, k)
    assert all(
        math.isclose(g[0], e[0], abs_tol=1e-9) and math.isclose(g[1], e[1], abs_tol=1e-9)
        for g, e in zip(got, expected)
    )


def test_squared_closed_form_bounds_endpoints_in_simplex():
    for n, k in [(5, 3), (4, 4)]:
        for r in feasible_reports(n, k):
            for lo, hi in squared_closed_form_bounds(r, n, k):
                assert -1e-12 <= lo <= hi <= 1.0 + 1e-12


def test_l1_threshold_bounds_returns_valid_intervals():
    # Smoke test: shape and validity. Numeric values are pinned via
    # consistency_check.py against the committed CSV.
    r, n, k = (2, 1, 0), 3, 3
    coords, mean, n_feasible = l1_threshold_bounds(r, n, k, c_denom=200)
    assert coords is not None
    assert len(coords) == k
    for lo, hi in coords:
        assert -1e-9 <= lo <= hi <= 1.0 + 1e-9
    assert n_feasible > 0


def test_simplex_grid_shape():
    # simplex_grid returns vectors summing to 1 with the right cardinality.
    pts = simplex_grid(k=3, denom=5)
    assert len(pts) == math.comb(5 + 3 - 1, 3 - 1)  # 21
    for p in pts:
        assert math.isclose(float(p.sum()), 1.0, abs_tol=1e-12)
        assert all(pi >= 0 for pi in p)
