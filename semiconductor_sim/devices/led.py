# semiconductor_sim/devices/led.py

import numpy as np
from typing import Optional, Tuple
from semiconductor_sim.utils import q, k_B, DEFAULT_T
from semiconductor_sim.utils import (
    intrinsic_carrier_concentration,
    diffusion_coefficient_temperature,
)
from semiconductor_sim.models import srh_recombination, radiative_recombination
from semiconductor_sim.utils.numerics import safe_expm1
import matplotlib.pyplot as plt
from .base import Device

class LED(Device):
    """Light-emitting diode (LED) model.

    Assumptions:
    - Ideal diode IV: I = I_s * (exp(V/V_T) - 1)
    - Emission ~ efficiency * radiative_recombination * area (simplified)
    - Improved temperature dependencies for carrier concentration and mobility
    - Optional parasitics: series resistance R_s and shunt resistance R_sh
    - Units: cm, cm^2, cm^3, K; q in C, k_B in J/K
    """
    def __init__(
        self,
        doping_p: float,
        doping_n: float,
        area: float = 1e-4,
        efficiency: float = 0.1,
        temperature: float = DEFAULT_T,
        B: float = 1e-10,
        D_n: float = 25.0,
        D_p: float = 10.0,
        L_n: float = 5e-4,
        L_p: float = 5e-4,
        R_s: float = 0.0,
        R_sh: float = np.inf,
        enable_parasitics: bool = False,
    ) -> None:
        """
        Initialize the LED device.

        Parameters:
            doping_p (float): Acceptor concentration in p-region (cm^-3)
            doping_n (float): Donor concentration in n-region (cm^-3)
            area (float): Cross-sectional area of the LED (cm^2)
            efficiency (float): Radiative recombination efficiency (0 to 1)
            temperature (float): Temperature in Kelvin
            B (float): Radiative recombination coefficient (cm^3/s)
            D_n: Electron diffusion coefficient at reference temperature (cm^2/s)
            D_p: Hole diffusion coefficient at reference temperature (cm^2/s)
            L_n: Electron diffusion length (cm)
            L_p: Hole diffusion length (cm)
            R_s: Series resistance (Ω)
            R_sh: Shunt resistance (Ω)
            enable_parasitics: Enable parasitic effects
        """
        super().__init__(area=area, temperature=temperature, R_s=R_s, R_sh=R_sh, enable_parasitics=enable_parasitics)
        if not (0.0 <= efficiency <= 1.0):
            raise ValueError("efficiency must be between 0 and 1")
        self.doping_p = float(doping_p)
        self.doping_n = float(doping_n)
        self.efficiency = float(efficiency)
        self.B = float(B)  # Radiative recombination coefficient
        self.D_n_ref = float(D_n)
        self.D_p_ref = float(D_p)
        self.L_n = float(L_n)
        self.L_p = float(L_p)
        self.I_s = self.calculate_saturation_current()

    def calculate_saturation_current(self) -> float:
        """
        Calculate the saturation current (I_s) with improved temperature dependence.

        Returns:
            float: The saturation current in amperes.
        """
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
        n_conc: Optional[float | np.ndarray] = None,
        p_conc: Optional[float | np.ndarray] = None,
    ) -> Tuple[np.ndarray, ...]:
        """
        Calculate current and optical emission across `voltage_array`.

        Parameters:
            voltage_array: Array of voltage values (V).
            n_conc: Electron concentration (cm^-3). If provided with `p_conc`,
                SRH and radiative recombination are computed and emission includes radiative term.
            p_conc: Hole concentration (cm^-3).

        Returns:
            - If both `n_conc` and `p_conc` are provided: `(I, emission, R_SRH)` where each is `np.ndarray`.
            - Else: `(I, emission)` where both are `np.ndarray`.
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
                n_conc,
                p_conc,
                temperature=self.temperature,
                tau_n=1e-6,
                tau_p=1e-6,
            )
            R_rad = radiative_recombination(
                n_conc,
                p_conc,
                B=self.B,
                temperature=self.temperature,
            )
        else:
            R_SRH = np.zeros_like(voltage_array)
            R_rad = np.zeros_like(voltage_array)

        emission = self.efficiency * R_rad * self.area  # Simplified emission calculation
        I = np.asarray(I)
        emission = np.asarray(emission)
        if n_conc is not None and p_conc is not None:
            R_SRH = np.broadcast_to(R_SRH, np.shape(voltage_array))
            return I, emission, R_SRH
        return I, emission

    def plot_iv_characteristic(
        self,
        voltage: np.ndarray,
        current: np.ndarray,
        emission: Optional[np.ndarray] = None,
        recombination: Optional[np.ndarray] = None,
    ) -> None:
        """
        Plot the IV characteristics, emission intensity, and recombination rate.

        Parameters:
            voltage (np.ndarray): Voltage values (V)
            current (np.ndarray): Current values (A)
            emission (np.ndarray, optional): Emission intensities (arb. units)
            recombination (np.ndarray, optional): Recombination rates (cm^-3 s^-1)
        """
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            subplot_titles=("IV Characteristic", "Emission & Recombination"),
        )

        # IV Plot
        fig.add_trace(go.Scatter(x=voltage, y=current, mode='lines', name='IV Characteristic',
                                 line=dict(color='blue')), row=1, col=1)
        if recombination is not None:
            fig.add_trace(go.Scatter(x=voltage, y=recombination, mode='lines',
                                     name='SRH Recombination', line=dict(color='green', dash='dash')), row=1, col=1)

        # Emission Plot (Secondary y-axis)
        if emission is not None:
            fig.add_trace(go.Scatter(x=voltage, y=emission, mode='lines',
                                     name='Emission', line=dict(color='red', dash='dot')), row=1, col=1)

        # Second subplot shows emission and/or recombination if provided
        if emission is not None:
            fig.add_trace(
                go.Scatter(
                    x=voltage,
                    y=emission,
                    mode='lines',
                    name='Emission',
                    line=dict(color='red', dash='dot')
                ),
                row=2,
                col=1,
            )
        if recombination is not None:
            fig.add_trace(
                go.Scatter(
                    x=voltage,
                    y=recombination,
                    mode='lines',
                    name='SRH Recombination',
                    line=dict(color='green', dash='dash')
                ),
                row=2,
                col=1,
            )

        fig.update_layout(height=800, width=800, title_text="LED IV, Emission & Recombination")
        fig.show()

    def __repr__(self) -> str:
        parasitic_str = f", R_s={self.R_s}, R_sh={self.R_sh}, enable_parasitics={self.enable_parasitics}" if self.enable_parasitics else ""
        return (
            f"LED(doping_p={self.doping_p}, doping_n={self.doping_n}, area={self.area}, "
            f"efficiency={self.efficiency}, temperature={self.temperature}, B={self.B}{parasitic_str})"
        )

    def plot_iv_comparison(self, voltage: np.ndarray, show_parasitics: bool = True) -> None:
        """Plot IV characteristics with and without parasitics for comparison."""
        from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style
        use_headless_backend("Agg")
        apply_basic_style()
        
        # Calculate ideal current (no parasitics)
        old_enable = self.enable_parasitics
        self.enable_parasitics = False
        results_ideal = self.iv_characteristic(voltage)
        current_ideal = results_ideal[0]
        
        if show_parasitics and (self.R_s > 0 or not np.isinf(self.R_sh)):
            # Calculate current with parasitics
            self.enable_parasitics = True
            results_parasitic = self.iv_characteristic(voltage)
            current_parasitic = results_parasitic[0]
            self.enable_parasitics = old_enable
            
            plt.figure(figsize=(8, 6))
            plt.plot(voltage, current_ideal, 'b-', label='Ideal (no parasitics)', linewidth=2)
            plt.plot(voltage, current_parasitic, 'r--', label=f'With parasitics (Rs={self.R_s}Ω, Rsh={self.R_sh}Ω)', linewidth=2)
            plt.xlabel('Voltage (V)')
            plt.ylabel('Current (A)')
            plt.title('LED: Ideal vs Parasitic Model')
            plt.grid(True)
            plt.legend()
            plt.show()
        else:
            self.enable_parasitics = old_enable
            plt.figure(figsize=(8, 6))
            plt.plot(voltage, current_ideal, 'b-', label='IV Characteristic', linewidth=2)
            plt.xlabel('Voltage (V)')
            plt.ylabel('Current (A)')
            plt.title('LED IV Characteristics')
            plt.grid(True)
            plt.legend()
            plt.show()
