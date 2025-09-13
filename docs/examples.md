# Examples

Scripts: browse the `examples/` folder for CLI-friendly runs.
Notebooks: interactive versions use ipywidgets and Plotly for exploration.

Quick LED sample:

```python
import numpy as np
from semiconductor_sim.devices import LED

led = LED(doping_p=1e17, doping_n=1e17, temperature=300)
V = np.linspace(0, 2, 5)
current, emission = led.iv_characteristic(V)
```
