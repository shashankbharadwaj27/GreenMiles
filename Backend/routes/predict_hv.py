# Backend/routes/predict_hv.py

from fastapi import APIRouter, HTTPException
from Backend.schemas.hv_schema import HVInput
from Backend.models.model_loader import load_hv_model
from Backend.preprocess.hv_preprocess import preprocess_hv_input
import math # Import math for isnan

router = APIRouter()

# Load model once when the application starts
model = load_hv_model()

@router.post("/hv")
def predict_hv_range(data: HVInput):
    """
    Predicts the range of a Hydrogen Vehicle based on input data.
    """
    input_dict = data.dict()
    print("--- HV DEBUG: Endpoint hit! Received data:", input_dict)

    try:
        df = preprocess_hv_input(input_dict)

        # Ensure the DataFrame is not empty or malformed after preprocessing
        if df.empty:
            raise ValueError("Preprocessing resulted in an empty DataFrame.")
        if not all(col in df.columns for col in df.columns): # Basic check for column integrity
             raise ValueError("Preprocessing resulted in missing columns required for prediction.")

        prediction = model.predict(df)
        
        # Check if prediction is valid before returning
        if prediction is None or len(prediction) == 0:
            raise ValueError("Model returned no prediction.")

        predicted_value = float(prediction[0])

        if math.isnan(predicted_value) or not math.isfinite(predicted_value):
            # This catches NaN or infinite values from the model
            raise ValueError(f"Model returned invalid prediction: {predicted_value}")

        return {"predicted_range_km": round(predicted_value, 2)}

    except Exception as e:
        print("❌ Error during HV prediction:", e)
        # Return a 500 Internal Server Error for unhandled exceptions or prediction errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error during prediction: {e}. Check backend logs for details.")