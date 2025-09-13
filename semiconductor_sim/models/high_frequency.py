# semiconductor_sim/models/high_frequency.py

import numpy as np


def high_frequency_capacitance(C_dc, f, R=1000):
    """
    Calculate the high-frequency capacitance using the voltage-dependent capacitance.

    Parameters:
        C_dc (float or np.ndarray): DC capacitance (F)
        f (float): Frequency (Hz)
        R (float): Resistance (Ohms), default 1000 Ohms

    Returns:
        C_ac (float or np.ndarray): AC capacitance (F)
    """
    omega = 2 * np.pi * f
    C_ac = C_dc / np.sqrt(1 + (omega * R * C_dc) ** 2)
    return C_ac
