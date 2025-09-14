"""Plot material effects for LED and SolarCell (Si vs GaAs)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from semiconductor_sim import LED, SolarCell
from semiconductor_sim.materials import get_material
from semiconductor_sim.utils.plotting import apply_basic_style, use_headless_backend


def plot_led(si_label: str, gaas_label: str) -> None:
    si = get_material("Si")
    gaas = get_material("GaAs")
    led_si = LED(1e17, 1e17, efficiency=0.2, material=si)
    led_gaas = LED(1e17, 1e17, efficiency=0.2, material=gaas)

    v = np.linspace(0.0, 1.5, 200)
    I_si, E_si = led_si.iv_characteristic(v)
    I_gaas, E_gaas = led_gaas.iv_characteristic(v)

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.set_title("LED: IV and Emission vs Material")
    ax1.set_xlabel("Voltage (V)")
    ax1.set_ylabel("Current (A)")
    ax1.plot(v, I_si, label=f"I ({si_label})", color="tab:blue")
    ax1.plot(v, I_gaas, label=f"I ({gaas_label})", color="tab:blue", linestyle="--")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Emission (arb)")
    ax2.plot(v, E_si, label=f"E ({si_label})", color="tab:red")
    ax2.plot(v, E_gaas, label=f"E ({gaas_label})", color="tab:red", linestyle="--")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    fig.tight_layout()


def plot_solar(si_label: str, gaas_label: str) -> None:
    si = get_material("Si")
    gaas = get_material("GaAs")
    sc_si = SolarCell(1e17, 1e17, light_intensity=1.0, material=si)
    sc_gaas = SolarCell(1e17, 1e17, light_intensity=1.0, material=gaas)

    v = np.linspace(0.0, 0.9, 200)
    (I_si,) = sc_si.iv_characteristic(v)
    (I_gaas,) = sc_gaas.iv_characteristic(v)

    plt.figure(figsize=(8, 5))
    plt.title("Solar Cell: IV vs Material")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(v, I_si, label=f"{si_label}")
    plt.plot(v, I_gaas, label=f"{gaas_label}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()


def main() -> None:
    use_headless_backend("Agg")
    apply_basic_style()
    plot_led("Si", "GaAs")
    plot_solar("Si", "GaAs")
    plt.show()


if __name__ == "__main__":
    main()
