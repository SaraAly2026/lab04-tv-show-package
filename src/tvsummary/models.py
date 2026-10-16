"""TV show data model."""


class TVShow:
    """Represent a TV show and clean its data."""

    def __init__(self, raw_data):
        if not isinstance(raw_data, dict):
            raw_data = {}

        self.name = (
            raw_data.get("name")
            if isinstance(raw_data.get("name"), str)
            else None
        )

        self.language = (
            raw_data.get("language")
            if isinstance(raw_data.get("language"), str)
            else None
        )

        genres = raw_data.get("genres")
        self.genres = (
            [genre for genre in genres if isinstance(genre, str)]
            if isinstance(genres, list)
            else []
        )

        rating_info = raw_data.get("rating")
        rating = (
            rating_info.get("average")
            if isinstance(rating_info, dict)
            else None
        )

        self.rating = (
            rating if isinstance(rating, (int, float)) else None
        )

    def __str__(self):
        return self.name or "Unknown TV Show"