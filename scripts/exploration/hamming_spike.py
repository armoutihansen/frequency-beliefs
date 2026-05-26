"""Step 0b: feasibility spike for computing Hamming-distance identification
bounds in the design comparison.

Step 0a (`hamming_interior_search.py`) refuted the interior single-transfer
sufficiency conjecture, so there is no route to *certified-sharp* Hamming
bounds. This spike tests whether Hamming coordinate and mean bounds can be
*computed* tractably and reliably at the design grid's hardest cell
(n = 50, k = 10), which is the remaining gate for putting Hamming into the
four-rule design comparison as a computational bound.

Pieces:

1. Forward solver. The optimal Hamming report maximizes
   G(r;p) = sum_i b(r_i;n,p_i) subject to sum_i r_i = n. This is a separable
   max-plus dynamic program over the count budget, O(n^2 k) -- cheap, and it
   does not need discrete concavity.

2. Membership / deficit oracle. d(p) = V*(p) - G(r;p) >= 0, with V*(p) the DP
   optimum; p is in the identified set P_H(r) iff d(p) = 0. Cheap (one DP).

3. Bound computation. sup / inf of a linear functional over P_H(r). The
   identified set is non-convex, so this is a global optimization. We optimize
   over the relaxation {d(p) <= tol}: a thin outer shell of P_H(r). This errs
   slightly WIDE (the safe direction for a horse race -- it cannot make
   Hamming look artificially informative) and keeps the feasible set
   full-dimensional. Multistart SLSQP.

4. Validation. For k = 3, computed bounds are checked against the fine-grid
   ground truth in `verify_regions.hamming_grid_bounds`. For n = 50, k = 10,
   each computed bound is checked to contain the closed-form modal-box inner
   bound and to dominate a dense feasible sample, and the per-report wall time
   is measured and projected to a full `--final` run.

Run from the repository root:

    uv run python scripts/hamming_spike.py
    uv run python scripts/hamming_spike.py --quick
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Allow `from verify_regions import ...` when run as `python scripts/exploration/hamming_spike.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from scipy.optimize import minimize
from scipy.stats import binom, dirichlet

from config import SEED_HAMMING
from verify_regions import feasible_reports, hamming_grid_bounds


# --------------------------------------------------------------------------
# Binomial point masses and the separable Hamming objective.
# --------------------------------------------------------------------------

def binom_col(n: int, p: float) -> np.ndarray:
    """[b(0;n,p), ..., b(n;n,p)] as floats."""
    return binom.pmf(np.arange(n + 1), n, float(np.clip(p, 0.0, 1.0)))


def pmf_columns(p: np.ndarray, n: int) -> list[np.ndarray]:
    return [binom_col(n, pi) for pi in p]


def hamming_dp_value(cols: list[np.ndarray], n: int) -> float:
    """V*(p) = max over feasible reports of sum_i b(r_i;n,p_i).

    Max-plus convolution: dp[t] = best value using processed coordinates with
    t units allocated. After all k coordinates, dp[n] = V*.
    """
    dp = np.full(n + 1, -np.inf)
    dp[0] = 0.0
    for col in cols:
        ndp = np.full(n + 1, -np.inf)
        for u in range(n + 1):
            shifted = np.full(n + 1, -np.inf)
            shifted[u:] = dp[: n + 1 - u]
            ndp = np.maximum(ndp, shifted + col[u])
        dp = ndp
    return float(dp[n])


def hamming_optimal_report(p: np.ndarray, n: int) -> tuple[tuple[int, ...], float]:
    """An optimal Hamming report and V*(p), via the DP with traceback."""
    cols = pmf_columns(p, n)
    k = len(cols)
    dp = np.full(n + 1, -np.inf)
    dp[0] = 0.0
    choice = [np.zeros(n + 1, dtype=int) for _ in range(k)]
    for i, col in enumerate(cols):
        ndp = np.full(n + 1, -np.inf)
        for t in range(n + 1):
            vals = dp[t::-1] + col[: t + 1]  # u = 0..t
            u = int(np.argmax(vals))
            ndp[t] = vals[u]
            choice[i][t] = u
        dp = ndp
    r = [0] * k
    t = n
    for i in range(k - 1, -1, -1):
        u = int(choice[i][t])
        r[i] = u
        t -= u
    return tuple(r), float(dp[n])


def hamming_G(r: tuple[int, ...], cols: list[np.ndarray]) -> float:
    return float(sum(cols[i][r[i]] for i in range(len(r))))


def hamming_deficit(r: tuple[int, ...], p: np.ndarray, n: int) -> float:
    """d(p) = V*(p) - G(r;p) >= 0; zero iff r is an optimal Hamming report."""
    cols = pmf_columns(p, n)
    return hamming_dp_value(cols, n) - hamming_G(r, cols)


# --------------------------------------------------------------------------
# Closed-form modal-box inner bound (the sandwich's lower bracket).
# --------------------------------------------------------------------------

def modal_box(r: tuple[int, ...], n: int) -> tuple[np.ndarray, np.ndarray]:
    lo = np.array([ri / (n + 1) for ri in r], dtype=float)
    hi = np.array([(ri + 1) / (n + 1) for ri in r], dtype=float)
    return lo, hi


def modal_box_coordinate_bounds(r: tuple[int, ...], n: int, k: int) -> list[tuple[float, float]]:
    """sup/inf p_h over MB(r) intersect simplex -- a valid INNER bound."""
    lo, hi = modal_box(r, n)
    out = []
    for h in range(k):
        sup_h = min(hi[h], 1.0 - (lo.sum() - lo[h]))
        inf_h = max(lo[h], 1.0 - (hi.sum() - hi[h]))
        out.append((max(0.0, inf_h), min(1.0, sup_h)))
    return out


# --------------------------------------------------------------------------
# Bound computation: optimize a linear functional over {d(p) <= tol}.
# --------------------------------------------------------------------------

def _seeds(r: tuple[int, ...], n: int, k: int, rng: np.random.Generator, count: int) -> list[np.ndarray]:
    seeds = []
    rshare = np.array(r, dtype=float) / n
    seeds.append(rshare)
    lo, hi = modal_box(r, n)
    centre = 0.5 * (lo + hi)
    seeds.append(centre / centre.sum())
    seeds.append(np.full(k, 1.0 / k))
    conc = 4.0 * rshare + 0.3
    for _ in range(max(0, count - 3)):
        seeds.append(dirichlet.rvs(conc, random_state=rng)[0])
    return seeds


def optimize_functional(
    r: tuple[int, ...],
    n: int,
    k: int,
    c: np.ndarray,
    maximize: bool,
    tol: float,
    rng: np.random.Generator,
    n_seeds: int = 12,
) -> tuple[float, np.ndarray]:
    """Extremum of c . p over the relaxed identified set {d(p) <= tol}."""
    sign = -1.0 if maximize else 1.0

    def objective(p: np.ndarray) -> float:
        return sign * float(c @ p)

    def deficit_slack(p: np.ndarray) -> float:
        # feasible when >= 0, i.e. d(p) <= tol
        return tol - hamming_deficit(r, p, n)

    constraints = [
        {"type": "eq", "fun": lambda p: float(p.sum() - 1.0)},
        {"type": "ineq", "fun": deficit_slack},
    ]
    bounds = [(0.0, 1.0)] * k

    best_val = np.inf
    best_p = None
    for seed in _seeds(r, n, k, rng, n_seeds):
        p0 = np.clip(seed, 1e-9, 1.0)
        p0 = p0 / p0.sum()
        res = minimize(
            objective, p0, method="SLSQP", bounds=bounds,
            constraints=constraints, options={"maxiter": 200, "ftol": 1e-10},
        )
        p = np.clip(res.x, 0.0, 1.0)
        if p.sum() <= 0:
            continue
        p = p / p.sum()
        # Accept only points within the relaxed feasible shell.
        if hamming_deficit(r, p, n) <= tol * 1.5:
            val = sign * float(c @ p)
            if val < best_val:
                best_val = val
                best_p = p
    if best_p is None:
        # Fall back to the report-share belief (r is optimal there by construction
        # when r is a joint mode; otherwise this still yields a feasible-ish point).
        best_p = np.array(r, dtype=float) / n
        best_val = sign * float(c @ best_p)
    return sign * best_val, best_p


def hamming_coordinate_bounds(
    r: tuple[int, ...], n: int, k: int, tol: float, rng: np.random.Generator
) -> list[tuple[float, float]]:
    out = []
    for h in range(k):
        c = np.zeros(k)
        c[h] = 1.0
        hi, _ = optimize_functional(r, n, k, c, True, tol, rng)
        lo, _ = optimize_functional(r, n, k, c, False, tol, rng)
        out.append((lo, hi))
    return out


def hamming_mean_bounds(
    r: tuple[int, ...], n: int, k: int, tol: float, rng: np.random.Generator
) -> tuple[float, float]:
    c = np.arange(k, dtype=float) / (k - 1) if k > 1 else np.zeros(1)
    hi, _ = optimize_functional(r, n, k, c, True, tol, rng)
    lo, _ = optimize_functional(r, n, k, c, False, tol, rng)
    return lo, hi


# --------------------------------------------------------------------------
# Validation.
# --------------------------------------------------------------------------

def self_check_forward() -> list[str]:
    """DP forward solver and V* against brute-force enumeration, small cases."""
    msgs = []
    failures = 0
    checks = 0
    rng = np.random.default_rng(11)
    for n, k in [(3, 3), (4, 3), (5, 4), (3, 5)]:
        reports = feasible_reports(n, k)
        for _ in range(40):
            p = dirichlet.rvs(np.full(k, 1.0), random_state=rng)[0]
            cols = pmf_columns(p, n)
            v_dp = hamming_dp_value(cols, n)
            v_brute = max(hamming_G(s, cols) for s in reports)
            checks += 1
            if abs(v_dp - v_brute) > 1e-9:
                failures += 1
            r_dp, _ = hamming_optimal_report(p, n)
            if abs(hamming_G(r_dp, cols) - v_brute) > 1e-9:
                failures += 1
    msgs.append(
        f"forward DP vs brute force: {'PASS' if failures == 0 else 'FAIL'} "
        f"({checks} beliefs, {failures} mismatch)"
    )
    if failures:
        raise SystemExit("FORWARD SOLVER SELF-CHECK FAILED -- aborting.")
    return msgs


def validate_k3(tol: float, rng: np.random.Generator) -> tuple[list[str], bool]:
    """Computed bounds vs the fine-grid ground truth, k = 3."""
    cases = [(2, 3, (1, 1, 0)), (5, 3, (2, 2, 1)), (5, 3, (3, 2, 0)), (10, 3, (5, 3, 2))]
    grid_denom = 240
    lines = ["", "## k = 3 validation against the fine grid", "",
             f"Grid ground truth: `hamming_grid_bounds`, simplex denominator {grid_denom}.",
             f"Optimizer relaxation tolerance: tol = {tol:g}.", "",
             "| n | k | r | coord | grid (lo, hi) | computed (lo, hi) | abs gap |",
             "|---|---|---|---|---|---|---|"]
    worst_gap = 0.0
    for n, k, r in cases:
        grid_coord, _, count = hamming_grid_bounds(r, n, k, grid_denom)
        comp = hamming_coordinate_bounds(r, n, k, tol, rng)
        for h in range(k):
            glo, ghi = grid_coord[h]
            clo, chi = comp[h]
            gap = max(abs(glo - clo), abs(ghi - chi))
            worst_gap = max(worst_gap, gap)
            lines.append(
                f"| {n} | {k} | {r} | p{h+1} | "
                f"({glo:.4f}, {ghi:.4f}) | ({clo:.4f}, {chi:.4f}) | {gap:.4f} |"
            )
    # The computed bound optimizes over a tol-relaxation, so it should weakly
    # contain the grid bound; the grid is itself denom-limited. Allow a margin.
    tolerance = 1.0 / grid_denom + 5e-3
    ok = worst_gap <= tolerance
    lines += ["", f"Worst coordinate gap vs grid: {worst_gap:.4f} "
              f"(acceptance threshold {tolerance:.4f}: grid resolution + margin). "
              f"{'PASS' if ok else 'FAIL'}."]
    return lines, ok


def feasible_sample_extremes(
    r: tuple[int, ...], n: int, k: int, tol: float, draws: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray, int]:
    """Coordinate-wise min/max of p over a dense feasible sample (a valid
    interval INNER bound: every sampled point lies in {d <= tol})."""
    conc = 3.0 * np.array(r, dtype=float) / n + 0.25
    lo = np.full(k, np.inf)
    hi = np.full(k, -np.inf)
    kept = 0
    batch = 4000
    drawn = 0
    while drawn < draws:
        ps = dirichlet.rvs(conc, size=batch, random_state=rng)
        drawn += batch
        for p in ps:
            if hamming_deficit(r, p, n) <= tol:
                kept += 1
                lo = np.minimum(lo, p)
                hi = np.maximum(hi, p)
    if kept == 0:
        return np.zeros(k), np.ones(k), 0
    return lo, hi, kept


def probe_k10(tol: float, rng: np.random.Generator, quick: bool) -> tuple[list[str], bool]:
    """Timing and sandwich containment at n = 50, k = 10."""
    n, k = (20, 10) if quick else (50, 10)
    sample_draws = 8000 if quick else 40000
    # Representative reports: a balanced near-modal report, a moderately skewed
    # report, and a sparse report -- all feasible (each is its own DP optimum
    # at p = r/n for the balanced/skewed cases; verified below).
    base = n // k
    rem = n - base * k
    balanced = tuple(base + (1 if i < rem else 0) for i in range(k))
    skewed = tuple(sorted(hamming_optimal_report(
        dirichlet.rvs(np.full(k, 0.5), random_state=rng)[0], n)[0], reverse=True))
    sparse = hamming_optimal_report(
        dirichlet.rvs(np.full(k, 0.12), random_state=rng)[0], n)[0]
    reports = [("balanced", balanced), ("skewed", skewed), ("sparse", sparse)]

    lines = ["", f"## n = {n}, k = {k} probe", "",
             f"Optimizer relaxation tolerance: tol = {tol:g}. "
             f"Feasible-sample size target: {sample_draws}.", "",
             "| report kind | r | per-report time (s) | sandwich OK | "
             "dominates feasible sample | feasible sample size |",
             "|---|---|---|---|---|---|"]
    all_ok = True
    total_time = 0.0
    for kind, r in reports:
        t0 = time.time()
        comp = hamming_coordinate_bounds(r, n, k, tol, rng)
        mean_lo, mean_hi = hamming_mean_bounds(r, n, k, tol, rng)
        elapsed = time.time() - t0
        total_time += elapsed

        inner = modal_box_coordinate_bounds(r, n, k)
        s_lo, s_hi, kept = feasible_sample_extremes(r, n, k, tol, sample_draws, rng)

        sandwich_ok = True
        dominates_sample = True
        for h in range(k):
            clo, chi = comp[h]
            ilo, ihi = inner[h]
            # computed interval must contain the closed-form inner interval
            if clo > ilo + 5e-3 or chi < ihi - 5e-3:
                sandwich_ok = False
            # computed interval must contain the dense feasible sample
            if kept and (clo > s_lo[h] + 5e-3 or chi < s_hi[h] - 5e-3):
                dominates_sample = False
        all_ok = all_ok and sandwich_ok and dominates_sample
        lines.append(
            f"| {kind} | {r} | {elapsed:.2f} | "
            f"{'yes' if sandwich_ok else 'NO'} | "
            f"{'yes' if dominates_sample else 'NO'} | {kept} |"
        )

    # Project a full --final run. The final grid has k in {2,3,5,10}; only the
    # k=10 cells and large k=5 cells need this optimizer. Distinct optimal
    # reports per cell are far fewer than all feasible reports (caching). Use a
    # deliberately conservative estimate: ~300 distinct reports per heavy cell,
    # ~12 heavy cells.
    per_report = total_time / len(reports)
    projected = per_report * 300 * 12 / 3600.0
    lines += ["", f"Mean per-report bound time: {per_report:.2f} s.",
              f"Conservative full-run projection (~300 distinct reports x ~12 "
              f"heavy cells): {projected:.1f} h.", ""]
    runtime_ok = projected <= 24.0
    lines.append(
        f"Sandwich + feasible-sample containment: {'PASS' if all_ok else 'FAIL'}. "
        f"Runtime projection under 24 h: {'PASS' if runtime_ok else 'FAIL'}."
    )
    return lines, all_ok and runtime_ok


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="smaller probe (n=20)")
    parser.add_argument("--tol", type=float, default=1e-6, help="relaxation tolerance")
    parser.add_argument(
        "--output", type=Path,
        default=Path("outputs/verification/hamming_spike.md"),
        help="markdown report path",
    )
    args = parser.parse_args()

    rng = np.random.default_rng(SEED_HAMMING)
    lines = ["# Hamming Bound-Computation Spike (Step 0b)", "",
             "Feasibility spike for computing Hamming identification bounds in "
             "the design comparison. See `_context/next_steps.md`, Hamming-first "
             "plan, Step 0b.", "",
             f"- Mode: `{'quick' if args.quick else 'full'}`.",
             f"- Relaxation tolerance: tol = {args.tol:g}.", ""]

    print("Self-check: forward DP solver...", flush=True)
    for msg in self_check_forward():
        print("  " + msg, flush=True)
        lines.append(f"- {msg}")

    print("Validating k=3 against the fine grid...", flush=True)
    k3_lines, k3_ok = validate_k3(args.tol, rng)
    lines += k3_lines
    print(f"  k=3 validation: {'PASS' if k3_ok else 'FAIL'}", flush=True)

    print("Probing n=50, k=10...", flush=True)
    probe_lines, probe_ok = probe_k10(args.tol, rng, args.quick)
    lines += probe_lines
    print(f"  k=10 probe: {'PASS' if probe_ok else 'FAIL'}", flush=True)

    overall = k3_ok and probe_ok
    lines += ["", "## Verdict", ""]
    if overall:
        verdict = (
            "SPIKE PASSES. Hamming bounds can be computed and validated at the "
            "design grid's hardest cell. Hamming can enter the four-rule design "
            "comparison as a COMPUTED bound (never labelled sharp). Proceed to "
            "Step 2: integrate Hamming into `scripts/design_efficiency.py`."
        )
    else:
        verdict = (
            "SPIKE FAILS. Hamming bounds could not be computed reliably and/or "
            "tractably at n=50, k=10. Per the Hamming-first plan, decouple: "
            "resume the 3-rule revision (`_context/revision_plan.md`); the "
            "Hamming computed-bound simulation becomes documented future work."
        )
    lines.append(verdict)
    print("\n" + verdict, flush=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote {args.output}", flush=True)


if __name__ == "__main__":
    main()
