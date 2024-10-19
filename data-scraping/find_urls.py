import pandas as pd
import os
import json
from typing import Optional
from phi.tools import Toolkit
from phi.utils.log import logger
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.email import EmailTools
from phi.tools.googlesearch import GoogleSearch

# Import OpenAPI key
json_path = os.path.join("..", "secrets", "opensecret.json")
with open(json_path, "r") as file:
    config = json.load(file)
api_key = config["OPENAI_API_KEY"]
os.environ['OPENAI_API_KEY'] = api_key

assistant = Assistant(llm = OpenAIChat(model="gpt-4o-mini"),
                      tools=[GoogleSearch()],
                      show_tool_calls=True,
                      description = """You are an advanced AI-powered agent, designed to efficiently manage and complete complex tasks by dividing them into smaller, manageable subtasks. Your objective is to receive an input, analyze and break it down into distinct tasks, and then execute each task using the most appropriate tools available at your disposal. Once all tasks are completed, you must provide a final summary indicating whether the overall task was completed successfully or not.

Guidelines:

Task Analysis: Upon receiving an input, analyze it thoroughly to understand the requirements and objectives.

Task Division: Break down the input into logical and manageable subtasks, considering dependencies and prioritizing them accordingly.

Tool Selection: For each subtask, identify and utilize the best tool or method available in your toolkit, including but not limited to external APIs, databases, or other software agents.

Execution: Implement each subtask independently, ensuring accuracy and efficiency.

Monitoring & Error Handling: Continuously monitor the execution of each subtask. If a subtask fails, attempt to resolve the issue or select an alternative approach.

Final Assessment: After all subtasks are executed, assess whether the overall task is complete. Provide a clear final response indicating "Task Complete" or "Task Incomplete," along with any relevant details or outcomes.

Optimization: Where possible, optimize your approach to reduce time, resources, or improve the quality of the output.""")

prompt = f"""
            Generate a list of 100 URLs of articles related to health, fitness, diet, and exercise. These articles
            can be published papers, blogs, editorials, or scientific reports. Pay special attention that each URL really
            links to an article that can be accessed publicly. Include nothing else in the list except for these URLs.
"""

assistant.print_response(prompt)