import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Decodes an image from bytes and returns a 3-channel color image
    suitable for CRAFT text detection (no grayscale or CLAHE).
    
    Args:
        image_bytes: Raw image bytes from the upload.
        
    Returns:
        np.ndarray: The decoded BGR color image.
        
    Raises:
        ValueError: If the image cannot be decoded.
    """
    try:
        # Decode bytes to numpy array in color mode (BGR)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to decode image data")
        
        logger.info(f"Image decoded successfully. Shape: {img.shape}")
        logger.info(f"Image dtype: {img.dtype}, contiguous: {img.flags['C_CONTIGUOUS']}")

        
        return img
        
    except Exception as e:
        logger.error(f"Error during preprocessing: {e}")
        raise
