"""Tests for universal β convergence vs. domain-specific clustering."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any


@dataclass
class UniversalityTestResult:
    n_systems: int
    n_clusters: int
    within_cluster_variance: float
    between_cluster_variance: float
    f_statistic: float
    universality_rejected: bool   # True = domain-specific, not universal


def run_universality_test(systems: list[dict[str, Any]]) -> UniversalityTestResult:
    """One-way ANOVA: are β values domain-specific?

    H₀: all β drawn from same distribution (universality)
    H₁: β differs by domain (domain-specific clusters)
    """
    domain_betas: dict[str, list[float]] = defaultdict(list)
    for s in systems:
        domain_betas[str(s.get("domain", "unknown"))].append(float(s["beta"]))

    all_betas = [float(s["beta"]) for s in systems]
    grand_mean = sum(all_betas) / len(all_betas) if all_betas else 0.0

    k = len(domain_betas)
    n = len(all_betas)

    ss_between = sum(
        len(vals) * (sum(vals) / len(vals) - grand_mean) ** 2
        for vals in domain_betas.values() if vals
    )
    ss_within = sum(
        (b - sum(vals) / len(vals)) ** 2
        for vals in domain_betas.values() if vals
        for b in vals
    )

    df_between = k - 1
    df_within = n - k

    ms_between = ss_between / max(df_between, 1)
    ms_within  = ss_within  / max(df_within, 1)

    f_stat = ms_between / ms_within if ms_within > 0 else float("inf")

    # Critical F at α=0.05 (approximate for df1≈4, df2≈73 → F_crit ≈ 2.5)
    universality_rejected = f_stat > 2.5

    return UniversalityTestResult(
        n_systems=n,
        n_clusters=k,
        within_cluster_variance=ms_within,
        between_cluster_variance=ms_between,
        f_statistic=f_stat,
        universality_rejected=universality_rejected,
    )
