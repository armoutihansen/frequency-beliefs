# Frequency-Report Scoring Rules

> Replication code and manuscript for **"The Informativeness of Frequency-Report
> Scoring Rules"** by Jesper Armouti-Hansen.
> Status: manuscript complete; replication package finalised.

## What this is

The paper studies belief elicitation with *frequency reports* --- subjects
submit count vectors $r = (r_1, \dots, r_k)$ with $\sum_i r_i = n$, and a scoring
rule pays them on the distance between $r$ and the realised count vector. The
paper characterises the *identified set* of latent beliefs consistent with each
observed report and compares three rules --- squared-distance, frequency-guessing
(Schlag & Tremewan 2021), and Manhattan distance --- on the sharpness of the
belief bounds they induce.

The main result is contingent: no rule dominates. Squared-distance is most
informative when beliefs concentrate on a few categories; frequency-guessing
when beliefs are balanced; Manhattan distance is rarely the narrowest but is
regime-robust.

## Quick reproduction

From the repository root:

```bash
uv sync                # install Python dependencies into .venv/
make reproduce         # verify + simulate (5000 draws) + consistency check + compile paper
```

The full simulation runs for about 30 minutes. To regenerate only the PDF from
the committed outputs:

```bash
make paper
```

For a guided walkthrough, open the notebook:

```bash
uv run jupyter notebook notebooks/reproduce_analysis.ipynb
```

It walks from a worked example to the paper's headline tables, with parameter
cells at the top so you can change `n`, `k`, `α` and rerun on your own.

## Repository layout

| Path | What it is |
|---|---|
| `paper/` | LaTeX manuscript. Entry point: `paper/main.tex`. Compiled PDF: `paper/main.pdf`. |
| `scripts/verify_regions.py` | Finite-sample verification of the rule characterisations and the worked examples. |
| `scripts/design_efficiency.py` | Latent-belief simulation across the $(n, k, \alpha)$ grid. Run with `--final --draws 5000`. |
| `scripts/consistency_check.py` | Reconciles paper numbers against the committed CSV outputs. |
| `scripts/utils.py`, `scripts/config.py` | Shared helpers, tolerances, and seeds. |
| `scripts/exploration/` | Auxiliary scripts used during paper development (Hamming derisking, candidate-rule screening). Not part of the replication path. |
| `notebooks/reproduce_analysis.ipynb` | Guided walkthrough for replicating the analysis. |
| `outputs/` | Simulation CSVs. See `outputs/README.md` for the data dictionary. |
| `tests/` | `pytest` suite for the math core and a snapshot guard against output drift. |

## Software requirements

Python 3.14 and [`uv`](https://docs.astral.sh/uv/) are required. `uv sync`
installs everything from the committed `uv.lock`. The runtime depends on
`numpy` and `scipy` only; the notebook adds `jupyter` and `pandas`.

## Tests

```bash
uv run pytest -q tests/
```

The suite pins the numeric behaviour of the math core (closed-form bounds,
multinomial PMF, threshold root-finds) and reruns `consistency_check.py` as a
snapshot guard --- any drift between the simulation CSVs and the paper's
manuscript numbers fails the suite.

## Outputs

The committed CSVs in `outputs/design_exercise/` are the source for every
quantitative claim in the paper. See `outputs/README.md` for column-level
documentation and the mapping from each CSV to the paper table or appendix
section it supports.

## Citation

```bibtex
@unpublished{ArmoutiHansen2026FrequencyReports,
  author = {Armouti-Hansen, Jesper},
  title  = {The Informativeness of Frequency-Report Scoring Rules},
  year   = {2026},
  note   = {Working paper}
}
```
