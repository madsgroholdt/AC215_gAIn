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


# def test_combine_sentences_with_custom_buffer():
#     sentences = [
#         {"sentence": "The"},
#         {"sentence": "quick"},
#         {"sentence": "brown"},
#         {"sentence": "fox"},
#         {"sentence": "jumps"},
#     ]

#     expected_output = [
#         {"sentence": "The", "combined_sentence": "The quick brown"},
#         {"sentence": "quick", "combined_sentence": "The quick brown fox"},
#         {"sentence": "brown", "combined_sentence": "The quick brown fox jumps"},
#         {"sentence": "fox", "combined_sentence": "quick brown fox jumps"},
#         {"sentence": "jumps", "combined_sentence": "brown fox jumps"},
#     ]

#     result = combine_sentences(sentences, buffer_size=2)
#     assert result == expected_output
