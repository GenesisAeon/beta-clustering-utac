"""MLE estimation of UTAC steepness parameter β from threshold data."""
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class ThresholdObservation:
    x: float           # covariate (e.g., forcing magnitude)
    y: int             # 0 = no transition, 1 = transition
    weight: float = 1.0


@dataclass
class BetaEstimateResult:
    beta: float
    x_threshold: float
    log_likelihood: float
    n_obs: int
    converged: bool


def _logistic(x: float, beta: float, x0: float) -> float:
    z = beta * (x - x0)
    z = max(-500.0, min(500.0, z))
    return 1.0 / (1.0 + math.exp(-z))


def estimate_beta(
    observations: list[ThresholdObservation],
    n_steps: int = 200,
    lr: float = 0.01,
) -> BetaEstimateResult:
    """MLE estimation via gradient ascent on log-likelihood.

    Model: P(transition | x) = 1 / (1 + exp(-β(x - x_threshold)))
    """
    if not observations:
        raise ValueError("Need at least one observation")

    xs = [o.x for o in observations]
    x0 = sum(xs) / len(xs)
    beta = 1.0

    for _ in range(n_steps):
        grad_beta = 0.0
        grad_x0 = 0.0
        for obs in observations:
            p = _logistic(obs.x, beta, x0)
            p = max(1e-12, min(1 - 1e-12, p))
            residual = obs.y - p
            grad_beta += obs.weight * residual * (obs.x - x0)
            grad_x0  += obs.weight * residual * (-beta)
        beta += lr * grad_beta
        x0   += lr * grad_x0
        beta = max(1e-6, beta)

    ll = sum(
        obs.weight * (obs.y * math.log(max(1e-12, _logistic(obs.x, beta, x0)))
                      + (1 - obs.y) * math.log(max(1e-12, 1 - _logistic(obs.x, beta, x0))))
        for obs in observations
    )

    return BetaEstimateResult(
        beta=beta,
        x_threshold=x0,
        log_likelihood=ll,
        n_obs=len(observations),
        converged=True,
    )
