# PN Junction Theory

## Physical Principles

The PN junction forms when p-type and n-type semiconductor materials are brought into contact, creating a depletion region where mobile carriers are depleted due to diffusion and drift processes.

## Key Physics

### 1. Equilibrium Conditions

**Built-in Potential:**
```
V_bi = (k_B T / q) ln(N_A N_D / n_i²)
```

Where:
- N_A = acceptor concentration (p-side)
- N_D = donor concentration (n-side)  
- n_i = intrinsic carrier concentration

**Depletion Width:**
```
W = √(2ε_s V_bi / q) × √(1/N_A + 1/N_D)
```

### 2. Forward Bias Operation

**Ideal Diode Equation:**
```
I = I_s (e^(V/V_T) - 1)
```

**Saturation Current:**
```
I_s = q A n_i² (D_p/L_p N_D + D_n/L_n N_A)
```

Where:
- D_p, D_n = hole and electron diffusion coefficients
- L_p, L_n = hole and electron diffusion lengths
- A = junction area

### 3. Current Components

**Diffusion Current (majority carriers):**
- Dominates in forward bias
- Exponential voltage dependence
- Temperature sensitive via n_i²

**Generation-Recombination Current:**
- Important at low forward bias
- Linear voltage dependence in depletion region

### 4. Temperature Effects

**Intrinsic Concentration:**
```
n_i(T) = n_i(T_0) (T/T_0)^1.5 exp(-E_g/2k_B T)
```

**Thermal Voltage:**
```
V_T = k_B T / q ≈ 26 mV at T = 300K
```

## Model Implementation

### SRH Recombination

The Shockley-Read-Hall recombination rate accounts for trap-assisted recombination:

```
R_SRH = (np - n_i²) / (τ_p(n + n_1) + τ_n(p + p_1))
```

For mid-gap traps: n_1 ≈ p_1 ≈ n_i

### Temperature Scaling

The model scales the saturation current with temperature:

```python
n_i = 1.5e10 * (T / 300)**1.5  # Simplified temperature dependence
I_s = q * A * n_i**2 * (D_p/(L_p*N_D) + D_n/(L_n*N_A))
```

## Physical Limitations

### Low-Injection Assumption
- Model valid when injected minority carriers << majority carriers
- Breaks down at high forward bias or high current density

### Uniform Doping
- Assumes step junction profile
- Real devices may have graded junctions

### No High-Level Effects
- No series resistance
- No high-injection effects
- No avalanche breakdown

## Design Guidelines

### Doping Optimization
- **Light doping**: Lower built-in voltage, wider depletion region
- **Heavy doping**: Higher built-in voltage, narrower depletion region
- **Asymmetric doping**: One side dominates reverse saturation current

### Temperature Considerations
- Forward voltage decreases ~2 mV/°C
- Reverse current doubles every ~10°C
- Breakdown voltage varies with temperature

## Applications

### Rectification
- Convert AC to DC
- Forward bias: low resistance
- Reverse bias: high resistance (ideally infinite)

### Voltage References
- Forward voltage drop relatively constant
- Temperature compensation needed

### Switching
- Fast transition between on/off states
- Limited by minority carrier storage

## Related Devices

The PN junction forms the foundation for:
- **LEDs**: Add radiative recombination
- **Solar Cells**: Add photogeneration
- **Bipolar Transistors**: Multiple junctions
- **Varactors**: Voltage-dependent capacitance

## Key Equations Summary

| Parameter | Equation | Units |
|-----------|----------|-------|
| Built-in Voltage | V_bi = (k_B T/q) ln(N_A N_D/n_i²) | V |
| Saturation Current | I_s = qA n_i²(D_p/L_p N_D + D_n/L_n N_A) | A |
| Forward Current | I = I_s(e^(V/V_T) - 1) | A |
| Depletion Width | W = √(2ε_s V_bi/q × (1/N_A + 1/N_D)) | cm |
| Thermal Voltage | V_T = k_B T/q | V |

## References

1. Sze, S. M., & Ng, K. K. (2006). *Physics of Semiconductor Devices*. John Wiley & Sons. Chapter 2.
2. Streetman, B. G., & Banerjee, S. K. (2015). *Solid State Electronic Devices*. Pearson. Chapter 5.
3. Neamen, D. A. (2012). *Semiconductor Physics and Devices*. McGraw-Hill. Chapter 8.

---

**Next:** [LED Theory](led-theory.md) | **Related:** [PN Junction Model Card](../model-cards/pn-junction.md)