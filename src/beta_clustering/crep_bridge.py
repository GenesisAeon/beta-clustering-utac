"""β ↔ Γ relationship — bridges UTAC β-parameter to CREP Γ-value."""
from __future__ import annotations

import math

# HONESTY NOTE (2026-09-15, verified numerically, following up on the
# ecosystem-wide Gamma-circularity review): the claim "sigma~=2.2 emerges
# from the beta distribution (UTAC v1.0 finding)" does NOT hold up when
# checked against this package's own data and its own
# sigma_from_beta_distribution() formula. Running it on both the default
# synthetic 78-system generator (system.py's _synthetic_78_systems(),
# itself built to "reproduce the UTAC v1.0 distribution") and on the
# literature-citing data/utac_v1_78_systems.yaml gives sigma ~= 1.28 in
# both cases -- not 2.2, a ~42% discrepancy. BETA_SCALE=2.2 here is the
# same shared default reused unchanged across unrelated GenesisAeon UTAC
# packages (see e.g. amoc-utac, afet-tensions), not an independently
# derived result for this package's beta-clustering domain. See
# D:\mandala\crep-utac-afet-formalism\FOLLOWUP_TICKETS.md for the full
# finding, including a second, related issue: system.py's
# _build_crep_state() always uses this hardcoded BETA_SCALE via
# beta_to_gamma()'s default, never the sigma_from_beta_distribution()
# value that _run_cycle() computes and reports separately -- the same
# "measured-but-unused" disconnect pattern found in amoc-utac.
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

    NOTE (2026-09-15): running this on this package's own default data
    (synthetic or the literature-citing YAML, see BETA_SCALE's docstring)
    gives sigma~=1.28, not the BETA_SCALE=2.2 default used elsewhere in
    this module -- this function's result is computed and reported by
    system.py's _run_cycle() but is not fed back into beta_to_gamma()'s
    actual Gamma computation, which always uses the hardcoded default.
    """
    if not betas:
        return BETA_SCALE
    mean_beta = sum(betas) / len(betas)
    # tanh(mean_beta / σ) = 0.5  →  σ = mean_beta / atanh(0.5)
    return mean_beta / math.atanh(0.5)
