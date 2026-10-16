"""Tests for the application entry point."""

from pathlib import Path

from tvsummary.main import main


def test_main_missing_config_returns_one(
    tmp_path: Path,
    capsys,
) -> None:
    """A missing configuration must return exit code 1."""
    missing_file = tmp_path / "missing.toml"

    exit_code = main(["--config", str(missing_file)])

    assert exit_code == 1
    assert capsys.readouterr().err.startswith("Error:")


def test_main_missing_config_has_no_traceback(
    tmp_path: Path,
    capsys,
) -> None:
    """Expected failures must not display a Python traceback."""
    missing_file = tmp_path / "missing.toml"

    main(["--config", str(missing_file)])

    captured = capsys.readouterr()
    assert "Traceback" not in captured.err
    assert len(captured.err.strip().splitlines()) == 1


def test_main_logs_configuration_error(
    tmp_path: Path,
    caplog,
) -> None:
    """Verify that main logs an expected configuration failure."""
    import logging

    missing_file = tmp_path / "missing.toml"

    with caplog.at_level(logging.ERROR):
        exit_code = main(["--config", str(missing_file)])

    assert exit_code == 1
    assert "Application failed:" in caplog.text
