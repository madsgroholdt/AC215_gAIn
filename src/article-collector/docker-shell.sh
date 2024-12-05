#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets/
export GCP_PROJECT="ac215-final-project"
export GCS_BUCKET_NAME="gain-ml-pipeline"
export IMAGE_NAME="article-collector"

docker build -t $IMAGE_NAME -f Dockerfile .

# Run Docker container
docker run --rm -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$BASE_DIR"/articles:/articles \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-pipeline.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
$IMAGE_NAME
