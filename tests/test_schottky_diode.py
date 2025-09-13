# tests/test_schottky_diode.py

import unittest
import numpy as np
from semiconductor_sim import SchottkyDiode


class TestSchottkyDiode(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.diode = SchottkyDiode(
            barrier_height=0.8,  # eV
            area=1e-4,  # cm^2
            temperature=300,  # K
            A_eff=120.0,  # A/(cm^2·K^2)
            series_resistance=0.0,  # Ohm
            image_force_lowering=0.0  # eV
        )
    
    def test_initialization(self):
        """Test proper initialization of SchottkyDiode."""
        self.assertEqual(self.diode.barrier_height, 0.8)
        self.assertEqual(self.diode.area, 1e-4)
        self.assertEqual(self.diode.temperature, 300)
        self.assertEqual(self.diode.A_eff, 120.0)
        self.assertEqual(self.diode.series_resistance, 0.0)
        self.assertEqual(self.diode.image_force_lowering, 0.0)
        self.assertGreater(self.diode.I_s, 0, "Saturation current should be positive")
    
    def test_invalid_parameters(self):
        """Test that invalid parameters raise appropriate errors."""
        # Negative barrier height
        with self.assertRaises(ValueError):
            SchottkyDiode(barrier_height=-0.1)
        
        # Negative effective Richardson constant
        with self.assertRaises(ValueError):
            SchottkyDiode(barrier_height=0.8, A_eff=-10)
        
        # Negative series resistance
        with self.assertRaises(ValueError):
            SchottkyDiode(barrier_height=0.8, series_resistance=-1)
        
        # Negative image force lowering
        with self.assertRaises(ValueError):
            SchottkyDiode(barrier_height=0.8, image_force_lowering=-0.1)
    
    def test_iv_characteristic_length(self):
        """Test that IV characteristic returns arrays of correct length."""
        voltage = np.array([0.0, 0.1, 0.2, 0.3])
        current, = self.diode.iv_characteristic(voltage)
        self.assertEqual(len(current), len(voltage), "Current array length mismatch")
        self.assertTrue(isinstance(current, np.ndarray), "Current should be numpy array")
    
    def test_forward_monotonicity(self):
        """Test that forward current is monotonically increasing."""
        voltage = np.linspace(0.0, 0.5, 100)
        current, = self.diode.iv_characteristic(voltage)
        
        # Check that current is monotonically increasing in forward bias
        for i in range(1, len(current)):
            self.assertGreaterEqual(current[i], current[i-1], 
                                  f"Current not monotonic at index {i}")
    
    def test_reverse_leakage_behavior(self):
        """Test reverse bias leakage current behavior."""
        voltage = np.array([-0.1, -0.2, -0.5, -1.0])
        current, = self.diode.iv_characteristic(voltage)
        
        # In reverse bias, current should be negative and approximately -I_s
        self.assertTrue(np.all(current < 0), "Reverse current should be negative")
        
        # For large reverse bias, current should approach -I_s
        expected_reverse = -self.diode.I_s
        self.assertAlmostEqual(current[-1], expected_reverse, places=10,
                              msg="Large reverse bias current should approach -I_s")
    
    def test_broadcasting(self):
        """Test that the function works with different array shapes."""
        # Scalar input
        V_scalar = 0.2
        I_scalar, = self.diode.iv_characteristic(np.array([V_scalar]))
        self.assertEqual(len(I_scalar), 1)
        
        # 1D array
        V_1d = np.array([0.1, 0.2, 0.3])
        I_1d, = self.diode.iv_characteristic(V_1d)
        self.assertEqual(I_1d.shape, V_1d.shape)
        
        # 2D array
        V_2d = np.array([[0.1, 0.2], [0.3, 0.4]])
        I_2d, = self.diode.iv_characteristic(V_2d)
        self.assertEqual(I_2d.shape, V_2d.shape)
    
    def test_temperature_dependence(self):
        """Test temperature dependence of saturation current."""
        # Create diodes at different temperatures
        T1, T2 = 300, 400
        diode1 = SchottkyDiode(barrier_height=0.8, temperature=T1)
        diode2 = SchottkyDiode(barrier_height=0.8, temperature=T2)
        
        # Richardson equation: I_s ∝ T^2 * exp(-φ_B/k_B*T)
        # At higher temperature, I_s should be larger
        self.assertGreater(diode2.I_s, diode1.I_s, 
                          "Higher temperature should give larger saturation current")
        
        # Test that current increases with temperature at fixed voltage
        voltage = np.array([0.2])
        I1, = diode1.iv_characteristic(voltage)
        I2, = diode2.iv_characteristic(voltage)
        self.assertGreater(I2[0], I1[0], 
                          "Higher temperature should give larger forward current")
    
    def test_series_resistance_effect(self):
        """Test the effect of series resistance on IV characteristics."""
        # Create diodes with and without series resistance
        diode_no_rs = SchottkyDiode(barrier_height=0.8, series_resistance=0.0)
        diode_with_rs = SchottkyDiode(barrier_height=0.8, series_resistance=10.0)
        
        voltage = np.array([0.3, 0.5, 0.7])
        
        I_no_rs, = diode_no_rs.iv_characteristic(voltage)
        I_with_rs, = diode_with_rs.iv_characteristic(voltage)
        
        # With series resistance, current should be lower for same applied voltage
        for i in range(len(voltage)):
            self.assertLess(I_with_rs[i], I_no_rs[i], 
                           f"Series resistance should reduce current at V={voltage[i]}")
    
    def test_image_force_lowering(self):
        """Test the effect of image force lowering on barrier height."""
        # Create diodes with and without image force lowering
        diode_no_ifl = SchottkyDiode(barrier_height=0.8, image_force_lowering=0.0)
        diode_with_ifl = SchottkyDiode(barrier_height=0.8, image_force_lowering=0.1)
        
        # Effective barrier height should be reduced
        self.assertAlmostEqual(diode_with_ifl.barrier_height_eff, 0.7, places=10)
        
        # Lower effective barrier should give higher saturation current
        self.assertGreater(diode_with_ifl.I_s, diode_no_ifl.I_s, 
                          "Image force lowering should increase saturation current")
    
    def test_zero_voltage(self):
        """Test behavior at zero voltage."""
        voltage = np.array([0.0])
        current, = self.diode.iv_characteristic(voltage)
        
        # At zero voltage, current should be zero (exp(0) - 1 = 0)
        self.assertAlmostEqual(current[0], 0.0, places=12, 
                              msg="Current should be zero at zero voltage")
    
    def test_large_forward_voltage(self):
        """Test behavior at large forward voltages."""
        voltage = np.array([2.0])  # Large forward voltage
        current, = self.diode.iv_characteristic(voltage)
        
        # Should not raise overflow errors and should give finite result
        self.assertTrue(np.isfinite(current[0]), "Current should be finite")
        self.assertGreater(current[0], 0, "Large forward voltage should give positive current")
    
    def test_repr(self):
        """Test string representation."""
        diode_str = repr(self.diode)
        self.assertIn("SchottkyDiode", diode_str)
        self.assertIn("barrier_height=0.8", diode_str)
        self.assertIn("temperature=300", diode_str)


if __name__ == '__main__':
    unittest.main()