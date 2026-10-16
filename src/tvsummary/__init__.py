"""TVMaze summary package."""

from .aggregations import (
    Aggregation,
    AverageRating,
    GenreList,
    LanguageCount,
)
from .models import TVShow
from .report import build_summary, save_summary
from .sources import TVMazeSource

__all__ = [
    "Aggregation",
    "AverageRating",
    "GenreList",
    "LanguageCount",
    "TVMazeSource",
    "TVShow",
    "build_summary",
    "save_summary",
]
