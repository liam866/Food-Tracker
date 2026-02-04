import logging
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Request

from app.schemas.menu import MenuAnalysisResponse
from app.clients.vision_client import VisionClient, get_vision_client
from app.clients.relational_client import RelationalClient, get_relational_client
from app.clients.ollama_client import OllamaClient
from app.services.menu.menu_service import analyze_menu

router = APIRouter()
logger = logging.getLogger(__name__)

def get_ollama_client(request: Request) -> OllamaClient:
    return request.app.state.ollama_client

@router.post("/menu/analyze", response_model=MenuAnalysisResponse)
async def analyze_menu_endpoint(
    image: UploadFile = File(...),
    vision_client: VisionClient = Depends(get_vision_client),
    db_client: RelationalClient = Depends(get_relational_client),
    ollama_client: OllamaClient = Depends(get_ollama_client)
):
    logger.info(f"[MenuRoute] Received analysis request for file: {image.filename}")
    try:
        content = await image.read()
        response = await analyze_menu(content, vision_client, db_client, ollama_client)
        logger.info("[MenuRoute] Successfully generated menu analysis.")
        return response
    except Exception as e:
        logger.error(f"[MenuRoute] Error during menu analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze menu")
