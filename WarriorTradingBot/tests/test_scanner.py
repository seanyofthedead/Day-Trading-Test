"""Tests for the scanner module placeholders."""

from ..src import scanner


def test_scan_premarket_returns_list():
    """Premarket scan should return a list (even if empty)."""

    result = scanner.scan_premarket()
    assert isinstance(result, list)


def test_scan_realtime_returns_list():
    """Realtime scan should return a list (even if empty)."""

    result = scanner.scan_realtime()
    assert isinstance(result, list)
