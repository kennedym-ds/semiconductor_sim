#!/usr/bin/env python3
"""
Demonstration of acceleration features and solver utilities.

This script demonstrates the new acceleration backends and robust solvers
added to the semiconductor simulation library.
"""

import numpy as np
import time
from semiconductor_sim.devices.pn_junction import PNJunctionDiode
from semiconductor_sim.utils.numerics import (
    safe_expm1,
    get_accelerated_expm1,
    get_accelerated_diode_current,
    is_numba_available,
    is_jax_available,
)
from semiconductor_sim.utils.solvers import (
    find_voltage_for_current,
    find_operating_point,
)


def demo_acceleration_detection():
    """Demonstrate acceleration backend detection."""
    print("=== Acceleration Backend Detection ===")
    print(f"Numba available: {is_numba_available()}")
    print(f"JAX available: {is_jax_available()}")
    print()


def demo_numerical_consistency():
    """Demonstrate that accelerated versions give identical results."""
    print("=== Numerical Consistency Check ===")
    
    # Test data
    voltage = np.linspace(-1, 1, 1000)
    I_s = 1e-14
    V_T = 0.026
    
    # Get different implementations
    expm1_numpy = get_accelerated_expm1("numpy")
    expm1_auto = get_accelerated_expm1("auto")
    
    diode_numpy = get_accelerated_diode_current("numpy")
    diode_auto = get_accelerated_diode_current("auto")
    
    # Test expm1 consistency
    result_numpy = expm1_numpy(voltage / V_T)
    result_auto = expm1_auto(voltage / V_T)
    
    max_diff = np.max(np.abs(result_numpy - result_auto))
    print(f"Max difference in expm1 results: {max_diff:.2e}")
    
    # Test diode current consistency
    current_numpy = diode_numpy(voltage, I_s, V_T)
    current_auto = diode_auto(voltage, I_s, V_T)
    
    max_diff = np.max(np.abs(current_numpy - current_auto))
    print(f"Max difference in diode current results: {max_diff:.2e}")
    print()


def demo_performance_comparison():
    """Demonstrate performance differences between backends."""
    print("=== Performance Comparison ===")
    
    # Large array for timing
    voltage = np.linspace(-2, 2, 100000)
    I_s = 1e-14
    V_T = 0.026
    
    # Get implementations
    expm1_numpy = get_accelerated_expm1("numpy")
    expm1_auto = get_accelerated_expm1("auto")
    
    # Time expm1 computation
    start_time = time.time()
    for _ in range(10):
        result_numpy = expm1_numpy(voltage / V_T)
    numpy_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(10):
        result_auto = expm1_auto(voltage / V_T)
    auto_time = time.time() - start_time
    
    print(f"NumPy expm1 time (10 runs): {numpy_time:.4f}s")
    print(f"Auto expm1 time (10 runs): {auto_time:.4f}s")
    if auto_time > 0:
        speedup = numpy_time / auto_time
        print(f"Speedup: {speedup:.2f}x")
    print()


def demo_solver_utilities():
    """Demonstrate the robust solver utilities."""
    print("=== Robust Solver Demonstration ===")
    
    # Create a realistic PN junction
    diode = PNJunctionDiode(
        doping_p=1e16,
        doping_n=1e16,
        area=1e-4,
        temperature=300
    )
    
    # Define IV characteristic function
    def iv_func(v):
        current, _ = diode.iv_characteristic(np.array([v]))
        return current[0]
    
    # Find voltage for target current
    target_current = 1e-6  # 1 μA
    voltage = find_voltage_for_current(iv_func, target_current, voltage_range=(0, 1))
    print(f"Voltage for {target_current:.2e}A current: {voltage:.4f}V")
    
    # Verify the result
    actual_current = iv_func(voltage)
    print(f"Verification - actual current: {actual_current:.2e}A")
    print(f"Error: {abs(actual_current - target_current):.2e}A")
    
    # Demonstrate operating point calculation
    V_supply = 3.3  # 3.3V supply
    R_load = 3300   # 3.3k ohm load
    
    def load_line(v):
        return (V_supply - v) / R_load
    
    v_op, i_op = find_operating_point(iv_func, load_line, voltage_range=(0, V_supply))
    print(f"\nOperating point: V = {v_op:.4f}V, I = {i_op:.2e}A")
    
    # Verify operating point
    diode_current = iv_func(v_op)
    load_current = load_line(v_op)
    print(f"Verification - diode current: {diode_current:.2e}A")
    print(f"Verification - load current: {load_current:.2e}A")
    print(f"Difference: {abs(diode_current - load_current):.2e}A")
    print()


def demo_device_iv_calculation():
    """Demonstrate accelerated IV calculation for semiconductor devices."""
    print("=== Device IV Calculation Demo ===")
    
    # Create a PN junction diode
    diode = PNJunctionDiode(
        doping_p=1e16,
        doping_n=1e16,
        area=1e-4,
        temperature=300
    )
    
    # Create voltage array
    voltage = np.linspace(-0.5, 1.0, 1000)
    
    # Calculate IV characteristic
    start_time = time.time()
    current, recombination = diode.iv_characteristic(voltage)
    calc_time = time.time() - start_time
    
    print(f"IV calculation for {len(voltage)} points: {calc_time:.4f}s")
    print(f"Forward voltage at 1mA: {voltage[np.argmin(np.abs(current - 1e-3))]:.4f}V")
    print(f"Reverse saturation current: {current[0]:.2e}A")
    print()


def main():
    """Run all demonstrations."""
    print("Semiconductor Simulation Library - Acceleration & Solver Demo")
    print("=" * 60)
    print()
    
    demo_acceleration_detection()
    demo_numerical_consistency()
    demo_performance_comparison()
    demo_solver_utilities()
    demo_device_iv_calculation()
    
    print("Demo completed successfully!")


if __name__ == "__main__":
    main()