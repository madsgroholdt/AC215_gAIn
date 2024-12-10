import os
import requests
import csv
import pandas as pd
import json
import time
from google.cloud import secretmanager
if __package__ is None or __package__ == '':
    from csv_to_txt import get_csv_txt_paths
else:
    from api.data_preprocessing.csv_to_txt import get_csv_txt_paths


def get_strava_config(project_num, secret_name, version='latest'):
    client = secretmanager.SecretManagerServiceClient()
    path = f"projects/{project_num}/secrets/{secret_name}/versions/{version}"
    response = client.access_secret_version(name=path)
    secret_value = response.payload.data.decode('UTF-8')
    return secret_value


def update_strava_config_in_gcp(project_num, secret_name, new_config):
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_num}/secrets/{secret_name}"

    # Add a new version of the secret with the updated JSON
    client.add_secret_version(
        parent=parent,
        payload={"data": new_config.encode("UTF-8")}
    )
    print("Updated strava_config secret in GCP Secret Manager.")


def unlink_strava(project_num, secret_name):
    data = json.loads(get_strava_config(project_num, secret_name))
    unlinked_config = {
        'client_id': data['client_id'],
        'client_secret': data['client_secret'],
    }
    unlinked_config = json.dumps(unlinked_config, indent=4)
    update_strava_config_in_gcp(project_num, secret_name, unlinked_config)


def get_access_token():
    PROJECT_NUM = os.getenv("PROJECT_NUM")
    SECRET_NAME = os.getenv("SECRET_NAME")
    # Retrieve the JSON secret and parse it
    secret_data = get_strava_config(PROJECT_NUM, SECRET_NAME)
    strava_config = json.loads(secret_data)

    client_id = strava_config['client_id']
    client_secret = strava_config['client_secret']
    access_token = strava_config['access_token']
    refresh_token = strava_config['refresh_token']
    expires_at = strava_config['expires_at']

    assert (access_token)
    assert (refresh_token)
    assert (expires_at)

    # Check if the current token is still valid
    current_time = int(time.time())
    if current_time < expires_at:
        print("Current access token is still valid.")
        return access_token

    # Token has expired -> generate a new one using the refresh token
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    token_url = "https://www.strava.com/oauth/token"
    token_response = requests.post(token_url, data=params)

    if token_response.status_code == 200:
        token_info = token_response.json()
        access_token = token_info.get('access_token')
        refresh_token = token_info.get('refresh_token')
        expires_at = token_info.get('expires_at')

        # Update the configuration file with the new tokens and expiry
        strava_config['access_token'] = access_token
        strava_config['refresh_token'] = refresh_token
        strava_config['expires_at'] = expires_at

        # Convert updated config to JSON and upload to GCP Secret Manager
        updated_config_json = json.dumps(strava_config, indent=4)
        update_strava_config_in_gcp(PROJECT_NUM,
                                    SECRET_NAME,
                                    updated_config_json)

        return access_token

    print("Error refreshing access token:", token_response.json())
    exit(1)


def get_strava_data(access_token):
    activities_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': f'Bearer {access_token}'}

    # GET request to get activities list
    request_page_num = 1
    all_activities = []
    while True:
        param = {'per_page': 200, 'page': request_page_num}
        response = requests.get(activities_url, headers=header, params=param)
        if response.status_code == 200:
            activities_subset = response.json()

            if len(activities_subset) == 0:
                break

            all_activities.extend(activities_subset)
            request_page_num += 1
        else:
            print(f"Error: {response.status_code} - {response.text}")
            exit(1)

    return all_activities


def create_activities_csv(all_activities, access_token):
    titles = [
        "start_date", "name", "sport_type", "distance", "moving_time",
        "elapsed_time", "total_elevation_gain", "average_speed", "max_speed",
        "average_watts", "max_watts", "average_heartrate", "max_heartrate",
        "kilojoules", "elev_high", "elev_low", "timezone", "achievement_count",
        "kudos_count", "athlete_count",
    ]

    athlete_url = "https://www.strava.com/api/v3/athlete"
    header = {'Authorization': f'Bearer {access_token}'}
    athlete_response = requests.get(athlete_url, headers=header)
    athlete_info = athlete_response.json()

    first_name, last_name = athlete_info["firstname"], athlete_info["lastname"]
    csv_path, _ = get_csv_txt_paths()
    csv_file = f"{csv_path[1:]}{first_name}_{last_name}_strava_data.csv"

    # write the data to a CSV file
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=titles)
        writer.writeheader()

        # each activity is a new row
        for activity in all_activities:
            filtered_activity = {key: activity.get(key) for key in titles}
            writer.writerow(filtered_activity)

    updated_titles = {
        "start_date": "start date",
        "name": "name",
        "sport_type": "sport type",
        "distance": "distance (meters)",
        "moving_time": "moving time (seconds)",
        "elapsed_time": "elapsed time (seconds)",
        "total_elevation_gain": "total elevation gain (meters)",
        "average_speed": "average speed (meters/second)",
        "max_speed": "max speed (meters/second)",
        "average_watts": "average watts (watts)",
        "max_watts": "max watts (watts)",
        "average_heartrate": "average heartrate (bpm)",
        "max_heartrate": "max heartrate (bpm)",
        "kilojoules": "kilojoules (kJ)",
        "elev_high": "elev high (meters)",
        "elev_low": "elev low (meters)",
        "achievement_count": "achievement count",
        "kudos_count": "kudos count",
        "athlete_count": "athlete count",
    }

    df = pd.read_csv(csv_file)
    df.rename(columns=updated_titles, inplace=True)
    df.to_csv(csv_file, index=False)

    print(f"CSV file '{csv_file}' created successfully.")
