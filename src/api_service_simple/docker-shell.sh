#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define environment variables
export BASE_DIR=$(pwd)
export PERSISTENT_DIR=$(pwd)/../persistent-folder/
export SECRETS_DIR=$(pwd)/../secrets/
export IMAGE_NAME="gain-rag-api-service"

# Create a Docker network if it doesn't already exist
docker network inspect gain-rag-network >/dev/null 2>&1 || docker network create gain-rag-network

# Build the Docker image with the specified Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run the Docker container, mapping volumes and ports
docker run --rm --name $IMAGE_NAME -p 9000:9000 \
  -v "$SECRETS_DIR":/secrets \
  -v "$PERSISTENT_DIR":/persistent \
  -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json" \
  --network gain-rag-network \
  $IMAGE_NAME