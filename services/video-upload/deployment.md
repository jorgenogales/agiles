# GKE Deployment Guide: Video Upload Service

This document outlines the steps to build, containerize, and deploy the `video-upload` service to Google Kubernetes Engine (GKE) using Google Cloud Build for continuous integration.

## 1. Prerequisites

*   **Google Cloud Project:** Configured with billing enabled.
*   **GKE Cluster:** A running GKE cluster.
*   **Google Container Registry (GCR) or Artifact Registry (GAR):** Enabled in your project.
*   **Cloud Build API:** Enabled in your project.
*   **`gcloud` CLI:** Authenticated and configured with your project.
*   **`kubectl` CLI:** Configured to connect to your GKE cluster.
*   **Service Account for Workload Identity:**
    *   A GCP Service Account (GSA) with necessary permissions (e.g., `roles/storage.objectAdmin` for GCS, permission to call Orchestrator).
    *   A Kubernetes Service Account (KSA) linked to the GSA.

## 2. Containerization (Dockerfile)

The `video-upload` service is containerized using a multi-stage `Dockerfile` to create a minimal and secure production image. It builds both the Go backend and the React frontend, serving them from a single container.

**`services/video-upload/Dockerfile`**
```dockerfile
# ---- Backend Builder Stage ----
FROM golang:1.21-alpine AS backend-builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
# Statically link the binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main ./cmd/main.go

# ---- Frontend Builder Stage ----
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# ---- Final Stage ----
FROM gcr.io/distroless/static-debian11
WORKDIR /app
COPY --from=backend-builder /app/main .
# Copy the built frontend assets to a directory the Go server can serve
COPY --from=frontend-builder /app/frontend/dist ./static
EXPOSE 8080
ENTRYPOINT ["/app/main"]
```

## 3. Building with Google Cloud Build

We will use Google Cloud Build to build the Docker image and push it to Google Container Registry (GCR).

**`services/video-upload/cloudbuild.yaml`**
```yaml
steps:
  # Build the Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/${PROJECT_ID}/video-upload-service:${COMMIT_SHA}', '.']
    dir: 'services/video-upload' # Specify the working directory for the build
  # Push the Docker image to Google Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/${PROJECT_ID}/video-upload-service:${COMMIT_SHA}']
images:
  - 'gcr.io/${PROJECT_ID}/video-upload-service:${COMMIT_SHA}'
```

To trigger Cloud Build:

```bash
gcloud builds submit --config services/video-upload/cloudbuild.yaml ./services/video-upload/.
```
Replace `services/video-upload` at the end with `.` if you run this from the `video-upload` directory.

## 4. GKE Deployment

The service will be deployed to GKE using Kubernetes manifests.

### 4.1. Kubernetes Deployment (`services/video-upload/k8s/deployment.yaml`)

This manifest defines the `Deployment` for the `video-upload` service, including resource limits, liveness/readiness probes, and Workload Identity configuration.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: video-upload-service
  labels:
    app: video-upload-service
spec:
  replicas: 1 # Adjust as needed
  selector:
    matchLabels:
      app: video-upload-service
  template:
    metadata:
      labels:
        app: video-upload-service
    spec:
      serviceAccountName: video-upload-ksa # Kubernetes Service Account for Workload Identity
      containers:
        - name: video-upload-service
          image: gcr.io/${GCP_PROJECT_ID}/video-upload-service:${IMAGE_TAG} # Replace with your project ID and image tag (e.g., COMMIT_SHA)
          ports:
            - containerPort: 8080
          env:
            - name: PORT
              value: "8080"
            - name: GCP_PROJECT_ID
              value: "${GCP_PROJECT_ID}" # Automatically injected by GKE if Workload Identity is used correctly, or explicitly set.
            - name: GCS_BUCKET_NAME
              value: "pepito-uploaded-videos" # As per implementation plan
            - name: ORCHESTRATOR_SERVICE_URL
              value: "http://video-processing-orchestrator-service:8080" # Internal ClusterIP Service URL
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
```
**Workload Identity Setup (Pre-deployment):**
Ensure your GSA and KSA are set up and linked:
```bash
gcloud iam service-accounts create video-upload-gsa \
    --display-name "Service Account for Video Upload Service"

gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
    --member "serviceAccount:video-upload-gsa@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
    --role "roles/storage.objectAdmin" # Or a more granular role

gcloud iam service-accounts add-iam-policy-binding \
    video-upload-gsa@${GCP_PROJECT_ID}.iam.gserviceaccount.com \
    --role "roles/iam.workloadIdentityUser" \
    --member "serviceAccount:${GCP_PROJECT_ID}.svc.id.goog[default/video-upload-ksa]" # Assuming 'default' namespace and KSA name 'video-upload-ksa'

kubectl create serviceaccount video-upload-ksa --namespace default # Or your target namespace

kubectl annotate serviceaccount video-upload-ksa \
    --namespace default \
    iam.gke.io/gcp-service-account=video-upload-gsa@${GCP_PROJECT_ID}.iam.gserviceaccount.com
```

### 4.2. Kubernetes Service (`services/video-upload/k8s/service.yaml`)

This manifest exposes the `video-upload` Deployment internally within the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: video-upload-service
  labels:
    app: video-upload-service
spec:
  selector:
    app: video-upload-service
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
  type: ClusterIP # Internal service. Use Ingress for external exposure.
```

### 4.3. Kubernetes Ingress (`services/video-upload/k8s/ingress.yaml`)

As per the implementation plan, the `Video Upload Service` needs to be exposed to the internet.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: video-upload-ingress
  annotations:
    # Example: Use a GKE Managed Certificate for SSL. Replace with your domain.
    # networking.gke.io/managed-certificates: "your-managed-certificate-name"
    kubernetes.io/ingress.class: "gce" # Use GKE's default Ingress controller
    # Example: Use external IP
    # ingress.gcp.kubernetes.io/pre-shared-certs: "your-ssl-certificate-name"
    # Or for a simple HTTP ingress (no SSL) remove the above annotations
spec:
  # tls:
  # - secretName: your-tls-secret # If using a manually managed certificate
  #   hosts:
  #     - yourdomain.com
  rules:
  - http:
      paths:
      - path: /api/videos/upload
        pathType: Prefix
        backend:
          service:
            name: video-upload-service
            port:
              number: 8080
```

### 4.4. Deploy to GKE

Navigate to the `services/video-upload/k8s` directory and apply the manifests:

```bash
cd services/video-upload/k8s
kubectl apply -f .
```

This will create the Deployment, Service, and Ingress resources in your GKE cluster. Remember to replace placeholders like `${GCP_PROJECT_ID}` and `${IMAGE_TAG}` with actual values.

