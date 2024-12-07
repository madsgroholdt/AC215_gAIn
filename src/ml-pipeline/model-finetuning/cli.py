import argparse
import time
import vertexai
from vertexai.preview.tuning import sft

# Setup
GCP_PROJECT = "ac215-final-project"
GCS_BUCKET_NAME = "gain-ml-pipeline"
GCP_REGION = "us-central1"

DATASET = "gs:" + f"//{GCS_BUCKET_NAME}/processed_data"
TRAIN_DATASET = f"{DATASET}/train.jsonl"
VALIDATION_DATASET = f"{DATASET}/test.jsonl"


# Configuration settings for the content generation
GENERATIVE_SOURCE_MODEL = "gemini-1.5-pro-002"  # base model
generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.75,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}


def train(wait_for_job=True):
    print("train()")

    vertexai.init(project=GCP_PROJECT, location=GCP_REGION)

    # Supervised Fine Tuning
    sft_tuning_job = sft.train(
        source_model=GENERATIVE_SOURCE_MODEL,
        train_dataset=TRAIN_DATASET,
        validation_dataset=VALIDATION_DATASET,
        epochs=1,   # between 2-3
        adapter_size=4,
        learning_rate_multiplier=1.0,
        tuned_model_display_name="gain-finetuned",
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


def main(args=None):
    print("CLI Arguments:", args)

    if args.train:
        train()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--train",
        action="store_true",
        help="Train model",
    )

    args = parser.parse_args()

    main(args)
