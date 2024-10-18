#!/bin/bash

# Script to deploy the proxy service to GCP
set -euo pipefail

PROJECT_ID=${PROJECT_ID:-your-gcp-project-id}
IMAGE_NAME=${IMAGE_NAME:-gcr.io/$PROJECT_ID/proxy-service:latest}
REGION=${REGION:-us-central1}

function check_prerequisites() {
    echo "Checking prerequisites..."
    if ! command -v gcloud &> /dev/null; then
        echo "gcloud not found. Please install Google Cloud SDK."
        exit 1
    fi
}

function build_and_push_image() {
    echo "Building and pushing Docker image $IMAGE_NAME..."
    docker build -t "$IMAGE_NAME" .
    docker push "$IMAGE_NAME"
}

function deploy_to_gcp() {
    echo "Deploying to GCP Cloud Run..."
    gcloud run deploy proxy-service \
        --image "$IMAGE_NAME" \
        --platform managed \
        --region "$REGION" \
        --allow-unauthenticated
}

check_prerequisites
build_and_push_image
deploy_to_gcp

echo "Deployment to GCP completed successfully."
