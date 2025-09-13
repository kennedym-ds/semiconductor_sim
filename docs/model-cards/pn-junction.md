# PN Junction Diode Model Card

## Overview

The PN Junction Diode is a fundamental semiconductor device consisting of a p-type and n-type semiconductor junction. This model simulates the electrical characteristics including current-voltage (IV) behavior and Shockley-Read-Hall (SRH) recombination effects.

## Model Implementation

**Class:** `semiconductor_sim.devices.PNJunctionDiode`

## Inputs

| Parameter | Type | Units | Default | Description |
|-----------|------|-------|---------|-------------|
| `doping_p` | float | cm⁻³ | Required | Acceptor concentration in p-region |
| `doping_n` | float | cm⁻³ | Required | Donor concentration in n-region |
| `area` | float | cm² | 1e-4 | Cross-sectional area of the diode |
| `temperature` | float | K | 300 | Operating temperature |
| `tau_n` | float | s | 1e-6 | Electron lifetime |
| `tau_p` | float | s | 1e-6 | Hole lifetime |
| `D_n` | float | cm²/s | 25.0 | Electron diffusion coefficient |
| `D_p` | float | cm²/s | 10.0 | Hole diffusion coefficient |
| `L_n` | float | cm | 5e-4 | Electron diffusion length |
| `L_p` | float | cm | 5e-4 | Hole diffusion length |

### Method: `iv_characteristic(voltage_array, n_conc=None, p_conc=None)`

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `voltage_array` | np.ndarray | V | Array of voltage values |
| `n_conc` | float/np.ndarray | cm⁻³ | Optional electron concentration for SRH calculation |
| `p_conc` | float/np.ndarray | cm⁻³ | Optional hole concentration for SRH calculation |

## Outputs

| Output | Type | Units | Description |
|--------|------|-------|-------------|
| `current` | np.ndarray | A | Diode current array |
| `recombination` | np.ndarray | cm⁻³s⁻¹ | SRH recombination rate (when concentrations provided) |

## Model Assumptions

1. **Ideal Diode Equation**: Uses the Shockley diode equation: I = I_s(e^(V/V_T) - 1)
2. **Temperature Dependence**: Saturation current I_s scales with temperature via intrinsic carrier concentration
3. **SRH Recombination**: Includes Shockley-Read-Hall recombination with mid-gap trap assumption (n₁ ≈ p₁ ≈ nᵢ)
4. **Constant Transport Parameters**: Diffusion coefficients and lengths are temperature-independent
5. **No Series/Shunt Resistance**: Ideal diode with no parasitic resistances
6. **Uniform Doping**: Assumes uniform doping concentrations in each region

## Validity Range

- **Voltage**: Forward bias: 0 to ~1V; Reverse bias: down to ~-10V
- **Temperature**: 200K to 500K (limited by intrinsic carrier concentration model)
- **Doping**: 10¹⁴ to 10¹⁹ cm⁻³ (typical semiconductor doping range)
- **Current Density**: Up to ~10³ A/cm² (before high-injection effects)

## Physical Limitations

- Does not include generation-recombination current in depletion region
- No high-injection effects (assumes low-injection conditions)
- No avalanche breakdown modeling
- No tunneling current (significant in heavily doped junctions)
- No surface recombination effects

## Example Usage

```python
import numpy as np
from semiconductor_sim.devices import PNJunctionDiode

# Create PN junction diode
diode = PNJunctionDiode(
    doping_p=1e17,  # 10^17 cm^-3 acceptors
    doping_n=1e17,  # 10^17 cm^-3 donors
    temperature=300,
    area=1e-4  # 0.01 cm^2
)

# Calculate IV characteristic
voltages = np.linspace(-1, 0.8, 100)
current, recombination = diode.iv_characteristic(
    voltages, 
    n_conc=1e16, 
    p_conc=1e16
)

print(f"Saturation current: {diode.I_s:.2e} A")
```

## References

1. Sze, S. M., & Ng, K. K. (2006). *Physics of Semiconductor Devices*. John Wiley & Sons.
2. Streetman, B. G., & Banerjee, S. K. (2015). *Solid State Electronic Devices*. Pearson.
3. Neamen, D. A. (2012). *Semiconductor Physics and Devices*. McGraw-Hill.

## Related Models

- [LED Model Card](led.md) - Extends PN junction with emission modeling
- [Solar Cell Model Card](solar-cell.md) - PN junction under illumination
- [Theory: PN Junction Physics](../theory/pn-junction-theory.md)