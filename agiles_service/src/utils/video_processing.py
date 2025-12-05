import cv2
import os
import logging
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_first_frame(video_path):
    """
    Extracts the first frame from a video file and saves it as an image.

    Args:
        video_path (str): Path to the local video file.

    Returns:
        str: Path to the generated thumbnail image (temporary file), or None if failed.
    """
    try:
        vidcap = cv2.VideoCapture(video_path)
        success, image = vidcap.read()
        
        if success:
            # Create a temporary file for the thumbnail
            # We use a NamedTemporaryFile but close it so cv2 can write to it
            # and we can re-open it later
            temp_thumb = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
            temp_thumb_path = temp_thumb.name
            temp_thumb.close()
            
            cv2.imwrite(temp_thumb_path, image)
            logger.info(f"Thumbnail extracted to {temp_thumb_path}")
            return temp_thumb_path
        else:
            logger.error("Failed to read first frame from video.")
            return None
            
    except Exception as e:
        logger.error(f"Error extracting thumbnail: {e}")
        return None
    finally:
        if 'vidcap' in locals():
            vidcap.release()
