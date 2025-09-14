# Copilot Instructions for SemiconductorSim

Purpose: help AI coding agents work effectively in this repository without extra back-and-forth. Keep changes minimal, typed, and CI-aligned.

## Project Overview
- Library: `semiconductor_sim` — teaching-first device simulations (PN, LED, Solar, MOS-C, Zener, Varactor, Tunnel, BJT, etc.).
- Structure: `semiconductor_sim/{devices,models,materials,utils}` + `examples/`, `tests/`, `docs` via MkDocs Material.
- Public API patterns:
  - Base class `Device` in `semiconductor_sim/devices/base.py` with `iv_characteristic(voltage_array, n_conc=None, p_conc=None) -> tuple[np.ndarray, ...]`.
  - Implementations return a tuple; first item is always current array aligned to input voltage; extra arrays are model outputs (e.g., SRH recombination for PN, emission for LED).
  - Units: cm, cm^2, cm^3, K; constants in `semiconductor_sim.utils.constants` (e.g., `q`, `k_B`, `DEFAULT_T`).

## Conventions & Typing
- Use NumPy typing: `numpy.typing.NDArray[np.floating]` for arrays; broadcast outputs to match input shapes (`np.broadcast_to`).
- Prefer `semiconductor_sim.utils.numerics.safe_expm1` for numerical stability in diode equations.
- Keep plotting headless-safe using `semiconductor_sim.utils.plotting.use_headless_backend("Agg")` and `apply_basic_style()` before creating figures.
- Follow Ruff and Mypy configs in `ruff.toml` and `mypy.ini` (line length 100; disallow_any_generics = True). Short math-like names allowed in tests/examples only (see per-file-ignores).

## Developer Workflows
- Local checks (Windows PowerShell examples):
  - Lint: `.\.venv\Scripts\python.exe -m ruff check .`
  - Format check: `.\.venv\Scripts\python.exe -m ruff format --check .`
  - Types: `.\.venv\Scripts\python.exe -m mypy .`
  - Tests + coverage: `.\.venv\Scripts\python.exe -m coverage run -m pytest -q; .\.venv\Scripts\python.exe -m coverage report --fail-under=80`
  - Docs (strict): `.\.venv\Scripts\python.exe -m mkdocs build --strict`
  - Pre-push hooks mirror CI: `.\.venv\Scripts\pre-commit.exe run --hook-stage pre-push --all-files`
- VS Code tasks available for all the above (see workspace tasks list).
- CI (`.github/workflows/ci.yml`): matrix on Ubuntu/Windows/macOS and Python 3.10–3.13; runs Ruff, Mypy, tests with coverage, pip-audit, and strict docs. Coverage uploaded via Codecov OIDC. Artifacts are named per-OS/Python.
- Release: tag `v*.*.*` triggers `publish.yml` (Trusted Publishing to PyPI). Keep `pyproject.toml` version synced with tags.

## Patterns to Follow (examples)
- New device class skeleton:
  ```python
  import numpy as np
  import numpy.typing as npt
  from semiconductor_sim.utils import k_B, q, DEFAULT_T
  from semiconductor_sim.utils.numerics import safe_expm1
  from .base import Device

  class MyDevice(Device):
      def __init__(self, area: float = 1e-4, temperature: float = DEFAULT_T, ...):
          super().__init__(area=area, temperature=temperature)
          # store parameters as float(...)

      def iv_characteristic(
          self,
          voltage_array: npt.NDArray[np.floating],
          n_conc: float | npt.NDArray[np.floating] | None = None,
          p_conc: float | npt.NDArray[np.floating] | None = None,
      ) -> tuple[npt.NDArray[np.floating], ...]:
          V_T = k_B * self.temperature / q
          I = safe_expm1(voltage_array / V_T)  # scale appropriately
          # other outputs...
          return np.asarray(I, dtype=float),
  ```
- Broadcasting auxiliary outputs to `voltage_array` shape:
  ```python
  out = np.broadcast_to(out, np.shape(voltage_array))
  ```
- CLI demo pattern in `semiconductor_sim/cli.py` shows simple numeric demos and `zip(..., strict=False)` for consistent iteration.

## Testing & Examples
- Tests live in `tests/` and assert shapes/units consistency (see `tests/test_pn_junction.py`, `tests/test_led.py`, etc.). Use deterministic arrays and avoid GUI dependencies (tests set `MPLBACKEND=Agg` in `tests/conftest.py`).
- Examples in `examples/` demonstrate typical usage; keep APIs stable with these usages.

## Docs
- MkDocs config in `mkdocs.yml` with mkdocstrings; keep docstrings Google-style, include parameter/return descriptions. New public classes/functions should be discoverable by mkdocstrings.

## Housekeeping
- Don’t commit caches: `.hypothesis`, `.pytest_cache`, `.mypy_cache`, `build/`, `dist/`. Pre-commit is configured to ignore these. If pre-commit touches them locally, do not add them to git.
- Keep changes minimal and within existing style; avoid unrelated refactors in the same PR.

## Where to Start
- Adding/adjusting a device: mirror patterns in `semiconductor_sim/devices/` (use `PNJunctionDiode` as a reference).
- Numeric helpers/constants: `semiconductor_sim/utils/`.
- Materials and models: `semiconductor_sim/materials/`, `semiconductor_sim/models/` for reusable physics pieces.
