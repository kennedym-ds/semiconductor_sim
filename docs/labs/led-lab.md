# LED Device Lab

## Objectives

- Explore LED IV and emission trends vs. bias.
- Observe recombination rates and link to emission behavior.

## Tasks

1. Instantiate `LED` at 300 K with reasonable dopings.
2. Sweep `V` 0–2 V; compute `current, emission`.
3. Plot current and emission vs. voltage on dual axes.

## Hints

- Use `led.iv_characteristic(V)`; pass `n_conc`, `p_conc` to inspect SRH.
- Plot with Matplotlib or Plotly; keep CI headless in mind.

## Solution (Reference)

```python
import numpy as np
from semiconductor_sim.devices import LED

V = np.linspace(0, 2.0, 41)
led = LED(doping_p=1e17, doping_n=1e17, temperature=300)
I, Em = led.iv_characteristic(V)
```

## How to Run

- Try `examples/example_led.py` for a script-based run.
- Use a notebook for interactive tweaking (Phase 3 adds widgets).
