import logging
from sqlalchemy.orm import Session
from app.relational import models
from app.clients.vector_client import VectorClient

logger = logging.getLogger(__name__)
vector_client = VectorClient()

async def search_foods(query: str, db: Session):
    embedding = await vector_client.embed(query)
    if not embedding:
        return []
    
    search_hits = await vector_client.search(embedding, limit=20)
    
    ids = [hit['id'] for hit in search_hits]
    if not ids:
        return []
    
    foods = db.query(models.Food).filter(models.Food.id.in_(ids)).all()
    food_map = {f.id: f for f in foods}
    ordered_foods = [food_map[id] for id in ids if id in food_map]
    
    return ordered_foods

def get_food_by_id(food_id: int, db: Session):
    return db.query(models.Food).filter(models.Food.id == food_id).first()
