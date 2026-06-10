# Misreporting Robustness Exercise — Implementation Plan (P1)

Date: 2026-06-10. Status: IMPLEMENTED AND RUN same day (final: 5,000
draws/cell, full grid, all gates PASS; `scripts/misreporting_robustness.py`,
`outputs/misreporting/coverage_aggregate.csv`). **RESULT-DRIVEN REVISION
PENDING — read the addendum below before using the outputs.**

## ADDENDUM (post-run): sharp-set coverage is DEGENERATE by construction

The final run shows: conditional on one effective transfer, sharp-set
coverage is exactly 0 for all three rules in every cell (unconditional
nonzero values are no-ops and uniform-error random-walk returns only).
Explanation, knowable a priori and missed by both the design and the
methodologist review: the identified sets {P_S(r)} of distinct reports
TILE the simplex — they intersect only on tie boundaries of measure zero —
so the true belief is a.s. outside the sharp set of ANY effectively
perturbed report, for every rule. Sharp coverage is a one-bit optimal-
reporting diagnostic (consistent with §5.3's empirical-design use), not a
graded robustness metric; the survival statistic is degenerate
(share_T1 = 1 − no-op share for all rules).

The graded robustness contrast lives in: (i) **outer-box coverage** (boxes
of adjacent reports overlap with positive measure) — non-degenerate in the
run's data and directionally confirming §5.3 (center-bias, box-covered
share among misses at t=1 rises with alpha: squared 0.02→0.26 > Manhattan
0.01→0.26 ≥ guessing 0.01→0.23, squared ahead at every interior alpha);
and (ii) **violation magnitude** — how far p lies outside the claimed
bounds when coverage fails — which the facet-translation-vs-mode-jump
mechanism speaks to directly, and which the current script does NOT store
(only the zero/nonzero split).

REVISION (pending author go-ahead): drop survival as headline (degenerate;
keep the tiling fact as a stated result — it is itself a sharp,
publishable clarification: sharp identified-set inference has zero
tolerance for effective misreporting; robustness is a question of error
magnitude, not correctness); promote (a) unconditional box coverage at
t ∈ {1,2} and (b) violation-magnitude statistics (mean and 90th percentile
of the max-coordinate violation; linear-mean-bound violation analogously)
on the bounds subsample. Requires a small script change and a ~1.5h re-run
(same seed, same gates). Original plan follows.

## Question

If the submitted report deviates from an optimal report by a small number of
single-count transfers, how often does the identified set computed from the
perturbed report still contain the true latent belief, and what precision
does the researcher claim meanwhile? A sensitivity analysis of the
identification machinery to the conditional-on-optimal-reporting assumption
— NOT behavioral evidence.

## Key structural fact (state in the paper)

Identified-set widths are nearly invariant to single transfers
(frequency-guessing widths are report-independent constants; squared widths
depend on the report only through m(r)), so COVERAGE carries essentially all
the signal: claimed precision is unchanged while correctness degrades. Do
not build figures around width-vs-t (flat by construction).

## Perturbation models (single-count transfers; count-preserving)

- **Center-bias (CB)**: t times, move one count from the coordinate
  maximizing r_i − n/k to the coordinate minimizing it (seeded random
  tie-breaks). **No-op when max_i r_i − min_i r_i ≤ 1** (oscillation fix —
  otherwise t=2 mechanically restores t=0 in near-balanced cells). Record
  realized effective transfers t_eff per draw; report no-op shares and
  coverage both unconditional and conditional on t_eff ≥ 1.
- **Uniform error (UE)**: t times, move one count from a uniformly random
  positive coordinate to a uniformly random other coordinate. Record
  realized displacement ||r̃ − r||₁/2.
- Bound-evaluated intensities t ∈ {0, 1, 2}; t = 0 is the control gate.

## Headline statistic: survival

T = min{t : p ∉ P_S(r̃_t)} per draw and model, iterated with
membership-only checks (no bounds), censored at T_max = n. Report median T,
share with T = 1 (cliff mass), censored share, and T/n for cross-n
comparability. This operationalizes (not "confirms") the §5.3
facet-translation-vs-mode-jump contrast; the appendix must say
"we operationalize this contrast as ...".

## Grid, draws, seeds, rules

Main-exercise grid (n ∈ {5,10,20,50}, k ∈ {2,3,5,10}, α ∈ {0.1,0.3,1,3,10});
5,000 draws/cell final, 500 pilot; new constant SEED_MISREPORTING in
`scripts/config.py`, child generators spawned from it for perturbation
tie-breaks (determinism gate covers them). Three rules, canonical names from
`config.RULE_DISPLAY`.

## Metrics per (cell, rule, model, t)

- Coverage via existing membership tests (`exact_transfer_region`,
  `squared_transfer_region`, `l1_exchange_region`; O(k²) each), with
  per-cell SE √(c(1−c)/m).
- Paired coverage drops (t vs t−1) with paired SEs from within-draw 2×2
  transition counts.
- Unconditional claimed precision from the perturbed report (existing
  `BoundComputer`; reuse `linear_outcome`/`skewed_outcome`): avg/worst
  coordinate width, mean-bound widths.
- Severity proxy among non-covered draws: max coordinate-interval violation
  max_i dist(p_i,[lo_i,hi_i]) — an OUTER-BOX proxy, labeled as such — plus
  the share of non-covered draws with zero box-violation (boundary-grazing
  vs genuine departure).

## Cross-rule framing (fairness)

Coverage is mechanically confounded with identified-set size. Main device:
joint coverage-plus-width reporting with **Pareto statements per cell**
(A dominates B only with weakly higher coverage AND weakly narrower width;
report dominance frequencies). Explicitly reject matched-width calibration
as undefined (no rule has a width knob) and equal-tolerance inflation as
uncalibrated (rule-specific units). Optional secondary: ε-inflated
box-coverage curves (common probability units; outer box, labeled).
Never "rule X is fragile/robust" without model, intensity, and the width
qualifier.

## Validation gates

(a) t = 0 coverage ≡ 1.0 (weak inequalities include ties); on failure LOG
the witness (cell, rule, p, r). (b) Smoke mode: cross-check report
generators (`report_for_rule` ∈ brute argmin set) AND membership functions
against brute force separately, small cells (n ≤ 6, k ≤ 3). (c) Seeded
determinism including perturbation RNG. (d) Feasibility of r̃ by
construction. (e) Rationalizability: every feasible r̃ has P_S(r̃) ≠ ∅ —
p = r̃/n is a member for all three rules (exact/squared: transfer
inequalities at p = r̃/n; Manhattan: the binomial integer-mean median fact;
see the master-threshold memo's nonemptiness note); cite, and smoke-check
for Manhattan.

## Outputs

New dir `outputs/misreporting/` (never touches `outputs/design_exercise/`
or `outputs/simulation_design/`). Long-format
`coverage_aggregate.csv`: cell, rule (canonical), model, t, t_over_n,
draws, coverage, coverage_se, drop, drop_se, noop_share, mean_t_eff,
mean_displacement, tie_rate, avg_coord_width, max_coord_width,
mean_linear_width, mean_skewed_width, noncov_zero_boxviol_share,
survival_median_T, survival_share_T1, survival_censored_share, T_max,
seed, tolerance, script_version/git hash. Draw-level dump in pilot/smoke
only. Runtime control: bounds only at t ∈ {0,1,2}; survival iteration is
membership-only.

## Files

- New: `scripts/misreporting_robustness.py` (imports `report_for_rule`,
  `BoundComputer`, RULES, labels from `design_efficiency`; membership tests
  from `verify_regions`); `outputs/misreporting/`.
- Modified: `scripts/config.py` (SEED_MISREPORTING only).
- Untouched: `design_efficiency.py`, `verify_regions.py`, committed outputs.

## Paper integration (later; guardrail mode)

Short appendix subsection + 2–3 sentences sharpening §5.3's qualitative
paragraph. Wording discipline: CB is "motivated by" Danz–Vesterlund–Wilson
(different mechanism), never "calibrated to"; "sensitivity of
identification under stipulated report perturbations", not "robustness";
coverage statements are about the machinery, not subjects. The
methodologist's safe-wording template is in the review (session log
2026-06-10). Figure for P2: survival curves by rule, faceted (k, α), CB and
UE side by side; compact table (t=0 width, share T=1, median T) for
representative cells.

## Housekeeping noted during review

`CLAUDE.md`'s repository-structure line says `outputs/simulation_design/`
is the final simulation output; the live directory the paper tables and
consistency checks read is `outputs/design_exercise/` (the older committed
run remains in `outputs/simulation_design/`). Fixed in CLAUDE.md 2026-06-10.
