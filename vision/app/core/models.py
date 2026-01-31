import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

class ModelManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance.ocr = None
            cls._instance.layout_processor = None
            cls._instance.layout_model = None
            cls._instance.initialized = False
        return cls._instance

    def load_models(self):
        if self.initialized:
            logger.info("Models already initialized.")
            return

        logger.info("Loading Vision Models...")
        
        try:
            # Verify imports to ensure dependencies are present
            import cv2
            import numpy as np
            from paddleocr import PaddleOCR
            from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
            import torch

            # TODO: Uncomment for Milestone 2+ when real inference is needed
            # logger.info("Initializing PaddleOCR...")
            # self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)
            
            logger.info("Initializing LayoutLMv3...")
            self.layout_processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base")
            self.layout_model = LayoutLMv3ForTokenClassification.from_pretrained("microsoft/layoutlmv3-base")

            # For Milestone 1, we consider success if libraries are importable
            self.initialized = True
            logger.info("Vision Models established (Imports verified).")
            
        except ImportError as e:
            logger.error(f"Failed to import required ML libraries: {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise e

    def check_health(self):
        return self.initialized

model_manager = ModelManager()
