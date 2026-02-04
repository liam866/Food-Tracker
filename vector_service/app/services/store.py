import logging
from qdrant_client import QdrantClient
from app.core.config import settings

logger = logging.getLogger(__name__)

qdrant_client = QdrantClient(url=settings.QDRANT_URL)
COLLECTION_NAME = "foods"

def search_vectors(embedding: list, limit: int = 20, score_threshold: float = 0.0):
    try:
        result = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=embedding,
            limit=limit,
            score_threshold=score_threshold
        )
        return result.points
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return []
