# Parasitics and Temperature Models

This document describes the parasitic and temperature modeling enhancements added to the semiconductor device models.

## Parasitic Effects

All device models now support optional parasitic elements that can be enabled to provide more realistic behavior:

### Series Resistance (R_s)
- Models resistance in series with the ideal device
- Causes voltage drop: `V_diode = V_terminal - I_terminal * R_s`
- Reduces current at higher voltages due to resistive loss
- Default: `R_s = 0.0 Ω` (no effect)

### Shunt Resistance (R_sh)
- Models parallel leakage path across the device
- Adds leakage current: `I_leakage = V_terminal / R_sh`
- Increases current magnitude due to parallel conduction
- Default: `R_sh = ∞ Ω` (no effect)

### Usage

```python
from semiconductor_sim.devices import PNJunctionDiode
import numpy as np

# Create device with parasitics
diode = PNJunctionDiode(
    doping_p=1e17,
    doping_n=1e17,
    R_s=1.0,           # 1 Ω series resistance
    R_sh=1e6,          # 1 MΩ shunt resistance
    enable_parasitics=True  # Enable parasitic effects
)

# Calculate IV with parasitics
voltage = np.linspace(0, 0.7, 100)
current, _ = diode.iv_characteristic(voltage)

# Compare ideal vs parasitic behavior
diode.plot_iv_comparison(voltage, show_parasitics=True)
```

### Parasitic Model Implementation

The parasitic effects are solved using Newton-Raphson iteration for the terminal equation:
```
I_terminal = I_ideal(V_terminal - I_terminal*R_s) + V_terminal/R_sh
```

The solver handles the nonlinear coupling between series resistance voltage drop and device current.

## Temperature Dependencies

### Improved Intrinsic Carrier Concentration

The models now use temperature-dependent bandgap via the Varshni equation:
```
Eg(T) = Eg(0) - αT²/(T + β)
```

This affects the intrinsic carrier concentration:
```
n_i(T) ∝ T^1.5 * exp(-Eg(T)/(2*k_B*T))
```

### Temperature-Dependent Mobility

Diffusion coefficients scale with temperature to account for lattice scattering:
```
D(T) = D_ref * (T/T_ref)^(γ+1)
```
where γ ≈ -1.5 for lattice scattering dominated transport.

### Usage

```python
# Compare temperature effects
diode_300K = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
diode_350K = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=350)

print(f"I_s at 300K: {diode_300K.I_s:.2e} A")
print(f"I_s at 350K: {diode_350K.I_s:.2e} A")
```

## Supported Devices

The following devices support both parasitic effects and improved temperature modeling:

- **PNJunctionDiode**: Basic PN junction with optional parasitics
- **LED**: Light-emitting diode with emission modeling
- **ZenerDiode**: Breakdown diode with ML-predicted Zener voltage
- **VaractorDiode**: Variable capacitance diode
- **TunnelDiode**: High-doping tunnel junction
- **SolarCell**: Photovoltaic cell under illumination

## API Compatibility

All enhancements maintain full backward compatibility:
- New parameters are optional with sensible defaults
- Existing code continues to work without modification
- Parasitic effects are disabled by default (`enable_parasitics=False`)

## Testing

Comprehensive tests verify parasitic limit behavior:
- `R_s → 0` recovers ideal behavior
- `R_sh → ∞` recovers ideal behavior
- Series resistance reduces current
- Shunt resistance increases current magnitude
- Temperature dependencies follow expected physics

## References

1. Varshni, Y.P. "Temperature dependence of the energy gap in semiconductors." Physica 34.1 (1967): 149-154.
2. Sze, S.M. and Ng, K.K. "Physics of semiconductor devices." John Wiley & Sons (2006).