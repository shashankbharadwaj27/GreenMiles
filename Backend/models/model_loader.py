import joblib
import os

def load_ev_model():
    model_path = os.path.join(os.path.dirname(__file__), "ev_model.joblib")
    return joblib.load(model_path)