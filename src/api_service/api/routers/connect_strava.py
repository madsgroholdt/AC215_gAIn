import time
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
import json
import requests

from api.data_preprocessing.strava_api import (
    get_strava_config,
    update_strava_config_in_gcp,
    unlink_strava
)
from api.data_preprocessing.cli import main

# Define Route
router = APIRouter()

# Load Strava configuration
project_id = "1059187665772"
secret_name = "strava_config"
secret_data = get_strava_config(project_id, secret_name)
strava_config = json.loads(secret_data)

client_id = strava_config['client_id']
client_secret = strava_config['client_secret']
redirect_uri = "http://localhost:9000/callback"

# Construct the Strava authorization URL
strava_auth_url = (
    f"https://www.strava.com/oauth/authorize?client_id={client_id}"  # noqa
    f"&response_type=code&redirect_uri={redirect_uri}"
    f"&approval_prompt=force&scope=read,activity:read_all"  # noqa: E231
)


@router.get("/connection_status")
async def connection_status():
    # Fetch latest data
    secret_data = get_strava_config(project_id, secret_name, version='latest')
    strava_config = json.loads(secret_data)

    # Check if the user has a valid access token
    if ('access_token' in strava_config and
            strava_config['expires_at'] > int(time.time())):
        return {"connected": True}
    return {"connected": False}


@router.get("/connect_to_strava")
async def connect_strava():
    print("hello")
    # Redirect to the Strava authorization URL
    return RedirectResponse(url=strava_auth_url)


@router.get("/callback")
async def callback(request: Request):
    # Get the authorization code from the URL parameters
    auth_code = request.query_params.get("code")

    if auth_code:
        # Exchange the authorization code for an access token
        token_exchange_url = "https://www.strava.com/oauth/token"
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_exchange_url, data=payload)
        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info.get('access_token')
            refresh_token = token_info.get('refresh_token')
            expires_at = token_info.get('expires_at')

            # Update the strava_config.json file
            strava_config['access_token'] = access_token
            strava_config['refresh_token'] = refresh_token
            strava_config['expires_at'] = expires_at

            updated_config_json = json.dumps(strava_config, indent=4)
            update_strava_config_in_gcp(project_id,
                                        secret_name,
                                        updated_config_json)

            # Process the data after connecting
            main(['--fetch_data', '--generate', '--upload'])

            # Redirect back to the index page
            return RedirectResponse(
                url="http://localhost:3000/#connect"
            )

    # Catch all
    return RedirectResponse(
        url="http://localhost:3000/#connect"
    )


@router.post("/unlink")
async def unlink():
    try:
        # Call the unlink function
        unlink_strava(project_id, secret_name)

        # Return a success message
        return JSONResponse(
            content={"message": "Successfully unlinked Strava account."},
            status_code=200
        )
    except Exception as e:
        # Handle errors gracefully
        return JSONResponse(
            content={"error": "Failed to unlink Strava account.", "details": str(e)},
            status_code=500
        )
