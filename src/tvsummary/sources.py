"""Fetch TV show data from TVMaze."""

import requests

from .config import TVMAZE_URL, REQUEST_TIMEOUT
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
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()

            data = response.json()

            if not isinstance(data, list):
                raise ValueError("Expected a list of TV shows.")

            return [TVShow(record) for record in data]

        except (requests.RequestException, ValueError) as error:
            raise RuntimeError(
                f"Failed to download TV shows: {error}"
            ) from error