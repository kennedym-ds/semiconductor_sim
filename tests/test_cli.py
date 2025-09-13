"""Tests for the CLI functionality."""

import pytest
import tempfile
import json
import yaml
from pathlib import Path
from semiconductor_sim.cli.main import main
from semiconductor_sim.cli.utils import load_config, create_device, create_voltage_range


class TestCLIUtils:
    """Test CLI utility functions."""
    
    def test_load_config_json(self):
        """Test loading JSON config."""
        config_data = {
            "doping_p": 1e17,
            "doping_n": 1e17,
            "temperature": 300,
            "area": 1e-4
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            loaded_config = load_config(config_path)
            assert loaded_config == config_data
        finally:
            Path(config_path).unlink()
    
    def test_load_config_yaml(self):
        """Test loading YAML config."""
        config_data = {
            "doping_p": 1e17,
            "oxide_thickness": 1e-6,
            "temperature": 300,
            "area": 1e-4
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            loaded_config = load_config(config_path)
            assert loaded_config == config_data
        finally:
            Path(config_path).unlink()
    
    def test_create_device_pn_junction(self):
        """Test creating a PN junction device."""
        params = {
            "doping_p": 1e17,
            "doping_n": 1e17,
            "temperature": 300,
            "area": 1e-4
        }
        
        device = create_device("pn_junction", params)
        assert device.__class__.__name__ == "PNJunctionDiode"
        assert device.temperature == 300
        assert device.area == 1e-4
    
    def test_create_device_mos_capacitor(self):
        """Test creating a MOS capacitor device."""
        params = {
            "doping_p": 1e17,
            "oxide_thickness": 1e-6,
            "temperature": 300,
            "area": 1e-4
        }
        
        device = create_device("mos_capacitor", params)
        assert device.__class__.__name__ == "MOSCapacitor"
        assert device.temperature == 300
        assert device.area == 1e-4
    
    def test_create_voltage_range(self):
        """Test voltage range creation."""
        voltage = create_voltage_range(-1.0, 1.0, 101)
        assert len(voltage) == 101
        assert voltage[0] == -1.0
        assert voltage[-1] == 1.0


class TestCLICommands:
    """Test CLI command functionality."""
    
    def test_cli_help(self):
        """Test CLI help command."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])
        assert exc_info.value.code == 0
    
    def test_iv_command_basic(self):
        """Test basic IV command functionality."""
        config_data = {
            "doping_p": 1e17,
            "doping_n": 1e17,
            "temperature": 300,
            "area": 1e-4
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create config file
            config_path = Path(temp_dir) / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config_data, f)
            
            # Create output paths
            csv_path = Path(temp_dir) / "output.csv"
            png_path = Path(temp_dir) / "output.png"
            
            # Run IV command
            args = [
                "iv", "pn_junction",
                "--config", str(config_path),
                "--voltage-start", "-0.5",
                "--voltage-stop", "0.5",
                "--voltage-points", "10",
                "--output-csv", str(csv_path),
                "--output-png", str(png_path)
            ]
            
            result = main(args)
            assert result == 0
            assert csv_path.exists()
            assert png_path.exists()
            
            # Check CSV content
            with open(csv_path, 'r') as f:
                lines = f.readlines()
                assert len(lines) > 1  # Header + data
                assert "Voltage (V)" in lines[0]
                assert "Current (A)" in lines[0]
    
    def test_cv_command_basic(self):
        """Test basic CV command functionality."""
        config_data = {
            "doping_p": 1e17,
            "oxide_thickness": 1e-6,
            "temperature": 300,
            "area": 1e-4
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create config file
            config_path = Path(temp_dir) / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config_data, f)
            
            # Create output paths
            csv_path = Path(temp_dir) / "output.csv"
            png_path = Path(temp_dir) / "output.png"
            
            # Run CV command
            args = [
                "cv", "mos_capacitor",
                "--config", str(config_path),
                "--voltage-start", "-1.0",
                "--voltage-stop", "1.0",
                "--voltage-points", "10",
                "--output-csv", str(csv_path),
                "--output-png", str(png_path)
            ]
            
            result = main(args)
            assert result == 0
            assert csv_path.exists()
            assert png_path.exists()
            
            # Check CSV content
            with open(csv_path, 'r') as f:
                lines = f.readlines()
                assert len(lines) > 1  # Header + data
                assert "Voltage (V)" in lines[0]
                assert "Current (A)" in lines[0]
                assert "Capacitance (F)" in lines[0]


if __name__ == "__main__":
    pytest.main([__file__])