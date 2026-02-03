import logging
from fastapi import APIRouter, Depends, HTTPException

from app.clients.relational_client import RelationalClient, get_relational_client
from app.services.food.food_log import (
    add_food_log_service,
    update_food_log_service,
    delete_food_log_service,
    get_today_food_logs_service,
)
from app.schemas.log import (
    FoodLogCreate,
    FoodLogUpdate,
    FoodLoggedSchema,
    DailyLogSummary,
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/log/add", response_model=FoodLoggedSchema)
async def add_food_to_log(log_item: FoodLogCreate, db_client: RelationalClient = Depends(get_relational_client)):
    logger.info(f"Attempting to log {log_item.grams}g of food ID {log_item.food_id}.")
    food_log = add_food_log_service(db_client, log_item.food_id, log_item.grams)
    if not food_log:
        logger.error(f"Failed to log food: Food ID {log_item.food_id} not found.")
        raise HTTPException(status_code=404, detail="Food not found")

    food = db_client.get_food_by_id(food_log.food_id)
    if food:
        food_log.name = food.name
    
    logger.info(f"Successfully logged food: Log ID {food_log.id}, Food Name '{food.name if food else 'Unknown'}'.")
    return food_log


@router.put("/log/{log_id}", response_model=FoodLoggedSchema)
async def update_food_in_log(
    log_id: int, log_update: FoodLogUpdate, db_client: RelationalClient = Depends(get_relational_client)
):
    logger.info(f"Attempting to update log ID {log_id} to {log_update.grams}g.")
    food_log = update_food_log_service(db_client, log_id, log_update.grams)
    if not food_log:
        logger.error(f"Failed to update log: Log ID {log_id} not found.")
        raise HTTPException(status_code=404, detail="Log entry not found")

    food = db_client.get_food_by_id(food_log.food_id)
    if food:
        food_log.name = food.name

    logger.info(f"Successfully updated log ID {log_id}.")
    return food_log


@router.delete("/log/{log_id}")
async def delete_food_from_log(log_id: int, db_client: RelationalClient = Depends(get_relational_client)):
    logger.info(f"Attempting to delete log ID {log_id}.")
    if not delete_food_log_service(db_client, log_id):
        logger.error(f"Failed to delete log: Log ID {log_id} not found.")
        raise HTTPException(status_code=404, detail="Log entry not found")
    logger.info(f"Successfully deleted log ID {log_id}.")
    return {"message": "Log entry deleted"}


@router.get("/log/today", response_model=DailyLogSummary)
async def get_today_logs(db_client: RelationalClient = Depends(get_relational_client)):
    logger.info("Fetching today's food logs.")
    result = get_today_food_logs_service(db_client)
    logger.info(f"Found {len(result['logs'])} log entries for today.")

    logs_with_names = [
        FoodLoggedSchema(
            id=log['id'],
            food_id=log['food_id'],
            grams=log['grams'],
            calories=log['calories'],
            protein=log['protein'],
            carbs=log['carbs'],
            fat=log['fat'],
            datetime=log['datetime'],
            name=log['food_name'],
        )
        for log in result["logs"]
    ]

    return {
        "logs": logs_with_names,
        "totals": result["totals"],
        "calorie_target": result["calorie_target"],
    }
