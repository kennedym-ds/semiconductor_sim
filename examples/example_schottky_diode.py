# examples/example_schottky_diode.py

import numpy as np
from semiconductor_sim import SchottkyDiode


def main() -> None:
    """
    Demonstrate Schottky diode characteristics with temperature dependence
    and series resistance effects.
    """
    print("Schottky Diode Device Simulation")
    print("=" * 40)
    
    # Define voltage range for characterization
    voltage = np.linspace(-0.5, 0.8, 200)
    
    # Example 1: Basic Schottky diode (Silicon with typical parameters)
    print("\n1. Basic Silicon Schottky Diode")
    print("-" * 35)
    
    diode_basic = SchottkyDiode(
        barrier_height=0.8,    # eV - typical for Al/Si
        area=1e-4,            # cm^2
        temperature=300,       # K
        A_eff=120.0,          # A/(cm^2·K^2) - typical for Si
        series_resistance=0.0,  # Ohm
        image_force_lowering=0.0  # eV
    )
    
    print(f"Barrier height: {diode_basic.barrier_height:.2f} eV")
    print(f"Saturation current: {diode_basic.I_s:.2e} A")
    print(f"Area: {diode_basic.area:.1e} cm²")
    
    # Calculate and display current at key voltages
    test_voltages = np.array([0.0, 0.2, 0.4, 0.6])
    currents, = diode_basic.iv_characteristic(test_voltages)
    
    print("\nVoltage (V) | Current (A)")
    print("-" * 25)
    for v, i in zip(test_voltages, currents):
        print(f"{v:8.1f}   | {i:.2e}")
    
    # Plot basic IV characteristic
    current_basic, = diode_basic.iv_characteristic(voltage)
    diode_basic.plot_iv_characteristic(voltage, current_basic, 
                                     "Basic Schottky Diode (Al/Si)")
    
    # Example 2: Effect of series resistance
    print("\n2. Effect of Series Resistance")
    print("-" * 35)
    
    diode_with_rs = SchottkyDiode(
        barrier_height=0.8,
        area=1e-4,
        temperature=300,
        A_eff=120.0,
        series_resistance=5.0,  # 5 Ohm series resistance
        image_force_lowering=0.0
    )
    
    current_with_rs, = diode_with_rs.iv_characteristic(voltage)
    
    print(f"Series resistance: {diode_with_rs.series_resistance:.1f} Ω")
    print("Comparison at 0.6V:")
    print(f"  Without Rs: {currents[-1]:.2e} A")
    
    test_current_rs, = diode_with_rs.iv_characteristic(np.array([0.6]))
    print(f"  With Rs:    {test_current_rs[0]:.2e} A")
    print(f"  Reduction:  {(1 - test_current_rs[0]/currents[-1])*100:.1f}%")
    
    diode_with_rs.plot_iv_characteristic(voltage, current_with_rs,
                                       "Schottky Diode with Series Resistance")
    
    # Example 3: Temperature dependence demonstration
    print("\n3. Temperature Dependence")
    print("-" * 35)
    
    temperatures = np.array([250, 300, 350, 400])  # K
    
    print("Temperature (K) | I_s (A)")
    print("-" * 25)
    
    for T in temperatures:
        diode_temp = SchottkyDiode(barrier_height=0.8, temperature=T)
        print(f"{T:10.0f}     | {diode_temp.I_s:.2e}")
    
    # Plot temperature dependence
    diode_basic.plot_temperature_dependence(voltage, temperatures)
    
    # Example 4: Different barrier heights (different metals)
    print("\n4. Different Metal-Semiconductor Combinations")
    print("-" * 50)
    
    metals = [
        ("Aluminum", 0.72),   # Al/Si
        ("Titanium", 0.61),   # Ti/Si  
        ("Tungsten", 0.67),   # W/Si
        ("Platinum", 0.84),   # Pt/Si
    ]
    
    print("Metal      | φ_B (eV) | I_s (A)")
    print("-" * 35)
    
    for metal_name, phi_b in metals:
        diode_metal = SchottkyDiode(barrier_height=phi_b, temperature=300)
        print(f"{metal_name:10s} | {phi_b:6.2f}   | {diode_metal.I_s:.2e}")
    
    # Example 5: Image force lowering effect
    print("\n5. Image Force Lowering Effect")
    print("-" * 35)
    
    diode_no_ifl = SchottkyDiode(barrier_height=0.8, image_force_lowering=0.0)
    diode_with_ifl = SchottkyDiode(barrier_height=0.8, image_force_lowering=0.05)
    
    print(f"Original barrier height: {diode_no_ifl.barrier_height:.2f} eV")
    print(f"With image force lowering:")
    print(f"  Effective barrier: {diode_with_ifl.barrier_height_eff:.2f} eV")
    print(f"  I_s increase: {diode_with_ifl.I_s / diode_no_ifl.I_s:.1f}x")
    
    # Example 6: Reverse characteristics
    print("\n6. Reverse Leakage Characteristics")
    print("-" * 40)
    
    reverse_voltages = np.array([-0.1, -0.5, -1.0, -2.0])
    reverse_currents, = diode_basic.iv_characteristic(reverse_voltages)
    
    print("Reverse Voltage (V) | Leakage Current (A)")
    print("-" * 40)
    for v, i in zip(reverse_voltages, reverse_currents):
        print(f"{v:15.1f}     | {abs(i):.2e}")
    
    print(f"\nTheoretical reverse saturation: {diode_basic.I_s:.2e} A")
    
    print("\nSimulation completed! Check the generated plots for visual analysis.")


if __name__ == "__main__":
    main()