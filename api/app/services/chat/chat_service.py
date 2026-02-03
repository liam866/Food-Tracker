import logging
from typing import TYPE_CHECKING

from app.schemas.chat import ChatOverviewResponse
from app.services.chat.prompt_builder import build_chat_prompt
from app.services.llm.ollama_handler import generate_response

if TYPE_CHECKING:
    from app.clients.ollama_client import OllamaClient
    from app.clients.relational_client import RelationalClient

logger = logging.getLogger(__name__)

async def get_chat_overview(db_client: "RelationalClient", ollama_client: "OllamaClient") -> ChatOverviewResponse:
    logger.info("[ChatService] Orchestrating AI overview...")

    # 1. Fetch latest food log
    latest_food_log = db_client.get_latest_food_log()
    
    if latest_food_log:
         logger.info(f"[ChatService] Fetched latest food log: {latest_food_log[0].id}")
    else:
         logger.info(f"[ChatService] No food logs found.")

    # 2. Build prompt
    prompt = build_chat_prompt(latest_food_log)

    # 3. Call LLM Handler
    parsed_response = await generate_response(prompt, ollama_client)

    # 4. Handle response / fallback
    if parsed_response:
        try:
            return ChatOverviewResponse(**parsed_response)
        except Exception as e:
            logger.error(f"[ChatService] Failed to map response to schema: {e}")
    
    # Fallback
    return ChatOverviewResponse(
        progress="(AI Overview - unavailable)",
        improvement="(AI Improvement - unavailable)",
        encouragement="(AI Encouragement - unavailable)"
    )
