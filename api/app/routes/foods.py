from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.clients.relational_client import RelationalClient, get_relational_client
from app.services.food.food_search import search_foods_service, get_food_by_id_service
from app.schemas.food import FoodSchema

router = APIRouter()

@router.get("/foods/search", response_model=List[FoodSchema])
async def search_foods(q: Optional[str] = None, db_client: RelationalClient = Depends(get_relational_client)):
    if not q:
        return []
    foods = search_foods_service(db_client, q)
    return foods

@router.get("/foods/{food_id}", response_model=FoodSchema)
async def get_food_details(food_id: int, db_client: RelationalClient = Depends(get_relational_client)):
    food = get_food_by_id_service(db_client, food_id)
    if not food:
        raise HTTPException(status_code=44, detail="Food not found")
    return food
