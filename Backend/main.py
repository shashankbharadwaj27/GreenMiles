# Backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routes.predict_ev import router as ev_router # Explicitly import router as alias
from Backend.routes.predict_hv import router as hv_router # Explicitly import router as alias
from Backend.routes.suggestions import router as suggestion_router # New import for suggestions
import logging

# logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = FastAPI(
    title="EV + HV Range Predictor & Suggestions", # Updated title
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with prefixes and tags for better organization in docs
app.include_router(ev_router, prefix="/predict", tags=["EV Prediction"])
app.include_router(hv_router, prefix="/predict", tags=["HV Prediction"])
app.include_router(suggestion_router, prefix="/suggest", tags=["Suggestions"]) # New router inclusion