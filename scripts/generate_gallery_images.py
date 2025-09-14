"""Generate static PNG figures for docs gallery and device pages.

Saves figures under docs/images/*.png. Uses Agg backend for headless runs.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from semiconductor_sim import (
    BJT,
    LED,
    MOSCapacitor,
    Photodiode,
    PINDiode,
    PNJunctionDiode,
    SchottkyDiode,
    SolarCell,
    TunnelDiode,
    VaractorDiode,
    ZenerDiode,
)
from semiconductor_sim.materials import get_material
from semiconductor_sim.utils.plotting import apply_basic_style, use_headless_backend

DOCS_IMG = Path(__file__).resolve().parents[1] / "docs" / "images"
MANIFEST = DOCS_IMG / ".gallery_manifest.txt"
SAVED: list[Path] = []


def ensure_outdir() -> None:
    DOCS_IMG.mkdir(parents=True, exist_ok=True)


def save_current_plot(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    SAVED.append(path)


def pn_materials() -> None:
    si = get_material("Si")
    gaas = get_material("GaAs")
    d_si = PNJunctionDiode(1e17, 1e17, material=si)
    d_gaas = PNJunctionDiode(1e17, 1e17, material=gaas)
    v = np.linspace(0.0, 0.9, 200)
    I_si, _ = d_si.iv_characteristic(v)
    I_gaas, _ = d_gaas.iv_characteristic(v)
    plt.figure(figsize=(6, 4))
    plt.title("PN Junction: materials effect")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(v, I_si, label="Si")
    plt.plot(v, I_gaas, label="GaAs", linestyle="--")
    plt.grid(True)
    plt.legend()
    save_current_plot(DOCS_IMG / "pn_materials.png")


def led_materials() -> None:
    si = get_material("Si")
    gaas = get_material("GaAs")
    led_si = LED(1e17, 1e17, efficiency=0.2, material=si)
    led_gaas = LED(1e17, 1e17, efficiency=0.2, material=gaas)
    v = np.linspace(0.0, 1.5, 200)
    I_si, E_si = led_si.iv_characteristic(v)
    I_gaas, E_gaas = led_gaas.iv_characteristic(v)
    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.set_title("LED: IV & emission")
    ax1.set_xlabel("Voltage (V)")
    ax1.set_ylabel("Current (A)")
    ax1.plot(v, I_si, label="I (Si)")
    ax1.plot(v, I_gaas, label="I (GaAs)", linestyle="--")
    ax1.grid(True)
    ax2 = ax1.twinx()
    ax2.set_ylabel("Emission (arb)")
    ax2.plot(v, E_si, label="E (Si)", color="tab:red")
    ax2.plot(v, E_gaas, label="E (GaAs)", color="tab:red", linestyle="--")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    save_current_plot(DOCS_IMG / "led_materials.png")


def solar_materials() -> None:
    si = get_material("Si")
    gaas = get_material("GaAs")
    sc_si = SolarCell(1e17, 1e17, light_intensity=1.0, material=si)
    sc_gaas = SolarCell(1e17, 1e17, light_intensity=1.0, material=gaas)
    v = np.linspace(0.0, 0.9, 200)
    (I_si,) = sc_si.iv_characteristic(v)
    (I_gaas,) = sc_gaas.iv_characteristic(v)
    plt.figure(figsize=(6, 4))
    plt.title("Solar: IV vs material")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(v, I_si, label="Si")
    plt.plot(v, I_gaas, label="GaAs")
    plt.grid(True)
    plt.legend()
    save_current_plot(DOCS_IMG / "solar_materials.png")


def mos_cv() -> None:
    mos = MOSCapacitor(doping_p=1e17, oxide_thickness=1e-6)
    v = np.linspace(-2, 2, 200)
    c = mos.capacitance(v)
    plt.figure(figsize=(6, 4))
    plt.title("MOS: C–V")
    plt.xlabel("Gate Voltage (V)")
    plt.ylabel("Capacitance (F)")
    plt.plot(v, c)
    plt.grid(True)
    save_current_plot(DOCS_IMG / "mos_cv.png")


def varactor_cv() -> None:
    va = VaractorDiode(1e17, 1e17)
    v = np.linspace(0.0, 2.0, 200)
    Cj = va.capacitance(v)
    plt.figure(figsize=(6, 4))
    plt.title("Varactor: C–V")
    plt.xlabel("Reverse Voltage (V)")
    plt.ylabel("Capacitance (F)")
    plt.plot(v, Cj)
    plt.grid(True)
    save_current_plot(DOCS_IMG / "varactor_cv.png")


def tunnel_iv() -> None:
    td = TunnelDiode(1e19, 1e19)
    v = np.linspace(-0.3, 0.7, 200)
    I, R = td.iv_characteristic(v)
    plt.figure(figsize=(6, 4))
    plt.title("Tunnel: IV")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(v, I)
    plt.grid(True)
    save_current_plot(DOCS_IMG / "tunnel_iv.png")


def zener_iv() -> None:
    ze = ZenerDiode(1e17, 1e17, zener_voltage=5.0)
    v = np.linspace(0.0, 10.0, 200)
    I, _ = ze.iv_characteristic(v)
    plt.figure(figsize=(6, 4))
    plt.title("Zener: IV")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(v, I)
    plt.grid(True)
    save_current_plot(DOCS_IMG / "zener_iv.png")


def pin_iv() -> None:
    pd = PINDiode(1e17, 1e17, intrinsic_width_cm=1e-4)
    v = np.linspace(-0.2, 0.9, 200)
    (I,) = pd.iv_characteristic(v)
    plt.figure(figsize=(6, 4))
    plt.title("PIN: IV")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(v, I)
    plt.grid(True)
    save_current_plot(DOCS_IMG / "pin_iv.png")


def photodiode_iv() -> None:
    pd = Photodiode(1e17, 1e17, irradiance_W_per_cm2=1e-3, responsivity_A_per_W=0.5)
    v = np.linspace(-0.2, 0.8, 200)
    (I,) = pd.iv_characteristic(v)
    plt.figure(figsize=(6, 4))
    plt.title("Photodiode: IV")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(v, I)
    plt.grid(True)
    save_current_plot(DOCS_IMG / "photodiode_iv.png")


def bjt_output() -> None:
    bjt = BJT(
        doping_p=1e16, doping_n=1e18, early_voltage=50.0, vbe_values=[0.6, 0.65, 0.7, 0.75, 0.8]
    )
    vce = np.linspace(0.0, 5.0, 200)
    (ic_grid,) = bjt.iv_characteristic(vce)
    plt.figure(figsize=(6, 4))
    plt.title("BJT: Output characteristics")
    plt.xlabel("V_CE (V)")
    plt.ylabel("I_C (A)")
    for vbe, ic in zip(bjt.vbe_values, ic_grid):
        plt.plot(vce, ic, label=f"V_BE={vbe:.2f} V")
    plt.grid(True)
    plt.legend(loc="upper left", fontsize=8)
    save_current_plot(DOCS_IMG / "bjt_output.png")


def bjt_transfer() -> None:
    bjt = BJT(
        doping_p=1e16, doping_n=1e18, early_voltage=50.0, vbe_values=np.linspace(0.55, 0.80, 11)
    )
    vce_fixed = 2.0
    vbe = bjt.vbe_values
    (ic_grid,) = bjt.iv_characteristic(np.array([vce_fixed]))
    ic = ic_grid[:, 0]
    plt.figure(figsize=(6, 4))
    plt.title(f"BJT: Transfer (V_CE={vce_fixed:.1f} V)")
    plt.xlabel("V_BE (V)")
    plt.ylabel("I_C (A)")
    plt.semilogy(vbe, ic, marker="o")
    plt.grid(True, which="both")
    save_current_plot(DOCS_IMG / "bjt_transfer.png")


def schottky_iv() -> None:
    sd = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1)
    v = np.linspace(-0.2, 0.5, 200)
    (I,) = sd.iv_characteristic(v)
    plt.figure(figsize=(6, 4))
    plt.title("Schottky: IV")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(v, I)
    plt.grid(True)
    save_current_plot(DOCS_IMG / "schottky_iv.png")


def schottky_rs_compare() -> None:
    sd0 = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1)
    sd2 = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1, series_resistance_ohm=2.0)
    sd5 = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1, series_resistance_ohm=5.0)
    v = np.linspace(-0.2, 0.5, 200)
    (i0,) = sd0.iv_characteristic(v)
    (i2,) = sd2.iv_characteristic(v)
    (i5,) = sd5.iv_characteristic(v)
    plt.figure(figsize=(6, 4))
    plt.title("Schottky: IV with series resistance")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(v, i0, label="R_s = 0 Ω")
    plt.plot(v, i2, label="R_s = 2 Ω", linestyle="--")
    plt.plot(v, i5, label="R_s = 5 Ω", linestyle=":")
    plt.grid(True)
    plt.legend()
    save_current_plot(DOCS_IMG / "schottky_rs_compare.png")


def main() -> None:
    use_headless_backend("Agg")
    apply_basic_style()
    ensure_outdir()
    pn_materials()
    led_materials()
    solar_materials()
    mos_cv()
    varactor_cv()
    tunnel_iv()
    zener_iv()
    pin_iv()
    photodiode_iv()
    schottky_iv()
    schottky_rs_compare()
    bjt_output()
    bjt_transfer()
    try:
        with MANIFEST.open("w", encoding="utf-8") as fh:
            for p in SAVED:
                fh.write(f"{p.name}\n")
    except Exception:
        pass


if __name__ == "__main__":
    main()
