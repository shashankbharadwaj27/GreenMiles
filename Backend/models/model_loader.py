# Backend/models/model_loader.py
import joblib
import os

def load_ev_model():
    model_path = os.path.join(os.path.dirname(__file__), "ev_model.joblib")
    return joblib.load(model_path)

def load_hv_model(): # This function must be present exactly like this
    model_path = os.path.join(os.path.dirname(__file__), "hv_model.joblib")
    return joblib.load(model_path)