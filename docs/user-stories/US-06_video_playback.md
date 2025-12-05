# User Story: Video Playback

## Description
**As a** User,
**I want** to be able to click on a video in the list and watch it in a dedicated player view,
**So that** I can consume the content directly within the application, disrupting attention spans effectively.

## Acceptance Criteria
- [ ] Clicking on a video item (or a dedicated "Watch" button) in the enriched video list navigates the user to a specific video playback page (e.g., `/watch/{video_id}`).
- [ ] The video playback page features a prominent HTML5 video player.
- [ ] The player successfully loads and plays the video file directly from GCS (using a secure, temporary, or public URL as appropriate).
- [ ] The page prominently displays the AI-generated **Title**, **Description**, and **Tags** associated with the video, alongside the player.
- [ ] User controls for playback (play/pause, volume, seek, fullscreen) are available in the player.
- [ ] A clear navigation element (e.g., a "Back to List" button/link) is provided to return to the main video list.

## Definition of Done
- [ ] A new Flask route for video playback (e.g., `/watch/<string:video_id>`) is implemented.
- [ ] A new HTML template for the video playback page is created, incorporating an HTML5 `<video>` element.
- [ ] Backend logic to fetch the video's metadata (`metadata.json`) and generate a streamable URL for the video file from GCS is implemented.
- [ ] Manual verification:
    -   Navigate to a video's watch page.
    -   Confirm the video plays correctly.
    -   Confirm the AI-generated metadata (Title, Description, Tags) is displayed.
    -   Confirm navigation back to the list works.
