#!/bin/bash
echo "Container is running!!!"

# Run the Uvicorn server with pipenv in a non-interactive way
pipenv run uvicorn api.service:app --host 0.0.0.0 --port 9000