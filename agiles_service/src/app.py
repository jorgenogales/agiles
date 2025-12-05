import os
import logging
import uuid
import json
import tempfile
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from utils.storage import upload_file, list_files, upload_text
from utils.vertex_ai import analyze_video
from utils.video_processing import extract_first_frame

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
        
        # Organize blobs by video_id
        video_data = {}
        
        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) == 2:
                video_id = parts[0]
                if video_id not in video_data:
                    video_data[video_id] = {'id': video_id}
                
                if parts[1] == 'video.mp4':
                    video_data[video_id]['video_blob'] = blob
                    video_data[video_id]['url'] = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
                    video_data[video_id]['created_at'] = blob.time_created
                elif parts[1] == 'metadata.json':
                    video_data[video_id]['metadata_blob'] = blob
                elif parts[1] == 'thumbnail.jpg':
                    video_data[video_id]['thumbnail_url'] = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"

        # Process each video
        for vid, data in video_data.items():
            if 'video_blob' in data:
                video_entry = {
                    'id': data['id'],
                    'url': data['url'],
                    'thumbnail_url': data.get('thumbnail_url'), # Add thumbnail URL
                    'created_at': data['created_at'],
                    'title': data['id'], # Default title is ID
                    'description': 'No description available.',
                    'tags': []
                }
                
                # Try to load metadata if available
                if 'metadata_blob' in data:
                    try:
                        json_content = data['metadata_blob'].download_as_text()
                        metadata = json.loads(json_content)
                        video_entry['title'] = metadata.get('title', video_entry['title'])
                        video_entry['description'] = metadata.get('description', video_entry['description'])
                        video_entry['tags'] = metadata.get('tags', [])
                    except Exception as e:
                        logger.error(f"Error reading metadata for {vid}: {e}")
                
                videos.append(video_entry)
        
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
            # Create a temporary file to save the uploaded video
            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
            temp_video_path = temp_video.name
            
            try:
                # Save uploaded chunk to temp file
                file.save(temp_video_path)
                temp_video.close() # Close so other processes can access it
                
                # Generate a unique random ID
                unique_id = str(uuid.uuid4())
                bucket_name = os.environ.get("GCS_BUCKET_NAME")
                
                # US-01: Upload under the path {random_id}/video.mp4
                destination_path = f"{unique_id}/video.mp4"
                
                # Re-open temp file to upload to GCS
                with open(temp_video_path, 'rb') as f:
                    upload_file(f, destination_path, content_type=file.content_type)
                
                # US-04: Thumbnail Extraction
                thumbnail_path = extract_first_frame(temp_video_path)
                if thumbnail_path:
                    thumb_dest = f"{unique_id}/thumbnail.jpg"
                    with open(thumbnail_path, 'rb') as f:
                        upload_file(f, thumb_dest, content_type="image/jpeg")
                    # Clean up temp thumbnail
                    os.remove(thumbnail_path)
                else:
                    logger.warning("Thumbnail extraction failed.")

                # US-03: Synchronous AI Metadata Generation
                gcs_uri = f"gs://{bucket_name}/{destination_path}"
                logger.info(f"Starting synchronous analysis for {unique_id}...")
                
                try:
                    metadata = analyze_video(gcs_uri)
                    if metadata:
                        json_str = json.dumps(metadata)
                        meta_destination = f"{unique_id}/metadata.json"
                        upload_text(json_str, meta_destination, content_type="application/json")
                        logger.info(f"Metadata generated and saved for {unique_id}")
                    else:
                        logger.warning(f"No metadata generated for {unique_id}")
                except Exception as ai_error:
                    # We don't want to fail the upload if AI fails, just log it
                    logger.error(f"AI Analysis failed: {ai_error}")
                
                flash('Video uploaded successfully!')
                return redirect(url_for('index'))

            except Exception as e:
                logger.error(f"Upload failed: {e}")
                flash(f"An error occurred: {e}")
                return redirect(request.url)
            finally:
                # Clean up temp video file
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
        else:
            flash('Invalid file type')
            return redirect(request.url)

    return render_template('upload.html')

@app.route('/watch/<video_id>')
def watch_video(video_id):
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    try:
        # List files with the prefix of the video_id
        blobs = list_files(prefix=f"{video_id}/")
        
        if not blobs:
            flash('Video not found.')
            return redirect(url_for('index'))
            
        video_data = {
            'id': video_id,
            'title': video_id,
            'description': 'No description available.',
            'tags': [],
            'url': None,
            'created_at': None
        }
        
        metadata_blob = None
        
        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) == 2:
                if parts[1] == 'video.mp4':
                    video_data['url'] = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
                    video_data['created_at'] = blob.time_created
                elif parts[1] == 'metadata.json':
                    metadata_blob = blob
        
        if not video_data['url']:
            flash('Video file missing.')
            return redirect(url_for('index'))
            
        # Load metadata if available
        if metadata_blob:
            try:
                json_content = metadata_blob.download_as_text()
                metadata = json.loads(json_content)
                video_data['title'] = metadata.get('title', video_data['title'])
                video_data['description'] = metadata.get('description', video_data['description'])
                video_data['tags'] = metadata.get('tags', [])
            except Exception as e:
                logger.error(f"Error reading metadata for {video_id}: {e}")

        return render_template('watch.html', video=video_data)

    except Exception as e:
        logger.error(f"Error retrieving video {video_id}: {e}")
        flash(f"Error loading video: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)