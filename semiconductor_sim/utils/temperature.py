# semiconductor_sim/utils/temperature.py
"""
Temperature-dependent models for semiconductor physics.

This module provides improved temperature dependencies for:
- Intrinsic carrier concentration (with temperature-dependent bandgap)
- Mobility (temperature-dependent diffusion coefficients)
- Bandgap energy
"""

import numpy as np
from .constants import q, k_B, DEFAULT_T


def bandgap_varshni(temperature: float, Eg0: float = 1.12, alpha: float = 4.73e-4, beta: float = 636.0) -> float:
    """
    Calculate temperature-dependent bandgap using Varshni equation.
    
    Eg(T) = Eg(0) - αT²/(T + β)
    
    Parameters:
        temperature: Temperature in Kelvin
        Eg0: Bandgap at 0K in eV (default for silicon)
        alpha: Varshni parameter in eV/K (default for silicon)
        beta: Varshni parameter in K (default for silicon)
        
    Returns:
        Bandgap energy in eV
    """
    return Eg0 - (alpha * temperature**2) / (temperature + beta)


def intrinsic_carrier_concentration(temperature: float, Eg0: float = 1.12) -> float:
    """
    Calculate intrinsic carrier concentration with temperature-dependent bandgap.
    
    n_i(T) = √(N_c * N_v) * exp(-Eg(T)/(2*k_B*T))
    
    Simplified model uses temperature dependence: n_i ∝ T^1.5 * exp(-Eg(T)/(2*k_B*T))
    
    Parameters:
        temperature: Temperature in Kelvin
        Eg0: Bandgap at 0K in eV
        
    Returns:
        Intrinsic carrier concentration in cm^-3
    """
    # Temperature-dependent bandgap
    Eg_T = bandgap_varshni(temperature, Eg0)
    Eg_ref = bandgap_varshni(DEFAULT_T, Eg0)
    
    # Reference value at DEFAULT_T with simplified prefactor
    n_i_ref = 1.5e10  # cm^-3 at 300K
    
    # Temperature scaling - use simpler model to match expected behavior
    # For semiconductor device modeling, we typically see n_i increase with T
    # due to more carriers being excited across the bandgap
    n_i = n_i_ref * (temperature / DEFAULT_T)**1.5 * np.exp(
        -q * (Eg_T - Eg_ref) / (2 * k_B * temperature)
    )
    
    return float(n_i)


def mobility_temperature_scaling(temperature: float, mobility_ref: float, T_ref: float = DEFAULT_T, gamma: float = -1.5) -> float:
    """
    Calculate temperature-dependent mobility.
    
    μ(T) = μ_ref * (T/T_ref)^γ
    
    For lattice scattering dominated transport, γ ≈ -1.5
    
    Parameters:
        temperature: Temperature in Kelvin
        mobility_ref: Reference mobility at T_ref in cm²/(V·s)
        T_ref: Reference temperature in Kelvin
        gamma: Temperature exponent (negative for lattice scattering)
        
    Returns:
        Temperature-scaled mobility in cm²/(V·s)
    """
    return mobility_ref * (temperature / T_ref)**gamma


def diffusion_coefficient_temperature(temperature: float, D_ref: float, T_ref: float = DEFAULT_T, gamma: float = -1.5) -> float:
    """
    Calculate temperature-dependent diffusion coefficient.
    
    D(T) = D_ref * (T/T_ref)^(γ+1)
    
    Since D = μ*k_B*T/q, and μ ∝ T^γ, then D ∝ T^(γ+1)
    
    Parameters:
        temperature: Temperature in Kelvin
        D_ref: Reference diffusion coefficient at T_ref in cm²/s
        T_ref: Reference temperature in Kelvin  
        gamma: Mobility temperature exponent
        
    Returns:
        Temperature-scaled diffusion coefficient in cm²/s
    """
    return D_ref * (temperature / T_ref)**(gamma + 1)