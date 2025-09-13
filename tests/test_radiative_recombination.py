# tests/test_radiative_recombination.py

import unittest

import numpy as np

from semiconductor_sim.models import radiative_recombination


class TestRadiativeRecombination(unittest.TestCase):
    def test_radiative_recombination_positive(self):
        n = np.array([1e16, 1e17, 1e18])
        p = np.array([1e16, 1e17, 1e18])
        R_rad = radiative_recombination(n, p, B=1e-10, temperature=300)
        self.assertTrue(np.all(R_rad >= 0), "Radiative recombination rate should be non-negative")

    def test_radiative_recombination_zero(self):
        n = np.array([0, 0, 0])
        p = np.array([0, 0, 0])
        R_rad = radiative_recombination(n, p, B=1e-10, temperature=300)
        self.assertTrue(
            np.all(R_rad == 0),
            "Radiative recombination rate should be zero when carrier concentrations are zero",
        )

    def test_radiative_recombination_scalar(self):
        n = 1e17
        p = 1e17
        R_rad = radiative_recombination(n, p, B=1e-10, temperature=300)
        self.assertEqual(
            R_rad,
            1e-10 * (n * p - 1.5e10**2),
            "Incorrect radiative recombination rate for scalar inputs",
        )


if __name__ == '__main__':
    unittest.main()
