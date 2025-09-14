# Tunnel Diode

- Overview: Highly doped PN junction with negative differential resistance regions
  simplified to an exponential IV in this model.

## Usage

```python
from semiconductor_sim import TunnelDiode

td = TunnelDiode(1e19, 1e19)
```

## Plot

```python
import numpy as np
v = np.linspace(-0.3, 0.7, 200)
I, R = td.iv_characteristic(v)
td.plot_iv_characteristic(v, I, R)
```

![Tunnel: IV](../images/tunnel_iv.png)

### See also

- Gallery: [Tunnel IV](../gallery.md#other-devices)
