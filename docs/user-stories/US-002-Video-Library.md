# User Story: Video Library Catalog

**ID:** US-002
**Feature:** Video Library (Catalog)

## User Story
As a **Content Creator**,
I want to **browse a visual list of all uploaded videos**,
So that **I can quickly find and review previously processed content.**

## Acceptance Criteria
1.  **Library View:**
    *   The user accesses a dedicated `/library` page.
    *   The system queries the GCS bucket (`agiles-video-upload`) to identify all processed videos (scans for `metadata.json` files).

2.  **Video Cards:**
    *   Videos are displayed in a grid or list layout.
    *   Each video card displays:
        *   The AI-generated **Thumbnail** (image).
        *   The AI-generated **Title**.
        *   A short **excerpt** of the synopsis (truncated if necessary).

3.  **Navigation:**
    *   Clicking on any video card navigates the user to the specific Video Detail View (US-003) for that item.

## Technical Notes
*   This operation reads directly from GCS.
*   Pagination or lazy loading may be considered for future iterations if the bucket grows large, but for now, listing all objects is acceptable.
