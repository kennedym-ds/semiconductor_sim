# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [Unreleased]

- Nothing yet.

## [1.0.3] - 2025-09-14

### Changed (1.0.3)

- Patch release to publish cumulative fixes: typing updates,
  strict docs, and packaging cleanup since 1.0.2.

## [1.0.2] - 2025-09-14

### Changed (1.0.2)

- Migrated type annotations from bare `np.ndarray` to
  `numpy.typing.NDArray[np.floating]` across devices and models to
  satisfy `mypy` with `disallow_any_generics = True` on Linux/macOS.
- Harmonized plotting/type signatures and generalized docstrings to
  avoid `np.ndarray` mentions.

### Fixed (1.0.2)

- Resolved indentation/return placement issues in `solar_cell.py`,
  `photodiode.py`, and `zener_diode.py` introduced during typing pass.
- Addressed Ruff B905 by enforcing `zip(..., strict=True)` in gallery
  generation script.
- Verified strict docs build and full test suite (coverage ≥ 80%) pass locally.

## [1.0.0] - 2025-09-14

### Added (1.0.0)

- BJT device model with Early effect and complementary `PNP` variant.
- Gallery generation script now includes BJT transfer and
  output plots; added tiles and ordering.
- Tests expanded for BJT/PNP and Schottky edge cases; total coverage ~84%.
- VS Code tasks: combined docs build (images + strict) and pre-push suite.
- Docs workflow hardened: generate gallery before strict build,
  add concurrency, upload artifacts.

### Changed (1.0.0)

- Documentation updated for BJT/PNP with examples and images; gallery reordered.
- Pre-commit config and workflows tuned for stability on Windows and CI.

### Fixed (1.0.0)

- Stabilized BJT near-cutoff test threshold and removed magic number per linter.

## [0.1.1] - 2025-09-13

### Added (0.1.1)

- PEP 561 typing marker `py.typed` and MANIFEST entries to ship types.
- MkDocs strict build in CI and docs deployment workflow.
- Repo hygiene: comprehensive `.gitignore`, markdown lint fixes,
  simplified `CODEOWNERS`.

### Changed (0.1.1)

- Packaging metadata polish (SPDX license, keywords, classifiers,
  URLs for Bugs/Changelog).
- Standardized plotting helpers (e.g., MOS `plot_capacitance_vs_voltage`
  computes capacitance internally).
- Examples aligned to consistent `main()` structure and imports.

### Fixed (0.1.1)

- Twine metadata checks pass; wheels now include `py.typed`.

### Added

- Pre-commit config with Ruff/Mypy hooks
- GitHub workflows for CI, CodeQL, dependency review, docs deploy, and publish
- MkDocs site scaffold and docs pages
- Issue/PR templates and Code of Conduct
- PEP 621 metadata in `pyproject.toml`
- Dependabot for `github-actions` and `pip`
- Pip-audit security check in CI
- Smoke install/import job in CI

### Changed

- README overhaul with badges, quickstart, troubleshooting
- CONTRIBUTING guide updated for Windows-friendly setup and workflow
- CI matrix expanded to Linux/Windows/macOS and Python 3.10–3.13
- Coverage threshold enforced in CI

### Fixed

- Radiative recombination formula using `n_i^2`
- LED return signature alignment with tests
- Broadcast recombination arrays across device models
- Headless-safe plotting using Agg backend
- Tunnel diode reverse-bias current sign

## [0.1.0] - 2025-09-13

### Initial

- Initial release on PyPI with core device models
  (PN junction, LED, MOS capacitor, solar cell, tunnel diode,
  varactor, zener) and utilities.
