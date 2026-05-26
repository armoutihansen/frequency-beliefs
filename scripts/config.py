"""Numeric tolerances and random seeds shared across the replication scripts.

Each constant is documented with the semantic question it answers, so a future
tuning pass can adjust them with intent rather than search-and-replace.
"""

# --------------------------------------------------------------------- seeds

#: Default seed for the latent-belief and robustness simulations in
#: `design_efficiency.py`. The `--seed` CLI flag overrides it.
SEED_LATENT = 20260508

#: Default seed for the Hamming exploration scripts under `scripts/exploration/`.
SEED_HAMMING = 20260521

#: Default seed for the candidate-rule screening in
#: `scripts/exploration/candidate_rule_checks.py`.
SEED_CANDIDATE_RULES = 20260522


# --------------------------------------------------------------------- tolerances

#: Default float-equality tolerance. Used by `argmin_reports`/`argmax_reports`
#: in `verify_regions.py` to decide which reports tie for optimal.
FLOAT_EQUALITY_TOL = 1e-9

#: Consistency-check tolerance for comparing manuscript-rounded numbers (two
#: displayed decimals) to recomputed values.
CONSISTENCY_ROUND_TOL = 0.01
