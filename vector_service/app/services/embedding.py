import logging
import httpx
from typing import List
from app.core.config import settings

logger = logging.getLogger(__name__)

async def get_embedding(text: str) -> List[float]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/embeddings",
                json={"model": settings.OLLAMA_MODEL, "prompt": text},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            logger.error(f"Failed to get embedding from Ollama: {e}")
            return []
