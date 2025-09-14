---
post_title: Materials Registry
author1: Michael Kennedy
post_slug: materials-registry
microsoft_alias: mkennedy
featured_image: https://dummyimage.com/1200x630/0d47a1/ffffff&text=Semiconductor+Materials
categories: Education
tags: semiconductors, materials, bandgap
ai_note: Drafted with AI assistance and human review
summary: Overview of the built-in materials registry (Si, Ge, GaAs) with temperature-dependent bandgap, effective densities of states, and intrinsic carrier concentration.
post_date: 2025-09-14
---

## Overview

This project includes a small materials registry to simplify selecting
common semiconductors and computing temperature-dependent properties:

- Bandgap via the Varshni equation
- Effective density of states `Nc(T)`, `Nv(T)` using `A·T^{3/2}` forms
- Intrinsic carrier concentration `ni(T)`

Initial materials provided: Silicon (Si), Germanium (Ge), Gallium Arsenide (GaAs).

## Usage

```python
from semiconductor_sim.materials import get_material, list_materials

print(list(list_materials()))  # ['Si', 'Ge', 'GaAs']
si = get_material('Si')
Eg_300 = si.Eg(300.0)
ni_300 = si.ni(300.0)
```

Devices can optionally accept a `material`. For example,
`PNJunctionDiode` uses `ni(T)` from the selected material when provided.

### Using materials with devices

You can pass a `material` to several devices to influence temperature-dependent
behavior like dark saturation current and recombination:

```python
from semiconductor_sim import LED, SolarCell, PNJunctionDiode
from semiconductor_sim.materials import get_material

si = get_material("Si")

# PN diode using Silicon
d = PNJunctionDiode(1e17, 1e17, material=si)

# LED using Silicon; I_s depends on ni(T) from the material
led = LED(1e17, 1e17, efficiency=0.2, material=si)

# Solar cell using Silicon; I_s and thus V_oc depend on the material
sc = SolarCell(1e17, 1e17, light_intensity=1.0, material=si)
```

See device pages in the API reference for constructor signatures. When a
device exposes a `material` argument, it will use material properties in its
internal calculations (e.g., intrinsic carrier concentration for diode dark
current). This section serves as a dedicated reference for materials-enabled
usage.

## Formulas

- Varshni bandgap: $E_g(T)=E_{g0}-\frac{\alpha T^2}{T+\beta}$
- Effective DOS: $N_c=A\,T^{3/2}$, $N_v=B\,T^{3/2}$
- Intrinsic concentration:
  $n_i=\sqrt{N_c N_v}\,\exp\!\left(-\frac{E_g}{2 k_B T}\right)$ with
  $k_B=8.617\times10^{-5}$ eV/K

## References

- Ioffe Institute Semiconductor Database
  - Silicon: [ioffe.ru/Semicond/Si](https://www.ioffe.ru/SVA/NSM/Semicond/Si/)
  - Germanium: [ioffe.ru/Semicond/Ge](https://www.ioffe.ru/SVA/NSM/Semicond/Ge/)
  - GaAs: [ioffe.ru/Semicond/GaAs](https://www.ioffe.ru/SVA/NSM/Semicond/GaAs/)

Values and formulas used are consistent with the Ioffe pages:

- Bandgap temperature dependence via Varshni
- $T^{3/2}$ scaling for $N_c$ and $N_v$

For GaAs we match the 300 K reported $N_c$ and $N_v$ with a simple
$T^{3/2}$ scaling for education-oriented use.
