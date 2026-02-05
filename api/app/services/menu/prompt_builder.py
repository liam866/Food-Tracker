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
You are a high-energy, encouraging, and clever nutrition coach! Your goal is to make the user feel confident and excited about their meal choice while being mathematically precise.

USER'S VIBE:
- Calories remaining: {remaining_cals:.0f} kcal
- Protein remaining: {remaining_protein:.0f} g

NUTRITIONAL DATA (WARNING: These values are PER 100g. You MUST multiply these by a realistic portion weight!):
"""

    for item in context_data:
        name = getattr(item, "menu_item", "Unknown Item")
        ctx_list = getattr(item, "context", [])
        prompt += f"\n[{name}]\n"
        if ctx_list:
            for ctx in ctx_list:
                food_name = getattr(ctx, "food_name", "Unknown Food")
                prompt += f"- {food_name}: {getattr(ctx, 'calories', 0)} kcal/100g, {getattr(ctx, 'protein', 0)}g protein/100g\n"
        else:
            prompt += "- No data available (Use your best coaching intuition!)\n"

    prompt += """
CRITICAL STEP-BY-STEP LOGIC:
1. ESTIMATE: Use your knowledge of common portion sizes and ingredients to make an educated guess about the weight of the meal and its composition. Be as specific as possible in your reasoning (e.g., "This looks like a standard burger, which typically weighs around 150g, so I will calculate based on that").
2. VERIFY: Does this specific meal actually help them reach their protein goal?

COACHING STYLE REQUIREMENTS:
- BE VARIED: Do NOT use the same sentence structure for different items. 
- BE INTERPERSONAL: Use phrases like "You're going to love this," "This is a powerhouse pick," or "A perfect fit for your day!"
- BE SPECIFIC: Mention a specific ingredient or the estimated weight in each reasoning.
- DO NOT use the same phrase more than once.

OUTPUT FORMAT (STRICT JSON):
{
  "recommendations": [
    {
      "name": "Exact Menu Item Name",
      "reasoning": "Encouraging, specific, and unique reasoning for this item based on it's specific nutritional data.",
    }
  ]
}
"""
    return prompt