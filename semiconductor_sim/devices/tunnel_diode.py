"""Tunnel diode device model."""

import numpy as np
from typing import Optional, Tuple, Union
from semiconductor_sim.utils import q, k_B, DEFAULT_T
from semiconductor_sim.models import srh_recombination
from semiconductor_sim.utils.numerics import safe_expm1
from .base import Device
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style


class TunnelDiode(Device):
    def __init__(self, doping_p: float, doping_n: float, area: float = 1e-4, temperature: float = DEFAULT_T, tau_n: float = 1e-6, tau_p: float = 1e-6) -> None:
        """
        Initialize the Tunnel Diode.
        
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
        self.Eg = 0.7  # Bandgap energy for Tunnel Diode (eV), adjust as needed

    def calculate_saturation_current(self) -> float:
        """Calculate the saturation current (I_s) considering temperature."""
        # High doping concentrations lead to high I_s
        D_n = 30  # Electron diffusion coefficient (cm^2/s)
        D_p = 12  # Hole diffusion coefficient (cm^2/s)
        L_n = 1e-4  # Electron diffusion length (cm)
        L_p = 1e-4  # Hole diffusion length (cm)
        n_i = 1e10 * (self.temperature / DEFAULT_T)**1.5  # Intrinsic carrier concentration
        
        I_s = q * self.area * n_i**2 * (
            (D_p / (L_p * self.doping_n)) +
            (D_n / (L_n * self.doping_p))
        )
        return I_s

    def iv_characteristic(self, voltage_array: np.ndarray, n_conc: Optional[Union[float, np.ndarray]] = None, p_conc: Optional[Union[float, np.ndarray]] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate the current for a given array of voltages, including SRH recombination.

        Parameters:
            voltage_array: Array of voltage values (V)
            n_conc: Electron concentration (cm^-3)
            p_conc: Hole concentration (cm^-3)

        Returns:
            Tuple of `(current_array, recombination_array)` with shape matching `voltage_array`.
        """
        V_T = k_B * self.temperature / q  # Thermal voltage
        # Use a simplified exponential IV to ensure correct sign in reverse bias
        I = self.I_s * safe_expm1(voltage_array / V_T)
        
        if n_conc is not None and p_conc is not None:
            R_SRH = srh_recombination(n_conc, p_conc, temperature=self.temperature, tau_n=self.tau_n, tau_p=self.tau_p)
            R_SRH = np.broadcast_to(R_SRH, np.shape(voltage_array))
        else:
            R_SRH = np.zeros_like(voltage_array)

        return np.asarray(I), np.asarray(R_SRH)

    def plot_iv_characteristic(self, voltage: np.ndarray, current: np.ndarray, recombination: Optional[np.ndarray] = None) -> None:
        """Plot the IV characteristics and optionally the recombination rate."""
        use_headless_backend("Agg")
        apply_basic_style()
        fig, ax1 = plt.subplots(figsize=(8,6))

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
        plt.title('Tunnel Diode IV Characteristics')
        plt.show()
