import logging
import httpx
from typing import List, Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class VisionClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.VISION_SERVICE_URL

    async def extract_menu(self, image_content: bytes) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=60.0) as client:
            try:
                files = {'image': ('menu.jpg', image_content, 'image/jpeg')}
                resp = await client.post("/extract-menu", files=files)
                resp.raise_for_status()
                # Returns {"items": [...]}
                return resp.json().get("items", [])
            except Exception as e:
                logger.error(f"Vision service error: {e}")
                return []

def get_vision_client() -> VisionClient:
    return VisionClient()
