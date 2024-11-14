#!/bin/bash

set -e

export IMAGE_NAME="gain-frontend-react"

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile.dev .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
  -v "$(pwd)/:/app/" \
  -p 3000:3000 \
  --network gain-rag-network \
  $IMAGE_NAME

# docker run --rm --name $IMAGE_NAME -ti -v "$(pwd)/:/app/" -p 3000:3000 $IMAGE_NAME