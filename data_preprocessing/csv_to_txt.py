import os
import string
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account

def get_first_last_name(filename):
    filename_lst = filename.split("_")
    return filename_lst[0], filename_lst[1]

def csv_to_txt(input_csv, output_txt, filename):
    df = pd.read_csv(input_csv)
    first_name, last_name = get_first_last_name(filename)

    with open(output_txt, 'w') as f:
        for _, row in df.iterrows():
            date = row.iloc[0]  # first column is 'date'
            date = pd.to_datetime(date)
            formatted_date = date.strftime("%A, %B %d")
            day_suffix = "th" if 11 <= date.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(date.day % 10, "th")
            formatted_date += f"{day_suffix} {date.year}"

            # header for each entry
            f.write(f"On {formatted_date}, {first_name} {last_name} had the following health and activity metrics:\n")
            
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

def create_activities_txt():
    cwd = os.getcwd() 
    csv_folder_path = '/csv_data/'
    txt_folder_path = '/txt_data/'
    for filename in os.listdir(cwd + csv_folder_path):
        if filename.endswith('.csv'):
            csv_file = os.path.join(cwd + csv_folder_path, filename)
            txt_file = os.path.join(cwd + txt_folder_path, filename.replace('.csv', '.txt'))
            
            csv_to_txt(csv_file, txt_file, filename)
            print(f"Created txt file for {filename}")

def upload_to_gcp(bucket_name, folder_path, output_folder):
    credentials = service_account.Credentials.from_service_account_file(os.getcwd() +'/../secrets/data-preprocessing.json')
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)

    file_type = '.csv' if folder_path == '/csv_data/' else '.txt'

    for filename in os.listdir(os.getcwd() + folder_path):
        if filename.endswith(file_type):
            first_name, last_name = get_first_last_name(filename)

            destination_blob_name = f"{output_folder}/{first_name}_{last_name}/{filename}"
            blob = bucket.blob(destination_blob_name)

            full_file_path = os.path.join(os.getcwd() + folder_path, filename)
            print("Uploading:", destination_blob_name)
            blob.upload_from_filename(full_file_path)
