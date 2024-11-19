import argparse
from redirect import connect_to_strava
from strava_api import get_access_token, get_strava_data, create_activities_csv
from csv_to_txt import create_activities_txt, upload_to_gcp

# Setup
GCP_PROJECT = "ac215-final-project"
BUCKET_NAME = "gain-bucket"
BUCKET_CSV_OUTPUT_FOLDER = "raw_user_data"
BUCKET_TXT_OUTPUT_FOLDER = "processed_user_data"


def authenticate():
    """Step 1: Authenticate the user with Strava."""
    connect_to_strava()
    access_token = get_access_token()
    return access_token


def fetch_data(access_token):
    """Step 2: Fetch data from Strava API and store in CSV."""
    print("Fetching Activities via Strava API")
    activities = get_strava_data(access_token)

    print("Storing Activities in CSV file")
    create_activities_csv(activities, access_token)


def generate():
    """Step 3: Generate TXT files."""
    print("\nGenerating Activities TXT file")
    create_activities_txt()


def upload():
    """Step 4: Upload files to GCP Bucket"""
    print("\nUploading files to GCP Bucket")
    upload_to_gcp(BUCKET_NAME, '/csv_data/', BUCKET_CSV_OUTPUT_FOLDER)
    upload_to_gcp(BUCKET_NAME, '/txt_data/', BUCKET_TXT_OUTPUT_FOLDER)


def main():
    parser = argparse.ArgumentParser(
        description="Strava Data Processing Script"
        )
    parser.add_argument('--authenticate',
                        action='store_true',
                        help="Step 1: Authenticate")
    parser.add_argument('--fetch_data',
                        action='store_true',
                        help="Step 2: Fetch + Store data")
    parser.add_argument('--generate',
                        action='store_true',
                        help="Step 3: Generate TXT files")
    parser.add_argument('--upload',
                        action='store_true',
                        help="Step 4: Upload Data to GCP")

    args = parser.parse_args()
    print(args)

    if args == argparse.Namespace(authenticate=False,
                                  fetch_data=False,
                                  generate=False,
                                  upload=False):
        access_token = authenticate()
        fetch_data(access_token)
        generate()
        upload()
        exit(0)

    if args.authenticate:
        authenticate()

    if args.fetch_data:
        fetch_data(get_access_token())

    if args.generate:
        generate()

    if args.upload:
        upload()


if __name__ == "__main__":
    main()
