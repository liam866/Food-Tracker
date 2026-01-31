import logging
import json
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import UserProfile, FoodLog, Food
from app.services.build_prompt import build_chat_prompt
from app.services.chat_handler import send_to_ollama
from app.schemas.chat import ChatResponse
from app.clients.ollama_client import OllamaClient 

router = APIRouter()
logger = logging.getLogger(__name__)

def get_ollama_client(request: Request) -> OllamaClient:
    return request.app.state.ollama_client

@router.post("/chat", response_model=ChatResponse)
async def get_chat_response(db: Session = Depends(get_db), ollama_client: OllamaClient = Depends(get_ollama_client)):
    logger.info("[ChatRoute] Received request for AI overview.")
   
    latest_food_log = db.query(FoodLog, Food).join(Food, FoodLog.food_id == Food.id).order_by(FoodLog.datetime.desc()).first()
    logger.info(f"[ChatRoute] Fetched latest food log: {latest_food_log[0].id if latest_food_log else None}")

    prompt = build_chat_prompt(latest_food_log)

    try:
        llm_response = await send_to_ollama(prompt, ollama_client) # Pass the client here
        logger.info(f"[ChatRoute] Successfully received LLM response.")
        return llm_response
    except Exception as e:
        logger.error(f"[ChatRoute] Error getting response from LLM: {e}")
        raise HTTPException(status_code=500, detail="Failed to get AI overview")
