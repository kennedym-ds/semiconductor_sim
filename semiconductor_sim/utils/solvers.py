"""Robust numerical solvers for implicit relations in semiconductor devices.

This module provides robust root-finding utilities for solving implicit equations
commonly encountered in semiconductor device modeling, such as finding operating points
and solving transcendental equations.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
from typing import Callable, Optional, Tuple, Union
from scipy.optimize import brentq, newton
import warnings


def robust_brentq(
    func: Callable[[float], float],
    a: float,
    b: float,
    args: tuple = (),
    xtol: float = 1e-12,
    rtol: float = 1e-12,
    maxiter: int = 100,
) -> float:
    """
    Robust Brent's method for root finding with better error handling.
    
    This is a wrapper around scipy.optimize.brentq with improved error handling
    and sensible defaults for semiconductor device equations.
    
    Parameters:
        func: Function for which the root is sought. Should accept a scalar and return a scalar.
        a: One end of the bracketing interval [a, b]
        b: The other end of the bracketing interval [a, b]
        args: Extra arguments to pass to func
        xtol: Absolute tolerance for convergence
        rtol: Relative tolerance for convergence  
        maxiter: Maximum number of iterations
        
    Returns:
        Root of the function
        
    Raises:
        ValueError: If the function values at the endpoints don't have opposite signs
        RuntimeError: If convergence fails
    """
    try:
        # Check that the function values at endpoints have opposite signs
        fa = func(a, *args)
        fb = func(b, *args)
        
        if fa * fb > 0:
            raise ValueError(
                f"Function values at endpoints must have opposite signs. "
                f"f({a}) = {fa}, f({b}) = {fb}"
            )
        
        root = brentq(func, a, b, args=args, xtol=xtol, rtol=rtol, maxiter=maxiter)
        return float(root)
        
    except Exception as e:
        raise RuntimeError(f"Root finding failed: {e}") from e


def robust_newton(
    func: Callable[[float], float],
    x0: float,
    fprime: Optional[Callable[[float], float]] = None,
    args: tuple = (),
    tol: float = 1.48e-8,
    maxiter: int = 50,
    fprime2: Optional[Callable[[float], float]] = None,
) -> float:
    """
    Robust Newton-Raphson method with fallback to secant method.
    
    This is a wrapper around scipy.optimize.newton with improved error handling
    and automatic fallback when derivative is not provided or fails.
    
    Parameters:
        func: Function for which the root is sought
        x0: Initial guess for the root
        fprime: Derivative of func. If None, secant method is used
        args: Extra arguments to pass to func and fprime
        tol: Tolerance for convergence
        maxiter: Maximum number of iterations
        fprime2: Second derivative (for Halley's method, not implemented here)
        
    Returns:
        Root of the function
        
    Raises:
        RuntimeError: If convergence fails
    """
    try:
        # Use Newton's method if derivative is provided, otherwise secant method
        root = newton(
            func, x0, fprime=fprime, args=args, tol=tol, maxiter=maxiter, fprime2=fprime2
        )
        return float(root)
        
    except Exception as e:
        # If Newton's method fails and we have a derivative, try secant method
        if fprime is not None:
            try:
                warnings.warn(
                    f"Newton's method failed ({e}), falling back to secant method",
                    RuntimeWarning
                )
                root = newton(func, x0, fprime=None, args=args, tol=tol, maxiter=maxiter)
                return float(root)
            except Exception as e2:
                raise RuntimeError(f"Both Newton's and secant methods failed: {e2}") from e2
        else:
            raise RuntimeError(f"Root finding failed: {e}") from e


def find_voltage_for_current(
    iv_func: Callable[[float], float],
    target_current: float,
    voltage_range: Tuple[float, float] = (-2.0, 2.0),
    method: str = "brentq",
    **kwargs
) -> float:
    """
    Find the voltage that produces a target current in an IV characteristic.
    
    This is a convenience function for solving the common problem of finding
    the voltage V such that I(V) = I_target.
    
    Parameters:
        iv_func: Function that computes current given voltage I = f(V)
        target_current: Desired current value
        voltage_range: Search range for voltage as (v_min, v_max)
        method: Root finding method ('brentq' or 'newton')
        **kwargs: Additional arguments passed to the root finding method
        
    Returns:
        Voltage that produces the target current
        
    Raises:
        ValueError: If method is not supported or voltage range is invalid
        RuntimeError: If root finding fails
    """
    if voltage_range[0] >= voltage_range[1]:
        raise ValueError("voltage_range must be (v_min, v_max) with v_min < v_max")
    
    # Define the function whose root we want to find: I(V) - I_target = 0
    def objective(v: float) -> float:
        return iv_func(v) - target_current
    
    if method == "brentq":
        return robust_brentq(objective, voltage_range[0], voltage_range[1], **kwargs)
    elif method == "newton":
        # Use midpoint as initial guess for Newton's method
        x0 = kwargs.pop("x0", (voltage_range[0] + voltage_range[1]) / 2)
        return robust_newton(objective, x0, **kwargs)
    else:
        raise ValueError(f"Unsupported method: {method}. Use 'brentq' or 'newton'")


def find_operating_point(
    iv_func: Callable[[float], float],
    load_line: Callable[[float], float],
    voltage_range: Tuple[float, float] = (-2.0, 2.0),
    method: str = "brentq",
    **kwargs
) -> Tuple[float, float]:
    """
    Find the operating point (intersection) of an IV curve with a load line.
    
    Solves for the voltage V where I_device(V) = I_load(V), which gives
    the DC operating point of a device with a resistive load.
    
    Parameters:
        iv_func: Device IV characteristic function I = f(V)
        load_line: Load line function I = g(V) 
        voltage_range: Search range for voltage as (v_min, v_max)
        method: Root finding method ('brentq' or 'newton')
        **kwargs: Additional arguments passed to the root finding method
        
    Returns:
        Tuple of (voltage, current) at the operating point
        
    Raises:
        ValueError: If method is not supported or voltage range is invalid
        RuntimeError: If root finding fails
    """
    if voltage_range[0] >= voltage_range[1]:
        raise ValueError("voltage_range must be (v_min, v_max) with v_min < v_max")
    
    # Define the function whose root we want to find: I_device(V) - I_load(V) = 0
    def objective(v: float) -> float:
        return iv_func(v) - load_line(v)
    
    if method == "brentq":
        v_op = robust_brentq(objective, voltage_range[0], voltage_range[1], **kwargs)
    elif method == "newton":
        # Use midpoint as initial guess for Newton's method
        x0 = kwargs.pop("x0", (voltage_range[0] + voltage_range[1]) / 2)
        v_op = robust_newton(objective, x0, **kwargs)
    else:
        raise ValueError(f"Unsupported method: {method}. Use 'brentq' or 'newton'")
    
    # Calculate the current at the operating point
    i_op = iv_func(v_op)
    
    return float(v_op), float(i_op)