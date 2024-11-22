import pytest
from vector_db.semantic_splitter import (combine_sentences,
                                         calculate_cosine_distances)


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


def test_calculate_cosine_distances_basic():
    sentences = [
        {"combined_sentence_embedding": [1, 0, 0]},
        {"combined_sentence_embedding": [0, 1, 0]},
        {"combined_sentence_embedding": [0, 0, 1]},
    ]

    expected_distances = [1.0, 1.0]
    expected_output = [
        {"combined_sentence_embedding": [1, 0, 0], "distance_to_next": 1.0},
        {"combined_sentence_embedding": [0, 1, 0], "distance_to_next": 1.0},
        {"combined_sentence_embedding": [0, 0, 1]},
    ]

    distances, result = calculate_cosine_distances(sentences)
    assert distances == expected_distances
    assert result == expected_output


def test_calculate_cosine_distances_single_sentence():
    sentences = [
        {"combined_sentence_embedding": [1, 0, 0]},
    ]

    expected_distances = []
    expected_output = [{"combined_sentence_embedding": [1, 0, 0]}]

    distances, result = calculate_cosine_distances(sentences)
    assert distances == expected_distances
    assert result == expected_output


def test_calculate_cosine_distances_correct_sentence_updates():
    sentences = [
        {"combined_sentence_embedding": [1, 0, 0]},
        {"combined_sentence_embedding": [0.5, 0.5, 0]},
        {"combined_sentence_embedding": [0, 1, 0]},
    ]

    expected_distances = [0.2929, 0.2929]
    expected_output = [
        {"combined_sentence_embedding": [
            1, 0, 0], "distance_to_next": pytest.approx(0.2929, rel=1e-3)},
        {"combined_sentence_embedding": [
            0.5, 0.5, 0], "distance_to_next": pytest.approx(0.2929, rel=1e-3)},
        {"combined_sentence_embedding": [0, 1, 0]},
    ]

    distances, result = calculate_cosine_distances(sentences)
    assert distances == pytest.approx(expected_distances, rel=1e-3)
    assert result == expected_output
