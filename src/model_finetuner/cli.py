import os
import argparse
import time
import vertexai
from vertexai.preview.tuning import sft
from vertexai.generative_models import GenerativeModel

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
TRAIN_DATASET = "gs://gain-ft-articles/llm-finetune-dataset-small/train.jsonl"
VALIDATION_DATASET = "gs://gain-ft-articles/llm-finetune-dataset-small/test.jsonl"
GCP_LOCATION = "us-central1"
GENERATIVE_SOURCE_MODEL = "gemini-1.5-pro-002"  # base model
# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.75,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}

vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)


def train(wait_for_job=False):
    print("train()")

    # Supervised Fine Tuning
    sft_tuning_job = sft.train(
        source_model=GENERATIVE_SOURCE_MODEL,
        train_dataset=TRAIN_DATASET,
        validation_dataset=VALIDATION_DATASET,
        epochs=2,   # between 2-3
        adapter_size=4,
        learning_rate_multiplier=1.0,
        tuned_model_display_name="gain-ft-v1",
    )
    print("Training job started. Monitoring progress...\n\n")

    # Wait and refresh
    time.sleep(60)
    sft_tuning_job.refresh()

    if wait_for_job:
        print("Check status of tuning job:")
        print(sft_tuning_job)
        while not sft_tuning_job.has_ended:
            time.sleep(60)
            sft_tuning_job.refresh()
            print("Job in progress...")

    print(f"Tuned model name: {sft_tuning_job.tuned_model_name}")
    print(f"Tuned model endpoint name: {sft_tuning_job.tuned_model_endpoint_name}")
    print(f"Experiment: {sft_tuning_job.experiment}")


def chat():
    print("chat()")

    # Get the finetuned model endpoint from Vertex AI
    MODEL_ENDPOINT = \
        "projects/129349313346/locations/us-central1/endpoints/3319822527953371136"

    generative_model = GenerativeModel(MODEL_ENDPOINT)

    query = "How can I lose weight?"
    print("query: ", query)
    response = generative_model.generate_content(
        [query],  # Input prompt
        generation_config=generation_config,  # Configuration settings
        stream=False,  # Enable streaming for responses
    )
    generated_text = response.text
    print("Fine-tuned LLM Response:", generated_text)


def main(args=None):
    print("CLI Arguments:", args)

    if args.train:
        train()

    if args.chat:
        chat()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--train",
        action="store_true",
        help="Train model",
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Chat with model",
    )

    args = parser.parse_args()

    main(args)