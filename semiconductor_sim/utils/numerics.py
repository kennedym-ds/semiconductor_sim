from __future__ import annotations

import numpy as np
import numpy.typing as npt
from typing import Union, cast

def safe_expm1(x: Union[np.ndarray, float], max_arg: float = 700.0) -> npt.NDArray[np.float64]:
    """
    Compute exp(x) - 1 safely for arrays or scalars by clipping the argument to
    avoid overflow and using numpy.expm1 for better precision near zero.

    Parameters:
    - x: input value(s)
    - max_arg: maximum absolute argument allowed before clipping (float64 ~709)

    Returns:
    - np.ndarray: exp(x) - 1 computed safely
    """
    arr = np.asarray(x, dtype=float)
    clipped = np.clip(arr, -max_arg, max_arg)
    out = np.expm1(clipped)
    return cast(npt.NDArray[np.float64], out)
