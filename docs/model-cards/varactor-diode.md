# Varactor Diode Model Card

## Overview

The Varactor Diode (Variable Capacitor Diode) is a PN junction optimized for voltage-controlled capacitance applications. Under reverse bias, the junction capacitance varies with applied voltage, making it useful for frequency tuning and modulation circuits.

## Model Implementation

**Class:** `semiconductor_sim.devices.VaractorDiode`

## Inputs

| Parameter | Type | Units | Default | Description |
|-----------|------|-------|---------|-------------|
| `doping_p` | float | cm⁻³ | Required | Acceptor concentration in p-region |
| `doping_n` | float | cm⁻³ | Required | Donor concentration in n-region |
| `area` | float | cm² | 1e-4 | Cross-sectional area of the diode |
| `temperature` | float | K | 300 | Operating temperature |
| `tau_n` | float | s | 1e-6 | Electron lifetime |
| `tau_p` | float | s | 1e-6 | Hole lifetime |

### Methods

#### `capacitance(reverse_voltage)`
| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `reverse_voltage` | float/np.ndarray | V | Reverse bias voltage (negative values) |

#### `iv_characteristic(voltage_array, n_conc=None, p_conc=None)`
| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `voltage_array` | np.ndarray | V | Array of voltage values |
| `n_conc` | float/np.ndarray | cm⁻³ | Optional electron concentration |
| `p_conc` | float/np.ndarray | cm⁻³ | Optional hole concentration |

## Outputs

| Output | Type | Units | Description |
|--------|------|-------|-------------|
| `capacitance` | float/np.ndarray | F | Junction capacitance |
| `current` | np.ndarray | A | Diode current |
| `recombination` | np.ndarray | cm⁻³s⁻¹ | SRH recombination rate (when concentrations provided) |

## Model Assumptions

1. **Abrupt Junction**: Step junction profile for capacitance calculation
2. **Depletion Approximation**: Complete ionization in depletion region
3. **One-Sided Junction**: Typically N⁺P or P⁺N structure
4. **Linear Capacitance-Voltage**: C ∝ (V + V_bi)^(-1/2) relationship
5. **No Series Resistance**: Ideal capacitance without parasitic effects
6. **Temperature Independence**: Capacitance assumed temperature-independent

## Validity Range

- **Reverse Voltage**: 0V to -20V (typical varactor operation)
- **Forward Voltage**: Limited to <0.5V (avoid significant conduction)
- **Frequency**: DC to ~GHz (limited by parasitic effects not modeled)
- **Capacitance Ratio**: Typically 2:1 to 10:1 (C_max/C_min)

## Physical Limitations

- No parasitic series resistance or inductance
- No breakdown voltage modeling
- No frequency-dependent effects
- No temperature dependence of capacitance
- No manufacturing tolerances or variations

## Key Relationships

### Junction Capacitance
```
C = C₀ / √(1 + |V_R|/V_bi)
```

Where:
- C₀ = zero-bias capacitance
- V_R = reverse voltage
- V_bi = built-in voltage

### Capacitance Variation Ratio
```
γ = C_max / C_min = √(V_max + V_bi) / √(V_min + V_bi)
```

## Example Usage

```python
import numpy as np
from semiconductor_sim.devices import VaractorDiode

# Create varactor diode
varactor = VaractorDiode(
    doping_p=1e16,  # Moderate p-doping
    doping_n=1e18,  # Heavy n-doping (N+P structure)
    area=1e-4,
    temperature=300
)

# Calculate capacitance vs reverse voltage
reverse_voltages = np.linspace(0, -10, 50)
capacitance = varactor.capacitance(reverse_voltages)

# Calculate IV characteristic
voltages = np.linspace(-10, 0.5, 100)
current, recombination = varactor.iv_characteristic(
    voltages,
    n_conc=1e15,
    p_conc=1e15
)

# Capacitance variation ratio
C_max = capacitance[0]  # At 0V
C_min = capacitance[-1]  # At maximum reverse bias
ratio = C_max / C_min
print(f"Capacitance ratio: {ratio:.1f}:1")
print(f"Zero-bias capacitance: {C_max:.2e} F")
```

## Design Considerations

### Doping Profile
- **Abrupt Junction**: Higher capacitance ratio
- **Graded Junction**: More linear C-V characteristic
- **Hyperabrupt**: Enhanced capacitance variation

### Operating Point
- **Reverse Bias**: Normal operation region
- **Zero Bias**: Maximum capacitance
- **High Reverse Bias**: Minimum capacitance

## Applications

- **Voltage-Controlled Oscillators (VCOs)**: Frequency tuning
- **Phase-Locked Loops (PLLs)**: Frequency control
- **FM Modulators**: Frequency modulation
- **Parametric Amplifiers**: Signal amplification
- **Tunable Filters**: Frequency-selective circuits

## Quality Factor (Q)

```python
# Quality factor calculation (simplified)
Q = 1 / (2 * π * f * R_s * C)
```

Where R_s is the series resistance (not modeled in this implementation).

## References

1. Penfield, P., & Rafuse, R. P. (1962). *Varactor Applications*. MIT Press.
2. Sze, S. M., & Ng, K. K. (2006). *Physics of Semiconductor Devices*. John Wiley & Sons.
3. Howes, M. J., & Morgan, D. V. (Eds.). (1976). *Variable Capacitance Diodes*. Wiley.

## Related Models

- [PN Junction Model Card](pn-junction.md) - Base diode structure
- [MOS Capacitor Model Card](mos-capacitor.md) - Alternative voltage-controlled capacitor