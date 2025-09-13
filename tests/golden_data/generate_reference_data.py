#!/usr/bin/env python3
"""
Generate golden reference data for testing semiconductor devices.

This script creates CSV files with reference data based on textbook formulas
for ideal semiconductor devices. These golden datasets are used to validate
the simulation implementations against well-known analytical solutions.

Reference sources:
- Streetman & Banerjee, "Solid State Electronic Devices" (6th Ed.)
- Sze & Ng, "Physics of Semiconductor Devices" (3rd Ed.)
- Ideal diode equation: I = I_s * (exp(V/V_T) - 1)
"""

import numpy as np
import pandas as pd
import os
from typing import Dict, Any

# Constants (consistent with semiconductor_sim.utils.constants)
q = 1.602176634e-19  # Elementary charge (C)
k_B = 1.380649e-23  # Boltzmann constant (J/K)
DEFAULT_T = 300.0    # Default temperature (K)


def ideal_diode_iv(voltage: np.ndarray, I_s: float, temperature: float = DEFAULT_T) -> np.ndarray:
    """
    Calculate ideal diode current using Shockley equation.
    
    I = I_s * (exp(V/V_T) - 1)
    
    Args:
        voltage: Voltage array (V)
        I_s: Saturation current (A)
        temperature: Temperature (K)
    
    Returns:
        Current array (A)
    """
    V_T = k_B * temperature / q  # Thermal voltage
    return I_s * (np.exp(voltage / V_T) - 1)


def generate_pn_junction_data() -> Dict[str, Any]:
    """Generate reference IV data for PN junction diode."""
    # Voltage range: reverse bias to forward bias
    voltage = np.linspace(-1.0, 1.0, 101)
    
    # Typical parameters for silicon PN diode
    I_s = 1e-12  # Saturation current (A)
    temperature = 300.0  # Room temperature (K)
    
    current = ideal_diode_iv(voltage, I_s, temperature)
    
    return {
        'device': 'pn_junction',
        'source': 'Ideal diode equation (Streetman & Banerjee)',
        'parameters': {
            'I_s': I_s,
            'temperature': temperature,
            'V_T': k_B * temperature / q
        },
        'data': pd.DataFrame({
            'voltage_V': voltage,
            'current_A': current
        })
    }


def generate_led_data() -> Dict[str, Any]:
    """Generate reference IV data for LED."""
    # LED typically operates in forward bias only, limited voltage range
    voltage = np.linspace(0.0, 2.5, 51)  # Reduced range and points
    
    # LED parameters (higher threshold, different I_s)
    I_s = 1e-15  # Lower saturation current
    temperature = 300.0
    
    current = ideal_diode_iv(voltage, I_s, temperature)
    
    # Simple emission model: proportional to current above threshold
    V_threshold = 1.5  # Typical LED threshold voltage
    emission = np.where(voltage > V_threshold, 
                       (current - I_s) * 1e9,  # More reasonable scaling
                       0.0)
    
    return {
        'device': 'led',
        'source': 'Ideal diode + simplified emission model',
        'parameters': {
            'I_s': I_s,
            'temperature': temperature,
            'V_threshold': V_threshold,
            'V_T': k_B * temperature / q
        },
        'data': pd.DataFrame({
            'voltage_V': voltage,
            'current_A': current,
            'emission_arb': emission
        })
    }


def generate_solar_cell_data() -> Dict[str, Any]:
    """Generate reference IV data for solar cell."""
    # Solar cell operates in fourth quadrant (negative current for positive voltage)
    voltage = np.linspace(-0.5, 0.8, 101)
    
    # Solar cell parameters
    I_s = 1e-10  # Dark saturation current
    I_ph = 1e-3  # Photocurrent (illumination dependent)
    temperature = 300.0
    
    # Solar cell equation: I = I_ph - I_s * (exp(V/V_T) - 1)
    # Note: convention here is that negative current = power generation
    dark_current = ideal_diode_iv(voltage, I_s, temperature)
    current = -I_ph + dark_current  # Negative I_ph for power generation
    
    return {
        'device': 'solar_cell',
        'source': 'Ideal solar cell equation (Sze & Ng)',
        'parameters': {
            'I_s': I_s,
            'I_ph': I_ph,
            'temperature': temperature,
            'V_T': k_B * temperature / q
        },
        'data': pd.DataFrame({
            'voltage_V': voltage,
            'current_A': current
        })
    }


def save_golden_data(data_dict: Dict[str, Any], output_dir: str) -> None:
    """Save golden data to CSV with metadata."""
    device = data_dict['device']
    df = data_dict['data']
    
    # Save CSV data
    csv_path = os.path.join(output_dir, f"{device}_reference.csv")
    df.to_csv(csv_path, index=False, float_format='%.6e')
    
    # Save metadata
    metadata = {k: v for k, v in data_dict.items() if k != 'data'}
    metadata_path = os.path.join(output_dir, f"{device}_metadata.txt")
    
    with open(metadata_path, 'w') as f:
        f.write(f"Golden Reference Data: {device}\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Source: {metadata['source']}\n\n")
        f.write("Parameters:\n")
        for key, value in metadata['parameters'].items():
            f.write(f"  {key}: {value}\n")
        f.write(f"\nData shape: {df.shape}\n")
        f.write(f"Columns: {list(df.columns)}\n")


def main():
    """Generate all golden reference datasets."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate datasets
    datasets = [
        generate_pn_junction_data(),
        generate_led_data(),
        generate_solar_cell_data(),
    ]
    
    # Save all datasets
    for dataset in datasets:
        save_golden_data(dataset, script_dir)
        print(f"Generated golden data for {dataset['device']}")
    
    print(f"\nGolden reference data saved to: {script_dir}")


if __name__ == "__main__":
    main()