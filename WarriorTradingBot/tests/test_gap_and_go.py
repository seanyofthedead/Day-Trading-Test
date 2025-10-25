"""Tests for the Gap and Go strategy skeleton."""

from ..src import config
from ..src.strategy.gap_and_go import GapAndGoStrategy


def test_gap_and_go_no_signal_by_default():
    """Without populated stock data the strategy should not trigger an entry."""

    strategy = GapAndGoStrategy(config)
    assert strategy.check_entry({}) is False
