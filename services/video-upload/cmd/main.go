package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"video-upload/internal/config"
	"video-upload/internal/gcs"
	"video-upload/internal/handler"
	"video-upload/internal/orchestrator"
)

func main() {
	// 1. Setup Logging
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	slog.SetDefault(logger)

	// 2. Load Configuration
	cfg, err := config.Load()
	if err != nil {
		slog.Error("Failed to load configuration", "error", err)
		os.Exit(1)
	}

	// 3. Initialize GCS Client
	ctx := context.Background()
	gcsClient, err := gcs.NewClient(ctx, cfg.GCSBucketName)
	if err != nil {
		slog.Error("Failed to initialize GCS client", "error", err)
		os.Exit(1)
	}
	defer gcsClient.Close()

	// 4. Initialize Orchestrator Client
	orchClient := orchestrator.NewClient(cfg.OrchestratorURL)

	// 5. Setup Router/Handler
	uploadHandler := handler.NewUploadHandler(gcsClient, orchClient, cfg.GCSBucketName)
	mux := http.NewServeMux()
	mux.Handle("/api/videos/upload", uploadHandler)
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("ok"))
	})
	mux.HandleFunc("/readyz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("ok"))
	})

	// Serve static frontend files
	mux.Handle("/", http.FileServer(http.Dir("./static")))

	srv := &http.Server{
		Addr:    ":" + cfg.Port,
		Handler: mux,
	}

	// 6. Start Server
	go func() {
		slog.Info("Starting server", "port", cfg.Port)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			slog.Error("Server failed", "error", err)
			os.Exit(1)
		}
	}()

	// 7. Graceful Shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	slog.Info("Shutting down server...")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		slog.Error("Server forced to shutdown", "error", err)
		os.Exit(1)
	}

	slog.Info("Server exited properly")
}
