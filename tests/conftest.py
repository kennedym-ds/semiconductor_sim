import os

# Force a non-interactive backend to ensure no GUI is required during tests
os.environ.setdefault("MPLBACKEND", "Agg")

try:
    import matplotlib

    matplotlib.use("Agg", force=True)
except Exception:
    # If matplotlib is not installed for some reason, ignore; tests should not rely on it
    pass