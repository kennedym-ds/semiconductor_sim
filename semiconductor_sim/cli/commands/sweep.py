"""Parameter sweep command implementation."""

import argparse
import numpy as np
from pathlib import Path
from typing import Dict, Any, List
import matplotlib.pyplot as plt

from ..utils import load_config, create_device, save_data_csv, create_voltage_range
from semiconductor_sim.utils.plotting import use_headless_backend, apply_basic_style


def setup_parser(subparsers) -> None:
    """Set up the sweep command parser."""
    parser = subparsers.add_parser(
        'sweep',
        help='Perform parameter sweeps on semiconductor devices',
        description='Perform parameter sweeps to analyze device behavior across different conditions',
    )
    
    parser.add_argument(
        'device_type',
        help='Type of device (pn_junction, led, solar_cell, zener, mos_capacitor, tunnel_diode, varactor)',
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Base device configuration file (JSON or YAML)',
        required=True,
    )
    
    parser.add_argument(
        '--sweep-param',
        help='Parameter to sweep (e.g., temperature, doping_p, doping_n)',
        required=True,
    )
    
    parser.add_argument(
        '--sweep-start',
        type=float,
        help='Starting value for sweep parameter',
        required=True,
    )
    
    parser.add_argument(
        '--sweep-stop', 
        type=float,
        help='Ending value for sweep parameter',
        required=True,
    )
    
    parser.add_argument(
        '--sweep-points',
        type=int,
        default=5,
        help='Number of sweep points (default: 5)',
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
        '--output-csv', '-o',
        help='Output CSV file path (optional)',
    )
    
    parser.add_argument(
        '--output-png',
        help='Output PNG file path (optional)',
    )
    
    parser.add_argument(
        '--characteristic',
        choices=['iv', 'cv'],
        default='iv',
        help='Type of characteristic to sweep (default: iv)',
    )


def run(args) -> int:
    """Run the parameter sweep command."""
    try:
        # Load base device configuration
        base_config = load_config(args.config)
        
        # Create sweep parameter values
        sweep_values = np.linspace(args.sweep_start, args.sweep_stop, args.sweep_points)
        
        # Create voltage range
        voltage = create_voltage_range(args.voltage_start, args.voltage_stop, args.voltage_points)
        
        # Store results
        results = {}
        sweep_param = args.sweep_param
        
        print(f"Performing {sweep_param} sweep on {args.device_type}")
        print(f"Sweep range: {args.sweep_start} to {args.sweep_stop} ({args.sweep_points} points)")
        
        for i, sweep_val in enumerate(sweep_values):
            # Create device config for this sweep point
            config = base_config.copy()
            config[sweep_param] = sweep_val
            
            try:
                # Create device
                device = create_device(args.device_type, config)
                
                if args.characteristic == 'cv':
                    if not hasattr(device, 'capacitance'):
                        raise ValueError(f"Device type '{args.device_type}' does not support CV characteristics")
                    capacitance = device.capacitance(voltage)
                    current, _ = device.iv_characteristic(voltage)
                    results[f'{sweep_param}={sweep_val:.3e}'] = {
                        'voltage': voltage,
                        'current': current,
                        'capacitance': capacitance,
                        'sweep_value': sweep_val
                    }
                else:
                    # IV characteristics
                    current, *extra = device.iv_characteristic(voltage)
                    results[f'{sweep_param}={sweep_val:.3e}'] = {
                        'voltage': voltage,
                        'current': current,
                        'sweep_value': sweep_val
                    }
                    if extra:
                        results[f'{sweep_param}={sweep_val:.3e}']['extra'] = extra[0]
                
                print(f"  Point {i+1}/{args.sweep_points}: {sweep_param} = {sweep_val:.3e}")
                
            except Exception as e:
                print(f"  Warning: Failed at {sweep_param} = {sweep_val:.3e}: {e}")
                continue
        
        if not results:
            raise RuntimeError("No valid sweep points calculated")
        
        print(f"Successfully calculated {len(results)} sweep points")
        
        # Save CSV if requested
        if args.output_csv:
            save_sweep_csv(args.output_csv, results, args.characteristic)
            print(f"Data saved to: {args.output_csv}")
        
        # Save PNG if requested
        if args.output_png:
            save_sweep_plot(args.output_png, results, args.characteristic, sweep_param)
            print(f"Plot saved to: {args.output_png}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


def save_sweep_csv(filename: str, results: Dict[str, Dict], characteristic: str) -> None:
    """Save sweep results to CSV file."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get first result to determine structure
    first_key = next(iter(results.keys()))
    first_result = results[first_key]
    voltage = first_result['voltage']
    
    import csv
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        header = ['Voltage (V)']
        for key in results.keys():
            header.append(f'Current_{key} (A)')
            if characteristic == 'cv' and 'capacitance' in results[key]:
                header.append(f'Capacitance_{key} (F)')
        
        writer.writerow(header)
        
        # Write data
        for i in range(len(voltage)):
            row = [voltage[i]]
            for key, data in results.items():
                row.append(data['current'][i])
                if characteristic == 'cv' and 'capacitance' in data:
                    row.append(data['capacitance'][i])
            writer.writerow(row)


def save_sweep_plot(filename: str, results: Dict[str, Dict], characteristic: str, sweep_param: str) -> None:
    """Save sweep plot to PNG file."""
    use_headless_backend("Agg")
    apply_basic_style()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(results)))
    
    for i, (key, data) in enumerate(results.items()):
        voltage = data['voltage']
        current = data['current']
        sweep_val = data['sweep_value']
        
        if characteristic == 'cv' and 'capacitance' in data:
            # Plot capacitance
            capacitance = data['capacitance']
            ax.plot(voltage, capacitance * 1e12, color=colors[i], linewidth=2, 
                   label=f'{sweep_param} = {sweep_val:.3e}')
            ax.set_ylabel('Capacitance (pF)')
            ax.set_title(f'CV Characteristics - {sweep_param} Sweep')
        else:
            # Plot current
            ax.semilogy(voltage, np.abs(current), color=colors[i], linewidth=2,
                       label=f'{sweep_param} = {sweep_val:.3e}')
            ax.set_ylabel('Current (A)')
            ax.set_title(f'IV Characteristics - {sweep_param} Sweep')
    
    ax.set_xlabel('Voltage (V)')
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Save plot
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()