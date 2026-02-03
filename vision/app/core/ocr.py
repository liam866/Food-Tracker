import logging
import numpy as np
import cv2
from typing import List
from app.core.layout import ItemData

logger = logging.getLogger(__name__)

class OCRProcessor:
    def recognize(self, image: np.ndarray, items: List[ItemData], model_manager) -> List[ItemData]:
        """
        Takes the full image and a list of ItemData (with bboxes).
        Crops the image for each item and runs OCR recognition.
        Updates item.text.
        """
        logger.info(f"Running OCR on {len(items)} items...")
        
        if not model_manager.recognizer:
            logger.error("OCR recognizer not initialized.")
            return items

        count = 0
        for i, item in enumerate(items):
            try:
                x1, y1, x2, y2 = item.bbox
                
                # Validate bbox against image dimensions
                h, w = image.shape[:2]
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(w, x2)
                y2 = min(h, y2)
                
                if x2 <= x1 or y2 <= y1:
                    # logger.warning(f"Invalid crop for item {i}: {item.bbox}")
                    continue
                
                # Crop
                crop = image[y1:y2, x1:x2]
                
                if crop.size == 0:
                    continue

                # Run Recognition
                # det=False means treat the input image (crop) as a single text line/region
                # cls=True enables angle classification (upright adjustment)
                # result format for single image with det=False is usually: [(text, score)]
                # Note: PaddleOCR.ocr returns a list of results.
                result = model_manager.recognizer.ocr(crop, cls=True, det=False)
                
                text = ""
                if result:
                    # Handle potential list wrapping
                    # Standard output: [('text', 0.99), ...]
                    # Sometimes wrapped in list if batch?
                    
                    for res in result:
                        if isinstance(res, tuple):
                            # (text, score)
                            text += res[0] + " "
                        elif isinstance(res, list):
                            # [[(text, score)]] case?
                            for sub_res in res:
                                if isinstance(sub_res, tuple):
                                    text += sub_res[0] + " "
                    
                    text = text.strip()

                item.text = text
                if text:
                    count += 1
                # logger.debug(f"OCR Item {i}: {text}")

            except Exception as e:
                logger.error(f"OCR failed for item {i}: {e}")
                continue
                
        logger.info(f"OCR completed. Recognized text for {count}/{len(items)} items.")
        return items

ocr_processor = OCRProcessor()
