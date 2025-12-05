# User Story: Upload Video

## Description
**As a** User,
**I want to** upload a video file through a web interface,
**So that** it is securely stored in the cloud for future access.

## Acceptance Criteria
- [ ] The user interface provides a clear "Upload" button or form.
- [ ] The user can select a video file (e.g., .mp4, .avi, .mov) from their local device.
- [ ] Upon submission, the application generates a unique random ID for the upload.
- [ ] The video file is uploaded to Google Cloud Storage (GCS) under the path `{random_id}/video.mp4`.
- [ ] The user is redirected to the video list page or sees a success message upon completion.
- [ ] Proper error handling is in place for failed uploads (e.g., network error, invalid file).

## Definition of Done
- [ ] Feature implemented in the Flask application.
- [ ] Integration with Google Cloud Storage is verified.
- [ ] Unit tests for the upload logic are written and passing.
- [ ] Manual test completed: Upload a video and verify its existence in the GCS bucket under the correct path structure.
