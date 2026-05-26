# Exploration scripts

Auxiliary scripts used during paper development. **Not part of the replication
path** for the headline analysis (see `../README.md` and the project root
`README.md`). They are retained because the paper references the evidence they
produced.

| Script | What it does | Paper reference |
|---|---|---|
| `candidate_rule_checks.py` | Screens candidate frequency-report scoring rules against the separability and discrete-convexity hypotheses of Lemma 1. | §3 (structural lemma); CONTEXT.md analytical-bounds search. |
| `hamming_interior_search.py` | Exact-arithmetic search for counterexamples to single-transfer sufficiency under the Hamming rule. Documents that single-transfer optimality fails for Hamming at interior beliefs. | §5.2 "Other Frequency-Report Scoring Rules and the Limits of the Approach." |
| `hamming_spike.py` | Feasibility spike for computing sharp Hamming bounds at the largest design cell (`n=50, k=10`). Documents that the sharp bounds are intractable at the design grid's scale. | §5.2 (same); Appendix discussion of why Hamming is not headlined. |

## Running

From the repository root:

```bash
uv run python scripts/exploration/candidate_rule_checks.py
uv run python scripts/exploration/hamming_interior_search.py
uv run python scripts/exploration/hamming_spike.py --quick
```

Each script writes its diagnostic markdown to `outputs/verification/`.
