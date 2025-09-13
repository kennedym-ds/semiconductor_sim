"""Additional unit tests for models to improve coverage."""

import numpy as np

from semiconductor_sim.models import (
    high_frequency_capacitance,
    srh_recombination,
    temperature_dependent_bandgap,
)
from semiconductor_sim.utils import DEFAULT_T


def test_srh_equilibrium_zero_at_midgap():
    """At equilibrium with mid-gap trap (n=p=n_i) SRH should be ~0."""
    T = float(DEFAULT_T)
    n_i = 1.5e10 * (T / float(DEFAULT_T)) ** 1.5
    R = srh_recombination(n_i, n_i, temperature=T)
    assert np.allclose(R, 0.0)


def test_srh_broadcasting_shapes():
    """SRH should broadcast when one of the inputs is an array."""
    T = float(DEFAULT_T)
    p = np.linspace(1e14, 1e16, 7)
    n = 1e15
    R = np.asarray(srh_recombination(n, p, temperature=T))
    assert R.shape == p.shape


def test_bandgap_varshni_monotonic_decrease_with_temperature():
    """Varshni equation: bandgap decreases as temperature increases."""
    Eg_300 = temperature_dependent_bandgap(300.0)
    Eg_600 = temperature_dependent_bandgap(600.0)
    assert Eg_300 > Eg_600


def test_high_frequency_capacitance_limits():
    """AC capacitance equals DC at f=0 and decreases with frequency."""
    Cdc = np.array([1e-9, 2e-9, 5e-9])
    C0 = high_frequency_capacitance(Cdc, f=0.0)
    assert np.allclose(C0, Cdc)

    Chigh = high_frequency_capacitance(Cdc, f=1e6)
    assert np.all(Chigh < Cdc)
