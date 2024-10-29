from __future__ import print_function
import json
import os
import requests
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

def get_access_token():
    token_url = "https://www.strava.com/oauth/token"

    json_path = os.path.join('../..', 'secrets', 'strava_config.json')
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
    return token_response.json().get('access_token')

# Configure OAuth2 access token for authorization: strava_oauth
configuration = swagger_client.Configuration()
configuration.access_token = get_access_token()

# create an instance of the API class
api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
before = 56 # int | An epoch timestamp to use for filtering activities that have taken place before a certain time. (optional)
after = 56 # int | An epoch timestamp to use for filtering activities that have taken place after a certain time. (optional)
page = 56 # int | Page number. Defaults to 1. (optional)
per_page = 30 # int | Number of items per page. Defaults to 30. (optional) (default to 30)

try:
    # List Athlete Activities
    api_response = api_instance.get_logged_in_athlete_activities(
        # before=before, 
        # after=after, 
        # page=page, 
        per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->get_logged_in_athlete_activities: %s\n" % e)