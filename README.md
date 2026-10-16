# TVMaze TV Show Summary — Lab 04: Harden Your Package

This project builds on my Lab 03 TVMaze Python package by adding automated testing, custom exceptions, logging, type checking, linting, configuration management, and reproducible output.

The application downloads TV show data from the TVMaze API, calculates summary statistics, and saves the results as JSON.

## Data source

- API: https://api.tvmaze.com/shows?page=0
- Each record represents one TV show.
- The application currently retrieves page 0 of the API.

## Setup

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate tvsummary
```

Install the pinned dependencies and the package:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

The Conda environment uses Python 3.11 and the `conda-forge` channel.

## Run

Run the application from the repository root:

```bash
python -m tvsummary.main --config config/tvsummary.toml
```

A successful run creates or updates:

- `data/processed/summary.json`
- `data/processed/run_info.json`

The summary contains the source URL, record count, language counts, average rating, sorted unique genres, and a deterministic selection of featured shows.

## Check it

Run the four Lab 04 quality checks:

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
```

The tests are designed to run offline without making live API requests.

## Settings

Application settings are stored in `config/tvsummary.toml`.

| Setting | Purpose |
|---|---|
| `source_url` | TVMaze API endpoint |
| `timeout` | HTTP request timeout |
| `output_folder` | Directory for generated reports |
| `seed` | Random seed for reproducible featured shows |
| `sample_size` | Number of featured shows to select |
| `log_level` | Logging level |

The settings are loaded into a frozen `Settings` dataclass.

## Errors and exit codes

The application uses custom exceptions to describe expected failures.

| Exception | When it occurs |
|---|---|
| `TVSummaryError` | Base class for application errors |
| `ConfigurationError` | Configuration file is missing or invalid |
| `DataFetchError` | The API request fails |
| `DataValidationError` | The API response has an unexpected structure |
| `ReportWriteError` | A report cannot be written |

The main entry point returns:

- **0** when the application completes successfully.
- **1** when an expected application error occurs.

Expected failures produce an error message beginning with `Error:` instead of an uncaught traceback.

For example, running with a missing configuration file:

```bash
python -m tvsummary.main --config config/missing.toml
```

produces an error and exits with code 1.

## Reproducing a run

The application uses the `seed` and `sample_size` settings to select featured shows deterministically.

With the same input records and settings, the selected featured shows are the same. The other summary calculations are also deterministic for the same input data.

The `run_info.json` file records the application settings, Python version, and installed versions of the testing and quality-checking tools.

Live API data can change over time, so reproducing the exact numerical results also requires the same source data.

## What tests cover

The offline pytest suite covers:

- TV show records with missing or malformed values.
- Language, rating, and genre aggregations using handmade data.
- Parameterized test cases.
- Custom exception handling.
- Report generation and writing to temporary directories.
- Deterministic featured-show selection.
- Main entry-point error handling and exit codes.
- Logging of expected configuration errors.

One area not covered by the offline tests is the reliability or availability of the live TVMaze API.

## Package layout

- `config/tvsummary.toml` — Application settings.
- `src/tvsummary/config.py` — Configuration loading and validation.
- `src/tvsummary/exceptions.py` — Custom exception classes.
- `src/tvsummary/logging_setup.py` — Logging configuration.
- `src/tvsummary/models.py` — TV show model and data cleaning.
- `src/tvsummary/sources.py` — TVMaze API retrieval and response validation.
- `src/tvsummary/aggregations.py` — Summary calculations.
- `src/tvsummary/report.py` — JSON reporting and reproducibility information.
- `src/tvsummary/main.py` — Command-line entry point.
- `src/tvsummary/py.typed` — Marker for typed package support.
- `tests/` — Offline pytest suite.
- `data/raw/` — Reserved for raw data.
- `data/processed/` — Generated reports.

## Design choices

The `TVShow` class represents an individual TV show and handles missing or malformed record values.

The `TVMazeSource` class separates HTTP requests from data aggregation and report generation.

The abstract `Aggregation` class defines a shared `compute()` interface. `LanguageCount`, `AverageRating`, and `GenreList` implement this interface using inheritance and polymorphism.

The report builder calls `compute()` on aggregation objects without needing to know their concrete subclasses.

The package uses a `src` layout, editable installation, explicit type annotations, and automated quality checks.

## Known limitations

- Only page 0 of the TVMaze API is retrieved.
- A live run requires an internet connection.
- TVMaze data can change between runs.
- Automatic HTTP retries are not implemented.
- The offline test suite does not verify live API availability.
- The required Python 3.11 environment must be verified separately from the development virtual environment.