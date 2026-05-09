# Review and verify the computational components.

Steps:

1. Read `README.md`.
2. Read `_context/current_status.md`.
3. Read `_context/current_issues.md`.
4. Inspect `scripts/verify_regions.py`.
5. Inspect `scripts/design_efficiency.py`.
6. Use the `code-reviewer` agent.
7. Run, if appropriate:

```bash
uv run python scripts/verify_regions.py
uv run python -m py_compile scripts/design_efficiency.py scripts/verify_regions.py
```

Report:

1. verification status
2. code-paper consistency
3. mathematical claims covered by finite checks
4. mathematical claims not covered by checks
5. reproducibility issues
6. recommended tests or refactors
7. whether any generated outputs are stale

Do not run the final design simulation unless explicitly asked.
Do not overwrite outputs unless explicitly asked.