import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Vector service startup.")
    yield
    logger.info("Vector service shutdown.")
