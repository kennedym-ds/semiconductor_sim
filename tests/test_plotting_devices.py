"""Plotting smoke tests for Matplotlib-based devices (headless-safe)."""

import numpy as np

from semiconductor_sim import (
    MOSCapacitor,
    PNJunctionDiode,
    SolarCell,
    TunnelDiode,
    VaractorDiode,
    ZenerDiode,
)


def test_pn_plot_iv_with_recombination():
    d = PNJunctionDiode(1e17, 1e17)
    v = np.linspace(-0.2, 0.8, 5)
    I, R = d.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    d.plot_iv_characteristic(v, I, R)


def test_tunnel_plot_iv_with_recombination():
    d = TunnelDiode(1e19, 1e19)
    v = np.linspace(-0.2, 0.2, 5)
    I, R = d.iv_characteristic(v, n_conc=1e18, p_conc=1e18)
    d.plot_iv_characteristic(v, I, R)


def test_mos_plot_iv_and_cv():
    m = MOSCapacitor(1e17)
    v = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    I, R = m.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    m.plot_iv_characteristic(v, I, R)
    m.plot_capacitance_vs_voltage(v)


def test_varactor_plot_iv_and_cj():
    d = VaractorDiode(1e17, 1e17)
    v = np.array([-0.5, 0.0, 0.5, 1.0])
    I, R = d.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    d.plot_iv_characteristic(v, I, R)
    d.plot_capacitance_vs_voltage(np.array([0.1, 0.5, 1.0]))


def test_zener_plot_iv_with_recombination():
    z = ZenerDiode(1e17, 1e17, zener_voltage=5.0)
    v = np.array([4.5, 5.0, 5.5])
    I, R = z.iv_characteristic(v, n_conc=1e16, p_conc=1e16)
    z.plot_iv_characteristic(v, I, R)


def test_solar_plot_iv():
    s = SolarCell(1e17, 1e17, light_intensity=1.0)
    v = np.linspace(0.0, 0.8, 6)
    (I,) = s.iv_characteristic(v)
    s.plot_iv_characteristic(v, I)
