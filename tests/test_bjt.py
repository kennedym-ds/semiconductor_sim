import numpy as np

from semiconductor_sim.devices import BJT

NANOAMP_THRESHOLD = 5e-9


def test_bjt_output_characteristics_monotonic_vbe():
    bjt = BJT(doping_p=1e16, doping_n=1e18, early_voltage=50.0, vbe_values=[0.6, 0.65, 0.7])
    vce = np.linspace(0.0, 5.0, 101)
    (ic_grid,) = bjt.iv_characteristic(vce)
    assert ic_grid.shape == (3, vce.size)
    # Higher V_BE should produce higher collector current across V_CE
    assert np.all(ic_grid[2] > ic_grid[1])
    assert np.all(ic_grid[1] > ic_grid[0])


def test_bjt_early_effect_positive_slope():
    bjt = BJT(doping_p=1e16, doping_n=1e18, early_voltage=50.0, vbe_values=[0.7])
    vce = np.array([0.0, 1.0, 2.0, 5.0])
    (ic_grid,) = bjt.iv_characteristic(vce)
    ic = ic_grid[0]
    # With finite Early voltage, current should increase with V_CE in forward-active region
    assert np.all(np.diff(ic) > 0)


def test_bjt_near_cutoff_small_current():
    bjt = BJT(doping_p=1e16, doping_n=1e18, early_voltage=50.0, vbe_values=[0.3])
    vce = np.linspace(0.0, 1.0, 21)
    (ic_grid,) = bjt.iv_characteristic(vce)
    ic = ic_grid[0]
    # For low V_BE << ~0.6 V, current should be very small (nanoamp scale)
    assert float(ic.max()) < NANOAMP_THRESHOLD


def test_bjt_no_early_effect_for_nonpositive_va():
    # early_voltage <= 0 should behave like infinite Early voltage (flat vs V_CE)
    for va in [0.0, -10.0, float("inf"), float("nan")]:
        bjt = BJT(doping_p=1e16, doping_n=1e18, early_voltage=va, vbe_values=[0.7])
        vce = np.linspace(0.0, 5.0, 6)
        (ic_grid,) = bjt.iv_characteristic(vce)
        ic = ic_grid[0]
        assert np.allclose(ic, ic[0], rtol=0.0, atol=1e-18)
