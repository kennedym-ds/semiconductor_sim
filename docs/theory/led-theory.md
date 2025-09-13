# LED Theory

## Physical Principles

Light-Emitting Diodes (LEDs) are PN junctions optimized for radiative recombination. When electrons and holes recombine in the active region, they can emit photons with energy approximately equal to the bandgap.

## Key Physics

### 1. Radiative Recombination

**Band-to-Band Recombination:**
```
e⁻ + h⁺ → photon (hν ≈ E_g)
```

**Radiative Recombination Rate:**
```
R_rad = B × n × p
```

Where:
- B = radiative recombination coefficient (cm³/s)
- n, p = electron and hole concentrations

### 2. Energy and Wavelength

**Photon Energy:**
```
E_photon = hν = E_g
```

**Wavelength:**
```
λ = hc / E_g = 1.24 / E_g(eV) μm
```

**Common LED Materials:**
| Material | Bandgap (eV) | Wavelength (nm) | Color |
|----------|--------------|-----------------|-------|
| GaAs | 1.42 | 870 | Near-IR |
| GaAsP | 1.9-2.2 | 565-650 | Yellow-Red |
| GaN | 3.4 | 365 | UV |
| InGaN | 2.4-3.4 | 365-515 | Blue-UV |

### 3. Efficiency Considerations

**Internal Quantum Efficiency:**
```
η_int = R_rad / (R_rad + R_nr)
```

Where R_nr includes all non-radiative recombination processes.

**External Quantum Efficiency:**
```
η_ext = η_int × η_extraction
```

Where η_extraction accounts for light extraction from the semiconductor.

## Recombination Mechanisms

### 1. Radiative (Desired)
- **Band-to-band**: Direct bandgap materials preferred
- **Excitonic**: Bound electron-hole pairs
- **Free-to-bound**: Free carrier to trapped state

### 2. Non-Radiative (Parasitic)
- **SRH**: Via trap states in bandgap
- **Auger**: Three-carrier process (dominant at high injection)
- **Surface**: At interfaces and surfaces

### 3. Model Implementation

The LED model combines both mechanisms:

```python
# Forward current (same as diode)
I = I_s * (exp(V/V_T) - 1)

# Emission intensity (proportional to radiative recombination)
emission = efficiency * R_rad * area

# Where R_rad is calculated from carrier concentrations
```

## Light Emission Characteristics

### 1. Forward Bias Operation

**Threshold Behavior:**
- Minimal light below ~1.5V (for visible LEDs)
- Exponential increase with voltage above threshold
- Nearly linear with current in normal operation

**Current-Light Relationship:**
```
L ∝ I (in linear region)
```

### 2. Temperature Effects

**Thermal Quenching:**
- Efficiency decreases with temperature
- Non-radiative rates increase faster than radiative

**Wavelength Shift:**
- Bandgap decreases with temperature (~0.3 meV/K)
- Red-shift of emission spectrum

### 3. Efficiency Droop

At high current densities:
- Auger recombination increases
- Efficiency peaks then decreases
- Thermal effects compound the problem

## LED Design Considerations

### 1. Material Selection

**Direct vs. Indirect Bandgap:**
- **Direct** (GaAs, GaN): High radiative efficiency
- **Indirect** (Si, GaP): Low efficiency, need dopants/quantum dots

**Bandgap Engineering:**
- Alloy composition controls wavelength
- Quantum wells for improved efficiency
- Multiple quantum wells for higher output

### 2. Doping Optimization

**Heavy Doping:**
- Increases injection efficiency
- Reduces series resistance
- May increase non-radiative recombination

**Asymmetric Doping:**
- Optimizes carrier injection balance
- One side provides majority carriers

### 3. Structure Design

**Double Heterostructure:**
- Confines carriers to active region
- Reduces losses to cladding layers

**Light Extraction:**
- Surface texturing
- Shaped substrates
- Photonic crystals

## Model Limitations

### 1. Simplified Emission
- No spectral details
- No angular distribution
- No polarization effects

### 2. Efficiency Assumptions
- Constant internal quantum efficiency
- No temperature dependence
- No current-dependent droop

### 3. No Optical Effects
- No self-absorption
- No guided modes
- No extraction efficiency variations

## Performance Metrics

### 1. Efficiency Definitions

**Wall-Plug Efficiency:**
```
η_wp = P_optical / P_electrical = (hν × I_photons) / (V × I)
```

**Luminous Efficacy:**
```
η_lum = Φ_luminous / P_electrical [lm/W]
```

### 2. Light Output

**Radiant Flux:**
```
Φ_e = η_ext × (I/q) × hν [W]
```

**Luminous Flux:**
- Weighted by human eye response
- Peak at 555 nm (green)

## Applications and Trade-offs

### 1. Display Applications
- **Requirements**: High brightness, color purity
- **Trade-offs**: Efficiency vs. saturation

### 2. Lighting Applications
- **Requirements**: High efficiency, long lifetime
- **Trade-offs**: Cost vs. performance

### 3. Communication
- **Requirements**: High speed, reliability
- **Trade-offs**: Speed vs. power consumption

## Key Equations Summary

| Parameter | Equation | Units |
|-----------|----------|-------|
| Photon Energy | E = hν = E_g | eV |
| Wavelength | λ = hc/E_g = 1.24/E_g(eV) | μm |
| Radiative Rate | R_rad = B × n × p | cm⁻³s⁻¹ |
| Internal Efficiency | η_int = R_rad/(R_rad + R_nr) | - |
| Wall-Plug Efficiency | η_wp = P_opt/P_elec | - |

## References

1. Schubert, E. F. (2006). *Light-Emitting Diodes*. Cambridge University Press.
2. Piprek, J. (2003). *Semiconductor Optoelectronic Devices*. Academic Press.
3. Bergh, A., & Dean, P. (1976). *Light-Emitting Diodes*. Clarendon Press.

---

**Next:** Solar Cell Theory (Coming Soon) | **Related:** [LED Model Card](../model-cards/led.md)