# Device Model Cards

This section provides detailed model cards for each semiconductor device implemented in SemiconductorSim. Each model card includes comprehensive information about inputs, outputs, assumptions, validity ranges, and usage examples.

## Available Devices

### Basic Semiconductor Devices

| Device | Description | Key Features |
|--------|-------------|--------------|
| [PN Junction Diode](pn-junction.md) | Fundamental semiconductor junction | IV characteristics, SRH recombination, temperature effects |
| [LED](led.md) | Light-emitting diode | Emission intensity, radiative recombination, efficiency modeling |
| [Solar Cell](solar-cell.md) | Photovoltaic device | Photocurrent generation, short-circuit/open-circuit parameters |

### Specialized Diodes

| Device | Description | Key Features |
|--------|-------------|--------------|
| [Tunnel Diode](tunnel-diode.md) | Quantum tunneling device | Negative differential resistance, high-speed operation |
| [Varactor Diode](varactor-diode.md) | Voltage-controlled capacitor | Junction capacitance variation, frequency tuning |
| [Zener Diode](zener-diode.md) | Voltage regulation device | Breakdown characteristics, voltage reference |

### Advanced Structures

| Device | Description | Key Features |
|--------|-------------|--------------|
| [MOS Capacitor](mos-capacitor.md) | Metal-oxide-semiconductor structure | C-V characteristics, depletion width, MOSFET foundation |

## Model Card Contents

Each model card provides:

- **Overview**: Device purpose and basic physics
- **Implementation**: Class name and key methods
- **Inputs/Outputs**: Complete parameter descriptions
- **Assumptions**: Physical and mathematical approximations
- **Validity Range**: Operating conditions and limitations
- **Example Usage**: Code snippets and typical applications
- **References**: Relevant textbooks and papers

## Quick Comparison

### Current Transport Mechanisms

| Device | Primary Transport | Secondary Effects |
|--------|------------------|-------------------|
| PN Junction | Diffusion | SRH recombination |
| LED | Diffusion | Radiative recombination |
| Solar Cell | Photo-generated | Diffusion (dark current) |
| Tunnel Diode | Quantum tunneling | Diffusion (valley region) |
| Varactor | Leakage current | Capacitive behavior |
| Zener | Breakdown current | Normal diode (forward) |
| MOS Capacitor | Gate leakage | Capacitive behavior |

### Typical Operating Ranges

| Device | Forward Voltage | Reverse Voltage | Primary Application |
|--------|----------------|-----------------|-------------------|
| PN Junction | 0-1V | 0-10V | Rectification, switching |
| LED | 1.5-3V | Limited | Light emission |
| Solar Cell | -0.5-0.8V | Limited | Power generation |
| Tunnel Diode | 0-1V | 0-2V | Oscillators, amplifiers |
| Varactor | <0.5V | 0-20V | Frequency tuning |
| Zener | 0-1V | Breakdown | Voltage regulation |
| MOS Capacitor | Gate: ±5V | N/A | Capacitive sensing |

### Key Parameters

| Device | Critical Parameters | Design Trade-offs |
|--------|-------------------|------------------|
| PN Junction | Doping levels, area | Speed vs. current capability |
| LED | Efficiency, emission | Brightness vs. efficiency |
| Solar Cell | Light intensity, area | Power vs. voltage |
| Tunnel Diode | Heavy doping | Peak current vs. valley current |
| Varactor | Doping profile | Capacitance ratio vs. Q-factor |
| Zener | Breakdown voltage | Regulation vs. power dissipation |
| MOS Capacitor | Oxide thickness | Capacitance vs. breakdown voltage |

## Using Model Cards

### For Device Selection
1. **Identify Requirements**: Voltage, current, frequency, temperature
2. **Compare Capabilities**: Check validity ranges and limitations
3. **Review Trade-offs**: Understand design compromises
4. **Validate Assumptions**: Ensure model fits your application

### For Parameter Extraction
1. **Understand Inputs**: Required vs. optional parameters
2. **Check Defaults**: Verify default values are reasonable
3. **Calibrate Models**: Compare with experimental data
4. **Document Assumptions**: Record modeling choices

### For Educational Use
1. **Start Simple**: Begin with basic PN junction
2. **Build Complexity**: Progress to specialized devices
3. **Compare Models**: Understand relationships between devices
4. **Explore Limits**: Test boundary conditions

## Related Documentation

- **[Theory Pages](../theory/index.md)**: Physical principles and derivations
- **[Examples Gallery](../gallery/index.md)**: Visual examples and code snippets  
- **[API Reference](../api.md)**: Complete method documentation
- **[Getting Started](../getting-started.md)**: Installation and first steps

---

*For questions about specific models or to request additional features, please refer to the main repository or contact the maintainers.*