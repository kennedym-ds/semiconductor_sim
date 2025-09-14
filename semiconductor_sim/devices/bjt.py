"""Bipolar Junction Transistor (BJT) device model (teaching-simple).

Implements a forward-active Ebers–Moll style collector current with Early effect:

    I_C(V_CE, V_BE) = I_S * exp(V_BE / V_T) * (1 + V_CE / V_A)

This simple model generates output characteristics over a sweep of V_CE for
one or more specified V_BE values.

Assumptions:
- Forward-active region (no explicit saturation modeling beyond non-negativity).
- Saturation current I_S computed similar to PN-junction diffusion current.
- Early effect included via Early voltage V_A (> 0 gives finite output conductance).
"""

from __future__ import annotations

import numpy as np

from semiconductor_sim.materials import Material
from semiconductor_sim.utils import DEFAULT_T, k_B, q
from semiconductor_sim.utils.numerics import safe_expm1

from .base import Device


class BJT(Device):
    def __init__(
        self,
        doping_p: float,
        doping_n: float,
        *,
        area: float = 1e-4,
        temperature: float = DEFAULT_T,
        early_voltage: float = 50.0,
        vbe_values: np.ndarray | list[float] | tuple[float, ...] = (0.6, 0.65, 0.7, 0.75, 0.8),
        material: Material | None = None,
    ) -> None:
        """Initialize an NPN BJT model.

        Parameters:
            doping_p: Base acceptor concentration (cm^-3)
            doping_n: Emitter donor concentration (cm^-3)
            area: Effective emitter area (cm^2)
            temperature: Temperature in Kelvin
            early_voltage: Early voltage V_A (V), sets output conductance
            vbe_values: Iterable of base–emitter voltages (V) for characteristics
            material: Optional material providing temperature-dependent n_i(T)
        """
        super().__init__(area=area, temperature=temperature)
        self.doping_p = float(doping_p)
        self.doping_n = float(doping_n)
        self.early_voltage = float(early_voltage)
        self.vbe_values = np.asarray(vbe_values, dtype=float).ravel()
        self.material = material
        self.I_s = self._saturation_current()

    def _intrinsic_density(self) -> float:
        if self.material is not None:
            return float(np.asarray(self.material.ni(self.temperature)))
        return float(1.5e10 * (self.temperature / DEFAULT_T) ** 1.5)

    def _saturation_current(self) -> float:
        # Representative transport constants (aligned with PNJunctionDiode defaults)
        D_p, D_n = 10.0, 25.0
        L_p, L_n = 5e-4, 5e-4
        n_i = self._intrinsic_density()
        I_s = (
            q * self.area * n_i**2 * ((D_p / (L_p * self.doping_n)) + (D_n / (L_n * self.doping_p)))
        )
        return float(I_s)

    def iv_characteristic(
        self,
        voltage_array: np.ndarray,
        n_conc: float | np.ndarray | None = None,
        p_conc: float | np.ndarray | None = None,
    ) -> tuple[np.ndarray, ...]:
        """Compute collector current for a sweep of V_CE at configured V_BE values.

        Parameters:
            voltage_array: Array of collector–emitter voltages V_CE (V)

        Returns:
            (I_C,)
            where I_C has shape (N_VBE, N_VCE) corresponding to self.vbe_values
            by rows and the provided V_CE array by columns.
        """
        V_CE = np.asarray(voltage_array, dtype=float).ravel()
        V_T = k_B * self.temperature / q

        # Compute exp(V_BE / V_T) safely to handle small/large values
        exp_vbe = safe_expm1(self.vbe_values / V_T) + 1.0  # equals exp(V_BE / V_T)
        # Outer products to form grid over (V_BE, V_CE)
        term_vbe = exp_vbe[:, None]
        va = float(self.early_voltage)
        if not np.isfinite(va) or va <= 0.0:
            term_early = np.ones((self.vbe_values.size, V_CE.size))
        else:
            term_early = 1.0 + (V_CE[None, :] / va)

        I_C = self.I_s * term_vbe * term_early
        I_C = np.maximum(I_C, 0.0)
        return (I_C,)

    def __repr__(self) -> str:
        return (
            f"BJT(doping_p={self.doping_p}, doping_n={self.doping_n}, area={self.area}, "
            f"temperature={self.temperature}, early_voltage={self.early_voltage}, "
            f"n_vbe={self.vbe_values.size})"
        )


class PNP(Device):
    def __init__(
        self,
        doping_p: float,
        doping_n: float,
        *,
        area: float = 1e-4,
        temperature: float = DEFAULT_T,
        early_voltage: float = 50.0,
        veb_values: np.ndarray | list[float] | tuple[float, ...] = (0.6, 0.65, 0.7, 0.75, 0.8),
        material: Material | None = None,
    ) -> None:
        """Initialize a PNP BJT model (teaching-simple).

        Bias/sign conventions:
        - Forward-active typically uses negative V_CE.
        - We accept a sweep of V_CE (can be negative) and a list of V_EB values.
        - Collector current is returned negative for forward conduction.
        """
        super().__init__(area=area, temperature=temperature)
        self.doping_p = float(doping_p)
        self.doping_n = float(doping_n)
        self.early_voltage = float(early_voltage)
        self.veb_values = np.asarray(veb_values, dtype=float).ravel()
        self.material = material
        # reuse the same diffusion-like saturation current expression
        self.I_s = self._saturation_current()

    def _intrinsic_density(self) -> float:
        if self.material is not None:
            return float(np.asarray(self.material.ni(self.temperature)))
        return float(1.5e10 * (self.temperature / DEFAULT_T) ** 1.5)

    def _saturation_current(self) -> float:
        D_p, D_n = 10.0, 25.0
        L_p, L_n = 5e-4, 5e-4
        n_i = self._intrinsic_density()
        I_s = (
            q * self.area * n_i**2 * ((D_p / (L_p * self.doping_n)) + (D_n / (L_n * self.doping_p)))
        )
        return float(I_s)

    def iv_characteristic(
        self,
        voltage_array: np.ndarray,
        n_conc: float | np.ndarray | None = None,
        p_conc: float | np.ndarray | None = None,
    ) -> tuple[np.ndarray, ...]:
        """Compute collector current for a sweep of V_CE at configured V_EB values.

        Returns:
            (I_C,)
            where I_C has shape (N_VEB, N_VCE) corresponding to self.veb_values by rows.
        """
        V_CE = np.asarray(voltage_array, dtype=float).ravel()
        V_T = k_B * self.temperature / q

        exp_veb = safe_expm1(self.veb_values / V_T) + 1.0
        term_veb = exp_veb[:, None]
        va = float(self.early_voltage)
        if not np.isfinite(va) or va <= 0.0:
            term_early = np.ones((self.veb_values.size, V_CE.size))
        else:
            term_early = 1.0 + ((-V_CE)[None, :] / va)

        I_C_mag = self.I_s * term_veb * term_early
        I_C = -I_C_mag
        I_C = np.minimum(I_C, 0.0)
        return (I_C,)

    def __repr__(self) -> str:
        return (
            f"PNP(doping_p={self.doping_p}, doping_n={self.doping_n}, area={self.area}, "
            f"temperature={self.temperature}, early_voltage={self.early_voltage}, "
            f"n_veb={self.veb_values.size})"
        )
