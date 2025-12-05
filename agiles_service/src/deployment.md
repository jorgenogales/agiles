# Deployment Instructions for Simple Video Upload System

This folder contains all the necessary files to deploy the Simple Video Upload System to Google Kubernetes Engine (GKE).

## Prerequisites

1.  **Google Cloud Project**: Ensure you have an active GCP project.
2.  **Tools Installed**:
    *   `gcloud` CLI
    *   `kubectl`
3.  **APIs Enabled**:
    *   Kubernetes Engine API
    *   Cloud Build API
    *   Google Container Registry API (or Artifact Registry)

## Configuration

### Variables
*   **Project ID**: Replace `YOUR_PROJECT_ID` with your actual Google Cloud Project ID.
*   **LDAP**: Your unique user identifier. This will be used to prefix resource names.
*   **Bucket Name**: `[LDAP]-agiles-video-upload` (e.g., `jorgenogales-agiles-video-upload`).
*   **Cluster Name**: `[LDAP]-agiles-cluster` (e.g., `jorgenogales-agiles-cluster`).

## Deployment Steps

### 1. Setup Environment Variables

Set these variables in your terminal for convenience:

```bash
export PROJECT_ID=$(gcloud config get-value project)
# IMPORTANT: Change "your-ldap" to your actual LDAP or preferred unique identifier.
export LDAP=$(gcloud config get-value account | sed 's/@.*//' | tr -d '.')
export IMAGE_NAME="gcr.io/${PROJECT_ID}/${LDAP}-agiles-upload-service:latest"
export CLUSTER_NAME="${LDAP}-agiles-cluster"
export ZONE="europe-southwest1" # Change to your preferred zone
export BUCKET_NAME="${LDAP}-agiles-video-upload"
```

**Before proceeding, ensure you have your environment variables set. We will generate the `deployment.yaml` file from the template in step 4.**
**Get Cluster Credentials:**
```bash
gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE}
```

**Create GCS Bucket:**
```bash
gcloud storage buckets create gs://${BUCKET_NAME} --location=EU
```

### 3. Build and Push Docker Image

Navigate to this directory (`agiles-upload-service`) and submit the build:

```bash
gcloud builds submit --tag ${IMAGE_NAME} .
```

### 4. Deploy to GKE

**Generate the Manifest:**
Generate `deployment.yaml` from `deployment.yaml.template` substituting the variables:
```bash
sed -e "s/YOUR_PROJECT_ID/${PROJECT_ID}/g" \
    -e "s/\[LDAP\]/${LDAP}/g" \
    -e "s/${LDAP}-agiles-video-upload/${BUCKET_NAME}/g" \
    deployment.yaml.template > deployment.yaml
```

**Apply the Deployment:**
```bash
kubectl apply -f deployment.yaml
```

### 5. Access the Application

Once the Ingress is provisioned (this may take a few minutes), you can get its external IP address:

```bash
kubectl get ingress ${LDAP}-agiles-upload-ingress
```

Note the `ADDRESS` from the output. You will need to configure your DNS to point `[LDAP]-agiles.example.com` (or whatever hostname you chose in `deployment.yaml`) to this IP address.

Once DNS is propagated, navigate to `http://[LDAP]-agiles.example.com` in your browser to test the upload.

## Cleanup

To remove created resources:
```bash
kubectl delete -f deployment.yaml
gcloud container clusters delete ${CLUSTER_NAME} --zone ${ZONE}
gcloud storage rm -r gs://${BUCKET_NAME}
```
