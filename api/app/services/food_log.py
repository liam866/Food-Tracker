import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models import FoodLog, Food, UserProfile

def add_food_log_service(db: Session, food_id: int, grams: float):
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        return None

    logging.info(f"Logging {grams}g of food: {food.name} (Food ID: {food_id})")

    calories = (food.calories_per_100g / 100) * grams
    protein = (food.protein_per_100g / 100) * grams
    carbs = (food.carbs_per_100g / 100) * grams
    fat = (food.fat_per_100g / 100) * grams

    food_log = FoodLog(
        food_id=food_id,
        grams=grams,
        calories=calories,
        protein=protein,
        carbs=carbs,
        fat=fat,
    )
    db.add(food_log)
    db.commit()
    db.refresh(food_log)
    return food_log

def update_food_log_service(db: Session, log_id: int, grams: float):
    food_log = db.query(FoodLog).filter(FoodLog.id == log_id).first()
    if not food_log:
        return None

    food = db.query(Food).filter(Food.id == food_log.food_id).first()
    if not food:
        return None # Should not happen if data integrity is maintained

    food_log.grams = grams
    food_log.calories = (food.calories_per_100g / 100) * grams
    food_log.protein = (food.protein_per_100g / 100) * grams
    food_log.carbs = (food.carbs_per_100g / 100) * grams
    food_log.fat = (food.fat_per_100g / 100) * grams

    db.commit()
    db.refresh(food_log)
    return food_log

def delete_food_log_service(db: Session, log_id: int):
    food_log = db.query(FoodLog).filter(FoodLog.id == log_id).first()
    if not food_log:
        return False
    db.delete(food_log)
    db.commit()
    return True

def get_today_food_logs_service(db: Session):
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    logs = db.query(FoodLog, Food).filter(
        FoodLog.food_id == Food.id,
        FoodLog.datetime >= start_of_day,
        FoodLog.datetime <= end_of_day
    ).all()

    total_calories = sum(log.FoodLog.calories for log in logs)
    total_protein = sum(log.FoodLog.protein for log in logs)
    total_carbs = sum(log.FoodLog.carbs for log in logs)
    total_fat = sum(log.FoodLog.fat for log in logs)

    user_profile = db.query(UserProfile).filter(UserProfile.id == 1).first()
    calorie_target = user_profile.calorie_target if user_profile else 0

    return {
        "logs": logs,
        "totals": {
            "calories": total_calories,
            "protein": total_protein,
            "carbs": total_carbs,
            "fat": total_fat,
        },
        "calorie_target": calorie_target
    }
