import os
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.file import FileTools
from phi.tools.googlesearch import GoogleSearch
from google.cloud import secretmanager
from google.cloud import storage

# Import OpenAPI key
client = secretmanager.SecretManagerServiceClient()
name = "projects/ac215-final-project/secrets/OPENAI/versions/latest"
response = client.access_secret_version(request={"name": name})
secret = response.payload.data.decode("UTF-8")
os.environ['OPENAI_API_KEY'] = secret

assistant = Assistant(
    llm=OpenAIChat(model="gpt-4o-mini"),
    tools=[GoogleSearch(), FileTools()],
    show_tool_calls=True,
    description=(
        "You are an advanced AI-powered agent, designed to efficiently "
        "manage and complete complex tasks by dividing them into smaller, "
        "manageable subtasks. Your objective is to receive an input, "
        "analyze and break it down into distinct tasks, and then execute "
        "each task using the most appropriate tools available at your "
        "disposal. Once all tasks are completed, you must provide a final "
        "summary indicating whether the overall task was completed "
        "successfully or not.\n\n"

        "Guidelines:\n\n"

        "Task Analysis: Upon receiving an input, analyze it thoroughly to "
        "understand the requirements and objectives.\n\n"

        "Task Division: Break down the input into logical and manageable "
        "subtasks, considering dependencies and prioritizing them "
        "accordingly.\n\n"

        "Tool Selection: For each subtask, identify and utilize the best "
        "tool or method available in your toolkit, including but not "
        "limited to external APIs, databases, or other software agents.\n\n"

        "Execution: Implement each subtask independently, ensuring accuracy "
        "and efficiency.\n\n"

        "Monitoring & Error Handling: Continuously monitor the execution of "
        "each subtask. If a subtask fails, attempt to resolve the issue or "
        "select an alternative approach.\n\n"

        "Final Assessment: After all subtasks are executed, assess whether "
        "the overall task is complete. Provide a clear final response "
        "indicating 'Task Complete' or 'Task Incomplete,' along with any "
        "relevant details or outcomes.\n\n"

        "Optimization: Where possible, optimize your approach to reduce "
        "time, resources, or improve the quality of the output."
    )
)


def get_urls(bucket, num_urls=100):
    prompt = f"Generate a list of at least {num_urls} URLs of articles related to \
                health, fitness, diet, and exercise. These articles can be published \
                papers, blogs, editorials, or scientific reports. Pay special \
                attention that each URL really links to an article that can be \
                accessed publicly. Additionally, articles that have been published \
                recently are preferable, but this is not a strict limitation. \
                Include nothing else in the list except for \
                these URLs. Again, return just a list of the URLs, no text \
                besides the URLs, and each URL should be separated by a comma and a \
                new line character. There should be {num_urls} entries. \
                Export a CSV file containing all of these URLs and name this \
                file 'urls.csv'."

    assistant.print_response(prompt)
    print("URLs collected")

    # Send URLs to GCS
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob('urls/urls.csv')
    blob.upload_from_filename('urls.csv')
    print("URLs uploaded to GCP bucket")
