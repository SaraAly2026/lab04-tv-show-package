"""Aggregation classes for TV show summaries."""

from abc import ABC, abstractmethod
from collections import Counter


class Aggregation(ABC):
    """Base class for TV show aggregations."""

    @abstractmethod
    def compute(self, shows):
        """Calculate a summary from TV show objects."""
        pass


class LanguageCount(Aggregation):
    """Count TV shows by language."""

    def compute(self, shows):
        return dict(
            Counter(
                show.language
                for show in shows
                if show.language is not None
            )
        )


class AverageRating(Aggregation):
    """Calculate the average of available ratings."""

    def compute(self, shows):
        total_rating = 0
        rating_count = 0

        for show in shows:
            if show.rating is not None:
                total_rating += show.rating
                rating_count += 1

        if rating_count > 0:
            return total_rating / rating_count

        return None


class GenreList(Aggregation):
    """Return sorted unique TV show genres."""

    def compute(self, shows):
        genres = {
            genre
            for show in shows
            for genre in show.genres
        }

        return sorted(genres)