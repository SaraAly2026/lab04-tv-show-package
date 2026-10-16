
"""Tests for custom application exceptions."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

from tvsummary.exceptions import (
    DataFetchError,
    DataValidationError,
    ReportWriteError,
)
from tvsummary.report import save_summary
from tvsummary.sources import TVMazeSource


def test_network_failure():
    """A network error raises DataFetchError."""
    with (
        patch(
            "tvsummary.sources.requests.get",
            side_effect=requests.ConnectionError("Network unavailable"),
        ),
        pytest.raises(DataFetchError),
    ):
        TVMazeSource().fetch()


def test_invalid_json():
    """Invalid JSON raises DataValidationError."""
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.side_effect = ValueError("Invalid JSON")

    with (
        patch("tvsummary.sources.requests.get", return_value=response),
        pytest.raises(DataValidationError),
    ):
        TVMazeSource().fetch()


def test_invalid_response_structure():
    """A non-list response raises DataValidationError."""
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"error": "Invalid response"}

    with (
        patch("tvsummary.sources.requests.get", return_value=response),
        pytest.raises(DataValidationError),
    ):
        TVMazeSource().fetch()


def test_report_write_failure(tmp_path):
    """A file-writing error raises ReportWriteError."""
    output_path = tmp_path / "summary.json"

    with (
        patch.object(
            Path,
            "open",
            side_effect=PermissionError("Permission denied"),
        ),
        pytest.raises(ReportWriteError),
    ):
        save_summary({"record_count": 2}, output_path)
