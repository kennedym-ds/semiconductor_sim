import os
import numpy as np
from hypothesis import settings, Verbosity

# Force a non-interactive backend to ensure no GUI is required during tests
os.environ.setdefault("MPLBACKEND", "Agg")

try:
    import matplotlib

    matplotlib.use("Agg", force=True)
except Exception:
    # If matplotlib is not installed for some reason, ignore; tests should not rely on it
    pass

# Centralize RNG seeds for deterministic testing and CI reproducibility
np.random.seed(42)

# Configure Hypothesis for deterministic testing
settings.register_profile("ci", max_examples=50, verbosity=Verbosity.verbose, derandomize=True)
settings.register_profile("dev", max_examples=10)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))