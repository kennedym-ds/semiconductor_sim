# MOS Capacitor Model Card

## Overview

The MOS (Metal-Oxide-Semiconductor) Capacitor model simulates the fundamental building block of MOSFET devices. It consists of a metal gate, oxide insulator, and semiconductor substrate, exhibiting voltage-dependent capacitance behavior crucial for understanding MOSFET operation.

## Model Implementation

**Class:** `semiconductor_sim.devices.MOSCapacitor`

## Inputs

| Parameter | Type | Units | Default | Description |
|-----------|------|-------|---------|-------------|
| `doping_p` | float | cm⁻³ | Required | Acceptor concentration in p-type substrate |
| `oxide_thickness` | float | cm | 1e-6 | Gate oxide thickness |
| `oxide_permittivity` | float | - | 3.45 | Relative permittivity of gate oxide |
| `area` | float | cm² | 1e-4 | Gate area |
| `temperature` | float | K | 300 | Operating temperature |
| `tau_n` | float | s | 1e-6 | Electron lifetime |
| `tau_p` | float | s | 1e-6 | Hole lifetime |

### Methods

#### `capacitance(applied_voltage)`
| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `applied_voltage` | np.ndarray | V | Gate voltage array |

#### `depletion_width(applied_voltage)`
| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `applied_voltage` | np.ndarray | V | Gate voltage array |

#### `iv_characteristic(voltage_array, n_conc=None, p_conc=None)`
| Parameter | Type | Units | Description |
|-----------|------|-------|-------------|
| `voltage_array` | np.ndarray | V | Array of voltage values |
| `n_conc` | float/np.ndarray | cm⁻³ | Optional electron concentration |
| `p_conc` | float/np.ndarray | cm⁻³ | Optional hole concentration |

## Outputs

| Output | Type | Units | Description |
|--------|------|-------|-------------|
| `capacitance` | np.ndarray | F | Gate capacitance vs voltage |
| `depletion_width` | np.ndarray | cm | Depletion region width |
| `current` | np.ndarray | A | Gate leakage current |
| `C_ox` | float | F | Oxide capacitance (constant) |

## Model Assumptions

1. **Ideal MOS Structure**: No interface states or charges
2. **Uniform Doping**: Constant acceptor concentration in substrate
3. **Abrupt Interfaces**: Sharp metal-oxide and oxide-semiconductor boundaries
4. **Quasi-Static Operation**: Slow voltage variations (no AC effects)
5. **Thick Oxide**: No quantum mechanical effects or tunneling
6. **Temperature Independence**: Oxide properties assumed constant

## Validity Range

- **Gate Voltage**: -5V to +5V (typical MOS operation range)
- **Oxide Thickness**: >10nm (thick oxide, no tunneling)
- **Doping**: 10¹⁴ to 10¹⁸ cm⁻³ (typical substrate doping)
- **Temperature**: 200K to 400K (limited by mobility models)
- **Frequency**: DC to ~MHz (quasi-static approximation)

## Physical Limitations

- No interface trap states (Dit)
- No oxide charge or work function differences
- No quantum mechanical effects
- No gate leakage current for thin oxides
- No polysilicon gate depletion effects
- No high-frequency dispersion

## Operating Regimes

### 1. Accumulation (V_G < 0 for p-substrate)
- **Surface**: Hole accumulation
- **Capacitance**: C ≈ C_ox (maximum)
- **Depletion Width**: Minimal

### 2. Depletion (0 < V_G < V_T)
- **Surface**: Depletion of holes
- **Capacitance**: Series combination of C_ox and C_dep
- **Depletion Width**: Increases with voltage

### 3. Inversion (V_G > V_T)
- **Surface**: Electron inversion layer
- **Capacitance**: Returns toward C_ox
- **Depletion Width**: Maximum (approximately constant)

## Key Relationships

### Oxide Capacitance
```
C_ox = ε_ox × A / t_ox
```

### Depletion Capacitance
```
C_dep = ε_s × A / W_dep
```

### Total Capacitance (Depletion)
```
1/C_total = 1/C_ox + 1/C_dep
```

## Example Usage

```python
import numpy as np
from semiconductor_sim.devices import MOSCapacitor

# Create MOS capacitor
mos_cap = MOSCapacitor(
    doping_p=1e16,          # Lightly doped p-substrate
    oxide_thickness=100e-7, # 100nm oxide (thick)
    oxide_permittivity=3.9, # SiO2
    area=1e-4,              # 0.01 cm²
    temperature=300
)

# Calculate C-V characteristic
gate_voltages = np.linspace(-3, 3, 100)
capacitance = mos_cap.capacitance(gate_voltages)
depletion_width = mos_cap.depletion_width(gate_voltages)

# Key parameters
print(f"Oxide capacitance: {mos_cap.C_ox:.2e} F")
print(f"Max depletion width: {depletion_width.max():.2e} cm")

# Normalized C-V curve
C_norm = capacitance / mos_cap.C_ox
print(f"Min normalized capacitance: {C_norm.min():.3f}")
```

## Threshold Voltage Extraction

```python
def extract_threshold_voltage(gate_voltage, capacitance, C_ox):
    """Extract threshold voltage from C-V curve."""
    # Find point of maximum dC/dV (simplified method)
    dC_dV = np.gradient(capacitance, gate_voltage)
    max_slope_idx = np.argmax(np.abs(dC_dV))
    V_T = gate_voltage[max_slope_idx]
    return V_T

V_T = extract_threshold_voltage(gate_voltages, capacitance, mos_cap.C_ox)
print(f"Extracted threshold voltage: {V_T:.2f} V")
```

## Flatband Voltage

```python
def calculate_flatband_voltage(work_function_diff=0, oxide_charge=0, C_ox=None):
    """Calculate flatband voltage (simplified)."""
    V_FB = work_function_diff - oxide_charge / C_ox
    return V_FB
```

## Applications

- **MOSFET Characterization**: Understanding gate capacitance behavior
- **Process Monitoring**: Oxide quality and interface characterization
- **Device Modeling**: Parameter extraction for SPICE models
- **Sensor Applications**: Capacitive sensing devices
- **Memory Devices**: Charge storage mechanisms

## Device Physics Insights

### Surface Potential
- **Controls**: Carrier distribution at surface
- **Relationship**: V_G = V_surface + V_oxide

### Electric Field
- **Oxide Field**: V_G / t_ox
- **Surface Field**: Controls inversion layer formation

### Charge Relationships
- **Gate Charge**: Q_G = C_ox × V_G (in accumulation)
- **Depletion Charge**: Q_dep = q × N_A × W_dep × A

## References

1. Sze, S. M., & Ng, K. K. (2006). *Physics of Semiconductor Devices*. John Wiley & Sons.
2. Nicollian, E. H., & Brews, J. R. (1982). *MOS Physics and Technology*. Wiley.
3. Taur, Y., & Ning, T. H. (2009). *Fundamentals of Modern VLSI Devices*. Cambridge University Press.

## Related Models

- [Varactor Diode Model Card](varactor-diode.md) - Alternative voltage-controlled capacitor
- [PN Junction Model Card](pn-junction.md) - Related semiconductor junction