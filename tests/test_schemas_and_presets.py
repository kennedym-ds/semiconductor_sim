# tests/test_schemas_and_presets.py

"""Tests for parameter schemas and material presets."""

import pytest
from semiconductor_sim.schemas.material_presets import (
    get_material_properties, 
    list_available_materials,
    MaterialPresets
)

# Test if pydantic is available
try:
    import pydantic
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False


class TestMaterialPresets:
    """Test material property presets."""
    
    def test_list_available_materials(self):
        """Test listing available materials."""
        materials = list_available_materials()
        assert isinstance(materials, list)
        assert len(materials) > 0
        assert "SI" in materials
        assert "GAAS" in materials
    
    def test_get_material_properties_silicon(self):
        """Test getting silicon properties."""
        si_props = get_material_properties("Si")
        assert si_props.name == "Silicon"
        assert si_props.bandgap == 1.12
        assert si_props.ni_300k == 1.0e10
        assert si_props.epsilon_r == 11.7
    
    def test_get_material_properties_case_insensitive(self):
        """Test that material lookup is case-insensitive."""
        si_props1 = get_material_properties("Si")
        si_props2 = get_material_properties("SI")
        si_props3 = get_material_properties("si")
        
        assert si_props1.name == si_props2.name == si_props3.name
    
    def test_get_material_properties_unknown_material(self):
        """Test error handling for unknown materials."""
        with pytest.raises(ValueError, match="Material 'Unknown' not found"):
            get_material_properties("Unknown")
    
    def test_intrinsic_carrier_concentration_temperature_dependence(self):
        """Test temperature dependence of ni."""
        si_props = get_material_properties("Si")
        
        ni_300 = si_props.ni(300)
        ni_350 = si_props.ni(350)
        
        assert ni_300 == si_props.ni_300k
        assert ni_350 > ni_300  # Should increase with temperature
    
    def test_material_properties_consistency(self):
        """Test that diffusion lengths are consistent with D and tau."""
        materials = list_available_materials()
        
        for material in materials:
            props = get_material_properties(material)
            
            # Check Einstein relation consistency (within tolerance)
            expected_L_n = (props.D_n * props.tau_n) ** 0.5
            expected_L_p = (props.D_p * props.tau_p) ** 0.5
            
            # Allow 10% tolerance
            assert abs(props.L_n / expected_L_n - 1) < 0.1, f"L_n inconsistent for {material}"
            assert abs(props.L_p / expected_L_p - 1) < 0.1, f"L_p inconsistent for {material}"


@pytest.mark.skipif(not PYDANTIC_AVAILABLE, reason="pydantic not available")
class TestSchemas:
    """Test pydantic validation schemas."""
    
    def test_import_schemas(self):
        """Test that schemas can be imported when pydantic is available."""
        from semiconductor_sim.schemas import PNJunctionSchema, LEDSchema
        assert PNJunctionSchema is not None
        assert LEDSchema is not None
    
    def test_pn_junction_schema_valid_parameters(self):
        """Test PN junction schema with valid parameters."""
        from semiconductor_sim.schemas import PNJunctionSchema
        
        schema = PNJunctionSchema(
            doping_p=1e16,
            doping_n=1e17,
            area=1e-4,
            temperature=300
        )
        
        assert schema.doping_p == 1e16
        assert schema.doping_n == 1e17
        assert schema.area == 1e-4
        assert schema.temperature == 300
    
    def test_pn_junction_schema_validation_errors(self):
        """Test PN junction schema validation errors."""
        from semiconductor_sim.schemas import PNJunctionSchema
        
        # Test low doping
        with pytest.raises(ValueError, match="very low"):
            PNJunctionSchema(doping_p=1e10, doping_n=1e17)
        
        # Test high temperature
        with pytest.raises(ValueError, match="very high"):
            PNJunctionSchema(doping_p=1e16, doping_n=1e17, temperature=600)
        
        # Test large area (pydantic constraint validation)
        with pytest.raises(ValueError):
            PNJunctionSchema(doping_p=1e16, doping_n=1e17, area=2.0)
    
    def test_led_schema_valid_parameters(self):
        """Test LED schema with valid parameters."""
        from semiconductor_sim.schemas import LEDSchema
        
        schema = LEDSchema(
            doping_p=1e17,
            doping_n=1e18,
            efficiency=0.8,
            B=1e-10
        )
        
        assert schema.efficiency == 0.8
        assert schema.B == 1e-10
    
    def test_led_schema_efficiency_validation(self):
        """Test LED efficiency validation."""
        from semiconductor_sim.schemas import LEDSchema
        
        # Test efficiency > 1
        with pytest.raises(ValueError):
            LEDSchema(doping_p=1e17, doping_n=1e18, efficiency=1.5)
        
        # Test efficiency < 0
        with pytest.raises(ValueError):
            LEDSchema(doping_p=1e17, doping_n=1e18, efficiency=-0.1)
    
    def test_tunnel_diode_schema_high_doping_requirement(self):
        """Test tunnel diode requires high doping."""
        from semiconductor_sim.schemas import TunnelDiodeSchema
        
        # Test low doping (should fail)
        with pytest.raises(ValueError, match="too low for tunnel diode"):
            TunnelDiodeSchema(doping_p=1e16, doping_n=1e17)
        
        # Test high doping (should pass)
        schema = TunnelDiodeSchema(doping_p=1e19, doping_n=1e19)
        assert schema.doping_p == 1e19


class TestFromPreset:
    """Test from_preset class methods."""
    
    def test_pn_junction_from_preset_basic(self):
        """Test basic PN junction from_preset functionality."""
        from semiconductor_sim import PNJunctionDiode
        
        diode = PNJunctionDiode.from_preset("Si", doping_p=1e16, doping_n=1e17)
        
        assert diode.doping_p == 1e16
        assert diode.doping_n == 1e17
        assert diode.D_n == 35.0  # Silicon D_n
    
    def test_pn_junction_from_preset_override_parameters(self):
        """Test overriding material parameters."""
        from semiconductor_sim import PNJunctionDiode
        
        diode = PNJunctionDiode.from_preset(
            "Si", 
            doping_p=1e16, 
            doping_n=1e17,
            D_n=50.0  # Override default
        )
        
        assert diode.D_n == 50.0  # Should use override
    
    def test_led_from_preset_basic(self):
        """Test basic LED from_preset functionality."""
        from semiconductor_sim import LED
        
        led = LED.from_preset("GaAs", doping_p=1e17, doping_n=1e18, efficiency=0.8)
        
        assert led.doping_p == 1e17
        assert led.efficiency == 0.8
        assert led.B == 2e-10  # GaAs B coefficient
    
    def test_from_preset_unknown_material(self):
        """Test from_preset with unknown material."""
        from semiconductor_sim import PNJunctionDiode
        
        with pytest.raises(ValueError, match="Material 'Unknown' not found"):
            PNJunctionDiode.from_preset("Unknown", doping_p=1e16, doping_n=1e17)
    
    @pytest.mark.skipif(not PYDANTIC_AVAILABLE, reason="pydantic not available")
    def test_from_preset_with_validation(self):
        """Test from_preset with pydantic validation."""
        from semiconductor_sim import PNJunctionDiode
        
        # Valid parameters should work
        diode = PNJunctionDiode.from_preset("Si", doping_p=1e16, doping_n=1e17)
        assert diode is not None
        
        # Invalid parameters should raise validation error
        with pytest.raises(ValueError):
            PNJunctionDiode.from_preset("Si", doping_p=1e10, doping_n=1e17)  # Too low doping


class TestSchemasWithoutPydantic:
    """Test behavior when pydantic is not available."""
    
    @pytest.mark.skipif(PYDANTIC_AVAILABLE, reason="pydantic is available")
    def test_schemas_import_without_pydantic(self):
        """Test that schemas module handles missing pydantic gracefully."""
        # This test would only run if pydantic is not available
        with pytest.raises(ImportError, match="pydantic is required"):
            from semiconductor_sim.schemas import PNJunctionSchema
    
    def test_from_preset_without_pydantic_works(self):
        """Test that from_preset works without pydantic (no validation)."""
        from semiconductor_sim import PNJunctionDiode
        
        # Should work even with invalid parameters when no validation
        diode = PNJunctionDiode.from_preset("Si", doping_p=1e16, doping_n=1e17)
        assert diode is not None