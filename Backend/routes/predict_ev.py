from fastapi import APIRouter
import joblib
import os
from Backend.schemas.ev_schema import EVInput
from Backend.models.model_loader import load_ev_model
from Backend.preprocess.ev_preprocess import preprocess_ev_input

router = APIRouter()

# Load model
model = load_ev_model()

@router.post("/ev")
def predict_range(input_data: EVInput):
    input_dict = input_data.dict()
    print("Incoming data:", input_dict)

    try:
        df = preprocess_ev_input(input_dict)
        prediction = model.predict(df)[0]
        return {"predicted_range_km": round(float(prediction), 2)}
    except Exception as e:
        print("❌ Error during prediction:", e)
        return {"detail": "Internal Server Error"}