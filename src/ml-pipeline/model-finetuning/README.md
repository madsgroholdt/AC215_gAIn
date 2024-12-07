### Run Container
Run the startup script which makes building & running the container easy.

- Make sure you are inside the `model_finetuner` folder and open a terminal at this location
- Run `sh docker-shell.sh`
- After container startup, test the shell by running `python cli.py --help`

Create a secrets folder at the same level as the `src` folder.
This folder should contain:
 - finetuning-service-account.json: The credentials file connected to a gAIn GCP Service account with the necessary permissions:
   - `Storage Admin`
   - `Vertex AI User`

### Fine-tune Model
- Run `python cli.py --train` to fine-tune the Gemini model
- Change any of the default parameters if needed

### Chat with Fine-tuned Model
- Update the endpoint to the newly fine-tuned model.
- Run `python cli.py --chat`
