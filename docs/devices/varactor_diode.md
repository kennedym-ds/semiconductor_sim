# Varactor Diode

- Overview: Voltage-dependent junction capacitance device with ideal-diode IV.

## Usage

```python
from semiconductor_sim import VaractorDiode

va = VaractorDiode(1e17, 1e17)
```

## Plots

```python
import numpy as np
v = np.linspace(0.0, 2.0, 200)  # reverse voltage magnitude
Cj = va.capacitance(v)
va.plot_capacitance_vs_voltage(v)
```

![Varactor: C–V](../images/varactor_cv.png)

### See also

- Gallery: [Varactor C–V](../gallery.md#other-devices)
