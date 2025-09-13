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
- Command Line Interface (CLI)
- Units & Conventions
- Interactive Notebooks
- Development
- Troubleshooting
- Contributing
- License
- Releases

## 📚 Features

- PN Junction Diode Simulation: IV, SRH recombination, temperature dependence
- LED Simulation: IV with emission, efficiency model, temperature effects
- Solar Cell Simulation: IV under illumination, short/open-circuit conditions
- Tunnel, Varactor, Zener, MOS Capacitor: teaching-focused models and plots
- Interactive Visualizations: Jupyter widgets and Plotly/Matplotlib support
- **Command Line Interface**: Generate IV/CV characteristics and parameter sweeps headlessly
- Documentation: API references, tutorials, and example scripts

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
pip install semiconductor-sim
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

Minimal PN junction example (no plotting required):

```python
import numpy as np
from semiconductor_sim.devices import PNJunctionDiode

diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
V = np.array([0.0, 0.2, 0.4])
I, R = diode.iv_characteristic(V, n_conc=1e16, p_conc=1e16)
print("Current:", I)
print("Recombination (SRH):", R)
```

LED quick preview (two-value return when concentrations omitted):

```python
import numpy as np
from semiconductor_sim.devices import LED

led = LED(doping_p=1e17, doping_n=1e17, temperature=300)
V = np.linspace(0, 2, 5)
current, emission = led.iv_characteristic(V)
```

## 📓 Examples & Docs

- Examples: see the `examples/` folder for scripts and Jupyter notebooks (interactive versions use ipywidgets/plotly).
- API docs: browse module docstrings and examples until hosted docs are added.

## 🖥️ Command Line Interface (CLI)

The `semiconductor-sim` command provides a convenient CLI for quick device simulations and batch processing:

### Installation & Setup

After installing the package, the CLI is available as:

```bash
semiconductor-sim --help
```

### Available Commands

- `iv`: Generate current-voltage characteristics
- `cv`: Generate capacitance-voltage characteristics (capacitive devices)
- `sweep`: Perform parameter sweeps

### Quick Examples

**IV Characteristics:**
```bash
# PN Junction
semiconductor-sim iv pn_junction --config examples/cli_configs/pn_junction.json \
  --output-csv pn_iv.csv --output-png pn_iv.png

# LED
semiconductor-sim iv led --config examples/cli_configs/led.json \
  --voltage-start 0 --voltage-stop 3 --output-png led_iv.png
```

**CV Characteristics:**
```bash
# MOS Capacitor
semiconductor-sim cv mos_capacitor --config examples/cli_configs/mos_capacitor.yaml \
  --output-csv mos_cv.csv --output-png mos_cv.png
```

**Parameter Sweeps:**
```bash
# Temperature sweep
semiconductor-sim sweep pn_junction --config examples/cli_configs/pn_junction.json \
  --sweep-param temperature --sweep-start 250 --sweep-stop 350 --sweep-points 5 \
  --output-png temp_sweep.png

# Doping concentration sweep
semiconductor-sim sweep pn_junction --config examples/cli_configs/pn_junction.json \
  --sweep-param doping_p --sweep-start 1e16 --sweep-stop 1e18 --sweep-points 4 \
  --output-png doping_sweep.png
```

### Configuration Files

Device parameters are specified in JSON or YAML format:

**JSON Example (`pn_junction.json`):**
```json
{
  "doping_p": 1e17,
  "doping_n": 1e17,
  "area": 1e-4,
  "temperature": 300,
  "tau_n": 1e-6,
  "tau_p": 1e-6
}
```

**YAML Example (`mos_capacitor.yaml`):**
```yaml
doping_p: 1.0e+17
oxide_thickness: 1.0e-6
oxide_permittivity: 3.45
area: 1.0e-4
temperature: 300
```

### Device Types & Parameters

- `pn_junction`: PN Junction Diode
- `led`: Light Emitting Diode  
- `solar_cell`: Solar Cell
- `zener`: Zener Diode
- `mos_capacitor`: MOS Capacitor
- `tunnel_diode`: Tunnel Diode
- `varactor`: Varactor Diode

See `examples/cli_configs/` for sample configuration files for each device type.

### Demo Script

Run the complete CLI demo:

```bash
bash examples/cli_demo.sh
```

This generates example outputs for all device types and demonstrates the CLI capabilities.

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
