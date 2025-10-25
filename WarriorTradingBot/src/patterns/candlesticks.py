"""Candlestick pattern detection helpers."""

from __future__ import annotations


def is_doji(open_price: float, close_price: float, high_price: float, low_price: float, threshold: float = 0.02) -> bool:
    """Return True if the candle qualifies as a Doji.

    A Doji forms when the open and close are nearly equal, indicating indecision. The ``threshold``
    parameter controls how close the prices must be relative to the trading range.
    """

    # TODO: Use ``high_price`` and ``low_price`` to evaluate relative body size.
    return abs(open_price - close_price) <= threshold * (high_price - low_price if high_price != low_price else 1)


def is_bullish_engulfing(prev_open: float, prev_close: float, open_price: float, close_price: float) -> bool:
    """Return True when a bullish engulfing pattern appears.

    The current candle must open below the previous close and close above the previous open.
    """

    # TODO: Include volume confirmation and wick analysis if desired.
    return open_price < prev_close and close_price > prev_open


def is_hammer(open_price: float, close_price: float, high_price: float, low_price: float) -> bool:
    """Identify a hammer-style reversal candlestick.

    A hammer typically has a small body near the top of the range with a long lower wick.
    """

    # TODO: Incorporate configurable ratios for wick-to-body size comparisons.
    body = abs(close_price - open_price)
    lower_wick = min(open_price, close_price) - low_price
    upper_wick = high_price - max(open_price, close_price)
    return lower_wick > 2 * body and upper_wick < body
