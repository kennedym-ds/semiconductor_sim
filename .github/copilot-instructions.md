# SemiconductorSim

SemiconductorSim is a Python library for simulating fundamental semiconductor devices, designed for educational use by undergraduate students. It provides device models for PN junctions, LEDs, solar cells, tunnel diodes, varactor diodes, Zener diodes, and MOS capacitors with interactive visualization capabilities.

**ALWAYS follow these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap and Setup
- Install system Python dependencies:
  - `sudo apt update && sudo apt install -y python3-numpy python3-matplotlib python3-scipy python3-joblib python3-hypothesis python3-pytest mypy python3-coverage mkdocs`
  - Takes 2-5 minutes depending on network. NEVER CANCEL.
- Create virtual environment: `python3 -m venv .venv` -- takes 3 seconds
- **CRITICAL**: pip install commands will FAIL due to firewall limitations with timeout errors like "HTTPSConnectionPool(host='pypi.org', port=443): Read timed out"
- **WORKAROUND**: Use system packages via apt instead of pip for most dependencies
- Add package to Python path: `export PYTHONPATH=/home/runner/work/semiconductor_sim/semiconductor_sim:$PYTHONPATH`

### Quality Checks (All Fast Operations)
- Run linting: **ruff not available via apt** -- skip ruff commands in this environment
- Type checking: `mypy semiconductor_sim` -- takes 1 second, finds 49 type annotation issues (expected)
- Tests: `python3 -m pytest -q` -- takes 2 seconds, 60 tests pass
- Coverage: `python3 -m coverage run -m pytest -q && python3 -m coverage report --fail-under=80` -- takes 4 seconds, achieves 91% coverage
- Docs: `mkdocs build --config-file mkdocs_basic.yml` -- takes 1 second (material theme not available)

### Package Structure and Core Commands
- **Source**: `semiconductor_sim/` contains all library code
- **Tests**: `tests/` directory with 60 comprehensive tests
- **Examples**: `examples/` with both .py scripts and .ipynb notebooks
- **Documentation**: Uses MkDocs Material (not available in this environment, use basic theme)

## Validation

### Manual Device Testing
ALWAYS validate changes by running device simulations to ensure core functionality works:

```python
import numpy as np
from semiconductor_sim.devices import PNJunctionDiode, LED, SolarCell

# Test PN Junction
diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
V = np.array([0.0, 0.2, 0.4, 0.6])
I, R = diode.iv_characteristic(V, n_conc=1e16, p_conc=1e16)

# Test LED  
led = LED(doping_p=1e17, doping_n=1e17, temperature=300)
current, emission = led.iv_characteristic(np.linspace(0, 2, 5))

# Test Solar Cell
solar_cell = SolarCell(doping_p=1e17, doping_n=1e17, temperature=300) 
I_solar = solar_cell.iv_characteristic(np.linspace(-0.5, 0.5, 5))
```

### Core Quality Workflow
ALWAYS run these commands in sequence after making changes:
```bash
export PYTHONPATH=/home/runner/work/semiconductor_sim/semiconductor_sim:$PYTHONPATH
mypy semiconductor_sim                    # Type checking (finds issues, that's expected)
python3 -m pytest -q                     # Tests (should pass 60/60)
python3 -m coverage run -m pytest -q     # Coverage
python3 -m coverage report --fail-under=80  # Verify >80% coverage
```

## Critical Environment Limitations

### Network and Package Installation
- **pip install commands WILL FAIL** with timeout errors due to firewall restrictions
- **NEVER try pip install** for dependencies -- use apt packages instead
- Virtual environments work for isolation but cannot install packages via pip
- Use `export PYTHONPATH=...` to make package importable without installation

### Available vs Unavailable Tools
**Available via apt:**
- python3-numpy, python3-matplotlib, python3-scipy
- python3-joblib, python3-hypothesis  
- python3-pytest, mypy, python3-coverage
- mkdocs (basic themes only)

**NOT available:**
- ruff (linting/formatting) -- skip ruff commands
- mkdocs-material theme -- use basic mkdocs theme
- plotly, ipywidgets (for interactive examples) -- examples may fail
- pre-commit hooks -- cannot install

### Timing Expectations
All operations are FAST in this environment:
- Virtual environment creation: 3 seconds
- System package installation: 2-5 minutes first time, instant if cached
- Test suite: 2 seconds for 60 tests  
- Type checking: 1 second
- Coverage analysis: 4 seconds total
- Documentation build: 1 second

**NO LONG-RUNNING OPERATIONS** -- if anything takes >10 seconds, investigate

## Repository Navigation

### Key Files and Locations
- **Core devices**: `semiconductor_sim/devices/` (pn_junction.py, led.py, solar_cell.py, etc.)
- **Physical models**: `semiconductor_sim/models/` (recombination, bandgap, etc.) 
- **Configuration**: `pytest.ini`, `mypy.ini`, `pyproject.toml`, `requirements.txt`
- **CI/CD**: `.github/workflows/ci.yml` defines the quality gates
- **Examples**: `examples/example_*.py` scripts work, notebooks may need plotly/ipywidgets

### Common Development Tasks
- **Add new device**: Extend `semiconductor_sim/devices/base.py`, add to `__init__.py`
- **Add new model**: Create in `semiconductor_sim/models/`, import in `__init__.py`  
- **Update tests**: Add to `tests/test_*.py`, maintain >80% coverage
- **Check API changes**: Run device simulation validation script

## Validation Checklist
Before completing any change, ALWAYS:
- [ ] Import test: `python3 -c "import semiconductor_sim; from semiconductor_sim.devices import PNJunctionDiode; print('ok')"`
- [ ] Type check: `mypy semiconductor_sim` (49 errors expected)
- [ ] Test suite: `python3 -m pytest -q` (60 tests should pass)
- [ ] Coverage: `python3 -m coverage run -m pytest -q && python3 -m coverage report --fail-under=80` (>80% required)
- [ ] Device simulation: Run manual validation script testing actual device physics
- [ ] Example scripts: `python3 examples/example_pn_junction.py` (should complete without errors)

## Common File Contents (for Reference)

### Repository Root
```
README.md            # Installation and quickstart guide
CONTRIBUTING.md      # Development workflow details  
pyproject.toml       # Project configuration and dependencies
requirements.txt     # Runtime dependencies (numpy, matplotlib, scipy, plotly, ipywidgets, joblib)
requirements-dev.txt # Development dependencies
setup.py             # Setuptools entry point
pytest.ini           # Test configuration (filterwarnings for matplotlib)
mypy.ini             # Type checking configuration
mkdocs.yml           # Documentation configuration (uses material theme)
```

### Critical Package Dependencies
**Runtime (in requirements.txt):**
- numpy, matplotlib, scipy (core scientific computing)
- plotly, ipywidgets (interactive visualizations)  
- joblib (ML model loading for Zener diode)

**Development (in requirements-dev.txt):**
- ruff, mypy, pytest, coverage, hypothesis
- mkdocs-material, mkdocstrings, mkdocstrings-python
- pre-commit, pip-audit, build

## Known Issues and Workarounds
- **ZenerDiode ML model**: Missing `zener_voltage_rf_model.pkl` falls back to default value (expected)
- **Plotting warnings**: "FigureCanvasAgg is non-interactive" warnings in headless mode (safe to ignore)
- **Type annotations**: MyPy finds 49 ndarray type parameter issues (known technical debt)
- **Ruff unavailable**: Skip formatting/linting commands in this environment
- **Interactive examples**: Jupyter notebooks may fail without plotly/ipywidgets