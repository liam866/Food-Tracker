import logging
import pandas as pd
import asyncio
from sqlalchemy.orm import Session
from app.relational import models
from app.clients.vector_client import VectorClient

logger = logging.getLogger(__name__)

async def seed_data(db: Session, vector_client: VectorClient):
    try:
        logger.info("Checking vector service status...")
        count = await vector_client.count("foods")
        if count > 0:
            logger.info(f"Vector collection 'foods' already has {count} items. Seeding not required.")
            return

        logger.info(f"Vector collection is empty (count={count}). Starting seeding process...")
        
        try:
            df = pd.read_csv("/app/food_data.csv")
            logger.info(f"Loaded CSV with {len(df)} rows.")
        except Exception as e:
            logger.error(f"Failed to read CSV: {e}")
            return

        to_embed = []
        
        for index, row in df.iterrows():
            name = row['Description']
            calories = row['Data.Calories']
            protein = row['Data.Protein']
            carbs = row['Data.Carbohydrate']
            fat = row['Data.Fat.Total Lipid']
            
            existing = db.query(models.Food).filter(models.Food.name == name).first()
            if not existing:
                food = models.Food(
                    name=name,
                    calories_per_100g=calories,
                    protein_per_100g=protein,
                    carbs_per_100g=carbs,
                    fat_per_100g=fat
                )
                db.add(food)
                db.commit()
                db.refresh(food)
                food_id = food.id
            else:
                food_id = existing.id
            
            to_embed.append({
                "id": food_id,
                "text": name,
                "payload": {
                    "food_name": name,
                    "calories": calories,
                    "protein": protein
                }
            })
        
        logger.info(f"Prepared {len(to_embed)} items for embedding.")
        
        sem = asyncio.Semaphore(500) 
        
        async def process_item(item):
            async with sem:
                vec = await vector_client.embed(item['text'])
                if vec:
                    return {
                        "id": item['id'],
                        "vector": vec,
                        "payload": item['payload']
                    }
                return None

        tasks = [process_item(item) for item in to_embed]
        results = await asyncio.gather(*tasks)
        
        valid_points = [p for p in results if p]
        
        if valid_points:
            chunk_size = 500
            for i in range(0, len(valid_points), chunk_size):
                chunk = valid_points[i:i+chunk_size]
                success = await vector_client.upsert(chunk)
                if not success:
                    logger.error(f"Failed to upsert chunk {i}")
            
            logger.info(f"Seeded {len(valid_points)} foods into Vector Service.")
        else:
            logger.warning("No valid embeddings generated.")
            
    except Exception as e:
        logger.error(f"Seeding failed: {e}")
