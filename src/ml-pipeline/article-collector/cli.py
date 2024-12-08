import argparse
import requests
import csv
import re
from bs4 import BeautifulSoup
from google.cloud import storage
from find_urls import get_urls

GCS_BUCKET_NAME = "gain-ml-pipeline"

# Set directory names
destination_folder = "raw_articles"


# Upload a file's content to GCS
def upload_to_gcs(bucket_name, title, content):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(f"{destination_folder}/{title}.txt")
        blob.upload_from_string(content)
        print(f"File uploaded to {destination_folder}/{title}.txt\n")
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
        paragraphs = soup.find_all('p')

        # Extract and combine the text from each paragraph
        content = '\n'.join([para.get_text() for para in paragraphs])
        upload_to_gcs(GCS_BUCKET_NAME, title, content)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article content: {e}")


def scrape():
    # Get urls.csv
    print("Getting URLs from GCP bucket...\n")
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob('urls/urls.csv')
    blob.download_to_filename('urls.csv')

    print("Scraping article content...\n")

    with open('urls.csv') as file:
        urls = csv.reader(file)

        for i, url in enumerate(urls):
            # Convert link to unique filename
            title = re.sub(r'[^a-zA-Z0-9]', '', str(url[0]))

            # Get file content
            get_article_content(url[0], title)

    # Add url list to archive
    num_url_lists = sum(1 for _ in bucket.list_blobs(prefix='archive/urls'))
    destination_blob = bucket.blob(f'archive/urls/urls{num_url_lists}.csv')
    destination_blob.rewrite(blob)
    blob.delete()


def main(args=None):
    print("CLI Arguments:", args)

    if args.urls:
        print("Finding health and fitness articles from across the internet...\n")
        get_urls(GCS_BUCKET_NAME, args.urls)

    if args.scrape:
        scrape()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="Data Collector CLI")

    parser.add_argument(
        "--urls",
        type=int,
        help="Get URLs",
    )

    parser.add_argument(
        "--scrape",
        action="store_true",
        help="Scrape and upload articles from list of URLs",
    )

    args = parser.parse_args()

    main(args)
