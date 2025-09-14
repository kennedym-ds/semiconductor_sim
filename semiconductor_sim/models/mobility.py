from __future__ import annotations

from typing import Final

import numpy as np
from numpy.typing import NDArray


def _ct_model(
    N: float | NDArray[np.floating],
    mu_min: float,
    mu_0: float,
    N_ref: float,
    alpha: float,
    T: float | None = None,
    T_ref: float = 300.0,
    temp_exp: float = 0.0,
) -> float | NDArray[np.floating]:
    N_arr = np.asarray(N, dtype=float)
    mu = mu_min + (mu_0 - mu_min) / (1.0 + (N_arr / N_ref) ** alpha)
    if T is not None and temp_exp != 0.0:
        mu = mu * (np.asarray(T, dtype=float) / T_ref) ** (-temp_exp)
    return mu if isinstance(N, np.ndarray) else float(mu)


# Teaching-simple default parameters for Silicon (approximate, typical values)
_SI_ELECTRON: Final = dict(mu_min=92.0, mu_0=1414.0, N_ref=1.3e17, alpha=0.91)
_SI_HOLE: Final = dict(mu_min=54.3, mu_0=470.0, N_ref=2.35e17, alpha=0.88)


def mu_n(
    doping_cm3: float | NDArray[np.floating],
    T: float | None = None,
    material: str = "Si",
) -> float | NDArray[np.floating]:
    if material != "Si":
        # For now, reuse Si as a placeholder for other materials.
        pass
    return _ct_model(doping_cm3, **_SI_ELECTRON, T=T, temp_exp=0.5)


def mu_p(
    doping_cm3: float | NDArray[np.floating],
    T: float | None = None,
    material: str = "Si",
) -> float | NDArray[np.floating]:
    if material != "Si":
        pass
    return _ct_model(doping_cm3, **_SI_HOLE, T=T, temp_exp=0.7)
