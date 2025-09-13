# examples/training_data_zener.py

import numpy as np
import pandas as pd
from semiconductor_sim import ZenerDiode

# Generate synthetic data
def generate_data(num_samples=1000):
    doping_p = np.random.uniform(1e16, 1e20, num_samples)
    doping_n = np.random.uniform(1e16, 1e20, num_samples)
    temperature = np.random.uniform(250, 400, num_samples)
    
    zener_voltage = 5.0 + 0.1 * np.log10(doping_p) - 0.05 * np.log10(doping_n) + 0.01 * temperature + np.random.normal(0, 0.2, num_samples)
    
    data = pd.DataFrame({
        'doping_p': doping_p,
        'doping_n': doping_n,
        'temperature': temperature,
        'zener_voltage': zener_voltage
    })
    
    return data

# Save data to CSV
data = generate_data()
data.to_csv('zener_training_data.csv', index=False)
