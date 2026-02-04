import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.relational.database import get_db, engine
from app.relational import models
from app.clients.vector_client import VectorClient
from app.services.seeding_service import seed_data

logger = logging.getLogger(__name__)
vector_client = VectorClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Relational container startup.")
    
    # Initialize DB
    models.Base.metadata.create_all(bind=engine)
    
    # Ensure collection exists
    await vector_client.ensure_collection("foods")
    
    db = next(get_db())
    await seed_data(db, vector_client)
    db.close()
    
    yield
    logger.info("Relational container shutdown.")
