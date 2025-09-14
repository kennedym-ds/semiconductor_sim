# LED

- Overview: Light-emitting diode with ideal-diode IV and simple emission model.
- Emission is proportional to radiative recombination times area (simplified).

## Usage

```python
from semiconductor_sim import LED
from semiconductor_sim.materials import get_material

gaas = get_material("GaAs")
led = LED(1e17, 1e17, efficiency=0.2, material=gaas)
```

## Materials

- `material` modifies intrinsic concentration and IV; also affects emission trends.

![LED: materials effect](../images/led_materials.png)

### See also

- Examples: [materials plotting](../examples.md#plotting-based-materials-comparison)
- Gallery: [LED materials](../gallery.md#materials-effects)
