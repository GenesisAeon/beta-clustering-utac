"""BetaClusteringUTAC — Diamond interface for Package 32."""
from __future__ import annotations

import pathlib
import random
from typing import Any

import yaml
from diamond_setup.protocol import (
    CREPState,
    DiamondPackage,
    UTACState,
    ZenodoCreator,
    ZenodoRecord,
)

from beta_clustering.benchmark import check_targets
from beta_clustering.cluster_detector import BetaCluster, build_clusters
from beta_clustering.constants import (
    PACKAGE_NUMBER,
    PHI_CUBEROOT,
    ZENODO_DOI,
)
from beta_clustering.crep_bridge import beta_to_gamma, sigma_from_beta_distribution
from beta_clustering.phi_scaling import PhiScalingResult, analyse_phi_scaling
from beta_clustering.universality_test import run_universality_test

System = dict[str, Any]


def _load_systems(path: str | None) -> list[System]:
    """Load threshold systems from YAML or return synthetic defaults."""
    if path:
        p = pathlib.Path(path)
        if p.exists():
            with p.open() as f:
                data: dict[str, Any] = yaml.safe_load(f)
            result: list[System] = data.get("systems", [])
            return result
    return _synthetic_78_systems()


def _synthetic_78_systems() -> list[System]:
    """Synthetic 78 threshold systems reproducing UTAC v1.0 distribution."""
    rng = random.Random(42)

    domains = [
        ("climate", 0.09, 0.04, 16),
        ("ecological", 0.23, 0.06, 15),
        ("neural", 0.50, 0.08, 16),
        ("astrophysical", 0.90, 0.15, 15),
        ("ai", 1.75, 0.35, 16),
    ]

    systems: list[System] = []
    for domain, centre, sigma, count in domains:
        for i in range(count):
            beta = max(0.01, rng.gauss(centre, sigma))
            systems.append({
                "name": f"{domain}_{i + 1:02d}",
                "domain": domain,
                "beta": round(beta, 4),
            })
    return systems


class BetaClusteringUTAC(DiamondPackage):
    """Diamond interface — Package 32: β-Clustering over 78 threshold systems.

    Key result: β clusters by domain; inter-cluster ratios ≈ Φ^(1/3) ≈ 1.174.
    DOI: 10.5281/zenodo.17472834
    """

    PACKAGE_ID: int = 32

    def __init__(self, data_path: str | None = None, n_systems: int = 78) -> None:
        super().__init__()
        self.data_path = data_path
        self._n_systems = n_systems
        self._systems: list[System] = []
        self._clusters: list[BetaCluster] = []
        self._phi_result: PhiScalingResult | None = None
        self._cycle_result: dict[str, Any] = {}

    def run_cycle(self, n_systems: int | None = None) -> dict[str, Any]:
        """Run full β-clustering analysis (optional *n_systems* override)."""
        if n_systems is not None:
            self._n_systems = n_systems
        return super().run_cycle()

    def _run_cycle(self) -> dict[str, Any]:
        self._systems = _load_systems(self.data_path)
        if len(self._systems) > self._n_systems:
            self._systems = self._systems[: self._n_systems]

        self._clusters = build_clusters(self._systems)
        self._phi_result = analyse_phi_scaling(self._clusters)
        univ = run_universality_test(self._systems)
        all_betas = [float(s["beta"]) for s in self._systems]
        sigma = sigma_from_beta_distribution(all_betas)

        self._cycle_result = {
            "n_systems": len(self._systems),
            "phi_cuberoot": PHI_CUBEROOT,
            "inter_cluster_ratio": self._phi_result.mean_ratio,
            "domain_cluster_count": len(self._clusters),
            "universality_rejected": univ.universality_rejected,
            "sigma_from_beta": sigma,
            "phi_scaling_result": self._phi_result,
            "f_statistic": univ.f_statistic,
        }
        return self._cycle_result

    def _build_crep_state(self) -> CREPState:
        if not self._systems:
            raise RuntimeError("CREP state unavailable before _run_cycle completes")
        all_betas = [float(s["beta"]) for s in self._systems]
        gammas = [beta_to_gamma(b) for b in all_betas]
        mean_gamma = sum(gammas) / len(gammas) if gammas else 0.0
        phi_res = self._phi_result
        c_val = min(1.0, phi_res.mean_ratio / PHI_CUBEROOT) if phi_res else 0.5
        r_val = 1.0 - min(1.0, abs(phi_res.mean_ratio - PHI_CUBEROOT)) if phi_res else 0.5
        p_val = len(self._systems) / 78.0
        return CREPState(
            C=c_val,
            R=r_val,
            E=min(1.0, mean_gamma),
            P=min(1.0, p_val),
        )

    def _build_utac_state(self) -> UTACState:
        if not self._cycle_result:
            raise RuntimeError("UTAC state unavailable before _run_cycle completes")
        h_norm = min(1.0, len(self._systems) / 78.0)
        ratio = float(self._cycle_result.get("inter_cluster_ratio", PHI_CUBEROOT))
        h_star = min(1.0, ratio / PHI_CUBEROOT)
        k_eff = max(1e-6, float(self._cycle_result.get("sigma_from_beta", 2.2)))
        return UTACState(H=h_norm, H_star=h_star, K_eff=k_eff)

    def _build_phase_events(self) -> list[dict[str, Any]]:
        if not self._clusters:
            return []
        events: list[dict[str, Any]] = []
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

    def _build_zenodo_record(self) -> ZenodoRecord:
        return ZenodoRecord(
            title=(
                "beta-clustering-utac: Φ^(1/3) Inter-Cluster Scaling "
                "(GenesisAeon Package 32)"
            ),
            description=(
                "β-clustering across 78 threshold systems. "
                f"Inter-cluster ratios ≈ Φ^(1/3) ≈ {PHI_CUBEROOT:.4f}. "
                f"DOI: {ZENODO_DOI}."
            ),
            creators=[ZenodoCreator(name="Römer, Johann", affiliation="MOR Research Collective")],
        )

    def to_zenodo_record(self) -> dict[str, Any]:
        """Export results as Zenodo metadata with package-specific fields."""
        base = super().to_zenodo_record()
        if not self._cycle_result:
            return {
                **base,
                "doi": ZENODO_DOI,
                "package": PACKAGE_NUMBER,
                "name": "beta-clustering-utac",
            }
        return {
            **base,
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
        assert self._phi_result is not None
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