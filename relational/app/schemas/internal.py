from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class LogCreate(BaseModel):
    food_id: int
    grams: float

class LogUpdate(BaseModel):
    grams: float

class UserProfileUpdate(BaseModel):
    name: str
    height_cm: float
    weight_kg: float
    age: int
    sex: str
    goal: str
    calorie_target: float
    protein_target: float

class RetrievalRequest(BaseModel):
    menu_items: List[str]
