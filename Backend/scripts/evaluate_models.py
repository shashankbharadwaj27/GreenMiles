import pandas as pd
import joblib
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import logging

# Setup basic logging if not already configured by main script
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# --- Import HV-specific preprocessing and features (always needed for HV) ---
from Backend.preprocess.hv_preprocess import preprocess_hv_input
from Backend.utils.hv_feature_reference import TRAINED_FEATURES as HV_TRAINED_FEATURES

# --- Conditionally import EV-specific preprocessing and features ---
# This block will try to import EV components. If they are not present,
# it will log a warning and set the ev_imports_available flag to False,
# allowing the script to run without crashing, focusing only on the HV model.
ev_imports_available = False
try:
    from Backend.preprocess.ev_preprocess import preprocess_ev_input
    from Backend.utils.ev_feature_reference import TRAINED_FEATURES as EV_TRAINED_FEATURES
    ev_imports_available = True
except ImportError:
    logging.warning("EV model preprocessing or feature reference files not found. EV model evaluation will be skipped.")
except Exception as e:
    logging.error(f"An unexpected error occurred during EV import check: {e}. EV model evaluation will be skipped.")
    

def evaluate_model(model, preprocess_func, test_data_path, actual_range_col, trained_features_list):
    """
    Evaluates a given model using a test dataset and calculates regression metrics.
    """
    logging.info(f"\n--- Evaluating Model: {os.path.basename(test_data_path).replace('.csv', '')} ---")
    try:
        # Load test data
        test_df = pd.read_csv(test_data_path)
        actual_ranges = test_df[actual_range_col]
        input_features_df = test_df.drop(columns=[actual_range_col])

        # Preprocess test data using the flexible preprocess function
        preprocessed_test_df = preprocess_func(input_features_df, is_training_data=True)


        # Make predictions
        predictions = model.predict(preprocessed_test_df)

        # Calculate metrics
        mae = mean_absolute_error(actual_ranges.loc[preprocessed_test_df.index], predictions)
        mse = mean_squared_error(actual_ranges.loc[preprocessed_test_df.index], predictions)
        rmse = np.sqrt(mse) # Calculate RMSE from MSE
        r2 = r2_score(actual_ranges.loc[preprocessed_test_df.index], predictions)

        logging.info(f"  Mean Absolute Error (MAE): {mae:.2f} km")
        logging.info(f"  Root Mean Squared Error (RMSE): {rmse:.2f} km")
        logging.info(f"  R-squared (R²): {r2:.4f}")

    except FileNotFoundError:
        logging.error(f"Error: Test data file not found at {test_data_path}. Please ensure it is in the correct directory.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during evaluation of {os.path.basename(test_data_path)}: {e}")


if __name__ == "__main__":
    # --- Paths to your models and test data ---
    EV_MODEL_PATH = os.path.join("Backend", "models", "ev_model.joblib")
    HV_MODEL_PATH = os.path.join("Backend", "models", "hv_model.joblib")

    # Use the provided CSV files as test data
    EV_TEST_DATA_PATH = "ev_data.csv"
    HV_TEST_DATA_PATH = "hv.csv"

    # --- Load Models ---
    ev_model = None
    hv_model = None

    # Load EV model only if its imports are available and then evaluate
    if ev_imports_available:
        try:
            ev_model = joblib.load(EV_MODEL_PATH)
            logging.info(f"Successfully loaded EV model from {EV_MODEL_PATH}")
        except FileNotFoundError:
            logging.error(f"Error: EV model file not found at {EV_MODEL_PATH}. Make sure you have trained it.")
        except Exception as e:
            logging.error(f"An error occurred loading the EV model: {e}")
            ev_model = None # Ensure ev_model is None if loading fails

    try:
        hv_model = joblib.load(HV_MODEL_PATH)
        logging.info(f"Successfully loaded HV model from {HV_MODEL_PATH}")
    except FileNotFoundError:
        logging.error(f"Error: HV model file not found at {HV_MODEL_PATH}. Make sure you have trained it.")
    except Exception as e:
        logging.error(f"An error occurred loading the HV model: {e}")
        hv_model = None # Ensure hv_model is None if loading fails


    # --- Evaluate EV Model ---
    if ev_model and ev_imports_available: # Ensure model loaded AND imports available
        evaluate_model(ev_model, preprocess_ev_input, EV_TEST_DATA_PATH,
                       actual_range_col='electric_range_km', trained_features_list=EV_TRAINED_FEATURES)
    else:
        logging.info("Skipping EV model evaluation (files not present or model not loaded).")

    # --- Evaluate HV Model ---
    if hv_model: # Evaluate HV if its model loaded
        evaluate_model(hv_model, preprocess_hv_input, HV_TEST_DATA_PATH,
                       actual_range_col='range_in_km', trained_features_list=HV_TRAINED_FEATURES)
    else:
        logging.info("Skipping HV model evaluation (model not loaded).")