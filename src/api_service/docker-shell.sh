#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="gain-rag-api-service"
export BASE_DIR=$(pwd)
export PERSISTENT_DIR=$(pwd)/../persistent-folder/
export SECRETS_DIR=$(pwd)/../secrets/
export GCP_PROJECT="ac215-final-project"
export GCS_BUCKET_NAME="gain-bucket"
export BUCKET_CSV_OUTPUT_FOLDER="raw_user_data"
export BUCKET_TXT_OUTPUT_FOLDER="processed_user_data"
export PROJECT_NUM="1059187665772"
export SECRET_NAME="strava_config"
export CHROMADB_HOST="gain-vector-db"
export CHROMADB_PORT=8000

# Create the network if we don't have it yet
docker network inspect gain-rag-network >/dev/null 2>&1 || docker network create gain-rag-network

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
# M1/2 chip macs use this line
docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$PERSISTENT_DIR":/persistent \
-p 9000:9000 \
-e DEV=1 \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e BUCKET_CSV_OUTPUT_FOLDER=$BUCKET_CSV_OUTPUT_FOLDER \
-e BUCKET_TXT_OUTPUT_FOLDER=$BUCKET_TXT_OUTPUT_FOLDER \
-e PROJECT_NUM=$PROJECT_NUM \
-e SECRET_NAME=$SECRET_NAME \
-e CHROMADB_HOST=$CHROMADB_HOST \
-e CHROMADB_PORT=$CHROMADB_PORT \
--network gain-rag-network \
$IMAGE_NAME
