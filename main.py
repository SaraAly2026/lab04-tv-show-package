"""Entry point for the TVMaze summary application."""

from tvsummary.config import TVMAZE_URL
from tvsummary.sources import TVMazeSource
from tvsummary.aggregations import (
    LanguageCount,
    AverageRating,
    GenreList,
)
from tvsummary.report import build_summary, save_summary


def main():
    """Fetch, aggregate, and save TV show data."""

    source = TVMazeSource()

    try:
        shows = source.fetch()
    except RuntimeError as error:
        print(f"Download failed: {error}")
        return

    aggregations = {
        "language_counts": LanguageCount(),
        "average_rating": AverageRating(),
        "genres": GenreList(),
    }

    results = build_summary(shows, aggregations)

    summary = {
        "source_url": TVMAZE_URL,
        "record_count": len(shows),
        **results,
    }

    save_summary(summary)

    print(f"Downloaded {len(shows)} records.")
    print("Summary saved successfully.")


if __name__ == "__main__":
    main()