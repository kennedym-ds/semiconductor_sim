# Examples Gallery

This gallery showcases interactive examples and code snippets for each semiconductor device in SemiconductorSim. Each example demonstrates key device characteristics and practical usage patterns.

## Device Examples

### PN Junction Diode

**Key Features:** IV characteristics, SRH recombination, temperature effects

```python
import numpy as np
from semiconductor_sim.devices import PNJunctionDiode

# Create PN junction diode
diode = PNJunctionDiode(
    doping_p=1e17,  # 10^17 cm^-3 acceptors  
    doping_n=1e17,  # 10^17 cm^-3 donors
    temperature=300,
    area=1e-4
)

# Calculate IV characteristic
voltages = np.linspace(-1, 0.8, 100)
current, recombination = diode.iv_characteristic(
    voltages, 
    n_conc=1e16, 
    p_conc=1e16
)

# Plot results
diode.plot_iv_characteristic(voltages, current, recombination)
```

**Interactive Notebook:** [View on GitHub](https://github.com/kennedym-ds/semiconductor_sim/blob/main/examples/example_pn_junction.py) | 
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/example_pn_junction.py)

**Typical Output:**
- Forward voltage: ~0.7V at 1mA
- Reverse saturation current: ~10⁻¹² A
- SRH recombination rate: ~10¹⁴ cm⁻³s⁻¹

---

### LED (Light-Emitting Diode)

**Key Features:** Emission intensity, radiative efficiency, forward bias operation

```python
import numpy as np
from semiconductor_sim.devices import LED

# Create LED with high efficiency
led = LED(
    doping_p=5e17,      # Higher doping for LEDs
    doping_n=1e18,      # Heavy n-doping  
    efficiency=0.2,     # 20% internal quantum efficiency
    temperature=300,
    area=1e-4
)

# Calculate IV and emission characteristics
voltages = np.linspace(0, 3, 100)
current, emission = led.iv_characteristic(voltages)

# LED turn-on analysis
turn_on_voltage = voltages[np.argmax(emission > 0.1 * emission.max())]
print(f"LED turn-on voltage: {turn_on_voltage:.2f} V")
```

**Interactive Notebook:** [LED Interactive](https://github.com/kennedym-ds/semiconductor_sim/blob/main/examples/example_led_interactive.ipynb) | 
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/example_led_interactive.ipynb)

**3D Visualization:** [LED 3D Interactive](https://github.com/kennedym-ds/semiconductor_sim/blob/main/examples/example_led_3d_interactive.ipynb) | 
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/example_led_3d_interactive.ipynb)

**Typical Output:**
- Turn-on voltage: ~1.8V
- Peak emission: Forward bias > 2V
- Efficiency: 20% internal quantum efficiency

---

### Solar Cell

**Key Features:** Photocurrent generation, short-circuit current, open-circuit voltage

```python
import numpy as np
from semiconductor_sim.devices import SolarCell

# Create solar cell under illumination
solar_cell = SolarCell(
    doping_p=1e17,
    doping_n=1e17,
    area=1.0,           # 1 cm² cell
    light_intensity=1.0, # Standard test conditions
    temperature=300
)

# Calculate IV characteristic
voltages = np.linspace(-0.1, 0.7, 100)
current = solar_cell.iv_characteristic(voltages)

# Key solar cell parameters
print(f"Short-circuit current: {solar_cell.I_sc:.3f} A")
print(f"Open-circuit voltage: {solar_cell.V_oc:.3f} V")

# Power calculation
power = current * voltages
max_power = np.max(power)
fill_factor = max_power / (solar_cell.I_sc * solar_cell.V_oc)
print(f"Fill factor: {fill_factor:.3f}")
```

**Interactive Notebook:** [View on GitHub](https://github.com/kennedym-ds/semiconductor_sim/blob/main/examples/example_solar_cell.py) | 
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/example_solar_cell.py)

**Typical Output:**
- Short-circuit current: ~1 A/cm²
- Open-circuit voltage: ~0.6V
- Fill factor: ~0.7-0.8

---

### Tunnel Diode  

**Key Features:** Negative differential resistance, quantum tunneling, high-speed operation

```python
import numpy as np
from semiconductor_sim.devices import TunnelDiode

# Create tunnel diode with heavy doping
tunnel_diode = TunnelDiode(
    doping_p=5e19,  # Very heavy p-doping
    doping_n=5e19,  # Very heavy n-doping
    area=1e-4,
    temperature=300
)

# Calculate IV characteristic
voltages = np.linspace(-1, 1, 200)
current, recombination = tunnel_diode.iv_characteristic(
    voltages,
    n_conc=1e18,
    p_conc=1e18
)

# Find peak and valley points
forward_region = voltages > 0
peak_idx = np.argmax(current[forward_region])
valley_idx = np.argmin(current[voltages > voltages[peak_idx]])

print(f"Peak current: {current[peak_idx]:.2e} A")
print(f"Valley current: {current[valley_idx]:.2e} A")
print(f"Peak-to-valley ratio: {current[peak_idx]/current[valley_idx]:.1f}")
```

**Interactive Notebook:** [Tunnel Diode 3D](https://github.com/kennedym-ds/semiconductor_sim/blob/main/examples/example_tunnel_diode_3d_interactive.ipynb) | 
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/example_tunnel_diode_3d_interactive.ipynb)

**Typical Output:**
- Peak voltage: ~0.1V
- Valley voltage: ~0.4V  
- Peak-to-valley ratio: 3-10

---

### Varactor Diode

**Key Features:** Voltage-controlled capacitance, junction capacitance variation

```python
import numpy as np
from semiconductor_sim.devices import VaractorDiode

# Create varactor diode
varactor = VaractorDiode(
    doping_p=1e16,  # Moderate p-doping
    doping_n=1e18,  # Heavy n-doping (N+P structure)
    area=1e-4,
    temperature=300
)

# Calculate capacitance vs reverse voltage
reverse_voltages = np.linspace(0, -10, 50)
capacitance = varactor.capacitance(reverse_voltages)

# Capacitance variation analysis
C_max = capacitance[0]  # At 0V
C_min = capacitance[-1] # At maximum reverse bias
ratio = C_max / C_min

print(f"Capacitance ratio: {ratio:.1f}:1")
print(f"Zero-bias capacitance: {C_max:.2e} F")
print(f"Minimum capacitance: {C_min:.2e} F")

# Quality factor estimation (simplified)
f = 1e9  # 1 GHz
Q_est = 1 / (2 * np.pi * f * 50e-12 * C_max)  # Assuming 50 Ω series resistance
print(f"Estimated Q at 1 GHz: {Q_est:.1f}")
```

**Interactive Notebook:** [View on GitHub](https://github.com/kennedym-ds/semiconductor_sim/blob/main/examples/example_varactor_diode.py) | 
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/example_varactor_diode.py)

**Typical Output:**
- Capacitance ratio: 3-5:1
- Zero-bias capacitance: ~pF range
- Q-factor: 10-100 at GHz frequencies

---

### Zener Diode

**Key Features:** Voltage regulation, breakdown characteristics, ML voltage prediction

```python
import numpy as np
from semiconductor_sim.devices import ZenerDiode

# Create 5.1V Zener diode
zener = ZenerDiode(
    doping_p=1e17,
    doping_n=1e17,
    zener_voltage=5.1,
    area=1e-4,
    temperature=300
)

# Calculate IV characteristic
voltages = np.linspace(-8, 1, 200)
current, recombination = zener.iv_characteristic(
    voltages,
    n_conc=1e16,
    p_conc=1e16
)

# Use ML prediction for Zener voltage (if available)
try:
    predicted_vz = zener.predict_zener_voltage()
    print(f"ML predicted Zener voltage: {predicted_vz:.2f} V")
except:
    print("ML model not available, using configured value")

# Regulation analysis
breakdown_region = voltages < -zener.zener_voltage
if np.any(breakdown_region):
    breakdown_current = current[breakdown_region]
    dynamic_resistance = np.gradient(voltages[breakdown_region]) / np.gradient(breakdown_current)
    print(f"Dynamic resistance: {np.mean(dynamic_resistance):.1f} Ω")
```

**Interactive Notebook:** [Zener Interactive](https://github.com/kennedym-ds/semiconductor_sim/blob/main/examples/example_zener_diode_interactive.ipynb) | 
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/example_zener_diode_interactive.ipynb)

**ML Training:** [Train Zener Model](https://github.com/kennedym-ds/semiconductor_sim/blob/main/examples/train_ml_model_zener.py) | 
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/train_ml_model_zener.py)

**Typical Output:**
- Breakdown voltage: 2-200V range
- Dynamic resistance: <10 Ω in breakdown
- Temperature coefficient: ±2 mV/°C

---

### MOS Capacitor

**Key Features:** C-V characteristics, depletion width, surface physics

```python
import numpy as np
from semiconductor_sim.devices import MOSCapacitor

# Create MOS capacitor
mos_cap = MOSCapacitor(
    doping_p=1e16,          # Lightly doped p-substrate
    oxide_thickness=100e-7, # 100nm oxide
    oxide_permittivity=3.9, # SiO2
    area=1e-4,             # 0.01 cm²
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

# Threshold voltage extraction (simplified)
dC_dV = np.gradient(capacitance, gate_voltages)
max_slope_idx = np.argmax(np.abs(dC_dV))
V_T = gate_voltages[max_slope_idx]
print(f"Extracted threshold voltage: {V_T:.2f} V")
```

**Interactive Notebook:** [MOS Capacitor Interactive](https://github.com/kennedym-ds/semiconductor_sim/blob/main/examples/example_mos_capacitor_interactive.ipynb) | 
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/example_mos_capacitor_interactive.ipynb)

**Typical Output:**
- Oxide capacitance: ~pF range
- Maximum depletion width: ~μm range
- Threshold voltage: ~1V

---

## Advanced Examples

### Multi-Device Comparison

```python
import numpy as np
import matplotlib.pyplot as plt
from semiconductor_sim.devices import PNJunctionDiode, LED, TunnelDiode

# Create multiple devices for comparison
devices = {
    'PN Diode': PNJunctionDiode(1e17, 1e17),
    'LED': LED(5e17, 1e18, efficiency=0.2),
    'Tunnel Diode': TunnelDiode(5e19, 5e19)
}

# Compare IV characteristics
voltages = np.linspace(-0.5, 1.5, 100)
plt.figure(figsize=(10, 6))

for name, device in devices.items():
    if hasattr(device, 'iv_characteristic'):
        if name == 'LED':
            current, _ = device.iv_characteristic(voltages)
        else:
            current, _ = device.iv_characteristic(voltages, 1e16, 1e16)
        
        plt.semilogy(voltages, np.abs(current), label=name)

plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.legend()
plt.grid(True)
plt.title('Device Comparison: IV Characteristics')
plt.show()
```

### Temperature Analysis

```python
import numpy as np
from semiconductor_sim.devices import PNJunctionDiode

# Temperature sweep
temperatures = [250, 300, 350, 400]  # Kelvin
voltages = np.linspace(0, 0.8, 50)

plt.figure(figsize=(10, 6))
for T in temperatures:
    diode = PNJunctionDiode(1e17, 1e17, temperature=T)
    current, _ = diode.iv_characteristic(voltages, 1e16, 1e16)
    plt.semilogy(voltages, current, label=f'{T} K')

plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.legend()
plt.grid(True)
plt.title('Temperature Effects on PN Junction')
plt.show()
```

## Interactive Features

### Jupyter Widgets
All interactive notebooks include:
- **Slider controls** for device parameters
- **Real-time plotting** with parameter changes  
- **3D visualizations** for multi-parameter analysis
- **Export functionality** for data and plots

### Plotly Integration
Advanced examples feature:
- **Interactive zoom/pan**
- **Data point inspection**
- **Multi-axis plotting**
- **Animation capabilities**

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kennedym-ds/semiconductor_sim.git
   cd semiconductor_sim
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   pip install jupyter ipywidgets  # For interactive notebooks
   ```

3. **Run examples:**
   ```bash
   python examples/example_pn_junction.py
   jupyter notebook examples/  # For interactive notebooks
   ```

## Educational Progression

### Beginner Level
1. Start with **PN Junction** - understand basic semiconductor physics
2. Explore **LED** - see how light emission relates to electrical properties
3. Try **Solar Cell** - understand the reverse process (light → electricity)

### Intermediate Level  
4. Study **Varactor** - learn about voltage-controlled capacitance
5. Examine **Zener** - understand breakdown mechanisms
6. Analyze **MOS Capacitor** - foundation for modern electronics

### Advanced Level
7. Investigate **Tunnel Diode** - quantum mechanical effects
8. Compare all devices - understand relationships and trade-offs
9. Create custom analyses - develop your own characterization methods

## Contributing Examples

We welcome contributions of new examples! Please:
- Follow the existing code style
- Include comprehensive docstrings
- Add both script (.py) and notebook (.ipynb) versions
- Provide clear explanations of the physics involved
- Test with multiple parameter ranges

---

**Related:** [Model Cards](../model-cards/index.md) | [Theory Pages](../theory/index.md) | [API Reference](../api.md)