# User Story: Display Enriched Video List

## Description
**As a** User,
**I want** to see the AI-generated title, description, and tags, along with the first-frame thumbnail, in the video list,
**So that** I can easily browse and choose content based on rich, automatically generated information.

## Acceptance Criteria
- [ ] The Video List page (`/`) is updated to display a grid or detailed list of videos.
- [ ] For each video item, the following is displayed:
    -   The **Thumbnail** image (the first frame, served via GCS).
    -   The AI-generated **Title**.
    -   The AI-generated **Description** (truncated if necessary).
    -   The AI-generated **Tags** (displayed as chips or a comma-separated list).
- [ ] The application retrieves this data from the `metadata.json` and `thumbnail.png` files stored in GCS for each video.
- [ ] If any piece of enriched data (metadata or thumbnail) is missing, the system falls back gracefully (e.g., showing the video's original filename, a placeholder image, or "No description available").
- [ ] The user interface is responsive and designed to "scream engagement," aligning with "Web 4.0" aesthetics.

## Definition of Done
- [ ] Frontend templates for the video list are updated to render cards/items with images and text elements.
- [ ] Backend logic in the Flask app is updated to fetch and parse `metadata.json` and generate URLs for `thumbnail.png` for each video.
- [ ] Necessary CSS/styles are applied to ensure a modern and visually appealing display.
- [ ] Manual verification: The list page loads correctly, displaying the enriched data (thumbnail, title, description, tags) for uploaded videos.
