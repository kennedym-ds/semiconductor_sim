# Solar Cell Model Card

## Overview

The Solar Cell model simulates a photovoltaic device that converts light into electrical energy. Based on the PN junction diode under illumination, it models the photocurrent generation and IV characteristics under various lighting conditions.

## Model Implementation

**Class:** `semiconductor_sim.devices.SolarCell`

## Inputs

| Parameter | Type | Units | Default | Description |
|-----------|------|-------|---------|-------------|
| `doping_p` | float | cm⁻³ | Required | Acceptor concentration in p-region |
| `doping_n` | float | cm⁻³ | Required | Donor concentration in n-region |
| `area` | float | cm² | 1e-4 | Cross-sectional area of the solar cell |
| `light_intensity` | float | arb. units | 1.0 | Incident light intensity |
| `temperature` | float | K | 300 | Operating temperature |

### Method: `iv_characteristic(voltage_array)`

| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `voltage_array` | np.ndarray | V | Array of voltage values |

## Outputs

| Output | Type | Units | Description |
|--------|------|-------|-------------|
| `current` | np.ndarray | A | Solar cell current (negative for power generation) |
| `I_sc` | float | A | Short-circuit current |
| `V_oc` | float | V | Open-circuit voltage |

## Model Assumptions

1. **Illuminated Diode**: I = I_s(e^(V/V_T) - 1) - I_ph
2. **Linear Photocurrent**: I_ph proportional to light intensity
3. **Constant Absorption**: Light absorption independent of wavelength
4. **No Series/Shunt Resistance**: Ideal solar cell characteristics
5. **Uniform Illumination**: Light uniformly distributed across device area
6. **No Temperature Dependence**: Photocurrent assumed temperature-independent

## Validity Range

- **Voltage**: -0.5V to +0.8V (typical solar cell operation range)
- **Light Intensity**: 0 to 10 arbitrary units (proportional scaling)
- **Temperature**: 250K to 400K (typical solar cell operating range)
- **Current Density**: Up to ~10¹ A/cm² (limited by series resistance effects)

## Physical Limitations

- No spectral response modeling
- No temperature dependence of photocurrent
- No series or shunt resistance effects
- No reflection or optical losses
- No recombination in depletion region
- No hot-carrier effects or thermalization losses

## Key Parameters

### Short-Circuit Current (I_sc)
- Current when V = 0 (maximum photocurrent)
- Proportional to light intensity and device area
- Determined by photon absorption and carrier collection

### Open-Circuit Voltage (V_oc)
- Voltage when I = 0 (maximum voltage)
- Logarithmically dependent on light intensity
- Limited by dark saturation current

## Example Usage

```python
import numpy as np
from semiconductor_sim.devices import SolarCell

# Create solar cell
solar_cell = SolarCell(
    doping_p=1e17,
    doping_n=1e17,
    area=1.0,  # 1 cm² cell
    light_intensity=1.0,  # Standard test conditions
    temperature=300
)

# Calculate IV characteristic
voltages = np.linspace(-0.1, 0.7, 100)
current = solar_cell.iv_characteristic(voltages)

# Key parameters
print(f"Short-circuit current: {solar_cell.I_sc:.3f} A")
print(f"Open-circuit voltage: {solar_cell.V_oc:.3f} V")

# Power calculation
power = current * voltages
max_power_idx = np.argmax(power)
print(f"Maximum power: {power[max_power_idx]:.3f} W")
```

## Performance Metrics

### Fill Factor (FF)
```python
P_max = np.max(current * voltages)
FF = P_max / (solar_cell.I_sc * solar_cell.V_oc)
```

### Efficiency (η)
```python
P_in = light_intensity * area  # Input power (simplified)
efficiency = P_max / P_in
```

## References

1. Green, M. A. (1982). *Solar Cells: Operating Principles, Technology and System Applications*. Prentice-Hall.
2. Würfel, P., & Würfel, U. (2016). *Physics of Solar Cells: From Basic Principles to Advanced Concepts*. Wiley-VCH.
3. Nelson, J. (2003). *The Physics of Solar Cells*. Imperial College Press.

## Related Models

- [PN Junction Model Card](pn-junction.md) - Base diode model
- [LED Model Card](led.md) - Inverse process (electricity → light)