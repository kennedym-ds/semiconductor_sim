"""Common utilities for CLI commands."""

import json
import yaml
import csv
import numpy as np
from pathlib import Path
from typing import Dict, Any, Union, Optional

# Import after we've checked the package is installed
import semiconductor_sim
from semiconductor_sim import PNJunctionDiode, LED, SolarCell, ZenerDiode, MOSCapacitor, TunnelDiode, VaractorDiode


def load_config(config_path: str) -> Dict[str, Any]:
    """Load device configuration from JSON or YAML file."""
    path = Path(config_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(path, 'r') as f:
        if path.suffix.lower() in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif path.suffix.lower() == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {path.suffix}")


def create_device(device_type: str, params: Dict[str, Any]):
    """Create a device instance from type and parameters."""
    device_classes = {
        'pn_junction': PNJunctionDiode,
        'pnjunction': PNJunctionDiode,
        'led': LED,
        'solar_cell': SolarCell,
        'solarcell': SolarCell,
        'zener': ZenerDiode,
        'zener_diode': ZenerDiode,
        'mos_capacitor': MOSCapacitor,
        'moscapacitor': MOSCapacitor,
        'tunnel_diode': TunnelDiode,
        'tunneldiode': TunnelDiode,
        'varactor': VaractorDiode,
        'varactor_diode': VaractorDiode,
    }
    
    device_type_lower = device_type.lower()
    if device_type_lower not in device_classes:
        available = ', '.join(sorted(set(device_classes.keys())))
        raise ValueError(f"Unknown device type '{device_type}'. Available: {available}")
    
    device_class = device_classes[device_type_lower]
    return device_class(**params)


def save_data_csv(filename: str, voltage: np.ndarray, current: np.ndarray, 
                  capacitance: Optional[np.ndarray] = None, 
                  extra_data: Optional[Dict[str, np.ndarray]] = None) -> None:
    """Save simulation data to CSV file."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        header = ['Voltage (V)', 'Current (A)']
        if capacitance is not None:
            header.append('Capacitance (F)')
        
        if extra_data:
            for key in extra_data:
                header.append(key)
        
        writer.writerow(header)
        
        # Write data
        for i in range(len(voltage)):
            row = [voltage[i], current[i]]
            if capacitance is not None:
                row.append(capacitance[i])
            
            if extra_data:
                for key, data in extra_data.items():
                    row.append(data[i] if i < len(data) else '')
            
            writer.writerow(row)


def create_voltage_range(start: float, stop: float, num_points: int = 100) -> np.ndarray:
    """Create a voltage range array."""
    return np.linspace(start, stop, num_points)