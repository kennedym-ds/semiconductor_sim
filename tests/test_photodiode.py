import numpy as np

from semiconductor_sim import Photodiode


def test_photodiode_iv_shapes_and_sign():
    d = Photodiode(1e17, 1e17, irradiance_W_per_cm2=1e-3, responsivity_A_per_W=0.5)
    v = np.linspace(-0.1, 0.6, 50)
    (I,) = d.iv_characteristic(v)
    assert I.shape == v.shape
    # At small positive voltages, illuminated current should be negative (photocurrent dominates)
    assert I[0] < 0
