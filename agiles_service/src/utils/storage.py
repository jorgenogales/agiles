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

def upload_text(text_content, destination_blob_name, content_type="text/plain"):
    """
    Uploads text content to the bucket.

    Args:
        text_content (str): The text content to upload.
        destination_blob_name (str): The path of the GCS object.
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
        blob.upload_from_string(text_content, content_type=content_type)
        logger.info(f"Text uploaded to {destination_blob_name} in bucket {bucket_name}.")
        return f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"
    except Exception as e:
        logger.error(f"Failed to upload text: {e}")
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

def delete_blob(blob_name):
    """
    Deletes a blob from the bucket.

    Args:
        blob_name (str): The name of the blob to delete.
    """
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    try:
        blob.delete()
        logger.info(f"Blob {blob_name} deleted.")
    except Exception as e:
        logger.error(f"Failed to delete blob {blob_name}: {e}")
        raise

def delete_folder(prefix):
    """
    Deletes all blobs in the bucket that begin with the prefix.
    This effectively deletes a 'folder' in GCS.

    Args:
        prefix (str): The prefix of the blobs to delete.
    """
    blobs = list_files(prefix=prefix)
    for blob in blobs:
        delete_blob(blob.name)
    logger.info(f"Deleted all blobs with prefix {prefix}")