package orchestrator

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type Client struct {
	baseURL    string
	httpClient *http.Client
}

func NewClient(baseURL string) *Client {
	return &Client{
		baseURL: baseURL,
		httpClient: &http.Client{
			Timeout: 300 * time.Second, // Long timeout as the orchestrator might wait for processing
		},
	}
}

type ProcessVideoRequest struct {
	VideoGCSURI string `json:"video_gcs_uri"`
}

func (c *Client) TriggerProcessing(ctx context.Context, gcsURI string) error {
	reqBody := ProcessVideoRequest{
		VideoGCSURI: gcsURI,
	}

	jsonBody, err := json.Marshal(reqBody)
	if err != nil {
		return fmt.Errorf("failed to marshal request body: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, "POST", c.baseURL+"/process", bytes.NewBuffer(jsonBody))
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("failed to call orchestrator: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusAccepted {
		return fmt.Errorf("orchestrator returned non-OK status: %d", resp.StatusCode)
	}

	return nil
}
