# US-003: Video Player View

## Description
As a user, I want to play a selected video and view its details so that I can watch the content and read the AI-generated insights.

## Priority
Medium (Essential for consuming content)

## Dependencies
- US-002 (Video List Dashboard) - source of navigation.
- GCS bucket with accessible video and metadata files.

## Acceptance Criteria

### 1. Video Playback
- [ ] The page contains a standard HTML5 video player.
- [ ] The video source is set to the GCS URL of the selected video.
- [ ] The user can play, pause, and seek through the video.
- [ ] The video player uses the generated thumbnail as the "poster" image before playback starts.

### 2. Metadata Display
- [ ] The page displays the full **AI-generated Summary** text clearly.
- [ ] The page displays the list of **Tags** associated with the video.

### 3. Navigation
- [ ] There is a clearly visible "Back to List" button or link to return to the Dashboard (US-002).

## Technical Notes
- **Endpoint:** `GET /watch/<video_id>` or `GET /video?id=<filename>`
- **Data Source:** The view can either re-fetch the specific metadata JSON from GCS based on the ID or receive the data passed from the List view (though re-fetching is more robust for direct linking).
- **Public Access:** Ensure GCS objects are strictly accessible by the application or signed URLs are used if the bucket is not public. (For MVP, assumptions in PRD might imply simpler access, but be mindful of permissions).
