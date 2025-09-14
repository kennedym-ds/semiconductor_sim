from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt

from semiconductor_sim.utils import DEFAULT_T


class Device(ABC):
    """
    Abstract base class for semiconductor devices.

    Provides common fields and establishes a standard API for IV
    characteristics. Subclasses must implement `iv_characteristic`.
    """

    def __init__(self, area: float = 1e-4, temperature: float = DEFAULT_T) -> None:
        if not np.isfinite(area) or area <= 0:
            raise ValueError("area must be a positive finite value (cm^2)")
        if not np.isfinite(temperature) or temperature <= 0:
            raise ValueError("temperature must be a positive finite value (K)")
        self.area = area
        self.temperature = temperature

    @abstractmethod
    def iv_characteristic(
        self,
        voltage_array: npt.NDArray[np.floating],
        n_conc: float | npt.NDArray[np.floating] | None = None,
        p_conc: float | npt.NDArray[np.floating] | None = None,
    ) -> tuple[npt.NDArray[np.floating], ...]:
        """
        Compute current vs. voltage. Implementations must return a tuple where the
        first element is the current array, and optional subsequent arrays include
        model-specific outputs (e.g., recombination rates, emission).
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}(area={self.area}, temperature={self.temperature})"
