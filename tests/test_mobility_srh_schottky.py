import numpy as np

from semiconductor_sim.devices.schottky import SchottkyDiode
from semiconductor_sim.models.mobility import mu_n, mu_p
from semiconductor_sim.models.srh import srh_rate


def test_mobility_trends():
    low = mu_n(1e14)
    high = mu_n(1e19)
    assert low > high
    low_p = mu_p(1e14)
    high_p = mu_p(1e19)
    assert low_p > high_p


def test_srh_rate_equilibrium_zero():
    n_i = 1e10
    n = np.array([n_i, n_i])
    p = np.array([n_i, n_i])
    R = srh_rate(n, p, n_i=n_i, tau_n=1e-6, tau_p=1e-6)
    assert np.allclose(R, 0.0, atol=1e-30)


def test_schottky_iv_forward_current_increases():
    d = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1)
    V = np.linspace(0.0, 0.3, 5)
    (I,) = d.iv_characteristic(V)
    assert I[-1] > I[0]
