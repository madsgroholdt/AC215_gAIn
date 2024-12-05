#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets/
export GCP_PROJECT="ac215-final-project"
export GCS_BUCKET_NAME="gain-ml-pipeline"
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/finetuning-service-account.json"
export GCP_SERVICE_ACCOUNT="finetuning-service-account@ac215-final-project.iam.gserviceaccount.com"
export LOCATION="us-central1"
export IMAGE_NAME="model-finetuning"

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
$IMAGE_NAME
