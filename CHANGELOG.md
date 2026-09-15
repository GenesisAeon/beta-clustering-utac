# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.1.1] - 2026-09-15

### Fixed (real, verified false claim -- documentation only, no numeric value change)
- `crep_bridge.py`'s comment "σ≈2.2 emerges from the β distribution
  (UTAC v1.0 finding)" does NOT hold up: running this package's own
  `sigma_from_beta_distribution()` on its own data (both the default
  synthetic 78-system generator and the literature-citing
  `data/utac_v1_78_systems.yaml`) gives σ≈1.28, not 2.2 — a ~42%
  discrepancy, verified numerically. `BETA_SCALE=2.2` is the same
  shared cross-package default reused unchanged across unrelated
  GenesisAeon UTAC packages, not an independently derived result for
  this domain. Also documented a related, previously-undiscovered
  disconnect: `system.py`'s `_build_crep_state()` always uses this
  hardcoded default via `beta_to_gamma()`, never the
  `sigma_from_beta_distribution()` value that `_run_cycle()` computes
  and reports separately — the same "measured-but-unused" pattern
  found in `amoc-utac`. Numeric value of `BETA_SCALE` is unchanged;
  only the false claim is corrected. Updated `crep_bridge.py`,
  `.zenodo.json`. See
  `D:\mandala\crep-utac-afet-formalism\FOLLOWUP_TICKETS.md` for the
  full finding.

### Fixed (test compatibility with diamond-setup 2.3.0)
- `test_get_crep_state_keys` asserted an exact key set for
  `get_crep_state()`'s output, which broke when `diamond-setup` 2.3.0
  added an additive `bridge_adapted` field to `CREPState`. Changed to
  a subset check so future additive protocol fields don't break this
  test again.

## [1.1.0] - 2026-07-01
### Changed
- `BetaClusteringUTAC` subclasses `diamond_setup.DiamondPackage` (reference migration).
- `diamond-setup>=2.1.0` as runtime dependency; vendored `src/diamond_setup/` removed.
- `get_crep_state` / `get_utac_state` raise `NotConvergedError` before first `run_cycle`.
- UTAC keys: `{H, H_star, K_eff}`; CREP key `Gamma` (was `gamma`).

## [1.0.0] - 2026
### Added
- Initial v1.0.0 release as part of the GenesisAeon ecosystem-wide 1.0.0
  milestone.
- Standardized release tooling: `.zenodo.json` (Zenodo community entry),
  `RELEASE_GUIDE.md`, `CONTRIBUTING.md`, issue/PR templates.

### Changed
- Project metadata (`pyproject.toml`) corrected: `[project].name` now
  reads `beta-clustering-utac` (previously `diamond-setup`, a leftover
  from the bundled scaffold tool), description, authors, and project URLs
  updated to match the actual package and its Zenodo DOI
  (10.5281/zenodo.17472834).
