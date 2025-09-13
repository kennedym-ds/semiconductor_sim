# semiconductor_sim/devices/led.py

import numpy as np
from typing import Optional, Tuple
from semiconductor_sim.utils import q, k_B, DEFAULT_T
from semiconductor_sim.models import srh_recombination, radiative_recombination
from semiconductor_sim.utils.numerics import safe_expm1
import matplotlib.pyplot as plt
from .base import Device

class LED(Device):
    """Light-emitting diode (LED) model.

    Assumptions:
    - Ideal diode IV: I = I_s * (exp(V/V_T) - 1)
    - Emission ~ efficiency * radiative_recombination * area (simplified)
    - Default transport parameters (D, L) represent typical pedagogical values
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
        """
        super().__init__(area=area, temperature=temperature)
        if not (0.0 <= efficiency <= 1.0):
            raise ValueError("efficiency must be between 0 and 1")
        self.doping_p = float(doping_p)
        self.doping_n = float(doping_n)
        self.efficiency = float(efficiency)
        self.B = float(B)  # Radiative recombination coefficient
        self.D_n = float(D_n)
        self.D_p = float(D_p)
        self.L_n = float(L_n)
        self.L_p = float(L_p)
        self.I_s = self.calculate_saturation_current()

    @classmethod
    def from_preset(
        cls,
        material: str,
        doping_p: float,
        doping_n: float,
        area: float = 1e-4,
        efficiency: float = 0.1,
        temperature: float = DEFAULT_T,
        **kwargs
    ) -> "LED":
        """Create an LED using material presets.
        
        Args:
            material: Material name (e.g., "GaAs", "GaN", "InP")
            doping_p: Acceptor concentration in p-region (cm^-3)
            doping_n: Donor concentration in n-region (cm^-3)
            area: Cross-sectional area of the LED (cm^2)
            efficiency: Radiative recombination efficiency (0 to 1)
            temperature: Operating temperature (K)
            **kwargs: Override specific material parameters
            
        Returns:
            LED instance with material-specific parameters
            
        Raises:
            ImportError: If pydantic is not installed
            ValueError: If material is not found
            
        Example:
            >>> led = LED.from_preset("GaAs", doping_p=1e17, doping_n=1e18, efficiency=0.8)
            >>> led_custom = LED.from_preset("GaN", 1e17, 1e18, B=5e-11)
        """
        try:
            from ..schemas.material_presets import get_material_properties
        except ImportError:
            raise ImportError(
                "Material presets require the schemas module. "
                "Install with: pip install semiconductor-sim[schemas]"
            )
        
        # Get material properties
        material_props = get_material_properties(material)
        
        # Start with material defaults, but only use parameters that the LED class accepts
        params = {
            'doping_p': doping_p,
            'doping_n': doping_n,
            'area': area,
            'efficiency': efficiency,
            'temperature': temperature,
            'B': material_props.B,
            'D_n': material_props.D_n,
            'D_p': material_props.D_p,
            'L_n': material_props.L_n,
            'L_p': material_props.L_p,
        }
        
        # Override with any user-provided values
        params.update(kwargs)
        
        # Validate parameters if schemas are available
        try:
            from ..schemas.device_schemas import LEDSchema
            schema = LEDSchema(**params)
            validated_params = schema.model_dump()
        except ImportError:
            # If schemas not available, use params as-is
            validated_params = params
        
        return cls(**validated_params)

    def calculate_saturation_current(self) -> float:
        """
        Calculate the saturation current (I_s) considering temperature.

        Returns:
            float: The saturation current in amperes.
        """
        n_i = 1.5e10 * (self.temperature / DEFAULT_T) ** 1.5
        I_s = q * self.area * n_i**2 * (
            (self.D_p / (self.L_p * self.doping_n)) + (self.D_n / (self.L_n * self.doping_p))
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
        I = self.I_s * safe_expm1(voltage_array / V_T)

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
        return (
            f"LED(doping_p={self.doping_p}, doping_n={self.doping_n}, area={self.area}, "
            f"efficiency={self.efficiency}, temperature={self.temperature}, B={self.B})"
        )
