# Technical Design Document - Intelligent Asset Enrichment MVP

## 1. Introduction
This document outlines the architecture for the "Intelligent Asset Enrichment" MVP. The system extends the basic upload/list functionality to include Generative AI processing for metadata and thumbnail generation, along with video playback capabilities, utilizing Google Cloud Storage (GCS) and Vertex AI.

## 2. System Overview

### 2.1 High-Level Architecture
The application is a monolithic Python Flask service. It handles HTTP requests, orchestrates AI processing via Vertex AI, and manages data in GCS.

```mermaid
graph LR
    Client[Browser] -->|POST /upload| Flask[Flask App]
    Flask -->|Store Video| GCS[GCS Bucket]
    Flask -->|Analyze Video| Vertex[Vertex AI (Gemini)]
    Vertex -->|Metadata & Thumbnail| Flask
    Flask -->|Store Metadata & Thumbnail| GCS
    GCS -->|List Blobs & Metadata| Flask
    Client -->|GET /watch| Flask
```

## 3. Key Components

### 3.1 Web Application (Flask)
-   **Framework:** Flask.
-   **Deployment:** Local / Kubernetes.
-   **Responsibilities:** Request handling, orchestration of GCS I/O and Vertex AI calls.

### 3.2 Storage (GCS Bucket)
The GCS bucket acts as the file system and database.

**Bucket Structure:**
For each video, a "directory" (prefix) is created using a unique ID:
*   `{random_id}/video.mp4`: The original video file.
*   `{random_id}/metadata.json`: JSON file containing AI-generated title, description, and tags.
*   `{random_id}/thumbnail.png`: The AI-generated thumbnail image.

### 3.3 AI Service (Vertex AI)
-   **Model:** gemini-2.5-flash
-   **Task:** Analyze video content to generate text metadata.

## 4. Workflows

### 4.1 Upload & Enrich
1.  **Receive:** User sends `POST /upload` with a video file.
2.  **Generate ID:** App generates a unique `random_id`.
3.  **Store Video:** App streams the file to GCS at `{random_id}/video.mp4`.
4.  **Enrich (AI Processing):**
    *   App sends a request to Vertex AI with the GCS URI of the video.
    -   Prompt model to generate: Title, Description, and Tags.
5.  **Extract Thumbnail:**
    *   App uses standard Python libraries (e.g., OpenCV, moviepy) to extract the first frame of the video as a thumbnail.
6.  **Store Artifacts:**
    *   Save Title, Description, Tags to `{random_id}/metadata.json`.
    *   Save Thumbnail to `{random_id}/thumbnail.png`.
6.  **Respond:** Redirect user to the Dashboard.

### 4.2 Video List (Dashboard)
1.  **Scan:** App lists directories (prefixes) in the GCS bucket.
2.  **Fetch Data:** For each `random_id`:
    *   Read `{random_id}/metadata.json` (fallback to raw filename if missing).
    *   Generate signed URLs (or public URLs) for `{random_id}/thumbnail.png`.
3.  **Render:** Display a grid/list of videos with their AI-generated thumbnails and metadata.

### 4.3 Video Player
1.  **Request:** User requests `/watch/{random_id}`.
2.  **Fetch:** App retrieves metadata and generates a signed URL for `{random_id}/video.mp4`.
3.  **Render:** HTML page with an HTML5 video player and video details.

## 5. Technology Stack
-   **Language:** Python 3.9+
-   **Web Framework:** Flask
-   **Cloud Storage SDK:** `google-cloud-storage`
-   **AI SDK:** `google-cloud-aiplatform` (Vertex AI)

## 6. Trade-offs & Risks
-   **Latency:** AI processing is synchronous during upload. Large videos might time out the request. *Mitigation:* Use async processing (background tasks) in a future iteration. For MVP, we will assume short videos or long timeouts.
-   **Cost:** Vertex AI calls incur costs per request.
-   **Consistency:** GCS is eventually consistent, though strongly consistent for read-after-write in most regions. Metadata might lag slightly if listing immediately.
