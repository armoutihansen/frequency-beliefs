"""One-off consistency checks for the revised manuscript.

(1) Verifies Corollary 1 (average coordinate width of the closed-form rules)
    computationally against the closed-form coordinate bounds in
    verify_regions.py.
(2) Traces the numbers in the manuscript's design-comparison tables back to
    outputs/design_exercise/.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from verify_regions import (
    exact_coordinate_intervals,
    feasible_reports,
    squared_closed_form_bounds,
)

ROOT = Path(__file__).resolve().parents[1]


def w0(n: int, k: int) -> float:
    return (k - 1) * (2 * n + k) / (k * (n + 1) * (n + k - 1))


def wq(m: int, n: int, k: int) -> float:
    return (2 * m - 1 - m / k + m * (k - m) / (m + 1)) / (n * k)


def avg_width(intervals) -> float:
    return sum(hi - lo for lo, hi in intervals) / len(intervals)


def check_corollary() -> None:
    print("=== Check 2: Corollary 1 vs closed-form bounds ===")
    fails = 0
    for k in (2, 3, 5, 10):
        for n in (2, 5, 10, 20):
            const = None
            for r in feasible_reports(n, k):
                # Part (1): discrete average width is the constant W0.
                d_avg = avg_width(exact_coordinate_intervals(r, n, k))
                if abs(d_avg - w0(n, k)) > 1e-9:
                    fails += 1
                    print(f"  FAIL discrete n={n} k={k} r={r}: {d_avg} vs W0={w0(n,k)}")
                if const is None:
                    const = d_avg
                elif abs(d_avg - const) > 1e-12:
                    fails += 1
                    print(f"  FAIL discrete not constant n={n} k={k} r={r}")
                # Part (2): quadratic average width depends only on m and = WQ.
                m = sum(1 for x in r if x > 0)
                q_avg = avg_width(squared_closed_form_bounds(r, n, k))
                if abs(q_avg - wq(m, n, k)) > 1e-9:
                    fails += 1
                    print(f"  FAIL quadratic n={n} k={k} r={r} m={m}: {q_avg} vs WQ={wq(m,n,k)}")
            # Part (3): WQ(1) < W0 < WQ(k).
            if not (wq(1, n, k) < w0(n, k) < wq(k, n, k)):
                fails += 1
                print(f"  FAIL crossover n={n} k={k}: "
                      f"WQ(1)={wq(1,n,k):.5f} W0={w0(n,k):.5f} WQ(k)={wq(k,n,k):.5f}")
    print(f"  {'PASS' if fails == 0 else f'FAIL ({fails})'} -- "
          f"discrete=constant=W0, quadratic=WQ(m), WQ(1)<W0<WQ(k), all (n,k) tested.")


def load_csv(name: str) -> list[dict]:
    with (ROOT / "outputs" / "design_exercise" / name).open() as f:
        return list(csv.DictReader(f))


def check_numbers() -> None:
    print()
    print("=== Check 1: manuscript numbers vs outputs/design_exercise/ ===")
    rc = load_csv("rule_comparison.csv")
    agg = load_csv("latent_aggregate.csv")

    # tab:regime-wins / tab:regime-regret: win share & regret by alpha,
    # averaged over n,k, for metric coord_avg and mean_linear.
    for metric, label in (("coord_avg", "Average-coordinate"), ("mean_linear", "Linear-mean")):
        print(f"  -- win share / regret by alpha, metric={label} --")
        for alpha in ("0.1", "0.3", "1.0", "3.0", "10.0"):
            row = {}
            for rule in ("Discrete metric", "Quadratic distance", "Manhattan distance"):
                ws = [float(x["win_share"]) for x in rc
                      if x["metric"] == metric and x["rule"] == rule
                      and abs(float(x["alpha"]) - float(alpha)) < 1e-9]
                rg = [float(x["mean_regret"]) for x in rc
                      if x["metric"] == metric and x["rule"] == rule
                      and abs(float(x["alpha"]) - float(alpha)) < 1e-9]
                row[rule] = (sum(ws) / len(ws), sum(rg) / len(rg))
            d, q, m = row["Discrete metric"], row["Quadratic distance"], row["Manhattan distance"]
            print(f"    a={alpha:>4}: win {d[0]:.2f} {q[0]:.2f} {m[0]:.2f}   "
                  f"regret {d[1]:.3f} {q[1]:.3f} {m[1]:.3f}")

    # Overall mean coordinate width per rule (paper prose: 0.103, 0.104, 0.102).
    print("  -- overall mean avg-coordinate width per rule (paper: D 0.103, Q 0.104, M 0.102) --")
    for rule in ("Discrete metric", "Quadratic distance", "Manhattan distance"):
        vals = [float(x["avg_coord_width_mean"]) for x in agg if x["rule"] == rule]
        print(f"    {rule:<20}: {sum(vals)/len(vals):.4f}")

    # tab:design-nk: win share by k and by n (metric coord_avg & mean_linear).
    for metric, label in (("coord_avg", "Average-coordinate"), ("mean_linear", "Linear-mean")):
        print(f"  -- win share by k / by n, metric={label} --")
        for dim in ("k", "n"):
            for val in sorted({int(x[dim]) for x in rc}):
                cells = {}
                for rule in ("Discrete metric", "Quadratic distance", "Manhattan distance"):
                    ws = [float(x["win_share"]) for x in rc
                          if x["metric"] == metric and x["rule"] == rule and int(x[dim]) == val]
                    cells[rule] = sum(ws) / len(ws)
                print(f"    {dim}={val:>2}: "
                      f"{cells['Discrete metric']:.2f} {cells['Quadratic distance']:.2f} "
                      f"{cells['Manhattan distance']:.2f}")


if __name__ == "__main__":
    check_corollary()
    check_numbers()
