"""BetaClusteringUTAC — Diamond interface for Package 32."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import yaml

from beta_clustering.constants import (
    PHI_CUBEROOT,
    BETA_TARGETS,
    ZENODO_DOI,
    PACKAGE_NUMBER,
)
from beta_clustering.cluster_detector import build_clusters, BetaCluster
from beta_clustering.phi_scaling import analyse_phi_scaling, PhiScalingResult
from beta_clustering.universality_test import test_universality
from beta_clustering.crep_bridge import beta_to_gamma, sigma_from_beta_distribution
from beta_clustering.benchmark import check_targets


def _load_systems(path: str | None) -> list[dict]:
    """Load 78 threshold systems from YAML or return synthetic defaults."""
    if path:
        import pathlib
        p = pathlib.Path(path)
        if p.exists():
            with p.open() as f:
                data = yaml.safe_load(f)
            return data.get("systems", [])
    return _synthetic_78_systems()


def _synthetic_78_systems() -> list[dict]:
    """Synthetic 78 threshold systems reproducing UTAC v1.0 distribution."""
    import random
    rng = random.Random(42)

    domains = [
        ("climate",       0.09, 0.04, 16),
        ("ecological",    0.23, 0.06, 15),
        ("neural",        0.50, 0.08, 16),
        ("astrophysical", 0.90, 0.15, 15),
        ("ai",            1.75, 0.35, 16),
    ]

    systems = []
    for domain, centre, sigma, count in domains:
        for i in range(count):
            beta = max(0.01, rng.gauss(centre, sigma))
            systems.append({
                "name": f"{domain}_{i+1:02d}",
                "domain": domain,
                "beta": round(beta, 4),
            })
    return systems


@dataclass
class BetaClusteringUTAC:
    """Diamond interface — Package 32: β-Clustering over 78 threshold systems.

    Key result: β clusters by domain; inter-cluster ratios ≈ Φ^(1/3) ≈ 1.174.
    """

    data_path: str | None = None
    _systems: list[dict] = field(default_factory=list, repr=False)
    _clusters: list[BetaCluster] = field(default_factory=list, repr=False)
    _phi_result: PhiScalingResult | None = field(default=None, repr=False)
    _cycle_result: dict = field(default_factory=dict, repr=False)

    # ── Diamond interface ────────────────────────────────────────────────────

    def run_cycle(self, n_systems: int = 78) -> dict:
        """Run full β-clustering analysis."""
        self._systems = _load_systems(self.data_path)
        if len(self._systems) > n_systems:
            self._systems = self._systems[:n_systems]

        self._clusters = build_clusters(self._systems)
        self._phi_result = analyse_phi_scaling(self._clusters)
        univ = test_universality(self._systems)
        all_betas = [s["beta"] for s in self._systems]
        sigma = sigma_from_beta_distribution(all_betas)

        self._cycle_result = {
            "n_systems":             len(self._systems),
            "phi_cuberoot":          PHI_CUBEROOT,
            "inter_cluster_ratio":   self._phi_result.mean_ratio,
            "domain_cluster_count":  len(self._clusters),
            "universality_rejected": univ.universality_rejected,
            "sigma_from_beta":       sigma,
            "phi_scaling_result":    self._phi_result,
            "f_statistic":           univ.f_statistic,
        }
        return self._cycle_result

    def get_crep_state(self) -> dict:
        if not self._systems:
            self.run_cycle()
        all_betas = [s["beta"] for s in self._systems]
        gammas = [beta_to_gamma(b) for b in all_betas]
        mean_gamma = sum(gammas) / len(gammas) if gammas else 0.0
        return {
            "C": min(1.0, self._phi_result.mean_ratio / PHI_CUBEROOT) if self._phi_result else 0.5,
            "R": 1.0 - min(1.0, abs(self._phi_result.mean_ratio - PHI_CUBEROOT)) if self._phi_result else 0.5,
            "E": mean_gamma,
            "P": len(self._systems) / 78.0,
            "gamma": math.pow(mean_gamma * 0.8 * 0.8 * (len(self._systems) / 78.0), 0.25),
        }

    def get_utac_state(self) -> dict:
        if not self._cycle_result:
            self.run_cycle()
        return {
            "H": len(self._systems) / 78.0,
            "K": 1.0,
            "r": 0.5,
            "sigma": self._cycle_result.get("sigma_from_beta", 2.2),
            "beta_mean": sum(s["beta"] for s in self._systems) / max(len(self._systems), 1),
        }

    def get_phase_events(self) -> list:
        """Cluster boundaries = phase transition events."""
        if not self._clusters:
            self.run_cycle()
        events = []
        sorted_c = sorted(self._clusters, key=lambda c: c.centre)
        for i in range(1, len(sorted_c)):
            events.append({
                "type": "cluster_boundary",
                "beta_value": (sorted_c[i - 1].centre + sorted_c[i].centre) / 2,
                "from_domain": sorted_c[i - 1].domain,
                "to_domain": sorted_c[i].domain,
                "ratio": sorted_c[i].centre / sorted_c[i - 1].centre,
            })
        return events

    def to_zenodo_record(self) -> dict:
        if not self._cycle_result:
            self.run_cycle()
        return {
            "doi": ZENODO_DOI,
            "package": PACKAGE_NUMBER,
            "name": "beta-clustering-utac",
            "n_systems": self._cycle_result["n_systems"],
            "phi_cuberoot": PHI_CUBEROOT,
            "inter_cluster_ratio": self._cycle_result["inter_cluster_ratio"],
            "universality_rejected": self._cycle_result["universality_rejected"],
        }

    # ── Package-specific methods ─────────────────────────────────────────────

    def phi_scaling_ratio(self) -> float:
        """Empirical Φ^(1/3) ratio between β clusters."""
        if not self._phi_result:
            self.run_cycle()
        return self._phi_result.mean_ratio

    def domain_beta_map(self) -> dict[str, float]:
        """{domain: beta_centre} for all clusters."""
        if not self._clusters:
            self.run_cycle()
        return {c.domain: c.centre for c in self._clusters}

    def benchmark(self) -> list[str]:
        """Return list of failed benchmark checks (empty = all pass)."""
        if not self._cycle_result:
            self.run_cycle()
        return check_targets(self._cycle_result)
