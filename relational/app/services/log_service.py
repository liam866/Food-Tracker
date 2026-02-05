from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.relational import models
from app.schemas.internal import LogCreate, LogUpdate
from datetime import datetime, timezone

def add_food_log(log_data: LogCreate, db: Session):
    food = db.query(models.Food).filter(models.Food.id == log_data.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
        
    calories = (food.calories_per_100g / 100) * log_data.grams
    protein = (food.protein_per_100g / 100) * log_data.grams
    carbs = (food.carbs_per_100g / 100) * log_data.grams
    fat = (food.fat_per_100g / 100) * log_data.grams

    food_log = models.FoodLog(
        food_id=log_data.food_id,
        grams=log_data.grams,
        calories=calories,
        protein=protein,
        carbs=carbs,
        fat=fat,
    )
    db.add(food_log)
    db.commit()
    db.refresh(food_log)
    return food_log

def update_log(log_id: int, log_data: LogUpdate, db: Session):
    food_log = db.query(models.FoodLog).filter(models.FoodLog.id == log_id).first()
    if not food_log:
        raise HTTPException(status_code=404, detail="Log not found")
        
    food = db.query(models.Food).filter(models.Food.id == food_log.food_id).first()
    
    food_log.grams = log_data.grams
    if food:
        food_log.calories = (food.calories_per_100g / 100) * log_data.grams
        food_log.protein = (food.protein_per_100g / 100) * log_data.grams
        food_log.carbs = (food.carbs_per_100g / 100) * log_data.grams
        food_log.fat = (food.fat_per_100g / 100) * log_data.grams
        
    db.commit()
    db.refresh(food_log)
    return food_log

def delete_log(log_id: int, db: Session):
    food_log = db.query(models.FoodLog).filter(models.FoodLog.id == log_id).first()
    if not food_log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(food_log)
    db.commit()
    return {"success": True}

def get_today_logs(db: Session):
    today = datetime.now().date()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())
    
    logs = db.query(models.FoodLog, models.Food).filter(
        models.FoodLog.food_id == models.Food.id,
        models.FoodLog.datetime >= start,
        models.FoodLog.datetime <= end
    ).order_by(models.FoodLog.datetime.desc()).all()
    
    serialized_logs = []
    total_cal = 0
    total_prot = 0
    total_carbs = 0
    total_fat = 0
    
    for log, food in logs:
        total_cal += log.calories
        total_prot += log.protein
        total_carbs += log.carbs
        total_fat += log.fat
        
        serialized_logs.append({
            "id": log.id,
            "food_id": log.food_id,
            "grams": log.grams,
            "calories": log.calories,
            "protein": log.protein,
            "carbs": log.carbs,
            "fat": log.fat,
            "datetime": log.datetime.isoformat(),
            "food_name": food.name
        })
        
    user_profile = db.query(models.UserProfile).first()
    target = user_profile.calorie_target if user_profile else 0
    
    return {
        "logs": serialized_logs,
        "totals": {
            "calories": total_cal,
            "protein": total_prot,
            "carbs": total_carbs,
            "fat": total_fat
        },
        "calorie_target": target
    }

def get_latest_log(db: Session):
    result = db.query(models.FoodLog, models.Food).join(models.Food, models.FoodLog.food_id == models.Food.id).order_by(models.FoodLog.datetime.desc()).first()
    if not result:
        return None
    log, food = result
    return {
        "log": {
            "id": log.id,
            "food_id": log.food_id,
            "grams": log.grams,
            "protein": log.protein,
            "datetime": log.datetime.isoformat()
        },
        "food": {
            "id": food.id,
            "name": food.name
        }
    }
