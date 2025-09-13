# examples/example_mos_capacitor.py

import numpy as np

from semiconductor_sim import MOSCapacitor


def main():
    # Define voltage range for IV characteristics
    voltage_iv = np.linspace(-5, 5, 500)

    # Define voltage range for C-V characteristics
    voltage_cv = np.linspace(-5, 5, 500)

    # Initialize the MOS Capacitor with doping concentrations, oxide thickness, and temperature
    mos = MOSCapacitor(
        doping_p=1e17,
        oxide_thickness=1e-6,  # 1 micron
        oxide_permittivity=3.45,  # Relative permittivity for SiO2
        temperature=300,
    )

    # Assume constant carrier concentrations
    n_conc = np.full_like(voltage_iv, 1e16)  # cm^-3
    p_conc = np.full_like(voltage_iv, 1e16)  # cm^-3

    # Calculate current and recombination rate
    current, recombination = mos.iv_characteristic(voltage_iv, n_conc, p_conc)

    # Plot IV characteristics with recombination
    mos.plot_iv_characteristic(voltage_iv, current, recombination)

    # Calculate and plot C-V characteristics
    mos.plot_capacitance_vs_voltage(voltage_cv)


if __name__ == "__main__":
    main()
