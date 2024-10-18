#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

echo "Starting script..."

# Set vairables
export BASE_DIR=$(pwd)
export PERSISTENT_DIR=$(pwd)/../persistent-folder/
export SECRETS_DIR=$(pwd)/../secrets/
export GCP_PROJECT="ac215-final-project"
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json"
export IMAGE_NAME="gain-rag-cli"

echo "BASE_DIR is set to $BASE_DIR"
echo "SECRETS_DIR is set to $SECRETS_DIR"
echo "GCP_PROJECT is set to $GCP_PROJECT"

# Create the network if we don't have it yet
echo "Checking/creating Docker network..."
docker network inspect gain-rag-network >/dev/null 2>&1 || docker network create gain-rag-network

# Build the image based on the Dockerfile
echo "Building Docker image..."
docker build -t $IMAGE_NAME -f Dockerfile .

# Run All Containers
docker-compose run --rm --service-ports $IMAGE_NAME
