import matplotlib.pyplot as plt
import numpy as np

from semiconductor_sim import SchottkyDiode
from semiconductor_sim.utils.plotting import apply_basic_style, use_headless_backend


def main() -> None:
    use_headless_backend("Agg")
    apply_basic_style()

    d = SchottkyDiode(barrier_height_eV=0.7, ideality=1.1)
    V = np.linspace(-0.2, 0.5, 200)
    (I,) = d.iv_characteristic(V)

    plt.figure(figsize=(6, 4))
    plt.title("Schottky diode IV")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(V, I)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
