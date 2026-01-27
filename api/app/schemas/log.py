from pydantic import BaseModel
from typing import List
from datetime import datetime

class FoodLogBase(BaseModel):
    food_id: int
    grams: float

class FoodLogCreate(FoodLogBase):
    pass

class FoodLogUpdate(BaseModel):
    grams: float

class FoodLoggedSchema(BaseModel):
    id: int
    food_id: int
    grams: float
    calories: float
    protein: float
    carbs: float
    fat: float
    datetime: datetime
    name: str

    class Config:
        orm_mode = True

class DailyLogSummary(BaseModel):
    logs: List[FoodLoggedSchema]
    totals: dict
    calorie_target: float
