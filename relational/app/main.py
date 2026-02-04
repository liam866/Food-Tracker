import logging
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.routes import retrieval, foods, logs, user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

app.include_router(retrieval.router)
app.include_router(foods.router)
app.include_router(logs.router)
app.include_router(user.router)
