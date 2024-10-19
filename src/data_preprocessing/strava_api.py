import os
import requests
import csv
import pandas as pd
import json

def get_strava_data():
    # strava endpoints
    token_url = "https://www.strava.com/oauth/token"
    activities_url = "https://www.strava.com/api/v3/activities"

    json_path = os.path.join('..', 'secrets', 'strava_config.json')
    with open(json_path, 'r') as file:
        strava_config = json.load(file)

    client_id = strava_config['client_id']
    client_secret = strava_config['client_secret']
    refresh_token = strava_config['refresh_token']

    # POST request to get the new access token
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    token_response = requests.post(token_url, data=params)
    access_token = token_response.json().get('access_token')

    # GET request to get activities list
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    activities_response = requests.get(activities_url, headers=headers)

    if activities_response.status_code == 200:
        activities = activities_response.json()

        titles = [
            "start_date", "name", "sport_type", "distance", "moving_time", "elapsed_time",
            "total_elevation_gain", "average_speed", "max_speed", "average_watts", 
            "max_watts", "average_heartrate", "max_heartrate", "kilojoules", "elev_high",
            "elev_low", "timezone", "achievement_count", "kudos_count", "athlete_count",
        ]

        csv_file = "csv_data/activities_data.csv"

        # write the data to a CSV file
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=titles)
            writer.writeheader()

            # each activity is a new row
            for activity in activities:
                filtered_activity = {key: activity.get(key) for key in titles}
                writer.writerow(filtered_activity)

        print(f"CSV file '{csv_file}' created successfully.")

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
    else:
        print(f"Error: {activities_response.status_code} - {activities_response.text}")

if __name__ == "__main__":
    get_strava_data()

