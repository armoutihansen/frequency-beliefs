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
    exact_lp_mean_bounds,
    feasible_reports,
    l1_median_bound,
    l1_threshold_bounds,
    polytope_median_bound,
    squared_closed_form_bounds,
    squared_lp_bounds,
)
import numpy as np

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


def check_robustness() -> None:
    """Check 3: asymmetric-Dirichlet robustness table (Appendix tab:regime-wins-asymmetric).

    Verifies the win-share triples in the appendix subsection 'Robustness to
    asymmetric beliefs' against outputs/design_exercise/robustness/. Silently
    skips if the robustness output is missing (the main paper tables are
    independent of this check).
    """
    print()
    print("=== Check 3: asymmetric-Dirichlet robustness vs outputs/design_exercise/robustness/ ===")
    rc_path = ROOT / "outputs" / "design_exercise" / "robustness" / "rule_comparison.csv"
    if not rc_path.exists():
        print(f"  SKIP -- {rc_path.relative_to(ROOT)} not found "
              f"(run: uv run python scripts/design_efficiency.py --robustness-only --draws 5000)")
        return
    with rc_path.open() as f:
        rc = list(csv.DictReader(f))

    # Paper appendix table (Table tab:regime-wins-asymmetric) values, to 2 d.p.:
    expected = {
        "one-dominant": {
            "coord_avg":   (0.06, 0.60, 0.33),
            "mean_linear": (0.04, 0.72, 0.24),
        },
        "two-modes": {
            "coord_avg":   (0.03, 0.76, 0.21),
            "mean_linear": (0.04, 0.82, 0.14),
        },
        "graded": {
            "coord_avg":   (0.07, 0.67, 0.26),
            "mean_linear": (0.03, 0.86, 0.11),
        },
        "no-small": {
            "coord_avg":   (0.84, 0.11, 0.05),
            "mean_linear": (0.68, 0.27, 0.05),
        },
    }
    fails = 0
    for label, metrics in expected.items():
        for metric, (e_d, e_q, e_m) in metrics.items():
            d = next(float(r["win_share"]) for r in rc
                     if r["alpha_label"] == label and r["metric"] == metric
                     and r["rule"] == "Discrete metric")
            q = next(float(r["win_share"]) for r in rc
                     if r["alpha_label"] == label and r["metric"] == metric
                     and r["rule"] == "Quadratic distance")
            m = next(float(r["win_share"]) for r in rc
                     if r["alpha_label"] == label and r["metric"] == metric
                     and r["rule"] == "Manhattan distance")
            ok = all(abs(a - b) < 0.01 for a, b in ((d, e_d), (q, e_q), (m, e_m)))
            mark = "OK" if ok else "FAIL"
            if not ok:
                fails += 1
            print(f"  {mark} {label:<13} {metric:<11}: "
                  f"D {d:.2f}(={e_d:.2f}) Q {q:.2f}(={e_q:.2f}) M {m:.2f}(={e_m:.2f})")
    print(f"  {'PASS' if fails == 0 else f'FAIL ({fails})'} -- "
          f"appendix table tab:regime-wins-asymmetric vs CSV.")


def check_functional_menu() -> None:
    """Check 4: Appendix worked-example table for n=10, k=5, r=(2,2,2,2,2), x=(0,1,2,3,4)."""
    print()
    print("=== Check 4: Appendix worked-example functional menu ===")
    n, k = 10, 5
    r = (2, 2, 2, 2, 2)
    x = np.arange(k, dtype=float)
    expected = {
        # Each p_i (symmetric report, all coordinates identical)
        ("coord", "Discrete"):  (0.143, 0.273),
        ("coord", "Squared"):   (0.120, 0.280),
        ("coord", "Manhattan"): (0.129, 0.280),
        # Mean bound
        ("mean",  "Discrete"):  (1.75, 2.25),
        ("mean",  "Squared"):   (1.70, 2.30),
        ("mean",  "Manhattan"): (1.71, 2.29),
        # Median bound (as (x_lo, x_hi))
        ("median","Discrete"):  (1.0, 2.0),
        ("median","Squared"):   (1.0, 3.0),
        ("median","Manhattan"): (1.0, 3.0),
        # 0.25 quantile
        ("q25",   "Discrete"):  (0.0, 1.0),
        ("q25",   "Squared"):   (0.0, 1.0),
        ("q25",   "Manhattan"): (0.0, 1.0),
        # 0.75 quantile
        ("q75",   "Discrete"):  (3.0, 4.0),
        ("q75",   "Squared"):   (3.0, 4.0),
        ("q75",   "Manhattan"): (3.0, 4.0),
    }
    actual = {}
    actual[("coord","Discrete")]  = exact_coordinate_intervals(r, n, k)[0]
    actual[("coord","Squared")]   = squared_closed_form_bounds(r, n, k)[0]
    coord_l1, mean_l1, _          = l1_threshold_bounds(r, n, k, c_denom=4000, x=x)
    actual[("coord","Manhattan")] = coord_l1[0]
    actual[("mean","Discrete")]   = exact_lp_mean_bounds(r, n, k, x)
    _, mean_sq                    = squared_lp_bounds(r, n, k, objective=x)
    actual[("mean","Squared")]    = mean_sq
    actual[("mean","Manhattan")]  = mean_l1
    for rule_key, rule_name in [("exact","Discrete"),("squared","Squared")]:
        b_med, _ = polytope_median_bound(r, n, k, x, rule_key, tau=0.5)
        b_q25, _ = polytope_median_bound(r, n, k, x, rule_key, tau=0.25)
        b_q75, _ = polytope_median_bound(r, n, k, x, rule_key, tau=0.75)
        actual[("median", rule_name)] = b_med
        actual[("q25",    rule_name)] = b_q25
        actual[("q75",    rule_name)] = b_q75
    b_med, _ = l1_median_bound(r, n, k, x, tau=0.5,  c_denom=4000)
    b_q25, _ = l1_median_bound(r, n, k, x, tau=0.25, c_denom=4000)
    b_q75, _ = l1_median_bound(r, n, k, x, tau=0.75, c_denom=4000)
    actual[("median","Manhattan")] = b_med
    actual[("q25",   "Manhattan")] = b_q25
    actual[("q75",   "Manhattan")] = b_q75
    fails = 0
    for key, exp in expected.items():
        act = actual[key]
        ok = abs(exp[0] - act[0]) < 0.01 and abs(exp[1] - act[1]) < 0.01
        if not ok:
            fails += 1
        print(f"  {'OK' if ok else 'FAIL'} {key[0]:<6} {key[1]:<10}: paper={exp}  actual=({act[0]:.3f}, {act[1]:.3f})")
    print(f"  {'PASS' if fails == 0 else f'FAIL ({fails})'} -- Appendix worked-example table tab:functional-menu")


if __name__ == "__main__":
    check_corollary()
    check_numbers()
    check_robustness()
    check_functional_menu()
