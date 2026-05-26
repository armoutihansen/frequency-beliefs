"""Shared utilities used across the replication scripts.

Kept intentionally small: numeric tolerance helpers, interval-width arithmetic,
report (de)serialisation, and the simplex-grid generator. No domain logic.
"""

from __future__ import annotations

import math

import numpy as np


def clean(v: float, tol: float = 1e-10) -> float:
    """Snap a float to 0 or 1 if it is within `tol`, else cast to float."""
    if abs(v) < tol:
        return 0.0
    if abs(v - 1.0) < tol:
        return 1.0
    return float(v)


def fmt_float(v: float, digits: int = 6) -> str:
    if math.isnan(v):
        return ""
    return f"{v:.{digits}f}"


def fmt_interval(iv: tuple[float, float] | None, digits: int = 4) -> str:
    if iv is None:
        return "NA"
    return f"[{iv[0]:.{digits}f}, {iv[1]:.{digits}f}]"


def interval_width(iv: tuple[float, float] | None) -> float:
    if iv is None:
        return float("nan")
    return clean(iv[1] - iv[0])


def average_width(coord: list[tuple[float, float]]) -> float:
    return clean(float(np.mean([interval_width(iv) for iv in coord])))


def max_width(coord: list[tuple[float, float]]) -> float:
    return clean(max(interval_width(iv) for iv in coord))


def report_to_string(r: tuple[int, ...]) -> str:
    return "(" + ",".join(str(v) for v in r) + ")"


def parse_report(text: str) -> tuple[int, ...]:
    stripped = text.strip().strip("()")
    return tuple(int(part.strip()) for part in stripped.split(",") if part.strip())
