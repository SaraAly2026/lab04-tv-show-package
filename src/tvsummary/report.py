"""Build and save the TV show summary report."""

import json

from .config import OUTPUT_PATH


def build_summary(shows, aggregations):
    """Run aggregation objects and collect their results."""
    summary = {}

    for key, aggregation in aggregations.items():
        summary[key] = aggregation.compute(shows)

    return summary


def save_summary(summary, output_path=OUTPUT_PATH):
    """Save the summary as a formatted JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)