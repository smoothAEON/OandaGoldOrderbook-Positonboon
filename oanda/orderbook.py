from oandapyV20.endpoints.orderbook import OrderBook
from .client import get_client


def fetch_orderbook(oanda_token: str, instrument: str):
    """Fetch the orderbook for a given instrument."""
    client = get_client(oanda_token)
    r = OrderBook(instrument=instrument)
    client.request(r)
    return r.response
