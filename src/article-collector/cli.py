import argparse
import requests
import csv
import os
from bs4 import BeautifulSoup
from google.cloud import storage
from find_urls import get_urls


# Set directory names
bucket_name = "gain-ml-pipeline"
source_folder = "/articles"
destination_folder = "raw_articles"


# Upload a file's content to GCS
def upload_to_gcs(bucket_name, title, content):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(f"articles/{title}.txt")
        blob.upload_from_string(content)
        print(f"File uploaded to bucket {bucket_name} in folder articles/{title}.txt\n")
    except Exception:
        print(f"Error uploading file {title}.txt to GCP bucket\n")


# Scrape the content of a given article
def get_article_content(url, title):
    try:
        # Send a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content (adjust for different websites)
        # 'p' = paragraphs
        paragraphs = soup.find_all('p')

        # Extract and combine the text from each paragraph
        content = '\n'.join([para.get_text() for para in paragraphs])
        upload_to_gcs(bucket_name, title, content)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article content: {e}")


def scrape(base_index=0):
    # Get urls.csv
    print("Getting URLs from GCP bucket...\n")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('urls/urls.csv')
    blob.download_to_filename('urls.csv')

    print("Scraping article content...\n")

    os.makedirs('/articles', exist_ok=True)
    with open('urls.csv') as file:
        urls = csv.reader(file)

        # Access each row and element
        for i, url in enumerate(urls):
            get_article_content(url[0], f"article{i+base_index}")


def main(args=None):
    print("CLI Arguments:", args)

    if args.urls:
        print("Finding health and fitness articles from across the internet...\n")
        get_urls()

        # Initialize client
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob('urls/urls.csv')
        blob.upload_from_filename('urls.csv')
        print("URLs uploaded to GCP bucket")

    if args.scrape:
        scrape(base_index=200)  # Change base index to prevent overwrite


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="Data Collector CLI")

    parser.add_argument(
        "--urls",
        action="store_true",
        help="Get URLs",
    )

    parser.add_argument(
        "--scrape",
        action="store_true",
        help="Scrape and upload articles from list of URLs",
    )

    args = parser.parse_args()

    main(args)
