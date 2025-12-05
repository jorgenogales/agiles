import os
import json
import logging
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_vertex_ai():
    """
    Initializes Vertex AI SDK.
    Environment variables GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION 
    should be set, or default credentials/config will be used.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if project_id:
        vertexai.init(project=project_id, location=location)
    else:
        logger.warning("GOOGLE_CLOUD_PROJECT not set. Vertex AI init might depend on default credentials.")
        # Try init without project, letting it discover
        vertexai.init(location=location)

def analyze_video(gcs_uri):
    """
    Analyzes a video stored in GCS using Gemini Flash to generate metadata.

    Args:
        gcs_uri (str): The GCS URI of the video (gs://bucket/path).

    Returns:
        dict: A dictionary containing 'title', 'description', and 'tags'.
              Returns None if analysis fails.
    """
    try:
        init_vertex_ai()
        
        model = GenerativeModel("gemini-2.5-flash")
        
        video_part = Part.from_uri(
            uri=gcs_uri,
            mime_type="video/mp4"
        )
        
        prompt = """
        Analyze the uploaded video and generate a JSON object with the following fields:
        - title: A click-maximizing title for the video.
        - description: A generic description of the video content.
        - tags: A list of relevant metadata tags (strings).
        
        Ensure the output is valid JSON.
        """
        
        logger.info(f"Sending video {gcs_uri} to Vertex AI for analysis...")
        response = model.generate_content(
            [video_part, prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        
        text_response = response.text
        logger.info("Vertex AI response received.")
        
        try:
            metadata = json.loads(text_response)
            return metadata
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from Vertex AI response: {text_response}")
            return None
            
    except Exception as e:
        logger.error(f"Error during Vertex AI analysis: {e}")
        return None
