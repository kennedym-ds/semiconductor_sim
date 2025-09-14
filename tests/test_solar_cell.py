# tests/test_solar_cell.py

import unittest

import numpy as np

from semiconductor_sim import SolarCell
from semiconductor_sim.materials import get_material


class TestSolarCell(unittest.TestCase):
    def test_short_circuit_current(self):
        solar = SolarCell(doping_p=1e17, doping_n=1e17, light_intensity=1.0, temperature=300)
        self.assertGreater(solar.I_sc, 0, "Short-circuit current should be positive")

    def test_open_circuit_voltage(self):
        solar = SolarCell(doping_p=1e17, doping_n=1e17, light_intensity=1.0, temperature=300)
        self.assertGreater(solar.V_oc, 0, "Open-circuit voltage should be positive")

    def test_iv_characteristic_length(self):
        solar = SolarCell(doping_p=1e17, doping_n=1e17, light_intensity=1.0, temperature=300)
        voltage = np.array([0.0, 0.4, 0.8])
        (current,) = solar.iv_characteristic(voltage)
        self.assertEqual(len(current), len(voltage), "Current array length mismatch")

    def test_material_option_changes_Is_and_Voc(self):
        si = get_material("Si")
        sc_default = SolarCell(doping_p=1e17, doping_n=1e17, light_intensity=1.0, temperature=300)
        sc_si = SolarCell(
            doping_p=1e17, doping_n=1e17, light_intensity=1.0, temperature=300, material=si
        )
        # Dark saturation current should be positive and likely differ with material
        self.assertGreater(sc_default.I_s, 0)
        self.assertGreater(sc_si.I_s, 0)
        self.assertNotEqual(sc_default.I_s, sc_si.I_s)
        # V_oc depends on I_s, so also expect a change
        self.assertNotEqual(sc_default.V_oc, sc_si.V_oc)


if __name__ == '__main__':
    unittest.main()
