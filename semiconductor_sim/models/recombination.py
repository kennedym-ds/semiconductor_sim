"""Recombination models."""

import numpy as np
import numpy.typing as npt

from semiconductor_sim.utils import DEFAULT_T


def srh_recombination(
    n: float | npt.NDArray[np.floating],
    p: float | npt.NDArray[np.floating],
    temperature: float = float(DEFAULT_T),
    tau_n: float = 1e-6,
    tau_p: float = 1e-6,
    n1: float | None = None,
    p1: float | None = None,
) -> float | npt.NDArray[np.floating]:
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

    n_arr = np.asarray(n, dtype=float)
    p_arr = np.asarray(p, dtype=float)

    denominator = tau_p * (n_arr + n1_val) + tau_n * (p_arr + p1_val)
    R_SRH = (n_arr * p_arr - n_i**2) / denominator

    if np.isscalar(n) and np.isscalar(p):
        return float(np.asarray(R_SRH).item())
    return np.asarray(R_SRH, dtype=float)
