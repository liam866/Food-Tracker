import logging
from app.db.models import SexEnum, GoalEnum

logger = logging.getLogger(__name__)

def calculate_calorie_target(height_cm: float, weight_kg: float, age: int, sex: SexEnum, goal: GoalEnum) -> float:
    logger.info(f"[Backend] calculate_calorie_target: Input: height={height_cm}cm, weight={weight_kg}kg, age={age}, sex={sex.value}, goal={goal.value}")
    # Mifflin-St Jeor Equation for BMR
    if sex == SexEnum.male:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    logger.info(f"[Backend] calculate_calorie_target: BMR = {bmr:.2f}")

    # Sedentary (little to no exercise) TDEE multiplier
    tdee = bmr * 1.2
    logger.info(f"[Backend] calculate_calorie_target: TDEE (sedentary) = {tdee:.2f}")

    # Apply goal adjustments
    if goal.value == GoalEnum.lose_fat.value:
        tdee -= 500
        logger.info(f"[Backend] calculate_calorie_target: Applying lose_fat adjustment (-500 kcal). New TDEE = {tdee:.2f}")
    elif goal.value == GoalEnum.build_muscle.value:
        tdee += 300
        logger.info(f"[Backend] calculate_calorie_target: Applying build_muscle adjustment (+300 kcal). New TDEE = {tdee:.2f}")
    else:
        logger.info(f"[Backend] calculate_calorie_target: No adjustment for goal: {goal.value}. TDEE remains {tdee:.2f}")

    rounded_tdee = round(tdee)
    logger.info(f"[Backend] calculate_calorie_target: Final rounded calorie target = {rounded_tdee}")
    return rounded_tdee

def calculate_protein_target(weight_kg: float) -> float:
    """
    Calculates the recommended daily protein intake.
    """
    protein_target = round(weight_kg * 2.25)
    logger.info(f"[Backend] calculate_protein_target: Input: weight={weight_kg}kg. Calculated protein target = {protein_target}g")
    return protein_target
