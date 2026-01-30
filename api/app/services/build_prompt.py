import logging
from typing import Optional, Tuple

from app.db.models import FoodLog, Food 

logger = logging.getLogger(__name__)

def build_chat_prompt(latest_food_log: Optional[Tuple[FoodLog, Food]]) -> str:
    logger.info("[PromptBuilder] Building chat prompt...")
    prompt_parts = []

    if latest_food_log:
        log_entry, food_item = latest_food_log
        prompt_parts.append(f"Most recently eaten food: {food_item.name}, Protein: {log_entry.protein}g.")
    else:
        prompt_parts.append("No food logs available.")

    prompt_parts.append("You are a supportive, upbeat food coach who gives specific, energising, concise advice. Based on the given food above, provide three short, encouraging sentences in the following format (you must give one short sentence only for each):")
    prompt_parts.append("1. Progress: Say something positive about the nutrition of the food stated above.")
    prompt_parts.append("2. Improvement: Suggest an actionable improvement for the client's health, such as eating more vegetables for nutrients or staying hydrated.)")
    prompt_parts.append("3. Encouragement: Empower the user to keep eating healthy - they need a bit of support.)")
    prompt_parts.append("Your response MUST be in JSON format with keys: progress, improvement, encouragement.")

    final_prompt = "\n".join(prompt_parts)
    logger.info(f"[PromptBuilder] Final prompt generated:\n{final_prompt}")
    return final_prompt
