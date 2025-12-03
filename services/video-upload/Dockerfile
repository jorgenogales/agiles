# ---- Backend Builder Stage ----
FROM golang:1.25.5-alpine3.22 AS backend-builder
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
RUN npm install
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