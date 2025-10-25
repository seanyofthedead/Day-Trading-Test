"""Performance evaluation helpers for simulated trading sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class PerformanceEvaluator:
    """Track trade outcomes and compute performance statistics."""

    trades: List[float] = field(default_factory=list)

    def record_trade(self, profit_loss: float) -> None:
        """Append a completed trade result."""

        self.trades.append(profit_loss)

    def get_win_rate(self) -> float:
        """Return the percentage of trades that were profitable."""

        if not self.trades:
            return 0.0
        wins = sum(1 for trade in self.trades if trade > 0)
        return wins / len(self.trades)

    def get_profit_factor(self) -> float:
        """Return the ratio of gross profits to gross losses."""

        gross_profit = sum(trade for trade in self.trades if trade > 0)
        gross_loss = abs(sum(trade for trade in self.trades if trade < 0))
        if gross_loss == 0:
            return float("inf") if gross_profit > 0 else 0.0
        return gross_profit / gross_loss

    def get_max_drawdown(self) -> float:
        """Compute the largest drop from a running peak in cumulative P/L."""

        max_peak = 0.0
        max_drawdown = 0.0
        cumulative = 0.0
        for trade in self.trades:
            cumulative += trade
            max_peak = max(max_peak, cumulative)
            max_drawdown = max(max_drawdown, max_peak - cumulative)
        return max_drawdown

    def report(self) -> dict:
        """Return a summary of key performance metrics."""

        return {
            "total_trades": len(self.trades),
            "win_rate": self.get_win_rate(),
            "profit_factor": self.get_profit_factor(),
            "max_drawdown": self.get_max_drawdown(),
        }
