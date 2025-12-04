# Technical Design Document (v2)
## AI-Enhanced Video Upload & Catalog

### 1. Introduction
This document outlines the revised technical design for the "AI Video Metadata Automation & Catalog" project, aligned with the decision to build exclusively on Google Cloud Platform (GCP). It is based on the requirements in the [Product Requirements Document (PRD)](./PRD.md) and guides the development team.

### 2. High-Level Architecture
We will adopt a simplified, monolithic architecture deployed on Google Kubernetes Engine (GKE). The system will be a single Python Flask application that handles both frontend rendering and backend logic. It will leverage Google Cloud Storage (GCS) for all persistence and Vertex AI for content intelligence.

```
+-------------------------------------------------+
|                                                 |
|   User Browser                                  |
|                                                 |
+----------------------+--------------------------+
                       |
                       | HTTP(S) Request
                       v
+-------------------------------------------------+
|   Google Kubernetes Engine (GKE) Cluster        |
|                                                 |
|   +-----------------------------------------+   |
|   |                                         |   |
|   |      Python Flask Application           |   |
|   | (Frontend + Backend)                    |   |
|   |                                         |   |
|   +-----------------------------------------+   |
|       |                     ^                   |
|       | (1) Upload          | (5) Return        |
|       |     & Process       |     Result        |
|       v                     |                   |
|   +-----------------------------------------+   |
|   | (2) Vertex AI (gemini-2.5-flash)        |   |
|   |     - Analyzes video                    |   |
|   |     - Returns structured JSON           |   |
|   +-----------------------------------------+   |
|       |                     ^                   |
|       | (3) Get Metadata    | (4) Store         |
|       |     & Timestamps    |     Assets        |
|       v                     |                   |
|   +-----------------------------------------+   |
|   |     Google Cloud Storage (GCS)          |   |
|   |     - Stores video, metadata.json,      |   |
|   |       and thumbnails per UUID           |   |
|   +-----------------------------------------+   |
|                                                 |
+-------------------------------------------------+

```

### 3. Components

#### 3.1. Monolithic Application (Python/Flask)
*   **Technology Stack:** Python 3 with Flask. This single application will be responsible for serving the user interface, handling uploads, and orchestrating the entire AI processing workflow.
*   **Deployment:** The application will be containerized using Docker and deployed to a Google Kubernetes Engine (GKE) cluster named `agiles-cluster` for scalability and management. Google Cloud Build will be used for automating the Docker image creation and deployment process.
*   **Frontend (Server-Side Rendered):**
    *   **Templates:** Jinja2 templates will be used to render the HTML pages for the upload portal, video library, and video detail views.
    *   **Functionality:**
        *   **/upload:** A page with a simple HTML form for file selection.
        *   **/library:** A page that lists all processed videos by reading the contents of the GCS bucket.
        *   **/video/<uuid>:** A page to display a single video and its metadata.
*   **Backend Logic:**
    *   **`/upload` (POST):** This endpoint will be the core of the synchronous workflow. See data flow section for details.
    *   **`/library` (GET):** This route will list the objects in the GCS bucket that correspond to video metadata files to build the library view.
    *   **`/video/<uuid>` (GET):** This route will fetch the `metadata.json`, video, and thumbnail URLs from the corresponding GCS folder for the given UUID to render the detail page.

#### 3.2. AI Processing (Vertex AI)
*   **Service:** Google Vertex AI.
*   **Model:** `gemini-2.5-flash`.
*   **Process:** The Flask backend will make a direct, synchronous call to the Vertex AI API, sending the uploaded video. The prompt will explicitly request a structured JSON response containing:
    *   `title`: A powerful, SEO-friendly title.
    *   `synopsis`: An engaging summary.
    *   `thumbnail_timestamps_sec`: A list of integers representing the seconds in the video that are best for thumbnails.
*   **Example Prompt:**
    ```
    "Analyze this video and return a JSON object with the following structure: {\"title\": \"...\", \"synopsis\": \"...\", \"thumbnail_timestamps_sec\": [t1, t2, ...]}. The title should be catchy and optimized for clicks. The synopsis should be a concise and engaging pitch for the video content. The timestamps should correspond to the most visually compelling moments."
    ```

#### 3.3. Persistence Layer (Google Cloud Storage)
*   **Technology:** Google Cloud Storage (GCS) will be the single source of truth for all data. No database will be used.
*   **Data Structure:** All assets related to a single video will be grouped under a common prefix using a UUID generated upon upload.
    ```
    /agiles-video-upload/
    └── <video-uuid-1>/
        ├── video.mp4
        ├── metadata.json
        └── thumbnail.jpg
    └── <video-uuid-2>/
        ├── video.mp4
        ├── metadata.json
        └── thumbnail.jpg
    ...
    ```
*   **`metadata.json` Content:**
    ```json
    {
      "title": "AI Generated Title",
      "synopsis": "AI generated synopsis...",
      "video_url": "https://storage.googleapis.com/bucket/uuid/video.mp4",
      "thumbnail_url": "https://storage.googleapis.com/bucket/uuid/thumbnail.jpg",
      "original_filename": "my_awesome_video.mp4",
      "upload_timestamp": "2025-12-04T12:00:00Z"
    }
    ```

### 4. Data Flows

#### 4.1. Synchronous Video Upload
1.  **User selects and submits a video file** via the Flask-rendered `/upload` page.
2.  The **Flask backend receives the video file**. It generates a unique **UUID** for this video.
3.  The backend **uploads the original video to GCS** into a new "folder" named after the UUID (e.g., `gs://agiles-video-upload/<uuid>/video.mp4`).
4.  The backend **calls the Vertex AI Gemini API**, providing the GCS path to the video and the structured response prompt.
5.  **Vertex AI processes the video and returns the structured JSON** (`title`, `synopsis`, `thumbnail_timestamps_sec`).
6.  The backend uses the first timestamp from `thumbnail_timestamps_sec` to **extract a frame from the video** (using a library like `OpenCV-Python`).
7.  The extracted frame is **uploaded to GCS as `thumbnail.jpg`** in the same UUID-named folder.
8.  The backend **constructs the `metadata.json` file** with all the information (title, synopsis, GCS URLs) and **uploads it to the GCS folder**.
9.  The entire process is synchronous. Once the `metadata.json` is stored, the backend **redirects the user to the video detail page** (`/video/<uuid>`) or back to the library, displaying the results of the operation.

#### 4.2. Library Functionality
1.  **User navigates to the Library page** (`/library`).
2.  The **Flask backend queries the GCS bucket** (`agiles-video-upload`) to list all objects ending in `metadata.json`.
3.  The backend **downloads and parses each `metadata.json` file** to extract the title, thumbnail URL, and synopsis excerpt.
4.  The backend **renders the library template** with the list of video objects.
5.  The **User views the list of videos** and clicks on a card to navigate to the detail view (`/video/<uuid>`).

### 5. Future Considerations
*   **Editing Metadata:** To allow edits, a new POST route (e.g., `/video/<uuid>/edit`) could be created. It would overwrite the `metadata.json` file in GCS.
*   **Performance:** For the video library, listing GCS objects can become slow with a very large number of videos. If performance degrades, an index could be maintained (e.g., a single `index.json` file in the root of the bucket, updated on each upload), or a managed database like Firestore/Cloud SQL could be reconsidered.

### 6. Non-Functional Requirements
*   **Scalability**: The application, running on GKE, can be scaled by adjusting the number of pods. Since the application is stateless (all state is in GCS), horizontal scaling is straightforward.
*   **Security**: GKE and GCS have robust security features. To simplify deployment, the application will use the standard Compute Engine service account associated with the GKE nodes, ensuring it has the necessary scopes for GCS and Vertex AI.
*   **Reliability**: GKE and GCS are highly available services. The synchronous nature of the upload process means that any failure in the chain (upload, AI processing, thumbnailing) will result in an immediate error returned to the user, ensuring a predictable experience.

### 7. Local Development
*   **Environment:** For local development, the application should run within a standard Python virtual environment (e.g., `venv`) by directly executing the Flask entry point script.
*   **Infrastructure Emulation:**
    *   **Compute:** Instead of deploying to GKE, the developer will run the Flask app locally (`python main.py`).
    *   **Storage:** To avoid dependency on remote GCS buckets during development and testing, the application should be configurable to use a local temporary folder for storing videos, thumbnails, and metadata files. The code should abstract the storage layer to switch between GCS (production) and Local File System (development) based on an environment variable (e.g., `STORAGE_BACKEND=local`).
