# Backend/preprocess/hv_preprocess.py
import pandas as pd
import numpy as np
import logging
from fastapi import HTTPException
from Backend.utils.hv_feature_reference import TRAINED_FEATURES

# Setup basic logging if not already configured by main script (e.g., in evaluate_models.py)
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# --- Function to map numerical ambient_temp to categorical strings ---
# This function assumes the input temp_value is already a number.
# It should ONLY be applied AFTER converting a *numerical* 'ambient_temp' column from CSV.
def map_numeric_ambient_temp_to_categorical(temp_value):
    if temp_value < 5.0:
        return 'cold'
    elif 5.0 <= temp_value <= 25.0:
        return 'mild'
    else:
        return 'hot'


def preprocess_hv_input(input_data: dict | pd.DataFrame, is_training_data: bool = False) -> pd.DataFrame:
    """
    Preprocesses HV input data for both inference (single dict) and training (DataFrame).
    'is_training_data' flag helps differentiate behavior (e.g., error vs warning).
    """
    if isinstance(input_data, dict):
        df = pd.DataFrame([input_data])
        single_row_mode = True
    elif isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
        single_row_mode = False
    else:
        raise ValueError("Input data must be a dictionary (for single prediction) or a pandas DataFrame (for training).")


    # 1. Handle 'ambient_temp' ordinal encoding
    # --- CRITICAL FIX: REMOVE pd.to_numeric for ambient_temp here ---
    # df['ambient_temp'] = pd.to_numeric(df['ambient_temp'], errors='coerce') # <--- REMOVE THIS LINE
    
    # Ensure it's treated as string initially, then apply the map to get numeric categories.
    df['ambient_temp'] = df['ambient_temp'].astype(str).str.lower()
    
    ambient_map = {'cold': 0, 'mild': 1, 'hot': 2}

    if single_row_mode:
        if df['ambient_temp'].iloc[0] not in ambient_map:
            raise HTTPException(status_code=400, detail=f"Invalid ambient_temp: {df['ambient_temp'].iloc[0]}. Expected 'cold', 'mild', or 'hot'.")
        df['ambient_temp'] = ambient_map[df['ambient_temp'].iloc[0]]
    else: # For DataFrame
        if not df['ambient_temp'].isin(ambient_map.keys()).all() and is_training_data:
            invalid_temps = df[~df['ambient_temp'].isin(ambient_map.keys())]['ambient_temp'].unique()
            logging.warning(f"Invalid categorical ambient_temp values found: {invalid_temps}. These will be mapped to 0.")
        df['ambient_temp'] = df['ambient_temp'].map(ambient_map).fillna(0).astype(int)


    # 2. Handle 'hvac_on' mapping from 'yes'/'no' to binary (1/0)
    df['hvac_on'] = df['hvac_on'].astype(str).str.lower()
    
    hvac_map = {'yes': 1, 'no': 0}
    if single_row_mode:
        if df['hvac_on'].iloc[0] not in hvac_map:
            raise HTTPException(status_code=400, detail=f"Invalid hvac_on value: {df['hvac_on'].iloc[0]}. Expected 'yes' or 'no'.")
        df['hvac_on'] = hvac_map[df['hvac_on'].iloc[0]]
    else: # For DataFrame
        if not df['hvac_on'].isin(hvac_map.keys()).all() and is_training_data:
            invalid_hvac = df[~df['hvac_on'].isin(hvac_map.keys())]['hvac_on'].unique()
            logging.warning(f"Invalid hvac_on values found: {invalid_hvac}. These will be mapped to 0.")
        df['hvac_on'] = df['hvac_on'].map(hvac_map).fillna(0).astype(int)


    # 3. Create Derived Features (as per hv.csv generation logic)
    for col in ['hydrogen_percentage', 'fuel_cell_age_years', 'fuel_cell_efficiency', 'speed_avg_kmph', 'terrain_slope',
                'cargo_volume_liters', 'top_speed_kmph', 'total_power_kw', 'total_torque_nm', 'acceleration_level']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
        else:
            df[col] = 0.0

    df['speed_sq'] = (df['speed_avg_kmph'] ** 2).fillna(0).astype(float)
    df['abs_slope'] = abs(df['terrain_slope']).fillna(0).astype(float)
    
    # Placeholders for other potential derived features if your HV model training added them
    if 'hydrogen_per_year' not in df.columns:
        df['hydrogen_per_year'] = 0.0
    if 'age_squared' not in df.columns:
        df['age_squared'] = (df['fuel_cell_age_years'] ** 2).fillna(0).astype(float)
    if 'h2_x_efficiency' not in df.columns:
        df['h2_x_efficiency'] = (df['hydrogen_percentage'] * df['fuel_cell_efficiency']).fillna(0).astype(float)
    if 'h2_x_age' not in df.columns:
        df['h2_x_age'] = (df['hydrogen_percentage'] * df['fuel_cell_age_years']).fillna(0).astype(float)


    # 4. Handle Categorical Features using One-Hot Encoding
    df['driving_mode'] = df['driving_mode'].astype(str).str.lower()
    df['drive_type'] = df['drive_type'].astype(str).str.upper()

    df['driving_mode'] = pd.Categorical(df['driving_mode'], categories=['normal', 'sport', 'eco'])
    df['drive_type'] = pd.Categorical(df['drive_type'], categories=['FWD', 'RWD', 'AWD'])

    df = pd.get_dummies(df, columns=['driving_mode', 'drive_type'], drop_first=False)
    
    for col in ['driving_mode_normal', 'driving_mode_sport', 'driving_mode_eco', 
                'drive_type_FWD', 'drive_type_RWD', 'drive_type_AWD']:
        if col in df.columns:
            df[col] = df[col].astype('category')
        else:
            df[col] = 0
            df[col] = df[col].astype('category')


    # 5. Align with TRAINED_FEATURES
    df = df.reindex(columns=TRAINED_FEATURES, fill_value=0)
    return df