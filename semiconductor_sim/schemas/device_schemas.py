# semiconductor_sim/schemas/device_schemas.py

"""Pydantic schemas for device parameter validation."""

from typing import Optional, Union

try:
    from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
    _PYDANTIC_AVAILABLE = True
except ImportError:
    _PYDANTIC_AVAILABLE = False
    # Create dummy classes if pydantic not available
    BaseModel = object
    Field = None
    field_validator = None
    model_validator = None
    ConfigDict = None

if not _PYDANTIC_AVAILABLE:
    raise ImportError(
        "pydantic is required for parameter schemas. "
        "Install it with: pip install semiconductor-sim[schemas]"
    )

from ..utils import DEFAULT_T


class DeviceConfigSchema(BaseModel):
    """Base schema for all semiconductor devices."""
    
    area: float = Field(
        default=1e-4,
        gt=0,
        le=1.0,
        description="Cross-sectional area of the device (cm^2)"
    )
    
    temperature: float = Field(
        default=DEFAULT_T,
        gt=0,
        le=1000,
        description="Operating temperature (K)"
    )
    
    @field_validator('area')
    def validate_area(cls, v):
        if v > 1.0:
            raise ValueError(
                f"Area {v} cm^2 is unusually large. Typical values are between 1e-6 and 1e-2 cm^2. "
                "Please verify this is correct."
            )
        return v
    
    @field_validator('temperature')
    def validate_temperature(cls, v):
        if v < 200:
            raise ValueError(
                f"Temperature {v} K is very low. Typical range is 250-400 K for normal operation."
            )
        if v > 500:
            raise ValueError(
                f"Temperature {v} K is very high. Most semiconductors degrade above 450 K."
            )
        return v

    model_config = ConfigDict(validate_assignment=True, extra="forbid")


class DopingMixin(BaseModel):
    """Mixin for devices with doping parameters."""
    
    doping_p: float = Field(
        gt=0,
        description="Acceptor concentration in p-region (cm^-3)"
    )
    
    doping_n: float = Field(
        gt=0,
        description="Donor concentration in n-region (cm^-3)"
    )
    
    @field_validator('doping_p', 'doping_n')
    def validate_doping(cls, v, info):
        field_name = info.field_name
        if v < 1e12:
            raise ValueError(
                f"{field_name} = {v:.2e} cm^-3 is very low. "
                "Typical doping levels are between 1e14 and 1e19 cm^-3."
            )
        if v > 1e21:
            raise ValueError(
                f"{field_name} = {v:.2e} cm^-3 is extremely high. "
                "Doping above 1e20 cm^-3 may cause degeneracy effects."
            )
        return v


class TransportMixin(BaseModel):
    """Mixin for transport parameters."""
    
    tau_n: float = Field(
        default=1e-6,
        gt=0,
        description="Electron lifetime (s)"
    )
    
    tau_p: float = Field(
        default=1e-6,
        gt=0,
        description="Hole lifetime (s)"
    )
    
    D_n: float = Field(
        default=25.0,
        gt=0,
        description="Electron diffusion coefficient (cm^2/s)"
    )
    
    D_p: float = Field(
        default=10.0,
        gt=0,
        description="Hole diffusion coefficient (cm^2/s)"
    )
    
    L_n: float = Field(
        default=5e-4,
        gt=0,
        description="Electron diffusion length (cm)"
    )
    
    L_p: float = Field(
        default=5e-4,
        gt=0,
        description="Hole diffusion length (cm)"
    )
    
    @field_validator('tau_n', 'tau_p')
    def validate_lifetime(cls, v, info):
        field_name = info.field_name
        if v < 1e-12:
            raise ValueError(
                f"{field_name} = {v:.2e} s is extremely short. "
                "Typical lifetimes are between 1e-9 and 1e-3 s."
            )
        if v > 1e-2:
            raise ValueError(
                f"{field_name} = {v:.2e} s is very long. "
                "Most semiconductor lifetimes are below 1e-3 s."
            )
        return v
    
    @field_validator('D_n', 'D_p')
    def validate_diffusion_coeff(cls, v, info):
        field_name = info.field_name
        if v < 0.1:
            raise ValueError(
                f"{field_name} = {v} cm^2/s is very low. "
                "Typical diffusion coefficients are between 1 and 1000 cm^2/s."
            )
        if v > 10000:
            raise ValueError(
                f"{field_name} = {v} cm^2/s is extremely high. "
                "Most semiconductors have diffusion coefficients below 1000 cm^2/s."
            )
        return v
    
    @field_validator('L_n', 'L_p')
    def validate_diffusion_length(cls, v, info):
        field_name = info.field_name
        if v < 1e-6:
            raise ValueError(
                f"{field_name} = {v} cm is very short. "
                "Typical diffusion lengths are between 1e-5 and 1e-2 cm."
            )
        if v > 1e-1:
            raise ValueError(
                f"{field_name} = {v} cm is very long. "
                "Most diffusion lengths are below 1e-2 cm."
            )
        return v
    
    @model_validator(mode='after')
    def validate_einstein_relation(cls, values):
        """Check if diffusion coefficient and length are consistent with lifetime."""
        tau_n = values.tau_n
        tau_p = values.tau_p
        D_n = values.D_n
        D_p = values.D_p
        L_n = values.L_n
        L_p = values.L_p
        
        if all(x is not None for x in [tau_n, D_n, L_n]):
            expected_L_n = (D_n * tau_n) ** 0.5
            ratio_n = L_n / expected_L_n
            if not (0.1 <= ratio_n <= 10):
                raise ValueError(
                    f"Electron diffusion length L_n = {L_n:.2e} cm is inconsistent with "
                    f"D_n = {D_n} cm^2/s and tau_n = {tau_n:.2e} s. "
                    f"Expected L_n ≈ {expected_L_n:.2e} cm from L = sqrt(D*tau)."
                )
        
        if all(x is not None for x in [tau_p, D_p, L_p]):
            expected_L_p = (D_p * tau_p) ** 0.5
            ratio_p = L_p / expected_L_p
            if not (0.1 <= ratio_p <= 10):
                raise ValueError(
                    f"Hole diffusion length L_p = {L_p:.2e} cm is inconsistent with "
                    f"D_p = {D_p} cm^2/s and tau_p = {tau_p:.2e} s. "
                    f"Expected L_p ≈ {expected_L_p:.2e} cm from L = sqrt(D*tau)."
                )
        
        return values


class PNJunctionSchema(DeviceConfigSchema, DopingMixin, TransportMixin):
    """Schema for PN Junction diode parameters."""
    pass


class LEDSchema(DeviceConfigSchema, DopingMixin):
    """Schema for LED parameters."""
    
    efficiency: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Radiative recombination efficiency (0 to 1)"
    )
    
    B: float = Field(
        default=1e-10,
        gt=0,
        description="Radiative recombination coefficient (cm^3/s)"
    )
    
    D_n: float = Field(
        default=25.0,
        gt=0,
        description="Electron diffusion coefficient (cm^2/s)"
    )
    
    D_p: float = Field(
        default=10.0,
        gt=0,
        description="Hole diffusion coefficient (cm^2/s)"
    )
    
    L_n: float = Field(
        default=5e-4,
        gt=0,
        description="Electron diffusion length (cm)"
    )
    
    L_p: float = Field(
        default=5e-4,
        gt=0,
        description="Hole diffusion length (cm)"
    )
    
    @field_validator('B')
    def validate_B_coefficient(cls, v):
        if v < 1e-18:
            raise ValueError(
                f"Radiative recombination coefficient B = {v:.2e} cm^3/s is extremely low. "
                "Typical values are between 1e-15 and 1e-8 cm^3/s."
            )
        if v > 1e-6:
            raise ValueError(
                f"Radiative recombination coefficient B = {v:.2e} cm^3/s is extremely high. "
                "Most values are below 1e-8 cm^3/s."
            )
        return v
    
    @field_validator('D_n', 'D_p')
    def validate_diffusion_coeff(cls, v, info):
        field_name = info.field_name
        if v < 0.1:
            raise ValueError(
                f"{field_name} = {v} cm^2/s is very low. "
                "Typical diffusion coefficients are between 1 and 1000 cm^2/s."
            )
        if v > 10000:
            raise ValueError(
                f"{field_name} = {v} cm^2/s is extremely high. "
                "Most semiconductors have diffusion coefficients below 1000 cm^2/s."
            )
        return v
    
    @field_validator('L_n', 'L_p')
    def validate_diffusion_length(cls, v, info):
        field_name = info.field_name
        if v < 1e-6:
            raise ValueError(
                f"{field_name} = {v} cm is very short. "
                "Typical diffusion lengths are between 1e-5 and 1e-2 cm."
            )
        if v > 1e-1:
            raise ValueError(
                f"{field_name} = {v} cm is very long. "
                "Most diffusion lengths are below 1e-2 cm."
            )
        return v


class SolarCellSchema(DeviceConfigSchema, DopingMixin, TransportMixin):
    """Schema for Solar Cell parameters."""
    pass


class SolarCellSchema(DeviceConfigSchema, DopingMixin):
    """Schema for Solar Cell parameters."""
    
    light_intensity: float = Field(
        default=1.0,
        ge=0.0,
        description="Incident light intensity (arbitrary units)"
    )
    
    @field_validator('light_intensity')
    def validate_light_intensity(cls, v):
        if v > 10.0:
            raise ValueError(
                f"Light intensity {v} is very high. "
                "Typical values are between 0 and 5 for simulation purposes."
            )
        return v


class ZenerDiodeSchema(DeviceConfigSchema, DopingMixin, TransportMixin):
    """Schema for Zener Diode parameters."""
    
    v_zener: float = Field(
        gt=0,
        description="Zener breakdown voltage (V)"
    )
    
    @field_validator('v_zener')
    def validate_zener_voltage(cls, v):
        if v < 1.0:
            raise ValueError(
                f"Zener voltage {v} V is very low. "
                "Typical Zener voltages are between 2 and 100 V."
            )
        if v > 1000:
            raise ValueError(
                f"Zener voltage {v} V is extremely high. "
                "Most Zener diodes operate below 200 V."
            )
        return v


class TunnelDiodeSchema(DeviceConfigSchema, DopingMixin, TransportMixin):
    """Schema for Tunnel Diode parameters."""
    
    @field_validator('doping_p', 'doping_n')
    def validate_tunnel_doping(cls, v, info):
        field_name = info.field_name
        # Tunnel diodes require very high doping for degeneracy
        if v < 1e18:
            raise ValueError(
                f"{field_name} = {v:.2e} cm^-3 is too low for tunnel diode operation. "
                "Tunnel diodes require degenerate doping levels > 1e18 cm^-3."
            )
        return v


class VaractorDiodeSchema(DeviceConfigSchema, DopingMixin, TransportMixin):
    """Schema for Varactor Diode parameters."""
    pass


class MOSCapacitorSchema(DeviceConfigSchema):
    """Schema for MOS Capacitor parameters."""
    
    doping: float = Field(
        gt=0,
        description="Substrate doping concentration (cm^-3)"
    )
    
    oxide_thickness: float = Field(
        gt=0,
        description="Oxide thickness (cm)"
    )
    
    oxide_permittivity: float = Field(
        default=3.9,
        gt=0,
        description="Relative permittivity of oxide"
    )
    
    @field_validator('doping')
    def validate_substrate_doping(cls, v):
        if v < 1e13:
            raise ValueError(
                f"Substrate doping {v:.2e} cm^-3 is very low. "
                "Typical substrate doping is between 1e14 and 1e18 cm^-3."
            )
        if v > 1e20:
            raise ValueError(
                f"Substrate doping {v:.2e} cm^-3 is extremely high. "
                "Most substrates have doping below 1e19 cm^-3."
            )
        return v
    
    @field_validator('oxide_thickness')
    def validate_oxide_thickness(cls, v):
        if v < 1e-8:
            raise ValueError(
                f"Oxide thickness {v} cm is extremely thin. "
                "Typical oxide thickness is between 1e-7 and 1e-5 cm."
            )
        if v > 1e-4:
            raise ValueError(
                f"Oxide thickness {v} cm is very thick. "
                "Most gate oxides are below 1e-5 cm thick."
            )
        return v