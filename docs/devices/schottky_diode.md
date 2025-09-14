# Schottky Diode

A metal–semiconductor junction modeled with thermionic emission.

## Model

Using a teaching-simple thermionic emission equation:

$$
I = A\,A^*\,T^2\,e^{-\frac{q\Phi_B}{k_B T}}\left(e^{\frac{qV}{n k_B T}} - 1\right)
$$

- $\Phi_B$: barrier height (eV)
- $n$: ideality factor
- $A^*$: effective Richardson constant (A/cm²/K²)

Assumptions: no image-force lowering, no series resistance, uniform temperature.

## Usage

```python
from semiconductor_sim import SchottkyDiode
import numpy as np

d = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1)
V = np.linspace(-0.2, 0.5, 200)
I, = d.iv_characteristic(V)
```

See the Gallery for an IV example.

## Series Resistance (optional)

You can include a simple series resistance `R_s` to account for contact
and bulk resistances. The current then satisfies

$$
I = I_s\left(\exp\left(\frac{q\,(V - I\,R_s)}{n\,k_B T}\right) - 1\right),
$$

which we solve numerically with a stable Newton method for each voltage
point. Enable it by passing `series_resistance_ohm`:

```python
from semiconductor_sim import SchottkyDiode
import numpy as np

d = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1, series_resistance_ohm=5.0)
V = np.linspace(-0.2, 0.5, 200)
I, = d.iv_characteristic(V)
```

Note: This is a teaching-simple addition; effects like image-force barrier
lowering or bias-dependent ideality are not modeled.
