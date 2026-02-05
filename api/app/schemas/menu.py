from pydantic import BaseModel
from typing import List, Optional
from app.schemas.retrieval import FoodContext

class MenuRecommendation(BaseModel):
    name: str
    reasoning: str
    context: List[FoodContext] = []

class MenuAnalysisResponse(BaseModel):
    recommendations: List[MenuRecommendation]
