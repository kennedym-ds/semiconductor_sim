# Zener Diode Model Card

## Overview

The Zener Diode model simulates a PN junction designed to operate in reverse breakdown mode. It provides voltage regulation through the avalanche or Zener breakdown mechanism, maintaining a nearly constant voltage across a wide range of reverse currents.

## Model Implementation

**Class:** `semiconductor_sim.devices.ZenerDiode`

## Inputs

| Parameter | Type | Units | Default | Description |
|-----------|------|-------|---------|-------------|
| `doping_p` | float | cm⁻³ | Required | Acceptor concentration in p-region |
| `doping_n` | float | cm⁻³ | Required | Donor concentration in n-region |
| `area` | float | cm² | 1e-4 | Cross-sectional area of the diode |
| `zener_voltage` | float | V | 5.0 | Zener breakdown voltage |
| `temperature` | float | K | 300 | Operating temperature |
| `tau_n` | float | s | 1e-6 | Electron lifetime |
| `tau_p` | float | s | 1e-6 | Hole lifetime |

### Method: `iv_characteristic(voltage_array, n_conc=None, p_conc=None)`

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `voltage_array` | np.ndarray | V | Array of voltage values |
| `n_conc` | float/np.ndarray | cm⁻³ | Optional electron concentration |
| `p_conc` | float/np.ndarray | cm⁻³ | Optional hole concentration |

### Method: `predict_zener_voltage()`

Uses machine learning model to predict Zener voltage based on doping concentrations.

## Outputs

| Output | Type | Units | Description |
|--------|------|-------|-------------|
| `current` | np.ndarray | A | Zener diode current |
| `recombination` | np.ndarray | cm⁻³s⁻¹ | SRH recombination rate (when concentrations provided) |
| `predicted_voltage` | float | V | ML-predicted Zener voltage |

## Model Assumptions

1. **Ideal Forward Bias**: Standard diode equation for forward operation
2. **Sharp Breakdown**: Abrupt transition to breakdown region
3. **Constant Breakdown Voltage**: Zener voltage independent of current (in breakdown)
4. **Temperature Effects**: Limited temperature dependence modeling
5. **Uniform Breakdown**: Breakdown occurs uniformly across junction
6. **No Series Resistance**: Ideal characteristics without parasitic effects

## Validity Range

- **Forward Voltage**: 0V to +1V (normal diode operation)
- **Reverse Voltage**: 0V to -(Zener voltage + margin)
- **Zener Voltage**: 2V to 200V (typical Zener range)
- **Temperature**: 200K to 400K (limited by breakdown model)
- **Current**: mA to A range (limited by thermal effects not modeled)

## Physical Limitations

- No dynamic resistance modeling in breakdown
- No temperature coefficient of breakdown voltage
- No noise characteristics
- No avalanche multiplication modeling
- No thermal runaway protection

## Breakdown Mechanisms

### Zener Breakdown (< 5V)
- **Mechanism**: Band-to-band tunneling
- **Temperature Coefficient**: Negative (~-2mV/°C)
- **Characteristics**: Sharp, well-defined breakdown

### Avalanche Breakdown (> 7V)
- **Mechanism**: Impact ionization
- **Temperature Coefficient**: Positive (~+2mV/°C)
- **Characteristics**: Soft breakdown knee

### Mixed Region (5-7V)
- **Mechanism**: Combination of both effects
- **Temperature Coefficient**: Near zero

## Example Usage

```python
import numpy as np
from semiconductor_sim.devices import ZenerDiode

# Create 5.1V Zener diode
zener = ZenerDiode(
    doping_p=1e17,
    doping_n=1e17,
    zener_voltage=5.1,
    area=1e-4,
    temperature=300
)

# Calculate IV characteristic
voltages = np.linspace(-8, 1, 200)
current, recombination = zener.iv_characteristic(
    voltages,
    n_conc=1e16,
    p_conc=1e16
)

# Use ML prediction for Zener voltage
try:
    predicted_vz = zener.predict_zener_voltage()
    print(f"Predicted Zener voltage: {predicted_vz:.2f} V")
except:
    print("ML model not available, using default")

# Find breakdown characteristics
breakdown_region = voltages < -zener.zener_voltage
if np.any(breakdown_region):
    breakdown_current = current[breakdown_region]
    print(f"Breakdown current range: {breakdown_current.min():.3e} to {breakdown_current.max():.3e} A")
```

## Voltage Regulation Analysis

```python
# Regulation analysis
def analyze_regulation(zener, load_range):
    """Analyze voltage regulation over load current range."""
    # Simplified regulation analysis
    v_out = []
    for i_load in load_range:
        # Find operating point (simplified)
        v_reg = zener.zener_voltage  # Ideal regulation
        v_out.append(v_reg)
    
    regulation = (max(v_out) - min(v_out)) / min(v_out) * 100
    return regulation  # Percent regulation

# Example usage
load_currents = np.linspace(1e-3, 50e-3, 50)  # 1mA to 50mA
regulation_percent = analyze_regulation(zener, load_currents)
print(f"Line regulation: {regulation_percent:.2f}%")
```

## Applications

- **Voltage Regulation**: Constant voltage reference
- **Overvoltage Protection**: Clipping excessive voltages
- **Voltage Reference**: Precision voltage standards
- **Surge Protection**: Transient voltage suppression
- **Waveform Shaping**: Signal limiting circuits

## Design Considerations

### Zener Voltage Selection
- **Low Voltage** (2-5V): Zener breakdown dominant
- **Medium Voltage** (5-7V): Mixed breakdown mechanism
- **High Voltage** (>7V): Avalanche breakdown dominant

### Power Rating
```python
P_max = I_max * V_z  # Maximum power dissipation
```

### Dynamic Resistance
- **Forward**: Similar to regular diode
- **Breakdown**: Low resistance (good regulation)

## References

1. Zener, C. (1934). A theory of the electrical breakdown of solid dielectrics. *Proceedings of the Royal Society A*, 145(855), 523-529.
2. Sze, S. M., & Ng, K. K. (2006). *Physics of Semiconductor Devices*. John Wiley & Sons.
3. Millman, J., & Halkias, C. C. (1972). *Integrated Electronics*. McGraw-Hill.

## Related Models

- [PN Junction Model Card](pn-junction.md) - Base diode structure
- [Tunnel Diode Model Card](tunnel-diode.md) - Another quantum effect device