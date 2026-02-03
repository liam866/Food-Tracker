from pydantic import BaseModel
from typing import List

class FoodContext(BaseModel):
    food_name: str
    calories: float
    protein: float

class MenuItem(BaseModel):
    name: str
    context: List[FoodContext]
