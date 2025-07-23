# Backend/utils/feature_reference.py
TRAINED_FEATURES = [
'battery_percentage', 'battery_age_years', 'ambient_temp', # ambient_temp will be numeric after preprocess
'terrain_slope', 'speed_avg_kmph', 'acceleration_level', 'hvac_on', # hvac_on will be numeric after preprocess
'cargo_volume_liters', 'top_speed_kmph', 'total_power_kw', 'total_torque_nm',
'battery_capacity_kwh',
'battery_per_kWh', # Derived in preprocess
'battery_remaining_kWh', # Derived in preprocess
'eco_mode_flag', # Derived in preprocess
'driving_mode_Normal', 'driving_mode_Sport', 'driving_mode_Eco', # One-hot encoded
'drive_type_FWD', 'drive_type_RWD' # One-hot encoded (no AWD expected by model)
]