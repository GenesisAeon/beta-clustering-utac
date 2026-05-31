"""Validation of β-clustering results against UTAC v1.0 targets."""
from __future__ import annotations

from typing import Any

from beta_clustering.constants import BETA_TARGETS


def check_targets(results: dict[str, Any]) -> list[str]:
    """Return list of failed checks (empty = all pass)."""
    failures = []
    for key, (target, tol) in BETA_TARGETS.items():
        if key not in results:
            failures.append(f"Missing key: {key}")
            continue
        val = results[key]
        if tol is None:
            if val is not target and val != target:
                failures.append(f"{key}: expected {target}, got {val}")
        else:
            try:
                if abs(float(val) - float(target)) > float(tol):
                    failures.append(f"{key}: {val:.6g} not within {tol} of {target}")
            except (TypeError, ValueError) as e:
                failures.append(f"{key}: cannot compare — {e}")
    return failures
