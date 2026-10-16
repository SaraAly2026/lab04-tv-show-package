"""Entry point for the TVMaze summary application."""


from tvsummary.config import TVMAZE_URL
from tvsummary.sources import TVMazeSource
from tvsummary.aggregations import (
    LanguageCount,
    AverageRating,
    GenreList,
)
from tvsummary.report import build_summary, save_summary
from tvsummary.exceptions import (
    DataFetchError,
    DataValidationError,
    ReportWriteError,
)

import logging

from tvsummary.logging_config import setup_logging


logger = logging.getLogger(__name__)


def main():
    """Fetch, aggregate, and save TV show data."""

    source = TVMazeSource()
    setup_logging()
    logger.info("Starting TVMaze summary application")

    
    try:
        shows = source.fetch()
        logger.info("Downloaded %d TV shows", len(shows))
       
    except (DataFetchError, DataValidationError) as error:
        logger.error("TVMaze data error: %s", error)
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

    try:
        save_summary(summary)
        logger.info("Summary report saved successfully")
    except ReportWriteError as error:
        logger.error("Report saving error: %s", error)
        return

    print("TVMaze summary completed successfully.")


if __name__ == "__main__":
    main()