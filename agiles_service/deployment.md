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


## Deployment Steps

### 1. Setup Environment Variables

Set these variables in your terminal for convenience:

```bash
export PROJECT_ID=$(gcloud config get-value project)
export LDAP=$(gcloud config get-value account | sed 's/@.*//' | tr -d '.')
export IMAGE_NAME="gcr.io/${PROJECT_ID}/${LDAP}-agiles-upload-service:latest"
export CLUSTER_NAME="agiles-cluster"
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

Navigate to this directory (`agiles-service`) and submit the build:

```bash
gcloud builds submit --tag ${IMAGE_NAME} .
```

### 4. Deploy to GKE

**Generate the Manifest:**
Generate `deployment.yaml` from `deployment.yaml.template` by substituting the environment variables

***For Linux and macOS:***
```bash
sed -e "s/YOUR_PROJECT_ID/${PROJECT_ID}/g" \
    -e "s/\[LDAP\]/${LDAP}/g" \
    -e "s/${LDAP}-agiles-video-upload/${BUCKET_NAME}/g" \
    k8s/deployment.yaml.template > k8s/deployment.yaml
```

***For Windows (using PowerShell):***
```powershell
(Get-Content -Path k8s/deployment.yaml.template) -replace "YOUR_PROJECT_ID", $env:PROJECT_ID -replace "\[LDAP\]", $env:LDAP -replace "${env:LDAP}-agiles-video-upload", $env:BUCKET_NAME | Set-Content -Path k8s/deployment.yaml
```

**Apply the Deployment:**
```bash
kubectl apply -f k8s/deployment.yaml
```

### 5. Access the Application

Once the Ingress is provisioned (this may take a few minutes), you can get its external IP address to access the service:

```bash
kubectl get ingress ${LDAP}-agiles-upload-ingress
```
