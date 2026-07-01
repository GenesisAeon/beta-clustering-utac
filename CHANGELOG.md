# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
