"""Command-line entry point for the TVMaze summary application."""

import argparse
import logging
import sys

from .aggregations import AverageRating, GenreList, LanguageCount
from .config import load_settings
from .exceptions import TVSummaryError
from .logging_setup import configure_logging
from .report import (
    build_summary,
    save_run_info,
    save_summary,
    select_featured_shows,
)
from .sources import TVMazeSource

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Run the application and return an exit code."""
    parser = argparse.ArgumentParser(description="TVMaze summary")
    parser.add_argument("--config", default=None)
    args = parser.parse_args(argv)

    try:
        settings = load_settings(args.config)
        configure_logging(settings.log_level)

        logger.info("Starting TVMaze summary application")

        source = TVMazeSource(
            url=settings.source_url,
            timeout=settings.timeout,
        )
        shows = source.fetch()

        aggregations = {
            "language_counts": LanguageCount(),
            "average_rating": AverageRating(),
            "genres": GenreList(),
        }
        results = build_summary(shows, aggregations)

        summary = {
            "source_url": settings.source_url,
            "record_count": len(shows),
            **results,
            "featured_shows": select_featured_shows(
                shows, settings.seed, settings.sample_size
            ),
        }

        from pathlib import Path

        output_path = (
            Path(__file__).resolve().parents[2]
            / settings.output_folder
            / "summary.json"
        )
        save_summary(summary, output_path)
        save_run_info(settings, output_path.parent)

        logger.info("Summary report saved successfully")
        print("TVMaze summary completed successfully.")
        return 0

    except TVSummaryError as error:
        logger.error("Application failed: %s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
