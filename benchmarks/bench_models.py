"""Benchmarks for numerical utilities and physics models."""

import numpy as np
from semiconductor_sim.models import srh_recombination, auger_recombination, radiative_recombination
from semiconductor_sim.utils.numerics import safe_expm1


class PhysicsModelBenchmarks:
    """Benchmark physics model calculations."""
    
    def setup(self):
        """Set up benchmark parameters."""
        # Carrier concentration arrays
        self.n = np.logspace(15, 19, 1000)  # electron concentration (cm^-3)
        self.p = np.logspace(15, 19, 1000)  # hole concentration (cm^-3)
        self.ni = 1.5e10  # intrinsic carrier concentration at 300K
        
        # Recombination parameters
        self.tau_n = 1e-6  # electron lifetime (s)
        self.tau_p = 1e-6  # hole lifetime (s)
        self.Cn = 2.8e-31  # Auger coefficient for electrons (cm^6/s)
        self.Cp = 9.9e-32  # Auger coefficient for holes (cm^6/s)
        self.B = 1.1e-15   # radiative recombination coefficient (cm^3/s)
        
    def time_srh_recombination(self):
        """Benchmark SRH recombination calculation."""
        return srh_recombination(self.n, self.p, self.ni, self.tau_n, self.tau_p)
    
    def time_auger_recombination(self):
        """Benchmark Auger recombination calculation."""
        return auger_recombination(self.n, self.p, self.ni, self.Cn, self.Cp)
    
    def time_radiative_recombination(self):
        """Benchmark radiative recombination calculation."""
        return radiative_recombination(self.n, self.p, self.ni, self.B)


class NumericalUtilsBenchmarks:
    """Benchmark numerical utility functions."""
    
    def setup(self):
        """Set up benchmark parameters."""
        self.x_small = np.linspace(-1e-2, 1e-2, 1000)  # Small values for expm1
        self.x_large = np.linspace(-10, 10, 1000)      # Large values
        
    def time_safe_expm1_small(self):
        """Benchmark safe_expm1 with small values."""
        return safe_expm1(self.x_small)
    
    def time_safe_expm1_large(self):
        """Benchmark safe_expm1 with large values."""
        return safe_expm1(self.x_large)
    
    def time_numpy_expm1_comparison(self):
        """Benchmark numpy.expm1 for comparison."""
        return np.expm1(self.x_small)