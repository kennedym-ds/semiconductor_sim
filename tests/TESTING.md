# Testing Documentation: Golden Reference Data and Property Tests

This document describes the testing approach for the semiconductor simulation library, focusing on golden reference data and property-based testing implemented to strengthen validation.

## Golden Reference Data

### Overview

Golden reference datasets provide baseline validation for semiconductor device implementations against well-established theoretical models. These datasets are used to ensure accuracy and detect regressions in device behavior.

### Data Sources

#### PN Junction Diode
- **Source**: Ideal diode equation from Streetman & Banerjee, "Solid State Electronic Devices" (6th Ed.)
- **Model**: I = I_s × (exp(V/V_T) - 1)
- **Parameters**:
  - I_s = 1×10⁻¹² A (saturation current)
  - T = 300 K (room temperature)
  - V_T = k_B×T/q = 0.0259 V (thermal voltage)
- **Voltage Range**: -1.0 V to +1.0 V (101 points)
- **File**: `tests/golden_data/pn_junction_reference.csv`

#### LED (Light Emitting Diode)
- **Source**: Ideal diode equation with simplified emission model
- **Model**: 
  - Current: I = I_s × (exp(V/V_T) - 1)
  - Emission: E = (I - I_s) × 10⁹ for V > 1.5V, else 0
- **Parameters**:
  - I_s = 1×10⁻¹⁵ A (lower saturation current)
  - T = 300 K
  - V_threshold = 1.5 V (emission threshold)
- **Voltage Range**: 0.0 V to +2.5 V (51 points)
- **File**: `tests/golden_data/led_reference.csv`

#### Solar Cell
- **Source**: Standard photovoltaic equation from Sze & Ng, "Physics of Semiconductor Devices" (3rd Ed.)
- **Model**: I = -I_ph + I_s × (exp(V/V_T) - 1)
- **Parameters**:
  - I_ph = 1×10⁻³ A (photocurrent)
  - I_s = 1×10⁻¹⁰ A (dark saturation current)
  - T = 300 K
- **Voltage Range**: -0.5 V to +0.8 V (101 points)
- **File**: `tests/golden_data/solar_cell_reference.csv`

### Test Tolerances

The following tolerances are used in golden reference comparisons:

| Parameter | Tolerance | Justification |
|-----------|-----------|---------------|
| Current (relative) | 5% | Accounts for model approximations and parameter variations |
| Current (absolute) | 1 pA | Noise floor for very small currents |
| Emission (relative) | 10% | Simplified emission model has larger uncertainty |
| Shape comparison | 10% | For trend and monotonicity validation |

### Validation Approach

Rather than requiring exact numerical matches (which would be too restrictive given model differences), the golden reference tests validate:

1. **Shape consistency**: Forward/reverse bias behavior
2. **Monotonicity**: Current increases with voltage in forward bias
3. **Physical bounds**: Reasonable current magnitudes
4. **Sign conventions**: Correct current polarity for each device type

## Property-Based Testing

### Overview

Property-based tests use Hypothesis to automatically generate test cases that validate fundamental physical and mathematical properties of the semiconductor devices.

### Test Categories

#### 1. Monotonicity Tests
- **Purpose**: Ensure IV characteristics are physically realistic
- **Implementation**: Forward bias current must be non-decreasing
- **Devices**: PN Junction, LED
- **Strategy**: Generate sorted voltage arrays, verify current monotonicity

#### 2. Bounds Testing
- **Purpose**: Prevent unphysical results
- **Implementation**: Current magnitudes within reasonable ranges
- **Bounds**: 
  - PN Junction: |I| < 1×10⁶ A
  - LED: |I| < 1×10³⁰ A (relaxed for exponential growth)
  - Solar Cell: |I| < 1×10⁶ A (for operating range -0.5V to 1V)

#### 3. Reverse Bias Negativity
- **Purpose**: Validate correct diode behavior
- **Implementation**: Negative voltages produce negative currents
- **Devices**: PN Junction, LED

#### 4. Broadcasting Consistency
- **Purpose**: Ensure array operations work correctly
- **Implementation**: Output shapes match input voltage array shapes
- **Coverage**: All device types with various array sizes

#### 5. Temperature Dependence
- **Purpose**: Validate thermal behavior
- **Implementation**: Saturation current increases with temperature
- **Range**: 250 K to 400 K
- **Physical basis**: Intrinsic carrier concentration ~ T^1.5

#### 6. Parameter Sensitivity
- **Purpose**: Ensure reasonable parameter dependencies
- **Implementation**: Device characteristics change appropriately with doping
- **Range**: 1×10¹⁵ to 1×10¹⁹ cm⁻³

### Numerical Stability Tests

#### safe_expm1 Function
- **Purpose**: Validate numerical function used in device calculations
- **Properties tested**:
  - Always finite output
  - Approaches x for small |x|
  - Bounded above -1 for negative inputs
  - Correct asymptotic behavior

### Deterministic Testing

To ensure reproducible results in CI environments:

#### RNG Seed Configuration
- **NumPy seed**: Fixed at 42 for reproducibility
- **Hypothesis settings**: 
  - `derandomize=True` for consistent test generation
  - Environment-based profiles: "dev" (10 examples) vs "ci" (50 examples)

#### CI Configuration
Set environment variable `HYPOTHESIS_PROFILE=ci` for comprehensive testing in automated environments.

## Test Execution

### Running Tests

```bash
# Run all tests
pytest tests/

# Run only golden reference tests
pytest tests/test_golden_reference.py

# Run only property tests
pytest tests/test_properties.py

# Run with CI profile (more examples)
HYPOTHESIS_PROFILE=ci pytest tests/
```

### Expected Coverage

The expanded test suite covers:
- 11 golden reference validation tests
- 19 property-based tests with automatic test case generation
- All major device types (PN Junction, LED, Solar Cell)
- Temperature and parameter sensitivity
- Numerical stability and edge cases

## Maintenance

### Updating Golden Data

To regenerate golden reference data (e.g., after parameter changes):

```bash
cd tests/golden_data
python generate_reference_data.py
```

### Adding New Devices

For new device implementations:

1. Add golden data generation in `generate_reference_data.py`
2. Create test class in `test_golden_reference.py`
3. Add property tests in `test_properties.py`
4. Update this documentation

### Tolerance Adjustments

Tolerance values may need adjustment as models evolve:
- Tighter tolerances for improved models
- Looser tolerances for complex physics additions
- Document rationale for any changes