"""Offline unit tests for the TV summary package."""

import unittest

from tvsummary.models import TVShow
from tvsummary.aggregations import (
    LanguageCount,
    AverageRating,
    GenreList,
)


class TestTVSummary(unittest.TestCase):

    def setUp(self):
        """Create sample TV shows without using the API."""
        self.shows = [
            TVShow({
                "name": "Show A",
                "language": "English",
                "rating": {"average": 8.0},
                "genres": ["Drama", "Comedy"],
            }),
            TVShow({
                "name": "Show B",
                "language": "English",
                "rating": {"average": 6.0},
                "genres": ["Drama"],
            }),
            TVShow({
                "name": "Show C",
                "language": "Japanese",
                "rating": {"average": None},
                "genres": ["Anime"],
            }),
        ]

    def test_language_counts(self):
        """Check that shows are counted by language."""
        result = LanguageCount().compute(self.shows)

        self.assertEqual(
            result,
            {"English": 2, "Japanese": 1}
        )

    def test_average_rating(self):
        """Check that missing ratings are ignored."""
        result = AverageRating().compute(self.shows)

        self.assertEqual(result, 7.0)

    def test_unique_genres(self):
        """Check that genres are unique and sorted."""
        result = GenreList().compute(self.shows)

        self.assertEqual(
            result,
            ["Anime", "Comedy", "Drama"]
        )

    def test_missing_values(self):
        """Check that missing values are handled safely."""
        show = TVShow({})

        self.assertIsNone(show.language)
        self.assertIsNone(show.rating)
        self.assertEqual(show.genres, [])


if __name__ == "__main__":
    unittest.main()