# examples/example_pn_junction.py

import numpy as np
from semiconductor_sim import PNJunctionDiode


def main() -> None:
	# Define voltage range
	voltage = np.linspace(-0.5, 0.7, 200)

	# Initialize the diode with doping concentrations and temperature
	diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)

	# Assume constant carrier concentrations for simplicity
	n_conc = np.full_like(voltage, 1e16)  # cm^-3
	p_conc = np.full_like(voltage, 1e16)  # cm^-3

	# Calculate current and recombination rate
	current, recombination = diode.iv_characteristic(voltage, n_conc, p_conc)

	# Plot IV characteristics with recombination
	diode.plot_iv_characteristic(voltage, current, recombination)


if __name__ == "__main__":
	main()
