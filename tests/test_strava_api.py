import json
import os
import time
from src.api_service.api.data_preprocessing.strava_api import (
    get_strava_config,
    update_strava_config_in_gcp,
    unlink_strava,
    get_access_token,
    get_strava_data,
    create_activities_csv
)
from unittest.mock import patch, MagicMock

PROJECT_NUM = os.getenv("PROJECT_NUM")
SECRET_NAME = os.getenv("SECRET_NAME")


# Verify that the get_strava_config function correctly retrieves a
# configuration from the GCP Secret Manager
def test_get_strava_config():
    # Mock the SecretManagerServiceClient and its method access_secret_version
    # to simulate fetching a secret containing a JSON configuration
    mock_client = MagicMock()
    mock_secret = MagicMock()
    mock_secret.payload.data.decode.return_value = '{"key": "value"}'
    mock_client.access_secret_version.return_value = mock_secret

    with patch('api_service.api.data_preprocessing.strava_api.secretmanager.\
               SecretManagerServiceClient',
               return_value=mock_client):
        config = get_strava_config('123456', 'test_secret')

    assert config == '{"key": "value"}'
    mock_client.access_secret_version.assert_called_once_with(
        name='projects/123456/secrets/test_secret/versions/latest'
    )

    # Test that GCP holds at least the cliend id and client secret
    data = get_strava_config(PROJECT_NUM, SECRET_NAME)
    strava_config = json.loads(data)

    assert strava_config['client_id']
    assert strava_config['client_secret']

    if strava_config['access_token']:
        assert strava_config['refresh_token']
        assert strava_config['expires_at']


# Check that the update_strava_config_in_gcp function correctly updates a
# Strava configuration in the GCP Secret Manager
def test_update_strava_config_in_gcp():
    # Mock the SecretManagerServiceClient and simulate adding a new version of
    # secrets with the updated config
    mock_client = MagicMock()
    new_config = '{"key": "updated_value"}'

    with patch('api_service.api.data_preprocessing.strava_api.secretmanager.\
               SecretManagerServiceClient', return_value=mock_client):
        update_strava_config_in_gcp('123456', 'test_secret', new_config)

    # Assert add_secret_version method is called with the correct parameters
    mock_client.add_secret_version.assert_called_once_with(
        parent='projects/123456/secrets/test_secret',
        payload={'data': new_config.encode("UTF-8")}
    )


# Ensure that the unlink_strava function removes the access token and
# refresh token from the configuration, leaving only the client_id and
# client_secret
@patch('api_service.api.data_preprocessing.strava_api.get_strava_config')
@patch('api_service.api.data_preprocessing.strava_api.update_strava_config_in_gcp')
def test_unlink_strava(mock_update_config, mock_get_config):
    # Mock both get_strava_config and update_strava_config_in_gcp
    mock_get_config.return_value = json.dumps({
        'client_id': 'test_client_id',
        'client_secret': 'test_client_secret',
        'access_token': 'test_token'
    })

    unlink_strava('123456', 'test_secret')

    expected_unlinked_config = json.dumps({
        'client_id': 'test_client_id',
        'client_secret': 'test_client_secret',
    }, indent=4)

    # Assert that the update_strava_config_in_gcp function is called which
    # updates the config
    mock_update_config.assert_called_once_with(
        '123456',
        'test_secret',
        expected_unlinked_config
    )


@patch('api_service.api.data_preprocessing.strava_api.get_strava_config')
@patch('api_service.api.data_preprocessing.strava_api.update_strava_config_in_gcp')
@patch('requests.post')
def test_get_access_token_token_refresh(mock_post,
                                        mock_update_config,
                                        mock_get_config):
    mock_get_config.return_value = json.dumps({
        'client_id': 'test_client_id',
        'client_secret': 'test_client_secret',
        'access_token': 'expired_token',
        'refresh_token': 'test_refresh_token',
        'expires_at': 1
    })
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        'access_token': 'new_token',
        'refresh_token': 'new_refresh_token',
        'expires_at': int(time.time()) + 3600
    }

    token = get_access_token()

    assert token == 'new_token'
    mock_update_config.assert_called_once()
    mock_post.assert_called_once_with(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'refresh_token': 'test_refresh_token',
            'grant_type': 'refresh_token'
        }
    )


@patch('requests.get')
def test_get_strava_data(mock_get):
    mock_get.side_effect = [
        MagicMock(status_code=200, json=lambda: [{'activity_id': 1},
                                                 {'activity_id': 2}]),
        MagicMock(status_code=200, json=lambda: []),  # Ends pagination
    ]

    activities = get_strava_data('test_access_token')

    assert len(activities) == 2
    assert activities[0]['activity_id'] == 1
    assert activities[1]['activity_id'] == 2
    mock_get.assert_called()


@patch('api_service.api.data_preprocessing.strava_api.get_csv_txt_paths')
@patch('pandas.DataFrame.to_csv')
@patch('requests.get')
def test_create_activities_csv(mock_requests_get, mock_to_csv, mock_get_paths):
    # Mock get_csv_txt_paths
    mock_get_paths.return_value = ('/src/api_service/api/data_preprocessing/csv_data/',
                                   '/src/api_service/api/data_preprocessing/csv_data/')

    # Mock activities data
    activities = [{'start_date': '2024-12-01',
                   'name': 'Run',
                   'sport_type': 'Running',
                   'distance': 5000}]

    access_token = get_access_token()
    create_activities_csv(activities, access_token)

    # Assert the requests.get call for the athlete info
    athlete_url = "https://www.strava.com/api/v3/athlete"
    mock_requests_get.assert_called_with(athlete_url,
                                         headers={'Authorization':
                                                  f'Bearer {access_token}'})

    # Assert the CSV file creation
    mock_to_csv.assert_called_once()

    # Delete the created CSV file
    csv_path = 'src/api_service/api/data_preprocessing/csv_data/\
                    John_Doe_strava_data.csv'
    if os.path.exists(csv_path):
        os.remove(csv_path)
        print(f"Deleted test CSV file: {csv_path}")
