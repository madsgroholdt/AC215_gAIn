### Run Container
Run the startup script which makes building & running the container easy.

- Make sure you are inside the `data_preprocessing` folder and open a terminal at this location
- Run `sh docker-shell.sh`
- After container starts up, test the shell by running `python cli.py --help`

Create a secrets folder at the same level as the `src` folder.
This folder should contain:
- data_preprocessing.json: The credentials file connected to a gAIn GCP Service account with the necessary permissions:
  - `Storage Admin`
  - `Viewer`
- strava_config.json: Contains our Strava API's `client_id` and `client_secret` which allows a user to connect their Strava account to gAIn

### Authenticate Strava Account
- Run `python cli.py --authenticate`
- Sets up a local HTTP server to capture the authorization code
- Automatically opens a Strava authorization URL in a web browser allowing the user to sign into their Strava account, and accept the required permissions
- If the user successfully signs in and accpets the permissions, an `access_token`, `refresh_token`, and `expires_at` value are generated, and stored in strava_config.json


### Fetch Strava Data
- Run `python cli.py --fetch_data`
- Checks if the current `access_token` is expired, and if so, generates a new one using the `refresh_token`
  - Stores the new `access_token` and `expires_at` value in strava_config.json
- Using the `access_token`, submits a GET request to get all of the user's Strava activities and stores then in a `.csv` file
- The naming convention for each file is `firstname_lastname_souce_data.csv`
  - ex: `John_Doe_strava_data.csv`

### Generate .txt files (Preprocessing for RAG)
- Run `python cli.py --generate`
- Uses the `.csv` file generated in the previous step to generate a formatted `.txt` file summarizing health and activity metrics for a given individual. The summary is formatted with:
  - **Date Formatting:** The date is converted into a human-readable format with a proper suffix (e.g., "st", "nd", "rd", "th").
  - **Header Creation:** Each entry starts with a header indicating the date and individual's name, derived from the filename.
  - **Metric Output:** Health and activity metrics are listed with values and optional units extracted from column headers.
- The naming convention for each file is `firstname_lastname_souce_data.txt`
  - ex:`John_Doe_strava_data.txt`


### Upload to GCP Bucket
- Run `python cli.py --upload`
- Uploads both the generated `.csv` and `.txt` files to a GCP bucket
- `.csv` files go to a folder within the bucket called `processed_user_data/firstname_lastname/`
  - ex: `processed_user_data/John_Doe/John_Doe_strava_data.csv`
- `.txt` files go to a folder within the bucket called `raw_user_data/firstname_lastname/`
  - ex: `processed_user_data/John_Doe/John_Doe_strava_data.txt`


### Run Entire Pre-processing Pipeline
- Run `python cli.py`
- Runs the entire pipeline, including authentication, data-fetching, generating pre-processed data, and uploading the data
