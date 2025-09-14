# tests/test_led.py

import unittest

import numpy as np

from semiconductor_sim import LED
from semiconductor_sim.materials import get_material


class TestLED(unittest.TestCase):
    def test_saturation_current(self):
        led = LED(doping_p=1e17, doping_n=1e17, efficiency=0.2, temperature=300)
        self.assertGreater(led.I_s, 0, "Saturation current should be positive")

    def test_iv_characteristic_length(self):
        led = LED(doping_p=1e17, doping_n=1e17, efficiency=0.2, temperature=300)
        voltage = np.array([0.0, 0.5, 1.0])
        current, emission = led.iv_characteristic(voltage)
        self.assertEqual(len(current), len(voltage), "Current array length mismatch")
        self.assertEqual(len(emission), len(voltage), "Emission array length mismatch")

    def test_efficiency_boundaries(self):
        led = LED(doping_p=1e17, doping_n=1e17, efficiency=1.0, temperature=300)
        voltage = np.array([0.0, 0.5, 1.0])
        current, emission = led.iv_characteristic(voltage)
        self.assertTrue(np.all(emission <= current), "Emission should not exceed total current")

    def test_material_option_changes_Is(self):
        si = get_material("Si")
        led_default = LED(doping_p=1e17, doping_n=1e17, efficiency=0.2, temperature=300)
        led_si = LED(doping_p=1e17, doping_n=1e17, efficiency=0.2, temperature=300, material=si)
        self.assertGreater(led_default.I_s, 0)
        self.assertGreater(led_si.I_s, 0)
        self.assertNotEqual(led_default.I_s, led_si.I_s)


if __name__ == '__main__':
    unittest.main()
