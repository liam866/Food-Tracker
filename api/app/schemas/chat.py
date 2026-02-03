from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    prompt: str

class ChatOverviewResponse(BaseModel):
    progress: str
    improvement: str
    encouragement: str
