from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.relational.database import get_db
from app.services.food_service import search_foods, get_food_by_id

router = APIRouter()

@router.get("/foods/search")
async def search_foods_endpoint(query: str, db: Session = Depends(get_db)):
    return await search_foods(query, db)

@router.get("/foods/{food_id}")
async def get_food_by_id_endpoint(food_id: int, db: Session = Depends(get_db)):
    return get_food_by_id(food_id, db)
