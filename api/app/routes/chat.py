import logging
from fastapi import APIRouter, Depends, HTTPException, Request

# from sqlalchemy.orm import Session # Remove

from app.schemas.chat import ChatOverviewResponse
from app.clients.ollama_client import OllamaClient 
from app.clients.relational_client import RelationalClient, get_relational_client
from app.services.chat.chat_service import get_chat_overview

router = APIRouter()
logger = logging.getLogger(__name__)

def get_ollama_client(request: Request) -> OllamaClient:
    return request.app.state.ollama_client

@router.post("/chat", response_model=ChatOverviewResponse)
async def get_chat_response(db_client: RelationalClient = Depends(get_relational_client), ollama_client: OllamaClient = Depends(get_ollama_client)):
    logger.info("[ChatRoute] Received request for AI overview.")
    
    try:
        response = await get_chat_overview(db_client, ollama_client)
        logger.info(f"[ChatRoute] Successfully received AI overview.")
        return response
    except Exception as e:
        logger.error(f"[ChatRoute] Error in chat service: {e}")
        raise HTTPException(status_code=500, detail="Failed to get AI overview")
