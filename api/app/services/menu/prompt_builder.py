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
1. ESTIMATE: Look at the item name. How much does a "Dinner" or "Soup" usually weigh? (e.g., 350g-500g for a main). 
2. CALCULATE: (Weight / 100) * (Calories per 100g). Do NOT just report the 100g number!
3. VERIFY: Does this specific meal actually help them reach their protein goal?

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
      "reasoning": "You're crushing your goals! I've estimated this at a hearty 400g serving, giving you about X total protein to really fuel your muscles. It fits your remaining calories perfectly—enjoy every bite!"
    }
  ]
}
"""
    return prompt