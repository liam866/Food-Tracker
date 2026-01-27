from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.db.models import Food
from app.services.food_search import search_foods_service, get_food_by_id_service
from app.schemas.food import FoodSchema

router = APIRouter()

@router.get("/foods/search", response_model=List[FoodSchema])
async def search_foods(q: Optional[str] = None, db: Session = Depends(get_db)):
    if not q:
        return []
    foods = search_foods_service(db, q)
    return foods

@router.get("/foods/{food_id}", response_model=FoodSchema)
async def get_food_details(food_id: int, db: Session = Depends(get_db)):
    food = get_food_by_id_service(db, food_id)
    if not food:
        raise HTTPException(status_code=44, detail="Food not found")
    return food
