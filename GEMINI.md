# GEMINI.md - Go & GCP Best Practices for Agile Video Metadata Generation

This document outlines the key architectural and coding best practices to follow for the "Agile Video Metadata Generation" project. Adhering to these standards will ensure a scalable, maintainable, and robust system on Google Cloud Platform.

## 1. General Go Best Practices

*   **Idiomatic Go:** Write clean, simple, and readable Go code. Follow the principles outlined in [Effective Go](https://go.dev/doc/effective_go).
*   **Error Handling:**
    *   **Always check errors.** Do not ignore them (e.g., `_`).
    *   Use the `errors` package for simple errors and custom error types for more complex scenarios where you need to pass more context.
    *   Wrap errors to provide context using `fmt.Errorf("service: operation failed: %w", err)`. This preserves the original error for inspection.
*   **Concurrency:**
    *   Leverage Goroutines for concurrent operations, especially for I/O-bound tasks like calling external APIs (Gemini, GCS).
    *   Use channels for communication between goroutines.
    *   Use `sync.WaitGroup` to wait for a collection of goroutines to finish.
    *   Be mindful of race conditions. Use the `-race` flag during development and testing (`go test -race`).
*   **Dependency Management:** Use Go Modules (`go.mod`/`go.sum`) to manage dependencies.

## 2. Microservices in Go

*   **Project Structure:** Organize each microservice with a clear and consistent directory structure. A good starting point is the [Standard Go Project Layout](https://github.com/golang-standards/project-layout), but adapt it to the needs of each service.
    ```
    /cmd          # Main applications for your project
    /internal     # Private application and library code
    /pkg          # Public library code
    go.mod
    ```
*   **Configuration:**
    *   Externalize configuration. Do not hardcode values like GCS bucket names, project IDs, or API keys in the code.
    *   Use environment variables for configuration. Consider using a library like `viper` to manage them.
*   **Logging:**
    *   Use a structured logging library (e.g., `slog` from the standard library, or `zerolog`, `zap`).
    *   Log in JSON format. This makes logs easily searchable and analyzable in Google Cloud Logging.
    *   Include a request ID or correlation ID in every log message to trace requests across microservices.
*   **Health Checks:**
    *   Implement `/healthz` (liveness) and `/readyz` (readiness) endpoints in each service.
    *   **Liveness Probe:** Should return `200 OK` if the service is running. A failure indicates the container should be restarted.
    *   **Readiness Probe:** Should return `200 OK` if the service is ready to accept traffic (e.g., has a database connection, is fully initialized). A failure will remove the pod from the service load balancer.

## 3. GCP Services Integration

*   **Authentication (Workload Identity):**
    *   **DO NOT** use service account JSON keys.
    *   Configure GKE with **Workload Identity** to associate a Kubernetes Service Account (KSA) with a Google Service Account (GSA).
    *   Pods running with the KSA will automatically authenticate as the GSA when using Google Cloud client libraries. This is the most secure and recommended method.
*   **Google Cloud Storage (GCS):**
    *   Use the official `cloud.google.com/go/storage` client library.
    *   **Object Naming:** Use a predictable and structured naming convention. For metadata, `gs://pepito-video-metadata/{videoId}.json` is a good pattern.
    *   **Error Handling:** Handle specific GCS errors, such as `storage.ErrObjectNotExist`, gracefully.
    *   **Streaming:** For the `Video Upload Service`, stream uploads directly to GCS to avoid loading the entire file into memory. This is more memory-efficient and scalable.
*   **Vertex AI (Gemini API):**
    *   Use the official `cloud.google.com/go/vertexai/genai` client library.
    *   **Prompt Engineering:** Design a single, robust prompt that instructs Gemini to return a structured JSON object. This is more efficient than multiple calls. Example:
        ```json
        {
          "titles": ["..."],
          "synopsis": "...",
          "thumbnail_timestamps": [15, 45, 120]
        }
        ```
    *   **Error Handling & Retries:** Implement exponential backoff for retries on transient errors (e.g., `503 Service Unavailable`).

## 4. GKE & Docker

*   **Dockerfile Best Practices for Go:**
    *   Use a [multi-stage build](https://docs.docker.com/build/building/multi-stage/) to create a small, secure production image.
    *   The first stage (builder) compiles the Go binary with all the necessary build tools.
    *   The final stage copies **only the compiled binary** into a minimal base image (e.g., `gcr.io/distroless/static-debian11` or `alpine`). This reduces the image size and attack surface.
    ```dockerfile
    # ---- Builder Stage ----
    FROM golang:1.21-alpine AS builder
    WORKDIR /app
    COPY go.mod go.sum ./
    RUN go mod download
    COPY . .
    # Statically link the binary
    RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main ./cmd/my-service/

    # ---- Final Stage ----
    FROM gcr.io/distroless/static-debian11
    WORKDIR /app
    COPY --from=builder /app/main .
    # COPY config.yaml . # If using config files
    EXPOSE 8080
    ENTRYPOINT ["/app/main"]
    ```
*   **GKE Deployment Configuration:**
    *   **Resource Requests and Limits:** Always define `requests` and `limits` for CPU and memory in your `deployment.yaml`. This ensures proper scheduling and resource management.
    *   **Horizontal Pod Autoscaler (HPA):** Use an HPA for stateless services like the `Frame Extraction Service` to automatically scale based on CPU or memory usage.
    *   **Liveness and Readiness Probes:** Configure probes for each deployment to point to the `/healthz` and `/readyz` endpoints.

## 5. API Design

*   **RESTful Principles:** Design APIs to be stateless. Use standard HTTP methods (`GET`, `POST`, `PUT`).
*   **Structured JSON:** All API responses should be in JSON.
*   **Versioning:** Consider versioning your API from the start (e.g., `/api/v1/videos`). This makes future changes easier to manage.
*   **Status Reporting:** The polling mechanism is a good start. For the `GET /api/videos/{videoId}/metadata` endpoint, include a clear status field (e.g., `processing`, `completed`, `failed`).
    ```json
    {
      "status": "completed",
      "metadata": {
        "titles": [...],
        "synopsis": "...",
        "thumbnail_urls": [...]
      }
    }
    ```
