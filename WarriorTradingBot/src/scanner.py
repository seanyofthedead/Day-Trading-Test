"""Market scanner module for identifying Warrior Trading-style candidates."""

from __future__ import annotations

import json
import threading
import time
from typing import Dict, List

from . import config
from .utils.logger import get_logger

# Module-level logger for scanner activity
logger = get_logger(__name__)

# Thread-safe storage for the latest market metrics keyed by ticker symbol.
market_data: Dict[str, Dict[str, float]] = {}

# Lock used to guard concurrent access to ``market_data`` when background
# threads update it via the data feed bridge.
data_lock = threading.Lock()

# Minimum gap percentage expressed as a decimal (5% by default).
MIN_GAP_RATIO = 0.05


def _init_data_feed() -> None:
    """Set up the bridge that populates :data:`market_data` with live quotes.

    The project supports two bridge patterns, both of which remain partially
    stubbed until the NinjaTrader integration is finalized:

    * WebSocket bridge – NinjaTrader connects to a local WebSocket endpoint and
      streams JSON payloads. A future implementation should launch the server
      and pass each message to :func:`_handle_data_message`.
    * File-based bridge – NinjaTrader (or a simulator) appends JSON lines to a
      file on disk. We spawn a watcher thread that tails the file and parses the
      payloads in near real-time.
    """

    if getattr(config, "USE_WEBSOCKET", False):
        logger.info("Initializing WebSocket data feed bridge (TODO implementation)...")
        # TODO: Spin up a WebSocket server and invoke ``_handle_data_message``
        # for every payload received from NinjaTrader.
    elif getattr(config, "DATA_FEED_FILE", None):
        feed_file = getattr(config, "DATA_FEED_FILE")
        logger.info("Initializing file-based data feed from %s", feed_file)
        thread = threading.Thread(target=_watch_data_file, args=(feed_file,), daemon=True)
        thread.start()
    else:
        logger.warning("No data feed configured; scanner will operate on static data only.")


def _watch_data_file(filepath: str) -> None:
    """Tail ``filepath`` for JSON-encoded symbol updates.

    Each line is expected to be a JSON object containing the following keys:
    ``symbol``, ``price``, ``prev_close``, ``volume``, ``avg_vol``, ``float``,
    and optional boolean flags ``news``/``catalyst`` and ``runner``/
    ``former_runner``.
    """

    try:
        with open(filepath, "r", encoding="utf-8") as handle:
            handle.seek(0, 2)  # jump to end of file
            while True:
                line = handle.readline()
                if not line:
                    time.sleep(0.5)
                    continue

                try:
                    payload = json.loads(line.strip())
                except json.JSONDecodeError:
                    logger.debug("Skipping malformed line from data feed: %s", line.strip())
                    continue

                _handle_data_message(payload)
    except FileNotFoundError:
        logger.error("Data feed file not found at %s", filepath)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Unexpected error while watching data file %s: %s", filepath, exc)


def _handle_data_message(message: Dict[str, object]) -> None:
    """Merge an incoming message into :data:`market_data`."""

    symbol = message.get("symbol")
    if not isinstance(symbol, str):
        return

    with data_lock:
        entry = market_data.setdefault(symbol, {})
        entry.update(
            {
                "price": float(message.get("price", entry.get("price", 0.0))),
                "prev_close": float(message.get("prev_close", entry.get("prev_close", 0.0))),
                "volume": float(message.get("volume", entry.get("volume", 0.0))),
                "avg_vol": float(message.get("avg_vol", entry.get("avg_vol", 1.0))),
                "float": float(message.get("float", entry.get("float", 0.0))),
                "news": bool(message.get("news") or message.get("catalyst")),
                "runner": bool(message.get("runner") or message.get("former_runner")),
            }
        )

    logger.debug("Market data update for %s: %s", symbol, market_data[symbol])


def _qualifies(symbol: str, data: Dict[str, float]) -> bool:
    """Return ``True`` if ``symbol`` satisfies the Warrior Trading filters."""

    price = data.get("price", 0.0)
    prev_close = data.get("prev_close", 0.0)
    volume = data.get("volume", 0.0)
    avg_vol = data.get("avg_vol", 1.0) or 1.0
    stock_float = data.get("float", 0.0)
    has_news = bool(data.get("news"))
    is_runner = bool(data.get("runner"))

    if price < config.MIN_PRICE or price > config.MAX_PRICE:
        return False
    if prev_close <= 0:
        return False

    gap_ratio = (price - prev_close) / prev_close
    if gap_ratio < MIN_GAP_RATIO:
        return False

    rel_volume = volume / avg_vol
    if rel_volume < config.RELATIVE_VOLUME_MIN:
        return False

    if stock_float and stock_float > config.MAX_FLOAT:
        return False

    if not has_news and not is_runner:
        return False

    return True


def _sort_key(symbol: str) -> float:
    """Return the gap ratio for ``symbol`` used to order qualified results."""

    data = market_data.get(symbol, {})
    price = data.get("price")
    prev_close = data.get("prev_close")
    if not price or not prev_close:
        return 0.0
    return (price - prev_close) / prev_close


def scan_premarket() -> List[str]:
    """Scan pre-market data for gap-and-go candidates."""

    logger.info("Scanning premarket for qualifying stocks...")
    qualified: List[str] = []

    with data_lock:
        for symbol, data in market_data.items():
            if data.get("volume", 0.0) <= 0:
                continue
            if _qualifies(symbol, data):
                qualified.append(symbol)
                _log_qualification("Premarket", symbol, data)

    qualified.sort(key=_sort_key, reverse=True)
    logger.info("Premarket scan complete. %s stocks qualified: %s", len(qualified), qualified)
    return qualified


def scan_realtime() -> List[str]:
    """Scan live session data for ongoing momentum plays."""

    logger.info("Scanning real-time market for qualifying stocks...")
    qualified: List[str] = []

    with data_lock:
        for symbol, data in market_data.items():
            if data.get("volume", 0.0) <= 0:
                continue
            if _qualifies(symbol, data):
                qualified.append(symbol)
                _log_qualification("Real-time", symbol, data)

    qualified.sort(key=_sort_key, reverse=True)
    logger.info("Real-time scan complete. %s stocks qualified: %s", len(qualified), qualified)
    return qualified


def _log_qualification(stage: str, symbol: str, data: Dict[str, float]) -> None:
    """Write an informational log entry for a qualifying symbol."""

    price = data.get("price", 0.0)
    prev_close = data.get("prev_close", 0.0) or 1.0
    gap_pct = (price - prev_close) / prev_close * 100
    avg_vol = data.get("avg_vol", 1.0) or 1.0
    rel_vol = data.get("volume", 0.0) / avg_vol
    logger.info(
        "%s QUALIFIED: %s - Price $%.2f, Gap %.1f%%, Float %s, RelVol %.1fx, Catalyst=%s",
        stage,
        symbol,
        price,
        gap_pct,
        data.get("float", "N/A"),
        rel_vol,
        data.get("news") or data.get("runner"),
    )


# Kick off the data feed bridge when the module is imported so that external
# callers receive live updates without manual initialization.
_init_data_feed()

