"""Tests for report generation and reproducibility."""

from pathlib import Path

from tvsummary.models import TVShow
from tvsummary.report import save_summary, select_featured_shows


def test_featured_shows_same_seed(
    sample_shows: list[TVShow],
) -> None:
    """The same seed and input must produce identical selections."""
    first = select_featured_shows(sample_shows, seed=42, sample_size=2)
    second = select_featured_shows(sample_shows, seed=42, sample_size=2)

    assert first == second
    assert len(first) == 2
    assert all(name in {"Show A", "Show B", "Show C"} for name in first)


def test_save_summary_uses_tmp_path(tmp_path: Path) -> None:
    """A report can be saved to a temporary folder."""
    output_path = tmp_path / "summary.json"
    summary = {"record_count": 3}

    save_summary(summary, output_path)

    assert output_path.exists()
    assert '"record_count": 3' in output_path.read_text(encoding="utf-8")
