"""Helpers for loading historical market data."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


def load_data(csv_path: str | Path) -> Optional[pd.DataFrame]:
    """Load OHLCV data from a CSV file into a DataFrame."""

    path = Path(csv_path)
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except pd.errors.ParserError:
        return None
