import numpy as np

from semiconductor_sim import PINDiode


def test_pin_diode_shapes_and_monotonic():
    d = PINDiode(1e17, 1e17, intrinsic_width_cm=1e-4)
    v = np.linspace(-0.2, 0.9, 300)
    (i,) = d.iv_characteristic(v)
    assert i.shape == v.shape
    # Expect current to increase with voltage overall
    assert i[-1] > i[0]


def test_pin_diode_series_resistance_effect():
    v = np.linspace(0.0, 0.9, 200)
    d0 = PINDiode(1e17, 1e17, intrinsic_width_cm=1e-4, series_resistance_ohm=None)
    d2 = PINDiode(1e17, 1e17, intrinsic_width_cm=1e-4, series_resistance_ohm=2.0)
    (i0,) = d0.iv_characteristic(v)
    (i2,) = d2.iv_characteristic(v)
    # With series resistance, forward current should be reduced at higher voltages
    assert i2[-1] < i0[-1]
