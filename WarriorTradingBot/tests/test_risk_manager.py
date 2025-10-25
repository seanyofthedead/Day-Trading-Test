"""Tests for risk management logic."""

from ..src import config
from ..src.strategy.risk_manager import RiskManager


def test_halt_after_daily_loss():
    """Risk manager should halt when daily loss exceeds threshold."""

    manager = RiskManager(config)
    manager.register_trade(-config.DAILY_MAX_LOSS - 0.01)
    assert manager.check_should_halt() is True


def test_halt_after_three_losses():
    """Three consecutive losses should trigger a halt."""

    manager = RiskManager(config)
    manager.register_trade(-0.01)
    manager.register_trade(-0.01)
    manager.register_trade(-0.01)
    assert manager.check_should_halt() is True
