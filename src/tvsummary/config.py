"""Load and validate application settings."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from .exceptions import ConfigurationError

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    source_url: str
    timeout: int
    output_folder: str
    seed: int
    sample_size: int
    log_level: str


def load_settings(config_path: str | Path | None = None) -> Settings:
    """Read settings from a TOML file and validate required fields."""
    path = (
        Path(config_path)
        if config_path is not None
        else PROJECT_ROOT / "config" / "tvsummary.toml"
    )

    try:
        with path.open("rb") as file:
            data = tomllib.load(file)

        values = data["settings"]

        settings = Settings(
            source_url=values["source_url"],
            timeout=values["timeout"],
            output_folder=values["output_folder"],
            seed=values["seed"],
            sample_size=values["sample_size"],
            log_level=values["log_level"],
        )

        if (
            not isinstance(settings.source_url, str)
            or not settings.source_url.strip()
            or type(settings.timeout) is not int
            or settings.timeout <= 0
            or not isinstance(settings.output_folder, str)
            or not settings.output_folder.strip()
            or type(settings.seed) is not int
            or type(settings.sample_size) is not int
            or settings.sample_size <= 0
            or not isinstance(settings.log_level, str)
            or settings.log_level.upper()
            not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        ):
            raise ConfigurationError("Invalid configuration values")

        return settings

    except (OSError, tomllib.TOMLDecodeError, KeyError, TypeError) as error:
        raise ConfigurationError(
            f"Cannot load configuration from {path}: {error}"
        ) from error
