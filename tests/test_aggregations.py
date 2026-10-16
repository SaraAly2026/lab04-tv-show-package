"""Additional tests for TV show aggregations."""

import pytest

from tvsummary.aggregations import (
    AverageRating,
    GenreList,
    LanguageCount,
)
from tvsummary.models import TVShow


def test_no_shows_language_counts():
    assert LanguageCount().compute([]) == {}


def test_no_ratings_returns_none():
    shows = [
        TVShow({"name": "Show A", "rating": {"average": None}}),
        TVShow({"name": "Show B", "rating": {"average": None}}),
    ]

    assert AverageRating().compute(shows) is None


@pytest.mark.parametrize(
    "ratings, expected",
    [
        ([6.0, 8.0], 7.0),
        ([5.0, 7.0, 9.0], 7.0),
    ],
)
def test_average_rating_cases(ratings, expected):
    shows = [
        TVShow({"rating": {"average": rating}})
        for rating in ratings
    ]

    assert AverageRating().compute(shows) == expected


def test_genres_are_sorted_and_unique():
    shows = [
        TVShow({"genres": ["Drama", "Comedy"]}),
        TVShow({"genres": ["Drama", "Action"]}),
    ]

    assert GenreList().compute(shows) == [
        "Action",
        "Comedy",
        "Drama",
    ]