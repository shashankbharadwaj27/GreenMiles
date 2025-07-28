import joblib
import os

try:
    model_path = os.path.join(os.path.dirname(__file__), "hv_model.joblib")
    model = joblib.load(model_path)
    print("HV model loaded successfully!")
except Exception as e:
    print(f"Error loading HV model: {e}")