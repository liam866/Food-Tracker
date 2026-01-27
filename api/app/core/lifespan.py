from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.db.init_db import create_db_and_tables, ingest_food_data
from app.db.database import SessionLocal

async def lifespan_handler(app: FastAPI):
    create_db_and_tables()
    db: Session = SessionLocal()
    try:
        ingest_food_data(db)
    finally:
        db.close()
