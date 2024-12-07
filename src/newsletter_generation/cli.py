import os
import argparse
from datetime import date
from google.cloud import storage
# Vertex AI
import vertexai
from vertexai.generative_models import GenerativeModel

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
BUCKET_NAME = "gain-newsletters"
BUCKET_FOLDER = "newsletters_raw"
CONTEXT_BUCKET = "gain-ft-articles"
OUTPUT_FOLDER = "output"
GENERATIVE_MODEL = "gemini-1.5-flash-001"

vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 8192,  # Maximum number of tokens for output
    "temperature": 0.2,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}

# Initialize the GenerativeModel with specific system instructions
SYSTEM_INSTRUCTION = (
    "You are an AI assistant with expert knowledge about everything "
    "related to health and fitness. When answering a query:\n"
    "1. Write as if you are an accomplished fitness journalist/expert "
    "with the latest knowledge about research and trends in the field."
    "A few important points to remember:\n"
    "- You are an expert in health and fitness and should leverage all "
    "the knowledge you have.\n"
    "- Do not write about topics unrelated to health and fitness.\n"
    "Your goal is to provide accurate, helpful information about health "
    "and fitness to the readers."
)
generative_model = GenerativeModel(
    GENERATIVE_MODEL, system_instruction=[SYSTEM_INSTRUCTION]
)


def upload_file(bucket_name, source_file_path, destination_file_path):
    try:
        # Initialize client
        storage_client = storage.Client()

        # Get target destination
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_file_path)

        # Upload file to cloud and delete locally
        blob.upload_from_filename(source_file_path)
        print(f"\n{source_file_path} uploaded to GCP bucket")

        os.remove(source_file_path)
        print(f"{source_file_path} DELETED locally")

    except Exception:
        print(f"\nError uploading file {source_file_path} to GCP bucket")


def send_to_bucket(bucket_name=BUCKET_NAME,
                   source_folder=OUTPUT_FOLDER,
                   destination_folder=BUCKET_FOLDER):

    # Loop through local articles and upload
    for filename in os.listdir(source_folder):
        print(f"Uploading {filename} to GCP bucket")
        source_file_path = os.path.join(source_folder, filename)
        destination_file_path = os.path.join(destination_folder, filename)

        if os.path.isfile(source_file_path):
            upload_file(bucket_name, source_file_path, destination_file_path)


def generate_newsletter():
    print("Generating newsletter...")

    INPUT_PROMPT = (
        "Generate a 250-500 word newsletter about a recent development within "
        "health and fitness. Make your writing clear and concise, and try to "
        "make the contents of the newsletter understandable for the average "
        "person, not just someone with extensive previous knowledge about "
        "the specific topic within health and fitness. Choose a relatively "
        "specific topic to avoid the newsletter content becoming too broad "
        "and generic. Some examples of topics that could be good are: "
        "heart rate monitoring during exercise, vegetarian diets and "
        "their health consequences, the best exercises to do for your "
        "core strength. Please do not write about those specific topics, "
        "but use them as a guideline for the types of topics that would "
        "be relevant for the newsletter."
    )

    print("INPUT_PROMPT: ", INPUT_PROMPT)
    response = generative_model.generate_content(
        [INPUT_PROMPT],
        generation_config=generation_config,
        stream=False,
    )
    generated_text = response.text
    print("LLM Response:", generated_text)
    todays_date = date.today()
    title = "newsletter_" + str(todays_date) + ".txt"
    output_file_path = "output/" + title
    try:
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(generated_text)
        print(f"Generated text saved to {output_file_path}")
        send_to_bucket()
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


def main(args=None):
    print("CLI Arguments:", args)

    if args.generate_newsletter:
        generate_newsletter()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--generate_newsletter",
        action="store_true",
        help="Generate daily newsletter",
    )

    args = parser.parse_args()

    main(args)
