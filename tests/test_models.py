"""Tests for the TVShow data model."""

from tvsummary.models import TVShow


def test_valid_show():
    show = TVShow({
        "name": "Example Show",
        "language": "English",
        "genres": ["Drama", "Comedy"],
        "rating": {"average": 8.5},
    })

    assert show.name == "Example Show"
    assert show.language == "English"
    assert show.genres == ["Drama", "Comedy"]
    assert show.rating == 8.5


def test_missing_name():
    show = TVShow({})

    assert show.name == "Unknown"


def test_invalid_genres():
    show = TVShow({"genres": "Drama"})

    assert show.genres == []


def test_missing_rating():
    show = TVShow({"rating": {"average": None}})

    assert show.rating is None