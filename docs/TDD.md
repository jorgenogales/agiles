# Technical Design Document (v3)
## Simple Video Upload System

### 1. Introduction
This document outlines the technical design for the simplified "Simple Video Upload System". It focuses exclusively on the mechanism to upload a video file and store it in Google Cloud Storage (GCS) with a specific directory structure.

### 2. High-Level Architecture
A single Python Flask application running on Google Kubernetes Engine (GKE) will handle the file upload requests and stream the data directly to Google Cloud Storage (GCS).

```
+------------------+      (1) Upload Video      +-------------------------+      (2) Store Object      +-------------------------+
|   User Browser   | -------------------------> | Python Flask App (GKE)  | -------------------------> | Google Cloud Storage    |
+------------------+                            +-------------------------+                            +-------------------------+
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
    4.  Upload file to `agiles-video-upload` bucket with blob name `<uuid>/video.mp4`.
    5.  Return success message with UUID.

#### 3.2. Persistence (GCS)
*   **Bucket:** `agiles-video-upload`
*   **Object Key Format:** `<uuid>/video.mp4`

### 4. Deployment & Infrastructure
*   **Container:** Docker image built via Cloud Build.
*   **Orchestration:** Deployed to GKE cluster `agiles-cluster`.
*   **Security:** Uses Workload Identity or standard Node Service Account for GCS access.

### 5. Local Development
*   **Run:** `python main.py`
*   **Storage Abstraction:**
    *   **Production:** Uses `google.cloud.storage`.
    *   **Local:** If `STORAGE_BACKEND=local`, saves files to a local `tmp/` directory mimicking the bucket structure.