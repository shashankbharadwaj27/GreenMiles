# Backend/preprocess/ev_preprocess.py
import pandas as pd
import numpy as np
import logging
from fastapi import HTTPException
from Backend.utils.ev_feature_reference import TRAINED_FEATURES

# Ensure logging is set up if this module is run standalone
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# --- REVISED: Added 'is_training_data' to function signature ---
def preprocess_ev_input(input_data: dict | pd.DataFrame, is_training_data: bool = False) -> pd.DataFrame:
    """
    Preprocesses EV input data for both inference (single dict) and training (DataFrame).
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
    ambient_map = {'cold': 0, 'mild': 1, 'hot': 2}
    df['ambient_temp'] = df['ambient_temp'].astype(str).str.lower()
    
    if single_row_mode:
        if df['ambient_temp'].iloc[0] not in ambient_map:
            raise HTTPException(status_code=400, detail=f"Invalid ambient_temp: {df['ambient_temp'].iloc[0]}. Expected 'cold', 'mild', or 'hot'.")
        df['ambient_temp'] = ambient_map[df['ambient_temp'].iloc[0]]
    else:
        if not df['ambient_temp'].isin(ambient_map.keys()).all() and is_training_data: # Use is_training_data here
            invalid_temps = df[~df['ambient_temp'].isin(ambient_map.keys())]['ambient_temp'].unique()
            logging.warning(f"Invalid ambient_temp values found: {invalid_temps}. These will be mapped to 0.")
        df['ambient_temp'] = df['ambient_temp'].map(ambient_map).fillna(0).astype(int)


    # 2. Handle 'hvac_on' boolean/binary conversion
    if 'hvac_on' in df.columns:
        if pd.api.types.is_bool_dtype(df['hvac_on']):
            df['hvac_on'] = df['hvac_on'].astype(int)
        else:
            hvac_map = {'yes': 1, 'no': 0}
            df['hvac_on'] = df['hvac_on'].astype(str).str.lower().map(hvac_map).fillna(0).astype(int)
    else:
        df['hvac_on'] = 0


    # 3. Normalize casing for driving_mode and drive_type
    df['driving_mode'] = df['driving_mode'].astype(str).str.capitalize()
    df['drive_type'] = df['drive_type'].astype(str).str.upper()

    # 4. Handle 'eco_mode_flag'
    df['eco_mode_flag'] = (df['driving_mode'] == 'Eco').astype(int)

    # 5. Derived features
    for col in ['battery_percentage', 'battery_capacity_kwh', 'total_power_kw']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
        else:
            df[col] = 0.0

    df["battery_per_kWh"] = (df["battery_percentage"] / df["battery_capacity_kwh"].replace(0, np.nan)).fillna(0).astype(float)
    df["battery_remaining_kWh"] = (df["battery_capacity_kwh"] * df["battery_percentage"] / 100).fillna(0).astype(float)

    # 'power_efficiency_ratio' and 'range_per_kWh' are NOT created here

    # 6. Handle Categorical Features using One-Hot Encoding
    df['driving_mode'] = pd.Categorical(df['driving_mode'], categories=['Normal', 'Sport', 'Eco'])
    df['drive_type'] = pd.Categorical(df['drive_type'], categories=['FWD', 'RWD'])

    df = pd.get_dummies(df, columns=['driving_mode', 'drive_type'], drop_first=False)
    
    for col in ['driving_mode_Normal', 'driving_mode_Sport', 'driving_mode_Eco', 
                'drive_type_FWD', 'drive_type_RWD']:
        if col in df.columns:
            df[col] = df[col].astype('category')
        else:
            df[col] = 0
            df[col] = df[col].astype('category')

    # 7. Align with TRAINED_FEATURES
    df = df.reindex(columns=TRAINED_FEATURES, fill_value=0)
    return df