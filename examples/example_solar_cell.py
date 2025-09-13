# examples/example_solar_cell.py

import numpy as np

from semiconductor_sim import SolarCell


def main() -> None:
    # Define voltage range
    voltage = np.linspace(0, 0.8, 200)

    # Initialize the solar cell with doping concentrations, light intensity, and temperature
    solar = SolarCell(doping_p=1e17, doping_n=1e17, light_intensity=1.0, temperature=300)

    # Calculate current
    (current,) = solar.iv_characteristic(voltage)

    # Plot IV characteristics
    solar.plot_iv_characteristic(voltage, current)


if __name__ == "__main__":
    main()
