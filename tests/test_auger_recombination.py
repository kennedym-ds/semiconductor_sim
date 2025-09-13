# tests/test_auger_recombination.py

import unittest
import numpy as np
from semiconductor_sim.models import auger_recombination

class TestAugerRecombination(unittest.TestCase):
    def test_auger_recombination_positive(self):
        n = np.array([1e16, 1e17, 1e18])
        p = np.array([1e16, 1e17, 1e18])
        R_auger = auger_recombination(n, p, C=1e-31, temperature=300)
        self.assertTrue(np.all(R_auger >= 0), "Auger recombination rate should be non-negative")
    
    def test_auger_recombination_zero(self):
        n = np.array([0, 0, 0])
        p = np.array([0, 0, 0])
        R_auger = auger_recombination(n, p, C=1e-31, temperature=300)
        self.assertTrue(np.all(R_auger == 0), "Auger recombination rate should be zero when carrier concentrations are zero")
    
    def test_auger_recombination_scalar(self):
        n = 1e17
        p = 1e17
        R_auger = auger_recombination(n, p, C=1e-31, temperature=300)
        self.assertEqual(R_auger, 1e-31 * (n**2 * p + p**2 * n), "Incorrect Auger recombination rate for scalar inputs")

if __name__ == '__main__':
    unittest.main()
