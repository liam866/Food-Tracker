import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def build_menu_prompt(
    user_goals: Dict[str, float],
    daily_totals: Dict[str, float],
    menu_items: List[Dict[str, Any]],
    context_data: List[Dict[str, Any]]
) -> str:
    remaining_cals = user_goals.get("calories", 2000) - daily_totals.get("calories", 0)
    remaining_protein = user_goals.get("protein", 150) - daily_totals.get("protein", 0)

    prompt = f"""
You are a friendly, practical nutrition expert helping a user choose a meal from a restaurant menu.

USER CONTEXT:
- Remaining calories today: {remaining_cals:.0f} kcal
- Remaining protein today: {remaining_protein:.0f} g

MENU ITEMS AND VERIFIED NUTRITIONAL CONTEXT:
"""

    for item in context_data:
        name = getattr(item, "menu_item", "Unknown Item")
        ctx_list = getattr(item, "context", [])

        prompt += f"\n{name}:\n"
        if ctx_list:
            for ctx in ctx_list:
                food_name = getattr(ctx, "food_name", "Unknown Food")
                calories = getattr(ctx, "calories", 0)
                protein = getattr(ctx, "protein", 0)
                prompt += f"- {food_name}: {calories} kcal, {protein} g protein\n"
        else:
            prompt += "- No verified nutritional data available\n"

    prompt += """
TASK:
Select the TOP 3 menu items that best fit the user's remaining daily goals.

RULES (VERY IMPORTANT):
- Use ONLY the nutrition data explicitly provided above.
- Do NOT estimate, guess, or infer missing calories or protein.
- If an item lacks nutrition data, you may still recommend it, but you MUST clearly mention the lack of data.
- Keep reasoning concise, specific, and helpful (ONE sentence per item).
- Do NOT repeat the user's goals in the explanation.
- Do NOT include emojis, markdown, or extra commentary.

OUTPUT FORMAT (STRICT):
Return ONLY valid JSON.
Do NOT include backticks, markdown, or explanatory text.
If you cannot complete all 3 items, return only the ones you can complete fully.

{
  "recommendations": [
    {
      "name": "Exact Menu Item Name",
      "reasoning": "One concise sentence explaining why this item fits the user's remaining budget and goals, referencing the provided data."
    }
  ]
}
"""
    return prompt
