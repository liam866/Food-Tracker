from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    progress: str
    improvement: str
    encouragement: str
