# tests/test_tunnel_diode.py

import unittest
import numpy as np
from semiconductor_sim import TunnelDiode

class TestTunnelDiode(unittest.TestCase):
    def test_saturation_current(self):
        diode = TunnelDiode(doping_p=1e19, doping_n=1e19, temperature=300)
        self.assertGreater(diode.I_s, 0, "Saturation current should be positive")
    
    def test_iv_characteristic_length(self):
        diode = TunnelDiode(doping_p=1e19, doping_n=1e19, temperature=300)
        voltage = np.array([0.0, 0.1, 0.2])
        current, recombination = diode.iv_characteristic(voltage, n_conc=1e18, p_conc=1e18)
        self.assertEqual(len(current), len(voltage), "Current array length mismatch")
        self.assertEqual(len(recombination), len(voltage), "Recombination array length mismatch")
    
    def test_negative_voltage(self):
        diode = TunnelDiode(doping_p=1e19, doping_n=1e19, temperature=300)
        voltage = np.array([-0.1, -0.2, -0.3])
        current, recombination = diode.iv_characteristic(voltage, n_conc=1e18, p_conc=1e18)
        self.assertTrue(np.all(current < 0), "Current should be negative for reverse bias")

if __name__ == '__main__':
    unittest.main()
