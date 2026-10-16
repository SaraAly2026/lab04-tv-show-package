
# TVMaze TV Show Summary — Lab 03

This project refactors my Lab 02 TVMaze program into an installable Python package using object-oriented programming (OOP). It downloads TV show records, calculates summary statistics, and saves the results to JSON.

## Data source

- URL: https://api.tvmaze.com/shows?page=0
- Each record represents one TV show.
- The API returned approximately 240 records during testing.

## Setup

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate tvsummary
```

Install the pinned dependencies and the package:

```bash
pip install -r requirements.txt
pip install -e .
```

## Run

```bash
python main.py
```

Output: `data/processed/summary.json`

The summary contains the source URL, record count, language counts, average rating, and sorted unique genres.

## Test

Run the offline unit tests:

```bash
python -m unittest discover -s tests
```

The tests check language counts, average ratings, unique genres, and handling of missing values.

## Layout

- `src/tvsummary/__init__.py` — Exposes the package's public classes and functions.
- `src/tvsummary/config.py` — Stores the API URL, request timeout, and output path.
- `src/tvsummary/models.py` — Defines the `TVShow` class and cleans record values.
- `src/tvsummary/sources.py` — Downloads TVMaze records and converts them into `TVShow` objects.
- `src/tvsummary/aggregations.py` — Defines the aggregation base class and specialized subclasses.
- `src/tvsummary/report.py` — Builds the summary and writes JSON output.
- `main.py` — Connects the components and handles download failures.
- `tests/test_tvsummary.py` — Contains offline unit tests.
- `data/raw/` — Reserved for raw data.
- `data/processed/` — Stores the generated summary.

## What moved where

| Lab 02 function | Lab 03 location |
|---|---|
| `fetch_shows()` | `TVMazeSource.fetch()` in `sources.py` |
| `count_shows_by_language()` | `LanguageCount.compute()` in `aggregations.py` |
| `calculate_average_rating()` | `AverageRating.compute()` in `aggregations.py` |
| `get_show_names()` | `TVShow.name` in `models.py` |
| `get_unique_genres()` | `GenreList.compute()` in `aggregations.py` |
| `build_summary()` | `build_summary()` in `report.py`, with metadata assembled in `main.py` |
| `write_summary()` | `save_summary()` in `report.py` |
| `main()` | `main()` in `main.py` |

## Design choices

The `TVShow` class represents one record and handles missing or malformed values when an object is created.

The `TVMazeSource` class is responsible for downloading data and creating `TVShow` objects. It keeps network access separate from aggregation and reporting.

The abstract `Aggregation` class defines a shared `compute()` interface. `LanguageCount`, `AverageRating`, and `GenreList` inherit from it and override this method.

Polymorphism is used when the report builder loops over aggregation objects and calls `compute()` without checking their subclass types.

To add another aggregation, a new subclass can inherit from `Aggregation`, implement `compute()`, and be added to the aggregations dictionary in `main.py`.

The package uses a `src` layout and supports editable installation with `pip install -e .`.

## Known limitations

- Only page 0 of the TVMaze API is downloaded.
- An internet connection is required for live data retrieval.
- TVMaze data can change over time, affecting the summary values.
- Failed downloads produce an error message, but automatic retries are not implemented.
- The old Lab 02 summary is retained at the repository root for comparison.
