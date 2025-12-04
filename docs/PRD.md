# Product Requirements Document (PRD)
## Simple Video Upload System

### 1. Overview
**Project Name:** Simple Video Upload System
**Source:** Simplified Scope Request
**Date:** December 4, 2025
**Status:** Draft

### 2. Problem Statement
We need a basic mechanism to reliably upload video files to cloud storage with a consistent structure to serve as the foundation for future processing pipelines.

### 3. Objectives
*   **Simplicity:** Minimize complexity by focusing solely on the upload and storage capability.
*   **Structure:** Ensure all uploaded assets follow a strict folder hierarchy in GCS to facilitate future automation.

### 4. Functional Requirements

#### 4.1 Video Upload Portal
*   **Interface:** A minimal web interface allowing users to select and upload a video file.
*   **Processing:**
    *   Generate a unique UUID for each upload.
    *   Upload the file to Google Cloud Storage (GCS).
*   **Output:** Display the resulting GCS path and UUID to the user upon success.

#### 4.2 Persistence Layer
*   **Storage:** Google Cloud Storage (GCS).
*   **Bucket Name:** [LDAP]-agiles-video-upload.
*   **Structure:** `/<uuid>/video.mp4`.

### 5. User Experience (UX)
*   **Direct Feedback:** Immediate confirmation of success or failure.
*   **No Frills:** Standard HTML forms without complex client-side logic.