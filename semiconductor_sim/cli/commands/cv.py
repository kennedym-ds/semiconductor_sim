"""CV characteristic command implementation."""

import argparse
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any
import matplotlib.pyplot as plt

from ..utils import load_config, create_device, save_data_csv, create_voltage_range
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style


def setup_parser(subparsers) -> None:
    """Set up the CV command parser."""
    parser = subparsers.add_parser(
        'cv',
        help='Generate CV characteristics for capacitive devices',
        description='Generate capacitance-voltage (CV) characteristics for capacitive semiconductor devices',
    )
    
    parser.add_argument(
        'device_type',
        help='Type of device (currently supports: mos_capacitor, varactor)',
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Device configuration file (JSON or YAML)',
        required=True,
    )
    
    parser.add_argument(
        '--voltage-start', '-vs',
        type=float,
        default=-2.0,
        help='Starting voltage (V, default: -2.0)',
    )
    
    parser.add_argument(
        '--voltage-stop', '-ve',
        type=float, 
        default=2.0,
        help='Ending voltage (V, default: 2.0)',
    )
    
    parser.add_argument(
        '--voltage-points', '-vp',
        type=int,
        default=100,
        help='Number of voltage points (default: 100)',
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
    """Run the CV characteristic command."""
    try:
        # Load device configuration
        config = load_config(args.config)
        
        # Override temperature if specified
        if args.temperature is not None:
            config['temperature'] = args.temperature
        
        # Create device
        device = create_device(args.device_type, config)
        
        # Check if device supports capacitance calculation
        if not hasattr(device, 'capacitance'):
            raise ValueError(f"Device type '{args.device_type}' does not support CV characteristics")
        
        # Create voltage range
        voltage = create_voltage_range(args.voltage_start, args.voltage_stop, args.voltage_points)
        
        # Calculate CV characteristics
        capacitance = device.capacitance(voltage)
        
        # Also get IV characteristics for completeness
        current, _ = device.iv_characteristic(voltage)
        
        print(f"Calculated CV characteristics for {args.device_type}")
        print(f"Voltage range: {voltage[0]:.3f} to {voltage[-1]:.3f} V")
        print(f"Capacitance range: {capacitance.min():.3e} to {capacitance.max():.3e} F")
        
        # Save CSV if requested
        if args.output_csv:
            save_data_csv(args.output_csv, voltage, current, capacitance=capacitance)
            print(f"Data saved to: {args.output_csv}")
        
        # Save PNG if requested
        if args.output_png:
            save_plot(voltage, capacitance, current, device, args.output_png)
            print(f"Plot saved to: {args.output_png}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


def save_plot(voltage: np.ndarray, capacitance: np.ndarray, current: np.ndarray,
              device, output_path: str) -> None:
    """Save CV plot to PNG file."""
    use_headless_backend("Agg")
    apply_basic_style()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # CV plot
    ax1.plot(voltage, capacitance * 1e12, 'b-', linewidth=2, label='Capacitance')
    ax1.set_xlabel("Voltage (V)")
    ax1.set_ylabel("Capacitance (pF)")
    ax1.grid(True, alpha=0.3)
    ax1.set_title(f"CV Characteristics - {device.__class__.__name__}")
    
    # IV plot (secondary)
    ax2.semilogy(voltage, np.abs(current), 'r-', linewidth=2, label='|Current|')
    ax2.set_xlabel("Voltage (V)")
    ax2.set_ylabel("Current (A)")
    ax2.grid(True, alpha=0.3)
    ax2.set_title("IV Characteristics (Log Scale)")
    
    # Add device info
    fig.suptitle(f"Device Characteristics - T = {device.temperature:.1f} K", fontsize=14)
    
    # Save plot
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()