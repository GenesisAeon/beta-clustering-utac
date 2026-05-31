"""Domain-specific β-cluster identification."""
from __future__ import annotations

from dataclasses import dataclass, field
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


def build_clusters(systems: list[dict[str, object]]) -> list[BetaCluster]:
    """Build cluster objects from a list of {name, beta, domain} dicts."""
    cluster_map: dict[str, list[str]] = {d: [] for d in DOMAIN_BETA_CENTRES}
    for s in systems:
        domain = s.get("domain") or assign_cluster(s["beta"])
        if domain not in cluster_map:
            domain = assign_cluster(s["beta"])
        cluster_map[domain].append(s["name"])

    clusters = []
    for domain, centre in sorted(DOMAIN_BETA_CENTRES.items(), key=lambda kv: kv[1]):
        spread = centre * 0.6
        members = cluster_map[domain]
        clusters.append(BetaCluster(
            domain=domain,
            centre=centre,
            beta_min=centre - spread,
            beta_max=centre + spread,
            members=members,
        ))
    return clusters
