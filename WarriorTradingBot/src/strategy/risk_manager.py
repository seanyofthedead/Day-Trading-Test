"""Risk management utilities enforcing daily limits and halt conditions."""

from __future__ import annotations

from typing import Any


class RiskManager:
    """Track cumulative performance and determine when trading should stop."""

    def __init__(self, config_module: Any) -> None:
        self.config = config_module
        self.daily_loss = 0.0
        self.consecutive_losses = 0

    def register_trade(self, profit_loss: float) -> None:
        """Update loss counters after a trade closes."""

        if profit_loss < 0:
            self.daily_loss += abs(profit_loss)
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

    def check_should_halt(self) -> bool:
        """Return True if daily drawdown or consecutive loss limits are exceeded."""

        if self.daily_loss >= self.config.DAILY_MAX_LOSS:
            return True
        # Halt after three consecutive losses by default.
        return self.consecutive_losses >= 3
