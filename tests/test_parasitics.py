# tests/test_parasitics.py

import unittest
import numpy as np
from semiconductor_sim.devices import PNJunctionDiode


class TestParasitics(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with known diode parameters."""
        self.doping_p = 1e17
        self.doping_n = 1e17
        self.area = 1e-4
        self.temperature = 300
        self.voltage = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
        
    def test_parasitic_limits_Rs_zero(self):
        """Test that R_s -> 0 recovers ideal behavior."""
        # Create ideal diode (no parasitics)
        diode_ideal = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature
        )
        
        # Create diode with R_s=0 and parasitics enabled
        diode_Rs_zero = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature,
            R_s=0.0,
            R_sh=np.inf,
            enable_parasitics=True
        )
        
        # Get currents
        current_ideal, _ = diode_ideal.iv_characteristic(self.voltage)
        current_Rs_zero, _ = diode_Rs_zero.iv_characteristic(self.voltage)
        
        # Should be approximately equal
        np.testing.assert_allclose(current_ideal, current_Rs_zero, rtol=1e-10)
        
    def test_parasitic_limits_Rsh_infinite(self):
        """Test that R_sh -> ∞ recovers ideal behavior when R_s=0."""
        # Create ideal diode (no parasitics)
        diode_ideal = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature
        )
        
        # Create diode with R_sh=inf and parasitics enabled
        diode_Rsh_inf = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature,
            R_s=0.0,
            R_sh=np.inf,
            enable_parasitics=True
        )
        
        # Get currents
        current_ideal, _ = diode_ideal.iv_characteristic(self.voltage)
        current_Rsh_inf, _ = diode_Rsh_inf.iv_characteristic(self.voltage)
        
        # Should be approximately equal
        np.testing.assert_allclose(current_ideal, current_Rsh_inf, rtol=1e-10)
        
    def test_series_resistance_effect(self):
        """Test that series resistance reduces current for positive voltages."""
        # Create ideal diode
        diode_ideal = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature
        )
        
        # Create diode with series resistance
        diode_Rs = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature,
            R_s=10.0,  # 10 ohm series resistance
            R_sh=np.inf,
            enable_parasitics=True
        )
        
        # Test at positive voltages where current flows
        voltage_pos = np.array([0.5, 0.6, 0.7])
        current_ideal, _ = diode_ideal.iv_characteristic(voltage_pos)
        current_Rs, _ = diode_Rs.iv_characteristic(voltage_pos)
        
        # Series resistance should reduce current
        for i in range(len(voltage_pos)):
            self.assertLess(current_Rs[i], current_ideal[i], 
                           f"Series resistance should reduce current at V={voltage_pos[i]}")
                           
    def test_shunt_resistance_effect(self):
        """Test that shunt resistance increases current (leakage)."""
        # Create ideal diode  
        diode_ideal = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature
        )
        
        # Create diode with shunt resistance
        diode_Rsh = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature,
            R_s=0.0,
            R_sh=1e6,  # 1 MΩ shunt resistance
            enable_parasitics=True
        )
        
        # Test at all voltages
        current_ideal, _ = diode_ideal.iv_characteristic(self.voltage)
        current_Rsh, _ = diode_Rsh.iv_characteristic(self.voltage)
        
        # Shunt resistance should increase current magnitude
        for i in range(len(self.voltage)):
            if self.voltage[i] != 0:  # Skip zero voltage
                self.assertGreater(abs(current_Rsh[i]), abs(current_ideal[i]),
                                 f"Shunt resistance should increase current magnitude at V={self.voltage[i]}")
                                 
    def test_parasitics_disabled_equals_ideal(self):
        """Test that parasitics disabled equals ideal behavior."""
        # Create ideal diode
        diode_ideal = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature
        )
        
        # Create diode with parasitics but disabled
        diode_disabled = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            area=self.area,
            temperature=self.temperature,
            R_s=100.0,  # Large values
            R_sh=1e3,
            enable_parasitics=False  # But disabled
        )
        
        # Get currents
        current_ideal, _ = diode_ideal.iv_characteristic(self.voltage)
        current_disabled, _ = diode_disabled.iv_characteristic(self.voltage)
        
        # Should be identical
        np.testing.assert_allclose(current_ideal, current_disabled, rtol=1e-15)
        
    def test_input_validation(self):
        """Test input validation for parasitic parameters."""
        # Test negative R_s
        with self.assertRaises(ValueError):
            PNJunctionDiode(
                doping_p=self.doping_p,
                doping_n=self.doping_n,
                R_s=-1.0
            )
            
        # Test zero R_sh
        with self.assertRaises(ValueError):
            PNJunctionDiode(
                doping_p=self.doping_p,
                doping_n=self.doping_n,
                R_sh=0.0
            )
            
        # Test negative R_sh
        with self.assertRaises(ValueError):
            PNJunctionDiode(
                doping_p=self.doping_p,
                doping_n=self.doping_n,
                R_sh=-100.0
            )
            
    def test_temperature_dependence(self):
        """Test improved temperature dependence."""
        # Create diodes at different temperatures
        diode_300K = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            temperature=300
        )
        
        diode_350K = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            temperature=350
        )
        
        # Saturation current should increase with temperature
        self.assertGreater(diode_350K.I_s, diode_300K.I_s,
                          "Saturation current should increase with temperature")
        
        # Test IV characteristics at a low voltage where saturation current dominates
        # At very low voltages, temperature increase should increase current
        voltage_test = np.array([0.1])  # Very low voltage
        current_300K, _ = diode_300K.iv_characteristic(voltage_test)
        current_350K, _ = diode_350K.iv_characteristic(voltage_test)
        
        # Higher temperature should give higher current at low voltages
        self.assertGreater(current_350K[0], current_300K[0],
                          "Current should increase with temperature at low voltage")
                          
        # Also test that the improved model gives different results than the old model
        # by comparing saturation currents (which should be different due to bandgap effects)
        old_n_i_300 = 1.5e10 * (300 / 300) ** 1.5  # Old simple model
        old_n_i_350 = 1.5e10 * (350 / 300) ** 1.5  # Old simple model
        old_ratio = old_n_i_350 / old_n_i_300
        
        # New model should give different ratio due to bandgap temperature dependence
        new_ratio = diode_350K.I_s / diode_300K.I_s
        
        # The ratios should be different (new model includes bandgap effects)
        self.assertNotAlmostEqual(old_ratio**2, new_ratio, places=2,
                                 msg="New temperature model should differ from simple T^1.5 scaling")


if __name__ == '__main__':
    unittest.main()