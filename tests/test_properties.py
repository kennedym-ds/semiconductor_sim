import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import given, strategies as st

from semiconductor_sim import PNJunctionDiode, LED
from semiconductor_sim.utils.numerics import safe_expm1


@given(st.lists(st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False), min_size=3, max_size=20).map(sorted))
def test_pn_forward_iv_monotonic(volts):
    v = np.array(volts, dtype=float)
    diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    current, _ = diode.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    # Check non-decreasing
    npt.assert_array_less(-np.diff(current), 1e-20)


@given(st.lists(st.floats(min_value=-1.5, max_value=-0.01, allow_nan=False, allow_infinity=False), min_size=3, max_size=20))
def test_pn_reverse_iv_negative(volts):
    v = np.array(volts, dtype=float)
    diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    current, _ = diode.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    assert np.all(current <= 0.0)


def test_broadcasting_of_recombination_scalar():
    v = np.linspace(0.0, 1.0, 5)
    diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    I, R = diode.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    assert R.shape == v.shape


@pytest.mark.parametrize("x", [0.0, 1e-12, -1e-12, 700.0, -700.0, 1e6, -1e6])
def test_safe_expm1_boundaries(x):
    # Should not raise and should be finite
    y = safe_expm1(x)
    assert np.all(np.isfinite(y))