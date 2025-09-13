"""Schottky diode device model with temperature dependence and series resistance."""

import numpy as np
from typing import Optional, Tuple, Union
import matplotlib.pyplot as plt

from semiconductor_sim.utils import DEFAULT_T, k_B, q
from semiconductor_sim.utils.numerics import safe_expm1
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style

from .base import Device


class SchottkyDiode(Device):
    """Schottky diode device model.
    
    Models a metal-semiconductor junction using thermionic emission theory
    with the Richardson equation for temperature-dependent saturation current.
    
    Features:
    - Temperature-dependent saturation current via Richardson equation
    - Barrier height φ_B parameter for different metal-semiconductor combinations
    - Optional image-force lowering to reduce effective barrier height
    - Optional series resistance R_s
    - Area scaling
    
    Assumptions:
    - Thermionic emission dominates (not tunneling/field emission)
    - Ideal diode equation: I = I_s * (exp(q*V_j/k_B*T) - 1)
    - Richardson equation: I_s = A * A_eff * T^2 * exp(-q*φ_B_eff / k_B*T)
    - Series resistance creates voltage drop: V_j = V - I*R_s
    """
    
    def __init__(
        self,
        barrier_height: float,
        area: float = 1e-4,
        temperature: float = DEFAULT_T,
        A_eff: float = 120.0,  # Effective Richardson constant (A/(cm^2·K^2))
        series_resistance: float = 0.0,  # Series resistance (Ohm)
        image_force_lowering: float = 0.0,  # Image force lowering (eV)
    ) -> None:
        """
        Initialize the Schottky Diode.
        
        Parameters:
            barrier_height: Schottky barrier height φ_B (eV)
            area: Cross-sectional area of the diode (cm^2)
            temperature: Temperature (K)
            A_eff: Effective Richardson constant (A/(cm^2·K^2))
            series_resistance: Series resistance R_s (Ohm)
            image_force_lowering: Image force lowering constant (eV)
        """
        super().__init__(area=area, temperature=temperature)
        
        if barrier_height <= 0:
            raise ValueError("barrier_height must be positive")
        if A_eff <= 0:
            raise ValueError("A_eff must be positive")
        if series_resistance < 0:
            raise ValueError("series_resistance must be non-negative")
        if image_force_lowering < 0:
            raise ValueError("image_force_lowering must be non-negative")
            
        self.barrier_height = float(barrier_height)
        self.A_eff = float(A_eff)
        self.series_resistance = float(series_resistance)
        self.image_force_lowering = float(image_force_lowering)
        
        # Calculate effective barrier height and saturation current
        self.barrier_height_eff = self.barrier_height - self.image_force_lowering
        self.I_s = self.calculate_saturation_current()
    
    def calculate_saturation_current(self) -> float:
        """Calculate saturation current using Richardson equation.
        
        Richardson equation: I_s = A * A_eff * T^2 * exp(-q*φ_B_eff / k_B*T)
        
        Returns:
            Saturation current (A)
        """
        # Convert barrier height from eV to Joules for exponential
        barrier_energy = self.barrier_height_eff * q  # Convert eV to J
        
        # Richardson equation
        I_s = (self.area * self.A_eff * self.temperature**2 * 
               np.exp(-barrier_energy / (k_B * self.temperature)))
        
        return float(I_s)
    
    def iv_characteristic(
        self,
        voltage_array: np.ndarray,
        **kwargs  # Accept unused kwargs for API compatibility
    ) -> Tuple[np.ndarray]:
        """
        Calculate current for given voltage array.
        
        For series resistance, solves: V = V_j + I*R_s
        where V_j is the junction voltage and I = I_s * (exp(q*V_j/k_B*T) - 1)
        
        Parameters:
            voltage_array: Array of applied voltage values (V)
            **kwargs: Unused parameters for API compatibility with other devices
            
        Returns:
            Tuple containing (current_array,)
        """
        voltage_array = np.asarray(voltage_array)
        V_T = k_B * self.temperature / q  # Thermal voltage
        
        if self.series_resistance == 0.0:
            # No series resistance - direct calculation
            I = self.I_s * safe_expm1(voltage_array / V_T)
        else:
            # With series resistance - iterative solution required
            I = np.zeros_like(voltage_array, dtype=float)
            
            for i, V in enumerate(voltage_array.flat):
                # Initial guess: assume junction voltage ≈ applied voltage
                V_j = V
                
                # Newton-Raphson iteration to solve V = V_j + I*R_s
                for _ in range(10):  # Max 10 iterations
                    I_j = self.I_s * safe_expm1(V_j / V_T)
                    f = V_j + I_j * self.series_resistance - V
                    
                    # Check convergence
                    if abs(f) < 1e-12:
                        break
                        
                    # Derivative df/dV_j = 1 + R_s * dI/dV_j
                    dI_dVj = (self.I_s / V_T) * np.exp(V_j / V_T)
                    df_dVj = 1 + self.series_resistance * dI_dVj
                    
                    # Newton update
                    V_j = V_j - f / df_dVj
                
                I.flat[i] = self.I_s * safe_expm1(V_j / V_T)
        
        return (np.asarray(I),)
    
    def plot_iv_characteristic(
        self, 
        voltage: np.ndarray, 
        current: np.ndarray, 
        title: Optional[str] = None
    ) -> None:
        """Plot the IV characteristics of the Schottky diode.
        
        Parameters:
            voltage: Voltage array (V)
            current: Current array (A)
            title: Optional plot title
        """
        use_headless_backend("Agg")
        apply_basic_style()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        ax.semilogy(voltage, np.abs(current), 'b-', linewidth=2, label='|Current|')
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('|Current| (A)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        if title is None:
            title = f'Schottky Diode IV (φ_B={self.barrier_height:.2f} eV, T={self.temperature:.0f} K)'
            if self.series_resistance > 0:
                title += f', R_s={self.series_resistance:.1e} Ω'
        ax.set_title(title)
        
        plt.tight_layout()
        plt.show()
    
    def plot_temperature_dependence(
        self, 
        voltage: np.ndarray, 
        temperatures: np.ndarray
    ) -> None:
        """Plot IV characteristics at different temperatures.
        
        Parameters:
            voltage: Voltage array (V)
            temperatures: Array of temperatures to plot (K)
        """
        use_headless_backend("Agg")
        apply_basic_style()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        original_temp = self.temperature
        
        for T in temperatures:
            # Temporarily change temperature
            self.temperature = float(T)
            self.I_s = self.calculate_saturation_current()
            
            current, = self.iv_characteristic(voltage)
            ax.semilogy(voltage, np.abs(current), linewidth=2, 
                       label=f'T = {T:.0f} K')
        
        # Restore original temperature
        self.temperature = original_temp
        self.I_s = self.calculate_saturation_current()
        
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('|Current| (A)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_title(f'Schottky Diode Temperature Dependence (φ_B={self.barrier_height:.2f} eV)')
        
        plt.tight_layout()
        plt.show()
    
    def __repr__(self) -> str:
        return (
            f"SchottkyDiode(barrier_height={self.barrier_height}, area={self.area}, "
            f"temperature={self.temperature}, A_eff={self.A_eff}, "
            f"series_resistance={self.series_resistance}, "
            f"image_force_lowering={self.image_force_lowering})"
        )