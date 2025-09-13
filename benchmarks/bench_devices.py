"""Benchmarks for semiconductor device simulations."""

import numpy as np
from semiconductor_sim.devices import PNJunctionDiode, LED, SolarCell, ZenerDiode


class DeviceBenchmarks:
    """Benchmark the core device simulation performance."""
    
    def setup(self):
        """Set up benchmark parameters."""
        self.voltages = np.linspace(-2, 2, 1000)
        self.large_voltages = np.linspace(-5, 5, 10000)
        
        # Standard device parameters
        self.doping_p = 1e17
        self.doping_n = 1e17
        self.temperature = 300
        
    def time_pn_junction_iv_curve(self):
        """Benchmark PN junction I-V characteristic calculation."""
        diode = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            temperature=self.temperature
        )
        return diode.iv_characteristic(self.voltages)
    
    def time_pn_junction_large_array(self):
        """Benchmark PN junction with large voltage array."""
        diode = PNJunctionDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            temperature=self.temperature
        )
        return diode.iv_characteristic(self.large_voltages)
    
    def time_led_iv_curve(self):
        """Benchmark LED I-V characteristic calculation."""
        led = LED(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            temperature=self.temperature,
            bandgap=1.9  # Red LED bandgap
        )
        return led.iv_characteristic(self.voltages)
    
    def time_solar_cell_iv_curve(self):
        """Benchmark solar cell I-V characteristic calculation."""
        solar_cell = SolarCell(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            temperature=self.temperature,
            illumination=1000  # 1 sun
        )
        return solar_cell.iv_characteristic(self.voltages)
    
    def time_zener_diode_iv_curve(self):
        """Benchmark Zener diode I-V characteristic calculation."""
        zener = ZenerDiode(
            doping_p=self.doping_p,
            doping_n=self.doping_n,
            temperature=self.temperature,
            breakdown_voltage=5.1
        )
        return zener.iv_characteristic(self.voltages)


class MemoryBenchmarks:
    """Benchmark memory usage of device simulations."""
    
    def setup(self):
        """Set up benchmark parameters."""
        self.voltages = np.linspace(-2, 2, 1000)
        
    def peakmem_pn_junction_large_simulation(self):
        """Benchmark memory usage for large PN junction simulation."""
        diode = PNJunctionDiode(doping_p=1e17, doping_n=1e17, temperature=300)
        # Create large voltage array to test memory usage
        large_voltages = np.linspace(-10, 10, 100000)
        return diode.iv_characteristic(large_voltages)