from app.db.models import SexEnum, GoalEnum

def calculate_calorie_target(height_cm: float, weight_kg: float, age: int, sex: SexEnum, goal: GoalEnum) -> float:
    # Mifflin-St Jeor Equation for BMR
    if sex == SexEnum.male:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Sedentary (little to no exercise) TDEE multiplier
    tdee = bmr * 1.2

    # Apply goal adjustments
    if goal == GoalEnum.lose_fat:
        tdee -= 500
    elif goal == GoalEnum.build_muscle:
        tdee += 300

    return round(tdee)

def calculate_protein_target(weight_kg: float) -> float:
    """
    Calculates the recommended daily protein intake.
    """
    return round(weight_kg * 2.25)
