# Hamming Bound-Computation Spike (Step 0b)

Feasibility spike for computing Hamming identification bounds in the design comparison. See `_context/next_steps.md`, Hamming-first plan, Step 0b.

- Mode: `quick`.
- Relaxation tolerance: tol = 1e-06.

- forward DP vs brute force: PASS (160 beliefs, 0 mismatch)

## k = 3 validation against the fine grid

Grid ground truth: `hamming_grid_bounds`, simplex denominator 240.
Optimizer relaxation tolerance: tol = 1e-06.

| n | k | r | coord | grid (lo, hi) | computed (lo, hi) | abs gap |
|---|---|---|---|---|---|---|
| 2 | 3 | (1, 1, 0) | p1 | (0.2375, 0.6667) | (0.2367, 0.6667) | 0.0008 |
| 2 | 3 | (1, 1, 0) | p2 | (0.2375, 0.6667) | (0.2367, 0.6667) | 0.0008 |
| 2 | 3 | (1, 1, 0) | p3 | (0.0000, 0.3333) | (0.0000, 0.3333) | 0.0000 |
| 5 | 3 | (2, 2, 1) | p1 | (0.2833, 0.5000) | (0.2828, 0.5000) | 0.0006 |
| 5 | 3 | (2, 2, 1) | p2 | (0.2833, 0.5000) | (0.2828, 0.5000) | 0.0006 |
| 5 | 3 | (2, 2, 1) | p3 | (0.1417, 0.3333) | (0.1408, 0.3333) | 0.0009 |
| 5 | 3 | (3, 2, 0) | p1 | (0.4333, 0.6667) | (0.4296, 0.6667) | 0.0037 |
| 5 | 3 | (3, 2, 0) | p2 | (0.2750, 0.5000) | (0.2720, 0.5000) | 0.0030 |
| 5 | 3 | (3, 2, 0) | p3 | (0.0000, 0.1667) | (0.0000, 0.1667) | 0.0000 |
| 10 | 3 | (5, 3, 2) | p1 | (0.4208, 0.5417) | (0.4191, 0.5455) | 0.0038 |
| 10 | 3 | (5, 3, 2) | p2 | (0.2500, 0.3625) | (0.2469, 0.3636) | 0.0031 |
| 10 | 3 | (5, 3, 2) | p3 | (0.1667, 0.2708) | (0.1648, 0.2727) | 0.0019 |

Worst coordinate gap vs grid: 0.0038 (acceptance threshold 0.0092: grid resolution + margin). PASS.

## n = 20, k = 10 probe

Optimizer relaxation tolerance: tol = 1e-06. Feasible-sample size target: 8000.

| report kind | r | per-report time (s) | sandwich OK | dominates feasible sample | feasible sample size |
|---|---|---|---|---|---|
| balanced | (2, 2, 2, 2, 2, 2, 2, 2, 2, 2) | 397.61 | yes | yes | 0 |
| skewed | (11, 4, 2, 1, 1, 1, 0, 0, 0, 0) | 312.65 | NO | yes | 0 |
| sparse | (0, 10, 0, 0, 0, 0, 1, 4, 5, 0) | 314.68 | NO | NO | 2 |

Mean per-report bound time: 341.65 s.
Conservative full-run projection (~300 distinct reports x ~12 heavy cells): 341.6 h.

Sandwich + feasible-sample containment: FAIL. Runtime projection under 24 h: FAIL.

## Verdict

SPIKE FAILS. Hamming bounds could not be computed reliably and/or tractably at n=50, k=10. Per the Hamming-first plan, decouple: resume the 3-rule revision (`_context/revision_plan.md`); the Hamming computed-bound simulation becomes documented future work.
