import os
import logging
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from utils.storage import upload_file, list_files

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key-for-dev")
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    videos = []
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    try:
        # List all files in the bucket
        blobs = list_files()
        
        for blob in blobs:
            # We are looking for files that match the pattern {id}/video.mp4
            # blob.name would be something like "some-uuid-string/video.mp4"
            if blob.name.endswith('/video.mp4'):
                parts = blob.name.split('/')
                if len(parts) == 2:
                    video_id = parts[0]
                    # Construct public URL (though we don't really use it for watching anymore, 
                    # it might be useful for debugging or if we add a download link later)
                    video_url = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
                    
                    videos.append({
                        'id': video_id,
                        'url': video_url,
                        'created_at': blob.time_created
                    })
        
        # Sort videos by created_at descending (newest first)
        videos.sort(key=lambda x: x.get('created_at') or '', reverse=True)
        
    except Exception as e:
        logger.error(f"Error listing videos: {e}")
        flash(f"Error retrieving video list: {e}")

    return render_template('dashboard.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No video file part')
            return redirect(request.url)
        
        file = request.files['video']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Generate a unique random ID
                unique_id = str(uuid.uuid4())
                
                # US-01: Upload under the path {random_id}/video.mp4
                destination_path = f"{unique_id}/video.mp4"
                
                # Upload directly from the file object (stream)
                upload_file(file, destination_path, content_type=file.content_type)
                
                flash('Video uploaded successfully!')
                return redirect(url_for('index'))

            except Exception as e:
                logger.error(f"Upload failed: {e}")
                flash(f"An error occurred: {e}")
                return redirect(request.url)
        else:
            flash('Invalid file type')
            return redirect(request.url)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)