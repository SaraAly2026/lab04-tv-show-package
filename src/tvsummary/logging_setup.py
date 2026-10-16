"""Configure logging for the TV summary application."""

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure application logging at the requested level."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
