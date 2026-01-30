import logging
import json
import re
from typing import TYPE_CHECKING  # For type hinting without circular imports

from app.schemas.chat import ChatResponse
from app.schemas.ollama import OllamaGenerateRequest
from app.core.config import settings

# Conditional import for type hinting only
if TYPE_CHECKING:
    from api.app.services.ollama_client import OllamaClient 

logger = logging.getLogger(__name__)

async def send_to_ollama(prompt: str, ollama_client: "OllamaClient") -> ChatResponse:
    logger.info("[CHATSERVICE] Orchestrating prompt to Ollama...")
    
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
        logger.info(f"[CHATSERVICE] Raw response from Ollama wrapper: {raw_response_text}")

        # Strip triple backticks and possible language hints (e.g. ```json)
        cleaned_text = re.sub(r"^```[\w]*\n?", "", raw_response_text)
        cleaned_text = re.sub(r"\n?```$", "", cleaned_text)

        # Use regex to extract JSON object (including multiline)
        json_match = re.search(r"\{.*\}", cleaned_text, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            try:
                parsed_messages = json.loads(json_string)
                return ChatResponse(**parsed_messages)
            except json.JSONDecodeError as e:
                logger.error(f"[CHATSERVICE] JSON decoding error: {e}. Extracted JSON string: {json_string}")
        else:
            logger.error("[CHATSERVICE] Could not find valid JSON in cleaned LLM response text.")

        # Return fallback ChatResponse if JSON extraction/parsing fails
        return ChatResponse(
            progress="(AI Overview - JSON parse failure)",
            improvement="(AI Improvement - JSON parse failure)",
            encouragement="(AI Encouragement - JSON parse failure)"
        )

    except Exception as e:
        logger.error(f"[CHATSERVICE] Error during Ollama interaction: {e}")
        return ChatResponse(
            progress="(AI Overview - connection error)",
            improvement="(AI Improvement - connection error)",
            encouragement="(AI Encouragement - connection error)"
        )
