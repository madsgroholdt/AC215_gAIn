#!/bin/bash

docker build -t data-preprocessing -f Dockerfile .

# Run Docker container
docker run --rm -ti \
    -v $(pwd):/app \
    -v ~/ac215/AC215_gAIn/secrets:/secrets \
    -e GCP_PROJECT="gAIn" \
    data-preprocessing