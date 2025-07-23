# Backend/schemas/hv_schema.py
from pydantic import BaseModel

class HVInputData(BaseModel):
    # Raw inputs directly from hv.csv structure
    hydrogen_percentage: float
    fuel_cell_age_years: float
    fuel_cell_efficiency: float
    ambient_temp: str # <-- CRITICAL: ENSURE THIS IS 'str', NOT 'float'
    terrain_slope: float
    speed_avg_kmph: float
    acceleration_level: float
    hvac_on: str # In hv.csv it's 'yes'/'no' string, preprocess_hv_input will map this
    driving_mode: str
    drive_type: str
    cargo_volume_liters: float
    top_speed_kmph: float
    total_power_kw: float
    total_torque_nm: float