#!/bin/bash

docker build -t data-scraping -f Dockerfile .

# Run Docker container
docker run --rm -ti \
    -v $(pwd):/app \
    -v ~/ac215/AC215_gAIn/data-scraping/articles:/articles \
    -v ~/ac215/AC215_gAIn/secrets:/secrets \
    -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/web-scraping-service.json" \
    -e GCP_PROJECT="gAIn" \
    data-scraping
