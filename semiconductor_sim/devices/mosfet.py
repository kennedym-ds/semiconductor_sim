"""Teaching-focused NMOS transistor model with output and transconductance curves."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

from semiconductor_sim.utils import DEFAULT_T
from semiconductor_sim.utils.plotting import apply_basic_style, use_headless_backend

from .base import Device


class MOSFET(Device):
    def __init__(
        self,
        *,
        area: float = 1e-4,
        temperature: float = DEFAULT_T,
        threshold_voltage: float = 1.0,
        beta: float = 1e-3,
        channel_length_modulation: float = 0.02,
        vgs_values: npt.NDArray[np.floating] | list[float] | tuple[float, ...] = (
            1.0,
            1.5,
            2.0,
            2.5,
            3.0,
        ),
    ) -> None:
        """Initialize a teaching-oriented long-channel NMOS model."""
        super().__init__(area=area, temperature=temperature)
        self.threshold_voltage = float(threshold_voltage)
        self.beta = float(beta)
        self.channel_length_modulation = float(channel_length_modulation)
        self.vgs_values = np.asarray(vgs_values, dtype=float).ravel()

    def iv_characteristic(
        self,
        voltage_array: npt.NDArray[np.floating],
        n_conc: float | npt.NDArray[np.floating] | None = None,
        p_conc: float | npt.NDArray[np.floating] | None = None,
    ) -> tuple[npt.NDArray[np.floating], ...]:
        """Compute drain current and transconductance over VDS for configured VGS values."""
        vds = np.asarray(voltage_array, dtype=float).ravel()
        vgs = self.vgs_values[:, None]
        vov = np.maximum(vgs - self.threshold_voltage, 0.0)
        vds_grid = np.broadcast_to(vds, (vgs.shape[0], vds.size))
        lambda_factor = 1.0 + self.channel_length_modulation * vds_grid

        triode = self.beta * (2.0 * vov * vds_grid - vds_grid**2) * lambda_factor
        saturation = self.beta * (vov**2) * lambda_factor
        in_triode = vds_grid < vov
        ids = np.where(vov <= 0.0, 0.0, np.where(in_triode, triode, saturation))
        ids = np.maximum(ids, 0.0)

        gm_triode = 2.0 * self.beta * vds_grid * lambda_factor
        gm_saturation = 2.0 * self.beta * vov * lambda_factor
        gm = np.where(vov <= 0.0, 0.0, np.where(in_triode, gm_triode, gm_saturation))
        return np.asarray(ids, dtype=float), np.asarray(gm, dtype=float)

    def plot_output_characteristics(
        self,
        voltage: npt.NDArray[np.floating],
        current_grid: npt.NDArray[np.floating],
        gm_grid: npt.NDArray[np.floating] | None = None,
    ) -> None:
        """Plot NMOS output characteristics and optional transconductance traces."""
        use_headless_backend("Agg")
        apply_basic_style()
        fig, ax1 = plt.subplots(figsize=(8, 6))
        for idx, vgs in enumerate(self.vgs_values):
            ax1.plot(voltage, current_grid[idx], label=f"Id (VGS={vgs:.2f} V)")
        ax1.set_xlabel("VDS (V)")
        ax1.set_ylabel("Drain Current (A)")
        ax1.grid(True)

        if gm_grid is not None:
            ax2 = ax1.twinx()
            for idx, vgs in enumerate(self.vgs_values):
                ax2.plot(voltage, gm_grid[idx], linestyle="--", label=f"gm (VGS={vgs:.2f} V)")
            ax2.set_ylabel("Transconductance (S)")

        fig.tight_layout()
        plt.title("NMOS Output Characteristics")
        plt.show()

    def __repr__(self) -> str:
        return (
            f"MOSFET(area={self.area}, temperature={self.temperature}, "
            f"threshold_voltage={self.threshold_voltage}, beta={self.beta}, "
            f"channel_length_modulation={self.channel_length_modulation}, "
            f"n_vgs={self.vgs_values.size})"
        )
