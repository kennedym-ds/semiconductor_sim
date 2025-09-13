from __future__ import annotations

"""
Lightweight plotting helpers to ensure headless-safe behavior and consistent styles.
"""

from typing import Optional

try:
    import matplotlib
    _MATPLOTLIB_AVAILABLE = True
except ImportError:
    _MATPLOTLIB_AVAILABLE = False


def use_headless_backend(preferred: str = "Agg") -> None:
    """
    Switch Matplotlib backend to a non-interactive one if possible.

    Parameters:
    - preferred: Backend name to use when switching (default: 'Agg').
    """
    if not _MATPLOTLIB_AVAILABLE:
        return
    
    try:
        matplotlib.use(preferred, force=True)
    except Exception:
        # Best effort; ignore if backend can't be switched.
        pass


def apply_basic_style() -> None:
    """Apply a minimal style to keep plots consistent across devices."""
    if not _MATPLOTLIB_AVAILABLE:
        return
        
    try:
        import matplotlib.pyplot as plt

        plt.rcParams.update({
            "axes.grid": True,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "figure.figsize": (8, 6),
        })
    except Exception:
        pass
