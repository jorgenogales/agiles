package handler

import (
	"fmt"
	"log/slog"
	"net/http"
	"path/filepath"

	"github.com/google/uuid"
	"video-upload/internal/gcs"
	"video-upload/internal/orchestrator"
)

type UploadHandler struct {
	gcsClient          *gcs.Client
	orchestratorClient *orchestrator.Client
	bucketName         string
}

func NewUploadHandler(gcs *gcs.Client, orch *orchestrator.Client, bucketName string) *UploadHandler {
	return &UploadHandler{
		gcsClient:          gcs,
		orchestratorClient: orch,
		bucketName:         bucketName,
	}
}

func (h *UploadHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// 1. Parse Multipart Form
	// Limit upload size to 500MB for safety (adjust as needed)
	const maxUploadSize = 500 << 20 
	r.Body = http.MaxBytesReader(w, r.Body, maxUploadSize)
	if err := r.ParseMultipartForm(maxUploadSize); err != nil {
		slog.Error("Failed to parse multipart form", "error", err)
		http.Error(w, "File too large or invalid format", http.StatusBadRequest)
		return
	}

	file, header, err := r.FormFile("video")
	if err != nil {
		slog.Error("Failed to get file from form", "error", err)
		http.Error(w, "Invalid file", http.StatusBadRequest)
		return
	}
	defer file.Close()

	// 2. Generate Unique Filename
	ext := filepath.Ext(header.Filename)
	if ext == "" {
		ext = ".mp4" // Default to mp4 if no extension
	}
	videoID := uuid.New().String()
	objectName := fmt.Sprintf("%s%s", videoID, ext)

	slog.Info("Starting upload", "video_id", videoID, "filename", header.Filename)

	// 3. Upload to GCS
	ctx := r.Context()
	if err := h.gcsClient.Upload(ctx, objectName, file); err != nil {
		slog.Error("Failed to upload to GCS", "error", err, "video_id", videoID)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	gcsURI := fmt.Sprintf("gs://%s/%s", h.bucketName, objectName)
	slog.Info("Upload successful", "gcs_uri", gcsURI)

	// 4. Trigger Orchestrator
	if err := h.orchestratorClient.TriggerProcessing(ctx, gcsURI); err != nil {
		slog.Error("Failed to trigger orchestrator", "error", err, "video_id", videoID)
		// Even if orchestrator fails, the upload was successful. 
		// We might want to return 202 Accepted but indicate processing failure? 
		// For now, returning 500 as per "seamless workflow" expectation.
		http.Error(w, "Failed to start video processing", http.StatusBadGateway)
		return
	}

	w.WriteHeader(http.StatusCreated)
	fmt.Fprintf(w, `{"status": "uploaded", "video_id": "%s"}`, videoID)
}
