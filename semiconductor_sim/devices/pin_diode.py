from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from semiconductor_sim.materials import Material
from semiconductor_sim.utils import DEFAULT_T, k_B, q
from semiconductor_sim.utils.numerics import safe_expm1

from .base import Device


class PINDiode(Device):
    """Teaching-simple PIN diode model.

    DC I–V is modeled using an ideal diode with an effective saturation
    current that includes edge diffusion (PN-like) plus SRH generation in
    the intrinsic region. An optional series resistance captures ohmic drop.

    Notes:
    - This is a compact, didactic model; it omits high-level injection,
      conductivity modulation, and dynamic charge storage effects.
    - Units follow the package convention: cm, cm^2, cm^-3, K.
    """

    def __init__(
        self,
        doping_p: float,
        doping_n: float,
        *,
        intrinsic_width_cm: float = 1e-4,
        area: float = 1e-4,
        temperature: float = DEFAULT_T,
        D_n: float = 25.0,
        D_p: float = 10.0,
        L_n: float = 5e-4,
        L_p: float = 5e-4,
        tau_n: float = 1e-6,
        tau_p: float = 1e-6,
        material: Material | None = None,
        series_resistance_ohm: float | None = None,
    ) -> None:
        super().__init__(area=area, temperature=temperature)
        if intrinsic_width_cm <= 0:
            raise ValueError("intrinsic_width_cm must be > 0")
        self.doping_p = float(doping_p)
        self.doping_n = float(doping_n)
        self.intrinsic_width_cm = float(intrinsic_width_cm)
        self.D_n = float(D_n)
        self.D_p = float(D_p)
        self.L_n = float(L_n)
        self.L_p = float(L_p)
        self.tau_n = float(tau_n)
        self.tau_p = float(tau_p)
        self.material = material
        self.series_resistance_ohm = (
            float(series_resistance_ohm)
            if series_resistance_ohm is not None and series_resistance_ohm > 0
            else None
        )

    def _intrinsic_density(self) -> float:
        if self.material is not None:
            return float(np.asarray(self.material.ni(self.temperature)))
        return float(1.5e10 * (self.temperature / DEFAULT_T) ** 1.5)

    def saturation_current(self) -> float:
        """Effective saturation current: diffusion at edges + SRH generation in i-region.

        Diffusion (edges):
            I_s,PN = q A n_i^2 [ Dp/(Lp Nd) + Dn/(Ln Na) ]

        SRH generation current (i-region, reverse-dominated term):
            I_gen ≈ q A n_i W_i / (2 τ_eff)
        """
        n_i = self._intrinsic_density()
        Is_pn = (
            q
            * self.area
            * (n_i**2)
            * ((self.D_p / (self.L_p * self.doping_n)) + (self.D_n / (self.L_n * self.doping_p)))
        )
        tau_eff = max(min(self.tau_n, self.tau_p), 1e-15)
        Is_gen = q * self.area * n_i * self.intrinsic_width_cm / (2.0 * tau_eff)
        return float(Is_pn + Is_gen)

    def iv_characteristic(
        self,
        voltage_array: NDArray[np.floating],
        n_conc: float | NDArray[np.floating] | None = None,
        p_conc: float | NDArray[np.floating] | None = None,
    ) -> tuple[NDArray[np.floating]]:
        V = np.asarray(voltage_array, dtype=float)
        Vt = k_B * self.temperature / q
        Is = self.saturation_current()

        if self.series_resistance_ohm is None:
            I = Is * safe_expm1(V / Vt)
            return (I,)

        # Solve I = Is*expm1((V - I*Rs)/Vt) with simple Newton iterations
        Rs = float(self.series_resistance_ohm)
        I_out = np.zeros_like(V)
        for i, v in enumerate(V):
            Ii = Is * safe_expm1(v / Vt)
            for _ in range(50):
                f = Ii - Is * safe_expm1((v - Ii * Rs) / Vt)
                # derivative of safe_expm1(x) is exp(x)
                exp_term = np.exp((v - Ii * Rs) / Vt)
                df = 1.0 - Is * (-Rs / Vt) * exp_term
                step = f / df
                Ii = Ii - step
                if abs(step) < max(1e-18, 1e-6 * max(1.0, abs(Ii))):
                    break
            I_out[i] = Ii
        return (I_out,)
