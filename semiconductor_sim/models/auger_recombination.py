# semiconductor_sim/models/auger_recombination.py

import numpy as np
from semiconductor_sim.utils import q, k_B, DEFAULT_T

def auger_recombination(n, p, C=1e-31, temperature=DEFAULT_T):
    """
    Calculate the Auger Recombination rate.
    
    Parameters:
        n (float or np.ndarray): Electron concentration (cm^-3)
        p (float or np.ndarray): Hole concentration (cm^-3)
        C (float): Auger recombination coefficient (cm^6/s)
        temperature (float): Temperature in Kelvin
    
    Returns:
        R_auger (float or np.ndarray): Auger recombination rate (cm^-3 s^-1)
    """
    R_auger = C * (n**2 * p + p**2 * n)
    return R_auger
