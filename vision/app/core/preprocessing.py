import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Decodes an image from bytes, converts to grayscale, and applies CLAHE.
    
    Args:
        image_bytes: Raw image bytes from the upload.
        
    Returns:
        np.ndarray: The preprocessed grayscale image.
        
    Raises:
        ValueError: If the image cannot be decoded.
    """
    try:
        # 1. Decode bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to decode image data")
            
        # 2. Convert to Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 3. Enhance contrast using CLAHE
        # Clip limit 2.0 and tile size 8x8 are standard defaults that work well for text
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        logger.info(f"Image preprocessed successfully. Shape: {enhanced.shape}")
        
        return enhanced
        
    except Exception as e:
        logger.error(f"Error during preprocessing: {e}")
        raise
