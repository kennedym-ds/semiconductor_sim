# MOS Capacitor

- Overview: Simple MOS C–V model with oxide capacitance and depletion behavior.

## Usage

```python
from semiconductor_sim import MOSCapacitor

mos = MOSCapacitor(doping_p=1e17, oxide_thickness=1e-6)
```

## Plots

```python
import numpy as np
v = np.linspace(-2, 2, 200)
mos.plot_capacitance_vs_voltage(v)
```

![MOS: C–V](../images/mos_cv.png)

### See also

- Gallery: [MOS C–V](../gallery.md#other-devices)
