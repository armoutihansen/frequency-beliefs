# Outputs

Every quantitative claim in the paper traces to one of the CSVs below. The
schemas are documented so a referee or replication-package reviewer can read
the data without re-deriving the column meanings from the simulation script.

## `design_exercise/`

Produced by `scripts/design_efficiency.py --final --draws 5000` from the
repository root. Seed `20260508` (`scripts/config.SEED_LATENT`).

### `rule_comparison.csv` --- win shares and regret

| Column | Meaning |
|---|---|
| `n` | Number of trials. Grid: $\{5, 10, 20, 50\}$. |
| `k` | Number of categories. Grid: $\{2, 3, 5, 10\}$. |
| `alpha` | Symmetric Dirichlet concentration. Grid: $\{0.1, 0.3, 1, 3, 10\}$. |
| `metric` | Inferential target: `coord_avg`, `coord_max`, `mean_linear`, `mean_skewed`. |
| `rule` | `Discrete metric`, `Quadratic distance`, `Manhattan distance`. |
| `win_share` | Share of belief draws on which this rule gives the narrowest bound for this metric. |
| `mean_regret` | Mean cell-best regret: this rule's width minus the smallest width in the cell. |

**Paper references:** Table 1 (win shares by $\alpha$, averaged across $(n, k)$);
Table 2 (regret by $\alpha$); Appendix Table B (win shares marginalised by $n$
and $k$).

### `latent_aggregate.csv` --- raw width aggregates

| Column | Meaning |
|---|---|
| `n`, `k`, `alpha`, `rule` | Design cell. |
| `draws` | Draws per cell (5{,}000 in the final run). |
| `avg_coord_width_{mean,median}` | Average across coordinates of bound widths, then aggregated over draws. |
| `max_coord_width_{mean,median}` | Worst-coordinate width, aggregated. |
| `mean_linear_width_{mean,median}` | Width of the bound on $\sum_i p_i x_i$ with $x_i = (i-1)/(k-1)$. |
| `mean_skewed_width_{mean,median}` | Same, with $x_i = \mathbf{1}\{i = k\}$. |
| `tie_rate` | Fraction of draws where the optimal report ties. |
| `payment_probability_{mean,median}` | Exact-match payment probability (frequency-guessing only). |

**Paper references:** the underlying widths summarised in Table 1; the
payment-probability footnote at the end of §4.

### `fixed_reports.csv` --- fixed-report worked examples

For a hand-picked report $r$ at each $(n, k)$, the coordinate bounds, mean
bounds, and payment probability under each rule. Columns mirror the
`latent_aggregate.csv` schema with `report` replacing the draw-level
aggregations.

**Paper reference:** Appendix C (worked-example tables).

## `design_exercise/robustness/`

Produced by `scripts/design_efficiency.py --robustness --draws 5000`. Same
seed. Nine asymmetric concentration vectors at $n = 20$, $k = 5$.

### `rule_comparison.csv`

Same schema as the main run, but `alpha` is replaced by `alpha_label` (string,
e.g. `one-dominant`, `balanced-graded`) and an `alpha_vec` column carries the
concentration vector as a string (e.g. `"5,0.5,0.5,0.5,0.5"`).

**Paper reference:** Appendix C, `tab:regime-wins-asymmetric`.

### `latent_aggregate.csv`

Same schema as the main run, with the `alpha_label` / `alpha_vec` substitution.

## `verification/`

Diagnostic markdown artifacts from the Hamming derisking work:

- `hamming_interior_search.md` --- exact-arithmetic search for single-transfer
  counterexamples.
- `hamming_spike.md` --- feasibility spike for sharp Hamming bounds at the
  largest design cell.

**Paper references:** §5.2 (Hamming/Chebyshev "Limits of the Approach"). The
underlying scripts now live in `scripts/exploration/`.

## `simulation_design/` (legacy)

Pre-2026-05 outputs from a four-rule version of the analysis. The current
paper has dropped to three rules and uses `design_exercise/` exclusively.
These files are retained for archival only and are not referenced by the
manuscript or by any consistency check; safe to delete.
