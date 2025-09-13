# examples/example_led.py

import numpy as np
from semiconductor_sim import LED

def main():
    import plotly.graph_objects as go

    # Define voltage range
    voltage = np.linspace(-0.5, 0.7, 200)

    # Initialize the LED with doping concentrations, efficiency, temperature, and radiative recombination coefficient
    led = LED(doping_p=1e17, doping_n=1e17, efficiency=0.2, temperature=300, B=1e-10)

    # Assume constant carrier concentrations for simplicity
    n_conc = np.full_like(voltage, 1e16)  # cm^-3
    p_conc = np.full_like(voltage, 1e16)  # cm^-3

    # Calculate current, emission, and recombination rate
    current, emission, recombination = led.iv_characteristic(voltage, n_conc, p_conc)

    # Plot IV characteristics with recombination and emission
    led.plot_iv_characteristic(voltage, current, emission, recombination)

if __name__ == "__main__":
    main()
