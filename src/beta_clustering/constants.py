"""Physical and mathematical constants for beta-clustering-utac."""
import math

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0          # Golden ratio = 1.6180339887…
PHI_CUBEROOT: float = PHI ** (1.0 / 3.0)            # ≈ 1.17480502
PHI_SQRT: float = math.sqrt(PHI)                     # ≈ 1.27201965

SIGMA_PHI: float = 1.0 / 16.0                        # Frame Principle σ_Φ

# Domain beta cluster centres (from UTAC v1.0, DOI 10.5281/zenodo.17472834)
DOMAIN_BETA_CENTRES: dict[str, float] = {
    "climate":      0.09,
    "ecological":   0.23,
    "neural":       0.50,
    "astrophysical":0.90,
    "ai":           1.75,
}

# Benchmark targets
BETA_TARGETS: dict[str, tuple[float, float | None]] = {
    "n_systems":             (78,      0),
    "phi_cuberoot":          (1.17398, 0.00001),
    "inter_cluster_ratio":   (1.174,   1.0),
    "domain_cluster_count":  (5,       1),
    "universality_rejected": (True,    None),
    "sigma_from_beta":       (2.2,     0.2),
}

ZENODO_DOI: str = "10.5281/zenodo.17472834"
PACKAGE_NUMBER: int = 32
