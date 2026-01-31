from typing import List, Optional
from pydantic import BaseModel

class MenuItem(BaseModel):
    section: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None

class MenuResponse(BaseModel):
    items: List[MenuItem]
