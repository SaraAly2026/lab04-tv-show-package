"""Build and save the TV show summary report."""

import importlib.metadata
import json
import platform
import random
from collections.abc import Mapping
from pathlib import Path

from .aggregations import Aggregation
from .config import Settings
from .exceptions import ReportWriteError
from .models import TVShow


def build_summary(
    shows: list[TVShow],
    aggregations: dict[str, Aggregation],
) -> dict[str, dict[str, int] | float | list[str] | None]:
    """Run aggregation objects and collect their results."""
    summary: dict[str, dict[str, int] | float | list[str] | None] = {}

    for key, aggregation in aggregations.items():
        summary[key] = aggregation.compute(shows)

    return summary


def select_featured_shows(
    shows: list[TVShow],
    seed: int,
    sample_size: int,
) -> list[str]:
    """Select show names reproducibly using a local random seed."""
    names = [show.name for show in shows]
    rng = random.Random(seed)
    selected = rng.sample(names, k=min(sample_size, len(names)))
    return selected


def save_summary(
    summary: Mapping[str, object],
    output_path: Path,
) -> None:
    """Save the summary as a formatted JSON file."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(summary, file, indent=4, ensure_ascii=False)

    except (OSError, TypeError, ValueError) as error:
        raise ReportWriteError(f"Failed to save summary report: {error}") from error


def save_run_info(settings: Settings, output_folder: Path) -> None:
    """Save settings and software versions used for the run."""
    versions = {
        package: importlib.metadata.version(package)
        for package in ("pytest", "mypy", "ruff")
    }

    run_info = {
        "settings": {
            "source_url": settings.source_url,
            "timeout": settings.timeout,
            "output_folder": settings.output_folder,
            "seed": settings.seed,
            "sample_size": settings.sample_size,
            "log_level": settings.log_level,
        },
        "python_version": platform.python_version(),
        "tool_versions": versions,
    }

    output_path = output_folder / "run_info.json"

    try:
        output_folder.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(run_info, file, indent=4)
    except (OSError, TypeError, ValueError) as error:
        raise ReportWriteError(f"Failed to save run information: {error}") from error
