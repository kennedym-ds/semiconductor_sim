#!/bin/bash
# Example script demonstrating the semiconductor-sim CLI
# Run this script to generate example outputs

echo "=== Semiconductor Simulation CLI Demo ==="
echo

# Create output directory
mkdir -p cli_demo_output

echo "1. Generating PN Junction IV characteristics..."
python -m semiconductor_sim.cli.main iv pn_junction \
  --config examples/cli_configs/pn_junction.json \
  --output-csv cli_demo_output/pn_iv.csv \
  --output-png cli_demo_output/pn_iv.png \
  --voltage-start -1.0 --voltage-stop 1.0 --voltage-points 100

echo "2. Generating LED IV characteristics..."
python -m semiconductor_sim.cli.main iv led \
  --config examples/cli_configs/led.json \
  --output-csv cli_demo_output/led_iv.csv \
  --output-png cli_demo_output/led_iv.png \
  --voltage-start 0 --voltage-stop 3.0 --voltage-points 100

echo "3. Generating MOS Capacitor CV characteristics..."
python -m semiconductor_sim.cli.main cv mos_capacitor \
  --config examples/cli_configs/mos_capacitor.yaml \
  --output-csv cli_demo_output/mos_cv.csv \
  --output-png cli_demo_output/mos_cv.png \
  --voltage-start -3.0 --voltage-stop 3.0 --voltage-points 100

echo "4. Performing temperature sweep on PN junction..."
python -m semiconductor_sim.cli.main sweep pn_junction \
  --config examples/cli_configs/pn_junction.json \
  --sweep-param temperature --sweep-start 250 --sweep-stop 350 --sweep-points 5 \
  --output-csv cli_demo_output/temp_sweep.csv \
  --output-png cli_demo_output/temp_sweep.png \
  --voltage-start -0.5 --voltage-stop 0.8 --voltage-points 50

echo "5. Performing doping concentration sweep..."
python -m semiconductor_sim.cli.main sweep pn_junction \
  --config examples/cli_configs/pn_junction.json \
  --sweep-param doping_p --sweep-start 1e16 --sweep-stop 1e18 --sweep-points 4 \
  --output-csv cli_demo_output/doping_sweep.csv \
  --output-png cli_demo_output/doping_sweep.png \
  --voltage-start -0.5 --voltage-stop 0.8 --voltage-points 50

echo
echo "=== Demo Complete ==="
echo "Output files saved to: cli_demo_output/"
echo "View the generated PNG files to see the device characteristics!"
echo
echo "Files generated:"
ls -la cli_demo_output/