# tests/test_varactor_diode.py

import unittest

import numpy as np

from semiconductor_sim import VaractorDiode


class TestVaractorDiode(unittest.TestCase):
    def test_saturation_current(self):
        varactor = VaractorDiode(doping_p=1e17, doping_n=1e17, temperature=300)
        self.assertGreater(varactor.I_s, 0, "Saturation current should be positive")

    def test_capacitance(self):
        varactor = VaractorDiode(doping_p=1e17, doping_n=1e17, temperature=300)
        reverse_voltage = np.array([1, 2, 3, 4, 5])
        capacitance = varactor.capacitance(reverse_voltage)
        self.assertTrue(np.all(capacitance > 0), "Capacitance should be positive")

    def test_iv_characteristic_length(self):
        varactor = VaractorDiode(doping_p=1e17, doping_n=1e17, temperature=300)
        voltage = np.array([0.0, 1.0, 2.0])
        current, recombination = varactor.iv_characteristic(voltage, n_conc=1e16, p_conc=1e16)
        self.assertEqual(len(current), len(voltage), "Current array length mismatch")
        self.assertEqual(len(recombination), len(voltage), "Recombination array length mismatch")


if __name__ == '__main__':
    unittest.main()
