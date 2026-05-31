"""beta-clustering-utac — Package 32 of GenesisAeon.

β-Clustering across 78 threshold systems with Φ^(1/3) inter-cluster scaling.
DOI: 10.5281/zenodo.17472834
"""
from beta_clustering.constants import BETA_TARGETS, PHI, PHI_CUBEROOT
from beta_clustering.system import BetaClusteringUTAC

__version__ = "0.1.0"
__all__ = ["BetaClusteringUTAC", "PHI", "PHI_CUBEROOT", "BETA_TARGETS"]
