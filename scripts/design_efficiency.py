"""Latent-belief simulation for frequency-report scoring rules.

This script implements the latent-belief design exercise summarized in
`_context/current_status.md`.
It compares three headline rules:

1. discrete metric / exact match,
2. quadratic distance,
3. Manhattan distance.

The simulation draws latent beliefs, computes each rule's optimal report, then
computes the identification bounds induced by that report.

Examples:

    uv run python scripts/design_efficiency.py --smoke --validate
    uv run python scripts/design_efficiency.py --pilot
    uv run python scripts/design_efficiency.py --final --draws 5000
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Iterable

import numpy as np
from scipy.optimize import linprog
from scipy.special import betaincinv, gammaln
from scipy.stats import binom

from verify_regions import (
    exact_coordinate_intervals,
    exact_lp_mean_bounds,
    exact_modes,
    feasible_reports,
    l1_separable_optima,
    squared_closed_form_bounds,
    squared_lp_bounds,
    squared_projection_optima,
)


RULES = ("discrete", "quadratic", "manhattan")
RULE_LABELS = {
    "discrete": "Discrete metric",
    "quadratic": "Quadratic distance",
    "manhattan": "Manhattan distance",
}


def clean(v: float, tol: float = 1e-10) -> float:
    if abs(v) < tol:
        return 0.0
    if abs(v - 1.0) < tol:
        return 1.0
    return float(v)


def fmt_float(v: float, digits: int = 6) -> str:
    if math.isnan(v):
        return ""
    return f"{v:.{digits}f}"


def fmt_interval(iv: tuple[float, float], digits: int = 4) -> str:
    return f"[{iv[0]:.{digits}f}, {iv[1]:.{digits}f}]"


def interval_width(iv: tuple[float, float]) -> float:
    return clean(iv[1] - iv[0])


def average_width(coord: list[tuple[float, float]]) -> float:
    return clean(float(np.mean([interval_width(iv) for iv in coord])))


def max_width(coord: list[tuple[float, float]]) -> float:
    return clean(max(interval_width(iv) for iv in coord))


def linear_outcome(k: int) -> np.ndarray:
    if k == 1:
        return np.zeros(1)
    return np.arange(k, dtype=float) / (k - 1)


def skewed_outcome(k: int) -> np.ndarray:
    x = np.zeros(k, dtype=float)
    x[-1] = 1.0
    return x


def report_to_string(r: tuple[int, ...]) -> str:
    return "(" + ",".join(str(v) for v in r) + ")"


def parse_report(text: str) -> tuple[int, ...]:
    stripped = text.strip().strip("()")
    return tuple(int(part.strip()) for part in stripped.split(",") if part.strip())


def log_multinomial_pmf(w: tuple[int, ...], p: np.ndarray) -> float:
    n = sum(w)
    out = gammaln(n + 1.0)
    for wi, pi in zip(w, p):
        out -= gammaln(wi + 1.0)
        if wi > 0:
            if pi <= 0.0:
                return -math.inf
            out += wi * math.log(float(pi))
    return float(out)


def multinomial_pmf_stable(w: tuple[int, ...], p: np.ndarray) -> float:
    logp = log_multinomial_pmf(w, p)
    if logp == -math.inf:
        return 0.0
    return clean(float(math.exp(logp)))


def discrete_mode_report(p: np.ndarray, n: int, tol: float = 1e-12) -> tuple[tuple[int, ...], bool]:
    """Lexicographic multinomial mode by greedy discrete concave allocation."""
    k = len(p)
    counts = np.zeros(k, dtype=int)
    tie_seen = False
    logp = np.full(k, -np.inf)
    positive = p > 0.0
    logp[positive] = np.log(p[positive])
    for _ in range(n):
        priorities = logp - np.log(counts + 1.0)
        best = float(np.max(priorities))
        candidates = np.flatnonzero(np.abs(priorities - best) <= tol)
        if len(candidates) > 1:
            tie_seen = True
        counts[int(candidates[0])] += 1

    r = tuple(int(v) for v in counts)
    for j, rj in enumerate(r):
        if rj == 0:
            continue
        for i, ri in enumerate(r):
            if i == j:
                continue
            if abs(rj * float(p[i]) - (ri + 1) * float(p[j])) <= 1e-10:
                tie_seen = True
    return r, tie_seen


def quadratic_projection_report(p: np.ndarray, n: int, tol: float = 1e-12) -> tuple[tuple[int, ...], bool]:
    x = n * p
    floors = np.floor(x).astype(int)
    remaining = int(n - floors.sum())
    fractions = x - floors
    # Stable lexicographic tie-breaking: sort by descending fractional part, then index.
    order = sorted(range(len(p)), key=lambda i: (-fractions[i], i))
    counts = floors.copy()
    for idx in order[:remaining]:
        counts[idx] += 1

    tie_seen = False
    if 0 < remaining < len(p):
        cutoff = fractions[order[remaining - 1]]
        next_fraction = fractions[order[remaining]]
        tie_seen = abs(float(cutoff - next_fraction)) <= tol
    return tuple(int(v) for v in counts), tie_seen


def manhattan_report(p: np.ndarray, n: int, tol: float = 1e-12) -> tuple[tuple[int, ...], bool]:
    """Optimal Manhattan report via n smallest marginal increments."""
    increments: list[tuple[float, int, int]] = []
    for i, pi in enumerate(p):
        for t in range(n):
            inc = 2.0 * float(binom.cdf(t, n, float(pi))) - 1.0
            increments.append((inc, i, t))
    increments.sort(key=lambda item: (item[0], item[1], item[2]))

    counts = np.zeros(len(p), dtype=int)
    for _inc, i, _t in increments[:n]:
        counts[i] += 1

    tie_seen = False
    if n < len(increments):
        tie_seen = abs(increments[n - 1][0] - increments[n][0]) <= tol
    return tuple(int(v) for v in counts), tie_seen


def exact_transfer_mean_bounds(r: tuple[int, ...], n: int, k: int, x: np.ndarray) -> tuple[float, float]:
    return exact_lp_mean_bounds(r, n, k, x)


def quadratic_transfer_mean_bounds(r: tuple[int, ...], n: int, k: int, x: np.ndarray) -> tuple[float, float]:
    a_ub = []
    b_ub = []
    for j, rj in enumerate(r):
        if rj == 0:
            continue
        for i, ri in enumerate(r):
            row = np.zeros(k)
            row[i] = n
            row[j] -= n
            a_ub.append(row)
            b_ub.append(ri - rj + 1)
    a_eq = [np.ones(k)]
    b_eq = [1.0]
    bounds = [(0.0, 1.0)] * k

    def solve(c: np.ndarray) -> float:
        res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
        if not res.success:
            raise RuntimeError(res.message)
        return float(res.fun)

    return clean(solve(x)), clean(-solve(-x))


def inverse_binom_cdf_decreasing(t: int, n: int, c: np.ndarray) -> np.ndarray:
    c = np.asarray(c, dtype=float)
    out = np.empty_like(c)
    out[c <= 0.0] = 1.0
    out[c >= 1.0] = 0.0
    mask = (c > 0.0) & (c < 1.0)
    if mask.any():
        out[mask] = 1.0 - betaincinv(n - t, t + 1, c[mask])
    return np.clip(out, 0.0, 1.0)


_MANHATTAN_INV_CACHE: dict[tuple[int, int], dict[int, np.ndarray]] = {}


def manhattan_inverse_cache(n: int, c_grid: np.ndarray) -> dict[int, np.ndarray]:
    key = (n, len(c_grid))
    if key not in _MANHATTAN_INV_CACHE:
        _MANHATTAN_INV_CACHE[key] = {
            t: inverse_binom_cdf_decreasing(t, n, c_grid) for t in range(n)
        }
    return _MANHATTAN_INV_CACHE[key]


def box_simplex_linear_bounds(lo: np.ndarray, hi: np.ndarray, x: np.ndarray) -> tuple[float, float]:
    residual = 1.0 - float(lo.sum())
    p_min = lo.copy()
    left = residual
    for idx in np.argsort(x):
        add = min(float(hi[idx] - lo[idx]), left)
        p_min[idx] += add
        left -= add
        if left <= 1e-12:
            break

    p_max = lo.copy()
    left = residual
    for idx in np.argsort(-x):
        add = min(float(hi[idx] - lo[idx]), left)
        p_max[idx] += add
        left -= add
        if left <= 1e-12:
            break
    return clean(float(p_min @ x)), clean(float(p_max @ x))


def manhattan_threshold_bounds(
    r: tuple[int, ...],
    n: int,
    k: int,
    c_grid: np.ndarray,
    x_linear: np.ndarray,
    x_skewed: np.ndarray,
) -> tuple[list[tuple[float, float]], tuple[float, float], tuple[float, float], int]:
    inv_cache = manhattan_inverse_cache(n, c_grid)
    c_count = len(c_grid)
    lo_mat = np.zeros((c_count, k), dtype=float)
    hi_mat = np.ones((c_count, k), dtype=float)
    for h, rh in enumerate(r):
        if rh > 0:
            lo_mat[:, h] = inv_cache[rh - 1]
        if rh < n:
            hi_mat[:, h] = inv_cache[rh]

    sum_lo = lo_mat.sum(axis=1)
    sum_hi = hi_mat.sum(axis=1)
    feasible = (sum_lo <= 1.0 + 1e-10) & (sum_hi + 1e-10 >= 1.0)
    feasible_count = int(feasible.sum())
    if feasible_count == 0:
        raise RuntimeError(f"No feasible Manhattan threshold for r={r}, n={n}, k={k}")

    coord_los = np.maximum(lo_mat, 1.0 - (sum_hi[:, None] - hi_mat))
    coord_his = np.minimum(hi_mat, 1.0 - (sum_lo[:, None] - lo_mat))
    coord = [
        (clean(float(coord_los[feasible, i].min())), clean(float(coord_his[feasible, i].max())))
        for i in range(k)
    ]

    linear_lo = np.inf
    linear_hi = -np.inf
    skewed_lo = np.inf
    skewed_hi = -np.inf
    for lo, hi in zip(lo_mat[feasible], hi_mat[feasible]):
        lo_val, hi_val = box_simplex_linear_bounds(lo, hi, x_linear)
        linear_lo = min(linear_lo, lo_val)
        linear_hi = max(linear_hi, hi_val)
        lo_val, hi_val = box_simplex_linear_bounds(lo, hi, x_skewed)
        skewed_lo = min(skewed_lo, lo_val)
        skewed_hi = max(skewed_hi, hi_val)

    return (
        coord,
        (clean(linear_lo), clean(linear_hi)),
        (clean(skewed_lo), clean(skewed_hi)),
        feasible_count,
    )


@dataclass(frozen=True)
class BoundResult:
    coord: list[tuple[float, float]]
    mean_linear: tuple[float, float]
    mean_skewed: tuple[float, float]
    method: str


class BoundComputer:
    def __init__(self, tolerance: float) -> None:
        self.tolerance = tolerance
        denom = max(1, int(round(1.0 / tolerance)))
        self.c_grid = np.linspace(0.0, 1.0, denom + 1)
        self.cache: dict[tuple[str, int, int, tuple[int, ...]], BoundResult] = {}

    def bounds(self, rule: str, r: tuple[int, ...], n: int, k: int) -> BoundResult:
        key = (rule, n, k, r)
        if key in self.cache:
            return self.cache[key]

        x_linear = linear_outcome(k)
        x_skewed = skewed_outcome(k)
        if rule == "discrete":
            coord = exact_coordinate_intervals(r, n, k)
            linear = exact_transfer_mean_bounds(r, n, k, x_linear)
            skewed = exact_transfer_mean_bounds(r, n, k, x_skewed)
            method = "closed-form coordinates; LP functionals"
        elif rule == "quadratic":
            coord = squared_closed_form_bounds(r, n, k)
            linear = quadratic_transfer_mean_bounds(r, n, k, x_linear)
            skewed = quadratic_transfer_mean_bounds(r, n, k, x_skewed)
            method = "closed-form coordinates; LP functionals"
        elif rule == "manhattan":
            coord, linear, skewed, feasible = manhattan_threshold_bounds(
                r, n, k, self.c_grid, x_linear, x_skewed
            )
            method = f"threshold-computed; tolerance {self.tolerance:g}; {feasible} feasible thresholds"
        else:
            raise ValueError(rule)

        result = BoundResult(coord=coord, mean_linear=linear, mean_skewed=skewed, method=method)
        self.cache[key] = result
        return result


@dataclass
class RuleMetric:
    report: tuple[int, ...]
    tie: bool
    coord_avg: float
    coord_max: float
    mean_linear_width: float
    mean_skewed_width: float
    payment_probability: float
    method: str


def report_for_rule(rule: str, p: np.ndarray, n: int) -> tuple[tuple[int, ...], bool]:
    if rule == "discrete":
        return discrete_mode_report(p, n)
    if rule == "quadratic":
        return quadratic_projection_report(p, n)
    if rule == "manhattan":
        return manhattan_report(p, n)
    raise ValueError(rule)


def metric_for_rule(rule: str, p: np.ndarray, n: int, bounds: BoundComputer) -> RuleMetric:
    k = len(p)
    r, tie = report_for_rule(rule, p, n)
    b = bounds.bounds(rule, r, n, k)
    payment = multinomial_pmf_stable(r, p) if rule == "discrete" else math.nan
    return RuleMetric(
        report=r,
        tie=tie,
        coord_avg=average_width(b.coord),
        coord_max=max_width(b.coord),
        mean_linear_width=interval_width(b.mean_linear),
        mean_skewed_width=interval_width(b.mean_skewed),
        payment_probability=payment,
        method=b.method,
    )


def update_aggregate(store: dict, key: tuple, metric: RuleMetric) -> None:
    entry = store[key]
    entry["coord_avg"].append(metric.coord_avg)
    entry["coord_max"].append(metric.coord_max)
    entry["mean_linear"].append(metric.mean_linear_width)
    entry["mean_skewed"].append(metric.mean_skewed_width)
    entry["tie"].append(float(metric.tie))
    if not math.isnan(metric.payment_probability):
        entry["payment"].append(metric.payment_probability)


def split_winner_credit(values: dict[str, float], tol: float = 1e-12) -> dict[str, float]:
    best = min(values.values())
    winners = [rule for rule, val in values.items() if abs(val - best) <= tol]
    credit = 1.0 / len(winners)
    return {rule: (credit if rule in winners else 0.0) for rule in values}


def run_latent_simulation(
    n_values: Iterable[int],
    k_values: Iterable[int],
    alpha_values: Iterable[float],
    draws: int,
    seed: int,
    tolerance: float,
    draw_writer: csv.DictWriter | None = None,
) -> tuple[list[dict], list[dict]]:
    rng = np.random.default_rng(seed)
    bounds = BoundComputer(tolerance=tolerance)
    aggregate: dict[tuple[int, int, float, str], dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    wins: dict[tuple[int, int, float, str, str], float] = defaultdict(float)

    metrics = ("coord_avg", "coord_max", "mean_linear", "mean_skewed")
    draw_id = 0
    for k in k_values:
        for n in n_values:
            for alpha in alpha_values:
                for _ in range(draws):
                    draw_id += 1
                    p = rng.dirichlet(np.full(k, alpha, dtype=float))
                    per_rule = {rule: metric_for_rule(rule, p, n, bounds) for rule in RULES}
                    for rule, metric in per_rule.items():
                        update_aggregate(aggregate, (n, k, alpha, rule), metric)
                        if draw_writer is not None:
                            draw_writer.writerow(
                                {
                                    "draw_id": draw_id,
                                    "n": n,
                                    "k": k,
                                    "alpha": alpha,
                                    "rule": RULE_LABELS[rule],
                                    "p": "(" + ",".join(f"{v:.8f}" for v in p) + ")",
                                    "report": report_to_string(metric.report),
                                    "tie": int(metric.tie),
                                    "avg_coord_width": metric.coord_avg,
                                    "max_coord_width": metric.coord_max,
                                    "mean_linear_width": metric.mean_linear_width,
                                    "mean_skewed_width": metric.mean_skewed_width,
                                    "payment_probability": "" if math.isnan(metric.payment_probability) else metric.payment_probability,
                                    "method": metric.method,
                                }
                            )
                    values = {
                        "coord_avg": {rule: m.coord_avg for rule, m in per_rule.items()},
                        "coord_max": {rule: m.coord_max for rule, m in per_rule.items()},
                        "mean_linear": {rule: m.mean_linear_width for rule, m in per_rule.items()},
                        "mean_skewed": {rule: m.mean_skewed_width for rule, m in per_rule.items()},
                    }
                    for metric_name in metrics:
                        for rule, credit in split_winner_credit(values[metric_name]).items():
                            wins[(n, k, alpha, metric_name, rule)] += credit

    aggregate_rows = []
    for (n, k, alpha, rule), vals in sorted(aggregate.items()):
        row = {
            "n": n,
            "k": k,
            "alpha": alpha,
            "rule": RULE_LABELS[rule],
            "draws": len(vals["coord_avg"]),
            "avg_coord_width_mean": float(np.mean(vals["coord_avg"])),
            "avg_coord_width_median": float(median(vals["coord_avg"])),
            "max_coord_width_mean": float(np.mean(vals["coord_max"])),
            "max_coord_width_median": float(median(vals["coord_max"])),
            "mean_linear_width_mean": float(np.mean(vals["mean_linear"])),
            "mean_linear_width_median": float(median(vals["mean_linear"])),
            "mean_skewed_width_mean": float(np.mean(vals["mean_skewed"])),
            "mean_skewed_width_median": float(median(vals["mean_skewed"])),
            "tie_rate": float(np.mean(vals["tie"])),
            "payment_probability_mean": float(np.mean(vals["payment"])) if vals["payment"] else math.nan,
            "payment_probability_median": float(median(vals["payment"])) if vals["payment"] else math.nan,
        }
        aggregate_rows.append(row)

    win_rows = []
    for n in n_values:
        for k in k_values:
            for alpha in alpha_values:
                for metric_name in metrics:
                    total = draws
                    for rule in RULES:
                        win_rows.append(
                            {
                                "n": n,
                                "k": k,
                                "alpha": alpha,
                                "metric": metric_name,
                                "rule": RULE_LABELS[rule],
                                "win_share": wins[(n, k, alpha, metric_name, rule)] / total,
                            }
                        )
    return aggregate_rows, win_rows


def fixed_report_rows(reports: list[tuple[int, int, tuple[int, ...]]], tolerance: float) -> list[dict]:
    bounds = BoundComputer(tolerance=tolerance)
    rows = []
    for n, k, r in reports:
        p_report = np.array(r, dtype=float) / n
        for rule in RULES:
            b = bounds.bounds(rule, r, n, k)
            payment = multinomial_pmf_stable(r, p_report) if rule == "discrete" else math.nan
            rows.append(
                {
                    "n": n,
                    "k": k,
                    "report": report_to_string(r),
                    "rule": RULE_LABELS[rule],
                    "coordinate_intervals": "; ".join(fmt_interval(iv) for iv in b.coord),
                    "avg_coord_width": average_width(b.coord),
                    "max_coord_width": max_width(b.coord),
                    "mean_linear_interval": fmt_interval(b.mean_linear),
                    "mean_linear_width": interval_width(b.mean_linear),
                    "mean_skewed_interval": fmt_interval(b.mean_skewed),
                    "mean_skewed_width": interval_width(b.mean_skewed),
                    "payment_probability_at_report_share": "" if math.isnan(payment) else payment,
                    "method": b.method,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows and fieldnames is None:
        raise ValueError(f"No rows and no fieldnames for {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames or list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    return [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
        *["| " + " | ".join(row) + " |" for row in rows],
    ]


def make_summary_md(
    mode: str,
    aggregate_rows: list[dict],
    win_rows: list[dict],
    fixed_rows: list[dict],
    draws: int,
    seed: int,
    tolerance: float,
) -> str:
    lines = [
        "# Simulation Results Summary",
        "",
        "Generated by `scripts/design_efficiency.py`; current project status is summarized in `_context/current_status.md`.",
        "",
        "## Configuration",
        "",
        f"- Mode: `{mode}`.",
        f"- Draws per cell: `{draws}`.",
        f"- Random seed: `{seed}`.",
        f"- Manhattan threshold tolerance: `{tolerance:g}`.",
        "- Headline rules: discrete metric, quadratic distance, Manhattan distance.",
        "- Hamming and Chebyshev are not included in headline rankings.",
        "",
        "## Overall Averages Across Cells",
        "",
    ]

    by_rule: dict[str, list[dict]] = defaultdict(list)
    for row in aggregate_rows:
        by_rule[row["rule"]].append(row)
    overall = []
    for rule, rows in by_rule.items():
        overall.append(
            [
                rule,
                fmt_float(float(np.mean([r["avg_coord_width_mean"] for r in rows])), 4),
                fmt_float(float(np.mean([r["max_coord_width_mean"] for r in rows])), 4),
                fmt_float(float(np.mean([r["mean_linear_width_mean"] for r in rows])), 4),
                fmt_float(float(np.mean([r["mean_skewed_width_mean"] for r in rows])), 4),
                fmt_float(float(np.mean([r["tie_rate"] for r in rows])), 4),
            ]
        )
    lines += markdown_table(
        ["Rule", "avg coord", "max coord", "linear mean", "skewed mean", "tie rate"],
        overall,
    )

    lines += ["", "## Rule-Win Shares Across Cells", ""]
    by_metric_rule: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in win_rows:
        by_metric_rule[(row["metric"], row["rule"])].append(float(row["win_share"]))
    win_table = []
    for metric_name in ("coord_avg", "coord_max", "mean_linear", "mean_skewed"):
        for rule in [RULE_LABELS[r] for r in RULES]:
            vals = by_metric_rule[(metric_name, rule)]
            win_table.append([metric_name, rule, fmt_float(float(np.mean(vals)), 4)])
    lines += markdown_table(["Metric", "Rule", "mean win share"], win_table)

    lines += ["", "## Fixed-Report Illustrations", ""]
    fixed_table = []
    for row in fixed_rows:
        fixed_table.append(
            [
                f"n={row['n']}, k={row['k']}, r={row['report']}",
                row["rule"],
                fmt_float(float(row["avg_coord_width"]), 4),
                row["mean_linear_interval"],
                str(row["payment_probability_at_report_share"]),
                row["method"],
            ]
        )
    lines += markdown_table(
        ["Report", "Rule", "avg coord width", "mean interval", "payment prob.", "method"],
        fixed_table,
    )

    lines += [
        "",
        "## Interpretation Guardrails",
        "",
        "- These are design diagnostics conditional on optimal reporting and the stated belief environments.",
        "- They do not establish universal dominance of any scoring rule.",
        "- Manhattan entries are threshold-computed and should not be described as closed form.",
        "- Mean intervals use the full inverse region; they are not obtained by combining coordinate intervals.",
    ]
    return "\n".join(lines)


def validate_report_generators() -> list[str]:
    messages: list[str] = []
    failures = 0
    checks = 0
    for n, k, denom in [(3, 2, 6), (3, 3, 5), (4, 3, 5)]:
        for grid_counts in feasible_reports(denom, k):
            p = np.array(grid_counts, dtype=float) / denom
            if np.any(p == 0.0):
                # Exact enumeration has many boundary ties; the generators are
                # still valid, but interior grids are the useful smoke test.
                continue
            checks += 1
            r, _ = discrete_mode_report(p, n)
            if r not in exact_modes(p, n, k):
                failures += 1
                messages.append(f"discrete mismatch n={n}, k={k}, p={p}, r={r}, opt={exact_modes(p,n,k)}")
            r, _ = quadratic_projection_report(p, n)
            if r not in squared_projection_optima(p, n, k):
                failures += 1
                messages.append(f"quadratic mismatch n={n}, k={k}, p={p}, r={r}, opt={squared_projection_optima(p,n,k)}")
            r, _ = manhattan_report(p, n)
            if r not in l1_separable_optima(p, n, k):
                failures += 1
                messages.append(f"manhattan mismatch n={n}, k={k}, p={p}, r={r}, opt={l1_separable_optima(p,n,k)}")

        for report in feasible_reports(n, k):
            q_cf = squared_closed_form_bounds(report, n, k)
            q_lp, _ = squared_lp_bounds(report, n, k)
            checks += len(q_cf)
            for cf, lp in zip(q_cf, q_lp):
                if abs(cf[0] - lp[0]) > 1e-8 or abs(cf[1] - lp[1]) > 1e-8:
                    failures += 1
                    messages.append(f"quadratic bounds mismatch n={n}, k={k}, r={report}, cf={cf}, lp={lp}")

    if failures == 0:
        messages.insert(0, f"validation passed ({checks} checks)")
    else:
        messages.insert(0, f"validation FAILED ({failures} failures over {checks} checks)")
    return messages


def mode_grid(args: argparse.Namespace) -> tuple[str, list[int], list[int], list[float], int]:
    if args.smoke:
        return "smoke", [5], [2, 3], [1.0], args.draws or 50
    if args.final:
        return "final", [5, 10, 20, 50], [2, 3, 5, 10], [0.1, 0.3, 1.0, 3.0, 10.0], args.draws or 5000
    return "pilot", [5, 10, 20], [2, 3, 5], [0.3, 1.0, 3.0], args.draws or 1000


def default_fixed_reports() -> list[tuple[int, int, tuple[int, ...]]]:
    return [
        (10, 3, (5, 3, 2)),
        (2, 3, (1, 1, 0)),
        (20, 5, (10, 4, 3, 2, 1)),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true", help="Run a tiny smoke test.")
    parser.add_argument("--pilot", action="store_true", help="Run the pilot grid (default).")
    parser.add_argument("--final", action="store_true", help="Run the final grid.")
    parser.add_argument("--draws", type=int, default=None, help="Override draws per cell.")
    parser.add_argument("--seed", type=int, default=20260508)
    parser.add_argument("--manhattan-tolerance", type=float, default=1e-4)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/simulation_design"))
    parser.add_argument("--summary-path", type=Path, default=Path("_context/simulation_results_summary.md"))
    parser.add_argument("--save-draws", action="store_true", help="Save draw-level rows.")
    parser.add_argument("--validate", action="store_true", help="Run small brute-force validation checks first.")
    args = parser.parse_args()

    if args.validate:
        for message in validate_report_generators():
            print(message)

    mode, n_values, k_values, alpha_values, draws = mode_grid(args)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    draw_file = None
    draw_writer = None
    if args.save_draws:
        draw_file = (args.output_dir / "draw_level.csv").open("w", newline="")
        draw_writer = csv.DictWriter(
            draw_file,
            fieldnames=[
                "draw_id",
                "n",
                "k",
                "alpha",
                "rule",
                "p",
                "report",
                "tie",
                "avg_coord_width",
                "max_coord_width",
                "mean_linear_width",
                "mean_skewed_width",
                "payment_probability",
                "method",
            ],
        )
        draw_writer.writeheader()

    try:
        aggregate_rows, win_rows = run_latent_simulation(
            n_values=n_values,
            k_values=k_values,
            alpha_values=alpha_values,
            draws=draws,
            seed=args.seed,
            tolerance=args.manhattan_tolerance,
            draw_writer=draw_writer,
        )
    finally:
        if draw_file is not None:
            draw_file.close()

    fixed_rows = fixed_report_rows(default_fixed_reports(), tolerance=args.manhattan_tolerance)

    write_csv(args.output_dir / "latent_aggregate.csv", aggregate_rows)
    write_csv(args.output_dir / "rule_wins.csv", win_rows)
    write_csv(args.output_dir / "fixed_reports.csv", fixed_rows)
    args.summary_path.parent.mkdir(parents=True, exist_ok=True)
    args.summary_path.write_text(
        make_summary_md(
            mode=mode,
            aggregate_rows=aggregate_rows,
            win_rows=win_rows,
            fixed_rows=fixed_rows,
            draws=draws,
            seed=args.seed,
            tolerance=args.manhattan_tolerance,
        )
    )

    print(f"mode={mode}")
    print(f"wrote {args.output_dir / 'latent_aggregate.csv'}")
    print(f"wrote {args.output_dir / 'rule_wins.csv'}")
    print(f"wrote {args.output_dir / 'fixed_reports.csv'}")
    print(f"wrote {args.summary_path}")


if __name__ == "__main__":
    main()
