import logging
from typing import List, Dict, Any
from app.clients.vector_client import VectorClient

logger = logging.getLogger(__name__)
vector_client = VectorClient()

async def retrieve_context(menu_items: List[str]) -> List[Dict[str, Any]]:
    logger.info(f"Retrieving context for {len(menu_items)} items.")
    results = []
    
    for item in menu_items:
        embedding = await vector_client.embed(item)
        if not embedding:
            continue
            
        search_hits = await vector_client.search(embedding, limit=3, score_threshold=0.6)
        
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
