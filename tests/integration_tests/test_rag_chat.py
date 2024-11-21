# import pytest
import requests


def test_endpoint_return_status():
    url = "http://0.0.0.0:9000/llm-rag/chats?limit=5"
    headers = {
        "X-Session-ID": "test-session"
    }
    response = requests.get(url, headers=headers)

    assert response.status_code == 200


def test_endpoint_limit():
    url = "http://0.0.0.0:9000/llm-rag/chats?limit=5"
    headers = {
        "X-Session-ID": "test-session"
    }
    response = requests.get(url, headers=headers)

    result = response.json()

    assert len(result) <= 5


def test_chat_history_return_status():
    chat_id = "38d61d80-bbf9-4849-a7e9-f4decacc279d"
    url = f"http://0.0.0.0:9000/llm-rag/chats/{chat_id}"
    headers = {
        "X-Session-ID": "test-session"
    }
    response = requests.get(url, headers=headers)

    assert response.status_code == 200


def test_chat_history_return_value():
    chat_id = "38d61d80-bbf9-4849-a7e9-f4decacc279d"
    url = f"http://0.0.0.0:9000/llm-rag/chats/{chat_id}"
    headers = {
        "X-Session-ID": "test-session"
    }
    response = requests.get(url, headers=headers)

    result = response.json()
    answer = result['messages'][1]['content']

    assert answer[:5] == "Hello"


def test_new_chat_llm_return_status():
    url = "http://0.0.0.0:9000/llm-rag/chats"
    headers = {
        "accept": "application/json",
        "X-Session-ID": "test-session",
        "Content-Type": "application/json"
    }

    prompt = {"content": "Should I go for a run today?"}

    response = requests.post(url, headers=headers,
                             json=prompt)

    assert response.status_code == 200


def test_new_chat_llm_return_value():
    url = "http://0.0.0.0:9000/llm-rag/chats"
    headers = {
        "accept": "application/json",
        "X-Session-ID": "test-session",
        "Content-Type": "application/json"
    }

    prompt = {"content": "Should I go for a run today?"}

    response = requests.post(url, headers=headers,
                             json=prompt)

    result = response.json()

    assert len(result['messages'][1]['content']) > 0


def test_continue_chat_return_status():
    chat_id = "38d61d80-bbf9-4849-a7e9-f4decacc279d"
    url = f"http://0.0.0.0:9000/llm-rag/chats/{chat_id}"
    headers = {
        "accept": "application/json",
        "X-Session-ID": "test-session",
        "Content-Type": "application/json"
    }
    prompt = {
        "content": "Summarize our conversation so far"
    }

    response = requests.get(url, headers=headers,
                            json=prompt)

    assert response.status_code == 200


def test_continue_chat_return_value():
    chat_id = "38d61d80-bbf9-4849-a7e9-f4decacc279d"
    url = f"http://0.0.0.0:9000/llm-rag/chats/{chat_id}"
    headers = {
        "accept": "application/json",
        "X-Session-ID": "test-session",
        "Content-Type": "application/json"
    }
    prompt = {
        "content": "Summarize our conversation so far"
    }

    response = requests.get(url, headers=headers,
                            json=prompt)

    result = response.json()
    answer = result['messages'][-1]['content']

    assert answer[:12] == "We discussed"
