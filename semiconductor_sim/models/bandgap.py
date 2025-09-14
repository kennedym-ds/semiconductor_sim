# semiconductor_sim/models/bandgap.py

from __future__ import annotations

from typing import overload

import numpy as np
from numpy.typing import NDArray


@overload
def temperature_dependent_bandgap(
    T: float, E_g0: float = ..., alpha: float = ..., beta: float = ...
) -> float: ...


@overload
def temperature_dependent_bandgap(
    T: NDArray[np.floating], E_g0: float = ..., alpha: float = ..., beta: float = ...
) -> NDArray[np.floating]: ...


def temperature_dependent_bandgap(
    T: float | NDArray[np.floating], E_g0: float = 1.12, alpha: float = 4.73e-4, beta: float = 636
) -> float | NDArray[np.floating]:
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
    T_arr = np.asarray(T)
    E_g_arr = E_g0 - (alpha * T_arr**2) / (T_arr + beta)
    if E_g_arr.ndim == 0:
        return float(E_g_arr)
    return E_g_arr
