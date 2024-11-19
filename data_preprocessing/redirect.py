import os
import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import webbrowser


# Load Strava configuration
json_path = os.path.join('../', 'secrets', 'strava_config.json')
with open(json_path, 'r') as file:
    strava_config = json.load(file)

client_id = strava_config['client_id']
client_secret = strava_config['client_secret']
redirect_uri = "http://localhost:8080"  # Local server URI


# Construct the Strava authorization URL
strava_auth_url = (
    f"https://www.strava.com/oauth/authorize?client_id={client_id}"
    f"&response_type=code&redirect_uri={redirect_uri}"
    f"&approval_prompt=auto&scope=read,activity:read_all"
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
            self.wfile.write(b"Authorization code received. You can close this window.")

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

                with open(json_path, 'w') as file:
                    json.dump(strava_config, file, indent=4)
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