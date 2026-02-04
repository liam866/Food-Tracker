from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.relational.database import get_db
from app.schemas.internal import LogCreate, LogUpdate
from app.services.log_service import (
    add_food_log,
    update_log,
    delete_log,
    get_today_logs,
    get_latest_log
)

router = APIRouter()

@router.post("/logs")
async def add_food_log_endpoint(log_data: LogCreate, db: Session = Depends(get_db)):
    return add_food_log(log_data, db)

@router.put("/logs/{log_id}")
async def update_log_endpoint(log_id: int, log_data: LogUpdate, db: Session = Depends(get_db)):
    return update_log(log_id, log_data, db)

@router.delete("/logs/{log_id}")
async def delete_log_endpoint(log_id: int, db: Session = Depends(get_db)):
    return delete_log(log_id, db)

@router.get("/logs/today")
async def get_today_logs_endpoint(db: Session = Depends(get_db)):
    return get_today_logs(db)

@router.get("/logs/latest")
async def get_latest_log_endpoint(db: Session = Depends(get_db)):
    return get_latest_log(db)
