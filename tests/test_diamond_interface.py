"""Tests for the BetaClusteringUTAC Diamond-Template interface (Package 32)."""

from __future__ import annotations

import pytest
from diamond_setup.protocol import NotConvergedError
from diamond_setup.validation import validate_diamond_instance

from beta_clustering.system import BetaClusteringUTAC


@pytest.fixture(scope="module")
def beta_cluster() -> BetaClusteringUTAC:
    system = BetaClusteringUTAC()
    system.run_cycle()
    return system


def test_not_converged_before_run_cycle():
    pkg = BetaClusteringUTAC()
    with pytest.raises(NotConvergedError):
        pkg.get_crep_state()


def test_validate_diamond_instance():
    pkg = BetaClusteringUTAC()
    assert validate_diamond_instance(pkg) == []


def test_run_cycle_returns_dict():
    result = BetaClusteringUTAC().run_cycle()
    assert isinstance(result, dict)


def test_get_crep_state_keys(beta_cluster: BetaClusteringUTAC):
    state = beta_cluster.get_crep_state()
    assert set(state.keys()) == {"C", "R", "E", "P", "Gamma"}


def test_get_crep_state_range(beta_cluster: BetaClusteringUTAC):
    state = beta_cluster.get_crep_state()
    for k, v in state.items():
        assert v is not None
        assert 0.0 <= v <= 1.0, f"CREP component {k}={v} outside [0, 1]"


def test_get_utac_state_keys(beta_cluster: BetaClusteringUTAC):
    state = beta_cluster.get_utac_state()
    assert set(state.keys()) == {"H", "H_star", "K_eff"}


def test_get_phase_events_is_list(beta_cluster: BetaClusteringUTAC):
    events = beta_cluster.get_phase_events()
    assert isinstance(events, list)
    assert len(events) == 4


def test_to_zenodo_record_structure(beta_cluster: BetaClusteringUTAC):
    record = beta_cluster.to_zenodo_record()
    for key in ("title", "description", "creators", "doi", "package"):
        assert key in record