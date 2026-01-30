import logging
from typing import Optional, Tuple

from app.db.models import FoodLog, Food # Removed UserProfile

logger = logging.getLogger(__name__)

def build_chat_prompt(latest_food_log: Optional[Tuple[FoodLog, Food]]) -> str:
    logger.info("[PromptBuilder] Building chat prompt...")
    prompt_parts = []

    if latest_food_log:
        log_entry, food_item = latest_food_log
        prompt_parts.append(f"Most recently eaten Food Log: Food: {food_item.name}, Grams: {log_entry.grams}g, Calories: {log_entry.calories} kcal, Protein: {log_entry.protein}g.")
    else:
        prompt_parts.append("No food logs available.")

    prompt_parts.append("You are a supportive, fun food coach. Based on the above food log, provide three short, encouraging messages in the following format:")
    prompt_parts.append("1. Progress: Provide positive praise about the client's most recent food log. They're working hard on their nutrition!")
    prompt_parts.append("2. Improvement: Suggest an actionable improvement for the client to be healthy, such as eating more vegetables for nutrients or staying hydrated.)")
    prompt_parts.append("3. Ecouragement: Encourage the user to keep up the good effort. Provide a  supportive, energising statement with some humor.)")
    prompt_parts.append("Ensure your response is in JSON format with keys: progress, improvement, encouragement.")

    final_prompt = "\n".join(prompt_parts)
    logger.info(f"[PromptBuilder] Final prompt generated:\n{final_prompt}")
    return final_prompt
