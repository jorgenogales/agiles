# US-001: Video Upload and Synchronous Processing

## Description
As a user, I want to upload a video file so that it can be stored, analyzed by AI, and have a thumbnail generated automatically.

## Priority
High (Core MVP Feature)

## Dependencies
- Google Cloud Storage (GCS) Bucket configured.
- Vertex AI (Gemini) API enabled and accessible.
- Local environment configured with `opencv-python-headless`.

## Acceptance Criteria

### 1. File Selection & Upload
- [ ] The user interface provides a form to select a video file from the local device.
- [ ] Upon submission, the file is validated (basic check, e.g., is it a video?).
- [ ] The raw video file is uploaded to the GCS bucket under the `videos/` directory.

### 2. Thumbnail Generation
- [ ] The system generates a thumbnail image from the uploaded video using a local library (e.g., `opencv-python`).
- [ ] The generated thumbnail is uploaded to the GCS bucket under the `thumbnails/` directory.

### 3. AI Analysis (Gemini)
- [ ] The system calls the Vertex AI Gemini model with the uploaded video (referencing its GCS URI).
- [ ] The prompt requests a **text summary** and **5 relevant tags**.
- [ ] The system receives the structured response from the AI.

### 4. Metadata Persistence
- [ ] A JSON object is constructed containing:
    - Unique ID / Filename
    - GCS URL for the video
    - GCS URL for the thumbnail
    - AI-generated Summary
    - AI-generated Tags
    - Creation Timestamp
- [ ] This JSON object is saved to the GCS bucket under the `metadata/` directory.

### 5. User Experience (Synchronous Flow)
- [ ] The entire process (Upload -> Thumbnail -> AI -> Save Metadata) occurs synchronously within the HTTP request.
- [ ] The user sees a loading state during processing.
- [ ] Upon successful completion, the user is redirected to the Video List page (US-002).
- [ ] If an error occurs at any stage, a clear error message is displayed to the user.

## Technical Notes
- **Endpoint:** `POST /upload`
- **Timeout:** Since this is synchronous, ensure the web server timeout is sufficient (e.g., > 60s) or communicate the limitation.
- **Naming Convention:** Ensure filenames are sanitized or hashed to prevent collisions and issues in GCS.
