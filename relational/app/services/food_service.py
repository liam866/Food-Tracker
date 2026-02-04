import logging
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.relational import models

logger = logging.getLogger(__name__)

async def search_foods(query: str, db: Session):
    q = query.lower()
    return (
        db.query(models.Food)
        .filter(models.Food.name.ilike(f"%{q}%"))
        .order_by(
            case(
                (func.lower(models.Food.name) == q, 0),              # exact match
                (func.lower(models.Food.name).startswith(q), 1),     # prefix match
                else_=2
            ),
            func.length(models.Food.name)                            # shorter names first
        )
        .limit(20)
        .all()
    )

def get_food_by_id(food_id: int, db: Session):
    return db.query(models.Food).filter(models.Food.id == food_id).first()
