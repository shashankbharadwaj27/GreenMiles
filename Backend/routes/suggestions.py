# Backend/routes/suggestions.py

from fastapi import APIRouter
from Backend.schemas.ev_schema import EVInput
from Backend.schemas.hv_schema import HVInput # FIX: Corrected import from HVInputData to HVInput
from Backend.schemas.suggestion_schema import SuggestionResponse
from Backend.agents.suggestion_agent import get_ev_suggestions, get_hv_suggestions

router = APIRouter()

@router.post("/ev/suggestions", response_model=SuggestionResponse)
def get_ev_predictive_suggestions(input_data: EVInput):
    """
    Provides rule-based suggestions for Electric Vehicle optimization based on input.
    """
    suggestions = get_ev_suggestions(input_data.dict())
    return {"suggestions": suggestions}

@router.post("/hv/suggestions", response_model=SuggestionResponse)
def get_hv_predictive_suggestions(input_data: HVInput): # FIX: Corrected type hint to HVInput
    """
    Provides rule-based suggestions for Hydrogen Vehicle optimization based on input.
    """
    suggestions = get_hv_suggestions(input_data.dict())
    return {"suggestions": suggestions}