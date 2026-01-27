from sqlalchemy import case, func
from sqlalchemy.orm import Session
from app.db.models import Food

def search_foods_service(db: Session, query: str):
    q = query.lower()
    results = (
        db.query(Food)
        .filter(Food.name.ilike(f"%{q}%"))
        .order_by(
            case(
                (func.lower(Food.name) == q, 0),              # exact match
                (func.lower(Food.name).startswith(q), 1),     # prefix match
                else_=2
            ),
            func.length(Food.name)                            # shorter names first
        )
        .limit(20)
        .all()
    )
    return results

def get_food_by_id_service(db: Session, food_id: int):
    return db.query(Food).filter(Food.id == food_id).first()
