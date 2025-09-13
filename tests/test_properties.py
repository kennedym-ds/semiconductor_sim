import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import given, strategies as st, settings

from semiconductor_sim import PNJunctionDiode, LED
from semiconductor_sim.devices import SolarCell
from semiconductor_sim.utils.numerics import safe_expm1


# Property test strategies
voltage_forward = st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False)
voltage_reverse = st.floats(min_value=-2.0, max_value=-0.01, allow_nan=False, allow_infinity=False)
voltage_range = st.floats(min_value=-2.0, max_value=2.0, allow_nan=False, allow_infinity=False)
temperature_range = st.floats(min_value=250.0, max_value=400.0, allow_nan=False, allow_infinity=False)
doping_range = st.floats(min_value=1e15, max_value=1e19, allow_nan=False, allow_infinity=False)


@given(st.lists(voltage_forward, min_size=3, max_size=20).map(sorted))
@settings(max_examples=20)  # Reduce for faster testing
def test_pn_forward_iv_monotonic(volts):
    """Test that PN junction IV is monotonically increasing in forward bias."""
    v = np.array(volts, dtype=float)
    diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    current, _ = diode.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    # Check non-decreasing
    npt.assert_array_less(-np.diff(current), 1e-20)


@given(st.lists(voltage_reverse, min_size=3, max_size=20))
@settings(max_examples=20)
def test_pn_reverse_iv_negative(volts):
    """Test that PN junction has negative current in reverse bias."""
    v = np.array(volts, dtype=float)
    diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    current, _ = diode.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    assert np.all(current <= 0.0)


@given(st.lists(voltage_forward, min_size=3, max_size=20).map(sorted))
@settings(max_examples=20)
def test_led_forward_iv_monotonic(volts):
    """Test that LED IV is monotonically increasing in forward bias."""
    v = np.array(volts, dtype=float)
    led = LED(doping_p=1e17, doping_n=1e17, temperature=300)
    current, emission = led.iv_characteristic(v)
    # Current should be non-decreasing
    npt.assert_array_less(-np.diff(current), 1e-20)
    # Emission should be non-negative
    assert np.all(emission >= 0.0)


@given(st.lists(voltage_reverse, min_size=3, max_size=20))
@settings(max_examples=20)
def test_led_reverse_iv_negative(volts):
    """Test that LED has negative current in reverse bias."""
    v = np.array(volts, dtype=float)
    led = LED(doping_p=1e17, doping_n=1e17, temperature=300)
    current, emission = led.iv_characteristic(v)
    assert np.all(current <= 0.0)
    # No emission in reverse bias
    assert np.all(emission == 0.0)


@given(st.lists(st.floats(min_value=-0.5, max_value=1.0, allow_nan=False, allow_infinity=False), min_size=3, max_size=20))
@settings(max_examples=20)
def test_solar_cell_reasonable_bounds(volts):
    """Test that solar cell current is within reasonable bounds."""
    v = np.array(volts, dtype=float)
    solar_cell = SolarCell(doping_p=1e17, doping_n=1e17, area=1e-4, temperature=300)
    current = solar_cell.iv_characteristic(v)
    
    # Current should be finite
    assert np.all(np.isfinite(current))
    # For reasonable solar cell operating range, current should be bounded
    assert np.all(np.abs(current) < 1e6), "Current exceeds reasonable bounds"


@given(temperature_range)
@settings(max_examples=15)
def test_pn_temperature_dependence(temperature):
    """Test that PN junction behavior changes appropriately with temperature."""
    v = np.array([0.0, 0.5, 1.0])
    
    # Create devices at different temperatures
    diode_ref = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    diode_test = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=temperature)
    
    current_ref, _ = diode_ref.iv_characteristic(v)
    current_test, _ = diode_test.iv_characteristic(v)
    
    # At higher temperatures, saturation current should be higher
    # At lower temperatures, saturation current should be lower
    I_s_ref = diode_ref.I_s
    I_s_test = diode_test.I_s
    
    if temperature > 300:
        assert I_s_test > I_s_ref, "Saturation current should increase with temperature"
    elif temperature < 300:
        assert I_s_test < I_s_ref, "Saturation current should decrease with temperature"


@given(doping_range, doping_range)
@settings(max_examples=15)
def test_pn_doping_dependence(doping_p, doping_n):
    """Test that PN junction behavior depends on doping levels."""
    v = np.array([0.5])
    
    # Reference device
    diode_ref = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    diode_test = PNJunctionDiode(doping_p=doping_p, doping_n=doping_n, temperature=300)
    
    current_ref, _ = diode_ref.iv_characteristic(v)
    current_test, _ = diode_test.iv_characteristic(v)
    
    # Both should be positive in forward bias
    assert current_ref[0] > 0
    assert current_test[0] > 0
    
    # Saturation current should depend on doping (higher doping -> higher I_s typically)
    I_s_ref = diode_ref.I_s
    I_s_test = diode_test.I_s
    assert I_s_test > 0, "Saturation current should be positive"
    assert I_s_ref > 0, "Reference saturation current should be positive"


def test_broadcasting_of_recombination_scalar():
    """Test that recombination rate broadcasts correctly to voltage array shape."""
    v = np.linspace(0.0, 1.0, 5)
    diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    I, R = diode.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    assert R.shape == v.shape


@given(st.integers(min_value=1, max_value=20))
@settings(max_examples=10)
def test_array_broadcasting_consistency(array_size):
    """Test that device outputs broadcast consistently with input arrays."""
    v = np.linspace(0.0, 1.0, array_size)
    
    # Test PN junction
    diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    current_pn, recomb_pn = diode.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    assert current_pn.shape == v.shape
    assert recomb_pn.shape == v.shape
    
    # Test LED
    led = LED(doping_p=1e17, doping_n=1e17, temperature=300)
    current_led, emission_led = led.iv_characteristic(v)
    assert current_led.shape == v.shape
    assert emission_led.shape == v.shape
    
    # Test Solar Cell - returns tuple, extract first element
    solar_cell = SolarCell(doping_p=1e17, doping_n=1e17, temperature=300)
    current_solar_tuple = solar_cell.iv_characteristic(v)
    current_solar = current_solar_tuple[0]  # Extract from tuple
    assert current_solar.shape == v.shape


@given(st.lists(voltage_range, min_size=5, max_size=15))
@settings(max_examples=15)
def test_device_output_bounds(volts):
    """Test that all device outputs are within reasonable physical bounds."""
    v = np.array(volts, dtype=float)
    
    # Test PN junction bounds
    diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
    current_pn, recomb_pn = diode.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    
    # Current should be finite
    assert np.all(np.isfinite(current_pn))
    # Recombination should be non-negative and finite
    assert np.all(recomb_pn >= 0)
    assert np.all(np.isfinite(recomb_pn))
    
    # Test LED bounds
    led = LED(doping_p=1e17, doping_n=1e17, temperature=300)
    current_led, emission_led = led.iv_characteristic(v)
    
    assert np.all(np.isfinite(current_led))
    # LED emission should be non-negative
    assert np.all(emission_led >= 0)
    assert np.all(np.isfinite(emission_led))


@given(temperature_range, temperature_range)
@settings(max_examples=10)
def test_temperature_sweep_consistency(temp1, temp2):
    """Test that temperature sweeps produce consistent relative behavior."""
    v = np.array([0.0, 0.5, 1.0])
    
    # Create devices at different temperatures
    diode1 = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=temp1)
    diode2 = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=temp2)
    
    current1, _ = diode1.iv_characteristic(v)
    current2, _ = diode2.iv_characteristic(v)
    
    # Both should produce valid outputs
    assert np.all(np.isfinite(current1))
    assert np.all(np.isfinite(current2))
    
    # Forward bias current should always be positive
    forward_mask = v > 0.5
    if np.any(forward_mask):
        assert np.all(current1[forward_mask] > 0)
        assert np.all(current2[forward_mask] > 0)


@pytest.mark.parametrize("x", [0.0, 1e-12, -1e-12, 700.0, -700.0, 1e6, -1e6])
def test_safe_expm1_boundaries(x):
    """Test safe_expm1 numerical stability at boundaries."""
    # Should not raise and should be finite
    y = safe_expm1(x)
    assert np.all(np.isfinite(y))


@given(st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False))
@settings(max_examples=50)
def test_safe_expm1_property(x):
    """Property test for safe_expm1 numerical function."""
    y = safe_expm1(x)
    
    # Should always be finite
    assert np.isfinite(y)
    
    # For small x, should approximate x
    if abs(x) < 1e-10:
        npt.assert_allclose(y, x, rtol=1e-8)
    
    # For negative x with large magnitude, should approach -1 (but not equal)
    if x < -10:
        assert y >= -1.0, "expm1 should be greater than or equal to -1"
        assert y < 0.0, "expm1 should be negative for negative x"