import os
from pathlib import Path

from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)


def _get_timeout() -> float:
    raw_timeout = os.getenv("REQUEST_TIMEOUT", "10")
    try:
        return float(raw_timeout)
    except ValueError:
        return 10.0


BASE_URL = os.getenv("BASE_URL", "http://localhost:3001").rstrip("/")
REQUEST_TIMEOUT = _get_timeout()
