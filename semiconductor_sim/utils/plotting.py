from __future__ import annotations

"""Lightweight plotting helpers for headless-safe, consistent Matplotlib usage."""

from contextlib import suppress

import matplotlib


def use_headless_backend(preferred: str = "Agg") -> None:
    """
    Switch Matplotlib backend to a non-interactive one if possible.

    Parameters:
    - preferred: Backend name to use when switching (default: 'Agg').
    """
    with suppress(Exception):
        matplotlib.use(preferred, force=True)


def apply_basic_style() -> None:
    """Apply a minimal style to keep plots consistent across devices."""
    with suppress(Exception):
        import matplotlib.pyplot as plt

        plt.rcParams.update(
            {
                "axes.grid": True,
                "axes.titlesize": 12,
                "axes.labelsize": 10,
                "legend.fontsize": 9,
                "figure.figsize": (8, 6),
            }
        )
