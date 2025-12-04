# User Story: Video Upload & AI Processing

**ID:** US-001
**Feature:** Backend AI Pipeline & Upload Portal

## User Story
As a **Content Creator**,
I want to **upload a video file through a simple web interface**,
So that **the system automatically generates an optimized title, synopsis, and thumbnail without manual effort.**

## Acceptance Criteria
1.  **Upload Interface:**
    *   The user accesses a dedicated `/upload` page.
    *   The page provides a form to select a video file from the local device.
    *   Supported formats should include standard video types (e.g., .mp4).

2.  **Synchronous Processing:**
    *   Upon clicking "Upload", the UI shows a loading state indicating processing is active.
    *   The system uploads the raw video to a GCS bucket (`agiles-video-upload`) under a unique UUID.
    *   The system synchronously calls Vertex AI (`gemini-2.5-flash`) to analyze the video content.

3.  **AI Generation:**
    *   **Title:** A catchy, SEO-friendly title is generated.
    *   **Synopsis:** A coherent, engaging summary is generated.
    *   **Thumbnail:** The system identifies the best timestamp, extracts the frame, and saves it as `thumbnail.jpg`.

4.  **Completion & Storage:**
    *   A `metadata.json` file containing the title, synopsis, and GCS URLs is saved in the same GCS folder.
    *   Upon successful completion, the user is automatically redirected to the Video Detail View (US-003) for the uploaded video.

## Technical Notes
*   Use Python/Flask for the backend handler.
*   Use `OpenCV` or similar for frame extraction based on Vertex AI timestamps.
*   Ensure the GKE service account has permissions to write to GCS and invoke Vertex AI.
