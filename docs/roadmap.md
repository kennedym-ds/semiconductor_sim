# Roadmap & Phased Plan

This roadmap focuses on teaching and learning with SemiconductorSim.
It spells out concrete phases so contributors and instructors can track
progress and plan lessons.

## Status Overview

- Completed: Phase 0 (Baseline), Phase 1 (Hygiene), Phase 2 (Tutorials & Gallery),
  Phase 3 (Interactivity), Phase 4 (Materials & Models)
- In Progress: Phase 6 (Plotting API Unification – partial via helpers)
- Next Up: Phase 5 (New Devices), Phase 8 (CLI Enhancements), Phase 7 (Units – optional)

## Phased Plan

### Phase 0 — Decisions & Baseline

- ADR: Standardize device return tuples for `iv_characteristic`
  (ordering, names, shapes).
- Hygiene: Keep CI green; baseline Ruff/mypy/tests/docs.
- Acceptance: ADR merged in docs; Ruff + mypy clean; tests unchanged or
	improved.

### Phase 1 — Hygiene & Test Coverage (Completed)

- Ruff modernizations: Optional/Union → `X | Y`, `Tuple` → `tuple` where
  sensible. Clarify import-location rule for lazy matplotlib imports.
- Types: Remove Any-return warnings (notably in recombination and MOS
  capacitor) with precise NumPy typing.
- Tests: Improve LED/Zener coverage; add headless plot smoke tests.
- Acceptance: Ruff and mypy pass; coverage ≥ 90% on core devices; docs
  build strict OK.

### Phase 2 — Tutorials, Gallery, Glossary (Completed)

- Three guided labs: PN basics, LED, Solar — with goals, prompts, and
  solutions.
- Docs: Example gallery, glossary of terms/symbols/units, troubleshooting.
- Acceptance: Pages linked in nav; notebooks run; CI docs job green.

### Phase 3 — Interactivity (Completed)

- ipywidgets: canonical slider notebooks per device (doping, temperature,
  illumination).
- Demo App: minimal Panel or Streamlit app to compare PN/LED.
- Acceptance: Notebooks interactive; app launches locally; short guide
  included.

### Phase 4 — Materials & Models (Completed)

- Materials registry: Si/Ge/GaAs Varshni parameters; integrate with
  bandgap and intrinsic carrier density.
- Optional: simple mobility vs. doping/temperature for teaching.
- Acceptance: Tested registry; devices can opt into materials; docs
  reference sources.

### Phase 5 — New Devices (Teaching-Simple) [In Progress]

- Schottky diode (added) → next: PIN + photodiode → MOSFET (intro) → BJT (intro).
- Each device: consistent API, docstrings with assumptions/units, example
  script, one notebook, tests.
- Acceptance: Each device meets the above; CI remains green.

### Phase A — Foundations (Mobility, SRH, Schottky) [In Progress]

- Models: Caughey–Thomas mobility (mu_n, mu_p); SRH recombination rate utility.
- Device: Schottky diode (thermionic emission) with docs and gallery.
- Docs: API sections for materials/models/devices updated; gallery entry added.
- CI: Gallery generator and checks extended for new image.
- Acceptance: Lint/type/tests/docs all green; examples render headless;
  image present in gallery.

### Phase 6 — Plotting API Unification (In Progress)

- Centralize plotting helpers; optional backend selection
  (matplotlib/plotly) in one place.
- Acceptance: All device plots run headless in CI; one plotting guide in
  docs.

### Phase 7 — Optional Units with Pint (Feature-Flag)

- Offer unit-safe examples behind a toggle, not a hard dependency.
- Acceptance: Unit-enabled examples run; docs explain tradeoffs.

### Phase 8 — CLI Enhancements

- Extend `semisim` with ranges/export (CSV/PNG) and tests.
- Acceptance: CLI paths covered; docs include quickstart.

### Phase 9 — Release v0.2.0 (Planned)

- Version bump, changelog, docs refresh, highlights in README.
- Acceptance: CI+publish succeed; release notes emphasize learning features
  and new devices.

## Learning Themes (Ongoing)

- Tutorials & Exercises: parameter sweeps, IV fitting with
  `scipy.optimize.curve_fit`.
- Concept Visuals: depletion width, band diagrams, quasi-Fermi levels.
- Contribution Tasks: good-first-issues for labs, plots, and gallery
  entries.

## Notes on Scope & Style

- Keep models “teaching-simple,” with clear defaults and explicit units.
- Prefer vectorized NumPy implementations and headless-safe plotting.
- Document assumptions and cite sources for parameters where practical.

---

Contributions welcome! Open an issue or PR with a small, focused change.
