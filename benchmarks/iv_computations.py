"""Benchmarks for IV characteristic computations with and without acceleration."""

import numpy as np
from semiconductor_sim.devices.pn_junction import PNJunctionDiode
from semiconductor_sim.utils.numerics import (
    safe_expm1,
    safe_expm1_numba,
    safe_expm1_jax,
    get_accelerated_expm1,
    get_accelerated_diode_current,
)


class IVComputationBenchmarks:
    """Benchmarks for IV characteristic computations."""
    
    def setup(self):
        """Set up test data for benchmarks."""
        # Create voltage arrays of different sizes
        self.voltage_small = np.linspace(-1, 1, 100)
        self.voltage_medium = np.linspace(-1, 1, 1000)
        self.voltage_large = np.linspace(-1, 1, 10000)
        
        # Realistic device parameters
        self.I_s = 1e-14
        self.V_T = 0.026
        
        # Create a realistic PN junction diode
        self.diode = PNJunctionDiode(
            doping_p=1e16,
            doping_n=1e16,
            area=1e-4,
            temperature=300
        )
        
        # Get accelerated functions
        self.expm1_numpy = get_accelerated_expm1("numpy")
        self.expm1_auto = get_accelerated_expm1("auto")
        self.diode_current_numpy = get_accelerated_diode_current("numpy")
        self.diode_current_auto = get_accelerated_diode_current("auto")

    def time_safe_expm1_small_numpy(self):
        """Benchmark safe_expm1 with small array using numpy."""
        safe_expm1(self.voltage_small / self.V_T)

    def time_safe_expm1_small_numba(self):
        """Benchmark safe_expm1 with small array using numba."""
        safe_expm1_numba(self.voltage_small / self.V_T)

    def time_safe_expm1_small_jax(self):
        """Benchmark safe_expm1 with small array using JAX."""
        safe_expm1_jax(self.voltage_small / self.V_T)

    def time_safe_expm1_medium_numpy(self):
        """Benchmark safe_expm1 with medium array using numpy."""
        safe_expm1(self.voltage_medium / self.V_T)

    def time_safe_expm1_medium_numba(self):
        """Benchmark safe_expm1 with medium array using numba."""
        safe_expm1_numba(self.voltage_medium / self.V_T)

    def time_safe_expm1_medium_jax(self):
        """Benchmark safe_expm1 with medium array using JAX."""
        safe_expm1_jax(self.voltage_medium / self.V_T)

    def time_safe_expm1_large_numpy(self):
        """Benchmark safe_expm1 with large array using numpy."""
        safe_expm1(self.voltage_large / self.V_T)

    def time_safe_expm1_large_numba(self):
        """Benchmark safe_expm1 with large array using numba."""
        safe_expm1_numba(self.voltage_large / self.V_T)

    def time_safe_expm1_large_jax(self):
        """Benchmark safe_expm1 with large array using JAX."""
        safe_expm1_jax(self.voltage_large / self.V_T)

    def time_diode_current_small_numpy(self):
        """Benchmark diode current calculation with small array using numpy."""
        self.diode_current_numpy(self.voltage_small, self.I_s, self.V_T)

    def time_diode_current_small_auto(self):
        """Benchmark diode current calculation with small array using auto backend."""
        self.diode_current_auto(self.voltage_small, self.I_s, self.V_T)

    def time_diode_current_medium_numpy(self):
        """Benchmark diode current calculation with medium array using numpy."""
        self.diode_current_numpy(self.voltage_medium, self.I_s, self.V_T)

    def time_diode_current_medium_auto(self):
        """Benchmark diode current calculation with medium array using auto backend."""
        self.diode_current_auto(self.voltage_medium, self.I_s, self.V_T)

    def time_diode_current_large_numpy(self):
        """Benchmark diode current calculation with large array using numpy."""
        self.diode_current_numpy(self.voltage_large, self.I_s, self.V_T)

    def time_diode_current_large_auto(self):
        """Benchmark diode current calculation with large array using auto backend."""
        self.diode_current_auto(self.voltage_large, self.I_s, self.V_T)


class DeviceIVBenchmarks:
    """Benchmarks for complete device IV characteristic calculations."""
    
    def setup(self):
        """Set up test devices and voltage arrays."""
        # Different voltage array sizes
        self.voltage_small = np.linspace(-1, 1, 100)
        self.voltage_medium = np.linspace(-1, 1, 1000) 
        self.voltage_large = np.linspace(-1, 1, 10000)
        
        # Create test devices
        self.pn_diode = PNJunctionDiode(
            doping_p=1e16,
            doping_n=1e16,
            area=1e-4,
            temperature=300
        )

    def time_pn_junction_iv_small(self):
        """Benchmark PN junction IV calculation with small voltage array."""
        self.pn_diode.iv_characteristic(self.voltage_small)

    def time_pn_junction_iv_medium(self):
        """Benchmark PN junction IV calculation with medium voltage array."""
        self.pn_diode.iv_characteristic(self.voltage_medium)

    def time_pn_junction_iv_large(self):
        """Benchmark PN junction IV calculation with large voltage array."""
        self.pn_diode.iv_characteristic(self.voltage_large)

    def time_pn_junction_iv_with_recombination_small(self):
        """Benchmark PN junction IV with SRH recombination - small array."""
        n_conc = 1e15
        p_conc = 1e15
        self.pn_diode.iv_characteristic(self.voltage_small, n_conc=n_conc, p_conc=p_conc)

    def time_pn_junction_iv_with_recombination_medium(self):
        """Benchmark PN junction IV with SRH recombination - medium array."""
        n_conc = 1e15
        p_conc = 1e15
        self.pn_diode.iv_characteristic(self.voltage_medium, n_conc=n_conc, p_conc=p_conc)

    def time_pn_junction_iv_with_recombination_large(self):
        """Benchmark PN junction IV with SRH recombination - large array."""
        n_conc = 1e15
        p_conc = 1e15
        self.pn_diode.iv_characteristic(self.voltage_large, n_conc=n_conc, p_conc=p_conc)


class MemoryBenchmarks:
    """Memory usage benchmarks."""
    
    def setup(self):
        """Set up for memory benchmarks."""
        self.voltage = np.linspace(-1, 1, 10000)
        self.I_s = 1e-14
        self.V_T = 0.026
        
        self.diode_current_numpy = get_accelerated_diode_current("numpy")
        self.diode_current_auto = get_accelerated_diode_current("auto")

    def peakmem_diode_current_numpy(self):
        """Memory usage for diode current calculation with numpy."""
        return self.diode_current_numpy(self.voltage, self.I_s, self.V_T)

    def peakmem_diode_current_auto(self):
        """Memory usage for diode current calculation with auto backend."""
        return self.diode_current_auto(self.voltage, self.I_s, self.V_T)

    def peakmem_safe_expm1_numpy(self):
        """Memory usage for safe_expm1 with numpy."""
        return safe_expm1(self.voltage / self.V_T)

    def peakmem_safe_expm1_auto(self):
        """Memory usage for safe_expm1 with auto backend."""
        expm1_auto = get_accelerated_exmp1("auto")
        return expm1_auto(self.voltage / self.V_T)