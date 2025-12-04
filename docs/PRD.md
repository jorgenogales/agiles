# Product Requirements Document (PRD) - Video Processing MVP

## 1. Introduction
This document outlines the requirements for a Minimum Viable Product (MVP) video processing application. The goal is to demonstrate a "disruptive" solution that leverages Generative AI for video analysis, targeting a presentation to the Board of Directors.

## 2. Objectives
-   **Primary Goal:** Create a simple web application to upload, process, and view videos.
-   **Key Metrics:** Successful demonstration of the flow (Upload -> AI Process -> View).
-   **Deadline:** End of Week (EOW).

## 3. Functional Requirements

### 3.1. Video Upload
-   **FR-1:** The application must allow users to upload a video file.
-   **FR-2:** Uploaded videos must be stored in **Google Cloud Storage (GCS)**.

### 3.2. Video Processing (AI & Other)
-   **FR-3:** The system must utilize **Gemini on Vertex AI** to analyze the uploaded video.
-   **FR-4:** The system must generate a **text summary** of the video content using Gemini.
-   **FR-5:** The system must generate relevant **tags** for the video using Gemini.
-   **FR-6:** The system must generate a **thumbnail** image for the video (via a dedicated video processing tool/library, not Gemini).
-   **FR-7:** All generated artifacts (summary, tags, thumbnail) must be stored in GCS.

### 3.3. User Interface
-   **FR-8:** **Video List:** A webpage must list all available videos stored in the system.
-   **FR-9:** **Video Player:** Users must be able to click on a video from the list to play it.
-   **FR-10:** The player view should ideally display the generated metadata (summary, tags).

## 4. Technical Constraints & Stack
-   **Cloud Provider:** Google Cloud Platform (GCP).
-   **Storage:** Google Cloud Storage (GCS).
-   **AI Services:** Vertex AI (Gemini models).

## 5. Assumptions
-   The user has the necessary GCP permissions and credentials.
-   The "thumbnail generation" will be handled by a dedicated video processing component/library.

## 6. Source
-   Based on email directives from Brock L. Chain (CEO).
