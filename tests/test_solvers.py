"""Tests for numerical solvers utilities."""

import pytest
import numpy as np
from semiconductor_sim.utils.solvers import (
    robust_brentq,
    robust_newton,
    find_voltage_for_current,
    find_operating_point,
)


class TestRobustBrentq:
    """Test cases for robust Brent's method."""
    
    def test_simple_root(self):
        """Test finding root of a simple function."""
        def f(x):
            return x**2 - 4  # Root at x = 2
        
        root = robust_brentq(f, 0, 5)
        assert abs(root - 2.0) < 1e-10
        
    def test_linear_function(self):
        """Test finding root of a linear function."""
        def f(x):
            return 2*x - 6  # Root at x = 3
        
        root = robust_brentq(f, 0, 10)
        assert abs(root - 3.0) < 1e-10
        
    def test_with_arguments(self):
        """Test function with additional arguments."""
        def f(x, a, b):
            return a*x + b  # Root at x = -b/a
        
        root = robust_brentq(f, -10, 10, args=(2, -6))  # Root at x = 3
        assert abs(root - 3.0) < 1e-10
        
    def test_same_sign_endpoints(self):
        """Test error handling when endpoints have same sign."""
        def f(x):
            return x**2 + 1  # No real roots
        
        with pytest.raises(RuntimeError, match="Root finding failed"):
            robust_brentq(f, 0, 1)
            
    def test_transcendental_function(self):
        """Test with a transcendental function like those in semiconductor equations."""
        def f(x):
            return np.exp(x) - x - 2  # Transcendental equation
        
        root = robust_brentq(f, 0, 2)
        # Verify the root is correct
        assert abs(f(root)) < 1e-10


class TestRobustNewton:
    """Test cases for robust Newton's method."""
    
    def test_simple_root_with_derivative(self):
        """Test Newton's method with derivative provided."""
        def f(x):
            return x**2 - 4
        
        def fprime(x):
            return 2*x
        
        root = robust_newton(f, 1.5, fprime=fprime)
        assert abs(root - 2.0) < 1e-10
        
    def test_simple_root_without_derivative(self):
        """Test secant method (no derivative)."""
        def f(x):
            return x**2 - 4
        
        root = robust_newton(f, 1.5)  # No derivative provided
        assert abs(root - 2.0) < 1e-8
        
    def test_with_arguments(self):
        """Test function with additional arguments."""
        def f(x, a):
            return x**2 - a
        
        def fprime(x, a):
            return 2*x
        
        root = robust_newton(f, 1.5, fprime=fprime, args=(9,))  # Root at x = 3
        assert abs(root - 3.0) < 1e-10
        
    def test_fallback_to_secant(self):
        """Test fallback to secant method when Newton fails."""
        def f(x):
            return x**3 - 2*x - 5
        
        def bad_fprime(x):
            # Intentionally bad derivative to force fallback
            if x > 1.5:
                raise RuntimeError("Bad derivative")
            return 3*x**2 - 2
        
        # This should trigger fallback to secant method
        with pytest.warns(RuntimeWarning, match="Newton's method failed"):
            root = robust_newton(f, 2.0, fprime=bad_fprime)
            # Verify we still get a valid root
            assert abs(f(root)) < 1e-6


class TestFindVoltageForCurrent:
    """Test cases for finding voltage for target current."""
    
    def test_diode_like_function(self):
        """Test with a diode-like IV characteristic."""
        def iv_func(v):
            # Simple diode equation: I = I_s * (exp(V/V_T) - 1)
            I_s = 1e-12
            V_T = 0.026
            return I_s * (np.exp(v / V_T) - 1)
        
        target_current = 1e-6
        voltage = find_voltage_for_current(iv_func, target_current, voltage_range=(0, 1))
        
        # Verify the result
        computed_current = iv_func(voltage)
        assert abs(computed_current - target_current) < 1e-12
        
    def test_linear_function(self):
        """Test with a linear IV characteristic (resistor)."""
        def iv_func(v):
            R = 1000  # 1k ohm resistor
            return v / R
        
        target_current = 0.005  # 5 mA
        voltage = find_voltage_for_current(iv_func, target_current, voltage_range=(0, 10))
        
        expected_voltage = target_current * 1000  # V = I * R
        assert abs(voltage - expected_voltage) < 1e-10
        
    def test_newton_method(self):
        """Test using Newton's method."""
        def iv_func(v):
            return v**2 - 4  # I = V^2 - 4
        
        target_current = 5  # Root at V = 3
        voltage = find_voltage_for_current(
            iv_func, target_current, voltage_range=(0, 5), method="newton"
        )
        
        assert abs(voltage - 3.0) < 1e-8
        
    def test_invalid_method(self):
        """Test error handling for invalid method."""
        def iv_func(v):
            return v
        
        with pytest.raises(ValueError, match="Unsupported method"):
            find_voltage_for_current(iv_func, 1.0, method="invalid")
            
    def test_invalid_voltage_range(self):
        """Test error handling for invalid voltage range."""
        def iv_func(v):
            return v
        
        with pytest.raises(ValueError, match="voltage_range must be"):
            find_voltage_for_current(iv_func, 1.0, voltage_range=(2, 1))


class TestFindOperatingPoint:
    """Test cases for finding operating point."""
    
    def test_diode_with_resistor(self):
        """Test finding operating point of diode with series resistor."""
        # Diode IV characteristic
        def diode_iv(v):
            I_s = 1e-12
            V_T = 0.026
            if v < 0:
                return -I_s  # Reverse saturation current
            return I_s * (np.exp(v / V_T) - 1)
        
        # Load line: I = (V_supply - V_diode) / R
        V_supply = 5.0
        R = 1000
        def load_line(v):
            return (V_supply - v) / R
        
        v_op, i_op = find_operating_point(diode_iv, load_line, voltage_range=(0, 5))
        
        # Verify operating point
        assert abs(diode_iv(v_op) - i_op) < 1e-10
        assert abs(load_line(v_op) - i_op) < 1e-10
        
        # Check that we get a reasonable operating point
        assert 0 < v_op < V_supply
        assert i_op > 0
        
    def test_linear_intersection(self):
        """Test intersection of two linear functions."""
        def line1(v):
            return 2 * v + 1  # I = 2V + 1
        
        def line2(v):
            return -v + 4  # I = -V + 4
        
        # Analytical solution: 2V + 1 = -V + 4 => 3V = 3 => V = 1, I = 3
        v_op, i_op = find_operating_point(line1, line2, voltage_range=(0, 5))
        
        assert abs(v_op - 1.0) < 1e-10
        assert abs(i_op - 3.0) < 1e-10
        
    def test_newton_method(self):
        """Test using Newton's method for operating point."""
        def iv1(v):
            return v**2
        
        def iv2(v):
            return 4 * v
        
        # Intersection at V = 4, I = 16
        v_op, i_op = find_operating_point(iv1, iv2, voltage_range=(0, 10), method="newton")
        
        assert abs(v_op - 4.0) < 1e-8
        assert abs(i_op - 16.0) < 1e-8
        
    def test_invalid_method(self):
        """Test error handling for invalid method."""
        def iv1(v):
            return v
        
        def iv2(v):
            return 2 - v
        
        with pytest.raises(ValueError, match="Unsupported method"):
            find_operating_point(iv1, iv2, method="invalid")
            
    def test_invalid_voltage_range(self):
        """Test error handling for invalid voltage range."""
        def iv1(v):
            return v
        
        def iv2(v):
            return 2 - v
        
        with pytest.raises(ValueError, match="voltage_range must be"):
            find_operating_point(iv1, iv2, voltage_range=(2, 1))


def test_solver_integration_with_realistic_semiconductor():
    """Integration test with realistic semiconductor device parameters."""
    # Realistic PN junction parameters
    I_s = 1e-14  # Saturation current (A)
    V_T = 0.026  # Thermal voltage at room temperature (V)
    n = 1.0  # Ideality factor
    
    def pn_junction_current(v):
        """Realistic PN junction IV characteristic."""
        if v < -5 * V_T:
            return -I_s  # Reverse saturation
        return I_s * (np.exp(v / (n * V_T)) - 1)
    
    # Test finding voltage for specific current
    target_current = 1e-6  # 1 μA
    voltage = find_voltage_for_current(
        pn_junction_current, target_current, voltage_range=(0, 1)
    )
    
    # Should be around 0.36V for typical silicon diode
    assert 0.3 < voltage < 0.5
    assert abs(pn_junction_current(voltage) - target_current) < 1e-12
    
    # Test operating point with realistic load
    V_supply = 3.3  # 3.3V supply
    R_load = 3300   # 3.3k ohm load resistor
    
    def load_line(v):
        return (V_supply - v) / R_load
    
    v_op, i_op = find_operating_point(
        pn_junction_current, load_line, voltage_range=(0, V_supply)
    )
    
    # Verify the operating point makes sense
    assert 0.6 < v_op < 0.8  # Typical forward voltage
    assert 0.7e-3 < i_op < 0.9e-3  # Reasonable current level
    assert abs(pn_junction_current(v_op) - load_line(v_op)) < 1e-12