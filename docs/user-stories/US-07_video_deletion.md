# User Story: Video Deletion

## Description
**As a** User,
**I want** to delete a video I have uploaded,
**So that** I can remove unwanted content or manage my storage usage.

## Acceptance Criteria
- [ ] The Video List page and/or Video Playback page includes a "Delete" button for each video.
- [ ] Clicking "Delete" triggers a synchronous deletion process.
- [ ] The system permanently deletes the video file (`video.mp4`) from Google Cloud Storage (GCS).
- [ ] The system permanently deletes the associated metadata (`metadata.json`) and thumbnail (`thumbnail.png`) from GCS.
- [ ] The system removes the "directory" (prefix) associated with the video ID from GCS.
- [ ] After deletion, the user is redirected to the Video List page (if deleted from Playback) or the list is refreshed (if deleted from List), and the deleted video is no longer visible.
- [ ] A confirmation dialog confirms the user's intent before deletion.

## Definition of Done
- [ ] Backend route for video deletion (e.g., `DELETE /delete/<video_id>`) is implemented.
- [ ] Logic to list and delete all GCS blobs under the video's prefix is implemented.
- [ ] Frontend updated to include a Delete button with a confirmation step.
- [ ] Unit tests for the deletion logic are written and passing.
- [ ] Manual verification: Upload a video, delete it, and confirm all associated files are removed from the GCS bucket.
