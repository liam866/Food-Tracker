import logging
import pandas as pd
import asyncio
from sqlalchemy.orm import Session
from app.relational import models
from app.clients.vector_client import VectorClient

logger = logging.getLogger(__name__)

async def seed_data(db: Session, vector_client: VectorClient):
    try:
        # 1. Check if vector service has data
        count = await vector_client.count("foods")
        if count > 0:
            logger.info(f"Vector collection has {count} items. Skipping seeding.")
            return

        logger.info("Seeding data...")
        # 2. Read CSV
        try:
            df = pd.read_csv("/app/food_data.csv")
        except Exception as e:
            logger.error(f"Failed to read CSV: {e}")
            return

        # 3. Process
        to_embed = []
        
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
            
            to_embed.append({
                "id": food_id,
                "text": row['name'],
                "payload": {
                    "food_name": row['name'],
                    "calories": row['calories'],
                    "protein": row['protein']
                }
            })
        
        logger.info(f"Prepared {len(to_embed)} items for embedding.")
        
        # 4. Parallel Embedding
        sem = asyncio.Semaphore(10) 
        
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
            # Upsert in chunks
            chunk_size = 100
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
