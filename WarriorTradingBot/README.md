# Warrior Trading Strategy Agent

This repository scaffolds an autonomous trading assistant inspired by Warrior Trading's momentum playbook. The Python package organizes scanning, pattern recognition, risk management, and orchestration logic, while a NinjaTrader 8 NinjaScript (C#) stub handles order routing and data flow for the simulator. Each module currently contains descriptive docstrings and TODO markers that guide future implementation of the full trading workflow.

## Getting started

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Review the configuration values in `src/config.py` to adapt account size, float filters, and trading window settings to your preferences.
4. Run the placeholder unit tests with `pytest` to confirm the scaffold imports correctly.
5. Import `src/simulation/ninja_connector.cs` into NinjaTrader 8 when you are ready to flesh out the live simulator bridge.

## Project layout

```
WarriorTradingBot/
├── data/                  # Sample datasets for backtesting and offline evaluation
├── logs/                  # Runtime logs written by the Python agent
├── notebooks/             # Optional research and visualization notebooks
├── src/                   # Core Python package for scanning, strategies, and utilities
├── tests/                 # Pytest suite for module-level verification
└── requirements.txt       # Python dependency specification
```

## Next steps

The scaffold emphasizes Warrior Trading heuristics such as:

- Focusing on small-cap, low-float gappers between $1 and $10 with strong catalysts.
- Running scanners between 7:00 AM and 11:00 AM EST to build a daily watchlist.
- Confirming entries with candlestick/price action patterns and indicators like MACD, VWAP, and EMAs.
- Enforcing strict risk rules (2:1 reward-to-risk, max 5% account risk per trade, and 10% daily loss cap).

Implementers can now iterate on the TODO sections to connect real data feeds, refine pattern detection, and integrate order execution through NinjaTrader.
