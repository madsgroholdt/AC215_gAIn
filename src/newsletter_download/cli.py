import os
import json
import argparse
import random
from google.cloud import storage

GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
BUCKET_NAME = "gain-newsletters"
BUCKET_FOLDER = "newsletters_raw"
OUTPUT_FOLDER = "newsletters"
PROCESSED_OUTPUT_FOLDER = "newsletters_processed"


def download_from_gcp():
    """Downloads files from the GCS bucket to a local directory."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)

    blob = bucket.blob(BUCKET_FOLDER)
    destination = os.path.join(OUTPUT_FOLDER, os.path.basename(blob.name))
    blobs = bucket.list_blobs(prefix=BUCKET_FOLDER)
    for blob in blobs:
        if not blob.name.endswith("/"):
            destination = os.path.join(
                OUTPUT_FOLDER, os.path.basename(blob.name))
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            blob.download_to_filename(destination)
            print(f"Downloaded {blob.name} to {destination}")


def preprocess_files():
    for file_name in os.listdir(OUTPUT_FOLDER):
        # Get full file path
        file_path = os.path.join(OUTPUT_FOLDER, file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            # Read file content
            content = file.read()
            reading_time = random.randint(2, 6)

            json_data = {
                "id": file_name[-14:-4],
                "title": file_name[-14:-4],
                "excerpt": content[:100],
                "detail": content,
                "readTime": str(reading_time) + " min read",
                "category": "Health and Fitness",
                "image": "newsletter.jpg"
            }
            print(json_data["title"])
            # File path to save the JSON
            json_path = PROCESSED_OUTPUT_FOLDER + \
                "/" + json_data["title"] + ".json"
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=4, ensure_ascii=False)
                print(f"JSON file saved to {json_path}")


def main(args=None):
    print("CLI Arguments:", args)

    if args.download:
        download_from_gcp()
        preprocess_files()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--download",
        action="store_true",
        help="Download all daily newsletters",
    )

    args = parser.parse_args()

    main(args)
