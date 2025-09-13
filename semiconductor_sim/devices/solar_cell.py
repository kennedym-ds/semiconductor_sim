# semiconductor_sim/devices/solar_cell.py

import numpy as np
from typing import Optional, Tuple
from semiconductor_sim.utils import q, k_B, DEFAULT_T
from semiconductor_sim.utils.numerics import safe_expm1
import matplotlib.pyplot as plt
from .base import Device
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style


class SolarCell(Device):
    def __init__(
        self,
        doping_p: float,
        doping_n: float,
        area: float = 1e-4,
        light_intensity: float = 1.0,
        temperature: float = DEFAULT_T,
        R_s: float = 0.0,
        R_sh: float = np.inf,
        enable_parasitics: bool = False,
    ) -> None:
        """
        Initialize the Solar Cell device.

        Parameters:
            doping_p (float): Acceptor concentration in p-region (cm^-3)
            doping_n (float): Donor concentration in n-region (cm^-3)
            area (float): Cross-sectional area of the solar cell (cm^2)
            light_intensity (float): Incident light intensity (arbitrary units)
            temperature (float): Temperature in Kelvin
            R_s: Series resistance (Ω)
            R_sh: Shunt resistance (Ω)
            enable_parasitics: Enable parasitic effects
        """
        super().__init__(area=area, temperature=temperature, R_s=R_s, R_sh=R_sh, enable_parasitics=enable_parasitics)
        self.doping_p = doping_p
        self.doping_n = doping_n
        self.light_intensity = light_intensity
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
        V_oc = V_T * np.log((self.I_sc / 1e-12) + 1)  # Assuming I_s = 1e-12 A
        return float(V_oc)

    def iv_characteristic(
        self,
        voltage_array: np.ndarray,
        n_conc: Optional["np.ndarray | float"] = None,
        p_conc: Optional["np.ndarray | float"] = None,
    ) -> Tuple[np.ndarray, ...]:
        """
        Calculate the current for a given array of voltages under illumination.

        Parameters:
            voltage_array (np.ndarray): Array of voltage values (V)

        Returns:
            Tuple containing one element:
            - current_array (np.ndarray): Array of current values (A)
        """
        I_ideal = self.I_sc - 1e-12 * safe_expm1(
            voltage_array / (k_B * self.temperature / q)
        )

        # Apply parasitics if enabled
        if self.enable_parasitics:
            I = self._apply_parasitics(voltage_array, I_ideal)
        else:
            I = I_ideal
            
        return (np.asarray(I),)

    def plot_iv_characteristic(self, voltage, current):
        """
        Plot the IV characteristics of the solar cell.

        Parameters:
            voltage (np.ndarray): Voltage values (V)
            current (np.ndarray): Current values (A)
        """
        use_headless_backend("Agg")
        apply_basic_style()
        plt.figure(figsize=(8,6))
        plt.plot(voltage, current, label='Solar Cell IV')
        plt.title('Solar Cell IV Characteristics')
        plt.xlabel('Voltage (V)')
        plt.ylabel('Current (A)')
        plt.grid(True)
        plt.legend()
        plt.show()
