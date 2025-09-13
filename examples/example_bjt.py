# examples/example_bjt.py

import numpy as np
from semiconductor_sim import BJT


def main() -> None:
    """Demonstrate BJT device characteristics with Ebers-Moll model."""
    
    # Create NPN and PNP BJTs with typical silicon parameters
    npn_bjt = BJT(
        doping_emitter=1e18,  # Heavily doped emitter
        doping_base=1e16,     # Lightly doped base
        doping_collector=1e17, # Moderately doped collector
        bjt_type="NPN",
        beta_f=100.0,         # Forward current gain
        beta_r=1.0,           # Reverse current gain
        temperature=300,      # Room temperature
        area=1e-6             # 1 µm² active area
    )
    
    pnp_bjt = BJT(
        doping_emitter=1e18,
        doping_base=1e16,
        doping_collector=1e17,
        bjt_type="PNP",
        beta_f=100.0,
        beta_r=1.0,
        temperature=300,
        area=1e-6
    )
    
    print("=== BJT Device Characteristics ===")
    print(f"NPN BJT: {npn_bjt}")
    print(f"PNP BJT: {pnp_bjt}")
    print(f"NPN Saturation Current: {npn_bjt.I_s:.2e} A")
    print(f"PNP Saturation Current: {pnp_bjt.I_s:.2e} A")
    print()
    
    # Example 1: Forward active region (V_BE > 0, V_BC = 0)
    print("=== Example 1: Forward Active Region ===")
    v_be_forward = np.array([0.5, 0.6, 0.7, 0.8])
    v_bc = 0.0  # Base-collector at zero bias
    
    i_c_npn, i_b_npn, _ = npn_bjt.iv_characteristic(v_be_forward, v_bc)
    i_c_pnp, i_b_pnp, _ = pnp_bjt.iv_characteristic(-v_be_forward, v_bc)  # PNP needs negative V_BE
    
    print("NPN Forward Active (V_BC = 0 V):")
    for i, v_be in enumerate(v_be_forward):
        beta_npn = i_c_npn[i] / i_b_npn[i] if i_b_npn[i] != 0 else 0
        print(f"  V_BE = {v_be:.1f} V: I_C = {i_c_npn[i]:.2e} A, I_B = {i_b_npn[i]:.2e} A, β = {beta_npn:.1f}")
    
    print("\nPNP Forward Active (V_EB = +V_BE, V_BC = 0 V):")
    for i, v_be in enumerate(v_be_forward):
        beta_pnp = i_c_pnp[i] / i_b_pnp[i] if i_b_pnp[i] != 0 else 0
        print(f"  V_EB = {v_be:.1f} V: I_C = {i_c_pnp[i]:.2e} A, I_B = {i_b_pnp[i]:.2e} A, β = {beta_pnp:.1f}")
    print()
    
    # Example 2: Different V_BC values (saturation effects)
    print("=== Example 2: Saturation Effects ===")
    v_be = 0.7  # Fixed forward bias
    v_bc_array = np.array([0.0, 0.2, 0.4, 0.6])  # Increasing V_BC
    
    print(f"NPN BJT at V_BE = {v_be} V, varying V_BC:")
    for v_bc in v_bc_array:
        i_c, i_b, _ = npn_bjt.iv_characteristic(np.array([v_be]), v_bc)
        beta = i_c[0] / i_b[0] if i_b[0] != 0 else 0
        print(f"  V_BC = {v_bc:.1f} V: I_C = {i_c[0]:.2e} A, I_B = {i_b[0]:.2e} A, β = {beta:.1f}")
    print()
    
    # Example 3: Temperature effects
    print("=== Example 3: Temperature Effects ===")
    temperatures = [250, 300, 350, 400]  # K
    v_be = 0.7
    v_bc = 0.0
    
    print(f"NPN BJT at V_BE = {v_be} V, V_BC = {v_bc} V:")
    for temp in temperatures:
        bjt_temp = BJT(
            doping_emitter=1e18,
            doping_base=1e16,
            doping_collector=1e17,
            bjt_type="NPN",
            temperature=temp,
            area=1e-6
        )
        i_c, i_b, _ = bjt_temp.iv_characteristic(np.array([v_be]), v_bc)
        print(f"  T = {temp} K: I_S = {bjt_temp.I_s:.2e} A, I_C = {i_c[0]:.2e} A, I_B = {i_b[0]:.2e} A")
    print()
    
    # Example 4: Plotting IV characteristics
    print("=== Example 4: Generating IV Curves ===")
    v_be_range = np.linspace(0.0, 0.9, 100)
    
    # Forward active region (V_BC = 0)
    i_c_fa, i_b_fa, recomb_fa = npn_bjt.iv_characteristic(v_be_range, v_bc=0.0)
    
    # With SRH recombination
    n_conc = np.full_like(v_be_range, 1e16)  # cm^-3
    p_conc = np.full_like(v_be_range, 1e16)  # cm^-3
    i_c_srh, i_b_srh, recomb_srh = npn_bjt.iv_characteristic(v_be_range, v_bc=0.0, 
                                                              n_conc=n_conc, p_conc=p_conc)
    
    print(f"Generated IV curves with {len(v_be_range)} points")
    print(f"V_BE range: {v_be_range[0]:.1f} to {v_be_range[-1]:.1f} V")
    print(f"Max I_C: {np.max(i_c_fa):.2e} A")
    print(f"Max I_B: {np.max(i_b_fa):.2e} A")
    print(f"Max recombination rate: {np.max(recomb_srh):.2e} cm^-3 s^-1")
    
    # Plot the characteristics
    npn_bjt.plot_iv_characteristic(v_be_range, i_c_fa, i_b_fa, v_bc=0.0, recombination=recomb_srh)
    
    # Plot Gummel plot
    npn_bjt.plot_gummel_plot(v_be_range, i_c_fa, i_b_fa)
    
    print("\nPlots generated successfully (headless mode)")
    print("=== BJT Demonstration Complete ===")


if __name__ == "__main__":
    main()