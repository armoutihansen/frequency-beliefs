# Frequency-Report Scoring Rules

This repository contains a research project on belief elicitation with frequency reports.
The active paper studies what an experimenter can infer from an observed count report \(r\) when a scoring rule induces an optimal-report correspondence and therefore an inverse belief region \(P_S(r)\).

## Active Paper

The manuscript source is in `paper/`.

Compile from the paper directory with:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/private/tmp main.tex
```

For a local bibliography build, run `pdflatex main.tex`, `bibtex main`, and then `pdflatex main.tex` twice from `paper/`.
Generated LaTeX artifacts are ignored.

The current working title is:

> The Informational Efficiency of Frequency-Report Scoring Rules

## Code

The active scripts are:

- `scripts/verify_regions.py`: finite computational checks for the rule characterizations and worked examples.
- `scripts/design_efficiency.py`: latent-belief simulation and fixed-report comparison for the design exercise.

Run the checks with:

```bash
uv run python scripts/verify_regions.py
uv run python -m py_compile scripts/design_efficiency.py scripts/verify_regions.py
```

The final design exercise was generated with:

```bash
uv run python scripts/design_efficiency.py --final --draws 5000
```

The final CSV outputs are stored in `outputs/design_exercise/`. (`outputs/simulation_design/` retains the earlier four-rule run for archival reference.)

## Current Context

The active context files are:

- `_context/current_status.md`
- `_context/current_issues.md`
- `_context/next_steps.md`

Local literature PDFs are stored in `_context/related_literature/`.

## Current Scope

The active paper focuses on:

- quadratic-distance frequency scoring;
- discrete-metric frequency scoring;
- Manhattan-distance frequency scoring;
- belief and mean bounds from inverse belief regions;
- risk-aversion and probability implementation.

Hamming and Chebyshev distance are secondary computable rules, not the headline contribution.
