import logging
import json
from typing import TYPE_CHECKING # For type hinting without circular imports

from api.app.schemas.chat import ChatResponse
from app.schemas.ollama import OllamaGenerateRequest
from app.core.config import settings

# Conditional import for type hinting only
if TYPE_CHECKING:
    from app.services.ollama_wrapper import OllamaClient 

logger = logging.getLogger(__name__)

async def send_to_ollama(prompt: str, ollama_client: "OllamaClient") -> ChatResponse:
    logger.info("[LLMClient] Orchestrating prompt to Ollama...")
    
    try:
        ollama_request = OllamaGenerateRequest(
            model=settings.OLLAMA_MODEL, # Use model from settings
            prompt=prompt,
            stream=False,
            options={
                "temperature": 0.7,
                "num_predict": 128,
            }
        )

        ollama_raw_response = await ollama_client.generate(ollama_request)
        logger.info(f"[LLMClient] Raw response from Ollama wrapper: {ollama_raw_response.response}")

        llm_text_response = ollama_raw_response.response.strip()

        try:
            json_start = llm_text_response.find("{")
            json_end = llm_text_response.rfind("}")
            if json_start != -1 and json_end != -1 and json_start < json_end:
                json_string = llm_text_response[json_start : json_end + 1]
                parsed_messages = json.loads(json_string)
                return ChatResponse(**parsed_messages)
            else:
                logger.error("[LLMClient] Could not find valid JSON in LLM response text.")
                return ChatResponse(
                    progress="(AI Overview - no valid JSON)",
                    improvement="(AI Improvement - no valid JSON)",
                    encouragement="(AI Encouragement - no valid JSON)"
                )
        except json.JSONDecodeError as e:
            logger.error(f"[LLMClient] JSON decoding error: {e}. Raw LLM text: {llm_text_response}")
            return ChatResponse(
                progress="(AI Overview - JSON error)",
                improvement="(AI Improvement - JSON error)",
                encouragement="(AI Encouragement - JSON error)"
            )
    except Exception as e:
        logger.error(f"[LLMClient] Error during Ollama interaction: {e}")
        return ChatResponse(
            progress="(AI Overview - connection error)",
            improvement="(AI Improvement - connection error)",
            encouragement="(AI Encouragement - connection error)"
        )
