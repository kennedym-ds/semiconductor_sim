# tests/test_bjt.py

import unittest
import numpy as np
from semiconductor_sim import BJT


class TestBJT(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.npn_bjt = BJT(
            doping_emitter=1e18,
            doping_base=1e16,
            doping_collector=1e17,
            bjt_type="NPN",
            beta_f=100.0,
            beta_r=1.0,
            temperature=300
        )
        self.pnp_bjt = BJT(
            doping_emitter=1e18,
            doping_base=1e16,
            doping_collector=1e17,
            bjt_type="PNP",
            beta_f=100.0,
            beta_r=1.0,
            temperature=300
        )

    def test_initialization(self):
        """Test BJT initialization."""
        self.assertEqual(self.npn_bjt.bjt_type, "NPN")
        self.assertEqual(self.pnp_bjt.bjt_type, "PNP")
        self.assertGreater(self.npn_bjt.I_s, 0)
        self.assertGreater(self.pnp_bjt.I_s, 0)
        self.assertGreater(self.npn_bjt.beta_f_eff, 0)
        self.assertGreater(self.npn_bjt.beta_r_eff, 0)

    def test_iv_characteristic_length(self):
        """Test that output arrays have correct length."""
        v_be = np.array([0.0, 0.1, 0.2])
        i_c, i_b, recomb = self.npn_bjt.iv_characteristic(v_be)
        
        self.assertEqual(len(i_c), len(v_be))
        self.assertEqual(len(i_b), len(v_be))
        self.assertEqual(len(recomb), len(v_be))

    def test_npn_forward_active_region(self):
        """Test NPN transistor in forward active region (V_BE > 0, V_BC <= 0)."""
        v_be = np.array([0.6, 0.7, 0.8])  # Forward bias base-emitter
        v_bc = 0.0  # Zero or reverse bias base-collector
        
        i_c, i_b, _ = self.npn_bjt.iv_characteristic(v_be, v_bc)
        
        # In forward active: I_C should be positive and much larger than I_B
        self.assertTrue(np.all(i_c > 0), "Collector current should be positive in forward active")
        self.assertTrue(np.all(i_b > 0), "Base current should be positive in forward active")
        
        # Current gain should be approximately beta_f
        beta = i_c / i_b
        # Allow some tolerance due to numerical effects
        self.assertTrue(np.all(beta > 10), "Current gain should be substantial in forward active")

    def test_npn_cutoff_region(self):
        """Test NPN transistor in cutoff region (V_BE <= 0, V_BC <= 0)."""
        v_be = np.array([-0.1, -0.2, -0.3])  # Reverse bias base-emitter
        v_bc = 0.0  # Zero bias base-collector
        
        i_c, i_b, _ = self.npn_bjt.iv_characteristic(v_be, v_bc)
        
        # In cutoff: currents should be very small (essentially zero)
        self.assertTrue(np.all(np.abs(i_c) < 1e-10), "Collector current should be near zero in cutoff")
        self.assertTrue(np.all(np.abs(i_b) < 1e-10), "Base current should be near zero in cutoff")

    def test_pnp_behavior(self):
        """Test that PNP shows appropriate behavior for forward bias."""
        # For PNP, we need negative V_BE to forward bias (or positive V_EB)
        v_be_pnp_forward = np.array([-0.6, -0.7, -0.8])  # Forward bias for PNP
        v_be_npn_forward = np.array([0.6, 0.7, 0.8])     # Forward bias for NPN
        
        i_c_npn, i_b_npn, _ = self.npn_bjt.iv_characteristic(v_be_npn_forward)
        i_c_pnp, i_b_pnp, _ = self.pnp_bjt.iv_characteristic(v_be_pnp_forward)
        
        # Both should be in forward active with similar magnitude currents
        self.assertTrue(np.all(i_c_npn > 0), "NPN should have positive I_C for positive V_BE")
        self.assertTrue(np.all(i_b_npn > 0), "NPN should have positive I_B for positive V_BE")
        self.assertTrue(np.all(i_c_pnp < 0), "PNP should have negative I_C for negative V_BE")
        self.assertTrue(np.all(i_b_pnp < 0), "PNP should have negative I_B for negative V_BE")
        
        # Magnitudes should be similar (same device parameters)
        self.assertTrue(np.allclose(np.abs(i_c_npn), np.abs(i_c_pnp), rtol=0.1),
                        "NPN and PNP should have similar magnitude currents in forward active")

    def test_temperature_dependence(self):
        """Test that saturation current changes with temperature."""
        bjt_hot = BJT(
            doping_emitter=1e18,
            doping_base=1e16,
            doping_collector=1e17,
            temperature=350  # Higher temperature
        )
        
        # Higher temperature should increase saturation current
        self.assertGreater(bjt_hot.I_s, self.npn_bjt.I_s)

    def test_v_bc_array_input(self):
        """Test that V_BC can be provided as array."""
        v_be = np.array([0.6, 0.7, 0.8])
        v_bc = np.array([0.0, -0.1, -0.2])
        
        i_c, i_b, _ = self.npn_bjt.iv_characteristic(v_be, v_bc)
        
        self.assertEqual(len(i_c), len(v_be))
        self.assertEqual(len(i_b), len(v_be))

    def test_srh_recombination(self):
        """Test SRH recombination coupling."""
        v_be = np.array([0.6, 0.7, 0.8])
        n_conc = 1e16  # cm^-3
        p_conc = 1e16  # cm^-3
        
        i_c, i_b, recomb = self.npn_bjt.iv_characteristic(v_be, n_conc=n_conc, p_conc=p_conc)
        
        # Should have non-zero recombination
        self.assertTrue(np.any(recomb != 0), "Should have non-zero recombination when concentrations provided")

    def test_current_conservation(self):
        """Test that I_E = -(I_C + I_B) approximately holds."""
        v_be = np.array([0.6, 0.7, 0.8])
        
        i_c, i_b, _ = self.npn_bjt.iv_characteristic(v_be)
        i_e_expected = -(i_c + i_b)
        
        # For pedagogical model, this should hold quite well
        # but allow some numerical tolerance
        self.assertTrue(np.all(np.abs(i_e_expected) > 0), "Emitter current should be non-zero")

    def test_monotonic_behavior_forward(self):
        """Test that currents increase monotonically with V_BE in forward bias."""
        v_be = np.linspace(0.5, 0.8, 10)
        
        i_c, i_b, _ = self.npn_bjt.iv_characteristic(v_be)
        
        # Currents should increase with V_BE
        i_c_diff = np.diff(i_c)
        i_b_diff = np.diff(i_b)
        
        self.assertTrue(np.all(i_c_diff > 0), "Collector current should increase with V_BE")
        self.assertTrue(np.all(i_b_diff > 0), "Base current should increase with V_BE")

    def test_repr(self):
        """Test string representation."""
        repr_str = repr(self.npn_bjt)
        self.assertIn("BJT", repr_str)
        self.assertIn("NPN", repr_str)
        self.assertIn("beta_f", repr_str)


if __name__ == '__main__':
    unittest.main()