import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

class ModelManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance.detector = None
            cls._instance.recognizer = None  # Reserved for Milestone 3
            cls._instance.initialized = False
        return cls._instance

    def load_models(self):
        if self.initialized:
            logger.info("Models already initialized.")
            return

        logger.info("Loading Vision Models...")
        
        try:
            # Verify imports
            import cv2
            import numpy as np
            from paddleocr import PaddleOCR

            # Initialize PaddleOCR (Detection Only)
            logger.info("Initializing PaddleOCR Detector...")
            # det=True, rec=False means layout detection only (bounding boxes)
            # use_angle_cls=True helps with rotated text
            # lang='en' is default
            self.detector = PaddleOCR(use_angle_cls=True, lang='en', det=True, rec=False, use_gpu=False, show_log=False)
            
            # Initialize Recognizer
            logger.info("Initializing PaddleOCR Recognizer...")
            self.recognizer = PaddleOCR(use_angle_cls=True, lang='en', det=False, rec=True, use_gpu=False, show_log=False)

            self.initialized = True
            logger.info("Vision Models established (Detector & Recognizer Loaded).")
            
        except ImportError as e:
            logger.error(f"Failed to import required ML libraries: {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise e

    def check_health(self):
        return self.initialized and self.detector is not None

model_manager = ModelManager()
