package gcs

import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/storage"
)

type Client struct {
	bucketName string
	client     *storage.Client
}

func NewClient(ctx context.Context, bucketName string) (*Client, error) {
	client, err := storage.NewClient(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to create storage client: %w", err)
	}

	return &Client{
		bucketName: bucketName,
		client:     client,
	}, nil
}

func (c *Client) Upload(ctx context.Context, objectName string, data io.Reader) error {
	wc := c.client.Bucket(c.bucketName).Object(objectName).NewWriter(ctx)
	
	// Stream the data to GCS
	if _, err := io.Copy(wc, data); err != nil {
		wc.Close() // Attempt to close to clean up
		return fmt.Errorf("failed to stream data to GCS: %w", err)
	}

	// Close the writer to complete the upload
	if err := wc.Close(); err != nil {
		return fmt.Errorf("failed to close GCS writer: %w", err)
	}

	return nil
}

func (c *Client) Close() error {
	return c.client.Close()
}
