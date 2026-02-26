## MOSFET (NMOS)

A teaching-first long-channel NMOS analog model with two key outputs:

- Drain current (`I_D`) output characteristics over `V_DS`
- Transconductance (`g_m`) curves for each configured gate bias

The model uses square-law regions with optional channel-length modulation:

- Cutoff: `V_GS <= V_TH`
- Triode: `I_D = beta * (2 * V_OV * V_DS - V_DS^2) * (1 + lambda * V_DS)`
- Saturation: `I_D = beta * V_OV^2 * (1 + lambda * V_DS)`

where `V_OV = max(V_GS - V_TH, 0)`.

### Example

```python
import numpy as np
from semiconductor_sim.devices import MOSFET

mosfet = MOSFET(
    threshold_voltage=1.0,
    beta=1e-3,
    channel_length_modulation=0.02,
    vgs_values=[1.0, 1.5, 2.0, 2.5],
)
vds = np.linspace(0.0, 3.0, 200)
ids_grid, gm_grid = mosfet.iv_characteristic(vds)
mosfet.plot_output_characteristics(vds, ids_grid, gm_grid)
```
