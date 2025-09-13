"""BJT (Bipolar Junction Transistor) device model using Ebers-Moll equations."""

import numpy as np
from typing import Optional, Tuple, Union, Literal

from semiconductor_sim.utils import DEFAULT_T, k_B, q
from semiconductor_sim.models import srh_recombination
from semiconductor_sim.utils.numerics import safe_expm1
import matplotlib.pyplot as plt
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style

from .base import Device


class BJT(Device):
    """BJT (Bipolar Junction Transistor) device model using Ebers-Moll equations.

    Implements the Ebers-Moll model for both NPN and PNP transistors with:
    - Temperature-dependent saturation current I_S
    - Forward and reverse current gains (β_F, β_R)
    - Optional SRH recombination coupling
    - Pedagogical IV characteristics for forward active, saturation, cutoff, reverse regions

    Assumptions:
    - Uses simplified Ebers-Moll model suitable for undergraduate teaching
    - Temperature dependence follows semiconductor physics principles
    - Default transport parameters are representative silicon values
    - Units: cm, cm^2, cm^3, K; currents in A; voltages in V
    """

    def __init__(
        self,
        doping_emitter: float,
        doping_base: float,
        doping_collector: float,
        area: float = 1e-4,
        temperature: float = DEFAULT_T,
        bjt_type: Literal["NPN", "PNP"] = "NPN",
        beta_f: float = 100.0,
        beta_r: float = 1.0,
        tau_n: float = 1e-6,
        tau_p: float = 1e-6,
    ) -> None:
        """
        Initialize the BJT device.

        Parameters:
            doping_emitter: Emitter doping concentration (cm^-3)
            doping_base: Base doping concentration (cm^-3)
            doping_collector: Collector doping concentration (cm^-3)
            area: Cross-sectional area of the device (cm^2)
            temperature: Temperature in Kelvin
            bjt_type: Type of BJT - "NPN" or "PNP"
            beta_f: Forward current gain (dimensionless)
            beta_r: Reverse current gain (dimensionless)
            tau_n: Electron lifetime (s)
            tau_p: Hole lifetime (s)
        """
        super().__init__(area=area, temperature=temperature)
        self.doping_emitter = float(doping_emitter)
        self.doping_base = float(doping_base)
        self.doping_collector = float(doping_collector)
        self.bjt_type = bjt_type
        self.beta_f = float(beta_f)
        self.beta_r = float(beta_r)
        self.tau_n = float(tau_n)
        self.tau_p = float(tau_p)
        
        # Calculate temperature-dependent parameters
        self.I_s = self.calculate_saturation_current()
        self.beta_f_eff = self.calculate_effective_beta_f()
        self.beta_r_eff = self.calculate_effective_beta_r()

    def calculate_saturation_current(self) -> float:
        """Calculate the saturation current I_S with temperature dependence."""
        # Intrinsic carrier concentration with temperature dependence
        n_i = 1.5e10 * (self.temperature / DEFAULT_T) ** 1.5
        
        # Simplified I_S calculation based on junction properties
        # For pedagogical purposes, using representative diffusion constants
        D_n = 25.0  # cm^2/s
        D_p = 10.0  # cm^2/s
        L_n = 5e-4  # cm
        L_p = 5e-4  # cm
        
        # Simplified Ebers-Moll saturation current
        # Based on minority carrier diffusion in base and emitter regions
        I_s = q * self.area * n_i**2 * (
            (D_p / (L_p * self.doping_emitter)) + (D_n / (L_n * self.doping_collector))
        )
        return float(I_s)

    def calculate_effective_beta_f(self) -> float:
        """Calculate effective forward beta with temperature dependence."""
        # Simple temperature dependence for beta_F
        temp_factor = (DEFAULT_T / self.temperature) ** 0.5
        return self.beta_f * temp_factor

    def calculate_effective_beta_r(self) -> float:
        """Calculate effective reverse beta with temperature dependence."""
        # Simple temperature dependence for beta_R
        temp_factor = (DEFAULT_T / self.temperature) ** 0.5
        return self.beta_r * temp_factor

    def iv_characteristic(
        self,
        v_be_array: np.ndarray,
        v_bc: Union[float, np.ndarray] = 0.0,
        n_conc: Optional[Union[float, np.ndarray]] = None,
        p_conc: Optional[Union[float, np.ndarray]] = None,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate BJT currents using the Ebers-Moll model.

        Parameters:
            v_be_array: Base-emitter voltage array (V)
            v_bc: Base-collector voltage (V) - scalar or array matching v_be_array
            n_conc: Electron concentration for SRH recombination (cm^-3)
            p_conc: Hole concentration for SRH recombination (cm^-3)

        Returns:
            Tuple of (I_C, I_B, recombination_rate) arrays matching v_be_array shape
            where I_E = -(I_C + I_B) by current conservation

        Notes:
            - For NPN: positive v_be_array forward biases base-emitter
            - For PNP: signs are automatically handled by bjt_type
            - Uses simplified Ebers-Moll model suitable for undergraduate teaching
        """
        # Ensure inputs are numpy arrays
        v_be_array = np.asarray(v_be_array)
        v_bc = np.broadcast_to(v_bc, v_be_array.shape)
        
        # Thermal voltage
        V_T = k_B * self.temperature / q
        
        # Type factor for PNP vs NPN
        type_factor = -1.0 if self.bjt_type == "PNP" else 1.0
        
        # Apply type factor to voltages for PNP
        v_be_eff = type_factor * v_be_array
        v_bc_eff = type_factor * v_bc
        
        # Simplified Ebers-Moll model for pedagogy
        # Forward active: V_BE > 0, V_BC <= 0
        # Saturation: V_BE > 0, V_BC > 0
        # Cutoff: V_BE <= 0
        
        # Base-emitter junction current (forward)
        I_f = self.I_s * safe_expm1(v_be_eff / V_T)
        
        # Base-collector junction current (reverse when V_BC <= 0)
        I_r = self.I_s * safe_expm1(v_bc_eff / V_T)
        
        # Collector current using standard Ebers-Moll
        # I_C = α_F * I_f - I_r
        # where α_F = β_F/(1 + β_F) ≈ 1 for large β_F
        alpha_f = self.beta_f_eff / (1 + self.beta_f_eff)
        alpha_r = self.beta_r_eff / (1 + self.beta_r_eff)
        
        I_C = alpha_f * I_f - I_r
        
        # Emitter current using standard Ebers-Moll
        # I_E = I_f - α_R * I_r
        I_E = I_f - alpha_r * I_r
        
        # Base current from current conservation: I_B = I_E - I_C
        I_B = I_E - I_C
        
        # Apply type factor to currents for PNP
        I_C = type_factor * I_C
        I_B = type_factor * I_B
        
        # Calculate SRH recombination if carrier concentrations provided
        if n_conc is not None and p_conc is not None:
            R_SRH = srh_recombination(
                n_conc, p_conc, temperature=self.temperature, tau_n=self.tau_n, tau_p=self.tau_p
            )
            R_SRH = np.broadcast_to(R_SRH, v_be_array.shape)
        else:
            R_SRH = np.zeros_like(v_be_array)

        return np.asarray(I_C), np.asarray(I_B), np.asarray(R_SRH)

    def __repr__(self) -> str:
        return (
            f"BJT(type={self.bjt_type}, doping_emitter={self.doping_emitter}, "
            f"doping_base={self.doping_base}, doping_collector={self.doping_collector}, "
            f"area={self.area}, temperature={self.temperature}, "
            f"beta_f={self.beta_f}, beta_r={self.beta_r})"
        )

    def plot_iv_characteristic(
        self,
        v_be: np.ndarray,
        i_c: np.ndarray,
        i_b: np.ndarray,
        v_bc: Optional[Union[float, np.ndarray]] = None,
        recombination: Optional[np.ndarray] = None,
    ) -> None:
        """Plot the BJT IV characteristics."""
        use_headless_backend("Agg")
        apply_basic_style()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Plot collector current
        ax1.plot(v_be, i_c, 'b-', linewidth=2, label=f'$I_C$ ({self.bjt_type})')
        ax1.set_xlabel('$V_{BE}$ (V)')
        ax1.set_ylabel('$I_C$ (A)')
        ax1.set_title(f'{self.bjt_type} BJT Collector Current')
        ax1.grid(True)
        ax1.legend()
        ax1.set_yscale('symlog', linthresh=1e-12)
        
        # Plot base current
        ax2.plot(v_be, i_b, 'r-', linewidth=2, label=f'$I_B$ ({self.bjt_type})')
        ax2.set_xlabel('$V_{BE}$ (V)')
        ax2.set_ylabel('$I_B$ (A)')
        ax2.set_title(f'{self.bjt_type} BJT Base Current')
        ax2.grid(True)
        ax2.legend()
        ax2.set_yscale('symlog', linthresh=1e-12)
        
        # Add V_BC information if provided
        if v_bc is not None:
            if np.isscalar(v_bc):
                fig.suptitle(f'{self.bjt_type} BJT IV Characteristics ($V_{{BC}}$ = {v_bc:.2f} V)')
            else:
                fig.suptitle(f'{self.bjt_type} BJT IV Characteristics')
        
        # Optionally plot recombination rate
        if recombination is not None and np.any(recombination != 0):
            ax3 = ax2.twinx()
            ax3.plot(v_be, recombination, 'g--', alpha=0.7, label='SRH Recombination')
            ax3.set_ylabel('Recombination Rate (cm$^{-3}$ s$^{-1}$)', color='green')
            ax3.tick_params(axis='y', labelcolor='green')
            ax3.legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()

    def plot_gummel_plot(
        self,
        v_be: np.ndarray,
        i_c: np.ndarray,
        i_b: np.ndarray,
    ) -> None:
        """Plot Gummel plot (log current vs V_BE) for BJT characterization."""
        use_headless_backend("Agg")
        apply_basic_style()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Plot collector and base currents on log scale
        ax.semilogy(v_be, np.abs(i_c), 'b-', linewidth=2, label=f'|$I_C$| ({self.bjt_type})')
        ax.semilogy(v_be, np.abs(i_b), 'r-', linewidth=2, label=f'|$I_B$| ({self.bjt_type})')
        
        ax.set_xlabel('$V_{BE}$ (V)')
        ax.set_ylabel('Current Magnitude (A)')
        ax.set_title(f'{self.bjt_type} BJT Gummel Plot')
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
        
        # Add current gain information
        beta_eff = np.where(np.abs(i_b) > 1e-20, np.abs(i_c / i_b), np.nan)
        ax_beta = ax.twinx()
        ax_beta.plot(v_be, beta_eff, 'g--', alpha=0.7, label=f'$\\beta$ = $I_C/I_B$')
        ax_beta.set_ylabel('Current Gain $\\beta$', color='green')
        ax_beta.tick_params(axis='y', labelcolor='green')
        ax_beta.legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()