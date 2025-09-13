# semiconductor_sim/schemas/material_presets.py

"""Material property presets for common semiconductors."""

import math
from typing import Dict, Any, List
from dataclasses import dataclass

from ..utils import DEFAULT_T


@dataclass
class MaterialProperties:
    """Container for material properties of a semiconductor."""
    
    # Basic properties
    name: str
    bandgap: float  # eV at 300K
    ni_300k: float  # intrinsic carrier concentration at 300K (cm^-3)
    epsilon_r: float  # relative permittivity
    
    # Transport properties
    mu_n: float  # electron mobility (cm^2/V/s)
    mu_p: float  # hole mobility (cm^2/V/s)
    D_n: float  # electron diffusion coefficient (cm^2/s)
    D_p: float  # hole diffusion coefficient (cm^2/s)
    
    # Recombination properties
    tau_n: float  # electron lifetime (s)
    tau_p: float  # hole lifetime (s)
    L_n: float  # electron diffusion length (cm)
    L_p: float  # hole diffusion length (cm)
    
    # Radiative recombination coefficient
    B: float  # cm^3/s
    
    def ni(self, temperature: float = DEFAULT_T) -> float:
        """Calculate intrinsic carrier concentration at given temperature.
        
        Uses the relationship: ni(T) = ni_300K * (T/300)^1.5 * exp(-Eg/2kT + Eg/2k*300)
        """
        from ..utils import k_B, q
        
        k_eV = k_B / q  # Boltzmann constant in eV/K
        
        # Temperature scaling factor
        T_factor = (temperature / 300.0) ** 1.5
        
        # Exponential factor accounting for bandgap change with temperature
        exp_factor = math.exp(-self.bandgap / (2 * k_eV) * (1/temperature - 1/300.0))
        
        return self.ni_300k * T_factor * exp_factor


class MaterialPresets:
    """Collection of material property presets for common semiconductors."""
    
    # Material property database
    _MATERIALS = {
        "SI": MaterialProperties(
            name="Silicon",
            bandgap=1.12,
            ni_300k=1.0e10,
            epsilon_r=11.7,
            mu_n=1350.0,
            mu_p=480.0,
            D_n=35.0,  # Calculated from mu using Einstein relation at 300K
            D_p=12.4,
            tau_n=1e-6,
            tau_p=1e-6,
            L_n=(35.0 * 1e-6) ** 0.5,  # sqrt(D * tau)
            L_p=(12.4 * 1e-6) ** 0.5,
            B=1e-15,
        ),
        
        "GAAS": MaterialProperties(
            name="Gallium Arsenide",
            bandgap=1.42,
            ni_300k=2.1e6,
            epsilon_r=13.1,
            mu_n=8500.0,
            mu_p=400.0,
            D_n=220.0,
            D_p=10.3,
            tau_n=1e-9,
            tau_p=1e-9,
            L_n=(220.0 * 1e-9) ** 0.5,
            L_p=(10.3 * 1e-9) ** 0.5,
            B=2e-10,
        ),
        
        "GE": MaterialProperties(
            name="Germanium",
            bandgap=0.66,
            ni_300k=2.4e13,
            epsilon_r=16.0,
            mu_n=3900.0,
            mu_p=1900.0,
            D_n=101.0,
            D_p=49.1,
            tau_n=5e-7,
            tau_p=5e-7,
            L_n=(101.0 * 5e-7) ** 0.5,
            L_p=(49.1 * 5e-7) ** 0.5,
            B=5e-14,
        ),
        
        "GAN": MaterialProperties(
            name="Gallium Nitride",
            bandgap=3.4,
            ni_300k=1.9e-10,
            epsilon_r=9.0,
            mu_n=1000.0,
            mu_p=200.0,
            D_n=25.9,
            D_p=5.2,
            tau_n=1e-9,
            tau_p=1e-9,
            L_n=(25.9 * 1e-9) ** 0.5,
            L_p=(5.2 * 1e-9) ** 0.5,
            B=1e-11,
        ),
        
        "INP": MaterialProperties(
            name="Indium Phosphide",
            bandgap=1.35,
            ni_300k=1.3e7,
            epsilon_r=12.4,
            mu_n=4600.0,
            mu_p=150.0,
            D_n=119.0,
            D_p=3.9,
            tau_n=5e-10,
            tau_p=5e-10,
            L_n=(119.0 * 5e-10) ** 0.5,
            L_p=(3.9 * 5e-10) ** 0.5,
            B=1e-10,
        ),
    }
    
    @classmethod
    def get(cls, material: str) -> MaterialProperties:
        """Get material properties for a given material.
        
        Args:
            material: Material name (case-insensitive)
            
        Returns:
            MaterialProperties object
            
        Raises:
            ValueError: If material is not found
        """
        material_upper = material.upper()
        if material_upper not in cls._MATERIALS:
            available = ", ".join(cls._MATERIALS.keys())
            raise ValueError(
                f"Material '{material}' not found. Available materials: {available}"
            )
        return cls._MATERIALS[material_upper]
    
    @classmethod
    def list_available(cls) -> List[str]:
        """List all available materials."""
        return list(cls._MATERIALS.keys())
    
    @classmethod
    def add_material(cls, name: str, properties: MaterialProperties) -> None:
        """Add a custom material to the database.
        
        Args:
            name: Material name (will be converted to uppercase)
            properties: MaterialProperties object
        """
        cls._MATERIALS[name.upper()] = properties


def get_material_properties(material: str) -> MaterialProperties:
    """Get material properties for a given material.
    
    Args:
        material: Material name (case-insensitive)
        
    Returns:
        MaterialProperties object
        
    Raises:
        ValueError: If material is not found
    """
    return MaterialPresets.get(material)


def list_available_materials() -> List[str]:
    """List all available materials."""
    return MaterialPresets.list_available()