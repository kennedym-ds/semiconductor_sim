"""PN Junction diode device model."""

from typing import Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

from semiconductor_sim.models import srh_recombination
from semiconductor_sim.utils import DEFAULT_T, k_B, q
from semiconductor_sim.utils.numerics import safe_expm1
from semiconductor_sim.utils.plotting import apply_basic_style, use_headless_backend

from .base import Device


class PNJunctionDiode(Device):
    """PN Junction diode device model.

    Assumptions:
    - Ideal diode equation with temperature-dependent I_s
    - SRH recombination with default mid-gap trap (n1≈p1≈n_i)
    - Default transport parameters (D, L) are representative constants
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
        """
        super().__init__(area=area, temperature=temperature)
        self.doping_p = float(doping_p)
        self.doping_n = float(doping_n)
        self.tau_n = float(tau_n)
        self.tau_p = float(tau_p)
        self.D_n = float(D_n)
        self.D_p = float(D_p)
        self.L_n = float(L_n)
        self.L_p = float(L_p)
        self.I_s = self.calculate_saturation_current()

    def calculate_saturation_current(self) -> float:
        """Calculate the saturation current (I_s) considering temperature."""
        # Intrinsic carrier concentration with temperature dependence
        n_i = 1.5e10 * (self.temperature / DEFAULT_T) ** 1.5
        I_s = (
            q
            * self.area
            * n_i**2
            * ((self.D_p / (self.L_p * self.doping_n)) + (self.D_n / (self.L_n * self.doping_p)))
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
        I = self.I_s * safe_expm1(voltage_array / V_T)

        if n_conc is not None and p_conc is not None:
            R_SRH = srh_recombination(
                n_conc, p_conc, temperature=self.temperature, tau_n=self.tau_n, tau_p=self.tau_p
            )
            R_SRH = np.broadcast_to(R_SRH, np.shape(voltage_array))
        else:
            R_SRH = np.zeros_like(voltage_array)

        return np.asarray(I), np.asarray(R_SRH)

    def __repr__(self) -> str:
        return (
            f"PNJunctionDiode(doping_p={self.doping_p}, doping_n={self.doping_n}, "
            f"area={self.area}, temperature={self.temperature}, tau_n={self.tau_n}, "
            f"tau_p={self.tau_p})"
        )

    def plot_iv_characteristic(
        self, voltage: np.ndarray, current: np.ndarray, recombination: Optional[np.ndarray] = None
    ) -> None:
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
