import pytest
from typing import List
from src.models.semantic_splitter import combine_sentences


def test_combine_sentences_with_default_buffer():
    sentences = [
        {"sentence": "Hello"},
        {"sentence": "world"},
        {"sentence": "from"},
        {"sentence": "pytest"},
    ]

    expected_output = [
        {"sentence": "Hello", "combined_sentence": "Hello world"},
        {"sentence": "world", "combined_sentence": "Hello world from"},
        {"sentence": "from", "combined_sentence": "world from pytest"},
        {"sentence": "pytest", "combined_sentence": "from pytest"},
    ]
    result = combine_sentences(sentences)
    assert result == expected_output


def test_combine_sentences_with_empty_input():
    sentences = []

    expected_output = []

    result = combine_sentences(sentences)
    assert result == expected_output


def test_combine_sentences_with_single_sentence():
    sentences = [{"sentence": "Single"}]

    expected_output = [{"sentence": "Single", "combined_sentence": "Single"}]

    result = combine_sentences(sentences)
    assert result == expected_output
