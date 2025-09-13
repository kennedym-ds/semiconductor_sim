# semiconductor_sim/schemas/__init__.py

"""Parameter validation schemas and material presets for semiconductor devices.

This module provides pydantic-based parameter validation schemas for device configurations
and material presets for common semiconductors. It's an optional module that requires
pydantic to be installed.

Example:
    >>> # Install with schemas support
    >>> pip install semiconductor-sim[schemas]
    >>> 
    >>> # Use schemas for validation
    >>> from semiconductor_sim.schemas import PNJunctionSchema
    >>> schema = PNJunctionSchema(doping_p=1e16, doping_n=1e17)
    >>> 
    >>> # Use material presets
    >>> from semiconductor_sim import PNJunctionDiode
    >>> diode = PNJunctionDiode.from_preset(material="Si", doping_p=1e16, doping_n=1e17)
"""

try:
    import pydantic
    _PYDANTIC_AVAILABLE = True
except ImportError:
    _PYDANTIC_AVAILABLE = False


def _check_pydantic():
    """Check if pydantic is available and raise helpful error if not."""
    if not _PYDANTIC_AVAILABLE:
        raise ImportError(
            "pydantic is required for parameter schemas. "
            "Install it with: pip install semiconductor-sim[schemas]"
        )


if _PYDANTIC_AVAILABLE:
    from .device_schemas import *
    from .material_presets import *
    
    __all__ = [
        # Device schemas
        'DeviceConfigSchema',
        'PNJunctionSchema', 
        'LEDSchema',
        'SolarCellSchema',
        'ZenerDiodeSchema',
        'TunnelDiodeSchema', 
        'VaractorDiodeSchema',
        'MOSCapacitorSchema',
        # Material presets
        'MaterialPresets',
        'get_material_properties',
        'list_available_materials',
    ]
else:
    __all__ = []