import os
import logging
import pytest
from unittest.mock import MagicMock, patch
import sys
import datetime

# Add src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.list_files')
@patch('app.upload_file')
def test_upload_video_success(mock_upload_file, mock_list_files, client):
    # Setup mocks
    mock_list_files.return_value = [] # Return empty list for index page redirect
    
    # Mock file upload
    data = {
        'video': (open(__file__, 'rb'), 'test_video.mp4') # Use this file as dummy content
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)

    assert response.status_code == 200
    assert b'Video uploaded successfully!' in response.data
    
    # Verify upload called once
    assert mock_upload_file.call_count == 1
    # Check args of upload_file to verify path structure
    args, _ = mock_upload_file.call_args
    assert args[1].endswith('/video.mp4')
    assert len(args[1].split('/')) == 2 # {uuid}/video.mp4

def test_upload_no_file(client):
    response = client.post('/upload', data={}, follow_redirects=True)
    assert b'No video file part' in response.data

def test_upload_invalid_extension(client):
    data = {
        'video': (open(__file__, 'rb'), 'test.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b'Invalid file type' in response.data

@patch('app.list_files')
def test_index_route(mock_list_files, client):
    # Mock GCS blob
    mock_blob = MagicMock()
    mock_blob.name = "test-uuid/video.mp4"
    mock_blob.time_created = datetime.datetime.now()
    
    mock_list_files.return_value = [mock_blob]
    
    response = client.get('/')
    
    assert response.status_code == 200
    assert b'Video Library' in response.data
    assert b'Video ID: test-uuid' in response.data