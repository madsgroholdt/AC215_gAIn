#!/bin/bash

# set -e

export IMAGE_NAME="gain-ml-pipeline"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../secrets/
export GCP_PROJECT="ac215-final-project"
export GCS_BUCKET_NAME="gain-ml-pipeline"
export GCS_SERVICE_ACCOUNT="ml-pipeline@ac215-final-project.iam.gserviceaccount.com"
export GCP_REGION="us-central1"

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$BASE_DIR/../article-collector":/article-collector \
-v "$BASE_DIR/../article-processor":/article-processor \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-pipeline.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e GCS_SERVICE_ACCOUNT=$GCS_SERVICE_ACCOUNT \
-e GCP_REGION=$GCP_REGION \
$IMAGE_NAME
