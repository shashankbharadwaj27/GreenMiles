from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routes import predict_ev, predict_hv  # ✅ Just import both
import logging

# logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = FastAPI(
    title="EV + HV Range Predictor",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(predict_ev.router)
app.include_router(predict_hv.router)
