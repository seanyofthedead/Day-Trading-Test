"""Tests for candlestick helper functions."""

from ..src.patterns import candlesticks


def test_is_doji_detects_small_body():
    """A nearly equal open and close should be recognized as a Doji."""

    assert candlesticks.is_doji(1.0, 1.001, 1.05, 0.95)


def test_is_bullish_engulfing_basic_case():
    """Basic engulfing structure should return True."""

    assert candlesticks.is_bullish_engulfing(1.0, 0.9, 0.85, 1.05)
