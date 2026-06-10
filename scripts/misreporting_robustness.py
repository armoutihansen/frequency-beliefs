"""Misreporting robustness exercise (paper-1 task P1).

Implements the approved design in `_context/misreporting_robustness_plan.md`
(simulation-methodologist review: GO-WITH-CHANGES, changes incorporated).

For each design cell, latent beliefs p ~ Dirichlet(alpha) are drawn, each
rule's optimal report is computed, and the report is perturbed by
single-count transfers under two stipulated error models:

  center_bias    move one count from the largest-count coordinate to the
                 smallest (seeded tie-breaks); NO-OP when
                 max(r) - min(r) <= 1 (oscillation fix); effective
                 transfers t_eff are recorded.
  uniform_error  move one count from a uniformly random positive
                 coordinate to a uniformly random other coordinate.

Reported per (cell, rule, model, t in {0,1,2}): identified-set coverage of
the true belief (membership via the exact single-transfer/exchange tests),
paired coverage drops, claimed-precision widths on a bounds subsample, an
outer-box violation proxy among non-covered draws, and survival summaries
(T = first exit step, censored at t_max = n).

This is a sensitivity analysis of the identification machinery under
stipulated perturbation models, NOT behavioral evidence.

Outputs go to `outputs/misreporting/` (never touches
`outputs/design_exercise/` or `outputs/simulation_design/`).

Examples:

    uv run python scripts/misreporting_robustness.py --smoke
    uv run python scripts/misreporting_robustness.py --pilot
    uv run python scripts/misreporting_robustness.py --final --draws 5000
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import subprocess
from collections import defaultdict
from pathlib import Path

import numpy as np

from config import RULE_DISPLAY, SEED_MISREPORTING
from design_efficiency import BoundComputer, RULES, report_for_rule
from utils import average_width, interval_width, max_width
from verify_regions import (
    exact_modes,
    exact_transfer_region,
    feasible_reports,
    l1_exchange_region,
    l1_separable_optima,
    squared_projection_optima,
    squared_transfer_region,
)

SCRIPT_VERSION = "1.0 (2026-06-10)"
MODELS = ("center_bias", "uniform_error")
N_VALUES = (5, 10, 20, 50)
K_VALUES = (2, 3, 5, 10)
ALPHA_VALUES = (0.1, 0.3, 1.0, 3.0, 10.0)
T_BOUNDS = (0, 1, 2)  # intensities at which bounds/coverage rows are emitted


def member(rule: str, r: tuple[int, ...], p: np.ndarray, n: int) -> bool:
    if rule == "discrete":
        return exact_transfer_region(r, p)
    if rule == "quadratic":
        return squared_transfer_region(r, p, n)
    if rule == "manhattan":
        return l1_exchange_region(r, p, n)
    raise ValueError(rule)


def perturb_step(
    r: tuple[int, ...], model: str, rng: np.random.Generator
) -> tuple[tuple[int, ...], bool]:
    """One single-count transfer; returns (new report, moved flag)."""
    k = len(r)
    if model == "center_bias":
        if max(r) - min(r) <= 1:
            return r, False
        mx, mn = max(r), min(r)
        senders = [i for i, x in enumerate(r) if x == mx]
        receivers = [i for i, x in enumerate(r) if x == mn]
        i = senders[int(rng.integers(len(senders)))]
        j = receivers[int(rng.integers(len(receivers)))]
    elif model == "uniform_error":
        senders = [i for i, x in enumerate(r) if x > 0]
        i = senders[int(rng.integers(len(senders)))]
        others = [j for j in range(k) if j != i]
        j = others[int(rng.integers(len(others)))]
    else:
        raise ValueError(model)
    out = list(r)
    out[i] -= 1
    out[j] += 1
    return tuple(out), True


def walk_path(
    r0: tuple[int, ...],
    p: np.ndarray,
    rule: str,
    model: str,
    n: int,
    t_max: int,
    rng: np.random.Generator,
):
    """Follow one perturbation path; returns per-path statistics.

    Returns dict with: reports at t=1,2 (None where frozen), member flags at
    t=1,2, T (first exit; None if censored), censored flag, t_eff over the
    first two steps, displacement at t=1,2 (L1/2 from r0).
    """
    res = {
        "r": {1: None, 2: None},
        "mem": {1: None, 2: None},
        "T": None,
        "censored": False,
        "t_eff2": 0,
        "disp": {1: math.nan, 2: math.nan},
    }
    r = r0
    frozen = False
    for t in range(1, t_max + 1):
        if not frozen:
            r_new, moved = perturb_step(r, model, rng)
            if moved:
                r = r_new
                if t <= 2:
                    res["t_eff2"] += 1
            else:
                frozen = True  # center-bias fixed point: path stops changing
        m = member(rule, r, p, n)
        if t <= 2:
            res["r"][t] = r
            res["mem"][t] = m
            res["disp"][t] = float(np.abs(np.array(r) - np.array(r0)).sum() / 2)
        if res["T"] is None and not m:
            res["T"] = t
        if frozen and res["T"] is None and t >= 2:
            # Path is constant and still covered: censored; flags for t<=2 set.
            break
        if res["T"] is not None and t >= 2:
            break
    if res["T"] is None:
        res["censored"] = True
    # Fill t<=2 entries if the loop broke early (frozen before reaching t).
    for t in (1, 2):
        if res["r"][t] is None:
            res["r"][t] = r
            res["mem"][t] = member(rule, r, p, n)
            res["disp"][t] = float(np.abs(np.array(r) - np.array(r0)).sum() / 2)
    return res


def box_violation(coord: list[tuple[float, float]], p: np.ndarray) -> float:
    return max(max(lo - pi, pi - hi, 0.0) for (lo, hi), pi in zip(coord, p))


def git_hash() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10,
            cwd=Path(__file__).resolve().parent,
        )
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def run_cell(
    n: int, k: int, alpha: float, draws: int, tolerance: float,
    bounds_subsample: int, t_max: int | None, gate_log: list[str],
) -> list[dict]:
    """Simulate one design cell; returns output rows (one per rule/model/t)."""
    t_cap = max(t_max if t_max is not None else n, 2)
    ss = np.random.SeedSequence([SEED_MISREPORTING, n, k, int(round(alpha * 1000))])
    draw_ss, perturb_ss = ss.spawn(2)
    rng_draw = np.random.default_rng(draw_ss)
    rng_pert = np.random.default_rng(perturb_ss)
    bounds = BoundComputer(tolerance=tolerance)

    agg: dict[tuple[str, str], dict] = defaultdict(lambda: {
        "cov": {1: 0, 2: 0},
        "trans": defaultdict(int),          # (m1, m2) joint counts
        "cov_eff": [0, 0],                  # [covered & t_eff>=1, t_eff>=1] at t=1
        "noop": 0,                          # zero effective transfers in 2 steps
        "t_eff_sum": 0,
        "disp_sum": {1: 0.0, 2: 0.0},
        "T_list": [],
        "widths": {t: defaultdict(float) for t in T_BOUNDS},
        "n_sub": 0,
        "noncov_sub": {t: 0 for t in T_BOUNDS},
        "noncov_zeroviol": {t: 0 for t in T_BOUNDS},
    })
    ties = defaultdict(int)
    gate_failures = 0

    for d in range(draws):
        p = rng_draw.dirichlet([alpha] * k)
        in_sub = d < bounds_subsample
        for rule in RULES:
            r0, tie = report_for_rule(rule, p, n)
            ties[rule] += int(tie)
            if not member(rule, r0, p, n):  # t=0 gate: must hold exactly
                gate_failures += 1
                if len(gate_log) < 20:
                    gate_log.append(
                        f"t0-coverage FAIL n={n} k={k} a={alpha} rule={rule} "
                        f"p={np.round(p, 6).tolist()} r={r0}"
                    )
                continue
            sub_bounds = {}
            if in_sub:
                b0 = bounds.bounds(rule, r0, n, k)
                sub_bounds[0] = (r0, b0)
            for model in MODELS:
                a = agg[(rule, model)]
                path = walk_path(r0, p, rule, model, n, t_cap, rng_pert)
                m1, m2 = path["mem"][1], path["mem"][2]
                a["cov"][1] += int(m1)
                a["cov"][2] += int(m2)
                a["trans"][(int(m1), int(m2))] += 1
                if model == "center_bias":
                    a["t_eff_sum"] += path["t_eff2"]
                    if path["t_eff2"] == 0:
                        a["noop"] += 1
                    else:
                        a["cov_eff"][1] += 1
                        a["cov_eff"][0] += int(m1)
                a["disp_sum"][1] += path["disp"][1]
                a["disp_sum"][2] += path["disp"][2]
                a["T_list"].append(math.inf if path["censored"] else path["T"])
                if in_sub:
                    a["n_sub"] += 1
                    for t in T_BOUNDS:
                        rt, bt = (
                            sub_bounds[0] if t == 0
                            else (path["r"][t], bounds.bounds(rule, path["r"][t], n, k))
                        )
                        w = a["widths"][t]
                        w["avg_coord"] += average_width(bt.coord)
                        w["max_coord"] += max_width(bt.coord)
                        w["mean_linear"] += interval_width(bt.mean_linear)
                        w["mean_skewed"] += interval_width(bt.mean_skewed)
                        covered_t = True if t == 0 else bool(path["mem"][t])
                        if not covered_t:
                            a["noncov_sub"][t] += 1
                            if box_violation(bt.coord, p) <= 1e-12:
                                a["noncov_zeroviol"][t] += 1

    rows = []
    gh = git_hash()
    for rule in RULES:
        for model in MODELS:
            a = agg[(rule, model)]
            m = draws
            T_arr = a["T_list"]
            n_paths = len(T_arr)
            censored = sum(1 for T in T_arr if T is math.inf or T == math.inf)
            share_T1 = sum(1 for T in T_arr if T == 1) / max(n_paths, 1)
            finite_sorted = sorted(T_arr)
            med = finite_sorted[n_paths // 2] if n_paths else math.nan
            med_T = math.nan if med == math.inf else float(med)
            for t in T_BOUNDS:
                cov = 1.0 if t == 0 else a["cov"][t] / m
                cov_se = 0.0 if t == 0 else math.sqrt(cov * (1 - cov) / m)
                if t == 0:
                    drop, drop_se = math.nan, math.nan
                elif t == 1:
                    drop = 1.0 - cov
                    drop_se = cov_se
                else:
                    n10 = a["trans"][(1, 0)]
                    n01 = a["trans"][(0, 1)]
                    drop = (n10 - n01) / m
                    var = max((n10 + n01) - (n10 - n01) ** 2 / m, 0.0) / m**2
                    drop_se = math.sqrt(var)
                n_sub = max(a["n_sub"], 1)
                w = a["widths"][t]
                noncov = a["noncov_sub"][t]
                rows.append({
                    "n": n, "k": k, "alpha": alpha,
                    "rule": RULE_DISPLAY[rule], "model": model,
                    "t": t, "t_over_n": t / n, "draws": m,
                    "coverage": round(cov, 6), "coverage_se": round(cov_se, 6),
                    "drop": "" if math.isnan(drop) else round(drop, 6),
                    "drop_se": "" if math.isnan(drop_se) else round(drop_se, 6),
                    "coverage_cond_eff": (
                        round(a["cov_eff"][0] / a["cov_eff"][1], 6)
                        if model == "center_bias" and t == 1 and a["cov_eff"][1] else ""
                    ),
                    "noop_share": (
                        round(a["noop"] / m, 6) if model == "center_bias" else ""
                    ),
                    "mean_t_eff": (
                        round(a["t_eff_sum"] / m, 6) if model == "center_bias" else ""
                    ),
                    "mean_displacement": (
                        round(a["disp_sum"][t] / m, 6)
                        if model == "uniform_error" and t > 0 else ""
                    ),
                    "tie_rate": round(ties[rule] / m, 6),
                    "bounds_subsample": a["n_sub"],
                    "avg_coord_width": round(w["avg_coord"] / n_sub, 6),
                    "max_coord_width": round(w["max_coord"] / n_sub, 6),
                    "mean_linear_width": round(w["mean_linear"] / n_sub, 6),
                    "mean_skewed_width": round(w["mean_skewed"] / n_sub, 6),
                    "noncov_count_sub": noncov,
                    "noncov_zero_boxviol_share": (
                        round(a["noncov_zeroviol"][t] / noncov, 6) if noncov else ""
                    ),
                    "survival_median_T": "" if math.isnan(med_T) else med_T,
                    "survival_share_T1": round(share_T1, 6),
                    "survival_censored_share": round(censored / max(n_paths, 1), 6),
                    "t_max": t_cap,
                    "seed": SEED_MISREPORTING, "tolerance": tolerance,
                    "script_version": SCRIPT_VERSION, "git_hash": gh,
                })
    return rows


def run_smoke() -> bool:
    """Brute-force gates on small cells (plan, validation gates b/e)."""
    print("=== smoke: generator/membership/rationalizability gates ===")
    rng = np.random.default_rng(SEED_MISREPORTING)
    ok = True
    brute = {
        "discrete": exact_modes,
        "quadratic": squared_projection_optima,
        "manhattan": l1_separable_optima,
    }
    for n, k in ((4, 2), (5, 3), (6, 3)):
        reports = feasible_reports(n, k)
        # Rationalizability gate (Manhattan; closed-form rules are immediate).
        for r in reports:
            p = np.array(r, dtype=float) / n
            if not l1_exchange_region(r, p, n):
                ok = False
                print(f"  FAIL rationalizability n={n} k={k} r={r}")
        for alpha in (0.3, 1.0, 3.0):
            for _ in range(60):
                p = rng.dirichlet([alpha] * k)
                for rule in RULES:
                    opt = brute[rule](p, n, k)
                    r0, _tie = report_for_rule(rule, p, n)
                    if r0 not in opt:  # generator gate
                        ok = False
                        print(f"  FAIL generator {rule} n={n} k={k} p={p} r={r0}")
                    for r in reports:  # membership gate
                        if member(rule, r, p, n) != (r in opt):
                            ok = False
                            print(f"  FAIL membership {rule} n={n} k={k} r={r} p={p}")
    print(f"  {'PASS' if ok else 'FAIL'} -- smoke gates")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--draws", type=int, default=None)
    ap.add_argument("--tolerance", type=float, default=1e-4)
    ap.add_argument("--bounds-subsample", type=int, default=250)
    ap.add_argument("--t-max", type=int, default=None,
                    help="Survival censoring cap (default: n per cell).")
    ap.add_argument("--output-dir", type=Path,
                    default=Path(__file__).resolve().parents[1] / "outputs" / "misreporting")
    args = ap.parse_args()

    if args.smoke:
        raise SystemExit(0 if run_smoke() else 1)

    draws = args.draws or (500 if args.pilot else 5000)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / "coverage_aggregate.csv"

    gate_log: list[str] = []
    all_rows: list[dict] = []
    cells = [(n, k, a) for n in N_VALUES for k in K_VALUES for a in ALPHA_VALUES]
    for idx, (n, k, alpha) in enumerate(cells, 1):
        rows = run_cell(n, k, alpha, draws, args.tolerance,
                        args.bounds_subsample, args.t_max, gate_log)
        all_rows.extend(rows)
        print(f"[{idx:>2}/{len(cells)}] n={n} k={k} alpha={alpha} done", flush=True)

    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"wrote {len(all_rows)} rows to {out_path}")
    if gate_log:
        print("t=0 COVERAGE GATE FAILURES (witnesses):")
        for line in gate_log:
            print(" ", line)
        raise SystemExit(1)
    print("t=0 coverage gate: PASS (all draws, all rules, all cells)")


if __name__ == "__main__":
    main()
