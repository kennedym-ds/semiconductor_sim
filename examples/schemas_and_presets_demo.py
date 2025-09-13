#!/usr/bin/env python3
"""
Example demonstrating the new parameter schemas and material presets functionality.

This example shows how to:
1. Use material presets to create devices with semiconductor properties
2. Validate device parameters using pydantic schemas
3. Handle validation errors with clear messages
4. List available materials and their properties
"""

from semiconductor_sim import PNJunctionDiode, LED, SolarCell
from semiconductor_sim.schemas.material_presets import (
    list_available_materials, 
    get_material_properties
)

def demonstrate_material_presets():
    """Demonstrate material preset functionality."""
    print("=== Material Presets Demonstration ===")
    
    # List available materials
    materials = list_available_materials()
    print(f"Available materials: {', '.join(materials)}")
    print()
    
    # Show properties for different materials
    for material in ["SI", "GAAS", "GE"]:
        props = get_material_properties(material)
        print(f"{props.name} ({material}) properties:")
        print(f"  Bandgap: {props.bandgap} eV")
        print(f"  ni(300K): {props.ni_300k:.2e} cm^-3")
        print(f"  ni(350K): {props.ni(350):.2e} cm^-3")
        print(f"  Electron mobility: {props.mu_n} cm^2/V/s")
        print(f"  Hole mobility: {props.mu_p} cm^2/V/s")
        print()


def demonstrate_device_presets():
    """Demonstrate creating devices with material presets."""
    print("=== Device Creation with Presets ===")
    
    # Create a silicon PN junction diode
    print("Creating Silicon PN Junction Diode...")
    si_diode = PNJunctionDiode.from_preset(
        material="Si",
        doping_p=1e16,
        doping_n=1e17,
        area=1e-4
    )
    print(f"Silicon diode: D_n={si_diode.D_n} cm^2/s, L_n={si_diode.L_n:.2e} cm")
    
    # Create a GaAs LED
    print("\nCreating GaAs LED...")
    gaas_led = LED.from_preset(
        material="GaAs",
        doping_p=1e17,
        doping_n=1e18,
        efficiency=0.8
    )
    print(f"GaAs LED: B={gaas_led.B:.2e} cm^3/s, efficiency={gaas_led.efficiency}")
    
    # Create a solar cell with custom parameters
    print("\nCreating Solar Cell with overridden parameters...")
    solar_cell = SolarCell.from_preset(
        material="Si",
        doping_p=1e16,
        doping_n=1e17,
        light_intensity=2.0
    )
    print(f"Solar cell: I_sc={solar_cell.I_sc:.2e} A, V_oc={solar_cell.V_oc:.3f} V")


def demonstrate_validation():
    """Demonstrate parameter validation."""
    print("=== Parameter Validation Demonstration ===")
    
    try:
        from semiconductor_sim.schemas import PNJunctionSchema, LEDSchema
        
        print("Testing valid parameters...")
        # Valid parameters
        valid_schema = PNJunctionSchema(
            doping_p=1e16,
            doping_n=1e17,
            temperature=300,
            area=1e-4
        )
        print(f"✓ Valid schema created with doping_p={valid_schema.doping_p:.1e}")
        
        print("\nTesting validation errors...")
        
        # Test 1: Very low doping
        try:
            PNJunctionSchema(doping_p=1e10, doping_n=1e17)
        except ValueError as e:
            print(f"✓ Caught low doping error: {str(e).split('.')[0]}...")
        
        # Test 2: High temperature
        try:
            PNJunctionSchema(doping_p=1e16, doping_n=1e17, temperature=600)
        except ValueError as e:
            print(f"✓ Caught high temperature error: {str(e).split('.')[0]}...")
        
        # Test 3: LED efficiency validation
        try:
            LEDSchema(doping_p=1e17, doping_n=1e18, efficiency=1.5)
        except ValueError as e:
            print(f"✓ Caught efficiency error: {str(e).split('.')[0]}...")
    
    except ImportError:
        print("⚠ Pydantic not available - validation skipped")
        print("Install with: pip install semiconductor-sim[schemas]")


def demonstrate_error_handling():
    """Demonstrate error handling for unknown materials."""
    print("=== Error Handling Demonstration ===")
    
    try:
        # Try to use an unknown material
        unknown_diode = PNJunctionDiode.from_preset(
            material="NonExistent",
            doping_p=1e16,
            doping_n=1e17
        )
    except ValueError as e:
        print(f"✓ Caught unknown material error: {e}")
    
    try:
        # Try to use from_preset with validation error
        bad_diode = PNJunctionDiode.from_preset(
            material="Si",
            doping_p=1e10,  # Too low
            doping_n=1e17
        )
    except ValueError as e:
        print(f"✓ Caught validation error in from_preset: {str(e).split(':')[0]}...")


def main():
    """Run all demonstrations."""
    print("Semiconductor Simulation: Parameter Schemas and Material Presets Example")
    print("=" * 75)
    print()
    
    demonstrate_material_presets()
    demonstrate_device_presets()
    demonstrate_validation()
    demonstrate_error_handling()
    
    print("\n" + "=" * 75)
    print("Example completed successfully!")
    print("\nKey features demonstrated:")
    print("• Material property database with temperature-dependent calculations")
    print("• Easy device creation using material presets") 
    print("• Parameter validation with clear error messages")
    print("• Graceful error handling for invalid inputs")


if __name__ == "__main__":
    main()