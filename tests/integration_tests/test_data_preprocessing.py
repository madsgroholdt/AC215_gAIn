# import pytest
# from src.model_finetuner.cli import chat
import requests

print('The test file is being run!!')


def test_function():
    url = "http://0.0.0.0:5003/llm-rag/chats/38d61d80-bbf9-4849-a7e9-f4decacc279d"
    headers = {
        "X-test-session": "test-session"
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.json())
