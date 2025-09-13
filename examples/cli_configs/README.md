# CLI Configuration Examples

This directory contains example configuration files for the `semiconductor-sim` CLI tool.

## Quick Start

After installing the package, you can use these configurations to quickly generate device characteristics:

### IV Characteristics

```bash
# PN Junction Diode
semiconductor-sim iv pn_junction --config pn_junction.json --output-csv pn_iv.csv --output-png pn_iv.png

# LED  
semiconductor-sim iv led --config led.json --output-csv led_iv.csv --output-png led_iv.png

# Solar Cell
semiconductor-sim iv solar_cell --config solar_cell.json --output-csv solar_iv.csv --output-png solar_iv.png

# Zener Diode
semiconductor-sim iv zener --config zener_diode.json --output-csv zener_iv.csv --output-png zener_iv.png
```

### CV Characteristics

```bash
# MOS Capacitor
semiconductor-sim cv mos_capacitor --config mos_capacitor.yaml --output-csv mos_cv.csv --output-png mos_cv.png
```

### Parameter Sweeps

```bash
# Temperature sweep on PN junction
semiconductor-sim sweep pn_junction --config pn_junction.json \
  --sweep-param temperature --sweep-start 250 --sweep-stop 350 --sweep-points 5 \
  --output-csv temp_sweep.csv --output-png temp_sweep.png

# Doping concentration sweep  
semiconductor-sim sweep pn_junction --config pn_junction.json \
  --sweep-param doping_p --sweep-start 1e16 --sweep-stop 1e18 --sweep-points 5 \
  --output-csv doping_sweep.csv --output-png doping_sweep.png
```

## Configuration File Format

Configuration files can be in JSON or YAML format and should contain the device parameters.

### Example JSON (pn_junction.json):
```json
{
  "doping_p": 1e17,
  "doping_n": 1e17,
  "area": 1e-4,
  "temperature": 300,
  "tau_n": 1e-6,
  "tau_p": 1e-6
}
```

### Example YAML (mos_capacitor.yaml):
```yaml
doping_p: 1.0e+17
oxide_thickness: 1.0e-6
oxide_permittivity: 3.45
area: 1.0e-4
temperature: 300
tau_n: 1.0e-6
tau_p: 1.0e-6
```

## Available Commands

- `iv`: Generate current-voltage characteristics
- `cv`: Generate capacitance-voltage characteristics (for capacitive devices)
- `sweep`: Perform parameter sweeps

## Available Device Types

- `pn_junction`: PN Junction Diode
- `led`: Light Emitting Diode
- `solar_cell`: Solar Cell
- `zener`: Zener Diode  
- `mos_capacitor`: MOS Capacitor
- `tunnel_diode`: Tunnel Diode
- `varactor`: Varactor Diode

## Getting Help

```bash
semiconductor-sim --help
semiconductor-sim iv --help
semiconductor-sim cv --help
semiconductor-sim sweep --help
```