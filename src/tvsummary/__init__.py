"""TVMaze summary package."""

from .models import TVShow
from .sources import TVMazeSource
from .aggregations import (
    Aggregation,
    LanguageCount,
    AverageRating,
    GenreList,
)
from .report import build_summary, save_summary

__all__ = [
    "TVShow",
    "TVMazeSource",
    "Aggregation",
    "LanguageCount",
    "AverageRating",
    "GenreList",
    "build_summary",
    "save_summary",
]