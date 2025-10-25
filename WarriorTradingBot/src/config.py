"""Configuration constants for the Warrior Trading style strategies."""

TRADING_START_HOUR = 7
"""int: Start of the trading window in Eastern Time."""

TRADING_END_HOUR = 11
"""int: End of the trading window in Eastern Time."""

MIN_PRICE = 1.0
"""float: Minimum share price considered by the scanner."""

MAX_PRICE = 10.0
"""float: Maximum share price considered by the scanner."""

MAX_FLOAT = 20_000_000
"""int: Maximum acceptable public float for candidate stocks."""

RELATIVE_VOLUME_MIN = 5.0
"""float: Minimum relative volume to qualify for the watchlist."""

RISK_PER_TRADE = 0.05
"""float: Fraction of account equity to risk per trade."""

DAILY_MAX_LOSS = 0.10
"""float: Daily drawdown limit that forces the system to halt trading."""

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
"""Default MACD periods used across indicator calculations."""
