#!/bin/bash
set -e

source ../env.dev
REPO_NAME="gcf-artifacts"
IMAGE_NAME="model-finetuning"

# Tag the image for Artifact Registry
docker build -t $IMAGE_NAME --platform=linux/amd64 .
docker tag $IMAGE_NAME $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$REPO_NAME/$IMAGE_NAME

# Push the image to Artifact Registry
docker push $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$REPO_NAME/$IMAGE_NAME
