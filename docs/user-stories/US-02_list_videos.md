# User Story: List Videos

## Description
**As a** User,
**I want to** see a list of all available videos,
**So that** I can browse the content stored in the system.

## Acceptance Criteria
- [ ] The user interface displays a list of uploaded videos.
- [ ] The application retrieves the list of objects from the configured Google Cloud Storage (GCS) bucket.
- [ ] The list item displays the unique ID associated with the video (extracted from the folder name).
- [ ] If the bucket is empty, a friendly "No videos found" message is displayed.
- [ ] The list is automatically updated after a new video is successfully uploaded.

## Definition of Done
- [ ] Feature implemented in the Flask application.
- [ ] Logic to list GCS blobs and extract IDs is implemented.
- [ ] Unit tests for the listing logic are written and passing.
- [ ] Manual test completed: Upload multiple videos and verify they all appear in the list.
