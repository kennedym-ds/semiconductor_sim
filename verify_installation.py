# verify_installation.py

import semiconductor_sim
from semiconductor_sim.utils import DEFAULT_T, k_B, q

print(f"Package version: {semiconductor_sim.__version__}")
print(f"Elementary charge (q): {q} C")
print(f"Boltzmann constant (k_B): {k_B} J/K")
print(f"Default Temperature (DEFAULT_T): {DEFAULT_T} K")
