import logging
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from app.core.config import settings
from app.vector.store import search_vectors, qdrant_client, COLLECTION_NAME
from qdrant_client.http import models as qmodels

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.vector.embedding import get_embedding

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Vector service startup.")
    yield
    logger.info("Vector service shutdown.")

app = FastAPI(lifespan=lifespan)

class EmbedRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    vector: List[float]
    limit: int = 20
    score_threshold: float = 0.0

class UpsertRequest(BaseModel):
    points: List[Dict[str, Any]]

@app.post("/embed")
async def embed(request: EmbedRequest):
    embedding = await get_embedding(request.text)
    return {"embedding": embedding}

@app.post("/search")
async def search(request: SearchRequest):
    hits = await search_vectors(request.vector, request.limit, request.score_threshold)
    results = []
    for hit in hits:
        results.append({
            "id": hit.id,
            "score": hit.score,
            "payload": hit.payload
        })
    return results

@app.post("/upsert")
async def upsert(request: UpsertRequest):
    try:
        points = []
        for p in request.points:
            points.append(qmodels.PointStruct(
                id=p['id'],
                vector=p['vector'],
                payload=p.get('payload')
            ))
        
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        return {"success": True, "count": len(points)}
    except Exception as e:
        logger.error(f"Upsert failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections/{name}")
async def get_collection(name: str):
    try:
        qdrant_client.get_collection(name)
        return {"exists": True}
    except Exception:
        return {"exists": False}

@app.put("/collections/{name}")
async def create_collection(name: str):
    try:
        qdrant_client.create_collection(
            collection_name=name,
            vectors_config=qmodels.VectorParams(size=384, distance=qmodels.Distance.COSINE)
        )
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
