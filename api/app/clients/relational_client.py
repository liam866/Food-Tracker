import logging
import httpx
from typing import List, Optional, Any, Dict
from types import SimpleNamespace

from app.core.config import settings
from app.schemas.user import UserProfileCreate

logger = logging.getLogger(__name__)

class RelationalClient:
    def __init__(self):
        self.base_url = settings.RELATIONAL_SERVICE_URL
        self.client = httpx.Client(base_url=self.base_url, timeout=30.0)

    def _to_object(self, data: Any) -> Any:
        if isinstance(data, dict):
            return SimpleNamespace(**{k: self._to_object(v) for k, v in data.items()})
        elif isinstance(data, list):
            return [self._to_object(i) for i in data]
        return data

    def get_food_by_id(self, food_id: int) -> Optional[Any]:
        try:
            resp = self.client.get(f"/foods/{food_id}")
            if resp.status_code == 200 and resp.json():
                return self._to_object(resp.json())
        except Exception as e:
            logger.error(f"Error fetching food {food_id}: {e}")
        return None

    def search_foods(self, query: str) -> List[Any]:
        try:
            resp = self.client.get("/foods/search", params={"query": query})
            if resp.status_code == 200:
                return self._to_object(resp.json())
        except Exception as e:
            logger.error(f"Error searching foods: {e}")
        return []

    def add_food_log(self, food_id: int, grams: float) -> Optional[Any]:
        try:
            resp = self.client.post("/logs", json={"food_id": food_id, "grams": grams})
            if resp.status_code == 200:
                return self._to_object(resp.json())
        except Exception as e:
            logger.error(f"Error adding log: {e}")
        return None

    def update_food_log(self, log_id: int, grams: float) -> Optional[Any]:
        try:
            resp = self.client.put(f"/logs/{log_id}", json={"grams": grams})
            if resp.status_code == 200:
                return self._to_object(resp.json())
        except Exception as e:
            logger.error(f"Error updating log {log_id}: {e}")
        return None

    def delete_food_log(self, log_id: int) -> bool:
        try:
            resp = self.client.delete(f"/logs/{log_id}")
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"Error deleting log {log_id}: {e}")
            return False

    def get_today_food_logs(self) -> Dict[str, Any]:
        try:
            resp = self.client.get("/logs/today")
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.error(f"Error getting today logs: {e}")
            return {"logs": [], "totals": {}, "calorie_target": 0}

    def get_latest_food_log(self) -> Optional[List[Any]]:
        try:
            resp = self.client.get("/logs/latest")
            if resp.status_code == 200:
                data = resp.json()
                if not data: return None
                log_obj = self._to_object(data['log'])
                food_obj = self._to_object(data['food'])
                return [log_obj, food_obj]
        except Exception as e:
            logger.error(f"Error getting latest log: {e}")
        return None

    def get_user_profile(self) -> Optional[Any]:
        try:
            resp = self.client.get("/user/profile")
            if resp.status_code == 200 and resp.json():
                return self._to_object(resp.json())
        except Exception as e:
            logger.error(f"Error getting profile: {e}")
        return None

    def set_user_profile(self, profile_data: UserProfileCreate, calorie_target: float, protein_target: float) -> Any:
        try:
            payload = profile_data.model_dump()
            payload['calorie_target'] = calorie_target
            payload['protein_target'] = protein_target
            resp = self.client.post("/user/profile", json=payload)
            if resp.status_code == 200:
                return self._to_object(resp.json())
        except Exception as e:
            logger.error(f"Error setting profile: {e}")
        return None

    def delete_user_profile(self) -> bool:
        try:
            resp = self.client.delete("/user/profile")
            return resp.status_code == 200 and resp.json().get("success", False)
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            return False

    def retrieve_context(self, menu_items: List[str]) -> List[Any]:
        try:
            resp = self.client.post("/retrieve-context", json={"menu_items": menu_items})
            if resp.status_code == 200:
                return self._to_object(resp.json())
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
        return []

def get_relational_client() -> RelationalClient:
    return RelationalClient()
