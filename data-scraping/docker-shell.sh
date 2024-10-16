#!/bin/bash

docker build -t data-scraping -f Dockerfile .

docker run --rm -ti \
    -v ~/ac215/AC215_gAIn/data-scraping/articles:/articles \
    data-scraping