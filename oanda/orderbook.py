"""Orderbook related helpers for the Oanda API."""

from oandapyV20.endpoints.orderbook import OrderBook

from .client import OandaClient


class OrderBookService:
    """High level interface for fetching orderbook data."""

    def __init__(self, client: OandaClient) -> None:
        self._client = client

    def fetch(self, instrument: str) -> dict:
        """Retrieve the orderbook for the given instrument."""
        request = OrderBook(instrument=instrument)
        return self._client.request(request)


__all__ = ["OrderBookService"]

