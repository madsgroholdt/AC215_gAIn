#!/bin/bash

docker build -t data-preprocessing -f Dockerfile .

# Run Docker container
docker run --rm -ti \
    -v $(pwd):/app \
    -v ~/ac215/AC215_gAIn/data-scraping/articles:/articles \
    -v ~/ac215/AC215_gAIn/secrets:/secrets \
    -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-scraping-service.json" \
    -e GCP_PROJECT="gAIn" \
    data-scraping

docker run --rm -ti \
    -v "$(pwd)/csv_data:/app/csv_data" \
    -v "$(pwd)/txt_data:/app/txt_data" \
    data-preprocessing
