# semiconductor_sim/models/auger_recombination.py

import numpy as np
import numpy.typing as npt

from semiconductor_sim.utils import DEFAULT_T


def auger_recombination(
    n: float | npt.NDArray[np.floating],
    p: float | npt.NDArray[np.floating],
    C: float = 1e-31,
    temperature: float = DEFAULT_T,
) -> float | npt.NDArray[np.floating]:
    """
    Calculate the Auger Recombination rate.

    Parameters:
    n (float or array): Electron concentration (cm^-3)
    p (float or array): Hole concentration (cm^-3)
        C (float): Auger recombination coefficient (cm^6/s)
        temperature (float): Temperature in Kelvin

    Returns:
        R_auger (float or array): Auger recombination rate (cm^-3 s^-1)
    """
    R_auger = C * (n**2 * p + p**2 * n)
    return R_auger
