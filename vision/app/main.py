import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True
)

logger = logging.getLogger(__name__)
# Ensure the 'app' namespace logs are captured at INFO level
logging.getLogger("app").setLevel(logging.INFO)

from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager
from app.core.models import model_manager
from app.core.preprocessing import preprocess_image
from app.core.layout import layout_detector
from app.schemas import MenuResponse, MenuItem


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models on startup
    try:
        model_manager.load_models()
    except Exception as e:
        logger.error(f"Startup failed: {e}")
    yield
    # Clean up if needed

app = FastAPI(title="Vision Service", lifespan=lifespan)

@app.get("/health")
async def health_check():
    """
    Simple minimal verification that models are active.
    """
    if model_manager.check_health():
        return {"status": "ok", "models": "active"}
    else:
        # In a real scenario this might be 503, but for now we report status
        return {"status": "error", "models": "inactive"}

@app.post("/extract-menu", response_model=MenuResponse)
async def extract_menu(image: UploadFile = File(...)):
    """
    Ingests a menu image and returns structured menu items.
    """
    try:
        # Read image bytes
        content = await image.read()
        
        # Preprocess the image (Milestone 2)
        # This verifies ingestion and preprocessing works deterministically
        processed_image = preprocess_image(content)
        
        # Layout Extraction (Milestone 3)
        # Detect bounding boxes for sections, items, descriptions, prices
        layout_items = layout_detector.detect(processed_image, model_manager)
        logger.info(f"Layout Extraction: Detected {len(layout_items)} items")
        
        # In future milestones: OCR -> Merge
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")

    return {
        "items": [
            {
                "section": "Mains",
                "name": "Grilled Chicken Salad",
                "description": "Mixed greens, lemon dressing",
                "price": 22
            }
        ]
    }
