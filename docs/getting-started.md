# Getting Started

## Installation

```bash
pip install semiconductor-sim
```

From source:

```bash
git clone https://github.com/kennedym-ds/semiconductor_sim.git
cd semiconductor_sim
python -m venv .venv
. .venv/Scripts/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .
```

## First simulation

```python
import numpy as np
from semiconductor_sim.devices import PNJunctionDiode

d = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
V = np.array([0.0, 0.2, 0.4])
I, R = d.iv_characteristic(V, n_conc=1e16, p_conc=1e16)
print(I)
```

## Materials (optional)

Some devices accept a `material` to incorporate temperature-dependent material
properties such as intrinsic carrier concentration and bandgap.

```python
from semiconductor_sim.materials import get_material
from semiconductor_sim.devices import LED, SolarCell

si = get_material("Si")
led = LED(1e17, 1e17, efficiency=0.2, material=si)
sc = SolarCell(1e17, 1e17, light_intensity=1.0, material=si)
```
