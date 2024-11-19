import os
import requests
import csv
import pandas as pd
import json
import time


def get_access_token():
    token_url = "https://www.strava.com/oauth/token"
    json_path = os.path.join('../../', 'secrets', 'strava_config.json')

    with open(json_path, 'r') as file:
        strava_config = json.load(file)

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

        with open(json_path, 'w') as file:
            json.dump(strava_config, file, indent=4)
        print("Access token has been refreshed and strava_config.json has \
              been updated.")
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
    csv_file = f"csv_data/{first_name}_{last_name}_strava_data.csv"

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
