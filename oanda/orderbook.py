"""Orderbook related helpers for the Oanda API."""

from __future__ import annotations

from typing import Dict, List

from oandapyV20 import API
from oandapyV20.endpoints import accounts, orderbook
from oandapyV20.exceptions import V20Error

from .client import OandaClient


class OrderBookService:
    """High level interface for fetching orderbook data."""

    def __init__(self, client: OandaClient) -> None:
        self._client = client

    def fetch(self, instrument: str) -> dict:
        """Retrieve the raw orderbook for the given instrument."""
        request = orderbook.OrderBook(instrument=instrument)
        return self._client.request(request)


def _resolve_account_id(api: API, account_id: str | None) -> str:
    """Fetch the first available account ID if one is not supplied.

    The official v20 Python library recommends resolving an account ID
    dynamically when it is not provided; see the discussion in
    https://github.com/oanda/v20-python/issues/46 for context.
    """

    if account_id:
        return account_id

    try:
        resp = api.request(accounts.AccountList())
        return resp["accounts"][0]["id"]
    except Exception as exc:  # pragma: no cover - network failure
        raise ValueError("No account ID available; set OANDA_ACCOUNT_ID") from exc


def get_orderbook(instrument: str, depth: int) -> Dict[str, object]:
    """Fetch and parse orderbook levels for an instrument.

    Parameters
    ----------
    instrument:
        The instrument name, e.g. ``"XAU_USD"``.
    depth:
        Number of price levels to return for each side of the book.

    Returns
    -------
    Dict[str, object]
        Parsed order book containing metadata and bid/ask levels suitable for
        consumption by Telegram handlers.
    """

    if depth <= 0:
        raise ValueError("depth must be a positive integer")

    from config.settings import settings

    if not settings.oanda_token:
        raise ValueError("OANDA_TOKEN is not configured")

    api = API(access_token=settings.oanda_token)
    account_id = _resolve_account_id(api, settings.oanda_account_id)

    try:
        resp = api.request(orderbook.OrderBook(instrument=instrument))
    except V20Error as exc:  # pragma: no cover - depends on API response
        raise ValueError(f"invalid instrument: {instrument}") from exc

    ob = resp.get("orderBook", {})
    mid_price = float(ob.get("price", 0.0))
    bucket_width = float(ob.get("bucketWidth", 0.0))
    buckets = ob.get("buckets", [])

    bids: List[Dict[str, float]] = []
    asks: List[Dict[str, float]] = []

    for b in buckets:
        price = float(b["price"])
        long_pct = float(b.get("longCountPercent", 0.0))
        short_pct = float(b.get("shortCountPercent", 0.0))

        if price <= mid_price:
            bids.append({"price": price, "volume": long_pct})
        else:
            asks.append({"price": price, "volume": short_pct})

    bids = sorted(bids, key=lambda x: x["price"], reverse=True)[:depth]
    asks = sorted(asks, key=lambda x: x["price"])[:depth]

    return {
        "instrument": ob.get("instrument", instrument),
        "account_id": account_id,
        "time": ob.get("time"),
        "price": mid_price,
        "bucket_width": bucket_width,
        "bids": bids,
        "asks": asks,
    }


__all__ = ["OrderBookService", "get_orderbook"]

