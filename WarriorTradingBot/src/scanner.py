"""Market scanner module for identifying Warrior Trading-style candidates."""

from __future__ import annotations

from typing import List

from . import config


def scan_premarket() -> List[str]:
    """Scan for top pre-market gappers that meet float, price, and volume criteria.

    Returns:
        List[str]: Symbols that should populate the morning watchlist.

    TODO:
        - Connect to a market data API or NinjaTrader data feed for pre-market quotes.
        - Filter for stocks with price between ``config.MIN_PRICE`` and ``config.MAX_PRICE``.
        - Require float under ``config.MAX_FLOAT`` and relative volume above ``config.RELATIVE_VOLUME_MIN``.
        - Prefer symbols with credible news catalysts (press releases, filings, etc.).
    """

    return []


def scan_realtime() -> List[str]:
    """Monitor real-time session for momentum breakouts and volume spikes.

    Returns:
        List[str]: Active symbols showing continuation potential during live trading.

    TODO:
        - Stream live quotes and volume metrics from the NinjaTrader connector.
        - Detect flat-top breakouts, high-of-day breaks, and unusual volume bursts.
        - Prioritize symbols already on the pre-market watchlist to reduce noise.
    """

    return []
