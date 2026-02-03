import logging
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.relational.database import get_db, engine
from app.relational import models
from app.clients.vector_client import VectorClient

# Initialize DB tables
models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vector Client Instance
vector_client = VectorClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Relational container startup.")
    
    # Ensure collection exists
    vector_client.ensure_collection("foods")
    
    try:
        df = pd.read_csv("/app/food_data.csv")
        db = next(get_db())
        points = []
        
        for index, row in df.iterrows():
            # Check/Create in SQL
            existing = db.query(models.Food).filter(models.Food.name == row['name']).first()
            if not existing:
                food = models.Food(
                    name=row['name'],
                    calories_per_100g=row['calories'],
                    protein_per_100g=row['protein'],
                    carbs_per_100g=row['carbs'],
                    fat_per_100g=row['fat']
                )
                db.add(food)
                db.commit()
                db.refresh(food)
                food_id = food.id
            else:
                food_id = existing.id
            
            # Embed
            embedding = vector_client.embed(row['name'])
            if embedding:
                points.append({
                    "id": food_id,
                    "vector": embedding,
                    "payload": {
                        "food_name": row['name'],
                        "calories": row['calories'],
                        "protein": row['protein']
                    }
                })
        
        if points:
            success = vector_client.upsert(points)
            if success:
                logger.info(f"Seeded {len(points)} foods into Vector Service.")
            else:
                logger.error("Failed to upsert points to Vector Service.")
        
        db.close()
    except Exception as e:
        logger.error(f"Seeding failed: {e}")

    yield
    logger.info("Relational container shutdown.")

app = FastAPI(lifespan=lifespan)

# --- Schemas ---
class LogCreate(BaseModel):
    food_id: int
    grams: float

class LogUpdate(BaseModel):
    grams: float

class UserProfileUpdate(BaseModel):
    name: str
    height_cm: float
    weight_kg: float
    age: int
    sex: str
    goal: str
    calorie_target: float
    protein_target: float

class RetrievalRequest(BaseModel):
    menu_items: List[str]

# --- Endpoints ---

@app.post("/retrieve-context")
async def retrieve_context_endpoint(request: RetrievalRequest, db: Session = Depends(get_db)):
    logger.info(f"Retrieving context for {len(request.menu_items)} items.")
    results = []
    
    for item in request.menu_items:
        embedding = vector_client.embed(item)
        if not embedding:
            continue
            
        search_hits = vector_client.search(embedding, limit=3, score_threshold=0.6)
        
        context_list = []
        for hit in search_hits:
            payload = hit.get('payload', {})
            context_list.append({
                "food_name": payload.get("food_name"),
                "calories": payload.get("calories"),
                "protein": payload.get("protein")
            })
            
        results.append({
            "menu_item": item,
            "context": context_list
        })
        
    return results

@app.get("/foods/search")
async def search_foods(query: str, db: Session = Depends(get_db)):
    embedding = vector_client.embed(query)
    if not embedding:
        return []
    
    search_hits = vector_client.search(embedding, limit=20)
    
    ids = [hit['id'] for hit in search_hits]
    if not ids:
        return []
    
    foods = db.query(models.Food).filter(models.Food.id.in_(ids)).all()
    food_map = {f.id: f for f in foods}
    ordered_foods = [food_map[id] for id in ids if id in food_map]
    
    return ordered_foods

@app.get("/foods/{food_id}")
async def get_food_by_id(food_id: int, db: Session = Depends(get_db)):
    return db.query(models.Food).filter(models.Food.id == food_id).first()

@app.post("/logs")
async def add_food_log(log_data: LogCreate, db: Session = Depends(get_db)):
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

@app.put("/logs/{log_id}")
async def update_log(log_id: int, log_data: LogUpdate, db: Session = Depends(get_db)):
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

@app.delete("/logs/{log_id}")
async def delete_log(log_id: int, db: Session = Depends(get_db)):
    food_log = db.query(models.FoodLog).filter(models.FoodLog.id == log_id).first()
    if not food_log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(food_log)
    db.commit()
    return {"success": True}

@app.get("/logs/today")
async def get_today_logs(db: Session = Depends(get_db)):
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

@app.get("/logs/latest")
async def get_latest_log(db: Session = Depends(get_db)):
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

@app.get("/user/profile")
async def get_user_profile(db: Session = Depends(get_db)):
    return db.query(models.UserProfile).first()

@app.post("/user/profile")
async def set_user_profile(profile: UserProfileUpdate, db: Session = Depends(get_db)):
    p = db.query(models.UserProfile).filter(models.UserProfile.id == 1).first()
    if p:
        p.name = profile.name
        p.height_cm = profile.height_cm
        p.weight_kg = profile.weight_kg
        p.age = profile.age
        p.sex = models.SexEnum(profile.sex)
        p.goal = models.GoalEnum(profile.goal)
        p.calorie_target = profile.calorie_target
        p.protein_target = profile.protein_target
    else:
        p = models.UserProfile(
            id=1,
            name=profile.name,
            height_cm=profile.height_cm,
            weight_kg=profile.weight_kg,
            age=profile.age,
            sex=models.SexEnum(profile.sex),
            goal=models.GoalEnum(profile.goal),
            calorie_target=profile.calorie_target,
            protein_target=profile.protein_target
        )
        db.add(p)
    db.commit()
    db.refresh(p)
    return p

@app.delete("/user/profile")
async def delete_user_profile(db: Session = Depends(get_db)):
    p = db.query(models.UserProfile).filter(models.UserProfile.id == 1).first()
    if p:
        db.delete(p)
        db.commit()
        return {"success": True}
    return {"success": False}
