from __future__ import annotations

import numpy as np
import numpy.typing as npt
from typing import Union, cast
import warnings

# Feature flags for acceleration backends
_NUMBA_AVAILABLE = False
_JAX_AVAILABLE = False

# Try to import acceleration backends
try:
    import numba
    from numba import jit
    _NUMBA_AVAILABLE = True
except ImportError:
    pass

try:
    import jax
    import jax.numpy as jnp
    _JAX_AVAILABLE = True
except ImportError:
    pass


def is_numba_available() -> bool:
    """Check if Numba acceleration is available."""
    return _NUMBA_AVAILABLE


def is_jax_available() -> bool:
    """Check if JAX acceleration is available."""
    return _JAX_AVAILABLE


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


# Numba-accelerated version if available
if _NUMBA_AVAILABLE:
    @jit(nopython=True, cache=True)
    def _safe_expm1_numba(x: np.ndarray, max_arg: float = 700.0) -> np.ndarray:
        """Numba-accelerated version of safe_expm1."""
        clipped = np.clip(x, -max_arg, max_arg)
        return np.expm1(clipped)

    def safe_expm1_numba(x: Union[np.ndarray, float], max_arg: float = 700.0) -> npt.NDArray[np.float64]:
        """
        Numba-accelerated version of safe_expm1.
        
        Parameters:
        - x: input value(s)
        - max_arg: maximum absolute argument allowed before clipping
        
        Returns:
        - np.ndarray: exp(x) - 1 computed safely with Numba acceleration
        """
        arr = np.asarray(x, dtype=float)
        out = _safe_expm1_numba(arr, max_arg)
        return cast(npt.NDArray[np.float64], out)
else:
    def safe_expm1_numba(x: Union[np.ndarray, float], max_arg: float = 700.0) -> npt.NDArray[np.float64]:
        """Fallback to standard safe_expm1 when Numba is not available."""
        warnings.warn("Numba not available, falling back to standard implementation", RuntimeWarning)
        return safe_expm1(x, max_arg)


# JAX-accelerated version if available
if _JAX_AVAILABLE:
    @jax.jit
    def _safe_expm1_jax(x: jnp.ndarray, max_arg: float = 700.0) -> jnp.ndarray:
        """JAX-accelerated version of safe_expm1."""
        clipped = jnp.clip(x, -max_arg, max_arg)
        return jnp.expm1(clipped)

    def safe_expm1_jax(x: Union[np.ndarray, float], max_arg: float = 700.0) -> npt.NDArray[np.float64]:
        """
        JAX-accelerated version of safe_expm1.
        
        Parameters:
        - x: input value(s)
        - max_arg: maximum absolute argument allowed before clipping
        
        Returns:
        - np.ndarray: exp(x) - 1 computed safely with JAX acceleration
        """
        arr = jnp.asarray(x, dtype=float)
        out = _safe_expm1_jax(arr, max_arg)
        return cast(npt.NDArray[np.float64], np.asarray(out))
else:
    def safe_expm1_jax(x: Union[np.ndarray, float], max_arg: float = 700.0) -> npt.NDArray[np.float64]:
        """Fallback to standard safe_expm1 when JAX is not available."""
        warnings.warn("JAX not available, falling back to standard implementation", RuntimeWarning)
        return safe_expm1(x, max_arg)


def get_accelerated_expm1(backend: str = "auto") -> callable:
    """
    Get the best available accelerated version of safe_expm1.
    
    Parameters:
    - backend: Acceleration backend ('auto', 'numba', 'jax', 'numpy')
    
    Returns:
    - Callable: The appropriate safe_expm1 function
    """
    if backend == "auto":
        if _NUMBA_AVAILABLE:
            return safe_expm1_numba
        elif _JAX_AVAILABLE:
            return safe_expm1_jax
        else:
            return safe_expm1
    elif backend == "numba":
        if _NUMBA_AVAILABLE:
            return safe_expm1_numba
        else:
            warnings.warn("Numba not available, falling back to numpy", RuntimeWarning)
            return safe_expm1
    elif backend == "jax":
        if _JAX_AVAILABLE:
            return safe_expm1_jax
        else:
            warnings.warn("JAX not available, falling back to numpy", RuntimeWarning)
            return safe_expm1
    elif backend == "numpy":
        return safe_expm1
    else:
        raise ValueError(f"Unknown backend: {backend}. Use 'auto', 'numba', 'jax', or 'numpy'")


# Additional accelerated functions for common IV computations
if _NUMBA_AVAILABLE:
    @jit(nopython=True, cache=True)
    def _diode_current_numba(voltage: np.ndarray, I_s: float, V_T: float, max_arg: float = 700.0) -> np.ndarray:
        """Numba-accelerated diode current calculation."""
        normalized_v = voltage / V_T
        clipped_v = np.clip(normalized_v, -max_arg, max_arg)
        return I_s * np.expm1(clipped_v)

    def diode_current_numba(
        voltage: Union[np.ndarray, float], 
        I_s: float, 
        V_T: float, 
        max_arg: float = 700.0
    ) -> npt.NDArray[np.float64]:
        """
        Numba-accelerated diode current calculation: I = I_s * (exp(V/V_T) - 1).
        
        Parameters:
        - voltage: Applied voltage(s)
        - I_s: Saturation current
        - V_T: Thermal voltage
        - max_arg: Maximum argument for exponential to avoid overflow
        
        Returns:
        - Current array
        """
        v_arr = np.asarray(voltage, dtype=float)
        out = _diode_current_numba(v_arr, I_s, V_T, max_arg)
        return cast(npt.NDArray[np.float64], out)
else:
    def diode_current_numba(
        voltage: Union[np.ndarray, float], 
        I_s: float, 
        V_T: float, 
        max_arg: float = 700.0
    ) -> npt.NDArray[np.float64]:
        """Fallback diode current calculation when Numba is not available."""
        warnings.warn("Numba not available, using standard numpy implementation", RuntimeWarning)
        v_arr = np.asarray(voltage, dtype=float)
        return I_s * safe_expm1(v_arr / V_T, max_arg)


if _JAX_AVAILABLE:
    @jax.jit
    def _diode_current_jax(voltage: jnp.ndarray, I_s: float, V_T: float, max_arg: float = 700.0) -> jnp.ndarray:
        """JAX-accelerated diode current calculation."""
        normalized_v = voltage / V_T
        clipped_v = jnp.clip(normalized_v, -max_arg, max_arg)
        return I_s * jnp.expm1(clipped_v)

    def diode_current_jax(
        voltage: Union[np.ndarray, float], 
        I_s: float, 
        V_T: float, 
        max_arg: float = 700.0
    ) -> npt.NDArray[np.float64]:
        """
        JAX-accelerated diode current calculation: I = I_s * (exp(V/V_T) - 1).
        
        Parameters:
        - voltage: Applied voltage(s)
        - I_s: Saturation current
        - V_T: Thermal voltage
        - max_arg: Maximum argument for exponential to avoid overflow
        
        Returns:
        - Current array
        """
        v_arr = jnp.asarray(voltage, dtype=float)
        out = _diode_current_jax(v_arr, I_s, V_T, max_arg)
        return cast(npt.NDArray[np.float64], np.asarray(out))
else:
    def diode_current_jax(
        voltage: Union[np.ndarray, float], 
        I_s: float, 
        V_T: float, 
        max_arg: float = 700.0
    ) -> npt.NDArray[np.float64]:
        """Fallback diode current calculation when JAX is not available."""
        warnings.warn("JAX not available, using standard numpy implementation", RuntimeWarning)
        v_arr = np.asarray(voltage, dtype=float)
        return I_s * safe_expm1(v_arr / V_T, max_arg)


def get_accelerated_diode_current(backend: str = "auto") -> callable:
    """
    Get the best available accelerated version of diode current calculation.
    
    Parameters:
    - backend: Acceleration backend ('auto', 'numba', 'jax', 'numpy')
    
    Returns:
    - Callable: The appropriate diode current function
    """
    if backend == "auto":
        if _NUMBA_AVAILABLE:
            return diode_current_numba
        elif _JAX_AVAILABLE:
            return diode_current_jax
        else:
            return lambda v, I_s, V_T, max_arg=700.0: I_s * safe_expm1(np.asarray(v) / V_T, max_arg)
    elif backend == "numba":
        return diode_current_numba
    elif backend == "jax":
        return diode_current_jax
    elif backend == "numpy":
        return lambda v, I_s, V_T, max_arg=700.0: I_s * safe_expm1(np.asarray(v) / V_T, max_arg)
    else:
        raise ValueError(f"Unknown backend: {backend}. Use 'auto', 'numba', 'jax', or 'numpy'")
