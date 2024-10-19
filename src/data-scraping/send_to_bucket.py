import os
from google.cloud import storage

def upload_to_storage(bucket_name, source_file_path, destination_file_path):
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

    except:
        print(f"\nError uploading file {source_file_path} to GCP bucket")

# Set directory names
bucket_name = "gain-articles"
source_folder = "/articles"
destination_folder = "raw_articles"

# Loop through local articles and upload
for filename in os.listdir(source_folder):
    source_file_path = os.path.join(source_folder, filename)
    destination_file_path = os.path.join(destination_folder, filename)

    if os.path.isfile(source_file_path):
        upload_to_storage(bucket_name, source_file_path, destination_file_path)