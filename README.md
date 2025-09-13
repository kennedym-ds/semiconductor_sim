# SemiconductorSim

SemiconductorSim is an open-source Python library designed to simulate fundamental semiconductor devices, making complex semiconductor physics accessible to undergraduate students. Accompanied by interactive tutorials and comprehensive examples, this library serves as a valuable educational tool for students, educators, and enthusiasts in the fields of electronics and semiconductor engineering.

![CI](https://github.com/kennedym-ds/semiconductor_sim/actions/workflows/ci.yml/badge.svg)
![CodeQL](https://github.com/kennedym-ds/semiconductor_sim/actions/workflows/codeql.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/semiconductor-sim.svg)](https://pypi.org/project/semiconductor-sim/)
![Python](https://img.shields.io/pypi/pyversions/semiconductor-sim.svg)
![License](https://img.shields.io/github/license/kennedym-ds/semiconductor_sim.svg)
[![Coverage](https://codecov.io/gh/kennedym-ds/semiconductor_sim/branch/main/graph/badge.svg)](https://codecov.io/gh/kennedym-ds/semiconductor_sim)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-blue.svg)](https://kennedym-ds.github.io/semiconductor_sim/)

## 🧭 Table of Contents

- Installation
- Features
- Supported Devices
- Quickstart
- Examples & Docs
- Units & Conventions
- Interactive Notebooks
- Development
- Troubleshooting
- Contributing
- License
- Releases

## 📚 Features

- **Device Simulation**: PN Junction Diode, LED, Solar Cell, Tunnel, Varactor, Zener, MOS Capacitor
- **Physical Models**: SRH recombination, temperature dependence, emission models
- **Parameter Validation**: Optional pydantic-based schemas with clear error messages ⭐ NEW
- **Material Presets**: Pre-configured properties for Si, GaAs, Ge, GaN, InP ⭐ NEW  
- **Interactive Visualizations**: Jupyter widgets and Plotly/Matplotlib support
- **Educational Focus**: Teaching-oriented models with comprehensive documentation

## 🧪 Supported Devices

- PN Junction Diode: Ideal diode with SRH recombination and temperature effects.
- LED: Diode IV with emission intensity; simple efficiency model.
- Solar Cell: IV under illumination; short/open-circuit conditions.
- Tunnel Diode: Simplified IV with correct reverse-bias behavior for teaching.
- Varactor Diode: Junction capacitance vs. reverse bias; IV characteristic.
- Zener Diode: Breakdown behavior with optional ML-predicted Zener voltage.
- MOS Capacitor: C–V and I–V characteristics with depletion width model.

## 🔧 Installation

Install from PyPI (recommended):

```bash
# Standard installation
pip install semiconductor-sim

# With parameter validation and material presets
pip install semiconductor-sim[schemas]  # ⭐ RECOMMENDED
```

From source (editable):

```bash
git clone https://github.com/kennedym-ds/semiconductor_sim.git
cd semiconductor_sim
python -m venv .venv
. .venv/Scripts/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .
```

## 🚀 Quickstart

### Traditional Approach
```python
import numpy as np
from semiconductor_sim.devices import PNJunctionDiode

diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
V = np.array([0.0, 0.2, 0.4])
I, R = diode.iv_characteristic(V, n_conc=1e16, p_conc=1e16)
print("Current:", I)
print("Recombination (SRH):", R)
```

### New: Material Presets ⭐
```python
from semiconductor_sim import PNJunctionDiode, LED

# Create devices with realistic material properties
si_diode = PNJunctionDiode.from_preset("Si", doping_p=1e16, doping_n=1e17)
gaas_led = LED.from_preset("GaAs", doping_p=1e17, doping_n=1e18, efficiency=0.8)

# Automatic parameter validation with helpful error messages
V = np.linspace(0, 1, 100)
current, emission = gaas_led.iv_characteristic(V)
```

## 📓 Examples & Docs

- **Material Presets & Validation**: See [Parameter Schemas and Material Presets Guide](docs/schemas_and_presets.md) ⭐ NEW
- **Example Scripts**: Browse the `examples/` folder for complete demonstration scripts
- **Interactive Notebooks**: Check `examples/` for Jupyter notebooks using ipywidgets/plotly
- **API Documentation**: Explore module docstrings and inline help until hosted docs are available

## 📐 Units & Conventions

- Length: cm; Area: cm²; Volume: cm³; Charge: C; Capacitance: F.
- Doping and carrier concentrations: cm⁻³.
- Temperature: K (default `DEFAULT_T = 300 K`).
- Constants available via `semiconductor_sim.utils.constants`: `q`, `k_B`, `epsilon_0`, `DEFAULT_T`.
- Return shapes: device `iv_characteristic` methods return arrays aligned to the input `voltage_array`. Where scalar recombination is computed, it is broadcast to match the voltage vector.

## 💡 Interactive Notebooks

- Explore interactive notebooks in `examples/` with Jupyter and ipywidgets.
- Launch Jupyter:

```bash
python -m pip install jupyter ipywidgets
jupyter notebook examples
```

If running on a headless server/CI, plotting uses Matplotlib’s
non-interactive backend automatically inside plotting helpers.

## 🖼️ Plotting Helper (Headless-Safe)

To keep plots consistent and CI-friendly, device plotting functions call
lightweight helpers:

- `semiconductor_sim.utils.plotting.use_headless_backend("Agg")`:
  switch to a non-interactive backend before any figures are created.
- `semiconductor_sim.utils.plotting.apply_basic_style()`:
  apply minimal, consistent rcParams (grid, sizes, legend).

When writing new scripts that use Matplotlib directly, you can opt-in to the
same behavior:

```python
from semiconductor_sim.utils.plotting import (
  use_headless_backend,
  apply_basic_style,
)
use_headless_backend("Agg")
apply_basic_style()

import matplotlib.pyplot as plt
# ... your plotting code ...
```

Notes:

- Prefer relying on device `.plot_*` helpers where available.
- Avoid calling `plt.switch_backend` at runtime; set backend via the helper
  before any figures are created.

## 🧑‍💻 Development

Set up a virtual environment and install dev tools:

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .
pip install ruff mypy pytest pre-commit
pre-commit install
```

Run checks:

```bash
ruff check .
ruff format --check .
mypy .
pytest -q
```

CI runs Ruff, Mypy, and tests across Python 3.10–3.13 on
Linux/Windows/macOS with coverage thresholds. It includes dependency
review, pip-audit security checks, and CodeQL scanning. Dependabot keeps
GitHub Actions and pip dependencies updated. Publishing to PyPI is
automated on tags `v*.*.*`. See `CHANGELOG.md` for notable changes.

## 🩺 Troubleshooting

- "FigureCanvasAgg is non-interactive" warnings: safe to ignore in headless runs.
- Missing ML model for Zener voltage: library falls back to the configured
  default and prints a notice. You can train your own model and place the
  `zener_voltage_rf_model.pkl` under `semiconductor_sim/models/` if desired.
- On Windows, ensure you activate the venv before running commands:

```powershell
. .\.venv\Scripts\Activate.ps1
```

## 🤝 Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` for guidelines. Typical flow:

```bash
git checkout -b feature/my-improvement
ruff check . && mypy . && pytest -q
```

Open a PR; CI runs lint, types, tests, CodeQL, and dependency review.

## 📄 License

This project is licensed under the MIT License — see `LICENSE`.

## 🏷️ Releases

- Versioning: semantic (`MAJOR.MINOR.PATCH`).
- Publishing: push a tag like `v0.1.1` to trigger the publish workflow.
