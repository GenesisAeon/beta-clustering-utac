# beta-clustering-utac

**Package 32 — GenesisAeon Feldtheorie**

[![CI](https://github.com/GenesisAeon/beta-clustering-utac/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/beta-clustering-utac/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17472834-blue)](https://doi.org/10.5281/zenodo.17472834)
[![Package](https://img.shields.io/badge/GenesisAeon-Package%2032-gold)](https://doi.org/10.5281/zenodo.17472834)

β-Clustering über 78 Schwellensysteme aus Astrophysik, Klimaforschung, KI, Biologie und Neurowissenschaft. Kern-Ergebnis: **domänenspezifische β-Cluster** mit **Φ^(1/3) ≈ 1.174 Inter-Cluster-Skalierung**.

---

## Ergebnis

```
Domain          β-Zentrum   Beispiele
─────────────────────────────────────────────────────
climate         0.09        AMOC, Arktiseis, Amazon
ecological      0.23        Korallenbleiche, Epidemien
neural          0.50        Neurale Kritikalität, Anfälle
astrophysical   0.90        Sternkollaps, AGN-Zündung
ai              1.75        Grokking, LLM-Emergence

Inter-Cluster-Ratio: β_(n+1)/β_n ≈ Φ^(1/3) ≈ 1.17480
Universalitäts-Hypothese: ABGELEHNT (F-Test, α=0.05)
```

## Installation

```bash
pip install beta-clustering-utac
```

## Quickstart

```bash
uv sync
uv run python -c "
from beta_clustering import BetaClusteringUTAC
s = BetaClusteringUTAC()
r = s.run_cycle()
print(f'Systeme: {r[\"n_systems\"]}')
print(f'Φ^(1/3): {r[\"phi_cuberoot\"]:.5f}')
print(f'Inter-Cluster-Ratio: {r[\"inter_cluster_ratio\"]:.4f}')
print(f'Universalität abgelehnt: {r[\"universality_rejected\"]}')
"
```

## Diamond Interface

```python
from beta_clustering import BetaClusteringUTAC

system = BetaClusteringUTAC()

# Vollständige Analyse
result = system.run_cycle(n_systems=78)

# CREP-Zustand
crep = system.get_crep_state()   # {C, R, E, P, gamma}

# UTAC-Zustand
utac = system.get_utac_state()   # {H, K, r, sigma, beta_mean}

# Phasenübergänge (Cluster-Grenzen)
events = system.get_phase_events()

# Zenodo-Metadaten
record = system.to_zenodo_record()

# Φ^(1/3) Skalierungsratio
ratio = system.phi_scaling_ratio()  # ≈ 1.174

# Domain-β-Karte
mapping = system.domain_beta_map()  # {domain: beta_centre}
```

## Struktur

```
src/beta_clustering/
├── system.py              # BetaClusteringUTAC — Diamond Interface
├── constants.py           # Φ, Φ^(1/3), Domain-Cluster-Zentren
├── beta_estimator.py      # MLE β-Schätzung aus Schwellendaten
├── cluster_detector.py    # Domänenspezifische Cluster-Erkennung
├── phi_scaling.py         # Φ^(1/3) Inter-Cluster-Analyse
├── domain_mapper.py       # Domain → β-Cluster Mapping
├── crep_bridge.py         # β ↔ Γ Beziehung (CREP-Kopplung)
├── universality_test.py   # Einweg-ANOVA (Universalität vs. Domain-spez.)
└── benchmark.py           # Validierung gegen UTAC v1.0 Targets
```

## Falsifizierbare Vorhersage

Φ^(1/3)-Skalierung sollte halten, wenn neue Domains (seismisch, Quanten, zellulär) hinzugefügt werden. Jede Domain mit Inter-Cluster-Ratio signifikant ≠ 1.174 falsifiziert die Behauptung.

## Tests & Qualität

```bash
uv run pytest                     # 27 Tests, 90% Coverage
uv run mypy src/beta_clustering/  # Keine Fehler (strict mode)
uv run ruff check .               # Keine Fehler
```

## Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PLACEHOLDER.svg)](https://doi.org/10.5281/zenodo.PLACEHOLDER)

DOI will be assigned automatically on first GitHub Release once
Zenodo–GitHub integration is enabled for this repo. Until then, cite the
existing concept DOI above (`10.5281/zenodo.17472834`).

```bibtex
@software{roemer_beta_clustering_utac_2025,
  author    = {Römer, Johann},
  title     = {beta-clustering-utac: β-Clustering over 78 Threshold Systems},
  year      = {2025},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.17472834},
  url       = {https://doi.org/10.5281/zenodo.17472834},
  version   = {1.0.0},
  note      = {GenesisAeon Package 32 — MOR Research Collective}
}
```

---

Auch enthalten: `diamond-setup` — universales Python-Projekt-Scaffold. Siehe [`README_QUICKSTART.md`](README_QUICKSTART.md).

---

GenesisAeon · MOR Research Collective · Johann Römer · Mai 2026
