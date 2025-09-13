# Contributing to SemiconductorSim

Thank you for helping improve SemiconductorSim! Contributions of all kinds are
welcome — bug reports, feature requests, docs, tests, and code.

## Quick Start (Windows PowerShell)

- Clone your fork:
  `git clone https://github.com/<your-username>/semiconductor_sim.git; \
  cd semiconductor_sim`
- Create and activate a virtual environment:
  - `python -m venv .venv; .\.venv\\Scripts\\Activate.ps1`
- Install the package and dev tools:
  - Preferred: `pip install -e .[dev]`
  - Or: `pip install -r requirements-dev.txt` then `pip install -e .`
  - Minimal runtime only (no dev tools): `pip install -r requirements.txt`
  - Optionally: `pip install pre-commit`
- Enable pre-commit hooks: `pre-commit install`
- Run tests: `pytest -q`

## Development Workflow

1. Create a branch: `git checkout -b feature/<short-desc>` or `fix/<short-desc>`
2. Make focused changes with tests where applicable.
3. Lint and type-check locally: `ruff check .; mypy semiconductor_sim`
4. Run tests with coverage: `coverage run -m pytest -q; coverage report`
5. Commit using Conventional Commits (see below) and open a PR.

## Conventional Commits

Use the format: `<type>(optional scope): <short summary>`

Common types:

- `feat`: new capability
- `fix`: bug fix
- `docs`: documentation only
- `refactor`: code change that neither fixes a bug nor adds a feature
- `test`: add or improve tests
- `build/ci`: packaging, deps, CI/CD
- `chore`: maintenance

Examples:

- `feat(led): add quantum efficiency parameter`
- `fix(tunnel): correct reverse-bias current sign`

## Code Style and Quality

- Formatting/linting: Ruff (`ruff.toml` defines rules). Run `ruff check .` and
  `ruff format .`.
- Types: Mypy (`mypy.ini`). Prefer precise types and avoid `Any` where feasible.
- Tests: Pytest (`pytest.ini`). Place tests in `tests/` and keep them fast and deterministic.
- Plotting: Ensure non-interactive backends (Agg) for CI; avoid GUI-only calls
  in library code.
- Public API: Maintain backward compatibility or document breaking changes
  clearly in the changelog and PR.

## Project Structure

- Library code: `semiconductor_sim/`
- Device models: `semiconductor_sim/devices/`
- Physical models: `semiconductor_sim/models/`
- Utilities/constants: `semiconductor_sim/utils/`
- Examples and notebooks: `examples/`
- Tests: `tests/`

## Running the Test Suite

- Quick: `pytest -q`
- With coverage: `pytest --cov=semiconductor_sim --cov-report=term-missing`
- Selected tests: `pytest tests/test_led.py -q`

## Docs

- The README covers quickstart. The site uses MkDocs Material.
- Build locally: `pip install mkdocs-material; mkdocs serve`
- Docs live in `docs/`; the config is `mkdocs.yml`.

## Pull Request Template

Please use the project PR template to provide context and validation steps:

- [PR template](.github/pull_request_template.md)

It includes acceptance criteria and a QA checklist (lint, types, tests,
headless plotting, and packaging metadata updates when needed).

## Submitting a Pull Request

- Fill in the PR template with context and validation steps.
- Include tests for new behavior and bug fixes.
- Keep PRs focused and under ~400 lines of diff when possible.
- Ensure CI passes (lint, type checks, tests).

## QA Checks (Quick Reference)

Run the core quality checks locally before pushing:

```powershell
ruff check .
ruff format --check .
mypy .
pytest -q
```

## Git Hooks (pre-commit / pre-push)

This repo includes hooks that mirror CI checks to catch issues before they
hit the pipeline.

- Install once: `pip install pre-commit`; then `pre-commit install`
- Also enable pre-push hooks: `pre-commit install --hook-type pre-push`
- Run on all files: `pre-commit run --all-files`

Pre-push runs tests, docs build (strict), pip-audit, and a smoke import. If a
hook fails, fix the issues and re-run.

Required local tools for pre-push hooks:

- coverage: `pip install coverage`
- docs: `pip install mkdocs-material mkdocstrings mkdocstrings-python`
- security: `pip install pip-audit`

Alternatively, install all dev tooling:

```powershell
pip install pre-commit ruff mypy pytest coverage
pip install mkdocs-material mkdocstrings mkdocstrings-python pip-audit
```

## VS Code Tasks (using .venv)

This repo ships workspace tasks under `.vscode/tasks.json` that use the
local virtual environment explicitly.

- Open the Command Palette → "Run Task" and pick one of:
  - `venv: install dev` — install `requirements-dev.txt` and the package
    in editable mode
  - `venv: lint (ruff)` — run linting
  - `venv: types (mypy)` — run type checks
  - `venv: test + coverage` — run tests with coverage gate (80%)
  - `venv: docs (strict)` — build docs in strict mode
  - `venv: security audit` — run `pip-audit`
  - `venv: pre-commit (all files)` — run all hooks
  - `venv: build package` — build sdist/wheel with `python -m build`

These tasks assume Windows PowerShell and a `.venv` in the project root.

## Security and Dependencies

- Avoid introducing heavy dependencies; prefer NumPy/SciPy.
- If adding a dependency, justify it in the PR and update
  `pyproject.toml` and/or `requirements.txt`.
- Secrets: never commit credentials. Use GitHub Secrets for CI if needed.

## Releases

- We follow SemVer. Changelog entries should be added under the Unreleased section.
- Publishing is automated via GitHub Actions on tagged releases.

Thank you for contributing — we appreciate your time and expertise!
