from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Tuple
import numpy as np

from semiconductor_sim.utils import DEFAULT_T


class Device(ABC):
    """
    Abstract base class for semiconductor devices.

    Provides common fields and establishes a standard API for IV
    characteristics. Subclasses must implement `iv_characteristic`.
    """

    def __init__(
        self, 
        area: float = 1e-4, 
        temperature: float = DEFAULT_T,
        R_s: float = 0.0,
        R_sh: float = np.inf,
        enable_parasitics: bool = False,
    ) -> None:
        if not np.isfinite(area) or area <= 0:
            raise ValueError("area must be a positive finite value (cm^2)")
        if not np.isfinite(temperature) or temperature <= 0:
            raise ValueError("temperature must be a positive finite value (K)")
        if not np.isfinite(R_s) or R_s < 0:
            raise ValueError("R_s must be a non-negative finite value (Ω)")
        if R_sh <= 0:
            raise ValueError("R_sh must be a positive value (Ω)")
            
        self.area = area
        self.temperature = temperature
        self.R_s = R_s  # Series resistance (Ω)
        self.R_sh = R_sh  # Shunt resistance (Ω) 
        self.enable_parasitics = enable_parasitics

    @abstractmethod
    def iv_characteristic(
        self,
        voltage_array: np.ndarray,
        n_conc: Optional[float | np.ndarray] = None,
        p_conc: Optional[float | np.ndarray] = None,
    ) -> Tuple[np.ndarray, ...]:
        """
        Compute current vs. voltage. Implementations must return a tuple where the
        first element is the current array, and optional subsequent arrays include
        model-specific outputs (e.g., recombination rates, emission).
        """
        raise NotImplementedError

    def _apply_parasitics(self, voltage_terminal: np.ndarray, current_ideal: np.ndarray) -> np.ndarray:
        """
        Apply parasitic effects to ideal device current.
        
        The parasitic model accounts for:
        - Series resistance R_s: voltage drop I*R_s
        - Shunt resistance R_sh: parallel leakage current V/R_sh
        
        Terminal equation: I_terminal = I_ideal(V_terminal - I_terminal*R_s) + V_terminal/R_sh
        
        This is solved iteratively for I_terminal.
        """
        if not self.enable_parasitics:
            return current_ideal
            
        # If R_s = 0 and R_sh = inf, return ideal current
        if self.R_s == 0.0 and np.isinf(self.R_sh):
            return current_ideal
            
        I_terminal = np.zeros_like(voltage_terminal)
        
        # Calculate thermal voltage for this device
        V_T = 1.381e-23 * self.temperature / 1.602e-19  # k_B * T / q
        
        for i, V_term in enumerate(voltage_terminal):
            # Initial guess: start with ideal current
            I_guess = current_ideal[i]
            
            # Newton-Raphson iteration to solve:
            # I_terminal = I_ideal(V_terminal - I_terminal*R_s) + V_terminal/R_sh
            for iteration in range(20):  # Max 20 iterations
                V_diode = V_term - I_guess * self.R_s
                
                # Calculate ideal current at this diode voltage using diode equation
                # I_ideal = I_s * (exp(V_diode/V_T) - 1)
                I_s = self.I_s if hasattr(self, 'I_s') else 1e-12
                
                if V_diode / V_T > 700:  # Prevent overflow
                    I_ideal_at_V = I_s * np.exp(700)
                elif V_diode / V_T < -700:  # Prevent underflow
                    I_ideal_at_V = -I_s
                else:
                    I_ideal_at_V = I_s * (np.exp(V_diode / V_T) - 1)
                
                # Shunt current
                I_shunt = V_term / self.R_sh if not np.isinf(self.R_sh) else 0.0
                
                # Function: f = I_guess - I_ideal(V_diode) - I_shunt = 0
                f = I_guess - I_ideal_at_V - I_shunt
                
                # Derivative: df/dI = 1 + R_s * dI_ideal/dV_diode
                if V_diode / V_T > 700:
                    dI_dV = I_s * np.exp(700) / V_T
                elif V_diode / V_T < -700:
                    dI_dV = 0.0
                else:
                    dI_dV = I_s * np.exp(V_diode / V_T) / V_T
                    
                df_dI = 1 + self.R_s * dI_dV
                
                if abs(df_dI) < 1e-15:
                    break
                    
                I_new = I_guess - f / df_dI
                
                if abs(I_new - I_guess) / max(abs(I_guess), 1e-15) < 1e-12:
                    break
                    
                I_guess = I_new
            
            I_terminal[i] = I_guess
            
        return I_terminal

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        parasitic_str = f", R_s={self.R_s}, R_sh={self.R_sh}, enable_parasitics={self.enable_parasitics}" if self.enable_parasitics else ""
        return f"{cls}(area={self.area}, temperature={self.temperature}{parasitic_str})"
