import logging
import csv
from sqlalchemy.orm import Session

from app.db.models import Base, Food
from app.db.database import engine

logger = logging.getLogger(__name__)

def create_db_and_tables():
    logger.info("Creating database and tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database and tables created.")

def ingest_food_data(db: Session):
    logger.info("Checking if food data needs ingestion...")

    if db.query(Food).count() != 0:
        logger.info("Foods table is not empty, skipping ingestion.")
        return

    logger.info("Foods table is empty, ingesting data from food_data.csv...")

    try:
        foods_to_ingest = []

        with open("food_data.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                food = Food(
                    name=row["Description"],
                    calories_per_100g=float(row["Data.Calories"]),
                    protein_per_100g=float(row["Data.Protein"]),
                    carbs_per_100g=float(row["Data.Carbohydrate"]),
                    fat_per_100g=float(row["Data.Fat.Total Lipid"]),
                )
                foods_to_ingest.append(food)

        db.bulk_save_objects(foods_to_ingest)
        db.commit()

        logger.info(f"Successfully ingested {len(foods_to_ingest)} foods.")

    except Exception as e:
        logger.error(f"Error ingesting food data: {e}")
        db.rollback()
