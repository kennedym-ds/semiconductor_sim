"""Photodiode device model (teaching-simple).

Modeled as an illuminated diode: I(V) = -I_ph + I_s * (exp(V / V_T) - 1).

Assumptions:
- Constant responsivity over spectrum; photocurrent proportional to irradiance.
- Uses same dark-saturation current form as PN junction device.
- Optional `material` to compute intrinsic carrier density dependence.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from semiconductor_sim.materials import Material
from semiconductor_sim.utils import DEFAULT_T, k_B, q
from semiconductor_sim.utils.numerics import safe_expm1

from .base import Device


class Photodiode(Device):
    def __init__(
        self,
        doping_p: float,
        doping_n: float,
        area: float = 1e-4,
        irradiance_W_per_cm2: float = 1e-3,
        responsivity_A_per_W: float = 0.5,
        temperature: float = DEFAULT_T,
        material: Material | None = None,
    ) -> None:
        """Initialize a photodiode.

        Parameters:
            doping_p: Acceptor concentration in p-region (cm^-3)
            doping_n: Donor concentration in n-region (cm^-3)
            area: Active area of the photodiode (cm^2)
            irradiance_W_per_cm2: Incident optical power density (W/cm^2)
            responsivity_A_per_W: Responsivity (A/W)
            temperature: Temperature in Kelvin
            material: Optional material for intrinsic density model
        """
        super().__init__(area=area, temperature=temperature)
        self.doping_p = float(doping_p)
        self.doping_n = float(doping_n)
        self.irradiance_W_per_cm2 = float(irradiance_W_per_cm2)
        self.responsivity_A_per_W = float(responsivity_A_per_W)
        self.material = material

    def _intrinsic_density(self) -> float:
        if self.material is not None:
            return float(np.asarray(self.material.ni(self.temperature)))
        return float(1.5e10 * (self.temperature / DEFAULT_T) ** 1.5)

    def _dark_saturation_current(self) -> float:
        # Representative transport constants (consistent with PNJunction/SolarCell)
        D_p, D_n = 10.0, 25.0
        L_p, L_n = 5e-4, 5e-4
        n_i = self._intrinsic_density()
        I_s = (
            q * self.area * n_i**2 * ((D_p / (L_p * self.doping_n)) + (D_n / (L_n * self.doping_p)))
        )
        return float(I_s)

    def _photocurrent(self) -> float:
        # I_ph = Responsivity * IncidentPower; IncidentPower = irradiance * area
        return float(self.responsivity_A_per_W * self.irradiance_W_per_cm2 * self.area)

    def iv_characteristic(
        self,
        voltage_array: npt.NDArray[np.floating],
        n_conc: float | npt.NDArray[np.floating] | None = None,
        p_conc: float | npt.NDArray[np.floating] | None = None,
    ) -> tuple[npt.NDArray[np.floating], ...]:
        """Return the illuminated I–V curve as a tuple with current array.

        Returns:
            (current_array,)
        """
        V_T = k_B * self.temperature / q
        I_s = self._dark_saturation_current()
        I_ph = self._photocurrent()
        I = -I_ph + I_s * safe_expm1(voltage_array / V_T)
        return (np.asarray(I, dtype=float),)
