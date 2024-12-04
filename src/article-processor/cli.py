import os
import argparse
import pandas as pd
import json
import glob
from sklearn.model_selection import train_test_split
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
GENERATIVE_MODEL = "gemini-1.5-flash-002"
OUTPUT_FOLDER = "data"
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
INPUT_FOLDER = "raw_articles/"
# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 8192,  # Maximum number of tokens for output
    "temperature": 1,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}

# System Prompt
SYSTEM_INSTRUCTION = """Generate a set of 5 to 10 question-answer pairs about a \
      given article in English, adopting the tone and perspective of an \
      experienced fitness coach. Adhere to the following guidelines:

1. Question Independence:
- Ensure each question-answer pair is completely independent and self-contained.
- Do not reference other questions or answers within the set.
- Each Q&A pair should be understandable without any additional context.
- The number of questions should be proportional to the length of the article. \
      For longer articles, generate more questions, and for shorter articles, \
      generate fewer questions. Very short articles should have no more than \
      1-2 questions.
- If an article is empty, generate no questions.

2. Technical Information:
- Incorporate detailed information about fitness principles, workout \
      techniques, and health optimization strategies.
- Include specific data such as ideal heart rate zones for different \
      types of exercise, nutrient timing, and recommendations for various \
      fitness levels.
- Explain the scientific principles behind exercise, nutrition, and recovery.
- Discuss the role of physiological and biomechanical processes in achieving \
      health goals.
- Reference relevant terms, equipment, and methodologies used in fitness coaching.

3. Expert Perspective and Personalization:
- Embody the voice of a passionate fitness coach with a deep understanding of \
      diverse health and fitness topics.
- Infuse responses with encouragement and actionable insights.
- Reference real-life applications, examples, and success stories where relevant.

4. Content Coverage:
- Techniques for cardio, strength training, flexibility, and mobility.
- Fitness goal optimization, including weight loss, muscle gain, and endurance \
      improvement.
- Nutrition tips for various fitness objectives, including macronutrient \
      breakdowns and hydration strategies.
- Injury prevention, safe exercise practices, and recovery methods.
- Tailored advice for different fitness levels, age groups, and health conditions.
- Mental well-being and its connection to physical health.
- The role of technology in fitness, including activity trackers and apps.

5. Tone and Style:
- Use a motivational, authoritative, yet approachable tone that conveys years \
    of coaching experience.
- Incorporate dynamic and engaging phrases that inspire action and dedication.
- Emphasize a supportive and inclusive approach to fitness.

6. Complexity and Depth:
- Provide a mix of basic advice and advanced technical insights.
- Include lesser-known tips, expert techniques, and scientific explanations.
- Offer nuanced perspectives that reflect deep understanding of fitness and health.

7. Question Types:
- Include a variety of question types (e.g., "what", "how", "why", "can you \
      explain", "what's the best approach for").
- Formulate questions as if someone is passionate about fitness and seeking \
      practical, science-based guidance.
- Ensure questions cover a wide range of topics within the fitness domain, \
      including technical aspects.

8. Accuracy and Relevance:
- Extract information accurately and ensure alignment with the article's content.
- Focus on scientifically validated principles in fitness and health.

Output Format:
Provide the Q&A pairs in JSON format, with each pair as an object containing \
      'question' and 'answer' fields, within a JSON array.
Follow these strict guidelines:
1. Use double quotes for JSON keys and string values.
2. For any quotation marks within the text content, use single quotes (') \
      instead of double quotes. Avoid quotation marks.
3. If a single quote (apostrophe) appears in the text, escape it with a \
      backslash (\').
4. Ensure there are no unescaped special characters that could break \
      the JSON structure.
5. Avoid any invalid control characters that JSON decode will not be able \
    to decode.

Here's a sample JSON output for a fitness-related article:
```json
[
{
    "question": "What are the benefits of incorporating strength training \
          into a fitness routine?",
    "answer": "Great question! This powerhouse activity not only builds muscle \
          but also boosts your metabolism, improves bone density, and enhances \
          your overall functional strength. It's like giving your body a \
          superhero upgrade! Plus, strength training can reduce the risk of \
          injuries by supporting your joints and improving posture. Whether \
          you're lifting free weights, using resistance bands, or working \
          with machines, you're setting yourself up for long-term success."
},
{
    "question": "How can someone determine if they've exercised enough in a day?",
    "answer": "The answer depends on your goals, but here's a quick guide. For \
        general health, aim for at least 150 minutes of moderate-intensity \
        exercise or 75 minutes of vigorous activity each week, as recommended \
        by the CDC. If you're focused on a specific goal like building \
        endurance or weight loss, consider monitoring your heart rate, \
        step count, or calories burned. Tools like fitness trackers and apps \
        can provide real-time feedback to help you stay on track."
}
]
```

Note: The sample JSON includes two Q&A pairs for brevity. Generate 5-10 pairs \
    for each article, following these guidelines. """


# Helper function to get articles from GCS
def download_articles():
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=INPUT_FOLDER)
    articles = []
    for blob in blobs:
        if blob.name.endswith('.txt'):  # Assuming articles are in text files
            content = blob.download_as_text()
            articles.append(content)
    return articles


def generate():
    print("generate()")

    # Make dataset folders
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Initialize Vertex AI project and location
    vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

    # Initialize the GenerativeModel with specific system instructions
    model = GenerativeModel(
        GENERATIVE_MODEL,
        system_instruction=[SYSTEM_INSTRUCTION]
    )

    # Download articles
    articles = download_articles()

    # Loop to generate and save the content
    for i, article in enumerate(articles):
        INPUT_PROMPT = f"""Generate diverse, informative, and engaging \
        question-answer pairs about health and fitness using the following \
        article and these guidelines. ARTICLE CONTENT: {article}."""

        print(f"Generating batch: {i}")

        try:
            responses = model.generate_content(
                [INPUT_PROMPT],  # Input prompt
                generation_config=generation_config,  # Configuration settings
                stream=False,  # Enable streaming for responses
            )
            generated_text = responses.text

            # Create a unique filename for each article
            file_name = f"{OUTPUT_FOLDER}/health_qa_{i}.txt"
            # Save
            with open(file_name, "w") as file:
                file.write(generated_text)
        except Exception as e:
            print(f"Error occurred while generating content: {e}")


def prepare():
    print("prepare()")

    # Get the generated files
    output_files = glob.glob(os.path.join(OUTPUT_FOLDER, "health_qa_*.txt"))
    output_files.sort()

    # Consolidate the data
    output_pairs = []
    errors = []
    for output_file in output_files:
        print("Processing file:", output_file)
        with open(output_file, "r") as read_file:
            text_response = read_file.read()

        text_response = text_response.replace("```json", "").replace("```", "")

        try:
            json_responses = json.loads(text_response)
            output_pairs.extend(json_responses)

        except Exception as e:
            errors.append({"file": output_file, "error": str(e)})

    print("Number of errors:", len(errors))
    print(errors[:5])

    # Save the dataset
    output_pairs_df = pd.DataFrame(output_pairs)
    output_pairs_df.drop_duplicates(subset=['question'], inplace=True)
    output_pairs_df = output_pairs_df.dropna()
    print("Shape:", output_pairs_df.shape)
    print(output_pairs_df.head())
    filename = os.path.join(OUTPUT_FOLDER, "instruct-dataset.csv")
    output_pairs_df.to_csv(filename, index=False)

    # Build training formats
    output_pairs_df['text'] = "human: " + output_pairs_df['question'] + "\n" \
        + "bot: " + output_pairs_df['answer']

    # Gemini Data prep
    output_pairs_df["contents"] = \
        output_pairs_df.apply(lambda row:
                              [{"role": "user", "parts": [{"text": row["question"]}]},
                               {"role": "model", "parts": [{"text": row["answer"]}]}],
                              axis=1)

    # Test train split
    df_train, df_test = train_test_split(output_pairs_df,
                                         test_size=0.1,
                                         random_state=42)
    df_train[["text"]].to_csv(os.path.join(OUTPUT_FOLDER, "train.csv"),
                              index=False)
    df_test[["text"]].to_csv(os.path.join(OUTPUT_FOLDER, "test.csv"),
                             index=False)

    # Gemini : Max numbers of examples in validation dataset: 256
    df_test = df_test[:256]

    # JSONL
    with open(os.path.join(OUTPUT_FOLDER, "train.jsonl"), "w") as json_file:
        json_file.write(df_train[["contents"]].to_json(orient='records', lines=True))
    with open(os.path.join(OUTPUT_FOLDER, "test.jsonl"), "w") as json_file:
        json_file.write(df_test[["contents"]].to_json(orient='records', lines=True))


def upload():
    print("upload()")

    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    timeout = 300

    data_files = glob.glob(os.path.join(OUTPUT_FOLDER, "*.jsonl")) + \
        glob.glob(os.path.join(OUTPUT_FOLDER, "*.csv"))
    data_files.sort()

    # Upload
    for index, data_file in enumerate(data_files):
        filename = os.path.basename(data_file)
        destination_blob_name = os.path.join("llm-finetune-dataset-small", filename)
        blob = bucket.blob(destination_blob_name)
        print("Uploading file:", data_file, destination_blob_name)
        blob.upload_from_filename(data_file, timeout=timeout)
        print("Removing local file:", data_file)
        os.remove(data_file)


def main(args=None):
    print("CLI Arguments:", args)

    if args.generate:
        generate()

    if args.prepare:
        prepare()

    if args.upload:
        upload()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate data",
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Prepare data",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload data to bucket",
    )

    args = parser.parse_args()

    main(args)
