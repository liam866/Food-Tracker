import logging
import httpx
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class VectorClient:
    def __init__(self, base_url: str = "http://vector:8000"):
        self.base_url = base_url
        self.client = httpx.Client(base_url=self.base_url, timeout=30.0)

    def embed(self, text: str) -> List[float]:
        try:
            resp = self.client.post("/embed", json={"text": text})
            resp.raise_for_status()
            return resp.json()["embedding"]
        except Exception as e:
            logger.error(f"Embed failed: {e}")
            return []

    def search(self, vector: List[float], limit: int = 20, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        try:
            resp = self.client.post("/search", json={
                "vector": vector,
                "limit": limit,
                "score_threshold": score_threshold
            })
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def upsert(self, points: List[Dict[str, Any]]) -> bool:
        try:
            resp = self.client.post("/upsert", json={"points": points})
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Upsert failed: {e}")
            return False

    def ensure_collection(self, name: str) -> bool:
        try:
            resp = self.client.get(f"/collections/{name}")
            if resp.status_code == 200 and resp.json().get("exists"):
                return True
            
            # Create if not exists
            resp = self.client.put(f"/collections/{name}")
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"Collection check/create failed: {e}")
            return False
