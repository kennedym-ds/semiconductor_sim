# LED Model Card

## Overview

The Light-Emitting Diode (LED) model extends the basic PN junction diode to include optical emission characteristics. This model simulates both electrical IV behavior and light emission intensity based on radiative and non-radiative recombination processes.

## Model Implementation

**Class:** `semiconductor_sim.devices.LED`

## Inputs

| Parameter | Type | Units | Default | Description |
|-----------|------|-------|---------|-------------|
| `doping_p` | float | cm⁻³ | Required | Acceptor concentration in p-region |
| `doping_n` | float | cm⁻³ | Required | Donor concentration in n-region |
| `area` | float | cm² | 1e-4 | Cross-sectional area of the LED |
| `efficiency` | float | - | 0.1 | Radiative recombination efficiency (0-1) |
| `temperature` | float | K | 300 | Operating temperature |
| `B` | float | cm³/s | 1e-10 | Radiative recombination coefficient |
| `D_n` | float | cm²/s | 25.0 | Electron diffusion coefficient |
| `D_p` | float | cm²/s | 10.0 | Hole diffusion coefficient |
| `L_n` | float | cm | 5e-4 | Electron diffusion length |
| `L_p` | float | cm | 5e-4 | Hole diffusion length |

### Method: `iv_characteristic(voltage_array, n_conc=None, p_conc=None)`

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `voltage_array` | np.ndarray | V | Array of voltage values |
| `n_conc` | float/np.ndarray | cm⁻³ | Optional electron concentration |
| `p_conc` | float/np.ndarray | cm⁻³ | Optional hole concentration |

## Outputs

| Output | Type | Units | Description |
|--------|------|-------|-------------|
| `current` | np.ndarray | A | LED current array |
| `emission` | np.ndarray | arb. units | Optical emission intensity |
| `recombination` | np.ndarray | cm⁻³s⁻¹ | SRH recombination (when concentrations provided) |

## Model Assumptions

1. **Diode Base**: Inherits ideal diode behavior from PN junction model
2. **Radiative Recombination**: Emission proportional to radiative recombination rate
3. **Internal Quantum Efficiency**: Fraction of radiative recombination that produces photons
4. **Simplified Emission**: No spectral details or photon energy considerations
5. **Temperature Effects**: Emission efficiency assumed temperature-independent
6. **No Light Extraction**: Does not model optical losses or light extraction efficiency

## Validity Range

- **Voltage**: Forward bias: 0 to ~3V (typical LED operation range)
- **Temperature**: 200K to 400K (limited by efficiency model assumptions)
- **Efficiency**: 0.0 to 1.0 (physical constraint)
- **Current Density**: Up to ~10² A/cm² (before efficiency droop effects)

## Physical Limitations

- No efficiency droop at high current densities
- No spectral characteristics or wavelength modeling
- No temperature dependence of internal quantum efficiency
- No Auger recombination effects
- No current spreading or optical extraction modeling

## Example Usage

```python
import numpy as np
from semiconductor_sim.devices import LED

# Create LED device
led = LED(
    doping_p=5e17,      # Higher doping for LEDs
    doping_n=1e18,      # Heavy n-doping
    efficiency=0.2,     # 20% internal quantum efficiency
    temperature=300,
    area=1e-4
)

# Calculate IV and emission characteristics
voltages = np.linspace(0, 3, 100)
current, emission = led.iv_characteristic(voltages)

# With carrier concentrations for detailed analysis
current, emission, recombination = led.iv_characteristic(
    voltages,
    n_conc=1e17,
    p_conc=1e17
)

print(f"Saturation current: {led.I_s:.2e} A")
print(f"Efficiency: {led.efficiency}")
```

## Key Differences from PN Junction

- **Additional Output**: Emission intensity alongside electrical current
- **Efficiency Parameter**: Controls fraction of recombination that produces light
- **Extended Forward Bias**: Operates at higher forward voltages (1.5-3V)
- **Radiative Recombination**: Explicitly models radiative processes

## References

1. Schubert, E. F. (2006). *Light-Emitting Diodes*. Cambridge University Press.
2. Piprek, J. (2003). *Semiconductor Optoelectronic Devices*. Academic Press.
3. Sze, S. M., & Ng, K. K. (2006). *Physics of Semiconductor Devices*. John Wiley & Sons.

## Related Models

- [PN Junction Model Card](pn-junction.md) - Base diode model
- [Solar Cell Model Card](solar-cell.md) - Reverse process (light → electricity)
- [Theory: LED Physics](../theory/led-theory.md)