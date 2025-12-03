package config

import (
	"fmt"
	"os"
)

type Config struct {
	Port            string
	GCPProjectID    string
	GCSBucketName   string
	OrchestratorURL string
}

func Load() (*Config, error) {
	cfg := &Config{
		Port:            os.Getenv("PORT"),
		GCPProjectID:    os.Getenv("GCP_PROJECT_ID"),
		GCSBucketName:   os.Getenv("GCS_BUCKET_NAME"),
		OrchestratorURL: os.Getenv("ORCHESTRATOR_SERVICE_URL"),
	}

	if cfg.Port == "" {
		cfg.Port = "8080"
	}
	if cfg.GCPProjectID == "" {
		return nil, fmt.Errorf("GCP_PROJECT_ID environment variable is required")
	}
	if cfg.GCSBucketName == "" {
		return nil, fmt.Errorf("GCS_BUCKET_NAME environment variable is required")
	}
	if cfg.OrchestratorURL == "" {
		return nil, fmt.Errorf("ORCHESTRATOR_SERVICE_URL environment variable is required")
	}

	return cfg, nil
}
