#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# export TESTS_DIR=$(pwd)/../tests
# export API_SERVICE_DIR=$(pwd)/../src/api_service
export BASE_DIR=$(pwd)/..
export SECRETS_DIR=$(pwd)/../secrets
export GCP_PROJECT="ac215-final-project"
export GCS_BUCKET_NAME="gain-bucket"
export BUCKET_CSV_OUTPUT_FOLDER="raw_user_data"
export BUCKET_TXT_OUTPUT_FOLDER="processed_user_data"
export PROJECT_NUM="1059187665772"
export SECRET_NAME="strava_config"
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-preprocessing.json"
export GCP_SERVICE_ACCOUNT="data-preprocessing@ac215-final-project.iam.gserviceaccount.com"
export LOCATION="us-central1"
export IMAGE_NAME="test-runnner"

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e BUCKET_CSV_OUTPUT_FOLDER=$BUCKET_CSV_OUTPUT_FOLDER \
-e BUCKET_TXT_OUTPUT_FOLDER=$BUCKET_TXT_OUTPUT_FOLDER \
-e PROJECT_NUM=$PROJECT_NUM \
-e SECRET_NAME=$SECRET_NAME \
$IMAGE_NAME


# -v "$TESTS_DIR":/tests \
# -v "$API_SERVICE_DIR":/api_service \
