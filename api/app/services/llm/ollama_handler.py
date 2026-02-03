import logging
import json
import re
from typing import Optional, Dict, Any, TYPE_CHECKING

from app.schemas.ollama import OllamaGenerateRequest
from app.core.config import settings

if TYPE_CHECKING:
    from app.clients.ollama_client import OllamaClient

logger = logging.getLogger(__name__)

async def generate_response(prompt: str, ollama_client: "OllamaClient") -> Optional[Dict[str, Any]]:
    logger.info("[OllamaHandler] Sending prompt to Ollama...")

    try:
        ollama_request = OllamaGenerateRequest(
            model=settings.OLLAMA_MODEL,
            prompt=prompt,
            stream=False,
            options={
                "temperature": 0.7,
                "num_predict": 128,
            }
        )

        ollama_raw_response = await ollama_client.generate(ollama_request)
        raw_response_text = ollama_raw_response.response.strip()
        logger.info(f"[OllamaHandler] Raw response: {raw_response_text}")

        # Strip triple backticks and possible language hints (e.g. ```json)
        cleaned_text = re.sub(r"^```[\w]*\n?", "", raw_response_text)
        cleaned_text = re.sub(r"\n?```$", "", cleaned_text)

        # Use regex to extract JSON object (including multiline)
        json_match = re.search(r"\{.*\}", cleaned_text, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            try:
                parsed_json = json.loads(json_string)
                return parsed_json
            except json.JSONDecodeError as e:
                logger.error(f"[OllamaHandler] JSON decoding error: {e}. Extracted JSON string: {json_string}")
                return None
        else:
            logger.error("[OllamaHandler] Could not find valid JSON in cleaned LLM response text.")
            return None

    except Exception as e:
        logger.error(f"[OllamaHandler] Error during Ollama interaction: {e}")
        return None
