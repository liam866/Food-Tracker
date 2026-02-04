from pydantic import BaseModel
from typing import List, Optional

class MenuRecommendation(BaseModel):
    name: str
    reasoning: str

class MenuAnalysisResponse(BaseModel):
    recommendations: List[MenuRecommendation]
