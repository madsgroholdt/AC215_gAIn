import argparse
import requests
import csv
import os
from bs4 import BeautifulSoup
from google.cloud import storage
from find_urls import get_urls


# Set directory names
bucket_name = "gain-ft-articles"
source_folder = "/articles"
destination_folder = "raw_articles"


# Helper functions for uploading files
def upload_single_file(bucket_name, source_file_path, destination_file_path):
    try:
        # Initialize client
        storage_client = storage.Client()

        # Get target destination
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_file_path)

        # Upload file to cloud and delete locally
        blob.upload_from_filename(source_file_path)
        print(f"\n{source_file_path} uploaded to GCP bucket")

        os.remove(source_file_path)
        print(f"{source_file_path} DELETED locally")

    except Exception:
        print(f"\nError uploading file {source_file_path} to GCP bucket")


# Send all local files to bucket
def send_to_bucket(bucket_name=bucket_name,
                   source_folder=source_folder,
                   destination_folder=destination_folder):

    # Loop through local articles and upload
    for filename in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, filename)
        destination_file_path = os.path.join(destination_folder, filename)

        if os.path.isfile(source_file_path):
            upload_single_file(bucket_name, source_file_path, destination_file_path)


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

        # title = soup.title.get_text() if soup.title else 'No title found'

        # Extract and combine the text from each paragraph
        content = '\n'.join([para.get_text() for para in paragraphs])

        # Save the content to a text file
        with open(f"/articles/{title}.txt", 'w') as file:
            file.write(content)

        print(f"Article saved to {title}.txt")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")


def scrape(source, base_index=0):
    with open(source, mode='r') as file:
        urls = csv.reader(file)

        # Access each row and element
        for i, url in enumerate(urls):
            get_article_content(url[0], f"article{i+base_index}")

            if i % 50 == 0:
                send_to_bucket()


def main(args=None):
    print("CLI Arguments:", args)

    if args.urls:
        print("Finding health and fitness articles from across the internet...\n")
        get_urls()

    if args.scrape:
        print("Scraping article content...\n")
        scrape('urls.csv', base_index=100)  # Change base index to prevent overwrite


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
