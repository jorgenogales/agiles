# US-002: Video List Dashboard

## Description
As a user, I want to view a list of all uploaded videos so that I can browse the content library and choose a video to watch.

## Priority
High (Core MVP Feature)

## Dependencies
- US-001 (Video Upload & Processing) - to populate the data.
- GCS `metadata/` directory containing JSON files.

## Acceptance Criteria

### 1. Data Retrieval
- [ ] The application connects to the GCS bucket.
- [ ] The system iterates through all files located in the `metadata/` directory.
- [ ] The system downloads/reads the content of each JSON metadata file.

### 2. UI Display
- [ ] A webpage (Dashboard/Home) displays the list of videos.
- [ ] For each video, the following information is displayed:
    - **Thumbnail:** The image generated in US-001 (loaded via its GCS URL).
    - **Summary:** A snippet or the full text of the AI-generated summary.
    - **Tags:** Display the tags as badges or a list.
    - **Date:** (Optional) The upload date.

### 3. Interaction
- [ ] Clicking on a video card/item navigates the user to the Video Player View (US-003) for that specific video.

## Technical Notes
- **Endpoint:** `GET /` or `GET /videos`
- **Performance:** Be aware that listing and reading individual JSON files from GCS is an O(N) operation. For MVP, this is acceptable, but it may be slow if many videos exist.
- **Ordering:** Ideally, sort by `created_at` (newest first) if possible within the file listing constraints or by sorting the loaded list in memory.
