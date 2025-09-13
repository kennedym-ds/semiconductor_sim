# Development Roadmap

The SemiconductorSim 0.2.x series focuses on expanding device coverage, improving physics accuracy, and enhancing user experience. This page provides an overview of planned features and milestones.

## Current Status

**Current Version:** 0.1.1  
**Next Major Release:** 0.2.0 (Target: Q1 2024)

## Planned Features

### Core Device Expansion (0.2.0)
- **BJT Model (Ebers–Moll):** Bipolar junction transistor simulation with temperature effects
- **Schottky Diode:** Metal-semiconductor junction modeling with barrier height calculations
- **Enhanced Packaging:** Optional dependencies, robust wheels, improved release pipeline

### Physics & Performance (0.2.1)
- **Parasitic Modeling:** Capacitance and resistance effects across all devices
- **Temperature Refinements:** Enhanced thermal dependence for material parameters
- **Acceleration:** Numba/JAX optimization for large parameter sweeps
- **Benchmarking:** Automated performance testing and regression detection

### User Experience (0.2.2)
- **Parameter Validation:** Structured schemas with pydantic and material databases
- **Command Line Interface:** Batch simulations and automated parameter sweeps
- **Enhanced Documentation:** Model cards, theory guides, and interactive examples

## Timeline Overview

| Milestone | Target | Focus Area | Key Features |
|-----------|--------|------------|--------------|
| 0.2.0 | Q1 2024 | Device Expansion | BJT, Schottky, Packaging |
| 0.2.1 | Q2 2024 | Physics & Performance | Parasitics, Acceleration |
| 0.2.2 | Q3 2024 | User Experience | CLI, Schemas, Docs |

## Get Involved

We welcome contributions to any of these milestones! Check our [GitHub repository](https://github.com/kennedym-ds/semiconductor_sim) for:

- Issues labeled `good-first-issue` for newcomers
- Detailed acceptance criteria for each feature
- Coordination discussions to avoid duplicate work

For the complete roadmap with detailed specifications, see our [full roadmap document](https://github.com/kennedym-ds/semiconductor_sim/blob/main/ROADMAP.md).