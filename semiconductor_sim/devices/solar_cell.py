"""Solar cell device model."""

import matplotlib.pyplot as plt
import numpy as np

from semiconductor_sim.materials import Material
from semiconductor_sim.utils import DEFAULT_T, k_B, q
from semiconductor_sim.utils.numerics import safe_expm1
from semiconductor_sim.utils.plotting import apply_basic_style, use_headless_backend

from .base import Device


class SolarCell(Device):
    def __init__(
        self,
        doping_p: float,
        doping_n: float,
        area: float = 1e-4,
        light_intensity: float = 1.0,
        temperature: float = DEFAULT_T,
        material: Material | None = None,
    ) -> None:
        """
        Initialize the Solar Cell device.

        Parameters:
            doping_p (float): Acceptor concentration in p-region (cm^-3)
            doping_n (float): Donor concentration in n-region (cm^-3)
            area (float): Cross-sectional area of the solar cell (cm^2)
            light_intensity (float): Incident light intensity (arbitrary units)
            temperature (float): Temperature in Kelvin
        """
        super().__init__(area=area, temperature=temperature)
        self.doping_p = doping_p
        self.doping_n = doping_n
        self.light_intensity = light_intensity
        self.material = material
        self.I_s = self.calculate_dark_saturation_current()
        self.I_sc = self.calculate_short_circuit_current()
        self.V_oc = self.calculate_open_circuit_voltage()

    def calculate_short_circuit_current(self) -> float:
        """
        Calculate the short-circuit current (I_sc) based on light intensity.
        """
        # Simplified assumption: I_sc proportional to light intensity
        I_sc = q * self.area * self.light_intensity * 1e12  # A
        return float(I_sc)

    def calculate_open_circuit_voltage(self) -> float:
        """
        Calculate the open-circuit voltage (V_oc) using the diode equation.
        """
        V_T = k_B * self.temperature / q
        V_oc = V_T * np.log((self.I_sc / max(self.I_s, 1e-30)) + 1)
        return float(V_oc)

    def calculate_dark_saturation_current(self) -> float:
        """Calculate dark saturation current using material (if provided)."""
        if self.material is not None:
            n_i = float(np.asarray(self.material.ni(self.temperature)))
        else:
            n_i = 1.5e10 * (self.temperature / DEFAULT_T) ** 1.5
        # Use representative transport constants as in PNJunction/LED for I_s form
        D_p, D_n = 10.0, 25.0
        L_p, L_n = 5e-4, 5e-4
        I_s = (
            q * self.area * n_i**2 * ((D_p / (L_p * self.doping_n)) + (D_n / (L_n * self.doping_p)))
        )
        return float(I_s)

    def iv_characteristic(
        self,
        voltage_array: np.ndarray,
        n_conc: np.ndarray | float | None = None,
        p_conc: np.ndarray | float | None = None,
    ) -> tuple[np.ndarray, ...]:
        """
        Calculate the current for a given array of voltages under illumination.

        Parameters:
            voltage_array (np.ndarray): Array of voltage values (V)

        Returns:
            Tuple containing one element:
            - current_array (np.ndarray): Array of current values (A)
        """
        I = self.I_sc - self.I_s * safe_expm1(voltage_array / (k_B * self.temperature / q))
        return (np.asarray(I),)

    def __repr__(self) -> str:
        return (
            f"SolarCell(doping_p={self.doping_p}, doping_n={self.doping_n}, area={self.area}, "
            f"light_intensity={self.light_intensity}, temperature={self.temperature}, "
            f"I_s={self.I_s}, material={self.material.symbol if self.material else None})"
        )

    def plot_iv_characteristic(self, voltage, current):
        """
        Plot the IV characteristics of the solar cell.

        Parameters:
            voltage (np.ndarray): Voltage values (V)
            current (np.ndarray): Current values (A)
        """
        use_headless_backend("Agg")
        apply_basic_style()
        plt.figure(figsize=(8, 6))
        plt.plot(voltage, current, label='Solar Cell IV')
        plt.title('Solar Cell IV Characteristics')
        plt.xlabel('Voltage (V)')
        plt.ylabel('Current (A)')
        plt.grid(True)
        plt.legend()
        plt.show()
