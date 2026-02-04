import logging
from typing import List, Dict, Any
from app.services.embedding import get_embedding
from app.services.store import search_vectors, qdrant_client, COLLECTION_NAME
from qdrant_client.http import models as qmodels
from qdrant_client.http.exceptions import UnexpectedResponse

logger = logging.getLogger(__name__)

async def generate_embedding(text: str) -> List[float]:
    return await get_embedding(text)

def search(vector: List[float], limit: int = 20, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
    hits = search_vectors(vector, limit, score_threshold)
    results = []
    for hit in hits:
        results.append({
            "id": hit.id,
            "score": hit.score,
            "payload": hit.payload
        })
    return results

def upsert_points(points: List[Dict[str, Any]]) -> int:
    q_points = []
    for p in points:
        q_points.append(qmodels.PointStruct(
            id=p['id'],
            vector=p['vector'],
            payload=p.get('payload')
        ))
    
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=q_points
    )
    return len(q_points)

def check_collection_exists(name: str) -> bool:
    try:
        qdrant_client.get_collection(name)
        return True
    except UnexpectedResponse as e:
        if e.status_code == 404:
            return False
        raise e
    except Exception as e:
        logger.error(f"Error checking collection: {e}")
        raise e

def create_collection(name: str):
    qdrant_client.create_collection(
        collection_name=name,
        vectors_config=qmodels.VectorParams(size=384, distance=qmodels.Distance.COSINE)
    )

def count_points(collection_name: str = COLLECTION_NAME) -> int:
    try:
        count_result = qdrant_client.count(collection_name=collection_name)
        return count_result.count
    except UnexpectedResponse as e:
        if e.status_code == 404:
            return 0 # Collection doesn't exist implies 0 points (or logic error in caller)
        raise e
    except Exception as e:
        logger.error(f"Count failed: {e}")
        raise e
