# Zener Diode

- Overview: Reverse breakdown diode with simplified breakdown behavior and optional
  SRH recombination.

## Usage

```python
from semiconductor_sim import ZenerDiode

ze = ZenerDiode(1e17, 1e17, zener_voltage=5.0)
```

## Plot

```python
import numpy as np
v = np.linspace(0.0, 10.0, 200)
I, R = ze.iv_characteristic(v)
ze.plot_iv_characteristic(v, I, R)
```

![Zener: IV](../images/zener_iv.png)

### See also

- Gallery: [Zener IV](../gallery.md#other-devices)
