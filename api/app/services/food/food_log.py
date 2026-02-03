import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.clients.relational_client import RelationalClient

def add_food_log_service(db_client: "RelationalClient", food_id: int, grams: float):
    return db_client.add_food_log(food_id, grams)

def update_food_log_service(db_client: "RelationalClient", log_id: int, grams: float):
    return db_client.update_food_log(log_id, grams)

def delete_food_log_service(db_client: "RelationalClient", log_id: int):
    return db_client.delete_food_log(log_id)

def get_today_food_logs_service(db_client: "RelationalClient"):
    return db_client.get_today_food_logs()
