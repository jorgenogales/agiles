# Technical Design Document - Simplified Architecture (MVP)

## 1. Introduction
This document outlines the simplified architecture for the Video Processing MVP. To minimize complexity and external dependencies for the initial prototype, the system will operate without a traditional database and without asynchronous background workers. The Google Cloud Storage (GCS) bucket will serve as the single source of truth for state, and all processing will occur synchronously during the upload request.

## 2. System Overview

### 2.1 High-Level Architecture
The application is a monolithic Python Flask service. It handles HTTP requests, communicates directly with GCS for storage, and calls Vertex AI for video analysis in a blocking manner.

```mermaid
graph LR
    Client[Browser] -->|POST /upload| Flask[Flask App]
    
    subgraph "GCP Services"
        Flask -->|1. Store Video| GCS[GCS Bucket]
        Flask -->|2. Analyze Video| Vertex[Vertex AI (Gemini)]
    end
    
    Flask -->|3. Generate Thumbnail| LocalLib[OpenCV/FFmpeg]
    Flask -->|4. Store Thumbnail & Metadata| GCS
    
    GCS -->|List/Read| Flask
```

## 3. Key Components

### 3.1 Web Application (Flask)
-   **Framework:** Flask.
-   **Deployment:** Local / Kubernetes.
-   **State:** Stateless logic; relies entirely on GCS for data persistence.

### 3.2 "Database" (GCS Bucket)
There is no SQL or NoSQL database. The file structure within the GCS bucket acts as the database. The presence of a JSON file in the `metadata/` directory indicates a successfully processed video.

**Bucket Structure:**
*   `videos/{filename}`: The raw original video file.
*   `thumbnails/{filename}.jpg`: The generated thumbnail image.
*   `metadata/{filename}.json`: A JSON object containing the analysis results and references.

**Metadata JSON Schema:**
```json
{
  "id": "unique_id_or_filename",
  "video_url": "gs://bucket/videos/file.mp4",
  "thumbnail_url": "https://storage.googleapis.com/...",
  "summary": "AI generated summary...",
  "tags": ["tag1", "tag2"],
  "created_at": "ISO-8601 timestamp"
}
```

## 4. Workflows

### 4.1 Synchronous Upload & Process
This flow executes in a single HTTP request-response cycle. Note: This implies the user must keep the browser tab open until analysis is complete.

1.  **Receive:** User sends `POST /upload` with a video file.
2.  **Save Video:** App streams the file to GCS `videos/`.
3.  **Thumbnail:** App uses `opencv-python` locally to grab a frame, saves it to a temp file, and uploads to GCS `thumbnails/`.
4.  **Analyze:** App uses Vertex AI SDK to analyze the video (referencing the GCS URI).
    *   *Prompt:* "Summarize this video and generate 5 relevant tags."
5.  **Save Metadata:** App constructs the JSON metadata object and uploads it to GCS `metadata/`.
6.  **Respond:** App redirects user to the Video List page.

### 4.2 Video List & View
1.  **List:** App iterates over blobs in the `metadata/` prefix of the GCS bucket.
2.  **Parse:** App downloads/reads each JSON file to build the list of videos (Title, Thumbnail, Summary).
3.  **Render:** HTML template displays the list.

## 5. Technology Stack
-   **Language:** Python 3.9+
-   **Web Framework:** Flask
-   **Cloud Storage SDK:** `google-cloud-storage`
-   **AI SDK:** `google-cloud-aiplatform`
-   **Video Tools:** `opencv-python-headless` (for lightweight thumbnail extraction)

## 6. Trade-offs & Risks
-   **Latency:** Large videos or slow AI responses will block the HTTP request. If processing exceeds the web server's timeout (e.g., 30-60s), the request may fail from the user's perspective despite continuing on the server.
-   **Scalability:** Listing thousands of files from GCS to build the homepage will eventually become slow (O(N) API calls).
-   **Reliability:** If the process crashes after video upload but before metadata save, the system will have "orphaned" video files that don't appear in the list.
