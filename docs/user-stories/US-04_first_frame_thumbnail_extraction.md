# User Story: First Frame Thumbnail Extraction

## Description
**As a** Content Manager,
**I want** a visual thumbnail for each uploaded video to be automatically generated from its first frame,
**So that** users have a clear visual representation of the video content in the list without relying on AI image generation.

## Acceptance Criteria
- [ ] After a video file is uploaded to GCS, the system uses standard Python libraries to extract the **first frame** of the video.
- [ ] The extracted frame is saved as an image file (`thumbnail.png`) in the GCS bucket under the video's unique ID folder.
- [ ] The extraction process is efficient and does not significantly delay the upload workflow.
- [ ] The process handles errors gracefully (e.g., if frame extraction fails, a default placeholder thumbnail is used).

## Definition of Done
- [ ] Integration with a suitable Python video processing library (e.g., `moviepy`, `opencv-python`) is implemented.
- [ ] Logic to extract the first frame and save it as `thumbnail.png` to GCS is implemented.
- [ ] Unit tests for the thumbnail extraction logic are written and passing.
- [ ] Manual verification: Upload a video and confirm `thumbnail.png` appears in GCS, correctly showing the first frame of the video.
