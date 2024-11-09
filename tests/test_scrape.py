import pytest
from src.data_scraping import scrape
import requests
import os


def test_scrape_real_site():
    url = 'https://wholebrainhealth.org/exercise-and-brain-health/?gad_source=1&gclid=Cj0KCQiArby5BhCDARIsAIJvjIRzQvo-9defVqZe7r-aZXOCUjeN3xAeXGwdfFqsYQL3wmAF3Xaq0fIaAiO7EALw_wcB'
    os.mkdir('articles')
    assert scrape.get_article_content(url, 'test_file') is None


def test_scrape_fake_site():
    url = 'thisisafakeurl'
    with pytest.raises(requests.exceptions.RequestException) as exception:
        scrape.get_article_content(url, 'test_file')
