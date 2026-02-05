import logging
from typing import List
from app.clients.vision_client import VisionClient
from app.clients.relational_client import RelationalClient
from app.clients.ollama_client import OllamaClient
from app.services.menu.prompt_builder import build_menu_prompt
from app.services.llm.ollama_handler import generate_response
from app.schemas.menu import MenuAnalysisResponse

logger = logging.getLogger(__name__)

async def analyze_menu(
    image_content: bytes,
    vision_client: VisionClient,
    db_client: RelationalClient,
    ollama_client: OllamaClient
) -> MenuAnalysisResponse:
    # 1. Vision Extraction
    logger.info("[MenuService] Step 1: Extracting menu items via Vision Service...")
    menu_items = await vision_client.extract_menu(image_content)
    
    if not menu_items:
        logger.warning("[MenuService] No menu items could be extracted from the image.")
        return MenuAnalysisResponse(recommendations=[])
    
    logger.info(f"[MenuService] Detected {len(menu_items)} menu items.")
    item_names = [item['name'] for item in menu_items]
    
    # 2. Semantic Retrieval
    logger.info("[MenuService] Step 2: Retrieving nutritional context from Database Service...")
    context_data = db_client.retrieve_context(item_names)
    logger.info(f"[MenuService] Retrieved context for {len(context_data)} items.")
    
    # 3. Fetch User State
    logger.info("[MenuService] Step 3: Fetching user profile and daily totals...")
    user_profile = db_client.get_user_profile()
    daily_logs_data = db_client.get_today_food_logs()
    daily_totals = daily_logs_data.get("totals", {})
    
    user_goals = {}
    if user_profile:
        goal_val = getattr(user_profile, 'goal', 'Maintain weight')
        if hasattr(goal_val, 'value'):
            goal_val = goal_val.value
            
        user_goals = {
            "calories": getattr(user_profile, 'calorie_target', 2000),
            "protein": getattr(user_profile, 'protein_target', 150),
            "goal": goal_val
        }
    
    # 4. Prompt Engineering
    logger.info("[MenuService] Step 4: Building grounded LLM prompt...")
    prompt = build_menu_prompt(user_goals, daily_totals, menu_items, context_data)
    
    # 5. LLM Reasoning
    logger.info("[MenuService] Step 5: Generating recommendations via Ollama...")
    parsed_response = await generate_response(prompt, ollama_client)
    
    if parsed_response and "recommendations" in parsed_response:
        try:
            # Map context to each recommendation
            for rec in parsed_response['recommendations']:
                matched_item = next((item for item in context_data if item.menu_item == rec['name']), None)
                if matched_item:
                    #Convert the context objects to dictionaries
                    rec['context'] = [
                        {
                            "food_name": getattr(c, 'food_name', ''),
                            "calories": getattr(c, 'calories', 0),
                            "protein": getattr(c, 'protein', 0),
                            # Add any other fields your FoodContext schema requires
                        } 
                        for c in matched_item.context
                    ]
                else:
                    rec['context'] = []
                    
            logger.info(f"[MenuService] Successfully generated {len(parsed_response['recommendations'])} recommendations with context.")
            return MenuAnalysisResponse(**parsed_response)
        except Exception as e:
            logger.error(f"[MenuService] Validation error on LLM response: {e}")
    
    logger.error("[MenuService] Failed to get structured recommendations from LLM.")
    return MenuAnalysisResponse(recommendations=[])
