"""MOS capacitor device model."""

import numpy as np
from typing import Optional, Union
from semiconductor_sim.utils import q, k_B, epsilon_0, DEFAULT_T
from semiconductor_sim.models import srh_recombination
import matplotlib.pyplot as plt
from .base import Device
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style


class MOSCapacitor(Device):
    def __init__(self, doping_p: float, oxide_thickness: float = 1e-6, oxide_permittivity: float = 3.45, area: float = 1e-4, temperature: float = DEFAULT_T, tau_n: float = 1e-6, tau_p: float = 1e-6):
        """
        Initialize the MOS Capacitor.

        Parameters:
            doping_p (float): Acceptor concentration in p-region (cm^-3)
            oxide_thickness (float): Oxide thickness (cm)
            oxide_permittivity (float): Relative permittivity of the oxide
            area (float): Cross-sectional area of the capacitor (cm^2)
            temperature (float): Temperature in Kelvin
            tau_n (float): Electron lifetime (s)
            tau_p (float): Hole lifetime (s)
        """
        super().__init__(area=area, temperature=temperature)
        self.doping_p = doping_p
        self.oxide_thickness = oxide_thickness
        self.oxide_permittivity = oxide_permittivity
        self.tau_n = tau_n
        self.tau_p = tau_p
        self.C_ox = self.calculate_oxide_capacitance()

    def calculate_oxide_capacitance(self) -> float:
        """Calculate the oxide capacitance (C_ox)."""
        epsilon_ox = self.oxide_permittivity * epsilon_0  # F/cm
        C_ox = epsilon_ox * self.area / self.oxide_thickness  # F
        return C_ox

    def depletion_width(self, applied_voltage: np.ndarray) -> np.ndarray:
        """Calculate the depletion width for a given applied voltage."""
        # Built-in potential (simplified)
        V_bi = 0.7  # Volts, adjust as needed
        # Use effective reverse bias magnitude: positive gate voltage increases depletion
        V = V_bi + np.maximum(applied_voltage, 0)
        W = np.sqrt((2 * epsilon_0 * self.oxide_permittivity * V) / (q * self.doping_p))
        return W

    def capacitance(self, applied_voltage: np.ndarray) -> np.ndarray:
        """Calculate the capacitance as a function of applied voltage."""
        # In accumulation, capacitance is C_ox
        # In depletion, capacitance decreases with increasing reverse bias
        # In inversion, capacitance approaches C_ox again

        W = self.depletion_width(applied_voltage)
        C_depl = epsilon_0 * self.oxide_permittivity * self.area / W

        # Simplified model: capacitance transitions from C_ox to C_depl
        C = np.where(applied_voltage < 0, C_depl, self.C_ox)
        return C

    def iv_characteristic(
        self,
        voltage_array: np.ndarray,
        n_conc: Optional[Union[float, np.ndarray]] = None,
        p_conc: Optional[Union[float, np.ndarray]] = None,
    ):
        """Calculate current for `voltage_array`; optionally compute SRH recombination."""
        V_T = k_B * self.temperature / q  # Thermal voltage
        I = self.C_ox * (voltage_array) / V_T  # Simplified current model

        if n_conc is not None and p_conc is not None:
            R_SRH = srh_recombination(
                n_conc, p_conc, temperature=self.temperature, tau_n=self.tau_n, tau_p=self.tau_p
            )
            R_SRH = np.broadcast_to(R_SRH, np.shape(voltage_array))
        else:
            R_SRH = np.zeros_like(voltage_array)

        return np.asarray(I), np.asarray(R_SRH)

    def plot_capacitance_vs_voltage(self, voltage: np.ndarray) -> None:
        """Plot the capacitance-voltage (C-V) characteristics.

        Computes capacitance internally from the provided voltage array.
        """
        capacitance = self.capacitance(voltage)
        use_headless_backend("Agg")
        apply_basic_style()
        plt.figure(figsize=(8,6))
        plt.plot(voltage, capacitance, label='C-V Characteristic')
        plt.title('MOS Capacitor C-V Characteristics')
        plt.xlabel('Gate Voltage (V)')
        plt.ylabel('Capacitance (F)')
        plt.grid(True)
        plt.legend()
        plt.show()

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
        plt.title('MOS Capacitor IV Characteristics')
        plt.show()
