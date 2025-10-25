"""Entry point for orchestrating scanning, strategy evaluation, and execution."""

from __future__ import annotations

from typing import List

from . import config
from . import scanner
from .strategy.gap_and_go import GapAndGoStrategy
from .strategy.micro_pullback import MicroPullbackStrategy
from .strategy.risk_manager import RiskManager
from .utils.logger import get_logger


def main() -> None:
    """Run the high-level trading loop with placeholder logic.

    The function documents the intended control flow:

    1. Initialize utilities such as the logger, risk manager, and strategies.
    2. Run the pre-market scanner between 7:00 and 9:30 AM to assemble a watchlist.
    3. After the opening bell, monitor live data and evaluate each strategy for entry/exit signals.
    4. Relay orders through the NinjaTrader connector when signals trigger.
    5. Halt trading if the risk manager indicates daily limits have been reached.

    Actual data ingestion, scheduling, and order-routing integrations remain TODOs for future work.
    """

    logger = get_logger(__name__)
    risk_manager = RiskManager(config)
    strategies = [
        GapAndGoStrategy(config),
        MicroPullbackStrategy(config),
    ]

    logger.info("Starting Warrior Trading agent scaffold.")

    watchlist: List[str] = scanner.scan_premarket()
    logger.info("Premarket watchlist: %s", watchlist)

    # TODO: Implement live data loop. For now we simply log the intended actions.
    logger.info("Transitioning to live trading window from %s to %s EST.", config.TRADING_START_HOUR, config.TRADING_END_HOUR)
    logger.info("Strategies loaded: %s", [strategy.__class__.__name__ for strategy in strategies])

    if risk_manager.check_should_halt():
        logger.warning("Risk limits breached on startup; halting trading loop.")
        return

    logger.info("Trading loop placeholder complete.")


if __name__ == "__main__":
    main()
