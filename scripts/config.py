"""Numeric tolerances, random seeds, and rule naming shared across the replication scripts.

Each constant is documented with the semantic question it answers, so a future
tuning pass can adjust them with intent rather than search-and-replace.
"""

# --------------------------------------------------------------------- rule naming

#: Internal rule keys. These are stable identifiers predating the 2026-05-22
#: manuscript renaming; do NOT rename them (function names and the committed
#: CSV outputs' provenance depend on them).
RULE_KEYS = ("discrete", "quadratic", "manhattan")

#: Canonical display names, matching the manuscript's terminology
#: ("frequency-guessing", "squared-distance"). All NEW CSV outputs and
#: printed summaries use these.
RULE_DISPLAY = {
    "discrete": "Frequency guessing",
    "quadratic": "Squared distance",
    "manhattan": "Manhattan distance",
}

#: Display names used by CSV outputs committed BEFORE the renaming
#: (everything currently in `outputs/design_exercise/`). Mapped to the
#: canonical names on read; do not regenerate those outputs just to rename
#: labels (final outputs are not overwritten without explicit instruction).
LEGACY_RULE_DISPLAY = {
    "Discrete metric": "Frequency guessing",
    "Quadratic distance": "Squared distance",
    "Manhattan distance": "Manhattan distance",
}


def canonical_rule_label(label: str) -> str:
    """Map a rule display label of any vintage to the canonical name."""
    return LEGACY_RULE_DISPLAY.get(label, label)

# --------------------------------------------------------------------- seeds

#: Default seed for the latent-belief and robustness simulations in
#: `design_efficiency.py`. The `--seed` CLI flag overrides it.
SEED_LATENT = 20260508

#: Default seed for the Hamming exploration scripts under `scripts/exploration/`.
SEED_HAMMING = 20260521

#: Default seed for the candidate-rule screening in
#: `scripts/exploration/candidate_rule_checks.py`.
SEED_CANDIDATE_RULES = 20260522

#: Default seed for the misreporting robustness exercise in
#: `scripts/misreporting_robustness.py` (plan:
#: `_context/misreporting_robustness_plan.md`). Per-cell streams and the
#: perturbation tie-break streams are spawned from it deterministically.
SEED_MISREPORTING = 20260610


# --------------------------------------------------------------------- tolerances

#: Default float-equality tolerance. Used by `argmin_reports`/`argmax_reports`
#: in `verify_regions.py` to decide which reports tie for optimal.
FLOAT_EQUALITY_TOL = 1e-9

#: Consistency-check tolerance for comparing manuscript-rounded numbers (two
#: displayed decimals) to recomputed values.
CONSISTENCY_ROUND_TOL = 0.01
