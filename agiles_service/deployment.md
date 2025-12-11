# Deployment Instructions for Simple Video Upload System

This folder contains all the necessary files to deploy the Simple Video Upload System to Google Kubernetes Engine (GKE).

## Prerequisites

1.  **Google Cloud Project**: Ensure you have an active GCP project.
2.  **Tools Installed**:
    *   `gcloud` CLI https://docs.cloud.google.com/sdk/docs/install-sdk
    *   `kubectl` gcloud components install kubectl

## Deployment Steps

### 1. Setup Environment Variables

Set these variables in your terminal.

***For Linux and macOS (in a Bash shell):***
```bash
export PROJECT_ID=$(gcloud config get-value project)
export LDAP=$(gcloud config get-value account | sed 's/@.*//' | tr -d '.')
export IMAGE_NAME="gcr.io/${PROJECT_ID}/${LDAP}-agiles-service:latest"
export CLUSTER_NAME="agiles-cluster"
export ZONE="europe-southwest1" # Change to your preferred zone
export BUCKET_NAME="${LDAP}-agiles-video-upload"
```

***For Windows (in a PowerShell terminal):***
```powershell
$env:PROJECT_ID = (gcloud config get-value project)
$env:LDAP = (gcloud config get-value account) -replace '@.*','' -replace '\.',''
$env:IMAGE_NAME = "gcr.io/$($env:PROJECT_ID)/$($env:LDAP)-agiles-service:latest"
$env:CLUSTER_NAME = "agiles-cluster"
$env:ZONE = "europe-southwest1" # Change to your preferred zone
$env:BUCKET_NAME = "$($env:LDAP)-agiles-video-upload"
```

**Before proceeding, ensure you have your environment variables set. We will generate the `deployment.yaml` file from the template in step 4.**

**Get Cluster Credentials:**
```bash
gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE}
```

**Create GCS Bucket:**
```bash
gcloud storage buckets create gs://${BUCKET_NAME} --location=EU
gcloud storage buckets add-iam-policy-binding gs://${BUCKET_NAME} --member="allUsers" --role="roles/storage.objectViewer"
```

### 2. Build and Push Docker Image

Navigate to this directory (`agiles-service`) and submit the build:

```bash
gcloud builds submit --tag ${IMAGE_NAME} .
```

### 3. Deploy to GKE

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

### 4. Access the Application

Once the Ingress is provisioned (this may take a few minutes), you can get its external IP address to access the service:

```bash
kubectl get ingress ${LDAP}-agiles-upload-ingress
```