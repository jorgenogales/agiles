# User Story: AI Metadata Generation

## Description
**As a** Product Owner,
**I want** every uploaded video to be automatically analyzed by Generative AI for textual metadata,
**So that** we can generate a title, description, and tags without manual input for improved content discoverability.

## Acceptance Criteria
- [ ] Immediately after a video file is uploaded to GCS, the system triggers an analysis request to Vertex AI using the **gemini-2.5-flash** model.
- [ ] **Cognitive Labeling:** The AI generates a click-maximizing **Title** and a generic **Description**.
- [ ] **Taxonomy:** The AI generates a list of relevant **Metadata Tags**.
- [ ] The generated metadata (Title, Description, Tags) is saved as a JSON file (`metadata.json`) in the GCS bucket under the video's unique ID folder.
- [ ] The process handles errors gracefully (e.g., if AI fails, default/placeholder metadata is used).

## Definition of Done
- [ ] Integration with Google Cloud Vertex AI is implemented using the `gemini-2.5-flash` model.
- [ ] Helper functions to construct the prompt and parse the AI response for text metadata are written.
- [ ] Logic to save the generated `metadata.json` to GCS is implemented.
- [ ] Unit tests for the prompt construction and response parsing are passed.
- [ ] Manual verification: Upload a video and confirm `metadata.json` appears in GCS with meaningful AI-generated content.
