"""Additional device tests to increase coverage across branches and helpers."""

import numpy as np
import pytest

from semiconductor_sim import (
    LED,
    MOSCapacitor,
    PNJunctionDiode,
    SolarCell,
    VaractorDiode,
    ZenerDiode,
)
from semiconductor_sim.utils.plotting import apply_basic_style, use_headless_backend


def test_device_repr_smoke():
    objs = [
        PNJunctionDiode(1e17, 1e17),
        LED(1e17, 1e17, efficiency=0.2),
        SolarCell(1e17, 1e17, light_intensity=0.5),
        VaractorDiode(1e17, 1e17),
        MOSCapacitor(1e17),
        ZenerDiode(1e17, 1e17, zener_voltage=5.0),
    ]
    for obj in objs:
        s = repr(obj)
        assert isinstance(s, str) and len(s) > 0


@pytest.mark.parametrize("area,temperature", [(-1.0, 300), (1e-4, -10), (0.0, 300), (1e-4, 0.0)])
def test_device_invalid_params(area, temperature):
    with pytest.raises(ValueError):
        # Use PNJunctionDiode to exercise base class validation
        PNJunctionDiode(1e17, 1e17, area=area, temperature=temperature)


def test_led_emission_increases_with_concentration():
    led = LED(1e17, 1e17, efficiency=0.5)
    v = np.linspace(0.0, 1.0, 5)
    I1, E1 = led.iv_characteristic(v)
    I2, E2, _ = led.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    # With radiative component, emission should not be lower everywhere
    assert np.any(E2 >= E1)
    # Current should be identical for same voltage regardless of concentrations
    np.testing.assert_allclose(I1, I2)


def test_mos_cv_transition_behavior():
    mos = MOSCapacitor(1e17, oxide_thickness=1e-6, oxide_permittivity=3.45)
    v = np.array([-3.0, -1.0, 0.0, 1.0, 3.0])
    C = mos.capacitance(v)
    # Negative voltages -> depletion branch used by model
    assert np.all(C[v < 0] > 0)
    # Non-negative voltages -> equals C_ox in simplified model
    assert np.allclose(C[v >= 0], mos.C_ox)


def test_varactor_capacitance_monotonic_decrease():
    var = VaractorDiode(1e17, 1e17)
    v = np.array([0.1, 0.5, 1.0, 2.0])
    C = var.capacitance(v)
    assert np.all(np.diff(C) < 0)


def test_solarcell_iv_has_expected_signs():
    sc = SolarCell(1e17, 1e17, light_intensity=1.0)
    v = np.linspace(0.0, 0.8, 5)
    (I,) = sc.iv_characteristic(v)
    # Short-circuit current at V=0 approximates I_sc
    assert I[0] > 0
    # As voltage increases, current decreases
    assert I[-1] < I[0]


def test_zener_breakdown_kick_in_and_prediction_fallback(tmp_path, monkeypatch):
    z = ZenerDiode(1e17, 1e17, zener_voltage=4.0)
    # Ensure ML model is not found to exercise fallback path
    monkeypatch.setattr(z, "load_ml_model", lambda: None, raising=False)
    z.model = None
    z.zener_voltage = z.predict_zener_voltage()
    v = np.array([3.5, 4.0, 4.5, 5.0])
    I, R = z.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    # After breakdown, current should increase faster
    assert I[-1] > I[-2]
    # Recombination broadcasted to voltage shape
    assert R.shape == v.shape


def test_plotting_helpers_noop_headless():
    # Should not raise in environments without display
    use_headless_backend("Agg")
    apply_basic_style()
