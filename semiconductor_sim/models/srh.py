from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def srh_rate(
    n: float | NDArray[np.floating],
    p: float | NDArray[np.floating],
    n_i: float,
    tau_n: float,
    tau_p: float,
) -> NDArray[np.floating] | float:
    n_arr = np.asarray(n, dtype=float)
    p_arr = np.asarray(p, dtype=float)
    denom = tau_p * (n_arr + n_i) + tau_n * (p_arr + n_i)
    # Recombination rate R = (np - n_i^2) / denom
    R = (n_arr * p_arr - n_i**2) / denom
    return R if isinstance(n, np.ndarray) or isinstance(p, np.ndarray) else float(R)
