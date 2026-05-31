"""Φ^(1/3) inter-cluster scaling analysis."""
from __future__ import annotations

import math
from dataclasses import dataclass

from beta_clustering.constants import PHI_CUBEROOT
from beta_clustering.cluster_detector import BetaCluster


@dataclass
class PhiScalingResult:
    ratios: list[float]
    mean_ratio: float
    phi_cuberoot: float
    mean_deviation: float
    p_value_approx: float   # one-sample t-test approximation
    null_rejected: bool


def analyse_phi_scaling(clusters: list[BetaCluster]) -> PhiScalingResult:
    """Test whether β-cluster centre ratios ≈ Φ^(1/3).

    Null hypothesis: ratios are uniformly distributed in [1.0, 1.5].
    Alternative: mean ratio ≈ Φ^(1/3) = 1.17480.
    """
    sorted_clusters = sorted(clusters, key=lambda c: c.centre)
    centres = [c.centre for c in sorted_clusters]

    ratios = []
    for i in range(1, len(centres)):
        if centres[i - 1] > 0:
            ratios.append(centres[i] / centres[i - 1])

    if not ratios:
        return PhiScalingResult([], 0.0, PHI_CUBEROOT, float("inf"), 1.0, False)

    mean_ratio = sum(ratios) / len(ratios)
    mean_dev = abs(mean_ratio - PHI_CUBEROOT)

    # Approximate one-sample t-test: H₀ mean = 1.25 (midpoint of [1.0,1.5])
    n = len(ratios)
    var = sum((r - mean_ratio) ** 2 for r in ratios) / max(n - 1, 1)
    se = math.sqrt(var / n) if var > 0 else 1e-12
    null_mean = 1.25
    t = (mean_ratio - null_mean) / se if se > 0 else 0.0
    # Crude p-value approximation using normal CDF proxy
    p_approx = 2.0 * (1.0 - _norm_cdf(abs(t)))

    return PhiScalingResult(
        ratios=ratios,
        mean_ratio=mean_ratio,
        phi_cuberoot=PHI_CUBEROOT,
        mean_deviation=mean_dev,
        p_value_approx=p_approx,
        null_rejected=(p_approx < 0.05),
    )


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
