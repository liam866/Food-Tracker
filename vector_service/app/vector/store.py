import logging
from qdrant_client import QdrantClient
from app.core.config import settings

logger = logging.getLogger(__name__)

qdrant_client = QdrantClient(url=settings.QDRANT_URL)
COLLECTION_NAME = "foods"

async def search_vectors(embedding: list, limit: int = 20, score_threshold: float = 0.0):
    try:
        return qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=embedding,
            limit=limit,
            score_threshold=score_threshold
        )
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return []
