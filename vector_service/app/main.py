import logging
from fastapi import FastAPI
from app.routes import vector
from app.core.lifespan import lifespan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)
app.include_router(vector.router)
