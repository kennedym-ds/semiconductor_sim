# semiconductor_sim/models/bandgap.py

import numpy as np

def temperature_dependent_bandgap(T, E_g0=1.12, alpha=4.73e-4, beta=636):
    """
    Calculate the temperature-dependent bandgap energy using the Varshni equation.

    Parameters:
        T (float or np.ndarray): Temperature in Kelvin
        E_g0 (float): Bandgap energy at 0 K (eV)
        alpha (float): Varshni's alpha parameter (eV/K)
        beta (float): Varshni's beta parameter (K)

    Returns:
        E_g (float or np.ndarray): Bandgap energy at temperature T (eV)
    """
    E_g = E_g0 - (alpha * T**2) / (T + beta)
    return E_g
