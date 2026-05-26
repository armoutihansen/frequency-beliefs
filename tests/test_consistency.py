"""Snapshot guard: consistency_check.py must exit clean.

This script reconciles paper-manuscript numbers against the committed CSV
outputs in `outputs/design_exercise/`. If the refactor drifts any number,
consistency_check exits non-zero and this test fails.
"""

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_consistency_check_passes():
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "consistency_check.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"consistency_check.py failed (exit {result.returncode}).\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
