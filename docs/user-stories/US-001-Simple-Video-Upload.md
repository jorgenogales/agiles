# User Story: Simple Video Upload

**ID:** US-001-Simplified
**Feature:** Video Upload to GCS

## User Story
As a **Developer/User**,
I want to **upload a video file via a simple interface**,
So that **it is stored in a Google Cloud Storage (GCS) bucket with a structured folder organization.**

## Acceptance Criteria
1.  **Upload Interface:**
    *   A simple web page (`/upload`) with a file input and a submit button.
    *   Accepts standard video formats (e.g., .mp4).

2.  **Storage Structure:**
    *   Upon upload, a unique UUID is generated.
    *   The file is stored in the GCS bucket `agiles-video-upload`.
    *   The path format is: `gs://agiles-video-upload/<uuid>/video.mp4`.

3.  **Confirmation:**
    *   After a successful upload, the user receives a confirmation message displaying the generated UUID and the GCS path.
