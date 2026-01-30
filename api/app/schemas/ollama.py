from pydantic import BaseModel
from typing import Optional, Dict, Any

class OllamaGenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = False
    options: Optional[Dict[str, Any]] = None

class OllamaGenerateResponse(BaseModel):
    response: str

