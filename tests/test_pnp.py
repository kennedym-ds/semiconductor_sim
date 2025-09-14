import numpy as np

from semiconductor_sim.devices import PNP


def test_pnp_transfer_monotonic_veb():
    pnp = PNP(doping_p=1e18, doping_n=1e16, early_voltage=50.0, veb_values=[0.6, 0.65, 0.7])
    vce = np.linspace(-5.0, 0.0, 101)
    (ic_grid,) = pnp.iv_characteristic(vce)
    assert ic_grid.shape == (3, vce.size)
    # More forward V_EB should produce larger magnitude negative collector current
    assert np.all(ic_grid[2] < ic_grid[1])
    assert np.all(ic_grid[1] < ic_grid[0])


def test_pnp_early_effect_negative_slope():
    pnp = PNP(doping_p=1e18, doping_n=1e16, early_voltage=50.0, veb_values=[0.7])
    vce = np.array([-5.0, -2.0, -1.0, 0.0])
    (ic_grid,) = pnp.iv_characteristic(vce)
    ic = ic_grid[0]
    # As V_CE increases towards 0 (less negative), magnitude of current reduces (less negative values)
    assert np.all(np.diff(ic) > 0)
