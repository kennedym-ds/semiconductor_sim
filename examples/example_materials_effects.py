"""Compare material effects on LED and SolarCell behavior."""

import numpy as np

from semiconductor_sim import LED, SolarCell
from semiconductor_sim.materials import get_material


def main() -> None:
    si = get_material("Si")
    gaas = get_material("GaAs")

    # LED comparison
    led_si = LED(1e17, 1e17, efficiency=0.2, material=si)
    led_gaas = LED(1e17, 1e17, efficiency=0.2, material=gaas)
    v_led = np.linspace(0.0, 1.2, 7)
    I_si, E_si = led_si.iv_characteristic(v_led)
    I_gaas, E_gaas = led_gaas.iv_characteristic(v_led)

    print("LED saturation current (Si):   ", led_si.I_s)
    print("LED saturation current (GaAs):", led_gaas.I_s)
    print("LED emission at 1.0 V (Si, GaAs):", E_si[-2], E_gaas[-2])

    # Solar cell comparison
    sc_si = SolarCell(1e17, 1e17, light_intensity=1.0, material=si)
    sc_gaas = SolarCell(1e17, 1e17, light_intensity=1.0, material=gaas)
    v_sc = np.linspace(0.0, 0.9, 7)
    (I_si_sc,) = sc_si.iv_characteristic(v_sc)
    (I_gaas_sc,) = sc_gaas.iv_characteristic(v_sc)

    print("SolarCell I_s (Si):   ", sc_si.I_s)
    print("SolarCell I_s (GaAs): ", sc_gaas.I_s)
    print("SolarCell V_oc (Si, GaAs):", sc_si.V_oc, sc_gaas.V_oc)


if __name__ == "__main__":
    main()
