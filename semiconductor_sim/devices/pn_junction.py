"""PN Junction diode device model."""

import numpy as np
from typing import Optional, Tuple, Union

from semiconductor_sim.utils import DEFAULT_T, k_B, q
from semiconductor_sim.utils import (
    intrinsic_carrier_concentration,
    diffusion_coefficient_temperature,
)
from semiconductor_sim.models import srh_recombination
from semiconductor_sim.utils.numerics import safe_expm1
import matplotlib.pyplot as plt
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style

from .base import Device


class PNJunctionDiode(Device):
    """PN Junction diode device model.

    Assumptions:
    - Ideal diode equation with temperature-dependent I_s
    - SRH recombination with default mid-gap trap (n1≈p1≈n_i)
    - Improved temperature dependencies for carrier concentration and mobility
    - Optional parasitics: series resistance R_s and shunt resistance R_sh
    - Units: cm, cm^2, cm^3, K; q in C, k_B in J/K
    """
    def __init__(
        self,
        doping_p: float,
        doping_n: float,
        area: float = 1e-4,
        temperature: float = DEFAULT_T,
        tau_n: float = 1e-6,
        tau_p: float = 1e-6,
        D_n: float = 25.0,
        D_p: float = 10.0,
        L_n: float = 5e-4,
        L_p: float = 5e-4,
        R_s: float = 0.0,
        R_sh: float = np.inf,
        enable_parasitics: bool = False,
    ) -> None:
        """
        Initialize the PN Junction Diode.

        Parameters:
            doping_p: Acceptor concentration in p-region (cm^-3)
            doping_n: Donor concentration in n-region (cm^-3)
            area: Cross-sectional area of the diode (cm^2)
            temperature: Temperature in Kelvin
            tau_n: Electron lifetime (s)
            tau_p: Hole lifetime (s)
            D_n: Electron diffusion coefficient at reference temperature (cm^2/s)
            D_p: Hole diffusion coefficient at reference temperature (cm^2/s)
            L_n: Electron diffusion length (cm)
            L_p: Hole diffusion length (cm)
            R_s: Series resistance (Ω)
            R_sh: Shunt resistance (Ω)
            enable_parasitics: Enable parasitic effects
        """
        super().__init__(area=area, temperature=temperature, R_s=R_s, R_sh=R_sh, enable_parasitics=enable_parasitics)
        self.doping_p = float(doping_p)
        self.doping_n = float(doping_n)
        self.tau_n = float(tau_n)
        self.tau_p = float(tau_p)
        self.D_n_ref = float(D_n)  # Reference diffusion coefficient
        self.D_p_ref = float(D_p)  # Reference diffusion coefficient
        self.L_n = float(L_n)
        self.L_p = float(L_p)
        self.I_s = self.calculate_saturation_current()

    def calculate_saturation_current(self) -> float:
        """Calculate the saturation current (I_s) with improved temperature dependence."""
        # Improved intrinsic carrier concentration with temperature-dependent bandgap
        n_i = intrinsic_carrier_concentration(self.temperature)
        
        # Temperature-dependent diffusion coefficients
        D_n = diffusion_coefficient_temperature(self.temperature, self.D_n_ref)
        D_p = diffusion_coefficient_temperature(self.temperature, self.D_p_ref)
        
        I_s = q * self.area * n_i**2 * (
            (D_p / (self.L_p * self.doping_n)) + (D_n / (self.L_n * self.doping_p))
        )
        return float(I_s)

    def iv_characteristic(
        self,
        voltage_array: np.ndarray,
        n_conc: Optional[Union[float, np.ndarray]] = None,
        p_conc: Optional[Union[float, np.ndarray]] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate the current for a given array of voltages, including SRH recombination.

        Parameters:
            voltage_array: Array of voltage values (V)
            n_conc: Electron concentration (cm^-3)
            p_conc: Hole concentration (cm^-3)

        Returns:
            Tuple of `(current_array, recombination_array)` matching the shape of `voltage_array`.
        """
        V_T = k_B * self.temperature / q  # Thermal voltage
        I_ideal = self.I_s * safe_expm1(voltage_array / V_T)

        # Apply parasitics if enabled
        if self.enable_parasitics:
            I = self._apply_parasitics(voltage_array, I_ideal)
        else:
            I = I_ideal

        if n_conc is not None and p_conc is not None:
            R_SRH = srh_recombination(
                n_conc, p_conc, temperature=self.temperature, tau_n=self.tau_n, tau_p=self.tau_p
            )
            R_SRH = np.broadcast_to(R_SRH, np.shape(voltage_array))
        else:
            R_SRH = np.zeros_like(voltage_array)

        return np.asarray(I), np.asarray(R_SRH)

    def __repr__(self) -> str:
        parasitic_str = f", R_s={self.R_s}, R_sh={self.R_sh}, enable_parasitics={self.enable_parasitics}" if self.enable_parasitics else ""
        return (
            f"PNJunctionDiode(doping_p={self.doping_p}, doping_n={self.doping_n}, area={self.area}, "
            f"temperature={self.temperature}, tau_n={self.tau_n}, tau_p={self.tau_p}{parasitic_str})"
        )

    def plot_iv_characteristic(self, voltage: np.ndarray, current: np.ndarray, recombination: Optional[np.ndarray] = None) -> None:
        """Plot the IV characteristics and optionally the recombination rate."""
        use_headless_backend("Agg")
        apply_basic_style()
        fig, ax1 = plt.subplots(figsize=(8, 6))

        color = "tab:blue"
        ax1.set_xlabel("Voltage (V)")
        ax1.set_ylabel("Current (A)", color=color)
        ax1.plot(voltage, current, color=color, label="IV Characteristic")
        ax1.tick_params(axis="y", labelcolor=color)
        ax1.grid(True)

        if recombination is not None:
            ax2 = ax1.twinx()
            color = "tab:green"
            ax2.set_ylabel("Recombination Rate (cm$^{-3}$ s$^{-1}$)", color=color)
            ax2.plot(voltage, recombination, color=color, label="SRH Recombination")
            ax2.tick_params(axis="y", labelcolor=color)

        fig.tight_layout()
        plt.title("PN Junction Diode IV Characteristics")
        plt.show()

    def plot_iv_comparison(self, voltage: np.ndarray, show_parasitics: bool = True) -> None:
        """Plot IV characteristics with and without parasitics for comparison."""
        use_headless_backend("Agg")
        apply_basic_style()
        
        # Calculate ideal current (no parasitics)
        old_enable = self.enable_parasitics
        self.enable_parasitics = False
        current_ideal, _ = self.iv_characteristic(voltage)
        
        if show_parasitics and (self.R_s > 0 or not np.isinf(self.R_sh)):
            # Calculate current with parasitics
            self.enable_parasitics = True
            current_parasitic, _ = self.iv_characteristic(voltage)
            self.enable_parasitics = old_enable
            
            plt.figure(figsize=(8, 6))
            plt.plot(voltage, current_ideal, 'b-', label='Ideal (no parasitics)', linewidth=2)
            plt.plot(voltage, current_parasitic, 'r--', label=f'With parasitics (Rs={self.R_s}Ω, Rsh={self.R_sh}Ω)', linewidth=2)
            plt.xlabel('Voltage (V)')
            plt.ylabel('Current (A)')
            plt.title('PN Junction Diode: Ideal vs Parasitic Model')
            plt.grid(True)
            plt.legend()
            plt.show()
        else:
            self.enable_parasitics = old_enable
            plt.figure(figsize=(8, 6))
            plt.plot(voltage, current_ideal, 'b-', label='IV Characteristic', linewidth=2)
            plt.xlabel('Voltage (V)')
            plt.ylabel('Current (A)')
            plt.title('PN Junction Diode IV Characteristics')
            plt.grid(True)
            plt.legend()
            plt.show()
