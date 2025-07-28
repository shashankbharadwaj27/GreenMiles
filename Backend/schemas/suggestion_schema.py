# Backend/schemas/suggestion_schema.py
from pydantic import BaseModel
from typing import List

class SuggestionResponse(BaseModel):
    suggestions: List[str]