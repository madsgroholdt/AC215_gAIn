#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
source ../env.dev
export IMAGE_NAME="article-collector"

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run Docker container
docker run --rm -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$BASE_DIR"/articles:/articles \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
$IMAGE_NAME
