#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Read the settings file
source env.dev

export IMAGE_NAME="data-preprocessing"

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-p 8080:8080 \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e BUCKET_CSV_OUTPUT_FOLDER=$BUCKET_CSV_OUTPUT_FOLDER \
-e BUCKET_TXT_OUTPUT_FOLDER=$BUCKET_TXT_OUTPUT_FOLDER \
-e PROJECT_NUM=$PROJECT_NUM \
-e SECRET_NAME=$SECRET_NAME \
$IMAGE_NAME
