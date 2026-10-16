"""Shared fixtures for offline tests."""

import pytest

from tvsummary.models import TVShow


@pytest.fixture
def sample_shows() -> list[TVShow]:
    """Provide three TV shows without accessing the network."""
    return [
        TVShow(
            {
                "name": "Show A",
                "language": "English",
                "genres": ["Drama"],
                "rating": {"average": 8.0},
            }
        ),
        TVShow(
            {
                "name": "Show B",
                "language": "French",
                "genres": ["Comedy"],
                "rating": {"average": 7.0},
            }
        ),
        TVShow(
            {
                "name": "Show C",
                "language": "English",
                "genres": [],
                "rating": {"average": None},
            }
        ),
    ]
