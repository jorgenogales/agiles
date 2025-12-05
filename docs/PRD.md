# Product Requirements Document (PRD) - Intelligent Asset Enrichment MVP

## 1. Introduction
This document outlines the requirements for the "Intelligent Asset Enrichment" MVP. The goal is to pivot from a simple repository to a system that utilizes Generative AI to extract value from video content, targeting a presentation to the Board of Directors.

## 2. Objectives
-   **Primary Goal:** Create a web application that uploads, analyzes, lists, and plays videos.
-   **Key Metrics:** Successful AI generation of metadata (Title, Description, Tags, Thumbnail) and video playback.
-   **Deadline:** End of Week (EOW).

## 3. Functional Requirements

### 3.1. Video Upload & Enrichment
-   **FR-1:** The application must allow users to upload a video file.
-   **FR-2:** Uploaded videos must be stored in **Google Cloud Storage (GCS)**.
-   **FR-3:** Upon upload, the system must use **Generative AI** to automatically generate:
    -   A click-maximizing **Title**.
    -   A generic **Description**.
    -   **Metadata Tags** (Taxonomy).
    -   The **first frame** of the video as a visual **Thumbnail** (extracted using standard Python libraries).

### 3.2. User Interface
-   **FR-4:** **Video List:** A webpage must list all available videos, displaying the AI-generated metadata (Title, Description, Tags) and Thumbnail.
-   **FR-5:** **Video Player:** Users must be able to click on a video to watch it in a dedicated player view.

## 4. Technical Constraints & Stack
-   **Cloud Provider:** Google Cloud Platform (GCP).
-   **Storage:** Google Cloud Storage (GCS).
-   **AI Service:** Google Cloud Vertex AI (Gemini).

## 5. Assumptions
-   The user has the necessary GCP permissions and credentials.
-   The uploaded videos are in a format supported by the AI service and web browsers.