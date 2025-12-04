import os
import uuid
import logging
from flask import Flask, request, render_template
from google.cloud import storage
from werkzeug.utils import secure_filename

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Read configuration inside request to allow easier testing/env switching
    storage_backend = os.environ.get('STORAGE_BACKEND', 'gcs')
    gcs_bucket_name = os.environ.get('GCS_BUCKET_NAME', 'jorgenogales-agiles-video-upload')

    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400
        
    if file:
        # TDD: 3.1. Logic step 2: Generate UUID.
        file_uuid = str(uuid.uuid4())
        
        # TDD: 3.1. Logic step 4: Upload file ... with blob name <uuid>/video.mp4
        destination_blob_name = f"{file_uuid}/video.mp4"
        
        if storage_backend == 'local':
            # TDD: 6. Local Development: If STORAGE_BACKEND=local, saves files to a local tmp/ directory
            local_path = os.path.join('tmp', destination_blob_name)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            file.save(local_path)
            return f"Upload successful. UUID: {file_uuid}. Path: {local_path}"
            
        else:
            # GCS storage logic
            try:
                # TDD: 3.1. Logic step 3: Initialize GCS client.
                storage_client = storage.Client()
                bucket = storage_client.bucket(gcs_bucket_name)
                blob = bucket.blob(destination_blob_name)
                
                # Upload from file object
                blob.upload_from_file(file, content_type=file.content_type)
                
                # TDD: 4. Data Flow step 5: Return success message with UUID and full GCS path.
                gcs_path = f"gs://{gcs_bucket_name}/{destination_blob_name}"
                return f"Upload successful. UUID: {file_uuid}. GCS Path: {gcs_path}"
            except Exception as e:
                logging.error(f"Failed to upload to GCS: {e}")
                return f"Failed to upload to GCS: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
