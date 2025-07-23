# Backend/schemas/ev_schema.py
from pydantic import BaseModel

class EVInput(BaseModel):
    # Raw inputs directly from ev_data.csv structure
    battery_percentage: float
    battery_age_years: float
    battery_capacity_kwh: float
    ambient_temp: str # From ev_data.csv (e.g., 'cold', 'mild', 'hot')
    terrain_slope: float
    speed_avg_kmph: float
    acceleration_level: float
    hvac_on: bool # From ev_data.csv (True/False or 'yes'/'no' mapped to bool)
    driving_mode: str
    drive_type: str
    cargo_volume_liters: float
    top_speed_kmph: float
    total_power_kw: float
    total_torque_nm: float
    # Note: 'battery_per_kWh' and 'battery_remaining_kWh' are derived *after* input in preprocessing