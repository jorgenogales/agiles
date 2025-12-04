import os
import pytest
from unittest.mock import MagicMock, patch
import sys
import io

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the upload page renders successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Upload Video" in response.data

def test_upload_no_file(client):
    """Test upload endpoint without a file part."""
    response = client.post('/upload')
    assert response.status_code == 400
    assert b"No file part" in response.data

def test_upload_empty_filename(client):
    """Test upload endpoint with an empty filename."""
    data = {'file': (io.BytesIO(b''), '')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"No selected file" in response.data

def test_upload_local_backend(client, tmpdir):
    """Test upload with STORAGE_BACKEND='local'."""
    with patch.dict(os.environ, {'STORAGE_BACKEND': 'local'}):
        
        data = {'file': (io.BytesIO(b'fake video content'), 'test_video.mp4')}
        
        # Mock file.save to avoid actual filesystem writes and verify call
        with patch('werkzeug.datastructures.FileStorage.save') as mock_save:
            response = client.post('/upload', data=data, content_type='multipart/form-data')
            
            assert response.status_code == 200
            assert b"Upload successful" in response.data
            assert b"Path:" in response.data
            
            # Verify the path structure
            args, _ = mock_save.call_args
            saved_path = args[0]
            # Normalize path separators for Windows compatibility if needed, but we are on darwin
            assert "tmp/" in saved_path or "tmp\\" in saved_path
            assert "video.mp4" in saved_path

@patch('main.storage.Client')
def test_upload_gcs_backend(mock_storage_client, client):
    """Test upload with STORAGE_BACKEND='gcs' (default)."""
    # Setup Mock GCS
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_client_instance = MagicMock()
    
    mock_storage_client.return_value = mock_client_instance
    mock_client_instance.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    
    data = {'file': (io.BytesIO(b'fake video content'), 'test_video.mp4')}
    
    # Ensure env var is set to GCS (or default)
    with patch.dict(os.environ, {'STORAGE_BACKEND': 'gcs'}):
        response = client.post('/upload', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        assert b"Upload successful" in response.data
        assert b"GCS Path: gs://" in response.data
        
        # Verify GCS calls
        mock_client_instance.bucket.assert_called()
        mock_bucket.blob.assert_called()
        # Check that the blob name ends with video.mp4
        args, _ = mock_bucket.blob.call_args
        assert args[0].endswith('/video.mp4')
        mock_blob.upload_from_file.assert_called()


