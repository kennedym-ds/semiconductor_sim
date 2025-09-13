# Tunnel Diode Model Card

## Overview

The Tunnel Diode model simulates a heavily doped PN junction where quantum mechanical tunneling effects dominate the current transport. This device exhibits negative differential resistance in the forward bias region, making it useful for oscillator and amplifier applications.

## Model Implementation

**Class:** `semiconductor_sim.devices.TunnelDiode`

## Inputs

| Parameter | Type | Units | Default | Description |
|-----------|------|-------|---------|-------------|
| `doping_p` | float | cm⁻³ | Required | Acceptor concentration in p-region (typically >10¹⁹) |
| `doping_n` | float | cm⁻³ | Required | Donor concentration in n-region (typically >10¹⁹) |
| `area` | float | cm² | 1e-4 | Cross-sectional area of the diode |
| `temperature` | float | K | 300 | Operating temperature |
| `tau_n` | float | s | 1e-6 | Electron lifetime |
| `tau_p` | float | s | 1e-6 | Hole lifetime |

### Method: `iv_characteristic(voltage_array, n_conc=None, p_conc=None)`

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `voltage_array` | np.ndarray | V | Array of voltage values |
| `n_conc` | float/np.ndarray | cm⁻³ | Optional electron concentration |
| `p_conc` | float/np.ndarray | cm⁻³ | Optional hole concentration |

## Outputs

| Output | Type | Units | Description |
|--------|------|-------|-------------|
| `current` | np.ndarray | A | Total diode current (tunneling + diffusion) |
| `recombination` | np.ndarray | cm⁻³s⁻¹ | SRH recombination rate (when concentrations provided) |

## Model Assumptions

1. **Heavy Doping**: Doping concentrations >10¹⁹ cm⁻³ for tunneling behavior
2. **Degenerate Semiconductors**: Fermi levels within the bands
3. **Simplified Tunneling**: Phenomenological tunneling current model
4. **Narrow Depletion Region**: Very thin tunneling barrier due to heavy doping
5. **Temperature Effects**: Limited temperature dependence of tunneling
6. **No Band-to-Band Effects**: Simplified energy band considerations

## Validity Range

- **Voltage**: -2V to +1V (typical tunnel diode operation)
- **Doping**: >10¹⁹ cm⁻³ (required for significant tunneling)
- **Temperature**: 77K to 400K (tunneling less temperature-sensitive)
- **Current Density**: Up to ~10⁴ A/cm² (high current capability)

## Physical Limitations

- Simplified tunneling model (no detailed band structure)
- No phonon-assisted tunneling
- No impact ionization effects
- No trap-assisted tunneling
- Temperature dependence approximated

## Characteristic Regions

### 1. Tunneling Region (0 < V < V_peak)
- Current increases due to increasing tunneling probability
- Quantum mechanical effect dominates

### 2. Negative Resistance Region (V_peak < V < V_valley)
- Current decreases with increasing voltage
- Unique property enabling oscillator applications

### 3. Diffusion Region (V > V_valley)
- Normal diode behavior dominates
- Exponential current increase

## Example Usage

```python
import numpy as np
from semiconductor_sim.devices import TunnelDiode

# Create tunnel diode with heavy doping
tunnel_diode = TunnelDiode(
    doping_p=5e19,  # Very heavy p-doping
    doping_n=5e19,  # Very heavy n-doping
    area=1e-4,
    temperature=300
)

# Calculate IV characteristic
voltages = np.linspace(-1, 1, 200)
current, recombination = tunnel_diode.iv_characteristic(
    voltages,
    n_conc=1e18,
    p_conc=1e18
)

# Find peak and valley points
peak_idx = np.argmax(current[voltages > 0])
valley_idx = np.argmin(current[voltages > voltages[peak_idx]])

print(f"Peak current: {current[peak_idx]:.2e} A")
print(f"Valley current: {current[valley_idx]:.2e} A")
print(f"Peak-to-valley ratio: {current[peak_idx]/current[valley_idx]:.1f}")
```

## Key Parameters

### Peak Current (I_peak)
- Maximum current in the tunneling region
- Proportional to tunneling probability

### Valley Current (I_valley)
- Minimum current in the negative resistance region
- Determines the peak-to-valley current ratio

### Negative Resistance
- dI/dV < 0 in the valley region
- Enables oscillation and amplification

## Applications

- **Oscillators**: Negative resistance enables oscillation
- **Amplifiers**: High-frequency, low-noise amplification
- **Switches**: Fast switching due to quantum effects
- **Memory**: Bistable characteristics for storage

## References

1. Chang, L. L., Esaki, L., & Tsu, R. (1974). Resonant tunneling in semiconductor double barriers. *Applied Physics Letters*, 24(12), 593-595.
2. Sze, S. M., & Ng, K. K. (2006). *Physics of Semiconductor Devices*. John Wiley & Sons.
3. Burghartz, J. N. (Ed.). (2007). *Guide to State-of-the-Art Electron Devices*. Wiley.

## Related Models

- [PN Junction Model Card](pn-junction.md) - Base diode structure
- [Zener Diode Model Card](zener-diode.md) - Another breakdown mechanism
- [Theory: Tunneling Physics](../theory/tunnel-diode-theory.md)