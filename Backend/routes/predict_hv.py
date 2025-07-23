from fastapi import APIRouter
import joblib
import os
from Backend.schemas.hv_schema import HVInputData
from Backend.preprocess.hv_preprocess import preprocess_hv_input

router = APIRouter()

# Load model
model_path = os.path.join("Backend", "models", "hv_model.joblib")
model = joblib.load(model_path)

@router.post("/predict/hv")
def predict_hv_range(data: HVInputData):
    input_dict = data.dict()
    df = preprocess_hv_input(input_dict)
    prediction = model.predict(df)
    return {"predicted_range_km": round(float(prediction[0]), 2)}