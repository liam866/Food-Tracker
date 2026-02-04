from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services import vector_service

router = APIRouter()

class EmbedRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    vector: List[float]
    limit: int = 20
    score_threshold: float = 0.0

class UpsertRequest(BaseModel):
    points: List[Dict[str, Any]]

@router.post("/embed")
async def embed(request: EmbedRequest):
    embedding = await vector_service.generate_embedding(request.text)
    return {"embedding": embedding}

@router.post("/search")
async def search(request: SearchRequest):
    return vector_service.search(request.vector, request.limit, request.score_threshold)

@router.post("/upsert")
async def upsert(request: UpsertRequest):
    count = vector_service.upsert_points(request.points)
    return {"success": True, "count": count}

@router.get("/collections/{name}")
async def get_collection(name: str):
    try:
        exists = vector_service.check_collection_exists(name)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Vector DB error: {e}")

@router.put("/collections/{name}")
async def create_collection(name: str):
    try:
        vector_service.create_collection(name)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/collections/{name}/count")
async def count_collection(name: str):
    try:
        count = vector_service.count_points(name)
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
