# tests/test_mos_capacitor.py

import unittest
import numpy as np
from semiconductor_sim import MOSCapacitor

class TestMOSCapacitor(unittest.TestCase):
    def test_oxide_capacitance(self):
        mos = MOSCapacitor(doping_p=1e17, oxide_thickness=1e-6, oxide_permittivity=3.45, temperature=300)
        self.assertGreater(mos.C_ox, 0, "Oxide capacitance should be positive")
    
    def test_capacitance_vs_voltage(self):
        mos = MOSCapacitor(doping_p=1e17, oxide_thickness=1e-6, oxide_permittivity=3.45, temperature=300)
        voltage = np.array([-5, 0, 5])
        capacitance = mos.capacitance(voltage)
        self.assertTrue(np.all(capacitance > 0), "Capacitance should be positive")
    
    def test_depletion_width(self):
        mos = MOSCapacitor(doping_p=1e17, oxide_thickness=1e-6, oxide_permittivity=3.45, temperature=300)
        voltage = np.array([1, 2, 3])
        W = mos.depletion_width(voltage)
        self.assertTrue(np.all(W > 0), "Depletion width should be positive")
    
    def test_iv_characteristic_length(self):
        mos = MOSCapacitor(doping_p=1e17, oxide_thickness=1e-6, oxide_permittivity=3.45, temperature=300)
        voltage = np.array([-2, 0, 2])
        current, recombination = mos.iv_characteristic(voltage, n_conc=1e16, p_conc=1e16)
        self.assertEqual(len(current), len(voltage), "Current array length mismatch")
        self.assertEqual(len(recombination), len(voltage), "Recombination array length mismatch")

if __name__ == '__main__':
    unittest.main()
