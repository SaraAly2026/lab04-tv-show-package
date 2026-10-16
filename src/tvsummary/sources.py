"""Fetch TV show data from TVMaze."""

import logging

import requests

from .exceptions import DataFetchError, DataValidationError
from .models import TVShow

logger = logging.getLogger(__name__)


class TVMazeSource:
    """Download and convert TV show records from TVMaze."""

    def __init__(
        self,
        url: str,
        timeout: int,
    ) -> None:
        self.url = url
        self.timeout = timeout

    def fetch(self) -> list[TVShow]:
        """Return a list of TVShow objects."""
        logger.info("Fetching TV shows from %s", self.url)

        try:
            response = requests.get(
                self.url,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            logger.error("TVMaze request failed: %s", error)
            raise DataFetchError(f"Failed to download TV shows: {error}") from error

        try:
            data = response.json()
        except ValueError as error:
            logger.error("TVMaze returned invalid JSON")
            raise DataValidationError("TVMaze returned invalid JSON.") from error

        if not isinstance(data, list):
            logger.warning("TVMaze returned an unexpected response structure")
            logger.error("TVMaze response was not a list")
            raise DataValidationError("Expected a list of TV shows.")

        logger.debug("Received %d raw TV show records", len(data))
        shows = [TVShow(record) for record in data]
        logger.info("Successfully loaded %d TV shows", len(shows))
        return shows
