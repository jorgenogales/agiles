# Technical Implementation Plan: AI-Powered Video Metadata Generation

## 1. High-Level Architecture

The system will be a microservices-based architecture running on Google Kubernetes Engine (GKE). It will leverage Google Cloud Storage (GCS) for storing video, image assets, and metadata. It will use Google's AI/ML services for content analysis and generation. The frontend will be a single-page application (SPA) that communicates with the backend services via a REST API.

```
[User] -> [Frontend (SPA)] -> [Backend Services on GKE]
                                |
                                v
                        [GCS, Vertex AI]
```

## 2. Components

### 2.1. Frontend
A web-based interface consisting of static HTML pages with JavaScript for interactivity. This will provide the user interface for video uploads and for reviewing and editing the AI-generated metadata. These static assets will be served directly to the browser.

### 2.2. Backend Services (Microservices in Go on GKE)
All backend microservices will be written in **Go**. They will be designed to be lightweight and efficient, leveraging Go's strong support for concurrency to handle requests.

*   **Video Upload Service:** Handles multipart video uploads from the frontend and saves the video files to a GCS bucket. After the upload, it triggers the video processing orchestrator.
*   **Video Processing Orchestrator:** A service that is called synchronously by the Video Upload Service. It orchestrates the video analysis and metadata generation process by calling Gemini and the Frame Extraction Service.
*   **Frame Extraction Service:** Extracts video frames from given timestamps. It will save these thumbnails to a GCS bucket.
*   **Metadata Service:** A CRUD service for managing video metadata. It will store and retrieve metadata from **GCS** as JSON files. This includes video titles, descriptions, thumbnail URLs, and processing status, linking metadata with the uploaded video.

## 3. Data and Event Flow

1.  A Content Creator selects a video file for upload in the **Frontend**.
2.  The **Frontend** sends the video file to the **Video Upload Service**.
3.  The **Video Upload Service** streams the video to a GCS bucket (`gs://pepito-uploaded-videos`).
4.  Upon successful upload, the **Video Upload Service** synchronously calls the **Video Processing Orchestrator** with the path to the video in GCS.
5.  The **Video Processing Orchestrator** calls the **Gemini API** with the video file. The prompt will instruct Gemini to return a structured JSON response containing:
    *   `titles`: An array of suggested titles.
    *   `synopsis`: A generated synopsis of the video.
    *   `thumbnail_timestamps`: An array of seconds representing the most relevant moments for thumbnails.
6.  The orchestrator receives the structured data from Gemini.
7.  The orchestrator calls the **Frame Extraction Service**. This service takes the video file and the `thumbnail_timestamps` as input, extracts the specified frames (using a library like FFmpeg), and saves them as JPGs in a separate GCS bucket (`gs://pepito-video-thumbnails`).
8.  The orchestrator then calls the **Metadata Service** to save all the generated metadata (thumbnail URLs, synopsis, title suggestions) to a JSON file in a **GCS bucket** (`gs://pepito-video-metadata/{videoId}.json`). The processing status is updated to 'processed'.
9.  The **Frontend** periodically polls the **Metadata Service** for the status of the video processing. Once the status is 'processed', it displays the generated titles, synopsis, and thumbnail options to the user for review and editing.
10. When the user saves their changes, the **Frontend** calls the **Metadata Service** to update the final metadata in the GCS JSON file.

## 4. GCP Services Usage

*   **Google Kubernetes Engine (GKE):** To host and manage our containerized backend microservices.
*   **Google Cloud Storage (GCS):**
    *   `pepito-uploaded-videos` bucket: For storing the original uploaded videos.
    *   `pepito-video-thumbnails` bucket: For storing the generated thumbnail images.
    *   `pepito-video-metadata` bucket: For storing metadata as JSON files.
*   **Vertex AI:**
    *   **Gemini API:** For analyzing video content and generating titles, synopses, and key frame timestamps from a single, structured prompt.

## 5. GKE Deployment

Each backend microservice will be packaged as a Docker container and deployed to a GKE cluster.

*   **Deployments:** Each service will have its own GKE Deployment, specifying the container image, replicas, and resource requests/limits.
*   **Services:** Each Deployment will be exposed internally via a GKE Service (e.g., ClusterIP).
*   **Ingress:** A GKE Ingress resource will be used to expose the `Video Upload Service` and `Metadata Service` to the internet.
*   **Horizontal Pod Autoscaler (HPA):** Can be configured for the processing services to scale based on CPU/memory usage.
*   **Workload Identity:** GKE pods will be assigned dedicated GCP service accounts to securely access other Google Cloud services (GCS, Vertex AI) without needing to manage service account keys.

## 6. API Design (Simplified)

*   `POST /api/videos/upload`: Upload a new video.
*   `GET /api/videos/{videoId}/metadata`: Get metadata for a specific video, including AI-generated content.
*   `PUT /api/videos/{videoId}/metadata`: Update/save the final metadata for a video.

## 7. Implementation per User Story

1.  **Automatic Content Analysis:**
    *   Implemented by the **Video Processing Orchestrator** calling the **Gemini API**. A single prompt will instruct Gemini to analyze the video and return titles, a synopsis, and timestamps for thumbnails.

2.  **Thumbnail Suggestions:**
    *   The **Gemini API** will suggest timestamps. The **Frame Extraction Service** will then extract these frames from the video.

3.  **Synopsis Generation:**
    *   Implemented by the call to the **Gemini API**, which will generate a summary based on the video content.

4.  **Title Suggestions:**
    *   Also implemented by the single call to the **Gemini API**.

5.  **Review and Edit Interface:**
    *   The **Frontend** will have a dedicated view for this. After a video is processed, the UI will fetch the metadata and display the generated title and synopsis in editable text fields, and the suggested thumbnails as selectable images.

6.  **Seamless Workflow Integration:**
    *   This is achieved through a synchronous workflow. The video processing is triggered automatically after upload and runs in the background from the user's perspective, allowing the user to perform other tasks while waiting. The frontend can poll for the results.
