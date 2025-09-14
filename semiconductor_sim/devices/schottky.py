from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from semiconductor_sim.devices.base import Device
from semiconductor_sim.utils.constants import k_B, q

BARRIER_MIN_EV = 0.1
BARRIER_MAX_EV = 2.0
IDEALITY_MIN = 1.0
IDEALITY_MAX = 2.0


class SchottkyDiode(Device):
    """Teaching-simple Schottky diode using thermionic emission.

    I = A * A** * T^2 * exp(-qΦ_B/kT) * [exp(qV/nkT) - 1]

    Parameters
    - barrier_height_eV: Φ_B in eV
    - ideality: n (default 1.1)
    - area: junction area in cm^2 (default 1e-4)
    - temperature: K
    - A_star: effective Richardson constant (A/cm^2/K^2), default 120 for Si
    """

    def __init__(
        self,
        barrier_height_eV: float = 0.7,
        ideality: float = 1.1,
        *,
        area: float = 1e-4,
        temperature: float = 300.0,
        A_star: float = 120.0,
        series_resistance_ohm: float | None = None,
    ) -> None:
        super().__init__(area=area, temperature=temperature)
        if not (BARRIER_MIN_EV <= barrier_height_eV <= BARRIER_MAX_EV):
            raise ValueError(f"barrier_height_eV out of range [{BARRIER_MIN_EV}, {BARRIER_MAX_EV}]")
        if not (IDEALITY_MIN <= ideality <= IDEALITY_MAX):
            raise ValueError(f"ideality should be in [{IDEALITY_MIN}, {IDEALITY_MAX}]")
        self.barrier_height_eV = barrier_height_eV
        self.ideality = ideality
        self.A_star = A_star
        self.series_resistance_ohm = (
            series_resistance_ohm if series_resistance_ohm and series_resistance_ohm > 0 else None
        )

    def saturation_current(self) -> float:
        T = self.temperature
        kT_eV = 8.617333262145e-5 * T
        pref = self.area * self.A_star * (T**2)
        return float(pref * np.exp(-self.barrier_height_eV / kT_eV))

    def iv_characteristic(
        self, voltage_array: NDArray[np.floating], n_conc=None, p_conc=None
    ) -> tuple[NDArray[np.floating]]:
        V = np.asarray(voltage_array, dtype=float)
        Is = self.saturation_current()
        n = self.ideality
        T = self.temperature
        if self.series_resistance_ohm is None:
            I = Is * (np.exp(q * V / (n * k_B * T)) - 1.0)
            return (I,)

        # Solve I = Is * (exp(q(V - I*Rs)/(n kT)) - 1) using Newton's method
        Rs = float(self.series_resistance_ohm)
        a = q / (n * k_B * T)
        I_out = np.zeros_like(V)
        for i, v in enumerate(V):
            Ii = Is * (np.exp(a * v) - 1.0)
            for _ in range(50):
                f = Ii - Is * (np.exp(a * (v - Ii * Rs)) - 1.0)
                df = 1.0 - Is * (-a * Rs) * np.exp(a * (v - Ii * Rs))
                step = f / df
                Ii = Ii - step
                if abs(step) < max(1e-18, 1e-6 * max(1.0, abs(Ii))):
                    break
            I_out[i] = Ii
        return (I_out,)
