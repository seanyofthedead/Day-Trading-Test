"""Plotting utilities for visual analysis of strategies."""

from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt


def plot_candlestick(data) -> None:
    """Placeholder for rendering a candlestick chart from OHLCV data."""

    # TODO: Implement using mplfinance or manual Matplotlib drawing.
    plt.figure()
    plt.title("Candlestick Plot TODO")
    plt.close()


def plot_equity_curve(profits: Iterable[float]) -> None:
    """Plot a cumulative P/L curve for the provided profit series."""

    cumulative = []
    total = 0.0
    for profit in profits:
        total += profit
        cumulative.append(total)

    plt.figure()
    plt.plot(cumulative)
    plt.title("Equity Curve TODO")
    plt.close()
