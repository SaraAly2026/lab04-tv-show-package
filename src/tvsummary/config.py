from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# TVMaze API configuration
TVMAZE_URL = "https://api.tvmaze.com/shows?page=0"
REQUEST_TIMEOUT = 15

# Output configuration
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "summary.json"