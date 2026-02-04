import logging
import httpx
import json

from app.schemas.ollama import OllamaGenerateRequest, OllamaGenerateResponse

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
        logger.info(f"[OllamaClient] Initialized with base URL: {self.base_url}")

    async def generate(self, request: OllamaGenerateRequest) -> OllamaGenerateResponse:
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = request.model_dump_json(by_alias=True)

        logger.info(f"[OllamaClient] Sending generate request to {url} with model {request.model}")
        try:
            response = await self.client.post(url, headers=headers, content=data, timeout=60.0)
            response.raise_for_status()
            raw_response_data = response.json()
            logger.info(f"[OllamaClient] Received raw response (status {response.status_code})")
            return OllamaGenerateResponse(**raw_response_data)
        except httpx.RequestError as e:
            logger.error(f"[OllamaClient] HTTPX Request Error: {e}")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"[OllamaClient] HTTP Status Error: {e.response.status_code} - {e.response.text}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"[OllamaClient] JSON Decode Error: {e} - Response text: {response.text}")
            raise
        except Exception as e:
            logger.error(f"[OllamaClient] An unexpected error occurred during generate: {e}")
            raise

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        logger.info("[OllamaClient] HTTPX client closed.")
