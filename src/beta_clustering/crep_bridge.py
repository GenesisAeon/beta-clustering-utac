"""β ↔ Γ relationship — bridges UTAC β-parameter to CREP Γ-value."""
from __future__ import annotations

import math

# σ ≈ 2.2 emerges from the β distribution (UTAC v1.0 finding)
BETA_SCALE: float = 2.2


def beta_to_gamma(beta: float, beta_scale: float = BETA_SCALE) -> float:
    """Γ_domain ≈ tanh(β / β_scale)."""
    return math.tanh(beta / beta_scale)


def gamma_to_beta(gamma: float, beta_scale: float = BETA_SCALE) -> float:
    """Inverse: β = β_scale · atanh(Γ).  Γ must be in (-1, 1)."""
    gamma = max(-0.9999, min(0.9999, gamma))
    return beta_scale * math.atanh(gamma)


def sigma_from_beta_distribution(betas: list[float]) -> float:
    """Estimate β_scale (= σ) from a distribution of β values.

    σ is the value that maximises the log-likelihood of tanh(β/σ)
    as a Γ distribution. We use the empirical mean / atanh(0.5) heuristic.
    """
    if not betas:
        return BETA_SCALE
    mean_beta = sum(betas) / len(betas)
    # tanh(mean_beta / σ) = 0.5  →  σ = mean_beta / atanh(0.5)
    return mean_beta / math.atanh(0.5)
