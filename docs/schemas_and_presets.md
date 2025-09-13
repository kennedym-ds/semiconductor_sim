# Parameter Schemas and Material Presets

SemiconductorSim now includes powerful parameter validation and material preset functionality, making device creation safer and more convenient.

## Overview

The new features include:

- **Parameter Validation**: Optional pydantic-based schemas that validate device parameters with clear error messages
- **Material Presets**: Pre-configured material properties for common semiconductors (Si, GaAs, Ge, GaN, InP)
- **Easy Device Creation**: `from_preset()` class methods for creating devices with material-specific properties
- **Temperature Dependencies**: Built-in temperature-dependent calculations for material properties

## Installation

The schemas functionality requires pydantic as an optional dependency:

```bash
# Install with parameter validation support
pip install semiconductor-sim[schemas]

# Basic installation (material presets still work, but no validation)
pip install semiconductor-sim
```

## Material Presets

### Available Materials

The library includes comprehensive property databases for:

- **Silicon (Si)**: The most common semiconductor
- **Gallium Arsenide (GaAs)**: High-speed and optoelectronic applications
- **Germanium (Ge)**: Historical importance and specialized applications
- **Gallium Nitride (GaN)**: Wide bandgap for power and blue LEDs
- **Indium Phosphide (InP)**: High-frequency and telecommunications

### Material Properties

Each material includes:

- Bandgap energy (eV)
- Intrinsic carrier concentration at 300K (cm⁻³)
- Relative permittivity
- Electron and hole mobilities (cm²/V/s)
- Diffusion coefficients (cm²/s)
- Carrier lifetimes (s)
- Diffusion lengths (cm)
- Radiative recombination coefficient (cm³/s)

### Usage Examples

#### Basic Material Information

```python
from semiconductor_sim.schemas.material_presets import (
    get_material_properties, 
    list_available_materials
)

# List available materials
materials = list_available_materials()
print("Available:", materials)  # ['SI', 'GAAS', 'GE', 'GAN', 'INP']

# Get silicon properties
si_props = get_material_properties("Si")
print(f"Silicon bandgap: {si_props.bandgap} eV")
print(f"Silicon ni(300K): {si_props.ni_300k:.2e} cm⁻³")

# Temperature dependence
print(f"Silicon ni(350K): {si_props.ni(350):.2e} cm⁻³")
```

#### Creating Devices with Material Presets

```python
from semiconductor_sim import PNJunctionDiode, LED, SolarCell

# Create a silicon PN junction with material-specific properties
si_diode = PNJunctionDiode.from_preset(
    material="Si",
    doping_p=1e16,      # cm⁻³
    doping_n=1e17,      # cm⁻³
    area=1e-4           # cm²
)

# Create a GaAs LED with high efficiency
gaas_led = LED.from_preset(
    material="GaAs",
    doping_p=1e17,
    doping_n=1e18,
    efficiency=0.8
)

# Create a solar cell with custom light intensity
solar_cell = SolarCell.from_preset(
    material="Si",
    doping_p=1e16,
    doping_n=1e17,
    light_intensity=2.0
)
```

#### Overriding Material Parameters

```python
# Use silicon base properties but override diffusion coefficient
custom_diode = PNJunctionDiode.from_preset(
    material="Si",
    doping_p=1e16,
    doping_n=1e17,
    D_n=50.0  # Override default D_n
)
```

## Parameter Validation

When pydantic is installed, device parameters are automatically validated with helpful error messages.

### Validation Features

- **Range Checking**: Ensures parameters are within reasonable physical ranges
- **Consistency Validation**: Checks relationships like Einstein relation (L = √(D·τ))
- **Clear Error Messages**: Provides suggestions for typical parameter ranges
- **Automatic Type Conversion**: Safely converts parameter types

### Example Validation

```python
from semiconductor_sim.schemas import PNJunctionSchema

# Valid parameters
schema = PNJunctionSchema(
    doping_p=1e16,
    doping_n=1e17,
    temperature=300
)

# This will raise a validation error with helpful message
try:
    bad_schema = PNJunctionSchema(
        doping_p=1e10,  # Too low!
        doping_n=1e17
    )
except ValueError as e:
    print(e)
    # Output: doping_p = 1.00e+10 cm⁻³ is very low. 
    #         Typical doping levels are between 1e14 and 1e19 cm⁻³.
```

### Validation Rules

#### Doping Concentrations
- **Range**: 1e12 to 1e21 cm⁻³
- **Typical**: 1e14 to 1e19 cm⁻³
- **Special cases**: Tunnel diodes require > 1e18 cm⁻³

#### Temperature
- **Range**: 0 to 1000 K
- **Warnings**: < 200 K or > 500 K
- **Typical**: 250-400 K

#### Area
- **Range**: > 0 to 1.0 cm²
- **Warning**: > 1.0 cm² (unusually large)
- **Typical**: 1e-6 to 1e-2 cm²

#### Transport Parameters
- **Lifetimes**: 1e-12 to 1e-2 s
- **Diffusion coefficients**: 0.1 to 10,000 cm²/s
- **Diffusion lengths**: 1e-6 to 1e-1 cm
- **Einstein relation**: L ≈ √(D·τ) within factor of 10

## Available Schemas

- `DeviceConfigSchema`: Base schema for all devices
- `PNJunctionSchema`: PN junction diode parameters
- `LEDSchema`: LED parameters including efficiency and B coefficient
- `SolarCellSchema`: Solar cell parameters including light intensity
- `ZenerDiodeSchema`: Zener diode with breakdown voltage
- `TunnelDiodeSchema`: Tunnel diode with high doping requirements
- `VaractorDiodeSchema`: Varactor diode parameters
- `MOSCapacitorSchema`: MOS capacitor with oxide properties

## Error Handling

The system gracefully handles missing dependencies and provides clear guidance:

### Without Pydantic

```python
# Material presets work without pydantic
from semiconductor_sim import PNJunctionDiode
diode = PNJunctionDiode.from_preset("Si", doping_p=1e16, doping_n=1e17)
# Works fine, no validation

# Trying to import schemas without pydantic
try:
    from semiconductor_sim.schemas import PNJunctionSchema
except ImportError as e:
    print(e)
    # Output: pydantic is required for parameter schemas. 
    #         Install it with: pip install semiconductor-sim[schemas]
```

### Invalid Materials

```python
try:
    unknown_diode = PNJunctionDiode.from_preset("Unobtainium", 1e16, 1e17)
except ValueError as e:
    print(e)
    # Output: Material 'Unobtainium' not found. 
    #         Available materials: SI, GAAS, GE, GAN, INP
```

## Advanced Usage

### Custom Material Properties

```python
from semiconductor_sim.schemas.material_presets import MaterialPresets, MaterialProperties

# Define custom material
custom_props = MaterialProperties(
    name="Custom Semiconductor",
    bandgap=1.5,
    ni_300k=1e12,
    epsilon_r=10.0,
    mu_n=1000.0,
    mu_p=300.0,
    D_n=25.0,
    D_p=7.8,
    tau_n=1e-6,
    tau_p=1e-6,
    L_n=(25.0 * 1e-6) ** 0.5,
    L_p=(7.8 * 1e-6) ** 0.5,
    B=1e-12
)

# Add to database
MaterialPresets.add_material("CUSTOM", custom_props)

# Use in devices
custom_diode = PNJunctionDiode.from_preset("CUSTOM", 1e16, 1e17)
```

### Temperature-Dependent Calculations

```python
# Get temperature-dependent intrinsic carrier concentration
si_props = get_material_properties("Si")

temperatures = [250, 300, 350, 400]  # K
for T in temperatures:
    ni = si_props.ni(T)
    print(f"ni({T}K) = {ni:.2e} cm⁻³")
```

### Integration with Existing Code

The new features are fully backward compatible:

```python
# Old way still works
old_diode = PNJunctionDiode(
    doping_p=1e16,
    doping_n=1e17,
    area=1e-4,
    temperature=300,
    D_n=35.0,
    D_p=12.4
)

# New way with presets
new_diode = PNJunctionDiode.from_preset(
    "Si", 1e16, 1e17  # Much simpler!
)

# Both have the same capabilities
voltage = np.linspace(0, 1, 100)
old_iv = old_diode.iv_characteristic(voltage)
new_iv = new_diode.iv_characteristic(voltage)
```

## Best Practices

1. **Use Material Presets**: Start with `from_preset()` for realistic parameters
2. **Enable Validation**: Install with `[schemas]` extra for parameter checking
3. **Handle Errors**: Catch `ValueError` for parameter validation errors
4. **Override Selectively**: Use material presets as base, override specific parameters as needed
5. **Check Documentation**: Use `help()` on schemas for detailed parameter descriptions

## See Also

- [Complete Example Script](../examples/schemas_and_presets_demo.py)
- [API Reference](../semiconductor_sim/schemas/)
- [Device Documentation](../semiconductor_sim/devices/)