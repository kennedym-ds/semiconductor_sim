# Solar Cell Lab

## Objectives

- Explore illuminated I–V and short-circuit/open-circuit conditions.
- Observe how illumination shifts the I–V curve.

## Tasks

1. Instantiate `SolarCell` at 300 K with typical parameters.
2. Sweep `V` −0.2–0.8 V under a given `illumination` value.
3. Identify `I_sc` and `V_oc`; compute fill factor approximation.

## Hints

- Use `solar.iv_characteristic(V, illumination=...)`.
- Plot linear axes; annotate the axes intercepts.

## Solution (Reference)

```python
import numpy as np
from semiconductor_sim.devices import SolarCell

V = np.linspace(-0.2, 0.8, 101)
solar = SolarCell(temperature=300)
I, *_ = solar.iv_characteristic(V)
```

## How to Run

- Use `examples/example_solar_cell.py` for a quick scripted run.
- Notebook workflows are recommended for parameter sweeps.
