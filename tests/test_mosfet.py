import numpy as np

from semiconductor_sim import MOSFET


def test_mosfet_iv_shapes():
    m = MOSFET(vgs_values=[0.8, 1.5, 2.0])
    vds = np.linspace(0.0, 3.0, 7)
    ids, gm = m.iv_characteristic(vds)
    assert ids.shape == (3, 7)
    assert gm.shape == (3, 7)


def test_mosfet_cutoff_and_vgs_monotonicity():
    m = MOSFET(threshold_voltage=1.0, vgs_values=[0.5, 1.5, 2.5], channel_length_modulation=0.0)
    vds = np.array([0.5, 1.0, 2.0])
    ids, _ = m.iv_characteristic(vds)
    assert np.allclose(ids[0], 0.0)
    assert np.all(ids[2] >= ids[1])


def test_mosfet_saturation_flat_when_no_channel_modulation():
    m = MOSFET(threshold_voltage=1.0, vgs_values=[2.0], channel_length_modulation=0.0)
    vds = np.array([0.5, 1.0, 2.0, 3.0])
    ids, _ = m.iv_characteristic(vds)
    assert np.isclose(ids[0, 1], ids[0, 2])
    assert np.isclose(ids[0, 2], ids[0, 3])
