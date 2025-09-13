# examples/example_zener_diode.py

import numpy as np

from semiconductor_sim import ZenerDiode


def main():
    # Define voltage range
    voltage = np.linspace(-5, 10, 500)

    # Initialize the Zener Diode with doping concentrations, Zener voltage, and temperature
    zener = ZenerDiode(doping_p=1e17, doping_n=1e17, zener_voltage=5.0, temperature=300)

    # Assume constant carrier concentrations
    n_conc = np.full_like(voltage, 1e16)  # cm^-3
    p_conc = np.full_like(voltage, 1e16)  # cm^-3

    # Calculate current and recombination rate
    current, recombination = zener.iv_characteristic(voltage, n_conc, p_conc)

    # Plot IV characteristics with recombination
    zener.plot_iv_characteristic(voltage, current, recombination)


if __name__ == "__main__":
    main()
