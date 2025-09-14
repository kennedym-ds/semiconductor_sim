import numpy as np
import pytest

from semiconductor_sim.devices.schottky import (
    BARRIER_MAX_EV,
    BARRIER_MIN_EV,
    IDEALITY_MAX,
    IDEALITY_MIN,
    SchottkyDiode,
)


def test_schottky_parameter_validation():
    with pytest.raises(ValueError):
        SchottkyDiode(barrier_height_eV=BARRIER_MIN_EV - 0.01)
    with pytest.raises(ValueError):
        SchottkyDiode(barrier_height_eV=BARRIER_MAX_EV + 0.01)
    with pytest.raises(ValueError):
        SchottkyDiode(ideality=IDEALITY_MIN - 0.01)
    with pytest.raises(ValueError):
        SchottkyDiode(ideality=IDEALITY_MAX + 0.01)


def test_schottky_temperature_dependence():
    d_cold = SchottkyDiode(barrier_height_eV=0.7, temperature=250.0)
    d_hot = SchottkyDiode(barrier_height_eV=0.7, temperature=350.0)
    V = np.array([0.2])
    (I_cold,) = d_cold.iv_characteristic(V)
    (I_hot,) = d_hot.iv_characteristic(V)
    assert I_hot[0] > I_cold[0]


def test_schottky_series_resistance_limits():
    V = np.linspace(0.0, 0.5, 6)
    d_no_rs = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1, series_resistance_ohm=None)
    (I_no_rs,) = d_no_rs.iv_characteristic(V)

    d_small_rs = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1, series_resistance_ohm=1e-6)
    (I_small_rs,) = d_small_rs.iv_characteristic(V)
    # Very small Rs should approximate no-Rs solution closely
    assert np.allclose(I_small_rs, I_no_rs, rtol=1e-3, atol=0.0)

    d_large_rs = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1, series_resistance_ohm=1e6)
    (I_large_rs,) = d_large_rs.iv_characteristic(V)
    # Extremely large Rs should significantly reduce forward current at higher bias
    assert I_large_rs[-1] < I_no_rs[-1] * 0.5
