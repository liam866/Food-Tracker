import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.clients.relational_client import RelationalClient

def search_foods_service(db_client: "RelationalClient", query: str):
    return db_client.search_foods(query)

def get_food_by_id_service(db_client: "RelationalClient", food_id: int):
    return db_client.get_food_by_id(food_id)
