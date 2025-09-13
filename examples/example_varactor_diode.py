# examples/example_varactor_diode.py

import numpy as np
from semiconductor_sim import VaractorDiode

def main():
    
    # Define voltage range for IV characteristics
    voltage_iv = np.linspace(-0.5, 5, 200)
    
    # Define reverse voltage range for capacitance
    voltage_cap = np.linspace(1, 5, 100)
    
    # Initialize the Varactor Diode
    varactor = VaractorDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    
    # Assume constant carrier concentrations
    n_conc = np.full_like(voltage_iv, 1e16)  # cm^-3
    p_conc = np.full_like(voltage_iv, 1e16)  # cm^-3
    
    # Calculate current and recombination rate
    current, recombination = varactor.iv_characteristic(voltage_iv, n_conc, p_conc)
    
    # Plot IV characteristics with recombination
    varactor.plot_iv_characteristic(voltage_iv, current, recombination)
    
    # Calculate and plot capacitance vs. reverse voltage
    capacitance = varactor.capacitance(voltage_cap)
    varactor.plot_capacitance_vs_voltage(voltage_cap)

if __name__ == "__main__":
    main()
