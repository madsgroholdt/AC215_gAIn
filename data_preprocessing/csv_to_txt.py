import os
import string
import pandas as pd
from google.cloud import storage
from strava_api import get_strava_data 

# Setup
GCP_PROJECT = "ac215-final-project"
GCP_LOCATION = "us-central1"
BUCKET_NAME = "gain-bucket"
BUCKET_CSV_OUTPUT_FOLDER = "raw_user_data"
BUCKET_TXT_OUTPUT_FOLDER = "processed_user_data"

# Function to upload files to GCS
def upload_to_gcs(bucket_name, local_file, user_id, output_folder):
    """Uploads a file to a specific user's folder in GCS."""
    storage_client = storage.Client(project=GCP_PROJECT)
    bucket = storage_client.bucket(bucket_name)
    
    # Define the destination path in GCS (e.g., raw_user_data/user_id/filename.csv)
    destination_blob_name = f"{output_folder}/{user_id}/{os.path.basename(local_file)}"
    
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file)
    
    print(f"File {local_file} uploaded to {destination_blob_name}.")

def csv_to_txt(input_csv, output_txt):
    df = pd.read_csv(input_csv)

    with open(output_txt, 'w') as f:
        for _, row in df.iterrows():
            date = row.iloc[0]  # first column is 'date'
            date = pd.to_datetime(date)
            formatted_date = date.strftime("%A, %B %d")
            day_suffix = "th" if 11 <= date.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(date.day % 10, "th")
            formatted_date += f"{day_suffix} {date.year}"

            # header for each entry
            f.write(f"On {formatted_date}, I had the following health and activity metrics:\n")
            
            # get metric values
            for title in df.columns[1:]:
                value = row[title]
                if pd.isna(value):
                    continue
                
                left_p = title.find('(')
                right_p = title.find(')')
                metric = ''
                if left_p != right_p and left_p != -1:
                    metric = title[left_p+1:right_p]
                
                if metric:
                    f.write(f"{string.capwords(title)} was {value} {metric}\n")
                else:
                    f.write(f"{string.capwords(title)} was {value}\n")
            
            f.write("\n")

if __name__ == "__main__":
    cwd = os.getcwd()
    csv_folder_path = '/csv_data/'
    txt_folder_path = '/txt_data/'

    # Iterate over all CSV files in the csv_data folder
    for filename in os.listdir(cwd + csv_folder_path):
        if filename.endswith('.csv'):
            csv_file = os.path.join(cwd + csv_folder_path, filename)
            txt_file = os.path.join(cwd + txt_folder_path, filename.replace('.csv', '.txt'))

            # Convert CSV to TXT
            csv_to_txt(csv_file, txt_file)
            print(f"Created txt file for {filename}")

            # Extract the user_id from the filename (assumes format like 'user_<user_id>_data.csv')
            user_id = filename.split('_')[1]

            # Upload both the CSV and TXT files to GCS
            upload_to_gcs(BUCKET_NAME, csv_file, user_id, BUCKET_CSV_OUTPUT_FOLDER)
            upload_to_gcs(BUCKET_NAME, txt_file, user_id, BUCKET_TXT_OUTPUT_FOLDER)