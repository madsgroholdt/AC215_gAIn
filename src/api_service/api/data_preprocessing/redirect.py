import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import webbrowser
if __package__ is None or __package__ == '':
    # Standalone execution
    from strava_api import get_strava_config, update_strava_config_in_gcp
else:
    # Package execution
    from api.data_preprocessing.strava_api import (
        get_strava_config,
        update_strava_config_in_gcp
    )


# Load Strava configuration
secret_data = get_strava_config("1059187665772", "strava_config")
strava_config = json.loads(secret_data)

client_id = strava_config['client_id']
client_secret = strava_config['client_secret']
redirect_uri = "http://localhost:8080"  # Local server URI


# Construct the Strava authorization URL
strava_auth_url = (
    f"https://www.strava.com/oauth/authorize?client_id={client_id}"  # noqa
    f"&response_type=code&redirect_uri={redirect_uri}"
    f"&approval_prompt=auto&scope=read,activity:read_all"  # noqa: E231
)


# Set up a local HTTP server to capture the authorization code
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL query string
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)
        auth_code = query_params.get('code', [None])[0]

        if auth_code:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                b"Authorization code received. You can close this window."
                )

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
                update_strava_config_in_gcp("1059187665772",
                                            "strava_config",
                                            updated_config_json)
                print("\nstrava_config.json has been updated.\n")
            else:
                print("Error exchanging token:", response.json())

        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization code not found.")


def connect_to_strava():
    # Open the Strava authorization URL in the user's browser
    print("Opening browser for user authentication...")
    webbrowser.open(strava_auth_url)
    print(strava_auth_url)

    # Start the local server
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Listening for redirect with authorization code...")
    httpd.handle_request()  # Handles one request, then stops
