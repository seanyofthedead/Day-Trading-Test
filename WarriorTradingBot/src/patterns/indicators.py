"""Indicator calculation helpers used across strategies."""

from __future__ import annotations

from typing import Iterable, List, Tuple

from .. import config


def compute_ema(prices: Iterable[float], period: int) -> List[float]:
    """Compute an exponential moving average for the given period.

    TODO:
        - Implement EMA using pandas or manual smoothing.
        - Handle warm-up periods by seeding with the first price or simple moving average.
    """

    return []


def compute_macd(prices: Iterable[float]) -> Tuple[List[float], List[float]]:
    """Return MACD and signal line series using default periods from :mod:`config`."""

    # TODO: Produce MACD histogram as well for strategy use.
    return [], []


def compute_vwap(prices: Iterable[float], volumes: Iterable[float]) -> List[float]:
    """Calculate the volume-weighted average price over the session."""

    # TODO: Maintain cumulative price*volume and volume totals for realistic computation.
    return []
