import os
from google.cloud import storage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_storage_client():
    """
    Initializes and returns a Google Cloud Storage client.
    """
    return storage.Client()

def upload_file(file_obj, destination_blob_name, content_type=None):
    """
    Uploads a file object to the bucket.

    Args:
        file_obj: The file-like object to upload.
        destination_blob_name (str): The ID of the GCS object.
        content_type (str): The content type of the file.

    Returns:
        str: The public HTTP URL of the uploaded file.
    """
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        logger.error("GCS_BUCKET_NAME environment variable not set.")
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_file(file_obj, content_type=content_type)
        logger.info(f"File uploaded to {destination_blob_name} in bucket {bucket_name}.")
        return f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        raise

def list_files(prefix=None):
    """
    Lists all the blobs in the bucket that begin with the prefix.

    Args:
        prefix (str, optional): The prefix to filter by.

    Returns:
        list: A list of blob objects.
    """
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)

    return list(bucket.list_blobs(prefix=prefix))