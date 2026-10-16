"""Fetch TV show data from TVMaze."""

import requests

from .config import REQUEST_TIMEOUT, TVMAZE_URL
from .exceptions import DataFetchError, DataValidationError
from .models import TVShow


class TVMazeSource:
    """Download and convert TV show records from TVMaze."""

    def __init__(self, url=TVMAZE_URL):
        self.url = url

    def fetch(self):
        """Return a list of TVShow objects."""
        try:
            response = requests.get(
                self.url,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise DataFetchError(
                f"Failed to download TV shows: {error}"
            ) from error

        try:
            data = response.json()
        except ValueError as error:
            raise DataValidationError(
                "TVMaze returned invalid JSON."
            ) from error

        if not isinstance(data, list):
            raise DataValidationError(
                "Expected a list of TV shows."
            )

        return [TVShow(record) for record in data]