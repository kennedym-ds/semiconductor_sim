# semiconductor_sim/models/radiative_recombination.py

import numpy as np
from typing import Union
from semiconductor_sim.utils import DEFAULT_T

def radiative_recombination(
    n: Union[float, np.ndarray],
    p: Union[float, np.ndarray],
    B: float = 1e-10,
    temperature: float = DEFAULT_T,
) -> Union[float, np.ndarray]:
    """Compute the radiative recombination rate.

    Parameters:
    - n: Electron concentration (cm^-3)
    - p: Hole concentration (cm^-3)
    - B: Radiative recombination coefficient (cm^3/s)
    - temperature: Temperature in Kelvin (unused in simplified model)

    Returns:
    - Radiative recombination rate (cm^-3 s^-1)

    Notes:
    - Uses a simplified relation R = B * (n p - n_i^2), with n_i = 1.5e10 cm^-3.
    - Clamps negative values to zero for physical plausibility.
    """
    ni_sq = (1.5e10) ** 2
    R = B * (n * p - ni_sq)
    if isinstance(R, np.ndarray):
        return np.maximum(R, 0)
    return max(R, 0.0)
