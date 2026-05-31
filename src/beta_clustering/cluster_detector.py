"""Domain-specific β-cluster identification."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from beta_clustering.constants import DOMAIN_BETA_CENTRES


@dataclass
class BetaCluster:
    domain: str
    centre: float
    beta_min: float
    beta_max: float
    members: list[str] = field(default_factory=list)


def assign_cluster(beta: float) -> str:
    """Assign a β value to the nearest domain cluster."""
    best = min(DOMAIN_BETA_CENTRES.items(), key=lambda kv: abs(kv[1] - beta))
    return best[0]


def build_clusters(systems: list[dict[str, Any]]) -> list[BetaCluster]:
    """Build cluster objects from a list of {name, beta, domain} dicts."""
    cluster_map: dict[str, list[str]] = {d: [] for d in DOMAIN_BETA_CENTRES}
    for s in systems:
        raw_domain = s.get("domain")
        domain = str(raw_domain) if raw_domain else assign_cluster(float(s["beta"]))
        if domain not in cluster_map:
            domain = assign_cluster(float(s["beta"]))
        cluster_map[domain].append(str(s["name"]))

    clusters = []
    for domain, centre in sorted(DOMAIN_BETA_CENTRES.items(), key=lambda kv: kv[1]):
        spread = centre * 0.6
        clusters.append(BetaCluster(
            domain=domain,
            centre=centre,
            beta_min=centre - spread,
            beta_max=centre + spread,
            members=cluster_map[domain],
        ))
    return clusters
