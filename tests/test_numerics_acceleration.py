"""Tests for acceleration features in numerics module."""

import pytest
import numpy as np
import warnings
from semiconductor_sim.utils.numerics import (
    safe_expm1,
    safe_expm1_numba,
    safe_expm1_jax,
    diode_current_numba,
    diode_current_jax,
    get_accelerated_expm1,
    get_accelerated_diode_current,
    is_numba_available,
    is_jax_available,
)


class TestAccelerationDetection:
    """Test acceleration backend detection."""
    
    def test_feature_flags(self):
        """Test that feature detection functions work."""
        # These should not raise errors regardless of what's installed
        numba_flag = is_numba_available()
        jax_flag = is_jax_available()
        
        assert isinstance(numba_flag, bool)
        assert isinstance(jax_flag, bool)


class TestSafeExpm1Variants:
    """Test different variants of safe_expm1."""
    
    def test_baseline_safe_expm1(self):
        """Test the baseline numpy implementation."""
        x = np.array([0, 1, -1, 10, -10])
        result = safe_expm1(x)
        
        # Compare with numpy.expm1 for reasonable values
        expected = np.expm1(x)
        np.testing.assert_allclose(result, expected, rtol=1e-14)
        
    def test_safe_expm1_clipping(self):
        """Test that large values are clipped properly."""
        x = np.array([800, -800])  # Values that would overflow/underflow
        result = safe_expm1(x, max_arg=700)
        
        # Should not contain inf or -inf
        assert np.all(np.isfinite(result))
        
    def test_numba_variant_equivalence(self):
        """Test that Numba variant gives same results as baseline."""
        x = np.array([0, 0.1, 1, -1, 10, -10, 100])
        
        baseline = safe_expm1(x)
        
        if is_numba_available():
            numba_result = safe_expm1_numba(x)
            np.testing.assert_allclose(numba_result, baseline, rtol=1e-14)
        else:
            # Should warn and fall back
            with pytest.warns(RuntimeWarning, match="Numba not available"):
                numba_result = safe_expm1_numba(x)
            np.testing.assert_allclose(numba_result, baseline, rtol=1e-14)
            
    def test_jax_variant_equivalence(self):
        """Test that JAX variant gives same results as baseline."""
        x = np.array([0, 0.1, 1, -1, 10, -10, 100])
        
        baseline = safe_expm1(x)
        
        if is_jax_available():
            jax_result = safe_expm1_jax(x)
            np.testing.assert_allclose(jax_result, baseline, rtol=1e-14)
        else:
            # Should warn and fall back
            with pytest.warns(RuntimeWarning, match="JAX not available"):
                jax_result = safe_expm1_jax(x)
            np.testing.assert_allclose(jax_result, baseline, rtol=1e-14)
            
    def test_scalar_input(self):
        """Test that scalar inputs work for all variants."""
        x = 1.5
        
        baseline = safe_expm1(x)
        
        # Test Numba variant
        numba_result = safe_expm1_numba(x)
        assert abs(numba_result - baseline) < 1e-14
        
        # Test JAX variant  
        jax_result = safe_expm1_jax(x)
        assert abs(jax_result - baseline) < 1e-14


class TestDiodeCurrentAcceleration:
    """Test accelerated diode current calculations."""
    
    def test_diode_current_baseline(self):
        """Test baseline diode current calculation."""
        voltage = np.array([0, 0.1, 0.5, 0.7, 1.0])
        I_s = 1e-12
        V_T = 0.026
        
        # Manual calculation for comparison
        expected = I_s * safe_expm1(voltage / V_T)
        
        # Test accelerated versions
        if is_numba_available():
            numba_result = diode_current_numba(voltage, I_s, V_T)
            np.testing.assert_allclose(numba_result, expected, rtol=1e-14)
        else:
            with pytest.warns(RuntimeWarning, match="Numba not available"):
                numba_result = diode_current_numba(voltage, I_s, V_T)
            np.testing.assert_allclose(numba_result, expected, rtol=1e-14)
            
        if is_jax_available():
            jax_result = diode_current_jax(voltage, I_s, V_T)
            np.testing.assert_allclose(jax_result, expected, rtol=1e-14)
        else:
            with pytest.warns(RuntimeWarning, match="JAX not available"):
                jax_result = diode_current_jax(voltage, I_s, V_T)
            np.testing.assert_allclose(jax_result, expected, rtol=1e-14)
            
    def test_diode_current_scalar(self):
        """Test diode current calculation with scalar input."""
        voltage = 0.7
        I_s = 1e-12
        V_T = 0.026
        
        expected = I_s * safe_expm1(voltage / V_T)
        
        numba_result = diode_current_numba(voltage, I_s, V_T)
        jax_result = diode_current_jax(voltage, I_s, V_T)
        
        assert abs(numba_result - expected) < 1e-14
        assert abs(jax_result - expected) < 1e-14
        
    def test_diode_current_large_voltages(self):
        """Test diode current with large voltages (clipping)."""
        voltage = np.array([10, 20, -10, -20])
        I_s = 1e-12
        V_T = 0.026
        
        # Should not overflow
        numba_result = diode_current_numba(voltage, I_s, V_T)
        jax_result = diode_current_jax(voltage, I_s, V_T)
        
        assert np.all(np.isfinite(numba_result))
        assert np.all(np.isfinite(jax_result))


class TestAcceleratedFunctionGetters:
    """Test functions that return the best available accelerated version."""
    
    def test_get_accelerated_expm1_auto(self):
        """Test automatic selection of best expm1 function."""
        func = get_accelerated_expm1("auto")
        
        # Should return a callable
        assert callable(func)
        
        # Should work correctly
        x = np.array([0, 1, -1])
        result = func(x)
        expected = safe_expm1(x)
        np.testing.assert_allclose(result, expected, rtol=1e-14)
        
    def test_get_accelerated_expm1_specific_backends(self):
        """Test selection of specific backends."""
        backends = ["numpy", "numba", "jax"]
        
        for backend in backends:
            func = get_accelerated_expm1(backend)
            assert callable(func)
            
            x = np.array([0, 1, -1])
            result = func(x)
            expected = safe_expm1(x)
            np.testing.assert_allclose(result, expected, rtol=1e-14)
            
    def test_get_accelerated_expm1_invalid_backend(self):
        """Test error handling for invalid backend."""
        with pytest.raises(ValueError, match="Unknown backend"):
            get_accelerated_expm1("invalid")
            
    def test_get_accelerated_diode_current_auto(self):
        """Test automatic selection of best diode current function."""
        func = get_accelerated_diode_current("auto")
        
        # Should return a callable
        assert callable(func)
        
        # Should work correctly
        voltage = np.array([0, 0.5, 1.0])
        I_s = 1e-12
        V_T = 0.026
        result = func(voltage, I_s, V_T)
        expected = I_s * safe_expm1(voltage / V_T)
        np.testing.assert_allclose(result, expected, rtol=1e-14)
        
    def test_get_accelerated_diode_current_specific_backends(self):
        """Test selection of specific backends for diode current."""
        backends = ["numpy", "numba", "jax"]
        
        voltage = np.array([0, 0.5, 1.0])
        I_s = 1e-12
        V_T = 0.026
        expected = I_s * safe_expm1(voltage / V_T)
        
        for backend in backends:
            func = get_accelerated_diode_current(backend)
            assert callable(func)
            
            result = func(voltage, I_s, V_T)
            np.testing.assert_allclose(result, expected, rtol=1e-14)
            
    def test_get_accelerated_diode_current_invalid_backend(self):
        """Test error handling for invalid backend."""
        with pytest.raises(ValueError, match="Unknown backend"):
            get_accelerated_diode_current("invalid")


class TestPerformanceConsistency:
    """Test that accelerated versions give consistent results across problem sizes."""
    
    def test_small_vs_large_arrays(self):
        """Test consistency between small and large array computations."""
        # Small array
        x_small = np.array([0, 0.5, 1.0])
        
        # Large array
        x_large = np.linspace(-2, 2, 10000)
        
        # Test expm1 variants
        func_numpy = get_accelerated_expm1("numpy")
        func_auto = get_accelerated_expm1("auto")
        
        result_small_numpy = func_numpy(x_small)
        result_small_auto = func_auto(x_small)
        np.testing.assert_allclose(result_small_numpy, result_small_auto, rtol=1e-14)
        
        result_large_numpy = func_numpy(x_large)
        result_large_auto = func_auto(x_large)
        np.testing.assert_allclose(result_large_numpy, result_large_auto, rtol=1e-14)
        
    def test_diode_current_consistency(self):
        """Test diode current consistency across different array sizes."""
        I_s = 1e-12
        V_T = 0.026
        
        # Small voltage array
        v_small = np.array([0, 0.3, 0.7])
        
        # Large voltage array  
        v_large = np.linspace(-1, 1, 10000)
        
        func_numpy = get_accelerated_diode_current("numpy")
        func_auto = get_accelerated_diode_current("auto")
        
        # Test small arrays
        result_small_numpy = func_numpy(v_small, I_s, V_T)
        result_small_auto = func_auto(v_small, I_s, V_T)
        np.testing.assert_allclose(result_small_numpy, result_small_auto, rtol=1e-14)
        
        # Test large arrays
        result_large_numpy = func_numpy(v_large, I_s, V_T)
        result_large_auto = func_auto(v_large, I_s, V_T)
        np.testing.assert_allclose(result_large_numpy, result_large_auto, rtol=1e-14)


def test_integration_with_device_equations():
    """Integration test with realistic device equation parameters."""
    # Realistic semiconductor parameters
    I_s = 1e-14  # Saturation current (A)
    V_T = 0.026  # Thermal voltage (V)
    
    # Voltage range typical for semiconductor devices
    voltage = np.linspace(-0.5, 1.0, 1000)
    
    # Test all acceleration variants give same results
    func_numpy = get_accelerated_diode_current("numpy")
    func_auto = get_accelerated_diode_current("auto")
    
    current_numpy = func_numpy(voltage, I_s, V_T)
    current_auto = func_auto(voltage, I_s, V_T)
    
    # Should be identical within numerical precision
    np.testing.assert_allclose(current_numpy, current_auto, rtol=1e-14)
    
    # Test specific values make physical sense
    # At V = 0, current should be approximately 0 (actually -I_s)
    zero_idx = np.argmin(np.abs(voltage))
    assert abs(current_numpy[zero_idx] + I_s) < 1e-13
    
    # At forward bias (V > 0), current should be positive and increasing
    forward_mask = voltage > 0.1
    forward_currents = current_numpy[forward_mask]
    assert np.all(forward_currents > 0)
    assert np.all(np.diff(forward_currents) > 0)  # Monotonically increasing
    
    # At reverse bias (V < 0), current should be approximately -I_s
    reverse_mask = voltage < -0.1
    reverse_currents = current_numpy[reverse_mask]
    assert np.all(np.abs(reverse_currents - (-I_s)) < 1e-15)