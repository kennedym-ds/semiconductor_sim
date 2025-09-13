"""IV characteristic command implementation."""

import argparse
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any
import matplotlib.pyplot as plt

from ..utils import load_config, create_device, save_data_csv, create_voltage_range
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style


def setup_parser(subparsers) -> None:
    """Set up the IV command parser."""
    parser = subparsers.add_parser(
        'iv',
        help='Generate IV characteristics for semiconductor devices',
        description='Generate current-voltage (IV) characteristics for various semiconductor devices',
    )
    
    parser.add_argument(
        'device_type',
        help='Type of device (pn_junction, led, solar_cell, zener, mos_capacitor, tunnel_diode, varactor)',
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Device configuration file (JSON or YAML)',
        required=True,
    )
    
    parser.add_argument(
        '--voltage-start', '-vs',
        type=float,
        default=-1.0,
        help='Starting voltage (V, default: -1.0)',
    )
    
    parser.add_argument(
        '--voltage-stop', '-ve',
        type=float, 
        default=1.0,
        help='Ending voltage (V, default: 1.0)',
    )
    
    parser.add_argument(
        '--voltage-points', '-vp',
        type=int,
        default=100,
        help='Number of voltage points (default: 100)',
    )
    
    parser.add_argument(
        '--n-conc',
        type=float,
        help='Electron concentration (cm^-3)',
    )
    
    parser.add_argument(
        '--p-conc',
        type=float,
        help='Hole concentration (cm^-3)',
    )
    
    parser.add_argument(
        '--output-csv', '-o',
        help='Output CSV file path (optional)',
    )
    
    parser.add_argument(
        '--output-png',
        help='Output PNG file path (optional)',
    )
    
    parser.add_argument(
        '--temperature', '-T',
        type=float,
        help='Override temperature (K) from config file',
    )


def run(args) -> int:
    """Run the IV characteristic command."""
    try:
        # Load device configuration
        config = load_config(args.config)
        
        # Override temperature if specified
        if args.temperature is not None:
            config['temperature'] = args.temperature
        
        # Create device
        device = create_device(args.device_type, config)
        
        # Create voltage range
        voltage = create_voltage_range(args.voltage_start, args.voltage_stop, args.voltage_points)
        
        # Prepare carrier concentrations
        n_conc = None
        p_conc = None
        if args.n_conc is not None and args.p_conc is not None:
            n_conc = np.full_like(voltage, args.n_conc)
            p_conc = np.full_like(voltage, args.p_conc)
        
        # Calculate IV characteristics
        result = device.iv_characteristic(voltage, n_conc, p_conc)
        current = result[0]
        
        # Handle additional output (like recombination)
        extra_data = {}
        if len(result) > 1:
            extra_data['Recombination (cm^-3 s^-1)'] = result[1]
        
        print(f"Calculated IV characteristics for {args.device_type}")
        print(f"Voltage range: {voltage[0]:.3f} to {voltage[-1]:.3f} V")
        print(f"Current range: {current.min():.3e} to {current.max():.3e} A")
        
        # Save CSV if requested
        if args.output_csv:
            save_data_csv(args.output_csv, voltage, current, extra_data=extra_data)
            print(f"Data saved to: {args.output_csv}")
        
        # Save PNG if requested
        if args.output_png:
            save_plot(voltage, current, device, args.output_png, extra_data=extra_data)
            print(f"Plot saved to: {args.output_png}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


def save_plot(voltage: np.ndarray, current: np.ndarray, device, 
              output_path: str, extra_data: Optional[Dict[str, np.ndarray]] = None) -> None:
    """Save IV plot to PNG file."""
    use_headless_backend("Agg")
    apply_basic_style()
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Main IV plot
    color = "tab:blue"
    ax1.set_xlabel("Voltage (V)")
    ax1.set_ylabel("Current (A)", color=color)
    ax1.plot(voltage, current, color=color, linewidth=2, label="IV Characteristic")
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # Add secondary axis for extra data if available
    if extra_data and len(extra_data) > 0:
        ax2 = ax1.twinx()
        colors = ["tab:green", "tab:red", "tab:orange"]
        for i, (label, data) in enumerate(extra_data.items()):
            color = colors[i % len(colors)]
            ax2.plot(voltage, data, color=color, linewidth=2, linestyle='--', label=label)
            ax2.set_ylabel(label, color=color)
            ax2.tick_params(axis="y", labelcolor=color)
    
    # Add title and device info
    device_name = device.__class__.__name__
    plt.title(f"IV Characteristics - {device_name}\nT = {device.temperature:.1f} K")
    
    # Save plot
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()