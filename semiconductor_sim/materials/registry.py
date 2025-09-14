from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TypeAlias, cast

import numpy as np
from numpy.typing import NDArray

from semiconductor_sim.models.bandgap import temperature_dependent_bandgap

FloatArray: TypeAlias = NDArray[np.float64]


@dataclass(frozen=True)
class Material:
    name: str
    symbol: str
    Eg0_eV: float
    varshni_alpha_eV_per_K: float
    varshni_beta_K: float
    Nc_prefactor_cm3: float
    Nv_prefactor_cm3: float

    def Eg(self, T: float | NDArray[np.floating]) -> float | NDArray[np.floating]:
        return temperature_dependent_bandgap(
            T,
            E_g0=self.Eg0_eV,
            alpha=self.varshni_alpha_eV_per_K,
            beta=int(self.varshni_beta_K),
        )

    def Nc(self, T: float | NDArray[np.floating]) -> float | NDArray[np.floating]:
        T_arr = cast(FloatArray, np.asarray(T, dtype=float))
        Nc_arr = self.Nc_prefactor_cm3 * T_arr**1.5
        if np.ndim(Nc_arr) == 0:
            return float(Nc_arr)
        return Nc_arr

    def Nv(self, T: float | NDArray[np.floating]) -> float | NDArray[np.floating]:
        T_arr = cast(FloatArray, np.asarray(T, dtype=float))
        Nv_arr = self.Nv_prefactor_cm3 * T_arr**1.5
        if np.ndim(Nv_arr) == 0:
            return float(Nv_arr)
        return Nv_arr

    def ni(self, T: float | NDArray[np.floating]) -> float | NDArray[np.floating]:
        T_arr = cast(FloatArray, np.asarray(T, dtype=float))
        Nc = cast(FloatArray, np.asarray(self.Nc(T_arr), dtype=float))
        Nv = cast(FloatArray, np.asarray(self.Nv(T_arr), dtype=float))
        Eg_eV = cast(FloatArray, np.asarray(self.Eg(T_arr), dtype=float))
        # k_B/q in V/K; using eV units, k_B_eV_per_K ~ 8.617333262145e-5
        kB_eV_per_K = 8.617333262145e-5
        ni_arr = cast(FloatArray, np.sqrt(Nc * Nv) * np.exp(-Eg_eV / (2.0 * kB_eV_per_K * T_arr)))
        if np.ndim(ni_arr) == 0:
            return float(ni_arr)
        return ni_arr


# Prefactors Nc = A T^{3/2}, Nv = B T^{3/2} at 300 K yield ~ A*300^{3/2}
# Ioffe provides concise formulas:
# Si: Eg(T) = 1.17 - 4.73e-4 T^2/(T+636); Nc = 6.2e15 T^{3/2}; Nv = 3.5e15 T^{3/2}
# Ge: Eg(T) = 0.742 - 4.8e-4 T^2/(T+235); Nc = 1.98e15 T^{3/2}; Nv = 9.6e14 T^{3/2}
# GaAs: Eg(T) = 1.519 - 5.405e-4 T^2/(T+204); Nc = 8.63e13 T^{3/2} * (Γ,L,X corrections)
# For simplicity and stability here, we use the 300K effective Nc,Nv values from Ioffe basic params
# translated to T^{3/2} form using their given prefactors for Si, Ge, and the simple Nv for GaAs.

materials: dict[str, Material] = {
    # Silicon (Si)
    "Si": Material(
        name="Silicon",
        symbol="Si",
        Eg0_eV=1.17,
        varshni_alpha_eV_per_K=4.73e-4,
        varshni_beta_K=636.0,
        Nc_prefactor_cm3=6.2e15,
        Nv_prefactor_cm3=3.5e15,
    ),
    # Germanium (Ge)
    "Ge": Material(
        name="Germanium",
        symbol="Ge",
        Eg0_eV=0.742,
        varshni_alpha_eV_per_K=4.8e-4,
        varshni_beta_K=235.0,
        Nc_prefactor_cm3=1.98e15,
        Nv_prefactor_cm3=9.6e14,
    ),
    # Gallium Arsenide (GaAs)
    # For Nc, Ioffe provides a more complex expression including L and X valleys;
    # for teaching purposes, we approximate using the 300K reported Nc, Nv with
    # T^{3/2} scaling using coefficients
    # that match 300K values approximately.
    "GaAs": Material(
        name="Gallium Arsenide",
        symbol="GaAs",
        Eg0_eV=1.519,
        varshni_alpha_eV_per_K=5.405e-4,
        varshni_beta_K=204.0,
        # Fit coefficients so that at 300K, Nc ≈ 4.7e17 cm^-3 and Nv ≈ 9.0e18 cm^-3
        Nc_prefactor_cm3=4.7e17 / (300.0**1.5),
        Nv_prefactor_cm3=9.0e18 / (300.0**1.5),
    ),
}


def get_material(key: str) -> Material:
    m = materials.get(key)
    if m is None:
        raise KeyError(f"Unknown material key: {key}. Available: {', '.join(materials)}")
    return m


def list_materials() -> Iterable[str]:
    return materials.keys()
