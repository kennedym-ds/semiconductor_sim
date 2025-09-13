"""Recombination models."""

from typing import Union, Optional

import numpy as np
from semiconductor_sim.utils import DEFAULT_T


def srh_recombination(
    n: Union[float, np.ndarray],
    p: Union[float, np.ndarray],
    temperature: float = float(DEFAULT_T),
    tau_n: float = 1e-6,
    tau_p: float = 1e-6,
    n1: Optional[float] = None,
    p1: Optional[float] = None,
) -> Union[float, np.ndarray]:
    """
    Calculate the Shockley-Read-Hall (SRH) recombination rate.

    Parameters:
        n: Electron concentration (cm^-3)
        p: Hole concentration (cm^-3)
        temperature: Temperature in Kelvin
        tau_n: Electron lifetime (s)
        tau_p: Hole lifetime (s)

    Returns:
        SRH recombination rate (cm^-3 s^-1).

    Notes:
        Uses a simplified SRH form assuming mid-gap trap with n1 ≈ p1 ≈ n_i by default.
        Advanced users can override `n1` and `p1` to relax this assumption.
    """
    n_i = 1.5e10 * (temperature / float(DEFAULT_T)) ** 1.5
    n1_val = n_i if n1 is None else n1
    p1_val = n_i if p1 is None else p1
    denominator = tau_p * (n + n1_val) + tau_n * (p + p1_val)
    R_SRH = (n * p - n_i**2) / denominator
    return R_SRH
