"""Varactor diode device model."""

import matplotlib.pyplot as plt
import numpy as np

from semiconductor_sim.models import srh_recombination
from semiconductor_sim.utils import DEFAULT_T, k_B, q
from semiconductor_sim.utils.numerics import safe_expm1
from semiconductor_sim.utils.plotting import apply_basic_style, use_headless_backend

from .base import Device


class VaractorDiode(Device):
    def __init__(
        self,
        doping_p: float,
        doping_n: float,
        area: float = 1e-4,
        temperature: float = DEFAULT_T,
        tau_n: float = 1e-6,
        tau_p: float = 1e-6,
    ) -> None:
        """
        Initialize the Varactor Diode.

        Parameters:
            doping_p (float): Acceptor concentration in p-region (cm^-3)
            doping_n (float): Donor concentration in n-region (cm^-3)
            area (float): Cross-sectional area of the diode (cm^2)
            temperature (float): Temperature in Kelvin
            tau_n (float): Electron lifetime (s)
            tau_p (float): Hole lifetime (s)
        """
        super().__init__(area=area, temperature=temperature)
        self.doping_p = doping_p
        self.doping_n = doping_n
        self.tau_n = tau_n
        self.tau_p = tau_p
        self.I_s = self.calculate_saturation_current()

    def calculate_saturation_current(self) -> float:
        """Calculate the saturation current (I_s) considering temperature."""
        D_n = 25  # Electron diffusion coefficient (cm^2/s)
        D_p = 10  # Hole diffusion coefficient (cm^2/s)
        L_n = 5e-4  # Electron diffusion length (cm)
        L_p = 5e-4  # Hole diffusion length (cm)
        n_i = 1.5e10 * (self.temperature / DEFAULT_T) ** 1.5  # Intrinsic carrier concentration

        I_s = (
            q * self.area * n_i**2 * ((D_p / (L_p * self.doping_n)) + (D_n / (L_n * self.doping_p)))
        )
        return float(I_s)

    def capacitance(self, reverse_voltage: float | np.ndarray) -> float | np.ndarray:
        """Calculate the junction capacitance for a given reverse voltage."""
        # Permittivity of silicon (approx.)
        epsilon_s = 11.7 * 8.854e-14  # F/cm

        # Built-in potential (simplified)
        V_bi = 0.7  # Volts, adjust as needed

        # Calculate depletion width
        W = np.sqrt(
            (2 * epsilon_s * (V_bi + reverse_voltage))
            / (q * (self.doping_p + self.doping_n) / (self.doping_p * self.doping_n))
        )

        # Junction capacitance per unit area
        C_j_per_area = epsilon_s / W  # F/cm^2

        # Total junction capacitance
        C_j = C_j_per_area * self.area  # F

        return C_j

    def iv_characteristic(
        self,
        voltage_array: np.ndarray,
        n_conc: float | np.ndarray | None = None,
        p_conc: float | np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculate current for `voltage_array`, including SRH recombination
        if concentrations are provided.

        Returns `(I, R_SRH)` matching the shape of `voltage_array`.
        """
        V_T = k_B * self.temperature / q  # Thermal voltage
        I = self.I_s * safe_expm1(voltage_array / V_T)

        if n_conc is not None and p_conc is not None:
            R_SRH = srh_recombination(
                n_conc, p_conc, temperature=self.temperature, tau_n=self.tau_n, tau_p=self.tau_p
            )
            R_SRH = np.broadcast_to(R_SRH, np.shape(voltage_array))
        else:
            R_SRH = np.zeros_like(voltage_array)

        return np.asarray(I), np.asarray(R_SRH)

    def plot_iv_characteristic(
        self, voltage: np.ndarray, current: np.ndarray, recombination: np.ndarray | None = None
    ) -> None:
        """Plot the IV characteristics and optionally the recombination rate."""
        use_headless_backend("Agg")
        apply_basic_style()
        fig, ax1 = plt.subplots(figsize=(8, 6))

        color = 'tab:blue'
        ax1.set_xlabel('Voltage (V)')
        ax1.set_ylabel('Current (A)', color=color)
        ax1.plot(voltage, current, color=color, label='IV Characteristic')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True)

        if recombination is not None:
            ax2 = ax1.twinx()
            color = 'tab:green'
            ax2.set_ylabel('Recombination Rate (cm$^{-3}$ s$^{-1}$)', color=color)
            ax2.plot(voltage, recombination, color=color, label='SRH Recombination')
            ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()
        plt.title('Varactor Diode IV Characteristics')
        plt.show()

    def plot_capacitance_vs_voltage(self, voltage_array: np.ndarray) -> None:
        """Plot the junction capacitance as a function of reverse voltage."""
        C_j = self.capacitance(voltage_array)

        use_headless_backend("Agg")
        apply_basic_style()
        plt.figure(figsize=(8, 6))
        plt.plot(voltage_array, C_j, label='Junction Capacitance')
        plt.title('Varactor Diode Junction Capacitance vs. Reverse Voltage')
        plt.xlabel('Reverse Voltage (V)')
        plt.ylabel('Capacitance (F)')
        plt.grid(True)
        plt.legend()
        plt.show()
