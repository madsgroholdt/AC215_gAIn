import requests
# from src.data_scraping.scrape import get_article_content


def test_testfunction():
    print('Testing function...')
    test_response = requests.post(
        "http://localhost:5002/test")
    test_result = test_response.json()["result"]
    assert test_result, f"Expected TRUE, got {test_result}"
