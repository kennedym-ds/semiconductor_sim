# semiconductor_sim/devices/zener_diode.py

import numpy as np
from semiconductor_sim.utils import q, k_B, DEFAULT_T
from semiconductor_sim.models import srh_recombination
from semiconductor_sim.utils.numerics import safe_expm1
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style
import matplotlib.pyplot as plt
import joblib
import os
from .base import Device


class ZenerDiode(Device):
    def __init__(self, doping_p, doping_n, area=1e-4, zener_voltage=5.0, temperature=300, tau_n=1e-6, tau_p=1e-6):
        """
        Initialize the Zener Diode.

        Parameters:
            doping_p (float): Acceptor concentration in p-region (cm^-3)
            doping_n (float): Donor concentration in n-region (cm^-3)
            area (float): Cross-sectional area of the diode (cm^2)
            zener_voltage (float): Zener breakdown voltage (V)
            temperature (float): Temperature in Kelvin
            tau_n (float): Electron lifetime (s)
            tau_p (float): Hole lifetime (s)
        """
        super().__init__(area=area, temperature=temperature)
        self.doping_p = doping_p
        self.doping_n = doping_n
        self.zener_voltage = zener_voltage
        self.tau_n = tau_n
        self.tau_p = tau_p
        self.I_s = self.calculate_saturation_current()
        self.model = self.load_ml_model()

    def calculate_saturation_current(self):
        """
        Calculate the saturation current (I_s) considering temperature.
        """
        D_n = 25  # Electron diffusion coefficient (cm^2/s)
        D_p = 10  # Hole diffusion coefficient (cm^2/s)
        L_n = 5e-4  # Electron diffusion length (cm)
        L_p = 5e-4  # Hole diffusion length (cm)
        n_i = 1.5e10 * (self.temperature / DEFAULT_T)**1.5  # Intrinsic carrier concentration

        I_s = q * self.area * n_i**2 * (
            (D_p / (L_p * self.doping_n)) +
            (D_n / (L_n * self.doping_p))
        )
        return I_s

    def load_ml_model(self):
        """
        Load the pre-trained ML model for predicting Zener voltage.
        """
        model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'zener_voltage_rf_model.pkl')
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            return model
        else:
            print("ML model for Zener voltage not found. Using default value.")
            return None

    def predict_zener_voltage(self):
        """
        Predict the Zener voltage using the ML model.

        Returns:
            predicted_zener_voltage (float): Predicted Zener voltage (V)
        """
        if self.model:
            input_features = np.array([[self.doping_p, self.doping_n, self.temperature]])
            predicted_zener_voltage = self.model.predict(input_features)[0]
            return predicted_zener_voltage
        else:
            return self.zener_voltage

    def iv_characteristic(self, voltage_array, n_conc=None, p_conc=None):
        """
        Calculate the current for a given array of voltages, including SRH recombination.

        Parameters:
            voltage_array (np.ndarray): Array of voltage values (V)
            n_conc (float or np.ndarray): Electron concentration (cm^-3)
            p_conc (float or np.ndarray): Hole concentration (cm^-3)

        Returns:
            current_array (np.ndarray): Array of current values (A)
            recombination_array (np.ndarray): Array of recombination rates (cm^-3 s^-1)
        """
        # Update Zener voltage prediction
        self.zener_voltage = self.predict_zener_voltage()
        
        V_T = k_B * self.temperature / q  # Thermal voltage
        I = self.I_s * safe_expm1(voltage_array / V_T)

        # Implement Zener breakdown
        I_breakdown = np.where(
            voltage_array >= self.zener_voltage,
            0.1 * self.I_s * (voltage_array - self.zener_voltage),
            0,
        )
        I += I_breakdown

        if n_conc is not None and p_conc is not None:
            R_SRH = srh_recombination(n_conc, p_conc, temperature=self.temperature, tau_n=self.tau_n, tau_p=self.tau_p)
            R_SRH = np.broadcast_to(R_SRH, np.shape(voltage_array))
        else:
            R_SRH = np.zeros_like(voltage_array)

        return np.asarray(I), np.asarray(R_SRH)

    def plot_iv_characteristic(self, voltage, current, recombination=None):
        """
        Plot the IV characteristics and optionally the recombination rate.

        Parameters:
            voltage (np.ndarray): Voltage values (V)
            current (np.ndarray): Current values (A)
            recombination (np.ndarray, optional): Recombination rates (cm^-3 s^-1)
        """
        use_headless_backend("Agg")
        apply_basic_style()
        fig, ax1 = plt.subplots(figsize=(8,6))

        color = 'tab:blue'
        ax1.set_xlabel('Voltage (V)')
        ax1.set_ylabel('Current (A)', color=color)
        ax1.plot(voltage, current, color=color, label='IV Characteristic')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True)

        if recombination is not None:
            ax2 = ax1.twinx()
            color = 'tab:green'
            ax2.set_ylabel('Recombination Rate (cm$^{-3}$ s$^{-1}$)', color=color)
            ax2.plot(voltage, recombination, color=color, label='SRH Recombination')
            ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()
        plt.title('Zener Diode IV Characteristics')
        plt.show()
