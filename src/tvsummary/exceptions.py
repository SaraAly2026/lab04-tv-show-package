"""Custom exceptions for the TV summary package."""


class TVSummaryError(Exception):
    """Base exception for TV summary errors."""


class DataFetchError(TVSummaryError):
    """Raised when downloading TV show data fails."""


class DataValidationError(TVSummaryError):
    """Raised when downloaded data is invalid."""


class ConfigurationError(TVSummaryError):
    """Raised when application settings are invalid."""


class ReportWriteError(TVSummaryError):
    """Raised when saving a report fails."""
