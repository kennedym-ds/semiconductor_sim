# examples/example_tunnel_diode.py

import numpy as np

from semiconductor_sim import TunnelDiode


def main():
    # Define voltage range
    voltage = np.linspace(-0.5, 0.7, 200)

    # High doping concentrations for Tunnel Diode
    diode = TunnelDiode(doping_p=1e19, doping_n=1e19, temperature=300)

    # Assume constant carrier concentrations
    n_conc = np.full_like(voltage, 1e18)  # cm^-3
    p_conc = np.full_like(voltage, 1e18)  # cm^-3

    # Calculate current and recombination rate
    current, recombination = diode.iv_characteristic(voltage, n_conc, p_conc)

    # Plot IV characteristics with recombination
    diode.plot_iv_characteristic(voltage, current, recombination)


if __name__ == "__main__":
    main()
