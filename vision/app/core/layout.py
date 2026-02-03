import logging
import numpy as np
from typing import List, Optional, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ItemData(BaseModel):
    label: Optional[str] = None
    text: Optional[str] = None
    bbox: List[int]  # [x1, y1, x2, y2]

def polygon_to_bbox(polygon: np.ndarray, image_shape: tuple) -> Optional[List[int]]:
    """
    Converts a polygon (N points) to an axis-aligned bounding box [x1, y1, x2, y2].
    Ensures coordinates are within image bounds.
    """
    try:
        x_coords = polygon[:, 0]
        y_coords = polygon[:, 1]
        
        x1 = int(np.min(x_coords))
        y1 = int(np.min(y_coords))
        x2 = int(np.max(x_coords))
        y2 = int(np.max(y_coords))
        
        h, w = image_shape[:2]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        
        if x2 <= x1 or y2 <= y1:
            return None
            
        return [x1, y1, x2, y2]
    except Exception as e:
        logger.warning(f"Failed to convert polygon to bbox: {e}")
        return None

class LayoutDetector:
    def detect(self, image: np.ndarray, model_manager) -> List[ItemData]:
        """
        Runs PaddleOCR layout detection (det=True, rec=False).
        Returns ItemData with bbox populated.
        """
        logger.info(f"Running PaddleOCR Layout Detection on image shape: {image.shape}")
        
        items = []
        try:
            if not model_manager.detector:
                 logger.error("PaddleOCR detector not initialized.")
                 return []

            # Run PaddleOCR inference
            # result is typically a list of results (one per image passed)
            result = model_manager.detector.ocr(image, cls=True)
            
            # If no text detected, result might be [None] or empty list
            if not result or result[0] is None:
                logger.info("PaddleOCR detected no text regions.")
                return []

            boxes = result[0]
            logger.info(f"PaddleOCR detected {len(boxes)} raw regions.")

            for i, box_raw in enumerate(boxes):
                if i == 0:
                    logger.info(f"Sample box_raw type: {type(box_raw)}")
                    logger.info(f"Sample box_raw: {box_raw}")

                try:
                    # Handle case where box_raw is [coords, score] which causes shape (2,) error
                    if isinstance(box_raw, (list, tuple)) and len(box_raw) == 2:
                        # If first element looks like 4 points, take it
                        if isinstance(box_raw[0], (list, np.ndarray)) and len(box_raw[0]) == 4:
                            box_raw = box_raw[0]

                    # Convert raw box to numpy array
                    if isinstance(box_raw, list):
                        box = np.array(box_raw, dtype=np.float32)
                    elif isinstance(box_raw, np.ndarray):
                        box = box_raw.astype(np.float32)
                    else:
                        logger.warning(f"Skipping box {i} with unknown type: {type(box_raw)}")
                        continue
                    
                    # Validate shape (should be at least 3 points to form a region)
                    if box.ndim != 2 or box.shape[0] < 3 or box.shape[1] != 2:
                        logger.warning(f"Skipping box {i} with invalid shape: {box.shape}")
                        continue
                    
                    bbox = polygon_to_bbox(box, image.shape)
                    if bbox:
                        items.append(ItemData(label=None, text=None, bbox=bbox))
                    else:
                        logger.debug(f"Skipping invalid/empty bbox for box {i}")
                    
                except Exception as ex:
                    logger.warning(f"Error processing box {i}: {ex}")
                    continue
            
            logger.info(f"Layout Detection complete. Processed {len(items)} valid bounding boxes.")
            
        except Exception as e:
            logger.error(f"Layout detection critical failure: {e}")
            pass
            
        return items

layout_detector = LayoutDetector()
