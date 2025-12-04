# Technical Design Document (v3)
## Simple Video Upload System

### 1. Introduction
This document outlines the technical design for the simplified "Simple Video Upload System". It focuses exclusively on the mechanism to upload a video file and store it in Google Cloud Storage (GCS) with a specific directory structure.

### 2. High-Level Architecture
A single Python Flask application running on Google Kubernetes Engine (GKE) will handle the file upload requests and stream the data directly to Google Cloud Storage (GCS).

```
+------------------+      (1) Upload Video      +------------------------------------------+      (2) Store Object      +-------------------------------------------------+
|   User Browser   | -------------------------> | Python Flask App (GKE: [LDAP]-agiles-cluster) | -------------------------> | Google Cloud Storage (Bucket: [LDAP]-agiles-video-upload) |
+------------------+                            +------------------------------------------+                               +-------------------------------------------------+
```

### 3. Components

#### 3.1. Flask Application
*   **Stack:** Python 3, Flask, `google-cloud-storage` library.
*   **Endpoints:**
    *   `GET /`: Renders the upload form.
    *   `POST /upload`: Handles the file upload.
*   **Logic:**
    1.  Receive file from request.
    2.  Generate UUID.
    3.  Initialize GCS client.
    4.  Upload file to [LDAP]-agiles-video-upload bucket with blob name `<uuid>/video.mp4`.
    5.  Return success message with UUID.

#### 3.2. Persistence (GCS)
*   **Bucket:** [LDAP]-agiles-video-upload
*   **Object Key Format:** `<uuid>/video.mp4`

### 4. Data Flow
1.  **User uploads video:** The user selects a video file via the web interface and initiates the upload.
2.  **Flask receives file:** The Flask application receives the video file.
3.  **Generate UUID:** A unique UUID is generated for the uploaded file.
4.  **Upload to GCS:** The Flask application uploads the video file to the GCS bucket `[LDAP]-agiles-video-upload` using the structure `/<uuid>/video.mp4`.
5.  **Return Confirmation:** The Flask application returns a success message to the user, including the generated UUID and the full GCS path.

### 5. Deployment & Infrastructure
*   **Container:** Docker image built via Cloud Build. Both the Docker image name and Kubernetes service name will be prefixed with the user's LDAP (e.g., `[LDAP]-agiles-upload-service`).
*   **Deployment Packaging:** All deployable code artifacts will be enclosed within a dedicated deployment folder for clarity and ease of management.
*   **Orchestration:** Deployed to GKE cluster [LDAP]-agiles-cluster.
*   **Security:** Uses Workload Identity or standard Node Service Account for GCS access.

### 6. Local Development
*   **Run:** `python main.py`
*   **Storage Abstraction:**
    *   **Production:** Uses `google.cloud.storage`.
    *   **Local:** If `STORAGE_BACKEND=local`, saves files to a local `tmp/` directory mimicking the bucket structure.