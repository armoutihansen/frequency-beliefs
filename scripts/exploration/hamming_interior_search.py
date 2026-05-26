"""Step 0a: exact-arithmetic search for an INTERIOR counterexample to
single-unit-transfer sufficiency for Hamming-distance frequency scoring.

Conjecture (see `_context/exploration/bounds_search_manhattan_hamming.md`,
section (3')):

    For strictly interior beliefs p (every p_i > 0), if a report r is
    single-unit-transfer optimal under Hamming scoring, then r is globally
    optimal.

The memo verified this for k = 3 only (exact rational grids, n = 2..9, every
counterexample found had a coordinate exactly 0). This script extends the
exact rational-arithmetic search to k = 4, 5, 6. A single interior
counterexample refutes the conjecture and ends it cheaply; surviving the
search keeps the conjecture alive for a proof attempt.

All arithmetic in the classification is exact (`fractions.Fraction`); no
floating point is used, per the memo's warning that float sweeps are
unreliable where binomial pmf values are near zero.

Hamming expected loss is L_H(r;p) = sum_i (1 - b(r_i;n,p_i)); minimizing it
is maximizing G(r;p) = sum_i b(r_i;n,p_i) subject to sum_i r_i = n. A report
r is single-unit-transfer optimal iff no transfer j -> i strictly increases
G; it is globally optimal iff G(r;p) equals the maximum of G over all
feasible reports.

Run from the repository root:

    uv run python scripts/hamming_interior_search.py
    uv run python scripts/hamming_interior_search.py --quick
"""

from __future__ import annotations

import argparse
import math
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

# Allow `from config import ...` when run as `python scripts/exploration/<name>.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import SEED_HAMMING


def feasible_reports(n: int, k: int) -> list[tuple[int, ...]]:
    """All non-negative integer count vectors of length k summing to n."""
    if k == 1:
        return [(n,)]
    out: list[tuple[int, ...]] = []
    for x in range(n + 1):
        for tail in feasible_reports(n - x, k - 1):
            out.append((x,) + tail)
    return out


def binom_pmf_column(n: int, p: Fraction) -> list[Fraction]:
    """Exact [b(0;n,p), ..., b(n;n,p)] with b(t) = C(n,t) p^t (1-p)^(n-t)."""
    q = Fraction(1) - p
    return [Fraction(math.comb(n, t)) * (p ** t) * (q ** (n - t)) for t in range(n + 1)]


def pmf_table(n: int, p_vec: tuple[Fraction, ...]) -> list[list[Fraction]]:
    return [binom_pmf_column(n, pi) for pi in p_vec]


def g_value(r: tuple[int, ...], B: list[list[Fraction]]) -> Fraction:
    total = Fraction(0)
    for i, ri in enumerate(r):
        total += B[i][ri]
    return total


def single_transfer_optimal(r: tuple[int, ...], B: list[list[Fraction]], k: int) -> bool:
    """True iff no single-unit transfer j -> i strictly increases G.

    If r[j] > 0 then for any i != j the receiver has r[i] <= n - r[j] < n, so
    the index r[i] + 1 is always valid.
    """
    for j in range(k):
        if r[j] == 0:
            continue
        sender_gain = B[j][r[j] - 1] - B[j][r[j]]
        for i in range(k):
            if i == j:
                continue
            delta = (B[i][r[i] + 1] - B[i][r[i]]) + sender_gain
            if delta > 0:
                return False
    return True


def find_counterexamples(
    p_vec: tuple[Fraction, ...], n: int, k: int, reports: list[tuple[int, ...]]
) -> list[tuple[tuple[int, ...], tuple[int, ...], Fraction, Fraction]]:
    """Reports that are single-transfer optimal but strictly globally suboptimal.

    Each entry is (r, s, G(r), G(s)=V*) where r is the spurious local optimum
    and s is a strictly better report.
    """
    B = pmf_table(n, p_vec)
    g = {r: g_value(r, B) for r in reports}
    v_star = max(g.values())
    out = []
    for r in reports:
        if g[r] < v_star and single_transfer_optimal(r, B, k):
            best = next(s for s in reports if g[s] == v_star)
            out.append((r, best, g[r], v_star))
    return out


def grid_interior_beliefs(k: int, denom: int) -> list[tuple[Fraction, ...]]:
    """Strictly interior rational beliefs on the simplex grid of denominator denom."""
    out = []
    for counts in feasible_reports(denom, k):
        if all(c > 0 for c in counts):
            out.append(tuple(Fraction(c, denom) for c in counts))
    return out


def random_interior_belief(k: int, rng: random.Random, max_weight: int) -> tuple[Fraction, ...]:
    """A strictly interior rational belief: k positive integer weights, normalized."""
    a = [rng.randint(1, max_weight) for _ in range(k)]
    tot = sum(a)
    return tuple(Fraction(ai, tot) for ai in a)


def self_check() -> list[str]:
    """Confirm the classification logic on the memo's known k=3 boundary case."""
    msgs = []
    # Memo (3'): n=2, k=3, p=(0,0,1), r=(0,2,0) is single-transfer optimal but
    # strictly suboptimal; the global optimum is (0,0,2). This belief is on the
    # boundary, so it is not an interior counterexample -- it only validates
    # that find_counterexamples classifies a known case correctly.
    p = (Fraction(0), Fraction(0), Fraction(1))
    reports = feasible_reports(2, 3)
    cex = find_counterexamples(p, 2, 3, reports)
    hit = [(r, s) for (r, s, gr, gs) in cex]
    ok1 = ((0, 2, 0), (0, 0, 2)) in hit
    msgs.append(
        f"self-check 1 (known boundary counterexample n=2,k=3,p=(0,0,1)): "
        f"{'PASS' if ok1 else 'FAIL'} -- detected {hit}"
    )
    # A strictly interior, near-uniform belief should make its modal report
    # globally optimal; classify should return no counterexample for it.
    p2 = (Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4))
    cex2 = find_counterexamples(p2, 8, 4, feasible_reports(8, 4))
    ok2 = len(cex2) == 0
    msgs.append(
        f"self-check 2 (interior uniform n=8,k=4): "
        f"{'PASS' if ok2 else 'FAIL'} -- {len(cex2)} counterexample(s)"
    )
    if not (ok1 and ok2):
        raise SystemExit("SELF-CHECK FAILED -- classification logic is wrong; aborting.")
    return msgs


def run_search(quick: bool) -> str:
    rng = random.Random(SEED_HAMMING)
    weight_choices = [5, 12, 30, 80, 250]

    if quick:
        plan = {
            4: dict(n_range=range(2, 6), grids=[8, 12], n_random=2000),
            5: dict(n_range=range(2, 5), grids=[8, 10], n_random=1500),
            6: dict(n_range=range(2, 5), grids=[8], n_random=800),
        }
    else:
        plan = {
            4: dict(n_range=range(2, 9), grids=[8, 12, 16], n_random=25000),
            5: dict(n_range=range(2, 8), grids=[8, 10, 12], n_random=15000),
            6: dict(n_range=range(2, 6), grids=[8, 9, 10], n_random=6000),
        }

    start = time.time()
    lines: list[str] = []
    lines.append("# Hamming Interior Single-Transfer Sufficiency -- Exact Search")
    lines.append("")
    lines.append(
        "Step 0a of the Hamming-first plan (`_context/next_steps.md`). Exact "
        "rational-arithmetic search for an interior counterexample to: "
        "*single-unit-transfer optimality implies global optimality for "
        "strictly interior beliefs*."
    )
    lines.append("")
    lines.append(f"- Mode: `{'quick' if quick else 'full'}`.")
    lines.append("- Arithmetic: exact `fractions.Fraction`; no floating point.")
    lines.append(f"- Random-belief seed: `{SEED_HAMMING}`.")
    lines.append("")

    print("Running self-checks...", flush=True)
    for msg in self_check():
        print("  " + msg, flush=True)
        lines.append(f"- {msg}")
    lines.append("")

    all_counter: list[tuple] = []
    total_classifications = 0
    total_reports_scanned = 0
    per_k_summary: list[str] = []

    for k in sorted(plan):
        cfg = plan[k]
        n_values = list(cfg["n_range"])
        reports_by_n = {n: feasible_reports(n, k) for n in n_values}
        k_classifications = 0
        k_counter = 0
        print(f"k={k}: grids {cfg['grids']}, random {cfg['n_random']}, n in {n_values}", flush=True)

        # Structured grids.
        for denom in cfg["grids"]:
            beliefs = grid_interior_beliefs(k, denom)
            for n in n_values:
                reports = reports_by_n[n]
                for p in beliefs:
                    cex = find_counterexamples(p, n, k, reports)
                    k_classifications += 1
                    total_reports_scanned += len(reports)
                    if cex:
                        for entry in cex:
                            all_counter.append((n, k, p, *entry))
                        k_counter += len(cex)
            print(f"  grid denom={denom}: {len(beliefs)} interior beliefs done", flush=True)

        # Random interior beliefs.
        for idx in range(cfg["n_random"]):
            n = rng.choice(n_values)
            p = random_interior_belief(k, rng, rng.choice(weight_choices))
            reports = reports_by_n[n]
            cex = find_counterexamples(p, n, k, reports)
            k_classifications += 1
            total_reports_scanned += len(reports)
            if cex:
                for entry in cex:
                    all_counter.append((n, k, p, *entry))
                k_counter += len(cex)
            if (idx + 1) % 5000 == 0:
                print(f"  random: {idx + 1}/{cfg['n_random']}", flush=True)

        total_classifications += k_classifications
        per_k_summary.append(
            f"- k={k}: {k_classifications} (belief, n) classifications, "
            f"{k_counter} interior counterexample(s)."
        )
        print(f"  k={k} done: {k_counter} counterexample(s)", flush=True)

    elapsed = time.time() - start

    lines.append("## Search coverage")
    lines.append("")
    lines += per_k_summary
    lines.append(f"- Total: {total_classifications} (belief, n) classifications, "
                 f"{total_reports_scanned} report-optimality checks.")
    lines.append(f"- Elapsed: {elapsed:.1f} s.")
    lines.append("")

    lines.append("## Result")
    lines.append("")
    if not all_counter:
        verdict = (
            "NO interior counterexample found for k = 4, 5, 6. The conjecture "
            "(interior single-unit-transfer optimality implies global "
            "optimality) SURVIVES this extended exact search. It remains a "
            "conjecture -- a search is not a proof -- but a proof attempt is "
            "now warranted (Hamming-first plan, Step 1)."
        )
        lines.append(verdict)
        print("\nRESULT: " + verdict, flush=True)
    else:
        verdict = (
            f"REFUTED: {len(all_counter)} interior counterexample(s) found. "
            "Single-unit-transfer optimality is NOT sufficient for Hamming at "
            "strictly interior beliefs. The interior conjecture is dead; per "
            "the Hamming-first plan the fallback is to ship the 3-rule paper "
            "unless the simulation spike (Step 0b) still succeeds."
        )
        lines.append(verdict)
        lines.append("")
        lines.append("### Counterexamples (first 20)")
        lines.append("")
        for (n, k, p, r, s, gr, gs) in all_counter[:20]:
            p_str = "(" + ", ".join(str(pi) for pi in p) + ")"
            lines.append(
                f"- n={n}, k={k}, p={p_str}: report r={r} is single-transfer "
                f"optimal with G(r)={gr}, but s={s} has G(s)={gs} > G(r). "
                f"All p_i > 0: {all(pi > 0 for pi in p)}."
            )
        print("\nRESULT: " + verdict, flush=True)
        for (n, k, p, r, s, gr, gs) in all_counter[:5]:
            print(f"  n={n} k={k} p={tuple(str(pi) for pi in p)} r={r} s={s}", flush=True)
    lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="small grids/samples for a fast check")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/verification/hamming_interior_search.md"),
        help="markdown report path",
    )
    args = parser.parse_args()

    report = run_search(quick=args.quick)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"\nwrote {args.output}", flush=True)


if __name__ == "__main__":
    main()
