# gAIn API Service (Backend)

## Overview

The **gAIn Backend API Server** is designed to support various features like Strava integration, newsletter fetching, and chat interactions with an LLM-based system. The API is built using **FastAPI** and is composed of several distinct modules, each of which is handled by a specific route. This document provides an overview of the structure and how to deploy, test, and interact with the server locally.

## Features

1. **Strava Integration**
   - **Connect to Strava**: Redirects users to Strava's authorization page.
   - **Check Connection Status**: Checks if a valid Strava `access_token` is present in the GCP Secrets Manager `strava_config`
   - **Unlink Strava Account**: Allows users to unlink their Strava account from the system by getting rid of the `access_token`, `refresh_token`, and `expires_at` value GCP Secrets Manager `strava_config`

2. **Newsletter Management**
   - Fetches and returns newsletters from a local directory, typically populated by a machine learning pipeline.

3. **LLM-based Chat Management**
   - Allows users to start and continue chat sessions with a large language model (LLM) using retrieval-augmented generation (RAG).

## File Structure

- Within the `api/routers/` folder:
    - `connect_strava.py`: Handles Strava integration.
    - `newsletter.py`: Manages newsletters (fetching and serving them).
    - `llm_rag_chat.py`: Manages chat sessions with an LLM using retrieval-augmented generation (RAG).
- Within the `api/utils/` folder:
    - `chat_utils.py`:
    - `llm_rag_utils.py`:
- Within the `api/` folder:
    - `service.py`: The FastAPI application that ties all components together.

## Container Set-Up
Run the startup script which makes building & running the container easy.

- Make sure you are inside the `api_service` folder and open a terminal at this location
- Run `sh docker-shell.sh`
- Once the container is up and running, type `uvicorn_server`

Create a secrets folder at the same level as the `src` folder. This folder should contain:

- llm-service-account.json: The credentials file connected to a gAIn GCP Service account with the necessary permissions:
  - `AI Platform Admin`
  - `Storage Admin`
  - `Secret Manager Admin`
  - `Vertex AI Administrator`
- strava_config.json: Contains our Strava API's `client_id` and `client_secret` which allows a user to connect their Strava account to gAIn
  - Current Implementation now works by storing these Strava secrets in the GCP Secret Manager

## Strava Integration

### GET `/connection_status`
- Loads `strava_config` secrets from GCP Secrets Manager and checks if a valid `access_token` exists. If it does then it returns a json with `{"connected": True}`. Otherwise returns a json with `{"connected": False}`
    - When `True` the `Connect to Strava` Button is disabled, the text becomes `Connected to Strava`, and an `Unlink` Button appears to its right
    - When `False` the `Connect to Strava` Button is enabled
- Triggered by loading into the home page of the front-end, or any reload of the home page

### GET `/connect_to_strava`
- Redirects the user to the Strava authorization URL
- Triggered by the user clicking on the `Connect to Strava` Button

### GET `/callback`
- Gets the code returned by the user connecting their account to Strava via the authorization URL they were redirected to. Using this new code, it creates a valid `access_token`, `refresh_token`, and `expires_at` value. These values are then uploaded to the GCP Secrets Manager `strava_config`, and then triggers the rest of the data-preprocessing pipeline described in the `api/data_preprocessing/` folder. TLDR, it then fetches the users Strava Activities data, preprocesses it, and uploads it to a GCP bucket. Finally, once this pipeline completes, it redirects the user back to the front-end home page at the level of the button via `/#connect`. This redirect subsequently triggers **GET** `/connection_status` due to loading back into the home page
- Triggered by the user logging in via the Strava authorization URL and accepting the required permissions

### POST `/unlink`
- Calls the `unlink_strava(PROJECT_NUM, SECRET_NAME)` function from `strava_api.py` in the `api/data_preprocessing/` folder which simply gets rid of the `access_token`, `refresh_token`, and `expires_at` value from the secrets it downloads from GCP, and then uploads the new version to the GCP Secrets Manager. It then forces a reload of the main page which then gets rid of the `Unlink` Button, and re-enables the `Connect to Strava` Button
- Triggered by the `Unlink` Button next to the `Connected to Strava` Button
