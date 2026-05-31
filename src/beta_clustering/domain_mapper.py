"""Maps domains to β-cluster ranges."""
from __future__ import annotations

from beta_clustering.constants import DOMAIN_BETA_CENTRES


DOMAIN_DESCRIPTIONS: dict[str, str] = {
    "climate":       "Glacial cycles, AMOC, Arctic ice, Amazon dieback",
    "ecological":    "Coral bleaching, species extinction, epidemic thresholds",
    "neural":        "Neural criticality, seizure onset, anesthesia transitions",
    "astrophysical": "Stellar collapse, neutron star mass, jet accretion",
    "ai":            "Neural network phase transitions, LLM emergence",
}


def get_domain_info(domain: str) -> dict:
    centre = DOMAIN_BETA_CENTRES.get(domain, float("nan"))
    return {
        "domain": domain,
        "beta_centre": centre,
        "description": DOMAIN_DESCRIPTIONS.get(domain, ""),
    }


def list_domains() -> list[str]:
    return sorted(DOMAIN_BETA_CENTRES.keys(), key=lambda d: DOMAIN_BETA_CENTRES[d])
