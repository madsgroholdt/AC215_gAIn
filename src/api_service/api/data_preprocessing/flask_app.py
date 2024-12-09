from flask import Flask, redirect, request, render_template, url_for
import json
import requests
if __package__ is None or __package__ == '':
    from strava_api import get_strava_config, update_strava_config_in_gcp
    from cli import main
else:
    from api.data_preprocessing.strava_api import (
        get_strava_config,
        update_strava_config_in_gcp
    )
    from api.data_preprocessing.cli import main

app = Flask(__name__)

# Load Strava configuration
project_id = "1059187665772"
secret_name = "strava_config"
secret_data = get_strava_config(project_id, secret_name)
strava_config = json.loads(secret_data)

client_id = strava_config['client_id']
client_secret = strava_config['client_secret']
redirect_uri = "http://localhost:8080/callback"  # Adjusted callback URI

# Construct the Strava authorization URL
strava_auth_url = (
    f"https://www.strava.com/oauth/authorize?client_id={client_id}"  # noqa
    f"&response_type=code&redirect_uri={redirect_uri}"
    f"&approval_prompt=auto&scope=read,activity:read_all"  # noqa: E231
)


@app.route('/')
def index():
    # Render the template and pass the connected flag
    connected = request.args.get('connected', 'false') == 'true'
    return render_template('connect.html', connected=connected)


@app.route('/connect_to_strava')
def connect_strava():
    # Redirect to the Strava authorization URL
    return redirect(strava_auth_url)


@app.route('/callback')
def callback():
    # Get the authorization code from the URL parameters
    auth_code = request.args.get('code')

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

            main(['--fetch_data', '--generate', '--upload'])

            # Redirect back to the index page with 'connected' flag
            return redirect(url_for('index', connected='true'))

    return redirect(url_for('index', connected='false'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
