# Solar Cell

- Overview: Illuminated diode model with short-circuit current and open-circuit voltage.
- Uses ideal diode dark current with optional materials support.

## Usage

```python
from semiconductor_sim import SolarCell
from semiconductor_sim.materials import get_material

si = get_material("Si")
sc = SolarCell(1e17, 1e17, light_intensity=1.0, material=si)
```

## Materials

- `material` modifies `n_i(T)` driving the dark saturation current,
  impacting `V_oc` and IV.

![Solar: materials effect](../images/solar_materials.png)

### See also

- Examples: [materials plotting](../examples.md#plotting-based-materials-comparison)
- Gallery: [Solar materials](../gallery.md#materials-effects)
